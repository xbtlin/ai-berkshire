# Four-square mode and five-layer moat

> "Understanding MasterCard" Series·Part 02
> Reading time is about 10 minutes

---

## Sifang Model: Why this business is almost impossible to copy

The global payments market exceeds $100 trillion annually. As the infrastructure layer, Mastercard does not own any funds or bear any bad debts, but it takes away the most stable part of the profits in the entire link. To understand the logic behind this, we need to start with the four-party model.

Participants in the four-party model:

| Role | Who | What | What risks |
|------|---|--------|------------|
| Cardholder | You | Card consumption | Repayment responsibility |
| Card issuing bank | Your bank (such as ICBC, China Merchants Bank, Citigroup) | Card issuance, credit extension, interest collection | **Credit risk** |
| Acquiring bank | Merchant’s bank | Provide card swiping services to merchants | Merchant default risk |
| Card Network | **MasterCard** (or Visa) | Authorization, Clearing, Settlement | **Almost Zero** |

The key is in the last column: **Mastercard keeps the "tolls" to itself and assigns credit risk and merchant services to the bank. **

This is a natural consequence of network effects – banks are willing to take risks because access to Mastercard means issuing cards that can be accepted by 100 million merchants around the world. Without access, the card is just waste plastic.

### To what extent is it asset-light?

FY2025 data:

| Indicators | Mastercard | Meaning |
|------|---------|------|
| Net Profit Margin | **45.7%** | Net nearly $46 for every $100 in revenue |
| Operating profit margin | **59.2%** | Extremely high operating efficiency |
| Free cash flow / net profit | **109%** | Almost all net profit is converted into real money |
| ROIC | **43-50%** | Earn 43-50 cents for every $1 invested |
| Credit risk exposure | **0** | No lending, no holding of consumer debt |

