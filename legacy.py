import os
import json

from lib import g
from lib import io
from lib import llm
from lib import data
from lib import utils
from lib import polish
from lib import components
from lib import sections

legacy_data = io.csv_to_dict('legacy/Table.csv', ',')
wcvp_data = io.csv_to_dict(f'{g.DATABASE_FOLDERPATH}/csv/wcvp/wcvp_names.csv', '|')

herbs_slugs = []
for item in legacy_data:
    if 'https://terrawhisper.com/herbs' in item['URL']:
        # print(item)
        herb_slug = item['URL'].split('https://terrawhisper.com/herbs/')[1].split('/')[0].split('.html')[0]
        herbs_slugs.append(herb_slug)

def answer_score_extract(json_data):
    _objs = []
    for item in json_data:
        try: answer = item['answer']
        except: continue
        try: score = item['score']
        except: continue
        _objs.append({
            "answer": answer, 
            "score": score,
        })
    return _objs

def total_score_calc(outputs):
    outputs_final = []
    for output in outputs:
        outputs_final.append({
            'answer': output['answer'],
            'mentions': int(output['mentions']),
            'confidence_score': int(output['confidence_score']),
            'total_score': int(output['mentions']) * int(output['confidence_score']),
        })
    outputs_final = sorted(outputs_final, key=lambda x: x['total_score'], reverse=True)
    print('***********************')
    print('***********************')
    print('***********************')
    for output in outputs_final:
        print(output)
    print('***********************')
    print('***********************')
    print('***********************')
    return outputs_final

def json_gen_medicine_poison_inert(herb_slug, regen=False, dispel=False):
    json_filepath = f'{g.DATABASE_FOLDERPATH}/legacy/{herb_slug}.json'
    json_data = io.json_read(json_filepath)
    herb_name_scientific = json_data['herb_name_scientific']
    key = 'medicine_poison_inert'
    if key not in json_data: json_data[key] = ''
    if regen: json_data[key] = ''
    if dispel: 
        json_data[key] = ''
        io.json_write(json_filepath, json_data)
        return
    if json_data[key] == '':
        outputs = []
        for i in range(10):
            print(f'{i} - {herb_name_scientific}')
            prompt = f'''
                Tell me if the following herb is considered medicinal, poisonous, or inert: {herb_name_scientific}.
                Also, tell give a confidence score from 1 to 10, indicating how sure you are about your answer.
                Reply in the following JSON format: 
                [
                    {{"answer": <write "medicine", "poison", or "inert" here>, "score": 8}} 
                ]
                Only reply with the JSON, don't add additional info.
                Don't include notes, reply ONLY with the JSON.
                /no_think
            '''
            reply = llm.reply(prompt)
            if '</think>' in reply:
                reply = reply.split('</think>')[1].strip()
            reply_data = {}
            try: reply_data = json.loads(reply)
            except: pass 
            if reply_data != {}:
                _objs = answer_score_extract(reply_data)
                for _obj in _objs:
                    answer = _obj['answer']
                    score = _obj['score']
                    found = False
                    for output in outputs:
                        if answer in output['answer']: 
                            output['mentions'] += 1
                            output['confidence_score'] += int(score)
                            found = True
                            break
                    if not found:
                        outputs.append({
                            'answer': answer, 
                            'mentions': 1, 
                            'confidence_score': int(score), 
                        })
        outputs = total_score_calc(outputs)
        json_data[key] = outputs
        io.json_write(json_filepath, json_data)

def json_gen_intro(json_filepath, regen=False, dispel=False):
    json_article_filepath = json_filepath
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
            Write a detailed paragraph in 5 sentences about {json_article['herb_name_scientific']} for medicinal purposes.
        '''
        prompt += f'/no_think'
        reply = llm.reply(prompt).strip()
        if '</think>' in reply:
            reply = reply.split('</think>')[1].strip()
        json_article[key] = reply
        io.json_write(json_article_filepath, json_article)

def json_gen_benefits(json_filepath, regen=False, dispel=False):
    json_article_filepath = json_filepath
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
            Write a detailed paragraph in 5 sentences about the health benefits of {json_article['herb_name_scientific']}.
            Start with the following words: {json_article['herb_name_scientific']} has several health benefits, such as .
        '''
        prompt += f'/no_think'
        reply = llm.reply(prompt).strip()
        if '</think>' in reply:
            reply = reply.split('</think>')[1].strip()
        json_article[key] = reply
        io.json_write(json_article_filepath, json_article)

def json_gen_constituents(json_filepath, regen=False, dispel=False):
    json_article_filepath = json_filepath
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
            Write a detailed paragraph in 5 sentences about the bioactive constituents of {json_article['herb_name_scientific']} for medicinal purposes.
            Start with the following words: {json_article['herb_name_scientific']} has several bioactive constituents, such as .
        '''
        prompt += f'/no_think'
        reply = llm.reply(prompt).strip()
        if '</think>' in reply:
            reply = reply.split('</think>')[1].strip()
        json_article[key] = reply
        io.json_write(json_article_filepath, json_article)

def json_gen_preparations(json_filepath, regen=False, dispel=False):
    json_article_filepath = json_filepath
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
            Write a detailed paragraph in 5 sentences about the medicinal preparations of {json_article['herb_name_scientific']}.
            By medicinal preparations, I mean things like teas, tinctures, etc.
            Start with the following words: {json_article['herb_name_scientific']} has several medicinal preparations, such as .
        '''
        prompt += f'/no_think'
        reply = llm.reply(prompt).strip()
        if '</think>' in reply:
            reply = reply.split('</think>')[1].strip()
        json_article[key] = reply
        io.json_write(json_article_filepath, json_article)

