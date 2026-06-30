# Data Science Career Audit

A small reproducible companion analysis for the essay: **Data Science as a Career Was Made Up. The Work Was Not.**

This repo does not pretend to prove a causal labor-market theory. It uses source-backed public metrics to run a descriptive audit of the data science career category: projected growth, AI adoption, GenAI review gaps, and AI labor-market pressure.

## Core claim

Data science is not fake. But the modern job title is a bundled labor-market category: statistics + programming + business translation + dashboards + ML + domain reasoning. AI compresses the procedural parts of that bundle while increasing demand for the judgment-heavy parts.

## What's in here

Two layers, both descriptive and source-backed:

1. **Macro audit** (`src/run_audit.py`) — the growth-vs-AI-pressure contradiction
   from BLS / Stanford HAI / McKinsey / WEF aggregate metrics.
2. **Job-posting NLP** (`src/job_posting_nlp.py`) — what data-role postings
   actually ask for, how the "bundle" differs by title, and when GenAI/LLM
   language started entering data postings. Run on **real** public datasets.

## Run

```bash
pip install -r requirements.txt

# Layer 1 — macro audit (no download needed)
python src/run_audit.py

# Layer 2 — job-posting NLP (downloads ~260 MB of raw data on first run)
python src/fetch_data.py
python src/job_posting_nlp.py
```

### Layer 1 outputs (`outputs/`)
- `summary_results.csv` / `.md`
- `projected_growth_comparison.png`, `ai_adoption_2023_2024.png`, `genai_review_gap.png`

### Layer 2 outputs (`outputs/`)
- `nlp_summary.md` — all numbers, methods, and caveats in one place
- `title_mix_2023.csv`, `skill_frequency_2023.csv`, `skill_by_archetype_2023.csv`
- `skill_cooccurrence_2023.csv`, `skill_frequency_2026.csv`, `seniority_skill_split_2023.csv`
- `genai_keyword_monthly_2023.csv` + `genai_keyword_monthly_2023.png`
- `genai_2023_vs_2026.png`

## Job-posting datasets

| When | Source | Size | License | Role here |
|---|---|---|---|---|
| 2023 (base) | [`lukebarousse/data_jobs`](https://huggingface.co/datasets/lukebarousse/data_jobs) | ~785k postings, full 2023, clean monthly dates | public / CC0 | Robust within-source skill + GenAI-trend measurement |
| ~June 2026 (snapshot) | [`NextGig-Rocks/global-job-postings-multi-ats`](https://huggingface.co/datasets/NextGig-Rocks/global-job-postings-multi-ats) | ~113k global postings (~900 data roles) | CC-BY-4.0 | Recent snapshot of skill mix + GenAI prevalence |

Raw files are downloaded into `data/raw/` (gitignored). They are **not** committed.

**Cross-source honesty note:** the 2023 numbers come from a controlled skill
vocabulary; the 2026 numbers come from free-text descriptions. The two base
rates are not directly comparable, so the 2023 → 2026 change is reported as
**directional only** — never as a precise delta or a significance test. The
statistically robust result is the *within-2023* monthly trend.

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
| Early-career (22-25) employment change in most AI-exposed jobs (Stanford DEL) | -13 | percent (relative) |

### Job-posting findings (real text, descriptive)

- **The bundle is many jobs under one banner.** In 2023, Data Analyst (196k),
  Data Engineer (186k), and Data Scientist (172k) postings are near-equal in
  volume — and ask for very different stacks. Analyst postings lean Excel (34%)
  and dashboards (55%); Scientist postings lean Python (67%) and R (35%);
  Engineer postings lean Spark (30%), AWS (35%), Airflow (15%); ML Engineer
  postings lean deep learning (37%) and Docker/K8s (23%).
- **SQL (51%) and Python (50%) are the shared core**; their co-occurrence
  (~247k postings) is the single most common skill pair.
- **GenAI/LLM language is entering data postings.** It was ~0.1% of 2023 data
  postings (controlled skill lists) and already roughly doubled within 2023
  (Jan–Jun 0.10% → Jul–Dec 0.17%). In the ~June 2026 snapshot it appears in
  **~27%** of data-role postings (free text, n≈900 — directional, see caveat).
- **Entry-level exposure — an honest null.** Job postings can't show that the
  automatable stack sits at the entry level: procedural-skill prevalence is
  flat-to-*higher* in "Senior" postings and GenAI is ~0% across tiers in 2023.
  The "entry-level is hit hardest" claim therefore rests on external payroll
  research (Stanford Digital Economy Lab, *Canaries in the Coal Mine*, 2025:
  ~13% relative employment decline for ages 22–25 in the most AI-exposed
  occupations), not on this layer. See `outputs/seniority_skill_split_2023.csv`.

Full numbers, methods, and caveats: [`outputs/nlp_summary.md`](outputs/nlp_summary.md).

## Sources

- BLS Occupational Outlook Handbook — Data Scientists
- BLS Monthly Labor Review — 2024–2034 employment projections overview
- Stanford HAI AI Index 2025
- McKinsey State of AI 2025
- World Economic Forum Future of Jobs Report 2025
- Stanford Digital Economy Lab — *Canaries in the Coal Mine* (2025), early-career AI employment effects
- Job postings: `lukebarousse/data_jobs` (2023), `NextGig-Rocks/global-job-postings-multi-ats` (2026)

## Limitation

This is a source-backed **descriptive** audit, not a formal peer-reviewed labor
economics paper and not a causal analysis. The job-posting layer measures what
postings *say*; it does not estimate why, and it does not fit a model. The
2023 → 2026 comparison crosses two different data sources and is directional
only. For real causal work, extend with occupation-level historical employment
panels, salary trajectories, AI-exposure scores, and industry controls — and
only then add regression. Until the data supports it, no regression is run here
on purpose.
