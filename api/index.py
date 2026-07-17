"""Vercel Function exposing the source-grounded Investor Council selector.

The API is intentionally read-only and stateless. It never accepts filesystem
paths, executes subprocesses, or fetches arbitrary URLs.
"""

from __future__ import annotations

import json
import sys
from http.server import BaseHTTPRequestHandler
from pathlib import Path
from typing import Any
from urllib.parse import parse_qs, urlsplit


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from tools.investor_council import (  # noqa: E402
    LibraryError,
    investor_index,
    load_library,
    require_valid_library,
    select_lenses,
)
from tools.investor_council_ja import (  # noqa: E402
    LocalizationError,
    localize_catalog,
    localize_profile,
    localize_selection,
)


MAX_BODY_BYTES = 16 * 1024
MAX_REQUEST_TARGET = 4096
MAX_LIST_ITEMS = 30
DISCLAIMER = (
    "公開資料に着想を得た分析レンズです。投資家本人の現在の見解、"
    "推奨、投資助言、将来収益の保証ではありません。"
)

LIBRARY = load_library(ROOT / "data" / "investor_philosophies.json")
require_valid_library(LIBRARY)
INVESTORS = investor_index(LIBRARY)


def _catalog() -> dict[str, Any]:
    return {
        "schema_version": LIBRARY["schema_version"],
        "reviewed_at": LIBRARY["reviewed_at"],
        "focus_taxonomy": LIBRARY["focus_taxonomy"],
        "scenarios": LIBRARY["scenarios"],
        "investors": [
            {
                "id": profile["id"],
                "name": profile["name"],
                "name_zh": profile["name_zh"],
                "school": profile["school"],
                "scope": profile["scope"],
                "summary": profile["summary"],
                "best_for": profile["best_for"],
                "source_count": len(profile["sources"]),
            }
            for profile in LIBRARY["investors"]
        ],
        "limits": {"max_lenses": 4, "request_body_bytes": MAX_BODY_BYTES},
        "disclaimer": DISCLAIMER,
    }


CATALOG_JA = localize_catalog(_catalog())
INVESTORS_JA = {
    investor_id: localize_profile(profile) for investor_id, profile in INVESTORS.items()
}


def _error_payload(code: str, message: str) -> dict[str, Any]:
    return {"error": {"code": code, "message": message}}


def _string_field(payload: dict[str, Any], name: str, default: str) -> str:
    value = payload.get(name, default)
    if not isinstance(value, str) or not value.strip() or len(value) > 80:
        raise ValueError(f"{name} は1〜80文字の文字列で指定してください")
    return value.strip()


def _string_list(payload: dict[str, Any], name: str) -> list[str]:
    value = payload.get(name, [])
    if not isinstance(value, list) or len(value) > MAX_LIST_ITEMS:
        raise ValueError(f"{name} は最大{MAX_LIST_ITEMS}件の配列で指定してください")
    cleaned: list[str] = []
    for item in value:
        if not isinstance(item, str) or not item.strip() or len(item) > 80:
            raise ValueError(f"{name} の各要素は1〜80文字の文字列にしてください")
        cleaned.append(item.strip())
    return list(dict.fromkeys(cleaned))


def _selection_from_payload(payload: Any) -> dict[str, Any]:
    if not isinstance(payload, dict):
        raise ValueError("JSONのトップレベルはobjectにしてください")

    allowed = {"scenario", "focus_tags", "lenses", "limit"}
    unknown = sorted(set(payload) - allowed)
    if unknown:
        raise ValueError("未対応フィールド: " + ", ".join(unknown))

    scenario = _string_field(payload, "scenario", "company")
    focus_tags = _string_list(payload, "focus_tags")
    lenses = _string_list(payload, "lenses")
    limit = payload.get("limit", 4)
    if isinstance(limit, bool) or not isinstance(limit, int) or not 1 <= limit <= 4:
        raise ValueError("limit は1〜4の整数にしてください")
    if scenario not in LIBRARY["scenarios"]:
        raise ValueError(f"未対応のシナリオです: {scenario}")
    unknown_focus = sorted(set(focus_tags) - set(LIBRARY["focus_taxonomy"]))
    if unknown_focus:
        raise ValueError("未対応の関心軸です: " + ", ".join(unknown_focus))
    unknown_lenses = sorted(set(lenses) - set(INVESTORS))
    if unknown_lenses:
        raise ValueError("未対応の投資家レンズです: " + ", ".join(unknown_lenses))
    if len(lenses) > limit:
        raise ValueError("明示する投資家レンズ数はlimit以下にしてください")

    return localize_selection(
        select_lenses(
            LIBRARY,
            scenario_id=scenario,
            focus_tags=focus_tags,
            explicit_ids=lenses,
            limit=limit,
        )
    )


