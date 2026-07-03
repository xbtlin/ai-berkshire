"""config.py 单元测试：凭证加载与 headers 生成。"""
import os
import textwrap
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
    monkeypatch.setattr("tools.fin_ai.config._DOTENV_PATH", "/nonexistent")

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

    monkeypatch.setattr("tools.fin_ai.config._DOTENV_PATH", str(dotenv))

    cfg = Config.load()

    assert cfg.base_url == "http://dotenv:1234"
    assert cfg.uid == "du"
    assert cfg.model == "dm"


def test_env_takes_priority_over_dotenv(tmp_path, monkeypatch):
    """环境变量优先于 .env 文件。"""
    dotenv = tmp_path / ".env"
    dotenv.write_text("FIN_AI_UID=fromfile")
    monkeypatch.setenv("FIN_AI_UID", "fromenv")
    monkeypatch.setattr("tools.fin_ai.config._DOTENV_PATH", str(dotenv))
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
    monkeypatch.setattr("tools.fin_ai.config._DOTENV_PATH", "/nonexistent")

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
    monkeypatch.setattr("tools.fin_ai.config._DOTENV_PATH", "/nonexistent")

    cfg = Config.load()
    h = cfg.headers()

    assert h["uid"] == "u"
    assert h["tenantid"] == "t"
    assert h["productcode"] == "p"
    assert h["clientcategory"] == "c"
    assert h["Authorization"] == "Bearer abc123"
    assert h["Content-Type"] == "application/json"
