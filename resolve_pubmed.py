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
                wcvp_ipni_id = wcvp_row[0]
                wcvp_powo_id = wcvp_row[1]
                wcvp_taxon_name = wcvp_row[2]
                wcvp_taxon_name_normalized = wcvp_row[3]
                wcvp_taxon_rank = wcvp_row[4]
                wcvp_taxon_status = wcvp_row[5]
                wcvp_family = wcvp_row[6]
                wcvp_geographic_area = wcvp_row[7]
                wcvp_climate_description = wcvp_row[8]
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
    input_folderpath = f'{g.VAULT_FOLDERPATH}/terrawhisper/data/{input_foldername}/{source_name}/{entity_type}/json'
    output_folderpath = f'{g.VAULT_FOLDERPATH}/terrawhisper/data/{output_foldername}/{source_name}/{entity_type}/json'
    io.folders_recursive_gen(output_folderpath)
    input_filenames = os.listdir(input_folderpath)
    try: shutil.rmtree(output_folderpath)
    except: pass
    os.makedirs(output_folderpath, exist_ok=True)
    ###
    wcvp_folderpath = f'{g.VAULT_FOLDERPATH}/terrawhisper/data/reference/wcvp/wcvp.db'
    wcvp_conn = sqlite3.connect(wcvp_folderpath)
    drduke_folderpath = f'{g.VAULT_FOLDERPATH}/terrawhisper/data/reference/drduke/drduke.db'
    drduke_conn = sqlite3.connect(drduke_folderpath)
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
            activity_name_normalized = input_item['activity_name_normalized']
            if activity_name_normalized == 'null': continue
            ### RESOLVE PLANT (WCVP)
            wcvp_cur = wcvp_conn.cursor()
            wcvp_cur.execute("""
                SELECT *
                FROM wcvp
                WHERE taxon_name_normalized = ?
            """, (plant_name_normalized,))
            wcvp_row = wcvp_cur.fetchone()
            ### RESOLVE ACTIVITY (DRDIKE)
            drduke_cur = drduke_conn.cursor()
            drduke_cur.execute("""
                SELECT *
                FROM activities
                WHERE activity_name_normalized = ?
            """, (activity_name_normalized,))
            drduke_row = drduke_cur.fetchone()
            if wcvp_row and drduke_row:
                wcvp_ipni_id = wcvp_row[0]
                wcvp_powo_id = wcvp_row[1]
                wcvp_taxon_name = wcvp_row[2]
                wcvp_taxon_name_normalized = wcvp_row[3]
                wcvp_taxon_rank = wcvp_row[4]
                wcvp_taxon_status = wcvp_row[5]
                wcvp_family = wcvp_row[6]
                wcvp_geographic_area = wcvp_row[7]
                wcvp_climate_description = wcvp_row[8]
                drduke_activity_name = drduke_row[0]
                drduke_activity_name_normalized = drduke_row[1]
                resolved_item_new = resolved_item
                resolved_item_new['wcvp_taxon_name'] = wcvp_taxon_name
                resolved_item_new['wcvp_taxon_name_normalized'] = wcvp_taxon_name_normalized
                resolved_item_new['drduke_activity_name'] = drduke_activity_name
                resolved_item_new['drduke_activity_name_normalized'] = drduke_activity_name_normalized
                resolved_data.append(resolved_item_new)
        if resolved_data != []:
            io.json_write(output_filepath, resolved_data)
    wcvp_conn.close()
    drduke_conn.close()

def resolve_diseases():
    source_name = 'pubmed'
    entity_type = 'diseases'
    input_foldername = f'normalize'
    output_foldername = f'resolve'
    ###
    input_folderpath = f'{g.VAULT_FOLDERPATH}/terrawhisper/data/{input_foldername}/{source_name}/{entity_type}/json'
    output_folderpath = f'{g.VAULT_FOLDERPATH}/terrawhisper/data/{output_foldername}/{source_name}/{entity_type}/json'
    io.folders_recursive_gen(output_folderpath)
    input_filenames = os.listdir(input_folderpath)
    try: shutil.rmtree(output_folderpath)
    except: pass
    os.makedirs(output_folderpath, exist_ok=True)
    ###
    wcvp_folderpath = f'{g.VAULT_FOLDERPATH}/terrawhisper/data/reference/wcvp/wcvp.db'
    wcvp_conn = sqlite3.connect(wcvp_folderpath)
    mesh_folderpath = f'{g.VAULT_FOLDERPATH}/terrawhisper/data/reference/mesh/mesh.db'
    mesh_conn = sqlite3.connect(mesh_folderpath)
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
            disease_name_normalized = input_item['disease_name_normalized']
            if disease_name_normalized == 'null': continue
            ### RESOLVE PLANT (WCVP)
            wcvp_cur = wcvp_conn.cursor()
            wcvp_cur.execute("""
                SELECT *
                FROM wcvp
                WHERE taxon_name_normalized = ?
            """, (plant_name_normalized,))
            wcvp_row = wcvp_cur.fetchone()
            ### RESOLVE DISEASE (MESH)
            mesh_cur = mesh_conn.cursor()
            mesh_cur.execute("""
                SELECT *
                FROM diseases
                WHERE disease_name_normalized = ?
            """, (disease_name_normalized,))
            mesh_row = mesh_cur.fetchone()
            if wcvp_row and mesh_row:
                wcvp_ipni_id = wcvp_row[0]
                wcvp_powo_id = wcvp_row[1]
                wcvp_taxon_name = wcvp_row[2]
                wcvp_taxon_name_normalized = wcvp_row[3]
                wcvp_taxon_rank = wcvp_row[4]
                wcvp_taxon_status = wcvp_row[5]
                wcvp_family = wcvp_row[6]
                wcvp_geographic_area = wcvp_row[7]
                wcvp_climate_description = wcvp_row[8]
                mesh_activity_name = mesh_row[0]
                mesh_activity_name_normalized = mesh_row[1]
                resolved_item_new = resolved_item
                resolved_item_new['wcvp_taxon_name'] = wcvp_taxon_name
                resolved_item_new['wcvp_taxon_name_normalized'] = wcvp_taxon_name_normalized
                resolved_item_new['mesh_activity_name'] = mesh_activity_name
                resolved_item_new['mesh_activity_name_normalized'] = mesh_activity_name_normalized
                resolved_data.append(resolved_item_new)
        if resolved_data != []:
            io.json_write(output_filepath, resolved_data)
    wcvp_conn.close()
    mesh_conn.close()

def run():
    print('RESOLVE >> pubmed')

    # start = time.perf_counter()
    resolve_chemicals()
    # print(f'resolve chemicals() - execution time: ', time.perf_counter() - start)

    # start = time.perf_counter()
    resolve_activities()
    # print(f'resolve activities() - execution time: ', time.perf_counter() - start)

    start = time.perf_counter()
    resolve_diseases()
    print(f'resolve diseases() - execution time: ', time.perf_counter() - start)

