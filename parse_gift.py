import os
import csv
import json
import time
import shutil
import sqlite3

from lib import g
from lib import io

import masterize_utils
import parse_utils

def parse_traits():

    input_folderpath = f'{g.DATA_FOLDERPATH}/fetch/gift'
    with open(
        f"{input_folderpath}/species.csv",
        "r",
        encoding="utf8",
        errors="ignore",
        newline="",
    ) as f:
        reader = csv.DictReader(f, delimiter=",")
        batch = []
        for row in reader:
            print(json.dumps(row, indent=4))
            quit() 
    quit()
    ###
    input_folderpath = f'{g.DATA_FOLDERPATH}/fetch/gift/traits'
    with open(f"{input_folderpath}/trait_1_1_1.csv", "r", encoding="utf8", errors="ignore", newline="") as f:
        reader = csv.DictReader(f, delimiter=",")
        content = f.read()
    print(content[:1000])

def run():
    print(f'''HERBS >> PARSE >> col''')

    start = time.perf_counter()
    parse_traits()
    print(f'parse traits() - execution time: ', time.perf_counter() - start)

