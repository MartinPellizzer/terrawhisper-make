
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

model_filepath = '/home/ubuntu/vault-tmp/llm/gemma-4-26B-A4B-it-UD-Q4_K_XL.gguf'

HUB_FOLDERPATH = f'{g.DATA_FOLDERPATH}/organizations' 

def observations_get_all():
    db_filepath = f'{HUB_FOLDERPATH}/observe/observations.db'
    conn = sqlite3.connect(db_filepath)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    rows = cur.execute(f'SELECT * FROM organizations').fetchall()
    dict_rows = [dict(row) for row in rows]
    conn.close()
    return dict_rows

def augment_organizations():
    section_foldername = 'identity'
    input_folderpath = f'{HUB_FOLDERPATH}/derive/{section_foldername}'
    output_folderpath = f'{HUB_FOLDERPATH}/augment/{section_foldername}'
    try: shutil.rmtree(output_folderpath)
    except: pass
    io.folders_recursive_gen(output_folderpath)
    ###
    items = observations_get_all()
    for i, item in enumerate(items):
        print(f'{i}/{len(items)}')
        business_name_official = item['business_name_official']
        input_data = io.json_read(f'{HUB_FOLDERPATH}/derive/{section_foldername}/{business_name_official}.json')
        output_filepath = f'{HUB_FOLDERPATH}/augment/{section_foldername}/{business_name_official}.json'
        ###
        if os.path.exists(output_filepath): output_data = io.json_read(output_filepath)
        else: output_data = input_data
        for output_item in output_data:
            # print(output_data)
            # quit()
            ###
            key = 'llm'
            prompt = f'''
                I'm writing an article about the following business: {business_name_official}. 
                Write a detailed description focusing only on the following section: {section_foldername}.
                Use the following data to write the description: {output_data}.
                Reply in a paragraph.
                Write only in english, translate from other languages if necessary.
                Start with the following words: {business_name_official} is .
            '''.strip()
            print(prompt)
            reply = llm.reply(prompt, model_filepath)
            if '</think>' in reply:
                reply = reply.split('</think>')[1].strip()
            reply = polish.vanilla(reply)
            print('########################################################################')
            print(reply)
            print('########################################################################')
            output_item[key] = reply
            io.json_write(output_filepath, output_data)
            print(output_data)
            # quit()

    quit()
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

def gen():
    augment_organizations()
