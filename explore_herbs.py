import os
import json
import shutil
import sqlite3

from lorem_text import lorem

from lib import g
from lib import io
from lib import llm
from lib import data
from lib import polish
from lib import sections
from lib import components

import masterize_utils

shutil.copy2('styles.css', f'{g.website_folderpath}/styles.css')

model_filepath = '/home/ubuntu/vault-tmp/llm/gemma-4-26B-A4B-it-UD-Q4_K_XL.gguf'

sidebar_activities_rows = None
sidebar_chemicals_rows = None

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

def hero_html_gen(title):
    plants_rows = masterize_utils.masterize_plants_get_all()
    activities_rows = masterize_utils.masterize_activities_get_all()
    chemicals_rows = masterize_utils.masterize_chemicals_get_all()

    ### STATS
    plants_num = len(plants_rows)
    activities_num = len(activities_rows)
    chemicals_num = len(chemicals_rows)
    studies_num = len(os.listdir(f'{g.VAULT_FOLDERPATH}/terrawhisper/data/fetch/pubmed/medicinal_plant/abstracts'))
    '''
                    <div style="display: flex; align-items: center;">
                        <h1 style="font-size: 1.4rem; margin-bottom: 0; margin-top: 2px;">
                            {title}
                        </h1>
                        <span style="font-weight: 400;">: A scientifically curated directory of plants, their bioactive compounds, traditional uses, and research evidence</span>
                    </div>
    '''
    html = f'''
        <section
            style="
                padding-top: 1.6rem;
                padding-bottom: 1.6rem;
                box-shadow: rgba(0, 0, 0, 0.05) 0px 6px 24px 0px, rgba(0, 0, 0, 0.08) 0px 0px 0px 1px;
                margin-bottom: 3.2rem;
            "
        >
            <div class="container-xxl">
                <div class="explorer-hero">
                    <h1 style="font-size: 1.4rem; margin-bottom: 0;">
                        {title}
                    </h1>
                    <ul style="list-style: none; display: flex; align-items: center; gap: 1.2rem; font-size: 1.4rem;">
                        <li>{plants_num} Plants</li> <span>|</span>
                        <li>{chemicals_num} Compounds</li> <span>|</span>
                        <li>{activities_num} Activities</li> <span>|</span>
                        <li>{studies_num} Studies</li>
                    </ul>
                </div>
            </div>
        </section>
    '''
    return html

def sidebar_activities_get():
    global sidebar_activities_rows 
    db_filepath = f'{g.VAULT_FOLDERPATH}/terrawhisper/data/qualify/observations.db'
    conn = sqlite3.connect(db_filepath)
    cursor = conn.execute("""
        SELECT
            activity_canonical_name,
            COUNT(DISTINCT source_name) AS source_count
        FROM plants_activities
        GROUP BY activity_canonical_name
        ORDER BY source_count DESC, activity_canonical_name ASC;
    """)
    rows = cursor.fetchall()
    conn.close()
    sidebar_activities_rows = rows

def sidebar_chemicals_get():
    global sidebar_chemicals_rows 
    db_filepath = f'{g.VAULT_FOLDERPATH}/terrawhisper/data/qualify/observations.db'
    conn = sqlite3.connect(db_filepath)
    cursor = conn.execute("""
        SELECT
            chemical_canonical_name,
            COUNT(DISTINCT source_name) AS source_count
        FROM plants_chemicals
        GROUP BY chemical_canonical_name
        ORDER BY source_count DESC, chemical_canonical_name ASC;
    """)
    rows = cursor.fetchall()
    conn.close()
    sidebar_chemicals_rows = rows

