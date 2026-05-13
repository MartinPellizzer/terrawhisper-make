### TODO: try creating article with oregano diseases found with full paths
### TODO: get all targets from oregano and resolve the names (find dataset)

import os
import json
import sqlite3

from neo4j import GraphDatabase

from lib import g
from lib import io

neo4j_user = io.file_read(f'{g.DATABASE_FOLDERPATH}/neo4j-user.txt').strip()
neo4j_pass = io.file_read(f'{g.DATABASE_FOLDERPATH}/neo4j-pass.txt').strip()

def tsv_to_json(input_filepath):
    content = io.file_read(input_filepath)
    lines = content.split('\n')
    headings = lines[0].split('\t')
    # headings[0] = 'ID'
    items = []
    for line_i, line in enumerate(lines[:]):
        # print(line_i)
        if line_i == 0: continue
        if line.strip() == '': continue
        values = line.split('\t')
        item = {}
        for i in range(len(headings)):
            item[headings[i]] = values[i].strip()
        items.append(item)
    return items

def json__items_preview(json_filepath, num_items=10):
    items = io.json_read(json_filepath)
    for item in items[:num_items]:
        print(item)
    json_filename = json_filepath.split('/')[-1]
    print(f'{num_items}/{len(items)} - {json_filename}')
    print()

def analytics__oregano_compounds_print():
    if 0:
        input_filepath = (
            f'{g.SSOT_FOLDERPATH}/datasets/oregano/oregano-master/Integration/Integration V3/GESTION_ID/COMPOUND.tsv'
        )
        items = tsv_to_json(input_filepath)
        drugbank = []
        atc = []
        drugs_product_database = []
        pubchem_substance = []
        wikipedia = []
        pubchem_compound = []
        for i, item in enumerate(items[:]):
            print(f'{i}/{len(items)}')
            # print(json.dumps(item, indent=4))
            # quit()
            if item['DRUGBANK'].strip() != '': drugbank.append(item['DRUGBANK'])
            if item['ATC'].strip() != '': atc.append(item['ATC'])
            if item['DRUGS PRODUCT DATABASE '].strip() != '': drugs_product_database.append(item['DRUGS PRODUCT DATABASE '])
            if item['PUBCHEM SUBSTANCE'].strip() != '': pubchem_substance.append(item['PUBCHEM SUBSTANCE'])
            if item['WIKIPEDIA'].strip() != '': wikipedia.append(item['WIKIPEDIA'])
            if item['PUBCHEM COMPOUND'].strip() != '': pubchem_compound.append(item['PUBCHEM COMPOUND'])
        drugbank_perc = len(drugbank) / len(items) * 100.0
        atc_perc = len(atc) / len(items) * 100.0
        drugs_product_database_perc = len(drugs_product_database) / len(items) * 100.0
        pubchem_substance_perc = len(pubchem_substance) / len(items) * 100.0
        wikipedia_perc = len(wikipedia) / len(items) * 100.0
        pubchem_compound_perc = len(pubchem_compound) / len(items) * 100.0
        print(len(drugbank), '/', len(items), f'{drugbank_perc:.2f}%', '''DRUGBANK''')
        print(len(atc), '/', len(items), f'{atc_perc:.2f}%', '''ATC''')
        print(len(drugs_product_database), '/', len(items), f'{drugs_product_database_perc:.2f}%', 'DRUGS PRODUCT DATABASE')
        print(len(pubchem_substance), '/', len(items), f'{pubchem_substance_perc:.2f}%', '''PUBCHEM SUBSTANCE''')
        print(len(wikipedia), '/', len(items), f'{wikipedia_perc:.2f}%', '''WIKIPEDIA''')
        print(len(pubchem_compound), '/', len(items), f'{pubchem_compound_perc:.2f}%', '''PUBCHEM COMPOUND''')
    else:
        rows = sqlite3__table_get('oregano_compounds')[:]
        items = [{'ID': row[0], 'PUBCHEM COMPOUND': row[1]} for row in rows]
        pubchem_compound = []
        for i, item in enumerate(items[:]):
            print(f'''{i}/{len(items)} - {item['PUBCHEM COMPOUND']}''')
            # print(json.dumps(item, indent=4))
            # quit()
            if item['PUBCHEM COMPOUND'].strip() != '': pubchem_compound.append(item['PUBCHEM COMPOUND'])
        pubchem_compound_perc = len(pubchem_compound) / len(items) * 100.0
        print(len(pubchem_compound), '/', len(items), f'{pubchem_compound_perc:.2f}%', '''PUBCHEM COMPOUND''')
        print()

def json__oregano_compound_has_target_protein_create():
    ### get relevant triples
    tvs_lines = io.file_read(
        f'{g.SSOT_FOLDERPATH}/datasets/oregano/oregano-master/Data_OREGANO/Graphs/OREGANO_V3.tsv'
    ).split('\n')
    triples = []
    for line_i, line in enumerate(tvs_lines[:]):
        print(f'{line_i}/{len(tvs_lines)}')
        try: chunk_1, chunk_2, chunk_3 = line.split('\t')
        except: continue
        if chunk_2.lower() != 'has_target'.lower(): continue
        if 'PROTEIN'.lower() not in chunk_3.lower(): continue
        triple = [chunk_1, chunk_2, chunk_3]
        print(triple)
        # quit()
        triples.append(triple)
    for triple in triples:
        print(triple)
    print(len(triples))
    ### deduplicate triples
    seen = set()
    unique = []
    for lst in triples:
        t = tuple(lst)
        if t not in seen:
            seen.add(t)
            unique.append(lst)
    print(len(unique))
    ### triples to json
    triples_items = []
    for triple in unique[:]:
        triple_item = {
            'compound_id': triple[0],
            'relationship': triple[1],
            'protein_id': triple[2],
        }
        triples_items.append(triple_item)
    io.json_write(
        f'{g.SSOT_FOLDERPATH}/datasets/oregano/compound-has_target-protein.json',
        triples_items,
    )

def json__oregano_relationship_create(relationship_kind='acts_within'):
    ### get relevant triples
    tvs_lines = io.file_read(
        f'{g.SSOT_FOLDERPATH}/datasets/oregano/oregano-master/Data_OREGANO/Graphs/OREGANO_V3.tsv'
    ).split('\n')
    triples = []
    for line_i, line in enumerate(tvs_lines[:]):
        print(f'{line_i}/{len(tvs_lines)}')
        try: chunk_1, chunk_2, chunk_3 = line.split('\t')
        except: continue
        if chunk_2.lower() != relationship_kind.lower(): continue
        triple = [chunk_1, chunk_2, chunk_3]
        print(triple)
        # quit()
        triples.append(triple)
    for triple in triples:
        print(triple)
    print(len(triples))
    ### deduplicate triples
    seen = set()
    unique = []
    for lst in triples:
        t = tuple(lst)
        if t not in seen:
            seen.add(t)
            unique.append(lst)
    print(len(unique))
    ### triples to json
    triples_items = []
    for triple in unique[:]:
        triple_item = {
            'node1_id': triple[0],
            'relationship': triple[1],
            'node2_1': triple[2],
        }
        triples_items.append(triple_item)
    io.json_write(
        f'{g.SSOT_FOLDERPATH}/datasets/oregano/{relationship_kind}.json',
        triples_items,
    )

def sqlite3__table_get(table_name, id_1=None, id_2=None):
    if id_1 == None and id_2 == None:
        conn = sqlite3.connect(f'{g.SSOT_FOLDERPATH}/sqlite/database.db')
        cur = conn.cursor()
        cur.execute(f"SELECT * FROM {table_name}")
        rows = cur.fetchall()
        conn.close()
        return rows
    elif id_1 != None and id_2 != None:
        return None
    elif id_1 == None and id_2 != None:
        conn = sqlite3.connect(f'{g.SSOT_FOLDERPATH}/sqlite/database.db')
        cur = conn.cursor()
        query = f"SELECT * FROM {table_name} WHERE {id_2[0]} = ?"
        cur.execute(query, (id_2[1],))
        row = cur.fetchone()
        conn.close()
        return row
    elif id_1 != None and id_2 == None:
        conn = sqlite3.connect(f'{g.SSOT_FOLDERPATH}/sqlite/database.db')
        cur = conn.cursor()
        query = f"SELECT * FROM {table_name} WHERE {id_1[0]} = ?"
        cur.execute(query, (id_1[1],))
        row = cur.fetchone()
        conn.close()
        return row

