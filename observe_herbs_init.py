import os
import time
import json
import shutil
import sqlite3

from lib import g
from lib import io

HUB_FOLDERPATH = f'''{g.DATA_FOLDERPATH}/herbs'''
output_folderpath = f'{HUB_FOLDERPATH}/observe'
db_filepath = f'{output_folderpath}/observations.db'

import schema_herbs

def observations_table_plants_taxonomies_create(regen=False):
    table_name = 'plants_taxonomies'
    conn = sqlite3.connect(db_filepath)
    cur = conn.cursor()
    if regen: cur.execute(f"DROP TABLE IF EXISTS {table_name}")
    cur.execute(f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            id INTEGER PRIMARY KEY,
            plant_name_scientific_reference TEXT NOT NULL,
            plant_name_scientific_reference_normalize TEXT NOT NULL,
            taxon_kingdom TEXT,
            taxon_phylum TEXT,
            taxon_class TEXT,
            taxon_subclass TEXT,
            taxon_order TEXT,
            taxon_family TEXT,
            taxon_genus TEXT,
            source_name TEXT,
            source_acronym TEXT
        );
    """)
    conn.execute("PRAGMA journal_mode = WAL;")
    conn.execute("PRAGMA synchronous = OFF;")
    conn.execute("PRAGMA temp_store = MEMORY;")
    cur.execute(f"CREATE INDEX IF NOT EXISTS idx_{table_name}_plant_name_scientific_reference ON {table_name}(plant_name_scientific_reference)")
    conn.commit()
    conn.close()

def observations_table_plants_synonyms_create(regen=False):
    table_name = 'plants_synonyms'
    conn = sqlite3.connect(db_filepath)
    cur = conn.cursor()
    if regen: cur.execute(f"DROP TABLE IF EXISTS {table_name}")
    cur.execute(f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            id INTEGER PRIMARY KEY,
            plant_name_scientific_reference TEXT NOT NULL,
            plant_synonym_reference TEXT NOT NULL,
            source_name TEXT
        );
    """)
    conn.execute("PRAGMA journal_mode = WAL;")
    conn.execute("PRAGMA synchronous = OFF;")
    conn.execute("PRAGMA temp_store = MEMORY;")
    cur.execute(f"CREATE INDEX IF NOT EXISTS idx_{table_name}_plant_name_scientific_reference ON {table_name}(plant_name_scientific_reference)")
    conn.commit()
    conn.close()

def observations_table_plants_names_common_create(regen=False):
    table_name = 'plants_names_common'
    conn = sqlite3.connect(db_filepath)
    cur = conn.cursor()
    if regen: cur.execute(f"DROP TABLE IF EXISTS {table_name}")
    cur.execute(f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            id INTEGER PRIMARY KEY,
            plant_name_scientific_reference TEXT NOT NULL,
            plant_name_scientific_reference_normalize TEXT NOT NULL,
            plant_name_common TEXT NOT NULL,
            plant_name_common_transliteration TEXT,
            plant_name_common_language TEXT,
            plant_name_common_preferred TEXT,
            plant_name_common_country TEXT,
            plant_name_common_area TEXT,
            plant_name_common_type TEXT,
            source_name TEXT NOT NULL,
            source_acronym TEXT
        );
    """)
    conn.execute("PRAGMA journal_mode = WAL;")
    conn.execute("PRAGMA synchronous = OFF;")
    conn.execute("PRAGMA temp_store = MEMORY;")
    cur.execute(f"CREATE INDEX IF NOT EXISTS idx_{table_name}_plant_name_scientific_reference ON {table_name}(plant_name_scientific_reference)")
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
            plant_name_scientific_reference TEXT NOT NULL,
            plant_name_scientific_reference_normalize TEXT NOT NULL,
            locality_continent_code TEXT NOT NULL,
            locality_continent TEXT NOT NULL,
            locality_region_code TEXT NOT NULL,
            locality_region TEXT NOT NULL,
            locality_area_code TEXT NOT NULL,
            locality_area TEXT NOT NULL,
            locality_introduced TEXT NOT NULL,
            locality_extinct TEXT NOT NULL,
            locality_doubtful TEXT NOT NULL,
            locality_continent_normalize TEXT NOT NULL,
            locality_region_normalize TEXT NOT NULL,
            locality_area_normalize TEXT NOT NULL,
            source_name TEXT NOT NULL,
            source_acronym TEXT
        );
    """)
    conn.execute("PRAGMA journal_mode = WAL;")
    conn.execute("PRAGMA synchronous = OFF;")
    conn.execute("PRAGMA temp_store = MEMORY;")
    cur.execute(f"CREATE INDEX IF NOT EXISTS idx_{table_name}_plant_name_scientific_reference ON {table_name}(plant_name_scientific_reference)")
    conn.commit()
    conn.close()

