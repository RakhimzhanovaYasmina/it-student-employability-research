import csv
import json
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
CONFIG_PATH = ROOT / "configs" / "config.yaml"


def load_config(path):
    with path.open("r", encoding="utf-8") as file:
        config = yaml.safe_load(file)

    if not isinstance(config, dict):
        raise ValueError("Configuration file must contain a YAML mapping.")

    return config


def load_data(path):
    with path.open("r", encoding="utf-8", newline="") as file:
        return list(csv.DictReader(file))


def analyze(data):
    if not data:
        raise ValueError("The input CSV file contains no records.")

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
        1
        for row in data
        for col in required
        if not row.get(col, "").strip()
    )

    valid_rows = []
    invalid_records = 0

    for row in data:
        try:
            applications = int(row["applications_sent"])
            interviews = int(row["interview_invitations"])
            offers = int(row["job_offers"])

            valid = (
                bool(row["student_id"].strip())
                and row["professional_experience"] in {"yes", "no"}
                and row["internship"] in {"yes", "no"}
                and applications >= 0
                and interviews >= 0
                and offers >= 0
                and interviews <= applications
                and offers <= interviews
            )

            if valid:
                valid_rows.append(row)
            else:
                invalid_records += 1

        except (ValueError, KeyError, TypeError):
            invalid_records += 1

    if not valid_rows:
        raise ValueError("No valid records available for analysis.")

    total = len(valid_rows)
    applications = sum(int(row["applications_sent"]) for row in valid_rows)
    invitations = sum(
        int(row["interview_invitations"]) for row in valid_rows
    )
    offers = sum(int(row["job_offers"]) for row in valid_rows)

    internship_groups = {}

    for status in ("yes", "no"):
        group = [row for row in valid_rows if row["internship"] == status]

        internship_groups[status] = {
            "students": len(group),
            "average_interview_invitations": (
                round(
                    sum(int(row["interview_invitations"]) for row in group)
                    / len(group),
                    2,
                )
                if group
                else None
            ),
            "students_with_job_offers": sum(
                int(row["job_offers"]) > 0 for row in group
            ),
        }

    return {
        "data_type": "synthetic_demo",
        "records_total": len(data),
        "records_analyzed": total,
        "missing_values": missing_values,
        "invalid_records": invalid_records,
        "interview_invitation_rate": (
            round(invitations / applications, 4)
            if applications
            else None
        ),
        "job_offer_rate_per_application": (
            round(offers / applications, 4)
            if applications
            else None
        ),
        "average_interview_invitations": round(invitations / total, 2),
        "baseline_internship_yes_vs_no": internship_groups,
        "interpretation": (
            "Synthetic demonstration only. These results are not evidence "
            "about the real student population and cannot confirm "
            "the hypotheses."
        ),
    }


def main():
    config = load_config(CONFIG_PATH)

    input_path = ROOT / config["data"]["input_path"]
    output_path = ROOT / config["data"]["output_path"]

    data = load_data(input_path)
    results = analyze(data)

    results["data_type"] = config["project"]["data_type"]

    output_path.parent.mkdir(parents=True, exist_ok=True)

    with output_path.open("w", encoding="utf-8") as file:
        json.dump(results, file, indent=2, ensure_ascii=False)

    print("Research pipeline completed successfully.")
    print(f"Records analyzed: {results['records_analyzed']}")
    print(
        "Interview invitation rate: "
        f"{results['interview_invitation_rate']}"
    )
    print(f"Output saved to: {output_path.relative_to(ROOT)}")
    print("NOTICE: Results use synthetic demonstration data only.")


if __name__ == "__main__":
    main()