wikidata_folderpath = f'/home/ubuntu/vault/terrawhisper/database/ssot/wikidata'
taxdmp_folderpath = f'{wikidata_folderpath}/taxdmp'
taxdmp_nodes_filepath = f'{taxdmp_folderpath}/nodes.dmp'
taxdmp_names_filepath = f'{taxdmp_folderpath}/names.dmp'
# wikidata_filepath = f'{wikidata_folderpath}/label-map.json'

import os
import json
import shutil

from neo4j import GraphDatabase

from lib import io
from lib import llm
from lib import data

uri = "bolt://localhost:7687"
username = "neo4j"
password = "Newoliark1"

driver = GraphDatabase.driver(uri, auth=(username, password))

def db_clear():
    with driver.session() as session:
        tx = session.begin_transaction()
        tx.run("MATCH (n) DETACH DELETE n")
        tx.commit()

def db_read_family(plant_taxon_name):
    with driver.session() as session:
        tx = session.begin_transaction()
        query = """
            MATCH (p:Plant {name: $plant})-[:HAS_FAMILY]->(f:Family)
            RETURN f.name
        """
        result = tx.run(query, plant=plant_taxon_name)
        record = result.single()
        family = record['f.name'] if record else none
        tx.commit()
        print(family)
        # return record["family"] if record else None

        import textwrap
        prompt = textwrap.dedent(f'''
            Write one sentence with the following data and relationships:
            {plant_taxon_name} -> has family -> {family}
        ''').strip()
        print(prompt)
        reply = llm.reply(prompt, model_filepath, temperature=0)
        if '</think>' in reply:
            reply = reply.split('</think>')[1].strip()
        print('########################################')
        print(reply)
        print('########################################')

    
def db_insert__plant_family():
    triples = []
    jsons_foldername = 'wikidata-wcvp-jsons'
    jsons_folderpath = f'{wikidata_folderpath}/{jsons_foldername}'
    jsons_filepaths = [f'{jsons_folderpath}/{filename}' for filename in os.listdir(jsons_folderpath)]
    for json_filepath in jsons_filepaths:
        json_data = io.json_read(json_filepath)
        _item = {
            'taxon_name': json_data['taxon_name'],
            'family': json_data['family'],
        }
        triples.append(_item)
    ###
    batch_size = 1000
    with driver.session() as session:
        for i in range(0, len(triples), batch_size):
            batch = triples[i:i+batch_size]
            query = """
            UNWIND $rows AS row
            MERGE (p:Plant {name: row.taxon_name})
            MERGE (f:Family {name: row.family})
            MERGE (p)-[:HAS_FAMILY]->(f)
            """
            tx = session.begin_transaction()
            tx.run(query, rows=batch)
            tx.commit()

def insert_families_orders():
    data = io.json_read(f'{wikidata_folderpath}/families-orders.json')
    ###
    batch_size = 1000
    with driver.session() as session:
        for i in range(0, len(data), batch_size):
            batch = data[i:i+batch_size]
            query = """
                UNWIND $rows AS row
                MERGE (f:Family {name: row.family})
                MERGE (o:Order  {name: row.order})
                MERGE (f)-[:HAS_ORDER]->(o)
            """
            tx = session.begin_transaction()
            tx.run(query, rows=batch)
            tx.commit()

insert_families_orders()

driver.close()

quit()
# db_clear()
db_insert__plant_family()

'''
def read_dmp(path, num_fields=None):
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            # remove trailing row terminator
            line = line.strip()

            # remove final '|'
            if line.endswith("|"):
                line = line[:-1]

            # split on the real delimiter
            parts = [x.strip() for x in line.split("\t|\t")]

            # optional sanity check
            if num_fields and len(parts) != num_fields:
                continue  # or raise error

            yield parts
'''

