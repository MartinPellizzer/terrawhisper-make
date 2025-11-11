import os
import json
import shutil

from PIL import Image, ImageFont, ImageDraw, ImageColor, ImageOps

from lib import g
from lib import io
from lib import media

from infoproduct import checklist_vanilla

def file_parse(filepath):
    with open(filepath) as f: dump = f.read().strip()

    content = dump.split('---')[0]
    print(content)

    title = ''
    subtitle = ''
    categories = []
    category = []
    for line in content.split('\n'):
        line = line.strip()
        if line == '': continue
        elif line.startswith('# '):
            title = line.replace('# ', '')
        elif line.startswith('## '):
            subtitle = line.replace('## ', '')
        elif line.startswith('### '):
            if category != []: categories.append(category)
            category = {
                'heading': line.replace('### ', ''),
                'items': [],
            }
        elif line.startswith('* '):
            line = line.replace('* ', '')
            category['items'].append([line])
        elif line.startswith('[] '):
            line = line.replace('[] ', '')
            category['items'].append([line])
        elif line.startswith('- '):
            line = line.replace('- ', '')
            category['items'].append([line])
        else:
            category['items'].append([line])
    if category != []: categories.append(category)
    file_data = {
        'title': title,
        'subtitle': subtitle,
        'categories': categories,
    }
    return file_data

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

def text_to_paragraphs(text, font, max_w):
    paragraphs = []
    for paragraph in text.split('//'):
        lines = []
        line = ''
        for word in paragraph.split():
            _, _, word_w, word_h = font.getbbox(word)
            _, _, line_w, line_h = font.getbbox(line.strip())
            if  line_w + word_w < max_w:
                line += f'{word} '
            else:
                lines.append(line.strip())
                line = f'{word} '
        if line.strip() != '':
            lines.append(line.strip())
        paragraphs.append(lines)
    return paragraphs

