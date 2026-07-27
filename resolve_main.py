import os
import time
import json
import shutil
import sqlite3

from lib import g
from lib import io
from lib import llm

import resolve_utils

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
    print(input_filenames)
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
            plant_name_normalized = input_item['plant_name_normalized']
            chemical_name_normalized = input_item['chemical_name_normalized']
            if chemical_name_normalized == 'null': continue
            ### RESOLVE PLANT (WCVP)
            wcvp_row = resolve_utils.resolve_plant_accepted(wcvp_conn, plant_name_normalized)
            ### RESOLVE CHEMICAL (PUBCHEM)
            pubchem_cur = pubchem_conn.cursor()
            pubchem_cur.execute("""
                SELECT *
                FROM pubchem_cid_synonyms
                WHERE normalized_alias = ?
            """, (chemical_name_normalized,))
            pubchem_row = pubchem_cur.fetchone()
            ###
            if wcvp_row and pubchem_row:
                wcvp_plant_name_id = wcvp_row[0]
                wcvp_accepted_plant_name_id = wcvp_row[1]
                wcvp_taxon_status = wcvp_row[2]
                wcvp_taxon_name = wcvp_row[3]
                wcvp_taxon_name_normalized = wcvp_row[4]
                ###
                pubchem_cid = pubchem_row[0]
                pubchem_chemical_name = pubchem_row[1]
                pubchem_chemical_name_normalized = pubchem_row[2]
                ###
                resolved_item_new = resolved_item
                resolved_item_new['wcvp_taxon_name'] = wcvp_taxon_name
                resolved_item_new['wcvp_taxon_name_normalized'] = wcvp_taxon_name_normalized
                resolved_item_new['pubchem_cid'] = pubchem_cid
                resolved_item_new['pubchem_chemical_name'] = pubchem_chemical_name
                resolved_item_new['pubchem_chemical_name_normalized'] = pubchem_chemical_name_normalized
                resolved_data.append(resolved_item_new)
                # print(json.dumps(resolved_item_new, indent=True))
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

def run():
    print('RESOLVE')

    if 0:
        start = time.perf_counter()
        resolve_chemicals(source_foldername='drduke')
        resolve_chemicals(source_foldername='pubmed')
        print(f'resolve chemicals() - execution time: ', time.perf_counter() - start)

    start = time.perf_counter()
    resolve_synonyms(source_foldername='wcvp')
    print(f'resolve synonyms() - execution time: ', time.perf_counter() - start)

