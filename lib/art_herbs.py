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
    json_article_filepath = obj['json_article_filepath']
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
            Write a detailed paragraph in 5 sentences about {obj['herb_name_scientific']} for medicinal purposes.
        '''
        prompt += f'/no_think'
        reply = llm.reply(prompt).strip()
        if '</think>' in reply:
            reply = reply.split('</think>')[1].strip()
        json_article[key] = reply
        io.json_write(json_article_filepath, json_article)

def ai_llm_benefits(obj, regen=False, dispel=False):
    json_article_filepath = obj['json_article_filepath']
    json_article = io.json_read(json_article_filepath)
    key = 'benefits'
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
            Start with the following words: {obj['herb_name_scientific']} has several health benefits, such as .
        '''
        prompt += f'/no_think'
        reply = llm.reply(prompt).strip()
        if '</think>' in reply:
            reply = reply.split('</think>')[1].strip()
        json_article[key] = reply
        io.json_write(json_article_filepath, json_article)

def ai_llm_constituents(obj, regen=False, dispel=False):
    json_article_filepath = obj['json_article_filepath']
    json_article = io.json_read(json_article_filepath)
    key = 'constituents'
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
            Write a detailed paragraph in 5 sentences about the bioactive constituents of {obj['herb_name_scientific']} for medicinal purposes.
            Start with the following words: {obj['herb_name_scientific']} has several bioactive constituents, such as .
        '''
        prompt += f'/no_think'
        reply = llm.reply(prompt).strip()
        if '</think>' in reply:
            reply = reply.split('</think>')[1].strip()
        json_article[key] = reply
        io.json_write(json_article_filepath, json_article)

def ai_llm_preparations(obj, regen=False, dispel=False):
    json_article_filepath = obj['json_article_filepath']
    json_article = io.json_read(json_article_filepath)
    key = 'preparations'
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
            Write a detailed paragraph in 5 sentences about the medicinal preparations of {obj['herb_name_scientific']}.
            By medicinal preparations, I mean things like teas, tinctures, etc.
            Start with the following words: {obj['herb_name_scientific']} has several medicinal preparations, such as .
        '''
        prompt += f'/no_think'
        reply = llm.reply(prompt).strip()
        if '</think>' in reply:
            reply = reply.split('</think>')[1].strip()
        json_article[key] = reply
        io.json_write(json_article_filepath, json_article)

