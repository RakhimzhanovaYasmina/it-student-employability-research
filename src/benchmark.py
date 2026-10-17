
import csv
import json
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
CONFIG_PATH = ROOT / "configs" / "config.yaml"

REQUIRED_COLUMNS = [
    "student_id",
    "professional_experience",
    "academic_projects",
    "internship",
    "technical_skills",
    "communication_skills",
    "applications_sent",
    "interview_invitations",
    "job_offers",
]

COUNT_COLUMNS = [
    "academic_projects",
    "applications_sent",
    "interview_invitations",
    "job_offers",
]

SKILL_COLUMNS = [
    "technical_skills",
    "communication_skills",
]


def load_config(path):
    with path.open("r", encoding="utf-8") as file:
        config = yaml.safe_load(file)

    if not isinstance(config, dict):
        raise ValueError("Configuration file must contain a YAML mapping.")

    if "data" not in config or "project" not in config:
        raise ValueError("Config must contain 'data' and 'project' sections.")

    if "input_path" not in config["data"] or "output_path" not in config["data"]:
        raise ValueError("Config must define input_path and output_path.")

    return config


def load_data(path):
    with path.open("r", encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)

        if not reader.fieldnames:
            raise ValueError("The input CSV file has no header.")

        missing_columns = [
            column for column in REQUIRED_COLUMNS
            if column not in reader.fieldnames
        ]

        if missing_columns:
            raise ValueError(f"Missing CSV columns: {missing_columns}")

        return list(reader)


def analyze(data):
    if not data:
        raise ValueError("The input CSV file contains no records.")

    missing_values = 0
    records_with_missing_values = 0
    invalid_records = 0
    valid_rows = []

    for row in data:
        missing_fields = [
            column for column in REQUIRED_COLUMNS
            if row.get(column) is None or not row[column].strip()
        ]

        missing_values += len(missing_fields)

        if missing_fields:
            records_with_missing_values += 1

        invalid = False

        # Check categorical variables when values are present.
        for column in ("professional_experience", "internship"):
            value = row.get(column)

            if value is not None and value.strip():
                if value.strip().lower() not in {"yes", "no"}:
                    invalid = True

        # Check non-negative integer counts.
        numeric_values = {}

        for column in COUNT_COLUMNS:
            value = row.get(column)

            if value is None or not value.strip():
                continue

            try:
                number = int(value)
                if number < 0:
                    invalid = True
                else:
                    numeric_values[column] = number
            except ValueError:
                invalid = True

        # Skill ratings must be integers from 1 to 5.
        for column in SKILL_COLUMNS:
            value = row.get(column)

            if value is None or not value.strip():
                continue

            try:
                rating = int(value)
                if not 1 <= rating <= 5:
                    invalid = True
            except ValueError:
                invalid = True

        # Check consistency between application outcomes.
        if (
            "applications_sent" in numeric_values
            and "interview_invitations" in numeric_values
            and numeric_values["interview_invitations"]
            > numeric_values["applications_sent"]
        ):
            invalid = True

        if (
            "interview_invitations" in numeric_values
            and "job_offers" in numeric_values
            and numeric_values["job_offers"]
            > numeric_values["interview_invitations"]
        ):
            invalid = True

        if invalid:
            invalid_records += 1

        # Analyse only complete, valid records.
        if not missing_fields and not invalid:
            valid_rows.append(row)

    if not valid_rows:
        raise ValueError(
            "No complete, valid records available for analysis. "
            "Check the CSV data and validation rules."
        )

    total_students = len(valid_rows)

    total_applications = sum(
        int(row["applications_sent"]) for row in valid_rows
    )
    total_invitations = sum(
        int(row["interview_invitations"]) for row in valid_rows
    )
    total_offers = sum(
        int(row["job_offers"]) for row in valid_rows
    )

    internship_groups = {}

    for status in ("yes", "no"):
        group = [
            row for row in valid_rows
            if row["internship"].strip().lower() == status
        ]

        group_invitations = sum(
            int(row["interview_invitations"]) for row in group
        )
        group_applications = sum(
            int(row["applications_sent"]) for row in group
        )
        group_offers = sum(
            int(row["job_offers"]) for row in group
        )

        internship_groups[status] = {
            "students": len(group),
            "total_applications": group_applications,
            "total_interview_invitations": group_invitations,
            "interview_invitation_rate": (
                round(group_invitations / group_applications, 4)
                if group_applications
                else None
            ),
            "average_interview_invitations": (
                round(group_invitations / len(group), 2)
                if group
                else None
            ),
            "students_with_job_offers": sum(
                int(row["job_offers"]) > 0 for row in group
            ),
            "job_offer_rate_per_application": (
                round(group_offers / group_applications, 4)
                if group_applications
                else None
            ),
        }

    return {
        "data_type": "synthetic_demo",
        "records_total": len(data),
        "records_analyzed": total_students,
        "records_with_missing_values": records_with_missing_values,
        "missing_values": missing_values,
        "invalid_records": invalid_records,
        "total_applications": total_applications,
        "total_interview_invitations": total_invitations,
        "total_job_offers": total_offers,
        "interview_invitation_rate": (
            round(total_invitations / total_applications, 4)
            if total_applications
            else None
        ),
        "job_offer_rate_per_application": (
            round(total_offers / total_applications, 4)
            if total_applications
            else None
        ),
        "average_interview_invitations": round(
            total_invitations / total_students, 2
        ),
        "baseline_internship_yes_vs_no": internship_groups,
        "interpretation": (
            "Synthetic demonstration data only. Results test pipeline "
            "execution and do not confirm or reject research hypotheses."
        ),
    }


def main():
    config = load_config(CONFIG_PATH)

    input_path = ROOT / config["data"]["input_path"]
    output_path = ROOT / config["data"]["output_path"]

    data = load_data(input_path)
    results = analyze(data)
    results["data_type"] = config["project"].get(
        "data_type", "synthetic_demo"
    )

    output_path.parent.mkdir(parents=True, exist_ok=True)

    with output_path.open("w", encoding="utf-8") as file:
        json.dump(results, file, indent=2, ensure_ascii=False)

    print("Research pipeline completed successfully.")
    print(f"Records analyzed: {results['records_analyzed']}")
    print(f"Missing values: {results['missing_values']}")
    print(f"Records with missing values: {results['records_with_missing_values']}")
    print(f"Invalid records: {results['invalid_records']}")
    print(
        "Interview invitation rate: "
        f"{results['interview_invitation_rate']}"
    )
    print(
        "Job offer rate per application: "
        f"{results['job_offer_rate_per_application']}"
    )
    print(f"Output saved to: {output_path.relative_to(ROOT)}")
    print("NOTICE: Results use synthetic demonstration data only.")


if __name__ == "__main__":
    main()
