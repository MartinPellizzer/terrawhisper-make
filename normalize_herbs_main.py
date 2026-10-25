import os
import json
import time
import shutil

import re
import unicodedata

from lib import g
from lib import io

import normalize_utils
import schema_herbs

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
    input_folderpath = f'{HUB_FOLDERPATH}/parse/{source_foldername}/plants_plants_parts/json'
    output_folderpath = f'{HUB_FOLDERPATH}/normalize/{source_foldername}/plants_plants_parts/json'
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
            input_item['plant_name_scientific_raw_normalize'] = normalize_utils.normalize_plant_name(input_item['plant_name_scientific_raw'])
            input_item['plant_part_name_raw_normalize'] = normalize_utils.normalize_plant_part_name(input_item['plant_part_name_raw'])
        io.json_write(output_filepath, input_data)
    print(json.dumps(input_data[0], indent=4))
    # quit()

def normalize_activities(source_foldername):
    input_folderpath = f'{HUB_FOLDERPATH}/parse/{source_foldername}/plants_activities/json'
    output_folderpath = f'{HUB_FOLDERPATH}/normalize/{source_foldername}/plants_activities/json'
    try: shutil.rmtree(output_folderpath)
    except: pass
    io.folders_recursive_gen(output_folderpath)
    input_filenames = os.listdir(input_folderpath)
    ###
    for i, input_filename in enumerate(input_filenames[:]):
        print(f'NORMALIZE plants plants_activities {i}/{len(input_filenames)}')
        output_filepath = f'{output_folderpath}/{input_filename}'
        if os.path.exists(output_filepath): continue
        ###
        input_filepath = f'{input_folderpath}/{input_filename}'
        input_data = io.json_read(input_filepath)
        for input_item in input_data:
            input_item['plant_name_scientific_raw_normalize'] = normalize_utils.normalize_plant_name(input_item['plant_name_scientific_raw'])
            input_item['activity_name_raw_normalize'] = normalize_format(input_item['activity_name_raw'])
        io.json_write(output_filepath, input_data)
    print(json.dumps(input_data[0], indent=4))
    # quit()

def normalize_compounds(source_foldername):
    input_folderpath = f'{HUB_FOLDERPATH}/parse/{source_foldername}/plants_compounds/json'
    output_folderpath = f'{HUB_FOLDERPATH}/normalize/{source_foldername}/plants_compounds/json'
    try: shutil.rmtree(output_folderpath)
    except: pass
    io.folders_recursive_gen(output_folderpath)
    input_filenames = os.listdir(input_folderpath)
    ###
    for i, input_filename in enumerate(input_filenames[:]):
        print(f'NORMALIZE plants plants_compounds {i}/{len(input_filenames)}')
        output_filepath = f'{output_folderpath}/{input_filename}'
        if os.path.exists(output_filepath): continue
        ###
        input_filepath = f'{input_folderpath}/{input_filename}'
        input_data = io.json_read(input_filepath)
        for input_item in input_data:
            input_item['plant_name_scientific_raw_normalize'] = normalize_utils.normalize_plant_name(input_item['plant_name_scientific_raw'])
            input_item['compound_name_raw_normalize'] = normalize_format(input_item['compound_name_raw'])
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

def schema_normalize_gen(schema_item):
    schema_table_name = schema_item['table_name']
    schema_source_name = schema_item['sources'][0]['source_name']
    schema_output_foldername = schema_table_name
    schema_entity_1_val = schema_item['fields'][0]['field_name']
    schema_relationship_val = schema_item['fields'][1]['field_name']
    schema_entity_2_val = schema_item['fields'][2]['field_name']
    ###
    input_folderpath = f'{HUB_FOLDERPATH}/parse/{schema_source_name}/{schema_output_foldername}/json'
    output_folderpath = f'{HUB_FOLDERPATH}/normalize/{schema_source_name}/{schema_output_foldername}/json'
    if schema_item['regen'] == True:
        try: shutil.rmtree(output_folderpath)
        except: pass
    io.folders_recursive_gen(output_folderpath)
    input_filenames = os.listdir(input_folderpath)
    ###
    last = []
    for i, input_filename in enumerate(input_filenames[:]):
        print(f'NORMALIZE {schema_entity_1_val} {schema_entity_2_val} - {i}/{len(input_filenames)}')
        output_filepath = f'{output_folderpath}/{input_filename}'
        if os.path.exists(output_filepath): continue
        ###
        input_filepath = f'{input_folderpath}/{input_filename}'
        input_data = io.json_read(input_filepath)
        for input_item in input_data:
            # print(json.dumps(input_item, indent=4))
            input_item[f'{schema_entity_1_val}_raw_normalize'] = normalize_utils.normalize_plant_name(input_item[f'{schema_entity_1_val}_raw'])
            input_item[f'{schema_entity_2_val}_raw_normalize'] = normalize_format(input_item[f'{schema_entity_2_val}_raw'])
            # print(json.dumps(input_item, indent=4))
            # quit()
        io.json_write(output_filepath, input_data)
        if input_data != []:
            last = input_data
    print(json.dumps(last, indent=4))
    # quit()

