import os
import json
import random
import shutil
import time

from lib import g
from lib import io
from lib import llm
from lib import data
from lib import media
from lib import utils
from lib import polish
from lib import components
from lib import sections
from lib import zimage


def ai_llm_intro(obj, regen=False, dispel=False):
    json_article_filepath = f'''{g.database_folderpath}/json/{obj['url']}.json'''
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
        io.json_write(json_article_filepath, json_article)
        return
    if regen: 
        json_article[key] = []
    if json_article[key] == []:
        wcvp_dict = io.csv_to_dict(f'{g.database_folderpath}/csv/wcvp/wcvp_names.csv', '|')
        output_list = []
        for i in range(10):
            rnd_num = random.randint(10, 15)
            prompt = f'''
                Write a list of the {rnd_num} best herbal {obj['preparation_name_plural']} for {obj['ailment_name']}.
                Write only the scientific name of the herbs uses, not the type of preparation.
                By scientific name I mean botanical names in latin.
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
                    _herb_name_scientific = ''
                    for wcvp_obj in wcvp_dict:
                        wcvp_herb_name_scientific = f'''{wcvp_obj['genus']} {wcvp_obj['species']}'''.strip().lower()
                        if wcvp_herb_name_scientific in herb_name_scientific:
                            if len(wcvp_herb_name_scientific.split()) == 1: continue
                            _herb_name_scientific = wcvp_herb_name_scientific
                            found = True
                            print(f'#########################################')
                            print(f'FOUND: {herb_name_scientific}')
                            print(f'#########################################')
                            break
                    if not found: continue
                    ###
                    found = False
                    for output in output_list_tmp:
                        if output['herb_name_scientific'] == _herb_name_scientific:
                            found = True
                            break
                    if not found:
                        _obj = {
                            "herb_name_scientific": _herb_name_scientific, 
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
        json_article[key] = output_list[:10]
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
            io.json_write(json_article_filepath, json_article)
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
    json_article = io.json_read(json_article_filepath, create=True)
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

def image_ai_old(obj, clear=False):
    json_article_filepath = f'''{g.database_folderpath}/json/{obj['url']}.json'''
    json_article = io.json_read(json_article_filepath)
    preparation_slug = json_article['preparation_slug']
    preparation_name_singular = json_article['preparation_name_singular']
    preparation_name_plural = json_article['preparation_name_plural']
    preparation_list = json_article['preparations']
    for preparation_i, preparation in enumerate(preparation_list[:10]):
        herb_name_scientific = preparation['herb_name_scientific']
        herb_slug = herb_name_scientific.lower().strip().replace(' ', '-').replace('.', '')
        out_filepath = f'''{g.WEBSITE_FOLDERPATH}/images/preparations/{herb_slug}-{preparation_slug}.jpg'''
        print(f'{preparation_i}/{len(preparation_list)} - {out_filepath}')
        if clear:
            try: os.remove(out_filepath)
            except: pass
            continue
        if not os.path.exists(out_filepath):
        # if True:
            prompt = f'''
                herbal {preparation_name_plural} made with dry {herb_name_scientific},
                on a wooden table,
                rustic, vintage, boho,
                warm tones,
                high resolution,
            '''.replace('  ', ' ')
            image = media.image_gen(prompt, 1024, 1024)
            image = media.resize(image, 768, 768)
            # image.show()
            image.save(out_filepath)
        # quit()

def image_ai(obj, clear=False):
    json_article_filepath = f'''{g.database_folderpath}/json/{obj['url']}.json'''
    json_article = io.json_read(json_article_filepath)
    preparation_slug = json_article['preparation_slug']
    preparation_name_singular = json_article['preparation_name_singular']
    preparation_name_plural = json_article['preparation_name_plural']
    preparation_list = json_article['preparations']
    for preparation_i, preparation in enumerate(preparation_list[:10]):
        herb_name_scientific = preparation['herb_name_scientific']
        herb_slug = herb_name_scientific.lower().strip().replace(' ', '-').replace('.', '')
        out_filepath = f'''{g.WEBSITE_FOLDERPATH}/images/preparations/{herb_slug}-{preparation_slug}.jpg'''
        print(f'{preparation_i}/{len(preparation_list)} - {out_filepath}')
        if clear:
            try: os.remove(out_filepath)
            except: pass
            continue
        if not os.path.exists(out_filepath):
        # if True:
            prompt = f'''
                herbal {preparation_name_plural} made with dry {herb_name_scientific},
                on a wooden table,
                rustic, vintage, boho,
                warm tones,
                high resolution,
            '''.replace('  ', ' ')
            zimage.image_create(
                output_filepath=f'{out_filepath}', 
                prompt=prompt, width=768, height=768, seed=-1,
            )
            # image = media.image_gen(prompt, 1024, 1024)
            # image = media.resize(image, 768, 768)
            # image.show()
            # image.save(out_filepath)
        # quit()

def image_pil(obj):
    in_folderpath = f'''{g.database_folderpath}/images/preparations'''
    web_folderpath = f'''{g.website_folderpath}/images/preparations'''
    for in_filename in os.listdir(in_folderpath):
        in_filepath = f'''{in_folderpath}/{in_filename}'''
        web_filepath = f'''{web_folderpath}/{in_filename}'''
        print(in_filepath)
        print(web_filepath)
        print()
        shutil.copy2(in_filepath, web_filepath)

def html_gen(obj):
    json_article_filepath = f'''{g.database_folderpath}/json/{obj['url']}.json'''
    json_article = io.json_read(json_article_filepath)
    html_article = ''
    json_title = f'''{json_article['title']}'''
    meta_title = f'''{json_title}'''
    meta_description = f''
    html_article += f'''<h1>{json_title.title()}</h1>'''
    _preparation = json_article['preparations'][0]
    _herb_slug = _preparation['herb_name_scientific'].strip().lower().replace(' ', '-').replace('.', '')
    src = f'''/images/preparations/{json_article['preparation_slug']}/{_herb_slug}-{json_article['preparation_slug']}.jpg'''
    alt = f'''{_preparation['herb_name_scientific']} {json_article['preparation_name_singular']}'''
    # src = f'''/images/ailments/{json_article['ailment_slug']}-{json_article['preparation_slug']}.jpg'''
    # alt = f'''{json_article['ailment_name']} {json_article['preparation_name_singular']}'''
    html_article += f'''<img src="{src}" alt="{alt}">'''
    html_article += f'''{utils.format_1N1(json_article['intro'])}'''
    ### lead magnet
    form_head = ''
    if obj['preparation_slug'] == 'tinctures':
        with open(f'{g.ASSETS_FOLDERPATH}/scripts/newsletter/form-head.txt') as f: 
            form_head = f.read()
        with open(f'{g.ASSETS_FOLDERPATH}/scripts/newsletter/form-course-preparation-tincture.txt') as f: 
            form_body = f.read()
        if 0:
            html_article += f'''
                <div class="free-gift">
                    <p class="free-gift-heading">FREE COURSE</p>
                    <p style="text-align: center; margin-bottom: 1.6rem;">How to make medicinal herbal tinctures for common ailments at home and in a weekend (using the Healing Drops System).</p>
                    <img src="/images/shop/banner-course-preparation-tincture.jpg" alt="tincture preparation course banner">
                    {form_body}
                </div>
            '''
    else:
        with open(f'{g.ASSETS_FOLDERPATH}/scripts/newsletter/form-head.txt') as f: 
            form_head = f.read()
        with open(f'{g.ASSETS_FOLDERPATH}/scripts/newsletter/form-herb-drying-checklist.txt') as f: 
            form_body = f.read()
        if 0:
            html_article += f'''
                <div class="free-gift">
                    <p class="free-gift-heading">FREE Herb Drying Checklist</p>
                    <p style="text-align: center; margin-bottom: 1.6rem;">How to make sure every batch retains maximum flavor, color, and aroma without the risk of mold or over-drying. Eliminate guesswork and trial-and-error, making herb drying faster, easier, and more efficient every time.</p>
                    {form_body}
                </div>
            '''
    ### toc
    html_article += f'''[toc]'''
    ### sections
    for preparation_i, preparation in enumerate(json_article['preparations'][:10]):
        herb_name_scientific = preparation['herb_name_scientific'].capitalize()
        herb_slug = polish.sluggify(herb_name_scientific)
        herb_name_common = data.herb_name_common_get(herb_slug).capitalize()
        if herb_name_common != '':
            html_article += f'''<h2>{preparation_i+1}. {herb_name_common} ({herb_name_scientific})</h2>'''
        else:
            html_article += f'''<h2>{preparation_i+1}. {herb_name_scientific.capitalize()}</h2>'''
        src = f'''/images/preparations/{json_article['preparation_slug']}/{herb_slug}-{json_article['preparation_slug']}.jpg'''
        alt = f'''{preparation['herb_name_scientific']} {json_article['preparation_name_singular']}'''
        html_article += f'''<img src="{src}" alt="{alt}">'''
        html_article += f'''{utils.format_1N1(preparation['preparation_desc'])}'''
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

def gen():
    ailment_list = io.csv_to_dict(f'{g.database_folderpath}/csv/ailments.csv')
    preparation_list = io.csv_to_dict(f'{g.database_folderpath}/csv/preparations.csv')
    for ailment_i, ailment in enumerate(ailment_list):
        ailment_slug = ailment['ailment_slug']
        ailment_name = ailment['ailment_name']
        organ_slug = ailment['organ_slug']
        system_slug = ailment['system_slug']
        print(f'AILMENT: {ailment_i}/{len(ailment_list)} - {ailment_name}')
        for preparation_i, preparation in enumerate(preparation_list):
            preparation_slug = preparation['preparation_slug']
            preparation_name_singular = preparation['preparation_name_singular']
            preparation_name_plural = preparation['preparation_name_plural']
            ### TODO redo all these because accidentally deleted jsons
            # if preparation_slug != 'teas': continue
            # if preparation_slug != 'tinctures': continue
            # if preparation_slug != 'decoctions': continue
            # if preparation_slug != 'essential-oils': continue

            # if preparation_slug != 'creams': continue
            # if preparation_slug != 'syrups': continue
            # if preparation_slug != 'juices': continue
            # if preparation_slug != 'linctuses': continue

            # if preparation_slug != 'mucillages': continue
            # if preparation_slug != 'capsules': continue
            # if preparation_slug != 'lozenges': continue
            # if preparation_slug != 'baths': continue

            # if preparation_slug != 'lotions': continue
            print(f'PREPARATION: {preparation_slug}')
            try: os.mkdir(f'''{g.website_folderpath}/ailments''')
            except: pass
            try: os.mkdir(f'''{g.website_folderpath}/ailments/{ailment_slug}''')
            except: pass
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
            # image_ai(obj, clear=False)
            html_gen(obj)
            # quit()
    # image_pil(obj)

