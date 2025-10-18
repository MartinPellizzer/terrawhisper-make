import os
import json
import markdown

from lib import g
from lib import io
from lib import llm
from lib import media
from lib import utils
from lib import polish
from lib import components
from lib import sections

def art_wellness_hair_care_json_gen(article_data):
    print(f'ART: wellness hair care [json]')

def art_wellness_hair_care_html_gen(article_data):
    print(f'ART: wellness hair care [html]')

def art_wellness_hair_care():
    print(f'ART: wellness hair care')
    article_slug = f'wellness/hair-care'
    try: os.mkdir(f'wellness')
    except: pass
    article_data = {
        'article_slug': article_slug,
    }
    art_wellness_hair_care_json_gen(article_data)
    art_wellness_hair_care_html_gen(article_data)

def art_wellness_skin_care_herbs_json_gen_intro(article_data, regen=False, dispel=False):
    article_slug = article_data['article_slug']
    json_article_filepath = f'''{g.database_folderpath}/json/{article_slug}.json'''
    json_article = io.json_read(json_article_filepath)
    key = 'intro'
    if key not in json_article: 
        json_article[key] = ''
    if dispel: 
        json_article[key] = ''
        io.json_write(json_article_filepath, json_article)
        return
    if regen: 
        json_article[key] = ''
    if json_article[key] == '':
        prompt = f'''
            Write a detailed paragraph in 5 sentences about skin care herbs.
        '''
        prompt += f'/no_think'
        reply = llm.reply(prompt).strip()
        if '</think>' in reply:
            reply = reply.split('</think>')[1].strip()
        json_article[key] = reply
        io.json_write(json_article_filepath, json_article)

def art_wellness_skin_care_herbs_json_gen_list_init(article_data, regen=False, dispel=False):
    article_slug = article_data['article_slug']
    json_article_filepath = f'''{g.database_folderpath}/json/{article_slug}.json'''
    json_article = io.json_read(json_article_filepath)
    key = 'main_list'
    if key not in json_article: 
        json_article[key] = []
    if dispel: 
        json_article[key] = []
        io.json_write(json_article_filepath, json_article)
        return
    if regen: 
        json_article[key] = []
    if json_article[key] == []:
        output_list = []
        for i in range(1):
            prompt = f'''
                Write a list of the 10 best herbs for skin care.
                Also write a confidence score from 1 to 10 for each answer, indicating how confident you are about the answer.
                Reply using the following JSON format:
                [
                    {{"herb_name_common": "write name of herb 1 here", "confidence_score": 10}},
                    {{"herb_name_common": "write name of herb 2 here", "confidence_score": 5}},
                    {{"herb_name_common": "write name of herb 3 here", "confidence_score": 7}},
                    {{"herb_name_common": "write name of herb 4 here", "confidence_score": 3}},
                    {{"herb_name_common": "write name of herb 5 here", "confidence_score": 2}},
                    {{"herb_name_common": "write name of herb 6 here", "confidence_score": 6}},
                    {{"herb_name_common": "write name of herb 7 here", "confidence_score": 8}},
                    {{"herb_name_common": "write name of herb 8 here", "confidence_score": 9}},
                    {{"herb_name_common": "write name of herb 9 here", "confidence_score": 1}},
                    {{"herb_name_common": "write name of herb 10 here", "confidence_score": 4}}
                ]
                Reply only with the JSON.
            '''
            prompt += f'/no_think'
            reply = llm.reply(prompt).strip()
            if '</think>' in reply:
                reply = reply.split('</think>')[1].strip()
            try: json_reply = json.loads(reply)
            except: json_reply = {}
            if json_reply != {}:
                for json_obj in json_reply:
                    try: herb_name_common = json_obj['herb_name_common'].strip().lower()
                    except: continue
                    try: confidence_score = int(str(json_obj['confidence_score']).strip().lower())
                    except: continue
                    ###
                    _obj = {
                        "herb_name_common": herb_name_common, 
                        "confidence_score": confidence_score,
                    }
                    output_list.append(_obj)
        output_list = sorted(output_list, key=lambda x: x['confidence_score'], reverse=True)
        for output in output_list:
            print(output)
        json_article[key] = output_list
        io.json_write(json_article_filepath, json_article)

def art_wellness_skin_care_herbs_json_gen_list_desc(article_data, regen=False, dispel=False):
    article_slug = article_data['article_slug']
    json_article_filepath = f'''{g.database_folderpath}/json/{article_slug}.json'''
    json_article = io.json_read(json_article_filepath)
    key = 'desc'
    for json_obj in json_article['main_list']:
        if key not in json_obj: 
            json_obj[key] = ''
        if dispel: 
            json_obj[key] = ''
            io.json_write(json_article_filepath, json_article)
            return
        if regen: 
            json_obj[key] = ''
        if json_obj[key] == '':
            prompt = f'''
                Write a detailed paragraph in 5 sentences about {json_obj['herb_name_common']} for skin care.
            '''
            prompt += f'/no_think'
            reply = llm.reply(prompt).strip()
            if '</think>' in reply:
                reply = reply.split('</think>')[1].strip()
            reply = reply.replace('*', '')
            json_obj[key] = reply
            io.json_write(json_article_filepath, json_article)

