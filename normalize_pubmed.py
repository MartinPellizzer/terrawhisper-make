import os
import json
import time
import shutil

from lib import g
from lib import io

def normalize_plant_name(plant_name):
    plant_name = plant_name.lower()
    return plant_name

def normalize_chemicals():
    entity_type = 'chemicals'
    input_foldername = f'parse'
    output_foldername = f'normalize'
    input_folderpath = f'{g.VAULT_FOLDERPATH}/terrawhisper/data/{input_foldername}/pubmed/{entity_type}/json'
    output_folderpath = f'{g.VAULT_FOLDERPATH}/terrawhisper/data/{output_foldername}/pubmed/{entity_type}/json'
    io.folders_recursive_gen(output_folderpath)
    input_filenames = os.listdir(input_folderpath)
    ###
    i = 0
    for input_filename in input_filenames[i:]:
        print(input_filename)
        i += 1
        print(f'{i}/{len(input_filenames)}')
        output_filepath = f'{output_folderpath}/{input_filename}'
        # if os.path.exists(output_filepath): continue
        input_filepath = f'{input_folderpath}/{input_filename}'
        input_data = io.json_read(input_filepath)
        normalized_data = []
        for input_item in input_data:
            ### normalize plant_name
            normalized_item = input_item
            normalized_item['plant_name'] = normalize_plant_name(input_item['plant_name'])
            # print(json.dumps(normalized_item, indent=4))
            normalized_data.append(normalized_item)
        io.json_write(output_filepath, normalized_data)
        # quit()

def normalize_activities():
    entity_type = 'activities'
    input_foldername = f'parse'
    output_foldername = f'normalize'
    input_folderpath = f'{g.VAULT_FOLDERPATH}/terrawhisper/data/{input_foldername}/pubmed/{entity_type}/json'
    output_folderpath = f'{g.VAULT_FOLDERPATH}/terrawhisper/data/{output_foldername}/pubmed/{entity_type}/json'
    io.folders_recursive_gen(output_folderpath)
    input_filenames = os.listdir(input_folderpath)
    ###
    i = 0
    for input_filename in input_filenames[i:]:
        print(input_filename)
        i += 1
        print(f'{i}/{len(input_filenames)}')
        output_filepath = f'{output_folderpath}/{input_filename}'
        # if os.path.exists(output_filepath): continue
        input_filepath = f'{input_folderpath}/{input_filename}'
        input_data = io.json_read(input_filepath)
        normalized_data = []
        for input_item in input_data:
            ### normalize plant_name
            normalized_item = input_item
            normalized_item['plant_name'] = normalize_plant_name(input_item['plant_name'])
            # print(json.dumps(normalized_item, indent=4))
            normalized_data.append(normalized_item)
        io.json_write(output_filepath, normalized_data)
        # quit()

def run():
    print('normalize >> pubmed')

    start = time.perf_counter()
    # normalize_chemicals()
    print(f'folder_copy() - execution time: ', time.perf_counter() - start)

    start = time.perf_counter()
    normalize_activities()
    print(f'folder_copy() - execution time: ', time.perf_counter() - start)

