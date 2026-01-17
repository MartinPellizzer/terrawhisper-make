from lib import g
from lib import io
from lib import llm
from lib import utils
from lib import components
from lib import sections

preparation_list = io.csv_to_dict(f'{g.database_folderpath}/csv/preparations.csv')

def hub_preparations_preparation_gen():
    for preparation_i, preparation in enumerate(preparation_list):
        preparation_slug = preparation['preparation_slug']
        preparation_name_singular = preparation['preparation_name_singular']
        preparation_name_plural = preparation['preparation_name_plural']
        print(f'PREPARATION: {preparation_slug}')
        url_slug = f'preparations/{preparation_slug}'
        ################################################################################ 
        ### json
        ################################################################################ 
        ### json init
        json_article_filepath = f'''{g.database_folderpath}/json/{url_slug}.json'''
        json_article = io.json_read(json_article_filepath, create=True)
        json_article['url'] = url_slug
        json_article['preparation_slug'] = preparation_slug
        json_article['preparation_name_singular'] = preparation_name_singular
        json_article['preparation_name_plural'] = preparation_name_plural
        json_article['title'] = f'''What to know about medicinal herbal {preparation_name_plural}'''
        io.json_write(json_article_filepath, json_article)
        ### json intro
        regen = False
        dispel = False
        key = 'intro'
        if key not in json_article: json_article[key] = ''
        if regen: json_article[key] = ''
        if dispel: 
            json_article[key] = ''
            io.json_write(json_article_filepath, json_article)
            return
        if json_article[key] == '':
            prompt = f'''
                Write a detailed paragraph in 5 sentences about medicinal herbal {preparation_name_plural}.
                Include what is a {preparation_name_singular}.
                Include brief history or tradition of its use.
                Include why people choose this preparation method over others.
                Start with the following words: A medicinal herbal {preparation_name_singular} is .
            '''
            prompt += f'/no_think'
            reply = llm.reply(prompt).strip()
            if '</think>' in reply:
                reply = reply.split('</think>')[1].strip()
            json_article[key] = reply
            io.json_write(json_article_filepath, json_article)
        ### json benefits
        regen = False
        dispel = False
        key = 'benefits'
        if key not in json_article: json_article[key] = ''
        if regen: json_article[key] = ''
        if dispel: 
            json_article[key] = ''
            io.json_write(json_article_filepath, json_article)
            return
        if json_article[key] == '':
            prompt = f'''
                Write a detailed paragraph in 5 sentences about the purpose and benefits of medicinal herbal {preparation_name_plural}.
                Include what this preparation is typically used for.
                Include the key advantages (e.g., shelf life, potency, ease of use).
                Include which kinds of herbs work best in this form.
                Start with the following words: This preparation is typically used for .
            '''
            prompt += f'/no_think'
            reply = llm.reply(prompt).strip()
            if '</think>' in reply:
                reply = reply.split('</think>')[1].strip()
            json_article[key] = reply
            io.json_write(json_article_filepath, json_article)
        ### json how works
        regen = False
        dispel = False
        key = 'how_works'
        if key not in json_article: json_article[key] = ''
        if regen: json_article[key] = ''
        if dispel: 
            json_article[key] = ''
            io.json_write(json_article_filepath, json_article)
            return
        if json_article[key] == '':
            prompt = f'''
                Write a detailed paragraph in 5 sentences about how work medicinal herbal {preparation_name_plural}.
                Include a short explanation of how this preparaiton extracts, preserves, or delivers herbal properties.
                Include any relevant science or traditional reasoning.
            '''
            prompt += f'/no_think'
            reply = llm.reply(prompt).strip()
            if '</think>' in reply:
                reply = reply.split('</think>')[1].strip()
            json_article[key] = reply
            io.json_write(json_article_filepath, json_article)
        ### json ingredients
        regen = False
        dispel = False
        key = 'ingredients'
        if key not in json_article: json_article[key] = ''
        if regen: json_article[key] = ''
        if dispel: 
            json_article[key] = ''
            io.json_write(json_article_filepath, json_article)
            return
        if json_article[key] == '':
            prompt = f'''
                Write a detailed paragraph in 5 sentences about the ingredients and tools needed for medicinal herbal {preparation_name_plural}.
                Include list of common ingredients (base liquids, oils, waxes, alcohol, etc.).
                Include of basic tools or equipment (jars, strainers, pots, spoons, etc.).
            '''
            prompt += f'/no_think'
            reply = llm.reply(prompt).strip()
            if '</think>' in reply:
                reply = reply.split('</think>')[1].strip()
            json_article[key] = reply
            io.json_write(json_article_filepath, json_article)
        ### json instructions
        regen = False
        dispel = False
        key = 'instructions'
        if key not in json_article: json_article[key] = ''
        if regen: json_article[key] = ''
        if dispel: 
            json_article[key] = ''
            io.json_write(json_article_filepath, json_article)
            return
        if json_article[key] == '':
            prompt = f'''
                Write a detailed paragraph in 5 sentences about the step-by-step instructions to make medicinal herbal {preparation_name_plural}.
                Include clear instructions on how to make this preparation at home.
                Include optional varations (strong vs. mild, quick vs. long infusion, etc.).
            '''
            prompt += f'/no_think'
            reply = llm.reply(prompt).strip()
            if '</think>' in reply:
                reply = reply.split('</think>')[1].strip()
            json_article[key] = reply
            io.json_write(json_article_filepath, json_article)
        ### json how to use
        regen = False
        dispel = False
        key = 'how_use'
        if key not in json_article: json_article[key] = ''
        if regen: json_article[key] = ''
        if dispel: 
            json_article[key] = ''
            io.json_write(json_article_filepath, json_article)
            return
        if json_article[key] == '':
            prompt = f'''
                Write a detailed paragraph in 5 sentences about how to use medicinal herbal {preparation_name_plural}.
                Include typical dosage or application method.
                Include how often to take/apply.
                Include common pairings with other preparations (e.g., teas + tinctures).
            '''
            prompt += f'/no_think'
            reply = llm.reply(prompt).strip()
            if '</think>' in reply:
                reply = reply.split('</think>')[1].strip()
            json_article[key] = reply
            io.json_write(json_article_filepath, json_article)
        ### json storage
        regen = False
        dispel = False
        key = 'storage'
        if key not in json_article: json_article[key] = ''
        if regen: json_article[key] = ''
        if dispel: 
            json_article[key] = ''
            io.json_write(json_article_filepath, json_article)
            return
        if json_article[key] == '':
            prompt = f'''
                Write a detailed paragraph in 5 sentences about how to store medicinal herbal {preparation_name_plural}.
                Include best ways to store it (e.g., dark glass bottles, refrigeration).
                Include how long it lasts before losing potency or spoiling.
            '''
            prompt += f'/no_think'
            reply = llm.reply(prompt).strip()
            if '</think>' in reply:
                reply = reply.split('</think>')[1].strip()
            json_article[key] = reply
            io.json_write(json_article_filepath, json_article)
        ### json safety
        regen = False
        dispel = False
        key = 'safety'
        if key not in json_article: json_article[key] = ''
        if regen: json_article[key] = ''
        if dispel: 
            json_article[key] = ''
            io.json_write(json_article_filepath, json_article)
            return
        if json_article[key] == '':
            prompt = f'''
                Write a detailed paragraph in 5 sentences about safety and considerations medicinal herbal {preparation_name_plural}.
                Include possible contraindications (pregnancy, medications, allergies).
                Include which herbs to avoid in this form.
                Include tips for safe use.
            '''
            prompt += f'/no_think'
            reply = llm.reply(prompt).strip()
            if '</think>' in reply:
                reply = reply.split('</think>')[1].strip()
            json_article[key] = reply
            io.json_write(json_article_filepath, json_article)
        ### json faq
        regen = False
        dispel = False
        key = 'faq'
        if key not in json_article: json_article[key] = ''
        if regen: json_article[key] = ''
        if dispel: 
            json_article[key] = ''
            io.json_write(json_article_filepath, json_article)
            return
        if json_article[key] == '':
            prompt = f'''
                Write a detailed paragraph in 5 sentences about frequently asked question on medicinal herbal {preparation_name_plural}.
                Include "can i substitute ingredients?"
                Include "how long before i notice effects?"
                Include "is it safe for children/elderly?"
            '''
            prompt += f'/no_think'
            reply = llm.reply(prompt).strip()
            if '</think>' in reply:
                reply = reply.split('</think>')[1].strip()
            json_article[key] = reply
            io.json_write(json_article_filepath, json_article)
        ### html
        html_article = ''
        json_title = f'''{json_article['title']}'''
        meta_title = f'''{json_title}'''
        meta_description = f''
        html_article += f'''<h1>{json_title.title()}</h1>'''
        src = f'''/images/preparations/herbal-{json_article['preparation_slug']}.jpg'''
        alt = f'''herbal {json_article['preparation_name_plural']}'''
        html_article += f'''<img src="{src}" alt="{alt}">'''
        html_article += f'''{utils.format_1N1(json_article['intro'])}'''
        ### lead magnet
        form_head = ''
        if preparation_slug == 'tinctures':
            with open(f'{g.assets_folderpath}/scripts/newsletter/form-head.txt') as f: 
                form_head = f.read()
            with open(f'{g.assets_folderpath}/scripts/newsletter/form-course-preparation-tincture.txt') as f: 
                form_body = f.read()
            html_article += f'''
                <div class="free-gift">
                    <p class="free-gift-heading">FREE COURSE</p>
                    <p style="text-align: center; margin-bottom: 1.6rem;">How to make medicinal herbal tinctures for common ailments at home and in a weekend (using the Healing Drops System).</p>
                    <img src="/images/shop/banner-course-preparation-tincture.jpg" alt="tincture preparation course banner">
                </div>
            '''
                    # {form_body}
        ### toc
        html_article += f'''[toc]'''
        html_article += f'''<h2>Purpose and Benefits</h2>'''
        html_article += f'''{utils.format_1N1(json_article['benefits'])}'''
        html_article += f'''<h2>How It Works</h2>'''
        html_article += f'''{utils.format_1N1(json_article['how_works'])}'''
        html_article += f'''<h2>Ingredients and Tools Needed</h2>'''
        html_article += f'''{utils.format_1N1(json_article['ingredients'])}'''
        html_article += f'''<h2>Step-by-Step Instructions</h2>'''
        html_article += f'''{utils.format_1N1(json_article['instructions'])}'''
        html_article += f'''<h2>How to Use</h2>'''
        html_article += f'''{utils.format_1N1(json_article['how_use'])}'''
        html_article += f'''<h2>Storage and Shelf Life</h2>'''
        html_article += f'''{utils.format_1N1(json_article['storage'])}'''
        html_article += f'''<h2>Safety and Considerations</h2>'''
        html_article += f'''{utils.format_1N1(json_article['safety'])}'''
        html_article += f'''<h2>What are the best medicinal herbal {json_article['preparation_name_plural']}?</h2>'''
        html_article += f'''{utils.format_1N1(json_article['best'])}'''
        html_article += f'''<p>Check the following link for a full list of the <a href="/{json_article['url']}/best.html">100 best medicinal herbal {json_article['preparation_name_plural']}</a>.</p>'''
        html_article += f'''<h2>Frequently Asked Questions (FAQ)</h2>'''
        html_article += f'''{utils.format_1N1(json_article['faq'])}'''
        html_article = sections.toc(html_article)
        html = f'''
            <!DOCTYPE html>
            <html lang="en">
            {components.html_head(meta_title, meta_description)}
            <body>
                {sections.header()}
                {sections.breadcrumbs(url_slug)}
                <main class="container-md article">
                    {html_article}
                </main>
                <div class="mt-64"></div>
                {sections.footer()}
            </body>
            </html>
        '''
        html_filepath = f'''{g.website_folderpath}/{url_slug}.html'''
        with open(html_filepath, 'w') as f: f.write(html)

