"""oop_exporter.py

OOP exporter (A-grade extension).

Aggregates per park:
- Number of reviews
- Number of positive reviews (rating >= 4)
- Average review score
- Number of unique reviewer countries/locations
"""

from __future__ import annotations

import csv
import json
from collections import defaultdict
from dataclasses import dataclass


def _ensure_ext(filename: str, ext: str) -> str:
    filename = (filename or "").strip()
    if not filename:
        filename = "report"
    if not filename.lower().endswith(ext):
        filename += ext
    return filename


def _safe_int(value, default: int = 0) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


@dataclass(frozen=True)
class ParkSummary:
    park: str
    reviews: int
    positive_reviews: int
    average_score: float
    unique_countries: int


class ParkAnalyzer:
    def __init__(self, rows: list[dict]):
        self._rows = rows or []
        self._summaries: list[ParkSummary] = self._build_summaries()

    def _build_summaries(self) -> list[ParkSummary]:
        totals = defaultdict(int)
        positive = defaultdict(int)
        rating_sum = defaultdict(int)
        countries = defaultdict(set)

        for r in self._rows:
            park = (r.get("Branch") or "").strip()
            if not park:
                continue

            rating = _safe_int(r.get("Rating"), default=0)
            loc = (r.get("Reviewer_Location") or "").strip()

            totals[park] += 1
            rating_sum[park] += rating
            if rating >= 4:
                positive[park] += 1
            if loc:
                countries[park].add(loc)

        summaries: list[ParkSummary] = []
        for park in sorted(totals.keys()):
            n = totals[park]
            avg = (rating_sum[park] / n) if n else 0.0
            summaries.append(
                ParkSummary(
                    park=park,
                    reviews=n,
                    positive_reviews=positive[park],
                    average_score=round(avg, 2),
                    unique_countries=len(countries[park]),
                )
            )
        return summaries

    def get_aggregated_data(self) -> list[dict]:
        return [
            {
                "ParkName": s.park,
                "NumberOfReviews": s.reviews,
                "NumberOfPositiveReviews": s.positive_reviews,
                "AverageReviewScore": s.average_score,
                "NumberOfUniqueCountries": s.unique_countries,
            }
            for s in self._summaries
        ]

    def export_txt(self, filename: str) -> tuple[bool, str]:
        path = _ensure_ext(filename, ".txt")
        try:
            with open(path, "w", encoding="utf-8") as f:
                f.write("Disneyland Park Aggregated Report\n")
                f.write("=" * 34 + "\n\n")

                if not self._summaries:
                    f.write("No data to report.\n")
                    return True, path

                for s in self._summaries:
                    f.write(f"ParkName: {s.park}\n")
                    f.write(f"NumberOfReviews: {s.reviews}\n")
                    f.write(f"NumberOfPositiveReviews: {s.positive_reviews}\n")
                    f.write(f"AverageReviewScore: {s.average_score}\n")
                    f.write(f"NumberOfUniqueCountries: {s.unique_countries}\n")
                    f.write("-" * 30 + "\n")

            return True, path
        except OSError:
            return False, path

    def export_csv(self, filename: str) -> tuple[bool, str]:
        path = _ensure_ext(filename, ".csv")
        try:
            with open(path, "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(
                    f,
                    fieldnames=[
                        "ParkName",
                        "NumberOfReviews",
                        "NumberOfPositiveReviews",
                        "AverageReviewScore",
                        "NumberOfUniqueCountries",
                    ],
                )
                writer.writeheader()
                writer.writerows(self.get_aggregated_data())
            return True, path
        except OSError:
            return False, path

    def export_json(self, filename: str) -> tuple[bool, str]:
        path = _ensure_ext(filename, ".json")
        try:
            with open(path, "w", encoding="utf-8") as f:
                json.dump(self.get_aggregated_data(), f, indent=2)
            return True, path
        except OSError:
            return False, path
