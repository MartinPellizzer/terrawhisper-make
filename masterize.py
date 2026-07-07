import os
import time
import json
import shutil
import sqlite3

from lib import g
from lib import io

import masterize_pubmed
import masterize_drduke

def master_table_plants_create(regen=False):
    output_folderpath = f'{g.VAULT_FOLDERPATH}/terrawhisper/data/masterize'
    # try: shutil.rmtree(output_folderpath)
    # except: pass
    # os.makedirs(output_folderpath, exist_ok=True)
    db_filepath = f'{output_folderpath}/master.db'
    ###
    conn = sqlite3.connect(db_filepath)
    cur = conn.cursor()
    if regen:
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
    cur.execute("CREATE INDEX IF NOT EXISTS idx_plants_canonical_name ON plants(canonical_name)")
    conn.commit()
    conn.close()

def master_table_activities_create(regen=False):
    output_folderpath = f'{g.VAULT_FOLDERPATH}/terrawhisper/data/masterize'
    # try: shutil.rmtree(output_folderpath)
    # except: pass
    # os.makedirs(output_folderpath, exist_ok=True)
    db_filepath = f'{output_folderpath}/master.db'
    ###
    conn = sqlite3.connect(db_filepath)
    cur = conn.cursor()
    if regen:
        cur.execute("DROP TABLE IF EXISTS activities")
    cur.execute("""
        CREATE TABLE IF NOT EXISTS activities (
            id INTEGER PRIMARY KEY,
            canonical_name TEXT NOT NULL UNIQUE
        );
    """)
    conn.execute("PRAGMA journal_mode = WAL;")
    conn.execute("PRAGMA synchronous = OFF;")
    conn.execute("PRAGMA temp_store = MEMORY;")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_activities_canonical_name ON activities(canonical_name)")
    conn.commit()
    conn.close()

def test():
    output_folderpath = f'{g.VAULT_FOLDERPATH}/terrawhisper/data/masterize'
    db_filepath = f'{output_folderpath}/master.db'
    conn = sqlite3.connect(db_filepath)
    rows = conn.execute("SELECT * FROM activities").fetchall()
    for row in rows[:10]:
        print(row)
    print(len(rows))
    conn.close()

# master_table_plants_create(regen=False)
master_table_activities_create(regen=False)
test()

# masterize_pubmed.run()
masterize_drduke.run()
