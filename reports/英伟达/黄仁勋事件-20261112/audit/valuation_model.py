"""Reproducible, explicitly assumed NVDA event valuation. Amounts USD bn.
No API/network or company forecasts are embedded in the scenario assumptions.
"""
from decimal import Decimal as D, getcontext
from pathlib import Path
import json
import subprocess
getcontext().prec = 32
ROOT = Path(__file__).resolve().parents[4]
OUT = Path(__file__).resolve().parent
SHARES, PRICE, EBIT, TAX = D('24.147'), D('160'), D('197.579'), D('.20')
P0 = EBIT * (1-TAX)
NET_CASH = D('23.220')
R, ROIC = D('.10'), D('.25')
SPECS = [
    dict(name='悲观',p='.30',growth3='-.05',multiple3='15',profit10='140',g='.02',cash_ratio='.50'),
    dict(name='基准',p='.50',growth3='.15',multiple3='22',profit10='350',g='.03',cash_ratio='.65'),
    dict(name='乐观',p='.20',growth3='.25',multiple3='28',profit10='650',g='.04',cash_ratio='.75'),
]
def val(s,r=R,price=PRICE):
    g3, g, p10, cr = (D(s[k]) for k in ['growth3','g','profit10','cash_ratio'])
    p3 = P0*(1+g3)**3
    grow7 = (p10/p3)**(D(1)/7)-1
    profits = [P0*(1+g3)**t if t<=3 else p3*(1+grow7)**(t-3) for t in range(1,11)]
    flows = [p*cr for p in profits]
    # Tool PE is a forward-earnings multiple; multiply P10 by (1+g) for year-10 TV.
    terminal_pe = (1-g/ROIC)/(r-g)
    tv = p10*(1+g)*terminal_pe
    ev = sum(cf/(1+r)**t for t,cf in enumerate(flows,1))+tv/(1+r)**10
    equity = ev+NET_CASH
    # Consistent core-enterprise return proxy: net cash is available at purchase.
    cost = price*SHARES-NET_CASH
    def npv(x):
        return sum(cf/(1+x)**t for t,cf in enumerate(flows,1))+tv/(1+x)**10-cost
    lo,hi=D('-.8'),D('1')
    for _ in range(180):
        mid=(lo+hi)/2
        if npv(mid)>0: lo=mid
        else: hi=mid
    terminal_only=(p10*(1+g)*terminal_pe/(price*SHARES))**(D(1)/10)-1
    target3=p3/SHARES*D(s['multiple3'])
    return dict(**s, profit0=P0,profit3=p3,growth4_10=grow7,terminal_pe=terminal_pe,
        target3=target3,target3_pv=target3/(1+R)**3,return3=(target3/price)**(D(1)/3)-1,
        cashflows=flows, terminal_value=tv,dcf_price=equity/SHARES, irr_full=(lo+hi)/2,
        terminal_only=terminal_only,terminal_share_pv=(tv/(1+r)**10)/ev)
rows=[val(s) for s in SPECS]
def weighted(field,rs=rows): return sum(D(s['p'])*s[field] for s in rs)
def reverse_dcf(price,cr=D('.65'),g=D('.03')):
    target=price*SHARES-NET_CASH
    lo,hi=D('-.10'),D('.40')
    for _ in range(180):
        h=(lo+hi)/2
        ps=[P0*(1+h)**t for t in range(1,11)]
        tv=ps[-1]*(1+g)*(1-g/ROIC)/(R-g)
        pv=sum(p*cr/(1+R)**t for t,p in enumerate(ps,1))+tv/(1+R)**10
        if pv>target: hi=h
        else: lo=h
    return dict(price=price,required_growth=(lo+hi)/2,profit10=P0*(1+(lo+hi)/2)**10)
