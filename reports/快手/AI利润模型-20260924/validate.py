"""Review sampled report facts separately from assumptions and arithmetic.
The financial_rigor toolkit validates arithmetic, NOT forecast truth.
"""
import json, subprocess, sys
from pathlib import Path
from decimal import Decimal as D
P=Path(__file__).resolve().parent
ROOT=P.parents[2]
r=json.loads((P/'model-results.json').read_text())
sample=json.loads((P/'audit-sample.json').read_text())
b=r['scenarios']['base']; bull=r['scenarios']['bull']; bear=r['scenarios']['bear']
# Independently transcribed source fields, RMB100m. Single-source fields labelled.
facts={
23:(2.36,'Company 2026H1: (69251/67654-1)*100',2.36,'China Securities Journal 2026-09-03'),
24:(89.00,'Company 2026H1 comparative equity-holder earnings RMB8900m',None,None),
27:(101.98,'Company Q2 full announcement pp2/22: comparative RMB10198m',None,None),
29:(55.1,'Company 2026H1 comparative gross margin',55.1,'2025H1 statement; same issuer, not independent'),
36:(23.23,'Company cash flow comparative: 1-9044/11781',23.23,'China Securities Journal 2026-09-03'),
51:(297.87,'Company 2025 annual cash flow comparative RMB29787m',297.87,'StockAnalysis cash-flow statement'),
56:(float(D(1213)-D('273.62')-D('116.72')-D('252.48')),'Arithmetic using interim notes; financing notes official single source',None,None),
}
# These checks compare report transcription to disclosed model, not external verification.
models={7:b['annual'][2]['net'],8:b['terminal2036']['net'],9:bull['annual'][0]['net'],
71:D(r['anchor2026']['core_baseline_margin'])*100,109:bear['annual'][2]['kling_revenue'],130:b['annual'][2]['kling_operating'],
140:bull['annual'][0]['kling_fixed_cost'],144:bull['annual'][1]['kling_operating'],152:b['annual'][2]['ai_bridge']['ai_core_net'],
155:bear['annual'][0]['incremental_ai_net'],164:bear['terminal2036']['advertising_baseline'],167:bear['terminal2036']['live'],
174:b['terminal2036']['core_baseline_revenue'],180:b['terminal2036']['core_ai_operating'],184:bull['terminal2036']['finance'],
190:bull['terminal2036']['kling_revenue'],189:b['terminal2036']['kling_revenue'],218:8}
exclusions={58:'Seedance version, not a financial quantity',60:'Veo version, not a financial quantity',63:'Wan version, not a financial quantity',227:'Subjective conditional price range; not observed fact',228:'Subjective conditional price range; not observed fact'}
fa=[]; ma=[]; ex=[]
for x in sample:
 i=x['id']; y=dict(x)
 if i in facts:
  v,source,v2,s2=facts[i];y.update(fetched_value=v,fetched_source=source,fetched_value2=v2,fetched_source2=s2 or '',type='historical_fact_or_fact_arithmetic');fa.append(y)
 elif i in models:
  v=float(models[i]); assert abs(v-x['reported_value'])<=.006,(i,v,x)
  y.update(fetched_value=v,fetched_source='model-results.json, assumption/calculation only',fetched_value2=None,fetched_source2='',type='model_not_external_fact');ma.append(y)
 else:
  assert i in exclusions,i;y['reason']=exclusions[i];ex.append(y)
(P/'audit-facts.json').write_text(json.dumps(fa,ensure_ascii=False,indent=2)+'\n')
(P/'audit-model.json').write_text(json.dumps(ma,ensure_ascii=False,indent=2)+'\n')
(P/'audit-exclusions.json').write_text(json.dumps(ex,ensure_ascii=False,indent=2)+'\n')
checks=[]
for scenario,v in r['scenarios'].items():
 for row in v['annual']+[v['terminal2036']]:
  # Reconstruct shareholder earnings from segments, including loss-tax asymmetry.
  f=lambda k:D(str(row[k]))
  kop=f('kling_revenue')*f('kling_contribution_margin')-f('kling_fixed_cost')
  knet=kop*D('.8') if kop>0 else kop
  independently=(f('core_baseline_revenue')*f('core_baseline_margin')+f('core_ai_operating')+f('finance'))*(1-f('core_tax'))+knet*f('kling_share')
  assert abs(independently-f('net'))<D('.000001')
  checks.append({'scenario':scenario,'year':row['year'],'reconstructed_net':str(independently),'passed':True})
