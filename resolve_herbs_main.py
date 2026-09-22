import os
import time
import json
import shutil
import sqlite3

from lib import g
from lib import io
from lib import llm

import resolve_utils

HUB_FOLDERPATH = f'''{g.DATA_FOLDERPATH}/herbs'''

def resolve_preparations(source_foldername):
    input_folderpath = f'{HUB_FOLDERPATH}/normalize/{source_foldername}/preparations/json'
    output_folderpath = f'{HUB_FOLDERPATH}/resolve/{source_foldername}/preparations/json'
    try: shutil.rmtree(output_folderpath)
    except: pass
    os.makedirs(output_folderpath, exist_ok=True)
    ###
    wcvp_filepath = f'{HUB_FOLDERPATH}/reference/wcvp/wcvp.db'
    wcvp_conn = sqlite3.connect(wcvp_filepath)
    wcvp_conn.row_factory = sqlite3.Row
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
            print(json.dumps(input_item, indent=True))
            # quit()
            plant_name_raw_normalize = input_item['plant_name_raw_normalize']
            ### RESOLVE PLANT (WCVP)
            wcvp_row = resolve_utils.resolve_plant_accepted(wcvp_conn, plant_name_raw_normalize)
            ###
            if wcvp_row:
                wcvp_item = dict(wcvp_row)
                input_item['plant_name_scientific_reference'] = wcvp_item['taxon_name']
                input_item['plant_name_scientific_reference_normalize'] = wcvp_item['taxon_name_normalized']
                input_item['preparation_name_reference'] = input_item['preparation_name_raw']
                input_item['preparation_name_reference_normalize'] = input_item['preparation_name_raw_normalize']
                resolved_data.append(input_item)
                # print(json.dumps(input_item, indent=True))
                # quit()
        if resolved_data != []:
            io.json_write(output_filepath, resolved_data)
    wcvp_conn.close()
    # print(json.dumps(resolved_data, indent=4))

def resolve_plants_parts(source_foldername):
    input_folderpath = f'{HUB_FOLDERPATH}/normalize/{source_foldername}/plants_parts/json'
    output_folderpath = f'{HUB_FOLDERPATH}/resolve/{source_foldername}/plants_parts/json'
    try: shutil.rmtree(output_folderpath)
    except: pass
    os.makedirs(output_folderpath, exist_ok=True)
    ###
    wcvp_filepath = f'{HUB_FOLDERPATH}/reference/wcvp/wcvp.db'
    wcvp_conn = sqlite3.connect(wcvp_filepath)
    wcvp_conn.row_factory = sqlite3.Row
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
            print(json.dumps(input_item, indent=True))
            # quit()
            plant_name_raw_normalize = input_item['plant_name_raw_normalize']
            ### RESOLVE PLANT (WCVP)
            wcvp_row = resolve_utils.resolve_plant_accepted(wcvp_conn, plant_name_raw_normalize)
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
                    if raw_val in input_item['plant_part_name_raw_normalize']:
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
                wcvp_item = dict(wcvp_row)
                input_item['plant_name_scientific_reference'] = wcvp_item['taxon_name']
                input_item['plant_name_scientific_reference_normalize'] = wcvp_item['taxon_name_normalized']
                input_item['plant_part_name_reference'] = plant_part_canon
                input_item['plant_part_name_reference_normalize'] = plant_part_canon
                resolved_data.append(input_item)
                # if plant_name_raw_norm == 'panax ginseng':
                    # print(json.dumps(input_item, indent=True))
                    # quit()
                # print(json.dumps(input_item, indent=True))
                # quit()
        if resolved_data != []:
            io.json_write(output_filepath, resolved_data)
    wcvp_conn.close()
    # print(json.dumps(resolved_data, indent=4))

