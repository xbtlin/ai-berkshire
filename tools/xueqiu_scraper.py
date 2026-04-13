#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
雪球通用爬虫：遍历指定用户的完整时间线，按关键词筛选本人原发言。

特性：
  - Playwright 登录态复用：首次 headful 手动登录，state 持久化到本地
  - 双通道 fetch：优先页面内 JS fetch，失败回退 context.request（APIRequestContext）
  - 断点续爬：每 10 页保存进度；中断后再运行自动从上次位置继续
  - 反限流：2-4s 随机抖动 + 每 50 页长休 30s + 连续 5 次超时自动退出保进度
  - 纯转发过滤：只收录被采集用户自己写的内容（text 非空、非"转发微博"）

凭据通过环境变量传入，**不进入代码仓库**：
  export XQ_PHONE=13xxxxxxxxx
  export XQ_PASSWORD=xxx
也可不设，首次运行会弹出 headful 浏览器让你手动登录（扫码/短信/密码随意）。

用法示例：
  # 段永平关于拼多多
  python3 xueqiu_scraper.py \\
      --user-id 1247347556 \\
      --keywords 拼多多,PDD,Temu,黄峥 \\
      --output ../reports/拼多多/段永平雪球发言-PDD相关.md

  # 其他用户 + 其他关键词
  python3 xueqiu_scraper.py --user-id 6784593966 --keywords 茅台 --output /tmp/out.md

登录态缓存默认 /tmp/xueqiu_state.json，可用 --state-path 覆盖。
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
    """优先页面 JS fetch；失败回退到 context.request。"""
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
    print("\n[需要登录] 将打开 headful 浏览器，请在其中完成雪球登录")
    if phone:
        print(f"        环境变量 XQ_PHONE = {phone}   （密码用 XQ_PASSWORD）")
    else:
        print("        未设 XQ_PHONE/XQ_PASSWORD，请在浏览器中手动扫码或输入登录信息")
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
    print(">>> 请在浏览器内完成登录；脚本每 5s 轮询，检测成功自动继续（最长 10 分钟）")
    ok = False
    for i in range(120):
        await asyncio.sleep(5)
        try:
            if await verify_login(page, user_id):
                ok = True
                print(f"  ✓ 登录成功（第 {i+1} 次轮询）")
                break
        except Exception as e:
            print(f"  轮询异常(忽略): {e}")
        if (i + 1) % 6 == 0:
            print(f"  ...仍在等待登录（已等 {(i+1)*5}s）")
    if not ok:
        print("10 分钟内未检测到登录，退出")
        await browser.close()
        return None
    await context.storage_state(path=state_path)
    print(f"登录态已保存 → {state_path}")
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
            print(f"  首页加载失败(第{attempt+1}次): {e}")
            await asyncio.sleep(5)
    if not loaded:
        try:
            await page.goto('about:blank')
        except Exception:
            pass
    await asyncio.sleep(2)
    if await verify_login(page, user_id):
        print("✓ 已复用保存的登录态")
        return browser, context, page
    print("已保存的 state 已过期")
    await browser.close()
    return None


