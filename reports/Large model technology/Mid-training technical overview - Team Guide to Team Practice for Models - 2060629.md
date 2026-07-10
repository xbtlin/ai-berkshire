# Mid-train Technical Overview and Landing Manual: A Model Team with Post-train Experience

Author process: author ' s first draft - > technocrat prick - > editor prick - > author revision
Time frame: information released for the last two years, with emphasis on coverage 2024-06-29 to 2026-06-29
Target audience: Post-training experience, team to assume mid-train; also suitable for Model/ Data/ Training/ Eval/ Post-train DRI
Conclusion nature: Technical research and engineering references, not constituting any commercial or investment proposal

# Use navigation/ mainline map

This article is not a summary of the literature that must be read from the beginning, but a gate-driven launch manual. If today’s Mid-training launch is to be held, you will read 0.2, 0.3, 8 and 9; if data and experiments are to be designed, read 4.2-4.6, 6, 11; if training has occurred, read directly 7; if public information and references to boundaries are to be verified, read 2, 3, 12.

There is only one main line: to prove that the target is worth the Mid-training, to prove the validity of the data and the assessment, to prove the effectiveness of the short-range training and to prove that the proceeds remain.

• Decision-making issues
| --- | --- | --- | --- |
<unk> Whether the need for mid-train is real, target capability, non-sacrificial capacity, alternative exclusions
What steps can public information support?
<unk> What's the first round of verification?
<unk> Data training, <unk> data data, license, pollution, synthetic data management, <unk> 4.2, 7.3, 9.1 <unk> data data memory memo <unk>
<unk> checkpoint Whether it is worth continuing <unk> corecard, guardrail, accident log, Pareto curves 5, 6, 7, 8.0 <unk> extend / rollback / kill decision making
Whether to retain the proceeds after the post-train
<unk> Go/no-go memo, model recovery, cost gains 8, 9, 13 <unk> scale / shrink/ stop

#0 Summary

Mid-train is not a magnifying post-train, nor is it simply a run-off. This paper uses a conservative definition of project:

> Mid-train is a postbase pretain, former post-train section of SFT/RL, etc., which continues to be controlled and trained to change the distribution of capabilities of models, their contextual adaptive capacity, and the subsequent trainingability available to SFT/RL.

In the public information, OLMO 2 explicitly refers to the postbase pretraining phase and the pre-post-training phase as Mid-training; Qwen3, DeepSeek-V3, Llama 3, Qwen2.5-1M and so on, not always uses the term, but rather as pre-training, recontinued pre-training, context interpretation or long-text pre-training.

In practice, the new team should not pursue large-scale training first, but rather small models (ablation, data barrel validation, pollution inspection, base regression assessment), then test the direction with a fixed post-train return, and test whether the proceeds are retained. Mid-train’s success criteria are not a base benchmark rise, but a gain that is still available after empowerment, oblivion, post-train.

On the border, this does not equate all continued pretraining with Mid-train, nor does it simply classify reasoning or architecture techniques like DCA, YarN, standard application, chunked prefill as a training formula. Public cases can only be used as design references and cannot be copied as recipipe.

The data ratio in the text, token Budget, 90-day road map, quality door and accident runbook are all project starters for new teams and are not the general conclusions given directly in the public papers.

For a team of model models with post-training experience and ready to take on mid-train, it is not the immediate mass training, but the first four things:

1. Clear target capabilities and non-sacrifice capabilities: Math upgrading, for example, cannot be achieved at the expense of universal dialogue, factual knowledge, multilingual competence.
2. Small models and short distances: validation of data drums, learning rates, sequence length, pollution control and risk of forgetting.
3. Establish a mid-train evaluation: not just pretrain loss, not post-post-post-post-post-post-post-post-post-post-post-post-post-post-post-post-post-post-post-post-post-post-post-post-post-post-post-post-post-post-post-post-post-post-post-post-post-post-post-post-post-post-post-post-post-post-post-post-post-post-post-post-post-post-post-post-post-post-post-post-post-post-post-post-post-post-post-post-post-for-post-post-post-post-post-post-for-post-post-post-post-for-post-post-post-post-post-post-post-post-post-post-post-post-post-post-for-service-service-for-service-service-service-for-service-service-service-service-for-service-for-service-service-service-service-service-service-service-for-for-service-service-service-service-service-service-service-service-service-service-service-service-service-service-service-service-service-service-service-service-service-service-service-service-service-service-service-service-service-service-service-service-service-service-service-service-service-service-service-service-service-service-service-service-service-service-service-service-service-service-service-service-service-service-service-service-service-service-service-service-service-service-service-service-service-service-service-service-service-service-
4. Let the Post-train DRI relay prove that one of the success criteria for mid-train is that the gains after SFT/RL remain manageable and more manageable than just base checkpoints for some of the zero-shot scores.

#0.1 Reader decision tree: What kind of mid-train do you really want to be?

The first round of the experiment, the key assessment, the beginning of the process, the beginning of the process.
| --- | --- | --- | --- | --- |
Mathematics, code, STEM, complex QA <unk> Capabilty Mid-train <unk> small model data mex + Low LR short-range training <unk> Target capability enhancement + Universal capability retreat <unk> also stretching to 128K/1M <unk>
<unk> 32K/128K Long context <unk> Context extension<unk> Gradual length extension + Long Document Data Bail
RL reading caps <unk> Reasoning substrate Mid-training <unk> Verifys if base has edge-of-competence <unk> Fixed RL/RLVR relays <unk> Use RL as a source of capacity per se
<unk> Vertical field capability <unk> Domain continued pretraining <unk> Data in low-ratio fields + General-fiscal data <unk> Field tasks + Universal-return <unk> Training in single-area language <unk>
Code agent / tool use <unk> Code/ FIM/trajetory Mid-training UIM, repo-level integration, multifile positioning <unk> repo task, editor task, post-train <unk> to move all interactive formats forward to Mid-train <unk>

This decision tree is an implementation portal, not an exclusive classification. A mature project may end up containing both capability, long-content adaptation and post-training assumptions, but it is best to test only one main hypothesis in the first round.

# 0.2 How do you start the first day?

If you want to start the Mid-training project today, don't start training first. Only seven things on the first day:

1. DRI of Model, Data, Training Infra, Eval, Post-Train, Safety/Compluriance, Project/Domain.
2. Write a page on Mid-train charter: Target capability, ability not to sacrifice, why must it be done in Mid-train, budget boundaries.
Freezing v0 owner and schema of the eval registry; freezing v1 exal registry before training, including base eval, special event, long context eval, private holdout, manual sample review. No v1, no Gate 1.
4. Freeing Post-train DR of v0 owner and schema of paired protocol; freezing of v1 pre-training protocol, including SFT/RL data version, training budget, Seed, harness, assessment set and failure determination.
5. Create a schema for the experiment, which requires that experiments without the bill not enter into conclusions.
Definition of the conditions of passage, the terms of the blocking and the signatory of Gate 0-5.
7. To clarify what is not allowed in the first week: not only do not look at private holdout side-trips, but not change the mix/filter/evenal version under the same experimental ID, and not consider proxy success as the main model.

##0.3 How to use this text: skip by role and task

This article can be read from the beginning or when it is in the internal manual.

♪ The role, the part, the chapter, the output that needs to be taken away ♪
| --- | --- | --- |
<unk> Decision owner / Model Leader 0, 1, 4.6, 8, 11 <unk> Project should be done, target capacity, non-sacrificial capacity, Gate 0-5 decision caliber <unk>
<unk> Data DRI 4.2, 4.2.1, 4.2.2, 7.3, 9.1 Data drum access cards, data manifest, pollution inspection, synthetic data boundary <unk>
<unk> Training Infra DRI 4.3, 4.5, 5, 7.4 <unk> Training Rotton Free, Context Curriculum, Checkpoint Line, resume runbook
Eval DRI <unk> 6, 7.5, 9.3, 12.3 <unk> enal reconciliation, scorecard, Holdout stratification, claim/source boundary <unk>
Post-train DRI <unk> 1.2, 6.6, 7.6, 8 <unk> paired protocol, Seed/budget/harness, retention of earnings
<unk> Safety / Project / Domain DRI 0.1, 4.1, 6.3, 7.1, 10 <unk> No loss of capacity, guardrail, real task, release block conditions

If only one 90-minute start-up session, the meeting will not discuss “How much token in the summary”, but rather will be reduced in the following order:

♪ Time, problem, ♪ ♪ Quit the condition ♪
| --- | --- | --- |
<unk> 0-15 minutes <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk>
<unk> 15-35 minutes <unk> Test which assumptions only are used in the first round <unk> make clear the main line in capability/ contact / domain / reading substrate
35-55 min data, eval, pot-train pretocal confirm data manifest, eval record, post-train pretcol owner
<unk> 55-75 minutes <unk> Gate 0-2 kill condition <unk> Write pollution, retreat, accident, post-train without profit cut-off line <unk>
75-90 minutes, what's the delivery and the non-construction conditions this week?

# 1. Terminology boundary: what is mid-train

# 1.1 A practical definition

This paper adopts a definition of engineering rather than a terminological pseudo-taint:

> Mid-train is the continuing training phase after base pretain, before post-train. It still uses mainly language modelling targets or their variants, but data, learning rates, sequence length and capability targets have shifted from "Maximum World Texts" to "Quality Capability Plastics".

This definition covers several types of public practice:

- Late-staage pretring / annealing: Continue training with high quality data at lower learning rates, pursuing lower losses and stronger downstream capabilities.
- Domain / capability continued training: continuing training around code, mathematics, STEM, medicine, law, finance, multilingualism, etc.
- Long-content interpretation: Expanding to 32K, 128K, 256K on original base context, etc., with position code, attachment optimization and long document data; if the target is a 1M level context, the training length, position/attention extrapolation, China prefill, KV cache and serving costs should be separately validated and cannot be simply continued training or data formulation.
- reading-oriented Mid-training: making base model more suitable for follow-up RL or RLVR using mathematics, code, synthetic reasoning, teaching materials, QA/CoT etc.

Mid-training and continued pretraining overlaps, but different points of emphasis: the continued pretraining describes “where training goes and runs”; and the mid-train emphasizes “why run, what data to make, how to serve post-train”.

#1.2 It's a distribution of # Post-train

Post-training teams can easily think of Mid-train as " More SFT Data" or " Earlier SFTs." This is dangerous because the two optimized objects are different.

Mid-training concerns:

- Whether the knowledge, algorithm models and presentation capabilities needed to solve the problem are available within the model.
- The availability of location codes, attachments, retrievals and cross-sections in long context.
- Whether the basic distribution of codes, mathematics, tool tracks, complex commands enter model parameters.
- Whether the SFT/RL is more likely to stimulate the ability.

Post-training concerns:

- Instructions followed, answering style, safe rejection, preference ranking.
- Multi-round dialogue and user alignment.
- Whether the reasoning process is outward-looking and in line with product strategies.
- Reward optimized behaviour in RL/RLHF/RLAIF/RLVR.

In rough terms, the mid-train is more oriented towards changing the ability to reach and within-parameter distribution, and the pot-train is more oriented towards changing the mission interface, behavioral strategies and product presentation; but in resoning, tool use, agent and long-term context tasks, the two overlaps and must be judged by the use of the paired protocol to determine where the benefits are from.

# 1.3 It's not appropriate to call all training #

The following is not simply classified as mid-train:

- Large-scale pre-training, starting from scratch.
- SFTs for alignment, security or formatting.
- Continue to run language modelling only on post-train data, but have no capacity targets, data control and regression assessment.
- System engineering for RAG, external tools, search in reasoning, etc. that do not change model parameters.

The boundaries are clear, otherwise the team will manage the Mid-train in a post-train assessment and organizational manner, and it will be difficult to determine where the benefits come from.

#1.4 Ten differences in recognition for the base model team with post-train experience

1. Mid-training is aimed at the distribution of competencies, not the style of responses.
2. The main loss of Mid-train is usually still close to the goal of language modelling rather than preference for optimization.
3. Mid-training data may contain QA/CoT/FIM, but do not move the SFT data forward as a whole.
4. The good checkpoint for Mid-train is not necessarily the least checkpoint, but the Pareto point between capacity enhancement and forgetting.
The proceeds of Mid-train must be observed in both base event and post-train rediness.
Data contamination is more dangerous than SFT in mid-train because it enters base capacity judgement.
Synthetic data are first validated and stratified and should not be increased by “favourable”.
8. Long context capabilities distinguish between the length of training, extrapolation and line service.
RL revenues are usually dependent on the availability of the base and cannot be passed on to RL.
The conditions for cessation must be met before the training is expanded; the mid-train is not “continue before the budget is spent”.

#2. Public evidence is weak and weak

The public information is not entirely consistent, and the most likely error is to mix the “comprehensiveness of researchers” and “industry experience in interviews” of the “training phase” that the report clearly spells out.

##2.0 Evidence label for this post

To avoid mixing public facts with engineering assumptions, the following text implicitly uses four categories of evidence labels:

The label, the label, the meaning, the meaning, the meaning, the meaning, the meaning, the meaning, the meaning, the meaning, the meaning, the meaning, the meaning, the meaning, the meaning, the meaning, the meaning, the meaning, the meaning, the meaning, the meaning, the meaning, the meaning, the meaning, the meaning, the meaning, the meaning, the meaning, the purpose, the purpose, the purpose, the purpose, the purpose, the purpose, the purpose, the purpose, the purpose, the purpose, the purpose, the purpose, the purpose, the purpose, the purpose, the purpose, the purpose, the purpose, the purpose, the purpose, the purpose, the purpose, the purpose, the purpose, the purpose, the purpose, the purpose, the purpose, the purpose, the purpose, the purpose, the purpose, the purpose, the purpose, the purpose, the purpose, the purpose, the purpose, the purpose, the purpose, the purpose, the purpose, the purpose, the purpose, the purpose, the purpose, the purpose, the purpose, the purpose, the purpose, the purpose, the purpose, the purpose, the purpose, the purpose, the, the, the, the, the purpose, the, the purpose, the purpose, the purpose, the, the, the, the, the purpose, the purpose, the purpose, the purpose, the purpose, the purpose, the purpose, the purpose, the purpose, the purpose, the purpose, the purpose, the purpose, the purpose, the purpose, the purpose, the purpose, the purpose, the purpose, the purpose, the purpose, the, the purpose, the purpose, the purpose, the purpose, the purpose, the purpose, the purpose, the purpose, the purpose, the purpose, the purpose, the purpose, the, the, the, the purpose, the purpose, the, the, the purpose, the
| --- | --- | --- | --- |
<unk> Reporting facts Technical report, paper or direct disclosure of official material, token, contact, data type, training target, description of what a team actually did, and launching other teams should carry the same formula
<unk> Thesis summarizes the mechanisms, taxony, variable relationships, etc., design interiors, create assumptions, directly upgrade to the industry-level training law
The conservative practice suggested by the study based on a number of cases, the development of project processes, gate, billing and risk control, the claim that it was the original conclusion of a report, the claim that the project was a project, the claim that the project was a project, the claim that the project was a project, the claim that the project was a project, the claim that the project was a project, the claim that the project was a project, the claim that the project was a project, the claim that the project was a project, the claim that the project was a project, the claim that the project was a project, the claim that the project was a project, the claim that the report was a project, the claim that the report was a project, the claim that the project was a project, the claim that the project was a project, the claim that the project was a project, the claim that the project was a project, the claim that the project was a project, the claim that the project was a project was a project, the case that was a project, the case that was a project, the case that was a project, the case that was a project, the case that was a project, the project was a project, the project, the project was a project, the project, the project was a project that was a project, the project that was a project that was a project that was a project that was a project, the project that was a project, the project that was a project, the project, the project that was a project, the project that was a project, the project that was a project, the project that was a project that was a project that was a project, the project, the project that the project that the project that was a project that the project, the project, the project, the project, the project, the project, the project, the project, the project that was a project that was a project
<unk> Pending verification of the hypothesis <unk> Interviews, blogs, industry calibres or direction inspired by small samples <unk> Entering small models/short-range experiments <unk> Entering master models for magnifying decision making <unk>

