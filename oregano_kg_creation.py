from neo4j import GraphDatabase

from lib import g
from lib import io

neo4j_user = io.file_read(f'{g.DATABASE_FOLDERPATH}/neo4j-user.txt').strip()
neo4j_pass = io.file_read(f'{g.DATABASE_FOLDERPATH}/neo4j-pass.txt').strip()

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

# oregano__neo4j_create()
