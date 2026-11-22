# IT Student Employability Research

**Authors:** Rakhimzhanova Yasmina and Utebayeva Anel

## 1. Overview

This project investigates factors associated with the employability of IT students who have little or no professional work experience.

The research focuses on the role of professional experience, academic projects, internships, technical skills, and communication skills in students' employment prospects.

The repository provides a reproducible data-analysis workflow, including data validation, descriptive statistics, data-quality checks, a domain model, and scientific visualizations.

**Data status:** The analysis uses real responses from an anonymous Google Forms survey of IT students (17 respondents, 11 of whom had sent at least one application). The sample is a small convenience sample, so all results are exploratory and cannot be generalized to the student population. The earlier synthetic demonstration data were removed.

A 4-page IEEE-format paper based on these results is in [`paper/`](paper/) (`main.tex`, `references.bib`, compiled `main.pdf`).

## 2. Research Questions

- **RQ1:** What factors are associated with difficulties in finding a first IT job among students with little or no professional experience?
- **RQ2:** How are academic projects and internships associated with employment-related outcomes?
- **RQ3:** How are technical and communication skills associated with employment-related outcomes?

## 3. Research Hypotheses

The following hypotheses are based on the earlier project work:

- **H1:** Lack of professional experience is associated with greater difficulty finding a first job.
- **H2:** Students with practical experience from academic projects or internships have better employment prospects.
- **H3:** Higher technical and communication skills are associated with better employment prospects.

The corresponding null hypotheses state that there is no association between the respective factors and employment-related outcomes.

The hypotheses are tested exploratorily on the survey data (Section 6). With n = 17 none of the three primary tests is significant after Holm correction, so the data neither confirm nor reject H1-H3.

## 4. Dataset and Variables

The raw Google Forms export (Russian headers, with timestamps) is stored in `data/raw/` and is excluded from Git. `src/prepare_survey.py` converts it into the de-identified analysis file `data/survey/survey_clean.csv` (consent required, timestamps removed, identifiers S01-S17, answers translated to English).

| Variable | Description |
|---|---|
| `student_id` | Anonymous code |
| `study_year`, `track` | Study year (2-4) and main track |
| `professional_experience` | Professional IT experience (yes/no) |
| `academic_projects` | Number of study or personal projects |
| `internship` | Internship in an IT company (yes/no) |
| `technical_skills`, `communication_skills` | Self-rated skills, 1-5 |
| `applications_sent`, `interview_invitations`, `job_offers` | Job-search funnel counts |
| `working_in_it` | Currently working in IT (part-time or internship) / searching / not searching |
| `perceived_difficulty` | Perceived difficulty of a first IT job without experience, 1-5 |
| `barriers` | Perceived barriers (multi-select, `;`-separated) |

Rates are undefined for the 6 respondents with zero applications; they are excluded from rate statistics (not set to zero) and kept in the perception analyses.

## 5. Methodology

The analysis workflow consists of the following stages:

1. Load the sample dataset.
2. Validate required columns and record identifiers.
3. Check numeric values and consistency between applications, interview invitations, and job offers; exclude invalid records.
4. Calculate interview invitation and job offer rates.
5. Calculate descriptive statistics: mean, median, percentiles (p95, p99), and standard deviation.
6. Estimate bootstrap 95% confidence intervals for mean rates (5000 resamples).
7. Generate visualizations and export them in PNG (300 DPI) and PDF formats.
8. Save statistical summaries and data-quality results for reproducibility.

The bootstrap uses a fixed random seed (`42`) to make the calculations reproducible.

**Warm-up filtering.** The dataset consists of per-student survey-style counts, not timed benchmark runs, so there is no warm-up phase to discard. Data-quality guardrails (missing values, negative counts, invitations or offers exceeding applications) take the place of the warm-up filter.

Inferential steps (`src/inferential_analysis.py`): exact Mann-Whitney tests (permutation p-values with mid-ranks), Cliff's delta, Spearman correlation, Wilson intervals for pooled rates, bootstrap CI for the group difference, Fisher's exact test, leave-one-out sensitivity, and Holm correction for the three primary tests (H1-H3). All other tests are exploratory and unadjusted.

With n = 17 (11 applicants) percentiles and intervals are imprecise; p95 and p99 are shown for completeness only.

## 6. Results & Discussion

All numbers come from `results/` and are reproducible with the pipeline in Section 10.

### 6.1 Descriptive statistics (applicants only, n = 11)

| Indicator | n | Mean ± SD | Median | 95% bootstrap CI for mean |
|---|---:|---:|---:|---:|
| Interview invitation rate | 11 | 26.7% ± 22.2 | 25.0% | 14.3%-39.8% |
| Job offer rate per application | 11 | 16.6% ± 16.6 | 13.3% | 7.6%-26.4% |

Pooled over all applicants: 65 applications, 20 interview invitations (30.8%, Wilson 95% CI 20.9-42.8) and 12 offers (18.5%, 10.9-29.6).

### 6.2 Baseline (no internship) vs. internship

| Indicator | No internship (4 applicants) | Internship (7 applicants) |
|---|---:|---:|
| Pooled interview rate (Wilson 95% CI) | 17.6% (6.2-41.0) | 35.4% (23.4-49.6) |
| Median student rate [IQR] | 12.5% [0.0-27.1] | 26.7% [22.5-48.6] |
| Pooled offer rate | 11.8% (3.3-34.3) | 20.8% (11.7-34.3) |
| Currently working in IT (of 10 / 7 respondents) | 1 | 4 |

