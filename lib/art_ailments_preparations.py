import json
import random

from lib import g
from lib import io
from lib import llm
from lib import components

wcvp_rows = io.csv_read(f'{g.database_folderpath}/csv/wcvp/wcvp_names.csv', '|')
wcvp_dict = io.csv_to_dict(f'{g.database_folderpath}/csv/wcvp/wcvp_names.csv', '|')

def ai_llm_intro(obj, regen=False, dispel=False):
    json_article_filepath = f'''{g.database_folderpath}/json/{obj['url']}.json'''
    json_article = io.json_read(json_article_filepath)
    key = 'intro'
    if key not in json_article: 
        json_article[key] = ''
    if dispel: 
        json_article[key] = ''
        return
    if regen: 
        json_article[key] = ''
    if json_article[key] == '':
        prompt = f'''
            Write a detailed paragraph in 5 sentences about herbal {obj['preparation_name_plural']} for {obj['ailment_name']}.
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
    key = 'preparations'
    if key not in json_article: 
        json_article[key] = []
    if dispel: 
        json_article[key] = []
        return
    if regen: 
        json_article[key] = []
    if json_article[key] == []:
        output_list = []
        for i in range(10):
            rnd_num = random.randint(10, 15)
            prompt = f'''
                Write a list of the {rnd_num} best herbal {obj['preparation_name_plural']} for {obj['ailment_name']}.
                Write only the scientific name of the herbs uses, not the type of preparation.
                Don't repeat herbs.
                Also write a confidence score from 1 to 10 for each answer, indicating how confident you are about the answer.
                Reply using the following JSON format:
                [
                    {{"herb_name_scientific": "write scientific name of herb 1 here", "confidence_score": 10}},
                    {{"herb_name_scientific": "write scientific name of herb 2 here", "confidence_score": 5}},
                    {{"herb_name_scientific": "write scientific name of herb 3 here", "confidence_score": 7}}
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
                output_list_tmp = []
                for json_obj in json_reply:
                    try: herb_name_scientific = json_obj['herb_name_scientific'].strip().lower()
                    except: continue
                    try: herb_confidence_score = int(str(json_obj['confidence_score']).strip().lower())
                    except: continue
                    ###
                    found = False
                    for wcvp_obj in wcvp_dict:
                        wcvp_herb_name_scientific = f'''{wcvp_obj['genus']} {wcvp_obj['species']}'''.strip().lower()
                        if wcvp_herb_name_scientific in herb_name_scientific:
                            found = True
                            print(f'#########################################')
                            print(f'FOUND: {herb_name_scientific}')
                            print(f'#########################################')
                            break
                    if not found: continue
                    ###
                    found = False
                    for output in output_list_tmp:
                        if output['herb_name_scientific'] == herb_name_scientific:
                            found = True
                            break
                    if not found:
                        _obj = {
                            "herb_name_scientific": herb_name_scientific, 
                            "herb_confidence_score": herb_confidence_score,
                        }
                        output_list_tmp.append(_obj)
                for output_tmp in output_list_tmp:
                    found = False
                    for output in output_list:
                        if output['herb_name_scientific'] == output_tmp['herb_name_scientific']:
                            found = True
                            output['herb_mentions'] += 1
                            output['herb_confidence_score'] += output_tmp['herb_confidence_score']
                            output['herb_grade'] = output['herb_confidence_score'] * output['herb_mentions']
                            break
                    if not found:
                        _obj = {
                            "herb_name_scientific": output_tmp['herb_name_scientific'], 
                            "herb_mentions": 1,
                            "herb_confidence_score": output_tmp['herb_confidence_score'],
                            "herb_grade": output_tmp['herb_confidence_score'] * 1,
                        }
                        output_list.append(_obj)
        output_list = sorted(output_list, key=lambda x: x['herb_grade'], reverse=True)
        for output in output_list:
            print(output)
        json_article[key] = output_list
        io.json_write(json_article_filepath, json_article)

def ai_llm_list_desc(obj, regen=False, dispel=False):
    json_article_filepath = f'''{g.database_folderpath}/json/{obj['url']}.json'''
    json_article = io.json_read(json_article_filepath)
    key = 'preparation_desc'
    for json_obj in json_article['preparations']:
        if key not in json_obj: 
            json_obj[key] = ''
        if dispel: 
            json_obj[key] = ''
            return
        if regen: 
            json_obj[key] = ''
        if json_obj[key] == '':
            prompt = f'''
                Write a detailed paragraph in 5 sentences about {json_obj['herb_name_scientific']} herbal {json_article['preparation_name_plural']} for {json_article['ailment_name']}.
            '''
            prompt += f'/no_think'
            reply = llm.reply(prompt).strip()
            if '</think>' in reply:
                reply = reply.split('</think>')[1].strip()
            reply = reply.replace('*', '')
            json_obj[key] = reply
            io.json_write(json_article_filepath, json_article)

def json_gen(obj):
    json_article_filepath = f'''{g.database_folderpath}/json/{obj['url']}.json'''
    json_article = io.json_read(json_article_filepath)
    json_article['url'] = obj['url']
    json_article['ailment_slug'] = obj['ailment_slug']
    json_article['ailment_name'] = obj['ailment_name']
    json_article['preparation_slug'] = obj['preparation_slug']
    json_article['preparation_name_singular'] = obj['preparation_name_singular']
    json_article['preparation_name_plural'] = obj['preparation_name_plural']
    json_article['main_lst_num'] = 10
    json_article['title'] = f'''10 best herbal {obj['preparation_name_plural']} for {obj['ailment_name']}'''
    io.json_write(json_article_filepath, json_article)
    ###
    ai_llm_intro(obj, regen=False, dispel=False)
    ai_llm_list_init(obj, regen=False, dispel=False)
    ai_llm_list_desc(obj, regen=False, dispel=False)

def html_gen(obj):
    json_article_filepath = f'''{g.database_folderpath}/json/{obj['url']}.json'''
    json_article = io.json_read(json_article_filepath)
    html_article = ''
    json_title = f'''{json_article['title']}'''
    meta_title = f'''{json_title}'''
    meta_description = f''
    html_article += f'''<h1>{json_title}</h1>'''
    html_article += f'''<p>{json_article['intro']}</p>'''
    for preparation_i, preparation in enumerate(json_article['preparations'][:10]):
        html_article += f'''<h2>{preparation_i+1}. {preparation['herb_name_scientific'].capitalize()}</h2>'''
        html_article += f'''<p>{preparation['preparation_desc']}</p>'''
    html = f'''
        <!DOCTYPE html>
        <html lang="en">
        {components.html_head(meta_title, meta_description)}
        <body>
            {components.html_header()}
            <main class="container-md article">
                {html_article}
            </main>
            <div class="mt-64"></div>
            {components.html_footer()}
        </body>
        </html>
    '''
    html_filepath = f'{g.website_folderpath}/index.html'
    with open(html_filepath, 'w') as f: f.write(html)

def gen():
    ailment_list = io.csv_to_dict(f'{g.database_folderpath}/csv/ailments.csv')
    preparation_list = io.csv_to_dict(f'{g.database_folderpath}/csv/preparations.csv')
    for ailment in ailment_list:
        ailment_slug = ailment['ailment_slug']
        ailment_name = ailment['ailment_name']
        organ_slug = ailment['organ_slug']
        system_slug = ailment['system_slug']
        for preparation in preparation_list:
            preparation_slug = preparation['preparation_slug']
            preparation_name_singular = preparation['preparation_name_singular']
            preparation_name_plural = preparation['preparation_name_plural']
            url = f'ailments/{ailment_slug}/{preparation_slug}'
            obj = {
                'url': url,
                'ailment_slug': ailment_slug,
                'ailment_name': ailment_name,
                'organ_slug': organ_slug,
                'system_slug': system_slug,
                'preparation_slug': preparation_slug,
                'preparation_name_singular': preparation_name_singular,
                'preparation_name_plural': preparation_name_plural,
            }
            json_gen(obj)
            html_gen(obj)
            quit()

