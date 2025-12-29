import os

from lib import g
from lib import io
from lib import data
from lib import components
from lib import sections

def ailments_systems_gen():
    url_slug = 'ailments/systems'
    ###
    ailments = io.csv_to_dict(f'{g.DATABASE_FOLDERPATH}/csv/ailments.csv')
    clusters = data.systems_ailments_get()
    html_clusters = f''
    for cluster in clusters:
        cluster_slug = cluster['system_slug']
        cluster_name = cluster['system_slug']
        html_ailments = f''
        ailments_num = 4
        for ailment_i, ailment in enumerate(cluster['ailments'][:ailments_num]):
            ailment_slug = ailment['ailment_slug']
            ailment_name = ailment['ailment_name']
            print(f'AILMENT: {ailment_i}/{len(ailments)} - {ailment_name}')
            src = f'''/images/ailments/{ailment_slug}.jpg'''
            alt = f'''{ailment_name}'''
            html_ailments += f'''
                <div class="card-default">
                    <a href="/{url_slug}/{ailment_slug}.html">
                        <img src="{src}" alt="{alt}" style="margin-bottom: 0.8rem;">
                        <h3 style="margin-bottom: 0.8rem;">{ailment_name.title()}</h3>
                    </a>
                </div>
            '''
        html_clusters += f'''
            <div style="margin-bottom: 9.6rem;">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <h2 style="font-size: 4.8rem; line-height: 1; margin-bottom: 3.2rem;">{cluster_name.title()}</h2>
                    <a style="color: #111111; text-decoration: none;" href="/ailments/systems/{cluster_slug}.html">View All >></a>
                </div>
                <div class="grid-4" style="gap: 3.2rem;">
                    {html_ailments}
                </div>
            </div>
        '''
    html_main = f'''
        <h1 style="font-size: 6.4rem; line-height: 1; margin-bottom: 9.6rem;">Common Ailments and Their Herbal Remedies</h1>
        {html_clusters}
    '''
    meta_title = f'''Ailments'''
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
    html_filepath = f'''{g.website_folderpath}/{url_slug}.html'''
    with open(html_filepath, 'w') as f: f.write(html)

def ailments_systems_system_gen():
    ailments = io.csv_to_dict(f'{g.DATABASE_FOLDERPATH}/csv/ailments.csv')
    ### cluster by system
    clusters = data.systems_ailments_get()
    for cluster in clusters:
        system_name = cluster['system_slug']
        system_slug = system_name.strip().lower().replace(' ', '-')
        url_slug = f'ailments/systems/{system_slug}'
        html_ailments = f''
        for ailment_i, ailment in enumerate(cluster['ailments']):
            ailment_slug = ailment['ailment_slug']
            ailment_name = ailment['ailment_name']
            print(f'AILMENT: {ailment_i}/{len(ailments)} - {ailment_name}')
            src = f'''/images/ailments/{ailment_slug}.jpg'''
            alt = f'''{ailment_name} herbs'''
            html_ailments += f'''
                <div class="card-default">
                    <a href="/ailments/{ailment_slug}.html">
                        <img src="{src}" alt="{alt}" style="margin-bottom: 0.8rem;">
                        <h3 style="margin-bottom: 0.8rem;">{ailment_name.title()}</h3>
                    </a>
                </div>
            '''
        html_main = f'''
            <h1 style="font-size: 6.4rem; line-height: 1; margin-bottom: 9.6rem;">Common Ailments and Their Herbal Remedies</h1>
            <div style="margin-bottom: 9.6rem;">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <h2 style="font-size: 4.8rem; line-height: 1; margin-bottom: 3.2rem;">{system_name.title()}</h2>
                </div>
                <div class="grid-4" style="gap: 3.2rem;">
                    {html_ailments}
                </div>
            </div>
        '''
        meta_title = f'''{system_name.title()} Ailments'''
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
        try: os.mkdir(f'{g.website_folderpath}/ailments/systems')
        except: pass
        html_filepath = f'''{g.website_folderpath}/{url_slug}.html'''
        with open(html_filepath, 'w') as f: f.write(html)

