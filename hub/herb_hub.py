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
herbs_top = data.herbs_popular_get('teas', 10)
herbs_popular = data.herbs_popular_get('teas', 100)

categories_html = f'''
    <div style="display: flex; gap: 2.4rem; justify-content: center; margin-bottom: 1.6rem;">
        <a 
            style="color: #111111; font-weight: bold; font-size: 1.4rem; letter-spacing: 0.5px; text-decoration: none;" 
            href="/herbs.html"
        >
            ALL
        </a>
        <a 
            style="color: #111111; font-weight: bold; font-size: 1.4rem; letter-spacing: 0.5px; text-decoration: none;" 
            href="/herbs/top.html"
        >
            TOP 10
        </a>
        <a 
            style="color: #111111; font-weight: bold; font-size: 1.4rem; letter-spacing: 0.5px; text-decoration: none;" 
            href="/herbs/popular.html"
        >
            POPULAR 100
        </a>
        <a 
            style="color: #111111; font-weight: bold; font-size: 1.4rem; letter-spacing: 0.5px; text-decoration: none;" 
            href="/herbs/unverified.html"
        >
            UNVERIFIED
        </a>
    </div>
'''

def pagination_gen(group_i, groups, url_slug):
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
            <p 
                style="
                    font-size: 1.2rem; font-weight: bold; padding: 0.8rem 1.6rem; 
                    border: 1px solid #e7e7e7; color: #ffffff; background-color: #222222;
                "
            >
                {group_i+1}
            </p>
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
    pagination_html = f'''
        {prev_html}
        {numbers_html}
        {next_html}
    '''
    return pagination_html

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

def herbs_herb_primary_gen_overview(herb):
    import textwrap
    herb_name_scientific = herb['herb_name_scientific']
    herb_name_scientific = polish.sanitize(herb_name_scientific).capitalize()
    herb_slug = polish.sluggify(herb_name_scientific)
    url_slug = f'herbs/{herb_slug}'
    json_entity_filepath = f'''{g.DATABASE_FOLDERPATH}/ssot/herbs/herbs-primary/{herb_slug}.json'''
    json_entity = io.json_read(json_entity_filepath)
    herb_names_common = [name['answer'].title() for name in json_entity['herb_names_common']]
    herb_names_common_alt = ', '.join([name['answer'].title() for name in json_entity['herb_names_common'][1:4]])
    herb_name_common = herb_names_common[0]
    print(json_entity)
    herb_traditional_uses = json_entity['herb_traditional_uses']
    print(herb_name_common)
    # if herb_i == 15: quit()
    herb_family = json_entity['herb_family'][0]['answer'].title()
    herb_genus = herb_name_scientific.split(' ')[0].strip()
    herb_parts = json_entity['herb_parts']
    herb_parts_string = ', '.join([part['answer'] for part in herb_parts[:3]]).capitalize()
    herb_native_regions = ', and'.join(', '.join([
        item['answer'].title() 
        for item in json_entity['herb_native_regions'] 
        if item['total_score'] >= 7
    ][:3]).rsplit(',', 1))
    herb_parts_list = ', '.join(', '.join([
        item['answer'].title() 
        for item in json_entity['herb_parts'] 
        if item['total_score'] >= 7
    ][:3]).rsplit(',', 1))
    herb_parts = ', and'.join(', '.join([
        item['answer'].lower() 
        for item in json_entity['herb_parts'] 
        if item['total_score'] >= 7
    ][:3]).rsplit(',', 1))
    herb_historical_preparations = ', and'.join(', '.join([
        item['answer'].lower() + 's'
        for item in json_entity['herb_historical_preparations'] 
        if item['total_score'] >= 7
    ][:3]).rsplit(',', 1))
    herb_medicinal_actions = ', and'.join(', '.join([
        item['answer'].lower() 
        for item in json_entity['herb_medicinal_actions'] 
        if item['total_score'] >= 7
    ][:3]).rsplit(',', 1))
    herb_medicinal_actions_list = ', '.join(', '.join([
        item['answer'].title() 
        for item in json_entity['herb_medicinal_actions'] 
        if item['total_score'] >= 7
    ][:3]).rsplit(',', 1))
    herb_traditional_systems = ', and'.join(', '.join([
        item['answer'].lower() 
        for item in json_entity['herb_traditional_systems'] 
        if item['total_score'] >= 7
    ][:3]).rsplit(',', 1))
    ########################################
    # json
    ########################################
    ### json init
    json_article_filepath = f'''{g.DATABASE_FOLDERPATH}/json/{url_slug}.json'''
    json_article = io.json_read(json_article_filepath, create=True)
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
            prompt = textwrap.dedent(f'''
                You are an expert herbalist and content writer. 
                Generate a **neutral, factual, 2–3 sentence introduction paragraph** for a medicinal herb page. 
                Follow these rules:
                1. Start with the **common name** followed by the **scientific name in parentheses**.
                2. Mention the herb’s **primary traditional uses**, but do NOT make any health claims.
                3. Include the **plant family** and optionally the **cultural or regional use** if available.
                4. Include **plant parts used** (e.g., flowers, leaves, roots) if relevant.
                5. Keep the paragraph **informational and neutral**, suitable for search engines and human readers.
                6. Do not use promotional or persuasive language.
                Here is the data for the herb:
                - Common Name: {herb_name_common}  
                - Scientific Name: {herb_name_scientific}  
                - Family: {herb_family}  
                - Primary Traditional Uses: {herb_traditional_uses}  
                Generate the paragraph **only**, do not add titles, headings, or explanations.
            ''').strip()
                # - Plant Parts Used: {plant_parts}  
                # - Cultural/Regional Origin: {cultural_origin}  
            prompt += f'/no_think'
            reply = llm.reply(prompt).strip()
            if '</think>' in reply:
                reply = reply.split('</think>')[1].strip()
            reply = polish.vanilla(reply)
            json_article[key] = reply
            io.json_write(json_article_filepath, json_article)
    overview_quick_facts_html = textwrap.dedent(f'''
        <dl>
            <dt>Common Name</dt>
            <dd class="common-name"><strong>{herb_name_common}</strong></dd>
            <dt>Scientific Name</dt>
            <dd class="scientific-name"><strong>{herb_name_scientific.capitalize()}</strong></dd>
            <dt>Family</dt>
            <dd class="family"><strong>{herb_family.capitalize()}</strong></dd>
            <dt>Plant Parts Used</dt>
            <dd class="herb-parts"><strong>{herb_parts_string}</strong></dd>
        </dl>
    ''').strip()
    # TODO
    '''
    <dt>Traditional Use / Region:</dt>
    <dd>European and Ayurvedic herbal medicine</dd>
         data-synonyms="Chamomile, German Chamomile"
    '''
    ###
    overview_html = f'''
        <section id="overview">
            <h1>{herb_name_common} ({herb_name_scientific.capitalize()})</h1>
            <p>{json_article['intro']}</p>
            {overview_quick_facts_html}
        </section>
    '''

    overview_html = f'''
        <section>
          <h1 style="margin-bottom: 1.6rem;">{herb_name_common.title()} ({herb_name_scientific.capitalize()})</h1>
            <p>
                <!-- Short botanical summary: native region, family, key uses -->
                <strong>{herb_name_common} ({herb_name_scientific})</strong> is a member of the {herb_family} family, native to {herb_native_regions}. 
                Traditionally, its {herb_parts} have been used for {herb_historical_preparations}.
            </p>
            <p>
                This herb is particularly valued for its {herb_medicinal_actions} actions, and has a long history of use in {herb_traditional_systems}.
            </p>
            <figure>
              <img src="/images/herbs/{herb_slug}.jpg" 
                   alt="{herb_name_common} ({herb_name_scientific.capitalize()}) dried pieces of the herb arranged on a wooden table for reference" 
                   width="400">
              <figcaption>{herb_name_common} ({herb_name_scientific.capitalize()}) dried pieces of the herb arranged together on a wooden table for reference, used in teas and remedies.</figcaption>
            </figure>

        </section>
    '''
    ## not here? structured data in next section (quick facts)?
    '''
          <!-- Optional: Quick bullet points -->
          <ul style="margin-top: 1rem;">
            <li><strong>Common Name:</strong> {herb_name_common}</li>
            <li><strong>Scientific Name:</strong> {herb_name_scientific}</li>
            <li><strong>Family:</strong> {herb_family}</li>
            <li><strong>Plant Parts Used:</strong> {herb_parts_list}</li>
            <li><strong>Primary Medicinal Uses:</strong> {herb_medicinal_actions_list}</li>
          </ul>
    '''
    return overview_html

def herbs_herb_primary_gen_quick_facts_old(json_entity, herb_name_common, herb_name_scientific, herb_family, herb_parts_string):
    quick_facts_html = f'''
        <aside id="quick-facts" aria-labelledby="quick-facts-title">
          <h2 id="quick-facts-title">Quick Facts</h2>
          <dl>
            <dt>Common Name</dt>
            <dd class="quick-common-name"><strong>{herb_name_common}</strong></dd>
            <dt>Scientific Name</dt>
            <dd class="quick-scientific-name"><strong>{herb_name_scientific}</strong></dd>
            <dt>Plant Family</dt>
            <dd class="quick-family-name"><strong>{herb_family}</strong></dd>
            <dt>Plant Parts Used</dt>
            <dd class="quick-plant-parts-name"><strong>{herb_parts_string}</strong></dd>
          </dl>
        </aside>
    '''
    '''
            <dt>Traditional Systems</dt>
            <dd>European, Ayurvedic</dd>
    '''
    return quick_facts_html 

def herbs_herb_primary_gen_quick_facts(herb):
    import textwrap
    herb_name_scientific = herb['herb_name_scientific']
    herb_name_scientific = polish.sanitize(herb_name_scientific).capitalize()
    herb_slug = polish.sluggify(herb_name_scientific)
    url_slug = f'herbs/{herb_slug}'
    json_entity_filepath = f'''{g.DATABASE_FOLDERPATH}/ssot/herbs/herbs-primary/{herb_slug}.json'''
    json_entity = io.json_read(json_entity_filepath)
    herb_names_common = [name['answer'].title() for name in json_entity['herb_names_common']]
    herb_names_common_alt = ', '.join([name['answer'].title() for name in json_entity['herb_names_common'][1:4]])
    herb_name_common = herb_names_common[0]
    print(json_entity)
    herb_traditional_uses = json_entity['herb_traditional_uses']
    print(herb_name_common)
    # if herb_i == 15: quit()
    herb_family = json_entity['herb_family'][0]['answer'].title()
    herb_genus = herb_name_scientific.split(' ')[0].strip()
    herb_species = herb_name_scientific.split(' ')[1].strip()
    herb_parts = json_entity['herb_parts']
    herb_parts_string = ', '.join([part['answer'] for part in herb_parts[:3]]).capitalize()
    herb_native_regions = ', '.join(', '.join([
        item['answer'].title() 
        for item in json_entity['herb_native_regions'] 
        if item['total_score'] >= 7
    ][:3]).rsplit(',', 1))
    herb_parts = ', '.join(', '.join([
        item['answer'].title() 
        for item in json_entity['herb_parts'] 
        if item['total_score'] >= 7
    ][:3]).rsplit(',', 1))
    herb_historical_preparations = ', '.join(', '.join([
        item['answer'].title()
        for item in json_entity['herb_historical_preparations'] 
        if item['total_score'] >= 7
    ][:3]).rsplit(',', 1))
    herb_medicinal_actions = ', '.join(', '.join([
        item['answer'].title() 
        for item in json_entity['herb_medicinal_actions'] 
        if item['total_score'] >= 7
    ][:3]).rsplit(',', 1))
    herb_traditional_systems = ', '.join(', '.join([
        item['answer'].title() 
        for item in json_entity['herb_traditional_systems'] 
        if item['total_score'] >= 7
    ][:3]).rsplit(',', 1))
    herb_historical_preparations = ', '.join(', '.join([
        item['answer'].title() 
        for item in json_entity['herb_historical_preparations'] 
        if item['total_score'] >= 7
    ][:3]).rsplit(',', 1))
    quick_facts_html = f'''
        <section id="quick-facts" aria-labelledby="quick-facts-title">
        <h2 id="quick-facts-title">Quick Facts / Key Information</h2>
        <!-- Structured, scan-friendly fact table -->
        <table>
            <tbody>
              <tr>
                <th scope="row">Common Name</th>
                <td>{herb_name_common}</td>
              </tr>
              <tr>
                <th scope="row">Scientific Name</th>
                <td><em>{herb_name_scientific}</em></td>
              </tr>
              <tr>
                <th scope="row">Plant Family</th>
                <td>{herb_family}</td>
              </tr>
              <tr>
                <th scope="row">Genus</th>
                <td>{herb_genus}</td>
              </tr>
              <tr>
                <th scope="row">Species</th>
                <td>{herb_species}</td>
              </tr>
              <tr>
                <th scope="row">Native Range</th>
                <td>{herb_native_regions}</td>
              </tr>
              <tr>
                <th scope="row">Plant Parts Used</th>
                <td>{herb_parts}</td>
              </tr>
              <tr>
                <th scope="row">Primary Medicinal Actions</th>
                <td>{herb_medicinal_actions}</td>
              </tr>
              <tr>
                <th scope="row">Primary Traditional Systems</th>
                <td>{herb_traditional_systems}</td>
              </tr>
              <tr>
                <th scope="row">Historical Preparation Methods</th>
                <td>{herb_historical_preparations}</td>
              </tr>
            </tbody>
        </table>
    '''
    # TODO
    '''
          <tr>
            <th scope="row">Plant Type / Habit</th>
            <td>{{Plant Type / Growth Habit}}</td>
          </tr>
          <tr>
            <th scope="row">Taste / Energetics (if applicable)</th>
            <td>{{Taste / Energetics}}</td>
          </tr>
          <tr>
            <th scope="row">Safety Rating</th>
            <td>{{General Safety Level}}</td>
          </tr>
    '''
    return quick_facts_html 

