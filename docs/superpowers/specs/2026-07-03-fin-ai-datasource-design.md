# 金融 AI 数据源接入设计

| 字段 | 值 |
|------|-----|
| 撰写日期 | 2026-07-03 |
| 作者 | smile |
| 状态 | 待 writing-plans |
| 接口来源 | gangtise-reason（OpenAI 兼容 SSE 问答接口） |

---

## 1. 背景与目标

### 1.1 背景

现有 `tools/` 下 7 个工具（ashare_data、xueqiu_scraper、morningstar_fair_value 等）负责**公开事实数据**（股价、财报、估值），全部走直接 HTTP 抓取，无流式接口、无统一抽象层。

新接入的金融 AI 接口（gangtise-reason，OpenAI 兼容 SSE 流式问答）提供**现有 tools 无法覆盖的能力**：研报观点、事件解读、行业景气判断、宏观解读、多轮对话深入查询。

### 1.2 目标

把金融 AI 接入项目作为**观点/解读层数据源**，明确与现有"事实/数字层"的边界：

| 层 | 职责 | 来源 | 验证方式 |
|----|------|------|---------|
| 事实层 | 股价、财报、估值、市值 | 现有 tools（ashare/xueqiu/morningstar）| `financial_rigor.py` 多源验算 |
| 观点层 | 研报、解读、判断、归因 | **新增：金融 AI** | 标注来源，不参与程序化验算 |

### 1.3 范围

**In scope**

- Python 包 `tools/fin_ai/`（client + cache + quota + cli + config）
- CLI 入口：`python -m tools.fin_ai ask|quota|history|clear-cache`
- Python 库 API：`ask()` / `ask_multi_turn()` / `quota()`
- 文件 hash 缓存（TTL 分级：默认 24h，事件类 1h）
- 配额保护（80/天/用户硬约束）
- 多轮 REPL 对话模式
- 4 个 skill 的可选模块集成（investment-research / earnings-review / industry-research / investment-team）
- 单元测试 + 集成测试（mock SSE）+ 手工 e2e checklist

**Out of scope**

- MCP server 化（项目当前无 MCP 基础设施）
- 自动降级到现有 tools（观点类数据无法被数字工具替代）
- 服务端对话列表/详情查询（`POST /openai/conversations` 等）—— 用本地缓存替代，避免烧配额
- 消息投票、归档、心跳等管理类接口
- 容器预热（`pre-acquire`）—— YAGNI，先观察首问延迟再决定是否启用

---

## 2. 总体架构

### 2.1 包结构

```
ai-berkshire/
├── tools/
│   └── fin_ai/                       # 新增 Python 包
│       ├── __init__.py               # 暴露 ask / ask_multi_turn / quota
│       ├── client.py                 # HTTP + SSE 客户端（核心，约 150 行）
│       ├── cache.py                  # 文件 hash 缓存（约 80 行）
│       ├── quota.py                  # 配额预检 + 显示（约 50 行）
│       ├── cli.py                    # CLI 入口（argparse 子命令，约 100 行）
│       └── config.py                 # 凭证加载（约 30 行）
├── tests/
│   └── fin_ai/
│       ├── test_cache.py
│       ├── test_config.py
│       ├── test_quota.py
│       ├── test_client.py
│       └── e2e_checklist.md
├── data/
│   └── fin_ai_cache/                 # 缓存目录（gitignore）
│       └── <sha256>.json
├── .env                              # 凭证（gitignore）
├── .env.example                      # 占位模板（提交到仓库）
├── .gitignore                        # 新增 2 条
├── requirements.txt                  # 新增 httpx>=0.27
└── skills/
    ├── investment-research.md        # 末尾新增可选模块
    ├── earnings-review.md            # 末尾新增可选模块
    ├── industry-research.md          # 末尾新增可选模块
    └── investment-team.md            # 末尾新增可选模块
```

### 2.2 模块职责

| 模块 | 职责 | 依赖 |
|------|------|------|
| `config.py` | 从 `.env` / 环境变量读凭证，校验完整性 | 无 |
| `client.py` | 封装 `/openai/chat`，处理 SSE 增量拼接、断线重连、错误码 | `config` |
| `cache.py` | 文件 hash → JSON 查/写/清；TTL 过期判断 | 无 |
| `quota.py` | 调 `GET /openai/chat/limit`，返回剩余次数；调用前预检 | `client` |
| `cli.py` | argparse 子命令路由（ask / quota / history / clear-cache） | 全部 |
| `__init__.py` | 对外暴露 `ask()`、`ask_multi_turn()`、`quota()` | 全部 |

