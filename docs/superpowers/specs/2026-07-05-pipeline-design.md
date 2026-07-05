# Pipeline 设计选型（2026-07-05）

## 背景

`bottleneck-hunter` 已连续 60+ 天手动跑双扫描（早/午各 1 次，见 `reports/bottleneck-map/daily/`），用户人肉当 cron 用。需要把 skills（prompt-driven slash command）纳入自动调度。

3 个核心需求（来源：`memory/todo.md` → 投研 Pipeline）：
1. **定时调度**：盘前 news-pulse / 盘后 thesis-tracker / 周 portfolio-review / 月 industry-funnel
2. **热点驱动**：财经媒体 RSS / 巨潮公告 / 政策文件 → LLM 分类 → 触发对应 skill
3. **股票推荐系统**：MVP 已上线（`/stock-recommend` + `tools/stock_recommender.py`），不在本文档范围

## 用户决策（2026-07-05）

| 决策点 | 选定方案 | 理由 |
|---|---|---|
| 调度方案 | **Windows 任务计划程序 + Claude Code `-p` headless** | 复用现有订阅、原生 Windows、零额外成本 |
| 事件分类 | **规则前置 + LLM 兜底** | 配额可控、可解释、维护成本低 |
| MVP 范围 | **周月低频**（`portfolio-review` + `industry-funnel`） | 单次成本小、易验证、配额压力小 |

## 备选方案对比

### 调度方案（A vs B vs C）

| | A. GitHub Actions | **B. Windows 任务计划** ✅ | C. Python APScheduler |
|---|---|---|---|
| 本机开机依赖 | 无 | **强**（必须开机+登录） | 中（守护进程） |
| 成本 | 按 token 付费 | **零额外**（用订阅） | 零额外 |
| 跨平台 | 是 | Windows only | 是 |
| 复杂度 | 中（YAML + secret 管理） | **低**（schtasks 一键） | 中（需写守护进程） |
| 自动 push | 是 | 否（需 skill 自己 commit） | 否 |
| **判断** | 备选（云端稳定性优） | **MVP 首选** | 不推荐（违背架构） |

**C 不推荐**：把 prompt-driven skill 翻译成 Python 入口违背"skills/*.md 是 canonical workflow 源"原则。

**A 留作下一期**：单机稳定后再考虑云端备份。

### 事件分类（X vs Y vs Z）

| | **X. 规则前置 + LLM 兜底** ✅ | Y. 全 LLM | Z. 向量检索 + LLM |
|---|---|---|---|
| 配额消耗 | **低**（多数走规则） | 高（每条烧配额） | 中 |
| 准确率 | 中（规则覆盖内 95%+） | 高 | 中→高（需积累） |
| 实现复杂度 | **低** | 低 | 高（向量库） |
| 可解释性 | **强**（命中规则可追溯） | 弱 | 中 |
| **判断** | **MVP 首选** | 不可持续（80/天配额） | 过度工程 |

规则示例（待需求 3 实施时落地）：
- "业绩预告|财报|季报|Q[1-4]" → `earnings-review`
- "减持|增持|回购|股权激励|解禁" → `news-pulse`
- "行业政策|规划|补贴|关税|出口管制" → `industry-research`

## 关键技术验证（spike 结论）

Claude Code 支持 headless 模式：

```bash
claude -p "/skill args" --allowedTools "Read,Edit,..." --output-format json > log.json
```

**重要约束**：不用 `--bare`——它会跳过 `CLAUDE.md` 项目指令（金融 Decimal / 中文报告风格 / Codex 同步规则），让 skill 行为偏离。

参考：[Claude Code Headless 文档](https://code.claude.com/docs/en/headless.md)

## MVP 实施范围

| 任务 | 触发 | skill | 输入 |
|---|---|---|---|
| `AI-Berkshire-Portfolio-Weekly` | 每周日 03:00 | `portfolio-review` | "我的持仓"（读 `reports/portfolio-latest.md`） |
| `AI-Berkshire-Industry-Monthly` | 每月 1 号 03:00 | `industry-funnel` | 主题队列（`data/industry_funnel_queue.json`） |

**默认凌晨 3 点**：用户用的是 GLM Coding Plan（5 小时刷新套餐，非按 token 付费），凌晨跑不挤占白天配额。可用 `-RunAt "04:00"` 自定义。

队列管理：`python -m tools.scheduler {list-queue | add-theme "..."}`。

## 不在本期做

- 日频任务（`news-pulse` 盘前 / `thesis-tracker` 盘后）— 配额压力大，留下一期
- 需求 3 热点驱动 — 留下一期，但 `runner.py` 接口已预留
- `bottleneck-hunter` 自动化 — 用户当前手动节奏有意（每天 2 次需要人盯信号）
- GitHub Actions 备份方案 — 单机版稳定后再考虑

## 实施计划

详见 `docs/superpowers/plans/2026-07-05-pipeline-mvp.md`（已审批通过）。
