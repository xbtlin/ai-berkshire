#!/usr/bin/env python3
"""Deterministic calculations used in bank earnings analysis.

All rates passed to public functions are percentages, not decimals. Monetary
amounts must use one consistent unit. Functions return Decimal values so that
published tables do not inherit binary floating-point drift.
"""

from __future__ import annotations

from decimal import Decimal, InvalidOperation
from typing import Iterable, Mapping


ZERO = Decimal("0")
HUNDRED = Decimal("100")
TWELVE = Decimal("12")


def decimal(value: object) -> Decimal:
    if isinstance(value, Decimal):
        return value
    try:
        return Decimal(str(value).replace(",", "").strip())
    except (InvalidOperation, AttributeError) as exc:
        raise ValueError(f"invalid numeric value: {value!r}") from exc


def require_nonzero(value: Decimal, label: str) -> None:
    if value == ZERO:
        raise ValueError(f"{label} must not be zero")


def growth_rate(current: object, prior: object) -> Decimal:
    current_d, prior_d = decimal(current), decimal(prior)
    require_nonzero(prior_d, "prior")
    return (current_d / prior_d - Decimal("1")) * HUNDRED


def average_balance(opening: object, closing: object) -> Decimal:
    return (decimal(opening) + decimal(closing)) / Decimal("2")


def single_period_from_cumulative(current_cumulative: object, prior_cumulative: object) -> Decimal:
    return decimal(current_cumulative) - decimal(prior_cumulative)


def incremental_average_from_cumulative(
    current_cumulative_average: object,
    current_months: object,
    prior_cumulative_average: object,
    prior_months: object,
) -> Decimal:
    """Recover the average balance for the incremental period.

    A cumulative average is time-weighted. For example, Q4 average balance is
    (FY average * 12 - 9M average * 9) / 3, not FY average minus 9M average.
    """

    current_m, prior_m = decimal(current_months), decimal(prior_months)
    incremental_m = current_m - prior_m
    if current_m <= prior_m or prior_m < ZERO:
        raise ValueError("months must satisfy current_months > prior_months >= 0")
    return (
        decimal(current_cumulative_average) * current_m
        - decimal(prior_cumulative_average) * prior_m
    ) / incremental_m


def annualize(amount: object, months: object) -> Decimal:
    months_d = decimal(months)
    require_nonzero(months_d, "months")
    return decimal(amount) * TWELVE / months_d


def nii_from_average_earning_assets(
    average_earning_assets: object, nim_pct: object, months: object
) -> Decimal:
    return decimal(average_earning_assets) * decimal(nim_pct) / HUNDRED * decimal(months) / TWELVE


def infer_average_earning_assets(nii: object, nim_pct: object, months: object) -> Decimal:
    nim_d = decimal(nim_pct)
    require_nonzero(nim_d, "nim_pct")
    return annualize(nii, months) / (nim_d / HUNDRED)


def infer_annualized_nim(nii: object, average_earning_assets: object, months: object) -> Decimal:
    assets_d = decimal(average_earning_assets)
    require_nonzero(assets_d, "average_earning_assets")
    return annualize(nii, months) / assets_d * HUNDRED


def rounded_value_bounds(value: object, decimal_places: int = 2) -> tuple[Decimal, Decimal]:
    """Return the half-unit interval implied by a rounded disclosed value."""

    if decimal_places < 0:
        raise ValueError("decimal_places must be non-negative")
    half_unit = Decimal("0.5") * (Decimal("10") ** -decimal_places)
    value_d = decimal(value)
    return value_d - half_unit, value_d + half_unit


def effective_tax_rate(pre_tax_profit: object, net_profit: object) -> Decimal:
    pre_tax_d = decimal(pre_tax_profit)
    require_nonzero(pre_tax_d, "pre_tax_profit")
    return (Decimal("1") - decimal(net_profit) / pre_tax_d) * HUNDRED


def annualized_credit_cost(impairment: object, average_loans: object, months: object) -> Decimal:
    loans_d = decimal(average_loans)
    require_nonzero(loans_d, "average_loans")
    return annualize(impairment, months) / loans_d * HUNDRED


def annualized_rorwa(net_profit: object, average_rwa: object, months: object) -> Decimal:
    rwa_d = decimal(average_rwa)
    require_nonzero(rwa_d, "average_rwa")
    return annualize(net_profit, months) / rwa_d * HUNDRED


def risk_asset_generation_ratio(rwa: object, earning_assets: object) -> Decimal:
    earning_d = decimal(earning_assets)
    require_nonzero(earning_d, "earning_assets")
    return decimal(rwa) / earning_d * HUNDRED


