"""估值分位复算脚本（2026-09-12）。
数据来自 tools/quant 管线生成的 local/quant-data/panel/{ticker}.parquet（不入库）。
PE/PB/PCF 为百度股市通口径按日频重算；静态PS = 报表币市值 / 最近已披露年度收入（年报可得日按次年3月31日）。
分位 = 窗口内严格小于当前值的交易日占比；PE 分位剔除亏损期（PE<=0）。
"""
import pandas as pd
REV = {
 "0700.HK": {2004:11.44,2005:14.26,2006:28.00,2007:38.21,2008:71.55,2009:124.40,2010:196.46,2011:284.96,2012:438.94,2013:604.37,2014:789.32,2015:1028.63,2016:1519.38,2017:2377.60,2018:3126.94,2019:3772.89,2020:4820.64,2021:5601.18,2022:5545.52,2023:6090.15,2024:6602.57,2025:7517.66},
 "PDD": {2018:131.20,2019:301.42,2020:594.92,2021:939.50,2022:1305.58,2023:2476.39,2024:3938.36,2025:4318.46},
 "3690.HK": {2018:652.27,2019:975.29,2020:1147.95,2021:1791.28,2022:2199.55,2023:2767.45,2024:3375.92,2025:3648.55},
 "1024.HK": {2021:810.82,2022:941.83,2023:1134.70,2024:1268.98,2025:1427.76},
}
SCALE = {"0700.HK": 428.40/425.60, "3690.HK": 75.10/74.75, "1024.HK": 31.26/31.66, "PDD": 1.0}  # 管线最新日为9/10（PDD为9/11），按9/11收盘价平移
for t in REV:
    p = pd.read_parquet(f"local/quant-data/panel/{t}.parquet").sort_values("date").reset_index(drop=True)
    rev = pd.Series(REV[t]); avail = pd.DataFrame({"date": [pd.Timestamp(f"{y+1}-03-31") for y in rev.index], "rev": rev.values})
    p = pd.merge_asof(p, avail, on="date"); p["ps_static"] = p.market_cap_report_ccy/1e8/p.rev
    last = p.iloc[-1]
    for m in ["pe_ttm", "pb", "ps_static"]:
        v = float(last[m]) * SCALE[t]
        line = f"{t:8s} {m:10s} 现值 {v:7.2f}"
        for lab, days in [("5年", 5*365), ("10年", 10*365), ("20年", 20*365), ("上市以来", 99*365)]:
            w = p[p.date >= last.date - pd.Timedelta(days=days)]; s = w[m].dropna()
            if m == "pe_ttm": s = s[s > 0]
            pct = None if (m == "pe_ttm" and v < 0) else (s < v).mean()*100
            line += f" | {lab} 分位 {'亏损' if pct is None else f'{pct:5.1f}%'} 中位 {s.median():6.2f} 最低 {s.min():6.2f} 起 {w.date.min().date()}"
        print(line)
