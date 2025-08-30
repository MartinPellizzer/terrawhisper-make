import markdown

from lib import g
from lib import components
from lib import sections
from lib import polish

def gen():
    url_relative = f'uses/skin-care'
    with open(f'{g.database_folderpath}/articles/{url_relative}.md', encoding='utf-8') as f: 
        markdown_content = f.read()
    markdown_content = polish.to_ascii(markdown_content)
    html_article = markdown.markdown(markdown_content)
    meta_title = f''
    meta_description = f''
    for line in markdown_content.split('\n'):
        line = line.strip()
        if line.startswith('# '):
            line = line.replace('# ', '')
            meta_title = line
    html = f'''
        <!DOCTYPE html>
        <html lang="en">
        {components.html_head(meta_title, meta_description)}
        <body>
            {sections.header()}
            {sections.breadcrumbs(url_relative)}
            <main class="container-md article-markdown">
                {html_article}
            </main>
            <div class="spacer"></div>
            {sections.footer()}
        </body>
        </html>
    '''
    with open(f'{g.website_folderpath}/{url_relative}.html', 'w') as f: f.write(html)

