---
name: capital-allocation
description: "AI Berkshire skill: Capital Allocation: Cash or Portfolio Deployment. Source: skills/capital-allocation.md."
---

## Codex adapter note

This skill is generated from `skills/capital-allocation.md` so Claude Code and Codex users share one canonical workflow.

- Treat `$ARGUMENTS` as the user's request in the current Codex thread.
- When the source mentions Claude-only surfaces such as Task, Agent, WebSearch, Bash, Read, or Write, use the closest Codex capability available in this session: subagents when available, web search when needed, shell commands for local tools, and normal file edits for workspace files.
- Use shared project tools from `tools/` in this repository. Prefer running commands from the repository root with paths like `python3 tools/financial_rigor.py ...`; if the current thread starts outside the repo, locate the actual checkout path first instead of assuming a fixed home-directory path.
- Before starting research, run the `date` command to confirm today's date; treat it as the baseline for "latest" data and state the data cutoff date in the report header. Never assume the current date from training data.
- Preserve the research quality rules from `AGENTS.md`: cross-check financial data, use exact arithmetic tools for valuation/math, and clearly label uncertainty and source gaps.

# Capital Allocation: Cash or Portfolio Deployment

Use `$ARGUMENTS` to decide whether available capital should remain in cash or be allocated to one or more positions in an existing portfolio, and in what proportions.

The first valid option is always **keep the capital in cash**. Do not maximize yield, force deployment, or assume that investing 100% is desirable. This workflow supports research and decision discipline; it is not personalized investment advice or a guarantee of returns.

## Input

The minimal command is:

```text
/capital-allocation
```

Optional parameters:

```text
/capital-allocation --candidates "Itochu, Verizon, Coca-Cola"
/capital-allocation --mode income
/capital-allocation --external-capital 500
```

- `--candidates` limits the allocation universe to the comma-separated names, tickers, or `Cash` supplied.
- `--mode` accepts `long_term_growth`, `income`, or `balanced`; default: `balanced`.
- `--external-capital` is a new contribution not included in the portfolio report. Interpret it in the portfolio base currency unless the user explicitly states another currency.

Do not require the user to re-enter portfolio cash, weights, currency, or report path. Detect the latest `portfolio-review` automatically: prefer `reports/portfolio-latest.md` when it exists, otherwise find the most recent portfolio-review report in `reports/`. Extract its cash balance, portfolio value, position weights, target weights, limits, and base currency.

By default, the report's cash balance is the available capital and is already included in portfolio value. If `--external-capital` is supplied:

```text
available capital = reported portfolio cash + external capital
post-contribution portfolio value = reported portfolio value + external capital
```

Only ask for confirmation when:

- the user states a capital amount that differs from reported cash without using `--external-capital`;
- the user mentions an external contribution without a clear amount or currency;
- no usable portfolio-review can be found;
- the latest report is stale or does not expose cash, weights, portfolio value, or currency.

Do not invent missing prices, exchange rates, weights, dividends, yields, fees, tax treatment, target ranges, or report availability. Ask explicitly for missing decision-critical inputs. If they cannot be obtained after repository discovery, retain the capital in cash and list the exact missing evidence.

Treat the latest usable `portfolio-review` as the validated structural starting point. `portfolio-review` owns portfolio structure, concentration, factors, reductions, exits, holds, and overall portfolio health; `capital-allocation` answers only: **what is the best marginal use of the next available euro?** When that review concludes `NO IMMEDIATE TRADE REQUIRED` or an unambiguous localized equivalent, accept the current structure unless newer evidence explicitly invalidates it. Future cleanup work or descriptive observations are not immediate allocation blocks.

## Candidate Scope

If `--candidates` is provided, or the user names a candidate in a conversational reply, analyze only those named companies and `Cash`. Set the selection origin to `Explicit user choice`. Use every other holding solely for portfolio constraints; do not justify why it was excluded and do not assign it a status or rank.

If no candidate is explicit, derive the universe from the latest `portfolio-review` and set the selection origin to `Automatic`:

1. first include lines marked `Increase` or an unambiguous localized equivalent;
2. then include lines marked `Hold / Increase` or an unambiguous localized equivalent;
3. add existing positions whose thesis is intact, that may improve an underrepresented factor, whose current and plausible post-allocation weights are compatible, and that have no explicit `do not add`, reduction, exit, or portfolio-constraint block;
4. add companies with a documented trigger newer than the portfolio review;
5. always include `Cash` as an alternative;
6. treat included holdings as **candidates to evaluate**, never as candidates already approved to buy;
7. do not include the entire portfolio without applying these economic filters.

