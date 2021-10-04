# TODO
"""
1. update output_file [f] in line 75
2. seprate config, logging, excpetion and other   [Done]
3. create app strut  [Done]
4. change some variable and filename[exception] [Done]
5. Learn about GIT [rebase, stage, stash, commit, pull, push, init, --config, log --oneline, fetch, status, add]
"""
from collections import defaultdict
import pandas as pd
import os
import time
import json
import psutil
from config.ipl_config import read_yaml
import pprint
import sys
from tabulate import tabulate

from scoreboard import scoreboard_utils, preprocess_data

pd.options.mode.chained_assignment = None  # to avoid pandas warnings
pp = pprint.PrettyPrinter(indent = 4)

# print('You can check std.log to check for all logs')
# print('Check Result Folder for result generator during execution of code')
orig = sys.stdout

# Initializing
start_time = time.time()
pid = os.getpid()
total_size = 0
count = 0
p = psutil.Process(pid)
data_dir, output_dir, allowed_filetype,logger = read_yaml()

for filename in os.listdir(data_dir):
    # if it not in allowed extension or it has info in it filename
    try:
        file = os.path.join(data_dir, filename)  # getting file name
        logger.info(f"Currently Processing File {file}")

        df = pd.read_csv(file, low_memory=False)

        total_size += df.size
        df = preprocess_data(df) # apply some preprocessing to our data

        output_file = "".join(filename.split(".")[:-1]) + ".txt"
        df_ =pd.DataFrame(columns = ['filename', 'value'])

        with open(os.path.join(output_dir, output_file), "w") as f:
            to_write = df.groupby("match_id").apply(lambda subset_df: scoreboard_utils(subset_df, logger)).to_dict()
            # print(to_write)
            for match_id, value in to_write.items():
                for key, detail in value.items():
                    f.write(f'{detail}')
    except Exception as e:
        print(e)
        count += 1
        logger.exception(f'Error was occured during handling of file {filename}')
if count > 0:
    print(f'{count} Error was encouter during excution please check log/std.log')
else:

    print(f"Total Time Taken for input of size {total_size} is  {time.time() - start_time} seconds")
    memory = (p.memory_full_info().uss) /(1024 * 1024)
    print("Memory used: {:.2f} MB".format(memory))
