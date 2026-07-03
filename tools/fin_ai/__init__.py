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
