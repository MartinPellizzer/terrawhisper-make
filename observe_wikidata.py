import os
import time
import json
import shutil
import sqlite3

from lib import g
from lib import io
from lib import llm

def observations_table_plants_names_add():
    table_name = 'plants_names'
    input_folderpath = f'{g.DATA_FOLDERPATH}/resolve/wikidata/json'
    output_folderpath = f'{g.DATA_FOLDERPATH}/observe'
    db_filepath = f'{output_folderpath}/observations.db'
    ###
    input_filenames = os.listdir(input_folderpath)
    all_data = []
    for i, input_filename in enumerate(input_filenames[:]):
        print(f'{i}/{len(input_filenames)}')
        input_filepath = f'{input_folderpath}/{input_filename}'
        input_data = io.json_read(input_filepath)
        ### PROCESS LABELS
        for label in input_data['labels']:
            item = {
                'wcvp_taxon_name': input_data['wcvp_taxon_name'],
                'name_type': 'label',
                'language': label['language'],
                'value': label['value'],
                'source': input_data['source'],
            }
            all_data.append(item)
        ### PROCESS ALIASES
        for alias_list in input_data['aliases']:
            for alias in alias_list:
                item = {
                    'wcvp_taxon_name': input_data['wcvp_taxon_name'],
                    'name_type': 'alias',
                    'language': alias['language'],
                    'value': alias['value'],
                    'source': input_data['source'],
                }
                all_data.append(item)
    all_data_query = [
        (
            item.get("wcvp_taxon_name").capitalize(),
            item.get("name_type"),
            item.get("language"),
            item.get("value"),
            'Wikidata',
        )
        for item in all_data
    ]
    ###
    conn = sqlite3.connect(db_filepath)
    cur = conn.cursor()
    cur.executemany(
        f"""
        INSERT OR IGNORE INTO {table_name} (
            plant_canonical_name, 
            name_type,
            language_code,
            language_value,
            source
        )
        VALUES (?, ?, ?, ?, ?)
        """, all_data_query
    )
    conn.commit()
    rows = conn.execute(f"SELECT * FROM {table_name}")
    for row in list(rows)[:10]:
        print(row)
    conn.close()

def run():
    print('OBSERVE >> wikidata')

    observations_table_plants_names_add()