def read_dmp(path, num_fields=None):
    rows = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            # remove whitespace/newline
            line = line.strip()
            # remove trailing '|'
            if line.endswith("|"):
                line = line[:-1]
            # split on the custom delimiter
            parts = [x.strip() for x in line.split("\t|\t")]
            # optional validation
            if num_fields and len(parts) != num_fields:
                continue  # or raise ValueError
            rows.append(parts)
    return rows

'''
nodes_families = []
rows = read_dmp(taxdmp_nodes_filepath)
nodes = []
for row_i, row in enumerate(rows):
    # print(f'{row_i}/{len(list(rows))}')
    tax_id = row[0]
    parent_tax_id = row[1]
    rank = row[2]
    division_id = row[4]
    if rank == 'family':
        _item = {
            'tax_id': row[0],
            'parent_tax_id': row[1],
            'rank': row[2],
            'division_id': row[4],
        }
        nodes_families.append(_item)
        nodes.append(row)


print(f'NODES: {len(list(nodes_families))}')
print(nodes[0])

'''
import sqlite3

# connect (or create) database
conn = sqlite3.connect("taxonomy.db")
cur = conn.cursor()

'''
# create table
cur.execute("""
CREATE TABLE IF NOT EXISTS nodes (
    tax_id INTEGER PRIMARY KEY,
    parent_tax_id INTEGER,
    rank TEXT
)
""")

# transform rows → keep only needed fields
nodes_data = [(int(r[0]), int(r[1]), r[2]) for r in nodes]

# bulk insert (FAST)
cur.executemany(
    "INSERT INTO nodes (tax_id, parent_tax_id, rank) VALUES (?, ?, ?)",
    nodes_data
)

conn.commit()
'''

'''
# how many rows?
cur.execute("SELECT COUNT(*) FROM nodes")
print("nodes rows:", cur.fetchone()[0])

cur.execute("SELECT * FROM nodes LIMIT 10")
for row in cur.fetchall():
    print(row)
'''

'''
cur.execute("""
CREATE TABLE IF NOT EXISTS names (
    tax_id INTEGER,
    name_txt TEXT,
    unique_name TEXT,
    name_class TEXT
)
""")

names_rows = read_dmp(taxdmp_names_filepath)

names_data = [(int(r[0]), r[1], r[2], r[3]) for r in names_rows]

cur.executemany(
    "INSERT INTO names (tax_id, name_txt, unique_name, name_class) VALUES (?, ?, ?, ?)",
    names_data
)

conn.commit()
'''

'''
cur.execute("SELECT COUNT(*) FROM names")
print("names rows:", cur.fetchone()[0])

cur.execute("SELECT * FROM names LIMIT 10")
for row in cur.fetchall():
    print(row)
'''


'''
cur.execute("CREATE INDEX IF NOT EXISTS idx_names_name ON names(name_txt)")
cur.execute("CREATE INDEX IF NOT EXISTS idx_names_tax ON names(tax_id)")
cur.execute("CREATE INDEX IF NOT EXISTS idx_nodes_tax ON nodes(tax_id)")
conn.commit()
'''

'''
cur.execute("""
SELECT n.tax_id, n.parent_tax_id, n.rank
FROM names nm
JOIN nodes n ON nm.tax_id = n.tax_id
WHERE nm.name_txt = 'Rosaceae'
LIMIT 10
""")
'''

'''
triples = []
jsons_foldername = 'wikidata-wcvp-jsons'
jsons_folderpath = f'{wikidata_folderpath}/{jsons_foldername}'
jsons_filepaths = [f'{jsons_folderpath}/{filename}' for filename in os.listdir(jsons_folderpath)]
for json_filepath in jsons_filepaths:
    json_data = io.json_read(json_filepath)
    _item = {
        'taxon_name': json_data['taxon_name'],
        'family': json_data['family'],
    }
    triples.append(_item)

parents = []
for triple in triples:
    # print(triple)
    family = triple['family']
    query = f"""
    SELECT
        family.name_txt AS family,
        n.tax_id,
        n.parent_tax_id,
        parent.name_txt AS parent_name
    FROM names family
    JOIN nodes n ON family.tax_id = n.tax_id
    JOIN names parent ON n.parent_tax_id = parent.tax_id
    WHERE family.name_txt = '{family}'
    AND family.name_class = 'scientific name'
    AND parent.name_class = 'scientific name'
    """
    cur.execute(query)
    res = cur.fetchall()
    if res:
        res = res[0]
        print(res)
        parents.append({'family': res[0], 'order': res[3]})

io.json_write(f'{wikidata_folderpath}/families-orders.json', parents)

print(len(triples))
print(len(parents))
'''

