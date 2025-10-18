from lib import g
from lib import io
from lib import article

def article_spirituality_moon_aesthetic_gen():
    article_slug = f'''spirituality/moon/aesthetic'''
    print(f'ARTICLE: {article_slug}')
    article_obj = {
        'article_slug': article_slug,
        'keyword_main': 'moon aesthetic',
        'keyword_main_slug': 'moon-aesthetic',
        'keyword_main_pretty': 'moon aesthetic images',
        'keyword_main_title': 'moon aesthetic images for herbalism spiritual healing',
        'pin_board_name': 'spiritual herbalism',
        'main_list_num': '10',
        'article_type': 'listicle',
        'images_prompts': ['glowing full moon at night, nature photography, scenic view, bokeh, depth of field, high resolution'],
        'links': [],
    }
    article.images_gen(article_obj, regen=False, dispel=False)
    article.json_gen(article_obj, regen=False, dispel=False)
    article.html_gen(article_slug)

def article_spirituality_moon_wallpaper_gen():
    article_slug = f'''spirituality/moon/wallpaper'''
    print(f'ARTICLE: {article_slug}')
    article_obj = {
        'article_slug': article_slug,
        'keyword_main': 'moon wallpaper',
        'keyword_main_slug': 'moon-wallpaper',
        'keyword_main_pretty': 'moon wallpapers',
        'keyword_main_title': 'moon wallpapers for herbalist spiritual healing',
        'pin_board_name': 'spiritual herbalism',
        'main_list_num': '10',
        'article_type': 'listicle',
        'images_prompts': ['glowing full moon at night, nature photography, scenic view, bokeh, depth of field, high resolution'],
        'links': [],
    }
    article.images_gen(article_obj, regen=False, dispel=False)
    article.json_gen(article_obj, regen=False, dispel=False)
    article.html_gen(article_slug)

def article_spirituality_moon_gen():
    article_slug = f'''spirituality/moon'''
    print(f'ARTICLE: {article_slug}')
    article_spirituality_moon_aesthetic_gen()
    article_spirituality_moon_wallpaper_gen()

def article_spirituality_stars_aesthetic_gen():
    article_slug = f'''spirituality/stars/aesthetic'''
    print(f'ARTICLE: {article_slug}')
    article_obj = {
        'article_slug': article_slug,
        'keyword_main': 'stars aesthetic',
        'keyword_main_slug': 'stars-aesthetic',
        'keyword_main_pretty': 'stars aesthetics',
        'keyword_main_title': 'stars aesthetics herbalist spiritual healing',
        'pin_board_name': g.PIN_BOARD_NAME_SPIRITUAL,
        'main_list_num': '10',
        'article_type': 'listicle',
        'images_prompts': ['stars in the night sky, nature photography, dark background, scenic view, bokeh, depth of field, high resolution'],
        'links': [],
    }
    article.images_gen(article_obj, regen=False, dispel=False)
    article.json_gen(article_obj, regen=False, dispel=False)
    article.html_gen(article_slug)


def article_spirituality_stars_gen():
    article_slug = f'''spirituality/stars'''
    print(f'ARTICLE: {article_slug}')
    article_spirituality_stars_aesthetic_gen()

def article_spirituality_gen():
    article_slug = f'''spirituality'''
    print(f'ARTICLE: {article_slug}')
    article_spirituality_moon_gen()
    article_spirituality_stars_gen()

def gen():
    print(f'HUB: spirituality')
    article_spirituality_gen()
