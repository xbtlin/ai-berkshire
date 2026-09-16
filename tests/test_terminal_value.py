#!/usr/bin/env python3
"""terminal_value.py 回归测试（含 issue #96 flip 压力测试）.

覆盖：
  - stress_pass / flip_analysis：r±2pp 下结论翻转与稳定
  - flip CLI：清晰输出【翻转】/【稳定】，退出码 0
  - 既有 pe / evaluate 不被破坏

运行：  python3 tests/test_terminal_value.py
"""

import os
import subprocess
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'tools'))

import terminal_value as TV  # noqa: E402

_TOOLS = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'tools')
_TV = os.path.join(_TOOLS, 'terminal_value.py')


def _run(args):
    return subprocess.run(
        [sys.executable, _TV] + args,
        capture_output=True, text=True, encoding='utf-8')


class TestStressPass(unittest.TestCase):

    def test_covers_cost_of_capital(self):
        self.assertTrue(TV.stress_pass(10.0, 0.10))
        self.assertTrue(TV.stress_pass(10.5, 0.10))
        self.assertFalse(TV.stress_pass(9.9, 0.10))
        self.assertIsNone(TV.stress_pass(None, 0.10))


class TestFlipAnalysis(unittest.TestCase):

    def test_tencent_hkd_style_flips_at_pm_2pp(self):
        """Issue #96 复现：HKD 主用 r=10% 时腾讯期望 IRR 未覆盖 r，
        但 r-2pp=8% 时覆盖 → 必须报告翻转。"""
        spec = TV.PRESET['腾讯']
        result = TV.flip_analysis(
            spec, r=0.10, delta=0.02, g_shift=-0.01, rf=TV.RF['USD'])
        self.assertEqual(len(result['rates']), 3)
        for got, want in zip(result['rates'], (0.08, 0.10, 0.12)):
            self.assertAlmostEqual(got, want)
        self.assertTrue(result['passes'][0], 'r-2pp 应通过压力测试')
        self.assertFalse(result['passes'][1], '基准 r=10% 应未通过')
        self.assertTrue(result['flipped'])

    def test_stable_when_always_fail(self):
        """高 r + 低 ROIC 预设下，±2pp 内始终未通过 → 不翻转。"""
        # MiniMax 在较高 r 下期望 IRR 深度为负，±2pp 仍未通过
        spec = TV.PRESET['MiniMax']
        result = TV.flip_analysis(
            spec, r=0.10, delta=0.02, g_shift=-0.01, rf=TV.RF['CNY'])
        self.assertFalse(result['flipped'])
        self.assertTrue(all(p is False for p in result['passes']))

    def test_delta_must_be_positive(self):
        with self.assertRaises(ValueError):
            TV.flip_analysis(TV.PRESET['腾讯'], r=0.10, delta=0.0)


class TestFlipCLI(unittest.TestCase):

    def test_flip_cli_reports_flip_for_tencent(self):
        proc = _run([
            'flip', '--name', '腾讯', '--r', '0.10', '--delta', '0.02',
            '--g-shift', '-0.01', '--rf', '0.047',
        ])
        self.assertEqual(proc.returncode, 0, proc.stderr[-800:])
        out = proc.stdout
        self.assertIn('【翻转】', out)
        self.assertIn('仓位压力测试', out)
        self.assertIn('不是买入/持有/回避的唯一否决票', out)
        self.assertIn('禁止为迎合买入结论', out)
        self.assertIn('通过', out)
        self.assertIn('未通过', out)

    def test_flip_cli_unknown_company(self):
        proc = _run(['flip', '--name', '不存在的公司', '--r', '0.10'])
        self.assertEqual(proc.returncode, 1)
        self.assertIn('未知公司', proc.stderr)


class TestCoreRegression(unittest.TestCase):

    def test_exit_pe_basic(self):
        pe, retention, numerator, spread = TV.exit_pe(0.20, 0.02, 0.06)
        self.assertIsNotNone(pe)
        self.assertAlmostEqual(spread, 0.04)
        self.assertAlmostEqual(retention, 0.10)
        self.assertAlmostEqual(pe, numerator / spread)

    def test_pe_cli(self):
        proc = _run(['pe', '--roic', '0.20', '--g', '0.02', '--r', '0.06'])
        self.assertEqual(proc.returncode, 0, proc.stderr[-400:])
        self.assertIn('退出 PE', proc.stdout)


if __name__ == '__main__':
    unittest.main()
