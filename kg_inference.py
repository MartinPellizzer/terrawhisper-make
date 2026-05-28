import os
import json
import shutil
import sqlite3
import textwrap

from neo4j import GraphDatabase

from lib import g
from lib import io
from lib import kg
from lib import llm
from lib import data
from lib import utils
from lib import polish
from lib import components
from lib import sections

neo4j_user = io.file_read(f'{g.DATABASE_FOLDERPATH}/neo4j-user.txt').strip()
neo4j_pass = io.file_read(f'{g.DATABASE_FOLDERPATH}/neo4j-pass.txt').strip()

model_filepath = '/home/ubuntu/vault-tmp/llm/gemma-4-26B-A4B-it-UD-Q4_K_XL.gguf'

uri = "bolt://localhost:7687"
username = neo4j_user
password = neo4j_pass
driver = GraphDatabase.driver(uri, auth=(username, password))

shutil.copy2('styles.css', f'{g.website_folderpath}/styles.css')

def neo4j_nodes_get(kind):
    driver = GraphDatabase.driver(uri, auth=(username, password))
    records = []
    with driver.session() as session:
        result = session.run(f"MATCH (n:{kind}) RETURN n")
        for record in result:
            records.append(record['n'])
    driver.close()
    return records

def neo4j_paths_get(node1_kind, node2_kind):
    driver = GraphDatabase.driver(uri, auth=(username, password))
    with driver.session() as session:
        result = session.run(
            "MATCH p = (a:PLANT)-[*]-(b:DISEASE) "
            "RETURN p"
        )
        for record in result:
            path = record["p"]
            print(path)
    driver.close()

def neo4j__get_diseases_by_plant(plant_id):
    driver = GraphDatabase.driver(uri, auth=(username, password))
    diseases = []
    with driver.session() as session:
        query = f"""
            MATCH p=(s:PLANT {{id: "{plant_id}"}})-[*]->(o:DISEASE) RETURN o;
        """
        # print(query)
        result = session.run(query)
        for record in result:
            path = record["o"]
            disease = path['id']
            diseases.append(disease)
            # print(disease)
            # for node in path.nodes:
                # print(dict(node))
    driver.close()
    return diseases

def plants__plant__gen():
    def get_species_hierarchy(tx):
        query = """
        MATCH (s:Taxon {taxonRank: "species"})
        OPTIONAL MATCH (s)-[:PARENT_TAXON]->(g:Taxon)
        OPTIONAL MATCH (g)-[:PARENT_TAXON]->(f:Taxon)
        OPTIONAL MATCH (f)-[:PARENT_TAXON]->(o:Taxon)
        OPTIONAL MATCH (o)-[:PARENT_TAXON]->(c:Taxon)
        OPTIONAL MATCH (c)-[:PARENT_TAXON]->(p:Taxon)
        OPTIONAL MATCH (p)-[:PARENT_TAXON]->(k:Taxon)
        RETURN
            s.scientificName AS species,
            g.scientificName AS genus,
            f.scientificName AS family,
            o.scientificName AS order,
            c.scientificName AS class,
            p.scientificName AS phylum,
            k.scientificName AS kingdom
        """
        result = tx.run(query)
        return [
            record.data()
            for record in result
        ]
    with driver.session() as session:
        taxonomy_rows = session.execute_read(get_species_hierarchy)
    for taxonomy_row_i, taxonomy_row in enumerate(taxonomy_rows):
        print(f'{taxonomy_row_i}/{len(taxonomy_rows)} - {taxonomy_row}')
        species = taxonomy_row['species']
        genus = taxonomy_row['genus']
        family = taxonomy_row['family']
        order = taxonomy_row['order']
        clazz = taxonomy_row['class']
        phylum = taxonomy_row['phylum']
        kingdom = taxonomy_row['kingdom']
        plant_taxon_name = species
        plant_slug = polish.sluggify(plant_taxon_name)
        url_slug = f'herbs/{plant_slug}'
        ########################################
        # json
        ########################################
        ### json init
        json_article_filepath = f'''{g.DATABASE_FOLDERPATH}/json/{url_slug}.json'''
        json_article = io.json_read(json_article_filepath, create=True)
        json_article['url_slug'] = url_slug
        json_article['plant_slug'] = plant_slug
        json_article['plant_taxon_name'] = plant_taxon_name
        json_article['species'] = species
        json_article['genus'] = genus
        json_article['family'] = family
        json_article['order'] = order
        json_article['class'] = clazz
        json_article['phylum'] = phylum
        json_article['kingdom'] = kingdom
        json_article['article_title'] = plant_taxon_name
        io.json_write(json_article_filepath, json_article)
        regen = False
        dispel = False
        key = 'taxonomy'
        if key not in json_article: json_article[key] = ''
        if regen: json_article[key] = ''
        if dispel: 
            json_article[key] = ''
            io.json_write(json_article_filepath, json_article)
        if not dispel:
            if json_article[key] == '':
                prompt = textwrap.dedent(f'''
                    Write a paragraph about the taxonomy of this plant: {species}.
                    Use the following data:
                    - kingdom {kingdom}
                    - phylum {phylum}
                    - class {clazz}
                    - order {order}
                    - family {family}
                    - genus {genus}
                    - species {species}
                    Guidelines:
                    Start with the following words: {species} belongs .
                ''').strip()
                print(prompt)
                reply = llm.reply(prompt, model_filepath)
                if '</think>' in reply:
                    reply = reply.split('</think>')[1].strip()
                reply = polish.vanilla(reply)
                json_article[key] = reply
                io.json_write(json_article_filepath, json_article)

        ########################################
        # html
        ########################################
        html_article = ''
        html_article += f'''
            <h1>
                {plant_taxon_name}
            </h1>
            <section>
                <h2>
                    What's the taxonomical classification of {species}?
                </h2>
                <p>
                    {json_article['taxonomy']}
                </p>
                <table>
                  <thead>
                    <tr>
                      <th>Taxonomic Rank</th>
                      <th>Classification</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr>
                      <td>Kingdom</td>
                      <td>{json_article['kingdom']}</td>
                    </tr>
                    <tr>
                      <td>Phylum</td>
                      <td>{json_article['phylum']}</td>
                    </tr>
                    <tr>
                      <td>Class</td>
                      <td>{json_article['class']}</td>
                    </tr>
                    <tr>
                      <td>Order</td>
                      <td>{json_article['order']}</td>
                    </tr>
                    <tr>
                      <td>Family</td>
                      <td>{json_article['family']}</td>
                    </tr>
                    <tr>
                      <td>Genus</td>
                      <td>{json_article['genus']}</td>
                    </tr>
                    <tr>
                      <td>Species</td>
                      <td>{json_article['species']}</td>
                    </tr>
                  </tbody>
                </table>
            </section>
        '''
        meta_title = f'{plant_taxon_name}'
        meta_description = ''
        canonical_html = f'''<link rel="canonical" href="https://terrawhisper.com/{url_slug}.html">'''
        head_html = components.html_head(
            meta_title, meta_description, css='/styles.css', canonical=canonical_html
        )

        html = textwrap.dedent(f''' 
            <!DOCTYPE html>
            <html lang="en">
            {head_html}
            <body>
                {sections.header_default()}
                <main class="article">
                    {sections.breadcrumbs_new(url_slug)}
                    <article class="container-md">
                        {html_article}
                    </article>
                </main>
                {sections.footer()}
            </body>
            </html>
        ''').strip()
        html_filepath = f'''{g.website_folderpath}/{url_slug}.html'''
        with open(html_filepath, 'w') as f: f.write(html)
        # quit()

