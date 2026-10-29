import os
import time
import json
import shutil
import sqlite3

from lib import g
from lib import io
from lib import llm

HUB_FOLDERPATH = f'''{g.DATA_FOLDERPATH}/herbs'''

def masterize_table_studies_add(source_foldername):
    table_name = 'studies'
    input_folderpath = f'{HUB_FOLDERPATH}/resolve/{source_foldername}/{table_name}/json'
    output_folderpath = f'{HUB_FOLDERPATH}/database'
    db_filepath = f'{output_folderpath}/terra.db'
    ###
    input_filenames = os.listdir(input_folderpath)
    all_data = []
    for i, input_filename in enumerate(input_filenames[:]):
        print(f'STUDIES - {i}/{len(input_filenames)}')
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
                study_pmid, 
                study_title
            )
            VALUES (?, ?)
        """,
        [
            (
                item.get("study_pmid"),
                item.get("study_title_raw"),
            )
            for item in all_data
        ]
    )
    conn.commit()
    conn.row_factory = sqlite3.Row
    cursor = conn.execute(f'''
        SELECT * 
        FROM {table_name}
    ''')
    rows = cursor.fetchall()
    items = [dict(row) for row in rows]
    for item in items[:10]:
        print(json.dumps(item, indent=4))
    print(len(items))
    conn.close()

def masterize_table_plants_add(source_foldername, subfoldername):
    table_name = 'plants'
    input_folderpath = f'{HUB_FOLDERPATH}/resolve/{source_foldername}/{subfoldername}/json'
    output_folderpath = f'{HUB_FOLDERPATH}/database'
    db_filepath = f'{output_folderpath}/terra.db'
    ###
    input_filenames = os.listdir(input_folderpath)
    all_data = []
    for i, input_filename in enumerate(input_filenames[:]):
        print(f'PLANTS - {i}/{len(input_filenames)}')
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
                plant_name_scientific_reference_normalize
            )
            VALUES (?, ?)
        """,
        [
            (
                item.get("plant_name_scientific_reference"),
                item.get("plant_name_scientific_reference_normalize"),
            )
            for item in all_data
        ]
    )
    conn.commit()
    conn.row_factory = sqlite3.Row
    cursor = conn.execute(f'''
        SELECT * 
        FROM {table_name}
    ''')
    rows = cursor.fetchall()
    items = [dict(row) for row in rows]
    for item in items[:10]:
        print(json.dumps(item, indent=4))
    print(len(items))
    conn.close()

def masterize_table_plants_parts_add(source_foldername, subfoldername):
    table_name = 'plants_parts'
    input_folderpath = f'{HUB_FOLDERPATH}/resolve/{source_foldername}/{subfoldername}/json'
    output_folderpath = f'{HUB_FOLDERPATH}/masterize'
    db_filepath = f'{output_folderpath}/master.db'
    ###
    input_filenames = os.listdir(input_folderpath)
    all_data = []
    for i, input_filename in enumerate(input_filenames[:]):
        print(f'{i}/{len(input_filenames)}')
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
                plant_part_name_reference, 
                plant_part_name_reference_normalize
            )
            VALUES (?, ?)
        """,
        [
            (
                item.get("plant_part_name_reference"),
                item.get("plant_part_name_reference_normalize"),
            )
            for item in all_data
        ]
    )
    conn.commit()
    rows = conn.execute(f"SELECT * FROM {table_name}")
    for row in list(rows)[:10]:
        print(row)
    conn.close()

def masterize_table_activities_add(source_foldername, subfoldername):
    table_name = 'activities'
    output_folderpath = f'{HUB_FOLDERPATH}/database'
    input_folderpath = f'{HUB_FOLDERPATH}/resolve/{source_foldername}/{subfoldername}/json'
    db_filepath = f'{output_folderpath}/terra.db'
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
                activity_name_reference, 
                activity_name_reference_normalize
            )
            VALUES (?, ?)
        """,
        [
            (
                item.get("activity_name_reference"),
                item.get("activity_name_reference_normalize"),
            )
            for item in all_data
        ]
    )
    conn.commit()
    conn.row_factory = sqlite3.Row
    cursor = conn.execute(f'''
        SELECT * 
        FROM {table_name}
    ''')
    rows = cursor.fetchall()
    items = [dict(row) for row in rows]
    for item in items[:10]:
        print(json.dumps(item, indent=4))
    print(len(items))
    conn.close()

