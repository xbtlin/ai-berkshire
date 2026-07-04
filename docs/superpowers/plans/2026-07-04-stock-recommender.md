# 股票推荐系统（稳定收益 MVP）实施计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 在 `tools/stock_recommender.py`（单文件 CLI）实现 A 股稳定收益推荐：扫描中证红利 + 上证 50 成分股（约 100 只），按 4 维硬指标（股息率 TTM / PE / ROE 均值 / ROE 稳定性）打分，叠加 fin_ai 观点层，输出 Markdown 报告到 `reports/股票推荐/stable-{YYYYMMDD}.md`。

**Architecture:** 单文件 Python CLI（约 300 行），内部 5 步流水线：成分股加载 → 基本面拉取（urllib.request + 东财/腾讯 API）→ 4 维打分 → fin_ai 批量观点 → Markdown 报告。错误降级策略：单股失败跳过、fin_ai 配额耗尽降级为纯硬指标。

**Tech Stack:** Python >= 3.8、stdlib `urllib.request` + `json` + `argparse`（零外部依赖）、`tools/fin_ai`（已存在，观点层）、`pytest`（unit test）。

**Spec 来源:** `docs/superpowers/specs/2026-07-04-stock-recommender-design.md`

**Windows 提示:** 所有命令在 Git Bash 下运行；Python 用 `python`，不用 `python3`；测试用 `python -m pytest`，不用 `pytest` 直接调（避免 PATH 问题）；中文路径必须加引号。

---

## 文件结构总览

| 文件 | 操作 | 责任 |
|------|------|------|
| `tools/stock_recommender.py` | 创建 | 单文件 CLI：成分股加载 + 基本面拉取 + 打分 + fin_ai 观点 + 报告 |
| `tests/fin_ai/test_stock_recommender.py` | 创建 | 10 个 unit case（评分逻辑 + 排序 + 报告渲染） |
| `data/index_constituents.json` | 创建 | 中证红利 + 上证 50 成分股基线（约 100 只代码） |
| `reports/股票推荐/.gitkeep` | 创建 | 占位，让目录进仓库 |
| `skills/stock-recommend.md` | 创建 | slash command prompt，调用 CLI |
| `CLAUDE.md` | 修改 | Skills 全景表新增 `/stock-recommend` 行 |

---

## Task 1: 项目骨架 + 成分股基线 + 测试目录

**Files:**
- Create: `tools/stock_recommender.py`（占位骨架）
- Create: `data/index_constituents.json`（基线数据）
- Create: `reports/股票推荐/.gitkeep`（占位）
- Create: `tests/fin_ai/test_stock_recommender.py`（占位测试，先确认 pytest 能跑）

- [ ] **Step 1: 创建目录结构**

```bash
mkdir -p "reports/股票推荐"
```

- [ ] **Step 2: 写 `tools/stock_recommender.py` 占位骨架**

文件 `tools/stock_recommender.py`：

```python
#!/usr/bin/env python3
"""stock_recommender.py — A 股稳定收益推荐 CLI。

用法：
    python tools/stock_recommender.py stable
    python tools/stock_recommender.py stable --top 5 --min-dividend 4 --max-pe 15
    python tools/stock_recommender.py stable --dry-run
    python tools/stock_recommender.py stable --force

依赖：Python >= 3.8，仅 stdlib（urllib.request / json / argparse）。
"""

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.parse import urlencode
from decimal import Decimal, getcontext
from statistics import stdev

REPO_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = REPO_ROOT / "data"
REPORTS_DIR = REPO_ROOT / "reports" / "股票推荐"
INDEX_FILE = DATA_DIR / "index_constituents.json"


def main():
    parser = argparse.ArgumentParser(description="A 股股票推荐 CLI")
    sub = parser.add_subparsers(dest="mode", required=True)
    p_stable = sub.add_parser("stable", help="稳定收益模式（高股息+低PE+稳定ROE）")
    p_stable.add_argument("--top", type=int, default=5, help="Top N 推荐（默认 5）")
    p_stable.add_argument("--min-dividend", type=float, default=4.0, help="股息率下限 %（默认 4.0）")
    p_stable.add_argument("--max-pe", type=float, default=15.0, help="PE 上限（默认 15.0）")
    p_stable.add_argument("--min-roe", type=float, default=12.0, help="ROE 下限 %（默认 12.0）")
    p_stable.add_argument("--dry-run", action="store_true", help="仅打印不写文件")
    p_stable.add_argument("--force", action="store_true", help="覆盖当日报告")
    args = parser.parse_args()
    print(f"[stub] mode={args.mode}", file=sys.stderr)
    sys.exit(0)


if __name__ == "__main__":
    main()
```

- [ ] **Step 3: 写 `data/index_constituents.json` 基线**

文件 `data/index_constituents.json`（中证红利 + 上证 50，按代码聚合，名字仅用于人读）：

```json
{
  "_meta": {
    "version": "2026-07-04-baseline",
    "note": "中证红利（000922）+ 上证 50（000016）成分股基线，每年 6 月指数调整后手动更新",
    "sources": ["中证指数公司", "上海证券交易所"]
  },
  "csi_dividend": [
    {"code": "600000", "name": "浦发银行"},
    {"code": "600016", "name": "民生银行"},
    {"code": "600028", "name": "中国石化"},
    {"code": "600029", "name": "南方航空"},
    {"code": "600030", "name": "中信证券"},
    {"code": "600036", "name": "招商银行"},
    {"code": "600048", "name": "保利发展"},
    {"code": "600050", "name": "中国联通"},
    {"code": "600085", "name": "同仁堂"},
    {"code": "600089", "name": "特变电工"},
    {"code": "600104", "name": "上汽集团"},
    {"code": "600188", "name": "兖矿能源"},
    {"code": "600276", "name": "恒瑞医药"},
    {"code": "600309", "name": "万华化学"},
    {"code": "600325", "name": "华发股份"},
    {"code": "600346", "name": "恒力石化"},
    {"code": "600406", "name": "国电南瑞"},
    {"code": "600438", "name": "通威股份"},
    {"code": "600519", "name": "贵州茅台"},
    {"code": "600580", "name": "卧龙电驱"},
    {"code": "600585", "name": "海螺水泥"},
    {"code": "600598", "name": "北大荒"},
    {"code": "600600", "name": "青岛啤酒"},
    {"code": "600674", "name": "川投能源"},
    {"code": "600690", "name": "海尔智家"},
    {"code": "600703", "name": "三安光电"},
    {"code": "600741", "name": "华域汽车"},
    {"code": "600776", "name": "东方通信"},
    {"code": "600886", "name": "国投电力"},
    {"code": "600887", "name": "伊利股份"},
    {"code": "600900", "name": "长江电力"},
    {"code": "600919", "name": "江苏银行"},
    {"code": "600926", "name": "杭州银行"},
    {"code": "600958", "name": "东方证券"},
    {"code": "600999", "name": "招商证券"},
    {"code": "601006", "name": "大秦铁路"},
    {"code": "601088", "name": "中国神华"},
    {"code": "601111", "name": "中国国航"},
    {"code": "601166", "name": "兴业银行"},
    {"code": "601169", "name": "北京银行"},
    {"code": "601225", "name": "陕西煤业"},
    {"code": "601288", "name": "农业银行"},
    {"code": "601318", "name": "中国平安"},
    {"code": "601328", "name": "交通银行"},
    {"code": "601333", "name": "广深铁路"},
    {"code": "601336", "name": "新华保险"},
    {"code": "601377", "name": "兴业证券"},
    {"code": "601390", "name": "中国中铁"},
    {"code": "601398", "name": "工商银行"},
    {"code": "601528", "name": "瑞丰银行"},
    {"code": "601618", "name": "中国中冶"},
    {"code": "601628", "name": "中国人寿"},
    {"code": "601633", "name": "长城汽车"},
    {"code": "601668", "name": "中国建筑"},
    {"code": "601669", "name": "中国电建"},
    {"code": "601688", "name": "华泰证券"},
    {"code": "601727", "name": "上海电气"},
    {"code": "601766", "name": "中国中车"},
    {"code": "601788", "name": "光大证券"},
    {"code": "601800", "name": "中国交建"},
    {"code": "601818", "name": "光大银行"},
    {"code": "601838", "name": "成都银行"},
    {"code": "601857", "name": "中国石油"},
    {"code": "601881", "name": "中国银河"},
    {"code": "601888", "name": "中国中免"},
    {"code": "601919", "name": "中远海控"},
    {"code": "601939", "name": "建设银行"},
    {"code": "601985", "name": "中国核电"},
    {"code": "601988", "name": "中国银行"},
    {"code": "601989", "name": "中国重工"},
    {"code": "601998", "name": "中信银行"},
    {"code": "603259", "name": "药明康德"},
    {"code": "603288", "name": "福耀玻璃"},
    {"code": "603501", "name": "韦尔股份"},
    {"code": "603993", "name": "洛阳钼业"}
  ],
  "sse_50": [
    {"code": "600000", "name": "浦发银行"},
    {"code": "600016", "name": "民生银行"},
    {"code": "600028", "name": "中国石化"},
    {"code": "600030", "name": "中信证券"},
    {"code": "600036", "name": "招商银行"},
    {"code": "600048", "name": "保利发展"},
    {"code": "600050", "name": "中国联通"},
    {"code": "600085", "name": "同仁堂"},
    {"code": "600089", "name": "特变电工"},
    {"code": "600104", "name": "上汽集团"},
    {"code": "600196", "name": "复星医药"},
    {"code": "600276", "name": "恒瑞医药"},
    {"code": "600309", "name": "万华化学"},
    {"code": "600406", "name": "国电南瑞"},
    {"code": "600438", "name": "通威股份"},
    {"code": "600519", "name": "贵州茅台"},
    {"code": "600585", "name": "海螺水泥"},
    {"code": "600588", "name": "用友网络"},
    {"code": "600590", "name": "五矿发展"},
    {"code": "600600", "name": "青岛啤酒"},
    {"code": "600690", "name": "海尔智家"},
    {"code": "600745", "name": "闻泰科技"},
    {"code": "600809", "name": "山西汾酒"},
    {"code": "600837", "name": "海通证券"},
    {"code": "600887", "name": "伊利股份"},
    {"code": "600900", "name": "长江电力"},
    {"code": "600918", "name": "中泰证券"},
    {"code": "600919", "name": "江苏银行"},
    {"code": "600926", "name": "杭州银行"},
    {"code": "600941", "name": "中国移动"},
    {"code": "601012", "name": "隆基绿能"},
    {"code": "601066", "name": "中信建投"},
    {"code": "601088", "name": "中国神华"},
    {"code": "601138", "name": "工业富联"},
    {"code": "601155", "name": "新城控股"},
    {"code": "601166", "name": "兴业银行"},
    {"code": "601169", "name": "北京银行"},
    {"code": "601225", "name": "陕西煤业"},
    {"code": "601288", "name": "农业银行"},
    {"code": "601318", "name": "中国平安"},
    {"code": "601328", "name": "交通银行"},
    {"code": "601398", "name": "工商银行"},
    {"code": "601601", "name": "中国太保"},
    {"code": "601628", "name": "中国人寿"},
    {"code": "601633", "name": "长城汽车"},
    {"code": "601668", "name": "中国建筑"},
    {"code": "601688", "name": "华泰证券"},
    {"code": "601728", "name": "中国电信"},
    {"code": "601766", "name": "中国中车"},
    {"code": "601800", "name": "中国交建"},
    {"code": "601818", "name": "光大银行"},
    {"code": "601857", "name": "中国石油"},
    {"code": "601888", "name": "中国中免"},
    {"code": "601919", "name": "中远海控"},
    {"code": "601939", "name": "建设银行"},
    {"code": "601985", "name": "中国核电"},
    {"code": "601988", "name": "中国银行"},
    {"code": "601998", "name": "中信银行"},
    {"code": "603259", "name": "药明康德"},
    {"code": "603501", "name": "韦尔股份"},
    {"code": "603986", "name": "兆易创新"}
  ]
}
```

