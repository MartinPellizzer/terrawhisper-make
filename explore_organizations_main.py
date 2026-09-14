import os
import json
import shutil
import sqlite3

from lib import g
from lib import io
from lib import polish
from lib import sections
from lib import components

import masterize_utils
import masterize_organizations_utils

HUB_FOLDERPATH = f'{g.DATA_FOLDERPATH}/organizations'

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
    # plants_rows = masterize_utils.masterize_plants_get_all()
    # activities_rows = masterize_utils.masterize_activities_get_all()
    # chemicals_rows = masterize_utils.masterize_chemicals_get_all()

    ### STATS
    # plants_num = len(plants_rows)
    # activities_num = len(activities_rows)
    # chemicals_num = len(chemicals_rows)
    # studies_num = len(os.listdir(f'{g.VAULT_FOLDERPATH}/terrawhisper/data/fetch/pubmed/medicinal_plant/abstracts'))
    '''
        <div style="display: flex; align-items: center;">
            <h1 style="font-size: 1.4rem; margin-bottom: 0; margin-top: 2px;">
                {title}
            </h1>
            <span style="font-weight: 400;">: A scientifically curated directory of plants, their bioactive compounds, traditional uses, and research evidence</span>
        </div>
    '''
    """
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
    """
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
                </div>
            </div>
        </section>
    '''
    return html

def cards_header_html_gen(group_i, page_cards_num, items_num, title):
    from_num = page_cards_num*group_i+1
    to_num = page_cards_num*group_i+page_cards_num
    if to_num > items_num: to_num = items_num
    html = f'''
        <div class="m-flex" style="justify-content: space-between; align-items: center; margin-bottom: 2.4rem;">
            <h2 style="font-size: 2.4rem;">
               {title}
            </h2>
            <span style="font-size: 1.4rem;">Showing {from_num}-{to_num}  out of {items_num} results</span>
        </div>
    '''
    return html

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

def organizations_index():
    url_slug = f'organizations'
    io.folders_recursive_gen(f'''{g.WEBSITE_FOLDERPATH}/{url_slug}''')

    # plants_rows = masterize_utils.masterize_plants_get_all()
    organizations_items = masterize_organizations_utils.masterize_organizations_get_all()

    ### FILTER GOOD RESULTS
    ### ----------------------------------------
    organizations_items_filtered = []
    for organization_item in organizations_items[:]:
        business_name_canonical = organization_item['business_name_canonical']
        input_data = io.json_read(f'{HUB_FOLDERPATH}/compile/{business_name_canonical}.json')
        identity_data = input_data['identity']
        ### GET IDENTITY GMAP ITEM
        identity_gmap_item = None
        for identity_list in identity_data:
            for identity_item in identity_list['items']:
                if identity_item['source_name'] == 'Google Maps':
                    identity_gmap_item = identity_item
        ### FILTER BY GMAP DATA
        if identity_gmap_item['fields']['business_type_primary'] == None: continue
        if 'erboristeria' not in identity_gmap_item['fields']['business_type_primary'].lower(): continue
        if 'stati uniti' not in identity_gmap_item['fields']['business_address'].lower(): continue
        ### GET IDENTITY WEGSITE ITEM
        identity_website_item = None
        for identity_list in identity_data:
            for identity_item in identity_list['items']:
                if identity_item['source_name'] == 'Website':
                    identity_website_item = identity_item
        ### FILTER BY WEBSITE DATA DATA
        if identity_website_item['fields']['business_website_html'] == 'false': continue
        if identity_website_item['fields']['business_website_text'] == 'false': continue
        if identity_website_item['fields']['business_description'] == None: continue
        ### IF PASSED ALL FILTER:
        organizations_items_filtered.append(organization_item)

    ### GROUP ITEMS IN PAGES
    ### ----------------------------------------
    page_cards_num = 48
    groups = groups_gen(organizations_items_filtered, page_cards_num)

    ### GENERATE PAGES
    ### ----------------------------------------
    hero_title = f'Explore all organizations'
    items_num = len(organizations_items_filtered)
    cards_header_title = f'List of all organizations'
    for group_i, group in enumerate(groups):
        print(f'{group_i}/{len(groups)}')

        ### PAGE URL
        if group_i == 0:
            html_filepath = f'''{g.website_folderpath}/{url_slug}.html'''
        else:
            os.makedirs(f'''{g.website_folderpath}/{url_slug}/page''', exist_ok=True)
            html_filepath = f'''{g.website_folderpath}/{url_slug}/page/{group_i+1}.html'''

        hero_html = hero_html_gen(title=hero_title)
        # sidebar_html = sidebar_html_gen()
        sidebar_html = ''
        cards_header_html = cards_header_html_gen(group_i, page_cards_num, items_num, title=cards_header_title)
        # cards_html = cards_html_gen(group)
        cards_html = ''
        for i, item in enumerate(group[:]):
            print(f'{i}/{len(group)} - {item}')
            business_name_canonical = item['business_name_canonical']
            business_name_display = item['business_name_display']
            business_slug = polish.sluggify(business_name_canonical)
            business_description = ''
            input_data = io.json_read(f'{HUB_FOLDERPATH}/compile/{business_name_canonical}.json')
            for lst in input_data['identity']:
                for item in lst['items']:
                    if item['source_name'] == 'Website':
                        business_description = item['fields']['business_description']
            # print(identity_website_item)
            # quit()
            print(business_slug)
            ###
            card_html = f'''
                <article style="border: 1px solid #d8d8d8; margin-bottom: 1.6rem; padding: 1.6rem;">
                    <a href="/organizations/{business_slug}.html" style="text-decoration: none;">
                        <h3 style="font-size: 1.8rem;">{business_name_display}</h3>
                    </a>
                    <p style="margin-bottom: 1.6rem;">{business_description}</p>
                </article>
            '''
            cards_html += card_html

        pagination_html = pagination_html_gen(group_i, groups, url_slug)
        # pagination_html = ''

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
                        {cards_html}
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
        meta_title = f'Explore all organizations'
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
    organizations_index()
