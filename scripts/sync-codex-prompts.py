#!/usr/bin/env python3
"""Generate Codex custom prompts from AI Berkshire skills.

Codex custom prompts are deprecated in favor of skills, but they provide the
slash-command style entry point that Claude Code users expect.
"""

from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CLAUDE_SKILLS = ROOT / "skills"
CODEX_PROMPTS = ROOT / "codex-prompts"


def split_frontmatter(text: str):
    if not text.startswith("---\n"):
        return None, text
    end = text.find("\n---\n", 4)
    if end == -1:
        return None, text
    return text[4:end], text[end + 5 :].lstrip("\n")


def first_heading(text: str, fallback: str) -> str:
    for line in text.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return fallback


def yaml_quote(value: str) -> str:
    value = value.replace("\\", "\\\\").replace('"', '\\"')
    return f'"{value}"'


def prompt_for(source: Path) -> str:
    name = source.stem
    source_text = source.read_text(encoding="utf-8")
    _, body = split_frontmatter(source_text)
    title = first_heading(body, name)
    description = f"AI Berkshire slash entry for {title}."
    return (
        "---\n"
        f"description: {yaml_quote(description)}\n"
        "argument-hint: $ARGUMENTS\n"
        "---\n\n"
        f"Use the installed AI Berkshire Codex skill `{name}` for this request.\n\n"
        f"First find `{name}` in the current session's available-skills list "
        "and read its SKILL.md at the actual path provided there.\n\n"
        "If no readable installed skill is available, locate the actual "
        "AI Berkshire project root containing `AGENTS.md`, `skills/`, and "
        "`tools/`, then read and follow "
        f"`codex-skills/{name}/SKILL.md` under that root. "
        "Do not assume a fixed home-directory checkout or treat the "
        "installed skill directory as the project root.\n\n"
        "If neither location provides a readable skill file, report the "
        "missing or inaccessible skill instead of guessing a path.\n\n"
        "User arguments:\n"
        "$ARGUMENTS\n"
    )


def main() -> None:
    check = "--check" in sys.argv[1:]
    unknown_args = [arg for arg in sys.argv[1:] if arg != "--check"]
    if unknown_args:
        joined = ", ".join(unknown_args)
        raise SystemExit(f"Unknown argument(s): {joined}")

    if not check:
        CODEX_PROMPTS.mkdir(exist_ok=True)

    count = 0
    stale: list[str] = []
    for source in sorted(CLAUDE_SKILLS.glob("*.md")):
        target = CODEX_PROMPTS / source.name
        content = prompt_for(source)
        if check:
            if not target.exists() or target.read_text(encoding="utf-8") != content:
                stale.append(str(target.relative_to(ROOT)))
        else:
            target.write_text(content, encoding="utf-8")
        count += 1

    if check:
        if stale:
            print("Codex prompts are out of date:")
            for path in stale:
                print(f"  {path}")
            raise SystemExit(1)
        print(f"Checked {count} Codex prompts in {CODEX_PROMPTS.relative_to(ROOT)}")
        return

    print(f"Generated {count} Codex prompts in {CODEX_PROMPTS.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
