---
name: management-deep-dive
description: "AI Berkshire skill: Management research: buying shares is buying. Source: skills/management-deep-dive.md."
---

## Codex adapter note

This skill is generated from `skills/management-deep-dive.md` so Claude Code and Codex users share one canonical workflow.

- Treat `$ARGUMENTS` as the user's request in the current Codex thread.
- When the source mentions Claude-only surfaces such as Task, Agent, WebSearch, Bash, Read, or Write, use the closest Codex capability available in this session: subagents when available, web search when needed, shell commands for local tools, and normal file edits for workspace files.
- Use shared project tools from `tools/` in this repository. Prefer running commands from the repository root with paths like `python3 tools/financial_rigor.py ...`; if the current thread starts outside the repo, locate the actual checkout path first instead of assuming a fixed home-directory path.
- Before starting research, run the `date` command to confirm today's date; treat it as the baseline for "latest" data and state the data cutoff date in the report header. Never assume the current date from training data.
- Preserve the research quality rules from `AGENTS.md`: cross-check financial data, use exact arithmetic tools for valuation/math, and clearly label uncertainty and source gaps.

# Management research: buying shares is buying

Conducting management depth studies on $ARGUMENTS.

** Supported input format**: `The name of the company ' or `The name of the person ' , e.g. `The United States Corps ' , `The Wang Jing United Group ' , `Hang In-hoon Young Ying Wei Da '

"Assured is a buyer. Find the person you trust and hold it forever."
>
> "Assessment management depends on what they do when nobody looks." > -- Barfitt.

# Designing ideas

Most investment analyses assess management on the surface: curriculum vitae, shareholding, and remuneration. But Buffett spends a lot of time** and he eats and chats with management.

This Skill is a ** in-depth version of the fifth step management assessment. This is used for in-depth research when management ratings are uncertain (below or below) in standard investment studies or when management is the core investment logic.

AI cannot eat with management, but can do so through public information:
- **Tracking management's consistency of words and actions** (Commitment vs.
- ** Analysis of the return on each major capital allocation decision**
- ** Inferring character from decision-making in difficult times**
- ** through feedback from staff/business/clients**

# Execute process

# First step: identifying key management and initiating parallel data collection

Using WebSearch to identify the following key individuals:

Role Name Term Term Term Term Term Term Term
|------|------|------|------|----------|
<unk> CEO/Chairman <unk>
| CFO | | | | |
♪ If you're not in the seat ♪
<unk> Actual control person (if different from CEO) <unk>
Other key executives.

**Note **: Distinguishing "who makes decisions" from "who has the name on the title." Some of the founders of the company are still soul people (e.g. yellow-collars are too many words).

After identifying key individuals, several backstages were activated using the Task tool.
1. Agent 1: CEO ' s public statements and forecast records (shareholder letters, telephone conferences, interviews, social media)
2. Agent 2: Record of capital allocation decision-making (M & A, buy back, split, new business investment)
3. Agent 3: Governance structure and remuneration (equity structure, associated transactions, executive remuneration)
4. Agent 4: Side validation information (staff evaluation, client feedback, industry slogan)

# Step 2: CEO's Capability Circle Assessment

#2.1 Strategic vision

Searching for the CEO ' s public statements (shareholder letters, telephone conferences, interviews, social media) over the past five years, drawing its judgement on the following issues:

Time, CEO's judgement/prediction, actual results, accuracy, accuracy.
|------|--------------|---------|:------:|
"We think X Market will..."
"The point for us in the next three years is to do the actual execution of the...

** Key issues**:
- Did the CEO make the right judgment over the market?
- Did the CEO stay calm when everyone was watching?
- Is the CEO ' s understanding of industry trends following markets or thinking independently?

##2.2 Execution capacity

♪ The way you're going ♪
|------|------|------|
Did you do what you said?
Can you attract and retain talent?
What do you do when you're in trouble?
♪ The speed of error is fast?

#3 Step: Integrity Assessment (most important)

**Buffett**: "We seek three qualities: integrity, wisdom and energy. If there is no first, the last two will kill you."

