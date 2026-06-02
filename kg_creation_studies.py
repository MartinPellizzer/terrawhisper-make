import os
import json
import textwrap

from neo4j import GraphDatabase

from lib import g
from lib import io
from lib import kg
from lib import llm
from lib import polish

model_filepath = '/home/ubuntu/vault-tmp/llm/gemma-4-26B-A4B-it-UD-Q4_K_XL.gguf'

neo4j_user = io.file_read(f'{g.DATABASE_FOLDERPATH}/neo4j-user.txt').strip()
neo4j_pass = io.file_read(f'{g.DATABASE_FOLDERPATH}/neo4j-pass.txt').strip()

def relationship_extract_raw(output_foldename, node_1, relationship, node_2, rules):
    input_foldername = 'medicinal-plant'
    input_folderpath = f'{g.VAULT_FOLDERPATH}/terrawhisper/studies/pubmed/{input_foldername}/json'
    output_folderpath = f'{g.SSOT_FOLDERPATH}/studies/extraction/{output_foldername}'
    try: os.mkdir(output_folderpath)
    except: pass
    relationships_found = []
    input_filenames = os.listdir(input_folderpath)
    i = 0
    for input_filename in input_filenames[i:]:
        i += 1
        print(f'{i}/{len(input_filenames)}')
        output_filepath = f'{g.SSOT_FOLDERPATH}/studies/extraction/{output_foldername}/{input_filename}'
        if os.path.exists(output_filepath): continue
        input_filepath = f'{input_folderpath}/{input_filename}'
        input_data = io.json_read(input_filepath)
        try: article_data = input_data['PubmedArticle'][0]['MedlineCitation']['Article']
        except: pass
        try: input_title = article_data['ArticleTitle']
        except: input_title = ''
        try: input_abstract = ' '.join(article_data['Abstract']['AbstractText'])
        except: continue
        # print(json.dumps(input_title, indent=4))
        # print(input_title)
        # print(input_abstract)
        # quit()
        content_to_extract = f'{input_title} {input_abstract}'
        prompt = textwrap.dedent(f'''
            From the scientific study ABSTRACT below, extract all the relationships (triples) about {node_1} and {node_2}.
            Write each relationship using this format: [{node_1}, {relationship}, {node_2}]
            {rules}
            Only reply with the relationships requested.
            If you can't find these relationships, reply with "NONE".
            ABSTRACT:
            {content_to_extract}
        ''').strip()
        reply = llm.reply(prompt, model_filepath, max_tokens=512)
        if '</think>' in reply:
            reply = reply.split('</think>')[1].strip()
        print('################################################################################')
        print(reply)
        print('########################################')
        # print(prompt)
        print('################################################################################')
        if 'NONE'.strip() not in reply.strip():
            relationships_found.append(reply)
            output_data = {
                'title': input_title,
                'abstract': input_abstract,
                'reply': reply,
            }
            io.json_write(
                output_filepath,
                output_data,
            )
        # if i > 10:
            # quit()
    print(len(relationships_found))
    # quit()

def relationship_txt_to_json(output_foldername, node_1, relationship, node_2):
    input_foldername = output_foldername
    input_folderpath = f'{g.SSOT_FOLDERPATH}/studies/extraction/{input_foldername}'
    input_filenames = os.listdir(input_folderpath)
    output_filepath = f'{g.SSOT_FOLDERPATH}/studies/extraction/{input_foldername}.json'
    output_items = []
    node1_type = node_1.lower().strip().replace(' ', '_')
    node2_type = node_2.lower().strip().replace(' ', '_')
    for input_filename in input_filenames:
        input_filepath = f'{input_folderpath}/{input_filename}'
        input_data = io.json_read(input_filepath)
        # print(json.dumps(input_data, indent=4))
        relationships_text = input_data['reply']
        relationships_lines = []
        for line in relationships_text.split('\n'):
            line = line.strip()
            if line == '': continue
            if line.startswith('['): line = line[1:]
            if line.endswith(','): line = line[:-1]
            if line.endswith(']'): line = line[:-1]
            chunks = [chunk.strip() for chunk in line.split(',')]
            relationships_lines.append(chunks)
        print(len(relationships_lines))
        study_folderpath = f'{g.VAULT_FOLDERPATH}/terrawhisper/studies/pubmed/medicinal-plant/json'
        study_filepath = f'{study_folderpath}/{input_filename}'
        study_data = io.json_read(study_filepath)
        try: article_data = study_data['PubmedArticle'][0]['MedlineCitation']['Article']
        except: pass
        try: journal_title = article_data['Journal']['Title']
        except: pass
        # print(json.dumps(article_data, indent=4))
        # print(json.dumps(journal_title, indent=4))
        ###
        for line in relationships_lines:
            print(line)
            try: node1, relationship_llm, node2 = line
            except: continue
            if relationship_llm == relationship:
                output_item = {
                    f'{node1_type}': node1,
                    f'relationship': relationship_llm,
                    f'{node2_type}': node2,
                    f'source_id': input_filename.split('.')[0],
                    f'journal_title': journal_title,
                }
                output_items.append(output_item)
    for output_item in output_items:
        print(output_item)
    print(len(output_items))
    io.json_write(output_filepath, output_items)

