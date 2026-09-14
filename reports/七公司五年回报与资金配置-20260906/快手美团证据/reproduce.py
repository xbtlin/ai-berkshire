#!/usr/bin/env python3
"""Reproduce the two-company 2031 scenarios. All numbers are model assumptions unless labelled facts."""
from decimal import Decimal as D, getcontext
from pathlib import Path
import json
import subprocess

getcontext().prec = 48
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
RIGOR = ROOT / 'tools' / 'financial_rigor.py'
FX = D('0.86458')
YEARS = 5
data = {
    '快手': {
        'price_hkd': '33.66', 'issued_shares_100m': '43.26961215',
        'scenarios': {
            '保守': {'profit_expr': '1200*.07+40*(-.20)*.65-20', 'pe': '8', 'net_share_growth': '.015', 'annual_dps_hkd': '.3', 'ocf_less_capex_lease_nci_100m': ['20','20','30','40','50'], 'gross_issuance_rate': '.015', 'gross_buyback_rate': '0', 'buyback_price_hkd': ['30','25','20','15','15']},
            '基准': {'profit_expr': '1530*.12+120*.10*.60-15', 'pe': '12', 'net_share_growth': '0', 'annual_dps_hkd': '.8', 'ocf_less_capex_lease_nci_100m': ['50','70','90','110','130'], 'gross_issuance_rate': '.01', 'gross_buyback_rate': '.01', 'buyback_price_hkd': ['35','40','45','50','55']},
            '乐观': {'profit_expr': '1900*.14+250*.20*.55-5', 'pe': '16', 'net_share_growth': '-.01', 'annual_dps_hkd': '1.2', 'ocf_less_capex_lease_nci_100m': ['100','150','200','250','300'], 'gross_issuance_rate': '.01', 'gross_buyback_rate': '.02', 'buyback_price_hkd': ['40','60','80','100','120']},
        },
    },
    '美团': {
        'price_hkd': '81.75', 'issued_shares_100m': '61.754848',
        'scenarios': {
            '保守': {'profit_expr': '(3200*.08-60-120-20)*.8', 'pe': '12', 'net_share_growth': '.015', 'annual_dps_hkd': '0', 'ocf_less_capex_lease_nci_100m': ['-100','-50','0','20','40'], 'gross_issuance_rate': '.015', 'gross_buyback_rate': '0', 'buyback_price_hkd': ['70','50','30','20','15']},
            '基准': {'profit_expr': '(3600*.13-20-130-20)*.8', 'pe': '18', 'net_share_growth': '.005', 'annual_dps_hkd': '0', 'ocf_less_capex_lease_nci_100m': ['40','80','120','160','200'], 'gross_issuance_rate': '.005', 'gross_buyback_rate': '0', 'buyback_price_hkd': ['80','80','80','80','80']},
            '乐观': {'profit_expr': '(4400*.17+40-140-20)*.8', 'pe': '22', 'net_share_growth': '0', 'annual_dps_hkd': '0', 'ocf_less_capex_lease_nci_100m': ['80','150','250','350','450'], 'gross_issuance_rate': '.005', 'gross_buyback_rate': '.005', 'buyback_price_hkd': ['90','110','130','150','160']},
        },
    },
}

def dec_eval(expr):
    import ast
    def visit(n):
        if isinstance(n, ast.Expression): return visit(n.body)
        if isinstance(n, ast.Num): return D(str(n.n))
        if isinstance(n, ast.Constant): return D(str(n.value))
        if isinstance(n, ast.UnaryOp) and isinstance(n.op, ast.USub): return -visit(n.operand)
        if isinstance(n, ast.BinOp):
            a,b=visit(n.left),visit(n.right)
            if isinstance(n.op,ast.Add): return a+b
            if isinstance(n.op,ast.Sub): return a-b
            if isinstance(n.op,ast.Mult): return a*b
            if isinstance(n.op,ast.Div): return a/b
        raise ValueError(n)
    return visit(ast.parse(expr, mode='eval'))

def root5(x):
    return (x.ln()/D(5)).exp()

def irr(price, terminal_price, dps):
    low, high = D('-.999999'), D('10')
    for _ in range(200):
        r=(low+high)/2
        pv=sum(dps/(1+r)**t for t in range(1,6))+terminal_price/(1+r)**5
        if pv>price: low=r
        else: high=r
    return (low+high)/2

