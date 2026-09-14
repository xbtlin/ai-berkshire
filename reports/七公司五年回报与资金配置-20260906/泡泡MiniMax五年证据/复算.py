#!/usr/bin/env python3
"""Five-year scenarios; facts and assumptions remain separate. No probabilities."""
import ast
import json
import subprocess
from decimal import Decimal, getcontext
from pathlib import Path

getcontext().prec = 40
OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[2]
TOOL = ROOT / 'tools/financial_rigor.py'

def dec_eval(expression):
    def visit(node):
        if isinstance(node, ast.Expression): return visit(node.body)
        if isinstance(node, ast.Num): return Decimal(str(node.n))
        if isinstance(node, ast.Constant): return Decimal(str(node.value))
        if isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.USub): return -visit(node.operand)
        if isinstance(node, ast.BinOp):
            a, b = visit(node.left), visit(node.right)
            if isinstance(node.op, ast.Add): return a+b
            if isinstance(node.op, ast.Sub): return a-b
            if isinstance(node.op, ast.Mult): return a*b
            if isinstance(node.op, ast.Div): return a/b
            if isinstance(node.op, ast.Pow): return a**b
        raise ValueError(expression)
    return visit(ast.parse(expression, mode='eval'))

results, logs = {}, []
def calc(name, expression):
    p = subprocess.run(['python3', str(TOOL), 'calc', '--expr='+expression], text=True, capture_output=True, check=True)
    precise = dec_eval(expression)
    tool_value = Decimal(next(x.split('精确值:',1)[1].strip() for x in p.stdout.splitlines() if '精确值:' in x))
    assert abs(precise-tool_value) <= max(Decimal('0.000000001'), abs(precise)*Decimal('0.000000000001'))
    results[name] = {'expression': expression, 'decimal_result': str(precise), 'tool_result': str(tool_value), 'checked': True}
    logs.append(name+'\n'+p.stdout)
    return str(precise)

fx = '(6.7787/0.86458)'
calc('pop_market_cap_HKD100m', '154*1331779203/100000000')
calc('mini_market_cap_HKD100m', '361.4*349235308/100000000')
calc('mini_conversion_potential_shares', '6500000000/335')
calc('mini_conversion_percent', '19402985/349235308*100')
calc('mini_liquid_net_cash_June_USDb', '(930.905+14.038+278.347-133.555-2.035-1.833)/1000')
cash_start = calc('mini_proforma_cash_after_debt_USDb', '(930.905+14.038+278.347-133.555-2.035-1.833)/1000+(9443.71+6433.3-6500)/'+fx+'/1000')
calc('pop_normalized_PE', '154/(112*100000000/1331779203/0.86458)')
calc('mini_TTM_equity_PS', '361.4*349235308/'+fx+'/(79.038-30.429+116.573)/1000000')

pop = {
 'bear': {'revenue':'250','gm':'0.55','opex':'0.35','pe':'10','annual_profit_prefix':['80','65','50','40']},
 'base': {'revenue':'550','gm':'0.67','opex':'0.31','pe':'16','annual_profit_prefix':['105','115','125','135']},
 'bull': {'revenue':'950','gm':'0.70','opex':'0.29','pe':'22','annual_profit_prefix':['140','175','210','250']},
}
mini = {
 'bear': {'revenue_USDb':'1','gm':'0.25','rd_USDb':'0.5','sga_USDb':'0.15','shares':'750000000','multiple':'1','method':'equity_PS','cash_issue_price':'65','net_burn_USDb':'4.5'},
 'base': {'revenue_USDb':'5','gm':'0.45','rd_USDb':'1.8','sga_USDb':'0.5','shares':'500000000','multiple':'3','method':'equity_PS','cash_issue_price':'150','net_burn_USDb':'4'},
 'bull': {'revenue_USDb':'12','gm':'0.55','rd_USDb':'3','sga_USDb':'1.2','shares':'450000000','multiple':'25','method':'PE','cash_issue_price':'400','net_burn_USDb':'3.5'},
}
summary = {'pop':{},'mini':{}}
for scenario, row in pop.items():
    profit = calc('pop_'+scenario+'_profit_CNY100m', f"{row['revenue']}*({row['gm']}-{row['opex']})*0.75*0.98")
    dividends = calc('pop_'+scenario+'_cash_dividend_HKD', '('+'+'.join(row['annual_profit_prefix']+[profit])+')*100000000*0.25/1331779203/0.86458')
    price = calc('pop_'+scenario+'_exit_HKD', f"{profit}*100000000*{row['pe']}/1331779203/0.86458")
    cagr = calc('pop_'+scenario+'_CAGR_percent', f'(({price}+{dividends})/154)**(1/5)*100-100')
    summary['pop'][scenario] = dict(row, profit_CNY100m=profit, dividends_HKD=dividends, exit_HKD=price, CAGR_percent=cagr, shares='1331779203')
