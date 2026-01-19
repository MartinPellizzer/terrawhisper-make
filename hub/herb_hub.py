import os
import random

import lorem

from lib import g
from lib import io
from lib import llm
from lib import data
from lib import utils
from lib import polish
from lib import components
from lib import sections

herbs_primary_medicinal = data.herbs_primary_medicinal_get()
herbs_popular = data.herbs_popular_get('teas', 100)

def sitemaps_gen():
    sitemaps_folderpath = f'{g.WEBSITE_FOLDERPATH}/sitemaps'
    try: os.makedirs(sitemaps_folderpath)
    except: pass
    herbs_folderpath = f'{g.SSOT_FOLDERPATH}/herbs/herbs-wcvp/medicinal'
    filenames = []
    for filename in os.listdir(f'{herbs_folderpath}'):
        filename_base = filename.split('.')[0]
        filenames.append(f'{g.WEB_HERBS_URL}/{filename_base}.html')
    chunks = []
    chunk = []
    chunk_len = 0
    for filename in filenames:
        if chunk_len >= 40000:
            chunks.append(chunk)
            chunk = [filename]
            chunk_len = 0
        else:
            chunk.append(filename)
            chunk_len += 1
    if chunk_len != 0:
        chunks.append(chunk)
    print(chunks)
    print(len(filenames))
    print(len(chunks))
    # quit()
        
    for chunk_i, chunk in enumerate(chunks):
        sitemap = ''
        sitemap += '<?xml version="1.0" encoding="UTF-8"?>\n'
        sitemap += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        for filepath in chunk:
            sitemap += f'''
                <url>
                <loc>{filepath}</loc>
                </url>
            '''.strip() + '\n'
        sitemap += '</urlset>\n'
        io.file_write(f'{sitemaps_folderpath}/sitemap-herbs-wcvs-medicinal-{chunk_i}.xml', sitemap.strip())

def actions_clusters_get():
    clusters_actions = []
    for herb_i, herb in enumerate(herbs_popular[:]):
        print(f'HERB: {herb_i}/{len(herbs_popular[:])} - {herb}')
        herb_name_scientific = herb['herb_name_scientific']
        herb_name_scientific = polish.sanitize(herb_name_scientific)
        herb_slug = polish.sluggify(herb_name_scientific)
        json_filepath = f'{g.DATABASE_FOLDERPATH}/entities/herbs/{herb_slug}.json'
        try: json_article = io.json_read(json_filepath)
        except: print(herb_slug)
        herb_name_common = json_article['herb_name_common'][0]['answer']
        herb_therapeutic_actions = json_article['herb_therapeutic_actions']
        for x in herb_therapeutic_actions:
            print(x)
        # quit()
        for herb_therapeutic_action in herb_therapeutic_actions[:4]:
            herb_therapeutic_action_name = herb_therapeutic_action['answer'].strip().lower()
            found = False
            _obj = {
                'herb_name_scientific': herb_name_scientific,
                'herb_name_common': herb_name_common,
                'herb_image_src': f'''/images/herbs/{herb_slug}.jpg''',
                'herb_image_alt': f'''{herb_name_scientific}''',
            }
            for cluster_action in clusters_actions:
                if herb_therapeutic_action_name == cluster_action['name']:
                    cluster_action['herbs'].append(_obj)
                    found = True
                    break
            if not found:
                clusters_actions.append(
                    {
                        'name': herb_therapeutic_action_name,
                        'herbs': [_obj],
                    },
                )
    clusters_actions = sorted(clusters_actions, key=lambda x: x['name'], reverse=False)
    return clusters_actions

def herb_in_list(herbs_list, herb_obj):
    found = False
    for herb_list in herbs_list:
        if herb_obj['herb_name_scientific'] == herb_list['herb_name_scientific']:
            found = True
            break
    return found

def p2s(paragraph):
    html = ''
    sentences = [sentence for sentence in paragraph.split('.') if sentence.strip() != '']
    chunk_1 = '. '.join(sentences[:1]) + '.'
    chunk_2 = '. '.join(sentences[1:-1]) + '.'
    chunk_3 = '. '.join(sentences[-1:]) + '.'
    html += f'''<p>{chunk_1}</p>\n'''
    html += f'''<p>{chunk_2}</p>\n'''
    html += f'''<p>{chunk_3}</p>\n'''
    return html
    