# print(cur.fetchall())

quit()

        # if 'Rosaceae' in name_txt:

rows = read_dmp(taxdmp_names_filepath)
names_families = []
for node in nodes_families:
    node_id = node['tax_id']
    for row in rows:
        row_id = row[0]
        row_txt = row[1]
        print('FAMILY:', node_id, row_id, row_txt)
        if row_id == node_id:
            _item = {
                'tax_id': row_id,
                'name_txt': row_txt,
            }
            names_families.append(_item)
            found = True
            break

for item in names_families:
    print(item)

io.json_write(f'{wikidata_folderpath}/names_families.json', names_families)

quit()

# get 'ROSACEAE' id
result = None
rows = read_dmp(taxdmp_names_filepath)
for row in rows:
    name_txt = row[1]
    if 'Rosaceae' in name_txt:
        result = row

print(result)

quit()

names_rows = read_dmp(taxdmp_names_filepath)
names = []
i = 0
for node in nodes:
    node_id = node['tax_id']
    node_parent_id = node['parent_tax_id']
    node_name = None
    node_parent_name = None
    # found = False
    for row in names_rows:
        name_id = row[0]
        name_txt = row[1]
        print('FAMILY:', name_id, node_id, name_txt)
        ###
        if name_id == node_id:
            node_name = name_txt
        if name_id == node_parent_id:
            node_parent_name = name_txt
        if node_name != None and node_parent_name != None:
            _item = {
                'node_id': node_id,
                'node_name': node_name,
                'node_parent_name': node_parent_name,
            }
            names.append(_item)
            found = True
            break
    break
    # if found:
    i += 1
    # if i >= 5: break


for item in names:
    print(item)

quit()

divisions_rows = read_dmp(f'{taxdmp_folderpath}/division.dmp')
divisions = []
i = 0
for family in families:
    division_id = family['division_id']
    found = False
    for row in divisions_rows:
        tax_id = row[0]
        print(division_id, tax_id)
        if tax_id == division_id:
            _item = {
                'division_id': tax_id,
                'division_cde': row[1],
                'division_name': row[2],
                'comments': row[3],
            }
            divisions.append(_item)
            found = True
            break
    if found:
        break
    i += 1
    if i >= 5: break

for item in names:
    print(f'''TAXON_ID:     {item['taxon_id']}''')
    print(f'''NAME_TXT:     {item['name_txt']}''')
    print(f'''UNIQUE_NAME:  {item['unique_name']}''')
    print(f'''NAME_CLASS:   {item['name_class']}''')
    print()

for item in divisions:
    print(f'''DIVISION_ID:      {item['division_id']}''')
    print(f'''DIVISION_CDE:     {item['division_cde']}''')
    print(f'''DIVISION_NAME:    {item['division_name']}''')
    print(f'''COMMENTS:         {item['comments']}''')
    print()

quit()


quit()

model_filepath = '/home/ubuntu/vault-tmp/llm/gemma-4-26B-A4B-it-UD-Q4_K_XL.gguf'


# driver.close()

# quit()

def create_node(tx):
    tx.run("CREATE (n:Test {name: $name})", name="Python Node")

with driver.session() as session:
    session.execute_write(create_node)

def get_nodes(tx):
    query = "MATCH (n:Test) RETURN n.name AS name"
    result = tx.run(query)
    return [record["name"] for record in result]

with driver.session() as session:
    names = session.execute_read(get_nodes)
    print(names)

# driver.close()
# quit()

