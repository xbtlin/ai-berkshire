---
license: bigscience-bloom-rail-1.0
language:
- ak
- ar
- as
- bm
- bn
- ca
- code
- en
- es
- eu
- fon
- fr
- gu
- hi
- id
- ig
- ki
- kn
- lg
- ln
- ml
- mr
- ne
- nso
- ny
- or
- pa
- pt
- rn
- rw
- sn
- st
- sw
- ta
- te
- tn
- ts
- tum
- tw
- ur
- vi
- wo
- xh
- yo
- zh
- zu
programming_language: 
- C
- C++
- C#
- Go
- Java
- JavaScript
- Lua
- PHP
- Python
- Ruby
- Rust
- Scala
- TypeScript
pipeline_tag: text-generation
widget:
- text: 'A "whatpu" is a small, furry animal native to Tanzania. An example of a sentence that uses the word whatpu is: We were traveling in Africa and we saw these very cute whatpus. | To do a "farduddle" means to jump up and down really fast. An example of a sentence that uses the word farduddle is:'
  example_title: Imaginary word
  group: English
- text: 'Un "whatpu" est un petit animal à fourrure originaire de Tanzanie. Un exemple de phrase qui utilise le mot whatpu est: Nous étions en Afrique et nous avons vu des whatpus trop mignons. Faire un "farduddle" veut dire sauter sur place vraiment vite. Un exemple de phrase qui utilise le mot farduddle est:'
  example_title: Imaginary word
  group: French
- text: 'Un "whatpu" es un pequeño animal peludo nativo de Tanzania. Un ejemplo de una oración que usa la palabra whatpu es: Estábamos viajando por África y vimos estos whatpus muy bonitos. Hacer un "farduddle" significa saltar arriba y abajo muy rápido. Un ejemplo de una oración que usa la palabra farduddle es:'
  example_title: Imaginary word
  group: Spanish
- text: ' ال"واتبو" هو حيوان صغير مكسو بالفراء يعيش في تنزانيا. مثال على جملة تستخدم كلمة واتبو هي: كنا نسافر في افريقيا و رأينا هؤلاء الواتبو اللطفاء. للقيام ب"فاردادل" يعني ان تقفز للأعلى و الأسفل بسرعة كبيرة. مثال على جملة تستخدم كلمة فاردادل هي:'
  example_title: Imaginary word
  group: Arabic
- text: 'Um "whatpu" é um pequeno animal peludo nativo da Tanzânia. Um exemplo de uma frase que usa a palavra whatpu é: Estávamos a viajar por África e vimos uns whatpus muito queridos. Fazer um "farduddle" significa saltar para cima e para baixo muito rápido. Um exemplo de uma frase que usa a palavra farduddle é:'
  example : Imaginary word
  group: Portuguese
- text: Pour déguster un ortolan, il faut tout d'abord
  example_title: Recipe
  group: French
- text: |-
    34+10=44 
    54+20=
  example_title: Addition
  group: Math
- text: |-
    This tool converts irregular verbs to past tense.
    Arise - Arose
    Become - Became
    Forget - Forgot
    Freeze -
  example_title: Irregular verbs
  group: English
- text: |-
    Please unscramble the letters into a word, and write that word:
    r e!c.i p r o.c a/l = reciprocal
    d.o m i!n a n.t =
  example_title: Word unscrambling
  group: English
- text: |-
    Estos ejemplos quitan vocales de las palabras
    Ejemplos:
    hola - hl
    manzana - mnzn
    papas - pps
    alacran - lcrn
    papa -
  example_title: Vowel removal
  group: Spanish
- text: |-
    Traduce español de España a español de Argentina
    El coche es rojo - el auto es rojo
    El ordenador es nuevo - la computadora es nueva
    el boligrafo es negro - lapicera es negra
    la nevera
  example_title: Spanish to Argentinian Spanish
  group: Spanish
- text: To say "I love you" in Hindi, you would say
  example_title: Translation to Hindi
  group: English
- text: To say "I love you" in Hindi, you would say
  example_title: Translation from English
  group: Hindi
