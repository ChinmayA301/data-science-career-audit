"""
Fetch the raw job-posting datasets used by job_posting_nlp.py.

Both datasets are public and downloaded on demand into data/raw/ (gitignored).
They are NOT committed to the repo because of size (~260 MB combined).

Sources
-------
1. lukebarousse/data_jobs  (~785k postings, calendar year 2023)
   Real job postings collected from Google job listings via SerpAPI.
   License: CC0 / public. https://huggingface.co/datasets/lukebarousse/data_jobs

2. NextGig-Rocks/global-job-postings-multi-ats  (~113k postings, snapshot ~June 2026)
   Real multi-ATS global job postings. License: CC-BY-4.0.
   https://huggingface.co/datasets/NextGig-Rocks/global-job-postings-multi-ats
"""

from pathlib import Path
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"

FILES = {
    "data_jobs_2023.csv": (
        "https://huggingface.co/datasets/lukebarousse/data_jobs/"
        "resolve/main/data_jobs.csv"
    ),
    "nextgig_jobs_2026-06.parquet": (
        "https://huggingface.co/datasets/NextGig-Rocks/global-job-postings-multi-ats/"
        "resolve/main/nextgig_jobs_2026-06.parquet"
    ),
}


def main():
    RAW.mkdir(parents=True, exist_ok=True)
    for name, url in FILES.items():
        dest = RAW / name
        if dest.exists():
            print(f"[skip] {name} already present ({dest.stat().st_size/1e6:.0f} MB)")
            continue
        print(f"[download] {name} ...")
        urllib.request.urlretrieve(url, dest)
        print(f"[done]  {name} ({dest.stat().st_size/1e6:.0f} MB)")


if __name__ == "__main__":
    main()
