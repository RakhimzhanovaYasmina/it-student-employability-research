
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
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
        return float(values[0]), float(values[0])

    samples = rng.choice(
        values,
        size=(BOOTSTRAP_ITERATIONS, len(values)),
        replace=True,
    )
    means = samples.mean(axis=1)

    lower, upper = np.percentile(means, [2.5, 97.5])
    return float(lower), float(upper)


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
        ].dropna().to_numpy(dtype=float)

        if len(values) > 0:
            groups.append(values * 100)
            labels.append(f"{label}\n(n={len(values)})")

    if not groups:
        raise ValueError("No valid internship groups found.")

    fig, ax = plt.subplots(figsize=(8, 5.5))
    positions = np.arange(1, len(groups) + 1)

    for position, values in zip(positions, groups):
        mean = float(np.mean(values))
        lower, upper = bootstrap_mean_ci(values, rng)

        # Individual student observations.
        jitter = rng.uniform(-0.045, 0.045, size=len(values))
        ax.scatter(
            position + jitter,
            values,
            marker="o",
            s=55,
            alpha=0.8,
            label="Individual students" if position == 1 else None,
            zorder=3,
        )

        # Mean and bootstrap 95% confidence interval.
        ax.errorbar(
            position,
            mean,
            yerr=[
                [max(0.0, mean - lower)],
                [max(0.0, upper - mean)],
            ],
            fmt="D",
            capsize=6,
            markersize=7,
            color="black",
            label="Mean with bootstrap 95% CI"
            if position == 1 else None,
            zorder=4,
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
    ax.legend(loc="best", frameon=True)
    fig.tight_layout()

    save_figure(fig, "fig1_internship_comparison")


def plot_rate_distributions(data):
    """Show distributions of interview and job-offer rates."""
    interview_rates = (
        data["interview_invitation_rate"].dropna().to_numpy(dtype=float)
        * 100
    )
    offer_rates = (
        data["job_offer_rate_per_application"].dropna().to_numpy(dtype=float)
        * 100
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

    fig, ax = plt.subplots(figsize=(9, 5.5))

    ax.boxplot(
        distributions,
        tick_labels=labels,
        showmeans=True,
        showfliers=False,
        patch_artist=False,
        meanprops={
            "marker": "^",
            "markerfacecolor": "green",
            "markeredgecolor": "green",
            "markersize": 8,
        },
        medianprops={
            "color": "darkorange",
            "linewidth": 2,
        },
        boxprops={
            "color": "black",
            "linewidth": 1.4,
        },
        whiskerprops={
            "color": "black",
            "linewidth": 1.4,
        },
        capprops={
            "color": "black",
            "linewidth": 1.4,
        },
    )

    # Plot individual student observations with small horizontal offsets.
    rng = np.random.default_rng(RANDOM_SEED)

    for position, values in enumerate(distributions, start=1):
        jitter = rng.uniform(-0.07, 0.07, size=len(values))
        ax.scatter(
            position + jitter,
            values,
            marker="o",
            s=42,
            alpha=0.75,
            zorder=3,
        )

    # Explicit legend for all displayed statistics.
    legend_handles = [
        Line2D(
            [0], [0],
            marker="o",
            linestyle="none",
            markerfacecolor="steelblue",
            markeredgecolor="steelblue",
            markersize=7,
            label="Individual students",
        ),
        Line2D(
            [0], [0],
            color="darkorange",
            linewidth=2,
            label="Median",
        ),
        Line2D(
            [0], [0],
            marker="^",
            linestyle="none",
            markerfacecolor="green",
            markeredgecolor="green",
            markersize=8,
            label="Mean",
        ),
        Line2D(
            [0], [0],
            color="black",
            linewidth=1.4,
            label="Whiskers: 1.5 × IQR",
        ),
    ]

    ax.legend(handles=legend_handles, loc="best", frameon=True)
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
