import os
import json
import time
import shutil
import sqlite3

from lib import g
from lib import io
from lib import data

import resolve_utils

def resolve_chemicals():
    input_foldername = f'normalize'
    output_foldername = f'resolve'
    ###
    input_folderpath = f'{g.VAULT_FOLDERPATH}/terrawhisper/data/{input_foldername}/pubmed/chemicals/json'
    output_folderpath = f'{g.VAULT_FOLDERPATH}/terrawhisper/data/{output_foldername}/pubmed/chemicals/json'
    io.folders_recursive_gen(output_folderpath)
    input_filenames = os.listdir(input_folderpath)
    try: shutil.rmtree(output_folderpath)
    except: pass
    os.makedirs(output_folderpath, exist_ok=True)
    ###
    wcvp_folderpath = f'{g.VAULT_FOLDERPATH}/terrawhisper/data/reference/wcvp/wcvp.db'
    wcvp_conn = sqlite3.connect(wcvp_folderpath)
    pubchem_folderpath = f'{g.VAULT_FOLDERPATH}/terrawhisper/data/reference/pubchem/pubchem.db'
    pubchem_conn = sqlite3.connect(pubchem_folderpath)
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
            # print(json.dumps(input_item, indent=True))
            resolved_item = input_item
            plant_name_normalized = input_item['plant_name_normalized']
            chemical_name_normalized = input_item['chemical_name_normalized']
            if chemical_name_normalized == 'null': continue
            ### RESOLVE PLANT (WCVP)
            wcvp_cur = wcvp_conn.cursor()
            wcvp_cur.execute("""
                SELECT *
                FROM wcvp
                WHERE taxon_name_normalized = ?
            """, (plant_name_normalized,))
            wcvp_row = wcvp_cur.fetchone()
            ### RESOLVE CHEMICAL (PUBCHEM)
            pubchem_cur = pubchem_conn.cursor()
            pubchem_cur.execute("""
                SELECT *
                FROM pubchem_cid_synonyms
                WHERE normalized_alias = ?
            """, (chemical_name_normalized,))
            pubchem_row = pubchem_cur.fetchone()
            if wcvp_row and pubchem_row:
                wcvp_taxon_name = wcvp_row[0]
                wcvp_taxon_name_normalized = wcvp_row[1]
                pubchem_cid = pubchem_row[0]
                pubchem_chemical_name = pubchem_row[1]
                pubchem_chemical_name_normalized = pubchem_row[2]
                resolved_item_new = resolved_item
                resolved_item_new['wcvp_taxon_name'] = wcvp_taxon_name
                resolved_item_new['wcvp_taxon_name_normalized'] = wcvp_taxon_name_normalized
                resolved_item_new['pubchem_cid'] = pubchem_cid
                resolved_item_new['pubchem_chemical_name'] = pubchem_chemical_name
                resolved_item_new['pubchem_chemical_name_normalized'] = pubchem_chemical_name_normalized
                resolved_data.append(resolved_item_new)
        if resolved_data != []:
            io.json_write(output_filepath, resolved_data)
    pubchem_conn.close()
    wcvp_conn.close()

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

def resolve_diseases():
    source_name = 'pubmed'
    entity_type = 'diseases'
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
    ### RESOLVE PLANTS NAMES
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
            plant_name = input_item['plant_name']
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

    print(f'########################################')
    start = time.perf_counter()
    resolve_chemicals()
    print(f'resolve_chemicals() - execution time: ', time.perf_counter() - start)
    print(f'########################################')

    # start = time.perf_counter()
    # resolve_activities()
    # print(f'folder_copy() - execution time: ', time.perf_counter() - start)

    # start = time.perf_counter()
    # resolve_diseases()
    # print(f'resolve_diseases() - execution time: ', time.perf_counter() - start)

