# 金融 AI 数据源接入 实施计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 在 `tools/fin_ai/` 下实现一个 Python 包，封装 gangtise-reason 的 OpenAI 兼容 SSE 问答接口，作为观点/解读层数据源，配套 CLI 和 Python 库 API，并在 4 个 skill 末尾追加可选模块。

**Architecture:** 分层 Python 包（config / cache / client / quota / cli），事实层数据继续走现有 tools，观点层数据走金融 AI，二者不交叉降级。80 次/天配额用「预检 + 文件 hash 缓存 + 失败不计费」三层保护。

**Tech Stack:** Python >= 3.8、httpx（SSE 流式）、pytest、dataclasses、argparse。

**Spec 来源:** `docs/superpowers/specs/2026-07-03-fin-ai-datasource-design.md`

**Windows 提示:** 所有命令在 Git Bash 下运行；Python 用 `python`，不用 `python3`；测试用 `python -m pytest`，不用 `pytest` 直接调（避免 PATH 问题）。

---

## 文件结构总览

| 文件 | 操作 | 责任 |
|------|------|------|
| `tools/fin_ai/__init__.py` | 创建 | 暴露 `ask` / `ask_multi_turn` / `quota` |
| `tools/fin_ai/config.py` | 创建 | 从 `.env` / 环境变量读凭证 |
| `tools/fin_ai/cache.py` | 创建 | 文件 hash 缓存 |
| `tools/fin_ai/client.py` | 创建 | HTTP + SSE 客户端 |
| `tools/fin_ai/quota.py` | 创建 | 配额预检 |
| `tools/fin_ai/cli.py` | 创建 | argparse CLI 入口 |
| `tests/fin_ai/__init__.py` | 创建 | 测试包标记（空） |
| `tests/fin_ai/test_config.py` | 创建 | config 单元测试 |
| `tests/fin_ai/test_cache.py` | 创建 | cache 单元测试 |
| `tests/fin_ai/test_client.py` | 创建 | client 集成测试（mock SSE） |
| `tests/fin_ai/test_quota.py` | 创建 | quota 单元测试 |
| `tests/fin_ai/e2e_checklist.md` | 创建 | 手动验收清单 |
| `.env.example` | 创建 | 凭证占位模板 |
| `.gitignore` | 修改 | 加 `.env` 和 `data/fin_ai_cache/` |
| `requirements.txt` | 创建 | `httpx>=0.27` |
| `skills/investment-research.md` | 修改 | 末尾追加可选模块 |
| `skills/earnings-review.md` | 修改 | 末尾追加可选模块 |
| `skills/industry-research.md` | 修改 | 末尾追加可选模块 |
| `skills/investment-team.md` | 修改 | 末尾追加可选模块 |
| `CLAUDE.md` | 修改 | Python 工具表新增 `fin_ai` 一行 |

---

## Task 1: 项目骨架与配置文件

**Files:**
- Create: `tools/fin_ai/__init__.py`（占位，Task 6 才填实质内容）
- Create: `tests/fin_ai/__init__.py`（空文件）
- Create: `.env.example`
- Create: `requirements.txt`
- Modify: `.gitignore`

- [ ] **Step 1: 创建包骨架**

```bash
mkdir -p tools/fin_ai tests/fin_ai data/fin_ai_cache
```

- [ ] **Step 2: 写 `tools/fin_ai/__init__.py` 占位**

文件 `tools/fin_ai/__init__.py`：

```python
"""金融 AI 数据源包（gangtise-reason，OpenAI 兼容 SSE 问答接口）。

公开 API（Task 6 填充）：
    ask(query, ...)              单次查询
    ask_multi_turn(topic)        多轮 REPL session
    quota()                      配额查询
"""

__all__ = ["ask", "ask_multi_turn", "quota"]
```

- [ ] **Step 3: 写 `tests/fin_ai/__init__.py` 空文件**

文件 `tests/fin_ai/__init__.py`：

```python
```

- [ ] **Step 4: 写 `.env.example`**

文件 `.env.example`：

```ini
# 金融 AI（gangtise-reason）凭证 — 复制为 .env 后填实值
# 由 tools/fin_ai/config.py 加载
FIN_AI_BASE_URL=http://192.168.1.91:31176
FIN_AI_UID=your_uid
FIN_AI_TENANT_ID=your_tenant_id
FIN_AI_PRODUCT_CODE=your_product_code
FIN_AI_CLIENT_CATEGORY=your_client_category
FIN_AI_AUTH_TOKEN=your_token_here
FIN_AI_MODEL=gangtise-reason
```

- [ ] **Step 5: 写 `requirements.txt`**

文件 `requirements.txt`：

```
httpx>=0.27
```

- [ ] **Step 6: 修改 `.gitignore`，新增两条规则**

在现有 `.gitignore` 末尾追加：

```
# 金融 AI 凭证（本地配置，含 token）
.env

# 金融 AI 缓存目录（含问答内容，可能涉密）
data/fin_ai_cache/
```

- [ ] **Step 7: 提交**

```bash
git add tools/fin_ai/__init__.py tests/fin_ai/__init__.py .env.example requirements.txt .gitignore
git commit -m "feat(fin-ai): 添加包骨架、.env.example、requirements、gitignore 规则"
```

---

## Task 2: config.py — 凭证加载（TDD）

**Files:**
- Create: `tests/fin_ai/test_config.py`
- Create: `tools/fin_ai/config.py`

- [ ] **Step 1: 写失败测试**

文件 `tests/fin_ai/test_config.py`：

