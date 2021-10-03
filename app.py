import pandas as pd
import os
import sys
import yaml
from yaml.loader import SafeLoader
import time
import psutil

from log import log_decorator, logger
import exception
from scoreboard import scorboard_utils, preprocess_data

pd.options.mode.chained_assignment = None  # to avoid pandas warnings
print('You can check std.log to check for all logs\nError and Warning will be printed in console.')


@log_decorator
def read_yaml():  # To read Config YAML
    global allowed_filetype, output_dir, data_dir

    # reading file with open
    with open("config.yaml") as f:
        data = yaml.load(f, Loader=SafeLoader)

    data_dir = os.path.join(os.getcwd(), data["File"]["data_dir"])
    output_dir = os.path.join(os.getcwd(), data["File"]["output_dir"])
    allowed_filetype = data["FileType"]

    # Checking if data directory is present or not
    if not os.path.exists(data_dir) or not os.path.isdir(data_dir):
        raise exception.DirectoryNotFound(data_dir)

    # print(output_dir)
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)


# Initializing
start_time = time.time()
allowed_filetype = []
output_dir = ""
data_dir = ""
orig_stdout = sys.stdout
pid = os.getpid()
total_size = 0
p = psutil.Process(pid)
read_yaml()


# lopping every file present in data_dir
for filename in os.listdir(data_dir):

    # if it not in allowed extension or it has info in it filename
    if filename.split(".")[-1] not in allowed_filetype or "_info" in filename:
        continue

    file = os.path.join(data_dir, filename)  # getting file name
    logger.info(f"Currently Processing File {file}")

    try:
        df = pd.read_csv(file, low_memory=False)
    except KeyboardInterrupt:
        print('\nHello user you have pressed ctrl-c button. So we are quiting Function')
        sys.exit()
    except:
        logger.error(f'Can\'t Load data from file {filename}, So Skiping it')
        continue

    total_size += df.size
    df_ = preprocess_data(df) # apply some preprocessing to our data

    if isinstance(df_, pd.DataFrame):
        df = df_

    # now we create a new file for file in data directory and store our result
    output_file = "".join(filename.split(".")[:-1]) + ".txt"

    with open(os.path.join(output_dir, output_file), "w") as f:

        sys.stdout = f  # just to write into file which is easy you can use f.write to
        try:
            dfGroupMatch = df.groupby("match_id").apply(scorboard_utils)
        except Exception as e:
            logger.error(f'Error was raise during grouping by and error was {e}')

    sys.stdout  = orig_stdout

print(f"Total Time Taken for input of size {total_size} is  {time.time() - start_time} seconds")

memory = (p.memory_full_info().uss) /(1024 * 1024)
print("Memory used: {:.2f} MB".format(memory))

# Total Time Taken for input of size 4439754 is 37.23739409446716 seconds
# Memory used: 147.54 MB