Readers should use the term “report facts” as a base of fact, using the words “discussions” and “engineering” as experimental design inputs, and “supposing assumptions” as backlogs. Any decision that consumes large-scale training budgets should be returned to the team’s own data database, eval review and post-training implemented project.

##2.1 Strong evidence: stage design for clear disclosure in technical reports

Strong evidence refers to the training phase, token scale, context length or data strategy that the model team directly discloses in the technical report.

The original term of the report, the public report, directly supports the project analogy.
| --- | --- | --- | --- |
<unk> mid-training <unk> mid-training - > instruction/preference turning up; more transparent details such as Dolmino Mix, 50B/100B/Micro-annealing <unk> mid-training public reference sample <unk>
Qwen3 pre-training stops / Development / Long Contracting stock; approximately 36 T total, approximately 5T reading-staying tokens, 32K long context training <unk> mid-training-like capability
<unk> DeepSeek-V3 <unk> long contextense 14.8 T base pre-training 4K->32K- >128K contextense <unk> Mid-train-like long-contextextense <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> long-long-long-ext interpretation
Qwen2.5-1M long-content pre-training / post-training / inference shopping / progressing long-context pre-training, post-training, DCA/YaRN extrapolation, dilution and chanked prefixing deployment <unk> contact adaptation + integration/deposition
<unk> Phi-4 predating / / post-training / / mpdtraining / /post-training; micttraining explicitly extends 4K context to 16K synthetic-heavy trading border + contact border samples
Llama pre-training / long-content pre-training / annealing <unk> 405B in 15.6 T pre-training, about 800B tokens long-context pre-training to 128K, and finally 40M tokens annealing <unk> late-staage contining pre-training and annealing

These reports support the existence of the "phase design" but usually do not support the "Run-up-data ratio or learning rate". Unpublished tokenizers, data cleansing, sampling strategies, base checkpoint states, optimizer status and system realizations have significant impact on results.

##2.2 Evidence: Summary and Summary of Controlled Experiments

The study Mid-training survey, PRISM and pre-training / Mid-training / RL interplay help teams understand the variable relationship: data retention versus ability migration, capacity at model reach borders, RL whether RL can benefit from mid-trained checkpoint, etc.

The value of these studies is to present institutional assumptions and experimental dimensions, rather than to give a direct extrapolable industrial formulation. In particular, controlled synthetic task or small-scale model conclusions cannot be directly upgraded to “all large model training laws”.

#2.3 Weak evidence: interviews, blogs and industry calibres

Interviews and blogs often provide two types of information: how the terms are used by practitioners, and how teams describe the organizational logic of the training phase. But such information often omits failed experiments, data details, and engineering constraints, so it can only be used as a trend background and not as a hard fact.

If the interview claims that a certain stage is “very important”, it is considered as a test assumption; training decisions are entered only after technical reports, reproducing experiments or within a team support.

#2.4 Conservative consensus from open sources

First, the mid-train-like phase usually occurs after the base capacity has been formed and before the post-training. OLMo 2 is a narrow sample; Qwen3, DeepSeek-V3, Qwen2.5-1M, Llama 3 is a closely related sample but with different terminology.

Second, in OLMo 2, Qwen3, Phi-4, Llama 3, etc., late-stay / agreed pre-training often accompanied by stronger data screening, capability-directional sampling or high-quality data upswing; but the DeepSeek-V3 cases mainly support the length of the phase-up and do not directly support the data matching. It is more prudent to say that the marginal value of late token relies more on quality, match-making and training objectives than simply adding web to to the conclusions.

Third, the long context is not just the RoPE context. Real and long context capabilities require training data, length curriculum, location/focus mechanisms, reasoning frameworks, and assessment missions.

Fourthly, it is more appropriate to consider the strong engineering hypothesis of “enhancement of RL available substrate” than the general rule that has been proven. The more conservative argument is that if base/mid-trained checkpoint is completely non-constructive to the target mission, RL usually has difficulty in generating capacity; but RL brings real capacity gains, depending on pretraining exposure, whether the task is located at the border of model capacity, reward design and exploration budgets.

Fifth, synthetic data are valuable, but not free lunches. Phi-4 describes synthetic data that can significantly influence the reading performance and reminds the team that organic data are still needed to complement the world ' s knowledge, express diversity and distribution.

Sixth, transparent experimental accounts are more important than a single list. One of the greatest values of OLMo 2 reports is to separate the composition of pretraining, mid-training, post-training and data, helping later teams to build their own lines, drums and returns assessments.

Seventh, the public report can prove that “some mature teams have adopted phased late-stage trading” but rarely that “a given data ratio, learning rate or token bugget is the best for common use.” All subsequent recipe tables should read search space and quality door instead of re-engineer formulas from a model report.

# 3. What a public case can prove, what a public case can prove

This chapter is not a recapitulation of the model report or a recipipe source. It only answers one question: what evidence the public case can provide to the new team’s Mid-Train project and which cannot be extrapolated.

This chapter only answers “what can public materials prove and which internal experimental variables inspire” and does not provide recalculateable training formulations. Any content that involves token numbers, context length, data type or sequence of stages is recorded in fact; training decisions are only made after the team's own data data database, val recovery, proxy application and post-train prepared process.

Case / Information <unk> Original report term <unk> Reporting facts <unk> This evidence label <unk> Safe summary <unk> No internal validation actions <unk>
| --- | --- | --- | --- | --- | --- | --- |
OLMo 2 <unk> Mid-training <unk> Clear mid-training phase, revealing Dolmino Mix, 50B/100B/300B, micro-annealing, pot-training layer <unk> Fact report + Project summary <unk> Mid-training line/evengate <unk> its Domino mix, token or English open source ecology suitable for other models
<unk> pre-training projects <unk> General / Development / Long Contracting project <unk> report facts + project analogy <unk> projectability mapping and contact targeting management <unk> original report self-described mid-training, or complete data matching <unk> decomposition <unk> decomposition <unk> capbility and context experiments <unk> experition_id <unk>
<unk> DeepSeek-V3 long contextent interpretation 14.8 T base pre-training 2nd paragraphs 4K->32K->128K contextextence and coordination with architecture/system reporting facts + engineering analogues must be verified simultaneously in the context of training, structure, serving, eval <unk> context interpretation equal to continuing training in general data to do offline/online long-term context consistency and short-mission regression
<unk> Phi-4 predating / / post-training <unk> Synthetic data training, visible midtraining undertaking 4K-> 16K extensions reporting facts + Project summary <unk> Synthesis data with vefier, style diversity and organic data pelt <unk> resoning gain can be attributed precisely to "computing CoT Mid-train" <unk> creating synthetic bug validation, template repetition and manual error rates <unk>
<unk> wen2.5-1M long-content pre-training / post-training / inference scaling <unk> 1M capability from 256K training, post-training, DCA/YaRN extrapolation and deployment optimized co-role reporting facts + engineering synthesizing training length, extrapolation, deployment costs and real tasks separately
Llama 3 <unk> initial pre-training / long-content pre-training / annealing <unk> ininational pre-training, long-content pre-training, reporting facts + project summary <unk> late-stalling requires binding high-quality data, LR, and checkpoint selects tokenbudget or annealing default values
<unk> PRISM / pre-mid-RL study <unk> mid-training / RL interplay <unk> reference, intervention, RL substrate <unk> summary of papers + pending validation hypothesis <unk> mechanism assumes to enter proxy array <unk> law of large model upgradeable industry <unk>

#3.1 OLMo 2: the clearest mid-training public paradigm

OLMo 2 explicitly refers to Phase II as mid-training: Phase I is a large-scale pre-training exercise, and Phase II is a training exercise using high-quality data such as Dolmino Mix, before it is made instruction and preference to turn. The report also reveals details such as the mid-training token sample, micr-annealing and checkpointing. It is best suited as a transparent reference sample, rather than as a default organizational template for all teams.

Convertable to internal assumptions/checks:

- Separates the Mid-train into a phase with input output and an event date.
- Not mix all data, but clearly distinguish between sources such as Dolma, DCLM, StarCoder, OpenWebMath.
- Keep base checkpoint independent evaluation before post-training.
- Use small-scale later training experiments such as micro-annealing to help determine whether the formula is worth magnifying.

The part that cannot be extrapolated:

- The open formula for OLMo 2 does not equal the best formula for all teams. It is transparent and learningable, not directly replicable.
- Its data structure is based on an open-source English ecology, and targets such as Chinese, multilingual, tool use, and agenic count need to be redrawn.

### 3.2 Qwen3：General -> Reasoning -> Long Context

The three-stage route that the report discloses is:

- General State: about 36 T tokens, of which S1 is over 30 T tokens, covering knowledge of the common language.
- Reisoning State: about 5T high quality STEM, code, reasoning and synthesis data, enhancing mission-related capabilities.
Long Context Stage: Hundreds of billions of tokens, extending the length of training to 32K.

This means that a mature team will design late-stage trading into multiple capability targets rather than a single “continue training” phase.

Convertable to internal assumptions/checks:

- Designs the capability type mid-train separately from the long context mid-train.
- Phase two is more like capability building, phase three is more like context adaptation.
- Distinguishing the length of training from the length of reasoning support: the training phase in the Qwen3 report was extended to 32K; ABF was a RoPE base adjustment, YaRN and DCA were used to further support the longer length of reasoning.
- The evaluation should also be separated: STEM/ Code/Riction for specific benchmark and real tasks; long context for documents, long code and multi-evidence tasks.

The part that cannot be extrapolated:

- The complete data matching for Qwen3 is not fully open and cannot be considered replicable recipe.
- "Enabling capacity or long-term context" depends on the product’s objective.

#3.3 DeepSeek-V3: Context extension and engineering constraints after mass base

The DeepSeek-V3 report gives two signals of importance to the Mid-training:

- 14.8 T High-quality, diverse token corresponding to base pre-training phase.
- After base pre-training, use YarRN for two paragraphs long-content interpretation, 1,000 steps, from 4K to 32K, and 32K to 128K.

In addition, DeepSeek-V3 training includes structure and training designs such as MLA, DeepSeekMoE, Auxiliary-los-free road planning, MTP. For the Mid-training team, this reminds us that if base structures, location codes, MoE routers, attachment memory and reasoning frameworks are not supported, later data may not reach their targets.

Convertable to internal assumptions/checks:

- Long context extension should be phased and not be carried over to the target length.
- Context interpretation prior to confirming the reasoning framework and the deployment mode of attachment kenel that can carry training.
- Monitor MoE load ballage, training stability and data drums while multi-target training is in progress.

The part that cannot be extrapolated:

- DeepSeek-V3 is a large system that is in-depth and synergistic from architecture to training and cannot be isolated from the long-term context.
- Many of the key efficiencies in its report are derived from systems and architecture, and the data/training phase is only part of the whole.
- The 128K Capability Presentation contains tests such as NAH and cannot alone prove the full capacity of the real long document, long code and online service.

# 3.4 Phi-4: synthetic-heavy trading strategy, not cleaning #

Phi-4 is more appropriate as a case of synthetic-heavy trading strategy than a clean “reasoning Mid-training” formula. The report does emphasize synthetic data for pretraining and midtraining; while the obvious midtraining stage is primarily extended from 4K to 16K, and provides training for approximately 250B tokens.The description of the value added in this paper is a project summary: public reporting supports synthetic data, curriculum design, data mixing and post-training, but cannot be attributed precisely to the contributions of the various components.

Convertable to internal assumptions/checks:

- Math, code, logical reasoning, teaching material interpretation is well suited to introduce verifiable or semi-verifiable synthetic data.
- Synthetic data should ideally be generated, filtered, validated, de-stressed, difficult to layer and style diversified processes.
- The small model looks first at the ratio of synthetic data, the difficulty of the problem, the length of the answer, the impact of correct filtering on final capacity.

The part that cannot be extrapolated:

- Synthetic data will magnify the bias and error of the techer model.
- If the template is created in a single format, the model learns the surface format "Looks like reasoning".
- High-quality organic data still need to be mixed for open domain knowledge, real users query and multilingual expression.

# 3.5 Qwen2.5-1M: Training expansion, extrapolation and deployment optimization separated

The Qwen2.5-1M report shows how long-term contextual capabilities are made up of training, post-training, extrapolation and deployment systems. A particular misreading is needed: 1M context is not simply taught directly through Mid-train data, but training is not important.

The more precise method of dismantling is:

Long-content pre-training: using progressive pre-training, driven roughly along a long line of 4K->32K->64K->128K->256K, using natural long files, growing context tasks and length distributions.
- Post-training: Using long command data and multistages, post-training makes the model more likely to perform user tasks in long contexts.
- Support / deployment: 1M from a combination of 256K long-content trade and DCA/YaRN extrapolating; diffusing, chiunked prefill, vLM/BladeLLM fit the deployment costs of the main services rather than the regular Mid-training data formulation.

Convertable to internal assumptions/checks:

- Long context is the ability to define four things together: models, data, training, and the reasoning framework.
- From 4K to 1M, the risk is very high and it is recommended that the consistency of training and reasoning be verified gradually by 8K/16K/32K/128K/256K.
- To avoid a single needle indicator, the assessment should include complex long documents QA, long code, tables, cross-section reasoning and probative tests.

Attention is needed to:

- 1M context is very complex in cost and deployment and may not be appropriate for all products.
- For most teams, 32K/128K high-quality availability may be more commercially valuable than a 1M demonstration capability.

#3.6 Llama 3: conservative samples from the indigence pre-training + long-context + annealing