```python
"""config.py 单元测试：凭证加载与 headers 生成。"""
import os
import textwrap
import pytest

from tools.fin_ai.config import Config, ConfigError


def test_load_from_env(monkeypatch):
    """环境变量优先，正确加载所有字段。"""
    monkeypatch.setenv("FIN_AI_BASE_URL", "http://test:9999")
    monkeypatch.setenv("FIN_AI_UID", "u1")
    monkeypatch.setenv("FIN_AI_TENANT_ID", "t1")
    monkeypatch.setenv("FIN_AI_PRODUCT_CODE", "p1")
    monkeypatch.setenv("FIN_AI_CLIENT_CATEGORY", "c1")
    monkeypatch.setenv("FIN_AI_AUTH_TOKEN", "tok")
    monkeypatch.setenv("FIN_AI_MODEL", "m1")
    # 防止误读真实 .env
    monkeypatch.setattr("tools.fin_ai.config._DOTENV_PATH", "/nonexistent")

    cfg = Config.load()

    assert cfg.base_url == "http://test:9999"
    assert cfg.uid == "u1"
    assert cfg.tenant_id == "t1"
    assert cfg.product_code == "p1"
    assert cfg.client_category == "c1"
    assert cfg.auth_token == "tok"
    assert cfg.model == "m1"


def test_load_from_dotenv(tmp_path, monkeypatch):
    """.env 文件被正确解析。"""
    dotenv = tmp_path / ".env"
    dotenv.write_text(textwrap.dedent("""
        FIN_AI_BASE_URL=http://dotenv:1234
        FIN_AI_UID=du
        FIN_AI_TENANT_ID=dt
        FIN_AI_PRODUCT_CODE=dp
        FIN_AI_CLIENT_CATEGORY=dc
        FIN_AI_AUTH_TOKEN=dtok
        FIN_AI_MODEL=dm
    """).strip())

    # 清空所有相关环境变量，强制走 .env 文件
    for k in ("FIN_AI_BASE_URL", "FIN_AI_UID", "FIN_AI_TENANT_ID",
             "FIN_AI_PRODUCT_CODE", "FIN_AI_CLIENT_CATEGORY",
             "FIN_AI_AUTH_TOKEN", "FIN_AI_MODEL"):
        monkeypatch.delenv(k, raising=False)

    monkeypatch.setattr("tools.fin_ai.config._DOTENV_PATH", str(dotenv))

    cfg = Config.load()

    assert cfg.base_url == "http://dotenv:1234"
    assert cfg.uid == "du"
    assert cfg.model == "dm"


def test_env_takes_priority_over_dotenv(tmp_path, monkeypatch):
    """环境变量优先于 .env 文件。"""
    dotenv = tmp_path / ".env"
    dotenv.write_text("FIN_AI_UID=fromfile")
    monkeypatch.setenv("FIN_AI_UID", "fromenv")
    monkeypatch.setattr("tools.fin_ai.config._DOTENV_PATH", str(dotenv))
    # 其他字段用 env 补齐
    for k, v in [("FIN_AI_BASE_URL", "u"), ("FIN_AI_TENANT_ID", "t"),
                 ("FIN_AI_PRODUCT_CODE", "p"), ("FIN_AI_CLIENT_CATEGORY", "c"),
                 ("FIN_AI_AUTH_TOKEN", "tok"), ("FIN_AI_MODEL", "m")]:
        monkeypatch.setenv(k, v)

    cfg = Config.load()
    assert cfg.uid == "fromenv"


def test_missing_credential_raises(monkeypatch):
    """缺关键字段时抛 ConfigError。"""
    for k in ("FIN_AI_BASE_URL", "FIN_AI_UID", "FIN_AI_TENANT_ID",
             "FIN_AI_PRODUCT_CODE", "FIN_AI_CLIENT_CATEGORY",
             "FIN_AI_AUTH_TOKEN", "FIN_AI_MODEL"):
        monkeypatch.delenv(k, raising=False)
    monkeypatch.setattr("tools.fin_ai.config._DOTENV_PATH", "/nonexistent")

    with pytest.raises(ConfigError) as exc:
        Config.load()
    msg = str(exc.value)
    assert "FIN_AI_BASE_URL" in msg or "FIN_AI_UID" in msg


def test_headers_format(monkeypatch):
    """headers() 返回包含 Authorization Bearer 的完整 dict。"""
    monkeypatch.setenv("FIN_AI_BASE_URL", "http://x")
    monkeypatch.setenv("FIN_AI_UID", "u")
    monkeypatch.setenv("FIN_AI_TENANT_ID", "t")
    monkeypatch.setenv("FIN_AI_PRODUCT_CODE", "p")
    monkeypatch.setenv("FIN_AI_CLIENT_CATEGORY", "c")
    monkeypatch.setenv("FIN_AI_AUTH_TOKEN", "abc123")
    monkeypatch.setenv("FIN_AI_MODEL", "m")
    monkeypatch.setattr("tools.fin_ai.config._DOTENV_PATH", "/nonexistent")

    cfg = Config.load()
    h = cfg.headers()

    assert h["uid"] == "u"
    assert h["tenantid"] == "t"
    assert h["productcode"] == "p"
    assert h["clientcategory"] == "c"
    assert h["Authorization"] == "Bearer abc123"
    assert h["Content-Type"] == "application/json"
```

- [ ] **Step 2: 跑测试，确认失败**

```bash
python -m pytest tests/fin_ai/test_config.py -v
```

预期：所有用例 FAIL（`ModuleNotFoundError: No module named 'tools.fin_ai.config'`）。

- [ ] **Step 3: 实现 config.py**

文件 `tools/fin_ai/config.py`：

```python
"""凭证加载：从环境变量或 .env 文件读取金融 AI 接口配置。

优先级：环境变量 > .env 文件。
缺关键字段时抛 ConfigError。
"""
import os
from dataclasses import dataclass
from pathlib import Path


_DOTENV_PATH = Path(__file__).resolve().parents[2] / ".env"

_REQUIRED_FIELDS = (
    ("FIN_AI_BASE_URL", "base_url"),
    ("FIN_AI_UID", "uid"),
    ("FIN_AI_TENANT_ID", "tenant_id"),
    ("FIN_AI_PRODUCT_CODE", "product_code"),
    ("FIN_AI_CLIENT_CATEGORY", "client_category"),
    ("FIN_AI_AUTH_TOKEN", "auth_token"),
    ("FIN_AI_MODEL", "model"),
)


class ConfigError(Exception):
    """凭证缺失或格式错误。"""


@dataclass
class Config:
    base_url: str
    uid: str
    tenant_id: str
    product_code: str
    client_category: str
    auth_token: str
    model: str

    @classmethod
    def load(cls) -> "Config":
        """优先环境变量，其次 .env 文件。"""
        env = _load_dotenv()
        kwargs = {}
        missing = []
        for env_key, field in _REQUIRED_FIELDS:
            val = os.environ.get(env_key) or env.get(env_key)
            if not val:
                missing.append(env_key)
            else:
                kwargs[field] = val
        if missing:
            raise ConfigError(
                f"缺少金融 AI 凭证: {', '.join(missing)}；"
                f"参考 .env.example 配置 .env 文件"
            )
        return cls(**kwargs)

    def headers(self) -> dict:
        """生成请求头。"""
        return {
            "uid": self.uid,
            "tenantid": self.tenant_id,
            "productcode": self.product_code,
            "clientcategory": self.client_category,
            "Authorization": f"Bearer {self.auth_token}",
            "Content-Type": "application/json",
        }


def _load_dotenv() -> dict:
    """简单解析 .env 文件，不支持引号/嵌套变量。"""
    if not _DOTENV_PATH.exists():
        return {}
    result = {}
    for line in _DOTENV_PATH.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if "=" not in line:
            continue
        k, _, v = line.partition("=")
        result[k.strip()] = v.strip()
    return result
```

- [ ] **Step 4: 跑测试，确认通过**

```bash
python -m pytest tests/fin_ai/test_config.py -v
```

预期：5 个用例全 PASS。

- [ ] **Step 5: 提交**

```bash
git add tests/fin_ai/test_config.py tools/fin_ai/config.py
git commit -m "feat(fin-ai): 实现 config.py 凭证加载（环境变量+ .env）"
```

---

## Task 3: cache.py — 文件 hash 缓存（TDD）

**Files:**
- Create: `tests/fin_ai/test_cache.py`
- Create: `tools/fin_ai/cache.py`

- [ ] **Step 1: 写失败测试**

文件 `tests/fin_ai/test_cache.py`：

