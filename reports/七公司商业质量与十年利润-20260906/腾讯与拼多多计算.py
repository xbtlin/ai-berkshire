"""Only subprocess financial_rigor performs financial calculations; no market pricing."""
import json
import re
import subprocess
from decimal import Decimal, getcontext
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
TOOL = ROOT / 'tools/financial_rigor.py'
records = []

def run(name, args):
    result = subprocess.run(['python3', str(TOOL), *args], text=True, capture_output=True, check=True)
    item = {'name': name, 'args': args, 'output': result.stdout}
    match = re.search(r'精确值:\s*(\S+)', result.stdout)
    if match:
        item['result'] = match.group(1)
    records.append(item)
    return item.get('result')

checks = [
    ('Tencent FY2025 revenue', 751766, 751766, 'HKEX', 'StockAnalysis'),
    ('Tencent FY2025 IFRS attributable profit', 224842, 224842, 'HKEX', 'StockAnalysis'),
    ('Tencent H12026 revenue', 401243, 401243, 'HKEX', 'SP_Capital_IQ'),
    ('Tencent H12026 IFRS attributable profit', 114115, 114115, 'HKEX', 'SP_Capital_IQ'),
    ('PDD FY2025 revenue audited', 431845.713, 431846, '20F', 'StockAnalysis'),
    ('PDD FY2025 attributable profit audited', 97842.539, 97843, '20F', 'StockAnalysis'),
    ('PDD H12026 revenue', 218587, 218587, 'PDD_IR', 'SP_Capital_IQ'),
    ('PDD H12026 GAAP attributable profit', 39729, 39729, 'PDD_IR', 'SP_Capital_IQ'),
    ('PDD H12026 cash and short investments', 456414, 456414, 'PDD_IR', 'StockAnalysis'),
]
for name, a, b, sa, sb in checks:
    run(name, ['cross-validate','--field',name,'--values',json.dumps({sa:a,sb:b}),'--unit','RMB million'])

expressions = {
    'Tencent FY2025 revenue yi': '751766/100',
    'Tencent FY2025 profit yi': '224842/100',
    'Tencent FY2025 nonIFRS yi': '259626/100',
    'Tencent H12026 revenue yi': '401243/100',
    'Tencent H12026 profit yi': '114115/100',
    'Tencent H12026 nonIFRS yi': '136320/100',
    'Tencent H12026 operating profit yi': '134651/100',
    'Tencent H12026 SBC included attributable yi': '14949/100',
    'Tencent FY2025 repurchase and cash dividend yi': '(73312+37535)/100',
    'Tencent H12026 repurchase and cash dividend yi': '(22257+41595)/100',
    'Tencent TTM normalized bridge yi': '(259626+136320-124381-30756)/100-108.09',
    'PDD FY2025 revenue yi': '431845.713/100',
    'PDD FY2025 profit yi': '97842.539/100',
    'PDD FY2025 operating profit yi': '93102.131/100',
    'PDD H12026 revenue yi': '218587/100',
    'PDD H12026 profit yi': '39729/100',
    'PDD H12026 operating profit yi': '47330/100',
    'PDD H12026 nonGAAP yi': '42560/100',
    'PDD H12026 SBC yi': '(42560-39729)/100',
    'PDD FY2025 adjusted audit difference yi': '(99364.469-97842.539)/100',
    'PDD FY2025 operating margin pct': '93102.131/431845.713*100',
    'PDD FY2024 operating margin pct': '108422.862/393836.097*100',
    'PDD H12026 cash investments yi': '(128918+327496)/100',
    'PDD normalized bridge yi': '(93102.131+47330-41879)/100*0.8+80-18.425048',
    'Tencent model 2026 income check': '3900*0.32+1650*0.35+2400*0.16+200-100',
    'PDD model 2026 income check': '2200*0.35+2350*0+80',
    'Tencent 2036 bear profit': '3900*1**10*0.25+1650*1.02**10*0.25+2400*1**10*0.12+50-100',
    'Tencent 2036 base profit': '3900*1.06**10*0.32+1650*1.09**10*0.35+2400*1.06**10*0.18+250-50',
    'Tencent 2036 bull profit': '3900*1.08**10*0.36+1650*1.12**10*0.40+2400*1.09**10*0.22+350-50',
    'PDD 2036 bear profit': '2200*1**10*0.25+2350*0.98**10*(-0.03)+40',
    'PDD 2036 base profit': '2200*1.05**10*0.35+2350*1.08**10*0.06+80',
    'PDD 2036 bull profit': '2200*1.08**10*0.40+2350*1.12**10*0.13+120',
    'Tencent 2036 bear revenue': '3900*1**10+1650*1.02**10+2400*1**10',
    'Tencent 2036 base revenue': '3900*1.06**10+1650*1.09**10+2400*1.06**10',
    'Tencent 2036 bull revenue': '3900*1.08**10+1650*1.12**10+2400*1.09**10',
    'PDD 2036 bear revenue': '2200*1**10+2350*0.98**10',
    'PDD 2036 base revenue': '2200*1.05**10+2350*1.08**10',
    'PDD 2036 bull revenue': '2200*1.08**10+2350*1.12**10',
}
values = {key: run(key, ['calc','--expr',value]) for key,value in expressions.items()}
getcontext().prec = 40
decimal_checks = {}
for key, expr in expressions.items():
    decimal_expr = re.sub(r'\b\d+(?:\.\d+)?\b', lambda m: 'Decimal('+repr(m.group(0))+')', expr)
    exact = eval(decimal_expr, {'__builtins__':{},'Decimal':Decimal})
    residual = abs(Decimal(values[key])-exact)
    assert residual < Decimal('0.0000001'), (key, residual)
    decimal_checks[key] = {'expression':expr,'decimal_result':str(exact),'tool_result':values[key], 'absolute_residual':str(residual), 'pass': True}
(OUT / '腾讯与拼多多Decimal复算.json').write_text(json.dumps(decimal_checks, ensure_ascii=False, indent=2)+'\n')
(OUT / '腾讯与拼多多计算记录.json').write_text(json.dumps(records, ensure_ascii=False, indent=2)+'\n')
(OUT / '腾讯与拼多多计算记录.txt').write_text('\n'.join(x['name']+'\n'+x['output'] for x in records))
(OUT / '腾讯与拼多多模型结果.json').write_text(json.dumps(values, ensure_ascii=False, indent=2)+'\n')
print(json.dumps(values, ensure_ascii=False, indent=2))
