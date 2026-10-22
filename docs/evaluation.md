# Test Evidence and Maintainability Evaluation

## AR6: Automated tests

The tests are in `tests/test_analysis.py` and `tests/test_records.py` and use Python's built-in unittest, so no new dependency was added. Each test builds a small list of EVA records by hand with answers worked out in advance, so none of them read the data file, print anything or need matplotlib. Run them from the repository root with:

```
python -m unittest discover -s tests -v
```

There are 16 tests. They cover the three things AR6 asks for:

- The new country comparison (6 tests): totals, counts, averages and the leader for a normal range; start and end years both included; a country with no EVAs gets 0 and an unavailable average; equal totals are a tie, including when neither country has EVAs; a start year after the end year raises a ValueError.
- Existing analysis (4 tests): the short/standard/long breakdown and its percentages, the single-country summary, the case-sensitive country match and the cumulative duration.
- Boundary conditions and invalid input (6 tests): durations of exactly 4.0 and 7.0 hours go into the right category, an empty list of records, valid and invalid duration strings (invalid ones return None), invalid records are skipped and counted, and valid records come out sorted by date with their country kept.

## Test results

All 16 tests pass on commit 4393af4:

```
Ran 16 tests in 0.002s

OK
```

To check the tests really test the results and don't just pass, I changed the year filter in a copy of the code so it left out the start and end years. Two tests failed straight away (test_start_and_end_years_are_included and test_totals_counts_averages_and_leader), and they pass again with the correct code.

## Existing functionality still works

I ran the final version with the same five inputs as the AR5 check (USA, Russia, usa, Mars and an empty line). For each one, everything printed before the new comparison section is identical to the original program's output. The only difference is at the end: the program now goes on to the comparison prompts, and if input ends it prints "No more input. Goodbye!" instead of crashing.

I also checked the comparison results against totals calculated separately from the raw JSON file, for 1990 to 2000 (USA 36 EVAs, 233.13 hours; Russia 58 EVAs, 272.45 hours) and for single years at both ends of the data, and they match.

## Before and after restructuring

- Before: one file of 151 lines, mostly top-level code sharing global variables. Two functions, which couldn't be imported without running the whole program. No tests.
- After: five modules in the eva package plus a 4-line entry script, 318 lines in total including the new feature, and 16 automated tests.

### How many modules needed modification to implement FR22?

Three of the six files: analysis.py (the calculation), presentation.py (the prompts and output) and app.py (one extra step). loader.py, records.py and the entry script didn't change. The only edits to existing code were in presentation.ask_country, to stop the crash when input ends, and the new step in app.main.

In the original script the same feature would have meant changing the parsing loop to keep each EVA's year by country, plus adding more input, calculations and printing to the same file.

### Which modules depend on other modules?

- app.py depends on loader, records, analysis and presentation.
- analysis.py depends on records.py (for EvaRecord).
- The entry script depends only on app.py.
- loader.py, records.py and presentation.py don't import any other module from the project.

I checked this from the import lines in each file. Dependencies only point one way, and nothing depends on presentation.py, so how results are displayed can change without affecting the calculations. Before, every part of the script depended on the same global variables.

### Can calculations be tested without reading files or displaying results?

Yes. analysis.py and records.py don't read files or print, and neither imports matplotlib, so the tests create EvaRecord objects directly and check the returned values. All 16 tests run without the data file in 0.002 seconds. Before the restructure, nothing could be imported without the program reading the file, writing the chart and waiting for input.

### Are responsibilities easier to identify?

Yes. Each file is named after its responsibility, so it's clear where to look: changing the output wording means opening presentation.py, changing validation means opening records.py, and so on. Before, finding any of these meant reading the whole script, because validation, calculation and output were mixed in the same loop and blocks.

### Has duplication been reduced?

Yes. In the original, the per-country count and total were kept in two separate dictionaries that had to be updated together, and the average was calculated somewhere else again. Now country_summary works out all three in one place, and both the single-country report and the new comparison use it, so the comparison doesn't repeat any calculation.

Some duplication is left in presentation.py, which prints country statistics in two slightly different formats for the two features. I kept the original format exactly so existing output didn't change.

### Did the restructuring introduce unnecessary complexity?

A little, but I think it's justified. There are six files instead of one, two small dataclasses, and app.py has to pass data between the modules, so following one run means reading app.py first. The code grew from 151 to 318 lines, but most of that is the new feature: the restructure on its own went from 151 to 189 lines.

I avoided classes, frameworks and new dependencies, and each module is short. In a program this size, loader.py could reasonably be merged into records.py, but keeping reading separate is what AR1 asks for and it means a different data source only changes one file. In return, the calculations can be tested on their own and the new feature only touched three files.
