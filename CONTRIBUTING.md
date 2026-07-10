# Contributing Guide / Contributing Guide

Chinese | [English](#english)

Thank you for your interest in AI Berkshire. The starting point of this project is my personal investment research process. I open source it in the hope that the methodology will be useful to more people. To make maintenance sustainable, please take two minutes to read this guide before submitting an issue or PR.

## Contributions welcome

- **Skill bug fixes**: incorrect prompt words, process failure, output format issues, etc. Please explain in the PR description: which skill, in which scenario the problem occurred, and the results you actually ran after the fix.
- **Skill Improvements**: Changes to make analysis more rigorous, data cross-validation more reliable, and output more usable. Changes need to be accompanied by a description of "why this is better", and it is best to compare the output before and after the change.
- **Documentation improvements**: Corrections to typos, broken links, and unclear expressions in README and docs/; corrections to the out-of-sync content between the English and Chinese versions.
- **Compatibility Adaptation**: Adaptation issues caused by the new version of Claude Code / Codex.
- **Research reports produced using this framework**: Welcome to submit to the `reports/community/` subdirectory (organized by `reports/community/[company name]/`). Requirements: ① The report is indeed run using the skills of this warehouse, and the skill and model used are indicated at the beginning of the article; ② Attached is a disclaimer (does not constitute investment advice); ③ One PR per report. Those whose quality is obviously not up to standard (such as no framework, purely handwritten opinions, and lack of key financial cross-validation) will be closed.
- **New Skill Proposal**: Please open an issue for discussion first, explaining what research scenarios this skill solves and what the boundaries are with the existing 18 skills. Submitting a large new feature PR without discussing it first will likely get you shut down - not a denial of your work, but a waste of time for both parties when the directions are misaligned.

## Contributions not accepted

- **Modify existing reports under `reports/` (except `community/`), `real record/`, `screening company/`**: These are my personal research output and transaction records and do not accept external modifications. Please submit your own research to `reports/community/` (see above), or share the link in an issue after publishing it in your own repository.
- **Investment Viewpoint Debate**: The conclusion in the report (such as whether a company is worth buying) is the result of the methodology, and modifications based on "I disagree with this conclusion" are not accepted. If you have any questions about the methodology itself, you are welcome to open an issue for discussion.
- **Pure boilerplate PR**: Configuration files or governance files that are generated in batches by automated tools and have nothing to do with the actual needs of the project.
- **Mass Format/Rename**: Changes that don't change the actual content and just create a lot of diff noise.

## Basic requirements for submitting a PR

1. A PR only does one thing, keep the diff focused.
2. Write clearly in the description: what was changed, why it was changed, and how it was verified. For changes involving skill, please attach the actual effect of running it in Claude Code or Codex.
3. Both Chinese and English are accepted.
4. When changing parts of README.md that affect the content, please update README_EN.md simultaneously (and vice versa); pure typography corrections can only change one side.

## Submit Issue

Please select the corresponding type from the three Issue templates to submit (the blank issue has been closed). **Core requirement: Any opinion must be accompanied by specific and reproducible examples**, otherwise it cannot be verified and will be asked to supplement or be closed directly.

- **🐞 Skill error report**: Indicate the skill called (make sure the title is consistent with the text), complete command, error message, **model used and client version**.
- **📉 Data error** (stock price/market value/financial data): Give the specific target, error value, **what you think is the correct value and source link**, and explain whether it involves restoration of rights/transfer/additional issuance/exchange rate, etc.
- **💡 Improvement suggestions**: Give **specific sources** (which report, which table) and **expected improvement comparison** (currently looks like this → expected to look like this). Suggestions with only abstract descriptions are not accepted.
- **Research Request** ("Help me analyze such-and-such company"): No orders will be accepted for this project. The meaning of this framework is to allow you to run professional-level research yourself - just follow the quick start of the README and run it with your own AI tool.

## Security issues

If you find security vulnerabilities such as API key leaks and prompt injection, please **do not** open a public issue and report privately via [SECURITY.md](SECURITY.md).

## Disclaimer

All contents of this project are only a demonstration of research methodology and do not constitute investment advice. The content submitted by contributors also follows this principle by default. Please do not include stock recommendations or income commitments in your contributions.

---

<a name="english"></a>

# Contributing Guide (English)

Thanks for your interest in AI Berkshire. This project grew out of my personal investment research workflow; it is open-sourced so the methodology can be useful to others. Please read this short guide before opening an issue or PR.

## Welcome contributions

- **Skill bug fixes** — broken prompts, workflow failures, output format issues. In the PR description, state which skill, how the problem occurs, and the actual output after your fix.
- **Skill improvements** — changes that make the analysis more rigorous or the output more usable. Explain *why* it is better, ideally with a before/after comparison.
- **Documentation fixes** — typos, dead links, unclear wording, and syncing the English README with the Chinese one.
- **Compatibility fixes** for new versions of Claude Code / Codex.
- **Research reports produced with this framework** — submit to the `reports/community/` subdirectory (organized as `reports/community/[company]/`). Requirements: (1) the report was actually generated with this repo's skills — state the skill and model used at the top; (2) include a disclaimer (not investment advice); (3) one report per PR. Reports that clearly miss the bar (framework not used, hand-written opinions only, missing financial cross-validation) will be closed.
- **New skill proposals** — open an issue first to discuss the research scenario it addresses and how it differs from the existing 18 skills. Large unsolicited feature PRs may be closed to avoid wasted effort on both sides.

## Out of scope

- **Edits to existing reports under `reports/` (except `community/`), ` real trading records/` (live trading records), or `Screening companies/`** — these are my personal research output and trading records. Submit your own research to `reports/community/` (see above), or publish it in your own repo and share the link in an issue.
- **Disagreements over investment conclusions** — report conclusions are outputs of the methodology; "I disagree with this call" is not a basis for a PR. Challenges to the methodology itself are welcome as issues.
- **Boilerplate-only PRs** generated by automated tools without a concrete need in this project.
- **Mass reformatting/renaming** that produces large diffs without substantive change.

## PR basics

1. One PR does one thing.
2. Describe what changed, why, and how you verified it. For skill changes, include results from an actual run in Claude Code or Codex.
3. Chinese or English are both fine.
4. Substantive edits to README.md should be mirrored in README_EN.md (and vice versa).

## Issues

Please pick the matching Issue template (blank issues are disabled). **Core rule: every claim must come with a concrete, reproducible example**, otherwise it cannot be verified and will be asked for more detail or closed.

- **🐞 Skill error**: state the skill invoked (make sure the title matches the body), the full command, the error message, and **the model and client version used**.
- **📉 Data error** (price/market cap/financials): give the specific ticker, the wrong value, and **the value you believe is correct plus a source link**; note whether it involves split/bonus-issue/dilution/FX adjustments.
- **💡 Suggestion**: give a **concrete location** (which report, which table) and a **before/after expectation**; abstract-only suggestions are not accepted.
- **💬 Discussion / new skill proposal / other**: non-problem topics go here (no reproduction info required).
- **Research requests** ("please analyze company X"): not accepted — the whole point of this framework is that you can run professional-grade research yourself. Follow the Quick Start in the README.

## Security

For vulnerabilities (API key leakage, prompt injection, etc.), please do **not** open a public issue — report privately as described in [SECURITY.md](SECURITY.md).

## Disclaimer

Nothing in this project constitutes investment advice. Contributions must follow the same principle — no stock tips or return promises.
