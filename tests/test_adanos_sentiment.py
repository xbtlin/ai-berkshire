#!/usr/bin/env python3
"""Regression tests for the optional Adanos news-pulse adapter."""

import io
import http.client
import json
import os
import sys
import unittest
import urllib.error
from contextlib import redirect_stderr
from unittest import mock


sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "tools"))

import adanos_sentiment as A  # noqa: E402


class FakeResponse:
    def __init__(self, payload):
        self.payload = payload

    def __enter__(self):
        return self

    def __exit__(self, *_args):
        return False

    def read(self):
        return json.dumps(self.payload).encode("utf-8")


class FailingResponse(FakeResponse):
    def read(self):
        raise http.client.IncompleteRead(b'{"ticker":')


class TestValidation(unittest.TestCase):
    def test_normalizes_supported_tickers(self):
        self.assertEqual(A.normalize_ticker("$aapl"), "AAPL")
        self.assertEqual(A.normalize_ticker(" brk.b "), "BRK.B")
        self.assertEqual(A.normalize_ticker("0050"), "0050")

    def test_rejects_ambiguous_or_malformed_tickers(self):
        for ticker in ("", "12", "BRK/B", "AAPL?days=30", "TOO-LONG.T"):
            with self.subTest(ticker=ticker), self.assertRaises(ValueError):
                A.normalize_ticker(ticker)

    def test_rejects_invalid_or_reversed_dates(self):
        with self.assertRaisesRegex(ValueError, "YYYY-MM-DD"):
            A.build_request("AAPL", "reddit", "07/01/2026", "2026-07-29", "key")
        with self.assertRaisesRegex(ValueError, "on or before"):
            A.build_request("AAPL", "reddit", "2026-07-30", "2026-07-29", "key")


class TestRequest(unittest.TestCase):
    @mock.patch("adanos_sentiment._OPENER.open")
    def test_fetches_bounded_window_without_deprecated_days(self, open_request):
        open_request.return_value = FakeResponse({"ticker": "AAPL", "mentions": 12})

        result = A.fetch_sentiment(
            "$aapl", "reddit", "2026-07-15", "2026-07-29", "secret-key"
        )

        request = open_request.call_args.args[0]
        self.assertEqual(
            request.full_url,
            "https://api.adanos.org/reddit/stocks/v1/stock/AAPL?"
            "from=2026-07-15&to=2026-07-29",
        )
        self.assertNotIn("days=", request.full_url)
        self.assertNotIn("secret-key", request.full_url)
        self.assertEqual(request.get_header("X-api-key"), "secret-key")
        self.assertEqual(open_request.call_args.kwargs["timeout"], 30)
        self.assertEqual(result["data"]["mentions"], 12)
        self.assertEqual(result["window"]["timezone"], "UTC")
        self.assertIn("not an investment recommendation", result["limitations"][0])

    @mock.patch("adanos_sentiment._OPENER.open")
    def test_http_error_is_sanitized_and_keeps_request_id(self, open_request):
        open_request.side_effect = urllib.error.HTTPError(
            "https://api.adanos.org/test",
            429,
            "secret-key appeared upstream",
            {"X-Request-ID": "req-123"},
            io.BytesIO(b'{"detail":"secret-key"}'),
        )

        with self.assertRaises(A.AdanosSentimentError) as context:
            A.fetch_sentiment(
                "AAPL", "news", "2026-07-15", "2026-07-29", "secret-key"
            )

        message = str(context.exception)
        self.assertIn("HTTP 429", message)
        self.assertIn("req-123", message)
        self.assertNotIn("secret-key", message)

    @mock.patch("adanos_sentiment._OPENER.open")
    def test_rejects_non_object_response(self, open_request):
        open_request.return_value = FakeResponse([])
        with self.assertRaisesRegex(A.AdanosSentimentError, "response shape"):
            A.fetch_sentiment(
                "AAPL", "x", "2026-07-15", "2026-07-29", "secret-key"
            )

    def test_redirect_handler_refuses_to_forward_authentication(self):
        request = urllib.request.Request("https://api.adanos.org/test")
        with self.assertRaises(urllib.error.HTTPError) as context:
            A._RejectRedirects().redirect_request(
                request,
                io.BytesIO(),
                302,
                "Found",
                {"Location": "https://example.com/capture"},
                "https://example.com/capture",
            )
        self.assertEqual(context.exception.url, "https://api.adanos.org/test")

    @mock.patch("adanos_sentiment._OPENER.open")
    def test_response_read_failure_is_sanitized(self, open_request):
        open_request.return_value = FailingResponse(None)
        with self.assertRaisesRegex(A.AdanosSentimentError, "could not be read"):
            A.fetch_sentiment(
                "AAPL", "polymarket", "2026-07-15", "2026-07-29", "secret-key"
            )


class TestCli(unittest.TestCase):
    def test_missing_key_is_an_optional_skip(self):
        stderr = io.StringIO()
        with mock.patch.dict(os.environ, {}, clear=True), redirect_stderr(stderr):
            status = A.main(
                [
                    "--ticker",
                    "AAPL",
                    "--source",
                    "reddit",
                    "--from-date",
                    "2026-07-15",
                    "--to-date",
                    "2026-07-29",
                ]
            )

        self.assertEqual(status, 2)
        self.assertIn("continue news-pulse without Adanos", stderr.getvalue())


if __name__ == "__main__":
    unittest.main(verbosity=2)