def draw_cell(draw, text, font_size, font_weight, cell_x, cell_y, cell_w, gap_x, color, border_width=1, checkbox=False, px=48, py=32):
    font_family, font_weight = 'Lato', font_weight 
    font_path = f"{g.ASSETS_FOLDERPATH}/fonts/{font_family}/{font_family}-{font_weight}.ttf"
    font = ImageFont.truetype(font_path, font_size)
    ### CHECKBOX
    checkbox_size = 0
    checkbox_gap = 0
    if checkbox:
        checkbox_size = 64
        checkbox_gap = gap_x
        checkbox_x1 = cell_x + px
        checkbox_y1 = cell_y + py
        checkbox_x2 = cell_x + px + checkbox_size
        checkbox_y2 = cell_y + py + checkbox_size
        draw.rectangle([(checkbox_x1, checkbox_y1), (checkbox_x2, checkbox_y2)], outline=color, width=1)
    ### LINES
    # lines = text_to_lines(text, font, cell_w - px - checkbox_size - gap_x)
    # paragraphs = text_to_paragraphs(text, font, cell_w - px - checkbox_size - gap_x)
    paragraphs = text_to_paragraphs(text, font, cell_w - px - checkbox_size - checkbox_gap)
    line_height = 1.5
    y = cell_y + py
    for lines in paragraphs:
        for line_i, line in enumerate(lines):
            ### TODO: instead of fix color for [i] make it base color + alpha to make it lighter
            color_cur = color
            if '|' not in line:
                if line.startswith('[b]'):
                    line = line.replace('[b]', '')
                    font_family, font_weight = 'Lato', 'Bold' 
                    font_path = f"{g.ASSETS_FOLDERPATH}/fonts/{font_family}/{font_family}-{font_weight}.ttf"
                    font = ImageFont.truetype(font_path, font_size)
                elif line.startswith('[i]'):
                    line = line.replace('[i]', '')
                    font_family, font_weight = 'Lato', 'Italic' 
                    font_path = f"{g.ASSETS_FOLDERPATH}/fonts/{font_family}/{font_family}-{font_weight}.ttf"
                    font = ImageFont.truetype(font_path, font_size)
                    # color_cur = '#303633'
                else:
                    font_family, font_weight = 'Lato', 'Regular' 
                    font_path = f"{g.ASSETS_FOLDERPATH}/fonts/{font_family}/{font_family}-{font_weight}.ttf"
                    font = ImageFont.truetype(font_path, font_size)
                _, _, line_w, line_h = font.getbbox(line)
                x = cell_x + px
                if checkbox: x += checkbox_size + px
                draw.text((x, y), line, color_cur, font=font)
                y += (font_size*line_height)
            else:
                chunks = line.split('|')
                line = chunks[0].strip()
                if line.startswith('[b]'):
                    line = line.replace('[b]', '')
                    font_family, font_weight = 'Lato', 'Bold' 
                    font_path = f"{g.ASSETS_FOLDERPATH}/fonts/{font_family}/{font_family}-{font_weight}.ttf"
                    font = ImageFont.truetype(font_path, font_size)
                elif line.startswith('[i]'):
                    line = line.replace('[i]', '')
                    font_family, font_weight = 'Lato', 'Italic' 
                    font_path = f"{g.ASSETS_FOLDERPATH}/fonts/{font_family}/{font_family}-{font_weight}.ttf"
                    font = ImageFont.truetype(font_path, font_size)
                    # color_cur = '#303633'
                else:
                    font_family, font_weight = 'Lato', 'Regular' 
                    font_path = f"{g.ASSETS_FOLDERPATH}/fonts/{font_family}/{font_family}-{font_weight}.ttf"
                    font = ImageFont.truetype(font_path, font_size)
                _, _, line_w, line_h = font.getbbox(line)
                x = cell_x + px
                if checkbox: x += checkbox_size + px
                draw.text((x, y), line, color_cur, font=font)
                ###
                line = chunks[1].strip()
                if line.startswith('[b]'):
                    line = line.replace('[b]', '')
                    font_family, font_weight = 'Lato', 'Bold' 
                    font_path = f"{g.ASSETS_FOLDERPATH}/fonts/{font_family}/{font_family}-{font_weight}.ttf"
                    font = ImageFont.truetype(font_path, font_size)
                elif line.startswith('[i]'):
                    line = line.replace('[i]', '')
                    font_family, font_weight = 'Lato', 'Italic' 
                    font_path = f"{g.ASSETS_FOLDERPATH}/fonts/{font_family}/{font_family}-{font_weight}.ttf"
                    font = ImageFont.truetype(font_path, font_size)
                    # color_cur = '#303633'
                else:
                    font_family, font_weight = 'Lato', 'Regular' 
                    font_path = f"{g.ASSETS_FOLDERPATH}/fonts/{font_family}/{font_family}-{font_weight}.ttf"
                    font = ImageFont.truetype(font_path, font_size)
                _, _, line_w, line_h = font.getbbox(line)
                x = cell_x + cell_w - line_w - px
                draw.text((x, y), line, color_cur, font=font)
                y += (font_size*line_height)
    y += py//2
    ### RECT
    rect_x1 = cell_x
    rect_y1 = cell_y
    rect_x2 = cell_x + cell_w
    # rect_y2 = cell_y + (font_size*len(lines)*line_height) + py*2
    rect_y2 = y
    rect_y2_min = rect_y1 + checkbox_size + py*2
    if rect_y2 < rect_y2_min: rect_y2 = rect_y2_min
    draw.rectangle([(rect_x1, rect_y1), (rect_x2, rect_y2)], outline=color, width=border_width)
    return rect_y2

