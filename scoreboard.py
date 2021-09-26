import pandas as pd
from tabulate import tabulate
from exception import *

required_columns = [
    "match_id",
    "season",
    "start_date",
    "venue",
    "ball",
    "batting_team",
    "bowling_team",
    "striker",
    "non_striker",
    "bowler",
    "runs_off_bat",
    "extras",
    "wides",
    "noballs",
    "byes",
    "legbyes",
    "penalty",
    "wicket_type",
    "player_dismissed",
]


def create_scoreboard(Match, match_df, teams):
    match_detail = pd.DataFrame(
        {
            "Match-id": Match.match_id,
            "Teams": Match.team2 + " vs " + Match.team1,
            "Venue": Match.venue,
            "season": Match.season,
            "Start Date": Match.start_date,
        },
        index=[0],
    )
    header = tabulate(match_detail, headers="keys", tablefmt="grid", showindex=False)
    print(header)
    match_df.apply(lambda x: get_scoreboard(x, teams), axis=1)
    columns = ["Batmans", "Status", "Run", "Ball", "4s", "6s"]
    for _, team in teams.items():
        result = pd.DataFrame(columns=columns)

        for name, player in team.players.items():
            row = {
                "Batmans": name,
                "Status": player.out,
                "Run": player.run_scored,
                "Ball": player.ball_played,
                "4s": player.fours,
                "6s": player.six,
            }
            if row["Ball"] > 0 and row["Status"] == "":
                row["Status"] = "Not Out"

            result = result.append(row, ignore_index=True)

        table = tabulate(result, headers="keys", tablefmt="fancy_grid", showindex=False)
        print("\n" + team.name + "\n" + table + "\n" + "Extra -", int(team.extra_run),  '(' , end="")
        for key, value in team.extra.items():
            print(f" {key[0]}-{int(value)},", end="")
        print(")")


def get_scoreboard(row, teams):
    BattingTeam = row["batting_team"]
    BowlingTeam = row["bowling_team"]

    if BattingTeam not in teams or BowlingTeam not in teams:
        raise DiffrentTeam
    if float(row["ball"]) > 20.0:
        raise TooManyBall

    striker = teams[BattingTeam].find_player(row["striker"])
    non_striker = teams[BattingTeam].find_player(row["non_striker"])
    bowler = teams[BowlingTeam].find_player(row["bowler"])

    if int(row["extras"]) > 0:  # Checking if there is any extra or not.
        extras = [
            "wides",
            "noballs",
            "byes",
            "legbyes",
            "penalty",
        ]  # which type of extra it is

        if row["byes"] > 0 or row["legbyes"] > 0 or row["penalty"] > 0:
            striker.ball_played += 1
            bowler.balled += 1
        for extra in extras:
            if row[extra] > 0:
                teams[BattingTeam].add_extra(extra, row[extra])
    else:
        bowler.balled += 1
        striker.ball_played += 1

    if row["player_dismissed"] != "":
        player = row["player_dismissed"]
        if row["wicket_type"] != "run out":
            if striker.name == player:
                striker.isOut("B " + bowler.name.split()[-1])
            else:
                non_striker.isOut("B " + bowler.name.split()[-1])
        else:
            striker.add_run(row["runs_off_bat"])

            if striker.name == player:
                striker.isOut("Run Out")
            else:
                non_striker.isOut("Run Out")

    striker.add_run(row["runs_off_bat"])


def preprocessData(df):
    global required_columns
    string_type = ["wicket_type", "player_dismissed"]
    numerical_type = ["extras", "wides", "noballs", "byes", "legbyes", "penalty"]
    columns = df.columns
    for column in columns:
        if column not in required_columns:
            df.drop(column, inplace=True, axis=1)
        if column in string_type:
            df[column] = df[column].fillna("")
        elif column in numerical_type:
            df[column] = df[column].fillna(0.0)
    return df
