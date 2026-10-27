"""Rule-based, explainable recommendations grounded in computed findings."""


def generate_recommendations(statistics, quality_report, anomaly_summary, day_type_summary=None):
    """Return a list of recommendations; each rule uses actual supplied results."""
    recommendations = []
    valid_rows = statistics.get("valid_observations", 0)
    rejected_rows = quality_report.get("rows_rejected", 0)
    anomaly_count = anomaly_summary.get("anomaly_count", 0)

    if valid_rows == 0:
        return [
            "No valid readings are available. Correct the timestamp and electricity_kwh "
            "columns using the data-quality report, then analyse the file again."
        ]

    if rejected_rows > 0:
        recommendations.append(
            f"Review the {rejected_rows} rejected row(s) before drawing conclusions; "
            "missing consumption was not replaced with zero."
        )

    status = anomaly_summary.get("status")
    if status == "insufficient_data":
        recommendations.append(
            "Collect more valid readings before using IQR flagging; the current dataset is too small."
        )
    elif status == "constant_values":
        recommendations.append(
            "All valid readings are constant. Check whether this is expected for the monitored interval."
        )
    elif anomaly_count > 0:
        threshold = anomaly_summary.get("upper_fence_kwh")
        recommendations.append(
            f"Investigate the {anomaly_count} reading(s) above {threshold:.3f} kWh. Check occupancy, "
            "weather, schedules, and recording quality before deciding whether any action is needed."
        )
    else:
        recommendations.append(
            "No readings exceed the IQR upper fence. This does not prove that no inefficiency exists."
        )

    if day_type_summary is not None and not day_type_summary.empty:
        indexed = day_type_summary.set_index("day_type")
        if {"Weekday", "Weekend"}.issubset(indexed.index):
            weekday = indexed.loc["Weekday"]
            weekend = indexed.loc["Weekend"]
            if weekday["days"] >= 2 and weekend["days"] >= 2 and weekday["average_daily_kwh"] > 0:
                difference = (
                    (weekend["average_daily_kwh"] - weekday["average_daily_kwh"])
                    / weekday["average_daily_kwh"]
                    * 100.0
                )
                if abs(difference) >= 10:
                    direction = "higher" if difference > 0 else "lower"
                    recommendations.append(
                        f"Complete weekend days average {abs(difference):.1f}% {direction} consumption "
                        "than complete weekdays. Compare these periods with occupancy and operating schedules."
                    )

    recommendations.extend(
        [
            "Confirm the kWh unit, timestamp meaning, and reading interval before comparing files or periods.",
            "Use the savings calculator only for what-if scenarios; actual savings depend on behaviour, "
            "equipment, measurement coverage, and the applicable tariff.",
        ]
    )
    return recommendations
