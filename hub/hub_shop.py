import os

from lib import g
from lib import io
from lib import components
from lib import sections

def file_read_txt(filepath):
    with open(filepath) as f: 
        content = f.read()
    return content

def shop_course_prapration_tincture_download_gen():
    url_slug = f'shop/course-preparation-tincture/download'
    obj = {
        'url_slug': url_slug,
    }
    ###
    with open(f'{g.DATABASE_FOLDERPATH}/shop/courses/tincture-making/embeddings/00.txt') as f: lesson_00 = f.read()
    with open(f'{g.DATABASE_FOLDERPATH}/shop/courses/tincture-making/embeddings/01.txt') as f: lesson_01 = f.read()
    with open(f'{g.DATABASE_FOLDERPATH}/shop/courses/tincture-making/embeddings/02.txt') as f: lesson_02 = f.read()
    with open(f'{g.DATABASE_FOLDERPATH}/shop/courses/tincture-making/embeddings/03.txt') as f: lesson_03 = f.read()
    with open(f'{g.DATABASE_FOLDERPATH}/shop/courses/tincture-making/embeddings/04.txt') as f: lesson_04 = f.read()
    with open(f'{g.DATABASE_FOLDERPATH}/shop/courses/tincture-making/embeddings/05.txt') as f: lesson_05 = f.read()
    with open(f'{g.DATABASE_FOLDERPATH}/shop/courses/tincture-making/embeddings/06.txt') as f: lesson_06 = f.read()
    with open(f'{g.DATABASE_FOLDERPATH}/shop/courses/tincture-making/embeddings/07.txt') as f: lesson_07 = f.read()
    with open(f'{g.DATABASE_FOLDERPATH}/shop/courses/tincture-making/embeddings/08.txt') as f: lesson_08 = f.read()
    with open(f'{g.DATABASE_FOLDERPATH}/shop/courses/tincture-making/embeddings/09.txt') as f: lesson_09 = f.read()
    with open(f'{g.DATABASE_FOLDERPATH}/shop/courses/tincture-making/embeddings/10.txt') as f: lesson_10 = f.read()
    css_lesson_margin_top = '1.6rem;'
    css_lesson_margin_bottom = '9.6rem;'
    html_lessons = f'''
        <div class="container-xl">
            <h2 style="text-align: center; margin-bottom: {css_lesson_margin_top};">Module 1 - Lesson 1</h2>
            <div style="display: flex; justify-content: center; margin-bottom: {css_lesson_margin_bottom};">
                {lesson_00}
            </div>
        </div>
        <div class="container-xl">
            <h2 style="text-align: center; margin-bottom: {css_lesson_margin_top};">Module 2 - Lesson 1</h2>
            <div style="display: flex; justify-content: center; margin-bottom: {css_lesson_margin_bottom};">
                {lesson_01}
            </div>
        </div>
        <div class="container-xl">
            <h2 style="text-align: center; margin-bottom: {css_lesson_margin_top};">Module 2 - Lesson 2</h2>
            <div style="display: flex; justify-content: center; margin-bottom: {css_lesson_margin_bottom};">
                {lesson_02}
            </div>
        </div>
        <div class="container-xl">
            <h2 style="text-align: center; margin-bottom: {css_lesson_margin_top};">Module 2 - Lesson 3</h2>
            <div style="display: flex; justify-content: center; margin-bottom: {css_lesson_margin_bottom};">
                {lesson_03}
            </div>
        </div>
        <div class="container-xl">
            <h2 style="text-align: center; margin-bottom: {css_lesson_margin_top};">Module 3 - Lesson 1</h2>
            <div style="display: flex; justify-content: center; margin-bottom: {css_lesson_margin_bottom};">
                {lesson_04}
            </div>
        </div>
        <div class="container-xl">
            <h2 style="text-align: center; margin-bottom: {css_lesson_margin_top};">Module 3 - Lesson 2</h2>
            <div style="display: flex; justify-content: center; margin-bottom: {css_lesson_margin_bottom};">
                {lesson_05}
            </div>
        </div>
        <div class="container-xl">
            <h2 style="text-align: center; margin-bottom: {css_lesson_margin_top};">Module 3 - Lesson 3</h2>
            <div style="display: flex; justify-content: center; margin-bottom: {css_lesson_margin_bottom};">
                {lesson_06}
            </div>
        </div>
        <div class="container-xl">
            <h2 style="text-align: center; margin-bottom: {css_lesson_margin_top};">Module 4 - Lesson 1</h2>
            <div style="display: flex; justify-content: center; margin-bottom: {css_lesson_margin_bottom};">
                {lesson_07}
            </div>
        </div>
        <div class="container-xl">
            <h2 style="text-align: center; margin-bottom: {css_lesson_margin_top};">Module 4 -Lesson 2</h2>
            <div style="display: flex; justify-content: center; margin-bottom: {css_lesson_margin_bottom};">
                {lesson_08}
            </div>
        </div>
        <div class="container-xl">
            <h2 style="text-align: center; margin-bottom: {css_lesson_margin_top};">Module 4 -Lesson 3</h2>
            <div style="display: flex; justify-content: center; margin-bottom: {css_lesson_margin_bottom};">
                {lesson_09}
            </div>
        </div>
        <div class="container-xl">
            <h2 style="text-align: center; margin-bottom: {css_lesson_margin_top};">Module 5 -Lesson 1</h2>
            <div style="display: flex; justify-content: center; margin-bottom: {css_lesson_margin_bottom};">
                {lesson_10}
            </div>
        </div>
    '''
    html_main = f'''
        <h1 style="font-size: 6.4rem; line-height: 1; margin-bottom: 1.6rem; text-align: center;">Herbal Tincture Course</h1>
        <p style="margin-bottom: 4.8rem; text-align: center;">How to make medicinal herbal tincture for common ailments at home in a weekend (with the Healing Drops System).</p>
        {html_lessons}
    '''
    ###
    meta_title = f'''Tincture Preparation Course Download | TerraWhisper Shop'''
    meta_description = f''''''
    html = f'''
        <!DOCTYPE html>
        <html lang="en">
        {components.html_head(meta_title, meta_description)}
        <body>
            {sections.header()}
            {sections.breadcrumbs(obj['url_slug'])}
            <div class="spacer"></div>
            <main class="container-md">
                {html_main}
            </main>
            <div class="spacer"></div>
            {sections.footer()}
        </body>
        </html>
    '''
    html_filepath = f'''{g.website_folderpath}/{obj['url_slug']}.html'''
    with open(html_filepath, 'w') as f: f.write(html)

