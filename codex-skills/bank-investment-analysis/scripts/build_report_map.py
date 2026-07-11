#!/usr/bin/env python3
"""Build article-to-bank-report mapping requests from an extracted corpus."""

from __future__ import annotations

import argparse
import csv
import json
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Security:
    a_code: str
    exchange: str
    h_code: str = ""
    ir_url: str = ""


BANK_SECURITIES: dict[str, Security] = {
    "招商银行": Security("600036", "SSE", "03968", "https://www.cmbchina.com/cmbir/"),
    "建设银行": Security("601939", "SSE", "00939", "http://www.ccb.com/cn/investor/"),
    "工商银行": Security("601398", "SSE", "01398", "https://www.icbc-ltd.com/"),
    "农业银行": Security("601288", "SSE", "01288", "https://www.abchina.com/cn/AboutABC/Investor_Relations/"),
    "中国银行": Security("601988", "SSE", "03988", "https://www.boc.cn/investor/"),
    "交通银行": Security("601328", "SSE", "03328", "https://www.bankcomm.com/BankCommSite/shtml/jyjr/cn/7800/list.shtml"),
    "邮储银行": Security("601658", "SSE", "01658", "https://www.psbc.com/cn/tzzgx/"),
    "平安银行": Security("000001", "SZSE", "", "https://bank.pingan.com/about/investor.shtml"),
    "兴业银行": Security("601166", "SSE", "", "https://www.cib.com.cn/cn/aboutCIB/investor/"),
    "浦发银行": Security("600000", "SSE", "", "https://www.spdb.com.cn/about/investor/"),
    "民生银行": Security("600016", "SSE", "01988", "https://www.cmbc.com.cn/tzzgx/"),
    "中信银行": Security("601998", "SSE", "00998", "https://www.citicbank.com/about/investor/"),
    "光大银行": Security("601818", "SSE", "06818", "https://www.cebbank.com/site/gryw/tzzgx/index.html"),
    "华夏银行": Security("600015", "SSE", "", "https://www.hxb.com.cn/jrhx/tzzgx/"),
    "浙商银行": Security("601916", "SSE", "02016", "https://www.czbank.com/cn/investor/"),
    "宁波银行": Security("002142", "SZSE", "", "https://www.nbcb.com.cn/tzzgx/"),
    "江苏银行": Security("600919", "SSE", "", "https://www.jsbchina.cn/CN/tzzgx/"),
    "南京银行": Security("601009", "SSE", "", "https://www.njcb.com.cn/njcb/tzzgx/index.html"),
    "杭州银行": Security("600926", "SSE", "", "https://www.hzbank.com.cn/hzyh/tzzgx/index.html"),
    "成都银行": Security("601838", "SSE", "", "https://www.bocd.com.cn/tzzgx/"),
    "上海银行": Security("601229", "SSE", "", "https://www.bosc.cn/zh/investor/"),
    "苏州银行": Security("002966", "SZSE", "", "https://www.suzhoubank.com/tzzgx/"),
    "北京银行": Security("601169", "SSE", "", "https://www.bankofbeijing.com.cn/tzzgx/"),
    "江阴银行": Security("002807", "SZSE", "", "https://www.jybank.com.cn/tzzgx/"),
    "常熟银行": Security("601128", "SSE", "", "https://www.csrcbank.com/tzzgx/"),
    "无锡银行": Security("600908", "SSE", "", "https://www.wrcb.com.cn/tzzgx/"),
    "张家港行": Security("002839", "SZSE", "", "https://www.zrcbank.com/tzzgx/"),
    "长沙银行": Security("601577", "SSE", "", "https://www.bankofchangsha.com/tzzgx/"),
    "厦门银行": Security("601187", "SSE", "", "https://www.xmbankonline.com/tzzgx/"),
}


PERIOD_LABEL = {
    "Q1": "第一季度报告",
    "H1": "半年度报告",
    "Q3": "第三季度报告",
    "FY": "年度报告",
}


def prior_periods(year: int, period: str) -> list[dict[str, str]]:
    if period == "Q1":
        return [{"year": str(year - 1), "period": "FY"}]
    if period == "H1":
        return [
            {"year": str(year), "period": "Q1"},
            {"year": str(year - 1), "period": "FY"},
        ]
    if period == "Q3":
        return [
            {"year": str(year), "period": "H1"},
            {"year": str(year - 1), "period": "Q3"},
        ]
    if period == "FY":
        return [
            {"year": str(year), "period": "Q3"},
            {"year": str(year - 1), "period": "FY"},
        ]
    return []


