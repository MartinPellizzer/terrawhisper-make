
import os
import time
import json
import shutil
import sqlite3

from lib import g
from lib import io
from lib import llm

def observations_table_plants_synonyms_add(source_foldername):
    table_name = 'plants_synonyms'
    input_folderpath = f'{g.DATA_FOLDERPATH}/resolve/{source_foldername}/synonyms/json'
    output_folderpath = f'{g.DATA_FOLDERPATH}/observe'
    db_filepath = f'{output_folderpath}/observations.db'
    ###
    input_filenames = os.listdir(input_folderpath)
    all_data = []
    for i, input_filename in enumerate(input_filenames[:]):
        print(f'PLANTS_SYNONYMS - {i}/{len(input_filenames)}')
        input_filepath = f'{input_folderpath}/{input_filename}'
        input_data = io.json_read(input_filepath)
        for input_item in input_data:
            all_data.append(input_item)
            # print(json.dumps(input_item, indent=4))
            # quit()
    ###
    conn = sqlite3.connect(db_filepath)
    cur = conn.cursor()
    cur.executemany(
        f"""
            INSERT OR IGNORE INTO {table_name} (
                plant_canonical_name, 
                plant_synonym, 
                source_name
            )
            VALUES (?, ?, ?)
        """,
        [
            (
                item.get("wcvp_taxon_name"),
                item.get("plant_synonym_raw"),
                item.get("source_name"),
            )
            for item in all_data
        ]
    )
    conn.commit()
    rows = conn.execute(f"SELECT * FROM {table_name}")
    for row in list(rows)[:10]:
        print(row)
    conn.close()

