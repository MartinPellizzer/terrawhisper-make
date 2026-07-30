import os
import csv
import json
import time
import shutil

from lib import g
from lib import io

import pipeline_utils
import parse_utils

def parse_names():
    input_folderpath = f'{g.DATA_FOLDERPATH}/fetch/wikidata/qids'
    output_folderpath = f'{g.DATA_FOLDERPATH}/parse/wikidata/names/json'
    io.folders_recursive_gen(output_folderpath)
    ###
    input_filenames = sorted(os.listdir(input_folderpath))
    for i, input_filename in enumerate(input_filenames[:]):
        print(f'{i}/{len(input_filenames)}')
        input_filepath = f'{input_folderpath}/{input_filename}'
        input_data = io.json_read(input_filepath)
        # print(input_filepath)
        ### QID
        qid = input_filename.replace('.json', '')
        ### TAXON
        claims = input_data['claims']
        claim_taxon = claims['P225'][0]
        claim_taxon_value = claim_taxon['mainsnak']['datavalue']['value']
        ###
        output_items = []
        ### LABELS (COMMON NAMES)
        labels = input_data['labels']
        for key, label_item in labels.items():
            # print(json.dumps(labels_data, indent=4))
            # quit()
            output_item = parse_utils.common_name_create(
                plant_name_scientific_raw = claim_taxon_value,
                plant_name_scientific_norm = '',
                plant_name_common_raw = label_item['value'],
                plant_name_common_transliteration = '',
                plant_name_common_language = label_item['language'],
                plant_name_common_preferred = '',
                plant_name_common_country = '',
                plant_name_common_area = '',
                plant_name_common_type = 'label',
                source_name = 'Wikidata',
                source_acronym = '',
            )
            # print(json.dumps(output_item, indent=4))
            # quit()
            output_items.append(output_item)
        # quit()
        ### ALIASES (COMMON NAMES)
        aliases = input_data['aliases']
        for key, lst in aliases.items():
            for alias_item in lst:
                # print(json.dumps(alias_item, indent=4))
                # quit()
                output_item = parse_utils.common_name_create(
                    plant_name_scientific_raw = claim_taxon_value,
                    plant_name_scientific_norm = '',
                    plant_name_common_raw = alias_item['value'],
                    plant_name_common_transliteration = '',
                    plant_name_common_language = alias_item['language'],
                    plant_name_common_preferred = '',
                    plant_name_common_country = '',
                    plant_name_common_area = '',
                    plant_name_common_type = 'alias',
                    source_name = 'Wikidata',
                    source_acronym = '',
                )
                # print(json.dumps(output_item, indent=4))
                # quit()
                output_items.append(output_item)
        ###
        output_filepath = f'{output_folderpath}/{input_filename}'
        io.json_write(output_filepath, output_items)

def run():
    print('PARSE >> wikidata')

    start = time.perf_counter()
    parse_names()
    print(f'parse names() - execution time: ', time.perf_counter() - start)
