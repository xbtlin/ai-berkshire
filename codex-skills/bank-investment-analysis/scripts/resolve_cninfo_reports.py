#!/usr/bin/env python3
"""Resolve official A-share bank reports through CNINFO's disclosure index.

The script reads ``report-map.csv`` from ``build_report_map.py``, queries the
statutory disclosure platform once per bank, caches raw metadata, and writes a
resolved mapping. It does not download PDFs; use the resolved URLs to select a
bounded deep-reading set before downloading large files.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import time
import urllib.parse
import urllib.request
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import Iterable


CNINFO_QUERY_URL = "https://www.cninfo.com.cn/new/hisAnnouncement/query"
CNINFO_TOPSEARCH_URL = "https://www.cninfo.com.cn/new/information/topSearch/query"
CNINFO_PDF_ROOT = "https://static.cninfo.com.cn/"
CATEGORIES = ";".join(
    [
        "category_ndbg_szsh",
        "category_bndbg_szsh",
        "category_yjdbg_szsh",
        "category_sjdbg_szsh",
    ]
)


def org_id(code: str, exchange: str) -> str:
    if exchange == "SSE":
        return f"gssh0{code}"
    if exchange == "SZSE":
        return f"gssz0{code}"
    raise ValueError(f"Unsupported exchange: {exchange}")


def query_params(
    code: str, exchange: str, resolved_org_id: str, page_num: int
) -> dict[str, str]:
    return {
        "pageNum": str(page_num),
        "pageSize": "30",
        "column": "sse" if exchange == "SSE" else "szse",
        "tabName": "fulltext",
        "plate": "sh" if exchange == "SSE" else "sz",
        "stock": f"{code},{resolved_org_id}",
        "searchkey": "",
        "secid": "",
        "category": CATEGORIES,
        "trade": "",
        "seDate": "2017-01-01~2026-12-31",
        "sortName": "",
        "sortType": "",
        "isHLtitle": "true",
    }


def post_json(data: dict[str, str]) -> dict[str, object]:
    request = urllib.request.Request(
        CNINFO_QUERY_URL,
        data=urllib.parse.urlencode(data).encode("utf-8"),
        headers={
            "User-Agent": "Mozilla/5.0 (compatible; bank-research-corpus/1.0)",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Origin": "https://www.cninfo.com.cn",
            "Referer": "https://www.cninfo.com.cn/",
        },
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.loads(response.read().decode("utf-8"))


def lookup_org_id(code: str, exchange: str) -> str:
    url = CNINFO_TOPSEARCH_URL + "?" + urllib.parse.urlencode(
        {"keyWord": code, "maxNum": "10"}
    )
    request = urllib.request.Request(
        url,
        data=b"",
        headers={
            "User-Agent": "Mozilla/5.0 (compatible; bank-research-corpus/1.0)",
            "Referer": "https://www.cninfo.com.cn/",
        },
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        results = json.loads(response.read().decode("utf-8"))
    for item in results:
        if str(item.get("code") or "") == code and item.get("orgId"):
            return str(item["orgId"])
    return org_id(code, exchange)


def fetch_bank_announcements(
    code: str,
    exchange: str,
    cache_path: Path,
    refresh: bool,
) -> list[dict[str, object]]:
    if cache_path.exists() and not refresh:
        cached = json.loads(cache_path.read_text(encoding="utf-8"))
        if cached.get("announcements"):
            return cached["announcements"]

    announcements: list[dict[str, object]] = []
    resolved_org_id = lookup_org_id(code, exchange)
    seen_ids: set[str] = set()
    page_num = 1
    while page_num <= 20:
        payload = post_json(query_params(code, exchange, resolved_org_id, page_num))
        page_items = list(payload.get("announcements") or [])
        new_items = [
            item
            for item in page_items
            if str(item.get("announcementId") or "") not in seen_ids
        ]
        announcements.extend(new_items)
        seen_ids.update(str(item.get("announcementId") or "") for item in new_items)
        total = int(payload.get("totalAnnouncement") or payload.get("totalRecordNum") or 0)
        if (
            not payload.get("hasMore")
            or not page_items
            or not new_items
            or (total and len(announcements) >= total)
        ):
            break
        page_num += 1
        time.sleep(0.15)

    cache_path.parent.mkdir(parents=True, exist_ok=True)
    cache_path.write_text(
        json.dumps(
            {
                "fetched_at": datetime.now().astimezone().isoformat(timespec="seconds"),
                "code": code,
                "exchange": exchange,
                "org_id": resolved_org_id,
                "announcements": announcements,
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    return announcements


def clean_title(title: str) -> str:
    return re.sub(r"<[^>]+>", "", title).replace(" ", "").strip()


def announcement_period(title: str) -> tuple[str, str] | None:
    title = clean_title(title)
    year_match = re.search(r"((?:19|20)\d{2})年?", title)
    if not year_match:
        return None
    year = year_match.group(1)
    if re.search(r"第一季度报告|一季度报告|1季度报告", title):
        return year, "Q1"
    if re.search(r"半年度报告|中期报告", title):
        return year, "H1"
    if re.search(r"第三季度报告|三季度报告|3季度报告", title):
        return year, "Q3"
    if re.search(r"年度报告|年报", title):
        return year, "FY"
    return None


def usable_full_report(announcement: dict[str, object]) -> bool:
    title = clean_title(str(announcement.get("announcementTitle") or ""))
    if not announcement_period(title):
        return False
    excluded = (
        "摘要",
        "英文",
        "取消",
        "关于",
        "审计报告",
        "财务报表及审计报告",
    )
    return not any(word in title for word in excluded)


def announcement_url(announcement: dict[str, object]) -> str:
    adjunct = str(announcement.get("adjunctUrl") or "").lstrip("/")
    return urllib.parse.urljoin(CNINFO_PDF_ROOT, adjunct)


def timestamp_to_date(value: object) -> str:
    try:
        return datetime.fromtimestamp(int(value) / 1000).astimezone().date().isoformat()
    except (TypeError, ValueError, OSError):
        return ""


def choose_primary(candidates: list[dict[str, object]]) -> dict[str, object] | None:
    if not candidates:
        return None

    def rank(item: dict[str, object]) -> tuple[int, int, int, int]:
        title = clean_title(str(item.get("announcementTitle") or ""))
        is_h_share = int("H股" in title)
        is_revision = int(any(word in title for word in ("修订", "更正", "更新")))
        timestamp = int(item.get("announcementTime") or 0)
        return is_h_share, is_revision, timestamp, len(title)

    return sorted(candidates, key=rank)[0]


def load_csv(path: Path) -> tuple[list[dict[str, str]], list[str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        return list(reader), list(reader.fieldnames or [])


def write_csv(rows: list[dict[str, str]], fields: list[str], path: Path) -> None:
    extra_fields = [
        "announcement_id",
        "announcement_title",
        "announcement_date",
        "announcement_size_kb",
        "alternate_report_urls",
    ]
    output_fields = list(dict.fromkeys(fields + extra_fields))
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=output_fields)
        writer.writeheader()
        writer.writerows(rows)


def index_announcements(
    rows: list[dict[str, str]], cache_dir: Path, refresh: bool
) -> dict[tuple[str, str, str], list[dict[str, object]]]:
    securities = sorted({(row["a_code"], row["exchange"]) for row in rows})
    index: dict[tuple[str, str, str], list[dict[str, object]]] = defaultdict(list)
    for position, (code, exchange) in enumerate(securities, start=1):
        cache_path = cache_dir / f"{code}.json"
        announcements = fetch_bank_announcements(code, exchange, cache_path, refresh)
        for announcement in announcements:
            if not usable_full_report(announcement):
                continue
            period = announcement_period(str(announcement.get("announcementTitle") or ""))
            if period:
                index[(code, period[0], period[1])].append(announcement)
        print(f"Resolved metadata {position}/{len(securities)}: {code}")
        if position < len(securities) and (refresh or not cache_path.exists()):
            time.sleep(0.15)
    return index


def resolve_rows(
    rows: list[dict[str, str]],
    index: dict[tuple[str, str, str], list[dict[str, object]]],
) -> list[dict[str, str]]:
    for row in rows:
        key = (row["a_code"], row["report_year"], row["report_period"])
        candidates = index.get(key, [])
        primary = choose_primary(candidates)
        if not primary:
            row["source_status"] = "missing"
            row["source_notes"] = "CNINFO metadata query returned no exact full-report match"
            continue
        primary_url = announcement_url(primary)
        row["official_report_url"] = primary_url
        row["source_status"] = "resolved"
        row["announcement_id"] = str(primary.get("announcementId") or "")
        row["announcement_title"] = clean_title(str(primary.get("announcementTitle") or ""))
        row["announcement_date"] = timestamp_to_date(primary.get("announcementTime"))
        row["announcement_size_kb"] = str(primary.get("adjunctSize") or "")
        alternates = [announcement_url(item) for item in candidates if announcement_url(item) != primary_url]
        row["alternate_report_urls"] = json.dumps(alternates, ensure_ascii=False)
        if alternates:
            row["source_notes"] = "Alternate or revised full-report disclosures retained in alternate_report_urls"
    return rows


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--map", type=Path, required=True, help="Input report-map.csv")
    parser.add_argument("--output", type=Path, required=True, help="Resolved CSV destination")
    parser.add_argument("--cache-dir", type=Path, required=True, help="Directory for raw CNINFO JSON")
    parser.add_argument("--refresh", action="store_true", help="Ignore cached metadata")
    parser.add_argument("--summary", type=Path, help="Optional JSON summary")
    args = parser.parse_args()

    rows, fields = load_csv(args.map.expanduser().resolve())
    cache_dir = args.cache_dir.expanduser().resolve()
    index = index_announcements(rows, cache_dir, args.refresh)
    resolved = resolve_rows(rows, index)
    output = args.output.expanduser().resolve()
    write_csv(resolved, fields, output)

    status_counts: dict[str, int] = defaultdict(int)
    for row in resolved:
        status_counts[row["source_status"]] += 1
    summary = {
        "bank_period_count": len(resolved),
        "source_status": dict(status_counts),
        "resolved_ratio": round(status_counts.get("resolved", 0) / len(resolved), 4) if resolved else 0,
        "cache_file_count": len(list(cache_dir.glob("*.json"))),
    }
    if args.summary:
        summary_path = args.summary.expanduser().resolve()
        summary_path.parent.mkdir(parents=True, exist_ok=True)
        summary_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
