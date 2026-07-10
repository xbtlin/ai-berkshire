---
name: investment-research
description: "AI Berkshire skill: Investment research: Buffett-Mung-Dhong-Jongping-Li-Shu-Shong-Shong-Shong-Four Masters Integrated Analysis Framework. Source: skills/investment-research.md."
---

## Codex adapter note

This skill is generated from `skills/investment-research.md` so Claude Code and Codex users share one canonical workflow.

- Treat `$ARGUMENTS` as the user's request in the current Codex thread.
- When the source mentions Claude-only surfaces such as Task, Agent, WebSearch, Bash, Read, or Write, use the closest Codex capability available in this session: subagents when available, web search when needed, shell commands for local tools, and normal file edits for workspace files.
- Use shared project tools from `tools/` in this repository. Prefer running commands from the repository root with paths like `python3 tools/financial_rigor.py ...`; if the current thread starts outside the repo, locate the actual checkout path first instead of assuming a fixed home-directory path.
- Before starting research, run the `date` command to confirm today's date; treat it as the baseline for "latest" data and state the data cutoff date in the report header. Never assume the current date from training data.
- Preserve the research quality rules from `AGENTS.md`: cross-check financial data, use exact arithmetic tools for valuation/math, and clearly label uncertainty and source gaps.

# Investment research: Buffett-Mung-Dhong-Jongping-Li-Shu-Shong-Shong-Shong-Four Masters Integrated Analysis Framework

Systematized investment research analysis for $ARGUMENTS.

# Framework for research

Based on the methodology of the four master investment masters: Buffett, Mang, Suh Yongping and Lee Shu, the study was carried out in the following seven modular order:

# Prestep: AI study bias conscious (must be implemented)

Before starting the study, the company's "AI researchability" was assessed to identify potential data bias:

** Information abundance rating**:
♪ The big, big, big, big, big, big, big, big, big, big, big, big, big, big, big, big, big, big, big, big, big, big, big, big, big, big, big, big, big, big, big, big, big, big, big, big, big, big, big, big, big, big, big, big, big, big, big, big, big, big, big, big, big, big, big, big, big, big, big, big, big, big, big, big, big, big, big, big, big, big, big, big, big, big, big, big, big, big, big, big, big, big, big, big, big, big, big, big, big, big, big, big, big, big, big, big, big, big, big, big, big, big, big, big, big, big, big, big, big, big, big, big, big, big, big, big, big, big, big, big,
|------|------|-----------|---------|
A.C. (information is abundant) Years of listing, high bond-market coverage, intense media coverage, too much consensus, AI output converges on market pricing, alph is limited, and the focus is on the opposite: why not the smart?
The AI may fill the blanks with "reasonable speculation", but it looks complete and false.
<unk> C (information scarce) <unk> New listing/cold-door equity/emerging markets, almost no coverage <unk> AI is overconservative due to insufficient information, misconstruing it as "unable to see" <unk> <unk> <unk> <unk> Question with first-sex principle (see below) <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk>

** First-class theory study for C companies**:
When the information is not sufficiently public, do not attempt to collage the "looks complete" reports, but focus on the following bottom-line issues:
Who is the customer? Why are you paying? Is there an alternative?
2. How is repurchase driven? Is it habit, lock, or is it the continuous creation of new values?
Can a competitor replicate this business with 10 billion dollars?
4. What key decisions have management made and what are the judgement and values reflected in these decisions?

** Self-checked list of prejudices** (research vigilance throughout the course):
- [ Laughs ] Is my "sure" feeling business-based or is it from the amount of information?
- [ Laughs ] If we cut the company's data by half, will my conclusions change?
- [ ] Is the analysis of AI output highly similar to the market consensus? If so, what is my information advantage?
- [ ] Is there a risk that "the public information is scarce but the business is extremely good" is underestimated?

The information abundance rating results are included at the beginning of the report and the difference between "AI research confidence" and "actual investment certainty" is noted in the final conclusions.

# Step one: data collection

