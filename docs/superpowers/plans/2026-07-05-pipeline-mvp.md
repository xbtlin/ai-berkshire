# Pipeline MVP 实施计划：周月低频调度 + 事件分类框架

## Context

### 问题
用户已连续 60+ 天手动跑 `bottleneck-hunter` 每日双扫描（早/午各 1 次，见 `reports/bottleneck-map/daily/`），人肉当 cron 用。`skills/*.md` 是 prompt-driven slash command，不能直接被 cron 调用。需要构建调度框架，让 Claude Code 在 headless 模式下自动跑 skill。

### 用户已决策（3 项）
1. **调度方案**：Windows 任务计划程序 + Claude Code `-p` headless 模式
2. **事件分类**：规则前置 + LLM 兜底（需求 3 暂不实现，本期保留接口）
3. **MVP 范围**：周月低频（`portfolio-review` 周 / `industry-funnel` 月）

### 关键技术验证（已 spike 通过）
Claude Code 支持非交互模式：`claude -p "/skill args" --allowedTools "..." --output-format json > log.json`。

**重要约束**：不用 `--bare`——它会跳过 CLAUDE.md 项目指令（金融 Decimal 约束 / 中文报告风格 / Codex 同步规则），让 skill 行为偏离。

### 期望结果
- 周日晚 20:00 自动跑 `portfolio-review`，更新 `reports/portfolio-latest.md`
- 每月 1 号晚 20:00 自动跑 `industry-funnel`，主题从队列读取、跑完弹出
- 失败有日志可查（`logs/scheduler/*.json`），不静默崩
- 用户可用 `--dry-run` 先看命令再决定要不要真跑

---

## 实施步骤

### Step 1: 调度框架骨架（核心）

新建 `tools/scheduler/__init__.py`（空文件，标记 Python 包）。

新建 `tools/scheduler/runner.py`，核心函数：

```python
def run_skill_headless(
    skill_name: str,
    args: str = "",
    repo_root: Path = REPO_ROOT,
    log_dir: Path = LOG_DIR,
    extra_allowed_tools: list[str] = None,
    dry_run: bool = False,
) -> dict:
    """调 claude -p '/{skill} {args}'，返回 {ok, stdout, exit_code, log_path}。

    - 不加 --bare：保留 CLAUDE.md 项目指令
    - --allowedTools 显式授权（Read/Edit/Bash/WebSearch/WebFetch/mcp__http-tools__*）
    - --output-format json：stdout 是 JSON，含 cost/duration 等元数据
    - log 写到 logs/scheduler/{skill}-{YYYYMMDD-HHMMSS}.json
    - dry_run=True 时只打印命令、不调 claude
    """
```

辅助函数：
- `pop_next_theme(queue_file: Path) -> str | None`：从队列头部取主题，跑完移到 history
- `_build_command(...)`：构造 `claude` 调用参数
- `_write_log(...)`：把 stdout + 元数据写日志

### Step 2: industry-funnel 主题队列

新建 `data/industry_funnel_queue.json`：

```json
{
  "queue": [
    {"theme": "AI算力", "added": "2026-07-05"},
    {"theme": "创新药", "added": "2026-07-05"},
    {"theme": "核电", "added": "2026-07-05"}
  ],
  "history": []
}
```

`pop_next_theme()` 语义：
- 取 `queue[0].theme`，返回字符串
- 调用方跑完后调 `mark_theme_done(theme, report_path)`，把记录移到 `history`
- 队列空时返回 `None`，调用方应跳过并写 warning log

### Step 3: CLI 入口

新建 `tools/scheduler/__main__.py`：

```bash
# 已支持的命令：
python -m tools.scheduler portfolio-review [--dry-run]
python -m tools.scheduler industry-funnel --from-queue [--dry-run]
python -m tools.scheduler news-pulse "拼多多 跌12%" [--dry-run]   # 留接口，不绑定调度任务
python -m tools.scheduler list-queue                              # 查看主题队列
python -m tools.scheduler add-theme "AI算力"                      # 加主题
```

每个子命令调 `run_skill_headless()`，失败时 exit_code != 0 + 写 error log。

### Step 4: PowerShell 安装/卸载脚本

新建 3 个文件：

**`scripts/run-scheduled-task.ps1`**：任务计划程序的实际入口。
- 参数：`-Skill portfolio-review | industry-funnel`
- 切到 `C:\workspace\ai-berkshire`，调 `python -m tools.scheduler {skill}`
- 错误时写 Windows Event Log

**`scripts/install-windows-tasks.ps1`**：注册任务。

| 任务名 | 触发 | 命令 |
|---|---|---|
| `AI-Berkshire-Portfolio-Weekly` | 每周日 20:00 | `powershell -File scripts/run-scheduled-task.ps1 -Skill portfolio-review` |
| `AI-Berkshire-Industry-Monthly` | 每月 1 号 20:00 | `powershell -File scripts/run-scheduled-task.ps1 -Skill industry-funnel` |

用 `Register-ScheduledTask` + `-Action` + `-Trigger`。提供 `-Uninstall` switch 卸载。

**`scripts/uninstall-windows-tasks.ps1`**：调 `Unregister-ScheduledTask` 卸 2 个任务。

### Step 5: logs 目录

新建：
- `logs/scheduler/.gitkeep`
- `logs/scheduler/README.md`（说明 log 文件命名 + 不入 git 的理由）

更新 `.gitignore`（如未包含）：
- `logs/scheduler/*.json`（实际 log 不入 git）
- `!logs/scheduler/.gitkeep`（保留目录占位）

### Step 6: 测试

新建 `tests/scheduler/__init__.py` + `tests/scheduler/test_runner.py`：

