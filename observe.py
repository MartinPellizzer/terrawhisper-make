import os
import time
import json
import shutil
import sqlite3

from lib import g
from lib import io

import observe_pubmed
import observe_drduke

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
    ### TARGET TABLE (in the future)
    '''
    CREATE TABLE observations (
        id INTEGER PRIMARY KEY,
        -- What plant?
        plant_id INTEGER NOT NULL,
        -- What chemical?
        compound_id INTEGER NOT NULL,
        -- Which part of the plant?
        plant_part TEXT,
        -- Was the compound detected?
        detected INTEGER NOT NULL DEFAULT 1,
        -- Concentration (nullable)
        concentration REAL,
        -- Unit (mg/g, %, ppm, etc.)
        unit TEXT,
        -- Measurement basis
        -- e.g. dry_weight, fresh_weight, essential_oil, extract
        basis TEXT,
        -- Optional analytical method
        -- GC-MS, LC-MS, HPLC...
        method TEXT,
        -- Source publication
        source_id INTEGER NOT NULL,
        -- Optional page/table/figure
        source_location TEXT,
        -- Confidence in extraction
        confidence REAL DEFAULT 1.0
    );
    '''
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

### TODO: do a clean up by destroying db
observations_table_plants_chemicals_create(regen=True)
# observations_table_plants_activities_create(regen=True)
# observations_table_plants_diseases_create(regen=True)

observe_pubmed.run()
# observe_drduke.run()

