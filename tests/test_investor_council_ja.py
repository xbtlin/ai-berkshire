from __future__ import annotations

import copy
import unittest

from api.index import _catalog
from tools.investor_council import investor_index, load_library, select_lenses
from tools.investor_council_ja import (
    FOCUS_TAXONOMY_JA,
    INVESTOR_TRANSLATIONS_JA,
    SCENARIO_DESCRIPTIONS_JA,
    LocalizationError,
    localize_catalog,
    localize_profile,
    localize_selection,
)


class JapaneseLocalizationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.library = load_library()
        cls.investors = investor_index(cls.library)

    def test_mapping_coverage_matches_canonical_registry(self) -> None:
        self.assertEqual(set(self.library["focus_taxonomy"]), set(FOCUS_TAXONOMY_JA))
        self.assertEqual(set(self.library["scenarios"]), set(SCENARIO_DESCRIPTIONS_JA))
        self.assertEqual(set(self.investors), set(INVESTOR_TRANSLATIONS_JA))

    def test_localizers_preserve_inputs_and_source_identity(self) -> None:
        catalog = _catalog()
        catalog_before = copy.deepcopy(catalog)
        localized_catalog = localize_catalog(catalog)
        self.assertEqual(catalog_before, catalog)
        self.assertNotEqual(
            catalog["focus_taxonomy"]["business_quality"],
            localized_catalog["focus_taxonomy"]["business_quality"],
        )

        profile = self.investors["howard-marks"]
        profile_before = copy.deepcopy(profile)
        localized_profile = localize_profile(profile)
        self.assertEqual(profile_before, profile)
        self.assertEqual(
            [source["url"] for source in profile["sources"]],
            [source["url"] for source in localized_profile["sources"]],
        )
        self.assertTrue(all(source["kind_ja"] for source in localized_profile["sources"]))

    def test_every_scenario_selection_is_localized_and_unknown_id_fails(self) -> None:
        for scenario_id in self.library["scenarios"]:
            with self.subTest(scenario=scenario_id):
                selection = select_lenses(
                    self.library,
                    scenario_id=scenario_id,
                    focus_tags=[],
                    explicit_ids=[],
                    limit=4,
                )
                selection_before = copy.deepcopy(selection)
                localized = localize_selection(selection)
                self.assertEqual(selection_before, selection)
                self.assertEqual(
                    SCENARIO_DESCRIPTIONS_JA[scenario_id],
                    localized["scenario_description"],
                )
                self.assertTrue(
                    all(lens["name_ja"] for lens in localized["selected_lenses"])
                )

        unknown = copy.deepcopy(self.investors["howard-marks"])
        unknown["id"] = "unknown-investor"
        with self.assertRaises(LocalizationError):
            localize_profile(unknown)


if __name__ == "__main__":
    unittest.main()
