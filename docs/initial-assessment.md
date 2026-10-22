# Initial Architectural Assessment

## What the application currently does

The inherited application is a single Python script (`1399480evacodev2.py`) that analyses `1399478eva-data.json`. The number prefixes appear to be student numbers, so I refer to the files as evacodev2.py and eva-data.json below. The data file contains 375 EVA (extra-vehicular activity) records from 1965 to 2013, all from the USA or Russia. I ran it with Python 3.10 and matplotlib 3.10, entering USA, Russia, usa, Mars, an empty line, and once with no input at all. Every run does the following, in this order:

- Loads the JSON file.
- Skips invalid records: 45 of the 375 (44 have no date and one has no duration), which leaves 330.
- Saves a cumulative EVA duration chart to `cumulative_duration.png`.
- Prints a breakdown by EVA length: short (under 4 hours) 71 (21.52%), standard (4 to 7 hours) 187 (56.67%) and long (7 hours or more) 72 (21.82%).
- Prints the number of skipped rows (45).
- Asks for a country and prints its EVA count, total duration and average duration. USA: 217 EVAs, 1257.13 hours, average 5.79 hours. Russia: 113 EVAs, 527.90 hours, average 4.67 hours.

Other behaviour I found when running it:

- The country match is case-sensitive, so "usa" prints "No EVA records found for usa". Unknown or empty countries print the same message.
- If input ends before a country is entered, the program crashes.
- Two cancelled EVAs recorded with a duration of 0:00 (STS-5 and STS-31) have dates, so they are counted as valid short EVAs.

## Git history

The repo has six commits by one developer, including a feature branch merged through a pull request. Each feature was added to the same file, usually inside the same loop, so the script grew from 39 to 151 lines. The first two commits pointed at data files that don't exist, so the program only ran from the fourth commit onwards.

## Principal responsibilities

I identified six responsibilities in the current code:

- Reading data: opening and parsing the JSON file at the top of the script (lines 9 to 10), with the filename hard-coded.
- Validating and preparing data: the main loop (lines 64 to 97) and `parse_duration_hours` (lines 15 to 23), which skip records with a missing or invalid date or duration and convert durations to hours.
- Calculations and analysis: per-country totals and counts (lines 90 to 97), the cumulative total (lines 101 to 108), the length categories (`categorise_eva_by_length`, lines 27 to 53) and the per-country average (lines 133 to 136).
- Presenting results: the chart (lines 110 to 117) and the printed output (lines 120 to 128 and 138 to 151).
- Getting user input: the country prompt (line 130).
- Coordinating execution: there is no main function. The order of the top-level code is the only thing that coordinates the program.

## Existing modules and their responsibilities

There is one module, evacodev2.py, and it carries all six responsibilities. It has two functions:

- `parse_duration_hours` converts duration text such as "6:15" into hours, and returns None if the text is missing or invalid.
- `categorise_eva_by_length` counts EVAs as short, standard or long and works out the percentage of each.

Everything else is top-level code that runs as soon as the file is imported or executed.

## Areas where responsibilities are mixed

- The main loop (lines 64 to 97) validates each record, converts it, and also adds it to the per-country totals and counts. Adding any new calculation that needs per-record data means editing the parsing loop.
- The records list stores only (date, duration) and drops the country. Country statistics therefore can't be calculated from the cleaned records afterwards, and have to be accumulated while parsing. The new country comparison needs both the country and the date of each EVA, which this structure doesn't keep together.
- The country report (lines 130 to 151) mixes reading input, calculating the average and printing the results in one if/else block.
- The cumulative-duration calculation and the chart drawing sit next to each other at the top level, with no boundary between calculating the data and presenting it.

## Dependencies between parts of the application

- All parts of the program share module-level variables: `eva_data`, `records`, `total_eva_hours_by_country`, `eva_count_by_country` and `skipped_records`. They are written in the loop and read further down, so the order of the code matters.
- The analysis depends on the data file: the filename is hard-coded and the file must be in the current working directory.
- The country report depends on two separate dictionaries that were filled in the parsing loop, and on them always having the same keys.
- `categorise_eva_by_length` depends on the internal shape of records, because it unpacks each item as a (date, duration) tuple.
- matplotlib is imported and configured at the top of the file, so any use of the code needs matplotlib installed, even code that only calculates.

## Functionality that is difficult to test independently

- Importing the file runs the whole program: it reads the data file, writes the chart and then waits for keyboard input. No part of it can be imported into a test without these side effects.
- The per-country count, total and average exist only as top-level code. There is no function that can be called with known test data.
- Record validation and the skipped-row count happen only inside the main loop.
- The cumulative-duration calculation is inline and can't be called on its own.
- Results are printed rather than returned, so checking them would mean capturing the console output.
- `parse_duration_hours` and `categorise_eva_by_length` are the only functions, and even they can't be imported without running the program.
