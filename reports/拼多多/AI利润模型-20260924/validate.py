"""Reproduce arithmetic checks and a classified 15% report audit.

External observations below were retrieved 2026-09-24. This script does NOT
fetch new data or validate the truth of forecasts. Assumptions are checked
only against declared model inputs; qualitative scores are excluded.
"""
import contextlib
import importlib.util
import io
import json
import re
import subprocess
import sys
from decimal import Decimal as D
from pathlib import Path

HERE=Path(__file__).resolve().parent
REPO=HERE.parents[2]
REPORT=HERE.parent/'拼多多-AI与三年十年利润研究-20260924.md'
MODEL=json.loads((HERE/'model-results.json').read_text())
def run(args):
    p=subprocess.run([sys.executable,str(REPO/'tools/financial_rigor.py'),*args],capture_output=True,text=True,check=True)
    return {'args':args,'output':p.stdout,'exit_code':p.returncode}

primary='https://investor.pddholdings.com/static-files/92dafbdc-3125-4f2c-a28f-3d61203efbaf'
q2='https://investor.pddholdings.com/news-releases/news-release-details/pdd-holdings-announces-second-quarter-2026-unaudited-financial'
sa='https://stockanalysis.com/stocks/pdd/financials/'
cap='https://www.marketscreener.com/news/pdd-holdings-inc-reports-earnings-results-for-the-second-quarter-and-six-months-ended-june-30-2026-ce7858dbda8bf527'
fy2023='https://investor.pddholdings.com/news-releases/news-release-details/pdd-holdings-announces-fourth-quarter-2023-and-fiscal-year-2023'
data={
 '2022 revenue':('1305.57589','1305.58',fy2023,sa),
 '2023 revenue':('2476.39205','2476.39',primary,sa),
 '2024 revenue':('3938.36097','3938.36',primary,sa),
 '2025 revenue':('4318.45713','4318.46',primary,sa),
 '2022 operating profit':('304.01921','304.02',fy2023,sa),
 '2023 operating profit':('586.98762','586.99',primary,sa),
 '2024 operating profit':('1084.22862','1084.23',primary,sa),
 '2025 operating profit':('931.02131','931.02',primary,sa),
 '2022 net':('315.38062','315.38',fy2023,sa),
 '2023 net':('600.26544','600.27',primary,sa),
 '2024 net':('1124.34512','1124.35',primary,sa),
 '2025 net':('978.42539','978.43',primary,sa),
 '2022 OCF':('485.07860','485.08',fy2023,sa),
 '2023 OCF':('941.62531','941.63',primary,sa),
 '2024 OCF':('1219.29292','1219.29',primary,sa),
 '2025 OCF':('1069.38690','1069.39',primary,sa),
 '2026H1 revenue':('2185.87','2185.87',q2,cap),
 '2026H1 net':('397.29','397.29',q2,cap),
 '2026Q2 revenue':('1123.58','1123.58',q2,cap),
 '2026Q2 net':('271.82','271.82',q2,cap),
 '2026Q2 cash and short investments':('4564.14','4564.14',q2,sa),
 '2026Q2 cash less leases':('4515.70','4515.70',q2,sa),
 '20260923 USD close':('79.20','79.20','https://stockanalysis.com/stocks/pdd/history/',cap),
}
validation={'cutoff':'2026-09-24','units':'RMB亿元 except price USD','cross_source':[],'tools':[],
 'limitations':['Tool cross-validate uses median and 2%; our release gate uses primary denominator and 1%.',
               'Tool calc evaluates floats; model.py separately computes with Decimal.',
               'Historical facts and forecast assumptions are different audit categories.',
               'Latest precise point-in-time share count and AI ROI remain unverified.']}
for field,(a,b,u1,u2) in data.items():
    diff=abs(D(a)-D(b))/abs(D(a))*100
    assert diff<=1,(field,diff)
    validation['cross_source'].append({'field':field,'primary':a,'secondary':b,'primary_url':u1,'secondary_url':u2,'difference_pct':str(diff),'pass_1pct':True})
    validation['tools'].append(run(['cross-validate','--field',field,'--values',json.dumps({'primary':float(a),'independent':float(b)}),'--unit','亿元 or USD']))

validation['version_difference']={'FY2025_audited_net':'978.42539','preliminary_net':'993.64469',
    'difference_pct':str((D('993.64469')/D('978.42539')-1)*100),
    'resolution':'Use audited annual report, do not average versions; preliminary number is not used as current annual fact.'}
validation['tools'].append(run(['verify-market-cap','--price','78.38','--shares','1423396462','--reported','111570000000','--currency','USD']))
validation['market_cap_check_scope']='20260924 12:26 EDT StockAnalysis snapshot 78.38/111.57bn vs verified legal share count; closing cap at79.20 is separately calculated, not a verified exact close capitalization.'
validation['tools'].append(run(['verify-valuation','--price','79.2','--eps',str(D('920.75539')/D('14.8')/7)]))
for scenario,obj in MODEL['scenarios'].items():
    for r in [*obj['annual'],obj['2036']]:
        e=f"({r['revenue']}*{r['pre_ai_op_margin']}+({r['ai_op']})+{r['finance_pre_tax']})*(1-{r['tax']})"
        validation['tools'].append(run(['calc','--expr',e]))
        independent=(D(r['marketing'])+D(r['transaction']))*D(r['pre_ai_op_margin'])
        independent=(independent+D(r['ai_op'])+D(r['finance_pre_tax']))*(1-D(r['tax']))
        assert independent==D(r['net'])