def observations_table_plants_names_common_add(source_foldername):
    table_name = 'plants_names_common'
    input_folderpath = f'{g.DATA_FOLDERPATH}/resolve/{source_foldername}/names/json'
    output_folderpath = f'{g.DATA_FOLDERPATH}/observe'
    db_filepath = f'{output_folderpath}/observations.db'
    ###
    input_filenames = os.listdir(input_folderpath)
    all_data = []
    for i, input_filename in enumerate(input_filenames[:]):
        print(f'PLANTS_NAMES_COMMON - {i}/{len(input_filenames)}')
        input_filepath = f'{input_folderpath}/{input_filename}'
        input_data = io.json_read(input_filepath)
        for input_item in input_data:
            all_data.append(input_item)
            # print(json.dumps(input_item, indent=4))
            # quit()
    # print(json.dumps(all_data[0], indent=4))
    # quit()
    ###
    conn = sqlite3.connect(db_filepath)
    cur = conn.cursor()
    cur.executemany(
        f"""
            INSERT OR IGNORE INTO {table_name} (
                plant_name_scientific_canon,
                plant_name_scientific_canon_norm,
                plant_name_scientific_raw,
                plant_name_scientific_raw_norm,
                plant_name_common_raw,
                plant_name_common_transliteration,
                plant_name_common_language,
                plant_name_common_preferred,
                plant_name_common_country,
                plant_name_common_area,
                plant_name_common_type,
                source_name,
                source_acronym
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        [
            (
                item.get("wcvp_name_taxon"),
                item.get("wcvp_name_taxon_norm"),
                item.get("plant_name_scientific_raw"),
                item.get("plant_name_scientific_raw_norm"),
                item.get("plant_name_common_raw"),
                item.get("plant_name_common_transliteration"),
                item.get("plant_name_common_language"),
                item.get("plant_name_common_preferred"),
                item.get("plant_name_common_country"),
                item.get("plant_name_common_area"),
                item.get("plant_name_common_type"),
                item.get("source_name"),
                item.get("source_acronym"),
            )
            for item in all_data
        ]
    )
    conn.commit()
    rows = conn.execute(f"SELECT * FROM {table_name}")
    for row in list(rows)[:10]:
        print(row)
    conn.close()

def observations_table_plants_activities_add(source_foldername):
    table_name = 'plants_activities'
    input_folderpath = f'{g.DATA_FOLDERPATH}/resolve/{source_foldername}/activities/json'
    output_folderpath = f'{g.DATA_FOLDERPATH}/observe'
    db_filepath = f'{output_folderpath}/observations.db'
    ###
    input_filenames = os.listdir(input_folderpath)
    all_data = []
    for i, input_filename in enumerate(input_filenames[:]):
        print(f'PLANTS_ACTIVITIES - {i}/{len(input_filenames)}')
        input_filepath = f'{input_folderpath}/{input_filename}'
        input_data = io.json_read(input_filepath)
        for input_item in input_data:
            all_data.append(input_item)
            # print(json.dumps(input_item, indent=4))
            # quit()
            
    ###
    conn = sqlite3.connect(db_filepath)
    cur = conn.cursor()
    cur.executemany(
        f"""
            INSERT OR IGNORE INTO {table_name} (
                plant_name_scientific_canon, 
                plant_name_scientific_canon_norm, 
                activity_name_canon, 
                activity_name_canon_norm, 
                source_name,
                source_acronym,
                reference_name
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        [
            (
                item.get("plant_name_scientific_canon"),
                item.get("plant_name_scientific_canon_norm"),
                item.get("activity_name_canon"),
                item.get("activity_name_canon_norm"),
                item.get("source_name"),
                item.get("source_acronym"),
                item.get("reference_name"),
            )
            for item in all_data
        ]
    )
    conn.commit()
    rows = conn.execute(f"SELECT * FROM {table_name}")
    for row in list(rows)[:10]:
        print(row)
    conn.close()

def observations_table_plants_chemicals_add(source_foldername):
    table_name = 'plants_chemicals'
    input_folderpath = f'{g.DATA_FOLDERPATH}/resolve/{source_foldername}/chemicals/json'
    output_folderpath = f'{g.DATA_FOLDERPATH}/observe'
    db_filepath = f'{output_folderpath}/observations.db'
    ###
    input_filenames = os.listdir(input_folderpath)
    all_data = []
    for i, input_filename in enumerate(input_filenames[:]):
        print(f'PLANTS_CHEMICALS - {i}/{len(input_filenames)}')
        input_filepath = f'{input_folderpath}/{input_filename}'
        input_data = io.json_read(input_filepath)
        for input_item in input_data:
            all_data.append(input_item)
            # print(json.dumps(input_item, indent=4))
            # quit()
    ###
    conn = sqlite3.connect(db_filepath)
    cur = conn.cursor()
    cur.executemany(
        f"""
            INSERT OR IGNORE INTO {table_name} (
                plant_name_scientific_canon,
                plant_name_scientific_canon_norm,
                chemical_name_canon,
                chemical_name_canon_norm,
                plant_part_name_raw,
                concentration,
                unit,
                source_name,
                source_acronym,
                reference_name
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        [
            (
                item.get("plant_name_scientific_canon"),
                item.get("plant_name_scientific_canon_norm"),
                item.get("chemical_name_canon"),
                item.get("chemical_name_canon_norm"),
                item.get("plant_part_name_raw"),
                item.get("concentration"),
                item.get("unit"),
                item.get("source_name"),
                item.get("source_acronym"),
                item.get("reference_nam"),
            )
            for item in all_data
        ]
    )
    conn.commit()
    rows = conn.execute(f"SELECT * FROM {table_name}")
    for row in list(rows)[:10]:
        print(row)
    conn.close()

def test():
    output_folderpath = f'{g.VAULT_FOLDERPATH}/terrawhisper/data/observe'
    db_filepath = f'{output_folderpath}/observations.db'
    conn = sqlite3.connect(db_filepath)
    rows = conn.execute("SELECT * FROM plants_chemicals")
    for row in list(rows)[:10]:
        print(row)
    conn.close()

def run():
    print('OBSERVE')

    if 0:
        observations_table_plants_names_common_add(source_foldername='wikidata')
        observations_table_plants_names_common_add(source_foldername='col')

    if 0:
        observations_table_plants_synonyms_add(source_foldername='wcvp')

    if 1:
        observations_table_plants_activities_add(source_foldername='drduke')
        observations_table_plants_activities_add(source_foldername='pubmed')

    if 1:
        observations_table_plants_chemicals_add(source_foldername='drduke')
        observations_table_plants_chemicals_add(source_foldername='pubmed')
    # test()



