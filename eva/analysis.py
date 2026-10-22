from dataclasses import dataclass
from typing import List, Optional

from eva.records import EvaRecord


@dataclass(frozen=True)
class CountrySummary:
    count: int
    total_hours: float
    average_hours: Optional[float]


def categorise_eva_by_length(records: List[EvaRecord]):
    short = 0
    standard = 0
    long = 0

    for record in records:
        if record.duration_hours < 4.0:
            short += 1
        elif record.duration_hours < 7.0:
            standard += 1
        else:
            long += 1

    total_records = short + standard + long

    if total_records == 0:
        return {
            "short": {"count": 0, "percentage": 0.0},
            "standard": {"count": 0, "percentage": 0.0},
            "long": {"count": 0, "percentage": 0.0},
        }

    return {
        "short": {"count": short, "percentage": (short / total_records) * 100},
        "standard": {"count": standard, "percentage": (standard / total_records) * 100},
        "long": {"count": long, "percentage": (long / total_records) * 100},
    }


def cumulative_duration(records: List[EvaRecord]):
    dates = []
    cumulative_hours = []
    total_hours = 0.0

    for record in records:
        total_hours += record.duration_hours
        dates.append(record.date)
        cumulative_hours.append(total_hours)

    return dates, cumulative_hours


def country_summary(records: List[EvaRecord], country):
    durations = [record.duration_hours for record in records if record.country == country]
    total_hours = sum(durations)
    average_hours = total_hours / len(durations) if durations else None
    return CountrySummary(len(durations), total_hours, average_hours)
