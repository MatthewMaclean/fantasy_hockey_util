from unittest2 import TestCase
from yfantasy.commands.weekly_winner import (
    category_winners,
    parse_api_response)


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