Llama 3 series reports do not call the relevant phase Mid-training, but it gives a valuable conservative sample. In the 405B model, the report reveals that the indigence pre-training uses 8K context, about 15.6 T tokens; then long-context pre-training about 800 B tokens, extending from 8K to 128K in six; finally, 40M tokens do learning annealing to 0 and maintain 128K context, and some high-quality data.

Convertable to internal assumptions/checks:

- Late-staying can simultaneously assume long context adaptation and quality reduction, but must continue to be a universal capability return.
- Annealing is not a slogan for “retrain a little more”, but rather a stage of binding choice with data quality, learning rates, and the checkpoint.
- Llama 3 is inspired not by the pursuit of complex flowers, but by the decomposition of continuous training, long-term context and end-of-life harvests into observable steps, if the team is conservative.

The part that cannot be extrapolated:

- The specific token numbers and data formulations in the Llama 3 report rely on their large-scale basic training and are not suitable for migration to small team default budgets.
- Its long-term context and subsequent command model capabilities are also affected by the post-training and system realization.

#3.7 PRISM and pre/mid/RL study: use mechanism assumptions as assumptions

The value of PRISM and pre-training / Mid-training / RL interplay papers is to turn several long-standing empirical issues into experimental questions: how mid-training affects retention, what capabilities are mutually reinforcing or interfering in continuing training, and whether RL relies on the capability boundaries that have been exposed during the pre/mid phase.

Convertable to internal assumptions/checks:

- Dismantling the “retention of old” and “injection of new” capacities into two indicators, rather than just targeting capacity growth.
- Check whether the task is located in the model edge-of-competence as RL pre-screening.
- Use the conclusions of the controlled exercise as a reference for design, not as a direct primary training conclusion.

Attention is needed to:

- Such papers are usually controlled in terms of size, task and data distribution, and must be re-tested when extrapolated to industrial models.
- The judgement on resoning is particularly conservative: RL may magnify the capacity or the incentive gaps and formatting deviations.

#4. Mid-train design framework

This chapter is first read in the first round of the minimum closed loop: Gate 0 freezing target capacity, non-sacrificial ability, eval recovery and post-train prepared process; Gate 1 freezing data manifest; Gate 2 excluding the bad direction with control mix + 3-5 single variable variables in proxy scale; Gate 3 using target mode short-range training to find capability/forgotten Pareto checkpoint; Gate 4 using the same set of frozen past-train preset process to verify whether proceeds are retained.4.1-4.6 Explain the goal, data, training knobs, ablation, curiculum and organizational quality doors in the closed ring.

An implementable Mid-training project should ultimately answer five questions: what is the target capacity, what is not to degrade, which is driven by the data drums, how the length/learning rate/content curriculum of training is set up and how it can prove useful for post-training.

# 4.0 First round of the minimum closed

The minimum closed loop is not the minimum training formula, but the minimum evidence chain: whether data, training, evaluation and the post-training relay can be interpreted at the lowest possible experimental cost. Run through one target, one master hypothesis, one data drum, one short training window, one frozen post-train executed protocol.

♪ The little thing that's not there ♪
| --- | --- | --- | --- |
♪ Why must the target be capable, not at risk, not excluded from substitution ♪
<unk> Data <unk> Which drum may drive the target capability <unk> data manifest, pollution inspection, linked event, manual sample <unk> Back to the data drum access card <unk>
<unk> Training <unk> Whether low-risk short-range yields directional benefits <unk> Fixed checkpoint curves and drums loss <unk> back to the training knob or data mix <unk>
<unk> Assessment whether the proceeds are not public lists or falsely positive
Whether the proceeds after the relay post are retained
<unk> Decision / rollback / kill <unk> Gate dashboard, event_path, door

Chapter 11 gives a set of examples of search grids for this closed ring, not default formulas. Chapter 4 first deals with the design object, chapter 6-8 with how to judge the evidence, and chapter 11 gives the start-up example.

##4.1 Capability target layer

It is proposed to divide the objectives into four layers:

First level: Universal base sure

- The Universal Language Model lost doesn't go up very well.
- Common knowledge, facts, multilingualism, basic instruction, no significant deterioration.
- Multiple rounds of dialogue, although not the main Mid-training goal, cannot be broken down in terms of readability.

Second tier: enhanced core competencies

- Mathematics: GSM8K, MATH, AIME classes, and internal verifiable libraries.
- Codes: HumanEval, MBPP, EvalPlus, repo-level communication, FIM, multi-file positioning, etc.; SWE-bench is more suitable for use in fixed harmness, lightweight instraction grinding or post-training rediness.
STEM: GPQA, MMLU-Pro, domain database.
- Reason: BBC, ARC, Logical Logic, Complex QA.

Level 3: Structural capacity

- Long context retrieval, synthesis, conflict resolution.
- FIM, code completion, multi-file editing.
- Tables, logs, long-term PDF, summary of meetings.

Fourth floor: post-train readines

- Whether SFT is more likely to learn the target format after it.
- RL/RLVR is not more stable up.
- Rewarding hacking is decreasing.
- Whether the reasoning trajectory is more manageable.

##4.2 Data drum design

It is recommended that at least the following data drums be established:

<unk> Data drum <unk> Target <unk> Main risk <unk> Suggested control <unk>
| --- | --- | --- | --- |
High-quality web/ book <unk> Maintenance of universal language and world knowledge <unk> Noise, repetition, copyright/complimentation <unk> weight, quality classification, sampling cap
<unk> code programming capability, formalised structure <unk> license, repeat, benchmark leak <unk> license filter, repo re-rep, <unk>
Mathematical / STEM <unk> Logic and Symbolic Capability <unk> Simulation of the puzzle, error answers <unk> Authenticability, difficulty tiered, proof/ answer verification <unk>
<unk> Synthetic teaching materials <unk> Condensed concept, pedagogy reasoning <unk> Single style, wrong teacher <unk> multiteacher, multi-template, certifier filter <unk>
QA/ COT <unk> Logic trajectory and task format
<unk> Long document <unk> Long context adapted to empty padding, ineffectual token <unk> Real long document + Growing task <unk>
<unk> FIM/ Code Edit <unk> code agent capabilities <unk> destroy normal LM distribution <unk> barrel loss and code eval <unk>
<unk> Area data <unk> Industry/product capacity <unk> Catastrophe oblivion, narrowness <unk> Low percentage mix, general regression <unk>

Do not just do one global mix. Each barrel has:

- Data sources and records of the License.
- Go to the big game.
- Quality score.
- Contamination check.
- Sampling ratio.
- Alone.
- Corresponds to the eval.

##4.2.1 Data drum access card

Each data drum should be entered before training. The smallest field is as follows:

Fields
| --- | --- |
<unk> bucket_id ' / `bucket_name ' <unk> Data drum number and name <unk>
<unk> source_manifest '<unk> Original source, time frame, license/ compliance
<unk> Processing_committee '<unk> Purge, parsing, filtering script version
<unk> edup_version '<unk> Document, paragraph, code repo, title level de-re-re-version
<unk> contribution_version '<unk> and public benchmark, pravate holdout, synthetic pollution inspection version of the project
<unk> tokenizer_version 'tokenizer and special versions
`Quality_score_distortion ' <unk> Mass scoring distribution, not just average <unk>
<unk> language_domain_distrition '<unk> Language, field, file type, length distribution<unk>
<unk> time frame, old and new distribution, and whether to include new post-training events <unk>
<unk> sampling_weight '<unk> Shows weight and cap in current mix
`shuffle_seed ' / `bucket_interleaving ' <unk> Data sequence, bucket interwoven strategy, whether to make a phased change in the mix <unk>
<unk> bucket_valued_loss ' <unk> bunks value loss and abnormal changes
<unk> linked_evenal_id '<unk> for the evaluation item in the event review
`Known_risks` <unk> example, pollution, templateing, repetition, factual error, too narrow distribution

The data drum access door is proposed to be written as a hard rule:

- No manifest/ash, not into training.
- No corresponding eval, no higher sampling weight.
- Contamination hit untreated, not entering the prismary experiment.
- Synthetic data are not properly filtered and style diversity checks are not limited to low-ratio exploration.
- Field data do not have universal regression protection and do not enter the short course of the main model.
- Long context data are only collated text, without real tasks, and do not enter long-text prism mex.
- Any action to change filters, quality models, dedup thresholds, sampling weights, synthetic generation of propt or data sequences must generate new `data_manifest_hash ' and `experaction_id ' .

##4.2.2 Use boundaries for synthetic data

Synthetic data need to be addressed separately, as it is the most easy to “seem effective” on short-term indicators:

Risk, risk, performance, control, control.
| --- | --- | --- |
<unk> Teacher error magnification <unk> Math/code answers seem fluid but unverifiable <unk> Verifyable, answer check, sample manual review
<unk> Style template <unk> Output is all like the same teacher, reasoning moves fixed <unk> multiteacher, multiprompt, multi-drying, blending organic data <unk>
Benchmark, near pollution, public issue changes are on the rise, solver structures, embedding and translating duplicate checkup.
<unk> Difficulty distribution is not true <unk> Training is too simple or covers only one type <unk> Difficult batch, failure sample refill, private holdout comparison
<unk> COT excess before behavior <unk> base model early learns long interpretation format <unk> control of CT ratio, mix short answers, no COT, natural text <unk>

The logical use of synthetic data is the "verifiable ability amplifier" (CLM), not the low cost token alternative. Mathematics, codes, structural reasoning are suitable for multiple verifiable synthesis; open domain knowledge, language style, multilingual expression still requires a high quality organic data drive.

The boundaries of the different types of synthetic data are different:

<unk> Synthetic data type <unk> Suitable for use <unk> Unsuitable for use <unk> Must check <unk>
| --- | --- | --- | --- |
<unk> Authenticable mathematics/code <unk> Increase in symbol reasoning, executable resolution, unit test capability <unk> Replace open domain knowledge <unk> vereifier, answer execution, difficulty drums <unk>
<unk> Educational explanation <unk> Condensed concepts, completed knowledge structure <unk> Large proportion of natural language replacement <unk> teacher diversity, expression templates, fact check <unk>
<unk> COT/ réationale <unk> provides a path of reasoning <unk> let base pre-fix long answer style <unk> COT ratio, short-response mix, style drift <unk>
<unk> Long context synthesis task <unk> Covering scarce long task mode <unk> Replace real long document and long code <unk> Evidence location, interference with information, non-response sample <unk>
<unk> Area synthesis QA <unk> Fields to complement Tasking typologies <unk> Alternative field files <unk> Expert sample, source tracking, terminology consistency <unk>

Synthetic Bucket must also record the teacher mode/version, generate prompt, sample parameters, version of the verifier, filter rules, percentage of rejected samples, template repetition, answer-verifiability, manual pictor error rate, and whether the generator has read the eval/ benchmark. Synthetic CoT/QA will check style entropy, templace n-gram and respence Length pattern to avoid pre-stabilizing the past-training behavior format.

# 4.3 Learning rate and token Budget

Public reporting does not usually give all the details in full, but there are several robust principles in the project.

First, the mid-train should not normally use high learning rates close to the beginning of pretrain. Models have developed a large number of generic competencies, and over-learning rates can lead to forgetting, style drifting and lost style.

Second, learning rate strategies are geared towards matching objectives:

- Shorter-range capacity enhancement: continuing training with low learning rates, observation of specialized competencies and generic return.
- Late-staying: further reducing learning rates and reducing them with high-quality data.
- Context interpretation: learning rates are more conservative and match length curriculum.
- Domain adaptation: limit token binget and data ratio and avoid narrow models.

Third, token Budget is not as big as it gets. The following three steps are just conservative scales for initiating experiments, are not linear in nature at the scale of the model, and are not a substitute for scaling effort:

- 1B-10B tokens: for pipeline, data quality, LR, pollution inspection and production.
- 10B-100B tokens: As an example interval for observable capacity enhancement and small and medium model validation, the actual budget is determined by the size of the model, data quality and the date of the results.
- 100B-1T+tokens: either suitable for a more complete model capability scheming or long-context interpretation.

These are not industry laws, but more conservative engineering start-ups. The true scale of the models, data quality, target capacity and budget are to be determined jointly.

## 4.3.1 The formula button cannot change the principle simultaneously

Training variables are also frozen as data and eval. At least every run records:

