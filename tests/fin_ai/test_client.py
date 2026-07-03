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
    with FinAIClient(fake_config, transport=transport) as client:
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
    with FinAIClient(fake_config, transport=transport) as client:
        result = client.chat("问")
    assert result.content == "答"


def test_daily_limit_exceeded(fake_config):
    """SSE 返回 daily_limit_exceeded → raise FinAIError，不重试。"""
    events = [
        ("error", {"errorCode": "daily_limit_exceeded", "errorMsg": "当日次数已达上限"}),
    ]
    transport = _mock_transport(events)
    with FinAIClient(fake_config, transport=transport) as client:
        with pytest.raises(FinAIError) as exc:
            client.chat("问")
    assert "daily_limit_exceeded" in str(exc.value)


def test_reconnect_expired_no_retry(fake_config):
    """reconnect_expired → 不重试，直接 raise。"""
    events = [
        ("error", {"errorCode": "reconnect_expired", "errorMsg": "会话不存在"}),
    ]
    transport = _mock_transport(events)
    with FinAIClient(fake_config, transport=transport) as client:
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
    with FinAIClient(fake_config, transport=transport) as client:
        result = client.chat("问")
    assert result.content == "正常"


def test_conversation_sid_auto_generated(fake_config):
    """conversation_sid 未传时自动生成 uuid4。"""
    events = [
        ("response.completed", {"response": {"usage": {"total_tokens": 1}}}),
    ]
    transport = _mock_transport(events)
    with FinAIClient(fake_config, transport=transport) as client:
        result = client.chat("问")
    assert result.conversation_sid  # 非空
    assert len(result.conversation_sid) == 36  # uuid4 长度


def test_conversation_sid_reused(fake_config):
    """传入 conversation_sid 时复用。"""
    events = [
        ("response.completed", {"response": {"usage": {"total_tokens": 1}}}),
    ]
    transport = _mock_transport(events)
    with FinAIClient(fake_config, transport=transport) as client:
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
    with FinAIClient(fake_config, transport=transport, retry_delay=0) as client:
        result = client.chat("问")
    assert call_count["n"] == 2
    assert isinstance(result, ChatResult)


def test_5xx_retry_then_success(fake_config):
    """HTTP 5xx 首次失败，重试 1 次成功。"""
    events = [
        ("response.completed", {"response": {"usage": {"total_tokens": 1}}}),
    ]
    body = "\n".join(_sse_lines(events)).encode("utf-8")

    call_count = {"n": 0}

    def handler(request):
        call_count["n"] += 1
        if call_count["n"] == 1:
            return httpx.Response(503, content="service unavailable")
        return httpx.Response(200, headers={"Content-Type": "text/event-stream"},
                              content=body)

    transport = httpx.MockTransport(handler)
    with FinAIClient(fake_config, transport=transport, retry_delay=0) as client:
        result = client.chat("问")
    assert call_count["n"] == 2
    assert isinstance(result, ChatResult)
