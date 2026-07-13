import os
import time
import json
import shutil
import sqlite3

from lib import g
from lib import io
from lib import data
from lib import polish
from lib import sections
from lib import components

shutil.copy2('styles.css', f'{g.website_folderpath}/styles.css')

def plant_listing_page_gen_new(plant_name):
    plant_data = io.json_read(f'{g.VAULT_FOLDERPATH}/terrawhisper/data/compile/herbs/{plant_name}.json')

    plant_taxon_name_slug = polish.sluggify(plant_name)

    output_filepath = f'{g.SSOT_FOLDERPATH}/studies/extraction_new/chemicals/database.db'
    conn = sqlite3.connect(output_filepath)

    ###
    html_article = f''
    html_article += f'<h1>{plant_name}</h1>'

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

    url_slug = f'herbs/{plant_taxon_name_slug}'
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
            {sections.header_default()}
            {sections.breadcrumbs_new(url_slug)}
            <main class="container-xl listing m-flex">
                <div style="flex: 2;">
                {html_article}
                </div>
                <div style="flex: 1;">
                </div>
            </main>
            {sections.footer()}
        </body>
        </html>
    '''.strip()
    html_filepath = f'{g.website_folderpath}/{url_slug}.html'
    with open(html_filepath, 'w') as f: f.write(html)
    print(html_filepath)

plants_rows = data.sqlite__plants_get()
for plant_row in plants_rows[:]:
    print(plant_row)
    plant_listing_page_gen_new(plant_row[1])
