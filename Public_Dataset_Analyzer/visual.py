"""visual.py

Matplotlib visualisations for the Disneyland Review Analyser.
"""

from __future__ import annotations

import matplotlib.pyplot as plt


def pie_review_counts(labels: list[str], counts: list[int]) -> None:
    if not labels or not counts or sum(counts) == 0:
        print("No data to plot.")
        return

    fig, ax = plt.subplots(figsize=(6, 6))
    ax.pie(counts, labels=labels, autopct="%1.1f%%", startangle=90)
    ax.set_title("Number of Reviews per Park")
    ax.axis("equal")
    plt.tight_layout()
    plt.show()


def _bar_chart(
    x_labels: list[str],
    y_values: list[float],
    title: str,
    x_axis: str,
    y_axis: str,
    value_format: str = "{:.2f}",
) -> None:
    if not x_labels or not y_values or len(x_labels) != len(y_values):
        print("Invalid data for bar chart.")
        return

    fig, ax = plt.subplots(figsize=(9, 5))
    bars = ax.bar(x_labels, y_values)

    ax.set_title(title)
    ax.set_xlabel(x_axis)
    ax.set_ylabel(y_axis)

    plt.xticks(rotation=45, ha="right")
    ax.grid(axis="y", linestyle="--", alpha=0.5)

    for bar in bars:
        height = bar.get_height()
        ax.annotate(
            value_format.format(height),
            xy=(bar.get_x() + bar.get_width() / 2, height),
            xytext=(0, 3),
            textcoords="offset points",
            ha="center",
            va="bottom",
            fontsize=8,
        )

    plt.tight_layout()
    plt.show()


def bar_top_locations(park: str, locations: list[str], avgs: list[float]) -> None:
    _bar_chart(
        locations,
        avgs,
        title=f"Top 10 Locations by Avg Rating for {park}",
        x_axis="Reviewer Location",
        y_axis="Average Rating (out of 5)",
    )


def bar_monthly_average(park: str, months: list[str], avgs: list[float]) -> None:
    _bar_chart(
        months,
        avgs,
        title=f"Average Rating per Month for {park}",
        x_axis="Month",
        y_axis="Average Rating (out of 5)",
    )
