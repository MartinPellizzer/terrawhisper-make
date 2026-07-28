import os
import csv
import json
import time
import shutil
import sqlite3

from lib import g
from lib import io

def parse_name():
    input_folderpath = f'{g.DATA_FOLDERPATH}/fetch/col/datasets'
    output_folderpath = f'{g.DATA_FOLDERPATH}/parse/col/vernacular_names/json'
    io.folders_recursive_gen(output_folderpath)
    with open(f"{input_folderpath}/NameUsage.tsv", "r", encoding="utf8", errors="ignore", newline="") as f:
        reader = csv.DictReader(f, delimiter="\t")
        i = 0
        for row in reader:
            # print(f'{i}')
            print('NameUsage.tsv')
            print(json.dumps(row, indent=4))
            break
    print()
    with open(f"{input_folderpath}/VernacularName.tsv", "r", encoding="utf8", errors="ignore", newline="") as f:
        reader = csv.DictReader(f, delimiter="\t")
        i = 0
        for row in reader:
            # print(f'{i}')
            print('VernacularName.tsv')
            print(json.dumps(row, indent=4))
            break

def run():
    print(f'''HERBS >> PARSE >> col''')

    start = time.perf_counter()
    parse_name() ### WARNING: takes many many minutes
    print(f'wcvp to_jsons() - execution time: ', time.perf_counter() - start)

