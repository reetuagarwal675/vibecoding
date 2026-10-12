"""Local job-market exploration with transparent skill-overlap calculations."""

from __future__ import annotations

import hashlib
import io
from collections import Counter
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st


# CSV contract: salary bounds are optional, as approved during planning.
APP_DIR = Path(__file__).resolve().parent
REQUIRED_COLUMNS = (
    "job_id", "posted_date", "title", "role_category", "seniority",
    "salary_mid_usd", "skills", "remote_status", "industry", "country",
    "source", "source_url", "data_origin",
)
FILTER_COLUMNS = {
    "role_category": "Role category",
    "seniority": "Seniority",
    "remote_status": "Remote status",
    "country": "Country",
}
UPLOAD_PROMPT = "Please upload a CSV in the first tab."
EMPTY_PROMPT = "No postings match these filters. Try selecting more values or resetting the filters."


def split_skills(value: object) -> list[str]:
    """Normalize and deduplicate skills within each individual posting."""
    if pd.isna(value):
        return []
    return sorted({part.strip().casefold() for part in str(value).split(";") if part.strip()})


def prepare_data(raw: pd.DataFrame) -> tuple[pd.DataFrame, list[str], dict[str, str]]:
    """Validate headers and clean values without inventing missing information."""
    raw = raw.copy()
    raw.columns = raw.columns.str.strip()
    if raw.columns.duplicated().any():
        raise ValueError("The CSV contains duplicate column names. Please give every column a unique name.")
    missing = sorted(set(REQUIRED_COLUMNS) - set(raw.columns))
    if missing:
        raise ValueError("Missing required columns: " + ", ".join(missing))
    if raw.empty:
        raise ValueError("The CSV has column headers but no rows. Please upload a CSV containing postings.")
    if any(str(column).startswith("_") for column in raw.columns):
        raise ValueError("Column names beginning with '_' are reserved for analysis. Please rename them.")

    notes: list[str] = []
    data = raw.copy()
    # Accept common CSV date formats; invalid dates remain unavailable.
    data["posted_date"] = pd.to_datetime(raw["posted_date"], errors="coerce", format="mixed", utc=True).dt.tz_convert(None)
    invalid_dates = int(data["posted_date"].isna().sum())
    if invalid_dates:
        notes.append(f"{invalid_dates:,} rows have missing or invalid posting dates; the date range uses available dates only.")

    original_salary = raw["salary_mid_usd"].astype("string").str.strip()
    numeric_salary = pd.to_numeric(raw["salary_mid_usd"], errors="coerce")
    valid_salary = numeric_salary.notna() & numeric_salary.gt(0) & numeric_salary.lt(float("inf"))
    data["salary_mid_usd"] = numeric_salary.where(valid_salary)
    rejected_salary = int((original_salary.notna() & original_salary.ne("") & ~valid_salary).sum())
    if rejected_salary:
        notes.append(f"{rejected_salary:,} nonempty salary values are invalid or nonpositive and were excluded from salary calculations.")

    for column in FILTER_COLUMNS:
        data[column] = raw[column].fillna("").astype(str).str.strip().replace("", "Unknown")
    data["data_origin"] = raw["data_origin"].fillna("").astype(str).str.strip().str.casefold().replace("", "unknown")
    data["_skill_list"] = raw["skills"].apply(split_skills)
    skill_labels: dict[str, str] = {}
    for value in raw["skills"].dropna():
        for skill in str(value).split(";"):
            skill = skill.strip()
            if skill:
                skill_labels.setdefault(skill.casefold(), skill)
    duplicate_ids = int(raw["job_id"].dropna().duplicated().sum())
    if duplicate_ids:
        notes.append(f"{duplicate_ids:,} repeated job IDs found. Each CSV row is counted as one posting, as specified.")
    unknown_origins = sorted(set(data["data_origin"]) - {"real", "derived", "synthetic"})
    if unknown_origins:
        notes.append("Unrecognized data-origin labels are retained as supplied: " + ", ".join(unknown_origins))
    no_skills = int(data["_skill_list"].map(len).eq(0).sum())
    if no_skills:
        notes.append(f"{no_skills:,} rows have no listed skills and are excluded from skill-match calculations.")
    return data, notes, skill_labels


