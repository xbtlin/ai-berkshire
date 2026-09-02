#!/usr/bin/env python3
"""生成与 star-history.com 完全同款的 star 增长曲线 SVG（浅色/深色两版）。

背景：GitHub 已将 stargazers 数据限制为仓库管理员/协作者可读，star-history.com
等第三方图表服务无法再匿名获取数据，README 里的外链图表因此失效。本脚本用
本仓库自己的令牌拉取数据，按 star-history 开源渲染器（star-history/star-history
仓库 shared/packages/xy-chart.tsx 及 utils/）逐项复刻其 SVG 输出：xkcd 手绘滤镜、
monotone 曲线、嵌入字体、标题带仓库头像、左上图例、右下水印。

数据来源：GitHub REST API stargazers（Accept: application/vnd.github.star+json
带 starred_at 时间戳），按页均匀采样（每页 100 条，取每页首条时间戳即可精确
还原累计曲线）。

用法：
    GITHUB_TOKEN=$(gh auth token) python3 tools/star_history_chart.py

依赖素材（提取自 star-history 开源仓库，随本仓库提交）：
    tools/xkcd.woff              — xkcd 手写字体
    tools/star-history-logo.png  — 右下角水印图标

输出：assets/star-history.svg 和 assets/star-history-dark.svg
"""

import base64
import json
import math
import os
import sys
import urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path

REPO = "xbtlin/ai-berkshire"
API = "https://api.github.com"
MAX_SAMPLE_PAGES = 36  # 采样页数上限，曲线平滑度足够且请求量可控

# 布局与配色常量全部取自 star-history 渲染器源码
WIDTH = 800
HEIGHT = 800 * 2 / 3
M_TOP, M_RIGHT, M_BOTTOM, M_LEFT = 60, 30, 50, 70  # 有标题时 top=60
CHART_W = WIDTH - M_LEFT - M_RIGHT
CHART_H = HEIGHT - M_TOP - M_BOTTOM

THEMES = {
    "": {"bg": "white", "stroke": "black", "line": "#dd4528"},
    "-dark": {"bg": "#0d1117", "stroke": "white", "line": "#ff6b6b"},
}

MONTHS = ["January", "February", "March", "April", "May", "June",
          "July", "August", "September", "October", "November", "December"]
MONTHS_ABBR = [m[:3] for m in MONTHS]
WEEKDAYS_ABBR = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]


def gh_get(path, accept="application/vnd.github+json", raw=False):
    req = urllib.request.Request(path if path.startswith("http") else API + path)
    req.add_header("Accept", accept)
    req.add_header("User-Agent", "star-history-chart")
    token = os.environ.get("GITHUB_TOKEN", "")
    if token and not path.startswith("https://avatars."):
        req.add_header("Authorization", f"Bearer {token}")
    with urllib.request.urlopen(req, timeout=30) as resp:
        data = resp.read()
    return data if raw else json.loads(data)


def fetch_points():
    repo = gh_get(f"/repos/{REPO}")
    total = repo["stargazers_count"]
    if total == 0:
        sys.exit("仓库没有 star，无需生成图表")

    last_page = math.ceil(total / 100)
    n = min(last_page, MAX_SAMPLE_PAGES)
    pages = sorted({round(1 + (last_page - 1) * i / (n - 1)) for i in range(n)}) if n > 1 else [1]

    points = []
    for p in pages:
        data = gh_get(
            f"/repos/{REPO}/stargazers?per_page=100&page={p}",
            accept="application/vnd.github.star+json",
        )
        if data:
            t = datetime.fromisoformat(data[0]["starred_at"].replace("Z", "+00:00"))
            points.append((t, (p - 1) * 100 + 1))
    points.append((datetime.now(timezone.utc), total))
    points.sort()
    # star-history 的 insertZeroPoint：首个 star 前一天补零点
    points.insert(0, (points[0][0] - timedelta(days=1), 0))
    # x 必须严格递增（monotone 曲线要求），去掉同时刻的重复采样
    dedup = [points[0]]
    for t, v in points[1:]:
        if t > dedup[-1][0]:
            dedup.append((t, v))
    return dedup, total, repo["owner"]["avatar_url"]


def fmt(x):
    """模拟 JS 数字序列化：整数不带小数点，浮点全精度。"""
    if isinstance(x, float) and x.is_integer():
        return str(int(x))
    return repr(x) if isinstance(x, float) else str(x)


