import os
import json
import time
import shutil

import re
import unicodedata

from lib import g
from lib import io

import normalize_utils

HUB_FOLDERPATH = f'''{g.DATA_FOLDERPATH}/herbs'''

def normalize_format(name):
    spaces = re.compile(r"\s+")
    if not name: return None
    name = unicodedata.normalize("NFKC", name)
    name = name.lower()
    name = name.replace("-", " ")
    name = re.sub(r"[.,;:()]", "", name)
    name = spaces.sub(" ", name)
    return name.strip()

def normalize_condition_name(name):
    spaces = re.compile(r"\s+")
    if not name: return None
    name = unicodedata.normalize("NFKC", name)
    name = name.lower()
    name = name.replace("-", " ")
    name = re.sub(r"[.,;:()]", "", name)
    name = spaces.sub(" ", name)
    return name.strip()

def normalize_name_lvl1(name):
    spaces = re.compile(r"\s+")
    if not name: return None
    name = unicodedata.normalize("NFKC", name)
    name = name.lower()
    name = name.replace("-", " ")
    name = re.sub(r"[.,;:()]", "", name)
    name = spaces.sub(" ", name)
    return name.strip()

def normalize_plants_parts(source_foldername):
    input_folderpath = f'{HUB_FOLDERPATH}/parse/{source_foldername}/plants_parts/json'
    output_folderpath = f'{HUB_FOLDERPATH}/normalize/{source_foldername}/plants_parts/json'
    try: shutil.rmtree(output_folderpath)
    except: pass
    io.folders_recursive_gen(output_folderpath)
    input_filenames = os.listdir(input_folderpath)
    ###
    for i, input_filename in enumerate(input_filenames[:]):
        print(f'NORMALIZE PLANTS PARTS {i}/{len(input_filenames)}')
        output_filepath = f'{output_folderpath}/{input_filename}'
        if os.path.exists(output_filepath): continue
        ###
        input_filepath = f'{input_folderpath}/{input_filename}'
        input_data = io.json_read(input_filepath)
        for input_item in input_data:
            input_item['plant_name_raw_normalize'] = normalize_utils.normalize_plant_name(input_item['plant_name_raw'])
            input_item['plant_part_name_raw_normalize'] = normalize_utils.normalize_plant_part_name(input_item['plant_part_name_raw'])
            # print(json.dumps(input_item, indent=4))
            # quit()
        io.json_write(output_filepath, input_data)
    print(json.dumps(input_data[0], indent=4))
    # quit()

def normalize_plants_activities(source_foldername):
    input_folderpath = f'{HUB_FOLDERPATH}/parse/{source_foldername}/activities/json'
    output_folderpath = f'{HUB_FOLDERPATH}/normalize/{source_foldername}/activities/json'
    try: shutil.rmtree(output_folderpath)
    except: pass
    io.folders_recursive_gen(output_folderpath)
    input_filenames = os.listdir(input_folderpath)
    ###
    input_data_last_valid = []
    for i, input_filename in enumerate(input_filenames[:]):
        print(f'NORMALIZE PLANTS ACTIVITIES {i}/{len(input_filenames)}')
        output_filepath = f'{output_folderpath}/{input_filename}'
        if os.path.exists(output_filepath): continue
        ###
        input_filepath = f'{input_folderpath}/{input_filename}'
        input_data = io.json_read(input_filepath)
        # print(json.dumps(input_data, indent=4))
        # quit()
        for input_item in input_data:
            # print(json.dumps(input_item, indent=4))
            # quit()
            input_item['plant_name_normalize'] = normalize_utils.normalize_plant_name(input_item['plant_name_raw'])
            input_item['activity_name_normalize'] = normalize_utils.normalize_activity_name(input_item['activity_name_raw'])
            # print(json.dumps(input_item, indent=4))
            # quit()
        io.json_write(output_filepath, input_data)
        if input_data != []:
            input_data_last_valid = input_data
    print(json.dumps(input_data_last_valid, indent=4))
    # quit()

