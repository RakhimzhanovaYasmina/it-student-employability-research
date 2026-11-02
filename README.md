
# IT Student Employability Research

**Authors:** Rakhimzhanova Yasmina and Utebayeva Anel

## 1. Overview

This project investigates factors associated with the employability of IT students who have little or no professional work experience.

The research focuses on the role of professional experience, academic projects, internships, technical skills, and communication skills in students' employment prospects.

The repository provides a reproducible data-analysis workflow, including data validation, descriptive statistics, data-quality checks, and scientific visualizations.

**Data status:** The current dataset contains eight synthetic demonstration records. All results are preliminary pipeline-testing outputs, not empirical evidence about the student population.

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

These hypotheses have **not been empirically tested** using real student data. The current synthetic dataset is insufficient to draw conclusions about the hypotheses.

## 4. Dataset and Variables

The demonstration dataset is stored in `data/sample/sample.csv`.

It contains eight synthetic records and includes the following variables:

| Variable | Description |
|---|---|
| `student_id` | Synthetic record identifier |
| `professional_experience` | Whether professional experience is reported |
| `academic_projects` | Number of academic projects |
| `internship` | Whether internship experience is reported |
| `technical_skills` | Technical skills score |
| `communication_skills` | Communication skills score |
| `applications_sent` | Number of job applications |
| `interview_invitations` | Number of interview invitations |
| `job_offers` | Number of job offers |

The records are artificial and do not represent actual students. They are used to validate the analysis pipeline and demonstrate the expected outputs.

## 5. Methodology

The analysis workflow consists of the following stages:

1. Load the sample dataset.
2. Validate required columns and record identifiers.
3. Check numeric values and consistency between applications, interview invitations, and job offers.
4. Calculate interview invitation and job offer rates.
5. Calculate descriptive statistics, including the mean, median, percentiles, and standard deviation.
6. Estimate bootstrap 95% confidence intervals for mean rates.
7. Generate visualizations and export them in PNG and PDF formats.
8. Save statistical summaries and data-quality results for reproducibility.

The bootstrap uses a fixed random seed to make the demonstration calculations reproducible.

Because the dataset contains only eight synthetic records, the percentiles and confidence intervals are illustrative and should not be interpreted as reliable population estimates.

## 6. Results & Discussion

### 6.1 Descriptive statistics

The following results were calculated from the eight synthetic demonstration records.

| Indicator | n | Mean | Median | 95% bootstrap CI for mean |
|---|---:|---:|---:|---:|
| Interview invitation rate | 8 | 14.91% | 18.47% | 9.39%–19.87% |
| Job offer rate per application | 8 | 3.81% | 4.77% | 1.63%–5.89% |

**Definitions**

- **Interview invitation rate:** interview invitations divided by job applications for each record.
- **Job offer rate per application:** job offers divided by job applications for each record.
- **95% bootstrap confidence interval:** an interval estimated by resampling the available records to illustrate uncertainty in the sample mean.

The summary statistics describe the current demonstration dataset only. The small sample and synthetic nature of the records limit their interpretation.

### 6.2 Scientific visualizations

**Figure 1. Interview invitation rate by internship status**

This figure displays individual records and group means with 95% bootstrap confidence intervals.

- [View PNG](reports/figures/fig1_internship_comparison.png)
- [View PDF](reports/figures/fig1_internship_comparison.pdf)

**Figure 2. Distribution of employability indicators**

This figure compares the distributions of interview invitation rates and job offer rates per application, showing individual records alongside boxplots.

- [View PNG](reports/figures/fig2_rate_distributions.png)
- [View PDF](reports/figures/fig2_rate_distributions.pdf)

Both figures are exported as PNG at 300 DPI and as PDF.

### 6.3 Data quality

The current eight-record demonstration dataset passed the implemented checks:

| Data-quality check | Invalid records detected |
|---|---:|
| Negative applications | 0 |
| Negative interview invitations | 0 |
| Negative job offers | 0 |
| Interview invitations exceeding applications | 0 |
| Job offers exceeding applications | 0 |

These checks confirm that the sample passes the implemented validation rules. They do not establish that the data are representative or that all possible data-quality problems have been eliminated.

### 6.4 Interpretation

The pipeline successfully demonstrates data processing, descriptive statistics, bootstrap confidence intervals, data-quality checks, and figure export.

The internship comparison is exploratory. It cannot establish that internships cause better employment outcomes. Any apparent differences may also reflect other variables.

No conclusion about H1, H2, or H3 can be justified from these synthetic records. Testing the research hypotheses requires real, appropriately collected student data and a suitable statistical analysis.

## 7. Baseline and Future Evaluation

The current exploratory baseline compares interview invitation rates between records with and without internship experience.

A future empirical evaluation should use a documented data-collection procedure and a sufficiently large sample of actual IT students. The analysis should define the outcome variables in advance, examine missing data, account for relevant confounding factors, and use statistical methods appropriate to the research questions and data.

The current comparison is a pipeline demonstration, not a completed empirical evaluation.

## 8. Repository Structure

```text
.
├── configs/
│   └── config.yaml
├── data/
│   ├── sample/
│   │   └── sample.csv
│   └── processed/
│       └── metrics_summary.csv
├── docs/
│   └── methodology_passport.md
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

The domain model document will be added under `docs/domain_model.md` when its contents are finalized.

## 9. Reproducibility

The repository includes source scripts, a demonstration dataset, a configuration file, a Jupyter Notebook, and generated analysis outputs.

Run the scripts from the repository root. The commands below use the virtual environment's Python executable on Windows.

Install the required packages if they are not already installed:

```bash
python -m pip install pandas numpy matplotlib seaborn jupyter PyYAML
```

Run the data-processing step:

```bash
python src/process_data.py
```

Run the statistical analysis:

```bash
python src/statistical_analysis.py
```

Generate the figures:

```bash
python src/visualize.py
```

Open the notebook:

```bash
jupyter notebook notebooks/01_data_analysis.ipynb
```

The scripts save processed data, statistical summaries, data-quality results, and figures to the project directories. The current output files are retained in the repository to support inspection and reproducibility.

**Note:** The Python package requirements should be kept consistent with the dependencies used by the scripts and notebook.

## 10. Limitations and Next Steps

The main limitations are:

- The current dataset contains only eight synthetic records.
- The results cannot be generalized to the student population.
- The analysis is descriptive and does not establish causality.
- The research hypotheses have not been tested on empirical data.
- The data-collection procedure and the suitability of the measures must be established before substantive conclusions can be drawn.

The next steps are to finalize the domain model, document the research methodology, collect suitable real-world data, and conduct an appropriate empirical evaluation.

## License

This project is distributed under the MIT License. See the `LICENSE` file for details.

## Citation

Rakhimzhanova, Y., and Utebayeva, A. *IT Student Employability Research*. Student research project.

Repository: https://github.com/RakhimzhanovaYasmina/it-student-employability-research