def sidebar_html_gen():
    li_a_style = f'''text-decoration: none; color: #111; font-size: 1.4rem; display: inline-block;'''

    ### ALPHABET
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
    alphabet_html = ''
    alphabet_html += '<ul style="list-style: none; display: grid; grid-template-columns: repeat(7, 1fr); gap: 0.8rem;">'
    for letter in letters:
        alphabet_html += f'''
            <a style="{li_a_style}" href="/herbs/alphabet/{letter}.html">
                <li style="border: 1px solid #cdcdcd; display: flex; justify-content: center; align-items: center; padding: 0.4rem 0.8rem;">
                    {letter.upper()}
                </li>
            </a>
        '''
    alphabet_html += '</ul>'

    activities_html = ''
    activities_html += f'''<ul style="list-style: none; display: flex; flex-direction: column; gap: 0.4rem;">'''
    for row in sidebar_activities_rows[:10]:
        activity_name = row[0]
        activity_slug = polish.sluggify(activity_name)
        activities_html += f'''
            <li>
                <a style="{li_a_style}" href="/herbs/activities/{activity_slug}.html">{activity_name}</a>
            </li>
        '''
    activities_html += f'''</ul>'''

    chemicals_html = ''
    chemicals_html += f'''<ul style="list-style: none; display: flex; flex-direction: column; gap: 0.4rem;">'''
    for row in sidebar_chemicals_rows[:10]:
        chemical_name = row[0]
        chemical_name = chemical_name[0].upper() + chemical_name[1:]
        chemical_slug = polish.sluggify(chemical_name)
        chemicals_html += f'''
            <li>
                <a style="{li_a_style}" href="/herbs/chemicals/{chemical_slug}.html">{chemical_name}</a>
            </li>
        '''
    chemicals_html += f'''</ul>'''

    # TODO: body systems    
    '''
            <h3 style="font-size: 1.4rem; letter-spacing: 0.5px; margin-bottom: 1.4rem;">
                body systems
            </h3>
            <ul style="list-style: none; display: flex; flex-direction: column; gap: 0.4rem;">
                <li>
                    <a style="{li_a_style}" href="/herbs.html">digestive</a>
                </li>
                <li>
                    <a style="{li_a_style}" href="/herbs.html">immune</a>
                </li>
                <li>
                    <a style="{li_a_style}" href="/herbs.html">nervous</a>
                </li>
                <li>
                    <a style="{li_a_style}" href="/herbs.html">respiratory</a>
                </li>
                <li>
                    <a style="{li_a_style}" href="/herbs.html">cardiovascular</a>
                </li>
                <li>
                    <a style="{li_a_style}" href="/herbs.html">skin</a>
                </li>
                <li>
                    <a style="{li_a_style}" href="/herbs.html">urinary</a>
                </li>
                <li>
                    <a style="{li_a_style}" href="/herbs.html">musculoskeletal</a>
                </li>
            </ul>
            <a style="{li_a_style} margin-top: 1.6rem;" href="/herbs.html">view all →</a>
            <hr style="border: 0; border-bottom: 1px solid #d8d8d8; margin-top: 2.4rem; margin-bottom: 2.4rem;">
    '''

    # TODO: plant parts    
    '''
            <h3 style="font-size: 1.4rem; letter-spacing: 0.5px; margin-bottom: 1.4rem;">
                plant parts
            </h3>
            <ul style="list-style: none; display: flex; flex-direction: column; gap: 0.4rem;">
                <li>
                    <a style="{li_a_style}" href="/herbs.html">root</a>
                </li>
                <li>
                    <a style="{li_a_style}" href="/herbs.html">leaf</a>
                </li>
                <li>
                    <a style="{li_a_style}" href="/herbs.html">flower</a>
                </li>
                <li>
                    <a style="{li_a_style}" href="/herbs.html">seed</a>
                </li>
                <li>
                    <a style="{li_a_style}" href="/herbs.html">fruit</a>
                </li>
                <li>
                    <a style="{li_a_style}" href="/herbs.html">bark</a>
                </li>
                <li>
                    <a style="{li_a_style}" href="/herbs.html">rhizome</a>
                </li>
                <li>
                    <a style="{li_a_style}" href="/herbs.html">whole plant</a>
                </li>
            </ul>
            <a style="{li_a_style} margin-top: 1.6rem;" href="/herbs.html">view all →</a>
            <hr style="border: 0; border-bottom: 1px solid #d8d8d8; margin-top: 2.4rem; margin-bottom: 2.4rem;">
    '''

    # TODO: families
    '''
            <h3 style="font-size: 1.4rem; letter-spacing: 0.5px; margin-bottom: 1.4rem;">
                botanical families
            </h3>
            <ul style="list-style: none; display: flex; flex-direction: column; gap: 0.4rem;">
                <li>
                    <a style="{li_a_style}" href="/herbs.html">lamiaceae</a>
                </li>
                <li>
                    <a style="{li_a_style}" href="/herbs.html">asteraceae</a>
                </li>
                <li>
                    <a style="{li_a_style}" href="/herbs.html">fabaceae</a>
                </li>
                <li>
                    <a style="{li_a_style}" href="/herbs.html">apiaceae</a>
                </li>
                <li>
                    <a style="{li_a_style}" href="/herbs.html">rosaceae</a>
                </li>
                <li>
                    <a style="{li_a_style}" href="/herbs.html">rutaceae</a>
                </li>
            </ul>
            <a style="{li_a_style} margin-top: 1.6rem;" href="/herbs.html">view all →</a>
            <hr style="border: 0; border-bottom: 1px solid #d8d8d8; margin-top: 2.4rem; margin-bottom: 2.4rem;">
    '''

    # TODO: geography
    '''
            <h3 style="font-size: 1.4rem; letter-spacing: 0.5px; margin-bottom: 1.4rem;">
                geographic origin
            </h3>
            <ul style="list-style: none; display: flex; flex-direction: column; gap: 0.4rem;">
                <li>
                    <a style="{li_a_style}" href="/herbs.html">europe</a>
                </li>
                <li>
                    <a style="{li_a_style}" href="/herbs.html">asia</a>
                </li>
                <li>
                    <a style="{li_a_style}" href="/herbs.html">africa</a>
                </li>
                <li>
                    <a style="{li_a_style}" href="/herbs.html">north america</a>
                </li>
                <li>
                    <a style="{li_a_style}" href="/herbs.html">south america</a>
                </li>
                <li>
                    <a style="{li_a_style}" href="/herbs.html">oceania</a>
                </li>
            </ul>
            <a style="{li_a_style} margin-top: 1.6rem;" href="/herbs.html">view all →</a>
            <hr style="border: 0; border-bottom: 1px solid #d8d8d8; margin-top: 2.4rem; margin-bottom: 2.4rem;">
    '''

    # TODO: traditions
    '''
            <h3 style="font-size: 1.4rem; letter-spacing: 0.5px; margin-bottom: 1.4rem;">
                traditional medicine
            </h3>
            <ul style="list-style: none; display: flex; flex-direction: column; gap: 0.4rem;">
                <li>
                    <a style="{li_a_style}" href="/herbs.html">ayurveda</a>
                </li>
                <li>
                    <a style="{li_a_style}" href="/herbs.html">traditional chinese medicine</a>
                </li>
                <li>
                    <a style="{li_a_style}" href="/herbs.html">western herbalism</a>
                </li>
                <li>
                    <a style="{li_a_style}" href="/herbs.html">unani</a>
                </li>
                <li>
                    <a style="{li_a_style}" href="/herbs.html">native america</a>
                </li>
                <li>
                    <a style="{li_a_style}" href="/herbs.html">african traditional medicine</a>
                </li>
            </ul>
            <a style="{li_a_style} margin-top: 1.6rem;" href="/herbs.html">view all →</a>
    '''

    sidebar_html = f'''
        <div 
            style=" 
            "
        >
            <h2 style="font-size: 1.4rem; letter-spacing: 0.5px; margin-bottom: 1.4rem;">
                Explore Herbs
            </h2>
            <ul style="list-style: none; display: flex; flex-direction: column; gap: 0.4rem;">
                <li>
                    <a style="text-decoration: none; color: #111; font-size: 1.4rem;" href="/herbs.html">All Herbs</a>
                </li>
                <li>
                    <a style="text-decoration: none; color: #111; font-size: 1.4rem;" href="/herbs.html">Popular Herbs</a>
                </li>
                <li>
                    <a style="text-decoration: none; color: #111; font-size: 1.4rem;" href="/herbs.html">Recently Added</a>
                </li>
            </ul>
            <hr style="border: 0; border-bottom: 1px solid #d8d8d8; margin-top: 2.4rem; margin-bottom: 2.4rem;">

            <a href="/herbs/alphabet.html">
                <h3 style="font-size: 1.4rem; letter-spacing: 0.5px; margin-bottom: 1.4rem;">Alphabet</h3>
            </a>
            {alphabet_html}
            <hr style="border: 0; border-bottom: 1px solid #d8d8d8; margin-top: 2.4rem; margin-bottom: 2.4rem;">

            <a href="/herbs/activities.html">
                <h3 style="font-size: 1.4rem; letter-spacing: 0.5px; margin-bottom: 1.4rem;">Biological Activity</h3>
            </a>
            {activities_html}
            <a style="{li_a_style} margin-top: 1.6rem;" href="/herbs/activities.html">View all →</a>
            <hr style="border: 0; border-bottom: 1px solid #d8d8d8; margin-top: 2.4rem; margin-bottom: 2.4rem;">

            <a href="/herbs/chemicals.html">
                <h3 style="font-size: 1.4rem; letter-spacing: 0.5px; margin-bottom: 1.4rem;">Bioactive Compounds</h3>
            </a>
            {chemicals_html}
            <a style="{li_a_style} margin-top: 1.6rem;" href="/herbs/chemicals.html">View all →</a>

        </div>
    '''
    return sidebar_html