def resolve_chemicals(source_foldername):
    input_folderpath = f'{HUB_FOLDERPATH}/normalize/{source_foldername}/chemicals/json'
    output_folderpath = f'{HUB_FOLDERPATH}/resolve/{source_foldername}/chemicals/json'
    try: shutil.rmtree(output_folderpath)
    except: pass
    os.makedirs(output_folderpath, exist_ok=True)
    ###
    wcvp_folderpath = f'{HUB_FOLDERPATH}/reference/wcvp/wcvp.db'
    pubchem_folderpath = f'{HUB_FOLDERPATH}/reference/pubchem/pubchem.db'
    wcvp_conn = sqlite3.connect(wcvp_folderpath)
    wcvp_conn.row_factory = sqlite3.Row
    pubchem_conn = sqlite3.connect(pubchem_folderpath)
    pubchem_conn.row_factory = sqlite3.Row
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
            # print(json.dumps(input_item, indent=4))
            # quit()
            resolved_item = input_item
            plant_name_raw_normalize = input_item['plant_name_raw_normalize']
            chemical_name_raw_normalize = input_item['chemical_name_raw_normalize']
            if chemical_name_raw_normalize == 'null':
                continue
            ### RESOLVE PLANT (WCVP)
            wcvp_row = resolve_utils.resolve_plant_accepted(wcvp_conn, plant_name_raw_normalize)
            ### RESOLVE CHEMICAL (PUBCHEM)
            pubchem_cur = pubchem_conn.cursor()
            pubchem_cur.execute("""
                SELECT *
                FROM pubchem_cid_synonyms
                WHERE alias_normalize = ?
            """, (chemical_name_raw_normalize,))
            # pubchem_row = pubchem_cur.fetchone()
            pubchem_rows = pubchem_cur.fetchall()
            pubchem_items = [dict(row) for row in pubchem_rows]
            ###
            if wcvp_row and pubchem_items:
                wcvp_item = dict(wcvp_row)
                pubchem_item = pubchem_items[0]
                # print(json.dumps(wcvp_item, indent=4))
                # print(json.dumps(pubchem_item, indent=4))
                # quit()
                input_item['plant_name_scientific_reference'] = wcvp_item['taxon_name']
                input_item['plant_name_scientific_reference_normalize'] = wcvp_item['taxon_name_normalized']
                input_item['chemical_name_reference'] = pubchem_item['alias']
                input_item['chemical_name_reference_normalize'] = pubchem_item['alias_normalize']
                resolved_data.append(input_item)
                # print(json.dumps(input_item, indent=True))
                # quit()
        if resolved_data != []:
            io.json_write(output_filepath, resolved_data)
    wcvp_conn.close()
    pubchem_conn.close()
    print(json.dumps(resolved_data[0], indent=True))
    # quit()

