import os
import csv
import json
import time
import shutil
import sqlite3

from lib import g
from lib import io

import masterize_utils

def parse_name():
    output_folderpath = f'{g.DATA_FOLDERPATH}/parse/col/names/json'
    try: shutil.rmtree(output_folderpath)
    except: pass
    io.folders_recursive_gen(output_folderpath)
    ###
    master_plants_rows = masterize_utils.masterize_plants_get_all()
    conn = sqlite3.connect(f"{g.DATA_FOLDERPATH}/reference/col/col.db")
    cursor = conn.cursor()
    for i, master_plant_row in enumerate(master_plants_rows[:]):
        print(f'{i}/{len(master_plants_rows)}')
        scientific_name = master_plant_row[1]
        scientific_name_norm = master_plant_row[2]

        cursor.execute("""
            SELECT v.*
            FROM name_usage n
            JOIN vernacular_name v
                ON v.col_id = n.col_id
            WHERE n.scientific_name_norm = ?
        """, (scientific_name_norm,))
        rows = cursor.fetchall()

        output_items = []
        for row in rows:
            output_item = {
                'scientific_name': scientific_name,
                'scientific_name_norm': scientific_name_norm,
                'common_name': row[1],
                'common_name_transliteration': row[2],
                'common_name_language': row[3],
                'common_name_preferred': row[4],
                'common_name_country': row[5],
                'common_name_area': row[6],
                'source_name': 'Catalogue of Life',
                'source_acronym': 'COL',
            }
            output_items.append(output_item)

        output_filepath = f'{output_folderpath}/{scientific_name}.json'
        io.json_write(output_filepath, output_items)

    conn.close()
       

def run():
    print(f'''HERBS >> PARSE >> col''')

    start = time.perf_counter()
    parse_name()
    print(f'wcvp to_jsons() - execution time: ', time.perf_counter() - start)

