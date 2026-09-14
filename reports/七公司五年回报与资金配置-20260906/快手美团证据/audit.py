from pathlib import Path
from decimal import Decimal as D
import json
import subprocess

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
raw=(HERE/'audit-extract-seed42.txt').read_text()
sample=json.loads(raw[raw.index('[\n'):])
results=json.loads((HERE/'decimal-results.json').read_text())
facts=[]
models=[]
for r in sample:
    i=r['id']
    if i==4:
        r.update(fetched_value=61.754848,fetched_source='Official Meituan August monthly return: (5596331814+579152986)/1e8',fetched_value2=61.754848,fetched_source2='Tencent quote snapshot: reports/美团/审计-20260906/tencent_quote.txt; exact shares match official latest monthly return')
        facts.append(r)
    elif i==5:
        r.update(fetched_value=float(results['快手']['market_cap_cny_100m']),fetched_source='Decimal:33.66*43.26961215*0.86458',fetched_value2=float(D('1456.4551')*D('.86458')),fetched_source2='Tencent independently reported HKD market cap1456.4551 hundred-million * same stated FX; derived value, not a second FX observation')
        facts.append(r)
    else:
        values={14:14,12:7,15:40,18:-20,29:288.5,32:16,36:.8,55:-140,68:.5,74:float(D(results['美团']['scenarios']['乐观']['terminal_wealth_cagr'])*100)}
        r.update(fetched_value=values[i],fetched_source='Model input or 48-digit Decimal reproduction; not external evidence of future outcome',fetched_value2=values[i],fetched_source2='financial-rigor.txt formula or declared model input transcription; not a second historical source')
        models.append(r)
for name,rows in [('facts',facts),('models',models)]:
    (HERE/f'audit-{name}-seed42.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n')
    p=subprocess.run(['python3',str(ROOT/'tools/report_audit.py'),'verdict','--results',json.dumps(rows,ensure_ascii=False),'--report',f'快手与美团五年底稿-{name}'],capture_output=True,text=True,check=True)
    (HERE/f'audit-{name}-verdict-seed42.txt').write_text(p.stdout)
scope={'sample_size':len(sample),'fact_or_current_derived':len(facts),'future_assumption_or_arithmetic':len(models),'boundary':'PASS confirms sampled transcription/calculation only. Future earnings, valuation multiples, FCF, dividend and dilution are assumptions, not verified forecasts. Price was independently re-accessed on Investing plus FT/StockAnalysis; exact shares were independently re-downloaded from official issuer PDFs. Tencent exact market-cap/share copy is a prior same-day snapshot checked against new official source, not freshly retrieved in this agent run.'}
(HERE/'audit-scope.json').write_text(json.dumps(scope,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(scope,ensure_ascii=False))
