#MINIMAX——Wild samples of China’s AI large model track

> "Understanding MINIMAX" series · Chapter 01 · Beginning
> Reading time approx. 8 minutes

---

## A confusing company

On January 9, 2026, a strange company came to the Hong Kong Stock Exchange. Founded 4 years ago, with 385 employees, the annual revenue is less than 600 million yuan - but the stock price doubled on the first day of listing, and the market value exceeded 100 billion Hong Kong dollars.

This is no ordinary AI startup going public. On the first day of listing, the stock price increased from the issue price of HK$165 to HK$345, an increase of 109%. Two months later, it reached HK$680, with a market value of HK$210 billion.

As of May 2026, its stock price is around **HK$742**, with a market value of approximately **HK$250 billion** (approximately US$32 billion), and a 52-week fluctuation range of **220-1,330 Hong Kong dollars** - the highest point is 6 times the lowest point.

This company is called **MiniMax (Xiyu Technology)**.

But if you look at its financial report, you'll see a confusing set of numbers:

| Indicators | 2025 | Magnitude Judgment |
|------|--------|---------|
| Total revenue | **US$79.04 million** (approximately 570 million yuan) | The annual revenue of a company with a market capitalization of HK$250 billion is less than 600 million |
| Revenue growth rate | **+158.9%** | Extremely fast |
| Gross profit margin | **25.4%** (vs 12.2% in 2024) | Rapid improvement |
| Adjusted net loss | **251 million US dollars** (approximately 1.8 billion yuan) | More than 3 times revenue |
| Loss during the year (including changes in fair value) | **1.872 billion US dollars** | The book figures are scary |
| Selling expenses | **51.9 million US dollars** (-40.3% year-on-year) | Abnormal signal: revenue increased by 159% but marketing expenses fell by 40% |
| Cumulative users | **236 million**, covering 200+ countries | Overseas revenue accounts for over 70% |
| Employees | **385 people**, average age** 29 years old** | Post-95s generation supports a market value of 100 billion |

**A company with annual revenue of less than 600 million yuan has a market value of HK$250 billion. Annual loss is 1.8 billion yuan. 385 people. **

If you think this is a bubble - you're probably right.
If you think there's an opportunity here - you're probably right too.

These two judgments are not contradictory because they look at different aspects of the same company.

---

## Who is MINIMAX?

MINIMAX (Xiyu Technology) was founded in Shanghai in early 2022 by **Yan Junjie**. Yan Junjie, born in 1989, received a bachelor's degree from the University of Science and Technology of China and a PhD in computer science from Carnegie Mellon University (CMU). He was the vice president and head of general intelligence technology at SenseTime.

Key time point: **At the end of 2021**, Yan Junjie resigned from SenseTime to start a business. At this time, there is still nearly a year before ChatGPT breaks out (November 2022) - he bet on the direction of large models earlier than most people.

In 4 years and 7 rounds of financing, the cumulative financing exceeded **1.5 billion**. Investors include Tencent, Alibaba, miHoYo, Hillhouse Capital, and Sequoia China. The Hong Kong stock market was listed in January 2026, raising **5.54 billion HKD**. 14 cornerstone investors (Alibaba, Abu Dhabi Investment Authority, E Fund, etc.) subscribed **2.723 billion HKD**, and the public offering was oversubscribed **1,837 times**.

**It only took 4 years from establishment to IPO, which is one of the fastest IPO records in the global AI field. **

But speed does not equal quality. To understand this company, you need to first understand what it is selling.

---

## Four product lines, one base

MINIMAX is the only startup company in China that has achieved world-class standards in the four modes of text, voice, video and music. Its product matrix looks like this:

| Products | Positioning | Key figures | Revenue share (2025) |
|------|------|---------|------------------|
| **Talkie/Hoshino** | AI social role playing | Cumulative users **147 million**, MAU **27.6 million**, overseas MAU **11 million** (50%+ from the United States) | ~67% (AI native product) |
| **Conch AI** | AI video generation + AI assistant | Cumulative users **42.34 million**, Hailuo 02 supports 1080p native resolution | Included in AI native products |
| **MiniMax Open Platform** | Large model API service | **214,000** enterprise customers and developers, covering 100+ countries | ~33% (growth rate **297%**) |
| **Speech-02** | Speech synthesis (TTS) | Ranked **No. 1** on the global Arena double list, surpassing OpenAI and ElevenLabs, with human voice similarity **99%** | Included in the open platform |

The bottom layer is the self-developed **M2.7 large model** - MoE architecture, with total parameters **230 billion**, activation parameters **10 billion**, and supports **200K tokens** ultra-long context. It scored **56.22%** in the SWE-Pro benchmark test, its code capabilities are close to the GPT-5.3-Codex level, and its price is only **1/10 to 1/20** of Opus 4.6.

**Summary in one sentence: MINIMAX = self-developed multi-modal large model (base) + Talkie (overseas AI social networking) + Conch AI (video generation) + open platform (API service). **

---

## Three common misjudgments about MINIMAX

### Misjudgment 1: MINIMAX is just another startup company making large models

There are so many large-scale startups in China - hundreds of them in 2023, and less than ten left in 2025. Most people classify MINIMAX into the "Six Little Tigers of the Big Model" (Dark Side of the Moon, Wisdom Spectrum, Baichuan, Zero One Thousand Things, MINIMAX, Step Star) and then brush it off.

