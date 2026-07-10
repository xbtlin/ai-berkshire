---
name: news-pulse
Discrition: Company news pulse: Rapid attribution in case of stock price variation. Use 4 parallel Agents to detect company events/regulatory policies/industry rivals/market sentiment, to produce "incident time line plus dissident primary judgment + whether to trigger re-examination of the paper".
---

# Corporate news pulse: fast-reducing team with variable stock prices

Recent news surveillance and aversion to $ARGUMENTS.** This is not an in-depth study, but a rapid response to intelligence** -- the goal is to answer in 10 minutes: "What's the recent situation with this company? What's the real reason for the price variation? Do you want to review the investment papers?"

# A fit for scenes

- Holding of warehouse/concerning large increase/slash in stock prices (general trigger: ~5% per day, ~10% per week)
- The stock market changes after the presentation, trying to figure out what the market is reacting to.
- I see the headlines, but I'm not sure if it's the noise or the real signal.
- ** Not applicable**: full study (in `/investment-team ' ), in-depth reading of the financial statements (in `/earnings-review ' ), long-term paper follow-up (in `/thesis-tracker ' )

# Execute process

# Step one: confirm parameters and scene

Clarification to users (if not provided in $ARGUMENTS):

<unk> Arguments <unk> Description <unk> Default <unk>
|------|------|------|
<unk> Name of company** Chinese/English/stock code
** Time window** days of retrospective surveillance news ** 14 days by default, fiscal season can be reduced to 7 days **
<unk> stock variations** <unk> rise/fall + time, e. g. "Down 12/3 Day" <unk> Select to fill in or focus on attribution
** Focus on ** company events / regulation / industry / mood ** Defaults to quadripartite average <unk>

If the user only says the name of the company, then ask: "How many days of news have you been telling us about the recent past? Any specific stock price movements to explain?" -- ** Don't pretend to be.**

## Second step: classification of information availability

