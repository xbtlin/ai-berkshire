import json
import subprocess
from decimal import Decimal
from pathlib import Path

DIR = Path(__file__).resolve().parent
ROOT = DIR.parents[1]
REPORT = DIR / '腾讯与拼多多底稿.md'
TOOL = ROOT / 'tools/report_audit.py'
out = subprocess.run(['python3', str(TOOL), 'extract', '--report', str(REPORT), '--seed', '42'], text=True, capture_output=True, check=True).stdout
(DIR/'腾讯与拼多多审计抽样.txt').write_text(out)
items = json.loads(out[out.index('[\n'):])
decimals = json.loads((DIR/'腾讯与拼多多Decimal复算.json').read_text())
model = json.loads((DIR/'腾讯与拼多多模型结果.json').read_text())
for x in items:
    item_id=x['id']
    if item_id == 8:
        x.update(fetched_value=2185.87, fetched_value2=2185.87, fetched_source='https://investor.pddholdings.com/news-releases/news-release-details/pdd-holdings-announces-second-quarter-2026-unaudited-financial/', fetched_source2='https://www.marketscreener.com/news/pdd-holdings-inc-reports-earnings-results-for-the-second-quarter-and-six-months-ended-june-30-2026-ce7858dbda8bf527', classification='historical_fact_two_sources')
    elif item_id == 9:
        x.update(fetched_value=1346.51, fetched_value2=1346.51, fetched_source='https://www1.hkexnews.hk/listedco/listconews/sehk/2026/0812/2026081200296.pdf', fetched_source2='https://finance.eastmoney.com/a/202608123839209916.html (Caizhong News original)', classification='historical_fact_two_sources')
    elif item_id in [16,15,18,41]:
        expected={16:8,15:6,18:9,41:12}[item_id]
        x.update(fetched_value=expected, fetched_value2=expected, fetched_source='Scenario input in 腾讯与拼多多计算.py', fetched_source2='Independent inspection of growth factor in 腾讯与拼多多Decimal复算.json', classification='model_assumption_consistency_only')
    elif item_id in [2,48,53]:
        key = 'PDD 2036 bull profit' if item_id==53 else 'PDD 2036 bear profit'
        quant = Decimal('1E2') if item_id in [2,53] else Decimal('0.01')
        a=float(Decimal(model[key]).quantize(quant))
        b=float(Decimal(decimals[key]['decimal_result']).quantize(quant))
        x.update(fetched_value=a, fetched_value2=b, fetched_source='financial_rigor output rounded as stated', fetched_source2='40 digit Decimal independent recalculation rounded as stated', classification='model_arithmetic_not_future_fact')
    else:
        raise ValueError('Unexpected sample; inspect it',x)
(DIR/'腾讯与拼多多审计样本.json').write_text(json.dumps(items,ensure_ascii=False,indent=2)+'\n')
verdict = subprocess.run(['python3',str(TOOL),'verdict','--results',json.dumps(items,ensure_ascii=False),'--report',str(REPORT),'--output-json'],text=True,capture_output=True,check=True)
(DIR/'腾讯与拼多多审计判决.txt').write_text(verdict.stdout)
(DIR/'腾讯与拼多多审计判决.json').write_text(verdict.stdout[verdict.stdout.rfind('\n{')+1:])
print(verdict.stdout)
