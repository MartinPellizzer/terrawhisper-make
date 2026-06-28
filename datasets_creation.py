import sqlite3
import csv
import json

from lib import g
from lib import io

DB_PATH = f'{g.SSOT_FOLDERPATH}/datasets/powo/wcvp/wcvp.db'
CSV_PATH = f'{g.SSOT_FOLDERPATH}/datasets/powo/wcvp/wcvp_names.csv'

wcvp_csv_path = f''

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

cur.execute("DROP TABLE IF EXISTS wcvp")

cur.execute("""
    CREATE TABLE IF NOT EXISTS wcvp (
        powo_id TEXT,
        taxon_name TEXT,
        data JSON
    )
""")

conn.execute("PRAGMA journal_mode = WAL;")
conn.execute("PRAGMA synchronous = OFF;")
conn.execute("PRAGMA temp_store = MEMORY;")

wcvp_data = io.csv_to_dict(CSV_PATH, delimiter="|")
'''
wcvp_rows = []
for item in wcvp_data:
    wcvp_rows.append((item['powo_id'], item['taxon_name']))
'''

print('start inserting...')
cur.executemany(
    """
    INSERT OR REPLACE INTO wcvp (powo_id, taxon_name, data)
    VALUES (?, ?, ?)
    """,
    [
        (
            item.get("powo_id"),
            item.get("taxon_name"),
            json.dumps(item)
        )
        for item in wcvp_data
    ]
)

'''
BATCH_SIZE = 10000
total = len(wcvp_rows)
for i in range(0, total, BATCH_SIZE):
    batch = wcvp_rows[i:i + BATCH_SIZE]
    if 0:
        cur.executemany("""
            INSERT OR IGNORE INTO wcvp (powo_id, taxon_name)
            VALUES (?, ?)
        """, batch)

    print(f"{min(i + BATCH_SIZE, total):,} / {total:,} rows inserted")
'''

cur.execute("CREATE INDEX idx_wcvp_taxon_name ON wcvp(taxon_name)")
cur.execute("CREATE UNIQUE INDEX idx_wcvp_powo_id ON wcvp(powo_id)")
conn.commit()

conn.commit()
conn.close()

