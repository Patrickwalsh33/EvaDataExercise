# Initial Architectural Assessment

## What the application currently does

The app I inherited is a single Python script (1399480evacodev2.py) that reads a JSON file of 375 spacewalks, or EVAs, carried out by the USA and Russia between 1965 and 2013. I'll just call them the script and the data file from here on.

I ran it a few times with different inputs: USA, Russia, usa, Mars, a blank line, and no input at all. Each time it:

- loads the data and skips 45 records that are missing a date or a duration, leaving 330
- saves a chart of total EVA hours over time
- prints how many EVAs were short (under 4 hours), standard (4 to 7) and long (7 or more), which comes out as 71, 187 and 72
- asks for a country and prints its number of EVAs, total hours and average. The USA has 217 EVAs, 1257.13 hours and 5.79 hours on average. Russia has 113, 527.90 and 4.67.

A few odd things came up too. Country names have to match exactly, so "usa" isn't found. If there's no input when it asks for a country, the program crashes. And two cancelled EVAs logged as 0:00 still count as short EVAs.

## Git history

There are six commits from one developer, including a branch that was merged with a pull request. Every new feature was added to the same file, usually inside the same loop, so the script grew from 39 lines to 151. The first two commits pointed at data files that didn't exist, so the program only actually ran from the fourth commit on.

## Principal responsibilities

Everything happens in one file, but I could pick out six separate jobs:

- reading the data file
- checking each record and converting durations to hours
- doing the calculations: the per-country totals, the running total for the chart and the length categories
- showing the results, both the printed output and the chart
- asking the user for a country
- running everything in the right order. There's no main function, so this is just the order the code happens to be written in.

## Existing modules and their responsibilities

There's only one module, and it does all six jobs. It has two functions: one that turns a duration like "6:15" into hours, and one that sorts EVAs into short, standard and long. Everything else is loose code that runs the moment the file is opened.

## Areas where responsibilities are mixed

- The main loop checks each record and adds it to the country totals at the same time, so any new calculation means editing that loop.
- The list of cleaned records only keeps the date and duration, not the country. That's why the country totals have to be worked out inside the loop. It also means the new comparison feature, which needs the country and date together, can't use the list as it is.
- The country report reads the input, works out the average and prints the result all in one block.
- The chart is drawn right next to the code that calculates its data, with nothing separating the two.

## Dependencies between parts of the application

All the parts share the same global variables. The loop fills them in and the code further down reads them, so nothing works unless it runs in exactly the right order. The calculations also depend on the data file being in the right folder with its exact name, and on matplotlib being installed, even though they don't use it.

## Functionality that is difficult to test independently

Pretty much all of it. Just importing the file runs the whole program: it reads the data, saves the chart and then waits for someone to type a country. The country totals and averages only exist as loose code, not functions, so there's nothing to call with test data. Results are printed instead of returned, so checking them would mean capturing what's printed. Even the two existing functions can't be imported without the rest of the program running.
