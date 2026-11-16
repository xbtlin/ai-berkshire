# /// script
# requires-python = ">=3.9"
# dependencies = ["beautifulsoup4", "markdownify"]
# ///
"""把公众号「投资炼丹」合集里新发的文章归档进 投资炼丹/。

流程：
  1. 拉合集列表（公开接口，免登录）
  2. 对比 投资炼丹/ 里已有文章（按原文链接的 mid/idx），找出新发的
  3. 逐篇抓发表版正文 → 转 Markdown → 图片下载到 投资炼丹/图片/ → 站内互链改成仓库相对路径
  4. 按正文重合度在 reports/ 里找对应的研究原稿
  5. 按标题关键词/原稿目录归到公司子目录，找不到归 综合/
  6. 重新生成 投资炼丹/README.md（按公司 + 按时间两张表）

不做 git 操作，跑完自己检查再提交。

用法：
  uv run tools/wechat_archive.py              # 归档新文章并重建 README
  uv run tools/wechat_archive.py --dry-run    # 只列出新文章和拟归档位置
  uv run tools/wechat_archive.py --company 腾讯   # 指定本次新文章的公司目录
  uv run tools/wechat_archive.py --readme-only    # 只重建 README

注意：
  - 原文链接必须保留 chksm，缺了会被微信"环境验证"拦截；scene/sharer 等追踪参数一律去掉。
  - 单篇抓取间隔约 20 秒；连抓二十多篇会被限流约 10 分钟，脚本会自动等待重试。
"""

from __future__ import annotations

import argparse
import collections
import datetime
import difflib
import hashlib
import json
import os
import random
import re
import subprocess
import sys
import time
from pathlib import Path

from bs4 import BeautifulSoup
from markdownify import MarkdownConverter

ROOT = Path(__file__).resolve().parent.parent
ARCHIVE = ROOT / "投资炼丹"
IMG_DIR = ARCHIVE / "图片"
BIZ = "MzIzNjQ4Nzc2OQ=="
ALBUM_ID = "2431718754171666432"
ALBUM_PAGE = f"https://mp.weixin.qq.com/mp/appmsgalbum?__biz={BIZ}&action=getalbum&album_id={ALBUM_ID}"
UA = ("Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 "
      "(KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.47")

# 公司目录顺序；新公司目录会排在 综合 之前
ORDER = ["腾讯", "拼多多", "美团", "阿里巴巴", "快手", "泡泡玛特", "MiniMax", "茅台", "英伟达", "理想汽车", "SpaceX"]
ALIASES = {
    "PDD": "拼多多", "Temu": "拼多多", "微信": "腾讯", "淘天": "阿里巴巴", "阿里": "阿里巴巴",
    "可灵": "快手", "Labubu": "泡泡玛特", "理想": "理想汽车", "外卖": "美团",
}
# reports/ 下的目录名 → 投资炼丹/ 目录名
REPORT_DIR_ALIASES = {"MINIMAX": "MiniMax", "Alibaba": "阿里巴巴"}


# ---------- 抓取 ----------

# curl 超时（秒）。网络卡住时报错退出，而不是无限挂起。
CONNECT_TIMEOUT = 15
MAX_TIME = 60
IMG_MAX_TIME = 120


def _timeouts(max_time: int) -> list[str]:
    return ["--connect-timeout", str(CONNECT_TIMEOUT), "--max-time", str(max_time)]


def curl(url: str) -> str:
    return subprocess.run(["curl", "-sL", *_timeouts(MAX_TIME), "-A", UA, url],
                          capture_output=True, check=True).stdout.decode("utf-8", "ignore")


def album_articles() -> list[dict]:
    base = (f"https://mp.weixin.qq.com/mp/appmsgalbum?action=getalbum&__biz={BIZ.replace('=', '%3D')}"
            f"&album_id={ALBUM_ID}&count=20&f=json")
    out, url = [], base
    for _ in range(50):
        resp = json.loads(curl(url))["getalbum_resp"]
        items = resp.get("article_list") or []
        if isinstance(items, dict):
            items = [items]
        if not items:
            break
        out += items
        if str(resp.get("continue_flag")) != "1":
            break
        last = items[-1]
        url = base + f"&begin_msgid={last['msgid']}&begin_itemidx={last['itemidx']}"
        time.sleep(1)
    arts = {a["key"]: a for a in out}.values()
    res = []
    for a in sorted(arts, key=lambda a: int(a["create_time"])):
        res.append({
            "date": datetime.datetime.fromtimestamp(int(a["create_time"])).strftime("%Y-%m-%d"),
            "title": a["title"].strip(),
            "mid": a["msgid"], "idx": a["itemidx"],
            "url": clean_link(a["url"].replace("http://", "https://")),
        })
    return res


