import json
import sqlite3

from lib import g
from lib import io
from lib import data

input_foldername = 'qualify'
output_foldername = 'derive'
input_folderpath = f'{g.VAULT_FOLDERPATH}/terrawhisper/data/{input_foldername}'
output_folderpath = f'{g.VAULT_FOLDERPATH}/terrawhisper/data/{output_foldername}'
db_filepath = f'{input_folderpath}/observations.db'
###

def taxonomy_summary_get(plant_canonical_name):
    conn = sqlite3.connect(db_filepath)
    cursor = conn.execute("""
        SELECT *
        FROM plants_taxonomies
        WHERE plant_canonical_name = ?
    """, (plant_canonical_name,))
    rows = cursor.fetchall()
    conn.close()
    return rows

def distribution_summary_get(plant_canonical_name):
    conn = sqlite3.connect(db_filepath)
    cursor = conn.execute("""
        SELECT *
        FROM plants_distribution
        WHERE plant_canonical_name = ?
    """, (plant_canonical_name,))
    rows = cursor.fetchall()
    conn.close()
    return rows

def chemical_summary_get(plant_canonical_name):
    conn = sqlite3.connect(db_filepath)
    cursor = conn.execute("""
        SELECT
            chemical_canonical_name,
            COUNT(DISTINCT plant_part) AS num_plant_parts,
            COUNT(DISTINCT source_name) AS num_sources,
            MIN(concentration) AS min_concentration,
            MAX(concentration) AS max_concentration
        FROM plants_chemicals
        WHERE plant_canonical_name = ?
        GROUP BY chemical_canonical_name
        ORDER BY chemical_canonical_name;
    """, (plant_canonical_name,))
    rows = cursor.fetchall()
    conn.close()
    return rows

def summary_activity_get(plant_canonical_name):
    conn = sqlite3.connect(db_filepath)
    cursor = conn.execute("""
        SELECT
            activity_canonical_name,
            COUNT(DISTINCT source_name) AS num_sources
        FROM plants_activities
        WHERE plant_canonical_name = ?
        GROUP BY activity_canonical_name
        ORDER BY activity_canonical_name;
    """, (plant_canonical_name,))
    rows = cursor.fetchall()
    conn.close()
    return rows

def summary_disease_get(plant_canonical_name):
    conn = sqlite3.connect(db_filepath)
    cursor = conn.execute("""
        SELECT
            disease_canonical_name,
            COUNT(DISTINCT source_name) AS num_sources
        FROM plants_diseases
        WHERE plant_canonical_name = ?
        GROUP BY disease_canonical_name
        ORDER BY disease_canonical_name;
    """, (plant_canonical_name,))
    rows = cursor.fetchall()
    conn.close()
    return rows

################################################################################
# JSONS
################################################################################

### TAXONOMIES
if 0:
    entity_foldername = 'taxonomies'
    master_plants_rows = data.sqlite__plants_get()
    for master_plant_row in master_plants_rows:
        summary_rows = taxonomy_summary_get(master_plant_row[1])
        output_items = []
        for row in summary_rows:
            output_item = {
                'plant_canonical_name': master_plant_row[1], ### MANDATORY
                'kingdom': row[2],
                'phylum': row[3],
                'class': row[4],
                'subclass': row[5],
                'order': row[6],
                'family': row[7],
                'genus': row[8],
            }
            print(json.dumps(output_item, indent=4))
            output_items.append(output_item)
        output_filepath = f'{g.DATA_FOLDERPATH}/{output_foldername}/herbs/{entity_foldername}/{master_plant_row[1]}.json'
        io.folder_create_from_filepath(output_filepath)
        io.json_write(output_filepath, output_items)

### DISTRIBUTION
if 1:
    entity_foldername = 'distribution'
    master_plants_rows = data.sqlite__plants_get()
    for master_plant_row in master_plants_rows:
        summary_rows = distribution_summary_get(master_plant_row[1])
        output_items = []
        for row in summary_rows:
            output_item = {
                'plant_canonical_name': master_plant_row[1], ### MANDATORY
                'continent': row[2],
                'region': row[3],
                'area': row[4],
            }
            print(json.dumps(output_item, indent=4))
            # quit()
            output_items.append(output_item)
        output_filepath = f'{g.DATA_FOLDERPATH}/{output_foldername}/herbs/{entity_foldername}/{master_plant_row[1]}.json'
        io.folder_create_from_filepath(output_filepath)
        io.json_write(output_filepath, output_items)

### CHEMICALS
if 0:
    master_plants_rows = data.sqlite__plants_get()
    for master_plant_row in master_plants_rows:
        chemical_summary_rows = chemical_summary_get(master_plant_row[1])
        output_items = []
        for row in chemical_summary_rows:
            output_item = {
                'plant_canonical_name': master_plant_row[1],
                'chemical_canonical_name': row[0],
                'plant_part': row[1],
                'num_sources': row[2],
                'min_concentration': row[3],
                'max_concentration': row[3],
            }
            print(json.dumps(output_item, indent=4))
            output_items.append(output_item)
        output_filepath = f'{g.VAULT_FOLDERPATH}/terrawhisper/data/{output_foldername}/herbs/chemicals/{master_plant_row[1]}.json'
        io.folder_create_from_filepath(output_filepath)
        io.json_write(output_filepath, output_items)

### ACTIVITIES
if 0:
    master_plants_rows = data.sqlite__plants_get()
    for master_plant_row in master_plants_rows:
        summary_activity_rows = summary_activity_get(master_plant_row[1])
        output_items = []
        for row in summary_activity_rows:
            output_item = {
                'plant_canonical_name': master_plant_row[1],
                'activity_canonical_name': row[0],
                'num_sources': row[1],
            }
            print(json.dumps(output_item, indent=4))
            output_items.append(output_item)
        output_filepath = f'{g.VAULT_FOLDERPATH}/terrawhisper/data/{output_foldername}/herbs/activities/{master_plant_row[1]}.json'
        io.folder_create_from_filepath(output_filepath)
        io.json_write(output_filepath, output_items)

### DISEASES
if 0:
    master_plants_rows = data.sqlite__plants_get()
    for master_plant_row in master_plants_rows:
        summary_disease_rows = summary_disease_get(master_plant_row[1])
        output_items = []
        for row in summary_disease_rows:
            output_item = {
                'plant_canonical_name': master_plant_row[1],
                'disease_canonical_name': row[0],
                'num_sources': row[1],
            }
            print(json.dumps(output_item, indent=4))
            output_items.append(output_item)
        output_filepath = f'{g.VAULT_FOLDERPATH}/terrawhisper/data/{output_foldername}/herbs/diseases/{master_plant_row[1]}.json'
        io.folder_create_from_filepath(output_filepath)
        io.json_write(output_filepath, output_items)

