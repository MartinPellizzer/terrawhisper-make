from lib import g
from lib import io
from lib import components
from lib import sections

def gen():
    url = f'ailments'
    obj = {
        'url': url,
    }
    html_main = f''
    html_ailments = f''
    ailment_list = io.csv_to_dict(f'{g.database_folderpath}/csv/ailments.csv')
    for ailment_i, ailment in enumerate(ailment_list):
        ailment_slug = ailment['ailment_slug']
        ailment_name = ailment['ailment_name']
        print(f'AILMENT: {ailment_i}/{len(ailment_list)} - {ailment_name}')
        src = f'''/images/ailments/{ailment_slug}-herbs.jpg'''
        alt = f'''{ailment_name} herbs'''
        html_ailments += f'''
            <div class="card-default">
                <a href="/{url}/{ailment_slug}.html">
                    <img src="{src}" alt="{alt}">
                    <h2>{ailment_name.title()}</h2>
                </a>
            </div>
        '''
        html_ailments += f''''''
    html_main += f'''
        <div class="grid-3" style="gap: 3.2rem;">
            {html_ailments}
        </div>
    '''
    meta_title = f'''Ailments'''
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