But there are essential differences between MINIMAX and other companies: **It doesn't just do models, it does applications; it doesn't just do domestic work, it does global work; it doesn't just do text, it does full modality. **

Six Little Tigers:
- The Dark Side of the Moon (Kimi) focuses on long text and search enhancement, almost purely in the domestic market
- GLM focuses on academic and enterprise services, open source route
- Baichuan and Zero-One Everything have shrunk or transformed

MINIMAX is the company with the highest **overseas revenue** (over 70%), the most complete product line** (text + voice + video + music), and the largest user base** (236 million).

**Opposite view**: A complete product line also means that the front is too long. 385 people are working on 4 product lines at the same time, and resources are severely dispersed. A startup’s ammunition should be used focused, not peppered.

### Misjudgment 2: The market value of 250 billion is a pure bubble

Market capitalization of HKD 250 billion (approximately RMB 230 billion) / revenue of RMB 570 million = PS approximately **400 times**. This number does seem crazy.

But there are a few facts to consider:
- By the end of February 2026, ARR has exceeded **150 million US dollars** (approximately 1.1 billion yuan), corresponding to a monthly revenue of approximately **12.5 million US dollars**, which is nearly **twice** the monthly average level in 2025
- The number of new registered users on the open platform will reach **more than 4 times that in December 2025** in February 2026
- The cost of M2 series inference computing power has dropped by more than **50%** compared with December 2025
- If the full-year revenue in 2026 reaches **150-200 million US dollars** (approximately 1.1-1.4 billion yuan), PS will drop to about **160-210 times**

Still very expensive. However, the valuation logic of AI companies is not based on current revenue, but on the final scale and path to arrival.

**Contrary view**: PS is still ridiculously high at more than 160 times. And the "endgame scale" is purely imaginative pricing - the same rhetoric was used during the Internet bubble in 2000. A company with an annual loss of 1.8 billion yuan is far from breaking even.

### Misjudgment 3: MINIMAX will be crushed by big manufacturers

ByteDouBao MAU has exceeded **226 million** (December 2025), and the average daily Token calls have exceeded **50 trillion**. Alibaba Tongyi Qianwen MAU **25.72 million**. Although Baidu Wenxinyiyan lags behind, it still has the advantage of search entry.

These giants have **more than 10 times** advantages in capital, traffic and computing power. Why does MINIMAX survive?

The answer is **niche differentiation**:
- **Talkie is doing overseas social AI**. The giants have no first-mover advantage in this track. Byte and TikTok themselves face geopolitical risks.
- **Conch AI is engaged in video generation**, which is the sub-field with the highest growth rate (annual growth of 100%+), and the giants have just begun to catch up.
- **The world’s No. 1 speech synthesis**, this vertical capability has not been crushed for the time being.

**Contrary view**: Niche differentiation can only last for a while. ByteDance is rapidly catching up in video generation; Google may refocus its efforts on social AI after incorporating Character.AI; once the giants get serious about it, the first-mover advantage of startups may only last 6-12 months.

---

## Four core questions that need to be answered to understand MINIMAX

MINIMAX is not an easy company to characterize. It has multiple labels as "the best AI startup company in China" - the fastest IPO, the highest proportion of overseas revenue, the most comprehensive multi-modal capabilities, and the youngest team - but it also faces all the common problems of AI startups: burning money, no moat, being crushed by giants, and inflated valuations.

To understand it, you need to answer at least four questions:

| Question | Core Conflict | Which part of this series to start |
|------|---------|---------------|
| What is the level of products and technology? | The real competitiveness of Talkie, Conch AI, and speech synthesis | Chapter 02 |
| How to survive in a track full of giants? | Competition with Byte, Alibaba, and DeepSeek | Chapter 03 |
| Do you have enough money to burn? Can you make money? | Annual loss of 1.8 billion vs. race to double income | Chapter 04 |
| Will this company still be there in 10 years? | The survival probability of startup companies in the AGI era | Chapter 04 |

---

## A preview: The war between 385 people born after 1995

In the next article, we will dismantle MINIMAX’s products and technologies—why does Talkie defeat Character.AI overseas? What is the level of video generation of Conch AI? Is being ranked No. 1 in the world in speech synthesis a real skill or just a ranking? Why does the M2.7 large model dare to say "self-evolution"?

A few tough questions to answer:

- How valuable is Talkie’s **27.6 million MAU**? Daily active users are nearly 10 million, and average daily usage is **70 minutes**—are these numbers credible?
- Conch AI was jointly sued by Disney, Universal Pictures, and Warner Bros. for copyright infringement—what does this lawsuit mean?
- How can 385 people support four product lines at the same time? Is this efficiency real or is it survivorship bias?
- World No. 1 in speech synthesis—can it be turned into real money?

See you in the next article.

---

*This article is the 01st article in the "Understanding MINIMAX" series. The next 3 articles will be released one after another. *

*Disclaimer: This article does not constitute any investment advice. MINIMAX (00100.HK) is a company listed on the Hong Kong stock market. The AI ​​industry is changing rapidly, and the data in this article may not be the latest. Please base your investment decisions on the latest financial reports and independent judgment. *

*Data sources: MiniMax 2025 annual report, Hong Kong Stock Exchange announcement, Wall Street News, 36Kr, Qubit, Artificial Analysis Arena, QuestMobile*