```python
"""cache.py 单元测试：hash key、TTL、原子写。"""
import json
import time
from pathlib import Path

import pytest

from tools.fin_ai import cache


@pytest.fixture
def cache_dir(tmp_path, monkeypatch):
    """重定向缓存目录到 tmp_path。"""
    d = tmp_path / "cache"
    d.mkdir()
    monkeypatch.setattr(cache, "_CACHE_DIR", d)
    return d


def test_cache_key_stable():
    """相同输入产相同 key。"""
    k1 = cache.cache_key("茅台研报", "gangtise-reason")
    k2 = cache.cache_key("茅台研报", "gangtise-reason")
    assert k1 == k2
    assert len(k1) == 64  # SHA256 hex


def test_cache_key_includes_model():
    """不同 model 不混淆。"""
    k1 = cache.cache_key("茅台研报", "model-a")
    k2 = cache.cache_key("茅台研报", "model-b")
    assert k1 != k2


def test_cache_key_multi_turn():
    """多轮对话 sid 区分。"""
    k1 = cache.cache_key("问题", "m", conversation_sid_prefix="sid1:turn:1")
    k2 = cache.cache_key("问题", "m", conversation_sid_prefix="sid1:turn:2")
    assert k1 != k2


def test_put_then_get(cache_dir):
    """写后读，命中。"""
    key = cache.cache_key("q", "m")
    cache.put(key, {"content": "答案", "ts": "2026-07-03T10:00:00+08:00"})
    got = cache.get(key, ttl_hours=24)
    assert got is not None
    assert got["content"] == "答案"


def test_get_returns_none_when_missing(cache_dir):
    """未写过返回 None。"""
    key = cache.cache_key("nope", "m")
    assert cache.get(key, ttl_hours=24) is None


def test_get_returns_none_when_expired(cache_dir):
    """过期返回 None。"""
    key = cache.cache_key("q", "m")
    # 写一个 2 小时前的 ts
    cache.put(key, {"content": "旧", "ts": "2026-07-03T08:00:00+08:00"})
    # 用 1h TTL 检查，应该过期（假设当前时间在 10:00 之后）
    # 为了测试稳定，直接 monkeypatch now
    import datetime as dt
    fake_now = dt.datetime(2026, 7, 3, 11, 0, 0, tzinfo=dt.timezone.utc)
    real_now = cache._now
    cache._now = lambda: fake_now
    try:
        # ts = 08:00, now = 11:00 → diff = 3h > 1h TTL → 过期
        # 但 ts 是 2026-07-03T08:00:00+08:00 = 00:00 UTC，diff 实际是 11h
        assert cache.get(key, ttl_hours=1) is None
    finally:
        cache._now = real_now


def test_atomic_write(cache_dir):
    """写入完成后无 .tmp 文件残留。"""
    key = cache.cache_key("q", "m")
    cache.put(key, {"content": "x", "ts": "2026-07-03T10:00:00+08:00"})
    files = list(cache_dir.iterdir())
    assert len(files) == 1
    assert files[0].suffix == ".json"
    assert not any(f.suffix == ".tmp" for f in files)


def test_clear_all(cache_dir):
    """clear(all=True) 删全部缓存。"""
    for q in ("a", "b", "c"):
        k = cache.cache_key(q, "m")
        cache.put(k, {"content": q, "ts": "2026-07-03T10:00:00+08:00"})
    assert len(list(cache_dir.iterdir())) == 3
    cleared = cache.clear(all=True)
    assert cleared == 3
    assert len(list(cache_dir.iterdir())) == 0


def test_clear_by_query(cache_dir):
    """clear(query='a') 仅删匹配的。"""
    for q in ("茅台", "腾讯", "茅台2"):
        k = cache.cache_key(q, "m")
        cache.put(k, {"content": q, "ts": "2026-07-03T10:00:00+08:00",
                      "query": q})
    cleared = cache.clear(query="茅台")
    assert cleared == 2  # "茅台" 和 "茅台2" 都匹配
    assert len(list(cache_dir.iterdir())) == 1


def test_list_recent(cache_dir):
    """history 返回最近条目，按 ts 倒序。"""
    for i, q in enumerate(("a", "b", "c")):
        k = cache.cache_key(q, "m")
        cache.put(k, {
            "content": q,
            "ts": f"2026-07-0{i+1}T10:00:00+08:00",
            "query": q,
        })
    items = cache.list_recent(limit=10)
    assert len(items) == 3
    # 按 ts 倒序，最新的 c 在前
    assert items[0]["query"] == "c"
```

- [ ] **Step 2: 跑测试，确认失败**

```bash
python -m pytest tests/fin_ai/test_cache.py -v
```

预期：所有用例 FAIL（`ImportError: cannot import name 'cache' from 'tools.fin_ai'`）。

- [ ] **Step 3: 实现 cache.py**

文件 `tools/fin_ai/cache.py`：

```python
"""文件 hash 缓存：避免 80 次/天配额被烧光。

缓存 key = SHA256(query + model + sid_prefix)。
缓存文件 = _CACHE_DIR/<key>.json，原子写（.tmp → rename）。
"""
import datetime as _dt
import hashlib
import json
import os
from pathlib import Path
from typing import Optional


_CACHE_DIR = Path(__file__).resolve().parents[2] / "data" / "fin_ai_cache"


def _now() -> _dt.datetime:
    """当前 UTC 时间（便于测试 monkeypatch）。"""
    return _dt.datetime.now(_dt.timezone.utc)


def cache_key(
    query: str,
    model: str,
    conversation_sid_prefix: str = "",
) -> str:
    """生成缓存 key。"""
    raw = f"{query}|{model}|{conversation_sid_prefix}"
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def get(key: str, ttl_hours: int) -> Optional[dict]:
    """命中且未过期返回 dict，否则 None。"""
    path = _CACHE_DIR / f"{key}.json"
    if not path.exists():
        return None
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return None
    ts = data.get("ts")
    if not ts:
        return None
    try:
        ts_dt = _dt.datetime.fromisoformat(ts)
    except ValueError:
        return None
    if ts_dt.tzinfo is None:
        ts_dt = ts_dt.replace(tzinfo=_dt.timezone.utc)
    age_seconds = (_now() - ts_dt).total_seconds()
    if age_seconds > ttl_hours * 3600:
        return None
    return data


def put(key: str, data: dict) -> None:
    """原子写（先写 .tmp 再 rename）。"""
    _CACHE_DIR.mkdir(parents=True, exist_ok=True)
    final = _CACHE_DIR / f"{key}.json"
    tmp = _CACHE_DIR / f"{key}.json.tmp"
    tmp.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    os.replace(tmp, final)


def clear(all: bool = False, query: str = "") -> int:
    """清缓存，返回删除条数。

    - all=True：清空整个缓存目录
    - query 非空：仅删 query 字段包含该子串的条目
    """
    if not _CACHE_DIR.exists():
        return 0
    removed = 0
    for path in _CACHE_DIR.glob("*.json"):
        if all:
            path.unlink()
            removed += 1
            continue
        if query:
            try:
                data = json.loads(path.read_text(encoding="utf-8"))
                if query in data.get("query", ""):
                    path.unlink()
                    removed += 1
            except (json.JSONDecodeError, OSError):
                continue
    return removed


def list_recent(limit: int = 20) -> list:
    """返回最近条目，按 ts 倒序。"""
    if not _CACHE_DIR.exists():
        return []
    items = []
    for path in _CACHE_DIR.glob("*.json"):
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
            items.append(data)
        except (json.JSONDecodeError, OSError):
            continue
    items.sort(key=lambda x: x.get("ts", ""), reverse=True)
    return items[:limit]
```

