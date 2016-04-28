class Batsman:
    def __init__(self, name, matches, runs, balls, runs_recent, balls_recent):
        self.name = name
        self.matches = matches
        self.runs = runs
        self.balls = balls
        self.runs_recent = runs_recent
        self.balls_recent = balls_recent

    def avg(self):
        return self.runs / self.matches

    def avg_recent(self):
        return self.runs_recent / self.matches

    def strike_rate(self):
        return self.runs / self.balls

    def strike_rate_recent(self):
        return self.runs_recent / self.balls_recent

    def export(self) :
        return " ".join([str(x) for x in ["_".join(self.name.split()), self.matches, self.runs, self.balls]])


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
        return self.runs / self.wickets

    def avg_recent(self):
        return self.runs_recent / self.wickets_recent

    def economy(self):
        return self.runs / self.balls

    def economy_recent(self):
        return self.runs_recent / self.wickets_recent

    def strike_rate(self):
        return self.balls / self.wickets

    def strike_rate_recent(self):
        return self.balls_recent / self.wickets_recent

    def export(self) :
        return " ".join([str(x) for x in ["_".join(self.name.split()), self.matches, self.runs, self.wickets, self.balls]])


class Team:
    def __init__(self, name, matches, wins, runs, balls, runs_recent, balls_recent):
        self.name = name
        self.matches = matches
        self.wins = wins
        self.runs_scored = runs
        self.runs_conceded = 0
        self.balls_faced = balls
        self.balls_bowled = 0
        self.runs_recent = runs_recent
        self.balls_recent = balls_recent

    def export(self) :
        return " ".join([str(x) for x in ["_".join(self.name.split()), self.matches, self.wins, self.runs_scored, self.runs_conceded, self.balls_faced, self.balls_bowled]])

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
        return " ".join([self.team_1, self.team_2] + self.batting_order_1 + self.bowlers_1 + self.batting_order_2 + self.bowlers_2 + str(self.outcome))
