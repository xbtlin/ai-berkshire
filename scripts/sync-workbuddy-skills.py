#!/usr/bin/env python3
"""Generate WorkBuddy skills from AI Berkshire Claude command files.

This is the WorkBuddy counterpart of ``sync-codex-skills.py``. It keeps
``skills/*.md`` as the single canonical source and renders
``workbuddy-skills/<name>/SKILL.md`` packages that WorkBuddy can load from
``~/.workbuddy/skills`` (user level) or ``<workspace>/.workbuddy/skills``
(project level).

Usage:
    python3 scripts/sync-workbuddy-skills.py              # regenerate
    python3 scripts/sync-workbuddy-skills.py --check      # CI drift check
    python3 scripts/sync-workbuddy-skills.py --prefix ab- # namespace names
    python3 scripts/sync-workbuddy-skills.py --prune      # drop stale output
"""

from __future__ import annotations

import os
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CLAUDE_SKILLS = ROOT / "skills"
WORKBUDDY_SKILLS = ROOT / "workbuddy-skills"

ADAPTER_MARKER = "## WorkBuddy adapter note"
DESC_LIMIT = 480
SUMMARY_LIMIT = 160

BLOCK_SCALARS = {">-", ">", ">+", "|-", "|", "|+"}


# --------------------------------------------------------------------------
# frontmatter helpers
# --------------------------------------------------------------------------
def split_frontmatter(text: str) -> tuple[str | None, str]:
    """Return (frontmatter_without_delimiters, body)."""
    if not text.startswith("---\n"):
        return None, text
    end = text.find("\n---\n", 4)
    if end == -1:
        return None, text
    return text[4:end], text[end + 5 :].lstrip("\n")


def yaml_field(frontmatter: str, key: str) -> str | None:
    """Read a scalar / block-scalar value out of a simple YAML frontmatter."""
    lines = frontmatter.splitlines()
    pattern = re.compile(r"^" + re.escape(key) + r":\s*(.*)$")
    for index, line in enumerate(lines):
        match = pattern.match(line)
        if not match:
            continue
        raw = match.group(1).strip()
        if raw in BLOCK_SCALARS:
            block: list[str] = []
            for nxt in lines[index + 1 :]:
                if not nxt.strip() or nxt[:1] in (" ", "\t"):
                    block.append(nxt.strip())
                else:
                    break
            return " ".join(part for part in block if part) or None
        if len(raw) >= 2 and raw[0] == raw[-1] and raw[0] in ("'", '"'):
            return raw[1:-1].replace('\\"', '"').replace("\\\\", "\\")
        return raw or None
    return None


def yaml_quote(value: str) -> str:
    value = value.replace("\\", "\\\\").replace('"', '\\"')
    value = re.sub(r"\s+", " ", value).strip()
    return f'"{value}"'


# --------------------------------------------------------------------------
# text extraction
# --------------------------------------------------------------------------
def first_heading(text: str, fallback: str) -> str:
    for line in text.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return fallback


def summarize(body: str, limit: int = SUMMARY_LIMIT) -> str:
    """Grab the first real prose paragraph so the description is searchable."""
    buffered: list[str] = []
    in_fence = False
    for raw in body.splitlines():
        line = raw.strip()
        if line.startswith("```"):
            in_fence = not in_fence
            buffered = []
            continue
        if in_fence:
            continue
        if not line:
            if buffered:
                break
            continue
        if line.startswith(("#", ">", "-", "*", "|", "=", ":")) or re.match(
            r"^\d+[.)]", line
        ):
            if buffered:
                break
            continue
        if line.lstrip("-*-").strip() == "":
            if buffered:
                break
            continue
        buffered.append(line)

    text = re.sub(r"\s+", " ", " ".join(buffered)).strip()
    text = text.replace("$ARGUMENTS", "the target subject")
    # strip markdown emphasis so the description stays plain text
    text = re.sub(r"\*\*([^*]+)\*\*", r"\1", text)
    text = re.sub(r"`([^`]+)`", r"\1", text)
    if len(text) > limit:
        text = text[:limit].rstrip(" ,.;:") + "..."
    return text


def slugify(value: str) -> str:
    return re.sub(r"-+", "-", re.sub(r"[^a-z0-9]+", "-", value.lower())).strip("-")


def clamp(value: str, limit: int) -> str:
    value = re.sub(r"\s+", " ", value).strip()
    return value if len(value) <= limit else value[:limit].rstrip(" ,.;:") + "..."


