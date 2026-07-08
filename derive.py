import json
import sqlite3

from lib import g
from lib import io
from lib import data

input_foldername = 'qualify'
output_foldername = 'derive'
input_folderpath = f'{g.VAULT_FOLDERPATH}/terrawhisper/data/{input_foldername}'
output_folderpath = f'{g.VAULT_FOLDERPATH}/terrawhisper/data/{output_foldername}'
db_filepath = f'{input_folderpath}/observations.db'
###

def get_chemical_summary(plant_canonical_name):
    conn = sqlite3.connect(db_filepath)

    cursor = conn.execute("""
        SELECT
            chemical_canonical_name,
            plant_part,
            COUNT(DISTINCT source_name) AS num_sources,
            MIN(concentration) AS min_concentration,
            MAX(concentration) AS max_concentration
        FROM plants_chemicals
        WHERE plant_canonical_name = ?
        GROUP BY chemical_canonical_name, plant_part
        ORDER BY chemical_canonical_name, plant_part
    """, (plant_canonical_name,))

    rows = cursor.fetchall()
    conn.close()
    return rows

master_plants_rows = data.sqlite__plants_get()
for master_plant_row in master_plants_rows:
    chemical_summary_rows = get_chemical_summary(master_plant_row[1])
    output_items = []
    for row in chemical_summary_rows:
        output_item = {
            'plant_canonical_name': master_plant_row[1],
            'chemical_canonical_name': row[0],
            'plant_part': row[1],
            'num_sources': row[2],
            'min_concentration': row[3],
            'max_concentration': row[3],
        }
        print(json.dumps(output_item, indent=4))
        output_items.append(output_item)
    output_filepath = f'{g.VAULT_FOLDERPATH}/terrawhisper/data/{output_foldername}/herbs/chemicals/{master_plant_row[1]}.json'
    io.folder_create_from_filepath(output_filepath)
    io.json_write(output_filepath, output_items)

