"""网易与百度底稿复算脚本（2026-09-12）。单位：人民币百万元（输出时折算为亿元）。
数据来源见《底稿-网易与百度.md》。"""
from decimal import Decimal as D, getcontext
getcontext().prec = 28
Y = lambda m: (D(m) / 100).quantize(D("0.01"))  # 百万元 -> 亿元

print("=== 网易 ===")
n = dict(fy25_rev=D("112625.8"), fy25_ni=D("33759.8"), h1_25_rev=D("56720.2"), h1_25_ni=D("18902.2"),
         h1_26_rev=D("60697.8"), h1_26_ni=D("17654.8"))
ttm_rev = n["fy25_rev"] + n["h1_26_rev"] - n["h1_25_rev"]
ttm_ni = n["fy25_ni"] + n["h1_26_ni"] - n["h1_25_ni"]
print("TTM收入", Y(ttm_rev), "TTM归母", Y(ttm_ni))
q = {  # Q3'25, Q4'25, Q1'26, Q2'26
 "rev":  [D("28358.6"), D("27547.0"), D("30591.3"), D("30106.5")],
 "ni":   [D("8615.7"), D("6242.0"), D("10674.1"), D("6980.7")],
 "op":   [D("8013.5"), D("8319.2"), D("12656.8"), D("12089.3")],
 "inv":  [D("1379.4"), D("-1669.1"), D("5.5"), D("-2953.7")],
 "int":  [D("936.7"), D("1002.4"), D("890.3"), D("863.2")],
 "fx":   [D("-373.8"), D("-518.0"), D("-622.1"), D("-436.5")],
 "oth":  [D("153.2"), D("485.9"), D("439.0"), D("62.9")],
 "tax":  [D("1316.4"), D("1250.4"), D("2523.8"), D("2458.7")],
 "sbc":  [D("886.4"), D("831.0"), D("600.7"), D("766.1")],
 "games":[D("23327.5"), D("21966.6"), D("25713.0"), D("25022.8")],
 "games_gp":[D("16176.4"), D("15494.4"), D("19230.5"), D("38279.4")-D("19230.5")],
 "youdao":[D("1628.5"), D("1564.7"), D("1348.0"), D("1466.9")],
 "youdao_gp":[D("687.9"), D("705.4"), D("602.3"), D("1319.2")-D("602.3")],
 "music":[D("1964.1"), D("1968.3"), D("1981.2"), D("1977.5")],
 "music_gp":[D("694.8"), D("682.3"), D("734.2"), D("1474.4")-D("734.2")],
 "inno":[D("1438.5"), D("2047.4"), D("1549.1"), D("1639.4")],
 "inno_gp":[D("618.6"), D("810.3"), D("650.1"), D("1361.5")-D("650.1")],
}
s = {k: sum(v) for k, v in q.items()}
for k in ["rev","ni","op","inv","int","fx","oth","tax","sbc","games","games_gp","youdao","youdao_gp","music","music_gp","inno","inno_gp"]:
    print(f"  TTM {k}: {Y(s[k])}")
print("  分部收入合计核对", Y(s["games"]+s["youdao"]+s["music"]+s["inno"]), "vs TTM收入", Y(ttm_rev))
nci_ttm = D("355.2") + (D("8615.7")-D("8615.7"))  # H1'26 少数股东 355.2；2025下半年少数股东未单列，按H1'26年化
nci_annual = D("355.2") * 2
pretax_norm = s["op"] + s["int"] + s["oth"]          # 剔除投资损益与汇兑
norm_tax_rate = D("0.18")
norm_ni = pretax_norm * (1 - norm_tax_rate) - nci_annual
print("  正常化税前(经营利润+净利息+其他收入)", Y(pretax_norm))
print("  正常化税后归母 = 税前×(1-18%) − 少数股东", Y(norm_ni))
print("  报表TTM归母", Y(ttm_ni), "差额", Y(norm_ni - ttm_ni))
print("  TTM投资损益+汇兑", Y(s["inv"]+s["fx"]), " TTM实际所得税", Y(s["tax"]), "TTM有效税率", (s["tax"]/(s["op"]+s["inv"]+s["int"]+s["fx"]+s["oth"])*100).quantize(D("0.1")), "%")
cash = D("22814.5")+D("101978.6")+D("260.0")+D("50599.6")
print("  现金+定存+短期投资(不含受限)", Y(cash), " 含受限", Y(cash+D("4451.3")))
print("  2025现金分红", Y(D("13825.681")), "2025回购净额", Y(D("639.335")))
# 2036情景
base = dict(games=D("1000"), youdao=D("60"), music=D("80"), inno=D("65"))
sc = {
 "悲观": dict(games=(D("0.00"),D("0.25")), youdao=(D("0.00"),D("0.00")), music=(D("0.00"),D("0.10")), inno=(D("-0.02"),D("0.00")), other=D("20")),
 "基准": dict(games=(D("0.05"),D("0.32")), youdao=(D("0.05"),D("0.06")), music=(D("0.04"),D("0.15")), inno=(D("0.03"),D("0.05")), other=D("40")),
 "乐观": dict(games=(D("0.08"),D("0.35")), youdao=(D("0.10"),D("0.10")), music=(D("0.07"),D("0.18")), inno=(D("0.06"),D("0.08")), other=D("60")),
}
chk = base["games"]*D("0.33")+base["youdao"]*D("0.02")+base["music"]*D("0.12")+base["inno"]*D("0.05")+D("30")
print("  2026校核利润", chk)
for name, a in sc.items():
    tot_rev = D(0); ni = a["other"]
    for k in base:
        g, m = a[k]; r = base[k]*(1+g)**10; tot_rev += r; ni += r*m
    print(f"  {name}: 2036收入合计 {tot_rev.quantize(D('1'))} 归母经济净利 {ni.quantize(D('0.01'))}")