def normalize_plants_chemicals(source_foldername):
    input_folderpath = f'{HUB_FOLDERPATH}/parse/{source_foldername}/chemicals/json'
    output_folderpath = f'{HUB_FOLDERPATH}/normalize/{source_foldername}/chemicals/json'
    try: shutil.rmtree(output_folderpath)
    except: pass
    io.folders_recursive_gen(output_folderpath)
    input_filenames = os.listdir(input_folderpath)
    ###
    for i, input_filename in enumerate(input_filenames[:]):
        print(f'NORMALIZE PLANTS CHEMICALS {i}/{len(input_filenames)}')
        output_filepath = f'{output_folderpath}/{input_filename}'
        if os.path.exists(output_filepath): continue
        ###
        input_filepath = f'{input_folderpath}/{input_filename}'
        input_data = io.json_read(input_filepath)
        for input_item in input_data:
            input_item['plant_name_raw_normalize'] = normalize_utils.normalize_plant_name(input_item['plant_name_raw'])
            input_item['chemical_name_raw_normalize'] = normalize_utils.normalize_chemical_name(input_item['chemical_name_raw'])
            # print(json.dumps(normalized_item, indent=4))
            # quit()
        io.json_write(output_filepath, input_data)
    # print(json.dumps(input_data[0], indent=4))
    # quit()

def normalize_plants_conditions(source_foldername):
    input_folderpath = f'{HUB_FOLDERPATH}/parse/{source_foldername}/conditions/json'
    output_folderpath = f'{HUB_FOLDERPATH}/normalize/{source_foldername}/conditions/json'
    try: shutil.rmtree(output_folderpath)
    except: pass
    io.folders_recursive_gen(output_folderpath)
    input_filenames = os.listdir(input_folderpath)
    ###
    for i, input_filename in enumerate(input_filenames[:]):
        print(f'NORMALIZE PLANTS CONDITIONS - {i}/{len(input_filenames)}')
        output_filepath = f'{output_folderpath}/{input_filename}'
        if os.path.exists(output_filepath): continue
        ###
        input_filepath = f'{input_folderpath}/{input_filename}'
        input_data = io.json_read(input_filepath)
        for input_item in input_data:
            input_item['plant_name_raw_normalize'] = normalize_utils.normalize_plant_name(input_item['plant_name_raw'])
            input_item['condition_name_raw_normalize'] = normalize_condition_name(input_item['condition_name_raw'])
            # print(json.dumps(normalized_item, indent=4))
            # quit()
        io.json_write(output_filepath, input_data)
    print(json.dumps(input_data[0], indent=4))
    # quit()

def normalize_plants_compounds(source_foldername):
    input_folderpath = f'{HUB_FOLDERPATH}/parse/{source_foldername}/compounds/json'
    output_folderpath = f'{HUB_FOLDERPATH}/normalize/{source_foldername}/chemicals/json'
    try: shutil.rmtree(output_folderpath)
    except: pass
    io.folders_recursive_gen(output_folderpath)
    input_filenames = os.listdir(input_folderpath)
    ###
    for i, input_filename in enumerate(input_filenames[:]):
        print(f'NORMALIZE PLANTS COMPOUNDS {i}/{len(input_filenames)}')
        output_filepath = f'{output_folderpath}/{input_filename}'
        if os.path.exists(output_filepath): continue
        ###
        input_filepath = f'{input_folderpath}/{input_filename}'
        input_data = io.json_read(input_filepath)
        for input_item in input_data:
            input_item['plant_name_raw_normalize'] = normalize_utils.normalize_plant_name(input_item['plant_name_raw'])
            input_item['chemical_name_raw_normalize'] = normalize_utils.normalize_chemical_name(input_item['compound_name_raw'])
            # print(json.dumps(normalized_item, indent=4))
            # quit()
        io.json_write(output_filepath, input_data)
    print(json.dumps(input_data, indent=4))
    # quit()

def normalize_plants_synonyms(source_foldername):
    input_folderpath = f'{HUB_FOLDERPATH}/parse/{source_foldername}/synonyms/json'
    output_folderpath = f'{HUB_FOLDERPATH}/normalize/{source_foldername}/synonyms/json'
    try: shutil.rmtree(output_folderpath)
    except: pass
    io.folders_recursive_gen(output_folderpath)
    input_filenames = os.listdir(input_folderpath)
    ###
    output_items_last = []
    for i, input_filename in enumerate(input_filenames[:]):
        print(f'NORMALIZE PLANTS SYNONYMS {i}/{len(input_filenames)}')
        output_filepath = f'{output_folderpath}/{input_filename}'
        if os.path.exists(output_filepath): continue
        ###
        input_filepath = f'{input_folderpath}/{input_filename}'
        input_data = io.json_read(input_filepath)
        for input_item in input_data:
            input_item['plant_name_normalized'] = normalize_utils.normalize_plant_name(input_item['plant_name_raw'])
            input_item['plant_synonym_normalized'] = normalize_utils.normalize_plant_name(input_item['plant_synonym_raw'])
            # print(json.dumps(normalized_item, indent=4))
            # quit()
        io.json_write(output_filepath, input_data)
        if input_data != []: output_items_last = input_data
    print(json.dumps(output_items_last, indent=4))
    # quit()

