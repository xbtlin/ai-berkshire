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

- [2025年报](https://www1.hkexnews.hk/listedco/listconews/sehk/2026/0421/2026042100395_c.pdf)：五年收入、利润、毛利；2023使用重述收入6301002千元；2025CFO10865152千元和租赁付款608288千元。
- [中期公告](https://www.hkexnews.hk/listedco/listconews/sehk/2026/0820/2026082000354_c.pdf)：收入17172921、归母5038384、现金12442065千元。仅取得现金流摘要，未取得完整附表。
- [8月股本](https://www1.hkexnews.hk/listedco/listconews/sehk/2026/0901/2026090102631.pdf)：1331779203股。

第二源：

- [StockAnalysis财务](https://stockanalysis.com/quote/hkg/9992/financials/)：历史收入与归母利润、2022/23毛利率57.49%/61.32%。2025收入37120、归母12776百万元。
- [StockAnalysis现金](https://stockanalysis.com/quote/hkg/9992/financials/balance-sheet/)：2025现金13775、最新12442、2022现金685.31百万元。
- [现金流](https://stockanalysis.com/quote/hkg/9992/financials/cash-flow-statement/)：2025CFO10865百万元，简单FCF与本报告租赁后口径不同。
- [财华社](https://www.finet.hk/newscenter/news_content/6a86c2d02308290c11eadd7c)：H1收入171.73亿元、归母50.38亿元、GPM69.7%与地区收入。
- [老虎公告整理](https://www.itiger.com/news/1176616877)：8月总股数1331779203。
- [国信证券历史报告](https://pdf.dfcfw.com/pdf/H3_AP202401051616654746_1.pdf)：2022A现金685百万元，与StockAnalysis685.31交叉。只采用该明确历史现金数，不将其预测和现金流标准化口径搬入报告。

抽样14项：9项事实、2项情景计算、3项模型输入，参数未填写伪fetched。2022现金已两独立数据商/券商交叉，未在本轮下载早期原件，属于原件归档缺口。早期现金流只保留第二源显示精度。当前股数以港交所月报为准；StockAnalysis当前市值和股数较低且差异未完全解释，未静默替换。王宁48.73%为年末被视为权益，简单穿透约46.00%不是完整最终受益披露。
