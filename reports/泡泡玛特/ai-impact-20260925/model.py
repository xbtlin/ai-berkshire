"""Reproduce the report. All money is RMB 100m unless explicitly labelled.
Run from any directory; writes model-results.json and financial-rigor.txt here.
Assumptions are scenarios, not company guidance. No network calls.
"""
from decimal import Decimal as D, getcontext
from pathlib import Path
import json
import subprocess
import sys

getcontext().prec = 28
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
RIGOR = ROOT / 'tools/financial_rigor.py'
def d(s): return D(str(s))
def cli(*args):
    return subprocess.check_output([sys.executable, str(RIGOR), *map(str,args)], text=True)

shares = d('13.31779203')
fx = d('.86054')  # CNY per HKD, official fixing 2026-09-24, not closing spot
price = d('151.1')
tax = d('.25')
attribution = d('.988')  # incremental profit attributable to parent, assumption
rows = []
for year,r,m,s,g,c,i in [
    (2027,'430','.275','.004','.002','.001','.0015'),
    (2028,'480','.27','.007','.004','.0015','.0015'),
    (2029,'535','.265','.01','.008','.0025','.0025')]:
    r,m,s,g,c,i = map(d,(r,m,s,g,c,i))
    bridge = dict(savings=r*s, sales_contribution=r*g, competition=-r*c, implementation=-r*i)
    pretax = sum(bridge.values())
    ai = pretax*(1-tax)*attribution
    rows.append(dict(year=year, revenue_without_incremental_ai=r, net_margin_without_incremental_ai=m,
                     non_ai_profit=r*m, **bridge, ai_pretax=pretax, ai_net_parent=ai,
                     total_profit=r*m+ai, ai_uplift=ai/(r*m)))
last = rows[-1]
scenarios2036 = []
for name,r,m,ai in [('bear',400,'.15',-5),('base',900,'.25',7),('bull',1500,'.28',20),('decline_tail',200,'.10',-3)]:
    r,m,ai = map(d,(r,m,ai))
    scenarios2036.append(dict(name=name,revenue=r,all_in_net_margin=m,net_profit=r*m,
                             embedded_ai_net=ai,profit_without_incremental_ai=r*m-ai,
                             revenue_cagr_from_2026=(r/d(390))**(d(1)/10)-1))
market_cap_hkd = shares*price
market_cap_cny = market_cap_hkd*fx
ttm_profit = d('127.75689')+d('50.38384')-d('45.74368')
ttm_revenue = d('371.20052')+d('171.72921')-d('138.76276')
valuation = dict(market_cap_hkd=market_cap_hkd,market_cap_cny=market_cap_cny,
                ttm_profit=ttm_profit,ttm_revenue=ttm_revenue,pe_ttm=market_cap_cny/ttm_profit,
                pe_2026=market_cap_cny/110,pe_2027=market_cap_cny/rows[0]['total_profit'],
                ps_ttm=market_cap_cny/ttm_revenue,pb=market_cap_cny/d('230.59024'),
                fair_value_2027={str(pe):rows[0]['total_profit']*pe/shares/fx for pe in [10,12,15,18,20]})
stress = dict(one_point_net_margin=last['revenue_without_incremental_ai']*d('.01'),
    price_down_3pct=last['revenue_without_incremental_ai']*d('.03')*(1-tax)*attribution,
    monster_down_30pct=last['revenue_without_incremental_ai']*d('.26')*d('.30')*d('.45')*(1-tax)*attribution,
    inventory_extra_10pct=d('61.01530')*d('.10')*(1-tax)*attribution)
result = dict(units='RMB 100m; HKD values explicitly labelled',cutoff='2026-09-24',
    assumptions=dict(tax=tax,attribution=attribution,shares_100m=shares,cny_per_hkd=fx),
    base2026=dict(revenue=390,profit=110,h2_revenue=d(390)-d('171.72921'),h2_profit=d(110)-d('50.38384')),
    ai_bridge=rows,ai_3year_total=sum(x['ai_net_parent'] for x in rows),
    ai2029_sensitivity={str(rate):d(535)*d(rate) for rate in ['-.01','.009633','.02']},
    scenarios2036=scenarios2036,valuation=valuation,stress=stress,
    cash2026h1=dict(cfo=d('36.37324'),capex_ppe=d('6.73560'),capex_intangibles=d('.50579'),lease_payment=d('5.02889'),
        fcf_before_lease=d('36.37324')-d('6.73560')-d('.50579'),
        cash_after_lease=d('36.37324')-d('6.73560')-d('.50579')-d('5.02889')),
    ratios=dict(roe2025=d('127.75689')/((d('222.77735')+d('106.83505'))/2),
                roa2025=d('130.12042')/((d('321.01354')+d('148.70672'))/2)))
HERE.joinpath('model-results.json').write_text(json.dumps(result,ensure_ascii=False,indent=2,default=str)+'\n')
logs=[]
logs.append(cli('verify-market-cap','--price',price,'--shares','1331779203','--reported','201232000000','--currency','HKD'))
for field,values in [('2025 revenue',{'HKEX':371.20052,'StockAnalysis':371.20}),
                     ('2025 parent profit',{'HKEX':127.75689,'StockAnalysis':127.76}),
                     ('2026 H1 revenue',{'HKEX':171.72921,'ETNet':171.73}),
                     ('2026 H1 parent profit',{'HKEX':50.38384,'ETNet':50.38}),
                     ('2026 H1 cash',{'HKEX':124.42065,'ETNet':124.42})]:
    logs.append(cli('cross-validate','--field',field,'--values',json.dumps(values),'--unit','亿元'))
logs.append(cli('verify-valuation','--price',price,'--eps',ttm_profit/shares/fx,'--bvps',d('230.59024')/shares/fx))
for expr in ['535 * (0.01 + 0.008 - 0.0025 - 0.0025) * 0.75 * 0.988','900 * 0.25','400 * 0.15','1500 * 0.28']:
    logs.append(cli('calc','--expr',expr))
# Actual 2029 scenarios: 240, base result, 75. Constant shares and exchange rate.
growth=[(p/d(110))**(d(1)/3)-1 for p in [d(240),last['total_profit'],d(75)]]
logs.append(cli('three-scenario','--price',price,'--eps',d(110)/shares/fx,'--shares',shares,
                '--growth',*growth,'--pe',24,18,10,'--years',3,'--currency','HKD'))
HERE.joinpath('financial-rigor.txt').write_text('\n'.join(logs))
print(json.dumps(result,ensure_ascii=False,indent=2,default=str))