def plants__plant():
    import textwrap
    rows = data.sqlite3__wikidata_powo_get_all()
    rows = [row for row in rows if row[-1] == 'SPECIES']

    study_plants = kg.neo4j__study_plants_get()
    '''
    for study_plant in study_plants:
        print(study_plant)
    print(len(study_plants))
    print(rows[0])
    found_count = 0
    for row_i, row in enumerate(rows):
        print(row_i)
        plant_name = row[-2]
        for study_plant in study_plants:
            if study_plant.lower().strip() == plant_name.lower().strip():
                found_count += 1
    print(found_count)
    quit()
    '''

    ###
    images_found = 0
    for row_i, row in enumerate(rows):
        print(row_i)
        plant_name = row[-2]
        plant_kingdom = row[3]
        plant_phylum = row[4]
        plant_class = row[5]
        plant_subclass = row[6]
        plant_order = row[7]
        plant_family = row[8]
        plant_genus = row[9]
        plant_species = row[10]
        plant_slug = polish.sluggify(plant_name)
        url_slug = f'herbs/{plant_slug}'
        image_filepath = f"{g.WEBSITE_FOLDERPATH}/images/herbs/{plant_slug}.jpg"
        print(image_filepath)
        if os.path.exists(image_filepath):
            images_found += 1
        print(images_found)

        ########################################
        # llm data
        ########################################
        herb_llm_data = io.json_read(f'{g.SSOT_FOLDERPATH}/herbs/herbs-wiki-powo-species/{plant_slug}.json')

        ########################################
        # json
        ########################################
        ### json init
        json_article_filepath = f'''{g.DATABASE_FOLDERPATH}/json/{url_slug}.json'''
        json_article = io.json_read(json_article_filepath, create=True)
        json_article['url_slug'] = url_slug
        json_article['plant_slug'] = plant_slug
        json_article['plant_name'] = plant_name
        json_article['kingdom'] = plant_kingdom
        json_article['phylum'] = plant_phylum
        json_article['class'] = plant_class
        json_article['subclass'] = plant_subclass
        json_article['order'] = plant_order
        json_article['family'] = plant_family
        json_article['genus'] = plant_genus
        json_article['species'] = plant_species
        json_article['article_title'] = plant_name
        io.json_write(json_article_filepath, json_article)

        regen_function = False
        dispel_function = False

        def section_gen(key_base, key_item, relationship_slug, topic, start_words, neo4j_data, study_node_1, study_node_2):
            regen = regen_function
            dispel = dispel_function
            key_base_name = key_base.replace('_', ' ')
            ################################################################################ 
            # NEO4J
            ################################################################################ 
            if neo4j_data:
                # TODO: separate first prompt, extract best items, save to a "key" list, use this list for html
                # STUDY LIST
                regen = regen_function
                dispel = dispel_function
                key_list = f'{key_base}_study_list'
                if key_list not in json_article: json_article[key_list] = ''
                if regen: json_article[key_list] = ''
                if dispel: 
                    json_article[key_list] = ''
                    io.json_write(json_article_filepath, json_article)
                    return 0
                if not dispel:
                    if json_article[key_list] == '':
                        names = [item[key_item] for item in neo4j_data]
                        names_unique = sorted(list(set(names)))
                        names_unique_prompt = '\n'.join(names_unique)
                        prompt = textwrap.dedent(f'''
                            Extract from the list below the 5 most relevant items about this topic:
                            {topic}
                            Reply only with the 5 {key_base_name}. Don't include additional text.
                            Here's the list of {key_base_name} to extract the most relevant 5 ones for the above topic:
                            {names_unique_prompt}
                        ''').strip()
                        reply = llm.reply(prompt, model_filepath)
                        if '</think>' in reply:
                            reply = reply.split('</think>')[1].strip()
                        reply = polish.vanilla(reply)
                        print(prompt)
                        json_article[key_list] = reply
                        io.json_write(json_article_filepath, json_article)

                # STUDY PARAGRAPH
                regen = regen_function
                dispel = dispel_function
                key = f'{key_base}_study_raw'
                if key not in json_article: json_article[key] = ''
                if regen: json_article[key] = ''
                if dispel: 
                    json_article[key] = ''
                    io.json_write(json_article_filepath, json_article)
                    return 0
                if not dispel:
                    if json_article[key] == '':
                        names = [item[key_item] for item in neo4j_data]
                        names_unique = sorted(list(set(names)))
                        names_unique_prompt = '\n'.join(names_unique)
                        prompt = textwrap.dedent(f'''
                            Extract from the list below the 5 most relevant items about this topic:
                            {topic}
                            Reply only with the 5 {key_base_name}. Don't include additional text.
                            Here's the list of {key_base_name} to extract the most relevant 5 ones for the above topic:
                            {names_unique_prompt}
                        ''').strip()
                        reply = llm.reply(prompt, model_filepath)
                        if '</think>' in reply:
                            reply = reply.split('</think>')[1].strip()
                        reply = polish.vanilla(reply)
                        print(prompt)
                        names_selected_prompt = reply
                        names_selected = []
                        for line in reply.split('\n'):
                            line = line.strip()
                            if line == '': continue
                            if len(line) < 2: continue
                            if line[0].isdigit(): line = line[1:]
                            if line[0] == '.': line = line[1:]
                            line = line.strip()
                            if line == '': continue
                            names_selected.append(line)
                        print('########################################')
                        print(reply)
                        print('########################################')
                        prompt = textwrap.dedent(f'''
                            Write a paragraph in 4-6 sentences about the following topic: 
                            {topic}
                            Include the following {key_base_name}: {names_selected_prompt}.
                            The first sentence must answer in the most direct, clear, detailed way possible without fluff.
                            The following sentences must give more details about this topic.
                            Don't give me bold or italicized text. 
                            Reply only with the content.
                            Start the reply with the following words: "{start_words}"
                        ''').strip()
                        reply = llm.reply(prompt, model_filepath)
                        if '</think>' in reply:
                            reply = reply.split('</think>')[1].strip()
                        reply = polish.vanilla(reply)
                        print('########################################')
                        print(reply)
                        print('########################################')
                        json_article[key] = reply
                        io.json_write(json_article_filepath, json_article)
                        ### STUDY SOURCE
                        key = f'{key_base}_study_source_raw'
                        for name in names_selected:
                            found = False
                            for neo4j_item in neo4j_data:
                                print(f'{neo4j_item[key_item].lower().strip()} == {name.lower().strip()}')
                                if neo4j_item[key_item].lower().strip() == name.lower().strip():
                                    print(neo4j_item, name)
                                    source_id = neo4j_item['source']
                                    ### TODO: remove try/except when fixing missing jsons
                                    try: 
                                        study_filepath = f'{g.SSOT_FOLDERPATH}/studies/extraction/{study_node_1}-{relationship_slug}-{study_node_2}/{source_id}.json'
                                        print(study_filepath)
                                        study_data = io.json_read(study_filepath)
                                    except: break
                                    study_folderpath = f'{g.VAULT_FOLDERPATH}/terrawhisper/studies/pubmed/medicinal-plant/json'
                                    study_filepath = f'{study_folderpath}/{source_id}.json'
                                    study_items = io.json_read(study_filepath)
                                    try: article_data = study_items['PubmedArticle'][0]['MedlineCitation']['Article']
                                    except: pass
                                    try: journal_title = article_data['Journal']['Title']
                                    except: pass
                                    prompt = textwrap.dedent(f'''
                                        Write a paragraph in 4-6 sentences about the following topic: 
                                        {topic}.
                                        Use only exclusively the content from the SCIENTIFIC STUDY below.
                                        Focus only on info and data related to the plant {plant_name}.
                                        Don't mention other plants.
                                        Incluse as many numbers as possible.
                                        Don't give me bold or italicized text. 
                                        Reply only with the content.
                                        Start the reply with the following words: According to a study published by "{journal_title}", 
                                        SCIENTIFIC STUDY:
                                        {study_data['title']} 
                                        {study_data['abstract']}
                                    ''').strip()
                                    reply = llm.reply(prompt, model_filepath)
                                    if '</think>' in reply:
                                        reply = reply.split('</think>')[1].strip()
                                    reply = polish.vanilla(reply)
                                    json_article[key] = reply
                                    io.json_write(json_article_filepath, json_article)
                                    print('########################################')
                                    print(reply)
                                    print('########################################')
                                    print(json_article_filepath)
                                    found = True
                                    break
                            if found:
                                break

            ################################################################################ 
            # LIST
            ################################################################################ 
            elif f'{key_base}_llm_list_1_try_hint' in herb_llm_data and herb_llm_data[f'{key_base}_llm_list_1_try_hint'] != '':
                key = f'{key_base}_llm_list_1_try_hint'
                if key not in json_article: json_article[key] = ''
                if regen: json_article[key] = ''
                if dispel: 
                    json_article[key] = ''
                    io.json_write(json_article_filepath, json_article)
                    return 0
                if not dispel:
                    if json_article[key] == '':
                        names = [item['answer'] for item in herb_llm_data[f'{key_base}_llm_list_1_try_hint']]
                        names = ', '.join(names)
                        prompt = textwrap.dedent(f'''
                            Write a paragraph in 4-6 sentences about the following topic:
                            {topic}
                            Include the following {key_base_name}: {names}.
                            The first sentence must answer in the most direct, clear, detailed way possible without fluff.
                            The following sentences must give more details about this topic.
                            Don't give me bold or italicized text. 
                            Reply only with the content.
                            Start the reply with the following words: "{start_words}"
                        ''').strip()
                        reply = llm.reply(prompt, model_filepath)
                        if '</think>' in reply:
                            reply = reply.split('</think>')[1].strip()
                        reply = polish.vanilla(reply)
                        json_article[key] = reply
                        io.json_write(json_article_filepath, json_article)

            ################################################################################ 
            # PARAGRAPH
            ################################################################################ 
            else:
                key = f'{key_base}'
                if key not in json_article: json_article[key] = ''
                if regen: json_article[key] = ''
                if dispel: 
                    json_article[key] = ''
                    io.json_write(json_article_filepath, json_article)
                    return 0
                if not dispel:
                    if json_article[key] == '':
                        prompt = textwrap.dedent(f'''
                            Write a paragraph in 4-6 sentences about the following topic: 
                            {topic}
                            The first sentence must answer in the most direct, clear, detailed way possible without fluff.
                            The following sentences must give more details about this topic.
                            Don't give me bold or italicized text. 
                            Reply only with the content.
                            Start the reply with the following words: "{start_words}"
                        ''').strip()
                        reply = llm.reply(prompt, model_filepath)
                        if '</think>' in reply:
                            reply = reply.split('</think>')[1].strip()
                        reply = polish.vanilla(reply)
                        json_article[key] = reply
                        io.json_write(json_article_filepath, json_article)
                        # FORMAT 1N1
                        reply_format_1N1 = utils.format_1N1(reply)
                        json_article[f'{key_base}_format_1N1'] = reply_format_1N1
                        io.json_write(json_article_filepath, json_article)

        section_gen(
            key_base=f'cultivation',
            key_item=f'cultivation',
            relationship_slug='',
            topic=f'cultivation of the plant {plant_name}',
            start_words=f'This plant ',
            neo4j_data='',
            study_node_1=f'',
            study_node_2=f'',
        )
        '''
        res = section_gen(
            key_base=f'pharmacological_activities',
            key_item=f'pharmacological_activity',
            relationship_slug='has_pharmacological_activity',
            topic=f'pharmacological activities the plant {plant_name} has',
            start_words=f'This plant has ',
            neo4j_data=kg.neo4j__get_rows(plant_name, 'PLANT', 'HAS_PHARMACOLOGICAL_ACTIVITY', 'PHARMACOLOGICAL_ACTIVITY', 'plant', 'pharmacological_activity'),
            study_node_1=f'plant-name',
            study_node_2=f'pharmacological-activity-name',
        )
        if res == 0:
            continue
        res = section_gen(
            key_base=f'compounds',
            key_item=f'compound',
            relationship_slug=f'contains',
            topic=f'medicinal compounds the plant {plant_name} contains',
            start_words=f'This plant contains',
            neo4j_data=kg.neo4j__get_plant_compounds(plant_name),
            study_node_1=f'plant-name',
            study_node_2=f'medicinal-compound-name',
        )
        if res == 0:
            continue
        res = section_gen(
            key_base=f'conditions',
            key_item=f'condition',
            relationship_slug=f'used_for',
            topic=f'health contitions the plant {plant_name} is used for',
            start_words=f'This plant is used for ',
            neo4j_data=kg.neo4j__get_plant_conditions(plant_name),
            study_node_1=f'plant-name',
            study_node_2=f'health-condition-name',
        )
        if res == 0:
            continue

        '''
        regen = regen_function
        dispel = dispel_function
        key = 'taxonomy'
        if key not in json_article: json_article[key] = ''
        if regen: json_article[key] = ''
        if dispel: 
            json_article[key] = ''
            io.json_write(json_article_filepath, json_article)
        if not dispel:
            if json_article[key] == '':
                prompt = textwrap.dedent(f'''
                    Write a paragraph about the taxonomy of this plant: {plant_name}.
                    Use the following data:
                    - kingdom {plant_kingdom}
                    - phylum {plant_phylum}
                    - class {plant_class}
                    - subclass {plant_subclass}
                    - order {plant_order}
                    - family {plant_family}
                    - genus {plant_genus}
                    - species {plant_species}
                    Guidelines:
                    Start with the following words: {plant_name} belongs .
                ''').strip()
                print(prompt)
                reply = llm.reply(prompt, model_filepath)
                if '</think>' in reply:
                    reply = reply.split('</think>')[1].strip()
                reply = polish.vanilla(reply)
                json_article[key] = reply
                io.json_write(json_article_filepath, json_article)

        regen = regen_function
        dispel = dispel_function
        key = 'morphology'
        if key not in json_article: json_article[key] = ''
        if regen: json_article[key] = ''
        if dispel: 
            json_article[key] = ''
            io.json_write(json_article_filepath, json_article)
            continue
        if not dispel:
            if json_article[key] == '':
                import textwrap
                prompt = textwrap.dedent(f'''
                    Write a paragraph in 4-6 sentences about the morphology of this plant: {plant_name}.
                    The first sentence must answer in the most direct, clear, detailed way possible without fluff.
                    The following sentences must give more details about this topic.
                    Don't give me bold or italicized text. 
                    Reply only with the content.
                    Start the reply with the following words: "{plant_name} has "
                    /no_think
                ''').strip()
                reply = llm.reply(prompt, model_filepath)
                if '</think>' in reply:
                    reply = reply.split('</think>')[1].strip()
                reply = polish.vanilla(reply)
                json_article[key] = reply
                io.json_write(json_article_filepath, json_article)
                print(json_article_filepath)

        regen = regen_function
        dispel = dispel_function
        key = 'distribution'
        if key not in json_article: json_article[key] = ''
        if regen: json_article[key] = ''
        if dispel: 
            json_article[key] = ''
            io.json_write(json_article_filepath, json_article)
            continue
        if not dispel:
            if json_article[key] == '':
                import textwrap
                prompt = textwrap.dedent(f'''
                    Write a paragraph in 4-6 sentences about the geographical distribution of this plant: {plant_name}.
                    The first sentence must answer in the most direct, clear, detailed way possible without fluff.
                    The following sentences must give more details about this topic.
                    Don't give me bold or italicized text. 
                    Reply only with the content.
                    Start the reply with the following words: "This plant is "
                    /no_think
                ''').strip()
                reply = llm.reply(prompt, model_filepath)
                if '</think>' in reply:
                    reply = reply.split('</think>')[1].strip()
                reply = polish.vanilla(reply)
                json_article[key] = reply
                io.json_write(json_article_filepath, json_article)
                print(json_article_filepath)

        regen = regen_function
        dispel = dispel_function
        key = 'parts'
        if key not in json_article: json_article[key] = ''
        if regen: json_article[key] = ''
        if dispel: 
            json_article[key] = ''
            io.json_write(json_article_filepath, json_article)
        if not dispel:
            if json_article[key] == '':
                import textwrap
                prompt = textwrap.dedent(f'''
                    Write a paragraph in 4-6 sentences about the plant's parts used medicinally of this plant: {plant_name}.
                    The first sentence must answer in the most direct, clear, detailed way possible without fluff.
                    The following sentences must give more details about this topic.
                    Don't give me bold or italicized text. 
                    Reply only with the content.
                    Start the reply with the following words: "{plant_name} contains "
                    /no_think
                ''').strip()
                reply = llm.reply(prompt, model_filepath)
                if '</think>' in reply:
                    reply = reply.split('</think>')[1].strip()
                reply = polish.vanilla(reply)
                json_article[key] = reply
                io.json_write(json_article_filepath, json_article)
                print(json_article_filepath)

        regen = regen_function
        dispel = dispel_function
        key = 'targets__llm_raw'
        if key not in json_article: json_article[key] = ''
        if regen: json_article[key] = ''
        if dispel: 
            json_article[key] = ''
            io.json_write(json_article_filepath, json_article)
        if not dispel:
            if json_article[key] == '':
                import textwrap
                prompt = textwrap.dedent(f'''
                    Write a paragraph in 4-6 sentences about the molecular targets of this plant: {plant_name}.
                    By molecoular targets, I mean mostly what proteins this plant interact with that lead to medicinal effects.
                    The first sentence must answer in the most direct, clear, detailed way possible without fluff.
                    The following sentences must give more details about this topic.
                    Don't give me bold or italicized text. 
                    Reply only with the content.
                    Start the reply with the following words: "{plant_name} targets "
                    /no_think
                ''').strip()
                reply = llm.reply(prompt, model_filepath)
                if '</think>' in reply:
                    reply = reply.split('</think>')[1].strip()
                reply = polish.vanilla(reply)
                json_article[key] = reply
                io.json_write(json_article_filepath, json_article)
                print(json_article_filepath)

        regen = regen_function
        dispel = dispel_function
        if 'ailments_llm_list_1_try_hint' in herb_llm_data and herb_llm_data['ailments_llm_list_1_try_hint'] != '':
            key = 'ailments_llm_list_1_try_hint'
            if key not in json_article: json_article[key] = ''
            if regen: json_article[key] = ''
            if dispel: 
                json_article[key] = ''
                io.json_write(json_article_filepath, json_article)
                continue
            if not dispel:
                if json_article[key] == '':
                    import textwrap
                    hint = [item['answer'] for item in herb_llm_data['ailments_llm_list_1_try_hint']]
                    hint = ', '.join(hint)
                    prompt = textwrap.dedent(f'''
                        Write a paragraph in 4-6 sentences about the common ailments treated with this plant: {plant_name}.
                        Include the following: {hint}.
                        The first sentence must answer in the most direct, clear, detailed way possible without fluff.
                        The following sentences must give more details about this topic.
                        Don't give me bold or italicized text. 
                        Reply only with the content.
                        Start the reply with the following words: "This plant is used to treat "
                        /no_think
                    ''').strip()
                    reply = llm.reply(prompt, model_filepath)
                    if '</think>' in reply:
                        reply = reply.split('</think>')[1].strip()
                    reply = polish.vanilla(reply)
                    json_article[key] = reply
                    io.json_write(json_article_filepath, json_article)
                    print(json_article_filepath)
        else:
            key = 'ailments'
            if key not in json_article: json_article[key] = ''
            if regen: json_article[key] = ''
            if dispel: 
                json_article[key] = ''
                io.json_write(json_article_filepath, json_article)
                continue
            if not dispel:
                if json_article[key] == '':
                    import textwrap
                    prompt = textwrap.dedent(f'''
                        Write a paragraph in 4-6 sentences about the common ailments treated with this plant: {plant_name}.
                        The first sentence must answer in the most direct, clear, detailed way possible without fluff.
                        The following sentences must give more details about this topic.
                        Don't give me bold or italicized text. 
                        Reply only with the content.
                        Start the reply with the following words: "This plant is used to treat "
                        /no_think
                    ''').strip()
                    reply = llm.reply(prompt, model_filepath)
                    if '</think>' in reply:
                        reply = reply.split('</think>')[1].strip()
                    reply = polish.vanilla(reply)
                    json_article[key] = reply
                    io.json_write(json_article_filepath, json_article)
                    print(json_article_filepath)

        regen = regen_function
        dispel = dispel_function
        key = 'preparations'
        if key not in json_article: json_article[key] = ''
        if regen: json_article[key] = ''
        if dispel: 
            json_article[key] = ''
            io.json_write(json_article_filepath, json_article)
            continue
        if not dispel:
            if json_article[key] == '':
                import textwrap
                prompt = textwrap.dedent(f'''
                    Write a paragraph in 4-6 sentences about the herbal preparation forms with this plant: {plant_name}.
                    The first sentence must answer in the most direct, clear, detailed way possible without fluff.
                    The following sentences must give more details about this topic.
                    Don't give me bold or italicized text. 
                    Reply only with the content.
                    Start the reply with the following words: "{plant_name} is prepared "
                    /no_think
                ''').strip()
                reply = llm.reply(prompt, model_filepath)
                if '</think>' in reply:
                    reply = reply.split('</think>')[1].strip()
                reply = polish.vanilla(reply)
                json_article[key] = reply
                io.json_write(json_article_filepath, json_article)
                print(json_article_filepath)

        regen = regen_function
        dispel = dispel_function
        if 'side_effects_llm_list_1_try_hint' in herb_llm_data and herb_llm_data['side_effects_llm_list_1_try_hint'] != '':
            key = 'side_effects_llm_list_1_try_hint'
            if key not in json_article: json_article[key] = ''
            if regen: json_article[key] = ''
            if dispel: 
                json_article[key] = ''
                io.json_write(json_article_filepath, json_article)
            if not dispel:
                if json_article[key] == '':
                    import textwrap
                    hint = [item['answer'] for item in herb_llm_data['side_effects_llm_list_1_try_hint']]
                    hint = ', '.join(hint)
                    prompt = textwrap.dedent(f'''
                        Write a paragraph in 4-6 sentences about the possible side effects of this plant: {plant_name}.
                        Include the following: {hint}.
                        The first sentence must answer in the most direct, clear, detailed way possible without fluff.
                        The following sentences must give more details about this topic.
                        Don't give me bold or italicized text. 
                        Reply only with the content.
                        Start the reply with the following words: "This plant can "
                        /no_think
                    ''').strip()
                    reply = llm.reply(prompt, model_filepath)
                    if '</think>' in reply:
                        reply = reply.split('</think>')[1].strip()
                    reply = polish.vanilla(reply)
                    json_article[key] = reply
                    io.json_write(json_article_filepath, json_article)
                    print(json_article_filepath)
        else:
            key = 'side_effects'
            if key not in json_article: json_article[key] = ''
            if regen: json_article[key] = ''
            if dispel: 
                json_article[key] = ''
                io.json_write(json_article_filepath, json_article)
            if not dispel:
                if json_article[key] == '':
                    import textwrap
                    prompt = textwrap.dedent(f'''
                        Write a paragraph in 4-6 sentences about the therapeutic actions of this plant: {plant_name}.
                        The first sentence must answer in the most direct, clear, detailed way possible without fluff.
                        The following sentences must give more details about this topic.
                        Don't give me bold or italicized text. 
                        Reply only with the content.
                        Start the reply with the following words: "{plant_name} has "
                        /no_think
                    ''').strip()
                    reply = llm.reply(prompt, model_filepath)
                    if '</think>' in reply:
                        reply = reply.split('</think>')[1].strip()
                    reply = polish.vanilla(reply)
                    json_article[key] = reply
                    io.json_write(json_article_filepath, json_article)
                    print(json_article_filepath)

        regen = regen_function
        dispel = dispel_function
        if 'preparations_llm_list_1_try_hint' in herb_llm_data and herb_llm_data['preparations_llm_list_1_try_hint'] != '':
            key = 'preparations_llm_list_1_try_hint'
            if key not in json_article: json_article[key] = ''
            if regen: json_article[key] = ''
            if dispel: 
                json_article[key] = ''
                io.json_write(json_article_filepath, json_article)
            if not dispel:
                if json_article[key] == '':
                    import textwrap
                    hint = [item['answer'] for item in herb_llm_data['preparations_llm_list_1_try_hint']]
                    hint = ', '.join(hint)
                    prompt = textwrap.dedent(f'''
                        Write a paragraph in 4-6 sentences about the herbal preparations of this plant: {plant_name}.
                        Include the following: {hint}.
                        The first sentence must answer in the most direct, clear, detailed way possible without fluff.
                        The following sentences must give more details about this topic.
                        Don't give me bold or italicized text. 
                        Reply only with the content.
                        Start the reply with the following words: "This plant can "
                        /no_think
                    ''').strip()
                    reply = llm.reply(prompt, model_filepath)
                    if '</think>' in reply:
                        reply = reply.split('</think>')[1].strip()
                    reply = polish.vanilla(reply)
                    json_article[key] = reply
                    io.json_write(json_article_filepath, json_article)
                    print(json_article_filepath)
        else:
            key = 'preparations'
            if key not in json_article: json_article[key] = ''
            if regen: json_article[key] = ''
            if dispel: 
                json_article[key] = ''
                io.json_write(json_article_filepath, json_article)
            if not dispel:
                if json_article[key] == '':
                    import textwrap
                    prompt = textwrap.dedent(f'''
                        Write a paragraph in 4-6 sentences about the therapeutic actions of this plant: {plant_name}.
                        The first sentence must answer in the most direct, clear, detailed way possible without fluff.
                        The following sentences must give more details about this topic.
                        Don't give me bold or italicized text. 
                        Reply only with the content.
                        Start the reply with the following words: "{plant_name} has "
                        /no_think
                    ''').strip()
                    reply = llm.reply(prompt, model_filepath)
                    if '</think>' in reply:
                        reply = reply.split('</think>')[1].strip()
                    reply = polish.vanilla(reply)
                    json_article[key] = reply
                    io.json_write(json_article_filepath, json_article)
                    print(json_article_filepath)


        ########################################
        # html
        ########################################
        def html_section_gen(key_slug, heading, list_intro):
            key_raw = key_slug
            key_list = f'{key_slug}_llm_list_1_try_hint'
            key_study = f'{key_slug}_study_raw'
            key_study_source = f'{key_slug}_study_source_raw'
            key_study_list = f'{key_slug}_study_list'
            html_list = ''
            html_paragraph = ''
            html_score = f'''
                <div class="reliability-1" aria-label="Reliability score 1 out of 5">
                    Evidence Level: ★☆☆☆☆
                </div>
            '''
            ### STUDY
            if key_study in json_article and json_article[key_study] != '':
                ### STUDY PARAGRAPH
                html_paragraph = f'<p>{json_article[key_study]}</p>'
                ### STUDY SOURCE
                try: html_paragraph += f'<p>{json_article[key_study_source]}</p>'
                except: pass
                ### STUDY LIST
                if key_study_list in json_article and json_article[key_study_list] != '':
                    items = json_article[key_study_list].split('\n')
                    html_list += f'<p>{list_intro}</p>'
                    html_list += f'<ul>'
                    for item in items:
                        html_list += f'<li>{item}</li>'
                    html_list += f'</ul>'
                ### STUDY RELIABILITY
                html_score = f'''
                    <div class="reliability-3" aria-label="Reliability score 3 out of 5">
                        Evidence Level: ★★★☆☆
                    </div>
                '''
            ### NO STUDY
            else:
                ### LIST
                if key_list in herb_llm_data and herb_llm_data[key_list] != '':
                    html_list += f'<p>{list_intro}</p>'
                    html_list += f'<ul>'
                    for item in herb_llm_data[key_list]:
                        html_list += f'''<li>{item['answer'].capitalize()}</li>'''
                    html_list += f'</ul>'
                ### PARAGRAPH LIST
                if key_list in json_article and json_article[key_list] != '':
                    # html_paragraph = utils.format_1N1(json_article[key_list])
                    html_paragraph = f'<p>{json_article[key_list]}</p>'
                ### PARAGRAPH RAW
                else:
                    key_format_1N1 = f'{key_slug}_format_1N1'
                    if key_format_1N1 in json_article and json_article[key_format_1N1] != '':
                        html_paragraph = json_article[key_format_1N1]
                    else:
                        html_paragraph = f'<p>{json_article[key_raw]}</p>'
            html_section = f'''
                <section>
                    <h2>{heading}</h2>
                    {html_paragraph}
                    {html_list}
                    {html_score}
                </secton>
            '''
            return html_section

        html_article = f'''
            <h1>
                {plant_name}
            </h1>
            <img src="/images/herbs/{plant_slug}.jpg">
        '''
        html_article += f'''
            <section>
                <h2>
                    What's the taxonomical classification of {plant_name}?
                </h2>
                <p>
                    {json_article['taxonomy']}
                </p>
                <table style="margin-bottom: 1.6rem;">
                  <thead>
                    <tr>
                      <th>Taxonomic Rank</th>
                      <th>Classification</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr>
                      <td>Kingdom</td>
                      <td>{json_article['kingdom']}</td>
                    </tr>
                    <tr>
                      <td>Phylum</td>
                      <td>{json_article['phylum']}</td>
                    </tr>
                    <tr>
                      <td>Class</td>
                      <td>{json_article['class']}</td>
                    </tr>
                    <tr>
                      <td>Subclass</td>
                      <td>{json_article['subclass']}</td>
                    </tr>
                    <tr>
                      <td>Order</td>
                      <td>{json_article['order']}</td>
                    </tr>
                    <tr>
                      <td>Family</td>
                      <td>{json_article['family']}</td>
                    </tr>
                    <tr>
                      <td>Genus</td>
                      <td>{json_article['genus']}</td>
                    </tr>
                    <tr>
                      <td>Species</td>
                      <td>{json_article['species']}</td>
                    </tr>
                  </tbody>
                </table>
                <div class="reliability-4" aria-label="Reliability score 4 out of 5">
                    Evidence Level: ★★★★☆
                </div>
            </section>
        '''

        html_article += html_section_gen(
            key_slug = f'morphology', 
            heading = f'What are the morphological characteristics of this plant?',
            list_intro = f'The morphological characteristics of this plant are shown in the list below.', 
        )
        html_article += html_section_gen(
            key_slug = f'distribution', 
            heading = f'What is the geographical distribution of this plant?',
            list_intro = f'The geographical distribution of this plant is shown in the list below.',
        )
        html_article += html_section_gen(
            key_slug = f'cultivation', 
            heading = f'How is this plant cultivated?',
            list_intro = f'The geographical distribution of this plant is shown in the list below.',
        )
        html_article += html_section_gen(
            key_slug = f'parts', 
            heading = f'What parts of this plant are used medicinally?',
            list_intro = f'The parts of this plant that are ued medicinally are shown in the list below.',
        )
        html_article += html_section_gen(
            key_slug = f'pharmacological_activities', 
            heading = f'What are the pharmacological activities of {plant_name}?',
            list_intro = f'The primary pharmacological activities of this plant are shown in the list below.',
        )
        html_article += html_section_gen(
            key_slug = f'compounds', 
            heading = f'What medicinal compounds this plant contains?',
            list_intro = f'The primary medicinal compounds of this plant are shown in the list below.',
        )
        html_article += html_section_gen(
            key_slug = f'conditions', 
            heading = f'What health conditions is this plant used for?',
            list_intro = f'The main health conditions this plant is used for are shown in the list below.',
        )
        html_article += html_section_gen(
            key_slug = f'preparations', 
            heading = f'What are the herbal preparations of this plant?',
            list_intro = f'The main herbal preparations of this plant are shown in the list below.',
        )
        html_article += html_section_gen(
            key_slug = f'side_effects', 
            heading = f'What side effects this plant can have?',
            list_intro = f'The main side effects this plant can have are shown in the list below.',
        )

        '''
            <section>
                <h2>What are the molecular targets of this plant?</h2>
                <p>
                    {json_article['targets__llm_raw']}
                </p>
            </section>
        html_article += html_section_gen(
            key_slug = f'ailments', 
            heading = f'What common ailments are treated using this plant?',
            list_intro = f'The main common ailment treated using this plant are shown in the list below.',
        )
        '''
            # {html_ailments}

        meta_title = f'{plant_name}'
        meta_description = ''
        canonical_html = f'''<link rel="canonical" href="https://terrawhisper.com/{url_slug}.html">'''
        head_html = components.html_head(
            meta_title, meta_description, css='/styles.css', canonical=canonical_html
        )
        html = textwrap.dedent(f''' 
            <!DOCTYPE html>
            <html lang="en">
            {head_html}
            <body>
                {sections.header_default()}
                <main class="article">
                    {sections.breadcrumbs_new(url_slug)}
                    <article>
                        {html_article}
                    </article>
                </main>
                {sections.footer()}
            </body>
            </html>
        ''').strip()
        html_filepath = f'''{g.website_folderpath}/{url_slug}.html'''
        with open(html_filepath, 'w') as f: f.write(html)
        print(html_filepath)
        # quit()

