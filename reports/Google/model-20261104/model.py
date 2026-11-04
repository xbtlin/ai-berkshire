"""Alphabet 2026-11-04. Amounts in USD billions, shares in billions, prices in USD.
Run with Python 3 from any directory. Historical inputs and assumptions are sourced in the report.
"""
from pathlib import Path
import json
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
from terminal_value import exit_pe, irr_from_terminal

PRICE, PRICE_C, SHARES = 280.03, 278.27, 12.294
MCAP = (5.888 + 0.827) * PRICE + 5.579 * PRICE_C
RATE, TAX, ROIC = 0.10, 0.18, 0.24
# Operating leases remain expensed in EBIT. Deduct finance leases and preferred book claim.
NET_ASSETS = 265.098 - 90.384 - 126.118 - 3.705 + 0.70 * 90.384 + 0.50 * 135.230 - 18.023
NOPAT = 156.976 * (1 - TAX)
EPS = NOPAT / SHARES

# First/second five-year sales CAGR, operating margins at years 5 and 10.
# Central AI and Other Bets losses are deducted once, after adding segment profits.
SCENARIOS = {
    "下行": dict(services=(.02,.01,.34,.30), cloud=(.10,.06,.22,.22), losses=(28,32),
               eps_growth=.03, near_pe=17, perpetuity=.02, probability=.25),
    "基准": dict(services=(.07,.05,.41,.40), cloud=(.23,.14,.32,.32), losses=(34,45),
               eps_growth=.14, near_pe=25, perpetuity=.03, probability=.50),
    "上行": dict(services=(.10,.07,.45,.45), cloud=(.30,.19,.37,.38), losses=(45,65),
               eps_growth=.22, near_pe=32, perpetuity=.04, probability=.25),
}

def segment(start, assumptions):
    first, second, margin5, margin10 = assumptions
    sales5 = start * (1 + first) ** 5
    sales10 = sales5 * (1 + second) ** 5
    return (sales5, sales10), (sales5 * margin5, sales10 * margin10)

def reverse_dcf(start, rate=RATE):
    """Equity cash-flow proxy. Compare to total equity, without a separate asset add-back."""
    def pv(growth):
        flows = [start * (1 + growth) ** t for t in range(1, 11)]
        pv_flows = sum(cf / (1 + rate) ** t for t, cf in enumerate(flows, 1))
        terminal = flows[-1] * 1.03 / (rate - .03) / (1 + rate) ** 10
        return pv_flows + terminal
    low, high = -0.5, 1.5
    for _ in range(110):
        mid = (low + high) / 2
        if pv(mid) < MCAP:
            low = mid
        else:
            high = mid
    assert abs(pv(mid) - MCAP) < 1e-6
    return mid

def operating_dcf(profit5, profit10, conversion5, conversion10):
    """Ten annual operating cash flows plus terminal value and current financial assets."""
    pv = 0
    for year in range(1, 11):
        if year <= 5:
            start, end = NOPAT, profit5
            cash_start, cash_end, elapsed = 19.747 / NOPAT, conversion5, year
        else:
            start, end = profit5, profit10
            cash_start, cash_end, elapsed = conversion5, conversion10, year - 5
        profit = start * (end / start) ** (elapsed / 5)
        cash_ratio = cash_start + (cash_end - cash_start) * elapsed / 5
        pv += profit * cash_ratio / (1 + RATE) ** year
    terminal = profit10 * 1.03 * exit_pe(ROIC, .03, RATE)[0]
    return (pv + terminal / (1 + RATE) ** 10 + NET_ASSETS) / SHARES

def tool(name, *args):
    subprocess.run([sys.executable, str(ROOT / "tools" / name), *map(str,args)], check=True)

