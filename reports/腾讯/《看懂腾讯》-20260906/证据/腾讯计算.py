from decimal import Decimal, getcontext
from pathlib import Path
import subprocess,json
getcontext().prec=40
D=Decimal
out=Path(__file__).resolve().parent
rigor=Path(__file__).resolve().parents[4]/'tools'/'financial_rigor.py'
checks=[]
def calc(name,expr,value):
    p=subprocess.run(['python3',str(rigor),'calc','--expr',expr],capture_output=True,text=True,check=True)
    checks.append(dict(name=name,expression=expr,decimal_independent=str(value),financial_rigor_stdout=p.stdout))
    return value
shares=D('9.103153877'); diluted=D('9.2'); fx=D('0.8559'); price=D('442.8')
mcap=calc('市场总市值_十亿港元','442.8*9.103153877',price*shares)
rmcap=calc('市场总市值_十亿元','442.8*9.103153877*0.8559',mcap*fx)
raw={'revenue':[560118,554552,609015,660257,751766], 'gross_profit':[245944,238746,293109,349246,422593], 'operating_profit_restated':[124656,110827,160074,208099,241562], 'attributable_profit':[224822,188243,115216,194073,224842], 'nonifrs_attributable_profit':[123788,115649,157688,222703,259626], 'cfo':[175186,146091,221962,258521,303052], 'parent_equity':[806299,721391,808591,973548,1154152]}
ttm={}
for k,f,h,p in [('revenue',751766,401243,364526),('gross_profit',422593,229698,205506),('operating_profit',241562,134651,117670),('attributable_profit',224842,114115,103449),('nonifrs_attributable_profit',259626,136320,124381),('nonifrs_operating_profit',280656,151263,138568),('attributable_sbc_adjustment',34711,14949,18904),('equity_settled_sbc',25660,11046,13397),('nonifrs_associates',33457,13482,13988)]:
 ttm[k]=calc('TTM_'+k,f'{f}+{h}-{p}',D(f)+D(h)-D(p))
metrics={}
metrics['ttm_nonifrs_after_attributable_sbc']=calc('TTM_nonIFRS减归母SBC','271565-30756',D(271565)-D(30756))
for k in ['attributable_profit','nonifrs_attributable_profit']:
 metrics[k+'_pe']=calc(k+'_PE',f'{rmcap}*1000/{ttm[k]}',rmcap*1000/ttm[k])
metrics['after_sbc_pe']=calc('扣SBC后参考倍数',f'{rmcap}*1000/240809',rmcap*1000/D(240809))
metrics['price_cny']=calc('股价人民币','442.8*0.8559',price*fx)
metrics['fcf2025_proxy']=calc('2025集团广义现金余额_百万元','303052-87482-25399+6-6783',D(303052)-87482-25399+6-6783)
metrics['fcfh125_proxy']=calc('2025H1集团广义现金余额_百万元','151265-45558-11899+6-3265',D(151265)-45558-11899+6-3265)
metrics['fcfh126_proxy']=calc('2026H1集团广义现金余额_百万元','154061-95615-11547-1-3636',D(154061)-95615-11547-1-3636)
metrics['fcfttm_proxy']=calc('TTM集团广义现金余额_百万元','183394+43262-90549',D(183394)+43262-90549)
metrics['fcf2025_reference']=calc('2025现金粗锚减SBC及估计少数股东_百万元','183394-25660-5000',D(183394)-25660-5000)
metrics['fcfttm_reference']=calc('TTM现金粗锚减SBC及估计少数股东_百万元','136107-23309-6000',D(136107)-23309-6000)
metrics['q2_newai_op_gap']=calc('Q2新AI经营利润差额_十亿元','86.1-75.636',D('86.1')-D('75.636'))
metrics['reserve_netcash']=calc('可加入估值净现金_十亿元','58.191-50',D('58.191')-50)
for i,year in enumerate(range(2021,2026)):
 metrics[f'{year}_gpm']=calc(f'{year}_毛利率',f"{raw['gross_profit'][i]}/{raw['revenue'][i]}*100",D(raw['gross_profit'][i])/D(raw['revenue'][i])*100)
 if i: metrics[f'{year}_roe']=calc(f'{year}_IFRS归母平均权益ROE',f"{raw['attributable_profit'][i]}/(({raw['parent_equity'][i-1]}+{raw['parent_equity'][i]})/2)*100",D(raw['attributable_profit'][i])*200/(D(raw['parent_equity'][i-1])+D(raw['parent_equity'][i])))