def herbs_herb_primary_gen_botany(herb):
    herb_name_scientific = herb['herb_name_scientific']
    herb_name_scientific = polish.sanitize(herb_name_scientific).capitalize()
    herb_slug = polish.sluggify(herb_name_scientific)
    url_slug = f'herbs/{herb_slug}'
    json_entity_filepath = f'''{g.DATABASE_FOLDERPATH}/ssot/herbs/herbs-primary/{herb_slug}.json'''
    json_entity = io.json_read(json_entity_filepath)
    herb_names_common = [name['answer'].title() for name in json_entity['herb_names_common']]
    herb_names_common_alt = ', '.join([name['answer'].title() for name in json_entity['herb_names_common'][1:4]])
    herb_name_common = herb_names_common[0]
    print(json_entity)
    herb_traditional_uses = json_entity['herb_traditional_uses']
    print(herb_name_common)
    # if herb_i == 15: quit()
    herb_family = json_entity['herb_family'][0]['answer'].title()
    herb_genus = herb_name_scientific.split(' ')[0].strip()
    herb_parts = json_entity['herb_parts']
    herb_parts_string = ', '.join([part['answer'] for part in herb_parts[:3]]).capitalize()
    # herb_native_regions = [item['answer'].title() for item in json_entity['native_regions']]
    ########################################
    # json
    ########################################
    ### json init
    json_article_filepath = f'''{g.DATABASE_FOLDERPATH}/json/{url_slug}.json'''
    json_article = io.json_read(json_article_filepath, create=True)
    ###
    regen = False
    dispel = False
    key = 'botany_growth_habit'
    if key not in json_article: json_article[key] = ''
    if regen: json_article[key] = ''
    if dispel: 
        json_article[key] = ''
        io.json_write(json_article_filepath, json_article)
    if not dispel:
        if json_article[key] == '':
            prompt = textwrap.dedent(f'''
                You are a botanist and semantic SEO content specialist.
                Generate ONE concise sentence describing ONLY the **growth habit** of the herb listed below.
                This sentence will be used inside a <dd> element under the label “Growth Habit”.
                STRICT RULES (do not break these):
                1. Mention ONLY:
                   - life cycle classification (annual, biennial, perennial)
                   - plant type (herbaceous, woody, shrub, tree, vine)
                2. Choose ONE life cycle classification only.
                3. Do NOT mention:
                   - leaves, flowers, stems, height, or appearance
                   - flowering time or developmental stages
                   - habitat, origin, or distribution
                   - medicinal, culinary, or traditional uses
                4. Do NOT combine or qualify life cycle terms (e.g., no “perennial with biennial cycle”).
                5. Use neutral, factual, encyclopedic language.
                6. Output ONE sentence only.
                Herb name:
                {herb_name_scientific}
                Return ONLY the sentence. No explanations, no formatting, no extra text.
            ''').strip()
            prompt += f'/no_think'
            reply = llm.reply(prompt).strip()
            if '</think>' in reply:
                reply = reply.split('</think>')[1].strip()
            reply = polish.vanilla(reply)
            json_article[key] = reply
            io.json_write(json_article_filepath, json_article)
    ###
    regen = False
    dispel = False
    key = 'botany_height'
    if key not in json_article: json_article[key] = ''
    if regen: json_article[key] = ''
    if dispel: 
        json_article[key] = ''
        io.json_write(json_article_filepath, json_article)
    if not dispel:
        if json_article[key] == '':
            prompt = textwrap.dedent(f'''
                You are a botanist and scientific content writer.
                Determine the plant type of "{herb_name_scientific}" (herb, shrub, tree, vine, or grass).
                Then write ONE concise, neutral sentence describing ONLY its typical height.
                Rules:
                - The sentence must describe height only (no plant type, no uses, no benefits).
                - Use a biologically realistic height range for the plant type.
                - Use meters for trees and shrubs; centimeters for herbs and grasses.
                - Do NOT mention the plant name.
                - Do NOT mention that it is a tree, herb, or shrub.
                - Do NOT include cultivation, habitat, or medicinal information.
                - Use factual, objective language.
                - Write a single complete sentence suitable for a <dd> element.
                - Return ONLY the sentence, with no formatting, no italics, and no extra text.
            ''').strip()
            prompt += f'/no_think'
            reply = llm.reply(prompt).strip()
            if '</think>' in reply:
                reply = reply.split('</think>')[1].strip()
            reply = polish.vanilla(reply)
            json_article[key] = reply
            io.json_write(json_article_filepath, json_article)
    ###
    regen = False
    dispel = False
    key = 'botany_leaves_present'
    if key not in json_article: json_article[key] = ''
    if regen: json_article[key] = ''
    if dispel: 
        json_article[key] = ''
        io.json_write(json_article_filepath, json_article)
    if not dispel:
        if json_article[key] == '':
            prompt = textwrap.dedent(f'''
                You are a bot that provides accurate botanical information based on verified plant sources. 
                Question: Does the plant with the scientific name "{herb_name_scientific}" have leaves?
                Instructions:
                - Answer **only** with "yes" or "no".
                - Do not provide any explanation, commentary, or extra text.
                - Base your answer only on documented botanical knowledge.
                - If the plant part does not exist for this species, respond with "no".
                - Do not guess; answer strictly according to botanical facts.
                Example:
                - Question: Does "Matricaria chamomilla" have flowers?
                - Answer: yes
                - Question: Does "Sphagnum palustre" have flowers?
                - Answer: no
                Now answer the following:
                Does "{herb_name_scientific}" have leaves?
            ''').strip()
            prompt += f'/no_think'
            reply = llm.reply(prompt).strip()
            if '</think>' in reply:
                reply = reply.split('</think>')[1].strip()
            reply = polish.vanilla(reply)
            json_article[key] = reply
            io.json_write(json_article_filepath, json_article)
    ###
    if json_article['botany_leaves_present'].lower().strip() == 'yes':
        regen = False
        dispel = False
        key = 'botany_leaves_description'
        if key not in json_article: json_article[key] = ''
        if regen: json_article[key] = ''
        if dispel: 
            json_article[key] = ''
            io.json_write(json_article_filepath, json_article)
        if not dispel:
            if json_article[key] == '':
                prompt = textwrap.dedent(f'''
                    You are a botanist and scientific content writer.
                    Write a concise botanical description of the LEAVES of the following plant species.
                    STRICT RULES (MANDATORY):
                    - Do NOT start the sentence with “The leaves of…”
                    - Do NOT mention the plant name in any form.
                    - Write in noun-phrase style, not full sentences.
                    - Describe ONLY high-certainty, universally accepted traits.
                    - Include ONLY:
                        - leaf type (needle-like, broad, etc.) if certain
                        - upper and lower surface color if known
                        - universally recognized features (e.g., stomatal bands)
                    - Do NOT include:
                        - shape adjectives that are redundant with leaf type
                        - phyllotaxy (alternate, opposite, spiral) unless certain
                        - subjective descriptors (simple, papery, soft, fuzzy, long, short)
                        - measurements, size, or numeric ranges
                        - invented traits
                        - medicinal uses, benefits, effects
                    - Write exactly ONE sentence.
                    - Use neutral, objective scientific language.
                    Focus on:
                    - conveying the leaf’s observable category and color
                    - universally recognized diagnostic features only
                    Plant:
                    - Common Name: {herb_name_common}
                    - Scientific Name: {herb_name_scientific}
                    Output ONLY the sentence that belongs inside the <dd> element.
                    Do not add explanations, headings, or extra text.
                ''').strip()
                prompt += f'/no_think'
                reply = llm.reply(prompt).strip()
                if '</think>' in reply:
                    reply = reply.split('</think>')[1].strip()
                reply = polish.vanilla(reply)
                json_article[key] = reply
                io.json_write(json_article_filepath, json_article)
    ###
    regen = False
    dispel = False
    key = 'botany_flowers_present'
    if key not in json_article: json_article[key] = ''
    if regen: json_article[key] = ''
    if dispel: 
        json_article[key] = ''
        io.json_write(json_article_filepath, json_article)
    if not dispel:
        if json_article[key] == '':
            prompt = textwrap.dedent(f'''
                You are a bot that provides accurate botanical information based on verified plant sources. 
                Question: Does the plant with the scientific name "[Scientific Name]" have flowers?
                Instructions:
                - Answer **only** with "yes" or "no".
                - Do not provide any explanation, commentary, or extra text.
                - Base your answer only on documented botanical knowledge.
                - If the plant does not produce flowers, respond with "no".
                - Do not guess; answer strictly according to botanical facts.
                Examples:
                - Question: Does "Matricaria chamomilla" have flowers?
                - Answer: yes
                - Question: Does "Sphagnum palustre" have flowers?
                - Answer: no
                Now answer the following:
                Does "{herb_name_scientific}" have flowers?
            ''').strip()
            prompt += f'/no_think'
            reply = llm.reply(prompt).strip()
            if '</think>' in reply:
                reply = reply.split('</think>')[1].strip()
            reply = polish.vanilla(reply)
            json_article[key] = reply
            io.json_write(json_article_filepath, json_article)
    ###
    if json_article['botany_flowers_present'].lower().strip() == 'yes':
        regen = False
        dispel = False
        key = 'botany_flowers_description'
        if key not in json_article: json_article[key] = ''
        if regen: json_article[key] = ''
        if dispel: 
            json_article[key] = ''
            io.json_write(json_article_filepath, json_article)
        if not dispel:
            if json_article[key] == '':
                prompt = textwrap.dedent(f'''
                    You are a botanist and scientific content writer.
                    Write a concise botanical description of the FLOWERS of the following plant species.
                    STRICT RULES (MANDATORY):
                    - Do NOT start the sentence with “The flowers of…”
                    - Do NOT mention the plant name in any form.
                    - Write in noun-phrase style, not full sentences.
                    - Describe ONLY high-certainty, universally accepted traits.
                    - Include ONLY:
                        - flower color(s) if known
                        - flower arrangement if universally recognized (e.g., solitary, clustered, spike, raceme)
                        - basic symmetry (actinomorphic / zygomorphic) if certain
                        - universally recognized diagnostic features (e.g., number of petals, unique markings) if reliably documented
                    - Do NOT include:
                        - subjective descriptors (beautiful, showy, fragrant)
                        - inferred or uncertain traits
                        - measurements, sizes, or numeric ranges
                        - invented features
                        - medicinal uses, benefits, effects
                    - Write exactly ONE sentence.
                    - Use neutral, objective scientific language.
                    Focus on:
                    - conveying observable floral traits only
                    - universally recognized diagnostic features
                    Plant:
                    - Common Name: {herb_name_common}
                    - Scientific Name: {herb_name_scientific}
                    Output ONLY the sentence that belongs inside the <dd> element.
                    Do not add explanations, headings, or extra text.
                ''').strip()
                prompt += f'/no_think'
                reply = llm.reply(prompt).strip()
                if '</think>' in reply:
                    reply = reply.split('</think>')[1].strip()
                reply = polish.vanilla(reply)
                json_article[key] = reply
                io.json_write(json_article_filepath, json_article)
    ###
    regen = False
    dispel = False
    key = 'botany_stems_present'
    if key not in json_article: json_article[key] = ''
    if regen: json_article[key] = ''
    if dispel: 
        json_article[key] = ''
        io.json_write(json_article_filepath, json_article)
    if not dispel:
        if json_article[key] == '':
            prompt = textwrap.dedent(f'''
                You are a bot that provides accurate botanical information based on verified plant sources. 
                Question: Does the plant with the scientific name "[Scientific Name]" have stems?
                Instructions:
                - Answer **only** with "yes" or "no".
                - Do not provide any explanation, commentary, or extra text.
                - Base your answer only on documented botanical knowledge.
                - If the plant does not have stems, respond with "no".
                - Do not guess; answer strictly according to botanical facts.
                Examples:
                - Question: Does "Matricaria chamomilla" have stems?
                - Answer: yes
                - Question: Does "Sphagnum palustre" have stems?
                - Answer: no
                Now answer the following:
                Does "{herb_name_scientific}" have stems?
            ''').strip()
            prompt += f'/no_think'
            reply = llm.reply(prompt).strip()
            if '</think>' in reply:
                reply = reply.split('</think>')[1].strip()
            reply = polish.vanilla(reply)
            json_article[key] = reply
            io.json_write(json_article_filepath, json_article)
    if json_article['botany_stems_present'].lower().strip() == 'yes':
        regen = False
        dispel = False
        key = 'botany_stems_description'
        if key not in json_article: json_article[key] = ''
        if regen: json_article[key] = ''
        if dispel: 
            json_article[key] = ''
            io.json_write(json_article_filepath, json_article)
        if not dispel:
            if json_article[key] == '':
                prompt = textwrap.dedent(f'''
                    You are a botanist and scientific content writer.
                    Write a concise botanical description of the STEMS of the following plant species.
                    STRICT RULES (MANDATORY):
                    - Do NOT start the sentence with “The stems of…”
                    - Do NOT mention the plant name in any form.
                    - Write in noun-phrase style, not full sentences.
                    - Describe ONLY high-certainty, universally accepted traits.
                    - Include ONLY:
                        - growth habit (e.g., erect, creeping, climbing) if universally documented
                        - branching pattern if certain (e.g., simple, dichotomous, opposite, alternate)
                        - surface characteristics if reliably documented (e.g., glabrous, hairy, woody, succulent)
                        - universally recognized diagnostic features if documented
                    - Do NOT include:
                        - subjective descriptors (slender, strong, flexible, ornamental)
                        - inferred or uncertain traits
                        - measurements, sizes, or numeric ranges
                        - invented features
                        - medicinal uses, benefits, effects
                    - Write exactly ONE sentence.
                    - Use neutral, objective scientific language.
                    Focus on:
                    - conveying observable stem traits only
                    - universally recognized diagnostic features
                    Plant:
                    - Common Name: {herb_name_common}
                    - Scientific Name: {herb_name_scientific}
                    Output ONLY the sentence that belongs inside the <dd> element.
                    Do not add explanations, headings, or extra text.
                ''').strip()
                prompt += f'/no_think'
                reply = llm.reply(prompt).strip()
                if '</think>' in reply:
                    reply = reply.split('</think>')[1].strip()
                reply = polish.vanilla(reply)
                json_article[key] = reply
                io.json_write(json_article_filepath, json_article)
    leaves_description_html = ''
    if json_article['botany_leaves_present'].lower().strip() == 'yes':
        leaves_description_html = f'''
            <dt>Leaves</dt>
            <dd>{json_article['botany_leaves_description'].capitalize()}</dd>
        '''
    flowers_description_html = ''
    if json_article['botany_flowers_present'].lower().strip() == 'yes':
        flowers_description_html = f'''
            <dt>Flowers</dt>
            <dd>{json_article['botany_flowers_description'].capitalize()}</dd>
        '''
    stems_description_html = ''
    if json_article['botany_stems_present'].lower().strip() == 'yes':
        stems_description_html = f'''
            <dt>Stems</dt>
            <dd>{json_article['botany_stems_description'].capitalize()}</dd>
        '''
    botany_html = f'''
        <section id="botanical-identity">
          <h2>Botanical Identity</h2>
          <dl>
            <dt>Scientific Name</dt>
            <dd class="quick-scientific-name"><strong>{herb_name_scientific}</strong></dd>
            <dt>Common Name</dt>
            <dd class="quick-common-name"><strong>{herb_name_common}</strong></dd>
            <dt>Synonyms / Alternative Names</dt>
            <dd class="quick-synonyms"><strong>{herb_names_common_alt}</strong></dd>
            <dt>Plant Family</dt>
            <dd class="quick-family-name"><strong>{herb_family}</strong></dd>
            <dt>Genus</dt>
            <dd class="quick-genus"><strong>{herb_genus}</strong></dd>
          </dl>
        <h3>Botanical Description</h3>
          <dl>
            <dt>Growth Habit</dt>
            <dd>{json_article['botany_growth_habit']}</dd>
            <dt>Height</dt>
            <dd>{json_article['botany_height']}</dd>
            {leaves_description_html}
            {flowers_description_html}
            {stems_description_html}
          </dl>
        </section>
    '''
    # TODO
    '''
            <dt>Botanical Description</dt>
            <dd>A small, daisy-like flowering plant with feathery leaves and white petals surrounding a yellow central disc.</dd>
    '''
    return botany_html 