def plants__families__gen():
    def neo4j_families_get(tx):
        query = """
            MATCH (s:Taxon {taxonRank: "family"}) RETURN s
        """
        result = tx.run(query)
        return [
            record.data()['s']
            for record in result
        ]
    with driver.session() as session:
        families_rows = session.execute_read(neo4j_families_get)
    url_slug = f'herbs/families'
    links_html = ''
    links_html += '<ul>'
    for family_row in families_rows:
        family_scientific_name = family_row['scientificName']
        family_taxon_rank = family_row['taxonRank']
        family_slug = polish.sluggify(family_scientific_name)
        links_html += f'''<li><a href="/{url_slug}/{family_slug}.html">{family_scientific_name}</a></li>'''
    links_html += '</ul>'
    ########################################
    # json
    ########################################
    ### json init
    json_article_filepath = f'''{g.DATABASE_FOLDERPATH}/json/{url_slug}.json'''
    json_article = io.json_read(json_article_filepath, create=True)
    json_article['url_slug'] = url_slug
    json_article['article_title'] = f'''Families'''
    io.json_write(json_article_filepath, json_article)
    regen = False
    dispel = False
    ########################################
    # html
    ########################################
    html_article = ''
    html_article += f'''
        <h1>
            {family_scientific_name}
        </h1>
        {links_html}
    '''
    meta_title = f'Families'
    meta_description = ''
    canonical_html = f'''<link rel="canonical" href="https://terrawhisper.com/{url_slug}.html">'''
    head_html = components.html_head(
        meta_title, meta_description, css='/styles-herb-monograph.css', canonical=canonical_html
    )
    html = textwrap.dedent(f''' 
        <!DOCTYPE html>
        <html lang="en">
        {head_html}
        <body>
            {sections.header_default()}
            {sections.breadcrumbs_new(url_slug)}
            <div class="hub">
                <main>
                    <article class="container-md">
                        {html_article}
                    </article>
                </main>
            </div>
            {sections.footer()}
        </body>
        </html>
    ''').strip()
    html_filepath = f'''{g.website_folderpath}/{url_slug}.html'''
    io.folder_create_from_filepath(html_filepath)
    # print(html_filepath)
    with open(html_filepath, 'w') as f: f.write(html)
    # quit()