def observations_table_plants_traits_create(regen=False):
    table_name = 'plants_traits'
    conn = sqlite3.connect(db_filepath)
    cur = conn.cursor()
    if regen: cur.execute(f"DROP TABLE IF EXISTS {table_name}")
    cur.execute(f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            id INTEGER PRIMARY KEY,
            plant_name_scientific_reference TEXT NOT NULL,
            plant_name_scientific_reference_normalize TEXT NOT NULL,
            trait_category TEXT NOT NULL,
            trait_1 TEXT NOT NULL,
            trait_2 TEXT NOT NULL,
            trait_units TEXT NOT NULL,
            trait_type TEXT NOT NULL,
            trait_value TEXT NOT NULL,
            trait_agreement TEXT,
            trait_coeff_var TEXT,
            trait_n TEXT,
            trait_refs TEXT,
            source_name TEXT NOT NULL,
            source_acronym TEXT
        );
    """)
    conn.execute("PRAGMA journal_mode = WAL;")
    conn.execute("PRAGMA synchronous = OFF;")
    conn.execute("PRAGMA temp_store = MEMORY;")
    cur.execute(f"CREATE INDEX IF NOT EXISTS idx_{table_name}_plant_name_scientific_reference ON {table_name}(plant_name_scientific_reference)")
    cur.execute(f"CREATE INDEX IF NOT EXISTS idx_{table_name}_source_name ON {table_name}(source_name)")
    conn.commit()
    conn.close()

def observations_table_plants_plants_parts_create(regen=False):
    table_name = 'plants_plants_parts'
    conn = sqlite3.connect(db_filepath)
    cur = conn.cursor()
    if regen: cur.execute(f"DROP TABLE IF EXISTS {table_name}")
    cur.execute(f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            id INTEGER PRIMARY KEY,
            plant_name_scientific_reference TEXT NOT NULL,
            plant_name_scientific_reference_normalize TEXT,
            plant_part_name_reference TEXT NOT NULL,
            plant_part_name_reference_normalize TEXT,
            source_name TEXT NOT NULL,
            source_acronym TEXT,
            reference_id TEXT,
            reference_name TEXT
        );
    """)
    conn.execute("PRAGMA journal_mode = WAL;")
    conn.execute("PRAGMA synchronous = OFF;")
    conn.execute("PRAGMA temp_store = MEMORY;")
    cur.execute(f"CREATE INDEX IF NOT EXISTS idx_{table_name}_plant_name_scientific_reference ON {table_name}(plant_name_scientific_reference)")
    cur.execute(f"CREATE INDEX IF NOT EXISTS idx_{table_name}_plant_part_name_reference ON {table_name}(plant_part_name_reference)")
    conn.commit()
    conn.close()

