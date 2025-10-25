import os
import random

from lib import g
from lib import io
from lib import llm
from lib import media
from lib import utils
from lib import polish
from lib import components
from lib import sections

def article_art_aesthetic_gen():
    data = [
        {'article_url_slug': 'art/aesthetic/pink', 'article_keyword': 'pink aesthetic', },
        {'article_url_slug': 'art/aesthetic/pfp', 'article_keyword': 'pfp aesthetic', },
        {'article_url_slug': 'art/aesthetic/blue', 'article_keyword': 'blue aesthetic', },
        {'article_url_slug': 'art/aesthetic/orange', 'article_keyword': 'orange aesthetic', },
        {'article_url_slug': 'art/aesthetic/green', 'article_keyword': 'green aesthetic', },
        {'article_url_slug': 'art/aesthetic/black', 'article_keyword': 'black aesthetic', },
        {'article_url_slug': 'art/aesthetic/black-white', 'article_keyword': 'black and white aesthetic', },
        {'article_url_slug': 'art/aesthetic/night', 'article_keyword': 'night aesthetic', },
        {'article_url_slug': 'art/aesthetic/autumn', 'article_keyword': 'autumn aesthetic', },
    ]
    for item in data:
        article_url_slug = item['article_url_slug']
        article_keyword = item['article_keyword']
        article_keyword_slug = polish.sluggify(article_keyword)

        ########################################
        # init
        ########################################
        json_article_filepath = f'''{g.DATABASE_FOLDERPATH}/json/{item['article_url_slug']}.json'''
        json_article = io.json_read(json_article_filepath, create=True)
        json_article['article_url_slug'] = article_url_slug
        json_article['article_keyword'] = article_keyword
        json_article['article_keyword_slug'] = article_keyword
        json_article['article_title'] = f'''{article_keyword} with medicinal herbs'''.title()
        json_article['main_list_num'] = f'''10'''
        json_article['images_prompts'] = [f'''{article_keyword} with medicinal herbs, soft focus, bokeh, depth of field, high resolution''']
        io.json_write(json_article_filepath, json_article)

        ########################################
        # images
        ########################################
        images_folderpath = f'{g.WEBSITE_FOLDERPATH}/images/{article_url_slug}'
        io.folders_recursive_gen(images_folderpath)
        regen = False
        dispel = False
        if regen:
            for image_filename in os.listdir(images_folderpath):
                image_filepath = f'{images_folderpath}/{image_filename}'
                if os.path.isfile(image_filepath):
                    os.remove(image_filepath)
        if dispel:
            for image_filename in os.listdir(images_folderpath):
                image_filepath = f'{images_folderpath}/{image_filename}'
                if os.path.isfile(image_filepath):
                    os.remove(image_filepath)
            return
        for i in range(int(json_article['main_list_num'])):
            found = False
            for filename in os.listdir(images_folderpath):
                if filename.startswith(f'{i}-'):
                    found = True
                    break
            if not found:
                image_prompt = json_article['images_prompts'][i % len(json_article['images_prompts'])]
                print(f'##################################################')
                print(f'{image_prompt}')
                print(f'##################################################')
                prompt = f'''
                    Write a slug in less than 7 words about the following title: {image_prompt.split(',')[0].lower()}.
                    Include only the most important words and do not include stop words.
                    Separate the words with the character "-", which is common for slugs.
                    Start the slug with the following words: {article_keyword_slug}.
                    Use only ascii characters.
                    Reply only with the slug.
                '''
                prompt += f'/no_think'
                print(prompt)
                reply = llm.reply(prompt).strip()
                if '</think>' in reply:
                    reply = reply.split('</think>')[1].strip()
                reply = reply.strip().lower().replace(' ', '-')
                image_filename = f'''{i}-{reply}.jpg'''
                image_filepath = f'{g.WEBSITE_FOLDERPATH}/images/{article_url_slug}/{image_filename}' 
                print(f'''{i}/{json_article['main_list_num']}''')
                image = media.image_gen(image_prompt, 832, 1216)
                image.save(image_filepath)
        ### featured
        image_prompt = random.choice(json_article['images_prompts'])
        image_filename = f'''{json_article['article_keyword_slug']}.jpg'''
        image_filepath = f'{g.WEBSITE_FOLDERPATH}/images/{article_url_slug}/{image_filename}' 
        if not os.path.exists(image_filepath):
            image = media.image_gen(image_prompt, 1024, 1024)
            image.save(image_filepath)

        ########################################
        # json
        ########################################
        regen = False
        dispel = False
        key = 'intro'
        if key not in json_article: 
            json_article[key] = ''
        if dispel: 
            json_article[key] = ''
            io.json_write(json_article_filepath, json_article)
            return
        if regen: 
            json_article[key] = ''
        if json_article[key] == '':
            prompt = f'''
                Write a detailed intro paragraph in 6 sentences for an article with the following title: {json_article['article_title']}.
                Write only the paragaraph.
                Use only ascii characters.
            '''
            prompt += f'/no_think'
            print(prompt)
            reply = llm.reply(prompt).strip()
            if '</think>' in reply:
                reply = reply.split('</think>')[1].strip()
            json_article[key] = reply
            io.json_write(json_article_filepath, json_article)

        regen = False
        dispel = False
        key = 'main_list'
        if key not in json_article: 
            json_article[key] = []
        if dispel: 
            json_article[key] = []
            io.json_write(json_article_filepath, json_article)
            return
        if regen: 
            json_article[key] = []
        if json_article[key] == []:
            images_folderpath = f'''{g.WEBSITE_FOLDERPATH}/images/{article_url_slug}'''
            io.folders_recursive_gen(images_folderpath)
            output_list = []
            for image_filename in sorted(os.listdir(images_folderpath)):
                if not image_filename[0].isdigit(): continue
                output_list.append({
                    'image_filename': image_filename,
                })
            json_article[key] = output_list
            io.json_write(json_article_filepath, json_article)

        key = 'image_desc'
        for json_obj in json_article['main_list']:
            if key not in json_obj: 
                json_obj[key] = ''
            if dispel: 
                json_obj[key] = ''
                io.json_write(json_article_filepath, json_article)
                return
            if regen: 
                json_obj[key] = ''
            if json_obj[key] == '':
                images_folderpath = f'''{g.WEBSITE_FOLDERPATH}/images/{article_url_slug}'''
                image_filename = json_obj['image_filename']
                image_filepath = f'{images_folderpath}/{image_filename}'
                image_prompt = image_filename
                image_prompt = image_prompt.replace('.jpg', '')
                if image_prompt[0].isdigit():
                    image_prompt = '-'.join(image_prompt.split('-')[1:])
                image_prompt = image_prompt.replace('-', ' ')
                print(image_prompt)
                prompt = f'''
                    Write a small description in about 40 words for the following image: {image_prompt}.
                '''
                prompt += f'/no_think'
                reply = llm.reply(prompt).strip()
                if '</think>' in reply:
                    reply = reply.split('</think>')[1].strip()
                json_obj[key] = reply
                io.json_write(json_article_filepath, json_article)
        key = 'image_alt'
        for json_obj in json_article['main_list']:
            if key not in json_obj: 
                json_obj[key] = ''
            if dispel: 
                json_obj[key] = ''
                io.json_write(json_article_filepath, json_article)
                return
            if regen: 
                json_obj[key] = ''
            if json_obj[key] == '':
                images_folderpath = f'''{g.WEBSITE_FOLDERPATH}/images/{article_url_slug}'''
                image_filename = json_obj['image_filename']
                image_filepath = f'{images_folderpath}/{image_filename}'
                image_prompt = image_filename
                image_prompt = image_prompt.replace('.jpg', '')
                if image_prompt[0].isdigit():
                    image_prompt = '-'.join(image_prompt.split('-')[1:])
                image_prompt = image_prompt.replace('-', ' ')
                print(image_prompt)
                prompt = f'''
                    Write a small alt description in less than 10 words for the following image: {image_prompt}.
                '''
                prompt += f'/no_think'
                reply = llm.reply(prompt).strip()
                if '</think>' in reply:
                    reply = reply.split('</think>')[1].strip()
                json_obj[key] = reply
                io.json_write(json_article_filepath, json_article)

        ########################################
        # html
        ########################################
        html_article = ''
        json_title = f'''{json_article['article_title']}'''
        meta_title = f'''{json_title}'''
        meta_description = f''
        html_article += f'''<h1>{json_title.title()}</h1>'''
        src = f'''/images/{article_url_slug}/{json_article['article_keyword_slug']}.jpg'''
        alt = f'''{json_article['article_keyword']}'''
        html_article += f'''<img src="{src}" alt="{alt}">'''
        html_article += f'''{utils.format_1N1(json_article['intro'])}'''
        html_article += f'<h2>{json_article["article_keyword"].title()}</h2>\n'
        html_article += f'''<div class="listicle">\n'''
        for i, item in enumerate(json_article['main_list']):
            image_filename = f'''{item['image_filename']}'''
            image_desc = f'''{i+1}. {item['image_desc']}'''
            src = f'/images/{article_url_slug}/{image_filename}'
            alt = f'''{item['image_alt']}'''
            html_article += f'''<p>{image_desc}</p>\n'''
            html_article += f'''<img src="{src}" alt="{alt}">\n'''
            html_article += f'''<div style="margin-bottom: 4.8rem;"><a class="button-default" href="{src}">Download Image</a></div>'''
        html_article += f'''</div>\n'''
        ### lead magnet
        form_head = ''
        if 0:
            with open(f'{g.DATABASE_FOLDERPATH}/assets/scripts/newsletter/form-head.txt') as f: form_head = f.read()
            with open(f'{g.DATABASE_FOLDERPATH}/assets/scripts/newsletter/form-course-preparation-tincture.txt') as f: form_body = f.read()
            html_article += f'''
                <div class="free-gift">
                    <p class="free-gift-heading">FREE COURSE</p>
                    <p style="text-align: center; margin-bottom: 1.6rem;">How to make medicinal herbal tinctures for common ailments at home and in a weekend (using the Healing Drops System).</p>
                    <img src="/images/shop/banner-course-preparation-tincture.jpg" alt="tincture preparation course banner">
                    {form_body}
                </div>
            '''
        ### toc
        # html_article += f'''[toc]'''
        # html_article += f'''<h2>Scientific and Botanical Profile</h2>'''
        # html_article += f'''{utils.format_1N1(json_article['botany'])}'''
        # html_article = sections.toc(html_article)
        html = f'''
            <!DOCTYPE html>
            <html lang="en">
            {components.html_head(meta_title, meta_description, form_head)}
            <body>
                {sections.header()}
                {sections.breadcrumbs(json_article['article_url_slug'])}
                <main class="container-md article">
                    {html_article}
                </main>
                <div class="mt-64"></div>
                {sections.footer()}
            </body>
            </html>
        '''
        html_filepath = f'''{g.website_folderpath}/{json_article['article_url_slug']}.html'''
        with open(html_filepath, 'w') as f: f.write(html)
        # quit()

def main():
    article_art_aesthetic_gen()
    pass
