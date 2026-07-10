# Large model unicorn from Tsinghua laboratory

> "Understanding Intelligent Spectrum AI" Series · Part 01 · Beginning
> Reading time approx. 8 minutes

---

## A company that is hard to understand

A company with revenue of 700 million and losses of 4.7 billion had a market value of over 400 billion four months after its listing. It is not a game company or a consumer product. It is an AI research institution that trains large language models. It came out of the laboratory of Tsinghua Computer Department.

On January 8, 2026, Zhipu AI was listed on the Hong Kong Stock Exchange at an issue price of HK$116.2/share**, becoming the "first large model stock in the world". What happened next was more unexpected than any AI model’s output:

- First day of listing: Market capitalization **HK$57.89 billion**, a good start
- 43 days later (February 20): The stock price rose by more than **500%**, and the market value exceeded **HK$323.2 billion**, surpassing JD.com and Kuaishou
- May 6: Closed **928.5 HKD**, with a market value of approximately **413.9 billion HKD**
- May 14: It rose to **HK$1,229** during the session, and the market value once exceeded **HK$500 billion**

In 4 months, the stock price increased nearly 10 times.

But looking at the financial report——

| Indicators | 2025 Data |
|------|-----------|
| Total revenue | **724 million yuan** |
| Net loss | **4.718 billion yuan** |
| R&D expenditure | **3.180 billion yuan** |
| Gross profit margin | 41.0% |
| Current market capitalization (May 2026) | **~450 billion Hong Kong dollars (approximately 410 billion yuan)** |
| Implied price-to-sales ratio | **About 560 times** |

Revenue was 700 million, loss was 4.7 billion, and market value was over 400 billion.

If you think this is a bubble - you may be right, but you may also be ignoring the special logic of AI track valuation.
If that sounds reasonable to you - you might be right, but you might also be paying for the narrative.

What this series will do is to break down Zhipu AI company layer by layer -- technology, products, competition, commercialization, risks -- so that you can judge for yourself whether this is the "Chinese version of Anthropic" or the "next SenseTime".

---

## Who is Zhipu AI?

### A business card