Before concluding that no candidate is economically relevant, scan report filenames and contents for newer `investment-checklist`, `thesis-tracker`, `earnings-review`, `investment-research`, or `investment-team` evidence. A documented trigger can add or accelerate a candidate, but absence of a trigger does not prevent evaluation of an economically relevant existing position. A recent file alone is not a trigger.

Eliminate a company from the eligible ranking when the portfolio review already proves that it is above its upper bound, would exceed the upper bound after buying one whole share, breaches a sector, factor, or income-pocket cap, or would breach minimum cash. A newer trigger never overrides these strategic constraints. Keep the company in the candidate-status table with principal status `BLOCK` and the exact constraint; any missing reports are secondary future work. Use a reliable dated price and exchange rate for the one-share test; if either is unavailable, do not invent the result. Do not return early merely because the portfolio review contains no `Increase` label; complete candidate discovery and marginal evaluation first.

## Repository Report Discovery

Before marking any report `missing`, search recursively from the repository root. Use the file capabilities available in the current client; with a shell, prefer:

```text
rg --files reports
rg -il --glob '*.md' '<candidate name or ticker>' reports
```

For each candidate:

1. build search keys from the supplied name, full legal name, ticker, portfolio label, known localized name, and obvious spelling variants;
2. compare case-insensitively after treating spaces, hyphens, underscores, punctuation, and corporate suffixes as non-distinguishing;
3. search paths first, then Markdown content for tickers or aliases not present in filenames;
4. include root-level reports and company subdirectories;
5. search for `portfolio-review`, `investment-research`, `investment-checklist`, `income-investment`, `thesis-tracker`, `quality-screen`, and, when present, `investment-team` and `earnings-review` evidence;
6. list every matched path before deciding what is missing;
7. if a short ticker or alias produces ambiguous matches, read the candidate headings and ask for confirmation rather than guessing.

Never claim that a report is absent merely because the user did not pass its path. A localized name cannot be inferred without a shared alias, ticker, portfolio label, or report content; mark such a match `ambiguous`, not `missing`, until checked.

## Position in the Workflow

Use prior work instead of reproducing it:

```text
portfolio-review
    ↓
investment-research
    ↓
income-investment, when relevant
    ↓
investment-checklist
    ↓
capital-allocation
    ↓
thesis-tracker after a purchase or reinforcement
```

| Need | Required source |
|---|---|
| Portfolio weights, cash target, concentration limits | `portfolio-review` |
| Business quality, moat, management, intrinsic value | `investment-research` |
| Dividend coverage, durability, debt and income role | `income-investment` when relevant |
| Pre-purchase quality, discipline and margin-of-safety gates | `investment-checklist` |
| Existing thesis health and red lines | `thesis-tracker` when required by the rules below |

Do not redo full fundamental research. Read the discovered reports, record their paths, dates and conclusions, detect conflicts or gaps, and distinguish missing documentation from a documented price or allocation block.

## Required Evidence by Candidate Type

For a new candidate, normally require current `investment-research`, `investment-checklist`, and portfolio context. Require `income-investment` only when the dividend is central to the thesis or role. Create `thesis-tracker` after a purchase; its absence alone does not block a new candidate.

For an existing position, recent research and checklist evidence may provisionally support a reinforcement decision. Require a current `thesis-tracker` after a new purchase, after a significant reinforcement, for a core position, or when the thesis is old, ambiguous, or disputed. Do not block a small allocation solely because no formal tracker exists yet.

For `income-satellite`, `cyclical-income`, high-yield, highly leveraged, or dividend-led candidates, require a current `income-investment` report. For other income candidates, mark it `not required` only when research and checklist evidence already cover dividend safety sufficiently.

## Freshness Rules

- `portfolio-review`: current only if it reflects the latest portfolio transaction and cash balance;
- price: current session or latest available market close, clearly timestamped;
- `investment-research`: remains usable until a major event, material thesis change, or excessive age makes its conclusions unreliable;
- `investment-checklist`: must be reconciled with the current price and its stated buy zone or valuation assumptions;
- `income-investment`: must incorporate the latest available results, dividend decision, debt and refinancing information;
- `thesis-tracker`: update after purchase, significant reinforcement, or a material fundamental change.

