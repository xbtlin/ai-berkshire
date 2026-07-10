# Investment Thesis Tracking: A Discipline System After Buying

Performs an investment thesis tracking check on $ARGUMENTS.

**Supported input formats**:
- `Company Name` — Create an investment thesis when using it for the first time, and follow it up when using it later.
- `Company Name Create Thesis` — force re-creation of investment thesis
- `Company Name Quarterly Check` — paper check based on the latest financial reports

> "Buying is just the beginning. The real work is the continuous tracking during the holding period." —— Li Lu
>
> "When the facts change, I change my mind. What about you?" - Keynes

## Design concept

The process for most investors is: Research → Buy → Pray. The lack of systematic follow-up after purchase leads to:
- Reluctant to sell when it's time to sell ("If you wait a little longer, the price will rise again")
- Panic selling when you shouldn't sell ("It fell 20%, am I wrong?")
- Forgot why I bought it in the first place ("Why did I buy this?")

What Buffett and Li Lu do is: **write down the selling conditions before buying**. Then check the paper for completeness every quarter.

## Execution process

### Step 1: Determine the operating mode

Check whether the company’s investment thesis file (`reports/{company name}-thesis.md`) already exists:
- If not present → enter **Create Paper** mode
- If exists → enter **trace check** mode
- If it cannot be found but the user says it already exists → Ask for the file path

---

## Mode A: Building an Investment Thesis

### A0: Data collection

Use WebSearch to obtain the current stock price, valuation indicators (PE/PB/dividend rate), and the latest financial report core data to fill in the valuation anchor point. If the company's `/investment-research` or `/investment-team` report already exists, it will be read from it first.

Use `tools/financial_rigor.py verify-valuation` to verify valuation data.

### A1: Core paper (must be written clearly within 200 words)

The investment thesis must answer the following 5 questions, one sentence for each question:

```
I bought ___ company for ___ yuan because:
1. The essence of this business is ___, I understand how it makes money
2. Its moat is ___ and is getting wider/stable
3. Management ___ is trustworthy because ___
4. The current price is equivalent to ___ discount of intrinsic value, and the margin of safety comes from ___
5. Even if I’m wrong, downside risk is manageable because ___
```

**If the 5 sentences are incomplete, there is a problem with the paper itself - it means that the buying decision is not clear enough. **

### A2: List of Core Assumptions

Break down your investment thesis into specific, testable hypotheses:

| # | Core Assumptions | Verification Method | Verification Frequency | Current Status |
|---|---------|---------|---------|---------|
| 1 | Example: Revenue growth maintained at 15%+ | Quarterly revenue growth rate | Quarterly | 🟢 Established |
| 2 | Example: Gross profit margin is stable at 60%+ | Quarterly gross profit margin | Quarterly | 🟢 Established |
| 3 | Example: Management’s continuous buybacks | Buyback announcement/cash flow statement | Quarterly | 🟢 Establishment |
| 4 | Example: Competitor has not made a breakthrough | Industry data/competitor financial report | Every six months | 🟢 Established |
| 5 | ... | ... | ... | ... |

Usually 3-7 hypotheses. Too little means that the thinking is not deep enough, and too much means that the paper is not focused enough.

### A3: Red line list (any one triggered = must be re-evaluated)

| # | Redline condition | Severity | Post-trigger action |
|---|---------|---------|-----------|
| 1 | Example: Management integrity issues (financial fraud, related transactions) | Fatal | Clear positions immediately |
| 2 | Example: Core business revenue declined for 2 consecutive quarters | Serious | Reduce position by 50% and re-evaluate |
| 3 | Example: The moat has been clearly breached (the competition has the same ability) | Serious | Start in-depth research and consider exiting |
| 4 | Example: Regulatory policies fundamentally change the business model | Serious | Reassess intrinsic value |
| 5 | Example: Management’s large-scale reduction of holdings (unplanned) | Warning | In-depth investigation into the reasons |

**Duan Yongping**: "There are only three reasons to sell: 1. Found that the purchase was wrong; 2. The company's fundamentals have changed; 3. Found a better one."

### A4: Valuation anchor point

| Indicators | When to Buy | Optimistic Target | Neutral Target | Pessimistic Scenario |
|------|-------|---------|---------|---------|
| Stock Price | | | | |
| PE | | | | |
| Market capitalization | | | | |
| Intrinsic value estimation | | | | |
| Margin of safety | | | | |

### A5: Save the paper