for scenario,row in mini.items():
    pretax = calc('mini_'+scenario+'_pretax_USDb', f"{row['revenue_USDb']}*{row['gm']}-{row['rd_USDb']}-{row['sga_USDb']}")
    profit = calc('mini_'+scenario+'_profit_USDb', f"{pretax}*{('0.75' if Decimal(pretax)>0 else '1')}")
    profit_cny = calc('mini_'+scenario+'_profit_CNY100m', f'{profit}*10*6.7787')
    equity_value = calc('mini_'+scenario+'_equity_USDb', f"{(profit if row['method']=='PE' else row['revenue_USDb'])}*{row['multiple']}")
    price = calc('mini_'+scenario+'_exit_HKD', f"{equity_value}*1000000000*{fx}/{row['shares']}")
    cagr = calc('mini_'+scenario+'_CAGR_percent', f'({price}/361.4)**(1/5)*100-100')
    dilution = calc('mini_'+scenario+'_share_increase_percent', f"({row['shares']}/349235308-1)*100")
    proceeds = calc('mini_'+scenario+'_future_cash_equity_proceeds_USDb', f"({row['shares']}-349235308-20000000)*{row['cash_issue_price']}*0.99/{fx}/1000000000")
    cash_end = calc('mini_'+scenario+'_residual_cash_USDb', f"{cash_start}+{proceeds}-{row['net_burn_USDb']}")
    summary['mini'][scenario] = dict(row, profit_USDb=profit, profit_CNY100m=profit_cny, equity_value_USDb=equity_value, exit_HKD=price, CAGR_percent=cagr, share_increase_percent=dilution, future_equity_proceeds_USDb=proceeds, residual_cash_USDb=cash_end, dividends_HKD='0')

for pe in ['12','16','20']:
    calc('pop_base_PE'+pe+'_CAGR_percent', f"(({summary['pop']['base']['profit_CNY100m']}*100000000*{pe}/1331779203/0.86458+{summary['pop']['base']['dividends_HKD']})/154)**(1/5)*100-100")
for ps in ['2','3','4']:
    calc('mini_base_PS'+ps+'_CAGR_percent', f'(5*1000000000*{ps}*{fx}/500000000/361.4)**(1/5)*100-100')
calc('mini_base_PS3_2036_profit_25PE_discount15_equity_USDb', '1.125*25/(1.15**5)')
calc('mini_15percent_required_2031_revenue_USDb_PS3', '361.4*(1.15**5)*500000000/'+fx+'/3/1000000000')
calc('pop_15percent_entry_HKD_base', f"({summary['pop']['base']['exit_HKD']}+{summary['pop']['base']['dividends_HKD']})/(1.15**5)")
calc('mini_15percent_entry_HKD_base', f"{summary['mini']['base']['exit_HKD']}/(1.15**5)")

checks = [
 ['verify-market-cap','--price','154','--shares','1331779203','--reported','205094000000','--currency','HKD'],
 ['verify-market-cap','--price','361.4','--shares','349235308','--reported','126213640000','--currency','HKD'],
 ['verify-valuation','--price','154','--eps',str(Decimal('112e8')/Decimal('1331779203')/Decimal('0.86458'))],
 ['verify-valuation','--price','361.4','--revenue-per-share',str((Decimal('79.038')-Decimal('30.429')+Decimal('116.573'))*Decimal('1e6')*(Decimal('6.7787')/Decimal('0.86458'))/Decimal('349235308'))],
 ['cross-validate','--field','pop_regular_close_20260904','--values',json.dumps({'StockAnalysis':154,'Investing':154}),'--unit','HKD'],
 ['cross-validate','--field','mini_regular_close_20260904','--values',json.dumps({'StockAnalysis':361.4,'FT':361.4}),'--unit','HKD'],
 ['cross-validate','--field','pop_issued_shares','--values',json.dumps({'HKEX':1331779203,'Tiger':1331779203}),'--unit','shares'],
 ['cross-validate','--field','mini_issued_shares','--values',json.dumps({'HKEX':349235308,'StockAnalysis':349240000}),'--unit','shares'],
]
for args in checks:
    p=subprocess.run(['python3',str(TOOL),*args],text=True,capture_output=True,check=True)
    logs.append(' '.join(args)+'\n'+p.stdout)
(OUT/'inputs.json').write_text(json.dumps({'pop':pop,'mini':mini,'fx_HKD_CNY':'0.86458','fx_USD_CNY':'6.7787','period_years':5,'price_date':'2026-09-04','dividend_reinvestment':False,'probabilities':None},ensure_ascii=False,indent=2)+'\n')
(OUT/'calculations.json').write_text(json.dumps(results,ensure_ascii=False,indent=2)+'\n')
(OUT/'model-summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n')
(OUT/'financial-rigor.txt').write_text('\n\n'.join(logs))
print(json.dumps(summary,ensure_ascii=False,indent=2))
