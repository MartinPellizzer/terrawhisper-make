import os
import csv
import time
import shutil

from lib import g
from lib import io
from lib import llm

def wcvp_to_jsons():
    source_foldername = 'wcvp'
    input_foldername = 'fetch'
    output_foldername = 'parse'
    input_folderpath = f'{g.DATA_FOLDERPATH}/{input_foldername}/{source_foldername}'
    output_folderpath = f'{g.DATA_FOLDERPATH}/{output_foldername}/{source_foldername}/json'
    io.folders_recursive_gen(output_folderpath)

    with open(f"{input_folderpath}/wcvp_names.csv", "r", encoding="utf8", errors="ignore", newline="") as f:
        reader = csv.DictReader(f, delimiter="|")
        i = 0
        for row in reader:
            print(f'{i}')
            taxon_name = row["taxon_name"]
            if not taxon_name: continue
            i+= 1
            io.json_write(f'{output_folderpath}/{taxon_name}.json', row)

def run():
    print('PARSE >> wcvp')

    start = time.perf_counter()
    wcvp_to_jsons() ### WARNING: takes many many minutes
    print(f'wcvp to_jsons() - execution time: ', time.perf_counter() - start)

