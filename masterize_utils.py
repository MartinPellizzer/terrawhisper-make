import sqlite3

from lib import g

def masterize_plants_get_all():
    db_filepath = f'{g.DATA_FOLDERPATH}/masterize/master.db'
    conn = sqlite3.connect(db_filepath)
    cur = conn.cursor()
    cur.execute("""
        SELECT *
        FROM plants
    """)
    rows = cur.fetchall()
    conn.close()
    return rows
