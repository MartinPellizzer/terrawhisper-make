from lib import g
from lib import io
from lib import components
from lib import sections

def gen():
    url = f'preparations'
    obj = {
        'url': url,
    }
    html_main = f''
    html_preparations = f''
    preparation_list = io.csv_to_dict(f'{g.database_folderpath}/csv/preparations.csv')
    for preparation_i, preparation in enumerate(preparation_list):
        preparation_slug = preparation['preparation_slug']
        preparation_name_singular = preparation['preparation_name_singular']
        preparation_name_plural = preparation['preparation_name_plural']
        print(f'AILMENT: {preparation_i}/{len(preparation_list)} - {preparation_name_plural}')
        src = f'''/images/preparations/herbal-{preparation_slug}.jpg'''
        alt = f'''herbal-{preparation_name_singular}'''
                    # <img src="{src}" alt="{alt}">
        html_preparations += f'''
            <div class="card-default">
                <a href="/{url}/{preparation_slug}.html">
                    <h2 style="margin-bottom: 1.6rem;">{preparation_name_plural.title()}</h2>
                    <img src="{src}" alt="{alt}">
                </a>
            </div>
        '''
        html_preparations += f''''''
    html_main += f'''
        <div class="grid-3" style="gap: 3.2rem;">
            {html_preparations}
        </div>
    '''
    meta_title = f'''Preparations'''
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
    html_filepath = f'''{g.website_folderpath}/{obj['url']}.html'''
    with open(html_filepath, 'w') as f: f.write(html)
    # image_pil(obj)

