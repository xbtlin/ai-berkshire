"""Unify seven independent company models; verify formulas with Decimal and financial_rigor.

All prospective inputs are assumptions. This checks arithmetic, not predictive validity.
Run from any directory; only writes beside this script. No network or trading actions.
"""
from pathlib import Path
from decimal import Decimal as D, getcontext
import ast
import json
import re
import subprocess

getcontext().prec = 48
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
FX = D('0.86458')
USD = D('6.7787')
YI = D('100000000')
SC = ('bear', 'base', 'bull')
CN = ('保守', '基准', '乐观')
logs = []


def read(p):
    return json.loads((HERE / p).read_text())


def exact(expression):
    def walk(n):
        if isinstance(n, (ast.Num, ast.Constant)):
            literal = re.match(r'(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?', expression[n.col_offset:])
            if literal is None: raise ValueError(ast.dump(n))
            return D(literal.group(0))
        if isinstance(n, ast.UnaryOp) and isinstance(n.op, ast.USub):
            return -walk(n.operand)
        if isinstance(n, ast.BinOp):
            a, b = walk(n.left), walk(n.right)
            if isinstance(n.op, ast.Add): return a+b
            if isinstance(n.op, ast.Sub): return a-b
            if isinstance(n.op, ast.Mult): return a*b
            if isinstance(n.op, ast.Div): return a/b
            if isinstance(n.op, ast.Pow): return a**b
        raise ValueError(ast.dump(n))
    return walk(ast.parse(expression, mode='eval').body)


def checked(expression, expected=None):
    result = exact(expression)
    proc = subprocess.run(['python3', str(ROOT/'tools/financial_rigor.py'),
                           'calc', '--expr='+expression], capture_output=True, text=True, check=True)
    raw = re.search(r'精确值:\s*([^\n]+)', proc.stdout)
    if not raw:
        raise RuntimeError(proc.stdout)
    shared = D(raw.group(1))
    assert abs(result-shared) < max(D('1e-8'), abs(result)*D('1e-11')), (expression, result, shared)
    if expected is not None:
        assert abs(result-D(str(expected))) < max(D('1e-10'), abs(result)*D('1e-12'))
    logs.append({'expression': expression, 'decimal': str(result), 'shared_tool': proc.stdout})
    return result


models = {}


def add(name, price, currency, key, profit, shares, multiple, div, method='PE', revenue=None, old_cagr=None):
    p, n, m, dividend = map(D, map(str, (profit, shares, multiple, div)))
    quote_fx = USD if currency == 'USD' else FX
    valuation_basis = p if method == 'PE' else D(str(revenue))
    target = checked(f'{valuation_basis}*100000000*{m}/({n}*{quote_fx})')
    wealth = checked(f'({target}+{dividend})/{price}')
    cagr = checked(f'{wealth}**0.2-1', old_cagr)
    entry12 = checked(f'({target}+{dividend})/1.12**5')
    entry15 = checked(f'({target}+{dividend})/1.15**5')
    item = models.setdefault(name, {'price': str(price), 'currency': currency, 'scenarios': {}})
    item['scenarios'][key] = dict(profit_cny_yi=str(p), shares=str(n), multiple=str(m), method=method,
        revenue_cny_yi=None if revenue is None else str(revenue), dividends=str(dividend),
        terminal_price=str(target), wealth_factor=str(wealth), cagr=str(cagr),
        entry_price_for_12pct=str(entry12), entry_price_for_15pct=str(entry15))


tp = read('腾讯拼多多证据/model-inputs.json')
tpr = read('腾讯拼多多证据/decimal-results.json')
for name, company in tp.items():
    for key, s in company['scenarios'].items():
        profit = checked(s['profit_expression'], tpr[name]['scenarios'][key]['profit_2031_yi'])
        shares = checked(f"{company['model_diluted_quote_units']}*(1+({s['net_share_change']}))**5")
        # Agent schedule starts with one year of growth applied to the declared starting dividend.
        dividend = sum(D(s['dividend_start'])*(1+D(s['dividend_growth']))**year for year in range(1,6))
        assert abs(dividend-D(tpr[name]['scenarios'][key]['dividends_cumulative'])) < D('1e-20')
        add(name, company['price'], company['currency'], key, profit, shares, s['pe'], dividend,
            old_cagr=tpr[name]['scenarios'][key]['cagr'])

