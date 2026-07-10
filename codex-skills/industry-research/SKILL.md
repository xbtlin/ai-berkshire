---
name: industry-research
description: "AI Berkshire skill: Industry Investment Research: Panoramic Scan of the Industrial Chain + Four Masters’ Stock Analysis Framework. Source: skills/industry-research.md."
---

## Codex adapter note

This skill is generated from `skills/industry-research.md` so Claude Code and Codex users share one canonical workflow.

- Treat `$ARGUMENTS` as the user's request in the current Codex thread.
- When the source mentions Claude-only surfaces such as Task, Agent, WebSearch, Bash, Read, or Write, use the closest Codex capability available in this session: subagents when available, web search when needed, shell commands for local tools, and normal file edits for workspace files.
- Use shared project tools from `tools/` in this repository. Prefer running commands from the repository root with paths like `python3 tools/financial_rigor.py ...`; if the current thread starts outside the repo, locate the actual checkout path first instead of assuming a fixed home-directory path.
- Before starting research, run the `date` command to confirm today's date; treat it as the baseline for "latest" data and state the data cutoff date in the report header. Never assume the current date from training data.
- Preserve the research quality rules from `AGENTS.md`: cross-check financial data, use exact arithmetic tools for valuation/math, and clearly label uncertainty and source gaps.

# Industry Investment Research: Panoramic Scan of the Industrial Chain + Four Masters’ Stock Analysis Framework

Conduct systematic industry chain investment research on the $ARGUMENTS industry.

## Research Objectives

Starting from an investment theme/logical chain, complete:
1. Verify every link of the investment logic chain
2. Draw a panoramic view of the complete industrial chain
3. Scan all listed companies around the world (A shares/Hong Kong stocks/US stocks/international)
4. Perform the Four Masters Framework analysis on the leading companies in each segment.
5. Output industry-level investment portfolio allocation recommendations

---

## Step one: Investment logic chain construction and verification

### 1.1 Draw logical chain
Use arrow links to express the causal relationship from "underlying trend" to "benefit target", for example:
```
Underlying trend A
    → leads to demand B
        → Create bottleneck/rigid need C
            → Benefit industry chain D
```

### 1.2 Step-by-step verification
Question each arrow of the logical chain and look for evidence:

| Links | Core Assumptions | Verification Methods | Data Sources |
|------|---------|---------|---------|
| A→B | | Search industry data/forecasts | |
| B→C | | Search supply and demand analysis | |
| C→D | | Search actual cases/signings | |

### 1.3 Find "Authentication events that have occurred"
List the **signed/implemented real business events** (rather than predictions) that support this logical chain, such as large company purchase agreements, policy documents, industry reports, etc.

---

## Step 2: Drawing a panoramic view of the industrial chain

### 2.1 Draw the industrial chain structure
Disassemble the industry into upstream → midstream → downstream → auxiliary links, for example:
```
Upstream: raw material/resource extraction → material processing/purification
Midstream: core equipment manufacturing → system integration/engineering construction → new technology research and development
Downstream: Operation/Service → End Customer
Auxiliary: Testing/Certification → Maintenance Services → Financial Instruments (ETF/Trust)
```

### 2.2 Identify the "business characteristics" of each link
Label each link:

| Links | Business model | Gross profit margin range | Competitive landscape | Barrier types | Cyclicity |
|------|---------|-----------|---------|---------|--------|
| | Sell resources/sell equipment/sell services/collect rent | | Monopoly/oligopoly/full competition | Resources/licenses/technology/scale | Strong/medium/weak |

### 2.3 Mark "stuck link"
Identify the links in the industrial chain where supply is tightest, where substitution is most difficult, and where profit margins are highest—these are often the best investment targets.

---

## AI Research Bias Consciousness: Special Traps in Industry Research

In industry research, AI data bias will be amplified in unique ways:

