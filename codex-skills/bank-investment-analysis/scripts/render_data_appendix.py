#!/usr/bin/env python3
"""Validate earnings-review records and render a Markdown data appendix.

The completed CSV is an internal interchange format only. Read it from a
temporary path or stdin, render the appendix to stdout, insert the output into
the main report, and do not retain the CSV in the delivery directory.
"""

from __future__ import annotations

import argparse
import csv
from pathlib import Path
import re
import sys
from typing import Iterable, TextIO


FIELDS = [
    "section",
    "metric",
    "value",
    "unit",
    "period",
    "comparison_period",
    "scope",
    "balance_type",
    "status",
    "confidence",
    "source_file",
    "page_note",
    "formula",
    "assumptions",
    "residual",
    "comment",
]
STATUSES = {"disclosed", "calculated", "estimated", "inferred", "N/A"}
CONFIDENCES = {"A", "B", "C", "D", "N/A"}
CORE_RECORD_COUNT = 144

FIELD_LABELS = {
    "section": "分析模块",
    "metric": "指标",
    "value": "数值",
    "unit": "单位",
    "period": "数据期间",
    "comparison_period": "对比期间",
    "scope": "数据范围",
    "balance_type": "统计口径",
    "status": "数据性质",
    "confidence": "可靠程度",
    "source_file": "证据文件",
    "page_note": "页码或附注",
    "formula": "计算方法",
    "assumptions": "估算假设",
    "residual": "核对差额",
    "comment": "使用限制及说明",
}
SECTION_LABELS = {
    "profit": "利润与经营效率（profit）",
    "assets": "资产结构（assets）",
    "loans": "贷款结构（loans）",
    "liabilities": "负债与存款（liabilities）",
    "risk": "风险生成与处置（risk）",
    "provision": "贷款减值准备（provision）",
    "capital": "资本与增长质量（capital）",
    "score": "财报基本面评分（score）",
}
STATUS_LABELS = {
    "disclosed": "财报直接披露",
    "calculated": "确定公式计算",
    "estimated": "假设估算",
    "inferred": "分析推断",
    "N/A": "未披露或不可得",
}
CONFIDENCE_LABELS = {
    "A": "高（A级）",
    "B": "较高（B级）",
    "C": "中（C级）",
    "D": "低（D级）",
    "N/A": "不足（N/A）",
}
METRIC_TERMS = [
    ("FVTPL", "FVTPL（以公允价值计量且变动计入当期损益）"),
    ("FVOCI", "FVOCI（以公允价值计量且变动计入其他综合收益）"),
    ("RORWA", "RORWA（风险加权资产收益率）"),
    ("ROAA", "ROAA（平均总资产收益率）"),
    ("ROAE", "ROAE（平均净资产收益率）"),
    ("CET1", "CET1（核心一级资本）"),
    ("NII", "NII（净利息收入）"),
    ("NIM", "NIM（净息差）"),
    ("RWA", "RWA（风险加权资产）"),
    ("AUM", "AUM（管理客户总资产）"),
    ("LCR", "LCR（流动性覆盖率）"),
    ("NSFR", "NSFR（净稳定资金比例）"),
    ("ABS", "ABS（资产证券化）"),
    ("QoQ", "QoQ（环比）"),
    ("YoY", "YoY（同比）"),
    ("OCI", "OCI（其他综合收益）"),
]
COMPACT_GROUPS = [
    ["section", "metric"],
    ["value", "unit"],
    ["period", "comparison_period"],
    ["scope", "balance_type"],
    ["status", "confidence"],
    ["source_file", "page_note"],
    ["formula", "assumptions", "residual", "comment"],
]


def read_rows(handle: TextIO) -> list[dict[str, str]]:
    reader = csv.DictReader(handle)
    if reader.fieldnames != FIELDS:
        raise ValueError(f"unexpected fields: {reader.fieldnames!r}")
    return [dict(row) for row in reader]


