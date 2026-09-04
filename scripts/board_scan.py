#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""板块超跌扫描：拉全行业板块，按60日跌幅排序，找抄底候选"""
import json, time, urllib.request, csv, sys

UA = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
      'Referer': 'https://quote.eastmoney.com/'}

def fetch_boards(page, pz=100, fid='f24', asc=0):
    url = ('https://push2.eastmoney.com/api/qt/clist/get'
           f'?pn={page}&pz={pz}&po=1&np=1&fltt=2&invt=2&fid={fid}&asc={asc}'
           f'&fs=m:90+t:2+f:!50&fields=f2,f3,f12,f14,f24,f25,f104,f105,f128,f136,f140,f8')
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=15) as r:
        d = json.loads(r.read().decode('utf-8', errors='replace'))
    return (d.get('data') or {}).get('diff') or []

def get_pct(v):
    """f24/f25等字段: fltt=2时直接是百分比数值，但可能以万/亿单位返回，需验证"""
    return v

all_boards = []
page = 1
while page <= 6:
    rows = fetch_boards(page)
    if not rows:
        break
    all_boards.extend(rows)
    page += 1
    time.sleep(0.25)

print(f'共获取板块 {len(all_boards)} 个', file=sys.stderr)

parsed = []
for b in all_boards:
    try:
        parsed.append({
            'code': b.get('f12', ''),
            'name': b.get('f14', ''),
            'chg_today': float(b.get('f3') or 0),
            'chg_60d': float(b.get('f24') or 0),
            'chg_ytd': float(b.get('f25') or 0),
            'up': int(b.get('f104') or 0),
            'down': int(b.get('f105') or 0),
            'leader': b.get('f128', ''),
            'leader_code': b.get('f140', ''),
            'turnover': float(b.get('f8') or 0),
        })
    except (TypeError, ValueError):
        continue

parsed.sort(key=lambda x: x['chg_60d'])

with open('data/boards_snapshot.csv', 'w', newline='', encoding='utf-8-sig') as f:
    w = csv.DictWriter(f, fieldnames=['code','name','chg_today','chg_60d','chg_ytd','up','down','leader','leader_code','turnover'])
    w.writeheader()
    w.writerows(parsed)

print(f'\n===== 60日跌幅最大前40板块 =====')
for b in parsed[:40]:
    print(f"{b['chg_60d']:>7.1f}% {b['name']:<10} 今{b['chg_today']:>6.2f}% 年初{b['chg_ytd']:>7.1f}% 涨跌{b['up']}/{b['down']} 领涨:{b['leader']}")
