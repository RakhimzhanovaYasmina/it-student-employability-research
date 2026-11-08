# Security Analysis — STRIDE Threat Model

## 1. Purpose

This document identifies potential security threats in the IT Student Employability Research project using the STRIDE threat-modeling framework. It covers the same components as the C4 diagram in [`domain_model.md`](domain_model.md).

The project is a local Python-based research pipeline. It reads a synthetic student dataset from a CSV file, loads configuration from YAML, validates records, calculates research metrics, generates figures, and saves results as CSV, JSON, PNG, and PDF files.

The current implementation does not include a web server, database, authentication service, or network API.

## 2. System Scope

| ID | Component | Description | Domain model node |
|---|---|---|---|
| C1 | `configs/config.yaml` | Project configuration: paths, variables, metric settings, random seed | Configuration |
| C2 | `data/sample/sample.csv` | Synthetic student demonstration records (input) | Sample Dataset |
| C3 | `src/process_data.py` | Validates records, removes invalid ones, computes per-student rates | Data Processing (M1) |
| C4 | `data/processed/metrics_summary.csv` | Student-level rates and the OVERALL row | Processed Metrics |
| C5 | `src/statistical_analysis.py` | Computes mean, median, p95, p99, SD, bootstrap 95% CI, data-quality checks | Statistical Analysis (M2, M3) |
| C6 | `src/benchmark.py` | Loads configuration and data, validates records, compares internship groups | Baseline Comparison (M4) |
| C7 | `results/` (`statistical_summary.csv`, `data_quality_summary.csv`, `analysis_summary.json`) | Aggregated analysis results | Analysis Results |
| C8 | `src/visualize.py` | Generates figures from processed data | Visualization (M5) |
| C9 | `reports/figures/` | Exported PNG and PDF figures | Figures |
| C10 | `notebooks/01_data_analysis.ipynb` | Jupyter notebook that repeats the analysis and exports figures and results | Analysis Notebook |
| C11 | `requirements.txt` and the Python environment | Third-party packages used by scripts and notebook | — |

## 3. STRIDE Threat Analysis

| STRIDE category | Potential threat | Affected components | Mitigation |
|---|---|---|---|
| Spoofing | The input CSV is replaced by a file from an untrusted source and treated as the genuine dataset | C2 | Use trusted input sources, review changes to the file in Git before analysis |
| Spoofing | A package with a look-alike name or a tampered release is installed instead of the intended dependency | C11 | Install only from the official package index, keep versions pinned in `requirements.txt` |
| Tampering | Input records or configuration values are modified without authorization, changing the results | C1, C2, C4 | Restrict write access, review changes through Git, validate input values (already implemented) |
| Tampering | Processed or result files are edited by hand so they no longer match the scripts' output | C4, C7, C9 | Regenerate outputs with the scripts, compare regenerated files with the committed ones |
| Tampering | The notebook is saved with outputs that do not match its code | C10 | Run the notebook with Kernel → Restart & Run All before committing |
| Repudiation | A previous analysis run or file modification cannot be reliably traced | C3, C5, C6, C8, C10 | Keep source files in Git, use fixed random seed 42, document runs in commit messages |
| Information Disclosure | Real personal data are added to the dataset and published with the repository | C2, C4, C7 | Keep only synthetic or anonymized records, check files before pushing, keep `data/raw/` in `.gitignore` |
| Information Disclosure | A notebook output, log, or error message exposes local file paths or other local details | C10, C3, C5 | Review notebook outputs before committing, avoid committing logs (`*.log` is ignored) |
| Denial of Service | An excessively large or malformed CSV causes high memory use or stops processing | C3, C5, C6 | Validate input files, limit dataset size, handle parsing errors |
| Denial of Service | A bootstrap run with a very large iteration count or data size blocks the analysis | C5, C8, C10 | Keep the iteration count fixed in code (5000) and the dataset size bounded |
| Elevation of Privilege | Untrusted code or an unsafe dependency runs with the user's local rights | C11, C3, C5, C6, C8 | Use trusted dependencies, review code changes, do not run unreviewed scripts |
| Elevation of Privilege | Opening an untrusted notebook executes code in the local environment | C10 | Open and run only notebooks from the project repository, review code cells first |

## 4. Risk Assessment

The following qualitative assessment considers the current local research environment.

| Threat | Likelihood | Impact | Priority |
|---|---|---|---|
| Spoofing | Low | Medium | Low |
| Tampering | Medium | Medium | Medium |
| Repudiation | Medium | Low | Low |
| Information Disclosure | Low | Medium | Low |
| Denial of Service | Medium | Medium | Medium |
| Elevation of Privilege | Low | High | Medium |

These ratings are preliminary assessments, not results of a formal security test.

## 5. Existing Security Controls

The current implementation provides several basic protections:

- Required CSV columns are checked before analysis (`process_data.py`, `benchmark.py`).
- Records with missing or negative counts, or with invitations or offers exceeding applications, are excluded (`process_data.py`) or reported (`statistical_analysis.py`).
- Duplicate or missing student IDs are removed (`process_data.py`).
- Counts are validated as non-negative integers and skill ratings are restricted to 1–5 (`benchmark.py`).
- YAML configuration is loaded using `yaml.safe_load`.
- Random steps use a fixed seed (42), so results can be reproduced and compared.
- Package versions are pinned in `requirements.txt`.
- `.gitignore` excludes virtual environments, caches, notebook checkpoints, logs, secrets files (`.env`), and `data/raw/`.
- The project uses Git for version control and change tracking.
- The demonstration dataset contains synthetic records rather than real student personal data.

These controls improve input validation and reduce some risks, but they do not replace a full security audit.

## 6. Limitations

- The project is a local research pipeline, not a deployed web application.
- No database, authentication mechanism, or network API is included in the current architecture.
- The threat assessment is qualitative and has not been validated through penetration testing.
- The dataset contains synthetic demonstration records.
- Security controls depend partly on the local operating system, repository permissions, and user practices.

## 7. Conclusion

The main security considerations for this project are protecting input and configuration files, ensuring data integrity, keeping dependencies trustworthy, preventing accidental disclosure, and handling malformed or excessively large input files.

The STRIDE analysis is scoped to the components that exist in the current local Python research pipeline and matches the containers in [`domain_model.md`](domain_model.md).