- [ ] **Step 4: 跑测试，确认通过**

```bash
python -m pytest tests/fin_ai/test_cache.py -v
```

预期：9 个用例全 PASS。

- [ ] **Step 5: 提交**

```bash
git add tests/fin_ai/test_cache.py tools/fin_ai/cache.py
git commit -m "feat(fin-ai): 实现 cache.py 文件 hash 缓存（SHA256 + TTL + 原子写）"
```

---

## Task 4: client.py — HTTP + SSE 客户端（TDD）

**Files:**
- Create: `tests/fin_ai/test_client.py`
- Create: `tools/fin_ai/client.py`

- [ ] **Step 1: 写失败测试（mock SSE）**

文件 `tests/fin_ai/test_client.py`：

```python
"""client.py 集成测试：mock SSE，不发真实请求。"""
import json
from unittest.mock import MagicMock

import httpx
import pytest

from tools.fin_ai.client import FinAIClient, FinAIError, ChatResult
from tools.fin_ai.config import Config


@pytest.fixture
def fake_config():
    return Config(
        base_url="http://test:9999",
        uid="u",
        tenant_id="t",
        product_code="p",
        client_category="c",
        auth_token="tok",
        model="m",
    )


def _sse_lines(events):
    """把 [(event_type, data_dict)] 转换为 SSE 文本行列表。"""
    lines = []
    for evt, data in events:
        lines.append(f"event: {evt}")
        lines.append(f"data: {json.dumps(data)}")
        lines.append("")
    lines.append("data: [STOP]")
    lines.append("")
    return lines


def _mock_transport(events, status_code=200, headers=None):
    """构造 mock SSE transport。"""
    body = "\n".join(_sse_lines(events)).encode("utf-8")
    response_headers = headers or {"Content-Type": "text/event-stream", "X-Session-Id": "173"}

    def handler(request):
        return httpx.Response(
            status_code,
            headers=response_headers,
            content=body,
        )
    return httpx.MockTransport(handler)


def test_normal_stream(fake_config):
    """正常 SSE 流，断言拼接内容、session_id、usage。"""
    events = [
        ("response.created", {"type": "response.created"}),
        ("response.output_text.delta", {"type": "response.output_text.delta", "delta": "你"}),
        ("response.output_text.delta", {"type": "response.output_text.delta", "delta": "好"}),
        ("response.completed", {
            "type": "response.completed",
            "response": {
                "id": "resp_xxx",
                "status": "completed",
                "usage": {"input_tokens": 100, "output_tokens": 2, "total_tokens": 102},
            },
        }),
    ]
    transport = _mock_transport(events)
    client = FinAIClient(fake_config, transport=transport)
    chunks = []
    result = client.chat("你好", on_delta=chunks.append)

    assert isinstance(result, ChatResult)
    assert result.content == "你好"
    assert result.session_id == 173
    assert result.usage["total_tokens"] == 102
    assert chunks == ["你", "好"]


def test_stop_marker_terminates(fake_config):
    """收到 [STOP] 正常结束。"""
    events = [
        ("response.output_text.delta", {"delta": "答"}),
        ("response.completed", {"response": {"usage": {"total_tokens": 1}}}),
    ]
    transport = _mock_transport(events)
    client = FinAIClient(fake_config, transport=transport)
    result = client.chat("问")
    assert result.content == "答"


def test_daily_limit_exceeded(fake_config):
    """SSE 返回 daily_limit_exceeded → raise FinAIError，不重试。"""
    events = [
        ("error", {"errorCode": "daily_limit_exceeded", "errorMsg": "当日次数已达上限"}),
    ]
    transport = _mock_transport(events)
    client = FinAIClient(fake_config, transport=transport)
    with pytest.raises(FinAIError) as exc:
        client.chat("问")
    assert "daily_limit_exceeded" in str(exc.value)


def test_reconnect_expired_no_retry(fake_config):
    """reconnect_expired → 不重试，直接 raise。"""
    events = [
        ("error", {"errorCode": "reconnect_expired", "errorMsg": "会话不存在"}),
    ]
    transport = _mock_transport(events)
    client = FinAIClient(fake_config, transport=transport)
    with pytest.raises(FinAIError) as exc:
        client.chat("问")
    assert "reconnect_expired" in str(exc.value)


def test_unknown_event_skipped(fake_config):
    """未知 event: 类型不报错。"""
    events = [
        ("unknown.future.event", {"foo": "bar"}),
        ("response.output_text.delta", {"delta": "正常"}),
        ("response.completed", {"response": {"usage": {"total_tokens": 1}}}),
    ]
    transport = _mock_transport(events)
    client = FinAIClient(fake_config, transport=transport)
    result = client.chat("问")
    assert result.content == "正常"


def test_conversation_sid_auto_generated(fake_config):
    """conversation_sid 未传时自动生成 uuid4。"""
    events = [
        ("response.completed", {"response": {"usage": {"total_tokens": 1}}}),
    ]
    transport = _mock_transport(events)
    client = FinAIClient(fake_config, transport=transport)
    result = client.chat("问")
    assert result.conversation_sid  # 非空
    assert len(result.conversation_sid) == 36  # uuid4 长度


def test_conversation_sid_reused(fake_config):
    """传入 conversation_sid 时复用。"""
    events = [
        ("response.completed", {"response": {"usage": {"total_tokens": 1}}}),
    ]
    transport = _mock_transport(events)
    client = FinAIClient(fake_config, transport=transport)
    result = client.chat("问", conversation_sid="my-fixed-sid")
    assert result.conversation_sid == "my-fixed-sid"


def test_network_error_retry_then_success(fake_config):
    """首次 ConnectError，重试 1 次成功。"""
    events = [
        ("response.completed", {"response": {"usage": {"total_tokens": 1}}}),
    ]
    body = "\n".join(_sse_lines(events)).encode("utf-8")

    call_count = {"n": 0}

    def handler(request):
        call_count["n"] += 1
        if call_count["n"] == 1:
            raise httpx.ConnectError("connection refused")
        return httpx.Response(200, headers={"Content-Type": "text/event-stream"},
                              content=body)

    transport = httpx.MockTransport(handler)
    client = FinAIClient(fake_config, transport=transport, retry_delay=0)
    result = client.chat("问")
    assert call_count["n"] == 2
    assert isinstance(result, ChatResult)
```

- [ ] **Step 2: 跑测试，确认失败**

```bash
python -m pytest tests/fin_ai/test_client.py -v
```

