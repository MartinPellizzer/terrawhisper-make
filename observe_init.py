import os
import time
import json
import shutil
import sqlite3

from lib import g
from lib import io

output_folderpath = f'{g.VAULT_FOLDERPATH}/terrawhisper/data/observe'
db_filepath = f'{output_folderpath}/observations.db'

def observations_table_plants_taxonomies_create(regen=False):
    table_name = 'plants_taxonomies'
    conn = sqlite3.connect(db_filepath)
    cur = conn.cursor()
    if regen: cur.execute(f"DROP TABLE IF EXISTS {table_name}")
    cur.execute(f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            id INTEGER PRIMARY KEY,
            plant_canonical_name TEXT NOT NULL,
            taxon_kingdom TEXT,
            taxon_phylum TEXT,
            taxon_class TEXT,
            taxon_subclass TEXT,
            taxon_order TEXT,
            taxon_family TEXT,
            taxon_genus TEXT,
            source TEXT
        );
    """)
    conn.execute("PRAGMA journal_mode = WAL;")
    conn.execute("PRAGMA synchronous = OFF;")
    conn.execute("PRAGMA temp_store = MEMORY;")
    cur.execute(f"CREATE INDEX IF NOT EXISTS idx_{table_name}_plant_canonical_name ON {table_name}(plant_canonical_name)")
    conn.commit()
    conn.close()

def observations_table_plants_names_create(regen=False):
    table_name = 'plants_names'
    conn = sqlite3.connect(db_filepath)
    cur = conn.cursor()
    if regen: cur.execute(f"DROP TABLE IF EXISTS {table_name}")
    cur.execute(f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            id INTEGER PRIMARY KEY,
            plant_canonical_name TEXT NOT NULL,
            name_type TEXT,
            language_code TEXT,
            language_value TEXT,
            source TEXT
        );
    """)
    conn.execute("PRAGMA journal_mode = WAL;")
    conn.execute("PRAGMA synchronous = OFF;")
    conn.execute("PRAGMA temp_store = MEMORY;")
    cur.execute(f"CREATE INDEX IF NOT EXISTS idx_{table_name}_plant_canonical_name ON {table_name}(plant_canonical_name)")
    conn.commit()
    conn.close()

def observations_table_plants_distributions_create(regen=False):
    table_name = 'plants_distributions'
    conn = sqlite3.connect(db_filepath)
    cur = conn.cursor()
    if regen: cur.execute(f"DROP TABLE IF EXISTS {table_name}")
    cur.execute(f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            id INTEGER PRIMARY KEY,
            plant_canonical_name TEXT NOT NULL,
            continent TEXT NOT NULL,
            region TEXT NOT NULL,
            area TEXT NOT NULL,
            source TEXT
        );
    """)
    conn.execute("PRAGMA journal_mode = WAL;")
    conn.execute("PRAGMA synchronous = OFF;")
    conn.execute("PRAGMA temp_store = MEMORY;")
    cur.execute(f"CREATE INDEX IF NOT EXISTS idx_{table_name}_plant_canonical_name ON {table_name}(plant_canonical_name)")
    conn.commit()
    conn.close()

def observations_table_plants_parts_create(regen=False):
    table_name = 'plants_parts'
    conn = sqlite3.connect(db_filepath)
    cur = conn.cursor()
    if regen: cur.execute(f"DROP TABLE IF EXISTS {table_name}")
    cur.execute(f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            id INTEGER PRIMARY KEY,
            plant_canonical_name TEXT NOT NULL,
            plant_part_canonical_name TEXT NOT NULL,
            source_name TEXT
        );
    """)
    conn.execute("PRAGMA journal_mode = WAL;")
    conn.execute("PRAGMA synchronous = OFF;")
    conn.execute("PRAGMA temp_store = MEMORY;")
    cur.execute(f"CREATE INDEX IF NOT EXISTS idx_{table_name}_plant_canonical_name ON {table_name}(plant_canonical_name)")
    cur.execute(f"CREATE INDEX IF NOT EXISTS idx_{table_name}_plant_part_canonical_name ON {table_name}(plant_part_canonical_name)")
    conn.commit()
    conn.close()

