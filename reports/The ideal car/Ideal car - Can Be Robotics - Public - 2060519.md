# Can Ideal become a robotics company?

On May 18, Li Auto’s Hong Kong stock price plummeted 14%. But what I am more interested in is not this plunge, but the humanoid robot team that Ideal quietly established in January.

Li wanted to make a big statement: to become "one of no more than three companies in the world that simultaneously deploy base models, chips, operating systems, and embodied intelligence."

Is this a strategic vision or a big lie? I did a complete research.

---

## Let’s first figure out a technical question: What does the ideal chip do?

Ideal this year released a chip called M100, which adopts an "orchestrated data flow architecture" and is oriented to edge AI reasoning.

What does this mean?

A traditional chip (Von Neumann architecture) is like a worker that performs tasks in sequence - no matter whether the data is ready or not, it has to be queued and waiting to be processed. The data flow architecture is completely different - the data is calculated immediately when it is ready, without queuing.

For example: the traditional architecture is like serving food in a cafeteria, and you come to each window one by one; the data flow architecture is like a buffet, and you just take whatever dish is ready.

The advantages of this architecture in AI reasoning are significant. Groq's data flow chip inference energy efficiency ratio is 35 times that of NVIDIA H100, and NextSilicon claims to be 4 times higher than NVIDIA Blackwell's energy efficiency ratio.

Ideal's decision to make the M100 shows that it doesn't just want to build cars, nor does it just want to build robots - it wants to build the entire AI computing stack starting from the underlying chip. The ambition is indeed great.

But on the other hand, making chips and making robots are two different things. Making chips can be promoted efficiently with a small team, but making robots requires large-scale system integration capabilities. Just because the chip is done well does not mean that the robot can do it well.

---

## What exactly does it take to make a humanoid robot?

After studying a large number of industry reports and cases, I divided the sufficient conditions for humanoid robots into four levels:

**First level: If one is missing, you will lose**
- AI large model/embodied intelligence capabilities
- Implementation of scenarios with real paying customers
- Sufficient and sustained funding

**Second level: Decide who wins**
- Data Flywheel (Deployment → Data → Training → Stronger → More Deployment)
- Hardware system integration
- Motion control + perception system

**Level 3: Determining the speed of scale**
- Supply chain and mass production
- Battery life (currently 2-4 hours, commercialization requires 8-12 hours)
- Cost control (from US$100,000-500,000 to US$20,000-50,000)

In one sentence: **Sufficient conditions for making a humanoid robot = AI ability x scene implementation x financial endurance x data flywheel**.

Although hardware, supply chain, mass production and other conditions are important, they are gradually becoming "outsourcing and leveraging". AI capabilities and scene data are the moats that are truly difficult to replicate.

This also explains why Tesla (FSD data + manufacturing scale + massive funds) is regarded as the most competitive player - it has accumulated conditions at every level.

---

## Ideal vs three opponents: Who meets several conditions?

I selected four companies for horizontal comparison: Li Auto, Xpeng Motors, Xiaomi, and Yushu Technology.

Let’s talk about the conclusion first:

| Company | Number of sufficient conditions to meet the standard | Stage |
|---|---|---|
| Yushu Technology | 5/9 | Leading in commercialization |
| Xpeng Motors | 5/9 | The most comprehensive technology, mass production soon |
| Xiaomi | 2/9 | Deep reserves but slow implementation |
| **Ideal Car** | **1/9** | **The determination is clear but the execution has just begun** |

The only condition for the ideal to meet the standard is **funds** - 101.2 billion cash reserves, the most abundant among the four.

### Yushu Technology: The only one that makes money

Data for 2025: revenue of 1.7 billion (an increase of 335%), net profit of 600 million (an increase of 674%), 5,500 humanoid robots shipped, and a global market share of 32.4%.

The self-developed M107 motor has a torque density of 120Nm/kg and the cost is only one-fifth to one-tenth of that of similar products overseas. The G1 is priced at 85,000 yuan, and the R1 is priced at 39,900 yuan. It has proven that humanoid robots are not just demos, but can actually be sold for money.

The shortcomings are that Smart Hands has just started, the large AI model relies on external cooperation, and the 4.2 billion IPO raised compared to car companies has limited ammunition.

###Xpeng Motors: The car company with the strongest technology stack

The IRON robot has 82 degrees of freedom, 3 self-developed Turing chips (2250 TOPS), a large model of the physical world with 72 billion parameters, a Wanka intelligent computing cluster, an all-solid-state battery, and dexterous hands that restore the human hand 1:1.

Among car companies, Xpeng is the only one that has truly achieved full-stack self-development of chips + large models + actuators + data factories. Large-scale mass production and the first batch of cooperation with Baosteel by the end of 2026 are key verification nodes.