Data source: [Mastercard FY2025 Annual Report](https://s25.q4cdn.com/479285134/files/doc_financials/2025/q4/4Q25-Mastercard-Earnings-Release.pdf), [ROIC Data](https://www.gurufocus.com/term/roic/MA)

**Opposite view**: Some people say that "not taking risks" also means "not controlling customer relationships" - the direct relationship between cardholders and merchants is with the bank, not with MasterCard. This is true. However, Mastercard has been transforming into "direct value delivery" through value-added services (fraud detection, data analysis, identity verification) - the revenue share of value-added services in FY2025 has exceeded **40%**, with a growth rate of **23%**. This will be expanded upon later.

---

## Five-layered moat: deep and multi-layered

Mastercard’s moat isn’t a wide ditch—it’s five layers of fortifications stacked on top of each other.

### First layer: Network effect (strongest)

- More than **3 billion** Mastercard cards in circulation worldwide
- Over **100 million merchants** accept Mastercard
- Covering **more than 200 countries and regions**

The network effect is two-way: the more cardholders there are, the more merchants are willing to connect; the more merchants there are, the more willing banks are to issue cards; the more banks issue cards, the more cardholders there are.

To build a new global payment network, you need to convince all banks, all merchants, and all consumers at the same time - this is the classic "chicken or egg" problem. In the past 50 years, only two multinational card networks have been successfully established in the world: Visa and Mastercard. There is no third one.

**Contrary view**: China UnionPay is the world’s largest card network in terms of card issuance volume. However, more than 90% of UnionPay’s transaction volume comes from within China**, and its acceptance by overseas merchants is much lower than that of Visa and MasterCard. Large scale does not mean strong network effects - the key is **cross-border interconnection capabilities**.

### Second level: switching cost (very high)

For a bank to switch from Mastercard to another network, it means:
- Re-sign and re-issue cards (physical replacement of tens of millions of cards)
- Reconnect all acquirer and merchant systems
- Consumers’ automatic deductions, subscription services, and bound payments are all invalid.

The cost is **astronomical**. Therefore, in reality, there have almost never been cases of large-scale "defection" of banks from card networks.

### The third layer: regulatory barriers

Payment networks are required to obtain **regulatory licenses, anti-money laundering compliance certifications, and PCI-DSS security certifications** in more than 200 countries around the world. These licenses cannot be bought with money – they are the result of decades of accumulation and involve long-term relationships with central banks and financial regulators.

Even if a new entrant has technical capabilities, it will take more than ten years to obtain all global licenses.

### The fourth layer: data assets

Mastercard processes **175.5 billion** transactions annually (FY2025) amounting to **$10.6 trillion**. These data provide it with:
- **Fraud Detection**: Real-time analysis of transaction patterns, accuracy continues to improve
- **Consumer Insights**: Products such as SpendingPulse provide governments and businesses with macro consumption data
- **Precision Marketing**: Help merchants improve conversion rates

The value of data grows **exponentially** with scale - the more transactions processed, the more accurate the fraud models, and the more valuable the value-added services become. This cannot be replicated by later entrants.

### Level 5: Brand Trust

In the world of payments, "trust" is everything. Consumers and merchants choose Mastercard because it means "the transaction will be completed and the funds will be received." This trust is built on decades of operational record without major accidents**.

---

## Flywheel effect: spinning faster and faster

The five-layered moat forms a self-reinforcing flywheel:

```
More cardholders → Merchants are more willing to accept → More merchants access
    ↑                                    ↓
    ← Better user experience ← More value-added services ←
```

And value-added services are adding new dimensions to the flywheel:

| Types of value-added services | Function | FY2025 performance |
|------------|------|------------|
| Cybersecurity and fraud detection | Reduce merchant/bank losses | One of the fastest growing sectors |
| Data analysis (SpendingPulse) | Provide customers with consumption insights | Extremely low marginal cost |
| Identity Authentication | Digital Business Infrastructure | New Scenarios for Agency Business |
| Precision marketing | Help merchants improve conversion rates | High repurchase rates |

In FY2025, the revenue share of value-added services has exceeded **40%**, the growth rate is **23%**, and the Q4 single-quarter growth rate is **26%**. This means that Mastercard is no longer just "collecting tolls" - it is also "selling navigation, selling insurance, and selling data" to people who pass through toll booths.

Data source: [Mastercard Q1 2026 results](https://www.tikr.com/blog/mastercard-q1-2026-earnings-revenue-hits-8-4b-eps-up-23)

---

## A key question: Are PayPal and Stripe competitors?

Many people view PayPal, Stripe, and Square as competitors to Mastercard. The reality is more nuanced.

| Company | Superficial role | Actual relationship |
|------|---------|---------|
| PayPal | "Digital wallet that bypasses the card network" | The bottom layer of most transactions is still Visa/Mastercard settlement |
| Stripe | "Online Payments Infrastructure" | Is Mastercard's **largest customer**, not a substitute |
| Square/Block | "Offline POS + Cash App" | The scale is much smaller than the card network and relies on the card network for settlement |

PayPal is indeed experimenting with "closed-loop payments" (paying directly with a bank account, bypassing the card network) and has also launched the PYUSD stablecoin. But as of now, the majority of PayPal transactions still end up being settled through the Visa/Mastercard network.

**This is the power of network effects**: Even if you want to bypass Mastercard, your users and merchants will most likely still be using Mastercard’s network.

**Opposite view**: In the long term, if digital wallets such as PayPal, Apple Pay, and Google Pay continue to promote account-to-account (A2A) payments, they may indeed cannibalize some card network transaction volumes. The risk exists, but at a much slower pace than expected—due to the extremely high switching costs of consumer habits and merchant systems.

---

## Duopoly with Visa

Mastercard and Visa together control **more than 80%** of the world's cross-border card network payment volumes:

| Network | Global card network market share | Relationships |
|------|------------------|------|
| Visa | **43.9%** | Boss |
♪ Mastercard ♪ 36.4% ♪ Penn ♪
| China UnionPay | ~15% | Mainly in China |
| American Express | ~4% | High-end niche |
| Others | <1% | Ignore |

Data source: [Capital One Shopping Research](https://capitaloneshopping.com/research/credit-card-market-share-statistics/)

Key features of a duopoly: **This is not a zero-sum game**. Visa and Mastercard's real rival is **cash**, not each other. Both benefit from every 1 percentage point increase in global cashless penetration. They are more like "two toll booths on the same highway" - increased traffic is a good thing for both.

**Consideration**: The duopoly pattern also means regulatory risks - when two companies control too much market share, the government may intervene. The European Union has already implemented a cap on interchange fees, and the United States is also under pressure from antitrust scrutiny. This risk is discussed in detail in Part 04.

---

## Summary of this article

| Dimensions | Judgment |
|------|------|
| Business model | Sifang model - allocate risks to banks, leave "tolls" to yourself, be asset-light to the extreme |
| Moat Depth | Five-layer Overlay: Network Effect + Switching Cost + Regulatory Barriers + Data Assets + Brand Trust |
| Flywheel status | Accelerating – value-added services add new dimensions |
| Competitor threats | Fintechs more customers than enemies – but long-term A2A payments are worth watching |
| Duopoly | Solid, the real enemy is cash, not each other |

---

## Next issue preview

No matter how deep the moat is, it depends on how big the business can grow. In the next article, we will talk about room for growth:

- How much cash is there in the world waiting to be digitized?
- Why is cross-border payment the "gold mine with the highest profit margin"?
- Can value-added services grow from 40% to 60%?
- Mastercard Move What does it mean to connect 17 billion endpoints?

---

*This article is the 02nd article in the series "Understanding MasterCard". The next 3 articles will be released one after another. *
*This series does not constitute any investment advice. *
