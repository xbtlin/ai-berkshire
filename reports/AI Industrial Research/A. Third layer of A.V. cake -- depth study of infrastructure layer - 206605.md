# AI Five-Layer Cake, Layer 3: $725 Billion Is Being Spent. Who Captures It?

> Research date: June 5, 2026
> Coverage: 10 core infrastructure-layer companies
> Data sources: Company financial reports (SEC 8-K/10-Q), sell-side research, industry databases

---

## I. Core Logic: Where Does the $725 Billion from the Major Cloud Vendors Go?

### 1. An unprecedented capex cycle

In 2026, the five major hyperscalers (Amazon, Google, Meta, Microsoft, and Oracle) are expected to spend a combined $725 billion in capital expenditures, up 64% YoY from $443 billion in 2025 and nearly triple the $256 billion spent in 2024.

The breakdown is roughly as follows: Amazon leads at about $200 billion, followed by Google at $175-185 billion, Microsoft at more than $120 billion, Meta at $115-135 billion, and Oracle at about $50 billion. What do these numbers mean? Some hyperscalers' capital intensity (capex/revenue) has already reached 45-57%, a level never seen historically. In plain terms, for every two dollars of revenue, one dollar is being poured back into infrastructure.

Goldman Sachs expects cumulative hyperscaler capex over 2025-2027 to reach $1.15 trillion, 2.4x the $477 billion spent over 2022-2024. This is not a "cyclical" increase in spending; it is a structural paradigm shift.

### 2. Where is the money going?

Of the $725 billion, about 75% (roughly $545 billion) is directed straight into AI infrastructure, across four major areas:

**First, servers and GPU clusters.** This is the largest slice of the pie. NVIDIA GPUs (GB200/B200) remain in short supply, but server assembly, racks, and power distribution are the real physical bottlenecks. Dell shipped $25 billion of AI servers in fiscal 2026 and guided fiscal 2027 revenue to double to $50 billion. Celestica, a leading contract manufacturer, has already crossed the $4 billion quarterly revenue mark.

**Second, network switching and interconnect.** The core of an AI cluster is not single-GPU compute, but communication efficiency between GPUs. Ethernet upgrades from 400G to 800G and then to 1.6T are non-discretionary. Arista leads the 800G Ethernet switch market, while Amphenol holds roughly 33% share in high-speed connectors. Optical modules (Zhongji Innolight, Coherent) and optical fiber (Corning) form the physical foundation of network transmission.

**Third, power and power-distribution systems.** A typical AI data-center rack has jumped from the traditional 5-10 kW to 50-120 kW. Whole-facility power demand is multiplying, making power distribution cabinets, UPS systems, transformers, and 800V DC systems key bottlenecks. Vertiv and Eaton are the two giants in this lane, while nVent is moving quickly into cabinets and power distribution.

**Fourth, liquid cooling systems.** Once rack power exceeds 50 kW, traditional air cooling no longer works, and liquid cooling becomes the only physically viable solution. NVIDIA GB200 NVL72 racks directly drive orders for companies such as nVent and Vertiv. nVent's organic orders grew 65% in Q3 2025, almost entirely from liquid cooling.

### 3. Why are leaders already expensive, yet still interesting?

The investment logic of the infrastructure layer is fundamentally different from the semiconductor layer. The semiconductor layer is winner-take-most (NVIDIA holds more than 80% of the AI training GPU market). The infrastructure layer has multiple winners: each sub-segment has its own leaders, and valuation gaps between them can be very large.

The market's current pricing tension is this: Vertiv trades at roughly 80x P/E, and Arista at roughly 58x. Their "AI premium" is already fully priced in, so any quarterly miss could trigger a 20-30% correction.

But the market is overlooking two facts:

**First, valuation gaps create arbitrage-like opportunities.** nVent does work that overlaps heavily with Vertiv (cabinets, liquid cooling, power distribution), yet its forward P/E is only 33x, less than half of Vertiv's. Eaton trades at about 41x P/E, while its data-center power-distribution business is growing no slower than Vertiv's. Zhongji Innolight's 2026E P/E is only 28x, despite controlling more than 40% of the global 800G optical-module market and 50-70% of the 1.6T market.

**Second, the certainty of "picks-and-shovels" companies is much higher than that of the "gold miners."** Whichever AI model ultimately wins, data centers still need optical fiber, connectors, power systems, and liquid cooling. Demand at this layer does not depend on the model-layer competitive landscape; it depends on hyperscaler capex, and the direction of that capex is already very clear.

The core question is: which companies in this layer are truly irreplaceable, and which are merely temporary cycle beneficiaries?

---

## II. Company-by-Company Deep Dive

---

### 1. nVent Electric (NVT) - The Undervalued Dark Horse in Liquid Cooling

**Company profile and bottleneck position**

nVent Electric is an electrical connection and protection solutions company spun out of Pentair in 2018. Its core products include data-center cabinets, liquid-cooling systems, power distribution, and cable management. During the AI wave, the company has strategically shifted from industrial electrical equipment to data-center infrastructure. In 2025, it was added to the NVIDIA Partner Network and began directly supporting liquid-cooling deployments for GB200 NVL72 racks.

