# Methodology Passport Card

## 1. Project Information

**Research Title:** Perceived Barriers and Early Job-Search Outcomes of IT Students Without Professional Experience: An Exploratory Survey

**Authors:** Yasmina Rakhimzhanova and Anel Utebayeva

**GitHub Repository:** https://github.com/RakhimzhanovaYasmina/it-student-employability-research

## 2. Research Design

**Research approach:** Quantitative, cross-sectional, exploratory survey research.

The study uses an anonymous Google Forms survey completed by 17 IT students. The sample is a non-probability convenience sample. The analysis examines students' perceived barriers to entering the IT labour market and descriptive associations between practical experience, self-rated skills, and early job-search outcomes.

The results are exploratory. The observational design and small sample do not support causal conclusions or broad generalisation to the IT student population.

## 3. Research Questions and Hypotheses

### RQ1

What factors do students perceive as hindering their first IT job, and is lack of professional experience associated with higher perceived difficulty?

**H1 (Alternative):** Students without professional experience report higher job-search difficulty than students with professional experience.

**H0 (Null):** Perceived job-search difficulty is not associated with professional experience.

### RQ2

How are academic projects and internships associated with interview invitations, job offers, and current IT employment?

**H2 (Alternative):** Students with internship experience have a higher interview-invitation rate than students without internship experience.

**H0 (Null):** Internship experience is not associated with the interview-invitation rate.

### RQ3

How are self-rated technical and communication skills associated with early job-search outcomes?

**H3 (Alternative):** Higher self-rated technical skill is positively associated with the interview-invitation rate.

**H0 (Null):** Self-rated technical skill is not associated with the interview-invitation rate.

Communication skills and other outcomes are also explored descriptively; they are not part of the three pre-specified primary hypotheses.

## 4. Variables and Operational Measures

| Research question | Explanatory variables | Outcomes | Notes / potential confounders |
|---|---|---|---|
| RQ1 | Professional experience (yes/no) | Self-reported job-search difficulty (1–5); selected barriers | Study year, IT track, skills, practical experience |
| RQ2 | Internship (yes/no); number of academic projects | Interview invitations, job offers, current IT employment | Applications, study year, IT track, skills; observational comparison only |
| RQ3 | Self-rated technical skills (1–5); communication skills (1–5) | Interview-invitation rate; offer rate in exploratory analyses | Internship, projects, applications, study year, IT track |

The dataset contains 17 respondent records. All 17 respondents consented and were retained. Six respondents had submitted no applications; therefore, the rate analyses use the 11 applicants, while perception analyses use all 17 respondents.

## 5. Metrics and Baseline

### Primary outcome metric

**Student-level interview-invitation rate:**

`r_i = interview invitations_i / job applications_i`

This rate is defined only for respondents with at least one application. Respondents with zero applications are not assigned a zero rate because not applying is different from applying without receiving an invitation.

### Additional metrics

- **Student-level offer rate:** job offers divided by applications, for applicants only.
- **Pooled interview-invitation rate:** total interview invitations divided by total applications in a group.
- **Pooled offer rate:** total job offers divided by total applications in a group.
- **Perceived difficulty:** self-reported rating on a five-point scale.
- **Current IT employment:** number and proportion of respondents currently working in IT.
- **Perceived barriers:** number and proportion of respondents selecting each barrier.

### Observed sample and descriptive baseline

- Total respondents: **17**.
- Applicants: **11**; respondents with no applications: **6**.
- Total applications: **65**.
- Interview invitations: **20**; pooled interview-invitation rate: **30.8%**.
- Job offers: **12**; pooled offer rate: **18.5%**.
- Respondents currently working in IT: **5**.
- Mean perceived job-search difficulty: **3.82/5**.

The main RQ2 descriptive comparison is between applicants without internship experience (baseline: 4 applicants, 17 applications) and applicants with internship experience (7 applicants, 48 applications). Their pooled interview-invitation rates are 17.6% and 35.4%, respectively. This is an observational comparison and must not be interpreted as evidence that internships caused the difference.

