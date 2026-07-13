import os
import time
import json
import shutil
import sqlite3

from lib import g
from lib import io
from lib import llm

def master_table_plants_add():
    chemicals_input_folderpath = f'{g.VAULT_FOLDERPATH}/terrawhisper/data/resolve/pubmed/chemicals/json'
    activities_input_folderpath = f'{g.VAULT_FOLDERPATH}/terrawhisper/data/resolve/pubmed/activities/json'
    output_folderpath = f'{g.VAULT_FOLDERPATH}/terrawhisper/data/masterize'
    ### CHEMICALS > PLANTS
    input_filenames = os.listdir(chemicals_input_folderpath)
    chemicals_data = []
    for i, input_filename in enumerate(input_filenames[:]):
        print(f'{i}/{len(input_filenames)}')
        input_filepath = f'{chemicals_input_folderpath}/{input_filename}'
        input_data = io.json_read(input_filepath)
        for input_item in input_data:
            chemicals_data.append(input_item)
    chemicals_data_query = [(item.get("plant_name"),) for item in chemicals_data]
    ### ACTIVITIES > PLANTS
    input_filenames = os.listdir(activities_input_folderpath)
    activities_data = []
    for i, input_filename in enumerate(input_filenames[:]):
        print(f'{i}/{len(input_filenames)}')
        input_filepath = f'{activities_input_folderpath}/{input_filename}'
        input_data = io.json_read(input_filepath)
        for input_item in input_data:
            activities_data.append(input_item)
    activities_data_query = [(item.get("plant_name"),) for item in activities_data]

    ###
    db_filepath = f'{output_folderpath}/master.db'
    conn = sqlite3.connect(db_filepath)
    cur = conn.cursor()
    cur.executemany(
        """
        INSERT OR IGNORE INTO plants (canonical_name)
        VALUES (?)
        """, chemicals_data_query
    )
    cur.executemany(
        """
        INSERT OR IGNORE INTO plants (canonical_name)
        VALUES (?)
        """, activities_data_query
    )
    conn.commit()

    ### TEST
    rows = conn.execute("SELECT * FROM plants")
    for row in list(rows)[:10]:
        print(row)

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
        for input_item in input_data:
            all_data.append({
                'activity_name': input_item['activity_name']
            })
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
    rows = conn.execute("SELECT * FROM activities")
    for row in list(rows)[:10]:
        print(row)
    conn.close()

def master_table_diseases_add():
    input_folderpath = f'{g.VAULT_FOLDERPATH}/terrawhisper/data/resolve/pubmed/diseases/json'
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
            all_data.append({
                'disease_name': input_item['disease_name']
            })
    conn = sqlite3.connect(db_filepath)
    cur = conn.cursor()
    print('start inserting...')
    cur.executemany(
        """
        INSERT OR IGNORE INTO diseases (canonical_name)
        VALUES (?)
        """,
        [
            (
                item.get("disease_name"),
            )
            for item in all_data
        ]
    )
    conn.commit()
    rows = conn.execute("SELECT * FROM diseases")
    for row in list(rows)[:10]:
        print(row)
    conn.close()

def test():
    db_filepath = f'{g.VAULT_FOLDERPATH}/terrawhisper/data/masterize/master.db'
    conn = sqlite3.connect(db_filepath)
    cur = conn.cursor()
    cur.execute("""
        SELECT *
        FROM plants
    """)
    rows = cur.fetchall()
    for row in rows:
        print(row)
        if row[1].lower() == 'acacia caven':
            print(row)
            quit() 
    conn.close()
    return row

def run():
    print('masterize >> pubmed')

    master_table_plants_add()
    # master_table_activities_add()
    # master_table_diseases_add()

    # test()

