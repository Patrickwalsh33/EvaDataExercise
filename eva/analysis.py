import math
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


@dataclass(frozen=True)
class CountryComparison:
    start_year: int
    end_year: int
    country_a: str
    summary_a: CountrySummary
    country_b: str
    summary_b: CountrySummary
    leader: Optional[str]  # None if it's a tie


def countries_in(records: List[EvaRecord]):
    return {record.country for record in records if record.country}


def records_between_years(records: List[EvaRecord], start_year, end_year):
    return [record for record in records if start_year <= record.date.year <= end_year]


def compare_countries(records: List[EvaRecord], country_a, country_b, start_year, end_year):
    if start_year > end_year:
        raise ValueError("start_year must not be after end_year")

    in_period = records_between_years(records, start_year, end_year)
    summary_a = country_summary(in_period, country_a)
    summary_b = country_summary(in_period, country_b)

    # decimals can be off by a tiny amount, so check for "close enough" instead of ==
    if math.isclose(summary_a.total_hours, summary_b.total_hours, abs_tol=1e-9):
        leader = None
    elif summary_a.total_hours > summary_b.total_hours:
        leader = country_a
    else:
        leader = country_b

    return CountryComparison(start_year, end_year, country_a, summary_a, country_b, summary_b, leader)
