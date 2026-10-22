# Country Comparison Feature

## Feature commit

The feature is commit 751a4da, "Add country comparison feature". It comes after the restructuring commit, so the restructure and the new functionality are in separate commits.

## How the comparison works

After the existing single-country step, the program asks for Country A, Country B, a start year and an end year. It then shows the number of EVAs, total duration and average duration for each country in that period, and which country has the greater total duration. Example run:

```
Country A: USA
Country B: Russia
Start year: 1990
End year: 2000

EVA comparison from 1990 to 2000:
USA: number of EVAs = 36
USA: total EVA duration = 233.13 hours
USA: average EVA duration = 6.48 hours
Russia: number of EVAs = 58
Russia: total EVA duration = 272.45 hours
Russia: average EVA duration = 4.70 hours
Result: Russia has the greater total EVA duration
```

How it meets each requirement:

- Both years are included: records_between_years keeps EVAs where start_year <= year <= end_year. 1965 to 1966 gives 9 USA EVAs, which is 1 from 1965 plus 8 from 1966.
- No matching EVAs: the count and total are 0 and the average is shown as "unavailable".
- Tie: if both totals are equal the result says it's a tie. Entering the same country twice shows this.
- Unknown countries: a country that isn't in the data (for example Mars) is reported as "not found in the data" with zero results, instead of an error.
- Invalid input: a blank country name, a year that isn't a whole number, or a start year after the end year gets a message and is asked for again.
- No unexpected termination: if input ends at any prompt, the program prints "No more input. Goodbye!" and exits normally. This also fixes the crash in the original single-country prompt.
- Existing functionality: for all five inputs from the baseline, everything before the comparison is identical to the original output.

I checked the numbers by calculating them separately from the raw JSON file, and they match.

## Reuse of existing analysis

compare_countries doesn't calculate any totals itself. It filters the records to the year range and then calls the existing country_summary for each country, which is the same function the single-country report uses. So count, total and average are worked out in one place, and the "unavailable" average comes from country_summary returning None for a country with no EVAs.

The comparison also uses the same EvaRecord list that prepare_records already produces, so no new loading or validation code was needed.

## Modules changed

Three modules changed:

- analysis.py: added CountryComparison, countries_in, records_between_years and compare_countries.
- presentation.py: added the comparison prompts and output, and a small _read helper that handles the end of input. ask_country now uses _read, which is the only change to existing code.
- app.py: added the comparison step after the existing country summary.

loader.py, records.py and the entry script didn't change. Adding a new analysis only needed the calculation in analysis.py, the input and output in presentation.py, and one step in app.py, which is how ADR-001 expected it to work.

## Architectural changes

No architectural changes were needed. There are no new modules and no new dependencies between modules, and the diagram in tab 2 still applies. The only new import is Python's standard math module in analysis.py, used to compare totals for a tie.

Two small design choices are worth recording:

- The year range is checked in two places. presentation.py asks the user again if the start year is after the end year, and compare_countries raises a ValueError if it's ever called with an invalid range. The first is for the user, and the second protects the calculation if it's reused somewhere else.
- Ties are checked with math.isclose instead of ==, because totals that should be equal can differ slightly in floating point.
