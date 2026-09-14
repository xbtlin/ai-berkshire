#!/usr/bin/env python3
"""Reproduce this memo's arithmetic through the repository's financial_rigor CLI."""
import json
import pathlib
import re
import subprocess
import sys

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[2]
TOOL = ROOT / "tools" / "financial_rigor.py"

calculations = {
    "kuaishou_2025_revenue_yi": "142776 / 100",
    "kuaishou_2025_parent_profit_yi": "18617 / 100",
    "kuaishou_2025_adjusted_profit_yi": "20647 / 100",
    "kuaishou_2026h1_revenue_yi": "69251 / 100",
    "kuaishou_2026h1_parent_profit_yi": "6049 / 100",
    "kuaishou_2026h1_adjusted_profit_yi": "7287 / 100",
    "meituan_2025_revenue_yi": "364854746 / 100000",
    "meituan_2025_parent_profit_yi": "-23355015 / 100000",
    "meituan_2025_adjusted_profit_yi": "-18648001 / 100000",
    "meituan_2026h1_revenue_yi": "195681950 / 100000",
    "meituan_2026h1_parent_profit_yi": "-4672487 / 100000",
    "meituan_2026h1_group_profit_yi": "-4672036 / 100000",
    "meituan_2026h1_adjusted_profit_yi": "-2444270 / 100000",
    "kuaishou_2025_ads_yi": "81462 / 100",
    "kuaishou_2025_live_yi": "39087 / 100",
    "kuaishou_2025_other_yi": "22227 / 100",
    "kuaishou_2025_ec_gmv_yi": "1598070.7 / 100",
    "kuaishou_2026h1_sbc_yi": "1311 / 100",
    "meituan_2026h1_sbc_yi": "3301589 / 100000",
    "meituan_2024_core_margin_pct": "52415162 / 250247496 * 100",
    "meituan_2026q2_core_margin_pct": "5668275 / 71530555 * 100",
    "meituan_2026h1_core_runrate_yi": "135593841 / 100000 * 2",
    "meituan_base_1ppt_core_margin_profit_yi": "5000 * 0.01 * (1 - 0.20)",
    "kuaishou_base_1pct_point_core_margin_yi": "1722 * 0.01",
    "kuaishou_base_kling_10pct_less_ownership_yi": "300 * 0.20 * 0.10",
    "kuaishou_2025_ocf_less_capex_yi": "267.16 - 149.42",
    "meituan_2024_buyback_cash_yi": "26089621 / 100000",
    "meituan_2025_buyback_cash_yi": "364843 / 100000",
}

kuaishou = {
    "bear": {"dau_million": 300, "annual_ad_arpu_cny": 180, "live_revenue_yi": 200, "gmv_yi": 11000, "commission_rate": "0.012", "core_net_margin": "0.05", "kling_revenue_yi": 60, "kling_net_margin": "-0.10", "kling_owner_share": "0.60", "other_net_loss_yi": 20},
    "base": {"dau_million": 400, "annual_ad_arpu_cny": 280, "live_revenue_yi": 280, "gmv_yi": 23000, "commission_rate": "0.014", "core_net_margin": "0.12", "kling_revenue_yi": 300, "kling_net_margin": "0.20", "kling_owner_share": "0.50", "other_net_loss_yi": 10},
    "bull": {"dau_million": 450, "annual_ad_arpu_cny": 350, "live_revenue_yi": 350, "gmv_yi": 35000, "commission_rate": "0.016", "core_net_margin": "0.15", "kling_revenue_yi": 800, "kling_net_margin": "0.25", "kling_owner_share": "0.40", "other_net_loss_yi": 0},
}
meituan = {
    "bear": {"core_revenue_yi": 3500, "core_operating_margin": "0.06", "new_business_operating_profit_yi": -80, "hq_sbc_cost_yi": 180, "net_funding_cost_yi": 20, "effective_tax": "0"},
    "base": {"core_revenue_yi": 5000, "core_operating_margin": "0.13", "new_business_operating_profit_yi": 30, "hq_sbc_cost_yi": 180, "net_funding_cost_yi": 20, "effective_tax": "0.20"},
    "bull": {"core_revenue_yi": 7000, "core_operating_margin": "0.17", "new_business_operating_profit_yi": 150, "hq_sbc_cost_yi": 220, "net_funding_cost_yi": 30, "effective_tax": "0.20"},
}
for case, a in kuaishou.items():
    ads = f"{a['dau_million']} * {a['annual_ad_arpu_cny']} / 100"
    commerce = f"{a['gmv_yi']} * {a['commission_rate']}"
    core = f"({ads} + {a['live_revenue_yi']} + {commerce})"
    kling = f"{a['kling_revenue_yi']} * {a['kling_net_margin']} * {a['kling_owner_share']}"
    calculations[f"kuaishou_{case}_ads_yi"] = ads
    calculations[f"kuaishou_{case}_commerce_yi"] = commerce
    calculations[f"kuaishou_{case}_core_revenue_yi"] = core
    calculations[f"kuaishou_{case}_core_profit_yi"] = f"{core} * {a['core_net_margin']}"
    calculations[f"kuaishou_{case}_kling_attributable_profit_yi"] = kling
    calculations[f"kuaishou_{case}_total_profit_yi"] = f"{core} * {a['core_net_margin']} + {kling} - {a['other_net_loss_yi']}"
