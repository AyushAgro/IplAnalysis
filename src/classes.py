from collections import defaultdict
import pandas as pd
from tabulate import tabulate  # to print in tabular form


class Match:
    def __init__(self, match_id, team1, team2, venue, start_date, season):
        self.match_id = match_id
        self.team1 = team1
        self.team2 = team2
        self.venue = venue
        self.start_date = start_date
        self.season = season
        self.winner = None

    def __str__(self):  # use this to easily print match detail.
        match_detail = pd.DataFrame(
            {
                "Match-id": self.match_id,
                "Teams": self.team1 + " vs " + self.team2,
                "Venue": self.venue,
                "season": self.season,
                "Start Date": self.start_date,
            },
            index=[0],
        )
        return tabulate(match_detail, headers="keys", tablefmt="grid", showindex=False)


# Each Match can have only two team
# and each team can have maximum playing player can be 11.
# we can raise error if any of the above condition fail.
class Team:
    def __init__(self, name):
        self.name = name
        self.players = defaultdict(Player)  # to store player data
        self.extra = {"b": 0, "l": 0, "w": 0, "nb": 0, "p": 0}  # to add extra
        self.extraRun = 0
        self.out = 0
        self.battingColumns = [
            "Batmans",
            "Status",
            "Run",
            "Ball",
            "4s",
            "6s",
        ]  # to print batting order

    # to find player with name
    def find_player(self, name):
        # if player is not present add him
        if name not in self.players:
            self.players[name] = Player(name)
        return self.players[name]  # return Player()

    # to add_extra to team
    def add_extra(self, type, run):
        self.extra[type] = self.extra.get(type, 0) + run
        self.extraRun += run

    # to get total score by team
    def get_total(self):
        runs = 0
        for _, value in self.players.items():
            runs += value.runScored
        return runs + self.extraRun

    # to print Batting Order Tabular Order
    def print_batting(self, output_file):
        result = pd.DataFrame(columns=self.battingColumns)
        for _, player in self.players.items():
            if player.out != "":
                result = result.append(player.get_batting_detail(), ignore_index=True)

        table = tabulate(result, headers="keys", tablefmt="fancy_grid", showindex=False)
        output_file.write(f"\n{self.name}\n{table}\nExtra - {int(self.extraRun)} (")
        for key, value in self.extra.items():
            output_file.write(f" {key}-{int(value)},")
        output_file.write(")")

    # after every inning we reset each player stores detail
    def reset_data(self):
        player_name = list(self.players.keys())
        # print(player_name)
        self.players = defaultdict(Player)
        for player in player_name:
            self.players[player] = Player(player)
        self.extra = {"b": 0, "l": 0, "w": 0, "nb": 0, "p": 0}
        self.extraRun = 0
        self.out = 0



# To describe each player data
class Player:
    def __init__(self, name):
        self.name = name
        self.runScored = 0
        self.ballPlayed = 0
        self.fours = 0
        self.six = 0
        self.out = ""

    def add_run(self, run):
        self.runScored += run
        if run == 4:
            self.fours += 1
        if run == 6:
            self.six += 1

    # if any Batman is Playing his isout will be changed to Not Out from this ''
    def is_playing(self):
        self.out = "Not Out"

    def is_out(self, name):
        self.out = str(name)

    # to getting Batting Details
    # you can also write for bowling.
    def get_batting_detail(self):
        row = {
            "Batmans": self.name,
            "Status": self.out,
            "Run": self.runScored,
            "Ball": self.ballPlayed,
            "4s": self.fours,
            "6s": self.six,
        }
        return row
