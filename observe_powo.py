import os
import time
import json
import shutil
import sqlite3

from lib import g
from lib import io
from lib import llm

def observations_table_plants_taxonomies_add():
    source_foldername = 'powo'
    input_foldername = 'resolve'
    output_foldername = 'observe'
    input_folderpath = f'{g.DATA_FOLDERPATH}/{input_foldername}/{source_foldername}/json'
    output_folderpath = f'{g.DATA_FOLDERPATH}/{output_foldername}'
    ###
    db_filepath = f'{output_folderpath}/observations.db'
    input_filenames = os.listdir(input_folderpath)
    all_data = []
    for i, input_filename in enumerate(input_filenames[:]):
        print(f'{i}/{len(input_filenames)}')
        input_filepath = f'{input_folderpath}/{input_filename}'
        input_data = io.json_read(input_filepath)
        # if input_data['wcvp_taxon_name'] == 'Tabernaemontana markgrafiana':
            # print(json.dumps(input_data, indent=4))
            # quit()
        # print(json.dumps(input_data, indent=4))
        # quit()
        all_data.append(input_data)
    ###
    conn = sqlite3.connect(db_filepath)
    cur = conn.cursor()
    print('start inserting...')
    cur.executemany(
        """
        INSERT OR IGNORE INTO plants_taxonomies (
            plant_canonical_name, 
            taxon_kingdom,
            taxon_phylum,
            taxon_class,
            taxon_subclass,
            taxon_order,
            taxon_family,
            taxon_genus,
            source
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        [
            (
                item.get("wcvp_taxon_name").capitalize(),
                item.get("wcvp_kingdom"),
                item.get("wcvp_phylum"),
                item.get("wcvp_class"),
                item.get("wcvp_subclass"),
                item.get("wcvp_order"),
                item.get("wcvp_family"),
                item.get("wcvp_genus"),
                'Plants of the World Online',
            )
            for item in all_data
        ]
    )
    conn.commit()
    rows = conn.execute("SELECT * FROM plants_taxonomies")
    for row in list(rows)[:10]:
        print(row)
        # quit()
        # if row[1] == 'Tabernaemontana markgrafiana':
            # print(row)
            # quit()
    conn.close()

def run():
    print('OBSERVE >> pubmed')

    observations_table_plants_taxonomies_add()
