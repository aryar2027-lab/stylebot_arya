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


if __name__ == "__main__":
    unittest.main()