def skill_counts(data: pd.DataFrame) -> Counter:
    """Each normalized skill contributes at most one count per posting."""
    return Counter(skill for skills in data["_skill_list"] for skill in skills)


def calculate_matches(data: pd.DataFrame, selected_skills: list[str]) -> pd.DataFrame:
    """Calculate posting-level overlap; no-skill postings have an undefined match."""
    matched = data.copy()
    owned = set(selected_skills)
    matched["_match_pct"] = matched["_skill_list"].map(
        lambda skills: 100 * len(owned.intersection(skills)) / len(skills) if skills else float("nan")
    )
    return matched


def date_range_label(data: pd.DataFrame) -> str:
    dates = data["posted_date"].dropna()
    if dates.empty:
        return "Unavailable"
    return f"{dates.min():%Y-%m-%d} to {dates.max():%Y-%m-%d}"


# Keep the uploaded dataset and analysis choices in this browser session.
def clear_uploaded_state() -> None:
    for key in list(st.session_state):
        if key in {"data", "raw_data", "data_notes", "skill_labels", "upload_digest", "uploaded_name", "owned_skills", "target_role"} or key.startswith("filter_"):
            del st.session_state[key]


def render_upload() -> None:
    st.subheader("Upload your job-market CSV")
    st.caption("Upload your own data or download the included, explicitly synthetic demo CSV below.")
    demo_path = APP_DIR / "demo_jobs.csv"
    if demo_path.exists():
        st.download_button("Download synthetic demo CSV", demo_path.read_bytes(), file_name="demo_jobs.csv", mime="text/csv")
    uploaded = st.file_uploader("Choose a job-market CSV", type=["csv"], key="csv_upload")
    if uploaded is None:
        clear_uploaded_state()
        st.info("Choose a CSV to begin. Your upload is kept only in the current Streamlit session.")
        return
    payload = uploaded.getvalue()
    digest = hashlib.sha256(payload).hexdigest()
    if digest != st.session_state.get("upload_digest"):
        clear_uploaded_state()
        try:
            raw = pd.read_csv(io.BytesIO(payload), encoding="utf-8-sig")
            data, notes, labels = prepare_data(raw)
        except (ValueError, UnicodeDecodeError, pd.errors.ParserError, pd.errors.EmptyDataError) as exc:
            st.error(f"Could not load this CSV. {exc}")
            return
        st.session_state.update(data=data, raw_data=raw, data_notes=notes, skill_labels=labels, upload_digest=digest, uploaded_name=uploaded.name)
    data = st.session_state["data"]
    st.success(f"Loaded {st.session_state['uploaded_name']}")
    row_col, date_col = st.columns([1, 2])
    row_col.metric("Uploaded rows — rows", f"{len(data):,}")
    date_col.metric("Posting date range — dates", date_range_label(data))
    synthetic_rows = int(data["data_origin"].eq("synthetic").sum())
    if synthetic_rows:
        st.warning(f"Synthetic data: {synthetic_rows:,} of {len(data):,} rows are mock records, not observed job postings. Treat these results as a demonstration.")
    origins = data["data_origin"].value_counts()
    st.caption("Data origin: " + " · ".join(f"{origin}: {count:,} rows" for origin, count in origins.items()))
    with st.expander("Data quality and calculation notes", expanded=bool(st.session_state["data_notes"])):
        for note in st.session_state["data_notes"]:
            st.write(note)
        st.write("Salary calculations use valid positive salary_mid_usd values. salary_min_usd and salary_max_usd are optional.")
    st.subheader("Data preview — first 20 rows")
    st.dataframe(st.session_state["raw_data"].head(20), hide_index=True, width="stretch")


