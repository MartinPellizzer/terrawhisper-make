import os
import json
import sqlite3
import shutil

from lib import g
from lib import io
from lib import llm
from lib import data
from lib import polish

import masterize_utils

HUB_FOLDERPATH = f'''{g.DATA_FOLDERPATH}/herbs'''

model_filepath = '/home/ubuntu/vault-tmp/llm/gemma-4-26B-A4B-it-UD-Q4_K_XL.gguf'

def augment_traits():
    input_folderpath = f'{HUB_FOLDERPATH}/derive/herbs/traits'
    output_folderpath = f'{HUB_FOLDERPATH}/augment/herbs/traits'
    try: shutil.rmtree(output_folderpath)
    except: pass
    io.folders_recursive_gen(output_folderpath)
    ###
    plants_rows = masterize_utils.masterize_plants_get_all()
    for i, plant_row in enumerate(plants_rows):
        print(f'{i}/{len(plants_rows)}')
        plant_name_scientific_canon = plant_row[1]
        ###
        input_data = io.json_read(f'{g.DATA_FOLDERPATH}/derive/herbs/traits/{plant_name_scientific_canon}.json')
        output_filepath = f'{g.DATA_FOLDERPATH}/augment/herbs/traits/{plant_name_scientific_canon}.json'
        if os.path.exists(output_filepath): output_data = io.json_read(output_filepath)
        else: output_data = input_data
        ###
        for trait_item in input_data:
            trait_category = trait_item['trait_category']
            traits = trait_item['traits']
            key = 'llm'
            ###
            prompt = f'''
                Write a detailed description about the {trait_category} of the following medicinal plant: {plant_name_scientific_canon}.
                Include the following traits and data: {traits}.
                Reply in a paragraph.
                Don't explain or define what the plant is, just start the reply by discussing directly the {trait_category}.
            '''.strip()
                # Start the reply with the following words: {plant_name_common}, scientifically known as {plant_name}, is
            print(prompt)
            reply = llm.reply(prompt, model_filepath)
            if '</think>' in reply:
                reply = reply.split('</think>')[1].strip()
            reply = polish.vanilla(reply)
            print('########################################################################')
            print(reply)
            print('########################################################################')
            trait_item[key] = reply
            io.json_write(output_filepath, output_data)
            
            print(trait_item)
        # quit()
        # print(json.dumps(input_data, indent=4))
        # quit()
        ###

def augment_copy(attribute):
    input_folderpath = f'{HUB_FOLDERPATH}/derive/{attribute}'
    output_folderpath = f'{HUB_FOLDERPATH}/augment/{attribute}'
    try: shutil.rmtree(output_folderpath)
    except: pass
    io.folders_recursive_gen(output_folderpath)
    ###
    master_items = masterize_utils.masterize_plants_get_all()
    for i, master_item in enumerate(master_items):
        print(f'{i}/{len(master_items)}')
        plant_name_scientific_reference = master_item['plant_name_scientific_reference']
        ###
        input_data = io.json_read(f'{input_folderpath}/{plant_name_scientific_reference}.json')
        output_filepath = f'{output_folderpath}/{plant_name_scientific_reference}.json'
        io.json_write(output_filepath, input_data)

def run():
    # augment_traits()

    # augment_copy(attribute='synonyms')
    # augment_copy(attribute='taxonomies')
    # augment_copy(attribute='distribution')
    # augment_copy(attribute='plants_parts')
    # augment_copy(attribute='diseases')
    # augment_copy(attribute='preparations')

    augment_copy(attribute='names_common')
    augment_copy(attribute='activities')
    augment_copy(attribute='chemicals')