Why freeze?
| --- | --- | --- |
<unk> base_checkpoint_hash ' <unk> Determines starting capacity and available data exposure
<unk> optimizer_state_strategy ' <unk> Success or replacement will change the loss curve and stability <unk> Replace warmup deficiency leads to false degradation <unk>
<unk> lr_schedule / `warmup ' <unk> influences forgetting, gathering and lost spot <unk> to compare final scores and not to compare training stability <unk>
<unk> peak_lr`/ `min_lr`/ `decay_shape ' <unk> decides to actually optimize the trajectory <unk> is called "low LR," but the training dynamics are completely different
<unk> gradient_clipping ' / `precision ' <unk> Impact stability and numerical error <unk>
`global_batch ' / `microbatch ' <unk> Change effective battling and training noise <unk> Small batt sound misconstrued to ability fluctuations <unk>
`Sequence_lenth_disarmament ' / `length_bucket_ratio ' <unk> Changes in effective token distribution and training dynamics <unk>
`data_order ' / `shuffle_seed ' <unk> curriculum, annealing, long context-sensitive <unk> The same mix order leads to the opposite conclusion
<unk> packing_policy ' / `masking_policy ' <unk> Impact on FIM, long files and short sample ratios <unk> Short task degradation but global loss normal <unk>
<unk> checkpoint_section_policy ' <unk> decides to compare the final object with the final target <unk> pick the best checkpoint afterwards
`veval_cadence ' , determining when to find forgotten and drifting , <unk> training to find irreversible retreat <unk>

The success of Proxy will only mean that a certain direction is worth continuing, not that the target size will necessarily succeed. At least four conditions are met before entering more training:

1. The two scale or target short run are in the same direction.
2. Changes in the drums loss, target eval, base restatement can be explained by the same data/training assumptions.
3. The same cross under different seed does not reverse, training in vomiting, checkpoint resume and surveillance have been verified.
4. Costly acceptable: If the 10 times token scale is increased and only marginal gains are possible, the data or the evaal should be improved rather than added to the budget.

Do not change too many knobs at the same time in an experiment. It is suggested that the usual knobs be opened:

♪ The key risks ♪
| --- | --- | --- | --- | --- |
LR/ warmup low LR, further decrease, short warmup sweep <unk> forget, lose spice, slow-down, lose, lose, drop, gradient, speke not recovering or the true indicator falling fast
Token Budget <unk> Increment short budget <unk> Waste budget, over-programming narrow distribution <unk> checkpoint interdeta, Pareto curve <unk> Marginal gains disappear or retreat to expand <unk>
<unk> Order length <unk>
<unk> Batch / packing <unk> Change packing, mixing sample <unk> Effective data distribution change <unk> toss, padding, short sample loss loss <unk> all normal but drums abnormal <unk>
<unk> Optimizer state <unk> succession or reset <unk> succession dynamics or warmup are insufficient <unk> early loss, gradient, resume continuity <unk> early only instabileity cannot explain <unk>
<unk> Synthetic rateo <unk> Step-by-step caps Templates, wrong magnifications, private eval, style review, failed examples <unk> Style collapse or private collection non-increasing <unk>
<unk> Domain ratio <unk> Low-ratio mix <unk> narrow model, common capability degradation <unk> general regression, private field tasks <unk> field increase is less than generic recovery costs <unk>

##4.4 First round of design table

The first round does not seek the “best formula” but quickly removes the wrong direction. The following scale is a sample of variables that are used to reveal sensitivity and bad direction and cannot be used as a default for primary training.

<unk> Experimental purpose <unk> Model size example<unk> Token Budget example<unk> Data mix search variable example<unk> LR variable<unk> Success indicator<unk> Stop condition<unk>
| --- | --- | --- | --- | --- | --- | --- |
<unk> Pipeline and eval calibration proxy model, e. g. 1B/3B<unk> 1B-3B tokens <unk> small sample drums mix <unk> low LR single point <unk> loss normal, eval can recreate <unk> los spice, eval unstable <unk>
<unk> Generic baseline <unk> proxy model, e.g. 3B/7B<unk> 3B-10B tokens <unk> Universal high quality ratio 30/50/70% <unk> Fixed low LR<unk> Universal ability to withdraw control <unk> Multilingual/fact crash <unk>
<unk> Math/STEM Injects Proxy model, e.g. 3B/7B<unk> 5B-20B tokens<unk> Mathematics/STEM 10/20/30%
<unk> code/FIM injects <unk> proxy model, e.g. 3B/7B<unk> 5B-20B tokens <unk> code/FIM 10/20/30 <unk> Fixed Low LR<unk> completion/FIM/repo task Upgrade <unk> Normal Generate Clear Codeization
<unk> Synthetic data ratio <unk> proxy model, e.g. 3B/7B<unk> 5B-20B tokens<unk> synthetic 5/15/30%
<unk> Primary model short-range validation 10B-100B tokens <unk> 2-3 <unk> 6 mix <unk> low LR sweep <unk> Pareto checkpoint appears <unk> target capacity not rising or forgotten too much <unk>

The output of these experiments is not a final model, but a decision as to which data drums are valid, which proportion is dangerous, which learning rate is safe between regions and whether it is worth more major training.

# 4.4.1 How to read

The output of Ablation is to exclude bad directions and to create a candidate, not to prove the final formula.

Proxy success is not equal to the success of target; two scale are required in the same direction before entering the main model, or a short run run review of the target.
2. A single public roll rise is not equivalent to an increase in capacity; it must be seen together with a private holdout, a sample of failures, and manual review.
3. Target ' s ability must be seen with the guardrail; the increase in mathematics/codes and the marked drop in speech, fact, natural creation are not clean gains.
4. Results close to the threshold are repeated or reviewed by adjacent checkpoints; not a small gain from a single perceived gain is used to make the decision.
Any midway conversion of the version of the micix, filter, LR, length curiculum or eval must be reopened.

# 4.5 Curriculum: Capability, later length, parallel?

It is recommended that the new team not mix all targets at the outset.

The more stable order is:

Base surety check: confirm the availability of checkpoint, tokenizer, optimizer state, data pipeline, evaluation system.
2. Capable mid-train: Mathematics/code/STEM/Quality synthesis data, short range ablation.
3. Long context: gradually stretching from shorter context, with separate surveillance of the boss 's context loss and real tasks.
4. Small-scale post-training relay: compare Mid-train with SFT/RL comparison checkpoint.
5. Whether to merge into the main training formula.

Why do you suggest a length after capacity? Because long context training is expensive, debug is difficult, and it is easy to mix architecture with data problems. If model base reading/code capability does not improve, long context simply magnifies input windows, not necessarily mission capacity.

There are exceptions: if the product is targeted by the law/finance master document QA or the code bank, the context can be pre-set, but it is still recommended that the small model be validated first.

<unk> , product owner, <unk> , recommended a priori, <unk> , first round of verification, <unk> , countersigned signal, <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> ,<unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk>
| --- | --- | --- | --- |
<unk> Math, Code, STEM, Complex QA <unk> Capability, later length + General Conservancy Drum Shorter
<unk> Legal/financial/ scientific master file QA <unk> capacity and length parallel, but two experimental IDs, one 32K/64K short-range <unk> long context search but complex/conflict/non-response task
<unk> Code/ FIM parallel to medium-term context <unk> FIM/repo task, long-code positioning, short-code return <unk> repo task up but normal code generation or short-mission degradation <unk>
<unk> Fields continue to be trained <unk> Areas first low proportion, then whether they need to be long <unk> Area 5/10/20% + Generic Return <unk> Field tasks increase less than generic capability recovery costs <unk>
<unk> long context display capability <unk> confirm product value and then do real long tasks, service costs, short-mission returns <unk> NAH good but no real tasks, online costs or short-missions <unk>

Longer context curriculum records the length distribution, not the maximum length.

- 4K/16K/32K/64K/128K sample ratio.
- Packing strategy, padding waste, short samples oversampled.
- Long sample source: natural long document, long code, co-generation task, cross-document collection.
- Mission structure: density of evidence, non-response samples, conflict evidence, multi-trip evidence, location of evidence, length of output.
- Training whether the Kernel matches the reasoning of the Kernel.

Otherwise, “extension to 128K” is a maximum length statement that does not explain whether the model has learned long context understanding, long distance retrieval or simply learn to keep the loss in longer input.

## 4.6 Organizational running mechanisms: roles, accounts and quality doors

The Mid-training project is not a continuation of the model that the training team has completed alone, but rather a data, training, eval, pot-train, a single experimental desk, a single group of quality doors, a capacity-building project.

First, the DRI is set, not the general “multi-team involvement”.

♪ The only thing that's ever been done ♪
| --- | --- | --- | --- | --- |
<unk> Model Lead <unk> Product/Domain, Eval, Post-train <unk> Model Lead <unk> Mid-train charter, no-sacrificial, experimental hypothesis
Data construction <unk> Data DATA DRI <unk> Research, Safety/Compluriance, Eval <unk> Data DRI + Safety/Compluriance <unk> Data Barkler Description, data manyest/ash, lineage, communication report
Training Infra DRI <unk> Model, Data, Infra <unk> Training Infra DRI <unk> Runbook, LR/token Budget configuration, checkpoint ledger, incident log
<unk> Evaluation system Eval DRI <unk> Model, Product/Domain, Post-training <unk> Eval DRI <unk> enal review, private holdout, scorecard, manual review sample
Post-train relays Post-train DRI Eval, Safety, Model
Infra DRI <unk> Training, Eval, Serving <unk> Infra DRI + Eval DRI <unk> kennel/serving Consistency Report, KV cache/latency/cost Evaluation
Risk and release of <unk> Safety/ComplishDRI<unk> Data, Project, Release<unk> Decision owner<unk> Compliance Review, Risk Register, go/no-go memo<unk>

Second, the experimental account must be fixed schema. The experiment without the account does not lead to conclusions; any intermediate change in the mix, filter change, and the eval version must be created.

Fields
| --- | --- |
<unk> Experiment_id / `hyphotesis ' / `owner ' <unk> Experiment number, assumptions to be verified, sole authority <unk>
<unk> base_checkpoint_hash ' / `training_code_committee ' <unk> Start checkpoint and training code version <unk>
<unk> data_manifest_hash ' / `data_bucket_rate ' <unk> Data manifest, sampling weight, data drum ratio<unk>
<unk> dedup_version ' / `convention_version ' <unk> Heavy, near-repeated and contaminated-checked version <unk>
<unk> lr_schedule` / `warmup` / `optimizer_state_strategy ' <unk> Learning rate, warmup, optimizer state
<unk> token_budget` / `security_legth_disarmament ' <unk> token budget and length distribution, not only recording maximum length <unk>
`eval_sue_version ' / `private_holdout_version ' , `eval reconciliation ' , private holdout, harnesscommittee .
`Seed ' / `cost ' / `incident_log ' <unk> Random seeds, training costs, anomalies and processing actions <unk>
<unk> Summary of the conclusions of `reult_summary ' / `dission ' / `signoff ' , <unk> , kill/retry/extend/promote decision-making, signatory <unk>
<unk> post_training_readines_result ' <unk> Fixed SFT/RL proceeds retained

Third, the only authority for the quality door is placed in section 8.0; this section only defines roles, desk fields and signature duties. This does not set a threshold for teams, but the minimum level of target capacity, the maximum withdrawal of generic capabilities, private event pass rates, the maximum pollution mean, the Loss Spike treatment rules, style drift determination, and the ratio of proceeds retained after the post-train status, evidentiary path, version Hash and expiry times are defined as section 8.0 dashboard.

<unk> Gate <unk> Entry conditions <unk> Exit conditions <unk> Interrupting conditions <unk> Signator <unk>
| --- | --- | --- | --- | --- |
<unk> Gate 0: target capacity, non-sacrificial capacity, budget and post-train relay needs are identified <unk> Mid-train charter passed; v1val relay and v1 post-train pretocol status is based on section 8.0 dashboard DRI, none of the whited protocol owner/schema, no private owner homeer/schema <unk> Model Lead, Eval Dri, Post-train Dri <unk>
<unk> Gate 1: Data freeze Data source, License, Cleaning, Reloading and Contamination check complete
<unk> Gate 2: Proxy campaign <unk> at least two candidates mics and fixed event suite <unk> proxy are used to exclude bad directions; two scales are required to match or target short-range to verify key signals <unk> to increase the public benchmark, private tasks remain intact, general capabilities <unk> Model Lead, Eval DRI, Data DRI <unk>
<unk> Gate 3: Main model short course training runbook, resume, surveillance and kill switch ready <unk> Pareto checkpoint, pine break can explain <unk> nan, unrecoverable los spike, gradient anomaly, vomit anomaly, resume incoherent, short-term, long-term, long-term, short-term tasks <unk> Training Infra DRI, Eval DRI, Model Lead
<unk> Gate 4: Post-train relay recipe, seed, budget, harness, failed determinations frozen post-protocol proceeds retained without significant deterioration <unk> mid-train proceeds disappeared after post-protin, passed protocol changes or difficulties increased significantly
<unk> Gate 5: Magnifying training Source of proceeds: data/evenal/auto-automated stable Go/no-go memo Pass, entering the next budget <unk> Reliance on pollution, narrow assessment, occasional checkpoint or inability to recreate <unk> Decision owner, Model Lead, Release owner <unk>

Fourth, the pace of meetings is to serve decision-making and not to report:

- Daily trading review: loss, vomiting, nn/loss spice, checkpoint, resume, accident management.
- Twiice-weekly event review: target capability, general return, private holdout, manual sample review.
- Weekly decision review:kill, retry, extend, promote, based on billing and gate memo decision-making only.
- Whether Post-train handoff review: Paired protocol is effective, whether the proceeds are preserved and whether security and style are degraded.

The bottom line of the mechanism is that calendars are not a substitute for quality doors. 90 days is just a reference rhythm, and it is determined by data readiness, training stability, val stability and the post-training relay.

#5. Training Engineering Checkpoint

# 5.1 Pre-start check

Before starting mid-train, complete:

- Base checkpoint's full eval snapshot.
- Whether the Optimizer state continues the decision.
- Tokenizer and special tokens freeze.
- Data to weigh and benchmark verification check.
- Sample review of each data drum.
- Small-scale dry run, confirming loss, vomiting, visible, checkpoint, resume normal.
- Post-train DRI confirms the follow-up SFT/RL paired protocol.

If the post-train relay is not validated, the mistarget is easily optimized.

#5.2 Surveillance in training

At least, we need surveillance:

- Global trading loss/ valuation loss.
- Qualified loss by data drum.
- The return of the universal capacity benchmark.
- The target capacity benchmark gain.
- loss of different length segments of the long context.
- Generate a model of style drift.
- Expert loads, route entropy and token drops of MoE models.
- Difference between gradient parameters, Loss Spike, and Checkpoint.

Do not wait for the training to be done. The failure of Mid-train often comes at an early stage: a universal eval drop, output style template, a data drum loss anomaly, long context short mission degradation.

#5.3 Checkpoint Policy

Suggested retention:

- pre-mid checkpoint。
- Early/mid/final checkpoint for each stage.
- Checkpoint before and after the change in the learning rate.
- Context length criculum checkpoint for each length.
- Candidates for the post-training relay checkpoint.

Not just the last. The best checkpoint for Mid-train may not be the least checkpoint for the lost, but the best for Pareto between the target ability and the forgotten.

# 5.4 Easily underestimated engineering risks

First, mass-lingth batting and context parallelism can cause load imbalances. The long-term catch-batch-showing, waste-and-communication patterns are different from the short-situation context, and training surveillance must be removed by length, otherwise the whole-scale vomiting will mask local instability.

Second, there may be problems with the succession or replacement of the ottiizer state. The succession of the otimizer state is more like an extension of the original training trajectory, but may inherit the old stage momentum; the reset of the otimizer state is cleaner, but the re-engineering of the warmup is necessary, otherwise it is easy to lose spike or slow-down. Both options should be measured at the proxy scale.

Third, training kenel and deployment of attachment kenel are inconsistent with creating false positives. Offline eval does not represent 128K/1M service available on line; long context training, extrapolation, kv cache, China prefill, sparse attachment and serviceing frameworks must be jointly validated.

#6. Assessment system

# 6.0 from benchmark list to eval recall

Mid-training does not collect the list, but a set of eval object versions, contamination status, running harness, thresholds and original output archive; the assessment results are not entered into registry and can only be observed and not used as a go/no-go basis.

Each project sets a maximum of 3-5 prism indicators, with several additional guardrails and diagnostics. Primaric is too much to induce a cherry-nick, and diagnostic is too little to make the team aware of why it is going to go up and down.

# 6.1 Eval review schema

Eval DRI should freeze v0 owner and schema in Gate 0 and then freeze v1 emergency record before entering Gate 1. The smallest field is as follows:

