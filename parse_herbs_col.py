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

def parse_names(schema_item):
    schema_table_name = schema_item['table_name']
    schema_fields = schema_item['fields']
    output_folderpath = f'{HUB_FOLDERPATH}/parse/col/{schema_table_name}/json'
    if schema_item['regen'] == True:
        try: shutil.rmtree(output_folderpath)
        except: pass
    io.folders_recursive_gen(output_folderpath)
    ###
    master_plants_rows = masterize_utils.masterize_plants_get_all()
    conn = sqlite3.connect(f"{HUB_FOLDERPATH}/reference/col/col.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    for i, master_plant_row in enumerate(master_plants_rows[:]):
        print(f'{i}/{len(master_plants_rows)}')
        print(master_plant_row)
        plant_name_scientific_reference = master_plant_row['plant_name_scientific_reference']
        plant_name_scientific_reference_normalize = master_plant_row['plant_name_scientific_reference_normalize']

        cursor.execute("""
            SELECT v.*
            FROM name_usage n
            JOIN vernacular_name v
                ON v.col_id = n.col_id
            WHERE n.plant_name_scientific_normalize = ?
        """, (plant_name_scientific_reference_normalize,))
        rows = cursor.fetchall()
        items = [dict(row) for row in rows]
        # print(items[0])
        # quit()

        output_items = []
        for item in items:
            # print(row)
            # quit()
            '''
            output_item = parse_utils.common_name_create(
                plant_name_scientific_raw = plant_name_scientific_reference,
                # plant_name_scientific_reference_normalize = plant_name_scientific_reference,
                plant_name_common_raw = item['name'],
                plant_name_common_transliteration = item['transliteration'],
                plant_name_common_language = item['language'],
                plant_name_common_preferred = item['preferred'],
                plant_name_common_country = item['country'],
                plant_name_common_area = item['area'],
                plant_name_common_type = 'vernacular',
                source_name = 'Catalogue of Life',
                source_acronym = 'COL',
            )
            '''
            output_item = {
                f'plant_name_scientific_raw': plant_name_scientific_reference,
                f'relationship_name_raw': 'has_name_common',
                f'plant_name_common_raw': item['name'],
                f'plant_name_common_transliteration': item['transliteration'],
                f'plant_name_common_language': item['language'],
                f'plant_name_common_preferred': item['preferred'],
                f'plant_name_common_country': item['country'],
                f'plant_name_common_area': item['area'],
                f'plant_name_common_type': 'vernacular',
                f'source_name': 'Catalogue of Life',
                f'source_acronym': 'COL',
                f'reference_id': '',
                f'reference_name': '',
            }
            output_items.append(output_item)
            # print(json.dumps(output_item, indent=4))
            # quit()

        output_filepath = f'{output_folderpath}/{plant_name_scientific_reference}.json'
        io.json_write(output_filepath, output_items)

    conn.close()

def run():
    print(f'''HERBS >> PARSE >> col''')

    '''
    start = time.perf_counter()
    parse_names()
    print(f'parse names() - execution time: ', time.perf_counter() - start)
    '''

    schema_items = schema_herbs.data['items']
    for schema_item in schema_items: 
        if schema_item['process'] != True: continue
        sources_names = [
            source['source_name'] 
            for source in schema_item['sources']
        ]
        if 'col' not in sources_names: continue
        parse_names(schema_item)

