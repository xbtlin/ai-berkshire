#!/usr/bin/env python3
"""Local research calculations. No network or portfolio actions."""
import json, subprocess
from pathlib import Path
from decimal import Decimal as D, getcontext
getcontext().prec=36
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]
rigor=ROOT/'tools/financial_rigor.py'
terminal=ROOT/'tools/terminal_value.py'
log=[]; results={}
def command(args):
 p=subprocess.run(['python3']+[str(v) for v in args],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,universal_newlines=True)
 log.append({'args':[str(v) for v in args][1:],'exit_code':p.returncode,'output':p.stdout});return p.stdout
def calc(name,expr):
 command([rigor,'calc','--expr',expr]);v=eval(expr,{'__builtins__':{}},{});results[name]={'expression':expr,'tool_calculated_value':str(v)}
price=D('33.66'); shares=D('4326961215'); fx=D('0.8559');shares_yi=shares/D('1e8');mcap=price*shares_yi; mcap_cny=mcap*fx
command([rigor,'verify-market-cap','--price',price,'--shares',shares,'--reported','145645000000','--currency','HKD'])
expressions={
 'shares':'3664102236+662858979','mcap_hkd_yi':'33.66*4326961215/1e8','mcap_cny_yi':'33.66*4326961215/1e8*0.8559',
 'ttm_revenue':'(142776-67654+69251)/100','ttm_net_parent':'(18617-8900+6049)/100','ttm_adjusted':'(20647-10198+7287)/100','ttm_sbc':'(2640-1320+1311)/100',
 'ttm_adjusted_less_sbc':'(20647-10198+7287-2640+1320-1311)/100','ocf_2025':'26716/100','fcf_2025':'(26716-14942)/100','fcf_2025_after_lease':'(26716-14942-3823)/100','fcf_2025_after_lease_sbc':'(26716-14942-3823-2640)/100',
 'ttm_ocf':'(26716-11781+9044)/100','h12026_capex_estimate':'121+59','h12026_fcf_estimate':'90.44-121-59','ttm_capex_estimate':'149.42-70.75+121+59','ttm_fcf_estimate':'(26716-11781+9044)/100-(149.42-70.75+121+59)',
 'cash_current_investment':'(11696+12358+56353)/100','total_borrowing':'(14792+12570)/100','total_lease':'(7920+3752)/100','netcash_current_includinglease':'(11696+12358+56353-14792-12570-7920-3752)/100',
 'example_contributions':'100-25-15','example_contributions_mid':'100-45-15','example_contributions_low':'100-65-15','tenor_simple_example':'30*(1+0.08*5)',
 'rev2025_structure_sum':'814.62+390.87+222.27','revenue_CAGR_2021_2025':'(142776/81082)**(1/4)-1','grossprofit_CAGR':'(78549/34030)**(1/4)-1','marketing_ratio2021':'44175.898/81081.513*100','marketing_ratio2025':'42229/142776*100',
 'q2_ads_perDAU':'20639/412.3','h1rev_yoy':'(69251/67654-1)*100','h1net_yoy':'(6049/8900-1)*100','q2rd_yoy':'(4581/3400-1)*100',
 'PE_ttm_IFRS':'33.66*4326961215*0.8559/(18617-8900+6049)/1e6','PE_ttm_adjusted':'33.66*4326961215*0.8559/(20647-10198+7287)/1e6','PE_ttm_adjusted_lesssbc':'33.66*4326961215*0.8559/(20647-10198+7287-2640+1320-1311)/1e6','PE_forward_low':'33.66*4326961215*0.8559/9e9','PE_forward_high':'33.66*4326961215*0.8559/8.5e9',
 'PE2025':'33.66*4326961215*0.8559/18617e6','FCFyield2025':'(26716-14942)*1e6/(33.66*4326961215*0.8559)*100','FCFyield2025_lease':'(26716-14942-3823)*1e6/(33.66*4326961215*0.8559)*100','FCFyield2025_lease_sbc':'(26716-14942-3823-2640)*1e6/(33.66*4326961215*0.8559)*100','PB':'33.66*4326961215*0.8559/82239e6','reverse_cash9':'(33.66*4326961215/1e8*0.8559-150)*0.09','reverse_cash8':'(33.66*4326961215/1e8*0.8559-150)*0.08',
 'q2_revenueshare_rise':'(12323-10542)/100','adjusted_bridge2025':'18624+2640-617','adjusted_bridgeh12026':'6057+1311-81'}
expressions.update({'h12025_fcf':'11781-7075','adjusted_less_sbc_2025':'20647-2640','adjusted_less_sbc_h12025':'10198-1320','adjusted_less_sbc_h12026':'7287-1311','q12026_parent':'6049-3146','kling_conditional_economic':'66.33+2','kling_conditional_vote':'52.23+1.57','kling_fullcap_postmoney_usd_bn':'15+3'})
for n,e in expressions.items():calc(n,e)
for name,a,b,unit,src1,src2 in [('2025收入',142776,142776,'百万元人民币','A25公司年报','Stock Analysis'),('2025归母IFRS',18617,18617,'百万元人民币','A25公司年报','Stock Analysis'),('TTM归母IFRS',15766,15766,'百万元人民币','A25和H26拼接','Stock Analysis'),('2025现金加流动投资',62256,62256,'百万元人民币','A25公司年报','Stock Analysis'),('2026H1现金加流动投资',80407,80407,'百万元人民币','H26公告','Stock Analysis'),('2025经营现金流',26716,26716,'百万元人民币','A25公司年报','Stock Analysis'),('2025资本购买及预付',14942,14942,'百万元人民币','A25公司年报','Stock Analysis'),('2026Q2调整净利',3913,3910,'百万元人民币','H26公告','光大海外20260820摘要，已舍入'),('2026年9月4日股价',33.66,33.66,'HKD','Investing历史行情','Stock Analysis历史行情'),('2026年9月4日汇率',.8559,.8560,'CNY/HKD','Investing历史汇率','ValutaFX历史汇率')]:
 command([rigor,'cross-validate','--field',name,'--values',json.dumps({src1:a,src2:b},ensure_ascii=False),'--unit',unit])
