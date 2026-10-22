import unittest
from datetime import datetime

from eva.analysis import categorise_eva_by_length, compare_countries, country_summary, cumulative_duration
from eva.records import EvaRecord


def eva(year, hours, country):
    return EvaRecord(datetime(year, 6, 1), hours, country)


RECORDS = [
    eva(1965, 0.5, "Russia"),
    eva(1966, 2.0, "USA"),
    eva(1990, 6.0, "USA"),
    eva(1990, 5.0, "Russia"),
    eva(1995, 7.5, "USA"),
    eva(2000, 3.0, "Russia"),
    eva(2001, 8.0, "USA"),
]


class CompareCountriesTests(unittest.TestCase):

    def test_totals_counts_averages_and_leader(self):
        result = compare_countries(RECORDS, "USA", "Russia", 1990, 2000)
        self.assertEqual(2, result.summary_a.count)
        self.assertAlmostEqual(13.5, result.summary_a.total_hours)
        self.assertAlmostEqual(6.75, result.summary_a.average_hours)
        self.assertEqual(2, result.summary_b.count)
        self.assertAlmostEqual(8.0, result.summary_b.total_hours)
        self.assertAlmostEqual(4.0, result.summary_b.average_hours)
        self.assertEqual("USA", result.leader)

    def test_start_and_end_years_are_included(self):
        result = compare_countries(RECORDS, "USA", "Russia", 1965, 1966)
        self.assertEqual(1, result.summary_a.count)
        self.assertEqual(1, result.summary_b.count)

    def test_country_with_no_evas_has_zero_and_unavailable_average(self):
        result = compare_countries(RECORDS, "USA", "Mars", 1990, 2000)
        self.assertEqual(0, result.summary_b.count)
        self.assertEqual(0, result.summary_b.total_hours)
        self.assertIsNone(result.summary_b.average_hours)
        self.assertEqual("USA", result.leader)

    def test_equal_totals_are_a_tie(self):
        records = [eva(1990, 2.5, "USA"), eva(1990, 1.0, "Russia"), eva(1991, 1.5, "Russia")]
        result = compare_countries(records, "USA", "Russia", 1990, 1991)
        self.assertIsNone(result.leader)

    def test_no_evas_for_either_country_is_a_tie(self):
        result = compare_countries(RECORDS, "USA", "Russia", 2005, 2010)
        self.assertEqual(0, result.summary_a.count)
        self.assertIsNone(result.leader)

    def test_start_year_after_end_year_is_rejected(self):
        with self.assertRaises(ValueError):
            compare_countries(RECORDS, "USA", "Russia", 2000, 1990)


class ExistingAnalysisTests(unittest.TestCase):

    def test_category_breakdown(self):
        categories = categorise_eva_by_length(RECORDS)
        self.assertEqual(3, categories["short"]["count"])
        self.assertEqual(2, categories["standard"]["count"])
        self.assertEqual(2, categories["long"]["count"])
        self.assertAlmostEqual(3 / 7 * 100, categories["short"]["percentage"])

    def test_category_boundaries(self):
        categories = categorise_eva_by_length([eva(2000, 4.0, "USA"), eva(2000, 7.0, "USA")])
        self.assertEqual(0, categories["short"]["count"])
        self.assertEqual(1, categories["standard"]["count"])
        self.assertEqual(1, categories["long"]["count"])

    def test_category_breakdown_with_no_records(self):
        categories = categorise_eva_by_length([])
        self.assertEqual({"count": 0, "percentage": 0.0}, categories["short"])

    def test_country_summary_over_all_years(self):
        summary = country_summary(RECORDS, "Russia")
        self.assertEqual(3, summary.count)
        self.assertAlmostEqual(8.5, summary.total_hours)
        self.assertAlmostEqual(8.5 / 3, summary.average_hours)

    def test_country_match_is_case_sensitive(self):
        self.assertEqual(0, country_summary(RECORDS, "usa").count)

    def test_cumulative_duration(self):
        dates, hours = cumulative_duration(RECORDS[:3])
        self.assertEqual([datetime(1965, 6, 1), datetime(1966, 6, 1), datetime(1990, 6, 1)], dates)
        self.assertEqual([0.5, 2.5, 8.5], hours)


if __name__ == "__main__":
    unittest.main()
