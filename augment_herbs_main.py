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
import schema_herbs
import sql

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

def augment_compounds():
    input_folderpath = f'{HUB_FOLDERPATH}/derive/compounds'
    output_folderpath = f'{HUB_FOLDERPATH}/augment/compounds'
    # try: shutil.rmtree(output_folderpath)
    # except: pass
    io.folders_recursive_gen(output_folderpath)
    ###
    master_items = masterize_utils.masterize_plants_get_all()
    found_num = 0
    for i, master_item in enumerate(master_items[:]):
        print(f'AUGMENT compounds {i}/{len(master_items)}')
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
            compounds = [item['compound_name_reference'] for item in input_data][:4]
            compounds_prompt = ', '.join(compounds)
            # quit()
            sentences_num = len(compounds)
            prompt = f'''
                Write a {sentences_num}-sentence paragraph about the compounds of the following plant: {plant_name_scientific_reference}.
                The compounds of this plant are the following: {compounds_prompt}.
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
                'compounds': input_data,
                'llm_intro': reply,
            }
        else: 
            input_data = {
                'compounds': input_data,
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

def augment_preparations():
    input_folderpath = f'{HUB_FOLDERPATH}/derive/preparations'
    output_folderpath = f'{HUB_FOLDERPATH}/augment/preparations'
    # try: shutil.rmtree(output_folderpath)
    # except: pass
    io.folders_recursive_gen(output_folderpath)
    ###
    master_items = masterize_utils.masterize_plants_get_all()
    found_num = 0
    for i, master_item in enumerate(master_items[:]):
        print(f'AUGMENT PREPARATIONS {i}/{len(master_items)}')
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
            preparations = [item['preparation_name_reference'] for item in input_data][:4]
            preparations_prompt = ', '.join(preparations)
            # quit()
            sentences_num = len(preparations)
            prompt = f'''
                Write a {sentences_num}-sentence paragraph about the preparations of the following plant: {plant_name_scientific_reference}.
                The preparations of this plant are the following: {preparations_prompt}.
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
                'preparations': input_data,
                'llm_intro': reply,
            }
        else: 
            input_data = {
                'preparations': input_data,
                'llm_intro': '',
            }
        print(json.dumps(input_data, indent=4))
        io.json_write(output_filepath, input_data)
        # quit()
    print(found_num)