def normalize_plants_taxonomies(source_foldername):
    input_folderpath = f'{HUB_FOLDERPATH}/parse/{source_foldername}/taxonomies/json'
    output_folderpath = f'{HUB_FOLDERPATH}/normalize/{source_foldername}/taxonomies/json'
    try: shutil.rmtree(output_folderpath)
    except: pass
    io.folders_recursive_gen(output_folderpath)
    input_filenames = os.listdir(input_folderpath)
    ###
    output_items_last = []
    for i, input_filename in enumerate(input_filenames[:]):
        print(f'NORMALIZE PLANTS TAXONOMIES {i}/{len(input_filenames)}')
        output_filepath = f'{output_folderpath}/{input_filename}'
        if os.path.exists(output_filepath): continue
        ###
        input_filepath = f'{input_folderpath}/{input_filename}'
        input_data = io.json_read(input_filepath)
        ### TEMP?
        input_data = [input_data]
        # print(json.dumps(input_data, indent=4))
        # quit()
        for input_item in input_data:
            input_item['plant_name_scientific_raw_normalize'] = normalize_utils.normalize_plant_name(input_item['name'])
            # print(json.dumps(normalized_item, indent=4))
            # quit()
        io.json_write(output_filepath, input_data)
        if input_data != []: output_items_last = input_data
    print(json.dumps(output_items_last, indent=4))
    # quit()

def normalize_plants_common_names(source_foldername):
    input_folderpath = f'{HUB_FOLDERPATH}/parse/{source_foldername}/names/json'
    output_folderpath = f'{HUB_FOLDERPATH}/normalize/{source_foldername}/names/json'
    try: shutil.rmtree(output_folderpath)
    except: pass
    io.folders_recursive_gen(output_folderpath)
    input_filenames = os.listdir(input_folderpath)
    ###
    for i, input_filename in enumerate(input_filenames[:]):
        print(f'NORMALIZE PLANTS COMMON NAMES {i}/{len(input_filenames)}')
        output_filepath = f'{output_folderpath}/{input_filename}'
        if os.path.exists(output_filepath): continue
        ###
        input_filepath = f'{input_folderpath}/{input_filename}'
        input_data = io.json_read(input_filepath)
        for input_item in input_data:
            input_item['plant_name_scientific_reference_normalize'] = normalize_utils.normalize_plant_name(input_item['plant_name_scientific_reference'])
            # print(json.dumps(input_item, indent=4))
            # quit()
        io.json_write(output_filepath, input_data)
    print(json.dumps(input_item, indent=4))
    # quit()

def normalize_plants_distributions(source_foldername):
    input_folderpath = f'{HUB_FOLDERPATH}/parse/{source_foldername}/distributions/json'
    output_folderpath = f'{HUB_FOLDERPATH}/normalize/{source_foldername}/distributions/json'
    try: shutil.rmtree(output_folderpath)
    except: pass
    io.folders_recursive_gen(output_folderpath)
    input_filenames = os.listdir(input_folderpath)
    ###
    for i, input_filename in enumerate(input_filenames[:]):
        print(f'NORMALIZE PLANTS DISTRIBUTIONS {i}/{len(input_filenames)}')
        output_filepath = f'{output_folderpath}/{input_filename}'
        if os.path.exists(output_filepath): continue
        ###
        input_filepath = f'{input_folderpath}/{input_filename}'
        input_data = io.json_read(input_filepath)
        for input_item in input_data:
            input_item['plant_name_scientific_reference_normalize'] = normalize_utils.normalize_plant_name(input_item['plant_name_scientific_reference'])
            input_item['locality_continent_normalize'] = normalize_utils.normalize_plant_name(input_item['locality_continent'])
            input_item['locality_region_normalize'] = normalize_utils.normalize_plant_name(input_item['locality_region'])
            input_item['locality_area_normalize'] = normalize_utils.normalize_plant_name(input_item['locality_area'])
            # print(json.dumps(input_item, indent=4))
            # quit()
        io.json_write(output_filepath, input_data)
    print(json.dumps(input_item, indent=4))
    # quit()

