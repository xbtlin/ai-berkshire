#!/usr/bin/env python3
"""financial_rigor.py 回归测试.

覆盖已修复的缺陷：

  BUG  Windows 控制台 GBK 编码崩溃
       verify_market_cap() 在偏差 > 5% 时打印 "❌ 警告"，U+274C 在 GBK
       控制台抛 UnicodeEncodeError 直接退出。

       危害尤其大：**崩溃的恰恰是「偏差超标」这条最该被看到的告警路径**。
       偏差正常时打印 ✅（U+2705）同样会崩，但用户至少能从退出码察觉；
       而在"验算失败"时静默退出，会让人误以为脚本没跑或跑过了。

  BUG  exact_calc 用 eval + float，"精确值"输出带浮点误差
       旧版 calc --expr '0.1 + 0.2' 输出 0.30000000000000004。
       现已重写为 AST 解析 + 全程 Decimal（见 TestExactCalcSemantics）。

运行：  python tests/test_financial_rigor.py
"""

import contextlib
import io
import os
import subprocess
import sys
import unittest
from decimal import Decimal

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'tools'))

import financial_rigor as F  # noqa: E402

_TOOLS = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'tools')


def _run(args, encoding='gbk'):
    """在模拟的 GBK 控制台下执行 financial_rigor.py。"""
    env = dict(os.environ)
    env['PYTHONIOENCODING'] = encoding
    env.pop('PYTHONUTF8', None)
    return subprocess.run(
        [sys.executable, os.path.join(_TOOLS, 'financial_rigor.py')] + args,
        capture_output=True, env=env)


class TestGbkConsoleSurvival(unittest.TestCase):

    def test_pass_path_prints_check_mark(self):
        """偏差 0%，打印 ✅（U+2705）——GBK 下不得崩溃。"""
        proc = _run(['verify-market-cap', '--price', '8.00',
                     '--shares', '500000000', '--reported', '4000000000',
                     '--currency', 'CNY'])
        self.assertEqual(proc.returncode, 0,
                         proc.stderr.decode('utf-8', 'replace')[-800:])
        self.assertNotIn(b'UnicodeEncodeError', proc.stderr)

    def test_fail_path_prints_cross_mark(self):
        """偏差超标，打印 ❌（U+274C）——这条路径是原 bug 的触发点。"""
        proc = _run(['verify-market-cap', '--price', '8.00',
                     '--shares', '500000000', '--reported', '40.00',
                     '--currency', 'CNY'])
        self.assertEqual(
            proc.returncode, 0,
            "偏差超标告警路径在 GBK 控制台崩溃了：\n"
            + proc.stderr.decode('utf-8', 'replace')[-800:])
        self.assertNotIn(b'UnicodeEncodeError', proc.stderr)
        self.assertIn('❌', proc.stdout.decode('utf-8', 'replace'),
                      "告警符号应当被输出（哪怕替换字符），而非静默退出")

    def test_warn_path_prints_warning_sign(self):
        """偏差 1%~5%，打印 ⚠️（U+26A0 U+FE0F，含变体选择符）。"""
        # 8.00 × 500,000,000 = 4,000,000,000；报告值放大 3% 触发警告档
        proc = _run(['verify-market-cap', '--price', '8.00',
                     '--shares', '500000000', '--reported', '4120000000',
                     '--currency', 'CNY'])
        self.assertEqual(proc.returncode, 0,
                         proc.stderr.decode('utf-8', 'replace')[-800:])
        self.assertNotIn(b'UnicodeEncodeError', proc.stderr)

    def test_cross_validate_under_gbk(self):
        proc = _run(['cross-validate', '--field', '2025营业收入',
                     '--values', '{"来源甲":1234567890.12,"来源乙":1234567890.12}',
                     '--unit', '元'])
        self.assertEqual(proc.returncode, 0,
                         proc.stderr.decode('utf-8', 'replace')[-800:])
        self.assertNotIn(b'UnicodeEncodeError', proc.stderr)

    def test_three_scenario_under_gbk(self):
        proc = _run(['three-scenario', '--price', '8.00', '--eps', '0.5000',
                     '--shares', '5.0000', '--growth', '0.15', '0.03', '-0.10',
                     '--pe', '22', '15', '10', '--years', '3',
                     '--currency', 'CNY'])
        self.assertEqual(proc.returncode, 0,
                         proc.stderr.decode('utf-8', 'replace')[-800:])
        self.assertNotIn(b'UnicodeEncodeError', proc.stderr)


class TestForceUtf8Stdio(unittest.TestCase):

    def test_idempotent(self):
        F._force_utf8_stdio()
        F._force_utf8_stdio()

    def test_tolerates_non_reconfigurable_stream(self):
        orig = sys.stdout
        try:
            sys.stdout = io.BytesIO()  # 没有 reconfigure 方法
            F._force_utf8_stdio()      # 不应抛异常
        finally:
            sys.stdout = orig


class TestMarketCapMathUnaffected(unittest.TestCase):
    """确认编码修复没有改动计算逻辑。"""

    def test_exact_match_returns_true(self):
        self.assertTrue(F.verify_market_cap(8.00, 500000000, 4000000000, 'CNY'))

    def test_gross_mismatch_returns_false(self):
        self.assertFalse(F.verify_market_cap(8.00, 500000000, 40.00, 'CNY'))


class TestExactCalcSemantics(unittest.TestCase):
    """exact_calc 从 eval+float 重写为 AST+Decimal 后的计算语义（#69）。"""

    def _calc(self, expr):
        with contextlib.redirect_stdout(io.StringIO()):
            return F.exact_calc(expr)

    def test_exact_calc_avoids_float_drift(self):
        """回归核心：旧版 0.1 + 0.2 的"精确值"是 0.30000000000000004。"""
        self.assertEqual(self._calc('0.1 + 0.2'), Decimal('0.3'))

    def test_exact_calc_supports_scientific_notation_and_parentheses(self):
        self.assertEqual(self._calc('(1.25e3 - 250) / 2'), Decimal('500'))

    def test_exact_calc_rejects_non_arithmetic_input(self):
        """去掉 eval 后，注入类输入必须被拒绝而非执行。"""
        self.assertIsNone(self._calc("__import__('os').system('echo unsafe')"))
        self.assertIsNone(self._calc("().__class__"))

    def test_exact_calc_integer_power(self):
        """复利常用：1.15**5 旧版可算，重写后不能回退。"""
        self.assertEqual(self._calc('1.15**5'), Decimal('2.0113571875'))
        self.assertEqual(self._calc('(1+0.03)**10').quantize(Decimal('1e-10')),
                         Decimal('1.3439163793'))

    def test_exact_calc_rejects_fractional_power(self):
        self.assertIsNone(self._calc('2**0.5'))

    def test_exact_calc_division_by_zero_friendly_message(self):
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            result = F.exact_calc('1/0')
        self.assertIsNone(result)
        self.assertIn('除数为零', buf.getvalue())

    def test_cross_validate_flags_outlier(self):
        with contextlib.redirect_stdout(io.StringIO()):
            result = F.cross_validate(
                "营收", {"年报": 100, "来源二": 101, "错误来源": 120}, tolerance_pct=2
            )
        self.assertFalse(result["all_consistent"])
        self.assertEqual(result["consensus"], 101.0)

    def test_market_cap_thresholds(self):
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertTrue(F.verify_market_cap(10, 100, 1005))
            self.assertFalse(F.verify_market_cap(10, 100, 1060))


if __name__ == '__main__':
    unittest.main(verbosity=2)