> ** Data source instruction**: See `kills/final-data.md ' . All financial data must come from two independent sources and error > 1% must be marked.
> - US share: Macrotrends(master) + stockanalysis (sub-author)
> - Port Unit: aastocks (main) + macrotrends ADR (sub-author)
> - A share: Eastern Wealth (Main) + Trend Information (sub-)

Start backstage with Task tool Agent to collect the following data from the network:

1. Income structure: revenue, growth, Māori rate for recent fiscal years and nearly four quarters
2. Financial indicators: nearly five years of income, net profit, Māori rate, operating profit margin, free cash flow, cash reserve
3. Competition patterns: market shares, major competitors versus competition
4. Business models and moats: sources of core competitive advantages
5. Technical capacity: core technology warehouse, R & D inputs
6. Management: founder/CEO ' s curriculum vitae, shareholding ratio, key decision-making records
7. Industry prospects: TAM (total locationable market), growth projections
8. Risk factors: geopolitics, regulation, supply chains, etc.
Current valuation: market value, PE, PS, PEG, EV/Revenue
10. Core multi-empty arguments

## Data cross-checking (must be implemented, financial rigour tools used)

Once data collection is completed,** it is necessary to call `tools/final_rigor.py ' to process key data** and to eliminate the error in the LLM ' s mind.

** Data points to be verified**:
- Total equity (as confirmed from at least two sources, including exchange, Yahoo Finance, StockAnalysis)
- Current stock prices and market values (** Manual calculations of total stock value x and comparison with reported market value, prevention of unit errors**)
- Recent fiscal year income and net profits (as recognized from corporate annual reports + at least one third-party source)
- Cash reserves and net cash (cash + short-term investments - total debt, note for calibre differences)
- Management share ratio (differentiating economic equity from voting rights, note AB unit structure)

** Force verification steps (using the Bash call tool)**:

Step 1 — Market value measurement (exact decimal, non-floating):
```bash
python3 tools/financial_rigor.py verify-market-cap \
- Price {equity} - Shares {total equity} - reported market value} - Currence {currency}
```

Step 2 — Key data multi-source cross-check:
```bash
python3 tools/financial_rigor.py cross-validate \
--field {field name} --values '{"source1": value, "source2": value} --unit {unit}
```
Separately, for income, net profit and cash reserves.

Step 3 — Exact valuation indicator measurement (PE/PB/ROE/ FCF Yield et al.):
```bash
python3 tools/financial_rigor.py verify-valuation \
--price {equity value} --eps {EPS} --bvps {net assets per share} --fcf-per-share {FCF} --dividend {per dividends}
```

** Certification rules**:
1. At least 2 independent sources per key data point
2. Where discrepancies between sources are identified, preference is given to the use of company annual reports/exchange data, with an indication of the reasons for the discrepancies
3. **All data related to calculations must be measured by tool, and LLM heart control is prohibited**
4. Tool output results directly embedded in the "Critical Data Cross-Current Record" appendix to the report
If the tool reports are too far apart, the reasons must be checked before further analysis can be conducted

** Common error prevention**:
- Market value unit: Hong Kong dollar vs. yuan.
- FCF caliber: the definition of capital expenditure may differ from source to source (whether or not it includes leasing, acquisition, etc.)
- Debt calibre: whether operating lease liabilities are included
- Shareholding ratio: economic interests of AB companies <unk> Voting rights

Step 2: Business Essentials Analysis - A Part of "The Right Business"

Elements of analysis:
- Define the nature of this business in a single sentence.
- Dismantling of income structure (charts)
- Five-year trend in profitability (charts)
- Business model canvass: one-time sale vs subscription/repurchase? hardware vs software vs platform?
- Eco-cooperability/client lock strength
- Level of Māori compared to peer, explaining why it is high/low
- Business Leveraging Analysis
- **The Infinity **: Where is the business? If only one sentence is used, what is it?

# Step three: A moat river assessment -- Buffett "The Economic moat."

The five types of moats are verified:

♪ The moat type ♪
|-----------|---------|
<unk> Brand/pricing rights <unk> Can you raise prices without losing sales? <unk>
How much is the cost of moving customers to the competition?
The more products the more users are, the better the product?
What are the cost advantages of scale?
Technology/proprietary barriers, technology leads a few years?

Analysis of the trend in the moat: broad or narrow over the past five years?

**Buffettian **: 10 years later, is this moat still there? What can destroy it?

# Step four: Reverse thinking and risk list - Manger "inverted"

- List all the paths that this company may fail.
- Historical analogy: what was the outcome of finding companies in a similar position in history?
- Interdisciplinary analysis: cross-checking using models such as network effect theory, technology adoption curves, competitive games, etc.
- Misconduct: narrative deviation, anchoring effects, survivor bias
- Collect core arguments of empty parties