预期：所有用例 FAIL（`ImportError: cannot import name 'FinAIClient'`）。

- [ ] **Step 3: 实现 client.py**

文件 `tools/fin_ai/client.py`：

```python
"""HTTP + SSE 客户端：封装 /openai/chat，处理增量拼接、错误码、断线重连。

外部 API:
    FinAIClient(config, transport=None, retry_delay=2)
        .chat(query, conversation_sid=None, on_delta=None, timeout=120) -> ChatResult

错误处理见 spec §5.1。
"""
import json
import time
import uuid
from dataclasses import dataclass, field
from typing import Callable, Optional

import httpx


class FinAIError(Exception):
    """金融 AI 接口业务错误（含 errorCode）。"""

    def __init__(self, code: str, msg: str = ""):
        self.code = code
        super().__init__(f"{code}: {msg}" if msg else code)


@dataclass
class ChatResult:
    content: str
    session_id: int
    conversation_sid: str
    usage: dict
    raw_events: list = field(default_factory=list)


class FinAIClient:
    def __init__(
        self,
        config,
        transport: Optional[httpx.BaseTransport] = None,
        retry_delay: int = 2,
    ):
        self.config = config
        self.retry_delay = retry_delay
        # transport 用于测试 mock；生产传 None 走默认
        self._client = httpx.Client(timeout=120.0, transport=transport)

    def chat(
        self,
        query: str,
        conversation_sid: Optional[str] = None,
        on_delta: Optional[Callable[[str], None]] = None,
        timeout: int = 120,
    ) -> ChatResult:
        """发起 SSE 问答。

        - conversation_sid=None 自动生成 uuid4
        - on_delta 收到 delta 时回调
        - 网络/5xx 错误重试 1 次
        """
        sid = conversation_sid or str(uuid.uuid4())
        last_exc = None
        for attempt in (1, 2):
            try:
                return self._chat_once(query, sid, on_delta, timeout)
            except httpx.HTTPStatusError as e:
                if e.response.status_code in (401, 403, 404):
                    raise  # 凭证/路径错误不重试
                last_exc = e
                if attempt == 1:
                    print(f"[RETRY] HTTP {e.response.status_code}")
                    time.sleep(self.retry_delay)
                    continue
                raise
            except (httpx.ConnectError, httpx.TimeoutException) as e:
                last_exc = e
                if attempt == 1:
                    print(f"[RETRY] {type(e).__name__}")
                    time.sleep(self.retry_delay)
                    continue
                raise
            except FinAIError:
                raise  # 业务错误不重试
        raise last_exc  # type: ignore

    def _chat_once(
        self,
        query: str,
        sid: str,
        on_delta: Optional[Callable[[str], None]],
        timeout: int,
    ) -> ChatResult:
        payload = {"input": query, "model": self.config.model, "conversationSid": sid}
        content_parts, usage, raw_events = [], {}, []
        current_event = None
        session_id = 0

        with self._client.stream(
            "POST",
            f"{self.config.base_url}/openai/chat",
            headers=self.config.headers(),
            json=payload,
            timeout=timeout,
        ) as stream:
            if stream.status_code >= 400:
                stream.read()
                raise httpx.HTTPStatusError(
                    f"HTTP {stream.status_code}",
                    request=stream.request,
                    response=stream,
                )
            session_id = int(stream.headers.get("X-Session-Id", "0") or 0)
            for line in stream.iter_lines():
                if not line:
                    current_event = None
                    continue
                if line.startswith("event:"):
                    current_event = line[6:].strip()
                    continue
                if not line.startswith("data:"):
                    continue
                payload_str = line[5:].strip()
                if payload_str == "[STOP]":
                    break
                try:
                    data = json.loads(payload_str)
                except json.JSONDecodeError:
                    continue
                raw_events.append({"event": current_event, "data": data})
                if "errorCode" in data:
                    raise FinAIError(data["errorCode"], data.get("errorMsg", ""))
                if current_event == "response.output_text.delta":
                    delta = data.get("delta", "")
                    if delta:
                        content_parts.append(delta)
                        if on_delta:
                            on_delta(delta)
                elif current_event == "response.completed":
                    usage = data.get("response", {}).get("usage", {})

        return ChatResult(
            content="".join(content_parts),
            session_id=session_id,
            conversation_sid=sid,
            usage=usage,
            raw_events=raw_events,
        )

    def close(self):
        self._client.close()
```

**注意**：测试中用 `httpx.MockTransport` 注入到 `transport` 参数；生产代码不传 `transport`，走默认。

- [ ] **Step 4: 跑测试，确认通过**

```bash
python -m pytest tests/fin_ai/test_client.py -v
```

预期：8 个用例全 PASS。

- [ ] **Step 5: 提交**

```bash
git add tests/fin_ai/test_client.py tools/fin_ai/client.py
git commit -m "feat(fin-ai): 实现 client.py HTTP+SSE 客户端（增量拼接、错误码、重试）"
```

---

## Task 5: quota.py — 配额预检（TDD）

**Files:**
- Create: `tests/fin_ai/test_quota.py`
- Create: `tools/fin_ai/quota.py`

- [ ] **Step 1: 写失败测试**

文件 `tests/fin_ai/test_quota.py`：

```python
"""quota.py 单元测试：剩余配额、警告阈值。"""
import json
from unittest.mock import MagicMock

import httpx
import pytest

from tools.fin_ai.quota import QuotaStatus, pre_check
from tools.fin_ai.client import FinAIClient
from tools.fin_ai.config import Config


@pytest.fixture
def fake_client():
    cfg = Config(
        base_url="http://test:9999", uid="u", tenant_id="t",
        product_code="p", client_category="c",
        auth_token="tok", model="m",
    )
    transport = httpx.MockTransport(lambda req: httpx.Response(
        200,
        content=json.dumps({
            "code": "000000", "msg": "ok",
            "data": {"exceeded": False, "used": 5, "limit": 80, "remaining": 75},
        }),
    ))
    return FinAIClient(cfg, transport=transport)


def test_pre_check_parses_response(fake_client):
    """pre_check 正确解析 limit 接口。"""
    status = pre_check(fake_client)
    assert isinstance(status, QuotaStatus)
    assert status.exceeded is False
    assert status.used == 5
    assert status.limit == 80
    assert status.remaining == 75


def test_pre_check_returns_exceeded():
    """exceeded=true 被正确捕获。"""
    cfg = Config(base_url="http://x", uid="u", tenant_id="t",
                 product_code="p", client_category="c",
                 auth_token="tok", model="m")
    transport = httpx.MockTransport(lambda req: httpx.Response(
        200,
        content=json.dumps({
            "code": "000000", "msg": "ok",
            "data": {"exceeded": True, "used": 80, "limit": 80, "remaining": 0},
        }),
    ))
    client = FinAIClient(cfg, transport=transport)
    status = pre_check(client)
    assert status.exceeded is True
    assert status.remaining == 0


def test_pre_check_degrades_on_api_error():
    """limit 接口自身失败时，降级返回 None（不阻塞调用）。"""
    cfg = Config(base_url="http://x", uid="u", tenant_id="t",
                 product_code="p", client_category="c",
                 auth_token="tok", model="m")
    transport = httpx.MockTransport(lambda req: httpx.Response(500))
    client = FinAIClient(cfg, transport=transport)
    status = pre_check(client)
    assert status is None


def test_should_warn_at_threshold_2():
    """remaining=2 触发警告。"""
    s = QuotaStatus(exceeded=False, used=78, limit=80, remaining=2)
    assert s.should_warn() is True


def test_no_warn_at_threshold_5():
    """remaining=5 不警告。"""
    s = QuotaStatus(exceeded=False, used=75, limit=80, remaining=5)
    assert s.should_warn() is False


def test_no_warn_when_exceeded():
    """已 exceeded 时不重复警告。"""
    s = QuotaStatus(exceeded=True, used=80, limit=80, remaining=0)
    assert s.should_warn() is False
```