def sqlite3__oregano_compound_diseases_create():
    ### get items
    items = io.json_read(f'{g.SSOT_FOLDERPATH}/datasets/oregano/compound-is_substance_that_treats-disease.json')
    ### create/populate sql table
    table_name = 'oregano_compounds_diseases'
    conn = sqlite3.connect(f'{g.SSOT_FOLDERPATH}/sqlite/database.db')
    cur = conn.cursor()
    ### delete previous table
    cur.execute(f"DROP TABLE IF EXISTS {table_name}")
    ### create new table
    cur.execute(f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            oregano_compound_id TEXT,
            oregano_disease_id TEXT
        )
    """)
    cur.execute("PRAGMA synchronous = OFF")
    cur.execute("PRAGMA journal_mode = MEMORY")
    cur.execute("PRAGMA temp_store = MEMORY")
    cur.execute("PRAGMA cache_size = 1000000")
    ## preview data
    for item_i, item in enumerate(items[:]):
        cur.execute(
            f"INSERT INTO {table_name} VALUES (?, ?)", 
            (item['compound_id'], item['disease_id'],)
        )
    ### create index
    cur.execute(f"CREATE INDEX IF NOT EXISTS idx_{table_name}_oregano_compound_id ON {table_name}(oregano_compound_id)")
    cur.execute(f"CREATE INDEX IF NOT EXISTS idx_{table_name}_oregano_disease_id ON {table_name}(oregano_disease_id)")
    conn.commit()
    conn.close()

def sqlite3__oregano_has_target_create():
    ### get items
    items = io.json_read(f'{g.SSOT_FOLDERPATH}/datasets/oregano/has_target.json')
    ### create/populate sql table
    table_name = 'oregano_has_target'
    conn = sqlite3.connect(f'{g.SSOT_FOLDERPATH}/sqlite/database.db')
    cur = conn.cursor()
    ### delete previous table
    cur.execute(f"DROP TABLE IF EXISTS {table_name}")
    ### create new table
    cur.execute(f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            oregano_compound_id TEXT,
            oregano_disease_id TEXT
        )
    """)
    cur.execute("PRAGMA synchronous = OFF")
    cur.execute("PRAGMA journal_mode = MEMORY")
    cur.execute("PRAGMA temp_store = MEMORY")
    cur.execute("PRAGMA cache_size = 1000000")
    ## preview data
    for item_i, item in enumerate(items[:]):
        cur.execute(
            f"INSERT INTO {table_name} VALUES (?, ?)", 
            (item['compound_id'], item['disease_id'],)
        )
    ### create index
    cur.execute(f"CREATE INDEX IF NOT EXISTS idx_{table_name}_oregano_compound_id ON {table_name}(oregano_compound_id)")
    cur.execute(f"CREATE INDEX IF NOT EXISTS idx_{table_name}_oregano_disease_id ON {table_name}(oregano_disease_id)")
    conn.commit()
    conn.close()


def sqlite3__table_preview(table_name, num_rows=10):
    conn = sqlite3.connect(f'{g.SSOT_FOLDERPATH}/sqlite/database.db')
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM {table_name}")
    rows = cur.fetchall()
    for row in rows[:num_rows]:
        print(row)
    cur.execute(f"SELECT COUNT(*) FROM {table_name}")
    row_count = cur.fetchone()[0]
    conn.close()
    print(f'{num_rows}/{row_count} - {table_name}')
    print()

def sqlite3__oregano_diseases_create(filtering=False):
    tsv_lines = io.file_read(
        f'{g.SSOT_FOLDERPATH}/datasets/oregano/oregano-master/Integration/Integration V3/GESTION_ID/DISEASES.tsv'
    ).split('\n')
    ###
    headings = tsv_lines[0].split('\t')
    headings[0] = 'ID'
    items = []
    for line_i, line in enumerate(tsv_lines[:]):
        # print(line_i)
        if line_i == 0: continue
        if line.strip() == '': continue
        values = line.split('\t')
        item = {}
        for i in range(len(headings)):
            item[headings[i]] = values[i].strip()
        # print(json.dumps(item, indent=4))
        # quit()
        mesh = item['MESH']
        if filtering:
            if mesh.strip() == '': continue
            if 'OMIM' in mesh.strip(): continue
            mesh = mesh.split(',')[0].strip()
            mesh = mesh.split(';')[0].strip()
            if mesh[0] == 'C': continue
        item = {
            'oregano_disease_id': item['ID'],
            'mesh_descriptor_ui': mesh,
        }
        items.append(item)
    ### create/populate sql table
    table_name = 'oregano_diseases'
    conn = sqlite3.connect(f'{g.SSOT_FOLDERPATH}/sqlite/database.db')
    cur = conn.cursor()
    ### delete previous table
    cur.execute(f"DROP TABLE IF EXISTS {table_name}")
    ### create new table
    cur.execute(f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            oregano_disease_id TEXT,
            mesh_descriptor_ui TEXT
        )
    """)
    cur.execute("PRAGMA synchronous = OFF")
    cur.execute("PRAGMA journal_mode = MEMORY")
    cur.execute("PRAGMA temp_store = MEMORY")
    cur.execute("PRAGMA cache_size = 1000000")
    ## preview data
    for item_i, item in enumerate(items[:]):
        print(item_i)
        cur.execute(
            f"INSERT INTO {table_name} VALUES (?, ?)", 
            (item['oregano_disease_id'], item['mesh_descriptor_ui'],)
        )
    ### create index
    cur.execute(f"CREATE INDEX IF NOT EXISTS idx_{table_name}_oregano_disease_id ON {table_name}(oregano_disease_id)")
    cur.execute(f"CREATE INDEX IF NOT EXISTS idx_{table_name}_mesh_descriptor_ui ON {table_name}(mesh_descriptor_ui)")
    conn.commit()
    conn.close()

def sqlite3__oregano_disease_name_get(_id):
    conn = sqlite3.connect(f'{g.SSOT_FOLDERPATH}/sqlite/database.db')
    cur = conn.cursor()
    cur.execute("""
        SELECT *
        FROM oregano_diseases t1
        JOIN mesh t2 ON t1.mesh_descriptor_ui = t2.mesh_descriptor_ui
        WHERE t1.oregano_disease_id = ?
    """, (_id,))
    rows = cur.fetchall()
    conn.close()
    return rows

def sqlite3__oregano_compounds_create():
    oregano_compounds_text = io.file_read(
        f'{g.SSOT_FOLDERPATH}/datasets/oregano/oregano-master/Integration/Integration V3/GESTION_ID/COMPOUND.tsv'
    )
    oregano_compounds_lines = oregano_compounds_text.split('\n')
    ###
    headings = oregano_compounds_lines[0].split('\t')
    headings[0] = 'ID_OREGANO'
    items = []
    for line_i, line in enumerate(oregano_compounds_lines[:]):
        # print(line_i)
        if line_i == 0: continue
        if line.strip() == '': continue
        values = line.split('\t')
        item = {}
        for i in range(len(headings)):
            item[headings[i]] = values[i].strip()
        # print(json.dumps(item, indent=4))
        # quit()
        pubchem_compound_id = item['PUBCHEM COMPOUND']
        if pubchem_compound_id.strip() == '': continue
        pubchem_compound_id = pubchem_compound_id.split(',')[0].strip()
        pubchem_compound_id = pubchem_compound_id.split(';')[0].strip()
        # print('ID:', item['ID_OREGANO'], 'CID:', pubchem_compound_id)
        item = {
            'oregano_compound_id': item['ID_OREGANO'],
            'pubchem_cid': pubchem_compound_id,
        }
        # print(item)
        items.append(item)
    ### create/populate sql table
    table_name = 'oregano_compounds'
    conn = sqlite3.connect(f'{g.SSOT_FOLDERPATH}/sqlite/database.db')
    cur = conn.cursor()
    ### delete previous table
    cur.execute(f"DROP TABLE IF EXISTS {table_name}")
    ### create new table
    cur.execute(f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            oregano_compound_id TEXT,
            pubchem_cid TEXT
        )
    """)
    cur.execute("PRAGMA synchronous = OFF")
    cur.execute("PRAGMA journal_mode = MEMORY")
    cur.execute("PRAGMA temp_store = MEMORY")
    cur.execute("PRAGMA cache_size = 1000000")
    ## preview data
    for item_i, item in enumerate(items[:]):
        print(item_i)
        cur.execute(
            f"INSERT INTO {table_name} VALUES (?, ?)", 
            (item['oregano_compound_id'], item['pubchem_cid'],)
        )
    ### create index
    cur.execute(f"CREATE INDEX IF NOT EXISTS idx_{table_name}_oregano_compound_id ON {table_name}(oregano_compound_id)")
    cur.execute(f"CREATE INDEX IF NOT EXISTS idx_{table_name}_pubchem_cid ON {table_name}(pubchem_cid)")
    conn.commit()
    conn.close()

