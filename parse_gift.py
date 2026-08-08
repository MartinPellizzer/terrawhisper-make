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

def parse_traits():
    output_folderpath = f'{g.DATA_FOLDERPATH}/parse/gift/traits/json'
    try: shutil.rmtree(output_folderpath)
    except: pass
    io.folders_recursive_gen(output_folderpath)
    ###
    master_plants_rows = masterize_utils.masterize_plants_get_all()
    conn = sqlite3.connect(f"{g.DATA_FOLDERPATH}/reference/gift/gift.db")
    cursor = conn.cursor()
    for i, master_plant_row in enumerate(master_plants_rows[:]):
        print(f'{i}/{len(master_plants_rows)}')
        plant_name_scientific_raw = master_plant_row[1]
        plant_name_scientific_norm = master_plant_row[2]
        cursor.execute("""
            SELECT 
                p.work_species,
                p.work_species_norm,
                p.work_genus,
                p.work_author,
                tm.category,
                tm.trait1,
                tm.trait2,
                tm.units,
                tm.type,
                pt.trait_value,
                pt.agreement,
                pt.coeff_var,
                pt.n,
                pt.refs
            FROM species p
            JOIN traits pt 
                ON p.work_id = pt.work_id
            JOIN traits_meta tm 
                ON pt.trait_id = tm.lvl3
            WHERE p.work_species_norm = ?
            ORDER BY tm.category;
        """, (plant_name_scientific_norm,))
        rows = cursor.fetchall()
        output_items = []
        for row in rows:
            output_item = parse_utils.trait_create(
                plant_name_scientific_raw = row[0],
                plant_name_scientific_norm = row[1],
                plant_genus = row[2],
                plant_author = row[3],
                trait_category = row[4],
                trait_1 = row[5],
                trait_2 = row[6],
                trait_units = row[7],
                trait_type = row[8],
                trait_value = row[9],
                trait_agreement = row[10],
                trait_coeff_var = row[11],
                trait_n = row[12],
                trait_refs = row[13],
                source_name = 'Global Inventory of Floras and Traits',
                source_acronym = 'GIFT',
            )
            output_items.append(output_item)
            # print(json.dumps(output_item, indent=4))
            # quit()

        output_filepath = f'{output_folderpath}/{plant_name_scientific_raw}.json'
        io.json_write(output_filepath, output_items)

    conn.close()
       

def run():
    print(f'''HERBS >> PARSE >> col''')

    start = time.perf_counter()
    parse_traits()
    print(f'parse traits() - execution time: ', time.perf_counter() - start)

