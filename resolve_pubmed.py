import os
import json
import time
import shutil

from lib import g
from lib import io
from lib import data

def resolve_chemicals():
    input_foldername = f'normalize'
    output_foldername = f'resolve'
    ###
    print('resolve >> pubmed')
    input_folderpath = f'{g.VAULT_FOLDERPATH}/terrawhisper/data/{input_foldername}/pubmed/chemicals/json'
    output_folderpath = f'{g.VAULT_FOLDERPATH}/terrawhisper/data/{output_foldername}/pubmed/chemicals/json'
    io.folders_recursive_gen(output_folderpath)
    input_filenames = os.listdir(input_folderpath)
    try: shutil.rmtree(output_folderpath)
    except: pass
    os.makedirs(output_folderpath, exist_ok=True)
    ###
    i = 0
    for input_filename in input_filenames[i:]:
        print(input_filename)
        i += 1
        print(f'{i}/{len(input_filenames)}')
        output_filepath = f'{output_folderpath}/{input_filename}'
        input_filepath = f'{input_folderpath}/{input_filename}'
        # if os.path.exists(output_filepath): continue
        input_data = io.json_read(input_filepath)
        resolved_data = []
        for input_item in input_data:
            print(input_item)
            resolved_item = input_item
            ### TODO: try make lookup faster by saving already did plants on a list and skip those you already know exististy (use 2 lists probalbly, one for found and one for not found in wcvp)
            wcvp_row = data.sqlite3__wcvp_get(input_item['plant_name'])
            if not wcvp_row: continue
            resolved_data.append(resolved_item)
        io.json_write(output_filepath, resolved_data)
        # quit()

def resolve_activities():
    source_name = 'pubmed'
    entity_type = 'activities'
    input_foldername = f'normalize'
    output_foldername = f'resolve'
    ###
    print('resolve >> pubmed')
    input_folderpath = f'{g.VAULT_FOLDERPATH}/terrawhisper/data/{input_foldername}/{source_name}/{entity_type}/json'
    output_folderpath = f'{g.VAULT_FOLDERPATH}/terrawhisper/data/{output_foldername}/{source_name}/{entity_type}/json'
    io.folders_recursive_gen(output_folderpath)
    input_filenames = os.listdir(input_folderpath)
    try: shutil.rmtree(output_folderpath)
    except: pass
    os.makedirs(output_folderpath, exist_ok=True)
    ###
    i = 0
    plants_names_found = set()
    plants_names_not_found = set()
    for input_filename in input_filenames[i:]:
        print(input_filename)
        i += 1
        print(f'{i}/{len(input_filenames)}')
        output_filepath = f'{output_folderpath}/{input_filename}'
        input_filepath = f'{input_folderpath}/{input_filename}'
        # if os.path.exists(output_filepath): continue
        input_data = io.json_read(input_filepath)
        resolved_data = []
        for input_item in input_data:
            print(input_item)
            resolved_item = input_item
            ### TODO: try make lookup faster by saving already did plants on a list and skip those you already know exististy (use 2 lists probalbly, one for found and one for not found in wcvp)
            plant_name = input_item['plant_name']
            # print(plant_name, plants_names_found) 
            if plant_name in plants_names_found:
                resolved_data.append(resolved_item)
                continue
            elif plant_name in plants_names_not_found:
                continue
            wcvp_row = data.sqlite3__wcvp_get(plant_name)
            if wcvp_row:
                resolved_data.append(resolved_item)
                plants_names_found.add(plant_name)
            else:
                plants_names_not_found.add(plant_name)
        io.json_write(output_filepath, resolved_data)
        # quit()

def run():
    print('RESOLVE >> pubmed')

    start = time.perf_counter()
    # resolve_chemicals()
    print(f'folder_copy() - execution time: ', time.perf_counter() - start)

    start = time.perf_counter()
    resolve_activities()
    print(f'folder_copy() - execution time: ', time.perf_counter() - start)

