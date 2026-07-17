from __future__ import annotations

import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class GeneratedArtifactTests(unittest.TestCase):
    def test_generated_codex_artifacts_are_current(self) -> None:
        for script in (
            ROOT / "scripts" / "sync-codex-skills.py",
            ROOT / "scripts" / "sync-codex-prompts.py",
        ):
            with self.subTest(script=script.name):
                completed = subprocess.run(
                    [sys.executable, str(script), "--check"],
                    cwd=ROOT,
                    text=True,
                    capture_output=True,
                    check=False,
                )
                self.assertEqual(
                    0,
                    completed.returncode,
                    completed.stdout + completed.stderr,
                )

    def test_all_canonical_skills_have_both_generated_entries(self) -> None:
        canonical = {path.stem for path in (ROOT / "skills").glob("*.md")}
        generated_skills = {
            path.parent.name
            for path in (ROOT / "codex-skills").glob("*/SKILL.md")
            if path.parent.name != "investment-memo-craft"
        }
        generated_prompts = {
            path.stem for path in (ROOT / "codex-prompts").glob("*.md")
        }
        self.assertEqual(canonical, generated_skills)
        self.assertEqual(canonical, generated_prompts)
        self.assertEqual(20, len(canonical))

    def test_readmes_advertise_the_canonical_skill_count(self) -> None:
        expectations = {
            "README.md": "Skills 一览（20个）",
            "README_EN.md": "Skills Overview (20 Skills)",
            "README_JA.md": "Skill一覧（20スキル）",
        }
        for filename, phrase in expectations.items():
            with self.subTest(filename=filename):
                text = (ROOT / filename).read_text(encoding="utf-8")
                self.assertIn(phrase, text)
                self.assertIn("skills/investor-council.md", text)

    def test_investor_council_prompt_points_to_generated_skill(self) -> None:
        prompt = (ROOT / "codex-prompts" / "investor-council.md").read_text(
            encoding="utf-8"
        )
        skill = (
            ROOT / "codex-skills" / "investor-council" / "SKILL.md"
        ).read_text(encoding="utf-8")
        self.assertIn("`investor-council`", prompt)
        self.assertIn("generated from `skills/investor-council.md`", skill)
        self.assertIn("不得以投资家第一人称写作", skill)


if __name__ == "__main__":
    unittest.main()