def sqlite3__mesh_create():
    ### get data
    items = io.json_read(f'{g.SSOT_FOLDERPATH}/datasets/mesh/data.json')
    ## preview data
    for item in items[:10]:
        print(item)
    ### create/populate sql table
    table_name = 'mesh'
    conn = sqlite3.connect(f'{g.SSOT_FOLDERPATH}/sqlite/database.db')
    cur = conn.cursor()
    ### delete previous table
    cur.execute(f"DROP TABLE IF EXISTS {table_name}")
    ### create new table
    cur.execute(f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            mesh_descriptor_ui TEXT,
            mesh_name TEXT
        )
    """)
    cur.execute("PRAGMA synchronous = OFF")
    cur.execute("PRAGMA journal_mode = MEMORY")
    cur.execute("PRAGMA temp_store = MEMORY")
    cur.execute("PRAGMA cache_size = 1000000")
    ### insert into new table
    for item_i, item in enumerate(items[:]):
        # print(item_i)
        mesh_descriptor_ui = item['mesh_descriptor_ui'].strip()
        mesh_name = item['mesh_name'].strip()
        cur.execute(
            f"INSERT INTO {table_name} VALUES (?, ?)", 
            (
                mesh_descriptor_ui,
                mesh_name,
            )
        )
    ### create index
    cur.execute(f"CREATE INDEX IF NOT EXISTS idx_{table_name}_mesh_descriptor_ui ON {table_name}(mesh_descriptor_ui)")
    conn.commit()
    conn.close()

def sqlite3__pubchem_big_create():
    pubchem_cid_inchikey_filepath = f'{g.SSOT_FOLDERPATH}/datasets/pubchem/CID-InChI-Key'
    ###
    table_name = 'pubchem_big'
    conn = sqlite3.connect(f'{g.SSOT_FOLDERPATH}/datasets/pubchem/pubchem-big.db')
    cur = conn.cursor()
    ### delete previous table
    cur.execute(f"DROP TABLE IF EXISTS {table_name}")
    ### create new table
    cur.execute(f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            pubchem_cid TEXT,
            inchikey TEXT
        )
    """)
    cur.execute("PRAGMA synchronous = OFF")
    cur.execute("PRAGMA journal_mode = MEMORY")
    cur.execute("PRAGMA temp_store = MEMORY")
    cur.execute("PRAGMA cache_size = 1000000")
    with open(pubchem_cid_inchikey_filepath, "r") as f:
        for i, line in enumerate(f):
            parts = line.strip().split("\t")
            if len(parts) < 2:
                continue
            pubchem_cid, pubchem_inchikey = parts[0], parts[2]
            cur.execute(f"INSERT INTO {table_name} VALUES (?, ?)", (pubchem_cid, pubchem_inchikey))
            if i % 100000 == 0 and i != 0:
                conn.commit()
                print(f"{i} lines inserted")
    cur.execute(f"CREATE INDEX IF NOT EXISTS idx_{table_name}_pubchem_cid ON {table_name}(pubchem_cid)")
    cur.execute(f"CREATE INDEX IF NOT EXISTS idx_{table_name}_inchikey ON {table_name}(inchikey)")
    conn.commit()
    conn.close()

def sqlite3__pubchem_create():
    ### get rows
    rows = sqlite3__table_get('oregano_compounds')
    ### search them on big pubchem db and store them to another table on main db for future faster lookup
    rows_valid = []
    conn = sqlite3.connect(f'{g.SSOT_FOLDERPATH}/datasets/pubchem/pubchem-big.db')
    for row_i, row in enumerate(rows[:]):
        print(row_i)
        pubchem_cid = row[1]
        cur = conn.cursor()
        cur.execute("""
            SELECT *
            FROM pubchem_big
            WHERE pubchem_cid = ?
        """, (pubchem_cid,))
        record = cur.fetchone()
        # print(record)
        if record:
            rows_valid.append(record)
    conn.close()
    ### create/populate sql table
    table_name = 'pubchem'
    conn = sqlite3.connect(f'{g.SSOT_FOLDERPATH}/sqlite/database.db')
    cur = conn.cursor()
    ### delete previous table
    cur.execute(f"DROP TABLE IF EXISTS {table_name}")
    ### create new table
    cur.execute(f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            pubchem_cid TEXT,
            inchikey TEXT
        )
    """)
    cur.execute("PRAGMA synchronous = OFF")
    cur.execute("PRAGMA journal_mode = MEMORY")
    cur.execute("PRAGMA temp_store = MEMORY")
    cur.execute("PRAGMA cache_size = 1000000")
    ## preview data
    for row_i, row in enumerate(rows_valid[:]):
        print(row_i)
        cur.execute(
            f"INSERT INTO {table_name} VALUES (?, ?)", 
            (row[0], row[1],)
        )
    ### create index
    cur.execute(f"CREATE INDEX IF NOT EXISTS idx_{table_name}_pubchem_cid ON {table_name}(pubchem_cid)")
    cur.execute(f"CREATE INDEX IF NOT EXISTS idx_{table_name}_inchikey ON {table_name}(inchikey)")
    conn.commit()
    conn.close()

def sqlite3__oregano_disease_inchikey_get(_id):
    conn = sqlite3.connect(f'{g.SSOT_FOLDERPATH}/sqlite/database.db')
    cur = conn.cursor()
    cur.execute("""
        SELECT *
        FROM oregano_compounds t1
        JOIN pubchem t2 ON t1.pubchem_cid = t2.pubchem_cid
        WHERE t1.oregano_compound_id = ?
    """, (_id,))
    record = cur.fetchone()
    conn.close()
    return record

def sqlite3__oregano_compounds_pubchem_get_all():
    rows = sqlite3__table_get('oregano_compounds_diseases')
    conn = sqlite3.connect(f'{g.SSOT_FOLDERPATH}/sqlite/database.db')
    cur = conn.cursor()
    rows_found = []
    for row_i, row in enumerate(rows[:]):
        # print(row_i)
        oregano_compound_id = row[0]
        cur.execute("""
            SELECT *
            FROM oregano_compounds t1
            JOIN pubchem t2 ON t1.pubchem_cid = t2.pubchem_cid
            WHERE t1.oregano_compound_id = ?
        """, (oregano_compound_id,))
        record = cur.fetchone()
        if record:
            rows_found.append(record)
    conn.close()
    return rows_found

################################################################################
# [0002] LOTUS
################################################################################

def sqlite3__lotus_components_create():
    ### get data
    items = io.json_read(f'{g.SSOT_FOLDERPATH}/datasets/lotus/data.json')
    ## preview data
    for item in items[:1]:
        print(json.dumps(item, indent=4))
    return
    ### create/populate sql table
    table_name = 'lotus_components'
    conn = sqlite3.connect(f'{g.SSOT_FOLDERPATH}/sqlite/database.db')
    cur = conn.cursor()
    ### delete previous table
    cur.execute(f"DROP TABLE IF EXISTS {table_name}")
    ### create new table
    cur.execute(f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            lotus_id TEXT,
            inchikey TEXT,
            taxonomy_npclassifier_pathway TEXT,
            taxonomy_npclassifier_superclass TEXT,
            taxonomy_npclassifier_class TEXT,
            taxonomy_classyfire_kingdom TEXT,
            taxonomy_classyfire_superclass TEXT,
            taxonomy_classyfire_class TEXT,
            taxonomy_classyfire_parent TEXT
        )
    """)
    cur.execute("PRAGMA synchronous = OFF")
    cur.execute("PRAGMA journal_mode = MEMORY")
    cur.execute("PRAGMA temp_store = MEMORY")
    cur.execute("PRAGMA cache_size = 1000000")
    ### insert into new table
    for item_i, item in enumerate(items[:]):
        print(item_i)
        lotus_id = item['component_lotus_id'].strip()
        lotus_inchikey = item['component_inchikey'].strip()
        try: lotus_taxonomy_npclassifier_pathway = item['component_taxonomy_npclassifier_pathway'].strip()
        except: lotus_taxonomy_classifier_pathway = ''
        try: lotus_taxonomy_npclassifier_superclass = item['component_taxonomy_npclassifier_superclass'].strip()
        except: lotus_taxonomy_npclassifier_superclass = ''
        try: lotus_taxonomy_npclassifier_class = item['component_taxonomy_npclassifier_class'].strip()
        except: lotus_taxonomy_npclassifier_class = ''
        try: lotus_taxonomy_classyfire_kingdom = item['component_taxonomy_classyfire_kingdom'].strip()
        except: lotus_taxonomy_classyfire_kingdom = ''
        try: lotus_taxonomy_classyfire_superclass = item['component_taxonomy_classyfire_superclass'].strip()
        except: lotus_taxonomy_classyfire_superclass = ''
        try: lotus_taxonomy_classyfire_class = item['component_taxonomy_classyfire_class'].strip()
        except: lotus_taxonomy_classyfire_class = ''
        try: lotus_taxonomy_classyfire_parent = item['component_taxonomy_classyfire_parent'].strip()
        except: lotus_taxonomy_classyfire_parent = ''
        cur.execute(
            f"INSERT INTO {table_name} VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", 
            (
                lotus_id,
                lotus_inchikey,
                lotus_taxonomy_npclassifier_pathway,
                lotus_taxonomy_npclassifier_superclass,
                lotus_taxonomy_npclassifier_class,
                lotus_taxonomy_classyfire_kingdom,
                lotus_taxonomy_classyfire_superclass,
                lotus_taxonomy_classyfire_class,
                lotus_taxonomy_classyfire_parent,
            )
        )
    ### create index
    cur.execute(f"CREATE INDEX IF NOT EXISTS idx_{table_name}_lotus_id ON {table_name}(lotus_id)")
    cur.execute(f"CREATE INDEX IF NOT EXISTS idx_{table_name}_inchikey ON {table_name}(inchikey)")
    conn.commit()
    conn.close()

