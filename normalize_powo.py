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
    source_foldername = 'powo'
    input_foldername = 'parse'
    output_foldername = 'normalize'
    ###
    input_folderpath = f'{g.DATA_FOLDERPATH}/{input_foldername}/{source_foldername}/json'
    output_folderpath = f'{g.DATA_FOLDERPATH}/{output_foldername}/{source_foldername}/json'
    io.folders_recursive_gen(output_folderpath)
    input_filenames = os.listdir(input_folderpath)
    i = 0
    for input_filename in input_filenames[i:]:
        i += 1
        print(f'{i}/{len(input_filenames)}')
        input_filepath = f'{input_folderpath}/{input_filename}'
        input_data = io.json_read(input_filepath)
        taxon_name = input_data["name"]
        taxon_name_normalized = normalize_utils.normalize_plant_name(taxon_name)
        input_data['taxon_name'] = taxon_name
        input_data['taxon_name_normalized'] = taxon_name_normalized
        output_filepath = f'{output_folderpath}/{taxon_name_normalized}.json'
        # print(json.dumps(input_data, indent=4))
        # quit()
        io.json_write(output_filepath, input_data)
        # quit()

def run():
    print('NORMALIZE >> powo')

    start = time.perf_counter()
    normalize_plants()
    print(f'normalize plants() - execution time: ', time.perf_counter() - start)

