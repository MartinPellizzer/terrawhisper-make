import json
import sqlite3
from collections import defaultdict

from lib import g
from lib import io
from lib import data

input_foldername = 'qualify'
output_foldername = 'derive'
input_folderpath = f'{g.VAULT_FOLDERPATH}/terrawhisper/data/{input_foldername}'
output_folderpath = f'{g.VAULT_FOLDERPATH}/terrawhisper/data/{output_foldername}'
db_filepath = f'{input_folderpath}/observations.db'
###

import masterize_utils

def synonym_summary_get(plant_canonical_name):
    conn = sqlite3.connect(db_filepath)
    cursor = conn.execute("""
        SELECT *
        FROM plants_synonyms
        WHERE plant_canonical_name = ?
    """, (plant_canonical_name,))
    rows = cursor.fetchall()
    conn.close()
    return rows

def names_common_summary_get(plant_name_scientific_canon):
    conn = sqlite3.connect(db_filepath)
    cursor = conn.execute("""
        SELECT *
        FROM plants_names_common
        WHERE plant_name_scientific_canon = ?
    """, (plant_name_scientific_canon,))
    rows = cursor.fetchall()
    conn.close()
    return rows

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

def name_summary_get(plant_canonical_name):
    conn = sqlite3.connect(db_filepath)
    cursor = conn.execute("""
        SELECT *
        FROM plants_names
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

def plant_part_summary_get(plant_canonical_name):
    conn = sqlite3.connect(db_filepath)
    cursor = conn.execute("""
        SELECT
            plant_part_canonical_name,
            COUNT(DISTINCT source_name) AS num_sources
        FROM plants_parts
        WHERE plant_canonical_name = ?
        GROUP BY plant_part_canonical_name
        ORDER BY num_sources DESC;
    """, (plant_canonical_name,))
    rows = cursor.fetchall()
    conn.close()
    return rows

def plant_part_summary_get_0000(plant_canonical_name):
    conn = sqlite3.connect(db_filepath)
    cursor = conn.execute("""
SELECT
    plant_canonical_name,
    plant_part_canonical_name,
    COUNT(*) AS num_sources,
    json_group_array(source_name) AS sources
FROM (
    SELECT DISTINCT
        plant_canonical_name,
        plant_part_canonical_name,
        source_name
    FROM plants_parts
    WHERE plant_canonical_name = ?
)
GROUP BY
    plant_canonical_name,
    plant_part_canonical_name
ORDER BY num_sources DESC;
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

def chemical_summary_get_0000(plant_canonical_name):
    conn = sqlite3.connect(db_filepath)
    cursor = conn.execute("""
        SELECT
            plant_name_scientific_canon,
            chemical_name_canon,
            COUNT(*) AS num_sources,
            json_group_array(source_name) AS sources
        FROM (
            SELECT DISTINCT
                plant_name_scientific_canon,
                chemical_name_canon,
                source_name
            FROM plants_chemicals
            WHERE plant_name_scientific_canon = ?
        )
        GROUP BY
            plant_name_scientific_canon,
            chemical_name_canon
        ORDER BY num_sources DESC;
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

def activity_summary_get_0000(plant_canonical_name):
    conn = sqlite3.connect(db_filepath)
    cursor = conn.execute("""
        SELECT
            plant_name_scientific_canon,
            activity_name_canon,
            COUNT(*) AS num_sources,
            json_group_array(source_name) AS sources
        FROM (
            SELECT DISTINCT
                plant_name_scientific_canon,
                activity_name_canon,
                source_name
            FROM plants_activities
            WHERE plant_name_scientific_canon = ?
        )
        GROUP BY
            plant_name_scientific_canon,
            activity_name_canon
        ORDER BY num_sources DESC;
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

def disease_summary_get_0000(plant_canonical_name):
    conn = sqlite3.connect(db_filepath)
    cursor = conn.execute("""
        SELECT
            plant_canonical_name,
            disease_canonical_name,
            COUNT(*) AS num_sources,
            json_group_array(source_name) AS sources
        FROM (
            SELECT DISTINCT
                plant_canonical_name,
                disease_canonical_name,
                source_name
            FROM plants_diseases
            WHERE plant_canonical_name = ?
        )
        GROUP BY
            plant_canonical_name,
            disease_canonical_name
        ORDER BY num_sources DESC;
    """, (plant_canonical_name,))
    rows = cursor.fetchall()
    conn.close()
    return rows

def preparation_summary_get(plant_canonical_name):
    conn = sqlite3.connect(db_filepath)
    cursor = conn.execute("""
        SELECT
            preparation_canonical_name,
            COUNT(DISTINCT source_name) AS num_sources
        FROM plants_preparations
        WHERE plant_canonical_name = ?
        GROUP BY preparation_canonical_name
        ORDER BY num_sources DESC;
    """, (plant_canonical_name,))
    rows = cursor.fetchall()
    conn.close()
    return rows

def preparation_summary_get_0000(plant_canonical_name):
    conn = sqlite3.connect(db_filepath)
    cursor = conn.execute("""
        SELECT
            plant_canonical_name,
            preparation_canonical_name,
            COUNT(*) AS num_sources,
            json_group_array(source_name) AS sources
        FROM (
            SELECT DISTINCT
                plant_canonical_name,
                preparation_canonical_name,
                source_name
            FROM plants_preparations
            WHERE plant_canonical_name = ?
        )
        GROUP BY
            plant_canonical_name,
            preparation_canonical_name
        ORDER BY num_sources DESC;
    """, (plant_canonical_name,))
    rows = cursor.fetchall()
    conn.close()
    return rows

def traits_gen():
    entity_foldername = 'traits'
    master_plants_rows = masterize_utils.masterize_plants_get_all()
    for i, master_plant_row in enumerate(master_plants_rows):
        print(f'{i}/{len(master_plants_rows)}')
        plant_name_scientific_canon = master_plant_row[1]
        ###
        conn = sqlite3.connect(db_filepath)
        conn.row_factory = sqlite3.Row
        cursor = conn.execute("""
            SELECT *
            FROM plants_traits
            WHERE plant_name_scientific_canon = ?
            ORDER BY trait_category;
        """, (plant_name_scientific_canon,))
        rows = cursor.fetchall()
        items = [dict(row) for row in rows]
        conn.close()
        ###
        output_items = []
        '''
        grouped_traits = defaultdict(list)
        for row in rows:
            category = row["trait_category"] or "General"
            grouped_traits[category].append({
                "trait_1": row["trait_1"],
                "trait_2": row["trait_2"],
                "value": row["trait_value"],
                "units": row["trait_units"]
            })
            output_item = dict(grouped_traits)
            # print(json.dumps(output_item, indent=4))
            # quit()
            output_items.append(output_item)
        '''
        traits_groups = []
        for item in items:
            found = False
            for trait_group in traits_groups:
                if trait_group['trait_category'] == item['trait_category']:
                    item_new = {
                        'trait_1': item['trait_1'],
                        'trait_2': item['trait_2'],
                        'trait_value': item['trait_value'],
                        'trait_units': item['trait_units'],
                    }
                    trait_group['traits'].append(item_new)
                    found = True
                    pass
                pass
            if not found:
                item_new = {
                    'trait_category': item['trait_category'],
                    'traits': [{
                        'trait_1': item['trait_1'],
                        'trait_2': item['trait_2'],
                        'trait_value': item['trait_value'],
                        'trait_units': item['trait_units'],
                    }],
                }
                traits_groups.append(item_new)
        output_items = traits_groups
        print(json.dumps(traits_groups, indent=4))
        # quit()
        ###
        output_filepath = f'{g.DATA_FOLDERPATH}/{output_foldername}/herbs/{entity_foldername}/{master_plant_row[1]}.json'
        io.folder_create_from_filepath(output_filepath)
        io.json_write(output_filepath, output_items)

################################################################################
# JSONS
################################################################################

def run():
    ### SYNONYMS
    if 0:
        entity_foldername = 'synonyms'
        master_plants_rows = masterize_utils.masterize_plants_get_all()
        for i, master_plant_row in enumerate(master_plants_rows):
            print(f'{i}/{len(master_plants_rows)}')
            summary_rows = synonym_summary_get(master_plant_row[1])
            output_items = []
            for row in summary_rows:
                output_item = {
                    'plant_canonical_name': master_plant_row[1], ### MANDATORY
                    'plant_synonym': row[2],
                    'source': row[3],
                }
                print(json.dumps(output_item, indent=4))
                output_items.append(output_item)
            output_filepath = f'{g.DATA_FOLDERPATH}/{output_foldername}/herbs/{entity_foldername}/{master_plant_row[1]}.json'
            io.folder_create_from_filepath(output_filepath)
            io.json_write(output_filepath, output_items)

    ### NAMES COMMON
    if 0:
        entity_foldername = 'names_common'
        master_plants_rows = masterize_utils.masterize_plants_get_all()
        common_names_labels_found_count = 0
        common_names_aliases_found_count = 0
        col_common_names_vernacular_found_count = 0
        for i, master_plant_row in enumerate(master_plants_rows):
            print(f'{i}/{len(master_plants_rows)}')
            plant_name_scientific_canon = master_plant_row[1]
            ### GET ALL NAMES COMMON
            conn = sqlite3.connect(db_filepath)
            conn.row_factory = sqlite3.Row
            cursor = conn.execute("""
                SELECT *
                FROM plants_names_common
                WHERE plant_name_scientific_canon = ?
            """, (plant_name_scientific_canon,))
            rows = cursor.fetchall()
            items = [dict(row) for row in rows]
            conn.close()

            ###
            plant_name_common_preferred = ''
            plant_name_common_en_labels = []
            plant_name_common_en_aliases = []
            plant_name_common_es = []
            plant_name_common_de = []
            plant_name_common_fr = []
            if items != []:
                for item in items:
                    if item['source_name'].lower() == 'wikidata':
                        if item['plant_name_common_raw'].lower() != item['plant_name_scientific_canon'].lower():
                            if item['plant_name_common_language'].lower() == 'en':
                                if item['plant_name_common_type'].lower() == 'label':
                                    if plant_name_common_preferred == '': plant_name_common_preferred = item['plant_name_common_raw']
                                    plant_name_common_en_labels.append(item['plant_name_common_raw'])
                                if item['plant_name_common_type'].lower() == 'alias':
                                    if plant_name_common_preferred == '': plant_name_common_preferred = item['plant_name_common_raw']
                                    common_names_aliases_found_count += 1
                            elif item['plant_name_common_language'].lower() == 'es':
                                plant_name_common_es.append(item['plant_name_common_raw'])
                            elif item['plant_name_common_language'].lower() == 'de':
                                plant_name_common_de.append(item['plant_name_common_raw'])
                            elif item['plant_name_common_language'].lower() == 'fr':
                                plant_name_common_fr.append(item['plant_name_common_raw'])

                    if item['source_name'].lower() == 'catalogue of life':
                        if item['plant_name_common_raw'].lower() != item['plant_name_scientific_canon'].lower():
                            if item['plant_name_common_language'].lower() == 'eng':
                                if plant_name_common_preferred == '': plant_name_common_preferred = item['plant_name_common_raw']
                                plant_name_common_en_aliases.append(item['plant_name_common_raw'])
                                ### DEBUG
                                col_common_names_vernacular_found_count += 1
                                # print(json.dumps(item, indent=4))
                                # quit()
                            if item['plant_name_common_language'].lower() == 'spa':
                                plant_name_common_es.append(item['plant_name_common_raw'])
                            if item['plant_name_common_language'].lower() == 'deu':
                                plant_name_common_de.append(item['plant_name_common_raw'])
                            if item['plant_name_common_language'].lower() == 'fra':
                                plant_name_common_fr.append(item['plant_name_common_raw'])

            ###
            output_items = {
                    'plant_name_common_preferred': plant_name_common_preferred,
                    'en_labels': plant_name_common_en_labels,
                    'en_aliases': plant_name_common_en_aliases,
                    'es_names': plant_name_common_es,
                    'de_names': plant_name_common_de,
                    'fr_names': plant_name_common_fr,
                    'all': [],
            }
            for item in items:
                # print(json.dumps(item, indent=4))
                # quit()
                output_item = {
                    'plant_name_scientific_canon': master_plant_row[1], ### MANDATORY FOR COMPILER
                    'plant_name_common': item['plant_name_common_raw'],
                    'source_name': item['source_name'],
                    'source_acronym': item['source_acronym'],
                }
                # print(json.dumps(output_item, indent=4))
                output_items['all'].append(output_item)
            output_filepath = f'{g.DATA_FOLDERPATH}/{output_foldername}/herbs/{entity_foldername}/{master_plant_row[1]}.json'
            io.folder_create_from_filepath(output_filepath)
            io.json_write(output_filepath, output_items)
            '''
            '''
        print(common_names_labels_found_count)
        print(common_names_aliases_found_count)
        print(col_common_names_vernacular_found_count)

    ### TAXONOMIES
    if 0:
        entity_foldername = 'taxonomies'
        master_plants_rows = masterize_utils.masterize_plants_get_all()
        for i, master_plant_row in enumerate(master_plants_rows):
            print(f'{i}/{len(master_plants_rows)}')
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
    if 0:
        entity_foldername = 'distribution'
        master_plants_rows = masterize_utils.masterize_plants_get_all()
        for i, master_plant_row in enumerate(master_plants_rows):
            print(f'{i}/{len(master_plants_rows)}')
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

    ### PLANTS PARTS
    if 0:
        entity_foldername = 'plants_parts'
        master_plants_rows = masterize_utils.masterize_plants_get_all()
        for i, master_plant_row in enumerate(master_plants_rows):
            print(f'{i}/{len(master_plants_rows)}')
            plant_name_scientific_canon = master_plant_row[1]
            ###
            conn = sqlite3.connect(db_filepath)
            cursor = conn.execute("""
                SELECT
                    plant_name_scientific_canon,
                    plant_part_name_canon,
                    COUNT(*) AS num_sources,
                    json_group_array(source_name) AS sources
                FROM (
                    SELECT DISTINCT
                        plant_name_scientific_canon,
                        plant_part_name_canon,
                        source_name
                    FROM plants_plants_parts
                    WHERE plant_name_scientific_canon = ?
                )
                GROUP BY
                    plant_name_scientific_canon,
                    plant_part_name_canon
                ORDER BY num_sources DESC;
            """, (plant_name_scientific_canon,))
            rows = cursor.fetchall()
            conn.close()
            ###
            output_items = []
            for row in rows:
                output_item = {
                    'plant_canonical_name': master_plant_row[1], ### MANDATORY
                    'plant_part_canonical_name': row[1],
                    'sources_num': row[2],
                    'sources': json.loads(row[3]),
                }
                print(json.dumps(output_item, indent=4))
                output_items.append(output_item)
            output_filepath = f'{g.DATA_FOLDERPATH}/{output_foldername}/herbs/{entity_foldername}/{master_plant_row[1]}.json'
            io.folder_create_from_filepath(output_filepath)
            io.json_write(output_filepath, output_items)

    ### CHEMICALS
    if 0:
        master_plants_rows = masterize_utils.masterize_plants_get_all()
        for i, master_plant_row in enumerate(master_plants_rows):
            print(f'{i}/{len(master_plants_rows)}')
            chemical_summary_rows = chemical_summary_get_0000(master_plant_row[1])
            output_items = []
            for row in chemical_summary_rows[:]:
                output_item = {
                    'plant_canonical_name': master_plant_row[1],
                    'chemical_canonical_name': row[1],
                    'sources_num': row[2],
                    'sources': json.loads(row[3]),
                }
                print(json.dumps(output_item, indent=4))
                output_items.append(output_item)
            output_filepath = f'{g.VAULT_FOLDERPATH}/terrawhisper/data/{output_foldername}/herbs/chemicals/{master_plant_row[1]}.json'
            io.folder_create_from_filepath(output_filepath)
            io.json_write(output_filepath, output_items)

    ### ACTIVITIES
    if 0:
        master_plants_rows = masterize_utils.masterize_plants_get_all()
        for i, master_plant_row in enumerate(master_plants_rows):
            print(f'{i}/{len(master_plants_rows)}')
            summary_activity_rows = activity_summary_get_0000(master_plant_row[1])
            output_items = []
            for row in summary_activity_rows:
                output_item = {
                    'plant_canonical_name': master_plant_row[1],
                    'activity_canonical_name': row[1],
                    'sources_num': row[2],
                    'sources': json.loads(row[3]),
                }
                print(json.dumps(output_item, indent=4))
                output_items.append(output_item)
            output_filepath = f'{g.VAULT_FOLDERPATH}/terrawhisper/data/{output_foldername}/herbs/activities/{master_plant_row[1]}.json'
            io.folder_create_from_filepath(output_filepath)
            io.json_write(output_filepath, output_items)

    ### DISEASES
    if 0:
        master_plants_rows = masterize_utils.masterize_plants_get_all()
        for i, master_plant_row in enumerate(master_plants_rows):
            print(f'{i}/{len(master_plants_rows)}')
            summary_disease_rows = disease_summary_get_0000(master_plant_row[1])
            output_items = []
            for row in summary_disease_rows:
                output_item = {
                    'plant_canonical_name': master_plant_row[1],
                    'disease_canonical_name': row[1],
                    'sources_num': row[2],
                    'sources': json.loads(row[3]),
                }
                print(json.dumps(output_item, indent=4))
                output_items.append(output_item)
            output_filepath = f'{g.DATA_FOLDERPATH}/{output_foldername}/herbs/diseases/{master_plant_row[1]}.json'
            io.folder_create_from_filepath(output_filepath)
            io.json_write(output_filepath, output_items)

    ### PREPARATIONS
    if 0:
        entity_foldername = 'preparations'
        master_plants_rows = masterize_utils.masterize_plants_get_all()
        for i, master_plant_row in enumerate(master_plants_rows):
            print(f'{i}/{len(master_plants_rows)}')
            summary_rows = preparation_summary_get_0000(master_plant_row[1])
            output_items = []
            for row in summary_rows:
                output_item = {
                    'plant_canonical_name': master_plant_row[1], ### MANDATORY
                    'preparation_canonical_name': row[1],
                    'sources_num': row[2],
                    'sources': json.loads(row[3]),
                }
                output_items.append(output_item)
            output_filepath = f'{g.DATA_FOLDERPATH}/{output_foldername}/herbs/{entity_foldername}/{master_plant_row[1]}.json'
            io.folder_create_from_filepath(output_filepath)
            io.json_write(output_filepath, output_items)

    ### TRAITS
    if 0:
        traits_gen()
