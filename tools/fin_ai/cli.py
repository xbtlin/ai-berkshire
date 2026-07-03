"""金融 AI CLI 入口。

子命令：
    ask "query"          单次查询（流式打印）
    ask --multi "topic"  多轮 REPL
    quota                查配额
    history              查最近缓存（本地，不烧配额）
    clear-cache          清缓存
"""
import argparse
import sys
import time
import uuid
from pathlib import Path

import httpx

from .cache import cache_key, get as cache_get, put as cache_put, clear as cache_clear, list_recent
from .client import FinAIClient, FinAIError
from .config import Config, ConfigError
from .quota import pre_check


def main(argv=None):
    parser = argparse.ArgumentParser(prog="python -m tools.fin_ai")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_ask = sub.add_parser("ask", help="单次或 REPL 多轮查询")
    p_ask.add_argument("query", nargs="?", help="查询内容（--multi 时为初始话题）")
    p_ask.add_argument("--multi", action="store_true", help="进入多轮 REPL")
    p_ask.add_argument("--ttl-hours", type=int, default=24, help="缓存 TTL（小时）")
    p_ask.add_argument("--no-cache", action="store_true", help="跳过查缓存（仍写缓存）")
    p_ask.add_argument("--refresh", action="store_true", help="强制刷新，覆盖旧缓存")

    sub.add_parser("quota", help="查当日配额")
    p_hist = sub.add_parser("history", help="查最近缓存")
    p_hist.add_argument("--limit", type=int, default=20)

    p_clear = sub.add_parser("clear-cache", help="清缓存")
    p_clear.add_argument("--all", action="store_true")
    p_clear.add_argument("--query", default="")

    args = parser.parse_args(argv)

    try:
        if args.cmd == "ask":
            return _cmd_ask(args)
        if args.cmd == "quota":
            return _cmd_quota()
        if args.cmd == "history":
            return _cmd_history(args.limit)
        if args.cmd == "clear-cache":
            return _cmd_clear(args.all, args.query)
    except ConfigError as e:
        print(f"[FIN_AI ERROR] {e}", file=sys.stderr)
        return 2
    except FinAIError as e:
        print(f"[FIN_AI ERROR] {e}", file=sys.stderr)
        if "daily_limit_exceeded" in str(e):
            return 4
        if "reconnect_expired" in str(e) or "reconnect_completed" in str(e):
            return 6
        if "reconnect_forbidden" in str(e):
            return 7
        return 5
    except httpx.HTTPStatusError as e:
        print(f"[FIN_AI ERROR] HTTP {e.response.status_code}: {e}", file=sys.stderr)
        if e.response.status_code in (401, 403):
            return 8
        if e.response.status_code == 404:
            return 9
        return 10
    except (httpx.ConnectError, httpx.TimeoutException) as e:
        print(f"[FIN_AI ERROR] 网络错误: {type(e).__name__}", file=sys.stderr)
        return 11


def _cmd_ask(args):
    cfg = Config.load()

    if not args.multi and not args.query:
        print("error: ask 需要提供 query 或 --multi", file=sys.stderr)
        return 1

    key = cache_key(args.query or "", cfg.model)
    # 缓存命中不需要 client（避免无谓的连接池开销）
    if not args.multi and not args.refresh and not args.no_cache:
        cached = cache_get(key, args.ttl_hours)
        if cached:
            print(f"[FIN_AI] [CACHE HIT] (cached at {cached.get('ts')})")
            print(cached["content"])
            return 0

    with FinAIClient(cfg) as client:
        if args.multi:
            return _repl(client, args.query or "")

        # 配额预检
        status = pre_check(client)
        if status and status.exceeded:
            print(f"[FIN_AI ERROR] 配额已耗尽 ({status.used}/{status.limit})，明天 00:00 重置", file=sys.stderr)
            return 3
        if status and status.should_warn():
            print(f"[FIN_AI WARN] 配额将耗尽：剩余 {status.remaining}/{status.limit}", file=sys.stderr)

        print(f"[FIN_AI] querying: {args.query}", file=sys.stderr)
        if status:
            print(f"[FIN_AI] quota: remaining {status.remaining}/{status.limit}", file=sys.stderr)

        start = time.time()
        sep = "─" * 40
        print(sep)
        result = client.chat(args.query, on_delta=lambda c: print(c, end="", flush=True))
        print()
        print(sep)

        elapsed = time.time() - start
        out_tok = result.usage.get("output_tokens", "?")
        in_tok = result.usage.get("input_tokens", "?")
        print(f"[FIN_AI] done in {elapsed:.1f}s · tokens: {out_tok} out / {in_tok} in · [SID: {result.session_id}]", file=sys.stderr)

        # 写缓存（即使 --no-cache 也写，让下次受益；refresh 也写以覆盖旧值；
        # SSE 错误由 client 异常路径保证不走到这里）
        cache_put(key, {
            "query": args.query,
            "model": cfg.model,
            "content": result.content,
            "usage": result.usage,
            "ts": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
            "session_id": result.session_id,
            "conversation_sid": result.conversation_sid,
        })

    return 0


def _repl(client, topic):
    """多轮 REPL 模式。"""
    sid = str(uuid.uuid4())
    print(f"[FIN_AI] multi-turn REPL (topic={topic!r}, sid={sid[:8]}...)")
    print("[FIN_AI] /quit 退出；每轮前会显示剩余配额")
    turn = 0
    try:
        while True:
            try:
                q = input(f"turn {turn + 1} >> ").strip()
            except (EOFError, KeyboardInterrupt):
                print()
                break
            if not q:
                continue
            if q in ("/quit", "/exit", "/q"):
                break
            turn += 1

            status = pre_check(client)
            if status and status.exceeded:
                print(f"[FIN_AI ERROR] 配额已耗尽，明天再试", file=sys.stderr)
                break
            if status:
                print(f"[quota: {status.remaining}/{status.limit}]", file=sys.stderr)

            try:
                result = client.chat(q, conversation_sid=sid)
                print(result.content)
                print(f"[SID: {result.session_id}]", file=sys.stderr)
            except FinAIError as e:
                print(f"[ERROR] {e}", file=sys.stderr)
                continue
    except KeyboardInterrupt:
        print("\n[FIN_AI] interrupted")
    finally:
        print("[FIN_AI] session ended")
    return 0


def _cmd_quota():
    cfg = Config.load()
    with FinAIClient(cfg) as client:
        status = pre_check(client)
    if status is None:
        print("[FIN_AI] limit 接口不可用，无法预检")
        return 0
    print(f"exceeded: {status.exceeded}")
    print(f"used:     {status.used}")
    print(f"limit:    {status.limit}")
    print(f"remaining:{status.remaining}")
    return 0


def _cmd_history(limit):
    items = list_recent(limit=limit)
    if not items:
        print("(无缓存)")
        return 0
    for i, it in enumerate(items, 1):
        q = it.get("query", "?")[:60]
        ts = it.get("ts", "?")
        sid = it.get("session_id", "?")
        print(f"{i:3d}. [{ts}] SID={sid}  {q}")
    return 0


def _cmd_clear(all_flag, query):
    n = cache_clear(all=all_flag, query=query)
    print(f"cleared {n} entries")
    return 0


if __name__ == "__main__":
    sys.exit(main())
