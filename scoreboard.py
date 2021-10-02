import pandas as pd
from exception import DiffrentTeam, TooManyBall, ColumnsNotFound
from log import log_decorator, logger_obj

pd.options.mode.chained_assignment = None  # to avoid pandas warnings


# Just using to check if we have all required columns and chaning their datatype to use minimum
# For example, just think of columns innings it can have integer like [1,2,3,4,5,6..] so we should waste
# 64 byte of integer as given at beganing but we can all in 8 byte hence int8.

required_columns = {
    "match_id": "int64",
    "season": "object",
    "start_date": "datetime64",
    "innings": "uint8",
    "venue": "object",
    "ball": "float32",
    "batting_team": "object",
    "bowling_team": "object",
    "striker": "object",
    "non_striker": "object",
    "bowler": "object",
    "runs_off_bat": "uint8",
    "extras": "uint8",
    "wides": "uint8",
    "noballs": "uint8",
    "byes": "uint8",
    "legbyes": "uint8",
    "penalty": "uint8",
    "wicket_type": "object",
    "player_dismissed": "object",
}


@log_decorator
def create_scoreboard(Match, match_df, teams):
    print(Match)  # using __str__ method in match to print

    # If match was played with no exceptions it must have Innings as even number
    # Like 1,2 or 1,2,3,4 so we need to work with innings as their can be super over
    # If it is super over the innings must be greater than 2
    # It it is odd Result was not declered because other team didn't played

    total_innings = match_df["innings"].nunique()
    score = {}

    innings = 1  # Inning start from 1
    while total_innings + 1 > innings:
        # Masking on our dataset to get data belong to paticular innings
        # and then appling our get_scoreboard
        innings_df = match_df[(match_df["innings"] == innings)]
        innings_df.apply(lambda x: get_scoreboard(x, teams), axis=1)

        BattingTeam = teams[innings_df["batting_team"].values[0]]
        BowlingTeam = teams[innings_df["bowling_team"].values[0]]

        # this was written for super over as if innings is greater than 2 which mean [3,4..]
        # it is super over
        if innings > 2 and innings % 2 == 1:
            try:
                declare_result(score, innings)
                print("\nSuper Over-" + "I" * (innings // 2))
            except: # if innings is odd
                logger_obj.error(f'Result for Match_id {Match.match_id} was not Declared')
                print("No Result was Declared")

        innings += 1
        BattingTeam.print_batting()  # to print Batting Scoreboard.
        score[BattingTeam.name] = [BattingTeam.get_total(), BattingTeam.out]
        BattingTeam.reset()  # After every inning we need to reset score of each player to zero
        BowlingTeam.reset()

    try:
        declare_result(score, innings)
    except: # if innings is odd
        logger_obj.error(f'Result for Match_id {Match.match_id} was not Declared')
        print("No Result was Decalred")


def get_scoreboard(row, teams):
    BattingTeam = row["batting_team"]
    BowlingTeam = row["bowling_team"]

    if BattingTeam not in teams or BowlingTeam not in teams:
        logger_obj.error("Team given is not as same as given before")
        raise DiffrentTeam

    if row["ball"] > 20.0:
        logger_obj.error("Single Innings can have maximum of 20 Over but it exceed")
        raise TooManyBall

    striker = teams[BattingTeam].find_player(row["striker"])
    non_striker = teams[BattingTeam].find_player(row["non_striker"])
    bowler = teams[BowlingTeam].find_player(row["bowler"])

    striker.playing()  ## To change player status from Yet To Bat --> Not Out
    non_striker.playing()
    striker.ball_played += 1  # striker played one ball
    striker.add_run(row["runs_off_bat"])  # adding run to striker

    if int(row["extras"]) > 0:  # Checking if there is any extra or not.
        isExtra(row, teams, BattingTeam, striker)

    if row["player_dismissed"] != "": # if someone got out
        isWicket(row, teams, BattingTeam, striker, non_striker, bowler)


def isWicket(row, teams, BattingTeam, striker, non_striker, bowler):
    teams[BattingTeam].out += 1  # increase total out of teams

    player = row["player_dismissed"]

    # if wicket type is not run out we have to add bowler name
    if row["wicket_type"] != "run out":
        if striker.name == player:
            striker.isOut("B " + bowler.name.split()[-1])
        else: # not necassary but just added in rare case
            non_striker.isOut("B " + bowler.name.split()[-1])

    # else it can be striker or non-striker we have to check out player_dismissed
    else:
        if striker.name == player:
            striker.isOut("Run Out")
        else:
            non_striker.isOut("Run Out")


def isExtra(row, teams, BattingTeam, striker):
    extras = [
        "wides",
        "noballs",
        "byes",
        "legbyes",
        "penalty",
    ]

    # wheneve bowler throw a ball we add it to striker
    # but if it a no Ball or wide, then we have to remove it as we have already added
    if row["noballs"] > 0 or row["wides"] > 0:
        striker.ball_played -= 1

    # going columns by columns for checking if there is extra
    for extra in extras:
        if row[extra] > 0:
            teams[BattingTeam].add_extra(extra[0], row[extra])  # extra will added to batting team


def declare_result(score, innings):
    team1, team2 = score.keys()
    # Whenever their is super over innings will be greater than 3 so teams switch or
    # if teams 1 first Bath then in super Over Bowler team will Bat First
    if innings > 3:
        team1, team2 = team2, team1
    # If score of team1 is greater than they will win by difference in run
    if score[team1][0] > score[team2][0]:
        print(f"\n{team1} won the Match by {score[team1][0] - score[team2][0]} Run")


    # if score of team2 is greater than they will win by 10 - total_out
    elif score[team1][0] < score[team2][0]:
        print(f"\n{team2} won the Match by {10 - score[team2][1]} wicket\n")

    # Else it will be tie
    else:
        print("It was a tie, So it Time for Super Over\n")


@log_decorator
def preprocessData(df):

    global required_columns
    numeric_dtype = ["wides", "noballs", "byes", "legbyes", "penalty"]
    category_dtype = ["wicket_type", "player_dismissed"]
    columns = df.columns

    for col, col_type in required_columns.items():
        # Just filling NaN Value with respect to their datatype
        if col in numeric_dtype:
            df[col].fillna(0, inplace=True)
        if col in category_dtype:
            df[col].fillna("", inplace=True)

        # this mean one of the required colums in not present so we wont be able to read it
        if col not in columns:
            logger_obj.error(f"{col} Cannot be Found")
            raise ColumnsNotFound(col)

        # If col is present we simply check it has mnimum required byte for each columns.
        else:
            try:
                df[col] = df[col].astype(col_type, errors="raise")
            except ValueError: # if we can't convert it into minimum required byte, so we continue
                logger_obj.warning(f"{col} Cannot be changed into {col_type}")
                pass

    df = df[required_columns.keys()]  # slicing df to keep only required columns
    df["start_date"] = df["start_date"].dt.strftime("%d %B %Y")  # Just Increasing readbility of datatime
    return df
