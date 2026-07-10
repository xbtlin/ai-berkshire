---
name: thesis-drift
description: "AI Berkshire skill: Investment paper drift detection: distinguishing factual changes from wording changes. Source: skills/thesis-drift.md."
---

## Codex adapter note

This skill is generated from `skills/thesis-drift.md` so Claude Code and Codex users share one canonical workflow.

- Treat `$ARGUMENTS` as the user's request in the current Codex thread.
- When the source mentions Claude-only surfaces such as Task, Agent, WebSearch, Bash, Read, or Write, use the closest Codex capability available in this session: subagents when available, web search when needed, shell commands for local tools, and normal file edits for workspace files.
- Use shared project tools from `tools/` in this repository. Prefer running commands from the repository root with paths like `python3 tools/financial_rigor.py ...`; if the current thread starts outside the repo, locate the actual checkout path first instead of assuming a fixed home-directory path.
- Before starting research, run the `date` command to confirm today's date; treat it as the baseline for "latest" data and state the data cutoff date in the report header. Never assume the current date from training data.
- Preserve the research quality rules from `AGENTS.md`: cross-check financial data, use exact arithmetic tools for valuation/math, and clearly label uncertainty and source gaps.

# Investment paper drift detection: distinguishing factual changes from wording changes

Perform investment thesis drift detection on $ARGUMENTS.

**Supported input formats**:
- `Company Name Old Report Path New Report Path` — Specify two research reports or paper snapshots for comparison
- `Company name reports/{Company name}-thesis-old date.md reports/{Company name}-thesis-new date.md` — Compare two dated paper snapshots
- `Company Name` — Automatically search for `reports/{Company Name}-thesis.md` and historical snapshots in the same directory; if there is no baseline, transfer to missing baseline processing

> "When the facts change, I change my mind. What about you?" - Keynes
>
> "Stock price fluctuations are not thesis drift, the facts have changed." —— AI Berkshire

## Design concept

The hardest thing about holding a long-term position is not reading the news every day, but distinguishing three things:
- **CHANGE OF FACTS**: Verifiable changes in revenue, margins, competitive landscape, management behavior, capital allocation
- **Price Change**: Market sentiment or valuation multiples change, but the business itself remains unchanged
- **Wording change**: The two reports express themselves differently, but the underlying evidence and judgment remain the same.

The goal of investing in paper drift detection is to: **Acknowledge paper changes only when the evidence changes**. You cannot create a drift just because the report is written differently, nor can you misjudge fundamentals just because the stock price rises or falls.

This Skill relies on the structured dimensions output by `/thesis-tracker`: core assumptions list, red line list, valuation anchors, and tracking record table. When there are no such structures, first fill in the baseline and then do drift detection.

## Execution process

### Step 1: Determine the operating mode

Parse `$ARGUMENTS`:
- If two report paths are provided → enter **specified report comparison** mode
- If only the company name is provided → Search `reports/{company name}-thesis.md` and historical snapshots, enter the **automatic snapshot comparison** mode
- If only one report is found or no historical baseline → Enter **Missing Baseline Handling** mode
- If the two reports are not from the same company → stop and ask the user to confirm, without making cross-company drift judgments

---

## Mode A: Specify report comparison

### A1: Read and verify two reports

Read old reports and new reports, extract:
- Report date, company name, stock code
- Core thesis (5 sentences)
- List of core assumptions
- Red line list
- Valuation anchor
- Tracking record sheet
- Management quality judgment
- Competitive moat judgment
- Current recommended actions (buy/hold/observe/reduce position/clear position)

If the report lacks key structures, first mark it as "missing structure", but still try to extract evidence from the text; mark the dimensions that cannot be extracted as "unable to judge" and do not make up conclusions.

### A2: Evidence normalization

Organize the factual evidence from the two reports into the same table:

| Dimensions | Old report evidence | New report evidence | Data source | Is it verifiable |
|------|-----------|-----------|---------|-----------|
| Valuation Anchor | | | | |
| Core Assumptions | | | | |
| red line | | | | |
| Management Quality | | | | |
| Competitive moat | | | | |

**Only compare evidence, not style of writing. ** If the old and new reports are only synonymous rewrites, sorting changes, and tone changes, but there are no changes in factual data and judgment thresholds, it is determined to be Unchanged.

### A3: Value and valuation verification

All numerical changes must be accurately calculated using `tools/financial_rigor.py`, LLM mental arithmetic is prohibited:

```bash
python3 tools/financial_rigor.py verify-valuation \
  --price {current price} \
  --eps {EPS} \
  --bvps {net assets per share} \
  --fcf-per-share {free cash flow per share}
```

To calculate market cap, percentage change, price target differential, or scenario valuation, use:

```bash
python3 tools/financial_rigor.py verify-market-cap --price {price} --shares {share capital} --reported {reported market capitalization} --currency {currency}
python3 tools/financial_rigor.py cross-validate --field {field} --values '{JSON}' --unit {unit}
python3 tools/financial_rigor.py three-scenario --price {price} --eps {EPS} --shares {equity billions} --growth {optimistic} {neutral} {pessimistic} --pe {optimistic PE} {neutral PE} {pessimistic PE}
python3 tools/financial_rigor.py calc --expr '{Exact calculation formula}'
```

Key financial data must be cross-verified by at least two independent sources. Figures with insufficient sources, inconsistent caliber, and unverifiable figures must be marked as "low confidence/pending verification".

### A4: Determine drift dimension by dimension

Use the following dimensions permanently and do not increase or decrease them temporarily:

