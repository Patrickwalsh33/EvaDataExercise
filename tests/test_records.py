import unittest
from datetime import datetime

from eva.records import parse_duration_hours, prepare_records


class ParseDurationTests(unittest.TestCase):

    def test_valid_durations(self):
        self.assertEqual(6.25, parse_duration_hours("6:15"))
        self.assertEqual(0.0, parse_duration_hours("0:00"))

    def test_invalid_durations_return_none(self):
        for text in [None, "", "615", "abc", "6:xx", "1:2:3"]:
            with self.subTest(text=text):
                self.assertIsNone(parse_duration_hours(text))


class PrepareRecordsTests(unittest.TestCase):

    def test_invalid_records_are_skipped_and_counted(self):
        raw = [
            {"date": "1990-01-02T00:00:00.000", "duration": "2:30", "country": "USA"},
            {"duration": "1:00", "country": "USA"},
            {"date": "1990-01-01T00:00:00.000", "country": "Russia"},
            {"date": "not a date", "duration": "1:00", "country": "USA"},
            {"date": "1990-01-03T00:00:00.000", "duration": "bad", "country": "USA"},
            "not a record",
            {"date": "1985-05-05T00:00:00.000", "duration": "1:30", "country": "Russia"},
        ]
        records, skipped = prepare_records(raw)
        self.assertEqual(5, skipped)
        self.assertEqual(2, len(records))

    def test_records_are_sorted_by_date_and_keep_the_country(self):
        raw = [
            {"date": "1990-01-02T00:00:00.000", "duration": "2:30", "country": "USA"},
            {"date": "1985-05-05T00:00:00.000", "duration": "1:30", "country": "Russia"},
        ]
        records, _ = prepare_records(raw)
        self.assertEqual(datetime(1985, 5, 5), records[0].date)
        self.assertEqual("Russia", records[0].country)
        self.assertEqual(2.5, records[1].duration_hours)


if __name__ == "__main__":
    unittest.main()