def normalize_plants_traits(source_foldername):
    input_folderpath = f'{HUB_FOLDERPATH}/parse/{source_foldername}/traits/json'
    output_folderpath = f'{HUB_FOLDERPATH}/normalize/{source_foldername}/traits/json'
    try: shutil.rmtree(output_folderpath)
    except: pass
    io.folders_recursive_gen(output_folderpath)
    input_filenames = os.listdir(input_folderpath)
    ###
    for i, input_filename in enumerate(input_filenames[:]):
        print(f'NORMALIZE PLANTS TRAITS {i}/{len(input_filenames)}')
        output_filepath = f'{output_folderpath}/{input_filename}'
        if os.path.exists(output_filepath): continue
        ### COPY FOLDER
        input_filepath = f'{input_folderpath}/{input_filename}'
        input_data = io.json_read(input_filepath)
        for input_item in input_data:
            input_item['plant_name_scientific_reference_normalize'] = normalize_utils.normalize_plant_name(input_item['plant_name_scientific_reference'])
            # print(json.dumps(input_item, indent=4))
            # quit()
        io.json_write(output_filepath, input_data)
    print(json.dumps(input_item, indent=4))

def normalize_plants_preparations(source_foldername):
    input_folderpath = f'{HUB_FOLDERPATH}/parse/{source_foldername}/preparations/json'
    output_folderpath = f'{HUB_FOLDERPATH}/normalize/{source_foldername}/preparations/json'
    try: shutil.rmtree(output_folderpath)
    except: pass
    io.folders_recursive_gen(output_folderpath)
    input_filenames = os.listdir(input_folderpath)
    ###
    for i, input_filename in enumerate(input_filenames[:]):
        print(f'NORMALIZE PLANTS PREPARATIONS - {i}/{len(input_filenames)}')
        output_filepath = f'{output_folderpath}/{input_filename}'
        if os.path.exists(output_filepath): continue
        ###
        input_filepath = f'{input_folderpath}/{input_filename}'
        input_data = io.json_read(input_filepath)
        for input_item in input_data:
            input_item['plant_name_raw_normalize'] = normalize_utils.normalize_plant_name(input_item['plant_name_raw'])
            input_item['preparation_name_raw_normalize'] = normalize_name_lvl1(input_item['preparation_name_raw'])
            # print(json.dumps(input_item, indent=4))
            # quit()
        io.json_write(output_filepath, input_data)
    print(json.dumps(input_data[0], indent=4))
    # quit()

def normalize_gen(entity_1, entity_2, source_foldername, output_foldername):
    input_folderpath = f'{HUB_FOLDERPATH}/parse/{source_foldername}/{output_foldername}/json'
    output_folderpath = f'{HUB_FOLDERPATH}/normalize/{source_foldername}/{output_foldername}/json'
    try: shutil.rmtree(output_folderpath)
    except: pass
    io.folders_recursive_gen(output_folderpath)
    input_filenames = os.listdir(input_folderpath)
    ###
    for i, input_filename in enumerate(input_filenames[:]):
        print(f'NORMALIZE {entity_1} {entity_2} - {i}/{len(input_filenames)}')
        output_filepath = f'{output_folderpath}/{input_filename}'
        if os.path.exists(output_filepath): continue
        ###
        input_filepath = f'{input_folderpath}/{input_filename}'
        input_data = io.json_read(input_filepath)
        for input_item in input_data:
            # print(json.dumps(input_item, indent=4))
            input_item[f'{entity_1}_raw_normalize'] = normalize_utils.normalize_plant_name(input_item[f'{entity_1}_raw'])
            input_item[f'{entity_2}_raw_normalize'] = normalize_format(input_item[f'{entity_2}_raw'])
            # print(json.dumps(input_item, indent=4))
            # quit()
        io.json_write(output_filepath, input_data)
    print(json.dumps(input_data[0], indent=4))
    # quit()

def run():
    print('NORMALIZE >> MAIN')

    normalize_gen('plant_name_scientific', 'compound_name', 'pubmed', 'compounds')
    normalize_gen('plant_name_scientific', 'preparation_name', 'pubmed', 'preparations')
    normalize_gen('plant_name_scientific', 'plant_part_name', 'pubmed', 'plants_parts')
    normalize_gen('plant_name_scientific', 'condition_name', 'pubmed', 'conditions')
    normalize_gen('plant_name_scientific', 'activity_name', 'pubmed', 'activities')
    normalize_gen('plant_name_scientific', 'plant_name_common', 'col', 'plants_names_common')

    normalize_plants_synonyms(source_foldername='wcvp')
    normalize_plants_synonyms(source_foldername='wcvp')
    normalize_plants_taxonomies(source_foldername='powo')
    normalize_plants_distributions(source_foldername='wcvp')
    normalize_plants_traits(source_foldername='gift')

    # quit()

    # normalize_plants_chemicals(source_foldername='drduke')
    # normalize_plants_chemicals(source_foldername='pubmed')
    # normalize_plants_activities(source_foldername='drduke')

    # normalize_plants_common_names(source_foldername='col')