def json_gen_side_effects(json_filepath, regen=False, dispel=False):
    json_article_filepath = json_filepath
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
            Write a detailed paragraph in 5 sentences about the possible side effects of {json_article['herb_name_scientific']} on health.
            Start with the following words: {json_article['herb_name_scientific']} can have some side effects, such as .
        '''
        prompt += f'/no_think'
        reply = llm.reply(prompt).strip()
        if '</think>' in reply:
            reply = reply.split('</think>')[1].strip()
        json_article[key] = reply
        io.json_write(json_article_filepath, json_article)

def json_gen(wcvp_item):
    herb_name_scientific = wcvp_item['taxon_name']
    herb_slug = polish.sluggify(herb_name_scientific)
    print(f'{herb_slug} [JSON]')
    json_filepath = f'{g.DATABASE_FOLDERPATH}/legacy/{herb_slug}.json'
    json_data = io.json_read(json_filepath, create=True)
    json_data['herb_slug'] = herb_slug
    json_data['herb_name_scientific'] = herb_name_scientific
    json_data['herb_family'] = wcvp_item['family']
    json_data['title'] = herb_name_scientific.capitalize()
    io.json_write(json_filepath, json_data)
    ###
    json_gen_medicine_poison_inert(herb_slug, regen=False, dispel=False)
    json_gen_intro(json_filepath, regen=False, dispel=False)
    json_gen_benefits(json_filepath, regen=False, dispel=False)
    json_gen_constituents(json_filepath, regen=False, dispel=False)
    json_gen_preparations(json_filepath, regen=False, dispel=False)
    json_gen_side_effects(json_filepath, regen=False, dispel=False)

def html_gen(obj):
    herb_name_scientific = obj['herb_name_scientific']
    herb_slug = obj['herb_slug']
    herb_family = obj['herb_family']
    url_slug = obj['url_slug']
    print(f'{herb_slug} [HTML]')
    ###
    json_article_filepath = f'{g.DATABASE_FOLDERPATH}/legacy/{herb_slug}.json'
    json_article = io.json_read(json_article_filepath)
    html_filepath = f'''{g.website_folderpath}/{url_slug}.html'''
    print(f'{html_filepath}')
    ###
    html_article = ''
    json_title = f'''{json_article['title']}'''
    meta_title = f'''{json_title}'''
    meta_description = f''
    html_article += f'''<h1>{json_title.title()}</h1>'''
    # src = f'''/images/herbs/{json_article['herb_slug']}.jpg'''
    # alt = f'''{json_article['herb_slug']}'''
    # html_article += f'''<img src="{src}" alt="{alt}">'''
    html_article += f'''{utils.format_1N1(json_article['intro'])}'''
    html_article += f'''<h2>Benefits</h2>'''
    html_article += f'''{utils.format_1N1(json_article['benefits'])}'''
    # html_article += f'''<p><a href="/herbs/{json_article['herb_slug']}/benefits.html">10 Best Health Beneift of {json_article['herb_name_scientific']}</a></p>'''
    html_article += f'''<h2>Constituents</h2>'''
    html_article += f'''{utils.format_1N1(json_article['constituents'])}'''
    html_article += f'''<h2>Preparations</h2>'''
    html_article += f'''{utils.format_1N1(json_article['preparations'])}'''
    html_article += f'''<h2>Side Effects</h2>'''
    html_article += f'''{utils.format_1N1(json_article['side_effects'])}'''
    ###
    # html_article += f'''<h2>Bioactive Constituents</h2>'''
    # html_article += f'''{utils.format_1N1(json_article['constituents'])}'''
    # html_article += f'''<h2>Medicinal Preparations</h2>'''
    # html_article += f'''{utils.format_1N1(json_article['preparations'])}'''
    # html_article += f'''<h2>Side Effects</h2>'''
    # html_article += f'''{utils.format_1N1(json_article['side_effects'])}'''
    html = f'''
        <!DOCTYPE html>
        <html lang="en">
        {components.html_head(meta_title, meta_description)}
        <body>
            {sections.header()}
            {sections.breadcrumbs(url_slug)}
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
    herbs_slugs_ok = []
    for legacy_herb_slug_i, legacy_herb_slug in enumerate(herbs_slugs):
        print(f'>> {legacy_herb_slug_i}/{len(herbs_slugs)}')
        print(f'{legacy_herb_slug}')
        json_filepath = f'{g.DATABASE_FOLDERPATH}/legacy/{legacy_herb_slug}.json'
        # if os.path.exists(json_filepath): continue
        for wcvp_item in wcvp_data:
            wcvp_item_herb_name_scientific = wcvp_item['taxon_name']
            wcvp_item_herb_slug = polish.sluggify(wcvp_item_herb_name_scientific)
            if legacy_herb_slug == wcvp_item_herb_slug:
                herb_name_scientific = wcvp_item['taxon_name']
                herb_slug = polish.sluggify(herb_name_scientific)
                herb_family = wcvp_item['family']
                json_filepath = f'{g.DATABASE_FOLDERPATH}/legacy/{herb_slug}.json'
                json_gen(wcvp_item)
                _obj = {
                    'url_slug': f'herbs/{herb_slug}',
                    'herb_name_scientific': herb_name_scientific,
                    'herb_slug': herb_slug,
                    'herb_family': herb_family,
                }
                html_gen(_obj)
                break
    # quit()


