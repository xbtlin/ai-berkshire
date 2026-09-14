#!/usr/bin/env python3
"""Separate historical-data sampling from forecast-assumption checks."""
import importlib.util
import json
import pathlib
import subprocess
import sys
from decimal import Decimal as D

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[2]
REPORT = HERE.parent / "快手与美团底稿.md"
TOOL = ROOT / "tools" / "report_audit.py"
spec = importlib.util.spec_from_file_location("report_audit", TOOL)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
sample = mod.sample_points(mod.extract_data_points(REPORT.read_text()), seed=42)
(HERE / "audit_sample_seed42.json").write_text(json.dumps(sample, ensure_ascii=False, indent=2) + "\n")
extract = subprocess.run([sys.executable, str(TOOL), "extract", "--report", str(REPORT), "--seed", "42"], capture_output=True, text=True, check=True)
(HERE / "audit_extract_seed42.txt").write_text(extract.stdout)

official_ks = "https://www1.hkexnews.hk/listedco/listconews/sehk/2026/0819/2026081900315_c.pdf"
official_mt = "https://www.hkexnews.hk/listedco/listconews/sehk/2026/0828/2026082800436_c.pdf"
ithome = "https://www.ithome.com/0/991/705.htm"
yiou = "https://finance.sina.com.cn/stock/relnews/hk/2026-08-28/doc-inipwnxp8987332.shtml"
facts = {
    4: (692.51, official_ks, 692.51, ithome),
    5: (60.49, official_ks, 60.49, ithome),
    12: (-24.44270, official_mt, -24.44, yiou),
}
# These are inputs or an independent Decimal reconstruction, not external forecasts.
assumptions = {
    15: D("300"),
    18: D("180"),
    29: D("35000"),
    32: D("0.016") * 100,
    36: D("300") * D("180") / 100 + D("200") + D("11000") * D("0.012"),
    55: D("300") * D("0.20") * D("0.50"),
    70: D("7000") * D("0.17"),
    76: -D("220"),
    82: D("7000") * D("0.17") + D("150") - D("220") - D("30"),
    87: (D("7000") * D("0.17") + D("150") - D("220") - D("30")) * D("0.80"),
}
actual, model, excluded = [], [], []
for p in sample:
    p = dict(p)
    if p["id"] in facts:
        p["fetched_value"], p["fetched_source"], p["fetched_value2"], p["fetched_source2"] = facts[p["id"]]
        p["classification"] = "historical_fact"
        actual.append(p)
    elif p["id"] in assumptions:
        p["fetched_value"] = float(assumptions[p["id"]])
        p["fetched_source"] = "Model input or independent Decimal reconstruction in audit.py; not externally verified forecast"
        p["classification"] = "model_assumption_or_calculation"
        model.append(p)
    elif p["id"] == 14:
        p["reason"] = "The extractor matched the year 2025 in a narrative table, not a financial amount. Full behavior claim checked in official annual report."
        excluded.append(p)
    else:
        raise RuntimeError(f"Unclassified sample {p}")
for name, items in (("facts", actual), ("model", model)):
    (HERE / f"audit_{name}_seed42.json").write_text(json.dumps(items, ensure_ascii=False, indent=2) + "\n")
    run = subprocess.run([sys.executable, str(TOOL), "verdict", "--report", f"{REPORT.name} - {name} only", "--results", json.dumps(items, ensure_ascii=False)], capture_output=True, text=True, check=True)
    (HERE / f"audit_{name}_verdict_seed42.txt").write_text(run.stdout)
    print(run.stdout[-450:])
(HERE / "audit_scope.json").write_text(json.dumps({"seed": 42, "sample_count": len(sample), "historical_facts": len(actual), "model_consistency_only": len(model), "excluded": excluded, "forecast_validated": False}, ensure_ascii=False, indent=2) + "\n")
