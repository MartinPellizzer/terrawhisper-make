import os
import time
import json
import shutil
import sqlite3

from lib import g
from lib import io
from lib import llm

import resolve_utils
import schema_herbs

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
        print(f'RESOLVE PLANTS PREPARATIONS {i}/{len(input_filenames)}')
        output_filepath = f'{output_folderpath}/{input_filename}'
        input_filepath = f'{input_folderpath}/{input_filename}'
        if os.path.exists(output_filepath): continue
        ###
        input_data = io.json_read(input_filepath)
        resolved_data = []
        for input_item in input_data:
            # print(json.dumps(input_item, indent=True))
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
                # print(json.dumps(input_item, indent=4))
                # quit()
        if resolved_data != []:
            io.json_write(output_filepath, resolved_data)
    wcvp_conn.close()
    # print(json.dumps(resolved_data, indent=4))

def resolve_plants_parts(source_foldername):
    input_folderpath = f'{HUB_FOLDERPATH}/normalize/{source_foldername}/plants_plants_parts/json'
    output_folderpath = f'{HUB_FOLDERPATH}/resolve/{source_foldername}/plants_plants_parts/json'
    try: shutil.rmtree(output_folderpath)
    except: pass
    os.makedirs(output_folderpath, exist_ok=True)
    ###
    wcvp_filepath = f'{HUB_FOLDERPATH}/reference/wcvp/wcvp.db'
    wcvp_conn = sqlite3.connect(wcvp_filepath)
    wcvp_conn.row_factory = sqlite3.Row
    ###
    input_filenames = os.listdir(input_folderpath)
    last = []
    for i, input_filename in enumerate(input_filenames[:]):
        print(f'RESOLVE PLANTS PARTS {i}/{len(input_filenames)}')
        output_filepath = f'{output_folderpath}/{input_filename}'
        input_filepath = f'{input_folderpath}/{input_filename}'
        if os.path.exists(output_filepath): continue
        ###
        input_data = io.json_read(input_filepath)
        resolved_data = []
        for input_item in input_data:
            # print(json.dumps(input_item, indent=True))
            # quit()
            plant_name_scientific_raw_normalize = input_item['plant_name_scientific_raw_normalize']
            ### RESOLVE PLANT (WCVP)
            wcvp_row = resolve_utils.resolve_plant_accepted(wcvp_conn, plant_name_scientific_raw_normalize)
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
                # print(json.dumps(input_item, indent=4))
                # quit()
        if resolved_data != []:
            io.json_write(output_filepath, resolved_data)
            # print(json.dumps(resolved_data, indent=4))
            # quit()
            last = resolved_data
    wcvp_conn.close()
    print(json.dumps(last, indent=4))

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
        print(f'RESOLVE PLANTS CHEMICALS {i}/{len(input_filenames)}')
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

# ;jump
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
    ###
    mesh_folderpath = f'{HUB_FOLDERPATH}/reference/mesh/mesh.db'
    mesh_conn = sqlite3.connect(mesh_folderpath)
    mesh_conn.row_factory = sqlite3.Row
    ###
    input_filenames = os.listdir(input_folderpath)
    for i, input_filename in enumerate(input_filenames[:]):
        print(f'RESOLVE PLANTS CONDITIONS {i}/{len(input_filenames)}')
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
    input_folderpath = f'{HUB_FOLDERPATH}/normalize/{source_foldername}/synonyms/json'
    output_folderpath = f'{HUB_FOLDERPATH}/resolve/{source_foldername}/synonyms/json'
    try: shutil.rmtree(output_folderpath)
    except: pass
    os.makedirs(output_folderpath, exist_ok=True)
    ###
    wcvp_folderpath = f'{HUB_FOLDERPATH}/reference/wcvp/wcvp.db'
    wcvp_conn = sqlite3.connect(wcvp_folderpath)
    ###
    input_filenames = os.listdir(input_folderpath)
    # print(input_filenames)
    output_items_last = []
    for i, input_filename in enumerate(input_filenames[:]):
        print(f'RESOLVE PLANTS SYNONYMS {i}/{len(input_filenames)}')
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
                # print(wcvp_name_row)
                # quit()
                wcvp_name = wcvp_name_row[4]
                wcvp_synonym = wcvp_synonym_row[4]
                if wcvp_name != wcvp_synonym: continue
                # print(wcvp_name_row)
                # print(wcvp_synonym_row)
                # quit()
                # input_item['plant_name_scientific_reference'] = wcvp_item['taxon_name']
                # input_item['plant_name_scientific_reference_normalize'] = wcvp_item['taxon_name_normalized']
                # input_item['condition_name_reference'] = mesh_item['disease_name']
                # input_item['condition_name_reference_normalize'] = mesh_item['disease_name_normalize']
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
        if resolved_data != []: output_items_last = resolved_data
    print(json.dumps(output_items_last, indent=4))
    wcvp_conn.close()

def resolve_common_names(source_foldername):
    input_folderpath = f'{HUB_FOLDERPATH}/normalize/{source_foldername}/plants_names_common/json'
    output_folderpath = f'{HUB_FOLDERPATH}/resolve/{source_foldername}/plants_names_common/json'
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
        print(f'RESOLVE PLANTS COMMON NAMES {i}/{len(input_filenames)}')
        output_filepath = f'{output_folderpath}/{input_filename}'
        input_filepath = f'{input_folderpath}/{input_filename}'
        if os.path.exists(output_filepath): continue
        input_data = io.json_read(input_filepath)
        ###
        resolved_data = []
        for input_item in input_data:
            # print(json.dumps(input_item, indent=4))
            # quit()
            plant_name_scientific_raw_normalize = input_item['plant_name_scientific_raw_normalize']
            ### RESOLVE PLANT NAME (WCVP)
            wcvp_row = resolve_utils.resolve_plant_accepted(wcvp_conn, plant_name_scientific_raw_normalize)
            ###
            if wcvp_row:
                wcvp_item = dict(wcvp_row)
                # print(wcvp_item)
                # quit()
                input_item['plant_name_scientific_reference'] = wcvp_row['taxon_name']
                input_item['plant_name_scientific_reference_normalized'] = wcvp_row['taxon_name_normalized']
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
    last = []
    for i, input_filename in enumerate(input_filenames[:]):
        print(f'RESOLVE PLANTS DISTRIBUTIONS {i}/{len(input_filenames)}')
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
            last = resolved_data
    wcvp_conn.close()
    print(json.dumps(last, indent=4))
    # quit()

def resolve_activities(source_foldername):
    input_folderpath = f'{HUB_FOLDERPATH}/normalize/{source_foldername}/plants_activities/json'
    output_folderpath = f'{HUB_FOLDERPATH}/resolve/{source_foldername}/plants_activities/json'
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
        print(f'RESOLVE PLANTS plants_activities {i}/{len(input_filenames)}')
        output_filepath = f'{output_folderpath}/{input_filename}'
        input_filepath = f'{input_folderpath}/{input_filename}'
        if os.path.exists(output_filepath): continue
        ###
        input_data = io.json_read(input_filepath)
        resolved_data = []
        for input_item in input_data[:]:
            # print(json.dumps(input_item, indent=True))
            # quit()
            plant_name_scientific_raw_normalize = input_item['plant_name_scientific_raw_normalize']
            activity_name_raw_normalize = input_item['activity_name_raw_normalize']
            # print(plant_name_scientific_raw_normalize, '->', activity_name_raw_normalize)
            # continue
            # quit()
            ### RESOLVE PLANT (WCVP)
            wcvp_row = resolve_utils.resolve_plant_accepted(wcvp_conn, plant_name_scientific_raw_normalize)
            ### RESOLVE ACTIVITY (DRDUKE)
            drduke_cur = drduke_conn.cursor()
            drduke_cur.execute("""
                SELECT *
                FROM drduke_activities_names
                WHERE activity_name_normalize = ?
            """, (activity_name_raw_normalize,))
            # drduke_row = drduke_cur.fetchone()
            drduke_rows = drduke_cur.fetchall()
            drduke_items = [dict(row) for row in drduke_rows]
            # if drduke_items != []:
                # print(drduke_items)
                # quit()
            # else:
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
    input_folderpath = f'{HUB_FOLDERPATH}/normalize/{source_foldername}/traits/json'
    output_folderpath = f'{HUB_FOLDERPATH}/resolve/{source_foldername}/traits/json'
    try: shutil.rmtree(output_folderpath)
    except: pass
    os.makedirs(output_folderpath, exist_ok=True)
    ###
    wcvp_folderpath = f'{HUB_FOLDERPATH}/reference/wcvp/wcvp.db'
    wcvp_conn = sqlite3.connect(wcvp_folderpath)
    ###
    input_filenames = os.listdir(input_folderpath)
    # print(input_filenames)
    for i, input_filename in enumerate(input_filenames[:]):
        print(f'RESOLVE PLANTS TRAITS {i}/{len(input_filenames)}')
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
    print(json.dumps(input_item, indent=4))

