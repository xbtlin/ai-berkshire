---
name: earnings-review
description: "AI Berkshire skill: Intensive reading of financial reports: in-depth interpretation of first-hand information. Source: skills/earnings-review.md."
---

## Codex adapter note

This skill is generated from `skills/earnings-review.md` so Claude Code and Codex users share one canonical workflow.

- Treat `$ARGUMENTS` as the user's request in the current Codex thread.
- When the source mentions Claude-only surfaces such as Task, Agent, WebSearch, Bash, Read, or Write, use the closest Codex capability available in this session: subagents when available, web search when needed, shell commands for local tools, and normal file edits for workspace files.
- Use shared project tools from `tools/` in this repository. Prefer running commands from the repository root with paths like `python3 tools/financial_rigor.py ...`; if the current thread starts outside the repo, locate the actual checkout path first instead of assuming a fixed home-directory path.
- Before starting research, run the `date` command to confirm today's date; treat it as the baseline for "latest" data and state the data cutoff date in the report header. Never assume the current date from training data.
- Preserve the research quality rules from `AGENTS.md`: cross-check financial data, use exact arithmetic tools for valuation/math, and clearly label uncertainty and source gaps.

# Intensive reading of financial reports: in-depth interpretation of first-hand information

Perform intensive financial report analysis on $ARGUMENTS.

**Supported input format**: `Company Name Quarter`, for example: `Tencent 2025Q4`, `PDD 2025 Annual Report`, `Meituan Latest` (the latest issue is read by default)

> "I never read sell-side research reports, only raw financial reports." —— Li Lu
>
> "I read 500 pages a day. This is how knowledge is accumulated, like compound interest." —— Buffett

## Design concept

Most AI investment research tools rely on second-hand information (news, research report summaries, data websites). But the core ability of Buffett and Li Lu is to read first-hand information—annual reports, quarterly reports, and conference call minutes.

Problems with secondary information:
- Filtered - analysts selectively present data that is favorable to their views
- Time lag - by the time others have finished digesting it, alpha is gone
- Lack of context - "Revenue growth 15%" is divorced from management's discussion of the quality of growth

This Skill directly interprets first-hand information and focuses on what Buffett and Li Lu would really read.

## Execution process

### Pre-step: Data availability rating

| Level | Characteristics | Impact |
|------|------|------|
| Level A | Obtain the complete original text (10-K/Annual Report/Conference Minutes) | Perform all steps normally |
| Level B | Only part of the original text or third-party summary was obtained | Mark "non-original source" and reduce the weight of the annotated analysis |
| Level C | Only news reports and data website summaries | Focus on changes in core financial data, skip explanatory mining, and mark "insufficient primary information" |

### Step one: Obtain first-hand information

Use the Task tool to start multiple background Agents **in parallel** to obtain the following raw materials:

1. **Original text of the financial report**: Obtained from the company's IR page, SEC EDGAR (US stock 10-K/10-Q), Hong Kong Exchanges and Clearing Limited (Hong Kong stocks), and Juchao Information Network (A shares)
2. **Earnings Conference Minutes/Recording**: Obtained from Seeking Alpha, company IR page, Snowball, etc.
3. **Management letter to shareholders** (annual report if available): read in full
4. **Investor Day/Analyst Day Materials** (if available in the near future)

If the complete original text cannot be obtained, use standard data sources to piece it together according to `skills/financial-data.md` specifications (US stocks: macrotrends+stockanalysis; Hong Kong stocks: aastocks+macrotrends; A shares: Oriental Fortune + Juchao Information), but must be marked as "non-original financial report, summarized from a third party", and the key data must be marked if the error between the two sources is >1%.

### Step 2: Core financial data extraction and verification

#### 2.1 Revenue and Income Statement

| Indicators | This issue | Previous issue | YoY changes | Management guidance | Whether the standard is met |
|------|------|------|---------|-----------|---------|

Must cover:
- Total revenue and breakdown of revenue by business/region
- Changes in gross profit and gross profit margin
- Changes in operating profit and operating profit margin (distinguish between GAAP and Non-GAAP)
- Net profit (note the impact of non-recurring gains and losses)
- EPS (base vs diluted)

#### 2.2 Cash flow statement (most important to Buffett)

| Indicators | This Issue | Previous Issue | Changes | Focus |
|------|------|------|------|--------|

Must cover:
- Ratio of operating cash flow vs net profit (>100% is good, <80% requires caution)
- Capital expenditure and its composition (maintenance vs expansion)
- Free cash flow = Operating cash flow - Capital expenditures
- Repurchase amount, dividend amount
- Closing balance of cash and equivalents

#### 2.3 Balance Sheet Health

Must cover:
- Cash + short-term investments vs interest-bearing liabilities
- Net cash/net debt trend
- Changes in receivables turnover days (are you relaxing credit conditions to offset income?)
- Changes in inventory turnover days (is there a backlog?)
- Proportion of goodwill and intangible assets (is there any risk of impairment?)

**Data verification**: Use `tools/financial_rigor.py` to verify key data:

```bash
# Revenue and net profit cross-validation (at least 2 sources)
python3 tools/financial_rigor.py cross-validate \
  --metric "revenue" --values 108.3e9 107.9e9 --sources "Company Financial Report" "Yahoo Finance"

# Market value verification
python3 tools/financial_rigor.py verify-market-cap \
  --price 101 --shares 1.488e9 --reported 1.44e11 --currency USD

# Valuation indicator calculation
python3 tools/financial_rigor.py verify-valuation \
  --price 101 --eps 9.6 --bvps 26.5 --fcf-per-share 10.2
```

