"""Transparent upper-fence IQR anomaly detection for WattWise."""

import numpy as np
import pandas as pd


MINIMUM_OBSERVATIONS = 4


def calculate_iqr(values, minimum_observations=MINIMUM_OBSERVATIONS):
    """Return Q1, Q3, IQR and upper fence for valid numeric observations.

    NaN, infinite, non-numeric, and negative values are excluded. At least four
    valid observations are required before the upper fence is used for flagging.
    """
    if isinstance(values, pd.DataFrame):
        if "electricity_kwh" not in values.columns:
            raise ValueError("DataFrame input must contain electricity_kwh")
        values = values["electricity_kwh"]

    series = pd.Series(values)
    numeric = pd.to_numeric(series, errors="coerce").to_numpy(dtype=float)
    valid = numeric[np.isfinite(numeric) & (numeric >= 0)]
    invalid_excluded = int(len(numeric) - len(valid))

    summary = {
        "q1_kwh": None,
        "q3_kwh": None,
        "iqr_kwh": None,
        "upper_fence_kwh": None,
        "valid_observations": int(len(valid)),
        "invalid_observations_excluded": invalid_excluded,
        "status": "no_valid_data",
        "explanation": "No valid non-negative numeric observations are available.",
    }
    if len(valid) == 0:
        return summary

    q1 = float(np.percentile(valid, 25))
    q3 = float(np.percentile(valid, 75))
    iqr = q3 - q1
    summary.update({"q1_kwh": q1, "q3_kwh": q3, "iqr_kwh": iqr})

    if len(valid) < minimum_observations:
        summary["status"] = "insufficient_data"
        summary["explanation"] = (
            f"At least {minimum_observations} valid observations are required; "
            f"only {len(valid)} were supplied. No readings are flagged."
        )
        return summary

    upper_fence = q3 + 1.5 * iqr
    summary["upper_fence_kwh"] = float(upper_fence)
    if np.allclose(valid, valid[0]):
        summary["status"] = "constant_values"
        summary["explanation"] = "All valid readings are constant, so no high anomalies are flagged."
    else:
        summary["status"] = "ok"
        summary["explanation"] = (
            "Readings strictly above Q3 + 1.5 × IQR are flagged as statistically unusual."
        )
    return summary


def detect_high_anomalies(data, minimum_observations=MINIMUM_OBSERVATIONS):
    """Return (annotated_data, summary) using the upper IQR fence only."""
    if not isinstance(data, pd.DataFrame) or "electricity_kwh" not in data.columns:
        raise ValueError("Input must be a DataFrame containing electricity_kwh")

    result = data.copy()
    summary = calculate_iqr(result["electricity_kwh"], minimum_observations)
    result["upper_fence_kwh"] = np.nan
    result["is_unusually_high"] = False

    if summary["status"] == "ok":
        threshold = summary["upper_fence_kwh"]
        result["upper_fence_kwh"] = threshold
        numeric = pd.to_numeric(result["electricity_kwh"], errors="coerce")
        result["is_unusually_high"] = (numeric > threshold).fillna(False)

    anomaly_count = int(result["is_unusually_high"].sum())
    summary["anomaly_count"] = anomaly_count
    summary["anomaly_percentage"] = (
        float(anomaly_count / len(result) * 100.0) if len(result) else 0.0
    )
    return result, summary
