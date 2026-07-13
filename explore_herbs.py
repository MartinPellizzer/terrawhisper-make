import os
import json
import shutil
import sqlite3

from lib import g
from lib import io
from lib import data
from lib import polish
from lib import sections
from lib import components

shutil.copy2('styles.css', f'{g.website_folderpath}/styles.css')

sidebar_activities_rows = None

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

def hero_html_gen():
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
                        Explore medicinal herbs: 
                        <span style="font-weight: 400;">A scientifically curated directory of plants, their bioactive compounds, traditional uses, and research evidence</span>
                    </h1>
                    <ul style="list-style: none; display: flex; align-items: center; gap: 1.2rem; font-size: 1.4rem;">
                        <li>15,420 Plants</li>
                        <span>|</span>
                        <li>32,800 Compounds</li>
                        <span>|</span>
                        <li>5,600 Studies Indexed</li>
                        <span>|</span>
                        <li>180 Botanical Families</li>
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

            <h3 style="font-size: 1.4rem; letter-spacing: 0.5px; margin-bottom: 1.4rem;">Alphabet</h3>
            {alphabet_html}
            <hr style="border: 0; border-bottom: 1px solid #d8d8d8; margin-top: 2.4rem; margin-bottom: 2.4rem;">

            <h3 style="font-size: 1.4rem; letter-spacing: 0.5px; margin-bottom: 1.4rem;">Biological Activity</h3>
            {activities_html}
            <a style="{li_a_style} margin-top: 1.6rem;" href="/herbs.html">view all →</a>
            <hr style="border: 0; border-bottom: 1px solid #d8d8d8; margin-top: 2.4rem; margin-bottom: 2.4rem;">

            <h3 style="font-size: 1.4rem; letter-spacing: 0.5px; margin-bottom: 1.4rem;">
                bioactive compounds
            </h3>
            <ul style="list-style: none; display: flex; flex-direction: column; gap: 0.4rem;">
                <li>
                    <a style="{li_a_style}" href="/herbs.html">alkaoids</a>
                </li>
                <li>
                    <a style="{li_a_style}" href="/herbs.html">flavonoids</a>
                </li>
                <li>
                    <a style="{li_a_style}" href="/herbs.html">terpenes</a>
                </li>
                <li>
                    <a style="{li_a_style}" href="/herbs.html">polyphenols</a>
                </li>
                <li>
                    <a style="{li_a_style}" href="/herbs.html">saponins</a>
                </li>
                <li>
                    <a style="{li_a_style}" href="/herbs.html">essential oils</a>
                </li>
                <li>
                    <a style="{li_a_style}" href="/herbs.html">tannins</a>
                </li>
            </ul>
            <a style="{li_a_style} margin-top: 1.6rem;" href="/herbs.html">view all →</a>
            <hr style="border: 0; border-bottom: 1px solid #d8d8d8; margin-top: 2.4rem; margin-bottom: 2.4rem;">
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
        </div>
    '''
    return sidebar_html

def cards_header_html_gen(group_i, page_cards_num, total_items_num):
    from_num = page_cards_num*group_i+1
    to_num = page_cards_num*group_i+page_cards_num
    if to_num > total_items_num: to_num = total_items_num
    html = f'''
        <div class="m-flex" style="justify-content: space-between; align-items: center; margin-bottom: 2.4rem;">
            <h2 style="font-size: 2.4rem;">
               List of all herbs
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
        html_image = f'''
            <img src="{plant_img_src}" alt="{plant_name}" style="margin-bottom: 1.6rem;">
        '''
        cards_html += f'''
            <article>
                <a href="/herbs/{plant_slug}.html" style="text-decoration: none;">
                    {html_image}
                    <h3 style="font-size: 1.8rem;">{plant_name}</h3>
                </a>
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
    plants_rows = data.sqlite__plants_get()
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


        hero_html = hero_html_gen()
        sidebar_html = sidebar_html_gen()
        cards_header_html = cards_header_html_gen(group_i, page_cards_num, len(plants_data))
        cards_html = cards_html_gen(group)
        pagination_html = pagination_html_gen(group_i, groups, url_slug)

        html_article = ''
        html_article += f'''
            <section style="margin-bottom: 9.6rem;">
                <div class="m-flex" style="gap: 4.8rem;">
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

def herbs_alphabet(alphabet_letter=''):
    if alphabet_letter == '': return

    url_slug = f'herbs/alphabet/{alphabet_letter}'
    io.folders_recursive_gen(f'''{g.website_folderpath}/{url_slug}''')

    ### GET ALL PLANTS -> TO LIST OF ITEMS
    plants_rows = data.sqlite__plants_get()
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


        hero_html = hero_html_gen()
        sidebar_html = sidebar_html_gen()
        cards_header_html = cards_header_html_gen(group_i, page_cards_num, len(plants_data))
        cards_html = cards_html_gen(group)
        pagination_html = pagination_html_gen(group_i, groups, url_slug)

        html_article = ''
        html_article += f'''
            <section style="margin-bottom: 9.6rem;">
                <div class="m-flex" style="gap: 4.8rem;">
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

def herbs_activities(activity_name):
    print(activity_name)
    activity_slug = polish.sluggify(activity_name)
    url_slug = f'herbs/activities/{activity_slug}'
    io.folders_recursive_gen(f'''{g.website_folderpath}/{url_slug}''')

    ### GET ALL PLANTS -> TO LIST OF ITEMS
    db_filepath = f'{g.VAULT_FOLDERPATH}/terrawhisper/data/observe/observations.db'
    conn = sqlite3.connect(db_filepath)
    cur = conn.cursor()
    cur.execute("""
        SELECT DISTINCT activity_canonical_name, plant_canonical_name
        FROM plants_activities
        WHERE activity_canonical_name = ?
    """, (activity_name,))
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


        hero_html = hero_html_gen()
        sidebar_html = sidebar_html_gen()
        cards_header_html = cards_header_html_gen(group_i, page_cards_num, len(plants_data))
        cards_html = cards_html_gen(group)
        pagination_html = pagination_html_gen(group_i, groups, url_slug)

        html_article = ''
        html_article += f'''
            <section style="margin-bottom: 9.6rem;">
                <div class="m-flex" style="gap: 4.8rem;">
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

    herbs_index()

    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
    for letter in letters:
        herbs_alphabet(letter)

    # activities = data.sqlite_activities_get()
    for activity in sidebar_activities_rows:
        activity_name = activity[0]
        herbs_activities(activity_name)
        # quit()