def augment_intro():
    input_preparations_folderpath = f'{HUB_FOLDERPATH}/derive/preparations'
    input_plants_parts_folderpath = f'{HUB_FOLDERPATH}/derive/plants_parts'
    input_conditions_folderpath = f'{HUB_FOLDERPATH}/derive/conditions'
    input_chemicals_folderpath = f'{HUB_FOLDERPATH}/derive/chemicals'
    input_activities_folderpath = f'{HUB_FOLDERPATH}/derive/activities'
    output_folderpath = f'{HUB_FOLDERPATH}/augment/intro'
    # try: shutil.rmtree(output_folderpath)
    # except: pass
    io.folders_recursive_gen(output_folderpath)
    ###
    master_items = masterize_utils.masterize_plants_get_all()
    found_num = 0
    for i, master_item in enumerate(master_items[:]):
        print(f'AUGMENT PREPARATIONS {i}/{len(master_items)}')
        plant_name_scientific_reference = master_item['plant_name_scientific_reference']
        input_preparations_filepath = f'{input_preparations_folderpath}/{plant_name_scientific_reference}.json'
        input_plants_parts_filepath = f'{input_plants_parts_folderpath}/{plant_name_scientific_reference}.json'
        input_conditions_filepath = f'{input_conditions_folderpath}/{plant_name_scientific_reference}.json'
        input_chemicals_filepath = f'{input_chemicals_folderpath}/{plant_name_scientific_reference}.json'
        input_activities_filepath = f'{input_activities_folderpath}/{plant_name_scientific_reference}.json'
        output_filepath = f'{output_folderpath}/{plant_name_scientific_reference}.json'
        input_preparations_data = io.json_read(input_preparations_filepath)
        input_plants_parts_data = io.json_read(input_plants_parts_filepath)
        input_conditions_data = io.json_read(input_conditions_filepath)
        input_chemicals_data = io.json_read(input_chemicals_filepath)
        input_activities_data = io.json_read(input_activities_filepath)
        ###
        # print(json.dumps(master_item, indent=4))
        # print(json.dumps(input_data, indent=4))
        # quit()
        if os.path.exists(output_filepath): continue
        if (
            input_preparations_data != [] or 
            input_plants_parts_data != [] or 
            input_conditions_data != [] or 
            input_chemicals_data != [] or 
            input_activities_data != []
        ):
            found_num += 1
            preparations = [item['preparation_name_reference'] for item in input_preparations_data][:4]
            plants_parts = [item['plant_part_name_reference'] for item in input_plants_parts_data][:4]
            conditions = [item['condition_name_reference'] for item in input_conditions_data][:4]
            chemicals = [item['chemical_name_reference'] for item in input_chemicals_data][:4]
            activities = [item['activity_name_reference'] for item in input_activities_data][:4]
            preparations_prompt = ', '.join(preparations)
            plants_parts_prompt = ', '.join(plants_parts)
            conditions_prompt = ', '.join(conditions)
            chemicals_prompt = ', '.join(chemicals)
            activities_prompt = ', '.join(activities)
            # quit()
            sentences_num = 0
            sentences_num += len(activities_prompt)
            sentences_num += len(chemicals_prompt)
            sentences_num += len(conditions_prompt)
            sentences_num += len(plants_parts_prompt)
            sentences_num += len(preparations_prompt)
            if activities_prompt.strip() != '': activities_prompt = f'''activities: {activities_prompt}'''
            if chemicals_prompt.strip() != '': chemicals_prompt = f'''chemicals: {chemicals_prompt}'''
            if conditions_prompt.strip() != '': conditions_prompt = f'''conditions: {conditions_prompt}'''
            if plants_parts_prompt.strip() != '': plants_parts_prompt = f'''plants_parts: {plants_parts_prompt}'''
            if preparations_prompt.strip() != '': preparations_prompt = f'''preparations: {preparations_prompt}'''
            prompt = f'''
                Write a 5-sentence intro paragraph about the following plant: {plant_name_scientific_reference}.
                CONTEXT:
                {activities_prompt}
                {chemicals_prompt}
                {conditions_prompt}
                {plants_parts_prompt}
                {preparations_prompt}
                RULES:
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
                'llm_intro': reply,
            }
        else: 
            input_data = {
                'llm_intro': '',
            }
        print(json.dumps(input_data, indent=4))
        io.json_write(output_filepath, input_data)
        # quit()
    print(found_num)


def schema_augment_gen(schema_item):
    schema_regen = schema_item['regen']
    schema_table_name = schema_item['table_name']
    schema_source_name = schema_item['sources'][0]['source_name']
    schema_output_foldername = schema_table_name
    schema_entity_1_val = schema_item['fields'][0]['field_name']
    schema_relationship_val = schema_item['fields'][1]['field_name']
    schema_entity_2_val = schema_item['fields'][2]['field_name']
    schema_fields_remaining = schema_item['fields'][3:]
    augment_fields_names = []
    for field in schema_fields_remaining:
        for key, val in field.items():
            if key == 'augment' and field['augment'] == 1:
                    augment_fields_names.append(field['field_name'])
    # quit()
    ###
    input_folderpath = f'{HUB_FOLDERPATH}/derive/{schema_table_name}'
    output_folderpath = f'{HUB_FOLDERPATH}/augment/{schema_table_name}'
    if schema_regen:
        try: shutil.rmtree(output_folderpath)
        except: pass
    io.folders_recursive_gen(output_folderpath)
    ###
    master_items = masterize_utils.masterize_plants_get_all()
    for i, master_item in enumerate(master_items[:]):
        print(f'AUGMENT {schema_table_name} {i}/{len(master_items)}')
        plant_name_scientific_reference = master_item['plant_name_scientific_reference']
        input_filepath = f'{input_folderpath}/{plant_name_scientific_reference}.json'
        output_filepath = f'{output_folderpath}/{plant_name_scientific_reference}.json'
        input_data = io.json_read(input_filepath)
        print(plant_name_scientific_reference)
        # if plant_name_scientific_reference != 'Panax ginseng': continue
        # print(json.dumps(master_item, indent=4))
        # quit()
        ###
        # print(json.dumps(input_data, indent=4))
        # quit()
        if os.path.exists(output_filepath): continue
        if input_data != []:
            # print(json.dumps(input_data, indent=4))
            # quit()
            prompt_relationships = []
            # relationships = []
            prompt_abstracts = []
            for input_item in input_data[:5]:
                entity_1_val = input_item[f'{schema_entity_1_val}_reference']
                relationship_val = input_item[f'{schema_relationship_val}_raw'].replace('_', ' ')
                entity_2_val = input_item[f'{schema_entity_2_val}_reference']
                augment_fields_vals = ''
                for augment_field_name in augment_fields_names:
                    augment_fields_vals += ', ' + input_item[f'{augment_field_name}']
                prompt_relationships.append(f'''{entity_1_val} {relationship_val} {entity_2_val}{augment_fields_vals}''')
                # print(prompt_relationships)
                # quit()
                ###
                for source in input_item['sources'][:3]:
                    source_id = source['reference_id']
                    if source_id.strip() == '': continue
                    study_filepath = f'{HUB_FOLDERPATH}/fetch/pubmed/medicinal_plant/abstracts/{source_id}.json'
                    ###
                    study_data = io.json_read(study_filepath)
                    try: article_data = study_data['PubmedArticle'][0]['MedlineCitation']['Article']
                    except: pass
                    try: study_title = article_data['ArticleTitle']
                    except: input_title = ''
                    try: study_abstract = ' '.join(article_data['Abstract']['AbstractText'])
                    except: continue
                    # print(study_abstract)
                    study_abstract = ' '.join(study_abstract.split(' ')[:800])
                    prompt_abstracts.append(f'{study_title} {study_abstract}')
                    # quit()
            prompt_relationships = '\n'.join(prompt_relationships)
            # print(prompt_relationships)
            # quit()
            ###
            # prompt_abstracts = '\n'.join(prompt_abstracts)[:10000]
            if prompt_abstracts != []:
                prompt_abstracts_0 = 'found in the ABSTRACTS below'
                prompt_abstracts_1 = '\n'.join(prompt_abstracts)[:]
                prompt_abstracts_1 = 'ABSTRACTS:\n' + prompt_abstracts_1
            else:
                prompt_abstracts_0 = ''
                prompt_abstracts_1 = ''
            # prompt_abstracts = ' '.join(prompt_abstracts.split(' '))
            ###
            prompt_sentences_count = len(prompt_relationships[:5])
            ### STUDY
            prompt = f'''
                Write a {prompt_sentences_count}-sentence paragraph for an article about the following plant RELATIONSHIPS {prompt_abstracts_0}.
                RELATIONSHIPS:
                {prompt_relationships.strip()}
                {prompt_abstracts_1}
                RULES:
                Reply only with the asked content.
                Reply using a prose that flows well and reads natural.
                Start with the following words: {plant_name_scientific_reference} .
            '''.strip()
                # Answer in a direct and straightforward way.
                # Don't start with generic info, reply directly with the relationships asked.
                # Don't start with generic info, reply directly with the relationships asked.
                # Don't end with generic info, only write about the relationships asked.
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
                schema_table_name: input_data,
                'llm_intro': reply,
            }
            # quit()
        else: 
            input_data = {
                schema_table_name: input_data,
                'llm_intro': '',
            }
        # print(json.dumps(input_data, indent=4))
        io.json_write(output_filepath, input_data)
        # quit()

def morphology_augment_gen(regen=False):
    ###
    input_folderpath = f'{HUB_FOLDERPATH}/derive/plants_morphologies'
    output_folderpath = f'{HUB_FOLDERPATH}/augment/plants_morphologies'
    if regen:
        try: shutil.rmtree(output_folderpath)
        except: pass
    io.folders_recursive_gen(output_folderpath)
    ###
    master_items = masterize_utils.masterize_plants_get_all()
    for i, master_item in enumerate(master_items[:]):
        print(f'AUGMENT HERBS morphology {i}/{len(master_items)}')
        plant_name_scientific_reference = master_item['plant_name_scientific_reference']
        input_filepath = f'{input_folderpath}/{plant_name_scientific_reference}.json'
        output_filepath = f'{output_folderpath}/{plant_name_scientific_reference}.json'
        input_data = io.json_read(input_filepath)
        print(plant_name_scientific_reference)
        # if plant_name_scientific_reference != 'Panax ginseng': continue
        # print(json.dumps(master_item, indent=4))
        # quit()
        ###
        # print(json.dumps(input_data, indent=4))
        # quit()
        if os.path.exists(output_filepath): continue
        if input_data != []:
            # print(json.dumps(input_data, indent=4))
            # quit()
            prompt_relationships = []
            # relationships = []
            prompt_abstracts = []
            for input_item in input_data[:5]:
                print(json.dumps(input_item, indent=4))
                # print(prompt_relationships)
                if input_item['relationship_name_raw'] == 'has_growth_form':
                    relationship_line = ''
                    relationship_line += input_item['plant_name_scientific_reference'] + ' '
                    relationship_line += input_item['relationship_name_raw'].replace('_', ' ') + ' '
                    relationship_line += input_item['growth_form_name_reference'] + ' '
                    prompt_relationships.append(relationship_line)
                    # print(relationship_line)
                elif input_item['relationship_name_raw'] == 'is_climber':
                    relationship_line = ''
                    relationship_line += input_item['plant_name_scientific_reference'] + ' '
                    if input_item['climber_name_reference'] == 'self-supporting':
                        relationship_line += 'is self-supporting'
                    elif input_item['climber_name_reference'] == 'obligatory':
                        relationship_line += 'has obligatory climbing habit'
                    elif input_item['climber_name_reference'] == 'facultative':
                        relationship_line += 'has facultative climbing habit'
                    elif input_item['climber_name_reference'] == 'vine':
                        relationship_line += 'has vine growth habit'
                    elif input_item['climber_name_reference'] == 'liana':
                        relationship_line += 'has liana growth habit'
                    prompt_relationships.append(relationship_line)
                    # print(relationship_line)
                elif input_item['relationship_name_raw'] == 'has_height_min':
                    relationship_line = ''
                    relationship_line += input_item['plant_name_scientific_reference'] + ' '
                    relationship_line += input_item['relationship_name_raw'].replace('_', ' ') + ' '
                    relationship_line += input_item['height_name_reference'] + ' '
                    prompt_relationships.append(relationship_line)
                    # print(relationship_line)
                elif input_item['relationship_name_raw'] == 'has_height_max':
                    relationship_line = ''
                    relationship_line += input_item['plant_name_scientific_reference'] + ' '
                    relationship_line += input_item['relationship_name_raw'].replace('_', ' ') + ' '
                    relationship_line += input_item['height_name_reference'] + ' '
                    prompt_relationships.append(relationship_line)
                    # print(relationship_line)
                # quit()
                ###
                for source in input_item['sources'][:3]:
                    source_id = source['reference_id']
                    if source_id.strip() == '': continue
                    study_filepath = f'{HUB_FOLDERPATH}/fetch/pubmed/medicinal_plant/abstracts/{source_id}.json'
                    ###
                    study_data = io.json_read(study_filepath)
                    try: article_data = study_data['PubmedArticle'][0]['MedlineCitation']['Article']
                    except: pass
                    try: study_title = article_data['ArticleTitle']
                    except: input_title = ''
                    try: study_abstract = ' '.join(article_data['Abstract']['AbstractText'])
                    except: continue
                    # print(study_abstract)
                    study_abstract = ' '.join(study_abstract.split(' ')[:800])
                    prompt_abstracts.append(f'{study_title} {study_abstract}')
                    # quit()
            prompt_sentences_count = len(prompt_relationships[:5])
            # if prompt_sentences_count < 3: continue
            prompt_relationships = '\n'.join(prompt_relationships)
            # print(prompt_relationships)
            # quit()
            ###
            # prompt_abstracts = '\n'.join(prompt_abstracts)[:10000]
            if prompt_abstracts != []:
                prompt_abstracts_0 = 'found in the ABSTRACTS below'
                prompt_abstracts_1 = '\n'.join(prompt_abstracts)[:]
                prompt_abstracts_1 = 'ABSTRACTS:\n' + prompt_abstracts_1
            else:
                prompt_abstracts_0 = ''
                prompt_abstracts_1 = ''
            # prompt_abstracts = ' '.join(prompt_abstracts.split(' '))
            ###
            ### STUDY
            prompt = f'''
                Write a {prompt_sentences_count}-sentence paragraph for an article about the following plant RELATIONSHIPS {prompt_abstracts_0}.
                RELATIONSHIPS:
                {prompt_relationships.strip()}
                {prompt_abstracts_1}
                RULES:
                Reply only with the asked content.
                Reply using a prose that flows well and reads natural.
                Start with the following words: {plant_name_scientific_reference} .
            '''.strip()
                # Answer in a direct and straightforward way.
                # Don't start with generic info, reply directly with the relationships asked.
                # Don't start with generic info, reply directly with the relationships asked.
                # Don't end with generic info, only write about the relationships asked.
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
                'plants_morphologies': input_data,
                'llm_intro': reply,
            }
            # quit()
        else: 
            input_data = {
                'plants_morphologies': input_data,
                'llm_intro': '',
            }
        # print(json.dumps(input_data, indent=4))
        io.json_write(output_filepath, input_data)
        # quit()

def augment_plants_activities_gen(regen=False):
    ### TODO: at the moment it just copies. implement llm.
    input_folderpath = f'{HUB_FOLDERPATH}/derive/plants_activities'
    output_folderpath = f'{HUB_FOLDERPATH}/augment/plants_activities'
    if regen:
        try: shutil.rmtree(output_folderpath)
        except: pass
    io.folders_recursive_gen(output_folderpath)
    ###
    plants_items = sql.sql_plants()
    for i, plant_item in enumerate(plants_items[:]):
        print(f'AUGMENT HERBS plants activities {i}/{len(plants_items)}')
        plant_name_scientific_reference = plant_item['plant_name_scientific_reference']
        input_filepath = f'{input_folderpath}/{plant_name_scientific_reference}.json'
        output_filepath = f'{output_folderpath}/{plant_name_scientific_reference}.json'
        input_data = io.json_read(input_filepath)
        # print(plant_name_scientific_reference)
        # print(json.dumps(input_data, indent=4))
        # quit()
        if os.path.exists(output_filepath): continue
        if input_data != []:
            # print(json.dumps(input_data, indent=4))
            # quit()
            pass
        io.json_write(output_filepath, input_data)

def augment__plants__plants_names_common_gen(regen=False):
    ### TODO: at the moment it just copies. implement llm.
    table_name = 'plants__plants_names_common'
    input_folderpath = f'{HUB_FOLDERPATH}/derive/{table_name}'
    output_folderpath = f'{HUB_FOLDERPATH}/augment/{table_name}'
    if regen:
        try: shutil.rmtree(output_folderpath)
        except: pass
    io.folders_recursive_gen(output_folderpath)
    ###
    plants_items = sql.sql_plants()
    for i, plant_item in enumerate(plants_items[:]):
        print(f'AUGMENT HERBS plants__plants_names_common_gen {i}/{len(plants_items)}')
        plant_name_scientific_reference = plant_item['plant_name_scientific_reference']
        input_filepath = f'{input_folderpath}/{plant_name_scientific_reference}.json'
        output_filepath = f'{output_folderpath}/{plant_name_scientific_reference}.json'
        input_data = io.json_read(input_filepath)
        # print(plant_name_scientific_reference)
        # print(json.dumps(input_data, indent=4))
        # quit()
        if os.path.exists(output_filepath): continue
        if input_data != []:
            # print(json.dumps(input_data, indent=4))
            # quit()
            pass
        io.json_write(output_filepath, input_data)

def run():
    # augment_plants_activities_gen(regen=True)
    augment__plants__plants_names_common_gen(regen=True)

    # morphology_augment_gen()
    return

    schema_items = schema_herbs.data['items']
    for schema_item in schema_items: 
        if schema_item['process'] != True: continue
        schema_augment_gen(schema_item)

    if 0:
        # augment_copy(attribute='taxonomies')
        # augment_copy(attribute='diseases')

        # augment_copy(attribute='preparations')
        # augment_compounds()

        augment_intro()
        # augment_preparations()
        augment_plants_parts()
        augment_conditions()
        # augment_chemicals()
        augment_activities()

        # augment_copy(attribute='chemicals')

        augment_copy(attribute='taxonomies')

        augment_copy(attribute='synonyms')


        augment_copy(attribute='traits')
        augment_copy(attribute='distributions')
        augment_copy(attribute='names_common')
