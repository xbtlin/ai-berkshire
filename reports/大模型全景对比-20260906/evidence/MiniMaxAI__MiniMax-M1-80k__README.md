---
pipeline_tag: text-generation
license: apache-2.0
library_name: transformers
tags:
- vllm
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

<div align="center" style="line-height: 1;">
  <a href="https://www.minimax.io" target="_blank" style="margin: 2px;">
    <img alt="Homepage" src="https://img.shields.io/badge/_Homepage-MiniMax-FF4040?style=flat-square&labelColor=2C3E50&logo=data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHhtbG5zOnhsaW5rPSJodHRwOi8vd3d3LnczLm9yZy8xOTk5L3hsaW5rIiB2aWV3Qm94PSIwIDAgNDkwLjE2IDQxMS43Ij48ZGVmcz48c3R5bGU+LmNscy0xe2ZpbGw6I2ZmZjt9PC9zdHlsZT48L2RlZnM+PHBhdGggY2xhc3M9ImNscy0xIiBkPSJNMjMzLjQ1LDQwLjgxYTE3LjU1LDE3LjU1LDAsMSwwLTM1LjEsMFYzMzEuNTZhNDAuODIsNDAuODIsMCwwLDEtODEuNjMsMFYxNDVhMTcuNTUsMTcuNTUsMCwxLDAtMzUuMDksMHY3OS4wNmE0MC44Miw0MC44MiwwLDAsMS04MS42MywwVjE5NS40MmExMS42MywxMS42MywwLDAsMSwyMy4yNiwwdjI4LjY2YTE3LjU1LDE3LjU1LDAsMCwwLDM1LjEsMFYxNDVBNDAuODIsNDAuODIsMCwwLDEsMTQwLDE0NVYzMzEuNTZhMTcuNTUsMTcuNTUsMCwwLDAsMzUuMSwwVjIxNy41aDBWNDAuODFhNDAuODEsNDAuODEsMCwxLDEsODEuNjIsMFYyODEuNTZhMTEuNjMsMTEuNjMsMCwxLDEtMjMuMjYsMFptMjE1LjksNjMuNEE0MC44Niw0MC44NiwwLDAsMCw0MDguNTMsMTQ1VjMwMC44NWExNy41NSwxNy41NSwwLDAsMS0zNS4wOSwwdi0yNjBhNDAuODIsNDAuODIsMCwwLDAtODEuNjMsMFYzNzAuODlhMTcuNTUsMTcuNTUsMCwwLDEtMzUuMSwwVjMzMGExMS42MywxMS42MywwLDEsMC0yMy4yNiwwdjQwLjg2YTQwLjgxLDQwLjgxLDAsMCwwLDgxLjYyLDBWNDAuODFhMTcuNTUsMTcuNTUsMCwwLDEsMzUuMSwwdjI2MGE0MC44Miw0MC44MiwwLDAsMCw4MS42MywwVjE0NWExNy41NSwxNy41NSwwLDEsMSwzNS4xLDBWMjgxLjU2YTExLjYzLDExLjYzLDAsMCwwLDIzLjI2LDBWMTQ1QTQwLjg1LDQwLjg1LDAsMCwwLDQ0OS4zNSwxMDQuMjFaIi8+PC9zdmc+&logoWidth=20" style="display: inline-block; vertical-align: middle;"/>
  </a>
  <a href="https://arxiv.org/abs/2506.13585" target="_blank" style="margin: 2px;">
    <img alt="Paper" src="https://img.shields.io/badge/📖_Paper-MiniMax--M1-FF4040?style=flat-square&labelColor=2C3E50" style="display: inline-block; vertical-align: middle;"/>
  </a>
  <a href="https://chat.minimax.io/" target="_blank" style="margin: 2px;">
    <img alt="Chat" src="https://img.shields.io/badge/_MiniMax_Chat-FF4040?style=flat-square&labelColor=2C3E50&logo=data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHhtbG5zOnhsaW5rPSJodHRwOi8vd3d3LnczLm9yZy8xOTk5L3hsaW5rIiB2aWV3Qm94PSIwIDAgNDkwLjE2IDQxMS43Ij48ZGVmcz48c3R5bGU+LmNscy0xe2ZpbGw6I2ZmZjt9PC9zdHlsZT48L2RlZnM+PHBhdGggY2xhc3M9ImNscy0xIiBkPSJNMjMzLjQ1LDQwLjgxYTE3LjU1LDE3LjU1LDAsMSwwLTM1LjEsMFYzMzEuNTZhNDAuODIsNDAuODIsMCwwLDEtODEuNjMsMFYxNDVhMTcuNTUsMTcuNTUsMCwxLDAtMzUuMDksMHY3OS4wNmE0MC44Miw0MC44MiwwLDAsMS04MS42MywwVjE5NS40MmExMS42MywxMS42MywwLDAsMSwyMy4yNiwwdjI4LjY2YTE3LjU1LDE3LjU1LDAsMCwwLDM1LjEsMFYxNDVBNDAuODIsNDAuODIsMCwwLDEsMTQwLDE0NVYzMzEuNTZhMTcuNTUsMTcuNTUsMCwwLDAsMzUuMSwwVjIxNy41aDBWNDAuODFhNDAuODEsNDAuODEsMCwxLDEsODEuNjIsMFYyODEuNTZhMTEuNjMsMTEuNjMsMCwxLDEtMjMuMjYsMFptMjE1LjksNjMuNEE0MC44Niw0MC44NiwwLDAsMCw0MDguNTMsMTQ1VjMwMC44NWExNy41NSwxNy41NSwwLDAsMS0zNS4wOSwwdi0yNjBhNDAuODIsNDAuODIsMCwwLDAtODEuNjMsMFYzNzAuODlhMTcuNTUsMTcuNTUsMCwwLDEtMzUuMSwwVjMzMGExMS42MywxMS42MywwLDEsMC0yMy4yNiwwdjQwLjg2YTQwLjgxLDQwLjgxLDAsMCwwLDgxLjYyLDBWNDAuODFhMTcuNTUsMTcuNTUsMCwwLDEsMzUuMSwwdjI2MGE0MC44Miw0MC44MiwwLDAsMCw4MS42MywwVjE0NWExNy41NSwxNy41NSwwLDEsMSwzNS4xLDBWMjgxLjU2YTExLjYzLDExLjYzLDAsMCwwLDIzLjI2LDBWMTQ1QTQwLjg1LDQwLjg1LDAsMCwwLDQ0OS4zNSwxMDQuMjFaIi8+PC9zdmc+&logoWidth=20" style="display: inline-block; vertical-align: middle;"/>
  </a>
  <a href="https://www.minimax.io/platform" style="margin: 2px;">
    <img alt="API" src="https://img.shields.io/badge/⚡_API-Platform-FF4040?style=flat-square&labelColor=2C3E50" style="display: inline-block; vertical-align: middle;"/>
  </a>
  <a href="https://github.com/MiniMax-AI/MiniMax-MCP" style="margin: 2px;">
    <img alt="MCP" src="https://img.shields.io/badge/🚀_MCP-MiniMax_MCP-FF4040?style=flat-square&labelColor=2C3E50" style="display: inline-block; vertical-align: middle;"/>
  </a>
