from __future__ import annotations

import json
import threading
import unittest
import urllib.error
import urllib.request
from http.server import ThreadingHTTPServer
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

from api.index import MAX_BODY_BYTES, handler  # noqa: E402


class QuietHandler(handler):
    def log_message(self, format: str, *args) -> None:
        return


class WebApiTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.server = ThreadingHTTPServer(("127.0.0.1", 0), QuietHandler)
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()
        cls.base = f"http://127.0.0.1:{cls.server.server_port}"

    @classmethod
    def tearDownClass(cls) -> None:
        cls.server.shutdown()
        cls.server.server_close()
        cls.thread.join(timeout=2)

    def request(self, path: str, *, method: str = "GET", payload=None, headers=None):
        data = None if payload is None else json.dumps(payload).encode("utf-8")
        request_headers = dict(headers or {})
        if payload is not None:
            request_headers.setdefault("Content-Type", "application/json")
        request = urllib.request.Request(
            self.base + path,
            data=data,
            headers=request_headers,
            method=method,
        )
        try:
            response = urllib.request.urlopen(request, timeout=3)
        except urllib.error.HTTPError as exc:
            response = exc
        body = response.read()
        parsed = json.loads(body.decode("utf-8")) if body else None
        return response.status, response.headers, parsed

    def test_health_and_security_headers(self) -> None:
        status, headers, payload = self.request("/api?view=health")
        self.assertEqual(200, status)
        self.assertEqual("ok", payload["status"])
        self.assertEqual("nosniff", headers["X-Content-Type-Options"])
        self.assertEqual("DENY", headers["X-Frame-Options"])
        self.assertEqual("no-store", headers["Cache-Control"])

    def test_catalog_has_expected_counts(self) -> None:
        status, _, payload = self.request("/api?view=meta")
        self.assertEqual(200, status)
        self.assertEqual(11, len(payload["investors"]))
        self.assertEqual(7, len(payload["scenarios"]))
        self.assertEqual(30, len(payload["focus_taxonomy"]))
        self.assertNotIn("sources", payload["investors"][0])
        self.assertEqual(4, payload["limits"]["max_lenses"])
        self.assertEqual("事業の質", payload["focus_taxonomy"]["business_quality"])
        self.assertEqual("企業", payload["scope_labels"]["company"])
        self.assertEqual("一次資料", payload["source_kind_labels"]["primary"])
        self.assertTrue(payload["investors"][0]["name_ja"])
        self.assertTrue(payload["investors"][0]["school_ja"])

    def test_selection_reuses_focus_coverage_rules(self) -> None:
        status, _, payload = self.request(
            "/api?view=select",
            method="POST",
            payload={
                "scenario": "company",
                "focus_tags": ["passive"],
                "lenses": [],
                "limit": 4,
            },
        )
        self.assertEqual(200, status)
        selected = [lens["id"] for lens in payload["data"]["selected_lenses"]]
        self.assertIn("john-bogle", selected)
        self.assertEqual([], payload["data"]["uncovered_focus_tags"])
        self.assertEqual([], payload["data"]["uncovered_focus_tags_ja"])
        self.assertEqual("上場企業1社の事業の質・価格・リスクを調査", payload["data"]["scenario_description"])
        self.assertTrue(payload["data"]["selected_lenses"][0]["name_ja"])
        self.assertTrue(payload["data"]["selected_lenses"][0]["school_ja"])
        self.assertIn("投資助言", payload["disclaimer"])

    def test_invalid_selection_is_fail_closed(self) -> None:
        cases = (
            {"scenario": "unknown", "focus_tags": [], "lenses": [], "limit": 4},
            {"scenario": "company", "focus_tags": ["not_a_tag"], "lenses": [], "limit": 4},
            {"scenario": "company", "focus_tags": [], "lenses": [], "limit": True},
            {"scenario": "company", "focus_tags": [], "lenses": [], "limit": 5},
            {"scenario": "company", "focus_tags": [], "lenses": [], "limit": 4, "path": "/tmp/x"},
        )
        for payload in cases:
            with self.subTest(payload=payload):
                status, _, body = self.request(
                    "/api?view=select", method="POST", payload=payload
                )
                self.assertEqual(422, status)
                self.assertEqual("invalid_selection", body["error"]["code"])

    def test_body_and_media_type_limits(self) -> None:
        status, _, payload = self.request(
            "/api?view=select",
            method="POST",
            payload=None,
            headers={"Content-Type": "text/plain"},
        )
        self.assertEqual(415, status)
        self.assertEqual("unsupported_media_type", payload["error"]["code"])

        request = urllib.request.Request(
            self.base + "/api?view=select",
            data=b"x" * (MAX_BODY_BYTES + 1),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with self.assertRaises(urllib.error.HTTPError) as caught:
            urllib.request.urlopen(request, timeout=3)
        self.assertEqual(413, caught.exception.code)

    def test_unknown_routes_and_methods_are_rejected(self) -> None:
        status, _, payload = self.request("/api?view=missing")
        self.assertEqual(404, status)
        self.assertEqual("not_found", payload["error"]["code"])

        status, headers, payload = self.request("/api?view=meta", method="PUT")
        self.assertEqual(405, status)
        self.assertEqual("GET, HEAD, POST, OPTIONS", headers["Allow"])
        self.assertIsNone(payload)

    def test_investor_profile_endpoint(self) -> None:
        status, _, payload = self.request("/api?view=investor&id=howard-marks")
        self.assertEqual(200, status)
        self.assertEqual("howard-marks", payload["data"]["id"])
        self.assertEqual("ハワード・マークス", payload["data"]["name_ja"])
        self.assertEqual("一次資料", payload["data"]["sources"][0]["kind_ja"])
        self.assertTrue(payload["data"]["sources"])


class StaticDeploymentTests(unittest.TestCase):
    def test_vercel_config_and_static_assets(self) -> None:
        config = json.loads((ROOT / "vercel.json").read_text(encoding="utf-8"))
        self.assertIsNone(config["framework"])
        self.assertEqual("public", config["outputDirectory"])
        self.assertIn("api/index.py", config["functions"])
        self.assertIn("reports/**", config["functions"]["api/index.py"]["excludeFiles"])
        csp = config["headers"][0]["headers"][0]["value"]
        self.assertIn("default-src 'self'", csp)
        self.assertIn("frame-ancestors 'none'", csp)

        html = (ROOT / "public" / "index.html").read_text(encoding="utf-8")
        self.assertIn('src="/app.js"', html)
        self.assertIn('href="/styles.css"', html)
        self.assertNotIn("<script>", html)
        self.assertTrue((ROOT / "public" / "app.js").is_file())
        self.assertTrue((ROOT / "public" / "styles.css").is_file())


if __name__ == "__main__":
    unittest.main()