def cards_header_html_gen(group_i, page_cards_num, total_items_num, title):
    from_num = page_cards_num*group_i+1
    to_num = page_cards_num*group_i+page_cards_num
    if to_num > total_items_num: to_num = total_items_num
    html = f'''
        <div class="m-flex" style="justify-content: space-between; align-items: center; margin-bottom: 2.4rem;">
            <h2 style="font-size: 2.4rem;">
               {title}
            </h2>
            <span style="font-size: 1.4rem;">Showing {from_num}-{to_num}  out of {total_items_num} results</span>
        </div>
    '''
    return html

def cards_html_gen(group):
    cards_html = ''
    for plant_row in group[:]:
        plant_name = plant_row['plant_name_canonical']
        plant_slug = polish.sluggify(plant_name)
        plant_img_src = f'/images/herbs/{plant_slug}.jpg'
        plant_filepath = f'{g.WEBSITE_FOLDERPATH}/images/herbs/{plant_slug}.jpg'
        json_article_filepath = f'''{g.DATA_FOLDERPATH}/enhance/{plant_slug}.json'''
        try: json_article = io.json_read(json_article_filepath) # TODO: fixe missing/extra? plants
        except: continue
        plant_desc = ' '.join(json_article['intro'].split(' ')[:16]).strip()
        if plant_desc[-1] == '.': plant_desc = plant_desc[:-1]
        plant_desc += '...'
        cards_html += f'''
            <article>
                <a href="/herbs/{plant_slug}.html" style="text-decoration: none;">
                    <img src="{plant_img_src}" alt="{plant_name}" style="margin-bottom: 1.6rem;">
                    <h3 class="explorer-card-title">{plant_name}</h3>
                </a>
                <p style="font-size: 1.4rem;">{plant_desc}</p>
            </article>
        '''
    return cards_html

def pagination_html_gen(group_i, groups, url_slug):
    ### prev
    if group_i > 1:
        prev_html = f'''
            <a rel="prev" href="/{url_slug}/page/{group_i}.html">PREV</a>
        '''
    elif group_i > 0:
        prev_html = f'''
            <a rel="prev" href="/{url_slug}.html">PREV</a>
        '''
    else:
        prev_html = f''
    ### numbers
    numbers_html = ''
    prev_num = 1
    next_num = 1
    ### first
    if group_i != 0:
        number_html = f'''
            <a href="/{url_slug}.html">1</a>
        '''
        numbers_html += number_html
    ### current prev ...
    if group_i > prev_num + 1:
        number_html = f'''
            <span>...</span>
        '''
        numbers_html += number_html
    ### current prev
    for i in range(prev_num, 0, -1):
        page_index = group_i+1-i
        if page_index > 1:
            number_html = f'''
                <a href="/{url_slug}/page/{page_index}.html">{page_index}</a>
            '''
            numbers_html += number_html
    ### current
    number_html = f'''
        <span class="p-cur">
            {group_i+1}
        </span>
    '''
    numbers_html += number_html
    ### current next
    for i in range(next_num):
        page_index = group_i+1+i+1
        if page_index < len(groups):
            number_html = f'''
                <a href="/{url_slug}/page/{page_index}.html">{page_index}</a>
            '''
            numbers_html += number_html
    ### current next ...
    if group_i < len(groups)-1 - next_num+1:
        number_html = f'''
            <span>...</span>
        '''
        numbers_html += number_html
    ### last
    if group_i != len(groups)-1:
        number_html = f'''
            <a href="/{url_slug}/page/{len(groups)}.html">{len(groups)}</a>
        '''
        numbers_html += number_html
    ### next
    if group_i != len(groups)-1:
        next_html = f'''
            <a rel="next" href="/{url_slug}/page/{group_i+2}.html">NEXT</a>
        '''
    else:
        next_html = f''
    pagination_html = f'''
        {prev_html}
        {numbers_html}
        {next_html}
    '''
    return pagination_html

def herbs_index():
    url_slug = 'herbs'

    ### GET ALL PLANTS -> TO LIST OF ITEMS
    # plants_rows = data.sqlite__plants_get()
    plants_rows = masterize_utils.masterize_plants_get_all()
    plants_data = [
        {
            'plant_id': row[0],
            'plant_name_canonical': row[1],
        }
        for row in plants_rows
    ]

    ### GROUP PLANTS IN PAGES
    page_cards_num = 48
    groups = groups_gen(plants_data, page_cards_num)

    ### GENERATE PAGES
    for group_i, group in enumerate(groups):
        print(f'{group_i}/{len(groups)}')
        ### PAGE URL
        if group_i == 0:
            html_filepath = f'''{g.website_folderpath}/herbs.html'''
        else:
            os.makedirs(f'''{g.website_folderpath}/herbs/page''', exist_ok=True)
            html_filepath = f'''{g.website_folderpath}/herbs/page/{group_i+1}.html'''


        hero_html = hero_html_gen(title='Explore all medicinal herbs')
        sidebar_html = sidebar_html_gen()
        cards_header_html = cards_header_html_gen(group_i, page_cards_num, len(plants_data), title='List of all herbs')
        cards_html = cards_html_gen(group)
        pagination_html = pagination_html_gen(group_i, groups, url_slug)

        html_article = ''
        html_article += f'''
            <section style="margin-bottom: 9.6rem;">
                <div class="explorer-layout" style="gap: 4.8rem;">
                    <div style="flex: 1;">
                        {sidebar_html}
                    </div>
                    <div style="flex: 3;">
                        {sections.breadcrumbs_explorer(url_slug)}
                        {cards_header_html}
                        <div class="grid-5" style="gap: 1.6rem; row-gap: 3.2rem;">
                            {cards_html}
                        </div>
                        <nav class="pagination">
                            <ul>
                                {pagination_html}
                            </ul>
                        </nav>
                    </div>
                </div>
            </section>
        '''

        ###
        meta_title = f'Medicinal Herbs'
        meta_description = ''
        canonical_html = f'''<link rel="canonical" href="https://terrawhisper.com/{url_slug}.html">'''
        head_html = components.html_head(
            meta_title, meta_description, css='/styles.css', canonical=canonical_html
        )
                # {sections.breadcrumbs_new(url_slug)}
        html = f''' 
            <!DOCTYPE html>
            <html lang="en">
            {head_html}
            <body style="background-color: #fff;">
                {sections.header_dark()}
                {hero_html}
                <main class="container-xxl explorer">
                    {html_article}
                </main>
                {sections.footer()}
            </body>
            </html>
        '''.strip()
        with open(html_filepath, 'w') as f: f.write(html)
        print(html_filepath)

