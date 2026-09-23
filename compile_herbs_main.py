import json
import sqlite3

from lib import g
from lib import io
from lib import data

import masterize_utils

HUB_FOLDERPATH = f'''{g.DATA_FOLDERPATH}/herbs'''
input_folderpath = f'{HUB_FOLDERPATH}/augment'
output_folderpath = f'{HUB_FOLDERPATH}/compile'

def run():
    io.folders_recursive_gen(output_folderpath)
    master_items = masterize_utils.masterize_plants_get_all()
    for i, master_item in enumerate(master_items):
        print(f'{i}/{len(master_items)}')
        plant_name_scientific_reference = master_item['plant_name_scientific_reference']
        output_filepath = f'{output_folderpath}/{plant_name_scientific_reference}.json'
        output_data = {}
        output_data['plant_name_scientific_reference'] = plant_name_scientific_reference

        """
        ### SYNONYMS
        output_data['synonyms'] = io.json_read(
            f'{input_folderpath}/{input_foldername}/herbs/synonyms/{plant_name_scientific_reference}.json'
        )

        ### TAXONOMIES
        taxonomies_data = io.json_read(
            f'{input_folderpath}/terrawhisper/data/{input_foldername}/herbs/taxonomies/{plant_name_scientific_reference}.json'
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
            f'{g.DATA_FOLDERPATH}/{input_foldername}/herbs/{data_type}/{plant_name_scientific_reference}.json'
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
        ### DISTRIBUTION
        distribution_data = io.json_read(
            f'{input_folderpath}/distribution/{plant_name_scientific_reference}.json'
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

        ### DISEASES
        output_data['diseases'] = io.json_read(
            f'{g.DATA_FOLDERPATH}/{input_foldername}/herbs/diseases/{plant_name_scientific_reference}.json'
        )

        """

        ### DISTRIBUTIONS
        output_data['distributions'] = io.json_read(
            f'{input_folderpath}/distributions/{plant_name_scientific_reference}.json'
        )

        ### NAMES COMMON (NEW) -> merge with wikidata
        output_data['names_common'] = io.json_read(
            f'{input_folderpath}/names_common/{plant_name_scientific_reference}.json'
        )

        ### ACTIVITIES
        output_data['activities'] = io.json_read(
            f'{input_folderpath}/activities/{plant_name_scientific_reference}.json'
        )

        ### CHEMICALS
        output_data['chemicals'] = io.json_read(
            f'{input_folderpath}/chemicals/{plant_name_scientific_reference}.json'
        )

        ### CONDITIONS
        output_data['conditions'] = io.json_read(
            f'{input_folderpath}/conditions/{plant_name_scientific_reference}.json'
        )

        ### PLANTS PARTS
        output_data['plants_parts'] = io.json_read(
            f'{input_folderpath}/plants_parts/{plant_name_scientific_reference}.json'
        )

        ### PREPARATIONS
        output_data['preparations'] = io.json_read(
            f'{input_folderpath}/preparations/{plant_name_scientific_reference}.json'
        )

        ### TRAITS
        output_data['traits'] = io.json_read(
            f'{input_folderpath}/traits/{plant_name_scientific_reference}.json'
        )

        io.json_write(output_filepath, output_data)
        # print(json.dumps(output_data, indent=4))
        # quit()

