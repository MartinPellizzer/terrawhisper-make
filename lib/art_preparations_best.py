import os

from lib import g
from lib import io
from lib import llm
from lib import data
from lib import media
from lib import utils
from lib import polish
from lib import components
from lib import sections

def ai_llm_intro(obj, regen=False, dispel=False):
    json_article_filepath = f'''{g.database_folderpath}/json/{obj['url']}.json'''
    json_article = io.json_read(json_article_filepath)
    key = 'intro'
    if key not in json_article: json_article[key] = ''
    if regen: json_article[key] = ''
    if dispel: 
        json_article[key] = ''
        io.json_write(json_article_filepath, json_article)
        return
    if json_article[key] == '':
        prompt = f'''
            Write a detailed paragraph in 5 sentences about some of the best medicinal herbal {obj['preparation_name_plural']}.
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
    key = 'herbs'
    if key not in json_article: 
        json_article[key] = []
    if dispel: 
        json_article[key] = []
        io.json_write(json_article_filepath, json_article)
        return
    if regen: 
        json_article[key] = []
    if json_article[key] == []:
        herbs = data.herbs_popular_get(obj['preparation_slug'], 100)
        json_article[key] = herbs
        io.json_write(json_article_filepath, json_article)

def ai_llm_list_desc(obj, regen=False, dispel=False):
    json_article_filepath = f'''{g.database_folderpath}/json/{obj['url']}.json'''
    json_article = io.json_read(json_article_filepath)
    key = 'herb_desc'
    for json_obj in json_article['herbs']:
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
                Write a detailed paragraph in 5 sentences about the uses of {json_obj['herb_name_scientific']} herbal {json_article['preparation_name_plural']} and why.
                Start with the following words: {json_obj['herb_name_scientific']} herbal {json_article['preparation_name_plural']} are used to .
            '''
            prompt += f'/no_think'
            reply = llm.reply(prompt).strip()
            if '</think>' in reply:
                reply = reply.split('</think>')[1].strip()
            reply = reply.replace('*', '')
            json_obj[key] = reply
            io.json_write(json_article_filepath, json_article)

def json_gen(obj):
    try: os.mkdir(f'{g.database_folderpath}/json/preparations')
    except: pass
    try: os.mkdir(f'''{g.database_folderpath}/json/preparations/{obj['preparation_slug']}''')
    except: pass
    json_article_filepath = f'''{g.database_folderpath}/json/{obj['url']}.json'''
    json_article = io.json_read(json_article_filepath, create=True)
    json_article['url'] = obj['url']
    json_article['preparation_slug'] = obj['preparation_slug']
    json_article['preparation_name_singular'] = obj['preparation_name_singular']
    json_article['preparation_name_plural'] = obj['preparation_name_plural']
    json_article['title'] = f'''What to know about medicinal herbal {obj['preparation_name_plural']}'''
    io.json_write(json_article_filepath, json_article)
    ###
    ai_llm_intro(obj, regen=False, dispel=False)
    ai_llm_list_init(obj, regen=False, dispel=False)
    ai_llm_list_desc(obj, regen=False, dispel=False)

