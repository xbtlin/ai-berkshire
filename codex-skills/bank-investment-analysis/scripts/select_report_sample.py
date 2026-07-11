#!/usr/bin/env python3
"""Select a traceable deep-reading set of official bank reports."""

from __future__ import annotations

import argparse
import csv
import json
from collections import Counter
from pathlib import Path

from resolve_cninfo_reports import (
    announcement_period,
    announcement_url,
    choose_primary,
    clean_title,
    timestamp_to_date,
    usable_full_report,
)


Key = tuple[str, str, str]


def load_csv(path: Path) -> tuple[list[dict[str, str]], list[str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        return list(reader), list(reader.fieldnames or [])


def row_key(row: dict[str, str]) -> Key:
    return row["bank"], row["report_year"], row["report_period"]


def add_reason(
    selected: dict[Key, dict[str, str]], row: dict[str, str], reason: str
) -> None:
    key = row_key(row)
    if key not in selected:
        selected[key] = dict(row)
        selected[key]["selection_reasons"] = reason
        return
    reasons = set(filter(None, selected[key]["selection_reasons"].split("|")))
    reasons.add(reason)
    selected[key]["selection_reasons"] = "|".join(sorted(reasons))


def load_cache_index(cache_dir: Path) -> dict[tuple[str, str, str], list[dict[str, object]]]:
    index: dict[tuple[str, str, str], list[dict[str, object]]] = {}
    for cache_path in sorted(cache_dir.glob("*.json")):
        payload = json.loads(cache_path.read_text(encoding="utf-8"))
        code = str(payload.get("code") or cache_path.stem)
        for announcement in payload.get("announcements") or []:
            if not usable_full_report(announcement):
                continue
            period = announcement_period(str(announcement.get("announcementTitle") or ""))
            if period:
                index.setdefault((code, period[0], period[1]), []).append(announcement)
    return index


def synthetic_row(
    anchor: dict[str, str],
    year: str,
    period: str,
    cache_index: dict[tuple[str, str, str], list[dict[str, object]]],
) -> dict[str, str] | None:
    candidates = cache_index.get((anchor["a_code"], year, period), [])
    primary = choose_primary(candidates)
    if not primary:
        return None
    row = {key: "" for key in anchor}
    row.update(
        {
            "bank": anchor["bank"],
            "a_code": anchor["a_code"],
            "exchange": anchor["exchange"],
            "h_code": anchor.get("h_code", ""),
            "report_year": year,
            "report_period": period,
            "report_label": {"Q1": "第一季度报告", "H1": "半年度报告", "Q3": "第三季度报告", "FY": "年度报告"}.get(period, period),
            "article_count": "0",
            "full_forecast_count": "0",
            "paid_forecast_count": "0",
            "full_review_count": "0",
            "comparison_count": "0",
            "ir_url": anchor.get("ir_url", ""),
            "official_report_url": announcement_url(primary),
            "source_status": "resolved_synthetic_input",
            "source_notes": "Added as a pre-forecast input or seasonal baseline; no direct corpus article mapping",
            "announcement_id": str(primary.get("announcementId") or ""),
            "announcement_title": clean_title(str(primary.get("announcementTitle") or "")),
            "announcement_date": timestamp_to_date(primary.get("announcementTime")),
            "announcement_size_kb": str(primary.get("adjunctSize") or ""),
            "alternate_report_urls": json.dumps(
                [announcement_url(item) for item in candidates if announcement_url(item) != announcement_url(primary)],
                ensure_ascii=False,
            ),
        }
    )
    return row


def select_forecast_inputs(
    rows: list[dict[str, str]],
    by_key: dict[Key, dict[str, str]],
    cache_index: dict[tuple[str, str, str], list[dict[str, object]]],
    selected: dict[Key, dict[str, str]],
) -> None:
    for row in rows:
        if int(row.get("full_forecast_count") or 0) <= 0:
            continue
        add_reason(selected, row, "forecast_target_actual")
        inputs = json.loads(row.get("prior_input_periods") or "[]")
        target_year = int(row["report_year"])
        target_period = row["report_period"]
        for offset in (1, 2):
            baseline_year = target_year - offset
            if baseline_year >= 2017:
                inputs.append({"year": str(baseline_year), "period": target_period})
        for input_period in inputs:
            key = (row["bank"], str(input_period["year"]), str(input_period["period"]))
            input_row = by_key.get(key)
            if input_row is None:
                input_row = synthetic_row(
                    row,
                    key[1],
                    key[2],
                    cache_index,
                )
            if input_row:
                add_reason(selected, input_row, "forecast_pre_cutoff_input")


def add_diverse_reviews(
    rows: list[dict[str, str]],
    selected: dict[Key, dict[str, str]],
    minimum: int,
) -> None:
    candidates = [
        row
        for row in rows
        if int(row.get("full_review_count") or 0) > 0 and row_key(row) not in selected
    ]
    covered_banks = {key[0] for key in selected}
    covered_years = {key[1] for key in selected}
    covered_periods = {key[2] for key in selected}

    while len(selected) < minimum and candidates:
        def score(row: dict[str, str]) -> tuple[int, int, int, int, int, str, str, str]:
            key = row_key(row)
            return (
                int(key[0] not in covered_banks),
                int(key[1] not in covered_years),
                int(key[2] not in covered_periods),
                int(row.get("full_review_count") or 0),
                int(row.get("article_count") or 0),
                key[1],
                key[0],
                key[2],
            )

        chosen = max(candidates, key=score)
        candidates.remove(chosen)
        add_reason(selected, chosen, "stratified_earnings_review")
        key = row_key(chosen)
        covered_banks.add(key[0])
        covered_years.add(key[1])
        covered_periods.add(key[2])


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--map", type=Path, required=True, help="Resolved report map CSV")
    parser.add_argument("--cache-dir", type=Path, required=True, help="CNINFO metadata cache")
    parser.add_argument("--output", type=Path, required=True, help="Selected report CSV")
    parser.add_argument("--minimum", type=int, default=150, help="Minimum unique reports")
    parser.add_argument("--summary", type=Path, help="Optional JSON summary")
    args = parser.parse_args()

    rows, fields = load_csv(args.map.expanduser().resolve())
    by_key = {row_key(row): row for row in rows}
    cache_index = load_cache_index(args.cache_dir.expanduser().resolve())
    selected: dict[Key, dict[str, str]] = {}

    for row in rows:
        if int(row.get("comparison_count") or 0) > 0:
            add_reason(selected, row, "cross_bank_comparison")
    select_forecast_inputs(rows, by_key, cache_index, selected)
    add_diverse_reviews(rows, selected, args.minimum)

    output_rows = [selected[key] for key in sorted(selected)]
    output_fields = list(dict.fromkeys(fields + ["selection_reasons"]))
    output = args.output.expanduser().resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=output_fields)
        writer.writeheader()
        writer.writerows(output_rows)

    reasons = Counter(
        reason
        for row in output_rows
        for reason in row["selection_reasons"].split("|")
        if reason
    )
    summary = {
        "selected_report_count": len(output_rows),
        "estimated_download_mb": round(
            sum(int(row.get("announcement_size_kb") or 0) for row in output_rows) / 1024,
            1,
        ),
        "bank_count": len({row["bank"] for row in output_rows}),
        "year_count": len({row["report_year"] for row in output_rows}),
        "period_counts": dict(Counter(row["report_period"] for row in output_rows)),
        "selection_reason_counts_overlapping": dict(reasons),
    }
    if args.summary:
        summary_path = args.summary.expanduser().resolve()
        summary_path.parent.mkdir(parents=True, exist_ok=True)
        summary_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