** Man format chase **: Where am I most likely to make a mistake? Why is smart people not buying/making empty of this company?

# Step five: Management assessment - a "right person" # Buffett "good management."

- CEO/founder ' s key decision review (table: time/decision/outcome/scoring)
- Capitalization capacity: R & D returns, M & A success rates, buyback timing
- Consistency of shareholders: management ownership, remuneration structure, reduction of records
- Organizational capacity: team stability, critical talent risk
- Cultural identity of enterprises

**The Eternity of the Enquiry**: If the CEO retires, will the company remain competitive?

# Step 6: Industry and civilizational trends - Lee Siu 'A framework for civilization evolution

- to determine whether the industry is in a "civilizational paradigm shift."
- Historical technological revolution analogy (steam engine/electricity/Internet/AI)
- TAM Growth Curve and ceiling analysis
- Position of the company in the industrial value chain
- Technology route risk
- Client/vendor concentration analysis

**Li's follow-up**: Stand back 20 years later, is this company "Standard Oil of the Age" or "Standing 3Com"?

# Step seven: valuation and security margin -- Barfitt "inner value" + price of "right"

- Current market pricing (Key Valuation Indicator Table) - ** Must pass tool validation**
- Inverse DCF: What are the growth expectations implied in current stock prices?
- Three scenario valuations - ** Must be calculated accurately by tool, inhibition of heart calculations**:
```bash
python3 tools/financial_rigor.py three-scenario \
- Price {shares {total equity billion)
{\cHFFE7C5}--groth {optimal {\cH00FFFF}--
- Pessimism Pessimism 3--Currentity {currency}
```
- Compared to their own historical valuations
- Comparison with peer valuation

** The Yongping question** If the stock market is closed for five years tomorrow, would you hold it at this price?

# Step 8: A comprehensive decision-making memorandum

Summary table:

♪ The dimension, the conclusions, the confidence, the confidence ♪
|------|------|--------|
♪ The quality of business ♪
♪ The moat ♪
<unk> Management (Yongping + Buffett) <unk>
The most dangerous risk (Munge)
<unk> Civilization trends (Li Ji)
<unk> Valuation (Buffett + Eongping) <unk>

Final decision form:

Policy Recommendations
|------|------|
♪ The empty man ♪
♪ The man who owns the barn ♪
♪ Sold the signal ♪
♪ The mackerel signal ♪

Four masters' simulations (in citation format).

# Output requirements

1. All analyses must be supported by data sources
2. Use Markdown tables to present key data
3. Each module must have a match to the master 's "chat" at the end.
4. Final inclusion of the complete report in the investment study `~/[name of company].md '
5. Make the conclusions clear and not shy away from making recommendations for buy-in/watch-and-see/shunting
6. The valuation component must give a specific price range
7. **The report begins** with the need to include "A/B/C" and "A.R. Limitation Statement".
8. **The report ends** with a distinction between "AI's analytical confidence" - which depends on the amount of information - and "investment certainty".
If the company falls into category C (information is scarce), the report must end with a list of "lists of issues requiring first-hand validation" - suggesting that readers supplement AI's blind areas through field surveys, product experiences, supply chain interviews, etc.

# Data extraction (promising process)

After the report is written into the document,** a data check must be performed and only after it is passed can the following be published:

**Step 1 — Extracting sample list (15% random sample):**
```bash
python3 tools/report_audit.py extract \
-Report < Report Document Path>
```
Outputs the JSON template, each containing `fetched_value ' (to be filled).

**Step 2 ** Denumeration:**
For each data point in the inventory, take the number from a reliable source by `kills/final-data.md '
(US share: macroftrends+stockanalysis; Port: aastocks+macrofts; A: Eastern wealth plus tidal information)
Enter `fetched_value ' / `fetched_source ' / `fetched_value2 ' / `fetched_source2 ' .

**Step 3 ** Export judgement:**
```bash
python3 tools/report_audit.py verdict \
- It's a complete json.
-Report < Reporter Name >
```

- ** [Acceeded]**: All sampling deviations <unk> 1% <unk> Reports are available for publication
- ** [Runback]**: Any dot deviation > 1% <unk> Re-checked after correcting the corresponding data until it is cleared
