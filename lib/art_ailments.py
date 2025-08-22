from lib import g
from lib import io
from lib import llm
from lib import utils
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
            Write a detailed paragraph in 5 sentences about {obj['ailment_name']} and the herbal remedies to treat it.
        '''
        prompt += f'/no_think'
        reply = llm.reply(prompt).strip()
        if '</think>' in reply:
            reply = reply.split('</think>')[1].strip()
        json_article[key] = reply
        io.json_write(json_article_filepath, json_article)

def ai_llm_definition(obj, regen=False, dispel=False):
    json_article_filepath = f'''{g.database_folderpath}/json/{obj['url']}.json'''
    json_article = io.json_read(json_article_filepath)
    key = 'definition'
    if key not in json_article: json_article[key] = ''
    if regen: json_article[key] = ''
    if dispel: 
        json_article[key] = ''
        io.json_write(json_article_filepath, json_article)
        return
    if json_article[key] == '':
        prompt = f'''
            Write a detailed paragraph in 5 sentences about what is {obj['ailment_name']} and how does it affect your body.
        '''
        prompt += f'/no_think'
        reply = llm.reply(prompt).strip()
        if '</think>' in reply:
            reply = reply.split('</think>')[1].strip()
        json_article[key] = reply
        io.json_write(json_article_filepath, json_article)

def ai_llm_causes(obj, regen=False, dispel=False):
    json_article_filepath = f'''{g.database_folderpath}/json/{obj['url']}.json'''
    json_article = io.json_read(json_article_filepath)
    key = 'causes'
    if key not in json_article: json_article[key] = ''
    if regen: json_article[key] = ''
    if dispel: 
        json_article[key] = ''
        io.json_write(json_article_filepath, json_article)
        return
    if json_article[key] == '':
        prompt = f'''
            Write a detailed paragraph in 5 sentences about the underlying causes and risk factors of {obj['ailment_name']}.
        '''
        prompt += f'/no_think'
        reply = llm.reply(prompt).strip()
        if '</think>' in reply:
            reply = reply.split('</think>')[1].strip()
        json_article[key] = reply
        io.json_write(json_article_filepath, json_article)

def ai_llm_actions(obj, regen=False, dispel=False):
    json_article_filepath = f'''{g.database_folderpath}/json/{obj['url']}.json'''
    json_article = io.json_read(json_article_filepath)
    key = 'actions'
    if key not in json_article: json_article[key] = ''
    if regen: json_article[key] = ''
    if dispel: 
        json_article[key] = ''
        io.json_write(json_article_filepath, json_article)
        return
    if json_article[key] == '':
        prompt = f'''
            Write a detailed paragraph in 5 sentences about how herbal remedies interact with {obj['ailment_name']}.
        '''
        prompt += f'/no_think'
        reply = llm.reply(prompt).strip()
        if '</think>' in reply:
            reply = reply.split('</think>')[1].strip()
        json_article[key] = reply
        io.json_write(json_article_filepath, json_article)

def ai_llm_herbs(obj, regen=False, dispel=False):
    json_article_filepath = f'''{g.database_folderpath}/json/{obj['url']}.json'''
    json_article = io.json_read(json_article_filepath)
    key = 'herbs'
    if key not in json_article: json_article[key] = ''
    if regen: json_article[key] = ''
    if dispel: 
        json_article[key] = ''
        io.json_write(json_article_filepath, json_article)
        return
    if json_article[key] == '':
        prompt = f'''
            Write a detailed paragraph in 5 sentences about the best herbs for managing {obj['ailment_name']}.
        '''
        prompt += f'/no_think'
        reply = llm.reply(prompt).strip()
        if '</think>' in reply:
            reply = reply.split('</think>')[1].strip()
        json_article[key] = reply
        io.json_write(json_article_filepath, json_article)

def ai_llm_preparations(obj, regen=False, dispel=False):
    json_article_filepath = f'''{g.database_folderpath}/json/{obj['url']}.json'''
    json_article = io.json_read(json_article_filepath)
    key = 'preparations'
    if key not in json_article: json_article[key] = ''
    if regen: json_article[key] = ''
    if dispel: 
        json_article[key] = ''
        io.json_write(json_article_filepath, json_article)
        return
    if json_article[key] == '':
        prompt = f'''
            Write a detailed paragraph in 5 sentences about herbal preparations and formulations for {obj['ailment_name']}.
        '''
        prompt += f'/no_think'
        reply = llm.reply(prompt).strip()
        if '</think>' in reply:
            reply = reply.split('</think>')[1].strip()
        json_article[key] = reply
        io.json_write(json_article_filepath, json_article)

def ai_llm_precautions(obj, regen=False, dispel=False):
    json_article_filepath = f'''{g.database_folderpath}/json/{obj['url']}.json'''
    json_article = io.json_read(json_article_filepath)
    key = 'precautions'
    if key not in json_article: json_article[key] = ''
    if regen: json_article[key] = ''
    if dispel: 
        json_article[key] = ''
        io.json_write(json_article_filepath, json_article)
        return
    if json_article[key] == '':
        prompt = f'''
            Write a detailed paragraph in 5 sentences about how to use herbal remedies safely for {obj['ailment_name']}.
        '''
        prompt += f'/no_think'
        reply = llm.reply(prompt).strip()
        if '</think>' in reply:
            reply = reply.split('</think>')[1].strip()
        json_article[key] = reply
        io.json_write(json_article_filepath, json_article)

def ai_llm_complementary(obj, regen=False, dispel=False):
    json_article_filepath = f'''{g.database_folderpath}/json/{obj['url']}.json'''
    json_article = io.json_read(json_article_filepath)
    key = 'complementary'
    if key not in json_article: json_article[key] = ''
    if regen: json_article[key] = ''
    if dispel: 
        json_article[key] = ''
        io.json_write(json_article_filepath, json_article)
        return
    if json_article[key] == '':
        prompt = f'''
            Write a detailed paragraph in 5 sentences lifestyle, diet, and complementary practices that enhance herbal treatment for {obj['ailment_name']}.
        '''
        prompt += f'/no_think'
        reply = llm.reply(prompt).strip()
        if '</think>' in reply:
            reply = reply.split('</think>')[1].strip()
        json_article[key] = reply
        io.json_write(json_article_filepath, json_article)

def ai_llm_studies(obj, regen=False, dispel=False):
    json_article_filepath = f'''{g.database_folderpath}/json/{obj['url']}.json'''
    json_article = io.json_read(json_article_filepath)
    key = 'studies'
    if key not in json_article: json_article[key] = ''
    if regen: json_article[key] = ''
    if dispel: 
        json_article[key] = ''
        io.json_write(json_article_filepath, json_article)
        return
    if json_article[key] == '':
        prompt = f'''
            Write a detailed paragraph in 5 sentences about case studies and historical usage of herbs for {obj['ailment_name']}.
        '''
        prompt += f'/no_think'
        reply = llm.reply(prompt).strip()
        if '</think>' in reply:
            reply = reply.split('</think>')[1].strip()
        json_article[key] = reply
        io.json_write(json_article_filepath, json_article)

def json_gen(obj):
    json_article_filepath = f'''{g.database_folderpath}/json/{obj['url']}.json'''
    json_article = io.json_read(json_article_filepath)
    json_article['url'] = obj['url']
    json_article['ailment_slug'] = obj['ailment_slug']
    json_article['ailment_name'] = obj['ailment_name']
    json_article['title'] = f'''{obj['ailment_name']}: What to know to use herbal remedies'''
    io.json_write(json_article_filepath, json_article)
    ###
    ai_llm_intro(obj, regen=False, dispel=False)
    ai_llm_definition(obj, regen=False, dispel=False)
    ai_llm_causes(obj, regen=False, dispel=False)
    ai_llm_actions(obj, regen=False, dispel=False)
    ai_llm_herbs(obj, regen=False, dispel=False)
    ai_llm_preparations(obj, regen=False, dispel=False)
    ai_llm_precautions(obj, regen=False, dispel=False)
    ai_llm_complementary(obj, regen=False, dispel=False)
    ai_llm_studies(obj, regen=False, dispel=False)

def html_gen(obj):
    json_article_filepath = f'''{g.database_folderpath}/json/{obj['url']}.json'''
    json_article = io.json_read(json_article_filepath)
    html_article = ''
    json_title = f'''{json_article['title']}'''
    meta_title = f'''{json_title}'''
    meta_description = f''
    html_article += f'''<h1>{json_title.title()}</h1>'''
    src = f'''/images/ailments/{json_article['ailment_slug']}-herbs.jpg'''
    alt = f'''{json_article['ailment_name']} herbs'''
    html_article += f'''<img src="{src}" alt="{alt}">'''
    html_article += f'''{utils.format_1N1(json_article['intro'])}'''
    html_article += f'''[toc]'''
    ###
    html_article += f'''<h2>What is {json_article['ailment_name']} and how does it affect your body?</h2>'''
    html_article += f'''{utils.format_1N1(json_article['definition'])}'''
    html_article += f'''<h2>Underlying causes and risk factors of {json_article['ailment_name']}</h2>'''
    html_article += f'''{utils.format_1N1(json_article['causes'])}'''
    html_article += f'''<h2>Best herbs for managing {json_article['ailment_name']}</h2>'''
    html_article += f'''{utils.format_1N1(json_article['herbs'])}'''
    ### preparations [prp]
    html_article += f'''<h2>Herbal preparations and formulations for {json_article['ailment_name']}</h2>'''
    html_article += f'''{utils.format_1N1(json_article['preparations'])}'''
    preparation_list = io.csv_to_dict(f'{g.database_folderpath}/csv/preparations.csv')
    html_article += f'''<p>The best herbal preparations for {json_article['ailment_name']} are listed below.</p>'''
    html_article += f'<ul>'
    for preparation in preparation_list:
        item_text = f'''10 best herbal {preparation['preparation_name_plural']} for {json_article['ailment_name']}'''.title()
        html_article += f'''<li><a href="/{obj['url']}/{preparation['preparation_slug']}.html">{item_text}</a></li>'''
    html_article += f'</ul>'
    ###
    html_article += f'''<h2>How to use herbal remedies safely for {json_article['ailment_name']}</h2>'''
    html_article += f'''{utils.format_1N1(json_article['precautions'])}'''
    html_article += f'''<h2>Lifestyle, diet, and complementary practices that enhance herbal treatment for {obj['ailment_name']}</h2>'''
    html_article += f'''{utils.format_1N1(json_article['complementary'])}'''
    html_article += f'''<h2>Case studies and historical usage of herbs for {obj['ailment_name']}</h2>'''
    html_article += f'''{utils.format_1N1(json_article['studies'])}'''
    ###
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
    ailment_list = io.csv_to_dict(f'{g.database_folderpath}/csv/ailments.csv')
    for ailment_i, ailment in enumerate(ailment_list):
        ailment_slug = ailment['ailment_slug']
        ailment_name = ailment['ailment_name']
        print(f'AILMENT: {ailment_i}/{len(ailment_list)} - {ailment_name}')
        url = f'ailments/{ailment_slug}'
        obj = {
            'url': url,
            'ailment_slug': ailment_slug,
            'ailment_name': ailment_name,
        }
        json_gen(obj)
        # image_ai(obj)
        html_gen(obj)
        # quit()
    # image_pil(obj)