def clean_link(u: str) -> str:
    """保留 __biz/mid/idx/sn/chksm，去掉其余参数和锚点。"""
    u = u.split("#")[0]
    if "?" not in u:
        return u
    base, q = u.split("?", 1)
    keep = [p for p in q.split("&") if p.split("=")[0] in ("__biz", "mid", "idx", "sn", "chksm")]
    return base + "?" + "&".join(keep)


def fetch_article(url: str) -> str:
    for attempt in range(6):
        html = curl(url)
        if 'id="js_content"' in html:
            return html
        print(f"  遇到验证/限流，等 10 分钟重试（第 {attempt + 1} 次）", flush=True)
        time.sleep(600)
    raise RuntimeError(f"多次重试仍被拦截：{url}")


# ---------- 转 Markdown ----------

class _Conv(MarkdownConverter):
    def convert_img(self, el, text, *args, **kwargs):
        src = el.get("data-src") or el.get("src") or ""
        return f"\n\n![]({src})\n\n" if src.startswith("http") else ""

    def convert_section(self, el, text, *args, **kwargs):
        return f"\n\n{text}\n\n"

    def convert_span(self, el, text, *args, **kwargs):
        return text


def html_to_md(html: str) -> str:
    c = BeautifulSoup(html, "html.parser").select_one("#js_content")
    for t in c.select("script,style,mpvoice,mp-common-profile,qqmusic"):
        t.decompose()
    # 合并相邻的同类强调标签，避免 *a**b* / **a****b**
    for tag in ("em", "i", "strong", "b"):
        for el in c.find_all(tag):
            nxt = el.next_sibling
            while nxt is not None and getattr(nxt, "name", None) == tag:
                for ch in list(nxt.contents):
                    el.append(ch)
                nxt.decompose()
                nxt = el.next_sibling
    md = _Conv(heading_style="ATX", bullets="-", strong_em_symbol="*").convert(str(c))
    md = md.replace(" ", " ").replace("​", "")
    md = re.sub(r"[ \t]+\n", "\n", md)
    md = re.sub(r"\n{3,}", "\n\n", md)
    md = re.sub(r"\*\*\s*\*\*", "", md)
    # GitHub 中文加粗：收尾 ** 前的标点移到外面；开头 ** 后紧跟引号括号时前面补空格
    md = re.sub(r"\*\*([^*\n]+?)([。，、；：！？”’）》]+)\*\*", r"**\1**\2", md)
    md = re.sub(r"(?<=[一-鿿])\*\*(?=[“‘（《])", " **", md)
    return md.strip()


def tidy_body(md: str, title: str) -> str:
    lines = md.split("\n")
    if lines and lines[0].startswith("#") and similar(lines[0].lstrip("# "), title) > 0.8:
        md = "\n".join(lines[1:]).lstrip()
    if re.search(r"^# ", md, re.M):  # 正文只留二级及以下标题
        md = re.sub(r"^(#{1,5}) ", lambda m: "#" + m.group(1) + " ", md, flags=re.M)
    return md


def localize_images(md: str, date: str) -> str:
    IMG_DIR.mkdir(parents=True, exist_ok=True)

    def repl(m):
        u = m.group(1)
        path = IMG_DIR / f"{date.replace('-', '')}-{hashlib.md5(u.encode()).hexdigest()[:8]}"
        tmp = path.with_suffix(".tmp")
        subprocess.run(["curl", "-sL", *_timeouts(IMG_MAX_TIME), "-e", "https://mp.weixin.qq.com/",
                        "-o", str(tmp), u], check=True)
        kind = subprocess.run(["file", "-b", str(tmp)], capture_output=True, text=True).stdout
        ext = "png" if "PNG" in kind else "gif" if "GIF" in kind else "webp" if "Web/P" in kind else "jpg"
        final = path.with_suffix("." + ext)
        tmp.replace(final)
        return f"![](../图片/{final.name})"

    return re.sub(r"!\[\]\((https?://mmbiz[^)]+)\)", repl, md)


def relink(md: str, here: Path, bymid: dict) -> str:
    def repl(m):
        u = m.group(1)
        mid, idx = re.search(r"mid=(\d+)", u), re.search(r"idx=(\d+)", u)
        key = (mid.group(1), idx.group(1) if idx else "1") if mid else None
        if key in bymid:
            return "(" + os.path.relpath(bymid[key], here.parent) + ")"
        return "(" + clean_link(u) + ")"
    return re.sub(r"\((https?://mp\.weixin\.qq\.com/[^)\s]+)\)", repl, md)