### Step 3: Management Discussion and Intensive Reading (MD&A)

This is the part where Buffett and Li Lu spend the most time. It’s not about looking at numbers, it’s about listening to what management has to say.

#### 3.1 Analysis of management tone

Read the management discussion/call speech paragraph by paragraph and mark the following signals:

| Signal type | Specific performance | Example |
|---------|---------|------|
| 🟢 **Honest Signal** | Proactively admit the problem and give specific reasons | "The decline in profit margin this quarter is mainly because our investment in X field exceeded expectations" |
| 🟢 **Clear signal** | The strategy is specific and has quantified goals | "We plan to increase the market share of business X from 15% to 20% in the next 12 months" |
| 🔴 **Blurred signal** | Extensive use of words without substance such as "we believe" and "in the long run" | "We are confident about the future" |
| 🔴 **Transfer Signals** | Avoid direct questions and use other topics | When asked about profit margins, talk about revenue growth |
| 🔴 **Externalization of attribution** | Blame all problems on the macro/industry/competitors | "Due to the impact of the macro environment..." |

#### 3.2 Commitment Tracking

Extract the specific commitments of management from the last financial report/conference, and compare them with the actual situation in this period:

| Commitments of the previous issue | Fulfillment status of this issue | Evaluation |
|---------|------------|------|
| "Profit margin will return to X% in the second half of the year" | Actual Y% | ✅Meet the standard / ❌Not meet the standard / ⚠️Partially meet the standard |

**Duan Yongping**: "The easiest way to judge whether a management is reliable is to see whether he has fulfilled what he said before."

#### 3.3 Key Issue Identification

Extract analysts’ toughest questions from the Q&A session of the conference call, as well as the quality of management’s answers:

| Analyst questions | Management answers | Answer quality (1-5) | Whether to avoid |
|-----------|-----------|:------------:|:-------:|

### Step 4: Annotations and Hidden Information Mining

Hidden in the financial report notes are information that management doesn’t want you to see easily:

#### 4.1 Required notes

- [ ] **Related Transactions**: Are the terms of transactions with major shareholders/related parties fair?
- [ ] **Equity Incentives**: How big is the dilution effect of options/RSUs? What is the exercise price?
- [ ] **Contingent liabilities**: off-balance sheet risks such as litigation, guarantees, commitments, etc.
- [ ] **Accounting policy change**: Has the revenue recognition method, depreciation period, etc. been changed?
- [ ] **Segment Information**: The difference in profit margins of different businesses, whether there is "good business subsidizing bad business"
- [ ] **Customer/Supplier Concentration**: Proportion of top five customers/suppliers

#### 4.2 Abnormal signal detection

- [ ] Accounts receivable growth rate > revenue growth rate (possibly blocked channels)
- [ ] Inventory growth rate > revenue growth rate (may be backlog)
- [ ] Operating cash flow < net profit and the gap widens (profit quality is questionable)
- [ ] Sudden increase in capitalized expenditure (possibly to glorify profits)
- [ ] The proportion of non-recurring income suddenly increased

### Step 5: Compare with historical data

#### 5.1 Trend Analysis

Put the key indicators of this period into a time series of at least 4 quarters (or 3 years of annual reports):

| Indicators | Q-4 | Q-3 | Q-2 | Q-1 | This issue | Trend judgment |
|------|-----|-----|-----|-----|------|---------|

Focus on:
- Are profit margins improving or deteriorating?
- Is revenue growth accelerating or decelerating?
- Is cash flow quality improving or declining?
- Is capital expenditure intensity increasing or decreasing?

#### 5.2 Comparison with management guidance

| Metrics | Management's previous guidance | Actual results | Deviations | Interpretation |
|------|--------------|---------|------|------|

### Step 6: Output intensive reading report

#### Report structure

```
1. Quick overview of core data (one-page table)
2. The three most important changes in this issue (no more than 500 words)
3. Management tone and commitment tracking
4. Hidden information in notes
5. Key issues (selected Q&A from the conference call)
6. Relationship with investment thesis (if any position is held)
7. Conclusion: What has changed in this financial report?
```

#### The conclusion must be clearly answered

1. **Does this financial report exceed expectations, meet expectations, or fall below expectations? **(You cannot say "basically consistent" and then list a bunch of double-talk)
2. **Impact on Investment Thesis**: Strengthening/No Impact/Weakening/Broken
3. **What’s the next catalyst to watch? **
4. **If you already hold it, should you add/hold/reduce it? **

### Step 7: Save the report

Write the report to `reports/{company name}-earnings-{period}.md`, for example `reports/Tencent-earnings-2025Q4.md`

### Step 8: Data sampling (exit process)

After the report is written, a random check of the data is performed and can be released only after passing the report:

```bash
# Step 1 — Extract random inspection list
python3 tools/report_audit.py extract \
  --report reports/{company name}-earnings-{period}.md

# Step 2 — Get numbers from reliable sources for each item in the list (see skills/financial-data.md)

# Step 3 — Output accurate/return decision
python3 tools/report_audit.py verdict \
--results '<Filled in JSON>' \
  --report {report file name}
```

**【Approved】** All passed → released; **【Rejected】** Some failed → reexamine after correction.

## Key Principles

- **Read the original text, not the abstract**: Do everything possible to obtain first-hand information
- **Look at changes, not absolute values**: The trend is more important than the number itself
- **Listen to tone, not just content**: How management says it is as important as what is said
- **Check the notes, not just the text**: The devil is in the details
- **Conclusion, no summary**: The purpose of intensive reading is to form a judgment, not to retell the financial report
