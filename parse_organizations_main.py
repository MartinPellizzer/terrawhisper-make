import os
import ast
import time
import json
import shutil
from urllib.parse import urlsplit

from bs4 import BeautifulSoup

from lib import g
from lib import io
from lib import llm
from lib import polish

import parse_utils
import parse_organizations_data
import parse_organizations_reviews_data
import parse_organizations_herbs_data

import re
import unicodedata

start = 0
end = 1000

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

def base_url(url):
    p = urlsplit(url)
    return f"{p.scheme}://{p.netloc}/"

def llm_gen(query, description, website_text, input_len_max=0):
    if input_len_max != 0:
        website_text = website_text[:input_len_max]
    prompt = f'''
        Extract the {query} from the following text found in the business website.
        By {query} i mean {description}.
        Reply only with the {query}.
        If you can't find the requested info, reply with "NONE".
        WEBSITE TEXT:
        {website_text}
    '''.strip()
    print(f'LEN CHARS: {len(prompt)}')
    print(f'LEN WORDS: {len(prompt.split())}')
    print(f'{prompt[:1000]}')
    # quit()
    reply = llm.reply(prompt, model_filepath, max_tokens=512)
    if '</think>' in reply:
        reply = reply.split('</think>')[1].strip()
    if 'none' in reply.lower(): return None
    if reply.strip() == '': return None
    print()
    return reply

def llm_herbs_gen(website_text, input_len_max=0):
    if input_len_max != 0:
        website_text = website_text[:input_len_max]
    website_text = re.sub(r'[^\x20-\x7E]', '', website_text)
    prompt = f'''
        Extract the list of all the herbs names mentined in the content of the following WEBSITE TEXT.
        Write the herbs names exactly as the are in the website text, using as few words as possible, and capitalize case.
        Write only herbs that are written using their scientific or common names.
        Write only the names of the herbs, not their forms, preparations, parts, etc. 
        NEVER include:
        - forms (infusion, decoction, etc.)
        - preparations (oil, tea, etc.)
        - parts (seed, root, etc.)
        - other descriptors associated with the name of the herb
        Separate each herb name with a comma, only one herb name in between commas.
        Reply only with the list of herbs names.
        If you can't find the requested info, reply with "NONE".
        WEBSITE TEXT:
        {website_text}
    '''.strip()
    print(f'LEN CHARS: {len(prompt)}')
    print(f'LEN WORDS: {len(prompt.split())}')
    print(f'{prompt[:1000]}')
    reply = llm.reply(prompt, model_filepath, max_tokens=512)
    if '</think>' in reply:
        reply = reply.split('</think>')[1].strip()
    print()
    if 'none' in reply.lower(): return None
    reply_lst = [x.strip() for x in reply.split(',')]
    return reply_lst

def llm_bool_gen(query, description, website_text):
    prompt = f'''
        Tell me if this company {query} from the following text found in the business website.
        By {query} i mean {description}.
        Reply only with the "TRUE" or "FALSE".
        If you can't find the requested info, reply with "NONE".
        WEBSITE TEXT:
        {website_text}
    '''.strip()
    reply = llm.reply(prompt, model_filepath, max_tokens=512)
    if '</think>' in reply:
        reply = reply.split('</think>')[1].strip()
    reply = reply.lower()
    if 'none' in reply.lower(): reply = None
    return reply

def website_text_get(website_filepath):
    try: html = io.file_read(website_filepath)
    except: html = ''
    if html != '':
        soup = BeautifulSoup(html, "html.parser")
        website_text = soup.get_text(separator="\n", strip=True)
        website_text = website_text[:16000]
        return website_text.strip()
    return html

def parse_gmap():
    output_folderpath = f'{g.DATA_FOLDERPATH}/organizations/parse/gmap/details/json'
    # try: shutil.rmtree(output_folderpath)
    # except: pass
    io.folders_recursive_gen(output_folderpath)
    ###
    reviews_output_folderpath = f'{g.DATA_FOLDERPATH}/organizations/parse/gmap/reviews/json'
    # try: shutil.rmtree(reviews_output_folderpath)
    # except: pass
    io.folders_recursive_gen(reviews_output_folderpath)
    ###
    input_foldername = f'{HUB_FOLDERPATH}/fetch/gmap/america/places'.replace(' ', '_')
    input_filenames = sorted(os.listdir(input_foldername))
    options = set()
    i = 0
    for input_filename in input_filenames[start:end]:
        print(f'{start+i}/{end}')
        print(f'{input_filename}')
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
                output_filepath = f'{output_folderpath}/{slug}.json'
                if os.path.exists(output_filepath): continue
                ###
                gmap_website = base_url(gmap_website)
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
                # if gmap_rating == None: continue
                print(f'gmap_name: {gmap_name}')
                '''
                print(f'gmap_label: {gmap_label}')
                print(f'gmap_address: {gmap_address}')
                print(f'gmap_website: {gmap_website}')
                print(f'gmap_phone: {gmap_phone}')
                print(f'gmap_info: {gmap_info}')
                print(f'gmap_slug: {slug}')
                print(f'***************************************')
                print()
                '''
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

