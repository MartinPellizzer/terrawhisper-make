import os
import time
import json
import shutil
import sqlite3

from lib import g
from lib import io
from lib import llm

import resolve_utils

def resolve_plants_parts(source_foldername):
    input_folderpath = f'{g.DATA_FOLDERPATH}/normalize/{source_foldername}/plants_parts/json'
    output_folderpath = f'{g.DATA_FOLDERPATH}/resolve/{source_foldername}/plants_parts/json'
    try: shutil.rmtree(output_folderpath)
    except: pass
    os.makedirs(output_folderpath, exist_ok=True)
    ###
    wcvp_folderpath = f'{g.DATA_FOLDERPATH}/reference/wcvp/wcvp.db'
    wcvp_conn = sqlite3.connect(wcvp_folderpath)
    input_filenames = os.listdir(input_folderpath)
    for i, input_filename in enumerate(input_filenames[:]):
        print(f'{i}/{len(input_filenames)}')
        output_filepath = f'{output_folderpath}/{input_filename}'
        input_filepath = f'{input_folderpath}/{input_filename}'
        if os.path.exists(output_filepath): continue
        ###
        input_data = io.json_read(input_filepath)
        resolved_data = []
        for input_item in input_data:
            # print(json.dumps(input_item, indent=True))
            # quit()
            plant_name_raw_norm = input_item['plant_name_raw_norm']
            ### RESOLVE PLANT (WCVP)
            wcvp_row = resolve_utils.resolve_plant_accepted(wcvp_conn, plant_name_raw_norm)
            ### RESOLVE PLANT PART (...)
            plant_parts_canon = [
                {
                    'canon': 'root',
                    'raw': ['root', 'roots'],
                },
                {
                    'canon': 'rhizome',
                    'raw': ['rhizome', 'rhizomes'],
                },
                {
                    'canon': 'stem',
                    'raw': ['stem', 'stems'],
                },
                {
                    'canon': 'leaf',
                    'raw': ['leaf', 'leaves'],
                },
                {
                    'canon': 'flower',
                    'raw': ['flower', 'flowers'],
                },
                {
                    'canon': 'fruit',
                    'raw': ['fruit', 'fruits', 'berry', 'berries'],
                },
                {
                    'canon': 'seed',
                    'raw': ['seed', 'seeds'],
                },
            ]
            plant_part_canon = ''
            for item in plant_parts_canon:
                found = False
                for raw_val in item['raw']:
                    if raw_val in input_item['plant_part_name_raw_norm']:
                        plant_part_canon = item['canon']
                        found = True
                        break
                if found: 
                    break
            if plant_part_canon == '':
                # plant_part_canon = input_item['plant_part_name_raw_norm']
                continue
            ###
            if wcvp_row:
                input_item['plant_name_scientific_canon'] = wcvp_row[3]
                input_item['plant_name_scientific_canon_norm'] = wcvp_row[4]
                input_item['plant_part_name_canon'] = plant_part_canon
                input_item['plant_part_name_canon_norm'] = plant_part_canon
                resolved_data.append(input_item)
                # if plant_name_raw_norm == 'panax ginseng':
                    # print(json.dumps(input_item, indent=True))
                    # quit()
                # print(json.dumps(input_item, indent=True))
                # quit()
        if resolved_data != []:
            io.json_write(output_filepath, resolved_data)
    wcvp_conn.close()