An existing but outdated document is `stale`, never `missing`. Display `STALE DATA`, state what must be refreshed, and do not silently reuse a stale price-sensitive conclusion.

## Documented Allocation Triggers

The `portfolio-review` remains the primary strategic source, but it is not the only allocation trigger. Accept exactly these documented triggers:

1. the portfolio review explicitly recommends an increase;
2. a more recent `investment-checklist` explicitly concludes `BUY`, purchasable, or adequate margin of safety at the current price;
3. a reliable current price is at or below a buy zone recorded in an existing report;
4. a new or updated thesis explicitly documents a material structural improvement, durable quality gain, major debt reduction, or improved capital allocation;
5. a recent results report explicitly documents a material improvement in results, sustainable FCF, dividend growth, or balance-sheet quality.
6. another report newer than the portfolio review explicitly documents an actionable opportunity.

Compare report dates and select the first supported trigger in this priority order. Show the portfolio-review date, triggering-source date, selected source, and why it is primary or complementary. Prefer the portfolio-review trigger when it remains current; a newer trigger may complement it, add a candidate, or accelerate its review. Never infer a trigger from recency, create a buy zone, or treat a positive event as sufficient by itself: every candidate still passes thesis, quality, price, factor, post-allocation weight, cash, and decision-data gates. If sources conflict, retain the more conservative conclusion unless the newer report explicitly resolves the older blocker. Trigger Scan is not the sole entry mechanism for economically relevant existing positions.

## Decision Principles

Apply this priority order:

1. capital preservation;
2. business quality;
3. margin of safety;
4. marginal factor contribution;
5. consistency of post-allocation weight with portfolio limits;
6. long-term capital growth;
7. durable income;
8. dividend timing only as a secondary consideration.

Use Duan Yongping for business simplicity and excellence, Buffett for intrinsic value and margin of safety, Munger for inversion and vetoes, Li Lu for long-term economic certainty, and `income-investment` for dividend durability.

Dividend yield never compensates for a weak thesis, excessive debt, poor coverage, bad capital allocation, or insufficient margin of safety.

## Research and Calculation Discipline

1. Run `date` before any current-data research and put the data cutoff date in the report header.
2. Record the date of every price and source report. Flag stale data and explain its decision impact.
3. Separate **Verified fact**, **Estimate**, **Assumption**, and **Analytical judgment**.
4. Cross-check decision-critical financial data with at least two independent sources when new verification is needed.
5. Use `python3 tools/financial_rigor.py calc --expr '<expression>'` for capital, fees, income, cash and weight arithmetic. Use its valuation commands when valuation figures require verification.
6. Round proposed quantities down to whole shares unless the broker explicitly supports fractional shares and the user requests them.
7. Recalculate all final weights using the post-trade portfolio value and remaining cash. Include fees when known.
8. If no reliable price is available, do not calculate shares. Show `Not calculable`.
9. Avoid false precision: use ranges when inputs or intrinsic values are ranges.

## Roles and Sizing

Do not require an administrative role for every current position. Record a role only when it already exists in the evidence, when a candidate is genuinely evaluated for allocation and the role is decision-relevant, or when a role-specific constraint must be applied. Absence of a role alone never produces `NOT READY`, `BLOCK`, or an exit recommendation.

When a role is required, use exactly one of:

- `core-compounder`
- `core-income`
- `cyclical-income`
- `income-satellite`
- `opportunistic`
- `watchlist`
- `exit-candidate`
- `cash`

Apply portfolio-review limits first. Within those limits:

- core convictions may receive the largest weights only with a current, clear thesis and strong evidence;
- `core-income` must pass strict coverage, debt, durability, and valuation checks;
- `cyclical-income`, `income-satellite`, and `opportunistic` positions must remain smaller than core convictions;
- `watchlist`, `exit-candidate`, and positions without a clear thesis receive no new capital;
- high yield alone can never promote a position to a core role.

Current weight is descriptive, not a quality judgment. In particular, `position < 2%` is never an automatic classification, normalization, exit, or readiness gate. Treat small size only as a review signal. It becomes economically problematic only when supported by evidence such as an insufficient thesis, no realistic reinforcement path, redundant exposure, inadequate expected return, disproportionate monitoring cost, clearly superior alternatives, inability to become meaningful, or weak or deteriorating conviction. A 1% position may be eligible when its thesis, valuation, factor contribution, and post-allocation weight pass.

