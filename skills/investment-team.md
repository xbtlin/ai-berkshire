# Teams: parallel analysis framework for four roles

Undertakes a team-based investment research analysis for $ARGUMENTS. Use the Team tool to create a real multiAgent parallel research team.

# Execute process

# Step one: show team framework

Show the following team structure to users, confirm it and start:

Role responsibilities responsibilities * Analysis framework * Analysis framework *
|------|------|----------|
**team-lead** (yourself) **
<unk> Business-analyst** Business model & moat river analysis <unk> Eongping perspective <unk>
**final-analyst** Financial statements & valuation analysis ** Buffett perspective **
**Industry-researcher**
<unk> rsk-assessor** <unk> Risk assessment & management development <unk> Lee Shun perspective <unk>

# First half: AI researches prejudice assessment

Before creating a team, show users the company's "AI researchability" assessment:

** Information abundance rating** (decision on research strategy):
<unk> Level, <unk> Characteristics, <unk> Research strategy adjustment, <unk>
|------|------|------------|
Teams focus on ** reverse-check** and ** non-consensual perspective** to avoid exporting the right "black bullshit" that is consistent with the market.
<unk> B (median) <unk> Short-listed, limited coverage <unk> Every Agent extrapolation must be trusted, and the team-lead aggregation time "data adequacy" <unk>
<unk> C level (information scarce) <unk> Cold door/new market/emerging market <unk> Team shift to "first-of-the-ground mode": not seeking the integrity of the report, focusing on a few core issues of business nature <unk>

** Key reminder**: The information is highly uncertain and the information is less certain. The confidence that AI can export <unk> The true certainty of investment is derived from the business model itself, not from the amount of information.

Inform each Agent of the rating results, affecting the way they are studied.

## Step 1 — 4: WebSearch Permission Pre-check (Key & Avoid Agent Degradation)

Before creating a team and starting any backstage Agent **, it is necessary to confirm that WebSearch permissions have been released.

**: Why must pre-screen**: Ben skill uses `run_in_background: true ' to start 4 backstages, Agent,** whose backstage cannot play interactive privileges to users** if `WebSebSearch `is not in `permissions.allow' white list `is intercepted ** that leads to degradation as a false study based on training knowledge (with knowledge deadlines) only, but still exports a "looks complete, but not connected" by frame `this is the most dangerous failure of this skill (see issue #58).

** Pre-screening steps**:
1. Check with Bash whether the white list contains WebSearch:
   ```bash
   grep -l '"WebSearch"' .claude/settings.local.json ~/.claude/settings.local.json 2>/dev/null
   ```
If both are missed (i.e. not released) ** Stop, do not start Agent**, prompt the user:
> > < < < < webSearch detected not in the list of rights. The back-office study Agent cannot be connected and will be degraded to a simple training-based response. > > > > > mission.
3. Hits continue normally.

# Step 2: Create a team

Create a team using TeamCreate:
- Team_name: `{corporate name}-research` (in lower case, e.g. `meituan-research ' )
- agent_type: `team-lead`

# Step 3: Create four tasks

Create the following four tasks using the TaskCreate (with subject, description, activeForm):

Task 1: Business Model Analysis
- subject: `Analysis of {corporate name} business models, moats and user values '
- Discreet contains:
1. The essence of business models: definition of core business, dismantling of income structures
2. How the platform/product fly-wheel effect works
3. Elephant River Analysis: Brand/conversion costs/network effects/scale effects/technical barriers, one by one
4. User/client value: what unique value has been created for all parties
5. Operational matrix and synergies
6. Evaluating the "good business" criteria of Sing Yongping: differentiation, pricing rights, sustainable competitive advantage
7. Request for public information such as updates on financial reports, industry reports, etc.

Task 2: Financial and valuation analysis
- subject: `Analysis of {corporate name} financial data, profitability and valuation '
- Discreet contains:
1. Trends in revenue, net profits, operating profits for nearly 3-5 years
2. Profitability indicators: ROE, ROA, Mäori rate, operating profit margin
3. Cash flow analysis: operating cash flows, free cash flows, capital expenditures
Balance sheet health: cash reserves, debt ratios, liquidity
5. Valuation analysis: PE/PS/PB/EV, etc., compared to history and industry
6. Security margin assessment: intrinsic value vs current share price
7. ** Financial rigour validation (Bash caller, disintention)**:
- Market value measurement: `python3 tools/final_rigor.py verify-market-cap-price<unk> price} --shares {equity} --reported {reported}-market value} -Currecy {currency}
- Valuation: `python3 tools/final_rigor.py value-value-price<unk> eps {EPS} --bvps {net assets per unit}
- Critical data cross-checking: `python3 tools/final_rigor.py cross-value-field-field {field} --values ' {JSON}' --unit {unit}
- Three scenario valuations: `python3 tools/final_rigor.py three-scenario -- price -- price}-eps {EPS}-shares {equity billion}--groth {middle pessimism}--pe {smuggling <unk> ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
- The output of the tool is directly embedded in the report as a validation record

Task 3: Industry and Competition Analysis
- subject: `Analysis of {industry} industry patterns and {corporate name} competition dynamics '
- Discreet contains:
1. Industry size and growth: market size, growth, penetration
2. Competition patterns: market shares of major rivals, comparison of competition strategies
3. Core competitor threat assessment: individual analysis of major competitors
4. Disaggregated track patterns
5. Industry trends: technological change, policy implications, new entrants
6. Industrial chain analysis: value distribution up-to-central and downstream
7. Requires search for up-to-date industry data and competition developments

