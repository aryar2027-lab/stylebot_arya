"""
StyleBot - Outfit & Accessory Finder
====================================
A console app that helps you decide what to wear. Pick the event and the
style of clothes you want, and StyleBot suggests a complete outfit with
footwear and accessories, splits your budget across the items, and gives
search links for Indian and international shopping sites.

Uses only the Python standard library (Python 3.8+).
"""

import json
import os
import random
import re
import sys
import webbrowser
from datetime import datetime
from urllib.parse import quote, quote_plus

SAVE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "saved_looks.json")

# ---------------------------------------------------------------------------
# Data
# ---------------------------------------------------------------------------

# Each event sets how dressy the outfit should be, which colours suit it,
# which styles people usually wear, extra accessories and a styling tip.
EVENTS = {
    "Wedding": {
        "level": "dressy",
        "colours": ["maroon", "emerald green", "royal blue", "mustard", "peach"],
        "styles": ["Ethnic", "Fusion"],
        "extras": {"Men": ["silk pocket square"], "Women": ["maang tikka"]},
        "tip": "Avoid wearing white or all-black to Indian weddings; rich jewel tones photograph best.",
    },
    "Festival (Diwali, Eid, Navratri...)": {
        "level": "smart",
        "colours": ["yellow", "orange", "pink", "green", "red"],
        "styles": ["Ethnic", "Fusion"],
        "extras": {"Men": [], "Women": ["bindi"]},
        "tip": "Bright colours and comfortable footwear: festivals mean lots of standing and visiting.",
    },
    "Party / Night out": {
        "level": "dressy",
        "colours": ["black", "wine", "navy", "emerald", "silver"],
        "styles": ["Western", "Fusion", "Casual"],
        "extras": {"Men": ["cologne"], "Women": ["statement ring"]},
        "tip": "Pick one statement piece (shoes, jacket or jewellery) and keep the rest simple.",
    },
    "Interview / Office": {
        "level": "smart",
        "colours": ["navy", "charcoal grey", "white", "beige", "light blue"],
        "styles": ["Formal"],
        "extras": {"Men": ["leather laptop bag"], "Women": ["leather laptop bag"]},
        "tip": "Well-fitted and ironed beats expensive. Neutral colours keep the focus on you.",
    },
    "College / Casual day out": {
        "level": "relaxed",
        "colours": ["olive", "black", "white", "sky blue", "lavender"],
        "styles": ["Casual", "Western", "Fusion"],
        "extras": {"Men": ["backpack"], "Women": ["backpack"]},
        "tip": "Comfort first: breathable fabrics and shoes you can walk in all day.",
    },
    "Date": {
        "level": "smart",
        "colours": ["red", "black", "pastel pink", "navy", "white"],
        "styles": ["Western", "Casual", "Fusion"],
        "extras": {"Men": ["cologne"], "Women": ["perfume"]},
        "tip": "Wear something you feel confident in. Fit matters more than trends.",
    },
    "Beach / Vacation": {
        "level": "relaxed",
        "colours": ["white", "sky blue", "pastel yellow", "coral", "mint green"],
        "styles": ["Casual", "Western"],
        "extras": {"Men": ["bucket hat"], "Women": ["straw hat"]},
        "tip": "Linen and cotton keep you cool; don't forget sunscreen.",
    },
}

STYLES = ["Ethnic", "Formal", "Casual", "Western", "Fusion"]
GENDERS = ["Men", "Women"]

