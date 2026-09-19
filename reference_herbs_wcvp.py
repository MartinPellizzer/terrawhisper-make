import os
import time
import json

import sqlite3
import csv
import re
import unicodedata
import time

from lib import g
from lib import io

HUB_FOLDERPATH = f'''{g.DATA_FOLDERPATH}/herbs'''

wcvp_table_name = f'wcvp_plants_names'

def normalize_plant_name(name):
    # Common botanical author abbreviations (extend over time)
    AUTHOR_PATTERNS = [
        r"\bL\.\b",
        r"\bLinn\.\b",
        r"\bDC\.\b",
        r"\bHook\.?\s*f?\.?\b",
        r"\bBenth\.\b",
        r"\bWilld\.\b",
        r"\bMill\.\b",
        r"\bLam\.\b",
        r"\bRoxb\.\b",
    ]
    AUTHOR_REGEX = re.compile("|".join(AUTHOR_PATTERNS), re.IGNORECASE)
    if not name:
        return ""
    # Unicode normalization
    name = unicodedata.normalize("NFKC", name)
    # lowercase
    name = name.lower()
    # normalize hybrid sign
    name = name.replace("×", " x ")
    # remove botanical author citations
    name = AUTHOR_REGEX.sub("", name)
    # remove punctuation except letters, numbers and spaces
    name = re.sub(r"[.,;:()\[\]{}]", " ", name)
    # collapse whitespace
    name = re.sub(r"\s+", " ", name).strip()
    return name

def wcvp_table_plants_names_create():
    input_folderpath = f'{HUB_FOLDERPATH}/fetch/wcvp/wcvp'
    output_folderpath = f'{HUB_FOLDERPATH}/reference/wcvp'
    io.folders_recursive_gen(output_folderpath)

    conn = sqlite3.connect(f"{output_folderpath}/wcvp.db")


    conn.executescript(f"""
    PRAGMA journal_mode = OFF;
    PRAGMA synchronous = OFF;
    PRAGMA temp_store = MEMORY;
    PRAGMA cache_size = -500000;

    DROP TABLE IF EXISTS {wcvp_table_name};

    CREATE TABLE {wcvp_table_name} (
        plant_name_id TEXT NOT NULL,
        accepted_plant_name_id TEXT NOT NULL,
        taxon_status TEXT NOT NULL,
        taxon_name TEXT NOT NULL,
        taxon_name_normalized TEXT NOT NULL,
        powo_id TEXT,
        ipni_id TEXT
    );
    """)

    conn.commit()

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
            # print(json.dumps(row, indent=4))
            # quit() 

            plant_name_id =             row["plant_name_id"]
            accepted_plant_name_id =    row["accepted_plant_name_id"]
            taxon_status =              row["taxon_status"]
            taxon_name =                row["taxon_name"]
            taxon_name_normalized =     normalize_plant_name(taxon_name)
            powo_id =                   row["powo_id"]
            ipni_id =                   row["ipni_id"]
            if not taxon_name:
                continue

            batch.append((
                plant_name_id,
                accepted_plant_name_id,
                taxon_status,
                taxon_name,
                taxon_name_normalized,
                powo_id,
                ipni_id,
            ))

            if len(batch) >= BATCH_SIZE:
                conn.executemany(f"""
                    INSERT INTO {wcvp_table_name}
                    (
                        plant_name_id,
                        accepted_plant_name_id,
                        taxon_status,
                        taxon_name,
                        taxon_name_normalized,
                        powo_id,
                        ipni_id
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, batch)

                processed += len(batch)

                if processed % 1000000 == 0:
                    elapsed = time.time() - start
                    print(f"{processed:,} inserted ({elapsed:.1f}s)")

                batch.clear()

        if batch:
            conn.executemany(f"""
                INSERT INTO {wcvp_table_name}
                (
                        plant_name_id,
                        accepted_plant_name_id,
                        taxon_status,
                        taxon_name,
                        taxon_name_normalized,
                        powo_id,
                        ipni_id
                )
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, batch)

    conn.commit()

    # Create lookup index AFTER import
    conn.execute(f"""
        CREATE INDEX idx_{wcvp_table_name}_plant_name_id
        ON {wcvp_table_name}(plant_name_id)
    """)
    conn.execute(f"""
        CREATE INDEX idx_{wcvp_table_name}_accepted_plant_name_id
        ON {wcvp_table_name}(accepted_plant_name_id)
    """)
    conn.execute(f"""
        CREATE INDEX idx_{wcvp_table_name}_taxon_name_normalized
        ON {wcvp_table_name}(taxon_name_normalized)
    """)
    conn.execute(f"""
        CREATE INDEX idx_{wcvp_table_name}_powo_id
        ON {wcvp_table_name}(powo_id)
    """)
    conn.execute(f"""
        CREATE INDEX idx_{wcvp_table_name}_ipni_id
        ON {wcvp_table_name}(ipni_id)
    """)

    conn.commit()
    cursor = conn.execute(f"""
        SELECT *
        FROM {wcvp_table_name}
        LIMIT 10
    """)
    for row in cursor:
        print(row)
    conn.close()

    print("Done")

def peek():
    ### TEST PRINT
    conn = sqlite3.connect(f"{HUB_FOLDERPATH}/reference/wcvp/wcvp.db")
    cursor = conn.execute(f"""
        SELECT *
        FROM {wcvp_table_name}
        LIMIT 10
    """)
    rows = cursor.fetchall()
        # print(row)

    from tabulate import tabulate
    print(tabulate(rows, 
        headers=[
            "PLANT_NAME_ID", 
            "ACCEPTED_PLANT_NAME_ID", 
            "TAXON_STATUS", 
            "TAXON_NAME", 
            "TAXON_NAME_NORMALIZED",
            "POWO_ID",
            "IPNI_ID",
        ], 
        tablefmt="plain")
    )

def run():
    print(f'REFERENCE >> wcvp')

    start = time.perf_counter()
    wcvp_table_plants_names_create()
    # peek()
    print(f'wcvp table_plants_names_create() - execution time: ', time.perf_counter() - start)


