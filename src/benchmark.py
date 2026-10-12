
import csv
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA_PATH = ROOT / "data" / "sample" / "sample.csv"
OUTPUT_PATH = ROOT / "results" / "analysis_summary.json"


def load_data(path):
    with path.open("r", encoding="utf-8", newline="") as file:
        return list(csv.DictReader(file))


def analyze(data):
    required = [
        "student_id",
        "professional_experience",
        "internship",
        "applications_sent",
        "interview_invitations",
        "job_offers",
    ]

    missing_columns = [col for col in required if col not in data[0]]
    if missing_columns:
        raise ValueError(f"Missing columns: {missing_columns}")

    missing_values = sum(
        1 for row in data
        for col in required
        if not row.get(col, "").strip()
    )

    invalid_records = 0
    for row in data:
        try:
            applications = int(row["applications_sent"])
            interviews = int(row["interview_invitations"])
            offers = int(row["job_offers"])

            if (
                applications < 0
                or interviews < 0
                or offers < 0
                or interviews > applications
                or offers > interviews
                or row["professional_experience"] not in {"yes", "no"}
                or row["internship"] not in {"yes", "no"}
            ):
                invalid_records += 1
        except (ValueError, KeyError):
            invalid_records += 1

    valid_rows = [
        row for row in data
        if row["student_id"].strip()
        and row["professional_experience"] in {"yes", "no"}
        and row["internship"] in {"yes", "no"}
        and row["applications_sent"].isdigit()
        and row["interview_invitations"].isdigit()
        and row["job_offers"].isdigit()
        and int(row["applications_sent"]) >= int(row["interview_invitations"])
        and int(row["interview_invitations"]) >= int(row["job_offers"])
    ]

    total = len(valid_rows)
    if total == 0:
        raise ValueError("No valid records available for analysis.")

    invitations = sum(int(r["interview_invitations"]) for r in valid_rows)
    offers = sum(int(r["job_offers"]) for r in valid_rows)
    applications = sum(int(r["applications_sent"]) for r in valid_rows)

    internship_groups = {}
    for status in ("yes", "no"):
        group = [r for r in valid_rows if r["internship"] == status]
        internship_groups[status] = {
            "students": len(group),
            "average_interview_invitations": (
                round(
                    sum(int(r["interview_invitations"]) for r in group)
                    / len(group),
                    2,
                )
                if group else None
            ),
            "students_with_job_offers": sum(
                int(r["job_offers"]) > 0 for r in group
            ),
        }

    return {
        "data_type": "synthetic_demo",
        "records_total": len(data),
        "records_analyzed": total,
        "missing_values": missing_values,
        "invalid_records": invalid_records,
        "interview_invitation_rate": round(invitations / applications, 4)
        if applications else None,
        "job_offer_rate_per_application": round(offers / applications, 4)
        if applications else None,
        "average_interview_invitations": round(invitations / total, 2),
        "baseline_internship_yes_vs_no": internship_groups,
        "interpretation": (
            "Synthetic demonstration only. These results are not evidence "
            "about the real student population and cannot confirm the hypotheses."
        ),
    }


def main():
    data = load_data(DATA_PATH)
    results = analyze(data)

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT_PATH.open("w", encoding="utf-8") as file:
        json.dump(results, file, indent=2, ensure_ascii=False)

    print("Research pipeline completed successfully.")
    print(f"Records analyzed: {results['records_analyzed']}")
    print(f"Interview invitation rate: {results['interview_invitation_rate']}")
    print(f"Output saved to: {OUTPUT_PATH.relative_to(ROOT)}")
    print("NOTICE: Results use synthetic demonstration data only.")


if __name__ == "__main__":
    main()
