#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
\u96ea\u7403\u901a\u7528\u722c\u866b：\u904d\u5386\u6307\u5b9a\u7528\u6237\u7684\u5b8c\u6574\u65f6\u95f4\u7ebf，\u6309\u5173\u952e\u8bcd\u7b5b\u9009\u672c\u4eba\u539f\u53d1\u8a00。

\u7279\u6027：
  - Playwright \u767b\u5f55\u6001\u590d\u7528：\u9996\u6b21 headful \u624b\u52a8\u767b\u5f55，state \u6301\u4e45\u5316\u5230\u672c\u5730
  - \u53cc\u901a\u9053 fetch：\u4f18\u5148\u9875\u9762\u5185 JS fetch，\u5931\u8d25\u56de\u9000 context.request（APIRequestContext）
  - \u65ad\u70b9\u7eed\u722c：\u6bcf 10 \u9875\u4fdd\u5b58\u8fdb\u5ea6；\u4e2d\u65ad\u540e\u518d\u8fd0\u884c\u81ea\u52a8\u4ece\u4e0a\u6b21\u4f4d\u7f6e\u7ee7\u7eed
  - \u53cd\u9650\u6d41：2-4s \u968f\u673a\u6296\u52a8 + \u6bcf 50 \u9875\u957f\u4f11 30s + \u8fde\u7eed 5 \u6b21\u8d85\u65f6\u81ea\u52a8\u9000\u51fa\u4fdd\u8fdb\u5ea6
  - \u7eaf\u8f6c\u53d1\u8fc7\u6ee4：\u53ea\u6536\u5f55\u88ab\u91c7\u96c6\u7528\u6237\u81ea\u5df1\u5199\u7684\u5185\u5bb9（text \u975e\u7a7a、\u975e"\u8f6c\u53d1\u5fae\u535a"）

\u51ed\u636e\u901a\u8fc7\u73af\u5883\u53d8\u91cf\u4f20\u5165，**\u4e0d\u8fdb\u5165\u4ee3\u7801\u4ed3\u5e93**：
  export XQ_PHONE=13xxxxxxxxx
  export XQ_PASSWORD=xxx
\u4e5f\u53ef\u4e0d\u8bbe，\u9996\u6b21\u8fd0\u884c\u4f1a\u5f39\u51fa headful \u6d4f\u89c8\u5668\u8ba9\u4f60\u624b\u52a8\u767b\u5f55（\u626b\u7801/\u77ed\u4fe1/\u5bc6\u7801\u968f\u610f）。

\u7528\u6cd5\u793a\u4f8b：
  # \u6bb5\u6c38\u5e73\u5173\u4e8e\u62fc\u591a\u591a
  python3 xueqiu_scraper.py \\
      --user-id 1247347556 \\
      --keywords \u62fc\u591a\u591a,PDD,Temu,\u9ec4\u5ce5 \\
      --output ../reports/\u62fc\u591a\u591a/\u6bb5\u6c38\u5e73\u96ea\u7403\u53d1\u8a00-PDD\u76f8\u5173.md

  # \u5176\u4ed6\u7528\u6237 + \u5176\u4ed6\u5173\u952e\u8bcd
  python3 xueqiu_scraper.py --user-id 6784593966 --keywords \u8305\u53f0 --output /tmp/out.md