km = read('快手美团证据/model-inputs.json')['companies']
kmr = read('快手美团证据/decimal-results.json')
for name, company in km.items():
    for key, cn in zip(SC, CN):
        s = company['scenarios'][cn]
        profit = checked(s['profit_expr'])
        shares = checked(f"{company['issued_shares_100m']}*100000000*(1+({s['net_share_growth']}))**5")
        dividend = checked(f"{s['annual_dps_hkd']}*5")
        add(name, company['price_hkd'], 'HKD', key, profit, shares, s['pe'], dividend,
            old_cagr=kmr[name]['scenarios'][cn]['terminal_wealth_cagr'])

pm = read('泡泡MiniMax五年证据/model-summary.json')
for key in SC:
    s = pm['pop'][key]
    profit = checked(f"{s['revenue']}*({s['gm']}-{s['opex']})*.75*.98", s['profit_CNY100m'])
    dividends = checked(f"({' + '.join(s['annual_profit_prefix'])}+{profit})*.25*100000000/({s['shares']}*.86458)")
    add('泡泡玛特', '154', 'HKD', key, profit, s['shares'], s['pe'], dividends,
        old_cagr=D(s['CAGR_percent'])/100)
    s = pm['mini'][key]
    pretax = checked(f"({s['revenue_USDb']}*{s['gm']}-{s['rd_USDb']}-{s['sga_USDb']})*10")
    profit_usd_yi = pretax * (D('.75') if pretax > 0 else D(1))
    profit = checked(f'{profit_usd_yi}*6.7787', s['profit_CNY100m'])
    revenue = checked(f"{s['revenue_USDb']}*10*6.7787")
    add('MiniMax', '361.4', 'HKD', key, profit, s['shares'], s['multiple'], 0,
        method=s['method'], revenue=revenue, old_cagr=D(s['CAGR_percent'])/100)

ali = [
    ('(8500*.10+3000*.05+200*(-.8)-100-180)*.75+50', '22000000000', 10, [D('.6')]*5),
    ('(11000*.18+5000*.15+300*(-.3)+0-200)*.75+100', '21000000000', 16, [D(1)]*5),
    ('(12500*.22+7500*.22+500*.10+100-250)*.75+150', '20500000000', 20, list(map(D,['1','1.25','1.5','1.75','2.5']))),
]
for key, (expr, shares, pe, divs) in zip(SC, ali):
    add('阿里巴巴', '110.1', 'HKD', key, checked(expr), shares, pe, sum(divs))
checked('-200+0+500+800+1000', 2100)
checked('210*5*.86458', '907.809')
checked('200+210*2*.86458', '563.1236')
# Fiscal 2026 reported earnings/current shares: historical static PE, not a forecast or TTM.
ali_eps = checked('1059.04*100000000/(19884988918*.86458)')
proc = subprocess.run(['python3', str(ROOT/'tools/financial_rigor.py'), 'verify-valuation',
                       '--price', '110.1', '--eps', str(ali_eps)],capture_output=True,text=True,check=True)
(HERE/'阿里历史估值核验.txt').write_text('口径：FY2026归母1059.04亿元/2026年8月最新股本，并非TTM。\n'+proc.stdout)

order = ['腾讯','拼多多','快手','阿里巴巴','泡泡玛特','美团','MiniMax']
models = {name: models[name] for name in order}
weights = dict(zip(order, map(D, ['.35','.20','.10','0','0','0','0'])))
weights['现金'] = D('.35')
cash_rate = D('.015')
raw = dict(zip(['拼多多','腾讯','快手','美团','泡泡玛特','MiniMax'], map(D,['29','26','22','9','8','7'])))
current = {name: checked(f'{w}/101') for name,w in raw.items()}
assert sum(raw.values()) == 101
shocks = dict(zip(order, map(D,['-.35','-.50','-.60','-.50','-.60','-.60','-.80'])))


