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
