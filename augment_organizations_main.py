
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
    output_folderpath = f'{HUB_FOLDERPATH}/augment'
    # try: shutil.rmtree(output_folderpath)
    # except: pass
    io.folders_recursive_gen(output_folderpath)
    ###
    master_items = masterize_organizations_utils.masterize_organizations_get_all()
    for i, master_item in enumerate(master_items):
        print(f'{i}/{len(master_items)}')
        business_name_canonical = master_item['business_name_canonical']
        # print(item)
        # quit()
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
            # quit()
            for output_list in output_data:
                # if len(output_list) < 2: continue
                # print(output_data)
                # quit()
                print(json.dumps(output_list, indent=4))
                # quit()
                ###
                for output_item in output_list:
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
                        print(json.dumps(output_data, indent=4))

def run():
    augment_organizations()
