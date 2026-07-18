import os
import time
import json
import shutil
import sqlite3

from lib import g
from lib import io
from lib import llm

import resolve_utils

def resolve_plants():
    source_name = 'powo'
    input_foldername = f'normalize'
    output_foldername = f'resolve'
    ###
    input_folderpath = f'{g.DATA_FOLDERPATH}/{input_foldername}/{source_name}/json'
    output_folderpath = f'{g.DATA_FOLDERPATH}/{output_foldername}/{source_name}/json'
    try: shutil.rmtree(output_folderpath)
    except: pass
    io.folders_recursive_gen(output_folderpath)
    ###
    input_filenames = os.listdir(input_folderpath)
    print(input_filenames[0])
    # quit()
    wcvp_folderpath = f'{g.VAULT_FOLDERPATH}/terrawhisper/data/reference/wcvp/wcvp.db'
    wcvp_conn = sqlite3.connect(wcvp_folderpath)
    i = 0
    for input_filename in input_filenames[i:]:
        print(input_filename)
        i += 1
        print(f'{i}/{len(input_filenames)}')
        output_filepath = f'{output_folderpath}/{input_filename}'
        input_filepath = f'{input_folderpath}/{input_filename}'
        # if os.path.exists(output_filepath): continue
        input_data = io.json_read(input_filepath)
        if input_data['taxon_name'] == 'Tabernaemontana markgrafiana':
            print(json.dumps(input_data, indent=4))
            # quit()
        ###
        resolved_data = []
        plant_name_normalized = input_data['taxon_name_normalized']
        ### RESOLVE PLANT (WCVP)
        wcvp_row = resolve_utils.resolve_plant(wcvp_conn, plant_name_normalized)
        ###
        if wcvp_row:
            wcvp_plant_name_id = wcvp_row[0]
            wcvp_accepted_plant_name_id = wcvp_row[1]
            wcvp_taxon_status = wcvp_row[2]
            wcvp_taxon_name = wcvp_row[3]
            wcvp_taxon_name_normalized = wcvp_row[4]
            ###
            resolved_data = {}
            resolved_data['wcvp_taxon_name'] = wcvp_taxon_name
            resolved_data['wcvp_taxon_name_normalized'] = wcvp_taxon_name_normalized
            resolved_data['wcvp_kingdom'] = input_data['kingdom']
            resolved_data['wcvp_phylum'] = input_data['phylum']
            resolved_data['wcvp_class'] = input_data['class']
            resolved_data['wcvp_subclass'] = input_data['subclass']
            resolved_data['wcvp_order'] = input_data['order']
            resolved_data['wcvp_family'] = input_data['family']
            resolved_data['wcvp_genus'] = input_data['genus']
            ###
            io.json_write(output_filepath, resolved_data)
            if resolved_data['wcvp_taxon_name'] == 'Tabernaemontana markgrafiana':
                print(json.dumps(resolved_data, indent=4))
                # quit()
            # print(json.dumps(resolved_data, indent=4))
            # quit()
    wcvp_conn.close()

def run():
    print('RESOLVE >> powo')

    start = time.perf_counter()
    resolve_plants()
    print(f'resolve plants() - execution time: ', time.perf_counter() - start)

