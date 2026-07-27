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
import masterize_utils
import reference_utils
import parse_utils

def wcvp_names():
    source_foldername = 'wcvp'
    input_foldername = 'fetch'
    output_foldername = 'parse'
    input_folderpath = f'{g.DATA_FOLDERPATH}/{input_foldername}/{source_foldername}'
    output_folderpath = f'{g.DATA_FOLDERPATH}/{output_foldername}/{source_foldername}/names/json'
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

def parse_synonyms():
    output_folderpath = f'{g.DATA_FOLDERPATH}/parse/wcvp/synonyms/json'
    try: shutil.rmtree(output_folderpath)
    except: pass
    os.makedirs(output_folderpath, exist_ok=True)
    ###
    plants_rows = masterize_utils.masterize_plants_get_all()
    for i, plant_row in enumerate(plants_rows[:]):
        print(f'{i}/{len(plants_rows)}')
        plant_name_raw = plant_row[1]
        plant_name_normalized = plant_row[2]
        input_filename = plant_name_raw
        output_filepath = f'{output_folderpath}/{input_filename}'
        if os.path.exists(output_filepath): continue
        ###
        synonyms_rows = reference_utils.wcvp_plant_synonym_get_rows(plant_name_normalized)
        items_output = []
        for synonym_row in synonyms_rows:
            plant_synonym_raw = synonym_row[3]
            item_output = parse_utils.synonym_create(
                plant_name_raw = plant_name_raw, 
                plant_synonym_raw = plant_synonym_raw, 
                source_name = 'WCVP',
            )
            items_output.append(item_output)
            # print(json.dumps(item_output, indent=4))
            # quit()
        io.json_write(output_filepath, items_output)
        # shutil.copy(input_filepath, output_filepath)
        # print(input_filename)

def wcvp_names_peek():
    source_foldername = 'wcvp'
    input_foldername = 'fetch'
    input_folderpath = f'{g.DATA_FOLDERPATH}/{input_foldername}/{source_foldername}'
    with open(f"{input_folderpath}/wcvp_names.csv", "r", encoding="utf8", errors="ignore", newline="") as f:
        reader = csv.DictReader(f, delimiter="|")
        i = 0
        conn = sqlite3.connect(f'{g.DATA_FOLDERPATH}/reference/wcvp/wcvp.db')
        for row in reader:
            print(f'{i}')
            print(json.dumps(row, indent=4))
            quit()

def wcvp_distribution_peek():
    source_foldername = 'wcvp'
    input_foldername = 'fetch'
    input_folderpath = f'{g.DATA_FOLDERPATH}/{input_foldername}/{source_foldername}/distribution'
    with open(f"{input_folderpath}/wcvp_distribution.csv", "r", encoding="utf8", errors="ignore", newline="") as f:
        reader = csv.DictReader(f, delimiter="|")
        i = 0
        conn = sqlite3.connect(f'{g.DATA_FOLDERPATH}/reference/wcvp/wcvp.db')
        for row in reader:
            print(f'{i}')
            print(json.dumps(row, indent=4))
            quit()

def run():
    print('PARSE >> wcvp')

    start = time.perf_counter()
    # wcvp_names() ### WARNING: takes many many minutes
    # wcvp_names_peek()
    print(f'wcvp to_jsons() - execution time: ', time.perf_counter() - start)

    ### WCVP DISTRIBUTION
    start = time.perf_counter()
    if 0:
        pipeline_utils.folder_copy(
            input_folderpath = f'{g.DATA_FOLDERPATH}/fetch/wcvp/distribution',
            output_folderpath = f'{g.DATA_FOLDERPATH}/parse/wcvp/distribution',
        )
    # wcvp_distribution_peek()
    print(f'wcvp distribution() - execution time: ', time.perf_counter() - start)

    start = time.perf_counter()
    parse_synonyms()
    print(f'parse synonyms() - execution time: ', time.perf_counter() - start)

