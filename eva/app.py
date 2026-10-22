from eva import analysis, loader, presentation, records

DATA_FILE = "1399478eva-data.json"
CHART_FILE = "cumulative_duration.png"


def main():
    raw_records = loader.load_eva_data(DATA_FILE)
    eva_records, skipped_count = records.prepare_records(raw_records)

    dates, cumulative_hours = analysis.cumulative_duration(eva_records)
    presentation.save_cumulative_chart(dates, cumulative_hours, CHART_FILE)

    presentation.show_category_breakdown(analysis.categorise_eva_by_length(eva_records))
    presentation.show_skipped(skipped_count)

    country = presentation.ask_country()
    if country is None:
        presentation.show_input_ended()
        return
    presentation.show_country_summary(country, analysis.country_summary(eva_records, country))

    request = presentation.ask_comparison()
    if request is None:
        presentation.show_input_ended()
        return
    country_a, country_b, start_year, end_year = request
    comparison = analysis.compare_countries(eva_records, country_a, country_b, start_year, end_year)
    presentation.show_comparison(comparison, analysis.countries_in(eva_records))