def html_gen(obj):
    try: os.mkdir(f'{g.website_folderpath}/preparations')
    except: pass
    try: os.mkdir(f'''{g.website_folderpath}/preparations/{obj['preparation_slug']}''')
    except: pass
    json_article_filepath = f'''{g.database_folderpath}/json/{obj['url']}.json'''
    json_article = io.json_read(json_article_filepath)
    html_article = ''
    json_title = f'''{json_article['title']}'''
    meta_title = f'''{json_title}'''
    meta_description = f''
    html_article += f'''<h1>{json_title.title()}</h1>'''
    src = f'''/images/preparations/herbal-{json_article['preparation_slug']}.jpg'''
    alt = f'''herbal {json_article['preparation_name_plural']}'''
    html_article += f'''<img src="{src}" alt="{alt}">'''
    html_article += f'''{utils.format_1N1(json_article['intro'])}'''
    ### lead magnet
    with open(f'{g.DATABASE_FOLDERPATH}/assets/scripts/newsletter/form-head.txt') as f: 
        form_head = f.read()
    with open(f'{g.DATABASE_FOLDERPATH}/assets/scripts/newsletter/form-herb-drying-checklist.txt') as f: 
        form_herb_drying_checklist = f.read()
    html_article += f'''
        <div class="free-gift">
            <p class="free-gift-heading">FREE Herb Drying Checklist</p>
            <p style="text-align: center; margin-bottom: 1.6rem;">How to make sure every batch retains maximum flavor, color, and aroma without the risk of mold or over-drying. Eliminate guesswork and trial-and-error, making herb drying faster, easier, and more efficient every time.</p>
            {form_herb_drying_checklist}
        </div>
    '''
    ### toc
    html_article += f'''[toc]'''
    ### list
    for i, herb in enumerate(json_article['herbs']):
        preparation_slug = json_article['preparation_slug']
        herb_slug = herb['herb_name_scientific'].strip().lower().replace(' ', '-').replace('.', '')
        # print(herb_slug)
        try:
            herb_slug_patched_for_common_name = herb_slug.replace('mentha-piperita', 'mentha-x-piperita')
            ssot_herb_primary_filepath = f'{g.SSOT_FOLDERPATH}/herbs/herbs-primary/{herb_slug_patched_for_common_name}.json'
            herb_data = io.json_read(ssot_herb_primary_filepath)
            herb_name_common = herb_data['herb_names_common'][0]['answer']
            html_article += f'''<h2>{i+1}. {herb_name_common.capitalize()} ({herb['herb_name_scientific'].capitalize()})</h2>'''
        except:
            html_article += f'''<h2>{i+1}. {herb['herb_name_scientific'].capitalize()}</h2>'''
        src = f'''/images/preparations/{preparation_slug}/{herb_slug}-{preparation_slug}.jpg'''
        alt = f'''{herb['herb_name_scientific']} {json_article['preparation_name_singular']}'''
        html_article += f'''<img src="{src}" alt="{alt}">'''
        html_article += f'''{utils.format_1N1(herb['herb_desc'])}'''
    html_article = sections.toc(html_article)
    html = f'''
        <!DOCTYPE html>
        <html lang="en">
        {components.html_head(meta_title, meta_description, form_head)}
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
    html_filepath = f'''{g.website_folderpath}/{obj['url']}.html'''
    with open(html_filepath, 'w') as f: f.write(html)

def image_ai(obj, regen=False):
    json_article_filepath = f'''{g.database_folderpath}/json/{obj['url']}.json'''
    json_article = io.json_read(json_article_filepath)
    preparation_slug = json_article['preparation_slug']
    preparation_name_singular = json_article['preparation_name_singular']
    preparation_name_plural = json_article['preparation_name_plural']
    # out_filepath = f'''{g.database_folderpath}/images/preparations/herbal-{preparation_slug}.jpg'''
    out_filepath = f'''{g.website_folderpath}/images/preparations/herbal-{preparation_slug}.jpg'''
    if regen == False:
        if os.path.exists(out_filepath): return
    else:
        prompt = f'''
            herbal {preparation_name_singular},
            surrounded by medicinal herbs,
            rustic, vintage, boho,
            warm tones,
            high resolution,
        '''.replace('  ', ' ')
        image = media.image_gen(prompt, 1024, 1024)
        image = media.resize(image, 768, 768)
        # image.show()
        image.save(out_filepath)
    # quit()

def gen():
    preparation_list = io.csv_to_dict(f'{g.database_folderpath}/csv/preparations.csv')
    for preparation_i, preparation in enumerate(preparation_list):
        preparation_slug = preparation['preparation_slug']
        preparation_name_singular = preparation['preparation_name_singular']
        preparation_name_plural = preparation['preparation_name_plural']
        print(f'PREPARATION: {preparation_slug}')
        url_relative = f'preparations/{preparation_slug}/best'
        obj = {
            'url': url_relative,
            'preparation_slug': preparation_slug,
            'preparation_name_singular': preparation_name_singular,
            'preparation_name_plural': preparation_name_plural,
        }
        json_gen(obj)
        # image_ai(obj, regen=False)
        html_gen(obj)
        # quit()

