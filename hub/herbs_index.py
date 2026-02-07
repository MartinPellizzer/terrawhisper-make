# TODO: <li> for pagination

import os

from lib import g
from lib import io
from lib import data
from lib import polish

herbs_primary_medicinal = data.herbs_primary_medicinal_get()

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

def pagination_gen(group_i, groups, url_slug):
    ### prev
    if group_i > 1:
        prev_html = f'''
            <a rel="prev" style="text-decoration: none;" href="/{url_slug}/page/{group_i}.html">
                <p style="font-size: 1.2rem; font-weight: bold; padding: 0.8rem 1.6rem; border: 1px solid #e7e7e7;">
                    PREV
                </p>
            </a>
        '''
    elif group_i > 0:
        prev_html = f'''
            <a rel="prev" style="text-decoration: none;" href="/{url_slug}.html">
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
            <a rel="next" style="text-decoration: none;" href="/{url_slug}/page/{group_i+2}.html">
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

def main():
    url_slug = f'herbs/all'

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
        cards_html = ''
        cards_list = []
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
            cards_html += html_card
            cards_list.append(f'''
                <li>
                  <article class="herb-entity" itemscope itemtype="https://schema.org/Plant">
                    <a href="/herbs/{herb_slug}.html" itemprop="url">
                      <span itemprop="name">{herb_name_scientific}</span>
                    </a>
                  </article>
                </li>
            ''')

        cards_list = '\n'.join(cards_list)

        '''
        <nav id="pagination" aria-label="Confirmed herbs pagination">
          <ul class="pagination-list">
            <li><a href="/herbs/all.html" aria-label="Page 1" rel="prev">← Prev</a></li>
            <li><a href="/herbs/all.html" aria-label="Page 1">1</a></li>
            <li><a href="/herbs/all/page/2.html" aria-label="Page 2">2</a></li>
            <li><a href="/herbs/all/page/3.html" aria-label="Page 3">3</a></li>
            <li><a href="/herbs/all/page/2.html" rel="next">Next →</a></li>
          </ul>
        </nav>
        '''

        herbs_grid = f'''
        <section id="herb-grid">
          <ul class="herb-list">
            {cards_list}
          </ul>
        </section>
        '''

        pagination_html = pagination_gen(group_i, groups, url_slug)

        import textwrap
        html = textwrap.dedent(f''' 
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Confirmed Medicinal Herbs Index</title>
</head>

<body>

<header id="site-header">
  <nav id="global-navigation">
  </nav>
</header>

<main id="main-content">

  <header id="catalog-header">
    <h1>Confirmed Medicinal Herbs</h1>
  </header>

  <section id="herb-index" aria-labelledby="herb-index-heading">
    <h2 id="herb-index-heading">All Confirmed Medicinal Herb Entities</h2>

    {herbs_grid}

    <nav id="pagination" aria-label="Confirmed herbs pagination">
      <ul class="pagination-list">
        <li><a href="/herbs/all.html" aria-label="Page 1">1</a></li>
        <li><a href="/herbs/all/page/2.html" aria-label="Page 2">2</a></li>
        <li><a href="/herbs/all/page/3.html" aria-label="Page 3">3</a></li>
        <li><a href="/herbs/all/page/2.html" rel="next">Next →</a></li>
      </ul>
    </nav>
    <nav>
        <ul style="display: flex; justify-content: center; gap: 0.8rem;">
            {pagination_html}
        </ul>
    </nav>

    <p id="catalog-summary">Showing herbs 1–20 of 1,000 confirmed medicinal herbs.</p>

  </section>

</main>

<footer id="site-footer">
  <nav id="footer-navigation">
  </nav>
</footer>

</body>
</html>
        ''').strip()
        # html_filepath = f'''{g.website_folderpath}/{url_slug}.html'''
        try: os.makedir(f'{g.website_folderpath}/herbs/all')
        except: pass
        try: os.makedir(f'{g.website_folderpath}/herbs/all/page')
        except: pass
        with open(html_filepath, 'w') as f: f.write(html)
        # quit()

main()
