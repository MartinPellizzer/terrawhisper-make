import os
import json
import textwrap

from neo4j import GraphDatabase

from lib import g
from lib import io
from lib import llm

model_filepath = '/home/ubuntu/vault-tmp/llm/gemma-4-26B-A4B-it-UD-Q4_K_XL.gguf'

neo4j_user = io.file_read(f'{g.DATABASE_FOLDERPATH}/neo4j-user.txt').strip()
neo4j_pass = io.file_read(f'{g.DATABASE_FOLDERPATH}/neo4j-pass.txt').strip()

### TODO: force only one plant name and one disease condition per line
def llm__study__used_to_treat__extract():
    input_folderpath = f'{g.VAULT_FOLDERPATH}/terrawhisper/studies/pubmed/medicinal-plant-0000/json'
    relationships_found = []
    input_filenames = os.listdir(input_folderpath)
    for i, input_filename in enumerate(input_filenames[:]):
        print(f'{i}/{len(input_filenames)}')
        input_filepath = f'{input_folderpath}/{input_filename}'
        input_data = io.json_read(input_filepath)
        try: input_title = input_data['PubmedArticle'][0]['MedlineCitation']['Article']['ArticleTitle']
        except: input_title = ''
        try: input_abstract = ' '.join(input_data['PubmedArticle'][0]['MedlineCitation']['Article']['Abstract']['AbstractText'])
        except: continue
        # print(json.dumps(input_title, indent=4))
        # print(input_title)
        # print(input_abstract)
        # quit()
        content_to_extract = f'{input_title} {input_abstract}'
        prompt = textwrap.dedent(f'''
            From the scientific study ABSTRACT below, extract all the relationships (triples) about plants names and the diseases they treat.
            Write each relationship using this format: [plant name, used_to_treat, diseases name]
            Always write the names of the plants in full scientific name, no common names or abbreviated names.
            Always write the names of the diseases in the exact way they are written in the abstract.
            Only reply with the relationships requested.
            If you can't find these relationships, reply with NONE.
            ABSTRACT:
            {content_to_extract}
        ''').strip()
        reply = llm.reply(prompt, model_filepath)
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
                f'{g.SSOT_FOLDERPATH}/studies/extraction/plant_name-used_to_treat-disease_name/{input_filename}', 
                output_data,
            )
    print(len(relationships_found))

def json__study__used_to_treat__extract():
    output_items = []
    input_folderpath = f'{g.SSOT_FOLDERPATH}/studies/extraction/plant_name-used_to_treat-disease_name'
    input_filenames = os.listdir(input_folderpath)
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
        ###
        for line in relationships_lines:
            print(line)
            try: node1, relationship, node2 = line
            except: continue
            if relationship != 'used_to_treat': continue
            output_item = {
                'plant_name': node1,
                'relationship': relationship,
                'disease_name': node2,
            }
            output_items.append(output_item)
            print(node1)
        # break
    for output_item in output_items:
        print(output_item)
    print(len(output_items))
    output_filepath = f'{g.SSOT_FOLDERPATH}/studies/extraction/json/plant_name-used_to_treat-disease_name.json'
    io.json_write(output_filepath, output_items)

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

neo4j__clear()
rows = io.json_read(f'{g.SSOT_FOLDERPATH}/studies/extraction/json/plant_name-used_to_treat-disease_name.json')
### populate kg
driver = GraphDatabase.driver("bolt://localhost:7687", auth=(neo4j_user, neo4j_pass))
def execute(tx, rows):
    tx.run("""
        UNWIND $rows AS row
        MERGE (s:Plant {id: row.plant_name})
        MERGE (o:Disease {id: row.disease_name})
        MERGE (s)-[:USED_TO_TREAT]->(o)
    """, rows=rows)
with driver.session() as session:
    session.run("""
        CREATE CONSTRAINT plant_name IF NOT EXISTS
        FOR (p:Plant)
        REQUIRE p.id IS UNIQUE
    """)
    session.run("""
        CREATE CONSTRAINT disease_name IF NOT EXISTS
        FOR (c:Disease)
        REQUIRE c.id IS UNIQUE
    """)
    session.execute_write(execute, rows)
driver.close()