def herbs_herb_primary_gen_traditional_uses(json_entity):
    herb_traditional_systems = '\n'.join([
        f'''<li>{item['answer'].title()}</li>''' 
        for item in json_entity['herb_traditional_systems']
        if item['total_score'] >= 600
    ][:4])
    herb_historical_preparations = '\n'.join([
        f'''<li>{item['answer'].title()}</li>''' 
        for item in json_entity['herb_historical_preparations']
        if item['total_score'] >= 600
    ][:4])
    traditional_uses_html = f'''
        <section id="traditional-uses">
          <h2>Traditional Uses / Historical Use</h2>
          <h3>Traditional Systems</h3>
          <ul>
            {herb_traditional_systems}
          </ul>
          <h3>Historical Preparation Methods</h3>
          <ul>
            {herb_historical_preparations}
          </ul>
        </section>
    '''
    '''
          <p>Chamomile (Matricaria chamomilla) has been historically used in European and Western Asian herbal traditions. It has been prepared as infusions, teas, and poultices, and referenced in folk medicine texts for its calming properties and culinary applications.</p>
    '''
    return traditional_uses_html

def herbs_herb_primary_gen_medicinal_actions(json_entity):
    herb_medicinal_actions = [
        item['answer']
        for item in json_entity['herb_medicinal_actions']
        if item['total_score'] >= 600
    ][:4]
    herb_medicinal_actions_html = ''
    template_intros = [
            line.strip() for line in 
            '''
                Traditionally described as a
                Historically regarded as a
                In herbal texts, considered a
                As described in traditional systems, a
                Commonly referenced as a
                In herbal literature, noted as a
            '''.split('\n')
            if line.strip() != ''
        ]
    random.shuffle(template_intros)
    template_adjectives = [
            line.strip() for line in 
            '''
                gentle
                mild
                moderate
                soothing
                calming
                warming
                cooling
            '''.split('\n')
            if line.strip() != ''
        ]
    random.shuffle(template_adjectives)
    for herb_medicinal_action in herb_medicinal_actions:
        # action dt
        if herb_medicinal_action == 'carminative':
            herb_medicinal_actions_html += '<dt>Carminative</dt>\n'
        elif herb_medicinal_action == 'sedative':
            herb_medicinal_actions_html += '<dt>Sedative</dt>\n'
        elif herb_medicinal_action == 'anti-inflammatory':
            herb_medicinal_actions_html += '<dt>Anti-inflammatory</dt>\n'
        elif herb_medicinal_action == 'antispasmodic':
            herb_medicinal_actions_html += '<dt>Antispasmodic</dt>\n'
        elif herb_medicinal_action == 'astringent':
            herb_medicinal_actions_html += '<dt>Astringent</dt>\n'
        elif herb_medicinal_action == 'diuretic':
            herb_medicinal_actions_html += '<dt>Diuretic</dt>\n'
        elif herb_medicinal_action == 'stimulant':
            herb_medicinal_actions_html += '<dt>Stimulant</dt>\n'
        elif herb_medicinal_action == 'expectorant':
            herb_medicinal_actions_html += '<dt>Expectorant</dt>\n'
        elif herb_medicinal_action == 'tonic':
            herb_medicinal_actions_html += '<dt>Tonic</dt>\n'
        elif herb_medicinal_action == 'bitter':
            herb_medicinal_actions_html += '<dt>Bitter</dt>\n'
        # action dd (general)
        template_intro = template_intros.pop(0)
        template_adjective = template_adjectives.pop(0)
        herb_medicinal_actions_html += '<dd>\n'
        herb_medicinal_actions_html += template_intro
        herb_medicinal_actions_html += ' ' + template_adjective
        herb_medicinal_actions_html += ' ' + herb_medicinal_action + ','
        # action dd (specific)
        if herb_medicinal_action == 'carminative':
            herb_medicinal_actions_html += ' ' + random.choice([
                line.strip() for line in 
                '''
                    within digestive system contexts
                    in relation to gastrointestinal comfort
                    for digestive process support
                    in digestion-focused applications
                    in stomach-related herbal uses
                '''.split('\n')
                if line.strip() != ''
            ])
        elif herb_medicinal_action == 'sedative':
            herb_medicinal_actions_html += ' ' + random.choice([
                line.strip() for line in 
                '''
                    in nervous system–related contexts
                    for relaxation-oriented uses
                    in calming-focused applications
                    in rest-related herbal contexts
                    in stress-related herbal practices
                '''.split('\n')
                if line.strip() != ''
            ])
        elif herb_medicinal_action == 'anti-inflammatory':
            herb_medicinal_actions_html += ' ' + random.choice([
                line.strip() for line in 
                '''
                    in tissue-soothing contexts
                    for irritation-related applications
                    in inflammation-focused discussions
                    in topical or internal use contexts
                    for general calming applications
                '''.split('\n')
                if line.strip() != ''
            ])
        elif herb_medicinal_action == 'antispasmodic':
            herb_medicinal_actions_html += ' ' + random.choice([
                line.strip() for line in 
                '''
                    in muscle-related contexts
                    for tension-related applications
                    in smooth muscle contexts
                    for cramp-focused discussions
                    in spasm-related situations
                '''.split('\n')
                if line.strip() != ''
            ])
        elif herb_medicinal_action == 'astringent':
            herb_medicinal_actions_html += ' ' + random.choice([
                line.strip() for line in 
                '''
                    in tissue-toning contexts
                    for skin-related applications
                    in drying-focused uses
                    for surface-level applications
                    in structural-support contexts
                '''.split('\n')
                if line.strip() != ''
            ])
        elif herb_medicinal_action == 'diuretic':
            herb_medicinal_actions_html += ' ' + random.choice([
                line.strip() for line in 
                '''
                    in fluid-regulation contexts
                    for elimination-focused applications
                    in urinary system discussions
                    for moisture-related balance
                    in cleansing-oriented uses
                '''.split('\n')
                if line.strip() != ''
            ])
        elif herb_medicinal_action == 'stimulant':
            herb_medicinal_actions_html += ' ' + random.choice([
                line.strip() for line in 
                '''
                    in energy-related contexts
                    for alertness-focused applications
                    in activation-oriented uses
                    for vitality-related discussions
                    in wakefulness-related contexts
                '''.split('\n')
                if line.strip() != ''
            ])
        elif herb_medicinal_action == 'expectorant':
            herb_medicinal_actions_html += ' ' + random.choice([
                line.strip() for line in 
                '''
                    in respiratory system contexts
                    for airway-related applications
                    in mucus-related discussions
                    for breathing-focused uses
                    in chest-related herbal contexts
                '''.split('\n')
                if line.strip() != ''
            ])
        elif herb_medicinal_action == 'tonic':
            herb_medicinal_actions_html += ' ' + random.choice([
                line.strip() for line in 
                '''
                    for long-term use contexts
                    in whole-system applications
                    for foundational support
                    in general wellness contexts
                    for broad-use formulations
                '''.split('\n')
                if line.strip() != ''
            ])
        elif herb_medicinal_action == 'bitter':
            herb_medicinal_actions_html += ' ' + random.choice([
                line.strip() for line in 
                '''
                    in taste-driven classifications
                    for digestion-related formulations
                    in appetite-focused contexts
                    for flavor-based applications
                    in bitter herb groupings
                '''.split('\n')
                if line.strip() != ''
            ])
        herb_medicinal_actions_html += '.'
        herb_medicinal_actions_html += '</dd>\n'
    ###
    # TODO: generate intro paragraph based on herb_medicinal_actions
    '''
          <p>
            In traditional herbal systems, chamomile (Matricaria chamomilla) has been
            described using a set of standardized medicinal actions. These terms are
            used to characterize how the plant has been traditionally understood to
            interact with the body.
          </p>
    '''
    medicinal_actions_html = f'''
        <section id="medicinal-actions">
          <h2>Medicinal Actions</h2>
          <dl>
            {herb_medicinal_actions_html}
          </dl>
        </section>
    '''
    return medicinal_actions_html

