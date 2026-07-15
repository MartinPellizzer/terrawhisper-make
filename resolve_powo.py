import os
import time
import json
import shutil
import sqlite3

from lib import g
from lib import io
from lib import llm

def resolve_plants():
    source_name = 'powo'
    input_foldername = f'normalize'
    output_foldername = f'resolve'
    ###
    input_folderpath = f'{g.DATA_FOLDERPATH}/{input_foldername}/{source_name}/json'
    output_folderpath = f'{g.DATA_FOLDERPATH}/{output_foldername}/{source_name}/json'
    # try: shutil.rmtree(output_folderpath)
    # except: pass
    io.folders_recursive_gen(output_folderpath)
    ###
    input_filenames = os.listdir(input_folderpath)
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
        ###
        resolved_data = []
        plant_name_normalized = input_data['taxon_name_normalized']
        ### RESOLVE PLANT (WCVP)
        wcvp_cur = wcvp_conn.cursor()
        wcvp_cur.execute("""
            SELECT *
            FROM wcvp
            WHERE taxon_name_normalized = ?
        """, (plant_name_normalized,))
        wcvp_row = wcvp_cur.fetchone()
        ###
        if wcvp_row:
            resolved_data = {}
            resolved_data['wcvp_taxon_name'] = input_data['taxon_name']
            resolved_data['wcvp_taxon_name_normalized'] = input_data['taxon_name_normalized']
            resolved_data['wcvp_kingdom'] = input_data['kingdom']
            resolved_data['wcvp_phylum'] = input_data['phylum']
            resolved_data['wcvp_class'] = input_data['class']
            resolved_data['wcvp_subclass'] = input_data['subclass']
            resolved_data['wcvp_order'] = input_data['order']
            resolved_data['wcvp_family'] = input_data['family']
            resolved_data['wcvp_genus'] = input_data['genus']
            ###
            io.json_write(output_filepath, resolved_data)
            # print(json.dumps(resolved_data, indent=4))
            # quit()
    wcvp_conn.close()

def run():
    print('RESOLVE >> powo')

    start = time.perf_counter()
    resolve_plants()
    print(f'resolve plants() - execution time: ', time.perf_counter() - start)

