#!/usr/bin/env python3
"""Audit sampled report facts, separately classified computations/assumptions,
and manually enumerate article facts because report_audit cannot parse prose.
Source values below were read from the cited original pages, not copied from
reported_value. Exact arithmetic is Decimal; verdict is delegated to repo tool.
"""
from pathlib import Path
from decimal import Decimal as D
import json,subprocess,hashlib,re
def cleanlog(s):
 return "\n".join(line.rstrip() for line in re.sub(r"\x1b\[[0-9;]*m", "", s).splitlines()).rstrip()+"\n"
ROOT=Path(__file__).resolve().parents[2]; OUT=Path(__file__).resolve().parent
REPORT=ROOT/'reports/腾讯/腾讯-earnings-2026Q3-研究报告-20261118.md'
ARTICLE=ROOT/'reports/腾讯/腾讯-公众号-20261118.md'
Q='https://www.tencent.com/wp-content/uploads/2026/11/C700_3Qresults.pdf'
Q2='https://www.tencent.com/wp-content/uploads/2026/08/C700_IRA.pdf'
J='https://m.jrj.com.cn/madapter/stock/2026/11/18163659194053.shtml'
C=json.loads((OUT/'calculations.json').read_text())
H=json.loads((OUT/'history_financial_data.json').read_text())['series']
yoy=lambda a,b: (D(str(a))/D(str(b))-1)*100
for report,label in [(REPORT,'report'),(ARTICLE,'article')]:
 p=subprocess.run(['python3',str(ROOT/'tools/report_audit.py'),'extract','--report',str(report),'--seed','42'],capture_output=True,text=True,check=True)
 (OUT/(label+'_audit_extract.log')).write_text(cleanlog(p.stdout))
 raw=p.stdout[p.stdout.index('\n[\n')+1:] if '\n[\n' in p.stdout else '[]'
 if label=='report': samples=json.loads(raw)
verified={
 2:(D(192869)/100,Q+' p1','disclosed'),
 7:(D(118433)/100,Q+' p1','disclosed'),
 8:(yoy(115911,118433),Q+' p1; Decimal (115911/118433-1)*100','derived'),
 9:(D(59147)/100,Q+' p1','disclosed'),
 23:(D(68415)/100,Q+' p1; '+Q2+' p1','disclosed'),
 24:(yoy(66519,68415),Q+' p1; Decimal (66519/68415-1)*100','derived'),
 27:(D('6.207'),Q+' p1','disclosed'),
 29:(D('6.947'),Q+' p1,33','disclosed'),
 36:(yoy('7.382','7.581'),Q+' p1; Decimal (7.382/7.581-1)*100','derived'),
 51:(yoy('814.33',587),Q+' p12; Nomura forecast via https://hk.stockstar.com/IG2026111700008107.shtml; same capex definition, individual forecast','derived'),
 58:(D(61),Q+' p7 prior VAS margin (rounded first value of arrow pair)','disclosed'),
 56:(D(63017)/100,Q+' p7','disclosed'),
 57:(yoy(63017,58623),Q+' p7; Decimal (63017/58623-1)*100','derived'),
 63:(D(57),Q+' p7 prior ad margin (rounded first value of arrow pair)','disclosed'),
 60:(yoy(43049,36242),Q+' p6; Decimal (43049/36242-1)*100','derived'),
 71:(D(-1235)/100,Q+' p7,26','disclosed'),
 72:(D(16),Q+' p7 prior other margin (rounded first value of arrow pair)','disclosed'),
 109:(D('34.0')*10,'2025 annual original announcement, liquidity section; history_financial_data.json','disclosed'),
 108:(D('58.5')*10,'2025Q3 original announcement, liquidity section; history_financial_data.json','disclosed'),
 115:(D(146860)/100,'2026Q1 original announcement, liquidity section; history_financial_data.json','disclosed'),
 130:(D(199176)/100,Q+' p21,39','disclosed'),
 140:(D(600),'Analyst configuration calculate.py: stress 2027 cash; assumption, not external fact','assumption'),
 152:(D(1600),'Analyst configuration calculate.py: bull 2027 cash; assumption, not external fact','assumption'),
 158:(D(C['dcf'][1]['hkd_per_share']),'Decimal dated model + independent review_model.md; base value rounded','model_output')
}
assert set(verified)==set(x['id'] for x in samples)
for row in samples:
 val,source,kind=verified[row['id']];row.update(fetched_value=float(val),fetched_source=source,classification=kind)
 if row['id']==9: row.update(fetched_value2=591.47,fetched_source2=J+' independent transcription, same issuer origin')
