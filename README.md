# AI Skill-Gap & Job Market Analyzer

AI Skill-Gap & Job Market Analyzer is a Streamlit app that explores uploaded job-market CSVs and compares your selected skills with the skills listed in those records. It is for job seekers, learners, and instructors who want transparent market summaries and a simple skill-gap demonstration.

## Features

### Upload Data
- Manually upload a CSV, validate required columns, and share it across tabs through session state.
- View the first 20 rows, row count, available date range, and data-quality notes.
- See a visible warning whenever synthetic rows are present; download the included synthetic demo CSV.

### Overview
- Filter by role category, seniority, remote status, and country; filters also affect diagnostics.
- View posting count, median annual salary in USD, remote percentage, and salary-availability percentage.
- Explore the top 10 skills by posting count and role mix with labeled Plotly bar charts.
- Receive a friendly message when no rows match the filters; use **Reset filters** to recover.

### Skill-Gap Diagnostic
- Select your skills and a target role.
- Compare average posting-level skill overlap by role; postings without skills are excluded.
- View the 25th–75th salary percentiles across all filtered postings with at least 50% match.
- See up to five missing target-role skills and their posting counts.

## Data

The user supplied `jobs.csv`. According to its `source` and `source_url` columns, 20 records use `luke_posting` and point to [Luke Barousse's data_jobs dataset](https://huggingface.co/datasets/lukebarousse/data_jobs); 480 use `aijobs_salary` and point to [the salaries.csv URL in the supplied metadata](https://huggingface.co/datasets/kestra/datasets/raw/main/csv/salaries.csv). This repository does not include the original extraction or transformation process; these are source attributions from the CSV, not an independent provenance audit.

| File | Rows | Available posting dates | Real | Derived | Synthetic |
|---|---:|---|---:|---:|---:|
| `jobs.csv` | 500 | 2023-01-03 to 2023-11-25 | 0 | 500 | 0 |
| `demo_jobs.csv` | 120 | 2026-07-01 to 2026-09-28 | 0 | 0 | 120 |

The original date range covers only 20 dated records; 480 dates are missing. Its 20 skill-bearing records have no salary, and its 480 salary-bearing records have no skills, so the original CSV cannot produce a salary band for skill-matched postings.

**All 120 rows of `demo_jobs.csv` are synthetic mock data.** They were generated locally by `scripts/generate_demo.py`, with `data_origin=synthetic` and `source=local_synthetic_demo`. They demonstrate the app and are not real job-market evidence; the original CSV is kept separate and unchanged. The demo has 114 rows with skills and 108 with salaries.

Required columns:

```text
job_id, posted_date, title, role_category, seniority, salary_mid_usd,
skills, remote_status, industry, country, source, source_url, data_origin
```

`salary_min_usd` and `salary_max_usd` are optional. Skills are semicolon-separated. Every CSV row counts as one posting; blank filter fields display as Unknown. Clearing all values in a filter selects no rows.

## Setup and run

Use Python 3.10–3.14. From this project folder, create and activate a virtual environment if you do not already have one:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
streamlit run app.py
```

On macOS/Linux, activate with `source .venv/bin/activate` instead.

The project's Windows `.venv` has already been created and dependencies installed in the development workspace. You can bypass activation and the Windows Python alias using:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m streamlit run app.py
```

Open the URL printed by Streamlit (normally http://localhost:8501). In **Upload Data**, click **Browse files** and select `jobs.csv` or `demo_jobs.csv`; neither file is loaded automatically. The live server in the development workspace uses http://127.0.0.1:8501. Stop the server with Ctrl+C in its terminal before starting another on that port.

## API key

No API key is needed or read by this application. The optional external API integration was removed during scope clarification, so there is no key-setting step. `.env` and `.streamlit/secrets.toml` are ignored by Git; no credential is included in the code or project materials.

## Screenshots

These are placeholders; capture the actual app and save the images using [the screenshot checklist](docs/SCREENSHOT_CHECKLIST.md).

![Upload Data](docs/screenshots/upload_data.png)
![Overview](docs/screenshots/overview.png)
![Skill-Gap Diagnostic](docs/screenshots/skill_gap_diagnostic.png)

## Limitations

- Salary data is sparse in the skill-bearing subset: none of the original 20 skill-bearing rows has a salary. Overall salary availability is 480/500, but that does not establish skill-associated pay.
- Skill pay premiums, if studied in future, would show correlation rather than causation. This app does not calculate pay premiums or predict individual compensation.
- Match percentage measures simple skill overlap, not proficiency, experience, hiring probability, or semantic equivalence. For example, distinct spellings or aliases beyond case and surrounding spaces remain distinct skills.
- The original data combines source categories and does not establish that every salary record is a current job posting. Row counts should not be treated as a verified live-market total.
- Historical data, missing dates, and uneven skill coverage limit representativeness. Missing and invalid values are reported or excluded rather than filled with invented facts.
- The demo dataset is entirely synthetic; its salary ranges and frequencies are invented for demonstration.
- Uploaded data persists only in the current Streamlit session. No capstone generator, LLM integration, or live job scraping is implemented.

## Validation

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe -m pip check
```

Nine behavior checks passed; dependency checks and syntax compilation passed. Streamlit AppTest uses an in-memory upload substitute and actual selection/filter widgets; native browser upload and screenshots still need manual review. See [BUILD_LOG.md](BUILD_LOG.md) for observed issues and fixes.

## Built with AI

Built with **OpenAI Codex**, with user approvals for layout and calculation rules. Read [the case study](docs/CASE_STUDY.md), [the five-minute demo script](docs/DEMO_SCRIPT.md), and [the submission checklist](docs/SUBMISSION_CHECKLIST.md).

## Local version control

The project is tracked in a local Git repository on branch `main`. GitHub publishing is a later manual step; no GitHub repository URL or completed push is claimed.
