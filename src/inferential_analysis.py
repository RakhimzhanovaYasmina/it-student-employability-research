"""Exploratory inferential analysis of the survey (RQ1-RQ3).

All tests are rank-based or exact because n is tiny (17 respondents, 11 of
whom sent at least one application). Primary tests (one per hypothesis) are
Holm-adjusted; every other test is exploratory and reported unadjusted.

Outputs (results/):
    tests_summary.csv          all tests with effect sizes and p-values
    barriers_summary.csv       frequency of perceived barriers (RQ1)
    sample_description.csv     sample composition
    inferential_summary.json   headline numbers used in the paper
"""

import json
from itertools import combinations
from math import sqrt
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

PROJECT_ROOT = Path(__file__).resolve().parent.parent
INPUT_FILE = PROJECT_ROOT / "data" / "processed" / "metrics_summary.csv"
OUTPUT_DIR = PROJECT_ROOT / "results"

RANDOM_SEED = 42
BOOTSTRAP_ITERATIONS = 5000
ALPHA = 0.05


def load_students() -> pd.DataFrame:
    data = pd.read_csv(INPUT_FILE)
    return data[data["student_id"] != "OVERALL"].copy()


def wilson_interval(successes: int, trials: int, z: float = 1.96):
    """Wilson score interval for a binomial proportion."""
    if trials == 0:
        return np.nan, np.nan
    p = successes / trials
    denom = 1 + z**2 / trials
    centre = (p + z**2 / (2 * trials)) / denom
    half = z * sqrt(p * (1 - p) / trials + z**2 / (4 * trials**2)) / denom
    return centre - half, centre + half


def cliffs_delta(x, y) -> float:
    """Cliff's delta: P(x > y) - P(x < y)."""
    x, y = np.asarray(x, float), np.asarray(y, float)
    greater = sum((xi > y).sum() for xi in x)
    less = sum((xi < y).sum() for xi in x)
    return float((greater - less) / (len(x) * len(y)))


def exact_mann_whitney(x, y):
    """Mann-Whitney U with an exact two-sided permutation p-value.

    Mid-ranks handle ties; the null distribution is enumerated over all
    C(n1+n2, n1) group assignments, so the p-value is exact for tied data.
    """
    x, y = np.asarray(x, float), np.asarray(y, float)
    pooled = np.concatenate([x, y])
    ranks = stats.rankdata(pooled)
    n1 = len(x)
    u_obs = ranks[:n1].sum() - n1 * (n1 + 1) / 2
    mean_u = n1 * len(y) / 2
    extreme = total = 0
    for idx in combinations(range(len(pooled)), n1):
        u = ranks[list(idx)].sum() - n1 * (n1 + 1) / 2
        total += 1
        if abs(u - mean_u) >= abs(u_obs - mean_u) - 1e-9:
            extreme += 1
    return float(u_obs), extreme / total


def bootstrap_diff_ci(x, y, rng):
    """Percentile bootstrap 95% CI for mean(x) - mean(y)."""
    x, y = np.asarray(x, float), np.asarray(y, float)
    bx = rng.choice(x, size=(BOOTSTRAP_ITERATIONS, len(x))).mean(axis=1)
    by = rng.choice(y, size=(BOOTSTRAP_ITERATIONS, len(y))).mean(axis=1)
    lo, hi = np.percentile(bx - by, [2.5, 97.5])
    return float(lo), float(hi)


def holm_adjust(p_values):
    """Holm step-down adjusted p-values."""
    order = np.argsort(p_values)
    m = len(p_values)
    adjusted = np.empty(m)
    running = 0.0
    for rank, i in enumerate(order):
        running = max(running, (m - rank) * p_values[i])
        adjusted[i] = min(1.0, running)
    return adjusted.tolist()


def leave_one_out_spearman(sub, x, y):
    """Range of Spearman rho when each applicant is dropped in turn."""
    values = []
    for idx in sub.index:
        rest = sub.drop(index=idx)
        rho, _ = stats.spearmanr(rest[x], rest[y])
        values.append(float(rho))
    return {"min": min(values), "max": max(values),
            "sign_changes": int(sum(v < 0 for v in values)
                                if stats.spearmanr(sub[x], sub[y])[0] > 0
                                else sum(v > 0 for v in values))}


