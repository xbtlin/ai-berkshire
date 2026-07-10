# Mid-train Technical Overview and Landing Manual: A Model Team with Post-train Experience

Scope of information: Public information for the last two years; latest version of the same model family priority, last version at most, older version only if there is irreplaceable evidence
Target audience: Post-training experience, team to assume mid-train; also suitable for Model/ Data/ Training/ Eval/ Post-train DRI
Conclusion nature: Technical research and engineering references, not constituting any commercial or investment proposal

# Use navigation/ mainline map

This article is not a summary of the literature that must be read from the beginning, but a gate-driven launch manual. If you want to open a Mid-training launch today, you will read 0.2, 0.3, 8 and 9; if you want to design data and experiments, read 4.2-4.6, 6, 11; if you have an accident in training, read directly 7; if you want to verify public information and quote boundaries, read 2, 3, 12.

** The main line is one: to prove that the target is worth the middle-training, then to prove the data and assessment credible, then to prove that the short-range training is effective and finally to prove that the proceeds remain.**

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

** Mid-train is not a magnifying post-train, nor is it simply a run-off of pretrain.** A conservative definition of project is used here:

> Mid-train is a postbase pretain, former post-train section of SFT/RL, etc., which continues to be controlled and trained to change the distribution of capabilities of models, their contextual adaptive capacity, and the subsequent trainingability available to SFT/RL.

In the public information, OLMo 2 explicitly refers to the postbase pretraining and pre-post-training phases as Mid-training; Qwen3, DeepSeek-V3, Qwen2.5-1M and so on, not always use this term, but as pre-training, recontinued pre-training, context interpretation or long-text pre-training.

Information selection does not include model history review. Each model family gives priority to the latest version of the public technical report; the last version only retains the previous version or necessary exceptions when the current version of the report is disclosed, for example, 1M context, the obvious Mid-training name, annealing or synthetic data details.

In practice, the new team should not pursue large-scale training first, but rather small models (ablation, data barrel validation, pollution inspection, base regression assessment) and then test the direction with a fixed post-train return to verify whether the proceeds are being retained.** Mid-train success criteria are not a base benchmark rise, but a gain still exists after the empowerment, oblivion, post-train.**

On the border, this does not equate all continued pretraining with Mid-train, nor does it simply classify reasoning or architecture techniques such as DCA, YarN, standard application, chunked prefill as a training formula. Public cases can only be used as design references and cannot be copied as recipipe.

The data ratio in the text, token Budget, 90-day road map, quality door and accident runbook are all project starters for new teams and are not the general conclusions given directly in the public papers.

For a team of model models with post-training experience ready to take on mid-train, the most important thing is not to go on to mass training immediately, but to build four things first:

1. ** Clear target and non-smoking**: Math upgrading, for example, cannot be achieved at the expense of universal dialogue, factual knowledge, multilingual competence.
2. ** Small modelling and short-range ablation**: validation of data drums, learning rates, sequence length, pollution control and risk of forgetting.
3. ** Created a Mid-train dedicated evaluation**: not just pretrain loss, not post-post-post-post-post-post-post-post-post-post-train.
4. ** One of the success criteria for the Post-Train TRI relay**: Mid-Train is that the gains from SFT/RL remain manageable and more manageable than just base checkpoints for some of the zero-shot scores.

#0.1 Reader decision tree: What kind of mid-train do you really want to be?

The first round of the experiment, the key assessment, the beginning of the process, the beginning of the process.
| --- | --- | --- | --- | --- |
Mathematics, code, STEM, complex QA <unk> Capabilty Mid-train <unk> small model data mex + Low LR short-range training <unk> Target capability enhancement + Universal capability retreat <unk> also stretching to 128K/1M <unk>
<unk> 32K/128K Long context <unk> Context extension<unk> Gradual length extension + Long Document Data Bail
RL reading caps <unk> Reasoning substrate Mid-training <unk> Verifys if base has edge-of-competence <unk> Fixed RL/RLVR relays <unk> Use RL as a source of capacity per se
<unk> Vertical field capability <unk> Domain continued pretraining <unk> Data in low-ratio fields + General-fiscal data <unk> Field tasks + Universal-return <unk> Training in single-area language <unk>
Code agent / tool use <unk> Code/ FIM/trajetory Mid-training UIM, repo-level integration, multi-file positioning <unk> repo task, post-train

This decision tree is an executive portal, not an exclusive classification. A mature project may end up containing both capability, long-content adaptation and post-training assumptions, but ** it is best to test only one main hypothesis in the first round.

# 0.2 How do you start the first day?

If you want to start the Mid-training project today, don't start training first.

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
Post-train DRI <unk> 1.2, 6.6, 7.6, 8 <unk> paired protocol, Seed/budget/harness, profit retention judgement
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

- Whether the knowledge, algorithm models and presentation capabilities needed to solve problems are available within the model.
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

1. **Mid-training is aimed at the distribution of competencies, not the style of responses.**
2. The main loss of Mid-train is usually still close to the goal of language modelling rather than preference for optimization.
3. Mid-training data may contain QA/CoT/FIM, but ** Do not move the SFT data forward as a whole**.
4. ** Mid-training 's good checkpoint is not necessarily the least checkpoint**, but the Pareto point between capacity enhancement and forgetting.
5. **Mid-train proceeds must be observed in base event and post-train rediness**
** Data contamination is more dangerous than SFT in mid-train** because it enters base capacity judgement.
Synthesis data should be validated and stratified first and should not be increased by “favourable”.
8. Long context capabilities distinguish between the length of training, extrapolation and line service.
9. The **RL returns are usually dependent on the availability of the base** and cannot be passed on to RL.
10. ** The conditions must be stopped before the expansion training**; mid-train is not “continue before the budget is spent”.

