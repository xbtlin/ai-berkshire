# 证据与审计说明

资料截止2026-09-24。报告的三个层次必须分开：历史事实、研究假设、由假设计算的结果。财务核对没有也不能证明2036预测正确。

## 实际执行

- 使用investment-team的四个并行角色完成商业、财务、行业、风险研究；主报告由组长整合。风险角色在报告写成后再次读取主文与model.py，未发现必须修订的口径/算术问题。
- `financial-rigor.txt`：12项跨来源核对、官方股数市值核算、估值和三情景终值、关键公式核算。模型另用Decimal实现，消除工具calc浮点尾差。
- `report-audit-extract.txt`：原报告提取156个数据点、随机种子42、15%抽样得到24项。
- `audit-results.json`及`audit-verdict.txt`：24项匹配，其中5项历史事实、11项公式重算、8项假设一致性。后三类中的公式和假设检查不属于外部事实验证；不能将24/24解释为24项预测已获外部证明。
- 5项历史样本里，2024营收及IFRS归母有公司原文和Stockanalysis两来源；2026H1归母、Q2精确non-IFRS经营利润、剔预付FCF只有本轮取得的发行人精确口径，独立第二来源不足。已保留缺口，没有用同一公司不同网址冒充独立来源。
- `decimal-valuation.json`：同日股价、股本及参考汇率的Decimal复算。

## 复现

在项目根目录执行：

```bash
python3 reports/腾讯/腾讯-AI利润研究-20260924/model.py
python3 tools/report_audit.py extract --report reports/腾讯/腾讯-AI利润研究-20260924/腾讯-investment-team-AI利润与竞争格局.md --seed 42
python3 reports/腾讯/腾讯-AI利润研究-20260924/evidence/validation.py
```

validation.py中的历史取值是本次联网读取后登记的证据，不会在复现时自动重新联网；复现只能重算，更新财报需要重新取数。

## 来源定位和交叉核对

| 信息 | 主来源 | 第二来源 / 限制 |
|---|---|---|
| 2023—2025营收、IFRS归母 | 腾讯2023/2025全年业绩原文及比较列 | Stockanalysis年度表，一致 |
| 2025 non-IFRS归母 | 腾讯2025业绩原文 | 36氪2026-03-18报道，一致 |
| 2024 non-IFRS归母 | 腾讯2025原文比较列 | 本轮未取得独立二源；不能因历史已广为引用而自动标双源 |
| 2026Q2收入、IFRS归母、确认资本开支 | 腾讯Q2原文 | Reuters，四舍五入误差低于1% |
| Q2 non-IFRS归母、实际FCF | 腾讯Q2原文 | MarketWatch，四舍五入误差低于1% |
| H1归母 | 港交所H1业绩公告页2 | Q1+Q2可重算，但同一发行人，并非独立验证 |
| H1现金流及SBC | 腾讯完整版中报、2025/2026利润调节表 | 无独立同口径全覆盖，参考而非双源认证 |
| 9月24日股价438.40港元 | Stockanalysis历史表 | Investing历史表，一致；未采用曾出现的过时搜索摘要437.80 |
| 当日股数9,095,133,109 | 腾讯翌日披露报表第一页 | 平台约90亿股相差1.046%，原始披露优先 |
| 每港元0.8559人民币 | Investing港元人民币历史表 | ExchangeRates UK同日参考值；时间截点未必相同 |

主要原始网址：

- [2025业绩原文](https://static.www.tencent.com/uploads/2026/03/18/e6a646796d0d869acc76271c9ee1a6a5.pdf)
- [2023业绩原文](https://static.www.tencent.com/uploads/2024/03/20/ebbe5a148484d3a0911109cdc82d1430.pdf)
- [2026Q2业绩原文](https://www.tencent.com/wp-content/uploads/2026/08/Tencent-Announces-2026-Second-Quarter-Results.pdf)
- [港交所中期业绩公告](https://www1.hkexnews.hk/listedco/listconews/sehk/2026/0812/2026081200296.pdf)
- [腾讯完整中报](https://www.tencent.com/wp-content/uploads/2026/08/E700_IR.pdf)：浏览解析超时，下载及pdftotext成功。Q2及中期公告已另行打开；中报未伪装成浏览工具成功解析。
- [当日股份披露](https://static.www.tencent.com/website-2026-upload/e_Next-Day-Disclosure-Return_20260924-9bc5db.pdf)：网页解析空，直接下载并提取文字核得股本。未把Q2加权股数当作9月期末股数。
- [Stockanalysis损益](https://stockanalysis.com/quote/hkg/0700/financials/)、[现金流](https://stockanalysis.com/quote/hkg/0700/financials/cash-flow-statement/)、[统计](https://stockanalysis.com/quote/hkg/0700/statistics/)
- [Reuters Q2报道](https://www.reuters.com/business/retail-consumer/chinas-tencent-posts-11-second-quarter-revenue-rise-profit-misses-estimates-2026-08-12/)
- [MarketWatch Q2报道](https://www.marketwatch.com/story/another-ai-lab-is-burning-through-cash-as-tencent-earnings-rise-1251b4c6)
- [36氪2025年度结果](https://www.36kr.com/p/3728291911613317)
- [Stockanalysis行情](https://stockanalysis.com/quote/hkg/0700/history/)、[Investing行情](https://www.investing.com/equities/tencent-holdings-hk-historical-data)
- [Investing汇率](https://www.investing.com/currencies/hkd-cny-historical-data)、[ExchangeRates UK汇率](https://www.exchangerates.org.uk/HKD-CNY-spot-exchange-rates-history-2026.html)

## 未被工具绿色标识解决的问题

1. `cross-validate`以中位数为分母；项目规范以主来源为分母。本报告股本差异按官方主来源计算为1.046%，尽管前者可能判一致，仍标差异。
2. 公司FCF与平台FCF相差18.06%，确认资本开支与付款相差10.46%；属于口径问题，没有把两者平均，也未强行塞入“通过”事实样本。
3. 9月法定股数与平台经济股数差异可能涉及奖励计划持股、回购、更新时点，不保证全部由四舍五入导致；官方股数市值相对平台相差约1.20%。
4. 股权薪酬：2025 non-IFRS归母调节加回347.11亿；2026H1为149.49亿。300亿年度经济成本假设参照H1年化量级，不是可忽略股权薪酬。2036金额仍是情景假设。
5. Aastocks基本财务页及Macrotrends未能取得可用数据；Aastocks报价缓存为8月26日，不能充当9月24日价。改用公司原文、Stockanalysis及独立新闻报道，并保留覆盖缺口。
6. 2036三情景终值工具固定股数、汇率及PE，未加入回购或分红，也没有给出折现内在价值；不要把其终值年化价格回报视为完整股东总回报。

## 研究假设的证据边界

新AI亏损、业务自然增速、AI带来的额外收入、贡献率、2036分部收入/利润率、税后归母转化及经济成本扣减均由研究者设定。公司尚未披露足以逐项估计AI净贡献的分部账目。模型目的是使观点可复算、可检验，非给不可观测的反事实贴上精确事实标签。
