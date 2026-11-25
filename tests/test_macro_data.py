#!/usr/bin/env python3
"""macro_data.py 回归测试（不联网，urlopen 被替换为本地假响应；数值仅为测试样例）。

运行：  python tests/test_macro_data.py
"""

import contextlib
import io
import json
import os
import sys
import unittest
import urllib.error
import urllib.parse
from datetime import date
from unittest import mock

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'tools'))

import macro_data as M  # noqa: E402


class _Resp(io.BytesIO):
    def __enter__(self):
        return self

    def __exit__(self, *exc):
        return False


def _fake_api(routes, seen):
    """按路径前缀返回假 JSON；未登记的路径返回 404。"""
    def urlopen(req, timeout=None):
        seen.append(req)
        path = req.full_url.split('/v1', 1)[1].split('?')[0]
        if path not in routes:
            raise urllib.error.HTTPError(req.full_url, 404, 'Not Found', {}, None)
        body = routes[path]
        if isinstance(body, int):
            raise urllib.error.HTTPError(req.full_url, body, 'Forbidden', {}, None)
        return _Resp(json.dumps(body).encode('utf-8'))
    return urlopen


CATALOGUE = {
    'policy_rate': {'name': 'Policy Rate', 'unit': '%', 'frequency': 'Irregular'},
    'inflation': {'name': 'Inflation', 'unit': '%YoY', 'frequency': 'Monthly'},
}
ROUTES = {
    '/data_catalogue/usd': CATALOGUE,
    '/announcements/usd/policy_rate': {'data': [
        {'date': '2026-09-17', 'val': 1.5}, {'date': '2026-07-30', 'val': 1.75}]},
    '/announcements/usd/inflation': {'data': [
        {'date': '2026-09-01', 'val': 2.2, 'previous_value': 2.4}]},
    '/calendar/usd': {'data': [
        {'announcement_datetime': 1792845000, 'release': 'inflation', 'time_announced': True},
        {'announcement_date': '2026-11-02', 'release': 'gdp', 'time_announced': False}]},
}


class MacroDataTest(unittest.TestCase):

    def run_cmd(self, fn, *args, routes=ROUTES, key=None):
        seen, out = [], io.StringIO()
        env = {'FXMACRODATA_API_KEY': key} if key else {}
        with mock.patch.dict(os.environ, env, clear=False), \
                mock.patch.object(M, '_KEY_FILE', '/nonexistent/key.txt'), \
                mock.patch.object(M.urllib.request, 'urlopen', _fake_api(routes, seen)), \
                contextlib.redirect_stdout(out):
            if not key:
                os.environ.pop('FXMACRODATA_API_KEY', None)
            fn(*args)
        return out.getvalue(), seen

    def test_snapshot_only_requests_catalogued_indicators(self):
        text, seen = self.run_cmd(M.cmd_snapshot, 'usd')
        paths = [r.full_url.split('/v1', 1)[1].split('?')[0] for r in seen]
        self.assertNotIn('/announcements/usd/gdp', paths)
        self.assertIn('1.5', text)
        self.assertIn('1.75', text)
        self.assertIn('2.4', text)      # 只有一期时用 previous_value
        self.assertIn('2026-10-24 12:30 UTC', text)
        self.assertIn('2026-11-02 (时间未公布)', text)

    def test_key_goes_in_header_not_url(self):
        _, seen = self.run_cmd(M.cmd_indicator, 'usd', 'inflation', 3, key='test-key')
        for req in seen:
            self.assertNotIn('test-key', req.full_url)
            self.assertEqual(req.get_header('X-api-key'), 'test-key')

    def test_keyless_non_usd_explains_subscription(self):
        routes = dict(ROUTES, **{'/announcements/eur/inflation': 403})
        with self.assertRaises(ConnectionError) as ctx:
            self.run_cmd(M.cmd_indicator, 'eur', 'inflation', 3, routes=routes)
        self.assertIn('USD', str(ctx.exception))

    def test_fx_one_year_change(self):
        calls = []

        def answers(req, timeout=None):
            calls.append(req.full_url)
            val = 100.0 if 'end_date' in req.full_url else 110.0
            return _Resp(json.dumps({'data': [{'date': '2025-10-14', 'val': val}]}).encode())
        out = io.StringIO()
        with mock.patch.object(M.urllib.request, 'urlopen', answers), \
                contextlib.redirect_stdout(out):
            M.cmd_fx('usd', 'jpy')
        self.assertEqual(len(calls), 2)
        self.assertIn('+10.00%', out.getvalue())


    def test_fx_anniversary_uses_prior_business_day(self):
        class FrozenDate(date):
            @classmethod
            def today(cls):
                return cls(2026, 10, 19)

        for historical_date in ('2025-10-17', '2025-10-16'):
            with self.subTest(historical_date=historical_date):
                calls = []

                def answers(req, timeout=None):
                    query = urllib.parse.parse_qs(urllib.parse.urlsplit(req.full_url).query)
                    calls.append(query)
                    if 'end_date' in query:
                        start = query.get('start_date', ['2025-10-19'])[0]
                        end = query['end_date'][0]
                        rows = ([{'date': historical_date, 'val': 100.0}]
                                if start <= historical_date <= end else [])
                    else:
                        rows = [{'date': '2026-10-19', 'val': 110.0}]
                    return _Resp(json.dumps({'data': rows}).encode())

                out = io.StringIO()
                with mock.patch.object(M, 'date', FrozenDate), \
                        mock.patch.object(M, '_api_key', return_value=None), \
                        mock.patch.object(M.urllib.request, 'urlopen', answers), \
                        contextlib.redirect_stdout(out):
                    M.cmd_fx('usd', 'jpy')
                self.assertEqual(calls[1], {
                    'start_date': ['2025-10-12'],
                    'end_date': ['2025-10-19'], 'limit': ['1'],
                })
                self.assertIn(historical_date, out.getvalue())
                self.assertIn('+10.00%', out.getvalue())

    def test_catalogue_transport_errors_exit_cli_with_failure(self):
        for command in (['catalogue', 'USD'], ['indicator', 'USD', 'inflation'],
                        ['snapshot', 'USD']):
            for error in (urllib.error.HTTPError('https://example.test', 429,
                                                 'Too Many Requests', {}, None),
                          urllib.error.URLError('offline')):
                with self.subTest(command=command, error=type(error).__name__):
                    def answers(req, timeout=None):
                        if '/data_catalogue/' in req.full_url:
                            raise error
                        return _Resp(json.dumps({'data': [
                            {'date': '2026-10-01', 'val': 2.2},
                        ]}).encode())

                    out = io.StringIO()
                    with mock.patch.object(sys, 'argv', ['macro_data.py'] + command), \
                            mock.patch.object(M, '_api_key', return_value=None), \
                            mock.patch.object(M.urllib.request, 'urlopen', answers), \
                            contextlib.redirect_stdout(out), \
                            self.assertRaises(SystemExit) as raised:
                        M.main()
                    self.assertEqual(raised.exception.code, 2)
                    self.assertIn('HTTP 429' if isinstance(error, urllib.error.HTTPError)
                                  else '网络请求失败', out.getvalue())
                    self.assertNotIn('2.2', out.getvalue())

    def test_catalogue_not_found_remains_empty(self):
        text, _ = self.run_cmd(M.cmd_catalogue, 'usd',
                               routes={'/data_catalogue/usd': 404})
        self.assertIn('USD', text)


