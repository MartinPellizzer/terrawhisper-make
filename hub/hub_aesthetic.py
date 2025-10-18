from lib import g
from lib import io
from lib import article

def article_aesthetic_green_gen():
    article_slug = f'''aesthetic/green'''
    print(f'ARTICLE: {article_slug}')
    article_obj = {
        'article_slug': article_slug,
        'keyword_main': 'green aesthetic',
        'keyword_main_slug': 'green-aesthetic',
        'keyword_main_pretty': 'green aesthetics',
        'keyword_main_title': 'green aesthetic images',
        'pin_board_name': g.PIN_BOARD_NAME_AESTHETIC,
        'main_list_num': '10',
        'article_type': 'listicle',
        'images_prompts': ['greenery, nature photography, bokeh, depth of field, high resolution'],
        'links': [],
    }
    article.images_gen(article_obj, regen=False, dispel=False)
    article.json_gen(article_obj, regen=False, dispel=False)
    article.html_gen(article_slug)

def article_aesthetic_gen():
    article_slug = f'''aesthetic'''
    print(f'ARTICLE: {article_slug}')
    article_aesthetic_green_gen()

def gen():
    print(f'HUB: aesthetic')
    article_aesthetic_gen()
