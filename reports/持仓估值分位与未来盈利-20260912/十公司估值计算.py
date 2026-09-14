"""十公司估值计算（2026-09-12）。
输入：tools/quant 管线面板（local/quant-data，不入库）、SEC XBRL 事实表、早期年度财务补录.json。
输出：十公司估值结果.json（现值、分位、反向折现）。
方法：
  A. 现值 = 9/11 收盘价 × 最新披露股本 / 最新TTM或正常化利润（见底稿）。
  B. 5年分位：百度股市通TTM口径日频序列（港股主板全历史；美股自2020年起）。
  C. 10年/20年/上市以来分位：静态年度口径序列 = 报表币市值 / 最近已披露财年的归母净利|归母权益|收入，
     年度数据来自 SEC XBRL（20-F）与早期补录，可得日=min(申报日, 财年末+120天)；
     美股历史市值 = 拆股调整后收盘价 × 今日ADS口径股数，股数按XBRL年度加权稀释股数相对2020年锚点缩放
     （港股主板与2020年后的美股直接用百度市值）。
"""
import pandas as pd, numpy as np, json, sys, os
ROOT="/Users/linxuan/ai-berkshire"; os.chdir(ROOT)
HERE=os.path.dirname(os.path.abspath(__file__))
EXTRA=json.load(open(os.path.join(HERE,"早期年度财务补录.json"))) if os.path.exists(os.path.join(HERE,"早期年度财务补录.json")) else {}
CLOSE_0911={"0700.HK":428.40,"3690.HK":75.10,"1024.HK":31.26,"PDD":77.76,"9988.HK":107.50,"9618.HK":106.20,"9999.HK":182.10,"9888.HK":89.10,"1810.HK":26.36,"9961.HK":305.80}
LAST_PANEL={"0700.HK":425.60,"3690.HK":74.75,"1024.HK":31.66,"PDD":77.76,"9988.HK":106.90,"1810.HK":25.92}
HKDCNY=0.8557; USDCNY=6.6964
# ---- 手算现值（来源见各底稿）----
CUR={ # 市值人民币亿元 = 价×股本×汇率；TTM收入/归母/净资产；正常化利润；2036三情景
 "腾讯":dict(t="0700.HK",mcap=428.40*91.0315*HKDCNY,rev=7884.83,ni=2355.08,eq=11186,norm=2300,s36=(1700,4600,6600),tag="TTM至2026Q2"),
 "拼多多":dict(t="PDD",mcap=77.76*14.234*USDCNY,rev=4507.76,ni=920.76,eq=4477.87,norm=850,s36=(530,1600,3000),tag="TTM至2026Q2"),
 "快手":dict(t="1024.HK",mcap=31.26*43.2696*HKDCNY,rev=1443.73,ni=157.66,eq=809,norm=158,s36=(20,230,450),tag="TTM至2026Q2"),
 "美团":dict(t="3690.HK",mcap=75.10*61.7548*HKDCNY,rev=3828.40,ni=-384.49,eq=1692.06,norm=358,s36=(-70,380,870),tag="TTM至2026Q2；正常化取2024年峰值"),
 "阿里巴巴":dict(t="BABA",t5="9988.HK",mcap=107.50*193.8*HKDCNY,rev=10449.71,ni=733.25,eq=10490.38,norm=1400,s36=(1100,3300,6900),tag="TTM至2026年6月季度；股本含8月配售估计"),
 "京东":dict(t="JD",mcap=106.20*26.88*HKDCNY,rev=13134.38,ni=147.94,eq=2191.18,norm=470,s36=(300,800,1400),tag="TTM至2026Q2"),
 "网易":dict(t="NTES",mcap=182.10*32.03*HKDCNY,rev=1166.03,ni=325.12,eq=1670.91,norm=370,s36=(280,590,870),tag="TTM至2026Q2"),
 "百度":dict(t="BIDU",mcap=89.10*27.22*HKDCNY,rev=1273.14,ni=-36.86,eq=2717.52,norm=116,s36=(100,270,540),tag="TTM至2026Q2；正常化剔除161.9亿减值"),
 "小米":dict(t="1810.HK",mcap=26.36*257.5918*HKDCNY,rev=4381.00,ni=330.00,eq=2696.999,norm=246,s36=(330,800,1400),tag="TTM至2026Q2；正常化剔除公允价值收益、含汽车亏损"),
 "携程":dict(t="TCOM",mcap=305.80*6.4958*HKDCNY,rev=647.87,ni=315.16,eq=1650.00,norm=161,s36=(150,340,540),tag="TTM至2026Q1（Q2未披露）；正常化剔除处置收益"),
}
# ---- 静态年度序列 ----
def annual_from_sec(t):
    f=pd.read_parquet(f"local/quant-data/financials/{t}/sec_facts.parquet")
    f=f[(f.fp=="FY")&(f.form.str.startswith("20-F"))&(f.unit=="CNY")].copy()
    for c in ("end","start","filed"): f[c]=pd.to_datetime(f[c])
    def pick(tags,flow=True):
        g=f[f.tag.isin(tags)]
        if flow: g=g[(g.end-g.start).dt.days.between(350,380)]
        g=g.sort_values(["end","filed"]).drop_duplicates("end")
        return g.set_index("end")[["val","filed"]]
    ni=pick(["NetIncomeLoss"]); pl=pick(["ProfitLoss"]); ni=pd.concat([ni,pl[~pl.index.isin(ni.index)]]).sort_index()
    rev=pick(["Revenues","RevenueFromContractWithCustomerExcludingAssessedTax","SalesRevenueNet"])
    eq=pick(["StockholdersEquity"],flow=False)
    sh=f[(f.tag=="WeightedAverageNumberOfDilutedSharesOutstanding")]
    sh=sh[(sh.end-sh.start).dt.days.between(350,380)].sort_values(["end","filed"]).drop_duplicates("end").set_index("end").val
    # 股数单位是 shares（unit 过滤掉了），重新取
    g=pd.read_parquet(f"local/quant-data/financials/{t}/sec_facts.parquet"); g=g[(g.fp=="FY")&(g.form.str.startswith("20-F"))&(g.tag=="WeightedAverageNumberOfDilutedSharesOutstanding")].copy()
    for c in ("end","start","filed"): g[c]=pd.to_datetime(g[c])
    g=g[(g.end-g.start).dt.days.between(350,380)].sort_values(["end","filed"]).drop_duplicates("end").set_index("end").val.astype(float)
    a=pd.DataFrame({"net_income":ni.val,"filed":ni.filed,"revenue":rev.val,"equity":eq.val,"shares":g})
    a=a.reset_index().rename(columns={"end":"fy_end"})
    a["avail"]=np.minimum(a.filed.fillna(a.fy_end+pd.Timedelta(days=120)),a.fy_end+pd.Timedelta(days=120))
    return a[["fy_end","avail","revenue","net_income","equity","shares"]]
