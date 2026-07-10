# LiblibAI Competitive position and moat in-depth analysis

**Analysis Date**: May 23, 2026
**Confidence annotation**: 🟢High / 🟡Medium / 🔴Low

---

## 1. Track status assessment

### 1.1 Domestic AI image generation track market share

| Indicators | LiblibAI | Jimeng AI (byte) | Keling AI (Kuaishou) | Meitu | Civitai (overseas) |
|------|----------|---------------|---------------|------|----------------|
| Registered users | 25 million 🟢 | Undisclosed (MAU about 12 million+) 🟡 | MAU 12 million 🟢 | MAU 276 million 🟢 | 3 million+ 🟡 |
| Monthly active | 4 million 🟢 | 12-20 million 🟡 | 12 million 🟢 | 276 million 🟢 | 12-13 million 🟡 |
| Annualized revenue | Domestic ARR ~ US$1.5 million (2024); Lovart ARR ~ US$80 million (2026E) 🟡 | Not independently disclosed 🔴 | ~US$140 million (2025) 🟢 | RMB 3.9 billion (company-wide) 🟢 | Not disclosed 🔴 |
| Latest financing/valuation | US$130 million Series B, valuation ~US$1 billion 🟢 | Byte's own funds | Proposed spin-off, valuation ~20 billion 🟡 | Hong Kong stock listing, market value ~ HK$20 billion 🟡 | US$5.1 million (a16z) 🟢 |

### 1.2 The value of "first"

LiblibAI's "first" needs to be added with an attributive: **China's largest "AI model community and aggregate creation platform", rather than the largest "AI image generation product". **

- **Model Community Track**: No. 1 in China, second only to Civitai in the world 🟢
- **Pan AI Image Generation Track**: Jiemeng’s monthly activity is higher, Keling’s income is higher, and the number of Meitu users far exceeds that of others. LiblibAI is not the first overall 🟡
- **Professional AI creation tool**: For professional users such as designers, e-commerce artists, etc., leading in the country 🟡

### 1.3 International market position (Lovart)

- Launched in June 2025, ARR exceeded US$30 million in 4 months, and ARR is estimated to reach US$80 million in 2026 🟢
- The United States is the largest single market, covering 70+ countries
- Musk’s likes bring millions of exposures
- Known as "the world's first AI design agent"

**Judgment**: Lovart is in a leading position in the emerging field of overseas "AI Design Agent", but the track is still in its early stages and the competitive landscape is far from finalized.

---

## 2. In-depth analysis of moat

### 2.1 Network Effect

**Rating: 3.5/5 | Judgment: Medium to wide, widening**

- **Bilateral network effect structure**: Model creators (500,000+LoRA) ↔ users (25 million users)
- **Forward Loop**: More models → more users → more payments → more creators
- **Comparison with mature platforms**: Bilibili (★★★★★, highly differentiated content) > Taobao (★★★★★, transaction lock) > LiblibAI (★★★, bilateral network exists but lock-in power is limited)
- **Key Weakness**: The LoRA model is portable and users can download it and use it on other platforms. However, the cloud reasoning + community discovery mechanism partially makes up for this weakness.
- **Critical Mass Judgment**: 500,000 models + 25 million users have exceeded the basic critical mass, and new entrants will need 2-3 years to catch up. But it is not insurmountable against giants like Byte 🟡

### 2.2 Data Barriers

**Rating: 3.0/5 | Judgment: Medium width, slowly widening**

- Cumulative prompt-image pairing data of 500 million+ pictures
- Usage preference data of 500,000+ models
- User workflow data (creation habits, model combination methods)
- **Self-enhancement effect exists**: The greater the usage → the more data → the more accurate the recommendations → the better the experience
- **Limitations**: Jimeng/Keling is backed by Byte/Kuaishou and naturally has massive data. The barriers may be deeper than LiblibAI 🟡

### 2.3 Switching costs

**Rating: 3.0/5 | Judgment: Medium width, stable**

| Asset type | Migration difficulty |
|---------|---------|
| Trained LoRA model | Medium (can be downloaded but reconfiguration will take time) |
| Workflow configuration | Medium to high (complex workflows are expensive to rebuild) |
| Community relations/fans | Medium to high (it is difficult for head creator fans to migrate) |
| B-side API integration | Medium to high (involving development and testing) |
| Favorite Model Library | Low |
| Creation History | Low |

Compared with Photoshop/Figma (extremely high conversion cost), LiblibAI is more similar to a material website - it has inertia but does not constitute a strong lock-in.

### 2.4 Brand Mind

**Rating: 2.5/5 | Judgment: Moderately narrow, being widened**