def resolve_taxonomies(source_foldername):
    input_folderpath = f'{HUB_FOLDERPATH}/normalize/{source_foldername}/taxonomies/json'
    output_folderpath = f'{HUB_FOLDERPATH}/resolve/{source_foldername}/taxonomies/json'
    try: shutil.rmtree(output_folderpath)
    except: pass
    os.makedirs(output_folderpath, exist_ok=True)
    ###
    wcvp_folderpath = f'{HUB_FOLDERPATH}/reference/wcvp/wcvp.db'
    wcvp_conn = sqlite3.connect(wcvp_folderpath)
    ###
    input_filenames = os.listdir(input_folderpath)
    # print(input_filenames)
    for i, input_filename in enumerate(input_filenames[:]):
        print(f'RESOLVE PLANTS TAXONOMIES {i}/{len(input_filenames)}')
        output_filepath = f'{output_folderpath}/{input_filename}'
        input_filepath = f'{input_folderpath}/{input_filename}'
        if os.path.exists(output_filepath): continue
        input_data = io.json_read(input_filepath)
        ###
        resolved_data = []
        for input_item in input_data:
            # print(json.dumps(input_item, indent=4))
            # quit()
            plant_name_scientific_reference_normalize = input_item['plant_name_scientific_raw_normalize']
            ### RESOLVE PLANT TAXONOMIES TODO?
            wcvp_row = resolve_utils.resolve_plant_accepted(wcvp_conn, plant_name_scientific_reference_normalize)
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
    print(json.dumps(input_item, indent=4))

def resolve_compounds(source_foldername):
    input_folderpath = f'{HUB_FOLDERPATH}/normalize/{source_foldername}/plants_compounds/json'
    output_folderpath = f'{HUB_FOLDERPATH}/resolve/{source_foldername}/plants_compounds/json'
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
        print(f'RESOLVE PLANTS plants_compounds {i}/{len(input_filenames)}')
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
            plant_name_scientific_raw_normalize = input_item['plant_name_scientific_raw_normalize']
            compound_name_raw_normalize = input_item['compound_name_raw_normalize']
            if compound_name_raw_normalize == 'null': continue
            ### RESOLVE PLANT (WCVP)
            wcvp_row = resolve_utils.resolve_plant_accepted(wcvp_conn, plant_name_scientific_raw_normalize)
            ### RESOLVE CHEMICAL (PUBCHEM)
            pubchem_cur = pubchem_conn.cursor()
            pubchem_cur.execute("""
                SELECT *
                FROM pubchem_cid_synonyms
                WHERE alias_normalize = ?
            """, (compound_name_raw_normalize,))
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
                input_item['compound_name_reference'] = pubchem_item['alias']
                input_item['compound_name_reference_normalize'] = pubchem_item['alias_normalize']
                resolved_data.append(input_item)
                # print(json.dumps(input_item, indent=True))
                # quit()
        if resolved_data != []:
            io.json_write(output_filepath, resolved_data)
    wcvp_conn.close()
    pubchem_conn.close()
    print(json.dumps(resolved_data[0], indent=True))
    # quit()


def resolve_gen(entity_1, entity_2, source_foldername, output_foldername):
    input_folderpath = f'{HUB_FOLDERPATH}/normalize/{source_foldername}/{output_foldername}/json'
    output_folderpath = f'{HUB_FOLDERPATH}/resolve/{source_foldername}/{output_foldername}/json'
    try: shutil.rmtree(output_folderpath)
    except: pass
    os.makedirs(output_folderpath, exist_ok=True)
    ###
    wcvp_filepath = f'{HUB_FOLDERPATH}/reference/wcvp/wcvp.db'
    wcvp_conn = sqlite3.connect(wcvp_filepath)
    wcvp_conn.row_factory = sqlite3.Row
    input_filenames = os.listdir(input_folderpath)
    last = []
    for i, input_filename in enumerate(input_filenames[:]):
        print(f'RESOLVE {entity_1} {entity_2} {i}/{len(input_filenames)}')
        output_filepath = f'{output_folderpath}/{input_filename}'
        input_filepath = f'{input_folderpath}/{input_filename}'
        if os.path.exists(output_filepath): continue
        ###
        input_data = io.json_read(input_filepath)
        resolved_data = []
        for input_item in input_data:
            # print(json.dumps(input_item, indent=True))
            plant_name_scientific_raw_normalize = input_item['plant_name_scientific_raw_normalize']
            ### RESOLVE PLANT (WCVP)
            wcvp_row = resolve_utils.resolve_plant_accepted(wcvp_conn, plant_name_scientific_raw_normalize)
            ###
            if wcvp_row:
                wcvp_item = dict(wcvp_row)
                # print(wcvp_item)
                # quit()
                input_item[f'{entity_1}_reference'] = wcvp_item[f'taxon_name']
                input_item[f'{entity_1}_reference_normalize'] = wcvp_item[f'taxon_name_normalized']
                input_item[f'{entity_2}_reference'] = input_item[f'{entity_2}_raw']
                input_item[f'{entity_2}_reference_normalize'] = input_item[f'{entity_2}_raw_normalize']
                resolved_data.append(input_item)
                # print(json.dumps(input_item, indent=4))
                # quit()
        if resolved_data != []:
            io.json_write(output_filepath, resolved_data)
            last = resolved_data 
    wcvp_conn.close()
    print(json.dumps(last, indent=4))

def schema_resolve_gen(schema_item):
    schema_table_name = schema_item['table_name']
    schema_source_name = schema_item['sources'][0]['source_name']
    schema_output_foldername = schema_table_name
    schema_entity_1_val = schema_item['fields'][0]['field_name']
    schema_relationship_val = schema_item['fields'][1]['field_name']
    schema_entity_2_val = schema_item['fields'][2]['field_name']
    ###
    input_folderpath = f'{HUB_FOLDERPATH}/normalize/{schema_source_name}/{schema_output_foldername}/json'
    output_folderpath = f'{HUB_FOLDERPATH}/resolve/{schema_source_name}/{schema_output_foldername}/json'
    if schema_item['regen'] == True:
        try: shutil.rmtree(output_folderpath)
        except: pass
    os.makedirs(output_folderpath, exist_ok=True)
    ###
    wcvp_filepath = f'{HUB_FOLDERPATH}/reference/wcvp/wcvp.db'
    wcvp_conn = sqlite3.connect(wcvp_filepath)
    wcvp_conn.row_factory = sqlite3.Row
    input_filenames = os.listdir(input_folderpath)
    last = []
    for i, input_filename in enumerate(input_filenames[:]):
        print(f'RESOLVE {schema_entity_1_val} {schema_entity_2_val} - {i}/{len(input_filenames)}')
        output_filepath = f'{output_folderpath}/{input_filename}'
        input_filepath = f'{input_folderpath}/{input_filename}'
        if os.path.exists(output_filepath): continue
        ###
        input_data = io.json_read(input_filepath)
        resolved_data = []
        for input_item in input_data:
            # print(json.dumps(input_item, indent=True))
            plant_name_scientific_raw_normalize = input_item['plant_name_scientific_raw_normalize']
            ### RESOLVE PLANT (WCVP)
            wcvp_row = resolve_utils.resolve_plant_accepted(wcvp_conn, plant_name_scientific_raw_normalize)
            ###
            if wcvp_row:
                wcvp_item = dict(wcvp_row)
                # print(wcvp_item)
                # quit()
                input_item[f'{schema_entity_1_val}_reference'] = wcvp_item[f'taxon_name']
                input_item[f'{schema_entity_1_val}_reference_normalize'] = wcvp_item[f'taxon_name_normalized']
                input_item[f'{schema_entity_2_val}_reference'] = input_item[f'{schema_entity_2_val}_raw']
                input_item[f'{schema_entity_2_val}_reference_normalize'] = input_item[f'{schema_entity_2_val}_raw_normalize']
                resolved_data.append(input_item)
                # print(json.dumps(input_item, indent=4))
                # quit()
        if resolved_data != []:
            io.json_write(output_filepath, resolved_data)
            last = resolved_data 
    wcvp_conn.close()
    print(json.dumps(last, indent=4))

