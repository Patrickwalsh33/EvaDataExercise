# Country Comparison Feature

## Feature commit

The comparison feature is in its own commit (751a4da), after the restructure.

## How the comparison works

After the existing country question, the program asks for two countries and a start and end year. It then shows each country's number of EVAs, total hours and average hours for that period, and says which one has more hours in total. For example:

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

It handles the awkward cases the brief mentions:

- Both the start and end years count. 1965 to 1966 gives the USA 9 EVAs: 1 in 1965 and 8 in 1966.
- A country with no EVAs in that period shows 0 EVAs, 0 hours and "unavailable" for the average.
- If both totals are the same, it says it's a tie.
- A country that isn't in the data at all, like Mars, gets a "not found" note and zeros instead of an error.
- A blank country, a year that isn't a number, or a start year after the end year gets a message and you're asked again.
- If the input runs out at any point, it says goodbye and exits normally instead of crashing. This fixes the old crash too.

Everything printed before the comparison is exactly the same as the original. I also double-checked the numbers by working them out separately from the raw data.

## Reuse of existing analysis

The comparison doesn't do any adding up of its own. It narrows the records down to the chosen years, then uses the same country summary that the original single-country report uses. So the count, total and average are only ever calculated in one place. It also works from the same clean records as everything else, so no new loading or checking code was needed.

## Modules changed

Only three: analysis.py got the comparison calculation, presentation.py got the new questions and output, and app.py got one extra step. loader.py, records.py and the starting script didn't change at all.

That's how the design was meant to work. A new feature adds a calculation, a way to show it and a step to run it, and nothing else needs touching. The only change to existing code was making the country question cope with input running out.

## Architectural changes

None were needed. There are no new modules and no new connections between them, so the diagram in tab 2 still holds.

Two small choices are worth mentioning. The year range is checked twice: once when the user types it, so they can try again, and once in the calculation itself, so it can't be misused if someone calls it from somewhere else. And ties are checked as "close enough" rather than exactly equal, because decimal numbers in Python can be off by a tiny amount.
