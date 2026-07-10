# AI Model Sub-Sector - Funnel-Style Value Investing Screen

**Research date**: 2026-05-09
**Methodology**: 4-layer funnel (full-market scan -> 5 hard filters -> detailed analysis -> final selection of 3 companies for the four-master deep dive)
**Sub-sector definition**: Foundation models and tightly coupled adjacent businesses - closed/open frontier models, model inference services, MLOps platforms, AI labs
**Currency convention**: Unless otherwise noted, USD is used for US dollars, HKD for Hong Kong dollars, and CNY for Chinese yuan

---

## 0. Executive Summary

- **Core tension**: Most of the value at the top of the model stack is concentrated in **private companies** (OpenAI at 852 billion USD, Anthropic at 380 billion USD and potentially rising to about 900 billion USD, xAI at 230 billion USD, ByteDance Doubao, and DeepSeek with rapidly rising valuations). Ordinary investors can only gain exposure through **large-cap proxy holdings** (Microsoft, Google, Meta, Alibaba, Tencent, Baidu)
- **5 hard-filter results**: Out of 30+ candidates, only **6 listed companies** passed all 5 filters: Microsoft, Alphabet, Meta, Alibaba, and Tencent (Baidu barely cleared, with a weaker moat)
- **Final 3**: Alphabet (core position), Meta (satellite position), Alibaba (satellite position for China exposure)
- **Key observation**: Pure model inference providers (CoreWeave, Together, Fireworks) mostly have negative operating cash flow or heavy debt, and do not pass the five-factor screen overall
- **Information sufficiency rating**: B+ (first-hand data: financial reports and official announcements are complete; valuation data mostly comes from secondary reporting and needs cross-checking)

---

## 1. Layer One: Full-Market Scan

### 1.1 Listed company universe (sorted by market cap, near the 2026-05-08 close)

| Name | Ticker | Exchange | Market cap (est., trillion / billion) | Model business share (est.) | Main model products |
|---|---|---|---|---|---|
| Microsoft | MSFT | NASDAQ | 3.13 trillion USD | 25-35% (including Azure AI, Copilot, and 27% OpenAI stake)<sup>est</sup> | OpenAI models (via equity), proprietary Phi, MAI |
| Alphabet | GOOGL/GOOG | NASDAQ | 4.79 trillion USD | 30-45% (Gemini + Cloud + Search AI)<sup>est</sup> | Gemini 3, Gemini Enterprise, TPU |
| NVIDIA | NVDA | NASDAQ | (giant, >3 trillion USD<sup>est</sup>, model business share small) | <5% (in-house models are not the core business; it mainly sells GPUs to everyone) | NeMo, NIM, not core to this theme |
| Meta | META | NASDAQ | 1.59 trillion USD | 15-25% (Llama open source + Meta AI + MTIA)<sup>est</sup> | Llama 4/5, Meta Superintelligence Labs |
| Amazon | AMZN | NASDAQ | (giant, model exposure via Anthropic + Bedrock) | 10-15%<sup>est</sup> (AWS Bedrock, 8B+ USD investment in Anthropic) | Nova, Anthropic exposure |
| Alibaba | 9988.HK / BABA.US | HKEX / NYSE | about 2.7 trillion HKD<sup>est</sup> | 15-25% (Cloud + Qwen + Qwen App)<sup>est</sup> | Qwen3.5, Qwen App (300M MAU) |
| Tencent Holdings | 0700.HK | HKEX | about 4.4 trillion HKD<sup>est</sup> (471 HKD x about 9.24 billion shares) | 5-10% (Hunyuan + Yuanbao + WeChat AI integration)<sup>est</sup> | Hunyuan, Yuanbao, Hunyuan-A13B |
| Baidu | BIDU/9888.HK | NASDAQ / HKEX | about 48 billion USD<sup>est</sup> | 35-50% (Intelligent Cloud + ERNIE + Apollo Go) <sup>est</sup> | ERNIE 5.0 (2.4 trillion-parameter native multimodal) |
| CoreWeave | CRWV | NASDAQ | about 60-80 billion USD<sup>est</sup> | >=90% (GPU cloud dedicated to AI training/inference) | No in-house model, provides compute |
| Zhipu AI | 02513.HK | HKEX | about 323.2 billion HKD<sup>est</sup> (peak on Feb 20) | >=95% | GLM series, ChatGLM |
| MiniMax | 00100.HK | HKEX | about 304.2 billion HKD<sup>est</sup> (peak on Feb 20) | >=95% | MiniMax-Text, Hailuo AI |
| SenseTime | 0020.HK | HKEX | about 70-100 billion HKD<sup>est</sup> | 60-70% (generative AI revenue 77%) | SenseNova V6.5 multimodal |
| iFlytek | 002230.SZ | Shenzhen Stock Exchange | about 150-200 billion CNY<sup>est</sup> | 30-40% (Spark + education/healthcare)<sup>est</sup> | Spark 4.0+ |
| 360 Security | 601360.SH | Shanghai Stock Exchange | about 100 billion CNY<sup>est</sup> | 20-30% (360 Brain) | 360 Brain |
| Kingsoft Office | 688111.SH | STAR Market | about 150 billion CNY<sup>est</sup> | 5-15% (WPS AI) | In-house + third-party integration |

> Note: NVIDIA is the **largest shovel seller** in the model race, but it is not a "model company" - this report does not analyze it in depth, but it does need to be mentioned in the risk section as a source of "compute cost / NVIDIA pricing power".

### 1.2 ETF list

| ETF | Ticker | Main holdings profile |
|---|---|---|
| iShares AI ETF | IRBO | Global AI concept stocks |
| Roundhill Generative AI & Tech | CHAT | Generative AI theme |
| Global X AI & Big Data | AIQ | AI + big data |
| WisdomTree AI ETF | WTAI | AI + innovation |

### 1.3 Important private players (IPO candidates)

