"""Kuaishou scenarios; future numbers are assumptions, not company guidance.
Units RMB 100m. Normalized earnings attributable to parent retain SBC/depreciation.
Run with Python stdlib. Outputs next to this file. No network dependencies.
"""
from decimal import Decimal as D, getcontext
from pathlib import Path
import json
getcontext().prec=28
P=Path(__file__).resolve().parent
def d(v): return D(str(v))
def clean(v):
    if isinstance(v,D): return str(v)
    if isinstance(v,dict): return {k:clean(x) for k,x in v.items()}
    if isinstance(v,list): return [clean(x) for x in v]
    return v
# Core baseline freezes AI capability at 2026; excludes Kling entirely.
A={
'bear':dict(growth=['-.01','-.08','.01'],margin=['.115','.11','.105'],uplift=['.005','.01','.015'],fee_uplift=['0','.005','.01'],savings=[6,10,14],retain='.40',ai_cost=[16,22,28],k_rev=[45,60,75],k_cm=['.30','.35','.40'],k_fixed=[60,65,70],tax='.20',finance=[8,8,8],terminal=[900,220,380,'.10',-30,150,'.30',70,'.55',10],pe=8),
'base':dict(growth=['.03','-.04','.06'],margin=['.13','.14','.15'],uplift=['.02','.035','.05'],fee_uplift=['.02','.03','.04'],savings=[10,18,26],retain='.70',ai_cost=[14,18,23],k_rev=[65,105,160],k_cm=['.50','.55','.60'],k_fixed=[58,66,76],tax='.15',finance=[10,10,10],terminal=[1250,300,400,'.18',45,500,'.50',150,'.65',20],pe=12),
'bull':dict(growth=['.07','0','.10'],margin=['.145','.16','.18'],uplift=['.03','.06','.09'],fee_uplift=['.03','.05','.07'],savings=[15,28,42],retain='.80',ai_cost=[15,22,30],k_rev=[85,170,300],k_cm=['.50','.58','.65'],k_fixed=[65,85,115],tax='.20',finance=[12,15,18],terminal=[1700,350,550,'.23',80,1200,'.60',360,'.6833',25],pe=16)}
def k_net(op): return op*d('.80') if op>0 else op # No unrecognized loss tax shield.
def row(y,adv,live,fee,margin,aiop,kr,kcm,kfix,share,tax,fin,ai_revenue=0):
    core=adv+live+fee; kop=kr*kcm-kfix
    core_net=(core*margin+aiop+fin)*(1-tax)
    no_new_ai=(core*margin+fin)*(1-tax)+d(-30)*share
    net=core_net+k_net(kop)*share
    return dict(year=y,advertising_baseline=adv,live=live,fees_baseline=fee,core_baseline_revenue=core,incremental_core_ai_revenue=d(ai_revenue),consolidated_revenue=core+kr+d(ai_revenue),core_baseline_margin=margin,core_ai_operating=aiop,core_net=core_net,kling_revenue=kr,kling_contribution_margin=kcm,kling_fixed_cost=kfix,kling_operating=kop,kling_net=k_net(kop),kling_share=share,kling_attributable=k_net(kop)*share,finance=fin,core_tax=tax,net=net,no_new_ai_net=no_new_ai,incremental_ai_net=net-no_new_ai)