测试覆盖（**不真跑 claude**）：
- `test_build_command_基础格式`：`_build_command("news-pulse", "拼多多 跌12%")` 返回正确参数列表
- `test_build_command_包含 allowed_tools`：默认 + extra 都正确合并
- `test_run_skill_headless_dry_run`：`dry_run=True` 时不调 subprocess、只返回命令
- `test_run_skill_headless_失败时写_error_log`（mock subprocess 返回非零）
- `test_pop_next_theme_空队列返回 None`
- `test_pop_next_theme_取头部_保留剩余`
- `test_mark_theme_done_移到 history`

Mock 模式参考现有 `test_stock_recommender.py::test_run_stable_*`（用 monkeypatch 替换 subprocess.run）。

### Step 7: 文档

新建：
- `docs/superpowers/specs/2026-07-05-pipeline-design.md`（设计选型记录，含 3 个方案对比 + 用户决策）
- `docs/superpowers/plans/2026-07-05-pipeline-mvp.md`（本计划副本，便于仓库内追溯）

修改 `CLAUDE.md`：在"## /stock-recommend 推荐系统"后加新章节 `## 调度 Pipeline`，含：
- MVP 范围（2 个任务）
- 安装/卸载命令
- 主题队列管理命令
- 故障排查（看 `logs/scheduler/`）

---

## 关键文件清单

**新建（11 个）**：
- `tools/scheduler/__init__.py`
- `tools/scheduler/__main__.py`
- `tools/scheduler/runner.py`
- `data/industry_funnel_queue.json`
- `scripts/run-scheduled-task.ps1`
- `scripts/install-windows-tasks.ps1`
- `scripts/uninstall-windows-tasks.ps1`
- `logs/scheduler/.gitkeep`
- `logs/scheduler/README.md`
- `tests/scheduler/__init__.py`
- `tests/scheduler/test_runner.py`
- `docs/superpowers/specs/2026-07-05-pipeline-design.md`

**修改（2 个）**：
- `.gitignore`（加 `logs/scheduler/*.json`）
- `CLAUDE.md`（加 `## 调度 Pipeline` 章节）

---

## 复用现有组件

- `tools/fin_ai/__init__.py`（参考 Python 包结构）
- `tools/stock_recommender.py` 的 `_http_get / _qq_code`（如果调度需要拉数据，复用）
- `tests/fin_ai/test_stock_recommender.py::test_run_stable_*`（mock 模式参考）
- 现有 skill 文件不变（`portfolio-review` / `industry-funnel` 都是已就绪的 slash command）

---

## Verification

### 单元测试
```bash
python -m pytest tests/scheduler/ -v
```

### Smoke 测试（不真跑 claude）
```bash
python -m tools.scheduler portfolio-review --dry-run
python -m tools.scheduler industry-funnel --from-queue --dry-run
python -m tools.scheduler list-queue
python -m tools.scheduler add-theme "AI算力"
```

### 真实跑（需本机有 claude CLI + 订阅配额）
```bash
# 先做最小验证（确认 --bare 不加能正常展开 skill）
claude -p "/portfolio-review 我的持仓" \
  --allowedTools "Read,Edit,Bash,WebSearch,WebFetch" \
  --output-format json > /tmp/test-portfolio.json
cat /tmp/test-portfolio.json | python -m json.tool

# 真跑调度入口
python -m tools.scheduler portfolio-review
ls logs/scheduler/
```

### Windows 任务计划程序验证
```powershell
# 安装任务
powershell -ExecutionPolicy Bypass -File scripts/install-windows-tasks.ps1

# 列出已注册任务
schtasks /query /tn "AI-Berkshire-*"

# 立即触发测试
schtasks /run /tn "AI-Berkshire-Portfolio-Weekly"

# 查最近运行结果（含 Last Run Time / Result）
schtasks /query /tn "AI-Berkshire-Portfolio-Weekly" /v

# 卸载
powershell -ExecutionPolicy Bypass -File scripts/uninstall-windows-tasks.ps1
```

---

## 实施时第一步必须验证（关键风险点）

**风险**：spike agent 推荐的 `--bare` 会跳过 CLAUDE.md，但不用 `--bare` 是否会有别的问题（如 hooks 干扰、加载慢）？这影响整个方案。

**实施 Step 1 完成后，立即手动验证**：
```bash
# 在 ai-berkshire 目录下手动跑一次（最小输入）
claude -p "/portfolio-review 我的持仓" \
  --allowedTools "Read,Edit,Bash,WebSearch,WebFetch" \
  --output-format json > /tmp/spike.json

# 检查
cat /tmp/spike.json | python -m json.tool | head -20
ls reports/portfolio-latest.md    # 应被更新
```

**通过标准**：
- exit_code = 0
- reports/portfolio-latest.md 更新时间 = 现在
- spike.json 含 `cost_usd` / `duration_ms` 等元数据

**未通过时的回退方案**（按优先级）：
1. 加 `--append-system-prompt-file <CLAUDE.md 摘要>`：把关键约束摘出来注入
2. 把 CLAUDE.md 的金融 Decimal / 报告风格核心约束复制到 skill.md 顶部（违反 DRY 但可控）
3. 加 `--permission-mode acceptEdits`：减少权限弹窗

---

## 不在本期做（明确排除）

- 日频任务（`news-pulse` 盘前 / `thesis-tracker` 盘后）— 配额压力大，留下一期
- 需求 3 热点驱动（RSS / 巨潮 / 政策文件）— 留下一期，但 `runner.py` 接口预留
- `bottleneck-hunter` 自动化 — 用户当前手动节奏有意（每天 2 次需要人盯信号），自动化需先讨论触发逻辑
- GitHub Actions 备份方案 — 单机版稳定后再考虑
