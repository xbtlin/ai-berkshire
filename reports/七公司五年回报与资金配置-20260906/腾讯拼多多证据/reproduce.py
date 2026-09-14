#!/usr/bin/env python3
"""Reproduce five-year scenarios with financial_rigor and independent Decimal."""
from decimal import Decimal as D, getcontext
import json
from pathlib import Path
import subprocess
import sys

getcontext().prec = 40
OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[2]
TOOL = ROOT / 'tools/financial_rigor.py'
records = []

def call(label, args):
    result = subprocess.run([sys.executable, str(TOOL), *map(str, args)], capture_output=True, text=True, check=True)
    if '不安全' in result.stdout or '❌' in result.stdout:
        raise RuntimeError(result.stdout)
    records.append({'label': label, 'args': args, 'output': result.stdout})

def calc(label, expr, expected):
    call(label, ['calc', '--expr', expr])
    raw = records[-1]['output'].split('精确值:')[-1].strip().splitlines()[0]
    if abs(D(raw) - expected) > max(D('0.00001'), abs(expected)*D('1e-12')):
        raise ValueError((label, raw, str(expected)))
    return str(expected)

def dec_expr(expr):
    import re
    return eval(re.sub(r'(?<![A-Za-z_])(?:\d+\.\d+|\d+)', lambda m: f'D("{m[0]}")', expr), {'D': D, '__builtins__': {}})

inputs = {
 '腾讯': {
   'price': '442.8', 'fx_rmb_per_quote': '0.86458', 'currency': 'HKD',
   'issued_quote_units': '9103153877', 'issued_as_of': '2026-09-04',
   'model_diluted_quote_units': '9200000000', 'profit_2026_yi': '2309.5',
   'scenarios': {
    'bear': {'profit_expression': '3900*0.25+1650*1.02**5*0.25+2400*0.12+50-100', 'pe': '12', 'net_share_change': '0', 'gross_buyback_rate': '0.01', 'share_issuance_rate': '0.01', 'dividend_start': '4', 'dividend_growth': '0', 'fcf_conversion': '0.55'},
    'base': {'profit_expression': '3900*1.06**5*0.32+1650*1.09**5*0.35+2400*1.06**5*0.17+225-75', 'pe': '18', 'net_share_change': '-0.01', 'gross_buyback_rate': '0.02', 'share_issuance_rate': '0.01', 'dividend_start': '5.3', 'dividend_growth': '0.05', 'fcf_conversion': '0.75'},
    'bull': {'profit_expression': '3900*1.08**5*0.34+1650*1.12**5*0.375+2400*1.09**5*0.19+275-75', 'pe': '22', 'net_share_change': '-0.015', 'gross_buyback_rate': '0.025', 'share_issuance_rate': '0.01', 'dividend_start': '5.3', 'dividend_growth': '0.10', 'fcf_conversion': '0.85'},
   },
 },
 '拼多多': {
   'price': '82.21', 'fx_rmb_per_quote': '6.7787', 'currency': 'USD',
   'issued_quote_units': '1423396462', 'issued_as_of': '2026-03-18 (also 2025-12-31); not an exact 2026-09-04 share count',
   'ordinary_per_ads': '4', 'model_diluted_quote_units': '1480000000', 'profit_2026_yi': '850',
   'scenarios': {
    'bear': {'profit_expression': '2200*0.25+2350*0.98**5*(-0.03)+40', 'pe': '8', 'net_share_change': '0.015', 'gross_buyback_rate': '0', 'share_issuance_rate': '0.015', 'dividend_start': '0', 'dividend_growth': '0', 'fcf_conversion': '0.60'},
    'base': {'profit_expression': '2200*1.05**5*0.35+2350*1.08**5*0.03+80', 'pe': '12', 'net_share_change': '0.01', 'gross_buyback_rate': '0', 'share_issuance_rate': '0.01', 'dividend_start': '0', 'dividend_growth': '0', 'fcf_conversion': '0.80'},
    'bull': {'profit_expression': '2200*1.08**5*0.375+2350*1.12**5*0.065+100', 'pe': '16', 'net_share_change': '0.005', 'gross_buyback_rate': '0', 'share_issuance_rate': '0.005', 'dividend_start': '0', 'dividend_growth': '0', 'fcf_conversion': '0.90'},
   },
 }
}

