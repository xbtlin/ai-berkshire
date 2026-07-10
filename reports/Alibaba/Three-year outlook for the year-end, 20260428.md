# Qianwen App Three-Year Outlook (2029) Comprehensive Research Report

> **Research framework**: Four investment-research roles working in parallel (Duan Yongping business model / Buffett financial resources / Munger industry structure / Li Lu management and risk)
> **Research date**: 2026-04-28
> **Research subject**: Qianwen App (Alibaba's AI assistant, formerly the consumer Tongyi Qianwen product)
> **AI researchability rating**: **B leaning C** -- data is available, but standalone App financials are not separately disclosed, and three-year extrapolation is highly uncertain

---

## 0. One-Sentence Core Conclusion

**Qianwen App is the flagship consumer gateway under Eddie Wu's "All-in AI" strategy, personally sponsored by the CEO and backed by RMB 380 billion of Capex (3800 in RMB 100 million units) -- the probability it is cut within three years is extremely low (<10%). But (a) average monthly uses per user are only 36% of Doubao's (19.8 vs 54.8 times), (b) retention fell by half to below 50% after RMB 3 billion (30 in RMB 100 million units) was spent during Spring Festival, (c) the 2026-03 departure of large-model lead Lin Junyang triggered turbulence in the core model team, and (d) the organization was adjusted 6 times within one year. The most likely position three years from now is "solid number two, unlikely number one, and further integrated with Quark or folded into cloud-business reporting." From Duan Yongping's perspective, this is not a good business (differentiation 3 / pricing power 1 / sustainable advantage 2), but as a "must-win battle" in Alibaba's AI strategy, it will inevitably keep receiving capital and executive attention.**

---

## 0.5 Source Statement and Researchability Limits

This report was produced by 4 independent sub-agents working in parallel. 3 used WebSearch (covering 2025Q4 - 2026Q1 earnings reports, third-party rankings, media reports, and official announcements), and 1 relied on public-information memory and reasoning (industry-structure section). All data points are source-labeled and confidence-rated in the sub-reports. The key figures in this integrated report are high- or medium-confidence.

**Limitations that must be stated plainly**:
- Qianwen App's standalone P&L, paying users, and internal KPIs have **never been publicly disclosed** by Alibaba
- Qianwen App MAU has two methodologies: Alibaba's official ~300 million (~3 hundred million, including Web/embedded calls) vs QuestMobile's 166 million (1.66 hundred million, standalone App MAU). This report uses QuestMobile when comparisons are needed
- Three years is an extremely long forecasting horizon in AI (foundation models iterate roughly every half year). All 2029 judgments are **inherently low-confidence** and should be recalibrated every 6 months
- No Chinese AI application has been listed, spun off, or independently valued. All "business-unit valuations" are inferred estimates with no market precedent

---

## 1. What Qianwen App Is

### 1.1 Three-Layer Positioning

| Layer | Positioning | Status |
|---|---|---|
| Foundation layer | Conversational / writing / vision assistant powered by Qwen3-Max-Thinking (benchmarking Doubao and ChatGPT) | Model has entered the global top-three cohort |
| Middle layer | Task-completion Agent, connected on 2026-01-15 to Taobao, Taobao Instant Commerce, Alipay, Fliggy, Amap, and 400+ services | World's first native AI assistant with a closed-loop transaction capability |
| Top layer | Alibaba Group's consumer AI strategic gateway + ecosystem orchestration hub | Unified as the Group's master AI brand on 2026-03-02 |

### 1.2 Position in Alibaba's AI Matrix (Status as of 2026.04)

```
Alibaba Token Hub (ATH, established 2026-03-16)
├── Tongyi Lab (Jingren Zhou) -- model R&D
├── MaaS business line -- model APIs / compute allocation
└── Qianwen Business Unit, Wukong Business Unit (video), AI Innovation Business Unit

Qianwen consumer business group (Jia Wu, established 2025-12-09)
├── Qianwen App (core consumer gateway)
├── Quark (AI search / browser, 200 million+ MAU, or 2 hundred million+)
├── UC, Shuqi (traffic base)
├── Tmall Genie (hardware gateway)
```

One subtle point: **Qianwen App is simultaneously influenced by ATH and the Qianwen consumer business group** -- ATH manages models and commercialization, while the Qianwen consumer business group manages user products. This kind of "dual reporting line" is common in Alibaba's history and carries a high coordination cost.

### 1.3 Relationship with Alibaba's Other AI Products

- **vs Quark**: Quark's 200 million+ MAU (2 hundred million+) provides traffic for "AI search + utility scenarios," while Qianwen App provides a "general AI assistant + task-completion Agent." The internal narrative is a closed loop of "Quark drives traffic -> Qianwen completes tasks -> data flows back -> models improve." But multiple media outlets, including 21st Century Business Herald and CBNData, have clearly raised the question of "complementary or cannibalizing." **Over the medium to long term, the probability that one side is merged or downgraded is high**
- **vs Tongyi API / MaaS**: They share the underlying Qwen models, but API revenue is booked under Cloud Intelligence Group (FY26Q3 quarterly revenue of RMB 43.284 billion, or 432.84 in RMB 100 million units) and does not cross-account with the App
- **vs DingTalk AI**: Enterprise collaboration AI, operated independently
- **vs Taobao/Alipay AI assistants**: Qianwen App connects to and invokes them -- Qianwen is the entry point, while Taobao/Alipay are dispatched services

---

## 2. Current Data Profile (2026Q1 Snapshot)

### 2.1 Key Operating Data

| Metric | Qianwen App | Doubao | DeepSeek | Yuanbao | Kimi |
|---|---|---|---|---|---|
| MAU | 166 million (1.66 hundred million, QuestMobile) / ~300 million (~3 hundred million, Alibaba official methodology) | **345 million** (3.45 hundred million) | 127-170 million (1.27-1.7 hundred million) | 41.64 million (4164 x 10,000) | Ranked around 6th, already falling behind |
| Global AI app MAU ranking | Third (surpassing Gemini) | Second (behind only ChatGPT) | Fourth | -- | -- |
| Average monthly uses per user | **19.8 times** | **54.8 times** (2.7x gap) | Relatively high | -- | -- |
| Spring Festival DAU peak | 73.52 million (7352 x 10,000) | 145 million (1.45 hundred million) | -- | -- | -- |
| Post-Spring Festival steady-state DAU | 30-40 million (3000-4000 x 10,000; fell to 32.45 million, or 3245 x 10,000, on 2-23) | Already above 100 million steady-state | -- | -- | -- |
| Retention rate (Spring Festival peak -> steady state) | **<50%** | Relatively high | -- | -- | -- |
| Marketing acquisition cost (per DAU) | **¥144** | Extremely low (embedded in Douyin) | Extremely low (word of mouth) | -- | Shifted to B-end after burning through ¥540 million/year (5.4 in RMB 100 million units) |
| Commercialization progress | Almost no direct monetization; Jia Wu said "commercialization is not the priority" | Not monetizing for now, competing for scale | API priced extremely low, no consumer commercialization | WeChat ecosystem traffic | Shifted to B-end |

> **Core insight**: Qianwen appears to be catching up with Doubao on MAU, but the **2.7x gap in average monthly uses per user** is structural. It means Doubao users have already formed a habit of "opening it as part of daily life," while most Qianwen users are still in a "low-frequency / occasional / summoned by red packets" state.

### 2.2 Alibaba AI Business Financial Profile (FY26Q3, as of 2025-12-31)

| Metric | Value | YoY | Confidence |
|---|---|---|---|
| Group total revenue | RMB 284.8 billion (2848 in RMB 100 million units) | +4.8% | High |
| Cloud Intelligence Group revenue | RMB 43.284 billion (432.84 in RMB 100 million units) | +36% | High |
| AI-related product revenue growth | **Triple digits** | **10 consecutive quarters** | High |
| Non-GAAP net profit | ~US$2.2 billion (22 in US$100 million units) | -66% | High |
| FY26Q1 quarterly Capex | RMB 38.676 billion (386.76 in RMB 100 million units) | **+220%** | High |
| Cumulative AI+cloud Capex over past 4 quarters | ~RMB 120 billion (1200 in RMB 100 million units) | -- | High |
| Cumulative T-Head self-developed GPU deliveries | **470,000 chips** (47 x 10,000 chips) | -- | High |
| Three-year AI infrastructure investment commitment | **RMB 380 billion** (3800 in RMB 100 million units; Eddie Wu called it "conservative") | -- | High |
| 5-year cloud+AI commercialization revenue target | **US$100 billion** (1000 in US$100 million units) | CAGR ~47% | High |
| Group free cash flow (FY2025) | ~RMB 150 billion (1500 in RMB 100 million units) | -- | High |
| Cash + short-term investments on balance sheet (2025-12-31) | ~RMB 550 billion (5500 in RMB 100 million units) | -- | High |
| Estimated annual cash burn for Qianwen App | RMB 11-14 billion (110-140 in RMB 100 million units) | **7-10%** of Group FCF | Medium |

---

## 3. Four-Dimension Integrated Scorecard

| Dimension | Framework | Score | Core judgment |
|---|---|---|---|
| **Business model** | Duan Yongping | ⭐⭐ (2.0/5) | Not a good business: differentiation 3 / pricing power 1 / sustainable advantage 2. But as Alibaba's "must-win battle," it will inevitably receive sustained investment |
| **Financials/resources** | Buffett | ⭐⭐⭐⭐ (4.0/5) | Extremely high resource safety (CEO priority + Capex called "conservative"); probability of being cut within three years is 15-20%; but the commercialization ceiling is unclear |
| **Industry structure** | Munger | ⭐⭐⭐ (3.0/5) | Stable second tier, unlikely number one. **The real killer is not DeepSeek, but WeChat/Douyin/system-level AI pulling the rug out from under standalone apps** |
| **Risk and management** | Li Lu | ⭐⭐ (2.5/5, B-) | Poor strategic consistency (6 organizational adjustments in one year), the Lin Junyang episode exposed route conflict, and Alibaba's record with "non-core-but-not-dead" businesses is not friendly |
| **Integrated** | -- | ⭐⭐⭐ (2.9/5) | Strategic-level business, but not a good business; resources are ample, but monetization is unproven and organizational risk is high |

**Horizontal management-score comparison**: DeepSeek's Liang Wenfeng A / ByteDance's Liang Rubo A- / Tencent's Pony Ma and Allen Zhang A- / Alibaba's Eddie Wu **B+** / Baidu's Robin Li C+

---

## 4. Core Findings by Dimension

### 4.1 Business Model (Duan Yongping Perspective)

**Duan Yongping asks, "What unchanging thing can you use to beat it within five years?" For Qianwen App, the truly "unchanging" moat is Alibaba's e-commerce ecosystem itself, not the AI model.**

- **Seven-dimensional moat test**:

| Dimension | Assessment | Explanation |
|---|---|---|
| Brand | Medium | "Qianwen/Qwen" has strong awareness among developers; consumer awareness of "Qianwen" only began scaling after Spring Festival |
| Data | Medium-high | Alibaba's e-commerce + Amap + Alipay behavioral-data loop has major potential, but current model training mainly relies on open-source data |
| Network effects | Weak | AI assistants are fundamentally 1-to-1 tools; network effects arise only indirectly when Agents invoke the e-commerce ecosystem |
| Switching costs | **Weak** | Users can switch at zero cost; the product is free and has no social graph deposits |
| Scale effects | Medium-high | Inference compute cost amortizes as users grow, but model gaps of <6 months can be closed by competitors |
| Technology | Medium | Qwen3-Max is in the global top three, but remains at a "same generation, slightly behind" level versus GPT-5/Claude Opus 4.5/Gemini 3 Pro |
| **Ecosystem distribution** | **High** | **The only true moat**: invoking Taobao/Alipay/Amap/Fliggy cannot be frictionlessly replicated by ByteDance/Tencent |

- **Key judgment**: Qianwen's moat is "borrowed from" Alibaba's e-commerce ecosystem. If e-commerce remains strong, Qianwen is strong. If e-commerce continues to be eroded by Pinduoduo/Douyin, Qianwen is impaired in parallel. **This is not an independently good business; it is Alibaba e-commerce's "AI defensive fortification"**

- **Spring Festival "RMB 3 billion free-order" postmortem**: Per-DAU acquisition cost was ¥144 (industry benchmark ¥10-15), and retention was <50% after 17 days. Users bought through subsidies are not users; they are arbitrageurs

### 4.2 Financials/Resources (Buffett Perspective)

**Core judgment: Qianwen App team = "high resource safety + medium probability of wealth realization"**

- **Absolutely no problem over the next three years**: Qianwen App burns RMB 11-14 billion (110-140 in RMB 100 million units) per year, only 7-10% of Group free cash flow. With RMB 550 billion (5500 in RMB 100 million units) of cash + short-term investments on the balance sheet, the burn is small enough to be covered by less than one quarter's net-profit decline
- **Eddie Wu's tolerance for Qianwen App is extremely high**: Jia Wu publicly stated that "commercialization is not the priority for Qianwen, and major versions will iterate every quarter" -- implying Qianwen App will not be cut for "losses" over the next 2 years
- **But Alibaba's CEO is not Buffett**: He is a "Bezos + Jensen Huang" hybrid (capital intensive, long-cycle, indifferent to short-term ROI). Calling RMB 380 billion (3800 in RMB 100 million units) "conservative" is offensive language, not defensive language

#### Three-Year Scenario Valuation (2029)

| Scenario | Probability | Direct ARR | PS multiple | Business-unit valuation | Trigger conditions |
|---|---|---|---|---|---|
| Bull | 20% | RMB 16 billion (160 in RMB 100 million units) | 6-8x | **RMB 80-130 billion** (800-1300 in RMB 100 million units) | MAU 350 million+ (3.5 hundred million+), subscription rate above 2%, self-operated AI e-commerce works; spin-off or independent financing |
| **Base** | **55%** | RMB 5 billion (50 in RMB 100 million units) | 3-5x | **RMB 15-25 billion** (150-250 in RMB 100 million units) | As part of Alibaba's AI matrix, **no independent valuation**, folded into cloud or Quark system |
| Bear | 25% | RMB 700 million (7 in RMB 100 million units) | 1-2x (cost center) | No independent valuation | MAU stagnates, suppressed by Doubao, merged into Quark or dissolved into a model-to-B team |

#### Industry-Level Truth
**No domestic AI App has achieved a "meaningful independent valuation breakout"**: Doubao is not being spun off, Kimi's valuation has already declined, and Moonshot AI is facing strategic difficulty. This is an industry-wide phenomenon, not a Qianwen-specific problem. **It means Qianwen App's valuation will not be separately marked by the market; it will be wrapped into the Alibaba Cloud story**.

#### Red-Line Triggers (15-20% Probability of "Cutting the Business")
1. User growth stalls + Doubao MAU widens to more than 4x Qianwen's (currently 2x)
2. Group free cash flow turns negative for two consecutive quarters (e-commerce bleeding + instant-commerce subsidies + AI spending all at once)
3. Eddie Wu steps down or strategy shifts materially (he has served 2 years; CEO tenures are often 3-5 years)

### 4.3 Industry Structure (Munger Perspective)

**Core judgment: By 2029, the Chinese general-purpose AI assistant App market will likely converge to 2-3 players (Doubao + one open-source camp + one system-level camp). Qianwen App sits in the upper second tier and could be absorbed into Alibaba's internal ecosystem at any time.**

#### Three Main Evolution Drivers

**(1) Technology-driven**: Foundation-model gaps are narrowing. The China-US gap in 2026 is roughly 6-12 months and will likely compress to 3-6 months by 2029. Models themselves will no longer be the barrier; application layer, ecosystem, and distribution will decide the outcome. The open-source camp is winning (DeepSeek/Qwen have already forced closed-source players to cut prices by 97%).

**(2) Form-factor-driven** (key): By 2029, **70% of AI interactions will occur in "non-standalone AI App" scenarios**:
- **WeChat AI entry point** (largest threat): In 2026, it was already testing "Ask." If Tencent truly commits, it can instantly access a billion-level user base
- **Embedded in Douyin** (already happening): Doubao is deeply embedded in Douyin
- **Apple Intelligence China version**: 2026 rumors pointed to Baidu as exclusive partner or a dual-supplier model. **If Qianwen wins Apple cooperation = life-extension package; if not = loss of important distribution**
- **Huawei / Xiaomi / vivo / OPPO system-level AI**: Hardware distribution is the ultimate killer advantage

**(3) Regulation and ecosystem**: Filing/registration becomes normalized (stricter but not suffocating), content safety remains under persistent pressure, data-export and training-data compliance audits become stricter, and overseas AI structurally exits China's consumer market.

#### Inverting the Problem: How Qianwen App Could Disappear

| Scenario | Probability | Trigger conditions |
|---|---|---|
| **A. Internally "folded" by Alibaba Group** | **35%** | Eddie Wu/Joe Tsai judge ROI as low and sink Qianwen capabilities into Taobao/Quark/DingTalk/Amap, closing the standalone App entry point. **Historical precedents**: Xiami, Laiwang, Koubei, etc. |
| B. WeChat/Douyin/system AI pulls the rug out | 30% | In 2027, WeChat "Ask" or Douyin AI rolls out at scale, making standalone Apps less necessary |
| C. Falls behind technically across generations | 10% | Qwen clearly falls behind DeepSeek/Doubao in a 2027 model-generation contest |
| D. Cut after commercialization failure | 5% | In 2028, Alibaba management requires AI businesses to prove ROI, and the consumer App cannot find a paid model |
| E. Merged | 10% | Merges with Quark/Zhipu in some form |
| F. Black swan | 10% | Regulatory shock, key executive departure, another major Alibaba reorganization |

> **Summary**: The combined probability that Qianwen App's "standalone App form disappears" is about 25-30%. **The biggest killer is not DeepSeek, but Alibaba's own internal strategic swing + ecosystem pressure from WeChat/Douyin/system-level AI**.

#### Historical Analogy Takeaways

- **Analogy 1 (worst case)**: Mobile IM war -> WeChat consumed everything. If WeChat takes AI seriously, Qianwen dies
- **Analogy 2 (base case)**: Search market -> Baidu dominates but is diverted by other entry points. Qianwen may be fragmented by scenarios, but will not die
- **Analogy 3 (most instructive)**: Map App war -> Amap/Baidu Maps coexist as a duopoly + are embedded inside super apps. **Qianwen App's most likely position in three years = "Baidu Maps in the map war" -- still present, but no longer independently growing**

### 4.4 Risk and Management (Li Lu Perspective)

**Core judgment: Jia Wu is one of Alibaba's few post-1985 managers with a successful consumer AI track record, but the underlying model team has just experienced severe turbulence after the departure of core lead Lin Junyang, and the product-side root problem of "not retaining users" has not yet been proven solved.**

#### Key-Person Profiles

| Person | Position | Key judgment |
|---|---|---|
| **Eddie Wu** | Alibaba Group CEO + Alibaba Cloud CEO | One of the 18 founders, the first programmer, 7 years as a VC (150+ projects). A "Bezos + Jensen Huang" true believer in AI, personally approving RMB 380 billion. Integrity B+ (messaging is consistent, but strategic statements are frequently escalated; AGI -> ASI has a headline-grabbing feel) |
| **Jingren Zhou** | Alibaba Cloud CTO + head of Tongyi Lab | Columbia PhD, 11 years at Microsoft Research, IEEE Fellow. Promoted to partner in 2025-12 (very strong political signal), appointed Group Chief AI Architect in 2026-04. Scholar-manager who prefers "industrialized large-army operations" -- the key background to the route conflict with Lin Junyang |
| **Jia Wu** | President of Qianwen consumer business group (post-85, appointed 2025-12-09) | Zhejiang University master's, 16 years at Alibaba, core builder of Quark (200 million+ MAU, or 2 hundred million+, track record). **The most reassuring variable** -- probability of replacement within three years <15%. But Quark succeeded under a "search + utility" logic, while Qianwen needs a "general assistant + ecosystem orchestration" logic; the underlying product philosophies differ substantially |
| **Lin Junyang** | **Former Qianwen large-model lead** (departed 2026-03-04) | Youngest P10, the soul of the Qwen open-source narrative. **Nuclear-level departure**: Alibaba required the Qwen team to move from "vertical integration" to "horizontal division of labor"; Lin did not accept the split of authority and responsibility and left, announcing it himself on X in the early hours of March 4 |

#### Historical Losses of Key Talent

| Time | Person | Former position | Destination |
|---|---|---|---|
| 2024.07 | Chang Zhou | Core member of Tongyi large-model team | ByteDance (4-2 level, 8-figure annual package) |
| 2025.02 | Zhijie Yan | Head of Tongyi Lab speech team (P10) | Tencent -> JD Explore Academy |
| 2025.06 | Liefeng Bo | Head of Tongyi application vision team (P10) | Tencent Hunyuan |
| **2026.03.04** | **Junyang Lin** | **Qianwen large-model lead (P10)** | **Undisclosed (speculated overseas or independent startup)** |

> Multiple core members left in succession after the Lin event. **Qianwen's technical core team is in a "collective reconstruction" phase in 2026, and the colleagues one meets on joining may look completely different six months later**.

#### 6 Organizational Adjustments Within One Year (Strong Yellow-Flag Signal)

1. End-2024: Tongyi To C team was separated from Alibaba Cloud and folded into Jia Wu's Intelligent Information business group
2. 2025-09: Eddie Wu decided Alibaba "must build an AI-native consumer super entry point," transferring hundreds of engineers from Beijing/Guangdong
3. 2025-11-17: Tongyi App renamed "Qianwen"
4. 2025-12-09: Qianwen consumer business group established (led by Jia Wu)
5. 2026-03-04: Lin Junyang departed, triggering reorganization of the underlying model team
6. 2026-03-16: ATH business group established

> This is extremely intense organizational turbulence. **Li Lu values strategic consistency most, and Alibaba clearly loses points here**.

#### Three-Year Organizational Risk Scenarios (Ranked by Probability)

| Scenario | Probability |
|---|---|
| **A. Qianwen App merges with Quark, standalone App closes, and everything is unified under Quark or a new brand** | **35-40%** |
| **B. Jia Wu changes roles or is replaced; Qianwen changes leadership** | 20-25% |
| **C. Qianwen consumer business group is folded into Alibaba Cloud or ATH; independent business group disappears** | 25% |
| **D. Alibaba's overall strategy pivots and AI investment is reduced** | 10-15% |
| **E. Continued loss of key talent hollows out the team** | **45-50% (high certainty)** |
| **F. Qianwen App is cut and the standalone App is shut down** | <10% |

> **A+B+C together exceed 70%** -- meaning organizational change is highly likely over the next three years, while F (complete shutdown) remains very unlikely.

---

## 5. Key Event Timeline + Three-Year Inflection-Point Forecast

### 5.1 Historical Review (2024 - 2026.04)

| Time | Event | Significance |
|---|---|---|
| 2023-09 | Eddie Wu concurrently became Alibaba Cloud CEO | Starting point of the All-in AI strategy |
| Full-year 2024 | Tongyi To C team was "sidelined" for a year | Model became famous, but the App stayed obscure |
| End-2024 | Tongyi To C was folded into Jia Wu's Intelligent Information business group | Product operator identified |
| 2025-02-24 | Eddie Wu announced RMB 380 billion (3800 in RMB 100 million units) of AI Capex | Largest AI infrastructure investment by a Chinese private enterprise |
| 2025-09 | Apsara Conference narrative: "ASI is the destination" | Strategic narrative escalated |
| 2025-11-17 | Tongyi App renamed "Qianwen" | First step in brand unification |
| 2025-12-09 | Qianwen consumer business group established (led by Jia Wu) | Independent business group + direct owner |
| 2025-12 | Jingren Zhou became an Alibaba partner | AI obtained formal representation in the highest decision-making layer |
| 2026-01-15 | Qianwen connected to Taobao / Instant Commerce / Alipay / Fliggy (400+ services) | "AI task completion" narrative entered implementation |
| 2026-02 | Spring Festival RMB 3 billion (30 in RMB 100 million units) free-order marketing war; DAU peaked at 73.52 million (7352 x 10,000) | Industry-wide subsidy war; retention <50% |
| **2026-03-02** | **Qianwen unified as the Group's master AI brand** | **Brand and organization unified** |
| **2026-03-04** | **Lin Junyang departed** | **Nuclear-level technical-talent loss** |
| 2026-03-16 | ATH business group established | Model + commercialization integration |
| 2026-03-19 | Eddie Wu announced 5-year US$100 billion target (1000 in US$100 million units) | Long-term numeric commitment |
| 2026-04 | Jingren Zhou appointed Group Chief AI Architect | Technical command system tightened |

### 5.2 Three-Year Key Inflection-Point Forecast (Events Deciding Qianwen's Fate)

| Time window | Key event | Impact on Qianwen |
|---|---|---|
| **2026Q3-Q4** | Whether WeChat's "Ask" AI entry point rolls out at scale | Determines survival space for standalone AI Apps |
| First half of 2027 | Apple Intelligence China version formally determines suppliers | Qianwen winning Apple cooperation = life-extension package |
| 2027 | Results of reasoning-model / Agent-model generation competition | Whether Qwen flagship catches DeepSeek/Doubao |
| Full-year 2027 | Boundary-integration event between Qianwen and Quark (merger / further division of labor) | Determines whether standalone App form continues |
| 2028 | Inflection point in maturity of on-device models | Whether system-level AI consumes standalone App traffic |
| 2028-2029 | Alibaba Group's next organizational adjustment / whether Eddie Wu stays | Internal status of the Qianwen business |

---

## 6. Three-Year Scenario Analysis (Integrated)

### 6.1 Integrated Three-Scenario Table (2029)

| Scenario | Probability | Qianwen App form | Key data | Business-unit valuation | Trigger conditions |
|---|---|---|---|---|---|
| **Bull** | **20-25%** | Standalone App + co-leader with Doubao | DAU 150-200 million (1.5-2 hundred million), MAU 500-600 million (5-6 hundred million), own revenue RMB 10-20 billion (100-200 in RMB 100 million units) | RMB 80-130 billion (800-1300 in RMB 100 million units) | (1) Qwen stays in global top three; (2) "AI task completion" becomes a high-frequency habit, and AI e-commerce GMV accounts for ≥10% of Taobao; (3) Alibaba e-commerce defends share; (4) Douyin/Doubao fails to integrate local services |
| **Base** | **50-55%** | "Qianwen = Alibaba's Bing" -- stable number two, folded into cloud or Quark system | DAU 50-100 million (5000 x 10,000 to 1 hundred million), MAU 300-400 million (3-4 hundred million); own ARR <RMB 5 billion (<50 in RMB 100 million units), main value is feeding back into the Group | RMB 15-25 billion (150-250 in RMB 100 million units; not marked separately by the market) | (1) Qwen remains first tier but not leading; (2) AI e-commerce gains penetration, but users still treat AI as an auxiliary tool; (3) Spring Festival-style promotions preserve ranking but produce only moderate retention |
| **Bear** | **20-25%** | "Qianwen = Alibaba's Wenxin Yiyan" -- downgraded / merged with Quark / standalone App marginalized | DAU <30 million (<3000 x 10,000), MAU <150 million (<1.5 hundred million); no longer operated independently | No independent valuation | (1) Qwen model falls behind generationally; (2) ByteDance succeeds in integrating Doubao with Douyin e-commerce; (3) Alibaba e-commerce is further eroded; (4) regulation restricts AI e-commerce traffic routing; (5) internal resource competition within the Group |

### 6.2 Expected-Value Estimate

Probability-weighted "Qianwen App business-unit expected valuation":
- Bull RMB 105 billion (1050 in RMB 100 million units) x 22% + Base RMB 20 billion (200 in RMB 100 million units) x 52% + Bear 0 x 26% ≈ **RMB 33.5 billion** (335 in RMB 100 million units)

But this figure is for reference only. **There is no domestic precedent for independent AI App valuation**. The most realistic interpretation is that "Qianwen App's valuation will be wrapped into Alibaba Group's overall rerating."

---

## 7. Investment Thesis (Bull vs Bear)

### 🟢 Bull Case (7 Points)

1. **CEO-level project, will not be cut within 3 years**: Qianwen App's cash burn is only 7-10% of Alibaba Group FCF; RMB 380 billion Capex (3800 in RMB 100 million units) is described as "conservative"; cash + short-term investments total RMB 550 billion (5500 in RMB 100 million units) -- very high resource safety
2. **Ecosystem orchestration is structural differentiation**: The frictionless transaction loop across Alibaba + Amap + Fliggy + Alipay is a moat ByteDance/Tencent cannot replicate in the short term (Doubao can chat but must jump to third parties; Qianwen can complete tasks directly)
3. **470,000+ T-Head self-developed GPUs (47 x 10,000+), with substantial room for unit inference-cost declines**: Alibaba has a structural cost advantage versus peers
4. **Qwen is in the global top open-source cohort**: >300 open-source models, 600 million downloads, 170,000 derivative models -- strong technology brand
5. **MAU has already reached global number three, surpassing Gemini**: Going from zero to this level in 6 months demonstrates Alibaba's execution capability
6. **Jia Wu is one of Alibaba's few product leaders with practical consumer AI experience**: Quark's 200 million+ MAU (2 hundred million+) is a real track record
7. **5-year US$100 billion cloud+AI commercialization target** (1000 in US$100 million units): CAGR 47%; if achieved, Alibaba will be rerated as a whole, and Qianwen benefits

### 🔴 Bear Case (7 Points)

1. **Average monthly usage frequency is only 36% of Doubao's** (19.8 vs 54.8 times): MAU is close, but the **structural engagement gap is enormous** -- more dangerous than the MAU gap
2. **Post-Spring Festival retention fell by half to <50%**, with per-DAU acquisition cost of ¥144 vs industry benchmark ¥10-15: Users bought through subsidies are not users; they are arbitrageurs
3. **Lin Junyang departed + Chang Zhou/Zhijie Yan/Liefeng Bo outflows**: The underlying model team is in severe turbulence; colleagues in 2026 may look completely different in 2027
4. **6 organizational adjustments in one year** (separate -> merge in -> rename -> Qianwen consumer business group -> ATH -> Lin event): Strong yellow-flag signal under Li Lu's framework
5. **WeChat / Douyin / Apple / Huawei system-level AI could pull the rug out**: By 2029, 70% of AI interactions may occur in "non-standalone AI App" scenarios
6. **Alibaba's historical handling of "neither-core-nor-dead" businesses is severe**: Xiami shutdown, UC marginalization, devastating failure in digital media and entertainment, Cainiao spin-off valuation below expectations, long-term losses in local services. Once KPIs are missed, merger/downgrade is almost inevitable
7. **No domestic AI App has an independent valuation precedent**: Doubao is not being spun off, Kimi's valuation is down -- Qianwen App will not be separately marked by the market; its option value is tied to Alibaba Group's overall rerating, not the business unit itself

---

## 8. Key Uncertainties (Hard to Resolve but Material to the Conclusion)

1. **Can AI Agents really become the high-frequency default entry point?** -- Current data (post-Spring Festival retention <50%) does not yet prove user habits have formed. If users ultimately treat AI only as "a tool used occasionally," Qianwen's "task-completion" narrative collapses
2. **Will WeChat truly decide to build an AI entry point?** -- Tencent's historical "internal horse-racing + conservatism" toward its own products may make AI entry-point rollout slower than expected. This is the largest single-point uncertainty
3. **Final choice for the China version of Apple Intelligence** -- Baidu exclusive vs dual suppliers vs three-party routing implies very different outcomes for Qianwen
4. **Will DeepSeek build a consumer App?** -- Liang Wenfeng currently says clearly that it will not, but three years is enough time to change one's mind
5. **Can the Qwen model remain global top three in 2029?** -- OpenAI/Google/Anthropic capabilities may move another generation ahead over three years; whether the gap between closed-source SOTA and open source widens is unknown
6. **Speed of Douyin e-commerce + Doubao counterattack** -- If ByteDance builds a loop of "AI recommendation + video seeding + order placement" through livestream/video feeds, it may fit Chinese user habits better than Qianwen's "conversation + order placement"
7. **Alibaba e-commerce base** -- Qianwen's moat is essentially Taobao/Instant Commerce/Alipay. If e-commerce continues to be eroded by Pinduoduo + Douyin, Qianwen's "task-completion" value is impaired in parallel
8. **Whether Eddie Wu remains CEO over the next three years** -- He has served 2 years; CEO tenures are often 3-5 years. If he leaves, the weakening effect of the "committee system" on AI resource allocation would quickly rebound

---

## 9. Alibaba Group Stock Perspective (Qianwen's "Investment Significance")

Qianwen App cannot be valued independently, but as Alibaba Group's "AI entry-point option":

- **Positive contribution**: (1) Consumer engine for the 5-year US$100 billion cloud+AI commercialization target (1000 in US$100 million units); (2) traffic flywheel for cloud/e-commerce/Alipay (conservative estimate of annual GMV RMB 7.5 billion, or 75 in RMB 100 million units, and monetization of RMB 1.5-2.5 billion, or 15-25 in RMB 100 million units); (3) improved AI narrative + brand image
- **Negative contribution**: (1) Annual burn of RMB 11-14 billion (110-140 in RMB 100 million units), pressuring Group profit; (2) overall AI Capex drove Non-GAAP net profit down 66% YoY
- **How much has the market already priced in**: Alibaba's Hong Kong shares rose from the 2024 low of HKD 70 to HKD 130-150 in 2026Q1 (~80% increase), and a meaningful portion was AI rerating. **Qianwen App's success or failure is already partially reflected in the share price**

> **Buffett-perspective conclusion**: It is reasonable for Alibaba overall to be rerated as a company with an "AI entry-point option," but **Qianwen App has limited standalone value** -- it makes sense in the hands of Alibaba as "owner," but viewed independently it is a poor business.

---

## 10. Summary

Qianwen App is a flagship consumer gateway backed by CEO-level All-in commitment, RMB 380 billion of Capex (3800 in RMB 100 million units), and the world's leading open-source model matrix. Over the next three years, it will **absolutely not lack money and almost certainly will not be cut** (shutdown probability <10%). But it faces three structural problems: (1) user usage frequency is only 36% of Doubao's -- engagement is far lower than the MAU number suggests; (2) 6 organizational adjustments in one year + Lin Junyang-level talent loss, with the route conflict between "large-army group operations vs elite small team" forcing out a soul figure; (3) no domestic AI App has an independent valuation precedent, and with the rug-pulling threat from WeChat/Douyin/system-level AI, the most likely 2029 position is "stable number two, merged with Quark or folded into cloud."

From Duan Yongping's perspective, **this is not a good business** (differentiation 3 / pricing power 1 / sustainable advantage 2). From Buffett's perspective, **resource safety is extremely high, but the commercialization ceiling is unclear**. From Munger's perspective, **the true killer is not DeepSeek but ecosystem-level suppression**. From Li Lu's perspective, **management is a composite B- (Eddie Wu B+, but strategic consistency loses major points)**.

For "Qianwen App business unit" as an investment target, this study rates it **Watch** -- no independent valuation precedent + industry-level fog. For investors holding Alibaba Group stock, Qianwen App is one of the AI entry-point options, and its value is already partially reflected in the share price. The most likely reality three years from now is that "Qianwen App is still running, but the market no longer marks it separately" -- its fate is tied to Alibaba's broader AI+e-commerce story, not the business unit's own financial self-proof.

---

## Appendix: Source Summary

### High Confidence (Financial Disclosures / Official Methodologies)
- Alibaba FY26Q3 earnings report (revenue, Capex, cloud revenue, triple-digit AI growth)
- RMB 380 billion three-year AI investment plan (3800 in RMB 100 million units) and "conservative" statement (Eddie Wu 2025-02-24 / 2025-11 earnings call)
- 5-year US$100 billion cloud+AI commercialization target (1000 in US$100 million units; Eddie Wu 2026-03-19)
- Formation of Qianwen consumer business group (led by Jia Wu, 2025-12-09)
- Establishment of ATH business group (2026-03-16)
- T-Head GPU delivery of 470,000 chips (47 x 10,000; disclosed 2026-02)
- Lin Junyang's 2026-03-04 departure (self-announced on X + Alibaba executive internal response)
- Jingren Zhou promoted to partner in 2025-12

### Medium Confidence (Third-Party Data / Media Estimates)
- Qianwen MAU: Alibaba official ~300 million (~3 hundred million) vs QuestMobile 166 million (1.66 hundred million, 2026Q1) -- methodology differences
- Doubao MAU 345 million (3.45 hundred million), DeepSeek 127 million (1.27 hundred million, QuestMobile 2026Q1)
- Average monthly uses per user: Doubao 54.8 times / Qianwen 19.8 times
- Spring Festival red-packet/free-order investment of RMB 3 billion (30 in RMB 100 million units), per-DAU acquisition cost of ¥144
- Tongyi Qianwen API revenue estimate (annualized RMB 20-40 billion range, or 200-400 in RMB 100 million units)
- Chang Zhou moving to ByteDance at 4-2 level with an 8-figure annual package

### Low Confidence (Estimates / Subjective Judgments)
- Qianwen App annual cash burn of RMB 11-14 billion (110-140 in RMB 100 million units; estimated from team size + compute)
- 2029 ARR scenarios (subscription/ads/e-commerce revenue-share assumptions)
- Business-unit valuation (subjective choice of PS multiple)
- Three-year organizational risk scenario probabilities
- "Qianwen App being cut" probability of 15-20%
- Probability of still working on Qianwen App product three years later: 30-40%

### Main References (Links in Each Sub-Agent Report)
- Alibaba FY26Q3 earnings report, Alibaba official announcements
- QuestMobile 2026Q1 AI Application Insights Report
- 21st Century Business Herald, Sina Finance, Wallstreetcn, Yicai, The Paper
- 36Kr (multiple deep-dive reports), LatePost, InfoQ, National Business Daily
- Bloomberg, Seeking Alpha
- Alibaba Cloud Developer Community

---

**Research Methodology Note**

This report was produced by team-lead synthesis after 4 independent sub-agents conducted parallel research:
1. Business-model analyst (Duan Yongping perspective, using WebSearch)
2. Financial/resource-investment analyst (Buffett perspective, using WebSearch)
3. Industry researcher (Munger perspective, based on public-information memory)
4. Risk and management evaluator (Li Lu perspective, using WebSearch)

Three years is an extremely long forecasting horizon in AI. This report should be recalibrated every 6 months.

**Last revised**: 2026-04-28