def article_wellness_skin_care_herbs_json_gen(article_obj):
    print(f'ART: wellness skin care herbs [json]')
    article_slug = article_obj['article_slug']
    main_list_num = 10
    try: os.mkdir(f'{g.database_folderpath}/json/wellness')
    except: pass
    try: os.mkdir(f'{g.database_folderpath}/json/wellness/skin-care')
    except: pass
    json_article_filepath = f'''{g.database_folderpath}/json/{article_slug}.json'''
    json_article = io.json_read(json_article_filepath, create=True)
    json_article['article_slug'] = article_slug
    json_article['article_title'] = f'''{main_list_num} skin care herbs for Glowing and Healthy Skin'''
    json_article['entity_name'] = f'''herbs'''
    json_article['keyword_main'] = f'''skin care herbs'''
    json_article['keyword_main_slug'] = f'''skin-care-herbs'''
    json_article['keyword_main_pretty'] = f'''skin care herbs'''
    json_article['pin_image_title'] = f'''skin care medicinal herbs'''
    json_article['pin_board_name'] = article_obj['pin_board_name'] 
    json_article['main_list_num'] = main_list_num
    json_article['images_prompts'] = article_obj['images_prompts']
    io.json_write(json_article_filepath, json_article)
    art_wellness_skin_care_herbs_json_gen_intro(article_obj, regen=False, dispel=False)
    art_wellness_skin_care_herbs_json_gen_list_init(article_obj, regen=False, dispel=False)
    art_wellness_skin_care_herbs_json_gen_list_desc(article_obj, regen=False, dispel=False)

def article_wellness_skin_care_herbs_images_gen(article_data, regen=False):
    print(f'ART: wellness skin care herbs [images]')
    article_slug = article_data['article_slug']
    try: os.mkdir(f'{g.website_folderpath}/images/wellness')
    except: pass
    try: os.mkdir(f'{g.website_folderpath}/images/wellness/skin-care')
    except: pass
    try: os.mkdir(f'{g.website_folderpath}/images/wellness/skin-care/herbs')
    except: pass
    json_article_filepath = f'''{g.database_folderpath}/json/{article_slug}.json'''
    json_article = io.json_read(json_article_filepath)
    main_list = json_article['main_list']
    for item_i, item in enumerate(main_list[:]):
        herb_name_common = item['herb_name_common']
        herb_slug = herb_name_common.lower().strip().replace(' ', '-').replace('.', '').replace("'", '')
        out_filepath = f'''{g.website_folderpath}/images/{article_slug}/{herb_slug}.jpg'''
        prompt = f'''
            {herb_name_common},
            skincare herbs,
            spa aesthetic, minimalist, modern,
            bokeh, depth of field,
            high resolution,
        '''.replace('  ', ' ')
        if regen:
            image = media.image_gen(prompt, 832, 1216)
            image.save(out_filepath)
        else:
            if not os.path.exists(out_filepath): 
                image = media.image_gen(prompt, 832, 1216)
                image.save(out_filepath)
    ### featured
    out_filepath = f'''{g.website_folderpath}/images/{article_slug}/herbs.jpg'''
    prompt = f'''
        skincare herbs,
        spa aesthetic, minimalist, modern,
        bokeh, depth of field,
        high resolution,
    '''.replace('  ', ' ')
    if regen:
        image = media.image_gen(prompt, 1024, 1024)
        image = media.resize(image, 768, 768)
        image.save(out_filepath)
    else:
        if not os.path.exists(out_filepath): 
            image = media.image_gen(prompt, 1024, 1024)
            image = media.resize(image, 768, 768)
            image.save(out_filepath)

