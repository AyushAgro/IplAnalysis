import pandas as pd
from tabulate import tabulate
import os, sys, yaml, collections, logging
from exception import *
from classes import Team, Match
from scoreboard import create_scoreboard, preprocessData
from yaml.loader import SafeLoader
import time


start_time = time.time()
allowed_filetype = []
output_dir = ""
data_dir = ""
log_file = ""
orig_stdout = sys.stdout


def read_yaml():  # To read Config YAML
    global allowed_filetype, output_dir, data_dir, log_file

    with open("config.yaml") as f:
        data = yaml.load(f, Loader=SafeLoader)

    data_dir = data["File"]["data_dir"]
    output_dir = data["File"]["output_dir"]
    allowed_filetype = data["FileType"]
    log_file = data["File"]["log_file"]

    files = os.listdir()
    if data_dir not in files:  # Cheking if data directory is present or not
        raise DirectoryNotFound(data_dir)

    if output_dir not in files:
        os.mkdir(output_dir)


def add_to_log(logger, type, message):
    if type == "info":
        logger.info(message)
    elif type == "warning":
        logger.warning(message)
    elif type == "debug":
        logger.debug(message)
    elif type == "error":
        logger.error(message)
    return


read_yaml()

logging.basicConfig(filename=log_file, format="%(asctime)s %(message)s", filemode="w")
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
output_file_handler = logging.FileHandler(log_file)
logger.addHandler(output_file_handler)


for filename in os.listdir(data_dir):
    file = data_dir + "/" + filename
    if '_info' in file: continue
    add_to_log(logger, "info", f"Currently Processing File {file}")

    df = pd.read_csv(file, low_memory=False)
    info_file = str(file.split(".")[:-1][0]) + "_info" + ".csv"
    teams = collections.defaultdict(Team)

    try:
        df_info = pd.read_csv(info_file, names = ['info', 'Team Name','Player Name', 'code'])
        df_info = df_info.drop(['info', 'code'], axis = 1).reset_index(drop = True ).dropna()
        df_info = df_info[df_info['Team Name'] != 'people']
        df_info.apply(lambda x: get_teams(x, teams), axis = 1)
    except:
        add_to_log(logger, "error", f"Info File cannot be found of name {file}")
     
    if df.empty:
        add_to_log(logger, "error", "Empty Table")
        raise TableEmpty
    df = preprocessData(df)

    output_file = open(output_dir + "/" + filename.split(".")[0] + ".txt", "w")
    sys.stdout = output_file

    df_group_match = df.groupby("match_id")
    all_match = df_group_match.groups.keys()

    for match_id in all_match:
        add_to_log(logger, "info", f"Match Start  {match_id}")
        match_df = df_group_match.get_group(match_id)

        if match_df.empty:
            raise TableEmpty

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

        add_to_log(logger, "info", f"Result of  match - {match_id} is added")
        add_to_log(logger, "info", f"Match is Ended - {match_id}")

    sys.stdout = orig_stdout
    output_file.close()
print(f"Total Time Taken for input of size {df.size} is ", time.time() - start_time)
# Total Time Taken for input of size 3834333 is  52.054842710494995
