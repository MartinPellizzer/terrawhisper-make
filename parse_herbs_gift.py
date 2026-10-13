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
import schema_herbs

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

def schema_parse_traits(schema_item):
    schema_table_name = schema_item['table_name']
    schema_fields = schema_item['fields']
    output_folderpath = f'{HUB_FOLDERPATH}/parse/gift/{schema_table_name}/json'
    if schema_item['regen'] == True:
        try: shutil.rmtree(output_folderpath)
        except: pass
    io.folders_recursive_gen(output_folderpath)
    ###
    master_plants_rows = masterize_utils.masterize_plants_get_all()
    conn = sqlite3.connect(f"{HUB_FOLDERPATH}/reference/gift/gift.db")
    cursor = conn.cursor()
    output_items_last = []
    for i, master_plant_row in enumerate(master_plants_rows[:]):
        print(f'PARSE HERBS TRAITS {i}/{len(master_plants_rows)}')
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
        ###
        entity_1_key = schema_fields[0]['field_name']
        relationship_key = schema_fields[1]['field_name']
        entity_2_key = schema_fields[2]['field_name']
        ###
        output_items = []
        for row in rows:
            output_item = {
                f'{entity_1_key}_raw': row[0],
                f'{relationship_key}_raw': 'has_trait',
                f'{entity_2_key}_raw': row[5],
                f'trait_2_name': row[6],
                f'trait_units': row[7],
                f'trait_type': row[8],
                f'trait_value': row[9],
                f'trait_category': row[4],
                f'plant_author': row[3],
                f'plant_genus': row[2],
                f'trait_agreement': row[10],
                f'trait_coeff_var': row[11],
                f'trait_n': row[12],
                f'trait_refs': row[13],
                f'source_name': 'Global Inventory of Floras and Traits',
                f'source_acronym': 'GIFT',
                f'reference_id': '',
                f'reference_name': '',
            }
            """
            source_name = 'Global Inventory of Floras and Traits',
            source_acronym = 'GIFT',
            """
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

def parse_traits():
    schema_table_name = schema_item['table_name']
    schema_fields = schema_item['fields']
    output_folderpath = f'{HUB_FOLDERPATH}/parse/gift/{schema_table_name}/json'
    if schema_item['regen'] == True:
        try: shutil.rmtree(output_folderpath)
        except: pass
    io.folders_recursive_gen(output_folderpath)
    ###
    master_plants_rows = masterize_utils.masterize_plants_get_all()
    conn = sqlite3.connect(f"{HUB_FOLDERPATH}/reference/gift/gift.db")
    cursor = conn.cursor()
    output_items_last = []
    for i, master_plant_row in enumerate(master_plants_rows[:]):
        print(f'PARSE HERBS TRAITS {i}/{len(master_plants_rows)}')
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
    print(f'''HERBS >> PARSE >> gift''')

    start = time.perf_counter()
    # parse_traits()
    print(f'parse traits() - execution time: ', time.perf_counter() - start)

    schema_items = schema_herbs.data['items']
    for schema_item in schema_items: 
        if schema_item['process'] != True: continue
        sources_names = [
            source['source_name'] 
            for source in schema_item['sources']
        ]
        if 'gift' not in sources_names: continue
        if schema_item['table_name'] == 'plants_traits':
            schema_parse_traits(schema_item)
    # quit()
