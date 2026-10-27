"""WattWise — Electricity Waste Detective.

Launch locally with: streamlit run app.py
High consumption is treated as an investigation lead, never as proof of waste.
"""

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

from analysis import (
    aggregate_daily_consumption,
    calculate_descriptive_statistics,
    calculate_savings,
    compare_weekday_weekend,
    infer_interval,
)
from anomaly_detection import detect_high_anomalies
from data_cleaning import clean_electricity_data, quality_report_to_frame
from recommendations import generate_recommendations
from visualizations import (
    plot_consumption_over_time,
    plot_daily_consumption,
    plot_distribution,
    plot_high_consumption,
    plot_weekday_weekend,
)


PROJECT_DIR = Path(__file__).resolve().parent
SAMPLE_PATH = PROJECT_DIR / "sample_data.csv"


def show_figure(figure):
    st.pyplot(figure, width="stretch")
    plt.close(figure)


def format_number(value, digits=3):
    return "Not available" if value is None else f"{value:,.{digits}f}"


def load_raw_data():
    st.sidebar.header("1. Choose data")
    source = st.sidebar.radio(
        "Data source",
        ["Synthetic demonstration", "Upload a CSV file"],
        help="The demonstration is simulated and is not a real household or campus dataset.",
    )

    if source == "Synthetic demonstration":
        if not SAMPLE_PATH.exists():
            st.error("sample_data.csv is missing. Run: python data_generator.py")
            st.stop()
        return (
            pd.read_csv(SAMPLE_PATH),
            "Synthetic demonstration — seed 42, 60 days, hourly; not real measurements",
        )

    uploaded_file = st.sidebar.file_uploader("Upload electricity CSV", type=["csv"])
    if uploaded_file is None:
        st.info("Upload a CSV file or select the synthetic demonstration in the sidebar.")
        st.stop()
    try:
        return pd.read_csv(uploaded_file), f"User-uploaded CSV: {uploaded_file.name}"
    except (pd.errors.EmptyDataError, pd.errors.ParserError, UnicodeDecodeError) as error:
        st.error(f"The CSV could not be read: {error}")
        st.stop()


