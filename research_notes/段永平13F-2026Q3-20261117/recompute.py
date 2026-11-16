"""Reproduce the two SEC 13F snapshots and compare independently hosted transcripts.

Run from any directory with Python 3. No network access or dependencies required.
Values in the SEC 2026 XML are USD, not thousands of USD. Decimal is used for
ratios; the independently hosted 13f.info endpoint displays truncated USD thousands.
"""
from pathlib import Path
from decimal import Decimal, getcontext
import hashlib
import json
import subprocess
import sys
import xml.etree.ElementTree as ET

getcontext().prec = 40
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
D = Decimal
NAMES = {
    'AAPL':'苹果', 'BRK-B':'伯克希尔B', 'PDD':'拼多多', 'TSLA':'特斯拉',
    'OXY':'西方石油', 'NVDA':'英伟达', 'GOOG':'谷歌C类', 'MSFT':'微软',
    'DIS':'迪士尼', 'UNH':'联合健康', 'CRDO':'Credo', 'SPCX':'SpaceX',
    'PLTR':'Palantir', 'SNPS':'新思科技', 'SNOW':'Snowflake', 'TEM':'Tempus AI',
    'BABA':'阿里巴巴', 'CRCL':'Circle', 'INOD':'Innodata',
}

def fields(node):
    return {e.tag.split('}')[-1]: e.text for e in node.iter()}

def parse(q):
    cover = fields(ET.parse(HERE/'raw'/f'2026{q}-primary_doc.xml').getroot())
    rows = {}
    for item in ET.parse(HERE/'raw'/f'2026{q}-infotable.xml').getroot():
        f = fields(item)
        key = (f['cusip'], f['titleOfClass'], f.get('putCall') or '', f['sshPrnamtType'])
        assert key not in rows, 'Unexpected duplicate: explicitly aggregate if present'
        assert not key[2] and key[3] == 'SH', 'Option/principal row must be handled separately'
        rows[key] = {'issuer':f['nameOfIssuer'], 'cusip':key[0], 'class':key[1],
                     'put_call':key[2], 'share_type':key[3],
                     'shares':int(f['sshPrnamt']), 'value_usd':int(f['value'])}
    total = sum(r['value_usd'] for r in rows.values())
    assert total == int(cover['tableValueTotal'])
    assert len(rows) == int(cover['tableEntryTotal'])
    assert cover['isConfidentialOmitted'] == 'false'
    assert cover['isAmendment'] == 'false'
    return rows, total, cover

q2,t2,c2 = parse('Q2')
q3,t3,c3 = parse('Q3')
checks = []
tickers = {}
for q,rows,total in [('q2',q2,t2),('q3',q3,t3)]:
    other = json.loads((HERE/'raw'/f'{q}_13finfo_data.json').read_text())['data']
    assert len(other) == len(rows)
    for r in other:
        key = (r[3],r[2],r[7] or '', 'SH')
        own = rows[key]
        tickers[r[3]] = r[0]
        assert own['shares'] == r[6], (q,r[0],'shares')
        delta = own['value_usd'] - r[4]*1000
        assert 0 <= delta < 1000, (q,r[0],delta)
        checks.append({'quarter':q,'ticker':r[0], 'shares_exact_match':True,
                       'SEC_value_usd':own['value_usd'],'13f_info_value_usd':r[4]*1000,
                       'value_rounding_difference_usd':delta,
                       'value_difference_pct':str(D(delta)/D(own['value_usd'])*100)})

changes=[]
for key in set(q2)|set(q3):
    a=q2.get(key,{'shares':0,'value_usd':0})
    b=q3.get(key,{'shares':0,'value_usd':0})
    shares=b['shares']-a['shares']
    ticker=tickers[key[0]]
    changes.append({
        'ticker':ticker,'name':NAMES[ticker],'cusip':key[0],'class':key[1],
        'q2_shares':a['shares'],'q3_shares':b['shares'],'delta_shares':shares,
        'q2_disclosed':key in q2,'q3_disclosed':key in q3,
        'share_change_pct':str(D(shares)/a['shares']*100) if a['shares'] else None,
        'q2_value_usd':a['value_usd'],'q3_value_usd':b['value_usd'],
        'q2_weight_pct':str(D(a['value_usd'])/t2*100),
        'q3_weight_pct':str(D(b['value_usd'])/t3*100),
        'weight_change_pp':str(D(b['value_usd'])/t3*100-D(a['value_usd'])/t2*100),
        'action':'新增披露' if not a['shares'] else '退出披露' if not b['shares'] else
                 '增加' if shares>0 else '减少' if shares<0 else '不变',
        'q2_implied_price_usd':str(D(a['value_usd'])/a['shares']) if a['shares'] else None,
        'q3_implied_price_usd':str(D(b['value_usd'])/b['shares']) if b['shares'] else None,
    })
