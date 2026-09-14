"""Reproduce the six-company comparison from explicit analyst scenario inputs.

Run from the repository root. Inputs are scenarios, not external observations.
All displayed calculations also run through the shared financial-rigor tool.
"""
import json
import subprocess
from decimal import Decimal, getcontext
from pathlib import Path

getcontext().prec = 40
BASE = Path(__file__).resolve().parent
ROOT = BASE.parent.parent
D = Decimal


def calculate(expr, log):
    result = subprocess.run(
        ["python3", str(ROOT / "tools/financial_rigor.py"), "calc", "--expr", expr],
        cwd=str(ROOT), stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
        universal_newlines=True, check=True,
    )
    log.append(result.stdout)


def irr(price, target, dividends):
    # Annual dividends received at each year end, with sale in year three.
    lo, hi = D("-0.99999"), D("100")
    for _ in range(180):
        mid = (lo + hi) / 2
        value = sum(d / (1 + mid) ** (i + 1) for i, d in enumerate(dividends))
        value += target / (1 + mid) ** 3
        if value > price:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


def main():
    payload = json.loads((BASE / "comparison-inputs.json").read_text(encoding="utf-8"))
    results, log = [], []
    for company in payload["companies"]:
        price = D(str(company["price"]))
        cases = {}
        for case, inputs in company["scenarios"].items():
            target = D(str(inputs["target_price"]))
            dividends = [D(str(v)) for v in inputs["annual_dividends"]]
            if len(dividends) != 3 or price <= 0 or target < 0:
                raise ValueError("Invalid three-year scenario inputs")
            wealth = target + sum(dividends)
            annual = (wealth / price) ** (D(1) / 3) - 1
            formula = "(({}+{})/{})**(1/3)*100-100".format(
                target, "+".join(str(x) for x in dividends), price)
            log.append(company["name"] + " / " + case + " / equivalent terminal-wealth CAGR")
            calculate(formula, log)
            cases[case] = {
                "target_price": str(target),
                "annual_dividends": [str(v) for v in dividends],
                "total_dividends": str(sum(dividends)),
                "total_return_pct": str((wealth / price - 1) * 100),
                "terminal_wealth_cagr_pct": str(annual * 100),
                "annual_cashflow_irr_pct": str(irr(price, target, dividends) * 100),
            }
        base = cases["base"]
        target, dividends = D(base["target_price"]), D(base["total_dividends"])
        # Independent sensitivities: fixed payouts, no additional dividends or
        # earnings growth in a delayed outcome. These are not new forecasts.
        lowered = ((target * D("0.8") + dividends) / price) ** (D(1) / 3) - 1
        delayed = ((target + dividends) / price) ** (D(1) / 5) - 1
        for label, formula in [
            ("terminal_price_minus_20pct", "(({}*0.8+{})/{})**(1/3)*100-100".format(target, dividends, price)),
            ("same_wealth_in_year5", "(({}+{})/{})**(1/5)*100-100".format(target, dividends, price)),
        ]:
            log.append(company["name"] + " / " + label)
            calculate(formula, log)
        results.append({
            "name": company["name"], "price": str(price),
            "currency": company["currency"], "report": company["report"],
            "scenarios": cases,
            "base_terminal_price_minus_20pct_cagr": str(lowered * 100),
            "base_same_wealth_in_year5_cagr": str(delayed * 100),
        })
    output = {
        "as_of": payload["as_of"],
        "method": "Scenario assumptions, not probabilities. CAGR assumes dividends retained without interest. IRR uses disclosed model annual payouts. Delay sensitivity adds no earnings or payout assumptions.",
        "companies": results,
    }
    (BASE / "comparison-results.json").write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding="utf-8")
    (BASE / "comparison-financial-rigor.txt").write_text("\n".join(log), encoding="utf-8")
    for row in results:
        b = row["scenarios"]["base"]
        print(row["name"], "base target", b["target_price"], "CAGR", round(D(b["terminal_wealth_cagr_pct"]), 2), "IRR", round(D(b["annual_cashflow_irr_pct"]), 2))


if __name__ == "__main__":
    main()