- [ ] **Step 2: 跑测试，确认失败**

```bash
python -m pytest tests/fin_ai/test_quota.py -v
```

预期：所有用例 FAIL（`ImportError: cannot import name 'pre_check'`）。

- [ ] **Step 3: 实现 quota.py**

文件 `tools/fin_ai/quota.py`：

```python
"""配额预检：调 GET /openai/chat/limit，返回剩余次数。

接口失败时降级返回 None（不阻塞调用，文档明确"容错返回 used=0"）。
"""
import json
from dataclasses import dataclass
from typing import Optional


@dataclass
class QuotaStatus:
    exceeded: bool
    used: int
    limit: int
    remaining: int

    def should_warn(self) -> bool:
        """剩余 < 3 且未 exceeded 时警告。"""
        return self.remaining < 3 and not self.exceeded


def pre_check(client) -> Optional[QuotaStatus]:
    """调 limit 接口，失败返回 None。"""
    try:
        resp = client._client.get(
            f"{client.config.base_url}/openai/chat/limit",
            headers=client.config.headers(),
            timeout=10.0,
        )
        if resp.status_code != 200:
            return None
        body = resp.json()
        data = body.get("data") or {}
        if not data:
            return None
        return QuotaStatus(
            exceeded=bool(data.get("exceeded", False)),
            used=int(data.get("used", 0)),
            limit=int(data.get("limit", 80)),
            remaining=int(data.get("remaining", 0)),
        )
    except Exception:
        return None
```

- [ ] **Step 4: 跑测试，确认通过**

```bash
python -m pytest tests/fin_ai/test_quota.py -v
```

预期：6 个用例全 PASS。

- [ ] **Step 5: 提交**

```bash
git add tests/fin_ai/test_quota.py tools/fin_ai/quota.py
git commit -m "feat(fin-ai): 实现 quota.py 配额预检（含降级）"
```

---

## Task 6: cli.py 与 __init__.py — 串联全流程

**Files:**
- Create: `tools/fin_ai/cli.py`
- Modify: `tools/fin_ai/__init__.py`

- [ ] **Step 1: 实现 cli.py（无单元测试，靠 e2e checklist 验收）**

文件 `tools/fin_ai/cli.py`：

```python
"""金融 AI CLI 入口。

子命令：
    ask "query"          单次查询（流式打印）
    ask --multi "topic"  多轮 REPL
    quota                查配额
    history              查最近缓存（本地，不烧配额）
    clear-cache          清缓存
"""
import argparse
import sys
import time
import uuid
from pathlib import Path

from .cache import cache_key, get as cache_get, put as cache_put, clear as cache_clear, list_recent
from .client import FinAIClient, FinAIError
from .config import Config, ConfigError
from .quota import pre_check


def main(argv=None):
    parser = argparse.ArgumentParser(prog="python -m tools.fin_ai")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_ask = sub.add_parser("ask", help="单次或 REPL 多轮查询")
    p_ask.add_argument("query", nargs="?", help="查询内容（--multi 时为初始话题）")
    p_ask.add_argument("--multi", action="store_true", help="进入多轮 REPL")
    p_ask.add_argument("--ttl-hours", type=int, default=24, help="缓存 TTL（小时）")
    p_ask.add_argument("--no-cache", action="store_true", help="跳过查缓存（仍写缓存）")
    p_ask.add_argument("--refresh", action="store_true", help="强制刷新，覆盖旧缓存")

    sub.add_parser("quota", help="查当日配额")
    p_hist = sub.add_parser("history", help="查最近缓存")
    p_hist.add_argument("--limit", type=int, default=20)

    p_clear = sub.add_parser("clear-cache", help="清缓存")
    p_clear.add_argument("--all", action="store_true")
    p_clear.add_argument("--query", default="")

    args = parser.parse_args(argv)

    try:
        if args.cmd == "ask":
            return _cmd_ask(args)
        if args.cmd == "quota":
            return _cmd_quota()
        if args.cmd == "history":
            return _cmd_history(args.limit)
        if args.cmd == "clear-cache":
            return _cmd_clear(args.all, args.query)
    except ConfigError as e:
        print(f"[FIN_AI ERROR] {e}", file=sys.stderr)
        return 2
    except FinAIError as e:
        print(f"[FIN_AI ERROR] {e}", file=sys.stderr)
        if "daily_limit_exceeded" in str(e):
            return 4
        if "reconnect_expired" in str(e) or "reconnect_completed" in str(e):
            return 6
        if "reconnect_forbidden" in str(e):
            return 7
        return 5


def _cmd_ask(args):
    cfg = Config.load()
    client = FinAIClient(cfg)

    if args.multi:
        return _repl(client, args.query or "")

    if not args.query:
        print("error: ask 需要提供 query 或 --multi", file=sys.stderr)
        return 1

    key = cache_key(args.query, cfg.model)
    if not args.refresh and not args.no_cache:
        cached = cache_get(key, args.ttl_hours)
        if cached:
            print(f"[FIN_AI] [CACHE HIT] (cached at {cached.get('ts')})")
            print(cached["content"])
            return 0

    # 配额预检
    status = pre_check(client)
    if status and status.exceeded:
        print(f"[FIN_AI ERROR] 配额已耗尽 ({status.used}/{status.limit})，明天 00:00 重置", file=sys.stderr)
        return 3
    if status and status.should_warn():
        print(f"[FIN_AI WARN] 配额将耗尽：剩余 {status.remaining}/{status.limit}", file=sys.stderr)

    print(f"[FIN_AI] querying: {args.query}", file=sys.stderr)
    if status:
        print(f"[FIN_AI] quota: remaining {status.remaining}/{status.limit}", file=sys.stderr)

    start = time.time()
    sep = "─" * 40
    print(sep)
    result = client.chat(args.query, on_delta=lambda c: print(c, end="", flush=True))
    print()
    print(sep)

    elapsed = time.time() - start
    out_tok = result.usage.get("output_tokens", "?")
    in_tok = result.usage.get("input_tokens", "?")
    print(f"[FIN_AI] done in {elapsed:.1f}s · tokens: {out_tok} out / {in_tok} in · [SID: {result.session_id}]", file=sys.stderr)

    # 写缓存（即使 --no-cache 也写，让下次受益；refresh 也写以覆盖旧值；
    # SSE 错误由 client 异常路径保证不走到这里）
    cache_put(key, {
        "query": args.query,
        "model": cfg.model,
        "content": result.content,
        "usage": result.usage,
        "ts": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
        "session_id": result.session_id,
        "conversation_sid": result.conversation_sid,
    })

    return 0


def _repl(client, topic):
    """多轮 REPL 模式。"""
    sid = str(uuid.uuid4())
    print(f"[FIN_AI] multi-turn REPL (topic={topic!r}, sid={sid[:8]}...)")
    print("[FIN_AI] /quit 退出；每轮前会显示剩余配额")
    turn = 0
    while True:
        try:
            q = input(f"turn {turn + 1} >> ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if not q:
            continue
        if q in ("/quit", "/exit", "/q"):
            break
        turn += 1

        status = pre_check(client)
        if status and status.exceeded:
            print(f"[FIN_AI ERROR] 配额已耗尽，明天再试", file=sys.stderr)
            break
        if status:
            print(f"[quota: {status.remaining}/{status.limit}]", file=sys.stderr)

        try:
            result = client.chat(q, conversation_sid=sid)
            print(result.content)
            print(f"[SID: {result.session_id}]", file=sys.stderr)
        except FinAIError as e:
            print(f"[ERROR] {e}", file=sys.stderr)
            continue

    print("[FIN_AI] session ended")
    return 0


def _cmd_quota():
    cfg = Config.load()
    client = FinAIClient(cfg)
    status = pre_check(client)
    if status is None:
        print("[FIN_AI] limit 接口不可用，无法预检")
        return 0
    print(f"exceeded: {status.exceeded}")
    print(f"used:     {status.used}")
    print(f"limit:    {status.limit}")
    print(f"remaining:{status.remaining}")
    return 0


def _cmd_history(limit):
    items = list_recent(limit=limit)
    if not items:
        print("(无缓存)")
        return 0
    for i, it in enumerate(items, 1):
        q = it.get("query", "?")[:60]
        ts = it.get("ts", "?")
        sid = it.get("session_id", "?")
        print(f"{i:3d}. [{ts}] SID={sid}  {q}")
    return 0


def _cmd_clear(all_flag, query):
    n = cache_clear(all=all_flag, query=query)
    print(f"cleared {n} entries")
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

- [ ] **Step 2: 实现 __init__.py（暴露 Python 库 API）**

文件 `tools/fin_ai/__init__.py`（覆盖 Task 1 的占位）：

```python
"""金融 AI 数据源包（gangtise-reason，OpenAI 兼容 SSE 问答接口）。

公开 API:
    ask(query, ...)              单次查询
    ask_multi_turn(topic)        多轮 REPL session（context manager）
    quota()                      配额查询
"""
import time
import uuid
from contextlib import contextmanager