def render_filters(data: pd.DataFrame) -> pd.DataFrame:
    filtered = data
    with st.sidebar:
        st.header("Shared filters")
        st.caption("Apply to Overview and Skill-Gap Diagnostic. Upload preview shows the full file.")
        if st.button("Reset filters"):
            for column in FILTER_COLUMNS:
                st.session_state[f"filter_{column}"] = sorted(data[column].unique())
        for column, label in FILTER_COLUMNS.items():
            options = sorted(data[column].unique())
            filter_key = f"filter_{column}"
            if filter_key not in st.session_state:
                st.session_state[filter_key] = options
            chosen = st.multiselect(label, options, key=filter_key)
            filtered = filtered[filtered[column].isin(chosen)]
        st.caption(f"Showing {len(filtered):,} of {len(data):,} postings. Clearing a filter selects no rows.")
    return filtered


# Overview counts all filtered rows; skill charts disclose their coverage.
def render_overview(data: pd.DataFrame, labels: dict[str, str]) -> None:
    if data.empty:
        st.info(EMPTY_PROMPT)
        return
    st.subheader("Job-market overview")
    salaries = data["salary_mid_usd"].dropna()
    remote_pct = 100 * data["remote_status"].str.casefold().eq("remote").mean()
    salary_pct = 100 * data["salary_mid_usd"].notna().mean()
    metrics = st.columns(4)
    metrics[0].metric("Postings — postings", f"{len(data):,}")
    metrics[1].metric("Median salary — USD/year", f"${salaries.median():,.0f}" if not salaries.empty else "Unavailable")
    metrics[2].metric("Remote — % of postings", f"{remote_pct:.1f}%")
    metrics[3].metric("Listed salary — % of postings", f"{salary_pct:.1f}%")
    st.caption(f"Salary sample: {len(salaries):,} postings. Remote means Remote only; Hybrid and Unknown remain in the denominator.")
    counts = skill_counts(data)
    if counts:
        top = pd.DataFrame([(labels[skill], count) for skill, count in sorted(counts.items(), key=lambda item: (-item[1], item[0]))[:10]], columns=["Skill", "Posting count"])
        fig = px.bar(top, x="Posting count", y="Skill", orientation="h", title="Top 10 skills by posting count", labels={"Posting count": "Postings listing the skill (postings)", "Skill": "Skill"}, color_discrete_sequence=["#2563eb"])
        fig.update_yaxes(categoryorder="array", categoryarray=top["Skill"].tolist()[::-1])
        st.plotly_chart(fig, width="stretch", key="top_skills_chart")
        st.caption(f"Skill coverage: {data['_skill_list'].map(bool).sum():,} of {len(data):,} postings list at least one skill.")
    else:
        st.info("These postings do not list skills. Select other filters or upload a dataset with skills.")
    role_mix = data["role_category"].value_counts().rename_axis("Role").reset_index(name="Posting count")
    fig = px.bar(role_mix, x="Role", y="Posting count", title="Role mix by posting count", labels={"Role": "Role category", "Posting count": "Number of postings (postings)"}, color_discrete_sequence=["#14b8a6"])
    st.plotly_chart(fig, width="stretch", key="role_mix_chart")