## 6. Statistical Analysis and Reproducibility

The analysis pipeline includes the following scripts:

- `src/prepare_survey.py` — prepares the survey export, including the English analysis schema and respondent inclusion based on consent.
- `src/process_data.py` — validates and processes the survey data and derives analysis variables.
- `src/statistical_analysis.py` — produces descriptive statistics and summary measures.
- `src/inferential_analysis.py` — performs the pre-specified and exploratory inferential analyses.
- `src/visualize.py` — generates figures used in the analysis and paper.
- `src/benchmark.py` — supports the project's benchmark/demo workflow; it is not the main empirical survey-analysis entry point.

The empirical analysis uses:

- Bootstrap resamples: **5,000**.
- Random seed: **42**.
- Significance level: **0.05**.
- Primary hypothesis tests in the Holm correction family: **3**.
- Rank-based methods for ordinal ratings and small-sample comparisons.
- Wilson confidence intervals for pooled proportions, interpreted descriptively because applications are clustered within students.
- Exact permutation p-values for rank-based group comparisons, effect sizes (including Cliff's delta), and Spearman's rank correlation where appropriate.
- Holm adjustment for the three primary tests; exploratory tests are reported without that adjustment.

Install the dependencies listed in `requirements.txt` with:

`python -m pip install -r requirements.txt`

The repository includes a de-identified survey dataset at `data/survey/survey_clean.csv`, a processed metrics file at `data/processed/metrics_summary.csv`, configuration in `configs/config.yaml`, analysis scripts in `src/`, and generated outputs in the results/report folders. The original Google Forms export is kept out of version control for privacy. The exact analysis commands and configured input/output paths should be followed as documented in the repository README and configuration file.

## 7. Main Findings and Hypothesis Outcomes

The most frequently reported barriers were lack of professional experience (13 of 17 respondents; 76.5%), insufficient technical skills (11 of 17; 64.7%), and lack of a portfolio or projects (10 of 17; 58.8%).

For the internship comparison, the pooled interview-invitation rate was higher among applicants with internship experience (35.4%) than among those without it (17.6%). The estimated group difference was not statistically significant after the study's testing procedure. Self-rated technical skills had a moderate positive Spearman association with interview-invitation rate, but this result was also not statistically significant after Holm correction.

None of the three pre-specified hypotheses was statistically supported in this sample after Holm correction (all adjusted p-values exceeded 0.05). This does not demonstrate that the relationships are absent; the small sample provides limited statistical power and estimates are imprecise.

## 8. Limitations

1. The sample is small (17 respondents; 11 applicants) and was recruited through convenience channels.
2. The sample is not representative of all IT students; results should not be generalised to the wider population.
3. The study is observational and cross-sectional; associations cannot establish causation.
4. Skills and perceived difficulty are self-reported single-item measures and may be affected by self-assessment bias.
5. Internship experience and current IT employment may overlap, complicating interpretation of employment status.
6. Wilson intervals for pooled application-level rates treat applications as independent and do not account for multiple applications from the same student.
7. Six respondents had no applications, so their interview and offer rates are undefined and excluded from rate analyses.
8. Three respondents selected more than the requested maximum number of barriers, and one respondent reported not yet searching while also reporting two applications; these inconsistencies were retained and flagged.
9. Potential confounding variables were not jointly adjusted for in the primary analysis.

## 9. Future Research

1. Recruit a larger and more diverse sample across institutions, study years, and IT specialisations.
2. Use longitudinal data to follow applications, interviews, offers, and employment outcomes over time.
3. Collect more objective measures of technical and communication skills alongside self-assessments.
4. Record relevant covariates consistently, including application volume, study year, IT track, project experience, and internship characteristics.
5. With a sufficiently large sample, use models that account for the number of applications and the clustering of applications within students.
6. Pre-register hypotheses, outcome definitions, and a target sample size for a follow-up study.
