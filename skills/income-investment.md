# Income Investment: Durable and Opportunistic Distribution Analysis

Analyze `$ARGUMENTS` to answer:

> Can this company produce sufficiently durable and attractive distributable income to justify a portfolio role, either as a long-term income conviction or as an opportunistic yield position?

Never treat a high displayed yield as evidence of a good opportunity. This workflow is for learning and research, not personalized investment advice.

## Input

Use this command form:

```text
/income-investment "<company or ticker>" [mode=new|existing] [role=core-income|opportunistic-income|unspecified] [quantity=...] [cost_basis=...] [portfolio_weight=...] [target_yield=...] [tax_residence=...] [portfolio_file=...] [horizon=...]
```

The company or ticker is required. All other fields are optional. Accept equivalent natural-language input. Do not invent missing values: mark them `Unknown` or `Not calculable` and state the consequence. In particular, do not estimate net income without the tax residence, account type, applicable treaty, and confirmed withholding treatment.

## Related Workflows

Use or refer to existing workflows instead of reproducing them:

| Need | Workflow |
|---|---|
| Verified financial data and cross-source reconciliation | `financial-data` |
| Full general fundamental research | `investment-research` |
| Final pre-purchase decision | `investment-checklist` |
| Portfolio fit, concentration, and sizing | `portfolio-review` |
| Post-decision monitoring | `thesis-tracker` |
| Update after reported results | `earnings-review` |
| Rapid analysis of a discrete event | `news-pulse` |

`income-investment` owns the income-specific decision. It must not silently override a current `portfolio-review` conclusion.

## Research Discipline

1. Run `date` before research. Put the data cutoff date in the report header.
2. Prefer annual and interim reports, earnings releases, investor documents, regulatory filings, official releases, and official exchange data, in that order. Use secondary sources only to fill gaps and label them as secondary.
3. Apply `skills/financial-data.md`: verify decision-critical financial data with at least two independent sources when available and flag discrepancies above 1%.
4. Date or period-label every time-sensitive figure. Separate every material statement as **Verified fact**, **Estimate**, **Assumption**, or **Analytical judgment**.
5. Use `python3 tools/financial_rigor.py` for exact payout, yield, valuation, market-cap, portfolio-income, and scenario arithmetic. Never rely on mental arithmetic for a decision-sensitive result.
6. After saving the report, run the `tools/report_audit.py extract` and `verdict` workflow. A report that fails audit is a draft, not publishable research.

## Execution Workflow

### 1. Parse the Request and Establish Data Quality

- Resolve the security, listing, currency, distribution currency, mode, desired role, and optional portfolio inputs.
- State which gross-income, net-income, yield-on-cost, portfolio contribution, and after-trade calculations are possible.
- Rate evidence quality `A` (complete primary material), `B` (partial primary material), or `C` (mostly secondary/incomplete). Materially insufficient fundamentals trigger the `INSUFFICIENT DATA` gate.

### 2. Understand the Distribution

Cover at least five years when available:

- frequency; ordinary, special, or variable status; payment currency;
- annual dividend per share and total distributions;
- counts of increases, holds, cuts, and suspensions;
- dividend CAGR, with the exact period and treatment of special dividends;
- indicative announcement, ex-dividend, record, and payment dates.

Explain that waiting for the ex-dividend date is not a free gain: the share price theoretically adjusts by the distribution. The calendar may inform execution timing, but must never justify buying a weak company or delaying a necessary sale.

### 3. Trace the Cash Available for Distribution

Analyze net-income payout, free-cash-flow payout, cash flow after necessary investment, cash-flow stability and quality, interest coverage, net debt, debt maturities, refinancing needs, maintenance and growth capex, relevant off-balance-sheet commitments, and buybacks competing with dividends.

Do not mechanically apply an EPS payout ratio across sectors:

| Sector | Required sector measures |
|---|---|
| REIT / SIIC | FFO, AFFO, occupancy, LTV |
| Bank | CET1, distributable earnings, regulatory constraints |
| Insurer | Solvency and capital generation |
| BDC | NII, NAV, non-accruals |
| Resources | Mid-cycle cash flow and variable-distribution policy |
| Telecom / utility | Capex, debt, and FCF coverage |

### 4. Test Quality and Durability

Assess the business model, moat, pricing power, cyclicality, rate/currency/commodity sensitivity, income predictability, capital allocation, management quality, and the ability to maintain the distribution in a downside case. Distinguish accounting profit from repeatable distributable cash.

### 5. Value the Income Stream

Analyze current yield, historical average yield, appropriate sector multiples, FCF yield, a reasonable intrinsic-value range, margin of safety, and combined price-decline/dividend-cut scenarios. Yield on cost is retrospective information only and never a reason to keep a position.

