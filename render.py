import os
import time
import json
import shutil
import sqlite3

from lorem_text import lorem

from lib import g
from lib import io
from lib import data
from lib import polish
from lib import sections
from lib import components

import normalize_utils

shutil.copy2('styles.css', f'{g.website_folderpath}/styles.css')

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

    ### TODO: move the data "resolve" -> "compile", pass the data through the entire pipeline
    # wcvp_plant_data = io.json_read(f'{g.DATA_FOLDERPATH}/resolve/wcvp/json/{plant_taxon_name_normalized}.json')

    ###
    html_article = f''
    '''
                border-bottom: 1px solid #d8d8d8; 
                padding-bottom: 4.8rem;
    '''
    html_hero = f'''
        <section
            style="
            "
        >
            {sections.breadcrumbs_explorer(url_slug)}
            <div class="m-flex" style="
                gap: 3.2rem;
box-shadow: rgba(0, 0, 0, 0.15) 1.95px 1.95px 2.6px;
box-shadow: rgba(0, 0, 0, 0.16) 0px 1px 4px;
box-shadow: rgba(0, 0, 0, 0.05) 0px 6px 24px 0px, rgba(0, 0, 0, 0.08) 0px 0px 0px 1px;
                    box-shadow: rgba(149, 157, 165, 0.2) 0px 8px 24px;
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
                <div style="flex: 3; padding-top: 4.8rem; padding-bottom: 4.8rem;">
                    <h1>{plant_name}</h1>
                    <p>Common name</p>
                    <p>{lorem.words(48)}</p>
                    <p>Scientific resources: Moderate (★★★☆☆)</p>
                    <ul style="list-style: none;">
                        <li>Scientific names: {plant_name}</li>
                        <li>Common names</li>
                        <li>Family: {plant_data['taxonomies'][0]['family']}</li>
                        <li>Native range</li>
                    </ul>
                </div>
            </div>
        </section>
    '''
    html_article += html_hero

    ### TAXONOMY
    taxonomies = plant_data['taxonomies']
    if taxonomies != []:
        taxonomy = taxonomies[0]
        html_table_body = f''
        html_table_body += f'''<tbody>'''
        html_table_body += f'''
            <tr>
                <td>Kingdom</td>
                <td>{taxonomy['kingdom']}</td>
            </tr>
            <tr>
                <td>Phylum</td>
                <td>{taxonomy['phylum']}</td>
            </tr>
            <tr>
                <td>Class</td>
                <td>{taxonomy['class']}</td>
            </tr>
            <tr>
                <td>Subclass</td>
                <td>{taxonomy['subclass']}</td>
            </tr>
            <tr>
                <td>Order</td>
                <td>{taxonomy['order']}</td>
            </tr>
            <tr>
                <td>Family</td>
                <td>{taxonomy['family']}</td>
            </tr>
            <tr>
                <td>Genus</td>
                <td>{taxonomy['genus']}</td>
            </tr>
        '''
        html_table_body += f'''</tbody>'''
        html_article += f'''
            <section>
                <h2>
                    Taxonomical Classification
                </h2>
                <table>
                  <thead>
                    <tr>
                      <th>Rank</th>
                      <th>Classification</th>
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
            print(chemical)
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
                    {plant_name} has {len(plant_data['chemicals'])} reported phytochemicals identified across {source_tot} scientific publications and several other databases. The most consistently reported compounds include {chemicals_p_str}.
                </p>
                <dl>
                    <div>
                        <dt>Total compounds</dt>
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
                    {plant_name} has {len(plant_data['activities'])} reported activities identified across {source_tot} scientific publications and several other databases. The most consistently reported compounds include {activities_p_str}.
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
                    Diseases
                </h2>
                <p>
                    {plant_name} has {len(plant_data['diseases'])} reported treated diseases identified across {source_tot} scientific publications and several other databases. The most consistently reported compounds include {diseases_p_str}.
                </p>
                <dl>
                    <div>
                        <dt>Total diseases</dt>
                        <dd>{len(plant_data['diseases'])}</dd>
                    </div>
                    <div>
                        <dt>Scientific sources</dt>
                        <dd>{source_tot}</dd>
                    </div>
                </dl>
                <h3>Most Reported Diseases</h3>
                <table>
                  <thead>
                    <tr>
                      <th>Disease</th>
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
    html = f''' 
        <!DOCTYPE html>
        <html lang="en">
        {head_html}
        <body>
            {sections.header_dark()}
            <main class="container-xl listing m-flex" style="gap: 4.8rem; margin-top: 4.8rem;">
                <div style="flex: 3;">
                    {html_article}
                </div>
                <div style="flex: 1;">
                    {sidebar_html}
                </div>
            </main>
            {sections.footer()}
        </body>
        </html>
    '''.strip()
    html_filepath = f'{g.website_folderpath}/{url_slug}.html'
    with open(html_filepath, 'w') as f: f.write(html)
    print(html_filepath)

plants_rows = sqlite_table_master_plants_get()
for plant_row in plants_rows[:1]:
    print(plant_row)
    plant_listing_page_gen_new(plant_row[1])

