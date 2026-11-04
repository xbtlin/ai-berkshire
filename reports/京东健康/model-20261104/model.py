"""京东健康估值复算。金额单位为亿元人民币，价格、每股指标为港元。运行此文件即可复算。"""
from decimal import Decimal as D
from pathlib import Path
import json
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
from terminal_value import exit_pe, irr_from_terminal

PRICE, FX, SHARES = D("40.14"), D("0.85581"), D("31.90481011")
MCAP = PRICE * FX * SHARES
PROFIT = D("53.75405") + D("34.36804") - D("25.96445")
PRODUCT = D("608.84805") + D("339.03508") - D("293.31139")
SERVICE = D("125.56682") + D("69.84376") - D("59.58908")
# 概率、两项收入增速、五年/十年归母利润率、永续增长。
CASES = [
    ("悲观", ".25", ".03", ".05", ".05", ".045", "0"),
    ("基准", ".55", ".08", ".12", ".08", ".085", ".02"),
    ("乐观", ".20", ".11", ".17", ".09", ".105", ".03"),
]
RATE, ROIC = D(".08"), D(".15")


def run(tool, *args):
    command = [sys.executable, str(ROOT / "tools" / (tool + ".py")), *map(str, args)]
    subprocess.run(command, check=True)


def reverse_growth(payout):
    """各年可分配现金占利润的比例固定，反解统一的前十年归母利润增速。"""
    terminal_pe = (1 - D(".02") / ROIC) / (RATE - D(".02"))
    lo, hi = D("-.2"), D(".4")
    for _ in range(110):
        growth = (lo + hi) / 2
        factor = (1 + growth) / (1 + RATE)
        pv = PROFIT * (payout * sum(factor ** t for t in range(1, 11)) + terminal_pe * factor ** 10)
        if pv < MCAP:
            lo = growth
        else:
            hi = growth
    return (lo + hi) / 2


def main():
    cross = [
        ("总股本（亿股）", str(SHARES), "31.9048", "HKEX", "同花顺"),
        ("2025营收", "734.41487", "734.41", "年报", "S&P"),
        ("2025归母", "53.75405", "53.75", "年报", "S&P"),
        ("TTM归母", str(PROFIT), "62.16", "公告桥接", "S&P"),
        ("H1现金等价物", "204.45564", "204.46", "中报", "S&P"),
        ("H1流动现金及理财扣租赁", "483.98362", "483.98", "中报附注", "S&P"),
        ("H1广义资金储备", "714.96821", "715", "中报附注加总", "GPLP转述"),
    ]
    for field, value1, value2, source1, source2 in cross:
        run("financial_rigor", "cross-validate", "--field", field, "--values",
            json.dumps({source1: float(value1), source2: float(value2)}, ensure_ascii=False), "--unit", "亿", "--tolerance", 1)
    run("financial_rigor", "verify-market-cap", "--price", PRICE, "--shares", SHARES * 10**8,
        "--reported", D("1280.66") * 10**8, "--currency", "HKD")
    eps = PROFIT / SHARES / FX
    run("financial_rigor", "verify-valuation", "--price", PRICE, "--eps", eps,
        "--bvps", D("614.56106") / SHARES / FX, "--revenue-per-share", (PRODUCT + SERVICE) / SHARES / FX,
        "--fcf-per-share", D("81.85") / SHARES / FX, "--dividend", 0)
    run("financial_rigor", "three-scenario", "--price", PRICE, "--eps", eps, "--shares", SHARES,
        "--growth", ".18", ".10", "-.03", "--pe", 22, 17, 12, "--years", 3, "--currency", "HKD")
    run("terminal_value", "audit", "--currency", "CNY", "--r", RATE, "--roic", ROIC,
        "--g", "0,.02,.03", "--rf", ".01621", "--beta", "1", "--discrete-risks",
        "监管收紧:情景,集团费率上行:情景,重大医疗责任事件:未建模")
    print("股权市值/TTM利润/商品/服务:", MCAP, PROFIT, PRODUCT, SERVICE, flush=True)
    for growth, pe in [(D("-.03"),12),(D(".10"),17),(D(".18"),22)]:
        target = eps * (1 + growth) ** 3 * pe
        print(f"三年股价 {target:.2f}，今日按8%折回 {target / (1 + RATE)**3:.2f}")
    anchors = []
    for label, prob, prod, service, m5, m10, g in CASES:
        for years, margin in [(5, m5), (10, m10)]:
            revenue = PRODUCT * (1+D(prod))**years + SERVICE * (1+D(service))**years
            profit = revenue * D(margin)
            print(f"{label} {years}年 收入={revenue:.2f} 利润={profit:.2f}", flush=True)
        pe = exit_pe(float(ROIC), float(g), float(RATE))[0]
        run("terminal_value", "irr", "--profit", profit, "--mcap", MCAP, "--pe", pe, "--payout", 0)
        anchor_pe = exit_pe(float(ROIC), float(g), .10)[0]
        anchors.append(100 * irr_from_terminal(float(profit), float(MCAP), anchor_pe))
    for delta in [".02", ".01"]:
        run("terminal_value", "flip", "--name", "京东健康", "--r", RATE, "--delta", delta,
            "--currency", "CNY", "--rf", ".01621", "--g", "0,.02,.03", "--roic", ROIC, "--p", ".25,.55,.20",
            "--irr10=" + ",".join(map(str, anchors)), "--k", 0)
    for p in [D("0"), D(".5")]:
        print(f"反向估值 分配 {p:.0%}，隐含增长 {reverse_growth(p):.3%}")


if __name__ == "__main__":
    main()
