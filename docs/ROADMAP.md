# ai-berkshire Roadmap

## P0: Recent (1-2 months)

### A-share data source access
- Access free data sources such as akshare and Oriental Fortune
- Covers A-share financial data, market trends, and dragon and tiger rankings
- Existing skills do not need to be modified, the data layer can be expanded

## P1: Mid-term (3-6 months)

### HTML report output
- Add HTML report format based on Markdown
- Support dark mode, navigation bar, chart visualization
- Improve report dissemination and reading experience

### Multi-level depth mode
- `lite`: 5-minute quick judgment, quickly give valuation range and core conclusions
- `standard`: current default mode, complete multi-Agent research
- `deep`: Add more cross-validation and historical analogies, institution-level depth

### Horizontal comparison of multiple stocks
-Support 2-4 stocks in the same dimension for horizontal duel
- Valuation benchmarking of companies in the same industry
- Output comparison matrix and selection suggestions

## P2: Long term (6 months+)

### Test coverage
- Add unit tests for core tools (financial_rigor.py, etc.)
- Add regression testing for Skill output
- Ensure iteration does not break existing functionality

### Portfolio Level Analysis
- Assessment of the health of the position portfolio
- Industry/geographical concentration analysis
- Relevance risk detection