> 注：上面是 2025-07 已知的常见成分股样本。**真实成分股以指数公司公布为准，此基线用于 MVP 跑通，后续由用户手动校正**。

- [ ] **Step 4: 写 `reports/股票推荐/.gitkeep`**

文件 `reports/股票推荐/.gitkeep`（空文件，仅占位）：

```
```

- [ ] **Step 5: 写 `tests/fin_ai/test_stock_recommender.py` 占位测试**

文件 `tests/fin_ai/test_stock_recommender.py`：

```python
"""占位测试：确认 pytest 能识别本文件。Task 6 起填实质用例。"""


def test_placeholder():
    assert True
```

- [ ] **Step 6: 跑占位测试，确认 pytest 工作**

Run:
```bash
python -m pytest tests/fin_ai/test_stock_recommender.py -v
```

Expected: `1 passed`

- [ ] **Step 7: 跑 CLI 骨架，确认 argparse 工作**

Run:
```bash
python tools/stock_recommender.py stable --top 3
```

Expected: stderr 显示 `[stub] mode=stable`，退出码 0。

Run:
```bash
python tools/stock_recommender.py --help
```

Expected: 显示 argparse 帮助。

- [ ] **Step 8: Commit**

```bash
git add tools/stock_recommender.py data/index_constituents.json "reports/股票推荐/.gitkeep" tests/fin_ai/test_stock_recommender.py
git commit -m "feat(stock-recommender): 项目骨架 + 成分股基线 + 测试目录占位"
```

---

## Task 2: 加载成分股 + 去重

**Files:**
- Modify: `tools/stock_recommender.py`（新增 `load_index_constituents()`）
- Modify: `tests/fin_ai/test_stock_recommender.py`（新增 1 个测试）

- [ ] **Step 1: 写测试**

在 `tests/fin_ai/test_stock_recommender.py` 末尾追加：

```python
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(REPO_ROOT))

from tools.stock_recommender import load_index_constituents


def test_load_index_constituents_returns_unique_codes():
    """加载成分股：返回去重后的代码列表，格式为 6 位字符串。"""
    codes = load_index_constituents()
    # 中证红利 + 上证 50 去重后总数应在 70-100 之间
    assert 70 <= len(codes) <= 100, f"实际数量: {len(codes)}"
    # 全部是 6 位数字
    assert all(len(c) == 6 and c.isdigit() for c in codes), "代码必须是 6 位数字"
    # 无重复
    assert len(codes) == len(set(codes)), "代码必须去重"
    # 应包含招行（必在两个指数里）
    assert "600036" in codes, "应包含招行"
```

把占位 `test_placeholder` 删掉。

- [ ] **Step 2: 跑测试，确认失败**

Run:
```bash
python -m pytest tests/fin_ai/test_stock_recommender.py -v
```

Expected: FAIL with `ImportError: cannot import name 'load_index_constituents'`

- [ ] **Step 3: 实现 `load_index_constituents()`**

在 `tools/stock_recommender.py` 的 `main()` 上方插入：

```python
def load_index_constituents():
    """加载中证红利 + 上证 50 成分股，返回去重后的 6 位代码列表。

    数据源：data/index_constituents.json（本地基线）。
    失败时抛异常，由 main() 统一处理。
    """
    with open(INDEX_FILE, encoding="utf-8") as f:
        data = json.load(f)
    seen = set()
    codes = []
    for key in ("csi_dividend", "sse_50"):
        for entry in data.get(key, []):
            code = entry["code"].strip()
            if code and code not in seen:
                seen.add(code)
                codes.append(code)
    return codes
```

- [ ] **Step 4: 跑测试，确认通过**

Run:
```bash
python -m pytest tests/fin_ai/test_stock_recommender.py -v
```

Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add tools/stock_recommender.py tests/fin_ai/test_stock_recommender.py
git commit -m "feat(stock-recommender): load_index_constituents 加载成分股"
```

---

## Task 3: HTTP 工具函数 + 腾讯行情拉取（fetch_quote）

**Files:**
- Modify: `tools/stock_recommender.py`（新增 `_http_get()` + `_qq_code()` + `fetch_quote()`）
- Modify: `tests/fin_ai/test_stock_recommender.py`（新增 2 个测试）

> **工程决策**：用 stdlib `urllib.request`，零依赖。腾讯行情返回 GBK，注意解码。

- [ ] **Step 1: 写测试**

在 `tests/fin_ai/test_stock_recommender.py` 末尾追加：

```python
from tools.stock_recommender import _qq_code, _parse_qq_quote


def test_qq_code_上海():
    """6 开头代码 → sh 前缀。"""
    assert _qq_code("600036") == "sh600036"


def test_qq_code_深圳():
    """0/3 开头代码 → sz 前缀。"""
    assert _qq_code("000001") == "sz000001"
    assert _qq_code("300750") == "sz300750"


def test_qq_code_去除后缀():
    """带 .SH/.SZ 后缀的代码也要能处理。"""
    assert _qq_code("600036.SH") == "sh600036"


def test_parse_qq_quote_标准格式():
    """能解析腾讯行情返回的 ~ 分隔字符串。"""
    # 简化的样本：50+ 字段，关键字段在固定位置
    raw = '"招商银行~600036~35.50~35.00~36.00~100000~50000~50000~"'
    raw += "~" * 50  # 填充到 50+ 字段
    d = _parse_qq_quote(raw)
    assert d["name"] == "招商银行"
    assert d["code"] == "600036"
    assert d["price"] == "35.50"
