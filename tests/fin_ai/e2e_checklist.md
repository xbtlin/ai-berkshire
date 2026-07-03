# 金融 AI 工具端到端验收清单

> 配额贵，不写自动化。手动按本清单逐项跑通。
> 准入要求：至少通 8/10。

## 准备

- [ ] 复制 `.env.example` 为 `.env`，填入真实凭证
- [ ] `python -c "import httpx; print(httpx.__version__)"` ≥ 0.27

## 10 项验收

- [ ] **1. 配置加载**：`python -m tools.fin_ai quota` 正常返回 remaining/limit
- [ ] **2. 单次查询**：`python -m tools.fin_ai ask "茅台研报观点"` 流式打印 + 元数据 footer
- [ ] **3. 缓存命中**：再次跑相同命令，输出 `[CACHE HIT]` 标记，**不消耗配额**
- [ ] **4. 多轮 REPL**：`python -m tools.fin_ai ask --multi "长城军工"` → 3 轮对话上下文延续
- [ ] **5. 强制刷新**：`python -m tools.fin_ai ask "茅台研报观点" --refresh` → 重新调用，覆盖缓存
- [ ] **6. TTL 覆盖**：`--ttl-hours 1` + 1h 后再查，验证失效
- [ ] **7. 配额耗尽**：手动构造 `exceeded=true` 场景（或改 daily_limit 配置），CLI 拒绝调用，exit 3
- [ ] **8. 错误凭证**：清空 `FIN_AI_AUTH_TOKEN`，跑 ask → exit 2 + 提示
- [ ] **9. Python 库**：`python -c "from tools.fin_ai import ask; print(ask('茅台').content[:50])"` 正常输出
- [ ] **10. skill 集成**：跑 `/investment-research 测试公司`，报告含「§X.X 金融 AI 观点补充」段落

## 准入规则

- 10 项通 8 项及以上：可合入主分支
- 通 7 项及以下：返回修复，不得合入

## 已知不验（YAGNI）

- 容器预热（pre-acquire）：spec §9 未决项，先观察首问延迟
- 服务端对话列表：用本地 history 替代
- 跨设备会话同步：单设备够用
