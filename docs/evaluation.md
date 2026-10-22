# Test Evidence and Maintainability Evaluation

## AR6: Automated tests

There are 16 automated tests using Python's built-in unittest, so nothing extra needs installing. Each test makes a small list of EVAs by hand where I already know the right answer, so none of them need the data file, print anything or use matplotlib. You can run them with:

```
python -m unittest discover -s tests -v
```

They cover what the brief asks for:

- The comparison (6 tests): normal results, both end years counting, a country with no EVAs, ties, and rejecting a start year after the end year.
- Existing features (4 tests): the length breakdown, the single-country summary, the exact country match and the running total.
- Edge cases and bad input (6 tests): EVAs of exactly 4 and 7 hours, an empty list, bad duration text, invalid records being skipped and counted, and records coming out in date order.

## Test results

All 16 pass:

```
Ran 16 tests in 0.002s

OK
```

To make sure the tests actually check something, I deliberately broke the year filter in a copy of the code so it ignored the start and end years. Two tests failed straight away, and they passed again once I put it back.

## Existing functionality still works

I ran the finished version with the same five inputs as before. Everything up to the new comparison section matched the original exactly. The only difference is at the end, where it now moves on to the comparison and exits cleanly instead of crashing when input runs out. I also checked the comparison numbers against totals worked out separately from the raw data, and they match.

## Before and after restructuring

Before, it was one 151-line file of loose code sharing global variables, with no tests and nothing that could be tested. After, it's five small modules plus a 4-line starting script, 318 lines in total including the new feature, and 16 tests.

### How many modules needed modification to implement FR22?

Three out of six: analysis.py, presentation.py and app.py. The rest didn't change. In the original, the same feature would have meant going back into the main loop to track years for each country, and piling more input, maths and printing into the same file.

### Which modules depend on other modules?

app.py depends on the other four modules, and analysis.py depends on records.py. Nothing else depends on anything, and nothing depends on presentation.py, so the display can change without affecting a calculation. I checked this by looking at what each file imports. In the original, everything depended on the same shared variables.

### Can calculations be tested without reading files or displaying results?

Yes. analysis.py and records.py don't read files, print or use matplotlib, so the tests just hand them some records and check what comes back. The whole set runs in a fraction of a second without the data file. Before, you couldn't even import the code without the whole program running.

### Are responsibilities easier to identify?

Yes. Each module is named after what it does, so you know where to look. Want to change the wording of the output? That's presentation.py. Want to change what counts as a valid record? That's records.py. Before, you had to read the whole script to find anything, because it was all mixed together.

### Has duplication been reduced?

Yes. The original kept the count and total in two separate dictionaries that had to be updated in step, and worked out the average somewhere else. Now one function does all three, and both the old report and the new comparison use it.

There's still a bit of repetition in how the two features print country stats, because I kept the original output exactly as it was.

### Did the restructuring introduce unnecessary complexity?

A bit, but I think it's worth it. There are six files instead of one, and you have to start in app.py to follow what happens. The code went from 151 lines to 318, but most of that is the new feature. The restructure on its own only took it to 189.

I didn't add classes, frameworks or extra libraries, and every module is short. Honestly, in a program this small loader.py could be folded into records.py, but the brief wants reading kept separate, and it does mean a new data source only changes one file. In return, the calculations can be tested on their own and the new feature only touched three files.
