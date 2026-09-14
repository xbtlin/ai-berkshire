# 研究审计说明（2026-09-06）

本目录保存原件、复算与随机抽检。报告是研究情景，不是收益承诺。原件PDF与pdftotext文本按文件同名对应。所有取得日期为2026-09-06；价格时点为2026-09-04收盘。汇率是官方中间价，非收盘成交汇率。

- `financial-rigor.txt`：市值、双源收入/归母利润/现金、股本、估值和情景计算。
- `模型结果.json`：完整表达式与工具输出数值；`comparison_summary.json`：用Decimal独立复算三情景退出价和逐年股息。
- `基础模型脚本.py`、`补充模型脚本.py`：从仓库根目录运行后者，可复算两家公司（会更新两家本日期审计计算文件）。calc原工具先评估表达式，重要每股估值另以Decimal独立实现复核，未将浮点输出包装为无限精度。
- `audit-extract.txt`：实际运行report_audit extract，seed42；`audit-results.json`只含可观测事实或可复算数学；`audit-assumptions.json`记录被抽中的预测输入，未伪造fetched字段。
- `audit-verdict.txt`：工具对11项事实/计算判PASS、零差异警告。此PASS只表示样本数值误差合格，不是事实全覆盖、所有第二源质量一致、未来假设已证实或监管意义的审计。未利用工具对空值跳过仍PASS的行为来掩盖缺口。
- `抽检脚本.py`保存真实读数和来源URL、数学独立实现；不会从报告数值自动填入核验数。模型输入单独核对定义，不假装是外部事实。
- 六公司共用行情与同行源见`../../六公司研究审计-20260906/market-snapshot.json`、`tencent-quotes.txt`、`peer-reference.md`和对应工具日志。

## 来源与口径

原件：

- [2025年报](https://www1.hkexnews.hk/listedco/listconews/sehk/2026/0422/2026042202118.pdf)：2022—2025收入毛利、IFRS与调整利润，2024—2025现金流、股东经济及投票结构。
- [招股书](https://www1.hkexnews.hk/listedco/listconews/sehk/2025/1231/2025123100025.pdf)：2022—2024现金流与资本开支；正文早期FCF为CFO减设备开支计算，不是官方名为FCF的指标。
- [中期公告](https://www1.hkexnews.hk/listedco/listconews/sehk/2026/0826/2026082600680.pdf)：最新收入116.573、净亏损357.997、现金等价物930.905百万美元。完整H1现金流量表未取得。
- [8月股本月报](https://www1.hkexnews.hk/listedco/listconews/sehk/2026/0903/2026090301230.pdf)：349235308股，A/B分开。已发行总股数不是流通股数。
- [7月融资完成](https://www1.hkexnews.hk/listedco/listconews/sehk/2026/0716/2026071601147.pdf)：配售及债券净融资。
- [关联交易](https://www1.hkexnews.hk/listedco/listconews/sehk/2026/0826/2026082601949.pdf)：云服务额度、融资用途与阿里权益。年度上限不是实际成本。

第二源：

- [StockAnalysis财务](https://stockanalysis.com/quote/hkg/0100/financials/)：2025收入79.04、IFRS净亏损1872百万美元；2023毛利-0.85、2023/24亏损-269.25/-465.24；年度CFO及简单FCF。S&P Global数据为独立转录，不是独立审计。
- [StockAnalysis资产负债](https://stockanalysis.com/quote/hkg/0100/financials/balance-sheet/)：2025现金507.62、最新930.91、2023现金206.3百万美元；股本349.24百万。
- [Reuters独立报道](https://www.investing.com/news/stock-market-news/chinas-minimax-sees-revenue-nearly-quadruple-in-first-half-as-ai-demand-surges-4876820)：最新收入116.6、亏损358百万美元，业务拆分。
- [SCMP](https://www.scmp.com/tech/big-tech/article/3365341/minimax-revenue-surges-283-remains-behind-pace-meet-forecast-amid-crowded-ai-race)：H1毛利率17.9%。
- [智通业绩会转述](https://www.webull.com/news/15472214899246080)：8月ARR8亿美元；ARR是当时运行率，不是已实现年度收入。

抽样16项：10项历史/最新事实，1项情景毛利计算，5项模型输入。2022调整亏损12.15百万美元第二源仅找到[富途社区转述](https://q.futunn.com/en/feed/115769089130500)，可信度低于Reuters/专业数据商，标记来源质量缺口；不因此否定已取得年报原件，也不称完整高质量双源覆盖。创始人融资后持股/投票比例是保持旧持股数量的参考计算，未获得截至9月的最终受益链重建。H1完整现金流缺口限制资金消耗判断。
