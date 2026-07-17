import io
import json
import subprocess
import sys
import unittest
from contextlib import redirect_stdout
from pathlib import Path

from tools import report_audit


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / 'tools' / 'report_audit.py'


def audited_item(**overrides):
    item = {
        'id': 1,
        'label': '营业收入',
        'reported_value': 100,
        'unit': '亿',
        'fetched_value': 100,
        'fetched_source': 'annual filing',
        'fetched_value2': 100,
        'fetched_source2': 'stock exchange',
    }
    item.update(overrides)
    return item


class ExtractionTests(unittest.TestCase):
    def test_extracts_negative_and_zero_values_from_tables_and_labels(self):
        markdown = '''\
| 指标 | 2025 |
| --- | ---: |
| 净利润 | -12.5亿 |
| 自由现金流 | 0亿元 |

负债率：−3.2%
资本开支：0亿
'''
        points = report_audit.extract_data_points(markdown)
        values = {(point['label'], point['reported_value']) for point in points}

        self.assertIn(('净利润 · 2025', -12.5), values)
        self.assertIn(('自由现金流 · 2025', 0.0), values)
        self.assertIn(('负债率', -3.2), values)
        self.assertIn(('资本开支', 0.0), values)

    def test_empty_table_cell_does_not_shift_later_column_labels(self):
        markdown = '''\
| 指标 | 2024 | 2025 |
| --- | ---: | ---: |
| 营业收入 | | 100亿 |
'''
        points = report_audit.extract_data_points(markdown)
        values = {(point['label'], point['reported_value']) for point in points}

        self.assertIn(('营业收入 · 2025', 100.0), values)
        self.assertNotIn(('营业收入 · 2024', 100.0), values)


class VerdictTests(unittest.TestCase):
    def verdict(self, results):
        with redirect_stdout(io.StringIO()):
            return report_audit.render_verdict(results)

    def test_empty_results_fail(self):
        self.assertEqual(self.verdict([])['verdict'], 'FAIL')

    def test_unverified_item_fails(self):
        outcome = self.verdict([audited_item(fetched_value=None)])
        self.assertEqual(outcome['verdict'], 'FAIL')
        self.assertIn('主来源核验值缺失', outcome['fail_items'][0]['reason'])

    def test_missing_second_source_fails(self):
        outcome = self.verdict([
            audited_item(fetched_value2=None, fetched_source2='')
        ])
        self.assertEqual(outcome['verdict'], 'FAIL')
        self.assertIn('第二来源', outcome['fail_items'][0]['reason'])

    def test_one_mismatching_source_fails_instead_of_warning(self):
        outcome = self.verdict([audited_item(fetched_value2=102)])
        self.assertEqual(outcome['verdict'], 'FAIL')
        self.assertEqual(outcome['warn_count'], 0)
        self.assertEqual(outcome['fail_count'], 1)

    def test_sources_must_be_independent(self):
        outcome = self.verdict([
            audited_item(
                fetched_source='Annual Filing',
                fetched_source2=' annual  filing ',
            )
        ])
        self.assertEqual(outcome['verdict'], 'FAIL')
        self.assertIn('不独立', outcome['fail_items'][0]['reason'])

    def test_source_placeholders_are_unverified(self):
        outcome = self.verdict([
            audited_item(
                fetched_source='unknown',
                fetched_source2='TBD',
            )
        ])
        self.assertEqual(outcome['verdict'], 'FAIL')
        self.assertIn('主来源名称缺失', outcome['fail_items'][0]['reason'])
        self.assertIn('第二来源名称缺失', outcome['fail_items'][0]['reason'])

    def test_two_independent_sources_within_one_percent_pass(self):
        outcome = self.verdict([
            audited_item(fetched_value=99, fetched_value2=101)
        ])
        self.assertEqual(outcome['verdict'], 'PASS')
        self.assertEqual(outcome['pass_count'], 1)

    def test_zero_and_negative_reported_values_can_pass(self):
        results = [
            audited_item(
                id=1,
                reported_value=0,
                fetched_value=0,
                fetched_value2=0,
            ),
            audited_item(
                id=2,
                reported_value=-100,
                fetched_value=-99,
                fetched_value2=-101,
            ),
        ]
        self.assertEqual(self.verdict(results)['verdict'], 'PASS')


class ReportAuditCliTests(unittest.TestCase):
    def run_verdict(self, results, output_json=False):
        arguments = [
            sys.executable,
            str(SCRIPT),
            'verdict',
            '--results',
            json.dumps(results),
        ]
        if output_json:
            arguments.append('--output-json')
        return subprocess.run(
            arguments,
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )

    def test_empty_results_have_nonzero_exit_code(self):
        self.assertNotEqual(self.run_verdict([]).returncode, 0)

    def test_fully_verified_results_have_zero_exit_code(self):
        result = self.run_verdict([audited_item()])
        self.assertEqual(result.returncode, 0, result.stdout)

    def test_failed_decimal_result_is_json_serializable(self):
        result = self.run_verdict(
            [audited_item(
                reported_value=100.1,
                fetched_value=100.1,
                fetched_value2=102.2,
            )],
            output_json=True,
        )
        self.assertEqual(result.returncode, 1, result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(payload['verdict'], 'FAIL')
        self.assertNotIn('\033[', result.stdout)


if __name__ == '__main__':
    unittest.main()
