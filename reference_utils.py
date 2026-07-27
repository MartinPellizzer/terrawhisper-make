import sqlite3

from lib import g

def wcvp_plant_name_get_row(plant_name_normalized):
    conn = sqlite3.connect(f'{g.DATA_FOLDERPATH}/reference/wcvp/wcvp.db')
    cursor = conn.execute("""
        SELECT *
        FROM plants_names
        WHERE taxon_name_normalized = ?
    """, (plant_name_normalized,))
    row = cursor.fetchone()
    return row

def wcvp_plant_synonym_get_rows(plant_name_normalized):
    conn = sqlite3.connect(f'{g.DATA_FOLDERPATH}/reference/wcvp/wcvp.db')
    cursor = conn.execute("""
        SELECT s.*
        FROM plants_names AS a
        JOIN plants_names AS s
            ON s.accepted_plant_name_id = a.plant_name_id
        WHERE a.taxon_name_normalized = ?
          AND a.plant_name_id = a.accepted_plant_name_id
          AND s.plant_name_id <> s.accepted_plant_name_id
          AND s.taxon_status = 'Synonym';
    """, (plant_name_normalized,))
    rows = cursor.fetchall()
    return rows
