import os
import time
import json
import sys

import sqlite3
import csv
import re
import unicodedata
import time

from lib import g
from lib import io

import normalize_utils

def table_species_create():
    input_folderpath = f'{g.DATA_FOLDERPATH}/fetch/gift'
    output_folderpath = f'{g.DATA_FOLDERPATH}/reference/gift'
    io.folders_recursive_gen(output_folderpath)

    conn = sqlite3.connect(f"{output_folderpath}/gift.db")

    table_name = 'species'
    conn.executescript(
    f"""
        PRAGMA journal_mode = OFF;
        PRAGMA synchronous = OFF;
        PRAGMA temp_store = MEMORY;
        PRAGMA cache_size = -500000;

        DROP TABLE IF EXISTS {table_name};

        CREATE TABLE {table_name} (
            work_id TEXT NOT NULL,
            genus_id TEXT NOT NULL,
            work_genus TEXT NOT NULL,
            work_species TEXT NOT NULL,
            work_author TEXT,
            work_species_norm TEXT NOT NULL
        );
    """)

    conn.commit()

    csv.field_size_limit(sys.maxsize)

    BATCH_SIZE = 100000
    processed = 0
    start = time.time()
    conn.execute("BEGIN")
    with open(
        f"{input_folderpath}/species.csv",
        "r",
        encoding="utf8",
        errors="ignore",
        newline="",
    ) as f:
        reader = csv.DictReader(f, delimiter=",")
        batch = []
        for row in reader:
            # print(json.dumps(row, indent=4))
            # quit() 

            work_id = row["work_ID"]
            genus_id = row["genus_ID"]
            work_genus = row["work_genus"]
            work_species = row["work_species"]
            work_author = row["work_author"]
            work_species_norm = normalize_utils.normalize_plant_name(work_species)

            batch.append((
                work_id,
                genus_id,
                work_genus,
                work_species,
                work_author,
                work_species_norm,
            ))

            if len(batch) >= BATCH_SIZE:
                conn.executemany(
                f"""
                    INSERT INTO {table_name}
                    (
                        work_id,
                        genus_id,
                        work_genus,
                        work_species,
                        work_author,
                        work_species_norm
                    )
                    VALUES (?, ?, ?, ?, ?, ?)
                """, batch)

                processed += len(batch)

                if processed % 1000000 == 0:
                    elapsed = time.time() - start
                    print(f"{processed:,} inserted ({elapsed:.1f}s)")

                batch.clear()

        if batch:
            conn.executemany(
            f"""
                INSERT INTO {table_name}
                (
                        work_id,
                        genus_id,
                        work_genus,
                        work_species,
                        work_author,
                        work_species_norm
                )
                VALUES (?, ?, ?, ?, ?, ?)
            """, batch)

    conn.commit()

    # Create lookup index AFTER import
    conn.execute(
    f"""
        CREATE INDEX idx_{table_name}_work_id
        ON {table_name}(work_id)
    """)
    conn.execute(
    f"""
        CREATE INDEX idx_{table_name}_genus_id
        ON {table_name}(genus_id)
    """)
    conn.execute(
    f"""
        CREATE INDEX idx_{table_name}_work_species
        ON {table_name}(work_species)
    """)
    conn.execute(
    f"""
        CREATE INDEX idx_{table_name}_work_species_norm
        ON {table_name}(work_species_norm)
    """)

    conn.commit()
    cursor = conn.execute(
    f"""
        SELECT *
        FROM {table_name}
        LIMIT 10
    """)
    for row in cursor:
        print(row)
    conn.close()