#2. Public evidence is weak and weak

The public material is not entirely consistent, and the most likely error is to mix “the researcher's summary” and “the industry experience in interviews” in the “training phase” that the report clearly describes. This paper uses information by evidence strength and model version of the two new lines: the family of the same model gives priority to the latest version, at most the previous one; earlier material is the exception only when there is no alternative evidence.

##2.0 Evidence label for this post

To avoid mixing public facts with engineering assumptions, the following text implicitly uses four categories of evidence labels:

The label, the label, the meaning, the meaning, the meaning, the meaning, the meaning, the meaning, the meaning, the meaning, the meaning, the meaning, the meaning, the meaning, the meaning, the meaning, the meaning, the meaning, the meaning, the meaning, the meaning, the meaning, the meaning, the meaning, the meaning, the meaning, the meaning, the purpose, the purpose, the purpose, the purpose, the purpose, the purpose, the purpose, the purpose, the purpose, the purpose, the purpose, the purpose, the purpose, the purpose, the purpose, the purpose, the purpose, the purpose, the purpose, the purpose, the purpose, the purpose, the purpose, the purpose, the purpose, the purpose, the purpose, the purpose, the purpose, the purpose, the purpose, the purpose, the purpose, the purpose, the purpose, the purpose, the purpose, the purpose, the purpose, the purpose, the purpose, the purpose, the purpose, the purpose, the purpose, the purpose, the purpose, the purpose, the purpose, the purpose, the purpose, the purpose, the purpose, the purpose, the purpose, the purpose, the, the, the, the, the, the, the purpose, the purpose, the, the purpose, the, the, the, the, the purpose, the purpose, the purpose, the purpose, the purpose, the purpose, the purpose, the purpose, the purpose, the purpose, the purpose, the purpose, the purpose, the purpose, the purpose, the purpose, the purpose, the purpose, the purpose, the purpose, the, the, the purpose, the purpose, the purpose, the purpose, the purpose, the purpose, the purpose, the purpose, the purpose, the purpose, the purpose, the purpose, the, the, the, the, the purpose, the, the, the, the purpose,
| --- | --- | --- | --- |
<unk> Reporting facts Technical report, paper or direct disclosure of official material, token, contact, data type, training target, description of what a team actually did, and launching other teams should carry the same formula
<unk> Thesis summarizes the mechanisms, taxony, variable relationships, etc., design interiors, create assumptions, directly upgrade to the industry-level training law
The conservative practice suggested by the study based on a number of cases, the development of project processes, gate, billing and risk control, the claim that it was the original conclusion of a report, the claim that the project was a project, the claim that the project was a project, the claim that the project was a project, the claim that the project was a project, the claim that the project was a project, the claim that the project was a project, the claim that the project was a project, the claim that the project was a project, the claim that the project was a project, the claim that the project was a project, the claim that the project was a project, the claim that the report was a project, the claim that the report was a project, the claim that the project was a project, the claim that the project was a project, the claim that the project was a project, the claim that the project was a project, the claim that the project was a project, the claim that the project was a project was a project, the case that was a project, the case that was a project, the case that was a project, the case that was a project, the case that was a project, the project was a project, the project, the project was a project, the project, the project was a project that was a project, the project that was a project that was a project that was a project that was a project, the project that was a project, the project that was a project, the project, the project that was a project, the project that was a project that was a project, the project, the project that was a project that was a project that was a project, the project that the project that was a project, the project that was a project that the project, the project, the project, the project, the project, the project, the project, the project that was a project that was a project that was
<unk> Pending verification of the hypothesis <unk> Interviews, blogs, trade calibres or direction inspired by small samples <unk> Entering small models/short-range experiments <unk> Entering master models for magnifying decision making <unk>

Readers should use the term “report facts” as a base of fact, using the words “discussions” and “engineering” as experimental design inputs, and “supposing assumptions” as backlogs. Any decision that consumes large-scale training budgets should be returned to the team’s own data database, eval review and post-training implemented project.

##2.1 Strong evidence: stage design for clear disclosure in technical reports

Strong evidence refers to the training phase, token scale, context length or data strategy that the model team directly discloses in the technical report.

The case is the level of the report, the original term, the public report directly supports the project.
| --- | --- | --- | --- | --- |
Qwen3 <unk> pre-training stops / Reasoning / Long Context pre-training stage; approximately 36T total, approximately 5T reading-stall tokens, 32K long-term context training <unk> mid-training-like capability
<unk> DeepSeek-V3 master read; replace <unk> long contextextense 14.8 T base pre-training using YaRN to make two paragraphs of 1000 steps 4K->32K->128K contextense <unk> mid-train-like long-text interpretation
<unk> GLM-4.5 <unk> mid-training <unk> 23T pre-training about 1.1T mid-training tokens, with three subphases of the visualization: repo-level code (~500B,4K<unk> 32K), synthetic reading (~500B), long-context + agent (~100B, 1-1228K); MoE 355B <unk> generic mid-training + multi-stage plastic + progressive modexentsion; reference sample for mid-train under the MoE structure
<unk> wen2.5-1M <unk> Previous special reserve <unk> Long-content pre-training / post-training / inference scaling <unk> progressing long-term-content pre-training, long-line post-training, DCA/YaRN extrapolation, dilution and chanked prefilling deployment
<unk> OLMo 2 <unk> Middle-training ->mid-training -> clear stratification instrification/preference turing; more transparent details such as Dolmino Mix, 50B/100B/300B, micro-annealing <unk> mid-training public reference sample in narrow sense <unk>
<unk> Phi-4 <unk> Pretaining / midtraining / post-training <unk> & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & & ; & & & ; & & & & & & & & ; & & & & & & & & & & & ; & & & & & ; & & & ; & & ; & ; ; & & ; ; ; ;
Llama pre-training / long-content pre-training / annealing 405B in 15.6 T tokens pre-training, about 800B tokens long-context pre-training to 128K, and finally 40M tokens annealing <unk> late-staage Conservative reference pre-training and annealing

