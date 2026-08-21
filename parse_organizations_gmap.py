import os
import ast
import time
import json
import shutil

from bs4 import BeautifulSoup

from lib import g
from lib import io
from lib import llm

import parse_utils
import parse_organizations_data

import re
import unicodedata

HUB_FOLDERPATH = f'{g.DATA_FOLDERPATH}/organizations'

model_filepath = '/home/ubuntu/vault-tmp/llm/gemma-4-12b-it-Q4_K_S.gguf'
model_filepath = '/home/ubuntu/vault-tmp/llm/gemma-4-12B-it-qat-UD-Q4_K_XL.gguf'

_NON_ALNUM = re.compile(r"[^\w\s-]", re.UNICODE)
_SEPARATORS = re.compile(r"[-\s]+")

def to_slug(name: str) -> str:
    """Convert an organization name into a stable, URL-safe slug."""
    name = unicodedata.normalize("NFKD", name)
    name = "".join(c for c in name if not unicodedata.combining(c))
    name = name.replace("&", " and ")
    name = _NON_ALNUM.sub("", name)
    return _SEPARATORS.sub("-", name).strip("-").lower()

def parse_gmap():
    start = 0
    end = 10
    ###
    output_folderpath = f'{g.DATA_FOLDERPATH}/organizations/parse/gmap/json'
    try: shutil.rmtree(output_folderpath)
    except: pass
    io.folders_recursive_gen(output_folderpath)
    ###
    input_foldername = f'{HUB_FOLDERPATH}/fetch/gmap/america/places'.replace(' ', '_')
    input_filenames = sorted(os.listdir(input_foldername))
    i = 0
    for input_filename in input_filenames[start:end]:
        print(f'{start+i}/{end}')
        i += 1
        input_filename_base = input_filename.split('.')[0].strip()
        input_filepath = f'{input_foldername}/{input_filename}'
        with open(input_filepath, encoding="utf-8") as f: rows = f.read().strip().split('\n')
        for row in rows:
            values = row.split('~')
            if values != [] and values != ['']:
                gmap_label = values[0]
                gmap_address = values[1]
                gmap_website = values[2]
                gmap_name = values[4]
                gmap_info = values[5]
                slug = to_slug(gmap_label)
                print(f'gmap_label: {gmap_label}')
                print(f'gmap_address: {gmap_address}')
                print(f'gmap_website: {gmap_website}')
                print(f'gmap_name: {gmap_name}')
                print(f'gmap_info: {gmap_info}')
                print(f'gmap_slug: {slug}')
                print(f'***************************************')
                print()

                fields_data = parse_organizations_data.data

                output_items = []
                output_item = {}
                for field_item in fields_data:
                    reply = None
                    if field_item['field_name'] == 'business_name_raw': reply = gmap_name
                    elif field_item['field_name'] == 'business_gmap_name_raw': reply = gmap_name
                    elif field_item['field_name'] == 'business_website': reply = gmap_website
                    elif field_item['field_name'] == 'business_address': reply = gmap_address
                    key = field_item['field_name']
                    val = reply
                    output_item[key] = val

                output_item['source_name'] = 'Google Maps'
                output_item['source_acronym'] = 'GM'

                output_filepath = f'{output_folderpath}/{slug}.json'
                output_items.append(output_item)
                io.json_write(output_filepath, output_items)

def run():
    print(f'ORGANIZATION >> PARSE >> gmap')

    start = time.perf_counter()
    parse_gmap()
    print(f'''
################################################################################
parse website() - execution time: 
---
SECONDS: {(time.perf_counter() - start)}
MINUTES: {(time.perf_counter() - start)/60}
HOURS:   {(time.perf_counter() - start)/60/60}
################################################################################
    ''')

