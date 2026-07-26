
import os
import time
import json
import shutil
import sqlite3

from lib import g
from lib import io
from lib import llm

def observations_table_plants_chemicals_add(source_foldername):
    ###
    table_name = 'plants_chemicals'
    input_folderpath = f'{g.DATA_FOLDERPATH}/resolve/{source_foldername}/chemicals/json'
    output_folderpath = f'{g.DATA_FOLDERPATH}/observe'
    db_filepath = f'{output_folderpath}/observations.db'
    ###
    input_filenames = os.listdir(input_folderpath)
    all_data = []
    for i, input_filename in enumerate(input_filenames[:]):
        print(f'PLANTS_CHEMICALS - {i}/{len(input_filenames)}')
        input_filepath = f'{input_folderpath}/{input_filename}'
        input_data = io.json_read(input_filepath)
        # print(json.dumps(input_data, indent=4))
        # quit()
        for input_item in input_data:
            all_data.append(input_item)
            # print(json.dumps(input_item, indent=4))
            # quit()
    ###
    conn = sqlite3.connect(db_filepath)
    cur = conn.cursor()
    cur.executemany(
        f"""
            INSERT OR IGNORE INTO {table_name} (
                plant_canonical_name, 
                chemical_canonical_name, 
                plant_part, 
                concentration, 
                unit, 
                source_name
            )
            VALUES (?, ?, ?, ?, ?, ?)
        """,
        [
            (
                item.get("wcvp_taxon_name"),
                item.get("pubchem_chemical_name"),
                item.get("plant_part_name_raw"),
                "",
                "",
                item.get("source_name"),
            )
            for item in all_data
        ]
    )
    conn.commit()
    rows = conn.execute(f"SELECT * FROM {table_name}")
    for row in list(rows)[:10]:
        print(row)
    conn.close()

def test():
    output_folderpath = f'{g.VAULT_FOLDERPATH}/terrawhisper/data/observe'
    db_filepath = f'{output_folderpath}/observations.db'
    conn = sqlite3.connect(db_filepath)
    rows = conn.execute("SELECT * FROM plants_chemicals")
    for row in list(rows)[:10]:
        print(row)
    conn.close()

def run():
    print('OBSERVE')

    observations_table_plants_chemicals_add(source_foldername='drduke')
    observations_table_plants_chemicals_add(source_foldername='pubmed')
    # test()