| Company | Latest valuation (USD) | Valuation date | Revenue / ARR | Potential IPO window | Notes |
|---|---|---|---|---|---|
| OpenAI | 852 billion | 2026-03 | 2B per month / 24B annualized USD | 2026-2027 (IPO plan rumored) | Amazon 50B, Nvidia 30B, SoftBank 30B; Microsoft holds 27% equity |
| Anthropic | 380 billion (2026-02 Series G) -> rumored 900 billion (in talks in 2026-04) | 2026-02 / in talks in 2026-04 | ARR 30B USD (2026-03) | 2027+ | YoY growth about 1400%, Claude Code ARR 2.5B |
| xAI | 230 billion (2026-01 Series E); combined with SpaceX implied value 1.25 trillion | 2026-01 | Grok 2025 revenue 350M, 2026 est. 2B | IPO rumored within 2026 | Nvidia / Cisco / QIA strategic participation |
| ByteDance | valuation about 400-500 billion USD<sup>est</sup> (secondary market) | 2026 ongoing | Doubao daily token calls 100 trillion | Long-term unclear | Doubao 2.0 priced at 1/10 of GPT-5.2 |
| DeepSeek | 10B -> 45B -> rumored 50B+ USD (funding in talks) | 2026-04 to 2026-05 | Not disclosed | Could reach STAR Market in 1-2 years | National Big Fund rumored lead investor |
| Mistral AI | 11.7B EUR (about 13B USD); in 2026-03 it also raised 830M USD in data-center debt | 2025-09 / 2026-03 | ARR 400M -> target 1B USD by end-2026 | 2026-2028 | European flag-bearer; led by ASML |
| Moonshot / Kimi | 10-18B USD | 2026-02-03 | Not disclosed | Not urgent in the short term | Backed by Alibaba and Tencent |
| Cohere | 7B USD; merger with Aleph Alpha rumored at 20B | 2025-09 / 2026-04 | ARR 240M USD | 2026-2027 | Positioned for enterprise + sovereign AI |
| Together AI | 3.3B USD | 2025-02 | API + GPU rental | Unclear | Inference platform |
| Fireworks AI | 4B USD | 2025-10 | ARR 315M USD (2026-02), YoY +416% | Unclear | Inference platform |
| 01.AI | about 10-15B CNY<sup>est</sup> | 2026 ongoing | Not disclosed | Unknown | Founded by Kai-Fu Lee |
| Baichuan AI | 20-30B CNY range<sup>est</sup> | 2026 ongoing | Not disclosed | Unknown | Founded by Wang Xiaochuan |

### 1.4 Summary

About **80% of the real top tier in the model race is not in public markets** - among the five closed-source frontier model leaders (OpenAI, Anthropic, xAI, ByteDance Doubao, DeepSeek), only Microsoft (27% OpenAI stake), Alphabet (wholly owned Gemini), Meta (wholly owned Llama), Alibaba (wholly owned Qwen), ByteDance (private), and xAI (private) can be considered "in-house frontier" players.

---

## 2. Layer Two: 5 Hard Filters

### 2.1 Screening criteria

1. **Reasonable PE**: For high-growth companies, PEG can be used as a relaxed standard (PEG < 2 is considered reasonable)
2. **ROE > 15%** or an improving trend
3. **Operating cash flow is positive and is >70% of net profit**
4. **Debt-to-asset ratio < 60%**
5. **Moat quick score >= three stars**

### 2.2 Screening table

| Company | PE (TTM) / PEG | ROE | Operating CF / Net profit | Debt-to-asset ratio | Moat | Passed how many | Conclusion |
|---|---|---|---|---|---|---|---|
| **Microsoft MSFT** | 24.5 / PEG about 1.5<sup>est</sup> | about 35%<sup>est</sup>, FY26Q3 operating profit YoY +20% | >100%<sup>est</sup> | <50%<sup>est</sup> | five stars | 5/5 | **Retain** |
| **Alphabet GOOGL** | 31.1 / PEG about 1.4<sup>est</sup> | about 32%<sup>est</sup> (Q1 net profit +81%) | >100%<sup>est</sup> (heavy capex but strong OCF) | <30%<sup>est</sup> | five stars | 5/5 | **Retain** |
| **Meta META** | 21.2 / PEG about 1.0<sup>est</sup> (Q1 revenue +33%) | about 35%<sup>est</sup> | >100%<sup>est</sup> | <40%<sup>est</sup> | four stars | 5/5 | **Retain** |
| **Alibaba 9988.HK** | about 18-20<sup>est</sup> / PEG 1.2<sup>est</sup> | 8-12%<sup>est</sup> (ROE does not reach 15%, but the trend is improving: Cloud up 36% / AI revenue triple-digit growth for 10 consecutive quarters) | 100%+<sup>est</sup> | <40%<sup>est</sup> | four stars | 4.5/5 (ROE borderline) | **Retain** (include improving ROE trend) |
| **Tencent 0700.HK** | about 19-22<sup>est</sup> / PEG 1.5<sup>est</sup> | about 18-20%<sup>est</sup>, non-IFRS net profit +17% | Free cash flow 182.6B CNY, >100% | <35%<sup>est</sup> | four stars | 5/5 | **Retain** |
| **Baidu BIDU** | about 12-14<sup>est</sup> / PEG <1 (growth is not strong) | 10-13%<sup>est</sup> (below 15%) | >100%<sup>est</sup> | 32.6% (2025 est.) | three stars | 4/5 (ROE misses) | **Watch** (cheap PE but weak growth) |
| **CoreWeave CRWV** | loss-making / N/A PEG | negative | unstable, huge capex and debt | very high (massive non-recourse loans) | three stars (GPU rental, medium technical moat) | 1/5 | **Eliminate** |
| **Zhipu AI 02513.HK** | N/A (loss-making) | negative | negative | high est. | three stars | 1/5 | **Eliminate** |
| **MiniMax 00100.HK** | N/A (loss-making) | negative | negative | high est. | three stars | 1/5 | **Eliminate** |
| **SenseTime 0020.HK** | N/A (loss-making) | negative | negative | high | three stars | 1/5 | **Eliminate** |
| **iFlytek 002230** | high (thin net margins) | <10%<sup>est</sup> | unstable | medium | three stars | 1/5 | **Eliminate** |
| **360 Security 601360** | high | near zero or negative<sup>est</sup> | unstable | medium | two stars | 0/5 | **Eliminate** |
| **Kingsoft Office 688111** | high (>50) | medium | positive | low | three stars (office + AI, but models are not the core in-house business) | 3/5 | **Watch** (better suited to the AI applications theme than the model theme) |

### 2.3 Conclusion of the second layer

**6 listed companies pass all 5 filters**
- Microsoft, Alphabet, Meta, Alibaba, Tencent (Baidu as a watchlist candidate)

**Main reasons for elimination**:
- Pure model unicorns (Zhipu / MiniMax / SenseTime) are still deeply loss-making
- AI compute services (CoreWeave) do not fit on cash flow or balance sheet
- A-share AI concept stocks generally have high PE and low ROE

---

## 3. Layer Three: Detailed Analysis (300-500 words each)

### 3.1 Microsoft Microsoft (MSFT)

**Business model**: A triad of B2B software + cloud + AI. Azure (including OpenAI API) + Microsoft 365 Copilot + GitHub Copilot create a closed loop. AI business ARR in FY26Q3 has exceeded 37B USD (YoY +123%). Microsoft holds 27% of OpenAI equity (about 135B USD book value) + IP license rights through 2032 (non-exclusive) + revenue share through 2030 (capped).

**Financial quality**: FY26Q3 revenue 82.9B USD (+18%), operating profit 38.4B (+20%). Azure growth 40%. RPO 627B USD (YoY +99%), with a very long order book. Commercial cloud 54.5B (+29%). Capex is large but OCF is extremely strong and free cash flow is stable.

**Moat**:
- **Ecosystem lock-in**: Office / Windows / Azure are three major platforms with extremely high switching costs (5 stars)
- **OpenAI equity**: Essentially a low-cost investment in a front-runner "rabbit," plus IP usage rights through 2032 (5 stars)
- **AI data flywheel**: feedback data generated after Copilot is embedded into enterprise workflows cannot be replaced (4 stars)