### 2.3 与现有部分的关系

- **不动** `tools/` 下其他 7 个工具——继续负责事实层数据
- **不强制嵌入** skill 主流程——以"可选模块"形式附加，由用户决定是否启用
- **新增** `.gitignore` 两条：`.env` 和 `data/fin_ai_cache/`
- **新增** `requirements.txt` 一行：`httpx>=0.27`

---

## 3. 关键模块详述

### 3.1 `config.py`

```python
@dataclass
class Config:
    base_url: str           # http://192.168.1.91:31176
    uid: str
    tenant_id: str
    product_code: str
    client_category: str
    auth_token: str
    model: str              # gangtise-reason

    @classmethod
    def load(cls) -> "Config":
        """优先环境变量，其次 .env 文件；缺凭证 raise ConfigError"""

    def headers(self) -> dict[str, str]:
        return {
            "uid": self.uid,
            "tenantid": self.tenant_id,
            "productcode": self.product_code,
            "clientcategory": self.client_category,
            "Authorization": f"Bearer {self.auth_token}",
            "Content-Type": "application/json",
        }
```

### 3.2 `client.py`

**对外暴露**

```python
class FinAIClient:
    def __init__(self, config: Config): ...

    def chat(
        self,
        query: str,
        conversation_sid: str | None = None,
        on_delta: Callable[[str], None] | None = None,
        timeout: int = 120,
    ) -> ChatResult:
        """返回完整响应 + usage + session_id + message_id"""

    def pre_acquire(self) -> None:
        """调 /chat/pre-acquire 预热容器（YAGNI，暂不调用）"""

@dataclass
class ChatResult:
    content: str          # 完整拼接文本
    session_id: int       # openai_message.id，用于断线重连
    conversation_sid: str # 会话标识
    usage: dict           # {input_tokens, output_tokens, total_tokens}
    raw_events: list      # 原始 SSE 事件（调试用）
```

**SSE 解析逻辑**（核心，约 50 行）

```python
for line in response.iter_lines():
    if line.startswith("event:"):
        current_event = line[6:].strip()
    elif line.startswith("data:"):
        payload = line[5:].strip()
        if payload == "[STOP]":
            break
        data = json.loads(payload)
        if "errorCode" in data:
            raise FinAIError(data["errorCode"], data.get("errorMsg"))
        if current_event == "response.output_text.delta":
            if on_delta: on_delta(data["delta"])
            buffer.append(data["delta"])
        elif current_event == "response.completed":
            usage = data["response"]["usage"]
```

**断线重连**：网络中断时用上次的 `session_id` 调用 `reconnectToMessageId`，重试 1 次（`reconnect_expired` / `reconnect_completed` / `reconnect_forbidden` 不重试）。

### 3.3 `cache.py`

```python
def cache_key(query: str, model: str, conversation_sid_prefix: str = "") -> str:
    """SHA256(query + model + sid_prefix)"""

def get(key: str, ttl_hours: int) -> dict | None:
    """命中且未过期返回 {content, usage, ts, query}，否则 None"""

def put(key: str, data: dict) -> None:
    """原子写（先写 .tmp 再 rename）"""
```

**缓存文件结构** `data/fin_ai_cache/<sha256>.json`

```json
{
  "query": "茅台研报观点",
  "model": "gangtise-reason",
  "content": "完整响应文本...",
  "usage": {"input_tokens": 13311, "output_tokens": 40, "total_tokens": 13351},
  "ts": "2026-07-03T10:30:00+08:00",
  "session_id": 173,
  "conversation_sid": "a1b2c3..."
}
```

**多轮对话 key**：包含 `sid + ":turn:" + N`，避免不同轮次混淆。

### 3.4 `quota.py`

```python
def pre_check(client: FinAIClient) -> QuotaStatus:
    """调 GET /openai/chat/limit"""

@dataclass
class QuotaStatus:
    exceeded: bool
    used: int
    limit: int
    remaining: int

    def should_warn(self) -> bool:
        return self.remaining < 3 and not self.exceeded
```

### 3.5 `cli.py`

**子命令**

```bash
# 单次查询
python -m tools.fin_ai ask "茅台研报观点"
python -m tools.fin_ai ask "..." --ttl-hours 1
python -m tools.fin_ai ask "..." --no-cache
python -m tools.fin_ai ask "..." --refresh

# 多轮 REPL
python -m tools.fin_ai ask --multi "长城军工"
# >> 第1轮问题
# >> 第2轮问题（上下文延续）
# >> /quit

# 配额查询
python -m tools.fin_ai quota

# 历史记录（仅本地缓存，不消耗配额）
python -m tools.fin_ai history [--limit 20]

# 清缓存
python -m tools.fin_ai clear-cache [--all | --query "茅台"]
```

