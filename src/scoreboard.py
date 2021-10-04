from utils import *
from classes import Team, Match
from collections import defaultdict


"""
    Just using to check if we have all required columns and changing their datatype
    to use minimum For example, just think of columns innings it can have integer
    like [1,2,3,4,5,6..] so we should not waste 64 byte of integer as given at
    beginning but we can just use 8 byte unsigned interger hence uint8.
"""
required_columns = {
    "match_id": "int64",
    "season": "category",
    "start_date": "datetime64[ns]",
    "innings": "uint8",
    "venue": "category",
    "ball": "float32",
    "batting_team": "category",
    "bowling_team": "category",
    "striker": "category",
    "non_striker": "category",
    "bowler": "category",
    "runs_off_bat": "uint8",
    "extras": "uint8",
    "wides": "uint8",
    "noballs": "uint8",
    "byes": "uint8",
    "legbyes": "uint8",
    "penalty": "uint8",
    "wicket_type": "category",
    "player_dismissed": "category",
}

teams = defaultdict(Team)


def scoreboard_utils(match_df, output_file, logger):
    global teams
    match_id = match_df['match_id'].values[0]
    logger.info(f"Match Start  {match_id}")

    if match_df.empty:
        logger.warning(f"Match with id  {match_id} has no data avilable.")
        return

    teams1 = match_df["batting_team"].values[0]
    teams2 = match_df["bowling_team"].values[0]
    venue = match_df["venue"].values[0]
    season = match_df["season"].values[0]
    start_date = match_df["start_date"].values[0]

    # if teams are not present add them
    if teams1 not in teams:
        teams[teams1] = Team(teams1)
    teams[teams1].reset_data()
    if teams2 not in teams:
        teams[teams2] = Team(teams2)
    teams[teams2].reset_data()

    match = Match(match_id, teams1, teams2, venue, start_date, season)

    # function to create scoreboard
    output_file.write(str(match))
    create_scoreboard(match, match_df, teams, output_file, logger)

    logger.info(f"Result of  match - {match_id} is added")
    logger.info(f"Match is Ended - {match_id}")


def create_scoreboard(match, match_df, teams, output_file, logger):

    totalInnings = match_df["innings"].nunique()
    score = {}
    winner = None

    innings = 1  # Inning start from 1
    while totalInnings + 1 > innings:

        inningsDf = match_df[(match_df["innings"] == innings)]
        inningsDf.apply(lambda x: get_scoreboard(x, teams, logger), axis=1)

        battingTeam = teams[inningsDf["batting_team"].values[0]]
        bowlingTeam = teams[inningsDf["bowling_team"].values[0]]

        # this was written for super over as if innings is greater than 2 which mean [3,4..]
        # so it is super over
        if innings > 2 and innings % 2 == 1:
            declare_result(score, innings, output_file)
            output_file.write("\nSuper Over-" + "I" * (innings // 2))

        innings += 1
        battingTeam.print_batting(output_file)  # to print Batting Scoreboard.
        score[battingTeam.name] = [battingTeam.get_total(), battingTeam.out]

        # After every inning we need to reset score of each player to zero
        battingTeam.reset_data()
        bowlingTeam.reset_data()
    winner = declare_result(score, innings, output_file)
    match.winner = winner


def get_scoreboard(row, teams, logger):
    battingTeam = row["batting_team"]
    bowlingTeam = row["bowling_team"]

    if battingTeam not in teams or bowlingTeam not in teams:
        logger.error("Team given is not as same as given before")
        raise DifferentTeam

    if row["ball"] > 20.0:
        logger.error(
            "Single Innings can have maximum of 20 Over but it exceed")
        raise TooManyBall

    striker = teams[battingTeam].find_player(row["striker"])
    nonStriker = teams[battingTeam].find_player(row["non_striker"])
    bowler = teams[bowlingTeam].find_player(row["bowler"])

    striker.is_playing()  # To change player status from Yet To Bat --> Not Out
    nonStriker.is_playing()
    striker.ballPlayed += 1  # striker played one ball
    striker.add_run(row["runs_off_bat"])  # adding run to striker

    if row["extras"] > 0:  # Checking if there is any extra or not.
        is_extra(row, teams, battingTeam, striker)

    if row["player_dismissed"] != "":  # if someone got out
        is_wicket(row, teams, battingTeam, striker, nonStriker, bowler)


def is_wicket(row, teams, battingTeam, striker, nonStriker, bowler):
    teams[battingTeam].out += 1  # increase total out of teams


    # if wicket type is not run out we have to add bowler name
    if row["wicket_type"] != "run out":
        striker.is_out("B " + bowler.name.split()[-1])

    # else it can be striker or non-striker we have to check out player_dismissed
    else:
        player = row["player_dismissed"]
        if striker.name == player:
            striker.is_out("Run Out")
        else:
            nonStriker.is_out("Run Out")


def is_extra(row, teams, battingTeam, striker):
    extras = [
        "wides",
        "noballs",
        "byes",
        "legbyes",
        "penalty",
    ]

    # whenever bowler throw a ball we add it to striker
    # but if it a no Ball or wide, then we have to remove it as we have already added
    if row["noballs"] > 0 or row["wides"] > 0:
        striker.ballPlayed -= 1

    # going columns by columns for checking if there is extra
    for extra in extras:
        if row[extra] > 0:
            # extra will added to batting team
            teams[battingTeam].add_extra(extra[0], row[extra])


def declare_result(score, innings, output_file):
    try:
        team1, team2 = score.keys()
    except ValueError:
        output_file.write('Result was not declared')
        return
    # Whenever their is super over innings will be greater than 3 so teams switch or
    # if teams 1 first Bat then in super Over Bowler team will Bat First
    if innings > 3:
        team1, team2 = team2, team1

    # If score of team1 is greater than they will win by difference in run
    if score[team1][0] > score[team2][0]:
        output_file.write(
            f"\n{team1} won the Match by {score[team1][0] - score[team2][0]} Run\n")
        return team1

    # if score of team2 is greater than they will win by 10 - total_out
    elif score[team1][0] < score[team2][0]:
        output_file.write(f"\n{team2} won the Match by {10 - score[team2][1]} wicket\n")
        return team2

    # Else it will be tie
    else:
        output_file.write("\nIt was a tie, So it Time for Super Over\n")
        return None


def preprocess_data(df):
    global required_columns
    columns_set = set(df.columns)
    # columns_set.remove('match_id')
    required_columns_set = set(required_columns.keys())
    subset = required_columns_set - columns_set
    if len(subset)>0:
        raise ColumnsNotFound(list(subset))

    df = df[required_columns_set]
    df.select_dtypes('object').fillna('', inplace=True)
    df.select_dtypes(['int64', 'float64']).fillna(0, inplace=True)
    df = df.astype(required_columns, errors='ignore')

    df["start_date"] = df["start_date"].dt.strftime("%d %B %Y")

    return df
