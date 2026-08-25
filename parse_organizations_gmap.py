import os
import ast
import time
import json
import shutil

from bs4 import BeautifulSoup

from lib import g
from lib import io
from lib import llm
from lib import polish

import parse_utils
import parse_organizations_data
import parse_organizations_reviews_data

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

def parse_gmap_backup():
    start = 0
    end = 100
    ###
    output_folderpath = f'{g.DATA_FOLDERPATH}/organizations/parse/gmap/details/json'
    try: shutil.rmtree(output_folderpath)
    except: pass
    io.folders_recursive_gen(output_folderpath)
    ###
    reviews_output_folderpath = f'{g.DATA_FOLDERPATH}/organizations/parse/gmap/reviews/json'
    try: shutil.rmtree(reviews_output_folderpath)
    except: pass
    io.folders_recursive_gen(reviews_output_folderpath)
    ###
    input_foldername = f'{HUB_FOLDERPATH}/fetch/gmap/america/places'.replace(' ', '_')
    input_filenames = sorted(os.listdir(input_foldername))
    options = set()
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
                gmap_phone = values[3]
                gmap_name = values[4]
                gmap_info = values[5]
                gmap_business_map = values[6]
                slug = to_slug(gmap_label)

                info_lst = result = ast.literal_eval(gmap_info)
                gmap_rating = None
                gmap_reviews_num = None
                gmap_business_type_primary = None
                if len(info_lst) == 1:
                    gmap_business_type_primary = info_lst[0]
                elif len(info_lst) == 4:
                    gmap_rating = info_lst[0]
                    gmap_reviews_num = info_lst[1]
                    gmap_business_type_primary = info_lst[3]

                if gmap_rating == None: continue
                
                print(f'gmap_label: {gmap_label}')
                print(f'gmap_address: {gmap_address}')
                print(f'gmap_website: {gmap_website}')
                print(f'gmap_phone: {gmap_phone}')
                print(f'gmap_name: {gmap_name}')
                print(f'gmap_info: {gmap_info}')
                print(f'gmap_slug: {slug}')
                print(f'***************************************')
                print()
                # quit()

                ################################################################################
                # DETAILS
                ################################################################################
                fields_data = parse_organizations_data.data

                output_items = []
                output_item = {}
                for field_item in fields_data:
                    reply = None
                    if field_item['field_name'] == 'business_name_raw': reply = gmap_name
                    elif field_item['field_name'] == 'business_gmap_name_raw': reply = gmap_name
                    elif field_item['field_name'] == 'business_website': reply = gmap_website
                    elif field_item['field_name'] == 'business_address': reply = gmap_address
                    elif field_item['field_name'] == 'business_phone': reply = gmap_phone
                    elif field_item['field_name'] == 'business_rating': reply = gmap_rating
                    elif field_item['field_name'] == 'business_reviews_num': reply = gmap_reviews_num
                    elif field_item['field_name'] == 'business_type_primary': reply = gmap_business_type_primary
                    elif field_item['field_name'] == 'business_map': reply = gmap_business_map
                    key = field_item['field_name']
                    val = reply
                    output_item[key] = val

                output_item['source_name'] = 'Google Maps'
                output_item['source_acronym'] = 'GM'

                output_filepath = f'{output_folderpath}/{slug}.json'
                output_items.append(output_item)
                io.json_write(output_filepath, output_items)

                # print(json.dumps(output_items, indent=4))
                # quit()

                ################################################################################
                # REVIEWS
                ################################################################################
                html_folderpath = f'{g.DATA_FOLDERPATH}/organizations/fetch/gmap/america/htmls'
                html_filepath = f'{html_folderpath}/{gmap_name}.html'
                html = io.file_read(html_filepath)
                # print(html_filepath)
                # quit()
                soup = BeautifulSoup(html, "html.parser")

                fields_data = parse_organizations_reviews_data.fields

                elements = soup.find_all(
                    attrs={
                        "data-review-id": True,
                        "class": lambda classes: classes and "fontBodyMedium" in classes
                    }
                )

                reviews_output_items = []
                for element in elements:
                    element_card_body = element.find(
                        attrs={
                            "data-irrelevant-review-text-id": True,
                        }
                    )
                    # print(element_card_body.get_text(separator="\n", strip=True))
                    print(element_card_body.find_all("div")[0].get_text(separator="\n", strip=True))
                    print(element_card_body.find_all("div")[1].get_text(separator="\n", strip=True))
                    print(element_card_body.find_all("div")[2].get_text(separator="\n", strip=True))
                    print(element_card_body.find_all("div")[3].get_text(separator="\n", strip=True))
                    # print(element_card_body.find_all("div")[4].get_text(separator="\n", strip=True))
                    # print(element_card_body.find_all("div")[5].get_text(separator="\n", strip=True))
                    # print(element_card_body.find_all("div")[6].get_text(separator="\n", strip=True))
                    # print(element_card_body.find_all("div")[7].get_text(separator="\n", strip=True))
                    # print(element_card_body.find_all("div")[8].get_text(separator="\n", strip=True))
                    # print(element_card_body.find_all("div")[9].get_text(separator="\n", strip=True))
                    # print(element_card_body.find_all("div")[10].get_text(separator="\n", strip=True))
                    # review_text = element_card_body.find_all("div")[1].get_text(separator="\n", strip=True)

                    # print(review_text)
                    gmap_business_review_text_ita = element_card_body.find_all("div")[2].get_text(separator="\n", strip=True)
                    gmap_business_review_text_eng = ''
                    prompt = f'''
                        Translate from Italian to English the following TEXT.
                        TEXT:
                        {gmap_business_review_text_ita}
                        RULES:
                        Reply only with the asked content.
                    '''.strip()
                    print(prompt)
                    reply = llm.reply(prompt, model_filepath)
                    if '</think>' in reply:
                        reply = reply.split('</think>')[1].strip()
                    reply = polish.vanilla(reply)
                    gmap_business_review_text_eng = reply

                    output_item = {}
                    for field_item in fields_data:
                        reply = None
                        if field_item['field_name'] == 'business_name_raw': reply = gmap_name
                        elif field_item['field_name'] == 'business_review_text_ita': reply = gmap_business_review_text_ita 
                        elif field_item['field_name'] == 'business_review_text_eng': reply = gmap_business_review_text_eng 
                        key = field_item['field_name']
                        val = reply
                        output_item[key] = val
                    output_item['source_name'] = 'Google Maps'
                    output_item['source_acronym'] = 'GM'

                    # print(json.dumps(output_item, indent=4))
                    # quit()

                    # output_filepath = f'{output_folderpath}/{slug}.json'
                    # output_items.append(output_item)
                    # io.json_write(output_filepath, output_items)

                    reviews_output_items.append(output_item)

                reviews_output_filepath = f'{reviews_output_folderpath}/{slug}.json'
                io.json_write(reviews_output_filepath, reviews_output_items)

                # print(json.dumps(reviews_output_items, indent=4))
                # quit()

                # print(len(elements))
                # quit()


