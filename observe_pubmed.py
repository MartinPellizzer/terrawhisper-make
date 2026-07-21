import os
import time
import json
import shutil
import sqlite3

from lib import g
from lib import io
from lib import llm

def observations_table_plants_parts_add():
    table_name = 'plants_parts'
    input_folderpath = f'{g.VAULT_FOLDERPATH}/terrawhisper/data/resolve/pubmed/plants_parts/json'
    output_folderpath = f'{g.VAULT_FOLDERPATH}/terrawhisper/data/observe'
    db_filepath = f'{output_folderpath}/observations.db'
    ###
    input_filenames = os.listdir(input_folderpath)
    all_data = []
    for i, input_filename in enumerate(input_filenames[:]):
        print(f'PLANTS_PARTS - {i}/{len(input_filenames)}')
        input_filepath = f'{input_folderpath}/{input_filename}'
        input_data = io.json_read(input_filepath)
        for input_item in input_data:
            all_data.append(input_item)
    ###
    conn = sqlite3.connect(db_filepath)
    cur = conn.cursor()
    cur.executemany(
        f"""
        INSERT OR IGNORE INTO {table_name} (
            plant_canonical_name, 
            plant_part_canonical_name, 
            source_name
        )
        VALUES (?, ?, ?)
        """,
        [
            (
                item.get("wcvp_taxon_name").capitalize(),
                item.get("terra_plant_part_name"),
                item.get("journal_title"),
            )
            for item in all_data
        ]
    )
    conn.commit()
    rows = conn.execute(f"SELECT * FROM {table_name}")
    for row in list(rows)[:10]:
        print(row)
    conn.close()

def observations_table_plants_chemicals_add():
    table_name = 'plants_chemicals'
    input_folderpath = f'{g.VAULT_FOLDERPATH}/terrawhisper/data/resolve/pubmed/chemicals/json'
    output_folderpath = f'{g.VAULT_FOLDERPATH}/terrawhisper/data/observe'
    db_filepath = f'{output_folderpath}/observations.db'
    ###
    input_filenames = os.listdir(input_folderpath)
    all_data = []
    for i, input_filename in enumerate(input_filenames[:]):
        print(f'PLANTS_CHEMICALS - {i}/{len(input_filenames)}')
        input_filepath = f'{input_folderpath}/{input_filename}'
        input_data = io.json_read(input_filepath)
        for input_item in input_data:
            all_data.append(input_item)
    ###
    conn = sqlite3.connect(db_filepath)
    cur = conn.cursor()
    cur.executemany(
        f"""
        INSERT OR IGNORE INTO {table_name} (
            plant_canonical_name, 
            chemical_canonical_name, 
            plant_part, 
            source_name
        )
        VALUES (?, ?, ?, ?)
        """,
        [
            (
                item.get("plant_name").capitalize(),
                item.get("chemical_name"),
                item.get("plant_part_name"),
                item.get("journal_title"),
            )
            for item in all_data
        ]
    )
    conn.commit()
    rows = conn.execute(f"SELECT * FROM {table_name}")
    for row in list(rows)[:10]:
        print(row)
    conn.close()

def observations_table_plants_activities_add():
    table_name = 'plants_activities'
    input_folderpath = f'{g.VAULT_FOLDERPATH}/terrawhisper/data/resolve/pubmed/activities/json'
    output_folderpath = f'{g.VAULT_FOLDERPATH}/terrawhisper/data/observe'
    db_filepath = f'{output_folderpath}/observations.db'
    ###
    input_filenames = os.listdir(input_folderpath)
    all_data = []
    for i, input_filename in enumerate(input_filenames[:]):
        print(f'PLANTS_ACTIVITIES - {i}/{len(input_filenames)}')
        input_filepath = f'{input_folderpath}/{input_filename}'
        input_data = io.json_read(input_filepath)
        for input_item in input_data:
            all_data.append(input_item)
    ###
    conn = sqlite3.connect(db_filepath)
    cur = conn.cursor()
    cur.executemany(
        f"""
            INSERT OR IGNORE INTO {table_name} (
                plant_canonical_name, 
                activity_canonical_name, 
                source_name
            )
            VALUES (?, ?, ?)
        """,
        [
            (
                item.get("wcvp_taxon_name").capitalize(),
                item.get("drduke_activity_name"),
                item.get("journal_title"),
            )
            for item in all_data
        ]
    )
    conn.commit()
    rows = conn.execute(f"SELECT * FROM {table_name}")
    for row in list(rows)[:10]:
        print(row)
    conn.close()

