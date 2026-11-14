import fs from 'node:fs';
import ts from 'typescript';
const source=fs.readFileSync('content/curriculum.ts','utf8');
const js=ts.transpileModule(source,{compilerOptions:{module:ts.ModuleKind.ESNext,target:ts.ScriptTarget.ES2022}}).outputText;
const {lessons,resources}=await import('data:text/javascript;base64,'+Buffer.from(js).toString('base64'));
const lines=['# LLM 后训练系统学习导读','', '资料核验截止：2026-11-09。面向已有深度学习基础、希望掌握 SFT / DPO / RL 的学习者。','', '## 如何使用','', '以 RLHF Book 为主教材、Hugging Face 为实践入口、Stanford 为进阶补充。这里的“精选”是按一手性、系统性、可实践性和维护状况作出的编辑判断，不是客观全网排名。主线阅读资料免费，真实训练算力另计。','', '建议八周，每周约 6–10 小时，结课项目可能需要 8–12 小时；均为学习规划估计，不含长训练等待。先读本周导读，再到文末来源中查对应主题，完成验收任务与自测。','', '## 核心分类','', '- SFT / DPO / PPO / GRPO：训练目标或算法。','- LoRA / QLoRA：参数更新与显存策略，可搭配不同目标。','- RLHF / RLAIF / RLVR：人类反馈、AI 反馈与可验证奖励等反馈范式。','- 离线 DPO：固定偏好对；在线 RL：反复用当前或近期策略生成 rollout。异步生成、batch 内多次更新和引擎差异仍可能造成分布偏离。',''];
for(const l of lessons){lines.push(`## 第 ${Number(l.week)} 周：${l.title}`,'',`**目标：**${l.goal}（${l.hours}）`,'');for(const c of l.concepts)lines.push(`### ${c.title}`,'',c.text,'');lines.push('### 核心表达','',l.formula,'',l.symbols,'',`**常见误区：**${l.pitfall}`,'','### 验收任务','',...l.tasks.map(t=>'- [ ] '+t),'','### 自测','',l.quiz.q,'',...l.quiz.options.map((x,i)=>`${i+1}. ${x}`),'',`答案：${l.quiz.answer+1}。${l.quiz.why}`,'',`配套阅读：${l.refs.map(id=>resources.find(r=>r.id===id).title).join('；')}。原始链接统一列于文末。`,'')}
lines.push('## 可复跑实验交付模板','','1. 任务定义、模型与 tokenizer revision。','2. 数据来源、许可证、按问题族划分的 split、去重方法。','3. 环境锁定、训练配置、种子、硬件、峰值显存、训练与 rollout token 数。','4. 同测试集、同解码预算下的 base / SFT / DPO 或 RLVR 对照。','5. 消融与失败分析；报告样本数、波动和未能支持的推断。','','## 版本边界','','TRL 是滚动更新的实现。核验时 GRPO 默认 loss_type=dapo、beta=0.0，不等于原始 GRPO 配方。smol-course 单元开放程度不同，RL 实操以 TRL 和 LLM Course 第 12 章补足。CS336 当前主站为 Spring 2026，作业仓库主分支会更新。所有运行配置应锁定依赖与代码版本。','','## 参考资料','','以下为一手原始链接，访问核验日期均为 2026-11-09；本导读不复制第三方完整教材。','');
for(const r of resources)lines.push(`### ${r.title}`,'',`${r.author} · ${r.type} · ${r.level}`,'',r.why,'',`先读：${r.read}`,'',`边界：${r.limit}`,'',`[原始来源](${r.url})`,'');
fs.writeFileSync('public/learning-guide.md',lines.join('\n'));
const csv='实验ID,阶段,模型revision,数据revision,代码commit,依赖锁文件,seed,硬件,峰值显存GB,训练tokens,rollout_tokens,GPU小时,测试集,样本数,解码参数,最大输出长度,正确率,格式合法率,平均长度,胜率与判定规则,KL估计,失败案例,备注\n'+['base','sft','dpo','rlvr'].map((s,i)=>`${i+1},${s},,,,,,,,,,,,,,,,,,,,,`).join('\n')+'\n';
fs.writeFileSync('public/experiment-template.csv','\ufeff'+csv);
console.log(`Exported ${lessons.length} lessons / ${resources.length} sources.`);
