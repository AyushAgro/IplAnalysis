import pandas as pd
from tabulate import tabulate
from collections import defaultdict
import os
import sys
from exception import *
import logging
from yaml.loader import SafeLoader
import yaml


allowed_filetype = []
output_dir = ''
data_dir = ''
log_file = ''
orig_stdout = sys.stdout


def add_to_log(logger, type, message):
    if type == 'info':
        logger.info(message)
    elif type == 'warning':
        logger.warning(message)
    elif type == 'debug':
        logger.debug(message)
    elif type == 'error':
        logger.error(message)
    return


def read_yaml():
    global allowed_filetype, output_dir, data_dir, log_file
    with open('config.yaml') as f:
        data = yaml.load(f, Loader=SafeLoader)

    data_dir = data['File']['data_dir']
    output_dir = data['File']['output_dir']
    allowed_filetype = data['FileType']
    log_file = data['File']['log_file']

    files = os.listdir()
    if data_dir not in files:
        raise DirectoryNotFound(data_dir)

    if output_dir not in files:
        os.mkdir(output_dir)


read_yaml()
logging.basicConfig(filename=log_file,
                    format='%(asctime)s %(message)s',
                    filemode='w')
logger = logging.getLogger()

logger.setLevel(logging.DEBUG)

output_file_handler = logging.FileHandler(log_file)

# stdout_handler = logging.StreamHandler(sys.stdout)


logger.addHandler(output_file_handler)

# logger.addHandler(stdout_handler)

required_columns = ['match_id', 'season', 'start_date', 'venue',
                    'ball', 'batting_team', 'bowling_team',
                    'striker', 'non_striker', 'bowler', 'runs_off_bat',
                    'extras', 'wides', 'noballs', 'byes', 'legbyes',
                    'penalty', 'wicket_type', 'player_dismissed']


class Team:
    def __init__(self, name):
        self.name = name
        self.players = defaultdict(Player)
        self.extra = {}

    def find_player(self, name):
        if name not in self.players:
            self.players[name] = Player(name)
        return self.players[name]

    def total_score(self):
        total_score = self.extra()
        for player in self.players:
            total_score += player.get_run()
        return total_score

    def add_extra(self, type, run):
        self.extra[type] = self.extra.get(type, 0) + run


class Player:
    def __init__(self, name):
        self.name = name
        self.run_scored = 0
        self.ball_played = 0
        self.fours = 0
        self.six = 0
        self.out = ''
        self.balled = 0

    def add_run(self, run):
        self.run_scored += run
        if run == 4:
            self.fours += 1
        if run == 6:
            self.six += 1

    def isOut(self, name):
        self.out = str(name)


def get_scoreboard(row, teams):
    BattingTeam = row['batting_team']
    BowlingTeam = row['bowling_team']

    if BattingTeam not in teams or BowlingTeam not in teams:
        raise DiffrentTeam
    if float(row['ball']) > 20.0:
        raise TooManyBall

    striker = teams[BattingTeam].find_player(row['striker'])
    non_striker = teams[BattingTeam].find_player(row['non_striker'])
    bowler = teams[BowlingTeam].find_player(row['bowler'])

    if int(row['extras']) > 0:
        extras = ['wides', 'noballs', 'byes', 'legbyes', 'penalty']
        if row['byes'] > 0 or row['legbyes'] > 0 or row['penalty'] > 0:
            striker.ball_played += 1
            bowler.balled += 1
        for extra in extras:
            if row[extra] > 0:
                teams[BattingTeam].add_extra(extra, row[extra])
    else:
        bowler.balled += 1
        striker.ball_played += 1

    if row['player_dismissed'] != '':
        player = row['player_dismissed']
        if row['wicket_type'] != 'run out':
            if striker.name == player:
                striker.isOut('B ' + bowler.name.split()[-1])
            else:
                non_striker.isOut('B ' + bowler.name.split()[-1])
        else:
            striker.add_run(row['runs_off_bat'])

            if striker.name == player:
                striker.isOut('Run Out')
            else:
                non_striker.isOut('Run Out')

    striker.add_run(row['runs_off_bat'])


def preprocessData(df):
    global required_columns
    string_type = ['wicket_type', 'player_dismissed']
    numerical_type = ['extras', 'wides',
                      'noballs', 'byes', 'legbyes', 'penalty']
    columns = df.columns
    for column in columns:
        if column not in required_columns:
            df.drop(column, inplace = True, axis = 1)
            # add_to_log(logger, 'error', 'Required Columns is not Found')
        if column in string_type:
            df[column] = df[column].fillna('')
        elif column in numerical_type:
            df[column] = df[column].fillna(0.0)
    return df


for filename in os.listdir(data_dir):
    file = data_dir + '/' + filename
    add_to_log(logger, 'info', f"Currently Processing File {file}")

    if file.split('.')[-1] not in allowed_filetype:
        add_to_log(logger, 'error', 'Invalid File Type')
        raise InvalidFile(file.split('.')[-1], allowed_filetype)

    df = pd.read_csv(file)
    df = preprocessData(df)

    if df.empty:
        add_to_log(logger, 'error', 'Empty Table')
        raise TableEmpty

    output_file = open(output_dir + '/' +
                       filename.split('.')[0] + '.txt', 'w')
    sys.stdout = output_file

    groups = df.groupby('match_id')
    all_match = groups.groups.keys()

    for match_id in all_match:
        add_to_log(logger, 'info', f"Match Start  {match_id}")
        match_df = groups.get_group(match_id)
        teams = defaultdict(Team)

        teams1 = match_df.loc[0, 'batting_team']
        teams2 = match_df.loc[0, 'bowling_team']
        venue = match_df.loc[0, 'venue']
        season = match_df.loc[0, 'season']

        start_date = match_df.loc[0, 'start_date']

        match_detail = pd.DataFrame({'Match-id': match_id,
                                     'Teams': teams2 + ' vs ' + teams1,
                                     'Venue': venue, 'season': season,
                                     'Start Date': start_date}, index=[0])

        print(tabulate(match_detail, headers='keys', tablefmt='grid',
                       showindex=False))

        teams[teams1] = Team(teams1)
        teams[teams2] = Team(teams2)

        match_df.apply(lambda x: get_scoreboard(x, teams), axis=1)
        columns = ['Batmans', 'Status', 'Run', 'Ball', '4s', '6s']

        for team_name, team in teams.items():
            result = pd.DataFrame(columns=columns)

            for name, player in team.players.items():
                row = {'Batmans': name, 'Status': player.out,
                       'Run': player.run_scored, 'Ball': player.ball_played,
                       '4s': player.fours, '6s': player.six}

                if row['Ball'] > 0 and row['Status'] == '':
                    row['Status'] = 'Not Out'

                result = result.append(row, ignore_index=True)

            print(team.name )

            print(tabulate(result, headers='keys', tablefmt='fancy_grid',
                           showindex=False))
            print('Extra (', end='' )

            for key, value in team.extra.items():
                print(f'{key[0]}-{int(value)},')

            print(')')


        add_to_log(logger, 'info', f'Result of  match - {match_id} is added')
        add_to_log(logger, 'info', f'Match is Ended - {match_id}')
        sys.stdout = orig_stdout
        output_file.close()

