# Wetweet Public: Author-editor-reader of the three Agents

Three Agents are responsible for their work: authors write first drafts of in-depth studies, edit structures and expressions, and readers read them from the perspective of their target audience.

** Support input format**: thematic description, e.g. `Major Model OPD Technical Interpretation ' , `Qwen3 Technical Report Interpretation ' , `Why Barfitt does not buy the Science and Technology Unit '

---

# Designing ideas

A good article on the public is about three dimensions:
** Depth** - For those who can afford to read it over time (author's responsibility)
** Readability** - well structured, well-paced and non-resuasional (editor responsible)
** Can really read** — target readers will not give up (readers are responsible)

It's easy to write "hidden" in one person -- people who feel it's clear that the one who reads doesn't understand. The essence of the three Agent collaborations is that ** forced external perspectives**.

---

# Phase I: Research and material collection

# Step one: clear placement of articles

Before writing starts, the following information is confirmed (if not specified by the user), ask it on its own initiative:

<unk> dimension <unk> Confirmation is required <unk> default value <unk>
|------|---------|--------|
** Target reader** <unk> Technical background <unk> Technical background <unk>
**Extraction depth** <unk> Cope/medium depth/hard core <unk>
** Length of article** <unk> Word range <unk> 3000-4,000
** Whether the original paper/information** needs to be downloaded
<unk> Writing style** <unk> Official/dialogue/intelligence <unk> Dialogue style (like for smart friends) <unk>

# Step 2: Deep study

Launch of 2-3 studies with Agent tools** in parallel** to collect sufficient material:

** Study of Agent A: core content**
- If read in papers: downloading papers PDF, extracting core contributions, key graphs, experimental results
- If it is a technical subject: search for updates, key papers, technical details
- If it is a business/investment theme: search for up-to-date data, industry reports, competition patterns

** Study of Agent B: industry background and applications**
- Search for industry landings of the technology/theme
- Which companies are working? How's it working?
- Recent trends and milestones

** Study Agent C (optional): Competing/comparison study**
- Comparison of the same method/product
- History.
- The way forward.

# Step three: collating the material frame

After all of the studies of Agent were completed, it was organized:
1. ** Core arguments** (core message to be conveyed in one summary article)
2. ** Key data** (3-5 most powerful data points)
3. ** List of maps** (what maps are needed, what sources)
4. **The articles outline** (6-8 titles and core content of chapters)

---

# Phase two: author Agent writes the first draft

Starts with the Agent tool** author Agent**, giving detailed writing instructions.

# # Author of Agent's Prompt Template

```
You are a deep-tech writer who needs to write a micro-public article.

# Target audience
{\i1 \cH30D3F4}Approach the reader according to the first step

# Writing style requires
- Expressed in Chinese and avoided the Chinese-English mixture (technical terms given to English when first appeared, followed by Chinese)
- Like a tech-cop for a smart friend, not an academic thesis.
- Help with analogies, but they're good, they're not so common.
- Key formula/data, but every one in plain language.
- No, no, no, no, no, no, no, no, no, no, no, no, no, no, no, no, no, no, no, no, no, no, no, no, no, no, no, no, no, no.
- Paragraph does not exceed 4 lines (public reading environment)

# Core
♪ The data, the arguments ♪

# Article structure requirements
** At the beginning (first paragraph 3)**: There must be a strong hook - opening with a data shock or counter-intuitive conclusion, not a mild analogy
2. ** Background**: Why is this important? What is the solution?
3. ** Core content (2-3)**: The depth of technology is reflected here, but each point of technology requires a "black translation"
4. ** Empirical/case**: talk with data and cases, no talk
5. **Industry impact/prospects**: what does this mean for industry
6. ** End**: A powerful passivity of the frame, suitable for cross-reference

# The map requires
- Arts in the paper reading: the original drawings must be drawn from the paper PDF and used directly `!
- Extract method: render PDF page to high resolution PNG (at least 900 DPI) with pdftopm, and PIL customized target chart range
- Every picture is not less than 500 kB. Make sure it's high.
- The picture is stored in a single collection under `assets/{themes short}/ `aggregates'
- Non-symbol articles: search and download appropriate pictures if necessary, also directly insert

# Formula requires
- All mathematical formulae in LaTeX format: line-inline `$...$ ', stand-alone formulae `$...$...$ '
- Disable formulae in plain text (e. g. `> D_KL(P<unk> )=... ') and must be in LaTeX rendering format
- Each formula still has to be accompanied by a "black translation."

Please write a full draft of the article, about {target word}.
```

# When the author Agent is finished

Check whether the initial document is generated and read in full to confirm the integrity of the content.

---

# Phase III: Edit Agent+ Reader Agent

After the first draft is completed, the editor Agent and the reader Agent are activated in the same message** using the Agent tool.

# # Edit Agent's Prompt Template

```
You are a senior public editor (Editor Agent).

# Reviewing standards
1. ** Title**: Does it attract a click in the circle of friends? Will it be cut off (over 30 words)?
2. ** At the beginning**: Can the first three paragraphs be kept open? Is the hook strong enough?
3. ** Structure**: Is the logical chain fluid? Is there a leap or a fault?
4. **The depth-readability balance**: Is the formula/technical part really popular? Is there a "pretence of generality but not clear explanation"?
** Rhythm**: Is there too long a paragraph? Is the length of each section appropriate?
** Chart**: Has the picture actually been inserted (non-placeholder)? Does the location appear when the reader most needs visual aids?
7. ** End**: Is there a capacity for communication? Would the reader want to transmit it after reading it?

# Text of article
{complete draft}

# Output format
1. Overall evaluation (3-5 sentences)
2. Proposed title changes (for 2-3 options)
3. Section by section (specify the "recommended" comparison)
4. Three critical improvement points
```

# Reader Agent's Prompt Template

```
Read the following articles from the reader’s perspective.

# Your background
{Specify the level of knowledge and reading habits of the target audience}

# Text of article
{complete draft}

# Answer the question
1. After the first three paragraphs, will you continue reading them? Why?
2. Where do you "can't read" or "need to read to understand"? What is the exact phrase?
3. Do you understand the technical/formula part? "Is the word "speak" helping you?
4. Is the core of the article relevant? Is there a better analogy?
5. Is it too long or too short? Where would it lose patience?
6. Can you summarize the core of the article in one sentence after reading it?
Would you like to forward this article? What would you say when you did?
8. Are there any questions you want to know that are not covered by the articles?
```

---

# Phase IV: Final

# Step one: combining two Agents' feedback

Focus on the following high-frequency issues:

<unk> Problem type <unk> Edit common feedback <unk> Reader usual feedback <unk>
|---------|------------|------------|---------|
The beginning is too weak, the hook is not strong, the first three paragraphs are not motivated, and the beginning is rewritten with data/reverse instincts.
<unk> Technical paragraph discourages <unk> formula is too dense <unk> Some paragraph requires three readings <unk> delete formula or graphicization, with more intuitive analogies <unk>
♪ The rhythm drags, the rhythms, the hysteria of a section so long, the patience of a place, the combination or the deletion (especially the technical explanation of the second half)
The end is weak, the end is weak, the power is not available, the end is not transmitted, the end is rewritten as a tremor of the passing judgement, the end is not transmitted, the end is not transmitted, the end is rewritten as a tremor of the passing judgement, the end is lost.
♪ I'm not gonna get it, I'm not gonna get it, I'm not gonna get it, I'm not gonna get it, I'm not gonna get it, I'm gonna get it, I'm gonna get it, I'm gonna get it, I'm gonna get it, I'm gonna get it, I'm gonna get it, I'm gonna get it, I'm gonna get it, I'm gonna get it, I'm gonna get it, I'm gonna get it, I'm gonna get it, I'm gonna get it, I'm gonna get it, I'm gonna get it, I'm gonna get it, I'm gonna get it, I'm gonna get it, I'm gonna get it, I'm gonna get it, I'm gonna get it, I'm gonna get it, I'm gonna get it, I'm gonna get it, I'm gonna get it, I's gonna get it, I'm gonna get it, I'm gonna get it, I's gonna get it, I's gonna get it, I's gonna get it, I's gonna get it's gonna get it, I's, I's gonna get it's gonna get, you'm gonna get it's, you, you're gonna get it'

# Step 2: Implementing the changes

Rewrite the article based on feedback. Core revision principle:

1. ** ** Questions identified by both editors and readers need to be changed**
2. ** Only editorial issues identified, presumably modified** (editor ' s professional judgement is usually accurate)
3. ** ** Questions identified only by readers, modified as appropriate** (Ref feedback from readers represents a real experience, but not necessarily each one requires a response)
4. ** In the event of a contradiction, the reader is biased** (editor is in pursuit of perfection, but the reader ' s experience is the final criterion)

# Step three: extract the map

The paper reading category articles must be drawn up before they are finalized:

1. ** Rendering**: `pdftopm -png-r 900 -f {page number} -l {page number} Papers.pdf /tmp/page ' (900 DPI) rises to 1,200 or 1500 DPI if the picture is less than 500 KB)
2. **Placator**: Full page is rendered with 150 DPI, visual confirmation of pixel coordinates of charts
3. **Assuming: `compress_level=1 ' by PIL by coordinates, `compress_level=1 ' , ensuring that each ~500 KB
4. **Repository**: Saved to `assets/{themes short}/ ` Directory named `fig{sequent number}- {description}.png`
5. **Insert**: use `! [Description] in article (A/CN.9/WG.I/WP.46/Add.1 and Add.1 and 2); / //assets/{theme acronym}/fig{sequence}-- {description}.png)

# Step 4: Output final document

Saves the final text as a md document with a link to the papers/information in the original language at the end of the document:

```markdown
** Original paper:**
- arXiv: {link}
```

---

# File naming and storage

<unk> Type <unk> Path <unk> Named format <unk>
|------|------|---------|
<unk> Technical theme `reports/AI industry research/ `<unk> Public Number-{Themes} -<unk> YYYMMMD}.md '<unk>
<unk> The subject of investment <unk> reports/{corporate name}/<unk> corporate name} -The public number -<unk> YYYMMDD}.md`
<unk> Common theme <unk> reports/ <unk> Public Number - {Themes Keys} -<unk> YYYMMMD}.md '<unk>

---

# Write red lines

1. ** Non-constructive data**. The data cited must be sourced and the "estimate" must be marked without being found
2. ** No AI accent**. No "let's come and see" or "we should be concerned" or "we have to say" or something.
3. ** No overcommitment**. Technical articles do not say "subversive", "revolutionary", speak with data.
4. ** Formula must be accompanied by a big white **. Each formula must be followed by a "translation is a human ..."
5. ** Formulae must be in LaTeX**. `$...$$` format, which prohibits pure text formulae.
** The map must be actually inserted**. The paper reading class extracts the high plain from PDF (~500KB) and prohibits the use of `[figure X] ' placeholders
7. ** The table is bracketed in precise notes**. Use precise definitions when describing concepts, without vaguely verbed phrases (e.g. "text from teacher" instead of "text from teacher")
** The analogy is consistent**. The whole text is based on a main line analogy, and no new analogy is exchanged for each section.
9. ** Must have a communication power at the end. The last sentence should be transmitted separately.