def resolve_conditions(source_foldername):
    input_folderpath = f'{HUB_FOLDERPATH}/normalize/{source_foldername}/conditions/json'
    output_folderpath = f'{HUB_FOLDERPATH}/resolve/{source_foldername}/conditions/json'
    try: shutil.rmtree(output_folderpath)
    except: pass
    os.makedirs(output_folderpath, exist_ok=True)
    ###
    wcvp_folderpath = f'{HUB_FOLDERPATH}/reference/wcvp/wcvp.db'
    wcvp_conn = sqlite3.connect(wcvp_folderpath)
    wcvp_conn.row_factory = sqlite3.Row
    mesh_folderpath = f'{HUB_FOLDERPATH}/reference/mesh/mesh.db'
    mesh_conn = sqlite3.connect(mesh_folderpath)
    mesh_conn.row_factory = sqlite3.Row
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
            # print(json.dumps(input_item, indent=4))
            # quit()
            resolved_item = input_item
            plant_name_raw_normalize = input_item['plant_name_raw_normalize']
            condition_name_raw_normalize = input_item['condition_name_raw_normalize']
            if condition_name_raw_normalize == 'null':
                continue
            ### RESOLVE PLANT (WCVP)
            wcvp_row = resolve_utils.resolve_plant_accepted(wcvp_conn, plant_name_raw_normalize)
            ### RESOLVE DISEASE (MESH)
            mesh_cur = mesh_conn.cursor()
            mesh_cur.execute("""
                SELECT *
                FROM diseases
                WHERE disease_name_normalize = ?
            """, (condition_name_raw_normalize,))
            mesh_rows = mesh_cur.fetchall()
            mesh_items = [dict(row) for row in mesh_rows]
            ###
            if wcvp_row and mesh_items:
                wcvp_item = dict(wcvp_row)
                mesh_item = mesh_items[0]
                # print(json.dumps(wcvp_item, indent=4))
                # print(json.dumps(pubchem_item, indent=4))
                # quit()
                input_item['plant_name_scientific_reference'] = wcvp_item['taxon_name']
                input_item['plant_name_scientific_reference_normalize'] = wcvp_item['taxon_name_normalized']
                input_item['condition_name_reference'] = mesh_item['disease_name']
                input_item['condition_name_reference_normalize'] = mesh_item['disease_name_normalize']
                resolved_data.append(input_item)
                # print(json.dumps(input_item, indent=True))
                # quit()
        if resolved_data != []:
            io.json_write(output_filepath, resolved_data)
    wcvp_conn.close()
    mesh_conn.close()
    print(json.dumps(resolved_data[0], indent=True))
    # quit()

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
    input_folderpath = f'{HUB_FOLDERPATH}/normalize/{source_foldername}/names/json'
    output_folderpath = f'{HUB_FOLDERPATH}/resolve/{source_foldername}/names/json'
    try: shutil.rmtree(output_folderpath)
    except: pass
    os.makedirs(output_folderpath, exist_ok=True)
    ###
    wcvp_folderpath = f'{HUB_FOLDERPATH}/reference/wcvp/wcvp.db'
    wcvp_conn = sqlite3.connect(wcvp_folderpath)
    wcvp_conn.row_factory = sqlite3.Row
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
            plant_name_scientific_reference_normalize = input_item['plant_name_scientific_reference_normalize']
            ### RESOLVE PLANT NAME (WCVP)
            wcvp_row = resolve_utils.resolve_plant_accepted(wcvp_conn, plant_name_scientific_reference_normalize)
            ###
            if wcvp_row:
                wcvp_item = dict(wcvp_row)
                # print(wcvp_item)
                # quit()
                input_item['wcvp_name_taxon'] = wcvp_row['taxon_name']
                input_item['wcvp_name_taxon_normalized'] = wcvp_row['taxon_name_normalized']
                resolved_data.append(input_item)
                # print(json.dumps(input_item, indent=4))
                # quit()
        if resolved_data != []:
            io.json_write(output_filepath, resolved_data)
    wcvp_conn.close()
    print(json.dumps(resolved_data[0], indent=4))
    # quit()

def resolve_distributions(source_foldername):
    input_folderpath = f'{HUB_FOLDERPATH}/normalize/{source_foldername}/distributions/json'
    output_folderpath = f'{HUB_FOLDERPATH}/resolve/{source_foldername}/distributions/json'
    try: shutil.rmtree(output_folderpath)
    except: pass
    os.makedirs(output_folderpath, exist_ok=True)
    ###
    wcvp_folderpath = f'{HUB_FOLDERPATH}/reference/wcvp/wcvp.db'
    wcvp_conn = sqlite3.connect(wcvp_folderpath)
    wcvp_conn.row_factory = sqlite3.Row
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
            plant_name_scientific_reference_normalize = input_item['plant_name_scientific_reference_normalize']
            ### RESOLVE PLANT NAME (WCVP)
            wcvp_row = resolve_utils.resolve_plant_accepted(wcvp_conn, plant_name_scientific_reference_normalize)
            ###
            if wcvp_row:
                wcvp_item = dict(wcvp_row)
                # print(wcvp_item)
                # quit()
                # input_item['wcvp_name_taxon'] = wcvp_row['taxon_name']
                # input_item['wcvp_name_taxon_normalized'] = wcvp_row['taxon_name_normalized']
                resolved_data.append(input_item)
                # print(json.dumps(input_item, indent=4))
                # quit()
        if resolved_data != []:
            io.json_write(output_filepath, resolved_data)
    wcvp_conn.close()
    print(json.dumps(resolved_data[0], indent=4))
    # quit()