<unk> Fields <unk> Meaning <unk>
| --- | --- |
<unk> eveal_id '<unk> Unique number
| `eval_family` | base regression / target capability / long-context / post-train readiness / safety-style |
<unk> task_name ' <unk> taskname <unk>
| `data_source` | public / dev-private / sealed-private / final-blind / synthetic / human-written |
<unk> Created_at / `data_hash ' <unk> creation time and data hash; private collection must be earlier than corresponding training data
| `split_policy` | dev / private holdout / regression set / final-blind |
| `contamination_check_version` | exact / n-gram / MinHash / embedding / paraphrase / translated duplicate / manual |
<unk> harness_committee '<unk> Evaluation Code Version <unk>
<unk> prompt_or_wrapper_version 'base prompt, minimal prompt, new-shot policy, light instruction grinder, agent
`decoding_params ' <unk> temperature, top_p, max tokens, pass@k
`Metric ' / `agggregation ' <unk> Accuracy, pass@k, F1, judge score, latency/cost, etc., and the way of aggregation
| `decision_role` | primary / guardrail / diagnostic |
<unk> threshold_or_guardrail ' <unk> Raise threshold, maximum retreat, failure conditions, minimum significant differences <unk>
<unk> sample_size`<unk> Sample volume and sampling rules<unk>
`manual_review_rubric ' <unk> Rubric <unk> when manual review is required
<unk> raw_output_path '<unk> Original output archive location<unk>
`owner_note ' , explanatory note, leaving aside organizational responsibility

The Eval version changes rules to be dead: changing samples, changing programs, changing answers, changing metrics, changing harness, changing thresholds must generate a new `evenal_sue_version ' , with old results that cannot be confused horizontally.

Private holdout suggests three layers:

- dev-private: modulate pipeline, calibrate harm, not enter the final date.
- Sealed-private: Phase door use, which prohibits the modulation of data to it, or the introduction of data.
- Final-blind: used only before Gate 5 or release, to avoid being repeatedly optimized as “another set of training objectives”.

### 6.2 Eval suite matrix

Eval family purpose, mission, task, taskpoint, checkpoint, metric, failed signal, Raw output, request.
| --- | --- | --- | --- | --- | --- | --- |
Base review protection of ability not to be sacrificed
Target capability <unk> Determines whether target capabilities are really stronger
Long-content <unk> Whether long context can be judged by QA, conflict resolution, long code positioning, long table/log <unk> Mid, post-train after <unk> long drum performance, short mission regression, latency/cost <unk> needle full but real task input length, evidentiary location, Backend configuration
Post-training returns <unk> Whether the proceeds are retained after SFT/RL and the real task and security assessment after SFT/RL fixes
<unk> Safety/ style <unk> Prevention of style, safety and rejection of drifting <unk> Security set, denial of boundaries, Chinese writing, long-term quality of answers <unk> Mid, post-post-train <unk> Return rate, artificial rubric, denial of response to errors <unk> Templateization, lengthy CT, hallucination multiplicity <unk> Manual review of samples and justifications for rating <unk>

Target capability: eval answers "Are the capabilities really strong?" Base response event answers "Has the power hurt?" post-train readiness evaal answers "Is this base change still valuable through SFT/RL?"

### 6.3 Base regression eval

Base response is not about proving a stronger model, but about protecting the ability not to sacrifice. It should cover:

- Common knowledge: MMLU, MMLU-Pro, internal knowledge issues.
- Inference: BBC, ARC, GPQA, Logic.
- Mathematics: the internal questions of GSM8K, MATH, AIME style.
- Codes: HumanEval, MBPP, EvalPlus, repo-level integration, FIM, multi-file positioning.
- Multilingual: Chinese, English and target market languages.
- Generating quality: long-response, summary, interpretation, translation, natural dialogue.

Base mode does not necessarily follow complex formats, so the distinction is between "incompetence" and "insubordination". Each base event should record the minimal implementation, the new-shot policy, the answer extractor version and manual review rules. SWE-bench, the mission, the tool-use event mixes command compliance, tool protocol, environmental stability and scaffold quality, which is more appropriate as a target for rediness/diagnostic rather than a naked base.

Base report report report at least:

- The maximum capacity to retreat must not be sacrificed, not just the average.
- Low-screets and long tail language changes.
- Output style, rejection, length and hallucination samples.
- The conclusions of the fixed manual examination of the sample basket.

### 6.4 Target capability eval

Target capability event is to be separated from base restatement. It is not simply asking whether the public list is up, but whether the target power is stronger in real and private tasks.

Target capability, assessment method, necessary defense, and the most important part of the mission.
| --- | --- | --- |
<unk> Math/STEM <unk> Difficulty drums, verifiable answers, private variants, failed sample files, prevent competition problems from being repeated and synthetic overfit <unk>
<unk> Code/ FIM <unk> HumanEval/ MBPP/EvalPlus, FIM, repo-level commtion, multifile positioning <unk> SWE-bench/ tool-use as readess or diagnostic <unk>
<unk> Field competence Private issues, real files QA, specialist hand-made rubric <unk> Prevent area data from narrowing generic capabilities
<unk> Agent/ tool-use <unk> Fixed harness, environmental version, tool protocol, mission trajectory <unk> not misconstruing scaffold to base

If the target capacity is only increased in public benchmark and not supported by pravate hodout, failure sample sheets and manual review, it should be considered pollution, format fit or narrow distribution optimization.

### 6.5 Long-context eval

The long-term context assessment is three-tiered:

- Mechanical search: Needle-in-a-haystack, multiple needle, different locations and different noise density. It can only be diagnostic and should not enter the main gate.
- Real understanding: Long document QA, multi-section summaries, multi-evidence synthesis, conflict information judgement, long-form/log analysis.
- Mission accomplished: long code library modifications, multiple file bug positioning, comprehensive legal/fiscal/sert analysis, agent track retray and next decision-making.

Long context:

The axis shall be cut with the axis.
| --- | --- |
Context Length Bucket<unk> 4K, 16K, 32K, 64K, 128K; if target 1M, add 256K/1M
<unk> Job type <unk> Retrieval, abstract, multi-evidence QA, location of codes, cross-section reasoning, non-response of questions <unk>
Evidence density, thin facts, dense tables, long codes, conflicting evidence, and the evidence.
<unk> Interference with information <unk> non-disturbation, interference with subject matter, contradictory evidence, outdated information <unk>
<unk> Evidence location <unk> Beginning, middle, end, multiple locations <unk>
<unk> Output requirements Short answers, structured tables, long answers, citing evidence <unk>
Reverse Kernel, KV cache, China prefill, batting, serving configuration
Cost constraints, costs, costs of vomiting, storage, unit requests, costs, costs of unit use, costs of unit use, costs of equipment, and costs of equipment.
<unk> Short mission returns <unk> Short mission in long context if degraded <unk>

Hard date in the long context should not be viewed as only “wielding through the longest”. More reasonable thresholds are that short context capacity does not significantly deteriorate, long context real tasks are profitable, and the system of reasoning is acceptable at the target length of cost and delay.

### 6.6 Post-train readiness eval

Post-train readines with a paired protocol:

- pre-mid checkpoint and midcheckpoint use the same set of frozen post-train prepared protocol.
- Fixed data sequence,seed,budget,checkpoint section policy, reward/vereifier, harness, decoding and failure determination.
- When key conclusions are close to the threshold, more than seed or repeated run and report deviations or bootstrapped CI.
- No comparison after “best-training checkpoint”; comparison of results under fixed budget, fixed selection rules or reporting of training curves AUC.

The frozen SFT/RL recipipe is a diagnostic instrument used to compare pre-mid and midcheckpoint, which does not mean the final production of the past-train formulation. If you adjust the recipipe for better results, you should re-register the experition_id, which was not directly applicable to the original Mid-train conclusion.

♪ What are you looking at? ♪
| --- | --- | --- |
<unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk>
<unk> Final ability <unk> Target capability is retained after post-train <unk> base up, post-train disappears <unk>
<unk> Reward behavior <unk> RL reducing rewarding or raising a verifiable task <unk>
<unk> Security/style <unk> Denial of boundaries, Chinese expression, long-term quality of answers <unk> Safe return, templateization, denial of error
<unk> long context <unk> post-train long mission can continue to be used <unk> SFT long context ability is overwritten

Four-digit interpretation:

♪ And the results, and the explanations, and the decisions ♪
| --- | --- | --- |
♪ Base up, post-train up ♪
<unk> base up, post-train up, <unk> may be base evaal or post-train overlaying the proceeds <unk> back to data/eval, not directly zooming <unk>
<unk> base not up, post-train up and up <unk> may improve training or interact with SFT/RL <unk> Repeated seed and authentic task validation
♪ The power of the world is so great ♪

# 6.7 Scorrecard: How to read the results

Each candidate checkpoint should generate a page scorecard. It is Eval DR for gate, not replacing the final go/no-go decision of 4.6.

<unk> Fields <unk> Contents <unk>
| --- | --- |
<unk> checkpoint_id ' <unk> checkpoint hash, training steps, token numbers, contact Length <unk>
<unk> Target_capability_delta`<unk> primariy indicator changes, difficulty drum changes, private task changes <unk>
`base_repression_max_drawdown ' <unk> not at the expense of maximum ability to retreat and low barrel changes <unk>
<unk> usage and results of `private_holdout_result ' <unk> dev-private, sealed-private; financial-blind should maintain unused/reserved before Gate 5 or release, and record whether it has not yet been touched
<unk> long_text_resource`slong, real task, short mission return, serving configuration
`post_training_readines_result ' , paired protocol, seed, retention of proceeds, variance
`conception_status ' <unk> exact/near-duplicate/embeding/manual
<unk> Known_regressions `<unk> known degradation, failure sample, manual review findings <unk>
| `recommended_action` | kill / retry / extend / promote |

If the return on an indicator is exceptionally high and private tasks, manual reviews and adjacent eval are not supported, then contamination, formatting or completion should be assumed, rather than a breach of capability announced.

Gate meeting:

<unk> State <unk> Meaning <unk> Conference actions <unk>
| --- | --- | --- |
<unk> Green turget, guardrail, pravate holdout, pot-train readines supported in the same direction and complete evidence path
<unk> Yellow <unk> Gains but Differences, Evacuation, Pollution, Pot-Train retention or service costs are still unclear
Red <unk> not at the expense of capability overlaying, pollution/license unacknowledged, accident unattributed, post-post-train systemic variation <unk> rollback/kill, or reopening of the experiment_id <unk>

#7. Risk and accident management Runbook

Chapter 7 is not a failure mode, but an accident management in training Runbook: any anomaly must be able to fall into a symptom, an experimental ID, an affected checkpoint, a set of evidence paths and a continuing/rollback/kill decision.

# 7.0 How to use this chapter

Normal surveillance, val review and gate mechanisms are in chapter 4-6; this chapter only deals with anomalies. After triggering an anomaly, the duty DR freezes the site and then makes the first 30-minute diagnostic round and gives a provisional decision. Do not change data, change learning rates, change the eval senses or change the post-training schedule until the attribution is complete.

Three steps before the accident occurs, and no changes in configuration:

<unk> Steps, actions, outputs, etc.
| --- | --- | --- |
1. Freeze site
2. Decision level
System replay, data most diff, eval harm diff, model checkpoint diff root cause or unresolved tags in turn

Accidents are registered in six categories:

<unk> Accident type <unk> Typical range <unk>
| --- | --- |
<unk> Numerical <unk> Nan, Inf, Loss Explosion, Gradient, Mixed Precision Spill
<unk> data <unk> Data drum contamination, format drift, license problems, synthetic data templateation, sampling weight error <unk>
<unk> ifal <unk> harness, prompt, judge, metric, sampling or pollution
<unk> infra <unk> infe, GPU usage, NCCL, storage, checkpoint, serving configuration abnormal
The goal is not up, the universal is back, the guardrail is down, the long context is down.
<unk> post-train handoff <unk> SFT/RL relay loss, reward hooking increase, recipipe noise amplification

Hard rules: Any capability or training results must be preceded by four layers of isolation: system recall, data manifest diff, eval hares diff, model checkpoint diff; if a level is not involved in the accident, it should be marked `N/A ' and should state the reasons. When the evidence is not complete, only the non-accompanimental incident can be registered and not included in the capability conclusion.

#7.1 Accident classification: observation, alarm, block

<unk> Level, <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> ,
| --- | --- | --- | --- |
<unk> Observation individual event small fluctuations, drums loss slight deviation, single seed close to threshold log incident_id, rerun adjacent checkpoint or fixed sample baskets
<unk> Warnings Continuous checkpoint indicator anomaly, public/private disagreement, data drum loss, target capacity increase but targetrail is broken
<unk> Interruption of <unk> nN/Inf, resume incontinuous, contaminated or unclear, not at the expense of ability to cross the line, offline but not serviceable on the line

Principle of treatment:

Principles
| --- | --- |
<unk> Freeze site <unk> Keep checkpoint, optimizer state, training log, data manifest, eval raw outputs, system indicators and related committee <unk>
The stem, data, eval, model, pot-train recipipe, which layer has changed first.
♪ See the buckets first ♪ ♪ the whole world is lost ♪
We need to protect the guardrail before we lose the power threshold.
<unk> not making hidden fixes, changing filters, sampling weights, prompt, harness, judge, decoding or serving config must create new experition_id <unk>

#7.2 Accidents in training table

