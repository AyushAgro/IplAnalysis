import pandas as pd
import collections
import os
import sys
import yaml
from yaml.loader import SafeLoader # to load config file
import time # to check time used [optional]
import psutil # to see memory used by out program [optional]
from log import log_decorator, logger_obj # to handle log
import exception # to handle exception
from classes import Team, Match
from scoreboard import create_scoreboard, preprocessData

@log_decorator
def read_yaml():  # To read Config YAML
    global allowed_filetype, output_dir, data_dir

    # reading file with open
    with open("config.yaml") as f:
        data = yaml.load(f, Loader=SafeLoader)

    data_dir = os.path.join(os.getcwd(), data["File"]["data_dir"])
    output_dir = os.path.join(os.getcwd(), data["File"]["output_dir"])
    allowed_filetype = data["FileType"]

    # Cheking if data directory is present or not
    if not os.path.exists(data_dir) or not os.path.isdir(data_dir):
        raise exception.DirectoryNotFound(data_dir)

    # print(output_dir)
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)

# Initilazing
start_time = time.time()
allowed_filetype = []
output_dir = ""
data_dir = ""
orig_stdout = sys.stdout
pid = os.getpid()
p = psutil.Process(pid)
read_yaml()

# to add all team name from _info file if it present
# it is optional.
def get_teams(row, team):
    team_name = row["Team Name"]
    if team_name not in team:
        newTeam = Team(team_name)
        team[team_name] = newTeam
    team[team_name].find_player(row["Player Name"])

# lopping every file present in data_dir
# can use os.walk which we also consider subfolder present in it
for filename in os.listdir(data_dir):
    # if it not in allowed extension or it has info in it filename
    if filename.split('.')[-1] not in allowed_filetype or "_info" in filename:
        continue

    file = os.path.join(data_dir, filename) # getting file name
    logger_obj.info(f"Currently Processing File {file}")

    df = pd.read_csv(file, low_memory=False)  # reading file.. we just added csv extension
    df = preprocessData(df) # apply some preprocessing to our data

    teams = collections.defaultdict(Team)  # variation of python dict

    # To read info file, it a optional just added so you can get additional information about match
    try:
        info_file = str(file.split(".")[:-1][0]) + "_info" + ".csv"
        df_info = pd.read_csv(
            info_file, names=["info", "Team Name", "Player Name", "code"]
        )
        df_info = df_info.drop(["info", "code"], axis=1).reset_index(drop=True).dropna()
        df_info = df_info[df_info["Team Name"] != "people"]
        df_info.apply(lambda x: get_teams(x, teams), axis=1)

    except:  # if there is any exception/ error it will simply add it to log.
        logger_obj.warning(f"info File cannot be loaded for given {file}")

    if df.empty:
        logger_obj.error("Empty Table")
        raise exception.TableEmpty

    # now we create a new file for file in data directory and store our result
    output_file = ''.join(filename.split('.')[:-1]) + '.txt'
    with open(os.path.join(output_dir, output_file), "w") as f:

        sys.stdout = f  # just to write into file which is easy you can use f.write to

        # grouping our dataset with respect to mathch_id as it can be treated as primary key
        df_group_match = df.groupby("match_id")
        al_matches = df_group_match.groups.keys() # getting all_matches keys

        # lopping over each match_id present in our dataset.
        for match_id in al_matches:
            logger_obj.info(f"Match Start  {match_id}")
            match_df = df_group_match.get_group(match_id) # acessing data of paticular match

            if match_df.empty:
                logger_obj.info(f"Match with id  {match_id} has no data avilable.")
                continue

            teams1 = match_df["batting_team"].values[0]
            teams2 = match_df["bowling_team"].values[0]
            venue = match_df["venue"].values[0]
            season = match_df["season"].values[0]
            start_date = match_df["start_date"].values[0]

            # if teams are not present add them
            if teams1 not in teams:
                teams[teams1] = Team(teams1)
            if teams2 not in teams:
                teams[teams2] = Team(teams2)

            # Add detail of paticualar match, you can use namedTuple.
            match = Match(match_id, teams1, teams2, venue, start_date, season)

            # function to create scoreboard
            create_scoreboard(match, match_df, teams)

            logger_obj.info(f"Result of  match - {match_id} is added")
            logger_obj.info(f"Match is Ended - {match_id}")

        sys.stdout = orig_stdout # reseting sys.stdout for last line to print in screen

print(f"Total Time Taken for input of size {df.size} is ", time.time() - start_time)
# Total Time Taken for input of size 4036140 is  47.289313554763794

memory = p.memory_full_info().uss
memory /= 1024 * 1024
print("Memory used: {:.2f} MB".format(memory))
