# The Second Layer of the AI Five-Layer Cake: Nvidia at $5 Trillion Is Not Expensive, and SK Hynix at 7x PE Is Even Cheaper

> Research date: June 5, 2026
> Data cutoff: June 3, 2026
> Disclaimer: This report is for personal investment research only and does not constitute investment advice

---

## Core Thesis: The Chip Layer Is the Most Value-Dense Layer in the AI Value Chain

The second layer of the AI five-layer cake, the chip layer, is the most value-dense battlefield in the entire value chain. Not because it is the largest, but because it is the hardest to replace. Electricity can be supplied through nuclear, natural gas, solar, and other sources. Data centers can be built by different contractors. Models can be open-source, closed-source, or distilled. But the physical bottlenecks in the chip layer are truly hard constraints: if you cannot make HBM, you cannot build AI accelerators; if you do not have CoWoS packaging capacity, your chips are just bare dies; if you cannot buy EUV lithography tools, you do not even have a ticket to advanced manufacturing.

**How large is the market?** According to Bloomberg Intelligence, the AI accelerator market was about $116.0 billion in 2024, is expected to exceed $200.0 billion in 2026, and will surpass $600.0 billion by 2033 (source: Bloomberg Intelligence, January 2026). That is only the accelerator market itself. Including HBM memory (about $54.6 billion in 2026, source: Bank of America), advanced packaging, EDA tools, lithography equipment, and specialty materials, the chip layer's total addressable market already exceeds $300.0 billion in 2026.

**Nvidia's dominance and the cracks forming beneath it.** Nvidia holds roughly 75-80% revenue share in the AI accelerator market (source: Silicon Analysts). In FY2026, it generated $215.9 billion in full-year revenue, including $193.7 billion from data centers (source: Nvidia Q4 FY26 8-K). The CUDA ecosystem has an extremely deep moat: more than 5 million developers globally, hundreds of thousands of trained models, and deep integration with every mainstream AI framework. That cannot be replicated in one or two years. But cracks are appearing: in 2026, custom ASIC growth (+45%) systematically exceeded general-purpose GPU growth (+16%) for the first time. Google TPU is already in its seventh generation, and Meta's MTIA plus OpenAI's custom chips with Broadcom are entering mass production in the second half of 2026. Nvidia's share has retreated from its 2024 peak of 87% to 75%. This is a structural trend, not a cyclical wobble.

**HBM: the "ammunition" for AI chips.** The amount of HBM required per AI accelerator is growing exponentially: Nvidia H100 uses 80GB HBM3, B200 uses 192GB HBM3E, and Rubin uses 288GB+ HBM4. Bank of America forecasts the HBM market will reach $54.6 billion in 2026, up 58% year over year (source: Bank of America, December 2025). SK Hynix has 62% share, while Micron has overtaken Samsung with 21% versus Samsung's 17%. The key facts: HBM yields are extremely low (the yield for 12-high stacked HBM3E is about 60-70%), expansion cycles are long (new lines require 18-24 months), and the supply-demand gap is expected to persist through 2028. That means HBM suppliers have very strong pricing power over the next two years.

**Advanced packaging: the real bottleneck the market still underappreciates.** TSMC's CoWoS (Chip-on-Wafer-on-Substrate) packaging is the only mature mass-production solution for integrating GPU dies and HBM. Monthly capacity was about 35,000 wafers at the end of 2024 and is planned to expand to 130,000 wafers by the end of 2026, almost a fourfold increase, yet supply still cannot meet demand (source: TrendForce, April 2026). CoWoS wafer ASP is already approaching 7nm process levels (source: TrendForce, April 28, 2026), which means packaging is evolving from a "back-end process" into a genuine profit center. The ABF packaging substrates required by CoWoS are supplied globally mainly by a small group including Ibiden, Unimicron, and Shinko Electric, creating yet another nested bottleneck.

**Specialty gases: the invisible choke point.** NF3 (nitrogen trifluoride) is used for semiconductor chamber cleaning, and WF6 (tungsten hexafluoride) is used in tungsten deposition processes. Both are indispensable specialty gases for advanced nodes. In August 2025, a fire at Kanto Denka Kogyo's NF3 plant in Japan shook the global chip supply chain (source: TrendForce, August 14, 2025). After Mitsui Chemicals exited NF3 production in March 2026, Kanto Denka became Japan's only major NF3 supplier. WF6 is even tighter. In 2026, Japanese suppliers raised prices to Korean customers by 70-90%, while existing inventories were only sufficient through May-June 2026 (source: LDeepAI analysis). This is a company with only a $1.4 billion market cap, yet it sits on a lifeline for TSMC, Samsung, and Rapidus.

**Framework for this report:** We start with 10 companies covering the full chip-layer chain: design tools (Synopsys) -> lithography equipment (ASML) -> specialty gases (Kanto Denka Kogyo) -> manufacturing (TSMC) -> packaging substrates (Ibiden) -> memory (SK Hynix) -> optical interconnects (Coherent) -> accelerator design (Nvidia, AMD, Broadcom). For each company, we answer one core question: **What is this bottleneck worth, and is the market pricing it correctly?**

---

## 1. SK Hynix (000660.KS) - Buying AI's "Ammunition Depot" at 7x PE

### Company Overview and Bottleneck Positioning

SK Hynix is the world's second-largest memory chip manufacturer, but in the most critical AI-era memory category, HBM (high-bandwidth memory), it is the undisputed leader. HBM is the "ammunition" for AI accelerators. Without HBM, even the strongest GPU sits idle. SK Hynix holds 62% shipment share and about 57% revenue share in the HBM market (source: Astute Group, 2026), far ahead of Micron (21%) and Samsung (17%).

SK Hynix's lead is not an accident. It began co-developing HBM with Nvidia in 2013, mass-produced HBM3E two years earlier than Samsung, and has been the preferred supplier for every generation of Nvidia GPU. HBM4 development has been completed, with the company claiming a 40% improvement in power efficiency and data rates up to 10Gbps. It will be integrated into Nvidia's Rubin platform (source: SK Hynix official website and multiple media reports).