**输出格式**

```
[FIN_AI] querying: 茅台研报观点
[FIN_AI] quota: remaining 75/80
─────────────────────────────────────
（金融 AI 流式输出内容，实时打印）
─────────────────────────────────────
[FIN_AI] done in 12.3s · tokens: 40 out / 13311 in · [CACHED: no, SID: 173]
```

### 3.6 `__init__.py` — Python 库 API

```python
from tools.fin_ai import ask, ask_multi_turn, quota

# 单次
result = ask("茅台研报观点")
print(result.content)

# 强制刷新
result = ask("茅台研报观点", ttl_hours=1, refresh=True)

# 流式回调
def printer(chunk): print(chunk, end="", flush=True)
result = ask("...", on_delta=printer)

# 多轮（context manager）
with ask_multi_turn("长城军工") as session:
    r1 = session.ask("2025 年报怎么看？")
    r2 = session.ask("和北方导航比谁更好？")  # 上下文延续

# 配额
status = quota()
print(f"剩余 {status.remaining}/{status.limit}")
```

---

## 4. 数据流

### 4.1 单次调用主流程

```
CLI ask / Python ask()
        │
        ▼
1. config.load()                ← 读 .env
   缺凭证 → exit 2
        │
        ▼
2. quota.pre_check()            ← GET /openai/chat/limit
   exceeded=true → exit 3
   remaining<3 → 打印警告
        │
        ▼
3. cache.get(key, ttl)          ← 查本地缓存
   命中且未过期 → 直接返回（不烧配额，标 [CACHE HIT]）
        │
        ▼
4. client.chat_stream()         ← POST /openai/chat (SSE)
   - 实时打印 chunk 到 stdout
   - 累积拼接
   - 收到 [STOP] 结束
        │
   SSE errorCode → 退出（见错误处理表）
        │
        ▼
5. cache.put()                  ← 写入缓存（仅成功响应）
        │
        ▼
6. CLI 退出 0
   打印 [CACHED/REFRESHED] + usage + quota left
```

### 4.2 多轮 REPL 流程

```
python -m tools.fin_ai ask --multi "长城军工"
  ↓
进入交互式 REPL：
  >> 这家公司 2025 年报怎么看？           # 第 1 轮
  >> 它和北方导航比谁更好？               # 第 2 轮
  >> /quit

实现：
- 第 1 轮生成 conversationSid（uuid4），存 ~/.fin_ai_session.json
- 后续轮次复用 conversationSid
- 每轮独立缓存（key 包含 query + 轮次序号）
- /quit 清理 session，保留缓存
```

### 4.3 缓存命中决策

| 调用方式 | TTL 处理 |
|---------|---------|
| 默认 | 24h |
| `--ttl-hours 1` / `ask(ttl_hours=1)` | 覆盖 |
| `--no-cache` | 跳过查缓存，**仍写缓存**让下次受益 |
| `--refresh` | 强制重问，覆盖旧缓存文件 |

### 4.4 配额三层保护

80 次/天是硬约束：

1. **预检**：每次 `ask` 前查 `remaining`；`< 3` 警告；`exceeded` 拒绝
2. **缓存命中不计数**：命中即不发起 `/chat`
3. **失败不计费**：SSE 报错时不写缓存（避免错误响应被复用）

---

## 5. 错误处理与降级

### 5.1 错误码处理表

| 错误源 | 错误码 / 类型 | 处理策略 | exit code |
|-------|--------------|---------|-----------|
| SSE errorCode | `daily_limit_exceeded` | 拒绝，提示明天再试 | 4 |
| SSE errorCode | `reconnect_expired` | 不重试，提示会话已结束 | 6 |
| SSE errorCode | `reconnect_completed` | 不重试，提示会话已结束 | 6 |
| SSE errorCode | `reconnect_forbidden` | 不重试，提示归属不匹配 | 7 |
| SSE errorCode | `error`（通用）| 打印 `errorMsg` | 5 |
| HTTP 状态 | 401 / 403 | 提示 token 过期，检查 `.env` | 8 |
| HTTP 状态 | 404 | 提示 base_url 检查 | 9 |
| HTTP 状态 | 5xx | 重试 1 次（间隔 2s），失败提示服务不可用 | 10 |
| 网络 | `ConnectError` / `Timeout` | 重试 1 次（间隔 2s），失败提示网络 | 11 |
| 网络 | 流中断（已收 chunk）| 用 `session_id` 断线重连 1 次 | 12 |
| 配额预检 | `exceeded=true` | 拒绝调用，提示 `quota` 命令 | 3 |
| 配额预检 | `remaining < 3` | 打印警告，仍允许调用 | 0 |
| 配额预检 | 接口自身失败 | 降级放行（文档明确"容错返回 used=0"）| 0 |
| 配置 | `.env` 缺凭证 | 提示哪些字段缺失，附 `.env.example` 路径 | 2 |

