# 股票推荐系统设计（MVP：稳定收益模式）

**日期**：2026-07-04
**作者**：smile + Claude（brainstorming session）
**状态**：spec（待用户审核 → writing-plans）

---

## 1. 目标

构建一个 A 股「稳定收益」股票推荐工具，扫描中证红利 + 上证 50 成分股（约 100 只），按 4 维硬指标打分 + fin_ai 观点层，输出 Top 5 推荐 + Top 5 备选的 Markdown 报告。

**非目标**：

- 不做「长期看好」「短期收益」两种模式（后续 MVP）
- 不做港股 / 美股
- 不做定时调度（属于需求 2）
- 不做全市场扫描

---

## 2. 用户场景

```
用户：/stock-recommend stable
Claude：好的，正在扫描中证红利 + 上证 50 成分股（100 只）...
        1. 加载成分股 ✅
        2. 拉基本面（约 5 分钟）⏳
        3. 4 维打分 ✅
        4. fin_ai 观点层 ✅
        5. 生成报告 ✅
        报告已生成：reports/股票推荐/stable-20260704.md
```

报告内容包含：总结 / Top 5 推荐 / Top 5 备选 / 风险提示 / 方法论 / 数据来源。

---

## 3. 文件结构

```
新增（3 个）：
  tools/stock_recommender.py            # 单文件 CLI（约 300 行）
  skills/stock-recommend.md             # skill prompt（约 50 行）
  data/index_constituents.json          # 中证红利 + 上证 50 成分股基线（仓库内）

新增目录（1 个）：
  reports/股票推荐/
    └── stable-{YYYYMMDD}.md

新增测试（1 个）：
  tests/fin_ai/test_stock_recommender.py  # 10 个 unit case
```

---

## 4. CLI 接口

```bash
# 默认稳定收益模式
python tools/stock_recommender.py stable

# 自定义阈值
python tools/stock_recommender.py stable \
    --top 5 \
    --min-dividend 4 \
    --max-pe 15 \
    --min-roe 12

# 仅打印不写文件
python tools/stock_recommender.py stable --dry-run

# 强制覆盖当日报告
python tools/stock_recommender.py stable --force

# 显示帮助
python tools/stock_recommender.py --help
```

### Skill 触发示例

```
/stock-recommend                    # 默认 stable
/stock-recommend stable --top 5     # 显式指定
/stock-recommend long-term          # 提示「MVP 未实现」
/stock-recommend short-term         # 提示「MVP 未实现」
```

---

## 5. 评分维度与阈值（4 维硬指标，4 分制）

| 维度 | 阈值 | 数据源 | 分数 |
|------|------|--------|------|
| **股息率（TTM）** | > 4% | 东财 F10 分红 API（近 12 个月每股股息合计）÷ 当前股价 | 1 分 |
| **PE（动）** | < 15 | 腾讯行情 quote | 1 分 |
| **ROE 近 3 年均值** | > 12% | 东财 financials API（最近 3 份年报 ROEJQ 字段的算术平均） | 1 分 |
| **ROE 稳定性** | 近 3 年 ROE 标准差 < 5 个百分点（pp） | 东财 financials API（同样 3 份年报 ROEJQ 的 stddev） | 1 分 |

**股息率计算示例**：某股近 12 个月内派息 2 次（中期 + 年度），每股股息分别为 0.20 / 0.30 元，当前股价 10 元 → TTM 股息率 = (0.20 + 0.30) / 10 = 5.0% → 该维 1 分。

### 推荐阈值

| 总分 | 推荐度 | 用途 |
|------|--------|------|
| **4 分** | 强烈推荐 | Top 5 推荐 |
| **3 分** | 备选 | Top 5 备选 |
| **< 3 分** | 剔除 | 不出现在报告里 |

### 排序规则

同分时按**股息率降序**（稳定收益策略核心 = 股息率）。

### 银行业友好性

按上述阈值跑典型银行股：
- 招行（ROE ~16%, 股息率 ~5%, PE ~7）→ 4 分 ✅
- 工行（ROE ~12%, 股息率 ~6%, PE ~5）→ 3-4 分 ✅
- 不会一刀切错杀银行业

