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

def mesh_table_diseases_create():
    import sqlite3
    import time
    import xml.etree.ElementTree as ET
    import gzip

    source_foldername = 'mesh'
    input_foldername = 'fetch'
    output_foldername = 'reference'
    input_filepath = f'{g.VAULT_FOLDERPATH}/terrawhisper/data/{input_foldername}/{source_foldername}/database/desc2026.gz'
    output_folderpath = f'{g.VAULT_FOLDERPATH}/terrawhisper/data/{output_foldername}/{source_foldername}'
    io.folders_recursive_gen(output_folderpath)

    conn = sqlite3.connect(f"{output_folderpath}/mesh.db")
    table_name = 'diseases'
    conn.executescript(f"""
        PRAGMA journal_mode = OFF;
        PRAGMA synchronous = OFF;
        PRAGMA temp_store = MEMORY;
        PRAGMA cache_size = -500000;
        DROP TABLE IF EXISTS {table_name};
        CREATE TABLE {table_name} (
            mesh_id TEXT NOT NULL,
            disease_name TEXT NOT NULL,
            disease_name_normalized TEXT NOT NULL
        );
    """)
    conn.commit()


    BATCH_SIZE = 100000
    processed = 0
    start = time.time()
    conn.execute("BEGIN")
    with gzip.open(
        input_filepath,
        "rt",
        encoding="utf8",
        errors="ignore"
    ) as f:
        context = ET.iterparse(
            f,
            events=("end",)
        )
        batch = []
        for event, elem in context:
            if elem.tag != "DescriptorRecord":
                continue
            mesh_id = elem.findtext("DescriptorUI")
            # main descriptor name
            names = []
            main_name = elem.findtext(
                "./DescriptorName/String"
            )
            if main_name:
                names.append(main_name)
            # synonyms
            for term in elem.findall(
                ".//Term/String"
            ):
                if term.text:
                    names.append(term.text)
            for name in names:
                batch.append((
                    mesh_id,
                    name,
                    normalize_utils.normalize_disease_name(name)
                ))
            if len(batch) >= BATCH_SIZE:
                conn.executemany(f"""
                    INSERT INTO {table_name}
                    (
                        mesh_id,
                        disease_name,
                        disease_name_normalized
                    )
                    VALUES (?, ?, ?)
                """, batch)
                processed += len(batch)
                if processed % 1000000 == 0:
                    elapsed = time.time() - start
                    print(
                        f"{processed:,} inserted ({elapsed:.1f}s)"
                    )
                batch.clear()
            # VERY IMPORTANT for huge XML files
            elem.clear()
    if batch:
        conn.executemany(f"""
            INSERT INTO {table_name}
            (
                mesh_id,
                disease_name,
                disease_name_normalized
            )
            VALUES (?, ?, ?)
        """, batch)
    conn.commit()

    # Create lookup index AFTER import
    conn.execute(f"""
        CREATE INDEX idx_{table_name}_disease_name_normalized
        ON {table_name}(disease_name_normalized)
    """)
    conn.commit()

    ### TEST PRINT
    conn = sqlite3.connect(f"{output_folderpath}/mesh.db")
    cursor = conn.execute(f"""
        SELECT *
        FROM {table_name}
        LIMIT 100
    """)
    for row in cursor:
        print(row)

    print("Done")

def run():
    print(f'REFERENCE >> mesh')

    start = time.perf_counter()
    mesh_table_diseases_create()
    print(f'mesh table_diseases_create() - execution time: ', time.perf_counter() - start)