# LOOKS[style][gender][level] = list of clothing items.
# "{color}" is replaced by the chosen colour. The LAST item is always footwear.
LOOKS = {
    "Ethnic": {
        "Men": {
            "dressy": ["{color} silk kurta", "cream nehru jacket", "cream churidar", "embroidered mojaris"],
            "smart": ["{color} cotton kurta", "white pyjama", "kolhapuri chappals"],
            "relaxed": ["{color} linen short kurta", "white chinos", "kolhapuri sandals"],
        },
        "Women": {
            "dressy": ["{color} lehenga choli", "net dupatta", "embellished juttis"],
            "smart": ["{color} anarkali kurta set", "printed dupatta", "juttis"],
            "relaxed": ["{color} cotton kurti", "palazzo pants", "kolhapuri flats"],
        },
    },
    "Formal": {
        "Men": {
            "dressy": ["{color} two piece suit", "white formal shirt", "silk tie", "black oxford shoes"],
            "smart": ["{color} blazer", "light blue formal shirt", "grey formal trousers", "brown derby shoes"],
            "relaxed": ["{color} oxford shirt", "chinos", "loafers"],
        },
        "Women": {
            "dressy": ["{color} pantsuit", "silk camisole", "pointed pumps"],
            "smart": ["{color} blazer", "white formal shirt", "straight trousers", "block heels"],
            "relaxed": ["{color} formal shirt", "cigarette trousers", "loafers"],
        },
    },
    "Casual": {
        "Men": {
            "dressy": ["{color} printed shirt", "dark wash jeans", "white leather sneakers"],
            "smart": ["{color} polo t-shirt", "chinos", "white sneakers"],
            "relaxed": ["{color} graphic t-shirt", "cargo shorts", "slides"],
        },
        "Women": {
            "dressy": ["{color} satin top", "wide leg jeans", "strappy heels"],
            "smart": ["{color} knit top", "mom jeans", "white sneakers"],
            "relaxed": ["{color} oversized t-shirt", "denim shorts", "flat sandals"],
        },
    },
    "Western": {
        "Men": {
            "dressy": ["{color} velvet blazer", "black turtleneck", "slim fit trousers", "chelsea boots"],
            "smart": ["{color} linen shirt", "beige chinos", "loafers"],
            "relaxed": ["{color} cuban collar shirt", "linen shorts", "espadrilles"],
        },
        "Women": {
            "dressy": ["{color} satin slip dress", "strappy heels"],
            "smart": ["{color} midi dress", "block heels"],
            "relaxed": ["{color} sundress", "flat sandals"],
        },
    },
    "Fusion": {
        "Men": {
            "dressy": ["{color} bandhgala jacket", "slim fit trousers", "tan loafers"],
            "smart": ["{color} short kurta", "slim fit jeans", "loafers"],
            "relaxed": ["{color} printed short kurta", "denim jeans", "kolhapuri sandals"],
        },
        "Women": {
            "dressy": ["{color} indo western gown", "embellished heels"],
            "smart": ["{color} long kurta", "dhoti pants", "block heels"],
            "relaxed": ["{color} kurti", "straight jeans", "kolhapuri flats"],
        },
    },
}

# ACCESSORIES[gender][family][level]; family is "ethnic" for Ethnic/Fusion looks
ACCESSORIES = {
    "Men": {
        "ethnic": {
            "dressy": ["gold tone analog watch", "brooch", "embroidered stole"],
            "smart": ["analog watch", "kada bracelet"],
            "relaxed": ["beaded bracelet", "aviator sunglasses"],
        },
        "western": {
            "dressy": ["analog watch", "leather belt", "pocket square"],
            "smart": ["leather belt", "minimal watch"],
            "relaxed": ["sunglasses", "baseball cap"],
        },
    },
    "Women": {
        "ethnic": {
            "dressy": ["statement jhumkas", "bangles", "potli bag"],
            "smart": ["oxidised earrings", "bangles"],
            "relaxed": ["oxidised earrings", "cotton tote bag"],
        },
        "western": {
            "dressy": ["drop earrings", "clutch bag", "delicate necklace"],
            "smart": ["minimal earrings", "structured handbag", "watch"],
            "relaxed": ["sunglasses", "tote bag"],
        },
    },
}

# Search-link templates. {slug} = words-joined-by-dashes, {q} = URL-encoded
# text, {qp} = text with '+' for spaces. Edit here if a site changes its URLs.
SITES = {
    "Myntra":        {"url": "https://www.myntra.com/{slug}?rawQuery={q}", "ethnic": True},
    "Ajio":          {"url": "https://www.ajio.com/search/?text={q}", "ethnic": True},
    "Amazon.in":     {"url": "https://www.amazon.in/s?k={qp}", "ethnic": True},
    "Nykaa Fashion": {"url": "https://www.nykaafashion.com/catalogsearch/result/?q={q}", "ethnic": True},
    "Zara":          {"url": "https://www.zara.com/in/en/search?searchTerm={q}", "ethnic": False},
    "H&M":           {"url": "https://www2.hm.com/en_in/search-results.html?q={qp}", "ethnic": False},
}

# Share of the budget for each part of the outfit
BUDGET_SPLIT = {"clothing": 0.60, "footwear": 0.25, "accessories": 0.15}

# ---------------------------------------------------------------------------
# Input helpers
# ---------------------------------------------------------------------------


def choose(prompt, options):
    """Show a numbered menu and return the chosen option."""
    print(f"\n{prompt}")
    for i, option in enumerate(options, 1):
        print(f"  {i}. {option}")
    # Bug fix: "0" silently returned the LAST option (options[-1]),
    # and letters / out-of-range numbers crashed the program.
    while True:
        choice = input("> ").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(options):
            return options[int(choice) - 1]
        print(f"Please enter a number from 1 to {len(options)}.")


