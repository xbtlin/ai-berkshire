"""Reproduce the seeded sample and its explicitly scoped review."""
import json
from pathlib import Path
import re
import subprocess
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
REPORT = HERE.parent / "英伟达商业模式与十年利润研究-20260907.md"
TOOL = ROOT / "tools" / "report_audit.py"
REPORT_LABEL = str(REPORT.relative_to(ROOT))
raw = subprocess.check_output([sys.executable, str(TOOL), "extract", "--report", REPORT_LABEL, "--seed", "42"], cwd=ROOT, text=True)
(HERE / "audit-extract.txt").write_text("\n".join(line.rstrip() for line in raw.splitlines())+"\n")
sample = json.loads(raw[raw.index("[\n"):])
sec23 = "https://www.sec.gov/Archives/edgar/data/1045810/000104581023000017/nvda-20230129.htm"
sec26 = "https://www.sec.gov/Archives/edgar/data/1045810/000104581026000021/nvda-20260125.htm"
sa = "https://stockanalysis.com/stocks/nvda/financials/"
facts = {
    2:(269.74,269.74,sec23), 8:(297.60,297.60,sec26), 9:(728.80,728.80,sec26),
    15:(71.1,71.07,sec26), 18:(280.90,280.90,sec26),16:(91.08,91.08,sec23),
}
assert {x["id"] for x in sample} == set(facts) | {41,48,53}
for item in sample:
    if item["id"] in facts:
        value1, value2, source = facts[item["id"]]
        item.update(fetched_value=value1,fetched_value2=value2,fetched_source=source,fetched_source2=sa,review_type="reported_fact")
        if not item["unit"]:
            item["unit"] = "亿美元"
    elif item["id"] == 53:
        model = json.loads((HERE / "arithmetic.json").read_text())["calculations"]["base_share_minus_10pp_profit_USD_bn"]
        item.update(fetched_value=float(model["financial_rigor"])*10,
                    fetched_value2=float(model["independent_decimal"])*10,
                    fetched_source="financial_rigor: (2000 * 0.35 + 100) * 0.40; USD bn converted to 亿美元",
                    fetched_source2="Independent Decimal arithmetic; NOT independent forecast evidence",
                    review_type="formula_only",unit="亿美元")
    else:
        item.update(review_type="author_assumption_not_fact",review_note="Explicit scenario parameter; no external fetched value or factual certification is claimed.")
(HERE / "audit-results.json").write_text(json.dumps(sample, ensure_ascii=False,indent=2)+"\n")
verdict = subprocess.check_output([sys.executable, str(TOOL), "verdict", "--results", json.dumps(sample,ensure_ascii=False), "--report", REPORT_LABEL], cwd=ROOT, text=True)
verdict = re.sub(r"\x1b\[[0-9;]*m", "", verdict)
(HERE / "audit-verdict.txt").write_text("\n".join(line.rstrip() for line in verdict.splitlines())+"\n")
print(verdict)