result=dict(inputs=dict(price=PRICE,shares=SHARES,ebit=EBIT,tax=TAX,profit0=P0,net_cash=NET_CASH,r=R,roic=ROIC),
  market_cap=PRICE*SHARES,gaap_pe=PRICE/D('7.91'),core_pe=PRICE/(P0/SHARES),
  fcf_yield=D('126.886')/(PRICE*SHARES),economic_cash_yield=D('119.645')/(PRICE*SHARES),
  scenarios=rows,weighted_dcf=weighted('dcf_price'),weighted_3yr_pv=weighted('target3_pv'),
  sensitivity=[dict(r=r,weighted_dcf=weighted('dcf_price',[val(s,r) for s in SPECS]),
                   weighted_full_irr=weighted('irr_full',[val(s,r) for s in SPECS]))
               for r in map(D,['.08','.09','.10','.11','.12'])],
  reverse=[reverse_dcf(D(p)) for p in ['120','140','160','173.73']],
  event_example=dict(revenue='108',gross_margin='.74',opex='9.2',tax='.20',
    nopat_before=(D('108')*D('.74')-D('9.2'))*D('.8'),
    nopat_after_revenue_5pct_lower=(D('108')*D('.95')*D('.74')-D('9.2'))*D('.8'),
    nopat_after_margin_3pp_lower=(D('108')*D('.71')-D('9.2'))*D('.8')))
def serial(o):
    if isinstance(o,D): return float(o)
    raise TypeError(type(o))
(OUT/'model-results.json').write_text(json.dumps(result,ensure_ascii=False,indent=2,default=serial)+'\n')
log=[]
def run(*a):
    p=subprocess.run(['python3',*a],cwd=ROOT,text=True,capture_output=True)
    log.append('$ python3 '+' '.join(a)+'\n'+p.stdout+p.stderr)
    if p.returncode: raise RuntimeError(p.stdout+p.stderr)
run('tools/financial_rigor.py','verify-market-cap','--price','173.73','--shares','24147000000','--reported','4195550000000','--currency','USD')
run('tools/financial_rigor.py','verify-valuation','--price','160','--eps','7.91','--fcf-per-share',str(D('126.886')/SHARES),'--dividend','1')
run('tools/financial_rigor.py','three-scenario','--price','160','--eps',str(P0/SHARES),'--shares','241.47','--growth','.25','.15','-.05','--pe','28','22','15','--years','3','--currency','USD')
for label, values in [('FY2026收入',{'NVIDIA':215938,'StockAnalysis':215938}),('FY2026净利润',{'NVIDIA':120067,'StockAnalysis':120067}),('TTM收入',{'NVIDIA滚动':302970,'StockAnalysis':302970}),('TTM净利润',{'NVIDIA滚动':192880,'StockAnalysis':192880}),('现金与债券',{'SEC':56586,'NVIDIA财报公告':56586}),('股数_百万',{'SEC':24147,'LUKB':24147,'StockAnalysis四舍五入':24150})]:
    run('tools/financial_rigor.py','cross-validate','--field',label,'--values',json.dumps(values,ensure_ascii=False),'--unit','百万美元或百万股')
run('tools/terminal_value.py','audit','--currency','USD','--r','.10','--roic','.25','--g','.02,.03,.04','--rf','.0498','--beta','1','--discrete-risks','突然换帅:情景,有限出口限制:情景,严重全球处罚:未建模,台湾供应中断:未建模,未披露违法事实:未建模')
for s in rows:
    run('tools/terminal_value.py','pe','--roic','.25','--g',s['g'],'--r','.10')
    run('tools/terminal_value.py','irr','--profit',str(D(s['profit10'])*(1+D(s['g']))),'--mcap',str(PRICE*SHARES),'--pe',str(s['terminal_pe']),'--years','10','--payout','0')
config={'英伟达':{'roic':.25,'g':[.02,.03,.04],'p':[.3,.5,.2],'irr10':[float(s['terminal_only']*100) for s in rows],'k':0}}
(OUT/'terminal-config.json').write_text(json.dumps(config,ensure_ascii=False,indent=2)+'\n')
for delta in ['.02','.01']:
    run('tools/terminal_value.py','flip','--config',str(OUT/'terminal-config.json'),'--name','英伟达','--r','.10','--delta',delta,'--currency','USD','--rf','.0498')
(OUT/'calculation-log.txt').write_text('\n'.join(line.rstrip() for line in '\n'.join(log).splitlines()).rstrip()+'\n')
print(json.dumps({k:v for k,v in result.items() if k!='scenarios'},ensure_ascii=False,indent=2,default=serial))
print(json.dumps([{k:v for k,v in row.items() if k!='cashflows'} for row in rows],ensure_ascii=False,indent=2,default=serial))
