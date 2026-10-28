# 🐞 Debug Log: AI-Assisted Debugging

This log records the bugs found while testing the AI-generated StyleBot and how each was fixed with the help of an AI assistant. Every fix matches a commit in the Git history (`git log`).

**How testing was done:** each version was run with realistic *and* awkward inputs, the way a real user might type them: `₹3,000`, `0`, `9`, letters, a blank colour, decimals, Ctrl+C, and a Windows-style console. Any error message (traceback) was pasted to the AI with the question *"Why does this happen and how do I fix it?"*

---

## Round 1: Bugs in the first AI-generated version
*Fixed in commit "Fix crashes on budget and menu input, blank colour, and broken links"*

### Bug 1: Budget with ₹ or comma crashes the program
**Input:** `₹3,000`
```
  File "stylebot.py", line 60, in main
    budget = int(input("Budget in Rs: "))
ValueError: invalid literal for int() with base 10: '₹3,000'
```
**Cause (AI explanation):** `int()` only accepts plain digits. Indian users naturally type `₹` and commas.
**Fix:** a new `ask_budget()` function removes everything except digits and asks again if nothing valid is left.

### Bug 2: Typing `0` silently picks the wrong event (no error!)
**Input:** `0` at the event menu → the program chose **"Beach trip"**.
**Cause:** the code did `options[int(choice) - 1]`, so `0` becomes `options[-1]`. In Python, index `-1` means *the last item*, so instead of an error the user got the wrong answer. This is the most dangerous kind of bug because nothing looks broken.
**Fix:** only accept numbers from 1 to the length of the list.

### Bug 3: Out-of-range number or letters crash the menu
**Input:** `9` → `IndexError: list index out of range`; `abc` → `ValueError`.
**Fix:** same validation as Bug 2, inside a loop that asks again: `Please enter a number from 1 to 7.`

### Bug 4: Blank colour gives broken item names and links
**Input:** pressing Enter for colour.
```
-  kurta
    Myntra: https://www.myntra.com/+kurta
```
**Cause:** `"{color} kurta"` with an empty colour leaves a leading space, which became `+` in the URL.
**Fix:** collapse extra spaces with `" ".join(text.split())`. Links are now URL-encoded with `urllib.parse.quote`, and Myntra uses its `word-word-word` path format.

---

## Round 2: Logic problem found by reviewing output

### Bug 5: The event was ignored
A **wedding** and a **beach trip** produced the *same* outfit, because the first version never used the event, and the budget was printed but never used either.
**Fix (feature commit):** each event now sets a dress level (dressy / smart / relaxed), colour palette, extra accessories and a tip; the budget is split across items.

### Bug 6: A decimal budget was read 100× too big
**Input:** `3000.50` → the round-1 fix removed the dot and read **₹3,00,050**.
**Cause:** "keep only digits" also kept the paise digits.
**Fix:** take only the part before the decimal point: `text.split(".")[0]`.

---

## Round 3: Bugs found testing the full version

### Bug 7: Crash on Windows consoles (emoji and ₹)
**How found:** ran the app with a Windows-style console encoding (`PYTHONIOENCODING=cp1252`):
```
UnicodeEncodeError: 'charmap' codec can't encode character '\U0001f457' in position 3
```
**Cause (AI explanation):** older Windows consoles use the cp1252 code page, which has no emoji. Printing 👗 crashed the program before the menu even appeared.
**Fix:** `fix_console_encoding()` switches output to UTF-8 and uses `errors="replace"`, so an unsupported character prints as `?` instead of crashing.
*Commit: "Fix UnicodeEncodeError on Windows consoles that use a legacy code page"*

### Bug 8: Unrealistic budget split
**Output:** a lehenga and its dupatta were each budgeted ₹1,500.
**Fix:** the main garment now gets double weight → lehenga ₹2,000, dupatta ₹1,000.
*Commit: "Give the main garment a bigger share of the budget"*

### Also handled
- **Ctrl+C / Ctrl+D** printed a long traceback → now exits with `Bye! 👋`
- **Corrupted `saved_looks.json`** → shows a message and starts fresh instead of crashing
- **Odd suggestion:** "mojari-matching pocket square" for weddings → replaced with "silk pocket square"

---

## Final checks
- All **140** combinations (7 events × 5 styles × 2 genders × with/without colour) build a look without errors
- Rupee formatting: `₹999`, `₹1,000`, `₹1,25,000`, `₹1,00,00,000`
- Zara and H&M are correctly skipped for ethnic clothing items
