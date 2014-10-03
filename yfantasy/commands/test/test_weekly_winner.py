from unittest2 import TestCase
from yfantasy.commands.weekly_winner import category_winners


class WeeklyWinnerTest(TestCase):
    def test_winner_single(self):
        inp = {"A": 5}
        self.assertEqual(0, cmp(category_winners(inp, True), ["A"]))

    def test_winner_two(self):
        inp = {"A": 5, "B": 5}
        self.assertEqual(0, cmp(category_winners(inp, True), ["A", "B"]))

    def test_winner_replace(self):
        inp = {"A": 5, "B": 6}
        self.assertEqual(0, cmp(category_winners(inp, True), ["B"]))

    def test_winner_reverse_replace(self):
        inp = {"A": 5, "B": 4}
        self.assertEqual(0, cmp(category_winners(inp, False), ["B"]))
