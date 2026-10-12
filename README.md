
# IT Student Employability Research

**Authors:** Rakhimzhanova Yasmina and Utebayeva Anel

## Overview

This project examines factors associated with the employability of IT students
who have little or no professional work experience.

The study focuses on job-search difficulties, practical experience gained
through academic projects and internships, and the role of technical and
communication skills.

## Research Questions

- **RQ1:** What are the main difficulties and factors affecting the search
  for a first job among IT students with little or no professional experience?
- **RQ2:** How does practical experience gained through academic projects
  and internships relate to employment prospects?
- **RQ3:** How are technical and communication skills associated with
  employment prospects?

## Research Hypotheses

The hypotheses are based on Task 1. They will be evaluated only when suitable
empirical data become available.

- **H1₁:** Lack of professional experience is associated with greater
  difficulty finding a first job.
- **H1₂:** Students with practical experience from academic projects or
  internships have better employment prospects.
- **H1₃:** Higher technical and communication skills are associated with
  better employment prospects.

The corresponding null hypotheses state that these relationships are not
statistically significant.

## Current Data Status

The included CSV file contains synthetic demonstration data only.
It is used to test the analysis pipeline and does not represent real students.

The demonstration output must not be interpreted as evidence confirming or
rejecting the research hypotheses.

## Repository Structure

```text
.
├── configs/
│   └── config.yaml
├── data/
│   └── sample/
│       └── sample.csv
├── docs/
├── notebooks/
├── results/                  # Generated locally; ignored by Git
├── src/
│   └── benchmark.py
├── .gitignore
├── LICENSE
├── README.md
└── requirements.txt
```

## System Requirements

- Python 3.10 or later
- Git (required for version control)
- No third-party Python packages are required for the current script.

## Quickstart

Run these commands from the repository root.

```bash
python --version
python src/benchmark.py
```

The script reads `data/sample/sample.csv` and writes the analysis summary to
`results/analysis_summary.json`.

## Planned Evaluation Metrics

| Metric | Type | Purpose |
|---|---|---|
| Interview invitation rate | Primary | Proportion of invitations relative to applications |
| Job offer rate per application | Secondary | Proportion of offers relative to applications |
| Average interview invitations | Secondary | Mean number of interview invitations per record |
| Missing values | Guardrail | Checks data completeness |
| Invalid records | Guardrail | Checks basic data consistency |

These metrics are demonstrated on synthetic data. Their suitability for
hypothesis testing must be reassessed when real data and the data-collection
method are established.

## Baseline

The current demonstration compares records with and without internship
experience. The comparison is illustrative only and is not a valid empirical
conclusion about the student population.

## Reproducibility

The analysis script, configuration, and sample data are version-controlled.
Generated result files are excluded from Git and can be recreated by running
the script.

## License

This project is distributed under the MIT License. See `LICENSE`.

## Citation

This repository is a student research project prepared for Task 2.
Please cite the authors and repository URL after the public GitHub repository
has been created.
