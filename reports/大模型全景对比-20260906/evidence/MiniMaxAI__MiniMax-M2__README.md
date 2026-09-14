---
pipeline_tag: text-generation
license: other
license_name: modified-mit
license_link: https://github.com/MiniMax-AI/MiniMax-M2/blob/main/LICENSE
library_name: transformers
---

<div align="center">

<svg width="60%" height="auto" viewBox="0 0 144 48" fill="none" xmlns="http://www.w3.org/2000/svg">
<path d="M26.6782 7.96523C26.6782 7.02436 25.913 6.26087 24.9739 6.26087C24.0348 6.26087 23.2695 7.0261 23.2695 7.96523V36.2139C23.2695 38.4 21.4904 40.1791 19.3043 40.1791C17.1183 40.1791 15.3391 38.4 15.3391 36.2139V18.0904C15.3391 17.1496 14.5739 16.3861 13.6348 16.3861C12.6956 16.3861 11.9304 17.1513 11.9304 18.0904V25.7722C11.9304 27.9583 10.1513 29.7374 7.96518 29.7374C5.7791 29.7374 4 27.9583 4 25.7722V22.9878C4 22.3635 4.50609 21.8574 5.13043 21.8574C5.75478 21.8574 6.26087 22.3635 6.26087 22.9878V25.7722C6.26087 26.713 7.02605 27.4765 7.96518 27.4765C8.90431 27.4765 9.66954 26.7113 9.66954 25.7722V18.0904C9.66954 15.9044 11.4487 14.1252 13.6348 14.1252C15.8209 14.1252 17.6 15.9044 17.6 18.0904V36.2139C17.6 37.1548 18.3652 37.9183 19.3043 37.9183C20.2435 37.9183 21.0087 37.153 21.0087 36.2139V25.1322V7.96523C21.0087 5.77914 22.7878 4 24.9739 4C27.16 4 28.9391 5.77914 28.9391 7.96523V31.3565C28.9391 31.9809 28.433 32.487 27.8087 32.487C27.1843 32.487 26.6782 31.9809 26.6782 31.3565V7.96523ZM47.6539 14.1252C45.4678 14.1252 43.6887 15.9044 43.6887 18.0904V33.2296C43.6887 34.1704 42.9235 34.9339 41.9843 34.9339C41.0452 34.9339 40.28 34.1687 40.28 33.2296V7.96523C40.28 5.77914 38.5008 4 36.3148 4C34.1287 4 32.3496 5.77914 32.3496 7.96523V40.0348C32.3496 40.9756 31.5843 41.7391 30.6452 41.7391C29.7061 41.7391 28.9409 40.9739 28.9409 40.0348V36.0643C28.9409 35.44 28.4348 34.9339 27.8104 34.9339C27.1861 34.9339 26.68 35.44 26.68 36.0643V40.0348C26.68 42.2209 28.4591 44 30.6452 44C32.8313 44 34.6104 42.2209 34.6104 40.0348V7.96523C34.6104 7.02436 35.3756 6.26087 36.3148 6.26087C37.2539 6.26087 38.0191 7.0261 38.0191 7.96523V33.2296C38.0191 35.4156 39.7982 37.1948 41.9843 37.1948C44.1704 37.1948 45.9496 35.4156 45.9496 33.2296V18.0904C45.9496 17.1496 46.7148 16.3861 47.6539 16.3861C48.593 16.3861 49.3582 17.1513 49.3582 18.0904V31.3565C49.3582 31.9809 49.8643 32.487 50.4887 32.487C51.113 32.487 51.6191 31.9809 51.6191 31.3565V18.0904C51.6191 15.9044 49.84 14.1252 47.6539 14.1252Z" fill="url(#paint0_linear_17_483)"/>
<path d="M68.7671 16.5615H71.2541C71.3254 16.5615 71.3845 16.5859 71.435 16.6363C71.4836 16.6868 71.5097 16.7459 71.5097 16.8172V31.1824C71.5097 31.2537 71.4854 31.3128 71.435 31.3633C71.3845 31.4137 71.3254 31.4381 71.2541 31.4381H68.7671C68.6958 31.4381 68.6367 31.4137 68.5862 31.3633C68.5358 31.3146 68.5115 31.2537 68.5115 31.1824V21.812C68.5115 21.7563 68.4976 21.7268 68.4697 21.7268C68.4419 21.7268 68.4123 21.7476 68.3845 21.7911L66.1323 25.318C66.061 25.4311 65.9619 25.4885 65.8349 25.4885H64.581C64.4541 25.4885 64.3549 25.4328 64.2836 25.318L62.0315 21.7911C62.0036 21.7494 61.9741 21.7302 61.9462 21.7372C61.9184 21.7441 61.9045 21.7772 61.9045 21.8328V31.1824C61.9045 31.2537 61.8802 31.3128 61.8297 31.3633C61.7793 31.4137 61.7202 31.4381 61.6489 31.4381H59.1619C59.0906 31.4381 59.0315 31.4137 58.981 31.3633C58.9306 31.3146 58.9062 31.2537 58.9062 31.1824V16.8172C58.9062 16.7459 58.9306 16.6868 58.981 16.6363C59.0315 16.5859 59.0906 16.5615 59.1619 16.5615H61.6489C61.7758 16.5615 61.8749 16.6189 61.9462 16.732L65.1341 21.6833C65.1758 21.7685 65.2193 21.7685 65.261 21.6833L68.4697 16.732C68.541 16.6189 68.6402 16.5615 68.7671 16.5615Z" fill="currentColor"/>
<path d="M74.1764 31.3633C74.1259 31.3146 74.1016 31.2537 74.1016 31.1824V16.8172C74.1016 16.7459 74.1259 16.6868 74.1764 16.6363C74.2268 16.5859 74.2859 16.5615 74.3572 16.5615H76.8442C76.9155 16.5615 76.9746 16.5859 77.0251 16.6363C77.0737 16.6868 77.0998 16.7459 77.0998 16.8172V31.1824C77.0998 31.2537 77.0755 31.3128 77.0251 31.3633C76.9746 31.4137 76.9155 31.4381 76.8442 31.4381H74.3572C74.2859 31.4381 74.2268 31.4137 74.1764 31.3633Z" fill="currentColor"/>
<path d="M88.3066 16.6361C88.3553 16.5874 88.4162 16.5613 88.4875 16.5613H90.9744C91.0457 16.5613 91.1049 16.5857 91.1553 16.6361C91.204 16.6865 91.2301 16.7457 91.2301 16.817V31.1822C91.2301 31.2535 91.2057 31.3126 91.1553 31.363C91.1049 31.4135 91.0457 31.4378 90.9744 31.4378H88.5727C88.4301 31.4378 88.331 31.3822 88.2753 31.2674L82.771 22.1717C82.7431 22.13 82.7136 22.1109 82.6858 22.1178C82.6579 22.1248 82.644 22.1578 82.644 22.2135L82.6858 31.1805C82.6858 31.2518 82.6614 31.3109 82.611 31.3613C82.5606 31.4117 82.5014 31.4361 82.4301 31.4361H79.9431C79.8718 31.4361 79.8127 31.4117 79.7623 31.3613C79.7118 31.3126 79.6875 31.2518 79.6875 31.1805V16.8152C79.6875 16.7439 79.7118 16.6848 79.7623 16.6344C79.8127 16.5839 79.8718 16.5596 79.9431 16.5596H82.3449C82.4858 16.5596 82.5849 16.617 82.6423 16.73L88.124 25.7822C88.1518 25.8239 88.1797 25.8431 88.2092 25.8361C88.2371 25.8292 88.251 25.7978 88.251 25.7404L88.2301 16.8152C88.2301 16.7439 88.2545 16.6848 88.3049 16.6344L88.3066 16.6361Z" fill="currentColor"/>
<path d="M93.8951 31.3633C93.8446 31.3146 93.8203 31.2537 93.8203 31.1824V16.8172C93.8203 16.7459 93.8446 16.6868 93.8951 16.6363C93.9455 16.5859 94.0047 16.5615 94.076 16.5615H96.5629C96.6342 16.5615 96.6934 16.5859 96.7438 16.6363C96.7925 16.6868 96.8186 16.7459 96.8186 16.8172V31.1824C96.8186 31.2537 96.7942 31.3128 96.7438 31.3633C96.6934 31.4137 96.6342 31.4381 96.5629 31.4381H94.076C94.0047 31.4381 93.9455 31.4137 93.8951 31.3633Z" fill="currentColor"/>
<path d="M109.267 16.5615H111.754C111.825 16.5615 111.885 16.5859 111.935 16.6363C111.984 16.6868 112.01 16.7459 112.01 16.8172V31.1824C112.01 31.2537 111.985 31.3128 111.935 31.3633C111.885 31.4137 111.825 31.4381 111.754 31.4381H109.267C109.196 31.4381 109.137 31.4137 109.086 31.3633C109.036 31.3146 109.011 31.2537 109.011 31.1824V21.812C109.011 21.7563 108.998 21.7268 108.97 21.7268C108.942 21.7268 108.912 21.7476 108.885 21.7911L106.632 25.318C106.561 25.4311 106.462 25.4885 106.335 25.4885H105.081C104.954 25.4885 104.855 25.4328 104.784 25.318L102.531 21.7911C102.504 21.7494 102.474 21.7302 102.446 21.7372C102.418 21.7441 102.405 21.7772 102.405 21.8328V31.1824C102.405 31.2537 102.38 31.3128 102.33 31.3633C102.279 31.4137 102.22 31.4381 102.149 31.4381H99.6619C99.5906 31.4381 99.5315 31.4137 99.481 31.3633C99.4306 31.3146 99.4062 31.2537 99.4062 31.1824V16.8172C99.4062 16.7459 99.4306 16.6868 99.481 16.6363C99.5315 16.5859 99.5906 16.5615 99.6619 16.5615H102.149C102.276 16.5615 102.375 16.6189 102.446 16.732L105.634 21.6833C105.676 21.7685 105.719 21.7685 105.761 21.6833L108.97 16.732C109.041 16.6189 109.14 16.5615 109.267 16.5615Z" fill="currentColor"/>
<path d="M123.782 31.2241L123.144 29.1424C123.116 29.0867 123.079 29.0572 123.038 29.0572H117.81C117.768 29.0572 117.732 29.085 117.704 29.1424L117.088 31.2241C117.046 31.3668 116.954 31.4363 116.812 31.4363H114.112C114.027 31.4363 113.963 31.412 113.921 31.3615C113.879 31.3128 113.871 31.2381 113.9 31.1389L118.49 16.7737C118.532 16.6328 118.624 16.5615 118.766 16.5615H122.102C122.243 16.5615 122.335 16.6328 122.379 16.7737L126.968 31.1389C126.982 31.1668 126.989 31.2033 126.989 31.245C126.989 31.372 126.911 31.4363 126.756 31.4363H124.057C123.916 31.4363 123.824 31.365 123.78 31.2241H123.782ZM118.554 26.7407H122.295C122.38 26.7407 122.408 26.6989 122.38 26.6137L120.467 20.3024C120.453 20.2467 120.432 20.2207 120.403 20.2276C120.375 20.2346 120.352 20.2589 120.339 20.3024L118.469 26.6137C118.455 26.6989 118.483 26.7407 118.554 26.7407Z" fill="currentColor"/>
<path d="M128.222 31.353C128.18 31.2974 128.187 31.2261 128.243 31.1409L132.365 24.0643C132.393 24.0226 132.393 23.9791 132.365 23.9374L128.243 16.8609L128.201 16.7339C128.201 16.6209 128.28 16.5635 128.434 16.5635H131.133C131.274 16.5635 131.38 16.6209 131.452 16.7339L134.213 21.6C134.255 21.6852 134.299 21.6852 134.34 21.6L137.102 16.7339C137.173 16.6209 137.28 16.5635 137.42 16.5635H140.099C140.198 16.5635 140.269 16.5913 140.311 16.6487C140.353 16.7061 140.346 16.7756 140.29 16.8609L136.168 23.9374C136.154 23.9791 136.154 24.0226 136.168 24.0643L140.29 31.1409L140.332 31.2678C140.332 31.3809 140.253 31.4383 140.099 31.4383H137.42C137.278 31.4383 137.172 31.3826 137.102 31.2678L134.34 26.4226C134.299 26.3374 134.255 26.3374 134.213 26.4226L131.429 31.2678C131.358 31.3809 131.252 31.4383 131.111 31.4383H128.433C128.333 31.4383 128.262 31.4104 128.22 31.353H128.222Z" fill="currentColor"/>
<defs>
<linearGradient id="paint0_linear_17_483" x1="3.99826" y1="24" x2="51.6208" y2="24" gradientUnits="userSpaceOnUse">
<stop stop-color="#E21680"/>
<stop offset="1" stop-color="#FF633A"/>
</linearGradient>
</defs>
</svg>