The shortcoming is that it has not yet been mass-produced and delivered, and the cash of 47.6 billion is not as abundant as ideal and Xiaomi.

### Xiaomi: The one with the most potential but the slowest

CyberOne will be released in 2022, and the third generation has not been officially unveiled for four years. In March 2025, the official personally denied the news of mass production.

However, the technical reserves should not be underestimated: MiMo-Embodied is the industry’s first cross-body base model that unifies autonomous driving and embodied intelligence, reaching SOTA in 29 benchmarks. Dexterous Hands hired engineers from Tesla's Optimus team, reduced its size by 60%, and passed 150,000 grip tests.

The five-year R&D budget is 200 billion, and the AI ​​three-year budget is 60 billion. Money is not the issue, speed is the issue. Lei Jun said there will be new progress in 2026, but the market has waited too long.

### Ideal Car: Rich, but almost nothing

The humanoid robot team was only established in January 2026. There are plans for a two-wheeled robot (expected to be released mid-year) and a bipedal humanoid robot (timeline unclear).

**In the comparison of ten abilities, ideally 6 items are marked with crosses (✗), 3 items are marked with triangles (△), and only 1 item is marked with a check mark (✓). **

| Ability | Ideal | Comparison |
|---|---|---|
| Motor/Actuator | ✗ Recruiting | Yushu’s self-developed motors lead the world |
| Dexterous Hands | ✗ Recruiting | Xpeng’s 22 degrees of freedom has been achieved |
| Motion Control | ✗ No public results | Yushu 0.3 second gait adjustment |
| Embodied Intelligence | △ Self-driving and transferable | Xpeng 72 billion parameter model |
| Scenario implementation | ✗ No customers | Yushu’s revenue is 1.7 billion |
| Funds | ✓ 101.2 billion | The most abundant among the four |

---

## Core Contradiction

The ideal problem is not lack of money, but time.

Motor design requires repeated iterative testing, and it cannot be accelerated by spending money. Motion control algorithms need to be fed with real environment data, and simulation can only solve part of the problem. The accuracy and reliability of dexterous hands require tens of thousands of physical tests to verify. Mass production requires step-by-step efforts to establish standards from the first to the thousandth unit.

Yushu Technology has already gone through these pitfalls - the experience of shipping 5,500 humanoid robots cannot be bought with 101.2 billion cash.

Xiaopeng has also spent at least two years - from project establishment to IRON release to mass production planning. Ideal just started recruiting people.

**The gap is at least two years. **

The competitive landscape in two years' time will not wait for ideals. Yushu is already sprinting towards an IPO, Xpeng will be mass-producing by the end of the year, and Xiaomi may finally break out from silence. Two years later, the ideal opponent I will face is not the opponent today, but the opponent who has completed the first round of the data flywheel.

---

## What about the M100 chip?

M100 uses an orchestrated data flow architecture for edge AI inference, which is the right direction. The energy efficiency advantages of data flow architecture in AI reasoning have been verified by companies such as Groq and NextSilicon.

But the chip is just one component of the robotic system. Having a good chip does not mean having a good robot, just like having a good engine does not mean having a good car - it also requires chassis, suspension, gearbox, body, and vehicle tuning.

For ideals, the greater value of the M100 may be in autonomous driving and in-vehicle AI scenarios, rather than robots. In the field of robotics, what needs to be solved first is "can it be built?" rather than "what chip to use."

---

## Conclusion

**Can I ideally become a robotics company? Yes, but not now, and it won't be easy. **

It has three cards:
1. **101.2 billion in cash** — you can make many mistakes
2. **Autonomous Driving AI Accumulation** — Perception, simulation, and large model capabilities can be transferred
3. **M100 chip** — technical reserve for edge AI reasoning

It lacks three things:
1. **Time** — at least two years behind Xiaopeng and three years behind Yushu
2. **Hardware capabilities** — motors, dexterous hands, and motion control from scratch
3. **Scenario Data** — No real deployment, the flywheel has not started turning yet

If you ask me, can I make a humanoid robot ideally in five years? Most likely. If there is enough money, the strategy is firm enough, and the automobile industry chain can draw on its strength.

But if you ask me, can I ideally become the leader in the humanoid robot track? It's hard. This is not a track with "latecomer advantage" - the data flywheel determines that first movers will run faster and faster. Ideally, one needs to complete within two years what others have taken three to five years before it is possible to catch up.

101.2 billion in cash can buy you a window of time, but not an exception to the laws of physics.

---

*Research data sources: Li Auto/Xpeng Motors/Xiaomi 2025 annual report, Yushu Technology IPO prospectus, McKinsey humanoid robot report, Ministry of Industry and Information Technology standard system, IDC industry trend report, etc. *