def shop_item_gen():
    shop_course_prapration_tincture_download_gen()

    url_slug = f'shop/course-preparation-tincture'
    obj = {
        'url_slug': url_slug,
    }

    form_head = file_read_txt(f'{g.ASSETS_FOLDERPATH}/scripts/newsletter/form-head.txt')
    form_body = file_read_txt(f'{g.ASSETS_FOLDERPATH}/scripts/newsletter/form-course-preparation-tincture.txt')
    img_src = '/images/shop/banner-course-preparation-tincture.jpg'
    img_alt = 'tincture preparation course banner'
    html_main = f'''
        <div class='product'>
            <p style="text-align: center; margin-bottom: 1.6rem;">FREE COURSE</p>
            <h1 style="text-align: center; margin-bottom: 1.6rem;">Tincture Preparation Course</h1>
            <p style="text-align: center; margin-bottom: 1.6rem;">How to make medicinal herbal tinctures for common ailments at home and in a weekend (using the Healing Drops System).</p>
            <div class="container-sm" style="margin-bottom: 1.6rem;">
                <img src="{img_src}" alt="{img_alt}">
            </div>
            <p style="text-align: center; margin-bottom: 1.6rem;">Enter the email where you want me to send your free download in the form below.</p>
            {form_body}
        </div>
    '''

    ###
    meta_title = f'''Tincture Preparation Course | TerraWhisper Shop'''
    meta_description = f''''''
    html = f'''
        <!DOCTYPE html>
        <html lang="en">
        {components.html_head(meta_title, meta_description, form_head)}
        <body>
            {sections.header()}
            {sections.breadcrumbs(obj['url_slug'])}
            <div class="spacer"></div>
            <main class="container-md">
                {html_main}
            </main>
            <div class="spacer"></div>
            {sections.footer()}
        </body>
        </html>
    '''
    html_filepath = f'''{g.website_folderpath}/{obj['url_slug']}.html'''
    with open(html_filepath, 'w') as f: f.write(html)

