#!/usr/bin/env python3
"""Financial Rigor Toolkit for AI Berkshire.

Command-line tool for verifying financial data accuracy during investment research.
Automatically called by Claude Code Skills at critical validation checkpoints.

Zero external dependencies — uses only Python stdlib (decimal, json, math, argparse).
Requires Python >= 3.7.

Usage (called automatically by Skills, no manual execution needed):
    python3 tools/financial_rigor.py verify-market-cap --price 510 --shares 9.11e9 --reported 4.65e12 --currency HKD
    python3 tools/financial_rigor.py verify-valuation --price 510 --eps 23.5 --bvps 120 --fcf-per-share 18 --dividend 2.4
    python3 tools/financial_rigor.py cross-validate --field revenue --values '{"年报": 7518, "Yahoo": 7500, "StockAnalysis": 7520}' --unit 亿
    python3 tools/financial_rigor.py benford --values '[1234, 2345, 3456, ...]'
    python3 tools/financial_rigor.py calc --expr '510 * 9.11e9'
"""

import argparse
import ast
import json
import math
import re
import sys
from decimal import Decimal, Context, DecimalException, ROUND_HALF_EVEN, InvalidOperation

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
    """Format large numbers in human-readable form (亿/万亿/B/T)."""
    v = exact(d)
    abs_v = abs(v)
    if unit in ("亿", "亿元", "亿港元", "亿美元"):
        if abs_v >= Decimal("10000"):
            return f"{_CTX.divide(v, Decimal('10000')):.2f}万亿{unit[1:] if len(unit) > 1 else ''}"
        return f"{v:.2f}{unit}"
    if abs_v >= Decimal("1e12"):
        return f"{_CTX.divide(v, Decimal('1e12')):.2f}T"
    if abs_v >= Decimal("1e9"):
        return f"{_CTX.divide(v, Decimal('1e9')):.2f}B"
    if abs_v >= Decimal("1e6"):
        return f"{_CTX.divide(v, Decimal('1e6')):.2f}M"
    return f"{v:,.2f}"


# ---------------------------------------------------------------------------
# 1. Market Cap Verification (股价×总股本 vs 报告市值)
# ---------------------------------------------------------------------------

def verify_market_cap(price, shares, reported_cap, currency=""):
    """Verify market cap = price × shares, compare with reported value."""
    p = exact(price)
    s = exact(shares)
    r = exact(reported_cap)

    calculated = _CTX.multiply(p, s)
    if r == 0:
        deviation = Decimal("0") if calculated == 0 else Decimal("Infinity")
    else:
        deviation = _CTX.multiply(
            _CTX.divide(abs(calculated - r), abs(r)), Decimal("100")
        )

    print("=" * 60)
    print("市值验算 (Market Cap Verification)")
    print("=" * 60)
    print(f"  股价 (Price):       {p} {currency}")
    print(f"  总股本 (Shares):    {fmt_number(s)}")
    print(f"  计算市值:           {fmt_number(calculated)} {currency}")
    print(f"  报告市值:           {fmt_number(r)} {currency}")
    print(f"  偏差:               {deviation:.2f}%")
    print()

    if deviation > 5:
        print(f"  ❌ 警告: 偏差 {deviation:.1f}% > 5%, 请检查:")
        print(f"     - 股本是否为最新（回购/增发）?")
        print(f"     - 单位是否一致（港币 vs 人民币 vs 美元）?")
        print(f"     - 股价是否为最新?")
        return False
    elif deviation > 1:
        print(f"  ⚠️  偏差 {deviation:.1f}% 在可接受范围, 可能因股价波动/股本变化")
        return True
    else:
        print(f"  ✅ 验证通过, 偏差仅 {deviation:.2f}%")
        return True


# ---------------------------------------------------------------------------
# 2. Valuation Metrics Verification (估值指标验算)
# ---------------------------------------------------------------------------

