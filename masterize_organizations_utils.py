import sqlite3

from lib import g

HUB_FOLDERPATH = f'{g.DATA_FOLDERPATH}/organizations' 

def masterize_organizations_get_all():
    db_filepath = f'{HUB_FOLDERPATH}/masterize/master.db'
    conn = sqlite3.connect(db_filepath)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    rows = cur.execute(f'SELECT * FROM organizations').fetchall()
    dict_rows = [dict(row) for row in rows]
    conn.close()
    return dict_rows

