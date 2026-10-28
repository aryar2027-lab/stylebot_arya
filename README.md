# 👗 StyleBot: Outfit & Accessory Finder 👔

![Tests](../../actions/workflows/tests.yml/badge.svg)

A Python console app that automates an everyday decision: **"What should I wear?"**

Tell StyleBot the **occasion** you're dressing for and the **type of clothes** you want. It suggests a complete outfit with footwear and matching **accessories**, splits your **budget in ₹** across the items, and gives you search links to shop each piece on **Myntra, Ajio, Amazon.in, Nykaa Fashion, Zara and H&M**. It can even open them in your browser or export a shopping list.

> Built for **Mini-Project 2: Programming**. The code was generated with an AI assistant, debugged with AI help (see [DEBUG_LOG.md](DEBUG_LOG.md)), and this README was AI-generated too. The 24-commit Git history shows every step.

---

## ✨ Features

- **9 occasions:** Wedding, Haldi/Mehendi, Festival (Diwali/Eid/Navratri), Party, Interview/Office, College/Casual, Graduation/Convocation, Date, Beach/Vacation
- **5 styles:** Ethnic, Formal, Casual, Western, Fusion, for Men or Women
- **Event-aware outfits:** a wedding gets a silk kurta and nehru jacket; a beach trip gets linen; an interview gets a blazer. Each occasion has its own dress level, colour palette and styling tip
- **Accessories** matched to the look (jhumkas and potli bag for ethnic, watch and belt for formal, sunglasses and a hat for the beach…)
- **Budget split:** your ₹ budget is divided across items (main garment gets the most) and always adds up to exactly your budget, shown Indian-style (₹1,25,000)
- **Shopping links** for 6 sites, searched by gender ("women block heels") and opened in your browser if you want. Zara and H&M are skipped for ethnic wear they don't stock
- **Export a shopping list** as a Markdown checklist with clickable links
- **No colour in mind?** StyleBot picks one that suits the occasion; press `n` for another
- **Save, view and delete looks**
- Gentle **warning** if your style is unusual for the occasion (e.g. casual wear to an interview)
- **No installation needed:** only Python's standard library; tested on macOS, Windows and Linux

---

## 🚀 How to run

### On a Mac (easiest)
1. Open the `stylebot` folder in Finder.
2. Double-click **`run_on_mac.command`**.
   - First time only: macOS may say it "cannot be opened". **Right-click** the file → **Open** → **Open**.
3. A Terminal window opens with StyleBot running.

### From the Terminal (Mac, Linux or Windows)
1. Check you have **Python 3.8 or newer**:
   ```bash
   python3 --version
   ```
   On Windows use `python` instead of `python3`. If it's missing, install it from [python.org](https://www.python.org/downloads/) (on Windows, tick **"Add Python to PATH"**). On a Mac, running `python3` the first time may offer to install the Command Line Tools; click **Install**.
2. Go to the project folder and run:
   ```bash
   cd path/to/stylebot
   python3 stylebot.py
   ```

### Using it
Type the **number** of your choice and press **Enter**. Press **Ctrl+C** at any time to quit.

---

## 📸 Example session

```
What's the occasion?
  1. Wedding
  2. Haldi / Mehendi
  3. Festival (Diwali, Eid, Navratri...)
  ...
> 1

What type of clothes? (popular for this event: Ethnic, Fusion)
  1. Ethnic
  ...
> 1

Shopping for?
  1. Men
  2. Women
> 2

Favourite colour? (press Enter and I'll pick one): mustard
Total budget in ₹ (e.g. 3000): 5000

====================================================
 ✨ Your look: Wedding
    Ethnic · Women · Mustard · budget ₹5,000
====================================================

 👕 Clothing
    1. mustard lehenga choli            ~₹2,000
    2. net dupatta                      ~₹1,000

 👟 Footwear
    3. embellished juttis               ~₹1,250

 💍 Accessories
    4. statement jhumkas                ~₹200
    5. bangles                          ~₹200
    6. potli bag                        ~₹200
    7. maang tikka                      ~₹150

 💡 Tip: Avoid wearing white or all-black to Indian weddings; rich jewel tones photograph best.

What next?
  1-7 = shopping links for that item
  a = links for every item
  e = export as a shopping list (Markdown file)
  n = show another colour   s = save this look
  b = back to main menu
> 1

🛍  Shop 'mustard lehenga choli' (aim for about ₹2,000):
   Myntra         https://www.myntra.com/women-mustard-lehenga-choli?rawQuery=women%20mustard%20lehenga%20choli
   Ajio           https://www.ajio.com/search/?text=women%20mustard%20lehenga%20choli
   Amazon.in      https://www.amazon.in/s?k=women+mustard+lehenga+choli
   Nykaa Fashion  https://www.nykaafashion.com/catalogsearch/result/?q=women%20mustard%20lehenga%20choli
Open these in your browser? (y/n): y
Opened in your browser.
```

