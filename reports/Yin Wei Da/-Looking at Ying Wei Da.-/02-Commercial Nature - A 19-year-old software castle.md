# A 19-year-old software castle

> Understanding Inveida Series 02 Business Nature
> Read about 12 minutes

---

# What is the real thing that Yvettedha sells?

One detail is telling: the data centre manager at Caltech says** "Professors prefer 18 months to wait for the British Weida chip, and not to replace it with another supplier."** Wait a year and a half instead of moving to a competitive spot that is more abundant and less expensive.

This is not brand loyalty, it is migration costs too much to bear. It is not a shovel. ** It is a whole range of mining systems: shovels + mine trucks + mine lanes + operation manual + training school ** - in industry terms: **GPU chip + NVLink interconnectivity network + CUDA framework integration + business services. ** You can change shovels, but you can't move the four remaining ones.

At the heart of this system is the CUDA.

---

# What's the moat of the moat?

# An inaccurate but useful analogy

To interpret the CUDA as "GPU World Windows".

Microsoft Windows' moat is not working on the system itself -- Linux is better than Windows. Windows moat is about the millions of applications accumulated over decades, billions of users' habits, and the depth of the global enterprise IT system. You can create better operating systems, but you can't move the ecology.

The same is true of the CUDA. Its moat is not in a single technology point, but in **19 (2006-2026), the systematic input of the five layers of ecology is built **:

Level, level, content, key numbers, key numbers, key numbers, key numbers, key numbers, key numbers, key numbers, key numbers, key elements, and the key elements of the system.
|------|---------|---------|
<unk> Layer 1: Hardware abstract <unk> CUDA Driver / Runtime (symmetric development with British Weddge) <unk> GPU per generation
<unk> Layer 2: Core Mathematics Library <unk> cudNN (**100,000 lines** manual optimization code), cublas, NCCL, TensorRT <unk> AMD MIOPEN ** 30-50%**
<unk> Level 3: Field library <unk> cudf, cuML, cuQuantum, RAPIDS, Modulus, Isaac<unk> AMD** almost zero coverage**
<unk> Level 4: Frame layer <unk> PyTorch / JAX / vLLLM Default CUDA priority <unk> ROCm is a second-class citizen, behind ** 6-12 months**
<unk> Layer 5: Applied layers <unk> Huggingface, TensorRT-LLLM, Stable Diffusion, ComfyUI <unk> 80%** Mainstream model partially supports AMD <unk>

> Data source: British Weibo Network, ThunderCompute 2026 Assessment, PyTorch Community

** The moat = 5 layers multiplied, not 5 layers. ** There is not enough to break any layer -- it takes to break 5 layers simultaneously to actually replace the CUDA. That is why AMD has been a ROCm for 10 years, and still is a "cUDA replacement" instead of "cUDA replacement".

# Three deep moats

Of the 5 layers, 3 are the hardest to break:

**1. TensorRT-LLLM (Extension Optimization Engine)**

The engine of reasoning optimization in the British State allows the same GPU to run faster than naked **3-10 times ** reasoning performance. The AMD has no right-in-one product.

Actual data: H100 runs from NIM container (based on TensorRT-LLM) Llama 3.1 8B, throughput **1,201 tokens/s**, running naked PyTorch only 613 tokens/s ** same hardware, software 2 times **.

**2. NCCL (Hanca Cluster Communication Library)**

The front-line model for training GPT-5, Claude 4 requires tens of thousands of GPUs to work together. NCCL is a cluster communications bank in British Weida, which works with the NVLink and InfoBand networks, faster than the CCCL for AMD than all-reduce communications **30% **.

This is not a gap that can be "rapidly catch up" -- Meta's paper shows that the failure detection and recovery of 100,000-carat training clusters takes 3 minute response time, and this system-level optimization takes years of engineering accumulation.

**3. CudNN (Core language of in-depth learning)**

Each generation of GPU releases, the cudnn team does a cache level for the chip, a warp scheduler, a tensor core** manual optimization, ** by using hardware to 90%+limits. The English version of the V2/v3 is usually 6-12 months ** earlier than the AMD version.

---

