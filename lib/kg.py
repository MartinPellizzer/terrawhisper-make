import sqlite3

from neo4j import GraphDatabase

from lib import g
from lib import io

neo4j_user = io.file_read(f'{g.DATABASE_FOLDERPATH}/neo4j-user.txt').strip()
neo4j_pass = io.file_read(f'{g.DATABASE_FOLDERPATH}/neo4j-pass.txt').strip()

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

def sqlite3__terra_plant_taxonomy_get(terra_id):
    conn = sqlite3.connect(f'{g.SSOT_FOLDERPATH}/sqlite/database.db')
    cur = conn.cursor()
    cur.execute("""
        SELECT 
            t3.powo_kingdom,
            t3.powo_phylum,
            t3.powo_class,
            t3.powo_order,
            t3.powo_family,
            t3.powo_genus,
            t3.powo_species
        FROM terra_plants t1
        JOIN wikidata t2 ON t1.wikidata_id = t2.wikidata_id
        JOIN powo t3 ON t2.powo_id = t3.powo_id
        WHERE t1.terra_id = ?
    """, (terra_id,))
    row = cur.fetchone()
    conn.close()
    return row

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
        JOIN lotus_components t2 ON t1.lotus_id = t2.lotus_id
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


def neo4j__study_plants_get():
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
            MATCH (s:PLANT)-[p:CONTAINS]->(o:COMPOUND)
            WHERE s.id = $plant_name
            RETURN s.id AS plant, o.id AS compound, p.source_id AS source
            ORDER BY compound
        """, plant_name=plant_name)
        rows = [dict(record) for record in result]
    driver.close()
    return rows

def neo4j__get_plant_health_problems(plant_name):
    driver = GraphDatabase.driver("bolt://localhost:7687", auth=(neo4j_user, neo4j_pass))
    with driver.session() as session:
        result = session.run("""
            MATCH (s:PLANT)-[p:TREATS]->(o:HEALTH_PROBLEM)
            WHERE s.id = $plant_name
            RETURN s.id AS plant, o.id AS health_problem, p.source_id AS source
            ORDER BY health_problem
        """, plant_name=plant_name)
        rows = [dict(record) for record in result]
    driver.close()
    return rows

def neo4j__get_plant_conditions(plant_name):
    driver = GraphDatabase.driver("bolt://localhost:7687", auth=(neo4j_user, neo4j_pass))
    with driver.session() as session:
        result = session.run("""
            MATCH (s:PLANT)-[p:USED_FOR]->(o:CONDITION)
            WHERE s.id = $plant_name
            RETURN s.id AS plant, o.id AS condition, p.source_id AS source
            ORDER BY condition
        """, plant_name=plant_name)
        rows = [dict(record) for record in result]
    driver.close()
    return rows

def neo4j__get_rows(plant_name, node_1, relationship, node_2, node_1_as, node_2_as):
    driver = GraphDatabase.driver("bolt://localhost:7687", auth=(neo4j_user, neo4j_pass))
    with driver.session() as session:
        result = session.run(f"""
            MATCH (s:{node_1})-[p:{relationship}]->(o:{node_2})
            WHERE s.id = $plant_name
            RETURN s.id AS {node_1_as}, o.id AS {node_2_as}, p.source_id AS source
            ORDER BY {node_2_as}
        """, plant_name=plant_name)
        rows = [dict(record) for record in result]
    driver.close()
    return rows

