import os
import time
import json
import shutil
import sqlite3

from lorem_text import lorem

from lib import g
from lib import io
from lib import llm
from lib import data
from lib import polish
from lib import sections
from lib import components

import normalize_utils
import masterize_utils

shutil.copy2('styles.css', f'{g.website_folderpath}/styles.css')

model_filepath = '/home/ubuntu/vault-tmp/llm/gemma-4-26B-A4B-it-UD-Q4_K_XL.gguf'

def sqlite_table_master_plants_get():
    db_filepath = f'{g.VAULT_FOLDERPATH}/terrawhisper/data/masterize/master.db'
    conn = sqlite3.connect(db_filepath)
    cur = conn.cursor()
    cur.execute("""
        SELECT *
        FROM plants
    """)
    row = cur.fetchall()
    conn.close()
    return row

def sqlite_table_observations_plants_activities_get():
    db_filepath = f'{g.VAULT_FOLDERPATH}/terrawhisper/data/qualify/observations.db'
    conn = sqlite3.connect(db_filepath)
    cur = conn.cursor()
    cur.execute("""
        SELECT *
        FROM plants_activities
    """)
    row = cur.fetchall()
    conn.close()
    return row

def plant_listing_page_gen_new(plant_name):
    plant_data = io.json_read(f'{g.VAULT_FOLDERPATH}/terrawhisper/data/compile/herbs/{plant_name}.json')
    # print(json.dumps(plant_data, indent=4))
    # quit()

    plant_taxon_name_slug = polish.sluggify(plant_name)
    plant_taxon_name_normalized = normalize_utils.normalize_plant_name(plant_name)

    url_slug = f'herbs/{plant_taxon_name_slug}'

    sidebar_html = f'''
        <div 
            style="
                display: flex; flex-direction: column; gap: 1.6rem; position: sticky; top: 0;
            "
        >
            <p>{lorem.sentence()}</p>
            <img src="/images/herbs/{plant_taxon_name_slug}.jpg">
            <img src="/images/herbs/{plant_taxon_name_slug}.jpg">
            <img src="/images/herbs/{plant_taxon_name_slug}.jpg">
        </div>
    '''

    html_article = f''
    ###
    if plant_data['names'] != []: 
        hero_plant_common_name = plant_data['names'][0]['alias_en']
        if hero_plant_common_name == None:
            hero_plant_common_name_html = ''
        else:
            hero_plant_common_name_html = f'<p><strong>{hero_plant_common_name.capitalize()}</strong></p>'
    else: 
        hero_plant_common_name = None
        hero_plant_common_name_html = f''
    ###
    if plant_data['distribution'] != []: hero_distribution = plant_data['distribution'][0]['continent'].title()
    else: hero_distribution = 'Not available'
    if plant_data['taxonomies'] != []: hero_taxonomy = plant_data['taxonomies'][0]['family'].title()
    else: hero_taxonomy = 'Not available'
                    # <p>Scientific resources: Moderate (★★★☆☆)</p>
    ### LLM INTRO
    json_article_filepath = f'''{g.DATA_FOLDERPATH}/enhance/{plant_taxon_name_slug}.json'''
    json_article = io.json_read(json_article_filepath, create=True)
    regen = False
    key = f'intro'
    if key not in json_article: json_article[key] = ''
    if regen: json_article[key] = ''
    if json_article[key] == '':
        prompt = f'''
            Write 50 words for an introduction to the following medicinal plant: {plant_name}.
            Start the reply with the following words: {plant_name}, commonly known as 
        '''.strip()
        print(prompt)
        # quit()
        reply = llm.reply(prompt, model_filepath)
        if '</think>' in reply:
            reply = reply.split('</think>')[1].strip()
        reply = polish.vanilla(reply)
        json_article[key] = reply
        io.json_write(json_article_filepath, json_article)
    intro_text = json_article[key]
                    # box-shadow: rgba(149, 157, 165, 0.2) 0px 8px 24px;
                    # <li>Common names</li>
    html_hero = f'''
        <section
            style="
            "
        >
            {sections.breadcrumbs_explorer(url_slug)}
            <div class="m-flex" style="
                ">
                <div style="flex: 2;">
                    <img 
                        src="/images/herbs/{plant_taxon_name_slug}.jpg"
                        style="
                            height: 100%;
                            object-fit: cover;
                            object-position: center;
                        "
                    >
                </div>
                <div style="flex: 3; padding: 2.4rem;">
                    <h1>{plant_name}</h1>
                    {hero_plant_common_name_html}
                    <p>{intro_text}</p>
                    <ul style="list-style: none;">
                        <li><span style="font-weight: 700;">Scientific name:</span> <strong style="font-weight: 400;">{plant_name}</strong></li>
                        <li><span style="font-weight: 700;">Family:</span> <strong style="font-weight: 400;">{hero_taxonomy}</strong></li>
                        <li><span style="font-weight: 700;">Native range:</span> <strong style="font-weight: 400;">{hero_distribution}</strong></li>
                    </ul>
                </div>
            </div>
        </section>
    '''
    html_article += html_hero

    ### CLASSIFICATION

    ### TAXONOMIES
    taxonomies = plant_data['taxonomies']
    if taxonomies != []:
        taxonomy = taxonomies[0]
        ### llm
        json_article_filepath = f'''{g.DATA_FOLDERPATH}/enhance/{plant_taxon_name_slug}.json'''
        json_article = io.json_read(json_article_filepath, create=True)
        regen = False
        key = f'taxonomy'
        if key not in json_article: json_article[key] = ''
        if regen: json_article[key] = ''
        if json_article[key] == '':
            prompt = f'''
                Write a paragraph in 2-4 sentences about the taxonomy of the following medicinal plant: {plant_name}.
                Use the following taxonomical classification:
                Kingdom: {taxonomy['kingdom']}
                Phylum: {taxonomy['phylum']}
                Class: {taxonomy['class']}
                Subclass: {taxonomy['subclass']}
                Order: {taxonomy['order']}
                Family: {taxonomy['family']}
                Genus: {taxonomy['genus']}
                Start the reply with the following words: This plant 
            '''.strip()
            print(prompt)
            reply = llm.reply(prompt, model_filepath)
            if '</think>' in reply:
                reply = reply.split('</think>')[1].strip()
            reply = polish.vanilla(reply)
            json_article[key] = reply
            io.json_write(json_article_filepath, json_article)
        taxonomy_text = json_article[key]
        ### table
        html_table_body = f''
        html_table_body += f'''<tbody>'''
        html_table_body += f'''
            <tr>
                <td>Kingdom</td>
                <td>{taxonomy['kingdom']}</td>
                <td>WCVP</td>
            </tr>
            <tr>
                <td>Phylum</td>
                <td>{taxonomy['phylum']}</td>
                <td>WCVP</td>
            </tr>
            <tr>
                <td>Class</td>
                <td>{taxonomy['class']}</td>
                <td>WCVP</td>
            </tr>
            <tr>
                <td>Subclass</td>
                <td>{taxonomy['subclass']}</td>
                <td>WCVP</td>
            </tr>
            <tr>
                <td>Order</td>
                <td>{taxonomy['order']}</td>
                <td>WCVP</td>
            </tr>
            <tr>
                <td>Family</td>
                <td>{taxonomy['family']}</td>
                <td>WCVP</td>
            </tr>
            <tr>
                <td>Genus</td>
                <td>{taxonomy['genus']}</td>
                <td>WCVP</td>
            </tr>
        '''
        html_table_body += f'''</tbody>'''
        html_article += f'''
            <section>
                <h2>
                    Taxonomical Classification
                </h2>
                <p>{taxonomy_text}</p>
                <table>
                  <thead>
                    <tr>
                      <th>Rank</th>
                      <th>Classification</th>
                      <th>Source</th>
                    </tr>
                  </thead>
                  {html_table_body}
                </table>
            </section>
        '''

    ### DISTRIBUTION
    distributions = plant_data['distribution']
    if distributions != []:
        ### llm
        json_article_filepath = f'''{g.DATA_FOLDERPATH}/enhance/{plant_taxon_name_slug}.json'''
        json_article = io.json_read(json_article_filepath, create=True)
        regen = False
        key = f'distribution'
        if key not in json_article: json_article[key] = ''
        if regen: json_article[key] = ''
        if json_article[key] == '':
            distribution_prompt = ''
            for distribution in distributions[:5]:
                distribution_prompt += f'''{distribution['region']}: {distribution['area']}\n'''
            prompt = f'''
                Write a paragraph in 5 sentences about the geographical distribution of the following medicinal plant: {plant_name}.
                Use the following geographical distribution:
                {distribution_prompt}
                Start the reply with the following words: This plant 
            '''.strip()
            print(prompt)
            reply = llm.reply(prompt, model_filepath)
            if '</think>' in reply:
                reply = reply.split('</think>')[1].strip()
            reply = polish.vanilla(reply)
            json_article[key] = reply
            io.json_write(json_article_filepath, json_article)
        distribution_text = json_article[key]
        ###
        html_table_body = f''
        html_table_body += f'''<tbody>'''
        row_num = 10
        for distribution in distributions[:row_num]:
            # print(distribution)
            # plant_name = plants_chemicals_row[1]
            continent = distribution['continent']
            region = distribution['region']
            area = distribution['area']
            html_table_body += f'''
            <tr>
                <td>{region}</td>
                <td>{area}</td>
                <td>WCVP</td>
            </tr>'''
        html_table_body += f'''</tbody>'''
        html_article += f'''
            <section>
                <h2>
                    Distribution
                </h2>
                <p>{distribution_text}</p>
                <table>
                  <thead>
                    <tr>
                      <th>Region</th>
                      <th>Area</th>
                      <th>Source</th>
                    </tr>
                  </thead>
                  {html_table_body}
                </table>
            </section>
        '''

    ### CHEMICALS
    chemicals = plant_data['chemicals']
    chemicals = sorted(chemicals, key=lambda x: x['num_sources'], reverse=True)
    if chemicals != []:
        html_table_body = f''
        html_table_body += f'''<tbody>'''
        table_chemical_num = 10
        for chemical in chemicals[:table_chemical_num]:
            # print(chemical)
            # plant_name = plants_chemicals_row[1]
            chemical_name = chemical['chemical_canonical_name']
            plant_part = chemical['plant_part']
            max_concentration = chemical['max_concentration']
            min_concentration = chemical['min_concentration']
            num_sources = chemical['num_sources']
                # <td>{plant_name}</td>
            confidence = ''
            if int(num_sources) >= 10: confidence = '★★★★★'
            elif int(num_sources) >= 7: confidence = '★★★★☆'
            elif int(num_sources) >= 5: confidence = '★★★☆☆'
            elif int(num_sources) >= 3: confidence = '★★☆☆☆'
            elif int(num_sources) >= 1: confidence = '★☆☆☆☆'
            html_table_body += f'''
            <tr>
                <td>{chemical_name}</td>
                <td>{num_sources}</td>
                <td>{confidence}</td>
            </tr>'''
        chemicals_p = []
        for chemical in chemicals[:5]:
            chemicals_p.append(chemical['chemical_canonical_name'])
        source_tot = 0 
        for chemical in chemicals[:]:
            source_tot += int(chemical['num_sources'])
        chemicals_p_str = ', '.join(chemicals_p)
        html_table_body += f'''</tbody>'''
        html_article += f'''
            <section>
                <h2>
                    Chemicals
                </h2>
                <p>
                    {plant_name} has {len(plant_data['chemicals'])} reported phytochemicals identified across {source_tot} scientific publications and several other databases. The most consistently reported chemicals include {chemicals_p_str}.
                </p>
                <dl>
                    <div>
                        <dt>Total chemicals</dt>
                        <dd>{len(plant_data['chemicals'])}</dd>
                    </div>
                    <div>
                        <dt>Scientific sources</dt>
                        <dd>{source_tot}</dd>
                    </div>
                </dl>
                <h3>Most Reported Compounds</h3>
                <table>
                  <thead>
                    <tr>
                      <th>Compound</th>
                      <th>Sources</th>
                      <th>Confidence</th>
                    </tr>
                  </thead>
                  {html_table_body}
                </table>
            </section>
        '''

    ### ACTIVITIES
    activities = plant_data['activities']
    activities = sorted(activities, key=lambda x: x['num_sources'], reverse=True)
    if activities != []:
        html_table_body = f''
        html_table_body += f'''<tbody>'''
        table_chemical_num = 10
        for activity in activities[:table_chemical_num]:
            activity_name = activity['activity_canonical_name']
            num_sources = activity['num_sources']
            confidence = ''
            if int(num_sources) >= 10: confidence = '★★★★★'
            elif int(num_sources) >= 7: confidence = '★★★★☆'
            elif int(num_sources) >= 5: confidence = '★★★☆☆'
            elif int(num_sources) >= 3: confidence = '★★☆☆☆'
            elif int(num_sources) >= 1: confidence = '★☆☆☆☆'
            html_table_body += f'''
            <tr>
                <td>{activity_name}</td>
                <td>{num_sources}</td>
                <td>{confidence}</td>
            </tr>'''
        activities_p = []
        for activity in activities[:5]:
            activities_p.append(activity['activity_canonical_name'])
        source_tot = 0 
        for activity in activities[:]:
            source_tot += int(activity['num_sources'])
        activities_p_str = ', '.join(activities_p)
        html_table_body += f'''</tbody>'''
        html_article += f'''
            <section>
                <h2>
                    Activities
                </h2>
                <p>
                    {plant_name} has {len(plant_data['activities'])} reported activities identified across {source_tot} scientific publications and several other databases. The most consistently reported activities include {activities_p_str}.
                </p>
                <dl>
                    <div>
                        <dt>Total activities</dt>
                        <dd>{len(plant_data['activities'])}</dd>
                    </div>
                    <div>
                        <dt>Scientific sources</dt>
                        <dd>{source_tot}</dd>
                    </div>
                </dl>
                <h3>Most Reported Activities</h3>
                <table>
                  <thead>
                    <tr>
                      <th>Activity</th>
                      <th>Sources</th>
                      <th>Confidence</th>
                    </tr>
                  </thead>
                  {html_table_body}
                </table>
            </section>
        '''

    ### DISEASES
    diseases = plant_data['diseases']
    diseases = sorted(diseases, key=lambda x: x['num_sources'], reverse=True)
    if diseases != []:
        html_table_body = f''
        html_table_body += f'''<tbody>'''
        table_chemical_num = 10
        for disease in diseases[:table_chemical_num]:
            disease_name = disease['disease_canonical_name']
            num_sources = disease['num_sources']
            confidence = ''
            if int(num_sources) >= 10: confidence = '★★★★★'
            elif int(num_sources) >= 7: confidence = '★★★★☆'
            elif int(num_sources) >= 5: confidence = '★★★☆☆'
            elif int(num_sources) >= 3: confidence = '★★☆☆☆'
            elif int(num_sources) >= 1: confidence = '★☆☆☆☆'
            html_table_body += f'''
            <tr>
                <td>{disease_name}</td>
                <td>{num_sources}</td>
                <td>{confidence}</td>
            </tr>'''
        diseases_p = []
        for disease in diseases[:5]:
            diseases_p.append(disease['disease_canonical_name'])
        source_tot = 0 
        for disease in diseases[:]:
            source_tot += int(disease['num_sources'])
        diseases_p_str = ', '.join(diseases_p)
        html_table_body += f'''</tbody>'''
        html_article += f'''
            <section>
                <h2>
                    Medicinal Uses
                </h2>
                <p>
                    {plant_name} has {len(plant_data['diseases'])} reported medicinal uses identified across {source_tot} scientific publications and several other databases. The most consistently reported uses include {diseases_p_str}.
                </p>
                <dl>
                    <div>
                        <dt>Total uses</dt>
                        <dd>{len(plant_data['diseases'])}</dd>
                    </div>
                    <div>
                        <dt>Scientific sources</dt>
                        <dd>{source_tot}</dd>
                    </div>
                </dl>
                <h3>Most Reported Uses</h3>
                <table>
                  <thead>
                    <tr>
                      <th>Use</th>
                      <th>Sources</th>
                      <th>Confidence</th>
                    </tr>
                  </thead>
                  {html_table_body}
                </table>
            </section>
        '''

    meta_title = f'{plant_name}'
    meta_description = f''
    canonical_html = f'''<link rel="canonical" href="https://terrawhisper.com/{url_slug}.html">'''
    head_html = components.html_head(
        meta_title, meta_description, css='/styles.css', canonical=canonical_html
    )

    '''
            <main class="container-xl listing m-flex" style="gap: 4.8rem; margin-top: 4.8rem;">
                <div style="flex: 3;">
                    {html_article}
                </div>
                <div style="flex: 1;">
                    {sidebar_html}
                </div>
            </main>
    '''
    html = f''' 
        <!DOCTYPE html>
        <html lang="en">
        {head_html}
        <body>
            {sections.header_dark()}
            <main class="container-lg listing" style="margin-top: 4.8rem;">
                {html_article}
            </main>
            {sections.footer()}
        </body>
        </html>
    '''.strip()
    html_filepath = f'{g.website_folderpath}/{url_slug}.html'
    with open(html_filepath, 'w') as f: f.write(html)
    print(html_filepath)

plants_rows = masterize_utils.masterize_plants_get_all()
for plant_row in plants_rows[:]:
    print(plant_row)
    plant_listing_page_gen_new(plant_row[1])

