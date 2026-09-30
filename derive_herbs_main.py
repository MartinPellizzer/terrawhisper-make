import json
import sqlite3
from collections import defaultdict

from lib import g
from lib import io
from lib import data

import masterize_utils

HUB_FOLDERPATH = f'''{g.DATA_FOLDERPATH}/herbs'''

input_foldername = 'observe'
output_foldername = 'derive'
input_folderpath = f'{HUB_FOLDERPATH}/{input_foldername}'
output_folderpath = f'{HUB_FOLDERPATH}/{output_foldername}'
db_filepath = f'{input_folderpath}/observations.db'

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
        master_item = master_plant_row
        print(f'DERIVE TRAITS {i}/{len(master_plants_rows)}')
        plant_name_scientific_reference = master_plant_row['plant_name_scientific_reference']
        ###
        conn = sqlite3.connect(db_filepath)
        conn.row_factory = sqlite3.Row
        cursor = conn.execute("""
            SELECT *
            FROM plants_traits
            WHERE plant_name_scientific_reference = ?
            ORDER BY trait_category;
        """, (plant_name_scientific_reference,))
        rows = cursor.fetchall()
        items = [dict(row) for row in rows]
        conn.close()
        ###
        output_items = []
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
        # print(json.dumps(traits_groups, indent=4))
        # quit()
        ###
        output_filepath = f'''{HUB_FOLDERPATH}/{output_foldername}/traits/{master_item['plant_name_scientific_reference']}.json'''
        io.folder_create_from_filepath(output_filepath)
        io.json_write(output_filepath, output_items)
    print(json.dumps(output_items[0], indent=4))

def names_common_gen():
    entity_foldername = 'names_common'
    master_plants_rows = masterize_utils.masterize_plants_get_all()
    common_names_labels_found_count = 0
    common_names_aliases_found_count = 0
    col_common_names_vernacular_found_count = 0
    for i, master_plant_row in enumerate(master_plants_rows):
        print(f'DERIVE NAMES COMMON {i}/{len(master_plants_rows)}')
        plant_name_scientific_reference_normalize = master_plant_row['plant_name_scientific_reference_normalize']
        ### GET ALL NAMES COMMON
        conn = sqlite3.connect(db_filepath)
        conn.row_factory = sqlite3.Row
        cursor = conn.execute("""
            SELECT *
            FROM plants_names_common
            WHERE plant_name_scientific_reference_normalize = ?
        """, (plant_name_scientific_reference_normalize,))
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
                    if item['plant_name_common'].lower() != item['plant_name_scientific_reference_normalize'].lower():
                        if item['plant_name_common_language'].lower() == 'en':
                            if item['plant_name_common_type'].lower() == 'label':
                                if plant_name_common_preferred == '': plant_name_common_preferred = item['plant_name_common']
                                plant_name_common_en_labels.append(item['plant_name_common'])
                            if item['plant_name_common_type'].lower() == 'alias':
                                if plant_name_common_preferred == '': plant_name_common_preferred = item['plant_name_common']
                                common_names_aliases_found_count += 1
                        elif item['plant_name_common_language'].lower() == 'es':
                            plant_name_common_es.append(item['plant_name_common'])
                        elif item['plant_name_common_language'].lower() == 'de':
                            plant_name_common_de.append(item['plant_name_common'])
                        elif item['plant_name_common_language'].lower() == 'fr':
                            plant_name_common_fr.append(item['plant_name_common'])
                if item['source_name'].lower() == 'catalogue of life':
                    if item['plant_name_common'].lower() != item['plant_name_scientific_reference_normalize'].lower():
                        if item['plant_name_common_language'].lower() == 'eng':
                            if plant_name_common_preferred == '': plant_name_common_preferred = item['plant_name_common']
                            plant_name_common_en_aliases.append(item['plant_name_common'])
                            ### DEBUG
                            col_common_names_vernacular_found_count += 1
                            # print(json.dumps(item, indent=4))
                            # quit()
                        if item['plant_name_common_language'].lower() == 'spa':
                            plant_name_common_es.append(item['plant_name_common'])
                        if item['plant_name_common_language'].lower() == 'deu':
                            plant_name_common_de.append(item['plant_name_common'])
                        if item['plant_name_common_language'].lower() == 'fra':
                            plant_name_common_fr.append(item['plant_name_common'])
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
                'plant_name_scientific_reference_normalize': master_plant_row['plant_name_scientific_reference_normalize'], ### MANDATORY FOR COMPILER
                'plant_name_common': item['plant_name_common'],
                'source_name': item['source_name'],
                'source_acronym': item['source_acronym'],
            }
            # print(json.dumps(output_item, indent=4))
            output_items['all'].append(output_item)
        output_filepath = f'''{HUB_FOLDERPATH}/{output_foldername}/{entity_foldername}/{master_plant_row['plant_name_scientific_reference']}.json'''
        # print(output_filepath)
        # quit()
        io.folder_create_from_filepath(output_filepath)
        io.json_write(output_filepath, output_items)
        '''
        '''
    print(common_names_labels_found_count)
    print(common_names_aliases_found_count)
    print(col_common_names_vernacular_found_count)