### Key Financial Data

| Metric | Data | Source |
|------|------|------|
| Full-year 2025 revenue | ~KRW 84 trillion (estimated) | CNBC, 2026/01 |
| Full-year 2025 operating profit | KRW 47.2 trillion (record high, first time surpassing Samsung) | CNBC, 2026/01 |
| Q1 2026 revenue | KRW 52.58 trillion | CNBC, 2026/04 |
| Q1 2026 operating margin | 72% (above Nvidia) | LinkedIn/analyst reports |
| Share price (2026/6/2) | KRW 2,360,000 (record high) | Yahoo Finance |
| Market cap | About KRW 1,675 trillion (~$1.16 trillion) | Multiple sources |
| P/E (TTM) | About 5.8-7x | Seeking Alpha, 2026/05 |

### Irreplaceability Analysis

**Extremely strong.** HBM is not ordinary DRAM. It requires stacking 8-16 DRAM dies vertically with TSVs (through-silicon vias), then bonding them with micro-bumps. Yield is the core barrier. SK Hynix's 12-high HBM3E yield leads Samsung by roughly 6-12 months. More importantly, every generation of HBM requires co-designing customized interfaces and signaling protocols with GPU vendors. SK Hynix has worked with Nvidia for more than 10 years. That level of deep integration cannot be caught up with simply by spending money.

