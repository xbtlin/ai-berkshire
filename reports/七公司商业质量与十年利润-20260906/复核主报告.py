"""Recompute the 21 scenarios and classify the report-audit sample.

This validates arithmetic and cited historical values, not forecast assumptions.
"""
from pathlib import Path
from decimal import Decimal, localcontext, ROUND_HALF_UP
import ast
import json
import re
import subprocess

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[1]
REPORT = OUT / '七公司对比研究报告-20260906.md'

MODELS = {
    '腾讯': [
        '3900*1**10*0.25+1650*1.02**10*0.25+2400*1**10*0.12+50-100',
        '3900*1.06**10*0.32+1650*1.09**10*0.35+2400*1.06**10*0.18+250-50',
        '3900*1.08**10*0.36+1650*1.12**10*0.40+2400*1.09**10*0.22+350-50'],
    '拼多多': [
        '2200*1**10*0.25+2350*0.98**10*(-0.03)+40',
        '2200*1.05**10*0.35+2350*1.08**10*0.06+80',
        '2200*1.08**10*0.40+2350*1.12**10*0.13+120'],
    '阿里巴巴': [
        '(10000*0.12+6000*0.08+100*(-1)-100-150)*0.75+100',
        '(14000*0.18+10000*0.18+500*0+100-250)*0.75+150',
        '(19000*0.22+18000*0.25+2000*0.20+300-400)*0.75+200'],
    '美团': ['3500*0.06-80-180-20','(5000*0.13+30-180-20)*0.8','(7000*0.17+150-220-30)*0.8'],
    '快手': ['872*0.05+60*(-0.10)*0.60-20','1722*0.12+300*0.20*0.50-10','2485*0.15+800*0.25*0.40'],
    '泡泡玛特': ['210*(0.55-0.35)*0.75*0.98','780*(0.67-0.31)*0.75*0.98','1700*(0.70-0.29)*0.75*0.98'],
    'MiniMax': ['(10*0.25-6-2)*7','(100*0.50-25-10)*0.75*7','(300*0.60-70-30)*0.75*7'],
}
ROUNDING = {'腾讯':[100,100,100], '拼多多':[10,100,100], '阿里巴巴':[100,100,100],
            '美团':[10,10,10], '快手':[10,10,10], '泡泡玛特':[10,10,10], 'MiniMax':[10,10,10]}

def exact_expr(expr):
    def visit(node):
        if isinstance(node, ast.Num):
            return Decimal(str(node.n))
        if isinstance(node, ast.Constant):
            return Decimal(str(node.value))
        if isinstance(node, ast.UnaryOp):
            x = visit(node.operand)
            return -x if isinstance(node.op, ast.USub) else x
        if isinstance(node, ast.BinOp):
            a,b = visit(node.left),visit(node.right)
            if isinstance(node.op, ast.Add): return a+b
            if isinstance(node.op, ast.Sub): return a-b
            if isinstance(node.op, ast.Mult): return a*b
            if isinstance(node.op, ast.Div): return a/b
            if isinstance(node.op, ast.Pow) and b == int(b): return a**int(b)
        raise ValueError(ast.dump(node))
    with localcontext() as ctx:
        ctx.prec = 40
        return visit(ast.parse(expr, mode='eval').body)

def run(args):
    return subprocess.run(['python3', *args], cwd=ROOT, text=True, capture_output=True, check=True).stdout

report_text = REPORT.read_text()
results = []
for company, expressions in MODELS.items():
    forecast_row = next(line for line in report_text.splitlines() if line.startswith('| '+company+' |') and re.match(r'^\| '+re.escape(company)+r' \| -?\d+ \| -?\d+ \| -?\d+ \|',line))
    displayed = [Decimal(x.strip()) for x in forecast_row.split('|')[2:5]]
    for i,expr in enumerate(expressions):
        value = exact_expr(expr)
        output = run(['tools/financial_rigor.py','calc','--expr',expr])
        tool_value = Decimal(re.search(r'精确值:\s*(\S+)',output).group(1))
        assert abs(value-tool_value) < Decimal('0.000001')
        increment = Decimal(ROUNDING[company][i])
        rounded = (value/increment).quantize(Decimal('1'),rounding=ROUND_HALF_UP)*increment
        assert displayed[i] == rounded,(company,displayed[i],rounded)
        results.append({'company':company,'scenario':['保守','基准','乐观'][i], 'expression':expr,
                        'Decimal_value':str(value),'display_rounding_increment':str(increment),
                        'displayed':str(rounded),'tool_output':output,'verified':True})
(OUT/'主表21情景复算.json').write_text(json.dumps(results,ensure_ascii=False,indent=2)+'\n')

sample_text = run(['tools/report_audit.py','extract','--report',str(REPORT),'--seed','42'])
(OUT/'主报告抽样.txt').write_text(sample_text)
sample = json.loads(sample_text[sample_text.index('[\n  {'):])
facts,assumptions = [],[]
for row in sample:
    label = row['label']
    if label == '腾讯 · 最新一期归母净利润':
        row.update(fetched_value=1141.15,fetched_source='HKEX https://www1.hkexnews.hk/listedco/listconews/sehk/2026/0812/2026081200296.pdf',
                   fetched_value2=1141.15,fetched_source2='S&P Capital IQ https://www.marketscreener.com/news/tencent-holdings-limited-reports-earnings-results-for-the-second-quarter-and-six-months-ended-june-3-ce7859d8db80f42d')
        facts.append(row)
    elif label == '阿里巴巴 · 最近完整年度归母净利润':
        row.update(fetched_value=1059.04,fetched_source='HKEX https://www.hkexnews.hk/listedco/listconews/sehk/2026/0618/2026061800844.pdf',
                   fetched_value2=1059.04,fetched_source2='https://stockanalysis.com/stocks/baba/financials/')
        facts.append(row)
    elif label == '美团 · 最新一期归母净利润':
        row.update(fetched_value=-46.72487,fetched_source='HKEX https://www.hkexnews.hk/listedco/listconews/sehk/2026/0828/2026082800436_c.pdf',
                   fetched_value2=None,fetched_source2='',source_gap='第三方只核验集团亏损-46.72036亿元，不能充当精确归母第二源。')
        facts.append(row)
    elif '情景' in label:
        company,scenario = label.split(' · ')
        calc = next(x for x in results if x['company']==company and x['scenario']+'情景'==scenario)
        assumptions.append({**row,'type':'forecast_arithmetic_only','expression':calc['expression'],
                            'exact_model_value':calc['Decimal_value'],'rounded_model_value':calc['displayed'],
                            'verified':Decimal(calc['displayed'])==Decimal(str(row['reported_value']))})
    else:
        raise ValueError('Unclassified sample '+label)
(OUT/'主报告事实抽样核验.json').write_text(json.dumps(facts,ensure_ascii=False,indent=2)+'\n')
(OUT/'主报告模型抽样核验.json').write_text(json.dumps(assumptions,ensure_ascii=False,indent=2)+'\n')
verdict = run(['tools/report_audit.py','verdict','--results',json.dumps(facts,ensure_ascii=False),'--report',str(REPORT)])
(OUT/'主报告事实抽样判决.txt').write_text(verdict)
print('21 scenarios: Decimal/financial_rigor agreement; all main-table rounding verified.')
print('Seed 42 sample: 3 historical facts (2 dual-source, 1 single-source qualified); 3 forecast arithmetic checks.')
