from lib import g
from lib import io
from lib import article

def article_nutrition_drinks_coffee_aesthetic_gen():
    article_slug = f'''nutrition/drinks/coffee/aesthetic'''
    print(f'ARTICLE: {article_slug}')
    article_obj = {
        'article_slug': article_slug,
        'keyword_main': 'coffee aesthetic',
        'keyword_main_slug': 'coffee-aesthetic',
        'keyword_main_pretty': 'coffee aesthetics',
        'keyword_main_title': 'coffee aesthetics for healthy herbal nutrition',
        'pin_board_name': g.PIN_BOARD_NAME_NUTRITION,
        'main_list_num': '10',
        'article_type': 'listicle',
        'images_prompts': ['coffee, cozy, bokeh, depth of field, high resolution'],
        'links': [],
    }
    article.images_gen(article_obj, regen=False, dispel=False)
    article.json_gen(article_obj, regen=False, dispel=False)
    article.html_gen(article_slug)

def article_nutrition_drinks_coffee_gen():
    article_slug = f'''nutrition/drinks/coffee'''
    print(f'ARTICLE: {article_slug}')
    article_nutrition_drinks_coffee_aesthetic_gen()

def article_nutrition_drinks_matcha_aesthetic_gen():
    article_slug = f'''nutrition/drinks/matcha/aesthetic'''
    print(f'ARTICLE: {article_slug}')
    article_obj = {
        'article_slug': article_slug,
        'keyword_main': 'matcha aesthetic',
        'keyword_main_slug': 'matcha-aesthetic',
        'keyword_main_pretty': 'matcha aesthetics',
        'keyword_main_title': 'matcha aesthetics healthy herbal nutrition',
        'pin_board_name': g.PIN_BOARD_NAME_NUTRITION,
        'main_list_num': '10',
        'article_type': 'listicle',
        'images_prompts': ['matcha, cozy, bokeh, depth of field, high resolution'],
        'links': [],
    }
    article.images_gen(article_obj, regen=False, dispel=False)
    article.json_gen(article_obj, regen=False, dispel=False)
    article.html_gen(article_slug)

def article_nutrition_drinks_matcha_gen():
    article_slug = f'''nutrition/drinks/matcha'''
    print(f'ARTICLE: {article_slug}')
    article_nutrition_drinks_matcha_aesthetic_gen()

def article_nutrition_drinks_gen():
    article_slug = f'''nutrition/drinks'''
    print(f'ARTICLE: {article_slug}')
    article_nutrition_drinks_coffee_gen()
    article_nutrition_drinks_matcha_gen()

def article_nutrition_gen():
    article_slug = f'''nutrition'''
    print(f'ARTICLE: {article_slug}')
    article_nutrition_drinks_gen()

def gen():
    print(f'HUB: nutrition')
    article_nutrition_gen()
