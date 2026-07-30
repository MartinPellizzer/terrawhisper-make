import os
import csv
import json
import time
import shutil
import sqlite3

from lib import g
from lib import io

import masterize_utils
import parse_utils

def parse_names():
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
            output_item = parse_utils.common_name_create(
                plant_name_scientific_raw = scientific_name,
                plant_name_scientific_norm = scientific_name_norm,
                plant_name_common_raw = row[1],
                plant_name_common_transliteration = row[2],
                plant_name_common_language = row[3],
                plant_name_common_preferred = row[4],
                plant_name_common_country = row[5],
                plant_name_common_area = row[6],
                plant_name_common_type = 'vernacular',
                source_name = 'Catalogue of Life',
                source_acronym = 'COL',
            )
            output_items.append(output_item)

        output_filepath = f'{output_folderpath}/{scientific_name}.json'
        io.json_write(output_filepath, output_items)

    conn.close()
       

def run():
    print(f'''HERBS >> PARSE >> col''')

    start = time.perf_counter()
    parse_names()
    print(f'parse names() - execution time: ', time.perf_counter() - start)

