"""PDD scenario model. All forward inputs are research assumptions, not guidance.

Units: RMB 100 million, except USD/ADS, ADS count (100 million), ratios.
Run from any directory; writes model-results.json alongside this script.
"""
from decimal import Decimal as D, getcontext
from pathlib import Path
import json

getcontext().prec = 28
ROOT = Path(__file__).resolve().parent
def d(x): return D(str(x))
def clean(x):
    if isinstance(x, D): return str(x)
    if isinstance(x, dict): return {k: clean(v) for k, v in x.items()}
    if isinstance(x, list): return [clean(v) for v in x]
    return x

inputs = {
    "bear": {"growth": ["0", ".04"], "margins": [".175", ".17", ".165"], "ai": [-10,-15,-25], "finance": [100,110,120], "tax": ".25", "pe2029": 8,
             "terminal": [2600,3000,".14",-50,100]},
    "base": {"growth": [".06", ".12"], "margins": [".21", ".215", ".22"], "ai": [10,35,65], "finance": [120,130,140], "tax": ".22", "pe2029": 12,
             "terminal": [4000,5000,".215",180,140]},
    "bull": {"growth": [".10", ".18"], "margins": [".23", ".24", ".25"], "ai": [30,80,150], "finance": [150,170,190], "tax": ".20", "pe2029": 16,
             "terminal": [5500,8000,".25",350,200]},
}
def row(year, marketing, transaction, margin, ai, finance, tax):
    revenue=marketing+transaction
    pre_ai_op=revenue*margin
    op=pre_ai_op+ai
    no_ai_net=(pre_ai_op+finance)*(1-tax)
    net=(op+finance)*(1-tax)
    return {"year":year,"marketing":marketing,"transaction":transaction,"revenue":revenue,
            "pre_ai_op_margin":margin,"ai_op":ai,"op":op,"op_profit_over_base_revenue":op/revenue,
            "finance_pre_tax":finance,"tax":tax,"net_no_ai":no_ai_net,"ai_net":ai*(1-tax),
            "net":net,"net_profit_over_base_revenue":net/revenue}

results={"cutoff":"2026-09-24","units":"RMB亿元; valuation USD/ADS","definitions":{"revenue":"counterfactual baseline revenue excluding incremental AI commercialization", "profit_ratios":"AI-inclusive profits divided by counterfactual baseline revenue, not GAAP margins", "ai_cost_pools":"baseline volume only; incremental sales variable costs included in contribution rate; separate AI operating expenses deducted once", "net":"normalized attributable earnings with recurring SBC and depreciation retained; not exact future GAAP"},"inputs":inputs,"scenarios":{}}
results["anchor_2026E"]=row(2026,d(2250),d(2450),d('.21'),d(0),d(100),d('.22'))
for name,p in inputs.items():
    m,t=d(2250),d(2450)
    rows=[]
    for i,year in enumerate(range(2027,2030)):
        m*=1+d(p['growth'][0]); t*=1+d(p['growth'][1])
        rows.append(row(year,m,t,d(p['margins'][i]),d(p['ai'][i]),d(p['finance'][i]),d(p['tax'])))
    tm,tt,margin,ai,finance=p['terminal']
    terminal=row(2036,d(tm),d(tt),d(margin),d(ai),d(finance),d(p['tax']))
    terminal['revenue_cagr_2026_2036']=(terminal['revenue']/d(4700))**(d(1)/10)-1
    terminal['net_cagr_2026_2036']=(terminal['net']/results['anchor_2026E']['net'])**(d(1)/10)-1
    terminal['marketing_cagr_2029_2036']=(d(tm)/m)**(d(1)/7)-1
    terminal['transaction_cagr_2029_2036']=(d(tt)/t)**(d(1)/7)-1
    price=rows[-1]['net']/d('14.8')/d(7)*d(p['pe2029'])
    valuation={"ads_100m":d('14.8'),"rmb_per_usd":d(7),"pe":p['pe2029'],"price_2029":price,
               "price_only_annual_return_3_25yr":(price/d('79.2'))**(d(1)/d('3.25'))-1,
               "present_value_at_12pct":price/((1+d('.12'))**d('3.25'))}
    results['scenarios'][name]={"annual":rows,"2036":terminal,"valuation":valuation}

base=results['scenarios']['base']
results['ai_bridge_2029']={"marketing_basis":base['annual'][-1]['marketing'],
    "marketing_uplift":base['annual'][-1]['marketing']*d('.04')*d('.65'),
    "support_saving":d(180)*d('.15'),"creative_saving":d(100)*d('.15'),"fulfillment_saving":d(800)*d('.02')}
b=results['ai_bridge_2029']
gross=sum(b[k] for k in ['marketing_uplift','support_saving','creative_saving','fulfillment_saving'])
b.update({"gross":gross,"competitive_leakage":gross*d('.30'),"new_ai_cost":d(25),
          "net_operating":gross*d('.70')-25,"net_after_tax":(gross*d('.70')-25)*d('.78'),
          "model_rounded_ai_operating":d(65)})
results['base_ai_net_three_year_sum']=sum(r['ai_net'] for r in base['annual'])
results['sensitivity_2036']=[{"revenue":d(rev),"net_margin":d(margin),"net":d(rev)*d(margin)} for rev in [7500,9000,10500] for margin in ['.16','.20','.24']]
results['ai_sensitivity_2036']=[{"ai_op":d(ai),"net":(d(9000)*d('.215')+d(ai)+140)*d('.78')} for ai in [0,90,180,270]]
results['audit_math']={
    "2025_net_adjustment":d('993.64469')-d('978.42539'),
    "ads_issued_100m":d('5693585848')/4/d('1e8'),
    "closing_market_cap_usd_100m":d('79.2')*d('5693585848')/4/d('1e8'),
    "cash_short_investments":d('1289.18')+d('3274.96'),
    "cash_less_leases":d('4564.14')-d('48.44'),
    "cash_less_all_liabilities":d('4564.14')-d('2156.20'),
    "ttm_net":d('978.42539')-d('454.96')+d('397.29'),
    "ttm_op":d('931.02131')-d('418.79')+d('473.30'),
    "ttm_revenue":d('4318.45713')-d('1996.57')+d('2185.87'),
    "2029_base_margin_1pp_aftertax":base['annual'][-1]['revenue']*d('.01')*d('.78'),
    "2036_base_margin_1pp_aftertax":d(9000)*d('.01')*d('.78'),
    "2036_base_real_net_2026RMB_at_2pct_inflation":base['2036']['net']/(d('1.02')**10),
    "2036_base_2pct_dilution_relative_eps":1/(d('1.02')**10),
}
(ROOT/'model-results.json').write_text(json.dumps(clean(results),ensure_ascii=False,indent=2)+'\n')
print(json.dumps(clean({k:{"net":[r['net'] for r in v['annual']],"2036":v['2036']['net'],"valuation":v['valuation']} for k,v in results['scenarios'].items()}),ensure_ascii=False,indent=2))