| Dimensions | Determination focus | Improved | Unchanged | Weakened |
|------|---------|----------|-----------|----------|
| Valuation anchor point | Intrinsic value, PE/PB/FCF Yield, safety margin, target price range | The safety margin expands or the intrinsic value is revised upward and is verified by tools | There is no substantial change in the valuation range and safety margin | The safety margin narrows, the intrinsic value is revised downward, or the valuation assumption is invalid |
| List of core assumptions | Verifiable assumptions such as revenue growth, profit margin, cash flow, users/orders/capacity, etc. | More assumptions are strengthened by new evidence | The status of the assumptions is basically consistent with the evidence | The margins of the assumptions are weakened, damaged or broken |
| Red line list | Integrity, supervision, business decline, competition breakthrough, abnormal management actions | The original red line risk is lifted or significantly reduced | Not triggered and the risk level remains unchanged | The red line is triggered or the probability of triggering increases |
| Management quality | Integrity, capital allocation, repurchase dividends, execution, shareholder friendliness | New behaviors improve trust | Behaviors that continue old judgments | Behaviors that damage trust or worsen capital allocation |
| Competitive moat | Market share, pricing power, network effect, cost advantage, threat of substitution | The moat widens or the competitive advantage is verified | There is no substantial change in the pattern | The moat is weakened or the competition breaks through |

Only three types of conclusions can be given for each dimension: **Improved/Unchanged/Weakened**.

### A5: Evidence-driven rules

Each non-Unchanged conclusion must cite specific new evidence that led to the change:
- Financial report line items: such as revenue growth, gross profit margin, operating cash flow, repurchase amount, net cash
- Regulatory disclosures: such as 10-K/20-F, annual report, interim report, Hong Kong Stock Exchange announcement, SEC filing
- News events: such as management changes, regulatory penalties, major customer losses, competitive product breakthroughs
- Price and valuation: It must be stated whether this is a "change in valuation" or a "change in fundamentals" and cannot be confused.

If no evidence can be found to explain the change, it must be judged as **Unchanged** or **Unable to determine**, and the wording difference cannot be used to infer drift.

### A6: Output drift report

#### Report structure

```
1. Comparison objects and time span
2. Overall conclusion: Does the paper drift?
3. Dimension drift table
4. Details of evidence differences
5. Valuation and Numerical Calculation
6. Suggested action migration
7. Uncertain items and sources that need to be supplemented
8. Focus on tracking next time
```

#### Dimension drift table

| Dimensions | Old judgment | New judgment | Drift direction | Trigger evidence | Confidence |
|------|-------|-------|:--------:|---------|:------:|
| Valuation Anchors | | | Improved / Unchanged / Weakened | | High/Medium/Low |
| List of Core Assumptions | | | Improved / Unchanged / Weakened | | High/Medium/Low |
| Redline List | | | Improved / Unchanged / Weakened | | High/Medium/Low |
| Management Quality | | | Improved / Unchanged / Weakened | | High/Medium/Low |
| Competitive Moat | | | Improved / Unchanged / Weakened | | High/Medium/Low |

Write `—` as the triggering evidence for the **Unchanged line. Do not make up evidence just to fill in the form. **

#### The overall conclusion must be answered

1. **Does the paper drift? ** No drift / Positive drift / Negative drift / Insufficient evidence to judge
2. **Where does the drift come from? ** Valuation/Fundamentals/Management/Competitive Landscape/Red Line Events
3. **Is it a change in facts or a change in price? **Clear disassembly instructions
4. **How to migrate the recommended actions? ** For example: Watch → Buy, Buy → Hold, Hold → Reduce, Reduce → Exit
5. **What evidence is needed for the next step? ** Next financial report/Regulatory disclosures/Management notes/Competitive data

---

## Mode B: Automatic snapshot comparison

### B1: Find Snapshot

Look in `reports/` for:
- `reports/{company name}-thesis.md`
- `reports/{company name}-thesis-*.md`
- The `reports/{company name}/` directory contains reports of `thesis`, `thesis`, and `tracking`

Select the oldest file with complete structure as the old report, and the latest file as the new report. If the user specifies the date, the date specified by the user shall prevail.

### B2: Prevent wrong pairing

Before comparison, you must confirm:
- The company name or stock code is the same
- Different reporting dates
- Both reports contain extractable thesis structure or research conclusions

If the same company cannot be confirmed, stop and ask the user for a clear path.

### B3: Execution mode A

After finding two valid snapshots, execute mode A completely.

---

## Mode C: Missing baseline processing

If only one report is found or no old snapshots are found:

1. Clarification: **Lack of comparable historical baseline, drift detection cannot be performed**
2. Do not rewrite old papers based on memory or market impressions
3. Guide users to first use `/thesis-tracker {company name} to create a paper` to establish a structured baseline
4. If the current report is complete enough, it is recommended to save it as `reports/{company name}-thesis.md` as a baseline for future drift detection

Output format:

```
Unable to perform paper drift detection: missing historical baseline.

Found:
- Current report: {path/not found}
- Historical baseline: not found

Suggestions:
1. First run /thesis-tracker {company name} to create the paper
2. Next time there is a new financial report or major event, run /thesis-drift {company name} old report new report
```

---

## Key Principles

- **Evidence takes precedence over wording** — Synonymous rewriting is not drift, only changes in factual evidence are drift
- **Fundamentals take priority over stock price** — The rise and fall of stock price only affect the valuation anchor point and do not automatically change the quality of business.
- **Values must be verified** — All percentages, valuation multiples, and target price differences must be calculated using `tools/financial_rigor.py`
- **If you are not sure, mark it as uncertain** — When the source is missing, the caliber is inconsistent, and it is impossible to review, do not make a hard judgment.
- **Red lines are treated separately** — The red line triggering priority is cheaper than the valuation and cannot be masked by low PE
- **Output must be replayable** — Each Improved / Weakened conclusion must be traceable to specific evidence