def herbs_alphabet_category():
    url_slug = f'herbs/alphabet'
    io.folders_recursive_gen(f'''{g.website_folderpath}/{url_slug}''')
    html_filepath = f'''{g.website_folderpath}/{url_slug}.html'''

    hero_html = hero_html_gen(
        title='Explore herbs starting with letter'
    )
    sidebar_html = sidebar_html_gen()
    cards_header_html = cards_header_html_gen(0, 26, 26,
        title='List of herbs starting with letter'
    )

    alphabet_html = ''
    alphabet_letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
    for alphabet_letter in alphabet_letters:
        alphabet_letter_name = alphabet_letter[0]
        alphabet_letter_slug = polish.sluggify(alphabet_letter_name)
        ### GET PLANTS OF LETTER "?"
        plants_rows = masterize_utils.masterize_plants_get_all()
        plants_rows = sorted([row[1] for row in plants_rows])
        plants_data = [
            {
                'plant_name_canonical': name,
            }
            for name in plants_rows[:]
            if name.strip()[0].lower() == f'{alphabet_letter}'
        ]
        plants_html = f''
        for plant_item in plants_data[:3]:
            plant_name = plant_item['plant_name_canonical']
            plant_slug = polish.sluggify(plant_name)
            plants_html += f'''
                <div>
                    <img 
                        src="/images/herbs/{plant_slug}.jpg" 
                        style="margin-bottom: 0.8rem; width: 80px; height: 80px;"
                    >
                    <p style="font-size: 1.4rem;">{plant_name}</p>
                </div>
            '''
        ### DESCRIPTION
        plants_names_llm = ', '.join([x['plant_name_canonical'] for x in plants_data[:3]])
        idx = plants_names_llm.rfind(',')
        if idx != -1:
            plants_names_llm = plants_names_llm[:idx] + ', and' + plants_names_llm[idx + 1:]
        description_text = f'Browse medicinal herbs starting with the letter "{alphabet_letter.upper()}", such as {plants_names_llm}.'
        ###
        plants_count = len(plants_data)
        alphabet_html += f'''
            <article style="border: 1px solid #d8d8d8; margin-bottom: 1.6rem; padding: 1.6rem;">
                <div style="display: flex; gap: 4.8rem;">
                    <div style="flex: 2;">
                        <a href="/herbs/alphabet/{alphabet_letter_slug}.html" style="text-decoration: none;">
                            <h3 style="font-size: 1.8rem;">{alphabet_letter_name.upper()}</h3>
                        </a>
                        <p style="margin-bottom: 1.6rem;">{description_text}</p>
                        <p style="font-size: 1.4rem;"><span style="font-weight: 700;">Associated herbs:</span> {plants_count}</p>
                    </div>
                    <div style="flex: 1;">
                        <p style="font-size: 1.4rem; font-weight: 700; margin-bottom: 1.6rem;">Occurs naturally in</p>
                        <div class="grid-3" style="gap: 1.6rem;">
                            {plants_html}
                        </div>
                        <a 
                            style="color: #111; text-decoration: none; display: inline-block; margin-top: 1.6rem; font-size: 1.4rem;"
                            href="/herbs/alphabet/{alphabet_letter_slug}.html">View all {alphabet_letter_name} herbs →
                        </a>
                    </div>
                </div>
            </article>
        '''

    html_article = ''
    html_article += f'''
        <section style="margin-bottom: 9.6rem;">
            <div class="explorer-layout" style="gap: 4.8rem;">
                <div style="flex: 1;">
                    {sidebar_html}
                </div>
                <div style="flex: 3;">
                    {sections.breadcrumbs_explorer(url_slug)}
                    {cards_header_html}
                    {alphabet_html}
                </div>
            </div>
        </section>
    '''

    ###
    meta_title = f'Medicinal Herbs'
    meta_description = ''
    canonical_html = f'''<link rel="canonical" href="https://terrawhisper.com/{url_slug}.html">'''
    head_html = components.html_head(
        meta_title, meta_description, css='/styles.css', canonical=canonical_html
    )
            # {sections.breadcrumbs_new(url_slug)}
    html = f''' 
        <!DOCTYPE html>
        <html lang="en">
        {head_html}
        <body style="background-color: #fff;">
            {sections.header_dark()}
            {hero_html}
            <main class="container-xxl explorer">
                {html_article}
            </main>
            {sections.footer()}
        </body>
        </html>
    '''.strip()
    with open(html_filepath, 'w') as f: f.write(html)
    print(html_filepath)

    ### GROUP PLANTS IN PAGES
    page_cards_num = 48
    groups = groups_gen(sidebar_activities_rows, page_cards_num)

    ### GENERATE PAGES
    for group_i, group in enumerate(groups):
        print(f'{group_i}/{len(groups)}')
        ### PAGE URL
        if group_i == 0:
            html_filepath = f'''{g.website_folderpath}/{url_slug}.html'''
        else:
            os.makedirs(f'''{g.website_folderpath}/{url_slug}/page''', exist_ok=True)
            html_filepath = f'''{g.website_folderpath}/{url_slug}/page/{group_i+1}.html'''

        hero_html = hero_html_gen(
            title='Explore herbs biological activities'
        )
        sidebar_html = sidebar_html_gen()
        cards_header_html = cards_header_html_gen(group_i, page_cards_num, len(sidebar_activities_rows),
            title='List of herbs biological activities'
        )
        # cards_header_html = ''
        # cards_html = cards_html_gen(group)
        activities_html = f''
        for i, row in enumerate(group[:]):
            print(f'{i}/{len(group)}')
            activity_name = row[0]
            activity_slug = polish.sluggify(activity_name)

            conn = sqlite3.connect(f'{g.VAULT_FOLDERPATH}/terrawhisper/data/observe/observations.db')
            cur = conn.cursor()

            ### PLANTS NAMES
            cur.execute("""
                SELECT DISTINCT plant_canonical_name
                FROM plants_activities
                WHERE activity_canonical_name = ?
            """, (activity_name,))
            plants_rows = cur.fetchall()

            ### PLANTS COUNT
            cur.execute(
                """
                SELECT COUNT(DISTINCT plant_canonical_name)
                FROM plants_activities
                WHERE activity_canonical_name = ?
                """, (activity_name,)
            )
            plants_count = cur.fetchone()[0]

            conn.close()
            
            plants_html = f''
            for plant_row in plants_rows[:3]:
                plant_name = plant_row[0]
                plant_slug = polish.sluggify(plant_name)
                plants_html += f'''
                    <div>
                        <img 
                            src="/images/herbs/{plant_slug}.jpg" 
                            style="margin-bottom: 0.8rem; width: 80px; height: 80px;"
                        >
                        <p style="font-size: 1.4rem;">{plant_name}</p>
                    </div>
                '''

            ### DESCRIPTION
            json_article_filepath = f'''{g.DATA_FOLDERPATH}/explore/categories/activities.json'''
            json_article = io.json_read(json_article_filepath, create=True)
            regen = False
            key = f'activity_{activity_slug}'
            if key not in json_article: json_article[key] = ''
            if regen: json_article[key] = ''
            if json_article[key] == '':
                plants_names_llm = ','.join([x[0] for x in plants_rows[:3]])
                prompt = f'''
                    Write 2 sentences to explain the following biological activity of medicinal herbs: {activity_name}.
                    Include a sample on what herbs have this biological activity, like {plants_names_llm}.
                '''.strip()
                reply = llm.reply(prompt, model_filepath)
                if '</think>' in reply:
                    reply = reply.split('</think>')[1].strip()
                reply = polish.vanilla(reply)
                json_article[key] = reply
                io.json_write(json_article_filepath, json_article)
            description_text = json_article[key]

            activities_html += f'''
                <article style="border: 1px solid #d8d8d8; margin-bottom: 1.6rem; padding: 1.6rem;">
                    <div style="display: flex; gap: 4.8rem;">
                        <div style="flex: 2;">
                            <a href="/herbs/activities/{activity_slug}.html" style="text-decoration: none;">
                                <h3 style="font-size: 1.8rem;">{activity_name}</h3>
                            </a>
                            <p style="margin-bottom: 1.6rem;">{description_text}</p>
                            <p style="font-size: 1.4rem;"><span style="font-weight: 700;">Associated herbs:</span> {plants_count}</p>
                        </div>
                        <div style="flex: 1;">
                            <p style="font-size: 1.4rem; font-weight: 700; margin-bottom: 1.6rem;">Occurs naturally in</p>
                            <div class="grid-3" style="gap: 1.6rem;">
                                {plants_html}
                            </div>
                            <a 
                                style="color: #111; text-decoration: none; display: inline-block; margin-top: 1.6rem; font-size: 1.4rem;"
                                href="/herbs/activities/{activity_slug}.html">View all {activity_name} herbs →
                            </a>
                        </div>
                    </div>
                </article>
            '''
        pagination_html = pagination_html_gen(group_i, groups, url_slug)

        html_article = ''
        html_article += f'''
            <section style="margin-bottom: 9.6rem;">
                <div class="explorer-layout" style="gap: 4.8rem;">
                    <div style="flex: 1;">
                        {sidebar_html}
                    </div>
                    <div style="flex: 3;">
                        {sections.breadcrumbs_explorer(url_slug)}
                        {cards_header_html}
                        {activities_html}
                        <nav class="pagination">
                            <ul>
                                {pagination_html}
                            </ul>
                        </nav>
                    </div>
                </div>
            </section>
        '''

        ###
        meta_title = f'Medicinal Herbs'
        meta_description = ''
        canonical_html = f'''<link rel="canonical" href="https://terrawhisper.com/{url_slug}.html">'''
        head_html = components.html_head(
            meta_title, meta_description, css='/styles.css', canonical=canonical_html
        )
                # {sections.breadcrumbs_new(url_slug)}
        html = f''' 
            <!DOCTYPE html>
            <html lang="en">
            {head_html}
            <body style="background-color: #fff;">
                {sections.header_dark()}
                {hero_html}
                <main class="container-xxl explorer">
                    {html_article}
                </main>
                {sections.footer()}
            </body>
            </html>
        '''.strip()
        with open(html_filepath, 'w') as f: f.write(html)
        print(html_filepath)

