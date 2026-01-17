import os
import random
import csv
from datetime import datetime

from PIL import Image, ImageFont, ImageDraw, ImageColor, ImageOps

from lib import g
from lib import io
from lib import llm
from lib import data
from lib import media
from lib import zimage

file_content = '90'
if 0:
    try:
        with open('pinterest_article_num') as f: file_content = f.read()
    except:
        with open('pinterest_article_num', 'w') as f: f.write(file_content)

random_num = random.randint(-4, 4)
ARTICLES_NUM = int(file_content) - random_num

ailment_list = io.csv_to_dict(f'{g.database_folderpath}/csv/ailments.csv')

teas_articles_filepath = []
tinctures_articles_filepath = []
decoctions_articles_filepath = []
essential_oils_articles_filepath = []
creams_articles_filepath = []
juices_articles_filepath = []
linctuses_articles_filepath = []
syrups_articles_filepath = []
baths_articles_filepath = []
capsules_articles_filepath = []
for ailment in ailment_list:
    ailment_slug = ailment['ailment_slug']
    json_filepath = f'{g.database_folderpath}/json/ailments/{ailment_slug}/teas.json'
    if os.path.exists(json_filepath): 
        print(f'ok: {json_filepath}')
        teas_articles_filepath.append(json_filepath)
    else: 
        print(f'NOT FOUND: {json_filepath}')
    ###
    json_filepath = f'{g.database_folderpath}/json/ailments/{ailment_slug}/tinctures.json'
    if os.path.exists(json_filepath): 
        print(f'ok: {json_filepath}')
        tinctures_articles_filepath.append(json_filepath)
    else: 
        print(f'NOT FOUND: {json_filepath}')
    ###
    json_filepath = f'{g.database_folderpath}/json/ailments/{ailment_slug}/decoctions.json'
    if os.path.exists(json_filepath): 
        print(f'ok: {json_filepath}')
        decoctions_articles_filepath.append(json_filepath)
    else: 
        print(f'NOT FOUND: {json_filepath}')
    ###
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
    ###
    json_filepath = f'{g.database_folderpath}/json/ailments/{ailment_slug}/juices.json'
    if os.path.exists(json_filepath): 
        print(f'ok: {json_filepath}')
        juices_articles_filepath.append(json_filepath)
    ###
    json_filepath = f'{g.database_folderpath}/json/ailments/{ailment_slug}/linctuses.json'
    if os.path.exists(json_filepath): 
        print(f'ok: {json_filepath}')
        linctuses_articles_filepath.append(json_filepath)
    ###
    json_filepath = f'{g.database_folderpath}/json/ailments/{ailment_slug}/syrups.json'
    if os.path.exists(json_filepath): 
        print(f'ok: {json_filepath}')
        syrups_articles_filepath.append(json_filepath)
    json_filepath = f'{g.database_folderpath}/json/ailments/{ailment_slug}/baths.json'
    if os.path.exists(json_filepath): 
        print(f'ok: {json_filepath}')
        baths_articles_filepath.append(json_filepath)
    json_filepath = f'{g.database_folderpath}/json/ailments/{ailment_slug}/capsules.json'
    if os.path.exists(json_filepath): 
        print(f'ok: {json_filepath}')
        capsules_articles_filepath.append(json_filepath)
    else: 
        print(f'NOT FOUND: {json_filepath}')

herbs_articles_filepath = []
json_herbs_folderpath = f'{g.database_folderpath}/json/herbs'
for json_herb_filename in os.listdir(json_herbs_folderpath):
    json_herb_filepath = f'{json_herbs_folderpath}/{json_herb_filename}'
    if os.path.isdir(json_herb_filepath):
        json_herb_folderpath = json_herb_filepath
        json_herb_benefits_filepath = f'{json_herb_folderpath}/benefits.json'
        if os.path.exists(json_herb_benefits_filepath): 
            herbs_articles_filepath.append(json_herb_benefits_filepath)

random.shuffle(herbs_articles_filepath)
random.shuffle(teas_articles_filepath)
random.shuffle(tinctures_articles_filepath)
random.shuffle(decoctions_articles_filepath)
random.shuffle(essential_oils_articles_filepath)
random.shuffle(creams_articles_filepath)
random.shuffle(juices_articles_filepath)
random.shuffle(linctuses_articles_filepath)
random.shuffle(syrups_articles_filepath)
random.shuffle(baths_articles_filepath)
random.shuffle(capsules_articles_filepath)

