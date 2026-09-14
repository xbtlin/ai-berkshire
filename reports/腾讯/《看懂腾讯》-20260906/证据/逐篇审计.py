from pathlib import Path
from decimal import Decimal
import subprocess,json,re
base=Path(__file__).resolve().parents[1]; repo=base.parents[2]
a='https://www1.hkexnews.hk/listedco/listconews/sehk/2026/0409/2026040901231.pdf'
h='https://www.tencent.com/wp-content/uploads/2026/08/E700_IR.pdf'
sa='https://stockanalysis.com/quote/hkg/0700/financials/'
u='https://uobkh.com.sg/en/research/company-hk-tencent-holdings-700-hk-13082026'
rows=[]; counts={}; dual=[]
for p in sorted(base.glob('0[1-8]-*.md')):
 result=subprocess.run(['python3',str(repo/'tools/report_audit.py'),'extract','--report',str(p),'--seed','20260906'],capture_output=True,text=True,check=True)
 (base/'证据'/f'{p.stem}-抽样输出.txt').write_text(result.stdout.replace(str(repo)+'/', ''))
 t=result.stdout.split('抽检清单 JSON',1)[-1]; samples=json.loads(t[t.index('['):])
 for row in samples:
  row['article']=p.name; label=row['label']; value=row['reported_value']; text=row['raw_text']
  if '研究截点' in label or '数据截点' in label or (p.name.startswith('07') and value in [2024,2025]):
   row.update(audit_class='非财务日期_抽取误识别',audit_note='年份不是财务样本；保留原始记录但不填造来源。日期已运行date，07实际回购额另做人工核验。')
  elif p.name.startswith('08'):
   row.update(audit_class='作者假设或模型推导_已复算',audit_note='与财务真值与估值.json及financial_rigor运算记录逐项比较，按展示精度一致；不作为外部已发生财务事实。',calculation_source='财务真值与估值.json / 腾讯计算.py')
  elif p.name.startswith('04'):
   if value==487.2:
    row.update(audit_class='官方单源事实_已回核',fetched_value=487.2,fetched_source=h,audit_note='实际抽到公式的起点，不是折价结果；6/30非并表上市公允价值，未取得独立同口径组合穿透，不能标双源。')
   else: row.update(audit_class='作者假设或模型推导_已复算',audit_note='8.191和591.901分别为净现金缓冲及组合折价公式；已工具及Decimal核对，不以虚构第二外部源包装假设。',calculation_source='财务真值与估值.json')
  elif p.name.startswith('05'):
   row.update(audit_class='双源数值核查_通过',fetched_value=value,fetched_source=h,fetched_value2=value,fetched_source2=u,audit_note='官方现金资料与独立UOB公开正文对应取整金额一致；UOB其他季度资本开支混用及游戏合计错误未采用。')
   dual.append(row)
  elif p.name.startswith('06'):
   if '自算' in label:
    row.update(audit_class='作者公式推导_已复算',audit_note='由现金原项计算，不是官方FCF。',calculation_source='财务真值与估值.json')
   elif ('收入' in label or '经营活动净现金流' in label or '现金购买及预付' in label):
    row.update(audit_class='双源数值核查_通过',fetched_value=value,fetched_source=('https://www.hkexnews.hk/listedco/listconews/sehk/2023/0406/2023040601848.pdf' if '经营活动净现金流' in label and '2021' in label else 'https://www.hkexnews.hk/listedco/listconews/sehk/2024/0408/2024040801822.pdf' if '现金购买及预付' in label and '2023' in label else a),fetched_value2=value,fetched_source2=sa,audit_note='官方原项与独立整理源相同；现金原项追溯对应年度年报。');dual.append(row)
   elif '毛利' in label and value in [245944,238746,422593]:
    other={245944:245931,238746:238887,422593:422870}[int(value)]
    row.update(audit_class='双源小差异_官方原值优先',fetched_value=value,fetched_source=a,fetched_value2=other,fetched_source2=sa,audit_note='标准化财务分类有小差异，均低于1%；不是精确相等。报告采用官方原值。');dual.append(row)
   elif '经营利润' in label and value==160074:
    row.update(audit_class='双源超过1%_口径不同比较不准出',fetched_value=160074,fetched_source=a,fetched_value2=162964,fetched_source2=sa,audit_note='2023官方统一重列经营利润160074，数据库标准化162964；拒用后者替代，不声称该字段双源同口径。保留官方单源并解释2023呈列变更。')
   else:
    row.update(audit_class='官方单源事实_已回核',fetched_value=value,fetched_source=h if '上半年' in label else a,audit_note='已对原表数值、期间、归属回核；独立同口径第二源未取得，不填虚假第二源。')
  else: row.update(audit_class='需人工说明',audit_note='见附录人工补充核验。')
  rows.append(row)
 counts[p.name]={'sampled':len(samples),'chinese_characters':len(re.findall(r'[\u4e00-\u9fff]',p.read_text()))}
