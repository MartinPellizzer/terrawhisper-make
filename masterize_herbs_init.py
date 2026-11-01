import os
import time
import json
import shutil
import sqlite3

from lib import g
from lib import io

HUB_FOLDERPATH = f'''{g.DATA_FOLDERPATH}/herbs'''

def master_table_studies_create(regen=False):
    table_name = 'studies'
    output_folderpath = f'{HUB_FOLDERPATH}/database'
    db_filepath = f'{output_folderpath}/terra.db'
    ###
    os.makedirs(output_folderpath, exist_ok=True)
    conn = sqlite3.connect(db_filepath)
    cur = conn.cursor()
    if regen:
        cur.execute(f"DROP TABLE IF EXISTS {table_name}")
    cur.execute(f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            study_id INTEGER PRIMARY KEY,
            study_pmid TEXT NOT NULL UNIQUE,
            study_title TEXT NOT NULL UNIQUE
        );
    """)
    conn.execute("PRAGMA journal_mode = WAL;")
    conn.execute("PRAGMA synchronous = OFF;")
    conn.execute("PRAGMA temp_store = MEMORY;")
    ###
    cur.execute(f"CREATE INDEX IF NOT EXISTS idx_{table_name}_study_pmid ON {table_name}(study_pmid)")
    cur.execute(f"CREATE INDEX IF NOT EXISTS idx_{table_name}_study_title ON {table_name}(study_title)")
    conn.commit()
    conn.close()

def master_table_plants_create(regen=False):
    table_name = 'plants'
    output_folderpath = f'{HUB_FOLDERPATH}/database'
    db_filepath = f'{output_folderpath}/terra.db'
    ###
    os.makedirs(output_folderpath, exist_ok=True)
    conn = sqlite3.connect(db_filepath)
    cur = conn.cursor()
    if regen:
        cur.execute(f"DROP TABLE IF EXISTS {table_name}")
    cur.execute(f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            plant_id INTEGER PRIMARY KEY,
            plant_name_scientific_reference TEXT NOT NULL UNIQUE,
            plant_name_scientific_reference_normalize TEXT NOT NULL UNIQUE
        );
    """)
    conn.execute("PRAGMA journal_mode = WAL;")
    conn.execute("PRAGMA synchronous = OFF;")
    conn.execute("PRAGMA temp_store = MEMORY;")
    ###
    cur.execute(f"CREATE INDEX IF NOT EXISTS idx_{table_name}_name_scientific_reference ON {table_name}(plant_name_scientific_reference)")
    cur.execute(f"CREATE INDEX IF NOT EXISTS idx_{table_name}_name_scientific_reference_normalize ON {table_name}(plant_name_scientific_reference_normalize)")
    conn.commit()
    conn.close()

def master_table_activities_create(regen=False):
    table_name = 'activities'
    output_folderpath = f'{HUB_FOLDERPATH}/database'
    db_filepath = f'{output_folderpath}/terra.db'
    ###
    os.makedirs(output_folderpath, exist_ok=True)
    conn = sqlite3.connect(db_filepath)
    cur = conn.cursor()
    if regen:
        cur.execute(f"DROP TABLE IF EXISTS {table_name}")
    cur.execute(f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            activity_id INTEGER PRIMARY KEY,
            activity_name_reference TEXT NOT NULL UNIQUE,
            activity_name_reference_normalize TEXT NOT NULL UNIQUE
        );
    """)
    conn.execute("PRAGMA journal_mode = WAL;")
    conn.execute("PRAGMA synchronous = OFF;")
    conn.execute("PRAGMA temp_store = MEMORY;")
    ###
    cur.execute(f"CREATE INDEX IF NOT EXISTS idx_{table_name}_activity_name_reference ON {table_name}(activity_name_reference)")
    cur.execute(f"CREATE INDEX IF NOT EXISTS idx_{table_name}_activity_name_reference_normalize ON {table_name}(activity_name_reference_normalize)")
    conn.commit()
    conn.close()

def master_table_conditions_create(regen=False):
    table_name = 'conditions'
    output_folderpath = f'{HUB_FOLDERPATH}/database'
    db_filepath = f'{output_folderpath}/terra.db'
    ###
    os.makedirs(output_folderpath, exist_ok=True)
    conn = sqlite3.connect(db_filepath)
    cur = conn.cursor()
    if regen:
        cur.execute(f"DROP TABLE IF EXISTS {table_name}")
    cur.execute(f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            condition_id INTEGER PRIMARY KEY,
            condition_name_reference TEXT NOT NULL UNIQUE,
            condition_name_reference_normalize TEXT NOT NULL UNIQUE
        );
    """)
    conn.execute("PRAGMA journal_mode = WAL;")
    conn.execute("PRAGMA synchronous = OFF;")
    conn.execute("PRAGMA temp_store = MEMORY;")
    ###
    cur.execute(f"CREATE INDEX IF NOT EXISTS idx_{table_name}_condition_name_reference ON {table_name}(condition_name_reference)")
    cur.execute(f"CREATE INDEX IF NOT EXISTS idx_{table_name}_condition_name_reference_normalize ON {table_name}(condition_name_reference_normalize)")
    conn.commit()
    conn.close()

