import os
import re
import json
import time
import shutil

from lib import g
from lib import io
from lib import llm

import normalize_utils

def normalize_plants():
    input_folderpath = f'{g.DATA_FOLDERPATH}/parse/drduke/json'
    output_folderpath = f'{g.DATA_FOLDERPATH}/normalize/drduke/json'
    try: shutil.rmtree(output_folderpath)
    except: pass
    os.makedirs(output_folderpath, exist_ok=True)
    ###
    input_filenames = os.listdir(input_folderpath)
    for i, input_filename in enumerate(input_filenames[:1]):
        print(f'{i}/{len(input_filenames)}')
        output_filepath = f'{output_folderpath}/{input_filename}'
        input_filepath = f'{input_folderpath}/{input_filename}'
        input_data = io.json_read(input_filepath)
        ###
        plant_name_latin = input_data['herb_name_latin']
        input_data['plant_name_normalized'] = normalize_utils.normalize_plant_name(plant_name_latin)
        ###
        if 'chemicals' in input_data:
            for chemical in input_data['chemicals']:
                chemical['chemical_name_normalized'] = normalize_utils.normalize_plant_name(chemical['Chemical Name'])
        ###
        if os.path.exists(output_filepath): continue
        io.json_write(output_filepath, input_data)
        print(json.dumps(input_data, indent=4))
    
def run():
    print('NORMALIZE >> drduke')

    start = time.perf_counter()
    normalize_plants()
    print(f'normalize plants() - execution time: ', time.perf_counter() - start)

