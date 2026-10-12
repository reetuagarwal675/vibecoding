# Demo script — maximum 5 minutes

Use the actual app and the included **synthetic** demo dataset. The capstone generator was explicitly removed in BUILD_LOG Entry 07 and has no demo segment.

## Before recording

- [ ] Open the project folder and run `.\.venv\Scripts\python.exe -m streamlit run app.py` if a server is not already running.
- [ ] Open http://127.0.0.1:8501 (or the URL printed by your server).
- [ ] Have `demo_jobs.csv`, `jobs.csv`, `BUILD_LOG.md`, and the case study ready.
- [ ] Rehearse selecting **Python**, **SQL**, and **Docker**, with target **AI Engineer**.
- [ ] Keep the synthetic warning visible and use **Reset filters** before reporting the baseline figures.
- [ ] Prepare BUILD_LOG Entry 12's exact mock-data prompt and Entry 11's actual Python environment issue. Do not invent an application crash.
- [ ] Prepare screenshots of the recorded environment issue if available. A later reproduction must be labeled as a reproduction, not a historical capture.
- [ ] Set a five-minute timer, check audio and screen legibility, and hide unrelated windows or personal information.

## 0:00–0:30 — The problem

**Say:** “Job seekers need a way to compare their skills with listed requirements without confusing incomplete data with market certainty. This app lets me upload a CSV, explore role and skill counts, and identify skills I am missing for a target role.”

**Actions:**
1. Show the app title and the three tabs.
2. Click **Overview** before uploading; show “Please upload a CSV in the first tab.”
3. Return to **Upload Data**.

## 0:30–1:30 — How I used the AI coding tool

**Say:** “I used OpenAI Codex. I approved a visual layout and calculation rules before authorizing implementation. One exact prompt in Entry 12 was: ‘This is a demo application fill in the mock data if needed’. Codex created a separate synthetic CSV and kept the supplied data separate.”

“A real issue in Entry 11 was that the Python command pointed to the Windows Store alias and reported ‘Python was not found’. The fix was to locate a managed interpreter, create a local virtual environment, and run its explicit Python executable. The build log records this environment issue, plus the filter-reset warning found and fixed during testing.”

**Actions:**
1. Switch to `BUILD_LOG.md`; locate Entry 12 and point to its exact prompt.
2. Locate Entry 11 and show the Python alias issue and fix.
3. Show actual bug screenshots if captured, or show the log text and clearly state that no historical screenshot was captured.
4. Return to the app by 1:30.

## 1:30–4:00 — Live walkthrough

### 1:30–2:05 — Upload Data

**Actions:**
1. Click **Upload Data** → **Browse files**.
2. Select `demo_jobs.csv` from the project folder and click **Open**.
3. Point to **120 rows**, the **2026-07-01 to 2026-09-28** date range, and the synthetic warning.
4. Briefly show the preview and the notes explaining missing fields.

**Say:** “All 120 rows here are synthetic. They are for demonstrating the workflow, not for drawing real market conclusions.”

### 2:05–2:45 — Overview and shared filters

**Actions:**
1. Click **Overview** and **Reset filters** in the sidebar.
2. Show 120 postings, median **$110,500 USD/year**, **33.3% Remote**, and **90.0% with salary**.
3. Scroll through the top-skills and role-mix charts; point to titles and labeled axes.
4. In **Country**, remove each selected tag (**CA**, **IN**, **UK**, **US**) using its x. Show the empty-filter message.
5. Click **Reset filters** to restore all records.

**Say:** “The filters affect both analysis tabs. Empty selections show a helpful message rather than an error.”

### 2:45–4:00 — Skill-Gap Diagnostic

**Actions:**
1. Click **Skill-Gap Diagnostic**. Show the prompt to select skills.
2. Open **Skills you already have** and select **Python**, **SQL**, and **Docker**. Close the dropdown.
3. Set **Your target role** to **AI Engineer**.
4. Show the ranked match chart. Explain that it averages each posting's skill overlap, excluding records without skills.
5. Scroll to the salary band: **$88,000–$142,500 USD/year**, based on **70** qualifying demo records across all filtered roles.
6. Show missing skills for AI Engineer: **RAG — 24 postings**, **LLM Evaluation — 8 postings**. There are only two missing skills in this example, so the app does not fabricate five.

**Say:** “My selected skills determine posting-level overlap. The target role determines the missing-skills list; the salary band covers all filtered records with at least 50% match and a listed salary. Match is a simple overlap measure, not a hiring score.”

## 4:00–4:40 — Limitations and data honesty

**Actions:**
1. Click **Upload Data** → the uploader's **Browse files** control and select `jobs.csv` to replace the demo upload.
2. Point to 500 rows and the derived-origin label.
3. Show the quality notes: only 20 rows have skills; 480 have salaries and missing dates.
4. If time permits, click **Skill-Gap Diagnostic**, select **Python** and **SQL**, and show “Salary data unavailable.”

**Say:** “The original file labels all 500 rows as derived. Its dated rows are from 2023. Skills and salaries do not overlap across these rows, so the app cannot show a matched salary band. The separate synthetic dataset demonstrates that feature honestly. Any future skill-pay comparison would show association, not causation.”

## 4:40–5:00 — Learnings and next steps

**Say:** “The main lessons were to approve clear calculation rules, inspect data coverage before interpreting charts, and test empty states. Next, I would seek a dataset with skills and salaries on the same real records and improve provenance documentation. The code, exact prompts, fixes, and submission instructions are saved in the project.”

**Actions:**
1. Show the case study and submission checklist filenames.
2. If GitHub has been published later, show the actual repository link; otherwise say publishing is still pending.
3. Stop recording by 5:00.