def parse_website():
    input_folderpath = f'{HUB_FOLDERPATH}/fetch/gmap/america/places_json'
    output_folderpath = f'{HUB_FOLDERPATH}/parse/website/details/json'
    # try: shutil.rmtree(output_folderpath)
    # except: pass
    io.folders_recursive_gen(output_folderpath)
    ###
    input_filenames = sorted(os.listdir(input_folderpath))
    for i, input_filename in enumerate(input_filenames):
        print(f'{i}/{len(input_filenames)} - {input_filename}')
        ###
        input_filename_base = input_filename.split('.')[0].strip()
        input_filepath = f'{input_folderpath}/{input_filename}'
        input_data = io.json_read(input_filepath)
        gmap_label = input_data['gmap_label']
        gmap_website = input_data['gmap_website']
        gmap_name = input_data['gmap_name']
        gmap_slug = input_data['gmap_slug']
        ###
        '''
        print(f'name: {gmap_name}')
        print(f'label: {gmap_label}')
        print(f'gmap_website: {gmap_website}')
        print(f'gmap_slug: {gmap_slug}')
        print(f'***************************************')
        print()
        '''
        ###
        output_filepath = f'{output_folderpath}/{gmap_slug}.json'
        output_data = io.json_read(output_filepath, create=True)
        if type(output_data) is list: output_data = output_data[0]
        fields_data = parse_organizations_data.data
        website_filepath = f'{HUB_FOLDERPATH}/fetch/websites/america/places_html/{gmap_slug}.html'
        print(website_filepath)
        # print(json.dumps(output_data, indent=4))
        # quit()
        ###
        ### PARSE GENERAL FIELDS
        output_item = {}
        for field_item in fields_data:
            reply = None
            if field_item['field_name'] == 'business_name_raw': reply = gmap_name
            elif field_item['field_name'] == 'business_website': reply = gmap_website
            elif field_item['field_name'] == 'business_website_html': reply = None
            elif field_item['field_name'] == 'business_website_text': reply = None
            elif field_item['field_name'] == 'business_map': reply = None
            output_item[field_item['field_name']] = reply
        # print(json.dumps(output_item, indent=4))
        # quit()
        # continue
        ### PARSE FIELD THAT REQUIRE WEBSITE
        try: html = io.file_read(website_filepath)
        except: html = ''
        if html != '':
            soup = BeautifulSoup(html, "html.parser")
            website_text = soup.get_text(separator="\n", strip=True)
            website_text = website_text[:16000]
            if website_text.strip() != '':
                output_item['business_website_text'] = 'true'
                fields_data = parse_organizations_data.data
                for field_item in fields_data:
                    reply = ''
                    if field_item['field_name'] == 'business_name_raw': reply = gmap_name
                    elif field_item['field_name'] == 'business_website': reply = gmap_website
                    elif field_item['field_name'] == 'business_website_html': reply = 'true'
                    elif field_item['field_name'] == 'business_website_text': reply = 'true'
                    elif field_item['field_name'] == 'business_map': reply = None
                    elif field_item['field_type'] == 'bool':
                        if field_item['regen'] == True:
                            reply = llm_bool_gen(
                                query=field_item['field_query'],
                                description=field_item['field_description'],
                                website_text=website_text
                            )
                        else: 
                            if field_item['field_name'] not in output_data:
                                reply = llm_bool_gen(
                                    query=field_item['field_query'],
                                    description=field_item['field_description'],
                                    website_text=website_text
                                )
                            else: 
                                reply = output_data[field_item['field_name']]
                    ###
                    elif field_item['field_type'] == 'text':
                        # print(json.dumps(output_data, indent=4))
                        # quit()
                        if field_item['regen'] == True:
                            reply = llm_gen(
                                query=field_item['field_query'],
                                description=field_item['field_description'],
                                website_text=website_text
                            )
                        else:
                            if field_item['field_name'] not in output_data:
                                reply = llm_gen(
                                    query=field_item['field_query'],
                                    description=field_item['field_description'],
                                    website_text=website_text
                                )
                            else: 
                                reply = output_data[field_item['field_name']]
                    output_item[field_item['field_name']] = reply
                ### DEBUG
                # for field_item in fields_data:
                    # if field_item['field_name'] == 'business_products':
                        # print(field_item)
                        # quit()
            else:
                output_item['business_website_text'] = 'false'
        else:
            output_item['business_website_html'] = 'false'
            output_item['business_website_text'] = 'false'
        output_item['source_name'] = 'Website'
        output_item['source_acronym'] = None
        io.json_write(output_filepath, [output_item])
        # if output_item['business_website_html'] == 'true':
            # print(json.dumps(output_item, indent=4))
            # quit()
        ### CHECK SHAPE/DATA ERRORS
        for key, val in output_item.items():
            if val == '':
                print('################################################################################')
                print('''ERR: render > website > details > output_item data has invalid empty stings ''')
                print('################################################################################')
                quit()
        ###
        item = output_item
        print(output_filepath)
        none_count = 0
        empty_count = 0
        value_count = 0
        for key, val in item.items():
            if val == None: none_count += 1
            elif val == '': empty_count += 1
            else: value_count += 1
        total_count = none_count + empty_count + value_count
        print(f'NONE: {none_count}/{total_count} - {none_count/total_count*100}')
        print(f'EMPTY: {empty_count}/{total_count} - {empty_count/total_count*100}')
        print(f'VALUE: {value_count}/{total_count} - {value_count/total_count*100}')
        # quit()
        ###

