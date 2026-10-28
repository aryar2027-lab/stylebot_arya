"""
StyleBot - a console outfit helper.
Tell it the event and the style you want, and it suggests an outfit
with accessories and gives shopping links.
"""

import re
from urllib.parse import quote, quote_plus

EVENTS = ["Wedding", "Festival", "Party", "Interview", "Casual day out", "Date", "Beach trip"]
STYLES = ["Ethnic", "Formal", "Casual", "Western"]
GENDERS = ["Men", "Women"]

LOOKS = {
    "Ethnic": {
        "Men": ["{color} kurta", "white churidar", "mojaris"],
        "Women": ["{color} anarkali suit", "embroidered dupatta", "juttis"],
    },
    "Formal": {
        "Men": ["{color} blazer", "white formal shirt", "black trousers", "oxford shoes"],
        "Women": ["{color} blazer", "silk blouse", "straight trousers", "block heels"],
    },
    "Casual": {
        "Men": ["{color} t-shirt", "blue jeans", "white sneakers"],
        "Women": ["{color} top", "mom jeans", "white sneakers"],
    },
    "Western": {
        "Men": ["{color} shirt", "chinos", "loafers"],
        "Women": ["{color} midi dress", "heels"],
    },
}

ACCESSORIES = {
    "Men": ["watch", "belt", "sunglasses"],
    "Women": ["earrings", "handbag", "bracelet"],
}

SITES = {
    "Myntra": "https://www.myntra.com/{slug}?rawQuery={q}",
    "Amazon": "https://www.amazon.in/s?k={qp}",
    "Ajio": "https://www.ajio.com/search/?text={q}",
}


def choose(prompt, options):
    print(prompt)
    for i, option in enumerate(options, 1):
        print(f"  {i}. {option}")
    # Bug fix: "0" silently returned the LAST option (options[-1]),
    # and letters / out-of-range numbers crashed the program.
    while True:
        choice = input("> ").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(options):
            return options[int(choice) - 1]
        print(f"Please enter a number from 1 to {len(options)}.")


def ask_budget():
    # Bug fix: int("₹3,000") raised ValueError. Keep only the digits.
    while True:
        digits = re.sub(r"[^0-9]", "", input("Budget in Rs: "))
        if digits and int(digits) > 0:
            return int(digits)
        print("Please enter an amount, e.g. 3000.")


def make_link(site, item):
    # Bug fix: links were not URL-encoded, and Myntra needs "a-b-c" paths
    return SITES[site].format(
        slug=quote(item.replace(" ", "-")), q=quote(item), qp=quote_plus(item)
    )


def main():
    print("=== StyleBot ===")
    event = choose("What's the event?", EVENTS)
    style = choose("What style?", STYLES)
    gender = choose("For?", GENDERS)
    color = input("Preferred colour (optional): ").strip().lower()
    budget = ask_budget()

    # Bug fix: a blank colour produced " kurta" and links like "+kurta"
    items = [" ".join(i.format(color=color).split()) for i in LOOKS[style][gender]]
    items += ACCESSORIES[gender]

    print(f"\nYour look for {event} ({style}, {gender}), budget Rs {budget}:")
    for item in items:
        print(f"- {item}")
        for site in SITES:
            print(f"    {site}: {make_link(site, item)}")


if __name__ == "__main__":
    main()