#3.1 Promise vs follow

From the past three years of the financial statements, telephone conferences, shareholder letters, public interviews, the specific commitments made by management**:

♪ Time, time, time, time, time, time, time, time, time, time, time, time, time, time, time, time, time, time, time, time, time, time, time, time, time, time, time, time, time, time, time, time, time, time, time, time, time, time, time, time, time, time, time, time, time, time, time, time, time, time, time, time, time, time, time, time, time, time, time, time, time, time, time, time, time, time, time, time, time, time, time, time, time, time, time, time, time, time, time, time, time, time, time, time, time, time, time, time, time, time, time, time, time, time, time, time, time, time, time, time, time, time, time, time, time, time, time, time, time, time, time, time, time, time, time, time, time, time, time, time, time, time, time, time, time, time, time, time, time, time, time, time, time, time, time, time, time, time, time, time, time, time, time, time, time, time, time, time, time, time, time, time, time, time, time,
|---|------|---------|---------|---------|------|
<unk> "We're going to make a profit in X business in 2025"
2 million dollars we plan to buy back.

**Expire statistics**:

Performance rate of commitments
|:---------:|------|
> 80% > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > > # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
60-80% <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> in the main directions for the main directions and <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk>
40-60% Of concern - under-delivery of commitments
<40% > Serious problem - untrustworthy < < 40% >

# 3.2 Performance in difficult times

Major crises/difficulties (spills in stock prices, performance miss, regulatory shocks, increased competition) experienced by search companies, analysis of management responses:

<unk> Crisis event <unk> Time <unk> Management response <unk> Post-view evaluation <unk>
|---------|------|-----------|-------------|

** Concern**:
- Is it active communication or hiding?
- Is it internal or outside?
- Is it a difficult but correct thing to do, or is it a short-term market-friendly choice?

#3.3 Attitudinal attitudes towards stakeholders

• Stakeholders <unk> Management attitude <unk> Evidence <unk> Evaluation <unk>
|-----------|-----------|------|------|
<unk> Shareholders <unk> Respect/neglect/use <unk>
<unk> Staff <unk> be nice/cuff/insensitive <unk>
Client/user
Business/suppliers Fair cooperation/extreme price
<unk> Regulation/social compliance/flash ball <unk>

**Lisu**: "Assumption to stakeholders determines the long-term viability of the enterprise. Short-term pressurization can increase efficiency, but it can damage the ecology in the long term."

# Step four: capital allocation capacity

This is Buffett's most valued managerial competence -- ** How much can management turn into every dollar they make?**

##4.1 Record of decision-making on capital allocation

The search company ' s major capital allocation decisions over the past five years have been evaluated in a written way:

** Merger and purchase records**:

Time, amount of money, strategic logic, ex post, rating, 1-5 rating.
|------|---------|------|---------|---------|:---------:|

** Repurchase records**:

