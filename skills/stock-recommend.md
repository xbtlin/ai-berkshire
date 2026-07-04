---
description: A 股稳定收益推荐（高股息+低PE+稳定ROE），扫描中证红利+上证50成分股
---

# /stock-recommend — A 股推荐系统

## 使用示例

```
/stock-recommend                    # 默认 stable 模式
/stock-recommend stable --top 5     # 显式指定 top 5
/stock-recommend stable --dry-run   # 仅打印不写文件
/stock-recommend long-term          # MVP 未实现，会提示
```

## 执行步骤

收到本 slash command 后，**直接调底层 CLI**，不要重新实现逻辑：

### 模式 1：stable（稳定收益）

```bash
python tools/stock_recommender.py stable --top 5
```

执行流程（约 5-10 分钟）：
1. 加载中证红利 + 上证 50 成分股（约 100 只）
2. 顺序拉基本面（每只 3 个 HTTP）
3. 4 维硬指标打分（股息率 TTM / PE / ROE 均值 / ROE 稳定性）
4. fin_ai 批量观点层（烧 1 次配额）
5. 输出 Markdown 报告到 `reports/股票推荐/stable-{YYYYMMDD}.md`

### 模式 2 / 3：long-term / short-term

未实现。提示用户：

> 该模式 MVP 未实现，仅 `stable` 可用。请改用 `/investment-research {公司名}`（长期看好）或 `/news-pulse {公司名}`（短期事件驱动）。

## 输出处理

- 报告生成后，向用户展示路径并简要总结 top 推荐
- 如果报告顶部出现 ⚠️ fin_ai 降级 warning，主动告知用户原因（配额/超时）
- 询问是否要推送到 GitHub

## 配额约束

- 单次跑：1 次 fin_ai 调用（缓存命中 0 配额）
- 每日 80 次配额，足够跑数十次

## 相关 skill

- `/quality-screen`：去劣筛选 7 条硬指标（适用于单公司）
- `/investment-checklist`：买入前 6 关 checklist
- `/investment-research {公司}`：长期看好模式
