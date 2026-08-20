import os
import json
import time
import shutil

import re
import unicodedata

from lib import g
from lib import io

import normalize_utils
import parse_organizations_data
'''
    {
        'field_name': 'business_name_normalize',
        'field_query': 'normalized business name', 
        'field_description': '', 
        'field_type': '',
        'field_normalize': 'normalize',
        'field_normalize_ref': 'business_name_official',
    },
    {
        'field_name': 'business_name_display',
        'field_query': 'display business name', 
        'field_description': '', 
        'field_type': '',
        'field_normalize': 'display',
        'field_normalize_ref': 'business_name_official',
    },
    {
        'field_name': 'business_name_slug',
        'field_query': 'business slug', 
        'field_description': '', 
        'field_type': '',
        'field_normalize': 'slug',
        'field_normalize_ref': 'business_name_official',
    },
'''

HUB_FOLDERPATH = f'{g.DATA_FOLDERPATH}/organizations'

def normalize_name(name_raw: str) -> str:
    """
    Convert a raw USDA operation name into a clean canonical name.
    Example:
        '"BREDUN" LP' -> 'BREDUN LP'
    """
    if not name_raw: return ""
    # Normalize Unicode characters
    name = unicodedata.normalize("NFKC", name_raw)
    # Remove surrounding quotation marks
    name = name.replace('"', '').replace("'", "")
    # Collapse multiple whitespace characters
    name = re.sub(r"\s+", " ", name)
    return name.strip()

def normalize_gen(name):
    name = unicodedata.normalize("NFKC", name).casefold()
    name = re.sub(r"[^\w\s]", "", name)
    name = re.sub(r"\s+", " ", name)
    return name.strip()

def display_name_gen(text):
    # Good default, but don't treat this as authoritative branding.
    text = unicodedata.normalize("NFKC", text)
    text = re.sub(r"[®™©]", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text

def slug_gen(text):
    text = normalize_gen(text)
    text = text.replace("'", "")
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return text.strip("-")

def normalize_businesses(source_foldername):
    input_folderpath = f'{HUB_FOLDERPATH}/parse/{source_foldername}/json'
    output_folderpath = f'{HUB_FOLDERPATH}/normalize/{source_foldername}/json'
    try: shutil.rmtree(output_folderpath)
    except: pass
    io.folders_recursive_gen(output_folderpath)
    input_filenames = os.listdir(input_folderpath)
    ###
    for i, input_filename in enumerate(input_filenames[:]):
        print(f'{i}/{len(input_filenames)}')
        output_filepath = f'{output_folderpath}/{input_filename}'
        if os.path.exists(output_filepath): continue
        ###
        input_filepath = f'{input_folderpath}/{input_filename}'
        input_data = io.json_read(input_filepath)
        for input_item in input_data:
            # print(input_item)
            input_item['business_name_normalize'] = normalize_gen(input_item['business_gmap_name_raw'])
            input_item['business_name_display'] = display_name_gen(input_item['business_gmap_name_raw'])
            input_item['business_slug'] = slug_gen(input_item['business_gmap_name_raw'])
        io.json_write(output_filepath, input_data)
    # print(json.dumps(input_item, indent=4))
    # quit()

def run():
    print('NORMALIZE >> MAIN')

    if 1:
        start = time.perf_counter()
        normalize_businesses(source_foldername='website')
        print(f'normalize businesses() - execution time: ', time.perf_counter() - start)
