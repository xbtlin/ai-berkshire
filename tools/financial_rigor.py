#!/usr/bin/env python3
"""Financial Rigor Toolkit for AI Berkshire.

Command-line tool for verifying financial data accuracy during investment research.
Automatically called by Claude Code Skills at critical validation checkpoints.

Zero external dependencies — uses only Python stdlib (decimal, json, math, argparse).
Requires Python >= 3.7.

Usage (called automatically by Skills, no manual execution needed):
    python3 tools/financial_rigor.py verify-market-cap --price 510 --shares 9.11e9 --reported 4.65e12 --currency HKD
    python3 tools/financial_rigor.py verify-valuation --price 510 --eps 23.5 --bvps 120 --fcf-per-share 18 --dividend 2.4
    python3 tools/financial_rigor.py cross-validate --field revenue --values '{"\u5e74\u62a5": 7518, "Yahoo": 7500, "StockAnalysis": 7520}' --unit \u4ebf
    python3 tools/financial_rigor.py benford --values '[1234, 2345, 3456, ...]'
    python3 tools/financial_rigor.py calc --expr '510 * 9.11e9'
"""

import argparse
import json
import math
import sys
from decimal import Decimal, Context, ROUND_HALF_EVEN, InvalidOperation

# ---------------------------------------------------------------------------
# Exact Decimal Engine (no floating-point drift)
# ---------------------------------------------------------------------------

_CTX = Context(prec=28, rounding=ROUND_HALF_EVEN)


def exact(value) -> Decimal:
    """Convert any numeric to exact Decimal, avoiding float traps."""
    if isinstance(value, Decimal):
        return value
    if isinstance(value, float):
        return Decimal(str(value))
    return Decimal(str(value))


def fmt_number(d: Decimal, unit: str = "") -> str:
    """Format large numbers in human-readable form (\u4ebf/\u4e07\u4ebf/B/T)."""
    v = float(d)
    abs_v = abs(v)
    if unit in ("\u4ebf", "\u4ebf\u5143", "\u4ebf\u6e2f\u5143", "\u4ebf\u7f8e\u5143"):
        if abs_v >= 10000:
            return f"{v/10000:.2f}\u4e07\u4ebf{unit[1:] if len(unit) > 1 else ''}"
        return f"{v:.2f}{unit}"
    if abs_v >= 1e12:
        return f"{v/1e12:.2f}T"
    if abs_v >= 1e9:
        return f"{v/1e9:.2f}B"
    if abs_v >= 1e6:
        return f"{v/1e6:.2f}M"
    return f"{v:,.2f}"


# ---------------------------------------------------------------------------
# 1. Market Cap Verification (\u80a1\u4ef7×\u603b\u80a1\u672c vs \u62a5\u544a\u5e02\u503c)
# ---------------------------------------------------------------------------

def verify_market_cap(price, shares, reported_cap, currency=""):
    """Verify market cap = price × shares, compare with reported value."""
    p = exact(price)
    s = exact(shares)
    r = exact(reported_cap)

    calculated = _CTX.multiply(p, s)
    deviation = abs(float(calculated - r) / float(r)) * 100 if r != 0 else 0

    print("=" * 60)
    print("\u5e02\u503c\u9a8c\u7b97 (Market Cap Verification)")
    print("=" * 60)
    print(f"  \u80a1\u4ef7 (Price):       {p} {currency}")
    print(f"  \u603b\u80a1\u672c (Shares):    {fmt_number(s)}")
    print(f"  \u8ba1\u7b97\u5e02\u503c:           {fmt_number(calculated)} {currency}")
    print(f"  \u62a5\u544a\u5e02\u503c:           {fmt_number(r)} {currency}")
    print(f"  \u504f\u5dee:               {deviation:.2f}%")
    print()

    if deviation > 5:
        print(f"  ❌ \u8b66\u544a: \u504f\u5dee {deviation:.1f}% > 5%, \u8bf7\u68c0\u67e5:")
        print(f"     - \u80a1\u672c\u662f\u5426\u4e3a\u6700\u65b0（\u56de\u8d2d/\u589e\u53d1）?")
        print(f"     - \u5355\u4f4d\u662f\u5426\u4e00\u81f4（\u6e2f\u5e01 vs \u4eba\u6c11\u5e01 vs \u7f8e\u5143）?")
        print(f"     - \u80a1\u4ef7\u662f\u5426\u4e3a\u6700\u65b0?")
        return False
    elif deviation > 1:
        print(f"  ⚠️  \u504f\u5dee {deviation:.1f}% \u5728\u53ef\u63a5\u53d7\u8303\u56f4, \u53ef\u80fd\u56e0\u80a1\u4ef7\u6ce2\u52a8/\u80a1\u672c\u53d8\u5316")
        return True
    else:
        print(f"  ✅ \u9a8c\u8bc1\u901a\u8fc7, \u504f\u5dee\u4ec5 {deviation:.2f}%")
        return True


