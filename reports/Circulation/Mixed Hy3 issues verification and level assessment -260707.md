# Tencent Hunyuan Hy3 release verification and real level assessment

**Date**: 2026-07-07 (the day after the official version is released)
**Research method**: Multi-channel parallel network search → Grab primary sources → Verify each statement one by one with three votes (2/3 will be eliminated if refuted). A total of more than 20 statements were verified, and 4 statements failed to pass verification and were eliminated.

---

## 1. Summary of conclusions

1. **The news is true**. "Tencent Hunyuan Hy3 released: Agent capabilities and product experience jump" is the original title of Xinhuanet's report on July 6, 2026. The official version of Hy3 was released on the same day, and the preview version was open sourced on April 23. The official version of the model card has been launched by Hugging Face official tencent organization, licensed by Apache 2.0, and is open for download.
2. **However, all the quantitative basis for "jump" comes from Tencent's internal evaluation** and is not endorsed by a third party. The hallucination rate is halved, the multi-round dialogue problem rate is halved, and the blind test is better than GLM5.1 and other core data. The judges are Tencent internal employees and the scenes are Tencent's own products.
3. **Real level positioning**: It is positioned at the back of the first echelon of domestic open source, with outstanding cost performance in the same size (activation 21B), and coding and mathematical abilities are its strengths; there is a clear gap with the international closed source frontiers (Claude, GPT, Gemini). The only available third-party independent review (Artificial Analysis, for the April preview version) gave it a "significantly above average, but not top" position: 22nd out of 93 comparable models.
4. **The official version of the results (SWE-bench Verified 78 points) currently relies entirely on Tencent’s self-report**. It has only been released for one day, and there has not been any third-party retest.

---

## 2. Publish fact verification (confidence: high)

| Matters | Verification results |
|---|---|
| Release time | Official version 2026-07-06; Preview version 2026-04-23 Open source |
| Source | Original report by Xinhuanet, cross-checked by Securities Times, Tencent News, Titanium Media and other media on the same day |
| Open source status | Both preview and official versions are online Hugging Face / GitHub / ModelScope / GitCode, Apache 2.0 |
| The relationship between the official version and the preview version | The official model card says that the official version is based on the preview version, collecting feedback from more than 50 products and expanding the training scale |

The release path is clear: preview version at the end of April → official version on July 6. There is no problem of "fried rice" or false release.

## 3. Model specifications (open source weights can be directly verified, confidence level: high)

- Mixed Expertise (MoE) architecture that integrates fast and slow thinking
- Total parameters 295B, activation parameters 21B, including 3.8B multi-word prediction layer parameters
- 192 experts, 8 per activation, 80 layers transformer
- Maximum 256K context
- The preview version has the same structure as the official version

**Points**: The activation parameters are only 21B, which belongs to the "big general parameters, small activation" route and has low reasoning cost. According to the official statement, "2-5 times the parameter scale of the flagship model", the selling point is essentially **cost-effectiveness** rather than absolute capabilities.

## 4. Official self-reported results and claims (all based on manufacturer caliber)

### Benchmark test (official version, self-reported)

| Benchmark | Official version | Preview version (April) |
|---|---|---|
| SWE-bench Verified | 78 | 74.4 |
| GPQA Diamond | 90.4 | 87.2 |
| SWE-bench Pro | 57.9 | — |
| HLE (Human Final Examination) | 53.2 | — |
| Terminal-Bench 2.0 | — | 54.4 |

There is a real improvement from the preview version to the official version (74.4 → 78), but some official Agent benchmarks only provide picture comparisons and do not provide numerical tables.

### Agent capability claim (self-reported, not reproduced externally)

- Can stably support complex Agent workflows up to **495 steps** (numbers come from Tencent’s own product environment)
- Inference efficiency increased by 40% compared with the previous generation
- Internal product measurement: CodeBuddy/WorkBuddy first word delay dropped by 54%, end-to-end response dropped by 47%
- Real scene hallucination rate 12.5% → 5.4%, multi-turn dialogue problem rate 17.4% → 7.9%
- Internal blind test of 270 experts: Hy3 scored an average of 2.67/4, which is better than GLM5.1’s 2.51/4 (the judges are Tencent employees)

