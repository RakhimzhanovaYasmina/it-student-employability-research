
from pathlib import Path

import pandas as pd


# Find the project root directory.
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Input and output files.
INPUT_FILE = PROJECT_ROOT / "data" / "sample" / "sample.csv"
OUTPUT_DIR = PROJECT_ROOT / "data" / "processed"
OUTPUT_FILE = OUTPUT_DIR / "metrics_summary.csv"

# Columns required for the employability analysis.
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


def load_data(file_path: Path) -> pd.DataFrame:
    """Load the student employability dataset."""
    if not file_path.exists():
        raise FileNotFoundError(f"Input dataset not found: {file_path}")

    data = pd.read_csv(file_path)

    missing_columns = [
        column for column in REQUIRED_COLUMNS
        if column not in data.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Dataset is missing required columns: {missing_columns}"
        )

    return data


def clean_data(data: pd.DataFrame) -> pd.DataFrame:
    """Remove duplicate students and validate numeric metrics."""
    cleaned = data.copy()

    # Remove records without a student ID and duplicate student IDs.
    cleaned = cleaned.dropna(subset=["student_id"])
    cleaned = cleaned.drop_duplicates(subset=["student_id"])

    numeric_columns = [
        "applications_sent",
        "interview_invitations",
        "job_offers",
    ]

    for column in numeric_columns:
        cleaned[column] = pd.to_numeric(
            cleaned[column], errors="coerce"
        )

    # Exclude records with missing or impossible metric values.
    valid = cleaned[numeric_columns].notna().all(axis=1)
    valid &= (cleaned[numeric_columns] >= 0).all(axis=1)
    valid &= (
        cleaned["interview_invitations"]
        <= cleaned["applications_sent"]
    )
    valid &= (
        cleaned["job_offers"]
        <= cleaned["applications_sent"]
    )

    cleaned = cleaned.loc[valid].copy()

    return cleaned


def calculate_metrics(data: pd.DataFrame) -> pd.DataFrame:
    """Calculate student-level and overall employability metrics."""
    result = data.copy()

    # Avoid division by zero when a student sent no applications.
    applications = result["applications_sent"].replace(0, float("nan"))

    result["interview_invitation_rate"] = (
        result["interview_invitations"] / applications
    )

    result["job_offer_rate_per_application"] = (
        result["job_offers"] / applications
    )

    # Add an overall summary row for the entire dataset.
    total_applications = result["applications_sent"].sum()
    total_interviews = result["interview_invitations"].sum()
    total_offers = result["job_offers"].sum()

    summary_row = {
        column: None for column in result.columns
    }
    summary_row["student_id"] = "OVERALL"
    summary_row["applications_sent"] = total_applications
    summary_row["interview_invitations"] = total_interviews
    summary_row["job_offers"] = total_offers
    summary_row["interview_invitation_rate"] = (
        total_interviews / total_applications
        if total_applications > 0 else None
    )
    summary_row["job_offer_rate_per_application"] = (
        total_offers / total_applications
        if total_applications > 0 else None
    )

    result = pd.concat(
        [result, pd.DataFrame([summary_row])],
        ignore_index=True,
    )

    return result


def main() -> None:
    """Run the processing pipeline and export the CSV summary."""
    raw_data = load_data(INPUT_FILE)
    cleaned_data = clean_data(raw_data)
    metrics = calculate_metrics(cleaned_data)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    metrics.to_csv(OUTPUT_FILE, index=False)

    print("Data processing completed successfully.")
    print(f"Input records: {len(raw_data)}")
    print(f"Valid records: {len(cleaned_data)}")
    print(f"Excluded records: {len(raw_data) - len(cleaned_data)}")
    print(f"Output saved to: {OUTPUT_FILE.relative_to(PROJECT_ROOT)}")
    print(
        "NOTICE: The current sample contains synthetic demonstration "
        "data, not real student survey results."
    )


if __name__ == "__main__":
    main()