def resolve_activities(source_foldername):
    input_folderpath = f'{HUB_FOLDERPATH}/normalize/{source_foldername}/activities/json'
    output_folderpath = f'{HUB_FOLDERPATH}/resolve/{source_foldername}/activities/json'
    try: shutil.rmtree(output_folderpath)
    except: pass
    os.makedirs(output_folderpath, exist_ok=True)
    ###
    wcvp_folderpath = f'{HUB_FOLDERPATH}/reference/wcvp/wcvp.db'
    wcvp_conn = sqlite3.connect(wcvp_folderpath)
    wcvp_conn.row_factory = sqlite3.Row
    drduke_folderpath = f'{HUB_FOLDERPATH}/reference/drduke/drduke.db'
    drduke_conn = sqlite3.connect(drduke_folderpath)
    drduke_conn.row_factory = sqlite3.Row
    ###
    input_filenames = os.listdir(input_folderpath)
    last_resolved_data = []
    for i, input_filename in enumerate(input_filenames[:]):
        print(f'{i}/{len(input_filenames)}')
        output_filepath = f'{output_folderpath}/{input_filename}'
        input_filepath = f'{input_folderpath}/{input_filename}'
        if os.path.exists(output_filepath): continue
        ###
        input_data = io.json_read(input_filepath)
        resolved_data = []
        for input_item in input_data[:]:
            # print(json.dumps(input_item, indent=True))
            # quit()
            plant_name_normalize = input_item['plant_name_normalize']
            activity_name_normalize = input_item['activity_name_normalize']
            # print(plant_name_normalize, '->', activity_name_normalize)
            # continue
            # quit()
            ### RESOLVE PLANT (WCVP)
            wcvp_row = resolve_utils.resolve_plant_accepted(wcvp_conn, plant_name_normalize)
            ### RESOLVE ACTIVITY (DRDUKE)
            drduke_cur = drduke_conn.cursor()
            drduke_cur.execute("""
                SELECT *
                FROM drduke_activities_names
                WHERE activity_name_normalize = ?
            """, (activity_name_normalize,))
            # drduke_row = drduke_cur.fetchone()
            drduke_rows = drduke_cur.fetchall()
            drduke_items = [dict(row) for row in drduke_rows]
            # if drduke_items != []:
                # print(drduke_items)
                # quit()
            # continue
            ###
            if wcvp_row and drduke_items != []:
                # print(wcvp_row)
                wcvp_item = dict(wcvp_row)
                drduke_item = drduke_items[0]
                input_item['plant_name_scientific_reference'] = wcvp_item['taxon_name']
                input_item['plant_name_scientific_reference_normalize'] = wcvp_item['taxon_name_normalized']
                input_item['activity_name_reference'] = drduke_item['activity_name_raw']
                input_item['activity_name_reference_normalize'] = drduke_item['activity_name_normalize']
                resolved_data.append(input_item)
                # print(json.dumps(input_item, indent=True))
                # quit()
            # else:
        if resolved_data != []:
            io.json_write(output_filepath, resolved_data)
            last_resolved_data = resolved_data
    wcvp_conn.close()
    drduke_conn.close()
    print(json.dumps(last_resolved_data[0], indent=4))
    # quit()

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
        resolve_traits(source_foldername='gift')
        print(f'resolve traits() - execution time: ', time.perf_counter() - start)


    if 1:
        start = time.perf_counter()
        resolve_distributions(source_foldername='wcvp')
        print(f'resolve distributions() - execution time: ', time.perf_counter() - start)

    if 1:
        start = time.perf_counter()
        # resolve_common_names(source_foldername='wikidata')
        resolve_common_names(source_foldername='col')
        print(f'resolve common_names() - execution time: ', time.perf_counter() - start)

    if 1:
        start = time.perf_counter()
        # resolve_activities(source_foldername='drduke')
        resolve_activities(source_foldername='pubmed')
        print(f'resolve activiries() - execution time: ', time.perf_counter() - start)

    if 1:
        start = time.perf_counter()
        # resolve_chemicals(source_foldername='drduke')
        resolve_chemicals(source_foldername='pubmed')
        print(f'resolve chemicals() - execution time: ', time.perf_counter() - start)

    if 1:
        start = time.perf_counter()
        resolve_conditions(source_foldername='pubmed')
        print(f'resolve chemicals() - execution time: ', time.perf_counter() - start)

    if 1:
        start = time.perf_counter()
        resolve_plants_parts(source_foldername='pubmed')
        print(f'resolve plant_parts() - execution time: ', time.perf_counter() - start)

    if 1:
        start = time.perf_counter()
        resolve_preparations(source_foldername='pubmed')
        print(f'resolve plant_preparations() - execution time: ', time.perf_counter() - start)
