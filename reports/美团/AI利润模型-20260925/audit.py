"""Audit the fixed random sample. Forecast checks certify arithmetic only."""
from pathlib import Path
import json, subprocess, sys, re
from decimal import Decimal as D
H=Path(__file__).resolve().parent
R=H.parents[2]
report=H.parent/'美团-investment-team-AI利润-20260925.md'
sys.path.insert(0,str(R/'tools'))
import report_audit as a
points=a.sample_points(a.extract_data_points(report.read_text()),ratio=.15,seed=42)
I=json.loads((H/'inputs.json').read_text()); C=json.loads((H/'calculations.json').read_text())
annual='https://www1.hkexnews.hk/listedco/listconews/sehk/2026/0424/2026042400179.pdf'
half='https://www1.hkexnews.hk/listedco/listconews/sehk/2026/0828/2026082800435.pdf'
sa='https://stockanalysis.com/quote/hkg/3690/financials/'
hs='https://www.hstong.com/news/detail/26082920431659905'
wsj='https://www.wsj.com/business/earnings/meituan-returns-to-profit-as-food-delivery-competition-eases-1026a0e9'
facts={
 '收入 · 2025全年':(3648.54746,annual,3648.55,sa),
 '收入 · 2026上半年':(1956.8195,half,1956.82,hs+' [AI summary; transcription check only]'),
 '归母净利润 · 2023全年':(138.55828,annual,138.56,sa),
 '核心本地商业经营利润 · 2025全年':(-69.04083,annual,None,''),
 '核心本地商业经营利润 · 2026上半年':(36.38333,half,36.38,hs+' [AI summary; transcription check only]'),
 '新业务经营利润 · 2025全年':(-100.82340,annual,None,''),
 '未分配项目净额 · 2023全年':(-51.16976,annual,None,''),
 '经营现金流 · 2026上半年':(27.19085,half,None,''),
 '2026Q2收入 · 第二渠道值':(1046.43044,half,1046.40,wsj),
}
models={
 '客服、研发和运营节约 · 2027':I['ai_base_bridge']['2027'][1],
 '履约新增净节约 · 2036':D('700')*D('.20'),
 '履约新增净节约 · 2028':I['ai_base_bridge']['2028'][2],
 '履约新增净节约 · 2029':D('400')*D('.045'),
 '额外AI研发、推理、设备折旧 · 2028':I['ai_base_bridge']['2028'][3],
 '入口分流、渠道费用与额外让利 · 2027':I['ai_base_bridge']['2027'][4],
 '正常化税后AI净增量 · 2027':sum(I['ai_base_bridge']['2027'])*D('.8'),
 '正常化税后AI净增量 · 2028':sum(I['ai_base_bridge']['2028'])*D('.8'),
 '基准 · 2029利润':(D('2800')*D('1.07')**3*D('.14')-30-150-10+25)*D('.8'),
 '基准 · 2028利润':(D('2800')*D('1.07')**2*D('.12')-45-145-10+5)*D('.8'),
 '乐观 · AI在2029年贡献':D('65')*D('.8'),
 '总部经常成本（含SBC） · 基准':-D(I['long']['base']['hq']),
 '新增AI税后影响 · 乐观':D(I['long']['bull']['ai_pre'])*D('.8'),
}
res=[]; excluded=[]
for p in points:
 label=p['label']; q=dict(p)
 if label in facts:
  v,s,v2,s2=facts[label]
  q.update(fetched_value=v,fetched_source=s,fetched_value2=v2,fetched_source2=s2,verification_kind='external_fact',source_gap=('Only original official disclosure; independent second source not obtained' if v2 is None else ''))
 elif label in models:
  q.update(fetched_value=float(models[label]),fetched_source='Explicit analyst inputs / separately expanded Decimal expression',verification_kind='assumption_or_model_arithmetic',note='Not an external fact; pass does not certify forecast accuracy')
 elif label in ['资料截止','财务与估值 · 评分（满分5）']:
  q.update(reason='Parser captured date year or subjective score; not a financial measurement')
  excluded.append(q);continue
 else: raise ValueError('Unreviewed sample: '+label)
 res.append(q)
for name,records in [('audit_sample.json',points),('audit_results.json',res),('audit_exclusions.json',excluded)]:
 (H/name).write_text(json.dumps(records,ensure_ascii=False,indent=2)+'\n')
for kind in ['external_fact','assumption_or_model_arithmetic']:
 items=[x for x in res if x['verification_kind']==kind]
 run=subprocess.run([sys.executable,str(R/'tools/report_audit.py'),'verdict','--results',json.dumps(items,ensure_ascii=False),'--report',report.name+' ['+kind+']'],text=True,capture_output=True,check=True)
 (H/('verdict_'+kind+'.txt')).write_text('\n'.join(x.rstrip() for x in re.sub(r'\x1b\[[0-9;]*m','',run.stdout).splitlines())+'\n')
 print(run.stdout)
(H/'audit_scope.md').write_text('''# 审计范围\n\nseed=42，提取160个数字、随机抽取24个：9项事实核对，13项模型或假设一致性，2项日期/主观评分排除。\n\n事实PASS表示与原始披露一致，并不代表全部事实完成两个独立数据源验证。2025核心及新业务经营利润、2023未分配项目、2026H1经营现金流的抽样项独立第二来源未取得，保留单源限制。华盛通明确AI生成，只作抄录核对，且不采用其季度归母标签。预测PASS仅表示对应假设或Decimal算式一致。\n\n抽样之外，全部主情景、估值、净现金与风险单位换算由financial_rigor或Decimal复算。未对未经披露的AI归因、份额及未来现金流作真实性背书。年报原始档案可在同项目审计-20260906目录找到，本次通过在线HKEX公告及数据商重新核实关键数据。\n\n研究角色意见分歧：财务角色回报的705.95亿元算式将净融资成本误写为+20；主模型统一为−20，使用两套算术路径确认673.95亿元。风险角色评分3.0/5，主线程为反映最新酒旅调查和十年不确定性采用2.5/5；评分调整不改变事实。\n''')