def ai_llm_side_effects(obj, regen=False, dispel=False):
    json_article_filepath = obj['json_article_filepath']
    json_article = io.json_read(json_article_filepath)
    key = 'side_effects'
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
            Write a detailed paragraph in 5 sentences about the possible side effects of {obj['herb_name_scientific']} on health.
            Start with the following words: {obj['herb_name_scientific']} can have some side effects, such as .
        '''
        prompt += f'/no_think'
        reply = llm.reply(prompt).strip()
        if '</think>' in reply:
            reply = reply.split('</think>')[1].strip()
        json_article[key] = reply
        io.json_write(json_article_filepath, json_article)

def json_gen(obj):
    json_article_filepath = obj['json_article_filepath']
    json_article = io.json_read(json_article_filepath, create=True)
    json_article['url'] = obj['url']
    json_article['herb_slug'] = obj['herb_slug']
    json_article['herb_name_scientific'] = obj['herb_name_scientific']
    json_article['title'] = f'''{obj['herb_name_scientific']}: What to know before using it for medicinal purposes'''
    io.json_write(json_article_filepath, json_article)
    ###
    ai_llm_intro(obj, regen=False, dispel=False)
    ai_llm_benefits(obj, regen=False, dispel=False)
    ai_llm_constituents(obj, regen=False, dispel=False)
    ai_llm_preparations(obj, regen=False, dispel=False)
    ai_llm_side_effects(obj, regen=False, dispel=False)
    # ai_llm_list_init(obj, regen=False, dispel=False)
    # ai_llm_list_desc(obj, regen=False, dispel=False)

def json_gen_2(obj):
    json_article_filepath = obj['json_article_filepath']
    json_article = io.json_read(json_article_filepath, create=True)
    json_article['url'] = obj['url']
    json_article['herb_slug'] = obj['herb_slug']
    json_article['herb_name_scientific'] = obj['herb_name_scientific']
    json_article['title'] = f'''{obj['herb_name_scientific']}: What to know before using it for medicinal purposes'''
    io.json_write(json_article_filepath, json_article)
    ###
    ai_llm_intro(obj, regen=False, dispel=False)

def html_gen(obj):
    html_filepath = f'''{g.website_folderpath}/{obj['url']}.html'''
    json_article_filepath = obj['json_article_filepath']
    json_article = io.json_read(json_article_filepath)
    html_article = ''
    json_title = f'''{json_article['title']}'''
    meta_title = f'''{json_title}'''
    meta_description = f''
    html_article += f'''<h1>{json_title.title()}</h1>'''
    src = f'''/images/herbs/{json_article['herb_slug']}.jpg'''
    alt = f'''{json_article['herb_slug']}'''
    html_article += f'''<img src="{src}" alt="{alt}">'''
    html_article += f'''{utils.format_1N1(json_article['intro'])}'''
    html_article += f'''<h2>Health Benefits</h2>'''
    html_article += f'''{utils.format_1N1(json_article['benefits'])}'''
    html_article += f'''<p><a href="/herbs/{json_article['herb_slug']}/benefits.html">10 Best Health Beneift of {json_article['herb_name_scientific']}</a></p>'''
    ###
    html_article += f'''<h2>Bioactive Constituents</h2>'''
    html_article += f'''{utils.format_1N1(json_article['constituents'])}'''
    html_article += f'''<h2>Medicinal Preparations</h2>'''
    html_article += f'''{utils.format_1N1(json_article['preparations'])}'''
    html_article += f'''<h2>Side Effects</h2>'''
    html_article += f'''{utils.format_1N1(json_article['side_effects'])}'''
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

def medicine_poison_inert_get(tmp_filepath):
    tmp_data = io.json_read(tmp_filepath)
    try: tmp_medicine_poison_inert = tmp_data['medicine_poison_inert'] 
    except: return None
    score_medicine = 0
    score_inert = 0
    score_poison = 0
    for item in tmp_medicine_poison_inert:
        if item['answer'] == 'medicine':
            score_medicine = item['total_score']
        if item['answer'] == 'inert':
            score_inert = item['total_score']
        if item['answer'] == 'poison':
            score_poison = item['total_score']
    if score_medicine > score_inert and score_medicine > score_poison:
        _obj = {
            'answer': 'medicine',
            'total_score': score_medicine,
        }
        return _obj
    elif score_inert > score_medicine and score_inert > score_poison:
        _obj = {
            'answer': 'inert',
            'total_score': score_inert,
        }
        return _obj
    else:
        _obj = {
            'answer': 'poison',
            'total_score': score_poison,
        }
        return _obj

def gen():
    if 0:
        herbs = data.herbs_medicinal_get()
        for herb_i, herb in enumerate(herbs):
            print(f'HERB: {herb_i}/{len(herbs)} - {herb}')
            herb_name_scientific = herb['herb_name_scientific']
            herb_slug = polish.sluggify(herb_name_scientific)
            url_relative = f'herbs/{herb_slug}'
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
    else:
        tmp_filenames = os.listdir(f'{g.PLANTS_TMP_FOLDERPATH}')
        for tmp_filename_i, tmp_filename in enumerate(tmp_filenames[:]):
            tmp_filepath = f'{g.PLANTS_TMP_FOLDERPATH}/{tmp_filename}'
            medicine_poison_inert = medicine_poison_inert_get(tmp_filepath)
            if medicine_poison_inert == None: continue
            if medicine_poison_inert['answer'] == 'medicine':
                json_article_filepath = f'{g.JSON_HERBS_FOLDERPATH}/{tmp_filename}'
                json_article = io.json_read(json_article_filepath)
                herb_name_scientific = json_article['herb_name_scientific']
                herb_slug = polish.sluggify(herb_name_scientific)
                url_relative = f'herbs/{herb_slug}'
                obj = {
                    'url': url_relative,
                    'json_article_filepath': json_article_filepath,
                    'herb_slug': herb_slug,
                    'herb_name_scientific': herb_name_scientific,
                }
                print(f'{tmp_filename_i} - {json_article_filepath}')
                print(obj)
                # quit()
                json_gen_2(obj)
                # quit()
            

