import os
import json
import time
import shutil

from lib import g
from lib import io

HUB_FOLDERPATH = f'{g.DATA_FOLDERPATH}/organizations' 

import masterize_organizations_utils

def compile_gen():
    input_foldername = f'augment'
    output_foldername = f'compile'
    input_folderpath = f'{HUB_FOLDERPATH}/{input_foldername}'
    output_folderpath = f'{HUB_FOLDERPATH}/{output_foldername}'
    io.folders_recursive_gen(output_folderpath)
    input_filenames = os.listdir(input_folderpath)
    ###
    i = 0

    items = masterize_organizations_utils.masterize_organizations_get_all()
    for i, item in enumerate(items):
        print(f'{i}/{len(items)}')
        business_name_canonical = item['business_name_canonical']
        output_data = {}
        output_data['business_name_canonical'] = business_name_canonical

        output_data['identity'] = io.json_read(
            f'{input_folderpath}/identity/{business_name_canonical}.json'
        )

        print(json.dumps(output_data, indent=4))

        output_filepath = f'{output_folderpath}/{business_name_canonical}.json'
        io.json_write(output_filepath, output_data)

def run():
    start = time.perf_counter()
    compile_gen()
    print(f'compile_gen() - execution time: ', time.perf_counter() - start)