def master_table_compounds_create(regen=False):
    table_name = 'compounds'
    output_folderpath = f'{HUB_FOLDERPATH}/database'
    db_filepath = f'{output_folderpath}/terra.db'
    ###
    os.makedirs(output_folderpath, exist_ok=True)
    conn = sqlite3.connect(db_filepath)
    cur = conn.cursor()
    if regen:
        cur.execute(f"DROP TABLE IF EXISTS {table_name}")
    cur.execute(f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            compound_id INTEGER PRIMARY KEY,
            compound_name_reference TEXT NOT NULL UNIQUE,
            compound_name_reference_normalize TEXT NOT NULL UNIQUE
        );
    """)
    conn.execute("PRAGMA journal_mode = WAL;")
    conn.execute("PRAGMA synchronous = OFF;")
    conn.execute("PRAGMA temp_store = MEMORY;")
    ###
    cur.execute(f"CREATE INDEX IF NOT EXISTS idx_{table_name}_compound_name_reference ON {table_name}(compound_name_reference)")
    cur.execute(f"CREATE INDEX IF NOT EXISTS idx_{table_name}_compound_name_reference_normalize ON {table_name}(compound_name_reference_normalize)")
    conn.commit()
    conn.close()

def master_table_plants_names_common_create(regen=False):
    table_name = 'plants_names_common'
    output_folderpath = f'{HUB_FOLDERPATH}/database'
    db_filepath = f'{output_folderpath}/terra.db'
    ###
    os.makedirs(output_folderpath, exist_ok=True)
    conn = sqlite3.connect(db_filepath)
    cur = conn.cursor()
    if regen:
        cur.execute(f"DROP TABLE IF EXISTS {table_name}")
    cur.execute(f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            plant_name_common_id INTEGER PRIMARY KEY,
            plant_name_common_reference TEXT NOT NULL UNIQUE,
            plant_name_common_reference_normalize TEXT NOT NULL UNIQUE,
            plant_name_common_transliteration TEXT,
            plant_name_common_language TEXT,
            plant_name_common_preferred TEXT,
            plant_name_common_country TEXT,
            plant_name_common_area TEXT
        );
    """)
    conn.execute("PRAGMA journal_mode = WAL;")
    conn.execute("PRAGMA synchronous = OFF;")
    conn.execute("PRAGMA temp_store = MEMORY;")
    ###
    cur.execute(f"CREATE INDEX IF NOT EXISTS idx_{table_name}_plant_name_common_reference ON {table_name}(plant_name_common_reference)")
    cur.execute(f"CREATE INDEX IF NOT EXISTS idx_{table_name}_plant_name_common_reference_normalize ON {table_name}(plant_name_common_reference_normalize)")
    cur.execute(f"CREATE INDEX IF NOT EXISTS idx_{table_name}_plant_name_common_language ON {table_name}(plant_name_common_language)")
    conn.commit()
    conn.close()
    """
    TABLE RECORD EXAMPLE:
    ********************************************************************************
    {
        "plant_name_common_id": 1,
        "plant_name_common_reference": "Ozua",
        "plant_name_common_reference_normalize": "ozua",
        "plant_name_common_transliteration": "Ozua",
        "plant_name_common_language": "spa",
        "plant_name_common_preferred": "",
        "plant_name_common_country": "DO",
        "plant_name_common_area": "Dominican Republic"
    }
    """
 
def master_table_chemicals_create(regen=False):
    table_name = 'chemicals'
    output_folderpath = f'{HUB_FOLDERPATH}/masterize'
    db_filepath = f'{output_folderpath}/master.db'
    ###
    conn = sqlite3.connect(db_filepath)
    cur = conn.cursor()
    if regen:
        cur.execute(f"DROP TABLE IF EXISTS {table_name}")
    cur.execute(f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            id INTEGER PRIMARY KEY,
            chemical_name_reference TEXT NOT NULL UNIQUE,
            chemical_name_reference_normalize TEXT NOT NULL UNIQUE
        );
    """)
    conn.execute("PRAGMA journal_mode = WAL;")
    conn.execute("PRAGMA synchronous = OFF;")
    conn.execute("PRAGMA temp_store = MEMORY;")
    cur.execute(f"CREATE INDEX IF NOT EXISTS idx_{table_name}_chemical_name_reference ON {table_name}(chemical_name_reference)")
    cur.execute(f"CREATE INDEX IF NOT EXISTS idx_{table_name}_chemical_name_reference_normalize ON {table_name}(chemical_name_reference_normalize)")
    conn.commit()
    conn.close()

def master_table_plants_parts_create(regen=False):
    table_name = 'plants_parts'
    output_folderpath = f'{HUB_FOLDERPATH}/masterize'
    db_filepath = f'{output_folderpath}/master.db'
    ###
    conn = sqlite3.connect(db_filepath)
    cur = conn.cursor()
    if regen:
        cur.execute(f"DROP TABLE IF EXISTS {table_name}")
    cur.execute(f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            id INTEGER PRIMARY KEY,
            plant_part_name_reference TEXT NOT NULL UNIQUE,
            plant_part_name_reference_normalize TEXT NOT NULL UNIQUE
        );
    """)
    conn.execute("PRAGMA journal_mode = WAL;")
    conn.execute("PRAGMA synchronous = OFF;")
    conn.execute("PRAGMA temp_store = MEMORY;")
    ###
    cur.execute(f"CREATE INDEX IF NOT EXISTS idx_{table_name}_plant_part_name_reference ON {table_name}(plant_part_name_reference)")
    cur.execute(f"CREATE INDEX IF NOT EXISTS idx_{table_name}_plant_part_name_reference_normalize ON {table_name}(plant_part_name_reference_normalize)")
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

    # master_table_studies_create(regen=True)

    # master_table_plants_names_common_create(regen=True)

    # master_table_plants_create(regen=True)
    # master_table_activities_create(regen=True)
    # master_table_conditions_create(regen=True)
    master_table_compounds_create(regen=True)



    # master_table_diseases_create(regen=True)
    # test()



    # master_table_chemicals_create(regen=True)
    # master_table_plants_parts_create(regen=True)

    pass