def resolve_activities(source_foldername):
    input_folderpath = f'{g.DATA_FOLDERPATH}/normalize/{source_foldername}/activities/json'
    output_folderpath = f'{g.DATA_FOLDERPATH}/resolve/{source_foldername}/activities/json'
    try: shutil.rmtree(output_folderpath)
    except: pass
    os.makedirs(output_folderpath, exist_ok=True)
    ###
    wcvp_folderpath = f'{g.DATA_FOLDERPATH}/reference/wcvp/wcvp.db'
    drduke_folderpath = f'{g.DATA_FOLDERPATH}/reference/drduke/drduke.db'
    wcvp_conn = sqlite3.connect(wcvp_folderpath)
    drduke_conn = sqlite3.connect(drduke_folderpath)
    ###
    input_filenames = os.listdir(input_folderpath)
    for i, input_filename in enumerate(input_filenames[:]):
        print(f'{i}/{len(input_filenames)}')
        output_filepath = f'{output_folderpath}/{input_filename}'
        input_filepath = f'{input_folderpath}/{input_filename}'
        if os.path.exists(output_filepath): continue
        ###
        input_data = io.json_read(input_filepath)
        resolved_data = []
        for input_item in input_data:
            # print(json.dumps(input_item, indent=True))
            # quit()
            plant_name_raw_norm = input_item['plant_name_raw_norm']
            activity_name_raw_norm = input_item['activity_name_raw_norm']
            # if chemical_name_normalized == 'null': continue
            ### RESOLVE PLANT (WCVP)
            wcvp_row = resolve_utils.resolve_plant_accepted(wcvp_conn, plant_name_raw_norm)
            ### RESOLVE ACTIVITY (DRDUKE)
            drduke_cur = drduke_conn.cursor()
            drduke_cur.execute("""
                SELECT *
                FROM activities
                WHERE activity_name_raw_norm = ?
            """, (activity_name_raw_norm,))
            drduke_row = drduke_cur.fetchone()
            ###
            if wcvp_row and drduke_row:
                input_item['plant_name_scientific_canon'] = wcvp_row[3]
                input_item['plant_name_scientific_canon_norm'] = wcvp_row[4]
                input_item['activity_name_canon'] = drduke_row[0]
                input_item['activity_name_canon_norm'] = drduke_row[1]
                resolved_data.append(input_item)
                # print(json.dumps(input_item, indent=True))
                # quit()
        if resolved_data != []:
            io.json_write(output_filepath, resolved_data)
    wcvp_conn.close()
    drduke_conn.close()

def resolve_chemicals(source_foldername):
    input_folderpath = f'{g.DATA_FOLDERPATH}/normalize/{source_foldername}/chemicals/json'
    output_folderpath = f'{g.DATA_FOLDERPATH}/resolve/{source_foldername}/chemicals/json'
    try: shutil.rmtree(output_folderpath)
    except: pass
    os.makedirs(output_folderpath, exist_ok=True)
    ###
    wcvp_folderpath = f'{g.DATA_FOLDERPATH}/reference/wcvp/wcvp.db'
    pubchem_folderpath = f'{g.DATA_FOLDERPATH}/reference/pubchem/pubchem.db'
    wcvp_conn = sqlite3.connect(wcvp_folderpath)
    pubchem_conn = sqlite3.connect(pubchem_folderpath)
    ###
    input_filenames = os.listdir(input_folderpath)
    for i, input_filename in enumerate(input_filenames[:]):
        print(f'{i}/{len(input_filenames)}')
        output_filepath = f'{output_folderpath}/{input_filename}'
        input_filepath = f'{input_folderpath}/{input_filename}'
        if os.path.exists(output_filepath): continue
        ###
        input_data = io.json_read(input_filepath)
        resolved_data = []
        for input_item in input_data:
            # print(json.dumps(input_item, indent=True))
            resolved_item = input_item
            plant_name_raw_norm = input_item['plant_name_raw_norm']
            chemical_name_raw_norm = input_item['chemical_name_raw_norm']
            if chemical_name_raw_norm == 'null':
                continue
            ### RESOLVE PLANT (WCVP)
            wcvp_row = resolve_utils.resolve_plant_accepted(wcvp_conn, plant_name_raw_norm)
            ### RESOLVE CHEMICAL (PUBCHEM)
            pubchem_cur = pubchem_conn.cursor()
            pubchem_cur.execute("""
                SELECT *
                FROM pubchem_cid_synonyms
                WHERE normalized_alias = ?
            """, (chemical_name_raw_norm,))
            pubchem_row = pubchem_cur.fetchone()
            ###
            if wcvp_row and pubchem_row:
                input_item['plant_name_scientific_canon'] = wcvp_row[3]
                input_item['plant_name_scientific_canon_norm'] = wcvp_row[4]
                input_item['chemical_name_canon'] = pubchem_row[1]
                input_item['chemical_name_canon_norm'] = pubchem_row[2]
                resolved_data.append(input_item)
                # print(json.dumps(input_item, indent=True))
                # quit()
        if resolved_data != []:
            io.json_write(output_filepath, resolved_data)
    wcvp_conn.close()
    pubchem_conn.close()

