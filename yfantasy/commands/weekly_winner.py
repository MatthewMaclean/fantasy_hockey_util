import importlib
from os.path import join, dirname
from xml.etree import ElementTree
yahooapi = importlib.import_module("yfantasy.python-yahooapi.yahooapi")


GAME_KEY = "341"
TEAM_ID = "30872"
URL_BASE = "http://fantasysports.yahooapis.com/fantasy/v2/league/%s.l.%s/" % \
    (GAME_KEY, TEAM_ID)
TAG_PREFIX = "{http://fantasysports.yahooapis.com/fantasy/v2/base.rng}"
STATS = {
    "1": "G",
    "2": "A",
    "4": "+/-",
    "5": "PIM",
    "8": "PPP",
    "14": "SOG",
    "31": "HIT",
    "19": "W",
    "23": "GAA",
    "26": "SV%",
    "27": "SHO"}

COMPARISON = {
    "1": True,
    "2": True,
    "4": True,
    "5": True,
    "8": True,
    "14": True,
    "31": True,
    "19": True,
    "23": False,
    "26": True,
    "27": True}


def get_element(elem, name, prefix):
    # find wasn't working
    r = elem.findall("%s%s" % (prefix, name))
    return r[0]


def category_winners(people_points, max_order):
    people = []
    max_set = False
    max_value = 0

    for k, v in people_points.iteritems():
        if not max_set:
            max_set = True
            max_value = v
            people.append(k)
        elif max_order and v > max_value or not max_order and v < max_value:
            people = [k]
            max_value = v
        elif v == max_value:
            people.append(k)

    return [people, max_value]


def parse_api_response(xml, prefix):
    results = {}

    for i in STATS:
        results[i] = {}

    root = ElementTree.fromstring(xml)
    for elem in root.iter("%steam" % prefix):
        name = get_element(elem, "name", prefix).text

        for stat in elem.iter("%sstat" % prefix):
            stat_id = get_element(stat, "stat_id", prefix).text
            value = get_element(stat, "value", prefix).text

            if stat_id in STATS and value is not None:
                results[stat_id][name] = value

    return results


def team_weekly_wins(team_list, comparison_dictionary, stats_dictionary=None):
    team_counts = {}
    print ""

    for k, v in team_list.iteritems():
        winners = category_winners(v, comparison_dictionary[k])
        if stats_dictionary:
            print winners[1], stats_dictionary[k], winners[0]

        for team in winners[0]:
            if team in team_counts:
                team_counts[team] += 1
            else:
                team_counts[team] = 1

    return team_counts


def weekly_winner(args):
    api = yahooapi.YahooAPI(join(dirname(__file__), '../../auth'))
    week = raw_input("Which week do you want the scoreboard for? ")

    response = api.request("%sscoreboard;week=%s" % (URL_BASE, week))

    results = parse_api_response(response.content, TAG_PREFIX)

    team_counts = team_weekly_wins(results, COMPARISON, STATS)

    print "Final Winners"
    total_winner = category_winners(team_counts, True)
    print total_winner[1], "points", total_winner[0]