# ---------------------------------------------------------------------------
# 2. Valuation Metrics Verification (\u4f30\u503c\u6307\u6807\u9a8c\u7b97)
# ---------------------------------------------------------------------------

def verify_valuation(price, eps=None, bvps=None, fcf_per_share=None,
                     dividend=None, revenue_per_share=None):
    """Calculate and verify key valuation ratios from raw inputs."""
    p = exact(price)

    print("=" * 60)
    print("\u4f30\u503c\u6307\u6807\u9a8c\u7b97 (Valuation Verification)")
    print("=" * 60)
    print(f"  \u5f53\u524d\u80a1\u4ef7: {p}")
    print()

    results = {}

    if eps is not None:
        e = exact(eps)
        if e != 0:
            pe = _CTX.divide(p, e)
            print(f"  PE (TTM):  {p} / {e} = {pe:.2f}x")
            results["PE"] = float(pe)
            # Earnings yield
            ey = _CTX.divide(e, p) * 100
            print(f"  \u76c8\u5229\u6536\u76ca\u7387: {ey:.2f}%")
        else:
            print(f"  PE: EPS\u4e3a0, \u65e0\u6cd5\u8ba1\u7b97")

    if bvps is not None:
        b = exact(bvps)
        if b != 0:
            pb = _CTX.divide(p, b)
            print(f"  PB:        {p} / {b} = {pb:.2f}x")
            results["PB"] = float(pb)
            if eps is not None and float(exact(eps)) != 0:
                roe = _CTX.divide(exact(eps), b) * 100
                print(f"  ROE:       {exact(eps)} / {b} = {roe:.2f}%")
                results["ROE"] = float(roe)

    if fcf_per_share is not None:
        f = exact(fcf_per_share)
        if f != 0:
            fcf_yield = _CTX.divide(f, p) * 100
            pfcf = _CTX.divide(p, f)
            print(f"  P/FCF:     {p} / {f} = {pfcf:.2f}x")
            print(f"  FCF Yield: {fcf_yield:.2f}%")
            results["P_FCF"] = float(pfcf)
            results["FCF_Yield"] = float(fcf_yield)

    if dividend is not None:
        d = exact(dividend)
        if p != 0:
            div_yield = _CTX.divide(d, p) * 100
            print(f"  \u80a1\u606f\u7387:    {d} / {p} = {div_yield:.2f}%")
            results["Dividend_Yield"] = float(div_yield)

    if revenue_per_share is not None:
        r = exact(revenue_per_share)
        if r != 0:
            ps = _CTX.divide(p, r)
            print(f"  PS:        {p} / {r} = {ps:.2f}x")
            results["PS"] = float(ps)

    print()
    print("  ✅ \u4ee5\u4e0a\u6307\u6807\u5747\u4f7f\u7528\u7cbe\u786e\u5341\u8fdb\u5236\u8ba1\u7b97, \u65e0\u6d6e\u70b9\u8bef\u5dee")
    return results


# ---------------------------------------------------------------------------
# 3. Cross-Source Data Validation (\u591a\u6e90\u4ea4\u53c9\u9a8c\u8bc1)
# ---------------------------------------------------------------------------

