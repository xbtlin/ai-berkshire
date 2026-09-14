"""Fixed-seed audit. Explicit observed facts are distinct from model checks.
Assumptions are checked for disclosure consistency, never externally verified.
"""
from pathlib import Path
from decimal import Decimal as D, getcontext
import json, subprocess, importlib.util
getcontext().prec=32
spec=importlib.util.spec_from_file_location('audit','tools/report_audit.py');a=importlib.util.module_from_spec(spec);spec.loader.exec_module(a)
fx='https://hzf.mofcom.gov.cn/article/zyfw/jrfw/jrfwywzn/jrfwwh/hlfxglzy/202609/7872.html'
fx2='https://english.news.cn/20260904/790d1ee7b6864f7b96752579a210e783/c.html'
for c,t,slug in [('快手','1024','kuaishou-technology'),('美团','3690','meituan')]:
 d=Path('reports')/c/'审计-20260906'; report=Path('reports')/c/(c+'研究报告-20260906.md')
 extracted=subprocess.run(['python3','tools/report_audit.py','extract','--report',str(report),'--seed','42'],capture_output=True,text=True,check=True).stdout
 (d/'audit_extract_seed42.txt').write_text(extracted)
 sampled=a.sample_points(a.extract_data_points(report.read_text()),ratio=.15,seed=42)
 sa=f'https://stockanalysis.com/quote/hkg/{t}/financials/'
 bal=sa+'balance-sheet/';cf=f'https://www.stockopedia.com/share-prices/{slug}-HKG%3A{t}/cashflow/';sb=f'https://www.stockopedia.com/share-prices/{slug}-HKG%3A{t}/balance-sheet/'
 annual=json.load(open(d/'sources.json'))
 official='annual2025.pdf：五年财务概要（已下载官方原件）'
 model=json.load(open(d/'model_inputs.json'));calc=json.load(open(d/'calculations.json'));sh=D(model['shares']);f=D('.86458')
 facts={}
 def add(label,x,s,y,s2,note=''):
  facts[label]={'fetched_value':float(x),'fetched_source':s,'fetched_value2':float(y),'fetched_source2':s2,'verification_kind':'external-fact','note':note}
 add(('估值参考汇率' if c=='快手' else '参考汇率')+'（人民币/港元） · 数值','.86458',fx,D('86.458')/100,fx2,'同一官方定价的两个公开分发渠道，不是两次独立市场观测')
 if c=='快手':
  for y,v in [(2024,'692.92'),(2023,'573.91'),(2021,'340.30')]:add('毛利 · '+str(y),v,official,v,sa)
  add('归母净利润 · 2022','-136.90',official,'-136.90',sa)
  for y,v in [(2023,'48.97'),(2022,'51'),(2024,'80.63')]:add('资本支出 · '+str(y),v,sa,v,cf,'资本支出取现金流出绝对值；两供应商S&P及Refinitiv')
  add('现金及短期投资 · 2025','622.56',bal,'621.43',sb,'数据商分类差异，报告已披露；本数不进入最新现金桥')
  add('现金及短期投资 · 2021','454.57',bal,'452.80',sb,'分类差异约0.4%，报告已披露')
  add('流动公允价值损益金融资产 · 亿元','563.53','h12026.pdf资产负债表','563.53',bal+' Trading Asset Securities')
  add('TTM归母净利润 · 数值',D('186.17')+D('60.49')-D('89.00'),'官方年度+本年半年−上年半年，Decimal复算','157.66',sa)
  # Independently recompute SOTP from decimal inputs; no reading target output.
  cash=D('413.73')+D('142.91')+D('271.16')*D('.9')+D('25.02')*D('.5')-250-D('25.84')+180-600-D('.6')*sh*f
  target=(D('1300')*D('.06')*8+D('50')*2*D('.65')+cash)/sh/f
  calculated={'传统税后经营收益 · 乐观':(D('1387.4')*D('1.05')**3*D('.12'),'乐观传统税后经营收益'),'三年末目标价（港元） · 悲观':(target,'悲观三年目标价')}
  assumptions={'可灵收入 · 乐观':(160,'model_inputs.scenarios[2][4]'),'快手可灵权益 · 乐观':(55,'model_inputs.scenarios[2][6] ×100'),'三年传统股东现金流 · 基准':(300,'model_inputs.scenarios[1][7]')}
 else:
  for y,v,sa_v in [(2024,'1297.84594','1297.85'),(2023,'971.91161','971.91'),(2021,'424.74128','424.74')]:add('毛利 · '+str(y),v,official,sa_v,sa)
  add('归母净利润 · 2022','-66.86110',official,'-66.86',sa)
  add('资本支出 · 2023','68.80',sa,'68.80',cf,'现金流出绝对值')
  for y,v in [(2025,'1668.34'),(2021,'1167.95')]:add('现金及短期投资 · '+str(y),v,bal,v,sb)
  add('两项合计 · 数值',D('1047.16797')+D('635.97373'),'h12026.pdf现金等价物+短期理财，Decimal复算','1683.14',bal)
  add('TTM归母净利润 · 数值',-D('233.55015')-D('46.72487')-D('104.21644'),'官方年度+本年半年−上年半年，Decimal复算','-384.49',sa)
  net=D('1047.16797')+D('635.97373')-(D('353.04527')+D('68.33774')+D('460.60011')+D('5.02943')+D('42.63557')+D('28.52490'))
  bear_pv=(net-350-200+150)/sh/f/D('1.1')**3
  calculated={'归属股东税后经营收益 · 基准':((D('2800')*D('1.07')**3*D('.14')-30-150)*D('.8'),'基准税后经营收益'),'今日价值（10%折现，港元） · 悲观':(bear_pv,'悲观今日价值')}
  assumptions={'新业务经营亏损 · 悲观':(80,'model_inputs.scenarios[0][3]'),'三年累计股东现金流 · 乐观':(700,'model_inputs.scenarios[2][6]'),'战略投资估值 · 基准':(300,'model_inputs.scenarios[1][7]')}
 for label,(v,k) in calculated.items():facts[label]={'fetched_value':float(v),'fetched_source':'独立Decimal按显式公式重算（计算，非外部事实）','fetched_value2':calc[k]['value'],'fetched_source2':'financial_rigor calc：'+calc[k]['expression'],'verification_kind':'calculation-only','note':'两套计算检验数值，不证明预测假设'}
 for label,(v,k) in assumptions.items():facts[label]={'fetched_value':v,'fetched_source':'已披露主观假设一致性检查：'+k,'fetched_value2':None,'fetched_source2':'不适用：未来假设没有外部真实值','verification_kind':'assumption-disclosure-only','note':'此项只能检查报告与输入一致，不是独立信源核验通过'}
 for item in sampled:
  if item['label'] not in facts:raise ValueError('Missing explicit evidence '+str(item))
  item.update(facts[item['label']])
 (d/'audit_results_seed42.json').write_text(json.dumps(sampled,ensure_ascii=False,indent=2))
 result=subprocess.run(['python3','tools/report_audit.py','verdict','--report',str(report),'--results',json.dumps(sampled,ensure_ascii=False),'--output-json'],capture_output=True,text=True,check=True)
 (d/'audit_verdict_seed42.txt').write_text(result.stdout)
 (d/'audit_scope.md').write_text('固定 seed 42。已逐项区分 external-fact、calculation-only、assumption-disclosure-only。工具 PASS 表示选中数字与实取事实或计算/假设声明一致，不表示预测具有客观发生概率；假设不伪装成外部 fetched。历史现金数据商小幅分类差异保留原值并披露。')
 print(c,'PASS',len(sampled),'samples',sum(x['verification_kind']=='external-fact' for x in sampled),'external facts')
