from lib import g
from lib import io
from lib import components
from lib import sections

def gen():
    url = f'shop'
    obj = {
        'url': url,
    }
    html_main = f''
    shop_items = [
        {
            'name': 'Herbal Jar Label Designs',
            'img_src': '/images/shop/herbal-jar-label-designs.jpg',
            'img_alt': 'herbal jar label designs',
            'href': '/shop/labels.html',
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
    ]
    shop_items_html = f''
    for shop_item_i, shop_item in enumerate(shop_items):
        shop_items_html += f'''
            <div class="card-default">
                <a href="{shop_item['href']}">
                    <h2 style="margin-bottom: 1.6rem;">{shop_item['name'].title()}</h2>
                    <img src="{shop_item['img_src']}" alt="{shop_item['img_alt']}">
                </a>
            </div>
        '''
    html_main += f'''
        <div class="grid-3" style="gap: 3.2rem;">
            {shop_items_html}
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
    html_filepath = f'''{g.website_folderpath}/shop.html'''
    with open(html_filepath, 'w') as f: f.write(html)

