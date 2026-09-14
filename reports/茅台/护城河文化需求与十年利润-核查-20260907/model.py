"""Reproduce research arithmetic; scenario inputs are assumptions, not guidance."""
from decimal import Decimal as D, getcontext
import json
from pathlib import Path
import subprocess
import sys

getcontext().prec = 40
OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[2]
TOOL = ROOT / "tools/financial_rigor.py"
ANNUAL = "https://www.moutaichina.com/mtgf/articleFileDir/2026-04/17/07cf01cc11a14ea18cfadf9ebe2a4eb3.pdf"
HALF = "https://static.cninfo.com.cn/finalpage/2026-08-15/1225475868.PDF"
MEDIA25 = "https://finance.eastmoney.com/a/202604173708539018.html"
SEG25 = "https://www.nbd.com.cn/articles/2026-04-16/4343145.html"
MEDIA26 = "https://finance.sina.com.cn/stock/aiassist/yjbg/2026-08-14/doc-ininhxpi2824915.shtml"

checks = [
    ("2025营业收入", "1688.3810251479", "1688.38", "亿元", ANNUAL, MEDIA25),
    ("2025归母净利润", "823.2006710168", "823.20", "亿元", ANNUAL, MEDIA25),
    ("2025茅台酒收入", "1464.9990648049", "1465", "亿元", ANNUAL, SEG25),
    ("2025系列酒收入", "222.7467870716", "222.75", "亿元", ANNUAL, SEG25),
    ("2025茅台酒销量", "4.675066", "4.68", "万吨", ANNUAL, SEG25),
    ("2026H1营业收入", "907.0326096448", "907.03", "亿元", HALF, MEDIA26),
    ("2026H1归母净利润", "445.1688042186", "445.17", "亿元", HALF, MEDIA26),
]
logs = []
verified = []
for field, a, b, unit, source1, source2 in checks:
    command = [sys.executable, str(TOOL), "cross-validate", "--field", field,
               "--values", json.dumps({"公司原始财报": float(a), "独立媒体取数": float(b)}, ensure_ascii=False),
               "--unit", unit, "--tolerance", "1"]
    result = subprocess.run(command, check=True, capture_output=True, text=True)
    logs.append(result.stdout)
    error = abs(D(a)-D(b))/D(a)*100
    assert error <= 1
    verified.append(dict(field=field, primary=a, secondary=b, unit=unit,
                         deviation_percent=str(error), primary_url=source1, secondary_url=source2))

# All revenue amounts in RMB 100 million. Prices are issuer revenue per tonne,
# excluding VAT; they are not a 500 ml bottle's consumer retail price.
mt, series, total, profit = map(D, ["1464.9990648049", "222.7467870716", "1688.3810251479", "823.2006710168"])
qty = D("46750.66")
other = total-mt-series
results = {}
for name, volume, price, other_growth, margin in [
    ("悲观", "-0.01", "0", "-0.02", "0.43"),
    ("中性", "0.02", "0.03", "0.03", "0.49"),
    ("乐观", "0.03", "0.05", "0.05", "0.51"),
]:
    q, p, s, m = map(D, [volume, price, other_growth, margin])
    n = 11  # FY2025 to FY2036; the research date is September 2026.
    rmt = mt * (1+q)**n * (1+p)**n
    rs = series * (1+s)**n
    revenue = rmt + rs + other
    net = revenue*m
    expression = f"({mt}*((1+({q}))*(1+({p})))**{n}+{series}*(1+({s}))**{n}+{other})*{m}"
    calc = subprocess.run([sys.executable, str(TOOL), "calc", "--expr", expression],
                          check=True, capture_output=True, text=True)
    logs.append(calc.stdout)
    # Tool calc internally evaluates floats; the stored Decimal value is the
    # precision authority. Compare independently to a floating-point formula.
    floating = (float(mt)*((1+float(q))*(1+float(p)))**n + float(series)*(1+float(s))**n + float(other))*float(m)
    assert abs(net-D(str(floating))) < D("0.00000001")
    results[name] = {"volume_cagr":str(q), "realized_price_cagr":str(p),
                    "series_revenue_cagr":str(s), "attributable_profit_to_operating_revenue":str(m),
                    "2036_mt_sales_tonnes":str(qty*(1+q)**n),
                    "2036_mt_revenue":str(rmt), "2036_series_revenue":str(rs),
                    "2036_revenue":str(revenue), "2036_profit":str(net),
                    "profit_cagr_from_2025":str((net/profit)**(D(1)/n)-1),
                    "expression":expression}

base_rev = D(results["中性"]["2036_revenue"])
sensitivity = []
for p in [D("0.01"), D("0.02"), D("0.03"), D("0.04")]:
    for m in [D("0.45"), D("0.49"), D("0.51")]:
        net = (mt*D("1.02")**11*(1+p)**11+series*D("1.03")**11+other)*m
        sensitivity.append({"price_cagr":str(p), "margin":str(m), "2036_profit":str(net)})

metrics = {
    "2025_attributable_margin":str(profit/total*100),
    "2026H1_attributable_margin":str(D("445.1688042186")/D("907.0326096448")*100),
    "2025_mt_price_wan_per_tonne":str(mt*10000/qty),
    "2025_mt_operating_revenue_share":str(mt/total*100),
    "2025_core_yoy_realized_price_pct_from_rounded_changes":str((D("1.0039")/D("1.0073")-1)*100),
    "2025_foreign_share_alcohol_revenue":str(D("48.5014232268")/(mt+series)*100),
    "2026H1_imoutai_share_operating_revenue":str(D("402.635642")/D("907.0326096448")*100),
    "2026H1_direct_share_alcohol_revenue":str(D("519.620470")/(D("777.244379")+D("129.341865"))*100),
    "2025_to_2036_zero_volume_3pct_price_profit":str((mt*D("1.03")**11+series*D("1.03")**11+other)*D("0.49")),
    "2025_to_2036_double_profit_cagr":str(D(2)**(D(1)/11)-1),
    "2025_to_2036_3000_profit_cagr":str((D(3000)/profit)**(D(1)/11)-1),
    "base_2036_1pp_margin_profit_effect":str(base_rev*D("0.01")),
    "base_2036_profit_2026_purchasing_power_at_2pct_inflation":str(D(results["中性"]["2036_profit"])/D("1.02")**10),
}
payload = {"as_of":"2026-09-07", "base_year":2025, "target_year":2036, "periods":11,
           "units":"RMB 100 million except explicitly stated", "source_checks":verified,
           "base_other_revenue":str(other), "scenarios":results, "sensitivity":sensitivity,
           "metrics":metrics, "scope":"conditional scenarios, not statistical confidence intervals or investment recommendations"}
(OUT/"calculations.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2)+"\n")
(OUT/"financial-rigor-output.txt").write_text("\n".join(logs))
print(json.dumps({"scenarios":results,"metrics":metrics,"sensitivity":sensitivity}, ensure_ascii=False, indent=2))