def shop_product_download_gen(data):
    url_slug = f'''shop/{data['slug']}/download'''
    ###
    form_head = ''
    preview_src = f'''/images/shop/{data['slug']}-preview.jpg'''
    preview_alt = f'''{data['product_title']} {data['product_type']} preview'''
    product_src = f'''/images/shop/{data['slug']}.jpg'''
    html_main = f'''
        <div class='product'>
            <p style="text-align: center; margin-bottom: 1.6rem;">YOUR DOWNLOAD IS READY</p>
            <h1 style="text-align: center; margin-bottom: 1.6rem;">{data['product_title'].title()} ({data['product_type'].title()})</h1>
            <p style="text-align: center; margin-bottom: 3.2rem;">{data['product_desc']}</p>
            <div class="container-sm" style="margin-bottom: 1.6rem;">
                <img src="{preview_src}" alt="{preview_alt}">
            </div>
            <div style="text-align: center;" >
                <a class="button-accent" href="{product_src}">CLICK HERE TO DOWNLOAD</a>
            </div>
        </div>
    '''
    ###
    meta_title = f'''{data['product_title']} {data['product_type']} Download | TerraWhisper Shop'''
    meta_description = f''''''
    html = f'''
        <!DOCTYPE html>
        <html lang="en">
        {components.html_head(meta_title, meta_description)}
        <body>
            {sections.header()}
            {sections.breadcrumbs(url_slug)}
            <div class="spacer"></div>
            <main class="container-md">
                {html_main}
            </main>
            <div class="spacer"></div>
            {sections.footer()}
        </body>
        </html>
    '''
    html_filepath = f'''{g.website_folderpath}/{url_slug}.html'''
    with open(html_filepath, 'w') as f: f.write(html)

def shop_product_gen(data):
    shop_product_download_gen(data)
    ###
    url_slug = f'''shop/{data['slug']}'''
    form_head = file_read_txt(f'{g.ASSETS_FOLDERPATH}/scripts/newsletter/form-head.txt')
    form_body = file_read_txt(f'{g.ASSETS_FOLDERPATH}/scripts/newsletter/form-checklist-foraging-fall.txt')
    banner_src = f'''/images/shop/{data['slug']}-banner.jpg'''
    banner_alt = f'''{data['product_title']} {data['product_type']} banner'''
    html_main = f'''
        <div class='product'>
            <p style="text-align: center; margin-bottom: 1.6rem;">FREE DOWNLOAD</p>
            <h1 style="text-align: center; margin-bottom: 1.6rem;">{data['product_title'].title()} ({data['product_type'].title()})</h1>
            <p style="text-align: center; margin-bottom: 3.2rem;">{data['product_desc']}</p>
            <div class="container-sm" style="margin-bottom: 1.6rem;">
                <img src="{banner_src}" alt="{banner_alt}">
            </div>
            <p style="text-align: center; margin-bottom: 1.6rem;">Where do you want me to send your free download? Enter your best email address in the form below.</p>
            {form_body}
        </div>
    '''
    ###
    meta_title = f'''{data['product_title']} {data['product_type']} | TerraWhisper Shop'''
    meta_description = f''''''
    html = f'''
        <!DOCTYPE html>
        <html lang="en">
        {components.html_head(meta_title, meta_description, form_head)}
        <body style="background-color: #f7f6f2;">
            {sections.header()}
            {sections.breadcrumbs(url_slug)}
            <div class="spacer"></div>
            <main class="container-md">
                {html_main}
            </main>
            <div class="spacer"></div>
            {sections.footer()}
        </body>
        </html>
    '''
    html_filepath = f'''{g.website_folderpath}/{url_slug}.html'''
    with open(html_filepath, 'w') as f: f.write(html)