MIN_BUDGET = 100


def parse_budget(text):
    """Turn user text like '₹3,000' into an int, or return None if invalid.

    Kept separate from input() so it can be unit-tested.
    """
    # Bug fix: int("₹3,000") raised ValueError, so we pull the number out.
    # Bug fix 2: "3000.50" became 300050 - ignore the paise part.
    # Bug fix 3: "Rs. 3000" was rejected because we cut at the FIRST "."
    # (the one in "Rs."). Now we look for the number itself instead.
    match = re.search(r"\d[\d,]*", text)
    if not match:
        return None
    amount = int(match.group().replace(",", ""))
    return amount if amount >= MIN_BUDGET else None


def ask_budget():
    """Ask for a budget in rupees; accepts '3000', '₹3,000', 'Rs 3000'."""
    while True:
        budget = parse_budget(input("\nTotal budget in ₹ (e.g. 3000): "))
        if budget is not None:
            return budget
        print(f"Please enter an amount of at least ₹{MIN_BUDGET}.")


def rupees(amount):
    """Format a number the Indian way: 125000 -> ₹1,25,000."""
    s = str(int(amount))
    if len(s) > 3:
        head, tail = s[:-3], s[-3:]
        head = re.sub(r"(\d)(?=(\d\d)+$)", r"\1,", head)
        s = f"{head},{tail}"
    return f"₹{s}"


# ---------------------------------------------------------------------------
# Outfit logic
# ---------------------------------------------------------------------------


def build_look(event, style, gender, colour, budget):
    """Return a dict describing the outfit, with a price guide per item."""
    info = EVENTS[event]
    level = info["level"]
    family = "ethnic" if style in ("Ethnic", "Fusion") else "western"

    clothes = LOOKS[style][gender][level]
    # Bug fix: a blank colour produced " kurta" and links like "+kurta"
    clothes = [" ".join(item.format(color=colour).split()) for item in clothes]
    footwear = clothes[-1]
    clothing = clothes[:-1]

    accessories = ACCESSORIES[gender][family][level] + info["extras"][gender]
    accessories = list(dict.fromkeys(accessories))  # remove duplicates, keep order

    items = []
    for group, names in (("clothing", clothing), ("footwear", [footwear]), ("accessories", accessories)):
        # The main garment (first clothing item) gets double weight, so a
        # lehenga is budgeted more than its dupatta.
        weights = [2 if group == "clothing" and i == 0 else 1 for i in range(len(names))]
        for name, weight in zip(names, weights):
            share = budget * BUDGET_SPLIT[group] * weight / sum(weights)
            items.append({
                "name": name,
                "group": group,
                "price": int(round(share / 50) * 50) or 50,  # round to nearest ₹50
                "ethnic": family == "ethnic" and group != "accessories",
            })

    return {
        "event": event, "style": style, "gender": gender,
        "colour": colour, "budget": budget, "items": items,
        "tip": info["tip"],
        "warning": None if style in info["styles"] else
        f"{style} is unusual for this event; most people choose {' or '.join(info['styles'])}.",
    }


def make_link(site, item_name):
    # Bug fix: links were not URL-encoded, and Myntra needs "a-b-c" paths
    return SITES[site]["url"].format(
        slug=quote(item_name.replace(" ", "-")), q=quote(item_name), qp=quote_plus(item_name)
    )


def links_for(item):
    """Return (site, url) pairs; skip Zara/H&M for ethnic clothing they don't sell."""
    return [(site, make_link(site, item["name"]))
            for site, data in SITES.items() if data["ethnic"] or not item["ethnic"]]


# ---------------------------------------------------------------------------
# Display
# ---------------------------------------------------------------------------

ICONS = {"clothing": "👕", "footwear": "👟", "accessories": "💍"}


def show_look(look):
    print("\n" + "=" * 52)
    print(f" ✨ Your look: {look['event']}")
    print(f"    {look['style']} · {look['gender']} · {look['colour'].title()} · budget {rupees(look['budget'])}")
    print("=" * 52)
    current = None
    for number, item in enumerate(look["items"], 1):
        if item["group"] != current:
            current = item["group"]
            print(f"\n {ICONS[current]} {current.title()}")
        print(f"   {number:>2}. {item['name']:<32} ~{rupees(item['price'])}")
    print(f"\n 💡 Tip: {look['tip']}")
    if look["warning"]:
        print(f" ⚠️  Heads up: {look['warning']}")