Separate the portfolio into:

- **Conviction pocket**: long-term capital growth and durable or growing dividends;
- **Income pocket**: higher current income used mainly for reinvestment, with a configurable aggregate cap, per-position cap, strict coverage test, debt monitoring, explicit exit rule, and smaller sizing than core convictions.

When the user permits some dividends to be consumed, separate projected reinvestable and consumable income and enforce the stated consumption maximum. Do not assume that any dividend will be consumed.

If an income-pocket cap or line cap is required but unavailable, do not allocate to that pocket.

## Evidence Extraction and Normalized Statuses

Read every matched report and extract explicit evidence when present:

- research verdict and business-quality conclusion;
- checklist verdict and failed gate;
- dated current price, buy zone, intrinsic-value range, and maximum price;
- `buy`, `hold`, `do not add`, `watch`, `avoid`, `reduce`, or `sell` conclusion;
- current weight, target range, portfolio role, and concentration limits;
- proposed amount, post-allocation weight, distance to the relevant bound, and sector and factor impact;
- main risks and invalidation conditions;
- dividend amount, yield, payout, FCF coverage, growth, debt, maturities, income-pocket cap, and exit rule.

Keep the source path and heading or short evidence excerpt for each extracted conclusion. If reports conflict, show the conflict and apply the more conservative conclusion until it is resolved.

Give every candidate one principal status, zero or more secondary statuses, and one next action. Determine the principal status in this order:

1. `BLOCK — <CONSTRAINT>` — post-allocation weight, whole-share sizing, sector, factor, income-pocket, fee, or minimum-cash constraints prevent allocation. Use exact reasons such as `BLOCK — FACTOR CONCENTRATION` or `BLOCK — MINIMUM CASH`. Missing reports are secondary future documentary work, never the principal blocker here.
2. `WAIT — PRICE` — price exceeds the buy zone or maximum price, margin of safety is inadequate, or the checklist fails on price.
3. `QUALITY BLOCK` — business quality, thesis, management, balance sheet, debt, dividend safety, or capital-allocation discipline fails.
4. `WAIT — TRIGGER` — quality, valuation, factor contribution, and sizing are acceptable, but a specific documented condition remains unmet.
5. `INSUFFICIENT DATA FOR THIS CANDIDATE` — genuinely required candidate-specific evidence remains absent after repository discovery. Name each missing item: research, checklist, income report, current price, current weight, target weight, or thesis. Exclude only this candidate and continue evaluating the others.
6. `ELIGIBLE` — thesis, business quality, valuation, marginal factor contribution, post-allocation weight, cash, debt, and applicable dividend requirements all pass, and expected attractiveness exceeds cash and alternatives.

Use `HOLD — DO NOT ADD` when an existing position is acceptable to retain but reports explicitly say hold or do not reinforce. `Keep small` alone is descriptive unless accompanied by an economic reason. Use `REDUCE / EXIT CANDIDATE` only when the review or research explicitly says reduce, exit, sell, thesis-invalid, or inferior on opportunity cost; missing role and sub-2% size are never sufficient reasons.

`HOLD CASH — NO ATTRACTIVE OPPORTUNITY` is a valid portfolio decision when decision data are sufficient but no `ELIGIBLE` candidate currently beats cash. A documented candidate can be a good business, a good dividend payer, or a reasonable existing holding without being eligible for reinforcement.

## Capital Deployment Status

Return exactly one portfolio-level decision after candidate evaluation:

- `DEPLOY`: at least one `ELIGIBLE` candidate is a better marginal use of capital than cash. Preserve one-position, multiple-position, and staged allocation as execution subtypes.
- `WAIT — PRICE`: the best otherwise eligible candidate is blocked only by valuation or margin of safety.
- `WAIT — TRIGGER`: the best otherwise eligible candidate awaits a specific documented condition.
- `BLOCK`: allocation is incompatible with post-allocation weight, sector, factor, concentration, minimum cash, income-pocket, or another portfolio constraint.
- `HOLD CASH — NO ATTRACTIVE OPPORTUNITY`: decision data are sufficient, but no candidate beats cash today.
- `NOT READY — INSUFFICIENT DECISION DATA`: missing or inconsistent global data prevent reliable comparison, such as absent price data for every viable candidate, incoherent portfolio value or weights, a portfolio review made stale by a major transaction, or portfolio constraints that cannot be calculated.

