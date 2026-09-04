#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""拉取光伏/锂板块核心标的财务数据(2023-2026Q1)供深研交叉验证"""
import json, time, urllib.request, urllib.parse, csv, sys

UA = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

def fetch_em(report, cols, code, pagesize=30):
    secucode = code + ('.SH' if code.startswith('6') else '.SZ')
    qs = urllib.parse.urlencode({
        'reportName': report, 'columns': cols,
        'filter': f'(SECUCODE="{secucode}")',
        'pageNumber': '1', 'pageSize': str(pagesize),
        'sortTypes': '-1', 'sortColumns': 'REPORT_DATE'})
    req = urllib.request.Request(f'https://datacenter.eastmoney.com/securities/api/data/v1/get?{qs}', headers=UA)
    with urllib.request.urlopen(req, timeout=20) as r:
        d = json.loads(r.read().decode('utf-8', errors='replace'))
    return (d.get('result') or {}).get('data') or []

def all_periods(rows, field):
    """按报告期提取所有数据 {YYYY-MM-DD: value}"""
    out = {}
    for r in rows:
        rd = str(r.get('REPORT_DATE', ''))[:10]
        v = r.get(field)
        if v is not None:
            out[rd] = v
    return out

stocks = {
    '600438': '通威股份', '601012': '隆基绿能', '002459': '晶澳科技', '002129': 'TCL中环', '600089': '特变电工',
    '002460': '赣锋锂业', '002466': '天齐锂业', '000792': '盐湖股份', '002756': '永兴材料', '002738': '中矿资源',
}
print(f"{'代码':<7}{'名称':<8}{'23营收':>11}{'24营收':>11}{'25营收':>11}{'26Q1营收':>11} {'23净利':>10}{'24净利':>10}{'25净利':>10}{'26Q1净利':>10}")
res = {}
for code, name in stocks.items():
    try:
        inc = fetch_em('RPT_DMSK_FN_INCOME', 'SECUCODE,REPORT_DATE,TOTAL_OPERATE_INCOME,PARENT_NETPROFIT', code)
        bal = fetch_em('RPT_DMSK_FN_BALANCE', 'SECUCODE,REPORT_DATE,TOTAL_LIABILITIES,TOTAL_ASSETS', code)
        rev = all_periods(inc, 'TOTAL_OPERATE_INCOME')
        np_ = all_periods(inc, 'PARENT_NETPROFIT')
        bal_all = all_periods(bal, 'TOTAL_ASSETS')
        liab_all = all_periods(bal, 'TOTAL_LIABILITIES')
        def g(d, k):
            return d.get(k)
        r23, r24, r25, rq1 = g(rev,'2023-12-31'), g(rev,'2024-12-31'), g(rev,'2025-12-31'), g(rev,'2026-03-31')
        n23, n24, n25, nq1 = g(np_,'2023-12-31'), g(np_,'2024-12-31'), g(np_,'2025-12-31'), g(np_,'2026-03-31')
        # 负债率(2026Q1)
        a26, l26 = g(bal_all,'2026-03-31'), g(liab_all,'2026-03-31')
        ratio = f'{l26/a26*100:.1f}%' if (a26 and l26) else '-'
        f = lambda v: f'{v/1e8:>11.1f}' if v is not None else f'{"-":>11}'
        f2 = lambda v: f'{v/1e8:>10.1f}' if v is not None else f'{"-":>10}'
        print(f"{code:<7}{name:<8}{f(r23)}{f(r24)}{f(r25)}{f(rq1)} {f2(n23)}{f2(n24)}{f2(n25)}{f2(nq1)} 负债率{ratio}")
        res[code] = {'name': name, 'rev23': r23, 'rev24': r24, 'rev25': r25, 'rev_q1': rq1,
                     'np23': n23, 'np24': n24, 'np25': n25, 'np_q1': nq1, 'debt_ratio': ratio}
    except Exception as e:
        print(f'{code} {name} 失败: {e}', file=sys.stderr)
    time.sleep(0.4)

with open('data/solar_lithium_fin.csv', 'w', newline='', encoding='utf-8-sig') as f:
    w = csv.DictWriter(f, fieldnames=['code','name','rev23','rev24','rev25','rev_q1','np23','np24','np25','np_q1','debt_ratio'])
    w.writeheader()
    for code, r in res.items():
        w.writerow({'code': code, **r})
print('\n已保存 data/solar_lithium_fin.csv')
