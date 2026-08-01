import json
import sqlite3

from lib import g
from lib import io
from lib import data

import masterize_utils

def sqlite_plants_get():
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

def run():
    input_foldername = 'derive'
    output_foldername = 'compile'
    input_folderpath = f'{g.VAULT_FOLDERPATH}/terrawhisper/data/{input_foldername}/herbs/chemicals'
    output_folderpath = f'{g.VAULT_FOLDERPATH}/terrawhisper/data/{output_foldername}/herbs'
    io.folders_recursive_gen(output_folderpath)

    plants_rows = masterize_utils.masterize_plants_get_all()
    for i, plant_row in enumerate(plants_rows):
        print(f'{i}/{len(plants_rows)}')
        plant_canonical_name = plant_row[1]
        output_filepath = f'{g.VAULT_FOLDERPATH}/terrawhisper/data/{output_foldername}/herbs/{plant_canonical_name}.json'
        output_data = {}
        output_data['plant_canonical_name'] = plant_row[1]

        ### SYNONYMS
        output_data['synonyms'] = io.json_read(
            f'{g.DATA_FOLDERPATH}/{input_foldername}/herbs/synonyms/{plant_canonical_name}.json'
        )

        ### TAXONOMIES
        taxonomies_data = io.json_read(
            f'{g.VAULT_FOLDERPATH}/terrawhisper/data/{input_foldername}/herbs/taxonomies/{plant_canonical_name}.json'
        )
        # print(json.dumps(chemicals_data, indent=4))
        output_data['taxonomies'] = []
        for item in taxonomies_data:
            item_new = {
                "kingdom": item['kingdom'],
                "phylum": item['phylum'],
                "class": item['class'],
                "subclass": item['subclass'],
                "order": item['order'],
                "family": item['family'],
                "genus": item['genus'],
            }
            output_data['taxonomies'].append(item)

        '''
        ### NAMES
        data_type = 'names'
        data = io.json_read(
            f'{g.DATA_FOLDERPATH}/{input_foldername}/herbs/{data_type}/{plant_canonical_name}.json'
        )
        # print(json.dumps(chemicals_data, indent=4))
        output_data['names'] = []
        for item in data:
            item_new = {
                "name_type": item['name_type'],
                "language_code": item['language_code'],
                "language_value": item['language_value'],
                "source": item['source'],
            }
            output_data[f'{data_type}'].append(item)

        '''
        ### NAMES COMMON (NEW) -> merge with wikidata
        output_data['names_common'] = io.json_read(
            f'{g.DATA_FOLDERPATH}/{input_foldername}/herbs/names_common/{plant_canonical_name}.json'
        )

        ### DISTRIBUTION
        distribution_data = io.json_read(
            f'{g.VAULT_FOLDERPATH}/terrawhisper/data/{input_foldername}/herbs/distribution/{plant_canonical_name}.json'
        )
        # print(json.dumps(chemicals_data, indent=4))
        output_data['distribution'] = []
        for item in distribution_data:
            item_new = {
                "continent": item['continent'],
                "region": item['region'],
                "area": item['area'],
            }
            output_data['distribution'].append(item)

        ### PLANTS PARTS
        output_data['plants_parts'] = io.json_read(
            f'{g.DATA_FOLDERPATH}/{input_foldername}/herbs/plants_parts/{plant_canonical_name}.json'
        )

        ### CHEMICALS
        output_data['chemicals'] = io.json_read(
            f'{g.DATA_FOLDERPATH}/{input_foldername}/herbs/chemicals/{plant_canonical_name}.json'
        )

        ### ACTIVITIES
        output_data['activities'] = io.json_read(
            f'{g.DATA_FOLDERPATH}/{input_foldername}/herbs/activities/{plant_canonical_name}.json'
        )

        ### DISEASES
        output_data['diseases'] = io.json_read(
            f'{g.DATA_FOLDERPATH}/{input_foldername}/herbs/diseases/{plant_canonical_name}.json'
        )

        ### PREPARATIONS 
        output_data['preparations'] = io.json_read(
            f'{g.DATA_FOLDERPATH}/{input_foldername}/herbs/preparations/{plant_canonical_name}.json'
        )

        ###

        io.json_write(output_filepath, output_data)

        # quit()