def wikidata_taxon_names_get():
    import os
    from lib import io
    taxon_names = []
    ###
    entity_foldername = 'entity_has-use_medicinal-plant'
    entity_folderpath = f'{wikidata_folderpath}/{entity_foldername}'
    entities_filepaths = [f'{entity_folderpath}/{filename}' for filename in os.listdir(entity_folderpath)]
    ###
    relationship_foldername = 'property_medicinal-plant'
    relationship_folderpath = f'{wikidata_folderpath}/{relationship_foldername}'
    ###
    P_ID = 'P225'
    for entity_i, entity_filepath in enumerate(entities_filepaths):
        s_id = entity_filepath.split('/')[-1].split('.')[0]
        s_data = io.json_read(entity_filepath)
        claims = s_data['entities'][s_id]['claims']
        for claim in claims:
            p_id = claim.strip()
            if p_id == P_ID:
                o_taxon_name_value = claims[P_ID][0]['mainsnak']['datavalue']['value']
                # print(o_taxon_name_value)
                taxon_names.append({'id': s_id, 'taxon_name': o_taxon_name_value})
        # quit()
    return taxon_names

# wikidata_taxon_names = wikidata_taxon_names_get()

# herbs_wcvp = data.herbs_wcvp_get()
# for herb in herbs_wcvp[:100]:
    # print(herb['family'])
    # print(herb)


def wikidata_found_in_wcvp_gen():
    entity_foldername = 'entity_has-use_medicinal-plant'
    entity_folderpath = f'{wikidata_folderpath}/{entity_foldername}'
    entities_filepaths = [f'{entity_folderpath}/{filename}' for filename in os.listdir(entity_folderpath)]
    ###
    relationship_foldername = 'property_medicinal-plant'
    relationship_folderpath = f'{wikidata_folderpath}/{relationship_foldername}'
    ###
    from_folderpath = f'{wikidata_folderpath}/entity_has-use_medicinal-plant'
    to_folderpath = f'{wikidata_folderpath}/wikidata-found-in-wcvp'
    ###
    P_ID = 'P225'
    for entity_i, entity_filepath in enumerate(entities_filepaths[:99999]):
        s_id = entity_filepath.split('/')[-1].split('.')[0]
        s_data = io.json_read(entity_filepath)
        claims = s_data['entities'][s_id]['claims']
        for claim in claims:
            p_id = claim.strip()
            if p_id == P_ID:
                o_taxon_name_value = claims[P_ID][0]['mainsnak']['datavalue']['value']
                from_filepath = f'{from_folderpath}/{s_id}.json'
                to_filepath = f'{to_folderpath}/{s_id}.json' 
                if os.path.exists(to_filepath):
                    continue
                found = False
                for herb_wcvp in herbs_wcvp:
                    if o_taxon_name_value.lower().strip() == herb_wcvp['taxon_name'].lower().strip():
                        shutil.copy2(from_filepath, to_filepath)
                        print(s_id, '->', o_taxon_name_value, '->', herb_wcvp['family'])
                        found = True
                        break
                if not found:
                    print('N/A')

def wikidata_wcvp_family_gen():
    wikidata_found_in_wcvp_foldername = 'wikidata-found-in-wcvp'
    wikidata_found_in_wcvp_folderpath = f'{wikidata_folderpath}/{wikidata_found_in_wcvp_foldername}'
    wikidata_found_in_wcvp_filepaths = [
        f'{wikidata_found_in_wcvp_folderpath}/{filename}' for filename in os.listdir(wikidata_found_in_wcvp_folderpath)
    ]
    ###
    output_folderpath = f'{wikidata_folderpath}/wikidata-wcvp-jsons'
    ###
    P_ID = 'P225'
    for wikidata_found_in_wcvp_filepath in wikidata_found_in_wcvp_filepaths[:10]:
        s_id = wikidata_found_in_wcvp_filepath.split('/')[-1].split('.')[0]
        s_data = io.json_read(wikidata_found_in_wcvp_filepath)
        claims = s_data['entities'][s_id]['claims']
        for claim in claims:
            p_id = claim.strip()
            if p_id == P_ID:
                o_taxon_name_value = claims[P_ID][0]['mainsnak']['datavalue']['value']
                output_filepath = f'{output_folderpath}/{s_id}.json'
                if os.path.exists(output_filepath):
                    continue
                for herb_wcvp in herbs_wcvp:
                    if o_taxon_name_value.lower().strip() == herb_wcvp['taxon_name'].lower().strip():
                        print(s_id, '->', o_taxon_name_value, '->', herb_wcvp['family'])
                        _item = {
                            'id': s_id,
                            'taxon_name': herb_wcvp['taxon_name'],
                            'family': herb_wcvp['family'],
                        }
                        io.json_write(output_filepath, _item)
                        break

