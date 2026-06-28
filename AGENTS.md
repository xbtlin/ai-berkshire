# AI Berkshire Codex Guide

This repository contains investment research workflows, reports, and shared
validation tools. Keep compatibility with both Claude Code and Codex users.

## Project Layout

- `skills/*.md`: Claude Code slash-command source files.
- `codex-skills/*/SKILL.md`: Codex skill packages. Most are generated from
  `skills/*.md`; Codex-only hand-written packages are allowed when clearly
  marked and no same-named `skills/*.md` source exists.
- `codex-prompts/*.md`: generated Codex custom prompts for slash-command
  style entry points. These are a compatibility layer; skills remain preferred.
- `tools/*.py`: shared financial validation and data tools used by both systems.
- `reports/`: research outputs. Do not rewrite unrelated reports while changing
  tooling or skills.
- `scripts/sync-codex-skills.py`: regenerates Codex skills from `skills/*.md`.
- `scripts/install-codex-skills.sh`: installs Codex skills locally.
- `scripts/install-codex-prompts.sh`: installs generated Codex slash prompts
  locally.
- `scripts/install-claude-commands.sh`: installs Claude Code commands locally.

## Compatibility Rules

- Treat `skills/*.md` as the canonical workflow source.
- After changing any file in `skills/`, run:
  `python3 scripts/sync-codex-skills.py`
- If slash prompt compatibility is needed, also run:
  `python3 scripts/sync-codex-prompts.py`
- Do not manually edit generated `codex-skills/*/SKILL.md` unless also updating
  the corresponding source in `skills/`.
- For Codex-only hand-written packages under `codex-skills/`, keep them clearly
  marked as Codex-only and do not create a same-named `skills/*.md` file unless
  intentionally adopting the workflow for Claude Code too.
- Keep tool paths compatible with the documented checkout path:
  `~/ai-berkshire/tools/...`
- Keep `CLAUDE.md` for Claude Code behavior and this `AGENTS.md` for Codex
  behavior.

## Research Quality Rules

- Financial data must come from at least two independent sources when the skill
  requires verification.
- Use exact arithmetic tools for market cap, valuation, cross-source checks, and
  scenario analysis:
  `python3 tools/financial_rigor.py ...`
- Use report audit tooling before treating generated research as publishable:
  `python3 tools/report_audit.py ...`
- Clearly label low-confidence conclusions, incomplete data, and source gaps.
- This project is for learning and research, not investment advice.
- Source-sufficiency is enforced by a deterministic gate, not by memory. Any
  report under `reports/**.md` must cite >= 2 independent recognized sources.
  Check locally:
  `python3 tools/report_audit.py sources --report reports/<path>.md`

## Commit Gate (one-time setup per clone)

A versioned pre-commit hook in `.githooks/` blocks committing under-sourced
reports. Enable it once after cloning:
  `git config core.hooksPath .githooks`
Bypass only when you knowingly accept responsibility: `git commit --no-verify`.

The same source check also runs server-side in CI (`.github/workflows/report-gate.yml`)
on every PR, so a local `--no-verify` cannot land an under-sourced report on `main`.
The CI also runs a regression eval guarding the sensor itself:
  `python3 tools/eval_sources.py`
When you change source detection in `report_audit.py`, add a case to
`tools/eval_sources.py` for any newly-handled source or fixed miss.

## Editing Rules

- Preserve existing report files unless the task specifically asks to change
  them.
- Keep changes scoped to the requested skill, tool, script, or documentation.
- Before finishing a skill/tool change, run the relevant syntax or generation
  check. For compatibility changes, run:
  `python3 scripts/sync-codex-skills.py`
- To verify generated Codex artifacts are current without rewriting files, run:
  `python3 scripts/sync-codex-skills.py --check`
  and, when slash prompts are relevant:
  `python3 scripts/sync-codex-prompts.py --check`