nVent sits at the "last meter" of the data center: cable management inside the rack, liquid-cooling pipework, and power distribution units. This position may look unglamorous, but once rack power breaks through 100 kW, thermal management and power-distribution design inside the cabinet become true physical bottlenecks.

**Key financials**

- 2025 full-year revenue: $3.9 billion, up about 30% YoY (13% organic growth)
- Data-center revenue: about $1.0 billion (roughly 26% of revenue), up 67% from $600 million in 2024
- Q1 2026 revenue: $1.24 billion, up 53.5% YoY (strong organic growth)
- Backlog: $2.6 billion, a record high, up more than 3x YoY
- 2025 gross margin: 37.7%; Q1 2026 gross margin: 35.9% (down 2.9 percentage points YoY)
- Current market cap: about $26.3 billion
- Forward P/E: about 34x
- Sources: SEC 8-K (Q1 2026), company financial reports

**Irreplaceability analysis**

nVent's unique attribute is its "NVIDIA certification." Being included in the NVIDIA Partner Network means that when hyperscalers procure GB200 racks, nVent's liquid-cooling solution is part of the "reference design." This certification barrier is difficult to break through in the short term. In addition, nVent built a new liquid-cooling factory in Minnesota in 2025 and brought it online quickly, giving it a lead in capacity expansion.

That said, nVent's moat is not deep. Liquid cooling itself is not technically complex (cold-plate liquid cooling is mainly about precision manufacturing and system integration), and competitors such as Vertiv and CoolIT are also competing aggressively. nVent's advantage is more "first mover + certification + delivery speed" than an insurmountable technology barrier.

**Valuation view**

At roughly 34x forward P/E, nVent is clearly cheaper than Vertiv at 80x and Eaton at 41x. Its $2.6 billion backlog gives strong revenue visibility for 2026-2027. If liquid-cooling penetration rises as expected from 15% in 2025 to 40% in 2028, nVent could sustain revenue growth above 30%.

Two risks deserve attention. First, margin compression: Q1 already showed a 2.9 percentage-point decline, with materials inflation and tariffs (about a $90 million negative impact) eroding profitability. Second, if hyperscalers develop liquid-cooling solutions in-house, nVent's value could be meaningfully impaired.

**Risk factors**

- Gross-margin pressure: materials-cost inflation, tariff impact, and fixed-cost dilution during capacity ramp-up
- Intensifying competition: Vertiv, CoolIT, and even hyperscaler in-house liquid-cooling efforts
- Customer concentration: large hyperscaler projects are becoming a rapidly growing share of revenue, increasing dependency

**One-sentence conclusion:** nVent is the most obvious valuation pocket in the infrastructure layer. Its 34x forward P/E is less than half of Vertiv's, and NVIDIA certification plus $2.6 billion of backlog provide a margin of safety, but gross-margin trends are the key variable to watch.

---

### 2. Celestica (CLS) - The Biggest Winner in AI Server Contract Manufacturing

**Company profile and bottleneck position**

Celestica is a Canadian electronics manufacturing services (EMS) provider that manufactures AI servers and network switches for hyperscalers. In AI infrastructure buildout, Celestica plays the role of "assembly plant": combining NVIDIA GPUs, Broadcom network chips, and various cooling and power modules into complete server racks.

That may sound low-tech, but in practice, there are only a handful of EMS vendors capable of delivering AI servers on time, at quality, and at scale. Celestica's advantage lies in its deep ties with several core hyperscalers (reportedly mainly Google and Meta).

**Key financials**

- Initial 2025 full-year revenue guidance: $16.0 billion, later raised
- Q1 2026 revenue: $4.05 billion, up 53% YoY
- 2026 full-year revenue guidance raised to: $19.0 billion, with adjusted EPS guidance of $10.15
- CCS (Connectivity & Cloud Solutions) is the growth engine; hardware-platform solutions revenue grew 82% YoY (Q2 2025)
- Current market cap: about $52.8 billion
- P/E: about 47x
- Sources: SEC 8-K (Q1 2026), company financial reports

**Irreplaceability analysis**

The moat in EMS is "relationship lock-in," not technology. Once a hyperscaler's server design is integrated with Celestica's production line, switching suppliers is very costly (recertification, line reconfiguration, and delivery-disruption risk). Celestica has maintained relationships with core customers for years and is unlikely to be replaced in the short term.

Over the long term, however, EMS pricing power is limited. Celestica is essentially paid on labor and materials markups, with gross margins typically ranging from low single digits to the teens. Once AI server demand growth slows, price competition is inevitable.

**Valuation view**

47x P/E is expensive for an EMS company. Historically, EMS peers such as Flex and Jabil have usually traded at 10-20x P/E. Celestica receives a premium because the market prices it as an "AI pure-play": AI-related revenue already accounts for more than 60% of its $19.0 billion 2026 revenue guidance.

The problem is that once AI capex growth falls from 64% in 2026 to 20-30% in 2027, Celestica's growth rate could drop sharply, and 47x P/E would lose support.

**Risk factors**

- Very high customer concentration: the top two customers may account for more than 50% of revenue
- EMS is structurally low-margin, so valuation-compression risk is high when growth slows
- Once AI servers become standardized, contract-manufacturing barriers fall