def preparations_gen():
    url_slug = f'preparations'
    html_filepath = f'''{g.website_folderpath}/{url_slug}.html'''
    html_main = f''
    for preparation_i, preparation in enumerate(preparation_list):
        print(preparation)
    ###
    ### category herbs popular
    html_popular_grid = f''
    popular_num = 100
    for preparation_i, preparation in enumerate(preparation_list[:popular_num]):
        print(f'PREPARATION: {preparation_i}/{len(preparation_list[:popular_num])} - {preparation}')
        preparation_name_plural = preparation['preparation_name_plural']
        preparation_slug = preparation['preparation_slug']
        src = f'''/images/preparations/herbal-{preparation_slug}.jpg'''
        alt = f'''herbal {preparation_name_plural}'''
        html_popular_grid += f'''
            <div class="card-default">
                <a href="/{url_slug}/{preparation_slug}.html">
                    <img src="{src}" alt="{alt}" style="margin-bottom: 0.8rem;">
                    <h3 style="margin-bottom: 0.8rem;">{preparation_name_plural.title()}</h3>
                </a>
            </div>
        '''
    html_popular = f'''
        <div style="margin-bottom: 9.6rem;">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <h2 style="font-size: 4.8rem; line-height: 1; margin-bottom: 3.2rem;">Popular</h2>
                <p><a href="/herbs/popular.html">View All</a></p>
            </div>
            <div class="grid-4" style="gap: 3.2rem;">
                {html_popular_grid}
            </div>
        </div>
    '''
    html_h1 = f'<h1 style="margin-bottom: 9.6rem;">Herbal Preparations For Natural Healing</h1>'
    html_main += f'''
        <div>
            {html_popular}
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
            {sections.breadcrumbs(url_slug)}
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
    print(html_filepath)

def gen():
    preparations_gen()
    # hub_preparations_preparation_gen()

