import matplotlib

# non-interactive backend: the chart is saved to a file, never shown in a window
matplotlib.use("Agg")
import matplotlib.pyplot as plt


def save_cumulative_chart(dates, cumulative_hours, path):
    if not dates:
        return

    plt.figure()
    plt.plot(dates, cumulative_hours)
    plt.xlabel("Year")
    plt.ylabel("Cumulative EVA duration (hours)")
    plt.tight_layout()
    plt.savefig(path)
    plt.close()


def show_category_breakdown(categories):
    print("EVA category breakdown:")
    for category_name in ("short", "standard", "long"):
        category_data = categories[category_name]
        print(
            f"{category_name}: count={category_data['count']}, "
            f"percentage={category_data['percentage']:.2f}%"
        )


def show_skipped(skipped_count):
    print(f"Skipped invalid rows: {skipped_count}")


def _read(prompt):
    # None means input has ended (Ctrl+D / Ctrl+Z or the end of a piped file)
    try:
        return input(prompt).strip()
    except EOFError:
        return None


def ask_country():
    return _read("Enter country: ")


def show_input_ended():
    print()
    print("No more input. Goodbye!")


def show_country_summary(country, summary):
    if summary.count == 0:
        print(f"No EVA records found for {country}")
        return

    print(f"Number of EVAs for {country} is {summary.count}")
    print(f"Total EVA duration for {country} is {summary.total_hours:.2f} hours")
    print(f"Average EVA duration for {country} is {summary.average_hours:.2f} hours")


def _ask_country_name(prompt):
    while True:
        name = _read(prompt)
        if name is None or name:
            return name
        print("Please enter a country name.")


def _ask_year(prompt):
    while True:
        text = _read(prompt)
        if text is None:
            return None
        try:
            return int(text)
        except ValueError:
            print("Please enter a year as a whole number, for example 1990.")


def ask_comparison():
    print()
    print("Compare EVA activity between two countries")
    country_a = _ask_country_name("Country A: ")
    if country_a is None:
        return None
    country_b = _ask_country_name("Country B: ")
    if country_b is None:
        return None

    while True:
        start_year = _ask_year("Start year: ")
        if start_year is None:
            return None
        end_year = _ask_year("End year: ")
        if end_year is None:
            return None
        if start_year <= end_year:
            return country_a, country_b, start_year, end_year
        print("The start year can't be after the end year. Please enter both years again.")


def _format_average(summary):
    if summary.average_hours is None:
        return "unavailable"
    return f"{summary.average_hours:.2f} hours"


def show_comparison(comparison, known_countries):
    print()
    print(f"EVA comparison from {comparison.start_year} to {comparison.end_year}:")
    for country, summary in (
        (comparison.country_a, comparison.summary_a),
        (comparison.country_b, comparison.summary_b),
    ):
        if country not in known_countries:
            print(f"{country}: not found in the data")
        print(f"{country}: number of EVAs = {summary.count}")
        print(f"{country}: total EVA duration = {summary.total_hours:.2f} hours")
        print(f"{country}: average EVA duration = {_format_average(summary)}")

    if comparison.leader is None:
        print(f"Result: tie, both countries have {comparison.summary_a.total_hours:.2f} hours")
    else:
        print(f"Result: {comparison.leader} has the greater total EVA duration")
