from lib import g
from lib import io
from lib import components
from lib import sections

def gen():
    url = f'shop/tincture-dosage-safety-cheatsheet'
    obj = {
        'url': url,
    }
    with open(f'{g.assets_folderpath}/scripts/newsletter/form-head.txt') as f: form_head = f.read()
    with open(f'{g.assets_folderpath}/scripts/newsletter/form-tincture-dosage-safety-cheatsheet.txt') as f: 
        form_tincture_dosage_safety_cheatsheet = f.read()
    html_main = f''
    img_src = '/images/shop/tincture-dosage-safety-cheatsheet-blurred.jpg'
    img_alt = 'tincture dosage and safety cheatsheet blurred'
    html_main = f'''
        <div class='product'>
            <p style="text-align: center; margin-bottom: 1.6rem;">FREE Cheatsheet:</p>
            <h1 style="text-align: center; margin-bottom: 1.6rem;">Tincture Dosage & Safety Cheatsheet</h1>
            <p style="text-align: center; margin-bottom: 1.6rem;">Download this free cheatsheet and print it to always remember what to do when dosaging tinctures to stay safe.</p>
            <div class="container-sm" style="margin-bottom: 1.6rem;">
                <img src="{img_src}" alt="{img_alt}">
            </div>
            <p style="text-align: center; margin-bottom: 1.6rem;">Enter the email where you want me to send your free download in the form below.</p>
            {form_tincture_dosage_safety_cheatsheet}
        </div>
    '''
    ###
    meta_title = f'''Tincture Dosage Safety Cheatsheet | TerraWhisper Shop'''
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