results = {}
for name, a in inputs.items():
    px, fx, issued, n0, p0 = (D(a[k]) for k in ['price', 'fx_rmb_per_quote', 'issued_quote_units', 'model_diluted_quote_units', 'profit_2026_yi'])
    call(name+'市值', ['verify-market-cap', '--price', str(px), '--shares', str(issued), '--reported', str(px*issued), '--currency', a['currency']])
    mcap = px*issued*fx/D('1e8')
    calc(name+'人民币市值亿元', f'{px}*{issued}*{fx}/1e8', mcap)
    eps0 = p0*D('1e8')/n0/fx
    call(name+'正常化模型PE', ['verify-valuation', '--price', str(px), '--eps', str(eps0)])
    results[name] = {'mcap_rmb_yi': str(mcap), 'model_pe': str(px/eps0), 'scenarios': {}}
    for sn, s in a['scenarios'].items():
        p5 = dec_expr(s['profit_expression'])
        calc(name+sn+'2031利润亿元', s['profit_expression'], p5)
        g, pe = D(s['net_share_change']), D(s['pe'])
        n5 = n0*(1+g)**5
        terminal = p5*D('1e8')*pe/n5/fx
        eps_growth = (p5/p0/(1+g)**5)**D('0.2')-1
        divs = [D(s['dividend_start'])*(1+D(s['dividend_growth']))**i for i in range(1,6)]
        dv = sum(divs)
        cagr = ((terminal+dv)/px)**D('0.2')-1
        calc(name+sn+'2031股数', f'{n0}*(1+({g}))**5', n5)
        calc(name+sn+'2031股价', f'{p5}*1e8*{pe}/{n5}/{fx}', terminal)
        calc(name+sn+'累计分红', '+'.join(str(x) for x in divs), dv)
        calc(name+sn+'五年年化', f'(({terminal}+{dv})/{px})**0.2-1', cagr)
        cashcheck = []
        for i in range(1,6):
            # A smooth operating/profit and purchase-price path tests feasibility,
            # not a year-by-year company forecast or instruction to buy at any price.
            pyear = p0*(p5/p0)**(D(i)/5)
            fcf = pyear*D(s['fcf_conversion'])
            nbeg = n0*(1+g)**(i-1)
            nend = n0*(1+g)**i
            buypx = px+(terminal-px)*D(i)/5
            buycash = nbeg*D(s['gross_buyback_rate'])*buypx*fx/D('1e8')
            divcash = nend*divs[i-1]*fx/D('1e8')
            ratio = (buycash+divcash)/fcf
            assert ratio <= 1
            calc(name+sn+str(i)+'股东分配现金覆盖', f'({buycash}+{divcash})/{fcf}', ratio)
            cashcheck.append({'year_index':i, 'profit_yi':str(pyear), 'fcf_yi':str(fcf), 'buyback_cash_yi':str(buycash), 'dividend_cash_yi':str(divcash), 'payout_to_fcf':str(ratio)})
        results[name]['scenarios'][sn] = {'profit_2031_yi':str(p5), 'shares_2031':str(n5), 'five_year_net_share_change':str(n5/n0-1), 'terminal_price':str(terminal), 'dividends_cumulative':str(dv), 'cagr':str(cagr), 'equivalent_eps_cagr':str(eps_growth), 'cash_feasibility':cashcheck}
    ss=results[name]['scenarios']
    call(name+'三情景等效EPS校核（不含息）', ['three-scenario', '--price',str(px),'--eps',str(eps0),'--shares',str(n0/D('1e8')),'--growth',*[ss[x]['equivalent_eps_cagr'] for x in ['bull','base','bear']],'--pe',*[a['scenarios'][x]['pe'] for x in ['bull','base','bear']],'--years','5','--currency',a['currency']])
    sensitivities = {}
    for newpe in ([16,20] if name == '腾讯' else [10,14]):
        b = ss['base']
        expr = f"(({b['terminal_price']}*{newpe}/{a['scenarios']['base']['pe']}+{b['dividends_cumulative']})/{px})**0.2-1"
        value = ((D(b['terminal_price'])*D(newpe)/D(a['scenarios']['base']['pe'])+D(b['dividends_cumulative']))/px)**D('0.2')-1
        calc(name+str(newpe)+'倍退出PE敏感性',expr,value)
        sensitivities[str(newpe)] = str(value)
    results[name]['base_pe_sensitivity_cagr'] = sensitivities

for name, values in [('腾讯收盘', {'StockAnalysis':442.8, 'Investing':442.8}), ('PDD收盘', {'StockAnalysis':82.21, 'ChartExchange历史收盘':82.21}), ('美元中间价',{'商务部转引央行':6.7787,'MoneyDJ独立新闻':6.7787}), ('港元中间价',{'商务部转引央行':0.86458,'MoneyDJ独立新闻':0.86458})]:
    call(name, ['cross-validate','--field',name,'--values',json.dumps(values,ensure_ascii=False),'--unit','quote'])

(OUT/'model-inputs.json').write_text(json.dumps(inputs,ensure_ascii=False,indent=2)+'\n')
(OUT/'decimal-results.json').write_text(json.dumps(results,ensure_ascii=False,indent=2)+'\n')
(OUT/'financial-rigor.json').write_text(json.dumps(records,ensure_ascii=False,indent=2)+'\n')
(OUT/'financial-rigor.txt').write_text('\n\n'.join(r['label']+'\n'+r['output'] for r in records))
for name, r in results.items():
    print(name,'PE',round(D(r['model_pe']),2))
    for sn,s in r['scenarios'].items():
        print(sn,'profit',round(D(s['profit_2031_yi']),2),'shares',round(D(s['shares_2031'])/D('1e8'),4),'price',round(D(s['terminal_price']),2),'div',round(D(s['dividends_cumulative']),2),'CAGR',round(D(s['cagr'])*100,2),'max payout/FCF',round(max(D(y['payout_to_fcf']) for y in s['cash_feasibility'])*100,2))