These reports support the existence of the "phase design" but usually do not support the "Run-up-data ratio or learning rate". Unpublished tokenizers, data cleansing, sampling strategies, base checkpoint states, optimizer status and system realizations have significant impact on results.

##2.2 Evidence: Summary and Summary of Controlled Experiments

The study Mid-training survey, PRISM and pre-training / Mid-training / RL interplay help teams understand the variable relationship: data retention versus ability migration, capacity at model reach borders, RL whether RL can benefit from mid-trained checkpoint, etc.

The value of these studies is to present institutional assumptions and experimental dimensions, rather than to give a direct extrapolable industrial formulation. In particular, controlled synthetic task or small-scale model conclusions cannot be directly upgraded to “all large model training laws”.

#2.3 Weak evidence: interviews, blogs and industry calibres

Interviews and blogs often provide two types of information: how the terms are used by practitioners, and how teams describe the organizational logic of the training phase. But such information often omits failed experiments, data details, and engineering constraints, so it can only be used as a trend background and not as a hard fact.

If the interview claims that a certain stage is “very important”, it is considered as a test assumption; training decisions are entered only after technical reports, reproducing experiments or within a team support.

#2.4 Conservative consensus from open sources

First, the mid-train-like phase usually occurs before the base capacity is formed. Qwen3, DeepSeek-V3, GLM-4.5 are master samples; Qwen2.5-1M, OLMo 2, Phi-4, Llama 3 are used as the last special, necessary exception or downgrade reference. GLM-4.5 and OLMO 2 are the most subtle samples of the current public report phase, using the middle-training term, GLM-4.5 further decombating the mid-training sub-stages.

Second, in cases such as Qwen3, OLMo 2, Phi-4, Llama 3, late-stay / agreed pre-training often accompanied by stronger data screening, capability-directional sampling or high-quality data upswing; but the DeepSeek-V3 cases mainly support the length of the phase-up and do not directly support the data matching. It is more prudent to say that the marginal value of late token relies more on quality, match-making and training objectives than simply adding web to to the conclusions.

Third, the long context is not just the RoPE context. Real and long context capabilities require training data, length curriculum, location/focus mechanisms, reasoning frameworks, and assessment missions.

Fourthly, it is more appropriate to consider the strong engineering hypothesis of “enhancement of RL available substrate” than the general rule that has been proven. The more conservative argument is that if base/mid-trained checkpoint is completely non-constructive to the target mission, RL usually has difficulty in generating capacity; but RL brings real capacity gains also depends on pretraining exposure, whether the task is located at the border of model capacity, reward design and exploration budgets.

Fifth, synthetic data are valuable, but not free lunches. Phi-4 describes synthetic data that can significantly influence the reading performance and reminds the team that organic data are still needed to complement the world ' s knowledge, express diversity and distribution.

Sixth, transparent experimental accounts are more important than a single list. One of the greatest values of OLMo 2 reports is to separate the composition of pretraining, mid-training, post-training and data, helping later teams to build their own lines, drums and returns assessments.

Seventh, the public report can prove that “some mature teams have adopted phased late-stage trading” but rarely that “a given data ratio, learning rate or token bugget is the best for common use.” All subsequent recipe tables should read search space and quality door instead of re-engineer formulas from a model report.

# 3. What a public case can prove, what a public case can prove

This chapter is not a recapitulation of the model report or a recipipe source. The case is used only to answer “what public facts can be turned into internal checks” and follows the selection rules of the version: the latest version of the same model family, at most the previous edition, must be given a reason for the reservation; earlier samples must be given.

