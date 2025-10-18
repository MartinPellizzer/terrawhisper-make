import os

from lib import g
from lib import components
from lib import sections

def html_page_styles_gen():
    label_oval_filename = os.listdir(f'{g.website_folderpath}/assets/shop/labels/100/vintage/oval/1x2/jpg/')[0]
    label_rectangle_filename = os.listdir(f'{g.website_folderpath}/assets/shop/labels/100/vintage/rectangle/1x2/jpg/')[0]
    label_round_filename = os.listdir(f'{g.website_folderpath}/assets/shop/labels/100/vintage/round/1x1/jpg/')[0]
    label_square_filename = os.listdir(f'{g.website_folderpath}/assets/shop/labels/100/vintage/square/1x1/jpg/')[0]
    html_main = ''
    html_main += f'''
        <h1>1200 Vintage Herbal Jar Labels [Digital Designs]</h1>
        <div class="spacer-md"></div>
        <p>
            To download any of the 1200 herbal jar labels (digital printables), start by choosing the label shape. You can choose between 4 different shapes: oval, rectangle, round, or square.
        </p>
        <div class="spacer-md"></div>
        <div class="grid-4" style="gap: 3.2rem;">
            <div>
                <h2 style="margin-bottom: 1.6rem;">Oval</h2>
                <a href="/shop/labels-premium/download/oval.html" class="button-default">View Oval Labels</a>
                <div class="spacer-sm"></div>
                <img src="/assets/shop/labels/100/vintage/oval/2x3/jpg/{label_oval_filename}">
            </div>
            <div>
                <h2 style="margin-bottom: 1.6rem;">Rectangle</h2>
                <a href="/shop/labels-premium/download/rectangle.html" class="button-default">View Rectangle Labels</a>
                <div class="spacer-sm"></div>
                <img src="/assets/shop/labels/100/vintage/rectangle/2x3/jpg/{label_rectangle_filename}">
            </div>
            <div>
                <h2 style="margin-bottom: 1.6rem;">Round</h2>
                <a href="/shop/labels-premium/download/round.html" class="button-default">View Round Labels</a>
                <div class="spacer-sm"></div>
                <img src="/assets/shop/labels/100/vintage/round/2x2/jpg/{label_round_filename}">
            </div>
            <div>
                <h2 style="margin-bottom: 1.6rem;">Square</h2>
                <a href="/shop/labels-premium/download/square.html" class="button-default">View Square Labels</a>
                <div class="spacer-sm"></div>
                <img src="/assets/shop/labels/100/vintage/square/2x2/jpg/{label_square_filename}">
            </div>
        </div>
    '''
    meta_title = f'''Herbal Jar Labels Download'''
    meta_description = f''''''
    html = f'''
        <!DOCTYPE html>
        <html lang="en">
        {components.html_head(meta_title, meta_description)}
        <body>
            {sections.header()}
            <div class="spacer"></div>
            <main class="container-xl">
                {html_main}
            </main>
            <div class="spacer"></div>
            {sections.footer()}
        </body>
        </html>
    '''
    html_filepath = f'''{g.website_folderpath}/shop/labels-premium/download.html'''
    with open(html_filepath, 'w') as f: f.write(html)

def html_page_style_shape_gen(style):
    size_small = ''
    size_medium = ''
    size_large = ''
    if style == 'oval' or style == 'rectangle': 
        size_small = '1x2'
        size_medium = '2x3'
        size_large = '3x5'
    if style == 'round' or style == 'square': 
        size_small = '1x1'
        size_medium = '2x2'
        size_large = '3x3'
    label_filename = os.listdir(f'{g.website_folderpath}/assets/shop/labels/100/vintage/{style}/{size_small}/jpg/')[0]
    html_main = ''
    html_main += f'''
        <h1>Herbal Jar Labels - Vintage {style.title()}</h1>
        <div class="spacer-md"></div>
        <p style="margin-bottom: 1.6rem;">
            Choose the size of the labels. You can choose between 3 sizes: small, medium, and large. 
        </p>
        <p>
            <b>WARNING:</b> The images below don't reflect the actual size of the labels. They are just thumbnails. The actual size of the the labels is stated above the images (in inches).
        </p>
        <div class="spacer-md"></div>
        <div class="grid-3" style="gap: 3.2rem;">
            <div>
                <h2 style="margin-bottom: 1.6rem;">Small ({size_small} inches)</h2>
                <a href="/shop/labels-premium/download/{style}/small.html" class="button-default">View Small Labels</a>
                <div class="spacer-sm"></div>
                <img src="/assets/shop/labels/100/vintage/{style}/{size_small}/jpg/{label_filename}" style="max-width: 100px;">
            </div>
            <div>
                <h2 style="margin-bottom: 1.6rem;">Medium ({size_medium} inches)</h2>
                <a href="/shop/labels-premium/download/{style}/medium.html" class="button-default">View Medium Labels</a>
                <div class="spacer-sm"></div>
                <img src="/assets/shop/labels/100/vintage/{style}/{size_medium}/jpg/{label_filename}" style="max-width: 200px;">
            </div>
            <div>
                <h2 style="margin-bottom: 1.6rem;">Large ({size_large} inches)</h2>
                <a href="/shop/labels-premium/download/{style}/large.html" class="button-default">View Large Labels</a>
                <div class="spacer-sm"></div>
                <img src="/assets/shop/labels/100/vintage/{style}/{size_large}/jpg/{label_filename}" style="max-width: 300px;">
            </div>
        </div>
    '''
    meta_title = f'''Herbal Jar Labels Download - Vintage {style.title()}'''
    meta_description = f''''''
    html = f'''
        <!DOCTYPE html>
        <html lang="en">
        {components.html_head(meta_title, meta_description)}
        <body>
            {sections.header()}
            <div class="spacer"></div>
            <main class="container-xl">
                {html_main}
            </main>
            <div class="spacer"></div>
            {sections.footer()}
        </body>
        </html>
    '''
    html_filepath = f'''{g.website_folderpath}/shop/labels-premium/download/{style}.html'''
    with open(html_filepath, 'w') as f: f.write(html)

