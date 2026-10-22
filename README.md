# EVA Data Analysis

Analyses extra-vehicular activity (EVA) records from `1399478eva-data.json` (375 EVAs by the USA and Russia, 1965 to 2013). When you run it, it:

1. Saves a chart of cumulative EVA duration to `cumulative_duration.png`.
2. Prints how many EVAs were short (under 4 hours), standard (4 to 7 hours) and long (7 hours or more).
3. Prints how many invalid records were skipped.
4. Asks for a country and prints its number of EVAs, total duration and average duration.
5. Asks for two countries and a range of years, and compares their EVA activity over that period.

## Setup

Requires Python 3.8 or later.

```
pip install -r requirements.txt
```

## Running the application

Run from the repository root, so the data file can be found:

```
python 1399480evacodev2.py
```

Country names are case-sensitive and must match the data (`USA` or `Russia`). Years are whole numbers, and the comparison includes both the start and end years.

## Running the tests

```
python -m unittest discover -s tests -v
```

The 16 tests don't need the data file or matplotlib.

## Module structure

| Module | Responsibility |
|---|---|
| `1399480evacodev2.py` | Entry point. Only calls `eva.app.main()` |
| `eva/app.py` | Coordinates a run: calls the other modules in order and passes data between them |
| `eva/loader.py` | Reads the JSON data file |
| `eva/records.py` | Validates raw entries and turns them into `EvaRecord` objects, counting the ones it skips |
| `eva/analysis.py` | All calculations: length categories, cumulative duration, country summaries and the country comparison. No file access, printing or input |
| `eva/presentation.py` | Everything the user sees: prompts, printed results and the chart |
| `tests/` | Automated tests for `records.py` and `analysis.py` |

`app.py` depends on the four modules below it, and `analysis.py` depends on `records.py`. Nothing else imports another project module. See [docs/architecture.md](docs/architecture.md) for the diagram and the interfaces between modules.

## Documentation and decision records

- [docs/initial-assessment.md](docs/initial-assessment.md): what the inherited code did and its problems
- [docs/architecture.md](docs/architecture.md): module responsibilities, dependencies, interfaces and diagram
- [docs/country-comparison.md](docs/country-comparison.md): how the comparison feature was added
- [docs/evaluation.md](docs/evaluation.md): test evidence and before/after evaluation
- [docs/adr/ADR-001.md](docs/adr/ADR-001.md): split the script into modules by responsibility
- [docs/adr/ADR-002.md](docs/adr/ADR-002.md): test the analysis as plain functions with hand-made records

## History

The repository was inherited with six commits that built up a single script. The commits since then are, in order: the initial assessment, the proposed architecture and ADR-001, a housekeeping commit (`.gitignore` and `requirements.txt`), the restructure on its own, the country comparison feature, the automated tests, and the evaluation, ADR-002 and this README.
