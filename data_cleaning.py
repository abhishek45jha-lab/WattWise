"""CSV validation and transparent cleaning for WattWise."""

import numpy as np
import pandas as pd


REQUIRED_COLUMNS = ["timestamp", "electricity_kwh"]


def validate_columns(data):
    """Raise a helpful error when input is not a suitable DataFrame."""
    if not isinstance(data, pd.DataFrame):
        raise ValueError("Input must be a Pandas DataFrame")

    stripped_columns = [str(column).strip() for column in data.columns]
    if len(stripped_columns) != len(set(stripped_columns)):
        raise ValueError("Column names must be unique after removing surrounding spaces")

    missing = [column for column in REQUIRED_COLUMNS if column not in stripped_columns]
    if missing:
        raise ValueError("Missing required column(s): " + ", ".join(missing))


def _parse_datetimes(series):
    """Parse common datetime formats and turn failures into NaT."""
    if series.empty:
        return pd.to_datetime(series, errors="coerce")
    try:
        return pd.to_datetime(series, format="mixed", errors="coerce")
    except (TypeError, ValueError):
        # Older Pandas versions may not support format='mixed'.
        return pd.to_datetime(series, errors="coerce")


def clean_electricity_data(raw_data):
    """Return (cleaned_data, quality_report).

    Cleaning order:
    1. Validate columns and remove exact duplicate rows.
    2. Parse timestamps and remove later rows with an already-seen timestamp.
    3. Remove invalid timestamps, missing/non-numeric/negative/non-finite kWh.
    4. Sort valid records chronologically.

    Missing consumption is NEVER replaced with zero. Every removed-row category
    is counted in the report. Categories are sequential and mutually exclusive.
    """
    validate_columns(raw_data)
    data = raw_data.copy()
    data.columns = [str(column).strip() for column in data.columns]
    original_columns = list(data.columns)

    report = {
        "input_rows": int(len(data)),
        "exact_duplicate_rows_removed": 0,
        "duplicate_timestamp_rows_removed": 0,
        "invalid_timestamp_rows_removed": 0,
        "missing_consumption_rows_removed": 0,
        "non_numeric_consumption_rows_removed": 0,
        "negative_reading_rows_removed": 0,
        "non_finite_reading_rows_removed": 0,
        "valid_rows": 0,
        "rows_rejected": 0,
    }

    # Exact duplicates are identified before type conversion.
    exact_duplicates = data.duplicated(keep="first")
    report["exact_duplicate_rows_removed"] = int(exact_duplicates.sum())
    data = data.loc[~exact_duplicates].copy()

    data["_parsed_timestamp"] = _parse_datetimes(data["timestamp"])
    data["_numeric_kwh"] = pd.to_numeric(data["electricity_kwh"], errors="coerce")

    # A timestamp should identify one interval. Keep the first occurrence and
    # report later occurrences rather than adding the same interval twice.
    duplicate_timestamps = data["_parsed_timestamp"].notna() & data.duplicated(
        subset=["_parsed_timestamp"], keep="first"
    )
    report["duplicate_timestamp_rows_removed"] = int(duplicate_timestamps.sum())
    data = data.loc[~duplicate_timestamps].copy()

    invalid_timestamps = data["_parsed_timestamp"].isna()
    report["invalid_timestamp_rows_removed"] = int(invalid_timestamps.sum())
    data = data.loc[~invalid_timestamps].copy()

    raw_consumption = data["electricity_kwh"]
    missing_consumption = raw_consumption.isna() | raw_consumption.astype(str).str.strip().eq("")
    report["missing_consumption_rows_removed"] = int(missing_consumption.sum())
    data = data.loc[~missing_consumption].copy()

    non_numeric = data["_numeric_kwh"].isna()
    report["non_numeric_consumption_rows_removed"] = int(non_numeric.sum())
    data = data.loc[~non_numeric].copy()

    negative = data["_numeric_kwh"] < 0
    report["negative_reading_rows_removed"] = int(negative.sum())
    data = data.loc[~negative].copy()

    numeric_values = data["_numeric_kwh"].astype(float)
    non_finite = ~np.isfinite(numeric_values)
    report["non_finite_reading_rows_removed"] = int(non_finite.sum())
    data = data.loc[~non_finite].copy()

    cleaned = data[original_columns].copy()
    cleaned["timestamp"] = data["_parsed_timestamp"]
    cleaned["electricity_kwh"] = data["_numeric_kwh"].astype(float)
    cleaned = cleaned.sort_values("timestamp").reset_index(drop=True)

    report["valid_rows"] = int(len(cleaned))
    report["rows_rejected"] = int(report["input_rows"] - report["valid_rows"])
    return cleaned, report


def quality_report_to_frame(report):
    """Convert a quality-report dictionary into a two-column DataFrame."""
    labels = {
        "input_rows": "Input rows",
        "exact_duplicate_rows_removed": "Exact duplicate rows removed",
        "duplicate_timestamp_rows_removed": "Later duplicate timestamps removed",
        "invalid_timestamp_rows_removed": "Invalid timestamps removed",
        "missing_consumption_rows_removed": "Missing consumption rows removed",
        "non_numeric_consumption_rows_removed": "Non-numeric consumption rows removed",
        "negative_reading_rows_removed": "Negative readings removed",
        "non_finite_reading_rows_removed": "Infinite readings removed",
        "valid_rows": "Valid rows retained",
        "rows_rejected": "Total rows rejected",
    }
    return pd.DataFrame(
        [{"check": labels.get(key, key), "count": value} for key, value in report.items()]
    )
