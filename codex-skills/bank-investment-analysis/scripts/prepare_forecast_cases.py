#!/usr/bin/env python3
"""Prepare forecast/article/actual evidence bundles for manual backtesting."""

from __future__ import annotations

import argparse
import csv
import json
import re
from pathlib import Path


FORECAST_CUE = re.compile(r"预测|评估|中性|乐观|悲观|高概率|区间|范围|上下限|估算|预估")
METRIC_CUE = re.compile(
    r"净利润|营收|营业收入|净利息收入|净息差|资产增速|手续费|非息收入|"
    r"信用减值|减值损失|所得税率|成本收入比"
)
ACTUAL_CUE = re.compile(r"归属于.{0,12}净利润|归母净利润|营业收入|净利息收入")


def load_jsonl(path: Path) -> list[dict[str, object]]:
    with path.open(encoding="utf-8") as handle:
        return [json.loads(line) for line in handle if line.strip()]


def load_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def paragraphs(text: str) -> list[str]:
    items = [re.sub(r"\s+", " ", item).strip() for item in re.split(r"\n\s*\n|\n", text)]
    return [item for item in items if len(item) >= 20]


def forecast_snippets(body: str) -> list[str]:
    candidates: list[tuple[int, int, str]] = []
    for position, paragraph in enumerate(paragraphs(body)):
        if not METRIC_CUE.search(paragraph):
            continue
        score = int(bool(FORECAST_CUE.search(paragraph))) * 3
        score += int(bool(re.search(r"\d+(?:\.\d+)?%|bps|BP|±|~|=", paragraph, re.IGNORECASE))) * 2
        score += int(bool(re.search(r"取决于|主要是|根据|所以|因此|考虑", paragraph)))
        if score >= 3:
            candidates.append((score, position, paragraph))
    candidates.sort(key=lambda item: (-item[0], item[1]))
    return [item[2] for item in candidates[:35]]


def review_snippets(reviews: list[dict[str, object]]) -> list[dict[str, str]]:
    results: list[dict[str, str]] = []
    for review in reviews:
        for paragraph in paragraphs(str(review.get("body") or "")):
            if ACTUAL_CUE.search(paragraph) and re.search(r"同比|环比|增长|下降|增速", paragraph):
                results.append(
                    {
                        "article_id": str(review["article_id"]),
                        "title": str(review["title"]),
                        "text": paragraph,
                    }
                )
                if len(results) >= 25:
                    return results
    return results


def split_pages(text: str) -> list[tuple[int, str]]:
    matches = list(re.finditer(r"^--- PAGE (\d+) ---$", text, re.MULTILINE))
    pages: list[tuple[int, str]] = []
    for index, match in enumerate(matches):
        start = match.end()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        pages.append((int(match.group(1)), text[start:end].strip()))
    return pages


def context_snippets(text: str, pattern: re.Pattern[str], limit: int = 12) -> list[dict[str, object]]:
    results: list[dict[str, object]] = []
    for page_number, page_text in split_pages(text):
        for match in pattern.finditer(page_text):
            start = max(0, match.start() - 260)
            end = min(len(page_text), match.end() + 700)
            snippet = re.sub(r"\s+", " ", page_text[start:end]).strip()
            if snippet:
                results.append({"page": page_number, "text": snippet})
            if len(results) >= limit:
                return results
    return results


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--articles", type=Path, required=True)
    parser.add_argument("--report-text-index", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--case-dir", type=Path, required=True)
    parser.add_argument("--summary", type=Path, required=True)
    args = parser.parse_args()

    articles = load_jsonl(args.articles.expanduser().resolve())
    report_rows = load_csv(args.report_text_index.expanduser().resolve())
    report_index = {
        (row["bank"], row["report_year"], row["report_period"]): row for row in report_rows
    }
    reviews_by_key: dict[tuple[str, str, str], list[dict[str, object]]] = {}
    for article in articles:
        if article.get("availability") != "full" or "earnings_review" not in set(article.get("categories") or []):
            continue
        for bank in article.get("banks") or []:
            key = (str(bank), str(article.get("report_year") or ""), str(article.get("report_period") or ""))
            reviews_by_key.setdefault(key, []).append(article)

    cases: list[dict[str, object]] = []
    case_dir = args.case_dir.expanduser().resolve()
    case_dir.mkdir(parents=True, exist_ok=True)
    for article in articles:
        if not (
            article.get("availability") == "full"
            and "earnings_forecast" in set(article.get("categories") or [])
        ):
            continue
        banks = list(article.get("banks") or [])
        if len(banks) != 1:
            continue
        key = (
            str(banks[0]),
            str(article.get("report_year") or ""),
            str(article.get("report_period") or ""),
        )
        report = report_index.get(key)
        official_snippets: list[dict[str, object]] = []
        if report and Path(report["text_path"]).exists():
            report_text = Path(report["text_path"]).read_text(encoding="utf-8")
            official_snippets = context_snippets(report_text, ACTUAL_CUE)
        case = {
            "case_id": str(article["article_id"]),
            "bank": key[0],
            "report_year": key[1],
            "report_period": key[2],
            "forecast_article_id": article["article_id"],
            "forecast_title": article["title"],
            "forecast_publish_date": article["publish_date"],
            "forecast_source_path": article["source_path"],
            "forecast_source_url": article["source_url"],
            "forecast_snippets": forecast_snippets(str(article.get("body") or "")),
            "paired_review_snippets": review_snippets(reviews_by_key.get(key, [])),
            "official_report_path": report.get("pdf_path", "") if report else "",
            "official_report_text_path": report.get("text_path", "") if report else "",
            "official_actual_snippets": official_snippets,
        }
        cases.append(case)

        lines = [
            f"# {case['forecast_title']}",
            "",
            f"- 银行: {case['bank']}",
            f"- 报告期: {case['report_year']} {case['report_period']}",
            f"- 预测文章日期: {case['forecast_publish_date']}",
            f"- 预测文章: {case['forecast_source_path']}",
            f"- 官方财报: {case['official_report_path']}",
            "",
            "## 预测文章中的高信号段落",
            "",
        ]
        lines.extend(f"- {snippet}" for snippet in case["forecast_snippets"])
        lines.extend(["", "## 后续点评中的实际结果候选", ""])
        lines.extend(
            f"- [{item['title']}] {item['text']}" for item in case["paired_review_snippets"]
        )
        lines.extend(["", "## 官方财报实际结果候选", ""])
        lines.extend(
            f"- 第{item['page']}页: {item['text']}" for item in case["official_actual_snippets"]
        )
        (case_dir / f"{case['case_id']}.md").write_text(
            "\n".join(lines).rstrip() + "\n", encoding="utf-8"
        )

    cases.sort(key=lambda item: (str(item["bank"]), str(item["report_year"]), str(item["report_period"]), str(item["forecast_publish_date"])))
    output = args.output.expanduser().resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", encoding="utf-8") as handle:
        for case in cases:
            handle.write(json.dumps(case, ensure_ascii=False) + "\n")
    summary = {
        "case_count": len(cases),
        "bank_counts": {
            bank: sum(case["bank"] == bank for case in cases)
            for bank in sorted({str(case["bank"]) for case in cases})
        },
        "case_with_official_report": sum(bool(case["official_report_path"]) for case in cases),
        "case_with_review_actual": sum(bool(case["paired_review_snippets"]) for case in cases),
        "case_with_official_actual_snippet": sum(bool(case["official_actual_snippets"]) for case in cases),
    }
    summary_path = args.summary.expanduser().resolve()
    summary_path.parent.mkdir(parents=True, exist_ok=True)
    summary_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
