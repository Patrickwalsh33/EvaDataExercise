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


def ask_country():
    return input("Enter country: ").strip()


def show_country_summary(country, summary):
    if summary.count == 0:
        print(f"No EVA records found for {country}")
        return

    print(f"Number of EVAs for {country} is {summary.count}")
    print(f"Total EVA duration for {country} is {summary.total_hours:.2f} hours")
    print(f"Average EVA duration for {country} is {summary.average_hours:.2f} hours")
