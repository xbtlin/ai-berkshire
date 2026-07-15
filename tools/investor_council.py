#!/usr/bin/env python3
"""Select and inspect source-grounded investor philosophy lenses.

This tool does not score securities or generate investment advice. It validates the
philosophy-card registry and deterministically selects a diverse set of lenses for a
research scenario. The selected lenses are then used by the investor-council skill.

Examples:
    python3 tools/investor_council.py validate
    python3 tools/investor_council.py list
    python3 tools/investor_council.py show howard-marks
    python3 tools/investor_council.py select --scenario company --format markdown
    python3 tools/investor_council.py select --scenario portfolio --focus costs,regime
    python3 tools/investor_council.py select --lenses benjamin-graham,philip-fisher
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any, Iterable
from urllib.parse import urlparse


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DATA = ROOT / "data" / "investor_philosophies.json"

ALLOWED_SCOPES = {"company", "security", "portfolio", "behavior"}
ALLOWED_SOURCE_KINDS = {
    "primary",
    "primary_platform",
    "official_firm",
    "official_archive",
    "institutional_archive",
    "publisher",
}
REQUIRED_INVESTOR_FIELDS = {
    "id",
    "name",
    "name_zh",
    "school",
    "scope",
    "summary",
    "principles",
    "questions",
    "focus_tags",
    "best_for",
    "limitations",
    "sources",
}


class LibraryError(ValueError):
    """Raised when the philosophy registry cannot be used safely."""


def load_library(path: Path | str = DEFAULT_DATA) -> dict[str, Any]:
    """Load a philosophy-card registry from JSON."""
    source = Path(path)
    try:
        with source.open("r", encoding="utf-8") as handle:
            data = json.load(handle)
    except FileNotFoundError as exc:
        raise LibraryError(f"哲学资料库不存在: {source}") from exc
    except json.JSONDecodeError as exc:
        raise LibraryError(f"哲学资料库 JSON 无效: {exc}") from exc
    if not isinstance(data, dict):
        raise LibraryError("哲学资料库顶层必须是 JSON object")
    return data


def _is_nonempty_string(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _validate_string_list(
    errors: list[str], value: Any, location: str, *, minimum: int = 1
) -> list[str]:
    if not isinstance(value, list) or len(value) < minimum:
        errors.append(f"{location} 必须是至少包含 {minimum} 项的数组")
        return []
    cleaned: list[str] = []
    for index, item in enumerate(value):
        if not _is_nonempty_string(item):
            errors.append(f"{location}[{index}] 必须是非空字符串")
        else:
            cleaned.append(item.strip())
    if len(cleaned) != len(set(cleaned)):
        errors.append(f"{location} 不能包含重复项")
    return cleaned


def validate_library(data: dict[str, Any]) -> list[str]:
    """Return all registry validation errors; an empty list means valid."""
    errors: list[str] = []

    if data.get("schema_version") != 1:
        errors.append("schema_version 必须为 1")

    reviewed_at = data.get("reviewed_at")
    if not _is_nonempty_string(reviewed_at) or not re.fullmatch(
        r"\d{4}-\d{2}-\d{2}", reviewed_at or ""
    ):
        errors.append("reviewed_at 必须是 YYYY-MM-DD")

    taxonomy = data.get("focus_taxonomy")
    if not isinstance(taxonomy, dict) or not taxonomy:
        errors.append("focus_taxonomy 必须是非空 object")
        taxonomy = {}
    else:
        for tag, label in taxonomy.items():
            if not re.fullmatch(r"[a-z][a-z0-9_]*", str(tag)):
                errors.append(f"focus_taxonomy tag 无效: {tag}")
            if not _is_nonempty_string(label):
                errors.append(f"focus_taxonomy.{tag} 必须有说明")
    known_tags = set(taxonomy)

    investors = data.get("investors")
    if not isinstance(investors, list) or not investors:
        errors.append("investors 必须是非空数组")
        investors = []

    investor_ids: list[str] = []
    for index, investor in enumerate(investors):
        location = f"investors[{index}]"
        if not isinstance(investor, dict):
            errors.append(f"{location} 必须是 object")
            continue

        missing = REQUIRED_INVESTOR_FIELDS - set(investor)
        if missing:
            errors.append(f"{location} 缺少字段: {', '.join(sorted(missing))}")
            continue

        investor_id = investor.get("id")
        if not _is_nonempty_string(investor_id) or not re.fullmatch(
            r"[a-z0-9]+(?:-[a-z0-9]+)*", investor_id or ""
        ):
            errors.append(f"{location}.id 必须是小写 kebab-case")
        else:
            investor_ids.append(investor_id)

        for field in ("name", "name_zh", "school", "summary"):
            if not _is_nonempty_string(investor.get(field)):
                errors.append(f"{location}.{field} 必须是非空字符串")

        scopes = _validate_string_list(errors, investor.get("scope"), f"{location}.scope")
        unknown_scopes = set(scopes) - ALLOWED_SCOPES
        if unknown_scopes:
            errors.append(
                f"{location}.scope 含未知值: {', '.join(sorted(unknown_scopes))}"
            )

        for field in ("principles", "questions", "best_for", "limitations"):
            _validate_string_list(errors, investor.get(field), f"{location}.{field}")

        focus_tags = _validate_string_list(
            errors, investor.get("focus_tags"), f"{location}.focus_tags"
        )
        unknown_tags = set(focus_tags) - known_tags
        if unknown_tags:
            errors.append(
                f"{location}.focus_tags 含未知值: {', '.join(sorted(unknown_tags))}"
            )

        sources = investor.get("sources")
        if not isinstance(sources, list) or not sources:
            errors.append(f"{location}.sources 必须至少包含一个来源")
            continue
        source_urls: list[str] = []
        for source_index, source in enumerate(sources):
            source_location = f"{location}.sources[{source_index}]"
            if not isinstance(source, dict):
                errors.append(f"{source_location} 必须是 object")
                continue
            title = source.get("title")
            url = source.get("url")
            kind = source.get("kind")
            if not _is_nonempty_string(title):
                errors.append(f"{source_location}.title 必须是非空字符串")
            if not _is_nonempty_string(url):
                errors.append(f"{source_location}.url 必须是非空字符串")
            else:
                parsed = urlparse(url)
                if parsed.scheme != "https" or not parsed.netloc:
                    errors.append(f"{source_location}.url 必须是有效 HTTPS URL")
                source_urls.append(url)
            if kind not in ALLOWED_SOURCE_KINDS:
                errors.append(f"{source_location}.kind 未获支持: {kind}")
        if len(source_urls) != len(set(source_urls)):
            errors.append(f"{location}.sources 不能包含重复 URL")

    if len(investor_ids) != len(set(investor_ids)):
        errors.append("investor id 不能重复")
    known_investors = set(investor_ids)

    scenarios = data.get("scenarios")
    if not isinstance(scenarios, dict) or not scenarios:
        errors.append("scenarios 必须是非空 object")
        scenarios = {}
    for scenario_id, scenario in scenarios.items():
        location = f"scenarios.{scenario_id}"
        if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", str(scenario_id)):
            errors.append(f"scenario id 无效: {scenario_id}")
        if not isinstance(scenario, dict):
            errors.append(f"{location} 必须是 object")
            continue
        if not _is_nonempty_string(scenario.get("description")):
            errors.append(f"{location}.description 必须是非空字符串")
        scenario_tags = _validate_string_list(
            errors, scenario.get("focus_tags"), f"{location}.focus_tags"
        )
        unknown_tags = set(scenario_tags) - known_tags
        if unknown_tags:
            errors.append(
                f"{location}.focus_tags 含未知值: {', '.join(sorted(unknown_tags))}"
            )
        defaults = _validate_string_list(
            errors,
            scenario.get("default_lenses"),
            f"{location}.default_lenses",
            minimum=2,
        )
        unknown_defaults = set(defaults) - known_investors
        if unknown_defaults:
            errors.append(
                f"{location}.default_lenses 含未知投资家: "
                + ", ".join(sorted(unknown_defaults))
            )

    return errors


def require_valid_library(data: dict[str, Any]) -> None:
    errors = validate_library(data)
    if errors:
        joined = "\n".join(f"- {error}" for error in errors)
        raise LibraryError(f"哲学资料库验证失败:\n{joined}")


def investor_index(data: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {investor["id"]: investor for investor in data["investors"]}


def _split_csv(value: str | None) -> list[str]:
    if not value:
        return []
    return [part.strip() for part in value.split(",") if part.strip()]


def _dedupe(items: Iterable[str]) -> list[str]:
    return list(dict.fromkeys(items))


def select_lenses(
    data: dict[str, Any],
    *,
    scenario_id: str = "company",
    focus_tags: Iterable[str] = (),
    limit: int = 4,
    explicit_ids: Iterable[str] = (),
) -> dict[str, Any]:
    """Select lenses, preserving scenario defaults unless custom focus is supplied."""
    require_valid_library(data)
    if not 1 <= limit <= 6:
        raise LibraryError("limit 必须在 1 到 6 之间")

    scenarios = data["scenarios"]
    if scenario_id not in scenarios:
        raise LibraryError(
            f"未知 scenario: {scenario_id}; 可选: {', '.join(sorted(scenarios))}"
        )
    scenario = scenarios[scenario_id]
    investors = investor_index(data)

    explicit = _dedupe(explicit_ids)
    unknown_investors = set(explicit) - set(investors)
    if unknown_investors:
        raise LibraryError(
            "未知投资家 lens: " + ", ".join(sorted(unknown_investors))
        )
    if len(explicit) > limit:
        raise LibraryError("显式 lenses 数量不能超过 limit")

    custom_focus = _dedupe(focus_tags)
    unknown_tags = set(custom_focus) - set(data["focus_taxonomy"])
    if unknown_tags:
        raise LibraryError("未知 focus tag: " + ", ".join(sorted(unknown_tags)))
    effective_focus = _dedupe([*scenario["focus_tags"], *custom_focus])

    if explicit:
        selected_ids = explicit
        selection_mode = "explicit"
    elif not custom_focus:
        selected_ids = scenario["default_lenses"][:limit]
        selection_mode = "scenario-default"
    else:
        defaults = set(scenario["default_lenses"])
        scenario_focus = set(scenario["focus_tags"])
        requested_focus = set(custom_focus)
        ranked: list[tuple[int, str, set[str], set[str]]] = []
        for investor in data["investors"]:
            matched = set(investor["focus_tags"]) & set(effective_focus)
            matched_requested = set(investor["focus_tags"]) & requested_focus
            scenario_score = len(set(investor["focus_tags"]) & scenario_focus) * 10
            score = (
                len(matched_requested) * 100
                + scenario_score
                + (4 if investor["id"] in defaults else 0)
            )
            ranked.append((score, investor["id"], matched, matched_requested))

        selected_ids = []
        selected_schools: set[str] = set()
        covered: set[str] = set()
        remaining = ranked[:]

        def adjusted(
            item: tuple[int, str, set[str], set[str]], *, prioritize_requested: bool
        ) -> tuple[int, int, int, str]:
            base_score, investor_id, matched, matched_requested = item
            school = investors[investor_id]["school"]
            diversity = 4 if school not in selected_schools else -6
            marginal = len(matched - covered) * 3
            requested_marginal = len(matched_requested - covered)
            requested_priority = requested_marginal * 1000 if prioritize_requested else 0
            return (
                base_score + diversity + marginal + requested_priority,
                requested_marginal,
                len(matched),
                investor_id,
            )

        def add_best(*, prioritize_requested: bool) -> bool:
            candidates = remaining
            if prioritize_requested:
                candidates = [
                    item for item in remaining if item[3] - covered
                ]
            if not candidates:
                return False

            best = max(
                candidates,
                key=lambda item: adjusted(
                    item, prioritize_requested=prioritize_requested
                ),
            )
            remaining.remove(best)
            _, investor_id, matched, _ = best
            selected_ids.append(investor_id)
            selected_schools.add(investors[investor_id]["school"])
            covered.update(matched)
            return True

        # A user-supplied focus is a requirement, not a weak hint. Cover as
        # many requested tags as the lens limit permits before filling the
        # remaining seats with scenario-fit and diversity.
        while (
            remaining
            and len(selected_ids) < limit
            and requested_focus - covered
            and add_best(prioritize_requested=True)
        ):
            pass
        while remaining and len(selected_ids) < limit:
            add_best(prioritize_requested=False)
        selection_mode = "focus-ranked"

    selected: list[dict[str, Any]] = []
    for investor_id in selected_ids:
        investor = investors[investor_id]
        matched = [tag for tag in effective_focus if tag in investor["focus_tags"]]
        selected.append(
            {
                "id": investor_id,
                "name": investor["name"],
                "name_zh": investor["name_zh"],
                "school": investor["school"],
                "scope": investor["scope"],
                "summary": investor["summary"],
                "principles": investor["principles"],
                "matched_focus": matched,
                "questions": investor["questions"],
                "best_for": investor["best_for"],
                "limitations": investor["limitations"],
                "sources": investor["sources"],
            }
        )

    selected_coverage = {
        tag
        for lens in selected
        for tag in lens["matched_focus"]
    }
    uncovered_focus = [
        tag for tag in custom_focus if tag not in selected_coverage
    ]

    return {
        "schema_version": data["schema_version"],
        "library_reviewed_at": data["reviewed_at"],
        "scenario": scenario_id,
        "scenario_description": scenario["description"],
        "selection_mode": selection_mode,
        "focus_tags": effective_focus,
        "requested_focus_tags": custom_focus,
        "uncovered_focus_tags": uncovered_focus,
        "selected_lenses": selected,
    }


def render_selection_markdown(selection: dict[str, Any]) -> str:
    """Render selection cards without pretending to speak as an investor."""
    lines = [
        f"## 投资家评议会：{selection['scenario']}",
        "",
        f"- 资料库复核日：{selection['library_reviewed_at']}",
        f"- 选择模式：{selection['selection_mode']}",
        f"- 场景：{selection['scenario_description']}",
        f"- 关注轴：{', '.join(selection['focus_tags'])}",
        f"- 用户追加关注轴：{', '.join(selection['requested_focus_tags']) or '无'}",
        "",
        "| Lens | 学派 | 适用范围 | 命中关注轴 |",
        "|---|---|---|---|",
    ]
    for lens in selection["selected_lenses"]:
        lines.append(
            "| {name_zh} ({name}) | {school} | {scope} | {focus} |".format(
                name_zh=lens["name_zh"],
                name=lens["name"],
                school=lens["school"],
                scope=", ".join(lens["scope"]),
                focus=", ".join(lens["matched_focus"]) or "补充/反方",
            )
        )
    lines.extend(["", "### 分析卡", ""])
    for lens in selection["selected_lenses"]:
        lines.extend(
            [
                f"#### {lens['name_zh']} ({lens['id']})",
                "",
                lens["summary"],
                "",
                "核心原则：",
                "",
                *[f"- {principle}" for principle in lens["principles"]],
                "",
                "关键问题：",
                "",
                *[f"- {question}" for question in lens["questions"]],
                "",
                "适用场景：",
                "",
                *[f"- {use_case}" for use_case in lens["best_for"]],
                "",
                "适用限制：",
                "",
                *[f"- {limitation}" for limitation in lens["limitations"]],
                "",
                "资料来源：",
                "",
                *[
                    f"- [{source['title']}]({source['url']}) ({source['kind']})"
                    for source in lens["sources"]
                ],
                "",
            ]
        )
    if selection["uncovered_focus_tags"]:
        lines.extend(
            [
                "> ⚠️ 受 lens 数量上限限制，以下追加关注轴尚未覆盖："
                + ", ".join(selection["uncovered_focus_tags"]),
                "",
            ]
        )
    lines.append(
        "> 以上为公开资料启发的分析 lens，不代表投资家本人对当前标的的观点。"
    )
    return "\n".join(lines)


def render_library_list(data: dict[str, Any]) -> str:
    lines = [
        "| id | 投资家 | 学派 | 适用范围 |",
        "|---|---|---|---|",
    ]
    for investor in sorted(data["investors"], key=lambda item: item["id"]):
        lines.append(
            f"| {investor['id']} | {investor['name_zh']} ({investor['name']}) "
            f"| {investor['school']} | {', '.join(investor['scope'])} |"
        )
    return "\n".join(lines)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Investor Council — 出典付き投資哲学 lens 选择工具"
    )
    parser.add_argument(
        "--data",
        type=Path,
        default=DEFAULT_DATA,
        help=f"资料库 JSON（默认: {DEFAULT_DATA}）",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("validate", help="验证哲学资料库 schema 和来源")
    sub.add_parser("list", help="列出可用投资家 lens")

    show = sub.add_parser("show", help="显示单个投资家 lens 的完整资料卡")
    show.add_argument("investor_id", help="投资家 id")

    select = sub.add_parser("select", help="按场景或关注轴选择 lens")
    select.add_argument("--scenario", default="company", help="研究场景")
    select.add_argument("--focus", default="", help="额外关注轴，逗号分隔")
    select.add_argument("--lenses", default="", help="显式 lens id，逗号分隔")
    select.add_argument("--limit", type=int, default=4, help="最多 lens 数，1-6")
    select.add_argument(
        "--format",
        choices=("markdown", "json", "ids"),
        default="markdown",
        help="输出格式",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        data = load_library(args.data)
        errors = validate_library(data)
        if errors:
            if args.command == "validate":
                print("❌ 哲学资料库验证失败:")
                for error in errors:
                    print(f"  - {error}")
                return 1
            require_valid_library(data)

        if args.command == "validate":
            print(
                f"✅ 哲学资料库有效: {len(data['investors'])} 位投资家, "
                f"{len(data['scenarios'])} 个场景, 复核日 {data['reviewed_at']}"
            )
            return 0
        if args.command == "list":
            print(render_library_list(data))
            return 0
        if args.command == "show":
            investors = investor_index(data)
            if args.investor_id not in investors:
                raise LibraryError(f"未知投资家 lens: {args.investor_id}")
            print(json.dumps(investors[args.investor_id], ensure_ascii=False, indent=2))
            return 0
        if args.command == "select":
            selection = select_lenses(
                data,
                scenario_id=args.scenario,
                focus_tags=_split_csv(args.focus),
                limit=args.limit,
                explicit_ids=_split_csv(args.lenses),
            )
            if selection["uncovered_focus_tags"] and args.format in {"json", "ids"}:
                print(
                    "⚠️ lens 数量上限内未覆盖的用户追加关注轴: "
                    + ", ".join(selection["uncovered_focus_tags"]),
                    file=sys.stderr,
                )
            if args.format == "json":
                print(json.dumps(selection, ensure_ascii=False, indent=2))
            elif args.format == "ids":
                print(",".join(lens["id"] for lens in selection["selected_lenses"]))
            else:
                print(render_selection_markdown(selection))
            return 0
    except LibraryError as exc:
        print(f"❌ {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