Candidate-specific missing data do not make the portfolio `NOT READY`; exclude that candidate and continue. Use portfolio-level `NOT READY — INSUFFICIENT DECISION DATA` only when the remaining evidence cannot support any reliable portfolio decision. Small positions, missing administrative roles, concentration that can be enforced as an allocation constraint, minimum cash that can be enforced, no attractive opportunity, and absence of an unlock condition do not by themselves mean `NOT READY`.

For `WAIT — PRICE`, `WAIT — TRIGGER`, `BLOCK`, and `NOT READY — INSUFFICIENT DECISION DATA`, produce short, measurable `Unlock Conditions` supported by existing evidence, such as a documented maximum price, named report refresh, specified result, weight threshold, or post-trade cash floor. Never invent one or use vague instructions such as “monitor the market.” When none exists, write exactly: `No documented unlock condition is currently available.`

## Execution Workflow

### A. Establish Portfolio Context and Cash

Calculate:

```text
post-trade cash = reported portfolio cash + external capital - proposed purchases - fees
post-trade portfolio value = reported portfolio value + external capital
post-trade cash weight = post-trade cash / post-trade portfolio value
```

Compare both with the cash target or minimum from `portfolio-review`. If a proposed allocation would breach the minimum, mark that candidate `BLOCK — MINIMUM CASH` and continue evaluating feasible alternatives.

### B. Select and Pre-filter Candidates

Apply explicit or automatic selection rules. In automatic mode, include economically relevant existing positions as well as newer documented triggers before deciding that no company merits evaluation. Then test allocation feasibility and record allocation failures as principal blockers.

### C. Discover and Read Candidate Evidence

For each in-scope candidate, search the latest portfolio review, investment checklist, investment research, income investment, thesis tracker, documented buy zones, earnings review, and investment team evidence. Read the matches, build both the evidence map and Trigger Scan, and label freshness before any missing-document or no-trigger conclusion. Mark a source `Searched: Yes` only after actually searching it.

### D. Evaluate the Marginal Euro

For each candidate, compare the portfolio-review date with the latest relevant evidence and name any selected trigger. No trigger does not prevent evaluation of an economically relevant existing position. Use this decision pipeline in order:

```text
Thesis intact?
    ↓
Business quality sufficient?
    ↓
Valuation and margin of safety acceptable?
    ↓
Marginal factor contribution useful?
    ↓
Post-allocation weight compatible?
    ↓
Expected attractiveness greater than cash and alternatives?
    ↓
DEPLOY / WAIT / BLOCK
```

For each candidate calculate with `financial_rigor.py` when applicable:

```text
gap = relevant target weight - current weight
post-allocation weight = (current position value + proposed amount) / post-contribution portfolio value
distance to bound = relevant upper bound - post-allocation weight
```

Show current weight, proposed amount, post-allocation weight, distance to the relevant bound, sector impact, and factor impact. Current weight alone is never a verdict. When the target is a range, do not automatically use its midpoint. Explain whether the proposed weight aims at the lower bound, midpoint, or upper bound based on evidence quality, conviction, cyclicality, downside risk, and portfolio concentration.

For `Marginal factor contribution`, state the currently overweight and underrepresented factors, the candidate's relevant exposures, and whether the proposed allocation improves, is neutral to, or worsens factor diversification. A good company at a good price is still `BLOCK — FACTOR CONCENTRATION` when its relevant factor is saturated. An underrepresented factor never overrides an inadequate price or weak thesis.

### E. Rank Eligible Uses of Capital

Rank only `ELIGIBLE` candidates. Compare each with every other eligible candidate and with holding cash. Evaluate:

- business quality and simplicity;
- long-term certainty;
- moat;
- management and capital allocation;
- valuation and margin of safety;
- balance sheet and permanent-loss risk;
- dividend contribution, coverage and growth;
- marginal factor contribution and diversification benefit;
- opportunity cost;
- final position size;
- transaction fees.

Do not collapse these dimensions into a mechanically precise numeric score. Rank by evidence-backed judgment after gates.

### F. Apply Inversion

For every proposed allocation answer:

> Why could this allocation be a mistake?

Give at least three distinct reasons, one order-cancellation signal, a maximum advisable price when supported by a current valuation report, and explicit wait conditions. If no defensible maximum price exists, show `Not calculable` and do not place the order.