**Another 4 product implementation indicators (WorkBuddy success rate 72% → 90%, Yuanbao hallucination rate reduced by 50%, etc.) failed to pass the confrontation verification, and this report will not be accepted. **

## 5. Horizontal comparison: domestic and international positioning

### Compared with domestic open source competing products (official base comparison table, self-reported)

| Baseline | Hy3 Preview Base | Kimi-K2 Base | DeepSeek-V3 Base | GLM-4.5 Base |
|---|---|---|---|---|
| LiveCodeBench-v6 | **34.86** | 30.86 | 29.31 | 27.43 |
| MATH | **76.28** | 71.20 | 59.37 | 61.00 |
| MMLU | 87.42 (last of the four) | **88.24** | 87.68 | 87.73 |

Coding and math are in the lead, general knowledge is at the bottom. Note: The official statement states that MMLU is "slightly lower than Kimi and DeepSeek", and the actual GLM-4.5 is also higher than it - the official has a slight embellishment tendency, and this report has been corrected.

### Third-party independent review (only covers preview version)

- **Artificial Analysis Intelligence Index: 34 points, 22nd out of 93 comparable models** (group average of 25 points). Officially characterized as "significantly above average", its tweet also said that the Hy3 preview version "lags behind recent open source peers."
- Third-party aggregated SWE-bench Verified comparison: Hy3 preview 74.4, lower than Claude Opus 4.6 (80.8), GLM-5 (77.8), Kimi-K2.5 (76.8). If the official version's self-reported score of 78 is true, it can tie the GLM-5 and still be about 3 points behind Claude - but this number needs to be retested.

### Comparison with international closed source frontiers (major gaps)

Tencent's official press release (Chinese and English versions) **does not make any direct comparison** with GPT, Claude, and Gemini, but only compares it with its previous generation Hy2. This in itself is a signal: if the comparison results are favorable, manufacturers usually will not remain silent.

## 6. Evidence gaps and reservations

1. **Timeliness**: The official version is released for only one day. All official version results are self-reported. Third-party evaluation only covers the April preview version.
2. **Related interests**: All core data such as hallucination rate, blind test, and 495-step workflow come from within Tencent, and the 270 blind test judges are Tencent employees.
3. **Lack of word-of-mouth in the community**: Developer actual testing and real feedback from the forum did not obtain any evidence that passed the three-vote verification. This report cannot evaluate the actual use experience.
4. **Questions to be observed**: Can the 78 points of the official version be reproduced by Artificial Analysis / LMArena? Can the 495-step workflow be reproduced outside of Tencent products? Whether the inference speed and tool call stability after local deployment are consistent with official data.

## 7. Overall judgment

- **News Authenticity**: True, official primary sources are complete, and open source is sincere (Apache 2.0, full weight).
- **"Leap" Statement**: Compared with its own predecessor Hy2, it is established; compared with the industry, it is exaggerated - all based on internal data.
- **Domestic Positioning**: Behind the first echelon of open source. Code/mathematics is a strong point, and general knowledge is a shortcoming; the preview version's benchmark lags behind GLM-5 and Kimi-K2.5, and the official version's self-reported numbers are tied with GLM-5 but need to be verified.
- **International positioning**: There is a clear gap with the closed source frontier (the preview version of SWE-bench is about 6 points behind Claude Opus 4.6), and the official avoids direct comparison.
- **The real highlight**: 21B activation parameters achieve this result, and the inference cost advantage is obvious, which is suitable for the embedded implementation of Tencent's own massive products - this is consistent with the narrative direction of productization indicators such as "495-step workflow" and "first word delay reduced by 54%". **Hy3’s strategic significance lies in reducing costs and increasing efficiency to support Tencent’s product matrix, rather than impacting the top spot in terms of capabilities. **

---

### Main sources

- Original text of Xinhuanet report: news.cn/tech/20260706/d611426ecba54475b2dd94920e4e3557
- Tencent official press release (Chinese/English): tencent.com/zh-cn/articles/2202320
- Hugging Face official model card: huggingface.co/tencent/Hy3, huggingface.co/tencent/Hy3-preview
- GitHub official repository: github.com/Tencent-Hunyuan/Hy3-preview
- Third-party evaluation: artificialanalysis.ai/models/hy3 (verified online on 2026-07-07)