def studies_resolve(source_foldername):
    input_folderpath = f'{HUB_FOLDERPATH}/normalize/{source_foldername}/studies/json'
    output_folderpath = f'{HUB_FOLDERPATH}/resolve/{source_foldername}/studies/json'
    try: shutil.rmtree(output_folderpath)
    except: pass
    os.makedirs(output_folderpath, exist_ok=True)
    ###
    input_filenames = os.listdir(input_folderpath)
    last_resolved_data = []
    for i, input_filename in enumerate(input_filenames[:]):
        print(f'RESOLVE PLANTS studies {i}/{len(input_filenames)}')
        output_filepath = f'{output_folderpath}/{input_filename}'
        input_filepath = f'{input_folderpath}/{input_filename}'
        if os.path.exists(output_filepath): continue
        ###
        input_data = io.json_read(input_filepath)
        resolved_data = []
        for input_item in input_data[:]:
            # print(json.dumps(input_item, indent=True))
            # quit()
            input_item['study_title_reference_normalize'] = input_item['study_title_raw_normalize']
            resolved_data.append(input_item)
            # print(json.dumps(input_item, indent=True))
            # quit()
        if resolved_data != []:
            io.json_write(output_filepath, resolved_data)
            last_resolved_data = resolved_data
    print(json.dumps(last_resolved_data[0], indent=4))
    # quit()

def plants_resolve(source_foldername):
    input_folderpath = f'{HUB_FOLDERPATH}/normalize/{source_foldername}/plants/json'
    output_folderpath = f'{HUB_FOLDERPATH}/resolve/{source_foldername}/plants/json'
    try: shutil.rmtree(output_folderpath)
    except: pass
    os.makedirs(output_folderpath, exist_ok=True)
    ###
    wcvp_folderpath = f'{HUB_FOLDERPATH}/reference/wcvp/wcvp.db'
    wcvp_conn = sqlite3.connect(wcvp_folderpath)
    wcvp_conn.row_factory = sqlite3.Row
    ###
    input_filenames = os.listdir(input_folderpath)
    last_resolved_data = []
    for i, input_filename in enumerate(input_filenames[:]):
        print(f'RESOLVE PLANTS plants {i}/{len(input_filenames)}')
        output_filepath = f'{output_folderpath}/{input_filename}'
        input_filepath = f'{input_folderpath}/{input_filename}'
        if os.path.exists(output_filepath): continue
        ###
        input_data = io.json_read(input_filepath)
        resolved_data = []
        for input_item in input_data[:]:
            # print(json.dumps(input_item, indent=True))
            # quit()
            plant_name_scientific_raw_normalize = input_item['plant_name_scientific_raw_normalize']
            wcvp_row = resolve_utils.resolve_plant_accepted(wcvp_conn, plant_name_scientific_raw_normalize)
            ###
            if wcvp_row:
                wcvp_item = dict(wcvp_row)
                input_item['plant_name_scientific_reference'] = wcvp_item['taxon_name']
                input_item['plant_name_scientific_reference_normalize'] = wcvp_item['taxon_name_normalized']
                resolved_data.append(input_item)
                # print(json.dumps(input_item, indent=True))
                # quit()
        if resolved_data != []:
            io.json_write(output_filepath, resolved_data)
            last_resolved_data = resolved_data
    wcvp_conn.close()
    print(json.dumps(last_resolved_data[0], indent=4))
    # quit()

def activities_resolve(source_foldername):
    input_folderpath = f'{HUB_FOLDERPATH}/normalize/{source_foldername}/activities/json'
    output_folderpath = f'{HUB_FOLDERPATH}/resolve/{source_foldername}/activities/json'
    try: shutil.rmtree(output_folderpath)
    except: pass
    os.makedirs(output_folderpath, exist_ok=True)
    ###
    drduke_folderpath = f'{HUB_FOLDERPATH}/reference/drduke/drduke.db'
    drduke_conn = sqlite3.connect(drduke_folderpath)
    drduke_conn.row_factory = sqlite3.Row
    ###
    input_filenames = os.listdir(input_folderpath)
    last_resolved_data = []
    for i, input_filename in enumerate(input_filenames[:]):
        print(f'RESOLVE HERBS activities {i}/{len(input_filenames)}')
        output_filepath = f'{output_folderpath}/{input_filename}'
        input_filepath = f'{input_folderpath}/{input_filename}'
        if os.path.exists(output_filepath): continue
        ###
        input_data = io.json_read(input_filepath)
        resolved_data = []
        for input_item in input_data[:]:
            # print(json.dumps(input_item, indent=True))
            # quit()
            ###
            activity_name_raw_normalize = input_item['activity_name_raw_normalize']
            drduke_cur = drduke_conn.cursor()
            drduke_cur.execute("""
                SELECT *
                FROM drduke_activities_names
                WHERE activity_name_normalize = ?
            """, (activity_name_raw_normalize,))
            drduke_rows = drduke_cur.fetchall()
            drduke_items = [dict(row) for row in drduke_rows]
            ###
            if drduke_rows:
                drduke_item = drduke_items[0]
                input_item['activity_name_reference'] = drduke_item['activity_name_raw']
                input_item['activity_name_reference_normalize'] = drduke_item['activity_name_normalize']
                resolved_data.append(input_item)
                # print(json.dumps(input_item, indent=4))
                # quit()
        if resolved_data != []:
            io.json_write(output_filepath, resolved_data)
            last_resolved_data = resolved_data
    drduke_conn.close()
    print(json.dumps(last_resolved_data[0], indent=4))
    # quit()

def conditions_resolve(source_foldername):
    input_folderpath = f'{HUB_FOLDERPATH}/normalize/{source_foldername}/conditions/json'
    output_folderpath = f'{HUB_FOLDERPATH}/resolve/{source_foldername}/conditions/json'
    try: shutil.rmtree(output_folderpath)
    except: pass
    os.makedirs(output_folderpath, exist_ok=True)
    ###
    mesh_folderpath = f'{HUB_FOLDERPATH}/reference/mesh/mesh.db'
    mesh_conn = sqlite3.connect(mesh_folderpath)
    mesh_conn.row_factory = sqlite3.Row
    ###
    input_filenames = os.listdir(input_folderpath)
    last_resolved_data = []
    failed_resolved = 0
    failed_data = 0
    succeded_data = 0
    for i, input_filename in enumerate(input_filenames[:]):
        print(f'RESOLVE HERBS conditions {i}/{len(input_filenames)}')
        output_filepath = f'{output_folderpath}/{input_filename}'
        input_filepath = f'{input_folderpath}/{input_filename}'
        if os.path.exists(output_filepath): continue
        ###
        input_data = io.json_read(input_filepath)
        resolved_data = []
        for input_item in input_data[:]:
            # print(json.dumps(input_item, indent=True))
            # quit()
            ###
            condition_name_raw_normalize = input_item['condition_name_raw_normalize']
            if condition_name_raw_normalize == 'null': continue
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
            if mesh_items:
                mesh_item = mesh_items[0]
                input_item['condition_name_reference'] = mesh_item['disease_name']
                input_item['condition_name_reference_normalize'] = mesh_item['disease_name_normalize']
                resolved_data.append(input_item)
                # print(json.dumps(input_item, indent=4))
                # quit()
        if resolved_data != []:
            io.json_write(output_filepath, resolved_data)
            last_resolved_data = resolved_data
    mesh_conn.close()
    print(json.dumps(last_resolved_data[0], indent=4))
    # quit()