def activities_gen():
    master_items = masterize_utils.masterize_plants_get_all()
    # print(json.dumps(items, indent=4))
    # quit()
    for i, master_item in enumerate(master_items):
        print(f'DERIVE ACTIVITIES {i}/{len(master_items)}')
        ###
        # if master_item['plant_name_scientific_reference'] != 'cakile maritima': continue
        conn = sqlite3.connect(db_filepath)
        conn.row_factory = sqlite3.Row
        # cursor = conn.execute(f"SELECT * FROM plants_activities")
        # rows = cursor.fetchall()
        # items = [dict(row) for row in rows]
        # for item in items[:1]:
            # print(json.dumps(item, indent=4))
        cursor = conn.execute("""
            SELECT
                plant_name_scientific_reference,
                activity_name_reference,
                COUNT(*) AS sources_num,
                json_group_array(
                    json_object(
                        'reference_name', reference_name,
                        'reference_id', reference_id
                    )
                ) AS sources
            FROM (
                SELECT DISTINCT
                    plant_name_scientific_reference,
                    activity_name_reference,
                    reference_name,
                    reference_id
                FROM plants_activities
                WHERE plant_name_scientific_reference = ?
            )
            GROUP BY
                plant_name_scientific_reference,
                activity_name_reference
            ORDER BY sources_num DESC;
        """, (master_item['plant_name_scientific_reference'],))
        items = cursor.fetchall()
        items = [dict(item) for item in items]
        conn.close()
        ###
        output_items = []
        for item in items:
            output_item = {
                'plant_name_scientific_reference': master_item['plant_name_scientific_reference'],
                'activity_name_reference': item['activity_name_reference'],
                'sources_num': item['sources_num'],
                'sources': json.loads(item['sources']),
            }
            # print(json.dumps(output_item, indent=4))
            output_items.append(output_item)
        output_filepath = f'''{HUB_FOLDERPATH}/{output_foldername}/activities/{master_item['plant_name_scientific_reference']}.json'''
        io.folder_create_from_filepath(output_filepath)
        io.json_write(output_filepath, output_items)
        # print(json.dumps(output_items, indent=4))
        # quit()

