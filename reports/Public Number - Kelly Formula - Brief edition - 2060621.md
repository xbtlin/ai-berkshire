# A formula to solve the problem of "how much to buy"

The most common mistake in investing is not buying the wrong stock, but buying the right stock but in the wrong position.

If you are optimistic about a stock, if you buy too little, it will rise and you will feel nothing, but if you buy too much, it will fall and hurt your muscles and bones. How much should I buy? More than sixty years ago, a physicist gave a precise answer.

---

## Kelly's formula: four variables, one division

There are only four variables in an investment: the probability of winning, the probability of losing, how much you earn when you win, and how much you lose when you lose. The Kelly formula combines them into an optimal position:

> **Optimal position = winning rate ÷ loss margin - loss rate ÷ profit margin **

Intuitive understanding: The more you may lose, the less you should buy; the more you may make, the more you should buy. ** What the formula does is find the optimal balance between the two.

Give three examples:

**Example 1: Good opportunity - great chance of winning, but can afford to lose. **

For a stock, you judge that there is a 60% probability that it will double, and a 40% probability that it will fall by 50%.

> Position = 0.6 ÷ 0.5 - 0.4 ÷ 1.0 = 1.2 - 0.4 = **80%**

With a high winning rate, large room for upside, and limited downside, Kelly said you can take heavy positions.

**Example 2: Average opportunity - a bit of an advantage, but about the same. **

There is a 55% probability of a rise of 30% and a 45% probability of a fall of 30%.

> Position = 0.55 ÷ 0.3 - 0.45 ÷ 0.3 = 1.83 - 1.50 = **33%**

With only a small win rate advantage, the position should be significantly reduced.

**Example 3: No advantage – don’t touch. **

There is a 50% probability of a rise of 20% and a 50% probability of a fall of 20%.

> Position = 0.5 ÷ 0.2 - 0.5 ÷ 0.2 = 2.5 - 2.5 = **0%**

In a coin toss chance, the optimal position is zero - no bet should be made without an information advantage. If the calculation is negative, stay away.

The logic is very clear: **Opportunities that are truly worthy of a heavy position need to have a high winning rate, a large profit margin, and a limited loss margin. If any one of the three conditions is missing, the position should be reduced. **

---

## What happens if you buy too much? It’s not about making more, but it’s about losing everything.

This is the most counterintuitive aspect of Kelly’s formula. Many people think that "since they are optimistic about something, they should buy more." But mathematics tells you that after exceeding the optimal position, the more you buy, the less you will earn in the long term—until you lose everything.

![Kelly Curve](../assets/kelly/fig1-kelly-curve.png)

| Position strategy | Long-term growth rate | Volatility | One sentence summary |
|---------|-----------|------|-----------|
| Half Position Kelly | The best 75% | The best 50% | Earn less, but be more stable |
| Full position Kelly | 100% (theoretical optimal) | 100% | The fastest growing, but extremely bumpy |
| 1.5 times Kelly | The best 75% | The best 150% | The profit is the same as half position, but the fluctuation is three times |
| **2x Kelly** | **Zero** | Optimal 200% | **Busy in vain** |
| **More than 2 times** | **Negative number** | Higher | **Inevitable loss in the long run** |

Focus on the 1.5 times line: the growth rate is exactly the same as that of Half Kelly, but the volatility is three times that of Half Kelly. Not only will you not make more money if you buy more, you will also have to endure three times the suffering.

2x Kelly is even more extreme - making money on every trade but with zero long-term growth rate. **More than 2 times, even if you make a profit on every trade, you will eventually lose everything. **

This is not a theoretical deduction. In 1998, Long-Term Capital Management, with 25 times leverage, lost US$4.6 billion in four months; in 2021, Archegos Fund lost US$36 billion to zero in two days. It's not that they made a wrong judgment, it's that their positions were too heavy.

---

## Why losing 50% is more serious than you think

The reason why overbetting is fatal is because losses and profits are mathematically asymmetric:

![Loss Asymmetry](../assets/kelly/fig2-loss-asymmetry.png)

