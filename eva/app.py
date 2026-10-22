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
    presentation.show_country_summary(country, analysis.country_summary(eva_records, country))
