"""Regression coverage for signed and zero-median source comparisons."""

import io
import json
import os
import subprocess
import sys
import unittest
from contextlib import redirect_stdout

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'tools'))

import financial_rigor as F


class TestCrossValidate(unittest.TestCase):
    def compare(self, values, tolerance=2.0):
        with redirect_stdout(io.StringIO()):
            return F.cross_validate('net_income', values, tolerance_pct=tolerance)

    def test_disagreeing_losses_are_inconsistent(self):
        result = self.compare({'annual_report': -100, 'provider': -200})
        self.assertEqual(result['consensus'], -150)
        self.assertFalse(result['all_consistent'])

    def test_equal_losses_are_consistent(self):
        result = self.compare({'annual_report': -100, 'provider': -100})
        self.assertEqual(result['consensus'], -100)
        self.assertTrue(result['all_consistent'])

    def test_negative_median_respects_tolerance(self):
        values = {'annual_report': -100, 'provider': -102}
        self.assertTrue(self.compare(values)['all_consistent'])
        self.assertFalse(self.compare(values, tolerance=0.5)['all_consistent'])

    def test_positive_median_behavior_is_preserved(self):
        self.assertTrue(self.compare({'a': 100, 'b': 102})['all_consistent'])
        self.assertFalse(self.compare({'a': 100, 'b': 200})['all_consistent'])

    def test_all_zero_sources_are_consistent(self):
        result = self.compare({'a': 0, 'b': 0, 'c': 0})
        self.assertEqual(result['consensus'], 0)
        self.assertTrue(result['all_consistent'])

    def test_zero_median_does_not_hide_nonzero_values(self):
        for values in ({'a': -100, 'b': 100},
                       {'a': 0, 'b': 0, 'c': 100},
                       {'a': -100, 'b': 0, 'c': 0}):
            with self.subTest(values=values):
                result = self.compare(values)
                self.assertEqual(result['consensus'], 0)
                self.assertFalse(result['all_consistent'])

    def test_cli_warns_for_disagreeing_losses_and_zero_median(self):
        for values in ({'annual_report': -100, 'provider': -200},
                       {'annual_report': -100, 'provider': 100}):
            with self.subTest(values=values):
                proc = subprocess.run(
                    [sys.executable, F.__file__, 'cross-validate',
                     '--field', 'net_income', '--values', json.dumps(values)],
                    capture_output=True)
                self.assertEqual(proc.returncode, 0, proc.stderr)
                output = proc.stdout.decode('utf-8')
                self.assertIn('❌', output)
                self.assertIn('请核实差异原因', output)
                self.assertNotIn('数据一致', output)


if __name__ == '__main__':
    unittest.main()
