# Before Buffett's value investment is bought

Checklist analysis of $ARGUMENTS before buying Buffett value investments.

** Support input format**: individual or multiple companies separated by comma/Don/space. For example: `Team, Mau, Yveida ' or `NVDA AAPL MSFT '

# Execute process

# Step one: parsing input, identifying all companies to be analysed

Disassemble all company names/codes from $ARGUMENTS. For each firm, determine:
- Company full name, stock code, listed exchange
- If the company is not listed, mark "not listed" and give a brief explanation (if there is an indirect investment route), skip the whole Checklist

# First half: AI studies prejudice warning

A rapid rating of each company for "information abundance" (A/B/C) was noted in the report:

The effect of the test on Checklist.
|------|---------|-----------------|
A.C., years of listing, data availability, normal execution, but beware of the Consensus Trap -- all indicators seem clear and do not mean they're really certain.
The data are limited and the confidence level is marked for each extrapolated indicator, and the weight of "good business" is considered to be the reliability of the data.
<unk> C level, <unk> information is extremely scarce, <unk> not only fill out the six-level form, but honestly label "data is not enough to judge," focus on the core issues that can be verified <unk>

** Core principle**: The goal of the Checklist is to ** exclude bad choices**. For a class C company, "deficit data" does not mean "no pass" or "no pass" -- honestly labeled as "grey area" and requires a first-hand addition of information, not a rejection because AI is unable to fill the form.

And Yongping said, "I don't know." There are two kinds of things -- one that are too complicated to read, one that you haven't spent time with. The only limit of AI research is that it's easy to mix "less information" with "not understanding".

# Step 2: Parallel data collection

Data collection using the Task tool for **Initiating independent backstage for each company** (all companies simultaneously running in parallel), each collecting:

1. ** Profitability**: ROE (trend 5-10 years), Māori rate, net interest rate, free cash flow
2. ** Valuation data**: current stock price, market value, PE(TTM), forward-looking PE, PB, dividends rate
3. ** Growth trend**: Income/profit growth for the last three years
4. **Financial health**: level of liabilities, capital expenditure requirements, cash reserve, net cash/net liabilities
5. **Competition pattern**: market share, major competitors, trends in share changes
** Evidence from the moat**: Specific evidence of branding/conversion costs/network effects/scale effects/technical barriers
7. ** Management records**: CEO ' s curriculum vitae, key decision-making, shareholding, capital allocation records
** Update on developments**: Major events (performance, mergers and acquisitions, controls, management changes, etc.) for nearly six months

# Step three: Six Levels per Company

For each listed company, six steps in line:

---

# First level: Can I understand this business?

The answer must be:
- [ Laughs ] Can you tell me in one sentence what this company is making money for?
- [ Laughs ] What's the business going on in about 10 years?
- [ ] Which key variables determine success or failure?
- [ ] Is the knowledge of this industry from deep research or from hearsay?

** Rating criteria** (pp 1-5):
- <unk> : Business models are extremely simple and clear, with 10 years of certainty (e.g., mashed: wine making and selling)
- <unk> : The model is clear but technically high and requires some expertise to understand
- <unk> : Modes understandable but less certain for 10 years, industry changes fast
- <unk> : Complex lines of business or in a period of industry change, difficult to predict the future
- Q: Not at all in the circle.

** Hard veto**: If not even the way of making money, it is marked as "not in the circle of ability, not analysis".

---

# Second: Is this a good business?

In the words of data,** key indicators must be calculated accurately by means of tools**:

```bash
python3 tools/financial_rigor.py verify-valuation \
--price {equity value} --eps {EPS} --bvps {net assets per share} --fcf-per-share {FCF} --dividend {per dividends}
```

<unk> Indicators <unk> Company values <unk> Reference criteria <unk> Judgement <unk>
|------|-----------|---------|------|
ROE (5-year average) > 15% excellent, > 20% excellent
<unk> Māori ratio > 40% implied pricing rights > <unk>
Free cash flow, constant positive, net profit, and profit.
<unk> Capital expenditure intensity <unk> Light assets are superior to heavy assets <unk>
Level of liability <unk> Interest-bearing liabilities/net profit < 3 years <unk>

** Rating criteria** (pp 1-5):
- <unk> : ROE > 25%, High Mauric, Strong FCF, Light Assets, Low Liabilities (all met)
- <unk> : 4 met
- <unk> : 3 met the target
- <unk> : 2 met or the trend deteriorated
- <unk> : Most of the non-achievements or FCFs remain negative

---

# Third: Is the moat deep enough (competitive advantage)

Checks per item:

Do you have any concrete evidence of the size, width or narrowness of the river?
|-----------|---------|---------|--------------|
Brand/pricing authority
<unk> Conversion costs
<unk> Network effects<unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk>
Cost/scale advantage
Technical/proprietary barriers

Additional test: If 10 billion dollars were given to competitors, could this business be replicated?

