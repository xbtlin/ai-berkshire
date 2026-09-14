"""Reproduce the comparison report's sampled checks; no network fetching is implied."""
import importlib.util
import json
import subprocess
from decimal import Decimal as D
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
REPORT = HERE / "腾讯与快手对比研究-20260906.md"
spec = importlib.util.spec_from_file_location("report_audit", ROOT / "tools/report_audit.py")
audit = importlib.util.module_from_spec(spec)
spec.loader.exec_module(audit)

run = subprocess.run(
    ["python3", str(ROOT / "tools/report_audit.py"), "extract", "--report", str(REPORT), "--seed", "42"],
    text=True, capture_output=True, check=True,
)
(HERE / "横评抽样原始输出.txt").write_text(run.stdout.replace(str(ROOT) + "/", ""))
points = audit.extract_data_points(REPORT.read_text())
sample = audit.sample_points(points, ratio=0.15, seed=42)
verified, assumptions = [], []
for point in sample:
    item = dict(point)
    label = item["label"]
    if label.startswith("收盘价") and "腾讯" in label:
        item.update(fetched_value=442.80,
                    fetched_source="https://stockanalysis.com/quote/hkg/0700/history/ (2026-09-04)",
                    fetched_value2=442.80,
                    fetched_source2="https://cn.investing.com/equities/tencent-holdings-hk-historical-data (2026-09-04)")
    elif label.startswith("已发行股数") and "快手" in label:
        item.update(fetched_value=3664102236 + 662858979,
                    fetched_source="IR linked Euroland: September 3 next-day B shares + August monthly A shares; URLs in 独立来源与反方核查.md",
                    fetched_value2=4330000000,
                    fetched_source2="https://stockanalysis.com/quote/hkg/1024/statistics/ (4.33 billion, rounded)")
    elif "TTM 归母净利润" in label and "腾讯" in label:
        item.update(fetched_value=float((D(224842) + D(114115) - D(103449)) / 100),
                    fetched_source="Tencent FY2025 + H12026 - H12025 IFRS attributable income; primary statement values 224842,114115,103449 million CNY",
                    fetched_value2=2355.08,
                    fetched_source2="https://stockanalysis.com/quote/hkg/0700/financials/ (TTM net income 235508 million CNY)")
    elif "要求更厚价格保护" in label and "快手" in label:
        values = json.loads((HERE / "估值折现敏感性.json").read_text())
        base = D(next(x["base_price_hkd"] for x in values if x["company"] == "kuaishou" and x["r"] == "0.12"))
        policy = base * D("0.75")
        assert policy.quantize(D("1")) == D(str(item["reported_value"])).quantize(D("1"))
        item.update(classification="研究价格条件，不是可从外部取得的事实", exact_model_value=str(policy),
                    check="12%基准价值打25%折扣后取整为约25港元；未计入事实准出项")
        assumptions.append(item)
        continue
    else:
        raise RuntimeError(f"Sample changed: independently classify and source {label}")
    assert abs(D(str(item["reported_value"])) - D(str(item["fetched_value"]))) / abs(D(str(item["reported_value"]))) <= D(".01")
    assert abs(D(str(item["reported_value"])) - D(str(item["fetched_value2"]))) / abs(D(str(item["reported_value"]))) <= D(".01")
    verified.append(item)

(HERE / "横评抽样事实核验.json").write_text(json.dumps(verified, ensure_ascii=False, indent=2))
(HERE / "横评抽样假设核验.json").write_text(json.dumps(assumptions, ensure_ascii=False, indent=2))
run = subprocess.run(
    ["python3", str(ROOT / "tools/report_audit.py"), "verdict", "--results", json.dumps(verified, ensure_ascii=False), "--report", REPORT.name, "--output-json"],
    capture_output=True, text=True, check=True,
)
(HERE / "横评抽样判决.txt").write_text(run.stdout)
(HERE / "横评抽样范围.json").write_text(json.dumps({
    "seed": 42, "ratio": 0.15, "extracted_points": len(points), "sample_count": len(sample),
    "facts_with_two_source_checks": len(verified), "model_policy_separately_checked": len(assumptions),
    "unclassified_samples": 0,
    "limitation": "仅为本横评抽样，不表示全系列每项事实均双源，也不验证未来假设会实现。来源值为本次实际核读记录；脚本重跑不会自动刷新网络。",
}, ensure_ascii=False, indent=2))
print(f"Sample: {len(sample)}; dual-source factual checks: {len(verified)}; separate model-policy checks: {len(assumptions)}")
