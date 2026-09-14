"""Reproduce two research models. Inputs are facts or explicitly subjective assumptions.
Run from repository root. No network, no trading, no old report edits.
"""
from pathlib import Path
from decimal import Decimal as D
import subprocess,json,re

ROOT=Path('reports'); FX=D('0.86458')
CONFIG={
 '快手':{'ticker':'1024','price':'33.66','shares':'43.26961215','reported_cap':'1456.4551',
  'hist':{'收入':[810.82,941.83,1134.70,1268.98,1427.76],'归母净利润':[-780.74,-136.90,63.96,153.35,186.17],'毛利':[340.30,421.31,573.91,692.92,785.49],'标准化经营利润':[-276.91,-111.79,59.52,135.73,178.41],'经营现金流':[-55.19,7.95,207.81,297.87,267.16],'资本支出':[77.64,51,48.97,80.63,149.42],'现金及短期投资':[454.57,356.20,490.18,516.40,622.56]},
  'scenarios':[['悲观','1300','.06',8,50,2,'.65',180,600,'.6'],['基准','1387.4*1.02*1.02*1.02','.095',10,100,6,'.60',300,180,'1.5'],['乐观','1387.4*1.05*1.05*1.05','.12',12,160,10,'.55',450,90,'2.4']]},
 '美团':{'ticker':'3690','price':'81.75','shares':'61.754848','reported_cap':'5048.4588',
  'hist':{'收入':[1791.27997,2199.54948,2767.44954,3375.91576,3648.54746],'归母净利润':[-235.38379,-66.86110,138.55828,358.07179,-233.55015],'毛利':[424.74128,617.52979,971.91161,1297.84594,1110.08626],'标准化经营利润':[-259.44,-66.04,89.97,331.59,-310.36],'经营现金流':[-40.11,114.11,405.22,571.46784,-138.15001],'资本支出':[90.10,57.31,68.80,109.99490,132.70708],'现金及短期投资':[1167.95,1120.32,1451.60,1682.43,1668.34]},
  'scenarios':[['悲观','1.03','.08',80,180,12,-200,150],['基准','1.07','.14',30,150,16,300,300],['乐观','1.10','.18',0,130,20,700,500]]}}

def run(c,args):
 r=subprocess.run(['python3','tools/financial_rigor.py']+list(map(str,args)),capture_output=True,text=True,check=True)
 with (ROOT/c/'审计-20260906'/'financial_rigor.txt').open('a') as f:f.write('$ financial_rigor.py '+' '.join(map(str,args))+'\n'+r.stdout+'\n')
 if '❌' in r.stdout:raise RuntimeError(r.stdout)
 return r.stdout

def calc(c,key,expr,out):
 txt=run(c,['calc','--expr='+str(expr)]);m=re.search('精确值:\s*([^\n]+)',txt)
 if not m:raise ValueError(txt)
 val=float(m.group(1));out[key]={'expression':str(expr),'value':val};return val

