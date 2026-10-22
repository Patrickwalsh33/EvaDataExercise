from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass(frozen=True)
class EvaRecord:
    date: datetime
    duration_hours: float
    country: Optional[str]


def parse_duration_hours(duration_text):
    if not duration_text or ":" not in duration_text:
        return None

    try:
        hours, minutes = map(int, duration_text.split(":"))
        return hours + minutes / 60
    except ValueError:
        return None


def prepare_records(raw_records):
    records = []
    skipped = 0

    for eva in raw_records:
        if not isinstance(eva, dict):
            skipped += 1
            continue

        date_text = eva.get("date")
        duration_text = eva.get("duration")

        if not date_text or not duration_text:
            skipped += 1
            continue

        try:
            date = datetime.fromisoformat(date_text)
        except ValueError:
            skipped += 1
            continue

        duration_hours = parse_duration_hours(duration_text)
        if duration_hours is None:
            skipped += 1
            continue

        # treat a blank country the same as a missing one
        records.append(EvaRecord(date, duration_hours, eva.get("country") or None))

    records.sort(key=lambda record: record.date)
    return records, skipped