for case, a in meituan.items():
    core = f"{a['core_revenue_yi']} * {a['core_operating_margin']}"
    pre_tax = f"({core} + {a['new_business_operating_profit_yi']} - {a['hq_sbc_cost_yi']} - {a['net_funding_cost_yi']})"
    calculations[f"meituan_{case}_core_profit_yi"] = core
    calculations[f"meituan_{case}_pretax_profit_yi"] = pre_tax
    calculations[f"meituan_{case}_total_profit_yi"] = f"{pre_tax} * (1 - {a['effective_tax']})"

cross_checks = [
    ("快手2025收入", {"HKEX": 1427.76, "StockAnalysis_SandP": 1427.76}),
    ("快手2025归母利润", {"HKEX": 186.17, "StockAnalysis_SandP": 186.17}),
    ("快手2026H1收入", {"HKEX": 692.51, "ITHome_editorial_reproduction": 692.51}),
    ("快手2026H1归母利润", {"HKEX": 60.49, "ITHome_editorial_reproduction": 60.49}),
    ("美团2025收入", {"HKEX": 3648.54746, "StockAnalysis_SandP": 3648.55}),
    ("美团2025归母利润", {"HKEX": -233.55015, "StockAnalysis_SandP": -233.55}),
    ("美团2026H1收入", {"HKEX": 1956.81950, "ChinaSecuritiesJournal_via_Eastmoney": 1956.82}),
    ("美团2026H1集团利润_不是归母", {"HKEX": -46.72036, "ChinaSecuritiesJournal_via_Eastmoney": -46.72}),
    ("美团2026H1经调整集团利润", {"HKEX": -24.44270, "Yiou_via_Sina_editorial_reproduction": -24.44}),
    ("快手2025经营现金流", {"HKEX": 267.16, "Stockopedia_Refinitiv": 267.16}),
    ("快手2025资本支出", {"HKEX": 149.42, "Stockopedia_Refinitiv": 149.42}),
]

outputs = []
results = {}
for name, expr in calculations.items():
    result = subprocess.run([sys.executable, str(TOOL), "calc", "--expr", expr], check=True, text=True, capture_output=True)
    exact = re.search(r"精确值:\s*(\S+)", result.stdout)
    if not exact:
        raise RuntimeError(result.stdout)
    results[name] = {"expression": expr, "exact": exact.group(1)}
    outputs.append(name + "\n" + result.stdout)
for name, values in cross_checks:
    result = subprocess.run([sys.executable, str(TOOL), "cross-validate", "--field", name, "--values", json.dumps(values, ensure_ascii=False), "--unit", "亿元"], check=True, text=True, capture_output=True)
    outputs.append(result.stdout)

payload = {"cutoff": "2026-09-06", "forecast_year": 2036, "unit": "CNY 100 million", "kuaishou": kuaishou, "meituan": meituan, "cross_checks": cross_checks}
(HERE / "model_inputs.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n")
(HERE / "calculations.json").write_text(json.dumps(results, ensure_ascii=False, indent=2) + "\n")
(HERE / "financial_rigor.txt").write_text("\n".join(outputs))
print(json.dumps({k: v for k, v in results.items() if "total_profit" in k}, ensure_ascii=False, indent=2))
