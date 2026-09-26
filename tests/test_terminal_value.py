#!/usr/bin/env python3
"""terminal_value.py 回归测试（含 issue #96 flip 压力测试）.

覆盖：
  - stress_pass / flip_analysis：r±Δ 下结论翻转与稳定；币种区间外档位不参与判定
  - flip CLI：--currency 必填、区间外标注、内联参数 / --config 支持新公司
  - 既有 pe / evaluate 不被破坏

运行：  python3 tests/test_terminal_value.py
"""

import json
import os
import subprocess
import sys
import tempfile
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
        """Issue #96 / PR #108 review：HKD 区间 [9%, 11.5%]。
        r=10%±2pp 时 8%/12% 两档在区间外，只作参考、不参与翻转判定；
        8% 档虽"通过"，但不得据此报告翻转（否则就是调低 r 去买）。"""
        spec = TV.PRESET['腾讯']
        result = TV.flip_analysis(
            spec, r=0.10, delta=0.02, g_shift=-0.01, rf=TV.RF['USD'],
            band=TV.CURRENCY_BANDS['HKD'])
        self.assertEqual(len(result['rates']), 3)
        for got, want in zip(result['rates'], (0.08, 0.10, 0.12)):
            self.assertAlmostEqual(got, want)
        self.assertEqual(result['in_band'], (False, True, False))
        self.assertTrue(result['passes'][0], 'r-2pp=8% 数值上通过，但在区间外')
        self.assertFalse(result['passes'][1], '基准 r=10% 应未通过')
        self.assertFalse(result['flipped'], '区间外档位不得触发翻转')

    def test_tencent_hkd_pm_1pp_in_band_stable(self):
        """维护者复现：±1pp 三档都在区间内，期望 IRR 7.66%/6.30%/5.11%，全部未通过 → 稳定。"""
        result = TV.flip_analysis(
            TV.PRESET['腾讯'], r=0.10, delta=0.01, g_shift=-0.01, rf=TV.RF['USD'],
            band=TV.CURRENCY_BANDS['HKD'])
        self.assertEqual(result['in_band'], (True, True, True))
        for got, want in zip(result['means'], (7.66, 6.30, 5.11)):
            self.assertAlmostEqual(got, want, places=2)
        self.assertTrue(all(p is False for p in result['passes']))
        self.assertFalse(result['flipped'])

    def test_flip_inside_band_is_reported(self):
        """CNY 区间 [6%, 9%] 内 r=7.5%±1pp：6.5%/7.5% 通过、8.5% 未通过 → 区间内翻转。"""
        result = TV.flip_analysis(
            TV.PRESET['腾讯'], r=0.075, delta=0.01, g_shift=-0.01,
            band=TV.CURRENCY_BANDS['CNY'])
        self.assertEqual(result['in_band'], (True, True, True))
        self.assertEqual(result['passes'], [True, True, False])
        self.assertTrue(result['flipped'])

    def test_no_band_keeps_all_tiers(self):
        """band=None（库函数直接调用）时不做区间过滤，保持原判定。"""
        result = TV.flip_analysis(
            TV.PRESET['腾讯'], r=0.10, delta=0.02, g_shift=-0.01, rf=TV.RF['USD'])
        self.assertEqual(result['in_band'], (None, None, None))
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


_TENCENT_INLINE = ['--roic', '0.20', '--g', '0.015,0.030,0.040', '--p', '0.35,0.50,0.15',
                   '--irr10', '0.3,9.3,15.4', '--k', '0.02']