**One-sentence conclusion:** Celestica is the highest-beta contract-manufacturing name in the current AI capex cycle, with an impressive 53% revenue growth rate, but its 47x P/E has already pulled forward part of the growth expectation. It is better suited to trend trading than long-term ownership.

---

### 3. Zhongji Innolight (300308.SZ) - The Strongest Player in Optical Modules

**Company profile and bottleneck position**

Zhongji Innolight is the global leader in high-speed optical transceiver modules. It is headquartered in Jinan, Shandong, with most production capacity in China. The company is a tier-one supplier to core customers such as NVIDIA and Google. In AI data centers, high-speed communication between GPUs depends on optical modules. Without optical modules, even the most powerful GPUs become isolated islands.

Zhongji Innolight's core advantage is this: it holds more than 40% global share in 800G optical modules and 50-70% share in 1.6T optical modules. That level of market position is rare across the entire AI supply chain. Few segments have a single supplier with such high share.

**Key financials**

- 2025 full-year revenue: RMB 38.24 billion, up 60.25% YoY
- 2025 net profit attributable to the parent: RMB 10.80 billion, up 108.78% YoY, officially entering the "RMB 10 billion net-profit club"
- Q1 2026 revenue: RMB 19.50 billion, up 192% YoY
- Q1 2026 net profit attributable to the parent: RMB 5.74 billion, up 262% YoY
- Optical-communications transceiver module gross margin: up from 34.65% in 2024 to 42.61% in 2025, and further to 46.06% in Q1 2026
- Net margin: 32.40% (Q1 2026)
- Current market cap: about RMB 1.29 trillion
- 2026E P/E: about 28x (based on forecast net profit of RMB 22.5 billion)
- Sources: Company annual report (Shenzhen Stock Exchange filings), Tonghuashun

**Irreplaceability analysis**

Zhongji Innolight's irreplaceability rests on three layers: first, capacity scale (the world's largest optical-module production base); second, speed of technology iteration (retaining leading share through the transition from 800G to 1.6T); and third, customer-certification barriers (strict certification by top North American hyperscalers takes 2-3 years).

More importantly, the competitive landscape in 1.6T optical modules is more concentrated than in 800G. Zhongji Innolight's 50-70% share in 1.6T means competitors (Coherent, Lumentum, and others) are already clearly behind in this generation of products.

The risk is also obvious: geopolitics. If the United States further restricts Chinese optical-module companies from entering North American supply chains, Zhongji Innolight's business would be severely hit. It has not happened yet, but it remains a Sword of Damocles.

**Valuation view**

28x forecast P/E is very cheap for a company growing profit by more than 100% with net margin above 30%. Compared with Coherent at more than 150x trailing P/E, Zhongji Innolight offers a much stronger risk/reward profile.

But the low valuation itself reflects the market's pricing of geopolitical risk. If you can accept that risk, Zhongji Innolight may be the most attractively valued company across the entire AI infrastructure layer.

**Risk factors**

- Geopolitical risk: U.S.-China technology decoupling could directly affect North American customers
- Technology-generation transition risk: the competitive landscape could change in the next generation of products (3.2T)
- A-share liquidity and sentiment can amplify volatility

**One-sentence conclusion:** Zhongji Innolight is the infrastructure-layer name with the "highest certainty and lowest valuation": 28x P/E buys 40% global share and 262% profit growth. If you can tolerate geopolitical risk, this is almost a layup.

---

### 4. Arista Networks (ANET) - The Clear King of AI Network Switching

**Company profile and bottleneck position**

Arista is the leader in data-center Ethernet switches, with more than 40% market share in high-speed network switching (400G/800G). The core challenge in AI data centers is not single-GPU compute, but efficient communication among thousands of GPUs. Arista is a key supplier solving that problem.

The company's EOS (Extensible Operating System) is its core technical barrier. Unlike Cisco's traditional network architecture, Arista's EOS is a software-defined, programmable network operating system, better suited to the dynamic traffic-management needs of AI clusters.

**Key financials**

- 2025 full-year revenue: $9.0 billion
- Q1 2026 revenue: $2.71 billion, up 35.1% YoY
- 2026 full-year revenue guidance: $11.5 billion, including about $3.5 billion AI-related revenue
- 800G Ethernet switch port shipments: up 3x QoQ in Q2 2025
- Cumulative shipments: 150 million ports
- Current market cap: about $150.0 billion
- P/E: about 58x
- Sources: SEC 8-K (Q1 2026, Q4 2025), company releases

**Irreplaceability analysis**

Arista's position in AI Ethernet is almost unshakable. Its EOS operating system has been refined over many years and has become the de facto standard in hyperscaler data centers. More importantly, Arista is making a heavy bet on "AI Ethernet" (as distinct from NVIDIA's InfiniBand approach), and is developing XPO and CPO (co-packaged optics) technologies with the goal of reaching InfiniBand-level performance without sacrificing compatibility with the Ethernet ecosystem.

If Ethernet ultimately becomes the mainstream networking architecture for AI, rather than InfiniBand, Arista will be the largest beneficiary.

But this is also the biggest risk: if NVIDIA's InfiniBand continues to dominate in very large-scale clusters, Arista's AI networking opportunity could be compressed.

**Valuation view**

