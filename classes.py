from collections import defaultdict
from exception import MaximumPlayer


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
        self.extra = {"b": 0, "lb": 0, "w": 0, "nb": 0, "p": 0}
        self.extra_run = 0
        self.out = 0

    def find_player(self, name):
        if len(self.players) > 11:
            raise MaximumPlayer(self.name)
        if name not in self.players:
            self.players[name] = Player(name)
        return self.players[name]

    def add_extra(self, type, run):
        self.extra[type] = self.extra.get(type, 0) + run
        self.extra_run += run

    def get_total(self):
        runs = 0
        for key, value in self.players.items():
            runs += value.run_scored
        return runs + self.extra_run

    def reset(self):
        player_name = list(self.players.keys())
        print(player_name)
        self.players = defaultdict(Player)
        for player in player_name:
            self.players[player] = Player(player)
        self.extra = {"b": 0, "lb": 0, "w": 0, "nb": 0, "p": 0}
        self.extra_run = 0
        self.out = 0


class Player:
    def __init__(self, name):
        self.name = name
        self.run_scored = 0
        self.ball_played = 0
        self.fours = 0
        self.six = 0
        self.out = ""

    def add_run(self, run):
        self.run_scored += run
        if run == 4:
            self.fours += 1
        if run == 6:
            self.six += 1

    def playing(self):
        self.out = "Not Out"

    def isOut(self, name):
        self.out = str(name)
