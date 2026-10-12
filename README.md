# IT Student Employability Research

**Authors:** Rakhimzhanova Yasmina

## Overview

This project investigates factors associated with the employability of IT students who have little or no professional work experience.

The research focuses on difficulties in finding a first IT job, practical experience gained through academic projects and internships, and the role of technical and communication skills.

The repository provides a reproducible data-analysis pipeline for checking data quality and calculating descriptive employment-related metrics.

## Research Questions

- **RQ1:** What are the main difficulties and factors affecting the search for a first job among IT students with little or no professional experience?
- **RQ2:** How does practical experience gained through academic projects and internships relate to employment prospects?
- **RQ3:** How are technical and communication skills associated with employment prospects?

## Research Hypotheses

The following alternative hypotheses are based on Task 1.

- **H1₁:** Lack of professional experience is associated with greater difficulty finding a first job.
- **H1₂:** Students with practical experience from academic projects or internships have better employment prospects.
- **H1₃:** Higher technical and communication skills are associated with better employment prospects.

The corresponding null hypotheses state that there is no statistically significant relationship between the respective factors and employment outcomes.

These hypotheses have not yet been empirically tested by the demonstration pipeline.

## Current Data Status

The included file `data/sample/sample.csv` contains eight synthetic demonstration records. These records are used exclusively to test the analysis pipeline and do not represent real students.

The generated results must not be interpreted as evidence confirming or rejecting the research hypotheses. Empirical conclusions require suitable real-world data and an appropriate statistical analysis.

## Repository Structure

```text
.
├── configs/
│   └── config.yaml
├── data/
│   └── sample/
│       └── sample.csv
├── docs/
│   └── methodology_passport.md
├── notebooks/
├── src/
│   └── benchmark.py
├── .gitignore
├── .python-version
├── LICENSE
├── README.md
└── requirements.txt
```

The `results/` directory is generated locally when the script runs and is excluded from Git.

## System Requirements

- Python 3.14.3
- Git for version control
- PyYAML 6.0.3, specified in `requirements.txt`

The required Python version is recorded in `.python-version`.

## Quickstart

Run the following commands from the repository root.

**1. Verify the Python version:**

```bash
python --version
```

Expected output:

```text
Python 3.14.3
```

**2. Install the pinned dependency:**

```bash
python -m pip install -r requirements.txt
```

**3. Run the demonstration experiment:**

```bash
python src/benchmark.py
```

The script reads the input and output paths from `configs/config.yaml`, processes the sample data, and writes the analysis summary to `results/analysis_summary.json`.

A successful run prints the number of records analyzed and the interview invitation rate. The script also identifies the output as synthetic demonstration data.

## Planned Evaluation Metrics

| Metric | Type | Purpose |
|---|---|---|
| Interview invitation rate | Primary | Measures interview invitations relative to job applications |
| Job offer rate per application | Secondary | Measures job offers relative to job applications |
| Average interview invitations | Secondary | Calculates the mean number of interview invitations per record |
| Missing values | Guardrail | Checks data completeness |
| Invalid records | Guardrail | Checks basic data consistency |

The metrics are currently demonstrated on synthetic data. Their suitability for testing the research hypotheses must be reassessed when real data and the data-collection procedure are established.

## Baseline

The demonstration pipeline compares records with and without internship experience.

This is an exploratory observational comparison, not a randomized experiment. Differences between the groups may be influenced by other factors, including technical skills, communication skills, academic projects, and previous professional experience.

The synthetic comparison does not establish a real-world relationship between internships and employability.

## Reproducibility

The repository contains the analysis script, configuration file, sample data, and dependency specification.

The script uses the configuration file to locate the input data and output file. Generated analysis results are excluded from Git and can be recreated by running the Quickstart commands.

The dependency version is pinned in `requirements.txt`. The Python version is recorded in `.python-version`.

## Limitations and Next Steps

The current pipeline performs descriptive analysis and basic data-quality checks. It does not perform statistical hypothesis tests.

The next research stage is to collect suitable empirical data, assess data quality, refine the operational definitions of the variables, and conduct appropriate statistical analyses to evaluate the hypotheses.

## License

This project is distributed under the MIT License. See the `LICENSE` file for details.

## Citation

Rakhimzhanova, Y., and Utebayeva, A. *IT Student Employability Research*. Student research project, Task 2.

Repository: https://github.com/RakhimzhanovaYasmina/it-student-employability-research