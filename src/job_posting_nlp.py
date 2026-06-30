"""
Job-Posting NLP: skills, role bundles, and GenAI keyword drift in data roles.

This is the descriptive job-posting layer of the Data Science Career Audit. It
measures, on REAL job-posting text, the things the essay argues about:

  - the "bundle" composition of data roles (which skills actually co-occur)
  - how that bundle differs by title (Analyst vs Scientist vs Engineer vs ML)
  - whether GenAI / LLM language is entering data-role postings, and when

Two real public datasets are used (downloaded by src/fetch_data.py):

  2023 base      lukebarousse/data_jobs   ~785k postings, full calendar 2023,
                 clean monthly dates and a controlled skill vocabulary.
  2026 snapshot  NextGig multi-ATS        ~113k global postings as of ~June 2026,
                 free-text descriptions. Only ~1.1k are data-family roles, so the
                 2026 numbers are a small recent SNAPSHOT, not a robust series.

HONESTY NOTES
-------------
* The 2023 monthly trend is a single-source, within-dataset measurement and is
  the statistically robust result. n is large (hundreds of thousands).
* The 2026 figures come from a different source with a different extraction
  method (regex over free text vs. a controlled skill list). Therefore the
  2023 -> 2026 comparison is reported as DIRECTIONAL ONLY. The absolute levels
  are not apples-to-apples and we do not compute a "significance" on the gap.
* No model is fit here. This is descriptive measurement, not causal inference.
"""

from __future__ import annotations

import ast
import re
from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"
OUT = ROOT / "outputs"
OUT.mkdir(exist_ok=True)

LB_PATH = RAW / "data_jobs_2023.csv"
NG_PATH = RAW / "nextgig_jobs_2026-06.parquet"

# --------------------------------------------------------------------------- #
# Vocabulary                                                                   #
# --------------------------------------------------------------------------- #
# Each skill maps to a regex searched (case-insensitive) against a per-posting
# text blob. For 2023 the blob is the controlled skill list; for 2026 it is the
# free-text description + skills + qualifications. Same patterns, two corpora.

SKILLS = {
    "python": r"\bpython\b",
    "sql": r"\bsql\b",
    "r": r"(?:^|[,'\s])r(?:[,'\s]|$)",          # 2023 skill-list only (too noisy in prose)
    "excel": r"\bexcel\b",
    "tableau": r"\btableau\b",
    "power bi": r"power\s?bi",
    "sas": r"\bsas\b",
    "spark": r"\bspark\b",
    "airflow": r"\bairflow\b",
    "aws": r"\baws\b",
    "azure": r"\bazure\b",
    "gcp": r"\bgcp\b|google cloud",
    "spreadsheet/dashboard": r"\bexcel\b|tableau|power\s?bi|looker|dashboard",
    "machine learning": r"machine learning|\bml\b|scikit|sklearn|xgboost",
    "deep learning": r"deep learning|pytorch|tensorflow|\bkeras\b",
    "nlp": r"\bnlp\b|natural language",
    "docker/k8s": r"\bdocker\b|kubernetes|\bk8s\b",
}

# The "GenAI bundle" — the language that barely existed in data postings before
# late 2022 and is the thing AI is adding to (and unbundling from) the role.
GENAI = {
    "generative ai / genai": r"generative ai|gen ?ai",
    "llm": r"\bllms?\b|large language model",
    "gpt / chatgpt": r"\bgpt\b|chatgpt",
    "rag": r"\brag\b|retrieval[- ]augmented",
    "langchain / llamaindex": r"langchain|llama ?index",
    "prompt engineering": r"prompt engineer|prompting",
    "ai agents": r"\bai agents?\b|agentic",
    "vector database": r"vector (?:database|db|store)|pinecone|weaviate|\bfaiss\b",
    "hugging face": r"hugging ?face",
}
GENAI_ANY = re.compile("|".join(GENAI.values()), re.I)

# Map lukebarousse 2023 titles to coarse archetypes for the "bundle by title" view
LB_ARCHETYPE = {
    "Data Analyst": "Analyst",
    "Senior Data Analyst": "Analyst",
    "Business Analyst": "Analyst",
    "Data Scientist": "Scientist",
    "Senior Data Scientist": "Scientist",
    "Data Engineer": "Engineer",
    "Senior Data Engineer": "Engineer",
    "Machine Learning Engineer": "ML Engineer",
}

