"""Behavior checks for CSV ingestion, calculations, and Streamlit empty states."""

import io
import unittest
from pathlib import Path
from unittest.mock import patch

import pandas as pd
from streamlit.testing.v1 import AppTest

from app import calculate_matches, date_range_label, prepare_data, skill_counts


ROOT = Path(__file__).resolve().parents[1]


class Upload(io.BytesIO):
    def __init__(self, contents, name="test.csv"):
        super().__init__(contents)
        self.name = name


def fixture():
    return pd.DataFrame({
        "job_id": ["1", "2", "3"],
        "posted_date": ["2023-01-01", "4/23/2023", "bad-date"],
        "title": ["Engineer"] * 3,
        "role_category": ["Engineer"] * 3,
        "seniority": ["Mid"] * 3,
        "salary_mid_usd": [100000, 200000, "bad-salary"],
        "skills": ["Python;python; SQL ", "python", None],
        "remote_status": ["Remote", "Hybrid", None],
        "industry": ["Software"] * 3,
        "country": ["US"] * 3,
        "source": ["test"] * 3,
        "source_url": [""] * 3,
        "data_origin": ["synthetic"] * 3,
    })


def run_with_upload(app, payload=None, name="test.csv"):
    upload = Upload(payload, name) if payload is not None else None
    # AppTest does not expose a file-selection action; exercise the CSV path
    # with an in-memory upload and use real Streamlit widgets for other actions.
    with patch("streamlit.file_uploader", return_value=upload):
        app.run(timeout=30)
    if len(app.exception):
        raise AssertionError(str([item.message for item in app.exception]))
    return app


class CalculationTests(unittest.TestCase):
    def test_salary_skill_and_date_calculations(self):
        data, notes, labels = prepare_data(fixture())
        self.assertEqual(skill_counts(data), {"python": 2, "sql": 1})
        self.assertEqual(labels["python"], "Python")
        self.assertEqual(date_range_label(data), "2023-01-01 to 2023-04-23")
        self.assertEqual(data["salary_mid_usd"].median(), 150000)
        self.assertAlmostEqual(data["salary_mid_usd"].notna().mean(), 2 / 3)
        self.assertTrue(notes)
        matched = calculate_matches(data, ["python"])
        self.assertEqual(matched["_match_pct"].iloc[0], 50)
        self.assertEqual(matched["_match_pct"].iloc[1], 100)
        self.assertTrue(pd.isna(matched["_match_pct"].iloc[2]))
        self.assertEqual(matched["_match_pct"].mean(), 75)
        qualifying = matched.loc[matched["_match_pct"].ge(50), "salary_mid_usd"].dropna()
        self.assertEqual(qualifying.quantile(0.25), 125000)
        self.assertEqual(qualifying.quantile(0.75), 175000)

    def test_required_headers_and_empty_file(self):
        with self.assertRaisesRegex(ValueError, "Missing required columns: skills"):
            prepare_data(fixture().drop(columns="skills"))
        with self.assertRaisesRegex(ValueError, "no rows"):
            prepare_data(fixture().iloc[:0])
        # Optional bounds are deliberately absent in this fixture.
        prepare_data(fixture())

    def test_nonpositive_infinite_and_missing_salaries_are_excluded(self):
        raw = fixture()
        raw["salary_mid_usd"] = [0, float("inf"), None]
        data, _, _ = prepare_data(raw)
        self.assertTrue(data["salary_mid_usd"].isna().all())

    def test_original_data_and_demo_are_kept_distinct(self):
        original, _, _ = prepare_data(pd.read_csv(ROOT / "jobs.csv"))
        self.assertEqual(len(original), 500)
        self.assertEqual(original["data_origin"].value_counts().to_dict(), {"derived": 500})
        self.assertEqual(int(original["_skill_list"].map(bool).sum()), 20)
        matched = calculate_matches(original, list(skill_counts(original)))
        self.assertTrue(matched.loc[matched["_match_pct"].ge(50), "salary_mid_usd"].dropna().empty)
        demo, _, _ = prepare_data(pd.read_csv(ROOT / "demo_jobs.csv"))
        self.assertEqual(len(demo), 120)
        self.assertTrue(demo["data_origin"].eq("synthetic").all())
        demo_matches = calculate_matches(demo, ["python", "sql", "docker"])
        self.assertFalse(demo_matches.loc[demo_matches["_match_pct"].ge(50), "salary_mid_usd"].dropna().empty)


