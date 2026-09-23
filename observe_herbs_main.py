import os
import time
import json
import shutil
import sqlite3

from lib import g
from lib import io
from lib import llm

HUB_FOLDERPATH = f'''{g.DATA_FOLDERPATH}/herbs'''
output_folderpath = f'{HUB_FOLDERPATH}/observe'
db_filepath = f'{output_folderpath}/observations.db'

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
    input_folderpath = f'{HUB_FOLDERPATH}/resolve/{source_foldername}/names/json'
    output_folderpath = f'{HUB_FOLDERPATH}/observe'
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
                plant_name_scientific_reference,
                plant_name_scientific_reference_normalize,
                plant_name_common,
                plant_name_common_transliteration,
                plant_name_common_language,
                plant_name_common_preferred,
                plant_name_common_country,
                plant_name_common_area,
                plant_name_common_type,
                source_name,
                source_acronym
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        [
            (
                item.get("plant_name_scientific_reference"),
                item.get("plant_name_scientific_reference_normalize"),
                item.get("plant_name_common"),
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

def observations_table_plants_distributions_add(source_foldername):
    table_name = 'plants_distributions'
    input_folderpath = f'{HUB_FOLDERPATH}/resolve/{source_foldername}/distributions/json'
    output_folderpath = f'{HUB_FOLDERPATH}/observe'
    db_filepath = f'{output_folderpath}/observations.db'
    ###
    input_filenames = os.listdir(input_folderpath)
    all_data = []
    for i, input_filename in enumerate(input_filenames[:]):
        print(f'PLANTS_DISTRIBUTIONS - {i}/{len(input_filenames)}')
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
                plant_name_scientific_reference,
                plant_name_scientific_reference_normalize,
                locality_continent_code,
                locality_continent,
                locality_region_code,
                locality_region,
                locality_area_code,
                locality_area,
                locality_introduced,
                locality_extinct,
                locality_doubtful,
                locality_continent_normalize,
                locality_region_normalize,
                locality_area_normalize,
                source_name,
                source_acronym
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        [
            (
                item.get('plant_name_scientific_reference'),
                item.get('plant_name_scientific_reference_normalize'),
                item.get('locality_continent_code'),
                item.get('locality_continent'),
                item.get('locality_region_code'),
                item.get('locality_region'),
                item.get('locality_area_code'),
                item.get('locality_area'),
                item.get('locality_introduced'),
                item.get('locality_extinct'),
                item.get('locality_doubtful'),
                item.get('locality_continent_normalize'),
                item.get('locality_region_normalize'),
                item.get('locality_area_normalize'),
                item.get('source_name'),
                item.get('source_acronym')
            )
            for item in all_data
        ]
    )
    conn.commit()
    rows = conn.execute(f"SELECT * FROM {table_name}")
    for row in list(rows)[:10]:
        print(row)
    conn.close()

def observations_table_plants_traits_add(source_foldername):
    table_name = 'plants_traits'
    input_folderpath = f'{HUB_FOLDERPATH}/resolve/{source_foldername}/traits/json'
    output_folderpath = f'{HUB_FOLDERPATH}/observe'
    db_filepath = f'{output_folderpath}/observations.db'
    ###
    input_filenames = os.listdir(input_folderpath)
    all_data = []
    for i, input_filename in enumerate(input_filenames[:]):
        print(f'PLANTS_TRAITS - {i}/{len(input_filenames)}')
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
                plant_name_scientific_reference,
                plant_name_scientific_reference_normalize,
                trait_category,
                trait_1,
                trait_2,
                trait_units,
                trait_type,
                trait_value,
                trait_agreement,
                trait_coeff_var,
                trait_n,
                trait_refs,
                source_name,
                source_acronym
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        [
            (
                item.get("wcvp_name_taxon"),
                item.get("wcvp_name_taxon_norm"),
                item.get("trait_category"),
                item.get("trait_1"),
                item.get("trait_2"),
                item.get("trait_units"),
                item.get("trait_type"),
                item.get("trait_value"),
                item.get("trait_agreement"),
                item.get("trait_coeff_var"),
                item.get("trait_n"),
                item.get("trait_refs"),
                item.get("source_name"),
                item.get("source_acrony"),
            )
            for item in all_data
        ]
    )
    conn.commit()
    rows = conn.execute(f'SELECT * FROM {table_name}')
    for row in list(rows)[:10]:
        print(row)
    conn.close()

def observations_table_plants_plants_parts_add(source_foldername):
    table_name = 'plants_plants_parts'
    input_folderpath = f'{HUB_FOLDERPATH}/resolve/{source_foldername}/plants_parts/json'
    output_folderpath = f'{HUB_FOLDERPATH}/observe'
    db_filepath = f'{output_folderpath}/observations.db'
    ###
    input_filenames = os.listdir(input_folderpath)
    all_data = []
    for i, input_filename in enumerate(input_filenames[:]):
        print(f'PLANTS_PARTS - {i}/{len(input_filenames)}')
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
                plant_name_scientific_reference, 
                plant_name_scientific_reference_normalize, 
                plant_part_name_reference, 
                plant_part_name_reference_normalize, 
                source_name,
                source_acronym,
                reference_name
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        [
            (
                item.get("plant_name_scientific_reference"),
                item.get("plant_name_scientific_reference_normalize"),
                item.get("plant_part_name_reference"),
                item.get("plant_part_name_reference_normalize"),
                item.get("source_name"),
                item.get("source_acronym"),
                item.get("reference_name"),
            )
            for item in all_data
        ]
    )
    conn.commit()
    rows = conn.execute(f'SELECT * FROM {table_name}')
    for row in list(rows)[:10]:
        print(row)
    conn.close()