def chemicals_gen():
    master_plants_rows = masterize_utils.masterize_plants_get_all()
    # print(json.dumps(master_plants_rows[0], indent=4))
    # quit()
    last = []
    for i, master_plant_row in enumerate(master_plants_rows):
        master_item = master_plant_row
        print(f'DERIVE CHEMICALS {i}/{len(master_plants_rows)}')
        conn = sqlite3.connect(db_filepath)
        conn.row_factory = sqlite3.Row
        # cursor = conn.execute(f"SELECT * FROM plants_chemicals")
        # rows = cursor.fetchall()
        # items = [dict(row) for row in rows]
        # for item in items[:1]:
            # print(json.dumps(item, indent=4))
        # quit()
        cursor = conn.execute('''
            SELECT
                plant_name_scientific_reference,
                chemical_name_reference,
                COUNT(*) AS sources_num,
                json_group_array(
                    json_object(
                        'reference_name', reference_name,
                        'reference_id', reference_id
                    )
                ) AS sources
            FROM (
                SELECT DISTINCT
                    plant_name_scientific_reference,
                    chemical_name_reference,
                    reference_name,
                    reference_id
                FROM plants_chemicals
                WHERE plant_name_scientific_reference = ?
            )
            GROUP BY
                plant_name_scientific_reference,
                chemical_name_reference
            ORDER BY sources_num DESC;
        ''', (master_item['plant_name_scientific_reference'],))
        rows = cursor.fetchall()
        conn.close()
        ###
        output_items = []
        for row in rows[:]:
            output_item = {
                'plant_name_scientific_reference': master_plant_row['plant_name_scientific_reference'],
                'chemical_name_reference': row['chemical_name_reference'],
                'sources_num': row['sources_num'],
                'sources': json.loads(row['sources']),
            }
            # print(json.dumps(output_item, indent=4))
            output_items.append(output_item)
        output_filepath = f'''{HUB_FOLDERPATH}/{output_foldername}/chemicals/{master_plant_row['plant_name_scientific_reference']}.json'''
        io.folder_create_from_filepath(output_filepath)
        io.json_write(output_filepath, output_items)
        if output_items != []:
            last = output_items
    print(json.dumps(last, indent=4))
    # quit()

def conditions_gen():
    master_plants_rows = masterize_utils.masterize_plants_get_all()
    last = []
    for i, master_plant_row in enumerate(master_plants_rows):
        master_item = master_plant_row
        print(f'DERIVE CONDITIONS {i}/{len(master_plants_rows)}')
        ###
        conn = sqlite3.connect(db_filepath)
        conn.row_factory = sqlite3.Row
        cursor = conn.execute("""
            SELECT
                plant_name_scientific_reference,
                condition_name_reference,
                COUNT(*) AS sources_num,
                json_group_array(
                    json_object(
                        'reference_name', reference_name,
                        'reference_id', reference_id
                    )
                ) AS sources
            FROM (
                SELECT DISTINCT
                    plant_name_scientific_reference,
                    condition_name_reference,
                    reference_name,
                    reference_id
                FROM plants_conditions
                WHERE plant_name_scientific_reference = ?
            )
            GROUP BY
                plant_name_scientific_reference,
                condition_name_reference
            ORDER BY sources_num DESC;
        """, (master_item['plant_name_scientific_reference'],))
        rows = cursor.fetchall()
        conn.close()
        ###
        output_items = []
        for row in rows:
            output_item = {
                'plant_name_scientific_reference': master_plant_row['plant_name_scientific_reference'],
                'condition_name_reference': row['condition_name_reference'],
                'sources_num': row['sources_num'],
                'sources': json.loads(row['sources']),
            }
            output_items.append(output_item)
        output_filepath = f'''{HUB_FOLDERPATH}/{output_foldername}/conditions/{master_plant_row['plant_name_scientific_reference']}.json'''
        io.folder_create_from_filepath(output_filepath)
        io.json_write(output_filepath, output_items)
        if output_items != []:
            last = output_items
    print(json.dumps(output_item, indent=4))
    # quit()