# ---------- 原稿匹配 ----------

def similar(a: str, b: str) -> float:
    return difflib.SequenceMatcher(None, a, b).ratio()


def _plain(s: str) -> str:
    s = re.sub(r"^>.*\n", "", s, flags=re.M)
    return re.sub(r"[\s#*|>\-]", "", s)


def _grams(s: str) -> set:
    return {s[i:i + 5] for i in range(0, len(s) - 5, 3)}


def best_drafts(md: str, top: int = 3) -> list[tuple[float, str]]:
    A = _grams(_plain(md))
    if not A:
        return []
    scores = []
    for p in (ROOT / "reports").rglob("*.md"):
        if p.stat().st_size < 1500:
            continue
        B = _grams(_plain(p.read_text("utf-8", "ignore")))
        scores.append((len(A & B) / len(A), str(p.relative_to(ROOT))))
    return sorted(scores, reverse=True)[:top]


# ---------- 归类 ----------

def guess_company(title: str, draft: str | None) -> str:
    existing = [d.name for d in ARCHIVE.iterdir() if d.is_dir() and d.name not in ("图片", "综合")]
    for name in sorted(set(existing) | set(ORDER), key=len, reverse=True):
        if name.lower() in title.lower():
            return name
    for k, v in ALIASES.items():
        if k in title:
            return v
    if draft and draft.startswith("reports/"):
        parts = draft.split("/")
        if len(parts) > 2:
            d = REPORT_DIR_ALIASES.get(parts[1], parts[1])
            if d in existing or d in ORDER:
                return d
    return "综合"


def fname(date: str, title: str) -> str:
    return f"{date.replace('-', '')}-" + re.sub(r'[\\/:*?"<>|：？“”，,、—\s]+', "-", title).strip("-") + ".md"


# ---------- 已有文章 / README ----------

def read_existing() -> list[dict]:
    rows = []
    for f in sorted(ARCHIVE.glob("*/*.md")):
        s = f.read_text("utf-8")
        m = re.search(r"> 公众号发表：(\S+)｜发表标题：(.+)", s)
        if not m:
            front = re.match(r"\A---\s*\n(.*?)\n---\s*\n", s, re.S)
            metadata = dict(re.findall(r"^(wechat_status|source_report):\s*(.+)$", front.group(1), re.M)) if front else {}
            title = re.search(r"^#\s+(.+)$", s, re.M)
            date = re.match(r"(\d{4})(\d{2})(\d{2})-", f.name)
            if metadata.get("wechat_status") == "待发布" and title and date:
                rows.append({"date": "-".join(date.groups()), "title": title.group(1).strip(),
                             "url": "", "src": metadata.get("source_report"), "note": "公众号定稿，待发布",
                             "company": f.parent.name, "path": f, "key": None, "status": "待发布"})
            continue
        u = re.search(r"> 公众号原文：(\S+)", s)
        src = re.search(r"> 原稿：\[([^\]]+)\]", s)
        note = re.search(r"> 备注：(.+)", s)
        url = u.group(1) if u else ""
        mid, idx = re.search(r"mid=(\d+)", url), re.search(r"idx=(\d+)", url)
        rows.append({
            "date": m.group(1), "title": m.group(2).strip(), "url": url,
            "src": src.group(1) if src else None, "note": note.group(1).strip() if note else "",
            "company": f.parent.name, "path": f,
            "key": (mid.group(1), idx.group(1)) if mid and idx else None,
        })
    return rows


