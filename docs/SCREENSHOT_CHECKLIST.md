# Screenshot checklist

Save real screen captures under `docs/screenshots/`. No PNG screenshots have been fabricated or captured automatically. Entry numbers refer to BUILD_LOG.md and the corresponding case-study build steps. The capstone feature was removed in Entry 07; no capstone-result screenshot is required.

1. **`docs/screenshots/planning_layout.png`** — Capture the approved three-tab wireframe from the actual planning conversation. Build steps **04–05**. If the conversation is unavailable, retain the text description rather than reconstructing a supposed historical screenshot.
2. **`docs/screenshots/no_upload.png`** — Fresh session, **Overview**, showing “Please upload a CSV in the first tab.” Build step **11**.
3. **`docs/screenshots/upload_data.png`** — **Upload Data**, after uploading `demo_jobs.csv`, showing 120 rows, the date range, preview, and visible synthetic warning. Build steps **11–12**.
4. **`docs/screenshots/overview.png`** — **Overview**, all filters reset, showing the four metrics and charts. Scroll or capture a full-page image as needed; leave the synthetic warning visible. Build steps **11–12**.
5. **`docs/screenshots/sidebar_filters.png`** — **Overview** with all four sidebar filters clearly visible. Build step **11**.
6. **`docs/screenshots/empty_filter.png`** — **Overview**, after removing all Country selections, showing the friendly empty-filter message. Build step **11**. Reset filters afterward.
7. **`docs/screenshots/no_skills_selected.png`** — **Skill-Gap Diagnostic**, before choosing skills, showing its friendly selection prompt. Build step **11**.
8. **`docs/screenshots/skill_gap_diagnostic.png`** — **Skill-Gap Diagnostic**, all demo filters reset, with Python, SQL, Docker selected and target AI Engineer; show the ranked match chart. Build steps **11–12**.
9. **`docs/screenshots/salary_band_missing_skills.png`** — Same diagnostic state, scrolled to the salary band ($88,000–$142,500 USD/year, 70 records) and missing-skills counts. Build steps **11–12**.
10. **`docs/screenshots/original_data.png`** — **Upload Data** with `jobs.csv`: 500 derived rows, date range, and missing-date/skill notes. Build steps **07, 11–12**.
11. **`docs/screenshots/salary_unavailable.png`** — **Skill-Gap Diagnostic** with `jobs.csv`, Python and SQL selected, showing the unavailable salary-band message. Build step **11**.
12. **`docs/screenshots/bug_before_fix.png`** — **PowerShell environment state**, illustrating the actual Entry 11 Python alias issue. No historical screenshot was captured during the failure. If the alias still reproduces, run `python --version` in an unactivated shell and capture the actual “Python was not found” output. Caption it “Reproduction of the recorded environment issue, captured after implementation.” If it no longer reproduces, leave the placeholder and cite the log; do not invent an error screen. Build step **11**.
13. **`docs/screenshots/bug_after_fix.png`** — **The same PowerShell view**, running `.\.venv\Scripts\python.exe --version` successfully to show the explicit local interpreter. Build step **11**. Identify it as a verification capture, not an original historical image.
14. **`docs/screenshots/tests_passed.png`** — **PowerShell**, showing `.\.venv\Scripts\python.exe -m unittest discover -s tests -v` completing with nine checks and OK. Build steps **11–12**.
15. **`docs/screenshots/local_git.png`** — **PowerShell or GitHub Desktop**, showing the actual main branch, initial commit, and clean working tree. Build step **13**.

For any screenshot you cannot obtain, retain an explicit placeholder and explain what evidence is available. Do not present the missing-column validation message or synthetic-data warning as an application bug; both are intentional behavior.