def sign(x):
    return -1.0 if x < 0 else (1.0 if x > 0 else 0.0)


def monotone_x_path(pts):
    """复刻 d3-shape curveMonotoneX 的贝塞尔路径输出。"""

    def slope3(x0, y0, x1, y1, x2, y2):
        h0, h1 = x1 - x0, x2 - x1
        s0 = (y1 - y0) / h0 if h0 else 0.0
        s1 = (y2 - y1) / h1 if h1 else 0.0
        p = (s0 * h1 + s1 * h0) / (h0 + h1) if h0 + h1 else 0.0
        return (sign(s0) + sign(s1)) * min(abs(s0), abs(s1), 0.5 * abs(p))

    def slope2(x0, y0, x1, y1, t):
        h = x1 - x0
        return (3 * (y1 - y0) / h - t) / 2 if h else t

    def bezier(x0, y0, x1, y1, t0, t1):
        dx = (x1 - x0) / 3
        return (f"C{fmt(x0 + dx)},{fmt(y0 + dx * t0)},"
                f"{fmt(x1 - dx)},{fmt(y1 - dx * t1)},{fmt(x1)},{fmt(y1)}")

    n = len(pts)
    path = f"M{fmt(pts[0][0])},{fmt(pts[0][1])}"
    if n == 1:
        return path
    if n == 2:
        return path + f"L{fmt(pts[1][0])},{fmt(pts[1][1])}"

    t0 = 0.0
    for i in range(2, n):
        (x0, y0), (x1, y1), (x2, y2) = pts[i - 2], pts[i - 1], pts[i]
        t1 = slope3(x0, y0, x1, y1, x2, y2)
        path += bezier(x0, y0, x1, y1,
                       slope2(x0, y0, x1, y1, t1) if i == 2 else t0, t1)
        t0 = t1
    (x0, y0), (x1, y1) = pts[-2], pts[-1]
    path += bezier(x0, y0, x1, y1, t0, slope2(x0, y0, x1, y1, t0))
    return path