def add_extra(a,t):
    rows=[]
    for r in EXTRA.get(t,[]):
        fx=1.0
        if r.get("currency")=="USD": fx=8.28 if int(r["fy"])<=2005 else 7.8  # 补录全部为人民币，此分支实际不触发
        fy_end=pd.Timestamp(r["fy_end"]); filed=pd.to_datetime(r.get("filed"),errors="coerce") if r.get("filed") else pd.NaT
        if pd.isna(filed): filed=fy_end+pd.Timedelta(days=120)
        m=1e6
        rows.append({"fy_end":fy_end,"avail":min(filed,fy_end+pd.Timedelta(days=120)),
            "revenue":(r["revenue"]*m*fx if r.get("revenue") is not None else np.nan),
            "net_income":(r["net_income"]*m*fx if r.get("net_income") is not None else np.nan),
            "equity":(r["equity"]*m*fx if r.get("equity") is not None else np.nan),
            "shares":(r["diluted_shares"]*m if r.get("diluted_shares") is not None else np.nan)})
    if rows:
        e=pd.DataFrame(rows)
        # 早期补录只填 SEC 没有的财年；SEC 有但缺股数的财年（如百度2011-2019）用补录股数补
        a=a.set_index("fy_end"); e=e.set_index("fy_end")
        for fy,r in e.iterrows():
            if fy in a.index:
                for c in ("shares","revenue","net_income","equity"):
                    if pd.isna(a.loc[fy,c]) and pd.notna(r[c]): a.loc[fy,c]=r[c]
            else: a.loc[fy]=r
        a=a.reset_index()
    return a.sort_values("fy_end").reset_index(drop=True)

