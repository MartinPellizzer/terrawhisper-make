import sqlite3

from lib import g

import masterize_utils

def plants_popular_get():
    plants_rows = masterize_utils.masterize_plants_get_all()
    plants_data = []
    db_filepath = f'{g.DATA_FOLDERPATH}/qualify/observations.db'
    conn = sqlite3.connect(db_filepath)
    for plant_row in plants_rows:
        plant_canonical_name = plant_row[1]
        rows_num = 0
        ###
        cursor = conn.execute("""
            SELECT COUNT (*)
            FROM plants_parts
            WHERE plant_canonical_name = ?
        """, (plant_canonical_name,))
        rows_num += int(cursor.fetchone()[0])
        cursor = conn.execute("""
            SELECT COUNT (*)
            FROM plants_chemicals
            WHERE plant_canonical_name = ?
        """, (plant_canonical_name,))
        rows_num += int(cursor.fetchone()[0])
        cursor = conn.execute("""
            SELECT COUNT (*)
            FROM plants_activities
            WHERE plant_canonical_name = ?
        """, (plant_canonical_name,))
        rows_num += int(cursor.fetchone()[0])
        cursor = conn.execute("""
            SELECT COUNT (*)
            FROM plants_diseases
            WHERE plant_canonical_name = ?
        """, (plant_canonical_name,))
        rows_num += int(cursor.fetchone()[0])
        print(rows_num)
        ###
        plant_item = {
            'plant_canonical_name': plant_canonical_name,
            'datapoints_num': rows_num,
        }
        plants_data.append(plant_item)
    conn.close()
    plants_data = sorted(plants_data, key=lambda x: x['datapoints_num'], reverse=True)
    plants_data = plants_data[:48]
    return plants_data

