import os
import time
import json
import shutil
import sqlite3

from lib import g
from lib import io


def observations_table_plants_taxonomies_create(regen=False):
    output_foldername = 'observe'
    output_folderpath = f'{g.VAULT_FOLDERPATH}/terrawhisper/data/{output_foldername}'
    # try: shutil.rmtree(output_folderpath)
    # except: pass
    os.makedirs(output_folderpath, exist_ok=True)
    db_filepath = f'{output_folderpath}/observations.db'
    ###
    conn = sqlite3.connect(db_filepath)
    cur = conn.cursor()
    if regen:
        cur.execute("DROP TABLE IF EXISTS plants_taxonomies")
    cur.execute("""
        CREATE TABLE IF NOT EXISTS plants_taxonomies (
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
    cur.execute("CREATE INDEX IF NOT EXISTS idx_plants_chemicals_plant_canonical_name ON plants_chemicals(plant_canonical_name)")
    conn.commit()
    conn.close()

def observations_table_plants_chemicals_create(regen=False):
    output_foldername = 'observe'
    output_folderpath = f'{g.VAULT_FOLDERPATH}/terrawhisper/data/{output_foldername}'
    # try: shutil.rmtree(output_folderpath)
    # except: pass
    os.makedirs(output_folderpath, exist_ok=True)
    db_filepath = f'{output_folderpath}/observations.db'
    ###
    conn = sqlite3.connect(db_filepath)
    cur = conn.cursor()
    if regen:
        cur.execute("DROP TABLE IF EXISTS plants_chemicals")
    cur.execute("""
        CREATE TABLE IF NOT EXISTS plants_chemicals (
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
    cur.execute("CREATE INDEX IF NOT EXISTS idx_plants_chemicals_plant_canonical_name ON plants_chemicals(plant_canonical_name)")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_plants_chemicals_plant_canonical_name ON plants_chemicals(chemical_canonical_name)")
    conn.commit()
    conn.close()

def observations_table_plants_activities_create(regen=False):
    output_foldername = 'observe'
    output_folderpath = f'{g.VAULT_FOLDERPATH}/terrawhisper/data/{output_foldername}'
    # try: shutil.rmtree(output_folderpath)
    # except: pass
    os.makedirs(output_folderpath, exist_ok=True)
    db_filepath = f'{output_folderpath}/observations.db'
    ###
    conn = sqlite3.connect(db_filepath)
    cur = conn.cursor()
    if regen:
        cur.execute("DROP TABLE IF EXISTS plants_activities")
    cur.execute("""
        CREATE TABLE IF NOT EXISTS plants_activities (
            id INTEGER PRIMARY KEY,
            plant_canonical_name TEXT NOT NULL,
            activity_canonical_name TEXT NOT NULL,
            source_name TEXT NOT NULL
        );
    """)
    conn.execute("PRAGMA journal_mode = WAL;")
    conn.execute("PRAGMA synchronous = OFF;")
    conn.execute("PRAGMA temp_store = MEMORY;")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_plants_activities_plant_canonical_name ON plants_activities(plant_canonical_name)")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_plants_activities_plant_canonical_name ON plants_activities(activity_canonical_name)")
    conn.commit()
    conn.close()

def observations_table_plants_diseases_create(regen=False):
    output_foldername = 'observe'
    output_folderpath = f'{g.VAULT_FOLDERPATH}/terrawhisper/data/{output_foldername}'
    # try: shutil.rmtree(output_folderpath)
    # except: pass
    os.makedirs(output_folderpath, exist_ok=True)
    db_filepath = f'{output_folderpath}/observations.db'
    ###
    conn = sqlite3.connect(db_filepath)
    cur = conn.cursor()
    if regen:
        cur.execute("DROP TABLE IF EXISTS plants_diseases")
    cur.execute("""
        CREATE TABLE IF NOT EXISTS plants_diseases (
            id INTEGER PRIMARY KEY,
            plant_canonical_name TEXT NOT NULL,
            disease_canonical_name TEXT NOT NULL,
            source_name TEXT NOT NULL
        );
    """)
    conn.execute("PRAGMA journal_mode = WAL;")
    conn.execute("PRAGMA synchronous = OFF;")
    conn.execute("PRAGMA temp_store = MEMORY;")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_plants_diseases_plant_canonical_name ON plants_diseases(plant_canonical_name)")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_plants_diseases_plant_canonical_name ON plants_diseases(disease_canonical_name)")
    conn.commit()
    conn.close()

def run():
    print('OBSERVE >> init')

    ### TODO: do a clean up by destroying db
    observations_table_plants_taxonomies_create(regen=True)
    # observations_table_plants_chemicals_create(regen=True)
    # observations_table_plants_activities_create(regen=True)
    # observations_table_plants_diseases_create(regen=True)

