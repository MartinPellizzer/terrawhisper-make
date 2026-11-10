parts_items = [
    {
        'preferred': 'leaf',
        'synonyms': ['leaf', 'leaves'],
    },
    {
        'preferred': 'root',
        'synonyms': ['root', 'roots', 'hairy roots', 'dried roots', 'radix'],
    },
    {
        'preferred': 'aerial parts',
        'synonyms': ['aerial part', 'aerial parts'],
    },
    {
        'preferred': 'whole plant',
        'synonyms': ['whole plant'],
    },
    {
        'preferred': 'fruit',
        'synonyms': ['fruit', 'fruits', 'berry', 'berries'],
    },
    {
        'preferred': 'stem',
        'synonyms': ['stem', 'stems'],
    },
    {
        'preferred': 'flower',
        'synonyms': ['flower', 'flowers'],
    },
    {
        'preferred': 'bark',
        'synonyms': ['bark', 'barks', 'cortex', 'stem bark', 'root bark'],
    },
    {
        'preferred': 'rhizome',
        'synonyms': ['rhizome', 'rhizomes', 'rhizoma'],
    },
    {
        'preferred': 'seed',
        'synonyms': ['seed', 'seeds'],
    },
    {
        'preferred': 'twig',
        'synonyms': ['twig', 'twigs'],
    },
    {
        'preferred': 'tuber',
        'synonyms': ['tuber', 'tubers'],
    },
]

preparations_items = [
    {
        'preferred': 'extract',
        'synonyms': ['extract', 'extracts'],
    },
    {
        'preferred': 'oil',
        'synonyms': ['oil', 'oils'],
    },
    {
        'preferred': 'essential oil',
        'synonyms': ['essential oil', 'essential oils'],
    },
    {
        'preferred': 'decoction',
        'synonyms': ['decoction', 'decoctions'],
    },
    {
        'preferred': 'infusion',
        'synonyms': ['infusion', 'infusions'],
    },
    {
        'preferred': 'powder',
        'synonyms': ['powder', 'powders'],
    },
    {
        'preferred': 'capsule',
        'synonyms': ['capsule', 'capsules'],
    },
    {
        'preferred': 'tea',
        'synonyms': ['tea', 'teas'],
    },
    {
        'preferred': 'juice',
        'synonyms': ['juice', 'juices'],
    },
]

import sys
import time
import json

import sqlite3
import csv

from lib import g
from lib import io

HUB_FOLDERPATH = f'''{g.DATA_FOLDERPATH}/herbs'''

def reference__parts__table_create():
    output_folderpath = f'{HUB_FOLDERPATH}/reference/manual'
    io.folders_recursive_gen(output_folderpath)
    conn = sqlite3.connect(f"{output_folderpath}/manual.db")
    table_name = 'ref__parts'
    conn.executescript(
    f"""
        PRAGMA journal_mode = OFF;
        PRAGMA synchronous = OFF;
        PRAGMA temp_store = MEMORY;
        PRAGMA cache_size = -500000;
        DROP TABLE IF EXISTS {table_name};
        CREATE TABLE {table_name} (
            ref_part_id TEXT NOT NULL,
            ref_part_name TEXT NOT NULL,
            ref_part_name_normalize TEXT NOT NULL
        );
    """)
    conn.commit()
    ###
    csv.field_size_limit(sys.maxsize)
    BATCH_SIZE = 100000
    processed = 0
    start = time.time()
    conn.execute("BEGIN")
    batch = []
    for i, item in enumerate(parts_items):
        # print(json.dumps(item, indent=4))
        # quit() 
        ref_part_id = i
        ref_part_name = item['preferred']
        ref_part_name_normalize = ref_part_name.lower().strip()
        batch.append((
            ref_part_id,
            ref_part_name,
            ref_part_name_normalize,
        ))
        if len(batch) >= BATCH_SIZE:
            conn.executemany(
            f"""
                INSERT INTO {table_name}
                (
                    ref_part_id,
                    ref_part_name,
                    ref_part_name_normalize
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
                    ref_part_id,
                    ref_part_name,
                    ref_part_name_normalize
            )
            VALUES (?, ?, ?)
        """, batch)
    conn.commit()
    # Create lookup index AFTER import
    conn.execute(
    f"""
        CREATE INDEX idx_{table_name}_ref_part_id
        ON {table_name}(ref_part_id)
    """)
    conn.execute(
    f"""
        CREATE INDEX idx_{table_name}_ref_part_name
        ON {table_name}(ref_part_name)
    """)
    conn.execute(
    f"""
        CREATE INDEX idx_{table_name}_ref_part_name_normalize
        ON {table_name}(ref_part_name_normalize)
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

def reference__preparations__table_create():
    output_folderpath = f'{HUB_FOLDERPATH}/reference/manual'
    io.folders_recursive_gen(output_folderpath)
    conn = sqlite3.connect(f"{output_folderpath}/manual.db")
    table_name = 'ref__preparations'
    conn.executescript(
    f"""
        PRAGMA journal_mode = OFF;
        PRAGMA synchronous = OFF;
        PRAGMA temp_store = MEMORY;
        PRAGMA cache_size = -500000;
        DROP TABLE IF EXISTS {table_name};
        CREATE TABLE {table_name} (
            ref_preparation_id TEXT NOT NULL,
            ref_preparation_name TEXT NOT NULL,
            ref_preparation_name_normalize TEXT NOT NULL
        );
    """)
    conn.commit()
    ###
    csv.field_size_limit(sys.maxsize)
    BATCH_SIZE = 100000
    processed = 0
    start = time.time()
    conn.execute("BEGIN")
    batch = []
    for i, item in enumerate(preparations_items):
        # print(json.dumps(item, indent=4))
        # quit() 
        ref_preparation_id = i
        ref_preparation_name = item['preferred']
        ref_preparation_name_normalize = ref_preparation_name.lower().strip()
        batch.append((
            ref_preparation_id,
            ref_preparation_name,
            ref_preparation_name_normalize,
        ))
        if len(batch) >= BATCH_SIZE:
            conn.executemany(
            f"""
                INSERT INTO {table_name}
                (
                    ref_preparation_id,
                    ref_preparation_name,
                    ref_preparation_name_normalize
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
                    ref_preparation_id,
                    ref_preparation_name,
                    ref_preparation_name_normalize
            )
            VALUES (?, ?, ?)
        """, batch)
    conn.commit()
    # Create lookup index AFTER import
    conn.execute(
    f"""
        CREATE INDEX idx_{table_name}_ref_preparation_id
        ON {table_name}(ref_preparation_id)
    """)
    conn.execute(
    f"""
        CREATE INDEX idx_{table_name}_ref_preparation_name
        ON {table_name}(ref_preparation_name)
    """)
    conn.execute(
    f"""
        CREATE INDEX idx_{table_name}_ref_preparation_name_normalize
        ON {table_name}(ref_preparation_name_normalize)
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
    print(f'''HERBS >> REFERENCE >> manual''')

    reference__parts__table_create()
    reference__preparations__table_create()

