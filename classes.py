from collections import defaultdict


class Match:
    def __init__(self, match_id, team1, team2, venue, start_date, season):
        self.match_id = match_id
        self.team1 = team1
        self.team2 = team2
        self.venue = venue
        self.start_date = start_date
        self.season = season


class Team:
    def __init__(self, name):
        self.name = name
        self.players = defaultdict(Player)
        self.extra = {}

    def find_player(self, name):
        if name not in self.players:
            self.players[name] = Player(name)
        return self.players[name]

    def total_score(self):
        total_score = self.extra()
        for player in self.players:
            total_score += player.get_run()
        return total_score

    def add_extra(self, type, run):
        self.extra[type] = self.extra.get(type, 0) + run


class Player:
    def __init__(self, name):
        self.name = name
        self.run_scored = 0
        self.ball_played = 0
        self.fours = 0
        self.six = 0
        self.out = ""
        self.balled = 0

    def add_run(self, run):
        self.run_scored += run
        if run == 4:
            self.fours += 1
        if run == 6:
            self.six += 1

    def isOut(self, name):
        self.out = str(name)