def observations_table_plants_diseases_add():
    table_name = 'plants_diseases'
    input_folderpath = f'{g.VAULT_FOLDERPATH}/terrawhisper/data/resolve/pubmed/diseases/json'
    output_folderpath = f'{g.VAULT_FOLDERPATH}/terrawhisper/data/observe'
    db_filepath = f'{output_folderpath}/observations.db'
    ###
    input_filenames = os.listdir(input_folderpath)
    all_data = []
    for i, input_filename in enumerate(input_filenames[:]):
        print(f'PLANTS_DISEASES - {i}/{len(input_filenames)}')
        input_filepath = f'{input_folderpath}/{input_filename}'
        input_data = io.json_read(input_filepath)
        for input_item in input_data:
            all_data.append(input_item)
    ###
    conn = sqlite3.connect(db_filepath)
    cur = conn.cursor()
    cur.executemany(
        f"""
            INSERT OR IGNORE INTO {table_name} (
                plant_canonical_name, 
                disease_canonical_name, 
                source_name
            )
            VALUES (?, ?, ?)
        """,
        [
            (
                item.get("plant_name").capitalize(),
                item.get("disease_name"),
                item.get("journal_title"),
            )
            for item in all_data
        ]
    )
    conn.commit()
    rows = conn.execute(f"SELECT * FROM {table_name}")
    for row in list(rows)[:10]:
        print(row)
    conn.close()

### TODO: complete for passing data labels for query
def observations_table_insert(folder_name, table_name, query):
    input_folderpath = f'{g.VAULT_FOLDERPATH}/terrawhisper/data/resolve/pubmed/{folder_name}/json'
    output_folderpath = f'{g.VAULT_FOLDERPATH}/terrawhisper/data/observe'
    db_filepath = f'{output_folderpath}/observations.db'
    ###
    input_filenames = os.listdir(input_folderpath)
    all_data = []
    for i, input_filename in enumerate(input_filenames[:]):
        print(f'{i}/{len(input_filenames)}')
        input_filepath = f'{input_folderpath}/{input_filename}'
        input_data = io.json_read(input_filepath)
        for input_item in input_data:
            all_data.append(input_item)
    ###
    conn = sqlite3.connect(db_filepath)
    cur = conn.cursor()
    cur.executemany(
        query,
        [
            (
                item.get("plant_name").capitalize(),
                item.get("disease_name"),
                item.get("journal_title"),
            )
            for item in all_data
        ]
    )
    conn.commit()
    rows = conn.execute(f"SELECT * FROM {table_name}")
    for row in list(rows)[:10]:
        print(row)
    conn.close()

def peek(table_name):
    output_folderpath = f'{g.VAULT_FOLDERPATH}/terrawhisper/data/observe'
    db_filepath = f'{output_folderpath}/observations.db'
    conn = sqlite3.connect(db_filepath)
    rows = conn.execute(f"SELECT * FROM {table_name}")
    for row in list(rows)[:10]:
        print(row)
    conn.close()

def run():
    print('OBSERVE >> pubmed')

    observations_table_plants_parts_add()
    observations_table_plants_chemicals_add()
    observations_table_plants_activities_add()
    observations_table_plants_diseases_add()

    '''
    folder_name = 'plants_parts'
    table_name = 'plants_parts'
    observations_table_insert(
        folder_name = folder_name,
        table_name = table_name,
        query = f"""
            INSERT OR IGNORE INTO {table_name} (
                plant_canonical_name, 
                plant_part_canonical_name, 
                source_name
            )
            VALUES (?, ?, ?)
        """,
    )
    '''
