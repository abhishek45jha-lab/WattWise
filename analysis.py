"""Beginner-friendly descriptive analysis and savings calculations."""

import math

import numpy as np
import pandas as pd


def _check_analysis_columns(data):
    if not isinstance(data, pd.DataFrame):
        raise ValueError("Input must be a Pandas DataFrame")
    missing = [c for c in ["timestamp", "electricity_kwh"] if c not in data.columns]
    if missing:
        raise ValueError("Missing required column(s): " + ", ".join(missing))


def calculate_descriptive_statistics(data):
    """Calculate population descriptive statistics for valid kWh observations.

    Population variance/std (ddof=0) are used because the supplied valid rows
    are the complete dataset being described, not a sample from which we infer
    a population. Empty-data results use None where a metric is undefined.
    """
    _check_analysis_columns(data)
    values = pd.to_numeric(data["electricity_kwh"], errors="coerce").to_numpy(dtype=float)
    values = values[np.isfinite(values)]

    if len(values) == 0:
        return {
            "total_kwh": 0.0,
            "mean_kwh": None,
            "median_kwh": None,
            "minimum_kwh": None,
            "maximum_kwh": None,
            "variance_kwh2": None,
            "standard_deviation_kwh": None,
            "valid_observations": 0,
        }

    return {
        "total_kwh": float(np.sum(values)),
        "mean_kwh": float(np.mean(values)),
        "median_kwh": float(np.median(values)),
        "minimum_kwh": float(np.min(values)),
        "maximum_kwh": float(np.max(values)),
        "variance_kwh2": float(np.var(values, ddof=0)),
        "standard_deviation_kwh": float(np.std(values, ddof=0)),
        "valid_observations": int(len(values)),
    }


def infer_interval(data):
    """Infer the median reading interval and check whether gaps are regular."""
    _check_analysis_columns(data)
    if len(data) < 2:
        return {
            "interval_hours": None,
            "is_regular": False,
            "gap_count": 0,
            "interpretation": "At least two valid timestamps are needed to infer an interval.",
        }

    timestamps = pd.to_datetime(data["timestamp"], errors="coerce").sort_values()
    gaps = timestamps.diff().dropna().dt.total_seconds() / 3600.0
    gaps = gaps.to_numpy(dtype=float)
    positive_gaps = gaps[np.isfinite(gaps) & (gaps > 0)]

    if len(positive_gaps) != len(gaps) or len(gaps) == 0:
        return {
            "interval_hours": None,
            "is_regular": False,
            "gap_count": int(len(gaps)),
            "interpretation": "Timestamps contain missing, duplicate, or non-positive gaps.",
        }

    median_gap = float(np.median(gaps))
    regular = bool(np.allclose(gaps, median_gap, rtol=1e-7, atol=1e-9))
    return {
        "interval_hours": median_gap,
        "is_regular": regular,
        "gap_count": int(len(gaps)),
        "interpretation": (
            f"Median interval: {median_gap:g} hours; all intervals are regular."
            if regular
            else f"Median interval: {median_gap:g} hours; intervals are irregular."
        ),
    }


def aggregate_daily_consumption(data, interval_info=None):
    """Return observed daily totals plus completeness flags.

    A daily total is marked complete only when timestamps are regular, 24 hours
    is divisible by the inferred interval, and the day has the expected count.
    Charts should use complete days to avoid presenting partial totals as full days.
    """
    _check_analysis_columns(data)
    columns = [
        "date",
        "electricity_kwh",
        "reading_count",
        "expected_readings",
        "is_complete",
    ]
    if data.empty:
        return pd.DataFrame(columns=columns)

    if interval_info is None:
        interval_info = infer_interval(data)

    working = data.copy()
    working["timestamp"] = pd.to_datetime(working["timestamp"], errors="coerce")
    working = working.dropna(subset=["timestamp", "electricity_kwh"])
    if working.empty:
        return pd.DataFrame(columns=columns)

    working["date"] = working["timestamp"].dt.floor("D")
    daily = (
        working.groupby("date", as_index=False)
        .agg(electricity_kwh=("electricity_kwh", "sum"), reading_count=("electricity_kwh", "size"))
        .sort_values("date")
        .reset_index(drop=True)
    )

    interval_hours = interval_info.get("interval_hours")
    expected_readings = np.nan
    aggregation_supported = False
    if interval_info.get("is_regular") and interval_hours and interval_hours > 0:
        raw_expected = 24.0 / interval_hours
        if raw_expected >= 1 and math.isclose(raw_expected, round(raw_expected), abs_tol=1e-9):
            expected_readings = int(round(raw_expected))
            aggregation_supported = True

    daily["expected_readings"] = expected_readings
    if aggregation_supported:
        daily["is_complete"] = daily["reading_count"].eq(expected_readings)
    else:
        daily["is_complete"] = False
    return daily[columns]


def compare_weekday_weekend(daily_data):
    """Compare complete daily totals for weekdays and weekends."""
    columns = ["day_type", "days", "average_daily_kwh", "median_daily_kwh", "total_kwh"]
    if daily_data.empty or "is_complete" not in daily_data.columns:
        return pd.DataFrame(columns=columns)

    complete = daily_data.loc[daily_data["is_complete"]].copy()
    if complete.empty:
        return pd.DataFrame(columns=columns)

    complete["date"] = pd.to_datetime(complete["date"])
    complete["day_type"] = np.where(complete["date"].dt.day_of_week < 5, "Weekday", "Weekend")
    summary = (
        complete.groupby("day_type", as_index=False)
        .agg(
            days=("date", "size"),
            average_daily_kwh=("electricity_kwh", "mean"),
            median_daily_kwh=("electricity_kwh", "median"),
            total_kwh=("electricity_kwh", "sum"),
        )
        .sort_values("day_type")
        .reset_index(drop=True)
    )
    return summary[columns]


def calculate_savings(observed_kwh, reduction_percent, tariff_inr_per_kwh):
    """Calculate a hypothetical reduction scenario; no savings are guaranteed."""
    try:
        observed_kwh = float(observed_kwh)
        reduction_percent = float(reduction_percent)
        tariff_inr_per_kwh = float(tariff_inr_per_kwh)
    except (TypeError, ValueError) as error:
        raise ValueError("Savings inputs must be numeric") from error

    inputs = [observed_kwh, reduction_percent, tariff_inr_per_kwh]
    if not all(math.isfinite(value) for value in inputs):
        raise ValueError("Savings inputs must be finite")
    if observed_kwh < 0:
        raise ValueError("Observed consumption cannot be negative")
    if not 0 <= reduction_percent <= 100:
        raise ValueError("Reduction percentage must be between 0 and 100")
    if tariff_inr_per_kwh < 0:
        raise ValueError("Tariff cannot be negative")

    saved_kwh = observed_kwh * reduction_percent / 100.0
    return {
        "observed_kwh": observed_kwh,
        "reduction_percent": reduction_percent,
        "estimated_kwh_savings": saved_kwh,
        "remaining_kwh": observed_kwh - saved_kwh,
        "tariff_inr_per_kwh": tariff_inr_per_kwh,
        "estimated_monetary_savings_inr": saved_kwh * tariff_inr_per_kwh,
    }