def resolve_synonyms(source_foldername):
    input_folderpath = f'{g.DATA_FOLDERPATH}/normalize/{source_foldername}/synonyms/json'
    output_folderpath = f'{g.DATA_FOLDERPATH}/resolve/{source_foldername}/synonyms/json'
    try: shutil.rmtree(output_folderpath)
    except: pass
    os.makedirs(output_folderpath, exist_ok=True)
    ###
    wcvp_folderpath = f'{g.DATA_FOLDERPATH}/reference/wcvp/wcvp.db'
    wcvp_conn = sqlite3.connect(wcvp_folderpath)
    ###
    input_filenames = os.listdir(input_folderpath)
    # print(input_filenames)
    for i, input_filename in enumerate(input_filenames[:]):
        print(f'{i}/{len(input_filenames)}')
        output_filepath = f'{output_folderpath}/{input_filename}'
        input_filepath = f'{input_folderpath}/{input_filename}'
        if os.path.exists(output_filepath): continue
        ###
        input_data = io.json_read(input_filepath)
        resolved_data = []
        for input_item in input_data:
            # print(json.dumps(input_item, indent=True))
            # quit()
            plant_name_normalized = input_item['plant_name_normalized']
            plant_synonym_normalized = input_item['plant_synonym_normalized']
            if plant_synonym_normalized == 'null': continue
            ### RESOLVE PLANT NAME (WCVP)
            wcvp_name_row = resolve_utils.resolve_plant_accepted(wcvp_conn, plant_name_normalized)
            ### RESOLVE PLANT SYNONYM (WCVP)
            wcvp_synonym_row = resolve_utils.resolve_plant_accepted(wcvp_conn, plant_synonym_normalized)
            ###
            if wcvp_name_row and wcvp_synonym_row:
                wcvp_name = wcvp_name_row[4]
                wcvp_synonym = wcvp_synonym_row[4]
                if wcvp_name != wcvp_synonym: continue
                # print(wcvp_name_row)
                # print(wcvp_synonym_row)
                # quit()
                wcvp_plant_name_id = wcvp_name_row[0]
                wcvp_accepted_plant_name_id = wcvp_name_row[1]
                wcvp_taxon_status = wcvp_name_row[2]
                wcvp_taxon_name = wcvp_name_row[3]
                wcvp_taxon_name_normalized = wcvp_name_row[4]
                ###
                resolved_item_new = input_item
                resolved_item_new['wcvp_taxon_name'] = wcvp_taxon_name
                resolved_item_new['wcvp_taxon_name_normalized'] = wcvp_taxon_name_normalized
                resolved_data.append(resolved_item_new)
                # print(json.dumps(resolved_item_new, indent=True))
                # quit()
        if resolved_data != []:
            io.json_write(output_filepath, resolved_data)
    wcvp_conn.close()