# wikidata_wcvp_family_gen()

# quit()

def scrape_powo():
    # gbif.org
    import time

    from selenium import webdriver
    from selenium.webdriver.common.keys import Keys
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.firefox.options import Options

    geckodriver_path = 'geckodriver'
    driver_service = webdriver.FirefoxService(executable_path=geckodriver_path)

    driver = webdriver.Firefox(service=driver_service)
    driver.get('https://www.google.com')
    driver.maximize_window()

    # driver.get('https://www.gbif.org/')
    time.sleep(10)

    taxon_name = 'achillea millefolium'
    powo_taxon_id = 'urn:lsid:ipni.org:names:541365-1'
    driver.get(f'https://powo.science.kew.org/taxon/{powo_taxon_id}')

    e = driver.find_element(By.XPATH, '//ul[@id="siteSearchInputHome"]')


'''
e = driver.find_element(By.XPATH, '//input[@id="siteSearchInputHome"]')
for c in 'test':
    try: e.send_keys(c)
    except: break
e.send_keys(Keys.ENTER)
'''

# quit()

def plants_taxon():
    import os
    import time
    import random

    from lib import io

    entity_foldername = 'entity_has-use_medicinal-plant'
    entity_folderpath = f'{wikidata_folderpath}/{entity_foldername}'
    entities_filepaths = [f'{entity_folderpath}/{filename}' for filename in os.listdir(entity_folderpath)]
    ###
    relationship_foldername = 'property_medicinal-plant'
    relationship_folderpath = f'{wikidata_folderpath}/{relationship_foldername}'
    ###
    for entity_i, entity_filepath in enumerate(entities_filepaths):
        s_id = entity_filepath.split('/')[-1].split('.')[0]
        s_data = io.json_read(entity_filepath)
        try: s_label = s_data['entities'][s_id]['labels']['en']['value']
        except: s_label = 'S_LABEL N/A'
        claims = s_data['entities'][s_id]['claims']
        print(entity_filepath)
        print(f'{entity_i}/{len(entities_filepaths)}')
        for claim in claims:
            p_id = claim.strip()
            p_filepath = f'{relationship_folderpath}/{p_id}.json'
            p_data = io.json_read(p_filepath)
            p_label = p_data['entities'][p_id]['labels']['en']['value']
            ###
            try: o_type = claims[p_id][0]['mainsnak']['datavalue']['type']
            except: continue
            if o_type == 'string':
                o_value = claims[p_id][0]['mainsnak']['datavalue']['value']
            elif o_type == 'monolingualtext':
                o_value = claims[p_id][0]['mainsnak']['datavalue']['value']
                o_value = o_value['text']
            else:
                o_value = claims[p_id][0]['mainsnak']['datavalue']['value']
                try: o_id = o_value['id']
                except: 
                    o_id = None
                    o_value = 'ID N/A'

                if o_id:
                    o_filepath = f'{wikidata_folderpath}/Q/{o_id}.json'
                    o_data = io.json_read(o_filepath)
                    try: o_value = o_data['entities'][o_id]['labels']['en']['value']
                    except: o_value = 'N/A'
            ###
            print(s_label, '->', p_label, '->', o_value)
            # quit()
        quit()
    quit()

