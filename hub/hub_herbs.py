from lib import g
from lib import io
from lib import article

def article_herbs_types_flowers_wallpaper_gen():
    article_slug = f'''herbs/types/flowers/wallpaper'''
    print(f'ARTICLE: {article_slug}')
    article_obj = {
        'article_slug': article_slug,
        'keyword_main': 'flower wallpaper',
        'keyword_main_slug': 'flower-wallpaper',
        'keyword_main_pretty': 'flower wallpapers',
        'keyword_main_title': 'healing flower wallpapers herbalism',
        'pin_board_name': g.PIN_BOARD_NAME_FLOWERS,
        'main_list_num': '10',
        'article_type': 'listicle',
        'images_prompts': ['flowers, nature photography, bokeh, depth of field, high resolution'],
        'links': [],
    }
    article.images_gen(article_obj, regen=False, dispel=False)
    article.json_gen(article_obj, regen=False, dispel=False)
    article.html_gen(article_slug)

def article_herbs_types_flowers_gen():
    article_herbs_types_flowers_wallpaper_gen()
    article_slug = f'''herbs/types/flowers'''
    print(f'ARTICLE: {article_slug}')
    article_obj = {
        'article_slug': article_slug,
        'article_type': 'listicle',
        'keyword_main': 'medicinal flowers',
        'keyword_main_slug': 'medicinal-flowers',
        'keyword_main_pretty': 'medicinal flowers',
        'keyword_main_title': 'medicinal flowers herbalism',
        'pin_board_name':  g.PIN_BOARD_NAME_FLOWERS,
        'main_list_num': '10',
        'images_prompts': ['flowers, bokeh, depth of field, high resolution'],
        'links': [],
    }
    article.images_gen(article_obj, regen=False, dispel=False)
    article.json_gen(article_obj, regen=False, dispel=False)
    article.html_gen(article_slug)

def article_herbs_types_gen():
    article_herbs_types_flowers_gen()
    # ---
    article_slug = f'''herbs/types'''
    print(f'ARTICLE: {article_slug}')
    article_obj = {
        'article_slug': article_slug,
        'article_type': 'category',
        'keyword_main': 'herb types',
        'keyword_main_slug': 'herb-types',
        'keyword_main_pretty': 'herb types',
        'keyword_main_title': 'herb types for general medicinal herbalism',
        'pin_board_name': 'medicinal herbs',
        'main_list_num': '',
        'images_prompts': ['herbs, nature photography, bokeh, depth of field, high resolution'],
        'links': [],
    }
    # article.images_gen(article_obj, regen=False, dispel=False)
    article.json_gen(article_obj, regen=False, dispel=False)
    article.html_gen(article_slug, article_obj)

def article_herbs_gen():
    article_slug = f'''herbs'''
    print(f'ARTICLE: {article_slug}')
    article_herbs_types_gen()

def gen():
    print(f'HUB: herbs')
    article_herbs_gen()
