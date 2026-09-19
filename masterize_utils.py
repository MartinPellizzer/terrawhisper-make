import sqlite3

from lib import g

HUB_HERBS_FOLDERPATH = f'''{g.DATA_FOLDERPATH}/herbs'''

def masterize_plants_get_all():
    db_filepath = f'{HUB_HERBS_FOLDERPATH}/masterize/master.db'
    conn = sqlite3.connect(db_filepath)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("""
        SELECT *
        FROM plants
    """)
    items = cur.fetchall()
    items = [dict(item) for item in items]
    conn.close()
    return items

def masterize_activities_get_all():
    db_filepath = f'{g.DATA_FOLDERPATH}/masterize/master.db'
    conn = sqlite3.connect(db_filepath)
    cur = conn.cursor()
    cur.execute("""
        SELECT *
        FROM activities
    """)
    rows = cur.fetchall()
    conn.close()
    return rows

def masterize_chemicals_get_all():
    db_filepath = f'{g.DATA_FOLDERPATH}/masterize/master.db'
    conn = sqlite3.connect(db_filepath)
    cur = conn.cursor()
    cur.execute("""
        SELECT *
        FROM chemicals
    """)
    rows = cur.fetchall()
    conn.close()
    return rows

def masterize_organizations_get_all():
    db_filepath = f'{g.DATA_FOLDERPATH}/organizations/masterize/master.db'
    conn = sqlite3.connect(db_filepath)
    cur = conn.cursor()
    cur.execute("""
        SELECT *
        FROM organizations
    """)
    rows = cur.fetchall()
    conn.close()
    return rows

