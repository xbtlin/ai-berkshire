#!/usr/bin/env python3
"""Scoped reproducible arithmetic. Inputs are facts or explicitly named assumptions."""
import ast
import json
import subprocess
from decimal import Decimal, getcontext
from pathlib import Path

getcontext().prec = 40
OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[2]
TOOL = ROOT / 'tools/financial_rigor.py'

def decimal_eval(expr):
    def visit(node):
        if isinstance(node, ast.Expression):
            return visit(node.body)
        if isinstance(node, ast.Num):
            return Decimal(str(node.n))
        if isinstance(node, ast.Constant):
            return Decimal(str(node.value))
        if isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.USub):
            return -visit(node.operand)
        if isinstance(node, ast.BinOp):
            a, b = visit(node.left), visit(node.right)
            if isinstance(node.op, ast.Add): return a+b
            if isinstance(node.op, ast.Sub): return a-b
            if isinstance(node.op, ast.Mult): return a*b
            if isinstance(node.op, ast.Div): return a/b
            if isinstance(node.op, ast.Pow): return a**b
        raise ValueError('Unsupported expression')
    return visit(ast.parse(expr, mode='eval'))

expressions = {
 'pop_2025_revenue_CNY100m':'37120052 / 100000',
 'pop_2025_parent_profit_CNY100m':'12775689 / 100000',
 'pop_H1_revenue_CNY100m':'17172921 / 100000',
 'pop_H1_parent_profit_CNY100m':'5038384 / 100000',
 'pop_2025_parent_margin':'12775689 / 37120052 * 100',
 'pop_H1_parent_margin':'5038384 / 17172921 * 100',
 'mini_2025_revenue_USD100m':'79038 / 100000',
 'mini_2025_parent_profit_USD100m':'-1871617 / 100000',
 'mini_H1_revenue_USD100m':'116573 / 100000',
 'mini_H1_parent_profit_USD100m':'-357997 / 100000',
 'mini_2025_adjusted_minus_SBC_USDm':'-250.856 - 24.031',
 'mini_H1_adjusted_minus_SBC_USDm':'-293.031 - 28.208',
 'mini_2025_operating_proxy_USDm':'-250.856 - 24.031 - 40.369',
 'mini_H1_operating_proxy_USDm':'-293.031 - 28.208 - 8.039',
 'mini_2025_H2_gross_margin':'(20.079-3.685)/(79.038-30.429)*100',
 'mini_H1_gross_margin':'20.813/116.573*100',
 'mini_H1_enterprise_mix':'73.929/116.573*100',
 'mini_H1_RD_over_revenue':'296.870/116.573',
 'pop_bear_revenue_CNY100m':'(20000000*600+10000000*800)/100000000+10',
 'pop_base_revenue_CNY100m':'(35000000*1000+30000000*1300)/100000000+40',
 'pop_bull_revenue_CNY100m':'(50000000*1300+60000000*1600)/100000000+90',
 'pop_bear_profit_CNY100m':'210*(0.55-0.35)*(1-0.25)*(1-0.02)',
 'pop_base_profit_CNY100m':'780*(0.67-0.31)*(1-0.25)*(1-0.02)',
 'pop_bull_profit_CNY100m':'1700*(0.70-0.29)*(1-0.25)*(1-0.02)',
 'pop_failure_profit_CNY100m':'100*(0.40-0.50)*0.98',
 'mini_bear_revenue_USD100m':'(10000*60000+10000000*40)/100000000',
 'mini_base_revenue_USD100m':'(100000*70000+30000000*100)/100000000',
 'mini_bull_revenue_USD100m':'(200000*100000+50000000*200)/100000000',
 'mini_bear_pretax_USD100m':'10*0.25-6-2',
 'mini_base_pretax_USD100m':'100*0.50-25-10',
 'mini_bull_pretax_USD100m':'300*0.60-70-30',
 'mini_bear_profit_USD100m':'(10*0.25-6-2)*1',
 'mini_base_profit_USD100m':'(100*0.50-25-10)*(1-0.25)',
 'mini_bull_profit_USD100m':'(300*0.60-70-30)*(1-0.25)',
 'mini_bear_profit_CNY100m':'(10*0.25-6-2)*7',
 'mini_base_profit_CNY100m':'(100*0.50-25-10)*(1-0.25)*7',
 'mini_bull_profit_CNY100m':'(300*0.60-70-30)*(1-0.25)*7',
 'mini_base_at_H1_margin_profit_CNY100m':'(100*(20.813/116.573)-25-10)*7',
 'mini_base_breakeven_GM_percent':'(25+10)/100*100',
}