# Diagnostics use per-posting overlap, then equal weighting within each role.
def render_diagnostic(data: pd.DataFrame, full_data: pd.DataFrame, labels: dict[str, str]) -> None:
    if data.empty:
        st.info(EMPTY_PROMPT)
        return
    st.subheader("Your skill-gap diagnostic")
    skill_options = sorted(skill_counts(full_data))
    owned = st.multiselect("Skills you already have", skill_options, format_func=lambda value: labels[value], key="owned_skills", help="Options come from the entire uploaded CSV. Select your existing skills.")
    roles = sorted(data["role_category"].unique())
    if st.session_state.get("target_role") not in roles:
        st.session_state["target_role"] = roles[0]
    target = st.selectbox("Your target role", roles, key="target_role")
    if not owned:
        st.info("Select at least one skill you already have to see your match and skill gaps.")
        return
    matched = calculate_matches(data, owned)
    available = matched.dropna(subset=["_match_pct"])
    if not available.empty:
        ranked = available.groupby("role_category")["_match_pct"].agg(["mean", "count"]).reset_index().rename(columns={"role_category": "Role", "mean": "Match (%)", "count": "Postings with skills"}).sort_values(["Match (%)", "Role"], ascending=[False, True])
        fig = px.bar(ranked, x="Match (%)", y="Role", orientation="h", title="Average skill match by role", labels={"Match (%)": "Average posting skill overlap (%)", "Role": "Role category"}, hover_data=["Postings with skills"], color_discrete_sequence=["#2563eb"])
        fig.update_xaxes(range=[0, 100])
        fig.update_yaxes(categoryorder="array", categoryarray=ranked["Role"].tolist()[::-1])
        st.plotly_chart(fig, width="stretch", key="match_chart")
        st.caption(f"Match = selected skills ÷ listed skills for each posting, averaged by role. Based on {len(available):,} of {len(data):,} filtered postings; postings without skills are excluded. This is not a hiring probability.")
    else:
        st.info("No filtered postings list skills, so a match percentage cannot be calculated.")
    qualified = matched.loc[matched["_match_pct"].ge(50), "salary_mid_usd"].dropna()
    st.subheader("Salary band for postings with at least 50% match")
    if qualified.empty:
        st.info("Salary data unavailable: no filtered postings have both at least 50% skill match and a valid listed salary.")
    else:
        lower, upper = qualified.quantile([0.25, 0.75])
        st.metric("25th–75th percentile salary — USD/year", f"${lower:,.0f} – ${upper:,.0f}")
        st.caption(f"Based on {len(qualified):,} qualifying postings across all filtered roles. This is an observed salary distribution, not a salary prediction.")
    st.subheader(f"Top 5 missing skills — {target}")
    target_data = data[data["role_category"].eq(target)]
    target_with_skills = int(target_data["_skill_list"].map(bool).sum())
    missing = [(labels[skill], count) for skill, count in sorted(skill_counts(target_data).items(), key=lambda item: (-item[1], item[0])) if skill not in set(owned)][:5]
    if not target_with_skills:
        st.info("This target role has no listed skills in the filtered data. Try another role or dataset.")
    elif not missing:
        st.success("You selected every skill listed for this target role in the filtered data.")
    else:
        st.dataframe(pd.DataFrame(missing, columns=["Missing skill", "Posting count"]), hide_index=True, width="stretch")
    st.caption(f"Target-role sample: {len(target_data):,} postings; {target_with_skills:,} list skills. Counts represent postings, not repeated mentions.")


def main() -> None:
    st.set_page_config(page_title="AI Skill-Gap & Job Market Analyzer", page_icon="📊", layout="wide")
    st.title("AI Skill-Gap & Job Market Analyzer")
    st.caption("Explore job-market data and compare your skills with listed requirements. No API key required.")
    upload_tab, overview_tab, diagnostic_tab = st.tabs(["Upload Data", "Overview", "Skill-Gap Diagnostic"])
    with upload_tab:
        render_upload()
    data = st.session_state.get("data")
    if data is None:
        with overview_tab:
            st.info(UPLOAD_PROMPT)
        with diagnostic_tab:
            st.info(UPLOAD_PROMPT)
        return
    filtered = render_filters(data)
    if data["data_origin"].eq("synthetic").any():
        st.warning("This upload contains synthetic mock data. Charts and diagnostics are demonstration results.")
    with overview_tab:
        render_overview(filtered, st.session_state["skill_labels"])
    with diagnostic_tab:
        render_diagnostic(filtered, data, st.session_state["skill_labels"])


if __name__ == "__main__":
    main()
