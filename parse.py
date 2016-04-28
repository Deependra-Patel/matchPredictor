import os, yaml
from classes import Batsman, Bowler, Team
from os import listdir
from os.path import isfile, join

batsmen = {}
bowlers = {}
teams = {}

def process_deliveries(deliveries, batting_team, bowling_team):
    for delivery in deliveries:
        for key, value in delivery.items():
            batsman = value["batsman"]
            bowler = value["bowler"]
            batsman_runs = value["runs"]["batsman"]
            total_runs = value["runs"]["total"]
            teams[batting_team].runs_scored += total_runs
            teams[batting_team].balls_faced += 1
            teams[bowling_team].runs_conceded += total_runs
            teams[bowling_team].balls_bowled += 1
            if batsman not in batsmen:
                batsmen[batsman] = Batsman(batsman, 0, 0, 0, 0, 0)
            batsmen[batsman].balls += 1
            batsmen[batsman].runs += batsman_runs
            if bowler not in bowlers:
                bowlers[bowler] = Bowler(bowler, 0, 0, 0, 0, 0, 0, 0)
            bowlers[bowler].balls += 1
            bowlers[bowler].runs += total_runs


def parse_file(file_name):
    with open(file_name, 'r') as f:
        info = yaml.load(f)
    try:
        if info["info"]["gender"] != "male":
            return
        team1 = info["info"]["teams"][0]
        team2 = info["info"]["teams"][1]
        if "result" in info["info"]["outcome"] and info["info"]["outcome"]["result"] == "no result":
            return
        if "winner" not in info["info"]["outcome"] :
            winner = -1
        else :
            winner = info["info"]["outcome"]["winner"]
        if team1 not in teams :
            teams[team1] = Team(team1, 0, 0, 0, 0, 0, 0)
        if team2 not in teams :
            teams[team2] = Team(team2, 0, 0, 0, 0, 0, 0)
        teams[team1].matches += 1
        teams[team2].matches += 1
        if winner != -1:
            teams[winner].wins += 1
        else :
            teams[team1].wins += 0.5
            teams[team2].wins += 0.5
        deliveries = info["innings"][0]["1st innings"]["deliveries"] + info["innings"][1]["2nd innings"]["deliveries"]
        if (info["innings"][0]["1st innings"]["team"] == team1) :
            process_deliveries(info["innings"][0]["1st innings"]["deliveries"], team1, team2)
            process_deliveries(info["innings"][1]["2nd innings"]["deliveries"], team2, team1)
        else :
            process_deliveries(info["innings"][0]["1st innings"]["deliveries"], team2, team1)
            process_deliveries(info["innings"][1]["2nd innings"]["deliveries"], team1, team2)
    except Exception as e:
        print("Error: ", e)
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)

match_files = [f for f in listdir('data/odis/') if isfile(join('data/odis/', f)) and f[-5:] == '.yaml']

def main():
    ind = 0
    for filename in match_files:
        print filename, ind
        parse_file("data/odis/"+filename)
        ind += 1
        if ind % 10 == 0:
            print ind
    batsmen_file = open("batsmen", "w+")
    for batsman in batsmen:
        print >>batsmen_file, batsmen[batsman].export()
    bowler_file = open("bowlers", "w+")
    for bowler in bowlers:
        print >>bowler_file, bowlers[bowler].export()
    teams_file = open("teams", "w+")
    for team in teams:
        print >>teams_file, teams[team].export()

main()