def plant_wcvp_filter(output_foldername):
    input_foldername = output_foldername
    input_filepath = f'{g.SSOT_FOLDERPATH}/studies/extraction/{input_foldername}.json'
    input_data = io.json_read(input_filepath)
    items_found = []
    for i, item in enumerate(input_data):
        print(i)
        row = kg.sqlite3__wcvp_get(item['plant_name'])
        if row != None:
            print(json.dumps(item, indent=4))
            items_found.append(item)
    output_filepath = f'{g.SSOT_FOLDERPATH}/studies/extraction/{input_foldername}-filter.json'
    io.json_write(output_filepath, items_found)

def neo4j__clear():
    driver = GraphDatabase.driver("bolt://localhost:7687", auth=(neo4j_user, neo4j_pass))
    def delete_data(tx):
        tx.run("MATCH (n) DETACH DELETE n")
    def drop_constraints(tx):
        result = tx.run("SHOW CONSTRAINTS")
        for record in result:
            name = record["name"]
            tx.run(f"DROP CONSTRAINT {name}")
    def drop_indexes(tx):
        result = tx.run("SHOW INDEXES")
        for record in result:
            name = record["name"]
            tx.run(f"DROP INDEX {name}")
    with driver.session() as session:
        session.execute_write(delete_data)
    with driver.session() as session:
        session.execute_write(drop_constraints)
    with driver.session() as session:
        session.execute_write(drop_indexes)
    driver.close()

def neo4j__create(output_filename, neo4j_node_1, neo4j_node_2, node_1_slug_underline, node_2_slug_underline, neo4j_relationship):
    input_filename = f'{output_foldername}-filter'
    rows = io.json_read(f'{g.SSOT_FOLDERPATH}/studies/extraction/{input_filename}.json')
    ### populate kg
    driver = GraphDatabase.driver("bolt://localhost:7687", auth=(neo4j_user, neo4j_pass))
    def execute(tx, rows):
        tx.run(f"""
            UNWIND $rows AS row
            MERGE (s:{neo4j_node_1} {{id: row.{node_1_slug_underline}}})
            MERGE (o:{neo4j_node_2} {{id: row.{node_2_slug_underline}}})
            MERGE (s)-[:{neo4j_relationship} {{source_id: row.source_id}}]->(o)
        """, rows=rows)
    with driver.session() as session:
        session.run(f"""
            CREATE CONSTRAINT {node_1_slug_underline} IF NOT EXISTS
            FOR (p:{neo4j_node_1})
            REQUIRE p.id IS UNIQUE
        """)
        session.run(f"""
            CREATE CONSTRAINT {node_2_slug_underline} IF NOT EXISTS
            FOR (c:{neo4j_node_2})
            REQUIRE c.id IS UNIQUE
        """)
        session.execute_write(execute, rows)
    driver.close()

def neo4j__create_plant_compounds(output_filename):
    input_filename = f'{output_foldername}-filter'
    rows = io.json_read(f'{g.SSOT_FOLDERPATH}/studies/extraction/{input_filename}.json')
    ### populate kg
    driver = GraphDatabase.driver("bolt://localhost:7687", auth=(neo4j_user, neo4j_pass))
    def execute(tx, rows):
        tx.run("""
            UNWIND $rows AS row
            MERGE (s:PLANT {id: row.plant_name})
            MERGE (o:COMPOUND {id: row.medicinal_compound_name})
            MERGE (s)-[:CONTAINS {source_id: row.source_id}]->(o)
        """, rows=rows)
    with driver.session() as session:
        session.run("""
            CREATE CONSTRAINT plant_name IF NOT EXISTS
            FOR (p:PLANT)
            REQUIRE p.id IS UNIQUE
        """)
        session.run("""
            CREATE CONSTRAINT medicinal_compound_name IF NOT EXISTS
            FOR (c:COMPOUND)
            REQUIRE c.id IS UNIQUE
        """)
        session.execute_write(execute, rows)
    driver.close()

