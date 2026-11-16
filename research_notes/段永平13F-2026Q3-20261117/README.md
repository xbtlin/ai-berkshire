# H&H 2026Q3 持仓文章：数据与复核记录

研究日期：2026-11-17，北京时间。比较 2026-09-30 与 2026-06-30；不是实时持仓。

成品：[公众号文章](../../reports/段永平/段永平-2026Q3持仓变化-公众号-20261117.md)。

## 原始证据

| 来源 | 文件/链接 | 用途 |
|---|---|---|
| SEC，Q3 | [完整申报](https://www.sec.gov/Archives/edgar/data/1759760/000175976026000008/0001759760-26-000008.txt)；本地 `raw/2026Q3-complete-submission.txt` | 备案号 0001759760-26-000008，16 行，总额 17,190,742,843 美元 |
| SEC，Q2 | [完整申报](https://www.sec.gov/Archives/edgar/data/1759760/000175976026000007/0001759760-26-000007.txt)；本地 `raw/2026Q2-complete-submission.txt` | 备案号 0001759760-26-000007，18 行，总额 19,100,584,155 美元 |
| 13f.info，Q3 | [季度页面](https://13f.info/13f/000175976026000008-h-h-international-investment-llc-q3-2026)；[数据端点](https://13f.info/data/13f/000175976026000008) | 独立托管转录，`raw/q3_13finfo_data.json` |
| 13f.info，Q2 | [季度页面](https://13f.info/13f/000175976026000007-h-h-international-investment-llc-q2-2026)；[数据端点](https://13f.info/data/13f/000175976026000007) | 独立托管转录，`raw/q2_13finfo_data.json` |
| DATAROMA | [H&H 持仓页](https://www.dataroma.com/m/holdings.php?m=HH)；`raw/q3_dataroma.html` | Q3 额外交叉比对，见独立数据核查 |
| 港交所 | [个人权益披露 IS20260805E00004](https://di.hkex.com.hk/di/NSForm1.aspx?fn=IS20260805E00004&lang=ZH)；`raw/hkex-control.html` | 第 20 项控制关系为 99.00%，仅用于核实机构与个人的关系 |
| SEC FAQ | [13F 问答](https://www.sec.gov/rules-regulations/staff-guidance/frequently-asked-questions-about-form-13f) | 第 8、38、39、43 问：季末口径、受管账户、小额省略、卖出期权边界 |

两份 XML 的 `tableValueTotal` 都以**美元**计，不能沿用旧版的千美元单位。各行合计与封面精确相等。两份封面均标注非修订、无保密遗漏；报告期、备案号已核对。截至本次查询，SEC 最新申报列表中未出现这两季的 13F 修订。

第三方页面均来自相同 SEC 申报，属于不同托管方的转录交叉检查，不是三套独立资产审计。34 行股数与 13f.info 完全一致；其市值为千美元截断，逐行少于 SEC 0–999 美元。没有把本仓库旧文章当成第二来源。

网页检索工具读取部分最新 SEC XML 失败，随后用 curl 获取 SEC 完整申报及 XML。SEC FAQ 和最新 submissions 列表经网页工具读取；本地 curl 对这两个端点返回 403，故没有伪造本地缓存。港交所简式链接已通过 curl 获取并核实 H&H 名称、地址、控制人和 99.00%。

## 计算口径

- 主键：CUSIP、证券类别、put/call 属性、股份/本金类型。两季均未出现期权行或重复主键。
- 原有持仓的股数变化率：本季股数减上季股数，再除以上季股数。
- 权重：该行申报市值除以当季封面总市值。每股价格：申报市值除以股数，受美元整数取整影响，文章保留到美分；不是交易价或内在价值。
- 消失/新增的条目在 JSON 算术合并时用零补齐，同时保留 `q2_disclosed`、`q3_disclosed`。**零只代表未列示，不证明真实持仓为零。**文章及 Markdown 对照表使用“未再披露”，不把差额写成真实清仓股数。
- 拼多多、阿里巴巴沿用申报 ADS 单位，不转换为其他市场普通股。
- 不从两季快照计算投资收益、现金余额、真实交易现金流或资金去向；不把持仓改变的动机作为事实。

## 复现

在仓库根目录运行（标准库即可）：

```sh
python3 research_notes/段永平13F-2026Q3-20261117/recompute.py
python3 research_notes/段永平13F-2026Q3-20261117/audit_article.py
```

`recompute.py` 解析已保存的原始证据，输出 `comparison.json`，并实际调用共享 `tools/financial_rigor.py` 完成 72 次精确运算/跨源检查，结果保存在 `financial_rigor.json`。其中 34 次为逐行市值跨源核对，股数另外逐行作整数相等断言。

`audit_article.py` 对正文两个表格全部 56 个可提取数值逐一检查，并核查精简版正文额外提取的 SpaceX 股数，合计 57 项。先保留两个来源的精确值，再按文章显示位数舍入，防止将 0.01% 与 0.0095% 的显示差异误判为经济错误；每个结果都保存未舍入值与显示精度。随后运行共享 `tools/report_audit.py extract`（100%）与 `verdict`。日志、结果和文章 SHA-256 分别保存在 `audit-extract.txt`、`audit-verdict.txt`、`audit-results.json`、`audit-manifest.json`。这覆盖数值表格；正文逻辑和解释另经人工式审读。

图表由 `charts.py` 基于同一 `comparison.json` 生成，使用 matplotlib 和本机中文字体；两张 2000×1520 PNG 已目视核对。脚本中的字体路径可按其他机器的中文字体位置调整。

## 编辑记录

初稿、编辑审读、读者审读和独立数据核查留在本目录，成品以 `reports/` 文件为准。修正内容与最终审阅状态见 `定稿复核.md`。中间材料不作为公众号正文或已发表微信文章归档。
