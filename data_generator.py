"""Create the reproducible synthetic WattWise demonstration dataset.

The generated values are NOT real household or campus measurements.
Run with: python data_generator.py
"""

from pathlib import Path
import argparse

import numpy as np
import pandas as pd


DEFAULT_SEED = 42
DEFAULT_DAYS = 60
HOURS_PER_DAY = 24


def generate_synthetic_data(seed=DEFAULT_SEED, days=DEFAULT_DAYS, start="2025-01-01"):
    """Return hourly synthetic electricity readings as a Pandas DataFrame.

    Each electricity_kwh value represents energy for one hourly interval.
    A fixed seed makes the demonstration reproducible.
    """
    if not isinstance(days, int) or days <= 0:
        raise ValueError("days must be a positive integer")
    if not isinstance(seed, int):
        raise ValueError("seed must be an integer")

    rng = np.random.default_rng(seed)
    row_count = days * HOURS_PER_DAY
    timestamps = pd.date_range(start=start, periods=row_count, freq="h")

    hours = timestamps.hour.to_numpy()
    weekdays = timestamps.day_of_week.to_numpy()

    # A simple daily shape: base load plus morning and evening peaks.
    base_load = 0.24
    morning_peak = 0.20 * np.exp(-((hours - 7) / 2.0) ** 2)
    afternoon_load = 0.08 * np.exp(-((hours - 13) / 3.0) ** 2)
    evening_peak = 0.44 * np.exp(-((hours - 19) / 2.8) ** 2)

    # Each day receives a small random scale factor; weekends are slightly higher.
    daily_factors = rng.normal(loc=1.0, scale=0.07, size=days)
    repeated_daily_factors = np.repeat(daily_factors, HOURS_PER_DAY)
    weekend_factors = np.where(weekdays >= 5, 1.10, 1.00)
    noise = rng.normal(loc=0.0, scale=0.035, size=row_count)

    expected_pattern = base_load + morning_peak + afternoon_load + evening_peak
    electricity = expected_pattern * repeated_daily_factors * weekend_factors + noise
    electricity = np.clip(electricity, 0.05, None)

    # Deliberately insert seven unusual high readings for demonstration only.
    # These are investigation examples, not labelled proof of electricity waste.
    unusual_readings = {
        (10 * HOURS_PER_DAY) + 18: 2.80,
        (17 * HOURS_PER_DAY) + 7: 2.20,
        (25 * HOURS_PER_DAY) + 20: 3.10,
        (36 * HOURS_PER_DAY) + 13: 2.60,
        (45 * HOURS_PER_DAY) + 21: 3.40,
        (52 * HOURS_PER_DAY) + 19: 2.90,
        (58 * HOURS_PER_DAY) + 8: 2.40,
    }
    for index, value in unusual_readings.items():
        if index < row_count:
            electricity[index] = value

    return pd.DataFrame(
        {
            "timestamp": timestamps.strftime("%Y-%m-%d %H:%M:%S"),
            "electricity_kwh": np.round(electricity, 3),
        }
    )


def save_sample_data(output_path="sample_data.csv", seed=DEFAULT_SEED, days=DEFAULT_DAYS):
    """Generate and save a CSV file, returning its Path."""
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    data = generate_synthetic_data(seed=seed, days=days)
    data.to_csv(output_path, index=False)
    return output_path


def main():
    parser = argparse.ArgumentParser(description="Generate synthetic WattWise data")
    parser.add_argument("--output", default=str(Path(__file__).with_name("sample_data.csv")))
    parser.add_argument("--seed", type=int, default=DEFAULT_SEED)
    parser.add_argument("--days", type=int, default=DEFAULT_DAYS)
    args = parser.parse_args()

    path = save_sample_data(args.output, seed=args.seed, days=args.days)
    print(f"Saved {args.days * HOURS_PER_DAY:,} synthetic rows to: {path}")
    print("These are simulated readings, not actual household or campus measurements.")


if __name__ == "__main__":
    main()
