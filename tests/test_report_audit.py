"""Regression tests for report data extraction and release verdicts."""

import contextlib
import importlib.util
import io
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "report_audit", ROOT / "tools" / "report_audit.py"
)
report_audit = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(report_audit)


class ReportAuditTests(unittest.TestCase):
    def test_extracts_table_and_key_value_points(self):
        report = """| 指标 | 2025年 |\n| --- | --- |\n| 营收 | 1,234亿元 |\n| 净利率 | 25% |\n\n自由现金流：456亿元\n"""

        points = report_audit.extract_data_points(report)
        labels = {point["label"] for point in points}

        self.assertIn("营收 · 2025年", labels)
        self.assertIn("净利率 · 2025年", labels)
        self.assertIn("自由现金流", labels)

    def test_sampling_is_reproducible_and_bounded(self):
        points = [{"line_number": i} for i in range(1, 101)]

        first = report_audit.sample_points(points, ratio=0.15, seed=42)
        second = report_audit.sample_points(points, ratio=0.15, seed=42)

        self.assertEqual(first, second)
        self.assertEqual(len(first), 15)

    def test_verdict_fails_when_both_sources_disagree(self):
        results = [{
            "id": 1,
            "label": "营收",
            "reported_value": 100,
            "unit": "亿",
            "fetched_value": 103,
            "fetched_source": "年报",
            "fetched_value2": 104,
            "fetched_source2": "数据库",
        }]

        with contextlib.redirect_stdout(io.StringIO()):
            outcome = report_audit.render_verdict(results)

        self.assertEqual(outcome["verdict"], "FAIL")
        self.assertEqual(outcome["fail_count"], 1)
