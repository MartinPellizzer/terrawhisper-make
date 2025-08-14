from lib import g
from lib import io
from lib import data
from lib import polish
from lib import components
from lib import sections

def gen():
    url = f'herbs'
    obj = {
        'url': url,
    }
    html_filepath = f'''{g.website_folderpath}/{obj['url']}.html'''
    html_main = f''
    html_herbs = f''
    herbs = data.herbs_medicinal_get()
    for herb_i, herb in enumerate(herbs):
        print(f'HERB: {herb_i}/{len(herbs)} - {herb}')
        herb_name_scientific = herb['herb_name_scientific']
        herb_slug = polish.sluggify(herb_name_scientific)
        src = f'''/images/herbs/{herb_slug}.jpg'''
        alt = f'''{herb_name_scientific}'''
        html_herbs += f'''
            <div class="card-default">
                <a href="/{url}/{herb_slug}.html">
                    <img src="{src}" alt="{alt}">
                    <h2>{herb_name_scientific.title()}</h2>
                </a>
            </div>
        '''
    html_main += f'''
        <div class="grid-3" style="gap: 3.2rem;">
            {html_herbs}
        </div>
    '''
    meta_title = f'''Herbs'''
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
    with open(html_filepath, 'w') as f: f.write(html)
    # image_pil(obj)


