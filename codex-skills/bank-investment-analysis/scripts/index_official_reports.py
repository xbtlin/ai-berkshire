#!/usr/bin/env python3
"""Extract page-level text and topic locations from official bank reports."""

from __future__ import annotations

import argparse
import csv
import json
import re
import unicodedata
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

from pypdf import PdfReader


TOPIC_PATTERNS: dict[str, re.Pattern[str]] = {
    "net_interest_margin": re.compile(r"净利息收入|净息差|平均生息资产|生息资产收益率|计息负债成本率"),
    "non_interest_income": re.compile(r"手续费及佣金|非利息净收入|投资收益|公允价值变动|汇兑损益|汇兑净收益|其他非利息"),
    "asset_quality": re.compile(r"不良贷款|关注类贷款|逾期贷款|贷款迁徙|迁徙率|重组贷款|核销|拨备覆盖率|不良生成"),
    "impairment": re.compile(r"信用减值|资产减值|减值损失|预期信用损失|贷款减值准备"),
    "capital_rwa": re.compile(r"资本充足率|核心一级资本|风险加权资产|RWA|杠杆率"),
    "balance_sheet_mix": re.compile(r"资产负债表|客户贷款|客户存款|金融投资|同业资产|同业负债|贷款和垫款"),
    "segments_subsidiaries": re.compile(r"分部报告|业务分部|地区分部|子公司|附属公司"),
    "accounting_policy": re.compile(r"会计政策|会计估计|会计准则|重分类|列报口径|新金融工具准则"),
    "shareholders": re.compile(r"股东总数|前十名股东|主要股东|沪股通|深股通|香港中央结算"),
}


def load_manifest(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def normalize_page_text(text: str) -> str:
    text = unicodedata.normalize("NFKC", text or "").replace("\xa0", " ")
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    lines = [re.sub(r"[ \t]+", " ", line).strip() for line in text.split("\n")]
    return "\n".join(line for line in lines if line).strip()


def text_destination(row: dict[str, str], output_dir: Path) -> Path:
    directory = output_dir / row["bank"]
    directory.mkdir(parents=True, exist_ok=True)
    return directory / f"{row['report_year']}-{row['report_period']}-{row['a_code']}.txt"


def extract_one(row: dict[str, str], output_dir: Path) -> tuple[dict[str, object], list[dict[str, object]]]:
    pdf_path = Path(row["local_report_path"])
    destination = text_destination(row, output_dir)
    result: dict[str, object] = {
        "bank": row["bank"],
        "a_code": row["a_code"],
        "report_year": row["report_year"],
        "report_period": row["report_period"],
        "pdf_path": str(pdf_path.resolve()),
        "text_path": str(destination.resolve()),
        "page_count": 0,
        "text_chars": 0,
        "median_chars_per_page": 0,
        "ocr_needed": False,
        "status": "",
        "error": "",
    }
    topic_pages: dict[str, list[int]] = defaultdict(list)
    try:
        reader = PdfReader(str(pdf_path), strict=False)
        page_texts: list[str] = []
        page_lengths: list[int] = []
        for page_number, page in enumerate(reader.pages, start=1):
            text = normalize_page_text(page.extract_text() or "")
            page_texts.append(text)
            page_lengths.append(len(text))
            for topic, pattern in TOPIC_PATTERNS.items():
                if pattern.search(text):
                    topic_pages[topic].append(page_number)
        payload: list[str] = []
        for page_number, text in enumerate(page_texts, start=1):
            payload.extend([f"--- PAGE {page_number} ---", text, ""])
        destination.write_text("\n".join(payload).rstrip() + "\n", encoding="utf-8")
        sorted_lengths = sorted(page_lengths)
        median = sorted_lengths[len(sorted_lengths) // 2] if sorted_lengths else 0
        total_chars = sum(page_lengths)
        result.update(
            {
                "page_count": len(page_texts),
                "text_chars": total_chars,
                "median_chars_per_page": median,
                "ocr_needed": bool(page_texts and (median < 80 or total_chars < len(page_texts) * 120)),
                "status": "extracted",
            }
        )
    except Exception as exc:
        result["status"] = "error"
        result["error"] = f"{type(exc).__name__}: {exc}"

    topic_rows = [
        {
            "bank": row["bank"],
            "a_code": row["a_code"],
            "report_year": row["report_year"],
            "report_period": row["report_period"],
            "topic": topic,
            "pages": json.dumps(pages, ensure_ascii=False),
            "page_count": len(pages),
            "text_path": str(destination.resolve()),
        }
        for topic, pages in sorted(topic_pages.items())
    ]
    return result, topic_rows


def write_csv(rows: list[dict[str, object]], path: Path) -> None:
    fields = list(rows[0]) if rows else []
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, required=True, help="Download manifest CSV")
    parser.add_argument("--output-dir", type=Path, required=True, help="Text output root")
    parser.add_argument("--report-index", type=Path, required=True, help="Per-report extraction CSV")
    parser.add_argument("--topic-index", type=Path, required=True, help="Topic/page CSV")
    parser.add_argument("--summary", type=Path, help="Optional JSON summary")
    parser.add_argument("--workers", type=int, default=3)
    args = parser.parse_args()

    rows = [row for row in load_manifest(args.manifest.expanduser().resolve()) if row["status"] != "error"]
    output_dir = args.output_dir.expanduser().resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    reports: list[dict[str, object]] = []
    topics: list[dict[str, object]] = []
    with ThreadPoolExecutor(max_workers=max(1, args.workers)) as executor:
        futures = {executor.submit(extract_one, row, output_dir): row for row in rows}
        for index, future in enumerate(as_completed(futures), start=1):
            report, topic_rows = future.result()
            reports.append(report)
            topics.extend(topic_rows)
            print(
                f"{index}/{len(rows)} {report['status']} {report['bank']} "
                f"{report['report_year']}-{report['report_period']} pages={report['page_count']}",
                flush=True,
            )

    reports.sort(key=lambda row: (str(row["bank"]), str(row["report_year"]), str(row["report_period"])))
    topics.sort(key=lambda row: (str(row["bank"]), str(row["report_year"]), str(row["report_period"]), str(row["topic"])))
    write_csv(reports, args.report_index.expanduser().resolve())
    write_csv(topics, args.topic_index.expanduser().resolve())
    summary = {
        "report_count": len(reports),
        "status_counts": dict(
            (status, sum(report["status"] == status for report in reports))
            for status in sorted({str(report["status"]) for report in reports})
        ),
        "total_pages": sum(int(report["page_count"]) for report in reports),
        "total_text_chars": sum(int(report["text_chars"]) for report in reports),
        "ocr_needed_count": sum(bool(report["ocr_needed"]) for report in reports),
        "topic_index_rows": len(topics),
    }
    if args.summary:
        destination = args.summary.expanduser().resolve()
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    if any(report["status"] == "error" for report in reports):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
