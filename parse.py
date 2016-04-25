import os, yaml
from classes import Batsman, Bowler

batsmen = {}
bowlers = {}


def parse_file(file_name):
    with open(file_name, 'r') as f:
        info = yaml.load(f)
    try:
        if info["info"]["gender"] != "male":
            return
        deliveries = info["innings"][0]["1st innings"]["deliveries"] + info["innings"][1]["2nd innings"]["deliveries"]
        for delivery in deliveries:
            for key, value in delivery.items():
                batsman = value["batsman"]
                bowler = value["bowler"]
                batsman_runs = value["runs"]["batsman"]
                total_runs = value["runs"]["total"]
                if batsman in batsmen:
                    batsmen[batsman].balls += 1
                    batsmen[batsman].runs += batsman_runs
                else:
                    batsmen[batsman] = Batsman(batsman, 0, 0, 0, 0, 0)
                if bowler in bowlers:
                    bowlers[bowler].balls += 1
                    bowlers[bowler].runs += total_runs
                else:
                    bowlers[bowler] = Bowler(bowler, 0, 0, 0, 0, 0, 0, 0)
    except Exception as e:
        print("Error: ", e)


def main():
    # all_files = os.listdirs("data/odis")
    parse_file("data/odis/225249.yaml")
    print(batsmen)
    print(bowlers)
    # for file in all_files:
    # file = "data/odis"


main()
