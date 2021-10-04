# TODO
"""
1. update output_file [f] in line 75
2. seprate config, logging, excpetion and other   [Done]
3. create app strut  [Done]
4. change some variable and filename[exception] [Done]
5. Learn about GIT [rebase, stage, stash, commit, pull, push, init, --config, log --oneline, fetch, status, add]
"""
import pandas as pd
import os
import time
import psutil
from config.ipl_config import read_yaml

import asyncio
from scoreboard import scoreboard_utils, preprocess_data

pd.options.mode.chained_assignment = None  # to avoid pandas warnings

# print('You can check std.log to check for all logs')
# print('Check Result Folder for result generator during execution of code')

# Initializing
start_time = time.time()
pid = os.getpid()
p = psutil.Process(pid)

data_dir, output_dir, allowed_filetype, logger = read_yaml()

async def get_result(filename):
    try:
        file = os.path.join(data_dir, filename)  # getting file name
        logger.info(f"Currently Processing File {file}")

        df = pd.read_csv(file, low_memory=False)
        df = preprocess_data(df)  # apply some preprocessing to our data


        df_group_match = df.groupby("match_id")
        all_match = df_group_match.groups.keys()
        output = {}
        for match_id in all_match:
            match_ = df_group_match.get_group(match_id)
            # print(match_)
            output[match_id] = asyncio.ensure_future(scoreboard_utils(match_, logger))
        output_file = os.path.join(output_dir, "".join(filename.split(".")[:-1]) + ".txt")
        file = open(output_file, "w")
        for _, value in output.items():
            file.write(f'{value}')
    except Exception as e:
        logger.exception(
            f'Error was occured during handling of file {filename}')
        return

async def main():
    tasks = []

    for filename in os.listdir(data_dir):
        if str(filename.split('.')[-1]) != 'csv' or 'info' in filename:
            continue
        # if it not in allowed extension or it has info in it filename
        task = asyncio.create_task(get_result(filename))
        tasks.append(task)
    await asyncio.gather(*tasks)
    print(f"Total Time Taken for input is  {time.time() - start_time} seconds")
    memory = (p.memory_full_info().uss) / (1024 * 1024)
    print("Memory used: {:.2f} MB".format(memory))

asyncio.run(main())