| Project | Content |
|------|------|
| Full name | Beijing Zhipu Huazhang Technology Co., Ltd. |
| Founder | Tang Jie (Professor of Department of Computer Science, Tsinghua University, 200+ papers) |
| CEO | Zhang Peng (Bachelor's degree in Computer Science, Tsinghua University, Class of 1998, PhD in Engineering, Class of 2018) |
| Date of establishment | 2019 (the technical foundation can be traced back to the AMiner system in 2006) |
| Team size | 883 people (51.2% shareholding) |
| Listing | January 8, 2026, Hong Kong Stock Exchange (02513.HK) |
| IPO fundraising | **HK$5.23 billion** |
| Cumulative financing | 8 rounds, exceeding **8.3 billion** |
| Investors | Tencent, Alibaba, Meituan, Ant, Hillhouse, Sequoia, Legend, Qiming, and multiple local state-owned assets |

### How deep is Tsinghua’s gene?

Zhipu is not a "company with Tsinghua background" - it is almost an extension of the Tsinghua Computer Department.

- Founder Tang Jie: Head of Tsinghua Knowledge Engineering Laboratory (KEG), created AMiner (academic search engine) in 2006, which is the technical starting point of Wisdom Spectrum
- CEO Zhang Peng: Bachelor’s degree, Master’s degree and Ph.D. from Tsinghua University, Ph.D. from Tsinghua Innovation Leading Engineering
- Chairman Liu Debing and President Wang Shaolan: both from Tsinghua KEG team
- There are about 400 people in the AI R&D Institute, **nearly half of whom are Tsinghua graduates** (Source: Pinwan Report)

**Contrary view**: The high degree of homogeneity of the team ("Tsinghua inbreeding") may lead to a lack of commercial sense and a more academic decision-making style. This issue will be expanded upon in subsequent chapters.

### Financing map

Zhipu’s investor lineup is extremely luxurious, almost gathering the “family portrait” of China’s technology circle:

| Rounds | Core Investors | Remarks |
|------|-----------|------|
| Early stage | Legend Capital, Qiming Venture Partners | VC routine operations |
| Round B starts | Meituan (leading investment of 300 million), Ant (accumulative investment of 600 million), Tencent (leading investment of 200 million) | Industry giants line up |
| Late stage | Hillhouse, Sequoia, Xiaomi, Kingsoft | All-star lineup |
| Pre-IPO | Beijing AI Industry Fund, Hangzhou Urban Investment, Zhuhai Huafa, Chengdu High-tech Zone | **Intensified entry of state-owned assets** |

(Source: Zhipu AI prospectus, Wall Street News)

**A noteworthy signal**: Unlike DeepSeek, which is purely market-oriented, Zhipu has **a large amount of state-owned assets and policy capital** behind it. This means two things: first, it is unlikely to "run out of food" in the short term; second, it may be saddled with some non-commercial goals (such as "domestic substitution", "independent and controllable").

---

## Three common misunderstandings about wisdom spectrum

### Misunderstanding 1: "Zhipu is engaged in ChatGPT"

Not accurate. Zhipu’s revenue structure clearly shows that it does not rely on the C-side to make money:

| Business | Revenue in 2025 | Proportion | Growth rate |
|------|-----------|------|------|
| Localized private deployment (ToB) | **534 million** | 73.7% | +102% |
| Cloud API/MaaS | **190 million** | 26.3% | **+293%** |

(Source: Zhipu 2025 Financial Report)

Zhipu Qingyan (C-side AI assistant) has **25 million** registered users, but its MAU is only about **6-8.38 million**. For comparison, ByteDou Bao MAU has exceeded **227 million** - a gap of **27 times**.

The true positioning of Zhipu is a **ToB+API platform company**, which is closer to Anthropic than OpenAI. The C-side is just a display window, not an income engine.

### Misunderstanding 2: "Tsinghua University students must be technically strong"

The Tsinghua background does provide profound technical accumulation - GLM-5.1 ran the world's best results on SWE-bench Pro and was fully aligned with Claude Opus 4.6. This is not false.

**But strong technology does not mean strong product**.

- Zhipu Qingyan's MAU growth has almost stagnated - from **7.02 million** in January 2025 to **8.38 million** in July 2025, an increase of less than 20% in half a year
- In the same period, Beanbao surged from tens of millions to over 200 million, and DeepSeek went from zero to phenomenal.
- Reason: Zhipu **does not have a native traffic entrance**. No Douyin, no WeChat, no search engine

Technical strength is a necessary condition, but the success or failure of C-end products depends on distribution capabilities. Wisdom spectrum is naturally disadvantaged in this dimension.

### Misunderstanding 3: "Valuation is too high = it must be a bubble"

The current price-to-sales ratio is about **560x**, which seems ridiculous. However, the valuation logic of the AI ​​track is different from that of traditional industries - what the market buys is not current revenue, but the expected exponential growth of future API calls.

Data supporting this expectation:
- MaaS platform ARR has reached **approximately 1.7 billion yuan** (approximately US$250 million), growing **60 times** in the past 12 months
- In Q1 of 2026, API call volume increased by **400%**, and pricing increased by **83%** (both volume and price increased)
- The number of registered users on the platform exceeded **4 million**, covering **218 countries** around the world

(Source: Zhipu 2025 Financial Report, Securities Times)

**Opposite view**: ARR is not equal to recognized revenue. The actual recognized revenue of 1.7 billion ARR is only 190 million (cloud part). The sudden increase in API calls is due to extremely low prices (price war). Once competition intensifies or subsidies are reduced, the growth rate may plummet. Anthropic's ARR in 2025 has reached **1 billion US dollars+**, and Zhipu's US$250 million is still a small size from a global perspective.

---

## To understand Zhipu AI, you need to answer four questions

Simplify the wisdom spectrum AI into one sentence:

> **Zhipu AI = Tsinghua University’s 20 years of technology accumulation + GLM flagship model (first echelon) + rapid growth of ToB/API revenue + C-side being crushed by big manufacturers + huge losses and money burning + 560 times sales ratio**

Each of these elements makes sense when taken apart, but when put together they are confusing. To understand this company clearly, you need to answer at least four questions:

| Question | Core Conflict | Which part of this series to start |
|------|---------|---------------|
| How strong is the technology? | GLM-5.1 is indeed aligned with Opus, but how long can the intergenerational advantage of the model be maintained? | Chapter 02 |
| Can the product ecology survive? | API grew by 400%, but the C-side was 27 times outpaced by Doubao | Article 02 |
| Who can beat the competition? | There is Baidu/Byte on the top and DeepSeek/MiniMax on the bottom | Article 03 |
| Do you have enough money to burn? | Annual loss of 4.7 billion, IPO financing of 5.2 billion, how long will it last? | Chapter 04 |

Looking at each question alone is not enough to judge whether the wisdom spectrum is worth paying attention to. **Looking together can form a complete picture. **

---

## Preview: What to talk about in the next article

In the next article, we will take an in-depth look at Zhipu’s **technology and products**——

- What is the level of GLM-5.1? How valuable is the phrase "Align Opus"?
- 74.4 billion parameters, MoE architecture - what do these technology choices mean?
- Why can’t I do Zhipu Qingyan? Is there any play between AutoGLM and CogVideoX?
- API call volume increased by 400% - is this number real growth or a by-product of the price war?

---

*This article is the 01st article in the series "Understanding Intelligent Intelligence AI". The next 3 articles will be released one after another. *
*This series is based on public information and does not constitute any investment advice. The AI ​​industry is changing rapidly. The data in this article is as of May 2026. Please refer to the latest announcement. *
