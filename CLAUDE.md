#AI Berkshire — Project Directive

## Project Overview

A collection of value investing research skills based on Claude Code. The Four Masters Framework: Buffett, Munger, Duan Yongping, and Li Lu.
GitHub: xbtlin/ai-berkshire

## Project structure

```
skills/ — Investment research Skill definition (.md), copy to ~/.claude/commands/ for use
tools/ — auxiliary tools (financial_rigor.py precise calculation)
reports/ — investment research report output
assets/ — static resources such as pictures
```

## Report directory structure

All reports are created in folders by **company name**, and all reports related to the company are placed in the corresponding folders:

```
reports/
├── AI Industry Research/ — Panoramic Research on AI Industry Chain (Top)
│ ├── AI five-layer cake-Industry Panoramic Research-20260605.md
│ └── AI five-layer cake-public account-20260605.md
├── Tencent/ — All Tencent research reports
│ ├── Tencent-research-20260408.md
│ ├── Tencent-earnings-2025Q4.md
│ ├── Tencent-management-20260409.md
│ └── Tencent-thesis.md
├── Pinduoduo/ — All Pinduoduo research reports
├── Bubble Mart/ — All research reports on Bubble Mart
├── Nuclear power-industry-20260409.md — Industry reports in the root directory
├── AI computing power-funnel-20260509.md — put the funnel screening report in the root directory
├── AI-Rotation Judgment-20260509.md — Topic-level comprehensive judgment report placed in the root directory
├── portfolio-latest.md — put the portfolio report in the root directory
└── Multi-company comparison-checklist-20260408.md — put multi-company reports in the root directory
```

## Report naming convention

| Skill | File Naming Format | Example |
|------|---------|------|
| /investment-team | `{Company name}/` Directory contains 4 perspectives + final report | `reports/pinduoduo/final report.md` |
| /investment-research | `{Company name}-research-{YYYYMMDD}.md` | `reports/Tencent/Tencent-research-20260408.md` |
| /investment-checklist | `{Company name}-checklist-{YYYYMMDD}.md` | `reports/Tencent/Tencent-checklist-20260408.md` |
| /industry-research | `{Industry name}-industry-{YYYYMMDD}.md` (root directory) | `reports/nuclear power-industry-20260409.md` |
| /industry-funnel | `{Industry name}-funnel-{YYYYMMDD}.md` (root directory) | `reports/AI computing power-funnel-20260509.md` |
| /private-company-research | `{Company name}-private-{YYYYMMDD}.md` | `reports/bytebeat/bytebeat-private-20260408.md` |
| /earnings-review | `{Company name}-earnings-{Period}.md` | `reports/Tencent/Tencent-earnings-2025Q4.md` |
| /earnings-team | `{Company name}/` The directory contains 4 master perspectives + research manuscripts + public account articles + reader reviews | `reports/Tencent/Tencent-earnings-2025Q4.md` (public account final draft) |
| /thesis-tracker | `{Company name}-thesis.md` (long-term maintenance) | `reports/Tencent/Tencent-thesis.md` |
| /portfolio-review | `portfolio-latest.md` (root directory, continuously updated) | `reports/portfolio-latest.md` |
| /management-deep-dive | `{Company name}-management-{YYYYMMDD}.md` | `reports/Tencent/Tencent-management-20260409.md` |

## /investment-team file structure

```
reports/{company name}/
├── README.md — Overview of research framework + core conclusions
├── 01-Business model analysis-Duan Yongping’s perspective.md
├── 02-Financial Valuation Analysis-Buffett’s Perspective.md
├── 03-Industry Competition Analysis-Munger’s Perspective.md
├── 04-Risk Management Assessment-Li Lu’s Perspective.md
└── Final report.md — Team Lead comprehensive report
```

## Core principles of investment research analysis (highest priority)

- **Objective, objective, objective** - All investment research analysis must be based on facts and data, and subjective assumptions are strictly prohibited
- Strictly distinguish between "facts" and "opinions": facts are supported by data, and opinions must be clearly marked as "opinions" or "speculations"
- **No preset position**: There is no preset of bullishness or bearishness. First, the data is presented, then the logic is deduced, and finally the conclusion is drawn. Conclusions must flow naturally from the data
- It is forbidden to use subjective expressions such as "I think", "I think", "Obviously", etc. Use "data shows", "evidence shows", "according to XX sources" instead
- **Present both sides**: Each core judgment must be accompanied by negative arguments ("But on the other hand..."), allowing readers to weigh their own
-Be honest about "uncertainty" or "insufficient data" about things you're not sure about, don't fill certainties with speculation
- All skills (investment-team, investment-research, earnings-review, etc.) must comply with the above principles when executing

## Reporting language and style

- All reports are in **Chinese**
- Style: direct, sharp, no nonsense
- Data must be labeled with sources, and key data must be cross-validated from at least 2 sources
- Estimates must be marked "estimated"
- Ratings use ★ symbols (★1-5), excluding half stars
- Interspersed with quotes and comments from Buffett/Munger/Duan Yongping/Li Lu

## GitHub Actions

- Local clone path: `~/ai-berkshire/`
- Remote warehouse: `https://github.com/xbtlin/ai-berkshire.git`
- `git pull --rebase origin main` before pushing (there are often new submissions on the remote)
- The commit message is in Chinese and clearly describes what has been changed.
- Do not push intermediate process files (such as data_collection.md), only push the final report

## Common commands

```bash
# Push report to GitHub
cd ~/ai-berkshire
git add reports/xxx.md
git commit -m "Add xxx report"
git pull --rebase origin main
git push origin main
```

## Notes

- Market value must be manually calculated and verified: stock price × total share capital, compared with the reported market value
- The currency unit must be clear (HKD/RMB/USD) to prevent confusion
- PE/ROE and other indicators are accurately calculated using tools/financial_rigor.py
- After writing the report, ask if you want to push it to GitHub
