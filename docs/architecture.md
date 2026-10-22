# Proposed Architecture

## Modules and their responsibilities

I'm splitting the script into five small modules inside a folder called eva, each with one job:

- loader reads the data file.
- records checks each entry, skips the bad ones and turns the good ones into a simple record with a date, hours and country.
- analysis does all the calculations. It never reads files, prints anything or asks for input.
- presentation handles everything the user sees: printing, asking questions and saving the chart.
- app runs the steps in order and passes data between the others.

The original script stays as the starting point, so you still run the program the same way. It now just hands over to app.

## Dependencies between modules

app uses the other four, because it's the one running things. analysis uses records, because it works with the records that module produces. Nothing else depends on anything. Everything points one way, so changing how results look can't break a calculation.

## Interfaces between modules

The modules only pass data to each other through function inputs and return values, never through shared variables. The main functions are:

```
load_eva_data(path)                -> the raw data
prepare_records(raw)               -> clean records, number skipped
categorise_eva_by_length(records)  -> short, standard and long counts
cumulative_duration(records)       -> dates and running totals
country_summary(records, country)  -> count, total and average
```

The presentation functions take these results and display them. If a country has no EVAs, its average is left empty (None), which the comparison feature needs later on.

## Architecture diagram

Each arrow points to a module the one above it uses.

```mermaid
graph TD
    entry["entry script"] --> app
    app --> loader
    app --> records
    app --> analysis
    app --> presentation
    analysis --> records
```

## AR1: Separation of concerns

Each of the five jobs in the brief gets its own module: reading data (loader), checking and preparing it (records), calculations (analysis), showing results (presentation) and running everything (app). In the original they're all in one file, and some of them share the same loop.

## AR2: Why these module boundaries

I drew the lines based on what would make each part change. A new data source only affects the loader. A new rule for what counts as a valid record only affects records. A new calculation only touches analysis, a change to how things look only touches presentation, and adding a step only touches app. So each module has one reason to change.

For example, turning "6:15" into hours goes in records rather than analysis, because it's tidying up the data, not analysing it.

## AR3: Coupling in the inherited code and how it is addressed

The clearest example is the country totals. The original drops the country from each cleaned record, so the totals have to be added up inside the loop that reads the data and kept in two global dictionaries. The country report only works if that loop has already run, and any new country-based calculation would mean going back into the loop.

In the new version each record keeps its country, and the country summary is worked out from the records whenever it's needed. Reading the data and calculating country stats aren't tangled together anymore.

Two smaller fixes follow the same idea. The file name is now passed in by app instead of being hard-coded where the file is opened. And the calculations return their results instead of printing them, so they don't care how results are shown.

## AR4: Why the functions in each module belong together

- loader has just one function, for reading the file.
- records has everything to do with turning raw entries into clean records. These all change together if the data format changes.
- analysis has everything that calculates something from the clean records.
- presentation has everything the user sees or types. It's the only part that knows about the screen or matplotlib.
- app has only the main function, which decides the order things happen in.