from .cache import cache_key, get as cache_get, put as cache_put
from .client import FinAIClient, FinAIError, ChatResult
from .config import Config, ConfigError
from .quota import pre_check, QuotaStatus


def ask(
    query: str,
    ttl_hours: int = 24,
    refresh: bool = False,
    no_cache: bool = False,
    on_delta=None,
):
    """单次查询。命中缓存则直接返回（不烧配额）。

    返回 ChatResult（content / session_id / conversation_sid / usage）。
    """
    cfg = Config.load()
    client = FinAIClient(cfg)

    key = cache_key(query, cfg.model)
    if not refresh and not no_cache:
        cached = cache_get(key, ttl_hours)
        if cached:
            # 把缓存包成 ChatResult
            return ChatResult(
                content=cached["content"],
                session_id=cached.get("session_id", 0),
                conversation_sid=cached.get("conversation_sid", ""),
                usage=cached.get("usage", {}),
            )

    result = client.chat(query, on_delta=on_delta)
    cache_put(key, {
        "query": query,
        "model": cfg.model,
        "content": result.content,
        "usage": result.usage,
        "ts": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
        "session_id": result.session_id,
        "conversation_sid": result.conversation_sid,
    })
    return result


class _MultiTurnSession:
    """多轮对话 session（由 ask_multi_turn context manager 进入）。"""

    def __init__(self, topic: str, ttl_hours: int = 24):
        self.topic = topic
        self.ttl_hours = ttl_hours
        self.sid = str(uuid.uuid4())
        self.client = FinAIClient(Config.load())
        self._turn = 0

    def ask(self, query: str, on_delta=None) -> ChatResult:
        self._turn += 1
        # 多轮 key 包含 turn 序号，避免不同轮次混淆
        key = cache_key(query, self.client.config.model,
                        conversation_sid_prefix=f"{self.sid}:turn:{self._turn}")
        if not self.ttl_hours or self.ttl_hours > 0:
            cached = cache_get(key, self.ttl_hours)
            if cached:
                return ChatResult(
                    content=cached["content"],
                    session_id=cached.get("session_id", 0),
                    conversation_sid=cached.get("conversation_sid", ""),
                    usage=cached.get("usage", {}),
                )
        result = self.client.chat(query, conversation_sid=self.sid, on_delta=on_delta)
        cache_put(key, {
            "query": query,
            "model": self.client.config.model,
            "content": result.content,
            "usage": result.usage,
            "ts": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
            "session_id": result.session_id,
            "conversation_sid": result.conversation_sid,
        })
        return result

    def close(self):
        self.client.close()


@contextmanager
def ask_multi_turn(topic: str, ttl_hours: int = 24):
    """多轮对话 context manager。

    用法:
        with ask_multi_turn("长城军工") as session:
            r1 = session.ask("2025 年报怎么看？")
            r2 = session.ask("和北方导航比谁更好？")  # 上下文延续
    """
    session = _MultiTurnSession(topic, ttl_hours=ttl_hours)
    try:
        yield session
    finally:
        session.close()


def quota() -> QuotaStatus:
    """查当日配额。"""
    cfg = Config.load()
    client = FinAIClient(cfg)
    return pre_check(client)


__all__ = ["ask", "ask_multi_turn", "quota", "FinAIError", "ConfigError", "ChatResult"]
```

- [ ] **Step 3: 手动 smoke test**

```bash
# 确认包能 import
python -c "from tools.fin_ai import ask, ask_multi_turn, quota; print('import OK')"

# 确认 CLI 帮助能打印
python -m tools.fin_ai --help
python -m tools.fin_ai ask --help
```

预期：import OK；CLI 帮助正常显示子命令。

- [ ] **Step 4: 跑全部单元测试，确认无回归**

```bash
python -m pytest tests/fin_ai/ -v
```

预期：config / cache / client / quota 全部 PASS。

- [ ] **Step 5: 提交**

```bash
git add tools/fin_ai/cli.py tools/fin_ai/__init__.py
git commit -m "feat(fin-ai): 实现 cli.py + __init__.py（串联 ask/quota/history/clear-cache + Python 库 API）"
```

---

## Task 7: Skill 集成（4 个文件末尾追加可选模块）

**Files:**
- Modify: `skills/investment-research.md`
- Modify: `skills/earnings-review.md`
- Modify: `skills/industry-research.md`
- Modify: `skills/investment-team.md`

- [ ] **Step 1: 准备追加内容片段**

将以下 Markdown 块追加到 4 个 skill 文件的**最末尾**：

```markdown