- text: 'Poor English: She no went to the market. Corrected English:'
  example_title: Grammar exercise 1 
  group: English
- text: 'استخراج العدد العاملي في لغة بايثون:'
  example_title: Code generation
  group: Arabic
- text: 'Regexp. Here is a regular expression to match a word starting with a number and then having only vowels:'
  example_title: Regular expressions
  group: English
- text: |-
    Do a hello world in different languages:
    Python: print("hello world")
    R:
  example_title: Code generation
  group: English
- text: |-
    Which is the correct preposition? I'm born X July. X is the preposition in
    He sat X a chair. X is the preposition on
    She drove X the bridge. X is the preposition
  example_title: Grammar exercise 2
  group: English
- text: |-
    Traduction en français: Dans cet essai je vais m'interroger sur la conscience des modèles d'intelligence artificielle récents comme les modèles de langue. Pour commencer, je m'intéresserai à la notion de conscience et à ce qui la caractérise. Ensuite, j'aborderai la question de l'intelligence et de son lien avec le langage. Enfin, dans une dernière partie je me pencherai sur le cas de l'IA et sur sa conscience.
    Traduction en espagnol:
  example_title: Translation to Spanish
  group: French
- text: |-
    Traducción al francés: Dans cet essai je vais m'interroger sur la conscience des modèles d'intelligence artificielle récents comme les modèles de langue. Pour commencer, je m'intéresserai à la notion de conscience et à ce qui la caractérise. Ensuite, j'aborderai la question de l'intelligence et de son lien avec le langage. Enfin, dans une dernière partie je me pencherai sur le cas de l'IA et sur sa conscience.
    Traducción al español:
  example_title: Translation from French
  group: Spanish
- text: ذات مرة ، عاش شبل الدب في الغابة
  example_title: Fairy tale
  group: Arabic
- text: एक बार की बात है, जंगल में एक भालू का शावक रहता था
  example_title: Fairy tale
  group: Hindi
- text: Il était une fois une licorne qui vivait
  example_title: Fairy tale
  group: French
- text: |-
    Q: A juggler can juggle 16 balls. Half of the balls are golf balls, and half of the golf balls are blue. How many blue golf balls are there?
    A: Let's think step by step.
  example_title: Mathematical reasoning
  group: English

co2_eq_emissions:
  emissions: 24700000
  source: "Estimating the Carbon Footprint of BLOOM, a 176B Parameter Language Model. https://arxiv.org/abs/2211.02001"
  training_type: "pre-training"
  geographical_location: "Orsay, France"
  hardware_used: "384 A100 80GB GPUs"

model-index:
- name: bloom
  results:
  - task:
      type: text-generation
    dataset:
      type: openai_humaneval
      name: humaneval
    metrics:
    - name: pass@1
      type: pass@1
      value: 0.15542682926829265
      verified: false
    - name: pass@10
      type: pass@10
      value: 0.3278356276947017
      verified: false
    - name: pass@100
      type: pass@100
      value: 0.5719815685597749
      verified: false
---

<img src="https://cdn-uploads.huggingface.co/production/uploads/1657124309515-5f17f0a0925b9863e28ad517.png" alt="BigScience Logo" width="800" style="margin-left:'auto' margin-right:'auto' display:'block'"/>

BigScience Large Open-science Open-access Multilingual Language Model  
Version 1.3 / 6 July 2022

Current Checkpoint: **Training Iteration  95000**

