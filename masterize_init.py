import os
import time
import json
import shutil
import sqlite3

from lib import g
from lib import io

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
            canonical_name TEXT NOT NULL UNIQUE,
            canonical_name_normalized TEXT NOT NULL UNIQUE
        );
    """)
    conn.execute("PRAGMA journal_mode = WAL;")
    conn.execute("PRAGMA synchronous = OFF;")
    conn.execute("PRAGMA temp_store = MEMORY;")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_plants_canonical_name ON plants(canonical_name)")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_plants_canonical_name_normalized ON plants(canonical_name_normalized)")
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
            canonical_name TEXT NOT NULL UNIQUE,
            canonical_name_normalized TEXT NOT NULL UNIQUE
        );
    """)
    conn.execute("PRAGMA journal_mode = WAL;")
    conn.execute("PRAGMA synchronous = OFF;")
    conn.execute("PRAGMA temp_store = MEMORY;")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_activities_canonical_name ON activities(canonical_name)")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_activities_canonical_name_normalized ON activities(canonical_name_normalized)")
    conn.commit()
    conn.close()

def master_table_diseases_create(regen=False):
    output_folderpath = f'{g.VAULT_FOLDERPATH}/terrawhisper/data/masterize'
    # try: shutil.rmtree(output_folderpath)
    # except: pass
    # os.makedirs(output_folderpath, exist_ok=True)
    db_filepath = f'{output_folderpath}/master.db'
    ###
    conn = sqlite3.connect(db_filepath)
    cur = conn.cursor()
    if regen:
        cur.execute("DROP TABLE IF EXISTS diseases")
    cur.execute("""
        CREATE TABLE IF NOT EXISTS diseases (
            id INTEGER PRIMARY KEY,
            canonical_name TEXT NOT NULL UNIQUE
        );
    """)
    conn.execute("PRAGMA journal_mode = WAL;")
    conn.execute("PRAGMA synchronous = OFF;")
    conn.execute("PRAGMA temp_store = MEMORY;")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_diseases_canonical_name ON diseases(canonical_name)")
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

def run():
    master_table_plants_create(regen=True)
    master_table_activities_create(regen=True)
    # master_table_diseases_create(regen=True)
    # test()
