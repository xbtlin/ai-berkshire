#!/usr/bin/env python3
"""Seed-42 sampling: historical facts and assumptions are separate verdicts."""
import importlib.util
import json
import subprocess
from pathlib import Path
from decimal import Decimal as D

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
REPORT=HERE.parent/'泡泡玛特与MiniMax五年底稿.md'
TOOL=ROOT/'tools/report_audit.py'
spec=importlib.util.spec_from_file_location('report_audit',TOOL)
mod=importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
sample=mod.sample_points(mod.extract_data_points(REPORT.read_text()),seed=42)
run=subprocess.run(['python3',str(TOOL),'extract','--report',str(REPORT),'--seed','42'],text=True,capture_output=True,check=True)
(HERE/'audit-extract.txt').write_text(run.stdout)
r=json.loads((HERE/'calculations.json').read_text())
facts={
 4:(349235308,'https://www1.hkexnews.hk/listedco/listconews/sehk/2026/0903/2026090301230.pdf',349240000,'https://stockanalysis.com/quote/hkg/0100/statistics/'),
 5:(float(D('154')*D('1331779203')/D('1e8')),'HKEX legal shares times live 154 HKD quote',2050.94,'https://www.lixinger.com/equity/company/detail/hk/09992/9992/announcement?type=mr'),
 12:(float((D('79.038')-D('30.429')+D('116.573'))/100),'HKEX 2025 annual and H1 2026: TTM arithmetic',1.65,'https://stockanalysis.com/quote/hkg/0100/financials/'),
}
models={15:'950',14:'550',18:'70',29:str(D('1331779203')/D('1e8')),32:r['pop_base_cash_dividend_HKD']['decimal_result'],36:r['pop_bull_exit_HKD']['decimal_result'],55:r['mini_bear_profit_CNY100m']['decimal_result'],70:r['mini_bear_CAGR_percent']['decimal_result'],76:'20',82:str(D(r['mini_bear_future_cash_equity_proceeds_USDb']['decimal_result'])*10),87:str(D(r['mini_bull_residual_cash_USDb']['decimal_result'])*10)}
actual, model=[],[]
for point in sample:
    p=dict(point)
    if p['id'] in facts:
        p['fetched_value'],p['fetched_source'],p['fetched_value2'],p['fetched_source2']=facts[p['id']]
        p['classification']='historical_fact_or_historical_arithmetic'
        actual.append(p)
    elif p['id'] in models:
        p['fetched_value']=float(D(models[p['id']]))
        p['fetched_source']='Explicit input or financial_rigor with independent Decimal arithmetic; no forecast verified'
        p['classification']='assumption_or_model_arithmetic_only'
        model.append(p)
    else: raise RuntimeError(p)
for label,data in [('facts',actual),('model',model)]:
    (HERE/('audit-'+label+'.json')).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
    run=subprocess.run(['python3',str(TOOL),'verdict','--report',REPORT.name+' '+label+' only','--results',json.dumps(data,ensure_ascii=False)],text=True,capture_output=True,check=True)
    (HERE/('audit-'+label+'-verdict.txt')).write_text(run.stdout)
    print(run.stdout[-550:])
(HERE/'audit-scope.json').write_text(json.dumps({'sample_count':len(sample),'historical_facts':len(actual),'model_consistency_only':len(model),'seed':42,'forecast_validated':False,'full_current_H1_cash_flow_statement_obtained':False},ensure_ascii=False,indent=2)+'\n')