58x P/E is high within the infrastructure layer, but given Arista's market position and software stickiness, the valuation has some rationale. The key variable is the share of AI networking revenue. If AI revenue of $3.5 billion in 2026 can double to $7.0 billion in 2027, 58x P/E has support.

Not cheap, but not absurd either. Worth watching on pullbacks.

**Risk factors**

- InfiniBand competition: NVIDIA continues to promote its own networking solution
- High valuation: 58x P/E is highly sensitive to any negative news
- Long-term threat from hyperscaler-designed switching chips

**One-sentence conclusion:** Arista is a "must-own" name in AI Ethernet, with a solid market position, but 58x P/E means it is a good company rather than a cheap one. It is better to add exposure once signals are clearer that Ethernet has fully won in AI clusters.

---

### 5. Vertiv (VRT) - Leader in Data-Center Power and Liquid Cooling, but Valuation Is the Problem

**Company profile and bottleneck position**

Vertiv is a leading global provider of critical data-center infrastructure, with products spanning power management (UPS, power distribution), thermal management (precision cooling, liquid cooling), and IT management systems. In the AI wave, Vertiv is the leader across both "power + cooling."

Power and cooling are the hardest physical bottlenecks in data centers. GPUs can be bought from NVIDIA (even if customers must wait in line), but data-center power interconnection and cooling systems require 12-24 months of construction. Vertiv has the most complete global product line and the largest delivery capacity in this lane.

**Key financials**

- 2025 full-year revenue: about $9.5-10.0 billion (based on quarterly run-rate aggregation)
- Q1 2026 revenue: $2.65 billion, up 30% YoY (23% organic growth)
- 2026 full-year revenue guidance: $13.25-13.75 billion (up 27-29% YoY)
- 2026 full-year adjusted EPS guidance: $5.97-6.07 (up 43% YoY)
- Q1 2026 adjusted operating margin: 20.8%, up 430 basis points YoY
- 2025 acquisitions: PurgeRite (liquid-cooling services, about $1.0 billion) and Great Lakes (cabinets, about $200 million)
- Current market cap: about $60.0 billion
- P/E: about 80x
- Sources: SEC 8-K (Q1 2026, Q4 2025), company financial reports

**Irreplaceability analysis**

Vertiv's moat is its "end-to-end" capability. Most competitors do either power or cooling; Vertiv can provide a one-stop solution spanning UPS, power distribution, liquid cooling, and monitoring. For hyperscalers, reducing the number of suppliers lowers integration risk and delivery time.

The two 2025 acquisitions further strengthened that capability. PurgeRite filled the liquid-cooling services gap (installation, maintenance, pipe flushing), and Great Lakes rounded out the cabinet product line.

However, Vertiv's history deserves attention. In 2020, short seller Muddy Waters shorted Vertiv, alleging insufficient financial transparency. Although the allegations were later disproven, that episode is a reminder to remain cautious about Vertiv's earnings quality.

**Valuation view**

80x P/E is the highest valuation in the list. Even considering 2026 adjusted EPS of $6 and a 43% growth rate, this valuation implies the market expects Vertiv to sustain growth above 30% for the next 3-5 years. If the capex cycle slows, the downside from 80x P/E could be substantial.

**Risk factors**

- Very high valuation: 80x P/E leaves almost no room for execution misses
- Intensifying competition: Eaton, nVent, Schneider Electric, and others are competing for the same pie
- Acquisition-integration risk: serial acquisitions could distract management

**One-sentence conclusion:** Vertiv is the benchmark company in data-center power and liquid cooling, with the most complete product line, but 80x P/E has already priced in the next three years of growth. Unless you believe AI capex will keep beating expectations, there is no margin of safety at this price.

---

### 6. Eaton (ETN) - A Legacy Electrical Giant with a New Data-Center Story

**Company profile and bottleneck position**

Eaton is a century-old electrical-management company with products spanning power distribution, UPS systems, transformers, circuit breakers, and more. Unlike Vertiv, Eaton's data-center business is only one part of a diversified portfolio (which also includes aerospace, automotive, industrial, and other businesses), but data centers are becoming its fastest-growing engine.

Eaton's core value in data centers is power distribution and UPS. When total data-center power rises from tens of megawatts to hundreds of megawatts or even gigawatt scale, the reliability and efficiency of power-distribution systems become critical. Eaton's 800V DC power-distribution solution is a technical direction for next-generation data centers.

**Key financials**

- 2025 full-year revenue: $27.4 billion
- Q1 2026 revenue: $7.5 billion, up 17% YoY (a quarterly record)
- 2026 full-year adjusted EPS guidance: $13.00-13.50 (up about 10% YoY)
- Q1 adjusted EPS: $2.81 (a Q1 record)
- Acquisitions since 2026 began: Fibrebond (modular data centers), Resilient Power Systems, Boyd Thermal (liquid cooling), Ultra PCS
- Current market cap: about $163.6 billion
- P/E: about 41x
- Sources: SEC 8-K (Q1 2026), company financial reports

**Irreplaceability analysis**

Eaton's moat differs from Vertiv's: Vertiv has high "data-center purity," while Eaton has broad "brand + channel + certification." Eaton's power-distribution products have decades of safety-certification history, and switching suppliers is very risky for data-center operators.

