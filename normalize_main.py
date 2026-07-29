import os
import json
import time
import shutil

import re
import unicodedata

from lib import g
from lib import io

import normalize_utils

def normalize_plants_chemicals(source_foldername):
    input_folderpath = f'{g.DATA_FOLDERPATH}/parse/{source_foldername}/chemicals/json'
    output_folderpath = f'{g.DATA_FOLDERPATH}/normalize/{source_foldername}/chemicals/json'
    try: shutil.rmtree(output_folderpath)
    except: pass
    io.folders_recursive_gen(output_folderpath)
    input_filenames = os.listdir(input_folderpath)
    ###
    for i, input_filename in enumerate(input_filenames[:]):
        print(f'{i}/{len(input_filenames)}')
        output_filepath = f'{output_folderpath}/{input_filename}'
        if os.path.exists(output_filepath): continue
        ###
        input_filepath = f'{input_folderpath}/{input_filename}'
        input_data = io.json_read(input_filepath)
        for input_item in input_data:
            input_item['plant_name_normalized'] = normalize_utils.normalize_plant_name(input_item['plant_name_raw'])
            input_item['chemical_name_normalized'] = normalize_utils.normalize_chemical_name(input_item['chemical_name_raw'])
            # print(json.dumps(normalized_item, indent=4))
            # quit()
        io.json_write(output_filepath, input_data)
    print(json.dumps(input_data[0], indent=4))
    # quit()

def normalize_plants_synonyms(source_foldername):
    input_folderpath = f'{g.DATA_FOLDERPATH}/parse/{source_foldername}/synonyms/json'
    output_folderpath = f'{g.DATA_FOLDERPATH}/normalize/{source_foldername}/synonyms/json'
    try: shutil.rmtree(output_folderpath)
    except: pass
    io.folders_recursive_gen(output_folderpath)
    input_filenames = os.listdir(input_folderpath)
    ###
    for i, input_filename in enumerate(input_filenames[:]):
        print(f'{i}/{len(input_filenames)}')
        output_filepath = f'{output_folderpath}/{input_filename}'
        if os.path.exists(output_filepath): continue
        ###
        input_filepath = f'{input_folderpath}/{input_filename}'
        input_data = io.json_read(input_filepath)
        for input_item in input_data:
            input_item['plant_name_normalized'] = normalize_utils.normalize_plant_name(input_item['plant_name_raw'])
            input_item['plant_synonym_normalized'] = normalize_utils.normalize_plant_name(input_item['plant_synonym_raw'])
            # print(json.dumps(normalized_item, indent=4))
            # quit()
        io.json_write(output_filepath, input_data)
    print(json.dumps(input_data[0], indent=4))
    # quit()

def normalize_plants_common_names(source_foldername):
    input_folderpath = f'{g.DATA_FOLDERPATH}/parse/{source_foldername}/names/json'
    output_folderpath = f'{g.DATA_FOLDERPATH}/normalize/{source_foldername}/names/json'
    try: shutil.rmtree(output_folderpath)
    except: pass
    io.folders_recursive_gen(output_folderpath)
    input_filenames = os.listdir(input_folderpath)
    ###
    for i, input_filename in enumerate(input_filenames[:]):
        print(f'{i}/{len(input_filenames)}')
        output_filepath = f'{output_folderpath}/{input_filename}'
        if os.path.exists(output_filepath): continue
        ### COPY FOLDER
        input_filepath = f'{input_folderpath}/{input_filename}'
        input_data = io.json_read(input_filepath)
        io.json_write(output_filepath, input_data)

def run():
    print('NORMALIZE')

    if 0:
        start = time.perf_counter()
        normalize_plants_synonyms(source_foldername='wcvp')
        print(f'normalize plants_synonyms() - execution time: ', time.perf_counter() - start)

    if 1:
        start = time.perf_counter()
        normalize_plants_common_names(source_foldername='col')
        print(f'normalize plants_common_names() - execution time: ', time.perf_counter() - start)

    if 0:
        start = time.perf_counter()
        normalize_plants_chemicals(source_foldername='drduke')
        normalize_plants_chemicals(source_foldername='pubmed')
        print(f'normalize_plants_chemicals() - execution time: ', time.perf_counter() - start)

