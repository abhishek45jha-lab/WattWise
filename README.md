# WattWise — Electricity Waste Detective

*A Python-Based Data Science Project*

WattWise is a local, beginner-readable data science application for exploring interval electricity-consumption CSV files. It cleans readings, calculates descriptive statistics, visualizes usage patterns, applies an upper-fence IQR rule, generates transparent recommendations, and evaluates hypothetical reduction scenarios.

**Important:** a statistically unusual reading is an investigation lead—not proof of electricity waste, a faulty appliance, theft, or guaranteed savings.

## Verified implementation status

Verified on **27 October 2026** in the available Linux Python environment:

- `sample_data.csv` generated successfully: **1,440 rows**, 60 days × 24 hourly readings.
- **18 `unittest` tests passed** in the project virtual environment.
- `validate_project.py` completed its dataset, interval, and complete-day assertions.
- `validate_app.py` completed a **headless Streamlit smoke test**: five tabs rendered without an application exception.
- The Streamlit server started successfully and its local page returned HTTP 200.
- Synthetic results and five Matplotlib chart assets were regenerated successfully.

Tested with Python 3.13.16, NumPy 2.5.4, Pandas 3.1.0, Matplotlib 3.11.2, and Streamlit 1.66.1. The headless test does **not** verify visual appearance in every browser. A native Windows run has not been performed here; exact Windows instructions are provided in `EXECUTION_GUIDE.md`.

## Features

- Built-in reproducible synthetic dataset or user-uploaded CSV.
- Required-column validation and optional-column preservation.
- Datetime parsing, numeric conversion, missing-value reporting, exact-duplicate and duplicate-timestamp handling, negative/non-finite checks, and chronological sorting.
- Data-quality report with explicit counts for every removal category.
- Total, mean, median, minimum, maximum, population variance, population standard deviation, and valid-observation count.
- Median interval inference and regularity check.
- Daily totals with complete-day flags; weekday/weekend comparison only for complete days.
- Upper-fence IQR flagging with small-data and constant-data safeguards.
- Time, daily, distribution, high-reading, and day-type Matplotlib charts when supported by the data.
- Hypothetical 5%, 10%, 15%, 20%, and custom reduction scenarios with a user-entered INR tariff.
- Rule-based recommendations tied to computed findings.
- CSV downloads for cleaned data, analytical summary, anomaly report, and data-quality report.

## Project structure

```text
WattWise/
├── app.py                         # Streamlit interface
├── run_wattwise.py                # VS Code-friendly application launcher
├── .vscode/launch.json            # F5 app/test/generator/validation configurations
├── data_generator.py              # Reproducible NumPy synthetic data
├── data_cleaning.py               # Validation, cleaning, quality report
├── analysis.py                    # Statistics, intervals, daily totals, savings
├── anomaly_detection.py           # IQR and high-reading flags
├── recommendations.py             # Transparent rule-based recommendations
├── visualizations.py              # Matplotlib figures
├── validate_project.py            # Reproduce results and chart assets
├── validate_app.py                # Headless Streamlit smoke test
├── sample_data.csv                # 1,440-row synthetic demonstration
├── requirements.txt
├── README.md
├── EXECUTION_GUIDE.md
├── VIVA_PREPARATION.md
├── LITERATURE_REVIEW.md
├── PRESENTATION_STATUS.md
├── .gitignore
├── tests/
│   ├── test_analysis.py
│   ├── test_anomaly_detection.py
│   ├── test_data_cleaning.py
│   └── test_data_generator.py
├── results/                       # Verified synthetic-data outputs
└── presentation_assets/           # Charts for the later official-template PPT
```

## Quick start on Windows

Open Command Prompt in the extracted `WattWise` folder:

```bat
py -3.12 -m venv .venv
.venv\Scripts\activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python data_generator.py
python -m unittest discover -s tests -v
python validate_project.py
python validate_app.py
streamlit run app.py
```

Alternatively, use the VS Code-friendly launcher:

```bat
python run_wattwise.py
```

Open the local URL printed by Streamlit, normally `http://localhost:8501`. See `EXECUTION_GUIDE.md` for PowerShell commands, VS Code F5 instructions, details, and troubleshooting.

## CSV contract

Required columns:

```csv
timestamp,electricity_kwh
2025-01-01 00:00:00,0.245
2025-01-01 01:00:00,0.231
```

