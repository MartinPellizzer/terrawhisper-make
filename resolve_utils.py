import sqlite3

from lib import g

### RESOLVE FOR "ACCEPTED" NAMES WHERE POSSIBLE
def resolve_plant(conn, name_normalized):
    wcvp_cur = conn.cursor()
    wcvp_cur.execute("""
        SELECT *
        FROM plants_names
        WHERE taxon_name_normalized = ?
    """, (name_normalized,))
    wcvp_row = wcvp_cur.fetchone()
    if wcvp_row != None:
        plant_name_id = wcvp_row[0]
        accepted_plant_name_id = wcvp_row[1]
        if plant_name_id != accepted_plant_name_id:
            wcvp_cur.execute("""
                SELECT *
                FROM plants_names
                WHERE plant_name_id = ?
            """, (accepted_plant_name_id,))
            wcvp_row = wcvp_cur.fetchone()
    return wcvp_row

