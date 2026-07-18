import json
import sqlite3

from lib import g
from lib import io
from lib import data

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

    plants_rows = sqlite_plants_get()
    for i, plant_row in enumerate(plants_rows):
        print(f'{i}/{len(plants_rows)}')
        plant_canonical_name = plant_row[1]
        output_filepath = f'{g.VAULT_FOLDERPATH}/terrawhisper/data/{output_foldername}/herbs/{plant_canonical_name}.json'
        output_data = {}
        output_data['plant_canonical_name'] = plant_row[1]

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

        ### CHEMICALS
        chemicals_data = io.json_read(
            f'{g.VAULT_FOLDERPATH}/terrawhisper/data/{input_foldername}/herbs/chemicals/{plant_canonical_name}.json'
        )
        # print(json.dumps(chemicals_data, indent=4))
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

        ### ACTIVITIES
        activities_data = io.json_read(
            f'{g.VAULT_FOLDERPATH}/terrawhisper/data/{input_foldername}/herbs/activities/{plant_canonical_name}.json'
        )
        # print(json.dumps(chemicals_data, indent=4))
        output_data['activities'] = []
        for activity_item in activities_data:
            activity_item_new = {
                "activity_canonical_name": activity_item['activity_canonical_name'],
                "num_sources": chemical_item['num_sources'],
            }
            output_data['activities'].append(activity_item)
        ###
        io.json_write(output_filepath, output_data)

        ### DISEASES
        diseases_data = io.json_read(
            f'{g.VAULT_FOLDERPATH}/terrawhisper/data/{input_foldername}/herbs/diseases/{plant_canonical_name}.json'
        )
        # print(json.dumps(chemicals_data, indent=4))
        output_data['diseases'] = []
        for disease_item in diseases_data:
            disease_item_new = {
                "disease_canonical_name": disease_item['disease_canonical_name'],
                "num_sources": chemical_item['num_sources'],
            }
            output_data['diseases'].append(disease_item)
        ###
        io.json_write(output_filepath, output_data)
            
        # quit()

