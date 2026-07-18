import os
import time
import json
import shutil
import sqlite3

from lib import g
from lib import io
from lib import llm

def observations_table_plants_chemicals_add():
    input_folderpath = f'{g.VAULT_FOLDERPATH}/terrawhisper/data/resolve/pubmed/chemicals/json'
    output_folderpath = f'{g.VAULT_FOLDERPATH}/terrawhisper/data/observe'
    ###
    db_filepath = f'{output_folderpath}/observations.db'
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
    print('start inserting...')
    cur.executemany(
        """
        INSERT OR IGNORE INTO plants_chemicals (plant_canonical_name, chemical_canonical_name, plant_part, source_name)
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
    conn.close()

def observations_table_plants_activities_add():
    input_folderpath = f'{g.VAULT_FOLDERPATH}/terrawhisper/data/resolve/pubmed/activities/json'
    output_folderpath = f'{g.VAULT_FOLDERPATH}/terrawhisper/data/observe'
    ###
    db_filepath = f'{output_folderpath}/observations.db'
    input_filenames = os.listdir(input_folderpath)
    all_data = []
    for i, input_filename in enumerate(input_filenames[:]):
        # print(f'{i}/{len(input_filenames)}')
        input_filepath = f'{input_folderpath}/{input_filename}'
        input_data = io.json_read(input_filepath)
        for input_item in input_data:
            all_data.append(input_item)
    ###
    conn = sqlite3.connect(db_filepath)
    cur = conn.cursor()
    print('start inserting...')
    cur.executemany(
        """
        INSERT OR IGNORE INTO plants_activities (plant_canonical_name, activity_canonical_name, source_name)
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
    rows = conn.execute("SELECT * FROM plants_activities")
    for row in list(rows)[:10]:
        print(row)
    conn.close()

def observations_table_plants_diseases_add():
    input_folderpath = f'{g.VAULT_FOLDERPATH}/terrawhisper/data/resolve/pubmed/diseases/json'
    output_folderpath = f'{g.VAULT_FOLDERPATH}/terrawhisper/data/observe'
    ###
    db_filepath = f'{output_folderpath}/observations.db'
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
    print('start inserting...')
    cur.executemany(
        """
        INSERT OR IGNORE INTO plants_diseases (plant_canonical_name, disease_canonical_name, source_name)
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
    rows = conn.execute("SELECT * FROM plants_diseases")
    for row in list(rows)[:10]:
        print(row)
    conn.close()

def test():
    output_folderpath = f'{g.VAULT_FOLDERPATH}/terrawhisper/data/observe'
    db_filepath = f'{output_folderpath}/observations.db'
    conn = sqlite3.connect(db_filepath)
    rows = conn.execute("SELECT * FROM plants_chemicals")
    for row in list(rows)[:10]:
        print(row)
    conn.close()

def run():
    print('OBSERVE >> pubmed')

    # observations_table_plants_chemicals_add()
    observations_table_plants_activities_add()
    # observations_table_plants_diseases_add()