</div>
<hr>

<div align="center" style="line-height: 1.4; font-size:16px; margin-top: 30px;">
  Join Our 
  <a href="https://github.com/MiniMax-AI/MiniMax-AI.github.io/blob/main/images/wechat-qrcode.jpeg" target="_blank" style="font-size:17px; margin: 2px;">
    💬 WeChat
  </a> | 
  <a href="https://discord.com/invite/hvvt8hAye6" target="_blank" style="font-size:17px; margin: 2px;">
    🧩 Discord
  </a> 
  community.
</div>
<div align="center" style="line-height: 1.2; font-size:16px;">
  <a href="https://agent.minimax.io/" target="_blank" style="display: inline-block; margin: 4px;">
    MiniMax Agent
  </a> | 
  <a href="https://platform.minimax.io/docs/guides/text-generation" target="_blank" style="display: inline-block; margin: 4px;">
    ⚡️ API (Now Free for a limited time!)
  </a> | 
  <a href="https://github.com/MiniMax-AI/MiniMax-MCP" style="display: inline-block; margin: 4px;">
    MCP
  </a> |
  <a href="https://www.minimax.io" target="_blank" style="display: inline-block; margin: 4px;">
    MiniMax Website
  </a> 
</div>
<div align="center" style="line-height: 1.2; font-size:16px; margin-bottom: 30px;">
  <a href="https://huggingface.co/MiniMaxAI" target="_blank" style="margin: 2px;">
    🤗 Hugging Face 
  </a> | 
  <a href="https://github.com/MiniMax-AI/MiniMax-M2" target="_blank" style="margin: 2px;">
    🐙 GitHub
  </a> | 
  <a href="https://www.modelscope.cn/organization/MiniMax" target="_blank" style="margin: 2px;">
    🤖️ ModelScope
  </a> | 
  <a href="https://github.com/MiniMax-AI/MiniMax-M2/blob/main/LICENSE" style="margin: 2px;">
    📄 License: MIT
  </a>