The accident type, the symptoms on the scene, the 30 minutes of initial examination, the gradation, the decision, the immediate decision, the stat.
| --- | --- | --- | --- | --- | --- |
<unk> numerical <unk> NN / Inf / loss Explosion Array Array Array Array, overflow count, LR/warmup, recent catch, optimizer state, resume log <unk> system: accuracy/kernel; data: bad samples; mdel: LR/clip; checkpoint: rasseme <unk> ; roll back to the recent health checkpoint, recheckpoint problem `checkpoint_id ', battid , catch id, overflow log, optimizer hash, replay results
<unk> numerical / model <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk>
<unk> infra <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk>
<unk> Data <unk> loss global bucket valuation loss, sampling night, tokenizer/packing, manifest diff, sample data priority; read tokenizer/packering and ebal bucket <unk> to freeze or delineate; rollback manifest <unk> baget id, manifest hash, sample sample, filter version, fix diff <unk> in serious cases
<unk> data/ capability <unk> Synthetic data templateing or error rate increasing <unk> paper/version, prompt, verifier, templace n-gram, response length, manual error rate <unk> data: generator; eval: sample too narrow; model: learning format instead of ability <unk> reducing synthetic ratio or isolation drums; not writing formatted benefit into reasoning gain <unk> generator config, version of verifier, repeat rate, manual review log <unk>
<unk> capability <unk> Early and significant retreat of general capabilities <unk> base correction max drawdown, low barrel, language/field fixed basket, data mix <unk> mdel: LR/ too long; data: excessive ad hoc; eval: sampling deviation <unk> trigger guardrail; rollback or decrease special ratio <unk> scorecard, failure sample, mix curve, rollback point
<unk> capability <unk> Target capacity increase but corrupt target indicator, non-sacrificial ability, adjacent checkpoint, change in type <unk> mdel/data trade-off; confirmed not to be an event caliber change <unk> promotion; extend <unk> Pareto curve, gardrail threshold, DRI signature, sample comparison <unk>
<unk> eval <unk> Data_hash, harness_committee, prompt/wrapper, judge, answers extraction, <unk> eval priority; old and old harness diff <unk> freeze capability conclusion with the same checkpoint; old/ new harness cross-run <unk> eval diff, raw outputs, judge version, metric change description <unk>
<unk> eval / data <unk> Public benchmark up but not up <unk> contamination report, private holdout, resemblance, raw output <unk> data contamination or eval preparation; also public too narrow to de-primariy indicator; cannot be scaled up <unk> contamination evidence, holdout use, de-sampling sample lists
<unk> capacitation / contact <unk> Needle <unk> good but real long tasks <unk> long task raw output, evidence location, information density, non-respondable sample, length distribution <unk> eval:needle too narrow; data: lack of integration/conflict tasks; system: addressing differences <unk> needle not be the main date; paused long training to expand <unk> long mission failure, evidence location, length barrel fractions, serving configuration <unk>
<unk> capability / context <unk> Long context training short-text training tasks <unk> length_legth_distrition, short-mission return, packing/pading, short sample ratio <unk> Data: long sample dilution; model: position/attitude adaptation side effects <unk> roll length mix or recovery ratio diff, short task scorrecard, curriculum version <unk>
<unk> infra/ context <unk> Short <unk> Serving contact context available but not wire priority <unk> serving contact, KV cache, chunked prefill, batting, Kernel, latency/ Cost <unk> system; model capability conclusion suspended <unk> system blocked; no release, no line failure recorded as model <unk> offline/online config diff, line raw output, profile <unk>
<unk> post-train handoff <unk> Post-train <unk> paired protocol, seed, SFT/ RL data version, checkpoint section, training curve AUC <unk> post-train
<unk> post-train handleoff <unk> reward hacking Add <unk> RL rw output, reward/verefier, rejection/ security, format dependency, CoT template <unk> post-train reward bug; mid-train may pre-crack format <unk> lower behavioral format data; re-rewd/vertier is reruned <unk> reward version, hacking sample, behaviour data ratio, repair records <unk>
<unk> infra <unk> Checkpoint resume uncontinuous <unk> resume <unk> resume resume <unk> <unk> checkpoint lineage, RNG/data cursor, checkpoint hash, training code version <unk> system/ checkpoint priority; data/ mode <unk> rollback; replay resume after the test has been excluded
<unk> Checkpoint conclusions repeatedly checkpoint, CI/angle, multiple seed, secaction policy, raw outputs evaal noise or error deviation; model real fluctuations need to be verified twice without single-point decision-making; report curves instead of optimals

# 7.3 Data accident runbook

The first principle of a data accident is a quarantine version, not a site fix. Any filter, generator, weight, tokenizer or packing changes must result in new data_version and manifest hash.

Step, step, move, step, step, step, step, step, step, step, step, step, step, step, step, step, step, step, step, step, step, step, step, step, step, step, step, step, step, step, step, step, step, step, step, step, step, step, step, step, step, step, step, step, step, step, step, step, step, step, step, step, step, step, step, step, step, step, step, step, step, step, step, step, step, step, step, step, step, step, step, step, step, step, step, step, step, step, step, step, step, step, step, step, step, step, step, step, step, step, step, step, step, step, step, step, step, step, step, step, step, step, step, step, step, step, step, step, step, step, step, step, step..
| --- | --- | --- |
1. Freezing of old manifest, sample weight, generator configuration, filter version and sample sample examples
2. Diff <unk> Comparison of token numbers, language/area/length distribution, repetition rates, pollution rates, bad sample rates <unk> Explanation of at least one abnormal drum <unk>
3. Isolation, delineation or de-barrel, retention of the universal security drum and gualar eval plating drums no longer enter further training
Retract. Retract. Retract with fixed checkpoint Data valuation and linked eval <unk> to prove that the fixation is from data instead of recalculation
5. Reciprocal <unk> Update data drum access cards and preparation_rule <unk> new data_version

If the contamination, license or privacy boundary cannot be explained, the data version should be killed directly. For mid-train, “possibly contaminated but good scores” is not an acceptable state.

# 7.4 Training accident runbook

Training accidents are a priority for the protection of resilience. When you find problems in the Numerical or resume category, do not make the learning rate a bit easier; checkpoint, optimizer, RNG, data cursor and code version are available.

Step, step, move, step, step, step, step, step, step, step, step, step, step, step, step, step, step, step, step, step, step, step, step, step, step, step, step, step, step, step, step, step, step, step, step, step, step, step, step, step, step, step, step, step, step, step, step, step, step, step, step, step, step, step, step, step, step, step, step, step, step, step, step, step, step, step, step, step, step, step, step, step, step, step, step, step, step, step, step, step, step, step, step, step, step, step, step, step, step, step, step, step, step, step, step, step, step, step, step, step, step, step, step, step, step, step, step, step, step, step, step, step, step..
| --- | --- | --- |
1. Stop Table <unk> mark incident_id, freeze current run, no longer write capability conclusions <unk> field log and state complete <unk>
<unk> 2. Replay <unk> Rewinding short window from recent healthy checkpoint to confirm whether re-recoverable <unk> Re-record and unrecording are possible to position <unk> record system uncertainties
<unk> Single variable repair <unk> Only one variable at a time: LR, clip, precision, bad catch, resume one of the logic <unk> Repair and indicator changes attributable <unk>
<unk> 4. Returning <unk> to loss, base restatement and key trageval<unk> without adding guardrail accident
5. Decision-making path for DRI signature and evidence

The minimum conditions for continuing the training are: numerical stability, system replay success, data undisappeared, and eval harms. None can be left but retry or rollback.

# 7.5 Assessment of accidents

The most common error in assessing accidents is to treat tool changes as a change of capability. Neither old nor new fractions can be directly compared to each change in the profile, wrapper, judge, answer extractor, decoding, sample set or metric.

<unk> Check matrix <unk> Old checkpoint <unk> New checkpoint <unk>
| --- | --- | --- |
♪ The old harness ♪
New harness, new tool caliber changes, new caliber results.

Only when the "old hares are new checkpoints" and "old checkpoints are not equally good" are established, the proceeds are initially attributed to the model. If private holdout is repeatedly viewed or transferred, it should be downgraded to dev-private and recreated as saaled-private or final-blind.

# 7.6 Post-train relay accident

If the proceeds of Mid-train disappear after the post-train, do not simply determine that the Mid-train is invalid. Four things need to be checked simultaneously:

<unk> Check item <unk> Possible problems <unk>
| --- | --- | --- |
<unk> recipe Whether SFT/RL Data, Seed, Budget, reward/version Change
<unk> Seletion is not different
<unk> Whether the ability is overridden by SFT style data, RL incentives are biased towards short answers or formats
<unk> Whether the proceeds are false positive <unk> base event pollution, public collusiveness, too narrow sample return to chapter 6 eval recovery and 7.5 <unk>

If the post-train relay fails under the paired protocol two consecutive rounds and the base end proceeds are only available in public benchmark or a single seed, it should kill the Mid-train direction; if the base end returns are stable but covered by SFT/RL, write the conclusion as “post-train Handoff is not reached” and do not write as “mid-train is not.”.When adjusting SFT/RL data, reward, verifier, budget or seed for the purpose of checking the coverage, the old papered protocol conclusions cannot continue as mid-train return evidence but as a diagnostic trail.

#7.7 Accident Remix Template

Each alarm or stop-level incident is recorded in a disk. The disk is not a recrimination document, but a way to keep the next training less from stepping on the same pit.

```text
incident_id:
experiment_id:
incident_type: numerical | data | eval | infra | capability | post-train handoff
severity: observation | alert | blocker
first_detected_at:
affected_checkpoint:
symptom:
root_cause: confirmed | suspected | unresolved
changed_variables:
rollback_point:
evidence_paths:
four_layer_isolation:
  system_replay:
  data_manifest_diff:
  eval_harness_diff:
  model_checkpoint_diff:
decision: kill | retry | rollback | extend | promote | unresolved
prevention_rule:
owner:
reviewed_by:
```

If `root_cause ' is still `unresolved ' , the accident can close the training action but cannot close the cognitive conclusion: only “not attributable to the accident, isolated” can be written in the document, and not “degradation of model capacity” or “a data drum is valid”.

# 8. 90 Days Road Map for the new team

This road map is a reference rhythm, not a calendar commitment. The next stage is for Gate 0-5 to decide, not for days.

#8.0 Gate dashboard: Only one decision-making question per phase

The 90-day road map is not intended to be a schedule, but to move the project from “want to train” to “evidence enough to train”. Each gate answers only one question:

<unk> Gate <unk> Decision making issues <unk> Evidence <unk> Blocker <unk> Owner <unk> Next action <unk>
| --- | --- | --- | --- | --- | --- |
<unk> Gate 0 <unk> Whether this target really needs mid-train charter, no-sacrificial capacity, v1 eval recovery, v1 post-train programmed protocol <unk> , is the target to be solved by SFT/RAG/ product logic; eval or holdout <unk> Model Lead go/ no-go charter <unk>
<unk> Gate 1 <unk> Data access experiment <unk> data manifest/ash, license, pollution inspection, sample review, linked eval <unk> Data source unknown, synthetic generator read eval, Holdout leak <unk> Data DRI data read memo
<unk> Gate 2<unk> proxy implementation Whether the bad direction is excluded <unk> Target return, two scale or target short-range signals, failed sample <unk> Only public benchmark ups; synthetic data templateing; proxy conclusions are unstable <unk> Eval DRI<unk> adactation memo
<unk> Gate 3 <unk> Whether the master model shortness is worth continuing <unk> checkpoint curves, drums loss, scorecard, accident records, Paretto results <unk> NaN/loss spice, non-continuity, guardrail overline, long context short tasks <unk> Training Infra DRI extend/ rollback/ kill
<unk> Gate 4 <unk> Whether the proceeds can be retained by the post-training paired SFT/RL results, Seed, AUC, raw outputs, reward/ Safety returns <unk> base but post-train disappears; recipe change; reward hacking increases <unk> Post-train DRI <unk> readreport
<unk> Gate 5 <unk> Whether to enter magnification training or to redo it with a contraction

As long as a gate evidence is incomplete, do not go around with "see again." Mid-train projects are costly, and real rhythm control comes from gate, not the calendar.

Each gaste dashboard record must also contain `status ', `owner ', `evidence_path ', `version_hash ', `stale_after ' and `text_action ' . Green status without an evident path should be considered yellow.

## 0-14 days: defining objectives and assessment

The decision-making session at this stage will answer only one question: whether this goal really needs Mid-training.

Delivery:

- Mid-train charter: Target capability, no sacrifice, target checkpoint, budget.
- Eval matrix: base event, capacity event, long context event, post-train rediness.
- Data cylinder design document.
- Risk list and go/no-go date.
- Frozen post-train recipe: SFT/RL data version, training budget, Seed, Harness, assessment set and failure determination.

Go/no-go：

- If the event freeze, private holdout and post-training relay recipe does not freeze, does not enter training.
- private holdout is not allowed if created later than training data mix, or if private holdout is allowed to be called.

## 15-35 days: data and small models

The corresponding Gate 1-2 is charged primarily with Data DRI and Eval DRI; all experiments must be registered with the test counter account of 4.6.

Delivery:

- For example, the data mix experiment on 1B/3B/7B proxy model; specifically scale is determined by the existing model spectrometry and budget of the team.
- Learning rate and token Budget Sweden.
- Synthesis of data accuracy and diversity reports.
- loss and capacity association analysis for each data drum.
- Data manifest/ash, near-duplicate detection reports, pollution inspection reports, manual sample tests.

Go/no-go：

- At least one mic is upgraded to target capacity and generic capability retreats are acceptable.
- Synthesis data do not contain significant contamination and collapse of style.
- Proxy success only indicates that bad direction is excluded and does not prove that target scale is certain to be established; at least two scale are required to match direction before entering the main model short course, or that the target model short run validates key signals.

# 36-60 days: primary model short-range Mid-training

Recognise Gate 3, with the primary responsibility for trading in infra DR, Eval DR and Model Lead; this phase must be defined before training starts.

Delivery:

- Master model short-range training, such as 10B-100B token level windows; specific token Budget is determined by Gate 2 evidence and training costs.
- Checkpoint daily.
- Capability/forgotten Parato curve.
- Candidate checkpoint selection.
- Training runbook, checkpoint lineage, resume records, training code code, accident records.

Go/no-go：

- Targeting capacity enhancement is not a single benchmark driver.
- The decline in common capabilities is below the predefined threshold.
- no apparent style drifting in the generation of samples.
- triggers a stop or rollback when a Nan appears, lose frame, gradient abnormal, vomit abnormal, a data drum loss abnormal, checkpoint resume is not continuous, or long context training for short injury tasks.

## 61-75 days: post-train relay verified

Corresponds to Gate 4, which is primarily attributed to Post-train DR and Eval DR; if the post-train recipe changes at this stage, the mid-train conclusion shall be considered invalid or remarked as experimental ID.

Delivery:

- Fixed SFT comparison.
- Fixed RL/RLVR comparison, if applicable.
- Post-post-train real mission assessment.
- rewardbacking / safety / style returns.
- Post-train readiness report: recipe version, seed, budget, harness, failure determination and retention ratio of proceeds.

Go/no-go：

- Mid-trained checkpoint retains the proceeds after the post-train.
- The difficulty of alignment has not increased significantly.

# 76-90 days: zooming in or shrinking decision making

Reverses Gate 5, with primary responsibility for Decision owner, Model Leader and Release owner; this stage is not automatic enlargement, but rather a decision to continue, shrink, redraw data or stop.

Delivery:

- Zoom in on candidates recipipe or retrench next stage.
- Whether to enter decision making for 100B-1T+token training.
- Automated inventory of improvements in data and assessment.
- A plan for the next phase of the long-term context or second capacity objective.
- Model review: checkpoint lineage, data management, eval raw outputs, training logs, permissions, retention cycles and rollback checkpoints.

Go/no-go：

- if the proceeds are derived mainly from pollution, narrow assessment or post-train accident, not magnified.
- if the benefits are stable, understandable, retained after the post-training, entering the main training.

#9. Executable checklist

##9.0 Minimum Delivery Pack and Delivery Index

If the team does not want to maintain the complete document system from the start, it must have at least eight deliverables below. Without any one, it is difficult to rewrite the middle-train conclusion.

♪ What meeting is the time when the ♪
| --- | --- | --- | --- | --- |
Mid-train charter <unk> Model Leader <unk> 8.0 <unk> Gate 0 <unk> Start-up session, go/no-go
<unk> Data many times <unk> Data Data <unk> Data <unk> DRI 4.2.1 / 9.1 <unk> Gate 1 <unk> Data readines, accident redisk
<unk> Eval review<unk> Eval DRI<unk> 6.1/9.3 <unk> Gate 0-1 <unk> ifal freeze, checkpoint review
Training runbook <unk> Training Infra DRI <unk> 4.3.1 / 5/ 7.4 <unk> Gate 3 <unk> Train Launch Conference, Accident Management
<unk> Experiment ledger <unk> Model Lead / PM <unk> 4.6 <unk> Gate 0
<unk> Checkpoint screencard <unk> Eval DRI <unk> 6.7 <unk> Gate 3-5 <unk> checkpoint review, zoom in on decision-making
Post-train readines report
Incident review <unk> accidents owner <unk> 7.7 <unk> alarm/ interruption incident <unk> accident rev, response review <unk>
Go/no-go memo <unk> Decision owner <unk> 8.0 / 9.4 <unk> Gate 5 <unk> Zoom, shrink or Stop Decision-Making