def plants_parts_gen():
    master_plants_rows = masterize_utils.masterize_plants_get_all()
    last = []
    for i, master_plant_row in enumerate(master_plants_rows):
        master_item = master_plant_row
        print(f'DERIVE PLANTS PARTS {i}/{len(master_plants_rows)}')
        ###
        conn = sqlite3.connect(db_filepath)
        conn.row_factory = sqlite3.Row
        cursor = conn.execute("""
            SELECT
                plant_name_scientific_reference,
                plant_part_name_reference,
                COUNT(*) AS sources_num,
                json_group_array(
                    json_object(
                        'reference_name', reference_name,
                        'reference_id', reference_id
                    )
                ) AS sources
            FROM (
                SELECT DISTINCT
                    plant_name_scientific_reference,
                    plant_part_name_reference,
                    reference_name,
                    reference_id
                FROM plants_plants_parts
                WHERE plant_name_scientific_reference = ?
            )
            GROUP BY
                plant_name_scientific_reference,
                plant_part_name_reference
            ORDER BY sources_num DESC;
        """, (master_item['plant_name_scientific_reference'],))
        rows = cursor.fetchall()
        conn.close()
        ###
        output_items = []
        for row in rows:
            output_item = {
                'plant_name_scientific_reference': master_plant_row['plant_name_scientific_reference'],
                'plant_part_name_reference': row['plant_part_name_reference'],
                'sources_num': row[2],
                'sources': json.loads(row[3]),
            }
            # print(json.dumps(output_item, indent=4))
            # quit()
            output_items.append(output_item)
        output_filepath = f'''{HUB_FOLDERPATH}/{output_foldername}/plants_parts/{master_plant_row['plant_name_scientific_reference']}.json'''
        io.folder_create_from_filepath(output_filepath)
        io.json_write(output_filepath, output_items)
        if output_items != []:
            last = output_items
    print(json.dumps(output_item, indent=4))

def preparations_gen():
    entity_foldername = 'preparations'
    master_plants_rows = masterize_utils.masterize_plants_get_all()
    for i, master_plant_row in enumerate(master_plants_rows):
        master_item = master_plant_row
        print(f'DERIVE PREPARATIONS {i}/{len(master_plants_rows)}')
        ###
        conn = sqlite3.connect(db_filepath)
        conn.row_factory = sqlite3.Row
        cursor = conn.execute("""
            SELECT
                plant_name_scientific_reference,
                preparation_name_reference,
                COUNT(*) AS sources_num,
                json_group_array(source_name) AS sources
            FROM (
                SELECT DISTINCT
                    plant_name_scientific_reference,
                    preparation_name_reference,
                    source_name
                FROM plants_preparations
                WHERE plant_name_scientific_reference = ?
            )
            GROUP BY
                plant_name_scientific_reference,
                preparation_name_reference
            ORDER BY sources_num DESC;
        """, (master_item['plant_name_scientific_reference'],))
        rows = cursor.fetchall()
        conn.close()
        ###
        output_items = []
        for row in rows:
            output_item = {
                'plant_name_scientific_reference': master_plant_row['plant_name_scientific_reference'],
                'preparation_name_reference': row['preparation_name_reference'],
                'sources_num': row[2],
                'sources': json.loads(row[3]),
            }
            output_items.append(output_item)
        output_filepath = f'''{HUB_FOLDERPATH}/{output_foldername}/preparations/{master_plant_row['plant_name_scientific_reference']}.json'''
        io.folder_create_from_filepath(output_filepath)
        io.json_write(output_filepath, output_items)
    print(json.dumps(output_item, indent=4))

