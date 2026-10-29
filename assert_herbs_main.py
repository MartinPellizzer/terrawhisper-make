### TODO: add study id
"""
    {
        "study_id": 9,
        "study_pmid": "8660820",
        "study_title": "Suppression of interleukin-1 and tumor necrosis factor-alpha production by acanthoic acid, (-)-pimara-9(11),15-dien-19-oic acid, and it antifibrotic effects in vivo."
    }
    {
        "study_id": 10,
        "study_pmid": "7829499",
        "study_title": "The delta pH-driven, ATP-independent protein translocation mechanism in the chloroplast thylakoid membrane. Kinetics and energetics."
    }
"""

import os
import json
import sqlite3

from lib import g
from lib import io

import sql

HUB_FOLDERPATH = f'''{g.DATA_FOLDERPATH}/herbs'''
output_folderpath = f'{HUB_FOLDERPATH}/database'
db_filepath = f'{output_folderpath}/terra.db'

def assertions_plants_activities_table_create():
    table_name = f'plants_activities'
    conn = sqlite3.connect(db_filepath)
    cur = conn.cursor()
    cur.execute(f"DROP TABLE IF EXISTS {table_name}")
    cur.execute(f'''
        CREATE TABLE IF NOT EXISTS {table_name} (
            plant_activity_id INTEGER PRIMARY KEY,
            plant_id TEXT,
            activity_id TEXT,
            study_id TEXT
        );
    ''')
    conn.execute("PRAGMA journal_mode = WAL;")
    conn.execute("PRAGMA synchronous = OFF;")
    conn.execute("PRAGMA temp_store = MEMORY;")
    cur.execute(f"CREATE INDEX IF NOT EXISTS idx_{table_name}_plant_id ON {table_name}(plant_id)")
    cur.execute(f"CREATE INDEX IF NOT EXISTS idx_{table_name}_activity_id ON {table_name}(activity_id)")
    cur.execute(f"CREATE INDEX IF NOT EXISTS idx_{table_name}_study_id ON {table_name}(study_id)")
    conn.commit()
    conn.close()

def assertions_plants_activities_table_add():
    table_name = 'plants_activities'
    input_folderpath = f'{HUB_FOLDERPATH}/resolve/pubmed/{table_name}/json'
    input_filenames = os.listdir(input_folderpath)
    ###
    all_data = []
    for i, input_filename in enumerate(input_filenames[:]):
        print(f'ASSERT HERBS plants_activities - {i}/{len(input_filenames)}')
        input_filepath = f'{input_folderpath}/{input_filename}'
        input_data = io.json_read(input_filepath)
        for input_item in input_data:
            all_data.append(input_item)
            # print(json.dumps(input_item, indent=4))
            # quit()
    # print(json.dumps(all_data[0], indent=4))
    # quit()
    data_ids = [] 
    plant_failed_count = 0
    plant_success_count = 0
    activity_failed_count = 0
    activity_success_count = 0
    study_failed_count = 0
    study_success_count = 0
    test_plant_count = 0
    for i, item in enumerate(all_data):
        print(f'ASSERT HERBS plants_activities - {i}/{len(all_data)}')
        plant_item = sql.sql_plant_id_by_name_normalize(item['plant_name_scientific_reference_normalize'])
        activity_item = sql.sql_activity_id_by_name_normalize(item['activity_name_reference_normalize'])
        study_item = sql.sql_study_id_by_pmid(item['reference_id'])
        # print(source_item )
        # quit()
        if plant_item == None:
            plant_failed_count += 1
            continue
        else:
            plant_success_count += 1
        if activity_item == None:
            activity_failed_count += 1
            continue
        else:
            activity_success_count += 1
        if study_item == None:
            study_failed_count += 1
            continue
        else:
            study_success_count += 1
        if plant_item['plant_name_scientific_reference_normalize'] == 'panax ginseng':
            test_plant_count += 1
        plant_id = plant_item['plant_id']
        activity_id = activity_item['activity_id']
        study_id = study_item['study_id']
        # print(plant_id)
        # print(activity_id)
        data_ids.append(
            {
                'plant_id': plant_item['plant_id'],
                'activity_id': activity_item['activity_id'],
                'study_id': study_item['study_id'],
            }
        )
        # quit()
    print(data_ids[0])
    print(plant_failed_count)
    print(activity_failed_count)
    print(study_failed_count)
    print(plant_success_count)
    print(activity_success_count)
    print(study_success_count)
    print(test_plant_count)
    # quit()
    ###
    conn = sqlite3.connect(db_filepath)
    cur = conn.cursor()
            # INSERT OR IGNORE INTO {table_name} (
    sql_query = f'''
            INSERT OR IGNORE INTO {table_name} (
                plant_id,
                activity_id,
                study_id
            )
            VALUES (?, ?, ?)
    '''
    cur.executemany(
        sql_query,
        [
            (
                item.get(f'plant_id'),
                item.get(f'activity_id'),
                item.get(f'study_id'),
            )
            for item in data_ids
        ]
    )
    conn.commit()
    conn.row_factory = sqlite3.Row
    cursor = conn.execute(f'''
        SELECT * 
        FROM {table_name}
    ''')
        # WHERE plant_name_scientific_reference_normalize == "panax ginseng"
    rows = cursor.fetchall()
    items = [dict(row) for row in rows]
    for item in items[:10]:
        print(json.dumps(item, indent=4))
    print(len(items))
    # for row in list(rows)[:10]:
        # print(row)
    ###
    # cols = conn.execute(f'PRAGMA table_info({schema_table_name})').fetchall()
    # print([c[1] for c in cols])
    # print(json.dumps(all_data[0], indent=4))
    # quit()
    ###
    conn.close()

