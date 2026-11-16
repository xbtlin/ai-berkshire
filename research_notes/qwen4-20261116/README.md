# Qwen4 发布日研究底稿

对应报告：[Qwen4 系列深度研究](../../reports/AI产业研究/Qwen4系列研究报告-20261116.md)。资料截止日：2026-11-16，北京时间。

## 文件

- `evidence.json`：人工摘录的 Vals 表格、标准价格算例与 Decimal 计算结果。来源链接和口径以正文来源表为准。
- `build_evidence.py`：重新生成数据文件、计算工具输出和质量—成本散点图，不调用任何模型推理 API。
- `calculation-tool-output.txt`：仓库 `financial_rigor.py calc` 的实际执行记录；同时使用 Decimal 复核，避免展示精度影响结论。
- `audit-extract.txt`：`report_audit.py extract --seed 42` 输出，171 个识别项中抽取 26 个。
- `audit-results.json`：抽样处置与额外关键数据核对记录。
- `audit-verdict.txt`：仓库判定工具的实际输出，51 项有效核对通过。

## 核对范围

随机抽样 26 项中，5 项是来源编号、模型版本或 P95 指标名，被解析器误当成测量值，明确排除；其余 21 项逐项按原始发布者数据或公式核对。两个时间单元原本只提取整分钟，按原始单元格的分秒统一成分钟后检查。另增加 30 项关键规格、价格、任务成绩、精确时长和退步项，合计 51 项有效核对。

数值检查采用公开来源的人工摘录，**不等于独立复现闭源模型测试**。同一评测机构的榜单与模型详情属于同一来源体系；厂商价表与厂商新闻也不是两个独立证明。没有虚构第二来源。

特别检查：正式版与 Preview 的输出上限不同；人民币与国际美元报价分开；Work360 中英文成本口径分开；综合任务成本未随单价同步下降；法律税务有回退；token/s 和在线 P95 未获得可信可比数据；三年情景权重与成本路径是作者假设。

## 复现

在仓库根目录运行（图表需要 matplotlib）：

```bash
python3 research_notes/qwen4-20261116/build_evidence.py
python3 tools/report_audit.py extract --report reports/AI产业研究/Qwen4系列研究报告-20261116.md --seed 42
```

`audit-results.json` 是针对本次发布日来源和报告内容的人工核对记录。更新正文或动态来源后，应重新抽样并重新核实，不能把本次 PASS 当作未来版本的核验。
