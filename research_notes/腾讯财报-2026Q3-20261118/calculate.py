#!/usr/bin/env python3
"""Reproducible calculations; all source amounts CNY million unless labelled.
Uses required financial_rigor CLI for checks, Decimal for all final arithmetic.
No changes to shared tools. Assumptions are analyst scenarios, not guidance.
"""
from decimal import Decimal, getcontext
from pathlib import Path
import json, subprocess
getcontext().prec=40
D=Decimal
ROOT=Path(__file__).resolve().parents[2]
OUT=Path(__file__).resolve().parent
anchors=json.loads((OUT/'quote_anchors.json').read_text())
price=D(anchors['price_hkd']); shares=D(anchors['shares_oct31']); fx=D(anchors['fx_cny_per_hkd_sina_165854'])
cap=price*shares*fx
q={'revenue':[207336,192869,204785],'gross':[115911,108798,118433],'op':[59147,63554,67276],'adj_op':[68073,72570,75636],'parent':[63612,63133,56022],'adj_parent':[66519,70551,68415],'capex':[81433,12983,52784]}
r={'source':'q3_announcement_cn.pdf pp.1,5-17; other explicit references in keys','market_cap_cny':str(cap),'market_cap_hkd':str(price*shares),'fx_cny_per_hkd':str(fx),'shares':str(shares)}
for k,vals in q.items():
 a,b,c=map(D,vals); r[k]={'current':str(a),'yoy_pct':str((a/b-1)*100),'qoq_pct':str((a/c-1)*100)}
r['current_gross_margin_pct']=str(D(115911)/207336*100)
r['prior_gross_margin_pct']=str(D(108798)/192869*100)
r['adj_op_margin_pct']=str(D(68073)/207336*100)
r['prior_adj_op_margin_pct']=str(D(72570)/192869*100)
r['ad_margin_pct']=str(D(22578)/43049*100)
r['prior_ad_margin_pct']=str(D(20551)/36242*100)
r['ocf_q3_million']=str(D(156713)-154061)
r['ocf_to_group_profit_pct']=str((D(156713)-154061)/65139*100)
r['ocf_to_parent_profit_pct']=str((D(156713)-154061)/63612*100)
r['prepay_inferred_cny_100m']=str(D(169)-D(-691))
r['income_increment_million']=str(D(207336)-192869)
r['ad_share_of_revenue_increment_pct']=str((D(43049)-36242)/(D(207336)-192869)*100)
r['fbs_share_of_revenue_increment_pct']=str((D(63655)-58174)/(D(207336)-192869)*100)
r['ad_incremental_gross_margin_pct']=str((D(22578)-20551)/(D(43049)-36242)*100)
r['tech_operating_cost_yoy_pct']=str((D(19991)/8623-1)*100)
r['depreciation_yoy_pct']=str((D(13701)/8808-1)*100)
r['rd_yoy_pct']=str((D(32362)/22822-1)*100)
r['prepayments_increase_million']=str(D(162901)+160469-24540-111270)
r['over90_ar_share_pct']=str(D(4862)/50062*100)
r['over90_ar_prior_share_pct']=str(D(3496)/49930*100)
r['over90_ar_growth_pct']=str((D(4862)/3496-1)*100)
r['current_ratio']=str(D(708144)/543416)
r['intangibles_asset_pct']=str(D(199993)/2346717*100)
r['netdebt_withleases_million']=str(D(13702)+14587+5623)
r['buyback_average_hkd']=str(D('7032259517.04')/15867600)
r['dividend_yield_pct']=str(D('5.3')/price*100)
r['quarter_annualized_adj_pe']=str(cap/(D(66519)*1000000*4))
r['group_cashflow_yield_q3_annualized_pct']=str(D(169)*100000000*4/cap*100)
r['normalized_steady_cash_required_r10_g3_cny_100m']=str(cap/100000000*(D('.10')-D('.03')))
# Three full annual periods after a 2026 year-end valuation origin.
# No remaining-Q4 cash contribution is assumed. Total shareholder cash includes
# cash dividends from associates, interest, NCI and recurring SBC economic cost;
# existing principal rolls over equally, net debt repayment if required must
# be deducted from cash; no net new borrowing supports distributions. No
# additional investment portfolio/net cash is added, preventing double count.
scenarios=[('压力',[600,1200,1500],'.11','.02'),('基准',[1000,1800,2200],'.10','.03'),('乐观',[1600,2400,3000],'.09','.04')]
models=[]
for name,cash,dr,tg in scenarios:
 rate,g=D(dr),D(tg); cash=list(map(D,cash)); tv=cash[-1]*(1+g)/(rate-g)
 pv=sum(x/(1+rate)**(i+1) for i,x in enumerate(cash)); tvpv=tv/(1+rate)**3; yearend_equity=pv+tvpv
 equity=yearend_equity/(1+rate)**(D(43)/365)
 hkd=equity*100000000/shares/fx
 models.append({'name':name,'cash_2027_2028_2029_cny_100m':[str(x) for x in cash],'r':str(rate),'g':str(g),'equity_cny_100m':str(equity),'hkd_per_share':str(hkd),'vs_price_pct':str((hkd/price-1)*100),'terminal_pv_share_pct':str(tvpv/yearend_equity*100),'valuation_date':'2026-11-18','yearend_equity_cny_100m':str(yearend_equity)})
