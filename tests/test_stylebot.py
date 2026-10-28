"""Unit tests for StyleBot.

Run from the project folder with:
    python3 -m unittest discover tests
"""

import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import stylebot  # noqa: E402


class TestRupees(unittest.TestCase):
    def test_small_numbers(self):
        self.assertEqual(stylebot.rupees(0), "₹0")
        self.assertEqual(stylebot.rupees(999), "₹999")

    def test_indian_grouping(self):
        self.assertEqual(stylebot.rupees(1000), "₹1,000")
        self.assertEqual(stylebot.rupees(125000), "₹1,25,000")
        self.assertEqual(stylebot.rupees(10000000), "₹1,00,00,000")


class TestParseBudget(unittest.TestCase):
    def test_plain_number(self):
        self.assertEqual(stylebot.parse_budget("3000"), 3000)

    def test_symbols_and_commas(self):
        self.assertEqual(stylebot.parse_budget("₹3,000"), 3000)
        self.assertEqual(stylebot.parse_budget("Rs 3000"), 3000)
        self.assertEqual(stylebot.parse_budget("3000 rupees"), 3000)

    def test_rs_with_dot(self):
        # Many people write "Rs." with a full stop
        self.assertEqual(stylebot.parse_budget("Rs. 3000"), 3000)
        self.assertEqual(stylebot.parse_budget("Rs.3,000"), 3000)

    def test_decimals_are_dropped(self):
        self.assertEqual(stylebot.parse_budget("3000.50"), 3000)

    def test_invalid(self):
        self.assertIsNone(stylebot.parse_budget(""))
        self.assertIsNone(stylebot.parse_budget("lots"))
        self.assertIsNone(stylebot.parse_budget("50"))  # below minimum


class TestBuildLook(unittest.TestCase):
    def test_every_combination_builds(self):
        for event in stylebot.EVENTS:
            for style in stylebot.STYLES:
                for gender in stylebot.GENDERS:
                    look = stylebot.build_look(event, style, gender, "red", 3000)
                    self.assertTrue(look["items"], f"empty look: {event}/{style}/{gender}")

    def test_event_changes_outfit(self):
        wedding = stylebot.build_look("Wedding", "Ethnic", "Men", "red", 3000)
        beach = stylebot.build_look("Beach / Vacation", "Ethnic", "Men", "red", 3000)
        self.assertNotEqual(
            [i["name"] for i in wedding["items"]], [i["name"] for i in beach["items"]]
        )

    def test_blank_colour_has_no_extra_spaces(self):
        look = stylebot.build_look("Wedding", "Ethnic", "Men", "", 3000)
        for item in look["items"]:
            self.assertEqual(item["name"], item["name"].strip())
            self.assertNotIn("  ", item["name"])

    def test_total_never_exceeds_budget(self):
        for budget in (500, 999, 2500, 3000, 5000, 12345, 125000):
            for style in stylebot.STYLES:
                for gender in stylebot.GENDERS:
                    look = stylebot.build_look("Wedding", style, gender, "red", budget)
                    total = sum(i["price"] for i in look["items"])
                    self.assertLessEqual(total, budget, f"{style}/{gender} at {budget}")

    def test_style_warning(self):
        look = stylebot.build_look("Interview / Office", "Casual", "Women", "navy", 3000)
        self.assertIsNotNone(look["warning"])
        look = stylebot.build_look("Interview / Office", "Formal", "Women", "navy", 3000)
        self.assertIsNone(look["warning"])


class TestLinks(unittest.TestCase):
    def test_links_are_url_encoded(self):
        url = stylebot.make_link("Ajio", "maroon silk kurta")
        self.assertNotIn(" ", url)
        self.assertIn("maroon%20silk%20kurta", url)

    def test_myntra_uses_dashes(self):
        self.assertIn("myntra.com/maroon-silk-kurta", stylebot.make_link("Myntra", "maroon silk kurta"))

    def test_ethnic_clothing_skips_zara_and_hm(self):
        item = {"name": "red lehenga choli", "ethnic": True}
        sites = [site for site, _ in stylebot.links_for(item)]
        self.assertNotIn("Zara", sites)
        self.assertNotIn("H&M", sites)
        self.assertIn("Myntra", sites)

    def test_search_includes_gender(self):
        look = stylebot.build_look("Date", "Western", "Women", "red", 3000)
        for _, url in stylebot.links_for(look["items"][0]):
            self.assertIn("women", url)

    def test_old_saved_looks_without_search_field_still_work(self):
        links = stylebot.links_for({"name": "black blazer", "ethnic": False})
        self.assertIn("black", links[0][1])

    def test_western_items_use_all_sites(self):
        item = {"name": "black blazer", "ethnic": False}
        self.assertEqual(len(stylebot.links_for(item)), len(stylebot.SITES))


class TestExport(unittest.TestCase):
    def test_safe_filename_removes_slashes(self):
        self.assertEqual(stylebot.safe_filename("Graduation / Convocation"), "graduation-convocation")
        self.assertNotIn("/", stylebot.safe_filename("Party / Night out red"))


if __name__ == "__main__":
    unittest.main()
