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
        labels = input_data['labels']
        if 'en' in labels:
            labels_en = labels['en']['value']
            if labels_en.lower().strip() == claim_taxon_value.lower().strip():
                labels_en = None
        else:
            labels_en = None
        ### ALIASES (COMMON NAMES)
        aliases = input_data['aliases']
        if 'en' in aliases:
            aliases_en = aliases['en'][0]['value']
            if aliases_en.lower().strip() == claim_taxon_value.lower().strip():
                aliases_en = None
        else:
            aliases_en = None
        if 'es' in aliases:
            aliases_es = aliases['es'][0]['value']
            if aliases_es.lower().strip() == claim_taxon_value.lower().strip():
                aliases_es = None
        else:
            aliases_es = None
        ###
        labels_data = [
            {'language_code': 'en', 'language_name': 'English', 'language_value': labels_en},
        ]
        aliases_data = [
            {'language_code': 'en', 'language_name': 'English', 'language_value': aliases_en},
            {'language_code': 'es', 'language_name': 'Spanish', 'language_value': aliases_es},
        ]
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
