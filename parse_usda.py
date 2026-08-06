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

def parse_txt():
    input_folderpath = f'{g.DATA_FOLDERPATH}/fetch/usda'
    with open(f"{input_folderpath}/plantlst.txt", "r", encoding="utf8", errors="ignore", newline="") as f:
        # reader = csv.DictReader(f, delimiter="|")
        content = f.read()
    print(content[:1000])

def run():
    print(f'''HERBS >> PARSE >> col''')

    start = time.perf_counter()
    parse_txt()
    print(f'parse names() - execution time: ', time.perf_counter() - start)