# plants_taxon()

def entities_relationships_distribution():
    import os
    import time
    import random

    from lib import io

    p_distributions = []

    entity_foldername = 'entity_has-use_medicinal-plant'
    entity_folderpath = f'{wikidata_folderpath}/{entity_foldername}'
    entities_filepaths = [f'{entity_folderpath}/{filename}' for filename in os.listdir(entity_folderpath)]
    ###
    relationship_foldername = 'property_medicinal-plant'
    relationship_folderpath = f'{wikidata_folderpath}/{relationship_foldername}'
    ###
    i = 0
    for entity_i, entity_filepath in enumerate(entities_filepaths):
        s_id = entity_filepath.split('/')[-1].split('.')[0]
        s_data = io.json_read(entity_filepath)
        try: s_label = s_data['entities'][s_id]['labels']['en']['value']
        except: s_label = 'S_LABEL N/A'
        claims = s_data['entities'][s_id]['claims']
        print(entity_filepath)
        print(f'{entity_i}/{len(entities_filepaths)}')
        for claim in claims:
            p_id = claim.strip()
            p_filepath = f'{relationship_folderpath}/{p_id}.json'
            p_data = io.json_read(p_filepath)
            p_label = p_data['entities'][p_id]['labels']['en']['value']
            print(p_id)
            found = False
            for p_distribution in p_distributions:
                if p_id == p_distribution['id']:
                    p_distribution['count'] += 1
                    found = True
                    break
            if not found:
                _item = {
                    'id': p_id,
                    'label': p_label,
                    'count': 1,
                }
                p_distributions.append(_item)
        i += 1
        if i >= 99999: break
    p_distributions = sorted(p_distributions, key=lambda x: x['count'], reverse=True)
    for p_distribution in p_distributions:
        print(p_distribution)
    io.json_write(f'{wikidata_folderpath}/relationships-distribution.json', p_distributions)
    quit()

entities_relationships_distribution()

def entities_jsons_get():
    import os
    import time
    import random

    import requests

    from lib import io

    data = io.json_read(f'{wikidata_folderpath}/entity_has-use_medicinal-plant.json')
    for item in data:
        item_url = item['item']
        item_id = item_url.split('/')[-1]
        print(item_id)
    
        output_filepath = f'{wikidata_folderpath}/entity_has-use_medicinal-plant/{item_id}.json'
        if not os.path.exists(output_filepath):
            # url = "https://www.wikidata.org/wiki/Special:EntityData/Q37153.json"
            # url = "https://www.wikidata.org/w/api.php?action=wbgetentities&ids=Q37153|P31|Q5&props=labels&languages=en&format=json"
            url = f"https://www.wikidata.org/wiki/Special:EntityData/{item_id}.json"

            headers = {
                "User-Agent": "MyWikidataApp/1.0 (your_email@example.com) requests"
            }

            response = requests.get(url, headers=headers)
            response.raise_for_status()

            data = response.json()
            # print(data["entities"]["Q37153"]["labels"]["en"]["value"])
            # print(data["entities"])
            io.json_write(output_filepath, data)

            time.sleep(random.randint(2, 3))
            # break

    quit()

def relationships_jsons_get():
    import os
    import time
    import random

    import requests

    from lib import io

    print(wikidata_folderpath)
    entity_foldername = 'entity_has-use_medicinal-plant'
    entity_folderpath = f'{wikidata_folderpath}/{entity_foldername}'
    entities_filenames = os.listdir(entity_folderpath)
    for entity_filename in entities_filenames:
        entity_id = entity_filename.split('.')[0]
        entity_filepath = f'{entity_folderpath}/{entity_filename}'
        print(entity_filepath)
        ###
        data = io.json_read(entity_filepath)
        claims = data['entities'][entity_id]['claims']
        for claim in claims:
            p_id = claim.strip()

            output_filepath = f'{wikidata_folderpath}/property_medicinal-plant/{p_id}.json'
            if not os.path.exists(output_filepath):
                url = f"https://www.wikidata.org/wiki/Special:EntityData/{p_id}.json"

                headers = {
                    "User-Agent": "MyWikidataApp/1.0 (your_email@example.com) requests"
                }

                response = requests.get(url, headers=headers)
                response.raise_for_status()

                data = response.json()
                # print(data["entities"]["Q37153"]["labels"]["en"]["value"])
                # print(data["entities"])
                io.json_write(output_filepath, data)

                time.sleep(random.randint(2, 3))
                # quit()

    quit()