herbs_articles_filepath_tmp = []
teas_articles_filepath_tmp = []
tinctures_articles_filepath_tmp = []
decoctions_articles_filepath_tmp = []
essential_oils_articles_filepath_tmp = []
creams_articles_filepath_tmp = []
juices_articles_filepath_tmp = []
linctuses_articles_filepath_tmp = []
syrups_articles_filepath_tmp = []
baths_articles_filepath_tmp = []
capsules_articles_filepath_tmp = []

def article_num_cur_get():
    return (
        len(herbs_articles_filepath_tmp) + \
        len(teas_articles_filepath_tmp) + \
        len(tinctures_articles_filepath_tmp) + \
        len(decoctions_articles_filepath_tmp) + \
        len(essential_oils_articles_filepath_tmp) + \
        len(creams_articles_filepath_tmp) + \
        len(juices_articles_filepath_tmp) + \
        len(linctuses_articles_filepath_tmp) + \
        len(syrups_articles_filepath_tmp) + \
        len(baths_articles_filepath_tmp) + \
        len(capsules_articles_filepath_tmp) + \
        len([])
    )

articles_filepath = []
for i in range(999):
    try: herbs_articles_filepath_tmp.append(herbs_articles_filepath[i])
    except: pass
    if article_num_cur_get() >= ARTICLES_NUM: break
    try: teas_articles_filepath_tmp.append(teas_articles_filepath[i])
    except: pass
    if article_num_cur_get() >= ARTICLES_NUM: break
    try: tinctures_articles_filepath_tmp.append(tinctures_articles_filepath[i])
    except: pass
    ###
    if article_num_cur_get() >= ARTICLES_NUM: break
    try: decoctions_articles_filepath_tmp.append(decoctions_articles_filepath[i])
    except: pass
    ###
    if article_num_cur_get() >= ARTICLES_NUM: break
    try: essential_oils_articles_filepath_tmp.append(essential_oils_articles_filepath[i])
    except: pass
    ###
    if article_num_cur_get() >= ARTICLES_NUM: break
    try: creams_articles_filepath_tmp.append(creams_articles_filepath[i])
    except: pass
    ###
    if article_num_cur_get() >= ARTICLES_NUM: break
    try: juices_articles_filepath_tmp.append(juices_articles_filepath[i])
    except: pass
    ###
    if article_num_cur_get() >= ARTICLES_NUM: break
    try: linctuses_articles_filepath_tmp.append(linctuses_articles_filepath[i])
    except: pass
    ###
    if article_num_cur_get() >= ARTICLES_NUM: break
    try: syrups_articles_filepath_tmp.append(syrups_articles_filepath[i])
    except: pass
    if article_num_cur_get() >= ARTICLES_NUM: break
    try: baths_articles_filepath_tmp.append(baths_articles_filepath[i])
    except: pass
    if article_num_cur_get() >= ARTICLES_NUM: break
    try: capsules_articles_filepath_tmp.append(capsules_articles_filepath[i])
    except: pass
    if article_num_cur_get() >= ARTICLES_NUM: break

herbs_articles_filepath = herbs_articles_filepath_tmp
teas_articles_filepath = teas_articles_filepath_tmp
tinctures_articles_filepath = tinctures_articles_filepath_tmp
decoctions_articles_filepath = decoctions_articles_filepath_tmp
essential_oils_articles_filepath = essential_oils_articles_filepath_tmp
creams_articles_filepath = creams_articles_filepath_tmp
juices_articles_filepath = juices_articles_filepath_tmp
linctuses_articles_filepath = linctuses_articles_filepath_tmp
syrups_articles_filepath = syrups_articles_filepath_tmp
baths_articles_filepath = baths_articles_filepath_tmp
capsules_articles_filepath = capsules_articles_filepath_tmp

for filepath in herbs_articles_filepath: articles_filepath.append(filepath)
for filepath in teas_articles_filepath: articles_filepath.append(filepath)
for filepath in tinctures_articles_filepath: articles_filepath.append(filepath)
for filepath in decoctions_articles_filepath: articles_filepath.append(filepath)
for filepath in essential_oils_articles_filepath: articles_filepath.append(filepath)
for filepath in creams_articles_filepath: articles_filepath.append(filepath)
for filepath in juices_articles_filepath: articles_filepath.append(filepath)
for filepath in linctuses_articles_filepath: articles_filepath.append(filepath)
for filepath in syrups_articles_filepath: articles_filepath.append(filepath)
for filepath in baths_articles_filepath: articles_filepath.append(filepath)
for filepath in capsules_articles_filepath: articles_filepath.append(filepath)

