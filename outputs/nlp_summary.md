# Job-Posting NLP Results

Descriptive measurement on real job-posting text. No model is fit.

## Datasets

- **2023 base**: lukebarousse/data_jobs — 728,481 data-family postings (Data Analyst/Scientist/Engineer/ML + Business Analyst), full calendar 2023, skills from a controlled vocabulary.
- **2026 snapshot**: NextGig multi-ATS — 888 data-family postings filtered from ~113k global postings as of ~June 2026, skills from free text.

## Title mix, 2023 (the bundle is many jobs under one banner)

| title                     |   postings |
|:--------------------------|-----------:|
| Data Analyst              |     196075 |
| Data Engineer             |     186241 |
| Data Scientist            |     172286 |
| Business Analyst          |      49063 |
| Senior Data Engineer      |      44563 |
| Senior Data Scientist     |      36957 |
| Senior Data Analyst       |      29216 |
| Machine Learning Engineer |      14080 |

## Skill frequency among data roles, 2023 (% of postings)

| skill                 |   pct_of_postings |
|:----------------------|------------------:|
| sql                   |              51.1 |
| python                |              49.8 |
| spreadsheet/dashboard |              34.9 |
| aws                   |              18.1 |
| r                     |              17.7 |
| tableau               |              17.2 |
| excel                 |              17   |
| azure                 |              16.8 |
| spark                 |              15.2 |
| power bi              |              13.2 |
| gcp                   |               6.3 |
| docker/k8s            |               6.2 |
| airflow               |               6   |
| sas                   |               5.6 |
| deep learning         |               5.3 |
| machine learning      |               2.7 |
| nlp                   |               0   |

## Same skills by archetype, 2023 (% of postings)

The point of the essay made concrete: 'data role' means very different stacks depending on the title.

|                       |   Analyst |   Engineer |   ML Engineer |   Scientist |
|:----------------------|----------:|-----------:|--------------:|------------:|
| python                |      27.8 |       59.3 |          68.7 |        66.7 |
| sql                   |      46.6 |       61.8 |          25   |        46.8 |
| r                     |      14.7 |        6.6 |          11.2 |        34.5 |
| excel                 |      33.6 |        4.3 |           4.1 |         9.9 |
| tableau               |      24   |       10.2 |           2.9 |        16.9 |
| power bi              |      19.9 |       10   |           1.8 |         8.9 |
| sas                   |       6.8 |        2   |           1.3 |         8.6 |
| spark                 |       2.6 |       30.2 |          19.3 |        14.8 |
| airflow               |       1.1 |       14.8 |           8.3 |         2.5 |
| aws                   |       4.7 |       35.3 |          26.9 |        16.1 |
| azure                 |       5.7 |       33.3 |          19.4 |        13   |
| gcp                   |       1.7 |       12.3 |          12   |         5.4 |
| spreadsheet/dashboard |      54.5 |       20.3 |           7.3 |        27   |
| machine learning      |       0.4 |        0.8 |          14.2 |         7.1 |
| deep learning         |       0.5 |        1.6 |          37.2 |        13.6 |
| nlp                   |       0   |        0   |           0   |         0   |
| docker/k8s            |       0.7 |       12.1 |          23.4 |         5.5 |

## GenAI / LLM language entering data postings

- 2023 monthly average, Jan–Jun: **0.10%** of data postings.
- 2023 monthly average, Jul–Dec: **0.17%** of data postings (rising within the year).
- 2023 full-year (controlled skill lists): **0.1%**.
- 2026 snapshot (free-text postings, n=888): **27.0%**.

> Cross-source caveat: 2023 counts presence in a controlled skill list; 2026 counts presence in free-text descriptions. The two base rates are not directly comparable, so treat the jump as **directional**, not a precise delta.

## Entry-level exposure: a check that did NOT pan out in postings

Is the procedural, automatable stack concentrated in entry-level roles? Job postings are a poor instrument for this: they list skills for all levels, so 'Senior' postings carry at least as many procedural skills. Below, procedural-skill prevalence is flat-to-*higher* for senior titles and GenAI is ~0% across tiers in 2023. So this layer does **not** prove 'entry-level is hit hardest.' That claim rests on external payroll research (Stanford Digital Economy Lab, 'Canaries in the Coal Mine,' 2025: ~13% relative employment decline for ages 22–25 in the most AI-exposed occupations) plus the task-automation logic — not on this table.

| role           | tier       |   postings |   procedural_skill_pct |   genai_pct |
|:---------------|:-----------|-----------:|-----------------------:|------------:|
| Data Analyst   | non-senior |     196075 |                   69.6 |       0.006 |
| Data Analyst   | senior     |      29216 |                   75.4 |       0.007 |
| Data Scientist | non-senior |     172286 |                   55.1 |       0.305 |
| Data Scientist | senior     |      36957 |                   58   |       0.655 |
| Data Engineer  | non-senior |     186241 |                   65.7 |       0.017 |
| Data Engineer  | senior     |      44563 |                   68.3 |       0.025 |

## Top skill co-occurrence pairs, 2023

| skill_a   | skill_b   |   co_postings |
|:----------|:----------|--------------:|
| python    | sql       |        246510 |
| python    | r         |        118504 |
| aws       | python    |        102907 |
| sql       | tableau   |         94977 |
| python    | spark     |         90508 |
| r         | sql       |         90447 |
| aws       | sql       |         87261 |
| azure     | sql       |         86607 |
| azure     | python    |         84537 |
| python    | tableau   |         78884 |
| spark     | sql       |         75571 |
| power bi  | sql       |         68969 |
| excel     | sql       |         65738 |
| java      | python    |         64745 |
| aws       | azure     |         53676 |