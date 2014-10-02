import importlib
from os.path import join, dirname


yahooapi = importlib.import_module("yfantasy.python-yahooapi.yahooapi")

def weekly_winner(args):
    api = yahooapi.YahooAPI(join(dirname(__file__), '../../auth'))

# TEAM_ID = "30872"
# URL_BASE = "http://hockey.fantasysports.yahoo.com/hockey/%s/" % TEAM_ID
#
# session = Session()
# cookies = chrome_cookies(URL_BASE)
# request = session.get("%smatchup?week=1&mid1=1" % URL_BASE, cookies=cookies)
# print request.text
#
# parser = YahooMatchupParser()
# parser.feed(html)