The recent run of acquisitions (Fibrebond, Boyd Thermal, and others) shows that Eaton is accelerating its expansion into data-center liquid cooling and modular solutions, trying to replicate Vertiv's "end-to-end" model. But integration takes time, and results remain to be proven.

Another advantage is Eaton's "diversification hedge." Even if data-center capex slows, aerospace and electrification (EV charging infrastructure) can provide growth support. This makes Eaton more resilient than Vertiv in a downcycle.

In addition, Eaton announced that it will spin off its Mobility business into a separately listed company, sharpening its focus on electrical management and data centers. The strategic intent is clear.

**Valuation view**

41x P/E is not cheap for a company growing revenue 17% and EPS about 10%, but given Eaton's diversification and century-old brand premium, the valuation sits in the "reasonable but somewhat expensive" range. Compared with Vertiv's 80x, Eaton offers a better risk/reward profile in data-center power.

**Risk factors**

- Growth is not especially fast: 17% revenue growth is slow relative to many AI-themed names
- Diversification also means "less purity," so AI thematic funds may prefer Vertiv
- Serial acquisitions take time to integrate and may weigh on margins in the short term

**One-sentence conclusion:** Eaton represents "buying a first-class asset at a reasonable price": 41x P/E, a century-old brand, diversification hedge, and data-center power-distribution leadership. It is better suited than Vertiv for long-term holding, though its near-term catalysts are weaker than pure-play AI names.

---

### 7. Coherent (COHR) - The "Aristocrat" of Optical Modules

**Company profile and bottleneck position**

Coherent is a global leader in optoelectronics and laser technology. Through the acquisitions and integration of Finisar and II-VI, it has become a full-product-line supplier across optical modules, optical components, and lasers. In AI data centers, Coherent provides 800G/1.6T optical transceiver modules and underlying optical components.

Unlike Zhongji Innolight's "pure optical module" positioning, Coherent's advantage lies in "vertical integration": full-chain capabilities from optical chips (VCSEL, EML) to optical components and then optical modules. This means Coherent can be self-sufficient in core optical components and is less constrained by upstream supply chains.

**Key financials**

- FY2025 (ended June 2025) revenue: $5.81 billion, up 23% YoY
- Networking segment revenue grew 48%, making it the fastest-growing segment
- Q1 FY2026 (ended September 2025) revenue: $1.58 billion, up 17% YoY
- 1.6T optical transceiver modules: mass production shipments began in Q4 2025
- March 2026: NVIDIA announced a $2.0 billion strategic investment in Coherent
- Current market cap: about $70.0-81.0 billion
- Trailing P/E: about 150-200x; forward P/E: about 48x
- Sources: SEC 8-K (FY2025, Q1 FY2026), company announcements

**Irreplaceability analysis**

NVIDIA's $2.0 billion strategic investment is the strongest endorsement. This was not only a financial investment; it also signals that NVIDIA chose Coherent as a core partner for next-generation optical interconnect technologies (CPO, silicon photonics). As AI clusters evolve toward higher bandwidth, technical barriers at the optical-component layer will rise, and Coherent's accumulated know-how at that layer is much deeper than Zhongji Innolight's.

Coherent's problem is that it is "big but not pure." Its business also includes industrial lasers, materials processing, and other non-data-center segments, which drag down overall growth. In addition, its share in the 800G optical-module market is far below Zhongji Innolight's (about 15-20% vs. more than 40%).

**Valuation view**

A trailing P/E of 150-200x is breathtaking, but the forward P/E of about 48x is more relevant because earnings are ramping quickly. NVIDIA's $2.0 billion investment provides an implicit valuation anchor. NVIDIA would not put that much money into an obviously overvalued company.

Still, 48x forward P/E is 72% more expensive than Zhongji Innolight's 28x. Given Zhongji Innolight's clear leadership in 800G/1.6T optical modules, Coherent's valuation premium needs to be justified by "vertical integration + NVIDIA endorsement + geopolitical immunity (non-China company)."

**Risk factors**

- Business complexity: non-data-center businesses dilute valuation purity
- Optical-module market share is weaker than Zhongji Innolight's
- Integration risk: organizational-efficiency issues after multiple large acquisitions

**One-sentence conclusion:** Coherent is NVIDIA's handpicked optical-interconnect partner, with unique vertical-integration capabilities, but its 48x forward P/E is 72% higher than Zhongji Innolight's. If you want to avoid geopolitical risk, Coherent is the substitute, but you must pay a premium for it.

---

### 8. Corning (GLW) - The "Unavoidable Tollbooth" in Optical Fiber

**Company profile and bottleneck position**

Corning is an oligopoly supplier of global optical-fiber preforms and optical fiber/cable, with an extremely unique position in the AI supply chain. No matter how optical-module technology evolves, optical signals ultimately need to travel through fiber. Corning is the "tollbooth" for optical fiber.

The company's Optical Communications segment is the growth engine. In 2025, optical-communications revenue reached $6.3 billion, up 35% YoY, with enterprise data-center fiber revenue up 61% YoY. In January 2026, Corning signed a $6.0 billion multi-year fiber supply contract with Meta, setting an industry record.

**Key financials**

