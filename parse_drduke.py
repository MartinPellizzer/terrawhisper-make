import os
import time
import json
import shutil

from lib import g
from lib import io
from lib import llm

import parse_utils

def parse_activities():
    input_folderpath = f'{g.DATA_FOLDERPATH}/fetch/drduke/json'
    output_folderpath = f'{g.DATA_FOLDERPATH}/parse/drduke/activities/json'
    try: shutil.rmtree(output_folderpath)
    except: pass
    os.makedirs(output_folderpath, exist_ok=True)
    ###
    input_filenames = os.listdir(input_folderpath)
    for i, input_filename in enumerate(input_filenames[:]):
        print(f'{i}/{len(input_filenames)}')
        output_filepath = f'{output_folderpath}/{input_filename}'
        input_filepath = f'{input_folderpath}/{input_filename}'
        if os.path.exists(output_filepath): continue
        data = io.json_read(input_filepath)
        # print(json.dumps(data, indent=4))
        # quit()
        ###
        items_output = []
        if 'activities' in data:
            for item in data['activities']:
                # print(json.dumps(item, indent=4))
                # quit()
                item_output = parse_utils.activity_create(
                    plant_name_raw = data['herb_name_latin'], 
                    activity_name_raw = item['Activity'], 
                    source_name = 'Dr. Duke',
                    source_acronym = '',
                    reference_name = item['Reference'],
                )
                items_output.append(item_output)
                # print(json.dumps(item_output, indent=4))
                # quit()
        io.json_write(output_filepath, items_output)
        # shutil.copy(input_filepath, output_filepath)
        # print(input_filename)
    

def parse_chemicals():
    input_folderpath = f'{g.DATA_FOLDERPATH}/fetch/drduke/json'
    output_folderpath = f'{g.DATA_FOLDERPATH}/parse/drduke/chemicals/json'
    try: shutil.rmtree(output_folderpath)
    except: pass
    os.makedirs(output_folderpath, exist_ok=True)
    ###
    input_filenames = os.listdir(input_folderpath)
    for i, input_filename in enumerate(input_filenames[:]):
        print(f'{i}/{len(input_filenames)}')
        output_filepath = f'{output_folderpath}/{input_filename}'
        input_filepath = f'{input_folderpath}/{input_filename}'
        if os.path.exists(output_filepath): continue
        data = io.json_read(input_filepath)
        # print(json.dumps(data, indent=4))
        # quit()
        ###
        items_output = []
        if 'chemicals' in data:
            for item in data['chemicals']:
                item_output = parse_utils.chemical_create(
                    plant_name_raw = data['herb_name_latin'], 
                    chemical_name_raw = item['Chemical Name'], 
                    plant_part_name_raw = item['Plant Part'], 
                    source_id = '', 
                    source_name = item['Reference'],
                )
                items_output.append(item_output)
                # print(json.dumps(item_output, indent=4))
                # quit()
        io.json_write(output_filepath, items_output)
        # shutil.copy(input_filepath, output_filepath)
        # print(input_filename)
    

def run():
    print('PARSE >> drduke')

    start = time.perf_counter()
    parse_activities()
    print(f'parse activities() - execution time: ', time.perf_counter() - start)

    start = time.perf_counter()
    parse_chemicals()
    print(f'parse chemicals() - execution time: ', time.perf_counter() - start)

