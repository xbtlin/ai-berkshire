#!/usr/bin/env python3
"""Fetch date-bounded US stock sentiment from the Adanos API.

The command is an optional evidence source for ``news-pulse``. It has no
third-party dependencies and never treats sentiment as an investment signal.

Example:
    python3 tools/adanos_sentiment.py \
        --ticker AAPL --source reddit \
        --from-date 2026-07-15 --to-date 2026-07-29
"""

from __future__ import annotations

import argparse
import http.client
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import date


_API_BASE = "https://api.adanos.org"
_SOURCES = ("reddit", "x", "news", "polymarket")
_TICKER_RE = re.compile(
    r"(?:[A-Z0-9]{1,8}[.-][A-Z]|(?=[A-Z0-9]{1,10}$)(?=.*[A-Z])[A-Z0-9]+|[0-9]{3,10})"
)
_TIMEOUT = 30


class AdanosSentimentError(Exception):
    """Raised for safe, user-facing Adanos request failures."""


class _RejectRedirects(urllib.request.HTTPRedirectHandler):
    """Keep the authentication header on the configured Adanos origin only."""

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        raise urllib.error.HTTPError(req.full_url, code, msg, headers, fp)


_OPENER = urllib.request.build_opener(_RejectRedirects())


def normalize_ticker(value: str) -> str:
    """Normalize and validate a stock ticker accepted by the Adanos API."""
    ticker = value.strip().removeprefix("$").upper()
    if not _TICKER_RE.fullmatch(ticker):
        raise ValueError(
            "ticker must be 1-10 alphanumeric characters, an exchange-style "
            "symbol such as BRK.B, or a 3-10 digit identifier"
        )
    return ticker


def parse_iso_date(value: str) -> date:
    """Parse a strict ISO calendar date for a reproducible UTC window."""
    try:
        parsed = date.fromisoformat(value)
    except ValueError as exc:
        raise ValueError("dates must use YYYY-MM-DD") from exc
    if parsed.isoformat() != value:
        raise ValueError("dates must use YYYY-MM-DD")
    return parsed


def build_request(
    ticker: str,
    source: str,
    from_date: str,
    to_date: str,
    auth_value: str,
) -> urllib.request.Request:
    """Build an authenticated request without placing the key in the URL."""
    normalized_ticker = normalize_ticker(ticker)
    if source not in _SOURCES:
        raise ValueError(f"source must be one of: {', '.join(_SOURCES)}")

    start = parse_iso_date(from_date)
    end = parse_iso_date(to_date)
    if start > end:
        raise ValueError("from-date must be on or before to-date")

    query = urllib.parse.urlencode({"from": from_date, "to": to_date})
    path_ticker = urllib.parse.quote(normalized_ticker, safe=".-")
    url = f"{_API_BASE}/{source}/stocks/v1/stock/{path_ticker}?{query}"
    request = urllib.request.Request(
        url,
        headers={
            "Accept": "application/json",
            "User-Agent": "ai-berkshire-news-pulse/1.0",
        },
    )
    request.add_header("X-API-Key", auth_value)
    return request


def fetch_sentiment(
    ticker: str,
    source: str,
    from_date: str,
    to_date: str,
    auth_value: str,
) -> dict:
    """Fetch one source and return provider data with explicit limitations."""
    request = build_request(ticker, source, from_date, to_date, auth_value)
    try:
        with _OPENER.open(request, timeout=_TIMEOUT) as response:
            payload = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        request_id = exc.headers.get("X-Request-ID") if exc.headers else None
        suffix = f" (request ID: {request_id})" if request_id else ""
        raise AdanosSentimentError(
            f"Adanos request failed with HTTP {exc.code}{suffix}"
        ) from exc
    except urllib.error.URLError as exc:
        raise AdanosSentimentError(f"Adanos network request failed: {exc.reason}") from exc
    except TimeoutError as exc:
        raise AdanosSentimentError("Adanos request timed out") from exc
    except (OSError, http.client.HTTPException) as exc:
        raise AdanosSentimentError("Adanos response body could not be read") from exc
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise AdanosSentimentError("Adanos returned an invalid JSON response") from exc

    if not isinstance(payload, dict):
        raise AdanosSentimentError("Adanos returned an unexpected response shape")

    return {
        "provider": "Adanos Market Sentiment API",
        "source": source,
        "ticker": normalize_ticker(ticker),
        "window": {"from": from_date, "to": to_date, "timezone": "UTC"},
        "data": payload,
        "limitations": [
            "Sentiment is supplementary evidence, not an investment recommendation.",
            "Sparse source coverage must be disclosed and corroborated with primary sources.",
        ],
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Fetch one date-bounded Adanos stock sentiment source."
    )
    parser.add_argument("--ticker", required=True, help="US stock ticker, e.g. AAPL")
    parser.add_argument("--source", required=True, choices=_SOURCES)
    parser.add_argument("--from-date", required=True, help="Inclusive UTC date, YYYY-MM-DD")
    parser.add_argument("--to-date", required=True, help="Inclusive UTC date, YYYY-MM-DD")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    auth_value = os.environ.get("ADANOS_API_KEY", "").strip()
    if not auth_value:
        print(
            "ADANOS_API_KEY is not set; continue news-pulse without Adanos evidence.",
            file=sys.stderr,
        )
        return 2

    try:
        result = fetch_sentiment(
            args.ticker,
            args.source,
            args.from_date,
            args.to_date,
            auth_value,
        )
    except (AdanosSentimentError, ValueError) as exc:
        print(f"Unable to fetch Adanos sentiment: {exc}", file=sys.stderr)
        return 1

    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
