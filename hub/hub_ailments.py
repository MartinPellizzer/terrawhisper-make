import os

from lib import g
from lib import io
from lib import components
from lib import sections

def systems_ailments_get():
    ailments = io.csv_to_dict(f'{g.DATABASE_FOLDERPATH}/csv/ailments.csv')
    clusters = []
    for ailment in ailments:
        system_slug = ailment['system_slug']
        organ_slug = ailment['organ_slug']
        ailment_slug = ailment['ailment_slug']
        ailment_name = ailment['ailment_name']
        found = False
        for cluster_i, cluster in enumerate(clusters):
            if system_slug == cluster['system_slug']:
                clusters[cluster_i]['ailments'].append(ailment)
                found = True
                break
        if not found:
            clusters.append(
                {
                    'system_slug': system_slug,
                    'ailments': [ailment],
                }
            )
    return clusters

def ailments_by_organ_get():
    ailments = io.csv_to_dict(f'{g.DATABASE_FOLDERPATH}/csv/ailments.csv')
    clusters = []
    for ailment in ailments:
        system_slug = ailment['system_slug']
        organ_slug = ailment['organ_slug']
        ailment_slug = ailment['ailment_slug']
        ailment_name = ailment['ailment_name']
        found = False
        for cluster_i, cluster in enumerate(clusters):
            if organ_slug == cluster['organ_slug']:
                clusters[cluster_i]['ailments'].append(ailment)
                found = True
                break
        if not found:
            clusters.append(
                {
                    'organ_slug': organ_slug,
                    'ailments': [ailment],
                }
            )
    return clusters

def organs_get():
    ailments = io.csv_to_dict(f'{g.DATABASE_FOLDERPATH}/csv/ailments.csv')
    organs = []
    for ailment in ailments:
        if ailment['organ_slug'] not in organs: organs.append(ailment['organ_slug'])
    return organs

def systems_get():
    ailments = io.csv_to_dict(f'{g.DATABASE_FOLDERPATH}/csv/ailments.csv')
    systems = []
    for ailment in ailments:
        if ailment['system_slug'] not in systems: systems.append(ailment['system_slug'])
    return systems

def ailments_systems_gen():
    ailments_systems_system_gen()
    ###
    url_slug = 'ailments/systems'
    ###
    ailments = io.csv_to_dict(f'{g.DATABASE_FOLDERPATH}/csv/ailments.csv')
    clusters = systems_ailments_get()
    html_clusters = f''
    for cluster in clusters:
        cluster_name = cluster['system_slug']
        html_ailments = f''
        for ailment_i, ailment in enumerate(cluster['ailments']):
            ailment_slug = ailment['ailment_slug']
            ailment_name = ailment['ailment_name']
            print(f'AILMENT: {ailment_i}/{len(ailments)} - {ailment_name}')
            src = f'''/images/ailments/{ailment_slug}-herbs.jpg'''
            alt = f'''{ailment_name} herbs'''
            html_ailments += f'''
                <div class="card-default">
                    <a href="/{url_slug}/{ailment_slug}.html">
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

def ailments_systems_system_gen():
    ailments = io.csv_to_dict(f'{g.DATABASE_FOLDERPATH}/csv/ailments.csv')
    ### cluster by system
    clusters = systems_ailments_get()
    for cluster in clusters:
        system_name = cluster['system_slug']
        system_slug = system_name.strip().lower().replace(' ', '-')
        url_slug = f'ailments/systems/{system_slug}'
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
                <h2 style="font-size: 4.8rem; line-height: 1; padding-bottom: 1.6rem; margin-bottom: 1.6rem; border-bottom: 1px solid #333333;">{system_name.title()}</h2>
                <div class="grid-3" style="gap: 3.2rem;">
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
    clusters = ailments_by_organ_get()
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
    clusters = ailments_by_organ_get()
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

def gen():
    ailments_systems_gen()
    ailments_organs_gen()
    ###
    url_slug = 'ailments'
    ailments = io.csv_to_dict(f'{g.DATABASE_FOLDERPATH}/csv/ailments.csv')
    preparations = io.csv_to_dict(f'{g.database_folderpath}/csv/preparations.csv')
    ### cluster by system
    clusters = systems_ailments_get()
    html_systems_cards = f''
    for cluster in clusters:
        system_slug = cluster['system_slug']
        ailment = cluster['ailments'][0]
        ailment_slug = ailment['ailment_slug']
        ailment_name = ailment['ailment_name']
        src = f'''/images/ailments/{ailment_slug}-herbs.jpg'''
        alt = f'''{ailment_name} herbs'''
        html_systems_cards += f'''
            <div class="card-default">
                <a href="/{url_slug}/systems/{system_slug}.html">
                    <img src="{src}" alt="{alt}">
                    <h2>{system_slug.title()}</h2>
                </a>
            </div>
        '''
    html_systems = f'''
        <div style="margin-bottom: 9.6rem;">
            <h2 style="font-size: 4.8rem; line-height: 1; padding-bottom: 1.6rem; margin-bottom: 1.6rem; border-bottom: 1px solid #333333;">Systems</h2>
            <div class="grid-3" style="gap: 3.2rem;">
                {html_systems_cards}
            </div>
        </div>
    '''
    ### cluster by organ
    clusters = ailments_by_organ_get()
    html_organs_cards = f''
    for cluster in clusters:
        organ_name = cluster['organ_slug']
        organ_slug = organ_name.strip().lower().replace(' ', '-')
        ailment = cluster['ailments'][0]
        ailment_slug = ailment['ailment_slug']
        ailment_name = ailment['ailment_name']
        src = f'''/images/ailments/{ailment_slug}-herbs.jpg'''
        alt = f'''{ailment_name} herbs'''
        html_organs_cards += f'''
            <div class="card-default">
                <a href="/{url_slug}/organs/{organ_slug}.html">
                    <img src="{src}" alt="{alt}">
                    <h2>{organ_name.title()}</h2>
                </a>
            </div>
        '''
    html_organs = f'''
        <div style="margin-bottom: 9.6rem;">
            <h2 style="font-size: 4.8rem; line-height: 1; padding-bottom: 1.6rem; margin-bottom: 1.6rem; border-bottom: 1px solid #333333;">Organs</h2>
            <div class="grid-3" style="gap: 3.2rem;">
                {html_organs_cards}
            </div>
        </div>
    '''
    html_main = f'''
        <h1 style="font-size: 6.4rem; line-height: 1; margin-bottom: 9.6rem;">Common Ailments and Their Herbal Remedies</h1>
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