# --------------------------------------------------------------------------
# generation
# --------------------------------------------------------------------------
def adapter_note(source_name: str) -> str:
    return (
        "## WorkBuddy adapter note\n\n"
        f"This skill is generated from `skills/{source_name}` so Claude Code, "
        "Codex and WorkBuddy users share one canonical workflow.\n\n"
        "- Treat `$ARGUMENTS` as the user's request in the current WorkBuddy "
        "session.\n"
        "- Tool mapping (Claude/Codex surface -> WorkBuddy equivalent):\n"
        "  - `Task` / `Agent` / parallel roles -> the `Agent` tool "
        "(`general-purpose` or `Explore`); run roles as parallel Agent calls.\n"
        "  - `WebSearch` -> `WebSearch` / `WebFetch`. For finance data prefer the "
        "connected data skills (e.g. `westock-data`, `ifind-finance-data`) over "
        "raw web scraping.\n"
        "  - `Bash` -> `Bash` (or `PowerShell` on Windows). Some WorkBuddy "
        "Git-Bash environments ship without coreutils; if `ls`/`dirname` are "
        "missing, prefix the command with "
        '`export PATH="/usr/bin:/bin:$PATH" `.\n'
        "  - `Read` / `Write` / `Edit` -> `Read` / `Write` / `Edit`.\n"
        "  - `TodoWrite` -> `TaskCreate` / `TaskUpdate` / `TaskList`.\n"
        "- Use shared project tools from `tools/`. Prefer running commands from "
        "the repository root with paths like "
        "`python3 tools/financial_rigor.py ...`; if the session starts outside "
        "the repo, resolve the real checkout path first instead of assuming a "
        "fixed home-directory path.\n"
        "- Before starting research, run the `date` command to confirm today's "
        "date; treat it as the baseline for \"latest\" data and state the data "
        "cutoff date in the report header. Never assume the current date from "
        "training data.\n"
        "- Preserve the research quality rules from `AGENTS.md`: cross-check "
        "financial data against two independent sources, use exact arithmetic "
        "tools (`tools/financial_rigor.py`) for valuation/math, run "
        "`tools/report_audit.py` before treating output as publishable, and "
        "clearly label uncertainty and source gaps.\n"
        "- Deliverables: write files with absolute paths, and surface any "
        "viewable result to the user instead of only describing it in chat.\n"
        "- If the environment exposes a finance entry skill (`wb-finance-skill`), "
        "load it first for finance tasks to pick up its hard constraints and "
        "timezone rules.\n"
        "- This project is for learning and research, not investment advice.\n\n"
    )


def build_frontmatter(
    name: str, source_name: str, source_text: str, prefix: str
) -> tuple[str, dict[str, str]]:
    existing, body = split_frontmatter(source_text)
    preserved: dict[str, str] = {}
    if existing:
        for key in ("name", "description", "description_zh", "description_en",
                    "display_name", "display_name_en", "version"):
            value = yaml_field(existing, key)
            if value:
                preserved[key] = value

    base_name = slugify(preserved.get("name") or name) or name
    final_name = slugify(f"{prefix}{base_name}")

    title = first_heading(body, base_name)
    summary = summarize(body)

    description = preserved.get("description") or clamp(
        f"AI Berkshire skill: {title}. {summary} Source: skills/{source_name}."
        if summary
        else f"AI Berkshire skill: {title}. Source: skills/{source_name}.",
        DESC_LIMIT,
    )
    description_zh = preserved.get("description_zh") or clamp(
        f"{title}。{summary}" if summary else title, DESC_LIMIT
    )

    lines = [
        "---",
        f"name: {final_name}",
        f"description: {yaml_quote(description)}",
        f"description_zh: {yaml_quote(description_zh)}",
    ]
    for key in ("description_en", "display_name_en"):
        if key in preserved:
            lines.append(f"{key}: {yaml_quote(preserved[key])}")
    lines.append(f"display_name: {yaml_quote(clamp(title, 60))}")
    lines.append(f"version: {preserved.get('version', '1.0.0')}")
    lines.append("agent_created: true")
    lines.append("---")
    return "\n".join(lines) + "\n\n", {
        "name": final_name,
        "title": title,
        "summary": summary,
    }


def render(name: str, source_name: str, source_text: str, prefix: str) -> str:
    _, body = split_frontmatter(source_text)
    frontmatter, _ = build_frontmatter(name, source_name, source_text, prefix)
    return frontmatter + adapter_note(source_name) + body.rstrip() + "\n"


