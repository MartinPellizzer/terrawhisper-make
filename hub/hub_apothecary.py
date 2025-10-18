from lib import g
from lib import io
from lib import article

def article_apothecary_kitchen_design_gen():
    article_slug = f'''apothecary/kitchen/design'''
    print(f'ARTICLE: {article_slug}')
    article_obj = {
        'article_slug': article_slug,
        'keyword_main': 'kitchen design',
        'keyword_main_slug': 'kitchen-design',
        'keyword_main_pretty': 'kitchen designs',
        'keyword_main_title': 'apothecary kitchen designs',
        'pin_board_name': g.PIN_BOARD_NAME_APOTHECARY,
        'main_list_num': '10',
        'article_type': 'listicle',
        'images_prompts': ['apothecary kitchen design, nature photography, bokeh, depth of field, high resolution'],
        'links': [],
    }
    article.images_gen(article_obj, regen=False, dispel=False)
    article.json_gen(article_obj, regen=False, dispel=False)
    article.html_gen(article_slug)

def article_apothecary_kitchen_gen():
    article_slug = f'''apothecary/kitchen'''
    print(f'ARTICLE: {article_slug}')
    article_apothecary_kitchen_design_gen()

def article_apothecary_academia_dark_aesthetic_gen():
    article_slug = f'''apothecary/academia/dark/aesthetic'''
    print(f'ARTICLE: {article_slug}')
    article_obj = {
        'article_slug': article_slug,
        'keyword_main': 'dark academia aesthetic',
        'keyword_main_slug': 'dark-academia-aesthetic',
        'keyword_main_pretty': 'dark academia aesthetics',
        'keyword_main_title': 'dark academia aesthetic photos herbalism',
        'pin_board_name': g.PIN_BOARD_NAME_APOTHECARY,
        'main_list_num': '10',
        'article_type': 'listicle',
        'images_prompts': ['dark academia, indoor, table, herbs, bokeh, depth of field, high resolution'],
        'links': [],
    }
    article.images_gen(article_obj, regen=False, dispel=False)
    article.json_gen(article_obj, regen=False, dispel=False)
    article.html_gen(article_slug)

def article_apothecary_academia_dark_gen():
    article_slug = f'''apothecary/academia/dark'''
    print(f'ARTICLE: {article_slug}')
    article_apothecary_academia_dark_aesthetic_gen()

def article_apothecary_academia_gen():
    article_slug = f'''apothecary/academia'''
    print(f'ARTICLE: {article_slug}')
    article_apothecary_academia_dark_gen()

def article_apothecary_gen():
    article_slug = f'''apothecary'''
    print(f'ARTICLE: {article_slug}')
    article_apothecary_kitchen_gen()
    article_apothecary_academia_gen()

def gen():
    print(f'HUB: apothecary')
    article_apothecary_gen()