def capital_required_for_rwa_growth(delta_rwa: object, target_core_tier1_pct: object) -> Decimal:
    return decimal(delta_rwa) * decimal(target_core_tier1_pct) / HUNDRED


def new_npl_balance(
    closing_npl: object,
    opening_npl: object,
    writeoffs_and_disposals: object = ZERO,
    acquisitions_and_transfers_in: object = ZERO,
) -> Decimal:
    """Approximate gross new NPL formation with an explicit bridge.

    new NPL = closing NPL - opening NPL + write-offs/disposals - transfers in.
    Pass only values supported by the report and label the result as an estimate
    whenever recoveries, upgrades, FX, or consolidation changes are unavailable.
    """

    return (
        decimal(closing_npl)
        - decimal(opening_npl)
        + decimal(writeoffs_and_disposals)
        - decimal(acquisitions_and_transfers_in)
    )


def balance_sheet_mix(
    current_components: Mapping[str, object],
    prior_components: Mapping[str, object],
    current_total: object,
    prior_total: object,
) -> dict[str, dict[str, Decimal | None]]:
    """Calculate balance-sheet mix and contribution to total growth.

    Component keys must match so a missing disclosure is not silently treated as
    zero. Contribution is None when the total balance did not change.
    """

    if set(current_components) != set(prior_components):
        raise ValueError("current and prior component keys must match")
    current_total_d, prior_total_d = decimal(current_total), decimal(prior_total)
    require_nonzero(current_total_d, "current_total")
    require_nonzero(prior_total_d, "prior_total")
    delta_total = current_total_d - prior_total_d
    result: dict[str, dict[str, Decimal | None]] = {}
    for name in current_components:
        current_d = decimal(current_components[name])
        prior_d = decimal(prior_components[name])
        current_share = current_d / current_total_d * HUNDRED
        prior_share = prior_d / prior_total_d * HUNDRED
        delta = current_d - prior_d
        result[name] = {
            "current": current_d,
            "prior": prior_d,
            "change": delta,
            "current_share_pct": current_share,
            "prior_share_pct": prior_share,
            "share_change_pp": current_share - prior_share,
            "contribution_to_total_change_pct": (
                None if delta_total == ZERO else delta / delta_total * HUNDRED
            ),
        }
    return result


def npl_stock_bridge(
    opening_npl: object,
    new_npl: object,
    transfers_in: object = ZERO,
    cash_recoveries: object = ZERO,
    writeoffs: object = ZERO,
    bulk_transfers_and_abs: object = ZERO,
    upgrades: object = ZERO,
    other_disposals: object = ZERO,
    fx_and_other: object = ZERO,
    reported_closing_npl: object | None = None,
) -> dict[str, Decimal | None]:
    """Reconcile opening NPL, formation, disposals, and reported closing NPL."""

    calculated_closing = (
        decimal(opening_npl)
        + decimal(new_npl)
        + decimal(transfers_in)
        - decimal(cash_recoveries)
        - decimal(writeoffs)
        - decimal(bulk_transfers_and_abs)
        - decimal(upgrades)
        - decimal(other_disposals)
        + decimal(fx_and_other)
    )
    reported = None if reported_closing_npl is None else decimal(reported_closing_npl)
    residual = None if reported is None else reported - calculated_closing
    return {
        "calculated_closing_npl": calculated_closing,
        "reported_closing_npl": reported,
        "residual": residual,
    }


def provision_rollforward(
    opening_provision: object,
    loan_impairment_charge: object,
    recoveries_of_written_off_loans: object = ZERO,
    transfers_in_fx_and_other: object = ZERO,
    writeoffs_and_transfers_out: object = ZERO,
    reported_closing_provision: object | None = None,
) -> dict[str, Decimal | None]:
    """Reconcile the loan-loss provision balance."""

    calculated_closing = (
        decimal(opening_provision)
        + decimal(loan_impairment_charge)
        + decimal(recoveries_of_written_off_loans)
        + decimal(transfers_in_fx_and_other)
        - decimal(writeoffs_and_transfers_out)
    )
    reported = (
        None if reported_closing_provision is None else decimal(reported_closing_provision)
    )
    residual = None if reported is None else reported - calculated_closing
    return {
        "calculated_closing_provision": calculated_closing,
        "reported_closing_provision": reported,
        "residual": residual,
    }