def neo4j__create_plant_health_problems(output_foldername):
    input_filename = f'{output_foldername}-filter'
    rows = io.json_read(f'{g.SSOT_FOLDERPATH}/studies/extraction/{input_filename}.json')
    ### populate kg
    driver = GraphDatabase.driver("bolt://localhost:7687", auth=(neo4j_user, neo4j_pass))
    def execute(tx, rows):
        tx.run("""
            UNWIND $rows AS row
            MERGE (s:PLANT {id: row.plant_name})
            MERGE (o:HEALTH_PROBLEM {id: row.health_problem_name})
            MERGE (s)-[:TREATS {source_id: row.source_id}]->(o)
        """, rows=rows)
    with driver.session() as session:
        session.run("""
            CREATE CONSTRAINT plant_name IF NOT EXISTS
            FOR (p:PLANT)
            REQUIRE p.id IS UNIQUE
        """)
        session.run("""
            CREATE CONSTRAINT health_problem_name IF NOT EXISTS
            FOR (c:HEALTH_PROBLEM)
            REQUIRE c.id IS UNIQUE
        """)
        session.execute_write(execute, rows)
    driver.close()

def neo4j__create_plant_conditions(output_foldername):
    input_filename = f'{output_foldername}-filter'
    rows = io.json_read(f'{g.SSOT_FOLDERPATH}/studies/extraction/{input_filename}.json')
    ### populate kg
    driver = GraphDatabase.driver("bolt://localhost:7687", auth=(neo4j_user, neo4j_pass))
    def execute(tx, rows):
        tx.run("""
            UNWIND $rows AS row
            MERGE (s:PLANT {id: row.plant_name})
            MERGE (o:CONDITION {id: row.health_condition_name})
            MERGE (s)-[:USED_FOR {source_id: row.source_id}]->(o)
        """, rows=rows)
    with driver.session() as session:
        session.run("""
            CREATE CONSTRAINT plant_name IF NOT EXISTS
            FOR (p:PLANT)
            REQUIRE p.id IS UNIQUE
        """)
        session.run("""
            CREATE CONSTRAINT problem_name IF NOT EXISTS
            FOR (c:CONDITION)
            REQUIRE c.id IS UNIQUE
        """)
        session.execute_write(execute, rows)
    driver.close()

def neo4j__get_plants():
    driver = GraphDatabase.driver("bolt://localhost:7687", auth=(neo4j_user, neo4j_pass))
    with driver.session() as session:
        result = session.run("""
            MATCH (p:PLANT)
            RETURN p.id AS plant_name
            ORDER BY plant_name
        """)
        plants = [record["plant_name"] for record in result]
    driver.close()
    return plants

def neo4j__get_plant_compounds(plant_name):
    driver = GraphDatabase.driver("bolt://localhost:7687", auth=(neo4j_user, neo4j_pass))
    with driver.session() as session:
        result = session.run("""
            MATCH (p:PLANT)-[:CONTAINS]->(c:COMPOUND)
            WHERE p.id = $plant_name
            RETURN p.id AS plant, c.id AS compound
            ORDER BY compound
        """, plant_name=plant_name)
        rows = [dict(record) for record in result]
    driver.close()
    return rows

def neo4j__get_plant_health_problems(plant_name):
    driver = GraphDatabase.driver("bolt://localhost:7687", auth=(neo4j_user, neo4j_pass))
    with driver.session() as session:
        result = session.run("""
            MATCH (p:PLANT)-[:TREATS]->(c:HEALTH_PROBLEM)
            WHERE p.id = $plant_name
            RETURN p.id AS plant, c.id AS health_problem
            ORDER BY health_problem
        """, plant_name=plant_name)
        rows = [dict(record) for record in result]
    driver.close()
    return rows

if 0:
    node_1 = 'plant name'
    node_2 = 'health problem name'
    relationship = 'treats'
    node_1_slug = polish.sluggify(node_1)
    node_2_slug = polish.sluggify(node_2)
    output_foldername = f'{node_1_slug}-{relationship}-{node_2_slug}'

# neo4j__clear()