cross = [
 ('pop_2025_revenue', {'HKEX':37120.052,'StockAnalysis':37120}, 'CNY_million'),
 ('pop_2025_parent_profit', {'HKEX':12775.689,'StockAnalysis':12776}, 'CNY_million'),
 ('pop_H1_revenue', {'HKEX':17172.921,'Finet':17173}, 'CNY_million'),
 ('pop_H1_parent_profit', {'HKEX':5038.384,'Finet':5038}, 'CNY_million'),
 ('pop_H1_members_repurchase', {'HKEX':51.6,'Yicai':51.6}, 'percent'),
 ('mini_2025_revenue', {'HKEX':79.038,'StockAnalysis':79.04}, 'USD_million'),
 ('mini_2025_parent_profit', {'HKEX':-1871.617,'StockAnalysis':-1872}, 'USD_million'),
 ('mini_H1_revenue', {'HKEX_live_PDF':116.573,'Reuters':116.6}, 'USD_million'),
 ('mini_H1_parent_profit', {'HKEX_live_PDF':-357.997,'Reuters':-358}, 'USD_million'),
 ('mini_H1_adjusted_profit', {'HKEX_live_PDF':-293.031,'EEO':-293.0}, 'USD_million'),
 ('mini_H1_RD', {'HKEX_live_PDF':296.870,'EEO':296.9}, 'USD_million'),
 ('mini_H1_enterprise_revenue', {'HKEX_live_PDF':73.929,'Reuters':73.9}, 'USD_million'),
 ('mini_H1_product_revenue', {'HKEX_live_PDF':42.644,'Reuters':42.6}, 'USD_million'),
]
logs, results = [], {}
for name, expr in expressions.items():
    p = subprocess.run(['python3', str(TOOL), 'calc','--expr',expr], text=True, capture_output=True, check=True)
    dec = decimal_eval(expr)
    line = next(x for x in p.stdout.splitlines() if '精确值:' in x)
    tool_value = Decimal(line.split('精确值:',1)[1].strip())
    delta = abs(tool_value-dec)
    tolerance = max(Decimal('0.000000001'),abs(dec)*Decimal('0.000000000001'))
    assert delta <= tolerance, (name, tool_value, dec)
    results[name] = {'expression':expr,'decimal_result':str(dec),'tool_result':str(tool_value),'absolute_delta':str(delta),'within_tolerance':True}
    logs.append(name+'\n'+p.stdout)
for name, values, unit in cross:
    p = subprocess.run(['python3',str(TOOL),'cross-validate','--field',name,'--values',json.dumps(values),'--unit',unit], text=True, capture_output=True,check=True)
    logs.append(p.stdout)
    vals = [Decimal(str(x)) for x in values.values()]
    assert abs(vals[0]-vals[1])/abs(vals[0]) <= Decimal('0.01')
(OUT/'financial-rigor.txt').write_text('\n\n'.join(logs))
(OUT/'decimal-checks.json').write_text(json.dumps(results,ensure_ascii=False,indent=2)+'\n')
(OUT/'cross-inputs.json').write_text(json.dumps(cross,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:v['decimal_result'] for k,v in results.items()},ensure_ascii=False,indent=2))
