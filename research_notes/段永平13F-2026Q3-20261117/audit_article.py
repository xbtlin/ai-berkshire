"""Audit every extracted table datum against SEC and the 13f.info transcript.

Source values are normalized to the article's displayed precision. Exact values
are retained alongside them. This avoids treating 0.01% versus 0.0095% as an
economic error while still requiring correct rounding for every table cell.
"""
from pathlib import Path
from decimal import Decimal, ROUND_HALF_UP
import hashlib
import importlib.util
import json
import re
import subprocess
import sys

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
REPORT=ROOT/'reports/段永平/段永平-2026Q3持仓变化-公众号-20261117.md'
spec=importlib.util.spec_from_file_location('audit',ROOT/'tools/report_audit.py')
audit=importlib.util.module_from_spec(spec);spec.loader.exec_module(audit)
D=Decimal
comp=json.loads((HERE/'comparison.json').read_text())
rows={r['name']:r for r in comp['changes']}
other={q:{r[0]:r for r in json.loads((HERE/'raw'/f'{q}_13finfo_data.json').read_text())['data']} for q in ['q2','q3']}
total3=sum(r[4]*1000 for r in other['q3'].values())
text=REPORT.read_text()
points=audit.extract_data_points(text)
result=[]
for p in points:
    if ' · ' in p['label']:
        name,field=p['label'].split(' · ')
    elif p['label']=='SpaceX 是本次两季对照中的新增条目':
        name,field='SpaceX','三季度末股数'
    else:
        raise AssertionError(('Unmapped prose point',p))
    r=rows[name];a=other['q2'].get(r['ticker']);b=other['q3'][r['ticker']]
    if field=='二季度末股数': v1,v2,precision=r['q2_shares'],a[6],'1'
    elif field=='三季度末股数': v1,v2,precision=r['q3_shares'],b[6],'1'
    elif field=='净变化': v1,v2,precision=r['delta_shares'],b[6]-a[6],'1'
    elif field=='幅度': v1,v2,precision=D(r['share_change_pct']),D(b[6]-a[6])/a[6]*100,'.01'
    elif field=='市值（亿美元）': v1,v2,precision=D(r['q3_value_usd'])/10**8,D(b[4])/10**5,'.001'
    elif field=='组合权重': v1,v2,precision=D(r['q3_weight_pct']),D(b[4]*1000)/total3*100,'.01'
    else: raise AssertionError(('Unmapped field',p))
    v1,v2=D(v1),D(v2)
    norm1=v1.quantize(D(precision),rounding=ROUND_HALF_UP)
    norm2=v2.quantize(D(precision),rounding=ROUND_HALF_UP)
    reported=D(str(p['reported_value']))
    assert reported==norm1==norm2,(p,norm1,norm2)
    result.append({'id':p['id'],'label':p['label'],'reported_value':str(reported),'unit':p['unit'],
        'line_number':p['line_number'],'raw_text':p['raw_text'],
        'fetched_value':str(norm1),'fetched_source':'SEC原始XML，按文章显示精度舍入',
        'fetched_value2':str(norm2),'fetched_source2':'13f.info两季独立转录，按文章显示精度舍入',
        'source_exact_value':str(v1),'source2_exact_value':str(v2),'display_quantum':precision})
table_count=sum(' · ' in p['label'] for p in points)
assert table_count==56 and len(result)==57,('Unexpected data point count',table_count,len(result))
for target in re.findall(r'!\[[^\]]*\]\(([^)]+)\)',text):
    assert (REPORT.parent/target).is_file(),target
assert all(word not in text for word in ['每股估值','自身期末估值','[图X','TODO'])
(HERE/'audit-results.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
ex=subprocess.run([sys.executable,str(ROOT/'tools/report_audit.py'),'extract','--report',str(REPORT),'--ratio','1','--seed','42'],capture_output=True,text=True,check=True)
(HERE/'audit-extract.txt').write_text('\n'.join(line.rstrip() for line in ex.stdout.splitlines())+'\n')
ver=subprocess.run([sys.executable,str(ROOT/'tools/report_audit.py'),'verdict','--results',json.dumps(result,ensure_ascii=False),'--report',REPORT.name,'--output-json'],capture_output=True,text=True,check=True)
clean_verdict=re.sub(r'\x1b\[[0-9;]*m','',ver.stdout)
(HERE/'audit-verdict.txt').write_text('\n'.join(line.rstrip() for line in clean_verdict.splitlines())+'\n')
assert '"verdict": "PASS"' in ver.stdout
manifest={'article':str(REPORT.relative_to(ROOT)), 'sha256':hashlib.sha256(REPORT.read_bytes()).hexdigest(),
          'extracted_table_data_points':table_count,'validated_table_data_points':table_count,
          'additional_prose_data_points':len(result)-table_count,'validated_total_data_points':len(result),
          'skipped':0,'source_rows_cross_checked':len(comp['cross_checks']),
          'note':'Arithmetic and transcription audit, not independent verification of actual asset ownership. Prose additionally reviewed by editor, reader and parent agent.'}
(HERE/'audit-manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(manifest,ensure_ascii=False,indent=2))