</div>
<div align="center" style="line-height: 1;">
  <a href="https://huggingface.co/MiniMaxAI" target="_blank" style="margin: 2px;">
    <img alt="Hugging Face" src="https://img.shields.io/badge/🤗_Hugging_Face-MiniMax-FF4040?style=flat-square&labelColor=2C3E50" style="display: inline-block; vertical-align: middle;"/>
  </a>
  <a href="https://github.com/MiniMax-AI/MiniMax-M1" target="_blank" style="margin: 2px;">
    <img alt="GitHub" src="https://img.shields.io/badge/🐙_GitHub-MiniMax-FF4040?style=flat-square&labelColor=2C3E50" style="display: inline-block; vertical-align: middle;"/>
  </a>
  <a href="https://www.modelscope.cn/organization/MiniMax" target="_blank" style="margin: 2px;">
    <img alt="ModelScope" src="https://img.shields.io/badge/🤖️_ModelScope-MiniMax-FF4040?style=flat-square&labelColor=2C3E50" style="display: inline-block; vertical-align: middle;"/>
  </a>
  <a href="https://github.com/MiniMax-AI/MiniMax-M1/blob/main/LICENSE" style="margin: 2px;">
    <img alt="License" src="https://img.shields.io/badge/⚖️_License-Apache_2.0-FF4040?style=flat-square&labelColor=2C3E50" style="display: inline-block; vertical-align: middle;"/>
  </a>
  <a href="https://github.com/MiniMax-AI/MiniMax-AI.github.io/blob/main/images/wechat-qrcode.jpeg" target="_blank" style="margin: 2px;">
    <img alt="WeChat" src="https://img.shields.io/badge/💬_WeChat-MiniMax-FF4040?style=flat-square&labelColor=2C3E50" style="display: inline-block; vertical-align: middle;"/>
  </a>