def compounds_resolve(source_foldername):
    table_name = 'compounds'
    input_folderpath = f'{HUB_FOLDERPATH}/normalize/{source_foldername}/{table_name}/json'
    output_folderpath = f'{HUB_FOLDERPATH}/resolve/{source_foldername}/{table_name}/json'
    try: shutil.rmtree(output_folderpath)
    except: pass
    os.makedirs(output_folderpath, exist_ok=True)
    ###
    pubchem_folderpath = f'{HUB_FOLDERPATH}/reference/pubchem/pubchem.db'
    pubchem_conn = sqlite3.connect(pubchem_folderpath)
    pubchem_conn.row_factory = sqlite3.Row
    ###
    input_filenames = os.listdir(input_folderpath)
    last_resolved_data = []
    failed_resolved = 0
    failed_data = 0
    succeded_data = 0
    for i, input_filename in enumerate(input_filenames[:]):
        print(f'RESOLVE HERBS {table_name} {i}/{len(input_filenames)}')
        output_filepath = f'{output_folderpath}/{input_filename}'
        input_filepath = f'{input_folderpath}/{input_filename}'
        if os.path.exists(output_filepath): continue
        ###
        input_data = io.json_read(input_filepath)
        resolved_data = []
        for input_item in input_data[:]:
            # print(json.dumps(input_item, indent=True))
            # quit()
            ###
            compound_name_raw_normalize = input_item['compound_name_raw_normalize']
            if compound_name_raw_normalize == 'null': continue
            ### RESOLVE CHEMICAL (PUBCHEM)
            pubchem_cur = pubchem_conn.cursor()
            pubchem_cur.execute("""
                SELECT *
                FROM pubchem_cid_synonyms
                WHERE alias_normalize = ?
            """, (compound_name_raw_normalize,))
            # pubchem_row = pubchem_cur.fetchone()
            pubchem_rows = pubchem_cur.fetchall()
            pubchem_items = [dict(row) for row in pubchem_rows]
            ###
            if pubchem_items:
                pubchem_item = pubchem_items[0]
                input_item['compound_name_reference'] = pubchem_item['alias']
                input_item['compound_name_reference_normalize'] = pubchem_item['alias_normalize']
                resolved_data.append(input_item)
                # print(json.dumps(input_item, indent=4))
                # quit()
        if resolved_data != []:
            io.json_write(output_filepath, resolved_data)
            last_resolved_data = resolved_data
    pubchem_conn.close()
    print(json.dumps(last_resolved_data[0], indent=4))
    # quit()

def preparations_resolve(source_foldername):
    table_name = 'preparations'
    input_folderpath = f'{HUB_FOLDERPATH}/normalize/{source_foldername}/{table_name}/json'
    output_folderpath = f'{HUB_FOLDERPATH}/resolve/{source_foldername}/{table_name}/json'
    try: shutil.rmtree(output_folderpath)
    except: pass
    os.makedirs(output_folderpath, exist_ok=True)
    ###
    ref_folderpath = f'{HUB_FOLDERPATH}/reference/manual/manual.db'
    ref_conn = sqlite3.connect(ref_folderpath)
    ref_conn.row_factory = sqlite3.Row
    ###
    input_filenames = os.listdir(input_folderpath)
    last_resolved_data = []
    failed_resolved = 0
    failed_data = 0
    succeded_data = 0
    for i, input_filename in enumerate(input_filenames[:]):
        print(f'RESOLVE HERBS {table_name} {i}/{len(input_filenames)}')
        output_filepath = f'{output_folderpath}/{input_filename}'
        input_filepath = f'{input_folderpath}/{input_filename}'
        if os.path.exists(output_filepath): continue
        ###
        input_data = io.json_read(input_filepath)
        resolved_data = []
        for input_item in input_data[:]:
            # print(json.dumps(input_item, indent=True))
            # quit()
            ### RESOLVE PREPARATIONS (MANUAL)
            preparation_name_raw_normalize = input_item['preparation_name_raw_normalize']
            ref_cur = ref_conn.cursor()
            ref_cur.execute("""
                SELECT *
                FROM ref__preparations
                WHERE ref_preparation_name_normalize = ?
            """, (preparation_name_raw_normalize,))
            ref_rows = ref_cur.fetchall()
            ref_items = [dict(row) for row in ref_rows]
            ###
            if ref_items:
                ref_item = ref_items[0]
                input_item['preparation_name_reference'] = ref_item['ref_preparation_name']
                input_item['preparation_name_reference_normalize'] = ref_item['ref_preparation_name_normalize']
                resolved_data.append(input_item)
                # print(json.dumps(input_item, indent=4))
                # quit()
        if resolved_data != []:
            io.json_write(output_filepath, resolved_data)
            last_resolved_data = resolved_data
    # pubchem_conn.close()
    print(json.dumps(last_resolved_data[0], indent=4))
    # quit()

def parts_resolve(source_foldername):
    table_name = 'parts'
    input_folderpath = f'{HUB_FOLDERPATH}/normalize/{source_foldername}/{table_name}/json'
    output_folderpath = f'{HUB_FOLDERPATH}/resolve/{source_foldername}/{table_name}/json'
    try: shutil.rmtree(output_folderpath)
    except: pass
    os.makedirs(output_folderpath, exist_ok=True)
    ###
    ref_folderpath = f'{HUB_FOLDERPATH}/reference/manual/manual.db'
    ref_conn = sqlite3.connect(ref_folderpath)
    ref_conn.row_factory = sqlite3.Row
    ###
    input_filenames = os.listdir(input_folderpath)
    last_resolved_data = []
    failed_resolved = 0
    failed_data = 0
    succeded_data = 0
    for i, input_filename in enumerate(input_filenames[:]):
        print(f'RESOLVE HERBS {table_name} {i}/{len(input_filenames)}')
        output_filepath = f'{output_folderpath}/{input_filename}'
        input_filepath = f'{input_folderpath}/{input_filename}'
        if os.path.exists(output_filepath): continue
        ###
        input_data = io.json_read(input_filepath)
        resolved_data = []
        for input_item in input_data[:]:
            part_name_raw_normalize = input_item['part_name_raw_normalize']
            # print(json.dumps(input_item, indent=True))
            # quit()
            ### RESOLVE PARTS (MANUAL)
            ref_cur = ref_conn.cursor()
            ref_cur.execute("""
                SELECT *
                FROM ref__parts
                WHERE ref_part_name_normalize = ?
            """, (part_name_raw_normalize,))
            ref_rows = ref_cur.fetchall()
            ref_items = [dict(row) for row in ref_rows]
            ###
            if ref_items:
                ref_item = ref_items[0]
                input_item['part_name_reference'] = ref_item['ref_part_name']
                input_item['part_name_reference_normalize'] = ref_item['ref_part_name_normalize']
                resolved_data.append(input_item)
                # print(json.dumps(input_item, indent=4))
                # quit()
        if resolved_data != []:
            io.json_write(output_filepath, resolved_data)
            last_resolved_data = resolved_data
    ref_conn.close()
    print(json.dumps(last_resolved_data[0], indent=4))
    # quit()

def resolve__plants_names_common(source_foldername):
    input_folderpath = f'{HUB_FOLDERPATH}/normalize/{source_foldername}/plants_names_common/json'
    output_folderpath = f'{HUB_FOLDERPATH}/resolve/{source_foldername}/plants_names_common/json'
    try: shutil.rmtree(output_folderpath)
    except: pass
    os.makedirs(output_folderpath, exist_ok=True)
    ###
    input_filenames = os.listdir(input_folderpath)
    last_resolved_data = []
    for i, input_filename in enumerate(input_filenames[:]):
        print(f'RESOLVE HERBS plants names common {i}/{len(input_filenames)}')
        output_filepath = f'{output_folderpath}/{input_filename}'
        input_filepath = f'{input_folderpath}/{input_filename}'
        if os.path.exists(output_filepath): continue
        ###
        input_data = io.json_read(input_filepath)
        resolved_data = []
        for input_item in input_data[:]:
            # print(json.dumps(input_item, indent=True))
            # quit()
            ###
            plant_name_common_raw_normalize = input_item['plant_name_common_raw_normalize']
            if plant_name_common_raw_normalize == 'null': continue
            ###
            if True:
                input_item['plant_name_common_reference'] = input_item['plant_name_common_raw']
                input_item['plant_name_common_reference_normalize'] = input_item['plant_name_common_raw_normalize']
                resolved_data.append(input_item)
                # print(json.dumps(input_item, indent=4))
                # quit()
        if resolved_data != []:
            io.json_write(output_filepath, resolved_data)
            last_resolved_data = resolved_data
    print(json.dumps(last_resolved_data[0], indent=4))
    # quit()