Case / information <unk> Use level <unk> Why keep <unk> safe to summarize <unk> not to launch <unk> internal authentication actions <unk>
| --- | --- | --- | --- | --- | --- |
<unk> wen3 <unk> master reading: sample of current/updated open technical reports <unk> discloses that stage 3 pre-training <unk> capability mapping and context targeting management <unk> original report self-identi-training, or full data matching rebuttable <unk> break capabilities to different length context experiments experiment_id <unk>
<unk> DeepSeek-V3 Main read: DeepSeek-V series public base report sample; should similar details be disclosed with the new family report, replace <unk> 32K/128K contact exit after disclosure of 14.8 T base pre-training, and stress architecture/system synergy <unk> context verification of training, architecture, serving, eval <unk> contact exit, etc. equals continuing training of general data to do offline/online long-term context consistency and short-term task return <unk>
<unk> GLM-4.5 Main reading: sample of the latest public technical report of the GLM family <unk> visible use of the Mid-training term to disclose ~1.1 T tokens ' tristage (repo-level code / synthetic resoning / long-content + agent), progressive 4K ~32 K 1-128K context interpretation <unk> mid-training can be separated into multiple substages by capacity objectives;Synthetic reasoning and anent trajectory data can be injected into the mid-train phase with a MoE structure, sub-stage token scale or specialist route strategy directly appropriate for the dese mode platinum by sub-phase experition_id; MoE additional monitoring path by entropy and specialist load
<unk> wen2.5-1M <unk> Previous special reserve <unk> wen3 not replacing details of 1M confext training, extrapolation and deployment <unk> Training length, extrapolation, deployment costs and real tasks separately <unk> Mid-training to 1M, or purely theoretical techniques <unk> Recording of tradeing length, servicing config, latency/cost and real tasks
<unk> OLMo 2 <unk> Required exceptions <unk> Clear use of mid-training terms and disclosure of data mix, micr-annealing, pot-training layers <unk> mid-training can independently manage and retain Domino mix of line/valgate <unk> OLMo 2, token numbers suitable for other models <unk> Create checkpoint lineage, mid-training pre-evaluation of <unk>
<unk> Phi-4 <unk> Disclosure synthetic data for pretring and midtraining, and obvious midtraining to undertake 4K-> 16K extensions <unk> synthesis data with a vereifier, style diversity and organic data spin
<unk> Llama 3 <unk> read only when public details of late-stay agreed pre-training, long-content pre-training, annealing are required
<unk> PRISM/ pre-mid-RL study mechanism hypothesis, not model version line <unk> use controlled experiments to raise retention, interaction, RL substrate problems <unk> Mechanism assumption to enter proxy adaptation system to upgrade to the law of large industry models <unk> use of paired SFT/RL certification proceeds <unk>

This table is used in a simple way: read the master sample first; only the current model report does not cover a key issue, is it necessary to read the previous version or the necessary exception. If the target group does something about a particular model family, such as Qwen, DeepSeek, Llama or self-research models, the internal information package should be replaced with the family’s latest report, with a maximum of one previous edition retained as a comparison.

The old version of the case retains only three scenarios: first, it provides terms or governance structures that are not available in the current version, such as the Mid-training layer of OLMo 2; second, it provides critical engineering work for dedicated capacity, such as the training/extension/deployment split of Qwen2.5-1M for 1M context; and third, it provides a controlled variable that has not been replaced by new reporting, such as the synthetic data boundary of Lla 3 or Phi-4. In addition, the old model should not enter the master list.

#4. Mid-train design framework

This chapter is first read in the first round of the minimum closed loop: Gate 0 freezing target capacity, non-sacrificial ability, eval recovery and post-train prepared process; Gate 1 freezing data manifest; Gate 2 excluding the bad direction with control mix + 3-5 single variable at the proxy scale; Gate 3 using target mode short-range training to find capability/forgotten Pareto checkpoint; Gate 4 using the same set of frozen past-train implemented proceeds to verify whether the proceeds are retained.4.1-4.6 Explain the goal, data, training knobs, ablation, curiculum and organizational quality doors in the closed ring.

An implementable Mid-training project should ultimately answer five questions: what is the target capacity, what is not to degrade, which is driven by the data drums, how the length/learning rate/content curriculum of training is set up and how it can prove useful for post-training.

# 4.0 First round of the minimum closed

The minimum closed loop is not the minimum training formula, but the minimum evidence chain: whether data, training, evaluation and the post-training relay can be interpreted at the lowest possible experimental cost. Run through one target, one master hypothesis, one data drum, one short training window, one frozen post-train executed protocol.

♪ The little thing that's got to be done ♪
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

- The Universal Language Model loss doesn't go up very well.
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

- Whether SFT is better to learn the target format after.
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
<unk> Synthetic materials <unk> Condensed concepts, pedagogy reasoning <unk> Single style, wrong teacher <unk> multiteacher, multi-template, certifier filter <unk>
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

> [!CAUTION]
> - ** No manifest/ash, no training**
> - ** There is no corresponding eval, does not increase sampling weight**
> - ** Contamination hit untreated and not entering the prismy experiment**
> - ** Synthetic data are not correctly filtered and style diversity checked, and do not exceed the low proportion explored.**
> - ** Field data do not have generic regression protection and do not enter the main model short-range.**
> - ** Long context data only bind text, no real long task, no long-text prism mix.**
> - ** Any action to change filters, quality models, dedup thresholds, sampling weights, synthetic generation prompt or data sequence must generate new `data_manifest_hash ' and `experaction_id ' .**

##4.2.2 Use boundaries for synthetic data

Synthetic data need to be addressed separately, as it is the most easy to “seem effective” on short-term indicators:

Risk, risk, performance, control, control.
| --- | --- | --- |
<unk> Teacher error magnification <unk> Math/code answers seem fluid but unverifiable <unk> Verifyable, answer check, sample manual review
<unk> Style template <unk> Output is all like the same teacher, reasoning moves fixed <unk> multiteacher, multiprompt, multi-drying, blending organic data <unk>
Benchmark, near pollution, public issue changes are on the rise, solver structures, embedding and translating duplicate checkup.
<unk> Difficulty distribution is not true <unk> Training is too simple or covers only one type <unk> Difficult batch, failure sample refill, private holdout comparison
<unk> COT excess before behavior <unk> base model early learns long interpretation format <unk> control of CT ratio, mix short answers, no COT, natural text <unk>