# Regex to pull data-family postings out of the general 2026 board
NG_FAMILY = {
    "Analyst": r"data analyst|analytics analyst|business intelligence|\bbi analyst\b",
    "Scientist": r"data scientist",
    "Engineer": r"data engineer|analytics engineer",
    "ML Engineer": r"machine learning|\bml engineer\b|\bai engineer\b|ai/ml",
}
NG_FAMILY_ANY = re.compile("|".join(NG_FAMILY.values()), re.I)


def _pct(series_bool) -> float:
    return round(100 * float(series_bool.mean()), 1)


# --------------------------------------------------------------------------- #
# Load + normalize                                                            #
# --------------------------------------------------------------------------- #
def load_2023() -> pd.DataFrame:
    df = pd.read_csv(
        LB_PATH,
        usecols=["job_title_short", "job_posted_date", "job_skills", "job_country"],
    )
    df = df[df["job_title_short"].isin(LB_ARCHETYPE)].copy()
    df["archetype"] = df["job_title_short"].map(LB_ARCHETYPE)
    df["date"] = pd.to_datetime(df["job_posted_date"], errors="coerce")
    df["month"] = df["date"].dt.to_period("M").astype(str)
    # blob = the controlled skill list, lowercased
    df["blob"] = df["job_skills"].fillna("[]").str.lower()
    return df


def load_2026() -> pd.DataFrame:
    df = pd.read_parquet(NG_PATH)
    title = (df["title"].fillna("") + " " + df["normalized_title"].fillna("")).str.lower()
    mask = title.str.contains(NG_FAMILY_ANY)
    df = df[mask].copy()
    df["title_blob"] = title[mask]
    df["archetype"] = pd.NA
    for arch, pat in NG_FAMILY.items():
        hit = df["title_blob"].str.contains(pat, regex=True)
        df.loc[hit & df["archetype"].isna(), "archetype"] = arch
    cols = ["skills_required", "job_description", "minimum_qualifications",
            "preferred_qualifications"]
    df["blob"] = (
        df[cols].fillna("").agg(" ".join, axis=1).str.lower()
    )
    return df


# --------------------------------------------------------------------------- #
# Measurements                                                                #
# --------------------------------------------------------------------------- #
def skill_freq(df: pd.DataFrame, skills: dict, drop=()) -> pd.DataFrame:
    rows = []
    for name, pat in skills.items():
        if name in drop:
            continue
        rows.append([name, _pct(df["blob"].str.contains(pat, regex=True))])
    out = pd.DataFrame(rows, columns=["skill", "pct_of_postings"])
    return out.sort_values("pct_of_postings", ascending=False).reset_index(drop=True)


def skill_by_archetype(df: pd.DataFrame, skills: dict) -> pd.DataFrame:
    out = {}
    for arch, g in df.groupby("archetype"):
        out[arch] = {name: _pct(g["blob"].str.contains(pat, regex=True))
                     for name, pat in skills.items()}
    return pd.DataFrame(out).round(1)


def genai_monthly_2023(df: pd.DataFrame) -> pd.DataFrame:
    df = df.dropna(subset=["month"]).copy()
    df["has_genai"] = df["blob"].str.contains(GENAI_ANY)
    g = (df.groupby("month")
           .agg(postings=("has_genai", "size"),
                genai_pct=("has_genai", lambda s: round(100 * s.mean(), 3)))
           .reset_index())
    return g


def cooccurrence_2023(df: pd.DataFrame, top_n=15) -> pd.DataFrame:
    """Top skill pairs that appear together, from the controlled 2023 skill lists."""
    from collections import Counter
    from itertools import combinations
    pair = Counter()
    for s in df["job_skills"].dropna():
        try:
            skills = sorted(set(ast.literal_eval(s)))
        except (ValueError, SyntaxError):
            continue
        for a, b in combinations(skills, 2):
            pair[(a, b)] += 1
    rows = [[a, b, c] for (a, b), c in pair.most_common(top_n)]
    return pd.DataFrame(rows, columns=["skill_a", "skill_b", "co_postings"])


# --------------------------------------------------------------------------- #
# Plots                                                                       #
# --------------------------------------------------------------------------- #
def plot_monthly(g: pd.DataFrame):
    plt.figure(figsize=(9, 5))
    plt.plot(g["month"], g["genai_pct"], marker="o")
    plt.title("GenAI / LLM language in data-role postings, by month (2023)")
    plt.ylabel("% of postings mentioning any GenAI/LLM term")
    plt.xticks(rotation=45, ha="right")
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig(OUT / "genai_keyword_monthly_2023.png", dpi=200)
    plt.close()


