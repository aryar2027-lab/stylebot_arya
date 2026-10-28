# 👗 StyleBot: Outfit & Accessory Finder 👔

A Python console app that automates an everyday decision: **"What should I wear?"**

Tell StyleBot the **event** you're dressing for and the **type of clothes** you want. It suggests a complete outfit with footwear and matching **accessories**, splits your **budget in ₹** across the items, and gives you search links to shop each piece on **Myntra, Ajio, Amazon.in, Nykaa Fashion, Zara and H&M**. It can even open them in your browser.

> Built for **Mini-Project 2: Programming**. The code was generated with an AI assistant, debugged with AI help (see [DEBUG_LOG.md](DEBUG_LOG.md)), and this README was AI-generated too. The Git history shows each step.

---

## ✨ Features

- **7 occasions:** Wedding, Festival (Diwali/Eid/Navratri), Party, Interview/Office, College/Casual, Date, Beach/Vacation
- **5 styles:** Ethnic, Formal, Casual, Western, Fusion, for Men or Women
- **Event-aware outfits:** a wedding gets a silk kurta and nehru jacket; a beach trip gets linen; an interview gets a blazer. Each event has its own dress level, colour palette and styling tip
- **Accessories** matched to the look (jhumkas and potli bag for ethnic, watch and belt for formal, sunglasses and a hat for the beach…)
- **Budget split:** your ₹ budget is divided across items (main garment gets the most), shown with Indian formatting like ₹1,25,000
- **Shopping links** for 6 sites, opened in your browser if you want. Zara and H&M are skipped for ethnic wear they don't stock
- **No colour in mind?** StyleBot picks one that suits the event; press `n` to see another colour
- **Save looks** and view them later
- Gentle **warning** if your chosen style is unusual for the event (e.g. casual wear to an interview)
- **No installation needed:** only Python's standard library

---

## 🚀 How to run

### 1. Install Python
You need **Python 3.8 or newer**. Check with:
```bash
python --version
```
(On macOS/Linux, use `python3` instead of `python` if needed.) Download it from [python.org](https://www.python.org/downloads/) if you don't have it; on Windows, tick **"Add Python to PATH"** during setup.

### 2. Get the code
```bash
git clone https://github.com/<your-username>/stylebot.git
cd stylebot
```
Or on GitHub click **Code → Download ZIP** and extract it.

### 3. Run it
```bash
python stylebot.py
```

### 4. Follow the prompts
Type the **number** of your choice and press **Enter**. Press **Ctrl+C** at any time to quit.

---

## 📸 Example session

```
Main menu
  1. Style me for an event
  2. View saved looks
  3. Exit
> 1

What's the occasion?
  1. Wedding
  2. Festival (Diwali, Eid, Navratri...)
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

Favourite colour? (press Enter and I'll pick one):
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
    7. maang tikka                      ~₹200

 💡 Tip: Avoid wearing white or all-black to Indian weddings; rich jewel tones photograph best.

What next?
  1-7 = shopping links for that item
  a = links for every item
  n = show another colour   s = save this look
  b = back to main menu
> 1

🛍  Shop 'mustard lehenga choli' (aim for about ₹2,000):
   Myntra         https://www.myntra.com/mustard-lehenga-choli?rawQuery=mustard%20lehenga%20choli
   Ajio           https://www.ajio.com/search/?text=mustard%20lehenga%20choli
   Amazon.in      https://www.amazon.in/s?k=mustard+lehenga+choli
   Nykaa Fashion  https://www.nykaafashion.com/catalogsearch/result/?q=mustard%20lehenga%20choli
Open these in your browser? (y/n): y
Opened in your browser.
```

---

## ⚙️ How it works

1. **Event → dress level.** Each event is tagged *dressy*, *smart* or *relaxed*, plus a colour palette and a tip (`EVENTS` in the code).
2. **Style + gender + level → outfit.** `LOOKS` holds 30 outfit templates (5 styles × 2 genders × 3 levels). The last item in each is the footwear.
3. **Accessories** come from `ACCESSORIES` (ethnic or western family) plus extras for the event.
4. **Budget** is split 60% clothing, 25% footwear, 15% accessories, rounded to the nearest ₹50.
5. **Links** are built from templates in `SITES`. StyleBot doesn't scrape websites: shopping sites block scrapers and change their pages often, while search links keep working and need no API keys.

## 🛠️ Customising

Everything lives in easy-to-edit dictionaries at the top of `stylebot.py`:
- Add an event: add an entry to `EVENTS`
- Change an outfit: edit `LOOKS`
- Add a shopping site: add a line to `SITES` with its search URL, using `{q}` where the search text goes

## 📁 Project structure

```
stylebot/
├── stylebot.py       # the app
├── README.md         # this file
├── DEBUG_LOG.md      # bugs found and how AI helped fix them
├── LICENSE           # MIT license
└── .gitignore        # keeps saved_looks.json out of Git
```
Saved looks are stored in `saved_looks.json` next to the script (created when you first save).

## 🤖 How AI was used

| Step | What happened |
|---|---|
| 1. Generate | Asked an AI assistant for a console script that suggests outfits and shopping links |
| 2. Test & debug | Tried tricky inputs; the first version crashed on `₹3,000`, `0`, `9` and blank colours. Tracebacks were given to the AI, which explained and fixed them |
| 3. Improve | Asked the AI to make outfits depend on the event and add accessories, budget split, more sites and saving |
| 4. Debug again | Found a crash on Windows consoles (emoji/₹) and an unrealistic budget split; fixed with AI |
| 5. Document | Asked the AI to write this README and the debug log |

See every step with `git log`, and the details in [DEBUG_LOG.md](DEBUG_LOG.md).

## ⚠️ Limitations

- Suggestions come from built-in rules, not live trends or your body type
- Links open a site's search results; prices and stock are whatever the site shows
- If a shopping site changes its search URL, update that line in `SITES`

## 📄 License

MIT. See [LICENSE](LICENSE).
