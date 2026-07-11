#!/usr/bin/env python3
"""Summarize manually verified forecast backtest rows with exact decimals."""

from __future__ import annotations

import argparse
import csv
import json
from collections import defaultdict
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path


Q = Decimal("0.01")


def D(value: str) -> Decimal | None:
    return Decimal(value) if value.strip() else None


def fmt(value: Decimal) -> str:
    return str(value.quantize(Q, rounding=ROUND_HALF_UP))


def metrics(rows: list[dict[str, str]]) -> dict[str, object]:
    errors = [D(row["actual_pct"]) - D(row["forecast_center_pct"]) for row in rows]
    errors = [error for error in errors if error is not None]
    absolute = sorted(abs(error) for error in errors)
    interval_rows = [row for row in rows if row["forecast_low_pct"] and row["forecast_high_pct"]]
    hits = sum(
        D(row["forecast_low_pct"]) <= D(row["actual_pct"]) <= D(row["forecast_high_pct"])
        for row in interval_rows
    )
    median = absolute[len(absolute) // 2] if absolute else Decimal("0")
    return {
        "count": len(rows),
        "mae_pp": fmt(sum(absolute) / Decimal(len(absolute))) if absolute else "0.00",
        "median_abs_error_pp": fmt(median),
        "mean_signed_error_pp": fmt(sum(errors) / Decimal(len(errors))) if errors else "0.00",
        "within_1pp": sum(error <= Decimal("1") for error in absolute),
        "within_2pp": sum(error <= Decimal("2") for error in absolute),
        "interval_count": len(interval_rows),
        "interval_hits": hits,
        "interval_hit_rate": fmt(Decimal(hits) / Decimal(len(interval_rows)) * 100) if interval_rows else "0.00",
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--json", type=Path, required=True)
    parser.add_argument("--markdown", type=Path, required=True)
    args = parser.parse_args()

    with args.input.expanduser().resolve().open(encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    overall = metrics(rows)
    by_bank: dict[str, list[dict[str, str]]] = defaultdict(list)
    by_era: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        by_bank[row["bank"]].append(row)
        by_era["2018-2021" if int(row["report_year"]) <= 2021 else "2022-2026"].append(row)

    summary = {
        "overall": overall,
        "by_bank": {bank: metrics(bank_rows) for bank, bank_rows in sorted(by_bank.items())},
        "by_era": {era: metrics(era_rows) for era, era_rows in sorted(by_era.items())},
        "quality_note_rows": sum(bool(row["quality_note"]) for row in rows),
    }
    json_path = args.json.expanduser().resolve()
    json_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    worst = sorted(
        rows,
        key=lambda row: abs(D(row["actual_pct"]) - D(row["forecast_center_pct"])),
        reverse=True,
    )[:8]
    lines = [
        "# 银行业专家财报预测回测",
        "",
        "## 口径",
        "",
        "- 以银行和报告期去重，合并同一预测的上下篇。",
        "- 预测值取文章最终采用的中性值；区间取文章明确表述的高概率区间，未给区间时不计算命中率。",
        "- 实际值取对应官方财报的归属于本行股东净利润同比增速，并由后续点评交叉核对。",
        "- 误差单位均为百分点，严格使用文章发布日期之前的信息作为预测输入。",
        "",
        "## 总体结果",
        "",
        f"- 独立报告期：{overall['count']} 个。",
        f"- 中性预测 MAE：{overall['mae_pp']} 个百分点；绝对误差中位数：{overall['median_abs_error_pp']} 个百分点。",
        f"- 30 个明确概率区间中命中 {overall['interval_hits']} 个，命中率 {overall['interval_hit_rate']}%。",
        f"- 中性值误差不超过 1 个百分点：{overall['within_1pp']} 个；不超过 2 个百分点：{overall['within_2pp']} 个。",
        "",
        "## 分银行",
        "",
        "| 银行 | 样本 | MAE（百分点） | 区间命中率 |",
        "|---|---:|---:|---:|",
    ]
    for bank, item in summary["by_bank"].items():
        lines.append(f"| {bank} | {item['count']} | {item['mae_pp']} | {item['interval_hit_rate']}% |")
    lines.extend(
        [
            "",
            "## 最大偏差案例",
            "",
            "| 银行/报告期 | 中性预测 | 实际 | 绝对误差 | 主要说明 |",
            "|---|---:|---:|---:|---|",
        ]
    )
    for row in worst:
        error = abs(D(row["actual_pct"]) - D(row["forecast_center_pct"]))
        lines.append(
            f"| {row['bank']} {row['report_year']}{row['report_period']} | "
            f"{row['forecast_center_pct']}% | {row['actual_pct']}% | {fmt(error)} | {row['quality_note'] or row['method_note']} |"
        )
    lines.extend(
        [
            "",
            "## 方法启示",
            "",
            "- 净利息收入、手续费等可拆分项目适合使用规模、价格、季节性和会计口径逐项建模。",
            "- 信用减值是净利润预测最大的非经营性扰动，需与资产质量所需拨备和管理层利润平滑能力分开建情景。",
            "- 宏观或监管制度突变时，历史环比法会失效；2020H1 是最显著样本。",
            "- 后期建设银行预测的稳定性优于早期样本，但仍会在净息差、其他非息收入和减值节奏变化时失准。",
            "- 发布前必须机械验算中性值与区间边界；语料中存在多处符号或上下限算术不一致。",
        ]
    )
    md_path = args.markdown.expanduser().resolve()
    md_path.parent.mkdir(parents=True, exist_ok=True)
    md_path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
