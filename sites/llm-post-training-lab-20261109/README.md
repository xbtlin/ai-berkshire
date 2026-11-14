# 后训练学习实验室

面向已有深度学习基础的中文 LLM 后训练学习网站，资料核验截止 2026-11-09。

[在线学习网站](https://llm-post-training-lab-nov09.xbtlin.chatgpt.site)（访问权限由 Sites 控制）。

- 八周模块：SFT、数据与 LoRA、奖励模型、DPO、PPO、GRPO/RLVR、评估、综合项目。
- 24 项一手资源，带阅读建议、标签筛选和收藏。
- 四项浏览器数学实验，均不训练模型。
- 每课验收清单、自测和本地笔记；localStorage 仅保存在当前浏览器，可导出 JSON。
- 下载资源：完整 Markdown 导读、CSV 实验记录模板、无第三方依赖的 Python 数学练习。

## 开发

需要 Node >=22.13；使用项目 Sites 配置和 Vinext 构建。

```sh
cd sites/llm-post-training-lab-20261109
npm ci
npm run dev
node node_modules/typescript/bin/tsc --noEmit
node scripts/export-guide.mjs
python3 public/loss-exercises.py
npm run build
```

`content/curriculum.ts` 是课程与来源数据。修改后运行 export-guide 同步下载版。组件位于 `app/page.tsx` 与 `app/lab.tsx`。CSS 含桌面和移动断点；字体使用系统字体回退。

## 验证边界

已检查 DPO margin=0、GRPO 全同奖励、PPO 正负优势裁剪与 SFT mask；未运行真实模型训练。教学公式的计算约定和实际训练库的版本差异已在页面注明。

资料只做原文链接和原创导读，不托管第三方教材全文。课程时间为规划估计，真实训练算力另计。