Mean difference in interview rate 19.0 pp (bootstrap 95% CI -2.6 to 39.5); exact Mann-Whitney p = 0.242, Cliff's delta = 0.46.

### 6.3 Hypothesis tests

| Test | n | Effect | p | Holm p |
|---|---:|---:|---:|---:|
| H1: perceived difficulty, no experience vs experience | 17 | delta = 0.26 | 0.378 | 0.485 |
| H2: interview rate, internship vs none | 11 | delta = 0.46 | 0.242 | 0.485 |
| H3: technical skills vs interview rate | 11 | rho = 0.52 | 0.103 | 0.309 |

Full list including exploratory tests: `results/tests_summary.csv`.

### 6.4 Perceived barriers (RQ1)

No professional experience 13/17 (76%), insufficient technical skills 11 (65%), no portfolio/projects 10 (59%), insufficient communication skills 6, few suitable vacancies 6, no employer response 4, language barrier 2. Median perceived difficulty is 4 of 5.

### 6.5 Figures

Figures are produced by `src/visualize.py` (PNG 300 DPI and vector PDF): `reports/figures/fig1_internship_comparison`, `fig2_rate_distributions`, and the three-panel paper figure `paper/figures/fig_results`.

### 6.6 Data quality

0 missing values, 0 negative counts, 0 records with invitations > applications or offers > invitations. Flags: 6 respondents with zero applications (rate undefined), 3 respondents selected more than the requested 3 barriers, 1 respondent who reports not searching but 2 applications. Flagged records were retained.

### 6.7 Interpretation

Results suggest, but do not demonstrate, a positive association of internship experience and technical skills with interview outcomes. The design can detect only very large effects (exact p < 0.05 requires |delta| >= 0.79 for 7 vs 4), so non-significance is not evidence of no effect.

## 7. Domain Model

The C4 container diagram (with the metric measurement nodes M1–M5), the entity and variable definitions, and the formal definitions of all metrics (rates, percentiles, bootstrap confidence interval, guardrails) are in [`docs/domain_model.md`](docs/domain_model.md).

The STRIDE threat model of the pipeline components is in [`docs/security_analysis.md`](docs/security_analysis.md). The research methodology is described in [`docs/methodology_passport.md`](docs/methodology_passport.md).

## 8. Baseline and Future Evaluation

The baseline is the group without internship experience. A future evaluation should use a larger multi-institution sample with a documented sampling frame and pre-registered sample size, adjust for confounders (year, track, number of applications) with count regression, and validate self-rated skills against objective assessments.

## 9. Repository Structure

```text
.
├── configs/
│   └── config.yaml
├── data/
│   ├── survey/
│   │   └── survey_clean.csv 
│   └── processed/
│       └── metrics_summary.csv
├── docs/
│   ├── domain_model.md
│   ├── methodology_passport.md
│   └── security_analysis.md
├── paper/
│   ├── main.tex, references.bib, main.pdf
│   └── figures/
├── notebooks/
│   ├── 01_data_analysis.ipynb
│   └── README.md
├── reports/
│   └── figures/
│       ├── fig1_internship_comparison.png
│       ├── fig1_internship_comparison.pdf
│       ├── fig2_rate_distributions.png
│       └── fig2_rate_distributions.pdf
├── results/
│   ├── analysis_summary.json
│   ├── statistical_summary.csv
│   └── data_quality_summary.csv
├── src/
│   ├── prepare_survey.py
│   ├── inferential_analysis.py
│   ├── benchmark.py
│   ├── process_data.py
│   ├── statistical_analysis.py
│   └── visualize.py
├── .gitignore
├── .python-version
├── requirements.txt
├── LICENSE
└── README.md
```

## 10. Reproducibility

The repository includes source scripts, the de-identified survey dataset, a configuration file, a Jupyter Notebook, and generated analysis outputs. All random steps use seed `42`.

Run everything from the repository root. Install the pinned dependencies:

```bash
python -m pip install -r requirements.txt
```

Run the pipeline in this order:

```bash
python src/prepare_survey.py        # data/raw -> data/survey (needs the raw export)
python src/process_data.py          # data/survey -> data/processed
python src/statistical_analysis.py  # statistics and data-quality summaries -> results/
python src/benchmark.py             # internship comparison -> results/analysis_summary.json
python src/inferential_analysis.py  # tests, barriers -> results/
python src/visualize.py             # figures -> reports/figures/, paper/figures/
```

Open the notebook and run it with **Kernel → Restart & Run All**:

```bash
jupyter notebook notebooks/01_data_analysis.ipynb
```

Compile the paper (Overleaf or `cd paper && latexmk -pdf main.tex`). The current output files are retained in the repository to support inspection and reproducibility.

## 11. Limitations and Next Steps

The main limitations are:

- Small convenience sample (n = 17; 11 applicants), likely affected by self-selection; no generalization.
- Observational design: no causal claims, no confounder adjustment.
- Self-reported single-item measures; "internship" and "working in IT" overlap.
- Low statistical power; Wilson intervals ignore clustering within students.

Next steps: collect a larger, multi-institution sample and run a pre-registered, adjusted analysis.

## License

This project is distributed under the MIT License. See the `LICENSE` file for details.

## Citation

Rakhimzhanova, Y., and Utebayeva, A. *IT Student Employability Research*. Student research project.

Repository: https://github.com/RakhimzhanovaYasmina/it-student-employability-research
