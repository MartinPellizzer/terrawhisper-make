import os
import csv
import json
import time
import shutil
import sqlite3

from collections import Counter

from lib import g
from lib import io

import masterize_utils
import parse_utils
import schema_herbs

HUB_FOLDERPATH = f'''{g.DATA_FOLDERPATH}/herbs'''

def trait_create(
    plant_name_scientific_reference,
    plant_name_scientific_reference_normalize,
    plant_genus,
    plant_author,
    trait_category,
    trait_1,
    trait_2,
    trait_units,
    trait_type,
    trait_value,
    trait_agreement,
    trait_coeff_var,
    trait_n,
    trait_refs,
    source_name,
    source_acronym,
):
    item = {
        'plant_name_scientific_reference': plant_name_scientific_reference,
        'plant_name_scientific_reference_normalize': plant_name_scientific_reference_normalize,
        'plant_genus': plant_genus,
        'plant_author': plant_author,
        'trait_category': trait_category,
        'trait_1': trait_1,
        'trait_2': trait_2,
        'trait_units': trait_units,
        'trait_type': trait_type,
        'trait_value': trait_value,
        'trait_agreement': trait_agreement,
        'trait_coeff_var': trait_coeff_var,
        'trait_n': trait_n,
        'trait_refs': trait_refs,
        'source_name': source_name,
        'source_acronym': source_acronym,
    }
    return item

def schema_parse_traits(schema_item):
    schema_table_name = schema_item['table_name']
    schema_fields = schema_item['fields']
    output_folderpath = f'{HUB_FOLDERPATH}/parse/gift/{schema_table_name}/json'
    if schema_item['regen'] == True:
        try: shutil.rmtree(output_folderpath)
        except: pass
    io.folders_recursive_gen(output_folderpath)
    ###
    master_plants_rows = masterize_utils.masterize_plants_get_all()
    conn = sqlite3.connect(f"{HUB_FOLDERPATH}/reference/gift/gift.db")
    cursor = conn.cursor()
    output_items_last = []
    for i, master_plant_row in enumerate(master_plants_rows[:]):
        print(f'PARSE HERBS TRAITS {i}/{len(master_plants_rows)}')
        # print(master_plant_row)
        # quit()
        plant_name_scientific_reference = master_plant_row['plant_name_scientific_reference']
        plant_name_scientific_reference_normalize = master_plant_row['plant_name_scientific_reference_normalize']
        cursor.execute("""
            SELECT 
                p.work_species,
                p.work_species_norm,
                p.work_genus,
                p.work_author,
                tm.category,
                tm.trait1,
                tm.trait2,
                tm.units,
                tm.type,
                pt.trait_value,
                pt.agreement,
                pt.coeff_var,
                pt.n,
                pt.refs
            FROM species p
            JOIN traits pt 
                ON p.work_id = pt.work_id
            JOIN traits_meta tm 
                ON pt.trait_id = tm.lvl3
            WHERE p.work_species_norm = ?
            ORDER BY tm.category;
        """, (plant_name_scientific_reference_normalize,))
        rows = cursor.fetchall()
        ###
        entity_1_key = schema_fields[0]['field_name']
        relationship_key = schema_fields[1]['field_name']
        entity_2_key = schema_fields[2]['field_name']
        ###
        output_items = []
        for row in rows:
            output_item = {
                f'{entity_1_key}_raw': row[0],
                f'{relationship_key}_raw': 'has_trait',
                f'{entity_2_key}_raw': row[5],
                f'trait_2_name': row[6],
                f'trait_units': row[7],
                f'trait_type': row[8],
                f'trait_value': row[9],
                f'trait_category': row[4],
                f'plant_author': row[3],
                f'plant_genus': row[2],
                f'trait_agreement': row[10],
                f'trait_coeff_var': row[11],
                f'trait_n': row[12],
                f'trait_refs': row[13],
                f'source_name': 'Global Inventory of Floras and Traits',
                f'source_acronym': 'GIFT',
                f'reference_id': '',
                f'reference_name': '',
            }
            """
            source_name = 'Global Inventory of Floras and Traits',
            source_acronym = 'GIFT',
            """
            output_items.append(output_item)
            # print(json.dumps(output_item, indent=4))
            # quit()
        output_filepath = f'{output_folderpath}/{plant_name_scientific_reference_normalize}.json'
        io.json_write(output_filepath, output_items)
        if output_items != []:
            output_items_last = output_items
    conn.close()
    print(json.dumps(output_items_last, indent=4))
    # quit()

