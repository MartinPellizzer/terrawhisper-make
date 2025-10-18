import os

from lib import g
from lib import io
from lib import llm
from lib import data
from lib import utils
from lib import polish
from lib import components
from lib import sections

def ai_llm_intro(obj, regen=False, dispel=False):
    json_article_filepath = f'''{obj['json_article_filepath']}'''
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
            Write a detailed paragraph in 5 sentences about the health benefits of {obj['herb_name_scientific']}.
        '''
        prompt += f'/no_think'
        reply = llm.reply(prompt).strip()
        if '</think>' in reply:
            reply = reply.split('</think>')[1].strip()
        json_article[key] = reply
        io.json_write(json_article_filepath, json_article)

def ai_llm_list_init(obj, regen=False, dispel=False):
    json_article_filepath = f'''{g.database_folderpath}/json/{obj['url']}.json'''
    json_article = io.json_read(json_article_filepath)
    key = 'benefits'
    if key not in json_article: 
        json_article[key] = []
    if dispel: 
        json_article[key] = []
        io.json_write(json_article_filepath, json_article)
        return
    if regen: 
        json_article[key] = []
    if json_article[key] == []:
        entity_herb_filepath = f'''{g.database_folderpath}/entities/herbs/{obj['herb_slug']}.json'''
        entity_herb = io.json_read(entity_herb_filepath)
        entity_herb_benefits = entity_herb['herb_benefits']
        entity_herb_benefits_names = [x['answer'] for x in entity_herb_benefits]
        json_article[key] = entity_herb_benefits
        io.json_write(json_article_filepath, json_article)

def ai_llm_list_desc(obj, regen=False, dispel=False):
    json_article_filepath = f'''{g.database_folderpath}/json/{obj['url']}.json'''
    json_article = io.json_read(json_article_filepath)
    key = 'benefit_desc'
    for json_obj in json_article['benefits']:
        if key not in json_obj: 
            json_obj[key] = ''
        if dispel: 
            json_obj[key] = ''
            io.json_write(json_article_filepath, json_article)
            return
        if regen: 
            json_obj[key] = ''
        if json_obj[key] == '':
            start_sentence = f'''{json_article['herb_name_scientific']} {json_obj['answer'].lower()}'''
            if start_sentence != '': 
                start_sentence_prompt = f'''Start the reply with the following words: {start_sentence}'''
            else: 
                start_sentence_prompt = ''
            prompt = f'''
                Write a detailed paragraph in 5 sentences about the following benefit of {json_article['herb_name_scientific']}: {json_obj['answer']}.
                {start_sentence_prompt}
            '''
            prompt += f'/no_think'
            reply = llm.reply(prompt).strip()
            if '</think>' in reply:
                reply = reply.split('</think>')[1].strip()
            reply = reply.replace('*', '')
            json_obj[key] = reply
            io.json_write(json_article_filepath, json_article)

def json_gen(obj):
    try: os.mkdir(f'{g.database_folderpath}/json/herbs')
    except: pass
    try: os.mkdir(f'{g.database_folderpath}/json/herbs/{herb_slug}')
    except: pass
    try: os.mkdir(f'{g.database_folderpath}/json/herbs/{herb_slug}')
    except: pass
    json_article_filepath = f'''{obj['json_article_filepath']}'''
    json_article = io.json_read(json_article_filepath, create=True)
    json_article['url'] = obj['url']
    json_article['herb_slug'] = obj['herb_slug']
    json_article['herb_name_scientific'] = obj['herb_name_scientific']
    json_article['main_lst_num'] = 10
    json_article['title'] = f'''10 best {obj['herb_name_scientific']} health benefits'''
    io.json_write(json_article_filepath, json_article)
    ###
    ai_llm_intro(obj, regen=False, dispel=False)
    ai_llm_list_init(obj, regen=False, dispel=False)
    ai_llm_list_desc(obj, regen=False, dispel=False)

def html_gen(obj):
    html_filepath = f'''{g.website_folderpath}/{obj['url']}.html'''
    try: os.mkdir(f'{g.website_folderpath}/herbs')
    except: pass
    try: os.mkdir(f'''{g.website_folderpath}/herbs/{obj['herb_slug']}''')
    except: pass
    json_article_filepath = f'''{obj['json_article_filepath']}'''
    json_article = io.json_read(json_article_filepath)
    html_article = ''
    json_title = f'''{json_article['title']}'''
    meta_title = f'''{json_title}'''
    meta_description = f''
    html_article += f'''<h1>{json_title.title()}</h1>'''
    src = f'''/images/herbs/{json_article['herb_slug']}.jpg'''
    alt = f'''{json_article['herb_slug']} benefits'''
    html_article += f'''<img src="{src}" alt="{alt}">'''
    html_article += f'''{utils.format_1N1(json_article['intro'])}'''
    for benefit_i, benefit in enumerate(json_article['benefits'][:10]):
        html_article += f'''<h2>{benefit_i+1}. {benefit['answer'].capitalize()}</h2>'''
        html_article += f'''{utils.format_1N1(benefit['benefit_desc'])}'''
    html = f'''
        <!DOCTYPE html>
        <html lang="en">
        {components.html_head(meta_title, meta_description)}
        <body>
            {sections.header()}
            {sections.breadcrumbs(obj['url'])}
            <main class="container-md article">
                {html_article}
            </main>
            <div class="mt-64"></div>
            {sections.footer()}
        </body>
        </html>
    '''
    with open(html_filepath, 'w') as f: f.write(html)

def gen():
    entities_herbs_folderpath = f'{g.database_folderpath}/entities/herbs'
    herbs = data.herbs_medicinal_get()
    for herb_i, herb in enumerate(herbs):
        print(f'HERB: {herb_i}/{len(herbs)} - {herb}')
        herb_name_scientific = herb['herb_name_scientific']
        herb_slug = polish.sluggify(herb_name_scientific)
        entity_herb_filepath = f'{entities_herbs_folderpath}/{herb_slug}.json'
        try: os.mkdir(f'{g.database_folderpath}/json/herbs/{herb_slug}')
        except: pass
        url_relative = f'herbs/{herb_slug}/benefits'
        json_article_filepath = f'{g.database_folderpath}/json/{url_relative}.json'
        obj = {
            'url': url_relative,
            'json_article_filepath': json_article_filepath,
            'herb_slug': herb_slug,
            'herb_name_scientific': herb_name_scientific,
        }
        json_gen(obj)
        # image_ai(obj)
        html_gen(obj)
        # quit()
    # image_pil(obj)