def _validated_range(low: object, high: object, label: str) -> tuple[Decimal, Decimal]:
    low_d, high_d = decimal(low), decimal(high)
    if low_d > high_d:
        raise ValueError(f"{label} low must not exceed high")
    return low_d, high_d


def estimate_writeoff_range(
    opening_provision: object,
    closing_provision: object,
    impairment_low: object,
    impairment_high: object,
    recovery_low: object = ZERO,
    recovery_high: object = ZERO,
    other_net_inflow_low: object = ZERO,
    other_net_inflow_high: object = ZERO,
) -> dict[str, Decimal]:
    """Estimate write-offs/transfers from a provision roll-forward interval."""

    impairment = _validated_range(impairment_low, impairment_high, "impairment")
    recovery = _validated_range(recovery_low, recovery_high, "recovery")
    other = _validated_range(other_net_inflow_low, other_net_inflow_high, "other_net_inflow")
    opening_d, closing_d = decimal(opening_provision), decimal(closing_provision)
    low = opening_d + impairment[0] + recovery[0] + other[0] - closing_d
    high = opening_d + impairment[1] + recovery[1] + other[1] - closing_d
    return {"low": low, "midpoint": (low + high) / Decimal("2"), "high": high}


def npl_generation_proxy(
    closing_npl: object,
    opening_npl: object,
    writeoffs_and_transfers_low: object,
    writeoffs_and_transfers_high: object,
    transfers_in_low: object = ZERO,
    transfers_in_high: object = ZERO,
) -> dict[str, Decimal]:
    """Return a non-negative proxy interval for gross new NPL formation.

    The proxy adds disclosed/estimated write-offs and transfers out to the NPL
    balance change, then subtracts known transfers in. It omits cash recovery,
    upgrades, bulk sales and other disposals, so it is a lower-bound proxy only
    when transfers in and consolidation effects are captured separately.
    """

    writeoff = _validated_range(
        writeoffs_and_transfers_low,
        writeoffs_and_transfers_high,
        "writeoffs_and_transfers",
    )
    transfers_in = _validated_range(transfers_in_low, transfers_in_high, "transfers_in")
    delta_npl = decimal(closing_npl) - decimal(opening_npl)
    raw_low = delta_npl + writeoff[0] - transfers_in[1]
    raw_high = delta_npl + writeoff[1] - transfers_in[0]
    low = max(ZERO, raw_low)
    high = max(low, raw_high)
    return {
        "low": low,
        "midpoint": (low + high) / Decimal("2"),
        "high": high,
        "raw_low": raw_low,
        "raw_high": raw_high,
    }


def confidence_grade(
    source_status: str,
    assumption_count: int = 0,
    residual: object = ZERO,
    reference_amount: object = Decimal("1"),
    residual_limit_pct: object = Decimal("5"),
) -> str:
    """Assign A/B/C/D/N/A using source type, assumptions, and bridge residual."""

    status = source_status.strip().lower()
    if status in {"n/a", "na", "unavailable"}:
        return "N/A"
    if status == "disclosed":
        return "A"
    if assumption_count < 0:
        raise ValueError("assumption_count must be non-negative")
    reference_d = abs(decimal(reference_amount))
    residual_d = abs(decimal(residual))
    if reference_d == ZERO:
        residual_ratio = ZERO if residual_d == ZERO else Decimal("Infinity")
    else:
        residual_ratio = residual_d / reference_d * HUNDRED
    limit = decimal(residual_limit_pct)
    if status == "calculated":
        return "B" if assumption_count == 0 and residual_ratio <= limit else "D"
    if status == "estimated":
        return "C" if assumption_count <= 2 and residual_ratio <= limit else "D"
    if status in {"proxy", "inferred"}:
        return "D"
    raise ValueError(f"unknown source_status: {source_status!r}")


