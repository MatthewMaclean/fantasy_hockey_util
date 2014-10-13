from unittest2 import TestCase
from yfantasy.commands.weekly_winner import (
    category_winners,
    parse_api_response,
    team_weekly_wins)


class WeeklyWinnerTest(TestCase):
    def test_winner_single(self):
        inp = {"A": 5}
        self.assertEqual(0, cmp(category_winners(inp, True), [["A"], 5]))

    def test_winner_two(self):
        inp = {"A": 5, "B": 5}
        self.assertEqual(0, cmp(category_winners(inp, True), [["A", "B"], 5]))

    def test_winner_replace(self):
        inp = {"A": 5, "B": 6}
        self.assertEqual(0, cmp(category_winners(inp, True), [["B"], 6]))

    def test_winner_string_bug(self):
        inp = {"A": "11", "B": "9"}
        self.assertEqual(0, cmp(category_winners(inp, True), [["A"], 11]))

    def test_winner_reverse_replace(self):
        inp = {"A": 5, "B": 4}
        self.assertEqual(0, cmp(category_winners(inp, False), [["B"], 4]))

    def test_xml_parse(self):
        inp = """
            <root>
                <random>
                    <team>
                        <name>A</name>
                        <stats>
                            <stat>
                                <stat_id>1</stat_id>
                                <value>1</value>
                            </stat>
                            <stat>
                                <stat_id>2</stat_id>
                                <value>2</value>
                            </stat>
                        </stats>
                    </team>
                    <team>
                        <name>B</name>
                        <stats>
                            <stat>
                                <stat_id>1</stat_id>
                                <value>3</value>
                            </stat>
                            <stat>
                                <stat_id>2</stat_id>
                                <value>4</value>
                            </stat>
                        </stats>
                    </team>
                </random>
                <random>
                    <team>
                        <name>C</name>
                        <stats>
                            <stat>
                                <stat_id>1</stat_id>
                                <value>5</value>
                            </stat>
                            <stat>
                                <stat_id>2</stat_id>
                                <value>6</value>
                            </stat>
                        </stats>
                    </team>
                </random>
            </root>"""
        expected = {
            "1": {
                "A": "1",
                "B": "3",
                "C": "5",
            },
            "2": {
                "A": "2",
                "B": "4",
                "C": "6",
            },
            "4": {},
            "5": {},
            "8": {},
            "14": {},
            "31": {},
            "19": {},
            "23": {},
            "26": {},
            "27": {}
        }
        self.assertEqual(
            0,
            len(set(expected) ^ set(parse_api_response(inp, "")))
        )

    def test_weekly_wins(self):
        inp = {
            "1": {
                "A": "1",
                "B": "3",
                "C": "5",
            },
            "2": {
                "A": "2",
                "B": "4",
                "C": "6",
            },
            "3": {
                "A": "4",
                "B": "2",
                "C": "1",
            }
        }
        conversion_array = {
            "1": True,
            "2": False,
            "3": True,
        }
        expected = {
            "A": 1,
            "C": 2,
        }
        self.assertEqual(
            0,
            len(set(expected) ^ set(team_weekly_wins(inp, conversion_array)))
        )