async def fetch_all_timeline(page, user_id, keywords, progress_path):
    collected = {}
    print("\n=== 遍历全量时间线 ===")
    data = await browser_fetch_json(
        page,
        f'https://xueqiu.com/v4/statuses/user_timeline.json?user_id={user_id}&page=1&count=20'
    )
    if not data or data.get('error_code'):
        print(f"  第1页失败: {data}")
        return collected
    max_page = data.get('maxPage', 600)
    total = data.get('total', '?')
    print(f"  用户ID: {user_id} | 总帖子数: {total} | 总页数: {max_page}")

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
            if own_text in ('', '转发微博', '轉發微博', 'Repost'):
                continue
            if is_match(title + ' ' + own_text, keywords):
                pid = str(post.get('id', ''))
                date = parse_ts(post.get('created_at', 0))
                entry = {'id': pid, 'date': date, 'title': title, 'text': own_text,
                         'url': f'https://xueqiu.com/{user_id}/{pid}'}
                if rt:
                    rt_user = (rt.get('user') or {}).get('screen_name', '')
                    entry['retweet_of'] = f'@{rt_user}: {rt_text}'
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
            print(f"  ↪ 续爬：从第 {start_page} 页开始，已有 {found} 条")
        except Exception as e:
            print(f"  进度文件读取失败: {e}")

    def save_progress(next_page):
        with open(progress_path, 'w', encoding='utf-8') as f:
            json.dump({'next_page': next_page, 'collected': list(collected.values())},
                      f, ensure_ascii=False)

    consec_fail = 0
    for p in range(start_page, max_page + 1):
        try:
            data = await browser_fetch_json(
                page,
                f'https://xueqiu.com/v4/statuses/user_timeline.json?user_id={user_id}&page={p}&count=20',
                timeout_s=15,
            )
        except Exception as e:
            print(f"  第{p}页异常: {e}")
            data = None
        if not data:
            consec_fail += 1
            print(f"  第{p}页无响应/超时（连续 {consec_fail} 次）")
            if consec_fail >= 5:
                print("  连续失败 5 次，保存进度并退出（再次运行自动续爬）")
                save_progress(p)
                break
            await asyncio.sleep(5 * consec_fail)
            continue
        consec_fail = 0
        if data.get('error_code'):
            print(f"  第{p}页错误: {data.get('error_code')} {data.get('error_description')}")
            save_progress(p)
            break
        statuses = data.get('statuses', [])
        if not statuses:
            print(f"  第{p}页空，结束")
            break
        prev_found = found
        process(data)
        if p % 10 == 0 or found > prev_found:
            print(f"  第{p}/{max_page}页 | 已扫 {total_posts} 条 | 命中 {found}")
        if p % 10 == 0:
            save_progress(p + 1)
        if p % 50 == 0:
            print(f"  ⏸ 第{p}页后休息 30s")
            await asyncio.sleep(30)
        else:
            await asyncio.sleep(random.uniform(2.0, 4.0))
    else:
        if os.path.exists(progress_path):
            os.remove(progress_path)

    print(f"\n完成：扫描 {total_posts} 条，命中 {found} 条")
    return collected


def format_md(collected, user_id, keywords):
    posts = sorted(collected.values(), key=lambda x: x.get('date', ''))
    lines = [
        f"# 雪球发言整理：用户 {user_id}",
        "",
        f"> **信息来源**：雪球 https://xueqiu.com/u/{user_id}",
        f"> **整理时间**：{datetime.now().strftime('%Y-%m-%d')}",
        f"> **收录条数**：{len(posts)} 条",
        f"> **关键词筛选**：{', '.join(keywords)}",
        f"> **采集方式**：Playwright 登录态 + user_timeline.json 全量遍历（仅本人原发言）",
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
            lines += [f"> 转发原文：{p['retweet_of']}", ""]
        if p.get('text'):
            lines.append(p['text'])
            lines.append("")
        lines += [f"来源：{p.get('url','')}", "", "---", ""]
    return '\n'.join(lines)


def parse_args():
    ap = argparse.ArgumentParser(description="雪球用户时间线爬虫（按关键词筛选本人原发言）")
    ap.add_argument('--user-id', type=int, required=True, help='雪球用户ID（主页URL数字段）')
    ap.add_argument('--keywords', type=str, required=True,
                    help='关键词列表，逗号分隔。例：拼多多,PDD,黄峥,Temu')
    ap.add_argument('--output', type=str, required=True, help='markdown 输出路径')
    ap.add_argument('--raw-json', type=str, default='', help='（可选）原始 JSON 输出路径')
    ap.add_argument('--state-path', type=str, default='/tmp/xueqiu_state.json',
                    help='登录态缓存文件（默认 /tmp/xueqiu_state.json）')
    return ap.parse_args()


async def main():
    args = parse_args()
    keywords = [k.strip() for k in args.keywords.split(',') if k.strip()]
    progress_path = args.state_path + f'.progress.{args.user_id}'
    raw_json = args.raw_json or f'/tmp/xueqiu_{args.user_id}_raw.json'

    print("=" * 60)
    print(f"雪球爬虫 | user_id={args.user_id} | keywords={keywords}")
    print("=" * 60)

    async with async_playwright() as pw:
        session = await load_with_state(pw, args.state_path, args.user_id)
        if not session:
            session = await interactive_login(pw, args.state_path, args.user_id)
        if not session:
            print("无法登录，退出")
            return
        browser, _, page = session
        collected = await fetch_all_timeline(page, args.user_id, keywords, progress_path)
        await browser.close()

    print(f"\n=== 最终: {len(collected)} 条命中 ===")
    if not collected:
        return
    with open(raw_json, 'w', encoding='utf-8') as f:
        json.dump(list(collected.values()), f, ensure_ascii=False, indent=2)
    print(f"原始JSON → {raw_json}")
    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    with open(args.output, 'w', encoding='utf-8') as f:
        f.write(format_md(collected, args.user_id, keywords))
    print(f"Markdown  → {args.output}")


if __name__ == '__main__':
    asyncio.run(main())
