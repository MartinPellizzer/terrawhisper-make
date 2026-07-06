import os
import time
import json
import shutil
import sqlite3

from lib import g
from lib import io
from lib import llm

def is_number(s):
    try:
        float(s)
        return True
    except (ValueError, TypeError):
        return False

def observations_table_plants_chemicals_add():
    source_foldername = 'drduke'
    input_foldername = 'resolve'
    output_foldername = 'observe'
    ###
    input_folderpath = f'{g.VAULT_FOLDERPATH}/terrawhisper/data/{input_foldername}/{source_foldername}/json'
    output_folderpath = f'{g.VAULT_FOLDERPATH}/terrawhisper/data/{output_foldername}'
    input_filenames = os.listdir(input_folderpath)
    ###
    all_data = []
    for i, input_filename in enumerate(input_filenames[:]):
        print(f'{i}/{len(input_filenames)}')
        input_filepath = f'{input_folderpath}/{input_filename}'
        input_data = io.json_read(input_filepath)
        # print(input_data)
        # quit()
        if 'chemicals' not in input_data: continue
        for input_item in input_data['chemicals']:
            low_ppm = input_item['Low Parts Per Million']
            high_ppm = input_item['High Parts Per Million']
            output_items = []
            # print(low_ppm)
            # print(high_ppm)
            # quit()
            if not is_number(low_ppm) and not is_number(high_ppm):
                output_items.append({
                    'plant_canonical_name': input_data['herb_name_latin'],
                    'chemical_canonical_name': input_item['Chemical Name'],
                    'plant_part': input_item['Plant Part'],
                    'concentration': None,
                    'unit': 'ppm',
                    'source_name': input_item['Reference'],
                })
            if is_number(low_ppm):
                output_items.append({
                    'plant_canonical_name': input_data['herb_name_latin'],
                    'chemical_canonical_name': input_item['Chemical Name'],
                    'plant_part': input_item['Plant Part'],
                    'concentration': low_ppm,
                    'unit': 'ppm',
                    'source_name': input_item['Reference'],
                })
            if is_number(high_ppm):
                output_items.append({
                    'plant_canonical_name': input_data['herb_name_latin'],
                    'chemical_canonical_name': input_item['Chemical Name'],
                    'plant_part': input_item['Plant Part'],
                    'concentration': high_ppm,
                    'unit': 'ppm',
                    'source_name': input_item['Reference'],
                })
            # print(input_item)
            for output_item in output_items:
                all_data.append(output_item)
                print(output_item)
    ###
    db_filepath = f'{output_folderpath}/observations.db'
    conn = sqlite3.connect(db_filepath)
    cur = conn.cursor()
    print('start inserting...')
    cur.executemany(
        """
        INSERT OR IGNORE INTO plants_chemicals (plant_canonical_name, chemical_canonical_name, plant_part, concentration, unit, source_name)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        [
            (
                item.get("plant_canonical_name").capitalize(),
                item.get("chemical_canonical_name"),
                item.get("plant_part"),
                item.get("concentration"),
                item.get("unit"),
                item.get("source_name"),
            )
            for item in all_data
        ]
    )
    conn.commit()
    conn.close()

def test():
    output_folderpath = f'{g.VAULT_FOLDERPATH}/terrawhisper/data/observe'
    db_filepath = f'{output_folderpath}/observations.db'
    conn = sqlite3.connect(db_filepath)
    rows = conn.execute("SELECT * FROM plants_chemicals")
    for row in list(rows)[:30]:
        print(row)
    conn.close()

def run():
    print('observe >> pubmed')

    observations_table_plants_chemicals_add()
    test()

