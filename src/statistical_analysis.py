
from pathlib import Path

import numpy as np
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parent.parent
INPUT_FILE = PROJECT_ROOT / "data" / "processed" / "metrics_summary.csv"
OUTPUT_DIR = PROJECT_ROOT / "results"
SUMMARY_FILE = OUTPUT_DIR / "statistical_summary.csv"
QUALITY_FILE = OUTPUT_DIR / "data_quality_summary.csv"

RANDOM_SEED = 42
BOOTSTRAP_ITERATIONS = 5000

METRICS = [
    "interview_invitation_rate",
    "job_offer_rate_per_application",
]


def bootstrap_mean_ci(values, rng):
    """Return a bootstrap 95% confidence interval for the mean."""
    values = np.asarray(values, dtype=float)
    values = values[np.isfinite(values)]

    if len(values) == 0:
        return np.nan, np.nan

    if len(values) == 1:
        return float(values[0]), float(values[0])

    samples = rng.choice(
        values,
        size=(BOOTSTRAP_ITERATIONS, len(values)),
        replace=True,
    )
    bootstrap_means = samples.mean(axis=1)

    lower, upper = np.percentile(bootstrap_means, [2.5, 97.5])
    return float(lower), float(upper)


def load_student_data():
    """Load processed data without the overall summary row."""
    if not INPUT_FILE.exists():
        raise FileNotFoundError(
            f"Processed data not found: {INPUT_FILE}\n"
            "Run src/process_data.py first."
        )

    data = pd.read_csv(INPUT_FILE)
    data = data[data["student_id"] != "OVERALL"].copy()

    for metric in METRICS:
        data[metric] = pd.to_numeric(data[metric], errors="coerce")

    return data


def summarize_metrics(data):
    """Calculate descriptive statistics and bootstrap confidence intervals."""
    rng = np.random.default_rng(RANDOM_SEED)
    rows = []

    for metric in METRICS:
        values = data[metric].dropna().to_numpy(dtype=float)

        if len(values) == 0:
            continue

        ci_lower, ci_upper = bootstrap_mean_ci(values, rng)

        rows.append({
            "metric": metric,
            "n": len(values),
            "mean": float(np.mean(values)),
            "median": float(np.median(values)),
            "p95": float(np.percentile(values, 95)),
            "p99": float(np.percentile(values, 99)),
            "std_dev": float(np.std(values, ddof=1))
            if len(values) > 1 else np.nan,
            "bootstrap_95ci_lower": ci_lower,
            "bootstrap_95ci_upper": ci_upper,
        })

    return pd.DataFrame(rows)


def summarize_data_quality(data):
    """Report missingness and basic validity checks."""
    total_records = len(data)
    metric_columns = [
        "applications_sent",
        "interview_invitations",
        "job_offers",
    ]

    missing_metric_values = int(data[metric_columns].isna().any(axis=1).sum())

    numeric = data[metric_columns].apply(pd.to_numeric, errors="coerce")
    invalid_negative = int((numeric < 0).any(axis=1).sum())

    invalid_interviews = int(
        (numeric["interview_invitations"] > numeric["applications_sent"])
        .fillna(False).sum()
    )
    invalid_offers = int(
        (numeric["job_offers"] > numeric["applications_sent"])
        .fillna(False).sum()
    )

    quality = pd.DataFrame([{
        "records_analyzed": total_records,
        "records_with_missing_metric_values": missing_metric_values,
        "missing_metric_record_rate_pct": (
            100 * missing_metric_values / total_records
            if total_records else np.nan
        ),
        "records_with_negative_values": invalid_negative,
        "records_with_interviews_exceeding_applications": invalid_interviews,
        "records_with_offers_exceeding_applications": invalid_offers,
        "data_type": "synthetic_demo",
        "interpretation": (
            "Demonstration only; do not generalize to the student population."
        ),
    }])

    return quality


def main():
    data = load_student_data()

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    summary = summarize_metrics(data)
    quality = summarize_data_quality(data)

    summary.to_csv(SUMMARY_FILE, index=False)
    quality.to_csv(QUALITY_FILE, index=False)

    print("Statistical analysis completed successfully.")
    print(f"Records analyzed: {len(data)}")
    print(f"Statistics saved to: {SUMMARY_FILE.relative_to(PROJECT_ROOT)}")
    print(f"Data quality saved to: {QUALITY_FILE.relative_to(PROJECT_ROOT)}")
    print("\nDescriptive statistics:")
    print(summary.to_string(index=False))
    print("\nData quality:")
    print(quality.to_string(index=False))
    print("\nNOTICE: All results use synthetic demonstration data.")


if __name__ == "__main__":
    main()