def plants__families__family__gen():
    def families_get(tx):
        query = """
            MATCH (s:Taxon {taxonRank: "family"}) RETURN s
        """
        result = tx.run(query)
        return [
            record.data()['s']
            for record in result
        ]
    with driver.session() as session:
        families_rows = session.execute_read(families_get)
    ###
    for family_row in families_rows:
        family_scientific_name = family_row['scientificName']
        family_taxon_rank = family_row['taxonRank']
        family_slug = polish.sluggify(family_scientific_name)
        url_slug = f'herbs/families/{family_slug}'
        ########################################
        # json
        ########################################
        ### json init
        json_article_filepath = f'''{g.DATABASE_FOLDERPATH}/json/{url_slug}.json'''
        json_article = io.json_read(json_article_filepath, create=True)
        json_article['url_slug'] = url_slug
        json_article['family_slug'] = family_slug
        json_article['family_scientific_name'] = family_scientific_name
        json_article['family_taxon_rank'] = family_taxon_rank
        json_article['article_title'] = family_scientific_name
        io.json_write(json_article_filepath, json_article)
        regen = False
        dispel = False
        ########################################
        # html
        ########################################
        html_article = ''
        html_article += f'''
            <h1>
                {family_scientific_name}
            </h1>
        '''
        meta_title = f'{family_scientific_name}'
        meta_description = ''
        canonical_html = f'''<link rel="canonical" href="https://terrawhisper.com/{url_slug}.html">'''
        head_html = components.html_head(
            meta_title, meta_description, css='/styles.css', canonical=canonical_html
        )
        html = textwrap.dedent(f''' 
            <!DOCTYPE html>
            <html lang="en">
            {head_html}
            <body>
                {sections.header_default()}
                <main class="article">
                    {sections.breadcrumbs_new(url_slug)}
                    <article class="container-md">
                        {html_article}
                    </article>
                </main>
                {sections.footer()}
            </body>
            </html>
        ''').strip()
        html_filepath = f'''{g.website_folderpath}/{url_slug}.html'''
        io.folder_create_from_filepath(html_filepath)
        # print(html_filepath)
        with open(html_filepath, 'w') as f: f.write(html)
        # quit()