def herbs_herb_primary_gen_active_compounds(json_entity):
    flavonoid_line = random.choice([
        line.strip() for line in 
        '''
            A widely occurring class of plant polyphenols found in leaves, flowers, and fruits.
            A group of naturally occurring compounds commonly present in many flowering plants.
            Plant-based polyphenolic compounds frequently distributed throughout aerial plant parts.
            A chemical class commonly identified in plant tissues, especially flowers and leaves.
            Naturally occurring polyphenols that contribute to pigmentation and structural chemistry.
        '''.split('\n')
        if line.strip() != ''
    ])
    phenolic_acid_line = random.choice([
        line.strip() for line in 
        '''
            A class of aromatic plant compounds commonly found in leaves, seeds, and stems.
            Naturally occurring phenolic compounds present in many plant species.
            Simple phenolic molecules widely distributed across plant tissues.
            A group of plant-derived compounds frequently identified in herbal material.
            Organic acids commonly occurring as part of plant secondary metabolism.
        '''.split('\n')
        if line.strip() != ''
    ])
    tannin_line = random.choice([
        line.strip() for line in 
        '''
            A class of polyphenolic compounds commonly found in bark, leaves, and seeds.
            Plant-derived compounds known for their ability to bind proteins.
            Naturally occurring polyphenols widely distributed in woody and leafy plant parts.
            A group of compounds frequently present in plant tissues exposed to herbivory.
            High-molecular-weight phenolic compounds found in many plant species.
        '''.split('\n')
        if line.strip() != ''
    ])
    terpenoid_line = random.choice([
        line.strip() for line in 
        '''
            A large class of naturally occurring compounds derived from isoprene units.
            Plant-produced compounds commonly found in essential oils and resins.
            A diverse group of organic compounds present in many aromatic plants.
            Naturally occurring metabolites widely distributed in leaves, flowers, and roots.
            A chemical class commonly associated with volatile plant constituents.
        '''.split('\n')
        if line.strip() != ''
    ])
    alkaloid_line = random.choice([
        line.strip() for line in 
        '''
            A class of nitrogen-containing compounds produced by many plant species.
            Naturally occurring organic compounds commonly involved in plant defense.
            Plant-derived nitrogenous compounds found in various tissues.
            A diverse group of secondary metabolites present in numerous plants.
            Organic compounds biosynthesized by plants as part of secondary metabolism.
        '''.split('\n')
        if line.strip() != ''
    ])
    saponin_line = random.choice([
        line.strip() for line in 
        '''
            A group of glycosidic compounds commonly found in roots, leaves, and seeds.
            Plant-derived compounds characterized by their soap-like properties.
            Naturally occurring metabolites distributed across many plant families.
            A chemical class frequently identified in herbaceous and woody plants.
            Secondary plant compounds composed of sugar-linked aglycones.
        '''.split('\n')
        if line.strip() != ''
    ])
    essential_oil_line = random.choice([
        line.strip() for line in 
        '''
            A complex mixture of volatile compounds produced by aromatic plant tissues.
            Naturally occurring plant oils composed primarily of volatile constituents.
            A collective term for aromatic compounds extracted from plant material.
            Volatile plant-derived substances commonly present in leaves and flowers.
            A mixture of naturally occurring compounds responsible for plant aroma.
        '''.split('\n')
        if line.strip() != ''
    ])
    coumarin_line = random.choice([
        line.strip() for line in 
        '''
            A class of aromatic organic compounds found in many plant species.
            Naturally occurring lactone compounds distributed across various plant tissues.
            Plant-derived compounds often associated with fragrance-related chemistry.
            A group of secondary metabolites present in seeds, roots, and leaves.
            Organic compounds biosynthesized as part of plant secondary metabolism.
        '''.split('\n')
        if line.strip() != ''
    ])
    anthocyanin_line = random.choice([
        line.strip() for line in 
        '''
            A class of water-soluble pigments responsible for red, purple, and blue coloration.
            Plant-derived flavonoid pigments commonly found in flowers and fruits.
            Naturally occurring compounds contributing to plant pigmentation.
            Pigment molecules widely distributed in colored plant tissues.
            A subgroup of flavonoids associated with visual coloration in plants.
        '''.split('\n')
        if line.strip() != ''
    ])
    glycoside_line = random.choice([
        line.strip() for line in 
        '''
            A broad class of compounds composed of a sugar bound to a non-sugar component.
            Plant-produced compounds commonly stored in inactive glycosylated forms.
            Naturally occurring metabolites distributed across many plant species.
            A chemical class frequently found in roots, leaves, and seeds.
            Secondary metabolites formed through glycosylation processes in plants.
        '''.split('\n')
        if line.strip() != ''
    ])
    ###
    herb_active_compounds = [
        item['answer']
        for item in json_entity['herb_active_compounds']
        if item['total_score'] >= 600
    ][:4]
    herb_active_compounds_dl = ''
    for compound in herb_active_compounds:
        herb_active_compounds_dl += f'<dt>{compound.title()}</dt>\n'
        if compound.lower() == 'flavonoid':
            herb_active_compounds_dl += f'<dd>{flavonoid_line}</dd>\n'
        if compound.lower() == 'phenolic acid':
            herb_active_compounds_dl += f'<dd>{phenolic_acid_line}</dd>\n'
        if compound.lower() == 'tannin':
            herb_active_compounds_dl += f'<dd>{tannin_line}</dd>\n'
        if compound.lower() == 'terpenoid':
            herb_active_compounds_dl += f'<dd>{terpenoid_line}</dd>\n'
        if compound.lower() == 'alkaloid':
            herb_active_compounds_dl += f'<dd>{alkaloid_line}</dd>\n'
        if compound.lower() == 'saponin':
            herb_active_compounds_dl += f'<dd>{saponin_line}</dd>\n'
        if compound.lower() == 'essential oil':
            herb_active_compounds_dl += f'<dd>{essential_oil_line}</dd>\n'
        if compound.lower() == 'coumarin':
            herb_active_compounds_dl += f'<dd>{coumarin_line}</dd>\n'
        if compound.lower() == 'anthocyanin':
            herb_active_compounds_dl += f'<dd>{anthocyanin_line}</dd>\n'
        if compound.lower() == 'glycoside':
            herb_active_compounds_dl += f'<dd>{glycoside_line}</dd>\n'
    herb_active_compounds_html = f'''
        <section id="active-compounds">
          <h2>Active Compounds</h2>
          <dl>
            {herb_active_compounds_dl}
          </dl>
        </section>
    '''
    # TODO
    '''
          <p>
            Chamomile (Matricaria chamomilla) contains several bioactive compounds, which have been
            identified in the flowers, leaves, and stems. These compounds are listed below with
            their chemical classification.
          </p>
    '''
    return herb_active_compounds_html

def herbs_herb_primary_gen_modern_research(json_entity):
    modern_research_placeholder = random.choice([
        '''
            Scientific research related to this plant is ongoing. This section will be
            expanded in the future to include summaries of phytochemical studies,
            laboratory research, and other relevant scientific literature as it becomes
            available.
        ''',
        '''
            Contemporary research on this plant includes areas such as chemical
            analysis, laboratory-based studies, and observational research. Detailed
            summaries of published findings are not included at this stage and will be
            added during future content updates.
        ''',
        '''
            Modern scientific investigation of this plant has focused on identifying
            its chemical constituents and examining their properties in controlled
            research settings. Comprehensive study summaries will be incorporated into
            this section as additional sources are reviewed.
        ''',
        '''
            This section is reserved for future summaries of scientific research related
            to this plant. As additional verified sources are reviewed, relevant study
            information will be added here.
        ''',
        '''
            Scientific literature concerning this plant spans multiple areas, including
            phytochemistry and laboratory research. Detailed analysis of published
            studies is not included at this time and will be added as part of future
            editorial expansion.
        ''',
    ])
    section_modern_research_html = f'''
        <section id="modern-research">
          <h2>Modern Research Overview</h2>
          <p>
              {modern_research_placeholder}
          </p>
        </section>
    '''
    return section_modern_research_html 

