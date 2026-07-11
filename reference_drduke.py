import os
import time

import sqlite3
import csv
import re
import unicodedata
import time

from lib import g
from lib import io

import normalize_utils

def drduke_table_activities_create():
    source_foldername = 'drduke'
    input_foldername = 'fetch'
    output_foldername = 'reference'
    input_filepath = f'{g.VAULT_FOLDERPATH}/terrawhisper/data/{input_foldername}/{source_foldername}/database/Duke-Source-CSV/ACTIVITIES.csv'
    output_folderpath = f'{g.VAULT_FOLDERPATH}/terrawhisper/data/{output_foldername}/{source_foldername}'
    io.folders_recursive_gen(output_folderpath)

    conn = sqlite3.connect(f"{output_folderpath}/drduke.db")
    table_name = 'activities'

    conn.executescript(f"""
        PRAGMA journal_mode = OFF;
        PRAGMA synchronous = OFF;
        PRAGMA temp_store = MEMORY;
        PRAGMA cache_size = -500000;
        DROP TABLE IF EXISTS {table_name};
        CREATE TABLE {table_name} (
            activity_name TEXT NOT NULL,
            activity_name_normalized TEXT NOT NULL
        );
    """)

    conn.commit()


    BATCH_SIZE = 100000
    processed = 0
    start = time.time()
    conn.execute("BEGIN")
    with open(
        f"{input_filepath}",
        "r",
        encoding="utf8",
        errors="ignore",
        newline="",
    ) as f:
        reader = csv.DictReader(f, delimiter=",")
        batch = []
        for row in reader:
            activity_name = row["ACTIVITY"]
            if not activity_name:
                continue
            batch.append((
                activity_name,
                normalize_utils.normalize_activity_name(activity_name)
            ))
            if len(batch) >= BATCH_SIZE:
                conn.executemany(f"""
                    INSERT INTO {table_name}
                    (activity_name, activity_name_normalized)
                    VALUES (?, ?)
                """, batch)
                processed += len(batch)
                if processed % 1000000 == 0:
                    elapsed = time.time() - start
                    print(f"{processed:,} inserted ({elapsed:.1f}s)")
                batch.clear()
        if batch:
            conn.executemany(f"""
                INSERT INTO {table_name}
                (activity_name, activity_name_normalized)
                VALUES (?, ?)
            """, batch)
    conn.commit()

    # Create lookup index AFTER import
    conn.execute(f"""
        CREATE INDEX idx_{table_name}_activity_name_normalized
        ON {table_name}(activity_name_normalized)
    """)

    conn.commit()

    ### TEST PRINT
    conn = sqlite3.connect(f"{output_folderpath}/drduke.db")
    cursor = conn.execute(f"""
        SELECT *
        FROM {table_name}
        LIMIT 100
    """)
    for row in cursor:
        print(row)

    print("Done")

def run():
    print(f'REFERENCE >> drduke')

    start = time.perf_counter()
    drduke_table_activities_create()
    print(f'drduke table_activities_create() - execution time: ', time.perf_counter() - start)
