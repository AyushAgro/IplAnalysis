import pandas as pd
from tabulate import tabulate
import os
import sys
import yaml
import collections
from log import log_decorator, logger_obj
import exception
from classes import Team, Match
from scoreboard import create_scoreboard, preprocessData
from yaml.loader import SafeLoader
import time


start_time = time.time()
allowed_filetype = []
output_dir = ""
data_dir = ""
orig_stdout = sys.stdout


@log_decorator
def read_yaml():  # To read Config YAML
    global allowed_filetype, output_dir, data_dir

    with open("config.yaml") as f:
        data = yaml.load(f, Loader=SafeLoader)

    data_dir = os.path.join(os.getcwd(), data["File"]["data_dir"])
    output_dir = os.path.join(os.getcwd(), data["File"]["output_dir"])
    allowed_filetype = data["FileType"]

    if not os.path.exists(data_dir):  # Cheking if data directory is present or not
        raise exception.DirectoryNotFound(data_dir)
    # print(output_dir)
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)


def get_teams(row, team):
    team_name = row["Team Name"]
    if team_name not in team:
        newTeam = Team(team_name)
        team[team_name] = newTeam
    team[team_name].find_player(row["Player Name"])


read_yaml()


for filename in os.listdir(data_dir):
    file = data_dir + "/" + filename
    if "_info" in file:
        continue
    logger_obj.info(f"Currently Processing File {file}")

    df = pd.read_csv(file, low_memory=False)
    info_file = str(file.split(".")[:-1][0]) + "_info" + ".csv"
    teams = collections.defaultdict(Team)

    try:
        df_info = pd.read_csv(
            info_file, names=["info", "Team Name", "Player Name", "code"]
        )
        df_info = df_info.drop(["info", "code"], axis=1).reset_index(drop=True).dropna()
        df_info = df_info[df_info["Team Name"] != "people"]
        df_info.apply(lambda x: get_teams(x, teams), axis=1)
    except:
        logger_obj.warning(f"info File cannot be found for given {file}")
    if df.empty:
        logger_obj.error("Empty Table")
        raise exception.TableEmpty
    df = preprocessData(df)

    with open(output_dir + "/" + filename.split(".")[0] + ".txt", "w") as f:
        sys.stdout = f

        df_group_match = df.groupby("match_id")
        all_match = df_group_match.groups.keys()

        for match_id in all_match:
            logger_obj.info(f"Match Start  {match_id}")
            match_df = df_group_match.get_group(match_id)

            if match_df.empty:
                logger_obj.info(f"Match with id  {match_id} has no data avilable.")
                continue

            teams1 = match_df["batting_team"].values[0]
            teams2 = match_df["bowling_team"].values[0]
            venue = match_df["venue"].values[0]
            season = match_df["season"].values[0]
            start_date = match_df["start_date"].values[0]

            if teams1 not in teams:
                teams[teams1] = Team(teams1)
            if teams2 not in teams:
                teams[teams2] = Team(teams2)

            match = Match(match_id, teams1, teams2, venue, start_date, season)
            create_scoreboard(match, match_df, teams)

            logger_obj.info(f"Result of  match - {match_id} is added")
            logger_obj.info(f"Match is Ended - {match_id}")

        sys.stdout = orig_stdout

print(f"Total Time Taken for input of size {df.size} is ", time.time() - start_time)
# Total Time Taken for input of size 4036140 is  47.289313554763794