def herbs_herb_primary_gen_safety_precautions(json_entity):
    herb_drugs_interaction_lines_yes = random.choice([
        line.strip() for line in 
        '''
            Potential interactions with prescription medications have been reported in available sources.
            This herb has been associated with interactions when used alongside certain pharmaceutical medications.
            Reports suggest that this herb may interact with prescription drugs in some contexts.
            Interactions between this herb and prescription medications have been noted in traditional use and literature.
            The use of this herb alongside pharmaceutical medications may result in potential interactions.
        '''.split('\n')
        if line.strip() != ''
    ])
    herb_drugs_interaction_lines_unknown = random.choice([
        line.strip() for line in 
        '''
            Interactions with prescription medications have not been well documented.
            Available information regarding interactions with pharmaceutical drugs is limited.
            The potential for interactions with prescription medications has not been extensively studied.
            There is insufficient evidence to determine whether this herb interacts with pharmaceutical drugs.
            Interactions between this herb and prescription medications are not clearly established.
        '''.split('\n')
        if line.strip() != ''
    ])
    total_score_yes = 0
    total_score_unknown = 0
    herb_drugs_interaction = json_entity['herb_drugs_interaction']
    for item in herb_drugs_interaction:
        if item['answer'] == 'yes':
            total_score_yes = int(item['total_score'])
        if item['answer'] == 'unknown':
            total_score_unknown = int(item['total_score'])
    if total_score_yes > total_score_unknown: 
        herb_drugs_interaction_line = herb_drugs_interaction_lines_yes 
    else:
        herb_drugs_interaction_line = herb_drugs_interaction_lines_unknown 
    ### ALLERGIES
    herb_allergies_lines_yes = random.choice([
        line.strip() for line in 
        '''
            Allergic reactions have been reported, particularly in individuals sensitive to related plant families.
            This herb may cause allergic responses in some individuals, especially those with known plant sensitivities.
            Sensitivity reactions have been noted in certain individuals following exposure to this herb.
            Reports indicate that this herb can trigger allergic reactions in susceptible individuals.
            Individuals with sensitivities to botanically related plants may experience allergic reactions.
        '''.split('\n')
        if line.strip() != ''
    ])
    herb_allergies_lines_unknown = random.choice([
        line.strip() for line in 
        '''
            Allergic reactions associated with this herb have not been well documented.
            Information regarding allergic responses to this herb is limited.
            There is insufficient evidence to determine whether this herb commonly causes allergic reactions.
            Sensitivity or allergy-related effects have not been clearly established.
            Reports of allergic reactions to this herb are not well documented in available sources.
        '''.split('\n')
        if line.strip() != ''
    ])
    total_score_yes = 0
    total_score_unknown = 0
    herb_allergies = json_entity['herb_allergies']
    for item in herb_allergies:
        if item['answer'] == 'yes':
            total_score_yes = int(item['total_score'])
        if item['answer'] == 'unknown':
            total_score_unknown = int(item['total_score'])
    if total_score_yes > total_score_unknown: 
        herb_allergies_line = herb_allergies_lines_yes 
    else:
        herb_allergies_line = herb_allergies_lines_unknown 
    ### TOXICITY
    herb_toxicity_lines_yes = random.choice([
        line.strip() for line in 
        '''
            Toxic effects have been reported in association with the use of this herb.
            This herb has been associated with toxic effects under certain conditions.
            Reports indicate that this herb may exhibit toxic properties in some contexts.
            Toxicity related to this herb has been documented in available sources.
            The use of this herb has been linked to reported toxic effects.
        '''.split('\n')
        if line.strip() != ''
    ])
    herb_toxicity_lines_unknown = random.choice([
        line.strip() for line in 
        '''
            Toxic effects associated with this herb have not been well documented.
            Available information regarding the toxicity of this herb is limited.
            There is insufficient evidence to determine the toxic potential of this herb.
            The toxicity profile of this herb has not been clearly established.
            Reports of toxicity related to this herb are not well documented in available literature.
        '''.split('\n')
        if line.strip() != ''
    ])
    total_score_yes = 0
    total_score_unknown = 0
    herb_toxicity = json_entity['herb_toxicity']
    for item in herb_toxicity:
        if item['answer'] == 'yes':
            total_score_yes = int(item['total_score'])
        if item['answer'] == 'unknown':
            total_score_unknown = int(item['total_score'])
    if total_score_yes > total_score_unknown: 
        herb_toxicity_line = herb_toxicity_lines_yes 
    else:
        herb_toxicity_line = herb_toxicity_lines_unknown 
    ### GENERAL PRECAUTIONS
    herb_generally_safe_lines_yes = random.choice([
        line.strip() for line in 
        '''
            General precautions have been noted regarding the use of this herb.
            Caution is advised in certain contexts based on traditional use and available information.
            Some general precautions have been associated with the use of this herb.
            The use of this herb may warrant general caution in certain situations.
            Precautionary considerations have been reported in relation to this herb.
        '''.split('\n')
        if line.strip() != ''
    ])
    herb_generally_safe_lines_unknown = random.choice([
        line.strip() for line in 
        '''
            Specific general precautions associated with this herb have not been well documented.
            Available information does not clearly establish general precautionary concerns for this herb.
            There is limited information regarding general precautions related to the use of this herb.
            General precautionary guidance for this herb is not clearly established in available sources.
            Reports outlining specific general precautions for this herb are limited.
        '''.split('\n')
        if line.strip() != ''
    ])
    total_score_yes = 0
    total_score_unknown = 0
    herb_generally_safe = json_entity['herb_generally_safe']
    for item in herb_generally_safe:
        if item['answer'] == 'yes':
            total_score_yes = int(item['total_score'])
        if item['answer'] == 'unknown':
            total_score_unknown = int(item['total_score'])
    if total_score_yes > total_score_unknown: 
        herb_generally_safe_line = herb_generally_safe_lines_yes 
    else:
        herb_generally_safe_line = herb_generally_safe_lines_unknown 
    ### CONTRAINDICATIONS
    herb_contraindications_lines_yes = random.choice([
        line.strip() for line in 
        '''
            Certain contraindications have been reported in relation to the use of this herb.
            The use of this herb has been associated with reported contraindications in some situations.
            Contraindications related to this herb have been noted in traditional use and available sources.
            Some conditions have been cited as contraindications for the use of this herb.
            Reported information suggests that this herb may be contraindicated in specific circumstances.
        '''.split('\n')
        if line.strip() != ''
    ])
    herb_contraindications_lines_unknown = random.choice([
        line.strip() for line in 
        '''
            Specific contraindications associated with this herb have not been well documented.
            Available information does not clearly establish contraindications for the use of this herb.
            There is insufficient evidence to determine specific contraindications related to this herb.
            Contraindications for this herb are not clearly established in available sources.
            Reports outlining specific contraindications for this herb are limited.
        '''.split('\n')
        if line.strip() != ''
    ])
    total_score_yes = 0
    total_score_unknown = 0
    herb_contraindications = json_entity['herb_contraindications']
    for item in herb_contraindications:
        if item['answer'] == 'yes':
            total_score_yes = int(item['total_score'])
        if item['answer'] == 'unknown':
            total_score_unknown = int(item['total_score'])
    if total_score_yes > total_score_unknown: 
        herb_contraindications_line = herb_contraindications_lines_yes 
    else:
        herb_contraindications_line = herb_contraindications_lines_unknown 
    ### PREGNANCY AND BREASTFEEDING
    herb_pregnancy_and_breastfeeding_lines_yes = random.choice([
        line.strip() for line in 
        '''
            Considerations regarding use during pregnancy or breastfeeding have been reported.
            The use of this herb during pregnancy or breastfeeding has been noted as a consideration in available sources.
            Pregnancy and breastfeeding-related considerations have been associated with the use of this herb.
            Reports suggest that use during pregnancy or breastfeeding may require special consideration.
            The use of this herb in pregnancy or breastfeeding contexts has been discussed in available information.
        '''.split('\n')
        if line.strip() != ''
    ])
    herb_pregnancy_and_breastfeeding_lines_unknown = random.choice([
        line.strip() for line in 
        '''
            Safety during pregnancy and breastfeeding has not been well documented.
            Available information regarding use during pregnancy or breastfeeding is limited.
            There is insufficient evidence to determine the safety of this herb during pregnancy or breastfeeding.
            Use during pregnancy or breastfeeding has not been clearly established in available sources.
            Information addressing pregnancy and breastfeeding-related safety for this herb is limited.
        '''.split('\n')
        if line.strip() != ''
    ])
    total_score_yes = 0
    total_score_unknown = 0
    herb_pregnancy_and_breastfeeding = json_entity['herb_pregnancy_and_breastfeeding']
    for item in herb_pregnancy_and_breastfeeding:
        if item['answer'] == 'yes':
            total_score_yes = int(item['total_score'])
        if item['answer'] == 'unknown':
            total_score_unknown = int(item['total_score'])
    if total_score_yes > total_score_unknown: 
        herb_pregnancy_and_breastfeeding_line = herb_pregnancy_and_breastfeeding_lines_yes 
    else:
        herb_pregnancy_and_breastfeeding_line = herb_pregnancy_and_breastfeeding_lines_unknown 
    ###
    section_safety_precautions_html = f'''
        <section id="safety-precautions">
          <h2>Safety & Contraindications</h2>
          <dl>
            <dt>General Precautions</dt>
            <dd>{herb_generally_safe_line}</dd>
            <dt>Contraindications</dt>
            <dd>{herb_contraindications_line}</dd>
            <dt>Allergies</dt>
            <dd>{herb_allergies_line}</dd>
            <dt>Drug Interactions</dt>
            <dd>{herb_drugs_interaction_line}</dd>
            <dt>Toxicity</dt>
            <dd>{herb_toxicity_line}</dd>
            <dt>Pregnancy & Breastfeeding</dt>
            <dd>{herb_pregnancy_and_breastfeeding_line}</dd>
          </dl>
        </section>
    '''
    return section_safety_precautions_html 

def herbs_herb_primary_gen_preparation_usage(json_entity):
    infusion = random.choice([
        line.strip() for line in 
        '''
            Plant material is steeped in hot water to extract water-soluble compounds.
            Dried or fresh plant parts are infused in hot water and consumed as a beverage.
            A preparation method involving steeping plant material in heated water for a short period.
            Water is poured over plant material and allowed to steep before straining.
            Infusions are commonly prepared using hot water to release aromatic and soluble components.
        '''.split('\n')
        if line.strip() != ''
    ])
    decoction = random.choice([
        line.strip() for line in 
        '''
            Plant material is simmered in water to extract compounds from tougher parts.
            A preparation method involving prolonged boiling of roots, bark, or dense plant material.
            Plant parts are gently boiled in water to release soluble constituents.
            Decoctions are made by heating plant material in water for an extended time.
            This method uses sustained heat to extract compounds from firm plant structures.
        '''.split('\n')
        if line.strip() != ''
    ])
    tincture = random.choice([
        line.strip() for line in 
        '''
            Plant material is macerated in alcohol to create a concentrated liquid extract.
            A preparation involving soaking plant parts in alcohol for extended extraction.
            Alcohol is used as a solvent to extract plant constituents over time.
            Tinctures are liquid extracts produced through alcoholic maceration.
            This method preserves plant compounds using an alcohol-based solution.
        '''.split('\n')
        if line.strip() != ''
    ])
    poultice = random.choice([
        line.strip() for line in 
        '''
Fresh or dried plant material is applied externally to the skin.
Plant parts are crushed or moistened and placed directly on the body.
A topical preparation made by applying softened plant material externally.
Poultices involve external application of prepared plant matter.
This method uses direct contact between plant material and the skin.
        '''.split('\n')
        if line.strip() != ''
    ])
    powder = random.choice([
        line.strip() for line in 
        '''
Dried plant material is ground into a fine powder.
Plant parts are dried and mechanically reduced to a powdered form.
A preparation created by pulverizing dried plant material.
Powdered preparations use finely milled plant parts.
This method converts dried plant material into a uniform powder.
        '''.split('\n')
        if line.strip() != ''
    ])
    capsule = random.choice([
        line.strip() for line in 
        '''
Powdered plant material is enclosed in a capsule for oral consumption.
Capsules contain measured amounts of dried, ground plant material.
A preparation format using encapsulated plant powders.
Plant material is processed into powder and sealed in capsules.
Capsules provide a standardized way to consume powdered plant material.
        '''.split('\n')
        if line.strip() != ''
    ])
    essential_oil = random.choice([
        line.strip() for line in 
        '''
Volatile compounds are extracted from plant material through distillation.
Essential oils are obtained by separating aromatic components from the plant.
A concentrated aromatic extract produced through steam distillation.
This method captures volatile plant compounds in oil form.
Essential oils consist of aromatic substances isolated from plant material.
        '''.split('\n')
        if line.strip() != ''
    ])
    extract = random.choice([
        line.strip() for line in 
        '''
Plant compounds are extracted using water, glycerin, or other solvents.
A preparation involving the separation of plant constituents without alcohol.
Extracts are created by dissolving plant material in a suitable non-alcoholic medium.
This method isolates plant compounds using alternative solvents.
Non-alcoholic extracts provide a liquid form of plant constituents.
        '''.split('\n')
        if line.strip() != ''
    ])
    oil_infusion = random.choice([
        line.strip() for line in 
        '''
Plant material is steeped in oil to transfer fat-soluble compounds.
Oils are infused with plant material over time to absorb constituents.
A preparation created by soaking plant parts in carrier oils.
Oil infusions capture plant compounds using lipid-based solvents.
This method allows plant material to release constituents into oil.
        '''.split('\n')
        if line.strip() != ''
    ])
    culinary_use = random.choice([
        line.strip() for line in 
        '''
Plant material is incorporated into food or beverages for flavor or aroma.
Leaves, flowers, or roots are used as ingredients in culinary preparations.
A preparation involving the use of plant parts in cooking or food production.
Culinary use includes adding plant material to recipes or beverages.
This method integrates plant material into edible preparations.
        '''.split('\n')
        if line.strip() != ''
    ])
    ###
    herb_preparations = json_entity['herb_preparations']
    herb_preparations_core = ['infusion',  'decoction', 'poultice']
    herb_preparations_extra = []
    for item in herb_preparations:
        herb_preparation_name = item['answer']
        if herb_preparation_name.lower().strip() not in herb_preparations_core:
            herb_preparations_extra.append(item)
    ###
    herb_preparations_selected = []
    for prep in herb_preparations_core:
        herb_preparations_selected.append(prep)
    i = 0
    max_i = 2
    for item in herb_preparations_extra:
        if item['total_score'] >= 600:
            herb_preparations_selected.append(item['answer'])
            i += 1
            if i >= max_i: break
    ###
    herb_preparations_html = ''
    for val in herb_preparations_selected:
        if val == 'infusion':
            herb_preparations_html += f'''<dt>Infusion</dt>\n'''
            herb_preparations_html += f'''<dd>{infusion}</dd>\n'''
        if val == 'decoction':
            herb_preparations_html += f'''<dt>Decoction</dt>\n'''
            herb_preparations_html += f'''<dd>{decoction}</dd>\n'''
        if val == 'poultice':
            herb_preparations_html += f'''<dt>Poultice</dt>\n'''
            herb_preparations_html += f'''<dd>{poultice}</dd>\n'''
        if val == 'tincture':
            herb_preparations_html += f'''<dt>Tincture</dt>\n'''
            herb_preparations_html += f'''<dd>{tincture}</dd>\n'''
        if val == 'powder':
            herb_preparations_html += f'''<dt>Powder</dt>\n'''
            herb_preparations_html += f'''<dd>{powder}</dd>\n'''
        if val == 'capsule':
            herb_preparations_html += f'''<dt>Capsule</dt>\n'''
            herb_preparations_html += f'''<dd>{capsule}</dd>\n'''
        if val == 'essential oil':
            herb_preparations_html += f'''<dt>Capsule</dt>\n'''
            herb_preparations_html += f'''<dd>{capsule}</dd>\n'''
        if val == 'extract':
            herb_preparations_html += f'''<dt>Extract</dt>\n'''
            herb_preparations_html += f'''<dd>{extract}</dd>\n'''
        if val == 'oil infusion':
            herb_preparations_html += f'''<dt>Infused Oil</dt>\n'''
            herb_preparations_html += f'''<dd>{oil_infusion}</dd>\n'''
        if val == 'culinary use':
            herb_preparations_html += f'''<dt>Culinary Use</dt>\n'''
            herb_preparations_html += f'''<dd>{culinary_use}</dd>\n'''
    section_preparation_usage_html = f'''
        <section id="preparation-usage">
          <h2>Preparation & Usage Methods</h2>
          <dl>
            {herb_preparations_html}
          </dl>
        </section>
    '''
    # TODO
    '''
          <p>
            Chamomile (Matricaria chamomilla) has been traditionally prepared in various forms.
            The most common methods include infusions, decoctions, poultices, and culinary uses.
          </p>
    '''
    return section_preparation_usage_html 