The Checklist function is to take over these deliveries, not to create process burdens. For the new team, it is more important to get the minimum delivery out of the bag than to pursue the perfect platform.

Each checklist entry should not be just ticked, but also be tied to the minimum audit field:

```text
owner:
evidence_path:
version_hash:
stale_after:
gate_role: primary | guardrail | diagnostic
status: green | yellow | red
```

If an inspection does not have `evidence_path ' or `version_hash ' it can count only as yellow, not as gate passing evidence.

#9.1 Data checklist

- [ ] Data manyest/ash, recording of source snapshot, processing committee, tokenizer, edup, communication, sampling night, shuffle seen.
- [ ] Each data source has a record of compliance.
- [ ] Each data drum has a quality score and manual sample review.
- [ ] Each data drum is tied Linked_eval_id, unbound drums of the event do not increase sampling weight.
- [ ] benchmark verification check complete.
- [ ] Training set, validation set, private holdout separation.
- [ ] Synthetic data records techer/version, prompt, sampling parameters, verifier, filter rules, rejection ratio, template repetition rate, manual error rate.
- [ ] Synthetic data have correct filtering, diversity, templateing and style intropy checks.
- [ ] Long context data contains real long tasks, not just collating text.
- [ ] Generic data retention ratio is supported by ablation.

# 9.2 Training checklist

- Base checkpoint event complete.
- [ ] Tokenizer / special tokens has good reason to freeze or change.
- [ ] Optimizer state clear succession strategy.
- [ ] LR schedule, warmup, peak/min LR, decayshape, gradient clipping, precision.
[ ] global catch, microbatch, packing/masking, data order, shuffle seen.
- [ ] checkpoint section policy freezes before training.
- [ ] There is a checkpoint saving policy at every stage.
- [ ] Plumbing value loss observable.
- [ ] MoE/attention/long-content system indicators are observable.
- [ ] Training can recreate, checkpoint can be repeated.

#9.3 Evaluation checklist

- [ ] Eval freeze has been frozen and includes eval_id, eval_family, data_hash, harness_committee, prompt_or_wrapper_version, metric, decision_rolle, threshold_or_guardrail, raw_output_path.
- [ ] Base event, capacity, long context, segment.
- [ ] Each event indicates that the target for prism, guardrail or diagnostic, prismary is not more than 3-5.
- [ ] Indicators include real tasks and manual reviews.
- [ ] See not only averages, but also the ability to retreat.
- [ ] Each candidate checkpoint generates scorecard, with target capacity delta, maximum retreat, contamination state, failure sample and recommended action.
- [ ] Every candidate checkpoint does the same thing.
- [ ] Private holdout is divided into dev-private, sealed-private, final-blind, created earlier than training data to freeze and not directed at secured/final.
- [ ] Long context eval coverage length, location, information density, mission type and deployment consistency.
[ ] Post-training relay fixes and records data sequences,seed,harness,budget,checkpointlinkaction policy and failure determinations.
- [ ] Post-Post-training gains may be recovered.

#9.4 Division checklist

- [ ] Data teams, training teams, Post-train DR share the same experimental accounts.
- [ ] Each experimental recording of data from the Mix, LR, token Budget, Context Length, eval.
- [ ] Research, Data, Training, Eval, Post-Train, Release owner are all identified.
- [ ] Model Lead, Data DRI, Trading Infra DRI, Eval DRI, Post-train DRI, Safety/Complature DRI, Project/Domain DRI, Decision owner.
[ ] Mid-train charter, Data manifest/ash, eval registry, runbook, checkpoint ledger, pot-train readines report, go/no-go memo owned.
- [ ] Freezing of “non-sacrificial capacity” and rollback conditions for all phases before the project starts.
- [ ] The threshold, blockage and signatory for each date have been written in the Gate memo prior to the experiment.
- [ ] Any intermediate change of mix, filter, or version of the eval will create a new version of interpretation_id.
- [ ] There are stop conditions in training.
- [ ] Must pass go/no-go date before amplifying training.
- [ ] reserve complete reports of pre-mid, mid, pot types of checkpoint prior to publication.

#10 Special reminder to the team of model models with post-training experience

First, do not use the SFT mind to do Mid-train. Mid-train data can contain QA, CoT, code tasks, but it is not aimed at modeling the formatting of the product, but at changing the distribution of capabilities.

Second, don't let RL take all the blame. If base model does not have enough math, code, context and self-correction substrate, RL probably only learns surface search or lengthy reasoning.

Third, not just follow. Mid-train’s real benefits are built in both private and real-product tasks and post-train relays.

Fourth, do not start with a 1M contact. For most teams, it is more practical to make 32K/128K reliable than to display a very long context.

Fifth, don't ignore the data project. In Mid-training, training codes are often not bottlenecks, as are data lines, pollution control, drums and experimental discipline.

#11 First round of search space: example search grids, not directly as default mix

This chapter is a work example, not a formula. It is designed to help the mid-train team to put data, training, evaluation and post-train relays into a minimum evidence chain.

If the team already has a base model and a stable post-training pipeline, it is recommended that the first round be not large and complete, starting with a minimum closed loop for the "competent mid-train + post-train relay". The following scale is not recommended as a reference, but as a search space for starting ablation; different model sizes, pre-training history, target language and product tasks will significantly change the best mix, and the main training must be validated by proxy scale and short-range master models.

The minimum closed loop here is not the minimum training formula, but the lowest possible experimental cost to verify whether data, training, evaluation and the post-training relay can be used to reach an interpretable conclusion. The following ratios and token compartments are used only for designing the ablation variable and cannot be used as default metix, default LR or default budget.

The following area can only be used as a value variable if the base checkpoint, target capacity, no-sacrificial capability, val duty, data manifest and post-train pretocol have been frozen; otherwise, the training configuration should not be included.

Objectives:

- Raise math, code, STEM and complex QA.
- Not to cause significant harm to common, multilingual, factual and natural origin.
- Verify whether there are still benefits after SFT/RL.

Data mix search space (bucket sensitity sweep axis):

- High-quality generic text: testing the bottom line of the truth with low/medium/high points, e.g. 30/50/70, not fixed ratio recommendations.
- Codes and FIM: test code capabilities and general generation drift at low/medium/high points, e.g. 10/20/30.
- Mathematics/STEM: Injecting the benefits, saturation points and generic retreats with low/medium/high test reasoning.
- Synthetic/verifiable reasoning: test the quality of the verefier with a cap sweep, template and bug magnification of the teacher.
- QA/CoT/Text Task Format: drifting in separate or low-scale test format to avoid pre-fixing of the post-train behavioural format.

These bucket axes are used only for the first round of single or small variables search, not for the unimodal scale table to be met simultaneously. Actual mex must be determined by small models and short-range master model experiments.

This starting point is not a complex formula for OLMO 2, Qwen3, Llama 3 or Phi-4, nor is it the optimal percentage to be rolled out from public reports. It is a search grid that allows new teams to expose data conflicts, forget risks and synthetic data boundaries.

The main training must be preceded by a mix of representation curve, not just one that looks the best.

- What are the first steps to retreat when the ratio of common data declines?
- Are the benefits linear, saturated or reversed when the ratio of mathematics/STEM or code increases?
- Does the repetition rate of private tasks, style reviews and templates deteriorate in tandem with the increase in Synthetic ratio?
- Is the same six in the same direction on different seed or adjacent checkpoint?
- Is the targeted capacity gain sufficient to compensate for the cost of generic evacuation and training?

Do not run just one cross in the first round. Better to keep a control mix and then make a small matrix around a single variable:

The cynics, the mutants, the cynics, the cynics, the chords, the chords, the chords, the chords, the chords, the chords, the chords, the chords, the chords, the chords, the chords, the chords, the chords, the chords, the chords, the chords, the chords, the chords, the chords, the chords, the chords, the chores, the tres, the tremen, the tremen, the twes, the treaches, the treache, the tremen, the tremen, the tremen, the t the t, the t the tres, the tres, the t the ts, the t the t the t the t the t the t the t the t the t the t the t the t the t the t the t the t the t the t the t the t the t the t the t the t the t the t the t the t the t the t the t the t the t the t the t the t the t the t the t the t the t the t the t the t the t the t the t the t the t the t the t the t the t the
| --- | --- | --- | --- |
<unk> Control <unk> Mix <unk> LR, token Budget, Context Length <unk> to create a return line
Math/STEM up <unk> only raises the cost of mathematics/STEM code, common, LR constant <unk>
<unk> Code/ FIM up <unk> only improves code/FIM mathematics, common, LR constant <unk> judgement code ability and general generation drift <unk>
<unk> Synthetic cap <unk> Limit synthetic cap <unk> Other drums remain constant <unk>
<unk> General retain <unk> Improve high quality generic data <unk> Target drums remain constant <unk>
LR lower <unk> Data mix constant <unk> Distinguishing data problems and optimization

Each variant can be modified only by one or two main variables. The training and the modification of the mix, filter, LR or eval versions will make the experiment impossible to explain.

Validate starting point by using the main model short-range after Gate 2:

- Continuing training with low learning rates.
- Use the original context Length or a small extension.
- 10B-50B tokens class master model validation cap examples; actual budget must be determined by proxy results, target model short-range signals, forget threshold and cost.
- every 10-20% token save checkpoint and eval.

Assessment starting point:

- Base eval: MMLU/MMLU-Pro, BBH, GPQA, GSM8K/MATH, HumanEval/MBPP, Multilingual Collection.
- Private: Internal math, code, complex QA, real user tasks.
- Post-train rediness: Fixed SFT recipe, pre-mid and midcheckpoint.

If this ring does not have a steady return, do not rush to expand token Budget. Go back to data and learning rates.

12. Information map

This chapter is not an endnote to the literature summary, but a road map for readers to review the conclusions of this paper. It is suggested that the team read the information into three categories: first, a first-hand report confirming the factual boundary, then a second, a reading of the synthesis creating a taxony, and finally a reading of the controlled experiment forming an internal assumption.

#12.1 One-hand technical report: Fact base

<unk> Information <unk> Original text to be verified as a priority <unk> How to use this text <unk> Can't launch anything <unk>
| --- | --- | --- | --- |
| OLMo 2 Technical Report: <https://arxiv.org/abs/2501.00656> <unk> The report explicitly uses mid-training stratification and discloses open paradigms for data mixing, mid-training, pot-training and open works > > > > > > > > > > > > > ; learning phase naming, data lineage and transparent laboratory accounts <unk> cannot launch OLMo2 data ratios appropriate for Chinese, multi-language, agenic code or closed source product models <unk>
| Qwen3 Technical Report: <https://arxiv.org/abs/2505.09388> > > three stages pre-training: generic knowledge, STEM/code/resumption enhancement, long context; and extrapolation/deployment technology
| DeepSeek-V3 Technical Report: <https://arxiv.org/abs/2412.19437> 14.8 T token pre-training, 32 K/128K contact interpretation, and MLA/MoE/ MTP structures and training synergies
| Phi-4 Technical Report: <https://arxiv.org/abs/2412.08905> synthetic data for pretrating and midtraining; 4K-> 16K extensions in midtraining about 250B tokens <unk> to show that synthetic data can be the core of training strategies, while reminding the visible midtraining that primary responsibility for context extension <unk> phi-4 cannot be simplified to "reasoning Mid-train only by synthesizing CoT" > > 16K extensions to > > > > > > > > > > <unk> tkmens <unk> > > > > > > > > > > > > > > > > > > > > > > > > > <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk>
| Qwen2.5-1M Technical Report: <https://arxiv.org/abs/2501.15383> Progressive long-context pre-training to 256K, long context post-training, DCA/YaRN extrapolation, distraction and chunced prefilling deployment > > > purge long-text pre-training > punctuation long-term forward-context pre-training > punctuation training extension, 1M extrapolation and deployment optimal boundaries > m context cannot be written as "direct Mid-train to 1M" > > > > > > > > > > > > > > > > > > <unk> > > > > > > <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk>
| The Llama 3 Herd of Models: <https://arxiv.org/abs/2407.21783> 405B iniative pre-training about 15.6 T tokens; long-content pre-training about 800 B tokens to 128K; last 40M tokens annealing <unk> conservative reference: reduced pre-training, long-context and annealing to be decomposable

##12.2 Overview and controlled empirical studies: hypothetical sources

<unk> Information <unk> Main use <unk> Use of borders <unk>
| --- | --- | --- |
| Mid-Training of Large Language Models: A Survey: <https://arxiv.org/abs/2510.06826> Create mid-training data entry, task type and synthesis is a secondary one and cannot replace the factual verification of the original report
| A Survey on LLM Mid-training: <https://arxiv.org/abs/2510.23081> <unk> Comparison of different Mid-training objectives, data patterns and evaluation caliber <unk> taxonomy can be drawn upon, specific formulations still need to be tested internally
| PRISM: Demystifying Retention and Interaction in Mid-Training: <https://arxiv.org/abs/2603.17074> <unk> Design retenion / intervention / capability transfer control
| On the Interplay of Pre-Training, Mid-Training, and RL on Reasoning Language Models: <https://arxiv.org/abs/2512.07783> <unk> Establishment of an experimental hypothesis as to whether RL relies on the pre/mid stage capability boundary <unk> reading/RL conclusions are particularly conservative and require verification of the <unk> by team itself RLVR/SFT painted protocol

### 12.3 Claim / source matrix