**Industry Level Bias**:
| Types of Bias | Manifestations | Coping |
|---------|------|------|
| Mature industry preferences | There is a lot of data in traditional industries (banking/energy/consumption), and AI analysis looks "more certain" | The certainty comes from the business model, not from the number of research reports |
| Emerging industries are underestimated | New industries (AI applications/synthetic biology, etc.) have little data and AI analysis is conservative | Use "end-game thinking" rather than "current data" to judge industry value |
| Leading preference | Large companies have far more information than small companies, and AI naturally tends to recommend leading companies | Small companies may have a better risk-return ratio, don't ignore it just because the AI analysis is short |
| Listing preference | Scanning only listed companies will miss key unlisted players in the industry chain | Unlisted companies must be searched and marked as "future IPO candidates" |
| English preference | AI has stronger ability to process English information and may underestimate Chinese/Asian market players | Chinese and English information sources must be searched at the same time |

**Anti-bias measures in industry chain scanning**:
1. For each link, not only list "companies that are easy to find with AI", but also actively search for "unpopular but potentially high-quality targets"
2. For small-capitalization companies with scarce information, do not reduce the recommendation level just because the length of the analysis is short—use the core issues (business nature, moat, management) rather than the length of the report to judge
3. Mark each company's "information adequacy" (Grade A/B/C) in the final report to let readers know the reliability of the AI analysis.

## Step 3: Scan global listed companies

Use the Task tool to start the background Agent and conduct a comprehensive search of all listed companies in the industry.

### Search list
- US stock (NYSE/NASDAQ/NYSE American) related companies
- A-share (Shanghai/Shenzhen) related companies
- Hong Kong stock related companies
- Other international markets (Japan/Korea/Europe/Australia, etc.)
- Industry ETFs
- Key unlisted companies (possible future IPO)

### Collect for each company
- Company name (Chinese and English)
- Stock symbols and exchanges
- Market capitalization (approximate)
- One sentence description (position and role in the industry chain)
- Whether the target is pure (pure nuclear power vs diversified with nuclear power business)
- Links in the industrial chain

### Output format
Classified by industry chain links, each link has a table containing all scanned companies.
Then layered according to investment certainty:
- **Tier 1**: Large market capitalization, pure target, industry leader
- **Tier 2**: Mid-market capitalization, pure or high proportion, segment leader
- **Tier 3**: small market capitalization, development stage, high risk and high flexibility
- **Tier 4**: Large enterprises with related businesses among diversified companies

---

## Step 4: Analysis of the four masters of the leading companies in each link

For **Tier 1 and Tier 2 companies** in each industry chain link, perform the following analysis (a brief review of Tier 3/4 companies will suffice):

### 4.1 The nature of business (Duan Yongping)
- Define in one sentence what this company does in the industry chain
- Income structure and growth rate
- Gross profit margin/net profit margin levels and trends
- Cash flow characteristics
- **Follow-up**: Is this a good business? Why?

### 4.2 Moat (Buffett)
Rating using five types of moats (★1-5):

| moat | strength | evidence |
|--------|------|------|
| Brand/Pricing Power | | |
|Switching costs | | |
| Network effects | | |
| Scale effect | | |
| Technical/License Barriers | | |

**Follow-up question**: Will the moat still be there in 10 years?

### 4.3 Risk (Munger)
- How is this company most likely to fail?
- How much is it worth in the worst case scenario?
- Why don’t smart people buy it?

### 4.4 Management (Duan Yongping + Buffett)
-Who is the CEO/Founder? Key decision records
- Alignment of shareholding ratio and interests
- Brief review (Grade A/B/C)

### 4.5 Valuation Snapshot
- Current PE/PS/EV/EBITDA
- Compare with competitors in the same segment
- Brief comment: Expensive/Reasonable/Cheap

### 4.6 Recommendation
Mark with ★1-5:
- ★★★★★ = Core position candidate
- ★★★★☆ = Satellite position candidate
- ★★★☆☆ = Watchlist
- ★★☆☆☆ = High Risk Options
- ★☆☆☆☆ = Not recommended

---

