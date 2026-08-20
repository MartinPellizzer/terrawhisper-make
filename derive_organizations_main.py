import os
import json
import time
import shutil
import sqlite3

from lib import g
from lib import io

import masterize_organizations_utils

HUB_FOLDERPATH = f'{g.DATA_FOLDERPATH}/organizations' 

import parse_organizations_data

def identity_gen():
    entity_foldername = 'identity'
    # items = observations_get_all()
    master_items = masterize_organizations_utils.masterize_organizations_get_all()
    for i, master_item in enumerate(master_items):
        print(f'{i}/{len(master_items)}')
        business_name_canonical = master_item['business_name_canonical']
        print(business_name_canonical)
        ###
        db_filepath = f'{HUB_FOLDERPATH}/qualify/observations.db'
        conn = sqlite3.connect(db_filepath)
        conn.row_factory = sqlite3.Row
        cursor = conn.execute("""
            SELECT *
            FROM organizations
            WHERE business_name_canonical = ?
            ORDER BY business_name_canonical;
        """, (business_name_canonical,))
        rows = cursor.fetchall()
        observe_items = [dict(row) for row in rows]
        conn.close()
        ###
        output_items = []
        for observe_item in observe_items:
            '''
            output_item = {
                'business_is_category_herbs': observe_item['business_is_category_herbs'],
                'official business name': observe_item['business_name_official'],
                'official business name': observe_item['business_name_official'],
                'business slogan': observe_item['business_slogan'],
                'short business description': observe_item['business_description_short'],
                'business description': observe_item['business_description'],
                'primary business type': observe_item['business_type_primary'],
                'secondary business type': observe_item['business_type_secondary'],
                'business industry': observe_item['business_industry'],
                'business niche': observe_item['business_niche'],
                'business model': observe_item['business_model'],
                'business status': observe_item['business_status'],
            }
            '''
            print(observe_item)
            output_item = {
                'business_is_category_herbs': observe_item['business_is_category_herbs'],
                'business_name_canonical': observe_item['business_name_canonical'],
            }
            output_items.append(output_item)
            # print(json.dumps(output_item, indent=4))
            # quit()
        ###
        output_filepath = f'{HUB_FOLDERPATH}/derive/{entity_foldername}/{business_name_canonical}.json'
        io.folder_create_from_filepath(output_filepath)
        io.json_write(output_filepath, output_items)
        # quit()

def field_section_gen(observe_item):
    fields_data = parse_organizations_data.data
    field_section = ''
    for observe_key, observe_val in observe_item.items():
        for field_item in fields_data:
            field_name = field_item['field_name']
            if observe_key == field_name:
                field_section = field_item['field_section']
                break
    return field_section

def derive_sections():
    try: shutil.rmtree(f'{HUB_FOLDERPATH}/derive')
    except: pass
    io.folders_recursive_gen(f'{HUB_FOLDERPATH}/derive')
    ###
    master_items = masterize_organizations_utils.masterize_organizations_get_all()
    for i, master_item in enumerate(master_items):
        print(f'{i}/{len(master_items)}')
        # print(json.dumps(master_item, indent=4))
        business_name_canonical = master_item['business_name_canonical']
        ### TODO: find observations by canonical name
        db_filepath = f'{HUB_FOLDERPATH}/observe/observations.db'
        conn = sqlite3.connect(db_filepath)
        conn.row_factory = sqlite3.Row
        cursor = conn.execute("""
            SELECT *
            FROM organizations
            WHERE business_name_canonical = ?
            ORDER BY business_name_canonical;
        """, (business_name_canonical,))
        rows = cursor.fetchall()
        observe_items = [dict(row) for row in rows]
        conn.close()
        ###
        output_items = []
        for observe_item in observe_items: 
            # field_section = field_section_gen(observe_item)
            fields_data = parse_organizations_data.data
            print(json.dumps(observe_item, indent=4))
            # print(json.dumps(fields_data, indent=4))
            for observe_key, observe_val in observe_item.items():
                field_section = ''
                # print(observe_key, observe_val)
                for field_item in fields_data:
                    # print(field_item)
                    # print(observe_key, field_item['field_name'])
                    if observe_key == field_item['field_name']:
                        field_section = field_item['field_section']
                        # print(observe_key, field_item['field_name'])
                        # print(field_section)
                        # print(observe_key)
                        break
                        # quit()
                if field_section != '':
                    print(field_section)
                    print(observe_key, observe_val)
                    found = False
                    for output_item in output_items:
                        if output_item['field_section'] == field_section:
                            output_item['fields'][observe_key] = observe_val
                            found = True
                            break
                    if not found:
                        output_item = {
                            'field_section': field_section,
                            'fields': {observe_key: observe_val},
                        }
                        output_items.append(output_item)
        print(json.dumps(output_items, indent=4))
        for output_item in output_items:
            field_section = output_item['field_section']
            fields = output_item['fields']
            output_filepath = f'{HUB_FOLDERPATH}/derive/{field_section}/{business_name_canonical}.json'
            io.folder_create_from_filepath(output_filepath)
            io.json_write(output_filepath, [fields])

def run():
    if 1:
        derive_sections()

    if 0:
        identity_gen()

