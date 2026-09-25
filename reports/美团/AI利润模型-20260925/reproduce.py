"""Reproduce analyst scenarios, not company guidance. RMB 100 million.
Run from any directory. financial_rigor.py Decimal engine checks every formula.
"""
from pathlib import Path
import json, subprocess, sys
from decimal import Decimal as D

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
TOOL = ROOT / 'tools/financial_rigor.py'
log = []
def calc(expr):
    log.append(subprocess.check_output([sys.executable,str(TOOL),'calc','--expr',expr],text=True))

inputs = {
 'unit':'CNY 100 million; all forward inputs are analyst assumptions',
 'core_revenue_2026':'2800', 'tax_rate':'0.20',
 'near':{
   'bear':{'growth':'0.03','margins':['0.06','0.07','0.08'],'new':['-100','-90','-80'],'hq':['160','170','180'],'finance':['15','15','15'],'ai_pre':['-25','-25','-25']},
   'base':{'growth':'0.07','margins':['0.10','0.12','0.14'],'new':['-60','-45','-30'],'hq':['140','145','150'],'finance':['10','10','10'],'ai_pre':['-10','5','25']},
   'bull':{'growth':'0.10','margins':['0.13','0.16','0.18'],'new':['-30','-10','20'],'hq':['130','135','140'],'finance':['10','10','10'],'ai_pre':['10','30','65']}},
 'long':{
   'bear':{'growth':'0.03','margin':'0.09','new':'-30','hq':'190','finance':'20','ai_pre':'-50'},
   'base':{'growth':'0.06','margin':'0.17','new':'80','hq':'170','finance':'20','ai_pre':'100'},
   'bull':{'growth':'0.09','margin':'0.22','new':'250','hq':'200','finance':'10','ai_pre':'250'}},
 'ai_base_bridge':{'2027':[15,7,5,-30,-7],'2028':[28,12,10,-35,-10],'2029':[42,18,18,-40,-13],'2036':[180,80,140,-180,-120]},
 'valuation_assumptions':{'shares_100m':'61.754848','fx_CNY_per_HKD':'0.86','price_HKD':'72.25','pe_2029':'16','excess_cash_2029':'500','investment_value_2029':'250','discount':'0.10'}
}
def after_tax(p): return p*(D('0.8') if p>0 else D(1))
out={'near':{},'long':{}}
for name,s in inputs['near'].items():
    rows=[]
    for i,year in enumerate([2027,2028,2029]):
        r=D('2800')*(1+D(s['growth']))**(i+1)
        pre=r*D(s['margins'][i])+D(s['new'][i])-D(s['hq'][i])-D(s['finance'][i])
        p=after_tax(pre+D(s['ai_pre'][i]))
        rows.append({'year':year,'core_revenue':str(r),'pre_AI_pretax':str(pre),'pre_AI_net':str(after_tax(pre)),'AI_net_increment':str(p-after_tax(pre)),'profit':str(p)})
        calc(f"(2800*(1+{s['growth']})**{i+1}*{s['margins'][i]}+({s['new'][i]})-{s['hq'][i]}-{s['finance'][i]}+({s['ai_pre'][i]}))*{'0.8' if pre+D(s['ai_pre'][i])>0 else '1'}")
    out['near'][name]=rows
for name,s in inputs['long'].items():
    r=D('2800')*(1+D(s['growth']))**10
    pre=r*D(s['margin'])+D(s['new'])-D(s['hq'])-D(s['finance'])
    p=after_tax(pre+D(s['ai_pre']))
    out['long'][name]={'core_revenue':str(r),'pre_AI_net':str(after_tax(pre)),'AI_net_increment':str(p-after_tax(pre)),'profit':str(p)}
    calc(f"(2800*(1+{s['growth']})**10*{s['margin']}+({s['new']})-{s['hq']}-{s['finance']}+({s['ai_pre']}))*0.8")
calc('(3762.965862163541377372*0.06-100-250-30-100)')
calc('3430.1204*0.01*0.8')
calc('500/61.754848/0.86/(1.1**3)')
v=inputs['valuation_assumptions']; p=D(out['near']['base'][-1]['profit'])
target=(p*D(v['pe_2029'])+D(v['excess_cash_2029'])+D(v['investment_value_2029']))/D(v['shares_100m'])/D(v['fx_CNY_per_HKD'])
out['valuation']={'2029_target_HKD':str(target),'PV_HKD':str(target/(1+D(v['discount']))**3),'return_CAGR':str((target/D(v['price_HKD']))**(D(1)/3)-1)}
calc(f"({p}*16+500+250)/61.754848/0.86/(1.10**3)")
out['sensitivity_2036']={str(m):str(after_tax(D(out['long']['base']['core_revenue'])*m+80-170-20+100)) for m in [D('.13'),D('.17'),D('.21')]}
for field,vals in {'2025收入':{'HKEX':3648.54746,'StockAnalysis':3648.55},'2025归母':{'HKEX':-233.55015,'StockAnalysis':-233.55},'2026H1收入':{'HKEX':1956.8195,'HSTong_AI_summary_not_independent_audit':1956.82},'2026Q2营收':{'HKEX':1046.43044,'WSJ':1046.4}}.items():
    log.append(subprocess.check_output([sys.executable,str(TOOL),'cross-validate','--field',field,'--values',json.dumps(vals),'--unit','亿元'],text=True))
log.append(subprocess.check_output([sys.executable,str(TOOL),'verify-market-cap','--price','72.25','--shares','6175484800','--reported','445920000000','--currency','HKD'],text=True))
for name,data in [('inputs.json',inputs),('calculations.json',out)]:
    (HERE/name).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
(HERE/'financial_rigor.txt').write_text('\n'.join(log))
print(json.dumps(out,ensure_ascii=False,indent=2))