Substitution risk: Micron has shown 11Gbps HBM4 samples (slightly above SK Hynix's 10Gbps), narrowing the technology gap. Samsung also claims to be the first to meet Nvidia's HBM4 pin-speed requirements. Competition in the HBM4 generation will be more intense than in HBM3E.

### Valuation View

**This is the largest pricing error in this report.** A 5.8-7x earnings multiple is absurdly cheap for a company with a 72% operating margin, sold-out capacity through 2028, and demand still exceeding supply. The market assigns a low PE because the memory industry has historically been highly cyclical, with boom-bust cycles every 3-4 years, and investors worry that HBM demand is temporary. But this time is different. AI demand for HBM is not a one-off equipment procurement cycle; it is a continuously expanding infrastructure requirement. Even assuming margins fall from 72% to 50%, the current valuation still embeds an expectation of profits being cut in half.

### Risk Factors

1. **Cyclicality risk**: Memory has never enjoyed a permanent upcycle. If AI investment slows in 2027-2028, HBM pricing may come under pressure
2. **Technology transition risk**: Samsung and Micron may narrow the gap in the HBM4 generation, and SK Hynix's share could fall from 62%
3. **Korean corporate governance discount**: Korea's chaebol structure and traditionally lower shareholder returns may limit valuation rerating potential
4. **Geopolitics**: U.S.-China technology decoupling could affect supply-chain layouts

### One-Sentence Conclusion

**Buying one of the world's most profitable chip companies at 7x PE is cheap even after a 50% haircut. This is the most severe pricing error in the chip layer.**

---

## 2. Kanto Denka Kogyo (4047.T) - The $1.4 Billion Invisible Choke Point

### Company Overview and Bottleneck Positioning

Kanto Denka Kogyo is one of Japan's largest specialty gas manufacturers. Its core products are NF3 (nitrogen trifluoride) and WF6 (tungsten hexafluoride). NF3 is used for semiconductor manufacturing equipment chamber cleaning and is required in every process step. WF6 is used for tungsten deposition in advanced nodes and is a key material for FinFET and GAA transistor structures.

After Mitsui Chemicals exited NF3 production in March 2026, Kanto Denka became Japan's only large-scale NF3 supplier, accounting for roughly 90% of Japan's NF3 capacity (source: Sourceability, 2025 reporting). Its customers include TSMC, Samsung, Micron, Kioxia, and Japan's newly built Rapidus. The August 2025 NF3 plant fire briefly triggered panic across the global chip supply chain, highlighting the critical role this small company plays in the industry.

### Key Financial Data

| Metric | Data | Source |
|------|------|------|
| FY2026 (ended 2026/3) operating profit | JPY 6.63 billion (+47%) | TipRanks/company announcements |
| FY2027 expected revenue (company guidance) | JPY 95.0 billion (+45%) | Company FY2026 earnings briefing |
| FY2027 expected operating profit | JPY 10.0 billion (+51%) | Company guidance |
| Share price (2026/6/2) | JPY 3,560 | Yahoo Finance |
| Market cap | ~JPY 208.0 billion (about $1.4 billion) | TradingView |
| P/E (TTM) | ~50x | Simply Wall St |
| 1-year share price gain | +302% | Simply Wall St |

### Irreplaceability Analysis

**Nearly the only supplier in the Japanese market.** NF3 and WF6 production requires sophisticated fluorine chemistry and strict safety controls because fluorine gas is highly toxic. Global suppliers are few. China has some capacity, but purity does not meet semiconductor-grade requirements. Korea's SK Materials has NF3 capacity, but it primarily serves internal demand. WF6 is even tighter: in 2026, Japanese suppliers raised prices to Korea by 70-90%, while inventories were only sufficient through mid-year (source: LDeepAI analysis).

Kanto Denka's moat is not patents, but process know-how and safety certification. An NF3 plant takes 2-3 years from groundbreaking to customer qualification. That is the substitution window. After the fire, Kanto Denka accelerated capacity expansion, and the expected 45% FY2027 revenue growth reflects that capacity coming online.

### Valuation View

**Complicated.** A 50x PE does not look cheap, but consider that: (1) FY2027 profit is expected to grow 51% (bringing P/E down to about 33x); (2) NF3/WF6 is in structural shortage; and (3) a $1.4 billion market cap corresponds to an invisible bottleneck holding up a trillion-dollar value chain. The valuation is not unreasonable. The real question is: how long can specialty gas price increases last? If new capacity comes online in 2027-2028 and reverses supply-demand conditions, the current valuation would look high.

### Risk Factors

1. **Safety incident risk**: The 2025 fire proves that fluorochemical production carries major safety hazards; another incident could be fatal for the thesis
2. **Demand volatility**: Specialty gas demand is highly correlated with fab utilization, so a semiconductor downcycle would directly hit revenue
3. **New entrants**: Chinese companies are developing high-purity NF3 capacity and may break Japan's monopoly over the long term
4. **Liquidity risk**: As a Japanese small-cap with a $1.4 billion market cap, foreign investors may face liquidity constraints

### One-Sentence Conclusion

**A $1.4 billion market cap sits on a trillion-dollar supply-chain choke point. WF6 price hikes of 70-90% show extreme tightness, but safety-incident risk and cyclicality need close monitoring.**

---

## 3. Ibiden (4062.T) - The "Foundation" Under the GPU

### Company Overview and Bottleneck Positioning

Ibiden is a global leader in ABF (Ajinomoto Build-up Film) packaging substrates. ABF substrates are the "bridge" between chips and circuit boards. Every Nvidia GPU, AMD CPU, and Broadcom ASIC needs an ABF substrate underneath it. Without the substrate, the chip is just a bare die that cannot be soldered into a system.

The ABF substrate market is highly concentrated: Unimicron (~22%), Ibiden, Shinko Electric, AT&S, and Nan Ya PCB together account for 74% share (source: Intel Market Research, 2026). Ibiden's differentiation lies in high-end AI/GPU substrates. Nvidia's H100 and B200 series GPU substrates are primarily supplied by Ibiden and Shinko. In February 2026, Ibiden announced a JPY 500.0 billion capital expenditure plan for AI substrate expansion, with customer prepayments already reaching JPY 92.1 billion (source: Ibiden IR materials).

### Key Financial Data

| Metric | Data | Source |
|------|------|------|
| FY2025 revenue forecast | ~JPY 106.65 billion | Investing.com |
| Share price (2026/6/2) | JPY 21,135 | Yahoo Finance |
| Market cap | ~JPY 4.3-5.9 trillion (about $29.0-40.0 billion) | Multiple sources (differences may reflect different dates) |
| P/E (TTM) | ~27x | CompaniesMarketCap |
| Customer prepayments | JPY 92.1 billion | Ibiden IR |
| Capital expenditure plan | JPY 500.0 billion | Ibiden announcement, 2026/02 |

### Irreplaceability Analysis

**Moderately strong to strong.** ABF substrates have high technical barriers, including multilayer precision wiring and thermal expansion coefficient control, but the competitive landscape is less concentrated than HBM. Unimicron has a larger market share, and Shinko Electric (acquired by Resonac) is also a strong competitor. Ibiden's advantages are: (1) deep ties with Nvidia as a GPU substrate supplier; and (2) customer prepayments backing its JPY 500.0 billion expansion, showing that customers are willing to pay to secure capacity.

Substitution risk: ABF substrate expansion cycles are about 12-18 months, shorter than HBM but still long enough to provide a protected window. Glass substrates are the long-term alternative technology path. Intel is already developing them, but mass production is unlikely before at least 2028.

### Valuation View

**Reasonable but somewhat expensive.** A 27x PE is not cheap for a Japanese manufacturing company, but the JPY 500.0 billion expansion plan implies substantial revenue and profit growth over the next 2-3 years. If AI substrate revenue rises from about 30% today to 50%+, the valuation has room to rerate. That said, large-scale capital expenditure also means near-term free cash flow pressure.

### Risk Factors

1. **Capital expenditure risk**: JPY 500.0 billion is a massive investment; if AI demand disappoints, it could lead to overcapacity
2. **Intensifying competition**: Unimicron and AT&S are also expanding AI substrate capacity, creating price-war risk
3. **Technology substitution**: Glass substrates could disrupt ABF substrates over the long term, though there is no material threat in the short term (within 3 years)
4. **Customer concentration risk**: Highly dependent on a small number of major customers such as Nvidia

### One-Sentence Conclusion

**A supplier of the GPU's "foundation." JPY 92.1 billion in customer prepayments confirms real demand, and 27x PE is reasonable during a large expansion phase, but it is not the cheapest option.**

---

## 4. Nvidia (NVDA) - The $5 Trillion Monopolist, Still Not Expensive at 26x PE

### Company Overview and Bottleneck Positioning

Nvidia needs no introduction. It defined the AI accelerator market, holds 75-80% revenue share, and its CUDA ecosystem is the "operating system" of AI computing. Every company training large models globally uses Nvidia GPUs, not because there are no alternatives, but because switching costs are too high.

Nvidia's bottleneck position is not the hardware itself, since AMD and ASICs are catching up, but the **software ecosystem**. CUDA has more than 5 million developers, 300+ accelerated libraries, and native support across all mainstream AI frameworks. This is a classic network effect: more users -> more complete libraries -> new users are more likely to choose CUDA -> even more users. Breaking that loop requires 5-10 years.

### Key Financial Data

| Metric | Data | Source |
|------|------|------|
| Full-year FY2026 revenue | $215.9 billion (+65%) | Nvidia Q4 FY26 8-K |
| Data center revenue | $193.7 billion (+68%) | Nvidia Q4 FY26 8-K |
| Q4 FY26 quarterly revenue | $68.1 billion (+73%) | Nvidia Q4 FY26 8-K |
| Gross margin | ~73-75% | Nvidia financial reports |
| Market cap (2026/6) | ~$5.28 trillion | CompaniesMarketCap |
| Trailing P/E | ~32.9x | MacroTrends |
| Forward P/E | ~21.6-25x | GuruFocus/StockAnalysis |

### Irreplaceability Analysis

**Extremely strong, but slowly being diluted.** CUDA's ecosystem moat is real, but the rise of custom ASICs means the largest 5-6 customers (Google, Meta, Amazon, Microsoft, OpenAI) are developing their own chips. Broadcom has confirmed 6 major XPU customers. This will not eliminate Nvidia, since general-purpose GPUs remain the training standard, but it will erode its monopoly in inference.

Nvidia's response is to go "full stack": from chips to systems (DGX SuperPOD), software (NIM, CUDA-X), and networking (Spectrum-X), locking customers into the entire ecosystem. It is a smart strategy, but it also means Nvidia is moving from a high-margin chip company toward a systems integrator, which could pressure long-term gross margins.

### Valuation View

**A 22-25x forward PE is genuinely not expensive for Nvidia.** FY2026 revenue was $215.9 billion. Assuming FY2027 growth of 40-50% (Wall Street consensus is about 45%), revenue would exceed $300.0 billion. At a 30% net margin, net income would be about $90.0 billion, and a $5.28 trillion market cap would imply about 22x forward PE. For a company growing 40%+ with 73%+ gross margins, that valuation sits in a reasonable to slightly cheap range.

On the other hand, a $5.28 trillion market cap means the market has already priced in Nvidia sustaining high growth for the next 5 years. If the AI investment cycle sees a 2018 crypto-like correction (Nvidia FY2019 revenue fell 7%), this market cap may not hold up.

### Risk Factors

1. **Custom ASIC erosion**: Share falling from 87% to 75% has already happened and could continue toward 60-65%
2. **Export controls**: U.S. restrictions on chip exports to China have already affected about 10-15% of Nvidia's potential revenue
3. **Valuation sensitivity**: A $5 trillion market cap is extremely sensitive to growth expectations; every 10 percentage point growth decline could drive a 15-20% share-price correction
4. **Capital expenditure cycle**: Hyperscaler capex cannot grow at 50%+ forever; the timing of the inflection point is the core uncertainty

### One-Sentence Conclusion

**The world's best AI company, trading at 22-25x forward PE for 40%+ growth. The valuation is reasonable. The risk is not valuation, but when the growth inflection arrives.**

---

## 5. TSMC (TSM) - Dual Monopoly in Advanced Nodes and CoWoS

### Company Overview and Bottleneck Positioning

TSMC is the only foundry in the world that can mass-produce 3nm/2nm advanced nodes. Samsung has lines, but its yield gap remains significant. TSMC also dominates CoWoS advanced packaging, the key process for integrating GPU dies and HBM. Put simply, **whether you use Nvidia GPUs, Broadcom ASICs, or Google TPUs, the chips ultimately pass through TSMC's factories.**

In Q1 2026, advanced nodes (7nm and below) accounted for 74% of TSMC's total revenue, with 3nm at 25% and 5nm at 36% (source: TSMC Q1 2026 6-K). CoWoS monthly capacity rose from 35,000 wafers at the end of 2024 toward a planned 130,000 wafers by the end of 2026, but demand still exceeds supply, and Nvidia has reserved most of the capacity (source: multiple TrendForce reports in 2026).

### Key Financial Data

| Metric | Data | Source |
|------|------|------|
| Full-year 2025 revenue | TWD 3.81 trillion (+32%) | TSMC financial reports |
| Q1 2026 revenue | TWD 1.13 trillion (about $35.9 billion) | TSMC Q1 2026 6-K |
| Q2 2026 guidance | $39.0-40.2 billion | TSMC Q1 2026 6-K |
| 2026 capex budget | $52.0-56.0 billion | TSMC guidance |
| Gross margin | ~58-59% | TSMC financial reports |
| Market cap (2026/6) | ~$2.26 trillion | CompaniesMarketCap |
| P/E (TTM) | ~34.8x | GuruFocus |
| Forward P/E | ~21.8x | StockAnalysis |

### Irreplaceability Analysis

**The strongest, almost impossible to replace.** Advanced-node foundry manufacturing has the highest technical barriers in global manufacturing. A 3nm fab requires more than $20.0 billion in investment, 3-4 years of construction, and another 1-2 years for yield ramp. Samsung is 1-2 generations behind TSMC technologically, and Intel Foundry is still restructuring. In CoWoS packaging, TSMC is also the de facto standard.

The only "substitution" comes from the demand side: if chip designers move toward chiplet architectures to reduce reliance on a single large die, or if the UCIe standard matures enough for more packaging houses to handle heterogeneous integration, TSMC's monopoly could loosen. But that is more than 5 years away.

### Valuation View

**A 35x TTM PE and 22x forward PE are reasonable for the world's most irreplaceable manufacturer.** Annual capex of $52.0-56.0 billion means TSMC is laying the groundwork for growth over the next 3-5 years. If CoWoS packaging truly becomes a profit center (with ASP approaching 7nm levels), TSMC's profit mix will improve further.

On the other hand, TSMC faces geopolitical risk. The Taiwan Strait is the Sword of Damocles hanging over every TSMC investor. U.S. fabs in Arizona can partly mitigate that risk, but costs are 30-50% higher.

### Risk Factors

1. **Geopolitical risk**: The Taiwan Strait is a tail risk that cannot be ignored
2. **Rising capital intensity**: Investment roughly doubles with each process generation, and returns on capital may decline
3. **Customer concentration**: Apple + Nvidia + AMD + Qualcomm account for 50%+ of revenue, giving major customers strong bargaining power
4. **U.S. fab costs**: Arizona fabs cost 30-50% more than Taiwan fabs and may drag on margins

### One-Sentence Conclusion

**The most irreplaceable manufacturer on Earth, and 22x forward PE is a reasonable price. The only truly material risk is geopolitics.**

---

## 6. Broadcom (AVGO) - King of Custom ASICs

### Company Overview and Bottleneck Positioning

Broadcom is the absolute leader in custom AI ASICs. It designed seven generations of TPU for Google, designed MTIA for Meta, signed a multi-year agreement with OpenAI to develop 10GW-scale custom accelerators, and is designing chips for other hyperscale customers (reportedly including Anthropic). In early 2026, CEO Hock Tan said there was a "clear line of sight" to the 2027 target of more than $100.0 billion in chip AI revenue, backed by a $73.0 billion AI backlog (source: Broadcom financial reports and multiple media reports).

Broadcom's role is that of an "arms dealer for custom chip design and advanced packaging IP": the customer defines the desired performance, and Broadcom designs the chip and coordinates TSMC manufacturing. The beauty of this model is that Broadcom does not carry inventory or sales risk for the chips. It earns high-margin revenue from design services and IP licensing.

### Key Financial Data

| Metric | Data | Source |
|------|------|------|
| Q1 FY2026 AI semiconductor revenue | $8.4 billion (+106%) | Tech-Insider, 2026 |
| Q2 FY2026 AI guidance | $10.7 billion | Company guidance |
| Full-year 2026 AI revenue forecast | $46.0 billion (+134%) | Analyst forecasts |
| AI backlog | $73.0 billion | Company financial reports |
| Market cap (2026/6) | ~$1.96 trillion | StockAnalysis |
| P/E (TTM) | ~81-94x | Multiple sources |
| Forward P/E | ~31-37x | GuruFocus/StockAnalysis |

### Irreplaceability Analysis

**Strong, but being diluted.** In custom ASICs, Broadcom's main competitor is Marvell Technology, which designs Trainium for Amazon. Google is reportedly also negotiating with Marvell to open a second supplier for inference chips. But Broadcom's advantage lies in scale and experience: seven TPU generations, combined with full-stack capabilities in SerDes, networking IP, and advanced packaging know-how, make it the preferred choice for most hyperscale customers.

Substitution risk: if hyperscale customers build their own chip design teams (Google already has a chip team of several thousand people), long-term dependence on Broadcom may decline. But designing an advanced AI ASIC requires 2-3 years and billions of dollars of investment, so customers are unlikely to fully internalize it in the short term.

### Valuation View

**31-37x forward PE is not expensive for 134% AI revenue growth, but investors need to watch the drag from non-AI businesses.** Broadcom is not a pure AI company. It also owns VMware (enterprise software), networking equipment, storage, and other businesses that grow far more slowly than AI. If valued only on the AI business, the stock would be more attractive. But as a consolidated company, the complexity of the business mix matters.

### Risk Factors

1. **Customer concentration risk**: Google may account for 40%+ of AI revenue; if Google accelerates internal design, the impact would be large
2. **Marvell competition**: Direct competition in Amazon and potentially Google's inference chips
3. **VMware integration risk**: The $69.0 billion VMware acquisition completed at the end of 2023 is still being integrated and may distract management
4. **Sustainability of pricing power**: As customers improve their own chip design capabilities, Broadcom's design-service premium may compress

### One-Sentence Conclusion

**The biggest winner in custom ASICs, with a $73.0 billion backlog providing more than 3 years of visibility. A 31-37x forward PE is reasonable, but not being a pure AI company deserves a valuation discount.**

---

## 7. Coherent (COHR) - The Photon Era Has Arrived

### Company Overview and Bottleneck Positioning

Coherent is a global leader in optoelectronic components. Its core products are indium phosphide (InP)-based laser chips and optical transceiver modules used for high-speed optical interconnects in AI data centers. When AI clusters expand from a single rack to cross-data-center deployments, copper cables hit physical limits because signal attenuation becomes severe beyond 100 meters. Fiber is the only option. The core of an optical transceiver module is the InP laser chip, a compound semiconductor that cannot be made from silicon.

Coherent is transitioning from 4-inch InP wafers to 6-inch wafers and operates 6-inch production lines in Sherman, Texas and Jarfalla, Sweden (source: TradingKey analysis, 2026). The data center business has a book-to-bill ratio above 4x, meaning that for every $1 of revenue, it receives more than $4 of new orders. That is a classic signal of severe undersupply. Nvidia has signed a $2.0 billion strategic cooperation agreement with Coherent (source: LongYield analysis).

### Key Financial Data

| Metric | Data | Source |
|------|------|------|
| Q2 FY2026 revenue | $1.7 billion (+17.5%) | Futurum Group |
| Data center revenue | $1.2 billion (+33.6%) | Futurum Group |
| FY2025 revenue | $5.8 billion | SEC 8-K |
| FY2028E revenue forecast | $10.6 billion | Analyst forecasts |
| Share price (2026/6) | ~$398 | Yahoo Finance |
| Market cap | ~$81.7 billion | Yahoo Finance |
| P/E (TTM) | ~89-204x (wide variation depending on calculation method) | Multiple sources |
| Forward P/E | ~44x | GuruFocus |
| Data center book-to-bill | >4x | Analyst reports |

### Irreplaceability Analysis

**Strong, but the playing field is widening.** InP optical components are in severe global shortage today, with a demand gap of about 70%. Coherent is one of the largest capacity suppliers, alongside Lumentum. Mass-producing 6-inch InP wafers has high barriers: material preparation, epitaxial growth, and device-processing yield control all require years of accumulated know-how.

Substitution risk: silicon photonics technology is maturing, and Intel, Cisco, and Broadcom are all advancing it. Silicon photonics can be manufactured with traditional silicon processes, giving it lower costs and higher yields, but it still trails InP in high-performance scenarios such as 800G/1.6T long-distance transmission. Over the long term, silicon photonics may replace InP in short- and medium-distance use cases, but InP's position in the high-end market should remain solid in the medium term (3-5 years).

### Valuation View

**At 44x forward PE, the market has already priced in most of the growth expected from a company facing undersupply and book-to-bill above 4x.** Coherent's issue is that it is not a pure InP company. It also has slower-growth businesses such as industrial lasers and materials, which drag on overall margins. If the data center business could be valued independently, the story would be more attractive. At the current price, this is more a case of "right direction, elevated price."

### Risk Factors

1. **Silicon photonics substitution risk**: The largest medium- to long-term threat
2. **Capacity ramp risk**: Unstable yields on 6-inch InP lines may affect delivery
3. **High valuation risk**: A 44x forward PE already reflects optimistic expectations; slower growth would drive multiple compression
4. **Drag from non-AI businesses**: Industrial lasers and other businesses grow slowly and lower overall margins

### One-Sentence Conclusion

**A core supplier for AI data center optical interconnects. The undersupply is real, but a 44x forward PE means the market has already noticed. Not cheap, but the direction is right.**

---

## 8. ASML (ASML) - EUV Lithography, No Alternative

### Company Overview and Bottleneck Positioning

ASML is the sole supplier of EUV (extreme ultraviolet) lithography tools. 100% of the world's EUV lithography tools come from ASML. Without EUV, there are no advanced chips below 7nm: no AI GPUs, no HBM, and no advanced-node products of any kind. It is not one monopolist among several. It is literally the only one.

An EUV lithography tool (NXE series) costs about $180.0-200.0 million, while the latest High-NA EUV (EXE series) costs $350.0-400.0 million. ASML's backlog reached EUR 38.8 billion at the end of 2025 (source: ASML Q4 2025 6-K), including a record EUR 13.2 billion in orders during Q4 2025 alone. SK Hynix has committed to buying about 30 EUV tools by December 2027, and Samsung plans to buy 20 units for its Pyeongtaek P5 fab (source: ASML statistics).

### Key Financial Data

| Metric | Data | Source |
|------|------|------|
| Full-year 2025 revenue | EUR 32.7 billion | ASML 6-K |
| 2025 EUV revenue | EUR 11.6 billion (+39%) | ASML 6-K |
| Q1 2026 revenue | EUR 8.8 billion | ASML Q1 2026 |
| Full-year 2026 guidance | EUR 36.0-40.0 billion | ASML guidance |
| Gross margin guidance | 51-53% | ASML guidance |
| Backlog (end-2025) | EUR 38.8 billion | ASML 6-K |
| Market cap (2026/6) | ~$621.6 billion | Analyst data |
| P/E (TTM) | ~57-59x | Multiple sources |
| Forward P/E | ~40-46x | GuruFocus |

### Irreplaceability Analysis

**Irreplaceable, literally.** The EUV lithography tool supply chain is itself an unrepeatable miracle: Zeiss supplies the optical system, Trumpf supplies the laser source, and Berliner Glas supplies mirrors. Every link is a sole-source supplier. An entire EUV tool contains more than 100,000 parts and over 40 subsystems. No second company can build it.

China has been completely excluded from EUV supply by U.S. export controls. Japan's Nikon has no mass-production EUV solution, and Canon is exploring nanoimprint lithography (NIL), but it is far from mature. ASML's monopoly will not be broken in the foreseeable future (10 years+).

### Valuation View

**A 40-46x forward PE is a monopoly premium, but it is not cheap.** ASML's problem is not competition, but growth rate. EUV capacity expansion is constrained by supply-chain bottlenecks, especially Zeiss's limited annual capacity for optical systems, so annual shipment growth may be only 15-20%. The EUR 38.8 billion backlog provides extremely high revenue visibility, but it also means short-term growth is capped by capacity.

For investors seeking certainty, ASML is an excellent choice: monopoly + backlog + irreplaceability. For investors seeking value for money, a 40-46x forward PE requires 5-7 years of earnings growth to "digest" the valuation.

### Risk Factors

1. **Valuation risk**: A 40-46x forward PE requires sustained high growth to be justified
2. **Geopolitics**: Expanded export controls could reduce the addressable market
3. **Lithography technology roadmap**: Alternative technologies such as nanoimprint lithography (NIL) and directed self-assembly (DSA) are far from mature, but cannot be completely ruled out
4. **Cyclicality**: Semiconductor capex is cyclical; in downcycles, ASML orders can fall sharply, as in 2023

### One-Sentence Conclusion

**The most irreplaceable equipment company on Earth, but a 40-46x forward PE shows the market knows it. Whether paying a premium for certainty is worthwhile depends on your investment horizon.**

---

## 9. AMD (AMD) - The Only General-Purpose GPU Challenger

### Company Overview and Bottleneck Positioning

AMD is the only company that can challenge Nvidia in the general-purpose AI GPU market. Its MI300/MI350 accelerator series has won large-scale customer validation: OpenAI selected AMD to build 6GW of compute capacity (MI450 deployment starts in the second half of 2026), Meta committed to a multi-year contract (MI450, with contract value of about $60.0 billion), and AMD's data center revenue reached a record $16.6 billion in 2025 (source: AMD 8-K, January 2026).

AMD's value is not in "beating Nvidia," which is unrealistic in the near to medium term. Its value is in giving customers a "second choice." When Nvidia GPUs are undersupplied and aggressively priced, AMD offers an alternative with 80-90% of the performance at a lower price. For inference workloads, which do not require top-tier training performance, AMD's value-for-money advantage is more obvious.

### Key Financial Data

| Metric | Data | Source |
|------|------|------|
| 2025 data center revenue | $16.6 billion (+32%) | AMD 8-K |
| Q1 2026 data center revenue | $5.8 billion (+57%) | AMD Q1 2026 8-K |
| Q1 2026 data center share | >50% of total revenue | AMD financial reports |
| 3-5 year target data center AI revenue CAGR | 80%+ | AMD Analyst Day, 2025/11 |
| Market cap (2026/6) | ~$350.0-400.0 billion (estimated) | Multiple sources |
| Forward P/E | ~45-69x (wide source variation) | GuruFocus/multiple sources |

### Irreplaceability Analysis

**Moderate.** AMD is narrowing the hardware performance gap with Nvidia (MI350 versus B200, MI450 versus the next generation), but the software ecosystem (ROCm versus CUDA) is the biggest weakness. ROCm's compatibility and stability still lag CUDA, and bug reports in large-model training remain frequent. AMD is investing heavily in ROCm development, but catching up in software ecosystems takes 3-5 years.

AMD's real value lies in EPYC server CPUs. Its cloud server market share has already exceeded 30%, and AI inference is increasingly running on CPUs. The CPU+GPU combination differentiates AMD from pure GPU suppliers.

### Valuation View

**Complicated.** Forward PE ranges from 45-69x, with source variation reflecting different earnings forecasts. That multiple corresponds to an 80%+ data center AI revenue CAGR target. If AMD delivers that growth, the current valuation is supportable. If growth disappoints, for example because OpenAI and Meta orders are delayed, the valuation will face significant compression.

Compared with Nvidia's 22-25x forward PE, AMD is actually more expensive: a higher PE with a weaker market position. That reflects the market's "challenger premium" for AMD, betting on share-gain optionality rather than absolute earnings certainty.

### Risk Factors

1. **Software ecosystem gap**: The gap between ROCm and CUDA may be harder to close than the hardware gap
2. **Order execution risk**: There is uncertainty around whether OpenAI's and Meta's very large orders can be delivered on schedule
3. **Elevated valuation**: Relative to Nvidia, AMD has a higher PE but a weaker market position
4. **Custom ASIC erosion**: AMD faces not only Nvidia competition, but also substitution from Broadcom/Marvell custom ASICs

### One-Sentence Conclusion

**The only general-purpose GPU challenger. OpenAI and Meta endorsements matter, but valuation is expensive relative to Nvidia. Investors are paying for share gains, not monopoly economics.**

---

## 10. Synopsys (SNPS) - The "Water and Electricity" of Chip Design

### Company Overview and Bottleneck Positioning

Synopsys and Cadence together control about 85% of the global EDA (electronic design automation) market (source: HeyGoTrade analysis). EDA software is the foundational tooling for chip design. From logic synthesis and place-and-route to timing analysis and physical verification, no chip can be designed without EDA software. Every Nvidia GPU, AMD CPU, Broadcom ASIC, and Apple chip globally is designed using Synopsys or Cadence tools.

In July 2025, Synopsys completed its $35.0 billion acquisition of Ansys (source: multiple media reports), expanding from EDA into simulation and analysis, creating full-chain coverage across "design + verification + simulation." After the merger, Synopsys holds about 46% EDA market share.

### Key Financial Data

| Metric | Data | Source |
|------|------|------|
| Q2 FY2026 revenue | $2.276 billion (vs Q2 FY2025 $1.604 billion) | Synopsys 8-K |
| Full-year FY2026 guidance | $9.56-9.66 billion | Company guidance |
| Backlog | $11.4 billion | Analyst reports |
| Market cap (2026/6) | ~$97.3 billion | Yahoo Finance |
| P/E (TTM) | ~116x | MacroTrends |
| Forward P/E | ~35x | FullRatio |

### Irreplaceability Analysis

**Extremely strong.** EDA is a classic duopoly. Synopsys and Cadence have alternated leadership for decades, and no third company has ever truly threatened them. The reason is simple: chip design workflows depend heavily on the completeness and reliability of toolchains. Switching EDA vendors means revalidating every design flow, at extremely high cost. Customer stickiness is reflected in Synopsys's $11.4 billion backlog and high renewal rates.

AI affects EDA in two ways: (1) AI chip design complexity is exploding (a B200 has more than 200 billion transistors), requiring more and more expensive EDA tools; and (2) AI itself is being used to accelerate chip design, such as Synopsys's AI-driven synthesis tools, which may increase the tools' pricing power.

### Valuation View

**A 35x forward PE is reasonable for a software company growing steadily at 15-20% and facing almost no substitution risk.** But there are two issues: (1) the 116x TTM PE reflects one-off costs from the Ansys acquisition and is not representative; and (2) integration risk from the $35.0 billion Ansys acquisition remains. If synergies disappoint, margins may come under pressure.

Compared with Cadence, which also grows around 17% and trades in a similar valuation range, Synopsys has the additional upside from Ansys simulation, but also more integration risk. Between the two, Synopsys has slightly higher odds.

### Risk Factors

1. **Ansys integration risk**: A $35.0 billion mega-acquisition creates uncertainty around cultural integration and whether cross-selling meets expectations
2. **Growth ceiling**: The total EDA market is about $15.0-18.0 billion, and growth is constrained by the number of global chip design starts
3. **Open-source EDA threat**: Google-backed open-source EDA tools such as OpenROAD have made some progress in low-end markets, though they do not threaten high-end workflows in the short term
4. **Not cheap**: A 35x forward PE for 15-20% growth implies a PEG of about 1.8-2.3x, which is not undervalued

### One-Sentence Conclusion

**The "water and electricity" of chip design. The duopoly is secure, and 35x forward PE is reasonable but not cheap. The success or failure of Ansys integration is the key variable over the next two years.**

---

## Conclusion: Which Names Deserve Deeper Research?

### Ranked by Valuation Appeal

| Rank | Company | Forward P/E | Core Thesis | Depth of Further Research |
|------|------|---------|----------|------------------|
| **1** | **SK Hynix** | **5.8-7x** | 62% HBM share + 72% operating margin + 7x PE | **★★★★★** |
| **2** | **Nvidia** | **22-25x** | $5 trillion market cap but only 22-25x forward PE, 40%+ growth | **★★★★★** |
| **3** | **TSMC** | **22x** | Dual monopoly + 22x forward PE; geopolitics is the only real risk | **★★★★★** |
| 4 | Kanto Denka Kogyo | ~33x (FY27E) | $1.4 billion choke point, but safety-incident and cycle risks | ★★★★ |
| 5 | Broadcom | 31-37x | Custom ASIC leader + $73.0 billion backlog, but not pure AI | ★★★★ |
| 6 | Synopsys | ~35x | Duopoly + irreplaceability, but Ansys integration risk | ★★★ |
| 7 | Ibiden | ~27x | GPU substrate demand is real, but the competitive landscape is less concentrated than HBM | ★★★ |
| 8 | ASML | 40-46x | Absolute monopoly, but fully priced by the market; growth constrained by capacity | ★★★ |
| 9 | Coherent | ~44x | Right direction, but valuation already reflects expectations | ★★ |
| 10 | AMD | 45-69x | Challenger premium; more expensive than Nvidia despite a much weaker position | ★★ |

### The Three Names Most Worth Deeper Research

**No. 1: SK Hynix.** Buying the HBM leader with 62% share at 7x PE, a 72% operating margin above Nvidia's, and capacity sold out through 2028. The market is pricing it as a traditional cyclical memory stock, but AI demand for HBM is structural rather than cyclical. Even if margins fall from 72% to 50%, the current valuation still offers a significant margin of safety. This is the clearest pricing error across the entire chip layer.

**No. 2: Nvidia.** A $5 trillion market cap looks intimidating, but a 22-25x forward PE for 40%+ growth implies a PEG of about 0.5-0.6x, cheaper than most technology stocks. CUDA's ecosystem moat, execution on the full-stack strategy, and the $193.7 billion revenue scale of the data center business make Nvidia the most certain beneficiary in the AI value chain. The risk is the timing of the growth inflection, not valuation itself.

**No. 3: TSMC.** Dual monopoly in advanced nodes and CoWoS, 22x forward PE, and $52.0-56.0 billion in capex laying the foundation for future growth. Geopolitics is the only truly material risk, but it is also why TSMC cannot be replaced: there is no second company globally that can replicate TSMC's manufacturing capability within 2-3 years.

### Final Word

**The investment logic for the chip layer is simple: identify physical-world bottlenecks that cannot be quickly replaced by software, capital, or time, then ask whether the market has correctly priced that irreplaceability. SK Hynix at 7x PE is a clear pricing error. Nvidia and TSMC at 22-25x forward PE are good businesses at reasonable prices. The other 7 companies are either already fully priced or not quite as irreplaceable.**

---

> **Data source note:** The data in this report comes from public company filings with the SEC/Japan Financial Services Agency (8-K, 6-K, 10-Q), Bloomberg Intelligence, Bank of America, TrendForce, Silicon Analysts, Seeking Alpha, GuruFocus, Yahoo Finance, CompaniesMarketCap, and other public sources. Some valuation data varies by source and calculation method; multiple sources are noted where possible for cross-checking. All forward-looking data is based on analyst consensus forecasts, and actual results may differ materially.

Sources:
- [CNBC - SK Hynix record Q1 2026 profit](https://www.cnbc.com/2026/04/23/sk-hynix-earnings-ai-memory-shortage-hbm-demand.html)
- [CNBC - SK Hynix overtakes Samsung in annual profit](https://www.cnbc.com/2026/01/29/sk-hynix-beats-samsung-2025-profit-ai-memory-hbm.html)
- [Seeking Alpha - SK Hynix trading at 7x](https://seekingalpha.com/article/4837148-sk-hynix-trading-7x-growing-hbm-complexity)
- [Astute Group - SK hynix holds 62% of HBM](https://www.astutegroup.com/news/general/sk-hynix-holds-62-of-hbm-micron-overtakes-samsung-2026-battle-pivots-to-hbm4/)
- [Bloomberg Intelligence - AI Accelerator Market $600B by 2033](https://www.bloomberg.com/company/press/ai-accelerator-market-looks-set-to-exceed-600-billion-by-2033-driven-by-hyperscale-spending-and-asic-adoption-according-to-bloomberg-intelligence/)
- [Nvidia Q4 FY26 CFO Commentary](https://www.sec.gov/Archives/edgar/data/0001045810/000104581026000019/q4fy26cfocommentary.htm)
- [TrendForce - CoWoS ASP nears 7nm](https://www.trendforce.com/news/2026/04/28/news-tsmc-cowos-wafer-asp-reportedly-nears-7nm-levels-advanced-packaging-poised-to-become-a-key-profit-driver/)
- [TrendForce - Kanto Denka fire threatens NF3 supply](https://www.trendforce.com/news/2025/08/14/news-japans-kanto-denka-kogyo-fire-threatens-nf%E2%82%83-supply-alerts-chipmakers-like-tsmc-and-rapidus/)
- [LDeepAI - WF6 Sourcing Crisis](https://www.ldeepai.com/tech-hub/wf6-sourcing-crisis-market-analysis-semiconductor-supply-chain-risks-2026/)
- [Broadcom AI Revenue Surges 106%](https://tech-insider.org/broadcom-ai-revenue-custom-chips-2026/)
- [Tom's Hardware - Custom AI ASICs May 2026](https://www.tomshardware.com/tech-industry/semiconductors/custom-ai-asics-examined-from-broadcom-to-mtia)
- [TSMC Q1 2026 6-K](https://www.sec.gov/Archives/edgar/data/1046179/000104617926000199/a1q26e_withguidancexfinal.htm)
- [ASML Q1 2026 Revenue](https://www.sec.gov/Archives/edgar/data/937966/000162828026025147/presentationinvestorrela.htm)
- [AMD Q1 2026 Earnings](https://www.sec.gov/Archives/edgar/data/0000002488/000000248826000072/amdq126earningsslidesfin.htm)
- [Synopsys Q2 FY2026 8-K](https://www.sec.gov/Archives/edgar/data/0000883241/000119312526241911/d126227dex991.htm)
- [Futurum - Coherent Q2 FY2026](https://futurumgroup.com/insights/coherent-q2-fy-2026-ai-datacenter-demand-lifts-revenue-and-margins/)
- [GuruFocus - Nvidia Forward PE](https://www.gurufocus.com/term/forward-pe-ratio/NVDA)
- [GuruFocus - ASML Forward PE](https://www.gurufocus.com/term/forward-pe-ratio/ASML)
- [GuruFocus - Broadcom Forward PE](https://www.gurufocus.com/term/forward-pe-ratio/AVGO)
- [GuruFocus - AMD Forward PE](https://www.gurufocus.com/term/forward-pe-ratio/AMD)
- [Silicon Analysts - Nvidia AI GPU Market Share](https://siliconanalysts.com/analysis/nvidia-ai-accelerator-market-share-2024-2026)
- [Ibiden Deep Analysis - Capital Blueprint](https://capitalblueprint.substack.com/p/ibiden-co-ltd-tyo-4062-deep-analysis)
- [Synopsys vs Cadence EDA Duopoly](https://www.heygotrade.com/en/blog/synopsys-vs-cadence-snps-vs-cdns-eda-duopoly-ai-chip-boom/)
- [Simply Wall St - Kanto Denka valuation](https://simplywall.st/stocks/jp/materials/tse-4047/kanto-denka-kogyo-shares/news/a-look-at-kanto-denka-kogyos-valuation-after-its-fy2026-resu)
