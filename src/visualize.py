"""Generate the publication figures for the employability analysis.

Figures follow the project's visualization rules:
* axes carry names and units (%),
* uncertainty is shown as bootstrap 95% confidence intervals,
* a colorblind-safe palette is used and groups differ by marker, hatch and
  line style as well as by colour (readable in black-and-white print),
* every figure is exported as PNG (300 DPI) and as vector PDF.
"""

from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Patch
import numpy as np
import pandas as pd
import seaborn as sns


PROJECT_ROOT = Path(__file__).resolve().parent.parent
INPUT_FILE = PROJECT_ROOT / "data" / "processed" / "metrics_summary.csv"
FIGURES_DIR = PROJECT_ROOT / "reports" / "figures"

RANDOM_SEED = 42
BOOTSTRAP_ITERATIONS = 5000

# Colorblind-safe palette (seaborn "colorblind"): blue, orange.
PALETTE = sns.color_palette("colorblind")
# One style per group: colour + marker + hatch + error-bar line style.
GROUP_STYLES = {
    "no": {
        "label": "No internship",
        "color": PALETTE[0],
        "marker": "o",
        "hatch": "//",
        "linestyle": "-",
    },
    "yes": {
        "label": "Internship",
        "color": PALETTE[1],
        "marker": "s",
        "hatch": "..",
        "linestyle": "--",
    },
}
# Styles of the two outcome distributions in Figure 2.
OUTCOME_STYLES = [
    {"color": PALETTE[0], "marker": "o", "hatch": "//", "linestyle": "-"},
    {"color": PALETTE[1], "marker": "s", "hatch": "..", "linestyle": "--"},
]

plt.rcParams["pdf.fonttype"] = 42  # embed TrueType fonts in the PDF
plt.rcParams["font.size"] = 11


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
    """Save a figure as high-resolution PNG (300 DPI) and vector PDF."""
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


def _draw_mean_ci(ax, x, values, rng, linestyle="-"):
    """Draw the mean with its bootstrap 95% CI as a black error bar."""
    mean = float(np.mean(values))
    lower, upper = bootstrap_mean_ci(values, rng)
    container = ax.errorbar(
        x,
        mean,
        yerr=[[max(0.0, mean - lower)], [max(0.0, upper - mean)]],
        fmt="D",
        capsize=6,
        markersize=7,
        color="black",
        markerfacecolor="white",
        markeredgewidth=1.6,
        elinewidth=1.6,
        zorder=5,
    )
    for bar in container[2]:  # vertical error-bar line
        bar.set_linestyle(linestyle)
    return mean, lower, upper


def plot_internship_comparison(data):
    """Compare interview invitation rates by internship status."""
    rng = np.random.default_rng(RANDOM_SEED)
    groups = []

    for key in ["no", "yes"]:
        values = data.loc[
            data["internship"] == key,
            "interview_invitation_rate",
        ].dropna().to_numpy(dtype=float)

        if len(values) > 0:
            groups.append((key, values * 100))

    if not groups:
        raise ValueError("No valid internship groups found.")

    fig, ax = plt.subplots(figsize=(8, 5.5))
    positions = np.arange(1, len(groups) + 1)
    tick_labels = []
    legend_handles = []

    for position, (key, values) in zip(positions, groups):
        style = GROUP_STYLES[key]

        # Individual student observations (jittered horizontally).
        jitter = rng.uniform(-0.06, 0.06, size=len(values))
        ax.scatter(
            position + jitter - 0.12,
            values,
            marker=style["marker"],
            s=70,
            color=style["color"],
            edgecolor="black",
            linewidth=0.8,
            alpha=0.9,
            zorder=3,
        )

        # Mean and bootstrap 95% confidence interval.
        _draw_mean_ci(
            ax, position + 0.12, values, rng, linestyle=style["linestyle"]
        )

        tick_labels.append(f"{style['label']}\n(n={len(values)})")
        legend_handles.append(
            Line2D(
                [0], [0],
                marker=style["marker"],
                linestyle="none",
                markerfacecolor=style["color"],
                markeredgecolor="black",
                markersize=8,
                label=f"{style['label']}: individual students",
            )
        )

    legend_handles.append(
        Line2D(
            [0], [0],
            marker="D",
            linestyle="none",
            markerfacecolor="white",
            markeredgecolor="black",
            markeredgewidth=1.6,
            markersize=7,
            label="Mean with bootstrap 95% CI",
        )
    )

    ax.set_xticks(positions)
    ax.set_xticklabels(tick_labels)
    ax.set_xlim(0.4, len(groups) + 0.6)
    ax.set_ylim(bottom=-1.5)
    ax.set_ylabel("Interview invitation rate (%)")
    ax.set_xlabel("Internship experience")
    ax.set_title(
        "Interview Invitation Rate by Internship Status\n"
        "Synthetic demonstration data"
    )
    ax.grid(axis="y", linestyle="--", alpha=0.35)
    ax.legend(handles=legend_handles, loc="lower right", frameon=True)
    fig.tight_layout()

    save_figure(fig, "fig1_internship_comparison")