def entity_json_download(q_id):
    import os
    import time
    import random

    import requests

    from lib import io

    output_filepath = f'{wikidata_folderpath}/Q/{q_id}.json'
    if not os.path.exists(output_filepath):
        url = f"https://www.wikidata.org/wiki/Special:EntityData/{q_id}.json"

        headers = {
            "User-Agent": "MyWikidataApp/1.0 (your_email@example.com) requests"
        }

        response = requests.get(url, headers=headers)
        response.raise_for_status()

        data = response.json()
        io.json_write(output_filepath, data)
        time.sleep(random.randint(2, 3))

def triples_gen():
    import os
    import time
    import random

    from lib import io

    entity_foldername = 'entity_has-use_medicinal-plant'
    entity_folderpath = f'{wikidata_folderpath}/{entity_foldername}'
    entities_filepaths = [f'{entity_folderpath}/{filename}' for filename in os.listdir(entity_folderpath)]
    ###
    relationship_foldername = 'property_medicinal-plant'
    relationship_folderpath = f'{wikidata_folderpath}/{relationship_foldername}'
    ###
    for entity_i, entity_filepath in enumerate(entities_filepaths):
        s_id = entity_filepath.split('/')[-1].split('.')[0]
        s_data = io.json_read(entity_filepath)
        try: s_label = s_data['entities'][s_id]['labels']['en']['value']
        except: s_label = 'S_LABEL N/A'
        claims = s_data['entities'][s_id]['claims']
        print(entity_filepath)
        print(f'{entity_i}/{len(entities_filepaths)}')
        for claim in claims:
            p_id = claim.strip()
            p_filepath = f'{relationship_folderpath}/{p_id}.json'
            p_data = io.json_read(p_filepath)
            p_label = p_data['entities'][p_id]['labels']['en']['value']
            ###
            try: o_type = claims[p_id][0]['mainsnak']['datavalue']['type']
            except: continue
            if o_type == 'string':
                o_value = claims[p_id][0]['mainsnak']['datavalue']['value']
            elif o_type == 'monolingualtext':
                o_value = claims[p_id][0]['mainsnak']['datavalue']['value']
                o_value = o_value['text']
            else:
                o_value = claims[p_id][0]['mainsnak']['datavalue']['value']
                try: o_id = o_value['id']
                except: 
                    o_id = None
                    o_value = 'ID N/A'

                if o_id:
                    entity_json_download(o_id)

                    o_filepath = f'{wikidata_folderpath}/Q/{o_id}.json'
                    o_data = io.json_read(o_filepath)
                    try: o_value = o_data['entities'][o_id]['labels']['en']['value']
                    except: o_value = 'N/A'
                    # quit()
                    # print(p_id)
                    # print(o_value)
            ###
            print(s_label, '->', p_label, '->', o_value)
            # quit()
        # quit()
    quit()

# entities_jsons_get()
# relationships_jsons_get()

triples_gen()

