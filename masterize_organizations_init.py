import os
import time
import json
import shutil
import sqlite3

from lib import g
from lib import io

HUB_ORGANIZATIONS_FOLDERPATH = f'{g.DATA_FOLDERPATH}/organizations'

output_folderpath = f'{HUB_ORGANIZATIONS_FOLDERPATH}/masterize'
db_filepath = f'{output_folderpath}/master.db'

def master_table_organizations_create(regen=False):
    table_name = 'organizations'
    ###
    conn = sqlite3.connect(db_filepath)
    cur = conn.cursor()
    if regen:
        cur.execute(f"DROP TABLE IF EXISTS {table_name}")
    cur.execute(f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            id INTEGER PRIMARY KEY,
            business_name_canonical TEXT NOT NULL UNIQUE,
            business_name_normalize TEXT NOT NULL UNIQUE,
            business_name_display TEXT NOT NULL UNIQUE,
            business_slug TEXT NOT NULL UNIQUE
        );
    """)
    conn.execute("PRAGMA journal_mode = WAL;")
    conn.execute("PRAGMA synchronous = OFF;")
    conn.execute("PRAGMA temp_store = MEMORY;")
    ###
    cur.execute(f"CREATE INDEX IF NOT EXISTS idx_{table_name}_business_name_canonical ON {table_name}(business_name_canonical)")
    conn.commit()
    conn.close()

def run():
    os.makedirs(output_folderpath, exist_ok=True)
    master_table_organizations_create(regen=True)