# Why did Huang In-hoon say, "Someone else's chips are worth more than any other girl in England."

That sounds preposterous, but it's supported by data.

** Core logic**: Chip cost is only part of the total AI infrastructure cost. The larger cost is: software fit, clustering, training of personnel, migration risks.

♪ Cost item ♪
|--------|---------|--------------|
<unk> Chip price <unk> $30-50 K/Plus (B200) <unk> $10-15 K/Plus (MI300X) <unk>
<unk> Software fit-out <unk> Zero cost (CUDA original) <unk> Several months of engineer time <unk>
<unk> Performance loss <unk> Benchmark 100% <unk> Naked run about 70-85% (need extra optimization) <unk>
<unk> Cluster communication <unk> NCCL + NVLink (manufacturing) <unk> RCCL + Infinity Fabric (kcal level authentication) <unk>
<unk> Transport risk <unk> Industry standards, faulty maturity <unk> New platform, few production environment cases <unk>
** TCO (total cost of ownership)** Baseline** ** Potentially higher** (Provincial chip but cost-effective) <unk>

** Reverse view**: This logic is established for universities and start-ups, but not necessarily for companies like AWS, Google, Microsoft, which have thousands of chip engineers.

---

# The moat is breaking up # # and it's not falling

# Crack 1: AI programming tool to cause the cost of code migration to collapse

In January 2026, a developer used Claude Code ** to transplant the CUDA backend to the AMD platform** in 30 minutes, without relying on any intermediate translation tool, with less than 10 per cent performance loss.

This was impossible in 2023. The CUDA migration to ROCm took months.

The AI programming tool is rapidly weakening the CUDA "code lock" layer:

Time, AI programming capability, CUDA migration costs,
|------|-----------|-------------|
<unk> 2023 <unk> only write base code <unk> team + months <unk>
<unk> 2025 <unk> <unk> <unk> 1-2 + weeks <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk> <unk>
<unk> 2026 <unk> port to end CUDA backend <unk> 1 + hours** <unk>

> Data source: Techstrange.ai, CASS dissertation (95% source translation accuracy), ThunderCompute evaluation

** But the moat doesn't collapse overnight** -- 30 minutes to transplant a simple Kernel. Complex cluster communication code, a highly optimal reasoning engine, a vanka-level system that is now out of reach of AI tools.

# Crack 2: ROCm gap from 3 to 30%

Year <unk> ROCm vs CUDA performance gap (calculating intensive tasks) <unk>
|------|--------------------------------------|
<unk> 2023 ** 2-3 times** <unk>
** 10-30%**

> Data source: TunderCompute Independent Evaluation, April 2026

The AMD ROCm 7.0 strategy clearly states "tighter alignment with the CUDA semantics" - it systematically narrows the gap.

# Crack 3: Triton compiler to build the escape tunnel

OpenAI's open source Triton compiler (version 3.6.0, released January 2026) already supports the AMD backend. PyTorch's TorchInductor compiler is also pushing the "rearless" programming paradigm - the developers write a code that automatically matches different chips.

** This means**: future AI developers may no longer need to write directly about CUDA -- they write Python/Triton, and the compiler automatically generates the bottom code. If this road goes through, CUDA's "code lock" will be fundamentally bypassed.

# But the moat is far from falling

** Still strong part**:

The moat level, the moat, the moist state, the moustache, the moustache.
|-----------|------|------|
<unk> TensorRT-LLMM Extremely reasoned optimization <unk> solid**<unk> 3-10 times, AMD unmatched
NCCL Combining <unk> solid** <unk> 100,000cal level training no substitute <unk>
<unk> cudnn per generation manual optimization <unk> solid** <unk> need to sync with hardware, AMD lags 6-12
NVLink / NVSwitch Interlink <unk> solid** <unk> 72 GPU Full Link (NVL72), with no match between the competitions
<unk> The new algorithm is first released <unk> solid** <unk> FlashAttention <unk>
<unk> AI programming reverse flyer<unk> ** solid** <unk> Internet 99% GPU code is CUDA, AI writing CUDA is easier to write than ROCm

** Part being eroded**:

