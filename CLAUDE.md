# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

# AI Berkshire — 项目指令

## 项目概述

基于 Claude Code / Codex 的价值投资研究 Skill 合集。四大师框架：巴菲特、芒格、段永平、李录。
GitHub: xbtlin/ai-berkshire

核心卖点（详见 README.md）：强制给结论不打太极 / 四大师视角对抗 / 结构化反偏见机制 / 金融数据精确计算（Decimal）/ 可复现研究流程 / 多 Agent 并行深度 / 连续两年实盘跑赢全球主要指数 40-50 个百分点。

## 项目结构

```
skills/          — Claude Code slash-command 源文件（canonical workflow 源）
codex-skills/    — Codex skill 包，由 scripts/sync-codex-skills.py 从 skills/*.md 生成
codex-prompts/   — Codex slash prompt 兼容层（可选）
scripts/         — 安装/同步脚本（install-*.sh、sync-*.py）
tools/           — 金融严谨性 + 数据获取工具（Python，跨 Claude/Codex 共用）
reports/         — 投资研究报告输出
assets/          — 图片等静态资源
data/            — 缓存的财务/行情/估值 CSV 与 JSON
docs/            — ROADMAP、外部研究文档
AGENTS.md        — Codex 行为约束（与 CLAUDE.md 平行，互不重复）
ai_CLAUDE.md     — AI 协作记忆文件（用户画像、项目演进、已知问题）
```

**关键事实**：`skills/*.md` 是 workflow 唯一源文件。修改 skills/ 后必须跑 `sync-codex-skills.py` 同步给 Codex，不要手改 codex-skills/。

## 报告目录结构

所有报告按**公司名**建文件夹，公司相关的所有报告放在对应文件夹内：

```
reports/
├── AI产业研究/              — AI产业链全景研究（置顶）
│   ├── AI五层蛋糕-产业全景研究-20260605.md
│   └── AI五层蛋糕-公众号-20260605.md
├── 腾讯/                    — 腾讯所有研究报告
│   ├── 腾讯-research-20260408.md
│   ├── 腾讯-earnings-2025Q4.md
│   ├── 腾讯-management-20260409.md
│   └── 腾讯-thesis.md
├── 拼多多/                  — 拼多多所有研究报告
├── 泡泡玛特/                — 泡泡玛特所有研究报告
├── 核电-industry-20260409.md — 行业报告放根目录
├── AI算力-funnel-20260509.md  — 漏斗筛选报告放根目录
├── AI-轮动判断-20260509.md    — 主题级综合判断报告放根目录
├── portfolio-latest.md       — 组合报告放根目录
└── 多公司对比-checklist-20260408.md — 多公司报告放根目录
```

## 报告命名规范

| Skill | 文件命名格式 | 示例 |
|------|---------|------|
| /investment-team | `{公司名}/` 目录内含4个视角+最终报告 | `reports/拼多多/最终报告.md` |
| /investment-research | `{公司名}-research-{YYYYMMDD}.md` | `reports/腾讯/腾讯-research-20260408.md` |
| /investment-checklist | `{公司名}-checklist-{YYYYMMDD}.md` | `reports/腾讯/腾讯-checklist-20260408.md` |
| /industry-research | `{行业名}-industry-{YYYYMMDD}.md`（根目录） | `reports/核电-industry-20260409.md` |
| /industry-funnel | `{行业名}-funnel-{YYYYMMDD}.md`（根目录） | `reports/AI算力-funnel-20260509.md` |
| /private-company-research | `{公司名}-private-{YYYYMMDD}.md` | `reports/字节跳动/字节跳动-private-20260408.md` |
| /earnings-review | `{公司名}-earnings-{期间}.md` | `reports/腾讯/腾讯-earnings-2025Q4.md` |
| /earnings-team | `{公司名}/` 目录内含4个大师视角+研究底稿+公众号文章+读者评审 | `reports/腾讯/腾讯-earnings-2025Q4.md`（公众号定稿） |
| /thesis-tracker | `{公司名}-thesis.md`（长期维护） | `reports/腾讯/腾讯-thesis.md` |
| /portfolio-review | `portfolio-latest.md`（根目录，持续更新） | `reports/portfolio-latest.md` |
| /management-deep-dive | `{公司名}-management-{YYYYMMDD}.md` | `reports/腾讯/腾讯-management-20260409.md` |

