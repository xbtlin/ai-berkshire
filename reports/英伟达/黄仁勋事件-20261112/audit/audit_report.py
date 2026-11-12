"""Audit the fixed 15% report sample; facts, assumptions and arithmetic differ."""
from pathlib import Path
from decimal import Decimal as D
import json, sys, subprocess, re
ROOT=Path(__file__).resolve().parents[4]
OUT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'tools'))
from report_audit import extract_data_points, sample_points
REPORT=ROOT/'reports/英伟达/英伟达黄仁勋事件研究报告-20261112.md'
S='https://stockanalysis.com/stocks/nvda/financials/'
CF=S+'cash-flow-statement/'
N='https://nvidianews.nvidia.com/news/nvidia-announces-financial-results-for-'
Q='https://www.sec.gov/Archives/edgar/data/1045810/000104581026000075/nvda-20260726.htm'
F23=N+'fourth-quarter-and-fiscal-2023'
F25=N+'fourth-quarter-and-fiscal-2025'
F26=N+'fourth-quarter-and-fiscal-2026'
facts={
 'FY2022 · GAAP净利润':(9.752,F23,9.752,S,'独立数据来源交叉'),
 'FY2022 · 公司口径FCF':(8.049,F23,8.132-.083,CF+' ; official equipment principal 0.083','调整比较口径；第二值使用官方本金项桥接'),
 'FY2025 · 公司口径FCF':(60.724,F25,60.853-.129,CF+' ; official equipment principal 0.129','调整比较口径；第二值使用官方本金项桥接'),
 'FY2025 · 收入':(130.497,F25,130.497,S,'独立数据来源交叉'),
 'FY2026 · 收入':(215.938,F26,215.938,S,'独立数据来源交叉'),
 '截至2026年7月TTM · 收入':(215.938+177.837-90.805,F26+' + '+Q,302.970,S,'年度加本年半年减上年半年'),
 'FY2027 Q1 · GAAP毛利率':(74.9,N+'first-quarter-fiscal-2027',74.9,Q,'公司两期披露互证，非独立第三方'),
 'FY2027 Q1 · 数据中心收入，约数':(75.2,N+'first-quarter-fiscal-2027',75.246,Q,'公司两期披露互证，约数小数精度'),
 'FY2027 Q2 · GAAP毛利率':(75,N+'second-quarter-fiscal-2027',75,Q,'公司公告与申报互证，非独立第三方'),
 'FY2027 Q2 · 总收入':(96.221,Q,96.221,S+'?p=quarterly','独立数据来源交叉'),
 '有息债务 · 金额':(1+32.366,Q,None,None,'官方短债加长债；供应商含租赁总债不能直接比较'),
}
model=json.loads((OUT/'model-results.json').read_text())
derived={
 '悲观 · 以10%折回今天':(float((D('197.579')*D('.8')/D('24.147'))*D('.95')**3*15/D('1.1')**3),'独立Decimal复算三年折回价格'),
 '第三年主营税后利润，十亿美元 · 悲观':(float(D('197.579')*D('.8')*D('.95')**3),'独立Decimal复算利润'),
 '次年利润终值倍数 · 乐观':(float((1-D('.04')/D('.25'))/(D('.10')-D('.04'))),'独立Decimal永续倍数复算'),
 '173.73 · 第十年利润，十亿美元':(model['reverse'][3]['profit10'],'valuation_model.py反向DCF求根；不属于外部预测'),
}
assumptions={'2036年主营税后利润，十亿美元 · 悲观':140.,'永续增长g · 悲观':2.}
allpoints=extract_data_points(REPORT.read_text())
sample=sample_points(allpoints,ratio=.15,seed=42)
for p in sample:
 label=p['label']
 if label=='date':
  p.update(classification='extractor_noise',fetched_value=None,fetched_source='日期被误提取为财务值，不纳入数值准出')
 elif label in facts:
  a,b,c,d,note=facts[label]
  p.update(classification='reported_fact',fetched_value=a,fetched_source=b,fetched_value2=c,fetched_source2=d,note=note)
 elif label in derived:
  a,b=derived[label]
  p.update(classification='calculation',fetched_value=a,fetched_source=b,note='仅核算数学，非外部预测验证')
 elif label in assumptions:
  p.update(classification='research_assumption',fetched_value=assumptions[label],fetched_source='valuation_model.py SPECS：检查正文与显式输入一致',note='假设一致不代表假设可靠')
 else: raise RuntimeError('Unreviewed sample: '+label)
(OUT/'report-audit-results.json').write_text(json.dumps(sample,ensure_ascii=False,indent=2)+'\n')
cmd=['python3','tools/report_audit.py','verdict','--results',json.dumps(sample,ensure_ascii=False),'--report',str(REPORT.relative_to(ROOT)),'--output-json']
r=subprocess.run(cmd,cwd=ROOT,text=True,capture_output=True)
(OUT/'report-audit-verdict.txt').write_text('\n'.join(line.rstrip() for line in re.sub(r'\x1b\[[0-9;]*m','',r.stdout+r.stderr).splitlines()).rstrip()+'\n')
if r.returncode: raise RuntimeError(r.stdout+r.stderr)
counts={k:sum(x['classification']==k for x in sample) for k in ['reported_fact','calculation','research_assumption','extractor_noise']}
summary=f'''---
date: 2026-11-12
type: 底稿
---

# 抽检判决与范围

最终报告提取{len(allpoints)}项，按15%及固定种子42抽取{len(sample)}项。

- 已披露事实：{counts['reported_fact']}项。
- 算术复核：{counts['calculation']}项。
- 研究假设一致性：{counts['research_assumption']}项。
- 日期提取噪声：{counts['extractor_noise']}项，明确排除，未伪装成财务验证。

对其余17项，工具判决通过；这是来源/口径/算术一致性检查，不是17项独立双源事实全部通过。
部分季度分项只取得公司不同披露互证；FCF的第三方口径需用官方设备本金桥接；债务采用官方明确口径。
现金独立分类仍有10.40%差异，保留在正文，不使用有争议的供应商值估值。
Macrotrends正文受限，未声称完整读取。所有原始来源保存在financial-data.json。

终值审计参数USD、r10%、稳态增量ROIC25%、g2%/3%/4%，通过同币种、分母和离散风险归属检查。
9%至11%敏感性未发生仓位压力测试翻转；8%/12%为区间外参考，8%下乐观分母不足5个百分点。
完整经营现金IRR与只计终值年化分别披露，三年近似倍数与十年EV/NOPAT不可混称股东PE。

未建模重大尾部风险、经营现金转换假设、股数滞后、非经营投资价值遗漏均已在正文说明。
'''
(OUT/'report-audit-summary.md').write_text(summary)
print(json.dumps(counts,ensure_ascii=False))
print(r.stdout[-1400:])
