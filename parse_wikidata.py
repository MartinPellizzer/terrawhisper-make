import os
import csv
import json
import time
import shutil

from lib import g
from lib import io

import pipeline_utils

def wikidata_qids():
    input_folderpath = f'{g.DATA_FOLDERPATH}/fetch/wikidata/qids'
    output_folderpath = f'{g.DATA_FOLDERPATH}/parse/wikidata/json'
    io.folders_recursive_gen(output_folderpath)
    ###
    input_filenames = sorted(os.listdir(input_folderpath))
    for i, input_filename in enumerate(input_filenames[:]):
        print(f'{i}/{len(input_filenames)}')
        input_filepath = f'{input_folderpath}/{input_filename}'
        input_data = io.json_read(input_filepath)
        print(input_filepath)
        ### QID
        qid = input_filename.replace('.json', '')
        ### TAXON
        claims = input_data['claims']
        claim_taxon = claims['P225'][0]
        claim_taxon_value = claim_taxon['mainsnak']['datavalue']['value']
        ### LABELS (COMMON NAMES)
        labels_data = []
        labels = input_data['labels']
        for key, item in labels.items():
            labels_data.append(item)
        ### ALIASES (COMMON NAMES)
        aliases_data = []
        aliases = input_data['aliases']
        for key, item in aliases.items():
            aliases_data.append(item)
        ###
        output_filepath = f'{output_folderpath}/{input_filename}'
        output_item = {
            'taxon_name': claim_taxon_value,
            'source': 'wikidata',
            'qid': qid,
            'labels': labels_data,
            'aliases': aliases_data,
        }
        io.json_write(output_filepath, output_item)

def run():
    print('PARSE >> wikidata')

    start = time.perf_counter()
    wikidata_qids()
    print(f'wikidata qids() - execution time: ', time.perf_counter() - start)
