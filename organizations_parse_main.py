import os
import ast
import time
import json
import shutil

from lib import g
from lib import io
from lib import llm

import parse_utils

import re
import unicodedata

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
    input_foldername = f'{g.DATA_FOLDERPATH}/organizations/fetch/gmap/america/places'.replace(' ', '_')
    input_filenames = sorted(os.listdir(input_foldername))
    for input_filename in input_filenames[:10]:
        input_filepath = f'{input_foldername}/{input_filename}'
        with open(input_filepath, encoding="utf-8") as f: rows = f.read().strip().split('\n')
        for row in rows:
            values = row.split('~')
            print(values)
            if values != [] and values != ['']:
                label = values[0]
                address = values[1]
                website = values[2]
                phone = values[3]
                name = values[4]
                info = values[5]
                slug = to_slug(label)
                print(f'label: {label}')
                print(f'address: {address}')
                print(f'website: {website}')
                print(f'phone: {phone}')
                print(f'name: {name}')
                print(f'info: {info}')
                print(f'slug: {slug}')
                print(f'***************************************')
                print()
                print(info)

                lst = ast.literal_eval(info)
                if 'Erborista' in lst:
                    # print('found')
                    slug = to_slug(label)
                    # print(slug)

                # quit()
        # print(json.dumps(item, indent=4))
    quit()

def run():
    print(f'ORGANIZATION >> PARSE >> main')

    start = time.perf_counter()
    parse_gmap()
    print(f'parse activities() - execution time: ', time.perf_counter() - start)