</div>

# Meet MiniMax-M2

Today, we release and open source MiniMax-M2, a **Mini** model built for **Max** coding & agentic workflows.

**MiniMax-M2** redefines efficiency for agents. It's a compact, fast, and cost-effective MoE model (230 billion total parameters with 10 billion active parameters) built for elite performance in coding and agentic tasks, all while maintaining powerful general intelligence. With just 10 billion activated parameters, MiniMax-M2 provides the sophisticated, end-to-end tool use performance expected from today's leading models, but in a streamlined form factor that makes deployment and scaling easier than ever.

<p align="center">
  <img width="100%" src="figures/Bench.png">
</p>

---

## Highlights

**Superior Intelligence**. According to benchmarks from Artificial Analysis, MiniMax-M2 demonstrates highly competitive general intelligence across mathematics, science, instruction following, coding, and agentic tool use. **Its composite score ranks #1 among open-source models globally**.

**Advanced Coding**. Engineered for end-to-end developer workflows, MiniMax-M2 excels at multi-file edits, coding-run-fix loops, and test-validated repairs. Strong performance on Terminal-Bench and (Multi-)SWE-Bench–style tasks demonstrates practical effectiveness in terminals, IDEs, and CI across languages.

**Agent Performance**. MiniMax-M2 plans and executes complex, long-horizon toolchains across shell, browser, retrieval, and code runners. In BrowseComp-style evaluations, it consistently locates hard-to-surface sources, maintains evidence traceable, and gracefully recovers from flaky steps.

