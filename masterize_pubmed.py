import os
import time
import json
import shutil
import sqlite3

from lib import g
from lib import io
from lib import llm

def master_table_plants_add():
    chemicals_input_folderpath = f'{g.VAULT_FOLDERPATH}/terrawhisper/data/resolve/pubmed/chemicals/json'
    activities_input_folderpath = f'{g.VAULT_FOLDERPATH}/terrawhisper/data/resolve/pubmed/activities/json'
    output_folderpath = f'{g.VAULT_FOLDERPATH}/terrawhisper/data/masterize'
    conn = sqlite3.connect(f"{g.VAULT_FOLDERPATH}/terrawhisper/data/reference/wcvp/wcvp.db")
    ### CHEMICALS > PLANTS
    input_filenames = os.listdir(chemicals_input_folderpath)
    chemicals_data = []
    for i, input_filename in enumerate(input_filenames[:]):
        print(f'{i}/{len(input_filenames)}')
        input_filepath = f'{chemicals_input_folderpath}/{input_filename}'
        input_data = io.json_read(input_filepath)
        for input_item in input_data:
            cursor = conn.execute("""
                SELECT *
                FROM wcvp
                WHERE taxon_name_normalized = ?
            """, (input_item['wcvp_taxon_name_normalized'],))
            row = cursor.fetchone()
            input_item['ipni_id'] = row[0]
            input_item['powo_id'] = row[1]
            input_item['taxon_name'] = row[2]
            input_item['taxon_name_normalized'] = row[3]
            input_item['taxon_rank'] = row[4]
            input_item['taxon_status'] = row[5]
            input_item['family'] = row[6]
            input_item['geographic_area'] = row[7]
            input_item['climate_description'] = row[8]
            chemicals_data.append(input_item)
    chemicals_data_query = [(
        item.get("plant_name"),
        item.get("ipni_id"),
        item.get("powo_id"),
        item.get("taxon_name"),
        item.get("taxon_name_normalized"),
        item.get("taxon_rank"),
        item.get("taxon_status"),
        item.get("family"),
        item.get("geographic_area"),
        item.get("climate_description"),
    ) for item in chemicals_data]
    ### ACTIVITIES > PLANTS
    input_filenames = os.listdir(activities_input_folderpath)
    activities_data = []
    for i, input_filename in enumerate(input_filenames[:]):
        print(f'{i}/{len(input_filenames)}')
        input_filepath = f'{activities_input_folderpath}/{input_filename}'
        input_data = io.json_read(input_filepath)
        for input_item in input_data:
            cursor = conn.execute("""
                SELECT *
                FROM wcvp
                WHERE taxon_name_normalized = ?
            """, (input_item['wcvp_taxon_name_normalized'],))
            row = cursor.fetchone()
            input_item['ipni_id'] = row[0]
            input_item['powo_id'] = row[1]
            input_item['taxon_name'] = row[2]
            input_item['taxon_name_normalized'] = row[3]
            input_item['taxon_rank'] = row[4]
            input_item['taxon_status'] = row[5]
            input_item['family'] = row[6]
            input_item['geographic_area'] = row[7]
            input_item['climate_description'] = row[8]
            activities_data.append(input_item)
    activities_data_query = [(
        item.get("plant_name"),
        item.get("ipni_id"),
        item.get("powo_id"),
        item.get("taxon_name"),
        item.get("taxon_name_normalized"),
        item.get("taxon_rank"),
        item.get("taxon_status"),
        item.get("family"),
        item.get("geographic_area"),
        item.get("climate_description"),
    ) for item in activities_data]

    ###
    db_filepath = f'{output_folderpath}/master.db'
    conn = sqlite3.connect(db_filepath)
    cur = conn.cursor()
    cur.executemany(
        """
        INSERT OR IGNORE INTO plants (
            canonical_name,
            ipni_id,
            powo_id,
            taxon_name,
            taxon_name_normalized,
            taxon_rank,
            taxon_status,
            family,
            geographic_area,
            climate_description
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, chemicals_data_query
    )
    cur.executemany(
        """
        INSERT OR IGNORE INTO plants (
            canonical_name,
            ipni_id,
            powo_id,
            taxon_name,
            taxon_name_normalized,
            taxon_rank,
            taxon_status,
            family,
            geographic_area,
            climate_description
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, activities_data_query
    )
    conn.commit()

    ### TEST
    rows = conn.execute("SELECT * FROM plants")
    for row in list(rows)[:10]:
        print(row)

    conn.close()

def master_table_activities_add():
    input_folderpath = f'{g.VAULT_FOLDERPATH}/terrawhisper/data/resolve/pubmed/activities/json'
    output_folderpath = f'{g.VAULT_FOLDERPATH}/terrawhisper/data/masterize'
    ###
    db_filepath = f'{output_folderpath}/master.db'
    input_filenames = os.listdir(input_folderpath)
    all_data = []
    for i, input_filename in enumerate(input_filenames[:]):
        print(f'{i}/{len(input_filenames)}')
        input_filepath = f'{input_folderpath}/{input_filename}'
        input_data = io.json_read(input_filepath)
        for input_item in input_data:
            all_data.append({
                'activity_name': input_item['activity_name']
            })
    conn = sqlite3.connect(db_filepath)
    cur = conn.cursor()
    print('start inserting...')
    cur.executemany(
        """
        INSERT OR IGNORE INTO activities (canonical_name)
        VALUES (?)
        """,
        [
            (
                item.get("activity_name"),
            )
            for item in all_data
        ]
    )
    conn.commit()
    rows = conn.execute("SELECT * FROM activities")
    for row in list(rows)[:10]:
        print(row)
    conn.close()

def master_table_diseases_add():
    input_folderpath = f'{g.VAULT_FOLDERPATH}/terrawhisper/data/resolve/pubmed/diseases/json'
    output_folderpath = f'{g.VAULT_FOLDERPATH}/terrawhisper/data/masterize'
    ###
    db_filepath = f'{output_folderpath}/master.db'
    input_filenames = os.listdir(input_folderpath)
    all_data = []
    for i, input_filename in enumerate(input_filenames[:]):
        print(f'{i}/{len(input_filenames)}')
        input_filepath = f'{input_folderpath}/{input_filename}'
        input_data = io.json_read(input_filepath)
        for input_item in input_data:
            all_data.append({
                'disease_name': input_item['disease_name']
            })
    conn = sqlite3.connect(db_filepath)
    cur = conn.cursor()
    print('start inserting...')
    cur.executemany(
        """
        INSERT OR IGNORE INTO diseases (canonical_name)
        VALUES (?)
        """,
        [
            (
                item.get("disease_name"),
            )
            for item in all_data
        ]
    )
    conn.commit()
    rows = conn.execute("SELECT * FROM diseases")
    for row in list(rows)[:10]:
        print(row)
    conn.close()

def test():
    db_filepath = f'{g.VAULT_FOLDERPATH}/terrawhisper/data/masterize/master.db'
    conn = sqlite3.connect(db_filepath)
    cur = conn.cursor()
    cur.execute("""
        SELECT *
        FROM plants
        LIMIT 10
    """)
    rows = cur.fetchall()
    for row in rows:
        print(row)
    conn.close()
    return rows

def run():
    print('masterize >> pubmed')

    master_table_plants_add()
    # master_table_activities_add()
    # master_table_diseases_add()

    test()