def observations_table_plants_chemicals_create(regen=False):
    table_name = 'plants_chemicals'
    conn = sqlite3.connect(db_filepath)
    cur = conn.cursor()
    if regen: cur.execute(f"DROP TABLE IF EXISTS {table_name}")
    cur.execute(f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            id INTEGER PRIMARY KEY,
            plant_canonical_name TEXT NOT NULL,
            chemical_canonical_name TEXT NOT NULL,
            plant_part TEXT,
            concentration REAL,
            unit TEXT,
            source_name TEXT NOT NULL
        );
    """)
    conn.execute("PRAGMA journal_mode = WAL;")
    conn.execute("PRAGMA synchronous = OFF;")
    conn.execute("PRAGMA temp_store = MEMORY;")
    cur.execute(f"CREATE INDEX IF NOT EXISTS idx_{table_name}_plant_canonical_name ON {table_name}(plant_canonical_name)")
    cur.execute(f"CREATE INDEX IF NOT EXISTS idx_{table_name}_plant_canonical_name ON {table_name}(chemical_canonical_name)")
    conn.commit()
    conn.close()

def observations_table_plants_activities_create(regen=False):
    table_name = 'plants_activities'
    conn = sqlite3.connect(db_filepath)
    cur = conn.cursor()
    if regen: cur.execute(f"DROP TABLE IF EXISTS {table_name}")
    cur.execute(f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            id INTEGER PRIMARY KEY,
            plant_canonical_name TEXT NOT NULL,
            activity_canonical_name TEXT NOT NULL,
            source_name TEXT NOT NULL
        );
    """)
    conn.execute("PRAGMA journal_mode = WAL;")
    conn.execute("PRAGMA synchronous = OFF;")
    conn.execute("PRAGMA temp_store = MEMORY;")
    cur.execute(f"CREATE INDEX IF NOT EXISTS idx_{table_name}_plant_canonical_name ON {table_name}(plant_canonical_name)")
    cur.execute(f"CREATE INDEX IF NOT EXISTS idx_{table_name}_plant_canonical_name ON {table_name}(activity_canonical_name)")
    conn.commit()
    conn.close()

def observations_table_plants_diseases_create(regen=False):
    table_name = 'plants_diseases'
    conn = sqlite3.connect(db_filepath)
    cur = conn.cursor()
    if regen: cur.execute(f"DROP TABLE IF EXISTS {table_name}")
    cur.execute(f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            id INTEGER PRIMARY KEY,
            plant_canonical_name TEXT NOT NULL,
            disease_canonical_name TEXT NOT NULL,
            source_name TEXT NOT NULL
        );
    """)
    conn.execute("PRAGMA journal_mode = WAL;")
    conn.execute("PRAGMA synchronous = OFF;")
    conn.execute("PRAGMA temp_store = MEMORY;")
    cur.execute(f"CREATE INDEX IF NOT EXISTS idx_{table_name}_plant_canonical_name ON {table_name}(plant_canonical_name)")
    cur.execute(f"CREATE INDEX IF NOT EXISTS idx_{table_name}_plant_canonical_name ON {table_name}(disease_canonical_name)")
    conn.commit()
    conn.close()

def run():
    print('OBSERVE >> init')

    # try: shutil.rmtree(output_folderpath)
    # except: pass
    os.makedirs(output_folderpath, exist_ok=True)

    ### TODO: do a clean up by destroying db
    observations_table_plants_taxonomies_create(regen=True)
    observations_table_plants_names_create(regen=True)
    observations_table_plants_distributions_create(regen=True)
    observations_table_plants_parts_create(regen=True)
    observations_table_plants_chemicals_create(regen=True)
    observations_table_plants_activities_create(regen=True)
    observations_table_plants_diseases_create(regen=True)