A/B/C rating for `investment-team.md ' , but with different dimensions:

<unk> Level, <unk> Characteristics, <unk> Tracking strategy, <unk>
|------|------|---------|
**A level** (information is abundant) ** big stock, wide media coverage, financial season ** focus ** noise reduction and attribution** ** too much information is hard to find, each Agent has to be able to decrypt the double-tracked news *
**B level (median)** Medium and small disks, covering general pattern, with 1-2 separate sources attached to each key event
**C level (information scarce)** Ports share, new listings, cold doors, to "literacy model" - no news explaining the difference may be found,** this conclusion is worth it in itself** (possibly technical/financial rather than basic) **

Inform each Agent of the ratings, affecting their detection methods.

# Step three: create a team

Create a team using TeamCreate:
- `team_name ': `{corporate name}-newsple ' (in lower case, e.g. `pdd-newsple ' )
- `agent_type`: `team-lead`

# Step four: create 4 reconnaissance missions

Create the following four tasks using the TaskCreate:

## Mission 1: Company-event-scout

- **subject**: `Survey {corporate name} Near {n}day of company nature incident '
- **description**:
1. **Official communiqué**: recent disclosure by regulatory disclosure platforms such as port posts/SEC/mode
2. **Foundation and performance guidelines**: latest quarterly/annual reports, performance forecasts, highlights of performance sessions
3. ** Management action**: change in senior management, increase and decrease, buy-back, dividends, equity incentives
**Major business event**: new product release, merger reorganization, business separation, large client/large order
5. ** Capital operations**: refinancing, debt transfer, ADR conversion, A/Creation
6. **Prosecution and compliance**: prosecuted, self-disclosed compliance incidents
7. Each event label: ** Date / Source Link / One Summary / Possible Relevance to Stock Price Variations (High/Medium/ Low)**
8. Output time line tables in chronological reverse

## Mission 2: regulation and policy (regular-watcher)

- **subject**: `Survey {industry/company} Near {N} the regulatory and policy changes of the day '
- **description**:
1. **Industry regulation**: new regulations, fines, modifications, changes in license plates in the industry
2. ** Cross-border policy**: Central American relations (general), customs, export controls, data security
3. ** Tax policy**: VAT, enterprise income tax, individual tax-related changes
4. **Anti-monopoly and competition law**: investigations, fines, merger and acquisition denial
** Special industrial policy**: medical collection, double reduction in education, three-way red line of real estate, Internet platform regulation, etc.
** Currency and foreign exchange**: exchange rate/interest rate/capital control changes affecting the company
7. Each policy indicator: ** Date/Source / Extent of direct impact on the company (direct/indirect/indistinguishable)**
8. Focused judgment: Is there a "policy black swan" just landed?

## Mission 3: Industry and Competition (industry-peer-analyst)

- **subject**: `Survey {corporate name} Industry pattern close to opponent {N} The dynamics of the day `
- **description**:
1. ** Direct opponent**: List of 3-5 core competitors, each looking at the latest events (fiscal, product, price fighting, personnel)
2. ** Up and down the industrial chain**: upstream raw materials/suppliers, downstream customers/channels, recent price, capacity, change in orders
3. **Integration**: industry landscape data, volume of goods delivered, demand side signals (consumption data, tender data, etc.)
4. ** Alternative threat**: New technologies, new business impacts on the industry
5. **Indices of industry**: recent performance of the same sector stock, the company is winning/run/synthesizing
Key judgements: ** Is this an individual company event or is it a business-wide beta fluctuation?**
7. Description of source and date of each event

## Job 4: Market sentiment and seller/big V (sentement-tracker)

- **subject**: `Survey {corporate name} Near {N} days of market sentiment and institutional change '
- **description**:
1. ** Change in vendor rating**: Recent rating/target adjustment for Goldman Sachs, Morgan, Middle Gold etc.
2. ** Change in institutional holdings**: 13F Disclosure (United States share), Ports holdings, Northward financial flows
3. ** Empty data**: empty ratio, newly released empty report if available
4. ** Large V Perspective**: Available from `python3 tools/xueqiu_scraper.py ' . Recent relevant statement V
- Shun Yongping user_id: `1247347556 `
- Example of the command: `python3 tools/xueqiu_scraper.py-user-id 124737556 --keywords {corporate name}, {stock code} --output /tmp/dyp-{corporate name}.md`
- Call only when the company is a feature of Yongping/Li Jie, otherwise skip the time saved
5. ** Rumours and essays**: unverified rumours in the media, social media discussion hot spots (Snowball/X/Reeddit)
**Technology signal**: whether critical support/resistance is touched, large transactions are available, financing coupons are abnormal
Key judgements: ** Is it a fundamental or emotional/financial driver?**

# Step five: parallel start 4 Agent

** Must call Task tool ** in parallel to the same message. Each Agent configuration:
- `subagent_type`: `general-purpose`
- `run_in_background`: `true`
- `team_name ': `company name' - newsple '
- `name ': counterpart role name (company-event-scout / regulatory-watcher / indexy-peer-analyst /sentiment-tracker)

Prompt templates for each Agent:

```
You are the latest {N} day event of the news pulse team, which is responsible for detecting the dimensions of the surveillance.

Time window: {start date} ~ Today date}
Stock price variant: {Focus information provided by users, without exception "No specific movements, routine medical examination"}
Level of availability of information: {A/B/C}

Please complete #{task number}: {tasksubject}

Specific reconnaissance requirements:
{Content of Task Description}

** Reconnaissance method**:
- Give priority to WebSearch search for time-limited queries (key plus date or "latest", "latest", "2026")
- Use WebFech to read the original source (original bulletin, financial statements, regulatory documents) for key events
- "Independent source verification" for each event -- rumor is at least two independent sources.
- ** Don't be misled by the title party**: events whose title does not match the text are marked with "title misled"

** Output format (important)**:
1. ** Core findings**: 3-5 events of the most critical importance, 1 - 2 sentences per article
2. ** Full event time line table** (in reverse order of date):
<unk> Date event source <unk> relevance of stock price variations <unk>
3. **The present dimension attribution conclusion**: Based on the detected event, answer "Can this dimension explain the price variation? How much confidence?"
4. ** Data gap statement**: which information was not found, which were doubtful, what needed to be further information
5. Strict distinction between "fact" and "supposition", following the principle of CLAUDE.md objectivity

