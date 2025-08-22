from lib import g
from lib import io
from lib import components
from lib import sections

def gen():
    url = f'shop/herb-drying-checklist/download'
    obj = {
        'url': url,
    }
    html_main = f''
    img_src = '/images/shop/herb-drying-checklist.jpg'
    img_alt = 'herb drying checklist'
    html_main = f'''
        <div class='product'>
            <h1 style="text-align: center; margin-bottom: 1.6rem;">Herb Drying Checklist Download</h1>
            <div class="container-sm" style="margin-bottom: 1.6rem;">
                <img src="{img_src}" alt="{img_alt}">
            </div>
            <div style="text-align: center; margin-bottom: 1.6rem;">
                <a class="button-default" href="/assets/shop/herb-drying-checklist.pdf">DOWNLOAD CHECKLIST (HD)</a>
            </div>
        </div>
    '''
    ###
    meta_title = f'''Herb Drying Checklist Download | TerraWhisper Shop'''
    meta_description = f''''''
    html = f'''
        <!DOCTYPE html>
        <html lang="en">
        {components.html_head(meta_title, meta_description)}
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