<unk> Claim <unk> Body position <unk> most supportive <unk> support strength <unk> suggested language <unk>
| --- | --- | --- | --- | --- |
<unk> mid-training can independently manage <unk> 0/ 1/ 3.1/ 4.6 <unk> OLMo 2 for the express use of mid-training; Phi-4 uses pretraining/midtraining/post-training stratification; <unk> report facts + project synthesis; <unk> “The public report already contains a sample of the mid-training independence phase; the team can draw on its governance.”
<unk> Many cases are just mid-train-like <unk> 0/ 2/3 <unk> Qwen3, DeepSeek-V3, Llama 3, Qwen2.5-1M The original reporting terminology is strong: The report's facts: <unk> “This paper is similar in the sense of the project and does not rewrite the original reporting terminology.” <unk>
<unk> wen3 has General / Reasoning / Long Context three pre-training stop <unk> 3.2 / 12.1 <unk> Qwen3 Technical Report <unk> : report the facts
<unk> DeepSeek-V3 long-term context extension of the last two paragraphs of 14.8 T base pre-training 1000 steps <unk> 3.3 / 12.1 <unk> DeepSeek-V3 Technical Report <unk> : report the fact that “support phase conversion; do not support reverse generic data mix.” <unk>
<unk> wen2.5-1M 1M capability from training, post-training, extrapolation and deployment of co-ordinated <unk> 3.5 / 12.1 <unk> Qwen2.5-1M Technical Report <unk> : report facts + Project Summary <unk> “not directly trained to 1M, nor is it purely a matter of reasoning.”
Long-content and annealing of Llama 3 can be used as a reference for late-staying 3.6/ 12.1 <unk> Llama 3 Technical Report <unk> Report facts <unk> “405B size sample, not small team budget proposal.”
<unk> Synthetic data are valuable, but must be addressed for templateization, pollution and teacher errors <unk> 3.4/ 4.2.2 / 12.1 <unk> Phi-4, Qwen3 and controlled studies related to synthetic data <unk> Strong: report facts + thesis summed up <unk> "Synthesizing data is a verifiable ability amplifier and not a low-cost token alternative."
Reisoning Mid-training is more like raising the engineering hypothesis for RL substrate <unk> 2.4/ 3.7/ 6.6 <unk> PRISM, pre/mid/RL interplay paper <unk> Summary of the paper + To be authenticated assumption <unk> “need to be verified with team own paired RL/ SFT protocol.”
<unk> Public benchmark rise is not sufficient to prove the success of the Mid-train evaluation practice of multiple public reports + in this document project management <unk> : Project summary <unk> "It is necessary to look at private holdout, raw output, pollution and post-train rediness."
Public reports usually cannot give replicable recipe<unk> 4/ 11/12 <unk> a single-hand report that together reflects the incompleteness of key details in the public report: Project summary: <unk> “The table in this paper is a search of space and quality doors, not a re-engineer formula.” <unk>

#12.4 Recommended reading order

1. Read OLMo 2: understand how documents, data, checkpoint and post-training are stratified when mid-training is an independent phase.
Reread Qwen3: Understanding the phase design of "General-> Capacity Enhancement-> Long Context", noting that the original report used pre-training tables.
3. Reread DeepSeek-V3 and Qwen2.5-1M: Understanding that long context extension cannot be separated from architecture, extrapolation and serviceing systems.
4. Reread Phi-4: understand the value and boundaries of synthetic data, especially not to simplify synthetic-heavy strategy into a single reading Mid-training.
5. Read Llama 3: Understanding conservative routes of conservative pre-training, long-content pre-training and annealing.
6. Final reading of the papers on survey, PRISM and pre/mid/RL: transforming the institutional assumptions into ablation of the team itself, rather than directly writing the findings of the papers into training decisions.

# 13. Go/no-go memo Minimum Template

For specific start-up actions see 0.2, for the deliverable index see 9.0. Only one decision template is retained at the end of the text: each go/no-go must be able to track the evidence path, version and owner.

```text
decision_id:
gate:
status: green | yellow | red
decision: go | no-go | retry | rollback | kill
target_capability:
non_regression_guardrails:
evidence_paths:
version_hash:
stale_after:
data_manifest_hash:
eval_registry_version:
post_train_protocol_version:
checkpoint_or_run_id:
known_risks:
owner:
signoff:
reviewed_by:
next_action:
```

A mature Mid-training project does not start as “training runs” but can answer before the first checkpoint comes out: what the target is, what it cannot sacrifice, where the evidence is, who will determine whether it continues or ceases.

# Appendix A: Proceedings of the absorption of comments from the review

Following the technical experts ' s puncture, the author has made the following revisions:

- Add a qualification to the abstract and terminology boundary: OLMo 2 is a narrow mid-training sample, Qwen3, DeepSeek-V3, Llama 3, Qwen2.5-1M, etc., which is classified as mid-train-like only in the context of the project.
- Qwen2.5-1M: to distinguish long-content pre-training, pot-training and inference/disposition; to clarify 1M support mainly from extrapolation and reasoning systems such as DCA/YaRN, without making a misdirectional mid-train data formulation.
- Amendment of Phi-4: to synthetic-heavy trading strategy case, no longer written as clean enough mid-train formulation.
- Reduction of the intensity of the statement of reasoning/RL: change to a strong engineering assumption and emphasis on edge-of-competence, reward design and exploration budget.
- Change the ratio of data and token Budget from the Recommended Formula to the `first round of search space'.
- Adjust SWE-bench position: more suitable for cross-referenced harm, lightweight instruction grinding or post-train rediness.

After editing the puncture, the author has made the following revisions:

- Add a reader decision tree after the summary, so that the team can judge whether it should be the case, the case, the case, the case, the case, the case, the case, the case, the case, the case, the case, the case, the case, the case, the case, the case, the case, the case, the case, the case, the case, the case, the case, the case, the case, the case, the case, the case, the case, the case, the case, the case, the case, the case, the case.
- Replace the words “consensus for the last two years” with the words “public evidence is weak and weak”, distinguishing between technical reports, synthesis/controlled experiments and interviews/blogs.
- Adding the first round of ablation design table to move the articles from an overview to an implementable project plan.
- Supplement 10 differences in the team of model models with post-training experience.
- Dismantling of information maps into one-hand technical reports, syntheses and controlled empirical studies.

In the first time-span, the author absorbed the technical and editorial reviews and made the following revisions:

- Add a new section 0.2: How to start the first day, compress the startup action into DRI, charter, eval registry, post-train recipe, laboratory counter and date memo.
- Replace section 4.6 with “Organisation operating mechanisms: roles, accounts and quality doors”, complementing the DRI tables, experimental accounts, schema, Gate 0-5 quality doors and meeting rhythms.
- Change the 90-day road map to a phase-door drive, emphasizing that the calendar is a reference and that the next stage is determined by data readiness, training stability, eval stability and the post-training relay validation.
- Supplementing the boundary of the proxy application: Proxy can only exclude the bad direction and cannot prove that the target scale is certain.
- Upgrade organization checklist, add date memo, signatory, change_id change rules and model review.

In the second time frame, the author incorporated the following revisions after the technical and editorial reviews:

- Change chapter 6 from the benchmark list to the Eval Reference note, emphasizing that the result of not entering registry cannot be used as a basis for go/no-go.
- Add an additional eval registry schema, which covers the paragraphs on eval_id, Data_hash, Harness_committee, prompt/wrapper, decoding, metric, threshold, raw output.
- Dismantling private holdout into dev-private, sealed-private, financial-blind, avoiding repeated team involvement in the “private collection”.
- Split base restatement, target capability, long-content, post-train readines and safety/style event, with clear uses and failed signals.
- Supplemented by a signed post-training record request for a freeze on the seed, budget, budget, reviewpoint section policy, reward/verefier, harness, decoding and failure.
- Add a new checkpoint template requiring simultaneous reporting of target capacity delta, maximum retreat, contamination status, failure examples and recommended actions.

In the third time frame, the author incorporated the following revisions after the technical and editorial reviews:

- Supplementing the data drum access card in section 4.2, requiring the words data most/ash, tokenizer, sampling night, shuffle seen, linked_eval_id for each data version.
- Supplementing the boundaries of use of synthetic data in section 4.2.2 by requiring records of sampling parameters, filter rules, template repetition rates, manual error rates and whether to read eval.
- Supplementary training button freezes in Section 4.3.1 including pak/min LR, decay shamp, gradient clipping, precision, global catch, microbatch, data order and checkpoint section section policy.
- Supplements the length distribution of curriculum in section 4.5 to avoid recording only the maximum context length.
- Reduce the temperature of the 4.4 array table to " Example of Search Variables " and add the requirement for the metix notification curve in chapter 11.
- Synchronize data upgrades and training checklist, emphasizing that data, filters, generators, training formulations and checkpoint selections must be re-emerging.

In the fourth time frame, the author ' s technical and editorial review was followed by the following revisions:

- Replace chapter 7 with “Runbook for risk and accident management”, making it clear that this chapter deals only with training anomalies and does not duplicate normal gate, surveillance and event recovery.
- New types of accidents and classification of accidents covering the six categories of accidents in Numerical, Data, eval, infra, capability, post-train Handoff, and observation, alarm, disruption of third-level treatment.
- Supplementing the hard rule of “four-storey isolation”: the inability to include the ability conclusion cannot be included in the lack of evidence.
- Upgrading training incident table to field symptoms, 30 minutes of initial screening, tiered attribution, immediate decision-making and a runbook that must be kept in reserve.
- Additional specialized processing processes for data accidents, training accidents, assessment of accidents and post-train relay accidents.
- Adding an accident redisk template requiring records of events_id, events_id, affected_checkpoint, changed_variables, events_paths, declaration and reservation_rule.

In the fifth time frame, the author ' s technical and editorial review was followed by the following revisions:

- Add a new evidence label to chapter 2, distinguishing between the facts of the report, the syntheses, the project syntheses and the assumptions to be validated.
- Replace the table in section 2.1 with “direct support for public reporting” and “work analogy” and avoid mixing the original reporting terms with the author.
- A narrow phrase “generally improved quality data for open cases”, clarifying that DeepSeek-V3 is primarily supportive of phasing context comparisons and does not directly support the conclusion of data matching.
- Fact-checking of the OLMO 2, Qwen3, DeepSeek-V3, Phi-4, Qwen2.5-1M, Llama 3 cases, adding the original terminology, token/content/stage, which limits and cannot be extrapolated.
- Upgrading chapter 12 from the reference sheet to a map of information, adding a hand-held reporting table of uses, a summary/controlled experimental boundary table and a claim / source matrix.
- In the summary and in the supplementary column for chapter 11, it is clear that the data ratio, token Budget, 90-day road map and quality door are the initial recommendations and not the general conclusions given directly in the public paper.

In the sixth time frame, the author ' s technical and editorial review was followed by the following revisions:

- Add a new “use of navigation” at the beginning of the text, which pre-empts reading paths for start-up sessions, data experiments, training accidents and data verification.
- Amendment of Section 0.2 caliber Day-1: freeze on first day of business/schema, v1 exal recovery and post-training pre-training.
- Adjust the mid-train/ post-train presentation to emphasize that there is a overlap between resoning, tool use, agent and long-term context tasks, and that a faired protocol is required to judge the source of the proceeds.
- Add a new curriculum branch table in Section 4.5 to distinguish between prior capacity, first length or parallel validation by the main product objective, avoiding the writing of “first-power before-length” as a hard rule.
- To add section 6.7 to the available red green summary.
- Supplementing the three steps in accident management in section 7.0: freezing of site, determination level, stratification.
- Replace section 8.0 with an executable Gate dashboard, with audit fields such as owner, Next action and event_path/version_hash/status.
- Upgrading section 9.0 to a minimum package and delivery index, specifying the template location, freezing Gate and using the meeting.
- Amend the title of chapter 11 to read “Examples search grid, not directly as default mix”, and write the hard conditions before entering the scale table on the same screen.
- Add a new text-block entry, which will be then compressed to chapter 13 go/no-go memo minimum template, reducing duplication with 0.2 and 9.0.

In the seventh time frame, the author ' s technical and editorial review was followed by the following revisions:

- Upgrading the use of navigation to " Use navigation/mainline maps " , tightening the first round of the validation of the corresponding chapters to 4.0, 4.4 and 11.
- Add a new summary of evidence in cases in chapter 3 and split it by the original reporting terminology, reporting facts, evidence labels, safe syntheses, non-publishing and internal validation actions.
- To downgrade the “engineering inspiration/reusable points” of the cases in chapter 3 to “convertable into internal assumptions/checks” and avoid the reader being co-mingled into public teams recipe.
- To replace the beginning of chapter 4 with the first round of minimum closed loop instruction and to make it clear that the “minimum closed link” is the minimum evidence chain and not the least training formula.
- Amend the two details of section 4.3.1: the word “scale” condition to “four” and the length variable to read `sequitation_slistrition / Lengh_distrification / Length_bucket_ratio'.
- Additional information in section 6.6: The frozen SFT/RL recipe is a diagnostic instrument and does not represent the production of the past-train formulation.
- Further downgrade of chapter 11 to a minimum evidence chain sample, with clear ratios and token blocks not to be used as default multiples, default LRs or default budgets.
- To compress chapter 13 into a minimum template for go/no-go memo, reducing duplication with 0.2 and 9.0.

The eighth time-frame was optimized by the following revisions following the author ' s incorporation of the technical and editorial reviews:

- Uniform title, target reader, section 1.4 and chapter 10 is termed “the team of modeled mid-train with post-train experience prepared to assume the role of the model”.
- Condensed long-text interpretation: 32K/128K/256K may be an example of extended training length, and the 1M context must separately describe the length of training, location/attenance extrapolation, servicing and cost validation.
- To specify section 8.0 as the only Gate dashboard, section 4.6 retains only the role, account and signature responsibility, avoiding the two sets of gate calibres.
- Change the percentage of data in chapter 11 to the Bucket Sensity sweep axis, making it clear that they are not a unicoded scale to be met simultaneously.
- Adjustment of the strict rules of accidents: Capability and training results must be divided into four layers; the unrelated layer can be written `N/A ' and reasons to avoid mechanical setups.
- Clearly, final-blinder should be maintained until Gate 5 or released, to prevent phased penetration.
- Add at the post-training handoff: once SFT/RL data, reward, verifier, budget or seed have been adjusted, an experiment_id or paired_protocol_version, old papered conclusions cannot be used as evidence of the return of the Mid-train.
- Completion of audit fields such as `status ' , `version_hash ' , `stale_after ' , `signoff ' , `reviewed_by ' , for chapter 13.

# Appendix B: Final quality statement

This paper is currently used as an internal manual for the start-up of the Mid-Train project for the model team, but it is not yet a training formula or a rescript for the public model.

♪ The last one ♪
| --- | --- | --- |
Structure <unk> has formed a closed loop for "Use Navigation - > Define Boundary - > Evidence Map - > Experimental Design - > Engineering Inspection - > event review - > runbook - > roadmap - > reviewlist - > Source Map - > go/no-go memo"
<unk> Factual qualification Distinguishing the facts of the report, the syntheses, the project syntheses and assumptions to be validated, and maintaining the claim/source article before chapter 12 should still review the latest version of the report and the paper, particularly after 2026
<unk> Implementation route <unk> Gate 0-5 dashboard, minimum delivery package, scorecard, incidident runbook and go/no-go memo already supporting the start-up of the project <unk> threshold, budget, model size and acceptance line must be set by the team according to its own model and product objectives <unk>
<unk> Recipe boundary <unk> Chapter 11 has been downgraded to sensitization sample to avoid being copied into default mix, LR or token bugget <unk> need to be internally validated before any amplification training is available
Risk control has covered data, training, eval, infra, capability, pot-train handoff six and requires evidence trails and versions of hash <unk> to access the team real training platform, the eval system, model review and permission audit before the project is fielded
Eight rounds of technical and editorial reviews have been recorded in appendix A, and core differences have been absorbed into the body of the text.