def sqlite3__oregano_compounds_lotus_get_all():
    rows = sqlite3__table_get('oregano_compounds_diseases')
    conn = sqlite3.connect(f'{g.SSOT_FOLDERPATH}/sqlite/database.db')
    cur = conn.cursor()
    rows_found = []
    for row_i, row in enumerate(rows[:]):
        # print(row_i)
        oregano_compound_id = row[0]
        cur.execute("""
            SELECT *
            FROM oregano_compounds t1
            JOIN pubchem t2 ON t1.pubchem_cid = t2.pubchem_cid
            JOIN lotus_components t3 ON t2.inchikey = t3.inchikey
            WHERE t1.oregano_compound_id = ?
        """, (oregano_compound_id,))
        record = cur.fetchone()
        if record:
            rows_found.append(record)
    conn.close()
    return rows_found

################################################################################
# [0000] WIKIDATA
################################################################################

def sqlite3__wikidata_create():
    ### get items
    plants_folderpath = f'{g.SSOT_FOLDERPATH}/datasets/wikidata/medicinal-plants'
    plants_filepaths = sorted([f'{plants_folderpath}/{filename}' for filename in os.listdir(plants_folderpath)])
    items = []
    for plant_filepath_i, plant_filepath in enumerate(plants_filepaths):
        print(f'{plant_filepath_i}/{len(plants_filepaths)}')
        plant_filename_raw = plant_filepath.split('/')[-1].split('.')[0]
        plant_data = io.json_read(plant_filepath)
        try: claim = plant_data['entities'][plant_filename_raw]['claims']['P5037'][0]
        except: claim = None
        if claim:
            value = claim['mainsnak']['datavalue']['value']
            value_url_id = value.split(':')[-1]
            items.append({
                'wikidata_id': plant_filename_raw,
                'powo_id': value,
            })
    ### sqlite
    table_name = 'wikidata'
    conn = sqlite3.connect(f'{g.SSOT_FOLDERPATH}/sqlite/database.db')
    cur = conn.cursor()
    ### delete previous table
    cur.execute(f"DROP TABLE IF EXISTS {table_name}")
    ### create new table
    cur.execute(f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            wikidata_id TEXT,
            powo_id TEXT
        )
    """)
    cur.execute("PRAGMA synchronous = OFF")
    cur.execute("PRAGMA journal_mode = MEMORY")
    cur.execute("PRAGMA temp_store = MEMORY")
    cur.execute("PRAGMA cache_size = 1000000")
    ### insert into new table
    for item_i, item in enumerate(items[:]):
        wikidata_id = item['wikidata_id'].strip()
        powo_id = item['powo_id'].strip()
        cur.execute(f"INSERT INTO {table_name} VALUES (?, ?)", (wikidata_id, powo_id))
    ### create index
    cur.execute(f"CREATE INDEX IF NOT EXISTS idx_{table_name}_wikidata_id ON {table_name}(wikidata_id)")
    conn.commit()
    conn.close()
    print(f"{item_i} lines inserted")

################################################################################
# [0001] POWO
################################################################################

def sqlite3__wcvp_create():
    items = io.csv_to_dict(f'{g.SSOT_FOLDERPATH}/datasets/powo/wcvp/wcvp_names.csv', delimiter='|')
    ### create/populate sql table
    table_name = 'wcvp'
    conn = sqlite3.connect(f'{g.SSOT_FOLDERPATH}/sqlite/database.db')
    cur = conn.cursor()
    ### delete previous table
    cur.execute(f"DROP TABLE IF EXISTS {table_name}")
    ### create new table
    cur.execute(f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            taxon_name TEXT,
            powo_id TEXT
        )
    """)
    cur.execute("PRAGMA synchronous = OFF")
    cur.execute("PRAGMA journal_mode = MEMORY")
    cur.execute("PRAGMA temp_store = MEMORY")
    cur.execute("PRAGMA cache_size = 1000000")
    ### insert into new table
    for item_i, item in enumerate(items[:]):
        taxon_name = item['taxon_name'].strip()
        powo_id = item['powo_id'].strip()
        cur.execute(f"INSERT INTO {table_name} VALUES (?, ?)", (taxon_name, powo_id,))
        if item_i % 100000 == 0:
            conn.commit()
            print(f"{item_i} lines inserted")
    ### create index
    cur.execute(f"CREATE INDEX IF NOT EXISTS idx_{table_name}_taxon_name ON {table_name}(taxon_name)")
    cur.execute(f"CREATE INDEX IF NOT EXISTS idx_{table_name}_powo_id ON {table_name}(powo_id)")
    conn.commit()
    print(f"{item_i} lines inserted")
    conn.close()

def sqlite3__wcvp_get(taxon_name):
    conn = sqlite3.connect(f'{g.SSOT_FOLDERPATH}/sqlite/database.db')
    cur = conn.cursor()
    cur.execute("""
        SELECT *
        FROM wcvp
        WHERE taxon_name = ?
    """, (taxon_name,))
    row = cur.fetchone()
    conn.close()
    return row