- 2025 full-year core sales: $16.41 billion, up 13% YoY
- 2025 Optical Communications revenue: $6.3 billion, up 35% YoY
- 2025 core EPS: $2.52, up 29% YoY
- Q1 2026 core sales: $4.35 billion, up 18% YoY
- Q1 2026 Optical Communications revenue: about $1.85 billion, up 36% YoY
- Operating margin reached 20.2%, achieving the "Springboard Plan" target one year early
- Meta $6.0 billion multi-year contract (signed January 2026)
- Management target: double revenue to $40.0 billion by 2030
- Current market cap: about $166.0-173.0 billion
- P/E: about 96x
- Sources: SEC 8-K (Q1 2026), investor-relations announcements

**Irreplaceability analysis**

Corning's position in optical-fiber preforms is close to "irreplaceable." The global optical-fiber preform market is highly concentrated (an oligopoly of Corning, Shin-Etsu Chemical of Japan, and YOFC), technical barriers are extremely high (preform recipes and drawing processes require decades of accumulation), and capacity expansion cycles are long (new preform lines take 2-3 years to build).

More importantly, Corning has launched next-generation high-density fiber connection solutions for AI data centers and works directly with NVIDIA and hyperscalers. Jensen Huang has publicly named Corning several times as a key partner in AI data-center optical interconnect.

**Valuation view**

96x P/E looks expensive, but Corning's valuation includes a large amount of non-data-center business (display, environmental, specialty materials, and others). Those businesses grow slowly but have large bases, dragging down overall EPS growth. If one looks only at the Optical Communications growth trajectory (35-36% growth), the valuation is easier to understand.

The issue is whether Corning's overall growth (18% revenue, 30% EPS) can support 96x P/E. The 2030 target of doubling revenue to $40.0 billion implies roughly 20% CAGR over the next five years. At today's valuation, investors need a meaningful combination of "P/E compression + growth-driven earnings" to earn a reasonable return.

**Risk factors**

- High valuation: 96x P/E is not cheap for a company with 18% overall revenue growth
- Non-data-center businesses weigh on results: display-panel and related businesses are cyclical
- Fiber demand is tightly linked to the data-center construction cycle

**One-sentence conclusion:** Corning is the most certain name in the logic chain of "data must travel through fiber," with oligopoly status, Jensen Huang endorsement, and a $6.0 billion Meta contract. But 96x P/E prices in too much optimism. It would be safer to revisit below 70x.

---

### 9. Dell (DELL) - Number One in AI Server Shipments, but Margins Are the Achilles' Heel

**Company profile and bottleneck position**

Dell is the world's largest AI server vendor by shipment value. In fiscal 2026 (ended January 2026), Dell's AI-optimized server revenue reached $25.0 billion, up more than 150% YoY. ISG (Infrastructure Solutions Group) full-year revenue was $60.8 billion, up 40% YoY.

Dell's position in the AI supply chain is "channel and integration." It does not produce GPUs (NVIDIA), does not produce network chips (Broadcom), and can even outsource server assembly to Celestica. But Dell has the broadest enterprise customer relationships and the most complete after-sales service system. For enterprise customers that do not purchase directly from NVIDIA, Dell is the default channel for AI servers.

**Key financials**

- FY2026 ISG revenue: $60.8 billion, up 40% YoY
- FY2026 AI-optimized server revenue: $25.0 billion, up more than 150% YoY
- Q4 FY2026 AI server revenue: $9.0 billion (quarterly record), up 342% YoY
- FY2026 ISG operating profit: $7.1 billion, operating margin of 14.8%
- But AI server operating margin: mid-single digits (about 5%), far below traditional servers
- FY2027 AI server revenue guidance: about $50.0 billion (doubling)
- AI server backlog: $43.0 billion
- Current market cap: about $276.0 billion
- P/E: about 19-33x (varies by source and calculation method)
- Sources: SEC 8-K (FY2026 Q4, FY2027 Q1), Futurum Group analysis

**Irreplaceability analysis**

Dell's "irreplaceability" is not technological; it is channel-based. For most enterprises globally (excluding hyperscalers), Dell is the default choice when buying servers. This channel advantage has existed in traditional servers for 20 years and is now extending naturally into AI servers.

But Dell has very limited pricing power in AI servers. The GPU comes from NVIDIA; Dell mainly handles assembly, testing, and after-sales service, leaving gross-margin headroom severely compressed. Management has explicitly said AI server operating margins are in the "mid-single digits" (about 5%), far below traditional servers at more than 15%.

This means the more Dell's AI server revenue grows, the more its overall margin may decline. "Revenue growth without profit growth" is Dell's structural dilemma.

**Valuation view**

P/E of about 19-33x (depending on calculation method) is among the lowest valuations in the infrastructure layer. But that low valuation has a rationale: Dell is essentially a "toll-taking" model, earning thin-margin volume profits from AI servers.

The only bullish case for Dell is: (1) AI server penetration accelerates in the enterprise market (spreading from hyperscalers to small and midsize enterprises), and (2) Dell increases value-added content through software and services (raising margins).

**Risk factors**

- Low AI server margin: mid-single-digit operating margin limits earnings leverage
- GPU supply depends on NVIDIA: Dell does not control delivery cadence
- Declines in traditional PC and storage businesses may weigh on overall results