The moat level, the moat, the moist state, the moustache, the moustache.
|-----------|------|------|
<unk> Base CUDA code migration threshold <unk> ** has been significantly weakened** <unk> AI tool + Triton + HIPCIFY <unk>
<unk> PyTorch's default reliance on CUDA <unk> **Lessing** <unk> TorchInductor supports multiple backends
<unk> The CUDA of the simple reasoning scene locks <unk> ** have largely disappeared ** <unk> AMD MI355X TCO has partly turned back <unk>

---

# The moat is changing -- from "soft locking" to "full-storage factory"

A more precise judgement is that the CUDA moat is not "disappearing", but in **deformation**.

The time, the moat form, the core barrier, the core barrier, the core, the core, the core, the core, the core, the core, the core, the core, the core, the core, the core, the core, the core, the core, the core, the core, the core, the core, the core, the core, the core, the core, the core, the core, the core, the core, the core, the core, the core, the core, the core, the core, the core, the core, the core, the core, the core, the core, the core, the core, the core, the core, the core, the core, the core, the core, the core, the core, the core, the core, the other.
|------|-----------|---------|
<unk> 2006-2020 <unk> CUDA software locking <unk> code migration costs are extremely high <unk>
<unk> 202025 <unk> CUDA+ Whole-Stock Integration <unk> GPU+NVLink+Software + Network <unk>
<unk> 2025-2030 (projection) <unk> All-in-house AI factory <unk> Hardware intergenerational lead + NVL72/576 System-level sales + services + services

Yin Wei-Da used to make money by "your code is locked down by the CUDA and you can't go." The future's making money by "my whole system is two to three times better than yours." You don't want to go.

The former is **-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

** Counterpart **: The strategy of the All-Buy AI factory means that British Wedder needs to invest $15 billion a year in research and development to sustain intergenerational leadership. Once a generation of products (such as Rubin Ultra) is delayed or under-performing, the moat may quickly narrow. This is a battle that requires "winning every year" -- unlike a mansion, it will not be shallow.

---

# A core question from the end of Yongping

In his April 2024 snowball speech, Yongping Tsang said a crucial thing:

"What I don't understand at this point is: ** How long can their monopoly last? How long can the need for the British Weida chip last? ** It's hard to do it if it's not clear. Nothing makes sense if it doesn't.

Two years later (2025 Q4), Yongping added Yingping to the group **7.7%** (the third largest warehouse), but never exceeded 10%. He explained later:

"Not exactly, but it does feel a little bit NVDA moundy. Look at this. It's a good company. Buying is probably a good money."

"I accept the yellow word that the DeepSeek innovation will not reduce the view of the need for arithmetic, and understand broadly what he thinks is that the NVDA's position in terms of arithmetic will not be threatened."

** The attitude of the Eternity is that good companies, the moats have a certain depth but do not understand for 10 years - below medium position, without heavy effort.**

This is a very disciplined decision-making framework:** acknowledging that it is not fully understood but willing to participate in the management of the warehouse.**

---

# This conclusion

♪ Judgements, conclusions, conclusions ♪
|------|------|
♪ Deep, but being eroded from the top ♪
<unk> Erosion speed? <unk> Code locking layer ** significant weakening in 2-3 years**; system level (Hank + extreme optimization)** 5-10 years still solid** <unk>
<unk> Not disappear, but it's deformed** -- from "soft locking" to "full-store competitiveness."
<unk> Impact on valuation? ** The probability of structural downward shifts in the Māori ratio** (75% <unk> 65-70%) is increasing

---

# Next week's forecast

Next, we enter the AI's most structural changes in the computing market -- ** training vs. the division of reasoning**.

In 2026, the reasoning factor had taken over two thirds of AI's total power. The reasoning market and the training market rules were completely different -- training for "excellent" and "price for sex". What does that mean for British Wedda?

A few questions to answer:

- Why is the market the most vulnerable battleground in England?
- Groq, Cerebras, why are these special reasoning chips important?
- What does it mean to buy a Groq from Yvette?
- The reasoned share is down from 75% to 50% -- how much more can we make?

---

* This is the text of the 02nd in the series Reading Weida.*
* This series does not constitute any investment proposal.*