def run():
    audit = ("audit","--currency","USD","--r",RATE,"--roic",ROIC,"--g","0.02,0.03,0.04",
             "--rf",.0495,"--beta",1,"--discrete-risks","AI入口流失:情景,监管执行:情景,客户违约:情景,系统性能源中断:未建模")
    tool("terminal_value.py", *audit)
    for field, first, second, unit in [
        ("FY25 revenue",402.836,402.836,"USD bn"),("FY25 net income",132.170,132.170,"USD bn"),
        ("September cash and marketable securities",265.098,265.098,"USD bn"),
        ("TTM FCF",19.747,19.747,"USD bn"),("filing date shares",12.294,12.294,"bn shares"),
        ("TTM revenue",471.097,471.098,"USD bn")]:
        tool("financial_rigor.py","cross-validate","--field",field,"--values",
             json.dumps({"SEC":first,"StockAnalysis":second}),"--unit",unit)
    tool("financial_rigor.py","verify-market-cap","--price",PRICE,"--shares",SHARES * 1e9,
         "--reported",3.44e12,"--currency","USD")
    tool("financial_rigor.py","verify-valuation","--price",PRICE,"--eps",19.15,
         "--bvps",53.65,"--fcf-per-share",19.747/SHARES,"--dividend",.88)
    tool("financial_rigor.py","three-scenario","--price",PRICE,"--shares",SHARES*10,"--eps",EPS,
         "--growth",.22,.14,.03,"--pe",32,25,17,"--years",3,"--currency","USD")
    anchors = []
    print("mcap, net assets, assets/share, NOPAT, EPS:", MCAP, NET_ASSETS, NET_ASSETS/SHARES, NOPAT, EPS)
    print("P/S, adjusted operating multiple, adjusted EV/S:", MCAP/471.097,
          (MCAP-NET_ASSETS)/NOPAT,(MCAP-NET_ASSETS)/471.097)
    print("Annualized dividend yield, FCF yield:", .88/PRICE, 19.747/MCAP)
    print("reverse DCF [9,10,11%]:", {base:[reverse_dcf(base,r) for r in (.09,.10,.11)] for base in (19.747,100.)})
    for label, spec in SCENARIOS.items():
        sales_s, profits_s = segment(376.341, spec["services"])
        sales_c, profits_c = segment(93.169, spec["cloud"])
        earnings = [(s+c-loss)*(1-TAX) for s,c,loss in zip(profits_s,profits_c,spec["losses"])]
        if label == "基准":
            for c5, c10 in [(.30, .50), (.45, .65), (.60, .80)]:
                print("Year 5/10 cash conversion, operating DCF/share:", c5, c10,
                      operating_dcf(*earnings, c5, c10))
        eps3 = EPS * (1+spec["eps_growth"])**3
        operating_target = eps3 * spec["near_pe"]
        pv = operating_target/(1+RATE)**3 + NET_ASSETS/SHARES
        terminal_pe = exit_pe(ROIC, spec["perpetuity"], RATE)[0]
        tool("terminal_value.py","pe","--roic",ROIC,"--g",spec["perpetuity"],"--r",RATE)
        tool("terminal_value.py","irr","--profit",earnings[-1],"--mcap",MCAP,
             "--pe",terminal_pe,"--years",10,"--payout",0)
        anchors.append(100*irr_from_terminal(earnings[-1],MCAP,terminal_pe))
        print(label, "sales S/C:",sales_s,sales_c,"NOPAT:",earnings,"three-year EPS, exit and PV:",
              eps3,operating_target,pv,"margin vs PV:",1-PRICE/pv,flush=True)
    print("expected terminal-only return:",sum(s["probability"]*v for s,v in zip(SCENARIOS.values(),anchors)))
    print("10% return terminal hurdle, base PE without interim distributions:",MCAP*(1+RATE)**10/exit_pe(ROIC,.03,RATE)[0])
    for delta in (.02,.01):
        tool("terminal_value.py","flip","--name","Alphabet","--roic",ROIC,"--g",".02,.03,.04",
             "--p",".25,.50,.25","--irr10="+",".join(map(str,anchors)),"--k",0,"--r",RATE,
             "--delta",delta,"--currency","USD","--g-shift",0,"--rf",.0495)
    tool("terminal_value.py", *audit)

if __name__ == "__main__":
    run()