def herbs_herb_primary_gen_growing_harvesting_storage(json_entity):

    soil_type = json_entity['herb_growing_soil'][0]['answer']
    soil_drainage = json_entity['herb_growing_soil_drainage'][0]['answer']
    soil_fertility = json_entity['herb_growing_soil_fertility'][0]['answer']
    soil_ph = json_entity['herb_growing_soil_ph'][0]['answer']
    sunlight_type = json_entity['herb_growing_sunlight_type'][0]['answer']
    sunlight_tolerance = json_entity['herb_growing_sunlight_tolerance'][0]['answer']
    watering_type = json_entity['herb_growing_watering_type'][0]['answer']
    watering_tolerance = json_entity['herb_growing_watering_tolerance'][0]['answer']

    section_growing_harvesting_storage_html = f'''
        <section id="growing-harvesting-storage">
          <h2>Growing, Harvesting & Storage</h2>
          <h3>Growing / Cultivation</h3>
          <dl>
            <dt>Soil</dt>
            <dd>
                Prefers {soil_type} with {soil_drainage}.
                Typically grows best in {soil_fertility}.
            </dd>
            <dt>Sunlight</dt>
            <dd>
                Thrives in {sunlight_type}.
                Tolerates {sunlight_tolerance}.
            </dd>
            <dt>Watering</dt>
            <dd>
                Prefers {watering_type}.
                Tolerates {watering_tolerance}.
            </dd>
    '''
    # TODO
    '''
            <dt>Climate</dt>
            <dd>Temperate climates; tolerates mild frost.</dd>
          </dl>
          <h3>Harvesting</h3>
          <dl>
            <dt>Plant Parts</dt>
            <dd>Flowers are primarily harvested for traditional use.</dd>
            <dt>Optimal Timing</dt>
            <dd>Harvest when flowers are fully open, usually in late spring to early summer.</dd>
          </dl>
          <h3>Storage</h3>
          <dl>
            <dt>Drying</dt>
            <dd>Air-dry in a shaded, well-ventilated area to preserve color and aroma.</dd>
            <dt>Storage Conditions</dt>
            <dd>Store dried plant material in airtight containers away from light and moisture.</dd>
            <dt>Shelf Life</dt>
            <dd>Dried flowers can be stored for up to 1–2 years under optimal conditions.</dd>
          </dl>
        </section>
    '''
    return section_growing_harvesting_storage_html 

def herbs_herb_primary_gen_related_herbs(json_entity):
    herb_medicinal_actions = [
        item['answer']
        for item in json_entity['herb_medicinal_actions']
        # if item['total_score'] >= 600
    ][:4]
    ###
    herbs = []
    if 1:
        for herb in herbs_primary_medicinal: 
            herbs.append({'herb_name_scientific': herb['herb_name_scientific']})
    if 1:
        for herb in herbs_popular: 
            herbs.append({'herb_name_scientific': herb['herb_name_scientific']})
    ###
    related_herbs = []
    related_herbs_i = 0
    for herb_i, herb in enumerate(herbs):
        herb_name_scientific = herb['herb_name_scientific']
        herb_name_scientific = polish.sanitize(herb_name_scientific).capitalize()
        herb_slug = polish.sluggify(herb_name_scientific)
        url_slug = f'herbs/{herb_slug}'
        json_entity_filepath = f'''{g.DATABASE_FOLDERPATH}/ssot/herbs/herbs-primary/{herb_slug}.json'''
        _json_entity = io.json_read(json_entity_filepath)
        # match by medicinal actions
        _herb_medicinal_actions = [
            item['answer']
            for item in _json_entity['herb_medicinal_actions']
            # if item['total_score'] >= 600
        ]
        # skip comparing herb with itself
        if json_entity['herb_name_scientific'].lower().strip() == herb_name_scientific.lower().strip():
            continue
        # add herb with matching top action
        if _herb_medicinal_actions[0].lower().strip() == herb_medicinal_actions[0].lower().strip():
            related_herbs.append(herb)
            related_herbs_i += 1
            if related_herbs_i >= 2:
                break
    ###
    herbs_medicinal_actions_dd = []
    for related_herb in related_herbs:
        herb_name_scientific = related_herb['herb_name_scientific']
        herb_name_scientific = polish.sanitize(herb_name_scientific).capitalize()
        herb_slug = polish.sluggify(herb_name_scientific)
        url_slug = f'herbs/{herb_slug}'
        json_entity_filepath = f'''{g.DATABASE_FOLDERPATH}/ssot/herbs/herbs-primary/{herb_slug}.json'''
        json_entity = io.json_read(json_entity_filepath)
        herb_names_common = [name['answer'].title() for name in json_entity['herb_names_common']]
        herb_name_common = herb_names_common[0]
        herbs_medicinal_actions_dd.append(f'''<a href="/{url_slug}.html">{herb_name_common}</a>''')
    herbs_medicinal_actions_dd = ', '.join(herbs_medicinal_actions_dd)

    section_related_herbs_html = f'''
        <section id="related-herbs">
          <h2>Related Herbs & Semantic Links</h2>
          <dl>
            <dt>Shared Medicinal Actions</dt>
            <dd>
                {herbs_medicinal_actions_dd}
            </dd>
            <dt>Shared Compounds</dt>
            <dd>
              <a href="/herbs/lemon-balm">Lemon Balm</a>, <a href="/herbs/fennel">Fennel</a>
            </dd>
            <dt>Shared Traditional Use Systems</dt>
            <dd>
              <a href="/herbs/fennel">Fennel</a>, <a href="/herbs/mint">Mint</a>
            </dd>
            <dt>Shared Preparation Methods</dt>
            <dd>
              <a href="/herbs/mint">Mint</a>, <a href="/herbs/lavender">Lavender</a>
            </dd>
          </dl>
        </section>
    '''
    return section_related_herbs_html

def herbs_herb_primary_gen_faq(json_entity):
    section_faq_html = f'''
    '''
    return section_faq_html

def herbs_herb_primary_gen_medical_disclaimer(json_entity):
    if 0:
        section_medical_disclaimer_html = f'''
            <section id="medical-disclaimer">
              <h2>Medical Disclaimer</h2>
              <p>
                The information provided on this page about Chamomile (Matricaria chamomilla) is for educational and informational purposes only.
                It is not intended to diagnose, treat, cure, or prevent any medical condition. 
                Always consult a qualified healthcare professional before using any herb for medicinal purposes.
              </p>
            </section>
        '''
    section_medical_disclaimer_html = f'''
        <section class="medical-disclaimer">
          <h2>Medical Disclaimer</h2>
          <p>
            The information provided on this page is for educational and informational purposes only.
            It is not intended to diagnose, treat, cure, or prevent any medical condition. 
            Always consult a qualified healthcare professional before using any herb for medicinal purposes.
          </p>
        </section>
    '''
    return section_medical_disclaimer_html