---

## 6. 数据流（5 步）

```
[1] 加载成分股（100 只）
    └─ data/index_constituents.json（首次仓库内基线）
       └─ 过期时从指数公司/东财更新
            ↓
[2] 顺序拉基本面（每只 3 个 HTTP，约 5 分钟）
    ├─ 腾讯行情 quote    → PE / PB / 市值 / 当前价
    ├─ 东财 financials  → 近 5 年 ROE
    └─ 东财 F10 分红    → 近 3 年分红方案 → 算股息率
            ↓
[3] 4 维打分 → 过滤 < 3 分
    └─ 4 分组按股息率排序 → Top 5
       3 分组按股息率排序 → Top 5
            ↓
[4] fin_ai 观点层（1 次调用，批量问 Top 10）
    └─ Prompt:
       "以下是 10 只候选股 [列表]，请：
        1. 按股息可持续性排序
        2. 标注每只股的 1 个核心风险
        3. 推荐 top 3 + 警告 bottom 2"
            ↓
[5] 拼 Markdown 报告 → reports/股票推荐/stable-{YYYYMMDD}.md
    └─ 章节: 总结 / Top 5 推荐 / Top 5 备选 /
             风险提示 / 方法论 / 数据来源
```

---

## 7. 模块内部分层（单文件内）

```python
# tools/stock_recommender.py 内部函数
load_index_constituents()       # 步骤 1
fetch_quote(code)               # 步骤 2-A：腾讯行情
fetch_financials(code)          # 步骤 2-B：东财财务
fetch_dividends(code)           # 步骤 2-C：东财 F10 分红（新增逻辑）
calc_dividend_yield(...)        # 算股息率（净利润 ÷ 当前价）
score_stable(fund)              # 步骤 3：4 维打分
ask_fin_ai_opinion(top_10)      # 步骤 4：批量问 fin_ai
generate_report(results, path)  # 步骤 5：拼 Markdown
main()                          # argparse 入口
```

---

## 8. 错误处理（降级策略）

| 故障点 | 降级方案 |
|--------|---------|
| 成分股 API 拉不到 | 用本地 `data/index_constituents.json` 基线 |
| 单只股基本面拉失败 | 跳过该股，标记 `data_quality: partial` |
| 腾讯行情返回空（停牌/退市） | 跳过 + warn |
| 东财财务数据为空（次新股） | ROE 维度 0 分 + warn |
| 东财分红数据为空（IPO < 1 年） | 股息率维度 0 分 + warn |
| **fin_ai 配额耗尽**（80/天用完） | 跳过观点层，仅硬指标 + 报告顶部 warning |
| **fin_ai 超时**（> 30s） | 同上降级 |
| HTTP 全局失败（断网） | 退出码 1 + 提示重试 |

---

## 9. 工程决策

1. **HTTP 走 MCP http-tools**（按 hard-rules #1）：不用 curl，不用 Python `requests`。
2. **HTTP 顺序执行**：300 个请求顺序约 5 分钟可接受；并发会触发东财反爬 + Windows Git Bash 进程管理不稳。
3. **基本面缓存 1 天**：`data/fundamentals_stable_{date}.json`，同一天重复跑不重新拉。
4. **报告覆盖**：同一天重复跑会覆盖当日报告（`--force` 强制、`--dry-run` 仅打印）。
5. **不污染 `ashare_data.py`**：股息率逻辑在 `stock_recommender.py` 内部实现，避免改动现有工具。
6. **不抽象多模式框架**：YAGNI。`long-term` / `short-term` 模式未来直接复制粘贴改阈值。

---

## 10. 测试与验收

### Unit test（10 个 case）

文件：`tests/fin_ai/test_stock_recommender.py`