def describe_sample(data: pd.DataFrame) -> pd.DataFrame:
    rows = [("respondents", "all", len(data))]
    for column in ("study_year", "track", "professional_experience",
                   "internship", "working_in_it"):
        for value, count in data[column].value_counts().items():
            rows.append((column, str(value), int(count)))
    rows.append(("with_applications", ">0", int((data["applications_sent"] > 0).sum())))
    rows.append(("zero_applications", "=0", int((data["applications_sent"] == 0).sum())))
    return pd.DataFrame(rows, columns=["variable", "category", "n"])


def barrier_table(data: pd.DataFrame) -> pd.DataFrame:
    labels = data["barriers"].str.split(";").explode().str.strip()
    counts = labels.value_counts()
    n = len(data)
    rows = []
    for label, count in counts.items():
        lo, hi = wilson_interval(int(count), n)
        rows.append({
            "barrier": label,
            "n": int(count),
            "share_pct": 100 * count / n,
            "wilson_lo_pct": 100 * lo,
            "wilson_hi_pct": 100 * hi,
        })
    return pd.DataFrame(rows)


def main() -> None:
    rng = np.random.default_rng(RANDOM_SEED)
    students = load_students()
    for column in ("interview_invitation_rate", "job_offer_rate_per_application"):
        students[column] = pd.to_numeric(students[column], errors="coerce")
    applicants = students[students["applications_sent"] > 0].copy()

    tests = []

    # ---- RQ1 / H1: professional experience vs perceived difficulty (n = 17)
    with_exp = students.loc[students["professional_experience"] == "yes", "perceived_difficulty"]
    no_exp = students.loc[students["professional_experience"] == "no", "perceived_difficulty"]
    u, p = exact_mann_whitney(no_exp, with_exp)
    tests.append({
        "id": "H1", "family": "primary", "rq": "RQ1",
        "test": "Mann-Whitney U (exact), difficulty: no experience vs experience",
        "n": len(students), "statistic": u, "p_raw": p,
        "effect_name": "Cliff's delta", "effect": cliffs_delta(no_exp, with_exp),
        "median_a": float(no_exp.median()), "median_b": float(with_exp.median()),
        "n_a": len(no_exp), "n_b": len(with_exp),
    })

    # ---- RQ2 / H2: internship vs interview invitation rate (n = 11)
    yes = applicants.loc[applicants["internship"] == "yes", "interview_invitation_rate"]
    no = applicants.loc[applicants["internship"] == "no", "interview_invitation_rate"]
    u, p = exact_mann_whitney(yes, no)
    diff_lo, diff_hi = bootstrap_diff_ci(yes, no, rng)
    tests.append({
        "id": "H2", "family": "primary", "rq": "RQ2",
        "test": "Mann-Whitney U (exact), interview rate: internship vs none",
        "n": len(applicants), "statistic": u, "p_raw": p,
        "effect_name": "Cliff's delta", "effect": cliffs_delta(yes, no),
        "median_a": float(yes.median()), "median_b": float(no.median()),
        "n_a": len(yes), "n_b": len(no),
        "mean_diff": float(yes.mean() - no.mean()),
        "mean_diff_ci_lo": diff_lo, "mean_diff_ci_hi": diff_hi,
    })

    # ---- RQ3 / H3: technical skills vs interview rate (n = 11)
    rho, p = stats.spearmanr(applicants["technical_skills"], applicants["interview_invitation_rate"])
    tests.append({
        "id": "H3", "family": "primary", "rq": "RQ3",
        "test": "Spearman rho, technical skills vs interview rate",
        "n": len(applicants), "statistic": float(rho), "p_raw": float(p),
        "effect_name": "Spearman rho", "effect": float(rho),
    })

    adjusted = holm_adjust([t["p_raw"] for t in tests])
    for t, padj in zip(tests, adjusted):
        t["p_holm"] = padj

    # ---- Exploratory tests (unadjusted)
    def spearman(label, x, y, rq, sub):
        r, pv = stats.spearmanr(sub[x], sub[y])
        tests.append({
            "id": label, "family": "exploratory", "rq": rq,
            "test": f"Spearman rho, {x} vs {y}", "n": len(sub),
            "statistic": float(r), "p_raw": float(pv),
            "effect_name": "Spearman rho", "effect": float(r),
        })

    spearman("E1", "communication_skills", "interview_invitation_rate", "RQ3", applicants)
    spearman("E2", "academic_projects", "interview_invitation_rate", "RQ2", applicants)
    spearman("E3", "technical_skills", "job_offer_rate_per_application", "RQ3", applicants)
    spearman("E4", "academic_projects", "job_offer_rate_per_application", "RQ2", applicants)

    u, p = exact_mann_whitney(
        applicants.loc[applicants["internship"] == "yes", "job_offer_rate_per_application"],
        applicants.loc[applicants["internship"] == "no", "job_offer_rate_per_application"],
    )
    tests.append({
        "id": "E5", "family": "exploratory", "rq": "RQ2",
        "test": "Mann-Whitney U (exact), offer rate: internship vs none",
        "n": len(applicants), "statistic": u, "p_raw": p,
        "effect_name": "Cliff's delta",
        "effect": cliffs_delta(
            applicants.loc[applicants["internship"] == "yes", "job_offer_rate_per_application"],
            applicants.loc[applicants["internship"] == "no", "job_offer_rate_per_application"],
        ),
    })

    table = pd.crosstab(
        students["internship"], students["working_in_it"].str.startswith("yes")
    ).reindex(index=["yes", "no"], columns=[True, False], fill_value=0)
    odds, p = stats.fisher_exact(table.to_numpy())
    tests.append({
        "id": "E6", "family": "exploratory", "rq": "RQ2",
        "test": "Fisher exact, internship vs currently working in IT",
        "n": len(students), "statistic": float(odds), "p_raw": float(p),
        "effect_name": "odds ratio", "effect": float(odds),
        "table_yes_working": int(table.loc["yes", True]),
        "table_yes_not": int(table.loc["yes", False]),
        "table_no_working": int(table.loc["no", True]),
        "table_no_not": int(table.loc["no", False]),
    })

    tests_df = pd.DataFrame(tests)

    # ---- Pooled rates with Wilson intervals (descriptive; clustering ignored)
    pooled = {}
    for label, group in (("internship", applicants[applicants["internship"] == "yes"]),
                         ("no_internship", applicants[applicants["internship"] == "no"]),
                         ("all_applicants", applicants)):
        apps = int(group["applications_sent"].sum())
        inv = int(group["interview_invitations"].sum())
        off = int(group["job_offers"].sum())
        pooled[label] = {
            "n_students": len(group), "applications": apps,
            "interviews": inv, "offers": off,
            "interview_rate": inv / apps,
            "interview_rate_wilson": wilson_interval(inv, apps),
            "offer_rate": off / apps,
            "offer_rate_wilson": wilson_interval(off, apps),
            "mean_student_rate_interview": float(group["interview_invitation_rate"].mean()),
            "median_student_rate_interview": float(group["interview_invitation_rate"].median()),
            "iqr_interview": [float(group["interview_invitation_rate"].quantile(0.25)),
                              float(group["interview_invitation_rate"].quantile(0.75))],
            "mean_student_rate_offer": float(group["job_offer_rate_per_application"].mean()),
            "median_student_rate_offer": float(group["job_offer_rate_per_application"].median()),
            "students_with_offer": int((group["job_offers"] > 0).sum()),
        }

    working = students["working_in_it"].str.startswith("yes")
    headline = {
        "leave_one_out_spearman": {
            "technical_skills": leave_one_out_spearman(
                applicants, "technical_skills", "interview_invitation_rate"),
            "communication_skills": leave_one_out_spearman(
                applicants, "communication_skills", "interview_invitation_rate"),
        },
        "n_respondents": len(students),
        "n_applicants": len(applicants),
        "difficulty_median": float(students["perceived_difficulty"].median()),
        "difficulty_mean": float(students["perceived_difficulty"].mean()),
        "difficulty_ge4_share": float((students["perceived_difficulty"] >= 4).mean()),
        "working_in_it_n": int(working.sum()),
        "pooled": pooled,
        "random_seed": RANDOM_SEED,
        "bootstrap_iterations": BOOTSTRAP_ITERATIONS,
    }

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    tests_df.to_csv(OUTPUT_DIR / "tests_summary.csv", index=False)
    barrier_table(students).to_csv(OUTPUT_DIR / "barriers_summary.csv", index=False)
    describe_sample(students).to_csv(OUTPUT_DIR / "sample_description.csv", index=False)
    with (OUTPUT_DIR / "inferential_summary.json").open("w", encoding="utf-8") as f:
        json.dump(headline, f, indent=2, ensure_ascii=False)

    pd.set_option("display.width", 220, "display.max_columns", 30)
    print("Inferential analysis completed successfully.")
    print(tests_df[["id", "family", "n", "statistic", "effect", "p_raw"]
                   + (["p_holm"] if "p_holm" in tests_df else [])].round(3).to_string(index=False))
    print(json.dumps(pooled, indent=1, default=float))


if __name__ == "__main__":
    main()
