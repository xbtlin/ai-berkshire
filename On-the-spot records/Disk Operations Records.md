#Real operation record

> **Caliber description**: This record discloses the direction, price and combination weight changes of each operation, but does not disclose the number and amount of shares (the original ledger is only saved locally). The weight is based on the shareholding portfolio (excluding cash and unexercised derivatives), converted based on the latest closing price on the record date, and rounded to an integer. Refer to Duan Yongping’s approach: make decisions public but not the scale.

| Date | Target | Operation | Price | Position changes | Remarks |
|---|---|---|---|---|---|
| 2026-04-21 | PDD (Pinduoduo) | Buy | $103.66 | First time opening a position (test position) | For details, see [Mirror Test](PDD_Systems Tests_2020421.md) |
| 2026-04-21 | Meituan (3690.HK) | Sell PUT (exercise price 85) | Royalty to be paid | If all options are exercised, Meituan’s weight will rise to about 30% of the portfolio | Actual cost is about 83~84, see [Mirror Test](%E2%99%AA The mirror test %E2%99%AA) for details |

---

## Current position (as of 2026-07-04, converted based on the closing price on 2026-07-03)

| Underlying | Portfolio weight (approximately) | Cost price |
|---|---|---|
| Tencent Holdings (0700.HK) | 47% | HK$453.75 |
| PDD (Pinduoduo) | 42% | $91.484 |
| Meituan-W (3690.HK) | 11% | HK$96.75 |

*The weight fluctuates with the market price, and the target allocation is not fixed. Closing price source: stockanalysis.com and Google Finance dual source cross (Tencent 431.20 / Meituan 71.60 / PDD $82.39, PDD is the closing price on July 2, and the US stock market is closed on July 3). *