def expected_metrics(template_path: Path) -> list[str]:
    with template_path.open(encoding="utf-8-sig", newline="") as handle:
        return [row["metric"] for row in read_rows(handle)]


def validate_rows(rows: list[dict[str, str]], metrics: list[str]) -> None:
    errors: list[str] = []
    actual_metrics = [row["metric"] for row in rows]
    if len(rows) < len(metrics):
        errors.append("completed records do not contain all core template metrics")
    elif actual_metrics[: len(metrics)] != metrics:
        errors.append("core metric names or order do not match the internal template")
    if len(actual_metrics) != len(set(actual_metrics)):
        errors.append("metric names are not unique")
    for index, row in enumerate(rows, start=1):
        record_id = record_id_for(index)
        status = row["status"]
        confidence = row["confidence"]
        if status not in STATUSES:
            errors.append(f"{record_id}: invalid status {status!r}")
        if confidence not in CONFIDENCES:
            errors.append(f"{record_id}: invalid confidence {confidence!r}")
        if not row["period"]:
            errors.append(f"{record_id}: period is required")
        if status == "N/A":
            if row["value"]:
                errors.append(f"{record_id}: N/A row must not contain value")
            if not row["comment"]:
                errors.append(f"{record_id}: N/A row requires a reason in comment")
        elif not row["value"]:
            errors.append(f"{record_id}: non-N/A row requires value")
        if confidence in {"C", "D"} and not row["assumptions"]:
            errors.append(f"{record_id}: C/D row requires assumptions")
        if status != "N/A" and not row["source_file"]:
            errors.append(f"{record_id}: non-N/A row requires source_file")
    if errors:
        raise ValueError("\n".join(errors))


def escape(value: object) -> str:
    return str(value or "").replace("\n", "<br>").replace("|", "\\|")


def markdown_row(values: Iterable[object]) -> str:
    return "| " + " | ".join(escape(value) for value in values) + " |"


def record_id_for(index: int) -> str:
    if index < 1:
        raise ValueError("record index must be positive")
    if index <= CORE_RECORD_COUNT:
        return f"D{index:03d}"
    return f"E{index - CORE_RECORD_COUNT:03d}"


def display_metric(metric: str) -> str:
    result = metric
    for term, label in METRIC_TERMS:
        result = re.sub(rf"(?<![A-Za-z]){re.escape(term)}(?![A-Za-z])", label, result)
    return result


def raw_metric(metric: str) -> str:
    result = metric
    for term, label in reversed(METRIC_TERMS):
        result = result.replace(label, term)
    return result


def display_value(field: str, value: str) -> str:
    if field == "section":
        return SECTION_LABELS.get(value, value)
    if field in {"metric", "formula", "assumptions", "comment"}:
        return display_metric(value)
    if field == "status":
        return STATUS_LABELS.get(value, value)
    if field == "confidence":
        return CONFIDENCE_LABELS.get(value, value)
    return value


def raw_value(field: str, value: str) -> str:
    if field == "section":
        return {label: raw for raw, label in SECTION_LABELS.items()}.get(value, value)
    if field in {"metric", "formula", "assumptions", "comment"}:
        return raw_metric(value)
    if field == "status":
        return {label: raw for raw, label in STATUS_LABELS.items()}.get(value, value)
    if field == "confidence":
        return {label: raw for raw, label in CONFIDENCE_LABELS.items()}.get(value, value)
    return value


def combined_cell(row: dict[str, str], fields: Iterable[str]) -> str:
    """Pack named CSV fields into one reader-friendly, reversible Markdown cell."""
    return "<br>".join(
        f"{FIELD_LABELS[field]}：{display_value(field, row[field])}" for field in fields
    )


def compact_record(row: dict[str, str], index: int) -> list[str]:
    """Map one 16-field record to the fixed eight-column appendix layout."""
    return [
        record_id_for(index),
        *[combined_cell(row, fields) for fields in COMPACT_GROUPS],
    ]


