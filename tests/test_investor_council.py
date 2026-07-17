from __future__ import annotations

import copy
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from tools import investor_council  # noqa: E402


class InvestorCouncilLibraryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.library = investor_council.load_library()

    def test_default_library_is_valid_and_source_grounded(self) -> None:
        self.assertEqual([], investor_council.validate_library(self.library))
        self.assertEqual(11, len(self.library["investors"]))
        for investor in self.library["investors"]:
            self.assertTrue(investor["sources"])
            self.assertTrue(
                all(source["url"].startswith("https://") for source in investor["sources"])
            )

    def test_company_scenario_has_stable_default_council(self) -> None:
        selection = investor_council.select_lenses(self.library, scenario_id="company")
        self.assertEqual("scenario-default", selection["selection_mode"])
        self.assertEqual(
            [
                "warren-buffett",
                "charlie-munger",
                "philip-fisher",
                "howard-marks",
            ],
            [lens["id"] for lens in selection["selected_lenses"]],
        )

    def test_custom_portfolio_focus_selects_portfolio_lenses(self) -> None:
        selection = investor_council.select_lenses(
            self.library,
            scenario_id="portfolio",
            focus_tags=("costs", "regime"),
        )
        selected = [lens["id"] for lens in selection["selected_lenses"]]
        self.assertIn("john-bogle", selected)
        self.assertIn("ray-dalio", selected)
        self.assertEqual("focus-ranked", selection["selection_mode"])
        self.assertEqual([], selection["uncovered_focus_tags"])

    def test_custom_focus_is_covered_before_scenario_defaults(self) -> None:
        selection = investor_council.select_lenses(
            self.library,
            scenario_id="company",
            focus_tags=("passive",),
        )
        selected = [lens["id"] for lens in selection["selected_lenses"]]
        self.assertIn("john-bogle", selected)
        self.assertEqual([], selection["uncovered_focus_tags"])

    def test_uncovered_focus_is_reported_when_limit_is_too_small(self) -> None:
        selection = investor_council.select_lenses(
            self.library,
            scenario_id="company",
            focus_tags=("passive", "credit"),
            limit=1,
        )
        self.assertEqual(1, len(selection["selected_lenses"]))
        self.assertEqual(1, len(selection["uncovered_focus_tags"]))

    def test_explicit_lenses_preserve_user_order(self) -> None:
        selection = investor_council.select_lenses(
            self.library,
            explicit_ids=("howard-marks", "benjamin-graham"),
        )
        self.assertEqual(
            ["howard-marks", "benjamin-graham"],
            [lens["id"] for lens in selection["selected_lenses"]],
        )
        self.assertEqual("explicit", selection["selection_mode"])

    def test_unknown_focus_is_rejected(self) -> None:
        with self.assertRaises(investor_council.LibraryError):
            investor_council.select_lenses(
                self.library, focus_tags=("crystal_ball",)
            )

    def test_registry_validation_rejects_non_https_sources(self) -> None:
        broken = copy.deepcopy(self.library)
        broken["investors"][0]["sources"][0]["url"] = "http://example.com/source"
        errors = investor_council.validate_library(broken)
        self.assertTrue(any("HTTPS URL" in error for error in errors))

    def test_markdown_calls_profiles_lenses_not_endorsements(self) -> None:
        selection = investor_council.select_lenses(self.library, scenario_id="deep-value")
        rendered = investor_council.render_selection_markdown(selection)
        self.assertIn("不代表投资家本人", rendered)
        self.assertIn("benjamin-graham", rendered)
        self.assertIn("核心原则", rendered)
        self.assertIn("适用场景", rendered)
        self.assertIn("资料来源", rendered)

    def test_cli_validate_and_invalid_lens_exit_codes(self) -> None:
        tool = ROOT / "tools" / "investor_council.py"
        valid = subprocess.run(
            [sys.executable, str(tool), "validate"],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(0, valid.returncode, valid.stderr)

        invalid = subprocess.run(
            [
                sys.executable,
                str(tool),
                "select",
                "--lenses",
                "unknown-investor",
                "--format",
                "ids",
            ],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(2, invalid.returncode)

        uncovered = subprocess.run(
            [
                sys.executable,
                str(tool),
                "select",
                "--scenario",
                "company",
                "--focus",
                "passive,credit",
                "--limit",
                "1",
                "--format",
                "ids",
            ],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(0, uncovered.returncode, uncovered.stderr)
        self.assertIn("未覆盖", uncovered.stderr)


class InvestorCouncilSkillContractTests(unittest.TestCase):
    def test_skill_contains_safety_and_output_contracts(self) -> None:
        text = (ROOT / "skills" / "investor-council.md").read_text(encoding="utf-8")
        required_phrases = (
            "不得以投资家第一人称写作",
            "N/A",
            "unknown",
            "禁止把不同哲学",
            "两个独立来源",
            "交叉质询",
            "低成本指数基准",
            "不构成投资建议",
        )
        for phrase in required_phrases:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, text)


if __name__ == "__main__":
    unittest.main()