def plot_rate_distributions(data):
    """Show distributions of interview and job-offer rates."""
    rng = np.random.default_rng(RANDOM_SEED)
    series = [
        ("Interview invitations", "interview_invitation_rate"),
        ("Job offers", "job_offer_rate_per_application"),
    ]

    distributions = []
    labels = []
    styles = []

    for (label, column), style in zip(series, OUTCOME_STYLES):
        values = data[column].dropna().to_numpy(dtype=float) * 100
        if len(values):
            distributions.append(values)
            labels.append(f"{label}\n(n={len(values)})")
            styles.append(style)

    if not distributions:
        raise ValueError("No valid rate values available for plotting.")

    fig, ax = plt.subplots(figsize=(9, 5.5))
    positions = np.arange(1, len(distributions) + 1)

    box = ax.boxplot(
        distributions,
        positions=positions,
        widths=0.4,
        tick_labels=labels,
        showmeans=False,
        showfliers=False,
        patch_artist=True,
        medianprops={"color": "black", "linewidth": 2.2},
        boxprops={"linewidth": 1.4},
        whiskerprops={"linewidth": 1.4},
        capprops={"linewidth": 1.4},
    )
    for patch, style in zip(box["boxes"], styles):
        patch.set_facecolor(style["color"])
        patch.set_alpha(0.45)
        patch.set_edgecolor("black")
        patch.set_hatch(style["hatch"])
        patch.set_linestyle(style["linestyle"])

    for position, values, style in zip(positions, distributions, styles):
        # Individual student observations (jittered horizontally).
        jitter = rng.uniform(-0.05, 0.05, size=len(values))
        ax.scatter(
            position + jitter - 0.32,
            values,
            marker=style["marker"],
            s=55,
            color=style["color"],
            edgecolor="black",
            linewidth=0.8,
            zorder=3,
        )
        # Mean and bootstrap 95% confidence interval.
        _draw_mean_ci(
            ax, position + 0.32, values, rng, linestyle=style["linestyle"]
        )

    legend_handles = [
        Line2D(
            [0], [0],
            marker="o",
            linestyle="none",
            markerfacecolor="lightgray",
            markeredgecolor="black",
            markersize=7,
            label="Individual students (marker differs by outcome)",
        ),
        Line2D([0], [0], color="black", linewidth=2.2, label="Median"),
        Patch(
            facecolor="lightgray",
            edgecolor="black",
            label="Interquartile range (whiskers: 1.5 × IQR)",
        ),
        Line2D(
            [0], [0],
            marker="D",
            linestyle="none",
            markerfacecolor="white",
            markeredgecolor="black",
            markeredgewidth=1.6,
            markersize=7,
            label="Mean with bootstrap 95% CI",
        ),
    ]

    ax.set_xlim(0.4, len(distributions) + 0.6)
    ax.set_ylim(bottom=-1.5)
    ax.legend(handles=legend_handles, loc="upper right", frameon=True)
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
