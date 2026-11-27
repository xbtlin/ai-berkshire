#!/usr/bin/env python3
"""wechat_archive.py 回归测试：curl 必须有超时，连接卡住时不能无限挂起。

运行：  python3 tests/test_wechat_archive.py
"""

import importlib.util
import os
import socket
import subprocess
import sys
import tempfile
import threading
import time
import types
import unittest
from pathlib import Path

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'tools'))

# 抓取逻辑不依赖 bs4 / markdownify；未安装时用占位模块，让测试只靠标准库就能跑。
for _name, _attr in (('bs4', 'BeautifulSoup'), ('markdownify', 'MarkdownConverter')):
    if importlib.util.find_spec(_name) is None:
        sys.modules[_name] = types.SimpleNamespace(**{_attr: object})

import wechat_archive as WA  # noqa: E402


class _SilentServer:
    """接受连接但永远不回响应的本地服务，模拟网络卡死。"""

    def __init__(self):
        self.sock = socket.socket()
        self.sock.bind(('127.0.0.1', 0))
        self.sock.listen(8)
        self.port = self.sock.getsockname()[1]
        self.conns = []
        self._stop = False
        threading.Thread(target=self._accept, daemon=True).start()

    def _accept(self):
        while not self._stop:
            try:
                conn, _ = self.sock.accept()
            except OSError:
                return
            self.conns.append(conn)

    def close(self):
        self._stop = True
        for c in self.conns:
            c.close()
        self.sock.close()


class TestCurlTimeout(unittest.TestCase):

    def setUp(self):
        self.server = _SilentServer()
        self.addCleanup(self.server.close)
        self._saved = (WA.CONNECT_TIMEOUT, WA.MAX_TIME) if hasattr(WA, 'MAX_TIME') else None
        WA.CONNECT_TIMEOUT, WA.MAX_TIME = 2, 2

    def tearDown(self):
        if self._saved:
            WA.CONNECT_TIMEOUT, WA.MAX_TIME = self._saved

    def test_stalled_page_fetch_fails_instead_of_hanging(self):
        result = {}

        def run():
            t0 = time.monotonic()
            try:
                WA.curl(f'http://127.0.0.1:{self.server.port}/')
                result['outcome'] = 'returned'
            except subprocess.CalledProcessError as exc:
                result['outcome'] = 'CalledProcessError'
                result['code'] = exc.returncode
            result['elapsed'] = time.monotonic() - t0

        worker = threading.Thread(target=run, daemon=True)
        worker.start()
        worker.join(15)
        self.assertFalse(worker.is_alive(), 'curl() 在 15 秒内没有返回：连接卡住时会无限挂起')
        self.assertEqual(result['outcome'], 'CalledProcessError')
        self.assertEqual(result['code'], 28)   # curl: operation timed out

    def test_image_download_passes_timeouts_to_curl(self):
        calls = []

        def fake_run(cmd, *args, **kwargs):
            calls.append(cmd)
            raise subprocess.CalledProcessError(28, cmd)

        with tempfile.TemporaryDirectory() as tmp:
            saved_dir, saved_run = WA.IMG_DIR, WA.subprocess.run
            WA.IMG_DIR, WA.subprocess.run = Path(tmp), fake_run
            try:
                with self.assertRaises(subprocess.CalledProcessError):
                    WA.localize_images('![](https://mmbiz.qpic.cn/x.png)', '2026-11-16')
            finally:
                WA.IMG_DIR, WA.subprocess.run = saved_dir, saved_run
        self.assertTrue(calls and calls[0][0] == 'curl')
        self.assertIn('--max-time', calls[0])
        self.assertIn('--connect-timeout', calls[0])


if __name__ == '__main__':
    unittest.main()