def sqlite3__powo_create():
    ### get all wikidata medicinal plants, only use these to create powo table
    conn = sqlite3.connect(f'{g.SSOT_FOLDERPATH}/sqlite/database.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM wikidata")
    rows = cur.fetchall()
    conn.close()
    ### get all powo plants data
    items = []
    for row_i, row in enumerate(rows[:]):
        print(f'{row_i}/{len(rows)}')
        powo_plant_id_end = row[1].split(':')[-1].strip()
        powo_plant_filepath = f'''{g.SSOT_FOLDERPATH}/datasets/powo/plants/{powo_plant_id_end}.json'''
        if not os.path.exists(powo_plant_filepath): continue
        powo_plant_data = io.json_read(powo_plant_filepath)
        powo_plant_kingdom = powo_plant_data['kingdom']
        powo_plant_phylum = powo_plant_data['phylum']
        powo_plant_class = powo_plant_data['clazz']
        powo_plant_subclass = powo_plant_data['subclass']
        powo_plant_order = powo_plant_data['order']
        powo_plant_family = powo_plant_data['family']
        powo_plant_genus = powo_plant_data['genus']
        try: powo_plant_species = powo_plant_data['species']
        except: powo_plant_species = ''
        powo_plant_name = powo_plant_data['name']
        powo_plant_rank = powo_plant_data['rank']
        _powo_plant = {
            'powo_plant_id': row[1],
            'powo_plant_kingdom': powo_plant_kingdom,
            'powo_plant_phylum': powo_plant_phylum,
            'powo_plant_class': powo_plant_class,
            'powo_plant_subclass': powo_plant_subclass,
            'powo_plant_order': powo_plant_order,
            'powo_plant_family': powo_plant_family,
            'powo_plant_genus': powo_plant_genus,
            'powo_plant_species': powo_plant_species,
            'powo_plant_name': powo_plant_name,
            'powo_plant_rank': powo_plant_rank,
        }
        items.append(_powo_plant)
    ### create/populate sql table
    table_name = 'powo'
    conn = sqlite3.connect(f'{g.SSOT_FOLDERPATH}/sqlite/database.db')
    cur = conn.cursor()
    ### delete previous table
    cur.execute(f"DROP TABLE IF EXISTS {table_name}")
    ### create new table
    cur.execute(f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            powo_id TEXT,
            powo_kingdom TEXT,
            powo_phylum TEXT,
            powo_class TEXT,
            powo_subclass TEXT,
            powo_order TEXT,
            powo_family TEXT,
            powo_genus TEXT,
            powo_species TEXT,
            powo_name TEXT,
            powo_rank TEXT
        )
    """)
    cur.execute("PRAGMA synchronous = OFF")
    cur.execute("PRAGMA journal_mode = MEMORY")
    cur.execute("PRAGMA temp_store = MEMORY")
    cur.execute("PRAGMA cache_size = 1000000")
    ### insert into new table
    for item_i, item in enumerate(items[:]):
        powo_id = item['powo_plant_id'].strip()
        powo_kingdom = item['powo_plant_kingdom'].strip()
        powo_phylum = item['powo_plant_phylum'].strip()
        powo_class = item['powo_plant_class'].strip()
        powo_subclass = item['powo_plant_subclass'].strip()
        powo_order = item['powo_plant_order'].strip()
        powo_family = item['powo_plant_family'].strip()
        powo_genus = item['powo_plant_genus'].strip()
        powo_species = item['powo_plant_species'].strip()
        powo_name = item['powo_plant_name'].strip()
        powo_rank = item['powo_plant_rank'].strip()
        cur.execute(f"INSERT INTO {table_name} VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (powo_id, powo_kingdom, powo_phylum, powo_class, powo_subclass, powo_order, powo_family, powo_genus, powo_species, powo_name, powo_rank,))
        if item_i % 100000 == 0:
            conn.commit()
            print(f"{item_i} lines inserted")
    ### create index
    cur.execute(f"CREATE INDEX IF NOT EXISTS idx_{table_name}_powo_id ON {table_name}(powo_id)")
    conn.commit()
    print(f"{item_i} lines inserted")
    conn.close()

################################################################################
# [0000_0001] WIKIDATA_POWO
################################################################################

def sqlite3__wikidata_powo_get_all():
    rows = sqlite3__table_get('wikidata')
    conn = sqlite3.connect(f'{g.SSOT_FOLDERPATH}/sqlite/database.db')
    cur = conn.cursor()
    rows_found = []
    for row_i, row in enumerate(rows[:]):
        # print(row_i)
        wikidata_id = row[0]
        cur.execute("""
            SELECT *
            FROM wikidata t1
            JOIN powo t2 ON t1.powo_id = t2.powo_id
            WHERE t1.wikidata_id = ?
        """, (wikidata_id,))
        record = cur.fetchone()
        if record:
            rows_found.append(record)
    conn.close()
    return rows_found

################################################################################
# [9999] TERRA
################################################################################

def sqlite3__terra_compounds_lotus_create():
    ### get all plants from lotus table
    rows = io.json_read(f'{g.SSOT_FOLDERPATH}/datasets/lotus/terra-lotus-maps.json')
    ### create/populate terra plants table
    table_name = 'terra_compounds_lotus'
    conn = sqlite3.connect(f'{g.SSOT_FOLDERPATH}/sqlite/database.db')
    cur = conn.cursor()
    ### delete previous table
    cur.execute(f"DROP TABLE IF EXISTS {table_name}")
    ### create new table
    cur.execute(f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            terra_compound_id TEXT,
            lotus_id TEXT
        )
    """)
    cur.execute("PRAGMA synchronous = OFF")
    cur.execute("PRAGMA journal_mode = MEMORY")
    cur.execute("PRAGMA temp_store = MEMORY")
    cur.execute("PRAGMA cache_size = 1000000")
    ### insert into new table
    for row_i, row in enumerate(rows[:]):
        terra_compound_id = row['terra_compound_id']
        lotus_id = row['lotus_id']
        cur.execute(f"INSERT INTO {table_name} VALUES (?, ?)", (terra_compound_id, lotus_id))
    ### create index
    cur.execute(f"CREATE INDEX IF NOT EXISTS idx_{table_name}_terra_compound_id ON {table_name}(terra_compound_id)")
    cur.execute(f"CREATE INDEX IF NOT EXISTS idx_{table_name}_lotus_id ON {table_name}(lotus_id)")
    conn.commit()
    print(f"{len(rows)} lines inserted")
    conn.close()

def sqlite3__terra_lotus_get_all():
    rows = sqlite3__table_get('terra_compounds_lotus')
    conn = sqlite3.connect(f'{g.SSOT_FOLDERPATH}/sqlite/database.db')
    cur = conn.cursor()
    rows_found = []
    for row_i, row in enumerate(rows[:]):
        # print(row_i)
        terra_compound_id = row[0]
        cur.execute("""
            SELECT *
            FROM terra_compounds_lotus t1
            JOIN lotus_components t2 ON t1.lotus_id = t2.lotus_id
            WHERE t1.terra_compound_id = ?
        """, (terra_compound_id,))
        record = cur.fetchone()
        if record:
            rows_found.append(record)
    conn.close()
    return rows_found

def sqlite3__terra_lotus_pubchem_get_all():
    rows = sqlite3__table_get('terra_compounds_lotus')
    conn = sqlite3.connect(f'{g.SSOT_FOLDERPATH}/sqlite/database.db')
    cur = conn.cursor()
    rows_found = []
    for row_i, row in enumerate(rows[:]):
        # print(row_i)
        terra_compound_id = row[0]
        cur.execute("""
            SELECT *
            FROM terra_compounds_lotus t1
            JOIN lotus_components t2 ON t1.lotus_id = t2.lotus_id
            JOIN pubchem t3 ON t2.inchikey = t3.inchikey
            WHERE t1.terra_compound_id = ?
        """, (terra_compound_id,))
        record = cur.fetchone()
        if record:
            rows_found.append(record)
    conn.close()
    return rows_found

def sqlite3__terra_lotus_pubchem_oregano_get_all():
    rows = sqlite3__table_get('terra_compounds_lotus')
    conn = sqlite3.connect(f'{g.SSOT_FOLDERPATH}/sqlite/database.db')
    cur = conn.cursor()
    rows_found = []
    for row_i, row in enumerate(rows[:]):
        # print(row_i)
        terra_compound_id = row[0]
        cur.execute("""
            SELECT *
            FROM terra_compounds_lotus t1
            JOIN lotus_components t2 ON t1.lotus_id = t2.lotus_id
            JOIN pubchem t3 ON t2.inchikey = t3.inchikey
            JOIN oregano_compounds t4 ON t3.pubchem_cid = t4.pubchem_cid
            WHERE t1.terra_compound_id = ?
        """, (terra_compound_id,))
        record = cur.fetchone()
        if record:
            rows_found.append(record)
    conn.close()
    return rows_found

def sqlite3__terra_lotus_pubchem_oregano_relationship_get_all():
    rows = sqlite3__table_get('terra_compounds_lotus')
    conn = sqlite3.connect(f'{g.SSOT_FOLDERPATH}/sqlite/database.db')
    cur = conn.cursor()
    rows_found = []
    for row_i, row in enumerate(rows[:]):
        # print(row_i)
        terra_compound_id = row[0]
        cur.execute("""
            SELECT *
            FROM terra_compounds_lotus t1
            JOIN lotus_components t2 ON t1.lotus_id = t2.lotus_id
            JOIN pubchem t3 ON t2.inchikey = t3.inchikey
            JOIN oregano_compounds t4 ON t3.pubchem_cid = t4.pubchem_cid
            JOIN oregano_compounds_diseases t5 ON t4.oregano_compound_id = t5.oregano_compound_id
            WHERE t1.terra_compound_id = ?
        """, (terra_compound_id,))
        record = cur.fetchone()
        if record:
            rows_found.append(record)
    conn.close()
    return rows_found

