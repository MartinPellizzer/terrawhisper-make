import textwrap

from neo4j import GraphDatabase

from lib import g
from lib import io
from lib import polish
from lib import components
from lib import sections

uri = "bolt://localhost:7687"
username = "neo4j"
password = "Newoliark1"

driver = GraphDatabase.driver(uri, auth=(username, password))

def plants__plant__gen():
    # GET PLANTS
    '''
    plants_taxon_names = []
    with driver.session() as session:
        tx = session.begin_transaction()
        query = """
            MATCH (s:Plant)
            RETURN s.name
        """
        result = tx.run(query)
        for record in result:
            plants_taxon_names.append(record['s.name'])
        tx.commit()
    '''

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
        '''
        # GET FAMILY
        key = 'taxonomy_family'
        if key not in json_article: json_article[key] = ''
        if regen: json_article[key] = ''
        if dispel: 
            json_article[key] = ''
            io.json_write(json_article_filepath, json_article)
        if not dispel:
            if json_article[key] == '':
                with driver.session() as session:
                    tx = session.begin_transaction()
                    query = """
                        MATCH (s:Plant {name: $plant_taxon_name})-[:HAS_FAMILY]->(o:Family)
                        RETURN o.name
                    """
                    result = tx.run(query, plant_taxon_name=plant_taxon_name)
                    record = result.single()
                    item = record['o.name'] if record else None
                    json_article[key] = item
                    io.json_write(json_article_filepath, json_article)
                    tx.commit()
        '''


        ########################################
        # html
        ########################################
        html_article = ''
        html_article += f'''
            <h1>
                {plant_taxon_name}
            </h1>
            <ul>
                <li>Kingdom: {json_article['kingdom']}</li>
                <li>Phylum: {json_article['phylum']}</li>
                <li>Class: {json_article['class']}</li>
                <li>Order: {json_article['order']}</li>
                <li>Family: {json_article['family']}</li>
                <li>Genus: {json_article['genus']}</li>
                <li>Species: {json_article['species']}</li>
            </ul>
        '''
        meta_title = f'{plant_taxon_name}'
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
        with open(html_filepath, 'w') as f: f.write(html)
        # quit()

def main():
    plants__plant__gen()

main()

