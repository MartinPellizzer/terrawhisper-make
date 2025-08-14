from lib import g
from lib import io
from lib import components
from lib import sections

def gen():
    html_main = f''
    meta_title = f'''TerraWhisper'''
    meta_description = f''''''
    html = f'''
        <!DOCTYPE html>
        <html lang="en">
        {components.html_head(meta_title, meta_description)}
        <body>
            {sections.header()}
            <div class="spacer"></div>
            <main class="container-xl">
            </main>
            <div class="spacer"></div>
            {sections.footer()}
        </body>
        </html>
    '''
    html_filepath = f'''{g.website_folderpath}/index.html'''
    with open(html_filepath, 'w') as f: f.write(html)

