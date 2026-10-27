"""Matplotlib charts used by the Streamlit application."""

import matplotlib

matplotlib.use("Agg")

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def _format_time_axis(axis):
    locator = mdates.AutoDateLocator()
    axis.xaxis.set_major_locator(locator)
    axis.xaxis.set_major_formatter(mdates.ConciseDateFormatter(locator))


def plot_consumption_over_time(data):
    fig, axis = plt.subplots(figsize=(10, 3.8))
    timestamps = pd.to_datetime(data["timestamp"])
    values = data["electricity_kwh"]
    if len(data) == 1:
        axis.scatter(timestamps, values, color="#1565C0", s=45)
    else:
        axis.plot(timestamps, values, color="#1565C0", linewidth=0.9)
    axis.set_title("Electricity consumption over time")
    axis.set_xlabel("Timestamp")
    axis.set_ylabel("Energy per reading (kWh)")
    axis.grid(alpha=0.2)
    _format_time_axis(axis)
    fig.tight_layout()
    return fig


def plot_daily_consumption(complete_daily_data):
    fig, axis = plt.subplots(figsize=(10, 3.8))
    dates = pd.to_datetime(complete_daily_data["date"])
    axis.plot(dates, complete_daily_data["electricity_kwh"], color="#00897B", marker="o", markersize=2.5)
    axis.set_title("Daily consumption — complete days only")
    axis.set_xlabel("Date")
    axis.set_ylabel("Daily energy (kWh)")
    axis.set_ylim(bottom=0)
    axis.grid(alpha=0.2)
    _format_time_axis(axis)
    fig.tight_layout()
    return fig


def plot_distribution(data):
    values = pd.to_numeric(data["electricity_kwh"], errors="coerce").dropna().to_numpy()
    bins = min(30, max(5, int(np.sqrt(len(values)))))
    fig, axis = plt.subplots(figsize=(8, 3.8))
    axis.hist(values, bins=bins, color="#5E35B1", edgecolor="white", alpha=0.85)
    axis.axvline(np.mean(values), color="#E53935", linestyle="--", label="Mean")
    axis.axvline(np.median(values), color="#FB8C00", linestyle=":", label="Median")
    axis.set_title("Distribution of valid readings")
    axis.set_xlabel("Energy per reading (kWh)")
    axis.set_ylabel("Number of readings")
    axis.legend()
    axis.grid(axis="y", alpha=0.2)
    fig.tight_layout()
    return fig


def plot_high_consumption(annotated_data, anomaly_summary):
    fig, axis = plt.subplots(figsize=(10, 4.0))
    timestamps = pd.to_datetime(annotated_data["timestamp"])
    values = annotated_data["electricity_kwh"]
    axis.plot(timestamps, values, color="#90A4AE", linewidth=0.8, label="Valid readings")

    unusual = annotated_data["is_unusually_high"]
    if unusual.any():
        axis.scatter(
            timestamps[unusual],
            values[unusual],
            color="#D32F2F",
            s=42,
            zorder=3,
            label="Above upper fence",
        )
    threshold = anomaly_summary.get("upper_fence_kwh")
    if threshold is not None:
        axis.axhline(threshold, color="#F57C00", linestyle="--", label=f"Upper fence: {threshold:.3f} kWh")
    axis.set_title("High-consumption observations — investigation leads, not proof of waste")
    axis.set_xlabel("Timestamp")
    axis.set_ylabel("Energy per reading (kWh)")
    axis.legend()
    axis.grid(alpha=0.2)
    _format_time_axis(axis)
    fig.tight_layout()
    return fig


def plot_weekday_weekend(day_type_summary):
    fig, axis = plt.subplots(figsize=(6.5, 3.8))
    colors = ["#1565C0" if day == "Weekday" else "#00897B" for day in day_type_summary["day_type"]]
    bars = axis.bar(day_type_summary["day_type"], day_type_summary["average_daily_kwh"], color=colors)
    axis.bar_label(bars, fmt="%.2f", padding=3)
    axis.set_title("Average consumption per complete day")
    axis.set_xlabel("Day type")
    axis.set_ylabel("Average daily energy (kWh)")
    maximum = float(day_type_summary["average_daily_kwh"].max())
    if maximum > 0:
        axis.set_ylim(0, maximum * 1.18)
    axis.grid(axis="y", alpha=0.2)
    fig.tight_layout()
    return fig