- Professional AIGC Creator Circle: "AI Photo Generation = LiblibAI" part established 🟢
- Mass market: limited popularity, "AI-generated pictures" are more associated with beautiful pictures and dreams 🔴
- Lovart: After the Musk effect, product strength supports retention (ARR 30 million → 80 million), not just one-time traffic 🟢

### 2.5 Economies of Scale

**Rating: 3.0/5 | Verdict: Medium width, widening**

- GPU inference scale effect: the more users, the higher the utilization rate, and the lower the single cost 🟢
- Community model has zero marginal cost (UGC model) 🟢
- Compared with Jimeng/Keling, which needs to invest a lot of R&D expenses to maintain self-developed models, the cost structure is lighter
- **Limitations**: The scale effect is not unique to LiblibAI. Any large-scale AI platform enjoys similar effects.

---

## 3. Moat vulnerability test

### 3.1 Byte invests 1 billion to build a similar platform?

- **Short term (within 1 year)**: The moat is still there, community migration has inertia, and the 500,000 model library cannot be copied at once. Lumi is not fully open yet 🟢
- **Mid-term (2-3 years)**: The pressure has increased significantly, and the merger of Jimeng + Lumi will form integrated competition 🔴
- **Conclusion**: Byte is the biggest single threat, but its efforts are highly dispersed. LiblibAI window period is about 2-3 years 🟡

### 3.2 Does GPT-5 support LoRA-level fine control?

- The "intermediate value" of community models will shrink significantly 🔴
- But it will not be completely zeroed: professional scenes still need fine tuning 🟡
- **Coping Space**: From "model supermarket" to "creative workflow platform", LibTV and Xingliu Agent are in this direction 🟢
- **Conclusion**: Real but gradual threat, complete replacement will take a long time

### 3.3 Midjourney open model community?

- Big impact on Lovart overseas 🔴
- Limited impact on domestic business (access barriers + insufficient localization) 🟢
- Lovart is positioned as a "design agent" rather than a "model community", and the competition dimensions do not completely overlap 🟡
- **Conclusion**: Increase overseas competitive pressure, but will not subvert the overall value

---

## 4. Evolution trend of moat

| Moat Dimension | Current Rating | Trends | Reasons |
|-----------|---------|------|------|
| Network Effects | 3.5/5 | **WIDENING** | Users and models continue to grow, LibTV/StarStream expands multi-modal dimension |
| Data Barriers | 3.0/5 | **Slow Widening** | Data volume accumulates but exclusivity is limited |
| Switching cost | 3.0/5 | **Stable** | Workflow and API depth are increased, but C-side migration is still easy |
| Brand Mind | 2.5/5 | **Widening** | Lovart globalization + LibTV expands awareness |
| Economies of scale | 3.0/5 | **Watching in progress** | Increased user scale brings cost reduction |

**Comprehensive judgment**: The moat is deepening, but not as fast as the growth of competitive threats.

### The evolutionary path from "model supermarket" to "AI creation operating system"

**Doable but challenging. **

- 2023-2024: Model supermarket stage
- 2025: 2.0 upgraded to "AI Professional Creation Studio"
- 2026: LibTV+Xingliu Agent, evolving towards video and agent

The key to success: Deep enough ecological barriers must be established before the giant completes the integration of "model + community + distribution". The window period is about 2-3 years.

---

## 5. Overall evaluation

**Moat overall rating: 3.0/5 (medium)**

1. LiblibAI has established a meaningful first-mover advantage in the "AI model community" segmented track, but its protection against giants like Byte is limited.
2. Lovart is the brightest growth point (0→$80 million ARR) and may become the most valuable part of the overall valuation
3. The biggest risk is "middle layer extrusion" - upstream basic mold companies may build their own platforms, and downstream users may directly use general-purpose large models.
4. The US$1 billion valuation plus Lovart’s revenue is within the understandable range. The key assumption is whether Lovart can continue to grow.

---

Sources:
- [4 million monthly active users, 25 million users, US$130 million - Sina Finance](https://finance.sina.com.cn/stock/t/2025-10-23/doc-infuvrat2626622.shtml)
- [LiblibAI commercial ARR exceeds US$1.5 million - Yibang Power](https://m.ebrun.com/555577.html)
- [Lovart ARR breaks through 30 million US dollars - Zhihu](https://zhuanlan.zhihu.com/p/1960289646727636053)
- [Keling AI's full-year revenue is approximately US$140 million - China Business News](https://www.yicai.com/news/102919501.html)
- [Kuaishou Keling AI’s monthly active users exceeded 12 million - Sina Finance](https://finance.sina.com.cn/stock/t/2026-01-21/doc-inhhzycx8227978.shtml)
- [Meitu’s revenue in 2025 is 3.9 billion - IT Home](https://www.ithome.com/0/933/432.htm)
- [Lumi - Tencent News](https://news.qq.com/rain/a/20241104A04WYE00)
