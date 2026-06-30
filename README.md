# Data Science Career Audit

A small reproducible companion analysis for the essay: **Data Science as a Career Was Made Up. The Work Was Not.**

This repo does not pretend to prove a causal labor-market theory. It uses source-backed public metrics to run a descriptive audit of the data science career category: projected growth, AI adoption, GenAI review gaps, and AI labor-market pressure.

## Core claim

Data science is not fake. But the modern job title is a bundled labor-market category: statistics + programming + business translation + dashboards + ML + domain reasoning. AI compresses the procedural parts of that bundle while increasing demand for the judgment-heavy parts.

## Run

```bash
pip install -r requirements.txt
python src/run_audit.py
```

Outputs are written to `outputs/`:

- `summary_results.csv`
- `summary_results.md`
- `projected_growth_comparison.png`
- `ai_adoption_2023_2024.png`
- `genai_review_gap.png`

## Current results

| Result | Value | Unit |
|---|---:|---|
| Data scientist jobs, 2024 | 245,900 | jobs |
| Projected data scientist jobs, 2034 | 329,506 | jobs |
| Projected jobs added, 2024-2034 | 83,606 | jobs |
| DS projected growth vs all occupations | 10.97 | x |
| Data scientist median pay, 2024 | 112,590 | USD/year |
| AI adoption absolute change, 2023-2024 | 23 | percentage points |
| AI adoption relative change, 2023-2024 | 41.8 | percent |
| GenAI investment as share of US private AI investment | 31.1 | percent |
| GenAI orgs reviewing all outputs | 27 | percent |
| GenAI orgs reviewing <=20% outputs | 27 | percent |
| WEF respondents expecting AI/info tech business transformation | 86 | percent |
| WEF projected net global job change by 2030 | 78 | million jobs |

## Sources

- BLS Occupational Outlook Handbook — Data Scientists
- BLS Monthly Labor Review — 2024–2034 employment projections overview
- Stanford HAI AI Index 2025
- McKinsey State of AI 2025
- World Economic Forum Future of Jobs Report 2025

## Limitation

This is a source-backed technical audit, not a formal peer-reviewed labor economics paper. For real causal analysis, extend the project with occupation-level historical employment data, job-posting text, salaries, education requirements, AI-exposure scores, and industry controls.
