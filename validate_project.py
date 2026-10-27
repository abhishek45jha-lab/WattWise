"""Reproduce and export illustrative synthetic-data results and chart assets.

Run after data_generator.py: python validate_project.py
This script performs analysis validation; unit tests are run separately.
"""

import json
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

from analysis import (
    aggregate_daily_consumption,
    calculate_descriptive_statistics,
    calculate_savings,
    compare_weekday_weekend,
    infer_interval,
)
from anomaly_detection import detect_high_anomalies
from data_cleaning import clean_electricity_data, quality_report_to_frame
from visualizations import (
    plot_consumption_over_time,
    plot_daily_consumption,
    plot_distribution,
    plot_high_consumption,
    plot_weekday_weekend,
)


PROJECT_DIR = Path(__file__).resolve().parent
RESULTS_DIR = PROJECT_DIR / "results"
ASSETS_DIR = PROJECT_DIR / "presentation_assets"


def save_chart(figure, filename):
    figure.text(
        0.99,
        0.005,
        "Illustrative synthetic-data result • not real household/campus measurements",
        ha="right",
        va="bottom",
        fontsize=7,
        color="#546E7A",
    )
    figure.savefig(ASSETS_DIR / filename, dpi=170, bbox_inches="tight")
    plt.close(figure)


def main():
    RESULTS_DIR.mkdir(exist_ok=True)
    ASSETS_DIR.mkdir(exist_ok=True)
    sample_path = PROJECT_DIR / "sample_data.csv"
    if not sample_path.exists():
        raise FileNotFoundError("Run python data_generator.py first")

    raw = pd.read_csv(sample_path)
    cleaned, quality = clean_electricity_data(raw)
    statistics = calculate_descriptive_statistics(cleaned)
    interval = infer_interval(cleaned)
    daily = aggregate_daily_consumption(cleaned, interval)
    complete_daily = daily.loc[daily["is_complete"]].copy()
    day_types = compare_weekday_weekend(daily)
    anomaly_data, anomaly_summary = detect_high_anomalies(cleaned)

    # These checks apply to the required default demonstration, not arbitrary uploads.
    assert len(raw) == 1440, "Default synthetic sample must contain 1,440 rows"
    assert quality["valid_rows"] == 1440, "Default generated sample should be fully valid"
    assert interval["is_regular"] and interval["interval_hours"] == 1.0
    assert len(complete_daily) == 60, "Default sample should contain 60 complete days"

    pd.DataFrame([statistics]).to_csv(RESULTS_DIR / "descriptive_statistics.csv", index=False)
    quality_report_to_frame(quality).to_csv(RESULTS_DIR / "data_quality_report.csv", index=False)
    daily.to_csv(RESULTS_DIR / "daily_consumption.csv", index=False)
    day_types.to_csv(RESULTS_DIR / "weekday_weekend_summary.csv", index=False)
    anomalies = anomaly_data.loc[anomaly_data["is_unusually_high"]].copy()
    anomalies.to_csv(RESULTS_DIR / "anomaly_report.csv", index=False)

    savings_rows = []
    assumed_tariff = 8.0
    for reduction in [5, 10, 15, 20]:
        scenario = calculate_savings(statistics["total_kwh"], reduction, assumed_tariff)
        scenario["assumption"] = "Hypothetical only; tariff is user-assumed, not a verified bill rate"
        savings_rows.append(scenario)
    pd.DataFrame(savings_rows).to_csv(RESULTS_DIR / "hypothetical_savings_scenarios.csv", index=False)

    validation = {
        "project": "WattWise — Electricity Waste Detective",
        "dataset_source": "Reproducible NumPy synthetic demonstration; not real measurements",
        "random_seed": 42,
        "generated_rows": len(raw),
        "valid_rows": quality["valid_rows"],
        "rejected_rows": quality["rows_rejected"],
        "start_timestamp": str(cleaned["timestamp"].min()),
        "end_timestamp": str(cleaned["timestamp"].max()),
        "statistics": statistics,
        "interval": interval,
        "observed_days": len(daily),
        "complete_days": len(complete_daily),
        "iqr": anomaly_summary,
        "weekday_weekend": day_types.to_dict(orient="records"),
        "savings_assumption": {
            "tariff_inr_per_kwh": assumed_tariff,
            "note": "Hypothetical scenarios only; no actual savings are claimed",
        },
    }
    with open(RESULTS_DIR / "validation_summary.json", "w", encoding="utf-8") as file:
        json.dump(validation, file, indent=2, ensure_ascii=False)

    save_chart(plot_consumption_over_time(cleaned), "consumption_over_time.png")
    save_chart(plot_daily_consumption(complete_daily), "daily_consumption.png")
    save_chart(plot_distribution(cleaned), "reading_distribution.png")
    save_chart(plot_high_consumption(anomaly_data, anomaly_summary), "iqr_anomalies.png")
    save_chart(plot_weekday_weekend(day_types), "weekday_weekend.png")

    print("WattWise synthetic-data validation completed.")
    print(f"Rows: {len(raw):,}; valid: {quality['valid_rows']:,}; complete days: {len(complete_daily)}")
    print(f"Observed total: {statistics['total_kwh']:.3f} kWh")
    print(f"Mean per hourly reading: {statistics['mean_kwh']:.3f} kWh")
    print(f"IQR upper fence: {anomaly_summary['upper_fence_kwh']:.3f} kWh")
    print(f"Readings above upper fence: {anomaly_summary['anomaly_count']}")
    print("Results are illustrative synthetic-data findings, not real-world savings or waste measurements.")


if __name__ == "__main__":
    main()