def sqlite3__terra_lotus_pubchem_oregano_relationship_disease_get_all():
    rows = sqlite3__table_get('terra_compounds_lotus')
    conn = sqlite3.connect(f'{g.SSOT_FOLDERPATH}/sqlite/database.db')
    cur = conn.cursor()
    rows_found = []
    for row_i, row in enumerate(rows[:]):
        # print(row_i)
        terra_compound_id = row[0]
        cur.execute("""
            SELECT *
            FROM terra_compounds_lotus t1
            JOIN lotus_components t2 ON t1.lotus_id = t2.lotus_id
            JOIN pubchem t3 ON t2.inchikey = t3.inchikey
            JOIN oregano_compounds t4 ON t3.pubchem_cid = t4.pubchem_cid
            JOIN oregano_compounds_diseases t5 ON t4.oregano_compound_id = t5.oregano_compound_id
            JOIN oregano_diseases t6 ON t5.oregano_disease_id = t6.oregano_disease_id
            WHERE t1.terra_compound_id = ?
        """, (terra_compound_id,))
        record = cur.fetchone()
        if record:
            rows_found.append(record)
    conn.close()
    return rows_found

def sqlite3__terra_lotus_pubchem_oregano_relationship_disease_mesh_get_all():
    rows = sqlite3__table_get('terra_compounds_lotus')
    conn = sqlite3.connect(f'{g.SSOT_FOLDERPATH}/sqlite/database.db')
    cur = conn.cursor()
    rows_found = []
    for row_i, row in enumerate(rows[:]):
        # print(row_i)
        terra_compound_id = row[0]
        cur.execute("""
            SELECT *
            FROM terra_compounds_lotus t1
            JOIN lotus_components t2 ON t1.lotus_id = t2.lotus_id
            JOIN pubchem t3 ON t2.inchikey = t3.inchikey
            JOIN oregano_compounds t4 ON t3.pubchem_cid = t4.pubchem_cid
            JOIN oregano_compounds_diseases t5 ON t4.oregano_compound_id = t5.oregano_compound_id
            JOIN oregano_diseases t6 ON t5.oregano_disease_id = t6.oregano_disease_id
            JOIN mesh t7 ON t6.mesh_descriptor_ui = t7.mesh_descriptor_ui
            WHERE t1.terra_compound_id = ?
        """, (terra_compound_id,))
        record = cur.fetchone()
        if record:
            rows_found.append(record)
    conn.close()
    return rows_found

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

def neo4j__terra_plants_compounds_create():
    rows = io.json_read(f'{g.SSOT_FOLDERPATH}/datasets/terra/plants-compounds.json')
    ### populate kg
    driver = GraphDatabase.driver("bolt://localhost:7687", auth=(neo4j_user, neo4j_pass))
    def insert_relationships(tx, rows):
        tx.run("""
            UNWIND $rows AS row
            MERGE (s:Plant {id: row.terra_plant_id})
            MERGE (o:Compound {id: row.terra_compound_id})
            MERGE (s)-[:HAS_COMPOUND]->(o)
        """, rows=rows)
    with driver.session() as session:
        session.run("""
            CREATE CONSTRAINT plant_id IF NOT EXISTS
            FOR (p:Plant)
            REQUIRE p.id IS UNIQUE
        """)
        session.run("""
            CREATE CONSTRAINT compound_id IF NOT EXISTS
            FOR (c:Compound)
            REQUIRE c.id IS UNIQUE
        """)
        session.execute_write(insert_relationships, rows)
    driver.close()

def neo4j__terra_plants_compounds_create_new_temp():
    # rows = io.json_read(f'{g.SSOT_FOLDERPATH}/datasets/terra/plants-compounds.json')
    rows = sqlite3__terra_lotus_pubchem_oregano_get_all()
    rows = [{'terra_plant_id': row[0], 'oregano_compound_id': row[-2], 'oregano_compound_type': row[-2].split(':')[0]} for row in rows]
    print(rows[0])
    print(len(rows))
    plants = set()
    for row in rows:
        plants.add(row['terra_plant_id'])
    print(list(plants)[0])
    print(len(plants))
    quit()
    ### populate kg
    driver = GraphDatabase.driver("bolt://localhost:7687", auth=(neo4j_user, neo4j_pass))
    def insert_relationships(tx, rows):
        tx.run("""
            UNWIND $rows AS row
            MERGE (s:Plant {id: row.terra_plant_id})
            MERGE (o:Entity {id: row.oregano_compound_id, type: row.oregano_compound_type})
            MERGE (s)-[:HAS_COMPOUND]->(o)
        """, rows=rows)
    with driver.session() as session:
        session.run("""
            CREATE CONSTRAINT plant_id IF NOT EXISTS
            FOR (p:Plant)
            REQUIRE p.id IS UNIQUE
        """)
        session.run("""
            CREATE CONSTRAINT compound_id IF NOT EXISTS
            FOR (c:Compound)
            REQUIRE c.id IS UNIQUE
        """)
        session.execute_write(insert_relationships, rows)
    driver.close()

def neo4j__terra_plants_compounds_get():
    driver = GraphDatabase.driver("bolt://localhost:7687", auth=(neo4j_user, neo4j_pass))
    def _get(tx):
        result = tx.run("""
            MATCH (p:Plant)-[:HAS_COMPOUND]->(c:Compound)
            RETURN p.id AS plant, c.id AS compound
        """)
        return [(r["plant"], r["compound"]) for r in result]
    with driver.session() as session:
        results = session.execute_read(_get)
    driver.close()
    return results

def sqlite3__terra_plant_name_get(terra_id):
    conn = sqlite3.connect(f'{g.SSOT_FOLDERPATH}/sqlite/database.db')
    cur = conn.cursor()
    cur.execute("""
        SELECT t3.powo_name
        FROM terra_plants t1
        JOIN wikidata t2 ON t1.wikidata_id = t2.wikidata_id
        JOIN powo t3 ON t2.powo_id = t3.powo_id
        WHERE t1.terra_id = ?
    """, (terra_id,))
    row = cur.fetchone()
    conn.close()
    return row[0] if row else None

def sqlite3__terra_compound_name_get(terra_id):
    conn = sqlite3.connect(f'{g.SSOT_FOLDERPATH}/sqlite/database.db')
    cur = conn.cursor()
    cur.execute("""
        SELECT 
            t2.lotus_id,
            t2.inchikey,
            t2.taxonomy_npclassifier_pathway,
            t2.taxonomy_npclassifier_superclass,
            t2.taxonomy_npclassifier_class,
            t2.taxonomy_classyfire_kingdom,
            t2.taxonomy_classyfire_superclass,
            t2.taxonomy_classyfire_class,
            t2.taxonomy_classyfire_parent
        FROM terra_compounds_lotus t1
        JOIN lotus_components t2 ON t1.lotus_compound_id = t2.lotus_id
        WHERE t1.terra_compound_id = ?
    """, (terra_id,))
    row = cur.fetchone()
    best_name = None
    inchikey = row[1]
    taxonomy_npclassifier_pathway = row[2]
    taxonomy_npclassifier_superclass = row[3]
    taxonomy_npclassifier_class = row[4]
    taxonomy_classyfire_kingdom = row[5]
    taxonomy_classyfire_superclass = row[6]
    taxonomy_classyfire_class = row[7]
    taxonomy_classyfire_parent = row[8]
    if taxonomy_classyfire_parent != None or taxonomy_classyfire_parent != '': best_name = taxonomy_classyfire_parent
    elif taxonomy_classyfire_class != None or taxonomy_classyfire_class != '': best_name = taxonomy_classyfire_class
    elif taxonomy_classyfire_superclass != None or taxonomy_classyfire_superclass != '': best_name = taxonomy_classyfire_superclass
    elif taxonomy_classyfire_kingdom != None or taxonomy_classyfire_kingdom != '': best_name = taxonomy_classyfire_kingdom
    elif taxonomy_npclassifier_class != None or taxonomy_npclassifier_class != '': best_name = taxonomy_npclassifier_class
    elif taxonomy_npclassifier_superclass != None or taxonomy_npclassifier_superclass != '': best_name = taxonomy_npclassifier_superclass
    elif taxonomy_npclassifier_pathway != None or taxonomy_npclassifier_pathway != '': best_name = taxonomy_npclassifier_pathway
    conn.close()
    return best_name 