** Rating criteria** (pp 1-5):
- <unk> : Multiple moats and rivers are folding and growing wide
- Pyro: at least one strong moat and stable
- <unk> : There are moats but not deep enough or trends are unclear
- Xiao: The moat is being eroded.
- <unk> : No visible moat

---

# # # level four: Is management trustworthy?

<unk> Check item <unk> Evaluation <unk>
|--------|------|
<unk> Integrity (Commitment vs. Delivery) <unk>
• Capital allocation capacity (repurchase/record/merger and acquisitions records)
• Shareholder-oriented (shareholding, remuneration)
<unk> Owner mentality (founder vs career manager) <unk>
Corporate governance (associated transactions, goodwill, auditing)
Can the CEO run as usual after he leaves?

** Rating criteria** (pp 1-5):
- The founder has the helm, the capital is well-capitalized and the interests are fully consistent
- Pyramid: Management is good but has a slight flaw
- <unk> : qualified management but with governance concerns
- • Probity or governance issues
- Question of serious integrity (hard veto)

---

# # Fifth: Is the price cheap enough (security margin)

<unk> Indicators <unk> Value <unk> History Division <unk> Judgement <unk>
|------|------|---------|------|
| PE (TTM) | | | |
♪ The way I see it ♪
| PB | | | |
♪ The rate of dividends ♪
| FCF Yield | | | |

Additional tests (** must be calculated accurately by tool, inhibit the heart **):
```bash
python3 tools/financial_rigor.py three-scenario \
- Price {shares }-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
{\-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-----0-0----------0-0-0-0-----0-0-0-0-------------------
```
- Valuation interval under three scenarios (retrieving tool output results)
- If the judgement is wrong, what is the maximum loss on the current price?
- You dare to slash your arm?

** Rating criteria** (pp 1-5):
- <unk> : a relative intrinsic value of less than 50%, extreme security margin
- Xiaoqin: 70% discount, good security margin.
- <unk> : reasonable valuation, security margin average
- Qui: Precious, security marginal.
- <unk> : severe overestimation

---

# # Sixth level: Position and decision discipline (prevent mood loss)

Check the following emotional signals:
- Is it because FOMO wants to buy it?
- Is it because someone else recommended?
- If you've been out for five years, can you accept it?
- Can the buyout be written in 200 words?

---

# Step four: mirror test

The mirror test statement for each company:

> "I bought the company in _$<unk> because:
1. The essence of this business is ___, and I understand it;
> 2. Its moat is ___ and is wide/shrunk;
> 3. Management __, worthwhile/not trustworthy;
> 4. Current prices equal to _ discounts of intrinsic value, with/without sufficient security margins;
5. Even if I am wrong, downside risks are manageable/uncontrollable because ___."

** 5 sentences say incomplete = not bought.** Clear label "through" or "not through".

---

# Step five: fast-tracked list

Each company is examined article by article, triggering any direct label of "no":

- [ Laughs ] I don't know how this company makes money.
- [ ] Free cash flow is negative for three years without any improvement.
- [ ] Management has a reputation.
- [ ] The competitive advantage is being irreversibly eroded.
- [ Laughs ] It's gonna take the next picker to make money.
- [ ] Can't bear the consequences of zero investment.
- [ Laughs ] The main reasons for buying are "others are buying" or "good ups lately."
- [ ] Can't spell out the reasons for the purchase in 200 words.

---

# Step 6: Output Summary Comparison Table (Multi-company output)

When analysing multiple companies, a comparative overview must be generated:

The company, the Checklist, passed through the power circle, the good business, the moat, the management, the security margin, the core conclusion.
|------|----------------|--------|--------|--------|--------|---------|---------|
| | | ★☆☆☆☆ | ★☆☆☆☆ | ★☆☆☆☆ | ★☆☆☆☆ | ★☆☆☆☆ | |

---

# Step seven: Final conclusions and writing

Make clear conclusions for each company (no avoidance):
- <unk> through Checklist** (X/6) - can enter the advanced research phase
- <unk> not through Checklist** - Which red line is triggered
- <unk> ** Gray ** ** ** – what the key points of contention are, what investors need to judge for themselves
- N/A - Unlisted/not available

Write the full report to `~/Buffett Checklist-[name or "multi-comparison of companies"].md`

# Output format requirements

1. Each company has a separate chapter containing: six-point score sheet + core data sheet + key risks (3-5 articles) + mirror tests + clear conclusions
2. Multi-firm comparisons at the end of the summary
3. All ratings must be given using a glimmer (<unk> 1-5) and not containing half a star
4. Data must be marked at the source time and estimates must indicate "estimate"
5. The last sentence is a closing phrase echoing the quote of Buffett: "The first rule of investment is not to lose."
Language style: Direct, sharp, no bullshit.

# Key principles

- ** Better to miss, do not make mistakes**: The goal of Checklist is to rule out bad choices than to find the best.
- ** Honesty to the circle of ability**: I don't understand, I don't understand, don't try to analyze.
- ** The security margin is the lifeline**: good companies buy money and lose money.
- ** Mirror test cannot skip**: no one buys it for no reason, no exception.
