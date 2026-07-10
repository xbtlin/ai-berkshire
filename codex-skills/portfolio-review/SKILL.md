---
name: portfolio-review
description: "AI Berkshire skill: Portfolio Management: From \"Researching Companies\" to \"Managing Portfolios\". Source: skills/portfolio-review.md."
---

## Codex adapter note

This skill is generated from `skills/portfolio-review.md` so Claude Code and Codex users share one canonical workflow.

- Treat `$ARGUMENTS` as the user's request in the current Codex thread.
- When the source mentions Claude-only surfaces such as Task, Agent, WebSearch, Bash, Read, or Write, use the closest Codex capability available in this session: subagents when available, web search when needed, shell commands for local tools, and normal file edits for workspace files.
- Use shared project tools from `tools/` in this repository. Prefer running commands from the repository root with paths like `python3 tools/financial_rigor.py ...`; if the current thread starts outside the repo, locate the actual checkout path first instead of assuming a fixed home-directory path.
- Before starting research, run the `date` command to confirm today's date; treat it as the baseline for "latest" data and state the data cutoff date in the report header. Never assume the current date from training data.
- Preserve the research quality rules from `AGENTS.md`: cross-check financial data, use exact arithmetic tools for valuation/math, and clearly label uncertainty and source gaps.

# Portfolio Management: From "Researching Companies" to "Managing Portfolios"

Perform portfolio review and optimization on $ARGUMENTS.

**Supported input formats**:
- Position list, for example: `Tencent 30%, Meituan 20%, Moutai 20%, NVIDIA 15%, cash 15%`
- Or: `Tencent 500 shares @480 HKD, Meituan 1000 shares @130 HKD, ...`
- or: `My Positions` (if there is already a saved portfolio file `reports/portfolio-latest.md`)

> "Diversification is protection against ignorance. There is no point in diversifying if you know what you are doing." - Warren Buffett
>
> "I can count all the really good investment opportunities I've seen in my life on my ten fingers." —— Li Lu

## Design concept

Researching a company is only half of investing. The other half is **portfolio-level decisions**:
- How much to buy? (position)
- For what money? (Source of funds - new money or swap)
- Does it conflict with existing positions? (relevance)
-What does the optimal combination look like? (opportunity cost)

Buffett never looks at a stock in isolation - he's always thinking, "Is this the best thing I can do?"

## Execution process

### Step 1: Analyze positions

The current position is parsed from the input, normalized to the following format:

| Target | Code | Position | Cost price | Current price | Market value | Proportion | Profit and loss |
|------|------|--------|-------|------|------|------|------|

If you enter only a proportion without an amount, you can analyze it based on the proportion.

Also check whether there is an existing portfolio file (`reports/portfolio-latest.md`), and if so, read and update it.

### Step 2: Get the latest data

Use the Task tool to start the background Agent and obtain it in parallel for each position through WebSearch:
1. Current stock price and valuation indicators (PE, PB, dividend rate)
2. Key financial changes in the most recent quarter
3. Recent major events
4. Analyst consensus expectations (forward PE, target price)

Use `tools/financial_rigor.py verify-valuation` to verify the valuation data for each position. Each position is marked with information richness (A/B/C level), and the analysis conclusion of C-level positions is marked with low confidence.

### Step 3: Single position physical examination

Perform a quick health check on each position:

| Target | Current PE | Whether the buying logic has changed | Paper health | Position recommendations |
|------|:------:|:--------------:|:---------:|---------|
| Tencent | 18x | Unchanged | 8/10 | Reasonable |
| Meituan | 25x | Increasing competition | 6/10 | On the high side, consider reducing positions |

Answer for each position:
- [ ] **If you had no position today, would you still buy at the current price? **
- [ ] **If you can't trade tomorrow, are you comfortable holding it for 5 years? **
- [ ] **Is the purchase paper still complete? **

**Duan Yongping**: "If you don't want to hold a stock for 10 years, then don't hold it for a day."

### Step 4: Portfolio level analysis

#### 4.1 Concentration analysis

| Indicator | Current value | Recommended range | Judgment |
|------|-------|---------|------|
| The largest holding proportion | | <40% | |
| Proportion of top three holdings | | 50-80% | |
| Total number of positions | | 5-15 stocks | |
| Cash proportion | | 10-30% (depending on market environment) | |

**Li Lu’s standards**: 3-5 core holdings, with the top 3 accounting for 80%+. **But this requires thorough research on each one. **

**Buffett's Standard**: Core positions should not exceed 10, but more satellite positions are allowed.

#### 4.2 Dependency check

Identify implicit correlations between positions:

