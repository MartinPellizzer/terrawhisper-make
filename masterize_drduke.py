import os
import time
import json
import shutil
import sqlite3

from lib import g
from lib import io
from lib import llm

def build():
    input_folderpath = f'{g.VAULT_FOLDERPATH}/terrawhisper/data/resolve/pubmed/chemicals/json'
    output_folderpath = f'{g.VAULT_FOLDERPATH}/terrawhisper/data/masterize'
    try: shutil.rmtree(output_folderpath)
    except: pass
    os.makedirs(output_folderpath, exist_ok=True)
    ###
    db_filepath = f'{output_folderpath}/master.db'
    input_filenames = os.listdir(input_folderpath)
    all_data = []
    for i, input_filename in enumerate(input_filenames[:]):
        print(f'{i}/{len(input_filenames)}')
        input_filepath = f'{input_folderpath}/{input_filename}'
        ###
        input_data = io.json_read(input_filepath)
        for input_item in input_data:
            all_data.append(input_item)
    ###
    '''
    for item in all_data:
        print(json.dumps(item, indent=4))
        quit()
    '''

    conn = sqlite3.connect(db_filepath)
    cur = conn.cursor()
    cur.execute("DROP TABLE IF EXISTS plants")
    cur.execute("""
        CREATE TABLE IF NOT EXISTS plants (
            id INTEGER PRIMARY KEY,
            canonical_name TEXT NOT NULL UNIQUE
        );
    """)

    conn.execute("PRAGMA journal_mode = WAL;")
    conn.execute("PRAGMA synchronous = OFF;")
    conn.execute("PRAGMA temp_store = MEMORY;")

    print('start inserting...')
    cur.executemany(
        """
        INSERT OR IGNORE INTO plants (canonical_name)
        VALUES (?)
        """,
        [
            (
                item.get("plant_name"),
            )
            for item in all_data
        ]
    )

    cur.execute("CREATE INDEX idx_plants_canonical_name ON plants(canonical_name)")

    conn.commit()
    conn.close()

def sqlite__plants_add():
    source_foldername = 'drduke'
    input_foldername = 'resolve'
    output_foldername = 'masterize'
    ###
    input_folderpath = f'{g.VAULT_FOLDERPATH}/terrawhisper/data/{input_foldername}/{source_foldername}/json'
    output_folderpath = f'{g.VAULT_FOLDERPATH}/terrawhisper/data/{output_foldername}'
    input_filenames = os.listdir(input_folderpath)
    ###
    db_filepath = f'{output_folderpath}/master.db'
    conn = sqlite3.connect(db_filepath)
    cur = conn.cursor()
    ###
    all_data = []
    for i, input_filename in enumerate(input_filenames[:]):
        print(f'{i}/{len(input_filenames)}')
        input_filepath = f'{input_folderpath}/{input_filename}'
        input_data = io.json_read(input_filepath)
        all_data.append(input_data)
    ###
    cur.executemany(
        """
        INSERT OR IGNORE INTO plants (canonical_name)
        VALUES (?)
        """,
        [
            (
                item.get("herb_name_latin"),
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
    print('MASTERIZE >> drduke')

    # build()
    sqlite__plants_add()
    test()