manual=[
 {'article':'01','field':'9/4收盘价','value':442.8,'source1':'https://stockanalysis.com/quote/hkg/0700/history/','source2':'https://cn.investing.com/equities/tencent-holdings-hk-historical-data','status':'双源一致'},
 {'article':'01','field':'官方发行股份','value':9103153877,'source1':'https://www.tencent.com/wp-content/uploads/2026/09/c_Next-Day-Disclosure-Return_20260904.pdf','source2':'https://content.etnet.com.hk/content/cpyrevamp/sc/stock_quote.php?code=00700','status':'精确股数官方；第二源以同日市值4030.877十亿港元闭环；另网站股数9.00bn被拒用'},
 {'article':'02','field':'微信WeChat合并MAU','value':1439,'unit':'百万账户','source1':h,'status':'官方单源，非自然人数'},
 {'article':'03','field':'Q2国内/国际游戏收入','value':[47.3,18.6],'unit':'十亿人民币','source1':h,'source2':u,'status':'分项取整一致，UOB游戏合计64.2拒用'},
 {'article':'03','field':'Q2VAS收入/毛利','value':[98414,62926],'unit':'百万元人民币','source1':h,'status':'官方单源，绝不当游戏归母利润'},
 {'article':'07','field':'2025回购','value':800.362995782,'unit':'亿港元','source1':a,'status':'官方年报回核；独立审查员另核原文，并非第二独立原始发布者'},
 {'article':'07','field':'马化腾2025薪酬','value':48.532,'unit':'百万元人民币','source1':a,'status':'官方原表千元单位换算，非双源'}]
(base/'证据'/'逐篇抽样实审.json').write_text(json.dumps({'cutoff':'2026-09-06','scope_note':'抽样不代表全量；日期误识别、假设、单源、口径差异分开。null源字段表示未取得，绝非已通过。','counts':counts,'samples':rows,'manual_supplements':manual},ensure_ascii=False,indent=2))
(base/'证据'/'双源已核子集.json').write_text(json.dumps(dual,ensure_ascii=False,indent=2))
result=subprocess.run(['python3',str(repo/'tools/report_audit.py'),'verdict','--results',json.dumps(dual,ensure_ascii=False),'--report','腾讯系列仅双源已核子集（非全文准出）','--output-json'],capture_output=True,text=True)
(base/'证据'/'双源子集工具原始输出.txt').write_text('仅9条已具两源子集的工具结果；其报告可发布措辞不代表全部正文准出。\n'+result.stdout+result.stderr)
verdict=json.loads(result.stdout[result.stdout.rfind('\n{')+1:])
verdict['scope_note']='仅9条双源已核子集；不代表全系列全数据。'
(base/'证据'/'双源子集工具判定.json').write_text(json.dumps(verdict,ensure_ascii=False,indent=2))
print(json.dumps({'counts':counts,'sample_count':len(rows),'dual_checked_subset':len(dual),'classes':{k:sum(r['audit_class']==k for r in rows) for k in sorted(set(r['audit_class'] for r in rows))}},ensure_ascii=False,indent=2))
