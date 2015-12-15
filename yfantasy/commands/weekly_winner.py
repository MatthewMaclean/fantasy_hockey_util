import importlib
from os.path import join, dirname
from xml.etree import ElementTree
yahooapi = importlib.import_module("yfantasy.python-yahooapi.yahooapi")


GAME_KEY = "nhl"
TEAM_ID = "60802"
URL_BASE = "http://fantasysports.yahooapis.com/fantasy/v2/league/%s.l.%s/" % \
    (GAME_KEY, TEAM_ID)
TAG_PREFIX = "{http://fantasysports.yahooapis.com/fantasy/v2/base.rng}"

GOALIE_CATEGORIES = ["19", "23", "26", "27"]

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


def category_winners(people_points, max_order, excluded_people=[]):
    people = []
    max_set = False
    max_value = 0

    for k, v in people_points.iteritems():
        if k in excluded_people:
            continue

        v = float(v)
        if not max_set:
            max_set = True
            max_value = v
            people = [k]
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

def get_teams(xml, prefix):
    teams = []

    root = ElementTree.fromstring(xml)
    for elem in root.iter("%steam" % prefix):
        name = get_element(elem, "name", prefix).text
        teams.append(name)

    return teams


def team_weekly_wins(team_list, excluded_goalie_people, comparison_dictionary, goalie_categories, stats_dictionary=None):
    team_counts = {}

    for k, v in team_list.iteritems():
        if k in goalie_categories:
            winners = category_winners(v, comparison_dictionary[k], excluded_goalie_people)
        else:
            winners = category_winners(v, comparison_dictionary[k])

        if stats_dictionary:
            print winners[1], stats_dictionary[k], winners[0]

        for team in winners[0]:
            if team in team_counts:
                team_counts[team] += 1
            else:
                team_counts[team] = 1

    return team_counts


def get_excluced_goalie_people(teams):
    excluded_teams = []

    while(1):
        for (i, team) in enumerate(teams):
            print "[%s] - %s" % (i, team)

        print ""
        print "Currently Excluded Teams: %s" % (", ".join(map(str, excluded_teams)))
        print "(number to select, x to quit)"
        exclude = raw_input("Which player did not get enough goalie showings? ")

        if exclude == "x":
            return excluded_teams

        try:
            team = teams[int(exclude)]
            excluded_teams.append(team)
            teams.remove(team)
        except ValueError:
            print "Invalid option %s. Please enter an integer or 'x'" % exclude



def weekly_winner():
    api = yahooapi.YahooAPI(
        keyfile=join(dirname(__file__), '../../auth'),
        tokenfile=join(dirname(__file__), '../../token'))
    week = raw_input("Which week do you want the scoreboard for? ")

    response = api.request("%sscoreboard;week=%s" % (URL_BASE, week))

    results = parse_api_response(response.content, TAG_PREFIX)

    response2 = api.request("%steams" % (URL_BASE))
    teams = get_teams(response2.content, TAG_PREFIX)

    excluded_goalie_people = get_excluced_goalie_people(teams)

    print ""
    print "Scoreboard for Week %s" % (week)
    print ""
    team_counts = team_weekly_wins(results, excluded_goalie_people, COMPARISON, GOALIE_CATEGORIES, STATS)

    print "Final Winners"
    total_winner = category_winners(team_counts, True)
    print total_winner[1], "points", total_winner[0]