### G. Select One Decision

Aggregate candidates using the six portfolio-level decisions defined above. Candidate-local insufficient data exclude only that candidate. If all viable candidates lack decision-critical evidence, use `NOT READY — INSUFFICIENT DECISION DATA`; otherwise decide from the candidates that can be evaluated. Never force allocation of all available capital. Compare the selected decision explicitly with retaining 100% in cash.

## Dividend Calendar Rules

When reliable data exist, use the dividend calendar only to estimate annual income, map payment months, identify months with no income, and show the projected income change.

State explicitly:

> Buying a company only to fill a month without dividends is prohibited if quality or valuation fails the filters.

A nearby ex-dividend date never justifies a rushed purchase and is not a free gain.

## Required Report Format

Save the report to `reports/capital-allocation-{YYYYMMDD}.md`. Use these headings exactly once:

## Capital Deployment Status

```text
Decision:
Capital Deployment Status: DEPLOY | WAIT — PRICE | WAIT — TRIGGER | BLOCK | HOLD CASH — NO ATTRACTIVE OPPORTUNITY | NOT READY — INSUFFICIENT DECISION DATA
Portfolio Health:
Active trigger:
Current action:
```

## Portfolio Readiness

```text
Portfolio health:
Investment discipline:
Cash availability:
Documentation quality:
Active opportunity:
```

Add a calm factual synthesis only when supported, such as `The portfolio is ready. The market is not yet offering a sufficiently attractive opportunity.` or `Waiting is an active decision, not an absence of decision.`

## Trigger Scan

| Source | Searched | Found | Date | Freshness | Trigger |
|---|---|---|---|---|---|

Include Portfolio Review, Investment Checklist, Investment Research, Income Investment, Thesis Tracker, Buy Zones, Earnings Review, and Investment Team. Use one row per candidate/source when needed. Show `Yes` only after a search, preserve unknown dates as unknown, and apply the existing freshness rules. Then show `Selected trigger`, triggering-source date, and `Selection reason`. If none is active, write: `No active trigger found after reviewing all available sources.`

For `WAIT — PRICE`, `WAIT — TRIGGER`, `BLOCK`, and `NOT READY — INSUFFICIENT DECISION DATA`, follow the scan with `## Unlock Conditions` and a short evidence-backed list. Omit that heading for `DEPLOY` and `HOLD CASH — NO ATTRACTIVE OPPORTUNITY` unless a concrete condition is already documented.

## 1. Executive decision

```text
Decision:
Existing cash:
External capital:
Total deployable cash:
Capital allocated:
Cash retained:
Confidence:
```

The external contribution is zero when absent. For example, `1,346.58 EUR + 200 EUR = 1,546.58 EUR` of total deployable cash. Also show the data cutoff date and constraints used: cash target, weights, sector/factor limits, income-pocket cap, fees, mode, assumptions, and stale-data warnings.

## 2. Candidate selection origin

Write `Mode: Automatic` or `Mode: Explicit user choice`.

## 3. Evidence map

| Candidate | Research | Checklist | Income | Thesis | Portfolio target |
|---|---|---|---|---|---|

Use only `Found`, `Missing`, `Not required`, or `Stale`, and list matched report paths directly below the table.

Then separate evidence work exactly as:

```text
Blocking evidence gaps:
- None

Documentation backlog:
- <useful but non-blocking work, or None>
```

Only evidence needed to decide the next euro belongs under `Blocking evidence gaps`. Candidate-specific gaps name the affected candidate and do not block the others. Tracker completion, administrative role assignment, and other useful cleanup belong under `Documentation backlog` unless a specific allocation constraint requires them.

## 4. Candidate status

| Candidate | Business quality | Valuation | Current weight | Proposed amount | Post-allocation weight | Marginal factor contribution | Principal status | Next action |
|---|---|---|---:|---:|---:|---|---|---|

## 5. Eligible candidate ranking

| Rank | Candidate | Proposed amount | Estimated quantity | Final weight | Reason |
|---:|---|---:|---:|---:|---|

Show only `ELIGIBLE` candidates. If none qualify, state the already-aggregated portfolio decision. Use the following only when decision data are sufficient and no candidate beats cash:

```text
No eligible candidates.
HOLD CASH — NO ATTRACTIVE OPPORTUNITY.
```

