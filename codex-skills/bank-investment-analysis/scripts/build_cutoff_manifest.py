#!/usr/bin/env python3
"""Build eligible/sealed manifests for a point-in-time bank forecast."""

from __future__ import annotations

import argparse
import csv
import json
from datetime import date, datetime, time
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--cutoff",
        required=True,
        help="ISO date or timestamp. Use a timezone offset for same-day strict ordering.",
    )
    parser.add_argument("--bank", required=True)
    parser.add_argument("--target-year")
    parser.add_argument("--target-period")
    parser.add_argument(
        "--independent-replay",
        action="store_true",
        help="Seal forecast articles for the target period even if published before cutoff.",
    )
    parser.add_argument("--articles", type=Path, required=True)
    parser.add_argument("--report-map", type=Path, required=True)
    parser.add_argument("--research-root", type=Path, required=True)
    parser.add_argument(
        "--extra-sealed",
        action="append",
        default=[],
        help="Additional file/path/URL to place in the sealed list; repeat as needed.",
    )
    parser.add_argument("--output", type=Path, required=True)
    return parser.parse_args()


def parse_cutoff(value: str) -> tuple[datetime, bool]:
    has_time = "T" in value or " " in value
    if has_time:
        return datetime.fromisoformat(value), True
    return datetime.combine(date.fromisoformat(value), time.max), False


def classify(publication_date: str, cutoff: datetime, cutoff_has_time: bool) -> str:
    value = (publication_date or "").strip()
    if not value:
        return "sealed_unknown_date"
    publication_has_time = "T" in value or " " in value
    if publication_has_time:
        published = datetime.fromisoformat(value.replace(" ", "T", 1))
        if cutoff.tzinfo is not None and published.tzinfo is None:
            return "sealed_unknown_timezone"
        if cutoff.tzinfo is None and published.tzinfo is not None:
            return "sealed_unknown_timezone"
        return "eligible" if published <= cutoff else "sealed"
    published_date = date.fromisoformat(value[:10])
    if cutoff_has_time and published_date == cutoff.date():
        return "sealed_unknown_time"
    return "eligible" if published_date <= cutoff.date() else "sealed"


def require_columns(path: Path, fieldnames: list[str] | None, required: set[str]) -> None:
    missing = sorted(required - set(fieldnames or []))
    if missing:
        raise ValueError(f"{path} is missing required columns: {', '.join(missing)}")


def main() -> None:
    args = parse_args()
    if args.independent_replay and not (args.target_year and args.target_period):
        raise ValueError(
            "--independent-replay requires both --target-year and --target-period"
        )
    cutoff, cutoff_has_time = parse_cutoff(args.cutoff)
    rows: list[dict] = []

    with args.articles.open(encoding="utf-8") as handle:
        for line in handle:
            article = json.loads(line)
            if args.bank not in (article.get("banks") or []):
                continue
            published = article.get("publish_date", "")
            status = classify(published, cutoff, cutoff_has_time)
            categories = set(article.get("categories") or [])
            is_target_forecast = (
                args.independent_replay
                and "earnings_forecast" in categories
                and str(article.get("report_year", "")) == str(args.target_year or "")
                and str(article.get("report_period", "")) == str(args.target_period or "")
            )
            if is_target_forecast:
                status = "sealed"
            rows.append(
                {
                    "kind": "article",
                    "status": status,
                    "publication_date": published or "unknown",
                    "label": article.get("title", ""),
                    "path_or_url": article.get("source_path") or article.get("source_url", ""),
                }
            )

    with args.report_map.open(encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        require_columns(
            args.report_map,
            reader.fieldnames,
            {
                "bank",
                "a_code",
                "h_code",
                "report_year",
                "report_period",
                "announcement_date",
                "official_report_url",
            },
        )
        for report in reader:
            if report["bank"] != args.bank:
                continue
            security_code = report.get("a_code") or report.get("h_code")
            candidate = (
                args.research_root
                / "official-reports"
                / args.bank
                / f"{report['report_year']}-{report['report_period']}-{security_code}.pdf"
            )
            location = str(candidate.resolve()) if candidate.exists() else report["official_report_url"]
            rows.append(
                {
                    "kind": "official_report",
                    "status": classify(report["announcement_date"], cutoff, cutoff_has_time),
                    "publication_date": report["announcement_date"] or "unknown",
                    "label": f"{args.bank} {report['report_year']}{report['report_period']}",
                    "path_or_url": location,
                }
            )

    automatic_sealed = [
        args.research_root / "forecast-backtest.csv",
        args.research_root / "forecast-backtest-report.md",
        args.research_root / "forecast-backtest-summary.json",
        Path(__file__).resolve().parent.parent / "references" / "evidence-map.md",
    ]
    for location in automatic_sealed:
        rows.append(
            {
                "kind": "always_sealed",
                "status": "sealed",
                "publication_date": "not_applicable",
                "label": location.name,
                "path_or_url": str(location.resolve()) if location.exists() else str(location),
            }
        )
    for value in args.extra_sealed:
        is_url = "://" in value
        location = Path(value) if not is_url else None
        rows.append(
            {
                "kind": "always_sealed",
                "status": "sealed",
                "publication_date": "not_applicable",
                "label": value.rsplit("/", 1)[-1] or value,
                "path_or_url": (
                    value
                    if is_url
                    else str(location.resolve())
                    if location and location.exists()
                    else value
                ),
            }
        )

    rows.sort(key=lambda row: (row["status"], row["publication_date"], row["kind"], row["label"]))
    result = {
        "bank": args.bank,
        "cutoff": args.cutoff,
        "eligible_count": sum(row["status"] == "eligible" for row in rows),
        "sealed_count": sum(row["status"] != "eligible" for row in rows),
        "items": rows,
        "warning": "Do not open or search sealed items before the forecast is frozen.",
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({key: result[key] for key in ("bank", "cutoff", "eligible_count", "sealed_count")}, ensure_ascii=False))


if __name__ == "__main__":
    main()
