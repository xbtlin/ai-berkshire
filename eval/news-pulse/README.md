# news-pulse 异动归因评测集

接入 issue：[xbtlin/ai-berkshire#112](https://github.com/xbtlin/ai-berkshire/issues/112)
网关：decision-gateway（Kev 0.8B 常驻 8009 端口，`DG_BACKEND=kev`）

## 问法（v1 草案，与 issue #112 §1 逐字一致）

- key: `cause`，type: `choice`
- instructions: `这只股票的异动主因属于哪一类？`
- criteria: `company_event`（公司自身事件）/ `industry_policy`（行业格局/竞争对手/监管政策）/ `market_sentiment`（市场情绪/板块轮动/大盘带动）/ `technical_capital`（技术面/资金面，无基本面新闻可解释）

**问法同源纪律**：评测集、线上请求的 instructions/criteria 必须逐字一致；改任何一个字，全部历史报告作废重跑。

## 标注口径

- `state` = 异动描述（日期+幅度）+ 当期关键新闻摘要，写法对齐 news-pulse 实跑时喂给模型的情报摘要；
- 标签取**当期市场公认主因**，不以事后深度研究结论改标；
- 边界争议例（如「公司财报恰逢大盘暴跌」）主因归主导驱动因素，并在行内 `state` 写明背景；拿不准的宁可不进集。

## 现状与扩充路径

- `seed.jsonl`：13 条种子，agent 依据公开历史事件草标（2020–2025，四类覆盖），**未经业务复核**；
- 缺口到 ≥100 条的来源：① 每次 news-pulse 实跑后把当次归因结论回填一行（问法逐字一致）；② 持仓/关注池历史异动逐条补标；
- 复核入口：按 issue #112 §4 验收断言跑 `eval/run_eval.py` + `calibrate/temperature.py`。

## 运行

```bash
cd ~/Documents/Codex/decision-gateway
DG_BACKEND=kev python3 eval/run_eval.py \
  --dataset ~/ai-berkshire/eval/news-pulse/seed.jsonl \
  --report eval/reports/news-pulse-kev-0.8b-seed.json
python3 calibrate/temperature.py eval/reports/news-pulse-kev-0.8b-seed.json
```
