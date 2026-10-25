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
        CREATE TABLE IF NOT EXISTS plants_activities (
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
    conn.commit()
    conn.close()

### TODO: add study id
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
    activity_failed_count = 0
    test_plant_count = 0
    for i, item in enumerate(all_data):
        print(f'ASSERT HERBS plants_activities - {i}/{len(all_data)}')
        plant_item = sql.sql_plant_id_by_name_normalize(item['plant_name_scientific_reference_normalize'])
        activity_item = sql.sql_activity_id_by_name_normalize(item['activity_name_reference_normalize'])
        if plant_item == None:
            plant_failed_count += 1
            continue
        if activity_item == None:
            activity_failed_count += 1
            continue
        if plant_item['plant_name_scientific_reference_normalize'] == 'panax ginseng':
            test_plant_count += 1
        plant_id = plant_item['plant_id']
        activity_id = activity_item['activity_id']
        # print(plant_id)
        # print(activity_id)
        data_ids.append(
            {
                'plant_id': plant_item['plant_id'],
                'activity_id': activity_item['activity_id'],
            }
        )
        # quit()
    print(data_ids[0])
    print(plant_failed_count)
    print(activity_failed_count)
    print(test_plant_count)
    quit()
    ###
    conn = sqlite3.connect(db_filepath)
    cur = conn.cursor()
            # INSERT OR IGNORE INTO {table_name} (
    sql_query = f'''
            INSERT INTO {table_name} (
                plant_id,
                activity_id
            )
            VALUES (?, ?)
    '''
    cur.executemany(
        sql_query,
        [
            (
                item.get(f'plant_id'),
                item.get(f'activity_id'),
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

def run():
    assertions_plants_activities_table_create()
    assertions_plants_activities_table_add()
    # assertions_plants_activities_table_join()