** The logical use of synthetic data is "verifiable ability amplifiers" not low-cost token alternatives. ** Mathematics, codes, structural reasoning are suitable for multiple verifiable synthesis; open domain knowledge, language style, multilingual expression still requires a high quality organic data mix.

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
<unk> lr_schedule / `warmup ' <unk> influences forgetting, gathering and lost fraction only compared to final scores and not to training stability <unk>
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
<unk> Pipeline and eval calibration proxy model, e. g. 1B/3B<unk> 1B-3B tokens <unk> small sample drums mix <unk> low LR single dot <unk> loss normal, eval can recreate <unk> los spike, eval unstable <unk>
<unk> Generic baseline <unk> proxy model, e.g. 3B/7B<unk> 3B-10B tokens <unk> Universal high quality ratio 30/50/70% <unk> Fixed low LR <unk> Universal ability to withdraw control <unk> Multilingual/fact crash <unk>
<unk> Math/STEM Injects Proxy model, e.g. 3B/7B<unk> 5B-20B tokens<unk> Mathematics/STEM 10/20/30%
<unk> code/FIM injects <unk> proxy model, e.g. 3B/7B<unk> 5B-20B tokens <unk> code/FIM 10/20/30 <unk> Fixed Low LR<unk> completion/FIM/repo task Upgrade <unk> Normal Generate Clear Codeization
<unk> Synthetic data ratio <unk> proxy model, e.g. 3B/7B<unk> 5B-20B tokens<unk> synthetic 5/15/30%
<unk> Primary model short-range validation 10B-100B tokens <unk> 2-3 <unk> 6 mix <unk> low LR sweep <unk> Pareto checkpoint appears <unk> target capacity not rising or forgotten too much <unk>

The output of these experiments is not a final model, but a decision as to which data drums are valid, which proportion is dangerous, which learning rate is safe between regions and whether it is worth more major training.

# 4.4.1 How to read

The output of Ablation is to exclude bad directions and to create a candidate, not to prove the final formula.

1. **Proxy success is not equal to the Target success**; two scale are required in the same direction before entering the main model or the target short run review.
2. ** The rise in the single public list is not equivalent to an increase in capacity**; it must be seen with the private holdout, the failure sample, and manual review.
3. **Target capacity enhancement must be seen with guardrail**; mathematics/code rises and there is a pronounced drop in speech, fact, natural creation, not a clean gain.
4. Results close to thresholds are repeated or reviewed next to run;** not to be expanded with a small share of proceeds seen at a time**.
5. ** Any midway conversion of the versions of the micix, filter, LR, length curiculum or eval must be reopened.**

# 4.5 Curriculum: Capability, later length, parallel?

It is recommended that the new team not mix all targets at the outset.

The more stable order is:

Base surety check: confirm the availability of checkpoint, tokenizer, optimizer state, data pipeline, evaluation system.
2. Capable mid-train: Mathematics/code/STEM/Quality synthesis data, short range ablation.
3. Long context: gradually stretching from shorter context, with separate surveillance of the boss 's context loss and real tasks.
4. Small-scale post-training relay: compare Mid-train with SFT/RL comparison checkpoint.
5. Whether to merge into the main training formula.

Why do you suggest a length after capacity? Because long context training is expensive, debug is difficult, and it is easy to mix architecture with data problems. If model base reading/code capacity is not improved, long context simply magnifies input windows, not necessarily mission capacity.

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
`Seed ' / `cost ' / `incident_log ' <unk> Random seeds, training costs, anomalies and handling actions <unk>
<unk> Summary of the conclusions of `reult_summary ' / `dission ' / `signoff ' , <unk> , kill/retry/extend/promote decision-making, signatory <unk>
<unk> post_training_readines_result ' <unk> Fixed SFT/RL proceeds retained

Third, the only authority for the quality door is placed in section 8.0; this section only defines roles, desk fields and signature duties. This does not set a threshold for teams, but the minimum level of target capacity, the maximum withdrawal of generic capabilities, private event pass rates, the maximum pollution mean, the Loss Spike treatment rules, style drift determination, and the ratio of proceeds retained after the post-train status, evidentiary path, version Hash and expiry times are defined as section 8.0 dashboard.

<unk> Gate <unk> Entry conditions <unk> Exit conditions <unk> Interrupting conditions <unk> Signator <unk>
| --- | --- | --- | --- | --- |
<unk> Gate 0: target capacity, non-sacrificial capacity, budget and post-train relay needs are identified <unk> Mid-train charter passed; v1val relay and v1 post-train pretocol status is based on section 8.0 dashboard DRI, none of the whited protocol owner/schema, no private owner homeer/schema <unk> Model Lead, Eval Dri, Post-train Dri <unk>
<unk> Gate 1: Data freeze Data source, License, Cleaning, Reloading and Contamination check complete
<unk> Gate 2: Proxy campaign <unk> at least two candidates mics and fixed event suite <unk> proxy are used to exclude bad directions; two scales are required to match or target short-range to verify key signals <unk> to increase the public benchmark, private tasks remain intact, general capabilities are falling <unk> Model Lead, Eval DRI, Data DRI <unk>
<unk> Gate 3: Main model short course training runbook, resume, surveillance and kill switch ready <unk> Pareto checkpoint, pine break can explain <unk> nan, unrecoverable los spike, gradient anomaly, vomit anomaly, resume incoherent, short-term, long-term, long-term, short-term tasks <unk> Training Infra DRI, Eval DRI, Model Lead
<unk> Gate 4: Post-train relay recipe, seed, budget, harness, failed determinations frozen post-protocol proceeds retained without significant deterioration <unk> mid-train proceeds disappeared after post-protin, passed protocol changes or difficulties increased significantly
<unk> Gate 5: Magnifying training Source of proceeds: data/evenal/auto-memo stabilized Go/no-go memo pass, entering the next budget <unk> Revenue dependent on pollution, narrow assessment, occasional checkpoint or inability to recreate <unk> policy owner, Model Lead, Release owner <unk>

Fourth, the pace of meetings is to serve decision-making and not to report:

- Daily trading review: loss, vomiting, nn/loss spice, checkpoint, resume, accident management.
- Twiice-weekly event review: target capability, general return, private holdout, manual sample review.
- Weekly decision review:kill, retry, extend, promote, based on billing and gate memo decision-making only.
- Whether Post-train handoff review: Paired protocol is effective, whether the proceeds are preserved and whether security and style are degraded.

The bottom line of the mechanism is: ** Calendars are not a substitute for quality doors**. 90 days are just reference rhythms. Whether or not to move to the next stage is determined by data readiness, training stability, val stability and the post-training relay validation.

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

** Not to wait until the training is over for the event.** The failures of Mid-train are often early signalling: a universal evaal crash, output style templateing, a data drum loss anomaly, long context short mission degradation.

#5.3 Checkpoint Policy

Suggested retention:

- pre-mid checkpoint。
- Early/mid/final checkpoint for each stage.
- Checkpoint before and after the change in the learning rate.
- Context length criculum checkpoint for each length.
- Candidates for the post-training relay checkpoint.

Not just the last. **The best checkpoint for Mid-train may not be the least checkpoint for the lost, but the best for Pareto between the target ability and the forgotten. **

# 5.4 Easily underestimated engineering risks

First, mass-lingth batting and context parallelism can cause load imbalances. The long-term catch-batch-showing, waste-and-communication patterns are different from the short-situation context, and training surveillance must be removed by length, otherwise the whole-scale vomiting will mask local instability.

Second, there may be problems with the succession or replacement of the ottiizer state. The succession of the otimizer state is more like an extension of the original training trajectory, but may inherit the old stage momentum; the reset of the otimizer state is cleaner, but the re-engineering of the warmup is necessary, otherwise it is easy to lose spike or slow-down. Both options should be measured at the proxy scale.

Third,** training & & & & & & & & & & ; training & & & & & & & ; & & ; ; training & & & & & & & ; ; training & & & & & & ; ; training & & & & ; ; ; ; ; & & ; ; ; ; ; ; ; ; ; ; ; ; ; ; ; ; ; ; ; ; ; ; ; ; ; ; ; ;

#6. Assessment system

# 6.0 from benchmark list to eval recall

Mid-training does not collect the list, but a set of eval object values, which are available for a tape version, a state of contamination, running harm, thresholds and original output;** the results of the evaluation, which did not enter registry, are only to be observed and not to go/no-go.**

Each project sets a maximum of 3-5 prism indicators, with several additional guardrails and diagnostics. Primaric is too much to induce a cherry-nick, and diagnostic is too little to make the team aware of why it is going to go up or down.

# 6.1 Eval review schema

Eval DRI should freeze v0 owner and schema in Gate 0 and then freeze v1 emergency record before entering Gate 1. The smallest fields are as follows:

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
<unk> Code/ FIM <unk> HumanEval/ MBPP/EvalPlus, FIM, repo-level commation, multifile positioning <unk> SWE-bench/ tool-use as readess or diagnostic <unk>
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
- When the key conclusions are close to the threshold, more than seed or repeated run and report deviations or bootstrapped CI.
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

** If the return on an indicator is exceptionally high and private tasks, manual reviews and adjacent eval are not supported, then contamination, formatting or completion should be assumed, rather than a breach of capability should be announced.**

Gate meeting first look at a line of red and green summaries and then look at the whole section:

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

> [!CAUTION]
> ** Hard rule: Any competency or training effect conclusion must be completed first in four layers of isolation**: system recall, data manifest diff, eval hares diff, model checkpoint diff; if a level is not involved in the accident, it should be marked `N/A ' and should state the reasons.** When the evidence is not complete, only the absence of the causality can only be registered and not included in the capability conclusion**

