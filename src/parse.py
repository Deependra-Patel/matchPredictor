import os, yaml
from classes import Batsman, Bowler, Team, Match
from os import listdir
from os.path import isfile, join
import sys

batsmen = {}
bowlers = {}
teams = {}
matches = []

def process_deliveries(deliveries, batting_team, bowling_team, innings, match):
    batsmen_set = set([])
    bowlers_set = set([])
    for delivery in deliveries:
        for key, value in delivery.items():
            batsman = value["batsman"]
            bowler = value["bowler"]
            if innings == 1 :
                if batsman not in match.batting_order_1 :
                    match.batting_order_1.append(batsman)
                if bowler not in match.bowlers_1 :
                    match.bowlers_1.append(bowler)
            elif innings == 2 :
                if batsman not in match.batting_order_2 :
                    match.batting_order_2.append(batsman)
                if bowler not in match.bowlers_2 :
                    match.bowlers_2.append(bowler)
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
            if batsman not in batsmen_set :
                batsmen_set.add(batsman)
                batsmen[batsman].matches += 1
            if bowler not in bowlers_set :
                bowlers_set.add(bowler)
                bowlers[bowler].matches += 1
    return match

def parse_file(file_name):
    with open(file_name, 'r') as f:
        info = yaml.load(f)
    try:
        if info["info"]["gender"] != "male":
            return False
        team1 = info["info"]["teams"][0]
        team2 = info["info"]["teams"][1]
        if info["info"]["toss"]["decision"] == "bat" :
            if team1 == info["info"]["toss"]["winner"] :
                match = Match(team1, team2)
            else :
                match = Match(team2, team1)
        else :
            if team2 == info["info"]["toss"]["winner"] :
                match = Match(team1, team2)
            else :
                match = Match(team2, team1)

        if "result" in info["info"]["outcome"] and info["info"]["outcome"]["result"] in ["no result", "tie"]:
            return False
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
            match = process_deliveries(info["innings"][0]["1st innings"]["deliveries"], team1, team2, 1, match)
            match = process_deliveries(info["innings"][1]["2nd innings"]["deliveries"], team2, team1, 2, match)
        else :
            match = process_deliveries(info["innings"][0]["1st innings"]["deliveries"], team2, team1, 1, match)
            match = process_deliveries(info["innings"][1]["2nd innings"]["deliveries"], team1, team2, 2, match)
        if info["info"]["outcome"]["winner"] == match.team_1 :
            match.outcome = 1
        else :
            match.outcome = 0
        matches.append(match)
    except Exception as e:
        print("Error: ", e)
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)

DATA_PATH = '../data/odis/'
match_files = [f for f in listdir(DATA_PATH) if isfile(join(DATA_PATH, f)) and f[-5:] == '.yaml']

def main():
    ind = 0
    for filename in match_files:
        print filename, ind
        parse_file(DATA_PATH+filename)
        ind += 1
        if ind % 10 == 0:
            print ind
    batsmen_file = open("../data/batsmen.dat", "w+")
    for batsman in batsmen:
        print >>batsmen_file, batsmen[batsman].export()
    bowler_file = open("../data/bowlers.dat", "w+")
    for bowler in bowlers:
        print >>bowler_file, bowlers[bowler].export()
    teams_file = open("../data/teams.dat", "w+")
    for team in teams:
        print >>teams_file, teams[team].export()
    matches_file = open("../data/matches.dat", "w+")
    for match in matches:
        print >>matches_file, match.export()

main()
