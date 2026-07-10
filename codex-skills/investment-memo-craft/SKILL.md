---
name: investment-memo-craft
description: Codex-only writing and layout overlay for AI Berkshire investment research reports. Use whenever Codex creates, rewrites, revises, or critiques company/industry/fund research reports, especially long-form Markdown reports that need financial rigor, readable business mechanics, contrarian analysis, valuation-to-action guidance, investor-specific recommendations, restrained typography, and clear buy/hold/sell signals. Do not use this to modify Claude Code slash-command sources.
---

# Investment Memo Craft

## Purpose

Turn investment research into a decision-ready Codex research report. Keep the data discipline of the underlying research skill, but make the output easier for an investor to use: concrete business mechanics, sharp inverse thinking, explicit opportunity cost, action thresholds, and calm Markdown typography.

Use this as a writing and judgment overlay. It does not replace financial-data rules, primary-source checks, valuation tools, or report audit tooling.

For long-form AI Berkshire outputs, title the artifact as a "research report" by default. Use "investment memo" only when the user explicitly asks for a memo format.

This is a Codex-only hand-written skill kept under `codex-skills/` for simple installation. Do not add a same-named `skills/investment-memo-craft.md` source unless intentionally adopting this workflow for Claude Code too.

## Core Workflow

1. Open with context; reserve the full decision for after the evidence.
   - In the first screen, state the research date, price, market cap, valuation, and a short thesis.
   - Do not front-load the full buy/hold/sell table unless the user explicitly asks for an executive memo.
   - Put the detailed recommendation, investor-specific actions, and price bands near the end, after business quality, risk, and valuation have been argued.
   - Separate "good business" from "good investment at this price".

2. Build the operating map before the philosophy.
   - Include revenue structure, segment economics, unit drivers, and 3-5 year trends early.
   - For asset-heavy businesses, show the key assets individually when they explain the moat.
   - Explain the pricing mechanism, customer lock-in, cost structure, and reinvestment needs.

3. Compress business essence into one memorable sentence.
   - Prefer a sentence that describes who pays, why they pay, what is scarce, and what repeats.
   - Avoid generic labels such as "industry leader" unless followed by the mechanism that makes leadership durable.

4. Make the moat falsifiable.
   - Score or table the moat by source: brand/pricing power, switching cost, network effect, scale, cost advantage, regulation, resource scarcity, technology.
   - Explain whether the moat widened or narrowed over the last 5 years.
   - Ask what can destroy the moat, even if the answer is "not competitors, but regulation/weather/price paid".

5. Do real inverse thinking.
   - Include failure paths with probability, impact, and observable indicators.
   - Write the strongest bear case in language a smart short seller or non-buyer would actually use.
   - Explicitly identify the most likely analytical mistake.

6. Evaluate management through capital allocation.
   - Replace vague praise with decision history: acquisitions, divestitures, buybacks, dividends, leverage, reinvestment, strategic pivots.
   - Judge incentives: insider ownership, controlling shareholder behavior, compensation, related-party transactions, and shareholder return policy.
   - Ask whether the business depends on a person or on a system.

7. Connect industry trend to value capture.
   - Distinguish civilization-level trend from investable company-level economics.
   - Describe where the company sits in the value chain and who captures the profit pool.
   - Identify whether TAM growth, pricing, utilization, or capital intensity is the real driver.

8. Convert valuation into action.
   - Show current multiples, reverse DCF intuition, scenario valuation, historical comparison, and comparable companies when relevant.
   - Include dividends or capital returns in expected return when they matter.
   - Provide price bands, add signals, trim/sell signals, and what would change the thesis.

9. Close with a decision memo.
   - Include a summary table by business quality, moat, management, risk, trend, and valuation.
   - Give distinct advice for empty-handed investors and existing holders.
   - Include the action table here, not at the top, for long-form research reports.
   - End by separating AI analysis confidence from actual investment certainty.

## Style Standards

- Prefer concrete numbers and mechanisms over adjectives.
- Use tables when they reduce cognitive load: assets, segments, failure paths, management decisions, scenario valuations, action bands.
- Write in clear investor prose. A good memo should be understandable after one read and useful after one month.
- Keep memorable formulations, but never let rhetoric outrun evidence.
- Avoid hiding behind vague labels such as "wait and see" without specifying the price or event that would change the recommendation.