def herbs_alphabet(alphabet_letter=''):
    if alphabet_letter == '': return

    url_slug = f'herbs/alphabet/{alphabet_letter}'
    io.folders_recursive_gen(f'''{g.website_folderpath}/{url_slug}''')

    ### GET ALL PLANTS -> TO LIST OF ITEMS
    # plants_rows = data.sqlite__plants_get()
    plants_rows = masterize_utils.masterize_plants_get_all()
    plants_rows = sorted([row[1] for row in plants_rows])
    plants_data = [
        {
            'plant_name_canonical': name,
        }
        for name in plants_rows[:]
        if name.strip()[0].lower() == f'{alphabet_letter}'
    ]

    ### GROUP PLANTS IN PAGES
    page_cards_num = 48
    groups = groups_gen(plants_data, page_cards_num)

    ### GENERATE PAGES
    for group_i, group in enumerate(groups):
        print(f'{group_i}/{len(groups)}')
        ### PAGE URL
        if group_i == 0:
            html_filepath = f'''{g.website_folderpath}/{url_slug}.html'''
        else:
            os.makedirs(f'''{g.website_folderpath}/{url_slug}/page''', exist_ok=True)
            html_filepath = f'''{g.website_folderpath}/{url_slug}/page/{group_i+1}.html'''


        hero_html = hero_html_gen(title=f'Explore herbs starting with letter "{alphabet_letter.upper()}"')
        sidebar_html = sidebar_html_gen()
        cards_header_html = cards_header_html_gen(group_i, page_cards_num, len(plants_data),
            title=f'List of herbs starting with letter "{alphabet_letter.upper()}"'
        )
        cards_html = cards_html_gen(group)
        pagination_html = pagination_html_gen(group_i, groups, url_slug)

        html_article = ''
        html_article += f'''
            <section style="margin-bottom: 9.6rem;">
                <div class="explorer-layout" style="gap: 4.8rem;">
                    <div style="flex: 1;">
                        {sidebar_html}
                    </div>
                    <div style="flex: 3;">
                        {sections.breadcrumbs_explorer(url_slug)}
                        {cards_header_html}
                        <div class="grid-5" style="gap: 1.6rem; row-gap: 3.2rem;">
                            {cards_html}
                        </div>
                        <nav class="pagination">
                            <ul>
                                {pagination_html}
                            </ul>
                        </nav>
                    </div>
                </div>
            </section>
        '''

        ###
        meta_title = f'Medicinal Herbs'
        meta_description = ''
        canonical_html = f'''<link rel="canonical" href="https://terrawhisper.com/{url_slug}.html">'''
        head_html = components.html_head(
            meta_title, meta_description, css='/styles.css', canonical=canonical_html
        )
                # {sections.breadcrumbs_new(url_slug)}
        html = f''' 
            <!DOCTYPE html>
            <html lang="en">
            {head_html}
            <body style="background-color: #fff;">
                {sections.header_dark()}
                {hero_html}
                <main class="container-xxl explorer">
                    {html_article}
                </main>
                {sections.footer()}
            </body>
            </html>
        '''.strip()
        with open(html_filepath, 'w') as f: f.write(html)
        print(html_filepath)