logs=[]
def run_rigor(args):
    p=subprocess.run(['python3',str(RIGOR),*args],capture_output=True,text=True,check=True)
    logs.append('$ python3 tools/financial_rigor.py '+ ' '.join(args)+'\n'+p.stdout)

results={}
for name, c in data.items():
    p,n = D(c['price_hkd']),D(c['issued_shares_100m'])
    mc=p*n*FX
    run_rigor(['calc','--expr',f'{p}*{n}*{FX}'])
    results[name]={'market_cap_cny_100m':str(mc),'scenarios':{}}
    for scenario,s in c['scenarios'].items():
        profit=dec_eval(s['profit_expr'])
        run_rigor(['calc','--expr',s['profit_expr']])
        pe,ng,dps=D(s['pe']),D(s['net_share_growth']),D(s['annual_dps_hkd'])
        n_end=n*(1+ng)**5
        end_price=profit*pe/n_end/FX
        div=dps*5
        wealth=end_price+div
        cagr=root5(wealth/p)-1
        run_rigor(['calc','--expr',f'{profit}*{pe}/({n}*(1+({ng}))**5)/{FX}'])
        run_rigor(['calc','--expr',f'(({end_price}+{div})/{p})**(1/5)-1'])
        funding=[]
        n_cur=n
        for t in range(5):
            buyback=n_cur*D(s['gross_buyback_rate'])*D(s['buyback_price_hkd'][t])*FX
            n_next=n_cur*(1+D(s['gross_issuance_rate'])-D(s['gross_buyback_rate']))
            dividend=n_next*dps*FX
            fcf=D(s['ocf_less_capex_lease_nci_100m'][t])
            funding.append({'year':2027+t,'cash_after_capex_leases_nci':str(fcf),'gross_buyback_cash':str(buyback),'dividend_cash':str(dividend),'retained_cash':str(fcf-buyback-dividend)})
            n_cur=n_next
        assert n_cur==n_end
        results[name]['scenarios'][scenario]={
            'profit_cny_100m':str(profit),'pe':str(pe),'shares_2031_100m':str(n_end),
            'price_2031_hkd':str(end_price),'cumulative_dps_hkd':str(div),
            'terminal_wealth_hkd':str(wealth),'terminal_wealth_cagr':str(cagr),
            'annual_cashflow_irr':str(irr(p,end_price,dps)),
            'funding_assumptions':funding,
            'fcf_total_cny_100m':str(sum(D(r['cash_after_capex_leases_nci']) for r in funding)),
            'distribution_total_cny_100m':str(sum(D(r['gross_buyback_cash'])+D(r['dividend_cash']) for r in funding)),
        }

run_rigor(['verify-valuation','--price','33.66','--eps',str(D('157.66')/D('43.26961215')/FX),'--dividend','.69'])
# Current Meituan PE is economically uninformative because trailing earnings are negative.
# three-scenario is a mechanical terminal-EPS bridge only; the underlying earnings were built above.
for name,c in data.items():
    p,n=D(c['price_hkd']),D(c['issued_shares_100m'])
    terminal_eps=[D(results[name]['scenarios'][s]['price_2031_hkd'])/D(c['scenarios'][s]['pe']) for s in ['乐观','基准','保守']]
    bridge_growth=[root5(v)-1 for v in terminal_eps] # arbitrary HKD1 starting EPS, NOT current earnings
    run_rigor(['three-scenario','--price',str(p),'--eps','1','--shares',str(n),'--growth',*[str(v) for v in bridge_growth],'--pe',*[c['scenarios'][s]['pe'] for s in ['乐观','基准','保守']],'--years','5','--currency','HKD'])

(HERE/'model-inputs.json').write_text(json.dumps({'fx_cny_per_hkd':str(FX),'horizon_years':5,'companies':data},ensure_ascii=False,indent=2)+'\n')
(HERE/'decimal-results.json').write_text(json.dumps(results,ensure_ascii=False,indent=2)+'\n')
(HERE/'financial-rigor.txt').write_text('\n'.join(logs))
print(json.dumps({name:{s:{k:v for k,v in out.items() if k in ['profit_cny_100m','price_2031_hkd','terminal_wealth_cagr','annual_cashflow_irr','fcf_total_cny_100m','distribution_total_cny_100m']} for s,out in r['scenarios'].items()} for name,r in results.items()},ensure_ascii=False,indent=2))
