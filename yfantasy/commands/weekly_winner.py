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


def get_element(elem, name):
    # find wasn't working
    r = elem.findall("%s%s" % (TAG_PREFIX, name))
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

    return people


def weekly_winner(args):
    results = {}
    team_counts = {}

    for i in STATS:
        results[i] = {}

    api = yahooapi.YahooAPI(join(dirname(__file__), '../../auth'))
    week = raw_input("Which week do you want the scoreboard for? ")

    response = api.request("%sscoreboard;week=%s" % (URL_BASE, week))

    root = ElementTree.fromstring(response.content)
    for elem in root.iter("%steam" % TAG_PREFIX):
        name = get_element(elem, "name").text

        for stat in elem.iter("%sstat" % TAG_PREFIX):
            stat_id = get_element(stat, "stat_id").text
            value = get_element(stat, "value").text

            if stat_id in STATS:
                results[stat_id][name] = value

    for k, v in results.iteritems():
        winners = category_winners(v, COMPARISON[k])
        print STATS[k], winners

        for team in winners:
            if team in team_counts:
                team_counts[team] += 1
            else:
                team_counts[team] = 1

    print "Final Winners"
    print category_winners(team_counts, True)

    print "DEBUG"
    print results
    print team_counts