def plants_activities_resolve(source_foldername):
    input_folderpath = f'{HUB_FOLDERPATH}/normalize/{source_foldername}/plants_activities/json'
    output_folderpath = f'{HUB_FOLDERPATH}/resolve/{source_foldername}/plants_activities/json'
    try: shutil.rmtree(output_folderpath)
    except: pass
    os.makedirs(output_folderpath, exist_ok=True)
    ###
    wcvp_folderpath = f'{HUB_FOLDERPATH}/reference/wcvp/wcvp.db'
    wcvp_conn = sqlite3.connect(wcvp_folderpath)
    wcvp_conn.row_factory = sqlite3.Row
    ###
    drduke_folderpath = f'{HUB_FOLDERPATH}/reference/drduke/drduke.db'
    drduke_conn = sqlite3.connect(drduke_folderpath)
    drduke_conn.row_factory = sqlite3.Row
    ###
    input_filenames = os.listdir(input_folderpath)
    last_resolved_data = []
    for i, input_filename in enumerate(input_filenames[:]):
        print(f'RESOLVE HERBS plants_activities {i}/{len(input_filenames)}')
        output_filepath = f'{output_folderpath}/{input_filename}'
        input_filepath = f'{input_folderpath}/{input_filename}'
        if os.path.exists(output_filepath): continue
        ###
        input_data = io.json_read(input_filepath)
        resolved_data = []
        for input_item in input_data[:]:
            # print(json.dumps(input_item, indent=True))
            # quit()
            plant_name_scientific_raw_normalize = input_item['plant_name_scientific_raw_normalize']
            wcvp_row = resolve_utils.resolve_plant_accepted(wcvp_conn, plant_name_scientific_raw_normalize)
            ###
            activity_name_raw_normalize = input_item['activity_name_raw_normalize']
            drduke_cur = drduke_conn.cursor()
            drduke_cur.execute("""
                SELECT *
                FROM drduke_activities_names
                WHERE activity_name_normalize = ?
            """, (activity_name_raw_normalize,))
            drduke_rows = drduke_cur.fetchall()
            drduke_items = [dict(row) for row in drduke_rows]
            ###
            if wcvp_row and drduke_rows:
                wcvp_item = dict(wcvp_row)
                input_item['plant_name_scientific_reference'] = wcvp_item['taxon_name']
                input_item['plant_name_scientific_reference_normalize'] = wcvp_item['taxon_name_normalized']
                ###
                drduke_item = drduke_items[0]
                input_item['activity_name_reference'] = drduke_item['activity_name_raw']
                input_item['activity_name_reference_normalize'] = drduke_item['activity_name_normalize']
                resolved_data.append(input_item)
                # print(json.dumps(input_item, indent=4))
                # quit()
        if resolved_data != []:
            io.json_write(output_filepath, resolved_data)
            last_resolved_data = resolved_data
    drduke_conn.close()
    print(json.dumps(last_resolved_data[0], indent=4))
    # quit()

def resolve__plants__activities(source_foldername):
    input_folderpath = f'{HUB_FOLDERPATH}/normalize/{source_foldername}/plants__activities/json'
    output_folderpath = f'{HUB_FOLDERPATH}/resolve/{source_foldername}/plants__activities/json'
    try: shutil.rmtree(output_folderpath)
    except: pass
    os.makedirs(output_folderpath, exist_ok=True)
    ###
    wcvp_folderpath = f'{HUB_FOLDERPATH}/reference/wcvp/wcvp.db'
    wcvp_conn = sqlite3.connect(wcvp_folderpath)
    wcvp_conn.row_factory = sqlite3.Row
    ###
    drduke_folderpath = f'{HUB_FOLDERPATH}/reference/drduke/drduke.db'
    drduke_conn = sqlite3.connect(drduke_folderpath)
    drduke_conn.row_factory = sqlite3.Row
    ###
    input_filenames = os.listdir(input_folderpath)
    last_resolved_data = []
    for i, input_filename in enumerate(input_filenames[:]):
        print(f'RESOLVE HERBS plants_activities {i}/{len(input_filenames)}')
        output_filepath = f'{output_folderpath}/{input_filename}'
        input_filepath = f'{input_folderpath}/{input_filename}'
        if os.path.exists(output_filepath): continue
        ###
        input_data = io.json_read(input_filepath)
        resolved_data = []
        for input_item in input_data[:]:
            # print(json.dumps(input_item, indent=True))
            # quit()
            plant_name_scientific_raw_normalize = input_item['plant_name_scientific_raw_normalize']
            wcvp_row = resolve_utils.resolve_plant_accepted(wcvp_conn, plant_name_scientific_raw_normalize)
            ###
            activity_name_raw_normalize = input_item['activity_name_raw_normalize']
            drduke_cur = drduke_conn.cursor()
            drduke_cur.execute("""
                SELECT *
                FROM drduke_activities_names
                WHERE activity_name_normalize = ?
            """, (activity_name_raw_normalize,))
            drduke_rows = drduke_cur.fetchall()
            drduke_items = [dict(row) for row in drduke_rows]
            ###
            if wcvp_row and drduke_rows:
                wcvp_item = dict(wcvp_row)
                input_item['plant_name_scientific_reference'] = wcvp_item['taxon_name']
                input_item['plant_name_scientific_reference_normalize'] = wcvp_item['taxon_name_normalized']
                ###
                drduke_item = drduke_items[0]
                input_item['activity_name_reference'] = drduke_item['activity_name_raw']
                input_item['activity_name_reference_normalize'] = drduke_item['activity_name_normalize']
                resolved_data.append(input_item)
                # print(json.dumps(input_item, indent=4))
                # quit()
        if resolved_data != []:
            io.json_write(output_filepath, resolved_data)
            last_resolved_data = resolved_data
    drduke_conn.close()
    print(json.dumps(last_resolved_data[0], indent=4))
    # quit()

def resolve__plants__plants_names_common(source_foldername):
    table_name = 'plants__plants_names_common'
    input_folderpath = f'{HUB_FOLDERPATH}/normalize/{source_foldername}/{table_name}/json'
    output_folderpath = f'{HUB_FOLDERPATH}/resolve/{source_foldername}/{table_name}/json'
    try: shutil.rmtree(output_folderpath)
    except: pass
    os.makedirs(output_folderpath, exist_ok=True)
    ###
    wcvp_folderpath = f'{HUB_FOLDERPATH}/reference/wcvp/wcvp.db'
    wcvp_conn = sqlite3.connect(wcvp_folderpath)
    wcvp_conn.row_factory = sqlite3.Row
    ###
    input_filenames = os.listdir(input_folderpath)
    last_resolved_data = []
    failed_resolved = 0
    failed_data = 0
    succeded_data = 0
    for i, input_filename in enumerate(input_filenames[:]):
        print(f'RESOLVE HERBS plants__plants_names_common {i}/{len(input_filenames)}')
        output_filepath = f'{output_folderpath}/{input_filename}'
        input_filepath = f'{input_folderpath}/{input_filename}'
        if os.path.exists(output_filepath): continue
        ###
        input_data = io.json_read(input_filepath)
        resolved_data = []
        for input_item in input_data[:]:
            # print(json.dumps(input_item, indent=True))
            # quit()
            plant_name_scientific_raw_normalize = input_item['plant_name_scientific_raw_normalize']
            wcvp_row = resolve_utils.resolve_plant_accepted(wcvp_conn, plant_name_scientific_raw_normalize)
            ###
            if wcvp_row:
                wcvp_item = dict(wcvp_row)
                input_item['plant_name_scientific_reference'] = wcvp_item['taxon_name']
                input_item['plant_name_scientific_reference_normalize'] = wcvp_item['taxon_name_normalized']
                ###
                input_item['plant_name_common_reference'] = input_item['plant_name_common_raw']
                input_item['plant_name_common_reference_normalize'] = input_item['plant_name_common_raw_normalize']
                resolved_data.append(input_item)
                # print(json.dumps(input_item, indent=4))
                # quit()
            else:
                failed_resolved += 1
        if resolved_data != []:
            io.json_write(output_filepath, resolved_data)
            last_resolved_data = resolved_data
            succeded_data += 1
        else:
            failed_data += 1
    print(json.dumps(last_resolved_data[0], indent=4))
    print(failed_resolved)
    print(failed_data)
    print(succeded_data)
    quit()

