# MINIMAX (9922.HK) Business Model Analysis

**Analytical perspective: Duan Yongping** | **Date: April 9, 2026** | **Information richness: C level**

> "Do the right thing, do it right." —— Duan Yongping

---

## Important statement

Due to the limitations of the original analysis agent, this report was supplemented and completed by the Team Lead based on existing research data. The information richness is C level, and the first principles model is used to focus on core issues.

---

## 1. The essence of business model

### 1.1 Core business definition

MINIMAX (Xiyu Technology) is an **AI large model + application integrated company**. It develops self-developed general large models and builds a variety of consumer-level and enterprise-level products on this basis.

**Essence of business model**: Use self-developed large model capabilities to drive multiple AI application products, and achieve commercialization through ToC subscription/in-app purchase and ToB API calls.

### 1.2 Product Matrix and Revenue Structure

| Product | Positioning | Target market | Monetization model | Revenue proportion (estimate) | Confidence |
|------|------|---------|---------|----------------|--------|
| **Talkie** | AI social/role playing | Overseas (mainly North America) | Subscription + virtual items | ~40-50% | Low |
| **Conch AI** | AI assistant | China | Free + paid membership | ~10-15% | Low |
| **Hailuo AI** | AI video generation | Global | Free quota + paid | ~10-15% | Low |
| **MiniMax API** | Model as a service | B-side enterprise | API call pay-as-you-go | ~20-30% | Low |

> Duan Yongping’s comment: "A company does four things at the same time, and fails to achieve perfection in each one. This is not a good signal. A good company should focus on a core product and make it irreplaceable."

### 1.3 Revenue scale

| Year | Revenue (RMB, estimated) | Confidence level |
|------|-------------------|--------|
| 2023 | ~500-700 million yuan | Mid-low |
| 2024 | ~2.5-3.5 billion yuan | Low |
| 2025 (forecast) | ~5-8 billion yuan | Low |

---

## 2. Analysis of flywheel effect

### MINIMAX’s theoretical flywheel

```
User growth → Usage data accumulation → Model optimization (RLHF) → Better product experience → More users
    ↑                                                              ↓
    ←—————————— Word-of-mouth / Community Content ——————————————————←
```

### Flywheel Verification

| Flywheel link | Operating status | Rating |
|---------|---------|------|
| User growth → Data accumulation | Talkie has a certain user scale and social data is valuable | ★★★ |
| Data → Model Optimization | User feedback can optimize the quality of character dialogue, but it is not as barrier-free as search/e-commerce data | ★★ |
| Model optimization → Experience improvement | It has a certain effect, but the underlying model capability relies more on computing power investment | ★★ |
| Experience → User retention | The user retention rate of AI applications is generally not high, and the flywheel is leaking in this link | ★★ |

**Conclusion**: The flywheel exists but the speed is not fast and water leakage is obvious. Compared with Douyin (content recommendation flywheel) or Pinduoduo (low-price flywheel), MINIMAX’s flywheel effect is far from strong enough.

> Duan Yongping's comment: "The true flywheel effect is that the more users, the better the product, the stronger the competitive advantage - it should be self-reinforcing. If the flywheel requires continuous large investment of funds to rotate, then it is not a real flywheel, but a machine that needs constant refueling."

---

## 3. Moat analysis

### Verify one by one

| Moat type | Existence | Analysis | Score |
|-----------|---------|------|------|
| **Brand** | Weak | Talkie has a certain reputation in the overseas AI social track, but the brand loyalty of AI products is extremely low, and users care more about functions than brands | ★★ |
| **Switching Cost** | Extremely weak | The switching cost of AI applications is almost zero. The user's chat history and self-created roles may constitute a slight switching cost, but it is far from enough | ★ |
| **Network Effect** | Weak | Talkie's UGC character ecology and community have a weak network effect - the more characters → the more users → the more creators. But this effect is not as strong as social platforms | ★★ |
| **Scale effect** | Weak | AI inference costs decrease with scale, but the scale effect of GPU computing power is far less than the diminishing marginal cost of software | ★★ |
| **Technical Barriers** | Medium | There are certain thresholds for self-developed multi-modal large models (text + speech + video + music), especially video generation (Hailuo) and speech synthesis. However, large model technology iterates very quickly and may be matched in 6-12 months | ★★★ |

### Comprehensive assessment of moat

**Overall rating: ★★ (very weak)**

> Duan Yongping's perspective: "Moat is the lifeblood of a business. A business without a moat, no matter how good it looks, is only temporary. MINIMAX's current moat comes more from 'being one step ahead' than from real structural advantages. In the AI industry where technology changes rapidly, the advantage of being one step ahead may only last half a year."

---

## 4. User/customer value

### C-side value (Talkie/Conch AI)

| User groups | Core needs | Value provided by MINIMAX | Uniqueness |
|---------|---------|-----------------|--------|
| Generation Z young people | Emotional companionship, entertainment | AI role-playing, virtual social networking | Medium (Character.AI, etc. are also available) |
| Creator | Video/picture generation | Hailuo AI video generation | Higher (leading quality + speed) |
| Domestic users | AI assistant/search | Conch AI | Low (Doubao/Kimi is better to use) |