def html_page_style_shape_size_gen(style, size):
    size_text = ''
    if size == '3x5': size_text = 'large'
    elif size == '3x3': size_text = 'large'
    elif size == '2x3': size_text = 'medium'
    elif size == '2x2': size_text = 'medium'
    elif size == '1x2': size_text = 'small'
    elif size == '1x1': size_text = 'small'
    html_labels = ''
    input_folderpath = f'{g.website_folderpath}/assets/shop/labels/100/vintage/{style}/{size}/jpg'
    preview_folderpath = f'/assets/shop/labels/100/vintage/{style}/{size}/jpg'
    filename_list = sorted(os.listdir(input_folderpath))
    for filename in filename_list:
        preview_filepath = f'{preview_folderpath}/{filename}'
        download_filepath = preview_filepath.replace('jpg', 'png')
        title = filename
        title = ' '.join(title.split('-')[1:]).capitalize()
        title = ' '.join(title.split('.')[:-1]).capitalize()
        title = '<br>'.join(title.split(' ')).capitalize()
        html_labels += f'''
            <div>
                <h2 style="margin-bottom: 1.6rem;">{title}</h2>
                <a href="{download_filepath}" class="button-default">Download Label</a>
                <div class="spacer-sm"></div>
                <img src="{preview_filepath}">
            </div>
        '''
    html_main = ''
    html_main += f'''
        <h1>Herbal Jar Labels - Vintage {style.title()} {size_text.title()} ({size} inches)</h1>
        <div class="spacer-md"></div>
        <p style="margin-bottom: 1.6rem;">
            Choose the label you want to download (by herb). You can choose between 100 popular herbs. To download the label, click on the button under the herb name.
        </p>
        <p>
            <b>WARNING:</b> The images below don't reflect the actual size of the labels. They are just thumbnails. The actual size of the the labels is stated in the title at the top of this page (in inches).
        </p>
        <div class="spacer-md"></div>
        <div class="grid-4" style="gap: 3.2rem;">
            {html_labels}
        </div>
    '''
    meta_title = f'''Herbal Jar Labels Download - Vitage {style.title()} {size_text.title()}'''
    meta_description = f''''''
    html = f'''
        <!DOCTYPE html>
        <html lang="en">
        {components.html_head(meta_title, meta_description)}
        <body>
            {sections.header()}
            <div class="spacer"></div>
            <main class="container-xl">
                {html_main}
            </main>
            <div class="spacer"></div>
            {sections.footer()}
        </body>
        </html>
    '''
    html_filepath = f'''{g.website_folderpath}/shop/labels-premium/download/{style}/{size_text}.html'''
    with open(html_filepath, 'w') as f: f.write(html)

