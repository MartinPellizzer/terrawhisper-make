import os
import time
import random
import csv
from datetime import datetime
import re
from bs4 import BeautifulSoup

from PIL import Image, ImageFont, ImageDraw, ImageColor, ImageOps

from lib import g
import data_csv
import util
import util_data
from lib import io
from lib import utils
from lib import data

from oliark_io import json_write, json_read
from oliark_io import csv_read_rows_to_json
from oliark import img_resize

pipe = None

vault = '/home/ubuntu/vault'
vault_tmp = '/home/ubuntu/vault-tmp'
checkpoint_filepath = f'{g.VAULT}/stable-diffusion/checkpoints/xl/juggernautXL_juggXIByRundiffusion.safetensors'
proj_filepath_abs = '/home/ubuntu/proj/tw/terrawhisper-compiler'

random_num = random.randint(-2, 2)
# random_num = 0
ARTICLES_NUM = 50 - random_num

preparations_rows = util.csv_get_rows(g.CSV_PREPARATIONS_FILEPATH)
preparations_cols = util.csv_get_cols(preparations_rows)
preparations_rows = preparations_rows[1:]

status_rows, status_cols = data_csv.status()
systems_rows = util.csv_get_rows(g.CSV_SYSTEMS_NEW_FILEPATH)
systems_cols = util.csv_get_cols(systems_rows)
systems_rows = systems_rows[1:]

status_systems_rows = util.csv_get_rows(g.CSV_STATUS_SYSTEMS_FILEPATH)
status_systems_cols = util.csv_get_cols(status_systems_rows)
status_systems_rows = status_systems_rows[1:]

herbs_rows, herbs_cols = data_csv.herbs()
herbs_names_scientific = [herb[herbs_cols['herb_name_scientific']] for herb in herbs_rows]

def get_system_by_status(status_id):
    system_row = []
    status_systems_rows_filtered = util.csv_get_rows_filtered(
        g.CSV_STATUS_SYSTEMS_FILEPATH, status_systems_cols['status_id'], status_id,
    )
    if status_systems_rows_filtered != []:
        status_system_row = status_systems_rows_filtered[0]
        system_id = status_system_row[status_systems_cols['system_id']]
        systems_rows_filtered = util.csv_get_rows_filtered(
            g.CSV_SYSTEMS_NEW_FILEPATH, systems_cols['system_id'], system_id,
        )
        if systems_rows_filtered != []:
            system_row = systems_rows_filtered[0]
    return system_row

def get_preparations_by_status(status_id):
    util_data.j_status_preparations_rows_filtered = util.csv_get_rows_filtered(
        g.CSV_STATUS_PREPARATIONS_FILEPATH, util_data.j_status_preparations_cols['status_id'], status_id,
    )
    status_preparations_ids = [
        row[util_data.j_status_preparations_cols['preparation_id']] 
        for row in util_data.j_status_preparations_rows_filtered
        if row[util_data.j_status_preparations_cols['status_id']] == status_id
    ]
    preparations_rows_filtered = []
    for preparation_row in preparations_rows:
        herb_id = preparation_row[preparations_cols['preparation_id']]
        if herb_id in status_preparations_ids:
            preparations_rows_filtered.append(preparation_row)
    return preparations_rows_filtered

teas_articles_filepath = []
tinctures_articles_filepath = []
essential_oils_articles_filepath = []
creams_articles_filepath = []
for status_row in status_rows:
    status_exe = status_row[status_cols['status_exe']]
    status_id = status_row[status_cols['status_id']]
    status_slug = status_row[status_cols['status_slug']]
    status_name = status_row[status_cols['status_names']].split(',')[0].strip()
    if status_exe == '': continue
    if status_id == '': continue
    if status_slug == '': continue
    if status_name == '': continue
    print(f'>> {status_id} - {status_name}')
    system_row = get_system_by_status(status_id)
    system_id = system_row[systems_cols['system_id']]
    system_slug = system_row[systems_cols['system_slug']]
    system_name = system_row[systems_cols['system_name']]
    if system_id == '': continue
    if system_slug == '': continue
    if system_name == '': continue
    print(f'    {system_id} - {system_name}')
    preparations = get_preparations_by_status(status_id)[:10]
    preparations_names = [row[preparations_cols['preparation_name']] for row in preparations]
    print(preparations_names)
    json_filepath = f'database/json/remedies/{system_slug}/{status_slug}/teas.json'
    json_filepath = f'database/json/ailments/{status_slug}/teas.json'
    if 'teas' in preparations_names:
        if os.path.exists(json_filepath): 
            print(f'ok: {json_filepath}')
            teas_articles_filepath.append(json_filepath)
        else: print(f'NOT FOUND: {json_filepath}')
    else: print(f'NOT PREPARATION OF STATUS: {json_filepath}')
    json_filepath = f'database/json/remedies/{system_slug}/{status_slug}/tinctures.json'
    json_filepath = f'database/json/ailments/{status_slug}/tinctures.json'
    if 'tinctures' in preparations_names:
        if os.path.exists(json_filepath): 
            print(f'ok: {json_filepath}')
            tinctures_articles_filepath.append(json_filepath)
        else: print(f'NOT FOUND: {json_filepath}')
    else: print(f'NOT PREPARATION OF STATUS: {json_filepath}')
    json_filepath = f'database/json/remedies/{system_slug}/{status_slug}/essential-oils.json'
    json_filepath = f'database/json/ailments/{status_slug}/essential-oils.json'
    if 'essential oils' in preparations_names:
        if os.path.exists(json_filepath): 
            print(f'ok: {json_filepath}')
            essential_oils_articles_filepath.append(json_filepath)
        else: print(f'NOT FOUND: {json_filepath}')
    else: print(f'NOT PREPARATION OF STATUS: {json_filepath}')
    json_filepath = f'database/json/remedies/{system_slug}/{status_slug}/creams.json'
    json_filepath = f'database/json/ailments/{status_slug}/creams.json'
    if 'creams' in preparations_names:
        if os.path.exists(json_filepath): 
            print(f'ok: {json_filepath}')
            creams_articles_filepath.append(json_filepath)
        else: print(f'NOT FOUND: {json_filepath}')
    else: print(f'NOT PREPARATION OF STATUS: {json_filepath}')


'''
equipments = csv_read_rows_to_json('database/csv/equipments.csv', debug=False)
equipments_articles_filepath = []
for equipment_i, equipment in enumerate(equipments):
    equipment_id = equipment['equipment_id']
    equipment_slug = equipment['equipment_slug']
    equipment_name = equipment['equipment_name']
    print(equipment_id, equipment_slug, equipment_name)
    json_filepath = f'equipments/jsons/{equipment_slug}.json'
    if os.path.exists(json_filepath): 
        print(f'ok: {json_filepath}')
        equipments_articles_filepath.append(json_filepath)
    else: print(f'NOT FOUND: {json_filepath}')
'''

herbs_articles_filepath = []
herbs = data.herbs_books_get()
json_herbs_folderpath = f'database/json/herbs'
for json_herb_filename in os.listdir(json_herbs_folderpath):
    json_herb_filepath = f'{json_herbs_folderpath}/{json_herb_filename}'
    if os.path.isdir(json_herb_filepath):
        json_herb_folderpath = json_herb_filepath
        json_herb_benefits_filepath = f'{json_herb_folderpath}/benefits.json'
        if os.path.exists(json_herb_benefits_filepath): 
            herbs_articles_filepath.append(json_herb_benefits_filepath)

preparations_best_articles_filepath = []
preparation_list = io.csv_to_dict(f'database/entities/preparations.csv')
json_preparations_folderpath = f'database/json/preparations'
for json_preparation_filename in os.listdir(json_preparations_folderpath):
    json_preparation_filepath = f'{json_preparations_folderpath}/{json_preparation_filename}'
    if os.path.isdir(json_preparation_filepath):
        json_preparation_folderpath = json_preparation_filepath
        json_preparation_best_filepath = f'{json_preparation_folderpath}/best.json'
        if os.path.exists(json_preparation_best_filepath): 
            print(json_preparation_best_filepath)
            preparations_best_articles_filepath.append(json_preparation_best_filepath)

if 0:
    for herb_i, herb in enumerate(herbs):
        herb_name_scientific = herb.strip().lower()
        herb_slug = utils.sluggify(herb_name_scientific)
        url_relative = f'herbs/{herb_slug}'
        json_article_filepath = f'{g.ENTITIES_FOLDERPATH}/{url_relative}.json'
        print(f'    >> JSON: {json_article_filepath}')
        if data.herb_medicine_poison_get(url_relative) == 'medicine':
            if os.path.exists(json_filepath): 
                print(f'ok: {json_filepath}')
                herbs_articles_filepath.append(json_article_filepath)
            else: print(f'NOT FOUND: {json_filepath}')

random.shuffle(herbs_articles_filepath)
random.shuffle(teas_articles_filepath)
random.shuffle(tinctures_articles_filepath)
random.shuffle(essential_oils_articles_filepath)
random.shuffle(creams_articles_filepath)
random.shuffle(preparations_best_articles_filepath)

teas_articles_filepath_tmp = []
tinctures_articles_filepath_tmp = []
essential_oils_articles_filepath_tmp = []
creams_articles_filepath_tmp = []

equipments_articles_filepath_tmp = []
herbs_articles_filepath_tmp = []
preparations_best_articles_filepath_tmp = []

articles_filepath = []
for i in range(999):
    if 1:
        try: herbs_articles_filepath_tmp.append(herbs_articles_filepath[i])
        except: pass
        if len(teas_articles_filepath_tmp) + \
            len(tinctures_articles_filepath_tmp) + \
            len(essential_oils_articles_filepath_tmp) + \
            len(creams_articles_filepath_tmp) + \
            len(equipments_articles_filepath_tmp) + \
            len(herbs_articles_filepath_tmp) + \
            len(preparations_best_articles_filepath_tmp) + \
            len([]) \
            >= ARTICLES_NUM:
            break
    if 1:
        try: preparations_best_articles_filepath_tmp.append(preparations_best_articles_filepath[i])
        except: pass
        if len(teas_articles_filepath_tmp) + \
            len(tinctures_articles_filepath_tmp) + \
            len(essential_oils_articles_filepath_tmp) + \
            len(creams_articles_filepath_tmp) + \
            len(equipments_articles_filepath_tmp) + \
            len(herbs_articles_filepath_tmp) + \
            len(preparations_best_articles_filepath_tmp) + \
            len([]) \
            >= ARTICLES_NUM:
            break
    if 0:
        try: equipments_articles_filepath_tmp.append(equipments_articles_filepath[i])
        except: pass
        if len(teas_articles_filepath_tmp) + \
            len(tinctures_articles_filepath_tmp) + \
            len(essential_oils_articles_filepath_tmp) + \
            len(creams_articles_filepath_tmp) + \
            len(equipments_articles_filepath_tmp) + \
            len(herbs_articles_filepath_tmp) + \
            len(preparations_best_articles_filepath_tmp) + \
            len([]) \
            >= ARTICLES_NUM:
            break
    try: teas_articles_filepath_tmp.append(teas_articles_filepath[i])
    except: pass
    if len(teas_articles_filepath_tmp) + \
        len(tinctures_articles_filepath_tmp) + \
        len(essential_oils_articles_filepath_tmp) + \
        len(creams_articles_filepath_tmp) + \
        len(equipments_articles_filepath_tmp) + \
        len(herbs_articles_filepath_tmp) + \
        len(preparations_best_articles_filepath_tmp) + \
        len([]) \
        >= ARTICLES_NUM:
        break
    try: tinctures_articles_filepath_tmp.append(tinctures_articles_filepath[i])
    except: pass
    if len(teas_articles_filepath_tmp) + \
        len(tinctures_articles_filepath_tmp) + \
        len(essential_oils_articles_filepath_tmp) + \
        len(creams_articles_filepath_tmp) + \
        len(equipments_articles_filepath_tmp) + \
        len(herbs_articles_filepath_tmp) + \
        len(preparations_best_articles_filepath_tmp) + \
        len([]) \
        >= ARTICLES_NUM:
        break
    try: essential_oils_articles_filepath_tmp.append(essential_oils_articles_filepath[i])
    except: pass
    if len(teas_articles_filepath_tmp) + \
        len(tinctures_articles_filepath_tmp) + \
        len(essential_oils_articles_filepath_tmp) + \
        len(creams_articles_filepath_tmp) + \
        len(equipments_articles_filepath_tmp) + \
        len(herbs_articles_filepath_tmp) + \
        len(preparations_best_articles_filepath_tmp) + \
        len([]) \
        >= ARTICLES_NUM:
        break
    try: creams_articles_filepath_tmp.append(creams_articles_filepath[i])
    except: pass
    if len(teas_articles_filepath_tmp) + \
        len(tinctures_articles_filepath_tmp) + \
        len(essential_oils_articles_filepath_tmp) + \
        len(creams_articles_filepath_tmp) + \
        len(equipments_articles_filepath_tmp) + \
        len(herbs_articles_filepath_tmp) + \
        len(preparations_best_articles_filepath_tmp) + \
        len([]) \
        >= ARTICLES_NUM:
        break

# equipments_articles_filepath = equipments_articles_filepath_tmp
herbs_articles_filepath = herbs_articles_filepath_tmp
preparations_best_articles_filepath = preparations_best_articles_filepath_tmp
teas_articles_filepath = teas_articles_filepath_tmp
tinctures_articles_filepath = tinctures_articles_filepath_tmp
essential_oils_articles_filepath = essential_oils_articles_filepath_tmp
creams_articles_filepath = creams_articles_filepath_tmp

# for filepath in equipments_articles_filepath: articles_filepath.append(filepath)
for filepath in herbs_articles_filepath: articles_filepath.append(filepath)
for filepath in preparations_best_articles_filepath: articles_filepath.append(filepath)
for filepath in teas_articles_filepath: articles_filepath.append(filepath)
for filepath in tinctures_articles_filepath: articles_filepath.append(filepath)
for filepath in essential_oils_articles_filepath: articles_filepath.append(filepath)
for filepath in creams_articles_filepath: articles_filepath.append(filepath)

for filepath in articles_filepath:
    print(filepath)

print(ARTICLES_NUM)
# print(len(equipments))
print(len(teas_articles_filepath))
print(len(tinctures_articles_filepath))
print(len(essential_oils_articles_filepath))
print(len(creams_articles_filepath))

print(len(herbs_articles_filepath))
print(len(preparations_best_articles_filepath))
###########################################################################
# UTILS
###########################################################################

def pin_save(img, filename):
    img_filepath = f'pinterest/images/{filename}.jpg'
    img.save(
        img_filepath,
        format='JPEG',
        subsampling=0,
        quality=100,
    )
    return img_filepath

###########################################################################
# BLOCKS
###########################################################################

