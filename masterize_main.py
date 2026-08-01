import os
import time
import json
import shutil
import sqlite3

from lib import g
from lib import io
from lib import llm

def masterize_table_plants_add(source_foldername, subfoldername):
    table_name = 'plants'
    output_folderpath = f'{g.DATA_FOLDERPATH}/masterize'
    input_folderpath = f'{g.DATA_FOLDERPATH}/resolve/{source_foldername}/{subfoldername}/json'
    db_filepath = f'{output_folderpath}/master.db'
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
    ###
    conn = sqlite3.connect(db_filepath)
    cur = conn.cursor()
    cur.executemany(
        f"""
            INSERT OR IGNORE INTO {table_name} (
                plant_name_scientific_canon, 
                plant_name_scientific_canon_norm
            )
            VALUES (?, ?)
        """,
        [
            (
                item.get("plant_name_scientific_canon"),
                item.get("plant_name_scientific_canon_norm"),
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
    output_folderpath = f'{g.DATA_FOLDERPATH}/masterize'
    input_folderpath = f'{g.DATA_FOLDERPATH}/resolve/{source_foldername}/{subfoldername}/json'
    db_filepath = f'{output_folderpath}/master.db'
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
                activity_name_canon, 
                activity_name_canon_norm
            )
            VALUES (?, ?)
        """,
        [
            (
                item.get("activity_name_canon"),
                item.get("activity_name_canon_norm"),
            )
            for item in all_data
        ]
    )
    conn.commit()
    rows = conn.execute(f"SELECT * FROM {table_name}")
    for row in list(rows)[:10]:
        print(row)
    conn.close()

def masterize_table_chemicals_add(source_foldername, subfoldername):
    table_name = 'chemicals'
    output_folderpath = f'{g.DATA_FOLDERPATH}/masterize'
    input_folderpath = f'{g.DATA_FOLDERPATH}/resolve/{source_foldername}/{subfoldername}/json'
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
                chemical_name_canon, 
                chemical_name_canon_norm
            )
            VALUES (?, ?)
        """,
        [
            (
                item.get("chemical_name_canon"),
                item.get("chemical_name_canon_norm"),
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

    if 1:
        masterize_table_plants_add(source_foldername='drduke', subfoldername='activities')
        masterize_table_plants_add(source_foldername='drduke', subfoldername='chemicals')
        masterize_table_plants_add(source_foldername='pubmed', subfoldername='activities')
        masterize_table_plants_add(source_foldername='pubmed', subfoldername='chemicals')
        '''
        masterize_table_plants_add(source_foldername='pubmed', subfoldername='diseases')
        masterize_table_plants_add(source_foldername='pubmed', subfoldername='plants_parts')
        masterize_table_plants_add(source_foldername='pubmed', subfoldername='preparations')
        '''

    if 1:
        masterize_table_activities_add(source_foldername='drduke', subfoldername='activities')
        masterize_table_activities_add(source_foldername='pubmed', subfoldername='activities')

    if 1:
        masterize_table_chemicals_add(source_foldername='drduke', subfoldername='chemicals')
        masterize_table_chemicals_add(source_foldername='pubmed', subfoldername='chemicals')