**One-sentence conclusion:** Dell is the undisputed leader in AI server shipments, and $43.0 billion of backlog supports growth visibility. But mid-single-digit margins mean it "looks busy but does not make much money." The cheap valuation makes sense, and the stock is better suited to investors seeking certainty rather than upside beta.

---

### 10. Amphenol (APH) - The Hidden Champion in High-Speed Connectors

**Company profile and bottleneck position**

Amphenol is the world's second-largest connector manufacturer (behind TE Connectivity), but in high-speed interconnect for AI data centers, Amphenol is the de facto leader, with roughly 33% market share. Its products include high-speed copper-cable connectors between GPUs, backplane connectors, power connectors, and more. These seemingly unremarkable components are actually a key physical layer determining AI cluster performance.

In January 2026, Amphenol completed the acquisition of CommScope's connectivity and cable-solutions business (about $4.1 billion of annual revenue), further strengthening its dominant position in data-center fiber and copper-cable connectivity.

**Key financials**

- 2025 full-year revenue: $23.1 billion, up 52% YoY (38% organic growth)
- Q1 2026 revenue: $7.6 billion, up 58% YoY (record)
- Q1 2026 adjusted EPS: $1.06, up 68% YoY
- Q1 2026 orders: $9.4 billion (record), book-to-bill of 1.24
- IT Datacom accounted for about 38% of revenue and grew 110% YoY (Q4 2025)
- Adjusted operating margin: 27.5% (2025 full year, industry-leading)
- Current market cap: about $185.0 billion
- P/E: about 38-43x
- Sources: Company financial reports, Seeking Alpha, Simply Wall St

**Irreplaceability analysis**

The connector industry's moat is very deep but easy to miss. The reasons are: (1) certification barriers - each connector must pass strict end-customer certification, with certification cycles of 6-12 months; (2) high customization - every connector inside an NVIDIA GB200 rack has different specifications, and once the design is locked, switching costs are extremely high; (3) small size, high value - a high-speed connector may cost only dozens of dollars, but if it fails, the entire rack can go down, so customers demand very high quality and are unwilling to risk switching suppliers.

Amphenol's 27.5% operating margin is exceptional among industrial companies, directly reflecting its pricing power and irreplaceability.

**Valuation view**

38-43x P/E is medium-high within the infrastructure layer, but considering Amphenol's growth (58% revenue growth, 68% EPS growth), margins (27.5% operating margin), and market position (33% share), this valuation is better supported than many peers.

The key is Amphenol's very diversified business. Beyond AI data centers, it also serves automotive, defense, industrial, mobile devices, and other markets. This diversification provides a buffer in downcycles, similar to Eaton.

The $4.1 billion of revenue from the CommScope acquisition has not yet been fully reflected in profit. As integration progresses, 2026-2027 could release synergies.

**Risk factors**

- CommScope integration risk: integrating $4.1 billion of revenue takes time
- AI data-center connector growth may slow after 2027
- 38-43x P/E is historically high for a connector company

**One-sentence conclusion:** Amphenol is, in my view, the highest-quality company among these 10 names: 33% market share, 27.5% operating margin, 1.24 book-to-bill, and a diversified business structure. 38-43x P/E is not cheap, but this is the best-quality "picks-and-shovels" business you can buy at a reasonable price.

---

## III. Summary: Which Names Deserve Deeper Work?

| Company | Ticker | Core lane | P/E (approx.) | Revenue growth | Irreplaceability | Value-for-money rating |
|------|------|----------|-----------|----------|------------|------------|
| Zhongji Innolight | 300308.SZ | Optical modules | 28x | 192% (Q1) | Very high (800G 40%+ share) | Highest |
| nVent | NVT | Liquid cooling/cabinets | 34x | 54% (Q1) | Medium-high (NVIDIA certification) | High |
| Amphenol | APH | High-speed connectors | 38-43x | 58% (Q1) | Very high (33% share) | High |
| Eaton | ETN | Power distribution/UPS | 41x | 17% (Q1) | High (century-old brand + certification) | Medium-high |
| Celestica | CLS | Server contract manufacturing | 47x | 53% (Q1) | Medium (customer lock-in) | Medium |
| Dell | DELL | Server sales | 19-33x | 40% (FY) | Medium (channel advantage) | Medium |
| Coherent | COHR | Optical modules + optical components | 48x(fwd) | 17% (Q1 FY) | High (vertical integration + NVIDIA investment) | Medium |
| Arista | ANET | Network switches | 58x | 35% (Q1) | Very high (EOS ecosystem) | Medium-low |
| Vertiv | VRT | Power + liquid cooling | 80x | 30% (Q1) | High (end-to-end solution) | Low |
| Corning | GLW | Optical-fiber preforms | 96x | 18% (Q1) | Very high (oligopoly) | Low |

### The three most worth deeper research:

**No. 1: Zhongji Innolight (300308.SZ).** 28x P/E buys 262% profit growth and more than 40% global share, making it the clearest valuation mismatch in the list. The only question you must answer is: can you tolerate geopolitical risk? If the answer is "yes," this may be the best investment opportunity in the entire AI infrastructure layer.

**No. 2: Amphenol (APH).** This is the best-balanced name between "quality" and "price." A 33% market share, 27.5% operating margin, diversified business structure that provides downside protection, and incremental room from the CommScope acquisition. 38-43x P/E is not a bargain, but you are buying a first-class business.

