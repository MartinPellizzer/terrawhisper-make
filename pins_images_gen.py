import os
import random

from PIL import Image, ImageFont, ImageDraw, ImageColor, ImageOps

from lib import g
from lib import io
from lib import data
from lib import media
from lib import zimage

prompts_tables = ['table', 'wooden table', 'oak table', 'mapple table', 'walnut table', 'marble table', 'granite table', 'dark table']

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

def ai_img_herb_new(template, herb_name_scientific):
    for filename in os.listdir(f'{g.pinterest_tmp_image_folderpath}/tmp'):
        os.remove(f'{g.pinterest_tmp_image_folderpath}/tmp/{filename}')
    ###
    prompt_table = random.choice(prompts_tables)
    # prompt_table = prompts_tables[0]
    prompt = f'''
        dry {herb_name_scientific} herb on a {prompt_table} surrounded by medicinal herbs,
        rustic, vintage, boho,
    '''.replace('  ', ' ')
    pin_w = 1000
    pin_h = 1500
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
    if template == 5:
        i = 0
        width = 1024//2
        height = 1536//2
        for _ in range(1):
            print(prompt)
            output_filepath = f'{g.pinterest_tmp_image_folderpath}/tmp/img-{i}.jpg'
            image = zimage.image_create(output_filepath, prompt, width=width, height=height, seed=-1)
            image = media.resize(image, int(width*2), int(height*2))
            # image = image.resize((1024, 1536), Image.LANCZOS)
            image.save(output_filepath, format='JPEG', subsampling=0, quality=100)
            i += 1

def ai_img_preparation_new(template, preparation_name_plural):
    for filename in os.listdir(f'{g.pinterest_tmp_image_folderpath}/tmp'):
        os.remove(f'{g.pinterest_tmp_image_folderpath}/tmp/{filename}')
    ###
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
    elif preparation_name_plural == 'juices':
        prompt = f'''
            a glass bottle of {herb_name_scientific} juice on a {prompt_table} surrounded by dry herbs,
            rustic, vintage, boho,
        '''
    elif preparation_name_plural == 'syrups':
        prompt = f'''
            a glass bottle of {herb_name_scientific} syrup on a {prompt_table} surrounded by dry herbs,
            rustic, vintage, boho,
        '''
    else:
        prompt = f'''
            cat
        '''.replace('  ', ' ')
    pin_w = 1000
    pin_h = 1500
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
    if template == 5:
        i = 0
        width = 1024//2
        height = 1536//2
        for _ in range(1):
            print(prompt)
            output_filepath = f'{g.pinterest_tmp_image_folderpath}/tmp/img-{i}.jpg'
            image = zimage.image_create(output_filepath, prompt, width=width, height=height, seed=-1)
            image = media.resize(image, int(width*2), int(height*2))
            # image = image.resize((1024, 1536), Image.LANCZOS)
            image.save(output_filepath, format='JPEG', subsampling=0, quality=100)
            i += 1

