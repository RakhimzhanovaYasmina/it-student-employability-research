# Security Analysis — STRIDE Threat Model

## 1. Purpose

This document identifies potential security threats in the IT Student Employability Research project using the STRIDE threat-modeling framework.

The project is a local Python-based research pipeline. It reads a synthetic student dataset from a CSV file, loads configuration from YAML, validates records, calculates research metrics, and saves aggregated results as JSON.

The current implementation does not include a web server, database, authentication service, or network API.

## 2. System Scope

The security analysis covers the following components:

| Component | Description |
|---|---|
| `configs/config.yaml` | Stores project configuration, input and output paths, variables, and metric settings |
| `data/sample/sample.csv` | Contains synthetic student demonstration records |
| `src/benchmark.py` | Loads configuration and data, validates records, calculates metrics, and generates results |
| `results/analysis_summary.json` | Stores aggregated analysis results |

## 3. STRIDE Threat Analysis

| STRIDE category | Potential threat | Affected component | Mitigation |
|---|---|---|---|
| Spoofing | An attacker replaces the expected input CSV with a file from an untrusted source | `data/sample/sample.csv` | Use trusted input sources and verify files before analysis |
| Tampering | Input records or configuration values are modified without authorization | CSV and YAML files | Restrict write access, review changes through Git, and validate input values |
| Repudiation | A previous analysis run or file modification cannot be reliably traced | Research pipeline and Git history | Keep version-controlled source files and document analysis runs |
| Information Disclosure | Research outputs or files are accidentally published or shared | `results/analysis_summary.json` and repository | Check files before publishing and avoid including personal or confidential information |
| Denial of Service | An excessively large or malformed CSV file causes high memory consumption or prevents processing | `src/benchmark.py` | Validate input files, limit dataset size, and handle parsing errors |
| Elevation of Privilege | Untrusted code or unsafe dependencies are executed in the local environment | Python execution environment | Use trusted dependencies, review code changes, and avoid executing untrusted scripts |

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

- Required CSV columns are checked before analysis.
- Numeric fields are validated as non-negative integers.
- Skill ratings are restricted to the range from 1 to 5.
- Application outcome counts are checked for consistency.
- YAML configuration is loaded using `yaml.safe_load`.
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

The main security considerations for this project are protecting input and configuration files, ensuring data integrity, preventing accidental disclosure, and handling malformed or excessively large input files.

The STRIDE analysis is scoped to the components that exist in the current local Python research pipeline.