class TestFlipCLI(unittest.TestCase):

    def test_flip_cli_out_of_band_tiers_excluded(self):
        """维护者 review 场景：HKD r=10%±2pp，8% 档标区间外且不触发翻转。"""
        proc = _run([
            'flip', '--name', '腾讯', '--r', '0.10', '--delta', '0.02',
            '--currency', 'HKD', '--g-shift', '-0.01', '--rf', '0.047',
        ])
        self.assertEqual(proc.returncode, 0, proc.stderr[-800:])
        out = proc.stdout
        self.assertIn('【稳定】', out)
        self.assertNotIn('【翻转】', out)
        self.assertEqual(out.count('区间外，仅供参考'), 2)
        self.assertIn('仓位压力测试', out)
        self.assertIn('不是买入/持有/回避的唯一否决票', out)
        self.assertIn('禁止为迎合买入结论', out)

    def test_flip_cli_reports_flip_inside_band(self):
        proc = _run([
            'flip', '--name', '腾讯', '--r', '0.075', '--delta', '0.01',
            '--currency', 'CNY', '--g-shift', '-0.01',
        ])
        self.assertEqual(proc.returncode, 0, proc.stderr[-800:])
        self.assertIn('【翻转】', proc.stdout)
        self.assertNotIn('区间外', proc.stdout.split('判定规则')[1])
        self.assertIn('通过', proc.stdout)
        self.assertIn('未通过', proc.stdout)

    def test_flip_cli_requires_currency(self):
        proc = _run(['flip', '--name', '腾讯', '--r', '0.10'])
        self.assertEqual(proc.returncode, 2)
        self.assertIn('--currency', proc.stderr)

    def test_flip_cli_base_r_out_of_band_rejected(self):
        proc = _run(['flip', '--name', '腾讯', '--r', '0.08', '--currency', 'HKD'])
        self.assertEqual(proc.returncode, 1)
        self.assertIn('【打回】', proc.stdout)

    def test_flip_cli_unknown_company(self):
        proc = _run(['flip', '--name', '不存在的公司', '--r', '0.10', '--currency', 'USD'])
        self.assertEqual(proc.returncode, 1)
        self.assertIn('未知公司', proc.stderr)
        self.assertIn('内联参数', proc.stderr)

    def test_flip_cli_inline_params_match_preset(self):
        """新公司：内联参数与同值预设输出完全一致。"""
        common = ['--r', '0.10', '--delta', '0.01', '--currency', 'HKD', '--g-shift', '-0.01']
        inline = _run(['flip', '--name', '腾讯'] + _TENCENT_INLINE + common)
        preset = _run(['flip', '--name', '腾讯'] + common)
        self.assertEqual(inline.returncode, 0, inline.stderr[-800:])
        self.assertEqual(inline.stdout, preset.stdout)

    def test_flip_cli_inline_negative_irr10(self):
        """悲观档 IRR 为负是常态：--irr10=-2,8,14 写法可用（docstring 示例）。"""
        proc = _run(['flip', '--name', '某公司', '--roic', '0.18', '--g', '0.015,0.03,0.04',
                     '--p', '0.35,0.50,0.15', '--irr10=-2.0,8.0,14.0', '--k', '0.01',
                     '--r', '0.10', '--currency', 'USD'])
        self.assertEqual(proc.returncode, 0, proc.stderr[-800:])
        self.assertIn('某公司', proc.stdout)
        self.assertIn('基准 r', proc.stdout)

    def test_flip_cli_inline_params_incomplete(self):
        proc = _run(['flip', '--name', '新公司', '--roic', '0.2', '--r', '0.10',
                     '--currency', 'USD'])
        self.assertEqual(proc.returncode, 1)
        self.assertIn('--g', proc.stderr)

    def test_flip_cli_inline_probs_must_sum_to_one(self):
        args = list(_TENCENT_INLINE)
        args[args.index('--p') + 1] = '0.3,0.5,0.3'
        proc = _run(['flip', '--name', '新公司'] + args + ['--r', '0.10', '--currency', 'USD'])
        self.assertEqual(proc.returncode, 1)
        self.assertIn('概率之和', proc.stderr)

    def test_flip_cli_config_file(self):
        """新公司：按 skill 中写明的 JSON 格式传 --config。"""
        cfg = {'新公司': {'roic': 0.20, 'g': [0.015, 0.030, 0.040],
                          'p': [0.35, 0.50, 0.15], 'irr10': [0.3, 9.3, 15.4], 'k': 0.02}}
        with tempfile.NamedTemporaryFile('w', suffix='.json', delete=False,
                                         encoding='utf-8') as fh:
            json.dump(cfg, fh, ensure_ascii=False)
            path = fh.name
        try:
            proc = _run(['flip', '--name', '新公司', '--config', path, '--r', '0.10',
                         '--delta', '0.01', '--currency', 'HKD', '--g-shift', '-0.01'])
        finally:
            os.unlink(path)
        self.assertEqual(proc.returncode, 0, proc.stderr[-800:])
        self.assertIn('+6.30%', proc.stdout)
        self.assertIn('【稳定】', proc.stdout)


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
