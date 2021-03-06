#class for storing batsman stats
class Batsman:
    def __init__(self, name, matches, runs, balls, runs_recent, balls_recent):
        self.name = name
        self.matches = matches
        self.runs = runs
        self.balls = balls
        self.runs_recent = runs_recent
        self.balls_recent = balls_recent

    def avg(self):
        return self.runs * 1.0 / self.matches

    def avg_recent(self):
        return self.runs_recent * 1.0 / self.matches

    def strike_rate(self):
        return self.runs * 1.0 / self.balls

    def strike_rate_recent(self):
        return self.runs_recent * 1.0 / self.balls_recent

    def features(self):
        return [self.avg(), self.strike_rate(), self.matches]

    def export(self) :
        return " ".join([str(x) for x in ["_".join(self.name.split()), self.matches, self.runs, self.balls]])

#class for storing bowler stats
class Bowler:
    def __init__(self, name, matches, runs, wickets, balls, runs_recent, wickets_recent, balls_recent):
        self.name = name
        self.matches = matches
        self.runs = runs
        self.wickets = wickets
        self.runs_recent = runs_recent
        self.wickets_recent = wickets_recent
        self.balls = balls
        self.balls_recent = balls_recent

    def avg(self):
        return self.runs * 1.0 / self.wickets

    def avg_recent(self):
        return self.runs_recent * 1.0 / self.wickets_recent

    def economy(self):
        return self.runs * 1.0 / self.balls

    def economy_recent(self):
        return self.runs_recent * 1.0 / self.wickets_recent

    def strike_rate(self):
        return self.balls * 1.0 / self.wickets

    def strike_rate_recent(self):
        return self.balls_recent * 1.0 / self.wickets_recent

    def features(self):
        return [self.avg(), self.economy(), self.strike_rate(), self.matches]

    def export(self) :
        return " ".join([str(x) for x in ["_".join(self.name.split()), self.matches, self.runs, self.wickets, self.balls]])

#class for storing team stats
class Team:
    def __init__(self, name, matches, wins, runs_scored, runs_conceded, balls_faced, balls_bowled):
        self.name = name
        self.matches = matches
        self.wins = wins
        self.runs_scored = runs_scored
        self.runs_conceded = runs_conceded
        self.balls_faced = balls_faced
        self.balls_bowled = balls_bowled

    def features(self):
        return [self.wins* 1.0 / self.matches, self.runs_scored* 1.0 / self.balls_faced,
                self.runs_conceded* 1.0 / self.balls_bowled]

    def export(self) :
        return " ".join([str(x) for x in ["_".join(self.name.split()), self.matches, self.wins, self.runs_scored, self.runs_conceded, self.balls_faced, self.balls_bowled]])

def replace_space_all(lst):
    return ["_".join(x.split()) for x in lst]

#class for storing match stats
class Match :
    def __init__(self, team_1, team_2):
        self.team_1 = team_1
        self.team_2 = team_2
        self.batting_order_1 = []
        self.bowlers_1 = []
        self.batting_order_2 = []
        self.bowlers_2 = []
        self.outcome = 0

    def export(self) :
        return " ".join(["_".join(self.team_1.split()), "_".join(self.team_2.split())] + replace_space_all(self.batting_order_1) + replace_space_all(self.bowlers_1) + replace_space_all(self.batting_order_2) + replace_space_all(self.bowlers_2) + [str(self.outcome)])

    def normalize(self) :
        self.batting_order_1 += [self.team_1 + " avg"] * (11 - len(self.batting_order_1))
        self.batting_order_2 += [self.team_2 + " avg"] * (11 - len(self.batting_order_2))
        self.bowlers_1 += [self.bowlers_1[0]] * (5 - len(self.bowlers_1))
        self.bowlers_2 += [self.bowlers_2[0]] * (5 - len(self.bowlers_2))