R={'cutoff':'2026-09-24','unit':'RMB 100 million','inputs':A,'definitions':{'net':'normalized attributable earnings; recurring SBC and depreciation retained; excludes one-off fair values, restructuring and uncertain redemption accounting','ai_counterfactual':'core AI frozen at 2026 and Kling standalone annual loss frozen at RMB3bn; future equity share same in both cases; not a world without AI','contribution_margin':'Kling after inference, delivery support, channel and usage-dependent depreciation; fixed costs include training, product, sales, admin, SBC and non-usage depreciation; no internal sales'},'scenarios':{}}
# Full-year illustrative anchor, NOT extrapolation of actual H1 nor segment disclosure.
R['anchor2026']=row(2026,d(835),d(345),d(205),d('.125'),d(0),d(35),d('.45'),d('45.75'),d(1),d('.15'),d(10))
for name,p in A.items():
    adv,live,fee=map(d,[835,345,205]); rows=[]
    for i,y in enumerate(range(2027,2030)):
        adv*=1+d(p['growth'][0]);live*=1+d(p['growth'][1]);fee*=1+d(p['growth'][2])
        ad_extra=adv*d(p['uplift'][i]); fee_extra=fee*d(p['fee_uplift'][i])
        ad_op=ad_extra*d('.65');fee_op=fee_extra*d('.60');saving=d(p['savings'][i]);retain=d(p['retain'])
        gross=ad_op+fee_op+saving; leakage=gross*(1-retain); aiop=gross*retain-d(p['ai_cost'][i])
        r=row(y,adv,live,fee,d(p['margin'][i]),aiop,d(p['k_rev'][i]),d(p['k_cm'][i]),d(p['k_fixed'][i]),d('.6833'),d(p['tax']),d(p['finance'][i]),ad_extra+fee_extra)
        r['ai_bridge']=dict(ad_revenue=ad_extra,fee_revenue=fee_extra,ad_contribution=ad_op,fee_contribution=fee_op,saving=saving,competitive_leakage=leakage,extra_core_ai_cost=d(p['ai_cost'][i]),ai_core_net=aiop*(1-d(p['tax'])),kling_improvement_same_share=(k_net(r['kling_operating'])+30)*d('.6833'))
        rows.append(r)
    ta,tl,tf,tm,tai,tkr,tcm,tkf,ts,tfin=map(d,p['terminal'])
    terminal=row(2036,ta,tl,tf,tm,tai,tkr,tcm,tkf,ts,d(p['tax']),tfin)
    # terminal core totals already include all AI-supported sales, aiop is cost/mix effect only
    terminal['core_revenue_definition']='inclusive of AI-supported sales; terminal aiop is incremental efficiency/mix only'
    terminal['core_revenue_cagr10']=(terminal['core_baseline_revenue']/d(1385))**(d(1)/10)-1
    terminal['kling_revenue_cagr10']=(tkr/d(35))**(d(1)/10)-1
    terminal['net_cagr10']=(terminal['net']/R['anchor2026']['net'])**(d(1)/10)-1
    terminal['real_net_at_2pct_inflation']=terminal['net']/(d('1.02')**10)
    # Conditional per-share illustration, fixed diluted count and FX assumptions.
    price=rows[-1]['net']/d(44)*d('1.10')*p['pe']
    R['scenarios'][name]=dict(annual=rows,terminal2036=terminal,ai_increment_three_years=sum(r['incremental_ai_net'] for r in rows),valuation=dict(shares_100m_assumption=44,hkd_per_rmb_assumption='1.10',pe=p['pe'],price_2029=price,present_at12pct=price/(d('1.12')**d('3.25'))))
b=R['scenarios']['base']; terminal=b['terminal2036']; end=b['annual'][-1]
R['sensitivities']={'base2036_core_margin_minus3pp':terminal['net']-d(1950)*d('.03')*d('.85'),'base2036_kling_zero_profit':terminal['net']-terminal['kling_attributable'],'base2036_kling_share55pct':terminal['net']-d(100)*d('.8')*d('.10'),'base2036_kling_cm_minus10pp':terminal['net']-d(500)*d('.10')*d('.8')*d('.65'),'base2029_kling_revenue_breakeven':d(76)/d('.60'),'base2029_kling_cm_minus10pp':end['net']-d(160)*d('.10')*d('.8')*d('.6833'),'base2029_kling_revenue_minus25pct':end['core_net']+k_net(d(120)*d('.6')-76)*d('.6833'),'severe2036_tail':d(900)*d('.05')*d('.8')-d(50)*d('.4')}
R['audit_math']={'h1_fcf':d('90.44')-d('179.41'),'prior_h1_fcf':d('117.81')-d('70.75'),'h1_attributable_yoy':d('60.49')/d('89.00')-1,'h1_rd_yoy':d('82.02')/d('66.98')-1,'dau_mau2026':d('412.3')/d('797.3'),'dau_mau2025':d('408.9')/d('714.8'),'dilution_loss_sharing_effect_not_ai':d(30)*(1-d('.6833')),'equity_share':d('.6633')+d('.02')}
(P/'model-results.json').write_text(json.dumps(clean(R),ensure_ascii=False,indent=2)+'\n')
print(json.dumps(clean({'anchor':R['anchor2026']['net'],'scenarios':{k:{'profits':[r['net'] for r in v['annual']],'ai':[r['incremental_ai_net'] for r in v['annual']],'2036':v['terminal2036']['net'],'valuation':v['valuation']} for k,v in R['scenarios'].items()},'sensitivities':R['sensitivities']}),ensure_ascii=False,indent=2))
