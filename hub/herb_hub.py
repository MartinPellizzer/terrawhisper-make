import random

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

def article_herbs_herb_gen():
    herbs = []
    if 1:
        for herb in herbs_primary_medicinal: 
            if not herb_in_list(herbs, herb):
                herbs.append({'herb_name_scientific': herb['herb_name_scientific']})
    if 1:
        for herb in herbs_popular: 
            if not herb_in_list(herbs, herb):
                herbs.append({'herb_name_scientific': herb['herb_name_scientific']})
    for herb_i, herb in enumerate(herbs):
        herb_name_scientific = herb['herb_name_scientific']
        herb_name_scientific = polish.sanitize(herb_name_scientific)
        herb_slug = polish.sluggify(herb_name_scientific)
        url_slug = f'herbs/{herb_slug}'
        print(f'HERB: {herb_i}/{len(herbs)} - {herb_slug}')
        json_entity_filepath = f'''{g.DATABASE_FOLDERPATH}/entities/herbs/{herb_slug}.json'''
        json_entity = io.json_read(json_entity_filepath)
        herb_names_common = [name['answer'].title() for name in json_entity['herb_name_common']]
        herb_name_common = herb_names_common[0]
        herb_family = json_entity['family'][0]['answer'].title()
        herb_native_regions = [item['answer'].title() for item in json_entity['native_regions']]

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
                prompt_herb_family = herb_family
                prompt_herb_native_regions = ', '.join(herb_native_regions)
                prompt = f'''
                    Write a detailed paragraph in 5 sentences about the scientifi and botanical profile of {herb_name_common} ({herb_name_scientific}).
                    Include the following common names: {prompt_herb_names_common}.
                    Include the following family name: {prompt_herb_family}.
                    Include the following native regions: {prompt_herb_native_regions}.
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
        src = f'''/images/herbs/{herb_slug}.jpg'''
        alt = f'''herbal {herb_name_common}'''
        html_article += f'''<img src="{src}" alt="{alt}">'''
        html_article += f'''{utils.format_1N1(json_article['intro'])}'''
        ### lead magnet
        form_head = ''
        with open(f'{g.DATABASE_FOLDERPATH}/assets/scripts/newsletter/form-head.txt') as f: form_head = f.read()
        with open(f'{g.DATABASE_FOLDERPATH}/assets/scripts/newsletter/form-course-preparation-tincture.txt') as f: form_body = f.read()
        html_article += f'''
            <div class="free-gift">
                <p class="free-gift-heading">FREE COURSE</p>
                <p style="text-align: center; margin-bottom: 1.6rem;">How to make medicinal herbal tinctures for common ailments at home and in a weekend (using the Healing Drops System).</p>
                <img src="/images/shop/banner-course-preparation-tincture.jpg" alt="tincture preparation course banner">
                {form_body}
            </div>
        '''
        ### toc
        html_article += f'''[toc]'''
        html_article += f'''<h2>Scientific and Botanical Profile</h2>'''
        html_article += f'''{utils.format_1N1(json_article['botany'])}'''
        html_article += f'''<h2>History and Cultural Relevance</h2>'''
        html_article += f'''{utils.format_1N1(json_article['history'])}'''
        html_article += f'''<h2>Chemical Composition and Nutritional Profile</h2>'''
        html_article += f'''{utils.format_1N1(json_article['chemistry'])}'''
        html_article += f'''<h2>Medicinal Properties and Health Benefits</h2>'''
        html_article += f'''{utils.format_1N1(json_article['benefits'])}'''
        html_article += f'''<h2>Forms, Preparation and Usage</h2>'''
        html_article += f'''{utils.format_1N1(json_article['preparations'])}'''
        html_article += f'''<h2>Safety, Side Effects and Contraindications</h2>'''
        html_article += f'''{utils.format_1N1(json_article['safety'])}'''
        html_article += f'''<h2>Growing, Harvesting and Storage</h2>'''
        html_article += f'''{utils.format_1N1(json_article['gardening'])}'''
        html_article += f'''<h2>FAQ</h2>'''
        html_article += f'''{utils.format_1N1(json_article['faq'])}'''
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

def main():
    herb = herbs_primary_medicinal[0]
    herb_slug = herb['herb_slug']
    json_article = io.json_read(f'{g.DATABASE_FOLDERPATH}/entities/herbs/{herb_slug}.json')
    print(json_article)
    print(list(json_article.keys()))
    # quit()
    ### categories
    category_herbs_popular_gen()
    category_herbs_actions_gen()
    ### articles
    article_herbs_herb_gen()
    ###
    url_slug = f'herbs'
    html_filepath = f'''{g.website_folderpath}/{url_slug}.html'''
    html_main = f''
    html_herbs = f''
    ### category herbs primary medicinal
    for herb_i, herb in enumerate(herbs_primary_medicinal):
        print(f'HERB: {herb_i}/{len(herbs_primary_medicinal)} - {herb}')
        herb_slug = herb['herb_slug']
        herb_name_scientific = herb['herb_name_scientific']
        json_article = io.json_read(f'{g.DATABASE_FOLDERPATH}/entities/herbs/{herb_slug}.json')
        herb_name_common = json_article['herb_name_common'][0]['answer']
        src = f'''/images/herbs/{herb_slug}.jpg'''
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
        src = f'''/images/herbs/{herb_slug}.jpg'''
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
        herb_image_src = f'''/images/herbs/{herb_slug}.jpg'''
        herb_image_alt = f'''{herb_name_scientific}'''
        html_herbs_grid += f'''
            <div class="card-default">
                <a href="/{url_slug}/{herb_slug}.html">
                    <img src="{herb_image_src}" alt="{herb_image_alt}" style="margin-bottom: 0.8rem;">
                    <h3 style="margin-bottom: 0.8rem;">{cluster_name.title()}</h3>
                    <p style="font-size: 1.4rem; background-color: #f7f6f2; padding: 0.4rem 1.6rem; border-radius: 9999px;"><em>Latin Name: {herb_name_scientific.capitalize()}</em></p>
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
    meta_title = f'''Herbs'''
    meta_description = f''''''
    html = f'''
        <!DOCTYPE html>
        <html lang="en">
        {components.html_head(meta_title, meta_description)}
        <body>
            {sections.header()}
            {sections.breadcrumbs(url_slug)}
            <div class="spacer"></div>
            <main class="container-xl">
                {html_main}
            </main>
            <div class="spacer"></div>
            {sections.footer()}
        </body>
        </html>
    '''
    with open(html_filepath, 'w') as f: f.write(html)