def resolve__plants__conditions(source_foldername):
    table_name = 'plants__conditions'
    input_folderpath = f'{HUB_FOLDERPATH}/normalize/{source_foldername}/{table_name}/json'
    output_folderpath = f'{HUB_FOLDERPATH}/resolve/{source_foldername}/{table_name}/json'
    try: shutil.rmtree(output_folderpath)
    except: pass
    os.makedirs(output_folderpath, exist_ok=True)
    ###
    wcvp_folderpath = f'{HUB_FOLDERPATH}/reference/wcvp/wcvp.db'
    wcvp_conn = sqlite3.connect(wcvp_folderpath)
    wcvp_conn.row_factory = sqlite3.Row
    ###
    mesh_folderpath = f'{HUB_FOLDERPATH}/reference/mesh/mesh.db'
    mesh_conn = sqlite3.connect(mesh_folderpath)
    mesh_conn.row_factory = sqlite3.Row
    ###
    input_filenames = os.listdir(input_folderpath)
    last_resolved_data = []
    failed_resolved = 0
    failed_data = 0
    succeded_data = 0
    for i, input_filename in enumerate(input_filenames[:]):
        print(f'RESOLVE HERBS {table_name} {i}/{len(input_filenames)}')
        output_filepath = f'{output_folderpath}/{input_filename}'
        input_filepath = f'{input_folderpath}/{input_filename}'
        if os.path.exists(output_filepath): continue
        ###
        input_data = io.json_read(input_filepath)
        resolved_data = []
        for input_item in input_data[:]:
            # print(json.dumps(input_item, indent=True))
            # quit()
            ### RESOLVE PLANT (WCVP)
            plant_name_scientific_raw_normalize = input_item['plant_name_scientific_raw_normalize']
            wcvp_row = resolve_utils.resolve_plant_accepted(wcvp_conn, plant_name_scientific_raw_normalize)
            ### RESOLVE DISEASE (MESH)
            condition_name_raw_normalize = input_item['condition_name_raw_normalize']
            if condition_name_raw_normalize == 'null': continue
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
                input_item['plant_name_scientific_reference'] = wcvp_item['taxon_name']
                input_item['plant_name_scientific_reference_normalize'] = wcvp_item['taxon_name_normalized']
                input_item['condition_name_reference'] = mesh_item['disease_name']
                input_item['condition_name_reference_normalize'] = mesh_item['disease_name_normalize']
                resolved_data.append(input_item)
                # print(json.dumps(input_item, indent=4))
                # quit()
            else:
                failed_resolved += 1
        if resolved_data != []:
            io.json_write(output_filepath, resolved_data)
            last_resolved_data = resolved_data
            succeded_data += 1
        else:
            failed_data += 1
    wcvp_conn.close()
    mesh_conn.close()
    print(json.dumps(last_resolved_data[0], indent=4))
    print(failed_resolved)
    print(failed_data)
    print(succeded_data)
    quit()

def resolve__plants__compounds(source_foldername):
    table_name = 'plants__compounds'
    input_folderpath = f'{HUB_FOLDERPATH}/normalize/{source_foldername}/{table_name}/json'
    output_folderpath = f'{HUB_FOLDERPATH}/resolve/{source_foldername}/{table_name}/json'
    try: shutil.rmtree(output_folderpath)
    except: pass
    os.makedirs(output_folderpath, exist_ok=True)
    ###
    wcvp_folderpath = f'{HUB_FOLDERPATH}/reference/wcvp/wcvp.db'
    wcvp_conn = sqlite3.connect(wcvp_folderpath)
    wcvp_conn.row_factory = sqlite3.Row
    ###
    pubchem_folderpath = f'{HUB_FOLDERPATH}/reference/pubchem/pubchem.db'
    pubchem_conn = sqlite3.connect(pubchem_folderpath)
    pubchem_conn.row_factory = sqlite3.Row
    ###
    input_filenames = os.listdir(input_folderpath)
    last_resolved_data = []
    failed_resolved = 0
    failed_data = 0
    succeded_data = 0
    for i, input_filename in enumerate(input_filenames[:]):
        print(f'RESOLVE HERBS {table_name} {i}/{len(input_filenames)}')
        output_filepath = f'{output_folderpath}/{input_filename}'
        input_filepath = f'{input_folderpath}/{input_filename}'
        if os.path.exists(output_filepath): continue
        ###
        input_data = io.json_read(input_filepath)
        resolved_data = []
        for input_item in input_data[:]:
            # print(json.dumps(input_item, indent=True))
            # quit()
            ### RESOLVE PLANT (WCVP)
            plant_name_scientific_raw_normalize = input_item['plant_name_scientific_raw_normalize']
            wcvp_row = resolve_utils.resolve_plant_accepted(wcvp_conn, plant_name_scientific_raw_normalize)
            ### RESOLVE CHEMICAL (PUBCHEM)
            compound_name_raw_normalize = input_item['compound_name_raw_normalize']
            if compound_name_raw_normalize == 'null': continue
            pubchem_cur = pubchem_conn.cursor()
            pubchem_cur.execute("""
                SELECT *
                FROM pubchem_cid_synonyms
                WHERE alias_normalize = ?
            """, (compound_name_raw_normalize,))
            # pubchem_row = pubchem_cur.fetchone()
            pubchem_rows = pubchem_cur.fetchall()
            pubchem_items = [dict(row) for row in pubchem_rows]
            ###
            if wcvp_row and pubchem_items:
                wcvp_item = dict(wcvp_row)
                pubchem_item = pubchem_items[0]
                input_item['plant_name_scientific_reference'] = wcvp_item['taxon_name']
                input_item['plant_name_scientific_reference_normalize'] = wcvp_item['taxon_name_normalized']
                input_item['compound_name_reference'] = pubchem_item['alias']
                input_item['compound_name_reference_normalize'] = pubchem_item['alias_normalize']
                resolved_data.append(input_item)
                # print(json.dumps(input_item, indent=4))
                # quit()
            else:
                failed_resolved += 1
        if resolved_data != []:
            io.json_write(output_filepath, resolved_data)
            last_resolved_data = resolved_data
            succeded_data += 1
        else:
            failed_data += 1
    wcvp_conn.close()
    pubchem_conn.close()
    print(json.dumps(last_resolved_data[0], indent=4))
    print(failed_resolved)
    print(failed_data)
    print(succeded_data)

def resolve__plants__preparations(source_foldername):
    table_name = 'plants__preparations'
    input_folderpath = f'{HUB_FOLDERPATH}/normalize/{source_foldername}/{table_name}/json'
    output_folderpath = f'{HUB_FOLDERPATH}/resolve/{source_foldername}/{table_name}/json'
    try: shutil.rmtree(output_folderpath)
    except: pass
    os.makedirs(output_folderpath, exist_ok=True)
    ###
    wcvp_folderpath = f'{HUB_FOLDERPATH}/reference/wcvp/wcvp.db'
    wcvp_conn = sqlite3.connect(wcvp_folderpath)
    wcvp_conn.row_factory = sqlite3.Row
    ###
    ref_folderpath = f'{HUB_FOLDERPATH}/reference/manual/manual.db'
    ref_conn = sqlite3.connect(ref_folderpath)
    ref_conn.row_factory = sqlite3.Row
    ###
    input_filenames = os.listdir(input_folderpath)
    last_resolved_data = []
    failed_resolved = 0
    failed_data = 0
    succeded_data = 0
    for i, input_filename in enumerate(input_filenames[:]):
        print(f'RESOLVE HERBS {table_name} {i}/{len(input_filenames)}')
        output_filepath = f'{output_folderpath}/{input_filename}'
        input_filepath = f'{input_folderpath}/{input_filename}'
        if os.path.exists(output_filepath): continue
        ###
        input_data = io.json_read(input_filepath)
        resolved_data = []
        for input_item in input_data[:]:
            # print(json.dumps(input_item, indent=True))
            # quit()
            ### RESOLVE PLANT (WCVP)
            plant_name_scientific_raw_normalize = input_item['plant_name_scientific_raw_normalize']
            wcvp_row = resolve_utils.resolve_plant_accepted(wcvp_conn, plant_name_scientific_raw_normalize)
            ### RESOLVE PREPARATIONS (MANUAL)
            preparation_name_raw_normalize = input_item['preparation_name_raw_normalize']
            ref_cur = ref_conn.cursor()
            ref_cur.execute("""
                SELECT *
                FROM ref__preparations
                WHERE ref_preparation_name_normalize = ?
            """, (preparation_name_raw_normalize,))
            ref_rows = ref_cur.fetchall()
            ref_items = [dict(row) for row in ref_rows]
            if wcvp_row and ref_items:
                wcvp_item = dict(wcvp_row)
                ref_item = ref_items[0]
                input_item['plant_name_scientific_reference'] = wcvp_item['taxon_name']
                input_item['plant_name_scientific_reference_normalize'] = wcvp_item['taxon_name_normalized']
                input_item['preparation_name_reference'] = ref_item['ref_preparation_name']
                input_item['preparation_name_reference_normalize'] = ref_item['ref_preparation_name_normalize']
                resolved_data.append(input_item)
                # print(json.dumps(input_item, indent=4))
                # quit()
            else:
                failed_resolved += 1
        if resolved_data != []:
            io.json_write(output_filepath, resolved_data)
            last_resolved_data = resolved_data
            succeded_data += 1
        else:
            failed_data += 1
    wcvp_conn.close()
    # pubchem_conn.close()
    print(json.dumps(last_resolved_data[0], indent=4))
    print(failed_resolved)
    print(failed_data)
    print(succeded_data)

