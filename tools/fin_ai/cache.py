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
    """原子写（先写 .tmp 再 rename）。

    入口先清理可能存在的 .tmp 残留（上次进程崩溃在 write_text 之后、
    os.replace 之前留下的孤儿）。同 key 的 .tmp 会被本次写入覆盖，
    但显式 unlink 保证干净状态。
    """
    _CACHE_DIR.mkdir(parents=True, exist_ok=True)
    final = _CACHE_DIR / f"{key}.json"
    tmp = _CACHE_DIR / f"{key}.json.tmp"
    if tmp.exists():
        tmp.unlink(missing_ok=True)
    tmp.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    os.replace(tmp, final)


def clear(all: bool = False, query: str = "") -> int:
    """清缓存，返回删除条数。

    - all=True：清空整个缓存目录（含可能残留的 .json.tmp 孤儿）
    - query 非空：删 query 字段**包含该子串**的所有条目（模糊清理，
      用户输入部分关键词即可命中；如需精确匹配请在调用前自行过滤）。
      注意：子串匹配会同时命中 "茅台" 和 "茅台2" 等同类条目。
    """
    if not _CACHE_DIR.exists():
        return 0
    removed = 0
    # all=True 时同时清理 .json 和可能的 .json.tmp 孤儿
    if all:
        for path in _CACHE_DIR.glob("*.json"):
            path.unlink()
            removed += 1
        for tmp in _CACHE_DIR.glob("*.json.tmp"):
            tmp.unlink()
        return removed
    for path in _CACHE_DIR.glob("*.json"):
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