def gen_text_num(img, line_list, num):
    if num == 0: return img
    text_pos_x = 200
    num = str(num)
    img_w, img_h = 1000, 1500
    draw.rectangle(((0, img_h//2 - 160), (img_w, img_h//2 + 160)), fill='#000000')
    circle_size = 300
    x = img_w//2-circle_size//2
    font_size = 240
    font_family, font_weight = 'Lato', 'Bold'
    font_path = f"assets/fonts/{font_family}/{font_family}-{font_weight}.ttf"
    font = ImageFont.truetype(font_path, font_size)
    text = num
    text_w = font.getbbox(text)[2]
    text_h = font.getbbox(text)[3]
    draw.text((img_w//2 - text_w//2, img_h//2 - 320), text, '#ffffff', font=font)
    text_pos_x = 50 + text_w
    font_size = 48
    font_family, font_weight = 'Lato', 'Regular'
    font_path = f"assets/fonts/{font_family}/{font_family}-{font_weight}.ttf"
    font = ImageFont.truetype(font_path, font_size)
    text = line_list[0]
    text_w = font.getbbox(text)[2]
    text_h = font.getbbox(text)[3]
    draw.text((img_w//2 - text_w//2, img_h//2 - 50), text, '#ffffff', font=font)
    font_size = 96
    font_family, font_weight = 'Lato', 'Bold'
    font_path = f"assets/fonts/{font_family}/{font_family}-{font_weight}.ttf"
    font = ImageFont.truetype(font_path, font_size)
    text = line_list[1]
    text_w = font.getbbox(text)[2]
    text_h = font.getbbox(text)[3]
    draw.text((img_w//2 - text_w//2, img_h//2), text, '#ffffff', font=font)
    return img
    
###########################################################################
# TEMPLATES
###########################################################################

###########################################################################
# ;products
###########################################################################

# ;cards
def product_card_gen(pin_i):
    pin_w = 1000
    pin_h = 1500
    img = Image.new(mode="RGBA", size=(pin_w, pin_h), color='#ece0c4')
    draw = ImageDraw.Draw(img)
    x_off = 50
    y_off = 50
    col_n = 5
    row_n = 10
    gap = 20
    pin_w_adj = 900 - gap*(col_n-1)
    pin_h_adj = 1500 - gap*(row_n-1)
    # cards
    card_folderpath = 'assets/digital-products/cards/plants-new/cards-images'
    card_filepaths = [f'{card_folderpath}/{filename}' for filename in os.listdir(card_folderpath)]
    random.shuffle(card_filepaths)
    card_n = 23
    card_w = 900
    card_h = 1500
    card_i = 0
    no_more_cards = False
    for row_i in range(row_n):
        if no_more_cards: break
        for col_i in range(col_n):
            if no_more_cards: break
            card_img = Image.open(card_filepaths[card_i])
            card_w_resized = pin_w_adj//col_n
            card_h_resized = pin_h_adj//col_n
            card_img = util.img_resize(card_img, card_w_resized, card_h_resized)
            img.paste(card_img, (x_off+card_w_resized*col_i + gap*col_i, y_off+card_h_resized*row_i + gap*row_i))
            card_i += 1
            if card_i >= card_n: no_more_cards = True
    # label center
    label_img_w = 900
    label_img_h = 900
    label_img = Image.open('pinterest/components/label-0000.png')
    label_img.thumbnail((label_img_w, label_img_h), Image.LANCZOS)
    img.paste(label_img, (pin_w//2-label_img_w//2, pin_h//2-label_img_h//2), label_img)
    # rects top/bottom
    rect_h = 30
    draw.rectangle(((0, 0), (pin_w, rect_h)), fill='#262524')
    draw.rectangle(((0, pin_h-rect_h), (pin_w, pin_h)), fill='#262524')
    x1 = x_off+card_w_resized*3+gap*3
    y1 = y_off+card_h_resized*4+gap*4
    draw.rectangle(((x1, y1), (x1+pin_w, y1+pin_h)), fill='#262524')
    # copyright
    text = 'Terra Whisper'
    font_size = 48
    font_path = f"assets/fonts/allura/Allura-Regular.ttf"
    font = ImageFont.truetype(font_path, font_size)
    draw.text((675, 1325), text, '#ece0c4', font=font)
    # save img
    img = img.convert('RGB')
    img_filepath = f'pinterest/images/botanical-name-cards.jpg'
    img.save(img_filepath, format='JPEG', subsampling=0, quality=100)
    # img.show()
    # save json
    json_data = {
        'img_filepath': img_filepath,
        'title': 'Botanical Name Card Medicinal Herb Study Flashcard Plant Name Latin Identification Learning Tool',
        'description': '''This is a digital download. Beautifully designed printable deck of 40 botanical flashcards. Each 3x5" card features one medicinal plant, including its scientific name, plant family, and common names. Perfect for students, herbalists, and nature lovers alike. Styled with Victorian elegance and rustic charm, this digital deck blends old-world aesthetics with modern learning. Whether you're building your herbal knowledge or just love vintage botanical art, these cards are a practical study tool.''',
        'url': 'https://www.etsy.com/listing/1905803593/40-botanical-name-card-medicinal-herb',
        'board_name': 'Herb Digital Products',
    }
    io.json_write(f'{g.PINTEREST_PINS_IMAGE_FOLDERPATH}/{pin_i}.json', json_data)

def card_template_2(pin_i):
    c_yellow = '#ece0c4'
    c_dark = '#262524'
    pin_w = 1000
    pin_h = 1500
    img = Image.new(mode="RGB", size=(pin_w, pin_h), color=c_yellow)
    draw = ImageDraw.Draw(img)
    gap = 8
    rect_h = 440

    card_folderpath = 'assets/shop/cards/plants/final'
    images_filepaths = [f'{card_folderpath}/{filename}' for filename in os.listdir(card_folderpath)]
    random.shuffle(images_filepaths)

    img_w = 900
    img_h = 1500
    img_0000 = Image.open(images_filepaths[0])
    img_0001 = Image.open(images_filepaths[1])
    img_0002 = Image.open(images_filepaths[2])
    img_0003 = Image.open(images_filepaths[3])
    img_0004 = Image.open(images_filepaths[4])
    img_0005 = Image.open(images_filepaths[5])
    # img_0000 = util.img_resize(img_0000, int(img_w*0.33), int(img_h*0.33))
    # img_0001 = util.img_resize(img_0001, int(pin_w*0.33), int(pin_h*0.33))
    # img_0002 = util.img_resize(img_0002, int(pin_w*0.33), int(pin_h*0.33))
    # img_0003 = util.img_resize(img_0003, int(pin_w*0.33), int(pin_h*0.33))
    # img_0004 = util.img_resize(img_0004, int(pin_w*0.33), int(pin_h*0.33))
    # img_0005 = util.img_resize(img_0005, int(pin_w*0.33), int(pin_h*0.33))
    x_off = 17
    img_w_factor = 1.02
    img_h_factor = 1.02
    img_0000.thumbnail((300*img_w_factor, 500*img_h_factor), Image.Resampling.LANCZOS)
    img_0001.thumbnail((300*img_w_factor, 500*img_h_factor), Image.Resampling.LANCZOS)
    img_0002.thumbnail((300*img_w_factor, 500*img_h_factor), Image.Resampling.LANCZOS)
    img_0003.thumbnail((300*img_w_factor, 500*img_h_factor), Image.Resampling.LANCZOS)
    img_0004.thumbnail((300*img_w_factor, 500*img_h_factor), Image.Resampling.LANCZOS)
    img_0005.thumbnail((300*img_w_factor, 500*img_h_factor), Image.Resampling.LANCZOS)
    img.paste(img_0000, (x_off + 0, 0))
    img.paste(img_0001, (x_off + int(pin_w*0.33), 0))
    img.paste(img_0002, (x_off + int(pin_w*0.66), 0))
    img.paste(img_0003, (x_off + 0, int(pin_h*0.66)))
    img.paste(img_0004, (x_off + int(pin_w*0.33), int(pin_h*0.66)))
    img.paste(img_0005, (x_off + int(pin_w*0.66), int(pin_h*0.66)))
    random_theme = random.randint(0, 1)
    random_theme = 0
    if random_theme == 0:
        text_color = c_yellow
        bg_color = c_dark
    else:
        text_color = c_dark
        bg_color = c_yellow
    # rect
    draw.rectangle(((0, pin_h//2 - rect_h//2), (pin_w, pin_h//2 + rect_h//2)), fill=bg_color)

    # numer
    text = '545'
    font_size = 256
    font_path = f"assets/fonts/crimson-pro/static/CrimsonPro-Regular.ttf"
    # font_path = f"assets/fonts/rye/Rye-Regular.ttf"
    # font_path = f"assets/fonts/lora/static/Lora-Regular.ttf"
    font = ImageFont.truetype(font_path, font_size)
    _, _, text_w, text_h = font.getbbox(text)
    draw.text((pin_w//2 - text_w//2, pin_h//2 - text_h//2 - 150 + 20), text, '#ece0c4', font=font)

    y_off = 50
    # line 1
    text = 'Healing Herb'.upper()
    font_size = 72
    font_path = f"assets/fonts/crimson-pro/static/CrimsonPro-Regular.ttf"
    font_path = f"assets/fonts/lora/static/Lora-Regular.ttf"
    font = ImageFont.truetype(font_path, font_size)
    _, _, text_w, text_h = font.getbbox(text)
    draw.text((pin_w//2 - text_w//2, pin_h//2 - text_h//2 + y_off), text, '#ece0c4', font=font)

    # line 2
    text = 'Botanical Name Cards'.upper()
    font_size = 72
    font_path = f"assets/fonts/crimson-pro/static/CrimsonPro-Regular.ttf"
    font_path = f"assets/fonts/lora/static/Lora-Regular.ttf"
    font = ImageFont.truetype(font_path, font_size)
    _, _, text_w, text_h = font.getbbox(text)
    draw.text((pin_w//2 - text_w//2, pin_h//2 - text_h//2 + 80 + y_off), text, '#ece0c4', font=font)

    # circle
    '''
    circle_size = 300
    x1 = pin_w//2 - circle_size//2
    y1 = pin_h//2 - 160 - circle_size//2
    x2 = pin_w//2 + circle_size//2
    y2 = pin_h//2 - 160 + circle_size//2
    draw.ellipse((x1, y1, x2, y2), fill=bg_color)
    '''
    # draw.rectangle(((0, pin_h//2 - rect_h//2), (pin_w, pin_h//2 + rect_h//2)), fill=bg_color)
    
    '''
    ## text split
    try: status_name = data['ailment_name']
    except: pass
    try: status_name = data['status_name']
    except: pass
    text = f'{status_name}'.upper()
    #text = 'Breastfeeding pain'.upper()
    #text = 'Breastfeeding'.upper()
    font_size = 96
    font_family, font_weight = 'Lato', 'Bold'
    font_path = f"assets/fonts/{font_family}/{font_family}-{font_weight}.ttf"
    font = ImageFont.truetype(font_path, font_size)
    _, _, text_w, text_h = font.getbbox(text)
    if text_w > pin_w - 80:
        font_size = 80
        font = ImageFont.truetype(font_path, font_size)
        words = text.split(' ')
        words_per_line = len(words)//2
        line_1 = ' '.join(words[:words_per_line])
        line_2 = ' '.join(words[words_per_line:])
        _, _, text_w, text_h = font.getbbox(line_1)
        draw.text((pin_w//2 - text_w//2, pin_h//2 - text_h//2), line_1, text_color, font=font)
        _, _, text_w, text_h = font.getbbox(line_2)
        draw.text((pin_w//2 - text_w//2, pin_h//2 - text_h//2 + text_h), line_2, text_color, font=font)
        remedies_num = data['main_lst_num']
        preparation_name = data['preparation_name']
        text = f'best herbal {preparation_name} for'.title()
        font_size = 48
        font_family, font_weight = 'Lato', 'Regular'
        font_path = f"assets/fonts/{font_family}/{font_family}-{font_weight}.ttf"
        font = ImageFont.truetype(font_path, font_size)
        _, _, text_w, text_h = font.getbbox(text)
        draw.text((pin_w//2 - text_w//2, pin_h//2 - text_h//2 - text_h*1.5), text, text_color, font=font)
        text = str(data['main_lst_num'])
        font_size = 160
        font_family, font_weight = 'Lato', 'Regular'
        font_path = f"assets/fonts/{font_family}/{font_family}-{font_weight}.ttf"
        font = ImageFont.truetype(font_path, font_size)
        _, _, text_w, text_h = font.getbbox(text)
        x1 = pin_w//2 - text_w//2
        y1 = pin_h//2 - text_h//2 - 210
        draw.text((x1, y1), text, text_color, font=font)
    else:
        draw.text((pin_w//2 - text_w//2, pin_h//2 - text_h//2 + 16), text, text_color, font=font)
        remedies_num = data['main_lst_num']
        preparation_name = data['preparation_name']
        text = f'best herbal {preparation_name} for'.title()
        font_size = 48
        font_family, font_weight = 'Lato', 'Regular'
        font_path = f"assets/fonts/{font_family}/{font_family}-{font_weight}.ttf"
        font = ImageFont.truetype(font_path, font_size)
        _, _, text_w, text_h = font.getbbox(text)
        draw.text((pin_w//2 - text_w//2, pin_h//2 - text_h//2 - text_h*1.2), text, text_color, font=font)
        text = '10'
        font_size = 160
        font_family, font_weight = 'Lato', 'Regular'
        font_path = f"assets/fonts/{font_family}/{font_family}-{font_weight}.ttf"
        font = ImageFont.truetype(font_path, font_size)
        _, _, text_w, text_h = font.getbbox(text)
        x1 = pin_w//2 - text_w//2
        y1 = pin_h//2 - text_h//2 - 210
        draw.text((x1, y1), text, text_color, font=font)
    '''
    # save img
    img = img.convert('RGB')
    img_filepath = f'pinterest/images/botanical-name-cards.jpg'
    img.save(img_filepath, format='JPEG', subsampling=0, quality=100)
    # save json
    json_data = {
        'img_filepath': img_filepath,
        'title': 'Botanical Name Card Medicinal Herb Study Flashcard Plant Name Latin Identification Learning Tool',
        'description': '''This is a digital download. Beautifully designed printable deck of 40 botanical flashcards. Each 3x5" card features one medicinal plant, including its scientific name, plant family, and common names. Perfect for students, herbalists, and nature lovers alike. Styled with Victorian elegance and rustic charm, this digital deck blends old-world aesthetics with modern learning. Whether you're building your herbal knowledge or just love vintage botanical art, these cards are a practical study tool.''',
        'url': 'https://www.etsy.com/listing/1905803593/545-printable-herb-card-set-botanical',
        'board_name': 'Herb Digital Products',
    }
    io.json_write(f'{g.PINTEREST_PINS_IMAGE_FOLDERPATH}/{pin_i}.json', json_data)

def shop_herb_drying_checklist(pin_i):
    c_light_1 = '#f8f7f2'
    c_light_2 = '#dedacf'
    c_dark_1 = '#141410'
    c_dark_2 = '#616140'
    images_filepaths = []
    width = 1216
    height = 832
    for i in range(2):
        herb_name_scientific = random.choice(herbs_names_scientific).strip()
        prompt = f'''
            close-up of dry {herb_name_scientific} herb,
            on a wooden table, 
            surrounded by medicinal dry herbs,
            indoor, 
            natural light,
            earth tones,
            neutral colors,
            soft focus,
            warm tones,
            vintage,
            high resolution,
            cinematic
        '''.replace('  ', ' ')
        image = image_ai(prompt, width, height)
        image_filepath = f'pinterest/tmp/img-{i}.jpg'
        image.save(image_filepath)
        images_filepaths.append(image_filepath)
    ###
    c_yellow = '#ece0c4'
    c_dark = '#262524'
    pin_w = 1000
    pin_h = 1500
    img = Image.new(mode="RGB", size=(pin_w, pin_h), color=c_yellow)
    draw = ImageDraw.Draw(img)
    ###
    gap = 8
    rect_h = 320
    img_0000 = Image.open(images_filepaths[0])
    img_0001 = Image.open(images_filepaths[1])
    img_0000 = util.img_resize(img_0000, int(pin_w*1), int(pin_h*0.5))
    img_0001 = util.img_resize(img_0001, int(pin_w*1), int(pin_h*0.5))
    img.paste(img_0000, (0, 0))
    img.paste(img_0001, (0, int(pin_h*0.5) + gap))
    random_theme = random.randint(0, 1)
    if random_theme == 0:
        text_color = c_light_1
        bg_color = c_dark_1
    else:
        text_color = c_dark_1
        bg_color = c_light_1
    draw.rectangle(((0, pin_h//2 - rect_h//2), (pin_w, pin_h//2 + rect_h//2)), fill=bg_color)
    try: status_name = data['ailment_name']
    except: pass
    try: status_name = data['status_name']
    except: pass
    text_y_off = 0.6
    text = f'herb drying'.upper()
    font_size = 128
    font_family, font_weight = 'Lato', 'Bold'
    font_path = f"assets/fonts/{font_family}/{font_family}-{font_weight}.ttf"
    font = ImageFont.truetype(font_path, font_size)
    _, _, text_w, text_h = font.getbbox(text)
    draw.text((pin_w//2 - text_w//2, pin_h//2 - text_h//2 - int(font_size*text_y_off)), text, text_color, font=font)
    text = f'checklist'.upper()
    font_family, font_weight = 'Lato', 'Bold'
    font_path = f"assets/fonts/{font_family}/{font_family}-{font_weight}.ttf"
    font = ImageFont.truetype(font_path, font_size)
    _, _, text_w, text_h = font.getbbox(text)
    draw.text((pin_w//2 - text_w//2, pin_h//2 - text_h//2 + font_size - int(font_size*text_y_off)), text, text_color, font=font)
    ###
    # image_logo_size = 128
    # image_logo = Image.open('assets/logo/terrawhisper-logo-round.png')
    # image_logo = util.img_resize(image_logo, image_logo_size, image_logo_size)
    # img.paste(image_logo, (pin_w//2 - image_logo_size//2, pin_h - image_logo_size - 80), image_logo)
    ###
    text = f'terrawhisper.com'.upper()
    font_size = 24
    font_family, font_weight = 'Lato', 'Bold'
    font_path = f"assets/fonts/{font_family}/{font_family}-{font_weight}.ttf"
    font = ImageFont.truetype(font_path, font_size)
    _, _, text_w, text_h = font.getbbox(text)
    draw.text((pin_w//2 - text_w//2, pin_h - text_h - 80), text, '#ffffff', font=font)
    ###
    img_filepath = pin_save(img, 'herb-drying-checklist')
    ###
    img = img.convert('RGB')
    img_filepath = f'pinterest/images/herb-drying-checklist.jpg'
    img.save(img_filepath, format='JPEG', subsampling=0, quality=100)
    description = f'''Ready to dry your garden herbs the right way? Download the Ultimate Herb Drying Checklist — a free, easy-to-use digital guide covering everything from harvesting tips to storage methods. Perfect for beginners and seasoned growers alike, this checklist helps you preserve flavor and potency with confidence. Get organized and make the most of your herbal harvest today.'''
    json_data = {
        'img_filepath': img_filepath,
        'title': 'The Ultimate Herb Drying Checklist',
        'description': description,
        'url': 'https://terrawhisper.com/shop/herb-drying-checklist.html',
        'board_name': 'Herbalism Guides',
    }
    io.json_write(f'{g.PINTEREST_PINS_IMAGE_FOLDERPATH}/{pin_i}.json', json_data)

def shop_labels(pin_i):
    herb_list = [
        {'herb_name_scientific': 'Matriarca chamomilla', 'herb_name_common': 'Chamomile'},
        {'herb_name_scientific': 'Mentha x piperita', 'herb_name_common': 'Peppermint'},
        {'herb_name_scientific': 'Lavandula angustifolia', 'herb_name_common': 'Lavender'},
        {'herb_name_scientific': 'Echinacea purpurea', 'herb_name_common': 'Echinacea'},
        {'herb_name_scientific': 'Zingiber officinale', 'herb_name_common': 'Ginger'},
        {'herb_name_scientific': 'Allium sativum', 'herb_name_common': 'Garlic'},
        {'herb_name_scientific': 'Curcuma longa', 'herb_name_common': 'Turmeric'},
        {'herb_name_scientific': 'Taraxacum officinale', 'herb_name_common': 'Dandelion'},
        {'herb_name_scientific': 'Hypericum perforatum', 'herb_name_common': 'St. John\'s Wort'},
        {'herb_name_scientific': 'Melissa officinalis', 'herb_name_common': 'Lemon Balm'},
    ]
    c_light_2 = g.color_linen
    c_dark_2 = g.color_carbon_powder
    images_filepaths = []
    width = 1216
    height = 832
    ### images
    pin_w = 1000
    pin_h = 1500
    row_num = 10
    scale = 0.30
    col_num = 5
    gap = 30
    img_i = 0
    mx = -100
    my = -100
    pin_image = Image.new(mode="RGBA", size=(pin_w, pin_h), color=g.color_linen)
    herb_list_shuffle = herb_list[:]
    random.shuffle(herb_list_shuffle)
    for row_i in range(row_num):
        for col_i in range(col_num):
            img_i = img_i % len(herb_list_shuffle)
            if img_i < len(herb_list_shuffle):
                herb = herb_list_shuffle[img_i]
                herb_name_scientific = herb['herb_name_scientific']
                herb_name_common = herb['herb_name_common']
                herb_slug = herb_name_scientific.lower().strip().replace(' ', '-')
                herb_filename_correct = ''
                for herb_filename in os.listdir(f'assets/shop/labels/public/vintage/oval/3x4/png'):
                    if herb_slug in herb_filename:
                        herb_filename_correct = herb_filename
                        break
                rnd = random.randint(0, 3)
                if rnd == 0:
                    image_filepath = f'assets/shop/labels/public/vintage/round/3x3/png/{herb_filename_correct}'
                    label_w = int(3 * 300 * scale)
                    label_h = int(3 * 300 * scale)
                elif rnd == 1:
                    image_filepath = f'assets/shop/labels/public/vintage/oval/3x4/png/{herb_filename_correct}'
                    label_w = int(3 * 300 * scale)
                    label_h = int(4 * 300 * scale)
                elif rnd == 2:
                    image_filepath = f'assets/shop/labels/public/vintage/square/3x3/png/{herb_filename_correct}'
                    label_w = int(3 * 300 * scale)
                    label_h = int(3 * 300 * scale)
                else:
                    image_filepath = f'assets/shop/labels/public/vintage/rectangle/3x4/png/{herb_filename_correct}'
                    label_w = int(3 * 300 * scale)
                    label_h = int(4 * 300 * scale)
                image = Image.open(image_filepath)
                image = img_resize(image, label_w, label_h)
                label_w = int(3 * 300 * scale)
                label_h = int(4 * 300 * scale)
                pin_image.paste(image, (label_w*col_i+gap*col_i+mx, label_h*row_i+gap*row_i+my), image)
                img_i += 1
    pin_image = pin_image.convert('RGB')
    ### rectangle
    draw = ImageDraw.Draw(pin_image)
    draw.rectangle(((0, pin_h//2 - 160), (pin_w, pin_h//2 + 160)), fill=g.color_carbon_powder)
    ### circle
    circle_size = 420
    x1 = pin_w//2 - circle_size//2
    y1 = pin_h//2 - 160 - circle_size//2
    x2 = pin_w//2 + circle_size//2
    y2 = pin_h//2 - 160 + circle_size//2
    draw.ellipse((x1, y1, x2, y2), fill=g.color_carbon_powder)
    ### number
    color = g.color_linen
    line = '120'
    font_size = 192
    font_family, font_weight = 'Lato', 'Bold'
    font_path = f"assets/fonts/{font_family}/{font_family}-{font_weight}.ttf"
    font = ImageFont.truetype(font_path, font_size)
    _, _, line_w, line_h = font.getbbox(line)
    draw.text((pin_w//2 - line_w//2, pin_h//2 - line_h//2 - 220), line, color, font=font)
    ### text
    gap = 55
    y_off = 0
    line = 'healing herb'.upper()
    font_size = 96
    font_family, font_weight = 'Lato', 'Regular'
    font_path = f"assets/fonts/{font_family}/{font_family}-{font_weight}.ttf"
    font = ImageFont.truetype(font_path, font_size)
    _, _, line_w, line_h = font.getbbox(line)
    draw.text((pin_w//2 - line_w//2, pin_h//2 - line_h//2 - gap + y_off), line, color, font=font)
    ###
    line = 'jar labels'.upper()
    font_size = 96
    font_family, font_weight = 'Allura', 'Regular'
    font_family, font_weight = 'Lato', 'Regular'
    font_path = f"assets/fonts/{font_family}/{font_family}-{font_weight}.ttf"
    font = ImageFont.truetype(font_path, font_size)
    _, _, line_w, line_h = font.getbbox(line)
    draw.text((pin_w//2 - line_w//2, pin_h//2 - line_h//2 + gap + y_off), line, color, font=font)
    # copyright
    y_off = 120
    rect_h = 150
    rect_w = 200
    text_off_y = 25
    draw.rectangle(((pin_w//2 - rect_w, pin_h - y_off - rect_h), (pin_w//2 + rect_w, pin_h - y_off)), fill=g.color_carbon_powder)
    line = 'free designs'.title()
    font_size = 48
    font_family, font_weight = 'Lato', 'Regular'
    font_path = f"assets/fonts/{font_family}/{font_family}-{font_weight}.ttf"
    font = ImageFont.truetype(font_path, font_size)
    _, _, line_w, line_h = font.getbbox(line)
    draw.text((pin_w//2 - line_w//2, pin_h - y_off - rect_h + text_off_y), line, color, font=font)
    line = 'terrawhisper.com'.upper()
    font_size = 16
    font_family, font_weight = 'Lato', 'Regular'
    font_path = f"assets/fonts/{font_family}/{font_family}-{font_weight}.ttf"
    font = ImageFont.truetype(font_path, font_size)
    _, _, line_w, line_h = font.getbbox(line)
    draw.text((pin_w//2 - line_w//2, pin_h - y_off - rect_h + text_off_y + 70), line, color, font=font)
    ### save pin
    img = pin_image.convert('RGB')
    pin_filename = 'herbal-jar-labels'
    img_filepath = pin_save(img, pin_filename)
    img_filepath = f'pinterest/images/{pin_filename}.jpg'
    img.save(img_filepath, format='JPEG', subsampling=0, quality=100)
    pin_image.show()
    ###
    description = f'''Give Your Herbal Jars a Vintage Makeover (For Free). Love herbs? Want to organize your jars in style? Download 120 beautifully designed vintage-style herbal jar labels. These digital labels are inspired by antique apothecary designs and feature the 10 most popular healing herbs, including lavender, chamomile, peppermint, and more.'''
    json_data = {
        'img_filepath': img_filepath,
        'title': 'Healing Herbs Jar Labels',
        'description': description,
        'url': 'https://terrawhisper.com/shop/labels.html',
        'board_name': 'Herbal Designs',
    }
    io.json_write(f'{g.PINTEREST_PINS_IMAGE_FOLDERPATH}/{pin_i}.json', json_data)

def template_plain(images_file_paths, export_file_name):
    pin_w = 1000
    pin_h = 1500
    img = Image.open(images_file_paths[0])
    img = util.img_resize(img, pin_w, pin_h)
    export_file_path = pin_save(img, export_file_name)
    return export_file_path

def template_mosaic(images_file_paths, export_file_name):
    pin_w = 1000
    pin_h = 1500
    img = Image.new(mode="RGB", size=(pin_w, pin_h), color='#ffffff')
    gap = 8
    img_0000 = Image.open(images_file_paths[0])
    img_0001 = Image.open(images_file_paths[1])
    img_0002 = Image.open(images_file_paths[2])
    img_0003 = Image.open(images_file_paths[3])
    img_0000 = util.img_resize(img_0000, int(pin_w*0.66), int(pin_h*0.5))
    img_0001 = util.img_resize(img_0001, int(pin_w*0.66), int(pin_h*0.5))
    img_0002 = util.img_resize(img_0002, int(pin_w*0.66), int(pin_h*0.5))
    img_0003 = util.img_resize(img_0003, int(pin_w*0.66), int(pin_h*0.5))
    img.paste(img_0000, (0, 0))
    img.paste(img_0001, (int(pin_w*0.66) + gap, 0))
    img.paste(img_0002, (-int(pin_w*0.32), int(pin_h*0.5) + gap))
    img.paste(img_0003, (int(pin_w*0.34) + gap, int(pin_h*0.5) + gap))
    export_file_path = pin_save(img, export_file_name)
    return export_file_path

def template_mosaic_inverted(images_file_paths, export_file_name):
    pin_w = 1000
    pin_h = 1500
    img = Image.new(mode="RGB", size=(pin_w, pin_h), color='#ffffff')
    gap = 8
    img_0000 = Image.open(images_file_paths[0])
    img_0001 = Image.open(images_file_paths[1])
    img_0002 = Image.open(images_file_paths[2])
    img_0003 = Image.open(images_file_paths[3])
    img_0000 = util.img_resize(img_0000, int(pin_w*0.66), int(pin_h*0.5))
    img_0001 = util.img_resize(img_0001, int(pin_w*0.66), int(pin_h*0.5))
    img_0002 = util.img_resize(img_0002, int(pin_w*0.66), int(pin_h*0.5))
    img_0003 = util.img_resize(img_0003, int(pin_w*0.66), int(pin_h*0.5))
    img.paste(img_0000, (-int(pin_w*0.32), 0))
    img.paste(img_0001, (int(pin_w*0.34) + gap, 0))
    img.paste(img_0002, (0, int(pin_h*0.5) + gap))
    img.paste(img_0003, (int(pin_w*0.66) + gap, int(pin_h*0.5) + gap))
    export_file_path = pin_save(img, export_file_name)
    return export_file_path

def template_text_backup(data, images_file_paths, export_file_name):
    pin_w = 1000
    pin_h = 1500
    img = Image.new(mode="RGB", size=(pin_w, pin_h), color='#ffffff')
    draw = ImageDraw.Draw(img)
    gap = 8
    rect_h = 320
    img_0000 = Image.open(images_file_paths[0])
    img_0001 = Image.open(images_file_paths[1])
    img_0002 = Image.open(images_file_paths[2])
    img_0003 = Image.open(images_file_paths[3])
    img_0000 = util.img_resize(img_0000, int(pin_w*1), int(pin_h*0.5))
    img_0001 = util.img_resize(img_0001, int(pin_w*1), int(pin_h*0.5))
    img.paste(img_0000, (0, 0))
    img.paste(img_0001, (0, int(pin_h*0.5) + gap))
    random_theme = random.randint(0, 2)
    if random_theme == 0:
        text_color = '#ffffff'
        bg_color = '#000000'    
    elif random_theme == 1:
        text_color = '#ffffff'
        bg_color = '#a21caf'    
    else:
        text_color = '#000000'    
        bg_color = '#ffffff'
    # rect
    draw.rectangle(((0, pin_h//2 - rect_h//2), (pin_w, pin_h//2 + rect_h//2)), fill=bg_color)
    # line
    # draw.line((0, pin_h//2, pin_w, pin_h//2), fill='#ff00ff')
    # data
    try: status_name = data['ailment_name']
    except: pass
    try: status_name = data['status_name']
    except: pass
    text = f'{status_name}'.upper()
    words = text.split(' ')
    lines = []
    if len(words) > 2:
        lines.append(' '.join(words[:2]))
        lines.append(' '.join(words[2:]))
    else:
        lines.append(' '.join(words))
    len_lines_max = 0
    for line in lines:
        if len_lines_max < len(line): len_lines_max = len(line)
    font_size = 64
    font_step_size = 12
    font_start_size = 48
    if len_lines_max < 8: font_size = font_start_size + font_step_size*6
    elif len_lines_max < 12: font_size = font_start_size + font_step_size*5
    elif len_lines_max < 16: font_size = font_start_size + font_step_size*4
    elif len_lines_max < 20: font_size = font_start_size + font_step_size*3
    elif len_lines_max < 24: font_size = font_start_size + font_step_size*2
    elif len_lines_max < 28: font_size = font_start_size + font_step_size*1
    else: font_size = font_start_size + font_step_size*0
    if len(lines) > 1: ml_off_y = int(font_size*0.66)
    else: ml_off_y = 0
    
    # text
    remedies_num = data['main_lst_num']
    preparation_name = data['preparation_name']
    text = f'{main_lst_num} best herbal {preparation_name} for'.title()
    preparations_font_size = 48
    offset_y = int(preparations_font_size*0.2)
    line_spacing = int(preparations_font_size*0.75)
    font_family, font_weight = 'Lato', 'Bold'
    font_path = f"assets/fonts/{font_family}/{font_family}-{font_weight}.ttf"
    font = ImageFont.truetype(font_path, preparations_font_size)
    _, _, text_w, text_h = font.getbbox(text)
    draw.text((pin_w//2 - text_w//2, pin_h//2 - text_h//2 - offset_y - line_spacing- ml_off_y), text, text_color, font=font)
    # text status
    font_family, font_weight = 'Lato', 'Bold'
    font_path = f"assets/fonts/{font_family}/{font_family}-{font_weight}.ttf"
    font = ImageFont.truetype(font_path, font_size)
    _, _, text_w, text_h = font.getbbox(lines[0])
    draw.text((pin_w//2 - text_w//2, pin_h//2 - text_h//2 - offset_y + line_spacing - ml_off_y), lines[0], text_color, font=font)
    if len(lines) > 1:
        _, _, text_w, text_h = font.getbbox(lines[1])
        draw.text((pin_w//2 - text_w//2, pin_h//2 - text_h//2 - offset_y + line_spacing + text_h - ml_off_y), lines[1], text_color, font=font)
    export_file_path = pin_save(img, export_file_name)
    return export_file_path

def template_text(data, images_file_paths, export_file_name):
    pin_w = 1000
    pin_h = 1500
    img = Image.new(mode="RGB", size=(pin_w, pin_h), color='#ffffff')
    draw = ImageDraw.Draw(img)
    gap = 8
    rect_h = 320
    img_0000 = Image.open(images_file_paths[0])
    img_0001 = Image.open(images_file_paths[1])
    img_0002 = Image.open(images_file_paths[2])
    img_0003 = Image.open(images_file_paths[3])
    img_0000 = util.img_resize(img_0000, int(pin_w*1), int(pin_h*0.5))
    img_0001 = util.img_resize(img_0001, int(pin_w*1), int(pin_h*0.5))
    img.paste(img_0000, (0, 0))
    img.paste(img_0001, (0, int(pin_h*0.5) + gap))
    random_theme = random.randint(0, 2)
    if random_theme == 0:
        text_color = '#ffffff'
        bg_color = '#000000'    
    elif random_theme == 1:
        text_color = '#ffffff'
        bg_color = '#a21caf'    
    else:
        text_color = '#000000'    
        bg_color = '#ffffff'

    # rect
    draw.rectangle(((0, pin_h//2 - rect_h//2), (pin_w, pin_h//2 + rect_h//2)), fill=bg_color)

    # circle
    circle_size = 300
    x1 = pin_w//2 - circle_size//2
    y1 = pin_h//2 - 160 - circle_size//2
    x2 = pin_w//2 + circle_size//2
    y2 = pin_h//2 - 160 + circle_size//2
    draw.ellipse((x1, y1, x2, y2), fill=bg_color)

    # draw.rectangle(((0, pin_h//2 - rect_h//2), (pin_w, pin_h//2 + rect_h//2)), fill=bg_color)
    
    ## text split
    try: status_name = data['ailment_name']
    except: pass
    try: status_name = data['status_name']
    except: pass
    text = f'{status_name}'.upper()
    #text = 'Breastfeeding pain'.upper()
    #text = 'Breastfeeding'.upper()
    font_size = 96
    font_family, font_weight = 'Lato', 'Bold'
    font_path = f"assets/fonts/{font_family}/{font_family}-{font_weight}.ttf"
    font = ImageFont.truetype(font_path, font_size)
    _, _, text_w, text_h = font.getbbox(text)

    if text_w > pin_w - 80:
        font_size = 80
        font = ImageFont.truetype(font_path, font_size)
        words = text.split(' ')
        words_per_line = len(words)//2
        line_1 = ' '.join(words[:words_per_line])
        line_2 = ' '.join(words[words_per_line:])
        _, _, text_w, text_h = font.getbbox(line_1)
        draw.text((pin_w//2 - text_w//2, pin_h//2 - text_h//2), line_1, text_color, font=font)
        _, _, text_w, text_h = font.getbbox(line_2)
        draw.text((pin_w//2 - text_w//2, pin_h//2 - text_h//2 + text_h), line_2, text_color, font=font)

        remedies_num = data['main_lst_num']
        preparation_name = data['preparation_name']
        text = f'best herbal {preparation_name} for'.title()
        font_size = 48
        font_family, font_weight = 'Lato', 'Regular'
        font_path = f"assets/fonts/{font_family}/{font_family}-{font_weight}.ttf"
        font = ImageFont.truetype(font_path, font_size)
        _, _, text_w, text_h = font.getbbox(text)
        draw.text((pin_w//2 - text_w//2, pin_h//2 - text_h//2 - text_h*1.5), text, text_color, font=font)

        text = str(data['main_lst_num'])
        font_size = 160
        font_family, font_weight = 'Lato', 'Regular'
        font_path = f"assets/fonts/{font_family}/{font_family}-{font_weight}.ttf"
        font = ImageFont.truetype(font_path, font_size)
        _, _, text_w, text_h = font.getbbox(text)
        x1 = pin_w//2 - text_w//2
        y1 = pin_h//2 - text_h//2 - 210
        draw.text((x1, y1), text, text_color, font=font)
    else:
        draw.text((pin_w//2 - text_w//2, pin_h//2 - text_h//2 + 16), text, text_color, font=font)

        remedies_num = data['main_lst_num']
        preparation_name = data['preparation_name']
        text = f'best herbal {preparation_name} for'.title()
        font_size = 48
        font_family, font_weight = 'Lato', 'Regular'
        font_path = f"assets/fonts/{font_family}/{font_family}-{font_weight}.ttf"
        font = ImageFont.truetype(font_path, font_size)
        _, _, text_w, text_h = font.getbbox(text)
        draw.text((pin_w//2 - text_w//2, pin_h//2 - text_h//2 - text_h*1.2), text, text_color, font=font)

        text = '10'
        font_size = 160
        font_family, font_weight = 'Lato', 'Regular'
        font_path = f"assets/fonts/{font_family}/{font_family}-{font_weight}.ttf"
        font = ImageFont.truetype(font_path, font_size)
        _, _, text_w, text_h = font.getbbox(text)
        x1 = pin_w//2 - text_w//2
        y1 = pin_h//2 - text_h//2 - 210
        draw.text((x1, y1), text, text_color, font=font)

    # text

    export_file_path = pin_save(img, export_file_name)
    return export_file_path

def template_text_2(data, images_file_paths, export_file_name):
    pin_w = 1000
    pin_h = 1500
    img = Image.new(mode="RGB", size=(pin_w, pin_h), color='#ffffff')
    draw = ImageDraw.Draw(img)
    gap = 8
    rect_h = 320
    img_0000 = Image.open(images_file_paths[0])
    img_0001 = Image.open(images_file_paths[1])
    img_0000 = util.img_resize(img_0000, int(pin_w*1), int(pin_h*0.5))
    img_0001 = util.img_resize(img_0001, int(pin_w*1), int(pin_h*0.5))
    img.paste(img_0000, (0, 0))
    img.paste(img_0001, (0, int(pin_h*0.5) + gap))
    random_theme = random.randint(0, 1)
    if random_theme == 0:
        text_color = '#ffffff'
        bg_color = '#000000'    
    else:
        text_color = '#000000'    
        bg_color = '#ffffff'
    # rect
    draw.rectangle(((0, pin_h//2 - rect_h//2), (pin_w, pin_h//2 + rect_h//2)), fill=bg_color)
    # circle
    circle_size = 300
    x1 = pin_w//2 - circle_size//2
    y1 = pin_h//2 - 160 - circle_size//2
    x2 = pin_w//2 + circle_size//2
    y2 = pin_h//2 - 160 + circle_size//2
    draw.ellipse((x1, y1, x2, y2), fill=bg_color)
    # draw.rectangle(((0, pin_h//2 - rect_h//2), (pin_w, pin_h//2 + rect_h//2)), fill=bg_color)
    
    ## text split
    try: status_name = data['ailment_name']
    except: pass
    try: status_name = data['status_name']
    except: pass
    text = f'{status_name}'.upper()
    #text = 'Breastfeeding pain'.upper()
    #text = 'Breastfeeding'.upper()
    font_size = 96
    font_family, font_weight = 'Lato', 'Bold'
    font_path = f"assets/fonts/{font_family}/{font_family}-{font_weight}.ttf"
    font = ImageFont.truetype(font_path, font_size)
    _, _, text_w, text_h = font.getbbox(text)
    if text_w > pin_w - 80:
        font_size = 80
        font = ImageFont.truetype(font_path, font_size)
        words = text.split(' ')
        words_per_line = len(words)//2
        line_1 = ' '.join(words[:words_per_line])
        line_2 = ' '.join(words[words_per_line:])
        _, _, text_w, text_h = font.getbbox(line_1)
        draw.text((pin_w//2 - text_w//2, pin_h//2 - text_h//2), line_1, text_color, font=font)
        _, _, text_w, text_h = font.getbbox(line_2)
        draw.text((pin_w//2 - text_w//2, pin_h//2 - text_h//2 + text_h), line_2, text_color, font=font)
        remedies_num = data['main_lst_num']
        preparation_name = data['preparation_name']
        text = f'best herbal {preparation_name} for'.title()
        font_size = 48
        font_family, font_weight = 'Lato', 'Regular'
        font_path = f"assets/fonts/{font_family}/{font_family}-{font_weight}.ttf"
        font = ImageFont.truetype(font_path, font_size)
        _, _, text_w, text_h = font.getbbox(text)
        draw.text((pin_w//2 - text_w//2, pin_h//2 - text_h//2 - text_h*1.5), text, text_color, font=font)
        text = str(data['main_lst_num'])
        font_size = 160
        font_family, font_weight = 'Lato', 'Regular'
        font_path = f"assets/fonts/{font_family}/{font_family}-{font_weight}.ttf"
        font = ImageFont.truetype(font_path, font_size)
        _, _, text_w, text_h = font.getbbox(text)
        x1 = pin_w//2 - text_w//2
        y1 = pin_h//2 - text_h//2 - 210
        draw.text((x1, y1), text, text_color, font=font)
    else:
        draw.text((pin_w//2 - text_w//2, pin_h//2 - text_h//2 + 16), text, text_color, font=font)
        remedies_num = data['main_lst_num']
        preparation_name = data['preparation_name']
        text = f'best herbal {preparation_name} for'.title()
        font_size = 48
        font_family, font_weight = 'Lato', 'Regular'
        font_path = f"assets/fonts/{font_family}/{font_family}-{font_weight}.ttf"
        font = ImageFont.truetype(font_path, font_size)
        _, _, text_w, text_h = font.getbbox(text)
        draw.text((pin_w//2 - text_w//2, pin_h//2 - text_h//2 - text_h*1.2), text, text_color, font=font)
        text = '10'
        font_size = 160
        font_family, font_weight = 'Lato', 'Regular'
        font_path = f"assets/fonts/{font_family}/{font_family}-{font_weight}.ttf"
        font = ImageFont.truetype(font_path, font_size)
        _, _, text_w, text_h = font.getbbox(text)
        x1 = pin_w//2 - text_w//2
        y1 = pin_h//2 - text_h//2 - 210
        draw.text((x1, y1), text, text_color, font=font)
    # text
    export_file_path = pin_save(img, export_file_name)
    return export_file_path

def template_overlay(data, images_file_paths, export_file_name):
    pin_w = 1000
    pin_h = 1500
    img = Image.new(mode="RGB", size=(pin_w, pin_h), color='#ffffff')
    img_0000 = Image.open(images_file_paths[0])
    img_0000 = util.img_resize(img_0000, int(pin_w*1), int(pin_h*1))
    img.paste(img_0000, (0, 0))
    img = img.convert('RGBA')
    img_overlay = Image.new(mode="RGBA", size=(pin_w, pin_h), color=(0, 0, 0, int(255*0.75)))
    img.paste(img_overlay, (0, 0), img_overlay)
    img = img.convert('RGB')
    ###
    draw = ImageDraw.Draw(img)
    text_color = '#ffffff'
    y_cur = 50
    font_family, font_weight = 'Lato', 'Bold'
    font_path = f"assets/fonts/{font_family}/{font_family}-{font_weight}.ttf"
    font_path = f"assets/fonts/arial/ARIAL.TTF"
    font_path = f"assets/fonts/EB_Garamond/static/EBGaramond-Regular.ttf"
    ###
    text = '10'
    font_size = 384
    font = ImageFont.truetype(font_path, font_size)
    _, _, text_w, text_h = font.getbbox(text)
    draw.text((pin_w//2 - text_w//2, y_cur), text, text_color, font=font)
    y_cur += text_h
    y_cur += 50
    line_height = 1.3
    ###
    font_path = f"assets/fonts/arial/ARIAL.TTF"
    text = 'BEST HERBAL'
    font_size = 32
    font = ImageFont.truetype(font_path, font_size)
    _, _, text_w, text_h = font.getbbox(text)
    draw.text((pin_w//2 - text_w//2, y_cur), text, text_color, font=font)
    y_cur += text_h
    y_cur += 50
    ###
    preparation_name = data['preparation_name']
    text = f'{preparation_name} for'.upper()
    font_size = 96
    font = ImageFont.truetype(font_path, font_size)
    _, _, text_w, text_h = font.getbbox(text)
    draw.text((pin_w//2 - text_w//2, y_cur), text, text_color, font=font)
    y_cur += text_h*line_height
    ###
    ailment_name = data['ailment_name']
    text = f'{ailment_name}'.upper()
    # text = f'difficulty breathing'.upper()
    font_size = 96
    font = ImageFont.truetype(font_path, font_size)
    lines = []
    line = ''
    for word in text.split(' '):
        _, _, word_w, word_h = font.getbbox(word)
        _, _, line_w, line_h = font.getbbox(line)
        if line_w + word_w > int(pin_w*0.75):
            lines.append(line.strip())
            line = f'{word} '
        else:
            line += f'{word} '
    lines.append(line.strip())
    for line in lines:
        _, _, line_w, line_h = font.getbbox(line)
        draw.text((pin_w//2 - line_w//2, y_cur), line, text_color, font=font)
        y_cur += line_h*line_height
    y_cur += 230
    ###
    text = f'find out more >'.upper()
    font_size = 32
    font = ImageFont.truetype(font_path, font_size)
    _, _, text_w, text_h = font.getbbox(text)
    draw.text((pin_w//2 - text_w//2, pin_h-text_h-310), text, text_color, font=font)
    draw.rectangle(((pin_w//2 - text_w//2, pin_h-text_h-310+text_h+10), (pin_w//2 + text_w//2, pin_h-text_h-310+text_h+12)), fill="#ffffff")
    ###
    text = f'terrawhisper.com'.upper()
    font_size = 18
    font = ImageFont.truetype(font_path, font_size)
    _, _, text_w, text_h = font.getbbox(text)
    draw.text((pin_w//2 - text_w//2, pin_h-text_h-80), text, text_color, font=font)
    ###
    export_file_path = pin_save(img, export_file_name)
    return export_file_path

def gen_img_template(line_list, img_list, out_filename, num=0,):
    img_w, img_h = 1000, 1500
    img = Image.new(mode="RGB", size=(img_w, img_h), color='#e7e5e4')
    img1 = Image.open(img_list[0])
    img2 = Image.open(img_list[1])
    img3 = Image.open(img_list[2])
    img4 = Image.open(img_list[3])
    img1.thumbnail([img_w, img_h], Image.Resampling.LANCZOS)
    if random.randint(0, 100) < 50: img1 = ImageOps.mirror(img1)
    img1_w, img1_h = img1.size
    img2.thumbnail([img_w, img_h], Image.Resampling.LANCZOS)
    if random.randint(0, 100) < 50: img2 = ImageOps.mirror(img2)
    img2_w, img2_h = img2.size
    img3.thumbnail([img_w, img_h], Image.Resampling.LANCZOS)
    if random.randint(0, 100) < 50: img3 = ImageOps.mirror(img3)
    img3_w, img3_h = img3.size
    img4.thumbnail([img_w, img_h], Image.Resampling.LANCZOS)
    if random.randint(0, 100) < 50: img4 = ImageOps.mirror(img4)
    img4_w, img4_h = img4.size
    img_num = random.randint(2, 4)
    if img_num == 2:
        img.paste(img1, (0, 0 - int(img1_h*0.25)))
        img.paste(img2, (0, img_h - int(img2_h*0.75)))
    if img_num == 3:
        if random.randint(0, 100) < 50:
            img.paste(img1, (0, 0 - int(img1_h*0.25)))
            img.paste(img2, (0 - int(img2_h*0.50), img_h - int(img2_h*0.75)))
            img.paste(img3, (0 + int(img3_h*0.50), img_h - int(img3_h*0.75)))
            draw = ImageDraw.Draw(img)
            draw.rectangle(((img_w//2 - 4, img_h//2 + 160), (img_w//2 + 4, img_h)), fill="#e7e5e4")
        else:
            img.paste(img2, (0 - int(img2_h*0.50), 0))
            img.paste(img3, (0 + int(img3_h*0.50), 0))
            img.paste(img1, (0, img_h - int(img1_h*0.75)))
            draw = ImageDraw.Draw(img)
            draw.rectangle(((img_w//2 - 4, 0), (img_w//2 + 4, img_h//2 - 160)), fill="#e7e5e4")
    if img_num == 4:
        img.paste(img1, (0 - int(img1_h*0.50), 0))
        img.paste(img2, (0 + int(img2_h*0.50), 0))
        img.paste(img3, (0 - int(img3_h*0.50), img_h - int(img3_h*0.75)))
        img.paste(img4, (0 + int(img4_h*0.50), img_h - int(img4_h*0.75)))
        draw = ImageDraw.Draw(img)
        draw.rectangle(((img_w//2 - 4, 0), (img_w//2 + 4, img_h//2 - 160)), fill="#e7e5e4")
        draw.rectangle(((img_w//2 - 4, img_h//2 + 160), (img_w//2 + 4, img_h)), fill="#e7e5e4")
    text_pos_x = 200
    num = str(num)
    img_w, img_h = 1000, 1500
    
    draw = ImageDraw.Draw(img)
    draw.rectangle(((0, img_h//2 - 160), (img_w, img_h//2 + 160)), fill='#ffffff')
    circle_size = 300
    x = img_w//2-circle_size//2
    draw.ellipse((img_w//2 - circle_size//2, img_h//2 - 160 - circle_size//2, img_w//2 + circle_size//2, img_h//2 - 160 + circle_size//2), fill = "#ffffff")
    font_size = 160
    font_family, font_weight = 'Lato', 'Bold'
    font_path = f"assets/fonts/{font_family}/{font_family}-{font_weight}.ttf"
    font = ImageFont.truetype(font_path, font_size)
    text = num
    text_w = font.getbbox(text)[2]
    text_h = font.getbbox(text)[3]
    draw.text((img_w//2 - text_w//2, img_h//2 - 280), text, '#000000', font=font)
    text_pos_x = 50 + text_w
    font_size = 48
    font_family, font_weight = 'Lato', 'Regular'
    font_path = f"assets/fonts/{font_family}/{font_family}-{font_weight}.ttf"
    font = ImageFont.truetype(font_path, font_size)
    text = line_list[0]
    text_w = font.getbbox(text)[2]
    text_h = font.getbbox(text)[3] 
    draw.text((img_w//2 - text_w//2, img_h//2 - 80), text, '#000000', font=font) 
    text = line_list[1]
    font_size = 96
    if len(text) < 20: 
        font_size = 96
        text_y = img_h//2 - 30
    elif len(text) < 30: 
        font_size = 64
        text_y = img_h//2 - 20
    elif len(text) < 40: 
        font_size = 48
        text_y = img_h//2 - 10
    else: 
        font_size = 32
        text_y = img_h//2 - 0 
    font_family, font_weight = 'Lato', 'Bold'
    font_path = f"assets/fonts/{font_family}/{font_family}-{font_weight}.ttf"
    font = ImageFont.truetype(font_path, font_size)
    text_w = font.getbbox(text)[2]
    text_h = font.getbbox(text)[3]
    draw.text((img_w//2 - text_w//2, text_y), text, '#000000', font=font)
    img_filepath = pin_save(img, out_filename)
    return img_filepath


def pin_gen_backup(article_filepath, preparation_slug):
    preparation_name = preparation_slug.replace('-', ' ')
    data = util.json_read(article_filepath)
    remedy_num = data['main_lst_num']
    title = data['title']
    try: status_name = data['ailment_name']
    except: pass
    try: status_name = data['status_name']
    except: pass
    url = data['url']
    remedies = data['remedies_list']
    filename_out = url.replace('/', '-')

    # get image
    print(f'{vault}/terrawhisper/images/{preparation_slug}/2x3')
    images_folder = f'{vault}/terrawhisper/images/{preparation_slug}/2x3'
    img_creams_folders = os.listdir(images_folder)
    img_creams_filepaths = []
    for folder in img_creams_folders:
        img_filepaths = os.listdir(f'{images_folder}/{folder}')
        for img_filepath in img_filepaths:
            img_creams_filepaths.append(f'{images_folder}/{folder}/{img_filepath}')

    # gen pins
    random.shuffle(img_creams_filepaths)
    images = img_creams_filepaths
    line_1 = f'best herbal {preparation_name} for'.title()
    line_2 = f'{status_name}'.title()
    line_list = [line_1, line_2]

    rand_template = random.randint(0, 2)
    # rand_template = 2
    if rand_template == 0:
        img_filepath = template_plain(images, filename_out)
    elif rand_template == 1:
        if random.randint(0, 1) == 0:
            img_filepath = template_mosaic(images, filename_out)
        else:
            img_filepath = template_mosaic_inverted(images, filename_out)
    else:
        img_filepath = template_text(data, images, filename_out)


def pin_gen(article_filepath, article_i, preparation_slug):
    preparation_name = preparation_slug.replace('-', ' ')
    data = util.json_read(article_filepath)
    remedy_num = data['main_lst_num']
    title = data['title']
    try: status_name = data['ailment_name']
    except: pass
    try: status_name = data['status_name']
    except: pass
    # url = f'https://terrawhisper.com/{data["url"]}.html'
    url = data["url"]
    img_slug = url.replace('/', '-')
    filename_out = url.replace('/', '-')
    if 'remedies_list' in data:
        remedies = data['remedies_list']
    else:
        remedies = data['remedies']
    remedies_descriptions = []
    for remedy in remedies:
        remedies_descriptions.append(remedy['remedy_desc'])
    if remedies_descriptions:
        random.shuffle(remedies_descriptions)
        description = remedies_descriptions[0][:490] + '...'
    else:
        description = ''
    board_name = f'herbal {preparation_name}'.title()
    
    styles = ['', 'website']
    image_style = random.choice(styles)

    herbs_rows, herbs_cols = data_csv.herbs()
    herbs_names_scientific = [herb[herbs_cols['herb_name_scientific']] for herb in herbs_rows]
    images = []
    for i in range(4):
        rnd_herb_name_scientific = random.choice(herbs_names_scientific).strip()
        if preparation_name[-1] == 's': preparation_name_singular = preparation_name[:-1]
        else: preparation_name_singular = preparation_name

        preparation_container = ''
        if preparation_name_singular == 'tea': preparation_container = 'a cup of'
        if preparation_name_singular == 'tincture': preparation_container = 'a bottle of'
        if preparation_name_singular == 'cream': preparation_container = 'a jar of'
        if preparation_name_singular == 'essential oil': preparation_container = 'a bottle of'

        if image_style == 'website':
            prompt_juggernaut_xi = f'''
                {preparation_container} herbal {preparation_name} made with dry {rnd_herb_name_scientific} herb on a wooden table,
                indoor, 
                natural window light,
                earth tones,
                neutral colors,
                soft focus,
                warm tones,
                vintage,
                high resolution,
                cinematic
            '''.replace('  ', ' ')
        elif image_style == 'watercolor':
            prompt_juggernaut_xi = f'''
                close-up of {preparation_container} herbal {preparation_name},
                on a woodent, table, surrounded by {rnd_herb_name_scientific},
                watercolor illustration,  
                depth of field,
                detailed textures, high resolution, cinematic
            '''.replace('  ', ' ')
        else: 
            prompt_juggernaut_xi = f'''
                herbal {preparation_name} on a wooden table indoor surrounded with {rnd_herb_name_scientific}, 
                vibrant colors, 
                depth of field, bokeh, 
                detailed textures, high resolution, cinematic
            '''
            prompt_juggernaut_xi = f'''
                beautiful {preparation_container} {rnd_herb_name_scientific} herbal {preparation_name},
                on a wooden table surrounded by medicinal herbs, 
                portrait, close-up, high resolution, cinematic
            '''
            prompt_juggernaut_x = f'''
                beautiful{preparation_container} of {rnd_herb_name_scientific} herbal {preparation_name},
                on a wooden table surrounded by medicinal herbs, 
                portrait, close-up, high resolution, cinematic
            '''
        prompt = prompt_juggernaut_xi
        print(prompt)
        # image = pipe(prompt=prompt, num_inference_steps=30).images[0]
        # 1024x1024 square
        # 832x1216  portrait
        # 1216x832  landscape
        image = pipe(prompt=prompt, width=832, height=1216, num_inference_steps=30, guidance_scale=7.0).images[0]
        image.save(f'pinterest/tmp/img-{i}.jpg')
        images.append(f'pinterest/tmp/img-{i}.jpg')

    # gen pins
    rand_template = random.randint(0, 100)
    if rand_template >= 0 and rand_template <= 80:
        img_filepath = template_text(data, images, filename_out)
    else:
        img_filepath = template_plain(images, filename_out)

    obj = {
        'title': title,
        'status_name': status_name,
        'preparation_slug': preparation_slug,
        'url': url,
        'description': description,
        'img_filepath': img_filepath,
        'board_name': board_name
    }
    json_write(f'{g.PINTEREST_PINS_IMAGE_FOLDERPATH}/{article_i}.json', obj)


def pin_gen_2(article_filepath, article_i, preparation_slug):
    preparation_name = preparation_slug.replace('-', ' ')
    data = util.json_read(article_filepath)

    title = data['title']
    status_name = data['ailment_name']
    url = data["url"]
    img_slug = url.replace('/', '-')
    filename_out = url.replace('/', '-')
    remedies = data['remedies']
    remedies_descriptions = []

    for remedy in remedies:
        remedies_descriptions.append(remedy['remedy_desc'])

    if remedies_descriptions:
        random.shuffle(remedies_descriptions)
        description = remedies_descriptions[0][:490] + '...'
    else:
        description = ''

    board_name = f'herbal {preparation_name}'.title()
    
    styles = ['', 'website']
    image_style = random.choice(styles)

    herbs_rows, herbs_cols = data_csv.herbs()
    herbs_names_scientific = [herb[herbs_cols['herb_name_scientific']] for herb in herbs_rows]
    images = []

    for i in range(2):
        rnd_herb_name_scientific = random.choice(herbs_names_scientific).strip()
        if preparation_name[-1] == 's': preparation_name_singular = preparation_name[:-1]
        else: preparation_name_singular = preparation_name

        preparation_container = ''
        if preparation_name_singular == 'tea': preparation_container = 'a cup of'
        if preparation_name_singular == 'tincture': preparation_container = 'a bottle of'
        if preparation_name_singular == 'cream': preparation_container = 'a jar of'
        if preparation_name_singular == 'essential oil': preparation_container = 'a bottle of'

        if image_style == 'website':
            prompt_juggernaut_xi = f'''
                close-up of {preparation_container} herbal {preparation_name},
                on a wooden table, 
                surrounded by dry {rnd_herb_name_scientific} herbs,
                indoor, 
                natural window light,
                earth tones,
                neutral colors,
                soft focus,
                warm tones,
                vintage,
                high resolution,
                cinematic
            '''.replace('  ', ' ')
        else: 
            prompt_juggernaut_xi = f'''
                beautiful {preparation_container} {rnd_herb_name_scientific} herbal {preparation_name},
                on a wooden table surrounded by medicinal herbs, 
                portrait, close-up, high resolution, cinematic
            '''
        prompt = prompt_juggernaut_xi
        print(prompt)
        # image = pipe(prompt=prompt, num_inference_steps=30).images[0]
        # 1024x1024 square
        # 832x1216  portrait
        # 1216x832  landscape
        # image = pipe(prompt=prompt, width=832, height=1216, num_inference_steps=30, guidance_scale=7.0).images[0]
        image = pipe(prompt=prompt, width=1216, height=832, num_inference_steps=30, guidance_scale=7.0).images[0]
        image.save(f'pinterest/tmp/img-{i}.jpg')
        images.append(f'pinterest/tmp/img-{i}.jpg')

    # gen pins
    pin_w = 1000
    pin_h = 1500
    img = Image.new(mode="RGB", size=(pin_w, pin_h), color='#ffffff')
    draw = ImageDraw.Draw(img)
    gap = 8
    rect_h = 320

    img_0000 = Image.open(images[0])
    img_0001 = Image.open(images[1])

    img_0000 = util.img_resize(img_0000, int(pin_w*1), int(pin_h*0.5))
    img_0001 = util.img_resize(img_0001, int(pin_w*1), int(pin_h*0.5))

    img.paste(img_0000, (0, 0))
    img.paste(img_0001, (0, int(pin_h*0.5) + gap))
    random_theme = random.randint(0, 1)
    if random_theme == 0:
        text_color = '#ffffff'
        bg_color = '#000000'    
    else:
        text_color = '#000000'    
        bg_color = '#ffffff'

    # rect
    draw.rectangle(((0, pin_h//2 - rect_h//2), (pin_w, pin_h//2 + rect_h//2)), fill=bg_color)

    # circle
    circle_size = 300
    x1 = pin_w//2 - circle_size//2
    y1 = pin_h//2 - 160 - circle_size//2
    x2 = pin_w//2 + circle_size//2
    y2 = pin_h//2 - 160 + circle_size//2
    draw.ellipse((x1, y1, x2, y2), fill=bg_color)

    # draw.rectangle(((0, pin_h//2 - rect_h//2), (pin_w, pin_h//2 + rect_h//2)), fill=bg_color)
    
    ## text split
    try: status_name = data['ailment_name']
    except: pass
    try: status_name = data['status_name']
    except: pass
    text = f'{status_name}'.upper()
    #text = 'Breastfeeding pain'.upper()
    #text = 'Breastfeeding'.upper()
    font_size = 96
    font_family, font_weight = 'Lato', 'Bold'
    font_path = f"assets/fonts/{font_family}/{font_family}-{font_weight}.ttf"
    font = ImageFont.truetype(font_path, font_size)
    _, _, text_w, text_h = font.getbbox(text)

    if text_w > pin_w - 80:
        font_size = 80
        font = ImageFont.truetype(font_path, font_size)
        words = text.split(' ')
        words_per_line = len(words)//2
        line_1 = ' '.join(words[:words_per_line])
        line_2 = ' '.join(words[words_per_line:])
        _, _, text_w, text_h = font.getbbox(line_1)
        draw.text((pin_w//2 - text_w//2, pin_h//2 - text_h//2), line_1, text_color, font=font)
        _, _, text_w, text_h = font.getbbox(line_2)
        draw.text((pin_w//2 - text_w//2, pin_h//2 - text_h//2 + text_h), line_2, text_color, font=font)

        remedies_num = data['main_lst_num']
        preparation_name = data['preparation_name']
        text = f'best herbal {preparation_name} for'.title()
        font_size = 48
        font_family, font_weight = 'Lato', 'Regular'
        font_path = f"assets/fonts/{font_family}/{font_family}-{font_weight}.ttf"
        font = ImageFont.truetype(font_path, font_size)
        _, _, text_w, text_h = font.getbbox(text)
        draw.text((pin_w//2 - text_w//2, pin_h//2 - text_h//2 - text_h*1.5), text, text_color, font=font)

        text = str(data['main_lst_num'])
        font_size = 160
        font_family, font_weight = 'Lato', 'Regular'
        font_path = f"assets/fonts/{font_family}/{font_family}-{font_weight}.ttf"
        font = ImageFont.truetype(font_path, font_size)
        _, _, text_w, text_h = font.getbbox(text)
        x1 = pin_w//2 - text_w//2
        y1 = pin_h//2 - text_h//2 - 210
        draw.text((x1, y1), text, text_color, font=font)
    else:
        draw.text((pin_w//2 - text_w//2, pin_h//2 - text_h//2 + 16), text, text_color, font=font)

        remedies_num = data['main_lst_num']
        preparation_name = data['preparation_name']
        text = f'best herbal {preparation_name} for'.title()
        font_size = 48
        font_family, font_weight = 'Lato', 'Regular'
        font_path = f"assets/fonts/{font_family}/{font_family}-{font_weight}.ttf"
        font = ImageFont.truetype(font_path, font_size)
        _, _, text_w, text_h = font.getbbox(text)
        draw.text((pin_w//2 - text_w//2, pin_h//2 - text_h//2 - text_h*1.2), text, text_color, font=font)

        text = '10'
        font_size = 160
        font_family, font_weight = 'Lato', 'Regular'
        font_path = f"assets/fonts/{font_family}/{font_family}-{font_weight}.ttf"
        font = ImageFont.truetype(font_path, font_size)
        _, _, text_w, text_h = font.getbbox(text)
        x1 = pin_w//2 - text_w//2
        y1 = pin_h//2 - text_h//2 - 210
        draw.text((x1, y1), text, text_color, font=font)

    # text

    img_filepath = pin_save(img, filename_out)

    obj = {
        'title': title,
        'status_name': status_name,
        'preparation_slug': preparation_slug,
        'url': url,
        'description': description,
        'img_filepath': img_filepath,
        'board_name': board_name
    }
    json_write(f'{g.PINTEREST_PINS_IMAGE_FOLDERPATH}/{article_i}.json', obj)


def gen_image_equipment(images, i, equipment_name, image_style, width, height):
    rnd_table = random.choice(['wooden', 'dark'])
    if image_style == 'website':
        prompt_juggernaut_xi = f'''
            {equipment_name},
            on a {rnd_table} table, 
            surrounded by herbs,
            indoor, 
            natural light,
            earth tones,
            neutral colors,
            soft focus,
            warm tones,
            vintage,
            high resolution,
            cinematic
        '''.replace('  ', ' ')
    else: 
        prompt_juggernaut_xi = f'''
            beautiful {preparation_container} {rnd_herb_name_scientific} herbal {preparation_name},
            on a wooden table surrounded by medicinal herbs, 
            portrait, close-up, high resolution, cinematic
        '''
    prompt = prompt_juggernaut_xi
    print(prompt)
    image = pipe(prompt=prompt, width=width, height=height, num_inference_steps=30, guidance_scale=7.0).images[0]
    image.save(f'pinterest/tmp/img-{i}.jpg')
    images.append(f'pinterest/tmp/img-{i}.jpg')


def gen_image(images, i, preparation_name, image_style, width, height):
    rnd_herb_name_scientific = random.choice(herbs_names_scientific).strip()
    if preparation_name[-1] == 's': preparation_name_singular = preparation_name[:-1]
    else: preparation_name_singular = preparation_name

    preparation_container = ''
    if preparation_name_singular == 'tea': preparation_container = 'a cup of'
    if preparation_name_singular == 'tincture': preparation_container = 'a bottle of'
    if preparation_name_singular == 'cream': preparation_container = 'a jar of'
    if preparation_name_singular == 'essential oil': preparation_container = 'a bottle of'

    rnd_table = random.choice(['wooden', 'dark'])

    if image_style == 'website':
        prompt_juggernaut_xi = f'''
            close-up of {preparation_container} herbal {preparation_name},
            on a {rnd_table} table, 
            surrounded by dry {rnd_herb_name_scientific} herbs,
            indoor, 
            natural light,
            earth tones,
            neutral colors,
            soft focus,
            warm tones,
            vintage,
            high resolution,
            cinematic
        '''.replace('  ', ' ')
    elif image_style == 'watercolor': 
        prompt_juggernaut_xi = f'''
            close-up of {preparation_container} herbal {preparation_name},
            on a {rnd_table} table, 
            surrounded by dry {rnd_herb_name_scientific} herbs,
            indoor, 
            watercolor,
        '''.replace('  ', ' ')
    else: 
        prompt_juggernaut_xi = f'''
            beautiful {preparation_container} {rnd_herb_name_scientific} herbal {preparation_name},
            on a wooden table surrounded by medicinal herbs, 
            portrait, close-up, high resolution, cinematic
        '''
    prompt = prompt_juggernaut_xi
    print(prompt)
    image = image_ai(prompt, width, height)
    image.save(f'pinterest/tmp/img-{i}.jpg')
    images.append(f'pinterest/tmp/img-{i}.jpg')

def gen_image_2(images, i, preparation_name, width, height):
    rnd_herb_name_scientific = random.choice(herbs_names_scientific).strip()
    if preparation_name[-1] == 's': preparation_name_singular = preparation_name[:-1]
    else: preparation_name_singular = preparation_name
    ###
    prompt = f'''
        herbal {preparation_name} made with dry {rnd_herb_name_scientific},
        on a wooden table,
        rustic, vintage, boho,
        warm tones,
        high resolution,
    '''.replace('  ', ' ')
    print(prompt)
    image = image_ai(prompt, width, height)
    image.save(f'pinterest/tmp/img-{i}.jpg')
    images.append(f'pinterest/tmp/img-{i}.jpg')

def ai_img_herb(images, i, herb_name_scientific, width, height):
    prompt = f'''
        dry {herb_name_scientific} herb,
        on a wooden table,
        rustic, vintage, boho,
        warm tones,
        high resolution,
    '''.replace('  ', ' ')
    print(prompt)
    image = image_ai(prompt, width, height)
    image.save(f'pinterest/tmp/img-{i}.jpg')
    images.append(f'pinterest/tmp/img-{i}.jpg')

def ai_img_preparation(images, i, preparation_name_plural, herb_name_scientific, width, height):
    prompt = f'''
        herbal {preparation_name_plural} made with dry {herb_name_scientific} herb,
        on a wooden table,
        rustic, vintage, boho,
        warm tones,
        high resolution,
    '''.replace('  ', ' ')
    print(prompt)
    image = image_ai(prompt, width, height)
    image.save(f'pinterest/tmp/img-{i}.jpg')
    images.append(f'pinterest/tmp/img-{i}.jpg')

def equipment_template_1_img_b(data, images_file_paths, export_file_name):
    random_theme = random.randint(0, 1)
    if random_theme == 0:
        text_color = '#ffffff'
        bg_color = '#000000'    
    else:
        text_color = '#000000'    
        bg_color = '#ffffff'

    pin_w = 1000
    pin_h = 1500
    gap = 8
    rect_h = 500

    img = Image.new(mode="RGB", size=(pin_w, pin_h), color=bg_color)
    draw = ImageDraw.Draw(img)
    img_0000 = Image.open(images_file_paths[0])
    img_0000 = util.img_resize(img_0000, pin_w, pin_w)
    img.paste(img_0000, (0, pin_h//3))

    y_cur = 0

    # number
    text = str(data['products_num'])
    font_size = 192
    font_family, font_weight = 'Lato', 'Regular'
    font_path = f"assets/fonts/{font_family}/{font_family}-{font_weight}.ttf"
    font = ImageFont.truetype(font_path, font_size)
    _, _, text_w, text_h = font.getbbox(text)
    x1 = pin_w//2 - text_w//2
    draw.text((x1, y_cur), text, text_color, font=font)
    y_cur += font_size * 1.2

    # product
    try: text = f'best {data["product_type"]}'.upper()
    except: text = f'best {data["equipment_name"]}'.upper()
    font_size = 96
    font_family, font_weight = 'Lato', 'Bold'
    font_path = f"assets/fonts/{font_family}/{font_family}-{font_weight}.ttf"
    font = ImageFont.truetype(font_path, font_size)
    _, _, text_w, text_h = font.getbbox(text)
    draw.text((pin_w//2 - text_w//2, y_cur), text, text_color, font=font)
    y_cur += font_size * 1.2

    # for what
    text = 'for apothecary'.upper()
    font_size = 96
    font_family, font_weight = 'Lato', 'Bold'
    font_path = f"assets/fonts/{font_family}/{font_family}-{font_weight}.ttf"
    font = ImageFont.truetype(font_path, font_size)
    _, _, text_w, text_h = font.getbbox(text)
    draw.text((pin_w//2 - text_w//2, y_cur), text, text_color, font=font)

    export_file_path = pin_save(img, export_file_name)
    return export_file_path


def equipment_template_1_img_t(data, images_file_paths, export_file_name):
    random_theme = random.randint(0, 1)
    if random_theme == 0:
        text_color = '#ffffff'
        bg_color = '#000000'    
    else:
        text_color = '#000000'    
        bg_color = '#ffffff'

    pin_w = 1000
    pin_h = 1500
    gap = 8

    img = Image.new(mode="RGB", size=(pin_w, pin_h), color=bg_color)
    draw = ImageDraw.Draw(img)
    img_0000 = Image.open(images_file_paths[0])
    img_0000 = util.img_resize(img_0000, pin_w, pin_w)
    img.paste(img_0000, (0, 0))

    y_cur = 1000

    # number
    text = str(data['products_num'])
    font_size = 192
    font_family, font_weight = 'Lato', 'Regular'
    font_path = f"assets/fonts/{font_family}/{font_family}-{font_weight}.ttf"
    font = ImageFont.truetype(font_path, font_size)
    _, _, text_w, text_h = font.getbbox(text)
    x1 = pin_w//2 - text_w//2
    draw.text((x1, y_cur), text, text_color, font=font)
    y_cur += font_size * 1.2

    # product
    try: text = f'best {data["product_type"]}'.upper()
    except: text = f'best {data["equipment_name"]}'.upper()
    font_size = 96
    font_family, font_weight = 'Lato', 'Bold'
    font_path = f"assets/fonts/{font_family}/{font_family}-{font_weight}.ttf"
    font = ImageFont.truetype(font_path, font_size)
    _, _, text_w, text_h = font.getbbox(text)
    draw.text((pin_w//2 - text_w//2, y_cur), text, text_color, font=font)
    y_cur += font_size * 1.2

    # for what
    text = 'for apothecary'.upper()
    font_size = 96
    font_family, font_weight = 'Lato', 'Bold'
    font_path = f"assets/fonts/{font_family}/{font_family}-{font_weight}.ttf"
    font = ImageFont.truetype(font_path, font_size)
    _, _, text_w, text_h = font.getbbox(text)
    draw.text((pin_w//2 - text_w//2, y_cur), text, text_color, font=font)

    export_file_path = pin_save(img, export_file_name)
    return export_file_path


def equipment_template_1_img_c(data, images_file_paths, export_file_name):
    random_theme = random.randint(0, 1)
    if random_theme == 0:
        text_color = '#ffffff'
        bg_color = '#000000'    
    else:
        text_color = '#000000'    
        bg_color = '#ffffff'

    pin_w = 1000
    pin_h = 1500
    gap = 8

    img = Image.new(mode="RGB", size=(pin_w, pin_h), color=bg_color)
    draw = ImageDraw.Draw(img)
    # ;jump
    img_0000 = Image.open(images_file_paths[0])
    img_0000 = util.img_resize(img_0000, pin_w, 500)
    img.paste(img_0000, (0, 0))
    img_0001 = Image.open(images_file_paths[1])
    img_0001 = util.img_resize(img_0001, pin_w, 500)
    img.paste(img_0001, (0, 1000))

    y_cur = 500
    draw.rectangle(((0, y_cur), (pin_w, y_cur + 500)), fill=bg_color)
    # y_cur += 30

    # number
    text = str(data['products_num'])
    font_size = 192
    font_family, font_weight = 'Lato', 'Regular'
    font_path = f"assets/fonts/{font_family}/{font_family}-{font_weight}.ttf"
    font = ImageFont.truetype(font_path, font_size)
    _, _, text_w, text_h = font.getbbox(text)
    x1 = pin_w//2 - text_w//2
    draw.text((x1, y_cur), text, text_color, font=font)
    y_cur += font_size * 1.2

    # product
    try: text = f'best {data["product_type"]}'.upper()
    except: text = f'best {data["equipment_name"]}'.upper()
    font_size = 96
    font_family, font_weight = 'Lato', 'Bold'
    font_path = f"assets/fonts/{font_family}/{font_family}-{font_weight}.ttf"
    font = ImageFont.truetype(font_path, font_size)
    _, _, text_w, text_h = font.getbbox(text)
    draw.text((pin_w//2 - text_w//2, y_cur), text, text_color, font=font)
    y_cur += font_size * 1.2

    # for what
    text = 'for apothecary'.upper()
    font_size = 96
    font_family, font_weight = 'Lato', 'Bold'
    font_path = f"assets/fonts/{font_family}/{font_family}-{font_weight}.ttf"
    font = ImageFont.truetype(font_path, font_size)
    _, _, text_w, text_h = font.getbbox(text)
    draw.text((pin_w//2 - text_w//2, y_cur), text, text_color, font=font)

    export_file_path = pin_save(img, export_file_name)
    return export_file_path


def gen_template_1_img_b(data, images_file_paths, export_file_name):
    random_theme = random.randint(0, 1)
    if random_theme == 0:
        text_color = '#ffffff'
        bg_color = '#000000'    
    else:
        text_color = '#000000'    
        bg_color = '#ffffff'

    pin_w = 1000
    pin_h = 1500
    gap = 8
    rect_h = 500

    img = Image.new(mode="RGB", size=(pin_w, pin_h), color=bg_color)
    draw = ImageDraw.Draw(img)
    img_0000 = Image.open(images_file_paths[0])
    img_0000 = util.img_resize(img_0000, pin_w, pin_w)
    img.paste(img_0000, (0, pin_h//3))


    # draw.rectangle(((0, 0), (img_w, img_h//3)), fill=bg_color)

    ## text split
    try: ailment_name = data['ailment_name']
    except: pass
    try: ailment_name = data['status_name']
    except: pass
    ailment_text = f'{ailment_name}'.upper()
    font_size = 96
    font_family, font_weight = 'Lato', 'Bold'
    font_path = f"assets/fonts/{font_family}/{font_family}-{font_weight}.ttf"
    font = ImageFont.truetype(font_path, font_size)
    _, _, ailment_w, ailment_h = font.getbbox(ailment_text)

    ailment_lines = []
    if ailment_w > pin_w - 80:
        '''
        font_size = 80
        font = ImageFont.truetype(font_path, font_size)
        '''
        words = ailment_text.split(' ')
        words_per_line = len(words)//2
        line_1 = ' '.join(words[:words_per_line])
        line_2 = ' '.join(words[words_per_line:])
        ailment_lines.append(line_1)
        ailment_lines.append(line_2)
    else:
        ailment_lines.append(ailment_text)

    # number
    y_start = 0
    if len(ailment_lines) == 2:
        y_start = 0
    elif len(ailment_lines) == 1:
        y_start = 50
    y_cur = y_start
    y_cur += 0

    text = str(data['main_lst_num'])
    font_size = 160
    font_family, font_weight = 'Lato', 'Regular'
    font_path = f"assets/fonts/{font_family}/{font_family}-{font_weight}.ttf"
    font = ImageFont.truetype(font_path, font_size)
    _, _, text_w, text_h = font.getbbox(text)
    x1 = pin_w//2 - text_w//2
    draw.text((x1, y_cur), text, text_color, font=font)
    y_cur += font_size * 1.2

    # preparations
    preparation_name = data['preparation_name']
    text = f'best herbal {preparation_name} for'.title()
    font_size = 48
    font_family, font_weight = 'Lato', 'Regular'
    font_path = f"assets/fonts/{font_family}/{font_family}-{font_weight}.ttf"
    font = ImageFont.truetype(font_path, font_size)
    _, _, text_w, text_h = font.getbbox(text)
    draw.text((pin_w//2 - text_w//2, y_cur), text, text_color, font=font)
    y_cur += font_size * 1.2

    # ailment
    font_size = 96
    font_family, font_weight = 'Lato', 'Bold'
    font_path = f"assets/fonts/{font_family}/{font_family}-{font_weight}.ttf"
    font = ImageFont.truetype(font_path, font_size)
    for line in ailment_lines:
        _, _, line_w, line_h = font.getbbox(line)
        draw.text((pin_w//2 - line_w//2, y_cur), line, text_color, font=font)
        y_cur += font_size

    print('****************************************')
    print(data['main_lst_num'])
    print(data['preparation_name'])
    print(ailment_lines)
    print(x1)
    print(y_cur)
    print('****************************************')


    '''
    if len(ailment_lines) == 2:
        # preparations
        preparation_name = data['preparation_name']
        text = f'best herbal {preparation_name} for'.title()
        font_size = 48
        font_family, font_weight = 'Lato', 'Regular'
        font_path = f"assets/fonts/{font_family}/{font_family}-{font_weight}.ttf"
        font = ImageFont.truetype(font_path, font_size)
        _, _, text_w, text_h = font.getbbox(text)
        draw.text((pin_w//2 - text_w//2, y_cur), text, text_color, font=font)
        y_cur += font_size*1.5

        # ailment
        font_size = 96
        font_family, font_weight = 'Lato', 'Bold'
        font_path = f"assets/fonts/{font_family}/{font_family}-{font_weight}.ttf"
        font = ImageFont.truetype(font_path, font_size)
        line_1 = ailment_lines[0]
        line_2 = ailment_lines[1]
        _, _, line_1_w, line_1_h = font.getbbox(line_1)
        _, _, line_2_w, line_2_h = font.getbbox(line_2)
        y_ailment = rect_h//2 - line_1_h//2
        draw.text((pin_w//2 - line_1_w//2, y_ailment), line_1, text_color, font=font)
        draw.text((pin_w//2 - line_2_w//2, y_ailment + line_2_h), line_2, text_color, font=font)

    if len(ailment_lines) == 1:
        # preparations
        preparation_name = data['preparation_name']
        text = f'best herbal {preparation_name} for'.title()
        font_size = 48
        font_family, font_weight = 'Lato', 'Regular'
        font_path = f"assets/fonts/{font_family}/{font_family}-{font_weight}.ttf"
        font = ImageFont.truetype(font_path, font_size)
        _, _, text_w, text_h = font.getbbox(text)
        draw.text((pin_w//2 - text_w//2, y_cur), text, text_color, font=font)
        y_cur += font_size*1.5

        # ailment
        font_size = 96
        font_family, font_weight = 'Lato', 'Bold'
        font_path = f"assets/fonts/{font_family}/{font_family}-{font_weight}.ttf"
        font = ImageFont.truetype(font_path, font_size)
        line_1 = ailment_lines[0]
        _, _, line_1_w, line_1_h = font.getbbox(line_1)
        y_ailment = rect_h//2 - line_1_h//2
        draw.text((pin_w//2 - line_1_w//2, y_ailment), line_1, text_color, font=font)


    '''
    export_file_path = pin_save(img, export_file_name)
    return export_file_path

def gen_template_1_img_t(data, images_file_paths, export_file_name):
    random_theme = random.randint(0, 1)
    if random_theme == 0:
        text_color = '#ffffff'
        bg_color = '#000000'    
    else:
        text_color = '#000000'    
        bg_color = '#ffffff'

    pin_w = 1000
    pin_h = 1500
    gap = 8

    img = Image.new(mode="RGB", size=(pin_w, pin_h), color=bg_color)
    draw = ImageDraw.Draw(img)
    img_0000 = Image.open(images_file_paths[0])
    img_0000 = util.img_resize(img_0000, pin_w, pin_w)
    img.paste(img_0000, (0, 0))


    # draw.rectangle(((0, 0), (img_w, img_h//3)), fill=bg_color)

    ## text split
    try: ailment_name = data['ailment_name']
    except: pass
    try: ailment_name = data['status_name']
    except: pass
    ailment_text = f'{ailment_name}'.upper()
    font_size = 96
    font_family, font_weight = 'Lato', 'Bold'
    font_path = f"assets/fonts/{font_family}/{font_family}-{font_weight}.ttf"
    font = ImageFont.truetype(font_path, font_size)
    _, _, ailment_w, ailment_h = font.getbbox(ailment_text)

    ailment_lines = []
    if ailment_w > pin_w - 80:
        '''
        font_size = 80
        font = ImageFont.truetype(font_path, font_size)
        '''
        words = ailment_text.split(' ')
        words_per_line = len(words)//2
        line_1 = ' '.join(words[:words_per_line])
        line_2 = ' '.join(words[words_per_line:])
        ailment_lines.append(line_1)
        ailment_lines.append(line_2)
    else:
        ailment_lines.append(ailment_text)

    # number
    y_start = 1000
    if len(ailment_lines) == 2:
        y_start = 1000
    elif len(ailment_lines) == 1:
        y_start = 1050
    y_cur = y_start
    y_cur += 0

    text = str(data['main_lst_num'])
    font_size = 160
    font_family, font_weight = 'Lato', 'Regular'
    font_path = f"assets/fonts/{font_family}/{font_family}-{font_weight}.ttf"
    font = ImageFont.truetype(font_path, font_size)
    _, _, text_w, text_h = font.getbbox(text)
    x1 = pin_w//2 - text_w//2
    draw.text((x1, y_cur), text, text_color, font=font)
    y_cur += font_size * 1.2

    # preparations
    preparation_name = data['preparation_name']
    text = f'best herbal {preparation_name} for'.title()
    font_size = 48
    font_family, font_weight = 'Lato', 'Regular'
    font_path = f"assets/fonts/{font_family}/{font_family}-{font_weight}.ttf"
    font = ImageFont.truetype(font_path, font_size)
    _, _, text_w, text_h = font.getbbox(text)
    draw.text((pin_w//2 - text_w//2, y_cur), text, text_color, font=font)
    y_cur += font_size * 1.2

    # ailment
    font_size = 96
    font_family, font_weight = 'Lato', 'Bold'
    font_path = f"assets/fonts/{font_family}/{font_family}-{font_weight}.ttf"
    font = ImageFont.truetype(font_path, font_size)
    for line in ailment_lines:
        _, _, line_w, line_h = font.getbbox(line)
        draw.text((pin_w//2 - line_w//2, y_cur), line, text_color, font=font)
        y_cur += font_size

    print('****************************************')
    print(data['main_lst_num'])
    print(data['preparation_name'])
    print(ailment_lines)
    print(x1)
    print(y_cur)
    print('****************************************')

    export_file_path = pin_save(img, export_file_name)
    return export_file_path

def template_herb_1(json_article, images_filepaths, export_filename):
    random_theme = random.randint(0, 1)
    if random_theme == 0:
        text_color = '#ffffff'
        bg_color = '#000000'    
    else:
        text_color = '#000000'    
        bg_color = '#ffffff'
    ###
    pin_w = 1000
    pin_h = 1500
    gap = 8
    rect_h = 500
    img = Image.new(mode="RGB", size=(pin_w, pin_h), color=bg_color)
    draw = ImageDraw.Draw(img)
    img_0000 = Image.open(images_filepaths[0])
    img_0000 = util.img_resize(img_0000, pin_w, pin_w)
    img.paste(img_0000, (0, pin_h//3))
    ###
    text = json_article['herb_name_scientific']
    text = f'{text}'.upper()
    font_size = 96
    font_family, font_weight = 'Lato', 'Bold'
    font_path = f"assets/fonts/{font_family}/{font_family}-{font_weight}.ttf"
    font = ImageFont.truetype(font_path, font_size)
    _, _, text_w, text_h = font.getbbox(text)
    lines = []
    if text_w > pin_w - 80:
        words = text.split(' ')
        words_per_line = len(words)//2
        line_1 = ' '.join(words[:words_per_line])
        line_2 = ' '.join(words[words_per_line:])
        lines.append(line_1)
        lines.append(line_2)
    else:
        lines.append(text)
    print(lines)
    ###
    y_start = 0
    if len(lines) == 2: y_start = 0
    elif len(lines) == 1: y_start = 50
    y_cur = y_start
    y_cur += 0
    ###
    text = str(json_article['benefits_num'])
    font_size = 160
    font_family, font_weight = 'Lato', 'Regular'
    font_path = f"assets/fonts/{font_family}/{font_family}-{font_weight}.ttf"
    font = ImageFont.truetype(font_path, font_size)
    _, _, text_w, text_h = font.getbbox(text)
    x1 = pin_w//2 - text_w//2
    draw.text((x1, y_cur), text, text_color, font=font)
    y_cur += font_size * 1.2
    ###
    text = f'best health benefits of'.title()
    font_size = 48
    font_family, font_weight = 'Lato', 'Regular'
    font_path = f"assets/fonts/{font_family}/{font_family}-{font_weight}.ttf"
    font = ImageFont.truetype(font_path, font_size)
    _, _, text_w, text_h = font.getbbox(text)
    draw.text((pin_w//2 - text_w//2, y_cur), text, text_color, font=font)
    y_cur += font_size * 1.2
    ###
    font_size = 96
    font_family, font_weight = 'Lato', 'Bold'
    font_path = f"assets/fonts/{font_family}/{font_family}-{font_weight}.ttf"
    font = ImageFont.truetype(font_path, font_size)
    for line in lines:
        _, _, line_w, line_h = font.getbbox(line)
        draw.text((pin_w//2 - line_w//2, y_cur), line, text_color, font=font)
        y_cur += font_size
    ###
    export_file_path = pin_save(img, export_filename)
    return export_file_path

def template_herb_2(json_article, images_filepaths, export_filename):
    random_theme = random.randint(0, 1)
    if random_theme == 0:
        text_color = '#ffffff'
        bg_color = '#000000'    
    else:
        text_color = '#000000'    
        bg_color = '#ffffff'
    ###
    pin_w = 1000
    pin_h = 1500
    gap = 8
    rect_h = 500
    img = Image.new(mode="RGB", size=(pin_w, pin_h), color=bg_color)
    draw = ImageDraw.Draw(img)
    img_0000 = Image.open(images_filepaths[0])
    img_0000 = util.img_resize(img_0000, pin_w, pin_w)
    img.paste(img_0000, (0, 0))
    ###
    text = json_article['herb_name_scientific']
    text = f'{text}'.upper()
    font_size = 96
    font_family, font_weight = 'Lato', 'Bold'
    font_path = f"assets/fonts/{font_family}/{font_family}-{font_weight}.ttf"
    font = ImageFont.truetype(font_path, font_size)
    _, _, text_w, text_h = font.getbbox(text)
    lines = []
    if text_w > pin_w - 80:
        words = text.split(' ')
        words_per_line = len(words)//2
        line_1 = ' '.join(words[:words_per_line])
        line_2 = ' '.join(words[words_per_line:])
        lines.append(line_1)
        lines.append(line_2)
    else:
        lines.append(text)
    print(lines)
    ###
    y_start = 1000
    if len(lines) == 2: y_start = 1000
    elif len(lines) == 1: y_start = 1050
    y_cur = y_start
    y_cur += 0
    ###
    text = str(json_article['benefits_num'])
    font_size = 160
    font_family, font_weight = 'Lato', 'Regular'
    font_path = f"assets/fonts/{font_family}/{font_family}-{font_weight}.ttf"
    font = ImageFont.truetype(font_path, font_size)
    _, _, text_w, text_h = font.getbbox(text)
    x1 = pin_w//2 - text_w//2
    draw.text((x1, y_cur), text, text_color, font=font)
    y_cur += font_size * 1.2
    ###
    text = f'best health benefits of'.title()
    font_size = 48
    font_family, font_weight = 'Lato', 'Regular'
    font_path = f"assets/fonts/{font_family}/{font_family}-{font_weight}.ttf"
    font = ImageFont.truetype(font_path, font_size)
    _, _, text_w, text_h = font.getbbox(text)
    draw.text((pin_w//2 - text_w//2, y_cur), text, text_color, font=font)
    y_cur += font_size * 1.2
    ###
    font_size = 96
    font_family, font_weight = 'Lato', 'Bold'
    font_path = f"assets/fonts/{font_family}/{font_family}-{font_weight}.ttf"
    font = ImageFont.truetype(font_path, font_size)
    for line in lines:
        _, _, line_w, line_h = font.getbbox(line)
        draw.text((pin_w//2 - line_w//2, y_cur), line, text_color, font=font)
        y_cur += font_size
    ###
    export_file_path = pin_save(img, export_filename)
    return export_file_path

def template_preparation_1(preparation_name_plural, images_filepaths, export_filename):
    random_theme = random.randint(0, 1)
    if random_theme == 0:
        text_color = '#ffffff'
        bg_color = '#000000'    
    else:
        text_color = '#000000'    
        bg_color = '#ffffff'
    ###
    pin_w = 1000
    pin_h = 1500
    gap = 8
    rect_h = 500
    img = Image.new(mode="RGB", size=(pin_w, pin_h), color=bg_color)
    draw = ImageDraw.Draw(img)
    img_0000 = Image.open(images_filepaths[0])
    img_0000 = util.img_resize(img_0000, pin_w, pin_w)
    img.paste(img_0000, (0, pin_h//3))
    ###
    text = f'herbal {preparation_name_plural}'.upper()
    font_size = 96
    font_family, font_weight = 'Lato', 'Bold'
    font_path = f"assets/fonts/{font_family}/{font_family}-{font_weight}.ttf"
    font = ImageFont.truetype(font_path, font_size)
    _, _, text_w, text_h = font.getbbox(text)
    lines = []
    if text_w > pin_w - 80:
        words = text.split(' ')
        words_per_line = len(words)//2
        line_1 = ' '.join(words[:words_per_line])
        line_2 = ' '.join(words[words_per_line:])
        lines.append(line_1)
        lines.append(line_2)
    else:
        lines.append(text)
    print(lines)
    ###
    y_start = 0
    if len(lines) == 2: y_start = 0
    elif len(lines) == 1: y_start = 50
    y_cur = y_start
    y_cur += 0
    ###
    text = str(100)
    font_size = 160
    font_family, font_weight = 'Lato', 'Regular'
    font_path = f"assets/fonts/{font_family}/{font_family}-{font_weight}.ttf"
    font = ImageFont.truetype(font_path, font_size)
    _, _, text_w, text_h = font.getbbox(text)
    x1 = pin_w//2 - text_w//2
    draw.text((x1, y_cur), text, text_color, font=font)
    y_cur += font_size * 1.2
    ###
    text = f'best medicinal'.title()
    font_size = 48
    font_family, font_weight = 'Lato', 'Regular'
    font_path = f"assets/fonts/{font_family}/{font_family}-{font_weight}.ttf"
    font = ImageFont.truetype(font_path, font_size)
    _, _, text_w, text_h = font.getbbox(text)
    draw.text((pin_w//2 - text_w//2, y_cur), text, text_color, font=font)
    y_cur += font_size * 1.2
    ###
    font_size = 96
    font_family, font_weight = 'Lato', 'Bold'
    font_path = f"assets/fonts/{font_family}/{font_family}-{font_weight}.ttf"
    font = ImageFont.truetype(font_path, font_size)
    for line in lines:
        _, _, line_w, line_h = font.getbbox(line)
        draw.text((pin_w//2 - line_w//2, y_cur), line, text_color, font=font)
        y_cur += font_size
    ###
    export_file_path = pin_save(img, export_filename)
    return export_file_path

def template_preparation_2(preparation_name_plural, images_filepaths, export_filename):
    random_theme = random.randint(0, 1)
    if random_theme == 0:
        text_color = '#ffffff'
        bg_color = '#000000'    
    else:
        text_color = '#000000'    
        bg_color = '#ffffff'
    ###
    pin_w = 1000
    pin_h = 1500
    gap = 8
    rect_h = 500
    img = Image.new(mode="RGB", size=(pin_w, pin_h), color=bg_color)
    draw = ImageDraw.Draw(img)
    img_0000 = Image.open(images_filepaths[0])
    img_0000 = util.img_resize(img_0000, pin_w, pin_w)
    img.paste(img_0000, (0, 0))
    ###
    text = f'herbal {preparation_name_plural}'.upper()
    font_size = 96
    font_family, font_weight = 'Lato', 'Bold'
    font_path = f"assets/fonts/{font_family}/{font_family}-{font_weight}.ttf"
    font = ImageFont.truetype(font_path, font_size)
    _, _, text_w, text_h = font.getbbox(text)
    lines = []
    if text_w > pin_w - 80:
        words = text.split(' ')
        words_per_line = len(words)//2
        line_1 = ' '.join(words[:words_per_line])
        line_2 = ' '.join(words[words_per_line:])
        lines.append(line_1)
        lines.append(line_2)
    else:
        lines.append(text)
    print(lines)
    ###
    y_start = 1000
    if len(lines) == 2: y_start = 1000
    elif len(lines) == 1: y_start = 1050
    y_cur = y_start
    y_cur += 0
    ###
    text = str(100)
    font_size = 160
    font_family, font_weight = 'Lato', 'Regular'
    font_path = f"assets/fonts/{font_family}/{font_family}-{font_weight}.ttf"
    font = ImageFont.truetype(font_path, font_size)
    _, _, text_w, text_h = font.getbbox(text)
    x1 = pin_w//2 - text_w//2
    draw.text((x1, y_cur), text, text_color, font=font)
    y_cur += font_size * 1.2
    ###
    text = f'best medicinal'.title()
    font_size = 48
    font_family, font_weight = 'Lato', 'Regular'
    font_path = f"assets/fonts/{font_family}/{font_family}-{font_weight}.ttf"
    font = ImageFont.truetype(font_path, font_size)
    _, _, text_w, text_h = font.getbbox(text)
    draw.text((pin_w//2 - text_w//2, y_cur), text, text_color, font=font)
    y_cur += font_size * 1.2
    ###
    font_size = 96
    font_family, font_weight = 'Lato', 'Bold'
    font_path = f"assets/fonts/{font_family}/{font_family}-{font_weight}.ttf"
    font = ImageFont.truetype(font_path, font_size)
    for line in lines:
        _, _, line_w, line_h = font.getbbox(line)
        draw.text((pin_w//2 - line_w//2, y_cur), line, text_color, font=font)
        y_cur += font_size
    ###
    export_file_path = pin_save(img, export_filename)
    return export_file_path

def template_preparation_3(preparation_name_plural, images_filepaths, export_filename):
    pin_w = 1000
    pin_h = 1500
    img = Image.new(mode="RGB", size=(pin_w, pin_h), color='#ffffff')
    draw = ImageDraw.Draw(img)
    gap = 8
    rect_h = 320
    img_0000 = Image.open(images_filepaths[0])
    img_0001 = Image.open(images_filepaths[1])
    img_0000 = util.img_resize(img_0000, int(pin_w*1), int(pin_h*0.5))
    img_0001 = util.img_resize(img_0001, int(pin_w*1), int(pin_h*0.5))
    img.paste(img_0000, (0, 0))
    img.paste(img_0001, (0, int(pin_h*0.5) + gap))
    random_theme = random.randint(0, 1)
    if random_theme == 0:
        text_color = '#ffffff'
        bg_color = '#000000'    
    else:
        text_color = '#000000'    
        bg_color = '#ffffff'
    # rect
    draw.rectangle(((0, pin_h//2 - rect_h//2), (pin_w, pin_h//2 + rect_h//2)), fill=bg_color)
    # circle
    circle_size = 360
    x1 = pin_w//2 - circle_size//2
    y1 = pin_h//2 - 160 - circle_size//2
    x2 = pin_w//2 + circle_size//2
    y2 = pin_h//2 - 160 + circle_size//2
    draw.ellipse((x1, y1, x2, y2), fill=bg_color)
    ## text split
    text = f'herbal {preparation_name_plural}'.upper()
    font_size = 96
    font_family, font_weight = 'Lato', 'Bold'
    font_path = f"assets/fonts/{font_family}/{font_family}-{font_weight}.ttf"
    font = ImageFont.truetype(font_path, font_size)
    _, _, text_w, text_h = font.getbbox(text)
    if text_w > pin_w - 80:
        font_size = 80
        font = ImageFont.truetype(font_path, font_size)
        words = text.split(' ')
        words_per_line = len(words)//2
        line_1 = ' '.join(words[:words_per_line])
        line_2 = ' '.join(words[words_per_line:])
        _, _, text_w, text_h = font.getbbox(line_1)
        draw.text((pin_w//2 - text_w//2, pin_h//2 - text_h//2), line_1, text_color, font=font)
        _, _, text_w, text_h = font.getbbox(line_2)
        draw.text((pin_w//2 - text_w//2, pin_h//2 - text_h//2 + text_h), line_2, text_color, font=font)
        text = f'best medicinal'.title()
        font_size = 48
        font_family, font_weight = 'Lato', 'Regular'
        font_path = f"assets/fonts/{font_family}/{font_family}-{font_weight}.ttf"
        font = ImageFont.truetype(font_path, font_size)
        _, _, text_w, text_h = font.getbbox(text)
        draw.text((pin_w//2 - text_w//2, pin_h//2 - text_h//2 - text_h*1.5), text, text_color, font=font)
        text = str(100)
        font_size = 160
        font_family, font_weight = 'Lato', 'Regular'
        font_path = f"assets/fonts/{font_family}/{font_family}-{font_weight}.ttf"
        font = ImageFont.truetype(font_path, font_size)
        _, _, text_w, text_h = font.getbbox(text)
        x1 = pin_w//2 - text_w//2
        y1 = pin_h//2 - text_h//2 - 210
        draw.text((x1, y1), text, text_color, font=font)
    else:
        draw.text((pin_w//2 - text_w//2, pin_h//2 - text_h//2 + 16), text, text_color, font=font)
        text = f'best medicinal'.title()
        font_size = 48
        font_family, font_weight = 'Lato', 'Regular'
        font_path = f"assets/fonts/{font_family}/{font_family}-{font_weight}.ttf"
        font = ImageFont.truetype(font_path, font_size)
        _, _, text_w, text_h = font.getbbox(text)
        draw.text((pin_w//2 - text_w//2, pin_h//2 - text_h//2 - text_h*1.2), text, text_color, font=font)
        text = str(100)
        font_size = 160
        font_family, font_weight = 'Lato', 'Regular'
        font_path = f"assets/fonts/{font_family}/{font_family}-{font_weight}.ttf"
        font = ImageFont.truetype(font_path, font_size)
        _, _, text_w, text_h = font.getbbox(text)
        x1 = pin_w//2 - text_w//2
        y1 = pin_h//2 - text_h//2 - 210
        draw.text((x1, y1), text, text_color, font=font)
    # text
    export_file_path = pin_save(img, export_filename)
    return export_file_path

def pin_herb(article_filepath, article_i):
    json_article = util.json_read(article_filepath)
    ###
    title = json_article['title']
    herb_slug = json_article['herb_slug']
    herb_name_scientific = json_article['herb_name_scientific']
    url = json_article["url"]
    img_slug = url.replace('/', '-')
    filename_out = url.replace('/', '-')
    benefits = json_article['benefits']
    benefits_descriptions = []
    for benefit in benefits:
        benefits_descriptions.append(benefit['desc'])
    if benefits_descriptions:
        random.shuffle(benefits_descriptions)
        description = benefits_descriptions[0][:490] + '...'
    else:
        description = ''
    board_name = f'herbs'.title()
    ###
    templates = ['1_img_b', '1_img_t', '2_img_tb', 'overlay']
    templates = ['1_img_b', '1_img_t']
    template = random.choice(templates)
    # template = '1_img_b'
    images = []
    width = 0
    height = 0
    if template == '1_img_b': 
        width = 1024
        height = 1024
        ai_img_herb(images, 0, herb_name_scientific, width, height)
    elif template == '1_img_t': 
        width = 1024
        height = 1024
        ai_img_herb(images, 0, herb_name_scientific, width, height)
    elif template == '2_img_tb': 
        for i in range(2):
            ai_img_herb(images, i, herb_name_scientific, width, height)
        width = 1216
        height = 832
    elif template == 'overlay': 
        width = 832
        height = 1216
        ai_img_herb(images, 0, herb_name_scientific, width, height)
    ####
    if template == '1_img_b':
        img_filepath = template_herb_1(json_article, images, filename_out)
    elif template == '1_img_t':
        img_filepath = template_herb_2(json_article, images, filename_out)
    elif template == '2_img_tb': 
        img_filepath = template_text_2(data, images, filename_out)
    elif template == 'overlay': 
        img_filepath = template_overlay(data, images, filename_out)
    ###
    url = f'http://terrawhisper.com/{url}.html'
    obj = {
        'img_filepath': img_filepath,
        'title': title,
        'herb_slug': herb_slug,
        'herb_name_scientific': herb_name_scientific,
        'description': description,
        'url': url,
        'board_name': board_name
    }
    json_write(f'{g.PINTEREST_PINS_IMAGE_FOLDERPATH}/{article_i}.json', obj)
    pass

def pin_preparation(article_filepath, article_i):
    json_article = util.json_read(article_filepath)
    print(json_article)
    ###
    title = json_article['title']
    preparation_slug = json_article['preparation_slug']
    preparation_name_singular = json_article['preparation_name_singular']
    preparation_name_plural = json_article['preparation_name_plural']
    url = json_article["url"]
    img_slug = url.replace('/', '-')
    filename_out = url.replace('/', '-')
    preparation_list = json_article['preparation_list']
    preparation_list_herbs_names = []
    preparation_list_descriptions = []
    for preparation in preparation_list:
        preparation_list_herbs_names.append(preparation['herb_name_scientific'])
        preparation_list_descriptions.append(preparation['desc'])
    if preparation_list_descriptions:
        random.shuffle(preparation_list_herbs_names)
        random.shuffle(preparation_list_descriptions)
        description = preparation_list_descriptions[0][:490] + '...'
    else:
        description = ''
    board_name = f'herbal preparations'.title()
    print(title)
    print(description)
    ###
    templates = ['1_img_b', '1_img_t', '2_img_tb', 'overlay']
    templates = ['1_img_b', '1_img_t', '2_img_tb']
    template = random.choice(templates)
    # template = '2_img_tb'
    # template = '1_img_b'
    images = []
    width = 0
    height = 0
    if template == '1_img_b': 
        width = 1024
        height = 1024
        ai_img_preparation(images, 0, preparation_name_plural, preparation_list_herbs_names[0], width, height)
    elif template == '1_img_t': 
        width = 1024
        height = 1024
        ai_img_preparation(images, 0, preparation_name_plural, preparation_list_herbs_names[0], width, height)
    elif template == '2_img_tb': 
        for i in range(2):
            ai_img_preparation(images, i, preparation_name_plural, preparation_list_herbs_names[i], width, height)
        width = 1216
        height = 832
    elif template == 'overlay': 
        width = 832
        height = 1216
        # ai_img_herb(images, 0, herb_name_scientific, width, height)
        ai_img_preparation(images, 0, preparation_name_plural, preparation_list_herbs_names[0], width, height)
    ####
    if template == '1_img_b':
        img_filepath = template_preparation_1(preparation_name_plural, images, filename_out)
    elif template == '1_img_t':
        img_filepath = template_preparation_2(preparation_name_plural, images, filename_out)
    elif template == '2_img_tb': 
        img_filepath = template_preparation_3(preparation_name_plural, images, filename_out)
    elif template == 'overlay': 
        img_filepath = template_overlay(data, images, filename_out)
    ###
    url = f'http://terrawhisper.com/{url}.html'
    obj = {
        'img_filepath': img_filepath,
        'title': title,
        'description': description,
        'url': url,
        'board_name': board_name
    }
    json_write(f'{g.PINTEREST_PINS_IMAGE_FOLDERPATH}/{article_i}.json', obj)
    pass

def pin_gen_equipments(article_filepath, article_i, equipment_slug):
    equipment_name = equipment_slug.replace('-', ' ')

    data = util.json_read(article_filepath)
    title = data['title']
    url = data["url"]
    img_slug = url.replace('/', '-')
    filename_out = url.replace('/', '-')
    products = data['products']
    products_descriptions = [x['product_desc'] for x in products]
    if products_descriptions:
        random.shuffle(products_descriptions)
        description = products_descriptions[0][:490] + '...'
    else:
        description = ''

    board_name = f'herbalist equipments'.title()
    
    styles = ['website']
    templates = ['1_img_b', '1_img_t', '']
    image_style = random.choice(styles)
    template = random.choice(templates)
    print(template)

    images = []
    width = 0
    height = 0
    # template = '1_img_t'
    if template == '1_img_b': 
        width = 1024
        height = 1024
        gen_image_equipment(images, 0, equipment_name, image_style, width, height)
    elif template == '1_img_t': 
        width = 1024
        height = 1024
        gen_image_equipment(images, 0, equipment_name, image_style, width, height)
    else:
        width = 1216
        height = 832
        for i in range(2):
            gen_image_equipment(images, i, equipment_name, image_style, width, height)

    # gen pins
    if template == '1_img_b':
        img_filepath = equipment_template_1_img_b(data, images, filename_out)
    elif template == '1_img_t':
        img_filepath = equipment_template_1_img_t(data, images, filename_out)
    else:
        img_filepath = equipment_template_1_img_c(data, images, filename_out)

    obj = {
        'equipment_slug': equipment_slug,
        'equipment_name': equipment_name,
        'title': title,
        'url': url,
        'description': description,
        'img_filepath': img_filepath,
        'board_name': board_name
    }
    json_write(f'{g.PINTEREST_PINS_IMAGE_FOLDERPATH}/{article_i}.json', obj)
    # quit()

def pin_gen_3(article_filepath, article_i, preparation_slug):
    preparation_name = preparation_slug.replace('-', ' ')
    data = util.json_read(article_filepath)
    ###
    title = data['title']
    status_name = data['ailment_name']
    url = data["url"]
    img_slug = url.replace('/', '-')
    filename_out = url.replace('/', '-')
    remedies = data['preparations']
    remedies_descriptions = []

    for remedy in remedies:
        remedies_descriptions.append(remedy['preparation_desc'])

    if remedies_descriptions:
        random.shuffle(remedies_descriptions)
        description = remedies_descriptions[0][:490] + '...'
    else:
        description = ''

    board_name = f'herbal {preparation_name}'.title()
    
    styles = ['website', 'watercolor']
    # templates = ['1_img_b', '1_img_t', '2_img_tb', 'overlay']
    templates = ['1_img_b', '1_img_t', '2_img_tb']
    image_style = random.choice(styles)
    template = random.choice(templates)
    # template = 'overlay' 
    print(template)

    images = []

    width = 0
    height = 0
    if template == '1_img_b': 
        width = 1024
        height = 1024
        gen_image(images, 0, preparation_name, image_style, width, height)
    elif template == '1_img_t': 
        width = 1024
        height = 1024
        gen_image(images, 0, preparation_name, image_style, width, height)
    elif template == '2_img_tb': 
        for i in range(2):
            gen_image(images, i, preparation_name, image_style, width, height)
        width = 1216
        height = 832
    elif template == 'overlay': 
        width = 832
        height = 1216
        # gen_image(images, 0, preparation_name, image_style, width, height)
        gen_image_2(images, 0, preparation_name, width, height)

    # gen pins
    if template == '1_img_b':
        img_filepath = gen_template_1_img_b(data, images, filename_out)
    elif template == '1_img_t':
        img_filepath = gen_template_1_img_t(data, images, filename_out)
    elif template == '2_img_tb': 
        img_filepath = template_text_2(data, images, filename_out)
    elif template == 'overlay': 
        img_filepath = template_overlay(data, images, filename_out)
    ###
    url = f'http://terrawhisper.com/{url}.html'
    obj = {
        'img_filepath': img_filepath,
        'title': title,
        'status_name': status_name,
        'preparation_slug': preparation_slug,
        'description': description,
        'url': url,
        'board_name': board_name
    }
    json_write(f'{g.PINTEREST_PINS_IMAGE_FOLDERPATH}/{article_i}.json', obj)

i = 0
for article_filepath in articles_filepath:
    i += 1
    print(f'{i}/{len(articles_filepath)} >> {article_filepath}')

if 1:
    for filename in os.listdir(g.PINTEREST_TMP_IMAGE_FOLDERPATH):
        os.remove(f'{g.PINTEREST_TMP_IMAGE_FOLDERPATH}/{filename}')
    for filename in os.listdir(g.PINTEREST_PINS_IMAGE_FOLDERPATH):
        os.remove(f'{g.PINTEREST_PINS_IMAGE_FOLDERPATH}/{filename}')
    for filename in os.listdir('pinterest/images'):
        os.remove(f'pinterest/images/{filename}')

def image_ai(prompt, width, height):
    import torch
    from diffusers import DiffusionPipeline, StableDiffusionXLPipeline
    from diffusers import DPMSolverMultistepScheduler
    global pipe
    if not pipe:
        pipe = StableDiffusionXLPipeline.from_single_file(
            checkpoint_filepath, 
            torch_dtype=torch.float16, 
            use_safetensors=True, 
            variant="fp16"
        ).to('cuda')
        pipe.scheduler = DPMSolverMultistepScheduler.from_config(pipe.scheduler.config)
    print(prompt)
    image = pipe(prompt=prompt, width=width, height=height, num_inference_steps=30, guidance_scale=7.0).images[0]
    return image

i = 0

shop_labels(i)
# shop_herb_drying_checklist(i)
i += 1

# PINS HERBS
for article_filepath in herbs_articles_filepath:
    print(f'{i}/{len(articles_filepath)} >> {article_filepath}')
    pin_herb(article_filepath, i)
    i += 1

# PINS PREPARATIONS
for article_filepath in preparations_best_articles_filepath:
    print(f'{i}/{len(articles_filepath)} >> {article_filepath}')
    pin_preparation(article_filepath, i)
    i += 1

# PINS EQUIPMENTS
if 0:
    for article_filepath in equipments_articles_filepath:
        print(f'{i}/{len(articles_filepath)} >> {article_filepath}')
        # pin_gen(article_filepath, i, 'teas')
        equipment_slug = article_filepath.split('/')[-1].replace('.json', '')
        pin_gen_equipments(article_filepath, i, equipment_slug)
        i += 1

# PINS TEAS
for article_filepath in teas_articles_filepath:
    print(f'{i}/{len(articles_filepath)} >> {article_filepath}')
    pin_gen_3(article_filepath, i, 'teas')
    i += 1

# PINS TINCTURES
for article_filepath in tinctures_articles_filepath:
    print(f'{i}/{len(articles_filepath)} >> {article_filepath}')
    pin_gen_3(article_filepath, i, 'tinctures')
    i += 1

# PINS ESSENTIAL OILS
for article_filepath in essential_oils_articles_filepath:
    print(f'{i}/{len(articles_filepath)} >> {article_filepath}')
    pin_gen_3(article_filepath, i, 'essential-oils')
    i += 1

# PINS CREAMS
for article_filepath in creams_articles_filepath:
    print(f'{i}/{len(articles_filepath)} >> {article_filepath}')
    pin_gen_3(article_filepath, i, 'creams')
    i += 1

# card_template_2(i)
i += 1