</div>

# MiniMax-M1

## 1. Model Overview 

We introduce MiniMax-M1, the world's first open-weight, large-scale hybrid-attention reasoning model.
MiniMax-M1 is powered by a hybrid Mixture-of-Experts (MoE) architecture combined with a lightning
attention mechanism. The model is developed based on our previous [MiniMax-Text-01 model](https://huggingface.co/MiniMaxAI/MiniMax-Text-01), 
which contains a total of 456 billion parameters with 45.9 billion parameters activated
per token. Consistent with MiniMax-Text-01, the M1 model natively supports a context length of 1
million tokens, 8x the context size of DeepSeek R1. Furthermore, the lightning attention mechanism
in MiniMax-M1 enables efficient scaling of test-time compute – For example, compared to DeepSeek
R1, M1 consumes 25% of the FLOPs at a generation length of 100K tokens. These properties make M1
particularly suitable for complex tasks that require processing long inputs and thinking extensively.
MiniMax-M1 is trained using large-scale reinforcement learning (RL) on diverse problems ranging from
traditional mathematical reasoning to sandbox-based, real-world software engineering environments.
We develop an efficient RL scaling framework for M1 highlighting two perspectives: (1) We propose
CISPO, a novel algorithm that clips importance sampling weights instead of token updates, which
outperforms other competitive RL variants; (2) Our hybrid-attention design naturally enhances the
efficiency of RL, where we address unique challenges when scaling RL with the hybrid architecture. We
train two versions of MiniMax-M1 models with [40K](https://huggingface.co/MiniMaxAI/MiniMax-M1-40k) and 
[80K](https://huggingface.co/MiniMaxAI/MiniMax-M1-80k) thinking budgets respectively. Experiments
on standard benchmarks show that our models outperform other strong open-weight models such as
the original DeepSeek-R1 and Qwen3-235B, particularly on complex software engineering, tool using,
and long context tasks. With efficient scaling of test-time compute, MiniMax-M1 serves as a strong
foundation for next-generation language model agents to reason and tackle real-world challenges. 

<p align="center">
  <img width="100%" src="figures/TextBench.png">
  <br>
  <small><em>Benchmark performance comparison of leading commercial and open-weight models across competition-level mathematics, coding, software engineering, agentic tool use, and long-context understanding tasks. We use the MiniMax-M1-80k model here for MiniMax-M1.</em></small>
</p>


## 2. Evaluation

**Performance of MiniMax-M1 on core benchmarks.**


| **Category** | **Task** | **MiniMax-M1-80K** | **MiniMax-M1-40K** | **Qwen3-235B-A22B** | **DeepSeek-R1-0528** | **DeepSeek-R1** | **Seed-Thinking-v1.5** | **Claude 4 Opus** | **Gemini 2.5 Pro (06-05)** | **OpenAI-o3** |
|:---|:---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| | *Extended Thinking* | *80K* | *40K* | *32k* | *64k* | *32k* | *32k* | *64k* | *64k* | *100k* |
| ***Mathematics*** | AIME 2024 | 86.0 | 83.3 | 85.7 | 91.4 | 79.8 | 86.7 | 76.0 | 92.0 | 91.6 |
| | AIME 2025 | 76.9 | 74.6 | 81.5 | 87.5 | 70.0 | 74.0 | 75.5 | 88.0 | 88.9 |
| | MATH-500 | 96.8 | 96.0 | 96.2 | 98.0 | 97.3 | 96.7 | 98.2 | 98.8 | 98.1 |
| ***General Coding*** | LiveCodeBench *(24/8~25/5)* | 65.0 | 62.3 | 65.9 | 73.1 | 55.9 | 67.5 | 56.6 | 77.1 | 75.8 |
| | FullStackBench | 68.3 | 67.6 | 62.9 | 69.4 | 70.1 | 69.9 | 70.3 | -- | 69.3 |
| ***Reasoning & Knowledge***| GPQA Diamond | 70.0 | 69.2 | 71.1 | 81.0 | 71.5 | 77.3 | 79.6 | 86.4 | 83.3 |
| | HLE *(no tools)* | 8.4\* | 7.2\* | 7.6\* | 17.7\* | 8.6\* | 8.2 | 10.7 | 21.6 | 20.3 |
| | ZebraLogic | 86.8 | 80.1 | 80.3 | 95.1 | 78.7 | 84.4 | 95.1 | 91.6 | 95.8 |
| | MMLU-Pro | 81.1 | 80.6 | 83.0 | 85.0 | 84.0 | 87.0 | 85.0 | 86.0 | 85.0 |
| ***Software Engineering***| SWE-bench Verified| 56.0 | 55.6 | 34.4 | 57.6 | 49.2 | 47.0 | 72.5 | 67.2 | 69.1 |
| ***Long Context*** | OpenAI-MRCR *(128k)* | 73.4 | 76.1 | 27.7 | 51.5 | 35.8 | 54.3 | 48.9 | 76.8 | 56.5 |
| | OpenAI-MRCR *(1M)* | 56.2 | 58.6 | -- | -- | -- | -- | -- | 58.8 | -- |
| | LongBench-v2 | 61.5 | 61.0 | 50.1 | 52.1 | 58.3 | 52.5 | 55.6 | 65.0 | 58.8 |
| ***Agentic Tool Use***| TAU-bench *(airline)* | 62.0 | 60.0 | 34.7 | 53.5 | -- | 44.0 | 59.6 | 50.0 | 52.0 |
| | TAU-bench *(retail)* | 63.5 | 67.8 | 58.6 | 63.9 | -- | 55.7 | 81.4 | 67.0 | 73.9 |
| ***Factuality*** | SimpleQA | 18.5 | 17.9 | 11.0 | 27.8 | 30.1 | 12.9 | -- | 54.0 | 49.4 |
| ***General Assistant***| MultiChallenge | 44.7 | 44.7 | 40.0 | 45.0 | 40.7 | 43.0 | 45.8 | 51.8 | 56.5 |

\* conducted on the text-only HLE subset.

Our models are evaluated with `temperature=1.0`, `top_p=0.95`. 

### SWE-bench methodology 
We report results derived from the Agentless scaffold. Departing from the original pipeline, our methodology employs a two-stage localization process (without any embedding-based retrieval mechanisms): initial coarse-grained file localization followed by fine-grained localization to specific files and code elements. The values for our models are calculated on the subset of n=486 verified tasks which work on our infrastructure. The excluded 14 test cases that were incompatible with our internal infrastructure are:
`"astropy__astropy-7606"`,
`"astropy__astropy-8707"`,
`"astropy__astropy-8872"`,
`"django__django-10097"`,
`"matplotlib__matplotlib-20488"`,
`"psf__requests-2317"`,
`"psf__requests-2931"`,
`"psf__requests-5414"`,
`"pylint-dev__pylint-6528"`,
`"pylint-dev__pylint-7277"`,
`"sphinx-doc__sphinx-10435"`,
`"sphinx-doc__sphinx-7985"`,
`"sphinx-doc__sphinx-8269"`,
`"sphinx-doc__sphinx-8475"`

### TAU-bench methodology 
We evaluate TAU-Bench with GPT-4.1 as user model and without any custom tools. The maximum number of interaction steps is 40. 
Our general system prompt is: 
```
- In each round, you need to carefully examine the tools provided to you to determine if any can be used.
- You must adhere to all of the policies. Pay attention to the details in the terms. Solutions for most situations can be found within these policies.
``` 

## 3. Recommendations for Minimax-M1 Model Usage

To achieve the best results with the Minimax-M1 model, we suggest focusing on two key points: Inference Parameters and the System Prompt.

### 3.1. Inference Parameters
- Temperature: **`1.0`**
- Top_p: **`0.95`**

This setting is optimal for encouraging creativity and diversity in the model's responses. It allows the model to explore a wider range of linguistic possibilities, preventing outputs that are too rigid or repetitive, while still maintaining strong logical coherence.

### 3.2. System Prompt
Tailoring your system prompt to the specific task is crucial for guiding the model effectively. Below are suggested settings for different scenarios.

#### A. General-Purpose Scenarios
For common tasks like summarization, translation, Q&A, or creative writing:
```
You are a helpful assistant.
```
#### B. Web Development Scenarios
For complex tasks like generating code for web pages:
``` 
You are a web development engineer, writing web pages according to the instructions below. You are a powerful code editing assistant capable of writing code and creating artifacts in conversations with users, or modifying and updating existing artifacts as requested by users. 
All code is written in a single code block to form a complete code file for display, without separating HTML and JavaScript code. An artifact refers to a runnable complete code snippet, you prefer to integrate and output such complete runnable code rather than breaking it down into several code blocks. For certain types of code, they can render graphical interfaces in a UI window. After generation, please check the code execution again to ensure there are no errors in the output.
Output only the HTML, without any additional descriptive text. Make the UI looks modern and beautiful.
```
#### C. Mathematical Scenarios
When dealing with problems that require calculation or logical deduction:
```
Please reason step by step, and put your final answer within \boxed{}.
```

## 4. Deployment Guide

Download the model from HuggingFace repository: 
- [MiniMax-M1-40k](https://huggingface.co/MiniMaxAI/MiniMax-M1-40k)
- [MiniMax-M1-80k](https://huggingface.co/MiniMaxAI/MiniMax-M1-80k)

For production deployment, we recommend using [vLLM](https://docs.vllm.ai/en/latest/) to serve MiniMax-M1. vLLM provides excellent performance for serving large language models with the following features:
- 🔥 Outstanding service throughout performance
- ⚡ Efficient and intelligent memory management
- 📦 Powerful batch request processing capability
- ⚙️ Deeply optimized underlying performance

For detailed vLLM deployment instructions, please refer to our [vLLM Deployment Guide](./docs/vllm_deployment_guide.md). Special Note: Using vLLM versions below 0.9.2 may result in incompatibility or incorrect precision for the model.
Alternatively, you can also deploy using Transformers directly. For detailed Transformers deployment instructions, you can see our [MiniMax-M1 Transformers Deployment Guide](./docs/transformers_deployment_guide.md).


## 5. Function Calling

The MiniMax-M1 model supports function calling capabilities, enabling the model to identify when external functions need to be called and output function call parameters in a structured format. [MiniMax-M1 Function Call Guide](./docs/function_call_guide.md) provides detailed instructions on how to use the function calling feature of MiniMax-M1.


## 6. Chatbot & API
For general use and evaluation, we provide a [Chatbot](https://chat.minimax.io/) with online search capabilities and the [online API](https://www.minimax.io/platform/) for developers. For general use and evaluation, we provide the [MiniMax MCP Server](https://github.com/MiniMax-AI/MiniMax-MCP) with video generation, image generation, speech synthesis, and voice cloning for developers.


## 7. Citation
```
@misc{minimax2025minimaxm1scalingtesttimecompute,
      title={MiniMax-M1: Scaling Test-Time Compute Efficiently with Lightning Attention}, 
      author={MiniMax},
      year={2025},
      eprint={2506.13585},
      archivePrefix={arXiv},
      primaryClass={cs.CL},
      url={https://arxiv.org/abs/2506.13585}, 
}
```

## 8. Contact Us
Contact us at [model@minimax.io](mailto:model@minimax.io).