| Loss | Growth is needed to recover capital |
|------|-----------|
| -10% | +11% |
| -20% | +25% |
| -30% | +43% |
| -50% | **+100% (double)** |
| -75% | **+300% (up 3 times)** |

Lose 10%, gain 11% and come back. But if you lose 50%, you need to double it to get your money back. This is because investment is multiplication, not addition - a loss of 50% is multiplied by 0.5, a gain of 50% is multiplied by 1.5, 0.5 × 1.5 = 0.75, which cannot be returned to 1.

**The essence of Kelly's formula is to avoid large losses. ** Not losing money is the best strategy to make money.

---

## The formula is simple, but the difficult part is where the four numbers come from.

In a casino, the winning rate and odds are written on the rules and can be calculated accurately. But in stock investment, no one tells you these four parameters - you have to evaluate them yourself.

This is the real difficulty of Kelly's formula, and it is also its most profound point: **The quality of your estimates of the four parameters depends entirely on the depth of your understanding of the company. **

**Profit Margin – How much can you earn if you win? ** You have to know how much the company is worth and what discount the current price is on. This requires you to understand its business model, competitive landscape, and growth space. If you don’t understand the business, you can’t estimate its value, and you won’t know how much room there is for upside.

**Loss margin - How much will you lose if you lose? ** You have to know what will happen to the company in the worst-case scenario. Is it a short-term performance fluctuation, or is the business model being subverted? Will the cash flow be healthy and be able to survive, or will the balance sheet be fragile and shattered upon impact? If you don't understand business, you can't distinguish between "temporary difficulties" and "permanent damage."

**Winning rate - What is the probability of winning? ** You have to judge whether your valuation is reliable and whether the reasons for market underestimation are valid. This requires you to understand industry trends, management capabilities, and the depth of the moat. If you don't understand business, your "60% winning rate" may just feel good about yourself.

**Loss rate is 1 minus winning rate**. It does not need to be estimated separately, but it reminds you: no matter how confident your judgment is, it may be wrong.

The four parameters point to the same thing: **Do you understand this company or not? **

Therefore, the Kelly formula ultimately points not to a calculation problem, but to the most fundamental issue in investment - buying stocks means buying companies. ** The deeper you understand the company, the more accurate the parameter estimates will be, and the more reasonable the position decision will be. You know nothing about the company, the parameters are all guesswork, and the numbers calculated by the formula are meaningless.

This also explains why real investment masters dare to take heavy positions: not because they are brave, but because they spend a lot of time researching and understand the four parameters much more clearly than others. In their eyes, the fluctuations that panic the market are not risks at all, but just price swings.

---

## Two practical disciplines

After understanding the logic of the formula, it is enough to remember two disciplines in actual combat:

**First, discount in half. ** Even if you are very confident, only use half of what you think is a reasonable position. The reason is simple: Your estimate of your own judgment is almost certainly on the high side. Half-position Kelly only sacrifices 25% of the growth rate, but reduces the volatility by 50% - this deal is extremely cost-effective. Leave enough room for mistakes, because if you invest long enough, you will make mistakes.

**Second, set an upper limit. ** A single stock can never exceed 30% of total assets. No matter how confident you are, this is an iron rule. The previous mathematics has proven that exceeding the Kelly limit does not mean making more money, but leads to destruction.

---

##Finally

The Kelly Formula mathematically proves something investors should intuitively know:

**For companies that you can’t understand, the optimal position is zero. ** The parameters are all guesswork, and the calculated positions are meaningless.

**Only companies that understand it are qualified to discuss positions. ** The deeper the understanding, the more accurate the estimate and the more reasonable the position.

Back to the simplest sentence: buying a stock is buying a company. The Kelly formula just proves this point again with mathematics - your right to bet comes from your understanding of the company. **

---

*Reference:*
*Kelly, J.L. "A New Interpretation of Information Rate." Bell System Technical Journal, 1956.*
*Thorp, E.O. "Beat the Dealer." Random House, 1962.*