################################################################################
# [0004] OREGANO
################################################################################

def oregano__neo4j_create():
    from collections import defaultdict
    driver = GraphDatabase.driver("bolt://localhost:7687", auth=(neo4j_user, neo4j_pass))
    oregano_relationships_filepath = f'{g.SSOT_FOLDERPATH}/datasets/oregano/oregano-master/Data_OREGANO/Graphs/OREGANO_V3.tsv'
    def batch_insert_grouped(tx, grouped_batch):
        for rel_type, rows in grouped_batch.items():
            query = f"""
            UNWIND $rows AS row
            WITH row,
                 split(row.s, ":")[0] AS s_type,
                 split(row.s, ":")[1] AS s_id,
                 split(row.o, ":")[0] AS o_type,
                 split(row.o, ":")[1] AS o_id
            MERGE (s:Entity {{id: row.s}})
            SET s.type = s_type
            MERGE (o:Entity {{id: row.o}})
            SET o.type = o_type
            MERGE (s)-[:{rel_type}]->(o)
            """
            tx.run(query, rows=rows)
    batch = defaultdict(list)
    batch_size = 5000
    with open(oregano_relationships_filepath) as f:
        with driver.session() as session:
            session.run("CREATE INDEX entity_id IF NOT EXISTS FOR (n:Entity) ON (n.id)")
            for line in f:
                s, p, o = line.strip().split("\t")
                if p == "rdf/type":
                    continue
                batch[p].append({"s": s, "o": o})
                if sum(len(v) for v in batch.values()) >= batch_size:
                    session.execute_write(batch_insert_grouped, batch)
                    batch.clear()
                    print(batch_size)
            if batch:
                session.execute_write(batch_insert_grouped, batch)
    driver.close()

### OREGANO: COMPOUNDS --> DISEASES
# json__items_preview(f'{g.SSOT_FOLDERPATH}/datasets/oregano/compound-is_substance_that_treats-disease.json', num_items=1)
# sqlite3__oregano_compound_diseases_create()
### sqlite3__oregano_has_target_create()
# sqlite3__table_preview('oregano_compounds_diseases', num_rows=1)
# print(sqlite3__table_get('oregano_compounds_diseases', id_1=['oregano_compound_id', 'COMPOUND:131204']))

### --- BRANCH DISEASE ---

### OREGANO: DISEASES

### OREGANO: MESH
# sqlite3__mesh_create()
# sqlite3__table_preview('mesh', num_rows=1)

### OREGANO: DISEASES NAMES CHECK (good number of names found)
if 0:
    rows = sqlite3__table_get('oregano_compounds_diseases')
    # names_found = []
    for i, row in enumerate(rows):
        print(f'{i}/{len(rows)}')
        res = sqlite3__oregano_disease_name_get(row[1])
        # if res != []:
            # names_found.append(res)
        print(res)
        quit()
    # print(f'FOUND: {len(names_found)}')
    # print(f'MISSING: {len(rows) - len(names_found)}')
    # print(f'TOTAL: {len(rows)}')
    # for name in names_found[:5]:
        # print(name)
    quit()

### --- BRANCH COMPOUNDS ---

################################################################################
# [0000] WIKIDATA
################################################################################

if 0:
    # sqlite3__wikidata_create()
    sqlite3__table_preview('wikidata', num_rows=1)

################################################################################
# [0001] POWO
################################################################################

if 0:
    # sqlite3__wcvp_create()
    # print(sqlite3__wcvp_get('Lindera strychifolia'))
    # print(sqlite3__wcvp_get('Viola striis-notata'))
    # sqlite3__table_preview('wcvp', num_rows=1)
    # sqlite3__powo_create()
    sqlite3__table_preview('powo', num_rows=1)

################################################################################
# [0002] LOTUS
################################################################################

if 0:
    # sqlite3__lotus_components_create()
    sqlite3__table_preview('lotus_components', num_rows=1)

################################################################################
# [0004] OREGANO
################################################################################

if 0:
    oregano__neo4j_create()

### OREGANO: COMPOUNDS
if 0:
    analytics__oregano_compounds_print()
    sqlite3__oregano_compounds_create()
    sqlite3__table_preview('oregano_compounds', num_rows=10)

### OREGANO: PUBCHEM
# sqlite3__pubchem_big_create()
# sqlite3__pubchem_create()
# sqlite3__table_preview('pubchem', num_rows=10)

### OREGANO: COMPOUNDS --> PUBCHEM (((tmp)))
# rows = sqlite3__oregano_compounds_pubchem_get_all()
# print(rows[0])
# print(len(rows), 'oregano --> pubchem')
# print()

### OREGANO: COMPOUNDS --> LOTUS ***milestone***
# rows = sqlite3__oregano_compounds_lotus_get_all()
# print(rows[0])
# print(len(rows), 'oregano --> lotus')
# print()

### OREGANO: DISEASES
if 0:
    sqlite3__oregano_diseases_create()
    sqlite3__table_preview('oregano_diseases', num_rows=10000)

# -- OREGANO: RELATIONSHIPS ANALYTICS --
if 0:
    # json__oregano_compound_diseases_create()
    relationship_kind = 'acts_within'
    # json__oregano_relationship_create(relationship_kind=relationship_kind)
    items = io.json_read(f'{g.SSOT_FOLDERPATH}/datasets/oregano/{relationship_kind}.json')
    for item in items[:1]:
        print(item)
    print(len(items), '\n')
    ###
    relationship_kind = 'causes_condition'
    # json__oregano_relationship_create(relationship_kind=relationship_kind)
    items = io.json_read(f'{g.SSOT_FOLDERPATH}/datasets/oregano/{relationship_kind}.json')
    for item in items[:1]:
        print(item)
    print(len(items), '\n')
    ###
    relationship_kind = 'downregulates'
    # json__oregano_relationship_create(relationship_kind=relationship_kind)
    items = io.json_read(f'{g.SSOT_FOLDERPATH}/datasets/oregano/{relationship_kind}.json')
    for item in items[:1]:
        print(item)
    print(len(items), '\n')
    ###
    relationship_kind = 'gene_product_of'
    # json__oregano_relationship_create(relationship_kind=relationship_kind)
    items = io.json_read(f'{g.SSOT_FOLDERPATH}/datasets/oregano/{relationship_kind}.json')
    for item in items[:1]:
        print(item)
    print(len(items), '\n')
    ###
    relationship_kind = 'has_code'
    # json__oregano_relationship_create(relationship_kind=relationship_kind)
    items = io.json_read(f'{g.SSOT_FOLDERPATH}/datasets/oregano/{relationship_kind}.json')
    for item in items[:1]:
        print(item)
    print(len(items), '\n')
    ###
    relationship_kind = 'has_indication'
    # json__oregano_relationship_create(relationship_kind=relationship_kind)
    items = io.json_read(f'{g.SSOT_FOLDERPATH}/datasets/oregano/{relationship_kind}.json')
    for item in items[:1]:
        print(item)
    print(len(items), '\n')
    ###
    relationship_kind = 'has_phenotype'
    # json__oregano_relationship_create(relationship_kind=relationship_kind)
    items = io.json_read(f'{g.SSOT_FOLDERPATH}/datasets/oregano/{relationship_kind}.json')
    for item in items[:1]:
        print(item)
    print(len(items), '\n')
    ###
    relationship_kind = 'has_side_effect'
    # json__oregano_relationship_create(relationship_kind=relationship_kind)
    items = io.json_read(f'{g.SSOT_FOLDERPATH}/datasets/oregano/{relationship_kind}.json')
    for item in items[:1]:
        print(item)
    print(len(items), '\n')
    ###
    relationship_kind = 'has_target'
    # json__oregano_relationship_create(relationship_kind=relationship_kind)
    items = io.json_read(f'{g.SSOT_FOLDERPATH}/datasets/oregano/{relationship_kind}.json')
    for item in items[:1]:
        print(item)
    print(len(items), '\n')
    ###
    relationship_kind = 'interacts_with'
    # json__oregano_relationship_create(relationship_kind=relationship_kind)
    items = io.json_read(f'{g.SSOT_FOLDERPATH}/datasets/oregano/{relationship_kind}.json')
    for item in items[:1]:
        print(item)
    print(len(items), '\n')
    ###
    relationship_kind = 'involved_in'
    # json__oregano_relationship_create(relationship_kind=relationship_kind)
    items = io.json_read(f'{g.SSOT_FOLDERPATH}/datasets/oregano/{relationship_kind}.json')
    for item in items[:1]:
        print(item)
    print(len(items), '\n')
    ###
    relationship_kind = 'is_affecting'
    # json__oregano_relationship_create(relationship_kind=relationship_kind)
    items = io.json_read(f'{g.SSOT_FOLDERPATH}/datasets/oregano/{relationship_kind}.json')
    for item in items[:1]:
        print(item)
    print(len(items), '\n')
    ###
    relationship_kind = 'is_substance_that_treats'
    # json__oregano_relationship_create(relationship_kind=relationship_kind)
    items = io.json_read(f'{g.SSOT_FOLDERPATH}/datasets/oregano/{relationship_kind}.json')
    for item in items[:1]:
        print(item)
    print(len(items), '\n')
    ###
    relationship_kind = 'part_of'
    # json__oregano_relationship_create(relationship_kind=relationship_kind)
    items = io.json_read(f'{g.SSOT_FOLDERPATH}/datasets/oregano/{relationship_kind}.json')
    for item in items[:1]:
        print(item)
    print(len(items), '\n')
    ###
    relationship_kind = 'participates_in'
    # json__oregano_relationship_create(relationship_kind=relationship_kind)
    items = io.json_read(f'{g.SSOT_FOLDERPATH}/datasets/oregano/{relationship_kind}.json')
    for item in items[:1]:
        print(item)
    print(len(items), '\n')
    ###
    relationship_kind = 'reaction_of'
    # json__oregano_relationship_create(relationship_kind=relationship_kind)
    items = io.json_read(f'{g.SSOT_FOLDERPATH}/datasets/oregano/{relationship_kind}.json')
    for item in items[:1]:
        print(item)
    print(len(items), '\n')
    ###
    relationship_kind = 'upregulates'
    # json__oregano_relationship_create(relationship_kind=relationship_kind)
    items = io.json_read(f'{g.SSOT_FOLDERPATH}/datasets/oregano/{relationship_kind}.json')
    for item in items[:1]:
        print(item)
    print(len(items), '\n')
    quit()