Link to paper: [here](https://arxiv.org/abs/2211.05100)

Total seen tokens: **366B**

---

# Model Details  

BLOOM is an autoregressive Large Language Model (LLM), trained to continue text from a prompt on vast amounts of text data using industrial-scale computational resources. As such, it is able to output coherent text in 46 languages and 13 programming languages that is hardly distinguishable from text written by humans. BLOOM can also be instructed to perform text tasks it hasn't been explicitly trained for, by casting them as text generation tasks.

## Basics
*This section provides information about the model type, version, license, funders, release date, developers, and contact information.*
*It is useful for anyone who wants to reference the model.*

<details>
<summary>Click to expand</summary>
  
**Developed by:** BigScience ([website](https://bigscience.huggingface.co))

*All collaborators are either volunteers or have an agreement with their employer. (Further breakdown of participants forthcoming.)*
    
**Model Type:** Transformer-based Language Model

**Checkpoints format:** `transformers` (Megatron-DeepSpeed format available [here](https://huggingface.co/bigscience/bloom-optimizer-states))

**Version:** 1.0.0

**Languages:** Multiple; see [training data](#training-data)

**License:** RAIL License v1.0 ([link](https://huggingface.co/spaces/bigscience/license) / [article and FAQ](https://bigscience.huggingface.co/blog/the-bigscience-rail-license))

**Release Date Estimate:** Monday, 11.July.2022

**Send Questions to:** bigscience-contact@googlegroups.com

**Cite as:** BigScience, _BigScience Language Open-science Open-access Multilingual (BLOOM) Language Model_. International, May 2021-May 2022

**Funded by:** 
    
* The French government.

* Hugging Face ([website](https://huggingface.co)).

* Organizations of contributors.  *(Further breakdown of organizations forthcoming.)*

</details>


## Technical Specifications
*This section includes details about the model objective and architecture, and the compute infrastructure.*
*It is useful for people interested in model development.*

<details>
<summary>Click to expand</summary>

Please see [the BLOOM training README](https://github.com/bigscience-workshop/bigscience/tree/master/train/tr11-176B-ml#readme) for full details on replicating training.

### Model Architecture and Objective

* Modified from Megatron-LM GPT2 (see [paper](https://arxiv.org/abs/1909.08053), [BLOOM Megatron code](https://github.com/bigscience-workshop/Megatron-DeepSpeed)):

* Decoder-only architecture

* Layer normalization applied to word embeddings layer (`StableEmbedding`; see [code](https://github.com/facebookresearch/bitsandbytes), [paper](https://arxiv.org/pdf/2110.02861.pdf))

* ALiBI positional encodings (see [paper](https://arxiv.org/pdf/2108.12409.pdf)), with GeLU activation functions

* 176,247,271,424 parameters:

    * 3,596,615,680 embedding parameters

    * 70 layers, 112 attention heads

    * Hidden layers are 14336-dimensional

    * Sequence length of 2048 tokens used (see [BLOOM tokenizer](https://huggingface.co/bigscience/tokenizer), [tokenizer description](#tokenization))

**Objective Function:** Cross Entropy with mean reduction (see [API documentation](https://pytorch.org/docs/stable/generated/torch.nn.CrossEntropyLoss.html#torch.nn.CrossEntropyLoss)).
    
### Compute infrastructure
Jean Zay Public Supercomputer, provided by the French government (see [announcement](https://www.enseignementsup-recherche.gouv.fr/fr/signature-du-marche-d-acquisition-de-l-un-des-supercalculateurs-les-plus-puissants-d-europe-46733)).

#### Hardware

* 384 A100 80GB GPUs (48 nodes)
    
* Additional 32 A100 80GB GPUs (4 nodes) in reserve

* 8 GPUs per node Using NVLink 4 inter-gpu connects, 4 OmniPath links

* CPU: AMD

* CPU memory: 512GB per node

* GPU memory: 640GB per node

* Inter-node connect: Omni-Path Architecture (OPA)

* NCCL-communications network: a fully dedicated subnet

* Disc IO network: shared network with other types of nodes

#### Software

* Megatron-DeepSpeed ([Github link](https://github.com/bigscience-workshop/Megatron-DeepSpeed))

* DeepSpeed ([Github link](https://github.com/microsoft/DeepSpeed))

* PyTorch (pytorch-1.11 w/ CUDA-11.5; see [Github link](https://github.com/pytorch/pytorch))

* apex ([Github link](https://github.com/NVIDIA/apex))
    
</details>

---

# Training
*This section provides information about the training data, the speed and size of training elements, and the environmental impact of training.*
*It is useful for people who want to learn more about the model inputs and training footprint.*

<details>
<summary>Click to expand</summary>

## Training Data
*This section provides a high-level overview of the training data. It is relevant for anyone who wants to know the basics of what the model is learning.*

Details for each dataset are provided in individual [Data Cards](https://huggingface.co/spaces/bigscience/BigScienceCorpus), and the sizes of each of their contributions to the aggregated training data are presented in an [Interactive Corpus Map](https://huggingface.co/spaces/bigscience-catalogue-lm-data/corpus-map).

Training data includes:

-   46 natural languages
    
-   13 programming languages

-   In 1.6TB of pre-processed text, converted into 350B unique tokens (see [the tokenizer section](#tokenization) for more.)

### Languages
    
The pie chart shows the distribution of languages in training data.
   
![pie chart showing the distribution of languages in training data](https://github.com/bigscience-workshop/model_card/blob/main/assets/data/pie_v2.svg?raw=true)


The following tables shows the further distribution of Niger-Congo & Indic languages and programming languages in the training data.

Distribution of Niger Congo and Indic languages.
    
| Niger Congo    | Percentage |         | Indic     | Percentage |
|----------------|------------| ------  |-----------|------------|
| Chi Tumbuka    | 0.00002    |         | Assamese  | 0.01       |
| Kikuyu         | 0.00004    |         | Odia      | 0.04       |
| Bambara        | 0.00004    |         | Gujarati  | 0.04       |
| Akan           | 0.00007    |         | Marathi   | 0.05       |
| Xitsonga       | 0.00007    |         | Punjabi   | 0.05       |
| Sesotho        | 0.00007    |         | Kannada   | 0.06       |
| Chi Chewa      | 0.0001     |         | Nepali    | 0.07       |
| Setswana       | 0.0002     |         | Telugu    | 0.09       |
| Lingala        | 0.0002     |         | Malayalam | 0.10       |
| Northern Sotho | 0.0002     |         | Urdu      | 0.10       |
| Fon            | 0.0002     |         | Tamil     | 0.20       |
| Kirundi        | 0.0003     |         | Bengali   | 0.50       |
| Wolof          | 0.0004     |         | Hindi     | 0.70       |
| Luganda        | 0.0004     |
| Chi Shona      | 0.001      |
| Isi Zulu       | 0.001      |
| Igbo           | 0.001      |
| Xhosa          | 0.001      |
| Kinyarwanda    | 0.003      |
| Yoruba         | 0.006      |
| Swahili        | 0.02       |

Distribution of programming languages.
    
| Extension      | Language   | Number of files |
|----------------|------------|-----------------|
| java           | Java       | 5,407,724       |
| php            | PHP        | 4,942,186       |
| cpp            | C++        | 2,503,930       |
| py             | Python     | 2,435,072       |
| js             | JavaScript | 1,905,518       |
| cs             | C#         | 1,577,347       |
| rb             | Ruby       | 6,78,413        |
| cc             | C++        | 443,054         |
| hpp            | C++        | 391,048         |
| lua            | Lua        | 352,317         |
| go             | GO         | 227,763         |
| ts             | TypeScript | 195,254         |
| C              | C          | 134,537         |
| scala          | Scala      | 92,052          |
| hh             | C++        | 67,161          |
| H              | C++        | 55,899          |
| tsx            | TypeScript | 33,107          |
| rs             | Rust       | 29,693          |
| phpt           | PHP        | 9,702           |
| c++            | C++        | 1,342           |
| h++            | C++        | 791             |
| php3           | PHP        | 540             |
| phps           | PHP        | 270             |
| php5           | PHP        | 166             |
| php4           | PHP        | 29              |
    
### Preprocessing

**Tokenization:** The BLOOM tokenizer ([link](https://huggingface.co/bigscience/tokenizer)), a learned subword tokenizer trained using:
    
- A byte-level Byte Pair Encoding (BPE) algorithm 

- A simple pre-tokenization rule, no normalization

- A vocabulary size of 250,680

It was trained on a subset of a preliminary version of the corpus using alpha-weighting per language.  

## Speeds, Sizes, Times

Training logs: [Tensorboard link](https://huggingface.co/tensorboard/bigscience/tr11-176B-ml-logs/)

- Dates:
    
    - Started 11th March, 2022 11:42am PST

    - Estimated end: 5th July, 2022

- Checkpoint size:
    
    - Bf16 weights: 329GB
    
    - Full checkpoint with optimizer states: 2.3TB

- Training throughput: About 150 TFLOP per GPU per second

- Number of epochs: 1

- Estimated cost of training: Equivalent of $2-5M in cloud computing (including preliminary experiments)

- Server training location: Île-de-France, France


## Environmental Impact

The training supercomputer, Jean Zay ([website](http://www.idris.fr/eng/jean-zay/jean-zay-presentation-eng.html)), uses mostly nuclear energy. The heat generated by it is reused for heating campus housing.
    
**Estimated carbon emissions:**  *(Forthcoming.)*
    
**Estimated electricity usage:** *(Forthcoming.)*

</details>

---

# Uses

*This section addresses questions around how the model is intended to be used, discusses the foreseeable users of the model (including those affected by the model), and describes uses that are considered out of scope or misuse of the model.*
*It is useful for anyone considering using the model or who is affected by the model.*

<details>
<summary>Click to expand</summary>
    
## How to use

This model can be easily used and deployed using HuggingFace's ecosystem. This needs `transformers` and `accelerate` installed. The model can be downloaded as follows:

 <img src="https://s3.amazonaws.com/moonup/production/uploads/1657271608456-62441d1d9fdefb55a0b7d12c.png" width="800" style="margin-left:'auto' margin-right:'auto' display:'block'"/>

## Intended Use

This model is being created in order to enable public research on large language models (LLMs). LLMs are intended to be used for language generation or as a pretrained base model that can be further fine-tuned for specific tasks. Use cases below are not exhaustive.

### Direct Use

-   Text generation

-   Exploring characteristics of language generated by a language model

    -   Examples: Cloze tests, counterfactuals, generations with reframings

### Downstream Use

-   Tasks that leverage language models include: Information Extraction, Question Answering, Summarization

### Misuse and Out-of-scope Use
*This section addresses what users ought not do with the model.*

See the [BLOOM License](https://huggingface.co/spaces/bigscience/license), Attachment A, for detailed usage restrictions. The below list is non-exhaustive, but lists some easily foreseeable problematic use cases.

#### Out-of-scope Uses

Using the model in [high-stakes](#high-stakes) settings is out of scope for this model.  The model is not designed for [critical decisions](#critical-decisions) nor uses with any material consequences on an individual's livelihood or wellbeing. The model outputs content that appears factual but may not be correct.  

Out-of-scope Uses Include:

-   Usage in biomedical domains, political and legal domains, or finance domains

-   Usage for evaluating or scoring individuals, such as for employment, education, or credit

-   Applying the model for critical automatic decisions, generating factual content, creating reliable summaries, or generating predictions that must be correct

#### Misuse

Intentionally using the model for harm, violating [human rights](#human-rights), or other kinds of malicious activities, is a misuse of this model. This includes:

-   Spam generation

-   Disinformation and influence operations

-   Disparagement and defamation

-   Harassment and abuse
  
-   [Deception](#deception)

-   Unconsented impersonation and imitation

-   Unconsented surveillance 

-   Generating content without attribution to the model, as specified in the [RAIL License, Use Restrictions](https://huggingface.co/spaces/bigscience/license)

## Intended Users

### Direct Users

-   General Public

-   Researchers

-   Students

-   Educators

-   Engineers/developers

-   Non-commercial entities

-   Community advocates, including human and civil rights groups

### Indirect Users

-   Users of derivatives created by Direct Users, such as those using software with an [intended use](#intended-use)

-   Users of [Derivatives of the Model, as described in the License](https://huggingface.co/spaces/bigscience/license)

### Others Affected (Parties Prenantes)

-   People and groups referred to by the LLM

-   People and groups exposed to outputs of, or decisions based on, the LLM

-   People and groups whose original work is included in the LLM

</details>

---

# Risks and Limitations
*This section identifies foreseeable harms and misunderstandings.*
    
<details>
<summary>Click to expand</summary>

Model may:

-   Overrepresent some viewpoints and underrepresent others

-   Contain stereotypes
  
-   Contain [personal information](#personal-data-and-information)

-   Generate:

    -   Hateful, abusive, or violent language

    -   Discriminatory or prejudicial language

    -   Content that may not be appropriate for all settings, including sexual content

-   Make errors, including producing incorrect information as if it were factual

-   Generate irrelevant or repetitive outputs

-   Induce users into attributing human traits to it, such as sentience or consciousness

</details>

---

# Evaluation
*This section describes the evaluation protocols and provides the results.*


<details>
<summary>Click to expand</summary>

## Metrics 
*This section describes the different ways performance is calculated and why.*

Includes:

| Metric             | Why chosen                                                         |
|--------------------|--------------------------------------------------------------------|
| [Perplexity](#perplexity)         | Standard metric for quantifying model improvements during training |
| Cross Entropy [Loss](#loss) | Standard objective for language models.                            |

And multiple different metrics for specific tasks. _(More evaluation metrics forthcoming upon completion of evaluation protocol.)_

## Factors 
*This section lists some different aspects of BLOOM models. Its focus is on aspects that are likely to give rise to high variance in model behavior.*

- Language, such as English or Yoruba

- Domain, such as newswire or stories

- Demographic characteristics, such as gender or nationality

##  Results
*Results are based on the [Factors](#factors) and [Metrics](#metrics).*

**Zero-shot evaluations:**

<span style="color:red"><b>WARNING:</b> This section used to contain much more results, however they were not correct and we released without the approval of the evaluation working group. We are currently in the process of fixing the evaluations.</span>

See this repository for JSON files: https://github.com/bigscience-workshop/evaluation-results

| Task | Language | Metric | BLOOM-176B | OPT-175B* |
|:--------|:-----------------|:------------------------|-------------:|------------:|
| humaneval | python | pass@1 ↑ | 0.155 | 0.0 |
| humaneval | python | pass@10 ↑ | 0.328 | 0.0 |
| humaneval | python | pass@100 ↑ | 0.572 | 0.003 |


**Train-time Evaluation:**

Final checkpoint after 95K steps:

- Training Loss: 1.939

- Validation Loss: 2.061

- Perplexity: 7.045

For more see: https://huggingface.co/bigscience/tr11-176B-ml-logs

</details>

---

# Recommendations

*This section provides information on warnings and potential mitigations.*

<details>
<summary>Click to expand</summary>

-   Indirect users should be made aware when the content they're working with is created by the LLM.

-   Users should be aware of [Risks and Limitations](#risks-and-limitations), and include an appropriate age disclaimer or blocking interface as necessary.

-   Models trained or finetuned downstream of BLOOM LM should include an updated Model Card.

-   Users of the model should provide mechanisms for those affected to provide feedback, such as an email address for comments.

</details>

---

# Glossary and Calculations

*This section defines common terms and how metrics are calculated.*
<details>
<summary>Click to expand</summary>

-   <a name="loss">**Loss:**</a> A calculation of the difference between what the model has learned and what the data shows ("groundtruth"). The lower the loss, the better. The training process aims to minimize the loss. 

-   <a name="perplexity">**Perplexity:**</a> This is based on what the model estimates the probability of new data is. The lower the perplexity, the better.  If the model is 100% correct at predicting the next token it will see, then the perplexity is 1. Mathematically this is calculated using entropy. 

-   <a name="high-stakes">**High-stakes settings:**</a> Such as those identified as "high-risk AI systems" and "unacceptable risk AI systems" in the European Union's proposed [Artificial Intelligence (AI) Act](https://artificialintelligenceact.eu/annexes/).

-   <a name="critical-decisions">**Critical decisions:**</a> Such as those defined in [the United States' proposed Algorithmic Accountability Act](https://www.congress.gov/117/bills/s3572/BILLS-117s3572is.pdf).

-   <a name="human-rights">**Human rights:**</a> Includes those rights defined in the [Universal Declaration of Human Rights](https://www.un.org/sites/un2.un.org/files/2021/03/udhr.pdf).

-  <a name="personal-data-and-information">**Personal Data and Personal Information:**</a> Personal data and information is defined in multiple data protection regulations, such as "[personal data](https://gdpr-info.eu/issues/personal-data/)" in the [European Union's General Data Protection Regulation](https://gdpr-info.eu); and "personal information" in the Republic of South Africa's [Protection of Personal Information Act](https://www.gov.za/sites/default/files/gcis_document/201409/3706726-11act4of2013popi.pdf), The People's Republic of China's [Personal information protection law](http://en.npc.gov.cn.cdurl.cn/2021-12/29/c_694559.htm).
  
- <a name="sensitive-characteristics">**Sensitive characteristics:**</a> This includes specifically protected categories in human rights (see [UHDR, Article 2](https://www.un.org/sites/un2.un.org/files/2021/03/udhr.pdf)) and personal information regulation (see GDPR, [Article 9; Protection of Personal Information Act, Chapter 1](https://www.gov.za/sites/default/files/gcis_document/201409/3706726-11act4of2013popi.pdf))

- <a name="deception">**Deception:**</a> Doing something to intentionally mislead individuals to believe something that is false, such as by creating deadbots or chatbots on social media posing as real people, or generating text documents without making consumers aware that the text is machine generated.

</details>

---

# More Information
*This section provides links to writing on dataset creation, technical specifications, lessons learned, and initial results.*

<details>
<summary>Click to expand</summary>

## Intermediate checkpoints

For academic (or any) usage, we published the intermediate checkpoints, corresponding to the model state at each 5000 steps. Please follow [this link](https://huggingface.co/bigscience/bloom-176-intermediate) to get these checkpoints.

    
## Dataset Creation

Blog post detailing the design choices during the dataset creation: https://bigscience.huggingface.co/blog/building-a-tb-scale-multilingual-dataset-for-language-modeling

## Technical Specifications

Blog post summarizing how the architecture, size, shape, and pre-training duration where selected: https://bigscience.huggingface.co/blog/what-language-model-to-train-if-you-have-two-million-gpu-hours

More details on the architecture/optimizer: https://github.com/bigscience-workshop/bigscience/tree/master/train/tr11-176B-ml

Blog post on the hardware/engineering side: https://bigscience.huggingface.co/blog/which-hardware-to-train-a-176b-parameters-model

Details on the distributed setup used for the training: https://github.com/bigscience-workshop/bigscience/tree/master/train/tr11-176B-ml

Tensorboard updated during the training: https://huggingface.co/bigscience/tr11-176B-ml-logs/tensorboard#scalars&tagFilter=loss

## Lessons

Insights on how to approach training, negative results: https://github.com/bigscience-workshop/bigscience/blob/master/train/lessons-learned.md

Details on the obstacles overcome during the preparation on the engineering side (instabilities, optimization of training throughput, so many technical tricks and questions): https://github.com/bigscience-workshop/bigscience/blob/master/train/tr11-176B-ml/chronicles.md

## Initial Results

Initial prompting experiments using interim checkpoints: https://huggingface.co/spaces/bigscience/bloom-book

</details>


## Original checkpoints

The checkpoints in this repo correspond to the HuggingFace Transformers format. If you want to use our fork of [Megatron-DeepSpeed](https://github.com/bigscience-workshop/Megatron-DeepSpeed) that the model was trained with, you'd want to use [this repo instead](https://huggingface.co/bigscience/bloom-optimizer-states).

Many intermediate checkpoints are available at https://huggingface.co/bigscience/bloom-intermediate/

---
    
# Model Card Authors
*Ordered roughly chronologically and by amount of time spent on creating this model card.*

Margaret Mitchell, Giada Pistilli, Yacine Jernite, Ezinwanne Ozoani, Marissa Gerchick, Nazneen Rajani, Sasha Luccioni, Irene Solaiman, Maraim Masoud, Somaieh Nikpoor, Carlos Muñoz Ferrandis, Stas Bekman, Christopher Akiki, Danish Contractor, David Lansky, Angelina McMillan-Major, Tristan Thrush, Suzana Ilić, Gérard Dupont, Shayne Longpre, Manan Dey, Stella Biderman, Douwe Kiela, Emi Baylor, Teven Le Scao, Aaron Gokaslan, Julien Launay, Niklas Muennighoff