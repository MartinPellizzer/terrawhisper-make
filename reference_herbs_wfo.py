import csv
import json
import time
import sqlite3

from lib import g
from lib import io

HUB_FOLDERPATH = f'''{g.DATA_FOLDERPATH}/herbs'''

def reference__wfo__classification():
    table_name = f'ref__wfo__classification' 
    input_folderpath = f'{HUB_FOLDERPATH}/fetch/wfo/_DwC_backbone_R'
    output_folderpath = f'{HUB_FOLDERPATH}/reference/wfo'
    io.folders_recursive_gen(output_folderpath)
    conn = sqlite3.connect(f"{output_folderpath}/wfo.db")
    conn.executescript(f"""
    PRAGMA journal_mode = OFF;
    PRAGMA synchronous = OFF;
    PRAGMA temp_store = MEMORY;
    PRAGMA cache_size = -500000;
    DROP TABLE IF EXISTS {table_name};
    CREATE TABLE {table_name} (
        taxon_id TEXT PRIMARY KEY,
        scientific_name_id TEXT,
        local_id TEXT,
        scientific_name TEXT,
        taxon_rank TEXT,
        parent_name_usage_id TEXT,
        scientific_name_authorship TEXT,
        family TEXT,
        subfamily TEXT,
        tribe TEXT,
        subtribe TEXT,
        genus TEXT,
        subgenus TEXT,
        specific_epithet TEXT,
        infraspecific_epithet TEXT,
        verbatim_taxon_rank TEXT,
        nomenclatural_status TEXT,
        name_published_in TEXT,
        taxonomic_status TEXT,
        accepted_name_usage_id TEXT,
        original_name_usage_id TEXT,
        name_according_to_id TEXT,
        taxon_remarks TEXT,
        created TEXT,
        modified TEXT,
        refs TEXT,
        source TEXT,
        major_group TEXT,
        tpl_id TEXT
    );
    """)
    conn.commit()
    BATCH_SIZE = 100000
    processed = 0
    start = time.time()
    conn.execute("BEGIN")
    with open(
        f"{input_folderpath}/classification.csv",
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
            taxon_id = row['taxonID']
            scientific_name_id = row['scientificNameID']
            local_id = row['localID']
            scientific_name = row['scientificName']
            taxon_rank = row['taxonRank']
            parent_name_usage_id = row['parentNameUsageID']
            scientific_name_authorship = row['scientificNameAuthorship']
            family = row['family']
            subfamily = row['subfamily']
            tribe = row['tribe']
            subtribe = row['subtribe']
            genus = row['genus']
            subgenus = row['subgenus']
            specific_epithet = row['specificEpithet']
            infraspecific_epithet = row['infraspecificEpithet']
            verbatim_taxon_rank = row['verbatimTaxonRank']
            nomenclatural_status = row['nomenclaturalStatus']
            name_published_in = row['namePublishedIn']
            taxonomic_status = row['taxonomicStatus']
            accepted_name_usage_id = row['acceptedNameUsageID']
            original_name_usage_id = row['originalNameUsageID']
            name_according_to_id = row['nameAccordingToID']
            taxon_remarks = row['taxonRemarks']
            created = row['created']
            modified = row['modified']
            refs = row['references']
            source = row['source']
            major_group = row['majorGroup']
            tpl_id = row['tplID']
            ###
            batch.append((
                taxon_id,
                scientific_name_id,
                local_id,
                scientific_name,
                taxon_rank,
                parent_name_usage_id,
                scientific_name_authorship,
                family,
                subfamily,
                tribe,
                subtribe,
                genus,
                subgenus,
                specific_epithet,
                infraspecific_epithet,
                verbatim_taxon_rank,
                nomenclatural_status,
                name_published_in,
                taxonomic_status,
                accepted_name_usage_id,
                original_name_usage_id,
                name_according_to_id,
                taxon_remarks,
                created,
                modified,
                refs,
                source,
                major_group,
                tpl_id,
            ))
            if len(batch) >= BATCH_SIZE:
                conn.executemany(f"""
                    INSERT INTO {table_name}
                    (
                        taxon_id,
                        scientific_name_id,
                        local_id,
                        scientific_name,
                        taxon_rank,
                        parent_name_usage_id,
                        scientific_name_authorship,
                        family,
                        subfamily,
                        tribe,
                        subtribe,
                        genus,
                        subgenus,
                        specific_epithet,
                        infraspecific_epithet,
                        verbatim_taxon_rank,
                        nomenclatural_status,
                        name_published_in,
                        taxonomic_status,
                        accepted_name_usage_id,
                        original_name_usage_id,
                        name_according_to_id,
                        taxon_remarks,
                        created,
                        modified,
                        refs,
                        source,
                        major_group,
                        tpl_id
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, batch)
                processed += len(batch)
                if processed % 1000000 == 0:
                    elapsed = time.time() - start
                    print(f"{processed:,} inserted ({elapsed:.1f}s)")
                batch.clear()
        if batch:
            conn.executemany(f"""
                INSERT INTO {table_name}
                (
                    taxon_id,
                    scientific_name_id,
                    local_id,
                    scientific_name,
                    taxon_rank,
                    parent_name_usage_id,
                    scientific_name_authorship,
                    family,
                    subfamily,
                    tribe,
                    subtribe,
                    genus,
                    subgenus,
                    specific_epithet,
                    infraspecific_epithet,
                    verbatim_taxon_rank,
                    nomenclatural_status,
                    name_published_in,
                    taxonomic_status,
                    accepted_name_usage_id,
                    original_name_usage_id,
                    name_according_to_id,
                    taxon_remarks,
                    created,
                    modified,
                    refs,
                    source,
                    major_group,
                    tpl_id
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, batch)
    conn.commit()
    # Create lookup index AFTER import
    conn.execute(f"""
        CREATE INDEX idx_{table_name}_taxon_id
        ON {table_name}(taxon_id)
    """)
    conn.commit()
    cursor = conn.execute(f"""
        SELECT *
        FROM {table_name}
        LIMIT 10
    """)
    for row in cursor:
        print(row)
    conn.close()
    print("Done")

def run():
    if 1:
        reference__wfo__classification()
    else:
        input_folderpath = f'{HUB_FOLDERPATH}/fetch/wfo/_DwC_backbone_R'
        with open(
            f"{input_folderpath}/classification.csv",
            "r",
            encoding="utf8",
            errors="ignore",
            newline="",
        ) as f:
            reader = csv.DictReader(f, delimiter="\t")
            batch = []
            for row in reader:
                # print(row)
                print(json.dumps(row, indent=4))
                quit() 