### B-side value (API)

| Customer type | Needs | Value provided by MINIMAX |
|---------|------|-----------------|
| Small and medium-sized developers | Low-cost AI capability calling | Multi-modal API (text + voice + video) |
| Enterprise customers | Customized AI solutions | Large model capabilities + fine-tuning services |

**Core question**: MINIMAX has created value for users, but are these values **irreplaceable**? The answer is most likely no - competing products can provide a similar or even better experience.

---

## 5. Business matrix and synergy

### Synergy Effect Assessment

```
        MiniMax large model (low-level capabilities)
           /     |      \       \
     Talkie Hailuo AI Hailuo API
     (Overseas) (Domestic) (Video) (B-side)
```

| Synergy Dimensions | Description | Strength |
|---------|------|------|
| Technology sharing | All products share a set of underlying large models to reduce duplication of research and development | Strong |
| Data feedback | User data of each product can be used for model training and improvement | Medium |
| User diversion | Cross-diversion between products is limited (overseas/domestic/B-end user groups are different) | Weak |
| Brand synergy | The synergy effect of the "MiniMax" brand among various products is limited | Weak |

**Conclusion**: Collaboration at the technical level is real, but synergy at the business level is very weak. Multiple product lines are more about spreading resources than creating synergistic value.

---

## 6. Duan Yongping’s “Good Business” Standard Evaluation

### 6.1 Differentiation

| Comparative dimensions | MINIMAX | Byte Beanbao | DeepSeek | The Dark Side of the Moon Kimi |
|---------|---------|---------|----------|-------------|
| Core positioning | Multi-modal + overseas social networking | All-round AI assistant | Open source large model | Long text + search |
| Degree of differentiation | Medium (video generation + social) | Low (traffic wins) | High (open source + low cost) | Medium (long text features) |
| Moat depth | Shallow | Deep (traffic ecology) | Medium (open source community) | Shallow |

**MINIMAX’s differentiation is mainly reflected in**:
1. **Multi-modal capabilities such as video/voice/music** - cannot beat plain text, but multi-modal comprehensive capabilities have advantages
2. **Overseas Market** - Talkie avoids the traffic crush of domestic giants
3. **AI social/role playing** - not a tool AI, but an entertainment/companion AI

### 6.2 Pricing Power

**Rating: ★☆☆☆☆ (barely)**

- The AI API market is experiencing a fierce price war, and DeepSeek has driven the price to extremely low levels
- Talkie’s subscription pricing is limited by users’ willingness to pay (the ARPU of AI social is much lower than streaming media/games)
- Hailuo AI’s video generation oscillates between free and paid, and stable pricing has not yet been established.
- Overall, MINIMAX** has no pricing power** and is driven by market competition and user expectations.

> Duan Yongping commented: "A business without pricing power is not a good business. If you raise the price, customers will leave, and the profit from lowering the price will be gone - this is a business that suffers from both sides. Maotai can raise prices at will, because this is the brand that users recognize. Can MINIMAX raise prices? No."

### 6.3 Sustainable Competitive Advantage

**Will the advantages still exist after 3-5 years? **

| Current Strengths | Outlook 3-5 Years | Sustainability |
|---------|------------|---------|
| Talkie’s overseas user scale | Depends on whether the community ecology can continue to be active | Medium |
| Hailuo video generation technology | High probability of being tied (Byte/OpenAI invests more) | Low |
| Multi-modal comprehensive capabilities | Giant multi-modal capabilities are also catching up quickly | Low |
| Self-developed model | The performance of open source models is approaching, and the advantages of self-developed models are shrinking | Low |

**Conclusion: Sustainable competitive advantage is questionable. ** The only possible sustainable advantage is Talkie’s overseas community ecology, but this requires continuous operational investment and content innovation.

---

## 7. Overall conclusion

### Duan Yongping's "Good Business" Rating

| Criteria | Rating | Description |
|------|------|------|
| Differentiation | ★★★ | Multi-modal + overseas social networking has a certain degree of differentiation, but not deep enough |
| Pricing power | ★ | Almost no pricing power, driven by the market |
| Sustainable competitive advantage | ★★ | Most of the current advantages are not sustainable |
| The business model is simple and clear | ★★ | The four product lines are scattered and the model is not simple enough |
| Free cash flow | ★ | Deep cash burn, deep negative free cash flow |

### **Business model dimension comprehensive score: ★★☆☆☆**

> Duan Yongping’s final verdict: "MINIMAX is a company that pursues technology, and what the team is doing can be considered the 'right thing' - the general direction of AI is fine. But from a business perspective, this is not a good business. It has no pricing power, no moat, no free cash flow, and it is fighting on multiple fronts in a battlefield filled with giants. If you must invest in AI, it is better to invest in a platform company that has proven itself, rather than a startup that is still burning money to prove itself."

---

**Data Limitation Statement**: Most of the data in this report are estimates (confidence has been marked). Due to limitations of the original analysis agent, real-time data cannot be obtained through WebSearch. Readers are advised to verify with MINIMAX's latest prospectus and financial reports.
