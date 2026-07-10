# AI Berkshire — AI Memory Files

> This file records Claude’s accumulated project knowledge, user preferences, and historical decisions during collaboration with users for reference in subsequent sessions.

## User portrait

- Investment style: value investment, concentrated holding of large positions, focusing on China's Internet + consumption + AI
- Research preferences: direct and sharp, no nonsense, clear conclusions, don’t flatter both sides, data must be accurate
- Usage scenario: Personal investment decision-making assistance, while promoting this project as an open source product

## Project evolution history

### April 7-9, 2026 (first batch of research + framework improvement)

**Research Completed:**
1. `/investment-team Pinduoduo` — The first complete 4Agent parallel research, with an overall score of 3.4/5
2. `/investment-checklist` 7 companies - Moutai, Tencent, Nvidia, Meituan, Pinduoduo, Bubble Mart, Kuaishou
3. Master position tracking — Buffett/Li Lu/Duan Yongping’s latest 13F + PDD cost price analysis
4. Conducted in-depth re-evaluation of 5 companies including Meituan (users challenged the initial evaluation)

**Correction due to user feedback:**
- Meituan changed from ❌ to ✅ Conditionally passed - User pointed out: It will be too late to buy again after profits recover, 200 billion cannot defeat it = a real moat
- NVIDIA changed from ❓ to ✅ Conditional Pass — AI Capex still accelerating, Jevons Paradox
- Kuaishou changed from ❓ to ✅ Conditionally passed - Keling AI is underestimated and Sora has been shut down

**Key Lesson:**
- Don’t mechanically apply the checklist, use independent judgment
- "Waiting for profits to recover before buying" is a logical fallacy - the stock price will reflect it in advance
- Competitors spend more money but don’t take advantage = best evidence of moat

### Skill system evolution

**V1 (5 Skills) – Covers pre-buy research:**
- investment-research、investment-team、investment-checklist、industry-research、private-company-research

**V2 (9 Skills)—Complete the post-purchase process:**
- Newly added: earnings-review (intensive reading of financial reports), thesis-tracker (paper tracking), portfolio-review (portfolio management), management-deep-dive (management depth)
- After 2 rounds of self-verification iterative repairs: path unification, tool call completion, parallel collection, anti-bias mechanism, quantitative scoring formula

## Core selling points of the project (reflected in README)

1. **It is mandatory not to give a conclusion** — pass/fail/grey, with specific price range
2. **Confrontation from the perspectives of the four masters** — not division of labor but challenge to each other, creating real contradictions and tensions
3. **Structured anti-bias mechanism** — A/B/C information richness, Munger reverse, quick rejection, anti-consensus
4. **Accuracy of financial data** — Decimal accurate calculation, hand calculation of market value, multi-source cross-validation
5. **Reproducible research process** — Same input → output with consistent structure, supporting horizontal comparison and vertical tracking
6. **Multi-Agent Parallel Depth** — 4 Agents search + independent analysis, 4 times the amount of information
7. **Real market verification** — Accumulated income of 1.46 million in two years, continuously outperforming the index by 40-50 percentage points

## User preferences and work habits

- **Report Language**: Chinese
- **Push to GitHub**: After the research is completed, you will usually be asked to push, and ask proactively
- **git operation**: There are often new submissions remotely (the user may be making changes elsewhere), and `git pull --rebase` must be used before pushing.
- **Attitude towards mistakes**: Point it out directly, no need to be tactful. Users will challenge the AI’s judgment, and this should be a serious re-evaluation rather than a defense.
- **Don’t over-summarize**: Users can see the diff and don’t need to repeat what they did after each operation.
- **Research Depth**: It’s better to spend time doing deep and accurate research than to be rough just for the sake of speed.

## Known issues and improvements to be made

- There are some early file names in the reports/ directory that are not standardized (Chinese underscores are mixed), and will be unified into English short horizontal format in the future.
- Some early reports (such as Tencent Holdings-Investment Research Report.md) use the old naming and have not been migrated.
- The actual coverage of the financial_rigor.py tool needs to be verified in the Skill execution
- The output examples in the README are fictitious and should be replaced with excerpts from real reports.