def parse_website_herbs():
    input_folderpath = f'{HUB_FOLDERPATH}/fetch/gmap/america/places_json'
    output_folderpath = f'{HUB_FOLDERPATH}/parse/website/herbs/json'
    # try: shutil.rmtree(output_folderpath)
    # except: pass
    io.folders_recursive_gen(output_folderpath)
    ###
    input_filenames = sorted(os.listdir(input_folderpath))
    for i, input_filename in enumerate(input_filenames):
        print(f'{i}/{len(input_filenames)} - {input_filename}')
        ###
        input_filename_base = input_filename.split('.')[0].strip()
        input_filepath = f'{input_folderpath}/{input_filename}'
        input_data = io.json_read(input_filepath)
        gmap_label = input_data['gmap_label']
        gmap_website = input_data['gmap_website']
        gmap_name = input_data['gmap_name']
        gmap_slug = input_data['gmap_slug']
        ###
        output_filepath = f'{output_folderpath}/{gmap_slug}.json'
        try: output_data = io.json_read(output_filepath)
        except: output_data = []
        # print(json.dumps(output_data, indent=4))
        # quit()
        # if type(output_data) is list: output_data = output_data[0]
        fields_data = parse_organizations_herbs_data.fields
        website_filepath = f'{HUB_FOLDERPATH}/fetch/websites/america/places_html/{gmap_slug}.html'
        # print(website_filepath)
        # print(json.dumps(output_data, indent=4))
        # quit()
        ###
        ### PARSE GENERAL FIELDS
        '''
        output_item = {}
        for field_item in fields_data:
            reply = ''
            if field_item['field_name'] == 'business_name_raw': reply = gmap_name
            output_item[field_item['field_name']] = reply
        # print(json.dumps(output_item, indent=4))
        # quit()
        # continue
        '''
        # print(output_filepath)
        # print(json.dumps(output_data, indent=4))
        # quit()
        if output_data == []:
            output_items = []
            website_text = website_text_get(website_filepath)
            if website_text != '':
                llm_herbs_lst = llm_herbs_gen(website_text)
                if llm_herbs_lst != None:
                    for llm_herb in llm_herbs_lst:
                        output_item = {}
                        for field_item in fields_data:
                            reply = ''
                            if field_item['field_name'] == 'business_name_raw': reply = gmap_name
                            elif field_item['field_type'] == 'text': reply = llm_herb
                            ###
                            output_item[field_item['field_name']] = reply
                        output_item['source_name'] = 'Website'
                        output_item['source_acronym'] = None
                        output_items.append(output_item)
        else:
            output_items = output_data
        ###
        io.json_write(output_filepath, output_items)
        # print(json.dumps(output_items, indent=4))
        # quit()
        ###
        '''
        item = output_item
        print(output_filepath)
        none_count = 0
        empty_count = 0
        value_count = 0
        for key, val in item.items():
            if val == None: none_count += 1
            elif val == '': empty_count += 1
            else: value_count += 1
        total_count = none_count + empty_count + value_count
        print(f'NONE: {none_count}/{total_count} - {none_count/total_count*100}')
        print(f'EMPTY: {empty_count}/{total_count} - {empty_count/total_count*100}')
        print(f'VALUE: {value_count}/{total_count} - {value_count/total_count*100}')
        # quit()
        '''
        ###

