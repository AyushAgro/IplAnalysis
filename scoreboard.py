import pandas as pd
from tabulate import tabulate
from exception import DiffrentTeam, TooManyBall, ColumnsNotFound
from quo import echo
pd.options.mode.chained_assignment = None

required_columns = {
    "match_id" : 'int64',
    "season" : 'int16',
    "start_date" : 'datetime64',
    "innings": 'uint8',
    "venue": 'object',
    "ball": 'float32',
    "batting_team" : 'object',
    "bowling_team": 'object',
    "striker": 'object',
    "non_striker": 'object',
    "bowler": 'object',
    "runs_off_bat": 'uint8',
    "extras": 'uint8',
    "wides": 'uint8',
    "noballs": 'uint8',
    "byes": 'uint8',
    "legbyes": 'uint8',
    "penalty": 'uint8',
    "wicket_type": 'object',
    "player_dismissed": 'object',
}

def create_scoreboard(Match, match_df, teams):
    match_detail = pd.DataFrame(
        {
            "Match-id": Match.match_id,
            "Teams": Match.team1 + " vs " + Match.team2,
            "Venue": Match.venue,
            "season": Match.season,
            "Start Date": Match.start_date,
        },
        index=[0],
    )
    header = tabulate(match_detail, headers="keys", tablefmt="grid", showindex=False)
    print(header)
    columns = ["Batmans", "Status", "Run", "Ball", "4s", "6s"]
    total_innings = match_df['innings'].nunique()
    # print(total_innings)
    score = {}

    innings = 1
    while total_innings +1 > innings:
        innings_df = match_df[(match_df['innings'] == innings)]
        innings_df.apply(lambda x: get_scoreboard(x, teams), axis=1)

        BattingTeam = teams[innings_df["batting_team"].values[0]]
        BowlingTeam = teams[innings_df["bowling_team"].values[0]]
        print()
        if innings > 2 and innings % 2 == 1:
            declare_result(score, innings)
            BattingTeam.reset()
            BowlingTeam.reset()
            print('Super Over-' + 'I' * (innings // 2))
        innings += 1

        result = pd.DataFrame(columns=columns)
        for name, player in BattingTeam.players.items():
            if player.out != "":
                row = {
                    "Batmans": name,
                    "Status": player.out,
                    "Run": player.run_scored,
                    "Ball": player.ball_played,
                    "4s": player.fours,
                    "6s": player.six,
                }
                result = result.append(row, ignore_index=True)

        table = tabulate(result, headers="keys", tablefmt="fancy_grid", showindex=False)
        print(f"{BattingTeam.name}\n{table}\nExtra - {int(BattingTeam.extra_run)} (",end="",)

        for key, value in BattingTeam.extra.items():
            print(f" {key}-{int(value)},", end="")
        print(")")
        score[BattingTeam.name] = [BattingTeam.get_total(), BattingTeam.out]
    try:
        declare_result(score, innings)
    except Exception as e:
        print('No Result was Decalred')

def get_scoreboard(row, teams):
    BattingTeam = row["batting_team"]
    BowlingTeam = row["bowling_team"]

    if BattingTeam not in teams or BowlingTeam not in teams:
        # add_to_log(logger, 'error', 'Team given is not as same as given before')
        raise DiffrentTeam
    if row["ball"] > 20.0 :
        # add_to_log(logger, 'error', 'over Limit exceed from 20')
        raise TooManyBall

    striker = teams[BattingTeam].find_player(row["striker"])
    non_striker = teams[BattingTeam].find_player(row["non_striker"])
    bowler = teams[BowlingTeam].find_player(row["bowler"])

    striker.playing()
    non_striker.playing()
    striker.ball_played += 1
    striker.add_run(row["runs_off_bat"])

    if int(row["extras"]) > 0:  # Checking if there is any extra or not.
        isExtra(row, teams, BattingTeam, striker, bowler)

    if row["player_dismissed"] != "":
        isWicket(row, teams, BattingTeam, striker, non_striker, bowler)

def isWicket(row, teams, BattingTeam, striker, non_striker, bowler):
    teams[BattingTeam].out += 1

    player = row["player_dismissed"]

    if row["wicket_type"] != "run out":
        if striker.name == player:
            striker.isOut("B " + bowler.name.split()[-1])
        else:
            non_striker.isOut("B " + bowler.name.split()[-1])
    else:
        if striker.name == player:
            striker.isOut("Run Out")
        else:
            non_striker.isOut("Run Out")

def declare_result(score, i):
    team1, team2 = score.keys()
    if i > 3:
        team1, team2 = team2, team1
    if score[team1][0] > score[team2][0]:
        print(f'\n{team1} won the Match by {score[team1][0] - score[team2][0]} Run')
    elif score[team1][0] < score[team2][0]:
        print(f'\n{team2} won the Match by {10 - score[team2][1]} wicket\n')
    else:
        print('It was a tie, Check Below for Super Over\n')


def isExtra(row, teams, BattingTeam, striker, bowler):
    extras = [
        "wides",
        "noballs",
        "byes",
        "legbyes",
        "penalty",
    ]

    if row["noballs"] > 0 or row["wides"] > 0:
        striker.ball_played -= 1
        bowler.balled -= 1

    for extra in extras:
        if row[extra] > 0:
            teams[BattingTeam].add_extra(extra[0], row[extra])


def preprocessData(df):
    global required_columns
    numeric_dtype = ['wides', 'noballs', 'byes', 'legbyes', 'penalty']
    category_dtype = ['wicket_type', 'player_dismissed']

    columns = df.columns
    for col, col_type in required_columns.items():
        if col in numeric_dtype:
            df[col].fillna(0, inplace = True)
        if col in category_dtype:
            df[col].fillna('', inplace = True)
        if col not in columns:
            # add_to_log(logger, 'error', f'{col} Cannot be Found')
            raise ColumnsNotFound(col)
        else:
            try:
                df[col] = df[col].astype(col_type, errors = 'raise')
            except ValueError:
                pass
                # add_to_log(logger, 'warning', f'{col} Cannot be changed into {col_type}')
    df = df[required_columns.keys()]
    df['start_date'] = df['start_date'].dt.strftime('%d/%m/%y')
    return df
