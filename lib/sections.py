def header():
    html = f'''
        <header>
            <nav class="container-xl">
                <a href='/'>TerraWhisper</a>
                <ul>
                    <li><a href='/herbs.html'>Herbs</a></li>
                    <li><a href='/preparations.html'>Preparations</a></li>
                    <li><a href='/ailments.html'>Ailments</a></li>
                    <li><a href='/shop.html'>Shop</a></li>
                </ul>
            </nav>
        </header>
    '''
    return html

def footer():
    html = f'''
        <footer>
            <div class="container-xl">
                <span>Copyright TerraWhisper | All rights reserved</span>
            </div>
        </footer>
    '''
    return html

def breadcrumbs(url):
    breadcrumb_list = url.split('/')
    breadcrumb_href = f'/'
    breadcrumb_html = f'<a href="{breadcrumb_href}">Home</a>'
    for breadcrumb_i, breadcrumb_text in enumerate(breadcrumb_list):
        breadcrumb_href += '/' + breadcrumb_text
        breadcrumb_href = breadcrumb_href.replace('//', '/')
        breadcrumb_text = breadcrumb_text.strip().replace('-', ' ').title()
        if breadcrumb_i == len(breadcrumb_list)-1:
            breadcrumb_html += f' > {breadcrumb_text}'
        else:
            breadcrumb_html += f' > <a href="{breadcrumb_href}.html">{breadcrumb_text}</a>'
    html = f'''
        <section class="breadcrumbs">
            <div class="container-xl">
                {breadcrumb_html}
            </div>
        </section>
    '''
    return html

def toc(html_article):
    from bs4 import BeautifulSoup
    ### get headers
    soup = BeautifulSoup(html_article, 'html.parser')
    headings = soup.find_all([f'h{i}' for i in range(1,7)])
    ### add ids to headings
    for idx, heading in enumerate(headings):
        heading['id'] = f'{idx}'
    html_article = str(soup)
    ### gen toc data
    toc_items = []
    for i, heading in enumerate(headings):
        level = int(heading.name[1])
        level -= 1 # start from h2
        if level == 0: continue
        toc_items.append((level, heading.get_text(), heading['id']))
    ### build nested toc as <ul>
    toc_html = ''
    toc_html += '<div class="toc">\n'
    toc_html += f'''<p class="toc-heading">Table of Contents</p>\n'''
    toc_html += '<ul>\n'
    prev_level = 1
    for level, text, id_attr in toc_items:
        if level > prev_level:
            toc_html += '<ul>\n' * (level - prev_level)
        elif level < prev_level:
            toc_html += '<ul>\n' * (prev_level - level)
        toc_html += f'<li><a href="#{id_attr}">{text}</a></li>\n'
        prev_level = level
    toc_html += '</ul>\n'
    toc_html += '</div>\n'
    ### insert toc in html article
    html_article = html_article.replace('[toc]', toc_html)
    return html_article