def verify_valuation(price, eps=None, bvps=None, fcf_per_share=None,
                     dividend=None, revenue_per_share=None):
    """Calculate and verify key valuation ratios from raw inputs."""
    p = exact(price)

    print("=" * 60)
    print("估值指标验算 (Valuation Verification)")
    print("=" * 60)
    print(f"  当前股价: {p}")
    print()

    if p == 0:
        print("  ❌ 当前股价不能为 0，无法计算收益率或估值倍数")
        return None

    results = {}

    if eps is not None:
        e = exact(eps)
        if e != 0:
            pe = _CTX.divide(p, e)
            print(f"  PE (TTM):  {p} / {e} = {pe:.2f}x")
            results["PE"] = float(pe)
            # Earnings yield
            ey = _CTX.divide(e, p) * 100
            print(f"  盈利收益率: {ey:.2f}%")
        else:
            print(f"  PE: EPS为0, 无法计算")

    if bvps is not None:
        b = exact(bvps)
        if b != 0:
            pb = _CTX.divide(p, b)
            print(f"  PB:        {p} / {b} = {pb:.2f}x")
            results["PB"] = float(pb)
            if eps is not None and exact(eps) != 0:
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
            print(f"  股息率:    {d} / {p} = {div_yield:.2f}%")
            results["Dividend_Yield"] = float(div_yield)

    if revenue_per_share is not None:
        r = exact(revenue_per_share)
        if r != 0:
            ps = _CTX.divide(p, r)
            print(f"  PS:        {p} / {r} = {ps:.2f}x")
            results["PS"] = float(ps)

    print()
    print("  ✅ 以上指标均使用精确十进制计算, 无浮点误差")
    return results


# ---------------------------------------------------------------------------
# 3. Cross-Source Data Validation (多源交叉验证)
# ---------------------------------------------------------------------------

def _pairwise_relative_difference_pct(left: Decimal, right: Decimal) -> Decimal:
    """Return symmetric relative difference using the smaller absolute value."""
    denominator = min(abs(left), abs(right))
    if denominator == 0:
        return Decimal("0") if left == right else Decimal("Infinity")
    return _CTX.multiply(
        _CTX.divide(abs(_CTX.subtract(left, right)), denominator),
        Decimal("100"),
    )


