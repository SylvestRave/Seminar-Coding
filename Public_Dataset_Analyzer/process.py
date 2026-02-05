"""process.py

Data loading and analysis functions for the Disneyland Review Analyser.
"""

from __future__ import annotations

import csv
from collections import defaultdict
from typing import Callable


def _norm(text: str) -> str:
    return (text or "").strip().lower()


def read_reviews_csv(file_path: str) -> list[dict]:
    """Read CSV into list of dicts; convert Rating to int (invalid -> 0)."""
    rows: list[dict] = []
    with open(file_path, mode="r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            rating_raw = (row.get("Rating") or "").strip()
            row["Rating"] = int(rating_raw) if rating_raw.isdigit() else 0
            rows.append(row)
    return rows


def filter_reviews_by_park(rows: list[dict], park: str) -> list[dict]:
    target = _norm(park)
    return [r for r in rows if _norm(r.get("Branch", "")) == target]


def count_reviews_by_park_and_location(rows: list[dict], park: str, location: str) -> int:
    park_n = _norm(park)
    loc_n = _norm(location)
    return sum(
        1
        for r in rows
        if _norm(r.get("Branch", "")) == park_n and _norm(r.get("Reviewer_Location", "")) == loc_n
    )


def average_rating_for_park_in_year(rows: list[dict], park: str, year: str) -> float | None:
    park_n = _norm(park)
    total = 0
    count = 0
    for r in rows:
        if _norm(r.get("Branch", "")) != park_n:
            continue
        ym = (r.get("Year_Month") or "").strip()
        if ym.startswith(year):
            total += int(r.get("Rating", 0) or 0)
            count += 1
    return (total / count) if count else None


def review_counts_by_park(rows: list[dict]) -> list[tuple[str, int]]:
    counts: dict[str, int] = defaultdict(int)
    for r in rows:
        park = (r.get("Branch") or "").strip()
        if park:
            counts[park] += 1
    return sorted(counts.items(), key=lambda x: x[1], reverse=True)


def _group_sum_count(
    rows: list[dict],
    key_fn: Callable[[dict], str],
    filter_fn: Callable[[dict], bool] | None = None,
) -> dict[str, tuple[int, int]]:
    sums: dict[str, int] = defaultdict(int)
    counts: dict[str, int] = defaultdict(int)

    for r in rows:
        if filter_fn is not None and not filter_fn(r):
            continue
        key = key_fn(r)
        if not key:
            continue
        rating = int(r.get("Rating", 0) or 0)
        sums[key] += rating
        counts[key] += 1

    return {k: (sums[k], counts[k]) for k in counts.keys()}


def top_locations_by_average_rating(rows: list[dict], park: str, top_n: int = 10) -> list[tuple[str, float]]:
    park_n = _norm(park)
    grouped = _group_sum_count(
        rows,
        key_fn=lambda r: (r.get("Reviewer_Location") or "").strip(),
        filter_fn=lambda r: _norm(r.get("Branch", "")) == park_n,
    )

    avgs: list[tuple[str, float]] = []
    for location, (total, count) in grouped.items():
        if count:
            avgs.append((location, total / count))

    avgs.sort(key=lambda x: (-x[1], x[0]))
    return avgs[:top_n]


_MONTHS = (
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December",
)


def average_monthly_rating_ignoring_year(rows: list[dict], park: str) -> dict[str, float]:
    park_n = _norm(park)
    totals = [0] * 12
    counts = [0] * 12

    for r in rows:
        if _norm(r.get("Branch", "")) != park_n:
            continue
        ym = (r.get("Year_Month") or "").strip()
        parts = ym.split("-")
        if len(parts) != 2:
            continue
        try:
            month_idx = int(parts[1]) - 1
        except ValueError:
            continue
        if not (0 <= month_idx <= 11):
            continue

        totals[month_idx] += int(r.get("Rating", 0) or 0)
        counts[month_idx] += 1

    out: dict[str, float] = {}
    for idx, name in enumerate(_MONTHS):
        if counts[idx] > 0:
            out[name] = totals[idx] / counts[idx]
    return out


def average_rating_by_location_for_each_park(rows: list[dict]) -> dict[str, list[tuple[str, float]]]:
    sums: dict[str, dict[str, int]] = defaultdict(lambda: defaultdict(int))
    counts: dict[str, dict[str, int]] = defaultdict(lambda: defaultdict(int))

    for r in rows:
        park = (r.get("Branch") or "").strip()
        loc = (r.get("Reviewer_Location") or "").strip()
        if not park or not loc:
            continue
        rating = int(r.get("Rating", 0) or 0)
        sums[park][loc] += rating
        counts[park][loc] += 1

    report: dict[str, list[tuple[str, float]]] = {}
    for park in sums.keys():
        rows_out: list[tuple[str, float]] = []
        for loc in sums[park].keys():
            c = counts[park][loc]
            if c:
                rows_out.append((loc, sums[park][loc] / c))
        rows_out.sort(key=lambda x: (-x[1], x[0]))
        report[park] = rows_out

    return report