def herbs_activities_category():
    url_slug = f'herbs/activities'
    io.folders_recursive_gen(f'''{g.website_folderpath}/{url_slug}''')

    ### GROUP PLANTS IN PAGES
    page_cards_num = 48
    groups = groups_gen(sidebar_activities_rows, page_cards_num)

    ### GENERATE PAGES
    for group_i, group in enumerate(groups):
        print(f'{group_i}/{len(groups)}')
        ### PAGE URL
        if group_i == 0:
            html_filepath = f'''{g.website_folderpath}/{url_slug}.html'''
        else:
            os.makedirs(f'''{g.website_folderpath}/{url_slug}/page''', exist_ok=True)
            html_filepath = f'''{g.website_folderpath}/{url_slug}/page/{group_i+1}.html'''

        hero_html = hero_html_gen(
            title='Explore herbs biological activities'
        )
        sidebar_html = sidebar_html_gen()
        cards_header_html = cards_header_html_gen(group_i, page_cards_num, len(sidebar_activities_rows),
            title='List of herbs biological activities'
        )
        # cards_header_html = ''
        # cards_html = cards_html_gen(group)
        activities_html = f''
        for i, row in enumerate(group[:]):
            print(f'{i}/{len(group)}')
            activity_name = row[0]
            activity_slug = polish.sluggify(activity_name)

            conn = sqlite3.connect(f'{g.VAULT_FOLDERPATH}/terrawhisper/data/observe/observations.db')
            cur = conn.cursor()

            ### PLANTS NAMES
            cur.execute("""
                SELECT DISTINCT plant_canonical_name
                FROM plants_activities
                WHERE activity_canonical_name = ?
            """, (activity_name,))
            plants_rows = cur.fetchall()

            ### PLANTS COUNT
            cur.execute(
                """
                SELECT COUNT(DISTINCT plant_canonical_name)
                FROM plants_activities
                WHERE activity_canonical_name = ?
                """, (activity_name,)
            )
            plants_count = cur.fetchone()[0]

            conn.close()
            
            plants_html = f''
            for plant_row in plants_rows[:3]:
                plant_name = plant_row[0]
                plant_slug = polish.sluggify(plant_name)
                plants_html += f'''
                    <div>
                        <img 
                            src="/images/herbs/{plant_slug}.jpg" 
                            style="margin-bottom: 0.8rem; width: 80px; height: 80px;"
                        >
                        <p style="font-size: 1.4rem;">{plant_name}</p>
                    </div>
                '''

            ### DESCRIPTION
            json_article_filepath = f'''{g.DATA_FOLDERPATH}/explore/categories/activities.json'''
            json_article = io.json_read(json_article_filepath, create=True)
            regen = False
            key = f'activity_{activity_slug}'
            if key not in json_article: json_article[key] = ''
            if regen: json_article[key] = ''
            if json_article[key] == '':
                plants_names_llm = ','.join([x[0] for x in plants_rows[:3]])
                prompt = f'''
                    Write 2 sentences to explain the following biological activity of medicinal herbs: {activity_name}.
                    Include a sample on what herbs have this biological activity, like {plants_names_llm}.
                '''.strip()
                reply = llm.reply(prompt, model_filepath)
                if '</think>' in reply:
                    reply = reply.split('</think>')[1].strip()
                reply = polish.vanilla(reply)
                json_article[key] = reply
                io.json_write(json_article_filepath, json_article)
            description_text = json_article[key]

            activities_html += f'''
                <article style="border: 1px solid #d8d8d8; margin-bottom: 1.6rem; padding: 1.6rem;">
                    <div style="display: flex; gap: 4.8rem;">
                        <div style="flex: 2;">
                            <a href="/herbs/activities/{activity_slug}.html" style="text-decoration: none;">
                                <h3 style="font-size: 1.8rem;">{activity_name}</h3>
                            </a>
                            <p style="margin-bottom: 1.6rem;">{description_text}</p>
                            <p style="font-size: 1.4rem;"><span style="font-weight: 700;">Associated herbs:</span> {plants_count}</p>
                        </div>
                        <div style="flex: 1;">
                            <p style="font-size: 1.4rem; font-weight: 700; margin-bottom: 1.6rem;">Occurs naturally in</p>
                            <div class="grid-3" style="gap: 1.6rem;">
                                {plants_html}
                            </div>
                            <a 
                                style="color: #111; text-decoration: none; display: inline-block; margin-top: 1.6rem; font-size: 1.4rem;"
                                href="/herbs/activities/{activity_slug}.html">View all {activity_name} herbs →
                            </a>
                        </div>
                    </div>
                </article>
            '''
        pagination_html = pagination_html_gen(group_i, groups, url_slug)

        html_article = ''
        html_article += f'''
            <section style="margin-bottom: 9.6rem;">
                <div class="explorer-layout" style="gap: 4.8rem;">
                    <div style="flex: 1;">
                        {sidebar_html}
                    </div>
                    <div style="flex: 3;">
                        {sections.breadcrumbs_explorer(url_slug)}
                        {cards_header_html}
                        {activities_html}
                        <nav class="pagination">
                            <ul>
                                {pagination_html}
                            </ul>
                        </nav>
                    </div>
                </div>
            </section>
        '''

        ###
        meta_title = f'Medicinal Herbs'
        meta_description = ''
        canonical_html = f'''<link rel="canonical" href="https://terrawhisper.com/{url_slug}.html">'''
        head_html = components.html_head(
            meta_title, meta_description, css='/styles.css', canonical=canonical_html
        )
                # {sections.breadcrumbs_new(url_slug)}
        html = f''' 
            <!DOCTYPE html>
            <html lang="en">
            {head_html}
            <body style="background-color: #fff;">
                {sections.header_dark()}
                {hero_html}
                <main class="container-xxl explorer">
                    {html_article}
                </main>
                {sections.footer()}
            </body>
            </html>
        '''.strip()
        with open(html_filepath, 'w') as f: f.write(html)
        print(html_filepath)

