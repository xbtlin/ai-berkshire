#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""重点超跌板块K线分析：250日趋势位置 + 60日/20日动量 + 距高点回撤"""
import json, time, urllib.request, csv, sys

UA = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

def board_kline(bkcode, days=250):
    url = (f'https://push2his.eastmoney.com/api/qt/stock/kline/get?secid=90.{bkcode}'
           f'&fields1=f1&fields2=f51,f53&klt=101&fqt=1&beg=0&end=20500101&lmt={days}')
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=15) as r:
        d = json.loads(r.read().decode('utf-8', errors='replace'))
    kl = (d.get('data') or {}).get('klines') or []
    return [float(x.split(',')[1]) for x in kl]

def stats(closes):
    n = len(closes)
    if n < 60:
        return None
    now = closes[-1]
    hi = max(closes)
    lo = min(closes)
    hi_idx, lo_idx = closes.index(hi), closes.index(lo)
    days_since_hi = n - 1 - hi_idx
    return {
        'now': now, 'hi': hi, 'lo': lo,
        'drawdown': (now / hi - 1) * 100,
        'from_lo': (now / lo - 1) * 100,
        'chg_60d': (now / closes[-61] - 1) * 100,
        'chg_20d': (now / closes[-21] - 1) * 100,
        'chg_5d': (now / closes[-6] - 1) * 100,
        'days_since_hi': days_since_hi,
        'ma20': sum(closes[-20:]) / 20,
        'ma60': sum(closes[-60:]) / 60,
        'above_ma20': now > sum(closes[-20:]) / 20,
        'above_ma60': now > sum(closes[-60:]) / 60,
        'n': n,
    }

# 重点超跌板块（从board_scan结果中选出的代表性板块代码）
boards = []
with open('data/boards_snapshot.csv', encoding='utf-8-sig') as f:
    for r in csv.DictReader(f):
        boards.append(r)

# 手动选择重点：新能源产业链 + 军工 + 逆变器 + 其他
watch = ['逆变器', '锂', '能源金属', '光伏设备', '光伏电池组件', '光伏加工设备', '风电设备', '风电零部件',
         '风电整机', '电池', '电池化学品', '锂电专用设备', '航天装备Ⅲ', '通信线缆及配套', '电网自动化设备', '体育Ⅲ', '化妆品制造及其他']
targets = [b for b in boards if b['name'] in watch]
print(f'重点板块 {len(targets)} 个\n')
print(f"{'板块':<10}{'现指':>9}{'60日':>7}{'20日':>7}{'5日':>7}{'距高点':>7}{'自低点':>7}{'距高天数':>7} {'MA20':>6}{'MA60':>6} 状态")
for b in targets:
    try:
        closes = board_kline(b['code'])
        s = stats(closes)
    except Exception as e:
        print(f"{b['name']} ERROR: {e}", file=sys.stderr)
        time.sleep(0.5)
        continue
    if not s:
        continue
    status = []
    if s['drawdown'] < -40: status.append('深跌')
    elif s['drawdown'] < -25: status.append('超跌')
    if s['above_ma20']: status.append('站上20日')
    if s['above_ma60']: status.append('站上60日')
    if s['chg_5d'] > 3 and s['chg_20d'] > 3: status.append('企稳反弹')
    if s['chg_20d'] < -5: status.append('仍在下跌')
    print(f"{b['name']:<10}{s['now']:>9.1f}{s['chg_60d']:>7.1f}{s['chg_20d']:>7.1f}{s['chg_5d']:>7.1f}"
          f"{s['drawdown']:>7.1f}{s['from_lo']:>7.1f}{s['days_since_hi']:>7d} {s['ma20']:>6.1f}{s['ma60']:>6.1f} {'/'.join(status)}")
    time.sleep(0.3)