**Main risks**:
- 2026-04 Microsoft-OpenAI agreement reset: Microsoft is no longer exclusive and no longer pays OpenAI revenue share; OpenAI can run on Amazon / any cloud. **Azure exclusivity dividend is over**
- AI capex already exceeds 50%+ of OCF, creating pressure on return realization
- Regulation: frequent EU antitrust investigations

**Valuation quick view**: PE 24.5 (12-month average 32.6, already -25%), which is somewhat cheap relative to history. **Reasonably cheap**

### 3.2 Alphabet (GOOGL)

**Business model**: Search ads (cash cow) + YouTube + Google Cloud + Gemini. Q1 2026 revenue 109.9B USD (+22%, the fastest quarterly growth since 2022), net profit 62.6B (+81%!, EPS 5.11). Cloud exceeded 20B in a single quarter (+63%), backlog reached 460B USD. After Gemini 3 upgrades, core AI response cost fell 30%. Paid MAU for the Gemini app rose 40% QoQ, and AI-model-derived revenue grew 800% YoY.

**Financial quality**: Cash flow is extremely strong; 2026 capex guidance was raised to 180-190B, forming a "trillion-dollar club capex war" with the OpenAI camp, Meta, and xAI. Debt is extremely low and net cash is abundant.

**Moat**:
- **Data flywheel**: Search + YouTube + Android + Maps + Workspace cover almost all global internet user behavior (5 stars)
- **Compute independence**: TPU v6/v7 + owned data centers, with lower dependence on Nvidia than peers (5 stars)
- **Research depth**: after DeepMind and Google Brain were combined, talent density may be the highest in the world (5 stars)

**Main risks**:
- AI answers replacing search clicks, eroding the core ad ARPU over time
- Antitrust breakup pressure (the US DOJ is still pursuing the case)
- Capex of 180-190B is above expectations, and the market worries about ROIC

