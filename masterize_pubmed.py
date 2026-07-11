import os
import time
import json
import shutil
import sqlite3

from lib import g
from lib import io
from lib import llm


def master_table_plants_add():
    input_folderpath = f'{g.VAULT_FOLDERPATH}/terrawhisper/data/resolve/pubmed/chemicals/json'
    output_folderpath = f'{g.VAULT_FOLDERPATH}/terrawhisper/data/masterize'
    ###
    db_filepath = f'{output_folderpath}/master.db'
    input_filenames = os.listdir(input_folderpath)
    all_data = []
    for i, input_filename in enumerate(input_filenames[:]):
        print(f'{i}/{len(input_filenames)}')
        input_filepath = f'{input_folderpath}/{input_filename}'
        input_data = io.json_read(input_filepath)
        for input_item in input_data:
            all_data.append(input_item)
    conn = sqlite3.connect(db_filepath)
    cur = conn.cursor()
    print('start inserting...')
    cur.executemany(
        """
        INSERT OR IGNORE INTO plants (canonical_name)
        VALUES (?)
        """,
        [
            (
                item.get("plant_name").capitalize(), #TODO: remove capitalize in the future when better pipeline and the plant name here already is in canonical format
            )
            for item in all_data
        ]
    )
    conn.commit()
    conn.close()

def master_table_activities_add():
    input_folderpath = f'{g.VAULT_FOLDERPATH}/terrawhisper/data/resolve/pubmed/activities/json'
    output_folderpath = f'{g.VAULT_FOLDERPATH}/terrawhisper/data/masterize'
    ###
    db_filepath = f'{output_folderpath}/master.db'
    input_filenames = os.listdir(input_folderpath)
    all_data = []
    for i, input_filename in enumerate(input_filenames[:]):
        print(f'{i}/{len(input_filenames)}')
        input_filepath = f'{input_folderpath}/{input_filename}'
        input_data = io.json_read(input_filepath)
        all_data.append({
            'activity_name': input_data['reply']
        })
    print(all_data[0])
    quit()
    conn = sqlite3.connect(db_filepath)
    cur = conn.cursor()
    print('start inserting...')
    cur.executemany(
        """
        INSERT OR IGNORE INTO activities (canonical_name)
        VALUES (?)
        """,
        [
            (
                item.get("activity_name"),
            )
            for item in all_data
        ]
    )
    conn.commit()
    conn.close()

def test():
    output_folderpath = f'{g.VAULT_FOLDERPATH}/terrawhisper/data/masterize'
    db_filepath = f'{output_folderpath}/master.db'
    conn = sqlite3.connect(db_filepath)
    rows = conn.execute("SELECT * FROM plants")
    for row in list(rows)[:10]:
        print(row)
    conn.close()

def run():
    print('masterize >> pubmed')

    master_table_plants_add()
    # master_table_activities_add()
    test()