def ailments_organs_organ_gen():
    ailments = io.csv_to_dict(f'{g.DATABASE_FOLDERPATH}/csv/ailments.csv')
    ### cluster by organ
    clusters = data.ailments_by_organ_get()
    for cluster in clusters:
        organ_name = cluster['organ_slug']
        organ_slug = organ_name.strip().lower().replace(' ', '-')
        url_slug = f'ailments/organs/{organ_slug}'
        html_ailments = f''
        for ailment_i, ailment in enumerate(cluster['ailments']):
            ailment_slug = ailment['ailment_slug']
            ailment_name = ailment['ailment_name']
            print(f'AILMENT: {ailment_i}/{len(ailments)} - {ailment_name}')
            src = f'''/images/ailments/{ailment_slug}-herbs.jpg'''
            alt = f'''{ailment_name} herbs'''
            html_ailments += f'''
                <div class="card-default">
                    <a href="/ailments/{ailment_slug}.html">
                        <img src="{src}" alt="{alt}">
                        <h2>{ailment_name.title()}</h2>
                    </a>
                </div>
            '''
        html_main = f'''
            <h1 style="font-size: 6.4rem; line-height: 1; margin-bottom: 9.6rem;">Common Ailments and Their Herbal Remedies</h1>
            <div style="margin-bottom: 9.6rem;">
                <h2 style="font-size: 4.8rem; line-height: 1; padding-bottom: 1.6rem; margin-bottom: 1.6rem; border-bottom: 1px solid #333333;">{organ_name.title()}</h2>
                <div class="grid-3" style="gap: 3.2rem;">
                    {html_ailments}
                </div>
            </div>
        '''
        meta_title = f'''{organ_name.title()} Ailments'''
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
        try: os.mkdir(f'{g.website_folderpath}/ailments/organs')
        except: pass
        html_filepath = f'''{g.website_folderpath}/{url_slug}.html'''
        with open(html_filepath, 'w') as f: f.write(html)

def ailments_organs_gen():
    ailments_organs_organ_gen()
    ###
    ailments = io.csv_to_dict(f'{g.DATABASE_FOLDERPATH}/csv/ailments.csv')
    url_slug = 'ailments/organs'
    ### cluster by organ
    clusters = data.ailments_by_organ_get()
    html_clusters = f''
    for cluster in clusters:
        cluster_name = cluster['organ_slug']
        html_ailments = f''
        for ailment_i, ailment in enumerate(cluster['ailments']):
            ailment_slug = ailment['ailment_slug']
            ailment_name = ailment['ailment_name']
            print(f'AILMENT: {ailment_i}/{len(ailments)} - {ailment_name}')
            src = f'''/images/ailments/{ailment_slug}-herbs.jpg'''
            alt = f'''{ailment_name} herbs'''
            html_ailments += f'''
                <div class="card-default">
                    <a href="/ailments/{ailment_slug}.html">
                        <img src="{src}" alt="{alt}">
                        <h2>{ailment_name.title()}</h2>
                    </a>
                </div>
            '''
        html_clusters += f'''
            <div style="margin-bottom: 9.6rem;">
                <h2 style="font-size: 4.8rem; line-height: 1; padding-bottom: 1.6rem; margin-bottom: 1.6rem; border-bottom: 1px solid #333333;">{cluster_name.title()}</h2>
                <div class="grid-3" style="gap: 3.2rem;">
                    {html_ailments}
                </div>
            </div>
        '''
    html_main = f'''
        <h1 style="font-size: 6.4rem; line-height: 1; margin-bottom: 9.6rem;">Common Ailments and Their Herbal Remedies</h1>
        {html_clusters}
    '''
    meta_title = f'''Ailments'''
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
    html_filepath = f'''{g.website_folderpath}/{url_slug}.html'''
    with open(html_filepath, 'w') as f: f.write(html)