for filepath in articles_filepath:
    print(filepath)

print(ARTICLES_NUM)
print(len(herbs_articles_filepath))
print(len(teas_articles_filepath))
print(len(tinctures_articles_filepath))
print(len(decoctions_articles_filepath))
print(len(essential_oils_articles_filepath))
print(len(creams_articles_filepath))
print(len(juices_articles_filepath))
print(len(linctuses_articles_filepath))
print(len(syrups_articles_filepath))
print(len(baths_articles_filepath))
print(len(capsules_articles_filepath))

# quit()

###########################################################################
# PROMPTS
###########################################################################

prompts_tables = ['table', 'wooden table', 'oak table', 'mapple table', 'walnut table', 'marble table', 'granite table', 'dark table']

###########################################################################
# UTILS
###########################################################################

def pin_save(img, filename):
    img_filepath = f'{g.pinterest_tmp_image_folderpath}/images/{filename}.jpg'
    img.save(
        img_filepath,
        format='JPEG',
        subsampling=0,
        quality=100,
    )
    return img_filepath

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

def template_herbs_new(data, images_file_paths, export_file_name, herb_name_common, template):
    random_theme = random.randint(0, 1)
    if random_theme == 0:
        text_color = '#ffffff'
        bg_color = '#000000'    
    else:
        text_color = '#000000'    
        bg_color = '#ffffff'
    pin_w = 1000
    pin_h = 1500
    img = Image.new(mode="RGB", size=(pin_w, pin_h), color='#ffffff')
    draw = ImageDraw.Draw(img)
    gap = 4
    rect_h = 500
    if template == 1:
        img_0000 = Image.open(images_file_paths[0])
        img_0001 = Image.open(images_file_paths[1])
        img.paste(img_0000, (int(0.0), int(pin_h*0.0)))
        img.paste(img_0001, (int(0.0), int(pin_h*0.66)))
    if template == 2:
        img_0000 = Image.open(images_file_paths[0])
        img_0001 = Image.open(images_file_paths[1])
        img_0002 = Image.open(images_file_paths[2])
        img.paste(img_0000, (int(0.0), int(pin_h*0.0)))
        img.paste(img_0001, (int(0.0), int(pin_h*0.66)))
        img.paste(img_0002, (int(pin_w*0.5) + gap, int(pin_h*0.66) + gap))
        draw.rectangle(((pin_w//2-gap, int(pin_h*0.5)), (pin_w//2+gap, pin_h)), fill=bg_color)
    if template == 3:
        img_0000 = Image.open(images_file_paths[0])
        img_0001 = Image.open(images_file_paths[1])
        img_0002 = Image.open(images_file_paths[2])
        img.paste(img_0000, (int(0.0), int(pin_h*0.0)))
        img.paste(img_0001, (int(pin_w*0.5), int(pin_h*0.0)))
        img.paste(img_0002, (int(0.0), int(pin_h*0.66) + gap))
        draw.rectangle(((pin_w//2-gap, int(pin_h*0.0)), (pin_w//2+gap, int(pin_h*0.5))), fill=bg_color)
    if template == 4:
        img_0000 = Image.open(images_file_paths[0])
        img_0001 = Image.open(images_file_paths[1])
        img_0002 = Image.open(images_file_paths[2])
        img_0003 = Image.open(images_file_paths[3])
        img.paste(img_0000, (int(0.0), int(pin_h*0.0)))
        img.paste(img_0001, (int(pin_w*0.5), int(pin_h*0.0)))
        img.paste(img_0002, (int(0.0), int(pin_h*0.66)))
        img.paste(img_0003, (int(pin_w*0.5), int(pin_h*0.66)))
        draw.rectangle(((pin_w//2-gap, 0), (pin_w//2+gap, pin_h)), fill=bg_color)
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
    y_cur += 32
    ## pin image keyword
    text = f'most popular benefits of'.upper()
    font_size = 48
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
    ###
    text = f'{herb_name_common}'.upper()
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
    y_cur += 64
    ###
    if len(lines) == 1:
        text = f'Discover Benefits >'.upper()
        font_size = 24
        font_family, font_weight = 'Lato', 'Bold'
        font_path = f"{g.ASSETS_FOLDERPATH}/fonts/{font_family}/{font_family}-{font_weight}.ttf"
        font = ImageFont.truetype(font_path, font_size)
        _, _, text_w, text_h = font.getbbox(text)
        lines = text_to_lines(text, font, 800)
        for line in lines:
            _, _, line_w, line_h = font.getbbox(line)
            draw.text((pin_w//2 - line_w//2, y_cur), line, text_color, font=font)
            y_cur += font_size
        y_cur += 0
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
    # img_0000 = media.resize(img_0000, int(pin_w*1), int(pin_w*1))
    # img_0001 = media.resize(img_0001, int(pin_w*1), int(pin_w*1))
    # img.paste(img_0000, (0, 0))
    # img.paste(img_0001, (0, int(pin_h*0.66) + gap))
    img.paste(img_0000, (0, 0))
    img.paste(img_0001, (0, int(pin_h*0.66)))
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

def template_ailments_new(data, images_file_paths, export_file_name, template):
    random_theme = random.randint(0, 1)
    if random_theme == 0:
        text_color = '#ffffff'
        bg_color = '#000000'    
    else:
        text_color = '#000000'    
        bg_color = '#ffffff'
    pin_w = 1000
    pin_h = 1500
    img = Image.new(mode="RGB", size=(pin_w, pin_h), color='#ffffff')
    draw = ImageDraw.Draw(img)
    gap = 4
    rect_h = 500
    if template == 1:
        img_0000 = Image.open(images_file_paths[0])
        img_0001 = Image.open(images_file_paths[1])
        img.paste(img_0000, (int(0.0), int(pin_h*0.0)))
        img.paste(img_0001, (int(0.0), int(pin_h*0.66)))
    if template == 2:
        img_0000 = Image.open(images_file_paths[0])
        img_0001 = Image.open(images_file_paths[1])
        img_0002 = Image.open(images_file_paths[2])
        img.paste(img_0000, (int(0.0), int(pin_h*0.0)))
        img.paste(img_0001, (int(0.0), int(pin_h*0.66)))
        img.paste(img_0002, (int(pin_w*0.5) + gap, int(pin_h*0.66) + gap))
        draw.rectangle(((pin_w//2-gap, int(pin_h*0.5)), (pin_w//2+gap, pin_h)), fill=bg_color)
    if template == 3:
        img_0000 = Image.open(images_file_paths[0])
        img_0001 = Image.open(images_file_paths[1])
        img_0002 = Image.open(images_file_paths[2])
        img.paste(img_0000, (int(0.0), int(pin_h*0.0)))
        img.paste(img_0001, (int(pin_w*0.5), int(pin_h*0.0)))
        img.paste(img_0002, (int(0.0), int(pin_h*0.66) + gap))
        draw.rectangle(((pin_w//2-gap, int(pin_h*0.0)), (pin_w//2+gap, int(pin_h*0.5))), fill=bg_color)
    if template == 4:
        img_0000 = Image.open(images_file_paths[0])
        img_0001 = Image.open(images_file_paths[1])
        img_0002 = Image.open(images_file_paths[2])
        img_0003 = Image.open(images_file_paths[3])
        img.paste(img_0000, (int(0.0), int(pin_h*0.0)))
        img.paste(img_0001, (int(pin_w*0.5), int(pin_h*0.0)))
        img.paste(img_0002, (int(0.0), int(pin_h*0.66)))
        img.paste(img_0003, (int(pin_w*0.5), int(pin_h*0.66)))
        draw.rectangle(((pin_w//2-gap, 0), (pin_w//2+gap, pin_h)), fill=bg_color)
    # img_0000 = Image.open(images_file_paths[0])
    # img_0001 = Image.open(images_file_paths[1])
    # img_0000 = media.resize(img_0000, int(pin_w*1), int(pin_w*1))
    # img_0001 = media.resize(img_0001, int(pin_w*1), int(pin_w*1))
    # img.paste(img_0000, (0, 0))
    # img.paste(img_0001, (0, int(pin_h*0.66) + gap))
    # img.paste(img_0000, (0, 0))
    # img.paste(img_0001, (0, int(pin_h*0.66)))
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

def gen_image(images, i, preparation_name_plural, width, height):
    herb_list = data.herbs_primary_medicinal_get()
    herbs_names_scientific = [x['herb_name_scientific'] for x in herb_list]
    herb_name_scientific = random.choice(herbs_names_scientific).strip()
    ###
    if preparation_name_plural == 'teas':
        prompt = f'''
            a ceramic cup of {herb_name_scientific} tea on a wooden table surrounded by dry herbs,
            rustic, vintage, boho
        '''.replace('  ', ' ')
    elif preparation_name_plural == 'tinctures':
        prompt = f'''
            a dark amber glass dropper bottle of {herb_name_scientific} tincture on a wooden table surrounded by dry herbs,
            rustic, vintage, boho,
        '''
    elif preparation_name_plural == 'essential oils':
        prompt = f'''
            an amber glass bottle with black cap of {herb_name_scientific} essential oil on a wooden table surrounded by dry herbs,
            rustic, vintage, boho,
        '''
    elif preparation_name_plural == 'creams':
        prompt = f'''
            a glass jar of {herb_name_scientific} cream on a wooden table surrounded by dry herbs,
            rustic, vintage, boho,
        '''
    else:
        prompt = f'''
            cat
        '''.replace('  ', ' ')
    output_filepath = f'{g.pinterest_tmp_image_folderpath}/tmp/img-{i}.jpg'
    image = zimage.image_create(output_filepath, prompt, width=1024, height=512, seed=-1)
    images.append(output_filepath)
    # quit()

def ai_img_herb_new(template, herb_name_scientific):
    for filename in os.listdir(f'{g.pinterest_tmp_image_folderpath}/tmp'):
        os.remove(f'{g.pinterest_tmp_image_folderpath}/tmp/{filename}')
    # prompt_table = random.choice(['wooden table', 'dark table'])
    prompt_table = random.choice(prompts_tables)
    prompt = f'''
        dry {herb_name_scientific} herb on a {prompt_table} surrounded by medicinal herbs,
        rustic, vintage, boho,
    '''.replace('  ', ' ')
    square_w = 512
    square_h = 512
    landscape_w = 1024
    landscape_h = 512
    if template == 1:
        i = 0
        width = landscape_w
        height = landscape_h
        for _ in range(2):
            print(prompt)
            output_filepath = f'{g.pinterest_tmp_image_folderpath}/tmp/img-{i}.jpg'
            image = zimage.image_create(output_filepath, prompt, width=width, height=height, seed=-1)
            i += 1
    if template == 2:
        i = 0
        width = landscape_w
        height = landscape_h
        for _ in range(1):
            print(prompt)
            output_filepath = f'{g.pinterest_tmp_image_folderpath}/tmp/img-{i}.jpg'
            image = zimage.image_create(output_filepath, prompt, width=width, height=height, seed=-1)
            i += 1
        width = square_w
        height = square_h
        for _ in range(2):
            print(prompt)
            output_filepath = f'{g.pinterest_tmp_image_folderpath}/tmp/img-{i}.jpg'
            image = zimage.image_create(output_filepath, prompt, width=width, height=height, seed=-1)
            i += 1
    if template == 3:
        i = 0
        width = square_w
        height = square_h
        for _ in range(2):
            print(prompt)
            output_filepath = f'{g.pinterest_tmp_image_folderpath}/tmp/img-{i}.jpg'
            image = zimage.image_create(output_filepath, prompt, width=width, height=height, seed=-1)
            i += 1
        width = landscape_w
        height = landscape_h
        for _ in range(1):
            print(prompt)
            output_filepath = f'{g.pinterest_tmp_image_folderpath}/tmp/img-{i}.jpg'
            image = zimage.image_create(output_filepath, prompt, width=width, height=height, seed=-1)
            i += 1
    if template == 4:
        i = 0
        width = square_w
        height = square_h
        for _ in range(4):
            print(prompt)
            output_filepath = f'{g.pinterest_tmp_image_folderpath}/tmp/img-{i}.jpg'
            image = zimage.image_create(output_filepath, prompt, width=width, height=height, seed=-1)
            i += 1


def ai_img_preparation_new(template, preparation_name_plural):
    for filename in os.listdir(f'{g.pinterest_tmp_image_folderpath}/tmp'):
        os.remove(f'{g.pinterest_tmp_image_folderpath}/tmp/{filename}')
    herb_list = data.herbs_primary_medicinal_get()
    herbs_names_scientific = [x['herb_name_scientific'] for x in herb_list]
    herb_name_scientific = random.choice(herbs_names_scientific).strip()
    prompt_table = random.choice(prompts_tables)
    # prompt_table = prompts_tables[0]
    if preparation_name_plural == 'teas':
        prompts_cups = ['ceramic cup', 'glass cup']
        prompt_cup = random.choice(prompts_cups)
        prompt = f'''
            a {prompt_cup} of {herb_name_scientific} tea on a {prompt_table} surrounded by dry herbs,
            rustic, vintage, boho
        '''.replace('  ', ' ')
    elif preparation_name_plural == 'tinctures':
        prompt = f'''
            a dark amber glass dropper bottle of {herb_name_scientific} tincture on a {prompt_table} surrounded by dry herbs,
            rustic, vintage, boho,
        '''
    elif preparation_name_plural == 'essential oils':
        prompt = f'''
            an amber glass bottle with black cap of {herb_name_scientific} essential oil on a {prompt_table} surrounded by dry herbs,
            rustic, vintage, boho,
        '''
    elif preparation_name_plural == 'creams':
        prompt = f'''
            a glass jar of {herb_name_scientific} cream on a {prompt_table} surrounded by dry herbs,
            rustic, vintage, boho,
        '''
    else:
        prompt = f'''
            cat
        '''.replace('  ', ' ')
    square_w = 512
    square_h = 512
    landscape_w = 1024
    landscape_h = 512
    if template == 1:
        i = 0
        width = landscape_w
        height = landscape_h
        for _ in range(2):
            print(prompt)
            output_filepath = f'{g.pinterest_tmp_image_folderpath}/tmp/img-{i}.jpg'
            image = zimage.image_create(output_filepath, prompt, width=width, height=height, seed=-1)
            i += 1
    if template == 2:
        i = 0
        width = landscape_w
        height = landscape_h
        for _ in range(1):
            print(prompt)
            output_filepath = f'{g.pinterest_tmp_image_folderpath}/tmp/img-{i}.jpg'
            image = zimage.image_create(output_filepath, prompt, width=width, height=height, seed=-1)
            i += 1
        width = square_w
        height = square_h
        for _ in range(2):
            print(prompt)
            output_filepath = f'{g.pinterest_tmp_image_folderpath}/tmp/img-{i}.jpg'
            image = zimage.image_create(output_filepath, prompt, width=width, height=height, seed=-1)
            i += 1
    if template == 3:
        i = 0
        width = square_w
        height = square_h
        for _ in range(2):
            print(prompt)
            output_filepath = f'{g.pinterest_tmp_image_folderpath}/tmp/img-{i}.jpg'
            image = zimage.image_create(output_filepath, prompt, width=width, height=height, seed=-1)
            i += 1
        width = landscape_w
        height = landscape_h
        for _ in range(1):
            print(prompt)
            output_filepath = f'{g.pinterest_tmp_image_folderpath}/tmp/img-{i}.jpg'
            image = zimage.image_create(output_filepath, prompt, width=width, height=height, seed=-1)
            i += 1
    if template == 4:
        i = 0
        width = square_w
        height = square_h
        for _ in range(4):
            print(prompt)
            output_filepath = f'{g.pinterest_tmp_image_folderpath}/tmp/img-{i}.jpg'
            image = zimage.image_create(output_filepath, prompt, width=width, height=height, seed=-1)
            i += 1

# jump
def pin_herb(article_filepath, article_i):
    json_article = io.json_read(article_filepath)
    ###
    title = json_article['title']
    herb_slug = json_article['herb_slug']
    herb_name_scientific = json_article['herb_name_scientific']
    json_herb_filepath = f'{g.DATABASE_FOLDERPATH}/entities/herbs/{herb_slug}.json'
    json_herb_data = io.json_read(json_herb_filepath)
    herb_name_common = json_herb_data['herb_name_common'][0]['answer']
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
    ### TEMPLATE
    template = random.randint(1, 4)
    ### TMP IMAGES
    ai_img_herb_new(template, herb_name_scientific)
    tmp_images_folderpath = f'{g.pinterest_tmp_image_folderpath}/tmp'
    images_filepaths = sorted([f'{tmp_images_folderpath}/{filename}' for filename in os.listdir(tmp_images_folderpath)])
    ### PIN IMAGE
    img_filepath = template_herbs_new(data, images_filepaths, filename_out, herb_name_common, template)
    ### PIN JSON
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
    # quit()
    pass

def pin_gen_ailment(article_filepath, article_i, preparation_slug):
    preparation_name_plural = preparation_slug.replace('-', ' ')
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
    board_name = f'herbal {preparation_name_plural}'.title()
    ### TEMPLATE
    template = random.randint(1, 4)
    # template = 2
    ### TMP IMAGES
    ai_img_preparation_new(template, preparation_name_plural)
    tmp_images_folderpath = f'{g.pinterest_tmp_image_folderpath}/tmp'
    images_filepaths = sorted([f'{tmp_images_folderpath}/{filename}' for filename in os.listdir(tmp_images_folderpath)])
    print(f'template: {template}')
    ### gen pins
    img_filepath = template_ailments_new(data, images_filepaths, filename_out, template)
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

# jump
def json_pin_herb_gen(article_filepath, article_i):
    json_article = io.json_read(article_filepath)
    ###
    title = json_article['title']
    herb_slug = json_article['herb_slug']
    herb_name_scientific = json_article['herb_name_scientific']
    json_herb_filepath = f'{g.DATABASE_FOLDERPATH}/entities/herbs/{herb_slug}.json'
    json_herb_data = io.json_read(json_herb_filepath)
    herb_name_common = json_herb_data['herb_name_common'][0]['answer']
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
    img_filepath = f'{g.pinterest_tmp_image_folderpath}/images/{filename_out}.jpg'
    ###
    prompt = f'''
        I'm interested in this topic:
        {title}
        Please come up with a numbered list of 15 clickbait youtube titles all about this topic. 
        Make each one slightly different, get as micro as you'd like. 
        Make each title as similar with the topic as possible.
        Each title must be less than 10 words.
        Reply only with the titles.
    '''
    prompt += f'/no_think'
    print(prompt)
    reply = llm.reply(prompt)
    if '</think>' in reply:
        reply = reply.split('</think>')[1].strip()
    lines = []
    for line in reply.split('\n'):
        line = line.strip()
        if line == '': continue
        # if ':' in line: continue
        line = line.replace('"', '')
        line = line.replace('*', '')
        if not line[0].isdigit(): continue
        if '. ' not in line: continue
        line = '. '.join(line.split('. ')[1:])
        if line[-1] == '.': line = line[:-1]
        line = line.strip()
        lines.append(line)
    print(lines)
    title = random.choice(lines)
    print('################################################################################')
    print(line)
    print('################################################################################')
    ### PIN JSON
    url = f'http://terrawhisper.com/{url}.html'
    obj = {
        'img_filepath': img_filepath,
        'type': 'herb',
        'title': title,
        'herb_slug': herb_slug,
        'herb_name_scientific': herb_name_scientific,
        'description': description,
        'url': url,
        'board_name': board_name
    }
    io.json_write(f'{g.pinterest_tmp_image_folderpath}/pins/{article_i}.json', obj)
    pass

def image_pin_ailment_gen(article_filepath, article_i, preparation_slug):
    preparation_name_plural = preparation_slug.replace('-', ' ')
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
    ### TEMPLATE
    template = random.randint(1, 4)
    # template = 2
    ### TMP IMAGES
    ai_img_preparation_new(template, preparation_name_plural)
    tmp_images_folderpath = f'{g.pinterest_tmp_image_folderpath}/tmp'
    images_filepaths = sorted([f'{tmp_images_folderpath}/{filename}' for filename in os.listdir(tmp_images_folderpath)])
    print(f'template: {template}')
    ### gen pins
    img_filepath = template_ailments_new(data, images_filepaths, filename_out, template)

def json_pin_ailment_gen(article_filepath, article_i, preparation_slug):
    preparation_name_plural = preparation_slug.replace('-', ' ')
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
    board_name = f'herbal {preparation_name_plural}'.title()
    img_filepath = f'{g.pinterest_tmp_image_folderpath}/images/{filename_out}.jpg'
    ### TITLE GEN
    prompt = f'''
        I'm interested in this topic:
        {title}
        Please come up with a numbered list of 15 clickbait youtube titles all about this topic. 
        Make each one slightly different, get as micro as you'd like. 
        Make each title as similar with the topic as possible.
        Each title must be less than 10 words.
        Reply only with the titles.
    '''
        # Include the ailment name and the number in each title.
        # Never use the following characters: colon, asterisk, double quotes.
    prompt += f'/no_think'
    print(prompt)
    reply = llm.reply(prompt)
    if '</think>' in reply:
        reply = reply.split('</think>')[1].strip()
    lines = []
    for line in reply.split('\n'):
        line = line.strip()
        if line == '': continue
        if ':' in line: continue
        line = line.replace('"', '')
        line = line.replace('*', '')
        if not line[0].isdigit(): continue
        if '. ' not in line: continue
        line = '. '.join(line.split('. ')[1:])
        if line[-1] == '.': line = line[:-1]
        line = line.strip()
        lines.append(line)
    print(lines)
    title = random.choice(lines)
    print('################################################################################')
    print(line)
    print('################################################################################')
    ###
    output_filepath = f'{g.pinterest_tmp_image_folderpath}/tmp/img-{i}.jpg'
    url = f'http://terrawhisper.com/{url}.html'
    obj = {
        'img_filepath': img_filepath,
        'type': 'ailment',
        'title': title,
        'status_name': status_name,
        'preparation_slug': preparation_slug,
        'description': description,
        'url': url,
        'board_name': board_name
    }
    io.json_write(f'{g.pinterest_tmp_image_folderpath}/pins/{article_i}.json', obj)

def image_pin_ailment_gen(article_filepath, article_i, preparation_slug):
    preparation_name_plural = preparation_slug.replace('-', ' ')
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
    ### TEMPLATE
    template = random.randint(1, 4)
    # template = 2
    ### TMP IMAGES
    ai_img_preparation_new(template, preparation_name_plural)
    tmp_images_folderpath = f'{g.pinterest_tmp_image_folderpath}/tmp'
    images_filepaths = sorted([f'{tmp_images_folderpath}/{filename}' for filename in os.listdir(tmp_images_folderpath)])
    print(f'template: {template}')
    ### gen pins
    img_filepath = template_ailments_new(data, images_filepaths, filename_out, template)

if 0:
    for filename in os.listdir(f'{g.pinterest_tmp_image_folderpath}/images'):
        os.remove(f'{g.pinterest_tmp_image_folderpath}/images/{filename}')
if 1:
    for filename in os.listdir(f'{g.pinterest_tmp_image_folderpath}/pins'):
        os.remove(f'{g.pinterest_tmp_image_folderpath}/pins/{filename}')

i = 0

########################################
### PIN JSON 
########################################
if 1:
    for article_filepath in herbs_articles_filepath:
        print(f'{i}/{len(articles_filepath)} >> {article_filepath}')
        json_pin_herb_gen(article_filepath, i)
        i += 1

if 1:
    for article_filepath in teas_articles_filepath:
        print(f'{i}/{len(articles_filepath)} >> {article_filepath}')
        json_pin_ailment_gen(article_filepath, i, 'teas')
        i += 1
    for article_filepath in tinctures_articles_filepath:
        print(f'{i}/{len(articles_filepath)} >> {article_filepath}')
        json_pin_ailment_gen(article_filepath, i, 'tinctures')
        i += 1
    for article_filepath in decoctions_articles_filepath:
        print(f'{i}/{len(articles_filepath)} >> {article_filepath}')
        json_pin_ailment_gen(article_filepath, i, 'decoctions')
        i += 1
    for article_filepath in essential_oils_articles_filepath:
        print(f'{i}/{len(articles_filepath)} >> {article_filepath}')
        json_pin_ailment_gen(article_filepath, i, 'essential-oils')
        i += 1
    for article_filepath in creams_articles_filepath:
        print(f'{i}/{len(articles_filepath)} >> {article_filepath}')
        json_pin_ailment_gen(article_filepath, i, 'creams')
        i += 1
    for article_filepath in juices_articles_filepath:
        print(f'{i}/{len(articles_filepath)} >> {article_filepath}')
        json_pin_ailment_gen(article_filepath, i, 'juices')
        i += 1
    for article_filepath in syrups_articles_filepath:
        print(f'{i}/{len(articles_filepath)} >> {article_filepath}')
        json_pin_ailment_gen(article_filepath, i, 'syrups')
        i += 1
    for article_filepath in linctuses_articles_filepath:
        print(f'{i}/{len(articles_filepath)} >> {article_filepath}')
        json_pin_ailment_gen(article_filepath, i, 'linctuses')
        i += 1
    for article_filepath in baths_articles_filepath:
        print(f'{i}/{len(articles_filepath)} >> {article_filepath}')
        json_pin_ailment_gen(article_filepath, i, 'baths')
        i += 1
    for article_filepath in capsules_articles_filepath:
        print(f'{i}/{len(articles_filepath)} >> {article_filepath}')
        json_pin_ailment_gen(article_filepath, i, 'capsules')
        i += 1

