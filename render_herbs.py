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
    plant_data = io.json_read(f'{g.DATA_FOLDERPATH}/compile/herbs/{plant_name}.json')
    # print(json.dumps(plant_data, indent=4))
    # print(json.dumps(plant_data['names_common'], indent=4))
    # quit()

    plant_taxon_name_slug = polish.sluggify(plant_name)
    plant_taxon_name_normalized = normalize_utils.normalize_plant_name(plant_name)

    plant_parts_data = plant_data['plants_parts']
    plant_synonyms = plant_data['synonyms']

    url_slug = f'herbs/{plant_taxon_name_slug}'

    html_article = f''

    ################################################################################
    # HERO
    ################################################################################

    ## H1
    plant_name_common = plant_data['names_common']['plant_name_common_preferred']
    if plant_name_common != '': h1_html = f'<h1>{plant_name_common}</h1>'
    else: h1_html = f'<h1>{plant_name}</h1>'

    ### SCIENTIFIC NAME ACCEPTED
    name_scientific_accepted = f'''
        <p>
            <i lang="la">{plant_name}</i> · 
            <span>Accepted scientific name</span>
        </p>
    '''

    ### EVIDENCE CONSENSUS
    db_filepath = f'{g.DATA_FOLDERPATH}/qualify/observations.db'
    conn = sqlite3.connect(db_filepath)
    rows_num = 0
    ###
    plant_name_scientific_canon = plant_name
    cursor = conn.execute("""
        SELECT COUNT (*)
        FROM plants_parts
        WHERE plant_canonical_name = ?
    """, (plant_name_scientific_canon,))
    rows_num += int(cursor.fetchone()[0])
    cursor = conn.execute("""
        SELECT COUNT (*)
        FROM plants_chemicals
        WHERE plant_name_scientific_canon = ?
    """, (plant_name_scientific_canon,))
    rows_num += int(cursor.fetchone()[0])
    cursor = conn.execute("""
        SELECT COUNT (*)
        FROM plants_activities
        WHERE plant_name_scientific_canon = ?
    """, (plant_name_scientific_canon,))
    rows_num += int(cursor.fetchone()[0])
    cursor = conn.execute("""
        SELECT COUNT (*)
        FROM plants_diseases
        WHERE plant_canonical_name = ?
    """, (plant_name_scientific_canon,))
    rows_num += int(cursor.fetchone()[0])
    evidence_consensus_count = rows_num
    ###
    if evidence_consensus_count >= 200: 
        consensus_stars = '★★★★★'
        consensus_tag = 'Very Extensive'
    elif evidence_consensus_count >= 150: 
        consensus_stars = '★★★★☆'
        consensus_tag = 'Extensive'
    elif evidence_consensus_count >= 100: 
        consensus_stars = '★★★☆☆'
        consensus_tag = 'Moderate'
    elif evidence_consensus_count >= 50: 
        consensus_stars = '★★☆☆☆'
        consensus_tag = 'Sparse'
    else: 
        consensus_stars = '★☆☆☆☆'
        consensus_tag = 'Very Sparse'

    ### FAMILY
    if plant_data['taxonomies'] != []: hero_taxonomy = plant_data['taxonomies'][0]['family'].title()
    else: hero_taxonomy = 'Not available'

    ### NATIVE RANGE
    if plant_data['distribution'] != []: hero_distribution = plant_data['distribution'][0]['continent'].title()
    else: hero_distribution = 'Not available'

    ### PLANTS PARTS
    hero_plant_parts_list = []
    for item in plant_parts_data[:2]:
        hero_plant_parts_list.append(item['plant_part_canonical_name'])
    hero_plant_parts_html = ' · '.join(hero_plant_parts_list)
    hero_plant_parts_html = hero_plant_parts_html.title()
    if hero_plant_parts_html == '': hero_plant_parts_html = 'Not available'

    ### NAMES COMMON
    hero_names_common_list = []
    for value in plant_data['names_common']['en_labels']:
        hero_names_common_list.append(value)
    for value in plant_data['names_common']['en_aliases']:
        hero_names_common_list.append(value)
    hero_names_common_html = ' · '.join(hero_names_common_list[:2]).title()
    hero_names_common_count = len(hero_names_common_list) - 2
    if len(hero_names_common_list) <= 0:
        hero_names_common_html = f'''Not available'''
    elif len(hero_names_common_list) <= 2:
        hero_names_common_html = f'''
            <i lang="la">{hero_names_common_html}</i>
        '''
    else:
        hero_names_common_html = f'''
            <i lang="la">{hero_names_common_html}</i> · 
            <a href="#common-names">{hero_names_common_count} more</a>
        '''

    ### SYNONYMS
    hero_synonyms_list = []
    for item in plant_synonyms:
        hero_synonyms_list.append(item['plant_synonym'])
    hero_synonyms_html = ' · '.join(hero_synonyms_list[:2]).title()
    hero_synonyms_count = len(plant_synonyms) - 2
    if len(hero_synonyms_list) <= 0:
        hero_synonyms_html = f'''Not available'''
    elif len(hero_synonyms_list) <= 2:
        hero_synonyms_html = f'''
            <i lang="la">{hero_synonyms_html}</i>
        '''
    else:
        hero_synonyms_html = f'''
            <i lang="la">{hero_synonyms_html}</i> · 
            <a href="#synonyms">{hero_synonyms_count} more</a>
        '''

    ### LLM INTRO
    json_article_filepath = f'''{g.DATA_FOLDERPATH}/enhance/{plant_taxon_name_slug}.json'''
    json_article = io.json_read(json_article_filepath, create=True)
    regen = False
    dispel = False
    key = f'intro'
    if key not in json_article: json_article[key] = ''
    if regen: json_article[key] = ''
    if dispel: 
        json_article[key] = ''
        io.json_write(json_article_filepath, json_article)
        return
    if json_article[key] == '':
        plant_name_common = plant_data['names_common']['plant_name_common_preferred']
        prompt = f'''
            Write 50 words for an introduction to the following medicinal plant: {plant_name}.
            Start the reply with the following words: {plant_name_common}, scientifically known as {plant_name}, is
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

    ###
    html_hero = f'''
        {sections.breadcrumbs_explorer(url_slug)}
        <div class="flex-auto" 
            style="
                gap: 2.4rem;
                padding-bottom: 4.8rem;
                border-bottom: 1px solid #dcdcdc;
            "
        >
            <div style="flex: 3;">
              {h1_html}
              {name_scientific_accepted}
              <p>
                <span style="font-weight: 700;">Scientific literature:</span>
                <span>{consensus_tag}</span>
                <span>({evidence_consensus_count} studies)</span> · 
                <span aria-label="{consensus_tag}">{consensus_stars}</span>
              </p>
                <p>{intro_text}</p>
              <dl class="quick-facts">
                <div>
                  <dt>Family</dt>
                  <dd>{hero_taxonomy}</dd>
                </div>
                <div>
                  <dt>Native range</dt>
                  <dd>{hero_distribution}</dd>
                </div>
                <div>
                  <dt>Parts used</dt>
                  <dd>{hero_plant_parts_html}</dd>
                </div>
                <div>
                  <dt>Common names</dt>
                  <dd>{hero_names_common_html}</dd>
                </div>
                <div>
                  <dt>Scientific synonyms</dt>
                  <dd>{hero_synonyms_html}</dd>
                </div>
              </dl>
            </div>
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
        </div>

    '''
    '''
                <div>
                  <dt>Traditions</dt>
                  <dd>Ayurveda</dd>
                </div>
                <div>
                  <dt>Also known as</dt>
                  <dd>
                    Indian ginseng · Winter cherry ·
                    <a href="#common-names">25 more</a>
                  </dd>
                </div>

    '''
    html_article += html_hero

    ################################################################################
    ### NAMES
    ################################################################################
    ### NAMES COMMON
    if len(plant_data['names_common']['en_labels']) != 0 or len(plant_data['names_common']['en_aliases']) != 0:
        plant_names_common_en_html = f''
        plant_names_common_en_html = f'<h3 id="common-names">Common Names</h3>'
        plant_names_common_en_html += f'<ul style="list-style: none;">'
        for tag in plant_data['names_common']['en_labels']:
            plant_names_common_en_html += f'''
                <li class="tag">{tag}</li>
            '''
        for tag in plant_data['names_common']['en_aliases']:
            plant_names_common_en_html += f'''
                <li class="tag">{tag}</li>
            '''
        plant_names_common_en_html += f'</ul>'
    else:
        plant_names_common_en_html = ''

    ### NAMES REGIONAL
    plant_names_common_regional_html = ''
    ### SPANISH
    values_html = ''
    for value in plant_data['names_common']['es_names']:
        values_html += f'''
            <li class="tag">{value}</li>
        '''
    if values_html != '':
        plant_names_common_regional_html += f'<div style="display: flex; gap: 0.8rem;">'
        plant_names_common_regional_html += f'<h4>Spanish:</h4>' 
        plant_names_common_regional_html += f'<ul style="list-style: none;">'
        plant_names_common_regional_html += values_html 
        plant_names_common_regional_html += f'</ul>'
        plant_names_common_regional_html += f'</div>'
    ### GERMAN
    values_html = ''
    for value in plant_data['names_common']['de_names']:
        values_html += f'''
            <li class="tag">{value}</li>
        '''
    if values_html != '':
        plant_names_common_regional_html += f'<div style="display: flex; gap: 0.8rem;">'
        plant_names_common_regional_html += f'<h4>German:</h4>' 
        plant_names_common_regional_html += f'<ul style="list-style: none;">'
        plant_names_common_regional_html += values_html 
        plant_names_common_regional_html += f'</ul>'
        plant_names_common_regional_html += f'</div>'
    ### FRENCH
    values_html = ''
    for value in plant_data['names_common']['fr_names']:
        values_html += f'''
            <li class="tag">{value}</li>
        '''
    if values_html != '':
        plant_names_common_regional_html += f'<div style="display: flex; gap: 0.8rem;">'
        plant_names_common_regional_html += f'<h4>French:</h4>' 
        plant_names_common_regional_html += f'<ul style="list-style: none;">'
        plant_names_common_regional_html += values_html 
        plant_names_common_regional_html += f'</ul>'
        plant_names_common_regional_html += f'</div>'
    ###
    if plant_names_common_regional_html != '':
        plant_names_common_regional_html = f'''
            <h3>Regional and Traditional Names</h3>
            {plant_names_common_regional_html}
        '''

    ### SYNONYMS
    synonyms_html = ''
    synonyms_html += f'<ul style="list-style: none;">'
    for item in plant_data['synonyms']:
        value = item['plant_synonym']
        synonyms_html += f'''
            <li class="tag"><i>{value}</i></li>
        '''
    synonyms_html += f'</ul>'

    ### NAMES COMMON
    if len(plant_data['synonyms']) != 0:
        synonyms_html = f''
        synonyms_html = f'<h4 id="synonyms" style="margin-bottom: 1rem;">Synonyms</h4>'
        synonyms_html += f'<ul style="list-style: none;">'
        for item in plant_data['synonyms']:
            value = item['plant_synonym']
            synonyms_html += f'''
                <li class="tag"><i>{value}</i></li>
            '''
        synonyms_html += f'</ul>'
    else:
        synonyms_html = ''

    html_article += f'''
        <section id="names-and-synonyms">
          <h2>Names</h2>
          {plant_names_common_en_html}
          {plant_names_common_regional_html}
          <h3>Scientific Names</h3>
          <h4 style="margin-bottom: 1rem;">Accepted name</h4> <span class="tag">{plant_name}</span>
          {synonyms_html}
        </section>
    '''
    if 0:
        '''
            <h3>Other Names</h3>
            <ul>
            <li>{{other_name}}</li>
            </ul>
            <h3>Commonly Confused Plants</h3>
            <ul>
            <li>{{related_or_confused_species}}</li>
            </ul>
        '''

    ################################################################################
    ### CLASSIFICATION
    ################################################################################

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

    ################################################################################
    ### IDENTIFICATION
    ################################################################################

    ### PLANT PARTS
    plants_parts_data = plant_data['plants_parts']
    if plants_parts_data != []:
        ### filter rows
        row_num = 10
        items_filtered = []
        for item in plants_parts_data:
            ### add filter condition here if needed
            items_filtered.append(item)
            if len(items_filtered) >= row_num:
                break
        if 1:
            ### llm
            json_article_filepath = f'''{g.DATA_FOLDERPATH}/enhance/{plant_taxon_name_slug}.json'''
            json_article = io.json_read(json_article_filepath, create=True)
            regen = False
            key = f'plants_parts'
            if key not in json_article: json_article[key] = ''
            if regen: json_article[key] = ''
            if json_article[key] == '':
                list_prompt = ''
                for item in items_filtered[:5]:
                    plant_part = item['plant_part_canonical_name']
                    list_prompt += f'''{plant_part}\n'''
                prompt = f'''
                    Write a paragraph about the plant parts of the following medicinal plant: {plant_name}.
                    Use the following plant parts:
                    {list_prompt}
                    Start the reply with the following words: This plant 
                '''.strip()
                print(prompt)
                reply = llm.reply(prompt, model_filepath)
                if '</think>' in reply:
                    reply = reply.split('</think>')[1].strip()
                reply = polish.vanilla(reply)
                json_article[key] = reply
                io.json_write(json_article_filepath, json_article)
            names_text = json_article[key]
        else:
            names_text = ''
        ###
        html_table_body = f''
        html_table_body += f'''<tbody>'''
        for item in items_filtered:
            plant_part = item['plant_part_canonical_name']
            sources_num = item['sources_num']
            sources = item['sources']
            source = sources[0]
            confidence = ''
            if int(sources_num) >= 10: confidence = '★★★★★'
            elif int(sources_num) >= 7: confidence = '★★★★☆'
            elif int(sources_num) >= 5: confidence = '★★★☆☆'
            elif int(sources_num) >= 3: confidence = '★★☆☆☆'
            elif int(sources_num) >= 1: confidence = '★☆☆☆☆'
            html_table_body += f'''
                <tr>
                    <td>{plant_part}</td>
                    <td>{source} (and other {sources_num} sources)</td>
                    <td>{confidence}</td>
                </tr>
            '''
        source_tot = 0 
        for item in plants_parts_data[:]:
            source_tot += int(item['sources_num'])
        html_table_body += f'''</tbody>'''
        html_article += f'''
            <section>
                <h2>
                    Plant Parts
                </h2>
                {names_text}
                <table>
                  <thead>
                    <tr>
                      <th>Plant Part</th>
                      <th>Sources</th>
                      <th>Consensus</th>
                    </tr>
                  </thead>
                  {html_table_body}
                </table>
            </section>
        '''

    ### CHEMICALS
    chemicals = plant_data['chemicals']
    if chemicals != []:
        html_table_body = f''
        sources_html = f''
        html_table_body += f'''<tbody>'''
        table_chemical_num = 10
        for item in chemicals[:table_chemical_num]:
            chemical_name = item['chemical_canonical_name']
            chemical_slug = polish.sluggify(chemical_name)
            sources_num = item['sources_num']
            sources = item['sources']
            source = sources[0]
            confidence = ''
            if int(sources_num) >= 10: confidence = '★★★★★'
            elif int(sources_num) >= 7: confidence = '★★★★☆'
            elif int(sources_num) >= 5: confidence = '★★★☆☆'
            elif int(sources_num) >= 3: confidence = '★★☆☆☆'
            elif int(sources_num) >= 1: confidence = '★☆☆☆☆'
            html_table_body += f'''
                <tr>
                    <th scope="row">{chemical_name}</th>

                    <td>
                        <a href="#sources-{chemical_slug}">
                            {sources_num} supporting sources
                        </a>
                    </td>

                    <td>
                        <span>
                            {confidence}
                        </span>
                    </td>
                </tr>
            '''
            ### TODO: add this complete consensus instead of the one in the table
            '''
                        <span aria-label="Very high source consensus">
                            {confidence}
                        </span>
                        <span>Very high</span>
            '''
            ### SOURCES LISTS
            sources_html += f'''
                <h3 id="sources-{chemical_slug}">{chemical_name}</h3>
                <ol class="listing-sources">
            '''
            for source in sources[:5]:
                sources_html += f'''
                    <li>
                        <cite>
                            {source}
                        </cite>
                    </li>
                '''
            sources_html += f'''
                </ol>
            '''
            if len(sources)-5 > 0:
                sources_html += f'''
                    <details>
                        <summary>
                            View {len(sources)-5} additional sources
                        </summary>
                        <ol class="listing-sources" start="6">
                '''
                for source in sources[5:]:
                    sources_html += f'''
                        <li>
                            <cite>
                                {source}
                            </cite>
                        </li>
                    '''
                sources_html += f'''
                        </ol>
                    </details>
                '''
        source_tot = 0 
        for item in plants_parts_data[:]:
            source_tot += int(item['sources_num'])
        chemicals_p = []
        for chemical in chemicals[:5]:
            chemicals_p.append(chemical['chemical_canonical_name'])
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
                <table style="margin-top: 3.2rem;">
                    <caption style="text-align: left; margin-bottom: 0.8rem;">
                        Chemicals reported in {plant_name}
                    </caption>
                    <thead>
                        <tr>
                            <th scope="col">Chemical</th>
                            <th scope="col">Supporting sources</th>
                            <th scope="col">Consensus</th>
                        </tr>
                    </thead>
                    {html_table_body}
                </table>
            </section>
        '''
        ###

        html_article += f'''
            <section aria-labelledby="compounds-heading">
                {sources_html}
            </section>
        '''

    ### ACTIVITIES
    activities = plant_data['activities']
    if activities != []:
        html_table_body = f''
        html_table_body += f'''<tbody>'''
        table_chemical_num = 10
        for item in activities[:table_chemical_num]:
            activity_name = item['activity_canonical_name']
            sources_num = item['sources_num']
            sources = item['sources']
            source = sources[0]
            confidence = ''
            if int(sources_num) >= 10: confidence = '★★★★★'
            elif int(sources_num) >= 7: confidence = '★★★★☆'
            elif int(sources_num) >= 5: confidence = '★★★☆☆'
            elif int(sources_num) >= 3: confidence = '★★☆☆☆'
            elif int(sources_num) >= 1: confidence = '★☆☆☆☆'
            html_table_body += f'''
                <tr>
                    <td>{activity_name}</td>
                    <td>{source} (and other {sources_num} sources)</td>
                    <td>{confidence}</td>
                </tr>
            '''
        source_tot = 0 
        for item in plants_parts_data[:]:
            source_tot += int(item['sources_num'])
        activities_p = []
        for activity in activities[:5]:
            activities_p.append(activity['activity_canonical_name'])
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
                <h3>Most Reported Activities</h3>
                <table>
                  <thead>
                    <tr>
                      <th>Activity</th>
                      <th>Sources</th>
                      <th>Consensus</th>
                    </tr>
                  </thead>
                  {html_table_body}
                </table>
            </section>
        '''

    ### DISEASES
    diseases = plant_data['diseases']
    if diseases != []:
        html_table_body = f''
        html_table_body += f'''<tbody>'''
        table_chemical_num = 10
        for item in diseases[:table_chemical_num]:
            disease_name = item['disease_canonical_name']
            sources_num = item['sources_num']
            sources = item['sources']
            source = sources[0]
            confidence = ''
            if int(sources_num) >= 10: confidence = '★★★★★'
            elif int(sources_num) >= 7: confidence = '★★★★☆'
            elif int(sources_num) >= 5: confidence = '★★★☆☆'
            elif int(sources_num) >= 3: confidence = '★★☆☆☆'
            elif int(sources_num) >= 1: confidence = '★☆☆☆☆'
            html_table_body += f'''
                <tr>
                    <td>{disease_name}</td>
                    <td>{source} (and other {sources_num} sources)</td>
                    <td>{confidence}</td>
                </tr>
            '''
        source_tot = 0 
        for item in plants_parts_data[:]:
            source_tot += int(item['sources_num'])
        diseases_p = []
        for disease in diseases[:5]:
            diseases_p.append(disease['disease_canonical_name'])
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
                <h3>Most Reported Uses</h3>
                <table>
                  <thead>
                    <tr>
                      <th>Use</th>
                      <th>Sources</th>
                      <th>Consensus</th>
                    </tr>
                  </thead>
                  {html_table_body}
                </table>
            </section>
        '''

    ### PREPARATIONS
    data = plant_data['preparations']
    if data != []:
        ### filter rows
        row_num = 10
        items_filtered = []
        for item in data:
            ### add filter condition here if needed
            items_filtered.append(item)
            if len(items_filtered) >= row_num:
                break
        if 0:
            ### llm
            json_article_filepath = f'''{g.DATA_FOLDERPATH}/enhance/{plant_taxon_name_slug}.json'''
            json_article = io.json_read(json_article_filepath, create=True)
            regen = False
            key = f'preparations'
            if key not in json_article: json_article[key] = ''
            if regen: json_article[key] = ''
            if json_article[key] == '':
                list_prompt = ''
                for item in items_filtered[:5]:
                    list_item = item['preparation_canonical_name']
                    list_prompt += f'''{list_item}\n'''
                prompt = f'''
                    Write a paragraph about the herbal preparations of the following medicinal plant: {plant_name}.
                    Use the following plant parts:
                    {list_prompt}
                    Start the reply with the following words: This plant 
                '''.strip()
                print(prompt)
                reply = llm.reply(prompt, model_filepath)
                if '</think>' in reply:
                    reply = reply.split('</think>')[1].strip()
                reply = polish.vanilla(reply)
                json_article[key] = reply
                io.json_write(json_article_filepath, json_article)
            names_text = json_article[key]
        else:
            names_text = ''
        ###
        html_table_body = f''
        html_table_body += f'''<tbody>'''
        for item in items_filtered:
            preparation = item['preparation_canonical_name']
            sources_num = item['sources_num']
            sources = item['sources']
            source = sources[0]
            confidence = ''
            if int(sources_num) >= 10: confidence = '★★★★★'
            elif int(sources_num) >= 7: confidence = '★★★★☆'
            elif int(sources_num) >= 5: confidence = '★★★☆☆'
            elif int(sources_num) >= 3: confidence = '★★☆☆☆'
            elif int(sources_num) >= 1: confidence = '★☆☆☆☆'
            html_table_body += f'''
                <tr>
                    <td>{preparation}</td>
                    <td>{source} (and other {sources_num} sources)</td>
                    <td>{confidence}</td>
                </tr>
            '''
        source_tot = 0 
        for item in plants_parts_data[:]:
            source_tot += int(item['sources_num'])
        html_table_body += f'''</tbody>'''
        html_article += f'''
            <section>
                <h2>
                    Preparations
                </h2>
                {names_text}
                <table>
                  <thead>
                    <tr>
                      <th>Preparations</th>
                      <th>Sources</th>
                      <th>Consensus</th>
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

def gen():
    plants_rows = masterize_utils.masterize_plants_get_all()
    for plant_row in plants_rows[:]:
        print(plant_row)
        plant_listing_page_gen_new(plant_row[1])