def table_traits_create():
    input_folderpath = f'{g.DATA_FOLDERPATH}/fetch/gift/traits'
    output_folderpath = f'{g.DATA_FOLDERPATH}/reference/gift'
    io.folders_recursive_gen(output_folderpath)

    conn = sqlite3.connect(f"{output_folderpath}/gift.db")

    table_name = 'traits'
    conn.executescript(
    f"""
        PRAGMA journal_mode = OFF;
        PRAGMA synchronous = OFF;
        PRAGMA temp_store = MEMORY;
        PRAGMA cache_size = -500000;

        DROP TABLE IF EXISTS {table_name};

        CREATE TABLE {table_name} (
            work_id TEXT NOT NULL,
            trait_id TEXT NOT NULL,
            trait_value TEXT NOT NULL,
            agreement TEXT,
            coeff_var TEXT,
            n TEXT,
            refs TEXT
        );
    """)

    conn.commit()

    csv.field_size_limit(sys.maxsize)

    BATCH_SIZE = 100000
    processed = 0
    start = time.time()
    conn.execute("BEGIN")

    query = f"""
        INSERT INTO {table_name}
        (
            work_id,
            trait_id,
            trait_value,
            agreement,
            coeff_var,
            n,
            refs
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """
    # filenames = sorted(os.listdir(input_folderpath))
    filenames = os.listdir(input_folderpath)
    for filename_i, filename in enumerate(filenames):
        print(f'{filename_i}/{len(filenames)} - {filename}')
        
        # filename = 'trait_1_1_1.csv'
        with open(
            f"{input_folderpath}/{filename}",
            "r",
            encoding="utf8",
            errors="ignore",
            newline="",
        ) as f:
            reader = csv.DictReader(f, delimiter=",")
            batch = []
            for row in reader:
                # print(json.dumps(row, indent=4))
                # quit() 

                work_id = row["work_ID"]
                trait_id = filename.split('.')[0].replace('trait_', '').replace('_', '.')
                trait_value = row["trait_value"]
                agreement = row["agreement"]
                coeff_var = row["coeff_var"]
                n = row["n"]
                references = row["references"]

                batch.append((
                    work_id,
                    trait_id,
                    trait_value,
                    agreement,
                    coeff_var,
                    n,
                    references,
                ))

                if len(batch) >= BATCH_SIZE:
                    conn.executemany(query, batch)

                    processed += len(batch)

                    if processed % 1000000 == 0:
                        elapsed = time.time() - start
                        print(f"{processed:,} inserted ({elapsed:.1f}s)")

                    batch.clear()

            if batch:
                conn.executemany(query, batch)

        conn.commit()

    # Create lookup index AFTER import
    conn.execute(
    f"""
        CREATE INDEX idx_{table_name}_work_id
        ON {table_name}(work_id)
    """)

    conn.commit()
    cursor = conn.execute(
    f"""
        SELECT *
        FROM {table_name}
        LIMIT 10
    """)
    for row in cursor:
        print(row)
    conn.close()


def table_traits_meta_create():
    input_folderpath = f'{g.DATA_FOLDERPATH}/fetch/gift'
    output_folderpath = f'{g.DATA_FOLDERPATH}/reference/gift'
    io.folders_recursive_gen(output_folderpath)

    conn = sqlite3.connect(f"{output_folderpath}/gift.db")

    table_name = 'traits_meta'
    conn.executescript(
    f"""
        PRAGMA journal_mode = OFF;
        PRAGMA synchronous = OFF;
        PRAGMA temp_store = MEMORY;
        PRAGMA cache_size = -500000;

        DROP TABLE IF EXISTS {table_name};

        CREATE TABLE {table_name} (
            lvl1 TEXT NOT NULL,
            category TEXT NOT NULL,
            lvl2 TEXT NOT NULL,
            trait1 TEXT NOT NULL,
            lvl3 TEXT NOT NULL,
            trait2 TEXT NOT NULL,
            units TEXT,
            type TEXT,
            comment TEXT,
            count TEXT
        );
    """)

    conn.commit()

    csv.field_size_limit(sys.maxsize)

    BATCH_SIZE = 100000
    processed = 0
    start = time.time()
    conn.execute("BEGIN")

    query = f"""
        INSERT INTO {table_name}
        (
            lvl1,
            category,
            lvl2,
            trait1,
            lvl3,
            trait2,
            units,
            type,
            comment,
            count
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """

    with open(
        f"{input_folderpath}/traits_meta.csv",
        "r",
        encoding="utf8",
        errors="ignore",
        newline="",
    ) as f:
        reader = csv.DictReader(f, delimiter=",")
        batch = []
        for row in reader:
            # print(json.dumps(row, indent=4))
            # quit() 

            lvl1 = row["Lvl1"]
            category = row["Category"]
            lvl2 = row["Lvl2"]
            trait1 = row["Trait1"]
            lvl3 = row["Lvl3"]
            trait2 = row["Trait2"]
            units = row["Units"]
            _type = row["type"]
            comment = row["comment"]
            count = row["count"]

            batch.append((
                lvl1,
                category,
                lvl2,
                trait1,
                lvl3,
                trait2,
                units,
                _type,
                comment,
                count,
            ))

            if len(batch) >= BATCH_SIZE:
                conn.executemany(query, batch)

                processed += len(batch)

                if processed % 1000000 == 0:
                    elapsed = time.time() - start
                    print(f"{processed:,} inserted ({elapsed:.1f}s)")

                batch.clear()

        if batch:
            conn.executemany(query, batch)

    conn.commit()

    # Create lookup index AFTER import
    conn.execute(
    f"""
        CREATE INDEX idx_{table_name}_lvl3
        ON {table_name}(lvl3)
    """)

    conn.commit()
    cursor = conn.execute(
    f"""
        SELECT *
        FROM {table_name}
        LIMIT 10
    """)
    for row in cursor:
        print(row)
    conn.close()


def run():
    print(f'''HERBS >> REFERENCE >> gift''')

    if 0:
        start = time.perf_counter()
        table_species_create()
        print(f'table species_create() - execution time: ', time.perf_counter() - start)

    if 0:
        start = time.perf_counter()
        table_traits_create()
        print(f'table traits_create() - execution time: ', time.perf_counter() - start)

    if 0:
        start = time.perf_counter()
        table_traits_meta_create()
        print(f'table traits_create() - execution time: ', time.perf_counter() - start)