def resolve__plants__parts(source_foldername):
    table_name = 'plants__parts'
    input_folderpath = f'{HUB_FOLDERPATH}/normalize/{source_foldername}/{table_name}/json'
    output_folderpath = f'{HUB_FOLDERPATH}/resolve/{source_foldername}/{table_name}/json'
    try: shutil.rmtree(output_folderpath)
    except: pass
    os.makedirs(output_folderpath, exist_ok=True)
    ###
    wcvp_folderpath = f'{HUB_FOLDERPATH}/reference/wcvp/wcvp.db'
    wcvp_conn = sqlite3.connect(wcvp_folderpath)
    wcvp_conn.row_factory = sqlite3.Row
    ###
    ref_folderpath = f'{HUB_FOLDERPATH}/reference/manual/manual.db'
    ref_conn = sqlite3.connect(ref_folderpath)
    ref_conn.row_factory = sqlite3.Row
    ###
    input_filenames = os.listdir(input_folderpath)
    last_resolved_data = []
    failed_resolved = 0
    failed_data = 0
    succeded_data = 0
    for i, input_filename in enumerate(input_filenames[:]):
        print(f'RESOLVE HERBS {table_name} {i}/{len(input_filenames)}')
        output_filepath = f'{output_folderpath}/{input_filename}'
        input_filepath = f'{input_folderpath}/{input_filename}'
        if os.path.exists(output_filepath): continue
        ###
        input_data = io.json_read(input_filepath)
        resolved_data = []
        for input_item in input_data[:]:
            # print(json.dumps(input_item, indent=True))
            # quit()
            ### RESOLVE PLANT (WCVP)
            plant_name_scientific_raw_normalize = input_item['plant_name_scientific_raw_normalize']
            wcvp_row = resolve_utils.resolve_plant_accepted(wcvp_conn, plant_name_scientific_raw_normalize)
            ### RESOLVE PARTS (MANUAL)
            part_name_raw_normalize = input_item['part_name_raw_normalize']
            ref_cur = ref_conn.cursor()
            ref_cur.execute("""
                SELECT *
                FROM ref__parts
                WHERE ref_part_name_normalize = ?
            """, (part_name_raw_normalize,))
            ref_rows = ref_cur.fetchall()
            ref_items = [dict(row) for row in ref_rows]
            ###
            if wcvp_row and ref_items:
                wcvp_item = dict(wcvp_row)
                ref_item = ref_items[0]
                input_item['plant_name_scientific_reference'] = wcvp_item['taxon_name']
                input_item['plant_name_scientific_reference_normalize'] = wcvp_item['taxon_name_normalized']
                # input_item['compound_name_reference'] = pubchem_item['alias']
                # input_item['compound_name_reference_normalize'] = pubchem_item['alias_normalize']
                input_item['part_name_reference'] = ref_item['ref_part_name']
                input_item['part_name_reference_normalize'] = ref_item['ref_part_name_normalize']
                resolved_data.append(input_item)
                # print(json.dumps(input_item, indent=4))
                # quit()
            else:
                failed_resolved += 1
        if resolved_data != []:
            io.json_write(output_filepath, resolved_data)
            last_resolved_data = resolved_data
            succeded_data += 1
        else:
            failed_data += 1
    wcvp_conn.close()
    # pubchem_conn.close()
    print(json.dumps(last_resolved_data[0], indent=4))
    print(failed_resolved)
    print(failed_data)
    print(succeded_data)

def cluster__plants__parts(source_foldername):
    table_name = 'plants__parts'
    input_folderpath = f'{HUB_FOLDERPATH}/normalize/{source_foldername}/{table_name}/json'
    ###
    parts = []
    ###
    input_filenames = os.listdir(input_folderpath)
    for i, input_filename in enumerate(input_filenames[:]):
        print(f'RESOLVE HERBS CLUSTER {table_name} {i}/{len(input_filenames)}')
        input_filepath = f'{input_folderpath}/{input_filename}'
        ###
        input_data = io.json_read(input_filepath)
        for item in input_data:
            part_name_raw_normalize = item['part_name_raw_normalize']
            part_name_resolved_local = part_name_raw_normalize 
            """
            {
              "id": "plant_part_root",
              "preferred_label": "Root",
              "alternative_labels": [
                "Radix",
                "Roots"
              ],
              "category": "Plant part"
            }
            """
            ### MERGE
            if part_name_resolved_local.strip().lower() == 'leaves': part_name_resolved_local = 'leaf'
            if part_name_resolved_local.strip().lower() == 'roots': part_name_resolved_local = 'root'
            if part_name_resolved_local.strip().lower() == 'hairy roots': part_name_resolved_local = 'root'
            if part_name_resolved_local.strip().lower() == 'dried roots': part_name_resolved_local = 'root'
            if part_name_resolved_local.strip().lower() == 'radix': part_name_resolved_local = 'root'
            if part_name_resolved_local.strip().lower() == 'seeds': part_name_resolved_local = 'seed'
            if part_name_resolved_local.strip().lower() == 'aerial part': part_name_resolved_local = 'aerial parts'
            if part_name_resolved_local.strip().lower() == 'whole plants': part_name_resolved_local = 'whole plant'
            if part_name_resolved_local.strip().lower() == 'fruits': part_name_resolved_local = 'fruit'
            if part_name_resolved_local.strip().lower() == 'stems': part_name_resolved_local = 'stem'
            if part_name_resolved_local.strip().lower() == 'flowers': part_name_resolved_local = 'flower'
            if part_name_resolved_local.strip().lower() == 'barks': part_name_resolved_local = 'bark'
            if part_name_resolved_local.strip().lower() == 'cortex': part_name_resolved_local = 'bark'
            if part_name_resolved_local.strip().lower() == 'stem bark': part_name_resolved_local = 'bark'
            if part_name_resolved_local.strip().lower() == 'root bark': part_name_resolved_local = 'bark'
            if part_name_resolved_local.strip().lower() == 'rhizomes': part_name_resolved_local = 'rhizome'
            if part_name_resolved_local.strip().lower() == 'rhizoma': part_name_resolved_local = 'rhizome'
            if part_name_resolved_local.strip().lower() == 'bulbs': part_name_resolved_local = 'bulb'
            if part_name_resolved_local.strip().lower() == 'twigs': part_name_resolved_local = 'twig'
            if part_name_resolved_local.strip().lower() == 'tubers': part_name_resolved_local = 'tuber'
            if 'leaf' in part_name_resolved_local.strip().lower(): part_name_resolved_local = 'leaf'
            ### EXCLUDE
            if part_name_resolved_local.strip().lower() == 'essential oils': continue
            if part_name_resolved_local.strip().lower() == 'essential oil': continue
            if part_name_resolved_local.strip().lower() == 'herb': continue
            if part_name_resolved_local.strip().lower() == 'oil': continue
            if part_name_resolved_local.strip().lower() == 'extract': continue
            if part_name_resolved_local.strip().lower() == 'extracts': continue
            parts.append(part_name_resolved_local)
        # print(json.dumps(input_data, indent=4))
        # print(json.dumps(parts, indent=4))
        # quit()
    # print(parts[:20])
    from collections import Counter
    counts = Counter(parts)
    # print(counts[:100])
    print(json.dumps(counts.most_common(20), indent=4))

