#!/usr/bin/env python3
"""report_audit.py 回归测试.

覆盖两个已修复的缺陷：

  BUG-1  数字提取丢失负号
         7 处正则用 `([\\d,，\\.]+)` 捕获数字，无符号位。报告中的 "-1.72%"
         被提取为 1.72，核验时与信源的 -1.72 相比得出 200% 偏差，
         产出**假打回**。这是最危险的一类 bug：它不报错，只是悄悄
         把结论弄反。

  BUG-2  Windows 控制台 GBK 编码崩溃
         main() 中 print(json.dumps(...)) 遇到 €/→/★ 等字符抛
         UnicodeEncodeError 直接退出。

Zero external dependencies — 仅用 unittest，与 report_audit.py 本身保持一致。
运行：  python tests/test_report_audit.py
"""

import io
import os
import subprocess
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'tools'))

import report_audit as R  # noqa: E402

_TOOLS = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'tools')


class TestCleanNumSign(unittest.TestCase):
    """BUG-1 的最小单元：_clean_num 必须识别各类正负号。"""

    def test_ascii_minus(self):
        self.assertEqual(R._clean_num('-1.72'), -1.72)

    def test_plain_positive(self):
        self.assertEqual(R._clean_num('1.72'), 1.72)

    def test_ascii_plus_is_stripped(self):
        self.assertEqual(R._clean_num('+3.5'), 3.5)

    def test_unicode_minus_u2212(self):
        """报告里常出现 U+2212 真减号，而非 ASCII 连字符。"""
        self.assertEqual(R._clean_num('−4.2'), -4.2)

    def test_en_dash_u2013(self):
        """Markdown 编辑器会把 - 自动转成 en-dash。"""
        self.assertEqual(R._clean_num('–5.1'), -5.1)

    def test_fullwidth_minus_uff0d(self):
        """中文输入法下的全角减号。"""
        self.assertEqual(R._clean_num('－6.3'), -6.3)

    def test_negative_with_thousands_separator(self):
        self.assertEqual(R._clean_num('-1,234.5'), -1234.5)

    def test_negative_with_fullwidth_comma(self):
        self.assertEqual(R._clean_num('-1，234.5'), -1234.5)

    def test_garbage_returns_none(self):
        self.assertIsNone(R._clean_num('n/a'))


class TestNegativeExtractionFromTable(unittest.TestCase):
    """BUG-1 的端到端复现：报告表格中的负数必须被完整提取。

    表格结构复刻自触发假打回的行情表：跌幅列写作 "-1.72%"，
    修复前会被提取成 1.72，与信源比对得出 200% 偏差。
    数据为虚构，仅用于固定格式。
    """

    MD = (
        "| 公司 | 代码 | 股价 | 当日 | PB |\n"
        "|---|---|---|---|---|\n"
        "| 示例公司甲 | 000001 | 27.40 | -1.72% | 1.03 |\n"
        "| 示例公司乙 | 000002 | 17.56 | -1.90% | 2.18 |\n"
        "| 示例公司丙 | 000003 | 12.78 | +1.11% | 1.79 |\n"
        "| 毛利率 | — | — | -3.10% | — |\n"
    )

    def setUp(self):
        self.values = {p['reported_value'] for p in R.extract_data_points(self.MD)}

    def test_extracts_negative_percentages(self):
        for expected in (-1.72, -1.9, -3.1):
            with self.subTest(value=expected):
                self.assertIn(
                    expected, self.values,
                    f"{expected} 未被提取 —— 负号很可能又被正则吃掉了")

    def test_does_not_flip_sign(self):
        """回归核心：绝不能把 -1.72 提成 +1.72。"""
        self.assertNotIn(1.72, self.values, "负号丢失：-1.72 被提取成了 1.72")
        self.assertNotIn(1.9, self.values, "负号丢失：-1.90 被提取成了 1.90")

    def test_plus_sign_normalised_to_positive(self):
        self.assertIn(1.11, self.values)

    def test_negative_count(self):
        self.assertEqual(
            len([v for v in self.values if v < 0]), 3,
            "应恰好提取到 3 个负值（-1.72 / -1.90 / -3.10）")


class TestAbsoluteValueGuard(unittest.TestCase):
    """`val > 1e15` 的上限判断对负数永远为假，须用 abs()。"""

    def test_huge_negative_is_filtered(self):
        md = (
            "| 项目 | 数值 |\n"
            "|---|---|\n"
            "| 异常值 | -9999999999999999 |\n"
            "| 正常值 | -12.5 |\n"
        )
        values = {p['reported_value'] for p in R.extract_data_points(md)}
        self.assertIn(-12.5, values)
        self.assertTrue(
            all(abs(v) < 1e15 for v in values),
            "超过 1e15 的负值未被过滤（abs() 守卫失效）")


class TestGbkStdoutSurvival(unittest.TestCase):
    """BUG-2：Windows GBK 控制台下含 € 的报告必须能正常 extract 而不崩溃。"""

    MD = (
        "# 测试报告\n\n"
        "| 公司 | FY25营收 | 毛利率 |\n"
        "|---|---|---|\n"
        "| Example Corp | €11,297M | 26.1% |\n"
        "| 示例公司甲 | ¥23.6亿 | -3.10% |\n\n"
        "评级：★★☆☆☆ → 观察\n"
    )

    def test_extract_under_gbk_console(self):
        import tempfile
        with tempfile.NamedTemporaryFile('w', suffix='.md', delete=False,
                                         encoding='utf-8') as fh:
            fh.write(self.MD)
            path = fh.name
        try:
            env = dict(os.environ)
            # 模拟 Windows GBK 控制台；显式清掉 UTF-8 逃生阀
            env['PYTHONIOENCODING'] = 'gbk'
            env.pop('PYTHONUTF8', None)
            proc = subprocess.run(
                [sys.executable, os.path.join(_TOOLS, 'report_audit.py'),
                 'extract', '--report', path, '--seed', '1'],
                capture_output=True, env=env)
            self.assertEqual(
                proc.returncode, 0,
                "GBK 控制台下 extract 崩溃了：\n"
                + proc.stderr.decode('utf-8', 'replace')[-800:])
            self.assertNotIn(b'UnicodeEncodeError', proc.stderr)
        finally:
            os.unlink(path)

    def test_force_utf8_stdio_is_idempotent(self):
        """重复调用不应抛异常（stdout 可能已被重定向为非 TextIOWrapper）。"""
        R._force_utf8_stdio()
        R._force_utf8_stdio()

    def test_force_utf8_stdio_tolerates_non_reconfigurable_stream(self):
        orig = sys.stdout
        try:
            sys.stdout = io.BytesIO()  # 没有 reconfigure 方法
            R._force_utf8_stdio()      # 不应抛异常
        finally:
            sys.stdout = orig


if __name__ == '__main__':
    unittest.main(verbosity=2)