**Efficient Design**. With 10 billion activated parameters (230 billion in total), MiniMax-M2 delivers lower latency, lower cost, and higher throughput for interactive agents and batched sampling—perfectly aligned with the shift toward highly deployable models that still shine on coding and agentic tasks.

---

## Coding & Agentic Benchmarks

These comprehensive evaluations test real-world end-to-end coding and agentic tool use: editing real repos, executing commands, browsing the web, and delivering functional solutions. Performance on this suite correlates with day-to-day developer experience in terminals, IDEs, and CI.

| **Benchmark** | **MiniMax-M2** | **Claude Sonnet 4** | **Claude Sonnet 4.5** | **Gemini 2.5 Pro** | **GPT-5 (thinking)** | **GLM-4.6** | **Kimi K2 0905** | **DeepSeek-V3.2** |
|-----------|------------|-----------------|-------------------|-----------------|------------------|---------|---------------|----------------|
| **SWE-bench Verified** | 69.4 | 72.7 * | 77.2 * | 63.8 * | 74.9 * | 68 * | 69.2 * | 67.8 * |
| **Multi-SWE-Bench** | 36.2 | 35.7 * | 44.3 | / | / | 30 | 33.5 | 30.6 |
| **SWE-bench Multilingual** | 56.5 | 56.9 * | 68 | / | / | 53.8 | 55.9 * | 57.9 * |
| **Terminal-Bench** | 46.3 | 36.4 * | 50 * | 25.3 * | 43.8 * | 40.5 * | 44.5 * | 37.7 * |
| **ArtifactsBench** | 66.8 | 57.3* | 61.5 | 57.7* | 73* | 59.8 | 54.2 | 55.8 |
| **BrowseComp** | 44 | 12.2 | 19.6 | 9.9 | 54.9* | 45.1* | 14.1 | 40.1* |
| **BrowseComp-zh** | 48.5 | 29.1 | 40.8 | 32.2 | 65 | 49.5 | 28.8 | 47.9* |
| **GAIA (text only)** | 75.7 | 68.3 | 71.2 | 60.2 | 76.4 | 71.9 | 60.2 | 63.5 |
| **xbench-DeepSearch** | 72 | 64.6 | 66 | 56 | 77.8 | 70 | 61 | 71 |
| **HLE (w/ tools)** | 31.8 | 20.3 | 24.5 | 28.4 * | 35.2 * | 30.4 * | 26.9 * | 27.2 * |
| **τ²-Bench** | 77.2 | 65.5* | 84.7* | 59.2 | 80.1* | 75.9* | 70.3 | 66.7 |
| **FinSearchComp-global** | 65.5 | 42 | 60.8 | 42.6* | 63.9* | 29.2 | 29.5* | 26.2 |
| **AgentCompany** | 36 | 37 | 41 | 39.3* | / | 35 | 30 | 34 |