# Additional high-impact report facts, including numbers not selected at random.
extra=[('Q3 capital expenditure',814.33,814.33,Q+' p12'),('Q3 actual FCF',-691,-691,Q+' p17'),('Q3 ex-prepayment FCF',169,169,Q+' p17'),('Net debt',137.02,D(380101+159328-231717-294010)/100,Q+' p17; arithmetic'),('Q3 OCF',26.52,D(156713-154061)/100,Q+' p24 minus H1 cash flow'),('TTM FCF',78,sum(D(v)*10 for v in H['company_fcf_rmb_b_rounded'][1:]),'Four original quarterly liquidity sections; rounded values'),('TTM adjusted earnings',2675.33,sum(H['nonifrs_attributable_profit_rmb_m'][1:])/100,'Four original announcements'),('TTM adjusted PE',10.77,D(C['ttm_adj_pe']),'Market cap / TTM parent adjusted earnings; Decimal'),('DCF pressure',192,D(C['dcf'][0]['hkd_per_share']),'Conditional model, independent review_model.md'),('DCF base',363,D(C['dcf'][1]['hkd_per_share']),'Conditional model, independent review_model.md'),('DCF bull',692,D(C['dcf'][2]['hkd_per_share']),'Conditional model, independent review_model.md'),('Reverse DCF 2029 cash',2264,D(C['reverse_base_2029_cash_100m']),'Conditional model, independent review_model.md')]
report_results=samples+[{'id':1000+i,'label':label,'reported_value':v,'fetched_value':float(actual),'fetched_source':source,'unit':'see label','classification':'targeted_check'} for i,(label,v,actual,source) in enumerate(extra)]
# Explicit coverage of all decisive article financial claims and definitions.
article_specs=[
 ('调整归母利润',665,D(66519)/100,'亿元',Q+' p1'),('调整归母同比',-6,-6,'%',Q+' p1 rounded'),
 ('收入',2073,D(207336)/100,'亿元',Q+' p1'),('收入同比',8,8,'%',Q+' p1 rounded'),
 ('报告FCF',-691,-691,'亿元',Q+' p17'),('剔预付款FCF',169,169,'亿元',Q+' p17'),('预付款影响差额',860,D(169)-D(-691),'亿元',Q+' p17 rounded difference, not itemized pure AI spend'),
 ('本土游戏收入',476,476,'亿元',Q+' p6'),('本土游戏同比',11,11,'%',Q+' p6'),('国际游戏收入',189,189,'亿元',Q+' p6'),('国际游戏同比',-9,-9,'%',Q+' p6'),('国际固定汇率同比',-4,-4,'%',Q+' p6'),
 ('广告收入同比',19,19,'%',Q+' p6'),('广告毛利率去年',57,57,'%',Q+' p7 rounded'),('广告毛利率本季',52,52,'%',Q+' p7 rounded'),
 ('调整经营利润含新AI',681,D(68073)/100,'亿元',Q+' p1'),('调整经营利润剔新AI',833,833,'亿元',Q+' p8'),('新AI净拖累',152,D(833)-D('680.73'),'亿元',Q+' p8 rounded difference'),('上季新AI净拖累',105,D(861)-D('756.36'),'亿元',Q2+' p8 rounded difference'),('剔新AI经营同比本季',8,8,'%',Q+' p8'),('剔新AI经营同比上季',19,19,'%',Q2+' p8'),
 ('经营现金流取整',26,26,'亿元',Q+' p17 company rounded'),('资本开支付款',651,651,'亿元',Q+' p17'),('媒体内容付款',46,46,'亿元',Q+' p17'),('租赁付款',20,20,'亿元',Q+' p17'),('权责资本开支',814,D(81433)/100,'亿元',Q+' p12'),('上季剔预付款FCF',376,376,'亿元',Q2+' liquidity section'),
 ('云增长',35,35,'%',Q+' p7'),('金科企业服务毛利率',50,50,'%',Q+' p7'),('WorkBuddy日用户下界',1000,1000,'万',Q+' p3: exceeds, recent update not quarter average'),('WorkBuddy日token下界',100,100,'万亿',Q+' p3: exceeds, recent update not quarter average'),
 ('上季净现金',582,D(58191)/100,'亿元',Q+' p17'),('本季净债务',137,D(13702)/100,'亿元',Q+' p17'),('现金定存及其他',5257,D(231717+294010)/100,'亿元',Q+' p17'),('本季回购',70,D('7032259517.04')/100000000,'亿港元',Q+' p44'),('上季回购',169,169,'亿港元',Q2+' repurchase section rounded'),
 ('股价',372.8,D('372.8'),'港元','Tencent + Eastmoney captured quote endpoints'),('人民币市值',2.88,D(C['market_cap_cny'])/1000000000000,'万亿','October monthly shares * close * spot FX; Decimal'),('单季年化PE',10.8,D(C['quarter_annualized_adj_pe']),'倍','Decimal; not TTM or guidance')]
article_results=[{'id':i+1,'label':label,'reported_value':reported,'unit':unit,'fetched_value':float(actual),'fetched_source':source,'classification':'manual_prose_check'} for i,(label,reported,actual,unit,source) in enumerate(article_specs)]
article_text=ARTICLE.read_text()
for row in article_results:
 if row['label'] in ['调整归母利润','收入']:
  row['fetched_value2']=row['fetched_value'];row['fetched_source2']=J+' independent media transcription'
# Primary accounting integrity checks, independent of report rendering.
assert 98326+43049+63655+2306==207336
assert 63017+22578+31551-1235==115911
assert 115911-12144-44077-543==59147
assert 63612+7834-8780+3123+909+429+221-829==66519
assert 231717+294010-380101-159328==-13702
assert D('26')-651-46-20==-691
summary={}
for name,results,report in [('report',report_results,REPORT),('article',article_results,ARTICLE)]:
 (OUT/(name+'_audit_results.json')).write_text(json.dumps(results,ensure_ascii=False,indent=2)+'\n')
 p=subprocess.run(['python3',str(ROOT/'tools/report_audit.py'),'verdict','--results',json.dumps(results,ensure_ascii=False),'--report',report.name,'--output-json'],capture_output=True,text=True)
 (OUT/(name+'_audit_verdict.log')).write_text(cleanlog(p.stdout+p.stderr))
 if p.returncode: raise RuntimeError(name+' audit failed; see verdict log')
 summary[name]={'checked':len(results),'report_sha256':hashlib.sha256(report.read_bytes()).hexdigest(),'note':'report: 24 seeded samples incl assumptions plus 12 targeted; article: tool extracted zero prose points, manual 39 checks; PASS validates numbers, not completeness or forecasts'}
(OUT/'audit_summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(summary,ensure_ascii=False,indent=2))
