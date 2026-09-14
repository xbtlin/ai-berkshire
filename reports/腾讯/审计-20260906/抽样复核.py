from pathlib import Path
from decimal import Decimal as D, getcontext
import importlib.util, subprocess, json
getcontext().prec=35
ROOT=Path(__file__).resolve().parents[3]
spec=importlib.util.spec_from_file_location('audit',ROOT/'tools/report_audit.py')
a=importlib.util.module_from_spec(spec);spec.loader.exec_module(a)
TXAR='https://www1.hkexnews.hk/listedco/listconews/sehk/2026/0409/2026040901231.pdf'
TXH='https://www.tencent.com/wp-content/uploads/2026/08/E700_IR.pdf'
TXSA='https://stockanalysis.com/quote/hkg/0700/financials/'
PDDAR='https://cdn.yahoofinance.com/prod/sec-filings/0001737806/000110465926050727/pdd-20251231x20f.htm'
PDD23='https://investor.pddholdings.com/static-files/e9586d93-bb1d-4e98-af8a-4e73b62350f2'
PDDSA='https://stockanalysis.com/stocks/pdd/financials/'
facts={
'腾讯':{
'收入 · 2025':(751766,TXAR,751766,TXSA),
'经营现金流 · 2024':(258521,TXAR,258521,TXSA),
'收入 · 2025Q4':(194371,TXAR,194371,'https://en.tmtpost.com/news/7919264'),
'IFRS归母 · 2025Q4':(58260,TXAR,58260,'https://en.tmtpost.com/news/7919264'),
'收入 · 2024':(660257,TXAR,660257,TXSA),
'收入 · 2023':(609015,TXAR,609015,TXSA),
'收入 · 2022':(554552,TXAR,554552,TXSA),
'经营利润 · 2025':(241562,TXAR,241562,'https://www.stcn.com/article/detail/3683975.html'),
'经营利润 · 2024':(208099,TXAR,208099,'https://tech.cnr.cn/techph/20250321/t20250321_527108308.shtml'),
'经营利润 · 2022':(110827,TXAR,110880,TXSA),
'IFRS归母 · 2023':(115216,TXAR,115216,TXSA),
'收入 · 2026Q2':(204785,TXH,204800,'https://www.marketscreener.com/news/tencent-q2-revenue-climbs-11-on-ai-driven-ad-gains-but-profit-falls-short-ce7859d8d881fe2d'),
'IFRS归母 · 2026Q1':(58093,TXH,58093,'https://companies.caixin.com/2026-05-13/102443711.html'),
'Non-IFRS归母 · 2026Q1':(67905,TXH,67905,'https://companies.caixin.com/2026-05-13/102443711.html')},
'拼多多':{
'收入 · 2022':(130557.589,PDD23,130558,PDDSA),
'营业成本 · 2023':(91723.577,PDDAR,91723.6,'https://finance.sina.com.cn/tech/2025-03-20/doc-ineqiark3734433.shtml'),
'营业成本 · 2024':(153900.374,PDDAR,153900.4,'https://finance.sina.com.cn/tech/2025-03-20/doc-ineqiark3734433.shtml'),
'经营利润 · 2025':(93102.131,PDDAR,93102,PDDSA),
'GAAP归母 · 2023':(60026.544,PDDAR,60027,PDDSA),
'GAAP归母 · 2021':(7768.670,PDD23,7769,PDDSA)}}
for c in facts:
    p=ROOT/'reports'/c/'审计-20260906'
    report=ROOT/'reports'/c/(c+'研究报告-20260906.md')
    extracted=subprocess.run(['python3',str(ROOT/'tools/report_audit.py'),'extract','--report',str(report),'--seed','42'],capture_output=True,text=True,check=True).stdout
    (p/'抽样原始输出.txt').write_text(extracted)
    rows=a.sample_points(a.extract_data_points(report.read_text()),ratio=.15,seed=42)
    model=json.loads((p/'估值模型.json').read_text())
    excluded=[]
    for row in rows:
        label=row['label']
        if label=='研究日期与资料截止':
            row.update(verification_type='非财务抽取误报：只抽出了日期年份2026，已按date命令确认但不计双源金融事实',exclusion_reason='元数据日期，不是财务数字；保留原始抽样，不重抽替换')
            excluded.append(row)
        elif label in facts[c]:
            v,s,v2,s2=facts[c][label]
            row.update(fetched_value=v,fetched_source=s,fetched_value2=v2,fetched_source2=s2,verification_type='已读取官方原件与独立第二源的历史事实',source_note='详见sources.md，表中百万元人民币；来源值保留其披露精度')
        elif c=='腾讯' and label=='悲观 · 含息年化':
            dec=((D('230000000000')/D('9200000000')/D('.86458')*D('.92')**3*D(12)+D(12))/D('442.8'))**(D(1)/D(3))*100-D(100)
            row.update(fetched_value=model['scenarios'][2]['cagr'],fetched_source='工具原始输出.json：悲观含息年化，financial_rigor calc',fetched_value2=float(dec),fetched_source2='本文件独立Decimal 35位精度复算，输入2300亿元/92亿股/0.86458，增长-8%，PE12，分红12，现价442.8',verification_type='模型计算复核；不是外部事实双源')
        elif c=='拼多多' and label=='基准 · 2029目标价（美元）':
            dec=D('85000000000')/D('1480000000')/D('6.7787')*D('1.05')**3*D(12)
            row.update(fetched_value=model['scenarios'][1]['terminal'],fetched_source='工具原始输出.json：基准2029目标价，financial_rigor calc',fetched_value2=float(dec),fetched_source2='独立Decimal：850亿/14.8亿ADS/6.7787×1.05^3×12',verification_type='模型计算复核；不是外部事实双源')
        elif c=='拼多多' and label=='乐观 · 三年总回报':
            dec=(D('85000000000')/D('1480000000')/D('6.7787')*D('1.12')**3*D(16)/D('82.21')-D(1))*100
            row.update(fetched_value=model['scenarios'][0]['total'],fetched_source='工具原始输出.json：乐观含息累计回报，financial_rigor calc',fetched_value2=float(dec),fetched_source2='独立Decimal：850亿/14.8亿ADS/6.7787×1.12^3×16/82.21−1，零分红',verification_type='模型计算复核；不是外部事实双源')
        elif ' · ' in label and label.split(' · ')[0] in ['悲观','基准','乐观']:
            name,field=label.split(' · ',1)
            i={'乐观':0,'基准':1,'悲观':2}[name]
            s=model['scenarios'][i]
            eps=D(str(model['profit']))/D(str(model['model_shares']))/D(str(model['fx']))
            t=eps*(D(1)+D(str(s['growth'])))**3*D(s['pe'])
            wealth=(t+D(s['div']))/D(str(model['price']))
            if field=='三年总回报':v=s['total'];v2=float((wealth-1)*100)
            elif field in ['年化回报','含息年化']:v=s['cagr'];v2=float((wealth**(D(1)/D(3))-1)*100)
            elif field=='常态利润年增长':v=s['growth']*100;v2=[12,8,-8][i] if c=='腾讯' else [12,5,-10][i]
            elif field=='2029退出PE':v=s['pe'];v2=[22,18,12][i] if c=='腾讯' else [16,12,8][i]
            else:raise ValueError('Unmapped model field: '+field)
            row.update(fetched_value=v,fetched_source='估值模型.json / financial_rigor三情景与calc原输出',fetched_value2=v2,fetched_source2='独立Decimal35位复算；若为增长/PE，则与本文件事先明确的情景输入核对，非外部事实',verification_type='模型算术或假设一致性检查；不声称外部双源事实')
        else:
            raise ValueError('Unverified sample: '+label)
    (p/'抽样核验.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2))
    tested=[x for x in rows if x not in excluded]
    assert all(x.get('fetched_value') is not None and x.get('fetched_value2') is not None for x in tested)
    summary=dict(raw_sample_count=len(rows),excluded_metadata_count=len(excluded),historical_facts=sum(x['label'] in facts[c] for x in tested),model_calculation_or_assumption_count=sum(x['label'] not in facts[c] for x in tested),unverified_financial_samples=0,scope_note='仅样本与计算通过；正文披露资料缺口继续存在，不能解读为全报告所有事实完整双源')
    (p/'审计范围.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2))
    result=subprocess.run(['python3',str(ROOT/'tools/report_audit.py'),'verdict','--results',json.dumps(tested,ensure_ascii=False),'--report',str(report),'--output-json'],capture_output=True,text=True,check=True).stdout
    (p/'审计判决.txt').write_text(result)
    start=result.rfind('\n{')
    if start>=0:(p/'审计判决.json').write_text(result[start+1:])
    print(c,result[-1500:])
