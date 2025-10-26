import os
import time
import random
import csv
from datetime import datetime
import re
from bs4 import BeautifulSoup

from PIL import Image, ImageFont, ImageDraw, ImageColor, ImageOps

from lib import g
from lib import io
from lib import llm
from lib import data
from lib import media

pipe = None

checkpoint_filepath = f'{g.vault_tmp_folderpath}/stable-diffusion/juggernautXL_ragnarokBy.safetensors'

random_num = random.randint(-2, 2)
# random_num = 0
ARTICLES_NUM = 51 - random_num

preparation_list = io.csv_to_dict(f'{g.database_folderpath}/csv/preparations.csv')
ailment_list = io.csv_to_dict(f'{g.database_folderpath}/csv/ailments.csv')

teas_articles_filepath = []
tinctures_articles_filepath = []
essential_oils_articles_filepath = []
creams_articles_filepath = []
for ailment in ailment_list:
    ailment_slug = ailment['ailment_slug']
    json_filepath = f'{g.database_folderpath}/json/ailments/{ailment_slug}/teas.json'
    if os.path.exists(json_filepath): 
        print(f'ok: {json_filepath}')
        teas_articles_filepath.append(json_filepath)
    else: 
        print(f'NOT FOUND: {json_filepath}')
    json_filepath = f'{g.database_folderpath}/json/ailments/{ailment_slug}/tinctures.json'
    if os.path.exists(json_filepath): 
        print(f'ok: {json_filepath}')
        tinctures_articles_filepath.append(json_filepath)
    else: 
        print(f'NOT FOUND: {json_filepath}')
    json_filepath = f'{g.database_folderpath}/json/ailments/{ailment_slug}/essential-oils.json'
    if os.path.exists(json_filepath): 
        print(f'ok: {json_filepath}')
        essential_oils_articles_filepath.append(json_filepath)
    else: 
        print(f'NOT FOUND: {json_filepath}')
    json_filepath = f'{g.database_folderpath}/json/ailments/{ailment_slug}/creams.json'
    if os.path.exists(json_filepath): 
        print(f'ok: {json_filepath}')
        creams_articles_filepath.append(json_filepath)
    else: 
        print(f'NOT FOUND: {json_filepath}')

'''
print(teas_articles_filepath)
print(tinctures_articles_filepath)
print(essential_oils_articles_filepath)
print(creams_articles_filepath)
'''

herbs_0000 = io.csv_to_dict(f'{g.database_folderpath}/csv/herbs-book-0000.csv')
herbs_0000 = [herb['herb_name_scientific'].lower().strip() for herb in herbs_0000]
with open(f'{g.database_folderpath}/csv/medical-herbalism.txt') as f:
    herbs_0001 = [line.lower().strip() for line in f.read().split('\n') if line.lower().strip() != '']
herbs = []
for herb in herbs_0000:
    if herb.lower().strip() not in herbs:
        herbs.append(herb)
for herb in herbs_0001:
    if herb.lower().strip() not in herbs:
        herbs.append(herb)

'''
for herb in herbs_0000:
    found = False
    for _herb in herbs:
        print(_herb)
        if _herb.lower().strip() == herb.lower().strip():
            found = True
            break
    if not found:
        herbs.append(herb)
for herb in herbs_0001:
    found = False
    for _herb in herbs:
        print(_herb)
        if _herb.lower().strip() == herb.lower().strip():
            found = True
            break
    if not found:
        herbs.append(herb)
'''
herbs_articles_filepath = []
# herbs = data.herbs_books_get()
json_herbs_folderpath = f'{g.database_folderpath}/json/herbs'
for json_herb_filename in os.listdir(json_herbs_folderpath):
    json_herb_filepath = f'{json_herbs_folderpath}/{json_herb_filename}'
    if os.path.isdir(json_herb_filepath):
        json_herb_folderpath = json_herb_filepath
        json_herb_benefits_filepath = f'{json_herb_folderpath}/benefits.json'
        if os.path.exists(json_herb_benefits_filepath): 
            herbs_articles_filepath.append(json_herb_benefits_filepath)

preparations_best_articles_filepath = []
preparation_list = io.csv_to_dict(f'{g.database_folderpath}/entities/preparations.csv')
json_preparations_folderpath = f'{g.database_folderpath}/json/preparations'
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
    image = pipe(prompt=prompt, width=width, height=height, num_inference_steps=20, guidance_scale=3.0).images[0]
    return image

def pin_save(img, filename):
    img_filepath = f'{g.pinterest_tmp_image_folderpath}/images/{filename}.jpg'
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