def html_page_free_gen():
    url = f'shop/labels/download'
    obj = {
        'url': url,
    }
    input_folderpath = f'{g.website_folderpath}/assets/shop/labels/100/vintage/oval/1x2/jpg'
    filename_list = sorted(os.listdir(input_folderpath))
    html_labels = ''
    styles = ['oval', 'rectangle', 'round', 'square']
    for style in styles:
        if style == 'oval' or style == 'rectangle':
            preview_folderpath = f'/assets/shop/labels/100/vintage/{style}/1x2/jpg'
        else:
            preview_folderpath = f'/assets/shop/labels/100/vintage/{style}/1x1/jpg'
        html_labels += f'''<h2 style="font-size: 4.8rem; margin-bottom: 3.2rem; margin-top: 6.4rem;">{style.title()}</h2>'''
        html_labels += f'''<hr style="margin-bottom: 3.2rem;">'''
        html_labels += f'''<div class="grid-4" style="gap: 3.2rem;">'''
        for filename in filename_list[:10]:
            preview_filepath = f'{preview_folderpath}/{filename}'
            download_filepath = preview_filepath.replace('jpg', 'png')
            title = filename
            title = ' '.join(title.split('-')[1:]).capitalize()
            title = ' '.join(title.split('.')[:-1]).capitalize()
            title = '<br>'.join(title.split(' ')).capitalize()
            html_labels += f'''
                <div>
                    <h3 style="margin-bottom: 1.6rem;">{title}</h3>
                    <a href="{download_filepath}" class="button-default">Download Label</a>
                    <div class="spacer-sm"></div>
                    <img src="{preview_filepath}">
                </div>
            '''
        html_labels += f'''</div>'''

    html_main = ''
    html_main += f'''
        <h1>120 Herbal Jar Label Designs</h1>
        <div class="spacer-md"></div>
        {html_labels}
    '''

    if 0:
        label_oval_filename = os.listdir(f'{g.website_folderpath}/assets/shop/labels/100/vintage/oval/1x2/jpg/')[0]
        label_rectangle_filename = os.listdir(f'{g.website_folderpath}/assets/shop/labels/100/vintage/rectangle/1x2/jpg/')[0]
        label_round_filename = os.listdir(f'{g.website_folderpath}/assets/shop/labels/100/vintage/round/1x1/jpg/')[0]
        label_square_filename = os.listdir(f'{g.website_folderpath}/assets/shop/labels/100/vintage/square/1x1/jpg/')[0]
        html_main += f'''
            <h1>1200 Vintage Herbal Jar Labels [Digital Designs]</h1>
            <div class="spacer-md"></div>
            <p>
                To download any of the 1200 herbal jar labels (digital printables), start by choosing the label shape. You can choose between 4 different shapes: oval, rectangle, round, or square.
            </p>
            <div class="spacer-md"></div>
            <div class="grid-4" style="gap: 3.2rem;">
                <div>
                    <h2 style="margin-bottom: 1.6rem;">Oval</h2>
                    <a href="/shop/labels-premium/download/oval.html" class="button-default">View Oval Labels</a>
                    <div class="spacer-sm"></div>
                    <img src="/assets/shop/labels/100/vintage/oval/2x3/jpg/{label_oval_filename}">
                </div>
                <div>
                    <h2 style="margin-bottom: 1.6rem;">Rectangle</h2>
                    <a href="/shop/labels-premium/download/rectangle.html" class="button-default">View Rectangle Labels</a>
                    <div class="spacer-sm"></div>
                    <img src="/assets/shop/labels/100/vintage/rectangle/2x3/jpg/{label_rectangle_filename}">
                </div>
                <div>
                    <h2 style="margin-bottom: 1.6rem;">Round</h2>
                    <a href="/shop/labels-premium/download/round.html" class="button-default">View Round Labels</a>
                    <div class="spacer-sm"></div>
                    <img src="/assets/shop/labels/100/vintage/round/2x2/jpg/{label_round_filename}">
                </div>
                <div>
                    <h2 style="margin-bottom: 1.6rem;">Square</h2>
                    <a href="/shop/labels-premium/download/square.html" class="button-default">View Square Labels</a>
                    <div class="spacer-sm"></div>
                    <img src="/assets/shop/labels/100/vintage/square/2x2/jpg/{label_square_filename}">
                </div>
            </div>
        '''
    meta_title = f'''Herbal Jar Labels Download'''
    meta_description = f''''''
    html = f'''
        <!DOCTYPE html>
        <html lang="en">
        {components.html_head(meta_title, meta_description)}
        <body>
            {sections.header()}
            {sections.breadcrumbs(obj['url'])}
            <div class="spacer"></div>
            <main class="container-xl">
                {html_main}
            </main>
            <div class="spacer"></div>
            {sections.footer()}
        </body>
        </html>
    '''
    html_filepath = f'''{g.website_folderpath}/{obj["url"]}.html'''
    with open(html_filepath, 'w') as f: f.write(html)

def free_gen():
    html_page_free_gen()

def premium_gen():
    html_page_styles_gen()
    html_page_style_shape_gen('oval')
    html_page_style_shape_gen('rectangle')
    html_page_style_shape_gen('round')
    html_page_style_shape_gen('square')
    html_page_style_shape_size_gen(style='oval', size='1x2')
    html_page_style_shape_size_gen(style='oval', size='2x3')
    html_page_style_shape_size_gen(style='oval', size='3x5')
    html_page_style_shape_size_gen(style='rectangle', size='1x2')
    html_page_style_shape_size_gen(style='rectangle', size='2x3')
    html_page_style_shape_size_gen(style='rectangle', size='3x5')
    html_page_style_shape_size_gen(style='round', size='1x1')
    html_page_style_shape_size_gen(style='round', size='2x2')
    html_page_style_shape_size_gen(style='round', size='3x3')
    html_page_style_shape_size_gen(style='square', size='1x1')
    html_page_style_shape_size_gen(style='square', size='2x2')
    html_page_style_shape_size_gen(style='square', size='3x3')

def gen():
    free_gen()
    # premium_gen()