Write the investment thesis to `reports/{company name}-thesis.md`, including:
- Creation date
- Buy price and position
- Core thesis (5 sentences)
- List of core assumptions
- Red line list
- Valuation anchor
- Tracking record table (initially empty)

---

## Mode B: Tracking Check

### B1: Read existing papers

Read `reports/{company name}-thesis.md` and load:
- Core papers
- List of core assumptions
- Red line list
- Last inspection record

### B2: Collect the latest data

Use WebSearch to collect:
1. Latest financial report data (if there is a new quarterly/annual report)
2. Recent major events (management changes, regulatory policies, competitive dynamics)
3. Current stock price and valuation indicators
4. Insider transaction records (increase or decrease of holdings by major shareholders)

### B3: Check core assumptions item by item

For each core hypothesis, verify with the latest data:

| # | Core hypothesis | Last state | Latest evidence | Current state | Changes |
|---|---------|---------|---------|---------|------|
| 1 | Revenue growth rate 15%+ | 🟢 Established | Q4 revenue growth rate 12% | 🟡 Margin weakening | ⚠️ |
| 2 | Gross profit margin 60%+ | 🟢 Established | Gross profit margin 61.2% | 🟢 Established | — |
| 3 | ... | ... | ... | ... | ... |

Status definition:
- 🟢 **Established** — Latest data supports this hypothesis
- 🟡 **Marginal Weakening** — Data is still within acceptable range, but trend is unfavorable
- 🔴 **impaired** — data clearly does not support this hypothesis
- ⚫ **Broken** — hypothesis has been disproven

### B4: Red line check

Check the red line list one by one:

| # | Red line condition | Whether to trigger | Evidence |
|---|---------|:-------:|------|
| 1 | Management Integrity Issues | ❌ Not Triggered | — |
| 2 | Core business declined for 2 consecutive quarters | ❌ Not triggered | — |

**Any red line is triggered → Mark it clearly in the report and give clear action suggestions. **

### B5: Valuation Update

| Indicators | When Buying | Last Check | Current | Changes |
|------|-------|---------|------|------|
| Stock Price | | | | |
| PE(TTM) | | | | |
| Intrinsic value estimation | | | | |
| Margin of safety | | | | |

### B6: Output tracking report

#### Report structure

```
1. Paper health score (out of 10 points)
2. Core hypothesis check results (table)
3. Red line inspection results (table)
4. Key changes in this issue (no more than 500 words)
5. Valuation update
6. Conclusions and suggestions for action
7. Key points to pay attention to during the next inspection
```

#### Paper Health Scoring Criteria

| Rating | Meaning | Suggested action |
|:----:|------|---------|
**Calculation formula**: Health = 10 - (⚫Number of ruptured hypotheses × 3) - (🔴Number of damaged hypotheses × 2) - (🟡Number of weakened hypotheses × 1) - (Number of red line triggers × 5), with a minimum score of 1 and a maximum of 10 points.

| Rating | Meaning | Suggested action |
|:----:|------|---------|
| 9-10 | All assumptions are true, the thesis is stronger than when buying | Consider adding to the position |
| 7-8 | The core assumptions are established and individual margins are weakened | Continue to hold |
| 5-6 | 1-2 assumptions are damaged, but the core logic remains unchanged | Hold but be vigilant |
| 3-4 | Multiple assumptions are damaged and the foundation of the paper is shaken | Consider reducing positions |
| 1-2 | The red line is triggered or the core assumption breaks | Strongly recommended to sell |

#### The conclusion must be clearly answered

1. **Is the paper still complete? ** Intact / Marginally weakened / Damaged / Cracked
2. **How to do it? ** Add to position / hold / reduce position / clear position
3. **Next inspection time**: after the release of the next quarterly report / after a specific event

### B7: Update thesis file

Append this inspection record to the tracking record table of `reports/{company name}-thesis.md`:

| Check Date | Health | Core Changes | Action Suggestions |
|---------|:------:|---------|---------|
| 2026-04-09 | 7/10 | Revenue growth slowed to 12%, but profit margins improved | Hold |

---

## Key Principles

- **Write down your selling conditions before buying** — Decisions made when calm are better than those made when panicked
- **The paper should be specific enough to be verifiable** - "The company is very good" is not a paper, "ROE>25% and the trend is stable" is
- **As soon as the red line is triggered, act** — The most fearful thing is "wait and see", this is the beginning of losing big money
- **Thesis breaks ≠ Stock price drops** — You don’t have to sell if the stock price drops by 30%, you have to sell only if the thesis breaks.
- **Be honest about mistakes** — Admit if you make a mistake in your paper, don’t hold on for the sake of face.
