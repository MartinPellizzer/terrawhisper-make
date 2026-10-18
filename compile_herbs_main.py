import json
import sqlite3

from lib import g
from lib import io
from lib import data

import masterize_utils
import schema_herbs

HUB_FOLDERPATH = f'''{g.DATA_FOLDERPATH}/herbs'''
input_folderpath = f'{HUB_FOLDERPATH}/augment'
output_folderpath = f'{HUB_FOLDERPATH}/compile'

def run():
    io.folders_recursive_gen(output_folderpath)
    master_items = masterize_utils.masterize_plants_get_all()
    for i, master_item in enumerate(master_items):
        print(f'COMPILE {i}/{len(master_items)}')
        plant_name_scientific_reference = master_item['plant_name_scientific_reference']
        output_filepath = f'{output_folderpath}/{plant_name_scientific_reference}.json'
        output_data = {}
        output_data['plant_name_scientific_reference'] = plant_name_scientific_reference

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

        """
        ### PREPARATIONS
        output_data['preparations'] = io.json_read(
            f'{input_folderpath}/preparations/{plant_name_scientific_reference}.json'
        )
        """

        ### TRAITS
        output_data['traits'] = io.json_read(
            f'{input_folderpath}/traits/{plant_name_scientific_reference}.json'
        )

        ### SYNONYMS
        output_data['synonyms'] = io.json_read(
            f'{input_folderpath}/synonyms/{plant_name_scientific_reference}.json'
        )

        ### TAXONOMIES
        output_data['taxonomies'] = io.json_read(
            f'{input_folderpath}/taxonomies/{plant_name_scientific_reference}.json'
        )

        ### INTRO
        output_data['intro'] = io.json_read(
            f'{input_folderpath}/intro/{plant_name_scientific_reference}.json'
        )

        """
        output_data['compounds'] = io.json_read(
            f'{input_folderpath}/compounds/{plant_name_scientific_reference}.json'
        )
        """

        ### INTRO
        output_data['plants_morphologies'] = io.json_read(
            f'{input_folderpath}/plants_morphologies/{plant_name_scientific_reference}.json'
        )

        schema_items = schema_herbs.data['items']
        for schema_item in schema_items: 
            schema_table_name = schema_item['table_name']
            if schema_table_name == 'plants_growth_forms': continue
            if schema_table_name == 'plants_climbers': continue
            if schema_table_name == 'plants_heights': continue
            output_data[schema_table_name] = io.json_read(
                f'{input_folderpath}/{schema_table_name}/{plant_name_scientific_reference}.json'
            )

        io.json_write(output_filepath, output_data)
        # if output_data['plants_compounds']['plants_compounds'] != []:
            # print(json.dumps(output_data, indent=4))
            # quit()