def assertions_plants_activities_table_join():
    plant_name = "panax ginseng"
    sql_items = sql_plant_activities_by_name_normalize(plant_name)
    for item in items:
        print(json.dumps(sql_item, indent=4))
    print(len(results))
    conn.close()

def assertions__plants__plants_names_common__table_create():
    table_name = f'plants__plants_names_common'
    conn = sqlite3.connect(db_filepath)
    cur = conn.cursor()
    cur.execute(f"DROP TABLE IF EXISTS {table_name}")
    cur.execute(f'''
        CREATE TABLE IF NOT EXISTS {table_name} (
            plant_activity_id INTEGER PRIMARY KEY,
            plant_id TEXT,
            plant_name_common_id TEXT,
            study_id TEXT
        );
    ''')
    conn.execute("PRAGMA journal_mode = WAL;")
    conn.execute("PRAGMA synchronous = OFF;")
    conn.execute("PRAGMA temp_store = MEMORY;")
    cur.execute(f"CREATE INDEX IF NOT EXISTS idx_{table_name}_plant_id ON {table_name}(plant_id)")
    cur.execute(f"CREATE INDEX IF NOT EXISTS idx_{table_name}_plant_name_common_id ON {table_name}(plant_name_common_id)")
    cur.execute(f"CREATE INDEX IF NOT EXISTS idx_{table_name}_study_id ON {table_name}(study_id)")
    conn.commit()
    conn.close()

def assertions__plants__plants_names_common__table_add(source_foldername):
    table_name = 'plants__plants_names_common'
    input_folderpath = f'{HUB_FOLDERPATH}/resolve/{source_foldername}/{table_name}/json'
    input_filenames = os.listdir(input_folderpath)
    ###
    all_data = []
    for i, input_filename in enumerate(input_filenames[:]):
        print(f'ASSERT HERBS {table_name} add - {i}/{len(input_filenames)}')
        input_filepath = f'{input_folderpath}/{input_filename}'
        input_data = io.json_read(input_filepath)
        for input_item in input_data:
            all_data.append(input_item)
    # print(json.dumps(all_data[0], indent=4))
    # quit()
    ###
    plant_item_failed = 0
    data_ids = [] 
    for i, item in enumerate(all_data):
        print(f'ASSERT HERBS {table_name} add - {i}/{len(all_data)}')
        plant_item = sql.sql_plant_id_by_name_normalize(item['plant_name_scientific_reference_normalize'])
        plant_name_common_item = sql.sql_plant_name_common_id_by_name_normalize(item['plant_name_common_reference_normalize'])
        # study_item = sql.sql_study_id_by_pmid(item['source_id'])
        ###
        # print(plant_item)
        # print(plant_name_common_item)
        try: plant_id = plant_item['plant_id']
        except:
            plant_item_failed += 1
            continue
        plant_name_common_id = plant_name_common_item['plant_name_common_id']
        # study_id = study_item['study_id']
        data_ids.append(
            {
                'plant_id': plant_item['plant_id'],
                'plant_name_common_id': plant_name_common_item['plant_name_common_id'],
                # 'study_id': study_item['study_id'],
            }
        )
    ### INSERT TODO: add source id after creating source table
    conn = sqlite3.connect(db_filepath)
    cur = conn.cursor()
    sql_query = f'''
            INSERT OR IGNORE INTO {table_name} (
                plant_id,
                plant_name_common_id
            )
            VALUES (?, ?)
    '''
    cur.executemany(
        sql_query,
        [
            (
                item.get(f'plant_id'),
                item.get(f'plant_name_common_id'),
            )
            for item in data_ids
        ]
    )
    conn.commit()
    ### PEEK
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
    ###
    print(f'PLANT ITEM FAILED: {plant_item_failed}')
    conn.close()

def assertions__plants__plants_names_common__table_join():
    plants_items = sql.sql_plants()
    last = []
    for i, plant_item in enumerate(plants_items[:100]):
        print(f'ASSERT HERBS plants__plants_names_common__table_join {i}/{len(plants_items)}')
        plant_name_scientific_reference = plant_item['plant_name_scientific_reference']
        items = sql.sql__plants__plants_names_common__by_plant_name__and_group(plant_name_scientific_reference)
        for item in items:
            print(json.dumps(item, indent=4))
            quit()

def run():
    # assertions_plants_activities_table_create()
    # assertions_plants_activities_table_add()
    # assertions_plants_activities_table_join()

    # assertions__plants__plants_names_common__table_create()
    # assertions__plants__plants_names_common__table_add(source_foldername='col')
    assertions__plants__plants_names_common__table_join()