`tools/final_rigor.py valuation ' is used to verify valuation indicators such as the time of buyback and current PE.

The average buyback price.
|------|---------|-----------|:------:|---------|:---------:|

** Red record**:

<unk> Year <unk> Red amount <unk> Red rate <unk> FCF <unk> sustainable for the same period <unk>
|------|---------|:------:|---------|:---------:|

** New business investments**:

<unk> Time area <unk> Cumulative input <unk> Current status <unk> Evaluation of returns <unk> Rating (1-5) <unk>
|------|---------|---------|---------|---------|:---------:|

## 4.2 Capital allocation rating

<unk> Dimensions <unk> Ratings (1-5) <unk> Description <unk>
|------|:---------:|------|
Are you buying at a reasonable price?
Do you think the time for repurchases stop when they're underestimated or overestimated?
Is the score match with the FCF?
How's the success rate?
Is the cash reserve reasonable?
** Combined score**

** Buffett standard**: ideal management invests decisively when there are good opportunities, actively buy back/sallow when there are no good opportunities, never doing high-value M&As.

# Step 5: Governance structure assessment

## 5.1 Equity structure

Project details Risk assessment
|------|------|---------|
<unk> AB shares/super-vote vote?
<unk> Founder/Treator Shareholding Ratio?
Is there a VIE structure?
Are independent directors really independent?
<unk> Records of recent stockholders' growth and decline?

##5.2 Rationale of remuneration

<unk> Senior executives <unk> Total annual remuneration <unk>
|------|-----------|:------------:|:---------:|:-------:|

** Concern**: Does the incentive structure correspond to long-term shareholder interests or encourage short-term behaviour?

##5.3 Associated transactions

<unk> Related parties <unk> Trade content <unk> Amount <unk> Whether or not fair <unk> Risk assessment <unk>
|--------|---------|------|:-------:|---------|

# Step six: Side-checking

AI cannot communicate face to face with management, but can be validated through open access to side information.**Note: The following information is dependent on publicly searchable content and may be incomplete, indicating the source of information and availability.

# 6.1 Staff perspective

Search for employee evaluations for Glasdoor ratings, knowledge of discussions, etc.** that are publicly searchable** (the "user can supplement" for the platform that requires a pulse, etc.):

<unk> Dimensions <unk> Rating trends <unk> Key feedback <unk>
|------|---------|---------|
Business culture
Management evaluation
♪ The strength of the work ♪
<unk> Emolument satisfaction
Development prospects

##6.2 Client/business perspective

Searching App Street ratings, consumer complaints, business forum:

<unk> Dimension <unk> Rating/Trend <unk> Key feedback <unk>
|------|----------|---------|
<unk> Product satisfaction
Client services
Business/supplier relations

## 6.3 Industry

Search industry forums, social media and learn about the management ' s evaluation by peers and practitioners.

# Step seven: Situation analysis after CEO leaves

**Buffett**: "Good companies should be run by fools -- because sooner or later they'll be running."

Question. Question. Question.
|------|------|
If the CEO leaves tomorrow, will the company be able to function?
How deep is the current management team?
<unk> ..the competitive advantage of a company is to rely on the CEO personally or on the organization/system?
♪ How's the management transition going in history?

# # Step 8: Export management assessment report

# Report structure #

```
I. Quick-view of key persons (table)
II. Assessment of integrity
- Performance rate of commitments
- Performance in difficult times
- Attitudinal attitudes towards stakeholders
III. CAPACITY ASSESSMENT
- Strategic vision (predictability)
- Enforcement capacity
- Capital allocation records
IV. GOVERNANCE STRUCTURE
- Equity structure risk
- Justification of remuneration
- Associated transactions
V. Side verification
- The employee perspective.
- Client/business perspective
VI. OVERVIEW AND CONCLUSIONS
```

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

<unk> dimension <unk> weight <unk> Rating (1-5) <unk> Weight <unk>
|------|:----:|:---------:|:----:|
Good faith, 35%.
Strategy and implementation capacity 25%
Capital allocation capacity 25%
The governance structure, 15%, 15%, 15%, 15%, 15%, 15%, 15%,
** Combined score** ** ** ** ** ** ** ** ** ** 100% ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** ** *

# A piece of "buyer" standard

> Answer three questions:
> 1. ** Is this person righteous?** (honest, not cheap for shareholders)
> 2. ** Does the person have the capacity?** (Strategic vision + implementation + capital allocation)
> 3. ** Would you like to give the money to this man for 10 years?**
>
> Three are "yes" = <unk> (5 points)
> The first two are "yes" = <unk> (4 points)
> Only the first one is "yes" = <unk> (3 points)
♪ The first one is not "yes" ♪ ♪ 1 point, no vote ♪

# Step 9: Save the report

Write report to `reports/{corporate name}-management-{YYYYMMMD}.md`, for example `reports/USS-management-20260409.md`

---

# Key principles

- ** Integrity is a veto ** – lack of capacity to learn, integrity is not fixed
- ** Seeing behavior doesn't mean words** - What management says doesn't matter, what does matter.
- ** In the middle of the difficulties ** – In the wind, everyone is good CEOs, in the face of the wind.
- ** Capital allocation is the final exam** - Easy money, hard money to make
- ** Don't fall in love with management** - Be objective, even if you like it.