def parse_traits():
    schema_table_name = schema_item['table_name']
    schema_fields = schema_item['fields']
    output_folderpath = f'{HUB_FOLDERPATH}/parse/gift/{schema_table_name}/json'
    if schema_item['regen'] == True:
        try: shutil.rmtree(output_folderpath)
        except: pass
    io.folders_recursive_gen(output_folderpath)
    ###
    master_plants_rows = masterize_utils.masterize_plants_get_all()
    conn = sqlite3.connect(f"{HUB_FOLDERPATH}/reference/gift/gift.db")
    cursor = conn.cursor()
    output_items_last = []
    for i, master_plant_row in enumerate(master_plants_rows[:]):
        print(f'PARSE HERBS TRAITS {i}/{len(master_plants_rows)}')
        # print(master_plant_row)
        # quit()
        plant_name_scientific_reference = master_plant_row['plant_name_scientific_reference']
        plant_name_scientific_reference_normalize = master_plant_row['plant_name_scientific_reference_normalize']
        cursor.execute("""
            SELECT 
                p.work_species,
                p.work_species_norm,
                p.work_genus,
                p.work_author,
                tm.category,
                tm.trait1,
                tm.trait2,
                tm.units,
                tm.type,
                pt.trait_value,
                pt.agreement,
                pt.coeff_var,
                pt.n,
                pt.refs
            FROM species p
            JOIN traits pt 
                ON p.work_id = pt.work_id
            JOIN traits_meta tm 
                ON pt.trait_id = tm.lvl3
            WHERE p.work_species_norm = ?
            ORDER BY tm.category;
        """, (plant_name_scientific_reference_normalize,))
        rows = cursor.fetchall()
        output_items = []
        for row in rows:
            output_item = trait_create(
                plant_name_scientific_reference = row[0],
                plant_name_scientific_reference_normalize = row[1],
                plant_genus = row[2],
                plant_author = row[3],
                trait_category = row[4],
                trait_1 = row[5],
                trait_2 = row[6],
                trait_units = row[7],
                trait_type = row[8],
                trait_value = row[9],
                trait_agreement = row[10],
                trait_coeff_var = row[11],
                trait_n = row[12],
                trait_refs = row[13],
                source_name = 'Global Inventory of Floras and Traits',
                source_acronym = 'GIFT',
            )
            output_items.append(output_item)
            # print(json.dumps(output_item, indent=4))
            # quit()
        output_filepath = f'{output_folderpath}/{plant_name_scientific_reference_normalize}.json'
        io.json_write(output_filepath, output_items)
        if output_items != []:
            output_items_last = output_items
    conn.close()
    print(json.dumps(output_items_last, indent=4))
    # quit()

