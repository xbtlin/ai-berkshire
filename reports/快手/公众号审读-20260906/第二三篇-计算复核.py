"""Recalculate the article models; source verification is recorded separately."""
from decimal import Decimal as D, getcontext
from pathlib import Path
import json
import re
import subprocess

getcontext().prec = 40
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
RIGOR = ROOT / "tools/financial_rigor.py"
records = []


def check(name, expression, exact, kind="calculation"):
    run = subprocess.run(
        ["python3", str(RIGOR), "calc", "--expr", expression],
        text=True, capture_output=True, check=True,
    )
    match = re.search(r"精确值:\s*([^\s]+)", run.stdout)
    assert match, name
    tool_value = D(match.group(1))
    assert abs(tool_value - exact) <= max(abs(exact), D(1)) * D("1e-12"), name
    records.append({"name": name, "expression": expression, "decimal_value": str(exact),
                    "kind": kind, "tool_output": run.stdout})
    return exact


price, shares, fx = D("33.66"), D("4326961215"), D("0.8559")
share_units = shares / D("1e8")
hkd_cap = check("港元市值_亿元", "33.66*4326961215/1e8", price * share_units)
cny_cap = check("人民币市值_亿元", "33.66*4326961215/1e8*0.8559", hkd_cap * fx)
ttm_profit = check("IFRS归母TTM利润_亿元", "186.17+60.49-89", D("186.17") + D("60.49") - D("89"))
pe = check("IFRS归母TTM市盈率", "33.66*4326961215/1e8*0.8559/(186.17+60.49-89)", cny_cap / ttm_profit)

historical = []
for year, cfo, capex in [(2021, "-55.19", "77.64"), (2022, "7.95", "51.00"),
                         (2023, "207.81", "48.97"), (2024, "297.87", "80.63"),
                         (2025, "267.16", "149.42")]:
    fcf = check(f"{year}简单自由现金流_亿元", f"({cfo})-({capex})", D(cfo) - D(capex))
    historical.append({"year": year, "cfo": cfo, "capital_purchases": capex, "simple_fcf": str(fcf)})

bridge = {}
for name, expression, value in [
    ("2025扣租赁现金代理", "267.16-149.42-38.23", D("267.16") - D("149.42") - D("38.23")),
    ("2025再扣股份薪酬现金代理", "267.16-149.42-38.23-26.40", D("267.16") - D("149.42") - D("38.23") - D("26.40")),
    ("H12026近似资本购买", "121+59", D(121) + D(59)),
    ("H12026近似简单FCF", "90.44-121-59", D("90.44") - D(121) - D(59)),
    ("TTM经营现金流", "267.16-117.81+90.44", D("267.16") - D("117.81") + D("90.44")),
    ("TTM近似资本购买", "149.42-70.75+121+59", D("149.42") - D("70.75") + D(121) + D(59)),
    ("TTM近似简单FCF", "267.16-117.81+90.44-(149.42-70.75+121+59)", D("267.16") - D("117.81") + D("90.44") - (D("149.42") - D("70.75") + D(121) + D(59))),
    ("流动金融资源", "116.96+123.58+563.53", D("116.96") + D("123.58") + D("563.53")),
    ("流动资源减借款租赁", "804.07-273.62-116.72", D("804.07") - D("273.62") - D("116.72")),
    ("可灵条件经济权益", "66.33+2", D("66.33") + D(2)),
    ("可灵条件投票权", "52.23+1.57", D("52.23") + D("1.57")),
    ("可灵充分认购投后规模_亿美元", "150+30", D(150) + D(30)),
]:
    bridge[name] = str(check(name, expression, value))
for direct in (25, 45, 65):
    check(f"每100收入教学贡献_直接成本{direct}", f"100-{direct}-15", D(100) - D(direct) - D(15), "teaching_assumption")

cases = {
    "保守": {"cash": [0, 20, 35, 45, 50, 50, 50, 50, 50, 50], "g": "0", "surplus": "100"},
    "基准": {"cash": [30, 60, 80, 100, 120, 130, 140, 150, 160, 170], "g": "0.01", "surplus": "150"},
    "乐观": {"cash": [70, 100, 130, 160, 200, 230, 260, 290, 320, 350], "g": "0.02", "surplus": "200"},
}
original = json.loads((ROOT / "reports/快手/《看懂快手》-20260906/审计/dcf_scenarios.json").read_text())
models = []
for name, case in cases.items():
    for rate in (["0.08", "0.09", "0.10", "0.12"] if name == "基准" else ["0.08", "0.09"]):
        r, g, surplus = D(rate), D(case["g"]), D(case["surplus"])
        cash = [D(value) for value in case["cash"]]
        explicit = sum(value / (1 + r) ** year for year, value in enumerate(cash, 1))
        terminal = cash[-1] * (1 + g) / (r - g) / (1 + r) ** len(cash)
        total = explicit + terminal + surplus
        hkd_value = total / share_units / fx
        expression = "+".join(f"{value}/(1+{r})**{year}" for year, value in enumerate(cash, 1))
        expression += f"+{cash[-1]}*(1+{g})/({r}-{g})/(1+{r})**10+{surplus}"
        check(f"{name}_{rate}_每股港元", f"({expression})/(4326961215/1e8)/0.8559", hkd_value, "model_assumption")
        if rate in ["0.08", "0.09"]:
            prior = next(row for row in original if row["case"] == name and D(row["r"]) == r)
            assert abs(D(prior["hkd_per_share"]) - hkd_value) < D("1e-16")
        models.append({"case": name, "r": rate, "g": str(g), "cash_cny_yi": case["cash"],
                       "surplus_cny_yi": str(surplus), "explicit_pv": str(explicit),
                       "terminal_pv": str(terminal), "hkd_per_share": str(hkd_value),
                       "terminal_fraction_core": str(terminal / (explicit + terminal))})

base12 = D(next(row["hkd_per_share"] for row in models if row["case"] == "基准" and row["r"] == "0.12"))
check("25港元观察线的未取整计算", f"{base12}*0.75", base12 * D("0.75"), "model_policy")
report = {"cutoff": "2026-09-06", "price_date": "2026-09-04", "historical_cash": historical,
          "market_cap_cny_yi": str(cny_cap), "ttm_parent_profit_yi": str(ttm_profit), "ttm_pe": str(pe),
          "bridge": bridge, "models": models, "checks": records,
          "scope": "数学复算，不代表预测实现或全量双源审计；历史53.11亿元代理未精确扣融资付息和少数权益，前瞻现金另明确定义。近似现金流保留资本购买输入的舍入误差。"}
(HERE / "第二三篇-计算复核.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
print(json.dumps({"calculation_checks": len(records), "model_cases": len(models), "ttm_pe": str(pe)}, ensure_ascii=False))