anchor=D(MODEL['anchor_2026E']['net'])
growth=[(D(MODEL['scenarios'][s]['annual'][-1]['net'])/anchor)**(D(1)/3)-1 for s in ['bull','base','bear']]
validation['tools'].append(run(['three-scenario','--price','79.2','--eps',str(anchor/D('14.8')/7),'--shares','14.8','--growth',*[str(x) for x in growth],'--pe','16','12','8','--years','3','--currency','USD']))
validation['three_scenario_scope']='Equivalent 2026E-to-2029E earnings growth for terminal price cross-check only. Actual stock return horizon is 3.25 years in the report.'
validation['reverse_required_net']={str(pe):str(D('79.2')*(D('1.12')**D('3.25'))*D('14.8')*7/pe) for pe in [12,8]}
(HERE/'validation.json').write_text(json.dumps(validation,ensure_ascii=False,indent=2)+'\n')

spec=importlib.util.spec_from_file_location('report_audit',REPO/'tools/report_audit.py')
audit=importlib.util.module_from_spec(spec); spec.loader.exec_module(audit)
points=audit.extract_data_points(REPORT.read_text())
sample=audit.sample_points(points,ratio=.15,seed=42)
(HERE/'audit-sample.json').write_text(json.dumps(sample,ensure_ascii=False,indent=2)+'\n')
# Explicit, independently inspected mappings. Refuse silently accepting a changed sample.
mapping={
 '经营利润 · 2023':('fact','586.98762',primary,'586.99',sa),
 '经营利润 · 2024':('fact','1084.22862',primary,'1084.23',sa),
 '经营利润 · 2025审计':('fact','931.02131',primary,'931.02',sa),
 '2026Q2归母净利润 · 数值':('fact','271.82',q2,'271.82',cap),
 '2026H1在线营销收入 · 数值':('fact-single-source','1075.73',q2,None,None),
 '同口径TTM经营利润 · 数值':('fact-derived','985.53131','Audited FY2025 931.02131 - H1 2025 418.79 + H1 2026 473.30','985.53',sa),
 '现金及等价物 · 数值':('fact-single-source','1289.18',q2,None,None),
 '毛收益合计 · 税前毛收益/扣减（亿元）':('model-arithmetic',MODEL['ai_bridge_2029']['gross'],'model.py AI bridge, assumptions not facts',None,None),
 '税后贡献 · 计算假设':('assumption','78','Declared 1 - 22% tax assumption',None,None),
 '税后贡献 · 税前毛收益/扣减（亿元）':('model-arithmetic',MODEL['ai_bridge_2029']['net_after_tax'],'model.py AI bridge',None,None),
 '悲观 · 2027':('model-arithmetic','-7.5','-10*(1-.25)',None,None),
 '悲观 · 2029':('model-arithmetic','-18.75','-25*(1-.25)',None,None),
 '基准 · 2029':('model-arithmetic','50.7','65*(1-.22)',None,None),
 '交易服务年增长 · 乐观':('assumption','18','model.inputs.bull.growth[1]',None,None),
 '2027/2028/2029基础经营利润率 · 悲观':('assumption','17.5','Parser reads first year; full sequence17.5/17/16.5 checked against model',None,None),
 '含AI的正常化归母利润 · 2027E':('model-arithmetic',MODEL['scenarios']['base']['annual'][0]['net'],'model.py base2027',None,None),
 '含AI的正常化归母利润 · 2028E':('model-arithmetic',MODEL['scenarios']['base']['annual'][1]['net'],'model.py base2028',None,None),
 '基础交易服务收入（亿元） · 基准':('assumption','5000','model.inputs.base.terminal[1]',None,None),
 '正常化归母净利润（亿元） · 乐观':('model-arithmetic','3140','(13500*.25+350+200)*.8',None,None),
 '悲观 · PE假设':('assumption','8','model.inputs.bear.pe2029',None,None),
 '乐观 · PE假设':('assumption','16','model.inputs.bull.pe2029',None,None),
 '价格超过约97美元 · 对应行动条件':('assumption','12','Declared discount rate12%; parser captured percentage inside action prose',None,None),
}
excluded={
 '供给组织与成本效率 · 研究评分/5':'Qualitative research score, not externally verifiable fact',
 '商业模式与护城河 · 评分/5':'Qualitative research score, not externally verifiable fact',
 '欧盟小包关税 · 模型含义':'Parser captured3 inside a negation; reviewed actual rule: EUR3 per tariff subheading category, not per parcel/item. Official Council source S18.'}
audited=[]; exclusion=[]
for item in sample:
    label=item['label']
    if label in excluded:
        exclusion.append({**item,'reason':excluded[label]}); continue
    category,value,source,value2,source2=mapping[label]
    audited.append({**item,'category':category,'fetched_value':float(value),'fetched_source':source,
                    'fetched_value2':None if value2 is None else float(value2),'fetched_source2':source2})
capture=io.StringIO()
with contextlib.redirect_stdout(capture):
    verdict=audit.render_verdict(audited,report_name=REPORT.name)
(HERE/'audit-verdict.txt').write_text('\n'.join(line.rstrip() for line in re.sub(r'\x1b\[[0-9;]*m', '', capture.getvalue()).splitlines())+'\n')
(HERE/'audit-results.json').write_text(json.dumps({'sample_count':len(sample),'exclusions':exclusion,'checked':audited,'verdict':verdict,'interpretation':'Pass means checked observations/formulas/declared input consistency, not validation of forecasts.'},ensure_ascii=False,indent=2)+'\n')
assert verdict['fail_count']==0 and verdict['warn_count']==0
print(json.dumps({'historical_crosschecks':len(data),'sample_count':len(sample),'checked':len(audited),'excluded':len(exclusion),'verdict':verdict},ensure_ascii=False,indent=2))
