# coding: utf-8
from pathlib import Path
import json,re,subprocess,shutil
from decimal import Decimal as D,getcontext
getcontext().prec=40
root=Path('/Users/linxuan/ai-berkshire');exec(compile((Path(__file__).parent/'基础模型脚本.py').read_text(),'基础模型脚本.py','exec'))
run('MINIMAX','TTM股权PS验证',['verify-valuation','--price','361.4','--revenue-per-share',str(D(165182000)*D('6.7787')/D('0.86458')/D(349235308))])
for co, dd in {'泡泡玛特':{'王宁简单穿透年末权益百分比':'(561131960+31196420+62053027*0.4096)/1342943150*100','悲观2029归母利润率':'68.782/310*100','基准2029归母利润率':'141.087744/460*100','乐观2029归母利润率':'193.536/620*100'},'MINIMAX':{'悲观2029经营利润亿美元':'6*0.2-4-1.5','基准2029经营利润亿美元':'30*0.4-10-3','乐观2029经营利润亿美元':'60*0.55-17-6','基准净利率10%隐含PE':'6/0.1','基准净利率20%隐含PE':'6/0.2'}}.items():
 for label,expr in dd.items():calc(co,label,expr)

for y,cfo,capex in [(2022,-11019,256),(2023,-64455,697),(2024,-258483,759),(2025,-279641,920)]:
 calc('MINIMAX',str(y)+'简单自由现金流百万美元','('+str(cfo)+'-'+str(capex)+')/1000')
for co in results:(root/'reports'/co/'审计-20260906'/'模型结果.json').write_text(json.dumps(results[co],ensure_ascii=False,indent=2))
summary={}
for co in results:
 vals=results[co];price=D('361.4') if co=='MINIMAX' else D(154);sc=[]
 for label,g,pe,rev,sh in [('悲观','0.85',10,600,550),('基准','1.08',16,3000,450),('乐观','1.2',22,6000,400)]:
  if co=='MINIMAX':target=D(rev)*D(1000000)*{'悲观':2,'基准':6,'乐观':10}[label]*D('6.7787')/D('0.86458')/(D(sh)*D(1000000));div=[D(0)]*3
  else:eps=D(11200000000)/D(1331779203)/D('0.86458');target=eps*D(g)**3*D(pe);div=[eps*D('.25')*D(g)**i for i in (1,2,3)]
  assert abs(target-D(vals[label+'终值']['value']))<D('.000001')
  sc.append({'scenario':label,'terminal_price_hkd':str(target),'annual_dividends_hkd':[str(x) for x in div],'cash_dividend_sum_hkd':str(sum(div))})
 summary[co]={'price_hkd':str(price),'years':3,'terminal_year':2029,'scenarios':sc,'method':'Decimal独立重算; dividends held as cash, no reinvestment'}
 (root/'reports'/co/'审计-20260906'/'comparison_summary.json').write_text(json.dumps(summary[co],ensure_ascii=False,indent=2))