def load_jsonl(path: Path) -> list[dict[str, object]]:
    records: list[dict[str, object]] = []
    with path.open(encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                records.append(json.loads(line))
    return records


def build_groups(records: list[dict[str, object]]) -> dict[tuple[str, str, str], list[dict[str, object]]]:
    groups: dict[tuple[str, str, str], list[dict[str, object]]] = defaultdict(list)
    relevant = {"earnings_forecast", "earnings_review", "cross_bank_comparison"}
    for record in records:
        categories = set(record.get("categories") or [])
        year = str(record.get("report_year") or "")
        period = str(record.get("report_period") or "")
        banks = list(record.get("banks") or [])
        if not relevant.intersection(categories) or not year or not period or not banks:
            continue
        for bank in banks:
            groups[(str(bank), year, period)].append(record)
    return groups


def group_row(key: tuple[str, str, str], articles: list[dict[str, object]]) -> dict[str, object]:
    bank, year, period = key
    security = BANK_SECURITIES.get(bank, Security("", ""))
    dates = sorted(str(article.get("publish_date") or "") for article in articles if article.get("publish_date"))
    forecasts = [article for article in articles if "earnings_forecast" in set(article.get("categories") or [])]
    reviews = [article for article in articles if "earnings_review" in set(article.get("categories") or [])]
    comparisons = [article for article in articles if "cross_bank_comparison" in set(article.get("categories") or [])]
    report_label = PERIOD_LABEL.get(period, period)
    return {
        "bank": bank,
        "a_code": security.a_code,
        "exchange": security.exchange,
        "h_code": security.h_code,
        "report_year": year,
        "report_period": period,
        "report_label": report_label,
        "article_count": len(articles),
        "full_forecast_count": sum(article.get("availability") == "full" for article in forecasts),
        "paid_forecast_count": sum(article.get("availability") == "paid_preview" for article in forecasts),
        "full_review_count": sum(article.get("availability") == "full" for article in reviews),
        "comparison_count": len(comparisons),
        "first_article_date": dates[0] if dates else "",
        "last_article_date": dates[-1] if dates else "",
        "earliest_forecast_date": min(
            (str(article.get("publish_date") or "") for article in forecasts if article.get("publish_date")),
            default="",
        ),
        "article_ids": json.dumps([article["article_id"] for article in articles], ensure_ascii=False),
        "article_titles": json.dumps([article["title"] for article in articles], ensure_ascii=False),
        "prior_input_periods": json.dumps(prior_periods(int(year), period), ensure_ascii=False),
        "official_search_query": f"{bank} {year}年 {report_label} PDF",
        "ir_url": security.ir_url,
        "official_report_url": "",
        "local_report_path": "",
        "source_status": "missing",
        "source_notes": "",
    }


def write_csv(rows: list[dict[str, object]], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = list(rows[0]) if rows else []
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--articles", type=Path, required=True, help="articles.jsonl from extract_bank_articles.py")
    parser.add_argument("--output", type=Path, required=True, help="Destination CSV")
    parser.add_argument("--summary", type=Path, help="Optional JSON summary path")
    args = parser.parse_args()

    records = load_jsonl(args.articles.expanduser().resolve())
    groups = build_groups(records)
    rows = [group_row(key, groups[key]) for key in sorted(groups)]
    write_csv(rows, args.output.expanduser().resolve())

    summary = {
        "mapped_article_count": len({article["article_id"] for articles in groups.values() for article in articles}),
        "bank_period_count": len(rows),
        "bank_count": len({row["bank"] for row in rows}),
        "full_forecast_count": sum(int(row["full_forecast_count"]) for row in rows),
        "paid_forecast_count": sum(int(row["paid_forecast_count"]) for row in rows),
        "full_review_count": sum(int(row["full_review_count"]) for row in rows),
        "missing_security_metadata": sorted({str(row["bank"]) for row in rows if not row["a_code"]}),
    }
    if args.summary:
        destination = args.summary.expanduser().resolve()
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