def write_readme(rows: list[dict]) -> None:
    ready = [r for r in rows if r.get("status") == "待发布"]
    rows = [r for r in rows if r.get("status") != "待发布"]
    companies = {r["company"] for r in rows}
    order = [c for c in ORDER if c in companies] + sorted(companies - set(ORDER) - {"综合"}) + (["综合"] if "综合" in companies else [])
    groups = collections.defaultdict(list)
    for r in sorted(rows, key=lambda r: r["date"]):
        groups[r["company"]].append(r)
    esc = lambda x: x.replace("|", "｜")
    rel = lambda r: r["path"].relative_to(ARCHIVE).as_posix()
    src = lambda r: f"[{os.path.basename(r['src'])}](../{r['src']})" if r["src"] else "—"
    today = datetime.date.today().isoformat()
    L = ["# 投资炼丹", "",
         "微信公众号文章归档，按公司分目录。已发表文章抓取自「投资炼丹」合集，附公众号原文及研究原稿；待发布定稿单列，日期为定稿日期。", "",
         f"合集页：[投资炼丹]({ALBUM_PAGE})", "",
         "- 文件名：`日期-标题.md`；已发表文章使用发表日期，待发布定稿使用定稿日期",
         "- 正文里的图片存在 `图片/`，不依赖微信图床",
         "- 跨公司的方法、行业、大师持仓类文章放 `综合/`", "",
         f"已发表 {len(rows)} 篇，待发布定稿 {len(ready)} 篇，最近更新 {today}。发表版与原稿重合度低的，说明发表前改动较大，原稿仅供对照。", ""]
    if ready:
        L += ["## 待发布定稿", "", "| 定稿日期 | 公司 | 标题 | 原稿 | 状态 |", "|---|---|---|---|---|"]
        for r in sorted(ready, key=lambda r: r["date"], reverse=True):
            L.append(f"| {r['date']} | {r['company']} | [{esc(r['title'])}]({rel(r)}) | {src(r)} | 待发布 |")
        L.append("")
    L += ["## 按公司", ""]
    for c in order:
        L += [f"### {c}（{len(groups[c])}篇）", "", "| 日期 | 发表标题 | 原文 | 原稿 | 备注 |", "|---|---|---|---|---|"]
        for r in groups[c]:
            L.append(f"| {r['date']} | [{esc(r['title'])}]({rel(r)}) | [原文]({r['url']}) | {src(r)} | {r['note']} |")
        L.append("")
    L += ["## 按时间", "", "| 日期 | 公司 | 发表标题 | 原文 |", "|---|---|---|---|"]
    for r in sorted(rows, key=lambda r: r["date"]):
        L.append(f"| {r['date']} | {r['company']} | [{esc(r['title'])}]({rel(r)}) | [原文]({r['url']}) |")
    (ARCHIVE / "README.md").write_text("\n".join(L) + "\n", "utf-8")


# ---------- 主流程 ----------

def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--dry-run", action="store_true", help="只列出新文章，不写文件")
    ap.add_argument("--company", help="指定本次新文章归入的公司目录")
    ap.add_argument("--readme-only", action="store_true", help="只重建 README")
    args = ap.parse_args()

    existing = read_existing()
    if args.readme_only:
        write_readme(existing)
        print(f"README 已重建，共 {len(existing)} 篇")
        return

    known = {r["key"] for r in existing}
    arts = album_articles()
    new = [a for a in arts if (a["mid"], a["idx"]) not in known]
    print(f"合集共 {len(arts)} 篇，已归档 {len(existing)} 篇，新文章 {len(new)} 篇")
    if not new:
        write_readme(existing)
        return

    bymid = {r["key"]: r["path"] for r in existing if r["key"]}
    plans = []
    for i, a in enumerate(new):
        if i:
            time.sleep(15 + random.random() * 10)
        print(f"- {a['date']} {a['title']}", flush=True)
        md = html_to_md(fetch_article(a["url"]))
        drafts = best_drafts(md)
        draft = drafts[0][1] if drafts and drafts[0][0] >= 0.1 else None
        company = args.company or guess_company(a["title"], draft)
        path = ARCHIVE / company / fname(a["date"], a["title"])
        bymid[(a["mid"], a["idx"])] = path
        for score, p in drafts:
            print(f"    原稿候选 {score:.2f} {p}")
        print(f"    → {path.relative_to(ROOT)}")
        plans.append((a, md, draft, drafts[0][0] if drafts else 0, path))

    if args.dry_run:
        return

    for a, md, draft, score, path in plans:
        body = relink(localize_images(tidy_body(md, a["title"]), a["date"]), path, bymid)
        head = [f"> 公众号发表：{a['date']}｜发表标题：{a['title']}", f"> 公众号原文：{a['url']}"]
        if draft:
            head.append(f"> 原稿：[{draft}](../../{draft})")
            if score < 0.3:
                head.append(f"> 备注：发表版与原稿重合度 {score:.2f}，发表前改动较大")
        else:
            head.append("> 备注：仓库里没有找到对应的原稿")
        head.append("> 以下正文抓取自公众号发表版本。")
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("\n".join(head) + f"\n\n# {a['title']}\n\n{body}\n", "utf-8")

    write_readme(read_existing())
    print(f"完成：新增 {len(plans)} 篇，README 已重建")


if __name__ == "__main__":
    sys.exit(main())