## /investment-team 文件结构

```
reports/{公司名}/
├── README.md                         — 研究框架概览+核心结论
├── 01-商业模式分析-段永平视角.md
├── 02-财务估值分析-巴菲特视角.md
├── 03-行业竞争分析-芒格视角.md
├── 04-风险管理层评估-李录视角.md
└── 最终报告.md                       — Team Lead 综合报告
```

## Skills 全景（19 个，按场景选用）

| 类别 | Skill | 用途 |
|------|-------|------|
| 🔬 深度研究 | `/investment-research` `/investment-team` `/management-deep-dive` `/private-company-research` `/deep-company-series` | 单公司全方位研究；多 Agent 并行最快；管理层/未上市公司/公众号级系列 |
| 📊 财报分析 | `/earnings-review` `/earnings-team` | 一手财报精读；四大师并行 + 公众号发布 |
| 🏭 行业筛选 | `/industry-research` `/industry-funnel` `/quality-screen` `/bottleneck-hunter` `/investment-checklist` | 产业链全景；漏斗精选；去劣筛 7 条硬指标；供应链瓶颈；买入前 6 关 |
| 📈 持仓管理 | `/portfolio-review` `/thesis-tracker` `/news-pulse` `/stock-recommend` | 组合管理；论文追踪；股价异动 10 分钟归因；按偏好推荐 N 支候选股 |
| 🧠 思维工具 | `/dyp-ask` `/financial-data` `/wechat-article` | 段永平问答；财务数据交叉验证规范；公众号文章三 Agent 协作 |

调用示例：`/investment-research 腾讯`、`/industry-funnel AI算力`、`/news-pulse 拼多多 跌12% 一周内`。

## 工具与脚本

### Python 工具（`tools/`）

所有金融计算走 `decimal.Decimal`，**禁用 float**（PE 算错一位小数点 = 投资决策错）。

| 工具 | 用途 |
|------|------|
| `financial_rigor.py` | 市值验算 / 估值验算 / 多源交叉验证 / 三情景估值 / Benford 检测 / 精确计算器 |
| `report_audit.py` | 报告发布前的合规性审计（数据来源、置信度标注） |
| `ashare_data.py` | A 股行情+财务（腾讯行情+东方财富，零外部依赖） |
| `xueqiu_scraper.py` | 雪球数据抓取（含登录态缓存，详见 .gitignore） |
| `morningstar_fair_value.py` | Morningstar 公允价值拉取 |
| `stock_screener.py` | 股票筛选 |
| `momentum_backtest.py` / `momentum_backtest_v2.py` | 动量回测 |
| `fin_ai/` | 金融 AI（gangtise-reason）SSE 问答接口客户端：观点/研报/事件解读。CLI: `python -m tools.fin_ai ask "..."` / Python: `from tools.fin_ai import ask` |

`financial_rigor.py` 子命令（用 `--help` 看完整参数）：

```bash
# 市值手算校验（股价 × 总股本 vs 报告值）
python tools/financial_rigor.py verify-market-cap --price 510 --shares 9.11e9 --reported 4.65e12 --currency HKD

# 估值指标精确计算（PE/PB/ROE/FCF Yield）
python tools/financial_rigor.py verify-valuation --price 510 --eps 23.5 --bvps 120

# 多源交叉验证（同字段 N 个来源对比，超容差告警）
python tools/financial_rigor.py cross-validate --field revenue --values '{"年报": 7518, "Yahoo": 7500}' --unit 亿

# 三情景估值（乐观/中性/悲观）
python tools/financial_rigor.py three-scenario ...

# 任意表达式精确计算（替代 LLM 心算）
python tools/financial_rigor.py calc --expr '510 * 9.11e9'
```

