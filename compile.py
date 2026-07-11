import json
import sqlite3

from lib import g
from lib import io
from lib import data

def sqlite__plants_get():
    db_filepath = f'{g.VAULT_FOLDERPATH}/terrawhisper/data/masterize/master.db'
    conn = sqlite3.connect(db_filepath)
    cur = conn.cursor()
    cur.execute("""
        SELECT *
        FROM plants
    """)
    row = cur.fetchall()
    conn.close()
    return row

input_foldername = 'derive'
output_foldername = 'compile'
input_folderpath = f'{g.VAULT_FOLDERPATH}/terrawhisper/data/{input_foldername}/herbs/chemicals'
output_folderpath = f'{g.VAULT_FOLDERPATH}/terrawhisper/data/{output_foldername}/herbs'
io.folders_recursive_gen(output_folderpath)

plants_rows = sqlite__plants_get()
for i, plant_row in enumerate(plants_rows):
    print(f'{i}/{len(plants_rows)}')
    plant_canonical_name = plant_row[1]
    chemicals_filepath = f'{g.VAULT_FOLDERPATH}/terrawhisper/data/{input_foldername}/herbs/chemicals/{plant_canonical_name}.json'
    output_filepath = f'{g.VAULT_FOLDERPATH}/terrawhisper/data/{output_foldername}/herbs/{plant_canonical_name}.json'
    print(output_filepath)
    chemicals_data = io.json_read(chemicals_filepath)
    # print(json.dumps(chemicals_data, indent=4))
    output_data = {}
    output_data['plant_canonical_name'] = plant_row[1]
    output_data['chemicals'] = []
    for chemical_item in chemicals_data:
        chemical_item_new = {
            "chemical_canonical_name": chemical_item['chemical_canonical_name'],
            "plant_part": chemical_item['plant_part'],
            "num_sources": chemical_item['num_sources'],
            "min_concentration": chemical_item['min_concentration'],
            "max_concentration": chemical_item['max_concentration'],
        }
        output_data['chemicals'].append(chemical_item)
    io.json_write(output_filepath, output_data)
        
    # quit()

