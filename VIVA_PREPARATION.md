# WattWise Viva Preparation

## One-minute project explanation

WattWise is a Python data science application that turns interval electricity-consumption CSV records into cleaned tables, descriptive statistics, understandable charts, and investigation leads. Pandas handles tabular cleaning and grouping, NumPy calculates numerical statistics and percentiles, Matplotlib visualizes patterns, and Streamlit supplies the local Python interface. The project uses an upper-fence IQR rule rather than a complicated AI model. It deliberately avoids saying that high consumption equals waste: unusual readings can be legitimate usage, changed circumstances, or data-quality problems. A savings calculator evaluates user-selected what-if percentages and an assumed INR tariff, without guaranteeing real savings.

## Major modules and workflow

1. **`data_generator.py`** — creates the seed-42 synthetic demonstration: 60 days × 24 hours = 1,440 rows, daily shapes, random variation, weekend variation, and seven deliberately inserted high events.
2. **`app.py`** — selects the built-in/uploaded CSV and connects all modules through five Streamlit tabs.
3. **`data_cleaning.py`** — validates columns, parses types, detects duplicates and invalid readings, sorts data, and reports every removed-row category.
4. **`analysis.py`** — calculates NumPy descriptive statistics, infers interval regularity, creates complete-day totals, compares day types, and calculates hypothetical savings.
5. **`anomaly_detection.py`** — computes Q1, Q3, IQR, and the upper fence; adds `is_unusually_high` without labelling waste.
6. **`visualizations.py`** — produces Matplotlib time, daily, distribution, anomaly, and day-type charts only when supported.
7. **`recommendations.py`** — converts actual quality, anomaly, and day-type findings into transparent rules.
8. **`tests/`** — checks calculations, invalid/duplicate/empty input, IQR behaviour, anomalies, savings, and reproducibility.

**Workflow:** CSV input → column validation → data cleaning → NumPy/Pandas analysis → IQR flagging → charts/reports → interpretation, recommendations, and scenario estimates.

## Important verified demonstration numbers

Use these only when discussing the **synthetic** seed-42 dataset:

- 1,440 valid hourly readings and 60 complete days.
- Total 575.437 kWh; mean 0.399609 kWh; median 0.354 kWh.
- Q1 = 0.285 kWh, Q3 = 0.453 kWh, IQR = 0.168 kWh.
- Upper fence = 0.453 + 1.5 × 0.168 = **0.705 kWh**.
- 56 readings are above the fence. This exceeds the seven deliberately inserted high events because some recurring high daily-pattern readings also cross a global fence.
- Average complete weekend day = 10.58129 kWh versus 9.19895 kWh on weekdays. This is an observed synthetic pattern, not evidence of waste.

## 15 likely viva questions with answers

### 1. What problem does WattWise solve?

Raw interval readings and total bills do not easily reveal temporal patterns, data-quality issues, or observations worth investigating. WattWise makes those patterns easier to inspect using repeatable cleaning, statistics, charts, and IQR flags. It supports investigation; it does not prove waste.

### 2. Why is this a Fundamentals of Data Science project rather than an AI project?

The implementation centres on CSV file handling, Pandas DataFrames, NumPy arrays, data cleaning, descriptive statistics, percentiles, grouping, visualization, and interpretation. IQR is a transparent statistical rule. There is no trained neural network, external AI service, or complicated ML framework.

### 3. What is the difference between kW and kWh here?

kW is power at a moment; kWh is energy over time. WattWise expects each row's `electricity_kwh` to be energy associated with its reading interval. For the hourly demonstration, summing valid interval-kWh values gives observed energy. Treating cumulative meter readings or unknown kW values as interval kWh would be incorrect.

### 4. How does data cleaning handle missing and invalid values?

Required columns are checked first. Timestamps and kWh are converted with errors marked as invalid. Later exact duplicates, repeated timestamps, invalid timestamps, missing/non-numeric/negative/non-finite readings are removed in a documented sequence. Counts appear in the quality report. Missing kWh is never replaced with zero because zero would invent consumption.