def shop_herb_drying_checklist(pin_i):
    c_light_1 = '#f8f7f2'
    c_light_2 = '#dedacf'
    c_dark_1 = '#141410'
    c_dark_2 = '#616140'
    images_filepaths = []
    width = 1216
    height = 832
    entities_herbs_folderpath = f'{g.database_folderpath}/entities/herbs'
    # herb_list = io.csv_to_dict(f'{g.database_folderpath}/csv/herbs.csv')
    herb_list = io.csv_to_dict(f'{g.database_folderpath}/csv/herbs-book-0000.csv')
    herbs_names_scientific = [x['herb_name_scientific'] for x in herb_list]
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
        prompt = f'''
            dry {herb_name_scientific} herb,
            on a wooden table,
            rustic, vintage, boho,
            warm tones,
            high resolution,
        '''.replace('  ', ' ')
        image = image_ai(prompt, width, height)
        image_filepath = f'{g.pinterest_tmp_image_folderpath}/tmp/img-{i}.jpg'
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
    img_0000 = media.resize(img_0000, int(pin_w*1), int(pin_h*0.5))
    img_0001 = media.resize(img_0001, int(pin_w*1), int(pin_h*0.5))
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
    font_path = f"{g.ASSETS_FOLDERPATH}/fonts/{font_family}/{font_family}-{font_weight}.ttf"
    font = ImageFont.truetype(font_path, font_size)
    _, _, text_w, text_h = font.getbbox(text)
    draw.text((pin_w//2 - text_w//2, pin_h//2 - text_h//2 - int(font_size*text_y_off)), text, text_color, font=font)
    text = f'checklist'.upper()
    font_family, font_weight = 'Lato', 'Bold'
    font_path = f"{g.ASSETS_FOLDERPATH}/fonts/{font_family}/{font_family}-{font_weight}.ttf"
    font = ImageFont.truetype(font_path, font_size)
    _, _, text_w, text_h = font.getbbox(text)
    draw.text((pin_w//2 - text_w//2, pin_h//2 - text_h//2 + font_size - int(font_size*text_y_off)), text, text_color, font=font)
    ###
    # image_logo_size = 128
    # image_logo = Image.open('{g.ASSETS_FOLDERPATH}/logo/terrawhisper-logo-round.png')
    # image_logo = media.resize(image_logo, image_logo_size, image_logo_size)
    # img.paste(image_logo, (pin_w//2 - image_logo_size//2, pin_h - image_logo_size - 80), image_logo)
    ###
    text = f'terrawhisper.com'.upper()
    font_size = 24
    font_family, font_weight = 'Lato', 'Bold'
    font_path = f"{g.ASSETS_FOLDERPATH}/fonts/{font_family}/{font_family}-{font_weight}.ttf"
    font = ImageFont.truetype(font_path, font_size)
    _, _, text_w, text_h = font.getbbox(text)
    draw.text((pin_w//2 - text_w//2, pin_h - text_h - 80), text, '#ffffff', font=font)
    ###
    img_filepath = pin_save(img, 'herb-drying-checklist')
    ###
    img = img.convert('RGB')
    img_filepath = f'{g.pinterest_tmp_image_folderpath}/images/herb-drying-checklist.jpg'
    img.save(img_filepath, format='JPEG', subsampling=0, quality=100)
    description = f'''Ready to dry your garden herbs the right way? Download the Ultimate Herb Drying Checklist — a free, easy-to-use digital guide covering everything from harvesting tips to storage methods. Perfect for beginners and seasoned growers alike, this checklist helps you preserve flavor and potency with confidence. Get organized and make the most of your herbal harvest today.'''
    json_data = {
        'img_filepath': img_filepath,
        'title': 'The Ultimate Herb Drying Checklist',
        'description': description,
        'url': 'https://terrawhisper.com/shop/herb-drying-checklist.html',
        'board_name': 'Herbalism Guides',
    }
    io.json_write(f'{g.pinterest_tmp_image_folderpath}/pins/{pin_i}.json', json_data)

def shop_labels(pin_i):
    herb_list = os.listdir(f'{g.ASSETS_FOLDERPATH}/shop/labels/public/100/vintage/oval/1x2/png')
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
    x_cur = mx
    for col_i in range(col_num):
        y_cur = my
        for row_i in range(row_num):
            img_i = img_i % len(herb_list_shuffle)
            herb_filename_correct = herb_list[img_i]
            print(herb_filename_correct)
            rnd = random.randint(0, 3)
            if rnd == 0:
                image_filepath = f'{g.ASSETS_FOLDERPATH}/shop/labels/public/100/vintage/round/3x3/png/{herb_filename_correct}'
                label_w = int(3 * 300 * scale)
                label_h = int(3 * 300 * scale)
            elif rnd == 1:
                image_filepath = f'{g.ASSETS_FOLDERPATH}/shop/labels/public/100/vintage/oval/3x5/png/{herb_filename_correct}'
                label_w = int(3 * 300 * scale)
                label_h = int(5 * 300 * scale)
            elif rnd == 2:
                image_filepath = f'{g.ASSETS_FOLDERPATH}/shop/labels/public/100/vintage/square/3x3/png/{herb_filename_correct}'
                label_w = int(3 * 300 * scale)
                label_h = int(3 * 300 * scale)
            else:
                image_filepath = f'{g.ASSETS_FOLDERPATH}/shop/labels/public/100/vintage/rectangle/3x5/png/{herb_filename_correct}'
                label_w = int(3 * 300 * scale)
                label_h = int(5 * 300 * scale)
            image = Image.open(image_filepath)
            image = media.resize(image, label_w, label_h)
            # pin_image.paste(image, (label_w*col_i+gap*col_i+mx, label_h*row_i+gap*row_i+my), image)
            pin_image.paste(image, (x_cur, y_cur), image)
            y_cur += label_h + gap
            img_i += 1
        x_cur += label_w + gap
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
    font_path = f"{g.ASSETS_FOLDERPATH}/fonts/{font_family}/{font_family}-{font_weight}.ttf"
    font = ImageFont.truetype(font_path, font_size)
    _, _, line_w, line_h = font.getbbox(line)
    draw.text((pin_w//2 - line_w//2, pin_h//2 - line_h//2 - 220), line, color, font=font)
    ### text
    gap = 55
    y_off = 0
    line = 'healing herb'.upper()
    font_size = 96
    font_family, font_weight = 'Lato', 'Regular'
    font_path = f"{g.ASSETS_FOLDERPATH}/fonts/{font_family}/{font_family}-{font_weight}.ttf"
    font = ImageFont.truetype(font_path, font_size)
    _, _, line_w, line_h = font.getbbox(line)
    draw.text((pin_w//2 - line_w//2, pin_h//2 - line_h//2 - gap + y_off), line, color, font=font)
    ###
    line = 'jar labels'.upper()
    font_size = 96
    font_family, font_weight = 'Allura', 'Regular'
    font_family, font_weight = 'Lato', 'Regular'
    font_path = f"{g.ASSETS_FOLDERPATH}/fonts/{font_family}/{font_family}-{font_weight}.ttf"
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
    font_path = f"{g.ASSETS_FOLDERPATH}/fonts/{font_family}/{font_family}-{font_weight}.ttf"
    font = ImageFont.truetype(font_path, font_size)
    _, _, line_w, line_h = font.getbbox(line)
    draw.text((pin_w//2 - line_w//2, pin_h - y_off - rect_h + text_off_y), line, color, font=font)
    line = 'terrawhisper.com'.upper()
    font_size = 16
    font_family, font_weight = 'Lato', 'Regular'
    font_path = f"{g.ASSETS_FOLDERPATH}/fonts/{font_family}/{font_family}-{font_weight}.ttf"
    font = ImageFont.truetype(font_path, font_size)
    _, _, line_w, line_h = font.getbbox(line)
    draw.text((pin_w//2 - line_w//2, pin_h - y_off - rect_h + text_off_y + 70), line, color, font=font)
    ### save pin
    img = pin_image.convert('RGB')
    pin_filename = 'herbal-jar-labels'
    img_filepath = pin_save(img, pin_filename)
    img_filepath = f'{g.pinterest_tmp_image_folderpath}/images/{pin_filename}.jpg'
    img.save(img_filepath, format='JPEG', subsampling=0, quality=100)
    # pin_image.show()
    ###
    description = f'''Give Your Herbal Jars a Vintage Makeover (For Free). Love herbs? Want to organize your jars in style? Download 120 beautifully designed vintage-style herbal jar labels. These digital labels are inspired by antique apothecary designs and feature the 10 most popular healing herbs, including lavender, chamomile, peppermint, and more.'''
    json_data = {
        'img_filepath': img_filepath,
        'title': 'Healing Herbs Jar Labels',
        'description': description,
        'url': 'https://terrawhisper.com/shop/labels.html',
        'board_name': 'Herbal Designs',
    }
    io.json_write(f'{g.pinterest_tmp_image_folderpath}/pins/{pin_i}.json', json_data)

def text_to_lines(text, font, max_w):
    lines = []
    line = ''
    for word in text.split():
        _, _, word_w, word_h = font.getbbox(word)
        _, _, line_w, line_h = font.getbbox(line.strip())
        if  line_w + word_w < max_w:
            line += f'{word} '
        else:
            lines.append(line.strip())
            line = f'{word} '
    if line.strip() != '':
        lines.append(line.strip())
    return lines

def template_herbs(data, images_file_paths, export_file_name):
    pin_w = 1000
    pin_h = 1500
    img = Image.new(mode="RGB", size=(pin_w, pin_h), color='#ffffff')
    draw = ImageDraw.Draw(img)
    gap = 8
    rect_h = 500
    img_0000 = Image.open(images_file_paths[0])
    img_0001 = Image.open(images_file_paths[1])
    img_0000 = media.resize(img_0000, int(pin_w*1), int(pin_w*1))
    img_0001 = media.resize(img_0001, int(pin_w*1), int(pin_w*1))
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
    y_cur = 500
    ### pin image numer 
    text = f'''10'''.upper()
    font_size = 160
    font_family, font_weight = 'Lato', 'Bold'
    font_path = f"{g.ASSETS_FOLDERPATH}/fonts/{font_family}/{font_family}-{font_weight}.ttf"
    font = ImageFont.truetype(font_path, font_size)
    _, _, text_w, text_h = font.getbbox(text)
    lines = text_to_lines(text, font, 800)
    for line in lines:
        _, _, line_w, line_h = font.getbbox(line)
        draw.text((pin_w//2 - line_w//2, y_cur), line, text_color, font=font)
        y_cur += font_size
    y_cur += 16
    ## pin image keyword
    text = f'best herbal teas'.upper()
    font_size = 96
    font_family, font_weight = 'Lato', 'Bold'
    font_path = f"{g.ASSETS_FOLDERPATH}/fonts/{font_family}/{font_family}-{font_weight}.ttf"
    font = ImageFont.truetype(font_path, font_size)
    _, _, text_w, text_h = font.getbbox(text)
    lines = text_to_lines(text, font, 800)
    for line in lines:
        _, _, line_w, line_h = font.getbbox(line)
        draw.text((pin_w//2 - line_w//2, y_cur), line, text_color, font=font)
        y_cur += font_size
    y_cur += 32
    if 0:
        ## pin image ailment
        text = f'''for {data['ailment_name']}'''.title()
        font_size = 48
        font_family, font_weight = 'Lato', 'Regular'
        font_path = f"{g.ASSETS_FOLDERPATH}/fonts/{font_family}/{font_family}-{font_weight}.ttf"
        font = ImageFont.truetype(font_path, font_size)
        _, _, text_w, text_h = font.getbbox(text)
        lines = text_to_lines(text, font, 800)
        for line in lines:
            _, _, line_w, line_h = font.getbbox(line)
            draw.text((pin_w//2 - line_w//2, y_cur), line, text_color, font=font)
            y_cur += font_size
        y_cur += 32
    # text
    export_file_path = pin_save(img, export_file_name)
    # img.show()
    # quit()
    return export_file_path


def template_ailments(data, images_file_paths, export_file_name):
    pin_w = 1000
    pin_h = 1500
    img = Image.new(mode="RGB", size=(pin_w, pin_h), color='#ffffff')
    draw = ImageDraw.Draw(img)
    gap = 8
    rect_h = 500
    img_0000 = Image.open(images_file_paths[0])
    img_0001 = Image.open(images_file_paths[1])
    img_0000 = media.resize(img_0000, int(pin_w*1), int(pin_w*1))
    img_0001 = media.resize(img_0001, int(pin_w*1), int(pin_w*1))
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
    y_cur = 500
    ### pin image numer 
    text = f'''10'''.upper()
    font_size = 160
    font_family, font_weight = 'Lato', 'Bold'
    font_path = f"{g.ASSETS_FOLDERPATH}/fonts/{font_family}/{font_family}-{font_weight}.ttf"
    font = ImageFont.truetype(font_path, font_size)
    _, _, text_w, text_h = font.getbbox(text)
    lines = text_to_lines(text, font, 800)
    for line in lines:
        _, _, line_w, line_h = font.getbbox(line)
        draw.text((pin_w//2 - line_w//2, y_cur), line, text_color, font=font)
        y_cur += font_size
    y_cur += 16
    ## pin image keyword
    text = f'''best herbal {data['preparation_name_plural']}'''.upper()
    font_size = 96
    font_family, font_weight = 'Lato', 'Bold'
    font_path = f"{g.ASSETS_FOLDERPATH}/fonts/{font_family}/{font_family}-{font_weight}.ttf"
    font = ImageFont.truetype(font_path, font_size)
    _, _, text_w, text_h = font.getbbox(text)
    lines = text_to_lines(text, font, 800)
    for line in lines:
        _, _, line_w, line_h = font.getbbox(line)
        draw.text((pin_w//2 - line_w//2, y_cur), line, text_color, font=font)
        y_cur += font_size
    y_cur += 32
    ## pin image ailment
    text = f'''for {data['ailment_name']}'''.title()
    font_size = 48
    font_family, font_weight = 'Lato', 'Regular'
    font_path = f"{g.ASSETS_FOLDERPATH}/fonts/{font_family}/{font_family}-{font_weight}.ttf"
    font = ImageFont.truetype(font_path, font_size)
    _, _, text_w, text_h = font.getbbox(text)
    lines = text_to_lines(text, font, 800)
    for line in lines:
        _, _, line_w, line_h = font.getbbox(line)
        draw.text((pin_w//2 - line_w//2, y_cur), line, text_color, font=font)
        y_cur += font_size
    y_cur += 32
    # text
    export_file_path = pin_save(img, export_file_name)
    # img.show()
    # quit()
    return export_file_path

def pin_template_0000(text_top, text_center, text_bottom, images_file_paths, export_file_name):
    pin_w = 1000
    pin_h = 1500
    img = Image.new(mode="RGB", size=(pin_w, pin_h), color='#ffffff')
    draw = ImageDraw.Draw(img)
    gap = 8
    rect_h = 500
    img_0000 = Image.open(images_file_paths[0])
    img_0001 = Image.open(images_file_paths[1])
    img_0000 = media.resize(img_0000, int(pin_w*1), int(pin_w*1))
    img_0001 = media.resize(img_0001, int(pin_w*1), int(pin_w*1))
    img.paste(img_0000, (0, 0))
    img.paste(img_0001, (0, int(pin_h*0.5) + gap))
    random_theme = random.randint(0, 1)
    if random_theme == 0:
        text_color = '#ffffff'
        bg_color = '#000000'    
    else:
        text_color = '#000000'    
        bg_color = '#ffffff'
    text_color = '#ffffff'
    bg_color = '#000000'    
    # rect
    draw.rectangle(((0, pin_h//2 - rect_h//2), (pin_w, pin_h//2 + rect_h//2)), fill=bg_color)
    y_cur = 64
    ###
    text = f'''{text_top}'''.upper()
    font_size = 64
    font_family, font_weight = 'Lato', 'Bold'
    font_path = f"{g.ASSETS_FOLDERPATH}/fonts/{font_family}/{font_family}-{font_weight}.ttf"
    font = ImageFont.truetype(font_path, font_size)
    _, _, text_w, text_h = font.getbbox(text)
    lines = text_to_lines(text, font, 800)
    for line in lines:
        _, _, line_w, line_h = font.getbbox(line)
        x = pin_w//2 - line_w//2
        draw.rectangle(((x - 32, y_cur - 8), (x + line_w + 32, y_cur + font_size + 24)), fill=bg_color)
        draw.text((pin_w//2 - line_w//2, y_cur), line, text_color, font=font)
        y_cur += font_size
    y_cur = 500
    y_cur += 48
    ### text center
    text = f'''{text_center}'''.title()
    font_size = 108
    font_family, font_weight = 'Lato', 'Regular'
    font_path = f"{g.ASSETS_FOLDERPATH}/fonts/{font_family}/{font_family}-{font_weight}.ttf"
    font = ImageFont.truetype(font_path, font_size)
    _, _, text_w, text_h = font.getbbox(text)
    lines = text_to_lines(text, font, 800)
    for line in lines:
        _, _, line_w, line_h = font.getbbox(line)
        draw.text((pin_w//2 - line_w//2, y_cur), line, text_color, font=font)
        y_cur += font_size
    y_cur += 32
    ### text bottom
    text = f'''TerraWhisper.com >>'''
    font_size = 24
    font_family, font_weight = 'Lato', 'Regular'
    font_path = f"{g.ASSETS_FOLDERPATH}/fonts/{font_family}/{font_family}-{font_weight}.ttf"
    font = ImageFont.truetype(font_path, font_size)
    _, _, text_w, text_h = font.getbbox(text)
    lines = text_to_lines(text, font, 800)
    for line in lines:
        _, _, line_w, line_h = font.getbbox(line)
        draw.text((pin_w//2 - line_w//2, y_cur), line, text_color, font=font)
        y_cur += font_size
    y_cur += 32
    # text
    export_file_path = pin_save(img, export_file_name)
    # img.show()
    # quit()
    return export_file_path

def gen_image(images, i, preparation_name, width, height, prompt=''):
    herb_list = data.herbs_primary_medicinal_get()
    herbs_names_scientific = [x['herb_name_scientific'] for x in herb_list]
    rnd_herb_name_scientific = random.choice(herbs_names_scientific).strip()
    if preparation_name[-1] == 's': preparation_name_singular = preparation_name[:-1]
    else: preparation_name_singular = preparation_name
    ###
    if prompt == '':
        prompt = f'''
            herbal {preparation_name_singular} made with dry {rnd_herb_name_scientific},
            on a wooden table,
            rustic, vintage, boho,
            warm tones,
            high resolution,
        '''.replace('  ', ' ')
        prompt = f'''
            herbal {preparation_name_singular},
            surrounded by medicinal herbs,
            rustic, vintage, boho,
            warm tones,
            high resolution,
        '''.replace('  ', ' ')
    image = media.image_gen(prompt, width, height, steps=20, cfg=6.0)
    image.save(f'{g.pinterest_tmp_image_folderpath}/tmp/img-{i}.jpg')
    images.append(f'{g.pinterest_tmp_image_folderpath}/tmp/img-{i}.jpg')

def ai_img_herb(images, i, herb_name_scientific, width, height):
    prompt = f'''
        dry {herb_name_scientific} herb,
        on a wooden table,
        rustic, vintage, boho,
        warm tones,
        high resolution,
    '''.replace('  ', ' ')
    print(prompt)
    image = media.image_gen(prompt, width, height, steps=20, cfg=6.0)
    image.save(f'{g.pinterest_tmp_image_folderpath}/tmp/img-{i}.jpg')
    images.append(f'{g.pinterest_tmp_image_folderpath}/tmp/img-{i}.jpg')

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
    image.save(f'{g.pinterest_tmp_image_folderpath}/tmp/img-{i}.jpg')
    images.append(f'{g.pinterest_tmp_image_folderpath}/tmp/img-{i}.jpg')

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
    img_0000 = media.resize(img_0000, pin_w, pin_w)
    img.paste(img_0000, (0, pin_h//3))
    ###
    text = json_article['herb_name_scientific']
    text = f'{text}'.upper()
    font_size = 96
    font_family, font_weight = 'Lato', 'Bold'
    font_path = f"{g.ASSETS_FOLDERPATH}/fonts/{font_family}/{font_family}-{font_weight}.ttf"
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
    # text = str(json_article['benefits_num'])
    text = str(10)
    font_size = 160
    font_family, font_weight = 'Lato', 'Regular'
    font_path = f"{g.ASSETS_FOLDERPATH}/fonts/{font_family}/{font_family}-{font_weight}.ttf"
    font = ImageFont.truetype(font_path, font_size)
    _, _, text_w, text_h = font.getbbox(text)
    x1 = pin_w//2 - text_w//2
    draw.text((x1, y_cur), text, text_color, font=font)
    y_cur += font_size * 1.2
    ###
    text = f'best health benefits of'.title()
    font_size = 48
    font_family, font_weight = 'Lato', 'Regular'
    font_path = f"{g.ASSETS_FOLDERPATH}/fonts/{font_family}/{font_family}-{font_weight}.ttf"
    font = ImageFont.truetype(font_path, font_size)
    _, _, text_w, text_h = font.getbbox(text)
    draw.text((pin_w//2 - text_w//2, y_cur), text, text_color, font=font)
    y_cur += font_size * 1.2
    ###
    font_size = 96
    font_family, font_weight = 'Lato', 'Bold'
    font_path = f"{g.ASSETS_FOLDERPATH}/fonts/{font_family}/{font_family}-{font_weight}.ttf"
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
    img_0000 = media.resize(img_0000, pin_w, pin_w)
    img.paste(img_0000, (0, 0))
    ###
    text = json_article['herb_name_scientific']
    text = f'{text}'.upper()
    font_size = 96
    font_family, font_weight = 'Lato', 'Bold'
    font_path = f"{g.ASSETS_FOLDERPATH}/fonts/{font_family}/{font_family}-{font_weight}.ttf"
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
    # text = str(json_article['benefits_num'])
    text = str(10)
    font_size = 160
    font_family, font_weight = 'Lato', 'Regular'
    font_path = f"{g.ASSETS_FOLDERPATH}/fonts/{font_family}/{font_family}-{font_weight}.ttf"
    font = ImageFont.truetype(font_path, font_size)
    _, _, text_w, text_h = font.getbbox(text)
    x1 = pin_w//2 - text_w//2
    draw.text((x1, y_cur), text, text_color, font=font)
    y_cur += font_size * 1.2
    ###
    text = f'best health benefits of'.title()
    font_size = 48
    font_family, font_weight = 'Lato', 'Regular'
    font_path = f"{g.ASSETS_FOLDERPATH}/fonts/{font_family}/{font_family}-{font_weight}.ttf"
    font = ImageFont.truetype(font_path, font_size)
    _, _, text_w, text_h = font.getbbox(text)
    draw.text((pin_w//2 - text_w//2, y_cur), text, text_color, font=font)
    y_cur += font_size * 1.2
    ###
    font_size = 96
    font_family, font_weight = 'Lato', 'Bold'
    font_path = f"{g.ASSETS_FOLDERPATH}/fonts/{font_family}/{font_family}-{font_weight}.ttf"
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
    img_0000 = media.resize(img_0000, int(pin_w*1), int(pin_h*0.5))
    img_0001 = media.resize(img_0001, int(pin_w*1), int(pin_h*0.5))
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
    font_path = f"{g.ASSETS_FOLDERPATH}/fonts/{font_family}/{font_family}-{font_weight}.ttf"
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
        font_path = f"{g.ASSETS_FOLDERPATH}/fonts/{font_family}/{font_family}-{font_weight}.ttf"
        font = ImageFont.truetype(font_path, font_size)
        _, _, text_w, text_h = font.getbbox(text)
        draw.text((pin_w//2 - text_w//2, pin_h//2 - text_h//2 - text_h*1.5), text, text_color, font=font)
        text = str(100)
        font_size = 160
        font_family, font_weight = 'Lato', 'Regular'
        font_path = f"{g.ASSETS_FOLDERPATH}/fonts/{font_family}/{font_family}-{font_weight}.ttf"
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
        font_path = f"{g.ASSETS_FOLDERPATH}/fonts/{font_family}/{font_family}-{font_weight}.ttf"
        font = ImageFont.truetype(font_path, font_size)
        _, _, text_w, text_h = font.getbbox(text)
        draw.text((pin_w//2 - text_w//2, pin_h//2 - text_h//2 - text_h*1.2), text, text_color, font=font)
        text = str(100)
        font_size = 160
        font_family, font_weight = 'Lato', 'Regular'
        font_path = f"{g.ASSETS_FOLDERPATH}/fonts/{font_family}/{font_family}-{font_weight}.ttf"
        font = ImageFont.truetype(font_path, font_size)
        _, _, text_w, text_h = font.getbbox(text)
        x1 = pin_w//2 - text_w//2
        y1 = pin_h//2 - text_h//2 - 210
        draw.text((x1, y1), text, text_color, font=font)
    # text
    export_file_path = pin_save(img, export_filename)
    return export_file_path

def pin_herb(article_filepath, article_i):
    json_article = io.json_read(article_filepath)
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
        benefits_descriptions.append(benefit['benefit_desc'])
    if benefits_descriptions:
        random.shuffle(benefits_descriptions)
        description = benefits_descriptions[0][:490] + '...'
    else:
        description = ''
    board_name = f'herbs'.title()
    ###
    images = []
    width = 1216
    height = 832
    for i in range(2):
        ai_img_herb(images, i, herb_name_scientific, width, height)
    ####
    img_filepath = template_herbs(data, images, filename_out)
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
    io.json_write(f'{g.pinterest_tmp_image_folderpath}/pins/{article_i}.json', obj)
    pass

def pin_preparation(article_filepath, article_i):
    json_article = io.json_read(article_filepath)
    print(json_article)
    ###
    title = json_article['title']
    preparation_slug = json_article['preparation_slug']
    preparation_name_singular = json_article['preparation_name_singular']
    preparation_name_plural = json_article['preparation_name_plural']
    url = json_article["url"]
    img_slug = url.replace('/', '-')
    filename_out = url.replace('/', '-')
    preparation_list = json_article['herbs']
    preparation_list_herbs_names = []
    preparation_list_descriptions = []
    for preparation in preparation_list:
        preparation_list_herbs_names.append(preparation['herb_name_scientific'])
        preparation_list_descriptions.append(preparation['herb_desc'])
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
        ai_img_preparation(images, 0, preparation_name_plural, preparation_list_herbs_names[0], width, height)
    ####
    if template == '1_img_b':
        img_filepath = template_preparation_1(preparation_name_plural, images, filename_out)
    elif template == '1_img_t':
        img_filepath = template_preparation_2(preparation_name_plural, images, filename_out)
    elif template == '2_img_tb': 
        img_filepath = template_preparation_3(preparation_name_plural, images, filename_out)
    ###
    url = f'http://terrawhisper.com/{url}.html'
    obj = {
        'img_filepath': img_filepath,
        'title': title,
        'description': description,
        'url': url,
        'board_name': board_name
    }
    io.json_write(f'{g.pinterest_tmp_image_folderpath}/pins/{article_i}.json', obj)
    pass

def pin_template_checklist(text_center, text_bottom, images_file_paths, export_file_name, subtitle=''):
    pin_w = 1000
    pin_h = 1500
    img = Image.new(mode="RGB", size=(pin_w, pin_h), color='#ffffff')
    draw = ImageDraw.Draw(img)
    gap = 8
    rect_h = 500
    img_0000 = Image.open(images_file_paths[0])
    img_0001 = Image.open(images_file_paths[1])
    img_0000 = media.resize(img_0000, int(pin_w*1), int(pin_w*1))
    img_0001 = media.resize(img_0001, int(pin_w*1), int(pin_w*1))
    img_0000_h = img_0000.size[1]
    img_0001_h = img_0001.size[1]
    # img.paste(img_0000, (0, 0 - int(img_0000_h*0.25)))
    # img.paste(img_0001, (0, int(pin_h*0.5) + gap - int(img_0001_h*0.25)))
    img.paste(img_0000, (0, 0))
    img.paste(img_0001, (0, int(pin_h*0.5) + gap))
    random_theme = random.randint(0, 1)
    if random_theme == 0:
        text_color = '#ffffff'
        bg_color = '#000000'    
    else:
        text_color = '#000000'    
        bg_color = '#ffffff'
    text_color = '#f7f6f2'
    bg_color = '#101211'    
    # rect
    draw.rectangle(((0, pin_h//2 - rect_h//2), (pin_w, pin_h//2 + rect_h//2)), fill=bg_color)
    y_cur = 532
    ### text center
    text = f'''{text_center}'''.upper()
    font_size = 112
    font_family, font_weight = 'Lato', 'Bold'
    font_path = f"{g.ASSETS_FOLDERPATH}/fonts/{font_family}/{font_family}-{font_weight}.ttf"
    font = ImageFont.truetype(font_path, font_size)
    _, _, text_w, text_h = font.getbbox(text)
    lines = text_to_lines(text, font, 800)
    for line in lines:
        _, _, line_w, line_h = font.getbbox(line)
        draw.text((pin_w//2 - line_w//2, y_cur), line, text_color, font=font)
        y_cur += font_size
    y_cur += 48
    ### text bottom
    if 1:
        if subtitle != '':
            text = subtitle
        else:
            text = f'''FREE DOWNLOAD >>'''
        font_size = 24
        font_family, font_weight = 'Lato', 'Regular'
        font_path = f"{g.ASSETS_FOLDERPATH}/fonts/{font_family}/{font_family}-{font_weight}.ttf"
        font = ImageFont.truetype(font_path, font_size)
        _, _, text_w, text_h = font.getbbox(text)
        lines = text_to_lines(text, font, 800)
        for line in lines:
            _, _, line_w, line_h = font.getbbox(line)
            draw.text((pin_w//2 - line_w//2, y_cur), line, text_color, font=font)
            y_cur += font_size
        y_cur += 32
    ### copyright
    if 1:
        line = f'''TerraWhisper.com'''.upper()
        font_size = 24
        font_family, font_weight = 'Lato', 'Regular'
        font_path = f"{g.ASSETS_FOLDERPATH}/fonts/{font_family}/{font_family}-{font_weight}.ttf"
        font = ImageFont.truetype(font_path, font_size)
        _, _, text_w, text_h = font.getbbox(text)
        draw.text((pin_w//2 - line_w//2, pin_h - text_h - 96), line, text_color, font=font)
    # text
    export_file_path = pin_save(img, export_file_name)
    # img.show()
    # quit()
    return export_file_path

def pin_course_preparation_tincture(pin_i):
    ### tmp images
    images = []
    width = 1216
    height = 832
    for i in range(2):
        gen_image(images, i, 'tinctures', width, height)
    tmp_folderpath = f'{g.pinterest_tmp_image_folderpath}/tmp'
    images = [f'{tmp_folderpath}/{filename}' for filename in os.listdir(tmp_folderpath)]
    ### pin image
    img_filepath = pin_template_0000('FREE COURSE', 'How To Make Herbal Tinctures At Home', 'TerraWhisper.com', images, 'course-preparation-tincture')
    ### pin title
    pin_title = 'How to make herbal tinctures at home'
    ### pin description
    pin_description = ''
    prompt = f'''
        Write a description in less that 500 characters for a pinterest pin with the following title: {pin_title}.
        Write only the description.
        Use only ascii characters.
    '''
    prompt += f'/no_think'
    reply = llm.reply(prompt).strip()
    if '</think>' in reply:
        reply = reply.split('</think>')[1].strip()
    if len(pin_description) >= 500:
        pin_description = reply[:490] + '...'
    else:
        pin_description = reply
    ### pin json
    obj = {
        'img_filepath': img_filepath,
        'title': pin_title,
        'description': pin_description,
        'url': f'http://terrawhisper.com/shop/course-preparation-tincture.html',
        'board_name': 'Herbal Tinctures'
    }
    io.json_write(f'{g.pinterest_tmp_image_folderpath}/pins/{pin_i}.json', obj)

def pin_gen_3(article_filepath, article_i, preparation_slug):
    preparation_name = preparation_slug.replace('-', ' ')
    data = io.json_read(article_filepath)
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
    ###
    images = []
    width = 1216
    height = 832
    for i in range(2):
        gen_image(images, i, preparation_name, width, height)
    ### gen pins
    img_filepath = template_ailments(data, images, filename_out)
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
    io.json_write(f'{g.pinterest_tmp_image_folderpath}/pins/{article_i}.json', obj)

def pin_image_gen(article_slug):
    json_article_filepath = f'''{g.database_folderpath}/json/{article_slug}.json'''
    json_article = io.json_read(json_article_filepath, create=True)
    try: article_slug = json_article['article_slug']
    except: article_slug = json_article['article_url_slug']
    article_title = json_article['article_title']
    try: keyword_main = json_article['keyword_main']
    except: keyword_main = json_article['article_keyword']
    try: keyword_main_slug = json_article['keyword_main_slug']
    except: keyword_main_slug = json_article['article_keyword_slug']
    try: keyword_main_pretty = json_article['keyword_main_pretty']
    except: keyword_main_pretty = json_article['article_keyword'] + 's'
    main_list_num = json_article['main_list_num']
    '''
    article_desc = article_title
    article_desc = article_desc.lower()
    article_desc = article_desc.replace(f'{main_list_num}', '')
    for word in keyword_main_pretty.lower().split('\n'):
        article_desc = article_desc.replace(f'{word.lower()}', '')
    article_desc = ' '.join([word for word in article_desc.split() if word != ''])
    '''
    article_desc = 'with healing herbs'
    ###
    images_tmp_filepaths = []
    images_tmp_folderpath = f'{g.pinterest_tmp_image_folderpath}/tmp'
    for image_tmp_filename in os.listdir(images_tmp_folderpath):
        image_tmp_filepath = f'{images_tmp_folderpath}/{image_tmp_filename}'
        images_tmp_filepaths.append(image_tmp_filepath)
    export_filename = f'{keyword_main_slug}'
    ###
    text_color = '#ffffff'
    bg_color = '#000000'    
    ###
    pin_w = 1000
    pin_h = 1500
    gap = 8
    rect_h = 500
    img = Image.new(mode="RGB", size=(pin_w, pin_h), color=bg_color)
    draw = ImageDraw.Draw(img)
    img_0000 = Image.open(images_tmp_filepaths[0])
    img_0000 = media.resize(img_0000, pin_w//2, pin_w//2)
    img_0001 = Image.open(images_tmp_filepaths[1])
    img_0001 = media.resize(img_0001, pin_w//2, pin_w//2)
    img_0002 = Image.open(images_tmp_filepaths[2])
    img_0002 = media.resize(img_0002, pin_w//2, pin_w//2)
    img_0003 = Image.open(images_tmp_filepaths[3])
    img_0003 = media.resize(img_0003, pin_w//2, pin_w//2)
    img.paste(img_0000, (0, int(pin_h*0.0) - gap))
    img.paste(img_0001, (0, int(pin_h*0.66) + gap))
    img.paste(img_0002, (int(pin_w*0.5) + gap, int(pin_h*0.0) - gap))
    img.paste(img_0003, (int(pin_w*0.5) + gap, int(pin_h*0.66) + gap))
    y_cur = 500
    ### rect
    draw.rectangle(((0, 500), (1000, 1000)), fill=bg_color)
    ### number
    text = main_list_num
    text = f'{text}'.upper()
    font_size = 160
    font_family, font_weight = 'Lato', 'Bold'
    font_path = f"{g.ASSETS_FOLDERPATH}/fonts/{font_family}/{font_family}-{font_weight}.ttf"
    font = ImageFont.truetype(font_path, font_size)
    _, _, text_w, text_h = font.getbbox(text)
    lines = text_to_lines(text, font, 800)
    for line in lines:
        _, _, line_w, line_h = font.getbbox(line)
        draw.text((pin_w//2 - line_w//2, y_cur), line, text_color, font=font)
        y_cur += font_size
    y_cur += 16
    ### keyword
    text = f'{keyword_main_pretty}'.upper()
    font_size = 96
    y_off = 0
    line_w_max = 900
    for _ in range(10):
        font_family, font_weight = 'Lato', 'Bold'
        font_path = f"{g.ASSETS_FOLDERPATH}/fonts/{font_family}/{font_family}-{font_weight}.ttf"
        font = ImageFont.truetype(font_path, font_size)
        _, _, text_w, text_h = font.getbbox(text)
        lines = text_to_lines(text, font, line_w_max)
        if len(lines) == 2: break
        if len(lines) > 2:
            font_size -= 4
            y_off += 4
        else:
            # font_size += 4
            # y_off -= 4
            line_w_max -= 50
    y_cur += y_off
    for line in lines:
        _, _, line_w, line_h = font.getbbox(line)
        draw.text((pin_w//2 - line_w//2, y_cur), line, text_color, font=font)
        y_cur += font_size
    y_cur += 32
    ### subtitle
    text = article_desc
    text = f'{text}'.lower()
    font_size = 32
    font_family, font_weight = 'Lato', 'Regular'
    font_path = f"{g.ASSETS_FOLDERPATH}/fonts/{font_family}/{font_family}-{font_weight}.ttf"
    font = ImageFont.truetype(font_path, font_size)
    _, _, text_w, text_h = font.getbbox(text)
    lines = text_to_lines(text, font, 800)
    for line in lines:
        _, _, line_w, line_h = font.getbbox(line)
        draw.text((pin_w//2 - line_w//2, y_cur), line, text_color, font=font)
        y_cur += font_size
    ###
    export_filepath = pin_image_save(img, export_filename)
    return export_filepath

def pin_image_save(img, filename):
    img_filepath = f'{g.pinterest_tmp_image_folderpath}/images/{filename}.jpg'
    img.save(
        img_filepath,
        format='JPEG',
        subsampling=0,
        quality=100,
    )
    return img_filepath

def pin_checklist_foraging_fall(pin_i):
    ### tmp images
    images = []
    width = 1216
    height = 832
    if 1:
        for i in range(2):
            prompt = f'''
                autumn wallpaper with plants,
                nature photography,
                scenic view,
                soft focus,
                bokeh,
                depth of field,
                high resolution
            '''
            gen_image(images, i, '-', width, height, prompt=prompt)
    tmp_folderpath = f'{g.pinterest_tmp_image_folderpath}/tmp'
    images = [f'{tmp_folderpath}/{filename}' for filename in os.listdir(tmp_folderpath)]
    ### pin image
    img_filepath = pin_template_checklist('Fall Foraging Checklist', 'TerraWhisper.com', images, 'fall-foraging-checklist')
    ### pin title
    pin_title = 'Fall Foraging Checklist'
    ### pin description
    pin_description = ''
    prompt = f'''
        Write a description in less that 500 characters for a pinterest pin with the following title: {pin_title}.
        Write only the description.
        Use only ascii characters.
    '''
    prompt += f'/no_think'
    reply = llm.reply(prompt).strip()
    if '</think>' in reply:
        reply = reply.split('</think>')[1].strip()
    if len(pin_description) >= 500:
        pin_description = reply[:490] + '...'
    else:
        pin_description = reply
    ### pin json
    obj = {
        'img_filepath': img_filepath,
        'title': pin_title,
        'description': pin_description,
        'url': f'http://terrawhisper.com/shop/fall-foraging-cecklist.html',
        'board_name': 'Herbalism Guides'
    }
    io.json_write(f'{g.pinterest_tmp_image_folderpath}/pins/{pin_i}.json', obj)

def pin_quick_start_guide_preparation_lotion(pin_i):
    images = []
    width = 1216
    height = 832
    if 1:
        for i in range(2):
            prompt = f'''
                herbal lotion made with dry herbs,
                on a wooden table,
                surrounded by medicinal herbs,
                rustic, vintage, boho,
                soft focus,
                warm tones,
                high resolution,
            '''
            gen_image(images, i, '-', width, height, prompt=prompt)
    tmp_folderpath = f'{g.pinterest_tmp_image_folderpath}/tmp'
    images = [f'{tmp_folderpath}/{filename}' for filename in os.listdir(tmp_folderpath)]
    ### pin image
    img_filepath = pin_template_checklist('Make Your First Herbal Lotion', 'TerraWhisper.com', images, 'quick-start-guide-preparation-lotion', subtitle='FREE QUICK-START GUIDE >>')
    ### pin title
    pin_title = 'Make Your First Herbal Lotion'
    ### pin description
    pin_description = ''
    prompt = f'''
        Write a description in less that 500 characters for a pinterest pin with the following title: {pin_title}.
        Write only the description.
        Use only ascii characters.
    '''
    prompt += f'/no_think'
    reply = llm.reply(prompt).strip()
    if '</think>' in reply:
        reply = reply.split('</think>')[1].strip()
    if len(pin_description) >= 500:
        pin_description = reply[:490] + '...'
    else:
        pin_description = reply
    ### pin json
    obj = {
        'img_filepath': img_filepath,
        'title': pin_title,
        'description': pin_description,
        'url': f'http://terrawhisper.com/shop/quick-start-guide-preparation-lotion.html',
        'board_name': 'Herbalism Guides'
    }
    io.json_write(f'{g.pinterest_tmp_image_folderpath}/pins/{pin_i}.json', obj)

i = 0
for article_filepath in articles_filepath:
    i += 1
    print(f'{i}/{len(articles_filepath)} >> {article_filepath}')

if 1:
    for filename in os.listdir(f'{g.pinterest_tmp_image_folderpath}/tmp'):
        os.remove(f'{g.pinterest_tmp_image_folderpath}/tmp/{filename}')
    for filename in os.listdir(f'{g.pinterest_tmp_image_folderpath}/images'):
        os.remove(f'{g.pinterest_tmp_image_folderpath}/images/{filename}')
    for filename in os.listdir(f'{g.pinterest_tmp_image_folderpath}/pins'):
        os.remove(f'{g.pinterest_tmp_image_folderpath}/pins/{filename}')
    pass

i = 0

########################################
### 1-page handouts
########################################
if 0:
    pin_quick_start_guide_preparation_lotion(i)
    i += 1

if 0:
    pin_checklist_foraging_fall(i)
    i += 1

# quit()

########################################
### course
########################################
if 0:
    pin_course_preparation_tincture(i)
    i += 1

########################################
### labels
########################################
if 0:
    shop_labels(i)
    i += 1
    shop_herb_drying_checklist(i)
    i += 1
    # quit()


########################################
### aesthetic
########################################
from data import art_data
articles_slugs = []

art_aesthetic_articles_slugs = [item['article_url_slug'] for item in art_data.art_aesthetic_data]

for item in art_aesthetic_articles_slugs:
    articles_slugs.append([item])

if 0:
    articles_slugs = [
        [
            f'''wellness/skin-care/herbs''',
        ],
        [
            f'''herbs/types/flowers''',
        ],
        [
            f'''herbs/types/trees/christmas/ideas''',
        ],
        [
            f'''nutrition/drinks/coffee/aesthetic''',
            f'''nutrition/drinks/matcha/aesthetic''',
        ],
        [
            f'''art/crafts/pumpkin/carving/ideas''',
            f'''art/crafts/pumpkin/painting/ideas''',
        ],
        [
            f'''art/wallpapers/green''',
            f'''art/wallpapers/dark''',
            f'''art/wallpapers/dark/aesthetic''',
            f'''art/wallpapers/iphone/aesthetic''',
        ],
        [
            f'''art/nature/travel/aesthetic''',
        ],
        [
            f'''apothecary/kitchen/design''',
        ],
        [
            f'''apothecary/academia/dark/aesthetic''',
        ],
        [
            f'''spirituality/moon/aesthetic''',
            f'''spirituality/moon/wallpaper''',
            f'''spirituality/stars/aesthetic''',
        ],
        [
            f'''nature/photography''',
        ],
    ]



    if 0:
        articles_slugs = [
            [
                f'''herbs/types/trees/christmas/ideas''',
            ],
            [
                f'''nature/photography''',
            ],
        ]

def tmp_image_gen(json_article, keyword_main_slug):
    width = 1024
    height = 1024
    for i in range(4):
        prompt = json_article['images_prompts'][0]
        image = media.image_gen(prompt, width, height)
        image.save(f'{g.pinterest_tmp_image_folderpath}/tmp/img-{i}.jpg')
        ###

random.shuffle(articles_slugs)
for cluster_slugs in articles_slugs[:10]:
    article_slug = random.choice(cluster_slugs)
    print(article_slug)
    json_article_filepath = f'''{g.database_folderpath}/json/{article_slug}.json'''
    json_article = io.json_read(json_article_filepath)
    try: article_slug = json_article['article_slug']
    except: article_slug = json_article['article_url_slug']
    article_title = json_article['article_title']
    try: keyword_main = json_article['keyword_main']
    except: keyword_main = json_article['article_keyword']
    try: keyword_main_slug = json_article['keyword_main_slug']
    except: keyword_main_slug = json_article['article_keyword_slug']
    try: pin_board_name = json_article['pin_board_name'].title()
    except: pin_board_name = 'Herbal Art'
    ### gen tmp images
    tmp_image_gen(json_article, keyword_main_slug)
    ### gen pin image
    pin_image_filepath = pin_image_gen(article_slug)
    ### gen pin json
    article_description = ''
    prompt = f'''
        Write a description in less that 500 characters for a pinterest pin with the following title: {article_title}.
        Write only the description.
        Use only ascii characters.
    '''
    prompt += f'/no_think'
    reply = llm.reply(prompt).strip()
    if '</think>' in reply:
        reply = reply.split('</think>')[1].strip()
    if len(article_description) >= 500:
        article_description = reply[:490] + '...'
    else:
        article_description = reply
    # board_name = 'plants art'.title()
    article_url = f'https://terrawhisper.com/{article_slug}.html'
    obj = {
        'img_filepath': pin_image_filepath,
        'title': article_title,
        'description': article_description,
        'url': article_url,
        'board_name': pin_board_name
    }
    io.json_write(f'{g.pinterest_tmp_image_folderpath}/pins/{i}.json', obj)
    # quit()
    i += 1

# quit()

if 0:
    # PINS HERBS
    for article_filepath in herbs_articles_filepath:
        print(f'{i}/{len(articles_filepath)} >> {article_filepath}')
        pin_herb(article_filepath, i)
        i += 1
        quit()

    # PINS PREPARATIONS
    for article_filepath in preparations_best_articles_filepath:
        print(f'{i}/{len(articles_filepath)} >> {article_filepath}')
        pin_preparation(article_filepath, i)
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

print(datetime.now())
