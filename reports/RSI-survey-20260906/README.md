# RSI 中英文综述工作稿

文献截止：**2026-09-06**。这里的 RSI 指 Recursive Self-Improvement（递归自我改进）。

已完成一篇约 6,500 英文词的批判性叙述综述，以及约 11,300 汉字的对应中文版。两版使用相同的 53 条参考文献、同一组关键事实和相同的核心公式。中文末尾另附术语对照。未添加未经确认的作者、单位或邮箱，未提交到 arXiv。

## 阅读与修改

- 英文 PDF：`../../output/pdf/rsi-survey-en-20260906.pdf`
- 中文 PDF：`../../output/pdf/rsi-survey-zh-20260906.pdf`
- 英文编辑稿：`manuscript-en.md`
- 中文编辑稿：`manuscript-zh.md`
- 英文 LaTeX 主文件：`arxiv/main.tex`
- 中文 LaTeX 主文件：`arxiv/main-zh.tex`
- 参考文献：`arxiv/references.bib`
- 英文 arXiv 源码压缩包：`rsi-survey-arxiv-source.zip`
- 逐条证据与数值限定：`research/evidence-ledger.md`
- 来源登记：`research/source_register.md`
- 检索方式记录：`research/search-log.md`
- 检查结果：`research/validation-report.md`

## 论文定位

英文题目：**Recursive Self-Improvement in AI: A Critical Survey of Mechanisms, Evidence, and Evaluation**

中文题目：**人工智能递归自我改进：机制、证据与评估的批判性综述**

论文主线是：区分改好一个答案、持久改变一个系统，以及改善下一轮改进的方法。对于自修改编程智能体、模型自编辑、自训练和自动化科研，分别考察修改对象、反馈、继承关系和实验边界。

已有综述已覆盖“什么进化、何时进化、如何进化”和改进机制可修改等主题；HGM 也已提出当前表现与后代产出能力的区别。本文明确引用这些工作，不声称首次提出 RSI 分类、可修改改进机制或 metaproductivity。较集中的写作切口是把这些问题与 2026 年出现的新评估基准、匹配改进者对照和资源核算联系起来。

提出的算子产出度量和评估协议属于综合性方法建议，尚未开展实验验证。稿件属于叙述综述，不是穷尽式系统综述，不报告虚构的筛选总数、统计元分析或复现实验。

## 值得保留的关键限定

1. 当前所选文献支持多种有边界的自我改进，不能据此宣称已实现通用、持续、成本校正后的递归加速。
2. 权重变化既不是 RSI 的必要条件，也不是充分条件；需要说明复合系统的边界。
3. “零数据”描述特定后训练输入条件，并不抹去预训练、环境和人类设计的监督结构。
4. DGM 的 20%→50% 是论文特定 SWE-bench 子集的结果，不能改写为完整官方成绩。
5. 自我改进的历史最佳曲线按定义不会下降；需要检查当前系统、合法验证选优结果和事后审计最优值。
6. 2026 年的新预印本按照作者报告处理；核对书目信息不等于独立复现。

## 编译

在本目录执行：

```bash
python3 research/build_bibliography.py
python3 build.py
```

需要 Pandoc、pdfLaTeX、XeLaTeX、BibTeX。英文稿使用标准 TeX 字体；中文稿的 `arxiv/preamble-zh.tex` 当前使用本机 macOS 宋体路径，换电脑时可改为已安装的中文字体。英文 arXiv 包不依赖这些中文字体，也不包含中文稿或其字体路径。

只编译英文提交包时，在 `arxiv/` 中执行：

```bash
pdflatex main.tex
bibtex main
pdflatex main.tex
pdflatex main.tex
```

压缩包只有 `main.tex`、`main.bbl`、`references.bib` 和 `figure-loop.tex`，不包含参考论文缓存或临时编译文件。正文中的书目键通过 Pandoc 转换为正式引用。

## 提交 arXiv 前的定稿步骤

1. 补充真实英文署名、单位、邮箱；明确每位作者同意署名，并审阅全文。当前没有代填任何个人身份。
2. 人工复核证据台账中与论点最相关的原文段落，尤其是新预印本的评估设置和局限；结合个人判断重写核心论证。若希望获得更强原创贡献，可实施第 6 节的匹配算子实验，再把结果加入稿件；综述稿本身没有把该实验写成已完成。
3. 编辑 Markdown 后运行 `build.py`；若直接编辑 `arxiv/main.tex`，不要再运行会覆盖它的生成步骤。作者修改与文字修改应保存在同一源文件流程中。
4. 使用英文源码包创建投稿，选择与内容匹配的类别（可先考虑 cs.AI，是否交叉到 cs.LG/cs.CL 取决于最终稿重点），填写标题和摘要，按账户状态完成必要步骤，再检查平台重新编译的 PDF。
5. 工作稿带有真实的 AI 辅助说明。最终作者需要根据实际工作流程确认其表述，并对文稿内容负责。

arXiv 官方要求提交与主文对应的源文件和所需参考文献文件，并要求投稿者检查重新编译的 PDF，详见[TeX 投稿说明](https://info.arxiv.org/help/submit_tex.html)和[投稿总览](https://info.arxiv.org/help/submit/index.html)。如果还计划将中文版一并提交，应先查看[译本说明](https://info.arxiv.org/help/translations.html)，按同一作品的译本处理。本交付没有为两种语言创建重复投稿，也不保证平台收录或学术同行评审结果。
