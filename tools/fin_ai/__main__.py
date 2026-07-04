"""包级入口：让 `python -m tools.fin_ai` 可用。"""
import sys

# Windows 控制台默认 GBK，强制 stdin/stdout/stderr 用 UTF-8，
# 避免 piped 中文输入（如 printf | python）产生 surrogate 导致 JSON 序列化崩溃
for _stream_name in ("stdin", "stdout", "stderr"):
    _stream = getattr(sys, _stream_name, None)
    if _stream is not None and hasattr(_stream, "reconfigure"):
        try:
            _stream.reconfigure(encoding="utf-8", errors="replace")
        except (OSError, ValueError):
            pass

from .cli import main

if __name__ == "__main__":
    sys.exit(main())
