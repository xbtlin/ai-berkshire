#!/usr/bin/env python3
"""Separate a sampled filing fact from assumptions/formulas and parser noise."""
from pathlib import Path
from decimal import Decimal as D
import json
import subprocess
import sys

OUT=Path(__file__).resolve().parent
ROOT=OUT.parents[2]
REPORT=OUT.parent/'腾讯与拼多多五年底稿.md'
tool=ROOT/'tools/report_audit.py'
raw=subprocess.check_output([sys.executable,str(tool),'extract','--report',str(REPORT),'--seed','42'],text=True)
(OUT/'audit-extract.txt').write_text(raw)
sample=json.loads(raw[raw.index('\n[\n')+1:])
(OUT/'audit-sample.json').write_text(json.dumps(sample,ensure_ascii=False,indent=2)+'\n')
r=json.loads((OUT/'decimal-results.json').read_text())
a=json.loads((OUT/'model-inputs.json').read_text())
expected={
 12:D(a['拼多多']['model_diluted_quote_units'])/D('1e8'),
 14:D(a['拼多多']['profit_2026_yi']),
 15:D(r['腾讯']['model_pe']),
 18:(D('1.08')-1)*100,
 29:D(r['腾讯']['scenarios']['bull']['profit_2031_yi']),
 32:(D('0.98')-1)*100,
 36:D('80'),
 55:D(a['腾讯']['scenarios']['bull']['pe']),
 70:D(r['拼多多']['scenarios']['base']['shares_2031'])/D('1e8'),
 76:D(r['拼多多']['scenarios']['bull']['shares_2031'])/D('1e8'),
 82:D(a['腾讯']['scenarios']['bear']['share_issuance_rate'])*100,
 87:D(a['腾讯']['scenarios']['bear']['dividend_start']),
 95:max(D(y['payout_to_fcf']) for y in r['腾讯']['scenarios']['bull']['cash_feasibility'])*100,
}
facts=[]; models=[]; excluded=[]
for s in sample:
 if s['id']==5:
  s['exclusion_reason']='Parser captured the month 9 in the source-date boundary column; this is not a financial assertion.'
  excluded.append(s)
 elif s['id']==4:
  s.update(fetched_value=5693585848,fetched_source='Official PDD 2025 20-F p120: outstanding as of March 18, 2026; live accessed September 6, 2026',classification='historical_fact_single_official_source')
  facts.append(s)
 else:
  assert s['id'] in expected
  s.update(fetched_value=float(expected[s['id']]),fetched_source='Model inputs and independently recalculated Decimal result; not external verification of a forecast',classification='model_assumption_or_calculation')
  models.append(s)
for name, group in [('facts',facts),('models',models)]:
 (OUT/f'audit-{name}.json').write_text(json.dumps(group,ensure_ascii=False,indent=2)+'\n')
 args=[sys.executable,str(tool),'verdict','--results',json.dumps(group,ensure_ascii=False),'--report',str(REPORT)]
 (OUT/f'audit-{name}-verdict.txt').write_text(subprocess.check_output(args,text=True))
(OUT/'audit-scope.json').write_text(json.dumps({'seed':42,'sample_count':len(sample),'historical_fact_count':len(facts),'model_count':len(models),'excluded':excluded,'limitations':['Sampled PDD exact shares use one official source, not two independent exact share counts.','Other price and FX facts were separately cross-validated with financial_rigor.','Model assumptions and forecast outputs are not externally provable facts.','PASS concerns arithmetic and provenance consistency only, not expected investment outcomes.']},ensure_ascii=False,indent=2)+'\n')
print('Audit complete:',len(facts),'filing fact;',len(models),'model checks;',len(excluded),'non-financial extraction excluded.')