def plants_normalize(source_foldername):
    input_folderpath = f'{HUB_FOLDERPATH}/parse/{source_foldername}/plants/json'
    output_folderpath = f'{HUB_FOLDERPATH}/normalize/{source_foldername}/plants/json'
    try: shutil.rmtree(output_folderpath)
    except: pass
    io.folders_recursive_gen(output_folderpath)
    input_filenames = os.listdir(input_folderpath)
    ###
    for i, input_filename in enumerate(input_filenames[:]):
        print(f'NORMALIZE HERBS plants {i}/{len(input_filenames)}')
        output_filepath = f'{output_folderpath}/{input_filename}'
        if os.path.exists(output_filepath): continue
        ###
        input_filepath = f'{input_folderpath}/{input_filename}'
        input_data = io.json_read(input_filepath)
        for input_item in input_data:
            input_item['plant_name_scientific_raw_normalize'] = normalize_utils.normalize_plant_name(input_item['plant_name_scientific_raw'])
        io.json_write(output_filepath, input_data)
    print(json.dumps(input_data[0], indent=4))
    # quit()

def activities_normalize(source_foldername):
    input_folderpath = f'{HUB_FOLDERPATH}/parse/{source_foldername}/activities/json'
    output_folderpath = f'{HUB_FOLDERPATH}/normalize/{source_foldername}/activities/json'
    try: shutil.rmtree(output_folderpath)
    except: pass
    io.folders_recursive_gen(output_folderpath)
    input_filenames = os.listdir(input_folderpath)
    ###
    for i, input_filename in enumerate(input_filenames[:]):
        print(f'NORMALIZE HERBS activities {i}/{len(input_filenames)}')
        output_filepath = f'{output_folderpath}/{input_filename}'
        if os.path.exists(output_filepath): continue
        ###
        input_filepath = f'{input_folderpath}/{input_filename}'
        input_data = io.json_read(input_filepath)
        for input_item in input_data:
            input_item['activity_name_raw_normalize'] = normalize_format(input_item['activity_name_raw'])
        io.json_write(output_filepath, input_data)
    print(json.dumps(input_data[0], indent=4))
    # quit()

def studies_normalize(source_foldername):
    input_folderpath = f'{HUB_FOLDERPATH}/parse/{source_foldername}/studies/json'
    output_folderpath = f'{HUB_FOLDERPATH}/normalize/{source_foldername}/studies/json'
    try: shutil.rmtree(output_folderpath)
    except: pass
    io.folders_recursive_gen(output_folderpath)
    input_filenames = os.listdir(input_folderpath)
    ###
    for i, input_filename in enumerate(input_filenames[:]):
        print(f'NORMALIZE HERBS studies {i}/{len(input_filenames)}')
        output_filepath = f'{output_folderpath}/{input_filename}'
        if os.path.exists(output_filepath): continue
        ###
        input_filepath = f'{input_folderpath}/{input_filename}'
        input_data = io.json_read(input_filepath)
        for input_item in input_data:
            # print(input_item)
            input_item['study_title_raw_normalize'] = normalize_format(input_item['study_title_raw'])
        io.json_write(output_filepath, input_data)
    print(json.dumps(input_data[0], indent=4))
    # quit()

def plants_activities_normalize(source_foldername):
    input_folderpath = f'{HUB_FOLDERPATH}/parse/{source_foldername}/plants_activities/json'
    output_folderpath = f'{HUB_FOLDERPATH}/normalize/{source_foldername}/plants_activities/json'
    try: shutil.rmtree(output_folderpath)
    except: pass
    io.folders_recursive_gen(output_folderpath)
    input_filenames = os.listdir(input_folderpath)
    ###
    for i, input_filename in enumerate(input_filenames[:]):
        print(f'NORMALIZE HERBS plants_activities {i}/{len(input_filenames)}')
        output_filepath = f'{output_folderpath}/{input_filename}'
        if os.path.exists(output_filepath): continue
        ###
        input_filepath = f'{input_folderpath}/{input_filename}'
        input_data = io.json_read(input_filepath)
        for input_item in input_data:
            input_item['plant_name_scientific_raw_normalize'] = normalize_utils.normalize_plant_name(input_item['plant_name_scientific_raw'])
            input_item['activity_name_raw_normalize'] = normalize_format(input_item['activity_name_raw'])
        io.json_write(output_filepath, input_data)
    print(json.dumps(input_data[0], indent=4))
    # quit()

def run():
    print('NORMALIZE >> MAIN')

    ### ENTITIES
    studies_normalize(source_foldername='pubmed')
    return
    # plants_normalize(source_foldername='pubmed')
    # activities_normalize(source_foldername='pubmed')

    ### ASSERTIONS
    plants_activities_normalize(source_foldername='pubmed')
    return
    quit()

    if 0:
        normalize_activities('pubmed')
        normalize_plants_parts('pubmed')
        normalize_compounds('pubmed')

    schema_items = schema_herbs.data['items']
    for schema_item in schema_items: 
        if schema_item['process'] != True: continue
        if schema_item['table_name'] == 'plants_activities': continue
        if schema_item['table_name'] == 'plants_plants_parts': continue
        if schema_item['table_name'] == 'plants_compounds': continue
        schema_normalize_gen(schema_item)
    # quit()

    if 0:
        # normalize_gen('plant_name_scientific', 'preparation_name', 'pubmed', 'preparations')
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




