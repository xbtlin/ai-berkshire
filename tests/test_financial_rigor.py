import io
import subprocess
import sys
import unittest
from contextlib import redirect_stdout
from decimal import Decimal
from pathlib import Path
from unittest import mock

from tools import financial_rigor


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / 'tools' / 'financial_rigor.py'


class ExactCalculatorTests(unittest.TestCase):
    def calculate(self, expression):
        with redirect_stdout(io.StringIO()):
            return financial_rigor.exact_calc(expression)

    def test_decimal_addition_has_no_binary_float_drift(self):
        result = self.calculate('0.1 + 0.2')
        self.assertIsInstance(result, Decimal)
        self.assertEqual(result, Decimal('0.3'))

    def test_scientific_notation_precedence_and_unary_operators(self):
        self.assertEqual(
            self.calculate('-(1.2e3 + 3) / +3'),
            Decimal('-401'),
        )

    def test_calculator_does_not_call_eval(self):
        with mock.patch('builtins.eval', side_effect=AssertionError('eval called')):
            self.assertEqual(self.calculate('2 * (3 + 4)'), Decimal('14'))

    def test_calculator_supports_python37_without_ast_constant(self):
        legacy_num = type('Num', (), {'lineno': 1, 'col_offset': 0})()
        with mock.patch.object(financial_rigor.ast, 'Constant', None):
            self.assertEqual(
                financial_rigor._eval_decimal_ast(legacy_num, '1.2'),
                Decimal('1.2'),
            )

    def test_calculator_rejects_non_four_function_expressions(self):
        self.assertIsNone(self.calculate('2 ** 8'))
        self.assertIsNone(self.calculate('__import__("os")'))


class CrossValidationTests(unittest.TestCase):
    def validate(self, values, tolerance=Decimal('1')):
        with redirect_stdout(io.StringIO()):
            return financial_rigor.cross_validate(
                'revenue', values, tolerance_pct=tolerance
            )

    def test_default_one_percent_pairwise_tolerance_is_inclusive(self):
        at_boundary = self.validate({'filing': '100', 'exchange': '101'})
        formerly_fail_open = self.validate({'filing': '99', 'exchange': '101'})
        just_over = self.validate({'filing': '100', 'exchange': '101.0001'})

        self.assertTrue(at_boundary['all_consistent'])
        self.assertFalse(formerly_fail_open['all_consistent'])
        self.assertFalse(just_over['all_consistent'])

    def test_every_pair_must_be_within_tolerance(self):
        passing = self.validate({
            'filing': '100',
            'exchange': '100.5',
            'data vendor': '101',
        })
        failing = self.validate({
            'filing': '99',
            'exchange': '100',
            'data vendor': '101',
        })

        self.assertTrue(passing['all_consistent'])
        self.assertFalse(failing['all_consistent'])

    def test_pairwise_difference_handles_zero_and_signs(self):
        self.assertTrue(self.validate({'a': '0', 'b': '0'})['all_consistent'])
        self.assertFalse(self.validate({'a': '0', 'b': '0.01'})['all_consistent'])
        self.assertTrue(self.validate({'a': '-100', 'b': '-101'})['all_consistent'])
        self.assertFalse(self.validate({'a': '-100', 'b': '100'})['all_consistent'])

    def test_at_least_two_sources_are_required(self):
        outcome = self.validate({'filing': '100'})
        self.assertFalse(outcome['all_consistent'])
        self.assertIsNone(outcome['consensus'])


class ScenarioValuationTests(unittest.TestCase):
    def test_scenario_calculation_and_rendering_do_not_convert_to_float(self):
        with mock.patch('builtins.float', side_effect=AssertionError('float called')):
            with redirect_stdout(io.StringIO()):
                financial_rigor.three_scenario_valuation(
                    Decimal('100'), Decimal('5'), Decimal('10'),
                    Decimal('0.10'), Decimal('0.05'), Decimal('0'),
                    Decimal('25'), Decimal('20'), Decimal('15'),
                    years=3,
                )


class FinancialRigorCliTests(unittest.TestCase):
    def run_cli(self, *arguments):
        return subprocess.run(
            [sys.executable, str(SCRIPT), *arguments],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )

    def test_cross_validation_failure_has_nonzero_exit_code(self):
        result = self.run_cli(
            'cross-validate',
            '--field', 'revenue',
            '--values', '{"filing": 99, "exchange": 101}',
        )
        self.assertNotEqual(result.returncode, 0)

    def test_cross_validation_requires_two_sources_at_cli(self):
        result = self.run_cli(
            'cross-validate',
            '--field', 'revenue',
            '--values', '{"filing": 100}',
        )
        self.assertNotEqual(result.returncode, 0)

    def test_market_cap_failure_has_nonzero_exit_code(self):
        result = self.run_cli(
            'verify-market-cap',
            '--price', '10',
            '--shares', '100',
            '--reported', '1',
        )
        self.assertNotEqual(result.returncode, 0)

    def test_zero_price_and_negative_years_fail_without_traceback(self):
        valuation = self.run_cli(
            'verify-valuation',
            '--price', '0',
            '--eps', '1',
        )
        zero_price_scenario = self.run_cli(
            'three-scenario',
            '--price', '0',
            '--eps', '1',
            '--shares', '10',
            '--growth', '0.1', '0.05', '0',
            '--pe', '25', '20', '15',
        )
        negative_years = self.run_cli(
            'three-scenario',
            '--price', '100',
            '--eps', '5',
            '--shares', '10',
            '--growth', '0.1', '0.05', '0',
            '--pe', '25', '20', '15',
            '--years', '-1',
        )

        for result in (valuation, zero_price_scenario, negative_years):
            self.assertNotEqual(result.returncode, 0)
            self.assertNotIn('Traceback', result.stdout + result.stderr)

    def test_decimal_overflow_is_a_controlled_cli_failure(self):
        result = self.run_cli(
            'verify-market-cap',
            '--price', '9e999999',
            '--shares', '10',
            '--reported', '1',
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertNotIn('Traceback', result.stdout + result.stderr)

    def test_successful_commands_have_zero_exit_code(self):
        market_cap = self.run_cli(
            'verify-market-cap',
            '--price', '0.1',
            '--shares', '3',
            '--reported', '0.3',
        )
        cross_validation = self.run_cli(
            'cross-validate',
            '--field', 'revenue',
            '--values', '{"filing": 100, "exchange": 100.5}',
        )
        self.assertEqual(market_cap.returncode, 0, market_cap.stdout)
        self.assertEqual(cross_validation.returncode, 0, cross_validation.stdout)


if __name__ == '__main__':
    unittest.main()