def analyse_website():
    output_folderpath = f'{g.DATA_FOLDERPATH}/organizations/parse/website/json'
    # try: shutil.rmtree(output_folderpath)
    # except: pass
    io.folders_recursive_gen(output_folderpath)
    ###
    input_foldername = f'{g.DATA_FOLDERPATH}/organizations/fetch/gmap/america/places'.replace(' ', '_')
    input_filenames = sorted(os.listdir(input_foldername))
    for input_filename in input_filenames[:10]:
        input_filename_base = input_filename.split('.')[0].strip()
        input_filepath = f'{input_foldername}/{input_filename}'
        with open(input_filepath, encoding="utf-8") as f: rows = f.read().strip().split('\n')
        for row in rows:
            values = row.split('~')
            if values != [] and values != ['']:
                label = values[0]
                website = values[2]
                slug = to_slug(label)
                print(f'label: {label}')
                print(f'website: {website}')
                print(f'slug: {slug}')
                print(f'***************************************')
                print()
                ###
                output_filepath = f'{output_folderpath}/{slug}.json'
                data = io.json_read(output_filepath)
                item = data[0]
                none_count = 0
                empty_count = 0
                value_count = 0
                for key, val in item.items():
                    if val == None: none_count += 1
                    elif val == '': empty_count += 1
                    else: value_count += 1
                total_count = none_count + empty_count + value_count
                print(f'NONE: {none_count}/{total_count} - {none_count/total_count*100}')
                print(f'EMPTY: {empty_count}/{total_count} - {empty_count/total_count*100}')
                print(f'VALUE: {value_count}/{total_count} - {value_count/total_count*100}')
                quit()

def analyse_jsons():
    input_folderpath = f'{HUB_FOLDERPATH}/parse/website/json'
    input_filenames = sorted(os.listdir(input_folderpath))
    i = 0
    fields = []
    for input_filename in input_filenames[:]:
        i += 1
        input_filepath = f'{input_folderpath}/{input_filename}'
        data = io.json_read(input_filepath)[0]
        for key, val in data.items():
            found = False        
            for field in fields:
                if field['name'] == key:
                    none_count = 0
                    empty_count = 0
                    value_count = 0
                    if val == None: none_count += 1
                    elif val == '': empty_count += 1
                    else: value_count += 1
                    field['analytics']['none'] += none_count
                    field['analytics']['empty'] += empty_count
                    field['analytics']['value'] += value_count
                    ###
                    found = True        
                    break
            if not found:
                none_count = 0
                empty_count = 0
                value_count = 0
                if val == None: none_count += 1
                elif val == '': empty_count += 1
                else: value_count += 1
                item_new = {
                    'name': key,
                    'analytics': {
                        'none': none_count,
                        'empty': empty_count,
                        'value': value_count,
                    },
                }
                fields.append(item_new)
    # print(json.dumps(fields, indent=4))
    fields = sorted(fields, key=lambda x: x["analytics"]["value"], reverse=True)
    print(json.dumps(fields, indent=4))
    quit()

def analyse_field(field_name):
    input_folderpath = f'{g.DATA_FOLDERPATH}/organizations/parse/website/details/json'
    input_filenames = sorted(os.listdir(input_folderpath))
    none_count = 0
    empty_count = 0
    value_count = 0
    value_filepaths = []
    for input_filename in input_filenames[start:end]:
        input_filepath = f'{input_folderpath}/{input_filename}'
        data = io.json_read(input_filepath)
        item = data[0]
        try: val = item[field_name]
        except: continue
        if val == None: none_count += 1
        elif val == '': empty_count += 1
        else: 
            value_count += 1
            value_filepaths.append(input_filepath)
        # print(json.dumps(item, indent=4))
        # quit()
    total_count = none_count + empty_count + value_count
    print(f'FIELD_NAME: {field_name}')
    print(f'NONE: {none_count}/{total_count} - {none_count/total_count*100}')
    print(f'EMPTY: {empty_count}/{total_count} - {empty_count/total_count*100}')
    print(f'VALUE: {value_count}/{total_count} - {value_count/total_count*100}')
    for x in value_filepaths:
        print(x)
    quit()

