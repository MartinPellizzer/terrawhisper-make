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

HUB_FOLDERPATH = f'''{g.DATA_FOLDERPATH}/herbs'''

def trait_create(
    plant_name_scientific_reference,
    plant_name_scientific_reference_normalize,
    plant_genus,
    plant_author,
    trait_category,
    trait_1,
    trait_2,
    trait_units,
    trait_type,
    trait_value,
    trait_agreement,
    trait_coeff_var,
    trait_n,
    trait_refs,
    source_name,
    source_acronym,
):
    item = {
        'plant_name_scientific_reference': plant_name_scientific_reference,
        'plant_name_scientific_reference_normalize': plant_name_scientific_reference_normalize,
        'plant_genus': plant_genus,
        'plant_author': plant_author,
        'trait_category': trait_category,
        'trait_1': trait_1,
        'trait_2': trait_2,
        'trait_units': trait_units,
        'trait_type': trait_type,
        'trait_value': trait_value,
        'trait_agreement': trait_agreement,
        'trait_coeff_var': trait_coeff_var,
        'trait_n': trait_n,
        'trait_refs': trait_refs,
        'source_name': source_name,
        'source_acronym': source_acronym,
    }
    return item

def parse_traits():
    output_folderpath = f'{HUB_FOLDERPATH}/parse/gift/traits/json'
    try: shutil.rmtree(output_folderpath)
    except: pass
    io.folders_recursive_gen(output_folderpath)
    ###
    master_plants_rows = masterize_utils.masterize_plants_get_all()
    conn = sqlite3.connect(f"{HUB_FOLDERPATH}/reference/gift/gift.db")
    cursor = conn.cursor()
    output_items_last = []
    for i, master_plant_row in enumerate(master_plants_rows[:]):
        print(f'{i}/{len(master_plants_rows)}')
        # print(master_plant_row)
        # quit()
        plant_name_scientific_reference = master_plant_row['plant_name_scientific_reference']
        plant_name_scientific_reference_normalize = master_plant_row['plant_name_scientific_reference_normalize']
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
        """, (plant_name_scientific_reference_normalize,))
        rows = cursor.fetchall()
        output_items = []
        for row in rows:
            output_item = trait_create(
                plant_name_scientific_reference = row[0],
                plant_name_scientific_reference_normalize = row[1],
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
        output_filepath = f'{output_folderpath}/{plant_name_scientific_reference_normalize}.json'
        io.json_write(output_filepath, output_items)
        if output_items != []:
            output_items_last = output_items
    conn.close()
    print(json.dumps(output_items_last, indent=4))
    # quit()
       

def run():
    print(f'''HERBS >> PARSE >> col''')

    start = time.perf_counter()
    parse_traits()
    print(f'parse traits() - execution time: ', time.perf_counter() - start)