def cross_validate(field_name, source_values: dict, unit="", tolerance_pct=Decimal("1")):
    """Compare a data point across multiple sources, flag discrepancies."""
    print("=" * 60)
    print(f"交叉验证: {field_name} (Cross-Validation)")
    print("=" * 60)

    try:
        tolerance = exact(tolerance_pct)
    except (InvalidOperation, ValueError, TypeError):
        print(f"  ❌ 无效容差: {tolerance_pct}")
        return {"consensus": None, "all_consistent": False}

    if not tolerance.is_finite() or tolerance < 0:
        print(f"  ❌ 容差必须是有限的非负数: {tolerance_pct}")
        return {"consensus": None, "all_consistent": False}

    if not isinstance(source_values, dict) or len(source_values) < 2:
        source_count = len(source_values) if isinstance(source_values, dict) else 0
        print(f"  ❌ 至少需要 2 个独立来源，当前仅 {source_count} 个")
        return {"consensus": None, "all_consistent": False}

    if any(not str(source).strip() for source in source_values):
        print("  ❌ 每个来源都必须有非空名称")
        return {"consensus": None, "all_consistent": False}

    normalized_sources = {
        re.sub(r"\s+", " ", str(source)).strip().casefold()
        for source in source_values
    }
    if len(normalized_sources) < 2:
        print("  ❌ 至少需要 2 个名称不同的独立来源")
        return {"consensus": None, "all_consistent": False}

    try:
        values = {str(k): exact(v) for k, v in source_values.items()}
    except (InvalidOperation, ValueError, TypeError) as exc:
        print(f"  ❌ 来源数据不是有效数字: {exc}")
        return {"consensus": None, "all_consistent": False}

    if any(not value.is_finite() for value in values.values()):
        print("  ❌ 来源数据必须是有限数字")
        return {"consensus": None, "all_consistent": False}

    sources = list(values.keys())
    nums = list(values.values())

    # Find median as reference
    sorted_vals = sorted(nums)
    n = len(sorted_vals)
    median = (
        sorted_vals[n // 2]
        if n % 2 == 1
        else _CTX.divide(
            _CTX.add(sorted_vals[n // 2 - 1], sorted_vals[n // 2]),
            Decimal("2"),
        )
    )

    print(f"  数据来源数: {len(sources)}")
    print(f"  参考中位数: {fmt_number(median)} {unit}")
    print()

    # Keep the median as a descriptive consensus, but never use it as the
    # acceptance reference. Comparing each source only with the midpoint can
    # let two values nearly 2% apart pass a 1% tolerance.
    for src, val in values.items():
        if median == 0:
            dev = Decimal("0") if val == 0 else Decimal("Infinity")
        else:
            dev = _CTX.multiply(
                _CTX.divide(abs(val - median), abs(median)), Decimal("100")
            )
        print(
            f"  • {src:20s}: {fmt_number(val)} {unit}  "
            f"(距中位数 {dev:.2f}%)"
        )

    print()
    print("  来源两两相对差（以较小绝对值为分母）:")
    pairwise_results = []
    for left_index, left_source in enumerate(sources):
        for right_source in sources[left_index + 1:]:
            deviation = _pairwise_relative_difference_pct(
                values[left_source], values[right_source]
            )
            pairwise_results.append(deviation)
            status = "✅" if deviation <= tolerance else "❌"
            print(
                f"  {status} {left_source} ↔ {right_source}: "
                f"{deviation:.2f}%"
            )

    all_ok = all(deviation <= tolerance for deviation in pairwise_results)

    print()
    if all_ok:
        print(f"  ✅ 所有来源两两相对差 ≤ {tolerance}%, 数据一致")
    else:
        print(f"  ⚠️  存在来源组合的相对差 > {tolerance}%, 请核实差异原因")
        print(f"     建议: 优先采用公司年报/交易所数据")

    # Consensus value
    consensus = median
    print(f"\n  共识值 (中位数): {fmt_number(consensus)} {unit}")
    return {"consensus": consensus, "all_consistent": all_ok}


# ---------------------------------------------------------------------------
# 4. Benford's Law Quick Check (财务数据造假检测)
# ---------------------------------------------------------------------------

_BENFORD = {d: math.log10(1 + 1/d) for d in range(1, 10)}


def benford_check(values: list):
    """Quick Benford's Law check on a list of financial values."""
    print("=" * 60)
    print("Benford定律检测 (Financial Data Fabrication Check)")
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
        print(f"  ⚠️  样本量不足: {n} < 50, Benford分析不可靠")
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
        conformity = "Close (高度符合)"
    elif mad < 0.012:
        conformity = "Acceptable (可接受)"
    elif mad < 0.015:
        conformity = "Marginally Acceptable (边缘)"
    else:
        conformity = "Nonconforming (不符合 ⚠️)"

    print(f"  样本量:    {n}")
    print(f"  MAD:       {mad:.6f}")
    print(f"  Chi-sq:    {chi2:.2f}")
    print(f"  符合度:    {conformity}")
    print()

    # Digit distribution table
    print(f"  {'首位数':>6} {'观测':>8} {'Benford期望':>12} {'偏差':>8}")
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
        print("  ✅ 数据首位数字分布符合Benford定律")
    else:
        print("  ❌ 数据首位数字分布异常, 可能存在人为调整")
        print("     提示: 不符合Benford定律不一定是造假, 但值得进一步调查")

    return {"mad": mad, "chi2": chi2, "conformity": conformity, "is_conforming": is_ok}


# ---------------------------------------------------------------------------
# 5. Exact Calculator (精确计算器)
# ---------------------------------------------------------------------------

_DECIMAL_LITERAL_RE = re.compile(
    r"(?:[0-9]+(?:\.[0-9]*)?|\.[0-9]+)(?:[eE][+-]?[0-9]+)?\Z"
)
_DECIMAL_LITERAL_PREFIX_RE = re.compile(
    r"(?:[0-9]+(?:\.[0-9]*)?|\.[0-9]+)(?:[eE][+-]?[0-9]+)?"
)


def _numeric_token_at(source: str, node) -> str:
    """Read a numeric literal without relying on its float-valued AST payload."""
    lines = source.splitlines()
    if not getattr(node, "lineno", None) or node.lineno > len(lines):
        raise ValueError("数值位置无效")
    # The accepted expression alphabet is ASCII, so AST byte offsets and string
    # offsets are identical. This also works on Python 3.7, which lacks
    # ast.get_source_segment/end_col_offset.
    remainder = lines[node.lineno - 1][node.col_offset:]
    match = _DECIMAL_LITERAL_PREFIX_RE.match(remainder)
    if match is None:
        raise ValueError("仅可使用十进制数值")
    return match.group(0)


def _is_numeric_ast_node(node) -> bool:
    """Support both legacy ``Num`` and modern ``Constant`` AST nodes."""
    constant_type = getattr(ast, "Constant", None)
    if constant_type is not None and isinstance(node, constant_type):
        return True

    # ``Constant`` does not exist on Python 3.7, whose parser emits a concrete
    # ``Num`` node. Checking its type name avoids touching the deprecated
    # compatibility alias on newer Python versions.
    return type(node).__name__ == "Num"


def _eval_decimal_ast(node, source: str) -> Decimal:
    """Evaluate a parsed arithmetic AST using Decimal operations only."""
    if isinstance(node, ast.Expression):
        return _eval_decimal_ast(node.body, source)

    # Python 3.7 emits ``Num`` nodes; newer versions emit ``Constant``.
    if _is_numeric_ast_node(node):
        token = _numeric_token_at(source, node)
        if _DECIMAL_LITERAL_RE.fullmatch(token) is None:
            raise ValueError("仅可使用十进制数值")
        return Decimal(token)

    if isinstance(node, ast.UnaryOp) and isinstance(node.op, (ast.UAdd, ast.USub)):
        operand = _eval_decimal_ast(node.operand, source)
        return _CTX.plus(operand) if isinstance(node.op, ast.UAdd) else _CTX.minus(operand)

    if isinstance(node, ast.BinOp):
        left = _eval_decimal_ast(node.left, source)
        right = _eval_decimal_ast(node.right, source)
        if isinstance(node.op, ast.Add):
            return _CTX.add(left, right)
        if isinstance(node.op, ast.Sub):
            return _CTX.subtract(left, right)
        if isinstance(node.op, ast.Mult):
            return _CTX.multiply(left, right)
        if isinstance(node.op, ast.Div):
            return _CTX.divide(left, right)
        raise ValueError("仅可使用 +、-、*、/ 四则运算")

    raise ValueError("仅可使用数值、四则运算和括号")


def exact_calc(expr: str):
    """Evaluate a financial expression with exact decimal arithmetic.

    Supports: +, -, *, /, (), numbers (including scientific notation).
    """
    print("=" * 60)
    print("精确计算 (Exact Calculator)")
    print("=" * 60)

    if (
        not isinstance(expr, str)
        or not expr.strip()
        or len(expr) > 4096
        or re.fullmatch(r"[0-9.eE+\-*/()\s]+", expr) is None
    ):
        print(f"  ❌ 不安全的表达式: {expr}")
        return None

    try:
        tree = ast.parse(expr, mode="eval")
        if sum(1 for _ in ast.walk(tree)) > 512:
            raise ValueError("表达式过于复杂")
        d_result = _eval_decimal_ast(tree, expr)
        if not d_result.is_finite():
            raise ValueError("结果不是有限数字")
        print(f"  表达式: {expr}")
        print(f"  结果:   {fmt_number(d_result)}")
        print(f"  精确值: {d_result}")
        return d_result
    except (SyntaxError, ValueError, DecimalException) as e:
        print(f"  ❌ 计算错误: {e}")
        return None


# ---------------------------------------------------------------------------
# 6. Three-Scenario Valuation (三情景估值)
# ---------------------------------------------------------------------------

def three_scenario_valuation(current_price, current_eps, shares_billion,
                             growth_optimistic, growth_neutral, growth_pessimistic,
                             pe_optimistic, pe_neutral, pe_pessimistic,
                             years=3, currency=""):
    """Calculate three-scenario target prices with exact arithmetic."""
    print("=" * 60)
    print("三情景估值模型 (Three-Scenario Valuation)")
    print("=" * 60)

    p = exact(current_price)
    eps = exact(current_eps)
    shares = exact(shares_billion)

    if p == 0:
        print("  ❌ 当前股价不能为 0，无法计算目标价涨跌幅")
        return False
    if isinstance(years, bool) or not isinstance(years, int) or years < 0:
        print("  ❌ 预测期必须是非负整数")
        return False

    scenarios = [
        ("乐观 (Bull)", growth_optimistic, pe_optimistic),
        ("中性 (Base)", growth_neutral, pe_neutral),
        ("悲观 (Bear)", growth_pessimistic, pe_pessimistic),
    ]

    print(f"  当前股价: {p} {currency}")
    print(f"  当前EPS:  {eps}")
    print(f"  预测期:   {years}年")
    print()
    print(f"  {'情景':12} {'年增速':>8} {'目标PE':>8} {'目标EPS':>10} {'目标股价':>10} {'涨跌幅':>8}")
    print(f"  {'-'*12} {'-'*8} {'-'*8} {'-'*10} {'-'*10} {'-'*8}")

    for name, growth, pe in scenarios:
        g = exact(growth)
        target_pe = exact(pe)
        # Future EPS = current EPS × (1 + growth)^years
        future_eps = eps
        for _ in range(years):
            future_eps = _CTX.multiply(future_eps, _CTX.add(Decimal("1"), g))
        target_price = _CTX.multiply(future_eps, target_pe)
        change = _CTX.multiply(
            _CTX.divide(_CTX.subtract(target_price, p), p), Decimal("100")
        )
        growth_pct = _CTX.multiply(g, Decimal("100"))

        print(f"  {name:12} {growth_pct:>7.0f}% {target_pe:>7.0f}x "
              f"{future_eps:>10.2f} {target_price:>9.1f} {change:>+7.1f}%")

    print()
    print("  ✅ 所有计算使用精确十进制, 结果可审计复现")
    return True


# ---------------------------------------------------------------------------
# CLI Entry Point
# ---------------------------------------------------------------------------

def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Financial Rigor Toolkit — 金融数据严谨性验证工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s verify-market-cap --price 510 --shares 9.11e9 --reported 4.65e12 --currency HKD
  %(prog)s verify-valuation --price 510 --eps 23.5 --bvps 120
  %(prog)s cross-validate --field revenue --values '{"年报": 7518, "Yahoo": 7500}' --unit 亿
  %(prog)s benford --values '[1234, 2345, 3456, ...]'
  %(prog)s calc --expr '510 * 9.11e9'
        """)

    sub = parser.add_subparsers(dest="command")

    # verify-market-cap
    mc = sub.add_parser("verify-market-cap", help="验算市值 = 股价 × 总股本")
    mc.add_argument("--price", required=True)
    mc.add_argument("--shares", required=True, help="总股本")
    mc.add_argument("--reported", required=True, help="报告市值")
    mc.add_argument("--currency", default="", help="币种")

    # verify-valuation
    val = sub.add_parser("verify-valuation", help="验算估值指标")
    val.add_argument("--price", required=True)
    val.add_argument("--eps", default=None)
    val.add_argument("--bvps", default=None, help="每股净资产")
    val.add_argument("--fcf-per-share", default=None)
    val.add_argument("--dividend", default=None, help="每股股息")
    val.add_argument("--revenue-per-share", default=None)

    # cross-validate
    cv = sub.add_parser("cross-validate", help="多源交叉验证")
    cv.add_argument("--field", required=True, help="数据字段名")
    cv.add_argument("--values", required=True, help="JSON: {来源: 数值}")
    cv.add_argument("--unit", default="")
    cv.add_argument("--tolerance", default="1", help="容差百分比，默认 1%")

    # benford
    bf = sub.add_parser("benford", help="Benford定律检测")
    bf.add_argument("--values", required=True, help="JSON数组")

    # calc
    ca = sub.add_parser("calc", help="精确计算")
    ca.add_argument("--expr", required=True, help="算术表达式")

    # three-scenario
    ts = sub.add_parser("three-scenario", help="三情景估值")
    ts.add_argument("--price", required=True)
    ts.add_argument("--eps", required=True)
    ts.add_argument("--shares", required=True, help="总股本(亿)")
    ts.add_argument("--growth", nargs=3, required=True,
                    help="三情景年增速 (乐观 中性 悲观), 如 0.15 0.08 0.0")
    ts.add_argument("--pe", nargs=3, required=True,
                    help="三情景目标PE, 如 25 20 15")
    ts.add_argument("--years", default="3")
    ts.add_argument("--currency", default="")

    args = parser.parse_args(argv)

    def decimal_arg(value, option):
        if value is None:
            return None
        try:
            parsed = exact(value)
        except (InvalidOperation, ValueError, TypeError):
            parser.error(f"{option} 必须是有效数字: {value}")
        if not parsed.is_finite():
            parser.error(f"{option} 必须是有限数字: {value}")
        return parsed

    def integer_arg(value, option):
        parsed = decimal_arg(value, option)
        if parsed != parsed.to_integral_value():
            parser.error(f"{option} 必须是整数: {value}")
        return int(parsed)

    if args.command == "verify-market-cap":
        passed = verify_market_cap(
            decimal_arg(args.price, "--price"),
            decimal_arg(args.shares, "--shares"),
            decimal_arg(args.reported, "--reported"),
            args.currency,
        )
        return 0 if passed else 1
    elif args.command == "verify-valuation":
        outcome = verify_valuation(
            decimal_arg(args.price, "--price"),
            decimal_arg(args.eps, "--eps"),
            decimal_arg(args.bvps, "--bvps"),
            decimal_arg(args.fcf_per_share, "--fcf-per-share"),
            decimal_arg(args.dividend, "--dividend"),
            decimal_arg(args.revenue_per_share, "--revenue-per-share"),
        )
        return 0 if outcome is not None else 1
    elif args.command == "cross-validate":
        try:
            values = json.loads(
                args.values, parse_float=Decimal, parse_int=Decimal
            )
        except (json.JSONDecodeError, InvalidOperation) as exc:
            parser.error(f"--values JSON 解析失败: {exc}")
        if not isinstance(values, dict):
            parser.error("--values 必须是 JSON 对象: {来源: 数值}")
        outcome = cross_validate(
            args.field,
            values,
            args.unit,
            decimal_arg(args.tolerance, "--tolerance"),
        )
        return 0 if outcome["all_consistent"] else 1
    elif args.command == "benford":
        try:
            values = json.loads(
                args.values, parse_float=Decimal, parse_int=Decimal
            )
        except (json.JSONDecodeError, InvalidOperation) as exc:
            parser.error(f"--values JSON 解析失败: {exc}")
        if not isinstance(values, list):
            parser.error("--values 必须是 JSON 数组")
        benford_check(values)
        return 0
    elif args.command == "calc":
        return 0 if exact_calc(args.expr) is not None else 1
    elif args.command == "three-scenario":
        outcome = three_scenario_valuation(
            decimal_arg(args.price, "--price"),
            decimal_arg(args.eps, "--eps"),
            decimal_arg(args.shares, "--shares"),
            decimal_arg(args.growth[0], "--growth"),
            decimal_arg(args.growth[1], "--growth"),
            decimal_arg(args.growth[2], "--growth"),
            decimal_arg(args.pe[0], "--pe"),
            decimal_arg(args.pe[1], "--pe"),
            decimal_arg(args.pe[2], "--pe"),
            integer_arg(args.years, "--years"), args.currency)
        return 0 if outcome else 1
    else:
        parser.print_help()
        return 0


if __name__ == "__main__":
    try:
        exit_code = main()
    except DecimalException as exc:
        print(f"❌ 十进制计算失败: {exc}", file=sys.stderr)
        exit_code = 1
    sys.exit(exit_code)