** After completion**:
1. Mark task as completed using TaskUpdate
2. Send complete reconnaissance reports to team-lead via SendMessage
```

# Step 6: tracking progress in real time

- Each reconnaissance report shows the user 3 core findings of this dimension
- Waiting for all four.
- Send the shell_request to 4 Agents by SendMessage

# # Step seven:team-lead composite attribution

Summary of 4 reconnaissance reports, output** and cause of dissipation** (not studies, focus on "judgement"):

---

# 1. A word of attribution
> A statement (30-60) to explain: Main cause of the price variation + Sub-cause + Characteristic (value event/emotion/unknown)

##2. Full event time line (combined 4 dimensions)

Invert all dimensions of events by date:

The date, the dimensions, the events, the sources, the gravity of the activity, the weight of the activity, the weight of the activity, the weight of the activity, the weight of the activity, the weight of the activity, the weight of the activity, the weight of the activity, the weight of the activity, the weight of the activity, the weight of the activity, the weight of the activity, the weight of the activity, the weight of the activity, the weight of the activity, the weight of the activity, the weight of the activity, the weight of the activity, the weight of the activity, the weight of the person, the weight of the person, the weight of the person, the weight, the weight of the person, the weight of the person, the weight, the weight of the person, the weight of the person, the weight, the weight of the person, the weight, the weight of the person, the weight, the weight, the weight, the weight, the nature, the nature of the person, the nature, the person, the name, the name, the name, the name, the name, the name, the name, the name, the name, the name, the name, the name, the the the the name, the name, the name, the name, the the the, the, the the the the the name, the person, the name, the name, the name, the name, the name, the name, the name, the name, the name, the name, the name, the name, the name, the name, the name, the name, the name, the name, the name, the name, the name, the name, the name, the name, the name, the name, the name, the name, the name, the name, the name, the name, the name, the name, the name, the name, the name, the name,
|------|------|------|------|-----------|
<unk> 2026-04-30 <unk> Company <unk> <unk> link <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk>
<unk> 2026-04-29 Industry <unk> Link <unk>
<unk> 2026-04-28 <unk> Emotional <unk> Link <unk> Low <unk>

weight legend: <unk> High (separately enough to explain the variation) / <unk> Medium (part of contribution) / <unk> Low (background noise)

##3. Dissociative attribution table

The answer is no proof of confidence, continuity, continuity.
|---------|------|------|------|--------|
Example: Treasury revenue of 5% below expectations, decrease in Māori rate
The unit dropped significantly more than the industry, and the industry was synchronized with the industry.

##4 Nature judgement (core conclusion)

Check one:

- [ ] **value event**: Real changes in fundamentals (performance, moat, management, final results) requiring a review of investment papers
- [ ] ** Emotional/technology fluctuations**: no change in fundamentals, driven by finance/emotional/Beta, which can be considered as opportunity or noise
- [ ] **Sex unknown**: No event matching the price variation -- ** This is the most dangerous conclusion**, either the market knows what (intel/run) or we miss the source.
- [ ] **Mixed**: Some value event + Partial extenuation

## 5. Summary of reconnaissance of dimensions

The most important discovery of 3-5 dimensions per dimension + the dimension attribution contribution.

6. Recommendations for action

Do you suggest that we do so for reasons?
|------|--------|------|
<unk> Triggering the re-examination of the investment paper (`thesis-tracker ' ) <unk>
<unk> Trigger deep financial review (`/earnings-review ' ) <unk>
<unk> Trigger management retrial (`/management-deep-dive') <unk>
<unk> Rewinding actions (paste/silo/no move) <unk> Just give a hint, and ultimately the decision-making is in the user's hands <unk>
♪ Just watch ♪ ♪ ♪ watch ♪

# # 7. Next 7-30 days of the trail

- [ ] Incidents to be disclosed1 (e.g. 5/15 performance session)
- [ ] Target to be followed 2
- [ ] Key observation signal 3

##8. Information gap statement

An honest list of the questions that the survey failed to resolve, the information that it could not find, and the more disclosed things that need to be disclosed.** Rather mark "unsure" than presumably fill**.

---

# Step eight: Save the report

Write `reports/{corporate name}/{corporate name}-news-{YYYYMMMD}.md ' . Create `reports/{corporate name}/`catalogue if there is no existing (indicate that the company has not yet built any studies).

# Step 9: Cleaning team

Use TeamDelete to clean up team resources.

# Key principles

** Cough is better than the whole** - the core value of this skill is to give a attribution judgement within 10-15 minutes, and not get into deep analysis (as other skills do)
2. ** Attributions prevail over the column** - It is easy to find that an event is worthy of this stock price variation.
3. ** Honest to "unknown"** - When no main cause is found, express "unknown" is more valuable than a hard-fry causal chain.
4. ** No pre-established site** - Do not prefer "it's emotional, nothing." The evidence points to which side.
5. ** Distinguishing "catalyst" from "coincidence"** — Events at the same time are not necessarily the main cause of the heterogeneity, depending on whether the level of impact matches.
** Respect for the availability of information** — Level C company may not be able to find any news, and this conclusion itself is about to be written.
** Guided by the principle of `CLAUDE.md`objectiveness'** - all judgements with data sources, distinguishing between facts and points of view
** Non-decision-making for users** - List of attributions and proposals for action, but decision-making on sales is made by users
