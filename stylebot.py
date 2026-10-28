"""
StyleBot - a console outfit helper.
Tell it the event and the style you want, and it suggests an outfit
with accessories and gives shopping links.
"""

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
    "Myntra": "https://www.myntra.com/",
    "Amazon": "https://www.amazon.in/s?k=",
    "Ajio": "https://www.ajio.com/search/?text=",
}


def choose(prompt, options):
    print(prompt)
    for i, option in enumerate(options, 1):
        print(f"  {i}. {option}")
    choice = input("> ")
    return options[int(choice) - 1]


def make_link(site, item):
    return SITES[site] + item.replace(" ", "+")


def main():
    print("=== StyleBot ===")
    event = choose("What's the event?", EVENTS)
    style = choose("What style?", STYLES)
    gender = choose("For?", GENDERS)
    color = input("Preferred colour: ")
    budget = int(input("Budget in Rs: "))

    items = [i.format(color=color) for i in LOOKS[style][gender]]
    items += ACCESSORIES[gender]

    print(f"\nYour look for {event} ({style}, {gender}), budget Rs {budget}:")
    for item in items:
        print(f"- {item}")
        for site in SITES:
            print(f"    {site}: {make_link(site, item)}")


if __name__ == "__main__":
    main()