print("\n=== 百度 ===")
b = dict(fy25_rev=D("129079"), fy25_ni=D("5589"), h1_25_rev=D("65165"), h1_25_ni=D("15039"), h1_26_rev=D("63400"), h1_26_ni=D("5764"))
ttm_rev_b = b["fy25_rev"] + b["h1_26_rev"] - b["h1_25_rev"]
ttm_ni_b = b["fy25_ni"] + b["h1_26_ni"] - b["h1_25_ni"]
print("TTM收入", Y(ttm_rev_b), "TTM归母", Y(ttm_ni_b))
qb = {  # Q3'25, Q4'25, Q1'26, Q2'26
 "rev":[D("31174"),D("32740"),D("32075"),D("31325")],
 "ni":[D("-11232"),D("1782"),D("3445"),D("2319")],
 "nongaap":[D("3770"),D("3907"),D("4332"),D("2573")],
 "op":[D("-15091"),D("1483"),D("3193"),D("3024")],
 "core_rev":[D("24659"),D("26112"),D("26001"),D("25183")],
 "core_op":[D("-14971"),D("1441"),D("3416"),D("3131")],
 "core_op_nongaap":[D("2225"),D("2837"),D("3950"),D("3818")],
 "online":[D("15300"),D("17900")*D("0.84"),D("12600"),D("13100")],  # Q4'25为推算：Q4'24 179亿×(1−16%)
 "iqiyi_rev":[D("6682"),D("6794"),D("6226"),D("6287")],
 "iqiyi_op":[D("-15091")-D("-14971"),D("55"),D("-228"),D("-105")],  # Q3'25按合并−核心倒算，含少量抵销
 "other_inc":[D("1946"),D("1200"),D("626"),D("184")],
 "tax":[D("-1828"),D("1000"),D("528"),D("1000")],
 "sbc":[D("1044"),D("729"),D("519"),D("669")],
 "capex":[D("0"),D("0"),D("5916"),D("11390")],
}
sb = {k: sum(v) for k, v in qb.items()}
for k in ["rev","ni","nongaap","op","core_rev","core_op","core_op_nongaap","online","iqiyi_rev","iqiyi_op","other_inc","tax","sbc"]:
    print(f"  TTM {k}: {Y(sb[k])}")
print("  TTM非在线营销(核心−在线营销)", Y(sb["core_rev"]-sb["online"]))
print("  核心经营利润剔除减值161.9亿", Y(sb["core_op"]+D("16190")), " 合并经营利润剔除减值", Y(sb["op"]+D("16190")))
# 正常化A：非GAAP归母 − 股权激励（保留为经常性成本）
normA = sb["nongaap"] - sb["sbc"]
print("  正常化A = 非GAAP归母TTM − 股权激励TTM =", Y(sb["nongaap"]), "−", Y(sb["sbc"]), "=", Y(normA))
# 正常化B：自下而上
int_net = (D("1685")-D("608"))*4   # 以Q2'26净利息年化
eq_share = (D("357")+D("536"))*2   # 权益法收益按H1'26年化
pretax_b = sb["op"] + D("16190") + int_net + eq_share
tax_b = pretax_b * D("0.15")
nci_b = D("-200")  # 研究假设：爱奇艺等亏损中归少数股东部分约+2亿，取−2亿意为少数股东分担亏损后对归母的净影响为正
normB = pretax_b - tax_b - nci_b
print("  正常化B: 剔减值经营利润", Y(sb["op"]+D("16190")), "+净利息年化", Y(int_net), "+权益法收益年化", Y(eq_share), "=税前", Y(pretax_b), "−15%税", Y(tax_b), "+少数股东分担", Y(-nci_b), "=", Y(normB))
for inv in (D("3000"), D("4000"), D("6000")):
    print(f"  再剔除AI主动投入税前{Y(inv)}亿 → 正常化A+{Y(inv*D('0.85'))} = {Y(normA+inv*D('0.85'))}")
debt = D("26311")+D("2027")+D("20779")+D("2038")+D("46089")+D("1")+D("6615")
print("  有息负债合计", Y(debt), " 现金+短期投资", Y(D("24524")+D("141727")), " 加长期定存/持有至到期", Y(D("24524")+D("141727")+D("74311")))
print("  2025回购 US$677M × 7.19 ≈", (D("677")*D("7.19")/100).quantize(D("0.1")), "亿元(估算汇率)")
print("  股本 2,197,993,760 + 524,020,320 =", 2197993760+524020320, "; 2026-01-31:", 2198000952+524020320, "; ADS当量(÷8)=", (2198000952+524020320)/8/1e6, "百万ADS")
baseb = dict(online=D("520"), ai=D("500"))
scb = {
 "悲观": dict(online=(D("-0.06"),D("0.18")), ai=(D("0.06"),D("0.02")), iqiyi=D("-3"), other=D("30")),
 "基准": dict(online=(D("-0.02"),D("0.24")), ai=(D("0.12"),D("0.08")), iqiyi=D("3"), other=D("45")),
 "乐观": dict(online=(D("0.01"),D("0.28")), ai=(D("0.18"),D("0.12")), iqiyi=D("8"), other=D("60")),
}
print("  2026校核利润", baseb["online"]*D("0.24")+baseb["ai"]*D("-0.07")+D("0")+D("40"))
for name, a in scb.items():
    tot = D(0); ni = a["iqiyi"] + a["other"]
    for k in baseb:
        g, m = a[k]; r = baseb[k]*(1+g)**10; tot += r; ni += r*m
    print(f"  {name}: 2036两项收入合计 {tot.quantize(D('1'))} 归母经济净利 {ni.quantize(D('0.01'))}")
