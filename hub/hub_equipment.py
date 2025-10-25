from lib import g
from lib import io
from lib import llm
from lib import utils
from lib import components
from lib import sections

def hub_equipments_equipment_gen():
    equipments = io.csv_to_dict(f'{g.DATABASE_FOLDERPATH}/csv/equipment.csv')
    for equipment_i, equipment in enumerate(equipments):
        equipment_slug = equipment['supply_slug']
        equipment_name_amazon = equipment['supply_name_amazon']
        equipment_name_singular = equipment['supply_name_singular']
        equipment_name_plural = equipment['supply_name_plural']
        print(f'EQUIPMENT: {equipment_i}/{len(equipments)} - {equipment_name_singular}')
        equipment_image_src = ''
        equipment_image_alt = ''

        ######################################## 
        ### json
        ######################################## 
        url_slug = f'equipment/{equipment_slug}'

        ### json init
        json_article_filepath = f'''{g.DATABASE_FOLDERPATH}/json/{url_slug}.json'''
        json_article = io.json_read(json_article_filepath, create=True)
        json_article['url'] = url_slug
        json_article['equipment_slug'] = equipment_slug
        json_article['equipment_name_amazon'] = equipment_name_amazon
        json_article['equipment_name_singular'] = equipment_name_singular
        json_article['equipment_name_plural'] = equipment_name_plural
        json_article['title'] = f'''{equipment_name_plural} for herbalists'''.title()
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
                Write a detailed paragraph in 5 sentences about the following equipment for herbalism: {equipment_name_plural}.
                Briefly explain what the tool is and why it's essential for herbalists.
                Mention who it's for (e.g., beginners, home herbalists, small-batch makers, etc.).
                Promise what the readers will learn (uses, how-to, tips, care).
                Start with the following words: {equipment_name_plural.capitalize()} are .
            '''
            prompt += f'/no_think'
            reply = llm.reply(prompt).strip()
            if '</think>' in reply:
                reply = reply.split('</think>')[1].strip()
            json_article[key] = reply
            io.json_write(json_article_filepath, json_article)

        ######################################## 
        ### html
        ######################################## 
        html_article = ''
        meta_title = f'''{json_article['title']}'''
        meta_description = f''
        form_head = ''

        html_article += f'''<h1>{json_article['title']}</h1>'''
        html_article += f'''{utils.format_1N1(json_article['intro'])}'''

        html = f'''
            <!DOCTYPE html>
            <html lang="en">
            {components.html_head(meta_title, meta_description, form_head)}
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
def hub_equipments_gen():
    hub_equipments_equipment_gen()
    ###
    equipments = io.csv_to_dict(f'{g.DATABASE_FOLDERPATH}/csv/equipment.csv')
    url_slug = f'equipment'
    meta_title = f'''Equipment For Herbalists | TerraWhisper'''
    meta_description = f''
    form_head = f''
    html_main = f''
    html_equipment = f''
    for equipment_i, equipment in enumerate(equipments):
        equipment_slug = equipment['supply_slug']
        equipment_name_amazon = equipment['supply_name_amazon']
        equipment_name_singular = equipment['supply_name_singular']
        equipment_name_plural = equipment['supply_name_plural']
        print(f'EQUIPMENT: {equipment_i}/{len(equipments)} - {equipment_name_singular}')
        equipment_image_src = ''
        equipment_image_alt = ''
        html_equipment += f'''
            <div class="card-default">
                <a href="/{url_slug}/{equipment_slug}.html">
                    <img src="{equipment_image_src}" alt="{equipment_image_alt}">
                    <h2>{equipment_name_singular.title()}</h2>
                </a>
            </div>
        '''
    html_main += f'''
        <div class="grid-3" style="gap: 3.2rem;">
            {html_equipment}
        </div>
    '''
    html = f'''
        <!DOCTYPE html>
        <html lang="en">
        {components.html_head(meta_title, meta_description, form_head)}
        <body>
            {sections.header()}
            {sections.breadcrumbs(url_slug)}
            <main class="container-md article">
                {html_main}
            </main>
            <div class="mt-64"></div>
            {sections.footer()}
        </body>
        </html>
    '''
    html_filepath = f'''{g.website_folderpath}/{url_slug}.html'''
    with open(html_filepath, 'w') as f: f.write(html)

def main():
    hub_equipments_gen()