def article_wellness_skin_care_herbs_html_gen(article_data):
    article_slug = article_data['article_slug']
    print(f'ARTICLE: {article_slug} [html]')
    try: os.mkdir(f'{g.website_folderpath}/wellness')
    except: pass
    try: os.mkdir(f'{g.website_folderpath}/wellness/skin-care')
    except: pass
    json_article_filepath = f'''{g.database_folderpath}/json/{article_slug}.json'''
    json_article = io.json_read(json_article_filepath)
    html_article = ''
    json_title = f'''{json_article['title']}'''
    meta_title = f'''{json_title}'''
    meta_description = f''
    html_article += f'''<h1>{json_title.title()}</h1>'''
    src = f'''/images/{article_slug}/herbs.jpg'''
    alt = f'''skin care herbs'''
    html_article += f'''<img src="{src}" alt="{alt}">'''
    html_article += f'''{utils.format_1N1(json_article['intro'])}'''
    html_article += f'''[toc]'''
    for item_i, item in enumerate(json_article['main_list'][:10]):
        html_article += f'''<h2>{item_i+1}. {item['herb_name_common'].capitalize()}</h2>'''
        herb_name_common = item['herb_name_common']
        herb_slug = herb_name_common.strip().lower().replace(' ', '-').replace('.', '').replace("'", '')
        src = f'''/images/{article_slug}/{herb_slug}.jpg'''
        alt = f'''skin care {herb_name_common}'''
        html_article += f'''<img src="{src}" alt="{alt}">'''
        html_article += f'''{utils.format_1N1(item['desc'])}'''
    html_article = sections.toc(html_article)
    html = f'''
        <!DOCTYPE html>
        <html lang="en">
        {components.html_head(meta_title, meta_description)}
        <body>
            {sections.header()}
            {sections.breadcrumbs(article_slug)}
            <main class="container-md article">
                {html_article}
            </main>
            <div class="mt-64"></div>
            {sections.footer()}
        </body>
        </html>
    '''
    html_filepath = f'''{g.website_folderpath}/{article_slug}.html'''
    with open(html_filepath, 'w') as f: f.write(html)

def art_wellness_skin_care_herbs():
    print(f'ART: wellness skin care herbs')
    article_slug = f'wellness/skin-care/herbs'
    try: os.mkdir(f'wellness/skin-care')
    except: pass
    article_obj = {
        'article_slug': article_slug,
        'images_prompts': ['skincare herbs, spa aesthetic, minimalist, modern, bokeh, depth of field, high resolution'],
        'pin_board_name': 'herbal skin care',
    }
    article_wellness_skin_care_herbs_json_gen(article_obj)
    article_wellness_skin_care_herbs_images_gen(article_obj, regen=False)
    article_wellness_skin_care_herbs_html_gen(article_obj)

def art_wellness_skin_care_json_gen(article_data):
    print(f'ART: wellness skin care [json]')

def art_wellness_skin_care_html_gen(article_data):
    print(f'ART: wellness skin care [html]')

def article_wellness_skin_care():
    article_slug = f'wellness/skin-care'
    print(f'ART: {article_slug}')
    article_obj = {
        'article_slug': article_slug,
    }
    # art_wellness_skin_care_json_gen(article_data)
    # art_wellness_skin_care_html_gen(article_data)
    art_wellness_skin_care_herbs()

def article_wellness_json_gen(article_data):
    print(f'ART: wellness [json]')

def article_wellness_html_gen(article_data):
    print(f'ART: wellness [html]')

def article_wellness():
    article_slug = f'wellness'
    with open(f'{g.database_folderpath}/markdown/{article_slug}.md', encoding='utf-8') as f: 
        markdown_content = f.read()
    markdown_formatted = ''
    line_prev = ''
    for line in markdown_content.split('\n'):
        line = polish.to_ascii(line)
        if line.startswith('---'): continue
        if line_prev == '':
            markdown_formatted += '\n'
            markdown_formatted += line
            markdown_formatted += '\n'
        elif line_prev.startswith('-'): 
            markdown_formatted += line
            markdown_formatted += '\n'
        elif line_prev[0].isdigit(): 
            markdown_formatted += line
            markdown_formatted += '\n'
        elif line_prev.startswith('|'): 
            markdown_formatted += line
            markdown_formatted += '\n'
        else:
            markdown_formatted += '\n'
            markdown_formatted += line
            markdown_formatted += '\n'
        line_prev = line
        
    print(markdown_formatted)
    html_article = markdown.markdown(markdown_formatted, extensions=['markdown.extensions.tables'])
    meta_title = ''
    meta_description = ''
    html = f'''
        <!DOCTYPE html>
        <html lang="en">
        {components.html_head(meta_title, meta_description)}
        <body>
            {sections.header()}
            {sections.breadcrumbs(article_slug)}
            <main class="container-md article">
                <div class="article container-md">
                    {html_article}
                </div>
            </main>
            <div class="mt-64"></div>
            {sections.footer()}
        </body>
        </html>
    '''
    with open(f'{g.website_folderpath}/{article_slug}.html', 'w') as f: f.write(html)

    print(f'ART: wellness')
    article_slug = f'wellness'
    article_data = {
        'article_slug': article_slug,
    }
    # article_wellness_json_gen(article_data)
    # article_wellness_html_gen(article_data)
    article_wellness_skin_care()
    art_wellness_hair_care()

def gen():
    print(f'HUB: wellness')
    article_wellness()