class InterfaceTests(unittest.TestCase):
    def test_no_upload_exact_tabs_and_prompts(self):
        app = run_with_upload(AppTest.from_file(str(ROOT / "app.py")))
        self.assertEqual([tab.label for tab in app.tabs], ["Upload Data", "Overview", "Skill-Gap Diagnostic"])
        self.assertEqual(sum(item.value == "Please upload a CSV in the first tab." for item in app.info), 2)

    def test_demo_metrics_match_missing_skills_and_empty_filter(self):
        payload = (ROOT / "demo_jobs.csv").read_bytes()
        app = run_with_upload(AppTest.from_file(str(ROOT / "app.py")), payload, "demo_jobs.csv")
        self.assertTrue(any("Synthetic" in item.value or "synthetic" in item.value for item in app.warning))
        self.assertEqual(app.metric[2].value, "120")
        self.assertEqual(app.metric[4].value, "33.3%")
        self.assertEqual(app.metric[5].value, "90.0%")
        app.multiselect(key="owned_skills").set_value(["python", "sql", "docker"])
        run_with_upload(app, payload, "demo_jobs.csv")
        self.assertTrue(any("percentile" in item.label for item in app.metric))
        self.assertTrue(any("Missing skill" in frame.value.columns for frame in app.dataframe))
        app.multiselect(key="filter_country").set_value([])
        run_with_upload(app, payload, "demo_jobs.csv")
        self.assertEqual(sum("No postings match these filters" in item.value for item in app.info), 2)
        app.button[0].click()
        run_with_upload(app, payload, "demo_jobs.csv")
        self.assertEqual(len(app.session_state["data"]), 120)
        self.assertFalse(any("No postings match these filters" in item.value for item in app.info))
        self.assertFalse(any("default value" in item.value for item in app.warning))

    def test_missing_headers_rejected_and_stale_data_cleared(self):
        app = AppTest.from_file(str(ROOT / "app.py"))
        run_with_upload(app, (ROOT / "demo_jobs.csv").read_bytes())
        bad = fixture().drop(columns="skills").to_csv(index=False).encode()
        run_with_upload(app, bad)
        self.assertTrue(any("Missing required columns: skills" in item.value for item in app.error))
        self.assertEqual(sum(item.value == "Please upload a CSV in the first tab." for item in app.info), 2)
        self.assertNotIn("data", app.session_state)

    def test_original_salary_band_unavailable_and_upload_removal(self):
        payload = (ROOT / "jobs.csv").read_bytes()
        app = run_with_upload(AppTest.from_file(str(ROOT / "app.py")), payload, "jobs.csv")
        app.multiselect(key="owned_skills").set_value(["python", "sql"])
        run_with_upload(app, payload, "jobs.csv")
        self.assertTrue(any("Salary data unavailable" in item.value for item in app.info))
        run_with_upload(app)
        self.assertNotIn("data", app.session_state)
        self.assertEqual(sum(item.value == "Please upload a CSV in the first tab." for item in app.info), 2)

    def test_all_missing_salary_and_all_missing_skills(self):
        raw = fixture()
        raw["salary_mid_usd"] = None
        raw["skills"] = None
        payload = raw.to_csv(index=False).encode()
        app = run_with_upload(AppTest.from_file(str(ROOT / "app.py")), payload)
        self.assertTrue(any(item.label == "Median salary — USD/year" and item.value == "Unavailable" for item in app.metric))
        self.assertTrue(any("do not list skills" in item.value for item in app.info))


if __name__ == "__main__":
    unittest.main(verbosity=2)