\u767b\u5f55\u6001\u7f13\u5b58\u9ed8\u8ba4 /tmp/xueqiu_state.json，\u53ef\u7528 --state-path \u8986\u76d6。
"""

import argparse
import asyncio
import json
import os
import random
import re
from datetime import datetime
from pathlib import Path
from playwright.async_api import async_playwright


def is_match(text, keywords):
    t = (text or '').lower()
    return any(k.lower() in t for k in keywords)


def parse_ts(ts):
    try:
        return datetime.fromtimestamp(int(ts) / 1000).strftime('%Y-%m-%d %H:%M')
    except Exception:
        return str(ts)


def clean(s):
    if not s: return ''
    s = re.sub(r'<[^>]+>', '', s)
    for ent, rep in [('&amp;', '&'), ('&lt;', '<'), ('&gt;', '>'), ('&nbsp;', ' ')]:
        s = s.replace(ent, rep)
    return re.sub(r'&#\d+;', '', s).strip()


async def browser_fetch_json(page, url, timeout_s=15):
    """\u4f18\u5148\u9875\u9762 JS fetch；\u5931\u8d25\u56de\u9000\u5230 context.request。"""
    js = f"""
        async () => {{
            const ctl = new AbortController();
            const to = setTimeout(() => ctl.abort(), {int(timeout_s*1000)});
            try {{
                const r = await fetch({json.dumps(url)}, {{
                    headers: {{'Accept':'application/json','X-Requested-With':'XMLHttpRequest'}},
                    credentials: 'include', signal: ctl.signal
                }});
                const text = await r.text();
                clearTimeout(to);
                try {{ return JSON.parse(text); }}
                catch(e) {{ return {{_raw: text.substring(0, 300)}}; }}
            }} catch(e) {{
                clearTimeout(to);
                return {{_error: e.toString()}};
            }}
        }}
    """
    try:
        result = await asyncio.wait_for(page.evaluate(js), timeout=timeout_s + 5)
        if result and not result.get('_error') and not result.get('_raw'):
            return result
    except Exception:
        pass
    try:
        resp = await page.context.request.get(url, headers={
            'Accept': 'application/json',
            'X-Requested-With': 'XMLHttpRequest',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36',
            'Referer': 'https://xueqiu.com/',
        }, timeout=timeout_s * 1000)
        if resp.ok:
            return await resp.json()
    except Exception:
        return None
    return None


async def verify_login(page, user_id):
    test = await browser_fetch_json(
        page,
        f'https://xueqiu.com/v4/statuses/user_timeline.json?user_id={user_id}&page=2&count=1'
    )
    return bool(test and test.get('statuses') is not None)


async def interactive_login(pw, state_path, user_id):
    phone = os.environ.get('XQ_PHONE', '')
    print("\n[\u9700\u8981\u767b\u5f55] \u5c06\u6253\u5f00 headful \u6d4f\u89c8\u5668，\u8bf7\u5728\u5176\u4e2d\u5b8c\u6210\u96ea\u7403\u767b\u5f55")
    if phone:
        print(f"        \u73af\u5883\u53d8\u91cf XQ_PHONE = {phone}   （\u5bc6\u7801\u7528 XQ_PASSWORD）")
    else:
        print("        \u672a\u8bbe XQ_PHONE/XQ_PASSWORD，\u8bf7\u5728\u6d4f\u89c8\u5668\u4e2d\u624b\u52a8\u626b\u7801\u6216\u8f93\u5165\u767b\u5f55\u4fe1\u606f")
    browser = await pw.chromium.launch(
        headless=False,
        args=['--disable-blink-features=AutomationControlled'],
    )
    context = await browser.new_context(
        user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        locale='zh-CN',
        viewport={'width': 1280, 'height': 800},
    )
    await context.add_init_script(
        "Object.defineProperty(navigator,'webdriver',{get:()=>undefined})"
    )
    page = await context.new_page()
    await page.goto('https://xueqiu.com/', wait_until='domcontentloaded')
    print(">>> \u8bf7\u5728\u6d4f\u89c8\u5668\u5185\u5b8c\u6210\u767b\u5f55；\u811a\u672c\u6bcf 5s \u8f6e\u8be2，\u68c0\u6d4b\u6210\u529f\u81ea\u52a8\u7ee7\u7eed（\u6700\u957f 10 \u5206\u949f）")
    ok = False
    for i in range(120):
        await asyncio.sleep(5)
        try:
            if await verify_login(page, user_id):
                ok = True
                print(f"  ✓ \u767b\u5f55\u6210\u529f（\u7b2c {i+1} \u6b21\u8f6e\u8be2）")
                break
        except Exception as e:
            print(f"  \u8f6e\u8be2\u5f02\u5e38(\u5ffd\u7565): {e}")
        if (i + 1) % 6 == 0:
            print(f"  ...\u4ecd\u5728\u7b49\u5f85\u767b\u5f55（\u5df2\u7b49 {(i+1)*5}s）")
    if not ok:
        print("10 \u5206\u949f\u5185\u672a\u68c0\u6d4b\u5230\u767b\u5f55，\u9000\u51fa")
        await browser.close()
        return None
    await context.storage_state(path=state_path)
    print(f"\u767b\u5f55\u6001\u5df2\u4fdd\u5b58 → {state_path}")
    return browser, context, page


async def load_with_state(pw, state_path, user_id):
    if not os.path.exists(state_path):
        return None
    browser = await pw.chromium.launch(
        headless=True,
        args=['--no-sandbox', '--disable-blink-features=AutomationControlled'],
    )
    context = await browser.new_context(
        storage_state=state_path,
        user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        locale='zh-CN',
        viewport={'width': 1280, 'height': 800},
    )
    await context.add_init_script(
        "Object.defineProperty(navigator,'webdriver',{get:()=>undefined})"
    )
    page = await context.new_page()
    loaded = False
    for attempt in range(3):
        try:
            await page.goto('https://xueqiu.com/', wait_until='domcontentloaded', timeout=15000)
            loaded = True
            break
        except Exception as e:
            print(f"  \u9996\u9875\u52a0\u8f7d\u5931\u8d25(\u7b2c{attempt+1}\u6b21): {e}")
            await asyncio.sleep(5)
    if not loaded:
        try:
            await page.goto('about:blank')
        except Exception:
            pass
    await asyncio.sleep(2)
    if await verify_login(page, user_id):
        print("✓ \u5df2\u590d\u7528\u4fdd\u5b58\u7684\u767b\u5f55\u6001")
        return browser, context, page
    print("\u5df2\u4fdd\u5b58\u7684 state \u5df2\u8fc7\u671f")
    await browser.close()
    return None


async def fetch_all_timeline(page, user_id, keywords, progress_path, dump_all_path=''):
    collected = {}
    # all_posts：\u4fdd\u5b58\u8be5\u7528\u6237\u6240\u6709\u539f\u53d1\u8a00（\u4e0d\u6309\u5173\u952e\u8bcd\u8fc7\u6ee4），\u4f9b\u79bb\u7ebf\u591a\u4e3b\u9898\u5206\u6790
    all_posts = {}
    if dump_all_path and os.path.exists(dump_all_path):
        try:
            for e in json.load(open(dump_all_path)):
                all_posts[e['id']] = e
            print(f"  ↪ \u8f7d\u5165\u5df2\u6709\u5168\u91cf\u7f13\u5b58：{len(all_posts)} \u6761")
        except Exception as e:
            print(f"  \u5168\u91cf\u7f13\u5b58\u8bfb\u53d6\u5931\u8d25: {e}")
    print("\n=== \u904d\u5386\u5168\u91cf\u65f6\u95f4\u7ebf ===")
    data = await browser_fetch_json(
        page,
        f'https://xueqiu.com/v4/statuses/user_timeline.json?user_id={user_id}&page=1&count=20'
    )
    if not data or data.get('error_code'):
        print(f"  \u7b2c1\u9875\u5931\u8d25: {data}")
        return collected
    max_page = data.get('maxPage', 600)
    total = data.get('total', '?')
    print(f"  \u7528\u6237ID: {user_id} | \u603b\u5e16\u5b50\u6570: {total} | \u603b\u9875\u6570: {max_page}")

    total_posts = 0
    found = 0

    def process(d):
        nonlocal total_posts, found
        for post in d.get('statuses', []):
            total_posts += 1
            text = clean(post.get('text', '') or post.get('description', ''))
            title = clean(post.get('title', ''))
            rt = post.get('retweeted_status') or {}
            rt_text = clean(rt.get('text', ''))
            own_text = (text or '').strip()
            if own_text in ('', '\u8f6c\u53d1\u5fae\u535a', '\u8f49\u767c\u5fae\u535a', 'Repost'):
                continue
            pid = str(post.get('id', ''))
            date = parse_ts(post.get('created_at', 0))
            entry = {'id': pid, 'date': date, 'title': title, 'text': own_text,
                     'url': f'https://xueqiu.com/{user_id}/{pid}'}
            if rt:
                rt_user = (rt.get('user') or {}).get('screen_name', '')
                entry['retweet_of'] = f'@{rt_user}: {rt_text}'
            # \u5168\u91cf\u7f13\u5b58（\u4e0d\u8fc7\u6ee4）
            if dump_all_path and pid not in all_posts:
                all_posts[pid] = entry
            # \u6309\u5173\u952e\u8bcd\u8fc7\u6ee4\u6536\u96c6
            if keywords and is_match(title + ' ' + own_text, keywords):
                if pid not in collected:
                    collected[pid] = entry
                    found += 1
                    preview = own_text[:80] if own_text else (rt_text[:80] if rt_text else title[:80])
                    print(f"  ✓ [{date}] {preview}...")

    process(data)
    start_page = 2
    if os.path.exists(progress_path):
        try:
            with open(progress_path) as f:
                prev = json.load(f)
            start_page = max(2, prev.get('next_page', 2))
            for e in prev.get('collected', []):
                collected[e['id']] = e
                found += 1
            print(f"  ↪ \u7eed\u722c：\u4ece\u7b2c {start_page} \u9875\u5f00\u59cb，\u5df2\u6709 {found} \u6761")
        except Exception as e:
            print(f"  \u8fdb\u5ea6\u6587\u4ef6\u8bfb\u53d6\u5931\u8d25: {e}")

    def save_progress(next_page):
        with open(progress_path, 'w', encoding='utf-8') as f:
            json.dump({'next_page': next_page, 'collected': list(collected.values())},
                      f, ensure_ascii=False)
        if dump_all_path:
            with open(dump_all_path, 'w', encoding='utf-8') as f:
                json.dump(list(all_posts.values()), f, ensure_ascii=False)

    consec_fail = 0
    for p in range(start_page, max_page + 1):
        try:
            data = await browser_fetch_json(
                page,
                f'https://xueqiu.com/v4/statuses/user_timeline.json?user_id={user_id}&page={p}&count=20',
                timeout_s=15,
            )
        except Exception as e:
            print(f"  \u7b2c{p}\u9875\u5f02\u5e38: {e}")
            data = None
        if not data:
            consec_fail += 1
            print(f"  \u7b2c{p}\u9875\u65e0\u54cd\u5e94/\u8d85\u65f6（\u8fde\u7eed {consec_fail} \u6b21）")
            if consec_fail >= 5:
                print("  \u8fde\u7eed\u5931\u8d25 5 \u6b21，\u4fdd\u5b58\u8fdb\u5ea6\u5e76\u9000\u51fa（\u518d\u6b21\u8fd0\u884c\u81ea\u52a8\u7eed\u722c）")
                save_progress(p)
                break
            await asyncio.sleep(5 * consec_fail)
            continue
        consec_fail = 0
        if data.get('error_code'):
            print(f"  \u7b2c{p}\u9875\u9519\u8bef: {data.get('error_code')} {data.get('error_description')}")
            save_progress(p)
            break
        statuses = data.get('statuses', [])
        if not statuses:
            print(f"  \u7b2c{p}\u9875\u7a7a，\u7ed3\u675f")
            break
        prev_found = found
        process(data)
        if p % 10 == 0 or found > prev_found:
            print(f"  \u7b2c{p}/{max_page}\u9875 | \u5df2\u626b {total_posts} \u6761 | \u547d\u4e2d {found}")
        if p % 10 == 0:
            save_progress(p + 1)
        if p % 50 == 0:
            print(f"  ⏸ \u7b2c{p}\u9875\u540e\u4f11\u606f 30s")
            await asyncio.sleep(30)
        else:
            await asyncio.sleep(random.uniform(2.0, 4.0))
    else:
        if os.path.exists(progress_path):
            os.remove(progress_path)

    # \u6700\u540e\u4e00\u6b21\u843d\u76d8\u5168\u91cf\u7f13\u5b58
    if dump_all_path:
        with open(dump_all_path, 'w', encoding='utf-8') as f:
            json.dump(list(all_posts.values()), f, ensure_ascii=False)
        print(f"  \u5168\u91cf\u7f13\u5b58 → {dump_all_path}（{len(all_posts)} \u6761）")
    print(f"\n\u5b8c\u6210：\u626b\u63cf {total_posts} \u6761，\u547d\u4e2d {found} \u6761")
    return collected


def format_md(collected, user_id, keywords):
    posts = sorted(collected.values(), key=lambda x: x.get('date', ''))
    lines = [
        f"# \u96ea\u7403\u53d1\u8a00\u6574\u7406：\u7528\u6237 {user_id}",
        "",
        f"> **\u4fe1\u606f\u6765\u6e90**：\u96ea\u7403 https://xueqiu.com/u/{user_id}",
        f"> **\u6574\u7406\u65f6\u95f4**：{datetime.now().strftime('%Y-%m-%d')}",
        f"> **\u6536\u5f55\u6761\u6570**：{len(posts)} \u6761",
        f"> **\u5173\u952e\u8bcd\u7b5b\u9009**：{', '.join(keywords)}",
        f"> **\u91c7\u96c6\u65b9\u5f0f**：Playwright \u767b\u5f55\u6001 + user_timeline.json \u5168\u91cf\u904d\u5386（\u4ec5\u672c\u4eba\u539f\u53d1\u8a00）",
        "",
        "---",
        "",
    ]
    for i, p in enumerate(posts, 1):
        lines.append(f"## {i}. {p.get('date','?')}")
        lines.append("")
        if p.get('title'):
            lines += [f"**【{p['title']}】**", ""]
        if p.get('retweet_of'):
            lines += [f"> \u8f6c\u53d1\u539f\u6587：{p['retweet_of']}", ""]
        if p.get('text'):
            lines.append(p['text'])
            lines.append("")
        lines += [f"\u6765\u6e90：{p.get('url','')}", "", "---", ""]
    return '\n'.join(lines)


def parse_args():
    ap = argparse.ArgumentParser(description="\u96ea\u7403\u7528\u6237\u65f6\u95f4\u7ebf\u722c\u866b（\u6309\u5173\u952e\u8bcd\u7b5b\u9009\u672c\u4eba\u539f\u53d1\u8a00）")
    ap.add_argument('--user-id', type=int, help='\u96ea\u7403\u7528\u6237ID（\u4e3b\u9875URL\u6570\u5b57\u6bb5）')
    ap.add_argument('--keywords', type=str, default='',
                    help='\u5173\u952e\u8bcd\u5217\u8868，\u9017\u53f7\u5206\u9694。\u4f8b：\u62fc\u591a\u591a,PDD,\u9ec4\u5ce5,Temu')
    ap.add_argument('--output', type=str, default='', help='markdown \u8f93\u51fa\u8def\u5f84')
    ap.add_argument('--raw-json', type=str, default='', help='（\u53ef\u9009）\u547d\u4e2d\u6761\u76ee\u539f\u59cb JSON \u8f93\u51fa\u8def\u5f84')
    ap.add_argument('--state-path', type=str, default='/tmp/xueqiu_state.json',
                    help='\u767b\u5f55\u6001\u7f13\u5b58\u6587\u4ef6（\u9ed8\u8ba4 /tmp/xueqiu_state.json）')
    ap.add_argument('--dump-all', type=str, default='',
                    help='\u5168\u91cf\u7f13\u5b58\u8def\u5f84：\u722c\u53d6\u65f6\u540c\u65f6\u628a\u8be5\u7528\u6237\u6240\u6709\u539f\u53d1\u8a00\u5199\u5230\u8fd9\u91cc，\u7528\u4e8e\u540e\u7eed\u79bb\u7ebf\u591a\u4e3b\u9898\u5206\u6790')
    ap.add_argument('--from-cache', type=str, default='',
                    help='\u8df3\u8fc7\u722c\u53d6，\u4ece\u5df2\u6709\u5168\u91cf\u7f13\u5b58 JSON \u8fc7\u6ee4\u751f\u6210 markdown（\u9700 --keywords \u548c --output）')
    return ap.parse_args()


def filter_from_cache(cache_path, keywords, user_id):
    posts = json.load(open(cache_path))
    out = []
    for p in posts:
        if is_match((p.get('title','') + ' ' + p.get('text','')), keywords):
            out.append(p)
    return {p['id']: p for p in out}


async def main():
    args = parse_args()
    keywords = [k.strip() for k in args.keywords.split(',') if k.strip()]

    # \u79bb\u7ebf\u8fc7\u6ee4\u6a21\u5f0f
    if args.from_cache:
        if not (keywords and args.output):
            print("--from-cache \u9700\u540c\u65f6\u6307\u5b9a --keywords \u4e0e --output")
            return
        user_id = args.user_id or 0
        collected = filter_from_cache(args.from_cache, keywords, user_id)
        print(f"\u4ece\u7f13\u5b58 {args.from_cache} \u7b5b\u51fa {len(collected)} \u6761（\u5173\u952e\u8bcd: {keywords}）")
        if not collected:
            return
        Path(args.output).parent.mkdir(parents=True, exist_ok=True)
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(format_md(collected, user_id, keywords))
        print(f"Markdown → {args.output}")
        return

    if not args.user_id:
        print("\u9700\u8981 --user-id")
        return

    progress_path = args.state_path + f'.progress.{args.user_id}'
    raw_json = args.raw_json or f'/tmp/xueqiu_{args.user_id}_raw.json'

    print("=" * 60)
    print(f"\u96ea\u7403\u722c\u866b | user_id={args.user_id} | keywords={keywords} | dump_all={args.dump_all}")
    print("=" * 60)

    async with async_playwright() as pw:
        session = await load_with_state(pw, args.state_path, args.user_id)
        if not session:
            session = await interactive_login(pw, args.state_path, args.user_id)
        if not session:
            print("\u65e0\u6cd5\u767b\u5f55，\u9000\u51fa")
            return
        browser, _, page = session
        collected = await fetch_all_timeline(page, args.user_id, keywords, progress_path, args.dump_all)
        await browser.close()

    print(f"\n=== \u6700\u7ec8: {len(collected)} \u6761\u547d\u4e2d ===")
    if not collected:
        return
    with open(raw_json, 'w', encoding='utf-8') as f:
        json.dump(list(collected.values()), f, ensure_ascii=False, indent=2)
    print(f"\u539f\u59cbJSON → {raw_json}")
    if args.output:
        Path(args.output).parent.mkdir(parents=True, exist_ok=True)
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(format_md(collected, args.user_id, keywords))
        print(f"Markdown  → {args.output}")


if __name__ == '__main__':
    asyncio.run(main())
