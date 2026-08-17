import os
import time
import json
import shutil
import sqlite3

from lib import g
from lib import io
from lib import llm

HUB_FOLDERPATH = f'{g.DATA_FOLDERPATH}/organizations'

def observations_table_organizations_add(source_foldername):
    table_name = 'organizations'
    input_folderpath = f'{HUB_FOLDERPATH}/resolve/{source_foldername}/json'
    output_folderpath = f'{HUB_FOLDERPATH}/observe'
    db_filepath = f'{output_folderpath}/observations.db'
    ###
    input_filenames = os.listdir(input_folderpath)
    all_data = []
    for i, input_filename in enumerate(input_filenames[:]):
        print(f'ORGANIZATIONS - {i}/{len(input_filenames)}')
        input_filepath = f'{input_folderpath}/{input_filename}'
        input_data = io.json_read(input_filepath)
        for input_item in input_data:
            all_data.append(input_item)
            # print(json.dumps(input_item, indent=4))
            # quit()

    columns = list(all_data[0].keys())
    col_names = ", ".join(columns)
    placeholders = ", ".join(["?"] * len(columns))
    query = f"INSERT OR IGNORE INTO {table_name} ({col_names}) VALUES ({placeholders})"
    values = [tuple(item.get(col) for col in columns) for item in all_data]
    ###
    conn = sqlite3.connect(db_filepath)
    cur = conn.cursor()
    cur.executemany(query, values)
    conn.commit()

    ###
    '''
    conn = sqlite3.connect(db_filepath)
    cur = conn.cursor()
    cur.executemany(
        f"""
            INSERT OR IGNORE INTO {table_name} (
                business_is_category_herbs,
                business_label,
                business_name,
                business_name_official,
                business_name_legal,
                business_name_trade,
                business_slogan
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        [
            (
                item.get("business_is_category_herbs"),
                item.get("business_label"),
                item.get("business_name"),
                item.get("business_name_official"),
                item.get("business_name_legal"),
                item.get("business_name_trade"),
                item.get("business_slogan"),
            )
            for item in all_data
        ]
    )
    conn.commit()
    rows = conn.execute(f'SELECT * FROM {table_name}')
    for row in list(rows)[:10]:
        print(row)
    '''

    ### PEEK
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    rows = cur.execute(f'SELECT * FROM {table_name} LIMIT 10').fetchall()
    dict_rows = [dict(row) for row in rows]
    for row in dict_rows[:1]:
        print(json.dumps(row, indent=4))

    conn.close()


def run():
    print('OBSERVE')

    if 1:
        observations_table_organizations_add(source_foldername='website')