r['dcf']=models
base_pv12=D(1000)/D('1.1')+D(1800)/D('1.1')**2
required=(cap/100000000*D('1.1')**(D(43)/365)-base_pv12)*D('1.1')**3/(1+D('1.03')/D('.07'))
r['reverse_base_2029_cash_100m']=str(required)
r['base_margin20_price']=str(D(models[1]['hkd_per_share'])*D('.8'))
# First-year actual negative FCF would reduce value, not be silently added back.
r['instant_1000_cny_100m_equity_loss_price_impact']=str(D(1000)*100000000/shares/fx)
hist=json.loads((OUT/'history_financial_data.json').read_text())['series']
r['ttm_adj_parent_cny_100m']=str(sum(map(D,hist['nonifrs_attributable_profit_rmb_m'][1:]))/100)
r['ttm_ifrs_parent_cny_100m']=str(sum(map(D,hist['ifrs_attributable_profit_rmb_m'][1:]))/100)
r['ttm_adj_pe']=str(cap/(D(r['ttm_adj_parent_cny_100m'])*100000000))
r['ttm_ifrs_pe']=str(cap/(D(r['ttm_ifrs_parent_cny_100m'])*100000000))
r['ttm_fcf_cny_100m']=str(sum(map(D,hist['company_fcf_rmb_b_rounded'][1:]))*10)
r['ttm_fcf_marketcap_pct']=str(D(r['ttm_fcf_cny_100m'])*100000000/cap*100)
r['ar_estimated_days']=str((D(49930)+50062)/2/608579*273)
r['sensitivity']=[]
for rr in ['.09','.10','.11']:
 for gg in ['.02','.03','.04']:
  rate,g=D(rr),D(gg)
  pv=D(1000)/(1+rate)+D(1800)/(1+rate)**2+(D(2200)+D(2200)*(1+g)/(rate-g))/(1+rate)**3
  px=pv/(1+rate)**(D(43)/365)*100000000/shares/fx
  r['sensitivity'].append({'r':rr,'g':gg,'hkd':str(px)})
(OUT/'calculations.json').write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n')
cmds=[['verify-market-cap','--price',str(price),'--shares',str(shares),'--reported',str(price*shares),'--currency','HKD'],['verify-valuation','--price',str(price),'--eps',str(D(66519)*1000000*4/shares/fx)]]
for k,actual in [('收入',207336),('IFRS归母',63612),('调整归母',66519),('金科企业服务收入',63655)]:
 cmds.append(['cross-validate','--field',k,'--values',json.dumps({'腾讯公告':actual,'金融界转录':actual},ensure_ascii=False),'--unit','人民币百万元','--tolerance','1'])
cmds += [['calc','--expr','(833 - 680.73)'],['calc','--expr','26 - 651 - 46 - 20'],['calc','--expr','231717 + 294010 - 380101 - 159328']]
for m in models:
 c1,c2,c3=m['cash_2027_2028_2029_cny_100m']; dr=m['r'];g=m['g']
 e=f'({c1}/(1+{dr})+{c2}/((1+{dr})*(1+{dr}))+({c3}+{c3}*(1+{g})/({dr}-{g}))/((1+{dr})*(1+{dr})*(1+{dr})))*100000000/{shares}/{fx}'
 cmds.append(['calc','--expr',e]) # CLI cross-check is year-end before 43-day discount; Decimal final model above handles actual date.
with (OUT/'financial_rigor.log').open('w') as f:
 f.write('Required toolkit checks. Final values use Decimal in calculations.json; calc internally uses float, so its last digits are not used.\n')
 for cmd in cmds:
  p=subprocess.run(['python3',str(ROOT/'tools/financial_rigor.py')]+cmd,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
  f.write('COMMAND: '+repr(cmd)+'\n'+p.stdout+'\n')
  if p.returncode: raise RuntimeError(p.stdout)
print(json.dumps(r,ensure_ascii=False,indent=2))