def template_herb_new(data, images_file_paths, img_filepath, template):
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
    if template == 5:
        img_0000 = Image.open(images_file_paths[0])
        img.paste(img_0000, (int(0.0), int(pin_h*0.0)))
    # rect
    if template != 5:
        draw.rectangle(((0, pin_h//2 - rect_h//2), (pin_w, pin_h//2 + rect_h//2)), fill=bg_color)
        # text_template = random.choice([0, 1])
        if 0:
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
            text = f'''best herbal {preparation_name_plural}'''.upper()
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
            try: ailment_name = data['ailment_name'] 
            except: ailment_name = data['status_name']
            text = f'''for {ailment_name}'''.title()
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
        ###
        else:
            y_cur = 500
            font_size = 96
            for _ in range(10):
                text = f'''{data['title']}'''.upper()
                font_family, font_weight = 'Lato', 'Bold'
                font_path = f"{g.ASSETS_FOLDERPATH}/fonts/{font_family}/{font_family}-{font_weight}.ttf"
                font = ImageFont.truetype(font_path, font_size)
                _, _, text_w, text_h = font.getbbox(text)
                lines = text_to_lines(text, font, 900)
                if len(lines) < 5: break
                font_size -= 4    
            line_i = 0
            for line in lines:
                _, _, line_w, line_h = font.getbbox(line)
                draw.text(
                    (pin_w//2 - line_w//2, pin_h//2 - (len(lines)*font_size)//2 + line_i*font_size), 
                    line, text_color, font=font,
                )
                line_i += 1
    else:
        pass
    img.save(img_filepath, format='JPEG', subsampling=0, quality=100)
    return img_filepath

def template_ailments_new(data, images_file_paths, img_filepath, template, preparation_name_plural):
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
    if template == 5:
        img_0000 = Image.open(images_file_paths[0])
        img.paste(img_0000, (int(0.0), int(pin_h*0.0)))
    ###
    if template != 5:
        draw.rectangle(((0, pin_h//2 - rect_h//2), (pin_w, pin_h//2 + rect_h//2)), fill=bg_color)
        if 0:
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
            text = f'''best herbal {preparation_name_plural}'''.upper()
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
            try: ailment_name = data['ailment_name'] 
            except: ailment_name = data['status_name']
            text = f'''for {ailment_name}'''.title()
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
        ###
        else:
            y_cur = 500
            font_size = 96
            for _ in range(10):
                text = f'''{data['title']}'''.upper()
                font_family, font_weight = 'Lato', 'Bold'
                font_path = f"{g.ASSETS_FOLDERPATH}/fonts/{font_family}/{font_family}-{font_weight}.ttf"
                font = ImageFont.truetype(font_path, font_size)
                _, _, text_w, text_h = font.getbbox(text)
                lines = text_to_lines(text, font, 900)
                if len(lines) < 5: break
                font_size -= 4    
            line_i = 0
            for line in lines:
                _, _, line_w, line_h = font.getbbox(line)
                draw.text(
                    (pin_w//2 - line_w//2, pin_h//2 - (len(lines)*font_size)//2 + line_i*font_size), 
                    line, text_color, font=font,
                )
                line_i += 1
    else:
        pass
    img.save(img_filepath, format='JPEG', subsampling=0, quality=100)
    return img_filepath

def pins_images_gen():
    jsons_folderpath = f'{g.pinterest_tmp_image_folderpath}/pins'
    jsons_filepaths = [f'{jsons_folderpath}/{filename}' for filename in os.listdir(jsons_folderpath)]
    for json_filepath in jsons_filepaths:
        print(json_filepath)
        data = io.json_read(json_filepath)
        img_filepath = data['img_filepath']
        pin_type = data['type']
        # print(data)
        # quit()
        ###
        template = random.randint(1, 5)
        # template = 5
        if pin_type == 'herb':
            herb_name_scientific = data['herb_name_scientific']
            ai_img_herb_new(template, herb_name_scientific)
            # return
            ###
            tmp_images_folderpath = f'{g.pinterest_tmp_image_folderpath}/tmp'
            images_filepaths = sorted(
                [f'{tmp_images_folderpath}/{filename}' for filename in os.listdir(tmp_images_folderpath)]
            )
            ### gen pins
            img_filepath = template_herb_new(data, images_filepaths, img_filepath, template)
            # break
        else:
            preparation_slug = data['preparation_slug']
            preparation_name_plural = preparation_slug.replace('-', ' ')
            ai_img_preparation_new(template, preparation_name_plural)
            ###
            tmp_images_folderpath = f'{g.pinterest_tmp_image_folderpath}/tmp'
            images_filepaths = sorted(
                [f'{tmp_images_folderpath}/{filename}' for filename in os.listdir(tmp_images_folderpath)]
            )
            ### gen pins
            img_filepath = template_ailments_new(data, images_filepaths, img_filepath, template, preparation_name_plural)
            # break

for filename in os.listdir(f'{g.pinterest_tmp_image_folderpath}/images'):
    os.remove(f'{g.pinterest_tmp_image_folderpath}/images/{filename}')

pins_images_gen()

