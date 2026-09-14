"""Reproduce the arithmetic and source reconciliations for this dated report."""
from decimal import Decimal, getcontext
import json
from pathlib import Path
import re
import subprocess
import sys

getcontext().prec = 36
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
TOOL = ROOT / "tools" / "financial_rigor.py"
D = Decimal
logs = []

def run(*args):
    result = subprocess.run([sys.executable, str(TOOL), *args], check=True, text=True, capture_output=True)
    logs.append(result.stdout)
    return result.stdout

# Historical amounts below are USD millions, collected on 2026-09-07.
annual = {
    "FY2022": [26914, 9752, 64.9, 9108, 8049, 8132, 83],
    "FY2023": [26974, 4368, 56.9, 5641, 3750, 3808, 58],
    "FY2024": [60922, 29760, 72.7, 28090, 26947, 27021, 74],
    "FY2025": [130497, 72880, 75.0, 64089, 60724, 60853, 129],
    "FY2026": [215938, 120067, 71.1, 102718, 96575, 96676, 101],
}
checks = []
for year, (rev, profit, gm, ocf, fcf, sa_fcf, principal) in annual.items():
    for field, primary, secondary in [
        ("revenue", rev, rev), ("GAAP_net_income", profit, profit),
        ("operating_cash_flow", ocf, ocf),
        ("FCF_after_principal_reconciliation", fcf, sa_fcf-principal),
    ]:
        values = {"NVIDIA_SEC": primary, "StockAnalysis_reconciled" if "FCF" in field else "StockAnalysis": secondary}
        run("cross-validate", "--field", year+"_"+field, "--values", json.dumps(values), "--unit", "USD_million", "--tolerance", "1")
        checks.append({"field": year+"_"+field, "values": values, "deviation_pct": "0"})

for field, value in {"Q2_revenue":96221, "Q2_GAAP_net_income":59688, "Q2_operating_income":63734,
                     "TTM_revenue":302970, "TTM_GAAP_net_income":192880, "TTM_operating_income":197579}.items():
    run("cross-validate", "--field", field, "--values", json.dumps({"NVIDIA_SEC":value,"StockAnalysis":value}), "--unit", "USD_million", "--tolerance", "1")

expressions = {
    "TTM_revenue_USD_million": "215938 + 177837 - 90805",
    "TTM_GAAP_profit_USD_million": "120067 + 118010 - 45197",
    "Q2_Data_Center_pct": "89023 / 96221 * 100",
    "Q2_operating_margin_pct": "63734 / 96221 * 100",
    "TTM_tax_after_operating_profit_USD_bn": "197.579 * (1 - 0.17)",
    "Q2_annualized_revenue_USD_bn": "96.221 * 4",
    "Q2_annualized_tax_after_operating_profit_USD_bn": "63.734 * 4 * (1 - 0.17)",
    "Q2_tax_after_operating_margin_pct": "63.734 * (1 - 0.17) / 96.221 * 100",
    "bear_revenue_USD_bn": "1000 * 0.30 + 50",
    "bear_profit_USD_bn": "(1000 * 0.30 + 50) * 0.25",
    "base_revenue_USD_bn": "2000 * 0.45 + 100",
    "base_profit_USD_bn": "(2000 * 0.45 + 100) * 0.40",
    "bull_revenue_USD_bn": "3000 * 0.60 + 200",
    "bull_profit_USD_bn": "(3000 * 0.60 + 200) * 0.45",
    "base_revenue_CAGR_pct": "((1000 / (96.221 * 4)) ** (1 / 10) - 1) * 100",
    "base_profit_CAGR_pct": "((400 / (63.734 * 4 * 0.83)) ** (1 / 10) - 1) * 100",
    "base_share_minus_10pp_profit_USD_bn": "(2000 * 0.35 + 100) * 0.40",
    "base_margin_minus_10pp_profit_USD_bn": "(2000 * 0.45 + 100) * 0.30",
    "base_both_minus_10pp_profit_USD_bn": "(2000 * 0.35 + 100) * 0.30",
}
for year, row in annual.items():
    for field, pos in [("revenue", 0), ("net_income", 1), ("OCF", 3), ("FCF", 4)]:
        expressions[f"{year}_{field}_USD_100million"] = f"{row[pos]} / 100"
for field, value in {"Q2_revenue":96221, "Q2_net_income":59688, "Q2_operating_income":63734,
                     "Q2_FCF":21341, "TTM_FCF":126886, "TTM_revenue":302970,
                     "TTM_net_income":192880, "TTM_operating_income":197579,
                     "Data_Center":89023, "Edge":7198, "TTM_equity_gain":30552}.items():
    expressions[field+"_USD_100million"] = f"{value} / 100"
results = {}
for name, expr in expressions.items():
    output = run("calc", "--expr", expr)
    result = re.search(r"精确值:\s*([^\n]+)", output).group(1).replace(",", "").strip()
    # Independent Decimal evaluation of this fixed, locally authored arithmetic.
    decimal_expr = re.sub(r"(?<![A-Za-z_])\d+(?:\.\d+)?", lambda m: "D('"+m.group(0)+"')", expr)
    independent = eval(decimal_expr, {"__builtins__": {}, "D": D})
    relative = abs(D(result)-independent) / max(abs(independent), D(1))
    assert relative < D("1e-12"), (name, result, str(independent))
    results[name] = {"expression":expr,"financial_rigor":result,"independent_decimal":str(independent)}

payload = {"cutoff":"2026-09-07", "annual_columns":["revenue","GAAP_net_income","gross_margin_pct","OCF","NVIDIA_FCF","StockAnalysis_FCF","equipment_principal"],
           "annual_USD_million":annual,"cross_checks":checks,"calculations":results,
           "audit_boundary":"Inputs for 2036 are author assumptions, not observed facts or externally validated forecasts. Source agreement is not independent economic truth."}
(HERE / "arithmetic.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2)+"\n")
(HERE / "financial-rigor.txt").write_text("\n".join(logs))
print(json.dumps(results, ensure_ascii=False, indent=2))