def cross_validate(field_name, source_values: dict, unit="", tolerance_pct=2.0):
    """Compare a data point across multiple sources, flag discrepancies."""
    print("=" * 60)
    print(f"\u4ea4\u53c9\u9a8c\u8bc1: {field_name} (Cross-Validation)")
    print("=" * 60)

    values = {k: exact(v) for k, v in source_values.items()}
    sources = list(values.keys())
    nums = list(values.values())

    # Find median as reference
    sorted_vals = sorted(float(v) for v in nums)
    n = len(sorted_vals)
    median = sorted_vals[n // 2] if n % 2 == 1 else (sorted_vals[n//2-1] + sorted_vals[n//2]) / 2

    print(f"  \u6570\u636e\u6765\u6e90\u6570: {len(sources)}")
    print(f"  \u53c2\u8003\u4e2d\u4f4d\u6570: {fmt_number(exact(median))} {unit}")
    print()

    all_ok = True
    for src, val in values.items():
        dev = abs(float(val) - median) / median * 100 if median != 0 else 0
        status = "✅" if dev <= tolerance_pct else "❌"
        if dev > tolerance_pct:
            all_ok = False
        print(f"  {status} {src:20s}: {fmt_number(val)} {unit}  (\u504f\u5dee {dev:.2f}%)")

    print()
    if all_ok:
        print(f"  ✅ \u6240\u6709\u6765\u6e90\u504f\u5dee ≤ {tolerance_pct}%, \u6570\u636e\u4e00\u81f4")
    else:
        print(f"  ⚠️  \u5b58\u5728\u6765\u6e90\u504f\u5dee > {tolerance_pct}%, \u8bf7\u6838\u5b9e\u5dee\u5f02\u539f\u56e0")
        print(f"     \u5efa\u8bae: \u4f18\u5148\u91c7\u7528\u516c\u53f8\u5e74\u62a5/\u4ea4\u6613\u6240\u6570\u636e")

    # Consensus value
    consensus = median
    print(f"\n  \u5171\u8bc6\u503c (\u52a0\u6743\u4e2d\u4f4d\u6570): {fmt_number(exact(consensus))} {unit}")
    return {"consensus": consensus, "all_consistent": all_ok}


# ---------------------------------------------------------------------------
# 4. Benford's Law Quick Check (\u8d22\u52a1\u6570\u636e\u9020\u5047\u68c0\u6d4b)
# ---------------------------------------------------------------------------

_BENFORD = {d: math.log10(1 + 1/d) for d in range(1, 10)}


def benford_check(values: list):
    """Quick Benford's Law check on a list of financial values."""
    print("=" * 60)
    print("Benford\u5b9a\u5f8b\u68c0\u6d4b (Financial Data Fabrication Check)")
    print("=" * 60)

    # Extract leading digits
    digits = []
    for v in values:
        v = abs(float(v))
        if v > 0:
            sig = 10 ** (math.log10(v) - math.floor(math.log10(v)))
            d = int(sig)
            if 1 <= d <= 9:
                digits.append(d)

    n = len(digits)
    if n < 50:
        print(f"  ⚠️  \u6837\u672c\u91cf\u4e0d\u8db3: {n} < 50, Benford\u5206\u6790\u4e0d\u53ef\u9760")
        return None

    # Observed distribution
    counts = {}
    for d in digits:
        counts[d] = counts.get(d, 0) + 1
    observed = {d: counts.get(d, 0) / n for d in range(1, 10)}

    # MAD (Nigrini's Mean Absolute Deviation)
    mad = sum(abs(observed.get(d, 0) - _BENFORD[d]) for d in range(1, 10)) / 9

    # Chi-square
    chi2 = sum((counts.get(d, 0) - _BENFORD[d] * n) ** 2 / (_BENFORD[d] * n) for d in range(1, 10))

    # Conformity
    if mad < 0.006:
        conformity = "Close (\u9ad8\u5ea6\u7b26\u5408)"
    elif mad < 0.012:
        conformity = "Acceptable (\u53ef\u63a5\u53d7)"
    elif mad < 0.015:
        conformity = "Marginally Acceptable (\u8fb9\u7f18)"
    else:
        conformity = "Nonconforming (\u4e0d\u7b26\u5408 ⚠️)"

    print(f"  \u6837\u672c\u91cf:    {n}")
    print(f"  MAD:       {mad:.6f}")
    print(f"  Chi-sq:    {chi2:.2f}")
    print(f"  \u7b26\u5408\u5ea6:    {conformity}")
    print()

    # Digit distribution table
    print(f"  {'\u9996\u4f4d\u6570':>6} {'\u89c2\u6d4b':>8} {'Benford\u671f\u671b':>12} {'\u504f\u5dee':>8}")
    print(f"  {'-'*6} {'-'*8} {'-'*12} {'-'*8}")
    for d in range(1, 10):
        obs = observed.get(d, 0)
        exp = _BENFORD[d]
        dev = obs - exp
        flag = " ⚠️" if abs(dev) > 0.03 else ""
        print(f"  {d:>6d} {obs:>8.3f} {exp:>12.3f} {dev:>+8.3f}{flag}")

    print()
    is_ok = mad < 0.015
    if is_ok:
        print("  ✅ \u6570\u636e\u9996\u4f4d\u6570\u5b57\u5206\u5e03\u7b26\u5408Benford\u5b9a\u5f8b")
    else:
        print("  ❌ \u6570\u636e\u9996\u4f4d\u6570\u5b57\u5206\u5e03\u5f02\u5e38, \u53ef\u80fd\u5b58\u5728\u4eba\u4e3a\u8c03\u6574")
        print("     \u63d0\u793a: \u4e0d\u7b26\u5408Benford\u5b9a\u5f8b\u4e0d\u4e00\u5b9a\u662f\u9020\u5047, \u4f46\u503c\u5f97\u8fdb\u4e00\u6b65\u8c03\u67e5")

    return {"mad": mad, "chi2": chi2, "conformity": conformity, "is_conforming": is_ok}


# ---------------------------------------------------------------------------
# 5. Exact Calculator (\u7cbe\u786e\u8ba1\u7b97\u5668)
# ---------------------------------------------------------------------------

def exact_calc(expr: str):
    """Evaluate a financial expression with exact decimal arithmetic.

    Supports: +, -, *, /, (), numbers (including scientific notation).
    """
    print("=" * 60)
    print("\u7cbe\u786e\u8ba1\u7b97 (Exact Calculator)")
    print("=" * 60)

    # Safe evaluation: only allow numbers and arithmetic
    allowed = set("0123456789.+-*/() eE")
    if not all(c in allowed for c in expr.replace(" ", "")):
        print(f"  ❌ \u4e0d\u5b89\u5168\u7684\u8868\u8fbe\u5f0f: {expr}")
        return None

    try:
        # Replace scientific notation for Decimal compatibility
        result = eval(expr, {"__builtins__": {}}, {})
        d_result = exact(result)
        print(f"  \u8868\u8fbe\u5f0f: {expr}")
        print(f"  \u7ed3\u679c:   {fmt_number(d_result)}")
        print(f"  \u7cbe\u786e\u503c: {d_result}")
        return float(d_result)
    except Exception as e:
        print(f"  ❌ \u8ba1\u7b97\u9519\u8bef: {e}")
        return None


# ---------------------------------------------------------------------------
# 6. Three-Scenario Valuation (\u4e09\u60c5\u666f\u4f30\u503c)
# ---------------------------------------------------------------------------

def three_scenario_valuation(current_price, current_eps, shares_billion,
                             growth_optimistic, growth_neutral, growth_pessimistic,
                             pe_optimistic, pe_neutral, pe_pessimistic,
                             years=3, currency=""):
    """Calculate three-scenario target prices with exact arithmetic."""
    print("=" * 60)
    print("\u4e09\u60c5\u666f\u4f30\u503c\u6a21\u578b (Three-Scenario Valuation)")
    print("=" * 60)

    p = exact(current_price)
    eps = exact(current_eps)
    shares = exact(shares_billion)

    scenarios = [
        ("\u4e50\u89c2 (Bull)", growth_optimistic, pe_optimistic),
        ("\u4e2d\u6027 (Base)", growth_neutral, pe_neutral),
        ("\u60b2\u89c2 (Bear)", growth_pessimistic, pe_pessimistic),
    ]

    print(f"  \u5f53\u524d\u80a1\u4ef7: {p} {currency}")
    print(f"  \u5f53\u524dEPS:  {eps}")
    print(f"  \u9884\u6d4b\u671f:   {years}\u5e74")
    print()
    print(f"  {'\u60c5\u666f':12} {'\u5e74\u589e\u901f':>8} {'\u76ee\u6807PE':>8} {'\u76ee\u6807EPS':>10} {'\u76ee\u6807\u80a1\u4ef7':>10} {'\u6da8\u8dcc\u5e45':>8}")
    print(f"  {'-'*12} {'-'*8} {'-'*8} {'-'*10} {'-'*10} {'-'*8}")

    for name, growth, pe in scenarios:
        g = exact(growth)
        target_pe = exact(pe)
        # Future EPS = current EPS × (1 + growth)^years
        future_eps = eps
        for _ in range(years):
            future_eps = _CTX.multiply(future_eps, _CTX.add(Decimal("1"), g))
        target_price = _CTX.multiply(future_eps, target_pe)
        change = float(target_price - p) / float(p) * 100

        print(f"  {name:12} {float(g)*100:>7.0f}% {float(target_pe):>7.0f}x "
              f"{float(future_eps):>10.2f} {float(target_price):>9.1f} {change:>+7.1f}%")

    print()
    print("  ✅ \u6240\u6709\u8ba1\u7b97\u4f7f\u7528\u7cbe\u786e\u5341\u8fdb\u5236, \u7ed3\u679c\u53ef\u5ba1\u8ba1\u590d\u73b0")


# ---------------------------------------------------------------------------
# CLI Entry Point
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Financial Rigor Toolkit — \u91d1\u878d\u6570\u636e\u4e25\u8c28\u6027\u9a8c\u8bc1\u5de5\u5177",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s verify-market-cap --price 510 --shares 9.11e9 --reported 4.65e12 --currency HKD
  %(prog)s verify-valuation --price 510 --eps 23.5 --bvps 120
  %(prog)s cross-validate --field revenue --values '{"\u5e74\u62a5": 7518, "Yahoo": 7500}' --unit \u4ebf
  %(prog)s benford --values '[1234, 2345, 3456, ...]'
  %(prog)s calc --expr '510 * 9.11e9'
        """)

    sub = parser.add_subparsers(dest="command")

    # verify-market-cap
    mc = sub.add_parser("verify-market-cap", help="\u9a8c\u7b97\u5e02\u503c = \u80a1\u4ef7 × \u603b\u80a1\u672c")
    mc.add_argument("--price", type=float, required=True)
    mc.add_argument("--shares", type=float, required=True, help="\u603b\u80a1\u672c")
    mc.add_argument("--reported", type=float, required=True, help="\u62a5\u544a\u5e02\u503c")
    mc.add_argument("--currency", default="", help="\u5e01\u79cd")

    # verify-valuation
    val = sub.add_parser("verify-valuation", help="\u9a8c\u7b97\u4f30\u503c\u6307\u6807")
    val.add_argument("--price", type=float, required=True)
    val.add_argument("--eps", type=float, default=None)
    val.add_argument("--bvps", type=float, default=None, help="\u6bcf\u80a1\u51c0\u8d44\u4ea7")
    val.add_argument("--fcf-per-share", type=float, default=None)
    val.add_argument("--dividend", type=float, default=None, help="\u6bcf\u80a1\u80a1\u606f")
    val.add_argument("--revenue-per-share", type=float, default=None)

    # cross-validate
    cv = sub.add_parser("cross-validate", help="\u591a\u6e90\u4ea4\u53c9\u9a8c\u8bc1")
    cv.add_argument("--field", required=True, help="\u6570\u636e\u5b57\u6bb5\u540d")
    cv.add_argument("--values", required=True, help="JSON: {\u6765\u6e90: \u6570\u503c}")
    cv.add_argument("--unit", default="")
    cv.add_argument("--tolerance", type=float, default=2.0, help="\u5bb9\u5dee\u767e\u5206\u6bd4")

    # benford
    bf = sub.add_parser("benford", help="Benford\u5b9a\u5f8b\u68c0\u6d4b")
    bf.add_argument("--values", required=True, help="JSON\u6570\u7ec4")

    # calc
    ca = sub.add_parser("calc", help="\u7cbe\u786e\u8ba1\u7b97")
    ca.add_argument("--expr", required=True, help="\u7b97\u672f\u8868\u8fbe\u5f0f")

    # three-scenario
    ts = sub.add_parser("three-scenario", help="\u4e09\u60c5\u666f\u4f30\u503c")
    ts.add_argument("--price", type=float, required=True)
    ts.add_argument("--eps", type=float, required=True)
    ts.add_argument("--shares", type=float, required=True, help="\u603b\u80a1\u672c(\u4ebf)")
    ts.add_argument("--growth", nargs=3, type=float, required=True,
                    help="\u4e09\u60c5\u666f\u5e74\u589e\u901f (\u4e50\u89c2 \u4e2d\u6027 \u60b2\u89c2), \u5982 0.15 0.08 0.0")
    ts.add_argument("--pe", nargs=3, type=float, required=True,
                    help="\u4e09\u60c5\u666f\u76ee\u6807PE, \u5982 25 20 15")
    ts.add_argument("--years", type=int, default=3)
    ts.add_argument("--currency", default="")

    args = parser.parse_args()

    if args.command == "verify-market-cap":
        verify_market_cap(args.price, args.shares, args.reported, args.currency)
    elif args.command == "verify-valuation":
        verify_valuation(args.price, args.eps, args.bvps, args.fcf_per_share,
                        args.dividend, args.revenue_per_share)
    elif args.command == "cross-validate":
        values = json.loads(args.values)
        cross_validate(args.field, values, args.unit, args.tolerance)
    elif args.command == "benford":
        values = json.loads(args.values)
        benford_check(values)
    elif args.command == "calc":
        exact_calc(args.expr)
    elif args.command == "three-scenario":
        three_scenario_valuation(
            args.price, args.eps, args.shares,
            args.growth[0], args.growth[1], args.growth[2],
            args.pe[0], args.pe[1], args.pe[2],
            args.years, args.currency)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