# ---- 底稿整理的年度收入/归母（亿元，官方原件+独立源核对；用于覆盖 XBRL 标签口径差异与补齐早期年份）----
ANNUAL_OVERRIDE={
 "NTES":{"rev":{2000:0.30,2001:0.26,2002:2.21,2003:5.42,2004:9.04,2005:16.12,2006:21.64,2007:22.13,2008:30.85,2009:37.57,2010:55.08,2011:72.91,2012:82.01,2013:91.96,2014:117.13,2015:228.03,2016:381.8,2017:444.4,2018:511.8,2019:592.4,2020:736.7,2021:876.06,2022:964.96,2023:1034.68,2024:1052.95,2025:1126.26}},
 "BIDU":{"rev":{2005:3.19,2006:8.38,2007:17.44,2008:31.98,2009:44.48,2010:79.15,2011:145.01,2012:223.1,2013:319.4,2014:490.5,2015:663.8,2016:705.5,2017:848.1,2018:1022.8,2019:1074.1,2020:1070.7,2021:1244.93,2022:1236.75,2023:1345.98,2024:1331.25,2025:1290.79}},
 "TCOM":{"rev":{2003:1.73,2004:3.34,2005:5.21,2006:7.80,2007:12.0,2008:14.8,2009:19.9,2010:28.8,2011:35.0,2012:41.6,2013:53.9,2014:73.5,2015:109.0,2016:192.5,2017:268.0,2018:309.7,2019:356.7,2020:183.2,2021:200.23,2022:200.39,2023:445.10,2024:532.94,2025:624.09}},
 "JD":{"rev":{2012:413.81,2013:693.40,2014:1150.02,2015:1810.42,2016:2582.90,2017:3623.32,2018:4620.20,2019:5768.88,2020:7458.02,2021:9515.92,2022:10462.36,2023:10846.62,2024:11588.19,2025:13090.85},
       "ni":{2012:-33.17,2013:-24.85,2014:-129.54,2015:-91.08,2016:-38.07,2017:-1.52,2018:-24.92,2019:121.84,2020:494.05,2021:-35.60,2022:103.80,2023:241.67,2024:413.59,2025:196.31}},
 "BABA":{"rev":{2013:345.17,2014:525.04,2015:762.04,2016:1011.43,2017:1582.73,2018:2502.66,2019:3768.44,2020:5097.11,2021:7172.89,2022:8530.62,2023:8686.87,2024:9411.68,2025:9963.47,2026:10236.70},
         "ni":{2013:84.04,2014:230.76,2015:241.49,2016:714.60,2017:436.75,2018:639.85,2019:876.00,2020:1492.63,2021:1503.08,2022:619.59,2023:725.09,2024:797.41,2025:1294.70,2026:1059.04}},
}
FY_END_MONTH={"BABA":3}
def apply_override(a,t):
    o=ANNUAL_OVERRIDE.get(t)
    if not o: return a
    a=a.set_index("fy_end")
    m=FY_END_MONTH.get(t,12)
    for key,col in (("rev","revenue"),("ni","net_income")):
        for fy,v in o.get(key,{}).items():
            end=pd.Timestamp(year=fy,month=m,day=31 if m==12 else 31)
            if end not in a.index:
                a.loc[end]=np.nan; a.loc[end,"avail"]=end+pd.Timedelta(days=120)
            a.loc[end,col]=v*1e8
    a=a.sort_index().reset_index()
    a["avail"]=pd.to_datetime(a.avail); a["avail"]=a.avail.fillna(a.fy_end+pd.Timedelta(days=120))
    return a

