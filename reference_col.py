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

def table_name_usage_create():
    input_folderpath = f'{g.DATA_FOLDERPATH}/fetch/col/datasets'
    output_folderpath = f'{g.DATA_FOLDERPATH}/reference/col'
    io.folders_recursive_gen(output_folderpath)

    conn = sqlite3.connect(f"{output_folderpath}/col.db")

    table_name = 'name_usage'
    conn.executescript(
    f"""
        PRAGMA journal_mode = OFF;
        PRAGMA synchronous = OFF;
        PRAGMA temp_store = MEMORY;
        PRAGMA cache_size = -500000;

        DROP TABLE IF EXISTS {table_name};

        CREATE TABLE {table_name} (
            col_id TEXT NOT NULL,
            scientific_name TEXT NOT NULL,
            scientific_name_norm TEXT NOT NULL
        );
    """)

    conn.commit()

    csv.field_size_limit(sys.maxsize)

    BATCH_SIZE = 100000
    processed = 0
    start = time.time()
    conn.execute("BEGIN")
    with open(
        f"{input_folderpath}/NameUsage.tsv",
        "r",
        encoding="utf8",
        errors="ignore",
        newline="",
    ) as f:
        reader = csv.DictReader(f, delimiter="\t")
        batch = []
        for row in reader:
            # print(json.dumps(row, indent=4))
            # quit() 

            col_id = row["col:ID"]
            scientific_name = row["col:scientificName"]
            scientific_name_norm = normalize_utils.normalize_plant_name(scientific_name)

            if not scientific_name:
                continue

            batch.append((
                col_id,
                scientific_name,
                scientific_name_norm,
            ))

            if len(batch) >= BATCH_SIZE:
                conn.executemany(
                f"""
                    INSERT INTO {table_name}
                    (
                        col_id,
                        scientific_name,
                        scientific_name_norm
                    )
                    VALUES (?, ?, ?)
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
                        col_id,
                        scientific_name,
                        scientific_name_norm
                )
                VALUES (?, ?, ?)
            """, batch)

    conn.commit()

    # Create lookup index AFTER import
    conn.execute(
    f"""
        CREATE INDEX idx_{table_name}_col_id
        ON {table_name}(col_id)
    """)
    conn.execute(
    f"""
        CREATE INDEX idx_{table_name}_scientific_name
        ON {table_name}(scientific_name)
    """)
    conn.execute(
    f"""
        CREATE INDEX idx_{table_name}_scientific_name_norm
        ON {table_name}(scientific_name_norm)
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

def table_vernacular_name_create():
    input_folderpath = f'{g.DATA_FOLDERPATH}/fetch/col/datasets'
    output_folderpath = f'{g.DATA_FOLDERPATH}/reference/col'
    io.folders_recursive_gen(output_folderpath)

    conn = sqlite3.connect(f"{output_folderpath}/col.db")

    table_name = 'vernacular_name'
    conn.executescript(
    f"""
        PRAGMA journal_mode = OFF;
        PRAGMA synchronous = OFF;
        PRAGMA temp_store = MEMORY;
        PRAGMA cache_size = -500000;

        DROP TABLE IF EXISTS {table_name};

        CREATE TABLE {table_name} (
            col_id TEXT NOT NULL,
            name TEXT NOT NULL,
            transliteration TEXT,
            language TEXT,
            preferred TEXT,
            country TEXT,
            area TEXT
        );
    """)

    conn.commit()

    csv.field_size_limit(sys.maxsize)

    BATCH_SIZE = 100000
    processed = 0
    start = time.time()
    conn.execute("BEGIN")
    with open(
        f"{input_folderpath}/VernacularName.tsv",
        "r",
        encoding="utf8",
        errors="ignore",
        newline="",
    ) as f:
        reader = csv.DictReader(f, delimiter="\t")
        batch = []
        for row in reader:
            # print(json.dumps(row, indent=4))
            # quit() 

            col_id = row["col:taxonID"]
            name = row["col:name"]
            transliteration = row["col:transliteration"]
            language = row["col:language"]
            preferred = row["col:preferred"]
            country = row["col:country"]
            area = row["col:area"]

            if not name:
                continue

            batch.append((
                col_id,
                name,
                transliteration,
                language,
                preferred,
                country,
                area
            ))

            if len(batch) >= BATCH_SIZE:
                conn.executemany(
                f"""
                    INSERT INTO {table_name}
                    (
                        col_id,
                        name,
                        transliteration,
                        language,
                        preferred,
                        country,
                        area
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?)
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
                    col_id,
                    name,
                    transliteration,
                    language,
                    preferred,
                    country,
                    area
                )
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, batch)

    conn.commit()

    # Create lookup index AFTER import
    conn.execute(
    f"""
        CREATE INDEX idx_{table_name}_col_id
        ON {table_name}(col_id)
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
    print(f'''HERBS >> REFERENCE >> col''')

    if 0:
        start = time.perf_counter()
        # table_name_usage_create()
        print(f'reference sqlite_name_usage() - execution time: ', time.perf_counter() - start)

    start = time.perf_counter()
    table_vernacular_name_create()
    print(f'reference sqlite_vernacular_name_create() - execution time: ', time.perf_counter() - start)

