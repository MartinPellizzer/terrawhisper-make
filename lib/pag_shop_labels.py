from lib import g
from lib import io
from lib import components
from lib import sections

def gen():
    url = f'shop/labels'
    obj = {
        'url': url,
    }
    with open(f'{g.assets_folderpath}/scripts/newsletter/form-head.txt') as f: form_head = f.read()
    with open(f'{g.assets_folderpath}/scripts/newsletter/form-labels.txt') as f: form_labels = f.read()
    html_main = f''
    img_src = '/images/shop/herbal-jar-label-designs.jpg'
    img_alt = 'herbal jar label designs'
    html_main = f'''
        <div class='product'>
            <p style="text-align: center; margin-bottom: 1.6rem;">FREE Designs:</p>
            <h1 style="text-align: center; margin-bottom: 1.6rem;">120 Herbal Jar Label Designs</h1>
            <p style="text-align: center; margin-bottom: 1.6rem;">Download these free desings to print beautiful labels for your jars.</p>
            <div class="container-sm" style="margin-bottom: 1.6rem;">
                <img src="{img_src}" alt="{img_alt}">
            </div>
            <p style="text-align: center; margin-bottom: 1.6rem;">Enter the email where you want me to send your labels in the form below.</p>
            {form_labels}
        </div>
    '''
    ###
    meta_title = f'''Herbal Jar Label Designs | TerraWhisper Shop'''
    meta_description = f''''''
    html = f'''
        <!DOCTYPE html>
        <html lang="en">
        {components.html_head(meta_title, meta_description, form_head)}
        <body>
            {sections.header()}
            {sections.breadcrumbs(obj['url'])}
            <div class="spacer"></div>
            <main class="container-md">
                {html_main}
            </main>
            <div class="spacer"></div>
            {sections.footer()}
        </body>
        </html>
    '''
    html_filepath = f'''{g.website_folderpath}/{obj['url']}.html'''
    with open(html_filepath, 'w') as f: f.write(html)

