# Research Notebooks

This directory contains the Jupyter notebook used for the data analysis and scientific visualization of the project.

## Contents

| File | Description |
|---|---|
| `01_data_analysis.ipynb` | Loads `data/processed/metrics_summary.csv`, checks data quality, computes descriptive statistics (mean, median, percentiles, SD) and bootstrap 95% confidence intervals, creates the figures, and saves results |

The notebook works with the eight synthetic demonstration records. Its results are pipeline-testing outputs, not empirical evidence about the student population.

## What the notebook writes

- `reports/figures/fig1_internship_comparison.png` and `.pdf`
- `reports/figures/fig2_rate_distributions.png` and `.pdf`
- `results/statistical_summary.csv`
- `results/data_quality_summary.csv`

## How to run

1. Install dependencies from the repository root:

   ```bash
   python -m pip install -r requirements.txt
   ```

2. Generate the processed data (the notebook reads it):

   ```bash
   python src/process_data.py
   ```

3. Start Jupyter from the repository root and open the notebook:

   ```bash
   jupyter notebook notebooks/01_data_analysis.ipynb
   ```

   The notebook finds the project root relative to the `notebooks/` directory, so keep its location unchanged.

4. Run **Kernel → Restart & Run All** and check that every cell finishes without errors. The random seed is `42`.

Before committing, save the notebook with its outputs, and do not commit `.ipynb_checkpoints/` (it is ignored in `.gitignore`).

The same calculations are available as scripts in `src/`: `process_data.py`, `statistical_analysis.py`, and `visualize.py`.