def ailments_gen():
    url_slug = 'ailments'
    ### ailments
    ailments = io.csv_to_dict(f'{g.DATABASE_FOLDERPATH}/csv/ailments.csv')
    ailments_num = 4
    html_ailments_cards = f''
    for ailment in ailments[:ailments_num]:
        ailment_slug = ailment['ailment_slug']
        ailment_name = ailment['ailment_name']
        src = f'''/images/ailments/{ailment_slug}.jpg'''
        alt = f'''{ailment_name} remedies'''
        html_ailments_cards += f'''
            <div class="card-default">
                <a href="/{url_slug}/{ailment_slug}.html">
                    <img src="{src}" alt="{alt}" style="margin-bottom: 0.8rem;">
                    <h3 style="margin-bottom: 0.8rem;">{ailment_name.title()}</h3>
                </a>
            </div>
        '''
    html_ailments = f'''
        <div style="margin-bottom: 9.6rem;">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <h2 style="font-size: 4.8rem; line-height: 1; margin-bottom: 3.2rem;">All</h2>
                <a style="color: #111111; text-decoration: none;" href="/ailments/all.html">View All >></a>
            </div>
            <div class="grid-4" style="gap: 3.2rem;">
                {html_ailments_cards}
            </div>
        </div>
    '''
    ### systems
    clusters = data.systems_ailments_get()
    clusters_num = 4
    html_systems_cards = f''
    for cluster in clusters[:clusters_num]:
        system_slug = cluster['system_slug']
        ailment = cluster['ailments'][0]
        ailment_slug = ailment['ailment_slug']
        ailment_name = ailment['ailment_name']
        src = f'''/images/systems/{system_slug}.jpg'''
        alt = f'''{ailment_name} remedies'''
        html_systems_cards += f'''
            <div class="card-default">
                <a href="/{url_slug}/systems/{system_slug}.html">
                    <img src="{src}" alt="{alt}" style="margin-bottom: 0.8rem;">
                    <h3 style="margin-bottom: 0.8rem;">{system_slug.title()}</h3>
                </a>
            </div>
        '''
    html_systems = f'''
        <div style="margin-bottom: 9.6rem;">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <h2 style="font-size: 4.8rem; line-height: 1; margin-bottom: 3.2rem;">Body Systems</h2>
                <a style="color: #111111; text-decoration: none;" href="/ailments/systems.html">View All >></a>
            </div>
            <div class="grid-4" style="gap: 3.2rem;">
                {html_systems_cards}
            </div>
        </div>
    '''
    ### organs
    clusters = data.ailments_by_organ_get()
    cluster_num = 4
    html_organs_cards = f''
    for cluster in clusters[:cluster_num]:
        organ_name = cluster['organ_slug']
        organ_slug = organ_name.strip().lower().replace(' ', '-')
        ailment = cluster['ailments'][0]
        ailment_slug = ailment['ailment_slug']
        ailment_name = ailment['ailment_name']
        src = f'''/images/organs/{organ_slug}.jpg'''
        alt = f'''{ailment_name} remedies'''
        html_organs_cards += f'''
            <div class="card-default">
                <a href="/{url_slug}/organs/{organ_slug}.html">
                    <img src="{src}" alt="{alt}" style="margin-bottom: 0.8rem;">
                    <h3 style="margin-bottom: 0.8rem;">{organ_name.title()}</h3>
                </a>
            </div>
        '''
    html_organs = f'''
        <div style="margin-bottom: 9.6rem;">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <h2 style="font-size: 4.8rem; line-height: 1; margin-bottom: 3.2rem;">Body Organs</h2>
                <a style="color: #111111; text-decoration: none;" href="/ailments/organs.html">View All >></a>
            </div>
            <div class="grid-4" style="gap: 3.2rem;">
                {html_organs_cards}
            </div>
        </div>
    '''
    html_main = f'''
        <h1 style="font-size: 6.4rem; line-height: 1; margin-bottom: 9.6rem;">Common Ailments and Their Herbal Remedies</h1>
        {html_ailments}
        {html_systems}
        {html_organs}
    '''
    meta_title = f'''Ailments'''
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
    html_filepath = f'''{g.website_folderpath}/{url_slug}.html'''
    with open(html_filepath, 'w') as f: f.write(html)

def ailments_all_gen():
    url_slug = 'ailments/all'
    ailments = io.csv_to_dict(f'{g.DATABASE_FOLDERPATH}/csv/ailments.csv')
    html_ailments_cards = f''
    for ailment in ailments:
        ailment_slug = ailment['ailment_slug']
        ailment_name = ailment['ailment_name']
        src = f'''/images/ailments/{ailment_slug}.jpg'''
        alt = f'''{ailment_name} remedies'''
        html_ailments_cards += f'''
            <div class="card-default">
                <a href="/{url_slug}/{ailment_slug}.html">
                    <img src="{src}" alt="{alt}" style="margin-bottom: 0.8rem;">
                    <h3 style="margin-bottom: 0.8rem;">{ailment_name.title()}</h3>
                </a>
            </div>
        '''
    html_ailments = f'''
        <div style="margin-bottom: 9.6rem;">
            <div class="grid-4" style="gap: 3.2rem;">
                {html_ailments_cards}
            </div>
        </div>
    '''
    html_main = f'''
        <h1 style="font-size: 6.4rem; line-height: 1; margin-bottom: 9.6rem;">All Common Ailments</h1>
        {html_ailments}
    '''
    meta_title = f'''All Ailments'''
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
    html_filepath = f'''{g.website_folderpath}/{url_slug}.html'''
    with open(html_filepath, 'w') as f: f.write(html)

def gen():
    ailments_gen()
    ailments_all_gen()
    ailments_systems_gen()
    ailments_systems_system_gen()
    # ailments_organs_gen()
