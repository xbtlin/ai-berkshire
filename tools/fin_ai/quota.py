"""配额预检：调 GET /openai/chat/limit，返回剩余次数。

接口失败时降级返回 None（不阻塞调用，文档明确"容错返回 used=0"）。
"""
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
        resp = client.raw_get("/openai/chat/limit", timeout=10.0)
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