## Layout Standards

For long-form research reports, prefer a calm stepped layout:

- USE a simple title: `Avoid reading "the Four Masters Consolidated" to the Title unless the user asks for that fraggling.
- USe dated files for reports: `Study of corporate names -YYYYMMDD.md`.
- Start with one compact metadata block: research date, price, market cap, key multiples, and a one-sentence thesis.
- Use horizontal separators between major sections.
- Use China step heads for readabilization, for example "first step: a core data overview", "second step: business nature analysis", and "eighth step: final decision and action list".
- Keep section titles short and concrete; avoid dense numbering such as "2.3.1" unless the document is technical.
- Use quote blocks for master-style questions, not inline bold paragraphs.
- Treat GitHub Markdown as the typography system: use heading levels, tables, quote blocks, and bold text; do not add HTML/CSS font styling unless the user explicitly asks for a non-GitHub artifact.
- Use bold sparingly as a reading guide: metadata labels, one-sentence conclusion labels, key phrases, total/current-company rows, latest-year values, scenario target prices, action rows, and audit verdicts.
- Keep ordinary facts in normal weight. Do not bold full tables or every important-looking number; over-emphasis makes long research feel noisy.
- Use explicit `+` and `-` signs for growth rates and return ranges so positive/negative movement can be scanned without rereading the sentence.
- Put checklists under "AI research bias awareness" when the company is information-rich or consensus-heavy.
- Keep audit and tool details light at the end. Do not expose command lines unless the user asks for reproducibility commands.
- If a prior report has a layout the user likes, preserve its reading rhythm while keeping only data that passes the current validation standard.

## Default Report Shape

For AI Berkshire company reports, use this order unless the user asks otherwise:

1. `AI study of prejudice conscious '
   - State the information-richness rating, consensus trap, bias checklist, and AI research limitation.

`First step: a core data overview '
   - Show segment revenue, key operating assets or units, 3-5 year financial trend, and cross-source validation.

3. `Step 2: Business nature analysis '
   - Define the business in one sentence, map revenue/cost/customer/asset life/growth drivers, and explain the real profit variables.

`Step 3: Apocalypse assessment '
   - Score moat sources, explain evidence, and state what can destroy or weaken the moat.

`Step 4: Reverse reflection and risk list '
   - Put the bear case in serious language. Include failure paths, probability, impact, and observable warning indicators.

`Step 5: Management assessment '
   - Judge management through capital allocation, governance, incentives, dividends/buybacks, leverage, and whether the business is system-driven.

`Step 6: Industry and civilizational trends '
   - Separate broad trend from investable economics and explain where the company captures value.

`Step seven: valuation and security margin '
   - Show current valuation, reverse-DCF intuition, scenario valuation, comparable companies if useful, and explicit price bands.

`Step 8: final decision-making and action list '
   - Put the full decision here, not at the top: summary table, advice for empty-handed investors, advice for holders, add/sell triggers, and master-style comments if useful.

10. `AI analyzes confidence vs. investment certainty '
    - Separate data confidence from investment certainty.

`Sources of data and audit records '
    - List key sources and concise audit results. Keep command lines out of the report unless explicitly requested.

## Quality Bar

A strong memo should answer these questions without forcing the reader to infer:

- What exactly does this company sell, to whom, and why does money repeat?
- What are the 2-3 variables that actually move profit?
- Why might smart people refuse to buy?
- What is already priced in?
- What return is plausible under bull/base/bear cases, including dividends if relevant?
- What should an empty-handed investor do?
- What should a holder do?
- What evidence would make the thesis wrong?

## Pairing With Other Skills

When the task requires fresh company research, first use the relevant data/research skill and its validation requirements. Then use this skill to rewrite or structure the output as a memo.

For AI Berkshire work, pair especially with:

- `financial-data` for source hierarchy and cross-source validation.
- `investment-research` for the Buffett/Munger/Duan/Li Lu framework.
- `management-deep-dive` when management quality is the core uncertainty.
- `report_audit.py` before treating a report as publishable.
