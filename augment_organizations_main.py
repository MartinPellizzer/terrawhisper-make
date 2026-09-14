
import os
import json
import sqlite3
import shutil

from lib import g
from lib import io
from lib import llm
from lib import data
from lib import polish

import masterize_organizations_utils

model_filepath = '/home/ubuntu/vault-tmp/llm/gemma-4-12b-it-Q4_K_S.gguf'
model_filepath = '/home/ubuntu/vault-tmp/llm/gemma-4-12B-it-qat-UD-Q4_K_XL.gguf'
HUB_FOLDERPATH = f'{g.DATA_FOLDERPATH}/organizations' 

def augment_organizations():
    master_items = masterize_organizations_utils.masterize_organizations_get_all()
    for i, master_item in enumerate(master_items):
        print(f'{i}/{len(master_items)}')
        business_name_canonical = master_item['business_name_canonical']
        ###
        sections_folderpath = f'{HUB_FOLDERPATH}/derive'
        sections_foldernames = sorted(os.listdir(sections_folderpath))
        for section_foldername in sections_foldernames:
            section_folderpath = f'{sections_folderpath}/{section_foldername}'
            # print(section_folderpath)
            # quit()
            ###
            input_data = io.json_read(f'{HUB_FOLDERPATH}/derive/{section_foldername}/{business_name_canonical}.json')
            output_folderpath = f'{HUB_FOLDERPATH}/augment/{section_foldername}'
            io.folders_recursive_gen(output_folderpath)
            output_filepath = f'{HUB_FOLDERPATH}/augment/{section_foldername}/{business_name_canonical}.json'
            if os.path.exists(output_filepath): output_data = io.json_read(output_filepath)
            else: output_data = input_data
            ###
            print('#########################################################################')
            print(json.dumps(output_data, indent=4))
            print('#########################################################################')
            ### COPY DATA
            # if output_data[0]['field_section'] == 'identity':
                # quit()
            for output_list in output_data:
                if output_list['items'] == []:
                    io.json_write(output_filepath, output_data)
                else:
                    for output_item in output_list['items']:
                        # print(output_list)
                        # print(output_item)
                        # quit()
                        key = 'llm'
                        if 0:
                            prompt = f'''
                                I'm writing an article about the following business: {business_name_canonical}. 
                                Write a detailed description focusing only on the following section: {section_foldername}.
                                Use the following data to write the description: {output_data}.
                                Reply in a paragraph.
                                Write only in english, translate from other languages if necessary.
                                Start with the following words: {business_name_canonical} is .
                            '''.strip()
                            print(prompt)
                            reply = llm.reply(prompt, model_filepath)
                            # reply = 'test desc'
                            if '</think>' in reply:
                                reply = reply.split('</think>')[1].strip()
                            reply = polish.vanilla(reply)
                            print('########################################################################')
                            print(reply)
                            print('########################################################################')
                            print(output_item)
                            output_item[key] = reply
                            io.json_write(output_filepath, output_data)
                            print(json.dumps(output_data, indent=4))
                            # quit()
                        else:
                            output_item[key] = ''
                            io.json_write(output_filepath, output_data)
                            # print(json.dumps(output_data, indent=4))
                            # quit()
            # print('#########################################################################')
            # print(json.dumps(output_data, indent=4))
            # print('#########################################################################')

            ### GENERATE LOCATION
            if output_data[0]['field_section'] == 'identity':
                llm_location = ''
                business_address = None
                for output_item in output_data[0]['items']:
                    # print(json.dumps(output_item, indent=4))
                    if output_item['source_name'] == 'Google Maps':
                        if business_address == None: business_address = output_item['fields']['business_address']
                # print(business_address)
                # quit()
                if business_address != None:
                    prompt = f'''
                        Write a sentence using the following data:
                        business name: {business_name_canonical}
                        address: {business_address}
                        Reply only with the content asked.
                        Start with the following words: {business_name_canonical} 
                    '''.strip()
                    print(prompt)
                    reply = llm.reply(prompt, model_filepath)
                    # reply = 'test desc'
                    if '</think>' in reply:
                        reply = reply.split('</think>')[1].strip()
                    reply = polish.vanilla(reply)
                    print('########################################################################')
                    print(reply)
                    print('########################################################################')
                    print(output_item)
                    llm_location = reply
                output_data[0]['llm_location'] = llm_location
                io.json_write(output_filepath, output_data)
                print('#########################################################################')
                print(json.dumps(output_data, indent=4))
                print('#########################################################################')
                # quit()

            ### GENERATE BOTANICAL ACTIVITIES
            if output_data[0]['field_section'] == 'identity':
                llm_activities = ''
                business_researches = None
                for output_item in output_data[0]['items']:
                    # print(json.dumps(output_item, indent=4))
                    if output_item['source_name'] == 'Website':
                        if business_researches == None: 
                            business_researches = output_item['fields']['business_researches']
                # print(business_address)
                # quit()
                prompt_data = []
                if business_name_canonical != None: prompt_data.append(f'business name: {business_name_canonical}')
                if business_researches != None: prompt_data.append(f'business researches: {business_researches}')
                if prompt_data != []:
                    prompt_data_text = '\n'.join(prompt_data)
                    prompt = f'''
                        Write 2-4 sentences using the following data:
                        {prompt_data_text}
                        Reply only with the content asked.
                        Reply with a paragraph.
                    '''.strip()
                    print(prompt)
                    reply = llm.reply(prompt, model_filepath)
                    # reply = 'test desc'
                    if '</think>' in reply:
                        reply = reply.split('</think>')[1].strip()
                    reply = polish.vanilla(reply)
                    print('########################################################################')
                    print(reply)
                    print('########################################################################')
                    print(output_item)
                    llm_activities = reply
                output_data[0]['llm_activities'] = llm_activities
                io.json_write(output_filepath, output_data)
                print('#########################################################################')
                print(json.dumps(output_data, indent=4))
                print('#########################################################################')
                # quit()

            ### GENERATE PRODUCTS
            if output_data[0]['field_section'] == 'identity':
                llm_products = ''
                business_products = None
                for output_item in output_data[0]['items']:
                    # print(json.dumps(output_item, indent=4))
                    if output_item['source_name'] == 'Website':
                        if business_products == None: 
                            business_products = output_item['fields']['business_products']
                # print(business_address)
                # quit()
                prompt_data = []
                if business_name_canonical != None: prompt_data.append(f'business name: {business_name_canonical}')
                if business_products != None: prompt_data.append(f'business products: {business_products}')
                if prompt_data != []:
                    prompt_data_text = '\n'.join(prompt_data)
                    prompt = f'''
                        Write 2-4 sentences using the following data:
                        {prompt_data_text}
                        Reply only with the content asked.
                        Reply with a paragraph.
                    '''.strip()
                    print(prompt)
                    reply = llm.reply(prompt, model_filepath)
                    # reply = 'test desc'
                    if '</think>' in reply:
                        reply = reply.split('</think>')[1].strip()
                    reply = polish.vanilla(reply)
                    print('########################################################################')
                    print(reply)
                    print('########################################################################')
                    print(output_item)
                    llm_products = reply
                output_data[0]['llm_products'] = llm_products
                io.json_write(output_filepath, output_data)
                print('#########################################################################')
                print(json.dumps(output_data, indent=4))
                print('#########################################################################')
                # quit()

            ### GENERATE SERVICES
            if output_data[0]['field_section'] == 'identity':
                llm_services = ''
                business_herbal_consultation = None
                business_herbal_clinic = None
                business_medicinal_plant_consulting = None
                business_plant_identification = None
                business_botanical_identification = None
                business_cultivation_consulting = None
                business_contract_growing = None
                business_contract_manufacturing = None
                business_private_label_manufacturing = None
                business_extraction_services = None
                business_drying_services = None
                business_milling = None
                business_grinding = None
                business_packaging_service = None
                business_export_services = None
                business_laboratory_testing = None
                business_formulation = None
                business_research_services = None
                business_education = None
                business_workshops = None
                business_courses = None
                business_farm_tours = None
                business_botanical_tours = None
                for output_item in output_data[0]['items']:
                    # print(json.dumps(output_item, indent=4))
                    if output_item['source_name'] == 'Website':
                        if business_herbal_consultation == None: 
                            business_herbal_consultation = output_item['fields']['business_herbal_consultation']
                        if business_herbal_clinic == None: 
                            business_herbal_clinic = output_item['fields']['business_herbal_clinic']
                        if business_medicinal_plant_consulting == None: 
                            business_medicinal_plant_consulting = output_item['fields']['business_medicinal_plant_consulting']
                        if business_plant_identification == None: 
                            business_plant_identification = output_item['fields']['business_plant_identification']
                        if business_botanical_identification == None: 
                            business_botanical_identification = output_item['fields']['business_botanical_identification']
                        if business_cultivation_consulting == None: 
                            business_cultivation_consulting = output_item['fields']['business_cultivation_consulting']
                        if business_contract_growing == None: 
                            business_contract_growing = output_item['fields']['business_contract_growing']
                        if business_contract_manufacturing == None: 
                            business_contract_manufacturing = output_item['fields']['business_contract_manufacturing']
                        if business_private_label_manufacturing == None: 
                            business_private_label_manufacturing = output_item['fields']['business_private_label_manufacturing']
                        if business_extraction_services == None: 
                            business_extraction_services = output_item['fields']['business_extraction_services']
                        if business_drying_services == None: 
                            business_drying_services = output_item['fields']['business_drying_services']
                        if business_milling == None: 
                            business_milling = output_item['fields']['business_milling']
                        if business_grinding == None: 
                            business_grinding = output_item['fields']['business_grinding']
                        if business_packaging_service == None: 
                            business_packaging_service = output_item['fields']['business_packaging_service']
                        if business_export_services == None: 
                            business_export_services = output_item['fields']['business_export_services']
                        if business_laboratory_testing == None: 
                            business_laboratory_testing = output_item['fields']['business_laboratory_testing']
                        if business_formulation == None: 
                            business_formulation = output_item['fields']['business_formulation']
                        if business_research_services == None: 
                            business_research_services = output_item['fields']['business_research_services']
                        if business_education == None: 
                            business_education = output_item['fields']['business_education']
                        if business_workshops == None: 
                            business_workshops = output_item['fields']['business_workshops']
                        if business_courses == None: 
                            business_courses = output_item['fields']['business_courses']
                        if business_farm_tours == None: 
                            business_farm_tours = output_item['fields']['business_farm_tours']
                        if business_botanical_tours == None: 
                            business_botanical_tours = output_item['fields']['business_botanical_tours']
                # print(business_address)
                # quit()
                prompt_data = []
                if business_herbal_consultation != None: prompt_data.append(f'business herbal consultation: {business_herbal_consultation}')
                if business_herbal_clinic != None: prompt_data.append(f'business herbal clinic: {business_herbal_clinic}')
                if business_medicinal_plant_consulting != None: prompt_data.append(f'business medicinal plant consulting : {business_medicinal_plant_consulting}')
                if business_plant_identification != None: prompt_data.append(f'business plant identification: {business_plant_identification}')
                if business_botanical_identification != None: prompt_data.append(f'business botanical identification: {business_botanical_identification}')
                if business_cultivation_consulting != None: prompt_data.append(f'business cultivation consulting: {business_cultivation_consulting}')
                if business_contract_growing != None: prompt_data.append(f'business contract growing: {business_contract_growing}')
                if business_contract_manufacturing != None: prompt_data.append(f'business contract manufacturing: {business_contract_manufacturing}')
                if business_private_label_manufacturing != None: prompt_data.append(f'business private label manufacturing: {business_private_label_manufacturing}')
                if business_extraction_services != None: prompt_data.append(f'business extraction services: {business_extraction_services}')
                if business_drying_services != None: prompt_data.append(f'business drying services: {business_drying_services}')
                if business_milling != None: prompt_data.append(f'business milling: {business_milling}')
                if business_grinding != None: prompt_data.append(f'business grinding: {business_grinding}')
                if business_packaging_service != None: prompt_data.append(f'business packaging service: {business_packaging_service}')
                if business_export_services != None: prompt_data.append(f'business export services: {business_export_services}')
                if business_laboratory_testing != None: prompt_data.append(f'business laboratory testing: {business_laboratory_testing}')
                if business_formulation != None: prompt_data.append(f'business formulation: {business_formulation}')
                if business_research_services != None: prompt_data.append(f'business research services: {business_research_services}')
                if business_education != None: prompt_data.append(f'business education: {business_education}')
                if business_workshops != None: prompt_data.append(f'business workshops: {business_workshops}')
                if business_courses != None: prompt_data.append(f'business courses: {business_courses}')
                if business_farm_tours != None: prompt_data.append(f'business farm tours: {business_farm_tours}')
                if business_botanical_tours != None: prompt_data.append(f'business botanical tours: {business_botanical_tours}')
                if prompt_data != []:
                    prompt_data_text = '\n'.join(prompt_data)
                    prompt = f'''
                        Write 2-4 sentences using the following data:
                        business name: {business_name_canonical}
                        {prompt_data_text}
                        Reply only with the content asked.
                        Reply with a 2-4 senctence paragraph.
                        Answer only in plain paragraph format, never lists or other formats.
                    '''.strip()
                    print(prompt)
                    reply = llm.reply(prompt, model_filepath)
                    # reply = 'test desc'
                    if '</think>' in reply:
                        reply = reply.split('</think>')[1].strip()
                    reply = polish.vanilla(reply)
                    print('########################################################################')
                    print(reply)
                    print('########################################################################')
                    print(output_item)
                    llm_services = reply
                output_data[0]['llm_services'] = llm_services
                io.json_write(output_filepath, output_data)
                print('#########################################################################')
                print(json.dumps(output_data, indent=4))
                print('#########################################################################')
                # quit()
        # quit()

def run():
    output_folderpath = f'{HUB_FOLDERPATH}/augment'
    # try: shutil.rmtree(output_folderpath)
    # except: pass
    io.folders_recursive_gen(output_folderpath)

    ###
    augment_organizations()