---

## 🧪 Running the tests

```bash
python3 -m unittest discover -v tests
```
19 unit tests cover budget parsing, rupee formatting, every occasion/style/gender combination, budget totals and shopping links. They also run automatically on GitHub (macOS, Windows, Linux) on every push; see the **Actions** tab.

---

## ⚙️ How it works

1. **Occasion → dress level.** Each occasion is tagged *dressy*, *smart* or *relaxed*, with a colour palette and a tip (`EVENTS` in the code).
2. **Style + gender + level → outfit.** `LOOKS` holds 30 outfit templates (5 styles × 2 genders × 3 levels). The last item in each is the footwear.
3. **Accessories** come from `ACCESSORIES` (ethnic or western family) plus extras for the occasion.
4. **Budget** is split 60% clothing, 25% footwear, 15% accessories, rounded down to neat amounts with the leftover handed out so the total matches exactly (`split_budget`).
5. **Links** are built from templates in `SITES`. StyleBot doesn't scrape websites: shopping sites block scrapers and change their pages often, while search links keep working and need no API keys.

## 🛠️ Customising

Everything lives in dictionaries at the top of `stylebot.py`:
- Add an occasion: add an entry to `EVENTS`
- Change an outfit: edit `LOOKS`
- Add a shopping site: add a line to `SITES` with its search URL, using `{q}` where the search text goes

## 📁 Project structure

```
stylebot/
├── stylebot.py              # the app
├── run_on_mac.command       # double-click launcher for macOS
├── tests/
│   └── test_stylebot.py     # unit tests
├── .github/workflows/
│   └── tests.yml            # runs tests on GitHub
├── README.md                # this file
├── DEBUG_LOG.md             # bugs found and how AI helped fix them
├── CHANGELOG.md             # version history
├── LICENSE                  # MIT license
└── .gitignore               # keeps your saved looks and lists out of Git
```
Saved looks go in `saved_looks.json` and exported lists in `shopping_lists/`. Both are created next to the script and ignored by Git.

---

## 🤖 How AI was used

| Step | What happened |
|---|---|
| 1. Generate | Asked an AI assistant for a console script that suggests outfits and shopping links |
| 2. Test & debug | Tried tricky inputs; the first version crashed on `₹3,000`, `0`, `9` and blank colours. Tracebacks were given to the AI, which explained and fixed them |
| 3. Improve | Asked the AI to make outfits depend on the occasion and add accessories, budget split, more sites and saving |
| 4. Debug again | Found a crash on Windows consoles (emoji/₹) and an unrealistic budget split |
| 5. Test properly | Asked the AI to write unit tests, which **caught two more bugs** (`Rs. 3000` rejected; prices exceeding the budget) |
| 6. Extend | New occasions, delete, export, gender-aware search, Mac launcher, automated tests on GitHub |
| 7. Document | Asked the AI to write this README, the changelog and the debug log |

See every step with `git log` (or the **History** tab in GitHub Desktop), and the details in [DEBUG_LOG.md](DEBUG_LOG.md).

## ⚠️ Limitations

- Suggestions come from built-in rules, not live trends or your body type
- Links open a site's search results; prices and stock are whatever the site shows
- If a shopping site changes its search URL, update that line in `SITES`

## 📄 License

MIT. See [LICENSE](LICENSE).
