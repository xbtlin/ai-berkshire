#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
A股主板初筛流水线（一次性运行）
================================
用法: python scripts/market_screen.py [--top N] [--only-mainboard]
数据源: 新浪行情API + 东方财富财务API（均免费公开）
输出:
  data/market_snapshot.csv   全市场主板快照
  data/candidates_l1.csv     第一层: 价值底线+流动性 (PE 0-35, PB 0-6, 市值80-3000亿, 成交>3亿, 换手1-15%)
  data/candidates_l2.csv     第二层: 60日K线趋势过滤 (非过热/非破位)
  data/candidates_top25.csv  第三层: 综合打分 Top N
  data/candidates_fin.csv    财务验证 (营收/净利/ROE/现金流)

参考: skills/investment/china-stock-data (SKILL.md) 与 ai-berkshire 初筛模式
"""
import csv, json, re, sys, time, urllib.request, urllib.parse, argparse

UA = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
      'Referer': 'https://finance.sina.com.cn'}
UA_EM = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

# ---------- 阶段0: 全市场拉取 ----------
def fetch_sina_page(page, num=100):
    url = ('https://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/'
           f'Market_Center.getHQNodeData?page={page}&num={num}&sort=amount&asc=0'
           '&node=hs_a&symbol=&_s_r_a=init')
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=15) as r:
        raw = r.read().decode('utf-8', errors='replace')
    if not raw.strip():
        return []
    return json.loads(raw)

def stage0():
    all_stocks, page, empty = [], 1, 0
    while page <= 80 and empty < 3:
        try:
            rows = fetch_sina_page(page)
        except Exception as e:
            print(f'page {page} error: {e}', file=sys.stderr); time.sleep(1.0); continue
        if not rows:
            empty += 1; time.sleep(0.3); page += 1; continue
        empty = 0; all_stocks.extend(rows); page += 1; time.sleep(0.25)
    mb = []
    for s in all_stocks:
        code, name = s.get('code',''), s.get('name','')
        if 'ST' in name.upper() or '退' in name: continue
        if not code.startswith(('60','00')): continue      # 仅主板: 沪60/深00
        try:
            mb.append({'code': code, 'name': name,
                'price': float(s.get('trade',0) or 0), 'chg_pct': float(s.get('changepercent',0) or 0),
                'turnover': float(s.get('turnoverratio',0) or 0), 'pe': float(s.get('per',0) or 0),
                'pb': float(s.get('pb',0) or 0), 'mktcap_yi': float(s.get('mktcap',0) or 0)/1e4,
                'nmc_yi': float(s.get('nmc',0) or 0)/1e4, 'amount_yi': float(s.get('amount',0) or 0)/1e8})
        except (ValueError, TypeError): continue
    write_csv('data/market_snapshot.csv', mb)
    print(f'[0] 全市场 {len(all_stocks)} -> 主板 {len(mb)}', file=sys.stderr)
    return mb

# ---------- 阶段1: 价值底线+流动性 ----------
def stage1(rows):
    out = [s for s in rows
           if 0 < s['pe'] <= 35 and 0 < s['pb'] <= 6
           and 80 <= s['mktcap_yi'] <= 3000
           and s['amount_yi'] >= 3 and 1 <= s['turnover'] <= 15
           and s['chg_pct'] <= 9]
    out.sort(key=lambda s: s['amount_yi'], reverse=True)
    write_csv('data/candidates_l1.csv', out)
    print(f'[1] 通过 {len(out)}', file=sys.stderr)
    return out

# ---------- 阶段2: 趋势过滤 ----------
def kline_sina(code, datalen=70):
    sym = ('sh' if code.startswith('6') else 'sz') + code
    url = ('https://quotes.sina.cn/cn/api/jsonp_v2.php/var%20_=/CN_MarketDataService.getKLineData'
           f'?symbol={sym}&scale=240&ma=no&datalen={datalen}')
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=15) as r:
        raw = r.read().decode('utf-8', errors='replace')
    m = re.search(r'\((\[.*\])\)', raw, re.S)
    if not m: raise ValueError('bad kline response')
    return [float(x['close']) for x in json.loads(m.group(1))]

def trend_stats(closes):
    n = len(closes)
    if n < 30: return None
    c0, now = closes[0], closes[-1]
    hi = max(closes)
    return {'chg60': (now/c0-1)*100, 'drawdown': (now/hi-1)*100,
            'ma20': sum(closes[-20:])/20,
            'chg20': (now/closes[-21]-1)*100 if n >= 21 else None,
            'chg5': (now/closes[-6]-1)*100 if n >= 6 else None}

def stage2(rows):
    out = []
    for i, s in enumerate(rows):
        for _ in range(4):
            try:
                t = trend_stats(kline_sina(s['code'])); break
            except Exception:
                t = None; time.sleep(1.0)
        if not t: continue
        s.update(t)
        if not (-20 <= t['chg60'] <= 80): continue
        if t['drawdown'] < -30: continue
        if s['price'] < t['ma20'] * 0.92: continue
        if t['chg5'] is not None and t['chg5'] > 25: continue
        out.append(s); time.sleep(0.25)
        if (i+1) % 40 == 0: print(f'[2] ...{i+1}/{len(rows)} 通过 {len(out)}', file=sys.stderr)
    write_csv('data/candidates_l2.csv', out)
    print(f'[2] 通过 {len(out)}', file=sys.stderr)
    return out

# ---------- 阶段3: 综合打分 ----------
def score(s):
    pe, pb = s['pe'], s['pb']
    chg20, chg5, dd, to = s['chg20'], s['chg5'], s['drawdown'], s['turnover']
    v = 100 if 0 < pe <= 12 else 88 if pe <= 20 else 72 if pe <= 30 else 58 if pe <= 35 else 40
    if pb > 4.5: v -= 12
    elif pb > 3.5: v -= 6
    if chg20 is None: t = 50
    elif 5 <= chg20 <= 15: t = 100
    elif 15 < chg20 <= 25: t = 85
    elif 0 <= chg20 < 5: t = 80
    elif 25 < chg20 <= 40: t = 60
    elif -10 <= chg20 < 0: t = 50
    else: t = 35
    if chg5 is None: m = 50
    elif 0 <= chg5 <= 8: m = 95
    elif 8 < chg5 <= 15: m = 85
    elif 15 < chg5 <= 25: m = 60
    elif -8 <= chg5 < 0: m = 55
    else: m = 35
    a = 100 if 2 <= to <= 5 else 85 if to <= 8 else 70 if to >= 1 else 65
    return 0.30*v + 0.30*t + 0.20*m + 0.20*a

def stage3(rows, top=25):
    for s in rows: s['score'] = round(score(s), 1)
    rows.sort(key=lambda x: x['score'], reverse=True)
    write_csv('data/candidates_top25.csv', rows[:top])
    print(f'[3] Top{top} 已保存', file=sys.stderr)
    return rows[:top]

# ---------- 阶段4: 财务验证 ----------
def fetch_em(report, cols, code):
    secucode = code + ('.SH' if code.startswith('6') else '.SZ')
    qs = urllib.parse.urlencode({
        'reportName': report, 'columns': cols,
        'filter': f'(SECUCODE="{secucode}")',
        'pageNumber': '1', 'pageSize': '30',
        'sortTypes': '-1', 'sortColumns': 'REPORT_DATE'})
    req = urllib.request.Request(f'https://datacenter.eastmoney.com/securities/api/data/v1/get?{qs}', headers=UA_EM)
    with urllib.request.urlopen(req, timeout=20) as r:
        d = json.loads(r.read().decode('utf-8', errors='replace'))
    return (d.get('result') or {}).get('data') or []

def yearly(rows, field):
    out = {}
    for r in rows:
        rd = str(r.get('REPORT_DATE',''))[:10]
        if rd.endswith('-12-31') and r.get(field) is not None:
            out.setdefault(rd[:4], r[field])
    return out

def stage4(rows):
    out = []
    for s in rows:
        code = s['code']
        try:
            inc = fetch_em('RPT_DMSK_FN_INCOME', 'SECUCODE,REPORT_DATE,TOTAL_OPERATE_INCOME,PARENT_NETPROFIT', code)
            bal = fetch_em('RPT_DMSK_FN_BALANCE', 'SECUCODE,REPORT_DATE,TOTAL_EQUITY', code)
            cf  = fetch_em('RPT_DMSK_FN_CASHFLOW', 'SECUCODE,REPORT_DATE,NETCASH_OPERATE', code)
        except Exception as e:
            print(f'{code} 财务失败: {e}', file=sys.stderr); time.sleep(0.8); continue
        rev, np, eq, ocf = yearly(inc,'TOTAL_OPERATE_INCOME'), yearly(inc,'PARENT_NETPROFIT'), yearly(bal,'TOTAL_EQUITY'), yearly(cf,'NETCASH_OPERATE')
        r25, r24, n25, n24, e25, o25 = rev.get('2025'), rev.get('2024'), np.get('2025'), np.get('2024'), eq.get('2025'), ocf.get('2025')
        s.update({'rev25': r25, 'rev_g': (r25/r24-1)*100 if (r25 and r24) else None,
                  'np25': n25, 'np_g': (n25/n24-1)*100 if (n25 and n24) else None,
                  'roe25': n25/e25*100 if (n25 and e25) else None,
                  'ocf25': o25, 'ocf_ratio': o25/n25 if (o25 and n25) else None})
        out.append(s); time.sleep(0.3)
    write_csv('data/candidates_fin.csv', out)
    print(f'[4] 财务验证 {len(out)}', file=sys.stderr)
    return out

def write_csv(path, rows):
    if not rows: return
    with open(path, 'w', newline='', encoding='utf-8-sig') as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader(); w.writerows(rows)

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--top', type=int, default=25)
    ap.add_argument('--skip-fin', action='store_true', help='跳过财务验证阶段')
    args = ap.parse_args()
    r = stage0(); r = stage1(r); r = stage2(r); r = stage3(r, args.top)
    if not args.skip_fin:
        r = stage4(r)
    print('完成。结果见 data/ 目录。')