def article_herbs_herb_primary_gen():
    herbs = []
    if 1:
        for herb in herbs_primary_medicinal: 
            # if not herb_in_list(herbs, herb):
            herbs.append({'herb_name_scientific': herb['herb_name_scientific']})
    if 1:
        for herb in herbs_popular: 
            # if not herb_in_list(herbs, herb):
            herbs.append({'herb_name_scientific': herb['herb_name_scientific']})
    # quit()
    for herb_i, herb in enumerate(herbs):
        herb_name_scientific = herb['herb_name_scientific']
        herb_name_scientific = polish.sanitize(herb_name_scientific)
        herb_slug = polish.sluggify(herb_name_scientific)
        url_slug = f'herbs/{herb_slug}'
        print(f'HERB: {herb_i}/{len(herbs)} - {herb_slug}')
        json_entity_filepath = f'''{g.DATABASE_FOLDERPATH}/ssot/herbs/herbs-primary/{herb_slug}.json'''
        json_entity = io.json_read(json_entity_filepath)
        herb_names_common = [name['answer'].title() for name in json_entity['herb_names_common']]
        herb_name_common = herb_names_common[0]
        # herb_family = json_entity['family'][0]['answer'].title()
        # herb_native_regions = [item['answer'].title() for item in json_entity['native_regions']]
        ########################################
        # json
        ########################################
        ### json init
        json_article_filepath = f'''{g.DATABASE_FOLDERPATH}/json/{url_slug}.json'''
        json_article = io.json_read(json_article_filepath, create=True)
        json_article['url'] = url_slug
        json_article['herb_slug'] = herb_slug
        json_article['herb_name_scientific'] = f'{herb_name_scientific}'
        json_article['title'] = f'{herb_name_common} ({herb_name_scientific})'
        io.json_write(json_article_filepath, json_article)
        ### json intro
        regen = False
        dispel = False
        key = 'intro'
        if key not in json_article: json_article[key] = ''
        if regen: json_article[key] = ''
        if dispel: 
            json_article[key] = ''
            io.json_write(json_article_filepath, json_article)
        if not dispel:
            if json_article[key] == '':
                prompt = f'''
                    Write a detailed paragraph in 5 sentences about {herb_name_common} ({herb_name_scientific}) for medicinal purposes.
                    Start with the following words: {herb_name_common}, scientifically know as {herb_name_scientific}, 
                '''
                prompt = f'''
                    Write a detailed paragraph in 5 sentences about {herb_name_common} ({herb_name_scientific}) for medicinal purposes.
                    Include a brief description about what it is (e.g., medicinal herb, adaptogen, spice, etc.).
                    Include primary benefits.
                    Include traditional/cultural uses.
                    Include modern wellness uses.
                    Include unique features (e.g., distinctive flavor, rare active compound, historical fact, etc.).
                    Start with the following words: {herb_name_common}, scientifically know as {herb_name_scientific}, is  
                '''
                prompt += f'/no_think'
                reply = llm.reply(prompt).strip()
                if '</think>' in reply:
                    reply = reply.split('</think>')[1].strip()
                reply = polish.vanilla(reply)
                json_article[key] = reply
                io.json_write(json_article_filepath, json_article)
        ### json botany
        regen = False
        dispel = False
        key = 'botany'
        if key not in json_article: json_article[key] = ''
        if regen: json_article[key] = ''
        if dispel: 
            json_article[key] = ''
            io.json_write(json_article_filepath, json_article)
        if not dispel:
            if json_article[key] == '':
                prompt_herb_names_common = ', '.join(herb_names_common)
                # prompt_herb_family = herb_family
                # prompt_herb_native_regions = ', '.join(herb_native_regions)
                if 0:
                    prompt_backup = f'''
                        Write a detailed paragraph in 5 sentences about the scientifi and botanical profile of {herb_name_common} ({herb_name_scientific}).
                        Include the following common names: {prompt_herb_names_common}.
                        Include the following family name: {prompt_herb_family}.
                        Include the following native regions: {prompt_herb_native_regions}.
                        Include a botanical (morphological) description.
                        Start with the following words: {herb_name_common}, with botanical name {herb_name_scientific}, 
                    '''
                prompt = f'''
                    Write a detailed paragraph in 5 sentences about the scientifi and botanical profile of {herb_name_common} ({herb_name_scientific}).
                    Include the following common names: {prompt_herb_names_common}.
                    Include the family name.
                    Include the native regions.
                    Include a botanical (morphological) description.
                    Start with the following words: {herb_name_common}, with botanical name {herb_name_scientific}, 
                '''
                prompt += f'/no_think'
                reply = llm.reply(prompt).strip()
                if '</think>' in reply:
                    reply = reply.split('</think>')[1].strip()
                reply = polish.vanilla(reply)
                json_article[key] = reply
                io.json_write(json_article_filepath, json_article)
        ### json history
        regen = False
        dispel = False
        key = 'history'
        if key not in json_article: json_article[key] = ''
        if regen: json_article[key] = ''
        if dispel: 
            json_article[key] = ''
            io.json_write(json_article_filepath, json_article)
        if not dispel:
            if json_article[key] == '':
                prompt = f'''
                    Write a detailed paragraph in 5 sentences about the history and cultural relevance of the plant {herb_name_common} ({herb_name_scientific}).
                    Include historical use in cultures / traditional medicine systems.
                    Include cultural significance or rituals, any ceremonies or folk traditions.
                    Include traditional remedies still relevant today, with examples.
                    Start with the following words: {herb_name_common} was used 
                '''
                prompt += f'/no_think'
                reply = llm.reply(prompt).strip()
                if '</think>' in reply:
                    reply = reply.split('</think>')[1].strip()
                reply = polish.vanilla(reply)
                json_article[key] = reply
                io.json_write(json_article_filepath, json_article)
        ### json chemistry
        regen = False
        dispel = False
        key = 'chemistry'
        if key not in json_article: json_article[key] = ''
        if regen: json_article[key] = ''
        if dispel: 
            json_article[key] = ''
            io.json_write(json_article_filepath, json_article)
        if not dispel:
            if json_article[key] == '':
                prompt = f'''
                    Write a detailed paragraph in 5 sentences about the chemical composition and nutritional profile of the plant {herb_name_common} ({herb_name_scientific}).
                    Include active compounds (e.g., alkaloids, flavonoids, essential oli, terpenes, etc.).
                    Include nutritional content (e.g., vitamins, minerals, antioxidants).
                    Include mechanism of action (how it works in the body.)
                    Start with the following words: {herb_name_common} contains
                '''
                prompt += f'/no_think'
                reply = llm.reply(prompt).strip()
                if '</think>' in reply:
                    reply = reply.split('</think>')[1].strip()
                reply = polish.vanilla(reply)
                json_article[key] = reply
                io.json_write(json_article_filepath, json_article)
        ### json benefits
        regen = False
        dispel = False
        key = 'benefits'
        if key not in json_article: json_article[key] = ''
        if regen: json_article[key] = ''
        if dispel: 
            json_article[key] = ''
            io.json_write(json_article_filepath, json_article)
        if not dispel:
            if json_article[key] == '':
                prompt = f'''
                    Write a detailed paragraph in 5 sentences about the medicinal properties and health benefits of the plant: {herb_name_scientific}.
                    Include body systems and benefits.
                    Include comparison with similar herbs (unique advantages, potency difference, etc.).
                    Start with the following words: {herb_name_scientific} has .
                '''
                prompt += f'/no_think'
                reply = llm.reply(prompt).strip()
                if '</think>' in reply:
                    reply = reply.split('</think>')[1].strip()
                reply = polish.vanilla(reply)
                json_article[key] = reply
                io.json_write(json_article_filepath, json_article)
        ### json preparations
        regen = False
        dispel = False
        key = 'preparations'
        if key not in json_article: json_article[key] = ''
        if regen: json_article[key] = ''
        if dispel: 
            json_article[key] = ''
            io.json_write(json_article_filepath, json_article)
        if not dispel:
            if json_article[key] == '':
                prompt = f'''
                    Write a detailed paragraph in 5 sentences about the form, preparations and usage of of the medicinal plant: {herb_name_scientific}.
                    Include forms available (fresh, dried tincture, powder, essential oil, capsule).
                    Include preparation methods (tea, decoction, infusion, topical).
                    Include recommended dosage (adult, child if safe).
                    Include frequency and duration of use (stay conservative).
                    Start with the following words: {herb_name_scientific} has .
                '''
                prompt += f'/no_think'
                reply = llm.reply(prompt).strip()
                if '</think>' in reply:
                    reply = reply.split('</think>')[1].strip()
                reply = polish.vanilla(reply)
                json_article[key] = reply
                io.json_write(json_article_filepath, json_article)
        ### json safety
        regen = False
        dispel = False
        key = 'safety'
        if key not in json_article: json_article[key] = ''
        if regen: json_article[key] = ''
        if dispel: 
            json_article[key] = ''
            io.json_write(json_article_filepath, json_article)
        if not dispel:
            if json_article[key] == '':
                prompt = f'''
                    Write a detailed paragraph in 5 sentences about the safety, side effects and contraindications of the medicinal plant: {herb_name_scientific}.
                    Include potential side effects.
                    Include drug or herb interactions.
                    Include special populations (pregnancy, breastfeeding, chronic illness) warnings
                    Include safety tips (advice for safe use).
                    Start with the following words: {herb_name_scientific} can .
                '''
                prompt += f'/no_think'
                reply = llm.reply(prompt).strip()
                if '</think>' in reply:
                    reply = reply.split('</think>')[1].strip()
                reply = polish.vanilla(reply)
                json_article[key] = reply
                io.json_write(json_article_filepath, json_article)
        ### json gardening
        regen = False
        dispel = False
        key = 'gardening'
        if key not in json_article: json_article[key] = ''
        if regen: json_article[key] = ''
        if dispel: 
            json_article[key] = ''
            io.json_write(json_article_filepath, json_article)
        if not dispel:
            if json_article[key] == '':
                prompt = f'''
                    Write a detailed paragraph in 5 sentences about growing, harvesting, and storage of the medicinal plant: {herb_name_scientific}.
                    Include planting conditions (soil, sun, water, etc.).
                    Include care and maintenance (tips, etc.).
                    Include harvesting method (best time, technique, etc.).
                    Include storage to preserve potency (drying, refrigeration, containers, etc.).
                    Start with the following words: {herb_name_scientific} grows  .
                '''
                prompt += f'/no_think'
                reply = llm.reply(prompt).strip()
                if '</think>' in reply:
                    reply = reply.split('</think>')[1].strip()
                reply = polish.vanilla(reply)
                json_article[key] = reply
                io.json_write(json_article_filepath, json_article)
        ### json faq
        regen = False
        dispel = False
        key = 'faq'
        if key not in json_article: json_article[key] = ''
        if regen: json_article[key] = ''
        if dispel: 
            json_article[key] = ''
            io.json_write(json_article_filepath, json_article)
        if not dispel:
            if json_article[key] == '':
                prompt = f'''
                    Write a detailed paragraph in 5 sentences about FAQ of the medicinal plant: {herb_name_scientific}.
                    Include can I grow {herb_name_scientific} at home?
                    Include how long does it take to work?
                    Include can it be combiend with other herbs?
                    Include is it safe long-term?
                    Include what's the best way to consume {herb_name_scientific}?
                    Start with the following words: {herb_name_scientific} .
                '''
                prompt += f'/no_think'
                reply = llm.reply(prompt).strip()
                if '</think>' in reply:
                    reply = reply.split('</think>')[1].strip()
                reply = polish.vanilla(reply)
                json_article[key] = reply
                io.json_write(json_article_filepath, json_article)
        ########################################
        # html
        ########################################
        json_title = f'''{json_article['title']}'''
        meta_title = f'''{json_title}'''
        meta_description = f''
        html_article = ''
        html_article += f'''<h1>{json_title.title()}</h1>'''
        html_article += f'''
            <div style="font-size: 1.4rem; line-height: 2.0rem; background-color: #f7f6f2; padding: 1.6rem; margin-bottom: 3.2rem;">
                <p style="font-size: 1.4rem; line-height: 2.0rem;">
                    <strong>Information Reliability Score: 5/10</strong>
                </p>
                <p style="font-size: 1.4rem; line-height: 2.0rem; margin: 0;">
                    This score reflects the overall reliability of the information presented in this article. It is based on the quality of scientific evidence, accuracy of sources, and the transparency of references related to {herb_name_scientific.capitalize()}.
                </p>
            </div>
        '''
        src = f'''/images/herbs/primary/{herb_slug}.jpg'''
        alt = f'''herbal {herb_name_common}'''
        html_article += f'''<img src="{src}" alt="{alt}">\n'''
        html_article += p2s(json_article['intro'])
        ### lead magnet
        form_head = ''
        form_body = ''
        with open(f'{g.DATABASE_FOLDERPATH}/assets/scripts/newsletter/form-head.txt') as f: form_head = f.read()
        with open(f'{g.DATABASE_FOLDERPATH}/assets/scripts/newsletter/form-course-preparation-tincture.txt') as f: 
            form_body_0000 = f.read()
        with open(f'{g.DATABASE_FOLDERPATH}/assets/scripts/newsletter/form-checklist-10-herbs-90-percent-ailments.txt') as f: 
            form_body_0001 = f.read()
        lead_magnets = [
            {
                'suptitle': 'FREE COURSE',
                'title': 'How to make medicinal herbl tinctures for common ailments at home and in a weekend (using the Healing Drop System).',
                'img_src': '/images/shop/banner-course-preparation-tincture.jpg',
                'img_alt': 'tincture preparation course banner',
                'form_body': form_body_0000,
            },
            {
                'suptitle': 'FREE CHECKLIST',
                'title': 'The Only 10 Herbs You Need to Heal 90% of Common Ailments.',
                'img_src': '/images/shop/checklist-10-herbs-90-percent-ailments-banner.jpg',
                'img_alt': '10 herbs that heals 90% of common ailments',
                'form_body': form_body_0001,
            },
        ]
        lead_magnet = random.choice(lead_magnets)
        if 0:
            html_article += f'''
                <div class="free-gift">
                    <p class="free-gift-heading">{lead_magnet['suptitle']}</p>
                    <p style="text-align: center; margin-bottom: 1.6rem;">{lead_magnet['title']}</p>
                    <img src="{lead_magnet['img_src']}" alt="{lead_magnet['img_alt']}">
                    {lead_magnet['form_body']}
                </div>
            '''
        ### toc
        html_article += f'''[toc]'''
        html_article += f'''<h2>Scientific and Botanical Profile</h2>'''
        # html_article += f'''{utils.format_1N1(json_article['botany'])}'''
        html_article += p2s(json_article['botany'])
        html_article += f'''<h2>History and Cultural Relevance</h2>'''
        html_article += p2s(json_article['history'])
        html_article += f'''<h2>Chemical Composition and Nutritional Profile</h2>'''
        html_article += p2s(json_article['chemistry'])
        html_article += f'''<h2>Medicinal Properties and Health Benefits</h2>'''
        html_article += p2s(json_article['benefits'])
        html_article += f'''<p>Discover the <a href="/herbs/{herb_slug}/benefits.html">10 best health benefits of {herb_name_common}</a>.</p>'''
        html_article += f'''<h2>Forms, Preparation and Usage</h2>'''
        html_article += p2s(json_article['preparations'])
        html_article += f'''<h2>Safety, Side Effects and Contraindications</h2>'''
        html_article += p2s(json_article['safety'])
        html_article += f'''<h2>Growing, Harvesting and Storage</h2>'''
        html_article += p2s(json_article['gardening'])
        # html_article += f'''<h2>FAQ</h2>'''
        # html_article += p2s(json_article['faq'])
        html_article = sections.toc(html_article)
        html = f'''
            <!DOCTYPE html>
            <html lang="en">
            {components.html_head(meta_title, meta_description, form_head)}
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
        html_filepath = f'''{g.website_folderpath}/{url_slug}.html'''
        with open(html_filepath, 'w') as f: f.write(html)
        # quit()

def article_herbs_herb_wcvp_gen():
    herbs_folderpath = f'{g.SSOT_FOLDERPATH}/herbs/herbs-wcvp/medicinal'
    herbs = [
        io.json_read(f'{herbs_folderpath}/{filename}')
        for filename in os.listdir(f'{herbs_folderpath}') 
    ]
    for herb_i, herb in enumerate(herbs):
        herb_name_scientific = herb['herb_name_scientific']
        herb_name_scientific = polish.sanitize(herb_name_scientific).capitalize()
        herb_slug = polish.sluggify(herb_name_scientific)
        url_slug = f'herbs/{herb_slug}'
        print(f'HERB: {herb_i}/{len(herbs)} - {herb_slug}')
        ###
        herb_names_common = [name['answer'].capitalize() for name in herb['herb_names_common']]
        herb_name_common = herb_names_common[0]
        herb_family = herb['herb_family'].capitalize()
        herb_origin_continents = [item['answer'].title() for item in herb['herb_origin_continents']]
        ########################################
        # json
        ########################################
        ### json init
        json_article_filepath = f'''{g.DATABASE_FOLDERPATH}/json/{url_slug}.json'''
        json_article = io.json_read(json_article_filepath, create=True)
        json_article['url'] = url_slug
        json_article['herb_slug'] = herb_slug
        json_article['herb_name_scientific'] = f'{herb_name_scientific}'
        json_article['herb_names_common'] = f'{herb_names_common}'
        json_article['herb_family'] = f'{herb_family}'
        json_article['title'] = f'{herb_name_common} ({herb_name_scientific})'
        io.json_write(json_article_filepath, json_article)
        ### json intro
        print(f'HERB: {herb_i}/{len(herbs)} - {herb_slug}')
        regen = False
        dispel = False
        key = 'intro'
        if key not in json_article: json_article[key] = ''
        if regen: json_article[key] = ''
        if dispel: 
            json_article[key] = ''
            io.json_write(json_article_filepath, json_article)
        if not dispel:
            if json_article[key] == '':
                prompt = f'''
                    Write a detailed paragraph in 5 sentences about {herb_name_common} ({herb_name_scientific}) for medicinal purposes.
                    Include a brief description about what it is (e.g., medicinal herb, adaptogen, spice, etc.).
                    Include primary benefits.
                    Include traditional/cultural uses.
                    Include modern wellness uses.
                    Include unique features (e.g., distinctive flavor, rare active compound, historical fact, etc.).
                    Start with the following words: {herb_name_common}, scientifically know as {herb_name_scientific}, is  
                '''
                prompt += f'/no_think'
                reply = llm.reply(prompt).strip()
                if '</think>' in reply:
                    reply = reply.split('</think>')[1].strip()
                reply = polish.vanilla(reply)
                json_article[key] = reply
                io.json_write(json_article_filepath, json_article)
        ### json botany
        print(f'HERB: {herb_i}/{len(herbs)} - {herb_slug}')
        regen = False
        dispel = False
        key = 'botany'
        if key not in json_article: json_article[key] = ''
        if regen: json_article[key] = ''
        if dispel: 
            json_article[key] = ''
            io.json_write(json_article_filepath, json_article)
        if not dispel:
            if json_article[key] == '':
                prompt_herb_names_common = ', '.join(herb_names_common)
                prompt_herb_family = herb_family
                prompt_herb_origin_continents = ', '.join(herb_origin_continents)
                prompt = f'''
                    Write a detailed paragraph in 5 sentences about the scientifi and botanical profile of {herb_name_common} ({herb_name_scientific}).
                    Include the following common names: {prompt_herb_names_common}.
                    Include the following family name: {prompt_herb_family}.
                    Include the following native regions: {prompt_herb_origin_continents}.
                    Include a botanical (morphological) description.
                    Start with the following words: {herb_name_common}, with botanical name {herb_name_scientific}, 
                '''
                prompt += f'/no_think'
                reply = llm.reply(prompt).strip()
                if '</think>' in reply:
                    reply = reply.split('</think>')[1].strip()
                reply = polish.vanilla(reply)
                json_article[key] = reply
                io.json_write(json_article_filepath, json_article)
        ### json history
        print(f'HERB: {herb_i}/{len(herbs)} - {herb_slug}')
        regen = False
        dispel = False
        key = 'history'
        if key not in json_article: json_article[key] = ''
        if regen: json_article[key] = ''
        if dispel: 
            json_article[key] = ''
            io.json_write(json_article_filepath, json_article)
        if not dispel:
            if json_article[key] == '':
                prompt = f'''
                    Write a detailed paragraph in 5 sentences about the history and cultural relevance of the plant {herb_name_common} ({herb_name_scientific}).
                    Include historical use in cultures / traditional medicine systems.
                    Include cultural significance or rituals, any ceremonies or folk traditions.
                    Include traditional remedies still relevant today, with examples.
                    Start with the following words: {herb_name_common} was used 
                '''
                prompt += f'/no_think'
                reply = llm.reply(prompt).strip()
                if '</think>' in reply:
                    reply = reply.split('</think>')[1].strip()
                reply = polish.vanilla(reply)
                json_article[key] = reply
                io.json_write(json_article_filepath, json_article)
        ### json chemistry
        print(f'HERB: {herb_i}/{len(herbs)} - {herb_slug}')
        regen = False
        dispel = False
        key = 'chemistry'
        if key not in json_article: json_article[key] = ''
        if regen: json_article[key] = ''
        if dispel: 
            json_article[key] = ''
            io.json_write(json_article_filepath, json_article)
        if not dispel:
            if json_article[key] == '':
                prompt = f'''
                    Write a detailed paragraph in 5 sentences about the chemical composition and nutritional profile of the plant {herb_name_common} ({herb_name_scientific}).
                    Include active compounds (e.g., alkaloids, flavonoids, essential oli, terpenes, etc.).
                    Include nutritional content (e.g., vitamins, minerals, antioxidants).
                    Include mechanism of action (how it works in the body.)
                    Start with the following words: {herb_name_common} contains
                '''
                prompt += f'/no_think'
                reply = llm.reply(prompt).strip()
                if '</think>' in reply:
                    reply = reply.split('</think>')[1].strip()
                reply = polish.vanilla(reply)
                json_article[key] = reply
                io.json_write(json_article_filepath, json_article)
        ### json benefits
        print(f'HERB: {herb_i}/{len(herbs)} - {herb_slug}')
        regen = False
        dispel = False
        key = 'benefits'
        if key not in json_article: json_article[key] = ''
        if regen: json_article[key] = ''
        if dispel: 
            json_article[key] = ''
            io.json_write(json_article_filepath, json_article)
        if not dispel:
            if json_article[key] == '':
                prompt = f'''
                    Write a detailed paragraph in 5 sentences about the medicinal properties and health benefits of the plant: {herb_name_scientific}.
                    Include body systems and benefits.
                    Include comparison with similar herbs (unique advantages, potency difference, etc.).
                    Start with the following words: {herb_name_scientific} has .
                '''
                prompt += f'/no_think'
                reply = llm.reply(prompt).strip()
                if '</think>' in reply:
                    reply = reply.split('</think>')[1].strip()
                reply = polish.vanilla(reply)
                json_article[key] = reply
                io.json_write(json_article_filepath, json_article)
        ### json preparations
        print(f'HERB: {herb_i}/{len(herbs)} - {herb_slug}')
        regen = False
        dispel = False
        key = 'preparations'
        if key not in json_article: json_article[key] = ''
        if regen: json_article[key] = ''
        if dispel: 
            json_article[key] = ''
            io.json_write(json_article_filepath, json_article)
        if not dispel:
            if json_article[key] == '':
                prompt = f'''
                    Write a detailed paragraph in 5 sentences about the form, preparations and usage of of the medicinal plant: {herb_name_scientific}.
                    Include forms available (fresh, dried tincture, powder, essential oil, capsule).
                    Include preparation methods (tea, decoction, infusion, topical).
                    Include recommended dosage (adult, child if safe).
                    Include frequency and duration of use (stay conservative).
                    Start with the following words: {herb_name_scientific} has .
                '''
                prompt += f'/no_think'
                reply = llm.reply(prompt).strip()
                if '</think>' in reply:
                    reply = reply.split('</think>')[1].strip()
                reply = polish.vanilla(reply)
                json_article[key] = reply
                io.json_write(json_article_filepath, json_article)
        ### json safety
        print(f'HERB: {herb_i}/{len(herbs)} - {herb_slug}')
        regen = False
        dispel = False
        key = 'safety'
        if key not in json_article: json_article[key] = ''
        if regen: json_article[key] = ''
        if dispel: 
            json_article[key] = ''
            io.json_write(json_article_filepath, json_article)
        if not dispel:
            if json_article[key] == '':
                prompt = f'''
                    Write a detailed paragraph in 5 sentences about the safety, side effects and contraindications of the medicinal plant: {herb_name_scientific}.
                    Include potential side effects.
                    Include drug or herb interactions.
                    Include special populations (pregnancy, breastfeeding, chronic illness) warnings
                    Include safety tips (advice for safe use).
                    Start with the following words: {herb_name_scientific} can .
                '''
                prompt += f'/no_think'
                reply = llm.reply(prompt).strip()
                if '</think>' in reply:
                    reply = reply.split('</think>')[1].strip()
                reply = polish.vanilla(reply)
                json_article[key] = reply
                io.json_write(json_article_filepath, json_article)
        ### json gardening
        print(f'HERB: {herb_i}/{len(herbs)} - {herb_slug}')
        regen = False
        dispel = False
        key = 'gardening'
        if key not in json_article: json_article[key] = ''
        if regen: json_article[key] = ''
        if dispel: 
            json_article[key] = ''
            io.json_write(json_article_filepath, json_article)
        if not dispel:
            if json_article[key] == '':
                prompt = f'''
                    Write a detailed paragraph in 5 sentences about growing, harvesting, and storage of the medicinal plant: {herb_name_scientific}.
                    Include planting conditions (soil, sun, water, etc.).
                    Include care and maintenance (tips, etc.).
                    Include harvesting method (best time, technique, etc.).
                    Include storage to preserve potency (drying, refrigeration, containers, etc.).
                    Start with the following words: {herb_name_scientific} grows  .
                '''
                prompt += f'/no_think'
                reply = llm.reply(prompt).strip()
                if '</think>' in reply:
                    reply = reply.split('</think>')[1].strip()
                reply = polish.vanilla(reply)
                json_article[key] = reply
                io.json_write(json_article_filepath, json_article)
        ### json faq
        print(f'HERB: {herb_i}/{len(herbs)} - {herb_slug}')
        regen = False
        dispel = False
        key = 'faq'
        if key not in json_article: json_article[key] = ''
        if regen: json_article[key] = ''
        if dispel: 
            json_article[key] = ''
            io.json_write(json_article_filepath, json_article)
        if not dispel:
            if json_article[key] == '':
                prompt = f'''
                    Write a detailed paragraph in 5 sentences about FAQ of the medicinal plant: {herb_name_scientific}.
                    Include can I grow {herb_name_scientific} at home?
                    Include how long does it take to work?
                    Include can it be combiend with other herbs?
                    Include is it safe long-term?
                    Include what's the best way to consume {herb_name_scientific}?
                    Start with the following words: {herb_name_scientific} .
                '''
                prompt += f'/no_think'
                reply = llm.reply(prompt).strip()
                if '</think>' in reply:
                    reply = reply.split('</think>')[1].strip()
                reply = polish.vanilla(reply)
                json_article[key] = reply
                io.json_write(json_article_filepath, json_article)
        ########################################
        # html
        ########################################
        json_title = f'''{json_article['title']}'''
        meta_title = f'''{json_title}'''
        meta_description = f''
        html_article = ''
        html_article += f'''<h1>{json_title.title()}</h1>'''
        html_article += f'''
            <div style="font-size: 1.4rem; line-height: 2.0rem; background-color: #f7f6f2; padding: 1.6rem; margin-bottom: 3.2rem;">
                <p style="font-size: 1.4rem; line-height: 2.0rem;">
                    <strong>Information Reliability Score: 2/10</strong>
                </p>
                <p style="font-size: 1.4rem; line-height: 2.0rem; margin: 0;">
                    This score reflects the overall reliability of the information presented in this article. It is based on the quality of scientific evidence, accuracy of sources, and the transparency of references related to {herb_name_scientific.capitalize()}.
                </p>
            </div>
        '''
        src = f'''/images/herbs/{herb_slug}.jpg'''
        alt = f'''herbal {herb_name_common}'''
        # html_article += f'''<img src="{src}" alt="{alt}">'''
        # html_article += f'''{utils.format_1N1(json_article['intro'])}'''
        html_article += f'''{json_article['intro']}'''
        ### lead magnet
        form_head = ''
        with open(f'{g.DATABASE_FOLDERPATH}/assets/scripts/newsletter/form-head.txt') as f: form_head = f.read()
        form_body = ''
        html_article += components.html_lead_magnet_random()
        html = f'''
            <!DOCTYPE html>
            <html lang="en">
            {components.html_head(meta_title, meta_description, form_head)}
            <body>
                {sections.header()}
                {sections.breadcrumbs(url_slug)}
                <main class="container-md article">
                    {html_article}
                </main>
                <div style="margin-bottom: 6.4rem;"></div>
                {sections.footer()}
            </body>
            </html>
        '''
        html_filepath = f'''{g.website_folderpath}/{url_slug}.html'''
        with open(html_filepath, 'w') as f: f.write(html)
        print(html_filepath)
        # quit()

def category_herbs_popular_gen():
    herbs_popular_num = 100
    herbs_popular = data.herbs_popular_get('teas', herbs_popular_num)
    ###
    url_slug = f'herbs/popular'
    html_filepath = f'''{g.website_folderpath}/{url_slug}.html'''
    ### page main
    html_herbs_popular_grid = f''
    for herb_i, herb in enumerate(herbs_popular[:herbs_popular_num]):
        print(f'HERB: {herb_i}/{len(herbs_popular[:herbs_popular_num])} - {herb}')
        herb_name_scientific = herb['herb_name_scientific']
        herb_name_scientific = polish.sanitize(herb_name_scientific)
        herb_slug = polish.sluggify(herb_name_scientific)
        json_filepath = f'{g.DATABASE_FOLDERPATH}/entities/herbs/{herb_slug}.json'
        try: json_article = io.json_read(json_filepath)
        except: print(herb_slug)
        herb_name_common = json_article['herb_name_common'][0]['answer']
        src = f'''/images/herbs/{herb_slug}.jpg'''
        alt = f'''{herb_name_scientific}'''
        html_herbs_popular_grid += f'''
            <div class="card-default">
                <a href="/herbs/{herb_slug}.html">
                    <img src="{src}" alt="{alt}" style="margin-bottom: 0.8rem;">
                    <h3 style="margin-bottom: 0.8rem;">{herb_name_common.title()}</h3>
                    <p style="font-size: 1.4rem; background-color: #f7f6f2; padding: 0.4rem 1.6rem; border-radius: 9999px;"><em>Latin Name: {herb_name_scientific.capitalize()}</em></p>
                </a>
            </div>
        '''
    section_py = '12.8rem'
    html_main = f''
    html_main += f'''
        <section style="padding-top: {section_py}; padding-bottom: {section_py};">
            <h1 style="margin-bottom: 1.6rem; text-align: center;">{herbs_popular_num} Most Popular Healing Herbs</h1>
            <p class="container-md" style="margin-bottom: 9.6rem; text-align: center; font-size: 2.4rem; line-height: 3.2rem;">
                Discover what are the top 100 medicial plants used by home herbalists all around the world for common ailments.
            </p>
            <div class="grid-4" style="gap: 3.2rem;">
                {html_herbs_popular_grid}
            </div>
        </section>
        <div style="width: 100%; height: 1px; background-color: #f2f2f2;"></div>
        <section style="padding-top: {section_py}; padding-bottom: {section_py};">
            <h2 style="font-size: 3.2rem; line-height: 1.3; font-weight: normal; margin-bottom: 3.2rem;">Join the Apothecary Letter</h2>
            <p>If you feel alone in your herbal healing journey, enter your best email below and I'll send you weekly emails where I'll take you by the hand and guide you towards the joys of herbalism.</p>
        </section>
    '''
    meta_title = f'''Popular Healing Herbs'''
    meta_description = f''''''
    html = f'''
        <!DOCTYPE html>
        <html lang="en">
        {components.html_head(meta_title, meta_description)}
        <body>
            {sections.header()}
            {sections.breadcrumbs(url_slug)}
            <main class="container-xl">
                {html_main}
            </main>
            {sections.footer()}
        </body>
        </html>
    '''
    with open(html_filepath, 'w') as f: f.write(html)

def category_herbs_actions_gen():
    herbs_popular_num = 100
    herbs_popular = data.herbs_popular_get('teas', herbs_popular_num)
    ###
    url_slug = f'herbs/actions'
    html_filepath = f'''{g.website_folderpath}/{url_slug}.html'''
    ### cluster actions
    clusters_actions = []
    for herb_i, herb in enumerate(herbs_popular[:herbs_popular_num]):
        print(f'HERB: {herb_i}/{len(herbs_popular[:herbs_popular_num])} - {herb}')
        herb_name_scientific = herb['herb_name_scientific']
        herb_name_scientific = polish.sanitize(herb_name_scientific)
        herb_slug = polish.sluggify(herb_name_scientific)
        json_filepath = f'{g.DATABASE_FOLDERPATH}/entities/herbs/{herb_slug}.json'
        try: json_article = io.json_read(json_filepath)
        except: print(herb_slug)
        herb_name_common = json_article['herb_name_common'][0]['answer']
        herb_therapeutic_actions = json_article['herb_therapeutic_actions']
        for x in herb_therapeutic_actions:
            print(x)
        # quit()
        for herb_therapeutic_action in herb_therapeutic_actions[:4]:
            herb_therapeutic_action_name = herb_therapeutic_action['answer'].strip().lower()
            found = False
            _obj = {
                'herb_name_scientific': herb_name_scientific,
                'herb_name_common': herb_name_common,
                'herb_image_src': f'''/images/herbs/{herb_slug}.jpg''',
                'herb_image_alt': f'''{herb_name_scientific}''',
            }
            for cluster_action in clusters_actions:
                if herb_therapeutic_action_name == cluster_action['name']:
                    cluster_action['herbs'].append(_obj)
                    found = True
                    break
            if not found:
                clusters_actions.append(
                    {
                        'name': herb_therapeutic_action_name,
                        'herbs': [_obj],
                    },
                )
    clusters_actions = sorted(clusters_actions, key=lambda x: x['name'], reverse=False)
    # for cluster_action in clusters_actions[:10]:
        # print(cluster_action)
    ### html clusters
    html_clusters_actions = f''
    for cluster_action in clusters_actions:
        print(cluster_action)
        # quit()
        html_herbs_actions_grid = f''
        herbs_num = 4
        herbs = cluster_action['herbs'][:herbs_num]
        for herb_i, herb in enumerate(herbs):
            print(f'HERB: {herb_i}/{len(herbs[:herbs_num])} - {herb}')
            herb_name_scientific = herb['herb_name_scientific']
            herb_name_scientific = polish.sanitize(herb_name_scientific)
            herb_slug = polish.sluggify(herb_name_scientific)
            json_filepath = f'{g.DATABASE_FOLDERPATH}/entities/herbs/{herb_slug}.json'
            try: json_article = io.json_read(json_filepath)
            except: print(herb_slug)
            herb_name_common = json_article['herb_name_common'][0]['answer']
            herb_therapeutic_actions = json_article['herb_therapeutic_actions']
            herb_therapeutic_action = herb_therapeutic_actions[0]['answer']
            src = f'''/images/herbs/{herb_slug}.jpg'''
            alt = f'''{herb_name_scientific}'''
            html_herbs_actions_grid += f'''
                <div class="card-default">
                    <a href="/herbs/{herb_slug}.html">
                        <img src="{src}" alt="{alt}" style="margin-bottom: 0.8rem;">
                        <h3 style="margin-bottom: 0.8rem;">{herb_name_common.title()}</h3>
                        <p style="font-size: 1.4rem; background-color: #f7f6f2; padding: 0.4rem 1.6rem; border-radius: 9999px;"><em>Latin Name: {herb_name_scientific.capitalize()}</em></p>
                    </a>
                </div>
            '''
        html = f'''
            <div style="margin-bottom: 9.6rem;">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <h2 style="font-size: 4.8rem; line-height: 1; margin-bottom: 3.2rem;">{cluster_action['name'].capitalize()}</h2>
                    <p><a href="/herbs/popular.html">View All</a></p>
                </div>
                <div class="grid-4" style="gap: 3.2rem;">
                    {html_herbs_actions_grid}
                </div>
            </div>
        '''
        html_clusters_actions += html
    section_py = '12.8rem'
    html_main = f'''
        <section style="padding-top: {section_py}; padding-bottom: {section_py};">
            <h1 class="container-lg" style="margin-bottom: 1.6rem; text-align: center;">{len(clusters_actions)} Therapeutic Actions of Healing Herbs</h1>
            <p class="container-md" style="margin-bottom: 9.6rem; text-align: center; font-size: 2.4rem; line-height: 3.2rem;">
                The sections below show the most important therapeutic actions of healing herbs for the human body.
            </p>
            {html_clusters_actions}
        </section>
        <div style="width: 100%; height: 1px; background-color: #f2f2f2;"></div>
        <section style="padding-top: {section_py}; padding-bottom: {section_py};">
            <h2 style="font-size: 3.2rem; line-height: 1.3; font-weight: normal; margin-bottom: 3.2rem;">Join the Apothecary Letter</h2>
            <p>If you feel alone in your herbal healing journey, enter your best email below and I'll send you weekly emails where I'll take you by the hand and guide you towards the joys of herbalism.</p>
        </section>
    '''
    meta_title = f'''Therapeutic Actions of Healing Herbs'''
    meta_description = f''''''
    html = f'''
        <!DOCTYPE html>
        <html lang="en">
        {components.html_head(meta_title, meta_description)}
        <body>
            {sections.header()}
            {sections.breadcrumbs(url_slug)}
            <main class="container-xl">
                {html_main}
            </main>
            {sections.footer()}
        </body>
        </html>
    '''
    with open(html_filepath, 'w') as f: f.write(html)

### split a list of items in groups
### the number of element x groups is given by "group_len"
### this function is being used for "pagination purposes"
def groups_gen(items, group_len):
    pages = []
    page_cur = []
    for item_i, item in enumerate(items):
        if len(page_cur) < group_len:
            page_cur.append(item)
        else:
            pages.append(page_cur)
            page_cur = [item]
    if page_cur != []: pages.append(page_cur)
    return pages

def card_primary_gen(i, card_img_src, herb_slug, card_title, card_desc):
    ###
    card_padding_right = ''
    card_padding_left = ''
    card_margin_right = ''
    card_margin_left = ''
    card_border_right = ''
    if i % 3 == 0:
        card_padding_right = 'padding-right: 3.2rem;';
        card_border_right = 'border-right: 1px solid #e7e7e7; '
    if i % 3 == 1:
        card_padding_right = 'padding-right: 3.2rem;';
        card_padding_left = 'padding-left: 3.2rem;';
        card_border_right = 'border-right: 1px solid #e7e7e7; '
    elif i % 3 == 2:
        card_padding_left = 'padding-left: 3.2rem;';
        card_border_right = ''
    ###
    html_card = f'''
        <div style="border-bottom: 1px solid #e7e7e7; padding-bottom: 3.2rem; margin-bottom: 3.2rem;">
            <div style="{card_border_right}{card_padding_right}{card_padding_left}{card_margin_right}{card_margin_left}">
                <div style="">
                    <img 
                        style="margin-bottom: 1.6rem; height: 24rem; object-fit: cover;"
                        src="{card_img_src}"
                    >
                    <p style="margin-bottom: 1.6rem; font-size: 1.2rem; font-weight: bold; letter-spacing: 1px; color: #aaaaaa;">JULY 30, 2024</p>
                    <h2><a style="color: #111111; text-decoration: none;" href="/herbs/{herb_slug}.html">{card_title}</a></h2>
                    <p style="margin-bottom: 1.6rem;">{card_desc}</p>
                    <p><a style="color: #111111; font-weight: bold; font-size: 1.4rem; letter-spacing: 0.5px;" href="/herbs/{herb_slug}.html">READ MORE</a></p>
                </div>
            </div>
        </div>
    '''
    return html_card

def sidebar_gen():
    ###
    sidebar_cards_html = ''
    for i in range(4):
        herb = herbs_primary_medicinal[i+10]
        herb_slug = herb['herb_slug']
        herb_name_scientific = herb['herb_name_scientific']
        ###
        card_title = herb_name_scientific.capitalize()
        card_desc = ' '.join(lorem.paragraph().split(' ')[:8])
        card_img_src = f'/images/herbs/primary/{herb_slug}.jpg'
        html_card = f'''
            <div style="display: flex; gap: 2.4rem; margin-bottom: 2.4rem; padding-bottom: 1.6rem; border-bottom: 1px solid #e7e7e7;">
                <div style="flex: 1;">
                    <img 
                        style="height: 10rem; object-fit: cover;"
                        src="{card_img_src}"
                    >
                </div>
                <div style="flex: 2;">
                    <p style="margin-bottom: 1.6rem; font-size: 1.2rem; font-weight: bold; letter-spacing: 1px; color: #aaaaaa;">JULY 30, 2024</p>
                    <h3 style="font-size: 1.6rem; font-weight: 400;">{card_title}</h3>
                </div>
            </div>
        '''
        sidebar_cards_html += html_card
    html_sidebar = f'''
        <div style="padding-right: 4.8rem;">
            <img 
                style="margin-bottom: 1.6rem; height: 40rem; object-fit: cover; object-position: top;"
                src="{card_img_src}"
            >
            <p style="margin-bottom: 4.8rem;">{card_desc}</p>
            <h2 style="font-size: 1.8rem;">Recent Posts</h2>
            {sidebar_cards_html}
            <img 
                style="margin-bottom: 1.6rem; height: 40rem; object-fit: cover; object-position: top;"
                src="{card_img_src}"
            >
        </div>
    '''
    return html_sidebar

def page_herbs_gen_old():
    if 0:
        html_herbs = f''
        ### category herbs primary medicinal
        for herb_i, herb in enumerate(herbs_primary_medicinal):
            print(f'HERB: {herb_i}/{len(herbs_primary_medicinal)} - {herb}')
            herb_slug = herb['herb_slug']
            herb_name_scientific = herb['herb_name_scientific']
            json_article = io.json_read(f'{g.DATABASE_FOLDERPATH}/entities/herbs/{herb_slug}.json')
            herb_name_common = json_article['herb_name_common'][0]['answer']
            src = f'''/images/herbs/primary/{herb_slug}.jpg'''
            alt = f'''{herb_name_scientific}'''
            html_herbs += f'''
                <div class="card-default">
                    <a href="/{url_slug}/{herb_slug}.html">
                        <img src="{src}" alt="{alt}">
                        <h2>{herb_name_common} ({herb_name_scientific.title()})</h2>
                    </a>
                </div>
            '''
        ### category herbs popular
        html_herbs_popular_grid = f''
        herbs_popular_num = 4
        for herb_i, herb in enumerate(herbs_popular[:herbs_popular_num]):
            print(f'HERB: {herb_i}/{len(herbs_popular[:herbs_popular_num])} - {herb}')
            herb_name_scientific = herb['herb_name_scientific']
            herb_name_scientific = polish.sanitize(herb_name_scientific)
            herb_slug = polish.sluggify(herb_name_scientific)
            json_filepath = f'{g.DATABASE_FOLDERPATH}/entities/herbs/{herb_slug}.json'
            try: json_article = io.json_read(json_filepath)
            except: print(herb_slug)
            herb_name_common = json_article['herb_name_common'][0]['answer']
            src = f'''/images/herbs/primary/{herb_slug}.jpg'''
            alt = f'''{herb_name_scientific}'''
            html_herbs_popular_grid += f'''
                <div class="card-default">
                    <a href="/{url_slug}/{herb_slug}.html">
                        <img src="{src}" alt="{alt}" style="margin-bottom: 0.8rem;">
                        <h3 style="margin-bottom: 0.8rem;">{herb_name_common.title()}</h3>
                        <p style="font-size: 1.4rem; background-color: #f7f6f2; padding: 0.4rem 1.6rem; border-radius: 9999px;"><em>Latin Name: {herb_name_scientific.capitalize()}</em></p>
                    </a>
                </div>
            '''
        html_herbs_popular = f'''
            <div style="margin-bottom: 9.6rem;">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <h2 style="font-size: 4.8rem; line-height: 1; margin-bottom: 3.2rem;">Popular</h2>
                    <p><a href="/herbs/popular.html">View All</a></p>
                </div>
                <div class="grid-4" style="gap: 3.2rem;">
                    {html_herbs_popular_grid}
                </div>
            </div>
        '''
        ### category herbs actions
        actions_clusters = actions_clusters_get()
        html_herbs_grid = f''
        herbs_num = 4
        for cluster_i, cluster in enumerate(actions_clusters[:herbs_num]):
            print(f'HERB: {cluster_i}/{len(actions_clusters[:herbs_num])} - {cluster}')
            cluster_name = cluster['name']
            cluster_herbs = cluster['herbs']
            cluster_herb = random.choice(cluster_herbs)
            herb_name_scientific = cluster_herb['herb_name_scientific']
            herb_name_scientific = polish.sanitize(herb_name_scientific)
            herb_slug = polish.sluggify(herb_name_scientific)
            json_filepath = f'{g.DATABASE_FOLDERPATH}/entities/herbs/{herb_slug}.json'
            try: json_article = io.json_read(json_filepath)
            except: print(herb_slug)
            herb_name_common = json_article['herb_name_common'][0]['answer']
            herb_image_src = f'''/images/herbs/primary/{herb_slug}.jpg'''
            herb_image_alt = f'''{herb_name_scientific}'''
            html_herbs_grid += f'''
                <div class="card-default">
                    <a href="/{url_slug}/{herb_slug}.html">
                        <img src="{herb_image_src}" alt="{herb_image_alt}" style="margin-bottom: 0.8rem;">
                        <h3 style="margin-bottom: 0.8rem;">{cluster_name.title()}</h3>
                    </a>
                </div>
            '''
        html_herbs_actions = f'''
            <div style="margin-bottom: 9.6rem;">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <h2 style="font-size: 4.8rem; line-height: 1; margin-bottom: 3.2rem;">Therapeutic Actions</h2>
                    <p><a href="/herbs/actions.html">View All</a></p>
                </div>
                <div class="grid-4" style="gap: 3.2rem;">
                    {html_herbs_grid}
                </div>
            </div>
        '''
        ### page main
        html_main += f'''
            <div>
                <h1 style="margin-bottom: 9.6rem;">Medicinal Herbs For Natural Healing</h1>
                {html_herbs_popular}
                {html_herbs_actions}
            </div>
        '''
                # <div class="grid-3" style="gap: 3.2rem;">
                    # {html_herbs}
                # </div>
    if 0:
        html = f'''
            <!DOCTYPE html>
            <html lang="en">
            <head>
              <meta charset="UTF-8">
              <title>Blog Layout</title>
              <link rel="stylesheet" href="styles-tmp.css">
            </head>
            <body>
            <div class="container">
              <!-- SIDEBAR -->
              <aside class="sidebar">
                <div class="widget">
                  <h3>About Author</h3>
                  <img src="https://picsum.photos/400/450?random=1" alt="Author">
                  <p>
                    There are many variations of passages of Lorem Ipsum available,
                    but the majority have suffered alteration in some form.
                  </p>
                </div>
                <div class="widget">
                  <h3>Recent Post</h3>
                  <div class="recent-post">
                    <img src="https://picsum.photos/80/80?random=2">
                    <div>
                      <span class="date">July 30, 2024</span>
                      <p>Treat your makeup like jewelry for the face</p>
                    </div>
                  </div>
                  <div class="recent-post">
                    <img src="https://picsum.photos/80/80?random=3">
                    <div>
                      <span class="date">July 30, 2024</span>
                      <p>Glowing skin is a result of proper skincare</p>
                    </div>
                  </div>
                  <div class="recent-post">
                    <img src="https://picsum.photos/80/80?random=4">
                    <div>
                      <span class="date">July 30, 2024</span>
                      <p>5 Steps to Mastering the Bold Red Lip</p>
                    </div>
                  </div>
                </div>
              </aside>
              <!-- MAIN CONTENT -->
              <main class="content">
                <!-- FILTER TABS -->
                <nav class="tabs">
                  <a class="active">ALL</a>
                  <a>COMPANY NEWS</a>
                  <a>FEATURED</a>
                  <a>GUIDE</a>
                  <a>RECIPE</a>
                  <a>UNCATEGORIZED</a>
                </nav>
                <!-- BLOG GRID -->
                <div class="grid">
                  <article class="card">
                    <img src="https://picsum.photos/600/400?random=5">
                    <div class="card-body">
                      <span class="meta">ADMIN · JULY 30, 2024</span>
                      <h2>Treat Your Makeup Like Jewelry For The Face</h2>
                      <p>
                        Amet minim mollit non deserunt ullamco est sit aliqua dolor.
                      </p>
                      <a href="#">READ MORE</a>
                    </div>
                  </article>
                  <article class="card">
                    <img src="https://picsum.photos/600/400?random=6">
                    <div class="card-body">
                      <span class="meta">ADMIN · JULY 30, 2024</span>
                      <h2>Glowing Skin Is A Result Of Proper Skincare</h2>
                      <p>
                        Amet minim mollit non deserunt ullamco est sit aliqua dolor.
                      </p>
                      <a href="#">READ MORE</a>
                    </div>
                  </article>
                  <article class="card">
                    <img src="https://picsum.photos/600/400?random=7">
                    <div class="card-body">
                      <span class="meta">ADMIN · JULY 30, 2024</span>
                      <h2>5 Steps To Mastering The Bold Red Lip</h2>
                      <p>
                        Amet minim mollit non deserunt ullamco est sit aliqua dolor.
                      </p>
                      <a href="#">READ MORE</a>
                    </div>
                  </article>
                  <article class="card">
                    <img src="https://picsum.photos/600/400?random=8">
                    <div class="card-body">
                      <span class="meta">ADMIN · JULY 30, 2024</span>
                      <h2>I Believe That All Women Are Pretty Without Makeup</h2>
                      <p>
                        Amet minim mollit non deserunt ullamco est sit aliqua dolor.
                      </p>
                      <a href="#">READ MORE</a>
                    </div>
                  </article>
                  <article class="card">
                    <img src="https://picsum.photos/600/400?random=9">
                    <div class="card-body">
                      <span class="meta">ADMIN · JULY 30, 2024</span>
                      <h2>Chocolate Bread With Drinking Chocolate Crumbles</h2>
                      <p>
                        Amet minim mollit non deserunt ullamco est sit aliqua dolor.
                      </p>
                      <a href="#">READ MORE</a>
                    </div>
                  </article>
                  <article class="card">
                    <img src="https://picsum.photos/600/400?random=10">
                    <div class="card-body">
                      <span class="meta">ADMIN · JULY 30, 2024</span>
                      <h2>When The Eye Makes A Statement, The Lips Should</h2>
                      <p>
                        Amet minim mollit non deserunt ullamco est sit aliqua dolor.
                      </p>
                      <a href="#">READ MORE</a>
                    </div>
                  </article>
                </div>
              </main>
            </div>
            </body>
            </html>
        '''

def page_herbs_gen():
    groups = groups_gen(herbs_primary_medicinal, 15)
    for group_i, group in enumerate(groups):
        url_slug = f'herbs'
        ### page url
        if group_i == 0:
            html_filepath = f'''{g.website_folderpath}/{url_slug}.html'''
        else:
            try: os.makedirs(f'''{g.website_folderpath}/{url_slug}/page''')
            except: pass
            html_filepath = f'''{g.website_folderpath}/{url_slug}/page/{group_i+1}.html'''
        ###
        html_main = f''
        html_title = f'''
            <section class="container-xl" style="margin-bottom: 9.6rem;">
                {sections.breadcrumbs(url_slug)}
                <h1 style="margin-top: 4.8rem;">Medicinal Herbs</h1>
            </section>
        '''
        ###
        html_cards = ''
        for i in range(len(group)):
            herb = group[i]
            herb_slug = herb['herb_slug']
            herb_name_scientific = herb['herb_name_scientific']
            ###
            card_title = herb_name_scientific.capitalize()
            card_desc = ' '.join(lorem.paragraph().split(' ')[:16]) + '...'
            card_img_src = f'/images/herbs/primary/{herb_slug}.jpg'
            ###
            html_card = card_primary_gen(i, card_img_src, herb_slug, card_title, card_desc)
            html_cards += html_card
        ###
        html_sidebar = sidebar_gen()
        ###
        meta_title = f'''Herbs'''
        meta_description = f''''''

        ### PAGINATION
        ########################################
        ### prev
        if group_i > 1:
            prev_html = f'''
                <a style="text-decoration: none;" href="/{url_slug}/page/{group_i}.html">
                    <p style="font-size: 1.2rem; font-weight: bold; padding: 0.8rem 1.6rem; border: 1px solid #e7e7e7;">
                        PREV
                    </p>
                </a>
            '''
        elif group_i > 0:
            prev_html = f'''
                <a style="text-decoration: none;" href="/{url_slug}.html">
                    <p style="
                        font-size: 1.2rem; font-weight: bold; padding: 0.8rem 1.6rem; border: 1px solid #e7e7e7;
                        "
                    >
                        PREV
                    </p>
                </a>
            '''
        else:
            prev_html = f''
        ### numbers
        numbers_html = ''
        ### first
        if group_i != 0:
            number_html = f'''
                <a style="text-decoration: none;" href="/{url_slug}.html">
                    <p 
                        style="
                            font-size: 1.2rem; font-weight: bold; padding: 0.8rem 1.6rem; border: 1px solid #e7e7e7;
                        "
                    >
                        1
                    </p>
                </a>
            '''
            numbers_html += number_html
        ### current prev ...
        if group_i > 4:
            number_html = f'''
                <p 
                    style="
                        font-size: 1.2rem; font-weight: bold; padding: 0.8rem 1.6rem; border: 1px solid #e7e7e7;
                    "
                >
                    ...
                </p>
            '''
            numbers_html += number_html
        ### current prev
        for i in range(3, 0, -1):
            page_index = group_i+1-i
            if page_index > 1:
                number_html = f'''
                    <a style="text-decoration: none;" href="/{url_slug}/page/{page_index}.html">
                        <p 
                            style="
                                font-size: 1.2rem; font-weight: bold; padding: 0.8rem 1.6rem; border: 1px solid #e7e7e7;
                            "
                        >
                            {page_index}
                        </p>
                    </a>
                '''
                numbers_html += number_html
        ### current
        number_html = f'''
            <a style="text-decoration: none;" href="#">
                <p 
                    style="
                        font-size: 1.2rem; font-weight: bold; padding: 0.8rem 1.6rem; 
                        border: 1px solid #e7e7e7; color: #ffffff; background-color: #222222;
                    "
                >
                    {group_i+1}
                </p>
            </a>
        '''
        numbers_html += number_html
        ### current next
        for i in range(3):
            page_index = group_i+1+i+1
            if page_index < len(groups):
                number_html = f'''
                    <a style="text-decoration: none;" href="/{url_slug}/page/{page_index}.html">
                        <p 
                            style="
                                font-size: 1.2rem; font-weight: bold; padding: 0.8rem 1.6rem; border: 1px solid #e7e7e7;
                            "
                        >
                            {page_index}
                        </p>
                    </a>
                '''
                numbers_html += number_html
        ### current next ...
        if group_i < len(groups)-1 - 4:
            number_html = f'''
                <p 
                    style="
                        font-size: 1.2rem; font-weight: bold; padding: 0.8rem 1.6rem; border: 1px solid #e7e7e7;
                    "
                >
                    ...
                </p>
            '''
            numbers_html += number_html
        ### last
        if group_i != len(groups)-1:
            number_html = f'''
                <a style="text-decoration: none;" href="/{url_slug}/page/{len(groups)}.html">
                    <p 
                        style="
                            font-size: 1.2rem; font-weight: bold; padding: 0.8rem 1.6rem; border: 1px solid #e7e7e7;
                        "
                    >
                        {len(groups)}
                    </p>
                </a>
            '''
            numbers_html += number_html

        ### next
        if group_i != len(groups)-1:
            next_html = f'''
                <a style="text-decoration: none;" href="/{url_slug}/page/{group_i+2}.html">
                    <p style="font-size: 1.2rem; font-weight: bold; padding: 0.8rem 1.6rem; border: 1px solid #e7e7e7;">
                        NEXT
                    </p>
                </a>
            '''
        else:
            next_html = f''

        ### HERBS
        ########################################
        html_herbs = f'''
            <section style="max-width: 175rem; margin: 0 auto; padding-left: 1.6rem; padding-right: 1.6rem;">
                <div style="display: flex;">
                    <div style="flex: 1;">
                        {html_sidebar}
                    </div>
                    <div style="flex: 3; padding-left: 4.8rem; border-left: 1px solid #e7e7e7;">
                        <div class="grid-3">
                            {html_cards}
                        </div>
                        <div style="display: flex; justify-content: center; gap: 0.8rem;">
                            {prev_html}
                            {numbers_html}
                            {next_html}
                        </div>
                    </div>
                </div>
            </section>
        '''
        html_main += f'''
            {html_title}
            {html_herbs}
        '''

        html = f'''
            <!DOCTYPE html>
            <html lang="en">
            {components.html_head(meta_title, meta_description)}
            <body>
                {sections.header()}
                <main>
                    {html_main}
                </main>
                <div class="spacer"></div>
                {sections.footer()}
            </body>
            </html>
        '''

        with open(html_filepath, 'w') as f: f.write(html)

    sitemaps_gen()
    # quit()

def main():
    # clusters_get(data)
    # sitemaps_gen()
    # quit()
    ### pages categories
    # category_herbs_popular_gen()
    # category_herbs_actions_gen()
    ### articles
    # article_herbs_herb_primary_gen()
    # article_herbs_herb_wcvp_gen()

    page_herbs_gen()