## 6. Documented but blocked candidates

| Candidate | Block type | Current conclusion | Unlock condition |
|---|---|---|---|

Include `WAIT — PRICE`, `WAIT — TRIGGER`, quality and allocation blocks, `HOLD — DO NOT ADD`, `REDUCE / EXIT CANDIDATE`, and `INSUFFICIENT DATA FOR THIS CANDIDATE`. When allocation is already impossible, list missing reports as `Future documentation work`, not as the primary refusal reason.

Add an `Income impact` subsection when at least one in-scope candidate is income-led. Extract available annual dividend, yield, payout, FCF coverage, debt, maturities, cut history, dividend growth, role, maximum weight, and exit rule. Show income before and after, incremental income, yield on allocated capital, dividend quality, payout safety, and income-pocket weight. Distinguish a sound dividend, a sound stock to reinforce, and a sound existing holding that should receive no new capital.

## 7. Cash comparison

Compare investing, retaining cash, and waiting for a stated price or trigger. Cash wins when margin of safety, allocation capacity, income safety, or opportunity cost is inadequate. Candidate-specific missing documentation removes that candidate from comparison; it does not automatically make cash win against every other candidate.

## 8. Execution plan

Only provide orders when allocation is selected. Give amount, whole-share estimate, indicative order type, price limit, non-execution conditions, and when to rerun `portfolio-review`. Order instructions are indicative, not guarantees.

Otherwise write:

```text
No order to place.
Re-run the skill when a documented unlock condition is met or material evidence changes.
```

## 9. Journal entry

| Date | Capital available | Decision | Allocation | Cash retained | Reports used | Main justification | Next step |
|---|---:|---|---|---:|---|---|---|

## 10. Next analyses

Repeat the `Blocking evidence gaps` and `Documentation backlog` distinction. List only genuinely missing or stale reports, and separately list `thesis-tracker` actions required after a purchase, significant reinforcement, core-position designation, or material thesis change.

End with a limitations statement and reminder that the report is decision support, not a return guarantee.

## Illustrative Output Example

```markdown
# Capital Allocation Report

## Capital Deployment Status
Decision: WAIT — PRICE
Capital Deployment Status: WAIT — PRICE
Portfolio Health: Healthy
Active trigger: None
Current action: Retain cash until a documented buy price is reached.

## Portfolio Readiness
Portfolio health: Healthy
Investment discipline: Maintained
Cash availability: Sufficient
Documentation quality: Good
Active opportunity: Candidates exist, but none offers adequate margin of safety.

The portfolio is ready. The market is not yet offering a sufficiently attractive opportunity.

## Trigger Scan
| Source | Searched | Found | Date | Freshness | Trigger |
|---|---|---|---|---|---|
| Portfolio Review | Yes | Yes | 2026-07-15 | Current | No increase |
| Investment Checklist | Yes | Yes | 2026-07-18 | Current | No BUY |
| Investment Research | Yes | Yes | 2026-07-07 | Current | No change |
| Income Investment | Yes | Yes | 2026-07-10 | Current | No income trigger |
| Thesis Tracker | Yes | No | Unknown | Unknown | None |
| Buy Zones | Yes | Yes | 2026-07-07 | Current | No zone reached |
| Earnings Review | Yes | No | Unknown | Unknown | None |
| Investment Team | Yes | No | Unknown | Unknown | None |

Selected trigger: None
No active trigger found after reviewing all available sources.

## Unlock Conditions
- Itochu at or below its documented maximum buy price.
- A newer Verizon checklist explicitly concludes BUY.

## 1. Executive decision
Decision: WAIT — PRICE
Existing cash: 1,346.58 EUR
External capital: 200.00 EUR
Total deployable cash: 1,546.58 EUR
Capital allocated: 0.00 EUR
Cash retained: 1,546.58 EUR
Confidence: High

## 8. Execution plan
No order to place.
Re-run the skill when a documented unlock condition is met or material evidence changes.
```

## Release Audit

After saving a real report:

```bash
python3 tools/report_audit.py extract --report reports/capital-allocation-{YYYYMMDD}.md
# Verify extracted items against reliable sources, then:
python3 tools/report_audit.py verdict --results '<verified JSON>' --report reports/capital-allocation-{YYYYMMDD}.md
```

Fix failed items and repeat the audit. Keep unresolved gaps visible and reduce confidence instead of filling them with assumptions.
