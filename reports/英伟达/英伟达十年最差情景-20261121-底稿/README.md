# 底稿：英伟达十年最差情景（2026-11-21）

配套报告：[../英伟达十年最差情景-20261121.md](../英伟达十年最差情景-20261121.md)

## 目录

| 文件 | 内容 |
|---|---|
| `verify_model.py` | 全部财务计算、情景公式、概率测算的复算脚本。输出 `arithmetic.json`（284 条记录），使用 `decimal.Decimal` 精度 36 位，不依赖浮点。 |
| `arithmetic.json` | 复算结果。每条记录含名称、表达式、数值、单位、来源。 |
| `prob_base_rate.py` | 历史基准率。抓取 39 家可比公司的 SEC XBRL 年度净利，计算"从利润峰值出发，十年后净利跌到多少"。自包含，首次运行会向 SEC 拉数并缓存到 `xbrl_cache/`。 |
| `base_rate_rows.json` | 上一步生成的逐个观测明细。 |
| `prob_era.py` | 基准率的起点年代分层与行业分层。依赖 `base_rate_rows.json`。 |
| `prob_cond.py` | 条件概率结构。五个环节不是独立事件，模型为 P(环节1) × P(环节2-5 全部到位 \| 环节1 发生)。 |
| `prob_credit.py` | 单年巨亏概率的三层校准：担保的法律触发条件、承租方信用、下游新云的债券定价。 |
| `prob_sens.py` | 最差情景参数敏感性（价值池、份额、净利率单参数变动对 2036 年净利的影响）。 |
| `xbrl_cache/` | SEC EDGAR XBRL companyconcept 的原始 JSON，39 家公司的 NetIncomeLoss 与收入标签。属于一手原件缓存，保留以便离线复算。 |

## 运行顺序

```bash
python3 prob_base_rate.py    # 抓数（已缓存则直接读缓存）+ 计算基准率 → base_rate_rows.json
python3 prob_era.py          # 分层检验
python3 prob_cond.py         # 条件概率结构
python3 prob_sens.py         # 参数敏感性
python3 verify_model.py      # 全部复算 → arithmetic.json
```

## 两处需要说明的口径问题

**一、五个环节不是独立事件。** 早期版本把五个环节的独立概率相乘得到 0.1%，这是建模错误。环节二到五基本上是环节一的下游结果（需求崩塌会同时导致份额流失、定价权丧失、其他收入萎缩、担保被兑现），正确结构见 `prob_cond.py`。

**二、历史基准率只在"谷底仍为正"的观测里统计。** 全样本 74 个观测里有 23 个（31.1%）的谷底是负数，即公司直接转亏。英伟达的最差情景是净利 96 亿美元、仍然为正，把转亏观测算进来会把频率从 5.9% 高估到 35.1%。这个修正在 `prob_base_rate.py` 第一节。

另有一项本可采用但已弃用的证据：按峰值净利率分层看崩溃率。SEC XBRL 的 `us-gaap:Revenues` 对不同公司含义不一致——对 AAPL、GOOGL、META 是公司总收入，对 CRM 是分部口径（CRM FY2016 公开总收入 10014 百万美元，XBRL 给出 6667 百万美元），且与 `RevenueFromContractWithCustomerExcludingAssessedTax` 无交集可交叉校验。理由记录在 `prob_base_rate.py` 第三节。

## 数据来源

- 英伟达财务与担保：[SEC 8-K 2026-11-17](https://www.sec.gov/Archives/edgar/data/1045810/000104581026000088/q3fy27pr.htm)、[SEC 10-K FY2026](https://www.sec.gov/Archives/edgar/data/1045810/000104581026000021/nvda-20260125.htm)
- 同业年度净利：SEC EDGAR XBRL `companyconcept` API，`us-gaap:NetIncomeLoss`
- 同业资本开支：SEC EDGAR XBRL `companyconcept` API，`us-gaap:PaymentsToAcquirePropertyPlantAndEquipment` / `ProductiveAssets`