def distributions_gen():
    entity_foldername = 'distributions'
    master_plants_rows = masterize_utils.masterize_plants_get_all()
    for i, master_plant_row in enumerate(master_plants_rows):
        master_item = master_plant_row
        print(f'DERIVE DISTRIBUTIONS {i}/{len(master_plants_rows)}')
        ###
        conn = sqlite3.connect(db_filepath)
        conn.row_factory = sqlite3.Row
        cursor = conn.execute("""
            SELECT *
            FROM plants_distributions
            WHERE plant_name_scientific_reference = ?
        """, (master_item['plant_name_scientific_reference'],))
        rows = cursor.fetchall()
        items = [dict(row) for row in rows]
        conn.close()
        ###
        output_items = []
        for item in items:
            output_item = {
                'plant_name_scientific_reference': master_plant_row['plant_name_scientific_reference'],
                'locality_continent': item['locality_continent'],
                'locality_region': item['locality_region'],
                'locality_area': item['locality_area'],
            }
            output_items.append(output_item)
        output_filepath = f'''{HUB_FOLDERPATH}/{output_foldername}/distributions/{master_plant_row['plant_name_scientific_reference']}.json'''
        io.folder_create_from_filepath(output_filepath)
        io.json_write(output_filepath, output_items)
    # print(json.dumps(output_item, indent=4))

def synonyms_gen():
    entity_foldername = 'synonyms'
    master_plants_rows = masterize_utils.masterize_plants_get_all()
    for i, master_plant_row in enumerate(master_plants_rows):
        master_item = master_plant_row
        print(f'DERIVE PLANTS - SYNONYMS {i}/{len(master_plants_rows)}')
        ###
        conn = sqlite3.connect(db_filepath)
        conn.row_factory = sqlite3.Row
        cursor = conn.execute("""
            SELECT *
            FROM plants_synonyms
            WHERE plant_name_scientific_reference = ?
        """, (master_item['plant_name_scientific_reference'],))
        rows = cursor.fetchall()
        items = [dict(row) for row in rows]
        conn.close()
        ###
        output_items = []
        for item in items:
            output_item = {
                'plant_name_scientific_reference': master_plant_row['plant_name_scientific_reference'],
                'plant_synonym_reference': item['plant_synonym_reference'],
            }
            output_items.append(output_item)
        output_filepath = f'''{HUB_FOLDERPATH}/{output_foldername}/synonyms/{master_plant_row['plant_name_scientific_reference']}.json'''
        io.folder_create_from_filepath(output_filepath)
        io.json_write(output_filepath, output_items)
    print(json.dumps(output_item, indent=4))

def taxonomies_gen():
    entity_foldername = 'taxonomies'
    master_plants_rows = masterize_utils.masterize_plants_get_all()
    for i, master_plant_row in enumerate(master_plants_rows):
        master_item = master_plant_row
        print(f'DERIVE PLANTS TAXONOMIES {i}/{len(master_plants_rows)}')
        ###
        conn = sqlite3.connect(db_filepath)
        conn.row_factory = sqlite3.Row
        cursor = conn.execute("""
            SELECT *
            FROM plants_taxonomies
            WHERE plant_name_scientific_reference = ?
        """, (master_item['plant_name_scientific_reference'],))
        rows = cursor.fetchall()
        items = [dict(row) for row in rows]
        conn.close()
        ###
        output_items = []
        for item in items:
            output_item = {
                'plant_name_scientific_reference': master_plant_row['plant_name_scientific_reference'],
                'kingdom': item['taxon_kingdom'],
                'phylum': item['taxon_phylum'],
                'class': item['taxon_class'],
                'subclass': item['taxon_subclass'],
                'order': item['taxon_order'],
                'family': item['taxon_family'],
                'genus': item['taxon_genus'],
            }
            output_items.append(output_item)
        output_filepath = f'''{HUB_FOLDERPATH}/{output_foldername}/taxonomies/{master_plant_row['plant_name_scientific_reference']}.json'''
        io.folder_create_from_filepath(output_filepath)
        io.json_write(output_filepath, output_items)
    print(json.dumps(output_item, indent=4))

def run():
    plants_parts_gen()
    conditions_gen()
    chemicals_gen()
    activities_gen()

    taxonomies_gen()
    synonyms_gen()
    traits_gen()
    distributions_gen()
    names_common_gen()
    preparations_gen()