| Position A | Position B | Related Types | Risk |
|-------|-------|---------|------|
| Tencent | Kuaishou | Both Chinese Internet | Resonance of regulatory risks |
| NVIDIA | TSMC | AI supply chain upstream and downstream | AI Capex fluctuates in the same direction |
| Meituan | Pinduoduo | Both belong to Chinese consumption | Macro consumption fluctuates in the same direction |

**CHECKLIST**:
- [ ] Are more than 50% of positions exposed to the same theme/industry?
- [ ] Is more than 50% of the position exposed to the same country/currency?
- [ ] If Sino-US relations deteriorate, how much will the portfolio lose?
- [ ] How much will the portfolio lose if the global economy declines?

#### 4.3 Opportunity cost analysis

This is Buffett's core way of thinking - **Every dollar should be placed where the return is highest**.

Sort all positions by "expected annualized return":

| Ranking | Target | Current proportion | Expected annualized return | Certainty | Expected return × certainty |
|:----:|------|:-------:|:----------:|:------:|:--------------:|
| 1 | | | | | |
| 2 | | | | | |
| ... | | | | | |

Expected return estimation method (calculated using `tools/financial_rigor.py three-scenario`):
- **Simplified formula**: Expected annualized ≈ FCF Yield + expected growth rate (main method)
- **Value Verification**: Safety Margin Regression + Profit Growth + Dividend Rate
- **Growth Verification**: Profit Growth × Changes in Reasonable PE

**Key Question**: Is the expected return of the lowest position higher than cash (risk-free rate ~4%)? If not, it should be sold for cash.

#### 4.4 Stress Test

| Scenarios | Assumptions | Portfolio Expected Impact | Maximum Drawdown |
|------|------|-----------|---------|
| Global recession | Corporate profits drop 20-30% | | |
| The conflict between China and the United States escalates | Chinese concept stocks are discounted by 50% | | |
| Interest rates soar | 10-year Treasury bond → 6% | | |
| Technology bubble bursts | Technology stock PE compressed by 40% | | |

Make a qualitative + rough estimate of each scenario (based on the industry attributes and historical valuation fluctuation range of each position):
- Which positions are most affected? Rough influence direction and magnitude range
- Is the combination as a whole affordable?
- Is hedging required?

### Step 5: Optimization suggestions

#### 5.1 Suggestions for position adjustment

Based on the above analysis, specific suggestions for position adjustment are given:

| Action | Target | Current Proportion | Recommended Proportion | Reason |
|------|------|:-------:|:-------:|------|
| Add to position | | | | |
| Reduce positions | | | | |
| Clearance | | | | |
| New warehouse | | | | |
| Not moving | | | | |

#### 5.2 Find alternative targets

If there are positions in the portfolio that are "not as good as cash", or the proportion of cash is too high, it is recommended to use `/industry-research` or `/investment-checklist` to systematically screen the industries/companies of interest instead of directly recommending individual stocks within this skill.

#### 5.3 Cash Management

| Current cash ratio | Recommended cash ratio | Reasons |
|:----------:|:----------:|------|

**Buffett**: Currently holds $382 billion in cash, accounting for more than 25% of total assets - cash is the best position when no good opportunities can be found.

### Step 6: Output combination report

#### Report structure

```
1. Portfolio overview (position table + pie chart description)
2. Single position physical examination (health status of each position)
3. Combination analysis
   - Concentration: Is it overly dispersed/concentrated?
   - Correlation: Implicit correlation and risk resonance
   - Opportunity cost: Is the lowest ranked position worth holding?
   - Stress test: drawdown estimates under extreme scenarios
4. Suggestions for position adjustment (specific operations + reasons)
5. Time for next review and focus
```

#### The conclusion must be clearly answered

1. **Overall health of the portfolio**: Excellent / Good / Needs adjustment / Serious problem
2. What is the most important thing to do? **(Add position X / Reduce position Y / No move)
3. **What is the biggest risk right now? **

### Step 7: Save the combined file

Write portfolio information to `reports/portfolio-latest.md`, including:
- Latest position list
- Date and conclusion of this review
- Position adjustment record (additional)
- Reminder for next review

---

## Key Principles

- **Every dollar has an opportunity cost** — The cost of holding a mediocre stock is missing out on an excellent one
- **Concentration is not a risk, ignorance is** — It is safer to hold 3 stocks that you understand deeply than to hold 30 stocks that you know only a little about.
- **Cash is a Position** — There’s no shame in holding cash when you can’t find good opportunities
- **Portfolio Level > Individual Stock Level** — A good stock can drag you down in the wrong position
- **Review regularly, but don’t over-trade** — Review once a quarter is enough, don’t adjust positions every day
