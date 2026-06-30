"""
Data Science Career Audit

This script uses source-backed public figures to compute a small, reproducible
companion analysis for a blog post about data science as a bundled career label.

Important limitation:
This is not a causal inference paper. The data points here are aggregate public
metrics from BLS, Stanford HAI, McKinsey, and WEF. The script produces descriptive
and derived metrics. It intentionally does NOT pretend that a causal regression
can be identified from these aggregate source anchors alone.
"""

from __future__ import annotations

from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "source_metrics.csv"
OUT = ROOT / "outputs"
OUT.mkdir(exist_ok=True)


def get_value(df: pd.DataFrame, metric: str, year: int | None = None) -> float:
    subset = df[df["metric"].eq(metric)]
    if year is not None:
        subset = subset[subset["year"].eq(year)]
    if subset.empty:
        raise ValueError(f"Metric not found: {metric}, year={year}")
    return float(subset.iloc[0]["value"])


def save_bar(labels, values, title, ylabel, filename):
    plt.figure(figsize=(8, 5))
    plt.bar(labels, values)
    plt.title(title)
    plt.ylabel(ylabel)
    plt.xticks(rotation=20, ha="right")
    plt.tight_layout()
    plt.savefig(OUT / filename, dpi=200)
    plt.close()


def main():
    df = pd.read_csv(DATA)

    jobs_2024 = get_value(df, "bls_data_scientist_jobs", 2024)
    ds_growth = get_value(df, "bls_data_scientist_projected_growth", 2024)
    all_growth = get_value(df, "bls_all_occupations_projected_growth", 2024)
    median_pay = get_value(df, "bls_data_scientist_median_pay", 2024)

    ai_2023 = get_value(df, "stanford_ai_business_usage", 2023)
    ai_2024 = get_value(df, "stanford_ai_business_usage", 2024)
    genai_investment = get_value(df, "stanford_genai_private_investment", 2024)
    us_ai_investment = get_value(df, "stanford_us_private_ai_investment", 2024)

    review_all = get_value(df, "mckinsey_review_all_genai_outputs", 2025)
    review_low = get_value(df, "mckinsey_review_20_or_less_genai_outputs", 2025)
    wef_transform = get_value(df, "wef_ai_info_processing_transform_business", 2030)
    jobs_created = get_value(df, "wef_jobs_created_by_2030", 2030)
    jobs_displaced = get_value(df, "wef_jobs_displaced_by_2030", 2030)
    early_career_emp_change = get_value(df, "stanford_early_career_ai_exposed_emp_change", 2025)

    projected_jobs_2034 = jobs_2024 * (1 + ds_growth / 100)
    projected_added_jobs = projected_jobs_2034 - jobs_2024
    relative_growth_multiplier = ds_growth / all_growth
    ai_adoption_pp_change = ai_2024 - ai_2023
    ai_adoption_relative_change = ((ai_2024 / ai_2023) - 1) * 100
    genai_share_of_us_ai_private_investment = (genai_investment / us_ai_investment) * 100
    net_global_jobs_wef = jobs_created - jobs_displaced

    summary = pd.DataFrame([
        ["Data scientist jobs, 2024", jobs_2024, "jobs"],
        ["Projected data scientist jobs, 2034", round(projected_jobs_2034), "jobs"],
        ["Projected jobs added, 2024-2034", round(projected_added_jobs), "jobs"],
        ["DS projected growth vs all occupations", round(relative_growth_multiplier, 2), "x"],
        ["Data scientist median pay, 2024", median_pay, "USD/year"],
        ["AI adoption absolute change, 2023-2024", ai_adoption_pp_change, "percentage points"],
        ["AI adoption relative change, 2023-2024", round(ai_adoption_relative_change, 1), "percent"],
        ["GenAI investment as share of US private AI investment", round(genai_share_of_us_ai_private_investment, 1), "percent"],
        ["GenAI orgs reviewing all outputs", review_all, "percent"],
        ["GenAI orgs reviewing <=20% outputs", review_low, "percent"],
        ["WEF respondents expecting AI/info tech business transformation", wef_transform, "percent"],
        ["WEF projected net global job change by 2030", net_global_jobs_wef, "million jobs"],
        ["Early-career (22-25) employment change in most AI-exposed jobs (Stanford DEL)", early_career_emp_change, "percent (relative)"],
    ], columns=["result", "value", "unit"])

    summary.to_csv(OUT / "summary_results.csv", index=False)

    markdown_lines = ["# Audit Results\n"]
    markdown_lines.append("| Result | Value | Unit |")
    markdown_lines.append("|---|---:|---|")
    for _, row in summary.iterrows():
        markdown_lines.append(f"| {row['result']} | {row['value']} | {row['unit']} |")
    markdown_lines.append("\n## Interpretation\n")
    markdown_lines.append(
        "The numbers support a contradiction: data science remains a high-growth labor category, "
        "but the same AI adoption wave that increases demand for analytics also automates parts of "
        "the traditional analytics workflow. The safer career claim is not 'data science is dead'; "
        "it is 'generic tool-based data science is getting compressed.' The pressure is not evenly "
        "distributed: external payroll research (Stanford Digital Economy Lab, 'Canaries in the Coal "
        "Mine,' 2025) finds early-career workers (ages 22-25) in the most AI-exposed occupations down "
        "about 13% in relative employment, while their more experienced peers stay flat or grow. The "
        "entry rung is the most exposed part of the bundle."
    )
    (OUT / "summary_results.md").write_text("\n".join(markdown_lines), encoding="utf-8")

    save_bar(
        ["Data Scientists", "All Occupations"],
        [ds_growth, all_growth],
        "Projected Employment Growth, 2024-2034",
        "Percent growth",
        "projected_growth_comparison.png",
    )

    save_bar(
        ["2023", "2024"],
        [ai_2023, ai_2024],
        "Organizations Reporting AI Use",
        "Percent of organizations",
        "ai_adoption_2023_2024.png",
    )

    save_bar(
        ["Review all", "Review <=20%"],
        [review_all, review_low],
        "Human Review of GenAI Outputs",
        "Percent of genAI-using organizations",
        "genai_review_gap.png",
    )

    print(summary.to_string(index=False))
    print(f"\nSaved outputs to: {OUT}")


if __name__ == "__main__":
    main()