- `timestamp`: parseable date/time identifying the reading interval.
- `electricity_kwh`: **energy in kWh for that interval**, not instantaneous kW power.
- Optional fields such as `appliance` or `day_type` are preserved but are never assumed to exist.
- Use one row per non-overlapping interval. Do not mix cumulative meter readings with interval-energy readings.
- WattWise does not infer or convert an unknown unit. Confirm the source unit before interpreting totals or tariffs.

## Cleaning policy

Cleaning occurs in this order, and each category is reported:

1. Validate required columns and remove later exact duplicate rows.
2. Parse timestamps and numerically convert consumption; parsing/conversion failures are not silently repaired.
3. For repeated valid timestamps, retain the first occurrence and remove later occurrences to avoid double-counting an interval. The count is reported. Review such conflicts in the source file.
4. Remove invalid timestamps.
5. Remove missing consumption rows. **Missing kWh is never replaced with zero.**
6. Remove non-numeric, negative, and non-finite consumption rows.
7. Sort retained records chronologically.

The categories are sequential and mutually exclusive. For example, a row already removed as an exact duplicate is not counted again in a later category.

## Analytical choices

### Descriptive statistics

NumPy arrays calculate the statistics. Population variance and standard deviation (`ddof=0`) describe the supplied valid readings; no inference to a larger population is made. Empty-input metrics that are undefined return `None` rather than fabricated numbers.

### Daily totals and day types

A day is marked complete only when:

- all timestamp gaps are regular;
- 24 hours is divisible by the inferred interval; and
- the day contains the expected number of readings (24 for hourly data).

Only complete days are used in the daily-total chart and weekday/weekend daily comparison. This avoids presenting partial-day sums as full-day consumption.

### IQR investigation

```text
Q1 = 25th percentile
Q3 = 75th percentile
IQR = Q3 − Q1
Upper fence = Q3 + 1.5 × IQR
Flag when electricity_kwh > upper fence
```

Invalid observations are excluded. Fewer than four valid observations produce no flags. Constant data produces no high anomalies. If IQR is zero but values are not constant, the mathematical upper fence still applies.

### Savings scenarios

```text
Estimated kWh reduction = observed kWh × reduction % ÷ 100
Estimated monetary reduction = estimated kWh reduction × user tariff (INR/kWh)
```

These are arithmetic what-if estimates. They do not include slab tariffs, fixed charges, taxes, demand charges, behavioural rebound, or verification of an actual reduction.

## Verified illustrative synthetic-data results

These values come only from the default seed-42 synthetic CSV. They are **not actual household or campus measurements**.

| Metric | Verified value |
|---|---:|
| Generated / valid rows | 1,440 / 1,440 |
| Coverage | 1 Jan 2025 00:00–1 Mar 2025 23:00 |
| Complete days | 60 |
| Observed total | 575.437 kWh |
| Mean / median per hourly reading | 0.399609 / 0.354 kWh |
| Minimum / maximum | 0.098 / 3.400 kWh |
| Population standard deviation | 0.216752 kWh |
| Q1 / Q3 / IQR | 0.285 / 0.453 / 0.168 kWh |
| Upper fence | 0.705 kWh |
| Readings above upper fence | 56 (3.8889%) |
| Average complete weekday | 9.19895 kWh across 43 days |
| Average complete weekend day | 10.58129 kWh across 17 days |

The generator deliberately inserts seven high events, but the global IQR rule flags 56 values because some ordinary high parts of the daily pattern also exceed the fence. This is a useful limitation: the output is a set of candidates for contextual review, not a labelled waste diagnosis. No accuracy, precision, recall, real-world improvement, or actual savings is claimed.

Machine-readable outputs are in `results/validation_summary.json` and the accompanying CSV files.

## Limitations and future work

- The built-in data is synthetic; external validity requires a documented real dataset.
- Global IQR does not model hour, season, weather, occupancy, or operating schedule.
- Aggregate consumption alone cannot identify a responsible appliance.
- Keeping the first duplicate timestamp is a documented cleaning rule, not proof that the first record is correct.
- Tariff input is an assumption, not a bill calculation.
- No forecasting or machine-learning superiority claim is made.
- Useful future work: real-data validation, context-aware thresholds by hour/day type, additional labelled anomalies, and a properly designed comparison against forecasting methods.

## Presentation status

The mandatory `Project_Review_II_Template.pptx` was not present in the supplied workspace. No substitute SRM theme has been created. See `PRESENTATION_STATUS.md`; the official template is still required to produce the final editable 20-slide deck.