#7.1 Accident classification: observation, alarm, block

<unk> Level, <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> , <unk> ,
| --- | --- | --- | --- |
<unk> Observation individual event small fluctuations, drums loss slightly deflect, single seed close to the threshold log incident_id, rerun adjacent checkpoint or fixed sample baskets
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

** If the post-train relay fails under the paired protocol two consecutive rounds and the base end proceeds are only available in public benchmark or a single seed, kill the Mid-train direction**; if the base end gains are stable but covered by SFT/RL, write the conclusion as “post-train handleoff” is not completed and do not write as “mid-train no gain”.When adjusting SFT/RL data, reward, verifier, budget or seed for the purpose of checking the coverage, the old papered protocol conclusions cannot continue as mid-train return evidence but as a diagnostic trail.

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

This road map is a reference rhythm, not a calendar commitment.** The next stage should be decided by Gate 0-5 and not by the next few days.**

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

> [!CAUTION]
> ** Do not go around with "see again" as long as some gate evidence is incomplete.** Mid-train projects are costly,** true rhythm control comes from gate, not calendar**.

Each gaste dashboard record must also contain `status ', `owner ', `evidence_path ', `version_hash ', `stale_after ' and `text_action ' .** Green status without an evident path should be considered yellow.**

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
- triggering a stop or rollback when a nan appears, loss spike cannot be restored, gradient abnormal, vomit abnormal, a data drum loss abnormal, checkpoint resume is not continuous, or long context training for short injury tasks.

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