def parse_gmap():
    start = 0
    end = 100
    ###
    output_folderpath = f'{g.DATA_FOLDERPATH}/organizations/parse/gmap/details/json'
    try: shutil.rmtree(output_folderpath)
    except: pass
    io.folders_recursive_gen(output_folderpath)
    ###
    reviews_output_folderpath = f'{g.DATA_FOLDERPATH}/organizations/parse/gmap/reviews/json'
    try: shutil.rmtree(reviews_output_folderpath)
    except: pass
    io.folders_recursive_gen(reviews_output_folderpath)
    ###
    input_foldername = f'{HUB_FOLDERPATH}/fetch/gmap/america/places'.replace(' ', '_')
    input_filenames = sorted(os.listdir(input_foldername))
    options = set()
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
                gmap_phone = values[3]
                gmap_name = values[4]
                gmap_info = values[5]
                gmap_business_map = values[6]
                slug = to_slug(gmap_label)

                info_lst = result = ast.literal_eval(gmap_info)
                gmap_rating = None
                gmap_reviews_num = None
                gmap_business_type_primary = None
                if len(info_lst) == 1:
                    gmap_business_type_primary = info_lst[0]
                elif len(info_lst) == 4:
                    gmap_rating = info_lst[0]
                    gmap_reviews_num = info_lst[1]
                    gmap_business_type_primary = info_lst[3]

                if gmap_rating == None: continue
                
                print(f'gmap_label: {gmap_label}')
                print(f'gmap_address: {gmap_address}')
                print(f'gmap_website: {gmap_website}')
                print(f'gmap_phone: {gmap_phone}')
                print(f'gmap_name: {gmap_name}')
                print(f'gmap_info: {gmap_info}')
                print(f'gmap_slug: {slug}')
                print(f'***************************************')
                print()
                # quit()

                ################################################################################
                # DETAILS
                ################################################################################
                fields_data = parse_organizations_data.data

                output_items = []
                output_item = {}
                for field_item in fields_data:
                    reply = None
                    if field_item['field_name'] == 'business_name_raw': reply = gmap_name
                    elif field_item['field_name'] == 'business_gmap_name_raw': reply = gmap_name
                    elif field_item['field_name'] == 'business_website': reply = gmap_website
                    elif field_item['field_name'] == 'business_address': reply = gmap_address
                    elif field_item['field_name'] == 'business_phone': reply = gmap_phone
                    elif field_item['field_name'] == 'business_rating': reply = gmap_rating
                    elif field_item['field_name'] == 'business_reviews_num': reply = gmap_reviews_num
                    elif field_item['field_name'] == 'business_type_primary': reply = gmap_business_type_primary
                    elif field_item['field_name'] == 'business_map': reply = gmap_business_map
                    key = field_item['field_name']
                    val = reply
                    output_item[key] = val

                output_item['source_name'] = 'Google Maps'
                output_item['source_acronym'] = 'GM'

                output_filepath = f'{output_folderpath}/{slug}.json'
                output_items.append(output_item)
                io.json_write(output_filepath, output_items)

                # print(json.dumps(output_items, indent=4))
                # quit()

                ################################################################################
                # REVIEWS
                ################################################################################
                html_folderpath = f'{g.DATA_FOLDERPATH}/organizations/fetch/gmap/america/htmls'
                html_filepath = f'{html_folderpath}/{gmap_name}.html'
                html = io.file_read(html_filepath)
                # print(html_filepath)
                # quit()
                soup = BeautifulSoup(html, "html.parser")

                fields_data = parse_organizations_reviews_data.fields

                elements = soup.find_all(
                    attrs={
                        "data-review-id": True,
                        "class": lambda classes: classes and "fontBodyMedium" in classes
                    }
                )

                reviews_output_items = []
                for element in elements:
                    element_card_body = element.find(
                        attrs={
                            "data-irrelevant-review-text-id": True,
                        }
                    )
                    # print(element_card_body.get_text(separator="\n", strip=True))
                    print(element_card_body.find_all("div")[0].get_text(separator="\n", strip=True))
                    print(element_card_body.find_all("div")[1].get_text(separator="\n", strip=True))
                    print(element_card_body.find_all("div")[2].get_text(separator="\n", strip=True))
                    print(element_card_body.find_all("div")[3].get_text(separator="\n", strip=True))
                    # print(element_card_body.find_all("div")[4].get_text(separator="\n", strip=True))
                    # print(element_card_body.find_all("div")[5].get_text(separator="\n", strip=True))
                    # print(element_card_body.find_all("div")[6].get_text(separator="\n", strip=True))
                    # print(element_card_body.find_all("div")[7].get_text(separator="\n", strip=True))
                    # print(element_card_body.find_all("div")[8].get_text(separator="\n", strip=True))
                    # print(element_card_body.find_all("div")[9].get_text(separator="\n", strip=True))
                    # print(element_card_body.find_all("div")[10].get_text(separator="\n", strip=True))
                    # review_text = element_card_body.find_all("div")[1].get_text(separator="\n", strip=True)

                    ### GET REVIEW STARS
                    stars = element.select_one('[aria-label*="stelle"]')
                    if stars:
                        stars = stars.get("aria-label")
                    else:
                        stars = element.select_one('[aria-label*="stella"]')
                        if stars:
                            stars = stars.get("aria-label")
                    gmap_business_review_stars = stars
                    gmap_business_review_stars = gmap_business_review_stars.replace('stelle', '').strip()
                    gmap_business_review_stars = gmap_business_review_stars.replace('stella', '').strip()
                    # print(gmap_business_review_stars)

                    ### GET REVIEW AUTHOR NAME
                    button = element.select_one(
                        'button[data-href*="https://www.google.com/maps/contrib"]:not([aria-label])'
                    )
                    first_div = button.find("div")
                    gmap_business_review_author_name = first_div.get_text(separator="\n", strip=True)

                    # print(review_text)
                    gmap_business_review_text_ita = element_card_body.find_all("div")[2].get_text(separator="\n", strip=True)
                    gmap_business_review_text_eng = ''
                    prompt = f'''
                        Translate from Italian to English the following TEXT.
                        TEXT:
                        {gmap_business_review_text_ita}
                        RULES:
                        Reply only with the asked content.
                    '''.strip()
                    print(prompt)
                    reply = llm.reply(prompt, model_filepath)
                    if '</think>' in reply:
                        reply = reply.split('</think>')[1].strip()
                    reply = polish.vanilla(reply)
                    gmap_business_review_text_eng = reply

                    output_item = {}
                    for field_item in fields_data:
                        reply = None
                        if field_item['field_name'] == 'business_name_raw': reply = gmap_name
                        elif field_item['field_name'] == 'business_review_stars': reply = gmap_business_review_stars 
                        elif field_item['field_name'] == 'business_review_author_name': reply = gmap_business_review_author_name 
                        elif field_item['field_name'] == 'business_review_text_ita': reply = gmap_business_review_text_ita 
                        elif field_item['field_name'] == 'business_review_text_eng': reply = gmap_business_review_text_eng 
                        key = field_item['field_name']
                        val = reply
                        output_item[key] = val
                    output_item['source_name'] = 'Google Maps'
                    output_item['source_acronym'] = 'GM'

                    # print(json.dumps(output_item, indent=4))
                    # quit()

                    # output_filepath = f'{output_folderpath}/{slug}.json'
                    # output_items.append(output_item)
                    # io.json_write(output_filepath, output_items)

                    reviews_output_items.append(output_item)

                reviews_output_filepath = f'{reviews_output_folderpath}/{slug}.json'
                io.json_write(reviews_output_filepath, reviews_output_items)

                # print(json.dumps(reviews_output_items, indent=4))
                # quit()

                # print(len(elements))
                # quit()


