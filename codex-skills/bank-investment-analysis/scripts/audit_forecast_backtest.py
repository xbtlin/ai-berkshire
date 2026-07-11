#!/usr/bin/env python3
"""Audit forecast backtest dates, look-ahead boundaries, files, and intervals."""

from __future__ import annotations

import argparse
import csv
import json
from decimal import Decimal
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--backtest", type=Path, required=True)
    parser.add_argument("--articles", type=Path, required=True)
    parser.add_argument("--report-map", type=Path, required=True)
    parser.add_argument("--research-root", type=Path, required=True)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    article_dates: dict[str, str] = {}
    with args.articles.open(encoding="utf-8") as handle:
        for line in handle:
            row = json.loads(line)
            article_dates[row["article_id"]] = row["publish_date"][:10]

    report_dates: dict[tuple[str, str, str], str] = {}
    with args.report_map.open(encoding="utf-8-sig") as handle:
        for row in csv.DictReader(handle):
            report_dates[(row["bank"], row["report_year"], row["report_period"])] = row[
                "announcement_date"
            ]

    errors: list[dict] = []
    count = 0
    with args.backtest.open(encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            count += 1
            label = f"{row['bank']} {row['report_year']}{row['report_period']}"
            ids = row["forecast_article_ids"].split("|")
            missing_ids = [article_id for article_id in ids if article_id not in article_dates]
            if missing_ids:
                errors.append({"case": label, "type": "missing_article", "detail": missing_ids})
                continue

            expected_date = max(article_dates[article_id] for article_id in ids)
            if row["forecast_date"] != expected_date:
                errors.append(
                    {
                        "case": label,
                        "type": "forecast_date_mismatch",
                        "detail": [row["forecast_date"], expected_date],
                    }
                )

            key = (row["bank"], row["report_year"], row["report_period"])
            announcement_date = report_dates.get(key)
            if not announcement_date:
                errors.append({"case": label, "type": "missing_report_map", "detail": key})
            elif row["forecast_date"] >= announcement_date:
                errors.append(
                    {
                        "case": label,
                        "type": "lookahead",
                        "detail": [row["forecast_date"], announcement_date],
                    }
                )

            source = args.research_root / row["actual_source"]
            if not source.exists():
                errors.append({"case": label, "type": "missing_actual_source", "detail": str(source)})

            if row["forecast_low_pct"] and row["forecast_high_pct"]:
                low = Decimal(row["forecast_low_pct"])
                center = Decimal(row["forecast_center_pct"])
                high = Decimal(row["forecast_high_pct"])
                if not low <= center <= high:
                    errors.append(
                        {
                            "case": label,
                            "type": "invalid_interval",
                            "detail": [str(low), str(center), str(high)],
                        }
                    )

    result = {"case_count": count, "error_count": len(errors), "errors": errors}
    print(json.dumps(result, ensure_ascii=False, indent=2))
    raise SystemExit(1 if errors else 0)


if __name__ == "__main__":
    main()
