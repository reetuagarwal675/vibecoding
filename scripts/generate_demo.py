"""Reproducible mock data; every row is explicitly synthetic, never market evidence."""

import csv
from datetime import date, timedelta
from pathlib import Path


def main() -> None:
    destination = Path(__file__).resolve().parents[1] / "demo_jobs.csv"
    columns = "job_id posted_date title role_category seniority salary_min_usd salary_max_usd salary_mid_usd skills remote_status industry country source source_url data_origin".split()
    roles = [
        ("AI Engineer", ["Python", "RAG", "Docker", "SQL", "LLM Evaluation"], 120000),
        ("Data Scientist", ["Python", "SQL", "Statistics", "pandas", "Machine Learning"], 105000),
        ("ML Engineer", ["Python", "Docker", "PyTorch", "MLOps", "AWS"], 125000),
        ("Data Analyst", ["SQL", "Excel", "Tableau", "Python", "Statistics"], 80000),
    ]
    with destination.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=columns)
        writer.writeheader()
        for index in range(120):
            role, skills, base = roles[index % len(roles)]
            seniority = ["Junior", "Mid", "Senior"][(index // 4) % 3]
            salary = base + {"Junior": -25000, "Mid": 0, "Senior": 30000}[seniority] + ((index // 12) % 5) * 2000
            listed = index % 10 != 0
            skill_list = skills[:3 + (index % 3)] if index % 20 != 0 else []
            writer.writerow({
                "job_id": f"synthetic-demo-{index + 1:03}",
                "posted_date": (date(2026, 7, 1) + timedelta(days=index % 90)).isoformat(),
                "title": f"{seniority} {role} — Synthetic Demo",
                "role_category": role,
                "seniority": seniority,
                "salary_min_usd": salary - 10000 if listed else "",
                "salary_max_usd": salary + 10000 if listed else "",
                "salary_mid_usd": salary if listed else "",
                "skills": ";".join(skill_list),
                "remote_status": ["Remote", "Hybrid", "Onsite"][(index // 4 + index) % 3],
                "industry": ["Software", "Healthcare", "Finance"][(index // 8) % 3],
                "country": ["US", "UK", "CA", "IN"][(index // 4 + index) % 4],
                "source": "local_synthetic_demo",
                "source_url": "",
                "data_origin": "synthetic",
            })
    print(f"Created {destination.name}: 120 explicitly synthetic rows.")


if __name__ == "__main__":
    main()