def plants__all__gen():
    driver = GraphDatabase.driver("bolt://localhost:7687", auth=(neo4j_user, neo4j_pass))
    ### get all plants
    terra_plants_ids = []
    with driver.session() as session:
        result = session.run("""
            MATCH (s:Plant) RETURN s;
        """)
        for record in result:
            node = dict(record["s"])
            terra_plants_ids.append(node['id'])
    driver.close()
    ###
    url_slug = f'herbs/all'
    items = []
    for i, terra_plant_id in enumerate(terra_plants_ids):
        print(i)
        plant_name = kg.sqlite3__terra_plant_name_get(terra_plant_id)
        plant_slug = polish.sluggify(plant_name)
        items.append({'plant_name': plant_name, 'plant_slug': plant_slug})
    items = sorted(items, key=lambda x: x['plant_name'], reverse=False)
    ###
    html_links = ''
    html_links += '<ul>'
    for i, item in enumerate(items):
        html_links += f'''<li><a href="/herbs/{item['plant_slug']}.html">{item['plant_name']}</a></li>'''
    html_links += '</ul>'

    ########################################
    # html
    ########################################
    html_article = f'''
        <h1>
            List of All Medicinal Plants
        </h1>
        {html_links}
    '''

    meta_title = f'List of All Medicinal Plants'
    meta_description = ''
    canonical_html = f'''<link rel="canonical" href="https://terrawhisper.com/{url_slug}.html">'''
    head_html = components.html_head(
        meta_title, meta_description, css='/styles.css', canonical=canonical_html
    )
    html = textwrap.dedent(f''' 
        <!DOCTYPE html>
        <html lang="en">
        {head_html}
        <body>
            {sections.header_default()}
            <main class="article">
                {sections.breadcrumbs_new(url_slug)}
                <article>
                    {html_article}
                </article>
            </main>
            {sections.footer()}
        </body>
        </html>
    ''').strip()
    html_filepath = f'''{g.website_folderpath}/{url_slug}.html'''
    with open(html_filepath, 'w') as f: f.write(html)
    print(html_filepath)
    # quit()


def main():
    plants__plant()
    # plants__all__gen()
    # plants__taxonomy__gen()
    # plants__families__gen()
    # plants__families__family__gen()

main()