**No. 3: nVent Electric (NVT).** It is the cheapest on a peer basis (less than half of Vertiv's valuation), with NVIDIA certification and $2.6 billion of backlog providing certainty. It is the best risk/reward choice in liquid cooling, provided you can accept the near-term pain of gross-margin compression.

### Three names that need a better price:

Vertiv (80x), Corning (96x), and Arista (58x) are all good companies, but their current valuations already reflect optimistic expectations. Without upside catalysts, these three are better suited for the "watchlist" than "buy now" bucket.

### Names that require more nuanced treatment:

Dell has impressive shipment volume but worrying margins. Celestica has high beta, but EMS attributes limit long-term value. Coherent has NVIDIA's endorsement but trades 72% more expensive than Zhongji Innolight. The investment logic for all three is not "clean" enough and only becomes attractive under specific conditions.

---

**Final thought:** The window for infrastructure-layer opportunities will not stay open forever. When hyperscaler capex growth falls from 64% in 2026 to 20-30% in 2027 (highly likely), growth across this entire layer will step down. Before that happens, picking the right names matters more than timing.

---

## Sources

- [AI Capex Cycle 2026: $725B Hyperscaler Buildout - CFA Analysis](https://alcapitaladvisory.com/research/intelligence/ai-infrastructure.html)
- [Hyperscaler CapEx Hits $600B in 2026 | Introl Blog](https://introl.com/blog/hyperscaler-capex-600b-2026-ai-infrastructure-debt-january-2026)
- [AI Capex 2026: The $690B Infrastructure Sprint - Futurum](https://futurumgroup.com/insights/ai-capex-2026-the-690b-infrastructure-sprint/)
- [nVent Electric Revenue Jumps 42% - Alphastreet](https://news.alphastreet.com/nvent-electric-nvt-revenue-jumps-42-as-data-center-demand-tops-its-own-q1-guidance/)
- [nVent Collaborates with NVIDIA on AI-Ready Liquid Cooling](https://www.nvent.com/en-us/resources/news/nvent-collaborates-with-nvidia-on-ai-ready-liquid-cooling-solutions)
- [Celestica Q1 2026 AI-driven revenue and EPS growth](https://www.stocktitan.net/sec-filings/CLS/10-q-celestica-inc-quarterly-earnings-report-85e102e8bba6.html)
- [Zhongji Innolight Q1 net profit surges 262% - TMTPost](https://www.tmtpost.com/7957799.html)
- [Zhongji Innolight RMB 25.0 billion profit forecast draws debate - Time Weekly](https://time-weekly.com/post/323854)
- [Arista Networks Q1 2026 Financial Results](https://www.arista.com/en/company/news/press-release/24017-pr-20260505)
- [Arista Networks Q4 2025 Financial Results](https://www.arista.com/en/company/news/press-release/23416-pr-20260212)
- [Vertiv Q1 2026 Press Release - SEC Filing](https://www.sec.gov/Archives/edgar/data/0001674101/000162828026026379/q12026exhibit991vrt04222026.htm)
- [Eaton Q1 2026 Results - SEC Filing](https://www.sec.gov/Archives/edgar/data/0001551182/000155118226000010/etn03312026exhibit99.htm)
- [Eaton 2025 Revenue $27.4B - StockTitan](https://www.stocktitan.net/sec-filings/ETN/10-k-eaton-corp-plc-files-annual-report-52453dbea12c.html)
- [Coherent Q4 FY 2025 Earnings - Futurum](https://futurumgroup.com/insights/coherent-q4-fy-2025-earnings-rise-on-ai-datacenter-and-networking-demand/)
- [Corning 2025 Financial Results - Investor Relations](https://investor.corning.com/news-and-events/news/news-details/2026/Corning-Announces-Outstanding-2025-Financial-Results-1--Upgrades-Springboard-Plan-for-Faster-Sales-Growth-on-Significantly-Enhanced-Financial-Profile/default.aspx)
- [Corning Could Hit $144 by End of 2026 - BofA](https://finance.yahoo.com/news/corning-could-hit-144-end-190736391.html)
- [Dell Q4 FY 2026 Earnings - Futurum](https://futurumgroup.com/insights/dell-q4-fy-2026-earnings-highlight-ai-optimized-server-ramp/)
- [Dell Q2 FY 2026 Results - Futurum](https://futurumgroup.com/insights/dell-q2-fy-2026-results-show-19-revenue-jump-ai-server-shipments-surge/)
- [Amphenol Q4 2025 Earnings Call - Yahoo Finance](https://finance.yahoo.com/news/amphenol-corp-aph-q4-2025-010122630.html)
- [Amphenol Q1 2026 Record Sales - Simply Wall St](https://simplywall.st/stocks/us/tech/nyse-aph/amphenol/news/amphenol-aph-is-up-60-after-ai-datacenter-demand-lifts-nvidi)
- [Amphenol: The Connectivity Engine of the AI Era](https://simplywall.st/community/narratives/us/tech/nyse-aph/amphenol/evbnvx6q-amphenol-aph-the-connectivity-engine-of-the-ai-era-prepares-for-a-watershed-q1-reveal)