def portfolio(w):
    assert abs(sum(w.values())-1) < D('1e-40')
    out = {'weights': {k:str(v) for k,v in w.items()}, 'scenarios': {}}
    for key in SC:
        parts = [f"{v}*{models[k]['scenarios'][key]['wealth_factor']}" for k,v in w.items() if k != '现金']
        if '现金' in w: parts.append(f"{w['现金']}*1.015**5")
        wealth = checked('+'.join(parts))
        out['scenarios'][key] = {'wealth_factor': str(wealth), 'cagr': str(checked(f'{wealth}**.2-1'))}
    out['stress_loss'] = str(checked('+'.join(f'{v}*({shocks[k]})' for k,v in w.items() if k!='现金')))
    return out

old_same_cash = {name: value*D('.65') for name,value in current.items()}
old_same_cash['现金'] = D('.35')
new_stock_component = {name: value/D('.65') for name,value in weights.items() if name!='现金'}
checked('.35+.20+.10+.35', 1)
portfolios = {'reference_pool':portfolio(weights), 'old_stocks_only_not_account':portfolio(current),
              'old_mix_with_same_cash_hypothetical':portfolio(old_same_cash),
              'new_stock_component_only':portfolio(new_stock_component)}
base_parts = '+'.join(f"{v}*{models[k]['scenarios']['base']['wealth_factor']}" for k,v in weights.items() if k!='现金')
cash_sensitivity = {str(r):str(checked(f'({base_parts}+.35*(1+{r})**5)**.2-1')) for r in [D(0),D('.015'),D('.02')]}
stress_budget = {str(budget):str(checked(f'{budget}/(-({portfolios["reference_pool"]["stress_loss"]})/.65)'))
                for budget in [D('.20'),D('.30')]}
pe_sensitivity = {}
for name, multiples in {'腾讯':[16,18,20], '拼多多':[10,12,14], '快手':[10,12,14],
                       '阿里巴巴':[12,16,20], '泡泡玛特':[12,16,20], '美团':[14,18,22]}.items():
    s = models[name]['scenarios']['base']
    pe_sensitivity[name] = {str(m):str(checked(f"(({s['terminal_price']}*{m}/{s['multiple']}+{s['dividends']})/{models[name]['price']})**.2-1")) for m in multiples}
output = {'cutoff':'2026-09-06','price_date':'2026-09-04','horizon_years':5,
    'method':'Terminal wealth CAGR; dividends held as zero-interest cash. No rebalancing, FX changes or taxes.',
    'fx_cny_per_hkd':str(FX),'fx_cny_per_usd':str(USD),'companies':models,
    'cash_rate_assumption':str(cash_rate), 'portfolios':portfolios,
    'cash_rate_sensitivity':cash_sensitivity, 'equity_fraction_under_illustrative_stress_budget':stress_budget,
    'exit_pe_sensitivity':pe_sensitivity,
    'boundary':'All scenario assumptions are hypothetical. Adverse scenarios are not worst-case loss bounds.'}
(HERE/'统一模型.json').write_text(json.dumps(output,ensure_ascii=False,indent=2)+'\n')
(HERE/'统一计算核验.json').write_text(json.dumps(logs,ensure_ascii=False,indent=2)+'\n')
rows=[]
for name in order:
    c = models[name]
    rows.append('| '+name+' | '+c['price']+' '+c['currency']+' | '+' | '.join(f"{D(c['scenarios'][s]['cagr'])*100:.1f}%" for s in SC)+' |')
(HERE/'汇总表.txt').write_text('\n'.join(rows)+'\n')
print('\n'.join(rows))
print(json.dumps({'portfolios':portfolios,'cash_sensitivity':cash_sensitivity,'stress_equity_budget':stress_budget},ensure_ascii=False,indent=2))
print('Validated expressions:',len(logs))