def analyze_traits(schema_item):
    master_plants_rows = masterize_utils.masterize_plants_get_all()
    conn = sqlite3.connect(f"{HUB_FOLDERPATH}/reference/gift/gift.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    output_items_last = []
    category_lst = []
    trait1_lst = []
    trait2_lst = []
    schema_fields = schema_item['fields']
    entity_1_key = schema_fields[0]['field_name']
    relationship_key = schema_fields[1]['field_name']
    entity_2_key = schema_fields[2]['field_name']
    for i, master_plant_row in enumerate(master_plants_rows[:]):
        print(f'PARSE HERBS TRAITS ANALYZE {i}/{len(master_plants_rows)}')
        # print(master_plant_row)
        # quit()
        plant_name_scientific_reference = master_plant_row['plant_name_scientific_reference']
        plant_name_scientific_reference_normalize = master_plant_row['plant_name_scientific_reference_normalize']
        cursor.execute("""
            SELECT 
                p.work_species,
                p.work_species_norm,
                p.work_genus,
                p.work_author,
                tm.category,
                tm.trait1,
                tm.trait2,
                tm.units,
                tm.type,
                pt.trait_value,
                pt.agreement,
                pt.coeff_var,
                pt.n,
                pt.refs
            FROM species p
            JOIN traits pt 
                ON p.work_id = pt.work_id
            JOIN traits_meta tm 
                ON pt.trait_id = tm.lvl3
            WHERE p.work_species_norm = ?
            ORDER BY tm.category;
        """, (plant_name_scientific_reference_normalize,))
        rows = cursor.fetchall()
        items = [dict(row) for row in rows]
        ###
        if items != []:
            for item in items:
                category_lst.append(item['category']) 
                trait1_lst.append(item['trait1']) 
                trait2_lst.append(item['trait2']) 
        ###
        if items != []:
            for item in items:
                # print(json.dumps(item, indent=4))
                # quit()
                if item['category'] == 'Morphology':
                    output_item = {
                        f'{entity_1_key}_raw': plant_name_scientific_reference,
                        f'{relationship_key}_raw': 'has_trait',
                        f'{entity_2_key}_raw': item['trait_value'],
                        f'trait_1_name': item['trait1'],
                        f'category': 'morphology',
                    }
                    # print(json.dumps(output_item, indent=4))
                    # quit()
    category_result = [{"term": term, "count": count}for term, count in Counter(category_lst).items()]
    category_result = sorted(category_result, key=lambda x: x["count"], reverse=True)
    trait1_result = [{"term": term, "count": count}for term, count in Counter(trait1_lst).items()]
    trait1_result = sorted(trait1_result, key=lambda x: x["count"], reverse=True)
    # print(json.dumps(category_result, indent=4))
    # print(json.dumps(trait1_result, indent=4))
    # quit()

def analyze_traits_morphology():
    master_plants_rows = masterize_utils.masterize_plants_get_all()
    conn = sqlite3.connect(f"{HUB_FOLDERPATH}/reference/gift/gift.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    output_items_last = []
    trait1_lst = []
    trait2_lst = []
    for i, master_plant_row in enumerate(master_plants_rows[:]):
        print(f'PARSE HERBS TRAITS ANALYZE MORPHOLOGY {i}/{len(master_plants_rows)}')
        # print(master_plant_row)
        # quit()
        plant_name_scientific_reference = master_plant_row['plant_name_scientific_reference']
        plant_name_scientific_reference_normalize = master_plant_row['plant_name_scientific_reference_normalize']
        cursor.execute("""
            SELECT 
                p.work_species,
                p.work_species_norm,
                p.work_genus,
                p.work_author,
                tm.category,
                tm.trait1,
                tm.trait2,
                tm.units,
                tm.type,
                pt.trait_value,
                pt.agreement,
                pt.coeff_var,
                pt.n,
                pt.refs
            FROM species p
            JOIN traits pt 
                ON p.work_id = pt.work_id
            JOIN traits_meta tm 
                ON pt.trait_id = tm.lvl3
            WHERE p.work_species_norm = ?
            ORDER BY tm.category;
        """, (plant_name_scientific_reference_normalize,))
        rows = cursor.fetchall()
        items = [dict(row) for row in rows]
        ###
        if items != []:
            for item in items:
                if item['category'] == 'Morphology':
                    trait1_lst.append(item['trait1']) 
                    trait2_lst.append(item['trait2']) 
    trait1_result = [{"term": term, "count": count}for term, count in Counter(trait1_lst).items()]
    trait1_result = sorted(trait1_result, key=lambda x: x["count"], reverse=True)
    print(json.dumps(trait1_result, indent=4))
    trait2_result = [{"term": term, "count": count}for term, count in Counter(trait2_lst).items()]
    trait2_result = sorted(trait2_result, key=lambda x: x["count"], reverse=True)
    # print(json.dumps(trait2_result, indent=4))
    # quit()

def analyze_traits_morphology_growth_form():
    master_plants_rows = masterize_utils.masterize_plants_get_all()
    conn = sqlite3.connect(f"{HUB_FOLDERPATH}/reference/gift/gift.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    output_items_last = []
    trait1_lst = []
    trait2_lst = []
    type_lst = []
    trait_value_lst = []
    for i, master_plant_row in enumerate(master_plants_rows[:]):
        print(f'PARSE HERBS TRAITS ANALYZE MORPHOLOGY {i}/{len(master_plants_rows)}')
        # print(master_plant_row)
        # quit()
        plant_name_scientific_reference = master_plant_row['plant_name_scientific_reference']
        plant_name_scientific_reference_normalize = master_plant_row['plant_name_scientific_reference_normalize']
        cursor.execute("""
            SELECT 
                p.work_species,
                p.work_species_norm,
                p.work_genus,
                p.work_author,
                tm.category,
                tm.trait1,
                tm.trait2,
                tm.units,
                tm.type,
                pt.trait_value,
                pt.agreement,
                pt.coeff_var,
                pt.n,
                pt.refs
            FROM species p
            JOIN traits pt 
                ON p.work_id = pt.work_id
            JOIN traits_meta tm 
                ON pt.trait_id = tm.lvl3
            WHERE p.work_species_norm = ?
            ORDER BY tm.category;
        """, (plant_name_scientific_reference_normalize,))
        rows = cursor.fetchall()
        items = [dict(row) for row in rows]
        ###
        if items != []:
            for item in items:
                if (
                    item['category'] == 'Morphology' and
                    item['trait1'] == 'Growth form'
                ):
                    trait1_lst.append(item['trait1']) 
                    trait2_lst.append(item['trait2']) 
                    type_lst.append(item['type']) 
                    trait_value_lst.append(item['trait_value']) 
    '''
    trait1_result = [{"term": term, "count": count}for term, count in Counter(trait1_lst).items()]
    trait1_result = sorted(trait1_result, key=lambda x: x["count"], reverse=True)
    print(json.dumps(trait1_result, indent=4))
    '''
    trait2_result = [{"term": term, "count": count}for term, count in Counter(trait2_lst).items()]
    trait2_result = sorted(trait2_result, key=lambda x: x["count"], reverse=True)
    print(json.dumps(trait2_result, indent=4))
    ###
    type_result = [{"term": term, "count": count}for term, count in Counter(type_lst).items()]
    type_result = sorted(type_result, key=lambda x: x["count"], reverse=True)
    print(json.dumps(type_result, indent=4))
    ###
    trait_value_result = [{"term": term, "count": count}for term, count in Counter(trait_value_lst).items()]
    trait_value_result = sorted(trait_value_result, key=lambda x: x["count"], reverse=True)
    print(json.dumps(trait_value_result, indent=4))
    # quit()

def analyze_traits_morphology_climber():
    master_plants_rows = masterize_utils.masterize_plants_get_all()
    conn = sqlite3.connect(f"{HUB_FOLDERPATH}/reference/gift/gift.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    output_items_last = []
    trait1_lst = []
    trait2_lst = []
    type_lst = []
    trait_value_lst = []
    for i, master_plant_row in enumerate(master_plants_rows[:]):
        print(f'PARSE HERBS TRAITS ANALYZE CLIMBER {i}/{len(master_plants_rows)}')
        # print(master_plant_row)
        # quit()
        plant_name_scientific_reference = master_plant_row['plant_name_scientific_reference']
        plant_name_scientific_reference_normalize = master_plant_row['plant_name_scientific_reference_normalize']
        cursor.execute("""
            SELECT 
                p.work_species,
                p.work_species_norm,
                p.work_genus,
                p.work_author,
                tm.category,
                tm.trait1,
                tm.trait2,
                tm.units,
                tm.type,
                pt.trait_value,
                pt.agreement,
                pt.coeff_var,
                pt.n,
                pt.refs
            FROM species p
            JOIN traits pt 
                ON p.work_id = pt.work_id
            JOIN traits_meta tm 
                ON pt.trait_id = tm.lvl3
            WHERE p.work_species_norm = ?
            ORDER BY tm.category;
        """, (plant_name_scientific_reference_normalize,))
        rows = cursor.fetchall()
        items = [dict(row) for row in rows]
        ###
        if items != []:
            for item in items:
                if (
                    item['category'] == 'Morphology' and
                    item['trait1'] == 'Climber'
                ):
                    trait1_lst.append(item['trait1']) 
                    trait2_lst.append(item['trait2']) 
                    type_lst.append(item['type']) 
                    trait_value_lst.append(item['trait_value']) 
    '''
    trait1_result = [{"term": term, "count": count}for term, count in Counter(trait1_lst).items()]
    trait1_result = sorted(trait1_result, key=lambda x: x["count"], reverse=True)
    print(json.dumps(trait1_result, indent=4))
    '''
    trait2_result = [{"term": term, "count": count}for term, count in Counter(trait2_lst).items()]
    trait2_result = sorted(trait2_result, key=lambda x: x["count"], reverse=True)
    print(json.dumps(trait2_result, indent=4))
    ###
    type_result = [{"term": term, "count": count}for term, count in Counter(type_lst).items()]
    type_result = sorted(type_result, key=lambda x: x["count"], reverse=True)
    print(json.dumps(type_result, indent=4))
    ###
    trait_value_result = [{"term": term, "count": count}for term, count in Counter(trait_value_lst).items()]
    trait_value_result = sorted(trait_value_result, key=lambda x: x["count"], reverse=True)
    print(json.dumps(trait_value_result, indent=4))
    # quit()

def parse_traits_category_morphology():
    ## TODO
    schema_table_name = schema_item['table_name']
    schema_fields = schema_item['fields']
    output_folderpath = f'{HUB_FOLDERPATH}/parse/gift/{schema_table_name}/json'
    if schema_item['regen'] == True:
        try: shutil.rmtree(output_folderpath)
        except: pass
    io.folders_recursive_gen(output_folderpath)
    ###
    master_plants_rows = masterize_utils.masterize_plants_get_all()
    conn = sqlite3.connect(f"{HUB_FOLDERPATH}/reference/gift/gift.db")
    cursor = conn.cursor()
    output_items_last = []
    for i, master_plant_row in enumerate(master_plants_rows[:]):
        print(f'PARSE HERBS TRAITS {i}/{len(master_plants_rows)}')
        # print(master_plant_row)
        # quit()
        plant_name_scientific_reference = master_plant_row['plant_name_scientific_reference']
        plant_name_scientific_reference_normalize = master_plant_row['plant_name_scientific_reference_normalize']
        cursor.execute("""
            SELECT 
                p.work_species,
                p.work_species_norm,
                p.work_genus,
                p.work_author,
                tm.category,
                tm.trait1,
                tm.trait2,
                tm.units,
                tm.type,
                pt.trait_value,
                pt.agreement,
                pt.coeff_var,
                pt.n,
                pt.refs
            FROM species p
            JOIN traits pt 
                ON p.work_id = pt.work_id
            JOIN traits_meta tm 
                ON pt.trait_id = tm.lvl3
            WHERE p.work_species_norm = ?
            ORDER BY tm.category;
        """, (plant_name_scientific_reference_normalize,))
        rows = cursor.fetchall()
        output_items = []
        for row in rows:
            output_item = trait_create(
                plant_name_scientific_reference = row[0],
                plant_name_scientific_reference_normalize = row[1],
                plant_genus = row[2],
                plant_author = row[3],
                trait_category = row[4],
                trait_1 = row[5],
                trait_2 = row[6],
                trait_units = row[7],
                trait_type = row[8],
                trait_value = row[9],
                trait_agreement = row[10],
                trait_coeff_var = row[11],
                trait_n = row[12],
                trait_refs = row[13],
                source_name = 'Global Inventory of Floras and Traits',
                source_acronym = 'GIFT',
            )
            output_items.append(output_item)
            # print(json.dumps(output_item, indent=4))
            # quit()
        output_filepath = f'{output_folderpath}/{plant_name_scientific_reference_normalize}.json'
        io.json_write(output_filepath, output_items)
        if output_items != []:
            output_items_last = output_items
    conn.close()
    print(json.dumps(output_items_last, indent=4))
    # quit()

def schema_parse_growth_form(schema_item):
    schema_table_name = schema_item['table_name']
    schema_fields = schema_item['fields']
    entity_1_key = schema_fields[0]['field_name']
    relationship_key = schema_fields[1]['field_name']
    entity_2_key = schema_fields[2]['field_name']
    ###
    output_folderpath = f'{HUB_FOLDERPATH}/parse/gift/{schema_table_name}/json'
    if schema_item['regen'] == True:
        try: shutil.rmtree(output_folderpath)
        except: pass
    io.folders_recursive_gen(output_folderpath)
    ###
    master_plants_rows = masterize_utils.masterize_plants_get_all()
    conn = sqlite3.connect(f"{HUB_FOLDERPATH}/reference/gift/gift.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    output_items_last = []
    trait1_lst = []
    trait2_lst = []
    type_lst = []
    trait_value_lst = []
    last = []
    for i, master_plant_row in enumerate(master_plants_rows[:]):
        print(f'PARSE HERBS traits morphology {i}/{len(master_plants_rows)}')
        # print(master_plant_row)
        # quit()
        plant_name_scientific_reference = master_plant_row['plant_name_scientific_reference']
        plant_name_scientific_reference_normalize = master_plant_row['plant_name_scientific_reference_normalize']
        cursor.execute("""
            SELECT 
                p.work_species,
                p.work_species_norm,
                p.work_genus,
                p.work_author,
                tm.category,
                tm.trait1,
                tm.trait2,
                tm.units,
                tm.type,
                pt.trait_value,
                pt.agreement,
                pt.coeff_var,
                pt.n,
                pt.refs
            FROM species p
            JOIN traits pt 
                ON p.work_id = pt.work_id
            JOIN traits_meta tm 
                ON pt.trait_id = tm.lvl3
            WHERE p.work_species_norm = ?
            ORDER BY tm.category;
        """, (plant_name_scientific_reference_normalize,))
        rows = cursor.fetchall()
        items = [dict(row) for row in rows]
        ###
        output_items = []
        if items != []:
            for item in items:
                if (
                    item['category'] == 'Morphology' and
                    item['trait1'] == 'Growth form'
                ):
                    trait1_lst.append(item['trait1']) 
                    trait2_lst.append(item['trait2']) 
                    type_lst.append(item['type']) 
                    trait_value_lst.append(item['trait_value']) 
                if (
                    item['category'] == 'Morphology' and
                    item['trait1'] == 'Growth form'
                ):
                    output_item = {
                        f'{entity_1_key}_raw': plant_name_scientific_reference,
                        f'{relationship_key}_raw': 'has_growth_form',
                        f'{entity_2_key}_raw': item['trait_value'],
                        f'trait_1_name': item['trait1'].lower(),
                        f'category': 'morphology',
                        f'source_name': 'Global Inventory of Floras and Traits',
                        f'source_acronym': 'GIFT',
                        f'reference_id': '',
                        f'reference_name': '',
                    }
                    # print(json.dumps(output_item, indent=4))
                    # quit()
            output_items.append(output_item)
            # print(json.dumps(output_item, indent=4))
            # quit()
        output_filepath = f'{output_folderpath}/{plant_name_scientific_reference_normalize}.json'
        io.json_write(output_filepath, output_items)
        if output_items != []:
            last = output_items
            # print(json.dumps(output_items, indent=4))
            # quit()
    conn.close()
    '''
    trait1_result = [{"term": term, "count": count}for term, count in Counter(trait1_lst).items()]
    trait1_result = sorted(trait1_result, key=lambda x: x["count"], reverse=True)
    print(json.dumps(trait1_result, indent=4))
    trait2_result = [{"term": term, "count": count}for term, count in Counter(trait2_lst).items()]
    trait2_result = sorted(trait2_result, key=lambda x: x["count"], reverse=True)
    print(json.dumps(trait2_result, indent=4))
    ###
    type_result = [{"term": term, "count": count}for term, count in Counter(type_lst).items()]
    type_result = sorted(type_result, key=lambda x: x["count"], reverse=True)
    print(json.dumps(type_result, indent=4))
    ###
    trait_value_result = [{"term": term, "count": count}for term, count in Counter(trait_value_lst).items()]
    trait_value_result = sorted(trait_value_result, key=lambda x: x["count"], reverse=True)
    print(json.dumps(trait_value_result, indent=4))
    '''
    print(json.dumps(last, indent=4))
    # quit()

def schema_parse_climber(schema_item):
    schema_table_name = schema_item['table_name']
    schema_fields = schema_item['fields']
    entity_1_key = schema_fields[0]['field_name']
    relationship_key = schema_fields[1]['field_name']
    entity_2_key = schema_fields[2]['field_name']
    ###
    output_folderpath = f'{HUB_FOLDERPATH}/parse/gift/{schema_table_name}/json'
    if schema_item['regen'] == True:
        try: shutil.rmtree(output_folderpath)
        except: pass
    io.folders_recursive_gen(output_folderpath)
    ###
    master_plants_rows = masterize_utils.masterize_plants_get_all()
    conn = sqlite3.connect(f"{HUB_FOLDERPATH}/reference/gift/gift.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    output_items_last = []
    trait1_lst = []
    trait2_lst = []
    type_lst = []
    trait_value_lst = []
    last = []
    for i, master_plant_row in enumerate(master_plants_rows[:]):
        print(f'PARSE HERBS traits morphology climber {i}/{len(master_plants_rows)}')
        # print(master_plant_row)
        # quit()
        plant_name_scientific_reference = master_plant_row['plant_name_scientific_reference']
        plant_name_scientific_reference_normalize = master_plant_row['plant_name_scientific_reference_normalize']
        cursor.execute("""
            SELECT 
                p.work_species,
                p.work_species_norm,
                p.work_genus,
                p.work_author,
                tm.category,
                tm.trait1,
                tm.trait2,
                tm.units,
                tm.type,
                pt.trait_value,
                pt.agreement,
                pt.coeff_var,
                pt.n,
                pt.refs
            FROM species p
            JOIN traits pt 
                ON p.work_id = pt.work_id
            JOIN traits_meta tm 
                ON pt.trait_id = tm.lvl3
            WHERE p.work_species_norm = ?
            ORDER BY tm.category;
        """, (plant_name_scientific_reference_normalize,))
        rows = cursor.fetchall()
        items = [dict(row) for row in rows]
        ###
        output_items = []
        if items != []:
            for item in items:
                if (
                    item['category'] == 'Morphology' and
                    item['trait1'] == 'Climber'
                ):
                    trait1_lst.append(item['trait1']) 
                    trait2_lst.append(item['trait2']) 
                    type_lst.append(item['type']) 
                    trait_value_lst.append(item['trait_value']) 
                if (
                    item['category'] == 'Morphology' and
                    item['trait1'] == 'Climber'
                ):
                    output_item = {
                        f'{entity_1_key}_raw': plant_name_scientific_reference,
                        f'{relationship_key}_raw': 'is_climber',
                        f'{entity_2_key}_raw': item['trait_value'],
                        f'trait_1_name': item['trait1'].lower(),
                        f'category': 'morphology',
                        f'source_name': 'Global Inventory of Floras and Traits',
                        f'source_acronym': 'GIFT',
                        f'reference_id': '',
                        f'reference_name': '',
                    }
                    # print(json.dumps(output_item, indent=4))
                    # quit()
            output_items.append(output_item)
            # print(json.dumps(output_item, indent=4))
            # quit()
        output_filepath = f'{output_folderpath}/{plant_name_scientific_reference_normalize}.json'
        io.json_write(output_filepath, output_items)
        if output_items != []:
            last = output_items
            # print(json.dumps(output_items, indent=4))
            # quit()
    conn.close()
    print(json.dumps(last, indent=4))
    # quit()

def schema_parse_height(schema_item):
    schema_table_name = schema_item['table_name']
    schema_fields = schema_item['fields']
    entity_1_key = schema_fields[0]['field_name']
    relationship_key = schema_fields[1]['field_name']
    entity_2_key = schema_fields[2]['field_name']
    ###
    output_folderpath = f'{HUB_FOLDERPATH}/parse/gift/{schema_table_name}/json'
    if schema_item['regen'] == True:
        try: shutil.rmtree(output_folderpath)
        except: pass
    io.folders_recursive_gen(output_folderpath)
    ###
    master_plants_rows = masterize_utils.masterize_plants_get_all()
    conn = sqlite3.connect(f"{HUB_FOLDERPATH}/reference/gift/gift.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    output_items_last = []
    trait1_lst = []
    trait2_lst = []
    type_lst = []
    trait_value_lst = []
    last = []
    for i, master_plant_row in enumerate(master_plants_rows[:]):
        print(f'PARSE HERBS traits morphology climber {i}/{len(master_plants_rows)}')
        # print(master_plant_row)
        # quit()
        plant_name_scientific_reference = master_plant_row['plant_name_scientific_reference']
        plant_name_scientific_reference_normalize = master_plant_row['plant_name_scientific_reference_normalize']
        cursor.execute("""
            SELECT 
                p.work_species,
                p.work_species_norm,
                p.work_genus,
                p.work_author,
                tm.category,
                tm.trait1,
                tm.trait2,
                tm.units,
                tm.type,
                pt.trait_value,
                pt.agreement,
                pt.coeff_var,
                pt.n,
                pt.refs
            FROM species p
            JOIN traits pt 
                ON p.work_id = pt.work_id
            JOIN traits_meta tm 
                ON pt.trait_id = tm.lvl3
            WHERE p.work_species_norm = ?
            ORDER BY tm.category;
        """, (plant_name_scientific_reference_normalize,))
        rows = cursor.fetchall()
        items = [dict(row) for row in rows]
        ###
        output_items = []
        if items != []:
            for item in items:
                if (
                    item['category'] == 'Morphology' and
                    item['trait1'] == 'Plant height'
                ):
                    trait1_lst.append(item['trait1']) 
                    trait2_lst.append(item['trait2']) 
                    type_lst.append(item['type']) 
                    trait_value_lst.append(item['trait_value']) 
                if (
                    item['category'] == 'Morphology' and
                    item['trait1'] == 'Plant height'
                ):
                    if item['trait2'] == 'Plant_height_min': relationship_name = 'has_height_min'
                    elif item['trait2'] == 'Plant_height_max': relationship_name = 'has_height_max'
                    output_item = {
                        f'{entity_1_key}_raw': plant_name_scientific_reference,
                        f'{relationship_key}_raw': relationship_name,
                        f'{entity_2_key}_raw': item['trait_value'] + ' ' + item['units'],
                        f'trait_1_name': item['trait1'].lower(),
                        f'category': 'morphology',
                        f'source_name': 'Global Inventory of Floras and Traits',
                        f'source_acronym': 'GIFT',
                        f'reference_id': '',
                        f'reference_name': '',
                    }
                    # print(json.dumps(item, indent=4))
                    # print(json.dumps(output_item, indent=4))
                    # quit()
                    output_items.append(output_item)
            # print(json.dumps(output_item, indent=4))
            # quit()
        output_filepath = f'{output_folderpath}/{plant_name_scientific_reference_normalize}.json'
        io.json_write(output_filepath, output_items)
        if output_items != []:
            last = output_items
            # print(json.dumps(output_items, indent=4))
            # quit()
    conn.close()
    print(json.dumps(last, indent=4))
    # quit()

def run():
    print(f'''HERBS >> PARSE >> gift''')
    
    # analyze_traits_morphology()
    # analyze_traits_morphology_growth_form()
    # analyze_traits_morphology_climber()
    # quit()

    """
    schema_items = schema_herbs.data['items']
    for schema_item in schema_items: 
        if schema_item['process'] != True: continue
        sources_names = [
            source['source_name'] 
            for source in schema_item['sources']
        ]
        if 'gift' not in sources_names: continue
        if schema_item['table_name'] == 'plants_traits':
            # schema_parse_traits(schema_item)
            analyze_traits(schema_item)
    """

    schema_items = schema_herbs.data['items']
    for schema_item in schema_items: 
        if schema_item['process'] != True: continue
        sources_names = [
            source['source_name'] 
            for source in schema_item['sources']
        ]
        if 'gift' not in sources_names: continue
        ### morphology
        if schema_item['table_name'] == 'plants_growth_forms': schema_parse_growth_form(schema_item)
        elif schema_item['table_name'] == 'plants_climbers': schema_parse_climber(schema_item)
        elif schema_item['table_name'] == 'plants_heights': schema_parse_height(schema_item)

    # quit()