################################################################################
# [0000_0001] WIKIDATA_POWO
################################################################################

if 0:
    rows = sqlite3__wikidata_powo_get_all()
    print(rows[0], '\n', len(rows), 'wikidata --> powo', '\n')

################################################################################
# [9999] TERRA
################################################################################

if 0:
    sqlite3__terra_compounds_lotus_create()
    sqlite3__table_preview('terra_compounds_lotus', num_rows=1)
    # rows = sqlite3__terra_lotus_get_all()
    # print(rows[0], '\n', len(rows), 'terra --> lotus', '\n')
    # rows = sqlite3__terra_lotus_pubchem_get_all()
    # print(rows[0], '\n', len(rows), 'terra --> lotus --> pubchem', '\n')
    # rows = sqlite3__terra_lotus_pubchem_oregano_get_all()
    # print(rows[0], '\n', len(rows), 'terra --> lotus --> pubchem --> oregano', '\n')
    # rows = sqlite3__terra_lotus_pubchem_oregano_relationship_get_all()
    # print(rows[0], '\n', len(rows), 'terra --> lotus --> pubchem --> oregano --> relationship', '\n')
    # rows = sqlite3__terra_lotus_pubchem_oregano_relationship_disease_get_all()
    # print(rows[0], '\n', len(rows), 'terra --> lotus --> pubchem --> oregano --> relationship --> disease', '\n')
    # rows = sqlite3__terra_lotus_pubchem_oregano_relationship_disease_mesh_get_all()
    # print(rows[0], '\n', len(rows), 'terra --> lotus --> pubchem --> oregano --> relationship --> disease --> mesh', '\n')
    # for row in rows:
        # print(row[-1])

    # neo4j__clear()
    # neo4j__terra_plants_compounds_create()
    # neo4j__terra_plants_compounds_create_new_temp()
    # Nodes (146,828)
    # Relationships (3,601,505)
    pass

def neo4j__oregano__compounds_diseases__get():
    driver = GraphDatabase.driver("bolt://localhost:7687", auth=(neo4j_user, neo4j_pass))
    def run(tx):
        rows = sqlite3__terra_lotus_pubchem_oregano_get_all()
        print(rows[0], '\n', len(rows), 'terra --> lotus --> pubchem --> oregano', '\n')
        print(rows[0][-2])
        diseases = set()
        print(len(rows))
        compound_ids = [row[-2] for row in rows]
        '''
        query = """
            MATCH (c:Entity)
            WHERE c.id IN $compound_ids
            OPTIONAL MATCH (c)-[*1..6]->(d:Entity {type: "DISEASE"})
            WITH c, collect(DISTINCT d.id) AS diseases
            RETURN c.id AS compound, diseases
        """
        result = tx.run(query, {"compound_ids": compound_ids})
        for record in result:
            print(
                record["compound"],
                record["disease_paths"]
            )
        quit()
        '''

        for row_i, row in enumerate(rows[:]):
            print(f'{row_i}/{len(rows)}')
            query = f"""
                MATCH p = (s:Entity {{id: "{row[-2]}"}}) -[*1..6]-> (o:Entity {{type: "DISEASE"}})
                RETURN p
            """
            query = f"""
                MATCH (c:Entity {{id: "{row[-2]}"}})
                MATCH (c)-[*1..4]->(d:Entity {{type: "DISEASE"}})
                RETURN DISTINCT d.id AS disease
            """
            # print(query)
            result = tx.run(query)
            records_row_count = []
            for i, record in enumerate(result):
                # print(i)
                disease_id = record.data()['disease']
                '''
                continue
                ###
                path = record["p"]
                parts = []
                # first node
                first_node = path.nodes[0]
                first_type = first_node.get("id", "UNKNOWN")
                parts.append(first_type)
                # relationships + next nodes
                for rel, node in zip(path.relationships, path.nodes[1:]):
                    rel_type = rel.type
                    node_type = node.get("id", "UNKNOWN")
                    parts.append(f"{rel_type}")
                    parts.append(node_type)
                # print(f"Path {i}:")
                # print(" ".join(parts))
                # print("-" * 80)
                # quit()
                records.append(parts)
                records_row_count.append(parts)
                '''
                records_row_count.append(disease_id)
                diseases.add(disease_id)
                # quit()
            # print(len(records_row_count))
        # for record in records:
            # print(record)
        print(len(diseases))
        diseases_items = [{'oregano_disease_id': val} for val in diseases]
        for disease in diseases_items:
            print(disease)
        io.json_write(f'{g.SSOT_FOLDERPATH}/oregano/tmp.json', diseases_items)
    with driver.session() as session:
        results = session.execute_read(run)
    driver.close()

# neo4j__oregano__compounds_diseases__get()

# -- NAME RESOLUTION --

if 0:
    if 0:
        rows = neo4j__terra_plants_compounds_get()
        for i, row in enumerate(rows[:1000]):
            print(f'{i}/{len(rows)}')
            print(row)
            print(sqlite3__terra_plant_name_get(row[0]))
            print(sqlite3__terra_compound_name_get(row[1]))
            quit()
    if 1:
        sqlite3__oregano_diseases_create(filtering=False)
        sqlite3__oregano_diseases_create(filtering=True)
        sqlite3__table_preview('oregano_diseases', num_rows=1)
        # quit()
        items = io.json_read(f'{g.SSOT_FOLDERPATH}/oregano/tmp.json')
        found = []
        for i, item in enumerate(items[:]):
            print(f'{i}/{len(items)}')
            print(item)
            disease_id = item['oregano_disease_id']
            print(disease_id)
            row = sqlite3__oregano_disease_name_get(disease_id)
            print(row)
            if row != []:
                found.append(row)
        for val in found:
            print(val)
        print(len(found), 'found names')
            # quit()