### 5.2 重试策略

| 场景 | 重试次数 | 间隔 |
|------|---------|------|
| 5xx / ConnectError / Timeout | 1 次 | 2s |
| 流中断（已收 chunk） | 1 次（断线重连）| 0s |

其他错误**不重试**——避免在 80 次/天配额下烧得不明不白。每次重试打印 `[RETRY] reason`。

### 5.3 不做自动降级

按设计目标——金融 AI 是观点层，与事实层职责不同——金融 AI 不可用 ≠ 自动调 ashare_data。错误信息只做**建议性提示**：

```
[FIN_AI ERROR] daily_limit_exceeded
当日配额已耗尽（80/80）。明天 00:00 重置。

💡 提示：
- 查看历史问答：python -m tools.fin_ai history
- 查股价/财报：python tools/ashare_data.py 600519
```

### 5.4 缓存写入边界

| 场景 | 是否写缓存 |
|------|-----------|
| 正常成功响应 | 写 |
| SSE 报错（任何 errorCode）| 不写 |
| 用户 Ctrl+C 中断 | 不写 |
| 断线重连成功 | 写（拼接后的完整内容）|
| 流中断且重连失败 | 不写 |

### 5.5 SSE 解析鲁棒性

- 收到未知 `event:` 类型 → 跳过不报错（向前兼容）
- `data:` JSON 解析失败 → 跳过该 chunk，warning 到 stderr
- 流式过程中连接断开（非正常 `[STOP]`）→ 触发断线重连判断

---

## 6. 测试方案

### 6.1 测试金字塔

| 层级 | 范围 | 工具 | 占比 |
|------|------|------|------|
| 单元 | `cache.py` `config.py` `quota.py` 纯逻辑 | `pytest` + 不发请求 | 60% |
| 集成 | `client.py` SSE 解析 + 错误码 | `pytest` + `httpx.MockTransport` | 30% |
| 端到端 | 真实调一次接口 | 手动 checklist | 10% |

### 6.2 单元测试

**`tests/fin_ai/test_cache.py`**
- `test_cache_hit_within_ttl` — 24h 内命中
- `test_cache_miss_after_ttl` — 过期返回 None
- `test_cache_key_includes_model` — 不同 model 不混淆
- `test_cache_key_multi_turn` — 多轮 sid 区分
- `test_atomic_write` — 写入中断不留半文件

**`tests/fin_ai/test_config.py`**
- `test_load_from_env` — 环境变量优先
- `test_load_from_dotenv` — `.env` 文件解析
- `test_missing_credential_raises` — 缺字段抛 `ConfigError`
- `test_headers_format` — Authorization 带 `Bearer ` 前缀

**`tests/fin_ai/test_quota.py`**
- `test_should_warn_at_3` — remaining=2 触发警告
- `test_no_warn_at_5` — remaining=5 不警告

### 6.3 集成测试（mock SSE，不发真实请求）

**`tests/fin_ai/test_client.py`**
- `test_normal_stream` — 正常 SSE，断言拼接内容正确
- `test_delta_concatenation` — 多个 delta 拼接成完整文本
- `test_stop_marker` — `data: [STOP]` 后正常结束
- `test_daily_limit_exceeded` — SSE 返回错误码 → raise
- `test_reconnect_expired` — 不重试场景
- `test_network_error_retry` — 首次 ConnectError，重试成功
- `test_stream_interrupt_reconnect` — 流中断 → session_id 重连
- `test_unknown_event_skipped` — 未知 event 不报错

### 6.4 端到端验收（手动）

维护 `tests/fin_ai/e2e_checklist.md`：

```
□ 配置 .env 后跑：python -m tools.fin_ai quota       → 显示 75/80 类似
□ 单次查询：python -m tools.fin_ai ask "茅台研报观点" → 流式打印 + 元数据 footer
□ 缓存命中：再次跑相同命令 → [CACHE HIT] 不烧配额
□ 多轮 REPL：python -m tools.fin_ai ask --multi "长城军工" → 3 轮对话上下文延续
□ 强制刷新：--refresh → 重新调用，覆盖缓存
□ TTL 覆盖：--ttl-hours 1 → 1h 后再查验证失效
□ 配额耗尽模拟：把 daily_limit 改小 → 触发拒绝
□ 错误凭证：清空 FIN_AI_AUTH_TOKEN → exit 2 + 提示
□ Python 库：from tools.fin_ai import ask; print(ask("...").content)
□ skill 集成：跑 /investment-research 测试公司 → 报告含 [FIN_AI] 观点段
```