def checklist_vanilla_create(data):
    product_type_slug = data['product_type'].strip().lower().replace(' ', '-')
    base_folderpath = f'{g.DATABASE_FOLDERPATH}/shop/one-page/{product_type_slug}'
    input_filepath = f'''{base_folderpath}/{data['slug']}/{data['input_filename']}'''
    with open(input_filepath) as f: dump = f.read().strip()
    content = dump.split('---')[0]
    print(content)
    title = ''
    subtitle = ''
    categories = []
    category = []
    file_data = file_parse(input_filepath)
    title = file_data['title']
    subtitle = file_data['subtitle']
    categories = file_data['categories']
    print(title)
    print(subtitle)
    print(categories)
    ################################################################################
    # IMAGE GENERATE
    ################################################################################
    color_whisper_white = '#f7f6f2'
    color_carbon_powder = '#101211'
    img_w = 2480
    img_h = 3508
    gap_x = int((img_w / 100) * 5)
    gap_y = int((img_h / 100) * 5)
    img = Image.new(mode="RGBA", size=(img_w, img_h), color=color_whisper_white)
    ### OUTLINE
    draw = ImageDraw.Draw(img)
    draw.rectangle([(gap_x, gap_y), (img_w - gap_x, img_h - gap_y)], outline=color_carbon_powder, width=3)
    y_cur = 0
    cols_num = 1
    cols_gap = 48
    print_area_x = gap_x*2
    print_area_y = gap_y*2
    print_area_w = img_w - gap_x*4
    col_w = (print_area_w - cols_gap * (cols_num-1)) / cols_num
    ### TITLE
    text = title
    font_size = 256
    font_family, font_weight = 'Lato', 'Bold'
    font_path = f"{g.ASSETS_FOLDERPATH}/fonts/{font_family}/{font_family}-{font_weight}.ttf"
    font = ImageFont.truetype(font_path, font_size)
    lines = text_to_lines(text, font, img_w - gap_x*2)
    y_cur += gap_y * 1.5
    line_height = 1.0
    for line in lines:
        _, _, line_w, line_h = font.getbbox(line)
        draw.text((img_w//2 - line_w//2, y_cur), line, color_carbon_powder, font=font)
        y_cur += font_size * line_height
    ### CATEGORY
    y_cur += gap_y
    x_cur = gap_x * 2
    col_i = 0
    for category in categories:
        text = category['heading'].upper()
        cell_width = img_w//2 - gap_x*2 - gap_x//2
        cell_width = img_w - gap_x*4
        rect_y2 = draw_cell(
            draw, text, 48, 'Bold', 
            x_cur + col_w*col_i + cols_gap*col_i, 
            y_cur, 
            col_w, gap_x=gap_x, 
            color=color_carbon_powder, checkbox=False
        )
        y_cur = rect_y2
        ### ITEMS
        for item in category['items']:
            text = item[0]
            rect_y2 = draw_cell(draw, text, 32, 'Regular', x_cur + col_w*col_i + cols_gap*col_i, y_cur, col_w, gap_x=gap_x, color=color_carbon_powder, checkbox=True)
            # rect_y2 = draw_cell(draw, text, 48, 'Regular', x_cur, y_cur, cell_width, checkbox=True)
            y_cur = rect_y2
        # col_i += 1
        y_cur += 64 
    ### GUIDES
    # draw.line([(img_w//2, 0), (img_w//2, img_h)], fill="#FF00FF", width=3)
    ### COPYRIGHT
    text = 'terrawhisper.com'.upper()
    font_size = 32
    font_family, font_weight = 'Lato', 'Bold'
    font_path = f"{g.ASSETS_FOLDERPATH}/fonts/{font_family}/{font_family}-{font_weight}.ttf"
    font = ImageFont.truetype(font_path, font_size)
    lines = text_to_lines(text, font, img_w - gap_x*2)
    line_height = 1.0
    y_cur = img_h - gap_y*2
    for line in lines:
        _, _, line_w, line_h = font.getbbox(line)
        draw.text((img_w//2 - line_w//2, y_cur), line, color_carbon_powder, font=font)
        y_cur += font_size * line_height
    img = img.convert('RGB')
    output_filepath = f'''{base_folderpath}/{data['slug']}/{data['slug']}.jpg'''
    img.save(output_filepath, format='JPEG', subsampling=0, quality=100)
    output_filepath = f'''{base_folderpath}/{data['slug']}/{data['slug']}-preview.jpg'''
    img = media.resize(img, img_w//4, img_h//4)
    img.save(output_filepath, format='JPEG', subsampling=0, quality=70)

def checklist_base_create(data):
    product_type_slug = data['product_type'].strip().lower().replace(' ', '-')
    base_folderpath = f'{g.DATABASE_FOLDERPATH}/shop/one-page/{product_type_slug}'
    input_filepath = f'''{base_folderpath}/{data['slug']}/{data['input_filename']}'''
    with open(input_filepath) as f: dump = f.read().strip()
    content = dump.split('---')[0]
    print(content)
    title = ''
    subtitle = ''
    categories = []
    category = []
    file_data = file_parse(input_filepath)
    title = file_data['title']
    subtitle = file_data['subtitle']
    categories = file_data['categories']
    print(title)
    print(subtitle)
    print(categories)
    ################################################################################
    # IMAGE GENERATE
    ################################################################################
    color_whisper_white = '#f7f6f2'
    color_carbon_powder = '#101211'
    img_w = 2480
    img_h = 3508
    gap_x = int((img_w / 100) * 5)
    gap_y = int((img_h / 100) * 5)
    img = Image.new(mode="RGBA", size=(img_w, img_h), color=color_whisper_white)
    ### OUTLINE
    draw = ImageDraw.Draw(img)
    draw.rectangle([(gap_x, gap_y), (img_w - gap_x, img_h - gap_y)], outline=color_carbon_powder, width=3)
    y_cur = 0
    cols_num = 1
    cols_gap = 48
    print_area_x = gap_x*2
    print_area_y = gap_y*2
    print_area_w = img_w - gap_x*4
    col_w = (print_area_w - cols_gap * (cols_num-1)) / cols_num
    ### TITLE
    text = title
    font_size = 192
    font_family, font_weight = 'Lato', 'Bold'
    font_path = f"{g.ASSETS_FOLDERPATH}/fonts/{font_family}/{font_family}-{font_weight}.ttf"
    font = ImageFont.truetype(font_path, font_size)
    lines = text_to_lines(text, font, img_w - gap_x*4)
    y_cur += gap_y * 1.5
    line_height = 1.0
    for line in lines:
        _, _, line_w, line_h = font.getbbox(line)
        draw.text((img_w//2 - line_w//2, y_cur), line, color_carbon_powder, font=font)
        y_cur += font_size * line_height
    ### CATEGORY
    y_cur += gap_y
    x_cur = gap_x * 2
    col_i = 0
    for category_i, category in enumerate(categories):
        text = f'''{category_i+1}. {category['heading'].upper()}'''
        cell_width = img_w//2 - gap_x*2 - gap_x//2
        cell_width = img_w - gap_x*4
        rect_y2 = draw_cell(draw, text, 48, 'Bold', x_cur + col_w*col_i + cols_gap*col_i, y_cur, col_w, gap_x=gap_x, color=color_carbon_powder, checkbox=False, border_width=0, px=48, py=16)
        y_cur = rect_y2
        ### ITEMS
        for item in category['items']:
            text = item[0]
            rect_y2 = draw_cell(draw, text, 32, 'Regular', x_cur + col_w*col_i + cols_gap*col_i, y_cur, col_w, gap_x=gap_x, color=color_carbon_powder, checkbox=True, border_width=0, px=48, py=16)
            # rect_y2 = draw_cell(draw, text, 48, 'Regular', x_cur, y_cur, cell_width, checkbox=True)
            y_cur = rect_y2
        # col_i += 1
        y_cur += 48 
    ### GUIDES
    # draw.line([(img_w//2, 0), (img_w//2, img_h)], fill="#FF00FF", width=3)
    ### COPYRIGHT
    text = 'terrawhisper.com'.upper()
    font_size = 32
    font_family, font_weight = 'Lato', 'Bold'
    font_path = f"{g.ASSETS_FOLDERPATH}/fonts/{font_family}/{font_family}-{font_weight}.ttf"
    font = ImageFont.truetype(font_path, font_size)
    lines = text_to_lines(text, font, img_w - gap_x*2)
    line_height = 1.0
    y_cur = img_h - int(gap_y*2)
    for line in lines:
        _, _, line_w, line_h = font.getbbox(line)
        draw.text((img_w//2 - line_w//2, y_cur), line, color_carbon_powder, font=font)
        y_cur += font_size * line_height
    img = img.convert('RGB')
    output_filepath = f'''{base_folderpath}/{data['slug']}/{data['slug']}.jpg'''
    img.save(output_filepath, format='JPEG', subsampling=0, quality=100)
    output_filepath = f'''{base_folderpath}/{data['slug']}/{data['slug']}-preview.jpg'''
    img = media.resize(img, img_w//4, img_h//4)
    img.save(output_filepath, format='JPEG', subsampling=0, quality=70)

def checklist_create(data):
    product_type_slug = data['product_type'].strip().lower().replace(' ', '-')
    base_folderpath = f'{g.DATABASE_FOLDERPATH}/shop/one-page/{product_type_slug}'
    input_filepath = f'''{base_folderpath}/{data['input_filename']}'''
    with open(input_filepath) as f: dump = f.read().strip()
    content = dump.split('---')[0]
    print(content)
    title = ''
    subtitle = ''
    categories = []
    category = []
    for line in content.split('\n'):
        line = line.strip()
        if line == '': continue
        if line.startswith('# '):
            title = line.replace('# ', '')
        if line.startswith('## '):
            subtitle = line.replace('## ', '')
        if line.startswith('### '):
            if category != []: categories.append(category)
            category = {
                'heading': line.replace('### ', ''),
                'items': [],
            }
        if line.startswith('* '):
            line = line.replace('* ', '')
            items = line.split('|')
            category['items'].append(items)
        if line.startswith('[] '):
            line = line.replace('[] ', '')
            items = line.split('|')
            category['items'].append(items)
    if category != []: categories.append(category)
    print(title)
    print(subtitle)
    print(categories)
    ################################################################################
    # IMAGE GENERATE
    ################################################################################
    color_whisper_white = '#f7f6f2'
    color_carbon_powder = '#101211'
    img_w = 2480
    img_h = 3508
    gap_x = int((img_w / 100) * 5)
    gap_y = int((img_h / 100) * 5)
    img = Image.new(mode="RGBA", size=(img_w, img_h), color=color_whisper_white)
    ### BACKGROUND OVERLAY
    # overlay = Image.open(f'{g.DATABASE_FOLDERPATH}/shop/checklists/02.jpg').convert('RGBA')
    # overlay = overlay.resize(img.size, Image.Resampling.LANCZOS)
    '''
    alpha = 128
    overlay_with_alpha = overlay.copy()
    overlay_with_alpha.putalpha(alpha)
    img = Image.alpha_composite(img, overlay_with_alpha)
    '''
    # img = Image.blend(img, overlay, alpha=0.2)
    ### OUTLINE
    draw = ImageDraw.Draw(img)
    draw.rectangle([(gap_x, gap_y), (img_w - gap_x, img_h - gap_y)], outline=color_carbon_powder, width=3)
    y_cur = 0
    cols_num = 3
    cols_gap = 48
    print_area_x = gap_x*2
    print_area_y = gap_y*2
    print_area_w = img_w - gap_x*4
    col_w = (print_area_w - cols_gap * (cols_num-1)) / cols_num
    ### TITLE
    text = title
    font_size = 256
    font_family, font_weight = 'Lato', 'Bold'
    font_path = f"{g.ASSETS_FOLDERPATH}/fonts/{font_family}/{font_family}-{font_weight}.ttf"
    font = ImageFont.truetype(font_path, font_size)
    lines = text_to_lines(text, font, img_w - gap_x*2)
    y_cur += gap_y * 1.5
    line_height = 1.0
    for line in lines:
        _, _, line_w, line_h = font.getbbox(line)
        draw.text((img_w//2 - line_w//2, y_cur), line, color_carbon_powder, font=font)
        y_cur += font_size * line_height
    ### CATEGORY
    y_cur += gap_y
    y_start = y_cur
    x_cur = gap_x * 2
    col_i = 0
    for category in categories:
        y_cur = y_start
        text = category['heading'].upper()
        cell_width = img_w//2 - gap_x*2 - gap_x//2
        cell_width = img_w - gap_x*4
        rect_y2 = draw_cell(draw, text, 48, 'Bold', x_cur + col_w*col_i + cols_gap*col_i, y_cur, col_w, gap_x=gap_x, color=color_carbon_powder, checkbox=False)
        y_cur = rect_y2
        ### ITEMS
        for item in category['items']:
            text = item[0]
            rect_y2 = draw_cell(draw, text, 32, 'Regular', x_cur + col_w*col_i + cols_gap*col_i, y_cur, col_w, gap_x=gap_x, color=color_carbon_powder, checkbox=True)
            # rect_y2 = draw_cell(draw, text, 48, 'Regular', x_cur, y_cur, cell_width, checkbox=True)
            y_cur = rect_y2
        col_i += 1
        # y_cur += font_size * line_height
    ### GUIDES
    # draw.line([(img_w//2, 0), (img_w//2, img_h)], fill="#FF00FF", width=3)
    ### COPYRIGHT
    text = 'terrawhisper.com'.upper()
    font_size = 32
    font_family, font_weight = 'Lato', 'Bold'
    font_path = f"{g.ASSETS_FOLDERPATH}/fonts/{font_family}/{font_family}-{font_weight}.ttf"
    font = ImageFont.truetype(font_path, font_size)
    lines = text_to_lines(text, font, img_w - gap_x*2)
    line_height = 1.0
    y_cur = img_h - gap_y*2
    for line in lines:
        _, _, line_w, line_h = font.getbbox(line)
        draw.text((img_w//2 - line_w//2, y_cur), line, color_carbon_powder, font=font)
        y_cur += font_size * line_height
    img = img.convert('RGB')
    output_filepath = f'''{base_folderpath}/{data['slug']}.jpg'''
    img.save(output_filepath, format='JPEG', subsampling=0, quality=100)
    output_filepath = f'''{base_folderpath}/{data['slug']}-preview.jpg'''
    img = media.resize(img, img_w//4, img_h//4)
    img.save(output_filepath, format='JPEG', subsampling=0, quality=70)

def quick_start_guide_create(data):
    product_type_slug = data['product_type'].strip().lower().replace(' ', '-')
    base_folderpath = f'{g.DATABASE_FOLDERPATH}/shop/one-page/{product_type_slug}'
    input_filepath = f'''{base_folderpath}/{data['input_filename']}'''
    file_data = file_parse(input_filepath)
    title = file_data['title']
    subtitle = file_data['subtitle']
    categories = file_data['categories']
    print(f'##################################################################')
    print(f'TITLE: {title}')
    print(f'##################################################################')
    print()
    print(f'##################################################################')
    print(f'SUBTITLE: {subtitle}')
    print(f'##################################################################')
    print()
    print(f'##################################################################')
    print(f'CATEGORIES: {categories}')
    print(f'##################################################################')
    color_whisper_white = '#f7f6f2'
    color_carbon_powder = '#101211'
    img_w = 2480
    img_h = 3508
    gap_x = int((img_w / 100) * 5)
    gap_y = int((img_h / 100) * 5)
    img = Image.new(mode="RGBA", size=(img_w, img_h), color=color_whisper_white)
    ### OUTLINE
    draw = ImageDraw.Draw(img)
    draw.rectangle([(gap_x, gap_y), (img_w - gap_x, img_h - gap_y)], outline=color_carbon_powder, width=3)
    y_cur = 0
    ### COLUMNS
    cols_num = 2
    cols_gap = 48
    print_area_x = gap_x*2
    print_area_y = gap_y*2
    print_area_w = img_w - gap_x*4
    col_w = (print_area_w - cols_gap * (cols_num-1)) / cols_num
    ### TITLE
    text = title
    font_size = 256
    font_family, font_weight = 'Lato', 'Bold'
    font_path = f"{g.ASSETS_FOLDERPATH}/fonts/{font_family}/{font_family}-{font_weight}.ttf"
    font = ImageFont.truetype(font_path, font_size)
    lines = text_to_lines(text, font, img_w - gap_x*2)
    y_cur += gap_y * 1.5
    line_height = 1.0
    for line in lines:
        _, _, line_w, line_h = font.getbbox(line)
        draw.text((img_w//2 - line_w//2, y_cur), line, color_carbon_powder, font=font)
        y_cur += font_size * line_height
    ### CATEGORIES
    y_cur += gap_y
    y_start = y_cur
    x_cur = gap_x * 2
    ### 
    y_cur = y_start
    col_i = 0
    ### CATEGORY STUFF
    category = categories[0]
    text = category['heading'].upper()
    cell_width = img_w//2 - gap_x*2 - gap_x//2
    cell_width = img_w - gap_x*4
    rect_y2 = draw_cell(draw, text, 48, 'Bold', x_cur + col_w*col_i + cols_gap*col_i, y_cur, col_w, gap_x=gap_x, color=color_carbon_powder, checkbox=False)
    y_cur = rect_y2
    for item in category['items']:
        text = item[0]
        rect_y2 = draw_cell(draw, text, 32, 'Regular', x_cur + col_w*col_i + cols_gap*col_i, y_cur, col_w, gap_x=gap_x, color=color_carbon_powder, checkbox=False)
        y_cur = rect_y2
    y_cur += 50
    ### CATEGORY BENEFITS
    category = categories[1]
    text = category['heading'].upper()
    cell_width = img_w//2 - gap_x*2 - gap_x//2
    cell_width = img_w - gap_x*4
    rect_y2 = draw_cell(draw, text, 48, 'Bold', x_cur + col_w*col_i + cols_gap*col_i, y_cur, col_w, gap_x=gap_x, color=color_carbon_powder, checkbox=False)
    y_cur = rect_y2
    for item in category['items']:
        text = item[0]
        rect_y2 = draw_cell(draw, text, 32, 'Regular', x_cur + col_w*col_i + cols_gap*col_i, y_cur, col_w, gap_x=gap_x, color=color_carbon_powder, checkbox=False)
        y_cur = rect_y2
    y_cur += 50
    ### CATEGORY INGREDIENTS
    category = categories[2]
    text = category['heading'].upper()
    cell_width = img_w//2 - gap_x*2 - gap_x//2
    cell_width = img_w - gap_x*4
    rect_y2 = draw_cell(draw, text, 48, 'Bold', x_cur + col_w*col_i + cols_gap*col_i, y_cur, col_w, gap_x=gap_x, color=color_carbon_powder, checkbox=False)
    y_cur = rect_y2
    for item in category['items']:
        text = item[0]
        rect_y2 = draw_cell(draw, text, 32, 'Regular', x_cur + col_w*col_i + cols_gap*col_i, y_cur, col_w, gap_x=gap_x, color=color_carbon_powder, checkbox=False)
        y_cur = rect_y2
    y_cur += 50
    ### CATEGORY TOOLS
    category = categories[3]
    text = category['heading'].upper()
    cell_width = img_w//2 - gap_x*2 - gap_x//2
    cell_width = img_w - gap_x*4
    rect_y2 = draw_cell(draw, text, 48, 'Bold', x_cur + col_w*col_i + cols_gap*col_i, y_cur, col_w, gap_x=gap_x, color=color_carbon_powder, checkbox=False)
    y_cur = rect_y2
    for item in category['items']:
        text = item[0]
        rect_y2 = draw_cell(draw, text, 32, 'Regular', x_cur + col_w*col_i + cols_gap*col_i, y_cur, col_w, gap_x=gap_x, color=color_carbon_powder, checkbox=False)
        y_cur = rect_y2
    ### 
    y_cur = y_start
    col_i = 1
    ### CATEGORY HOW TO
    category = categories[4]
    text = category['heading'].upper()
    cell_width = img_w//2 - gap_x*2 - gap_x//2
    cell_width = img_w - gap_x*4
    rect_y2 = draw_cell(draw, text, 48, 'Bold', x_cur + col_w*col_i + cols_gap*col_i, y_cur, col_w, gap_x=gap_x, color=color_carbon_powder, checkbox=False)
    y_cur = rect_y2
    for item in category['items']:
        text = item[0]
        rect_y2 = draw_cell(draw, text, 32, 'Regular', x_cur + col_w*col_i + cols_gap*col_i, y_cur, col_w, gap_x=gap_x, color=color_carbon_powder, checkbox=False)
        y_cur = rect_y2
    ### COPYRIGHT
    ### calc size
    text = 'terrawhisper.com'.upper().strip()
    font_size = 32
    font_family, font_weight = 'Lato', 'Regular'
    font_path = f"{g.ASSETS_FOLDERPATH}/fonts/{font_family}/{font_family}-{font_weight}.ttf"
    font = ImageFont.truetype(font_path, font_size)
    line_height = 1.0
    line = text
    _, _, line_w, line_h = font.getbbox(line)
    x = img_w//2 - line_w//2
    y = img_h - gap_y//2 - line_h//2
    draw.text((x, y), line, color_carbon_powder, font=font)
    ### rect
    px = 32
    py = 16
    rect_x1 = x - px
    rect_y1 = y - py
    rect_x2 = x + line_w + px
    rect_y2 = y + line_h + py
    img = img.convert('RGB')
    output_filepath = f'''{base_folderpath}/{data['slug']}.jpg'''
    img.save(output_filepath, format='JPEG', subsampling=0, quality=100)
    output_filepath = f'''{base_folderpath}/{data['slug']}-preview.jpg'''
    img = media.resize(img, img_w//4, img_h//4)
    img.save(output_filepath, format='JPEG', subsampling=0, quality=70)

def lead_magnet_create(data):
    if data['product_layout'] == 'quick-start guide':
        quick_start_guide_create(data)
    elif data['product_layout'] == 'checklist':
        checklist_create(data)
    elif data['product_layout'] == 'checklist vanilla':
        checklist_vanilla_create(data)
    elif data['product_layout'] == 'checklist base':
        checklist_base_create(data)

def lead_magnet_banner_create(data, regen=False):
    if regen:
        product_type_slug = data['product_type'].strip().lower().replace(' ', '-')
        product_slug = data['slug'].strip().lower().replace(' ', '-')
        base_folderpath = f'{g.DATABASE_FOLDERPATH}/shop/one-page/{product_type_slug}/{product_slug}'
        images = []
        width = 1216
        height = 832
        ### images gen
        for i in range(2):
            prompt = f'''
                {data['banner_prompt_partial']},
                on a wooden table,
                surrounded by medicinal herbs,
                rustic, vintage, boho,
                soft focus,
                warm tones,
                high resolution,
            '''
            image = media.image_gen(prompt, width, height, steps=20, cfg=6.0)
            tmp_filepath = f'{g.vault_tmp_folderpath}/terrawhisper/lead-magnet/img-{i}.jpg' 
            image.save(tmp_filepath)
        ### pin gen
        tmp_folderpath = f'{g.vault_tmp_folderpath}/terrawhisper/lead-magnet'
        images_filepaths = [f'{tmp_folderpath}/{filename}' for filename in os.listdir(tmp_folderpath)]
        pin_w = 1000
        pin_h = 1500
        img = Image.new(mode="RGB", size=(pin_w, pin_h), color='#ffffff')
        draw = ImageDraw.Draw(img)
        gap = 8
        rect_h = 500
        img_0000 = Image.open(images_filepaths[0])
        img_0001 = Image.open(images_filepaths[1])
        img_0000 = media.resize(img_0000, int(pin_w*1), int(pin_w*1))
        img_0001 = media.resize(img_0001, int(pin_w*1), int(pin_w*1))
        img_0000_h = img_0000.size[1]
        img_0001_h = img_0001.size[1]
        img.paste(img_0000, (0, 0))
        img.paste(img_0001, (0, int(pin_h*0.5) + gap))
        text_color = '#f7f6f2'
        bg_color = '#101211'    
        # rect
        draw.rectangle(((0, pin_h//2 - rect_h//2), (pin_w, pin_h//2 + rect_h//2)), fill=bg_color)
        y_cur = 532
        ### text center
        text = f'''{data['product_title'].title()}'''.upper()
        font_size = 112
        font_family, font_weight = 'Lato', 'Bold'
        font_path = f"{g.ASSETS_FOLDERPATH}/fonts/{font_family}/{font_family}-{font_weight}.ttf"
        font = ImageFont.truetype(font_path, font_size)
        _, _, text_w, text_h = font.getbbox(text)
        lines = text_to_lines(text, font, data['banner_text_width'])
        for line in lines:
            _, _, line_w, line_h = font.getbbox(line)
            draw.text((pin_w//2 - line_w//2, y_cur), line, text_color, font=font)
            y_cur += font_size
        y_cur += 48
        ### text bottom
        if 1:
            text = f'''FREE {data['product_type'].upper()} >>'''
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
            _, _, text_w, text_h = font.getbbox(line)
            draw.text((pin_w//2 - text_w//2, pin_h - text_h - 96), line, text_color, font=font)
        # text
        output_filepath = f'''{base_folderpath}/{data['slug']}-banner.jpg'''
        img.save(output_filepath, format='JPEG', subsampling=0, quality=70)
        print(output_filepath)

def lead_magnet_upload(data):
    product_type_slug = data['product_type'].strip().lower().replace(' ', '-')
    product_slug = data['slug'].strip().lower().replace(' ', '-')
    shutil.copy2(
        f'''{g.DATABASE_FOLDERPATH}/shop/one-page/{product_type_slug}/{product_slug}/{data['slug']}-banner.jpg''',
        f'''{g.WEBSITE_FOLDERPATH}/images/shop/{data['slug']}-banner.jpg''',
    )
    shutil.copy2(
        f'''{g.DATABASE_FOLDERPATH}/shop/one-page/{product_type_slug}/{product_slug}/{data['slug']}-preview.jpg''',
        f'''{g.WEBSITE_FOLDERPATH}/images/shop/{data['slug']}-preview.jpg''',
    )
    shutil.copy2(
        f'''{g.DATABASE_FOLDERPATH}/shop/one-page/{product_type_slug}/{product_slug}/{data['slug']}.jpg''',
        f'''{g.WEBSITE_FOLDERPATH}/images/shop/{data['slug']}.jpg''',
    )

# json_dict = io.json_read(f'{g.DATABASE_FOLDERPATH}/shop/data.json')
# data = json_dict[-1]
# lead_magnet_create(data)

# quit()
json_dict = io.json_read(f'{g.DATABASE_FOLDERPATH}/shop/data.json')
for data in json_dict:
    if data['slug'] != 'checklist-10-herbs-90-percent-ailments': continue
    print(data)
    lead_magnet_create(data)
    lead_magnet_banner_create(data, regen=data['banner_regen'])
    lead_magnet_upload(data)

quit()
# >> create sign-up form (place in ???)
'''
Congratulations!
Check your email inbox for your download link. It may take a couple of minute to arrive. If you don't see it in the next 15 minutes, check your spam folder just in case.
'''
# >> shop_quick_start_guide_gen()
