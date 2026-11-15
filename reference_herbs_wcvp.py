import os
import time
import json

import sqlite3
import csv
import re
import unicodedata
import time
from tabulate import tabulate

from lib import g
from lib import io

HUB_FOLDERPATH = f'''{g.DATA_FOLDERPATH}/herbs'''

wcvp_table_name = f'plants_names'
wcvp_table_name_distribution = f'plants_distributions'

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

def wcvp_table_plants_distribution_create():
    input_folderpath = f'{HUB_FOLDERPATH}/fetch/wcvp/wcvp'
    output_folderpath = f'{HUB_FOLDERPATH}/reference/wcvp'
    io.folders_recursive_gen(output_folderpath)
    conn = sqlite3.connect(f"{output_folderpath}/wcvp.db")
    conn.executescript(f"""
    PRAGMA journal_mode = OFF;
    PRAGMA synchronous = OFF;
    PRAGMA temp_store = MEMORY;
    PRAGMA cache_size = -500000;
    DROP TABLE IF EXISTS {wcvp_table_name_distribution};
    CREATE TABLE {wcvp_table_name_distribution} (
        plant_locality_id TEXT NOT NULL,
        plant_name_id TEXT NOT NULL,
        continent_code_l1 TEXT,
        continent TEXT,
        region_code_l2 TEXT,
        region TEXT,
        area_code_l3 TEXT,
        area TEXT,
        introduced TEXT,
        extinct TEXT,
        location_doubtful TEXT
    );
    """)
    conn.commit()
    BATCH_SIZE = 100000
    processed = 0
    start = time.time()
    conn.execute("BEGIN")
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
            plant_locality_id = row['plant_locality_id']
            plant_name_id = row['plant_name_id']
            continent_code_l1 = row['continent_code_l1']
            continent = row['continent']
            region_code_l2 = row['region_code_l2']
            region = row['region']
            area_code_l3 = row['area_code_l3']
            area = row['area']
            introduced = row['introduced']
            extinct = row['extinct']
            location_doubtful = row['location_doubtful']
            batch.append((
                plant_locality_id,
                plant_name_id,
                continent_code_l1,
                continent,
                region_code_l2,
                region,
                area_code_l3,
                area,
                introduced,
                extinct,
                location_doubtful
            ))
            if len(batch) >= BATCH_SIZE:
                conn.executemany(f"""
                    INSERT INTO {wcvp_table_name_distribution}
                    (
                        plant_locality_id,
                        plant_name_id,
                        continent_code_l1,
                        continent,
                        region_code_l2,
                        region,
                        area_code_l3,
                        area,
                        introduced,
                        extinct,
                        location_doubtful
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, batch)
                processed += len(batch)
                if processed % 1000000 == 0:
                    elapsed = time.time() - start
                    print(f"{processed:,} inserted ({elapsed:.1f}s)")
                batch.clear()
        if batch:
            conn.executemany(f"""
                INSERT INTO {wcvp_table_name_distribution}
                (
                    plant_locality_id,
                    plant_name_id,
                    continent_code_l1,
                    continent,
                    region_code_l2,
                    region,
                    area_code_l3,
                    area,
                    introduced,
                    extinct,
                    location_doubtful
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, batch)
    conn.commit()
    # Create lookup index AFTER import
    conn.execute(f"""
        CREATE INDEX idx_{wcvp_table_name_distribution}_plant_locality_id
        ON {wcvp_table_name_distribution}(plant_locality_id)
    """)
    conn.execute(f"""
        CREATE INDEX idx_{wcvp_table_name_distribution}_plant_name_id
        ON {wcvp_table_name_distribution}(plant_name_id)
    """)
    conn.commit()
    cursor = conn.execute(f"""
        SELECT *
        FROM {wcvp_table_name_distribution}
        LIMIT 10
    """)
    rows = cursor.fetchall()
    # for row in cursor:
        # print(row)
    conn.close()
    print("Done")
    from tabulate import tabulate
    print(tabulate(rows, 
        headers=[
            'PLANT_LOCALITY_ID',
            'PLANT_NAME_ID',
            'CONTINENT_CODE_L1',
            'CONTINENT',
            'REGION_CODE_L2',
            'REGION',
            'AREA_CODE_L3',
            'AREA',
            'INTRODUCED',
            'EXTINCT',
            'LOCATION_DOUBTFUL',
        ], 
        tablefmt="plain")
    )

def wcvp_table_plants_distributions_peek():
    output_folderpath = f'{HUB_FOLDERPATH}/reference/wcvp'
    conn = sqlite3.connect(f"{output_folderpath}/wcvp.db")
    cursor = conn.execute(f"""
        SELECT *
        FROM {wcvp_table_name_distribution}
        WHERE plant_name_id == "146697"
        LIMIT 10
    """)
    rows = cursor.fetchall()
    conn.close()
    print(tabulate(rows, 
        headers=[
            'PLANT_LOCALITY_ID',
            'PLANT_NAME_ID',
            'CONTINENT_CODE_L1',
            'CONTINENT',
            'REGION_CODE_L2',
            'REGION',
            'AREA_CODE_L3',
            'AREA',
            'INTRODUCED',
            'EXTINCT',
            'LOCATION_DOUBTFUL',
        ], 
        tablefmt="plain")
    )

def wcvp_table_plants_names_peek():
    output_folderpath = f'{HUB_FOLDERPATH}/reference/wcvp'
    io.folders_recursive_gen(output_folderpath)
    conn = sqlite3.connect(f"{output_folderpath}/wcvp.db")
    cursor = conn.execute(f"""
        SELECT *
        FROM {wcvp_table_name}
        WHERE taxon_name_normalized == "panax ginseng"
        LIMIT 10
    """)
    rows = cursor.fetchall()
    conn.close()
    print(tabulate(rows, 
        headers=[
            'PLANT_NAME_ID',
            'ACCEPTED_PLANT_NAME_ID',
            'TAXON_STATUS',
            'TAXON_NAME',
            'TAXON_NAME_NORMALIZED',
            'POWO_ID',
            'IPNI_ID',
        ], 
        tablefmt="plain")
    )

def wcvp_plants_names_preview_csv():
    input_folderpath = f'{HUB_FOLDERPATH}/fetch/wcvp/wcvp'
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
            print(json.dumps(row, indent=4))
            quit() 

def wcvp_plants_distributions_preview_csv():
    input_folderpath = f'{HUB_FOLDERPATH}/fetch/wcvp/wcvp'
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
            print(json.dumps(row, indent=4))
            quit() 

def ref__wcvp__names__table_create():
    table_name = 'ref__wcvp__names'
    input_folderpath = f'{HUB_FOLDERPATH}/fetch/wcvp/wcvp'
    output_folderpath = f'{HUB_FOLDERPATH}/reference/wcvp'
    io.folders_recursive_gen(output_folderpath)
    conn = sqlite3.connect(f"{output_folderpath}/wcvp.db")
    conn.executescript(f"""
        PRAGMA journal_mode = OFF;
        PRAGMA synchronous = OFF;
        PRAGMA temp_store = MEMORY;
        PRAGMA cache_size = -500000;
        DROP TABLE IF EXISTS {table_name};
        CREATE TABLE {table_name} (
            plant_name_id TEXT,
            ipni_id TEXT,
            taxon_rank TEXT,
            taxon_status TEXT,
            family TEXT,
            genus_hybrid TEXT,
            genus TEXT,
            species_hybrid TEXT,
            species TEXT,
            infraspecific_rank TEXT,
            infraspecies TEXT,
            parenthetical_author TEXT,
            primary_author TEXT,
            publication_author TEXT,
            place_of_publication TEXT,
            volume_and_page TEXT,
            first_published TEXT,
            nomenclatural_remarks TEXT,
            geographic_area TEXT,
            lifeform_description TEXT,
            climate_description TEXT,
            taxon_name TEXT,
            taxon_authors TEXT,
            accepted_plant_name_id TEXT,
            basionym_plant_name_id TEXT,
            replaced_synonym_author TEXT,
            homotypic_synonym TEXT,
            parent_plant_name_id TEXT,
            powo_id TEXT,
            hybrid_formula TEXT,
            reviewed TEXT,
            taxon_name_normalized TEXT
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
            plant_name_id = row['plant_name_id']
            ipni_id = row['ipni_id']
            taxon_rank = row['taxon_rank']
            taxon_status = row['taxon_status']
            family = row['family']
            genus_hybrid = row['genus_hybrid']
            genus = row['genus']
            species_hybrid = row['species_hybrid']
            species = row['species']
            infraspecific_rank = row['infraspecific_rank']
            infraspecies = row['infraspecies']
            parenthetical_author = row['parenthetical_author']
            primary_author = row['primary_author']
            publication_author = row['publication_author']
            place_of_publication = row['place_of_publication']
            volume_and_page = row['volume_and_page']
            first_published = row['first_published']
            nomenclatural_remarks = row['nomenclatural_remarks']
            geographic_area = row['geographic_area']
            lifeform_description = row['lifeform_description']
            climate_description = row['climate_description']
            taxon_name = row['taxon_name']
            taxon_authors = row['taxon_authors']
            accepted_plant_name_id = row['accepted_plant_name_id']
            basionym_plant_name_id = row['basionym_plant_name_id']
            replaced_synonym_author = row['replaced_synonym_author']
            homotypic_synonym = row['homotypic_synonym']
            parent_plant_name_id = row['parent_plant_name_id']
            powo_id = row['powo_id']
            hybrid_formula = row['hybrid_formula']
            reviewed = row['reviewed']
            taxon_name_normalized = normalize_plant_name(taxon_name)
            ###
            batch.append((
                plant_name_id,
                ipni_id,
                taxon_rank,
                taxon_status,
                family,
                genus_hybrid,
                genus,
                species_hybrid,
                species,
                infraspecific_rank,
                infraspecies,
                parenthetical_author,
                primary_author,
                publication_author,
                place_of_publication,
                volume_and_page,
                first_published,
                nomenclatural_remarks,
                geographic_area,
                lifeform_description,
                climate_description,
                taxon_name,
                taxon_authors,
                accepted_plant_name_id,
                basionym_plant_name_id,
                replaced_synonym_author,
                homotypic_synonym,
                parent_plant_name_id,
                powo_id,
                hybrid_formula,
                reviewed,
                taxon_name_normalized,
            ))
            if len(batch) >= BATCH_SIZE:
                conn.executemany(f"""
                    INSERT INTO {table_name}
                    (
                        plant_name_id,
                        ipni_id,
                        taxon_rank,
                        taxon_status,
                        family,
                        genus_hybrid,
                        genus,
                        species_hybrid,
                        species,
                        infraspecific_rank,
                        infraspecies,
                        parenthetical_author,
                        primary_author,
                        publication_author,
                        place_of_publication,
                        volume_and_page,
                        first_published,
                        nomenclatural_remarks,
                        geographic_area,
                        lifeform_description,
                        climate_description,
                        taxon_name,
                        taxon_authors,
                        accepted_plant_name_id,
                        basionym_plant_name_id,
                        replaced_synonym_author,
                        homotypic_synonym,
                        parent_plant_name_id,
                        powo_id,
                        hybrid_formula,
                        reviewed,
                        taxon_name_normalized
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
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
                        plant_name_id,
                        ipni_id,
                        taxon_rank,
                        taxon_status,
                        family,
                        genus_hybrid,
                        genus,
                        species_hybrid,
                        species,
                        infraspecific_rank,
                        infraspecies,
                        parenthetical_author,
                        primary_author,
                        publication_author,
                        place_of_publication,
                        volume_and_page,
                        first_published,
                        nomenclatural_remarks,
                        geographic_area,
                        lifeform_description,
                        climate_description,
                        taxon_name,
                        taxon_authors,
                        accepted_plant_name_id,
                        basionym_plant_name_id,
                        replaced_synonym_author,
                        homotypic_synonym,
                        parent_plant_name_id,
                        powo_id,
                        hybrid_formula,
                        reviewed,
                        taxon_name_normalized
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, batch)
    conn.commit()
    # Create lookup index AFTER import
    conn.execute(f"""
        CREATE INDEX idx_{table_name}_plant_name_id
        ON {table_name}(plant_name_id)
    """)
    conn.execute(f"""
        CREATE INDEX idx_{table_name}_accepted_plant_name_id
        ON {table_name}(accepted_plant_name_id)
    """)
    conn.execute(f"""
        CREATE INDEX idx_{table_name}_taxon_name_normalized
        ON {table_name}(taxon_name_normalized)
    """)
    conn.execute(f"""
        CREATE INDEX idx_{table_name}_powo_id
        ON {table_name}(powo_id)
    """)
    conn.execute(f"""
        CREATE INDEX idx_{table_name}_ipni_id
        ON {table_name}(ipni_id)
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

def ref__wcvp__names__table_peek():
    table_name = 'ref__wcvp__names'
    output_folderpath = f'{HUB_FOLDERPATH}/reference/wcvp'
    io.folders_recursive_gen(output_folderpath)
    conn = sqlite3.connect(f"{output_folderpath}/wcvp.db")
    cursor = conn.execute(f"""
        SELECT *
        FROM {table_name}
        LIMIT 10
    """)
    rows = cursor.fetchall()
    conn.close()
    print(tabulate(rows, 
        headers=[
            'PLANT_NAME_ID',
            'IPNI_ID',
            'TAXON_RANK',
            'TAXON_STATUS',
            'FAMILY',
            'GENUS_HYBRID',
            'GENUS',
            'SPECIES_HYBRID',
            'SPECIES',
            'INFRASPECIFIC_RANK',
            'INFRASPECIES',
            'PARENTHETICAL_AUTHOR',
            'PRIMARY_AUTHOR',
            'PUBLICATION_AUTHOR',
            'PLACE_OF_PUBLICATION',
            'VOLUME_AND_PAGE',
            'FIRST_PUBLISHED',
            'NOMENCLATURAL_REMARKS',
            'GEOGRAPHIC_AREA',
            'LIFEFORM_DESCRIPTION',
            'CLIMATE_DESCRIPTION',
            'TAXON_NAME',
            'TAXON_AUTHORS',
            'ACCEPTED_PLANT_NAME_ID',
            'BASIONYM_PLANT_NAME_ID',
            'REPLACED_SYNONYM_AUTHOR',
            'HOMOTYPIC_SYNONYM',
            'PARENT_PLANT_NAME_ID',
            'POWO_ID',
            'HYBRID_FORMULA',
            'REVIEWED',
            'TAXON_NAME_NORMALIZED',
        ], 
        tablefmt="plain")
    )
    conn = sqlite3.connect(f"{output_folderpath}/wcvp.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.execute(f"""
        SELECT *
        FROM {table_name}
        LIMIT 10
    """)
    rows = cursor.fetchall()
    items = [dict(row) for row in rows]
    for item in items:
        print(json.dumps(item, indent=4))
    conn.close()

def run():
    print(f'REFERENCE >> wcvp')

    # wcvp_plants_names_preview_csv()
    # wcvp_plants_distributions_preview_csv()

    # wcvp_table_plants_names_create()
    # wcvp_table_plants_distribution_create()

    # wcvp_table_plants_names_peek()
    # wcvp_table_plants_distributions_peek()

    # ref__wcvp__names__table_create()
    ref__wcvp__names__table_peek()

    quit()
