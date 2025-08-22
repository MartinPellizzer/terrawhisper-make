def html_head(meta_title, meta_description, form_head=''):
    html = f'''
        <head>
            <link rel="stylesheet" href="/style.css">
            {form_head}
        </head>
    '''
    return html

