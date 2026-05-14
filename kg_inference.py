import os
import shutil
import textwrap
import sqlite3

from neo4j import GraphDatabase

from lib import g
from lib import io
from lib import kg
from lib import llm
from lib import data
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
        key = 'compounds'
        if key not in json_article: json_article[key] = ''
        if regen: json_article[key] = ''
        if dispel: 
            json_article[key] = ''
            io.json_write(json_article_filepath, json_article)
        if not dispel:
            if json_article[key] == '':
                import textwrap
                prompt = textwrap.dedent(f'''
                    Write a paragraph in 4-6 sentences about the medicinal compounds of this plant: {plant_name}.
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
        key = 'diseases'
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
                    Write a paragraph in 4-6 sentences about the diseases treated with this plant: {plant_name}.
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
        key = 'side_effects'
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
                    Write a paragraph in 4-6 sentences about the possible side effects of this plant: {plant_name}.
                    The first sentence must answer in the most direct, clear, detailed way possible without fluff.
                    The following sentences must give more details about this topic.
                    Don't give me bold or italicized text. 
                    Reply only with the content.
                    Start the reply with the following words: "{plant_name} can "
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
        html_article = f'''
            <h1>
                {plant_name}
            </h1>
            <img src="/images/herbs/{plant_slug}.jpg">
            <section>
                <h2>
                    What's the taxonomical classification of {plant_name}?
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
            </section>
            <section class="container-lg" style="margin-top: 4.8rem; border-bottom: 1px solid #e2e8f0; padding-bottom: 3.2rem;">
                <h2>What medicinal compounds this plant contains?</h2>
                <p>
                    {json_article['compounds']}
                </p>
                <h2>What are the therapeutic actions of {plant_name}?</h2>
                <p>
                    {json_article['actions']}
                </p>
                <h2>What diseases this plant treats?</h2>
                <p>
                    {json_article['diseases']}
                </p>
                <h2>What are the herbal preparations of {plant_name}?</h2>
                <p>
                    {json_article['preparations']}
                </p>
                <h2>What side-effects this plant can have?</h2>
                <p>
                    {json_article['side_effects']}
                </p>
            </section>
        '''

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