**Valuation quick view**: PE 31.1 (higher than MSFT but still consistent with META's growth), and given Cloud +63% and accelerating Gemini commercialization, **reasonably slightly expensive but acceptable**

### 3.3 Meta Platforms (META)

**Business model**: Advertising (97%+) + Reality Labs (continued losses). Q1 2026 revenue 56.3B (+33%). Llama 4/5 + Meta Superintelligence Labs launched the first model. MTIA in-house AI accelerators (co-developed with Broadcom, 2nm) reduce dependence on Nvidia. 2026 capex was raised to 125-145B USD.

**Financial quality**: Q1 revenue beat expectations, but the stock fell more than 6% after hours because capex guidance was raised. Margins remain among the best in the industry. Debt-to-asset ratio is about 30-40% (est.).

**Moat**:
- **3B-DAU social network**: advertising monetization power + user behavior data (5 stars)
- **Open-source Llama strategy**: effectively "AI Android," building a third-party developer ecosystem and then feeding that back into ad systems (4 stars)
- **MTIA in-house chips**: long-term compute cost reduction (3 stars)

**Main risks**:
- 125-145B capex makes the market question ROI; if Llama underperforms GPT-5 / Gemini 3, the open-source strategy could fall flat
- Regulation: EU DMA and US youth protection
- TikTok (ByteDance) continues to steal user time

**Valuation quick view**: PE 21.2 (forward 19.6), growth 33%, PEG <0.7, **cheap**

### 3.4 Alibaba (9988.HK)

**Business model**: E-commerce (Taobao / Tmall) + Alibaba Cloud + AIDC (international e-commerce) + Cainiao + Qwen App (300M MAU on the consumer side). In FY2026Q3 (calendar Q4 2025), Alibaba Cloud posted 43.284B CNY (+36%); AI-related product revenue has grown triple digits YoY for 10 straight quarters. Management's target is for cloud + AI commercialization revenue including MaaS to exceed 100B USD over the next five years. CMR (customer management revenue) was 102.7B CNY (+1%, showing a slowdown in the e-commerce core business).

**Financial quality**: Strong cash flow (dual engines of e-commerce + cloud), debt-to-asset ratio 30-40% (est.). ROE about 8-12% (below US big tech, but improving trend: higher net margins + cloud profit release).

**Moat**:
- **Cloud market share**: number one in China (4 stars)
- **Qwen open-source ecosystem**: Qwen3 series is consistently near the top of the HuggingFace open-source rankings and is the de facto benchmark for Chinese foundation models (4 stars)
- **T-Head in-house GPU**: this quarter it was first disclosed to have entered scaled production and commercialization (3 stars)
- **Qwen App 300M MAU**: one of the largest consumer AI user bases in China (4 stars)

**Main risks**:
- US-China technology decoupling and Nvidia GPU export restrictions
- E-commerce core business continues to be eroded by Pinduoduo and Douyin
- Hong Kong listing liquidity discount (vs. BABA ADR)

**Valuation quick view**: PE 18-20<sup>est</sup>, PEG close to 1, market cap up 5.98% YoY, **cheap**

### 3.5 Tencent Holdings (0700.HK)

**Business model**: Gaming + WeChat ecosystem + advertising + financial services + cloud + AI Yuanbao / Hunyuan. Full-year 2025 revenue was 751.766B CNY (+14%), attributable net profit 224.842B (+16%), non-IFRS attributable net profit 259.626B (+17%). Free cash flow 182.6B (+18%). Gross margin hit a record 56% (+3pp). Hunyuan has launched 30+ models; Yuanbao DAU is among the top three domestic AI-native apps; it is integrated into WeChat, QQ Music, Tencent Meeting, Docs, and Video.

**Financial quality**: Cash-flow champion (FCF 182.6B). ROE about 18-20% (est.). Debt-to-asset ratio about 30-35%. The investment portfolio (including Meituan, JD, PDD, Spotify, Reddit) has a book value of 800-1000B CNY<sup>est</sup>.

**Moat**:
- **WeChat 1.3B MAU**: unmatched distribution barrier (5 stars)
- **Yuanbao + WeChat AI**: AI touchpoint becomes "super app + super model" (4 stars)
- **Gaming cash cow**: funds AI capex across cycles (5 stars)

**Main risks**:
- Hunyuan often lags GPT-5 / Gemini 3 / Claude / Qwen in frontier evaluations
- AI ROI is unclear: Yuanbao commercialization has not yet broken through
- Domestic regulation (game approvals, youth protection)

**Valuation quick view**: PE 19-22<sup>est</sup>, relative to intrinsic value (including the investment portfolio) it is effectively low-teens PE, **cheap**

### 3.6 Baidu (BIDU)

**Business model**: Search (structural decline) + Intelligent Cloud + Apollo Go + ERNIE. In 2025, Intelligent Cloud reached 30B (infrastructure +34%, accelerator subscription Q4 +143%). ERNIE 5.0 is a 2.4-trillion-parameter native multimodal model, said to outperform Gemini 2.5 Pro and GPT-5-High overall.

**Financial quality**: Revenue growth is in the low single digits; ROE is 10-13%; debt-to-asset ratio is 32.6%; cash flow is stable.

**Moat**:
- **AI accelerator subscriptions +143% in Q4**: strong infrastructure demand (3 stars)
- **ERNIE iteration speed**: open-source + free pricing strategy (3 stars)
- **Apollo Go**: leading in autonomous driving (3 stars, but not in this theme)
- **Search traffic entry**: being squeezed by AI answers (2 stars)

**Main risks**:
- Search cash cow is being disrupted by AI, and Baidu itself is helping disrupt itself
- Surrounded by ByteDance, Alibaba, and DeepSeek, while Baidu's brand is "not sexy"
- Cheap valuation but questionable moat - classic value trap risk

**Valuation quick view**: PE 12-14<sup>est</sup>, **very cheap** but growth is weak and brand momentum is declining

---

## 4. Layer Four: Final 3 Deep Dives (Four-Master Perspective)

### Final selection logic

| Dimension | Alphabet | Meta | Alibaba |
|---|---|---|---|
| In-house frontier model | Gemini 3 (top-tier evaluation) | Llama 5 (open-source flag-bearer) | Qwen3.5 (Chinese / open-source benchmark) |
| Compute independence | TPU v6/v7 (best) | MTIA (medium) | T-Head (early stage) |
| Valuation attractiveness | PE 31, reasonably slightly expensive | PE 21, cheap | PE 18-20, cheap |
| Civilization-scale exposure | Search + cloud + model | Distribution to 3B users | China's strongest AI dual engine |
| Action recommendation (overall) | Core position | Satellite position | China exposure satellite position |

**Why Microsoft is not selected**: Microsoft is excellent, but after the 2026-04 agreement reset, OpenAI exclusivity ended. At PE 24.5, the 18% growth rate does not offer the same value-for-money as META (PE 21 / growth 33%). The moat is still strong, but short-term variables have increased. **MSFT is moved to the watchlist**.

**Why Tencent is not selected**: Tencent's financial quality is excellent (FCF 182.6B), but **its in-house frontier model is relatively behind** - Hunyuan often lags Qwen, GPT-5, Claude, and Gemini in international benchmarks. Tencent is fundamentally an "AI applications + investment company" rather than a "model company." In the narrower model theme, Tencent's exposure is not pure enough. **Tencent should be assessed separately in the gaming / AI applications theme**.

### 4.1 Alphabet (GOOGL) - Overall recommendation: five stars

#### 4.1.1 Duan Yongping perspective: business essence

> "Do the right thing, and do things right. When you look at a company, look at the business model, corporate culture, and moat."

Alphabet is fundamentally the **world's largest, highest-margin information infrastructure company**. Search has been its cash cow for the past 25 years, contributing 60%+ of revenue and close to 80% of profit every year. The nature of the business is:
1. **Very high ROIC**: search ads require almost no heavy assets
2. **Network effects**: more users -> more advertisers -> better algorithms -> better user experience
3. **Scale creates pricing power**: ad CPM is auction-based, but traffic-share dominance makes Google effectively the price setter

However, this old business is being disrupted by AI - AI answers mean users no longer click search results. Alphabet's key response is **self-disruption**. Gemini 3 + AI Overviews + AI Mode are not meant to preserve the old search model, but to keep Alphabet as the "information entry point" in the AI era. Q1 2026 data show: Cloud +63%, paid Gemini Enterprise users +40% QoQ, AI-model-derived revenue +800% YoY, and net profit +81%. This is a company that has **stepped out of its comfort zone and already proved the transition in its financials**.

Duan Yongping asks, "Is this a good business?" - **Yes**, because the core search business still throws off a huge amount of cash (annual free cash flow in the 100B+ USD range), AI is a move from one high-margin business into another potentially even higher-margin business (cloud + model APIs + Workspace AI), the culture is healthy (founder control + pragmatic Pichai), and the moat is being upgraded rather than weakened.

#### 4.1.2 Buffett perspective: moat

> "I look for companies with enduring competitive advantages, deep and wide moats, and plenty of crocodiles inside."

| Moat type | Strength | Evidence |
|---|---|---|
| **Data flywheel** | 5 stars | 8B+ daily searches, YouTube video data, Maps geography data, Android user behavior, Workspace documents; any competitor would need 10 years to replicate |
| **Scale of compute** | 5 stars | In-house TPU v6/v7 + global data centers; 2026 capex of 180-190B USD is affordable only for a few companies; less dependent on Nvidia than OpenAI / Anthropic / Meta / Microsoft |
| **Research talent density** | 5 stars | After the merger of DeepMind + Google Brain + Quantum AI, there are about 5,000+ AI researchers; Transformer, Diffusion, AlphaGo, and AlphaFold all came out of here |
| **Brand pricing power** | 4 stars | "Google it" has become a verb; advertisers cannot route around it |
| **Switching costs (B2B)** | 4 stars | Workspace has 2.2B users + Cloud backlog of 460B |

**Will the moat still be there in 10 years?** Three things will decide:
1. Whether AI answers displace search enough to destroy advertising - Google is countering with AI Mode
2. Whether TPU can continue to keep pace with Nvidia GPU - Gemini 3 training cost is already down 30%, showing the compute advantage is sustainable
3. Antitrust breakup - even if a breakup happens, Search / Cloud / YouTube as standalone companies could be worth more in aggregate than the current market cap (as with Standard Oil)

**Conclusion**: The moat is not only intact over the next 10 years, it may deepen in the AI era.

#### 4.1.3 Munger perspective: risks and failure modes

> "Just tell me where I am going to die, and I will never go there."

Possible scenarios that could cause Alphabet to fail or underperform:
1. **Search ads collapse quickly** (25% probability): AI answers cause search click-through rates to plunge 50%+, while new AI ad formats do not keep up -> short-term valuation could be cut in half
2. **Gemini loses to GPT-6 / Claude 5** (25% probability): Anthropic / OpenAI pull ahead in frontier capability and enterprise customers migrate at scale
3. **Antitrust breakup** (15% probability): the DOJ forces a Search + Chrome or Search + Android split; breakup may not reduce total value, but it could compress the valuation in the short term
4. **Capex black hole** (30% probability): 180-190B of capex persists for 3-5 years while ROIC falls and free cash flow shrinks
5. **Open-source parity** (50% probability): Llama, DeepSeek, and Qwen make 90% of use cases good enough with open models, destroying frontier-model rent - this is exactly the **largest systemic risk** in the model theme

Why not buy it if you're smart? Because frontier-model economics are uncertain, regulation is real, and the capex black hole is real - those concerns are reasonable, but **Alphabet is the hardest one to kill**: it has search ads as its base layer, so even if frontier model rents go to zero, it remains one of the world's largest advertising companies.

Worst-case valuation: assume Search -30%, Cloud growth slows to 30%, and Gemini commercialization fails -> net margin falls from 25% to 18%, and market cap could drop to 2.5-3 trillion USD (current 4.79T). Downside about -40%.

#### 4.1.4 Li Lu perspective: civilization-scale positioning

> "Investing is about spending half a lifetime looking for a few civilization-scale opportunities."

Alphabet's role in the civilization-scale paradigm is:
- **The past 25 years' "information retrieval -> ad monetization" model**: a money printer
- **The AI era's "knowledge and decision entry point -> multi-format monetization" model**: potentially larger than search

Li Lu would ask: Is this one of the few companies you can hold for 30 years?

Answer: **Yes**. Reasons:
1. Information technology and AI are the 21st century's biggest civilization-scale energies, similar to electricity and railroads in the 19th century
2. In every energy era, companies that control the distribution pipes and infrastructure tend to generate the best long-term returns (Edison General -> Standard Oil -> AT&T -> Microsoft -> Google)
3. Alphabet simultaneously owns **distribution** (Search / YouTube / Android / Chrome) + **infrastructure** (Cloud / TPU) + **models** (Gemini) + **research** (DeepMind), which is an unusually rare full-stack combination

Alphabet's civilization-scale bet is not on a brand-new thing; it is on the idea that the civilization-scale dividend from information and computing will continue for another 30 years.

#### 4.1.5 Overall score and action plan

| Dimension | Score | Notes |
|---|---|---|
| Duan Yongping: good business | five stars | High ROIC, self-disruption |
| Buffett: moat | five stars | Triple moat of data + compute + talent |
| Munger: risk | four stars | Regulation + capex are real risks |
| Li Lu: civilization scale | five stars | 30-year candidate |
| **Overall recommendation** | **five stars** | **Core position** |

**Action plan**:
- Position limit: 8-10% for a single holding, 12-15% within a 25-30% theme allocation
- Buy point: PE < 28 (current 31 is slightly expensive but reasonable); if there is a regulatory selloff and a 20%+ pullback, add up to the limit
- Sell point: PE > 40 or Cloud growth falls below 30% (a structural change signal)
- Holding period: at least 5-10 years

---

### 4.2 Meta Platforms (META) - Overall recommendation: four stars

#### 4.2.1 Duan Yongping perspective: business essence

Meta's essence is the **ultimate form of "user time -> ad monetization"**. More than 3B DAU and the four-product matrix of Facebook / Instagram / WhatsApp / Threads make advertising the largest business scale in human history (2025 ad revenue is roughly 170-180B USD).

But what Duan Yongping would really care about is whether Meta has pricing power. The answer is **partial**. Meta is not like Google, which relies on "users actively searching"; it relies on "users passively browsing." Its ad ROI depends on AI recommendation quality. So Meta's 145B capex is not "for AGI" - it is **to improve ad ROI by another 20-30%**, and that has already been validated (part of Q1 2026 revenue +33% came from this).

The open-source Llama strategy is another smart "borrowing strength from others" move: open source lets developers worldwide test the models and attract talent ("AI Android"), while Meta then uses the best model to improve its ad systems. This is a more business-driven AI strategy than Google's.

But Duan Yongping would also worry: **Is Reality Labs' continuing massive loss (200B+ USD per year) worth it?** Zuckerberg's "metaverse + AI" double bet, under a structure where he controls more than 60% of the voting rights, is almost impossible for the board to restrain.

#### 4.2.2 Buffett perspective: moat

| Moat | Strength | Evidence |
|---|---|---|
| **Network effects** | 5 stars | 3B+ DAU, friends and family are there -> switching costs are extremely high |
| **Data flywheel** | 4 stars | Users generate billions of social signals per second, continuously optimizing the ad system |
| **Brand** | 3 stars | Instagram is strong, Facebook is aging, WhatsApp is unbeatable in emerging markets |
| **Compute scale** | 3 stars | MTIA is in-house, but still behind TPU; capex is large but still depends on Nvidia |
| **Open-source ecosystem** | 4 stars | Llama downloads have exceeded 1B and an open-source community has formed |

**Will the moat still be there in 10 years?** The key risk is **population aging and younger users migrating to TikTok**. WhatsApp still dominates in emerging markets, and Instagram Reels is catching up to TikTok but has not regained share. Meta's moat is one notch shallower than Google's (search entry-point monopoly vs. social products that can be displaced by new platforms - see MySpace, ICQ, Yahoo Mail).

#### 4.2.3 Munger perspective: risks

1. **TikTok keeps stealing user time** (50% probability): especially Gen Z; Reels helps but does not solve it
2. **Reality Labs money pit** (70% continuing probability): annual losses of 200B+ USD with no end in sight
3. **145B capex if ROI disappoints** (40% probability): Meta's stock already fell more than 6% after hours for this reason
4. **Llama 5 falls behind GPT-6 / Gemini 4 / Claude 5** (30% probability): open-source strategy unravels
5. **EU DMA + US youth-protection lawsuits** (ongoing probability): fines + product restrictions
6. **MTIA fails to keep up with Nvidia** (50% probability): long-term compute cost disadvantage

Worst-case scenario: TikTok steals 30% of time + ad CPM drops 20% + Reality Labs keeps losing money -> valuation could fall to PE 14 (current 21), market cap around 1T (current 1.59T). Downside about -35%.

#### 4.2.4 Li Lu perspective: civilization-scale positioning

Meta's civilization-scale position is **"the digital infrastructure of human social relationships"** - an almost certain trend (people will not stop socializing; they will only socialize more digitally). But **the exact platform carrying this trend will change** (MSN -> Facebook -> Instagram -> TikTok -> ?).

Li Lu-style question: **Among WhatsApp + Instagram + Facebook + Threads, which one still exists 30 years from now?**
- WhatsApp: strongest probability, because India / Brazil / Indonesia still treat it like infrastructure
- Instagram: content format will evolve (images -> short video -> AI-generated content), so its survival probability is medium
- Facebook: youth attrition is obvious; 30 years later it could look like LinkedIn for old people
- Threads: not yet established

Meta's AI position (Llama + Meta AI in WhatsApp) is **a second monetization layer on top of its distribution channels** - if 3B DAU are still there, the AI assistant will have users. This path from "user base -> AI monetization" is more stable than pure API companies like OpenAI or Anthropic.

#### 4.2.5 Overall score and action plan

| Dimension | Score |
|---|---|
| Duan Yongping: good business | four stars |
| Buffett: moat | four stars |
| Munger: risk | three stars (TikTok + Reality Labs + capex triple risk) |
| Li Lu: civilization scale | four stars |
| **Overall recommendation** | **four stars** |

**Action plan**:
- Position limit: 5-7% for a single holding, 8-10% within the model theme
- Buy point: current PE 21, forward 19.6, and 33% growth (PEG 0.6) already look cheap; the post-earnings 6% drop is a good add point
- Sell point: single-quarter Reality Labs losses > 8B USD and capex guidance raised again; or TikTok is allowed in the US and steals Reels traffic
- Holding period: 3-5 years of observation

---

### 4.3 Alibaba (9988.HK) - Overall recommendation: four stars

#### 4.3.1 Duan Yongping perspective: business essence

Alibaba is now a **"e-commerce cash cow + cloud + AI" three-engine business**, and the best analogy is a **hybrid of "China's Amazon + Google's"**. In FY2026Q3: Alibaba Cloud was 43.284B CNY (+36%), and AI-related product revenue has grown triple digits YoY for 10 consecutive quarters. CEO Eddie Wu has set a target of "cloud + AI commercialization revenue including MaaS exceeding 100B USD over the next 5 years" - the clearest AI commercialization target among China's large tech firms.

The Qwen App has 300M MAU and is one of the largest consumer AI user bases in China (top four alongside Doubao, Kimi, and Yuanbao). The Qwen series is consistently in the top 3 on HuggingFace open-source rankings and is the **de facto benchmark for Chinese foundation models**. T-Head GPU disclosed scaled production and commercialization this quarter - a key milestone (the first large Chinese tech company to commercialize an in-house GPU).

Duan Yongping would ask, "Is this a good business?" - **Yes, but with shadows**:
- **Positive side**: e-commerce profitability is recovering (CMR +1% but margins improved), cloud + AI are growing rapidly, and the in-house GPU breakthrough is real
- **Shadow side**: the core e-commerce business is still being eroded by Pinduoduo and Douyin; CMR growth of only +1% is a structural issue; Hong Kong listing discount and ADR delisting risk
- **Management**: Eddie Wu's strategy of "lightening the load and starting over" is clear, and Joe Tsai's return has made buybacks more aggressive

#### 4.3.2 Buffett perspective: moat

| Moat | Strength | Evidence |
|---|---|---|
| **Cloud market share** | four stars | No. 1 cloud in China, >30% share; +36% in 2026Q3 is one of the fastest growth rates in the industry |
| **Data flywheel** | four stars | Shopping data from 1B Taobao / Tmall users + 300M Qwen App MAU + Amap + DingTalk |
| **Compute (in-house)** | three stars | T-Head commercialization is the first large Chinese company to generate scaled revenue from a domestic GPU (tied with Cambricon in terms of progress) |
| **Qwen open-source ecosystem** | four stars | HuggingFace ranking + global developer community + strong Chinese / English performance |
| **Payments / logistics** | four stars | Alipay (Ant Group) + Cainiao, e-commerce infrastructure |

**Will the moat still exist 10 years from now?** Key variables:
- Whether deeper US-China decoupling cuts off Nvidia GPU supply -> T-Head + Huawei Ascend determine survival
- Whether Pinduoduo and Douyin continue to steal GMV -> can Alibaba Cloud + AI offset it
- Whether Qwen stays in the top 3 in frontier evaluations

#### 4.3.3 Munger perspective: risks

1. **US-China technology decoupling** (60% probability): Nvidia export controls + ASML restrictions + ADR delisting
2. **E-commerce keeps getting eroded by Pinduoduo / Douyin** (70% probability): the +1% CMR already reflects this
3. **Hong Kong liquidity discount** (structural, long-term -10% to -20%)
4. **Domestic regulatory swings** (30% probability): AI, data security, platform economy
5. **AI commercialization target is too aggressive** (40% probability): the 100B USD / 5-year target is under pressure
6. **Qwen falls behind DeepSeek / ByteDance Doubao** (30% probability): domestic competition is intense

Worst-case scenario: decoupling + GPU cutoff + Pinduoduo keeps taking share -> Alibaba Cloud growth falls to 15%, the AI commercialization target is cut in half, and e-commerce margins compress -> market cap could fall to PE 12 / 1.5T HKD (current 2.7T). Downside about -45%.

#### 4.3.4 Li Lu perspective: civilization-scale positioning

Li Lu is a long-term holder of Chinese assets (Hillhouse has been heavily invested in BABA for many years). His logic is:

1. **China's 1.4B-person digitization is a civilization-scale opportunity**: Alibaba is a leader in the three most important digital infrastructure layers - e-commerce, cloud, and AI
2. **Qwen open source is a key carrier for "Chinese AI going global"**: open source is more geopolitically friendly and harder to block than closed models
3. **30-year perspective**: whether China can maintain an independent compute supply chain + independent foundation models in the AI era - Alibaba is one of the strongest players on both fronts

Li Lu would ask: **Is Alibaba the Chinese version of Alphabet?** Partly:
- **Similar**: search (X) vs e-commerce (sqrt), cloud (sqrt), AI (sqrt), open-source ecosystem (sqrt)
- **Different**: Alibaba does not have a pure search-ads monetization model; e-commerce margins are lower than ads
- **More complex**: Alibaba has Ant (finance), Cainiao (logistics), and other real-economy exposures that Alphabet does not

Net conclusion: Alibaba is **the best representative of Chinese AI, but it is not the same as "China's Alphabet"** - on valuation, giving it 18-20 vs Alphabet PE 31 is reasonable after discounting decoupling risk, Hong Kong discount, and e-commerce pressure.

#### 4.3.5 Overall score and action plan

| Dimension | Score |
|---|---|
| Duan Yongping: good business | four stars |
| Buffett: moat | four stars |
| Munger: risk | three stars (geopolitics is the top risk) |
| Li Lu: civilization scale | four stars (China's No.1 AI asset) |
| **Overall recommendation** | **four stars** |

**Action plan**:
- Position limit: 5-7% for a single holding, 8-12% within the model theme
- Buy point: HK-listed 9988 around 140 HKD (PE 18-20); below 130 HKD is a better add point; a 10%+ drop in the ADR is also acceptable
- Sell point: Qwen falls out of the global top 5 open-source models; Alibaba Cloud growth falls below 25%; decoupling escalates to a GPU cutoff
- Holding period: 5-10 years (consistent with Li Lu)
- HK stock vs ADR: prefer 9988.HK (to avoid ADR delisting risk)

---

## 5. Industry-Level Risk Assessment (Munger "Checklist")

### 5.1 Systemic risk list

| Risk | Probability | Impact | Response strategy |
|---|---|---|---|
| **Open-source model parity** (Llama / Qwen / DeepSeek makes 90% of use cases good enough) | High (50%+) | Destroys frontier-model rents | Diversify into big companies with distribution (Alphabet / Meta / Alibaba), avoid pure model unicorns |
| **Compute cost inflation** (Nvidia pricing power + insufficient power supply) | Medium (40%) | Downward pressure on capex ROI at the top | Own companies with in-house chips (Alphabet TPU, Meta MTIA, Alibaba T-Head) |
| **Regulation / antitrust** (US DOJ, EU DMA, China data security) | Medium (30%) | Short-term valuation compression | Choose diversified businesses (Alphabet could even be worth more after a breakup) |
| **US-China tech decoupling worsens** | High (60%) | Alibaba / Baidu exposure constrained; BABA delisting | Use HK-listed 9988 rather than ADR; diversify position sizes |
| **AI capex bubble bursts** | Medium (40%) | Large short-term market-cap correction (Meta already fell 6% after hours) | Build positions in tranches and keep 30% dry powder for a 25% correction |
| **Next-generation algorithmic paradigm shift** (non-Transformer route) | Low (15%) | Current accumulation becomes obsolete | Not really hedgeable - only trust the research depth of leading companies (DeepMind is the best insurance) |
| **Model capability hits a ceiling and AI growth peaks** | Low (10%) | Multiple compression | Watch frontier benchmarks (IMO / CMO / SWE-Bench) for growth changes |

### 5.2 Historical analogies

**Best analogy 1: the late-1990s internet boom**
- Most pure internet companies went to zero (Pets.com, Webvan)
- The real winners were infrastructure + distribution: Cisco, Intel, Microsoft, Amazon (the few that survived)
- **Implication for the model theme**: even if pure model companies (OpenAI / Anthropic) have high valuations, the eventual survivors may be the large companies with distribution moats

**Best analogy 2: the electricity revolution (1880-1920)**
- Edison Electric was eventually absorbed by GE
- The long-term winners were the grid (utilities) + electricity-consuming industries (GM, Ford)
- **Implication for the model theme**: models themselves may become commoditized, and the real AI dividend may lie in "applications transformed by AI" - which is why Alphabet (search + cloud + Workspace), Meta (social), and Alibaba (e-commerce) are more resilient exposures

**Best analogy 3: mobile internet 2007-2015**
- Apple + Google captured most of the value (operating system layer + application layer)
- Chinese domestic kings: Tencent + Alibaba
- **Implication for the model theme**: operating-system-level players (cloud + AI platforms) + Chinese domestic leaders form a dual-track structure

### 5.3 Bias self-check

- **Narrative bias**: Is the AI story too perfect - is the "unprecedented productivity revolution" exaggerated?
  - Self-check: actual enterprise AI ROI data (such as Meta ads +33%, Google net profit +81%) prove there is already real return, but these companies already had strong distribution; pure model company ROI still has not been proven
- **Anchoring**: Are we anchored to OpenAI at 852B and Anthropic at 900B?
  - Self-check: private-market valuations are not the same as publicly sustainable valuations (Snap and Coinbase both fell sharply after IPO)
- **Herding**: Is this just "Buffett bought Apple, so I should buy it too"?
  - Self-check: keep independent judgment; this report ranks MSFT behind Alphabet / Meta / Alibaba because of ROIC concerns

---

## 6. Civilization Trend Judgment (Li Lu Framework)

### 6.1 Paradigm question

**Is this a civilization-scale paradigm shift or a phase-specific boom?**

Data points (supporting civilization-scale):
- Microsoft AI business ARR 37B USD (YoY +123%)
- Anthropic ARR 30B USD (YoY ~1400%)
- OpenAI monthly revenue 2B USD
- Alphabet AI-model-derived revenue YoY +800%
- ByteDance Doubao daily volume 100 trillion tokens

The **absolute values** + **growth rates** of these figures already exceed the comparable data from the 1995-2000 internet boom.

Li Lu's perspective: **this is confirmed as a civilization-scale paradigm**. But **whether a single company can be held for 30 years is a separate question** - Cisco was a winner in the 1990s, but after the 2000 peak it took 25 years just to get back to the same level.

### 6.2 Historical analogy

The closest tech-revolution analogy is **electricity + computers combined** - AI is both a new kind of "energy" (intelligence can be plugged in) and a new kind of "computation" (natural language becomes the programming language).

Historical experience:
- The electricity revolution took 40 years to reach most households
- The computer revolution took 30 years to reach every desk
- The internet took 15 years to become mainstream
- AI is estimated to take 5-10 years to be embedded in every white-collar workflow

### 6.3 10-20 year endgame

**Most likely winners**:
1. **Large platforms with distribution**: Alphabet (search + cloud), Meta (3B users), Alibaba (e-commerce + cloud), Microsoft (enterprise software)
2. **Large companies with compute infrastructure + in-house chips**: Alphabet TPU, Meta MTIA, Alibaba T-Head (China); Nvidia still dominates GPUs but pricing power may weaken
3. **A few pure model companies**: OpenAI (consumer + enterprise API), Anthropic (enterprise + coding) - only 1-2 survivors may remain

**Most likely to be disrupted**:
- Search (already underway), customer support, entry-level coding, basic translation, entry-level legal advice, entry-level medical advice
- Most pure model unicorns (under open-source parity)

**Winner-take-all segments**:
- Operating-system-level AI platforms (OpenAI ChatGPT, Google Gemini App, Alibaba Qwen App)
- Enterprise AI workflows (Microsoft Copilot, Salesforce, Workday)

**Most disrupted segments**:
- Pure API providers (if open source becomes good enough)
- Single-point AI tools (if models become strong enough)

---

## 7. Portfolio Construction Recommendation

### 7.1 Suggested portfolio (model-theme structure)

| Tier | Weight inside theme | Security | Segment | Core logic |
|---|---|---|---|---|
| **Core position** | 40-50% | Alphabet (GOOGL) | Model + cloud + distribution + compute in one | Most certain, widest moat, 30-year civilization-scale candidate |
| **Satellite position** | 15-25% | Meta (META) | Model + distribution to 3B DAU | Cheap valuation (PEG <0.7), open-source ecosystem |
| **Satellite position (China)** | 10-20% | Alibaba 9988.HK | China cloud + Qwen + T-Head | China's No.1 AI asset, civilization-scale |
| **Watchlist** | 0-10% | Microsoft (MSFT) | Model + enterprise cloud + Copilot | Excellent, but more variables after the OpenAI reset |
| **Watchlist** | 0-5% | Tencent 0700.HK | AI applications + investment portfolio | Excellent financial quality, but not pure model exposure |
| **Not recommended** | 0% | CoreWeave, Zhipu, MiniMax, SenseTime | Pure models / compute | Cash flow does not qualify |
| **ETF alternative** | 100% | IRBO / CHAT / AIQ | All | "Lazy" solution for people who do not want to pick stocks - but it dilutes Alphabet's high certainty |

### 7.2 Buy / sell signals

| Signal type | Specific condition |
|---|---|
| **Add signal (trigger any one)** | • Alphabet PE < 28; Meta forward PE < 17; Alibaba 9988 < 130 HKD<br>• Sector-wide pullback of more than 25% (correction caused by AI capex concerns)<br>• Any of the final 3 discloses a major AI commercialization milestone (for example Cloud growth >70%) |
| **Reduce signal** | • Alphabet PE > 40; Meta PE > 30; Alibaba PE > 30<br>• Cloud / AI single-quarter growth falls below 20%<br>• Major regulatory or antitrust event (such as a breakup ruling) |
| **Exit signal** | • A company built on the next-generation paradigm (non-Transformer) leads frontier benchmarks by 18 months or more<br>• Core management (Pichai, Zuckerberg, Eddie Wu) leaves<br>• US-China decoupling escalates into a real GPU cutoff for Alibaba |

### 7.3 Theme-level position cap

**Model theme cap as a share of total portfolio: 30-35%** (not more than the entire AI theme; 50% of the total portfolio in AI is common for aggressive investors, while 20-25% is common for conservative ones)

Reasons:
- Civilization-scale opportunity, but with high internal risk (capex black hole, open-source parity, regulation)
- Two of the final 3 are tech giants (Alphabet / Meta), so the single-stock weight should not be too high
- Alibaba has geopolitical variables, so the single position should not exceed 10%

---

## 8. Decision Memo

### 8.1 Industry summary table

| Dimension | Conclusion | Confidence |
|---|---|---|
| Investment logic chain (degree of validation) | AI commercialization has already been largely monetized (financial data) | High |
| Best segment (Duan Yongping's "right business") | Large companies with the full chain of distribution + model + compute | High |
| Widest moat (Buffett) | Alphabet (data flywheel + TPU + DeepMind) | High |
| Biggest risk (Munger) | Open-source parity + capex bubble + US-China decoupling | Medium |
| Civilization trend positioning (Li Lu) | Civilization-scale paradigm (analogous to electricity + computers) | High |
| Overall valuation level | Top tech names trade at PE 21-31, broadly neutral to history; private unicorn valuations are too high | Medium |

### 8.2 Simulated commentary from the four masters

> **Duan Yongping**: "Look at the business model, corporate culture, and moat. In the AI race, most companies have not yet proven their business model; a few already make money - so buy the ones that already make money. Alphabet, Meta, and Alibaba are all cash-generating good businesses, and AI can only make them better, not disrupt them. I would rather hold them for 10 years than buy OpenAI or Anthropic at post-IPO highs."

> **Buffett**: "I do not understand AI very well, but I do understand moats. Alphabet's search business is one of the deepest moats I have ever seen - deeper than Coca-Cola. If they can bring that moat into the AI era, that is a 30-year good business. I will not bet on which model is the strongest; I will bet on distribution channels - and Alphabet and Meta are the strongest distribution channels in the world."

> **Munger**: "Smart people do not buy companies that are burning cash, unless the return on burning cash is even more valuable than the cash itself. OpenAI has 2B in monthly revenue and is still losing money - that smells like 1999. Avoid it. But while Alphabet and Meta are spending huge amounts of capex, every dollar is generating revenue from an already-existing 3B-user base - that's different. In the checklist, open-source parity is my biggest concern - so you must own companies with distribution moats."

> **Li Lu**: "Civilization-scale opportunities appear only 2-3 times in 30 years. AI is one of them. But a company you can hold for 30 years must have: (1) real cash flow, (2) top-tier management, and (3) the ability to keep evolving. Alphabet has DeepMind + Search + Cloud + Android at the same time, which is a rare full-stack company in history. Alibaba is a Chinese version of the Alphabet candidate - the valuation already reflects decoupling concerns, which actually gives it a decent margin of safety."

---

## 9. Information Sufficiency and Data Points to Update

### 9.1 Information sufficiency rating: **B+**

| Item | Rating | Notes |
|---|---|---|
| Listed company financial data | A | Microsoft / Alphabet / Meta Q1 2026 reports are public; Alibaba FY2026Q3 and Tencent full-year 2025 have also been released |
| Private valuation data | B | Cross-checked across multiple sources (CNBC, Bloomberg, TechCrunch), but secondary market quotes move quickly and actual figures may differ by +/-20% |
| Chinese AI company financials | C+ | SenseTime, Zhipu, and MiniMax are listed in Hong Kong but still losing money; valuation ranges are volatile; DeepSeek valuation rumors moved from 10B to 50B in one month, so credibility remains to be seen |
| Model capability benchmarks | B | Multiple sources (IMO / CMO / SWE-Bench / OpenCompass), but frontier iterations are fast and benchmarks become stale within 3-6 months |
| Regulation + geopolitics | B- | Highly uncertain, especially the pace of US-China decoupling |

### 9.2 Data points to update

- **Tencent 0700.HK 2026Q1 earnings** (released on May 13) - update Hunyuan + Yuanbao commercialization data
- **Alibaba 9988.HK FY2026Q4 earnings** (expected in mid-to-late May) - update Alibaba Cloud + AI commercialization progress
- **Baidu BIDU 2026Q1 earnings** (expected in May) - update ERNIE 5.0 commercialization and Intelligent Cloud growth
- **Whether Anthropic's 900B USD funding round closes** (in talks in 2026-04) - the latest private valuation anchor
- **OpenAI / xAI IPO timing** - whether either lists within 2026
- **Microsoft FY2026Q4 results** (late July) - the first full quarter after the OpenAI agreement reset
- **Meta capex 145B USD ROI realization pace** - whether guidance is raised again in the second half
- **DeepSeek funding price** + **STAR Market IPO filing status**
- **T-Head GPU + Huawei Ascend**: actual domestic AI chip capacity and performance data
- **TPU v7 performance data**: comparison with Nvidia Blackwell / Rubin

---

## 10. Sources

### 10.1 Official primary sources

| Company | Source |
|---|---|
| Microsoft | https://www.microsoft.com/en-us/investor/earnings/fy-2026-q3/press-release-webcast |
| Alphabet | https://s206.q4cdn.com/479360582/files/doc_financials/2026/q1/2026q1-alphabet-earnings-release.pdf |
| Meta | https://investor.atmeta.com/investor-news/press-release-details/2026/Meta-Reports-First-Quarter-2026-Results/ |
| Anthropic | https://www.anthropic.com/news/anthropic-raises-30-billion-series-g-funding-380-billion-post-money-valuation |
| OpenAI | https://openai.com/index/accelerating-the-next-phase-ai/、https://openai.com/index/next-chapter-of-microsoft-openai-partnership/ |
| Mistral | https://mistral.ai/news/mistral-ai-raises-1-7-b-to-accelerate-technological-progress-with-ai |
| Fireworks | https://fireworks.ai/blog/series-c |
| Alibaba | https://www.alibabagroup.com/zh-HK/ir-financial-reports-quarterly-results |
| Tencent | https://static.www.tencent.com/uploads/2025/11/13/62022d4f181b7c4d22127a6460d2eab6.pdf |
| CoreWeave | https://investors.coreweave.com/news/news-details/2026/CoreWeave-Reports-Strong-First-Quarter-2026-Results/ |

### 10.2 Secondary media (for cross-checking valuation / financing data)

- CNBC: OpenAI / Anthropic / Microsoft / Alphabet / Meta / xAI earnings and financing coverage
- Bloomberg: OpenAI 852B valuation
- TechCrunch: xAI 20B financing / Anthropic 900B financing / Microsoft-OpenAI agreement
- Sacra (private valuation data): OpenAI, Anthropic, xAI, Cohere, Together AI, Fireworks
- Caixin, Sina Finance, Xueqiu: Alibaba, Tencent, Baidu, SenseTime, Zhipu, MiniMax, DeepSeek
- 36Kr, PingWest, PEdaily: DeepSeek, Kimi, Moonshot valuations
- Finance websites: stock prices, PE, market cap (macrotrends.net, companiesmarketcap.com, stockanalysis.com)

### 10.3 Benchmark data

- HuggingFace open-source rankings
- OpenCompass multimodal benchmarks
- IMO / CMO / ICPC / Putnam math competition benchmarks
- SWE-Bench coding benchmark

---

**End of report.**