Task 4: Risk and Management Assessment
- subject: `Assessment of investment risk and management quality {corporate name}
- Discreet contains:
Management assessment: CEOs ' circle of competence, integrity, strategic vision, capital allocation capacity, quality of historical decision-making
2. Regulatory risk: current and potential regulatory impacts
Competition risk: threat assessment by competitors
4. Operational risk: new operating losses, expansion uncertainties
5. Macro-risk: economic cycle, industry cycle impact
6. Governance structure: equity structure, associated transactions, shareholder return policy
Long-term certainty: What will companies do in 10 years? What could destabilize their business model?
8. Request for a search for recent regulatory developments, management statements, etc.

# Step four: start four parallel Agents

Start four Agents simultaneously using the Task tool (** must be called in parallel in the same message):

Configuration of each Agent:
- `subagent_type`: `general-purpose`
- `run_in_background`: `true`
- `team_name ': counterpart team name
- `name ': counterpart role name (business-analyst / financial-analyst / industry-researcher / rsk-assessor)

Prompt templates for each Agent:

```
You are the "Round Chinese" of the research team, responsible for analysing the investment perspective from the point of view of the company.

Please complete #{task number}: {tasksubject}

Specific requirements:
{The job description content}

** Methods of study**:
- Use WebSearch to search for state-of-the-art public information (fiscal, industry reports, news)
- ** Financial data must come from two independent sources**, by `kills/final-data.md ' (US: macrectrends+stockanalysis; Port: aastocks+macrotrends; A: Eastern wealth plus tidal information), two-source error >1%
- Ensure accurate data, key data label source
- The analysis needs to be deep, not surfaced.
- ** Network failure prohibits disguise**: if WebSearch is intercepted/unusable, it is prohibited to use training knowledge to simulate the results of the network.

**Export request**:
- Report in detail, presenting key data using Markdown tables
- Each analytical dimension must have clear conclusions and ratings.
- The report should end with a general conclusion on the dimension.

** After completion**:
Mark task #{task number} as completed
2. Send complete analysis to team-lead via SendMessage
```

# Step five: receiving reports and tracking progress

- Real-time presentation of the schedule to users (who have completed the work and who are still under study)
- Each report received, updating progress and presenting the core elements of the report (3-5 articles)
- Waiting for all four reports.

# Step six: close team members

After all reports are received, the report is sent to four Agents (using SendMessage, type: "Shutdown_request”).

# Step seven: summary final report

Combine four analytical reports, and produce the following final reports:

---

# 1. One word of conclusion
> Summarize whether it is worth investing and core logic with a phrase (50-100 words)

##2. # 4D summary score
<unk> dimension, <unk> frame, <unk> rating (1-5 star) <unk> core judgement <unk>
|------|------|------------|----------|

Overall rating: X/5

##3. Core data quick
Tables of key financial and business indicators (relatively 2 years of comparison)

##4 4. Summary of dimensions analysis
Three or five of the most important discoveries per dimension.

##5. Investment argument (Bull vs Bear)
- <unk> Look at logic (5-7)
- <unk> Ostentatious logic (5-7)

# 6. Baffert bought the former Checklist
♪ Check the item through ♪
10 core checks, one by one

##7. Final investment advice
- Qualitative judgement forms (business quality/management/value/time)
- Quantified Recommended Schedule (radical/stabilistic/conservative <unk> Recommendation + price range)
- Key catalysts (silo signals/silo reduction signals 3-5 each)

## 8. Summary Paragraph
Final summary 100-200 words

---

# Step eight: Save the report

Write the complete final report to the investment study `~/{corporate name}<unk> Date}.md` (date format YYYMMDD).

## Step 9: Data extraction (promising process)

```bash
# Step 1 — extract the sample list (15% random sample)
python3 tools/report_audit.py extract \
-Report < Report Document Path>

# Step 2 — Checks from each list from reliable sources (see skills/final-data.md)

Step 3 - Output Permission/Running Judgement
python3 tools/report_audit.py verdict \
- It's a complete json.
-Report < Reporter Name >
```

** [Accredited]** All reports available;** [Rocked back]** There are no re-trials after revision.

Step 10: Cleaning team

Use TeamDelete to clean up team resources.

# Important attention

**4 Agents must start in parallel** - 4 calls to the Task tool in the same message
**Agent reported through SendMessage** - not document collaboration, message communication
** Data accuracy** - Request that Agent use WebSearch to search for up-to-date data, cross-check key data
** Conclusions to be clear** - not shy away from offering buy-in/watch-seeing/sustainability advice and specific price ranges
** All analyses must be supported by data** - with data sources
** Patience** — 4 Agent studies take minutes to update user progress in real time
** Anti-prejudice awareness** - Team-led must assess when summarizing: Are the Agent analyses limited to the adequacy of information? Are there excessive convergences with market consensus? Final reports need to include "information abundance rating" and "AI research limitation statement"
** The principle of honesty in the scarcity of information** - prefers to leave the white label "data inadequate" in the report, and not to use the presumably full frame to disguise certainty
