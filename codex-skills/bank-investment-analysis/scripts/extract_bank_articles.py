#!/usr/bin/env python3
"""Extract and index the bank-expert DOCX article corpus.

The source DOCX files store WeChat HTML inside ``word/afchunk.mht`` rather
than ordinary Word paragraphs. This script parses that MHT payload, preserves
source provenance and figure URLs, removes obvious promotional tails, assigns
lightweight bank/report-period labels, and writes reproducible research files.

Only Python's standard library is required.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import statistics
import sys
import unicodedata
import zipfile
from collections import Counter
from dataclasses import dataclass, field
from datetime import datetime
from email import policy
from email.parser import BytesParser
from html.parser import HTMLParser
from pathlib import Path
from typing import Iterable


BLOCK_TAGS = {
    "address",
    "article",
    "aside",
    "blockquote",
    "br",
    "div",
    "figcaption",
    "figure",
    "h1",
    "h2",
    "h3",
    "h4",
    "h5",
    "h6",
    "hr",
    "li",
    "p",
    "section",
    "table",
    "td",
    "th",
    "tr",
}
SKIP_TAGS = {"script", "style", "button", "svg"}


@dataclass
class Node:
    tag: str
    attrs: dict[str, str] = field(default_factory=dict)
    children: list["Node | str"] = field(default_factory=list)
    parent: "Node | None" = None

    @property
    def classes(self) -> set[str]:
        return set(self.attrs.get("class", "").split())


class MiniDOMParser(HTMLParser):
    """Build a small permissive DOM sufficient for the archived WeChat HTML."""

    VOID_TAGS = {
        "area",
        "base",
        "br",
        "col",
        "embed",
        "hr",
        "img",
        "input",
        "link",
        "meta",
        "param",
        "source",
        "track",
        "wbr",
    }

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.root = Node("document")
        self.stack = [self.root]

    def handle_starttag(
        self, tag: str, attrs: list[tuple[str, str | None]]
    ) -> None:
        node = Node(
            tag=tag.lower(),
            attrs={key.lower(): value or "" for key, value in attrs},
            parent=self.stack[-1],
        )
        self.stack[-1].children.append(node)
        if tag.lower() not in self.VOID_TAGS:
            self.stack.append(node)

    def handle_startendtag(
        self, tag: str, attrs: list[tuple[str, str | None]]
    ) -> None:
        self.handle_starttag(tag, attrs)
        if self.stack[-1].tag == tag.lower():
            self.stack.pop()

    def handle_endtag(self, tag: str) -> None:
        tag = tag.lower()
        for index in range(len(self.stack) - 1, 0, -1):
            if self.stack[index].tag == tag:
                del self.stack[index:]
                return

    def handle_data(self, data: str) -> None:
        if data:
            self.stack[-1].children.append(data)


BANK_ALIASES: list[tuple[str, tuple[str, ...]]] = [
    ("招商银行", ("招商银行", "招行")),
    ("建设银行", ("建设银行", "建行")),
    ("工商银行", ("工商银行", "工行")),
    ("农业银行", ("农业银行", "农行")),
    ("中国银行", ("中国银行", "中行")),
    ("交通银行", ("交通银行", "交行")),
    ("邮储银行", ("邮储银行", "邮储")),
    ("平安银行", ("平安银行",)),
    ("兴业银行", ("兴业银行",)),
    ("浦发银行", ("浦发银行", "浦发")),
    ("民生银行", ("民生银行",)),
    ("中信银行", ("中信银行",)),
    ("光大银行", ("光大银行",)),
    ("华夏银行", ("华夏银行",)),
    ("广发银行", ("广发银行",)),
    ("浙商银行", ("浙商银行",)),
    ("渤海银行", ("渤海银行",)),
    ("宁波银行", ("宁波银行",)),
    ("江苏银行", ("江苏银行",)),
    ("南京银行", ("南京银行",)),
    ("杭州银行", ("杭州银行",)),
    ("成都银行", ("成都银行",)),
    ("长沙银行", ("长沙银行",)),
    ("重庆银行", ("重庆银行",)),
    ("贵阳银行", ("贵阳银行",)),
    ("北京银行", ("北京银行",)),
    ("上海银行", ("上海银行",)),
    ("齐鲁银行", ("齐鲁银行",)),
    ("苏州银行", ("苏州银行",)),
    ("青岛银行", ("青岛银行",)),
    ("厦门银行", ("厦门银行",)),
    ("兰州银行", ("兰州银行",)),
    ("常熟银行", ("常熟银行",)),
    ("江阴银行", ("江阴银行",)),
    ("苏农银行", ("苏农银行",)),
    ("无锡银行", ("无锡银行",)),
    ("张家港行", ("张家港行",)),
    ("瑞丰银行", ("瑞丰银行",)),
]


CATEGORY_PATTERNS: list[tuple[str, re.Pattern[str]]] = [
    (
        "cross_bank_comparison",
        re.compile(r"横向对比|横评|大比武|哪家强|银行中报收官|银行年报收官"),
    ),
    (
        "macro_policy",
        re.compile(
            r"宏观|经济|金融数据|货币|LPR|降息|降准|通胀|社融|M1|M2|"
            r"PMI|GDP|国债|同业存单|央行|金融工作会议"
        ),
    ),
    (
        "bank_methodology",
        re.compile(
            r"我眼中的银行|财报大侦探|资产负债|净息差|信用风险|RORWA|"
            r"巴塞尔|读书笔记|银行估值|不良生成|信用减值|资本充足"
        ),
    ),
    ("investment_philosophy", re.compile(r"投资中|投资中的|价值投资|股市|市场|牛市|熊市")),
]


PROMO_MARKERS = (
    "点击文末的“阅读原文”",
    "点击文末的“ 阅读原文 ”",
    "点击文末的阅读原文",
    "粉丝福利子菜单",
    "低佣开户",
    "超低佣金",
    "佣金高",
    "量化T0机器人",
    "量化 T0机器人",
    "7*24小时开户",
)


def walk(node: Node) -> Iterable[Node]:
    yield node
    for child in node.children:
        if isinstance(child, Node):
            yield from walk(child)


def find_by_class(root: Node, class_name: str) -> list[Node]:
    return [node for node in walk(root) if class_name in node.classes]


def node_text(node: Node, *, skip_classes: set[str] | None = None) -> str:
    skip_classes = skip_classes or set()
    parts: list[str] = []

    def collect(current: Node | str) -> None:
        if isinstance(current, str):
            parts.append(current)
            return
        if current.tag in SKIP_TAGS or current.classes.intersection(skip_classes):
            return
        if current.tag in BLOCK_TAGS:
            parts.append("\n")
        for child in current.children:
            collect(child)
        if current.tag in BLOCK_TAGS:
            parts.append("\n")

    collect(node)
    return normalize_text("".join(parts))


def normalize_text(text: str) -> str:
    text = unicodedata.normalize("NFKC", text).replace("\xa0", " ")
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    lines = [re.sub(r"[ \t]+", " ", line).strip() for line in text.split("\n")]
    compact: list[str] = []
    for line in lines:
        if not line:
            if compact and compact[-1] != "":
                compact.append("")
            continue
        compact.append(line)
    return "\n".join(compact).strip()


def clean_promotional_tail(text: str) -> tuple[str, str]:
    """Split an obvious promotional footer without deleting analytical prose."""
    lines = text.splitlines()
    candidates: list[int] = []
    for index, line in enumerate(lines):
        normalized = line.replace(" ", "")
        if re.fullmatch(r"[-—_·.]{6,}", normalized):
            tail = "\n".join(lines[index + 1 :])
            if any(marker.replace(" ", "") in tail.replace(" ", "") for marker in PROMO_MARKERS):
                candidates.append(index)
    if candidates:
        cut = candidates[-1]
        return "\n".join(lines[:cut]).strip(), "\n".join(lines[cut + 1 :]).strip()

    # Some exports omitted the separator. Only cut late-occurring, unmistakable promos.
    cutoff = int(len(text) * 0.72)
    positions = [text.find(marker, cutoff) for marker in PROMO_MARKERS]
    positions = [position for position in positions if position >= 0]
    if positions:
        cut = min(positions)
        return text[:cut].strip(), text[cut:].strip()
    return text.strip(), ""


def extract_html_from_mht(raw: bytes) -> str:
    message = BytesParser(policy=policy.default).parsebytes(raw)
    for part in message.walk():
        if part.get_content_type() != "text/html":
            continue
        try:
            content = part.get_content()
            if isinstance(content, str):
                return content
        except (LookupError, UnicodeDecodeError):
            pass
        payload = part.get_payload(decode=True) or b""
        charset = part.get_content_charset() or "utf-8"
        return payload.decode(charset, errors="replace")
    raise ValueError("MHT payload has no text/html part")


def first_text(nodes: list[Node]) -> str:
    return node_text(nodes[0]).replace("\n", " ").strip() if nodes else ""


def first_tag_text(root: Node, tag: str) -> str:
    nodes = [node for node in walk(root) if node.tag == tag]
    return first_text(nodes)


def canonical_url(root: Node) -> str:
    for node in walk(root):
        if node.tag == "a":
            url = node.attrs.get("href", "")
            if "mp.weixin.qq.com/" in url:
                return url
    return ""


def body_images(nodes: list[Node]) -> list[str]:
    urls: list[str] = []
    for body in nodes:
        for node in walk(body):
            if node.tag != "img":
                continue
            src = node.attrs.get("data-src") or node.attrs.get("src", "")
            if src and not src.startswith("data:image/svg"):
                urls.append(src)
    return list(dict.fromkeys(urls))


def emphasized_text(nodes: list[Node]) -> list[str]:
    results: list[str] = []
    for body in nodes:
        for node in walk(body):
            style = node.attrs.get("style", "").lower().replace(" ", "")
            is_emphasis = (
                node.tag in {"b", "strong"}
                or "font-weight:bold" in style
                or "font-weight:700" in style
                or "color:rgb(255,0,0)" in style
                or "color:rgb(0,82,255)" in style
            )
            if not is_emphasis:
                continue
            text = node_text(node).replace("\n", " ").strip()
            if 4 <= len(text) <= 500:
                results.append(text)
    return list(dict.fromkeys(results))


def identify_banks(title: str, body: str, *, full_scan: bool = False) -> list[str]:
    banks: list[str] = []
    title_matches: list[str] = []
    for bank, aliases in BANK_ALIASES:
        if any(alias in title for alias in aliases):
            title_matches.append(bank)
    if title_matches and not full_scan:
        return title_matches

    probe = body if full_scan else body[:800]
    for bank, aliases in BANK_ALIASES:
        threshold = 1 if full_scan else 2
        if sum(probe.count(alias) for alias in aliases) >= threshold:
            banks.append(bank)
    return list(dict.fromkeys(title_matches + banks))


def infer_report_period(
    title: str, publish_date: str, categories: list[str], banks: list[str]
) -> tuple[str, str]:
    is_bank_reporting = bool(
        banks
        or {"earnings_forecast", "earnings_review", "cross_bank_comparison"}.intersection(
            categories
        )
    ) and bool(
        re.search(
            r"财报|年报|季报|中报|半年报|半年度|季度|业绩快报|全年业绩|业绩预测",
            title,
        )
    )
    if not is_bank_reporting:
        return "", ""

    years = re.findall(r"(?:19|20)\d{2}", title)
    report_year = years[0] if years else ""

    if re.search(r"一季报|1季报|第一季度|一季度|1季度|Q1", title, re.IGNORECASE):
        period = "Q1"
    elif re.search(r"中报|半年报|半年度|上半年|H1", title, re.IGNORECASE):
        period = "H1"
    elif re.search(r"三季报|3季报|第三季度|前三季度|3季度|Q3", title, re.IGNORECASE):
        period = "Q3"
    elif re.search(r"年报|全年|年度业绩|业绩快报|业绩预测", title):
        period = "FY"
    else:
        period = ""

    if not report_year and period and re.match(r"(?:19|20)\d{2}", publish_date):
        publish_year = int(publish_date[:4])
        report_year = str(publish_year - 1 if period == "FY" and publish_date[5:7] in {"01", "02", "03", "04"} else publish_year)
    return report_year, period


def classify(title: str, banks: list[str]) -> list[str]:
    """Assign conservative title-led categories.

    Body text is intentionally excluded here. Common banking words such as
    "预测", "宏观", and "市场" occur in many otherwise unrelated articles and
    caused inflated labels in the exploratory pass. Full text remains
    available for retrieval and evidence coding.
    """
    categories: list[str] = []
    if re.search(r"预测|展望和预测", title):
        categories.append("earnings_forecast")

    report_context = bool(
        re.search(
            r"财报|年报|季报|中报|半年报|半年度|季度|业绩快报|全年业绩|业绩预测",
            title,
        )
    )
    macro_document = bool(re.search(r"货币执行报告|金融数据|经济数据|宏观数据", title))
    if (
        (re.search(r"点评|解析|精读|复盘|收官", title) or "业绩快报" in title)
        and (banks or report_context)
        and not macro_document
    ):
        categories.append("earnings_review")

    categories.extend(
        name for name, pattern in CATEGORY_PATTERNS if pattern.search(title)
    )
    categories = list(dict.fromkeys(categories))
    return categories or ["other"]


def parse_article(path: Path) -> dict[str, object]:
    with zipfile.ZipFile(path) as archive:
        names = set(archive.namelist())
        if "word/afchunk.mht" not in names:
            raise ValueError("DOCX has no word/afchunk.mht")
        html = extract_html_from_mht(archive.read("word/afchunk.mht"))

    parser = MiniDOMParser()
    parser.feed(html)
    root = parser.root

    title = first_text(find_by_class(root, "title")) or first_tag_text(root, "title")
    title = title or path.stem
    publish_date = first_text(find_by_class(root, "create_time"))
    author = first_text(find_by_class(root, "author"))
    nickname = first_text(find_by_class(root, "nick_name"))
    ip_location = first_text(find_by_class(root, "ip"))
    source_url = canonical_url(root)

    body_nodes = find_by_class(root, "item_show_type_0")
    paid_nodes = find_by_class(root, "pay_subscribe_notice")
    teaser_nodes = find_by_class(root, "pay_subscribe_desc")
    raw_body = "\n".join(node_text(node, skip_classes={"__bottom-bar__"}) for node in body_nodes)
    raw_body = normalize_text(raw_body)
    cleaned_body, promo_tail = clean_promotional_tail(raw_body)
    teaser = first_text(teaser_nodes)
    figures = body_images(body_nodes)
    emphasis = emphasized_text(body_nodes)

    if len(cleaned_body) > 100:
        availability = "full"
    elif paid_nodes:
        availability = "paid_preview"
    else:
        availability = "empty"

    title_banks = identify_banks(title, "")
    categories = classify(title, title_banks)
    banks = identify_banks(
        title,
        cleaned_body,
        full_scan="cross_bank_comparison" in categories,
    )
    categories = classify(title, banks)
    report_year, report_period = infer_report_period(
        title, publish_date, categories, banks
    )
    text_hash = hashlib.sha256(cleaned_body.encode("utf-8")).hexdigest() if cleaned_body else ""
    source_key = source_url or str(path.name)
    article_id = hashlib.sha1(source_key.encode("utf-8")).hexdigest()[:12]

    return {
        "article_id": article_id,
        "file_name": path.name,
        "source_path": str(path.resolve()),
        "title": title,
        "publish_date": publish_date,
        "author": author,
        "nickname": nickname,
        "ip_location": ip_location,
        "source_url": source_url,
        "availability": availability,
        "teaser": teaser,
        "body": cleaned_body,
        "body_chars": len(cleaned_body),
        "removed_promo_chars": len(promo_tail),
        "figure_urls": figures,
        "figure_count": len(figures),
        "emphasized_passages": emphasis,
        "banks": banks,
        "report_year": report_year,
        "report_period": report_period,
        "categories": categories,
        "text_sha256": text_hash,
        "duplicate_of": "",
        "extraction_error": "",
    }


def assign_duplicates(records: list[dict[str, object]]) -> None:
    seen: dict[str, str] = {}
    for record in records:
        key = str(record.get("source_url") or record.get("text_sha256") or "")
        if not key:
            continue
        article_id = str(record["article_id"])
        if key in seen:
            record["duplicate_of"] = seen[key]
        else:
            seen[key] = article_id


def safe_markdown(value: object) -> str:
    return str(value or "").replace("\n", " ").strip()


def write_text_cache(record: dict[str, object], text_dir: Path) -> None:
    text_dir.mkdir(parents=True, exist_ok=True)
    destination = text_dir / f"{record['article_id']}.md"
    metadata = [
        "---",
        f"article_id: {safe_markdown(record['article_id'])}",
        f"title: {json.dumps(record['title'], ensure_ascii=False)}",
        f"publish_date: {json.dumps(record['publish_date'], ensure_ascii=False)}",
        f"source_file: {json.dumps(record['source_path'], ensure_ascii=False)}",
        f"source_url: {json.dumps(record['source_url'], ensure_ascii=False)}",
        f"availability: {record['availability']}",
        f"banks: {json.dumps(record['banks'], ensure_ascii=False)}",
        f"report_year: {json.dumps(record['report_year'], ensure_ascii=False)}",
        f"report_period: {json.dumps(record['report_period'], ensure_ascii=False)}",
        f"categories: {json.dumps(record['categories'], ensure_ascii=False)}",
        "---",
        "",
        f"# {safe_markdown(record['title'])}",
        "",
    ]
    if record.get("availability") == "paid_preview":
        metadata.extend(["## 付费摘要", "", str(record.get("teaser") or "")])
    else:
        metadata.append(str(record.get("body") or ""))
    figures = list(record.get("figure_urls") or [])
    if figures:
        metadata.extend(["", "## 原文图表链接", ""])
        metadata.extend(f"- {url}" for url in figures)
    destination.write_text("\n".join(metadata).rstrip() + "\n", encoding="utf-8")


def write_outputs(
    records: list[dict[str, object]], output_dir: Path, write_text: bool
) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    jsonl_path = output_dir / "articles.jsonl"
    with jsonl_path.open("w", encoding="utf-8") as handle:
        for record in records:
            handle.write(json.dumps(record, ensure_ascii=False) + "\n")

    csv_fields = [
        "article_id",
        "file_name",
        "title",
        "publish_date",
        "source_url",
        "availability",
        "body_chars",
        "figure_count",
        "banks",
        "report_year",
        "report_period",
        "categories",
        "duplicate_of",
        "extraction_error",
    ]
    with (output_dir / "index.csv").open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=csv_fields)
        writer.writeheader()
        for record in records:
            row = {field: record.get(field, "") for field in csv_fields}
            for field in ("banks", "categories"):
                row[field] = "|".join(str(item) for item in list(row[field] or []))
            writer.writerow(row)

    if write_text:
        text_dir = output_dir / "text"
        for record in records:
            write_text_cache(record, text_dir)

    full_lengths = sorted(
        int(record["body_chars"])
        for record in records
        if record.get("availability") == "full"
    )
    category_counts = Counter(
        category for record in records for category in list(record.get("categories") or [])
    )
    bank_counts = Counter(
        bank for record in records for bank in list(record.get("banks") or [])
    )
    year_counts = Counter(
        str(record.get("publish_date") or "")[:4]
        for record in records
        if re.match(r"(?:19|20)\d{2}", str(record.get("publish_date") or ""))
    )
    summary = {
        "generated_at": datetime.now().astimezone().isoformat(timespec="seconds"),
        "article_count": len(records),
        "availability": dict(Counter(str(record["availability"]) for record in records)),
        "duplicate_count": sum(bool(record.get("duplicate_of")) for record in records),
        "full_text_chars": sum(full_lengths),
        "full_text_median_chars": int(statistics.median(full_lengths)) if full_lengths else 0,
        "article_with_figures_count": sum(int(record.get("figure_count") or 0) > 0 for record in records),
        "figure_url_count": sum(int(record.get("figure_count") or 0) for record in records),
        "category_counts_overlapping": dict(category_counts.most_common()),
        "bank_counts_overlapping": dict(bank_counts.most_common()),
        "publish_year_counts": dict(sorted(year_counts.items())),
    }
    (output_dir / "summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input-dir", type=Path, required=True, help="Directory containing DOCX articles")
    parser.add_argument("--output-dir", type=Path, required=True, help="Directory for JSONL/CSV outputs")
    parser.add_argument(
        "--write-text-cache",
        action="store_true",
        help="Also write one normalized Markdown file per article for rg-based retrieval",
    )
    args = parser.parse_args()

    input_dir = args.input_dir.expanduser().resolve()
    output_dir = args.output_dir.expanduser().resolve()
    paths = sorted(input_dir.glob("*.docx"), key=lambda path: path.name)
    if not paths:
        raise SystemExit(f"No DOCX files found in {input_dir}")

    records: list[dict[str, object]] = []
    for index, path in enumerate(paths, start=1):
        try:
            records.append(parse_article(path))
        except Exception as exc:  # keep the corpus audit complete
            source_key = str(path.name)
            records.append(
                {
                    "article_id": hashlib.sha1(source_key.encode("utf-8")).hexdigest()[:12],
                    "file_name": path.name,
                    "source_path": str(path.resolve()),
                    "title": path.stem,
                    "publish_date": "",
                    "author": "",
                    "nickname": "",
                    "ip_location": "",
                    "source_url": "",
                    "availability": "error",
                    "teaser": "",
                    "body": "",
                    "body_chars": 0,
                    "removed_promo_chars": 0,
                    "figure_urls": [],
                    "figure_count": 0,
                    "emphasized_passages": [],
                    "banks": [],
                    "report_year": "",
                    "report_period": "",
                    "categories": ["other"],
                    "text_sha256": "",
                    "duplicate_of": "",
                    "extraction_error": f"{type(exc).__name__}: {exc}",
                }
            )
        if index % 250 == 0 or index == len(paths):
            print(f"Parsed {index}/{len(paths)}", file=sys.stderr)

    assign_duplicates(records)
    write_outputs(records, output_dir, args.write_text_cache)
    print(json.dumps(json.loads((output_dir / "summary.json").read_text(encoding="utf-8")), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
