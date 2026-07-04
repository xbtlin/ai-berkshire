"""config.py 单元测试：凭证加载与 headers 生成。"""
import os
import textwrap
from pathlib import Path

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
    monkeypatch.setattr("tools.fin_ai.config._DOTENV_PATH", Path("/nonexistent"))

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

    monkeypatch.setattr("tools.fin_ai.config._DOTENV_PATH", dotenv)

    cfg = Config.load()

    assert cfg.base_url == "http://dotenv:1234"
    assert cfg.uid == "du"
    assert cfg.model == "dm"


def test_dotenv_value_with_equals_sign(tmp_path, monkeypatch):
    """token 含 = 时（如 JWT/Base64）能正确解析，包括加引号的情况。"""
    dotenv = tmp_path / ".env"
    dotenv.write_text(
        'FIN_AI_AUTH_TOKEN="abc=def==ghi"\n'
        'FIN_AI_BASE_URL=http://x\n'
        'FIN_AI_UID=u\n'
        'FIN_AI_TENANT_ID=t\n'
        'FIN_AI_PRODUCT_CODE=p\n'
        'FIN_AI_CLIENT_CATEGORY=c\n'
        'FIN_AI_MODEL=m\n'
    )
    for k in ("FIN_AI_BASE_URL", "FIN_AI_UID", "FIN_AI_TENANT_ID",
             "FIN_AI_PRODUCT_CODE", "FIN_AI_CLIENT_CATEGORY",
             "FIN_AI_AUTH_TOKEN", "FIN_AI_MODEL"):
        monkeypatch.delenv(k, raising=False)
    monkeypatch.setattr("tools.fin_ai.config._DOTENV_PATH", dotenv)

    cfg = Config.load()
    assert cfg.auth_token == "abc=def==ghi"  # 不含引号，含等号


def test_env_takes_priority_over_dotenv(tmp_path, monkeypatch):
    """环境变量优先于 .env 文件。"""
    dotenv = tmp_path / ".env"
    dotenv.write_text("FIN_AI_UID=fromfile")
    monkeypatch.setenv("FIN_AI_UID", "fromenv")
    monkeypatch.setattr("tools.fin_ai.config._DOTENV_PATH", dotenv)
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
    monkeypatch.setattr("tools.fin_ai.config._DOTENV_PATH", Path("/nonexistent"))

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
    monkeypatch.setattr("tools.fin_ai.config._DOTENV_PATH", Path("/nonexistent"))

    cfg = Config.load()
    h = cfg.headers()

    assert h["uid"] == "u"
    assert h["tenantid"] == "t"
    assert h["productcode"] == "p"
    assert h["clientcategory"] == "c"
    assert h["Authorization"] == "Bearer abc123"
    assert h["Content-Type"] == "application/json"


def test_only_base_url_and_token_required(tmp_path, monkeypatch):
    """token-only 模式：仅 base_url + auth_token 必填，其余字段缺省；headers() 跳过空字段。"""
    dotenv = tmp_path / ".env"
    dotenv.write_text(
        "FIN_AI_BASE_URL=http://x\n"
        "FIN_AI_AUTH_TOKEN=tok\n"
    )
    for k in ("FIN_AI_BASE_URL", "FIN_AI_UID", "FIN_AI_TENANT_ID",
             "FIN_AI_PRODUCT_CODE", "FIN_AI_CLIENT_CATEGORY",
             "FIN_AI_AUTH_TOKEN", "FIN_AI_MODEL"):
        monkeypatch.delenv(k, raising=False)
    monkeypatch.setattr("tools.fin_ai.config._DOTENV_PATH", dotenv)

    cfg = Config.load()
    assert cfg.base_url == "http://x"
    assert cfg.auth_token == "tok"
    assert cfg.uid == ""
    assert cfg.tenant_id == ""
    assert cfg.product_code == ""
    assert cfg.client_category == ""
    assert cfg.model == "gangtise-reason"  # 默认值

    h = cfg.headers()
    assert "uid" not in h
    assert "tenantid" not in h
    assert "productcode" not in h
    assert "clientcategory" not in h
    assert h["Authorization"] == "Bearer tok"
    assert h["Content-Type"] == "application/json"


def test_auth_token_with_bearer_prefix(monkeypatch):
    """auth_token 已含 'Bearer ' 前缀时不再重复添加（兼容网关直发 token）。"""
    monkeypatch.setenv("FIN_AI_BASE_URL", "http://x")
    monkeypatch.setenv("FIN_AI_AUTH_TOKEN", "Bearer abc123")
    monkeypatch.setattr("tools.fin_ai.config._DOTENV_PATH", Path("/nonexistent"))

    cfg = Config.load()
    h = cfg.headers()
    assert h["Authorization"] == "Bearer abc123"  # 不是 "Bearer Bearer abc123"


def test_auth_token_case_insensitive_bearer(monkeypatch):
    """'bearer' 小写前缀也兼容。"""
    monkeypatch.setenv("FIN_AI_BASE_URL", "http://x")
    monkeypatch.setenv("FIN_AI_AUTH_TOKEN", "bearer xyz")
    monkeypatch.setattr("tools.fin_ai.config._DOTENV_PATH", Path("/nonexistent"))

    cfg = Config.load()
    h = cfg.headers()
    # 标准化为大写 Bearer
    assert h["Authorization"] in ("Bearer xyz", "bearer xyz")
