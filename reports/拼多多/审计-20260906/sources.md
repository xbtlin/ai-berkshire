# PDD研究来源与复核记录

资料截止2026-09-06，行情为2026-09-04正规82.21美元；82.30是盘后。财报默认百万元人民币。报告完成研究与抽样检查，明确分部盈利、其他损失组成、最新现金资本开支和可立即分配母公司现金的缺口。

## 原件及独立来源

- [2025年报SEC原件地址](https://www.sec.gov/Archives/edgar/data/1737806/000110465926050727/pdd-20251231x20f.htm)直接curl遇403；[同一SEC发行人申报镜像](https://cdn.yahoofinance.com/prod/sec-filings/0001737806/000110465926050727/pdd-20251231x20f.htm)已完整下载为 `2025官方镜像.html`，解析 `2025官方.txt`。镜像不算第二来源。年报2025收入431845.713、经营利润93102.131、归母97842.539、普通股稀释EPS16.50（每ADS×4）、股权报酬7936.971。
- [2023年报原件](https://investor.pddholdings.com/static-files/e9586d93-bb1d-4e98-af8a-4e73b62350f2)：web可读取，curl403。2021/22/23收入93949.939/130557.589/247639.205；归母7768.670/31538.062/60026.544，成本31718.093/31462.298/91723.577。没有将失败下载伪装为PDF保留。
- [2026Q2公告与完整半年财务表](https://investor.pddholdings.com/news-releases/news-release-details/pdd-holdings-announces-second-quarter-2026-unaudited-financial/)：Q2收入112358、归母27182、营业27764；H1收入218587、归母39729、营业47330；H125对应199657/45496/41879。现金128918、短投327496、受限77274、全部负债215620；其中商家应付109924、保证金18545。公司不披露单独Temu完整利润表。
- [2025初步年度公告](https://investor.pddholdings.com/news-releases/news-release-details/pdd-holdings-announces-fourth-quarter-2025-and-fiscal-year-2025)：归母99364.469、经营94624.061；审计年报分别少1521.930，管理费用相应增加。不对差异原因作无证据命名，TTM使用审计版本。
- [2025Q3公告](https://investor.pddholdings.com/news-releases/news-release-details/pdd-holdings-announces-third-quarter-2025-unaudited-financial)：收入108276.5、营销53347.6、交易54928.9；Q4收入123912.194、营销60010.1、交易63902.1。Q1由半年减Q2计算。
- [StockAnalysis独立数据库](https://stockanalysis.com/stocks/pdd/financials/)：2021—2025收入93950/130558/247639/393836/431846、归母7769/31538/60027/112435/97843、2025经营利润93102；现金短投456414、经营现金流2025为106939、TTM111895。采用S&P Global/Fiscal.ai标准化数据而不是官网转载。
- [FT财务数据](https://markets.ft.markitdigital.com/data/equities/tearsheet/financials?s=PDD%3ANSQ&subView=IncomeStatement)：审计年度97843和93102与SEC匹配，用于初稿差异查验。
- [新浪科技2024年度报道](https://finance.sina.com.cn/tech/2025-03-20/doc-ineqiark3734433.shtml)：总成本2024为1539.004亿元、2023为917.236亿元；归母2023为600.265亿元。用于成本抽样的第二来源，明确单位换为百万元。
- [Reuters2026Q2](https://www.marketscreener.com/news/temu-owner-pdd-revenue-misses-estimates-profit-falls-on-intense-china-competition-ce7858dbdb8bf323)：收入112.36bn、归母27.2bn人民币，与原件112358/27182容差内。报道调整后EPS不与GAAP估值混用。
- [欧盟Temu罚款原件](https://digital-strategy.ec.europa.eu/en/news/commission-fines-temu-eu200-million-breaching-digital-services-act)、[AP独立报道](https://apnews.com/article/07f53e968da89562e3f032abfa626fa4)：2026年5月DSA风险评估义务罚款€200m。没有证据映射到本季具体费用项目。
- [独立行情](https://www.trading212.com/trading-instruments/invest/PDD.US)、[StockAnalysis正规与盘后](https://stockanalysis.com/stocks/pdd/financials/)、腾讯财经共享原始 `../../六公司研究审计-20260906/market-snapshot.json`：正规82.21、盘后82.30。实际ADS以20-F5693585848/4算，而模型固定稀释14.8亿ADS。
- [新华社9月4日中间价](https://english.news.cn/20260904/790d1ee7b6864f7b96752579a210e783/c.html)：美元人民币6.7787，与SAFE同日中间价对应，不是市场收盘即期汇率。

## 现金、利润与治理限制

TTM归母使用97842.539+39729-45496=92075.539，经营利润93102.131+47330-41879=98553.131。2025全年稀释普通股EPS16.50×4+H126ADS26.90-H125ADS30.69=62.21人民币；与数据库62.26为加权期数拼接微差，不叫直接披露TTM。正常化基数98553.131×80%+8000－1842.5048=85000，税率与利息及缓冲都是假设。

现金SOTP=现金+短投+受限－全部负债－假设营运资金50000，再只做一次20%折价。受限资源与商家义务未双扣；全负债包含非流动债务但其他非流动投资不计，是保守压力口径，不宣称精确可分配金额。PE主模型已包含利息，不额外加现金；SOTP主业剔除全部利息再加净资源，两法不可相加。

2025年报截至2026年3月18日持股：黄铮1409744080、腾讯783468116、合伙安排370772220普通股。没有B类股发行在外，不能沿用早年10倍投票控制权。合伙人提名条款有条件，不能说所有特别任命权均已触发。最新母公司现金汇出能力未全量核验，报告不用全合并现金推断可立即派息。

## 工具和审计

计算入口在 `../../腾讯/审计-20260906/复核计算.py`；本目录保存 `工具原始输出.json/txt`、`估值模型.json`。市场市值、收入/归母/现金交叉、披露与正常化估值、三情景和所有派生财务均经financial_rigor工具计算。源记录明确每项输入是原件、第二源还是模型假设。

`抽样原始输出.txt` 是seed42 extract原输出；`抽样核验.json` 事实样本有两源读取值，情景目标与回报样本以financial_rigor和独立Decimal复算，分类为模型计算，不是外部已证实预测。`审计判决.txt/json`保留原输出。工具的PASS只表示这些抽样核验通过，报告列出的缺口不因PASS而消失。

## 收尾补充

五年经营现金流表的2021—2023原始千元数为28783011/48507860/94162531，见2023年报PDF第98页/现金流表第144页；2024—2025原件现金流与独立数据库取整121929/106939一致。表格全部取整百万元，不用它伪造最新TTM FCF。

最终seed42抽9项：6项历史财务事实双源、3项模型计算独立复算。全部verdict PASS，零警告、零失败，无未核验财务样本。模型样本不是外部事实，完整范围见 `审计范围.json`；分部经济性、最新现金资本支出、母公司可分配资金等缺口仍存在。