def linear_ticks(stop, count=5):
    """复刻 d3.ticks(0, stop, count)。"""
    step = stop / count
    power = math.floor(math.log10(step))
    error = step / 10 ** power
    factor = 10 if error >= math.sqrt(50) else 5 if error >= math.sqrt(10) else 2 if error >= math.sqrt(2) else 1
    step = factor * 10 ** power
    return [step * i for i in range(int(stop // step) + 1)]


def time_ticks(t0, t1, count=5):
    """复刻 d3 scaleTime.ticks：按跨度选择 天/2天/周/月/3月/年 间隔。"""
    span = (t1 - t0).total_seconds() * 1000
    target = span / count
    day = 864e5
    intervals = [("day", 1, day), ("day", 2, 2 * day), ("week", 1, 7 * day),
                 ("month", 1, 30 * day), ("month", 3, 90 * day), ("year", 1, 365 * day)]
    choice = intervals[-1]
    for i, iv in enumerate(intervals):
        if target <= iv[2]:
            if i > 0 and target / intervals[i - 1][2] < iv[2] / target:
                choice = intervals[i - 1]
            else:
                choice = iv
            break
    unit, step, _ = choice

    ticks = []
    if unit == "year":
        years = [y for y in linear_ticks(t1.year, count) if y >= t0.year]
        for y in years or range(t0.year + 1, t1.year + 1):
            t = datetime(int(y), 1, 1, tzinfo=timezone.utc)
            if t0 <= t <= t1:
                ticks.append(t)
    elif unit == "month":
        y, m = t0.year, t0.month
        while True:
            m += 1
            if m > 12:
                y, m = y + 1, 1
            if unit == "month" and step == 3 and (m - 1) % 3 != 0:
                continue
            t = datetime(y, m, 1, tzinfo=timezone.utc)
            if t > t1:
                break
            if t >= t0:
                ticks.append(t)
    elif unit == "week":
        # d3 timeWeek 以周日为界
        start = (t0 + timedelta(days=(6 - t0.weekday()) % 7 or 7)).replace(
            hour=0, minute=0, second=0, microsecond=0)
        t = start
        while t <= t1:
            if t >= t0:
                ticks.append(t)
            t += timedelta(weeks=1)
    else:
        start = t0.replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(days=1)
        t = start
        while t <= t1:
            ticks.append(t)
            t += timedelta(days=step)
    return ticks


def time_tick_label(t):
    """复刻 d3 默认时间多级格式：年首→%Y，月首→%B，周日→%b %d，其余→%a %d。"""
    if t.month == 1 and t.day == 1:
        return str(t.year)
    if t.day == 1:
        return MONTHS[t.month - 1]
    if t.weekday() == 6:
        return f"{MONTHS_ABBR[t.month - 1]} {t.day:02d}"
    return f"{WEEKDAYS_ABBR[t.weekday()]} {t.day:02d}"


def number_tick_label(v, unit):
    """复刻 star-history getFormatNumber。"""
    if unit == 1:
        return fmt(float(v))
    div, suffix = (1e6, "M") if unit == 1000000 else (1e3, "K")
    if v >= div and v % div == 0:
        return f"{int(v / div)}{suffix}"
    return f"{v / div:.1f}{suffix}"


def render(points, total, theme, font_b64, logo_b64, avatar_b64, avatar_mime):
    t0, t1 = points[0][0], points[-1][0]
    span = (t1 - t0).total_seconds()

    def x(t):
        return CHART_W * (t - t0).total_seconds() / span

    def y(v):
        return CHART_H * (1 - v / total)

    stroke, bg, line_color = theme["stroke"], theme["bg"], theme["line"]

    # X 轴（d3 axisBottom, tickSize 0, tickPadding 6, 刻度位置 +0.5）
    xticks = "".join(
        f'<g class="tick" opacity="1" transform="translate({fmt(x(t) + 0.5)},0)">'
        f'<line stroke="currentColor" y2="0"></line>'
        f'<text fill="currentColor" y="6" dy="0.71em" '
        f'style="font-family: xkcd; font-size: 16px; fill: {stroke};">{time_tick_label(t)}</text></g>'
        for t in time_ticks(t0, t1)
    )
    xaxis = (
        f'<g class="xaxis" transform="translate(0,{fmt(CHART_H)})" fill="none" '
        f'font-size="10" font-family="sans-serif" text-anchor="middle">'
        f'<path class="domain" stroke="currentColor" d="M0.5,0.5H{fmt(CHART_W + 0.5)}" '
        f'filter="url(#xkcdify)" style="stroke: {stroke};"></path>{xticks}</g>'
    )

    # Y 轴（d3 axisLeft, tickSize 1, tickPadding 6；0 刻度显示空格）
    yvals = linear_ticks(total)
    first = next(v for v in yvals if v)
    unit = 1000000 if first >= 1000000 else 1000 if first >= 300 else 1
    yticks = "".join(
        f'<g class="tick" opacity="1" transform="translate(0,{fmt(y(v) + 0.5)})">'
        f'<line stroke="currentColor" x2="-1"></line>'
        f'<text fill="currentColor" x="-7" dy="0.32em" '
        f'style="font-family: xkcd; font-size: 16px; fill: {stroke};">'
        f'{" " if v == 0 else number_tick_label(v, unit)}</text></g>'
        for v in yvals
    )
    yaxis = (
        f'<g class="yaxis" fill="none" font-size="10" font-family="sans-serif" text-anchor="end">'
        f'<path class="domain" stroke="currentColor" d="M-1,{fmt(CHART_H + 0.5)}H0.5V0.5H-1" '
        f'filter="url(#xkcdify)" style="stroke: {stroke};"></path>{yticks}</g>'
    )

    line_path = monotone_x_path([(x(t), y(v)) for t, v in points])
    line = (f'<path class="xkcd-chart-xyline" d="{line_path}" fill="none" '
            f'stroke="{line_color}" filter="url(#xkcdify)"></path>')

    # 图例（左上）：宽度公式取自 drawLegend
    L = len(REPO)
    legend_w = max(L * 7.5 + 8 + 7 + 14, L * 7 + 8 + 14 + 6)
    legend = (
        f'<svg><svg><rect style="fill: {bg};" fill-opacity="0.85" stroke="{stroke}" '
        f'stroke-width="2" rx="5" ry="5" filter="url(#xkcdify)" width="{fmt(float(legend_w))}" '
        f'height="32" x="8" y="5"></rect></svg>'
        f'<svg><rect style="fill: {line_color};" width="8" height="8" rx="2" ry="2" '
        f'filter="url(#xkcdify)" x="15" y="17"></rect>'
        f'<text style="font-size: 15px; fill: {stroke};" x="29" y="25">{REPO}</text></svg></svg>'
    )

    watermark = (
        f'<text style="font-size: 16px; fill: #666666;" '
        f'transform="translate({fmt(CHART_W - 50.0)},{fmt(CHART_H + 40)})" '
        f'text-anchor="middle">star-history.com</text>'
        f'<image transform="translate({fmt(CHART_W - 135.0)},{fmt(CHART_H + 24)})" '
        f'height="20" width="20" href="data:image/png;base64,{logo_b64}"></image>'
    )

    tooltip = (
        f'<svg x="15" y="10" style="visibility: hidden;">'
        f'<rect style="fill: {bg};" fill-opacity="0.9" stroke="{stroke}" stroke-width="2" '
        f'rx="5" ry="5" filter="url(#xkcdify)" width="25" height="30" x="5" y="5"></rect>'
        f'<text style="font-size: 15px; font-weight: bold; fill: {stroke};" x="15" y="25"></text></svg>'
    )

    # 标题 + 仓库头像（clipX = 800*0.5-73, logoX = 800*0.5-84）
    title = (
        f'<text style="font-size: 20px; font-weight: bold; fill: {stroke};" x="50%" y="30" '
        f'text-anchor="middle">Star History</text>'
        f'<svg><defs><clipPath id="clip-circle-title"><circle r="11" cx="327" cy="23">'
        f'</circle></clipPath></defs></svg>'
        f'<image x="316" y="12" height="22" width="22" '
        f'href="data:{avatar_mime};base64,{avatar_b64}" clip-path="url(#clip-circle-title)"></image>'
    )

    # Y 轴标签偏移：取自 xy-chart 按最大值分档
    offset_y = 2 if total > 100000 else 8 if total > 10000 else 12 if total > 1000 else 20 if total > 100 else 24
    label_x = math.floor(100 / 2 - HEIGHT / 2)
    labels = (
        f'<text style="font-size: 17px; fill: {stroke};" x="50%" y="{fmt(HEIGHT - 10)}" '
        f'text-anchor="middle">Date</text>'
        f'<text text-anchor="end" dy=".75em" transform="rotate(-90)" '
        f'style="font-size: 17px; fill: {stroke};" y="{offset_y}" x="{label_x}">GitHub Stars</text>'
    )

    return (
        f'<svg width="{WIDTH}" xmlns="http://www.w3.org/2000/svg" '
        f'style="stroke-width: 3; font-family: xkcd; background: {bg};" '
        f'height="{fmt(HEIGHT)}" preserveAspectRatio="xMidYMid meet">'
        f'<defs><style type="text/css">@font-face {{\n'
        f'      font-family: "xkcd";\n'
        f'      src: url(data:application/font-woff;charset=utf-8;base64,{font_b64}) format(\'woff\');\n'
        f'    }}</style></defs>'
        f'<filter id="xkcdify" filterUnits="userSpaceOnUse" x="-5" y="-5" width="100%" height="100%">'
        f'<feTurbulence type="fractalNoise" baseFrequency="0.05" result="noise"/>'
        f'<feDisplacementMap scale="5" xChannelSelector="R" yChannelSelector="G" '
        f'in="SourceGraphic" in2="noise"/></filter>'
        f'<g transform="translate({M_LEFT},{M_TOP})"><g pointer-events="all">'
        f'{watermark}{xaxis}{yaxis}{line}{legend}</g></g>'
        f'{tooltip}{title}{labels}</svg>'
    )


def main():
    tools_dir = Path(__file__).resolve().parent
    out_dir = tools_dir.parent / "assets"

    points, total, avatar_url = fetch_points()
    avatar = gh_get(avatar_url + "&s=64", raw=True)
    avatar_mime = "image/jpeg" if avatar[:2] == b"\xff\xd8" else "image/png"
    avatar_b64 = base64.b64encode(avatar).decode()
    font_b64 = base64.b64encode((tools_dir / "xkcd.woff").read_bytes()).decode()
    logo_b64 = base64.b64encode((tools_dir / "star-history-logo.png").read_bytes()).decode()

    for suffix, theme in THEMES.items():
        path = out_dir / f"star-history{suffix}.svg"
        path.write_text(render(points, total, theme, font_b64, logo_b64, avatar_b64, avatar_mime),
                        encoding="utf-8")
        print(f"已生成 {path}（{total:,} stars，{len(points)} 个采样点）")


if __name__ == "__main__":
    main()