def plot_genai_2023_vs_2026(p2023: float, p2026: float, n2026: int):
    plt.figure(figsize=(7, 5))
    bars = plt.bar(["2023\n(lukebarousse, ~480k)", f"2026\n(NextGig, n={n2026})"],
                   [p2023, p2026])
    plt.bar_label(bars, fmt="%.1f%%")
    plt.title("GenAI/LLM mentions in data-role postings (directional, cross-source)")
    plt.ylabel("% of data-role postings")
    plt.tight_layout()
    plt.savefig(OUT / "genai_2023_vs_2026.png", dpi=200)
    plt.close()


# --------------------------------------------------------------------------- #
def main():
    if not (LB_PATH.exists() and NG_PATH.exists()):
        raise SystemExit("Raw data missing. Run: python src/fetch_data.py")

    lb = load_2023()
    ng = load_2026()

    # ---- 2023 robust measurements ----
    title_mix = (lb["job_title_short"].value_counts()
                 .rename_axis("title").reset_index(name="postings"))
    title_mix.to_csv(OUT / "title_mix_2023.csv", index=False)

    freq23 = skill_freq(lb, SKILLS)
    freq23.to_csv(OUT / "skill_frequency_2023.csv", index=False)

    by_arch = skill_by_archetype(lb, SKILLS)
    by_arch.to_csv(OUT / "skill_by_archetype_2023.csv")

    monthly = genai_monthly_2023(lb)
    monthly.to_csv(OUT / "genai_keyword_monthly_2023.csv", index=False)
    plot_monthly(monthly)

    cooc = cooccurrence_2023(lb)
    cooc.to_csv(OUT / "skill_cooccurrence_2023.csv", index=False)

    # ---- 2026 snapshot (small n) ----
    freq26 = skill_freq(ng, SKILLS, drop=("r",))  # 'r' regex unreliable in prose
    freq26.to_csv(OUT / "skill_frequency_2026.csv", index=False)

    p2023_genai = _pct(lb["blob"].str.contains(GENAI_ANY))
    p2026_genai = _pct(ng["blob"].str.contains(GENAI_ANY))
    plot_genai_2023_vs_2026(p2023_genai, p2026_genai, len(ng))

    # ---- narrative summary ----
    h2 = monthly[monthly["month"] >= "2023-07"]["genai_pct"].mean()
    h1 = monthly[monthly["month"] < "2023-07"]["genai_pct"].mean()
    lines = [
        "# Job-Posting NLP Results\n",
        "Descriptive measurement on real job-posting text. No model is fit.\n",
        "## Datasets\n",
        f"- **2023 base**: lukebarousse/data_jobs — {len(lb):,} data-family postings "
        "(Data Analyst/Scientist/Engineer/ML + Business Analyst), full calendar 2023, "
        "skills from a controlled vocabulary.",
        f"- **2026 snapshot**: NextGig multi-ATS — {len(ng):,} data-family postings "
        "filtered from ~113k global postings as of ~June 2026, skills from free text.\n",
        "## Title mix, 2023 (the bundle is many jobs under one banner)\n",
        title_mix.to_markdown(index=False),
        "\n## Skill frequency among data roles, 2023 (% of postings)\n",
        freq23.to_markdown(index=False),
        "\n## Same skills by archetype, 2023 (% of postings)\n",
        "The point of the essay made concrete: 'data role' means very different "
        "stacks depending on the title.\n",
        by_arch.to_markdown(),
        "\n## GenAI / LLM language entering data postings\n",
        f"- 2023 monthly average, Jan–Jun: **{h1:.2f}%** of data postings.",
        f"- 2023 monthly average, Jul–Dec: **{h2:.2f}%** of data postings "
        f"({'rising' if h2 > h1 else 'flat/declining'} within the year).",
        f"- 2023 full-year (controlled skill lists): **{p2023_genai:.1f}%**.",
        f"- 2026 snapshot (free-text postings, n={len(ng):,}): **{p2026_genai:.1f}%**.",
        "\n> Cross-source caveat: 2023 counts presence in a controlled skill list; "
        "2026 counts presence in free-text descriptions. The two base rates are not "
        "directly comparable, so treat the jump as **directional**, not a precise delta.\n",
        "## Top skill co-occurrence pairs, 2023\n",
        cooc.to_markdown(index=False),
    ]
    (OUT / "nlp_summary.md").write_text("\n".join(lines), encoding="utf-8")

    print(f"2023 data-family postings: {len(lb):,}")
    print(f"2026 data-family postings: {len(ng):,}")
    print(f"GenAI mentions  2023: {p2023_genai}%  |  2026: {p2026_genai}%")
    print(f"GenAI monthly 2023  H1: {h1:.2f}%  H2: {h2:.2f}%")
    print(f"\nWrote outputs to {OUT}")


if __name__ == "__main__":
    main()
