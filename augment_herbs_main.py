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

# model_filepath = '/home/ubuntu/vault-tmp/llm/gemma-4-26B-A4B-it-UD-Q4_K_XL.gguf'
model_filepath = '/home/ubuntu/vault-tmp/llm/gemma-4-26B-A4B-it-UD-Q4_K_M.gguf'

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
        print(f'AUGMENT {attribute.upper()} {i}/{len(master_items)}')
        plant_name_scientific_reference = master_item['plant_name_scientific_reference']
        ###
        input_data = io.json_read(f'{input_folderpath}/{plant_name_scientific_reference}.json')
        output_filepath = f'{output_folderpath}/{plant_name_scientific_reference}.json'
        io.json_write(output_filepath, input_data)
        if input_data != []:
            pass
            # print(json.dumps(input_data, indent=4))
            # quit()
    # TODO: pass through derive to render "reference name"
    #       if it works, augment

def augment_activities():
    input_folderpath = f'{HUB_FOLDERPATH}/derive/activities'
    output_folderpath = f'{HUB_FOLDERPATH}/augment/activities'
    # try: shutil.rmtree(output_folderpath)
    # except: pass
    io.folders_recursive_gen(output_folderpath)
    ###
    master_items = masterize_utils.masterize_plants_get_all()
    found_num = 0
    for i, master_item in enumerate(master_items[:]):
        print(f'AUGMENT ACTIVITIES {i}/{len(master_items)}')
        plant_name_scientific_reference = master_item['plant_name_scientific_reference']
        input_filepath = f'{input_folderpath}/{plant_name_scientific_reference}.json'
        output_filepath = f'{output_folderpath}/{plant_name_scientific_reference}.json'
        input_data = io.json_read(input_filepath)
        if input_data != []:
            found_num += 1
        # print(json.dumps(input_data, indent=4))
        # quit()
        ###
        # print(json.dumps(master_item, indent=4))
        if os.path.exists(output_filepath): continue
        if input_data != []:
            found_num += 1
            plant_name_scientific_reference = [item['plant_name_scientific_reference'] for item in input_data][0]
            activities = [item['activity_name_reference'] for item in input_data][:4]
            activities_prompt = ', '.join(activities)
            # print(plant_name_scientific_reference)
            # print(activities_prompt)
            # quit()
            ### activity_sources = activity_item['activity_sources']
            sentences_num = len(activities)
            prompt = f'''
                Write a {sentences_num}-sentence paragraph about the biological activities of the following plant: {plant_name_scientific_reference}.
                The biological activities of this plant are the following: {activities_prompt}.
                Reply only with the asked content.
                Start with the following words: {plant_name_scientific_reference} .
            '''.strip()
            # print(prompt)
            # quit()
            reply = llm.reply(prompt, model_filepath)
            if '</think>' in reply:
                reply = reply.split('</think>')[1].strip()
            reply = polish.vanilla(reply)
            print()
            print('########################################################################')
            print(reply)
            print('########################################################################')
            print()
            input_data = {
                'activities': input_data,
                'llm_intro': reply,
            }
        else: 
            input_data = {
                'activities': input_data,
                'llm_intro': '',
            }
        print(json.dumps(input_data, indent=4))
        io.json_write(output_filepath, input_data)
        # quit()
    print(found_num)

def augment_chemicals():
    input_folderpath = f'{HUB_FOLDERPATH}/derive/chemicals'
    output_folderpath = f'{HUB_FOLDERPATH}/augment/chemicals'
    # try: shutil.rmtree(output_folderpath)
    # except: pass
    io.folders_recursive_gen(output_folderpath)
    ###
    master_items = masterize_utils.masterize_plants_get_all()
    found_num = 0
    for i, master_item in enumerate(master_items[:]):
        print(f'AUGMENT CHEMICALS {i}/{len(master_items)}')
        plant_name_scientific_reference = master_item['plant_name_scientific_reference']
        input_filepath = f'{input_folderpath}/{plant_name_scientific_reference}.json'
        output_filepath = f'{output_folderpath}/{plant_name_scientific_reference}.json'
        input_data = io.json_read(input_filepath)
        if input_data != []:
            found_num += 1
            # print(json.dumps(input_data, indent=4))
            # quit()
        ###
        # print(json.dumps(master_item, indent=4))
        # print(json.dumps(input_data, indent=4))
        # quit()
        if os.path.exists(output_filepath): continue
        if input_data != []:
            found_num += 1
            plant_name_scientific_reference = [item['plant_name_scientific_reference'] for item in input_data][0]
            chemicals = [item['chemical_name_reference'] for item in input_data][:4]
            chemicals_prompt = ', '.join(chemicals)
            # quit()
            sentences_num = len(chemicals)
            prompt = f'''
                Write a {sentences_num}-sentence paragraph about the chemicals constituents of the following plant: {plant_name_scientific_reference}.
                The chemicals constituents of this plant are the following: {chemicals_prompt}.
                Reply only with the asked content.
                Start with the following words: {plant_name_scientific_reference} .
            '''.strip()
            # print(prompt)
            # quit()
            reply = llm.reply(prompt, model_filepath)
            if '</think>' in reply:
                reply = reply.split('</think>')[1].strip()
            reply = polish.vanilla(reply)
            print()
            print('########################################################################')
            print(reply)
            print('########################################################################')
            print()
            input_data = {
                'chemicals': input_data,
                'llm_intro': reply,
            }
        else: 
            input_data = {
                'chemicals': input_data,
                'llm_intro': '',
            }
        print(json.dumps(input_data, indent=4))
        io.json_write(output_filepath, input_data)
        # quit()
    print(found_num)

