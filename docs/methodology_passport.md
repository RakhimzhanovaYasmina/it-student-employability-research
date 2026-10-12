
# Methodology Passport Card

## 1. Project Information

**Research Title:** Improving the Employability of IT Students with Little or No Professional Work Experience

**Authors:** Rakhimzhanova Yasmina and Utebayeva Anel

**GitHub Repository:** To be added after the repository is published.

## 2. Research Type

**Proposed approach:** Quantitative, with an exploratory data-analysis pipeline.

The research questions focus on relationships between professional experience, practical experience, technical and communication skills, and employment prospects. These relationships can be investigated quantitatively using structured student-level data.

At the current stage, the repository contains synthetic demonstration data only. No empirical conclusions can be drawn until suitable real data have been collected or obtained from a documented, appropriate source.

## 3. Research Questions and Hypotheses

### RQ1
What are the main difficulties and factors affecting the search for a first job among IT students with little or no professional experience?

**H1₁ (Alternative):** Lack of professional experience is associated with a higher likelihood of difficulties in finding a first job among IT students.

**H0₁ (Null):** Lack of professional experience is not associated with a significant increase in difficulties in finding a first job among IT students.

### RQ2
How does practical experience gained through academic projects and internships affect the employment prospects of IT students without professional experience?

**H1₂ (Alternative):** IT students with practical experience gained through academic projects or internships have better employment prospects than students without such experience.

**H0₂ (Null):** Practical experience gained through academic projects or internships has no statistically significant effect on the employment prospects of IT students without professional experience.

### RQ3
How does the level of technical and communication skills affect the employment prospects of IT students with little or no professional experience?

**H1₃ (Alternative):** A higher level of technical and communication skills is associated with better employment prospects among IT students with little or no professional experience.

**H0₃ (Null):** The level of technical and communication skills has no statistically significant relationship with employment prospects among IT students with little or no professional experience.

## 4. Variable Matrix

| Research Question | Independent Variables | Dependent Variables | Controlled / Potential Confounding Variables |
|---|---|---|---|
| RQ1 | Presence or absence of professional experience | Reported difficulty finding a first job | Education level, year of study, major, technical skills, portfolio projects |
| RQ2 | Presence and amount of academic project experience and internships | Interview invitations, job offers, first-job status | Year of study, major, technical skills, number of applications, résumé quality |
| RQ3 | Technical skill level and communication skill level | Interview invitations, job offers, employment status | Year of study, major, practical experience, number of applications, portfolio |

The variables above follow the research framework established in Task 1. Operational definitions and measurement instruments must be finalized before analysing real data.

## 5. Metrics and Baseline

### Primary Metric

**Interview invitation rate**

Formula:

Interview invitation rate = total interview invitations / total job applications

This metric represents the proportion of applications that result in interview invitations, provided that the data source records applications and invitations consistently.

### Secondary Metrics

- Job offer rate per application = total job offers / total job applications.
- Average number of interview invitations per student.
- Number or proportion of students who obtained a first IT job, if this information is collected.

These metrics describe different employment outcomes and should not be treated as interchangeable.

### Guardrail Metrics

- **Missing values:** number of required data fields that are empty.
- **Invalid records:** number of records that violate defined data-quality rules.
- **Sample size:** number of eligible observations available for analysis.

Guardrail metrics monitor data quality and the reliability of the analysis. They do not independently establish that a hypothesis is supported.

### Baseline

For the initial software demonstration, the script compares records with and without internship experience.

For the empirical study, the baseline will be students without internship experience compared with students who have internship experience, provided that the final dataset supports this comparison.

This comparison is observational rather than randomized. Potential confounding variables, such as year of study, technical skills, and application volume, must be considered before drawing conclusions.

## 6. Controlled Conditions and Reproducibility

The current pipeline uses:

- A fixed CSV schema and documented sample file.
- A configuration file at `configs/config.yaml`.
- A Python analysis script at `src/benchmark.py`.
- A fixed input path and output format.
- Data-quality checks before calculating metrics.

The demonstration script uses Python's standard library and does not require third-party packages.

For the empirical analysis, the team must document the real data source, collection period, inclusion criteria, variable definitions, missing-data handling, and Python version.

## 7. Current Limitations

1. The sample dataset is synthetic and contains only eight records.
2. The sample is intended to test software execution, not represent the IT student population.
3. The demonstration metrics cannot confirm or reject any research hypothesis.
4. The current script performs descriptive analysis and does not conduct statistical significance tests or control for confounding variables.
5. The operational definition of job-search difficulty for RQ1 requires a documented measurement method.

## 8. Next Research Steps

1. Identify an appropriate empirical data source or collect data using an approved research instrument.
2. Define inclusion criteria and operational measurements for every variable.
3. Document data provenance and prepare an anonymized analysis dataset.
4. Extend the pipeline with appropriate statistical tests when the data and sample size support them.
5. Interpret the results in relation to H0 and H1 and report limitations transparently.
