# Submission checklist

The materials are prepared locally. Creating an external Google Doc, recording a video, and publishing to GitHub remain manual steps.

## 1. Google Doc

- [ ] Open `docs/CASE_STUDY.md` and verify all sections against BUILD_LOG.md and the project.
- [ ] Capture the available screenshots listed in `docs/SCREENSHOT_CHECKLIST.md`.
- [ ] Create a Google Doc titled **AI Skill-Gap & Job Market Analyzer — Case Study**.
- [ ] Paste/import the case-study content and apply readable headings, code blocks, and tables. Preserve the exact user prompts.
- [ ] Render the Mermaid architecture diagram or reproduce its documented nodes and connections as a Google Docs diagram; replace the Mermaid code block with the diagram if desired.
- [ ] Replace screenshot placeholders with actual images and captions. Clearly label bug reproductions and any unavailable historical images.
- [ ] Keep the original derived data and synthetic demo data distinguished. Do not claim a live-market data collection or a completed external submission.
- [ ] Check the instructor's sharing requirements and copy the actual Google Doc link.

Google Doc link: **[ADD ACTUAL LINK AFTER CREATION]**

## 2. Video demo — 5 minutes or less

- [ ] Follow `docs/DEMO_SCRIPT.md` and complete its Before recording checklist.
- [ ] Rehearse the full recording with a timer; demonstrate the CSV upload, Overview, and Skill-Gap Diagnostic.
- [ ] Show one exact prompt and one actual issue from the build log.
- [ ] Identify demo rows as synthetic and explain the original file's coverage limitation.
- [ ] Do not include a capstone generator; it was removed from scope.
- [ ] Record clear screen video and audio; trim any delays so the total is at most 5:00.
- [ ] Upload to the destination required for your submission, check playback and permissions, and copy the actual video link.

Video link: **[ADD ACTUAL LINK AFTER UPLOAD]**

## 3. GitHub link

- [ ] Review the local repository, README, BUILD_LOG, case study, and demo dataset.
- [ ] Add actual screenshot files and commit them locally when ready.
- [ ] Confirm `.venv`, caches, `.env`, and `.streamlit/secrets.toml` remain untracked; never include credentials.
- [ ] Create a GitHub repository with the visibility required for submission. Avoid automatically creating a separate README if pushing this existing local repository.
- [ ] In GitHub Desktop, add this local repository and publish it, or use the commands below with the actual repository URL.
- [ ] Open the resulting GitHub page, verify the files and screenshot paths, and check access as a reviewer.
- [ ] Copy the actual repository link; a local commit is not a completed GitHub submission.

```text
git remote add origin <ACTUAL_GITHUB_REPOSITORY_URL>
git push -u origin main
```

GitHub link: **[ADD ACTUAL LINK AFTER PUBLISHING]**

Git is available in GitHub Desktop's bundled runtime in the development environment; use GitHub Desktop or install/configure Git on PATH before running bare `git` commands in PowerShell.

## Final review

- [ ] All three actual links are filled in and accessible.
- [ ] Screenshot placeholders are replaced where evidence exists; missing historical captures are identified honestly.
- [ ] Video length is no greater than five minutes.
- [ ] No API key or invented market evidence appears in any deliverable.