def herbs_herb_primary_gen():
    herbs = []
    if 1:
        for herb in herbs_primary_medicinal: 
            # if not herb_in_list(herbs, herb):
            herbs.append({'herb_name_scientific': herb['herb_name_scientific']})
    if 1:
        for herb in herbs_popular: 
            # if not herb_in_list(herbs, herb):
            herbs.append({'herb_name_scientific': herb['herb_name_scientific']})
    ###
    for herb_i, herb in enumerate(herbs):
        herb_name_scientific = herb['herb_name_scientific']
        herb_name_scientific = polish.sanitize(herb_name_scientific).capitalize()
        herb_slug = polish.sluggify(herb_name_scientific)
        url_slug = f'herbs/{herb_slug}'
        print(f'HERB: {herb_i}/{len(herbs)} - {herb_slug}')
        json_entity_filepath = f'''{g.DATABASE_FOLDERPATH}/ssot/herbs/herbs-primary/{herb_slug}.json'''
        json_entity = io.json_read(json_entity_filepath)
        herb_names_common = [name['answer'].title() for name in json_entity['herb_names_common']]
        herb_names_common_alt = ', '.join([name['answer'].title() for name in json_entity['herb_names_common'][1:4]])
        herb_name_common = herb_names_common[0]
        print(json_entity)
        herb_traditional_uses = json_entity['herb_traditional_uses']
        print(herb_name_common)
        # if herb_i == 15: quit()
        herb_family = json_entity['herb_family'][0]['answer'].title()
        herb_genus = herb_name_scientific.split(' ')[0].strip()
        herb_parts = json_entity['herb_parts']
        herb_parts_string = ', '.join([part['answer'] for part in herb_parts[:3]]).capitalize()
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
        # continue
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
        src = f'''/images/herbs/{herb_slug}.jpg'''
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
        if 0:
            html = f'''
                <!DOCTYPE html>
                <html lang="en">
                {components.html_head(meta_title, meta_description, form_head)}
                <body>
                    {sections.header()}
                    <section class="container-xl">
                        {sections.breadcrumbs(url_slug)}
                    </section>
                    <main class="container-md article">
                        {html_article}
                    </main>
                    <div class="mt-64"></div>
                    {sections.footer()}
                </body>
                </html>
            '''

        meta_title = f'{herb_name_common} ({herb_name_scientific.capitalize()}) – Medicinal Uses, Benefits & Safety'

        ### json meta description
        regen = False
        dispel = False
        key = 'meta_description'
        if key not in json_article: json_article[key] = ''
        if regen: json_article[key] = ''
        if dispel: 
            json_article[key] = ''
            io.json_write(json_article_filepath, json_article)
        if not dispel:
            if json_article[key] == '':
                prompt = textwrap.dedent(f'''
                    Write a meta description for a website page about the following medicinal plant:
                    {herb_name_common} ({herb_name_scientific.capitalize()}) 
                    I will provide the TEMPLATE you must follow.
                    The goal is to insert the [COMMON NAME] and the [SCIENTIFIC NAME] in the template with the provided data.
                    Also, you must fill the [BROAD ACTIONS] in the template with your own knowledge. Try to include 3 comma-separated actions using as few words as possible.
                    Here is the data.
                    COMMON NAME: {herb_name_common}
                    SCIENTIFIC NAME: {herb_name_scientific}
                    TEMPLATE TO FILL:
                    [COMMON NAME] ([SCIENTIFIC NAME]) is a medicinal plant traditionally used for [BROAD ACTIONS]. This page covers its botanical background, traditional uses, active compounds, preparation methods, and safety considerations.
                    GUIDELINES:
                    Replay only with the asked content, which is the meta description.
                ''').strip()
                prompt += f'/no_think'
                reply = llm.reply(prompt).strip()
                if '</think>' in reply:
                    reply = reply.split('</think>')[1].strip()
                reply = polish.vanilla(reply)
                json_article[key] = reply
                io.json_write(json_article_filepath, json_article)


        section_overview_html = herbs_herb_primary_gen_overview(herb)
        section_quick_facts_html = herbs_herb_primary_gen_quick_facts(herb)
        section_botany_html = herbs_herb_primary_gen_botany(herb)
        section_traditional_uses_html = herbs_herb_primary_gen_traditional_uses(json_entity)

        section_medicinal_actions_html = herbs_herb_primary_gen_medicinal_actions(json_entity)
        section_active_compounds_html = herbs_herb_primary_gen_active_compounds(json_entity)
        section_modern_research_html = herbs_herb_primary_gen_modern_research(json_entity)
        section_safety_precautions_html = herbs_herb_primary_gen_safety_precautions(json_entity)
        section_preparation_usage_html = herbs_herb_primary_gen_preparation_usage(json_entity)
        section_growing_harvesting_storage_html = herbs_herb_primary_gen_growing_harvesting_storage(json_entity)

        # TODO
        section_related_herbs_html = herbs_herb_primary_gen_related_herbs(json_entity)
        section_faq_html = herbs_herb_primary_gen_faq(json_entity)
        section_medical_disclaimer_html = herbs_herb_primary_gen_medical_disclaimer(json_entity)

        ###
        meta_description = json_article['meta_description']
        html_filepath = f'''{g.website_folderpath}/{url_slug}.html'''
        import textwrap
        site_name = 'Terra Whisper'
        html = textwrap.dedent(f''' 
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <link rel="stylesheet" href="/styles-herb.css">
                <title>{meta_title}</title>
                <meta name="description" content="{meta_description}">
                <link rel="canonical" href="https://terrawhisper.com/herbs/{herb_slug}.html">
                <meta property="og:title" content="{meta_title}">
                <meta property="og:description" content="{meta_description}">
                <meta property="og:type" content="article">
                <meta property="og:url" content="https://terrawhisper.com/herbs/{herb_slug}.html">
                <meta property="og:image" content="https://terrawhisper.com/images/herbs/{herb_slug}.jpg">
                <meta property="og:site_name" content="{site_name}">
                <meta property="og:locale" content="en_US">
            </head>
            <body>
              <header></header>
              <main>
                <article class="container-md">
                    {section_overview_html}
                    {section_quick_facts_html}
                    {section_botany_html}
                    {section_traditional_uses_html}
                    {section_medicinal_actions_html}
                    {section_active_compounds_html}
                    {section_modern_research_html} 
                    {section_safety_precautions_html}
                    {section_preparation_usage_html}
                    {section_growing_harvesting_storage_html}
                    {section_related_herbs_html}
                    {section_faq_html}
                    {section_medical_disclaimer_html}
                </article>
              </main>
              <footer></footer>
            </body>
            </html>
        ''').strip()
        with open(html_filepath, 'w') as f: f.write(html)

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

def card_primary_gen(i, card_img_src, herb_slug, card_title, card_desc, card_subtitle):
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
                    <a href="/herbs/{herb_slug}.html">
                        <img 
                            style="margin-bottom: 1.6rem; height: 24rem; object-fit: cover;"
                            src="{card_img_src}"
                        >
                    </a>
                    <p style="margin-bottom: 1.6rem; font-size: 1.2rem; font-weight: bold; letter-spacing: 1px; color: #aaaaaa;">JULY 30, 2024</p>
                    <h2><a style="color: #111111; text-decoration: none;" href="/herbs/{herb_slug}.html">{card_title}</a></h2>
                    <p style="
                        font-size: 1.4rem; background-color: #f7f6f2; 
                        padding: 0.4rem 1.6rem; border-radius: 9999px;
                        margin-bottom: 1.6rem;
                    ">
                        Common Name: <strong>{card_subtitle}</strong>
                    </p>
                    <p style="margin-bottom: 1.6rem;">{card_desc}</p>
                    <p> 
                        <a style="color: #111111; font-weight: bold; font-size: 1.4rem; letter-spacing: 0.5px;" href="/herbs/{herb_slug}.html">READ MORE</a>
                    </p>
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
        # card_desc = ' '.join(lorem.paragraph().split(' ')[:8])
        card_desc = 'Leen Randell is a herbalist, apothecary, and journalist, who loves to report insights on medicinal herbs and herbal preparations.'
        card_img_src = f'/images/herbs/{herb_slug}.jpg'
        html_card = f'''
            <div style="display: flex; gap: 2.4rem; margin-bottom: 2.4rem; padding-bottom: 1.6rem; border-bottom: 1px solid #e7e7e7;">
                <div style="flex: 1;">
                    <a href="/herbs/{herb_slug}.html">
                        <img 
                            style="height: 10rem; object-fit: cover;"
                            src="{card_img_src}"
                        >
                    </a>
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
            <h2 style="font-size: 1.8rem;">About Author</h2>
            <img 
                style="margin-bottom: 1.6rem; height: 40rem; object-fit: cover; object-position: top;"
                src="/images/leen-randell.jpg"
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
    url_slug = f'herbs'
    ###
    json_article_filepath = f'''{g.DATABASE_FOLDERPATH}/json/{url_slug}.json'''
    json_article = io.json_read(json_article_filepath, create=True)
    json_article['url'] = url_slug
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
                Write a detailed paragraph in 5 sentences for a page in my website.
                This page is about listing 1000+ medicinal herbs.
                Start with the following words: This page .
            '''
            prompt += f'/no_think'
            reply = llm.reply(prompt).strip()
            if '</think>' in reply:
                reply = reply.split('</think>')[1].strip()
            reply = polish.vanilla(reply)
            json_article[key] = reply
            io.json_write(json_article_filepath, json_article)
    ###
    groups = groups_gen(herbs_primary_medicinal, 15)
    for group_i, group in enumerate(groups):
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
            <section class="container-xl" style="margin-bottom: 6.4rem;">
                {sections.breadcrumbs(url_slug)}
                <h1 style="margin-top: 4.8rem;">Browse 1000+ Medicinal Herbs</h1>
            </section>
        '''
        intro_paragraphs = [f'{line}.'.replace('..', '.') for line in json_article['intro'].strip().split('. ')]
        intro_paragraphs_html = ''
        for intro_paragraph in intro_paragraphs:
            intro_paragraphs_html += f'''
                <p style="max-width: 76.8rem; margin: 0 auto; 
                    color: #ffffff; font-size: 1.8rem; line-height: 2.7rem;
                    padding-left: 3.2rem;
                    padding-right: 3.2rem;
                    margin-bottom: 1.6rem;
                ">
                    {intro_paragraph}
                </p>
            '''
        html_intro = f'''
            <section style="margin-bottom: 9.6rem; padding: 8.0rem 5%; background-color: #222222;">
                <div class="">
                    <div style="display: flex;">
                        <div style="flex: 1;">
                            <img style="
                                    display: block; height: 60rem; object-fit: cover;
                                    padding-right: 3.2rem; border-right: 1px solid #444444;
                                " 
                                src="/images/herbs/adiantum-capillus-veneris.jpg">
                        </div>
                        <div style="flex: 1; display: flex; flex-direction: column; justify-content: center;">
                            {intro_paragraphs_html}
                        </div>
                    </div>
                </div>
            </section>
        '''
        ###
        html_cards = ''
        for i in range(len(group)):
            herb = group[i]
            herb_slug = herb['herb_slug']
            herb_name_scientific = herb['herb_name_scientific']
            ###
            json_entity_filepath = f'''{g.DATABASE_FOLDERPATH}/ssot/herbs/herbs-primary/{herb_slug}.json'''
            json_entity = io.json_read(json_entity_filepath)
            herb_names_common = [name['answer'].title() for name in json_entity['herb_names_common']]
            herb_name_common = herb_names_common[0]
            ###
            card_img_src = f'/images/herbs/{herb_slug}.jpg'
            card_title = herb_name_scientific.capitalize()
            # card_title = herb_name_common.title().replace("'S", "'s")
            card_subtitle = herb_name_common.title().replace("'S", "'s")
            ###
            json_herb = io.json_read(f'{g.DATABASE_FOLDERPATH}/json/herbs/{herb_slug}.json')
            print(json_herb)
            card_article_preview = json_herb['intro']
            card_desc = ' '.join(card_article_preview.split(' ')[:16]) + '...'
            ###
            html_card = card_primary_gen(i, card_img_src, herb_slug, card_title, card_desc, card_subtitle)
            html_cards += html_card
        ###
        html_sidebar = sidebar_gen()
        ###
        meta_title = f'''Herbs'''
        meta_description = f''''''
        ###
        pagination_html = pagination_gen(group_i, groups, url_slug)
        ###
        ### HERBS
        ########################################
        html_herbs = f'''
            <section style="max-width: 175rem; margin: 0 auto; padding-left: 1.6rem; padding-right: 1.6rem;">
                <div style="display: flex;">
                    <div style="flex: 1;">
                        {html_sidebar}
                    </div>
                    <div style="flex: 3; 
                            padding-left: 4.8rem; border-left: 1px solid #e7e7e7; 
                        ">
                        {categories_html}
                        <div style="padding-top: 3.2rem; border-top: 1px solid #e7e7e7;">
                            <div class="grid-3">
                                {html_cards}
                            </div>
                        </div>
                        <div style="display: flex; justify-content: center; gap: 0.8rem;">
                            {pagination_html}
                        </div>
                    </div>
                </div>
            </section>
        '''
        html_main += f'''
            {html_title}
            {html_intro}
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