for y,ocf,capex in [(2021,-5519,7764),(2022,795,5100),(2023,20781,4897),(2024,29787,8063),(2025,26716,14942)]:calc('fcf_'+str(y),f'({ocf}-{capex})/100')
case_inputs={'保守':{'cash':[0,20,35,45,50,50,50,50,50,50],'g':'0','surplus':100},'基准':{'cash':[30,60,80,100,120,130,140,150,160,170],'g':'0.01','surplus':150},'乐观':{'cash':[70,100,130,160,200,230,260,290,320,350],'g':'0.02','surplus':200}}
model=[]
for name,inputs in case_inputs.items():
 for rr in ['0.08','0.09']:
  r=D(rr);g=D(inputs['g']);roic=D('0.20');fs=list(map(D,inputs['cash']));s=D(inputs['surplus'])
  pv=sum(f/(1+r)**(i+1) for i,f in enumerate(fs));tv=fs[-1]*(1+g)/(r-g);pvtv=tv/(1+r)**10;total=pv+pvtv+s; target=total/shares_yi/fx;pe=(1-g/roic)/(r-g)
  expr='+'.join(f'{f}/(1+{r})**{i+1}' for i,f in enumerate(fs))+f'+{fs[-1]}*(1+{g})/({r}-{g})/(1+{r})**10+{s}'
  command([rigor,'calc','--expr',expr]);command([terminal,'pe','--roic',roic,'--g',g,'--r',r])
  model.append({'case':name,'r':str(r),'g':str(g),'roic':'0.20','cashflows_cny_yi':inputs['cash'],'surplus_cny_yi':str(s),'pv_explicit':str(pv),'terminal_pe':str(pe),'r_minus_g':str(r-g),'terminal_equity':str(tv),'pv_terminal':str(pvtv),'equity_value_cny_yi':str(total),'hkd_per_share':str(target),'change_from_price':str(target/price-1),'terminal_fraction':str(pvtv/total)})
hurdles=[]
base=case_inputs['基准']
for rr in ['0.10','0.12']:
 r=D(rr); g=D(base['g']); fs=list(map(D,base['cash']));s=D(base['surplus'])
 pv=sum(f/(1+r)**(i+1) for i,f in enumerate(fs)); tv=fs[-1]*(1+g)/(r-g);pvtv=tv/(1+r)**10; total=pv+pvtv+s
 expr='+'.join(f'{f}/(1+{r})**{i+1}' for i,f in enumerate(fs))+f'+{fs[-1]}*(1+{g})/({r}-{g})/(1+{r})**10+{s}'
 command([rigor,'calc','--expr',expr])
 hurdles.append({'case':'基准现金路径不变，仅改变投资者要求回报','r':rr,'g':str(g),'cashflows_cny_yi':base['cash'],'surplus_cny_yi':str(s),'pv_explicit':str(pv),'pv_terminal':str(pvtv),'equity_value_cny_yi':str(total),'hkd_per_share':str(total/shares_yi/fx),'terminal_fraction_of_equity':str(pvtv/total)})
for r in ['0.08','0.09']:
 command([terminal,'audit','--currency','CNY','--r',r,'--roic','.20','--g','0,.01,.02','--rf','.02','--beta','1.0','--discrete-risks','主业份额损失:情景,可灵商业化失败:情景,融资回购触发:尾部档,VIE失效:未建模,算力供应中断:未建模'])
eps=D('6000000000')/shares/fx
command([rigor,'three-scenario','--price',price,'--eps',eps,'--shares',shares_yi,'--growth','0.35','0.18','-0.05','--pe','16','12','8','--years','3','--currency','HKD'])
command([rigor,'verify-valuation','--price',price,'--eps',D('15766000000')/shares/fx,'--bvps',D('82239000000')/shares/fx,'--fcf-per-share',D('11774000000')/shares/fx])
results['exact_decimal_market']={'price_hkd':str(price),'shares':str(shares),'CNY_per_HKD':str(fx),'market_cap_hkd_yi':str(mcap),'market_cap_cny_yi':str(mcap_cny)}
(HERE/'calculations.json').write_text(json.dumps(results,ensure_ascii=False,indent=2))
(HERE/'dcf_scenarios.json').write_text(json.dumps(model,ensure_ascii=False,indent=2))
(HERE/'hurdle_sensitivity.json').write_text(json.dumps(hurdles,ensure_ascii=False,indent=2))
(HERE/'financial_rigor_runs.json').write_text(json.dumps(log,ensure_ascii=False,indent=2))
print(json.dumps(results['exact_decimal_market'],ensure_ascii=False))
for x in model:print(x['case'],x['r'],'value',round(D(x['equity_value_cny_yi']),2),'HKD',round(D(x['hkd_per_share']),2),'change',round(D(x['change_from_price'])*100,1))
for n in ['PE_ttm_IFRS','PE_ttm_adjusted','PE_ttm_adjusted_lesssbc','PE_forward_low','PE_forward_high','FCFyield2025','FCFyield2025_lease','FCFyield2025_lease_sbc','PB','reverse_cash9','reverse_cash8']:print(n,results[n]['tool_calculated_value'])
print(log[-2]['output'])