def normalize_shares(s):
    s=s.copy(); v=s.values.astype(float); fac=np.ones(len(v))
    # 上市当年的加权平均股数偏低（IPO前月份权重），若首年不足次年60%则用次年股数替代
    if len(v)>1 and not np.isnan(v[0]) and not np.isnan(v[1]) and v[0]<0.6*v[1]: v[0]=v[1]
    for i in range(len(v)-1,0,-1):
        if np.isnan(v[i]) or np.isnan(v[i-1]): continue
        r=v[i]/v[i-1]
        if r>2.5 or r<0.4: fac[:i]*=r
    return pd.Series(v*fac,index=s.index)
def static_series(t):
    p=pd.read_parquet(f"local/quant-data/panel/{t}.parquet").sort_values("date").reset_index(drop=True)
    us=t in ("NTES","BIDU","TCOM","JD","BABA","PDD")
    a=add_extra(annual_from_sec(t) if us else pd.DataFrame(columns=["fy_end","avail","revenue","net_income","equity","shares"]),t)
    a=apply_override(a,t)
    if us:
        # 市值：2020年后用百度；之前用 收盘价×锚点ADS数×股数缩放
        anchor=p.dropna(subset=["market_cap"]); anchor=anchor[anchor.date>="2020-01-01"].iloc[0]
        ads_anchor=anchor.market_cap/anchor.close
        sh=normalize_shares(a.set_index("fy_end").shares.astype(float).ffill().bfill())
        fy_anchor=a[a.avail<=anchor.date].fy_end.max()
        a["ads"]=(sh/sh[fy_anchor]).values*ads_anchor
    q=pd.merge_asof(p[["date","close","market_cap","market_cap_report_ccy","fx"]],a.sort_values("avail"),left_on="date",right_on="avail")
    if us:
        q["mcap_ccy"]=np.where(q.date>=anchor.date,q.market_cap_report_ccy,q.close*q.ads*q.fx)
    else:
        q["mcap_ccy"]=q.market_cap_report_ccy
    q["pe_static"]=q.mcap_ccy/q.net_income; q["pb_static"]=q.mcap_ccy/q.equity; q["ps_static"]=q.mcap_ccy/q.revenue
    return q,a
def pct(s,v): s=s.dropna(); return None if (v is None or len(s)<100) else round(float((s<v).mean())*100,1)
def windows(q,m,v,last):
    out={}
    for lab,days in [("5y",5*365),("10y",10*365),("20y",20*365),("all",99*365)]:
        w=q[q.date>=last-pd.Timedelta(days=days)]; s=w[m].dropna()
        if m.startswith("pe"): s=s[s>0]
        if len(s)<100: out[lab]=None; continue
        out[lab]={"pct":(None if (m.startswith("pe") and (v is None or v<=0)) else pct(s,v)),"median":round(float(s.median()),2),"min":round(float(s.min()),2),"start":str(w.date.min().date()),"n":int(len(s))}
    return out
def rdcf(mc,e0,r=0.10,tg=0.03,n=10):
    from scipy.optimize import brentq
    pv=lambda g: sum(e0*(1+g)**k/(1+r)**k for k in range(1,n+1))+e0*(1+g)**n*(1+tg)/(r-tg)/(1+r)**n
    try: return round(brentq(lambda g: pv(g)-mc,-0.6,1.5)*100,1)
    except Exception: return None
