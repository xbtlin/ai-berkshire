"""Audit the main report's seed-42 sample, separating history from assumptions."""
from pathlib import Path
from decimal import Decimal as D
import json
import subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
raw = (HERE/'主报告抽检.txt').read_text()
sample = json.loads(raw[raw.index('[\n'):])
model = json.loads((HERE/'统一模型.json').read_text())
facts, assumptions = [], []
keymap = {'保守':'bear','基准':'base','乐观':'bull'}
for row in sample:
    left, label = row['label'].split(' · ', 1)
    if label == '起始价格':
        assert left == '美团', 'Review any newly sampled historical fact manually'
        row.update(fetched_value=81.75,
            fetched_source='https://www.investing.com/equities/meituan-dianping-historical-data ; regular close 2026-09-04, live inspected in this task',
            fetched_value2=81.75,
            fetched_source2='https://stockanalysis.com/quote/hkg/3690/history/ ; same close, live inspected in this task')
        facts.append(row)
        continue
    if left.startswith('三只股票'):
        k = next(value for word,value in keymap.items() if word in left)
        val = D(model['portfolios']['reference_pool']['scenarios'][k]['cagr'])*100
    else:
        if '/' in left:
            name, scenario = left.split('/')
            k = keymap[scenario]
        else:
            name = left
            k = next((value for word,value in keymap.items() if word in label), 'base')
        s = model['companies'][name]['scenarios'][k]
        if '年化' in label: val = D(s['cagr'])*100
        elif '股数' in label: val = D(s['shares'])/D('1e8')
        elif '股息' in label: val = D(s['dividends'])
        elif '终点' in label: val = D(s['terminal_price'])
        elif '利润' in label: val = D(s['profit_cny_yi'])
        elif name == 'MiniMax' and label == '退出估值':
            # Extractor captured revenue in a mixed text cell, not the PS multiple.
            val = D(s['revenue_cny_yi'])/D(model['fx_cny_per_usd'])
            row['audit_note'] = 'Extracted 50 USD hundred-million revenue assumption, not 3x PS.'
        elif '倍数' in label or '估值' in label: val = D(s['multiple'])
        else: raise ValueError(row)
    # Display rounding allows up to half of the shown final decimal place.
    tolerance = D('.051') if row['unit']=='%' else D('.0051')
    if '股数' in label: tolerance = D('.000051')
    assert abs(val-D(str(row['reported_value']))) <= tolerance, (row, val)
    row.update(fetched_value=float(val),
        fetched_source='统一模型.json: 48-digit Decimal formula/declared model assumption; NOT historical evidence',
        fetched_value2=float(val),
        fetched_source2='统一计算核验.json: financial_rigor formula agreement or input transcription; NOT independent evidence of future outcome')
    assumptions.append(row)

for name, data in [('历史事实',facts), ('假设与算术',assumptions)]:
    (HERE/f'主报告抽检-{name}.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
    out = subprocess.run(['python3',str(ROOT/'tools/report_audit.py'),'verdict','--results',
        json.dumps(data,ensure_ascii=False),'--report','五年回报与资金配置-'+name],
        capture_output=True,text=True,check=True)
    (HERE/f'主报告抽检-{name}-判决.txt').write_text(out.stdout)

# Check every generated scenario row, beyond the random sample.
text = (HERE/'五年回报与资金配置报告-20260906.md').read_text()
count = 0
for name,c in model['companies'].items():
    for cn,k in keymap.items():
        s = c['scenarios'][k]
        expected = f"| {name}/{cn} | {D(s['profit_cny_yi']):.2f} | {s['multiple']}{'PS' if s['method']=='equity_PS' else 'PE'} | {D(s['shares'])/D('1e8'):.4f} | {D(s['dividends']):.2f} | {D(s['terminal_price']):.2f} | {D(s['cagr'])*100:.1f}% |"
        assert expected in text, expected
        count += 1
assert count == 21
print(json.dumps({'sample_count':len(sample),'historical_facts':len(facts),
    'assumptions_or_arithmetic':len(assumptions),'all_scenario_rows_checked':count,
    'boundary':'No scenario probability or future financial outcome has been verified.'},ensure_ascii=False))