### 6.5 准入准出

**准入**（开发完成）
- 单元 + 集成测试全绿
- `e2e_checklist.md` 至少跑通 8/10

**准出**（合入主分支）
- `python tools/financial_rigor.py --help` 仍正常（无回归）
- `python tools/report_audit.py` 在测试报告上仍能跑通
- `.gitignore` 含 `.env` 和 `data/fin_ai_cache/`
- `requirements.txt` 含 `httpx>=0.27`

---

## 7. Skill 集成（可选模块）

### 7.1 集成位置

在 4 个 skill 文件末尾追加可选模块，**不修改原有流程**：

| Skill 文件 | 模块标题 |
|-----------|---------|
| `skills/investment-research.md` | 「可选步骤：金融 AI 观点补充」|
| `skills/earnings-review.md` | 「可选步骤：金融 AI 观点补充」|
| `skills/industry-research.md` | 「可选步骤：金融 AI 观点补充」|
| `skills/investment-team.md` | 「可选步骤：金融 AI 观点补充」|

### 7.2 模块内容模板（统一格式）

```markdown
### 可选步骤：金融 AI 观点补充（消耗配额，默认关闭）

如果你希望报告里包含金融 AI（gangtise-reason）的实时观点补充，
在数据收集阶段调用：

\```bash
# 单次：拿最新观点/事件解读
python -m tools.fin_ai ask "{公司名} 最新市场观点和研报解读" --ttl-hours 1

# 多轮：深入对话（4-5 轮覆盖业务/竞争/估值/风险）
python -m tools.fin_ai ask --multi "{公司名}"
\```

将返回内容嵌入报告「§X.X 金融 AI 观点补充」段落，明确标注：
- 来源：金融 AI（gangtise-reason），{日期}
- 类型：第三方观点，非事实数据
- 与报告其他模块的关系：补充参考，不替代程序化验算

⚠️ 不强制使用。配额 80/天 是硬约束，长公司研究请优先用缓存命中。
```

### 7.3 跑完 skill 后必跑 Codex 同步

按项目规则：改 `skills/*.md` 后**必须**执行：

```bash
python scripts/sync-codex-skills.py        # 同步
python scripts/sync-codex-skills.py --check # 校验
```

---

## 8. 风险与权衡

| 风险 | 缓解 |
|------|------|
| 80 次/天配额烧光 | 三层保护（预检 + 缓存 + 失败不计费）+ `quota` 命令可视化 |
| 服务端变更 SSE 格式 | 未知 event 跳过不报错；集成测试 mock 多种异常流 |
| token 泄露 | `.env` 加入 `.gitignore`；`.env.example` 仅占位 |
| skill 集成引发 Codex 同步问题 | 准入要求跑 `sync-codex-skills.py --check` |
| httpx 引入依赖 | 项目无 lock 文件，影响可控；SSE 流式比 requests 可靠 |
| 多轮对话配额失控 | REPL 每轮前显示 `quota remaining`；用户随时 `/quit` |

---

## 9. 未决事项

| 项 | 处理时机 |
|----|---------|
| 容器预热（pre-acquire）是否启用 | 观察 first-call 延迟后决定，YAGNI 默认不启用 |
| 服务端对话列表查询（conversations）| 当前用本地缓存 history 替代；如未来需要跨设备同步再考虑 |
| 配额阈值是否调宽（< 3 → < 10） | 实跑一周后根据实际消耗调整 |
| 多轮对话 session 持久化 | 当前会话内有效；如需跨会话延续，扩展 `~/.fin_ai_session.json` |

---

## 10. 实施顺序（给 writing-plans 的输入）

1. 创建包骨架 + `.env.example` + `.gitignore` + `requirements.txt`
2. 实现 `config.py` + 单元测试
3. 实现 `cache.py` + 单元测试
4. 实现 `client.py` + 集成测试（mock SSE）
5. 实现 `quota.py` + 单元测试
6. 实现 `cli.py`，串起全流程
7. 实现 `__init__.py`，Python 库 API
8. 端到端 checklist 验收（10 项至少通 8 项）
9. 在 4 个 skill 末尾追加可选模块 + 跑 sync-codex-skills
10. 更新 `CLAUDE.md` 工具表（新增一行 `fin_ai`）+ 提交
