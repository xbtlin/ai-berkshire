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
