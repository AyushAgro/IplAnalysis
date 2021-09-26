import pandas as pd
from tabulate import tabulate
import os, sys, yaml, collections, logging
from exception import *
from classes import Team, Match
from scoreboard import create_scoreboard, preprocessData
from yaml.loader import SafeLoader

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
    add_to_log(logger, "info", f"Currently Processing File {file}")

    if file.split(".")[-1] not in allowed_filetype:
        add_to_log(logger, "error", "Invalid File Type")
        raise InvalidFile(file.split(".")[-1], allowed_filetype)

    df = pd.read_csv(file)
    df = preprocessData(df)

    if df.empty:
        add_to_log(logger, "error", "Empty Table")
        raise TableEmpty

    output_file = open(output_dir + "/" + filename.split(".")[0] + ".txt", "w")
    sys.stdout = output_file

    df_group_match = df.groupby("match_id")
    all_match = df_group_match.groups.keys()

    for match_id in all_match:
        add_to_log(logger, "info", f"Match Start  {match_id}")

        match_df = df_group_match.get_group(match_id)
        if match_df.empty:
            raise TableEmpty

        teams = collections.defaultdict(Team)
        teams1 = match_df.loc[0, "batting_team"]
        teams2 = match_df.loc[0, "bowling_team"]
        venue = match_df.loc[0, "venue"]
        season = match_df.loc[0, "season"]
        start_date = match_df.loc[0, "start_date"]
        teams[teams1] = Team(teams1)
        teams[teams2] = Team(teams2)

        match = Match(match_id, teams1, teams2, venue, start_date, season)
        create_scoreboard(match, match_df, teams)

        add_to_log(logger, "info", f"Result of  match - {match_id} is added")
        add_to_log(logger, "info", f"Match is Ended - {match_id}")

        sys.stdout = orig_stdout
        output_file.close()