def show_links(item):
    print(f"\n🛍  Shop '{item['name']}' (aim for about {rupees(item['price'])}):")
    pairs = links_for(item)
    for site, url in pairs:
        print(f"   {site:<14} {url}")
    if input("Open these in your browser? (y/n): ").strip().lower() == "y":
        for _, url in pairs:
            webbrowser.open_new_tab(url)
        print("Opened in your browser.")


# ---------------------------------------------------------------------------
# Saving
# ---------------------------------------------------------------------------


def load_saved():
    if not os.path.exists(SAVE_FILE):
        return []
    try:
        with open(SAVE_FILE, encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        print("(Saved looks file was unreadable, starting a fresh one.)")
        return []


def save_look(look):
    looks = load_saved()
    looks.append({**look, "saved_on": datetime.now().strftime("%d %b %Y, %I:%M %p")})
    with open(SAVE_FILE, "w", encoding="utf-8") as f:
        json.dump(looks, f, indent=2, ensure_ascii=False)
    print(f"Saved! You now have {len(looks)} saved look(s).")


def view_saved():
    looks = load_saved()
    if not looks:
        print("\nNo saved looks yet. Create one and press 's' to save it.")
        return
    titles = [f"{l['event']} - {l['style']}, {l['colour']} ({l['saved_on']})" for l in looks]
    look = looks[titles.index(choose("Your saved looks:", titles))]
    look_menu(look, already_saved=True)


# ---------------------------------------------------------------------------
# Main flow
# ---------------------------------------------------------------------------


def look_menu(look, already_saved=False):
    """Let the user explore one look. Returns a new colour request or None."""
    while True:
        show_look(look)
        print("\nWhat next?")
        print(f"  1-{len(look['items'])} = shopping links for that item")
        print("  a = links for every item")
        if not already_saved:
            print("  n = show another colour   s = save this look")
        print("  b = back to main menu")
        choice = input("> ").strip().lower()

        if choice.isdigit() and 1 <= int(choice) <= len(look["items"]):
            show_links(look["items"][int(choice) - 1])
        elif choice == "a":
            for item in look["items"]:
                print(f"\n {item['name']}")
                for site, url in links_for(item):
                    print(f"   {site:<14} {url}")
        elif choice == "n" and not already_saved:
            return "another"
        elif choice == "s" and not already_saved:
            save_look(look)
            already_saved = True
        elif choice == "b":
            return None
        else:
            print("Sorry, I didn't understand that.")
            continue
        input("\nPress Enter to continue...")


def style_me():
    event = choose("What's the occasion?", list(EVENTS))
    recommended = EVENTS[event]["styles"]
    style = choose(f"What type of clothes? (popular for this event: {', '.join(recommended)})", STYLES)
    gender = choose("Shopping for?", GENDERS)
    colour = input("\nFavourite colour? (press Enter and I'll pick one): ").strip().lower()
    budget = ask_budget()

    used = {colour} if colour else set()
    while True:
        if not colour:
            # Pick an event-appropriate colour we haven't shown yet
            options = [c for c in EVENTS[event]["colours"] if c not in used] or EVENTS[event]["colours"]
            colour = random.choice(options)
            used.add(colour)
        look = build_look(event, style, gender, colour, budget)
        if look_menu(look) != "another":
            return
        colour = ""  # pick a new colour on the next loop


def main():
    print("=" * 52)
    print("   👗 StyleBot · Outfit & Accessory Finder 👔")
    print("=" * 52)
    print("Tell me where you're going and I'll put together a look,")
    print("with links to shop it on Myntra, Ajio, Amazon, Nykaa, Zara & H&M.")

    while True:
        choice = choose("Main menu", ["Style me for an event", "View saved looks", "Exit"])
        if choice == "Style me for an event":
            style_me()
        elif choice == "View saved looks":
            view_saved()
        else:
            print("Happy shopping! 🛍")
            break


def fix_console_encoding():
    """Bug fix: on Windows consoles using an old code page (e.g. cp1252),
    printing emoji or '₹' crashed with UnicodeEncodeError. Switch output to
    UTF-8, and if the console still can't show a character, print '?' instead
    of crashing."""
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except (AttributeError, ValueError):
            pass  # very old Python or an unusual stream: leave it as is


if __name__ == "__main__":
    fix_console_encoding()
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        # Bug fix: Ctrl+C used to print a long traceback
        print("\nBye! 👋")
