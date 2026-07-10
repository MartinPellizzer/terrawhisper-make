import os
import time

from lib import g
from lib import io

def pubchem__table_synonyms_create():
    source_foldername = 'pubchem'
    input_foldername = 'fetch'
    output_foldername = 'reference'
    input_folderpath = f'{g.VAULT_FOLDERPATH}/terrawhisper/data/{input_foldername}/{source_foldername}'
    output_folderpath = f'{g.VAULT_FOLDERPATH}/terrawhisper/data/{output_foldername}/{source_foldername}'
    io.folders_recursive_gen(output_folderpath)
    # with open(f'{input_folderpath}/CID-Synonym-unfiltered') as f: content = f.read()[:100]
    # lines = content.split('\n')

    ### CREATE TABLE
    import sqlite3
    conn = sqlite3.connect(f"{output_folderpath}/pubchem.db")
    conn.executescript("""
        PRAGMA journal_mode = OFF;
        PRAGMA synchronous = OFF;
        PRAGMA temp_store = MEMORY;
        PRAGMA locking_mode = EXCLUSIVE;
        PRAGMA cache_size = -500000;
        DROP TABLE IF EXISTS pubchem_cid_synonyms;
        CREATE TABLE pubchem_cid_synonyms (
            cid INTEGER NOT NULL,
            alias TEXT NOT NULL,
            normalized_alias TEXT NOT NULL
        );
    """)

    ### NORMALIZE FUNCTION
    import re
    import unicodedata
    spaces = re.compile(r"\s+")
    def normalize(name):
        name = unicodedata.normalize("NFKC", name)
        name = name.lower()
        name = name.replace("-", " ")
        name = spaces.sub(" ", name)
        return name.strip()

    ### ADD RECORDS
    import gzip
    from itertools import islice
    import time
    BATCH_SIZE = 100_000
    start = time.time()
    processed = 0
    conn.execute("BEGIN")
    with gzip.open(f"{input_folderpath}/CID-Synonym-unfiltered.gz", "rt", encoding="utf8", errors="ignore") as f:
        batch = []
        count = 0
        for line in f:
            cid, alias = line.rstrip("\n").split("\t", 1)
            batch.append((
                int(cid),
                alias,
                normalize(alias)
            ))
            # count += 1
            # if count >= 1000000:      # <-- TEST LIMIT
                # break
            if len(batch) >= BATCH_SIZE:
                conn.executemany(
                    """
                        INSERT INTO pubchem_cid_synonyms
                        VALUES (?, ?, ?)
                    """,
                    batch
                )
                processed += len(batch)
                if processed % 1_000_000 == 0:
                    elapsed = time.time() - start
                    print(f"{processed:,} inserted ({elapsed:.1f}s)")
                batch.clear()
        if batch:
            conn.executemany(
                """
                    INSERT INTO pubchem_cid_synonyms
                    VALUES (?, ?, ?)
                """,
                batch
            )
    conn.commit()

    ### CREATE INDEXES
    print("Creating index...")
    conn.execute("""
    CREATE INDEX idx_pubchem_cid_synonyms_alias
    ON pubchem_cid_synonyms(normalized_alias)
    """)
    conn.execute("""
    CREATE INDEX idx_pubchem_cid_synonyms_cid
    ON pubchem_cid_synonyms(cid)
    """)
    conn.commit()

    ### TEST PRINT
    cursor = conn.execute("""
    SELECT cid, alias, normalized_alias
    FROM pubchem_cid_synonyms
    LIMIT 100
    """)
    for row in cursor:
        print(row)

def run():
    print(f'PARSE >> pubchem')

    start = time.perf_counter()
    pubchem__table_synonyms_create()
    print(f'pubchem__table_synonyms_create() - execution time: ', time.perf_counter() - start)