def herbs_activities(activity_name):
    print(activity_name)
    activity_slug = polish.sluggify(activity_name)
    url_slug = f'herbs/activities/{activity_slug}'
    io.folders_recursive_gen(f'''{g.website_folderpath}/{url_slug}''')

    ### GET ALL PLANTS -> TO LIST OF ITEMS
    db_filepath = f'{g.VAULT_FOLDERPATH}/terrawhisper/data/qualify/observations.db'
    conn = sqlite3.connect(db_filepath)
    cur = conn.cursor()
    cur.execute("""
        SELECT DISTINCT plant_canonical_name
        FROM plants_activities
        WHERE activity_canonical_name = ?
    """, (activity_name,))
    plants_rows = cur.fetchall()
    conn.close()

    # plants_rows = sorted([row[1] for row in plants_rows])
    plants_rows = sorted([row[0] for row in plants_rows])
    plants_data = [
        {
            'plant_name_canonical': name,
        }
        for name in plants_rows[:]
    ]
    # print(plants_data[0])
    # print(plants_data[1])
    # quit()

    ### GROUP PLANTS IN PAGES
    page_cards_num = 48
    groups = groups_gen(plants_data, page_cards_num)

    ### GENERATE PAGES
    for group_i, group in enumerate(groups):
        print(f'{group_i}/{len(groups)}')
        ### PAGE URL
        if group_i == 0:
            html_filepath = f'''{g.website_folderpath}/{url_slug}.html'''
        else:
            os.makedirs(f'''{g.website_folderpath}/{url_slug}/page''', exist_ok=True)
            html_filepath = f'''{g.website_folderpath}/{url_slug}/page/{group_i+1}.html'''


        hero_html = hero_html_gen(
            title=f"Explore {activity_name.lower()} herbs"
        )
        sidebar_html = sidebar_html_gen()
        cards_header_html = cards_header_html_gen(group_i, page_cards_num, len(plants_data),
            title=f"List of {activity_name.lower()} herbs"
        )
        cards_html = cards_html_gen(group)
        pagination_html = pagination_html_gen(group_i, groups, url_slug)

        html_article = ''
        html_article += f'''
            <section style="margin-bottom: 9.6rem;">
                <div class="explorer-layout" style="gap: 4.8rem;">
                    <div style="flex: 1;">
                        {sidebar_html}
                    </div>
                    <div style="flex: 3;">
                        {sections.breadcrumbs_explorer(url_slug)}
                        {cards_header_html}
                        <div class="grid-5" style="gap: 1.6rem; row-gap: 3.2rem;">
                            {cards_html}
                        </div>
                        <nav class="pagination">
                            <ul>
                                {pagination_html}
                            </ul>
                        </nav>
                    </div>
                </div>
            </section>
        '''

        ###
        meta_title = f'Medicinal Herbs'
        meta_description = ''
        canonical_html = f'''<link rel="canonical" href="https://terrawhisper.com/{url_slug}.html">'''
        head_html = components.html_head(
            meta_title, meta_description, css='/styles.css', canonical=canonical_html
        )
                # {sections.breadcrumbs_new(url_slug)}
        html = f''' 
            <!DOCTYPE html>
            <html lang="en">
            {head_html}
            <body style="background-color: #fff;">
                {sections.header_dark()}
                {hero_html}
                <main class="container-xxl explorer">
                    {html_article}
                </main>
                {sections.footer()}
            </body>
            </html>
        '''.strip()
        with open(html_filepath, 'w') as f: f.write(html)
        print(html_filepath)

def herbs_chemicals_category():
    url_slug = f'herbs/chemicals'
    io.folders_recursive_gen(f'''{g.website_folderpath}/{url_slug}''')

    ### GROUP PLANTS IN PAGES
    page_cards_num = 48
    groups = groups_gen(sidebar_chemicals_rows[:1000], page_cards_num)

    ### GENERATE PAGES
    for group_i, group in enumerate(groups):
        print(f'{group_i}/{len(groups)}')
        ### PAGE URL
        if group_i == 0:
            html_filepath = f'''{g.website_folderpath}/{url_slug}.html'''
        else:
            os.makedirs(f'''{g.website_folderpath}/{url_slug}/page''', exist_ok=True)
            html_filepath = f'''{g.website_folderpath}/{url_slug}/page/{group_i+1}.html'''

        hero_html = hero_html_gen(
            title='Explore herbs bioactive compounds'
        )
        sidebar_html = sidebar_html_gen()
        cards_header_html = cards_header_html_gen(group_i, page_cards_num, len(sidebar_activities_rows),
            title='List of herbs bioactive compounds'
        )

        chemicals_html = f''
        for i, row in enumerate(group[:]):
            print(f'{i}/{len(group)}')
            chemical_name = row[0]
            chemical_slug = polish.sluggify(chemical_name)


            conn = sqlite3.connect(f'{g.VAULT_FOLDERPATH}/terrawhisper/data/observe/observations.db')
            cur = conn.cursor()

            ### PLANTS NAMES
            cur.execute("""
                SELECT DISTINCT plant_canonical_name
                FROM plants_chemicals
                WHERE chemical_canonical_name = ?
            """, (chemical_name,))
            plants_rows = cur.fetchall()

            ### PLANTS COUNT
            cur.execute(
                """
                SELECT COUNT(DISTINCT plant_canonical_name)
                FROM plants_chemicals
                WHERE chemical_canonical_name = ?
                """, (chemical_name,)
            )
            plants_count = cur.fetchone()[0]

            conn.close()
            
            plants_html = f''
            for plant_row in plants_rows[:3]:
                plant_name = plant_row[0]
                plant_slug = polish.sluggify(plant_name)
                plants_html += f'''
                    <div>
                        <img 
                            src="/images/herbs/{plant_slug}.jpg" 
                            style="margin-bottom: 0.8rem; width: 80px; height: 80px;"
                        >
                        <p style="font-size: 1.4rem;">{plant_name}</p>
                    </div>
                '''

            ### DESCRIPTION
            json_article_filepath = f'''{g.DATA_FOLDERPATH}/explore/categories/chemicals.json'''
            json_article = io.json_read(json_article_filepath, create=True)
            regen = False
            key = f'chemical_{chemical_slug}'
            if key not in json_article: json_article[key] = ''
            if regen: json_article[key] = ''
            if json_article[key] == '':
                plants_names_llm = ','.join([x[0] for x in plants_rows[:3]])
                prompt = f'''
                    Write 2 sentences to explain the following bioactive compound of medicinal herbs: {chemical_name}.
                    Include a sample on what herbs have this bioactive compound, like {plants_names_llm}.
                '''.strip()
                reply = llm.reply(prompt, model_filepath)
                if '</think>' in reply:
                    reply = reply.split('</think>')[1].strip()
                reply = polish.vanilla(reply)
                json_article[key] = reply
                io.json_write(json_article_filepath, json_article)
            description_text = json_article[key]

            chemicals_html += f'''
                <article style="border: 1px solid #d8d8d8; margin-bottom: 1.6rem; padding: 1.6rem;">
                    <div style="display: flex; gap: 4.8rem;">
                        <div style="flex: 2;">
                            <a href="/herbs/chemicals/{chemical_slug}.html" style="text-decoration: none;">
                                <h3 style="font-size: 1.8rem;">{chemical_name}</h3>
                            </a>
                            <p style="margin-bottom: 1.6rem;">{description_text}</p>
                            <p style="font-size: 1.4rem;"><span style="font-weight: 700;">Associated herbs:</span> {plants_count}</p>
                        </div>
                        <div style="flex: 1;">
                            <p style="font-size: 1.4rem; font-weight: 700; margin-bottom: 1.6rem;">Occurs naturally in</p>
                            <div class="grid-3" style="gap: 1.6rem;">
                                {plants_html}
                            </div>
                            <a 
                                style="color: #111; text-decoration: none; display: inline-block; margin-top: 1.6rem; font-size: 1.4rem;"
                                href="/herbs/chemicals/{chemical_slug}.html">View all {chemical_name} herbs →
                            </a>
                        </div>
                    </div>
                </article>
            '''
        pagination_html = pagination_html_gen(group_i, groups, url_slug)

        html_article = ''
        html_article += f'''
            <section style="margin-bottom: 9.6rem;">
                <div class="explorer-layout" style="gap: 4.8rem;">
                    <div style="flex: 1;">
                        {sidebar_html}
                    </div>
                    <div style="flex: 3;">
                        {sections.breadcrumbs_explorer(url_slug)}
                        {cards_header_html}
                        {chemicals_html}
                        <nav class="pagination">
                            <ul>
                                {pagination_html}
                            </ul>
                        </nav>
                    </div>
                </div>
            </section>
        '''

        ###
        meta_title = f'Medicinal Herbs'
        meta_description = ''
        canonical_html = f'''<link rel="canonical" href="https://terrawhisper.com/{url_slug}.html">'''
        head_html = components.html_head(
            meta_title, meta_description, css='/styles.css', canonical=canonical_html
        )
                # {sections.breadcrumbs_new(url_slug)}
        html = f''' 
            <!DOCTYPE html>
            <html lang="en">
            {head_html}
            <body style="background-color: #fff;">
                {sections.header_dark()}
                {hero_html}
                <main class="container-xxl explorer">
                    {html_article}
                </main>
                {sections.footer()}
            </body>
            </html>
        '''.strip()
        with open(html_filepath, 'w') as f: f.write(html)
        print(html_filepath)