### 5. What is the duplicate-timestamp policy, and why is it a limitation?

After exact duplicate rows are removed, the first valid occurrence of a timestamp is retained and later occurrences are removed to prevent double-counting an interval. The report shows the count. This is deterministic but does not prove that the first conflicting record is correct, so source review is recommended.

### 6. Where are Pandas and NumPy used?

Pandas stores and cleans tabular data, parses timestamps, sorts values, and groups daily totals. NumPy converts the cleaned kWh column into numerical arrays for total, mean, median, variance, standard deviation, and percentiles. Python functions, conditions, loops, dictionaries, exceptions, and file handling connect the workflow.

### 7. Why report both mean and median?

The mean uses every value and is sensitive to high readings; the median is the middle ordered value and is more robust. In the synthetic result, mean ≈ 0.399609 kWh and median = 0.354 kWh, consistent with a right-skewed distribution containing high values. This is interpretation, not proof of waste.

### 8. Which variance and standard deviation formula is used?

The project uses population variance and standard deviation, `ddof=0`, because it describes the supplied valid dataset rather than inferring a larger population. Variance is in squared kWh units; standard deviation returns to kWh and describes spread around the mean.

### 9. Explain IQR using the verified synthetic values.

Q1 is the 25th percentile and Q3 the 75th. Here, IQR = 0.453 − 0.285 = 0.168 kWh. The upper fence is Q3 + 1.5 × IQR = 0.453 + 0.252 = 0.705 kWh. A reading is flagged only when it is strictly greater than 0.705 kWh.

### 10. How are small, constant, and invalid datasets handled?

Invalid, negative, and non-finite values are excluded. Fewer than four valid observations produce an insufficient-data status and no flags. Constant valid data produces no high anomalies. Empty input returns safe statistics and no charts. If IQR is zero but data is not constant, the mathematical fence is still used.

### 11. Why is an anomaly not automatically electricity waste?

The IQR fence only describes statistical unusualness relative to the supplied values. A flagged reading could reflect guests, weather, a special activity, a changed schedule, legitimate equipment use, or a recording error. The synthetic result itself has 56 flags despite only seven deliberately inserted events, showing why context matters.

### 12. When are daily and weekday/weekend charts shown?

Daily totals are trusted only when timestamps are regular and each day has the expected count for the inferred interval—24 for hourly data. Weekday/weekend comparisons use complete days only. Otherwise the application explains why the chart is withheld instead of presenting a misleading partial total.

### 13. How does the savings calculator work?

For observed energy `E`, reduction `r%`, and tariff `t` INR/kWh: estimated kWh reduction = `E × r / 100`; estimated monetary reduction = that kWh value × `t`. For example, 10% of 575.437 kWh is 57.5437 kWh; at an assumed ₹8/kWh, the arithmetic estimate is ₹460.35. It is hypothetical, excludes billing complexities, and is not guaranteed savings.

### 14. How was the project validated?

The reference environment ran 18 `unittest` tests covering totals/averages, invalid and duplicate records, IQR, anomalies, savings, empty input, and generator reproducibility. `validate_project.py` checked the 1,440-row sample, one-hour regularity, and 60 complete days. A headless Streamlit `AppTest` also rendered the five tabs without an exception. Browser appearance and native Windows execution are not claimed as verified.

### 15. What are the main limitations and sensible future improvements?

The demonstration is synthetic, global IQR ignores context, aggregate kWh cannot identify an appliance, and tariff estimates are simplified. Future work should first obtain documented real data, then compare context-aware thresholds by hour/day type, collect labelled contextual outcomes, and only then design a fair comparison with forecasting or machine-learning approaches.

## Terms to use carefully

- Say **“statistically unusual high reading”**, not “confirmed waste.”
- Say **“observed synthetic total”**, not “household consumption measured.”
- Say **“hypothetical reduction estimate”**, not “guaranteed savings.”
- Say **“headless Streamlit smoke test passed”**, not “all browsers and Windows were fully tested.”
- Say **“future comparison with ML”**, not “IQR is superior to ML.”