### 6. Calculate Usable Income

Only when inputs support it, calculate annual gross dividend, gross dividend per payment frequency, known source withholding, estimated net income, contribution to portfolio income, and annual income after the proposed trade. If tax or account information is incomplete, show gross income and explain exactly why net income is not calculable. Label treaty rates and tax treatments with jurisdiction, account assumptions, and effective date.

### 7. Check Portfolio Fit

If a portfolio is provided:

- determine current and proposed weight;
- examine sector and geographic concentration, duplicated risks, and income dependence on one industry;
- distinguish capital diversification from dividend diversification;
- read the latest relevant `portfolio-review` report when available.

If conclusions diverge, show both conclusions, explain why, and separate company quality from allocation fit. A sound income security may still merit `HOLD – DO NOT ADD`, `REDUCE`, or `WATCHLIST` because of portfolio concentration.

When data permit, show expected gross income by month. Never recommend an inferior company to fill an empty month; quarterly payers can be combined to create monthly cash flow without requiring monthly payers.

### 8. Build Three Scenarios

Provide base, adverse, and severe cases. Each must state operating assumptions, distributable cash flow, payout coverage, balance-sheet/refinancing effect, dividend outcome, and valuation implication. The adverse and severe cases must explicitly test a dividend cut rather than assuming the dividend is fixed.

## Classification, Gates, and Verdict

First classify the income profile:

- **Conviction + durable income**: quality business, sustainable and potentially growing dividend, plausible long holding period.
- **Opportunistic income**: temporary yield or discount with explicit entry, monitoring, holding-period, and exit rules.
- **Yield trap**: recurring lack of coverage, incompatible leverage/investment needs, structural decline, or yield driven mainly by a falling price.
- **Unsuitable for income**: no meaningful distribution, marginal yield, insufficient evidence, or shareholder returns primarily delivered another way.

Use this qualitative scorecard; do not calculate a numeric average:

| Dimension | Rating (`Strong`, `Adequate`, `Weak`, `Critical`, `Unknown`) | Evidence |
|---|---|---|
| Business quality | | |
| Cash-flow visibility | | |
| Dividend coverage | | |
| Balance-sheet strength | | |
| Distribution history | | |
| Dividend growth potential | | |
| Valuation | | |
| Cyclicality | | |
| Cut risk | | |
| Portfolio fit | | |

Check these blocking gates before the verdict:

- recurring uncovered distribution;
- critical debt or refinancing risk;
- structural business deterioration;
- insufficient fundamental data;
- material governance or integrity concern.

A failed safety, debt, deterioration, or integrity gate overrides the scorecard and normally requires `REJECT / YIELD TRAP` (or `REDUCE` for an existing position when immediate disposal cannot be concluded from available portfolio facts). The insufficient-data gate requires `INSUFFICIENT DATA`. Do not use a score to offset a failed gate.

Return exactly one verdict:

- `CORE INCOME`
- `OPPORTUNISTIC INCOME`
- `WATCHLIST`
- `HOLD – DO NOT ADD`
- `REDUCE`
- `REJECT / YIELD TRAP`
- `INSUFFICIENT DATA`

For the verdict provide: possible portfolio role, primary reason, primary risk, entry conditions, a position-size range to study (never universally suitable), reinforcement conditions, reduction/exit criteria, monitoring indicators, and confidence. Do not give a firm personalized recommendation when portfolio, tax, or risk-tolerance information is insufficient.

## Required Report Format

Use these headings exactly once and avoid repeating the same analysis:

1. Executive summary
2. Verdict and category
3. Possible portfolio role
4. Business and source of distributed cash
5. Dividend history and calendar
6. Distribution coverage and safety
7. Balance sheet and refinancing
8. Income growth
9. Valuation and margin of safety
10. Tax and currency
11. Portfolio fit
12. Scenarios: base, adverse, severe
13. Dividend-cut risks
14. Purchase or reinforcement conditions
15. Reduction or sale conditions
16. Monitoring table
17. One-sentence conclusion
18. Sources and data quality

Save the result to `reports/{company}-income-investment-{YYYYMMDD}.md`, using a filesystem-safe company identifier. Include the scorecard and blocking-gate result in section 2, the monthly income calendar in section 11 when calculable, and source title, issuer/publisher, publication date, accessed date, reporting period, URL, and primary/secondary label in section 18.

## Release Audit

```bash
python3 tools/report_audit.py extract --report reports/{company}-income-investment-{YYYYMMDD}.md
# Verify every extracted item against reliable sources, then:
python3 tools/report_audit.py verdict --results '<verified JSON>' --report {company}-income-investment-{YYYYMMDD}.md
```

Fix failed items and repeat the audit. Clearly retain unresolved gaps and lower confidence rather than filling them with assumptions.