def triples_resolution_sparql():
    import sys
    from SPARQLWrapper import SPARQLWrapper, JSON

    endpoint_url = "https://query.wikidata.org/sparql"

    query = """
    SELECT ?plant ?plantLabel ?use ?useLabel WHERE {
      ?plant wdt:P31/wdt:P279* wd:Q207123 .
      OPTIONAL { ?plant wdt:P366 ?use . }

      SERVICE wikibase:label {
        bd:serviceParam wikibase:language "en".
      }
    }
    LIMIT 200
    """


    def get_results(endpoint_url, query):
        user_agent = "WDQS-example Python/%s.%s" % (sys.version_info[0], sys.version_info[1])
        # TODO adjust user agent; see https://w.wiki/CX6
        sparql = SPARQLWrapper(endpoint_url, agent=user_agent)
        sparql.setQuery(query)
        sparql.setReturnFormat(JSON)
        return sparql.query().convert()


    for i in range(2):
        results = get_results(endpoint_url, query)

        for result in results["results"]["bindings"]:
            print(result)

        print(len(results["results"]["bindings"]))



def triples_extraction():
    import json
    from lib import io

    label_map = [
        {'id': 'Q37153', 'value': 'Aguacate',},
        {'id': 'P366', 'value': 'has use',},
    ]

    wikidata_folderpath = f'/home/ubuntu/vault/terrawhisper/database/ssot/wikidata'
    wikidata_filepath = f'{wikidata_folderpath}/label-map.json'

    label_map = io.json_read(wikidata_filepath, create=True)

    s_id = 'Q37153'
    with open(f"{wikidata_folderpath}/{s_id}.json", "r", encoding="utf-8") as f:
        json_data = json.load(f)

    claims = data['entities'][subject_id]['claims']

    quit()

    subject_id = 'Q37153'
    predicate_id = 'P366'
    with open(f"{subject_id}.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    # print(json.dumps(data['entities'][subject]['claims']['P366'], indent=4))

    claims = data['entities'][subject_id]['claims']

    for claim in claims:
        subject_value = [item['value'] for item in label_map if item['id'] == subject_id][0]
        # _predicate = claim
        # _object = claim['mainsnak']['datavalue']['value']['id']

        # triple = f'{_subject} -> {_predicate} -> {_object}'
        # print(triple)
        predicate_id = claim
        predicate_data = claims[predicate_id]
        if predicate_id == 'P366':
            for predicate_item in predicate_data:
                # print(predicate_item)
                o_value = predicate_item['mainsnak']['datavalue']['value']
                print(o_value)
                # predicate_values = [item['value'] for item in label_map if item['id'] == predicate_id]
                # print(predicate_values)
            quit()
        predicate_values = [item['value'] for item in label_map if item['id'] == predicate_id]
        if predicate_values != []:
            predicate_value = predicate_values[0]
        else:
            predicate_value = predicate_id
        
        # print(claims[claim])
        print(subject_value, '->', predicate_value, '->', claims[claim][0]['mainsnak']['datavalue']['value'])

    # TODO
    # https://www.wikidata.org/w/api.php?action=wbgetentities&ids=Q37153|P31|Q5&props=labels&languages=en&format=json

triples_extraction()

quit()

import requests

def fetch_entities(qids):
    ids = "|".join(qids)
    url = "https://www.wikidata.org/w/api.php"
    
    params = {
        "action": "wbgetentities",
        "ids": ids,
        "format": "json",
        "languages": "en"
    }
    
    return requests.get(url, params=params).json()["entities"]

fetch_entities(['Q37153'])

quit()

# pip install sparqlwrapper
# https://rdflib.github.io/sparqlwrapper/

import sys
from SPARQLWrapper import SPARQLWrapper, JSON

endpoint_url = "https://query.wikidata.org/sparql"

query = """
    SELECT ?item ?itemLabel
    WHERE
    {
      ?item wdt:P366 wd:Q188840. # Must be a cat
      SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],mul,en". }
    }
    LIMIT 500 OFFSET 0
"""


def get_results(endpoint_url, query):
    user_agent = "WDQS-example Python/%s.%s" % (sys.version_info[0], sys.version_info[1])
    # TODO adjust user agent; see https://w.wiki/CX6
    sparql = SPARQLWrapper(endpoint_url, agent=user_agent)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    return sparql.query().convert()


for i in range(2):
    results = get_results(endpoint_url, query)

    for result in results["results"]["bindings"]:
        print(result)

    print(len(results["results"]["bindings"]))