assert abs(sum(D(x['incremental_ai_net']) for x in b['annual'])-D('78.5410993179625'))<D('.00001')
assert D(r['audit_math']['h1_fcf'])==D('-88.97')
(P/'validation.json').write_text(json.dumps({'segment_reconciliation':checks,'sample_facts':len(fa),'sample_model':len(ma),'sample_nonfinancial_exclusions':len(ex),'forecast_truth_verified':False},ensure_ascii=False,indent=2)+'\n')
logs=[]
def run(args):
 z=subprocess.run([sys.executable,'tools/financial_rigor.py']+args,cwd=ROOT,text=True,capture_output=True,check=True)
 logs.append('COMMAND: financial_rigor.py '+' '.join(args)+'\n'+z.stdout)
run(['cross-validate','--field','2026H1 revenue','--values',json.dumps({'issuer':692.51,'China Securities Journal':692.51}),'--unit','亿元'])
run(['cross-validate','--field','2026H1 attributable earnings','--values',json.dumps({'issuer':60.49,'China Securities Journal':60.49}),'--unit','亿元'])
run(['cross-validate','--field','2026H1 CFO','--values',json.dumps({'issuer':90.44,'China Securities Journal':90.44,'Tiger rounded':90.4}),'--unit','亿元'])
run(['cross-validate','--field','2026H1 capex payments','--values',json.dumps({'issuer':179.41,'Tiger rounded':179.4}),'--unit','亿元'])
run(['cross-validate','--field','2025 attributable earnings','--values',json.dumps({'issuer':186.17,'StockAnalysis':186.17,'MarketScreener':186.17}),'--unit','亿元'])
run(['cross-validate','--field','2026-09-24 price','--values',json.dumps({'StockAnalysis':30.5,'Investing':30.5}),'--unit','HKD'])
run(['verify-market-cap','--price','30.50','--shares','4.33e9','--reported','131.96e9','--currency','HKD'])
run(['calc','--expr','90.44-179.41'])
run(['calc','--expr','(1950*.18+45+20)*.85+(500*.5-150)*.8*.65'])
run(['calc','--expr','1213-273.62-116.72-252.48'])
run(['calc','--expr','204.471*(1+.08*5)'])
# Scenario toolkit uses 3-year equivalent growth for cross-check only; main PV uses 3.25y.
eps=D(r['anchor2026']['net'])/44*D('1.1')
run(['verify-valuation','--price','30.5','--eps',str(eps)])
growth=[(D(r['scenarios'][n]['annual'][-1]['net'])/D(r['anchor2026']['net']))**(D(1)/3)-1 for n in ['bull','base','bear']]
run(['three-scenario','--price','30.5','--eps',str(eps),'--shares','44','--growth',*[str(g) for g in growth],'--pe','16','12','8','--years','3','--currency','HKD'])
(P/'financial-rigor.txt').write_text('\n'.join(logs))
for kind,data in [('facts',fa),('model',ma)]:
 z=subprocess.run([sys.executable,'tools/report_audit.py','verdict','--results',json.dumps(data,ensure_ascii=False),'--report',f'Kuaishou20260924-{kind}'],cwd=ROOT,text=True,capture_output=True,check=True)
 (P/f'audit-{kind}-verdict.txt').write_text(z.stdout)
print(json.dumps({'facts':len(fa),'model':len(ma),'excluded_nonfinancial':len(ex),'segment_checks':len(checks),'passed':True}))