class RequestBoundaryTest(unittest.TestCase):
    def test_key_is_not_forwarded_by_urllib_redirects(self):
        seen = []
        with mock.patch.object(M, '_api_key', return_value='fixture-key'), \
                mock.patch.object(M.urllib.request, 'urlopen', _fake_api(ROUTES, seen)):
            M._get('/calendar/usd')
        redirected = M.urllib.request.HTTPRedirectHandler().redirect_request(
            seen[0], None, 302, 'Found', {}, 'https://other.example/calendar')
        self.assertIsNone(redirected.get_header('X-api-key'))

    def test_malformed_key_is_rejected_without_echo(self):
        with mock.patch.object(M, '_api_key', return_value='fixture-key\r\nX-Other: value'), \
                mock.patch.object(M.urllib.request, 'urlopen') as transport:
            with self.assertRaises(ValueError) as raised:
                M._get('/calendar/usd')
        self.assertNotIn('fixture-key', str(raised.exception))
        transport.assert_not_called()

    def test_error_and_scalar_payloads_are_rejected(self):
        for payload in ({'detail': 'fixture-private-value'}, {'error': 'fixture-private-value'}, None, 'text', []):
            with self.subTest(payload=payload), \
                    mock.patch.object(M, '_api_key', return_value=None), \
                    mock.patch.object(M.urllib.request, 'urlopen', return_value=_Resp(json.dumps(payload).encode())):
                with self.assertRaises(ValueError) as raised:
                    M._get('/calendar/usd')
                self.assertNotIn('fixture-private-value', str(raised.exception))

    def test_private_transport_reasons_are_not_in_tracebacks(self):
        import traceback
        errors = [urllib.error.URLError('fixture-private-value'),
                  urllib.error.HTTPError('https://example.invalid', 500, 'fixture-private-value', {}, None)]
        for error in errors:
            with self.subTest(error=type(error).__name__), \
                    mock.patch.object(M, '_api_key', return_value=None), \
                    mock.patch.object(M.urllib.request, 'urlopen', side_effect=error):
                try:
                    M._get('/calendar/usd')
                except ConnectionError as exc:
                    self.assertNotIn('fixture-private-value', ''.join(traceback.format_exception(exc)))
                else:
                    self.fail('transport failure was suppressed')


if __name__ == '__main__':
    unittest.main()