def recover_compact_record(cells: list[str]) -> dict[str, str]:
    """Recover the original 16 internal fields from compact_record output."""
    if len(cells) != 8:
        raise ValueError("compact record must contain exactly eight cells")
    label_to_field = {label: field for field, label in FIELD_LABELS.items()}
    recovered: dict[str, str] = {}
    for cell in cells[1:]:
        for item in cell.split("<br>"):
            label, separator, value = item.partition("：")
            if not separator or label not in label_to_field:
                raise ValueError(f"invalid compact field: {item!r}")
            field = label_to_field[label]
            recovered[field] = raw_value(field, value)
    if list(recovered) != FIELDS:
        raise ValueError(f"unexpected recovered fields: {list(recovered)!r}")
    return recovered


def render_appendix(rows: list[dict[str, str]]) -> str:
    extension_count = max(0, len(rows) - CORE_RECORD_COUNT)
    record_description = f"核心{CORE_RECORD_COUNT}项"
    if extension_count:
        record_description += f" + 扩展{extension_count}项"
    lines = [
        "## 附录A：可追溯数据底稿",
        "",
        f"> 本附录包含{record_description}，用于回答三个问题：数据来自哪里、数据是财报直接披露还是计算估算、使用这项数据时有什么限制。它不是第二份财报正文。",
        "",
        "| 底稿概念 | 含义 | 阅读方式 |",
        "|---|---|---|",
        "| 数据性质 | 财报直接披露、确定公式计算、假设估算、分析推断、未披露或不可得 | 区分事实、计算结果、估算和观点 |",
        "| 可靠程度 | 高（A级）、较高（B级）、中（C级）、低（D级）、不足（N/A） | 等级越低，越需要同时阅读假设和限制 |",
        "| 证据文件·页码 | 官方报告文件及对应页码或附注 | 用于返回原文复核 |",
        "| 计算方法·假设·限制 | 公式、估算前提、核对差额和适用边界 | 防止把代理值当成披露事实 |",
        "",
        "### 模块导航",
        "",
        "| 编号范围 | 内容 |",
        "|---|---|",
        "| 第1—23项 | 利润与经营效率 |",
        "| 第24—37项 | 资产结构 |",
        "| 第38—49项 | 贷款结构 |",
        "| 第50—68项 | 负债与存款 |",
        "| 第69—91项 | 风险生成与处置 |",
        "| 第92—101项 | 贷款减值准备 |",
        "| 第102—111项 | 资本与增长质量 |",
        "| 第112—144项 | 财报基本面评分 |",
    ]
    if extension_count:
        lines.append(f"| 扩展{extension_count}项 | 量价、手续费、其他非息和费用等补充披露及计算明细 |")
    lines.extend(
        [
            "",
            f"### 完整底稿（{record_description}）",
            "",
            "| 编号 | 分析模块·指标 | 数值·单位 | 数据期间·对比期 | 范围·统计口径 | 数据性质·可靠程度 | 证据文件·页码 | 计算方法·假设·限制 |",
            "|---|---|---:|---|---|---|---|---|",
        ]
    )
    for index, row in enumerate(rows, start=1):
        lines.append(markdown_row(compact_record(row, index)))
    return "\n".join(lines) + "\n"


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(description=__doc__)
    result.add_argument(
        "--input",
        default="-",
        help="Completed internal CSV path; use - for stdin (default).",
    )
    result.add_argument(
        "--template",
        type=Path,
        default=Path(__file__).resolve().parents[1]
        / "assets"
        / "earnings-review-data-template.csv",
        help="Internal metric template used to verify names and order.",
    )
    return result


def main() -> int:
    args = parser().parse_args()
    if args.input == "-":
        rows = read_rows(sys.stdin)
    else:
        with Path(args.input).open(encoding="utf-8-sig", newline="") as handle:
            rows = read_rows(handle)
    metrics = expected_metrics(args.template.expanduser().resolve())
    validate_rows(rows, metrics)
    sys.stdout.write(render_appendix(rows))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