# RAW: output not validated
if 0:
    node_1 = 'plant name'
    node_2 = 'pharmacological activity name'
    relationship = 'has_pharmacological_activity'
    node_1_slug = polish.sluggify(node_1)
    node_2_slug = polish.sluggify(node_2)
    node_1_slug_underline = node_1_slug.replace('-', '_')
    node_2_slug_underline = node_2_slug.replace('-', '_')
    output_foldername = f'{node_1_slug}-{relationship}-{node_2_slug}'
    rules = f'''
        Always write the names of the plants in latin binomial scientific name, no common names or abbreviated names.
        To clarify, by {node_2} (medicinal bioactivity) I mean things such as anti-inflammatory, antimicrobial, antioxidant, antiseptic, carminative, analgesic, sedative, etc.
    '''
    # relationship_extract_raw(output_foldername, node_1, relationship, node_2, rules)
    # relationship_txt_to_json(output_foldername, node_1, relationship, node_2)
    # plant_wcvp_filter(output_foldername)
    # quit()
    neo4j_node_1 = 'PLANT'
    neo4j_node_2 = 'PHARMACOLOGICAL_ACTIVITY'
    neo4j_relationship = 'HAS_PHARMACOLOGICAL_ACTIVITY'
    neo4j__create(output_foldername, neo4j_node_1, neo4j_node_2, node_1_slug_underline, node_2_slug_underline, neo4j_relationship)

if 0:
    node_1 = 'plant name'
    node_2 = 'medicinal compound name'
    relationship = 'contains'
    node_1_slug = polish.sluggify(node_1)
    node_2_slug = polish.sluggify(node_2)
    node_1_slug_underline = node_1_slug.replace('-', '_')
    node_2_slug_underline = node_2_slug.replace('-', '_')
    output_foldername = f'{node_1_slug}-{relationship}-{node_2_slug}'
    # relationship_extract_raw(output_foldername, node_1, relationship, node_2, rules)
    relationship_txt_to_json(output_foldername, node_1, relationship, node_2)
    plant_wcvp_filter(output_foldername)
    neo4j_node_1 = 'PLANT'
    neo4j_node_2 = 'COMPOUND'
    neo4j_relationship = 'CONTAINS'
    neo4j__create(output_foldername, neo4j_node_1, neo4j_node_2, node_1_slug_underline, node_2_slug_underline, neo4j_relationship)

if 0:
    node_1 = 'plant name'
    node_2 = 'health condition name'
    relationship = 'used_for'
    node_1_slug = polish.sluggify(node_1)
    node_2_slug = polish.sluggify(node_2)
    node_1_slug_underline = node_1_slug.replace('-', '_')
    node_2_slug_underline = node_2_slug.replace('-', '_')
    output_foldername = f'{node_1_slug}-{relationship}-{node_2_slug}'
    rules = f'''
        Always write the names of the plants in latin binomial scientific name, no common names or abbreviated names.
        By health conditions, I mean I want to extract all diseases, disorders, symptoms, syndromes, ailments, and health issues that the plant is claimed to treat, relieve, prevent, manage, or improve.
    '''
    # relationship_extract_raw(output_foldername, node_1, relationship, node_2, rules)
    relationship_txt_to_json(output_foldername, node_1, relationship, node_2)
    plant_wcvp_filter(output_foldername)
    neo4j_node_1 = 'PLANT'
    neo4j_node_2 = 'CONDITION'
    neo4j_relationship = 'USED_FOR'
    neo4j__create(output_foldername, neo4j_node_1, neo4j_node_2, node_1_slug_underline, node_2_slug_underline, neo4j_relationship)

### PARTS
if 1:
    node_1 = 'plant name'
    node_2 = 'plant part name'
    relationship = 'contains'
    node_1_slug = polish.sluggify(node_1)
    node_2_slug = polish.sluggify(node_2)
    node_1_slug_underline = node_1_slug.replace('-', '_')
    node_2_slug_underline = node_2_slug.replace('-', '_')
    output_foldername = f'{node_1_slug}-{relationship}-{node_2_slug}'
    rules = f'''
        Always write the names of the plants in latin binomial scientific name, no common names or abbreviated names.
        By plant parts I mean things like leaf, flower, root, etc.
    '''
    ### WARNING: next like takes hours
    # relationship_extract_raw(output_foldername, node_1, relationship, node_2, rules)
    relationship_txt_to_json(output_foldername, node_1, relationship, node_2)
    plant_wcvp_filter(output_foldername)
    neo4j_node_1 = 'PLANT'
    neo4j_node_2 = 'PART'
    neo4j_relationship = 'HAS_PART'
    neo4j__create(output_foldername, neo4j_node_1, neo4j_node_2, node_1_slug_underline, node_2_slug_underline, neo4j_relationship)

# plant_wcvp_filter(output_foldername)

# TODO: VALIDATED: output names checked if really present in the study (string matching)



'''
plants = neo4j__get_plants()
for plant in plants:
    print(plant)
print(len(plants))
'''

# paths = neo4j__get_plant_compounds("Ginkgo biloba")
# paths = neo4j__get_plant_health_problems("Ginkgo biloba")

# for path in paths:
    # print(path)

