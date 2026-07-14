"""Regression tests for the financial calculation tool."""

import contextlib
import importlib.util
import io
from decimal import Decimal
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "financial_rigor", ROOT / "tools" / "financial_rigor.py"
)
financial_rigor = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(financial_rigor)


class FinancialRigorTests(unittest.TestCase):
    def test_exact_calc_avoids_float_drift(self):
        with contextlib.redirect_stdout(io.StringIO()):
            result = financial_rigor.exact_calc("0.1 + 0.2")

        self.assertEqual(result, Decimal("0.3"))

    def test_exact_calc_supports_scientific_notation_and_parentheses(self):
        with contextlib.redirect_stdout(io.StringIO()):
            result = financial_rigor.exact_calc("(1.25e3 - 250) / 2")

        self.assertEqual(result, Decimal("500"))

    def test_exact_calc_rejects_non_arithmetic_input(self):
        with contextlib.redirect_stdout(io.StringIO()):
            result = financial_rigor.exact_calc("__import__('os').system('echo unsafe')")

        self.assertIsNone(result)

    def test_cross_validate_flags_outlier(self):
        with contextlib.redirect_stdout(io.StringIO()):
            result = financial_rigor.cross_validate(
                "营收", {"年报": 100, "来源二": 101, "错误来源": 120}, tolerance_pct=2
            )

        self.assertFalse(result["all_consistent"])
        self.assertEqual(result["consensus"], 101.0)

    def test_market_cap_thresholds(self):
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertTrue(financial_rigor.verify_market_cap(10, 100, 1005))
            self.assertFalse(financial_rigor.verify_market_cap(10, 100, 1060))
