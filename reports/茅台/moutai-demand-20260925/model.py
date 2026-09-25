"""Moutai demand scenarios; all forecasts are analyst assumptions, not guidance.
Run from any directory. Outputs are deterministic; no network/dependencies.
Currency: RMB 100 million; volume: tonnes; ASP: RMB 10,000/tonne.
"""
from decimal import Decimal as D, getcontext
from pathlib import Path
import json

getcontext().prec = 28
OUT = Path(__file__).resolve().parent
SHARES = D('12.50081601')  # 2026H1 disclosed shares, hundred million
INPUTS = {
    '2026E': [48000, 312, 40000, '53.5', '.48'],
    '2027E': [48000, 318, 39000, 54, '.48'],
    '2028E': [48500, 324, 39500, '55.5', '.4825'],
    '2029E': [49000, 330, 40000, 57, '.485'],
    '2036_bear': [40000, 280, 28000, 45, '.42'],
    '2036_base': [52000, 380, 40000, 65, '.49'],
    '2036_bull': [62000, 480, 48000, 85, '.51'],
}

def compute(vals):
    q, p, sq, sp, m = map(lambda x: D(str(x)), vals)
    mr, sr = q*p/D(10000), sq*sp/D(10000)
    revenue = mr+sr+D('.63')  # immaterial other revenue held flat
    profit = revenue*m  # attributable profit / operating revenue convention
    return dict(moutai_tonnes=q, moutai_asp_wan=p, series_tonnes=sq,
                series_asp_wan=sp, attributable_margin=m,
                moutai_revenue=mr, series_revenue=sr, other_revenue=D('.63'),
                revenue=revenue, attributable_profit=profit, eps=profit/SHARES)

results = {k: compute(v) for k,v in INPUTS.items()}
for k in ('2036_bear','2036_base','2036_bull'):
    r = results[k]
    r['profit_cagr_2026_2036'] = (r['attributable_profit']/results['2026E']['attributable_profit'])**D('.1')-1
    r['real_profit_2026_purchasing_power_at_2pct_inflation'] = r['attributable_profit']/D('1.02')**10
    r['moutai_volume_share_multiplier_if_industry_75'] = (r['moutai_tonnes']/D(48000))/D('.75')

sensitivity = {}
for name,vals in {
    'base_price_minus_10pct': [52000,342,40000,65,'.49'],
    'base_volume_minus_10pct': [46800,380,40000,65,'.49'],
    'base_margin_45pct': [52000,380,40000,65,'.45'],
    'base_moutai_asp_frozen_at_2026': [52000,312,40000,65,'.49'],
}.items():
    sensitivity[name] = compute(vals)['attributable_profit']

valuation = []
for price in (900,1000,1100,1200,1237,1300):
    p=D(price); n=results['2026E']['attributable_profit']
    valuation.append(dict(price=p, cap_yi=p*SHARES, pe_2026E=p*SHARES/n,
                          yield_at_assumed_75pct_payout=n*D('.75')/(p*SHARES)))

old_mr = D('1464.9990648049') * D('1.02')**11 * D('1.03')**11
old_sr = D('222.7467870716') * D('1.03')**11
bridge = {
    'old_base_profit_recomputed': (old_mr+old_sr+D('.63'))*D('.49'),
    'volume_change_profit_impact': (D(52000)-D('46750.66')*D('1.02')**11)*(D('1464.9990648049')*10000/D('46750.66')*D('1.03')**11)/10000*D('.49'),
    'new_base_profit': results['2036_base']['attributable_profit'],
}
payload = {'scope':'2036 annual attributable net profit; 2026E is an assumption, not annualised H1',
           'inputs':INPUTS,'results':results,'sensitivity':sensitivity,'valuation':valuation,
           'comparison_20260907':bridge}
(OUT/'model-results.json').write_text(json.dumps(payload,ensure_ascii=False,indent=2,default=str)+'\n')
for k,v in results.items():
    print(k, 'revenue',round(v['revenue'],2),'profit',round(v['attributable_profit'],2),'EPS',round(v['eps'],2))
print('sensitivity',sensitivity)
print('valuation',valuation)
print('old_base',bridge)