def analyze_businesses_types():
    start = 0
    end = 100
    input_foldername = f'{HUB_FOLDERPATH}/fetch/gmap/america/places'.replace(' ', '_')
    input_filenames = sorted(os.listdir(input_foldername))
    i = 0
    strings = []
    for input_filename in input_filenames[start:end]:
        print(f'{start+i}/{end}')
        i += 1
        input_filename_base = input_filename.split('.')[0].strip()
        input_filepath = f'{input_foldername}/{input_filename}'
        with open(input_filepath, encoding="utf-8") as f: rows = f.read().strip().split('\n')
        for row in rows:
            values = row.split('~')
            if values != [] and values != ['']:
                gmap_info = values[5]
                info_lst = result = ast.literal_eval(gmap_info)

                gmap_business_type_primary = None
                if len(info_lst) == 1:
                    gmap_business_type_primary = info_lst[0]
                elif len(info_lst) == 4:
                    gmap_business_type_primary = info_lst[3]
                print(gmap_business_type_primary)

                def clean(s):
                    if s is None:
                        return s
                    return re.sub(r"[^\w\s]+$", "", s).strip()

                gmap_business_type_primary = clean(gmap_business_type_primary)

                strings.append(gmap_business_type_primary)

    print('###########################################################')
    from collections import Counter
    counts = Counter(strings)
    for s, count in counts.most_common():
        print(f"{s}: {count}")

def run():
    print(f'ORGANIZATION >> PARSE >> gmap')

    start = time.perf_counter()
    # parse_gmap_backup()
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

    # analyze_businesses_types()
    # quit()
