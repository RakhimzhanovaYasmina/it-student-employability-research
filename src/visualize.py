
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parent.parent
INPUT_FILE = PROJECT_ROOT / "data" / "processed" / "metrics_summary.csv"
FIGURES_DIR = PROJECT_ROOT / "reports" / "figures"

RANDOM_SEED = 42
BOOTSTRAP_ITERATIONS = 5000


def bootstrap_mean_ci(values, rng):
    """Calculate a bootstrap 95% confidence interval for the mean."""
    values = np.asarray(values, dtype=float)
    values = values[np.isfinite(values)]

    if len(values) == 0:
        return np.nan, np.nan

    if len(values) == 1:
        return values[0], values[0]

    samples = rng.choice(
        values,
        size=(BOOTSTRAP_ITERATIONS, len(values)),
        replace=True,
    )
    means = samples.mean(axis=1)

    lower, upper = np.percentile(means, [2.5, 97.5])
    return lower, upper


def load_data():
    """Load processed student-level data, excluding the summary row."""
    if not INPUT_FILE.exists():
        raise FileNotFoundError(
            f"Processed data not found: {INPUT_FILE}\n"
            "Run src/process_data.py first."
        )

    data = pd.read_csv(INPUT_FILE)
    data = data[data["student_id"] != "OVERALL"].copy()

    data["internship"] = (
        data["internship"].astype(str).str.strip().str.lower()
    )

    for column in [
        "interview_invitation_rate",
        "job_offer_rate_per_application",
    ]:
        data[column] = pd.to_numeric(data[column], errors="coerce")

    return data


def save_figure(fig, filename):
    """Save a figure as high-resolution PNG and PDF."""
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)

    fig.savefig(
        FIGURES_DIR / f"{filename}.png",
        dpi=300,
        bbox_inches="tight",
    )
    fig.savefig(
        FIGURES_DIR / f"{filename}.pdf",
        bbox_inches="tight",
    )
    plt.close(fig)


def plot_internship_comparison(data):
    """Compare interview invitation rates by internship status."""
    rng = np.random.default_rng(RANDOM_SEED)
    groups = []
    labels = []

    for label, value in [
        ("No internship", "no"),
        ("Internship", "yes"),
    ]:
        values = data.loc[
            data["internship"] == value,
            "interview_invitation_rate",
        ].dropna().to_numpy()

        if len(values) > 0:
            groups.append(values * 100)
            labels.append(f"{label}\n(n={len(values)})")

    if not groups:
        raise ValueError("No valid internship groups found.")

    fig, ax = plt.subplots(figsize=(8, 5))

    positions = np.arange(1, len(groups) + 1)

    for position, values, label in zip(positions, groups, labels):
        mean = np.mean(values)
        lower, upper = bootstrap_mean_ci(values, rng)

        ax.scatter(
            np.full(len(values), position),
            values,
            marker="o",
            s=55,
            alpha=0.75,
            label="Individual students" if position == 1 else None,
        )

        ax.errorbar(
            position,
            mean,
            yerr=[[mean - lower], [upper - mean]],
            fmt="D",
            capsize=6,
            markersize=7,
            color="black",
            label="Mean with bootstrap 95% CI"
            if position == 1 else None,
        )

    ax.set_xticks(positions)
    ax.set_xticklabels(labels)
    ax.set_ylabel("Interview invitation rate (%)")
    ax.set_xlabel("Internship experience")
    ax.set_title(
        "Interview Invitation Rate by Internship Status\n"
        "Synthetic demonstration data"
    )
    ax.grid(axis="y", linestyle="--", alpha=0.35)
    ax.legend()
    fig.tight_layout()

    save_figure(fig, "fig1_internship_comparison")


def plot_rate_distributions(data):
    """Show distributions of interview and job-offer rates."""
    interview_rates = (
        data["interview_invitation_rate"].dropna().to_numpy() * 100
    )
    offer_rates = (
        data["job_offer_rate_per_application"].dropna().to_numpy() * 100
    )

    distributions = []
    labels = []

    if len(interview_rates):
        distributions.append(interview_rates)
        labels.append("Interview invitations")

    if len(offer_rates):
        distributions.append(offer_rates)
        labels.append("Job offers")

    if not distributions:
        raise ValueError("No valid rate values available for plotting.")

    fig, ax = plt.subplots(figsize=(8, 5))

    ax.boxplot(
        distributions,
        tick_labels=labels,
        showmeans=True,
        patch_artist=False,
    )

    # Display individual student observations.
    rng = np.random.default_rng(RANDOM_SEED)

    for position, values in enumerate(distributions, start=1):
        jitter = rng.uniform(-0.07, 0.07, size=len(values))
        ax.scatter(
            position + jitter,
            values,
            marker="o",
            s=35,
            alpha=0.7,
        )

    ax.set_ylabel("Rate per application (%)")
    ax.set_xlabel("Employment outcome")
    ax.set_title(
        "Distribution of Student Employment Outcome Rates\n"
        "Synthetic demonstration data"
    )
    ax.grid(axis="y", linestyle="--", alpha=0.35)
    fig.tight_layout()

    save_figure(fig, "fig2_rate_distributions")


def main():
    data = load_data()

    if data.empty:
        raise ValueError("No student records available for visualization.")

    plot_internship_comparison(data)
    plot_rate_distributions(data)

    print("Visualization completed successfully.")
    print(f"Student records plotted: {len(data)}")
    print(f"Figures saved to: {FIGURES_DIR.relative_to(PROJECT_ROOT)}")
    print("Each figure was exported as PNG (300 DPI) and PDF.")
    print("NOTICE: All plots use synthetic demonstration data.")


if __name__ == "__main__":
    main()