def gen():
    json_dict = io.json_read(f'{g.DATABASE_FOLDERPATH}/shop/data.json')

    shop_item_gen()
    shop_product_gen(json_dict[0])
    shop_product_gen(json_dict[1])

    url_slug = f'shop'
    obj = {
        'url_slug': url_slug,
    }

    data = [
        {
            'category': 'courses',
            'products': [
                {
                    'name': 'Tincture Preparation Course',
                    'img_src': '/images/shop/banner-course-preparation-tincture.jpg',
                    'img_alt': 'tincture preparation course',
                    'href': '/shop/course-preparation-tincture.html',
                },
            ],
        },
        {
            'category': 'resources',
            'products': [
                {
                    'name': f'''{json_dict[0]['product_title']} ({json_dict[0]['product_type']})''',
                    'img_src': f'''/images/shop/{json_dict[0]['slug']}-banner.jpg''',
                    'img_alt': f'''{json_dict[0]['product_title']} {json_dict[0]['product_type']} banner''',
                    'href': f'''/shop/{json_dict[0]['slug']}.html''',
                },
                {
                    'name': f'''{json_dict[1]['product_title']} ({json_dict[1]['product_type']})''',
                    'img_src': f'''/images/shop/{json_dict[1]['slug']}-banner.jpg''',
                    'img_alt': f'''{json_dict[1]['product_title']} {json_dict[1]['product_type']} banner''',
                    'href': f'''/shop/{json_dict[1]['slug']}.html''',
                },
                {
                    'name': f'''{json_dict[3]['product_title']} ({json_dict[3]['product_type']})''',
                    'img_src': f'''/images/shop/{json_dict[3]['slug']}-banner.jpg''',
                    'img_alt': f'''{json_dict[3]['product_title']} {json_dict[3]['product_type']} banner''',
                    'href': f'''/shop/{json_dict[3]['slug']}.html''',
                },
                {
                    'name': 'Herb Drying Checklist',
                    'img_src': '/images/shop/herb-drying-checklist-blurred.jpg',
                    'img_alt': 'herb drying checklist blurred',
                    'href': '/shop/herb-drying-checklist.html',
                },
                {
                    'name': 'Tincture Dosage and Safety Cheatsheet',
                    'img_src': '/images/shop/tincture-dosage-safety-cheatsheet-blurred.jpg',
                    'img_alt': 'tincture dosage safety cheatsheet blurred',
                    'href': '/shop/tincture-dosage-safety-cheatsheet.html',
                },
            ],
        },
        {
            'category': 'designs',
            'products': [
                {
                    'name': 'Herbal Jar Label Designs',
                    'img_src': '/images/shop/herbal-jar-label-designs.jpg',
                    'img_alt': 'herbal jar label designs',
                    'href': '/shop/labels.html',
                },
            ],
        },
    ]
    html_main = f''
    for item in data:
        category = item['category']
        products = item['products']
        products_html = f''
        for product in products:
            products_html += f'''
                <div class="card-default">
                    <a href="{product['href']}">
                        <h2 style="margin-bottom: 1.6rem;">{product['name'].title()}</h2>
                        <img src="{product['img_src']}" alt="{product['img_alt']}">
                    </a>
                </div>
            '''
        html_main += f'''
            <h2 style="margin-bottom: 4.8rem; font-size: 4.8rem;">{category.title()}</h2>
            <div class="grid-3" style="gap: 3.2rem; margin-bottom: 9.6rem;">
                {products_html}
            </div>
        '''

    ###
    meta_title = f'''TerraWhisper Shop'''
    meta_description = f''''''
    html = f'''
        <!DOCTYPE html>
        <html lang="en">
        {components.html_head(meta_title, meta_description)}
        <body>
            {sections.header()}
            {sections.breadcrumbs(obj['url_slug'])}
            <div class="spacer"></div>
            <main class="container-xl">
                {html_main}
            </main>
            <div class="spacer"></div>
            {sections.footer()}
        </body>
        </html>
    '''
    html_filepath = f'''{g.website_folderpath}/shop.html'''
    with open(html_filepath, 'w') as f: f.write(html)

