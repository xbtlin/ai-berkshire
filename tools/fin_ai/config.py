"""凭证加载：从环境变量或 .env 文件读取金融 AI 接口配置。

优先级：环境变量 > .env 文件。
缺关键字段时抛 ConfigError。
"""
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Optional


_DOTENV_PATH = Path(__file__).resolve().parents[2] / ".env"

# 必填字段：仅 base_url + auth_token。其余字段在 token-only 模式下网关自动解析
_REQUIRED_FIELDS = (
    ("FIN_AI_BASE_URL", "base_url"),
    ("FIN_AI_AUTH_TOKEN", "auth_token"),
)

# 可选字段：未填时使用默认值（空字符串或 model 默认名）
_OPTIONAL_FIELDS = (
    ("FIN_AI_UID", "uid", ""),
    ("FIN_AI_TENANT_ID", "tenant_id", ""),
    ("FIN_AI_PRODUCT_CODE", "product_code", ""),
    ("FIN_AI_CLIENT_CATEGORY", "client_category", ""),
    ("FIN_AI_MODEL", "model", "gangtise-reason"),
)


class ConfigError(Exception):
    """凭证缺失或格式错误。"""


@dataclass
class Config:
    base_url: str
    auth_token: str
    uid: str = ""
    tenant_id: str = ""
    product_code: str = ""
    client_category: str = ""
    model: str = "gangtise-reason"

    @classmethod
    def load(cls) -> "Config":
        """优先环境变量，其次 .env 文件。"""
        env = _load_dotenv()
        kwargs = {}
        missing = []
        for env_key, field in _REQUIRED_FIELDS:
            val = os.environ.get(env_key) or env.get(env_key)
            if not val:
                missing.append(env_key)
            else:
                kwargs[field] = val
        if missing:
            raise ConfigError(
                f"缺少金融 AI 凭证: {', '.join(missing)}；"
                f"参考 .env.example 配置 .env 文件"
            )
        for env_key, field, default in _OPTIONAL_FIELDS:
            val = os.environ.get(env_key) or env.get(env_key)
            kwargs[field] = val if val else default
        return cls(**kwargs)

    def headers(self) -> dict:
        """生成请求头。空字段跳过（token-only 模式下网关自动解析）。"""
        h = {
            "Authorization": _normalize_bearer(self.auth_token),
            "Content-Type": "application/json",
        }
        if self.uid:
            h["uid"] = self.uid
        if self.tenant_id:
            h["tenantid"] = self.tenant_id
        if self.product_code:
            h["productcode"] = self.product_code
        if self.client_category:
            h["clientcategory"] = self.client_category
        return h


def _normalize_bearer(token: str) -> str:
    """token 标准化为 Bearer 形式（兼容已含/不含 'Bearer ' 前缀，大小写不敏感）。"""
    if token.lower().startswith("bearer "):
        # 已含前缀，原样返回（保留原大小写）
        return token
    return f"Bearer {token}"


def _load_dotenv(path: Optional[Path] = None) -> dict:
    """简单解析 .env 文件，支持引号包裹的值（含 =）。"""
    dotenv_path = path if path is not None else _DOTENV_PATH
    if not dotenv_path.exists():
        return {}
    result = {}
    for line in dotenv_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if "=" not in line:
            continue
        k, _, v = line.partition("=")
        v = v.strip()
        # strip 一对首尾引号（双引号或单引号），保留中间字符
        if len(v) >= 2 and v[0] == v[-1] and v[0] in ('"', "'"):
            v = v[1:-1]
        result[k.strip()] = v
    return result