def fundamental_scorecard(
    items: Mapping[str, Mapping[str, object]],
    uncertain_weight_limit: object = Decimal("20"),
) -> dict[str, object]:
    """Aggregate a transparent 100-point bank fundamental scorecard.

    Each item requires weight, confidence, and raw_score from 0 to 5. raw_score
    may be None only for N/A. C/D/N/A items widen the score range. A single
    score is suppressed when uncertain weight exceeds the limit or any item is
    missing a raw score. A provisional range is publishable only when N/A
    weight is at most 50 and the range width is at most 40 points.
    """

    total_weight = sum((decimal(item["weight"]) for item in items.values()), ZERO)
    if total_weight != HUNDRED:
        raise ValueError("scorecard weights must sum to 100")
    uncertain_weight = ZERO
    na_weight = ZERO
    base_total = ZERO
    lower_total = ZERO
    upper_total = ZERO
    has_missing = False
    breakdown: dict[str, dict[str, object]] = {}
    for name, item in items.items():
        weight = decimal(item["weight"])
        confidence = str(item["confidence"]).upper()
        if confidence not in {"A", "B", "C", "D", "N/A"}:
            raise ValueError(f"invalid confidence for {name}: {confidence}")
        raw_value = item.get("raw_score")
        if confidence in {"C", "D", "N/A"}:
            uncertain_weight += weight
        if confidence == "N/A":
            na_weight += weight
        if raw_value is None:
            if confidence != "N/A":
                raise ValueError(f"raw_score may be None only for N/A: {name}")
            has_missing = True
            base_points = None
            lower_points = ZERO
            upper_points = weight
        else:
            raw = decimal(raw_value)
            if not ZERO <= raw <= Decimal("5"):
                raise ValueError(f"raw_score must be between 0 and 5: {name}")
            base_points = raw / Decimal("5") * weight
            base_total += base_points
            uncertainty_steps = {
                "A": ZERO,
                "B": ZERO,
                "C": Decimal("1"),
                "D": Decimal("2"),
                "N/A": Decimal("5"),
            }[confidence]
            lower_raw = max(ZERO, raw - uncertainty_steps)
            upper_raw = min(Decimal("5"), raw + uncertainty_steps)
            lower_points = lower_raw / Decimal("5") * weight
            upper_points = upper_raw / Decimal("5") * weight
        lower_total += lower_points
        upper_total += upper_points
        breakdown[name] = {
            "weight": weight,
            "confidence": confidence,
            "raw_score": raw_value,
            "weighted_points": base_points,
            "lower_points": lower_points,
            "upper_points": upper_points,
        }
    provisional = has_missing or uncertain_weight > decimal(uncertain_weight_limit)
    score_range = (lower_total, upper_total)
    range_width = upper_total - lower_total
    publishable = not (na_weight > Decimal("50") or range_width > Decimal("40"))
    return {
        "score": None if provisional else base_total,
        "score_range": score_range,
        "published_score_range": score_range if provisional and publishable else None,
        "uncertain_weight": uncertain_weight,
        "na_weight": na_weight,
        "range_width": range_width,
        "provisional": provisional,
        "publishable": publishable,
        "breakdown": breakdown,
    }


def scenario_midpoint(low: object, high: object) -> Decimal:
    low_d, high_d = decimal(low), decimal(high)
    if low_d > high_d:
        raise ValueError("scenario low must not exceed high")
    return (low_d + high_d) / Decimal("2")


def validate_interval(center: object, low: object, high: object) -> list[str]:
    center_d, low_d, high_d = decimal(center), decimal(low), decimal(high)
    errors: list[str] = []
    if low_d > high_d:
        errors.append("lower boundary exceeds upper boundary")
    if not low_d <= center_d <= high_d:
        errors.append("center lies outside interval")
    return errors


def reconcile_components(total: object, components: Iterable[object]) -> Decimal:
    """Return total minus component sum; a clean reconciliation returns zero."""

    return decimal(total) - sum((decimal(value) for value in components), ZERO)


def bank_profit_bridge(
    net_interest_income: object,
    fee_income: object,
    other_noninterest_income: object,
    taxes_and_surcharges: object,
    administrative_expense: object,
    credit_impairment: object,
    other_asset_impairment: object,
    other_business_cost: object,
    net_nonoperating_income: object,
    income_tax: object,
    minority_interest: object,
) -> dict[str, Decimal]:
    """Calculate a complete bank profit bridge.

    Pass expenses and losses as positive amounts. Pass reversals/recoveries as
    negative amounts. Minority interest follows the income statement sign, so
    a negative minority loss increases attributable profit.
    """

    revenue = sum(
        map(decimal, (net_interest_income, fee_income, other_noninterest_income)), ZERO
    )
    pre_tax_profit = (
        revenue
        - decimal(taxes_and_surcharges)
        - decimal(administrative_expense)
        - decimal(credit_impairment)
        - decimal(other_asset_impairment)
        - decimal(other_business_cost)
        + decimal(net_nonoperating_income)
    )
    net_profit = pre_tax_profit - decimal(income_tax)
    attributable_profit = net_profit - decimal(minority_interest)
    return {
        "revenue": revenue,
        "pre_tax_profit": pre_tax_profit,
        "net_profit": net_profit,
        "attributable_profit": attributable_profit,
    }
