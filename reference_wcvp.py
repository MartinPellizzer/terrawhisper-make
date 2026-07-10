import os
import time

import sqlite3
import csv
import re
import unicodedata
import time


from lib import g
from lib import io

def wcvp_table_plants_create():
    source_foldername = 'wcvp'
    input_foldername = 'fetch'
    output_foldername = 'reference'
    input_folderpath = f'{g.VAULT_FOLDERPATH}/terrawhisper/data/{input_foldername}/{source_foldername}'
    output_folderpath = f'{g.VAULT_FOLDERPATH}/terrawhisper/data/{output_foldername}/{source_foldername}'
    io.folders_recursive_gen(output_folderpath)

    conn = sqlite3.connect(f"{output_folderpath}/wcvp.db")

    conn.executescript("""
    PRAGMA journal_mode = OFF;
    PRAGMA synchronous = OFF;
    PRAGMA temp_store = MEMORY;
    PRAGMA cache_size = -500000;

    DROP TABLE IF EXISTS wcvp;

    CREATE TABLE wcvp (
        taxon_name TEXT NOT NULL,
        taxon_name_normalized TEXT NOT NULL
    );
    """)

    conn.commit()


    spaces = re.compile(r"\s+")

    def normalize(name):
        name = unicodedata.normalize("NFKC", name)
        name = name.lower()
        name = name.replace("-", " ")
        name = re.sub(r"[.,]", "", name)
        name = spaces.sub(" ", name)
        return name.strip()


    BATCH_SIZE = 100000

    processed = 0
    start = time.time()

    conn.execute("BEGIN")

    with open(
        f"{input_folderpath}/wcvp_names.csv",
        "r",
        encoding="utf8",
        errors="ignore",
        newline="",
    ) as f:

        reader = csv.DictReader(f, delimiter="|")

        batch = []

        for row in reader:

            taxon_name = row["taxon_name"]

            if not taxon_name:
                continue

            batch.append((
                taxon_name,
                normalize(taxon_name)
            ))

            if len(batch) >= BATCH_SIZE:

                conn.executemany("""
                    INSERT INTO wcvp
                    (taxon_name, taxon_name_normalized)
                    VALUES (?, ?)
                """, batch)

                processed += len(batch)

                if processed % 1000000 == 0:
                    elapsed = time.time() - start
                    print(f"{processed:,} inserted ({elapsed:.1f}s)")

                batch.clear()


        if batch:
            conn.executemany("""
                INSERT INTO wcvp
                (taxon_name, taxon_name_normalized)
                VALUES (?, ?)
            """, batch)


    conn.commit()


    # Create lookup index AFTER import
    conn.execute("""
    CREATE INDEX idx_wcvp_taxon_name_normalized
    ON wcvp(taxon_name_normalized)
    """)

    conn.commit()

    print("Done")

def test():
    source_foldername = 'wcvp'
    output_foldername = 'reference'
    output_folderpath = f'{g.VAULT_FOLDERPATH}/terrawhisper/data/{output_foldername}/{source_foldername}'

    ### TEST PRINT
    conn = sqlite3.connect(f"{output_folderpath}/wcvp.db")
    cursor = conn.execute("""
    SELECT *
    FROM wcvp
    LIMIT 100
    """)
    for row in cursor:
        print(row)


def run():
    print(f'PARSE >> wcvp')

    start = time.perf_counter()
    # wcvp_table_plants_create()
    test()
    print(f'wcvp_table_plants_create() - execution time: ', time.perf_counter() - start)