```

- [ ] **Step 2: 跑测试，确认失败**

Run:
```bash
python -m pytest tests/fin_ai/test_stock_recommender.py -v
```

Expected: FAIL with `ImportError: cannot import name '_qq_code'`

- [ ] **Step 3: 实现 HTTP 工具 + 解析器**

在 `tools/stock_recommender.py` 的 `load_index_constituents()` 上方插入：

```python
def _http_get(url, timeout=15, encoding="utf-8"):
    """stdlib HTTP GET（无外部依赖，跨平台）。

    返回解码后的字符串。失败抛 ConnectionError。
    """
    req = Request(url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urlopen(req, timeout=timeout) as resp:
            data = resp.read()
    except Exception as e:
        raise ConnectionError(f"HTTP 请求失败: {url} — {e}")
    try:
        return data.decode(encoding)
    except UnicodeDecodeError:
        return data.decode("gbk", errors="replace")


def _qq_code(code: str) -> str:
    """将股票代码转为腾讯行情格式（sh/sz 前缀）。"""
    code = code.strip().replace(".SH", "").replace(".SZ", "").replace(".BJ", "")
    if code.startswith(("6", "9", "5")):
        return f"sh{code}"
    elif code.startswith(("0", "3", "2", "1")):
        return f"sz{code}"
    elif code.startswith(("4", "8")):
        return f"bj{code}"
    return f"sh{code}"


def _parse_qq_quote(raw: str) -> dict:
    """解析腾讯行情返回的 ~ 分隔字符串。

    格式：v_shXXXXXX="字段1~字段2~...~字段N";
    返回关键字段 dict。失败返回空 dict。
    """
    start = raw.find('"')
    end = raw.rfind('"')
    if start < 0 or end <= start:
        return {}
    fields = raw[start + 1:end].split("~")
    if len(fields) < 9:
        return {}
    return {
        "name": fields[1],
        "code": fields[2],
        "price": fields[3],
        "prev_close": fields[4],
        "pe": fields[39] if len(fields) > 39 else "-",
        "market_cap_yi": fields[45] if len(fields) > 45 else "-",  # 单位：亿
        "pb": fields[46] if len(fields) > 46 else "-",
    }
```

- [ ] **Step 4: 跑测试，确认通过**

Run:
```bash
python -m pytest tests/fin_ai/test_stock_recommender.py -v
```

Expected: 5 个 case 全 PASS

- [ ] **Step 5: 实现 `fetch_quote()`**

在 `_parse_qq_quote` 下方追加：

```python
def fetch_quote(code: str) -> dict:
    """拉腾讯行情：PE / PB / 当前价 / 总市值（亿）。失败抛 ConnectionError。"""
    raw = _http_get(f"https://qt.gtimg.cn/q={_qq_code(code)}")
    return _parse_qq_quote(raw)
```

- [ ] **Step 6: 手动验证 `fetch_quote`**

Run:
```bash
python -c "import sys; sys.path.insert(0, '.'); from tools.stock_recommender import fetch_quote; print(fetch_quote('600036'))"
```

Expected: 输出含 `name='招商银行'`, `price`, `pe` 等字段的 dict。

> ⚠️ 如果网络失败：跳过手动验证，Step 7 直接 commit（CI 环境会跑 unit test）。

- [ ] **Step 7: Commit**

```bash
git add tools/stock_recommender.py tests/fin_ai/test_stock_recommender.py
git commit -m "feat(stock-recommender): HTTP 工具 + 腾讯行情拉取"
```

---

## Task 4: 东财财务拉取（fetch_financials）

**Files:**
- Modify: `tools/stock_recommender.py`（新增 `fetch_financials()`）
- Modify: `tests/fin_ai/test_stock_recommender.py`（新增 2 个测试）

> **数据源**：东方财富 datacenter API（`RPT_F10_FINANCE_MAINFINADATA`），返回近 5 年年报。关键字段：`ROEJQ`（ROE 加权）。

- [ ] **Step 1: 写测试**

在测试文件末尾追加：

```python
from tools.stock_recommender import extract_roe_history


def test_extract_roe_history_正常数据():
    """从东财 API 响应里抽出近 N 年 ROE（按日期降序）。"""
    api_response = {
        "result": {
            "data": [
                {"REPORT_DATE": "2024-12-31T00:00:00", "ROEJQ": 16.5, "REPORT_TYPE": "年报"},
                {"REPORT_DATE": "2023-12-31T00:00:00", "ROEJQ": 15.8, "REPORT_TYPE": "年报"},
                {"REPORT_DATE": "2022-12-31T00:00:00", "ROEJQ": 14.2, "REPORT_TYPE": "年报"},
                {"REPORT_DATE": "2021-12-31T00:00:00", "ROEJQ": 13.9, "REPORT_TYPE": "年报"},
            ]
        }
    }
    roes = extract_roe_history(api_response, years=3)
    assert roes == [16.5, 15.8, 14.2]


def test_extract_roe_history_空数据():
    """API 返回空数据时返回空列表。"""
    assert extract_roe_history({"result": {"data": []}}, years=3) == []
    assert extract_roe_history({}, years=3) == []
```

- [ ] **Step 2: 跑测试，确认失败**

Run:
```bash
python -m pytest tests/fin_ai/test_stock_recommender.py -v
```

Expected: FAIL with `ImportError: cannot import name 'extract_roe_history'`

- [ ] **Step 3: 实现 `extract_roe_history()` + `fetch_financials()`**

在 `fetch_quote()` 下方追加：

```python
def extract_roe_history(api_response: dict, years: int = 3) -> list:
    """从东财 financials API 响应提取近 N 年 ROE（按日期降序）。

    输入：完整的 API JSON 响应。
    输出：[ROE_最新年, ROE_去年, ROE_前年]（单位 %）。
    无数据返回空列表。
    """
    data = (api_response.get("result") or {}).get("data") or []
    annual = [r for r in data if r.get("REPORT_TYPE") == "年报" and r.get("ROEJQ") is not None]
    annual.sort(key=lambda x: x.get("REPORT_DATE", ""), reverse=True)
    return [float(r["ROEJQ"]) for r in annual[:years]]


def fetch_financials(code: str, years: int = 3) -> dict:
    """拉东财近 5 年年报财务数据。返回 {roe_history: [...]}。失败抛异常。

    只取年报，按日期降序。
    """
    code = code.strip().replace(".SH", "").replace(".SZ", "").replace(".BJ", "")
    market = "SH" if code.startswith(("6", "9", "5")) else "SZ"
    url = "https://datacenter.eastmoney.com/securities/api/data/get"
    params = {
        "type": "RPT_F10_FINANCE_MAINFINADATA",
        "sty": "ALL",
        "filter": f'(SECUCODE="{code}.{market}")(REPORT_TYPE="年报")',
        "p": "1", "ps": "5", "sr": "-1", "st": "REPORT_DATE",
        "source": "HSF10", "client": "PC",
    }
    full_url = f"{url}?{urlencode(params)}"
    raw = _http_get(full_url)
    api_response = json.loads(raw)
    return {"roe_history": extract_roe_history(api_response, years=years)}
```

- [ ] **Step 4: 跑测试，确认通过**

Run:
```bash
python -m pytest tests/fin_ai/test_stock_recommender.py -v
```

Expected: 7 个 case 全 PASS

- [ ] **Step 5: 手动验证 `fetch_financials`**

Run:
```bash
python -c "import sys; sys.path.insert(0, '.'); from tools.stock_recommender import fetch_financials; print(fetch_financials('600036'))"
```

Expected: 输出 `{'roe_history': [16.x, 15.x, 14.x]}`（招行近 3 年 ROE）。

- [ ] **Step 6: Commit**

```bash
git add tools/stock_recommender.py tests/fin_ai/test_stock_recommender.py
git commit -m "feat(stock-recommender): 东财财务拉取 + ROE 历史提取"
```

---

## Task 5: 东财 F10 分红拉取（fetch_dividends）+ TTM 股息率计算

**Files:**
- Modify: `tools/stock_recommender.py`（新增 `extract_dividends_ttm()` + `fetch_dividends()` + `calc_dividend_yield()`）
- Modify: `tests/fin_ai/test_stock_recommender.py`（新增 3 个测试）

> **数据源**：东方财富 `RPT_SHAREBONUS_DET` 分红明细 API。每条记录含 `EQUITY_REGISTRATION_DATE`（股权登记日）、`BONUS_RPS`（每10股送股）、`CAPITAL_RPS`（每10股转增）、`BEFORE_TAX_DIVIDEND`（每10股派息税前）。
>
> **TTM 股息率算法**：找最近 365 天内的所有分红记录，把"每 10 股派息"加起来 ÷ 10 ÷ 当前股价。

- [ ] **Step 1: 写测试**

在测试文件末尾追加：

```python
from tools.stock_recommender import (
    extract_dividends_ttm,
    calc_dividend_yield,
)


def test_extract_dividends_ttm_近365天():
    """汇总近 365 天内所有"每10股派息"总额。"""
    today = "2026-07-04"
    api_response = {
        "result": {
            "data": [
                # 假设今天 2026-07-04
                {"EQUITY_REGISTRATION_DATE": "2026-06-15", "BEFORE_TAX_DIVIDEND": 3.0},  # 中期
                {"EQUITY_REGISTRATION_DATE": "2025-07-10", "BEFORE_TAX_DIVIDEND": 5.0},  # 上年年度（< 365 天）
                {"EQUITY_REGISTRATION_DATE": "2025-06-20", "BEFORE_TAX_DIVIDEND": 4.0},  # 超过 365 天，剔除
            ]
        }
    }
    total = extract_dividends_ttm(api_response, today=today)
    assert total == 8.0  # 3 + 5


def test_extract_dividends_ttm_空():
    assert extract_dividends_ttm({}, today="2026-07-04") == 0.0


def test_calc_dividend_yield_标准():
    """股息率 = TTM 每10股派息 ÷ 10 ÷ 当前价 × 100。"""
    # 每 10 股派 5 元，当前价 10 元 → 5%
    rate = calc_dividend_yield(dividend_per_10_ttm=5.0, price=10.0)
    assert abs(rate - 5.0) < 0.01


def test_calc_dividend_yield_零价格():
    """价格为 0 时返回 0（防除零）。"""
    assert calc_dividend_yield(dividend_per_10_ttm=5.0, price=0) == 0.0
```

- [ ] **Step 2: 跑测试，确认失败**

Run:
```bash
python -m pytest tests/fin_ai/test_stock_recommender.py -v
```

Expected: FAIL with `ImportError: cannot import name 'extract_dividends_ttm'`

- [ ] **Step 3: 实现 `extract_dividends_ttm()` + `calc_dividend_yield()` + `fetch_dividends()`**

在 `fetch_financials()` 下方追加：

```python
from datetime import datetime, timedelta


def extract_dividends_ttm(api_response: dict, today: str = None) -> float:
    """汇总近 365 天内"每 10 股派息税前"总额。

    today: 'YYYY-MM-DD' 字符串，默认系统当天。
    返回单位：元（每 10 股）。
    """
    today_dt = datetime.strptime(today, "%Y-%m-%d") if today else datetime.now()
    cutoff = today_dt - timedelta(days=365)
    data = (api_response.get("result") or {}).get("data") or []
    total = 0.0
    for r in data:
        date_str = (r.get("EQUITY_REGISTRATION_DATE") or "")[:10]
        if not date_str:
            continue
        try:
            reg_date = datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            continue
        if reg_date >= cutoff:
            amt = r.get("BEFORE_TAX_DIVIDEND")
            if amt is not None:
                total += float(amt)
    return total


def calc_dividend_yield(dividend_per_10_ttm: float, price: float) -> float:
    """TTM 股息率 %。

    dividend_per_10_ttm: 近 12 个月每 10 股派息合计（元）。
    price: 当前股价（元）。
    返回：股息率百分比（5.0 表示 5%）。
    """
    if not price or price <= 0:
        return 0.0
    return dividend_per_10_ttm / 10.0 / price * 100.0


def fetch_dividends(code: str) -> dict:
    """拉东财 F10 分红明细。返回 {dividend_per_10_ttm: float, raw_records: [...]}。"""
    code = code.strip().replace(".SH", "").replace(".SZ", "").replace(".BJ", "")
    market = "SH" if code.startswith(("6", "9", "5")) else "SZ"
    url = "https://datacenter.eastmoney.com/securities/api/data/get"
    params = {
        "type": "RPT_SHAREBONUS_DET",
        "sty": "ALL",
        "filter": f'(SECUCODE="{code}.{market}")',
        "p": "1", "ps": "20", "sr": "-1", "st": "EQUITY_REGISTRATION_DATE",
        "source": "HSF10", "client": "PC",
    }
    full_url = f"{url}?{urlencode(params)}"
    raw = _http_get(full_url)
    api_response = json.loads(raw)
    return {
        "dividend_per_10_ttm": extract_dividends_ttm(api_response),
        "raw_records": (api_response.get("result") or {}).get("data") or [],
    }
```

- [ ] **Step 4: 跑测试，确认通过**

Run:
```bash
python -m pytest tests/fin_ai/test_stock_recommender.py -v
```

Expected: 11 个 case 全 PASS

- [ ] **Step 5: 手动验证 `fetch_dividends`**

Run:
```bash
python -c "import sys; sys.path.insert(0, '.'); from tools.stock_recommender import fetch_dividends; print(fetch_dividends('600036'))"
```

Expected: 输出含 `dividend_per_10_ttm` 数值（招行约 15-20 元 / 10 股）。

- [ ] **Step 6: Commit**

```bash
git add tools/stock_recommender.py tests/fin_ai/test_stock_recommender.py
git commit -m "feat(stock-recommender): 东财 F10 分红 + TTM 股息率"
```

---

## Task 6: 4 维打分（score_stable）— 核心 TDD

**Files:**
- Modify: `tools/stock_recommender.py`（新增 `score_stable()`）
- Modify: `tests/fin_ai/test_stock_recommender.py`（新增 7 个测试，覆盖 spec §5 全部用例）

> 这是核心业务逻辑，**完整 TDD**：每个 case 都先写测试。打分输入是一个 dict，包含股息率/PE/ROE 序列，输出是 0-4 分 + 详情。

- [ ] **Step 1: 写 7 个测试用例**

在测试文件末尾追加：

```python
from tools.stock_recommender import score_stable


def _fund(dividend_yield, pe, roe_history):
    """构造 score_stable 输入的工厂函数。"""
    return {
        "dividend_yield": dividend_yield,
        "pe": pe,
        "roe_history": roe_history,
    }


def test_score_stable_满分():
    """4 项全过 → 4 分。"""
    fund = _fund(dividend_yield=5.0, pe=10, roe_history=[14.0, 14.5, 13.8])
    result = score_stable(fund, min_dividend=4.0, max_pe=15.0, min_roe=12.0, max_roe_stddev=5.0)
    assert result["score"] == 4
    assert result["details"]["dividend_yield"] is True
    assert result["details"]["pe"] is True
    assert result["details"]["roe_mean"] is True
    assert result["details"]["roe_stable"] is True


def test_score_stable_股息率不达标():
    """股息率 3% < 4% → 该维 0 分。"""
    fund = _fund(dividend_yield=3.0, pe=10, roe_history=[14.0, 14.5, 13.8])
    result = score_stable(fund, min_dividend=4.0, max_pe=15.0, min_roe=12.0, max_roe_stddev=5.0)
    assert result["score"] == 3
    assert result["details"]["dividend_yield"] is False
    assert result["details"]["pe"] is True


def test_score_stable_PE过高():
    """PE 30 > 15 → 该维 0 分。"""
    fund = _fund(dividend_yield=5.0, pe=30, roe_history=[14.0, 14.5, 13.8])
    result = score_stable(fund, min_dividend=4.0, max_pe=15.0, min_roe=12.0, max_roe_stddev=5.0)
    assert result["score"] == 3
    assert result["details"]["pe"] is False


def test_score_stable_ROE低():
    """ROE 8% < 12% → 该维 0 分。"""
    fund = _fund(dividend_yield=5.0, pe=10, roe_history=[8.0, 8.5, 7.8])
    result = score_stable(fund, min_dividend=4.0, max_pe=15.0, min_roe=12.0, max_roe_stddev=5.0)
    assert result["score"] == 3
    assert result["details"]["roe_mean"] is False


def test_score_stable_ROE波动大():
    """ROE 序列 [8%, 15%, 22%]，stddev 7pp > 5pp → 稳定性 0 分。"""
    fund = _fund(dividend_yield=5.0, pe=10, roe_history=[8.0, 15.0, 22.0])
    result = score_stable(fund, min_dividend=4.0, max_pe=15.0, min_roe=12.0, max_roe_stddev=5.0)
    assert result["score"] == 3
    assert result["details"]["roe_stable"] is False


def test_score_stable_招行样本():
    """招行（股息 5.2%, PE 7, ROE 16%, stddev 0.8pp）→ 4 分。"""
    fund = _fund(dividend_yield=5.2, pe=7, roe_history=[16.0, 16.2, 15.8])
    result = score_stable(fund, min_dividend=4.0, max_pe=15.0, min_roe=12.0, max_roe_stddev=5.0)
    assert result["score"] == 4


def test_score_stable_茅台样本():
    """茅台（股息 1%, PE 30, ROE 30%, stddev 1.2pp）→ 股息 0 + PE 0 + ROE 1 + 稳定 1 = 2 分。"""
    fund = _fund(dividend_yield=1.0, pe=30, roe_history=[30.0, 30.5, 29.8])
    result = score_stable(fund, min_dividend=4.0, max_pe=15.0, min_roe=12.0, max_roe_stddev=5.0)
    assert result["score"] == 2
    assert result["details"]["dividend_yield"] is False
    assert result["details"]["pe"] is False
    assert result["details"]["roe_mean"] is True
    assert result["details"]["roe_stable"] is True
```

- [ ] **Step 2: 跑测试，确认失败**

Run:
```bash
python -m pytest tests/fin_ai/test_stock_recommender.py -v
```

Expected: FAIL with `ImportError: cannot import name 'score_stable'`

- [ ] **Step 3: 实现 `score_stable()`**

在 `fetch_dividends()` 下方追加：

```python
def score_stable(
    fund: dict,
    min_dividend: float = 4.0,
    max_pe: float = 15.0,
    min_roe: float = 12.0,
    max_roe_stddev: float = 5.0,
) -> dict:
    """4 维硬指标打分。

    fund: {dividend_yield, pe, roe_history}
        roe_history: 近 3 年 ROE 序列（最新在前），单位 %。
    返回: {score: 0-4, details: {dividend_yield, pe, roe_mean, roe_stable}}
    """
    details = {}
    # 1. 股息率 > 4%
    details["dividend_yield"] = fund.get("dividend_yield", 0) >= min_dividend
    # 2. PE < 15
    pe = fund.get("pe")
    details["pe"] = (pe is not None and 0 < pe <= max_pe)
    # 3. ROE 均值 > 12%
    roe_history = fund.get("roe_history") or []
    if roe_history:
        roe_mean = sum(roe_history) / len(roe_history)
        details["roe_mean"] = roe_mean >= min_roe
        # 4. ROE 稳定性：近 3 年 stddev < 5pp
        if len(roe_history) >= 2:
            details["roe_stable"] = stdev(roe_history) < max_roe_stddev
        else:
            details["roe_stable"] = False
    else:
        details["roe_mean"] = False
        details["roe_stable"] = False
    score = sum(1 for v in details.values() if v)
    return {"score": score, "details": details}
```

- [ ] **Step 4: 跑测试，确认通过**

Run:
```bash
python -m pytest tests/fin_ai/test_stock_recommender.py -v
```

Expected: 18 个 case 全 PASS

- [ ] **Step 5: Commit**

```bash
git add tools/stock_recommender.py tests/fin_ai/test_stock_recommender.py
git commit -m "feat(stock-recommender): 4 维硬指标打分（核心 TDD）"
```

---

## Task 7: 排序与过滤（sort_and_filter）

**Files:**
- Modify: `tools/stock_recommender.py`（新增 `sort_and_filter()`）
- Modify: `tests/fin_ai/test_stock_recommender.py`（新增 2 个测试）

- [ ] **Step 1: 写测试**

```python
from tools.stock_recommender import sort_and_filter


def _scored(code, score, div_yield):
    """构造 sort_and_filter 输入的工厂。"""
    return {"code": code, "score": score, "dividend_yield": div_yield}


def test_sort_and_filter_按分数分组_同分组按股息率降序():
    items = [
        _scored("A", 4, 4.5),
        _scored("B", 4, 6.0),
        _scored("C", 3, 5.0),
        _scored("D", 4, 5.5),
        _scored("E", 2, 8.0),  # 被剔除
    ]
    strong, weak = sort_and_filter(items, min_score=3, top_n=5)
    # 强推荐（4 分），按股息率降序
    assert [x["code"] for x in strong] == ["B", "D", "A"]
    # 备选（3 分）
    assert [x["code"] for x in weak] == ["C"]


def test_sort_and_filter_top_n_截断():
    items = [
        _scored("A", 4, 6.0),
        _scored("B", 4, 5.5),
        _scored("C", 4, 5.0),
        _scored("D", 4, 4.5),
    ]
    strong, weak = sort_and_filter(items, min_score=4, top_n=2)
    assert len(strong) == 2
    assert [x["code"] for x in strong] == ["A", "B"]
    assert weak == []
```

- [ ] **Step 2: 跑测试，确认失败**

Run:
```bash
python -m pytest tests/fin_ai/test_stock_recommender.py -v
```

Expected: FAIL with `ImportError`

- [ ] **Step 3: 实现**

在 `score_stable()` 下方追加：

```python
def sort_and_filter(items: list, min_score: int = 3, top_n: int = 5):
    """分组 + 排序 + 截断。

    items: [{code, score, dividend_yield, ...}]
    返回: (strong, weak)
        strong: score == 4（强烈推荐）的前 top_n 只，按股息率降序
        weak:   score == 3（备选）的前 top_n 只，按股息率降序
    """
    strong = sorted(
        [x for x in items if x["score"] >= 4],
        key=lambda x: x.get("dividend_yield", 0),
        reverse=True,
    )[:top_n]
    weak = sorted(
        [x for x in items if x["score"] == min_score],
        key=lambda x: x.get("dividend_yield", 0),
        reverse=True,
    )[:top_n]
    return strong, weak
```

- [ ] **Step 4: 跑测试，确认通过**

Run:
```bash
python -m pytest tests/fin_ai/test_stock_recommender.py -v
```

Expected: 20 个 case 全 PASS

- [ ] **Step 5: Commit**

```bash
git add tools/stock_recommender.py tests/fin_ai/test_stock_recommender.py
git commit -m "feat(stock-recommender): 排序与过滤（同分按股息率降序）"
```

---

## Task 8: fin_ai 批量观点层（ask_fin_ai_opinion）

**Files:**
- Modify: `tools/stock_recommender.py`（新增 `ask_fin_ai_opinion()`）
- 不写 unit test（外部依赖，按 spec §10 排除）

> **fin_ai 已存在**（`tools/fin_ai`），直接 import 调用。失败时返回空字符串，由 main() 决定是否降级。

- [ ] **Step 1: 实现 `ask_fin_ai_opinion()`**

在 `sort_and_filter()` 下方追加：

```python
def ask_fin_ai_opinion(candidates: list) -> dict:
    """调 fin_ai 批量问 top N 候选股的观点层。

    candidates: [{code, name, score, dividend_yield, pe, roe_mean}]
    返回: {summary: str, warnings: {code: str}, ok: bool, error: str}
        失败时 ok=False，error 描述原因（配额耗尽/超时/网络）。
    """
    if not candidates:
        return {"summary": "", "warnings": {}, "ok": True, "error": ""}
    try:
        from tools.fin_ai import ask, quota
    except ImportError as e:
        return {"summary": "", "warnings": {}, "ok": False,
                "error": f"fin_ai 模块不可用: {e}"}

    # 配额预检
    try:
        q = quota()
        if q.exceeded or q.remaining < 1:
            return {"summary": "", "warnings": {}, "ok": False,
                    "error": f"fin_ai 配额不足（剩余 {q.remaining}/{q.limit}）"}
    except Exception as e:
        # 配额接口失败时容错（不阻塞）
        pass

    lines = ["请评估以下 A 股稳定收益候选股（按稳定性排序）：\n"]
    for i, c in enumerate(candidates, 1):
        lines.append(
            f"{i}. {c.get('name', c['code'])} ({c['code']}) — "
            f"股息率 {c.get('dividend_yield', 0):.2f}%, "
            f"PE {c.get('pe', 'N/A')}, "
            f"ROE 均值 {c.get('roe_mean', 0):.2f}%"
        )
    lines.append("\n请输出：")
    lines.append("1. 按股息可持续性从高到低排序（仅代码）")
    lines.append("2. 每只股的 1 个核心风险（一句话）")
    lines.append("3. 强烈推荐的 top 3 + 应警惕的 bottom 2")
    query = "\n".join(lines)

    try:
        result = ask(query, ttl_hours=24)
        return {"summary": result.content, "warnings": {}, "ok": True, "error": ""}
    except Exception as e:
        return {"summary": "", "warnings": {}, "ok": False,
                "error": f"fin_ai 调用失败: {e}"}
```

- [ ] **Step 2: 手动验证（不写自动测试）**

Run:
```bash
python -c "
import sys
sys.path.insert(0, '.')
from tools.stock_recommender import ask_fin_ai_opinion
candidates = [{'code': '600036', 'name': '招商银行', 'score': 4, 'dividend_yield': 5.2, 'pe': 7, 'roe_mean': 16.0}]
result = ask_fin_ai_opinion(candidates)
print('ok:', result['ok'])
print('error:', result['error'])
print('summary:', result['summary'][:200])
"
```

Expected: `ok=True` + 招行的观点层文本。

> ⚠️ 失败容忍：如果配额耗尽或网络问题，`ok=False` + 错误描述。这是预期降级，**不算测试失败**。

- [ ] **Step 3: Commit**

```bash
git add tools/stock_recommender.py
git commit -m "feat(stock-recommender): fin_ai 批量观点层（含配额预检 + 降级）"
```

---

## Task 9: Markdown 报告生成（generate_report）

**Files:**
- Modify: `tools/stock_recommender.py`（新增 `generate_report()`）
- Modify: `tests/fin_ai/test_stock_recommender.py`（新增 1 个测试）

- [ ] **Step 1: 写测试**

```python
from tools.stock_recommender import generate_report


def test_generate_report_含必要章节():
    """生成的 Markdown 含：标题 / 总结 / Top 推荐 / 备选 / 方法论 / 数据来源。"""
    today = "2026-07-04"
    strong = [{
        "code": "600036", "name": "招商银行", "score": 4,
        "dividend_yield": 5.2, "pe": 7.0, "roe_mean": 16.0,
        "roe_history": [16.0, 16.2, 15.8],
    }]
    weak = [{
        "code": "601398", "name": "工商银行", "score": 3,
        "dividend_yield": 6.0, "pe": 5.5, "roe_mean": 12.5,
        "roe_history": [12.5, 12.8, 12.2],
    }]
    fin_ai_opinion = {"summary": "招行强烈推荐，工行警示不良贷款风险",
                      "warnings": {}, "ok": True, "error": ""}
    md = generate_report(
        today=today,
        strong=strong,
        weak=weak,
        fin_ai_opinion=fin_ai_opinion,
        scanned_count=80,
        thresholds={"min_dividend": 4.0, "max_pe": 15.0, "min_roe": 12.0, "max_roe_stddev": 5.0},
    )
    # 必须含的章节标题
    assert "# 稳定收益推荐" in md
    assert "## 总结" in md
    assert "## Top 推荐" in md
    assert "## 备选" in md
    assert "## fin_ai 观点层" in md
    assert "## 方法论" in md
    assert "## 数据来源" in md
    # 必须含的关键内容
    assert "2026-07-04" in md
    assert "招商银行" in md
    assert "工商银行" in md
    assert "扫描范围" in md  # 扫描数量


def test_generate_report_fin_ai_失败时含warning():
    """fin_ai 失败时报告顶部含 warning。"""
    fin_ai_opinion = {"summary": "", "warnings": {}, "ok": False,
                      "error": "配额不足（剩余 0/80）"}
    md = generate_report(
        today="2026-07-04", strong=[], weak=[],
        fin_ai_opinion=fin_ai_opinion, scanned_count=80,
        thresholds={"min_dividend": 4.0, "max_pe": 15.0, "min_roe": 12.0, "max_roe_stddev": 5.0},
    )
    assert "⚠️" in md or "warning" in md.lower() or "配额不足" in md
```

- [ ] **Step 2: 跑测试，确认失败**

Run:
```bash
python -m pytest tests/fin_ai/test_stock_recommender.py -v
```

Expected: FAIL with `ImportError`

- [ ] **Step 3: 实现 `generate_report()`**

在 `ask_fin_ai_opinion()` 下方追加：

```python
def _fmt_table_row(cells):
    return "| " + " | ".join(str(c) for c in cells) + " |"


def generate_report(
    today: str,
    strong: list,
    weak: list,
    fin_ai_opinion: dict,
    scanned_count: int,
    thresholds: dict,
) -> str:
    """生成稳定收益推荐 Markdown 报告。"""
    lines = []
    lines.append(f"# 稳定收益推荐 — {today}")
    lines.append("")
    lines.append("> 本报告由 `tools/stock_recommender.py stable` 自动生成。仅供参考，不构成投资建议。")
    lines.append("")

    # fin_ai 失败 warning
    if not fin_ai_opinion["ok"]:
        lines.append(f"> ⚠️ **fin_ai 观点层降级**：{fin_ai_opinion['error']}")
        lines.append(">")
        lines.append("> 本期仅含硬指标分析，建议次日重跑或单独调 fin_ai 补充观点。")
        lines.append("")

    # 总结
    lines.append("## 总结")
    lines.append("")
    lines.append(f"- 扫描范围：中证红利 + 上证 50 成分股（共 {scanned_count} 只）")
    lines.append(f"- 筛选阈值：股息率 ≥ {thresholds['min_dividend']}% | PE ≤ {thresholds['max_pe']} | "
                 f"ROE 均值 ≥ {thresholds['min_roe']}% | ROE 标准差 < {thresholds['max_roe_stddev']}pp")
    lines.append(f"- 强烈推荐：{len(strong)} 只 | 备选：{len(weak)} 只")
    lines.append("")

    # Top 推荐
    lines.append("## Top 推荐（4 分）")
    lines.append("")
    if strong:
        lines.append(_fmt_table_row(["代码", "名称", "股息率%", "PE", "ROE 均值%", "ROE 标准差pp"]))
        lines.append(_fmt_table_row(["---", "---", "---", "---", "---", "---"]))
        for s in strong:
            roe_history = s.get("roe_history", [])
            stddev = stdev(roe_history) if len(roe_history) >= 2 else 0
            lines.append(_fmt_table_row([
                s["code"], s.get("name", ""),
                f"{s.get('dividend_yield', 0):.2f}",
                s.get("pe", "-"),
                f"{s.get('roe_mean', 0):.2f}",
                f"{stddev:.2f}",
            ]))
    else:
        lines.append("_本期无 4 分强推荐_")
    lines.append("")

    # 备选
    lines.append("## 备选（3 分）")
    lines.append("")
    if weak:
        lines.append(_fmt_table_row(["代码", "名称", "股息率%", "PE", "ROE 均值%", "ROE 标准差pp"]))
        lines.append(_fmt_table_row(["---", "---", "---", "---", "---", "---"]))
        for s in weak:
            roe_history = s.get("roe_history", [])
            stddev = stdev(roe_history) if len(roe_history) >= 2 else 0
            lines.append(_fmt_table_row([
                s["code"], s.get("name", ""),
                f"{s.get('dividend_yield', 0):.2f}",
                s.get("pe", "-"),
                f"{s.get('roe_mean', 0):.2f}",
                f"{stddev:.2f}",
            ]))
    else:
        lines.append("_本期无 3 分备选_")
    lines.append("")

    # fin_ai 观点层
    lines.append("## fin_ai 观点层")
    lines.append("")
    if fin_ai_opinion["ok"] and fin_ai_opinion["summary"]:
        lines.append(fin_ai_opinion["summary"])
    else:
        lines.append("_观点层未启用（见顶部 warning）_")
    lines.append("")

    # 方法论
    lines.append("## 方法论")
    lines.append("")
    lines.append("**4 维硬指标打分（4 分制）**：")
    lines.append("")
    lines.append(f"- 股息率（TTM）≥ {thresholds['min_dividend']}% — 1 分")
    lines.append(f"- PE（动）≤ {thresholds['max_pe']} — 1 分")
    lines.append(f"- ROE 近 3 年均值 ≥ {thresholds['min_roe']}% — 1 分")
    lines.append(f"- ROE 近 3 年标准差 < {thresholds['max_roe_stddev']}pp — 1 分")
    lines.append("")
    lines.append("**推荐阈值**：4 分=强烈推荐 | 3 分=备选 | < 3 分=剔除。同分按股息率降序。")
    lines.append("")

    # 数据来源
    lines.append("## 数据来源")
    lines.append("")
    lines.append("- 成分股基线：`data/index_constituents.json`（每年 6 月指数调整后手动更新）")
    lines.append("- 行情 PE/PB/价格：腾讯行情 `qt.gtimg.cn`")
    lines.append("- 财务 ROE：东方财富 datacenter `RPT_F10_FINANCE_MAINFINADATA`")
    lines.append("- 分红派息：东方财富 datacenter `RPT_SHAREBONUS_DET`")
    lines.append("- 观点层：`tools/fin_ai`（gangtise-reason，每天 80 次配额）")
    lines.append("")
    lines.append("---")
    lines.append("_本报告仅供学习研究，不构成投资建议。_")

    return "\n".join(lines)
```

- [ ] **Step 4: 跑测试，确认通过**

Run:
```bash
python -m pytest tests/fin_ai/test_stock_recommender.py -v
```

Expected: 22 个 case 全 PASS

- [ ] **Step 5: Commit**

```bash
git add tools/stock_recommender.py tests/fin_ai/test_stock_recommender.py
git commit -m "feat(stock-recommender): Markdown 报告生成（含 fin_ai 降级 warning）"
```

---

## Task 10: 串起来 + main() 集成 + 完整流程

**Files:**
- Modify: `tools/stock_recommender.py`（重写 `main()`，串起 5 步）

- [ ] **Step 1: 重写 `main()`，集成完整流水线**

把 Task 1 中的占位 `main()` 替换为：

```python
def main():
    parser = argparse.ArgumentParser(description="A 股股票推荐 CLI")
    sub = parser.add_subparsers(dest="mode", required=True)
    p_stable = sub.add_parser("stable", help="稳定收益模式")
    p_stable.add_argument("--top", type=int, default=5)
    p_stable.add_argument("--min-dividend", type=float, default=4.0)
    p_stable.add_argument("--max-pe", type=float, default=15.0)
    p_stable.add_argument("--min-roe", type=float, default=12.0)
    p_stable.add_argument("--max-roe-stddev", type=float, default=5.0)
    p_stable.add_argument("--dry-run", action="store_true")
    p_stable.add_argument("--force", action="store_true")
    args = parser.parse_args()

    today = datetime.now().strftime("%Y%m%d")
    date_iso = datetime.now().strftime("%Y-%m-%d")

    if args.mode == "stable":
        sys.exit(run_stable(
            today=today,
            date_iso=date_iso,
            top_n=args.top,
            min_dividend=args.min_dividend,
            max_pe=args.max_pe,
            min_roe=args.min_roe,
            max_roe_stddev=args.max_roe_stddev,
            dry_run=args.dry_run,
            force=args.force,
        ))


def run_stable(
    today: str, date_iso: str,
    top_n: int, min_dividend: float, max_pe: float,
    min_roe: float, max_roe_stddev: float,
    dry_run: bool, force: bool,
) -> int:
    """稳定收益模式主流程。返回退出码。"""
    print(f"[1/5] 加载成分股...", file=sys.stderr)
    try:
        codes = load_index_constituents()
    except Exception as e:
        print(f"❌ 成分股加载失败: {e}", file=sys.stderr)
        return 1
    print(f"     共 {len(codes)} 只待扫描", file=sys.stderr)

    print(f"[2/5] 拉基本面（顺序，约 5 分钟）...", file=sys.stderr)
    scored_items = []
    for i, code in enumerate(codes, 1):
        try:
            quote = fetch_quote(code)
            fins = fetch_financials(code, years=3)
            divs = fetch_dividends(code)
            price = float(quote.get("price", 0))
            pe_raw = quote.get("pe", "-")
            pe = float(pe_raw) if pe_raw not in ("-", "", None) else None
            div_per_10 = divs["dividend_per_10_ttm"]
            div_yield = calc_dividend_yield(div_per_10, price)
            roe_history = fins["roe_history"]
            fund = {
                "code": code,
                "name": quote.get("name", code),
                "price": price,
                "pe": pe,
                "dividend_yield": div_yield,
                "roe_history": roe_history,
            }
            result = score_stable(
                fund, min_dividend=min_dividend, max_pe=max_pe,
                min_roe=min_roe, max_roe_stddev=max_roe_stddev,
            )
            fund.update({
                "score": result["score"],
                "details": result["details"],
                "roe_mean": sum(roe_history) / len(roe_history) if roe_history else 0,
            })
            scored_items.append(fund)
            print(f"     [{i}/{len(codes)}] {code} {fund['name']}: {fund['score']}/4 分", file=sys.stderr)
        except Exception as e:
            print(f"     [{i}/{len(codes)}] {code} ⚠️ 跳过 ({e})", file=sys.stderr)
            continue

    print(f"[3/5] 排序过滤...", file=sys.stderr)
    strong, weak = sort_and_filter(scored_items, min_score=3, top_n=top_n)

    print(f"[4/5] fin_ai 观点层...", file=sys.stderr)
    candidates = strong + weak
    opinion = ask_fin_ai_opinion(candidates) if candidates else {
        "summary": "", "warnings": {}, "ok": True, "error": ""
    }
    if not opinion["ok"]:
        print(f"     ⚠️ {opinion['error']}", file=sys.stderr)

    print(f"[5/5] 生成报告...", file=sys.stderr)
    md = generate_report(
        today=date_iso,
        strong=strong,
        weak=weak,
        fin_ai_opinion=opinion,
        scanned_count=len(codes),
        thresholds={
            "min_dividend": min_dividend, "max_pe": max_pe,
            "min_roe": min_roe, "max_roe_stddev": max_roe_stddev,
        },
    )

    report_path = REPORTS_DIR / f"stable-{today}.md"
    if dry_run:
        print(md)
        print(f"\n[dry-run] 不写文件（path={report_path}）", file=sys.stderr)
    else:
        if report_path.exists() and not force:
            print(f"❌ 报告已存在：{report_path}（用 --force 覆盖）", file=sys.stderr)
            return 1
        REPORTS_DIR.mkdir(parents=True, exist_ok=True)
        report_path.write_text(md, encoding="utf-8")
        print(f"✅ 报告已生成：{report_path}", file=sys.stderr)
    return 0
```

- [ ] **Step 2: 跑全部 unit test 确认无破坏**

Run:
```bash
python -m pytest tests/fin_ai/test_stock_recommender.py -v
```

Expected: 22 个 case 全 PASS

- [ ] **Step 3: 手动跑 dry-run，确认能串起来**

Run:
```bash
python tools/stock_recommender.py stable --dry-run --top 3
```

Expected: stderr 显示 [1/5] → [5/5] 进度，stdout 打印 Markdown 报告。如果网络不通，应有降级 warning 但不报错。

> ⚠️ 这是端到端 smoke test，预计 5-10 分钟跑完。

- [ ] **Step 4: Commit**

```bash
git add tools/stock_recommender.py
git commit -m "feat(stock-recommender): main() 集成 5 步流水线 + dry-run/force 选项"
```

---

## Task 11: skill 文件 + CLAUDE.md 更新

**Files:**
- Create: `skills/stock-recommend.md`
- Modify: `CLAUDE.md`（Skills 全景表新增一行）
- Run: `python scripts/sync-codex-skills.py`（按项目约定同步给 Codex）

- [ ] **Step 1: 写 `skills/stock-recommend.md`**

文件 `skills/stock-recommend.md`：

```markdown
---
description: A 股稳定收益推荐（高股息+低PE+稳定ROE），扫描中证红利+上证50成分股
---

# /stock-recommend — A 股推荐系统

## 使用示例

```
/stock-recommend                    # 默认 stable 模式
/stock-recommend stable --top 5     # 显式指定 top 5
/stock-recommend stable --dry-run   # 仅打印不写文件
/stock-recommend long-term          # MVP 未实现，会提示
```

## 执行步骤

收到本 slash command 后，**直接调底层 CLI**，不要重新实现逻辑：

### 模式 1：stable（稳定收益）

```bash
python tools/stock_recommender.py stable --top 5
```

执行流程（约 5-10 分钟）：
1. 加载中证红利 + 上证 50 成分股（约 100 只）
2. 顺序拉基本面（每只 3 个 HTTP）
3. 4 维硬指标打分（股息率 TTM / PE / ROE 均值 / ROE 稳定性）
4. fin_ai 批量观点层（烧 1 次配额）
5. 输出 Markdown 报告到 `reports/股票推荐/stable-{YYYYMMDD}.md`

### 模式 2 / 3：long-term / short-term

未实现。提示用户：

> 该模式 MVP 未实现，仅 `stable` 可用。请改用 `/investment-research {公司名}`（长期看好）或 `/news-pulse {公司名}`（短期事件驱动）。

## 输出处理

- 报告生成后，向用户展示路径并简要总结 top 推荐
- 如果报告顶部出现 ⚠️ fin_ai 降级 warning，主动告知用户原因（配额/超时）
- 询问是否要推送到 GitHub

## 配额约束

- 单次跑：1 次 fin_ai 调用（缓存命中 0 配额）
- 每日 80 次配额，足够跑数十次

## 相关 skill

- `/quality-screen`：去劣筛选 7 条硬指标（适用于单公司）
- `/investment-checklist`：买入前 6 关 checklist
- `/investment-research {公司}`：长期看好模式
```

- [ ] **Step 2: 更新 CLAUDE.md Skills 全景表**

在 `CLAUDE.md` 的「## Skills 全景（18 个，按场景选用）」表格里，标题改为「19 个」，并在「📊 财报分析」或新加一行「📈 持仓管理」类别下追加：

```markdown
| 📈 持仓管理 | `/portfolio-review` `/thesis-tracker` `/news-pulse` `/stock-recommend` | 组合管理；论文追踪；股价异动 10 分钟归因；按偏好推荐 N 支候选股 |
```

同时在文件末尾「## 注意事项」上方追加新章节：

```markdown
## /stock-recommend 推荐系统

A 股稳定收益推荐：扫描中证红利 + 上证 50 成分股（约 100 只），按 4 维硬指标打分（股息率 TTM / PE / ROE 均值 / ROE 稳定性）+ fin_ai 观点层。

```bash
python tools/stock_recommender.py stable --top 5
```

- 单文件 CLI：`tools/stock_recommender.py`（约 300 行，纯 stdlib）
- 输出：`reports/股票推荐/stable-{YYYYMMDD}.md`
- 配额：单次跑烧 1 次 fin_ai（80/天足够）
- 设计 spec：`docs/superpowers/specs/2026-07-04-stock-recommender-design.md`
```

- [ ] **Step 3: 同步给 Codex**

Run:
```bash
python scripts/sync-codex-skills.py
```

Expected: 输出 "已同步 N 个 skill 到 codex-skills/"。检查 `codex-skills/stock-recommend/SKILL.md` 是否生成。

校验不写文件：
```bash
python scripts/sync-codex-skills.py --check
```

Expected: 退出码 0。

- [ ] **Step 4: Commit**

```bash
git add skills/stock-recommend.md codex-skills/ CLAUDE.md
git commit -m "feat(skill): /stock-recommend slash command + CLAUDE.md 工具表 + Codex 同步"
```

---

## Task 12: 端到端 smoke test + 验收清单

**Files:**
- Create: `tests/fin_ai/e2e_checklist_stock_recommender.md`（手动验收清单）

- [ ] **Step 1: 写 e2e 验收清单**

文件 `tests/fin_ai/e2e_checklist_stock_recommender.md`：

```markdown
# stock_recommender 端到端验收清单

每次重大变更后手动跑一遍。

## Unit test

- [ ] `python -m pytest tests/fin_ai/test_stock_recommender.py -v` 全绿（22 个 case）

## CLI 入口

- [ ] `python tools/stock_recommender.py --help` 显示帮助，退出码 0
- [ ] `python tools/stock_recommender.py stable --help` 显示子命令帮助
- [ ] `python tools/stock_recommender.py long-term` 提示「MVP 未实现」，退出码 ≠ 0

## 端到端 dry-run

- [ ] `python tools/stock_recommender.py stable --dry-run --top 3` 跑通，stdout 输出 Markdown
- [ ] stderr 显示 [1/5] → [5/5] 进度
- [ ] 跑通时间 < 10 分钟（100 只股 × 3 HTTP）

## 完整跑 + 报告生成

- [ ] `python tools/stock_recommender.py stable --top 5` 跑通，退出码 0
- [ ] `reports/股票推荐/stable-{YYYYMMDD}.md` 文件存在
- [ ] 报告含 6 个章节：总结 / Top 推荐 / 备选 / fin_ai 观点层 / 方法论 / 数据来源
- [ ] Top 推荐按股息率降序排列
- [ ] 招行（600036）出现在 top 推荐里（基本面达标）

## fin_ai 配额耗尽场景

- [ ] 改 `tools/fin_ai/quota.py` 临时把 `limit=0`，跑一次：报告顶部出现 ⚠️ warning
- [ ] 改回原值

## Skill 触发

- [ ] Claude Code 里输 `/stock-recommend stable`，触发 CLI，生成同样报告

## Codex 同步

- [ ] `python scripts/sync-codex-skills.py --check` 退出码 0
- [ ] `codex-skills/stock-recommend/SKILL.md` 存在且内容正确
```

- [ ] **Step 2: 跑完整端到端**

按清单执行：

```bash
# Unit test
python -m pytest tests/fin_ai/test_stock_recommender.py -v

# CLI 入口
python tools/stock_recommender.py --help
python tools/stock_recommender.py stable --help

# 端到端
python tools/stock_recommender.py stable --dry-run --top 3
python tools/stock_recommender.py stable --top 5

# Codex 同步校验
python scripts/sync-codex-skills.py --check
```

每项预期见清单。**如果端到端跑失败但 unit test 全绿**：先 commit 当前状态，标记 e2e 清单未通过项，作为后续修复任务。

- [ ] **Step 3: Commit 验收清单**

```bash
git add tests/fin_ai/e2e_checklist_stock_recommender.md
git commit -m "docs(stock-recommender): 端到端验收清单"
```

---

## Task 13: 更新 memory（fin-ai 项目状态 → stock-recommender 上线）

**Files:**
- Modify: `C:\Users\SMILE\.claude\projects\C--workspace-ai-berkshire\memory\project_next_pipeline.md`（划掉需求 1，标完成日期）
- Create: `C:\Users\SMILE\.claude\projects\C--workspace-ai-berkshire\memory\project_stock_recommender.md`（新 memory：稳定收益推荐已上线）

- [ ] **Step 1: 在 `project_next_pipeline.md` 末尾追加状态更新**

在文件末尾（"关联：[[fin-ai-project-status]] [[ai-berkshire-fork-remote]]" 行之前）插入：

```markdown
## 状态更新（2026-07-04）

需求 1（推荐股票）**已实施 stable MVP**：
- spec: docs/superpowers/specs/2026-07-04-stock-recommender-design.md
- plan: docs/superpowers/plans/2026-07-04-stock-recommender.md
- 工具: tools/stock_recommender.py + skills/stock-recommend.md
- 详细记忆: [[stock-recommender-status]]

需求 2（定时调度）和需求 3（热点驱动）尚未实施。
```

- [ ] **Step 2: 创建 `project_stock_recommender.md`**

文件 `C:\Users\SMILE\.claude\projects\C--workspace-ai-berkshire\memory\project_stock_recommender.md`：

```markdown
---
name: stock-recommender-status
description: 股票推荐系统（稳定收益 MVP）已上线：单文件 CLI + skill + fin_ai 观点层
metadata:
  type: project
---

# 股票推荐系统：稳定收益 MVP（已上线 2026-07-04）

A 股推荐系统第一步——**稳定收益模式**。

## 范围

- 模式：stable（高股息 + 低 PE + 稳定 ROE）
- 市场：A 股（沪深京）
- 池子：中证红利 + 上证 50 成分股（约 100 只，data/index_constituents.json）
- 输出：reports/股票推荐/stable-{YYYYMMDD}.md

## 4 维评分（4 分制）

| 维度 | 阈值 |
|------|------|
| 股息率（TTM）| > 4% |
| PE（动）| < 15 |
| ROE 近 3 年均值 | > 12% |
| ROE 近 3 年 stddev | < 5pp |

- 4 分 = 强烈推荐 | 3 分 = 备选 | < 3 分 = 剔除
- 同分按股息率降序

## Why（设计动机）

工具层（18 skill + fin_ai + financial_rigor）齐备，缺一个按偏好筛选的工具。stable 模式 MVP 最快（数据源现成、不依赖 fin_ai 配额），先跑通整条链路。

## How to apply

下次会话用户提到「推荐股票 / 选股 / 高股息 / 稳定收益」时：
- 默认调 `/stock-recommend stable`
- 不要重新设计：spec 在 docs/superpowers/specs/2026-07-04-stock-recommender-design.md
- 后续模式（long-term / short-term）按"复制粘贴改阈值"原则，不抽象公共框架

## 已知限制

- 仅 A 股（港股/美股未实现）
- 仅 stable 模式（long-term / short-term 未实现）
- 不含定时调度（需求 2 未做）
- 成分股基线需每年 6 月指数调整后手动更新

关联：[[next-pipeline-opportunities]] [[fin-ai-project-status]]
```

- [ ] **Step 3: 更新 `MEMORY.md` 索引**

在 `C:\Users\SMILE\.claude\projects\C--workspace-ai-berkshire\memory\MEMORY.md` 末尾追加一行：

```markdown
- [stock-recommender 已上线（stable MVP）](project_stock_recommender.md) — A 股稳定收益推荐：4 维硬指标 + fin_ai 观点层，输出 reports/股票推荐/
```

- [ ] **Step 4: Commit 计划完成标记**

```bash
git add docs/superpowers/plans/2026-07-04-stock-recommender.md
git commit --allow-empty -m "chore(plan): 股票推荐系统实施计划完成（13 个任务）"
```

> Memory 文件不在仓库内，无需 commit。

---

## 全部任务总览

| # | 任务 | 主要产出 | 测试 |
|---|------|----------|------|
| 1 | 项目骨架 | tools/stock_recommender.py + data/index_constituents.json + 测试目录 | 1 占位 |
| 2 | 加载成分股 | `load_index_constituents()` | 1 case |
| 3 | 腾讯行情 | `_http_get / _qq_code / _parse_qq_quote / fetch_quote` | 4 case |
| 4 | 东财财务 | `extract_roe_history / fetch_financials` | 2 case |
| 5 | 东财分红 | `extract_dividends_ttm / calc_dividend_yield / fetch_dividends` | 4 case |
| 6 | 4 维打分 | `score_stable` | 7 case（spec §5 全覆盖） |
| 7 | 排序过滤 | `sort_and_filter` | 2 case |
| 8 | fin_ai 观点层 | `ask_fin_ai_opinion` | 手动验证 |
| 9 | 报告生成 | `generate_report` | 2 case |
| 10 | main 集成 | `main + run_stable` | 集成 |
| 11 | skill 文件 | skills/stock-recommend.md + CLAUDE.md | 手动验证 |
| 12 | e2e 验收 | 清单 + 全流程跑通 | 手动 |
| 13 | memory 更新 | project_stock_recommender.md | 无 |

**总计**：22 个 unit case + 端到端 smoke test + skill 集成验证。

---

## 未在 MVP 实现的 spec 条款（推迟）

| Spec 条款 | 推迟原因 | 后续触发 |
|-----------|----------|----------|
| §9 第 3 条「基本面缓存 1 天」（`data/fundamentals_stable_{date}.json`） | 顺序拉 100 只股 ~5 分钟可接受，缓存不是核心瓶颈；YAGNI | 单日多次重跑时再加 |
| §9 第 6 条「不抽象多模式框架」 | 已遵守（plan 内不出现 long-term / short-term） | 长期/短期模式上线时复制粘贴 |

> 上述推迟不影响 spec 验收标准。如果用户单日多次重跑感觉慢，可在 Task 10 后追加缓存 task。

---

## 执行顺序建议

按 Task 1 → 13 顺序执行。每个 Task 完成后 commit。

**关键依赖链**：
- Task 2 → 3 → 4 → 5（数据获取层，独立任务）
- Task 6 → 7（评分 + 排序，核心业务逻辑）
- Task 8（fin_ai，独立，可最后做）
- Task 9 → 10（报告生成 + 集成，依赖前 8 个 Task）
- Task 11 → 12 → 13（skill / 验收 / memory，收尾）

**中断恢复**：每个 Task 都是独立 commit，中断后 `git log` 看到已完成到哪个 Task，下一个继续即可。