# --------------------------------------------------------------------------
# cli
# --------------------------------------------------------------------------
def parse_args(argv: list[str]) -> tuple[dict, list[str]]:
    options = {
        "check": False,
        "prune": False,
        "verbose": False,
        "prefix": "",
        "only": None,
        "out": None,
    }
    rest: list[str] = []
    index = 0
    while index < len(argv):
        arg = argv[index]
        if arg == "--check":
            options["check"] = True
        elif arg == "--prune":
            options["prune"] = True
        elif arg in ("--verbose", "-v"):
            options["verbose"] = True
        elif arg.startswith("--prefix="):
            options["prefix"] = arg.split("=", 1)[1]
        elif arg == "--prefix":
            index += 1
            options["prefix"] = argv[index]
        elif arg.startswith("--only="):
            options["only"] = [p.strip() for p in arg.split("=", 1)[1].split(",")]
        elif arg == "--only":
            index += 1
            options["only"] = [p.strip() for p in argv[index].split(",")]
        elif arg.startswith("--out="):
            options["out"] = arg.split("=", 1)[1]
        elif arg == "--out":
            index += 1
            options["out"] = argv[index]
        elif arg in ("-h", "--help"):
            print(__doc__)
            raise SystemExit(0)
        else:
            rest.append(arg)
        index += 1
    return options, rest


def main() -> None:
    options, unknown = parse_args(sys.argv[1:])
    if unknown:
        raise SystemExit("Unknown argument(s): " + ", ".join(unknown))

    output_dir = (
        Path(options["out"]).expanduser()
        if options["out"]
        else Path(os.environ.get("WORKBUDDY_SKILLS_DIR", WORKBUDDY_SKILLS)).expanduser()
    )
    prefix = options["prefix"]
    if prefix and not prefix.endswith("-"):
        prefix += "-"

    sources = sorted(CLAUDE_SKILLS.glob("*.md"))
    if options["only"]:
        wanted = set(options["only"])
        sources = [s for s in sources if s.stem in wanted]

    if not options["check"]:
        output_dir.mkdir(parents=True, exist_ok=True)

    count = 0
    stale: list[str] = []
    for source in sources:
        name = source.stem
        source_text = source.read_text(encoding="utf-8")
        target_dir = output_dir / f"{prefix}{name}"
        target = target_dir / "SKILL.md"
        content = render(name, source.name, source_text, prefix)

        if options["check"]:
            if not target.exists() or target.read_text(encoding="utf-8") != content:
                stale.append(str(target.relative_to(ROOT)))
        else:
            target_dir.mkdir(parents=True, exist_ok=True)
            target.write_text(content, encoding="utf-8")
            if options["verbose"]:
                meta = build_frontmatter(name, source.name, source_text, prefix)[1]
                print(f"  {meta['name']:<28} {meta['title']}")
        count += 1

    orphans: list[str] = []
    if output_dir.exists():
        generated = {f"{prefix}{s.stem}" for s in sources}
        for child in sorted(output_dir.iterdir()):
            if not child.is_dir() or child.name in generated:
                continue
            marker = child / "SKILL.md"
            if not marker.exists():
                continue
            text = marker.read_text(encoding="utf-8")
            if ADAPTER_MARKER not in text:
                orphans.append(child.name + " (hand-written, kept)")
                continue
            orphans.append(child.name + " (stale)")
            if options["prune"] and not options["check"]:
                for path in sorted(child.rglob("*"), reverse=True):
                    path.rmdir() if path.is_dir() else path.unlink()

    if options["check"]:
        if stale:
            print("WorkBuddy skills are out of date:")
            for path in stale:
                print(f"  {path}")
            raise SystemExit(1)
        try:
            shown = output_dir.relative_to(ROOT)
        except ValueError:
            shown = output_dir
        print(f"Checked {count} WorkBuddy skills in {shown}")
        return

    try:
        shown = output_dir.relative_to(ROOT)
    except ValueError:
        shown = output_dir
    print(f"Generated {count} WorkBuddy skills in {shown}")
    if prefix:
        print(f"Name prefix applied: {prefix}")
    if orphans:
        print("Unmanaged packages:")
        for item in orphans:
            print(f"  {item}")
        if any("stale" in item for item in orphans):
            print("Re-run with --prune to remove stale generated packages.")


if __name__ == "__main__":
    main()