for c,p in CONFIG.items():
 d=ROOT/c/'审计-20260906'; (d/'financial_rigor.txt').write_text('')
 (d/'model_inputs.json').write_text(json.dumps(p,ensure_ascii=False,indent=2))
 out={};price=p['price'];sh=p['shares'];fx=str(FX)
 run(c,['verify-market-cap','--price',price,'--shares',str(D(sh)*D('1e8')),'--reported',str(D(p['reported_cap'])*D('1e8')),'--currency','HKD'])
 run(c,['cross-validate','--field','总股本','--values',json.dumps({'腾讯行情亿股':float(sh),'StockAnalysis亿股':43.3 if c=='快手' else 61.7},ensure_ascii=False),'--unit','亿股'])
 for field,v in [('收入',p['hist']['收入'][-1]),('归母净利润',p['hist']['归母净利润'][-1])]:
  sa=1427.76 if c=='快手' and field=='收入' else 186.17 if c=='快手' else 3648.55 if field=='收入' else -233.55
  run(c,['cross-validate','--field','2025'+field,'--values',json.dumps({'官方年报':v,'StockAnalysis':sa},ensure_ascii=False),'--unit','亿元人民币'])
 cash=804.07 if c=='快手' else 1683.14170
 run(c,['cross-validate','--field','2026H1现金及短期投资','--values',json.dumps({'官方分类加总':cash,'StockAnalysis':804.07 if c=='快手' else 1683.14},ensure_ascii=False),'--unit','亿元人民币'])
 for i,y in enumerate(range(2021,2026)):
  calc(c,f'{y}毛利率',f'{p["hist"]["毛利"][i]}/{p["hist"]["收入"][i]}*100',out)
  calc(c,f'{y}标准化经营利润率',f'{p["hist"]["标准化经营利润"][i]}/{p["hist"]["收入"][i]}*100',out)
  calc(c,f'{y}自由现金流',f'{p["hist"]["经营现金流"][i]}-{p["hist"]["资本支出"][i]}',out)
 cap=calc(c,'人民币市值',f'{price}*{sh}*{fx}',out)
 if c=='快手':
  profit=calc(c,'TTM归母净利','186.17+60.49-89.00',out)
  rev=calc(c,'TTM收入','1427.76+692.51-676.54',out)
  eps=calc(c,'TTM每股盈利港元',f'{profit}/{sh}/{fx}',out)
  bv=calc(c,'每股净资产港元',f'822.39/{sh}/{fx}',out)
  run(c,['verify-valuation','--price',price,'--eps',eps,'--bvps',bv,'--dividend','.69','--revenue-per-share',rev/float(sh)/float(FX)])
  liquid=calc(c,'狭义净现金含租赁','116.96+123.58+563.53-273.62-116.72',out)
  initial=calc(c,'初始可归属盈余金融资产','413.73+142.91+271.16*.9+25.02*.5-250-25.84',out)
  calc(c,'净流动资产','988.52-939.77',out)
  calc(c,'现金等价物','11696/100',out)
  calc(c,'H1经营现金流同比','(90.44/117.81-1)*100',out)
  calc(c,'Q2经调整净利同比','(39.13/56.18-1)*100',out)
  calc(c,'可灵基准收入CAGR','(100/34)**(1/3)-1',out)
  calc(c,'Q2去投资损益税前经营利润','183.28-99.22-8.95-45.81',out)
  calc(c,'历史利润桥接参考','186.17+19-31*.85',out)
  calc(c,'历史去可灵收入','1427.76-11',out)
  results=[]
  for name,r,m,pe,kr,km,stake,cf,support,div in p['scenarios']:
   revenue=calc(c,name+'传统收入',r,out); op=calc(c,name+'传统税后经营收益',f'{revenue}*{m}',out)
   core=calc(c,name+'传统业务估值',f'{op}*{pe}',out);kling=calc(c,name+'可灵归属价值',f'{kr}*{km}*{stake}',out)
   endcash=calc(c,name+'期末盈余现金',f'{initial}+{cf}-{support}-{div}*{sh}*{fx}',out)
   target=calc(c,name+'三年目标价',f'({core}+{kling}+{endcash})/{sh}/{fx}',out)
   total=calc(c,name+'三年总回报',f'({target}+{div})/{price}-1',out)
   cagr=calc(c,name+'年化回报',f'(({target}+{div})/{price})**(1/3)-1',out)
   pv=calc(c,name+'今日价值',f'{target}/(1.1*1.1*1.1)+({div}/3)/1.1+({div}/3)/1.21+({div}/3)/1.331',out)
   results.append(dict(name=name,revenue=revenue,profit=op,core=core,kling=kling,cash=endcash,target=target,dividend=float(div),total=total,cagr=cagr,pv=pv))
  calc(c,'可灵零估值基准价格',f'({results[1]["core"]}+{results[1]["cash"]})/{sh}/{fx}',out)
  calc(c,'基准晚两年年化',f'(({results[1]["target"]}+1.5)/{price})**(1/5)-1',out)
  calc(c,'现价隐含零可灵传统利润',f'({cap}-{initial})/10',out)
  # EPS scenario is a separate consolidated cross-check; never add Kling or cash to it.
  run(c,['three-scenario','--price',price,'--eps',eps,'--shares',sh,'--growth','.10','0','-.15','--pe','12','10','7','--years','3','--currency','HKD'])
 else:
  profit=calc(c,'TTM归母净利','-233.55015-46.72487-104.21644',out)
  rev=calc(c,'TTM收入','3648.54746+1956.81950-1776.96362',out)
  bv=calc(c,'每股净资产港元',f'1692.06460/{sh}/{fx}',out)
  run(c,['verify-valuation','--price',price,'--bvps',bv,'--revenue-per-share',rev/float(sh)/float(FX)])
  debt=calc(c,'含租赁总债務','(35304527+6833774+46060011+502943+4263557+2852490)/100000',out)
  net=calc(c,'含租赁净现金',f'(104716797+63597373)/100000-{debt}',out)
  initial=calc(c,'初始盈余现金',f'{net}-350',out)
  inv=calc(c,'战略投资账面池','(25863652+15030035+36387099)/100000',out)
  calc(c,'净投资资产扣递延税参考',f'{inv}-91.80227',out)
  calc(c,'Q2毛利减四费','(35094797-24723345-7670045-3238070-320931)/100000',out)
  calc(c,'核心收入TTM','2608.26094+1355.93841-1289.70753',out)
  calc(c,'SBC年化','19.18583*4',out)
  calc(c,'未分配费用极端上界年化','(12.38194+34.93946+.54814)*4',out)
  results=[]
  for name,g,m,new,cost,pe,cf,inv in p['scenarios']:
   revenue=calc(c,name+'核心收入',f'2800*{g}*{g}*{g}',out)
   core=calc(c,name+'核心经营利润',f'{revenue}*{m}',out)
   pretax=calc(c,name+'税前经营收益',f'{core}-{new}-{cost}',out)
   op=calc(c,name+'税后经营收益',f'{pretax}*'+('0.8' if pretax>0 else '1'),out)
   endcash=calc(c,name+'期末盈余现金',f'{initial}+{cf}',out)
   business=calc(c,name+'经营业务估值',f'{max(op,0)}*{pe}',out)
   target=calc(c,name+'三年目标价',f'({business}+{endcash}+{inv})/{sh}/{fx}',out)
   total=calc(c,name+'三年总回报',f'{target}/{price}-1',out)
   cagr=calc(c,name+'年化回报',f'({target}/{price})**(1/3)-1',out)
   pv=calc(c,name+'今日价值',f'{target}/(1.1*1.1*1.1)',out)
   results.append(dict(name=name,revenue=revenue,core=core,profit=op,cash=endcash,investments=inv,target=target,dividend=0,total=total,cagr=cagr,pv=pv))
  b=results[1]
  for m in ['.079','.08','.10','.12','.14']:
   calc(c,'利润率'+m+'三年目标价',f'(({b["revenue"]}*{m}-30-150)*.8*16+{b["cash"]}+300)/{sh}/{fx}',out)
  for hq in [110,150,190]:calc(c,'总部'+str(hq)+'三年目标价',f'(({b["revenue"]}*.14-30-{hq})*.8*16+{b["cash"]}+300)/{sh}/{fx}',out)
  calc(c,'现价隐含核心利润率',f'((({cap}-{b["cash"]}-300)/16)/.8+30+150)/{b["revenue"]}*100',out)
  calc(c,'10%三年回报所需核心率',f'((({cap}*1.1*1.1*1.1-{b["cash"]}-300)/16)/.8+30+150)/{b["revenue"]}*100',out)
  calc(c,'基准晚两年年化',f'({b["target"]}/{price})**(1/5)-1',out)
  (d/'three-scenario-not-applicable.txt').write_text('TTM归母净利润为负；EPS增长×PE无法表示由亏转盈。未运行无经济意义的负PE three-scenario，改用financial_rigor calc逐项验证核心收入×分部利润率−新业务亏损−未分配费用−税、盈余现金和战略投资三情景。')
 (d/'calculations.json').write_text(json.dumps(out,ensure_ascii=False,indent=2))
 (d/'scenarios.json').write_text(json.dumps(results,ensure_ascii=False,indent=2))
 summary={'version':'final-v1-20260906','currency':'HKD','reference_price':float(price),'shares_100million':float(sh),'fx_cny_per_hkd':float(FX),'years':3,'scenarios':results}
 for result in results:
  result['dividend_by_year']=[result['dividend']/3]*3
 (d/'comparison_summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2))
 print(c,json.dumps(results,ensure_ascii=False))