changes.sort(key=lambda r:r['q3_value_usd'],reverse=True)
summary={'q2_total_usd':t2,'q3_total_usd':t3,'total_change_usd':t3-t2,
         'total_change_pct':str(D(t3-t2)/t2*100), 'q2_rows':len(q2),'q3_rows':len(q3),
         'counts':{a:sum(r['action']==a for r in changes) for a in ['增加','减少','不变','新增披露','退出披露']}}
for q,total in [('q2',t2),('q3',t3)]:
    ranked=sorted(changes,key=lambda r:r[f'{q}_value_usd'],reverse=True)
    for n in [2,3,5,10]:
        summary[f'{q}_top{n}_weight_pct']=str(D(sum(r[f'{q}_value_usd'] for r in ranked[:n]))/total*100)

result={'summary':summary,'changes':changes,'cross_checks':checks,
        'source_note':'SEC primary + 13f.info independently hosted transcription; same underlying filing, not independently audited ownership.',
        'missing_row_note':'Zero is a disclosed-table comparison convention only. Missing row does not prove actual zero shares; see SEC FAQ 39 de minimis omission rule.'}
(HERE/'comparison.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
lines=['| 标的 | 二季度股数 | 三季度股数 | 股数变化 | 增减幅度 | 三季度权重 |','|---|---:|---:|---:|---:|---:|']
for r in changes:
    pct=f"{D(r['share_change_pct']):+.2f}%" if r['share_change_pct'] is not None else '新增披露'
    s2=f"{r['q2_shares']:,}" if r['q2_disclosed'] else '未列示'
    s3=f"{r['q3_shares']:,}" if r['q3_disclosed'] else '未再披露'
    delta=f"{r['delta_shares']:+,}" if r['q2_disclosed'] and r['q3_disclosed'] else '—'
    if not r['q3_disclosed']: pct='—'
    lines.append(f"| {r['name']} | {s2} | {s3} | {delta} | {pct} | {D(r['q3_weight_pct']):.2f}% |")
(HERE/'comparison-table.md').write_text('\n'.join(lines)+'\n')

# Run the repository's exact arithmetic/validation CLI and retain every result.
commands=[['calc','--expr',f'({t3}-{t2})/{t2}*100']]
for r in changes:
    if r['q2_shares']:
        commands.append(['calc','--expr',f"({r['q3_shares']}-{r['q2_shares']})/{r['q2_shares']}*100"])
    commands.append(['calc','--expr',f"{r['q3_value_usd']}/{t3}*100"])
for c in checks:
    commands.append(['cross-validate','--field',c['quarter']+'_'+c['ticker']+'_value',
                     '--values',json.dumps({'SEC原始XML':c['SEC_value_usd'],'13f.info转录':c['13f_info_value_usd']}),
                     '--unit','USD','--tolerance','1'])
logs=[]
for cmd in commands:
    p=subprocess.run([sys.executable,str(ROOT/'tools/financial_rigor.py')]+cmd,capture_output=True,text=True)
    assert p.returncode==0,(cmd,p.stderr)
    logs.append({'args':cmd,'output':p.stdout.strip()})
(HERE/'financial_rigor.json').write_text(json.dumps(logs,ensure_ascii=False,indent=2)+'\n')
hashes={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted((HERE/'raw').iterdir()) if p.is_file()}
(HERE/'raw-sha256.json').write_text(json.dumps(hashes,indent=2)+'\n')
print(json.dumps(summary,ensure_ascii=False,indent=2))
print('\n'.join(lines))
print(f'Validated {len(checks)} rows; saved {len(logs)} financial_rigor runs.')
