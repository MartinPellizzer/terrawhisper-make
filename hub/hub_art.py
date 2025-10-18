from lib import g
from lib import io
from lib import article

def article_art_crafts_pumpkin_carving_ideas_gen():
    article_slug = f'''art/crafts/pumpkin/carving/ideas'''
    print(f'ARTICLE: {article_slug}')
    article_obj = {
        'article_slug': article_slug,
        'keyword_main': 'pumpkin carving ideas',
        'keyword_main_slug': 'pumpkin-carving-ideas',
        'keyword_main_pretty': 'pumpkin carving ideas',
        'keyword_main_title': 'pumpkin carving ideas herbal art',
        'pin_board_name': g.PIN_BOARD_NAME_ART,
        'main_list_num': '10',
        'article_type': 'listicle',
        'images_prompts': ['pumpkin carving, nature photography, bokeh, depth of field, high resolution'],
        'links': [],
    }
    article.images_gen(article_obj, regen=False, dispel=False)
    article.json_gen(article_obj, regen=False, dispel=False)
    article.html_gen(article_slug)

def article_art_crafts_pumpkin_carving_gen():
    article_slug = f'''art/crafts/pumpkin/carving'''
    print(f'ARTICLE: {article_slug}')
    article_art_crafts_pumpkin_carving_ideas_gen()

def article_art_crafts_pumpkin_gen():
    article_slug = f'''art/crafts/pumpkin'''
    print(f'ARTICLE: {article_slug}')
    article_art_crafts_pumpkin_carving_gen()

def article_art_crafts_gen():
    article_slug = f'''art/crafts'''
    print(f'ARTICLE: {article_slug}')
    article_art_crafts_pumpkin_gen()

def article_art_wallpapers_dark_aesthetic_gen():
    article_slug = f'''art/wallpapers/dark/aesthetic'''
    print(f'ARTICLE: {article_slug}')
    article_obj = {
        'article_slug': article_slug,
        'keyword_main': 'dark wallpapers aesthetic',
        'keyword_main_slug': 'dark-wallpapers-aesthetic',
        'keyword_main_pretty': 'dark wallpapers aesthetic',
        'keyword_main_title': 'dark wallpapers aesthetic medicinal healing herbs',
        'pin_board_name': g.PIN_BOARD_NAME_ART,
        'main_list_num': '10',
        'article_type': 'listicle',
        'images_prompts': ['dark background, dark herbs, wallpaper, aesthetic, bokeh, depth of field, high resolution'],
        'links': [],
    }
    article.images_gen(article_obj, regen=False, dispel=False)
    article.json_gen(article_obj, regen=False, dispel=False)
    article.html_gen(article_slug)

def article_art_gen():
    article_slug = f'''art'''
    print(f'ARTICLE: {article_slug}')
    article_art_crafts_gen()

def gen():
    print(f'HUB: art')
    article_art_gen()