## Step 5: Industry-Level Risk Assessment (Munger "Checklist")

### 5.1 Systemic Risk List

| Risk | Probability | Impact | Countermeasures |
|------|------|------|---------|
| A certain link in the investment logic chain has been falsified | | | |
| Alternative technologies emerge | | | |
| Policy/Regulatory Black Swan | | | |
| Periodic callbacks in demand | | | |
| Valuation bubble bursts | | | |

### 5.2 Historical Analogy
Find similar industrial chain investment themes in history and analyze their final outcome:
- What is the analog industry?
-Who is the winner? (Upstream/midstream/downstream?)
-Do most investors make money or lose money?
- What are the implications for the current industry?

### 5.3 Self-examination of errors
- Narrative bias: Is the story too perfect?
- Anchoring effect: Is it anchored by recent gains?
- Bandwagon effect: Is it because "everyone is buying it"?

---

## Step Six: Judgment of Civilization Trends (Li Lu Framework)

- Is the underlying trend that this industry relies on a "civilization-level paradigm shift" or a "phased boom"?
- What is the closest historical analogy to a technological revolution?
- What will be the endgame for this industry in 10-20 years?
- Which link in the industrial chain is most likely to have a "winner-takes-all" situation?
- Which link is most likely to be disrupted?

---

## Step 7: Portfolio Allocation Recommendations

### 7.1 Recommended combination
Output according to the following structure:

| Level | Position proportion | Target | Link to which it belongs | Core logic |
|------|---------|------|---------|---------|
| **Core positions** | Account for 50-60% of thematic positions | | | The most certain and the widest moat |
| **Satellite positions** | Account for 25-35% of thematic positions | | | Greater flexibility, slightly lower certainty |
| **Option positions** | Account for 5-15% of thematic positions | | | High risk and high return, can be reset to zero |
| **ETF alternative** | Can replace all of the above | | | "Lazy man's plan" if you don't want to pick stocks |

### 7.2 Buy/Sell Signals

| Signal type | Specific conditions |
|---------|---------|
| Signal to increase position | |
| Reduce position signal | |
| Clearance signal | |

### 7.3 Suggestions on the upper limit of theme positions
Based on the certainty and risk level of the investment logic chain, it is recommended that this theme account for an upper limit percentage of the total position.

---

## Step 8: Comprehensive Decision Memorandum

### Industry General Rating Table

| Dimensions | Conclusion | Confidence |
|------|------|--------|
| Investment logic chain (level of verification) | | |
| The best link (Duan Yongping's "right business") | | |
| The widest moat (Buffett) | | |
| Maximum risk (Munger) | | |
| Civilization Trend Positioning (Li Lu) | | |
| Overall valuation level | | |

### Simulation comments by four masters
Use citation format to simulate the comments of four masters on investment opportunities in this industry.

---

## Output requirements

1. All analyzes must be supported by data, with data sources attached.
2. Use Markdown tables to present key data
3. The industrial chain panorama is represented by a text diagram of code blocks
4. Analyze at least 2-3 leading companies in each link
5. The global company scan should be as complete as possible (A shares/Hong Kong stocks/US stocks/international)
6. Finally write the complete report into `~/[Industry Name]Industrial Chain Investment Research Report.md`
7. The conclusion should be clear and give specific suggestions on targets, positions and price ranges.
8. At the end of each analysis module, there is a "question" from the corresponding master.

## Data sampling (exit process)

After the report is written, a random check of the data is performed and can be released only after passing the report:

```bash
# Step 1 — Extract the random inspection list (15% random sampling)
python3 tools/report_audit.py extract \
  --report <report file path>

# Step 2 — Get numbers from reliable sources for each item in the list (see skills/financial-data.md)

# Step 3 — Output accurate/return decision
python3 tools/report_audit.py verdict \
  --results '<Filled in JSON>' \
  --report <report file name>
```

**【Approved】** All passed → the report can be released; **【Rejected】** Some failed → reexamine after correction.
