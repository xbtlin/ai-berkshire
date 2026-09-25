"""Verify sampled observations and arithmetic without treating forecasts as facts."""
from pathlib import Path
from decimal import Decimal as D
import json
import re
import subprocess
import sys

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
REPORT=HERE.parent/'泡泡玛特-investment-team-AI利润与竞争格局-20260925.md'
sys.path.insert(0,str(ROOT/'tools'))
from report_audit import extract_data_points, sample_points

annual='https://www.hkexnews.hk/listedco/listconews/sehk/2026/0421/2026042100395_c.pdf'
interim='https://www1.hkexnews.hk/listedco/listconews/sehk/2026/0820/2026082000353.pdf'
stock='https://stockanalysis.com/quote/hkg/9992/financials/'
etnet='https://www.etnet.com.hk/www/tc/stocks/realtime/quote_ci_pl.php?code=9992'
# Observations were read independently from the named public sources.
facts={
 9:('63.01002',annual,'63.01',stock),
 23:('50.38384',interim,'50.38384',etnet),
 27:('47.09630',interim,'47.1','https://www.xinhuanet.com/tech/20250820/662517765fb040baafc93ec4ef647d24/c.html'),
 24:('11.90519',annual,'11.91','https://www.jiemian.com/article/10943681.html'),
 29:('61.3',annual,'61.32',stock),
 36:('108.65152',annual,'108.65','https://stockanalysis.com/quote/hkg/9992/financials/cash-flow-statement/'),
 130:('371.20052',annual,'371.20',stock),
 140:('50.38384',interim,'50.38384',etnet),
}
# Recompute with a different implementation: profit = r * [m + (s+g-c-i)*.741].
def profit(r,m,s,g,c,i):
    return D(r)*(D(m)+(D(s)+D(g)-D(c)-D(i))*D('.741'))
p27=profit('430','.275','.004','.002','.001','.0015')
p28=profit('480','.27','.007','.004','.0015','.0015')
p29=profit('535','.265','.01','.008','.0025','.0025')
maths={51:D(480)*D('.27'),58:p29,56:p27,57:p28,
       60:(p28/(D(480)*D('.27'))-1)*100,
       63:D(480)*D('.007'),71:-D(480)*D('.0015'),72:-D(535)*D('.0025'),
       109:D(60)*D('.23'),155:D(480)+D(360)}
classified=[]; results=[]
for item in sample_points(extract_data_points(REPORT.read_text()),.15,42):
    ident=item['id']
    if ident in facts:
        v,s,v2,s2=facts[ident]
        out=dict(item,kind='observed_fact',fetched_value=float(v),fetched_source=s,
                 fetched_value2=float(v2),fetched_source2=s2)
        results.append(out)
    elif ident in maths:
        out=dict(item,kind='conditional_model_arithmetic_only',fetched_value=float(maths[ident]),
                 fetched_source='audit.py independent Decimal arithmetic, NOT external forecast evidence')
        results.append(out)
    elif ident in [7,8,108]:
        out=dict(item,kind='subjective_score_or_forecast_input',note='Not externally verifiable; no fabricated fetched value')
    elif ident in [2,41,115]:
        out=dict(item,kind='parser_false_positive_year',note='Year/fiscal label was parsed as a financial value')
    else:
        raise ValueError(f'New sample requires review: {item}')
    classified.append(out)
HERE.joinpath('audit-classification.json').write_text(json.dumps(classified,ensure_ascii=False,indent=2)+'\n')
HERE.joinpath('audit-results.json').write_text(json.dumps(results,ensure_ascii=False,indent=2)+'\n')
log=subprocess.check_output([sys.executable,str(ROOT/'tools/report_audit.py'),'verdict','--results',json.dumps(results),
                             '--report',REPORT.name],text=True)
plain_log=re.sub(r'\x1b\[[0-9;]*m','',log)
HERE.joinpath('audit-verdict.txt').write_text('\n'.join(line.rstrip() for line in plain_log.splitlines())+'\n')
# Stricter supplemental checks for material unsampled model/market results.
model=json.loads(HERE.joinpath('model-results.json').read_text())
assert D(model['ai_bridge'][2]['ai_net_parent']) == p29-D(535)*D('.265')
assert D(model['valuation']['market_cap_hkd']) == D('151.1')*D('13.31779203')
assert D(model['ai_3year_total']) == (p27-D(430)*D('.275'))+(p28-D(480)*D('.27'))+(p29-D(535)*D('.265'))
assert [D(x['net_profit']) for x in model['scenarios2036']] == [D(60),D(225),D(420),D(20)]
for item in results:
    for key in ['fetched_value','fetched_value2']:
        if item.get(key) is not None:
            assert abs(D(str(item[key]))-D(str(item['reported_value'])))/abs(D(str(item[key]))) <= D('.01')
print(log)
print('Supplemental arithmetic and strict 1% source checks passed. No forecast assumption was empirically validated.')