def page_herbs_top_gen():
    url_slug = f'herbs/top'
    ###
    json_article_filepath = f'''{g.DATABASE_FOLDERPATH}/json/{url_slug}.json'''
    json_article = io.json_read(json_article_filepath, create=True)
    json_article['url'] = url_slug
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
                Write a detailed paragraph in 5 sentences for a page in my website.
                This page is about listing the top 10 medicinal herbs.
                Include "top 10".
                Don't mention the herb names.
                Start with the following words: This page .
            '''
            prompt += f'/no_think'
            reply = llm.reply(prompt).strip()
            if '</think>' in reply:
                reply = reply.split('</think>')[1].strip()
            reply = polish.vanilla(reply)
            json_article[key] = reply
            io.json_write(json_article_filepath, json_article)
    ###
    groups = groups_gen(herbs_top, 15)
    for group_i, group in enumerate(groups):
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
            <section class="container-xl" style="margin-bottom: 6.4rem;">
                {sections.breadcrumbs(url_slug)}
                <h1 style="margin-top: 4.8rem;">Top 10 Medicinal Herbs</h1>
            </section>
        '''
        intro_paragraphs = [f'{line}.'.replace('..', '.') for line in json_article['intro'].strip().split('. ')]
        intro_paragraphs_html = ''
        for intro_paragraph in intro_paragraphs:
            intro_paragraphs_html += f'''
                <p style="max-width: 76.8rem; margin: 0 auto; 
                    color: #ffffff; font-size: 1.8rem; line-height: 2.7rem;
                    padding-left: 3.2rem;
                    padding-right: 3.2rem;
                    margin-bottom: 1.6rem;
                ">
                    {intro_paragraph}
                </p>
            '''
        html_intro = f'''
            <section style="margin-bottom: 9.6rem; padding: 8.0rem 5%; background-color: #222222;">
                <div class="">
                    <div style="display: flex;">
                        <div style="flex: 1;">
                            <img style="
                                    display: block; height: 60rem; object-fit: cover;
                                    padding-right: 3.2rem; border-right: 1px solid #444444;
                                " 
                                src="/images/herbs/adiantum-capillus-veneris.jpg">
                        </div>
                        <div style="flex: 1; display: flex; flex-direction: column; justify-content: center;">
                            {intro_paragraphs_html}
                        </div>
                    </div>
                </div>
            </section>
        '''
        ###
        html_cards = ''
        for i in range(len(group)):
            herb = group[i]
            herb_name_scientific = herb['herb_name_scientific']
            herb_slug = polish.sluggify(herb_name_scientific)
            ###
            json_entity_filepath = f'''{g.DATABASE_FOLDERPATH}/ssot/herbs/herbs-primary/{herb_slug}.json'''
            json_entity = io.json_read(json_entity_filepath)
            herb_names_common = [name['answer'].title() for name in json_entity['herb_names_common']]
            herb_name_common = herb_names_common[0]
            ###
            card_img_src = f'/images/herbs/{herb_slug}.jpg'
            card_title = herb_name_scientific.capitalize()
            card_subtitle = herb_name_common.title().replace("'S", "'s")
            ###
            json_article = io.json_read(f'{g.DATABASE_FOLDERPATH}/json/herbs/{herb_slug}.json')
            print(json_article)
            card_article_preview = json_article['intro']
            card_desc = ' '.join(card_article_preview.split(' ')[:16]) + '...'
            ###
            html_card = card_primary_gen(i, card_img_src, herb_slug, card_title, card_desc, card_subtitle)
            html_cards += html_card
        ###
        html_sidebar = sidebar_gen()
        ###
        meta_title = f'''Herbs'''
        meta_description = f''''''
        pagination_html = pagination_gen(group_i, groups, url_slug)
        ###
        ### HERBS
        ########################################
        html_herbs = f'''
            <section style="max-width: 175rem; margin: 0 auto; padding-left: 1.6rem; padding-right: 1.6rem;">
                <div style="display: flex;">
                    <div style="flex: 1;">
                        {html_sidebar}
                    </div>
                    <div style="flex: 3; 
                            padding-left: 4.8rem; border-left: 1px solid #e7e7e7; 
                        ">
                        {categories_html}
                        <div style="padding-top: 3.2rem; border-top: 1px solid #e7e7e7;">
                            <div class="grid-3">
                                {html_cards}
                            </div>
                        </div>
                        <div style="display: flex; justify-content: center; gap: 0.8rem;">
                            {pagination_html}
                        </div>
                    </div>
                </div>
            </section>
        '''
        html_main += f'''
            {html_title}
            {html_intro}
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

def page_herbs_popular_gen():
    url_slug = f'herbs/popular'
    ###
    json_article_filepath = f'''{g.DATABASE_FOLDERPATH}/json/{url_slug}.json'''
    json_article = io.json_read(json_article_filepath, create=True)
    json_article['url'] = url_slug
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
                Write a detailed paragraph in 5 sentences for a page in my website.
                This page is about listing the popular 100 medicinal herbs.
                Include "popular 100".
                Don't mention the herb names.
                Start with the following words: This page .
            '''
            prompt += f'/no_think'
            reply = llm.reply(prompt).strip()
            if '</think>' in reply:
                reply = reply.split('</think>')[1].strip()
            reply = polish.vanilla(reply)
            json_article[key] = reply
            io.json_write(json_article_filepath, json_article)
    ###
    groups = groups_gen(herbs_popular, 15)
    for group_i, group in enumerate(groups):
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
            <section class="container-xl" style="margin-bottom: 6.4rem;">
                {sections.breadcrumbs(url_slug)}
                <h1 style="margin-top: 4.8rem;">Popular 100 Medicinal Herbs</h1>
            </section>
        '''
        intro_paragraphs = [f'{line}.'.replace('..', '.') for line in json_article['intro'].strip().split('. ')]
        intro_paragraphs_html = ''
        for intro_paragraph in intro_paragraphs:
            intro_paragraphs_html += f'''
                <p style="max-width: 76.8rem; margin: 0 auto; 
                    color: #ffffff; font-size: 1.8rem; line-height: 2.7rem;
                    padding-left: 3.2rem;
                    padding-right: 3.2rem;
                    margin-bottom: 1.6rem;
                ">
                    {intro_paragraph}
                </p>
            '''
        html_intro = f'''
            <section style="margin-bottom: 9.6rem; padding: 8.0rem 5%; background-color: #222222;">
                <div class="">
                    <div style="display: flex;">
                        <div style="flex: 1;">
                            <img style="
                                    display: block; height: 60rem; object-fit: cover;
                                    padding-right: 3.2rem; border-right: 1px solid #444444;
                                " 
                                src="/images/herbs/adiantum-capillus-veneris.jpg">
                        </div>
                        <div style="flex: 1; display: flex; flex-direction: column; justify-content: center;">
                            {intro_paragraphs_html}
                        </div>
                    </div>
                </div>
            </section>
        '''
        ###
        html_cards = ''
        for i in range(len(group)):
            herb = group[i]
            herb_name_scientific = herb['herb_name_scientific']
            herb_slug = polish.sluggify(herb_name_scientific)
            ###
            json_entity_filepath = f'''{g.DATABASE_FOLDERPATH}/ssot/herbs/herbs-primary/{herb_slug}.json'''
            json_entity = io.json_read(json_entity_filepath)
            herb_names_common = [name['answer'].title() for name in json_entity['herb_names_common']]
            herb_name_common = herb_names_common[0]
            ###
            card_img_src = f'/images/herbs/{herb_slug}.jpg'
            card_title = herb_name_scientific.capitalize()
            card_subtitle = herb_name_common.title().replace("'S", "'s")
            ###
            json_herb = io.json_read(f'{g.DATABASE_FOLDERPATH}/json/herbs/{herb_slug}.json')
            print(json_herb)
            card_article_preview = json_herb['intro']
            card_desc = ' '.join(card_article_preview.split(' ')[:16]) + '...'
            ###
            html_card = card_primary_gen(i, card_img_src, herb_slug, card_title, card_desc, card_subtitle)
            html_cards += html_card
        ###
        html_sidebar = sidebar_gen()
        ###
        meta_title = f'''Herbs'''
        meta_description = f''''''
        pagination_html = pagination_gen(group_i, groups, url_slug)
        ###
        ### HERBS
        ########################################
        html_herbs = f'''
            <section style="max-width: 175rem; margin: 0 auto; padding-left: 1.6rem; padding-right: 1.6rem;">
                <div style="display: flex;">
                    <div style="flex: 1;">
                        {html_sidebar}
                    </div>
                    <div style="flex: 3; 
                            padding-left: 4.8rem; border-left: 1px solid #e7e7e7; 
                        ">
                        {categories_html}
                        <div style="padding-top: 3.2rem; border-top: 1px solid #e7e7e7;">
                            <div class="grid-3">
                                {html_cards}
                            </div>
                        </div>
                        <div style="display: flex; justify-content: center; gap: 0.8rem;">
                            {pagination_html}
                        </div>
                    </div>
                </div>
            </section>
        '''
        html_main += f'''
            {html_title}
            {html_intro}
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

def page_herbs_unverified_gen():
    herbs_herbs_wcvp_medicinal = data.herbs_wcvp_medicinal_get()
    print(len(herbs_herbs_wcvp_medicinal))
    ###
    url_slug = f'herbs/unverified'
    ###
    json_article_filepath = f'''{g.DATABASE_FOLDERPATH}/json/{url_slug}.json'''
    json_article = io.json_read(json_article_filepath, create=True)
    json_article['url'] = url_slug
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
                Write a detailed paragraph in 5 sentences for a page in my website.
                This page is about a massive listing of more than 130.000 medicinal herbs.
                Include "more than 130.000" somewhere at the start.
                Stress the fact that this list a curation of all the info we could find around the web about less known herbs, but most of these info are neither verified by known folk practice nor modern scientific studies, so usage is highly discouraged and more investigation is required.
                Start with the following words: This page .
            '''
            prompt += f'/no_think'
            reply = llm.reply(prompt).strip()
            if '</think>' in reply:
                reply = reply.split('</think>')[1].strip()
            reply = polish.vanilla(reply)
            json_article[key] = reply
            io.json_write(json_article_filepath, json_article)
    ###
    groups = groups_gen(herbs_herbs_wcvp_medicinal, 15)
    for group_i, group in enumerate(groups):
        print(f'{group_i}/{len(groups)}')
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
            <section class="container-xl" style="margin-bottom: 6.4rem;">
                {sections.breadcrumbs(url_slug)}
                <h1 style="margin-top: 4.8rem;">130.000+ Unverified Medicinal Herbs</h1>
            </section>
        '''
        intro_paragraphs = [f'{line}.'.replace('..', '.') for line in json_article['intro'].strip().split('. ')]
        intro_paragraphs_html = ''
        for intro_paragraph in intro_paragraphs:
            intro_paragraphs_html += f'''
                <p style="max-width: 76.8rem; margin: 0 auto; 
                    color: #ffffff; font-size: 1.8rem; line-height: 2.7rem;
                    padding-left: 3.2rem;
                    padding-right: 3.2rem;
                    margin-bottom: 1.6rem;
                ">
                    {intro_paragraph}
                </p>
            '''
        html_intro = f'''
            <section style="margin-bottom: 9.6rem; padding: 8.0rem 5%; background-color: #222222;">
                <div class="">
                    <div style="display: flex;">
                        <div style="flex: 1;">
                            <img style="
                                    display: block; height: 60rem; object-fit: cover;
                                    padding-right: 3.2rem; border-right: 1px solid #444444;
                                " 
                                src="/images/herbs/adiantum-capillus-veneris.jpg">
                        </div>
                        <div style="flex: 1; display: flex; flex-direction: column; justify-content: center;">
                            {intro_paragraphs_html}
                        </div>
                    </div>
                </div>
            </section>
        '''
        ###
        html_cards = ''
        for i in range(len(group)):
            herb = group[i]
            herb_name_scientific = herb['herb_name_scientific']
            herb_slug = polish.sluggify(herb_name_scientific)
            ###
            json_entity_filepath = f'''{g.DATABASE_FOLDERPATH}/ssot/herbs/herbs-wcvp/medicinal/{herb_slug}.json'''
            json_entity = io.json_read(json_entity_filepath)
            herb_names_common = [name['answer'].title() for name in json_entity['herb_names_common']]
            herb_name_common = herb_names_common[0]
            ###
            card_img_src = f'/images/herbs/{herb_slug}.jpg'
            card_img_src = f'/images/no-image.jpg'
            card_title = herb_name_scientific.capitalize()
            card_subtitle = herb_name_common.title().replace("'S", "'s")
            ###
            json_article_plant = io.json_read(f'{g.DATABASE_FOLDERPATH}/json/herbs/{herb_slug}.json')
            card_article_preview = ''
            try: card_article_preview = json_article_plant['intro']
            except: pass
            card_desc = ' '.join(card_article_preview.split(' ')[:16]) + '...'
            ###
            html_card = card_primary_gen(i, card_img_src, herb_slug, card_title, card_desc, card_subtitle)
            html_cards += html_card
        ###
        html_sidebar = sidebar_gen()
        ###
        meta_title = f'''Herbs'''
        meta_description = f''''''
        pagination_html = pagination_gen(group_i, groups, url_slug)
        ###
        ### HERBS
        ########################################
        html_herbs = f'''
            <section style="max-width: 175rem; margin: 0 auto; padding-left: 1.6rem; padding-right: 1.6rem;">
                <div style="display: flex;">
                    <div style="flex: 1;">
                        {html_sidebar}
                    </div>
                    <div style="flex: 3; 
                            padding-left: 4.8rem; border-left: 1px solid #e7e7e7; 
                        ">
                        {categories_html}
                        <div style="padding-top: 3.2rem; border-top: 1px solid #e7e7e7;">
                            <div class="grid-3">
                                {html_cards}
                            </div>
                        </div>
                        <div style="display: flex; justify-content: center; gap: 0.8rem;">
                            {pagination_html}
                        </div>
                    </div>
                </div>
            </section>
        '''
        html_main += f'''
            {html_title}
            {html_intro}
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
    # herbs_herb_primary_gen()
    # article_herbs_herb_wcvp_gen()

    # page_herbs_top_gen()
    # page_herbs_popular_gen()
    # page_herbs_unverified_gen()

    # page_herbs_gen()

