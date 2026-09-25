"""Reproducible research scenarios, RMB 100 million; assumptions, not guidance."""
from decimal import Decimal as D, getcontext
from pathlib import Path
import json

getcontext().prec = 32
OUT = Path(__file__).resolve().parent

def ds(values):
    return [D(str(v)) for v in values]

near_inputs = {
    "bear": {"growth": ".03", "ad": [60,120,180], "game": [20,40,60],
        "cloud": [10,20,40], "efficiency": [20,35,50], "infra": [80,160,240], "new_ai_loss": [650,750,800]},
    "base": {"growth": ".07", "ad": [130,260,410], "game": [60,120,190],
        "cloud": [35,75,140], "efficiency": [45,80,115], "infra": [50,100,150], "new_ai_loss": [520,420,250]},
    "bull": {"growth": ".10", "ad": [180,380,620], "game": [90,180,300],
        "cloud": [60,140,260], "efficiency": [60,110,170], "infra": [50,100,150], "new_ai_loss": [450,200,-100]},
}
profit2026 = D(2800)
loss2026 = D(450)
conversion = D('.8')
core2026 = profit2026 + loss2026 * conversion
near = {}
for name, a in near_inputs.items():
    rows = []
    for i, year in enumerate([2027,2028,2029]):
        core = core2026 * (1 + D(a['growth'])) ** (i + 1)
        frozen = core - loss2026 * conversion
        benefits = sum(D(a[k][i]) for k in ['ad','game','cloud','efficiency'])
        total_ai_vs_ex_new = (benefits-D(a['infra'][i])-D(a['new_ai_loss'][i]))*conversion
        total = core + total_ai_vs_ex_new
        rows.append(dict(year=year, core_ex_new_ai=core, frozen_ai_profit=frozen,
            benefits_pretax=benefits, ai_delta_vs_frozen=total-frozen,
            ai_vs_core_ex_new=total_ai_vs_ex_new, profit=total))
    near[name] = rows

# Long-term revenue and operating margin AFTER segment expenses/depreciation;
# group-level central cost is additionally subtracted once.
segments = ['domestic_games','international_games','social','advertising','fintech','cloud_ai','other']
revenue2026 = ds([1900,800,1300,1800,1850,600,100])
long_inputs = {
    'bear': {'revenues':[2600,1400,1400,3000,2500,1700,150], 'margins':['.32','.24','.22','.32','.20','.08','.05'], 'central':300, 'associate_net':150},
    'base': {'revenues':[3800,2300,1800,5200,3500,2500,200], 'margins':['.43','.35','.30','.48','.30','.18','.10'], 'central':350, 'associate_net':250},
    'bull': {'revenues':[4800,3200,2100,8000,4300,5000,300], 'margins':['.48','.40','.34','.52','.33','.25','.10'], 'central':600, 'associate_net':400},
}
long = {}
for name, a in long_inputs.items():
    rev, margin = ds(a['revenues']), ds(a['margins'])
    op = [r*m for r,m in zip(rev,margin)]
    group_op = sum(op)-D(a['central'])
    p = group_op*conversion+D(a['associate_net'])
    long[name] = dict(segments=[dict(segment=s,revenue=r,margin=m,op=o,
        revenue_cagr=(r/r0)**D('.1')-1) for s,r,m,o,r0 in zip(segments,rev,margin,op,revenue2026)],
        revenue=sum(rev), segment_op=sum(op), central=D(a['central']), group_op=group_op,
        associate_net=D(a['associate_net']), profit=p, profit_cagr=(p/profit2026)**D('.1')-1,
        net_margin=p/sum(rev), post2029_cagr=(p/near[name][2]['profit'])**(D(1)/7)-1)

# Owner-earnings proxies: explicitly assumed recurring SBC and net maintenance
# capital burden; these are NOT forecasts of statutory IFRS adjustments or FCF.
owner = {name:long[name]['profit']-D(sbc)-D(maintenance)
    for name,sbc,maintenance in [('bear',250,250),('base',300,300),('bull',450,450)]}
sens = {'2029_base_ad_half':near['base'][2]['profit']-D(410)*D('.5')*conversion,
    '2029_new_ai_loss_600':near['base'][2]['profit']-(D(600)-D(250))*conversion,
    '2029_both':near['base'][2]['profit']-D(410)*D('.5')*conversion-(D(600)-D(250))*conversion,
    '2036_ad_revenue_minus_20pct':long['base']['profit']-D(5200)*D('.2')*D('.48')*conversion,
    '2036_all_segment_margin_minus_5pp':long['base']['profit']-long['base']['revenue']*D('.05')*conversion,
    '2036_cloud_margin_zero':long['base']['profit']-D(2500)*D('.18')*conversion,
    '2036_base_real_2026_rmb_at_2pct_inflation':long['base']['profit']/D('1.02')**10}
tax_conversion_sensitivity = {}
for c in ds(['.7','.8','1']):
    # Recalibrate 2026 core so the same observed/estimated 2800 anchor is held fixed.
    recalibrated_core=profit2026+loss2026*c
    p=recalibrated_core*D('1.07')**3+(D(855)-D(150)-D(250))*c
    tax_conversion_sensitivity[str(c)]=p
result = dict(unit='RMB 100 million', cutoff='2026-09-24',
    anchor=dict(profit2026=profit2026,new_ai_loss2026=loss2026,conversion=conversion,core2026=core2026),
    near_inputs=near_inputs, near=near, long_inputs=long_inputs, revenue2026_analytical_allocation=revenue2026,
    long=long,owner_earnings_proxy=owner,sensitivity=sens,tax_conversion_sensitivity=tax_conversion_sensitivity)
def convert(x):
    if isinstance(x,D): return str(x)
    raise TypeError(type(x).__name__)
(OUT/'model-results.json').write_text(json.dumps(result,ensure_ascii=False,indent=2,default=convert)+'\n')
for name in near:
    print(name, '2027-29:', ', '.join(f"{r['profit']:.2f}" for r in near[name]),
          '2036:',f"{long[name]['profit']:.2f}", '10Y CAGR:',f"{long[name]['profit_cagr']*100:.2f}%")
print('Base AI uplift:',[str(r['ai_delta_vs_frozen']) for r in near['base']])
print('Sensitivity:',json.dumps(sens,default=convert))
