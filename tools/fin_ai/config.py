"""凭证加载：从环境变量或 .env 文件读取金融 AI 接口配置。

优先级：环境变量 > .env 文件。
缺关键字段时抛 ConfigError。
"""
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Optional


_DOTENV_PATH = Path(__file__).resolve().parents[2] / ".env"

_REQUIRED_FIELDS = (
    ("FIN_AI_BASE_URL", "base_url"),
    ("FIN_AI_UID", "uid"),
    ("FIN_AI_TENANT_ID", "tenant_id"),
    ("FIN_AI_PRODUCT_CODE", "product_code"),
    ("FIN_AI_CLIENT_CATEGORY", "client_category"),
    ("FIN_AI_AUTH_TOKEN", "auth_token"),
    ("FIN_AI_MODEL", "model"),
)


class ConfigError(Exception):
    """凭证缺失或格式错误。"""


@dataclass
class Config:
    base_url: str
    uid: str
    tenant_id: str
    product_code: str
    client_category: str
    auth_token: str
    model: str

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
        return cls(**kwargs)

    def headers(self) -> dict:
        """生成请求头。"""
        return {
            "uid": self.uid,
            "tenantid": self.tenant_id,
            "productcode": self.product_code,
            "clientcategory": self.client_category,
            "Authorization": f"Bearer {self.auth_token}",
            "Content-Type": "application/json",
        }


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
