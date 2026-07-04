"""HTTP + SSE 客户端：封装 /openai/chat，处理增量拼接、错误码、网络重试。

外部 API:
    FinAIClient(config, transport=None, retry_delay=2)
        .chat(query, conversation_sid=None, on_delta=None, timeout=120) -> ChatResult

错误处理见 spec §5.1。
"""
import json
import logging
import time
import uuid
from dataclasses import dataclass, field
from typing import Callable, Optional

import httpx

_logger = logging.getLogger(__name__)


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

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()

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
                    _logger.warning("[RETRY] HTTP %s", e.response.status_code)
                    # 注：固定间隔，无指数退避。生产场景如需 backoff，可扩展 retry_delay 为 callable。
                    # 测试时通过 retry_delay=0 跳过等待。
                    time.sleep(self.retry_delay)
                    continue
                raise
            except (httpx.ConnectError, httpx.TimeoutException) as e:
                last_exc = e
                if attempt == 1:
                    _logger.warning("[RETRY] %s", type(e).__name__)
                    # 注：固定间隔，无指数退避。生产场景如需 backoff，可扩展 retry_delay 为 callable。
                    # 测试时通过 retry_delay=0 跳过等待。
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
                    continue
                if line.startswith(":"):  # SSE 注释（如 :heartbeat）
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
                # 优先用 data 内的 type 字段（实际服务端格式），其次 SSE event: 头（兼容旧 mock）
                event_type = data.get("type") or current_event or ""
                raw_events.append({"event": event_type, "data": data})
                if "errorCode" in data:
                    stream.read()  # 消费剩余 body，避免 keep-alive 告警
                    raise FinAIError(data["errorCode"], data.get("errorMsg", ""))
                if event_type == "response.output_text.delta":
                    delta = data.get("delta", "")
                    if delta:
                        content_parts.append(delta)
                        if on_delta:
                            on_delta(delta)
                elif event_type == "response.completed":
                    usage = data.get("response", {}).get("usage", {})

        return ChatResult(
            content="".join(content_parts),
            session_id=session_id,
            conversation_sid=sid,
            usage=usage,
            raw_events=raw_events,
        )

    def raw_get(self, path: str, timeout: float = 10.0) -> httpx.Response:
        """发起 GET 请求（公共 API，供其他模块复用，如 quota.pre_check）。

        Args:
            path: 相对路径（如 "/openai/chat/limit"），会拼到 base_url 后
            timeout: 超时秒数
        Returns:
            httpx.Response
        """
        return self._client.get(
            f"{self.config.base_url}{path}",
            headers=self.config.headers(),
            timeout=timeout,
        )

    def close(self):
        self._client.close()
