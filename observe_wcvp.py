import os
import csv
import time
import json
import shutil
import sqlite3

from lib import g
from lib import io
from lib import llm

def observations_table_plants_distribution_add():
    source_foldername = 'wcvp'
    input_foldername = 'resolve'
    output_foldername = 'observe'
    input_folderpath = f'{g.DATA_FOLDERPATH}/{input_foldername}/{source_foldername}/distribution'
    output_folderpath = f'{g.DATA_FOLDERPATH}/{output_foldername}'

    db_observations_filepath = f'{output_folderpath}/observations.db'
    db_wcvp_filepath = f'{g.DATA_FOLDERPATH}/reference/wcvp/wcvp.db'
    conn_observations = sqlite3.connect(db_observations_filepath)
    conn_wcvp = sqlite3.connect(db_wcvp_filepath)

    BATCH_SIZE = 100000
    processed = 0
    start = time.time()
    conn_observations.execute("BEGIN")
    with open(
        f"{input_folderpath}/wcvp_distribution.csv",
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
            plant_name_id = row["plant_name_id"]
            continent = row["continent"]
            region = row["region"]
            area = row["area"]

            cursor = conn_wcvp.execute("""
                SELECT taxon_name
                FROM wcvp
                WHERE plant_name_id = ?
            """, (plant_name_id,))
            row = cursor.fetchone()
            taxon_name = row[0]

            if not taxon_name:
                continue

            batch.append((
                taxon_name,
                continent,
                region,
                area,
                'WCVP',
            ))

            if len(batch) >= BATCH_SIZE:
                conn_observations.executemany("""
                    INSERT INTO plants_distribution
                    (
                        plant_canonical_name,
                        continent,
                        region,
                        area,
                        source
                    )
                    VALUES (?, ?, ?, ?, ?)
                """, batch)
                processed += len(batch)
                if processed % 1000000 == 0:
                    elapsed = time.time() - start
                    print(f"{processed:,} inserted ({elapsed:.1f}s)")
                batch.clear()

        if batch:
            conn_observations.executemany("""
                INSERT INTO plants_distribution
                (
                        plant_canonical_name,
                        continent,
                        region,
                        area,
                        source
                )
                VALUES (?, ?, ?, ?, ?)
            """, batch)

    conn_observations.commit()

    rows = conn_observations.execute("SELECT * FROM plants_distribution")
    for row in list(rows)[:10]:
        print(row)

    conn_observations.close()
    conn_wcvp.close()


def run():
    print('OBSERVE >> wcvp')

    start = time.perf_counter()
    observations_table_plants_distribution_add()
    print(f'observations table_plants_distribution_add() - execution time: ', time.perf_counter() - start)