def observations_table_plants_compounds_create(regen=False):
    table_name = 'plants_compounds'
    conn = sqlite3.connect(db_filepath)
    cur = conn.cursor()
    if regen: cur.execute(f"DROP TABLE IF EXISTS {table_name}")
    cur.execute(f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            id INTEGER PRIMARY KEY,
            plant_name_scientific_reference TEXT NOT NULL,
            plant_name_scientific_reference_normalize TEXT,
            compound_name_reference TEXT NOT NULL,
            compound_name_reference_normalize TEXT,
            plant_part_name_raw TEXT,
            concentration REAL,
            unit TEXT,
            source_name TEXT NOT NULL,
            source_acronym TEXT,
            reference_id TEXT,
            reference_name TEXT
        );
    """)
    conn.execute("PRAGMA journal_mode = WAL;")
    conn.execute("PRAGMA synchronous = OFF;")
    conn.execute("PRAGMA temp_store = MEMORY;")
    ###
    cur.execute(f"CREATE INDEX IF NOT EXISTS idx_{table_name}_plant_name_scientific_reference ON {table_name}(plant_name_scientific_reference)")
    cur.execute(f"CREATE INDEX IF NOT EXISTS idx_{table_name}_compound_name_reference ON {table_name}(compound_name_reference)")
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
            plant_name_scientific_reference TEXT NOT NULL,
            plant_name_scientific_reference_normalize TEXT,
            chemical_name_reference TEXT NOT NULL,
            chemical_name_reference_normalize TEXT,
            plant_part_name_raw TEXT,
            concentration REAL,
            unit TEXT,
            source_name TEXT NOT NULL,
            source_acronym TEXT,
            reference_id TEXT,
            reference_name TEXT
        );
    """)
    conn.execute("PRAGMA journal_mode = WAL;")
    conn.execute("PRAGMA synchronous = OFF;")
    conn.execute("PRAGMA temp_store = MEMORY;")
    ###
    cur.execute(f"CREATE INDEX IF NOT EXISTS idx_{table_name}_plant_name_scientific_reference ON {table_name}(plant_name_scientific_reference)")
    cur.execute(f"CREATE INDEX IF NOT EXISTS idx_{table_name}_chemical_name_reference ON {table_name}(chemical_name_reference)")
    cur.execute(f"CREATE INDEX IF NOT EXISTS idx_{table_name}_source_name ON {table_name}(source_name)")
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
            plant_name_scientific_reference TEXT NOT NULL,
            plant_name_scientific_reference_normalize TEXT,
            activity_name_reference TEXT NOT NULL,
            activity_name_reference_normalize TEXT,
            source_name TEXT NOT NULL,
            source_acronym TEXT,
            reference_id TEXT,
            reference_name TEXT
        );
    """)
    conn.execute("PRAGMA journal_mode = WAL;")
    conn.execute("PRAGMA synchronous = OFF;")
    conn.execute("PRAGMA temp_store = MEMORY;")
    cur.execute(f"CREATE INDEX IF NOT EXISTS idx_{table_name}_plant_name_scientific_reference ON {table_name}(plant_name_scientific_reference)")
    cur.execute(f"CREATE INDEX IF NOT EXISTS idx_{table_name}_activity_name_reference ON {table_name}(activity_name_reference)")
    conn.commit()
    conn.close()

def observations_table_plants_conditions_create(regen=False):
    table_name = 'plants_conditions'
    conn = sqlite3.connect(db_filepath)
    cur = conn.cursor()
    if regen: cur.execute(f"DROP TABLE IF EXISTS {table_name}")
    cur.execute(f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            id INTEGER PRIMARY KEY,
            plant_name_scientific_reference TEXT NOT NULL,
            plant_name_scientific_reference_normalize TEXT NOT NULL,
            condition_name_reference TEXT NOT NULL,
            condition_name_reference_normalize TEXT NOT NULL,
            source_name TEXT NOT NULL,
            source_acronym TEXT,
            reference_id TEXT,
            reference_name TEXT
        );
    """)
    conn.execute("PRAGMA journal_mode = WAL;")
    conn.execute("PRAGMA synchronous = OFF;")
    conn.execute("PRAGMA temp_store = MEMORY;")
    cur.execute(f"CREATE INDEX IF NOT EXISTS idx_{table_name}_plant_name_scientific_reference ON {table_name}(plant_name_scientific_reference)")
    cur.execute(f"CREATE INDEX IF NOT EXISTS idx_{table_name}_condition_name_reference ON {table_name}(condition_name_reference)")
    conn.commit()
    conn.close()

