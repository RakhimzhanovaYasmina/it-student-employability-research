# Methodology Passport Card

## 1. Project Information

**Research Title:** Improving the Employability of IT Students with Little or No Professional Work Experience

**Authors:** Rakhimzhanova Yasmina and Utebayeva Anel 

**GitHub Repository:** https://github.com/RakhimzhanovaYasmina/it-student-employability-research

## 2. Research Type

**Research approach:** Quantitative, with an exploratory data-analysis pipeline.

The research questions focus on relationships between professional experience, practical experience, technical and communication skills, and employment prospects. These relationships can be investigated quantitatively using structured student-level data.

At the current stage, the repository contains synthetic demonstration data only. No empirical conclusions can be drawn until suitable real data have been collected or obtained from a documented and appropriate source.

## 3. Research Questions and Hypotheses

### RQ1

What are the main difficulties and factors affecting the search for a first job among IT students with little or no professional experience?

**H1₁ (Alternative Hypothesis):** Lack of professional experience is associated with a higher likelihood of difficulties in finding a first job among IT students.

**H0₁ (Null Hypothesis):** Lack of professional experience is not associated with a significant increase in difficulties in finding a first job among IT students.

### RQ2

How does practical experience gained through academic projects and internships affect the employment prospects of IT students?

**H1₂ (Alternative Hypothesis):** IT students with practical experience gained through academic projects or internships have better employment prospects than students without such experience.

**H0₂ (Null Hypothesis):** Practical experience gained through academic projects or internships has no statistically significant relationship with the employment prospects of IT students.

### RQ3

How does the level of technical and communication skills affect the employment prospects of IT students with little or no professional work experience?

**H1₃ (Alternative Hypothesis):** Higher levels of technical and communication skills are associated with better employment prospects among IT students with little or no professional work experience.

**H0₃ (Null Hypothesis):** Technical and communication skill levels have no statistically significant relationship with employment prospects among IT students with little or no professional work experience.

## 4. Variable Matrix

| Research Question | Independent Variables | Dependent Variables | Controlled / Potential Confounding Variables |
|---|---|---|---|
| RQ1 | Presence or absence of professional experience | Reported difficulty finding a first job | Education level, year of study, major, technical skills, portfolio projects |
| RQ2 | Presence and amount of academic project experience and internships | Interview invitations, job offers, first-job status | Year of study, major, technical skills, number of applications, résumé quality |
| RQ3 | Technical skill level and communication skill level | Interview invitations, job offers, employment status | Year of study, major, practical experience, number of applications, portfolio |

The variables follow the research framework established in Task 1. Operational definitions and measurement instruments must be finalized before analysing real data.

## 5. Metrics and Baseline

### Primary Metric

**Interview Invitation Rate**

Formula:

Interview Invitation Rate = Total Interview Invitations / Total Job Applications

This metric represents the proportion of applications resulting in interview invitations, provided that the data source records applications and invitations consistently.

### Secondary Metrics

- **Job Offer Rate per Application:** Total Job Offers / Total Job Applications.
- **Average Interview Invitations:** Mean number of interview invitations per student.
- **First IT Job Status:** Number or proportion of students who obtained a first IT job, if this information is collected.

These metrics describe different employment outcomes and should not be treated as interchangeable.

### Guardrail Metrics

- **Missing Values:** Number of required data fields that are empty.
- **Invalid Records:** Number of records that violate defined data-quality rules.
- **Sample Size:** Number of eligible observations available for analysis.

Guardrail metrics monitor data quality and the reliability of the analysis. They do not independently establish whether a hypothesis is supported.

### Baseline

**Demonstration baseline:** The current script compares synthetic records with and without internship experience. This comparison is used only to verify that the analysis pipeline runs successfully.

**Planned empirical baseline:** Once suitable real data are available, students without internship experience will be compared with students who have internship experience, provided that the final dataset supports this comparison.

This will be an observational comparison rather than a randomized experiment. Potential confounding variables, including year of study, technical skills, academic projects, and application volume, must be considered before drawing conclusions.

The synthetic demonstration results do not establish a real-world relationship between internships and employability.

## 6. Controlled Conditions and Reproducibility

The current pipeline uses:

- A fixed CSV schema and documented sample file.
- A configuration file at `configs/config.yaml`.
- An analysis script at `src/benchmark.py`.
- Configurable input and output paths.
- Data-quality checks before calculating metrics.
- Python 3.14.3, recorded in `.python-version`.
- PyYAML 6.0.3, pinned in `requirements.txt`.

The script reads the input and output paths from `configs/config.yaml`. The dependency can be installed using:

`python -m pip install -r requirements.txt`

The demonstration experiment can be run using:

`python src/benchmark.py`

The included synthetic sample, configuration, and analysis script are version-controlled. Generated analysis results are excluded from Git and can be recreated by running the script.

For the empirical analysis, the team must document the real data source, collection period, inclusion criteria, variable definitions, missing-data handling, and Python version.

## 7. Current Limitations

1. The sample dataset is synthetic and contains only eight records.
2. The sample is intended to test software execution and does not represent the IT student population.
3. The demonstration metrics cannot confirm or reject any research hypothesis.
4. The current script performs descriptive analysis and data-quality checks. It does not conduct statistical significance tests or control for confounding variables.
5. The operational definition of job-search difficulty for RQ1 requires a documented measurement method.
6. The current internship comparison is illustrative and cannot establish a causal relationship between internships and employment outcomes.

## 8. Next Research Steps

1. Identify an appropriate empirical data source or collect data using an approved research instrument.
2. Define inclusion criteria and operational measurements for every variable.
3. Document data provenance and prepare an anonymized analysis dataset.
4. Extend the pipeline with appropriate statistical tests when the data and sample size support them.
5. Consider relevant confounding variables during the analysis.
6. Interpret the results in relation to H0 and H1 and report limitations transparently.