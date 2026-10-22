# EVA Data Analysis

This program looks at a dataset of 375 spacewalks (EVAs) by the USA and Russia between 1965 and 2013. When you run it, it:

1. saves a chart of total EVA hours over time
2. shows how many EVAs were short, standard or long
3. says how many records in the data were invalid and skipped
4. asks for a country and shows its number of EVAs, total hours and average
5. asks for two countries and a range of years, and compares them

## Setup

You need Python 3.8 or newer. Install matplotlib with:

```
pip install -r requirements.txt
```

## Running it

From this folder, so the program can find the data file:

```
python 1399480evacodev2.py
```

Country names have to match the data exactly (`USA` or `Russia`). The comparison counts both the start and end years.

## Running the tests

```
python -m unittest discover -s tests -v
```

There are 16 tests. They don't need the data file or matplotlib.

## How the code is organised

| Part | What it does |
|---|---|
| `1399480evacodev2.py` | The starting point. It just calls the app |
| `eva/app.py` | Runs each step in order and passes data between the other modules |
| `eva/loader.py` | Reads the data file |
| `eva/records.py` | Checks each entry, skips the bad ones and keeps the rest as clean records |
| `eva/analysis.py` | All the calculations. It never reads files, prints or asks for input |
| `eva/presentation.py` | Everything the user sees: the questions, the printed results and the chart |
| `tests/` | Tests for the records and the calculations |

The app uses the other four modules, and the analysis uses the records. Nothing else depends on anything. There's a diagram in [docs/architecture.md](docs/architecture.md).

## Write-ups and decision records

- [Initial assessment](docs/initial-assessment.md): what the inherited code did and what was wrong with it
- [Architecture](docs/architecture.md): the modules, how they connect and why
- [Restructuring](docs/restructuring.md): how the code was split up without changing what it does
- [Country comparison](docs/country-comparison.md): how the new feature was added
- [Evaluation](docs/evaluation.md): test results and a before-and-after comparison
- [ADR-001](docs/adr/ADR-001.md): split the script into modules by responsibility
- [ADR-002](docs/adr/ADR-002.md): test the calculations directly with made-up records

## History

I inherited this repository with six commits that built up a single script. Everything after that is my work: the assessment and design first, then a small tidy-up, the restructure on its own, the comparison feature, the tests, and finally the evaluation, the second ADR and this README.
