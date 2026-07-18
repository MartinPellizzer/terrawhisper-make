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
