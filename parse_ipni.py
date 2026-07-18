
import os
import csv
import json
import time
import shutil
import sqlite3

from lib import g
from lib import io
from lib import llm

import pipeline_utils

def ipni_peek():
    source_foldername = 'ipni'
    input_foldername = 'fetch'
    input_folderpath = f'{g.DATA_FOLDERPATH}/{input_foldername}/{source_foldername}/ipni'
    with open(f"{input_folderpath}/Name.tsv", "r", encoding="utf8", errors="ignore", newline="") as f:
        reader = csv.DictReader(f, delimiter="\t")
        i = 0
        for row in reader:
            print(f'{i}')
            print(json.dumps(row, indent=4))
            break
    with open(f"{input_folderpath}/NameRelation.tsv", "r", encoding="utf8", errors="ignore", newline="") as f:
        reader = csv.DictReader(f, delimiter="\t")
        i = 0
        for row in reader:
            print(f'{i}')
            print(json.dumps(row, indent=4))
            break
    with open(f"{input_folderpath}/Reference.tsv", "r", encoding="utf8", errors="ignore", newline="") as f:
        reader = csv.DictReader(f, delimiter="\t")
        i = 0
        for row in reader:
            print(f'{i}')
            print(json.dumps(row, indent=4))
            break
    with open(f"{input_folderpath}/Taxon.tsv", "r", encoding="utf8", errors="ignore", newline="") as f:
        reader = csv.DictReader(f, delimiter="\t")
        i = 0
        for row in reader:
            print(f'{i}')
            print(json.dumps(row, indent=4))
            break
    with open(f"{input_folderpath}/TypeMaterial.tsv", "r", encoding="utf8", errors="ignore", newline="") as f:
        reader = csv.DictReader(f, delimiter="\t")
        i = 0
        for row in reader:
            print(f'{i}')
            print(json.dumps(row, indent=4))
            break

def run():
    print('PARSE >> ipni')

    start = time.perf_counter()
    ipni_peek()
    print(f'ipni to_jsons() - execution time: ', time.perf_counter() - start)