def augment_conditions():
    input_folderpath = f'{HUB_FOLDERPATH}/derive/conditions'
    output_folderpath = f'{HUB_FOLDERPATH}/augment/conditions'
    # try: shutil.rmtree(output_folderpath)
    # except: pass
    io.folders_recursive_gen(output_folderpath)
    ###
    master_items = masterize_utils.masterize_plants_get_all()
    found_num = 0
    for i, master_item in enumerate(master_items[:]):
        print(f'AUGMENT CONDITIONS {i}/{len(master_items)}')
        plant_name_scientific_reference = master_item['plant_name_scientific_reference']
        input_filepath = f'{input_folderpath}/{plant_name_scientific_reference}.json'
        output_filepath = f'{output_folderpath}/{plant_name_scientific_reference}.json'
        input_data = io.json_read(input_filepath)
        if input_data != []:
            found_num += 1
            # print(json.dumps(input_data, indent=4))
            # quit()
        ###
        # print(json.dumps(master_item, indent=4))
        # print(json.dumps(input_data, indent=4))
        # quit()
        if os.path.exists(output_filepath): continue
        if input_data != []:
            found_num += 1
            plant_name_scientific_reference = [item['plant_name_scientific_reference'] for item in input_data][0]
            conditions = [item['condition_name_reference'] for item in input_data][:4]
            conditions_prompt = ', '.join(conditions)
            # quit()
            sentences_num = len(conditions)
            prompt = f'''
                Write a {sentences_num}-sentence paragraph about the conditions treated with the following plant: {plant_name_scientific_reference}.
                The conditions treated with this plant are the following: {conditions_prompt}.
                Reply only with the asked content.
                Start with the following words: {plant_name_scientific_reference} .
            '''.strip()
            # print(prompt)
            # quit()
            reply = llm.reply(prompt, model_filepath)
            if '</think>' in reply:
                reply = reply.split('</think>')[1].strip()
            reply = polish.vanilla(reply)
            print()
            print('########################################################################')
            print(reply)
            print('########################################################################')
            print()
            input_data = {
                'conditions': input_data,
                'llm_intro': reply,
            }
        else: 
            input_data = {
                'conditions': input_data,
                'llm_intro': '',
            }
        print(json.dumps(input_data, indent=4))
        io.json_write(output_filepath, input_data)
        # quit()
    print(found_num)

def augment_plants_parts():
    input_folderpath = f'{HUB_FOLDERPATH}/derive/plants_parts'
    output_folderpath = f'{HUB_FOLDERPATH}/augment/plants_parts'
    # try: shutil.rmtree(output_folderpath)
    # except: pass
    io.folders_recursive_gen(output_folderpath)
    ###
    master_items = masterize_utils.masterize_plants_get_all()
    found_num = 0
    for i, master_item in enumerate(master_items[:]):
        print(f'AUGMENT PLANTS PARTS {i}/{len(master_items)}')
        plant_name_scientific_reference = master_item['plant_name_scientific_reference']
        input_filepath = f'{input_folderpath}/{plant_name_scientific_reference}.json'
        output_filepath = f'{output_folderpath}/{plant_name_scientific_reference}.json'
        input_data = io.json_read(input_filepath)
        if input_data != []:
            found_num += 1
            # print(json.dumps(input_data, indent=4))
            # quit()
        ###
        # print(json.dumps(master_item, indent=4))
        # print(json.dumps(input_data, indent=4))
        # quit()
        if os.path.exists(output_filepath): continue
        if input_data != []:
            found_num += 1
            plant_name_scientific_reference = [item['plant_name_scientific_reference'] for item in input_data][0]
            plants_parts = [item['plant_part_name_reference'] for item in input_data][:4]
            plants_parts_prompt = ', '.join(plants_parts)
            # quit()
            sentences_num = len(plants_parts)
            prompt = f'''
                Write a {sentences_num}-sentence paragraph about the medicinal plant parts of the following plant: {plant_name_scientific_reference}.
                The medicinal plant parts of this plant are the following: {plants_parts_prompt}.
                Reply only with the asked content.
                Start with the following words: {plant_name_scientific_reference} .
            '''.strip()
            # print(prompt)
            # quit()
            reply = llm.reply(prompt, model_filepath)
            if '</think>' in reply:
                reply = reply.split('</think>')[1].strip()
            reply = polish.vanilla(reply)
            print()
            print('########################################################################')
            print(reply)
            print('########################################################################')
            print()
            input_data = {
                'plants_parts': input_data,
                'llm_intro': reply,
            }
        else: 
            input_data = {
                'plants_parts': input_data,
                'llm_intro': '',
            }
        print(json.dumps(input_data, indent=4))
        io.json_write(output_filepath, input_data)
        # quit()
    print(found_num)

def run():

    # augment_copy(attribute='taxonomies')
    # augment_copy(attribute='diseases')

    augment_plants_parts()
    augment_conditions()
    augment_chemicals()
    augment_activities()

    # augment_copy(attribute='chemicals')

    augment_copy(attribute='taxonomies')

    augment_copy(attribute='synonyms')


    augment_copy(attribute='traits')
    augment_copy(attribute='distributions')
    augment_copy(attribute='names_common')
    augment_copy(attribute='preparations')
