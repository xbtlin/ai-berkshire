# coding: utf-8
from pathlib import Path
from decimal import Decimal as D,getcontext
import subprocess,json,re
getcontext().prec=35
R=Path('/Users/linxuan/ai-berkshire')
miniannual='https://www1.hkexnews.hk/listedco/listconews/sehk/2026/0422/2026042202118.pdf'
minihalf='https://www1.hkexnews.hk/listedco/listconews/sehk/2026/0826/2026082600680.pdf'
pros='https://www1.hkexnews.hk/listedco/listconews/sehk/2025/1231/2025123100025.pdf'
popannual='https://www1.hkexnews.hk/listedco/listconews/sehk/2026/0421/2026042100395_c.pdf'
pophalf='https://www.hkexnews.hk/listedco/listconews/sehk/2026/0820/2026082000354_c.pdf'
sa='https://stockanalysis.com/quote/hkg/'
# Values below were read from actual public source pages, not copied automatically from report claims.
facts={'MINIMAX':{4:(116.573,minihalf,116.6,'https://www.investing.com/news/stock-market-news/chinas-minimax-sees-revenue-nearly-quadruple-in-first-half-as-ai-demand-surges-4876820'),5:(-.854,miniannual,-.85,sa+'0100/financials/'),12:(17.9,minihalf,17.9,'https://www.scmp.com/tech/big-tech/article/3365341/minimax-revenue-surges-283-remains-behind-pace-meet-forecast-amid-crowded-ai-race'),15:(-465.238,miniannual,-465.24,sa+'0100/financials/'),14:(-269.246,miniannual,-269.25,sa+'0100/financials/'),18:(-12.15,miniannual,-12.15,'https://q.futunn.com/en/feed/115769089130500 [社区转述招股书，较低可信；非第二审计意见]'),29:(float((D(-258483)-D(759))/1000),pros+' CFO -258483千美元减CAPEX759千美元',-259.24,sa+'0100/financials/'),28:(float((D(-64455)-D(697))/1000),pros+' CFO -64455千美元减CAPEX697千美元',-65.15,sa+'0100/financials/'),32:(206.295,miniannual+' 现金流期初比较数',206.3,sa+'0100/financials/balance-sheet/'),36:(53.08,miniannual+' 业务拆分',53.08,sa+'0100/financials/')},'泡泡玛特':{4:(130.37749,popannual,130.38,sa+'9992/financials/'),5:(371.20052,popannual,371.20,sa+'9992/financials/'),12:(50.38384,pophalf,50.38,'https://www.finet.hk/newscenter/news_content/6a86c2d02308290c11eadd7c'),15:(61.3,popannual,61.32,sa+'9992/financials/'),18:(69.7,pophalf,69.7,'https://www.finet.hk/newscenter/news_content/6a86c2d02308290c11eadd7c'),14:(57.5,popannual,57.49,sa+'9992/financials/'),29:(108.65152,popannual,108.65,sa+'9992/financials/cash-flow-statement/'),36:(124.42065,pophalf,124.42,sa+'9992/financials/balance-sheet/'),32:(6.8531,sa+'9992/financials/balance-sheet/',6.85,'https://pdf.dfcfw.com/pdf/H3_AP202401051616654746_1.pdf [国信证券2024-01-05:2022A现金685百万元；仅采用历史现金字段]')}}
assumptions={'MINIMAX':{55:65,70:6,76:6,87:17,95:6},'泡泡玛特':{55:112,70:10,76:22}}
for co,fn in [('MINIMAX','MiniMax研究报告-20260906.md'),('泡泡玛特','泡泡玛特研究报告-20260906.md')]:
 path=R/'reports'/co;aud=path/'审计-20260906';out=subprocess.check_output(['python3',str(R/'tools/report_audit.py'),'extract','--report',str(path/fn),'--seed','42']).decode();(aud/'audit-extract.txt').write_text(out);items=json.loads(out[out.index('\n[\n')+1:]);verifiable=[];excluded=[]
 for item in items:
  n=item['id']
  if n in facts[co]:a,s,b,s2=facts[co][n];item.update(fetched_value=a,fetched_source=s,fetched_value2=b,fetched_source2=s2,verification_type='observed_fact_or_derived_historical')
  elif n in assumptions[co]:item.update(verification_type='model_input_not_observed_fact',model_input=assumptions[co][n],note='仅核对模型参数定义；不填写fetched，不声称未来事实已核实');assert D(str(item['reported_value']))==D(str(assumptions[co][n]));excluded.append(item);continue
  elif co=='MINIMAX' and n==82:item.update(fetched_value=float(D(6)*D('.2')),fetched_source='情景数学：收入6亿美元×毛利率20%；假设而非事实',fetched_value2=None,verification_type='model_calculation')
  elif co=='泡泡玛特' and n in [82,87]:
   vals=json.loads((aud/'模型结果.json').read_text());k='乐观三年分红' if n==82 else '基准含分红年化';v=float(vals[k]['value']);eps=D(11200000000)/D(1331779203)/D('.86458');g=D('1.2') if n==82 else D('1.08');dv=sum(eps*D('.25')*g**i for i in [1,2,3]);ind=dv if n==82 else (((eps*g**3*16+dv)/154)**(D(1)/3)-1)*100
   item.update(fetched_value=v,fetched_source='financial_rigor calc 模型结果.json:'+k,fetched_value2=float(ind),fetched_source2='独立Decimal实现，见审计脚本；不是外部未来事实源',verification_type='model_calculation')
  else:raise RuntimeError('unmapped '+str(item))
  verifiable.append(item)
 (aud/'audit-results.json').write_text(json.dumps(verifiable,ensure_ascii=False,indent=2));(aud/'audit-assumptions.json').write_text(json.dumps(excluded,ensure_ascii=False,indent=2));out=subprocess.check_output(['python3',str(R/'tools/report_audit.py'),'verdict','--results',json.dumps(verifiable),'--report',str(path/fn),'--output-json']).decode();(aud/'audit-verdict.txt').write_text(out)
 print(co, 'facts/calcs',len(verifiable),'model inputs',len(excluded));print(out[-220:])
