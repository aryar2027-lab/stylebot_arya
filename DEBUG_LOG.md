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

## Round 4: Bugs caught by unit tests

Manual testing only finds what you think of trying, so the AI was asked to write **unit tests** (`tests/test_stylebot.py`). Each test file was committed *before* the fix, so the history shows the test failing first and passing after.

### Bug 9: `Rs. 3000` rejected as an invalid budget
**Failing test:**
```
FAIL: test_rs_with_dot
    self.assertEqual(stylebot.parse_budget("Rs. 3000"), 3000)
AssertionError: None != 3000
```
**Cause:** the fix for Bug 6 cut the text at the **first** `.` to drop paise, but in `Rs. 3000` the first dot belongs to "Rs.", so only `Rs` was left. *A fix for one bug created a new one.*
**Fix:** find the number itself with a regular expression (`\d[\d,]*`) instead of splitting at dots.
*Commits: "Add unit tests for rupee formatting and budget parsing" → "Fix 'Rs. 3000' being rejected as an invalid budget"*

### Bug 10: Item prices added up to more than the budget
**Failing test:**
```
FAIL: test_total_never_exceeds_budget
AssertionError: 650 not less than or equal to 500 : Ethnic/Men at 500
```
**Cause:** each item was rounded to the *nearest* ₹50 with a minimum of ₹50, so rounding up on several items pushed ₹5,000 to ₹5,050, and small budgets went far over.
**Fix:** a new `split_budget()` rounds every share **down**, then gives the leftover to the items that lost the most in rounding (the "largest remainder" method). Totals now match the budget exactly. The minimum budget was raised to ₹500.
*Commits: "Add unit tests for outfit building and shopping links" → "Fix item prices adding up to more than the budget"*

### Bug 11: Wrong saved look could be chosen
**Found while adding the delete feature (code review with AI):** saved looks were picked with `titles.index(choice)`. Two looks saved in the same minute have identical titles, and `index()` always returns the *first*, so deleting the second look would have deleted the first one.
**Fix:** `choose()` can now return the position (`return_index=True`).

### Bug 12: `/` in a file name
**Found while adding export:** naming the file after "Graduation / Convocation" would treat the `/` as a folder and fail. `safe_filename()` turns it into `graduation-convocation`, and a unit test covers it.

---

## Final checks
- **19 unit tests pass**, and GitHub Actions runs them on macOS, Windows and Linux (Python 3.10 and 3.13)
- Every combination of 9 occasions × 5 styles × 2 genders builds a look, and totals equal the budget exactly
- Rupee formatting: `₹999`, `₹1,000`, `₹1,25,000`, `₹1,00,00,000`
- Zara and H&M are correctly skipped for ethnic clothing items
- Searches include the gender ("women block heels")