def format_gmap_to_json():
    input_folderpath = f'{HUB_FOLDERPATH}/fetch/gmap/america/places'.replace(' ', '_')
    output_folderpath = f'{HUB_FOLDERPATH}/fetch/gmap/america/places_json'
    try: shutil.rmtree(output_folderpath)
    except: pass
    io.folders_recursive_gen(output_folderpath)
    ###
    input_filenames = sorted(os.listdir(input_folderpath))
    i = 0
    business_done = []
    business_count_total = 0
    business_count_duplicate = 0
    business_count_new = 0
    for input_filename in input_filenames[start:end]:
        print(f'{start+i}/{end}')
        print(f'{input_filename}')
        i += 1
        input_filename_base = input_filename.split('.')[0].strip()
        input_filepath = f'{input_folderpath}/{input_filename}'
        with open(input_filepath, encoding="utf-8") as f: rows = f.read().strip().split('\n')
        for row in rows:
            values = row.split('~')
            if values != [] and values != ['']:
                ### GET CSV ROW VALS
                gmap_label = values[0].strip()
                gmap_website = values[2].strip()
                gmap_name = values[4].strip()
                gmap_slug = to_slug(gmap_label).strip()
                ### EXTRACT BASE URL
                gmap_website = base_url(gmap_website).strip()
                if gmap_website == '': gmap_website = None
                if gmap_slug == '': continue
                business_count_total += 1
                if gmap_slug in business_done:
                    business_count_duplicate += 1
                    continue
                else:
                    business_count_new += 1
                business_done.append(gmap_slug)
                ###
                output_data = {
                    'gmap_label': gmap_label,
                    'gmap_website': gmap_website,
                    'gmap_name': gmap_name,
                    'gmap_slug': gmap_slug,
                }
                output_filepath = f'{output_folderpath}/{gmap_slug}.json'
                print(output_filepath)
                io.json_write(output_filepath, output_data)
    print(f'''NEW: {business_count_new}''')
    print(f'''DUPLICATE: {business_count_duplicate}''')
    print(f'''TOTAL: {business_count_total}''')

def format_websites_to_html():
    input_folderpath = f'{HUB_FOLDERPATH}/fetch/websites/america/places'.replace(' ', '_')
    output_folderpath = f'{HUB_FOLDERPATH}/fetch/websites/america/places_html'
    try: shutil.rmtree(output_folderpath)
    except: pass
    io.folders_recursive_gen(output_folderpath)
    ###
    input_foldernames = sorted(os.listdir(input_folderpath))
    i = 0
    business_done = []
    business_count_total = 0
    business_count_duplicate = 0
    business_count_new = 0
    for input_foldername in input_foldernames[start:end]:
        print(f'{start+i}/{end}')
        input_filenames = sorted(os.listdir(f'''{input_folderpath}/{input_foldername}'''))
        for input_filename in input_filenames[start:end]:
            input_filepath = f'{input_folderpath}/{input_foldername}/{input_filename}'
            shutil.copy2(input_filepath, f'''{output_folderpath}/{input_filename}''')

def run():
    print(f'ORGANIZATION >> PARSE >> main')

    format_gmap_to_json()
    format_websites_to_html()
    # quit()

    start = time.perf_counter()
    # parse_gmap()
    print(f'''
################################################################################
parse gmap()
################################################################################
    ''')

    start = time.perf_counter()
    # parse_website()
    print(f'''
################################################################################
parse website()
################################################################################
    ''')
    parse_website_herbs()
    print(f'''
################################################################################
parse website_herbs()
################################################################################
    ''')

    """
    print(f'''
################################################################################
parse gmap() - execution time: 
---
SECONDS: {(time.perf_counter() - start)}
MINUTES: {(time.perf_counter() - start)/60}
HOURS:   {(time.perf_counter() - start)/60/60}
################################################################################
    ''')
    """
    # analyse_website()
    # analyse_jsons()
    # analyse_field(field_name='business_founder_name')
    # quit()

