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
    source_foldername = 'wikidata'
    input_foldername = 'resolve'
    output_foldername = 'observe'
    input_folderpath = f'{g.DATA_FOLDERPATH}/{input_foldername}/{source_foldername}/json'
    output_folderpath = f'{g.DATA_FOLDERPATH}/{output_foldername}'
    ###
    db_filepath = f'{output_folderpath}/observations.db'
    input_filenames = os.listdir(input_folderpath)
    all_data = []
    for i, input_filename in enumerate(input_filenames[:]):
        print(f'{i}/{len(input_filenames)}')
        input_filepath = f'{input_folderpath}/{input_filename}'
        input_data = io.json_read(input_filepath)
        all_data.append(input_data)
    ###
    conn = sqlite3.connect(db_filepath)
    cur = conn.cursor()
    print('start inserting...')
    cur.executemany(
        f"""
        INSERT OR IGNORE INTO {table_name} (
            plant_canonical_name, 
            label_en,
            alias_en,
            source
        )
        VALUES (?, ?, ?, ?)
        """,
        [
            (
                item.get("wcvp_taxon_name").capitalize(),
                item.get("labels_en"),
                item.get("aliases_en"),
                'Wikidata',
            )
            for item in all_data
        ]
    )
    conn.commit()
    rows = conn.execute(f"SELECT * FROM {table_name}")
    for row in list(rows)[:10]:
        print(row)
    conn.close()

def run():
    print('OBSERVE >> wikidata')

    observations_table_plants_names_add()
