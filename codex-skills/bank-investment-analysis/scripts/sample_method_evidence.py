#!/usr/bin/env python3
"""Select a diverse, reproducible review sample from mined method evidence."""

from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--per-topic", type=int, default=12)
    parser.add_argument("--topics", nargs="*")
    return parser.parse_args()


def year_of(row: dict) -> str:
    value = str(row.get("publish_date", ""))
    return value[:4] if len(value) >= 4 else ""


def priority(row: dict) -> tuple:
    categories = set(row.get("article_categories") or [])
    category_weight = max(
        [
            4 if "earnings_forecast" in categories else 0,
            3 if "earnings_review" in categories else 0,
            2 if "macro_policy" in categories else 0,
            1 if "bank_methodology" in categories else 0,
        ]
    )
    text = row.get("text", "")
    formula_weight = sum(token in text for token in ("=", "计算", "推算", "拆分", "环比", "同比", "口径"))
    return (
        int(row.get("method_score", 0)),
        category_weight,
        formula_weight,
        min(len(text), 800),
    )


def select(rows: list[dict], count: int) -> list[dict]:
    ranked = sorted(rows, key=priority, reverse=True)
    selected: list[dict] = []
    article_counts: defaultdict[str, int] = defaultdict(int)
    bank_counts: defaultdict[str, int] = defaultdict(int)
    year_counts: defaultdict[str, int] = defaultdict(int)

    # First pass maximizes source diversity; later passes relax constraints.
    for article_limit, bank_limit, year_limit in ((1, 3, 3), (2, 5, 5), (99, 99, 99)):
        for row in ranked:
            if row in selected:
                continue
            article = row.get("article_id", "")
            banks = row.get("banks") or ["未归属"]
            bank = banks[0]
            year = year_of(row)
            if article_counts[article] >= article_limit:
                continue
            if bank_counts[bank] >= bank_limit or year_counts[year] >= year_limit:
                continue
            selected.append(row)
            article_counts[article] += 1
            bank_counts[bank] += 1
            year_counts[year] += 1
            if len(selected) >= count:
                return selected
    return selected


def main() -> None:
    args = parse_args()
    grouped: defaultdict[str, list[dict]] = defaultdict(list)
    with args.input.open(encoding="utf-8") as handle:
        for line in handle:
            row = json.loads(line)
            grouped[row["topic"]].append(row)

    topics = args.topics or sorted(grouped)
    lines = [
        "# 方法证据复核样本",
        "",
        "由证据候选集按方法分、文章类型、年份和银行多样性抽样；用于人工复核，不替代原文。",
        "",
    ]
    for topic in topics:
        lines.extend([f"## {topic}", ""])
        for row in select(grouped.get(topic, []), args.per_topic):
            banks = "、".join(row.get("banks") or ["未归属"])
            lines.extend(
                [
                    f"### {row['title']}",
                    "",
                    f"- 日期：{row.get('publish_date', '')}",
                    f"- 银行：{banks}",
                    f"- 方法分：{row.get('method_score', '')}",
                    f"- 原文：{row.get('source_path', '')}",
                    f"- 链接：{row.get('source_url', '')}",
                    "",
                    row.get("text", "").strip(),
                    "",
                ]
            )

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text("\n".join(lines), encoding="utf-8")
    print(json.dumps({"topics": len(topics), "output": str(args.output)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