def masterize_table_conditions_add(source_foldername):
    table_name = 'conditions'
    output_folderpath = f'{HUB_FOLDERPATH}/database'
    input_folderpath = f'{HUB_FOLDERPATH}/resolve/{source_foldername}/{table_name}/json'
    db_filepath = f'{output_folderpath}/terra.db'
    ###
    input_filenames = os.listdir(input_folderpath)
    all_data = []
    for i, input_filename in enumerate(input_filenames[:]):
        print(f'MASTERIZE HERBS conditions - {i}/{len(input_filenames)}')
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
                condition_name_reference, 
                condition_name_reference_normalize
            )
            VALUES (?, ?)
        """,
        [
            (
                item.get("condition_name_reference"),
                item.get("condition_name_reference_normalize"),
            )
            for item in all_data
        ]
    )
    conn.commit()
    conn.row_factory = sqlite3.Row
    cursor = conn.execute(f'''
        SELECT * 
        FROM {table_name}
    ''')
    rows = cursor.fetchall()
    items = [dict(row) for row in rows]
    for item in items[:10]:
        print(json.dumps(item, indent=4))
    print(len(items))
    conn.close()

def masterize_table_plants_names_common_add(source_foldername):
    table_name = 'plants_names_common'
    output_folderpath = f'{HUB_FOLDERPATH}/database'
    input_folderpath = f'{HUB_FOLDERPATH}/resolve/{source_foldername}/{table_name}/json'
    db_filepath = f'{output_folderpath}/terra.db'
    ###
    input_filenames = os.listdir(input_folderpath)
    all_data = []
    for i, input_filename in enumerate(input_filenames[:]):
        print(f'MASTERIZE HERBS plants names common - {i}/{len(input_filenames)}')
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
                plant_name_common_reference, 
                plant_name_common_reference_normalize,
                plant_name_common_transliteration,
                plant_name_common_language,
                plant_name_common_preferred,
                plant_name_common_country,
                plant_name_common_area
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        [
            (
                item.get('plant_name_common_reference'),
                item.get('plant_name_common_reference_normalize'),
                item.get('plant_name_common_transliteration'),
                item.get('plant_name_common_language'),
                item.get('plant_name_common_preferred'),
                item.get('plant_name_common_country'),
                item.get('plant_name_common_area'),
            )
            for item in all_data
        ]
    )
    conn.commit()
    conn.row_factory = sqlite3.Row
    cursor = conn.execute(f'''
        SELECT * 
        FROM {table_name}
    ''')
    rows = cursor.fetchall()
    items = [dict(row) for row in rows]
    for item in items[:10]:
        print(json.dumps(item, indent=4))
    print(len(items))
    conn.close()

def masterize_table_chemicals_add(source_foldername, subfoldername):
    table_name = 'chemicals'
    output_folderpath = f'{HUB_FOLDERPATH}/masterize'
    input_folderpath = f'{HUB_FOLDERPATH}/resolve/{source_foldername}/{subfoldername}/json'
    db_filepath = f'{output_folderpath}/master.db'
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
                chemical_name_reference, 
                chemical_name_reference_normalize
            )
            VALUES (?, ?)
        """,
        [
            (
                item.get("chemical_name_reference"),
                item.get("chemical_name_reference_normalize"),
            )
            for item in all_data
        ]
    )
    conn.commit()
    rows = conn.execute(f"SELECT * FROM {table_name}")
    for row in list(rows)[:10]:
        print(row)
    conn.close()

def run():
    print('MASTERIZE')

    # masterize_table_studies_add(source_foldername='pubmed')
    # masterize_table_plants_add(source_foldername='pubmed', subfoldername='plants')
    # masterize_table_activities_add(source_foldername='pubmed', subfoldername='activities')
    # masterize_table_conditions_add(source_foldername='pubmed')

    masterize_table_plants_names_common_add(source_foldername='col')

    if 0:
        # masterize_table_plants_add(source_foldername='drduke', subfoldername='activities')
        # masterize_table_plants_add(source_foldername='drduke', subfoldername='chemicals')
        '''
        masterize_table_plants_add(source_foldername='pubmed', subfoldername='diseases')
        '''
        masterize_table_plants_add(source_foldername='pubmed', subfoldername='activities')
        masterize_table_plants_add(source_foldername='pubmed', subfoldername='chemicals')
        masterize_table_plants_add(source_foldername='pubmed', subfoldername='conditions')
        masterize_table_plants_add(source_foldername='pubmed', subfoldername='plants_parts')
        masterize_table_plants_add(source_foldername='pubmed', subfoldername='preparations')

    return

    masterize_table_activities_add(source_foldername='drduke', subfoldername='activities')

    # masterize_table_chemicals_add(source_foldername='drduke', subfoldername='chemicals')
    masterize_table_chemicals_add(source_foldername='pubmed', subfoldername='chemicals')

    masterize_table_plants_parts_add(source_foldername='pubmed', subfoldername='plants_parts')

