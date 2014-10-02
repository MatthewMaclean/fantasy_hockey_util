from yfantasy.parser import build_parser
from yfantasy.commands.weekly_winner import weekly_winner


OPTIONS = {
    'command': str,
}


COMMANDS = {
    'weekly_winner': weekly_winner,
}


def main():
    parser = build_parser(OPTIONS)

    (opt, args) = parser.parse_known_args()

    if opt.command not in COMMANDS:
        return

    COMMANDS[opt.command](args)
    return 0