def main():
    st.set_page_config(page_title="WattWise", page_icon="⚡", layout="wide")
    st.title("⚡ WattWise — Electricity Waste Detective")
    st.caption("A Python-Based Data Science Project | Unusual consumption is an investigation lead, not proof of waste.")

    st.sidebar.header("2. Required CSV columns")
    st.sidebar.code("timestamp\nelectricity_kwh")
    st.sidebar.caption("Each kWh value should represent energy for the reading interval. Optional columns are retained but not required.")

    raw_data, source_label = load_raw_data()
    try:
        cleaned, quality_report = clean_electricity_data(raw_data)
    except ValueError as error:
        st.error(str(error))
        st.stop()

    statistics = calculate_descriptive_statistics(cleaned)
    interval_info = infer_interval(cleaned)
    daily = aggregate_daily_consumption(cleaned, interval_info)
    complete_daily = daily.loc[daily["is_complete"]].copy() if not daily.empty else daily
    day_type_summary = compare_weekday_weekend(daily)
    anomaly_data, anomaly_summary = detect_high_anomalies(cleaned)
    recommendations = generate_recommendations(statistics, quality_report, anomaly_summary, day_type_summary)

    st.info(f"**Data source:** {source_label}")
    if quality_report["rows_rejected"]:
        st.warning(
            f"{quality_report['rows_rejected']} row(s) were rejected. See the quality report; "
            "missing consumption was not replaced with zero."
        )

    overview_tab, charts_tab, anomaly_tab, savings_tab, download_tab = st.tabs(
        ["Overview", "Charts", "IQR investigation", "Savings & recommendations", "Downloads"]
    )

    with overview_tab:
        st.subheader("Observed consumption summary")
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Valid readings", f"{statistics['valid_observations']:,}")
        col2.metric("Observed total", f"{statistics['total_kwh']:,.3f} kWh")
        col3.metric("Mean per reading", format_number(statistics["mean_kwh"]) + " kWh")
        col4.metric("Median per reading", format_number(statistics["median_kwh"]) + " kWh")

        col5, col6, col7 = st.columns(3)
        col5.metric("Minimum", format_number(statistics["minimum_kwh"]) + " kWh")
        col6.metric("Maximum", format_number(statistics["maximum_kwh"]) + " kWh")
        col7.metric("Std. deviation", format_number(statistics["standard_deviation_kwh"]) + " kWh")

        st.write(f"**Measurement interval:** {interval_info['interpretation']}")
        if not cleaned.empty:
            st.write(
                f"**Coverage:** {cleaned['timestamp'].min()} to {cleaned['timestamp'].max()} "
                f"(timestamps supplied by the dataset)."
            )
        st.caption("Variance and standard deviation use the population formula (ddof=0) for the supplied valid readings.")

        left, right = st.columns([1, 1])
        with left:
            st.write("**Cleaned data preview**")
            st.dataframe(cleaned.head(20), width="stretch", hide_index=True)
        with right:
            st.write("**Data-quality report**")
            st.dataframe(quality_report_to_frame(quality_report), width="stretch", hide_index=True)

        st.write("**Daily aggregation check**")
        if daily.empty:
            st.info("Daily aggregation is not available without valid timestamped readings.")
        else:
            st.write(
                f"{len(complete_daily)} of {len(daily)} observed day(s) meet the complete-day rule "
                "for the inferred regular interval."
            )
            st.dataframe(daily.head(10), width="stretch", hide_index=True)

    with charts_tab:
        st.subheader("Consumption patterns")
        if cleaned.empty:
            st.warning("No charts can be generated because there are no valid readings.")
        else:
            show_figure(plot_consumption_over_time(cleaned))

            if not complete_daily.empty:
                show_figure(plot_daily_consumption(complete_daily))
            else:
                st.info(
                    "No daily-total chart is shown: regular intervals and complete expected daily "
                    "reading counts could not be verified."
                )

            if statistics["valid_observations"] >= 2 and statistics["maximum_kwh"] > statistics["minimum_kwh"]:
                show_figure(plot_distribution(cleaned))
            else:
                st.info("A distribution chart is not useful for fewer than two readings or constant values.")

            if len(day_type_summary) >= 2:
                show_figure(plot_weekday_weekend(day_type_summary))
                st.dataframe(day_type_summary, width="stretch", hide_index=True)
            else:
                st.info("Weekday/weekend comparison needs complete days from both day types.")

    with anomaly_tab:
        st.subheader("IQR upper-fence investigation")
        st.latex(r"IQR = Q3 - Q1 \qquad Upper\ fence = Q3 + 1.5 \times IQR")
        st.write(
            "Q1 is the 25th percentile and Q3 is the 75th percentile. Only readings "
            "**strictly above** the upper fence are flagged. A flagged value may be legitimate "
            "usage, a recording problem, or a change in circumstances."
        )
        st.write(f"**Method status:** {anomaly_summary['status']} — {anomaly_summary['explanation']}")

        if anomaly_summary["upper_fence_kwh"] is not None:
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Q1", f"{anomaly_summary['q1_kwh']:.3f} kWh")
            col2.metric("Q3", f"{anomaly_summary['q3_kwh']:.3f} kWh")
            col3.metric("IQR", f"{anomaly_summary['iqr_kwh']:.3f} kWh")
            col4.metric("Upper fence", f"{anomaly_summary['upper_fence_kwh']:.3f} kWh")

        if not cleaned.empty:
            show_figure(plot_high_consumption(anomaly_data, anomaly_summary))
        anomalies = anomaly_data.loc[anomaly_data["is_unusually_high"]].copy()
        st.write(f"**{len(anomalies)} statistically unusual high reading(s)**")
        st.dataframe(anomalies, width="stretch", hide_index=True)

    with savings_tab:
        st.subheader("Hypothetical savings calculator")
        st.caption("What-if estimates only. Actual savings are not guaranteed and depend on real actions and billing rules.")
        scenario = st.selectbox("Reduction scenario", ["5%", "10%", "15%", "20%", "Custom"])
        if scenario == "Custom":
            reduction = st.number_input("Custom reduction (%)", min_value=0.0, max_value=100.0, value=7.5, step=0.5)
        else:
            reduction = float(scenario.rstrip("%"))
        tariff = st.number_input("Tariff (INR per kWh)", min_value=0.0, value=8.0, step=0.5)
        savings = calculate_savings(statistics["total_kwh"], reduction, tariff)

        col1, col2, col3 = st.columns(3)
        col1.metric("Estimated energy reduction", f"{savings['estimated_kwh_savings']:,.3f} kWh")
        col2.metric("Estimated monetary reduction", f"₹{savings['estimated_monetary_savings_inr']:,.2f}")
        col3.metric("Remaining consumption", f"{savings['remaining_kwh']:,.3f} kWh")
        st.write(
            f"Calculation: {statistics['total_kwh']:.3f} kWh × {reduction:g}% ÷ 100 = "
            f"{savings['estimated_kwh_savings']:.3f} kWh; monetary estimate = kWh reduction × ₹{tariff:.2f}/kWh."
        )

        st.subheader("Transparent recommendations")
        for number, recommendation in enumerate(recommendations, start=1):
            st.write(f"**{number}.** {recommendation}")

    with download_tab:
        st.subheader("Download local CSV results")
        cleaned_download = cleaned.copy()
        if not cleaned_download.empty:
            cleaned_download["timestamp"] = cleaned_download["timestamp"].astype(str)
        st.download_button(
            "Download cleaned data",
            cleaned_download.to_csv(index=False).encode("utf-8"),
            "wattwise_cleaned_data.csv",
            "text/csv",
        )

        summary_rows = [{"metric": "data_source", "value": source_label}]
        summary_rows.extend({"metric": key, "value": value} for key, value in statistics.items())
        summary_rows.extend(
            [
                {"metric": "inferred_interval_hours", "value": interval_info["interval_hours"]},
                {"metric": "regular_intervals", "value": interval_info["is_regular"]},
                {"metric": "iqr_upper_fence_kwh", "value": anomaly_summary["upper_fence_kwh"]},
                {"metric": "unusually_high_readings", "value": anomaly_summary["anomaly_count"]},
            ]
        )
        summary_frame = pd.DataFrame(summary_rows)
        # A mixed numeric/text column is converted to text for reliable Arrow display.
        summary_frame["value"] = summary_frame["value"].map(
            lambda value: "" if value is None else str(value)
        )
        st.download_button(
            "Download analytical summary",
            summary_frame.to_csv(index=False).encode("utf-8"),
            "wattwise_analytical_summary.csv",
            "text/csv",
        )

        anomaly_download = anomaly_data.loc[anomaly_data["is_unusually_high"]].copy()
        if not anomaly_download.empty:
            anomaly_download["timestamp"] = anomaly_download["timestamp"].astype(str)
        st.download_button(
            "Download anomaly report",
            anomaly_download.to_csv(index=False).encode("utf-8"),
            "wattwise_anomaly_report.csv",
            "text/csv",
        )
        st.download_button(
            "Download data-quality report",
            quality_report_to_frame(quality_report).to_csv(index=False).encode("utf-8"),
            "wattwise_data_quality_report.csv",
            "text/csv",
        )
        st.dataframe(summary_frame, width="stretch", hide_index=True)

    st.divider()
    st.caption("WattWise uses descriptive statistics and IQR—not machine learning—and runs locally without a database or external API.")


if __name__ == "__main__":
    main()