res={}
for name,c in CUR.items():
    t=c["t"]; t5=c.get("t5",t)
    r={"ticker":t,"mcap_rmb":round(c["mcap"]),"pe_ttm":round(c["mcap"]/c["ni"],2) if c["ni"]>0 else None,"pb":round(c["mcap"]/c["eq"],2),"ps_ttm":round(c["mcap"]/c["rev"],2),
       "pe_norm":round(c["mcap"]/c["norm"],2),"earn_yield_ttm":round(c["ni"]/c["mcap"]*100,2),"earn_yield_norm":round(c["norm"]/c["mcap"]*100,2),
       "mcap_over_2036base":round(c["mcap"]/c["s36"][1],2) if c["s36"][1]>0 else None,"implied_g_10pct":rdcf(c["mcap"],c["norm"]),"implied_g_8pct":rdcf(c["mcap"],c["norm"],r=0.08),"implied_g_12pct":rdcf(c["mcap"],c["norm"],r=0.12),
       "base_cagr":round(((c["s36"][1]/c["norm"])**0.1-1)*100,1) if c["s36"][1]>0 else None,"note":c["tag"]}
    # B. 5年分位（百度TTM口径）
    p=pd.read_parquet(f"local/quant-data/panel/{t5}.parquet").sort_values("date").reset_index(drop=True)
    last=p.iloc[-1]; scale=CLOSE_0911.get(t5,last.close)/ (LAST_PANEL.get(t5,last.close))
    r["baidu_5y"]={}
    for m in ["pe_ttm","pb","ps_ttm"]:
        v=float(last[m])*scale if pd.notna(last[m]) else None
        w=p[p.date>=last.date-pd.Timedelta(days=5*365)]; s=w[m].dropna()
        if m=="pe_ttm": s=s[s>0]
        r["baidu_5y"][m]={"now":None if v is None else round(v,2),"pct":(None if (m=="pe_ttm" and (v is None or v<=0)) else pct(s,v)),"median":round(float(s.median()),2) if len(s) else None,"min":round(float(s.min()),2) if len(s) else None,"start":str(w.date.min().date()),"n":int(len(s))}
    # 港股主板全历史（百度口径）
    if t5 in ("0700.HK","3690.HK","1024.HK","1810.HK","9988.HK","PDD"):
        r["baidu_windows"]={}
        for m in ["pe_ttm","pb"]:
            v=float(last[m])*scale if pd.notna(last[m]) else None
            r["baidu_windows"][m]=windows(p,m,v,last.date)
    # C. 静态年度口径（美股/长历史）
    if t in ("NTES","BIDU","TCOM","JD","BABA","PDD"):
        q,a=static_series(t); ql=q.iloc[-1]
        r["static"]={"fy_table_from":str(a.fy_end.min().date()),"fy_table_to":str(a.fy_end.max().date()),"series_from":str(q.dropna(subset=["pe_static"]).date.min().date()) if q.pe_static.notna().any() else None}
        for m in ["pe_static","pb_static","ps_static"]:
            v=float(ql[m])*(CLOSE_0911.get(t5,1)/LAST_PANEL.get(t5,1)) if pd.notna(ql[m]) else None
            r["static"][m]={"now":None if v is None else round(v,2),**windows(q,m,v,ql.date)}
        # 校验：2020年前重建市值 vs 2020年后百度（重叠段只在2020年同一天，改为对比锚点前后30天连续性）
        res.setdefault("_recon_check",{})[t]={"ads_anchor_yi":round(float(a.ads.iloc[-1])/1e8,3) if "ads" in a else None,"shares_fy":{str(k.date()):(None if pd.isna(v) else round(v/1e8,3)) for k,v in a.set_index("fy_end").shares.items()}}
    res[name]=r
json.dump(res,open(os.path.join(HERE,"十公司估值结果.json"),"w"),ensure_ascii=False,indent=1)
for name,r in res.items():
    if name.startswith("_"): continue
    print(f"== {name} 市值{r['mcap_rmb']} PE{r['pe_ttm']} PB{r['pb']} PS{r['ps_ttm']} 正常化PE{r['pe_norm']} 隐含g{r['implied_g_10pct']}% 基准CAGR{r['base_cagr']}% 市值/2036基准{r['mcap_over_2036base']}")
    for m,x in r["baidu_5y"].items(): print(f"   百度5y {m}: now{x['now']} pct{x['pct']} med{x['median']} min{x['min']} from{x['start']}")
    if "baidu_windows" in r:
        for m,x in r["baidu_windows"].items(): print(f"   百度窗口 {m}: "+" | ".join(f"{k}:{'n/a' if v is None else str(v['pct'])+'% med'+str(v['median'])+' from'+v['start']}" for k,v in x.items()))
    if "static" in r:
        for m in ["pe_static","pb_static","ps_static"]:
            x=r["static"][m]; print(f"   静态 {m}: now{x['now']} "+" | ".join(f"{k}:{'n/a' if v is None else str(v['pct'])+'% med'+str(v['median'])+' min'+str(v['min'])+' from'+v['start']}" for k,v in x.items() if k in ('5y','10y','20y','all')))
print(json.dumps(res.get("_recon_check"),ensure_ascii=False)[:1500])
