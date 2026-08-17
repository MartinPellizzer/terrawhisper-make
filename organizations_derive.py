import os
import json
import time
import shutil
import sqlite3

from lib import g
from lib import io

HUB_FOLDERPATH = f'{g.DATA_FOLDERPATH}/organizations' 

def folder_copy():
    input_foldername = f'qualify'
    output_foldername = f'derive'
    input_folderpath = f'{HUB_FOLDERPATH}/{input_foldername}'
    output_folderpath = f'{HUB_FOLDERPATH}/{output_foldername}'
    io.folders_recursive_gen(output_folderpath)
    input_filenames = os.listdir(input_folderpath)
    ###
    i = 0
    for input_filename in input_filenames[i:]:
        print(input_filename)
        i += 1
        print(f'{i}/{len(input_filenames)}')
        output_filepath = f'{output_folderpath}/{input_filename}'
        input_filepath = f'{input_folderpath}/{input_filename}'
        # if os.path.exists(output_filepath): continue
        shutil.copy2(input_filepath, output_filepath)

def observations_get_all():
    db_filepath = f'{HUB_FOLDERPATH}/observe/observations.db'
    conn = sqlite3.connect(db_filepath)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    rows = cur.execute(f'SELECT * FROM organizations').fetchall()
    dict_rows = [dict(row) for row in rows]
    conn.close()
    return dict_rows

def identity_gen():
    entity_foldername = 'identity'
    items = observations_get_all()
    for i, item in enumerate(items):
        print(f'{i}/{len(items)}')
        business_name_official = item['business_name_official']
        print(business_name_official )
        output_items = []
        item_new = {
            'official business name': item['business_name_official'],
            'business slogan': item['business_slogan'],
            'short business description': item['business_description_short'],
            'business description': item['business_description'],
            'primary business type': item['business_type_primary'],
            'secondary business type': item['business_type_secondary'],
            'business industry': item['business_industry'],
            'business niche': item['business_niche'],
            'business model': item['business_model'],
            'business status': item['business_status'],
        }
        output_items.append(item_new)
        '''
        output_item = {
            'section': f'{entity_foldername}',
            'items': output_items,
        }
        '''
        print(json.dumps(output_items, indent=4))
        # quit()
        ###
        output_filepath = f'{HUB_FOLDERPATH}/derive/{entity_foldername}/{business_name_official}.json'
        io.folder_create_from_filepath(output_filepath)
        io.json_write(output_filepath, output_items)
        # quit()

def gen():
    print('QUALIFY')

    if 1:
        identity_gen()

    '''
    start = time.perf_counter()
    folder_copy()
    print(f'folder_copy() - execution time: ', time.perf_counter() - start)
    '''

gen()