def observations_table_plants_preparations_add(source_foldername):
    table_name = 'plants_preparations'
    input_folderpath = f'{HUB_FOLDERPATH}/resolve/{source_foldername}/preparations/json'
    output_folderpath = f'{HUB_FOLDERPATH}/observe'
    db_filepath = f'{output_folderpath}/observations.db'
    ###
    input_filenames = os.listdir(input_folderpath)
    all_data = []
    for i, input_filename in enumerate(input_filenames[:]):
        print(f'PLANTS_PREPARATIONS - {i}/{len(input_filenames)}')
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
                plant_name_scientific_reference, 
                plant_name_scientific_reference_normalize, 
                preparation_name_reference, 
                preparation_name_reference_normalize, 
                source_name,
                source_acronym,
                reference_name
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        [
            (
                item.get("plant_name_scientific_reference"),
                item.get("plant_name_scientific_reference_normalize"),
                item.get("preparation_name_reference"),
                item.get("preparation_name_reference_normalize"),
                item.get("source_name"),
                item.get("source_acronym"),
                item.get("reference_name"),
            )
            for item in all_data
        ]
    )
    conn.commit()
    rows = conn.execute(f'SELECT * FROM {table_name}')
    for row in list(rows)[:10]:
        print(row)
    conn.close()

def observations_table_plants_activities_add(source_foldername):
    table_name = 'plants_activities'
    input_folderpath = f'{HUB_FOLDERPATH}/resolve/{source_foldername}/activities/json'
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
                plant_name_scientific_reference, 
                plant_name_scientific_reference_normalize, 
                activity_name_reference, 
                activity_name_reference_normalize, 
                source_name,
                source_acronym
            )
            VALUES (?, ?, ?, ?, ?, ?)
        """,
        [
            (
                item.get("plant_name_scientific_reference"),
                item.get("plant_name_scientific_reference_normalize"),
                item.get("activity_name_reference"),
                item.get("activity_name_reference_normalize"),
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

def observations_table_plants_chemicals_add(source_foldername):
    table_name = 'plants_chemicals'
    input_folderpath = f'{HUB_FOLDERPATH}/resolve/{source_foldername}/chemicals/json'
    output_folderpath = f'{HUB_FOLDERPATH}/observe'
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
                plant_name_scientific_reference,
                plant_name_scientific_reference_normalize,
                chemical_name_reference,
                chemical_name_reference_normalize,
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
                item.get("plant_name_scientific_reference"),
                item.get("plant_name_scientific_reference_normalize"),
                item.get("chemical_name_reference"),
                item.get("chemical_name_reference_normalize"),
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

def observations_table_plants_conditions_add(source_foldername):
    table_name = 'plants_conditions'
    input_folderpath = f'{HUB_FOLDERPATH}/resolve/{source_foldername}/conditions/json'
    output_folderpath = f'{HUB_FOLDERPATH}/observe'
    db_filepath = f'{output_folderpath}/observations.db'
    ###
    input_filenames = os.listdir(input_folderpath)
    all_data = []
    for i, input_filename in enumerate(input_filenames[:]):
        print(f'PLANTS CONDITIONS - {i}/{len(input_filenames)}')
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
                plant_name_scientific_reference,
                plant_name_scientific_reference_normalize,
                condition_name_reference,
                condition_name_reference_normalize,
                source_name,
                source_acronym
            )
            VALUES (?, ?, ?, ?, ?, ?)
        """,
        [
            (
                item.get("plant_name_scientific_reference"),
                item.get("plant_name_scientific_reference_normalize"),
                item.get("condition_name_reference"),
                item.get("condition_name_reference_normalize"),
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
        observations_table_plants_synonyms_add(source_foldername='wcvp')


    if 1:
        observations_table_plants_traits_add(source_foldername='gift')

    if 1:
        observations_table_plants_distributions_add(source_foldername='wcvp')

    if 1:
        # observations_table_plants_names_common_add(source_foldername='wikidata')
        observations_table_plants_names_common_add(source_foldername='col')

    if 1:
        # observations_table_plants_activities_add(source_foldername='drduke')
        observations_table_plants_activities_add(source_foldername='pubmed')

    if 1:
        # observations_table_plants_chemicals_add(source_foldername='drduke')
        observations_table_plants_chemicals_add(source_foldername='pubmed')

    if 1:
        observations_table_plants_conditions_add(source_foldername='pubmed')

    if 1:
        observations_table_plants_plants_parts_add(source_foldername='pubmed')

    if 1:
        observations_table_plants_preparations_add(source_foldername='pubmed')

