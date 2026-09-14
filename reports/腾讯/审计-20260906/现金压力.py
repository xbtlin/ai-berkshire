from pathlib import Path
import subprocess,json
p=Path(__file__).resolve().parent
root=p.parents[2]
cases={'2029基准利润亿元':'2300*1.08**3','2029现金75pct亿元':'2300*1.08**3*.75'}
for ratio in [.6,.75,.9]:
    cases[f'{ratio}现金亿元']=f'2300*{ratio}'
    cases[f'{ratio}现金收益率']=f'230000000000*{ratio}/3485015236130.865*100'
    cases[f'{ratio}反向永续增长']=f'(0.12-230000000000*{ratio}/3485015236130.865)*100'
rows=[]
for k,v in cases.items():
    args=['python3',str(root/'tools/financial_rigor.py'),'calc','--expr',v]
    result=subprocess.run(args,capture_output=True,text=True,check=True).stdout
    rows.append(dict(label=k,expression=v,source='2300亿元为正文正常化利润假设；市值由9/4实际股数×价格×官方中间价复核；转化率、8%增长和12%贴现率均为研究假设',output=result))
(p/'现金压力输出.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2))
print(json.dumps(rows,ensure_ascii=False,indent=2))
