import os
import json
import time
import shutil

import re
import unicodedata

from lib import g
from lib import io

import normalize_utils

HUB_FOLDERPATH = f'{g.DATA_FOLDERPATH}/organizations'

def resolve_businesses(source_foldername):
    input_folderpath = f'{HUB_FOLDERPATH}/normalize/{source_foldername}/json'
    output_folderpath = f'{HUB_FOLDERPATH}/resolve/{source_foldername}/json'
    try: shutil.rmtree(output_folderpath)
    except: pass
    io.folders_recursive_gen(output_folderpath)
    input_filenames = os.listdir(input_folderpath)
    ###
    for i, input_filename in enumerate(input_filenames[:]):
        print(f'{i}/{len(input_filenames)}')
        output_filepath = f'{output_folderpath}/{input_filename}'
        if os.path.exists(output_filepath): continue
        ###
        input_filepath = f'{input_folderpath}/{input_filename}'
        input_data = io.json_read(input_filepath)
        ###
        resolved_data = []
        for input_item in input_data:
            business_name_normalize = input_item['business_name_normalize']
            input_item['business_name_canonical'] = business_name_normalize
            resolved_data.append(input_item)
            # print(json.dumps(input_item, indent=4))
            # quit()
        if resolved_data != []:
            io.json_write(output_filepath, resolved_data)

def run():
    print('NORMALIZE >> MAIN')

    if 1:
        start = time.perf_counter()
        resolve_businesses(source_foldername='gmap')
        resolve_businesses(source_foldername='website')
        print(f'resolve businesses() - execution time: ', time.perf_counter() - start)
