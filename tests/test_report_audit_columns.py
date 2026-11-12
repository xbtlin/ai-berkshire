"""Regression coverage for audit labels after empty Markdown table cells."""

import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'tools'))

from report_audit import extract_data_points


class TestTableColumnAlignment(unittest.TestCase):
    def extract(self, header, row):
        md = header + '\n|---|---|---|\n' + row + '\n'
        return [(p['label'], p['reported_value'])
                for p in extract_data_points(md)]

    def test_empty_middle_cell_preserves_year(self):
        for blank in ('', ' ', '** **'):
            with self.subTest(blank=blank):
                self.assertEqual(
                    self.extract('| Metric | 2024 | 2025 |',
                                 '| Revenue |' + blank + '| 200 |'),
                    [('Revenue · 2025', 200.0)])

    def test_empty_header_preserves_following_years(self):
        self.assertEqual(
            self.extract('| | 2024 | 2025 |', '| Revenue | 100 | 200 |'),
            [('Revenue · 2024', 100.0), ('Revenue · 2025', 200.0)])

    def test_empty_cell_does_not_move_value_into_skipped_column(self):
        self.assertEqual(
            self.extract('| Company | YoY | Revenue |',
                         '| Example Corp | | 200 |'),
            [('Example Corp · Revenue', 200.0)])

    def test_empty_cell_does_not_move_skipped_value_into_audit(self):
        self.assertEqual(
            self.extract('| Company | Revenue | YoY |',
                         '| Example Corp | | -12% |'), [])

    def test_empty_row_label_does_not_become_a_numeric_label(self):
        self.assertEqual(
            self.extract('| Metric | 2024 | 2025 |', '| | 100 | 200 |'), [])

    def test_populated_rows_with_optional_header_pipes(self):
        for header in ('| Metric | 2024 | 2025 |', 'Metric | 2024 | 2025'):
            with self.subTest(header=header):
                self.assertEqual(
                    self.extract(header, '| Revenue | 100 | -200 |'),
                    [('Revenue · 2024', 100.0), ('Revenue · 2025', -200.0)])


if __name__ == '__main__':
    unittest.main()