- ** If the income is derived mainly from pollution, narrow assessment or post-train accident, not magnified.**
- if the benefits are stable, understandable, retained after the post-training, entering the main training.

#9. Executable checklist

##9.0 Minimum Delivery Pack and Delivery Index

If the team does not want to maintain the complete document system from the start, it must have at least eight deliverables below. Without any one, it is difficult to rewrite the middle-train conclusion.

♪ What meeting is the time when the ♪
| --- | --- | --- | --- | --- |
Mid-train charter <unk> Model Leader <unk> 8.0 <unk> Gate 0 <unk> Startup Conference, go/no-go
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
- [ ] Synthetic data records techer/version, prompt, sampling parameters, verifier, filter rules, rejection rates, template repetition rates, manual error rates.
- [ ] Synthesis data have correct filtering, diversity, templateing and style intropy checks.
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
- [ ] Any intermediate change of mix, filter, or version of the eval will create a new version of the experiment_id.
- [ ] There are stop conditions in training.
- [ ] Must pass go/no-go date before amplifying training.
- [ ] reserve complete reports of pre-mid, mid, pot types of checkpoint prior to publication.

#10 Special reminder to the team of model models with post-training experience

First,** do not use the SFT mind to make Mid-train** (see 1.2, 1.4 for details). Mid-train data can contain QA, CoT, code tasks, but its goal is not to let models learn to answer the format of their products, but to change the distribution of capabilities.** Self-censorship: if the data mix is mostly command-to-answer, probably pre-sipulation of SFTs, rather than capability.**