for key in ['revenue','gross_profit','nonifrs_attributable_profit']:
 # CAGR is corroborated using Decimal fractional exponent rather than binary floats
 metrics[key+'_cagr2021to25']=calc(key+'_四年CAGR',f"({raw[key][-1]}/{raw[key][0]})**(1/4)-1",(D(raw[key][-1])/D(raw[key][0]))**(D(1)/4)-1)
scenarios={
 'bear':{'first5':['50','75','95','110','120'],'growth6to10':'0.02','terminal_g':'0','listed_haircut':'0.35','unlisted_haircut':'0.65'},
 'base':{'first5':['100','140','170','190','210'],'growth6to10':'0.05','terminal_g':'0.02','listed_haircut':'0.20','unlisted_haircut':'0.50'},
 'bull':{'first5':['130','180','220','260','300'],'growth6to10':'0.08','terminal_g':'0.02','listed_haircut':'0.10','unlisted_haircut':'0.30'}}
for name,s in scenarios.items():
 flows=list(map(D,s['first5']))
 for y in range(5): flows.append(flows[-1]*(1+D(s['growth6to10'])))
 s['flows10_bn_cny']=list(map(str,flows)); s['values']={}
 inv=calc(name+'_投资净现金桥',f"487.2*(1-{s['listed_haircut']})+387.9*(1-{s['unlisted_haircut']})+8.191",D('487.2')*(1-D(s['listed_haircut']))+D('387.9')*(1-D(s['unlisted_haircut']))+D('8.191'))
 for rstr in ['0.08','0.09']:
  r=D(rstr); g=D(s['terminal_g'])
  pv=sum((v/(1+r)**(i+1) for i,v in enumerate(flows)),D(0))
  tv=flows[-1]*(1+g)/(r-g)/(1+r)**10
  expr='+'.join(f'{f}/(1+{r})**{i+1}' for i,f in enumerate(flows))+f'+{flows[-1]}*(1+{g})/({r}-{g})/(1+{r})**10'
  core=calc(name+'_DCF_'+rstr,expr,pv+tv)
  fair=calc(name+'_每股港元_'+rstr,f'({core}+{inv})/9.2/0.8559',(core+inv)/diluted/fx)
  s['values'][rstr]={'core_bn_cny':str(core),'noncore_bridge_bn_cny':str(inv),'equity_bn_cny':str(core+inv),'hkd_per_share_9_2bn':str(fair),'terminal_share_of_core':str(tv/core)}