def observations_table_plants_preparations_create(regen=False):
    table_name = 'plants_preparations'
    conn = sqlite3.connect(db_filepath)
    cur = conn.cursor()
    if regen: cur.execute(f"DROP TABLE IF EXISTS {table_name}")
    cur.execute(f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            id INTEGER PRIMARY KEY,
            plant_name_scientific_reference TEXT NOT NULL,
            plant_name_scientific_reference_normalize TEXT NOT NULL,
            preparation_name_reference TEXT NOT NULL,
            preparation_name_reference_normalize TEXT NOT NULL,
            source_name TEXT NOT NULL,
            source_acronym TEXT,
            reference_id TEXT,
            reference_name TEXT
        );
    """)
    conn.execute("PRAGMA journal_mode = WAL;")
    conn.execute("PRAGMA synchronous = OFF;")
    conn.execute("PRAGMA temp_store = MEMORY;")
    cur.execute(f"CREATE INDEX IF NOT EXISTS idx_{table_name}_plant_name_scientific_reference ON {table_name}(plant_name_scientific_reference)")
    cur.execute(f"CREATE INDEX IF NOT EXISTS idx_{table_name}_preparation_name_reference ON {table_name}(preparation_name_reference)")
    conn.commit()
    conn.close()

def schema_observe_create(schema_item):
    schema_table_name = schema_item['table_name']
    schema_source_name = schema_item['sources'][0]['source_name']
    schema_output_foldername = schema_table_name
    schema_entity_1_val = schema_item['fields'][0]['field_name']
    schema_relationship_val = schema_item['fields'][1]['field_name']
    schema_entity_2_val = schema_item['fields'][2]['field_name']
    ###
    conn = sqlite3.connect(db_filepath)
    cur = conn.cursor()
    # if regen: cur.execute(f"DROP TABLE IF EXISTS {schema_table_name}")
    cur.execute(f"DROP TABLE IF EXISTS {schema_table_name}")
    sql_query = f'''
        CREATE TABLE IF NOT EXISTS {schema_table_name} (
            id INTEGER PRIMARY KEY,
            {schema_entity_1_val}_reference TEXT NOT NULL,
            {schema_entity_1_val}_reference_normalize TEXT,
            {schema_entity_2_val}_reference TEXT NOT NULL,
            {schema_entity_2_val}_reference_normalize TEXT,
            {schema_relationship_val}_raw TEXT,
            source_name TEXT NOT NULL,
            source_acronym TEXT,
            reference_id TEXT,
            reference_name TEXT
        );
    '''
    # print(sql_query)
    # quit()
    cur.execute(sql_query)
    conn.execute("PRAGMA journal_mode = WAL;")
    conn.execute("PRAGMA synchronous = OFF;")
    conn.execute("PRAGMA temp_store = MEMORY;")
    ###
    cur.execute(f"CREATE INDEX IF NOT EXISTS idx_{schema_table_name}_{schema_entity_1_val}_reference ON {schema_table_name}({schema_entity_1_val}_reference)")
    cur.execute(f"CREATE INDEX IF NOT EXISTS idx_{schema_table_name}_{schema_entity_2_val}_reference ON {schema_table_name}({schema_entity_2_val}_reference)")
    conn.commit()
    ###
    # cols = conn.execute(f'PRAGMA table_info({schema_table_name})').fetchall()
    # print([c[1] for c in cols])
    ###
    # quit()
    conn.close()

def run():
    print('OBSERVE >> init')

    # try: shutil.rmtree(output_folderpath)
    # except: pass
    os.makedirs(output_folderpath, exist_ok=True)

    schema_items = schema_herbs.data['items']
    for schema_item in schema_items: 
        schema_observe_create(schema_item)

    if 0:
        # observations_table_plants_compounds_create(regen=True)
        # observations_table_plants_preparations_create(regen=True)
        observations_table_plants_plants_parts_create(regen=True)
        observations_table_plants_conditions_create(regen=True)
        # observations_table_plants_chemicals_create(regen=True)
        observations_table_plants_activities_create(regen=True)

        # observations_table_plants_names_create(regen=True)
        observations_table_plants_names_common_create(regen=True)

        observations_table_plants_taxonomies_create(regen=True)

        observations_table_plants_synonyms_create(regen=True)
        observations_table_plants_traits_create(regen=True)

        observations_table_plants_distributions_create(regen=True)

