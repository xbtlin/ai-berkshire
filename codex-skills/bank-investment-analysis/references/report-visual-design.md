# 银行投研报告可视化规范

## 目标

让图表服务于判断，不做装饰。保持单一Markdown交付，以统一主题、语义颜色、结论式标题和标准图注形成协调的投研BI视觉。

## 统一主题

所有Mermaid占比图使用可自定义的 `base` 主题，不使用可能呈现为黑白的默认或 `neutral` 主题。结构图使用以下颜色顺序：

| 用途 | 色值 | 含义 |
|---|---|---|
| 核心/基准 | `#0B3B60` | 深蓝，主业务或基准项 |
| 第二主项 | `#168AAD` | 青蓝，第二大业务 |
| 改善/低风险 | `#2A9D8F` | 青绿，改善或低风险项 |
| 结构压力 | `#E9A23B` | 金色，期限或结构压力 |
| 其他 | `#7C6FB2` | 紫色，剩余项 |
| 高风险 | `#C44536` | 红色，只用于明显风险集中 |

风险图不要机械沿用结构图顺序：正常/低风险用深蓝或青绿，承压项用金色或橙色，最主要风险项用红色。不要使用彩虹色、纯黑切片或相邻低对比度颜色。

## Mermaid主题块

每张图在代码块内加入以下frontmatter，并按业务语义调整 `pie1`—`pie5`；色值只用十六进制：

```text
---
config:
  theme: base
  themeVariables:
    background: '#F7FAFC'
    fontFamily: 'Inter, PingFang SC, Microsoft YaHei, sans-serif'
    textColor: '#334E68'
    pie1: '#0B3B60'
    pie2: '#168AAD'
    pie3: '#2A9D8F'
    pie4: '#E9A23B'
    pie5: '#7C6FB2'
    pieStrokeColor: '#FFFFFF'
    pieStrokeWidth: '3px'
    pieOuterStrokeColor: '#D8E1EA'
    pieOuterStrokeWidth: '1px'
    pieOpacity: 0.96
    pieTitleTextColor: '#102A43'
    pieTitleTextSize: '20px'
    pieLegendTextColor: '#334E68'
    pieLegendTextSize: '14px'
    pieSectionTextColor: '#FFFFFF'
    pieSectionTextSize: '14px'
---
```

## 版式规则

1. 全文控制在3—5张关键图；同类图使用相同尺寸、字体和边框。
2. 图放在对应数据表之后、分析文字之前；不连续堆放两张无解释的图。
3. 标题直接写结论，不只写“资产结构图”；标题尽量不超过28个汉字。
4. 图例顺序与正文表格一致；结构图优先按余额或占比从高到低排列，语义配色优先级更高。
5. 图下注明期间、集团/母行、期末/日均、分母、单位、来源和核对结果。
6. 占比数据机械核对至100%；舍入差额超过0.1个百分点时说明原因。
7. 交付前在目标Markdown渲染器中检查颜色、中文字体、标题、图例和标签；若颜色未生效，不得以黑白默认图交付。
