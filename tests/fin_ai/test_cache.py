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
    # 用 monkeypatch 控制当前时间，避免依赖 wall clock
    import datetime as dt
    fake_now = dt.datetime(2026, 7, 3, 11, 0, 0, tzinfo=dt.timezone.utc)
    real_now = cache._now
    cache._now = lambda: fake_now
    try:
        # ts = 2026-07-03T08:00:00+08:00 = 2026-07-03T00:00:00 UTC
        # now = 2026-07-03T11:00:00 UTC
        # diff = 11 小时 > 1 小时 TTL → 过期
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