> Windows Git Bash 用 `python`，不是 `python3`（Windows 默认不创建 python3 软链接）。

### 脚本（`scripts/`）

| 脚本 | 用途 |
|------|------|
| `install-claude-commands.sh` | 把 skills/*.md 复制到 `~/.claude/commands/` 全局可用 |
| `install-codex-skills.sh` | 安装 Codex skills 到 `~/.codex/skills` |
| `install-codex-prompts.sh` | 安装 Codex slash prompts |
| `sync-codex-skills.py` | **改 skills/ 后必跑**：从 skills/*.md 重新生成 codex-skills/*/SKILL.md |
| `sync-codex-prompts.py` | 同步 Codex slash prompts 兼容层 |

校验是否同步（不写文件）：`python scripts/sync-codex-skills.py --check`

## Codex 兼容性

本项目同时支持 Claude Code 和 Codex，**canonical workflow 源在 `skills/*.md`**：

- 改 `skills/*.md` → 跑 `sync-codex-skills.py` → 提交 codex-skills/ 的生成结果
- 不要手改 `codex-skills/*/SKILL.md`，下次 sync 会覆盖
- Codex 专属行为写在 `AGENTS.md`，Claude Code 专属行为写在本文件，**互不重复**
- 仅 Codex 用的 hand-written 包需在 codex-skills/ 中标注，且不要建同名 skills/*.md

## 投研分析核心原则（最高优先级）

- **客观、客观、客观**——所有投研分析必须基于事实和数据，严禁主观臆断
- 严格区分"事实"与"观点"：事实用数据支撑，观点必须明确标注为"观点"或"推测"
- **不预设立场**：不预设看多或看空，先摆数据、再推逻辑、最后得结论。结论必须从数据中自然推出
- 禁止使用"我认为"、"我觉得"、"显然"等主观表述，改用"数据显示"、"证据表明"、"根据XX来源"
- **呈现正反两面**：每个核心判断都必须附带反面论据（"但另一方面..."），让读者自己权衡
- 对不确定的事情诚实说"不确定"或"数据不足"，不要用推测填充确定性
- **金融 AI（gangtise-reason）数据源优先**：当 fin_ai 有数据时，**以 fin_ai 为准确源**（B 级以下公司经验证比 WebSearch/东方财富更准——小商品城样本 fin_ai ROE 17.53% vs WebSearch 12.96%/4.15%）。但 PE/PB/ROE 等估值指标仍走 `tools/financial_rigor.py` 精确计算（Decimal，禁用 float）。fin_ai 提供输入数据，financial_rigor 做精确计算，**两者协同而非替代**。fin_ai 无数据/超时/无配额时 fallback 到 WebSearch + 年报。
- 所有skill（investment-team、investment-research、earnings-review等）在执行时都必须遵守以上原则

## 报告语言与风格

- 所有报告使用**中文**
- 风格：直接、犀利、不说废话
- 数据必须标注来源，关键数据至少2个来源交叉验证
- 估计值必须注明"估计"
- 评分使用★符号（★1-5），不含半星
- 穿插巴菲特/芒格/段永平/李录的语录点评

## GitHub 操作

- 本地克隆路径：`~/ai-berkshire/`
- 远程仓库：`https://github.com/xbtlin/ai-berkshire.git`
- 推送前先 `git pull --rebase origin main`（远程经常有新提交）
- commit message 用中文，描述清楚改了什么
- 不要推送中间过程文件（如 data_collection.md），只推最终报告

## 常用命令

```bash
# 推送报告到GitHub
cd ~/ai-berkshire
git add reports/xxx.md
git commit -m "添加xxx报告"
git pull --rebase origin main
git push origin main
```

## /stock-recommend 推荐系统

A 股稳定收益推荐：扫描中证红利 + 上证 50 成分股（约 100 只），按 4 维硬指标打分（股息率 TTM / PE / ROE 均值 / ROE 稳定性）+ fin_ai 观点层。

```bash
python tools/stock_recommender.py stable --top 5
```

- 单文件 CLI：`tools/stock_recommender.py`（约 400 行，纯 stdlib）
- 输出：`reports/股票推荐/stable-{YYYYMMDD}.md`
- 配额：单次跑烧 1 次 fin_ai（80/天足够）
- 设计 spec：`docs/superpowers/specs/2026-07-04-stock-recommender-design.md`

## 调度 Pipeline

Windows 任务计划程序 + Claude Code headless 模式定时触发 skill。MVP 含 2 个任务：

| 任务 | 触发 | skill | 输入 |
|------|------|-------|------|
| `AI-Berkshire-Portfolio-Weekly` | 每周日 20:00 | `portfolio-review` | "我的持仓"（读 `reports/portfolio-latest.md`） |
| `AI-Berkshire-Industry-Monthly` | 每月 1 号 20:00 | `industry-funnel` | 主题队列（`data/industry_funnel_queue.json`） |

### 用法

```bash
# 安装任务（注册到 Windows 任务计划程序）
powershell -ExecutionPolicy Bypass -File scripts/install-windows-tasks.ps1

# 卸载
powershell -ExecutionPolicy Bypass -File scripts/uninstall-windows-tasks.ps1

# 立即触发测试
schtasks /run /tn "AI-Berkshire-Portfolio-Weekly"

# 手动跑（不依赖任务计划程序）
python -m tools.scheduler portfolio-review
python -m tools.scheduler industry-funnel --from-queue
python -m tools.scheduler portfolio-review --dry-run    # 只打印命令、不调 claude

# 主题队列管理
python -m tools.scheduler list-queue
python -m tools.scheduler add-theme "AI算力"
```

### 故障排查

- **运行日志**：`logs/scheduler/{skill}-{YYYYMMDD-HHMMSS}.json`（每个任务一次 JSON，含 stdout/stderr/exit_code/duration）
- **任务计划程序结果**：`schtasks /query /tn "AI-Berkshire-*" /v` 看 Last Run Time / Result
- **关键约束**：调度命令**不用 `--bare`**——会跳过 CLAUDE.md 项目指令（金融 Decimal / 中文报告风格 / Codex 同步）

### 模块

- `tools/scheduler/runner.py`：核心，调 `claude -p` headless + 写 log
- `tools/scheduler/__main__.py`：CLI 入口
- `scripts/run-scheduled-task.ps1`：任务计划程序实际入口
- 设计 spec：`docs/superpowers/specs/2026-07-05-pipeline-design.md`
- 实施计划：`docs/superpowers/plans/2026-07-05-pipeline-mvp.md`

### 不在本期做

- 日频任务（`news-pulse` 盘前 / `thesis-tracker` 盘后）— 配额压力大
- 热点驱动（RSS / 巨潮 / 政策文件 → LLM 分类）— 留下一期，`runner.py` 接口已预留

## 注意事项

- 市值必须手算校验：股价 × 总股本，与报告市值对比
- 货币单位要明确（港币/人民币/美元），防止混淆
- PE/ROE 等指标用 `tools/financial_rigor.py` 精确计算，禁用 LLM 心算
- 报告发布前用 `tools/report_audit.py` 做合规审计（数据来源、置信度标注）
- 关键数据至少 2 个独立来源交叉验证，误差 >1% 告警
- 改 skills/ 后必须跑 `scripts/sync-codex-skills.py` 同步 Codex（用 `--check` 仅校验不写）
- Windows Git Bash 下用 `python` 不用 `python3`；所有路径用正斜杠
- 报告写完后主动询问是否推送到 GitHub
- 本项目仅供学习研究，不构成投资建议
