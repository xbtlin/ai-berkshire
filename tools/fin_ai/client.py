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