class handler(BaseHTTPRequestHandler):
    """Vercel Python runtime entry point."""

    server_version = "AI-Berkshire"
    sys_version = ""

    def _security_headers(self) -> None:
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("X-Frame-Options", "DENY")
        self.send_header("Referrer-Policy", "strict-origin-when-cross-origin")
        self.send_header("Permissions-Policy", "camera=(), microphone=(), geolocation=()")
        self.send_header("Cache-Control", "no-store")

    def _send_json(
        self, payload: dict[str, Any], status: int = 200, *, include_body: bool = True
    ) -> None:
        body = json.dumps(payload, ensure_ascii=False, separators=(",", ":")).encode(
            "utf-8"
        )
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self._security_headers()
        self.end_headers()
        if include_body:
            self.wfile.write(body)

    def _send_api_error(
        self, status: int, code: str, message: str, *, include_body: bool = True
    ) -> None:
        self._send_json(
            _error_payload(code, message), status=status, include_body=include_body
        )

    def _query(self) -> tuple[str, dict[str, list[str]]]:
        if len(self.path) > MAX_REQUEST_TARGET:
            raise OverflowError("request target too long")
        parsed = urlsplit(self.path)
        params = parse_qs(
            parsed.query, keep_blank_values=True, strict_parsing=False, max_num_fields=32
        )
        view = params.get("view", ["meta"])[-1]
        return view, params

    def _handle_get(self, *, include_body: bool) -> None:
        try:
            view, params = self._query()
        except OverflowError:
            self._send_api_error(
                414, "request_too_long", "リクエストURLが長すぎます", include_body=include_body
            )
            return
        except ValueError:
            self._send_api_error(
                400, "invalid_query", "クエリ文字列を解析できません", include_body=include_body
            )
            return

        if view == "health":
            self._send_json(
                {
                    "status": "ok",
                    "schema_version": LIBRARY["schema_version"],
                    "reviewed_at": LIBRARY["reviewed_at"],
                },
                include_body=include_body,
            )
            return
        if view == "meta":
            self._send_json(CATALOG_JA, include_body=include_body)
            return
        if view == "investor":
            investor_id = params.get("id", [""])[-1].strip()
            profile = INVESTORS_JA.get(investor_id)
            if profile is None:
                self._send_api_error(
                    404,
                    "investor_not_found",
                    "指定された投資家レンズはありません",
                    include_body=include_body,
                )
                return
            self._send_json(
                {"data": profile, "disclaimer": DISCLAIMER},
                include_body=include_body,
            )
            return

        self._send_api_error(
            404, "not_found", "指定されたAPI viewはありません", include_body=include_body
        )

    def do_GET(self) -> None:  # noqa: N802
        self._handle_get(include_body=True)

    def do_HEAD(self) -> None:  # noqa: N802
        self._handle_get(include_body=False)

    def do_POST(self) -> None:  # noqa: N802
        try:
            view, _ = self._query()
        except OverflowError:
            self._send_api_error(414, "request_too_long", "リクエストURLが長すぎます")
            return
        except ValueError:
            self._send_api_error(400, "invalid_query", "クエリ文字列を解析できません")
            return

        if view != "select":
            self._send_api_error(404, "not_found", "指定されたAPI viewはありません")
            return

        content_type = self.headers.get("Content-Type", "").split(";", 1)[0].strip()
        if content_type != "application/json":
            self._send_api_error(
                415, "unsupported_media_type", "Content-Typeはapplication/jsonにしてください"
            )
            return

        try:
            content_length = int(self.headers.get("Content-Length", "0"))
        except ValueError:
            self._send_api_error(400, "invalid_content_length", "Content-Lengthが不正です")
            return
        if content_length < 0 or content_length > MAX_BODY_BYTES:
            self._send_api_error(
                413,
                "payload_too_large",
                f"リクエスト本文は{MAX_BODY_BYTES} bytes以下にしてください",
            )
            return

        try:
            payload = json.loads(self.rfile.read(content_length).decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError):
            self._send_api_error(400, "invalid_json", "有効なUTF-8 JSONを送信してください")
            return

        try:
            selection = _selection_from_payload(payload)
        except LocalizationError:
            self._send_api_error(
                500,
                "localization_error",
                "日本語表示データを準備できませんでした",
            )
            return
        except (ValueError, LibraryError) as exc:
            self._send_api_error(422, "invalid_selection", str(exc))
            return

        self._send_json({"data": selection, "disclaimer": DISCLAIMER})

    def do_OPTIONS(self) -> None:  # noqa: N802
        self.send_response(204)
        self.send_header("Allow", "GET, HEAD, POST, OPTIONS")
        self._security_headers()
        self.end_headers()

    def _method_not_allowed(self) -> None:
        self.send_response(405)
        self.send_header("Allow", "GET, HEAD, POST, OPTIONS")
        self.send_header("Content-Length", "0")
        self._security_headers()
        self.end_headers()

    do_DELETE = _method_not_allowed
    do_PATCH = _method_not_allowed
    do_PUT = _method_not_allowed