def cluster__plants__preparations(source_foldername):
    table_name = 'plants__preparations'
    input_folderpath = f'{HUB_FOLDERPATH}/normalize/{source_foldername}/{table_name}/json'
    ###
    preparations = []
    ###
    input_filenames = os.listdir(input_folderpath)
    for i, input_filename in enumerate(input_filenames[:]):
        print(f'RESOLVE HERBS CLUSTER {table_name} {i}/{len(input_filenames)}')
        input_filepath = f'{input_folderpath}/{input_filename}'
        ###
        input_data = io.json_read(input_filepath)
        for item in input_data:
            # print(json.dumps(item, indent=4))
            preparation_name_raw_normalize = item['preparation_name_raw_normalize']
            preparation_name_resolved_local = preparation_name_raw_normalize 
            ### MERGE
            if 'extract' in preparation_name_resolved_local.strip().lower(): preparation_name_resolved_local = 'extract'
            if 'infusions' in preparation_name_resolved_local.strip().lower(): preparation_name_resolved_local = 'infusion'
            if 'oils' in preparation_name_resolved_local.strip().lower(): preparation_name_resolved_local = 'oil'
            if 'juices' in preparation_name_resolved_local.strip().lower(): preparation_name_resolved_local = 'juice'
            if 'capsules' in preparation_name_resolved_local.strip().lower(): preparation_name_resolved_local = 'capsule'
            # if preparation_name_resolved_local.strip().lower() == 'extracts': preparation_name_resolved_local = 'extract'
            if preparation_name_resolved_local.strip().lower() == 'decoctions': preparation_name_resolved_local = 'decoction'
            ### EXCLUDE
            if preparation_name_resolved_local.strip().lower() == 'leaves': continue
            if preparation_name_resolved_local.strip().lower() == 'roots': continue
            if preparation_name_resolved_local.strip().lower() == 'seeds': continue
            if preparation_name_resolved_local.strip().lower() == 'bark': continue
            if preparation_name_resolved_local.strip().lower() == 'fractions': continue
            if preparation_name_resolved_local.strip().lower() == 'fraction': continue
            if preparation_name_resolved_local.strip().lower() == 'stem bark': continue
            if preparation_name_resolved_local.strip().lower() == 'rhizomes': continue
            if preparation_name_resolved_local.strip().lower() == 'fruits': continue
            if preparation_name_resolved_local.strip().lower() == 'fruit': continue
            if preparation_name_resolved_local.strip().lower() == 'whole plant': continue
            if preparation_name_resolved_local.strip().lower() == 'eos': continue
            if preparation_name_resolved_local.strip().lower() == 'root': continue
            if preparation_name_resolved_local.strip().lower() == 'eo': continue
            if preparation_name_resolved_local.strip().lower() == 'ethyl acetate': continue
            if preparation_name_resolved_local.strip().lower() == 'drugs': continue
            if preparation_name_resolved_local.strip().lower() == 'preparations': continue
            if preparation_name_resolved_local.strip().lower() == 'volatile oil': continue
            if preparation_name_resolved_local.strip().lower() == 'callus': continue
            if preparation_name_resolved_local.strip().lower() == 'hairy roots': continue
            if 'fraction' in preparation_name_resolved_local.strip().lower(): continue
            # if 'fruit' in preparation_name_resolved_local.strip().lower(): continue
            preparations.append(preparation_name_resolved_local)
        # print(json.dumps(input_data, indent=4))
        # print(json.dumps(preparations, indent=4))
        # quit()
    # print(preparations[:20])
    from collections import Counter
    counts = Counter(preparations)
    # print(counts[:100])
    print(json.dumps(counts.most_common(20), indent=4))

def resolve__phrases__plants__activities(source_foldername):
    input_folderpath = f'{HUB_FOLDERPATH}/normalize/{source_foldername}/phrases__plants__activities/json'
    output_folderpath = f'{HUB_FOLDERPATH}/resolve/{source_foldername}/phrases__plants__activities/json'
    try: shutil.rmtree(output_folderpath)
    except: pass
    os.makedirs(output_folderpath, exist_ok=True)
    ###
    wcvp_folderpath = f'{HUB_FOLDERPATH}/reference/wcvp/wcvp.db'
    wcvp_conn = sqlite3.connect(wcvp_folderpath)
    wcvp_conn.row_factory = sqlite3.Row
    ###
    drduke_folderpath = f'{HUB_FOLDERPATH}/reference/drduke/drduke.db'
    drduke_conn = sqlite3.connect(drduke_folderpath)
    drduke_conn.row_factory = sqlite3.Row
    ###
    input_filenames = os.listdir(input_folderpath)
    last_resolved_data = []
    for i, input_filename in enumerate(input_filenames[:]):
        print(f'RESOLVE HERBS plants_activities {i}/{len(input_filenames)}')
        output_filepath = f'{output_folderpath}/{input_filename}'
        input_filepath = f'{input_folderpath}/{input_filename}'
        if os.path.exists(output_filepath): continue
        ###
        input_data = io.json_read(input_filepath)
        resolved_data = []
        # print(json.dumps(input_data, indent=4))
        # quit()
        for extraction in input_data['extractions']:
            for triple_item in extraction['triples_resolve_local_subject_string_match']:
                input_item = triple_item
                # print(json.dumps(input_item, indent=4))
                # quit()
                ###
                plant_name_scientific_raw_normalize = input_item['plant_name_scientific_raw_normalize']
                wcvp_row = resolve_utils.resolve_plant_accepted(wcvp_conn, plant_name_scientific_raw_normalize)
                ###
                activity_name_raw_normalize = input_item['activity_name_raw_normalize']
                drduke_cur = drduke_conn.cursor()
                drduke_cur.execute("""
                    SELECT *
                    FROM drduke_activities_names
                    WHERE activity_name_normalize = ?
                """, (activity_name_raw_normalize,))
                drduke_rows = drduke_cur.fetchall()
                drduke_items = [dict(row) for row in drduke_rows]
                ###
                if wcvp_row and drduke_rows:
                    wcvp_item = dict(wcvp_row)
                    input_item['plant_name_scientific_reference'] = wcvp_item['taxon_name']
                    input_item['plant_name_scientific_reference_normalize'] = wcvp_item['taxon_name_normalized']
                    ###
                    drduke_item = drduke_items[0]
                    input_item['activity_name_reference'] = drduke_item['activity_name_raw']
                    input_item['activity_name_reference_normalize'] = drduke_item['activity_name_normalize']
                    resolved_data.append(input_item)
                    # print(json.dumps(input_item, indent=4))
                    # quit()
        if resolved_data != []:
            io.json_write(output_filepath, resolved_data)
            last_resolved_data = resolved_data
    wcvp_conn.close()
    drduke_conn.close()
    print(json.dumps(last_resolved_data[0], indent=4))
    # quit()

def run():
    print('RESOLVE')

    # cluster__plants__parts(source_foldername='pubmed')
    # cluster__plants__preparations(source_foldername='pubmed')

    ### MASTER
    # resolve__plants_names_common(source_foldername='col')

    # studies_resolve(source_foldername='pubmed')
    # plants_resolve(source_foldername='pubmed')
    # activities_resolve(source_foldername='pubmed')
    # conditions_resolve(source_foldername='pubmed')
    # compounds_resolve(source_foldername='pubmed')
    # preparations_resolve(source_foldername='pubmed')
    # parts_resolve(source_foldername='pubmed')


    ### ASSERTIONS
    # resolve__plants__plants_names_common(source_foldername='col')

    # resolve__plants__activities(source_foldername='pubmed')
    # resolve__plants__conditions(source_foldername='pubmed')
    # resolve__plants__compounds(source_foldername='pubmed')
    resolve__plants__preparations(source_foldername='pubmed')
    # resolve__plants__parts(source_foldername='pubmed')

    # resolve__phrases__plants__activities(source_foldername='pubmed')

    return
    quit()

    if 0:
        resolve_activities('pubmed')
        resolve_plants_parts('pubmed')
        resolve_compounds('pubmed')

    schema_items = schema_herbs.data['items']
    for schema_item in schema_items: 
        if schema_item['process'] != True: continue
        if schema_item['table_name'] == 'plants_activities': continue
        if schema_item['table_name'] == 'plants_plants_parts': continue
        if schema_item['table_name'] == 'plants_compounds': continue
        schema_resolve_gen(schema_item)

    if 0:
        # resolve_gen('plant_name_scientific', 'compound_name', 'pubmed', 'compounds')
        # resolve_gen('plant_name_scientific', 'preparation_name', 'pubmed', 'preparations')
        resolve_gen('plant_name_scientific', 'condition_name', 'pubmed', 'conditions')
        resolve_gen('plant_name_scientific', 'activity_name', 'pubmed', 'activities')

        # resolve_chemicals(source_foldername='drduke')
        resolve_chemicals(source_foldername='pubmed')
        resolve_taxonomies(source_foldername='powo')
        resolve_synonyms(source_foldername='wcvp')
        resolve_traits(source_foldername='gift')
        resolve_distributions(source_foldername='wcvp')

        # resolve_common_names(source_foldername='wikidata')
        resolve_common_names(source_foldername='col')

