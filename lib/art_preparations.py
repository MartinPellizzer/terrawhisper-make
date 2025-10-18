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
            Write a detailed paragraph in 5 sentences about medicinal herbal {obj['preparation_name_plural']}.
        '''
        prompt += f'/no_think'
        reply = llm.reply(prompt).strip()
        if '</think>' in reply:
            reply = reply.split('</think>')[1].strip()
        json_article[key] = reply
        io.json_write(json_article_filepath, json_article)

def ai_llm_best(obj, regen=False, dispel=False):
    json_article_filepath = f'''{g.database_folderpath}/json/{obj['url']}.json'''
    json_article = io.json_read(json_article_filepath)
    key = 'best'
    if key not in json_article: json_article[key] = ''
    if regen: json_article[key] = ''
    if dispel: 
        json_article[key] = ''
        io.json_write(json_article_filepath, json_article)
        return
    if json_article[key] == '':
        prompt = f'''
            Write a detailed paragraph in 5 sentences about what are the best medicinal herbal {obj['preparation_name_plural']}.
            Start with the following words: Sone of the best medicinal herbal teas are .
        '''
        prompt += f'/no_think'
        reply = llm.reply(prompt).strip()
        if '</think>' in reply:
            reply = reply.split('</think>')[1].strip()
        json_article[key] = reply
        io.json_write(json_article_filepath, json_article)

def json_gen(obj):
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
    # ai_llm_definition(obj, regen=False, dispel=False)
    # ai_llm_causes(obj, regen=False, dispel=False)
    # ai_llm_actions(obj, regen=False, dispel=False)
    # ai_llm_herbs(obj, regen=False, dispel=False)
    # ai_llm_preparations(obj, regen=False, dispel=False)
    # ai_llm_precautions(obj, regen=False, dispel=False)
    # ai_llm_complementary(obj, regen=False, dispel=False)
    # ai_llm_studies(obj, regen=False, dispel=False)
    ai_llm_best(obj, regen=False, dispel=False)

def html_gen(obj):
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
    html_article += f'''[toc]'''
    html_article += f'''<h2>What are the best medicinal herbal {json_article['preparation_name_plural']}?</h2>'''
    html_article += f'''{utils.format_1N1(json_article['best'])}'''
    html_article += f'''<p>Check the following link for a full list of the <a href="/{json_article['url']}/best.html">100 best medicinal herbal {json_article['preparation_name_plural']}</a>.</p>'''
    html_article = sections.toc(html_article)
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
    html_filepath = f'''{g.website_folderpath}/{obj['url']}.html'''
    with open(html_filepath, 'w') as f: f.write(html)

def gen():
    preparation_list = io.csv_to_dict(f'{g.database_folderpath}/csv/preparations.csv')
    for preparation_i, preparation in enumerate(preparation_list):
        preparation_slug = preparation['preparation_slug']
        preparation_name_singular = preparation['preparation_name_singular']
        preparation_name_plural = preparation['preparation_name_plural']
        print(f'PREPARATION: {preparation_slug}')
        url_relative = f'preparations/{preparation_slug}'
        obj = {
            'url': url_relative,
            'preparation_slug': preparation_slug,
            'preparation_name_singular': preparation_name_singular,
            'preparation_name_plural': preparation_name_plural,
        }
        json_gen(obj)
        # image_ai(obj)
        html_gen(obj)
        # quit()