>Notes: Data points marked with an asterisk (*) are taken directly from the model's official tech report or blog. All other metrics were obtained using the evaluation methods described below.
>- SWE-bench Verified:  We use the same scaffold as [R2E-Gym](https://arxiv.org/pdf/2504.07164) (Jain et al. 2025) on top of OpenHands to test with agents on SWE tasks. All scores are validated on our internal infrastructure with 128k context length, 100 max steps, and no test-time scaling. All git-related content is removed to ensure agent sees only the code at the issue point. 
>- Multi-SWE-Bench & SWE-bench Multilingual: All scores are averaged across 8 runs using the [claude-code](https://github.com/anthropics/claude-code) CLI (300 max steps) as the evaluation scaffold.
>- Terminal-Bench: All scores are evaluated with the official claude-code from the original [Terminal-Bench](https://www.tbench.ai/) repository(commit `94bf692`), averaged over 8 runs to report the mean pass rate.
>- ArtifactsBench: All Scores are computed by averaging three runs with the official implementation of [ArtifactsBench](https://github.com/Tencent-Hunyuan/ArtifactsBenchmark), using the stable Gemini-2.5-Pro as the judge model.
>- BrowseComp & BrowseComp-zh & GAIA (text only) & xbench-DeepSearch: All scores reported use the same agent framework as [WebExplorer](https://arxiv.org/pdf/2509.06501) (Liu et al. 2025), with minor tools description adjustment. We use the 103-sample text-only GAIA validation subset following [WebExplorer](https://arxiv.org/pdf/2509.06501) (Liu et al. 2025).
>- HLE (w/ tools): All reported scores are obtained using search tools and a Python tool. The search tools employ the same agent framework as [WebExplorer](https://arxiv.org/pdf/2509.06501) (Liu et al. 2025), and the Python tool runs in a Jupyter environment. We use the text-only HLE subset.
>- τ²-Bench: All scores reported use "extended thinking with tool use", and employ GPT-4.1 as the user simulator.
>- FinSearchComp-global: Official results are reported for GPT-5-Thinking, Gemini 2.5 Pro, and Kimi-K2. Other models are evaluated using the open-source [FinSearchComp](https://arxiv.org/pdf/2509.13160) (Hu et al. 2025) framework using both  search and Python tools, launched simultaneously for consistency.
>- AgentCompany: All scores reported use OpenHands 0.42 agent framework.

---

## Intelligence Benchmarks

We align with **Artificial Analysis**, which aggregates challenging benchmarks using a consistent methodology to reflect a model’s broader **intelligence profile** across math, science, instruction following, coding, and agentic tool use.

| **Metric (AA)** | **MiniMax-M2** | **Claude Sonnet 4** | **Claude Sonnet 4.5** | **Gemini 2.5 Pro** | **GPT-5 (thinking)** | **GLM-4.6** | **Kimi K2 0905** | **DeepSeek-V3.2** |
|-----------------|----------------|---------------------|------------------------|---------------------|----------------------|-------------|------------------|-------------------|
| AIME25 | 78 | 74 | 88 | 88 | 94 | 86 | 57 | 88 |
| MMLU-Pro | 82 | 84 | 88 | 86 | 87 | 83 | 82 | 85 |
| GPQA-Diamond | 78 | 78 | 83 | 84 | 85 | 78 | 77 | 80 |
| HLE (w/o tools) | 12.5 | 9.6 | 17.3 | 21.1 | 26.5 | 13.3 | 6.3 | 13.8 |
| LiveCodeBench (LCB) | 83 | 66 | 71 | 80 | 85 | 70 | 61 | 79 |
| SciCode | 36 | 40 | 45 | 43 | 43 | 38 | 31 | 38 |
| IFBench | 72 | 55 | 57 | 49 | 73 | 43 | 42 | 54 |
| AA-LCR | 61 | 65 | 66 | 66 | 76 | 54 | 52 | 69 |
| τ²-Bench-Telecom | 87 | 65 | 78 | 54 | 85 | 71 | 73 | 34 |
| Terminal-Bench-Hard | 24 | 30 | 33 | 25 | 31 | 23 | 23 | 29 |
| **AA Intelligence** | 61 | 57 | 63 | 60 | 69 | 56 | 50 | 57 |

>AA: All scores of MiniMax-M2 aligned with Artificial Analysis Intelligence Benchmarking Methodology (https://artificialanalysis.ai/methodology/intelligence-benchmarking). All scores of other models reported from https://artificialanalysis.ai/.

---

## Why activation size matters

By maintaining activations around **10B** , the plan → act → verify loop in the agentic workflow is streamlined, improving responsiveness and reducing compute overhead:

- **Faster feedback cycles** in compile-run-test and browse-retrieve-cite chains.

- **More concurrent runs** on the same budget for regression suites and multi-seed explorations.

- **Simpler capacity planning** with smaller per-request memory and steadier tail latency.

In short: **10B activations = responsive agent loops + better unit economics**.

## At a glance

If you need frontier-style coding and agents without frontier-scale costs, **MiniMax-M2** hits the sweet spot: fast inference speeds, robust tool-use capabilities, and a deployment-friendly footprint.

We look forward to your feedback and to collaborating with developers and researchers to bring the future of intelligent collaboration one step closer.

## How to Use

- Our product **MiniMax Agent**, built on MiniMax-M2, is now **publicly available and free** for a limited time: https://agent.minimax.io/

- The MiniMax-M2 API is now live on the **MiniMax Open Platform** and is **free** for a limited time: https://platform.minimax.io/docs/guides/text-generation

- The MiniMax-M2 model weights are now **open-source**, allowing for local deployment and use: https://huggingface.co/MiniMaxAI/MiniMax-M2. 

## Local Deployment Guide

Download the model from HuggingFace repository: https://huggingface.co/MiniMaxAI/MiniMax-M2. We recommend using the following inference frameworks (listed alphabetically) to serve the model:

### SGLang

We recommend using [SGLang](https://docs.sglang.ai/) to serve MiniMax-M2. SGLang provides solid day-0 support for MiniMax-M2 model. Please refer to our [SGLang Deployment Guide](https://huggingface.co/MiniMaxAI/MiniMax-M2/blob/main/docs/sglang_deploy_guide.md) for more details, and thanks so much for our collaboration with the SGLang team.

### vLLM

We recommend using [vLLM](https://docs.vllm.ai/en/stable/) to serve MiniMax-M2. vLLM provides efficient day-0 support of MiniMax-M2 model, check https://docs.vllm.ai/projects/recipes/en/latest/MiniMax/MiniMax-M2.html for latest deployment guide. We also provide our [vLLM Deployment Guide](https://huggingface.co/MiniMaxAI/MiniMax-M2/blob/main/docs/vllm_deploy_guide.md).

### MLX

We recommend using [MLX-LM](https://github.com/ml-explore/mlx-lm) to serve MiniMax-M2.  Please refer to our [MLX Deployment Guide](https://huggingface.co/MiniMaxAI/MiniMax-M2/blob/main/docs/mlx_deploy_guide.md) for more details.

### Transformers

We recommend using [Transformers](https://github.com/huggingface/transformers) to serve MiniMax-M2.  Please refer to our [Transformers Deployment Guide](https://huggingface.co/MiniMaxAI/MiniMax-M2/blob/main/docs/transformers_deploy_guide.md) for more details.

### Inference Parameters
We recommend using the following parameters for best performance: `temperature=1.0`, `top_p = 0.95`, `top_k = 40`.

**IMPORTANT:** MiniMax-M2 is an interleaved thinking model. Therefore, when using it, it is important to retain the thinking content from the assistant's turns within the historical messages. In the model's output content, we use the `<think>...</think>` format to wrap the assistant's thinking content. When using the model, you must ensure that the historical content is passed back in its original format. Do not remove the `<think>...</think>` part, otherwise, the model's performance will be negatively affected.

## Tool Calling Guide

Please refer to our [Tool Calling Guide](https://huggingface.co/MiniMaxAI/MiniMax-M2/blob/main/docs/tool_calling_guide.md).



# Community Showcases

> The projects below are built and maintained by the community/partners. They are not official MiniMax products, and results may vary.

- **AnyCoder** — a web IDE–style coding assistant Space on Hugging Face, **uses MiniMax-M2 as the default model**: https://huggingface.co/spaces/akhaliq/anycoder  
  *Maintainer:* @akhaliq (Hugging Face)


# Contact Us

Contact us at [model@minimax.io](mailto:model@minimax.io) | [WeChat](https://github.com/MiniMax-AI/MiniMax-AI.github.io/blob/main/images/wechat-qrcode.jpeg).