---

## 可选步骤：金融 AI 观点补充（消耗配额，默认关闭）

如果你希望报告里包含金融 AI（gangtise-reason）的实时观点补充，在数据收集阶段调用：

\`\`\`bash
# 单次：拿最新观点/事件解读
python -m tools.fin_ai ask "{公司名} 最新市场观点和研报解读" --ttl-hours 1

# 多轮 REPL：深入对话（4-5 轮覆盖业务/竞争/估值/风险）
python -m tools.fin_ai ask --multi "{公司名}"

# 查剩余配额（每日 80 次硬上限）
python -m tools.fin_ai quota
\`\`\`

将返回内容嵌入报告「§X.X 金融 AI 观点补充」段落，明确标注：
- 来源：金融 AI（gangtise-reason），{日期}
- 类型：第三方观点，非事实数据
- 与报告其他模块的关系：补充参考，**不替代**程序化验算（PE/PB/ROE 等仍走 `financial_rigor.py`）

⚠️ **不强制使用**。配额 80/天是硬约束，长公司研究请优先用缓存命中。

Python 库调用方式（在脚本中复用）：

\`\`\`python
from tools.fin_ai import ask, ask_multi_turn

result = ask("茅台研报观点", ttl_hours=24)
print(result.content)

with ask_multi_turn("长城军工") as session:
    r1 = session.ask("2025 年报怎么看？")
    r2 = session.ask("和北方导航比谁更好？")
\`\`\`
```

- [ ] **Step 2: 追加到 4 个 skill 文件**

逐个用 Edit 工具在文件末尾追加（**注意**：先 Read 确认文件末尾结构，再用 Edit）。

对于 `skills/investment-research.md`：找到文件末尾最后一行的唯一标识（通常是「本报告仅供学习研究」之类的免责声明），在其后追加。

对其他 3 个文件同样处理。

- [ ] **Step 3: 跑 sync-codex-skills.py 同步给 Codex**

```bash
python scripts/sync-codex-skills.py
```

预期：生成 codex-skills/*/SKILL.md 更新。

- [ ] **Step 4: 校验同步**

```bash
python scripts/sync-codex-skills.py --check
```

预期：输出「所有 skills 同步一致」类信息，无 diff。

- [ ] **Step 5: 提交**

```bash
git add skills/investment-research.md skills/earnings-review.md skills/industry-research.md skills/investment-team.md codex-skills/
git commit -m "feat(fin-ai): 4 个 skill 末尾追加可选模块「金融 AI 观点补充」+ 同步 Codex"
```

---

## Task 8: 更新 CLAUDE.md + e2e checklist

**Files:**
- Modify: `CLAUDE.md`
- Create: `tests/fin_ai/e2e_checklist.md`

- [ ] **Step 1: 在 CLAUDE.md 的 Python 工具表新增一行**

找到原文中类似的表格（在「Python 工具（`tools/`）」一节）：

```markdown
| `momentum_backtest.py` / `momentum_backtest_v2.py` | 动量回测 |
```

在其**下方**新增一行：

```markdown
| `fin_ai/` | 金融 AI（gangtise-reason）SSE 问答接口客户端：观点/研报/事件解读。CLI: `python -m tools.fin_ai ask "..."` / Python: `from tools.fin_ai import ask` |
```

- [ ] **Step 2: 写 e2e_checklist.md**

文件 `tests/fin_ai/e2e_checklist.md`：

```markdown
# 金融 AI 工具端到端验收清单

> 配额贵，不写自动化。手动按本清单逐项跑通。
> 准入要求：至少通 8/10。

## 准备

- [ ] 复制 `.env.example` 为 `.env`，填入真实凭证
- [ ] `python -c "import httpx; print(httpx.__version__)"` ≥ 0.27

## 10 项验收

- [ ] **1. 配置加载**：`python -m tools.fin_ai quota` 正常返回 remaining/limit
- [ ] **2. 单次查询**：`python -m tools.fin_ai ask "茅台研报观点"` 流式打印 + 元数据 footer
- [ ] **3. 缓存命中**：再次跑相同命令，输出 `[CACHE HIT]` 标记，**不消耗配额**
- [ ] **4. 多轮 REPL**：`python -m tools.fin_ai ask --multi "长城军工"` → 3 轮对话上下文延续
- [ ] **5. 强制刷新**：`python -m tools.fin_ai ask "茅台研报观点" --refresh` → 重新调用，覆盖缓存
- [ ] **6. TTL 覆盖**：`--ttl-hours 1` + 1h 后再查，验证失效
- [ ] **7. 配额耗尽**：手动构造 `exceeded=true` 场景（或改 daily_limit 配置），CLI 拒绝调用，exit 3
- [ ] **8. 错误凭证**：清空 `FIN_AI_AUTH_TOKEN`，跑 ask → exit 2 + 提示
- [ ] **9. Python 库**：`python -c "from tools.fin_ai import ask; print(ask('茅台').content[:50])"` 正常输出
- [ ] **10. skill 集成**：跑 `/investment-research 测试公司`，报告含「§X.X 金融 AI 观点补充」段落

## 准入规则

- 10 项通 8 项及以上：可合入主分支
- 通 7 项及以下：返回修复，不得合入

## 已知不验（YAGNI）

- 容器预热（pre-acquire）：spec §9 未决项，先观察首问延迟
- 服务端对话列表：用本地 history 替代
- 跨设备会话同步：单设备够用
```

- [ ] **Step 3: 跑全部测试再确认无回归**

```bash
python -m pytest tests/fin_ai/ -v
python tools/financial_rigor.py --help 2>&1 | head -3
python tools/report_audit.py --help 2>&1 | head -3
```

预期：测试全绿；其他工具 --help 正常。

- [ ] **Step 4: 提交**

```bash
git add CLAUDE.md tests/fin_ai/e2e_checklist.md
git commit -m "docs(fin-ai): CLAUDE.md 工具表新增 fin_ai 条目 + e2e 验收清单"
```

---

## 完工验收

执行完所有 Task 后，确认：

- [ ] `python -m pytest tests/fin_ai/ -v` 全绿（≈ 28 个用例）
- [ ] `python -m tools.fin_ai --help` 正常打印子命令
- [ ] `.gitignore` 含 `.env` 和 `data/fin_ai_cache/`
- [ ] `requirements.txt` 含 `httpx>=0.27`
- [ ] `.env.example` 已提交，真实 `.env` 未提交
- [ ] `python scripts/sync-codex-skills.py --check` 输出无 diff
- [ ] `e2e_checklist.md` 至少通 8/10
- [ ] `CLAUDE.md` 工具表含 `fin_ai/` 条目
- [ ] 全部 commit 已推送到 main（或留 PR）
