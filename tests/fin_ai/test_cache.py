"""cache.py 单元测试：hash key、TTL、原子写。"""
import json
import time
from pathlib import Path

import pytest

from tools.fin_ai import cache


def _fresh_ts() -> str:
    """生成当前 ts（避免硬编码导致时间炸弹）。"""
    return cache._now().isoformat()


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
    cache.put(key, {"content": "答案", "ts": _fresh_ts()})
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
    cache.put(key, {"content": "x", "ts": _fresh_ts()})
    files = list(cache_dir.iterdir())
    assert len(files) == 1
    assert files[0].suffix == ".json"
    assert not any(f.suffix == ".tmp" for f in files)


def test_clear_all(cache_dir):
    """clear(all=True) 删全部缓存。"""
    for q in ("a", "b", "c"):
        k = cache.cache_key(q, "m")
        cache.put(k, {"content": q, "ts": _fresh_ts()})
    assert len(list(cache_dir.iterdir())) == 3
    cleared = cache.clear(all=True)
    assert cleared == 3
    assert len(list(cache_dir.iterdir())) == 0


def test_clear_by_query(cache_dir):
    """clear(query=...) 采用**子串匹配**（设计意图：用户输入部分关键词模糊清理）。

    意图说明：'茅台' 子串会同时命中 '茅台' 和 '茅台2'，这是面向用户的友好行为，
    避免要求用户输入完整 query 字符串。如需精确匹配应在调用方自行实现。
    """
    for q in ("茅台", "腾讯", "茅台2"):
        k = cache.cache_key(q, "m")
        cache.put(k, {"content": q, "ts": _fresh_ts(), "query": q})
    cleared = cache.clear(query="茅台")
    assert cleared == 2  # "茅台" 和 "茅台2" 都匹配（子串语义）
    assert len(list(cache_dir.iterdir())) == 1


def test_clear_all_also_removes_tmp_residual(cache_dir):
    """clear(all=True) 顺手清理孤儿 .json.tmp 残留。

    模拟场景：上次进程崩溃在 put() 的 write_text 之后、os.replace 之前，
    留下 .json.tmp 孤儿。clear(all=True) 应一并清理。
    """
    # 手动构造一个孤儿 .tmp（模拟崩溃残留）
    residual = cache_dir / "deadbeef.json.tmp"
    residual.write_text('{"incomplete": true}', encoding="utf-8")
    # 同时放一个正常 .json
    k = cache.cache_key("q", "m")
    cache.put(k, {"content": "x", "ts": _fresh_ts()})
    assert len(list(cache_dir.iterdir())) == 2  # 1 个 .json + 1 个 .tmp
    cleared = cache.clear(all=True)
    assert cleared == 1  # 仅 .json 计入返回值
    assert len(list(cache_dir.iterdir())) == 0  # .tmp 也被清掉


def test_put_clears_existing_tmp(cache_dir):
    """put() 入口清理同 key 的 .tmp 残留，避免历史孤儿干扰本次写入。"""
    key = cache.cache_key("q", "m")
    # 手动构造同 key 的 .tmp 残留
    tmp = cache_dir / f"{key}.json.tmp"
    tmp.write_text('{"stale": true}', encoding="utf-8")
    cache.put(key, {"content": "fresh", "ts": _fresh_ts()})
    # put 后只剩 .json，无 .tmp
    files = list(cache_dir.iterdir())
    assert len(files) == 1
    assert files[0].suffix == ".json"
    got = cache.get(key, ttl_hours=24)
    assert got is not None and got["content"] == "fresh"


def test_list_recent(cache_dir):
    """history 返回最近条目，按 ts 倒序。"""
    # 用动态时间序列保证 ts1 < ts2 < ts3（始终满足排序语义，不依赖墙钟）
    import datetime as dt
    base = dt.datetime.now(dt.timezone.utc) - dt.timedelta(days=3)
    for i, q in enumerate(("a", "b", "c")):
        ts = (base + dt.timedelta(days=i)).isoformat()
        k = cache.cache_key(q, "m")
        cache.put(k, {
            "content": q,
            "ts": ts,
            "query": q,
        })
    items = cache.list_recent(limit=10)
    assert len(items) == 3
    # 按 ts 倒序，最新的 c 在前
    assert items[0]["query"] == "c"
