import os
import time
import json
import shutil
import sqlite3

from lib import g
from lib import io

def master_table_plants_create(regen=False):
    output_folderpath = f'{g.VAULT_FOLDERPATH}/terrawhisper/data/masterize'
    db_filepath = f'{output_folderpath}/master.db'
    table_name = 'plants'
    ###
    conn = sqlite3.connect(db_filepath)
    cur = conn.cursor()
    if regen:
        cur.execute(f"DROP TABLE IF EXISTS {table_name}")
    cur.execute(f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            id INTEGER PRIMARY KEY,
            plant_name_scientific_canon TEXT NOT NULL UNIQUE,
            plant_name_scientific_canon_norm TEXT NOT NULL UNIQUE
        );
    """)
    conn.execute("PRAGMA journal_mode = WAL;")
    conn.execute("PRAGMA synchronous = OFF;")
    conn.execute("PRAGMA temp_store = MEMORY;")
    ###
    cur.execute(f"CREATE INDEX IF NOT EXISTS idx_{table_name}_canonical_name ON {table_name}(plant_name_scientific_canon)")
    cur.execute(f"CREATE INDEX IF NOT EXISTS idx_{table_name}_canonical_name_normalized ON {table_name}(plant_name_scientific_canon_norm)")
    conn.commit()
    conn.close()

def master_table_activities_create(regen=False):
    output_folderpath = f'{g.VAULT_FOLDERPATH}/terrawhisper/data/masterize'
    db_filepath = f'{output_folderpath}/master.db'
    table_name = 'activities'
    ###
    conn = sqlite3.connect(db_filepath)
    cur = conn.cursor()
    if regen:
        cur.execute(f"DROP TABLE IF EXISTS {table_name}")
    cur.execute(f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            id INTEGER PRIMARY KEY,
            activity_name_canon TEXT NOT NULL UNIQUE,
            activity_name_canon_norm TEXT NOT NULL UNIQUE
        );
    """)
    conn.execute("PRAGMA journal_mode = WAL;")
    conn.execute("PRAGMA synchronous = OFF;")
    conn.execute("PRAGMA temp_store = MEMORY;")
    ###
    cur.execute(f"CREATE INDEX IF NOT EXISTS idx_{table_name}_activity_name_canon ON {table_name}(activity_name_canon)")
    cur.execute(f"CREATE INDEX IF NOT EXISTS idx_{table_name}_activity_name_canon_norm ON {table_name}(activity_name_canon_norm)")
    conn.commit()
    conn.close()

def master_table_chemicals_create(regen=False):
    output_folderpath = f'{g.VAULT_FOLDERPATH}/terrawhisper/data/masterize'
    db_filepath = f'{output_folderpath}/master.db'
    table_name = 'chemicals'
    ###
    conn = sqlite3.connect(db_filepath)
    cur = conn.cursor()
    if regen:
        cur.execute(f"DROP TABLE IF EXISTS {table_name}")
    cur.execute(f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            id INTEGER PRIMARY KEY,
            chemical_name_canon TEXT NOT NULL UNIQUE,
            chemical_name_canon_norm TEXT NOT NULL UNIQUE
        );
    """)
    conn.execute("PRAGMA journal_mode = WAL;")
    conn.execute("PRAGMA synchronous = OFF;")
    conn.execute("PRAGMA temp_store = MEMORY;")
    cur.execute(f"CREATE INDEX IF NOT EXISTS idx_{table_name}_chemical_name_canon ON {table_name}(chemical_name_canon)")
    cur.execute(f"CREATE INDEX IF NOT EXISTS idx_{table_name}_chemical_name_canon_norm ON {table_name}(chemical_name_canon_norm)")
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
    master_table_chemicals_create(regen=True)
    # master_table_diseases_create(regen=True)
    # test()