Second,** RL should not be allowed to take the fall** (for details see 2.4, point 4, 6.6. If base model does not have enough mathematics, code, long context and self-correction substrate, RL may well learn only surface search or lengthy reasoning.** Self-censorship: if target task zero zero zero, the RL will probably not be able to be properly investigated ** if capacity is not within the base's reach border.

Third,** not just follow** (for details see 6.4, 7.2 event, 8.0). Mid-train ' s real gains are to be established in both private tasks, real product tasks and the post-train relay.** Self-censorship: if a certain event returns more than 5 percentage points but private holdout remains intact, assuming contamination or format is appropriate**.

Fourth,** do not start with 1M contact** (see 4.5 for details), but for most teams, it is more realistic to make 32K/128K reliable than to display extremely long context.** Self-censorship: if short-term (<4K) performance is significantly reduced after stretching, the cost of context interpretation is not contained**.

Fifth,** do not ignore the data engineering** (for details, see 4.2, 4.2.1, 9.1). In the Mid-training project, training codes are often not bottlenecks, as are data lines, pollution control, drums and experimental discipline.** Self-censorship: if the team is unable to identify the data most hash and the pollution inspection version of the current training within 30 seconds, the data governance is not in place**.

#11 First round of search space: example search grids, not directly as default mix

This chapter is a work example, not a formula. It is designed to help the team who first made Mid-Train to bind data, training, evaluation and the post-train relay into a minimum evidence chain (for the definition of the “minimum closed link”, see 4.0).

If the team already has a base model and a stable post-training pipeline, it is recommended that the first round not be large and complete, but first make a minimum closed loop for the "capable mid-train + post-train relay". The following scale is not recommended as a reference, but as a search space for starting ablation; different model sizes, pre-training histories, target language and product tasks will significantly change the best mix, and the main training must be validated by proxy scale and short-range master models. The following ratios and token compartments are used only for designing ablation variables and cannot be used as default mix, default LR or default budgets.

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

This starting point is not the composite formula for any open model, nor is it the optimal percentage to be rolled out from public reports. It is a search grid that allows new teams to expose data conflicts, forget risks and synthetic data boundaries.

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

This chapter is not an endnote to the literature summary, but a road map for readers to review the conclusions of this paper. The principles used are: the family of the same model first reads the latest version of the public technical report; the first version is completed at most; earlier material is retained only when it provides irreplaceable evidence and is marked “necessary exceptions” in the internal information package.

#12.1 One-hand technical report: Fact base

<unk> Information Level Use Level <unk> Original Priority Verification <unk> How to use this text
| --- | --- | --- | --- |
| Qwen3 Technical Report: <https://arxiv.org/abs/2505.09388> master reading <unk> pre-training, reading/context phase, extrapolation/deployment technology > capacitation
| DeepSeek-V3 Technical Report: <https://arxiv.org/abs/2412.19437> master reading; if similar details are disclosed in the new family report, replace <unk> 14.8T pre-training, 32K/128K context interpretation, structures and training synergy > long context extension must be seen with architecture, systems, training stability <unk>
| GLM-4.5 Technical Report: <https://arxiv.org/abs/2508.06471> > <unk> mid-training 3 subphases: repo-level code (~500B, 4K ~32K), synthetic reading (~500B), long-content + agent (~100B, lau 128K); MoE 355B/32B; ~1.1T mid-training tokens multi-stage mid-training engineering decomposition samples; synthetic reasoning and angent trajectory injections to Mid-train; MoE mid-train route/load reference <unk>
| Qwen2.5-1M Technical Report: <https://arxiv.org/abs/2501.15383> previous edition reserved: <unk> propressive long-content pre-training, post-training, DCA/YaRN, chunked prefilled training extension, 1M extrapolation and deployment of optimal boundaries
| OLMo 2 Technical Report: <https://arxiv.org/abs/2501.00656> <unk> Required exceptions <unk> Clear mid-training stratification, data mixing, micr-annealing, pot-training <unk> learning phase naming, data lineage and transparent laboratory accounts <unk>
| Phi-4 Technical Report: <https://arxiv.org/abs/2412.08905> <unk> synthetic data for pretraining and midtraining; 4K-> 16K context extension <unk> synthetic data governance, verefier, style diversity and organic data
| The Llama 3 Herd of Models: <https://arxiv.org/abs/2407.21783> <unk> ong_context pre-training, negotiating, andcheckpoint selection <unk> Read only when the details of the late-stange/ennealing are required to be published

Do not interpret this table as a "comprehensive list." If the team has the latest report from the target model family, it should replace the master sample; if the new report does not disclose the relevant details of Mid-training, the previous version or the necessary exception should be retained as an analogy to the engineering.

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
<unk> mid-training can independently manage <unk> 0/ 1/ 3/ 4.6 <unk> OLMo 2 for the express use of mid-training; Phi-4 uses pretraining/midtraining/post-training stratification; <unk> report facts + project synthesis; <unk> “The public report already contains a sample of the mid-training independence phase; the team can draw on its governance.”
<unk> Many cases are just mid-train-like <unk> 0/ 2/3 <unk> Qwen3, DeepSeek-V3, Llama 3, Qwen2.5-1M The original reporting terminology is strong: The report's facts: <unk> “This paper is similar in the sense of the project and does not rewrite the original reporting terminology.” <unk>
<unk> wen3 has General / Reasoning / Long Context three pre-training stage<unk> 3 / 12.1 <unk> Qwen3 Technical Report <unk> : report the facts of the fact that “Qwen3 called Pre-training State, not Mid-training.”
<unk> DeepSeek-V3 long-term context extension of the last two paragraphs of 14.8 T base pre-training 1000 steps <unk> <unk> <unk> <unk> DeepSeek-V3 Technical Report <unk> : report the fact that “support phase conversion; do not support reverse generic data mix.” <unk>
<unk> wen2.5-1M 's 1M capabilities are derived from training, post-training, extrapolation and deployment of co-ordinated <unk> 3/12.1<unk> Qwen2.5-1M Technical Report <unk> : report facts + Project Summary <unk> "not directly trained to 1M, nor is it purely a matter of reasoning."
Long-content and annealing of Llama 3 can be used as a reference for late-stay 3/12.1 <unk> Llama 3 Technical Report: report the fact that “405B size sample, not small team budget proposal.”
<unk> Synthetic data are valuable, but must be addressed for templateization, pollution and bugs in the teacher <unk> 3/ 4.2.2 / 12.1 <unk> Phi-4, Qwen3 and controlled studies related to the synthesis data <unk> Strong: report facts + thesis summed up <unk> "Synthetic data are verifiable capacity amplifiers, not low-cost token substitutes."
Reisoning Mid-training is more like raising the engineering hypothesis for RL substrate <unk> 2.4/ 3/ 6.6 <unk> PRISM, pre/mid/RL interplay paper <unk> Summary of the paper + To be authenticated assumption <unk> “need to be verified with team own paired RL/ SFT protocol.”
<unk> Public benchmark rise is not sufficient to prove the success of the Mid-train evaluation practice of multiple public reports + in this document project management <unk> : Project summary <unk> "It is necessary to look at private holdout, raw output, pollution and post-train rediness."
Public reports usually cannot give replicable recipe<unk> 4/ 11/12 <unk> a single-hand report that together reflects the incompleteness of key details in the public report: Project summary: <unk> “The table in this paper is a search of space and quality doors, not a re-engineer formula.” <unk>

#12.4 Recommended reading order

1. Read the latest report of the target model family first; if there is no target family, read Qwen3 and DeepSeek-V3.
2. Read Qwen2.5-1M only when doing 1M/super-long context.
3. Read OLMo 2 only when clear mid-training governance paradigm is required.
4. Read Phi-4 only when the composite data are the main variable.
5. Read Llama 3 only when the details are required to be disclosed.
6. Final reading of the papers on survey, PRISM and pre/mid/RL, transforming the institutional assumptions into their own ablation.

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

** A mature Mid-training project did not start as "training to run" but was able to answer before the first checkpoint came into existence: what the target was, what it was not to sacrifice, where the evidence was, who would determine whether it was going to continue or whether it was stopping.**

# Appendix: Use of boundary and updating principles

This paper can be used as an internal manual for the start-up of the Mid-Train project for the model team, but it is not a training formula or a repeat description of the public model.

<unk> dimension <unk> current state <unk> use <unk>
| --- | --- | --- |
The latest version of the same model family, at most the last one, the older version of which is only necessary exceptions, is reviewed before the latest report of the target model family is used, replacing the historical sample in this paper.
<unk> Factual qualification Distinguishing the facts of the report, the syntheses, the project syntheses and assumptions to be validated (chap. 12), updating the new report with the same matrix without directly adding the old model cases <unk>
Chapter 11 is a model for sensitization, LR or token bugt stubble, which requires internal validation before the amplification training is completed, pollution inspection, Holdout management and post-train pretcol
<unk> Risk control <unk> Data, training, eval, infra, capability, pot-train handoff 6 accidents <unk> Project landing is required to access team real training platforms, the eval system and model recovery