```
test_score_stable_满分()        # 4 项全过 → 4 分（虚构样本：股息 5%, PE 10, ROE 均 14%, stddev 1pp）
test_score_stable_股息率不达标() # 股息率 3% → 该维 0 分
test_score_stable_PE过高()      # PE 30 → 该维 0 分
test_score_stable_ROE低()       # ROE 8%（近 3 年均值）→ 该维 0 分
test_score_stable_ROE波动大()   # ROE 序列 [8%, 15%, 22%]，stddev 7pp → 稳定性 0 分
test_score_stable_银行股()      # 招行样本（股息 5.2%, PE 7, ROE 16%, stddev 0.8pp）→ 4 分
test_score_stable_消费股()      # 茅台样本（股息 1.0%, PE 30, ROE 30%, stddev 1.2pp）→ 股息 0 + PE 0 + ROE 1 + 稳定 1 = 2 分（被剔除）
test_sort_by_dividend()         # 同分按股息率降序
test_filter_below_threshold()   # < 3 分被剔除
test_format_report()            # Markdown 模板渲染正确（含数据来源、生成时间、配置参数）
```

### Smoke test（手动）

```bash
python tools/stock_recommender.py stable --dry-run
# 验证：能跑完、无 traceback、生成 reports/股票推荐/stable-{date}.md
```

### 验收标准

| # | 标准 | 验证方式 |
|---|------|----------|
| 1 | `python tools/stock_recommender.py stable` 退出码 0 | 手动跑 |
| 2 | `reports/股票推荐/stable-{date}.md` 文件生成 | 检查文件 |
| 3 | 报告含 Top 5 推荐 + Top 5 备选 + 风险提示 + 方法论 | 看报告内容 |
| 4 | fin_ai 配额耗尽时报告顶部出现 warning | 改小 limit 模拟 |
| 5 | Unit test 10/10 通过 | pytest |
| 6 | skill `/stock-recommend` 能触发并生成同样报告 | 手动调 skill |

### 不做的事（明确排除）

- ❌ Mock 外部 HTTP（外部 API 不稳就降级，不 mock）
- ❌ 性能测试
- ❌ 多市场测试
- ❌ 自动化 CI

---

## 11. 配额预算

| 调用点 | 次数 | 备注 |
|--------|------|------|
| 步骤 4：fin_ai 批量观点层 | 1 次 / 跑 | 缓存命中 0 配额 |
| 每日跑 1 次 | 1 次 / 天 | 80 配额足够 |
| 每日跑 5 次 | 5 次 / 天 | 仍充足 |

---

## 12. 后续演进（不在 MVP 内）

| 模式 | 增量工作 | 触发时机 |
|------|----------|----------|
| 长期看好 | +护城河维度（依赖 fin_ai）+ 趋势筛选 | 用户主动要求 |
| 短期收益 | 复用 stock_screener.py + news-pulse | 用户主动要求 |
| 定时调度 | CronCreate / 外部 cron | 需求 2 单独立项 |
| 港股 / 美股 | 新增数据源适配 | 用户主动要求 |

---

## 13. 风险与已知问题

| 风险 | 缓解 |
|------|------|
| 东财 F10 分红 API 反爬 | 顺序请求 + User-Agent 伪装 + 5 分钟节流 |
| 中证红利成分股变动（每年 6 月调整） | 手动更新基线（每年 7 月） |
| fin_ai 返回文本非结构化，解析难 | 用 LLM 二次结构化（在 prompt 里要求 JSON 输出） |
| Windows Git Bash 路径问题 | 用 http-tools 不用 curl，规避 |

---

## 14. 验收清单

- [ ] `tools/stock_recommender.py` 实现完整
- [ ] `skills/stock-recommend.md` 实现完整
- [ ] `data/index_constituents.json` 包含中证红利 + 上证 50 基线
- [ ] `tests/fin_ai/test_stock_recommender.py` 10 个 case 全绿
- [ ] 跑通一次完整流程，生成 `reports/股票推荐/stable-{date}.md`
- [ ] fin_ai 配额耗尽场景验证（warning 出现）
- [ ] skill `/stock-recommend` 触发验证
- [ ] 文档：在 CLAUDE.md 工具表新增条目
- [ ] 不破坏现有 18 skill