def herbs_chemicals(chemical_name):
    print(chemical_name)
    chemical_slug = polish.sluggify(chemical_name)
    url_slug = f'herbs/chemicals/{chemical_slug}'
    io.folders_recursive_gen(f'''{g.website_folderpath}/{url_slug}''')

    ### GET ALL PLANTS -> TO LIST OF ITEMS
    db_filepath = f'{g.VAULT_FOLDERPATH}/terrawhisper/data/observe/observations.db'
    conn = sqlite3.connect(db_filepath)
    cur = conn.cursor()
    cur.execute("""
        SELECT DISTINCT chemical_canonical_name, plant_canonical_name
        FROM plants_chemicals
        WHERE chemical_canonical_name = ?
    """, (chemical_name,))
    plants_rows = cur.fetchall()
    conn.close()

    plants_rows = sorted([row[1] for row in plants_rows])
    plants_data = [
        {
            'plant_name_canonical': name,
        }
        for name in plants_rows[:]
    ]

    ### GROUP PLANTS IN PAGES
    page_cards_num = 48
    groups = groups_gen(plants_data, page_cards_num)

    ### GENERATE PAGES
    for group_i, group in enumerate(groups):
        print(f'{group_i}/{len(groups)}')
        ### PAGE URL
        if group_i == 0:
            html_filepath = f'''{g.website_folderpath}/{url_slug}.html'''
        else:
            os.makedirs(f'''{g.website_folderpath}/{url_slug}/page''', exist_ok=True)
            html_filepath = f'''{g.website_folderpath}/{url_slug}/page/{group_i+1}.html'''


        hero_html = hero_html_gen(
            title=f"Explore herbs that contain {chemical_name}"
        )
        sidebar_html = sidebar_html_gen()
        cards_header_html = cards_header_html_gen(group_i, page_cards_num, len(plants_data),
            title=f"List of herbs that contain {chemical_name}"
        )
        cards_html = cards_html_gen(group)
        pagination_html = pagination_html_gen(group_i, groups, url_slug)

        html_article = ''
        html_article += f'''
            <section style="margin-bottom: 9.6rem;">
                <div class="explorer-layout" style="gap: 4.8rem;">
                    <div style="flex: 1;">
                        {sidebar_html}
                    </div>
                    <div style="flex: 3;">
                        {sections.breadcrumbs_explorer(url_slug)}
                        {cards_header_html}
                        <div class="grid-5" style="gap: 1.6rem; row-gap: 3.2rem;">
                            {cards_html}
                        </div>
                        <nav class="pagination">
                            <ul>
                                {pagination_html}
                            </ul>
                        </nav>
                    </div>
                </div>
            </section>
        '''

        ###
        meta_title = f'Medicinal Herbs'
        meta_description = ''
        canonical_html = f'''<link rel="canonical" href="https://terrawhisper.com/{url_slug}.html">'''
        head_html = components.html_head(
            meta_title, meta_description, css='/styles.css', canonical=canonical_html
        )
                # {sections.breadcrumbs_new(url_slug)}
        html = f''' 
            <!DOCTYPE html>
            <html lang="en">
            {head_html}
            <body style="background-color: #fff;">
                {sections.header_dark()}
                {hero_html}
                <main class="container-xxl explorer">
                    {html_article}
                </main>
                {sections.footer()}
            </body>
            </html>
        '''.strip()
        with open(html_filepath, 'w') as f: f.write(html)
        print(html_filepath)

def run():
    print(f'EXPLORE >> herbs')

    ### ACTIVITIES (do only ones, cache it)
    if sidebar_activities_rows == None:
        sidebar_activities_get()

    ### COMPOUNDS (do only ones, cache it)
    if sidebar_chemicals_rows == None:
        sidebar_chemicals_get()

    if 1:
        herbs_index()

    if 1:
        herbs_alphabet_category()

    if 1:
        letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
        for letter in letters:
            herbs_alphabet(letter)

    if 1:
        herbs_activities_category()

    if 1:
        for activity in sidebar_activities_rows:
            activity_name = activity[0]
            herbs_activities(activity_name)
            # quit()

    if 1:
        herbs_chemicals_category()

    if 1:
        for i, chemical in enumerate(sidebar_chemicals_rows[:1000]):
            print(f'{i}/{len(sidebar_chemicals_rows)}')
            chemical_name = chemical[0]
            herbs_chemicals(chemical_name)
            # quit()

