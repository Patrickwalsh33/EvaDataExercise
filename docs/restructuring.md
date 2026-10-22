# Restructuring

## Restructuring commit

The restructure is in its own commit (08adcaa). It only moves the existing code around, with no new features and no bug fixes, so it's easy to check that nothing changed.

Just before it there's a small tidy-up commit (5984205). It adds a .gitignore and a requirements file, and stops tracking files the program recreates every time it runs.

## Where the existing code moved

Reading the file went into loader.py, and the file name now comes from app.py. The validation loop and the sorting went into records.py, which now keeps the country on each record and returns the number skipped instead of using a global.

The length categories and the running total went into analysis.py. The two country dictionaries and the separate average calculation were replaced by one country summary function, also in analysis.py.

The chart, all the printing and the country question went into presentation.py, and the order of everything now lives in the main function in app.py. All the global variables are gone, and the original script is down from 151 lines to 4.

## AR5: Evidence that existing behaviour is preserved

Before touching anything, I saved what the original program printed for five inputs (USA, Russia, usa, Mars and a blank line), plus the chart it made. After the restructure I ran the new version with the same inputs and compared the two:

- the printed output was identical in all five cases
- the chart was identical, pixel for pixel
- with no input at all, both crashed in the same way. I left this alone on purpose so the restructure changed nothing, and fixed it later in the feature commit.

Here's the USA run, which looks the same before and after:

```
EVA category breakdown:
short: count=71, percentage=21.52%
standard: count=187, percentage=56.67%
long: count=72, percentage=21.82%
Skipped invalid rows: 45
Enter country: USA
Number of EVAs for USA is 217
Total EVA duration for USA is 1257.13 hours
Average EVA duration for USA is 5.79 hours
```