def resolve_common_names(source_foldername):
    input_folderpath = f'{g.DATA_FOLDERPATH}/normalize/{source_foldername}/names/json'
    output_folderpath = f'{g.DATA_FOLDERPATH}/resolve/{source_foldername}/names/json'
    try: shutil.rmtree(output_folderpath)
    except: pass
    os.makedirs(output_folderpath, exist_ok=True)
    ###
    wcvp_folderpath = f'{g.DATA_FOLDERPATH}/reference/wcvp/wcvp.db'
    wcvp_conn = sqlite3.connect(wcvp_folderpath)
    ###
    input_filenames = os.listdir(input_folderpath)
    # print(input_filenames)
    for i, input_filename in enumerate(input_filenames[:]):
        print(f'{i}/{len(input_filenames)}')
        output_filepath = f'{output_folderpath}/{input_filename}'
        input_filepath = f'{input_folderpath}/{input_filename}'
        if os.path.exists(output_filepath): continue
        input_data = io.json_read(input_filepath)
        ###
        resolved_data = []
        for input_item in input_data:
            # print(json.dumps(input_item, indent=4))
            # quit()
            plant_name_scientific_norm = input_item['plant_name_scientific_norm']
            ### RESOLVE PLANT NAME (WCVP)
            wcvp_row = resolve_utils.resolve_plant_accepted(wcvp_conn, plant_name_scientific_norm)
            ###
            if wcvp_row:
                # print(wcvp_name_row)
                # quit()
                input_item['wcvp_name_taxon'] = wcvp_row[3]
                input_item['wcvp_name_taxon_norm'] = wcvp_row[4]
                resolved_data.append(input_item)
                # print(json.dumps(input_item, indent=4))
                # quit()
        if resolved_data != []:
            io.json_write(output_filepath, resolved_data)
    wcvp_conn.close()

def resolve_traits(source_foldername):
    input_folderpath = f'{g.DATA_FOLDERPATH}/normalize/{source_foldername}/traits/json'
    output_folderpath = f'{g.DATA_FOLDERPATH}/resolve/{source_foldername}/traits/json'
    try: shutil.rmtree(output_folderpath)
    except: pass
    os.makedirs(output_folderpath, exist_ok=True)
    ###
    wcvp_folderpath = f'{g.DATA_FOLDERPATH}/reference/wcvp/wcvp.db'
    wcvp_conn = sqlite3.connect(wcvp_folderpath)
    ###
    input_filenames = os.listdir(input_folderpath)
    # print(input_filenames)
    for i, input_filename in enumerate(input_filenames[:]):
        print(f'{i}/{len(input_filenames)}')
        output_filepath = f'{output_folderpath}/{input_filename}'
        input_filepath = f'{input_folderpath}/{input_filename}'
        if os.path.exists(output_filepath): continue
        input_data = io.json_read(input_filepath)
        ###
        resolved_data = []
        for input_item in input_data:
            # print(json.dumps(input_item, indent=4))
            # quit()
            plant_name_scientific_norm = input_item['plant_name_scientific_norm']
            ### RESOLVE PLANT NAME (WCVP)
            wcvp_row = resolve_utils.resolve_plant_accepted(wcvp_conn, plant_name_scientific_norm)
            ###
            if wcvp_row:
                # print(wcvp_name_row)
                # quit()
                input_item['wcvp_name_taxon'] = wcvp_row[3]
                input_item['wcvp_name_taxon_norm'] = wcvp_row[4]
                resolved_data.append(input_item)
                # print(json.dumps(input_item, indent=4))
                # quit()
        if resolved_data != []:
            io.json_write(output_filepath, resolved_data)
    wcvp_conn.close()

def run():
    print('RESOLVE')

    if 0:
        start = time.perf_counter()
        resolve_synonyms(source_foldername='wcvp')
        print(f'resolve synonyms() - execution time: ', time.perf_counter() - start)

    if 0:
        start = time.perf_counter()
        resolve_common_names(source_foldername='wikidata')
        resolve_common_names(source_foldername='col')
        print(f'resolve common_names() - execution time: ', time.perf_counter() - start)

    if 1:
        start = time.perf_counter()
        resolve_traits(source_foldername='gift')
        print(f'resolve traits() - execution time: ', time.perf_counter() - start)

    if 0:
        start = time.perf_counter()
        resolve_plants_parts(source_foldername='pubmed')
        print(f'resolve plant_part() - execution time: ', time.perf_counter() - start)

    if 0:
        start = time.perf_counter()
        resolve_activities(source_foldername='drduke')
        resolve_activities(source_foldername='pubmed')
        print(f'resolve chemicals() - execution time: ', time.perf_counter() - start)

    if 0:
        start = time.perf_counter()
        resolve_chemicals(source_foldername='drduke')
        resolve_chemicals(source_foldername='pubmed')
        print(f'resolve chemicals() - execution time: ', time.perf_counter() - start)

