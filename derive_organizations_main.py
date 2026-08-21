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

def field_section_find(fields_data, observe_key):
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
        # quit()
        business_name_canonical = master_item['business_name_canonical']
        ###
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
        print(len(observe_items))
        # print(business_name_canonical)
        # continue
        # quit()
        ###
        # TODO: debug, remove
        if len(observe_items) < 2: continue
        print(business_name_canonical)
        # print(json.dumps(observe_items, indent=4))
        # quit()
        output_items = []
        for observe_item in observe_items: 
            fields_data = parse_organizations_data.data
            # print(json.dumps(observe_item, indent=4))
            # print(json.dumps(fields_data, indent=4))
            source_name = observe_item['source_name']
            for observe_key, observe_val in observe_item.items():
                field_section = field_section_find(fields_data, observe_key)
                # print(observe_key, observe_val)
                if field_section != '':
                    # print(field_section)
                    # print(observe_key, observe_val)
                    found_section = False
                    found_source = False
                    for output_item in output_items:
                        if output_item['field_section'] == field_section:
                            found_section = True
                        if output_item['source_name'] == source_name:
                            found_source = True
                    ###
                    if found_section and found_source:
                        output_item['fields'][observe_key] = observe_val
                    else:
                        output_item = {
                            'source_name': source_name,
                            'field_section': field_section,
                            'fields': {observe_key: observe_val},
                        }
                        output_items.append(output_item)
            # print(output_items)
            # quit()
        # print(json.dumps(output_items, indent=4))
        # quit()

        ### group by section
        output_items_grouped = []
        for output_item in output_items:
            found = False
            for output_item_grouped in output_items_grouped:
                if output_item_grouped['field_section'] == output_item['field_section']:
                    found = True
                    output_item_grouped['items'].append(output_item)
                    break
            if not found:
                new_item = {
                    'field_section': output_item['field_section'],
                    'items': [output_item],
                }
                output_items_grouped.append(new_item)
                # print(json.dumps(output_items_grouped, indent=4))
                # quit()

        # print(json.dumps(output_items_grouped, indent=4))
        # quit()

        for output_item_grouped in output_items_grouped:
            print(json.dumps(output_item_grouped, indent=4))
            field_section = output_item_grouped['field_section']
            io.folders_recursive_gen(f'{HUB_FOLDERPATH}/derive/{field_section}')
            output_filepath = f'{HUB_FOLDERPATH}/derive/{field_section}/{business_name_canonical}.json'
            io.json_write(output_filepath, [output_item_grouped['items']])

        quit()

        ### create folders from sections
        for output_item in output_items:
            field_section = output_item['field_section']
            io.folders_recursive_gen(f'{HUB_FOLDERPATH}/derive/{field_section}')

        for output_item in output_items:
            field_section = output_item['field_section']
            output_filepath = f'{HUB_FOLDERPATH}/derive/{field_section}/{business_name_canonical}.json'
            io.json_write(output_filepath, [output_item['fields']])

        quit()

        for output_item in output_items:
            print(json.dumps(output_item, indent=4))
            field_section = output_item['field_section']
            fields = output_item['fields']
            output_filepath = f'{HUB_FOLDERPATH}/derive/{field_section}/{business_name_canonical}.json'
            io.folder_create_from_filepath(output_filepath)
            io.json_write(output_filepath, [fields])
        quit()

def run():
    if 1:
        derive_sections()