metrics['base_safety20pct_price']=calc('基准8%价值八折',f"{scenarios['base']['values']['0.08']['hkd_per_share_9_2bn']}*0.8",D(scenarios['base']['values']['0.08']['hkd_per_share_9_2bn'])*D('0.8'))
metrics['base_safety25pct_price']=calc('基准8%价值七五折',f"{scenarios['base']['values']['0.08']['hkd_per_share_9_2bn']}*0.75",D(scenarios['base']['values']['0.08']['hkd_per_share_9_2bn'])*D('0.75'))
metrics['conservative_safety20pct_price']=calc('基准9%价值八折',f"{scenarios['base']['values']['0.09']['hkd_per_share_9_2bn']}*0.8",D(scenarios['base']['values']['0.09']['hkd_per_share_9_2bn'])*D('0.8'))
metrics['conservative_safety25pct_price']=calc('基准9%价值七五折',f"{scenarios['base']['values']['0.09']['hkd_per_share_9_2bn']}*0.75",D(scenarios['base']['values']['0.09']['hkd_per_share_9_2bn'])*D('0.75'))
metrics['reconciliation2025']=calc('2025归母nonIFRS调节','224842+34711-7896+11498-3117+2570+360-3342',D(224842)+34711-7896+11498-3117+2570+360-3342)
for key,expr,value in [('TTM_cfo','303052+154061-151265',D(303052)+154061-151265),('TTM_intangible','25399+11547-11899',D(25399)+11547-11899),('TTM_leaseprincipal','6783+3636-3265',D(6783)+3636-3265),('AIprepayQ2','37.6-(-13.8)',D('37.6')+D('13.8')),('bear8_downside','244.00988019236386/442.8-1',D(scenarios['bear']['values']['0.08']['hkd_per_share_9_2bn'])/price-1),('bear9_downside','221.18898997342228/442.8-1',D(scenarios['bear']['values']['0.09']['hkd_per_share_9_2bn'])/price-1)]: metrics[key]=calc(key,expr,value)
basecore=D(scenarios['base']['values']['0.08']['core_bn_cny']); basebridge=D('591.901')
metrics['market_implied_core_92bn']=calc('模型股本对应市值减非核心桥','442.8*9.2*0.8559-591.901',price*diluted*fx-basebridge)
metrics['market_implied_baseflow_scale8']=calc('8%基准市场隐含现金比例',f"{metrics['market_implied_core_92bn']}/{basecore}",metrics['market_implied_core_92bn']/basecore)
metrics['market_implied_baseflow_scale9']=calc('9%基准市场隐含现金比例',f"{metrics['market_implied_core_92bn']}/{scenarios['base']['values']['0.09']['core_bn_cny']}",metrics['market_implied_core_92bn']/D(scenarios['base']['values']['0.09']['core_bn_cny']))
metrics['base_cash20pct_lower']=calc('8%基准现金统一下调20%',f'({basecore}*0.8+591.901)/9.2/0.8559',(basecore*D('0.8')+basebridge)/diluted/fx)
metrics['base_assets_zero']=calc('8%基准非并表投资零值保留剩余净现金',f'({basecore}+8.191)/9.2/0.8559',(basecore+D('8.191'))/diluted/fx)
flows=list(map(D,scenarios['base']['flows10_bn_cny']))
pv=sum((v/D('1.08')**(i+1) for i,v in enumerate(flows)),D(0))
g1value=(pv+flows[-1]*D('1.01')/D('0.07')/D('1.08')**10+basebridge)/diluted/fx
metrics['base_g1pct']=calc('8%基准永续降至1%',f'({pv}+{flows[-1]}*1.01/0.07/1.08**10+591.901)/9.2/0.8559',g1value)
obj={'as_of' :'2026-09-06','price_as_of':'2026-09-04','raw_million_cny':raw,'shares_bn_actual':str(shares),'shares_bn_model':str(diluted),'fx_cny_per_hkd':str(fx),'price_hkd':str(price),'mcap_bn_hkd':str(mcap),'mcap_bn_cny':str(rmcap),'ttm_million_cny':{k:str(v) for k,v in ttm.items()},'metrics':{k:str(v) for k,v in metrics.items()},'scenarios':scenarios,'note':'Forward core cashflows are assumptions after economic SBC, attributable minority portion and all reinvestment; cash flow proxy is not reported FCF or attributable FCF. Discount rate sensitivity not risk probabilities. financial_rigor calc uses eval; Decimal independently corroborates.'}
(out/'财务真值与估值.json').write_text(json.dumps(obj,ensure_ascii=False,indent=2))
(out/'financial_rigor运算记录.json').write_text(json.dumps(checks,ensure_ascii=False,indent=2))
print(json.dumps(obj,ensure_ascii=False,indent=2))
