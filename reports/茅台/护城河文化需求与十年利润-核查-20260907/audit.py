"""Separate sampled historical facts, derived ratios, and model assumptions."""
from decimal import Decimal as D
import json
from pathlib import Path
import subprocess
import sys

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[2]
REPORT = OUT.parent / "贵州茅台护城河文化需求与十年利润研究报告-20260907.md"
TOOL = ROOT / "tools/report_audit.py"
calc = json.loads((OUT / "calculations.json").read_text())
raw = subprocess.run([sys.executable, str(TOOL), "extract", "--report", str(REPORT.relative_to(ROOT)), "--seed", "42"],
                     cwd=ROOT, check=True, text=True, capture_output=True).stdout
(OUT / "audit-extract.txt").write_text(raw)
sample = json.loads(raw[raw.index("[\n  {"):])
checked, assumptions = [], []
for item in sample:
    item = dict(item)
    if item["id"] == 2:
        c = next(x for x in calc["source_checks"] if x["field"] == "2026H1营业收入")
        item.update(fetched_value=float(c["primary"]), fetched_source=c["primary_url"],
                    fetched_value2=float(c["secondary"]), fetched_source2=c["secondary_url"], classification="historical_fact")
    elif item["id"] == 8:
        item.update(fetched_value=-1.95,
                    fetched_source="https://static.cninfo.com.cn/finalpage/2026-08-15/1225475868.PDF",
                    fetched_value2=-1.95,
                    fetched_source2="https://finance.sina.com.cn/stock/aiassist/yjbg/2026-08-14/doc-ininhxpi2824915.shtml",
                    classification="historical_fact")
    elif item["id"] == 9:
        item.update(fetched_value=float(calc["metrics"]["2025_attributable_margin"]),
                    fetched_source="2025公司年报归母利润/营业收入*100，Decimal计算",
                    fetched_value2=float(D("823.20")/D("1688.38")*100),
                    fetched_source2="中新网/东方财富报道823.20/1688.38*100，独立取数复算",
                    classification="derived_ratio_not_direct_disclosure")
    elif item["id"] in {15, 18, 16}:
        name, key = {15:("乐观", "realized_price_cagr"), 18:("乐观", "series_revenue_cagr"),
                     16:("悲观", "series_revenue_cagr")}[item["id"]]
        assert D(str(item["reported_value"])) == D(calc["scenarios"][name][key])*100
        item.update(classification="assumption", model_input_matched=True,
                    explanation="未来增长假设无可取历史真值，保留原抽样项，不列入事实核验准出。")
        assumptions.append(item)
        continue
    else:
        raise ValueError(f"Unreviewed sample: {item}")
    checked.append(item)

verdict = subprocess.run([sys.executable, str(TOOL), "verdict", "--results", json.dumps(checked,ensure_ascii=False),
                          "--report", "茅台研究：仅抽样事实及推导比率，排除三项前瞻假设", "--output-json"],
                         check=True, text=True, capture_output=True).stdout
(OUT/"audit-verdict.txt").write_text(verdict)
(OUT/"audit-classified.json").write_text(json.dumps({"historical_or_derived":checked,"assumptions":assumptions}, ensure_ascii=False, indent=2)+"\n")

# Verify all scenario output table cells, not merely the random sample.
report = REPORT.read_text()
for name, s in calc["scenarios"].items():
    for key in ["2036_revenue", "2036_profit"]:
        assert f"{D(s[key]):.2f} 亿元" in report, (name, key)
    assert f"{D(s['2036_mt_sales_tonnes'])/10000:.2f} 万吨" in report
    assert f"{D(s['profit_cagr_from_2025'])*100:+.2f}%" in report
for key in ["2025_attributable_margin", "2026H1_attributable_margin"]:
    assert f"{D(calc['metrics'][key]):.2f}%" in report
assert "1386.90 亿元" in report
print(verdict)
print("All scenario output cells matched Decimal calculations. Three sampled assumptions remain unverified future conditions.")
