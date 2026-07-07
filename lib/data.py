import os
import json
import sqlite3

from lib import g
from lib import io
from lib import polish

def is_herb_in_list(herb_tmp, herbs):
    found = False
    for herb in herbs:
        herb_a_name_scientific = herb['herb_name_scientific']
        herb_b_name_scientific = herb_tmp['herb_name_scientific']
        herb_a_name_scientific = herb_a_name_scientific.lower().strip().replace(' ', '-')
        herb_b_name_scientific = herb_b_name_scientific.lower().strip().replace(' ', '-')
        if  herb_a_name_scientific == herb_b_name_scientific:
            found = True
            break
    return found

def herbs_primary_get():
    herbs = []
    ###
    herbs_filepaths = [
        f'{g.database_folderpath}/csv/herbs-book-0001.csv',
        f'{g.database_folderpath}/csv/herbs-legacy.csv',
    ]
    for herbs_filepath in herbs_filepaths:
        herbs_tmp = io.csv_to_dict(herbs_filepath)
        for herb_tmp in herbs_tmp:
            herb_tmp_name_scientific = herb_tmp['herb_name_scientific'].lower().strip()
            herb_tmp_name_scientific = herb_tmp_name_scientific.replace('×', 'x')
            herb_tmp['herb_name_scientific'] = herb_tmp_name_scientific
            herb_tmp_slug = polish.sluggify(herb_tmp_name_scientific)
            found = is_herb_in_list(herb_tmp, herbs)
            if not found: herbs.append(herb_tmp)
    ###
    herbs = sorted(herbs, key=lambda x: x['herb_name_scientific'], reverse=False)
    for herb in herbs:
        print(herb)
    print(len(herbs))
    # quit()
    return herbs

def herbs_primary_medicinal_get():
    herbs = herbs_primary_get()
    herbs_medicinal = []
    for herb in herbs:
        print(herb)
        ssot_herb_filepath = f'''{g.database_folderpath}/ssot/herbs/herbs-primary/{herb['herb_slug']}.json'''
        if herb_medicine_or_poison_get(ssot_herb_filepath) == 'medicine':
            herbs_medicinal.append(herb)
    herbs_medicinal = sorted(herbs_medicinal, key=lambda x: x['herb_name_scientific'], reverse=False)
    # print(len(herbs_medicinal))
    return herbs_medicinal

def herbs_primary_medicinal_get_old():
    herbs = herbs_primary_get()
    herbs_medicinal = []
    for herb in herbs:
        print(herb)
        entities_herbs_folderpath = f''
        entity_herb_filepath = f'''{g.database_folderpath}/entities/herbs/{herb['herb_slug']}.json'''
        if herb_medicine_or_poison_get(entity_herb_filepath) == 'medicine':
            herbs_medicinal.append(herb)
    herbs_medicinal = sorted(herbs_medicinal, key=lambda x: x['herb_name_scientific'], reverse=False)
    # print(len(herbs_medicinal))
    return herbs_medicinal

def herbs_by_ailments():
    output_herb_list = []
    ailment_list = io.csv_to_dict(f'{g.database_folderpath}/csv/ailments.csv')
    preparation_list = io.csv_to_dict(f'{g.database_folderpath}/csv/preparations.csv')
    for ailment_i, ailment in enumerate(ailment_list):
        ailment_slug = ailment['ailment_slug']
        ailment_name = ailment['ailment_name']
        organ_slug = ailment['organ_slug']
        system_slug = ailment['system_slug']
        print(f'AILMENT: {ailment_i}/{len(ailment_list)} - {ailment_name}')
        for preparation_i, preparation in enumerate(preparation_list):
            preparation_slug = preparation['preparation_slug']
            preparation_name_singular = preparation['preparation_name_singular']
            preparation_name_plural = preparation['preparation_name_plural']
            print(f'PREPARATION: {preparation_slug}')
            url_relative = f'ailments/{ailment_slug}/{preparation_slug}'
            json_article_filepath = f'{g.database_folderpath}/json/{url_relative}.json'
            json_article = io.json_read(json_article_filepath)
            json_article_preparation_list = json_article['preparations']
            for json_article_preparation in json_article_preparation_list[:10]:
                json_article_herb_name_scientific = json_article_preparation['herb_name_scientific']
                print(json_article_preparation)
                if json_article_herb_name_scientific not in output_herb_list:
                    output_herb_list.append(json_article_herb_name_scientific)

def herb_medicine_or_poison_get(entity_herb_filepath):
    entity_herb = io.json_read(entity_herb_filepath)
    herb_name_scientific = entity_herb['herb_name_scientific']
    herb_medicine_or_poison = entity_herb['medicine_or_poison']
    medicine_or_poison = ''
    medicine_score = 0
    poison_score = 0
    inert_score = 0
    for obj in herb_medicine_or_poison:
        if 'answer' in obj:
            answer = obj['answer']
            total_score = obj['total_score']
            if answer == 'medicine':
                medicine_score = total_score
            elif answer == 'poison':
                poison_score = total_score
            elif answer == 'inert':
                inert_score = total_score
            
    if medicine_score > poison_score and medicine_score > inert_score:
        medicine_or_poison = 'medicine'
    elif poison_score > medicine_score and poison_score > inert_score:
        medicine_or_poison = 'poison'
    else:
        medicine_or_poison = 'inert'
    return medicine_or_poison

def herbs_popular_get(preparation_slug, herbs_num):
    herbs = []
    ailments = io.csv_to_dict(f'{g.database_folderpath}/csv/ailments.csv')
    preparations = io.csv_to_dict(f'{g.database_folderpath}/csv/preparations.csv')
    for ailment_i, ailment in enumerate(ailments):
        ailment_slug = ailment['ailment_slug']
        ailment_name = ailment['ailment_name']
        print(f'AILMENT: {ailment_i}/{len(ailments)} - {ailment_name}')
        for preparation_i, preparation in enumerate(preparations):
            _preparation_slug = preparation['preparation_slug']
            preparation_name_singular = preparation['preparation_name_singular']
            preparation_name_plural = preparation['preparation_name_plural']
            print(f'PREPARATION: {preparation_slug}')
            if preparation_slug != _preparation_slug: continue
            url_relative = f'ailments/{ailment_slug}/{preparation_slug}'
            json_article_filepath = f'''{g.database_folderpath}/json/{url_relative}.json'''
            json_article = io.json_read(json_article_filepath)
            json_article_preparations = json_article['preparations']
            for json_article_preparation in json_article_preparations:
                herb_name_scientific = json_article_preparation['herb_name_scientific']
                herb_name_scientific = herb_name_scientific.replace('mentha piperita', 'mentha x piperita')
                found = False
                for herb in herbs:
                    if herb['herb_name_scientific'] == herb_name_scientific:
                        herb['mentions'] += 1
                        found = True
                        break
                if not found:
                    herbs.append({
                        'herb_name_scientific': herb_name_scientific,
                        'mentions': 1,
                    })
            # quit()
    herbs = sorted(herbs, key=lambda x: x['mentions'], reverse=True)
    for herb in herbs:
        print(herb)
    print(len(herbs))
    herbs = herbs[:herbs_num]
    return herbs

def herbs_wcvp_medicinal_get():
    herbs = [
        io.json_read(f'{g.PLANT_MEDICINE_FOLDERPATH}/{filename}')
        for filename in os.listdir(f'{g.PLANT_MEDICINE_FOLDERPATH}')
    ]
    return herbs

def herbs_wcvp_get():
    herbs = io.csv_to_dict(
        f'{g.WCVP_FOLDERPATH}/wcvp_names.csv', 
        delimiter='|'
    )
    return herbs

def herb_name_common_get(herb_slug):
    herb_name_common = ''
    try:
        herb_slug = herb_slug.replace('mentha-piperita', 'mentha-x-piperita')
        ssot_herb_primary_filepath = f'{g.SSOT_FOLDERPATH}/herbs/herbs-primary/{herb_slug}.json'
        herb_data = io.json_read(ssot_herb_primary_filepath)
        herb_name_common = herb_data['herb_names_common'][0]['answer']
    except:
        pass
    return herb_name_common

########################################
# return ailments grouped by system
########################################
def systems_ailments_get():
    ailments = io.csv_to_dict(f'{g.DATABASE_FOLDERPATH}/csv/ailments.csv')
    clusters = []
    for ailment in ailments:
        system_slug = ailment['system_slug']
        organ_slug = ailment['organ_slug']
        ailment_slug = ailment['ailment_slug']
        ailment_name = ailment['ailment_name']
        found = False
        for cluster_i, cluster in enumerate(clusters):
            if system_slug == cluster['system_slug']:
                clusters[cluster_i]['ailments'].append(ailment)
                found = True
                break
        if not found:
            clusters.append(
                {
                    'system_slug': system_slug,
                    'ailments': [ailment],
                }
            )
    return clusters

########################################
# return ailments grouped by organ
########################################
def ailments_by_organ_get():
    ailments = io.csv_to_dict(f'{g.DATABASE_FOLDERPATH}/csv/ailments.csv')
    clusters = []
    for ailment in ailments:
        system_slug = ailment['system_slug']
        organ_slug = ailment['organ_slug']
        ailment_slug = ailment['ailment_slug']
        ailment_name = ailment['ailment_name']
        found = False
        for cluster_i, cluster in enumerate(clusters):
            if organ_slug == cluster['organ_slug']:
                clusters[cluster_i]['ailments'].append(ailment)
                found = True
                break
        if not found:
            clusters.append(
                {
                    'organ_slug': organ_slug,
                    'ailments': [ailment],
                }
            )
    return clusters

def organs_get():
    ailments = io.csv_to_dict(f'{g.DATABASE_FOLDERPATH}/csv/ailments.csv')
    organs = []
    for ailment in ailments:
        if ailment['organ_slug'] not in organs: organs.append(ailment['organ_slug'])
    return organs

def systems_get():
    ailments = io.csv_to_dict(f'{g.DATABASE_FOLDERPATH}/csv/ailments.csv')
    systems = []
    for ailment in ailments:
        if ailment['system_slug'] not in systems: systems.append(ailment['system_slug'])
    return systems

def phytochemicals_get(top=10):
    json_folderpath = f'{g.SSOT_FOLDERPATH}/phytochemicals'
    json_filepath = f'''{json_folderpath}/phytochemicals.json'''
    json_data = io.json_read(json_filepath)
    items = [item['answer'] for item in json_data['list'][:top]]
    return items
    
def actions_get(top=0):
    l = [
        'Anti-inflammatory',
        'Antimicrobial',
        'Antioxidant',
        'Adaptogenic',
        'Analgesic',
        'Antipyretic',
        'Sedative',
        'Carminative',
        'Diuretic',
        'Expectorant',
        'Immunomodulatory',
        'Antispasmodic',
        'Hepatoprotective',
        'Antidiabetic',
        'Cardiotonic',
    ]
    if top != 0:
        l = l[:top]
    return l

def preparations_get(top=0):
    l = [
        'Tinctures',
        'Teas',
        'Capsules',
        'Powders',
        'Oils',
        'Syrups',
        'Salves',
        'Poultices',
    ]
    if top != 0:
        l = l[:top]
    return l

def symptoms_get(top=0):
    l = [
        'Headache',
        'Migraine',
        'Abdominal Pain',
        'Low Back Pain',
        'Neck Pain',
        'Joint Pain',
        'Muscle Pain',
        'Menstrual Pain',
        'Nerve Pain',
        'Chest Pain',
    ]
    if top != 0:
        l = l[:top]
    return l

def herbs_get(top=0):
    herbs_filepath = f'{g.SSOT_FOLDERPATH}/herbs/herbs-medicinal-validated.json'
    l = io.json_read(herbs_filepath)
    if top != 0:
        l = l[:top]
    return l

################################################################################
# [0000_0001] WIKIDATA_POWO
################################################################################

def sqlite3__table_get(table_name, id_1=None, id_2=None):
    if id_1 == None and id_2 == None:
        conn = sqlite3.connect(f'{g.SSOT_FOLDERPATH}/sqlite/database.db')
        cur = conn.cursor()
        cur.execute(f"SELECT * FROM {table_name}")
        rows = cur.fetchall()
        conn.close()
        return rows
    elif id_1 != None and id_2 != None:
        return None
    elif id_1 == None and id_2 != None:
        conn = sqlite3.connect(f'{g.SSOT_FOLDERPATH}/sqlite/database.db')
        cur = conn.cursor()
        query = f"SELECT * FROM {table_name} WHERE {id_2[0]} = ?"
        cur.execute(query, (id_2[1],))
        row = cur.fetchone()
        conn.close()
        return row
    elif id_1 != None and id_2 == None:
        conn = sqlite3.connect(f'{g.SSOT_FOLDERPATH}/sqlite/database.db')
        cur = conn.cursor()
        query = f"SELECT * FROM {table_name} WHERE {id_1[0]} = ?"
        cur.execute(query, (id_1[1],))
        row = cur.fetchone()
        conn.close()
        return row

def sqlite3__wikidata_powo_get_all():
    rows = sqlite3__table_get('wikidata')
    conn = sqlite3.connect(f'{g.SSOT_FOLDERPATH}/sqlite/database.db')
    cur = conn.cursor()
    rows_found = []
    for row_i, row in enumerate(rows[:]):
        # print(row_i)
        wikidata_id = row[0]
        cur.execute("""
            SELECT *
            FROM wikidata t1
            JOIN powo t2 ON t1.powo_id = t2.powo_id
            WHERE t1.wikidata_id = ?
        """, (wikidata_id,))
        record = cur.fetchone()
        if record:
            rows_found.append(record)
    conn.close()
    return rows_found

################################################################################
# [0000] PLANTS
################################################################################

def studies__plants_popular_create():
    input_filepath = f'{g.SSOT_FOLDERPATH}/studies/extraction/plant-name-used_for-health-condition-name.json'
    input_data = io.json_read(input_filepath)
    items_group = []
    for item_i, item in enumerate(input_data):
        print(f'{item_i}/{len(input_data)} - {item}')
        found = False
        for item_group in items_group:
            if item['plant_name'] == item_group['name']:
                item_group['mentions'] += 1
                found = True
                break
        if not found:
            items_group.append({
                'name': item['plant_name'],
                'mentions': 1,
            })
    items_group = sorted(items_group, key=lambda x: x['mentions'], reverse=True)
    output_filepath = f'{g.SSOT_FOLDERPATH}/studies/extraction/json/plants-popular.json'
    io.json_write(output_filepath, items_group)
    return items_group

def studies__plants_popular_get(regen=False):
    filepath = f'{g.SSOT_FOLDERPATH}/studies/extraction/json/plants-popular.json'
    if regen:
        studies__plants_popular_create()
    else:
        if not os.path.exists(filepath):
            studies__plants_popular_create()
    items = io.json_read(filepath)
    return items

def search(items, key, val):
    for i, item in enumerate(items):
        if item[key].lower().strip() == val.lower().strip():
            return i
    return None

def studies__actions_popular_create():
    input_filepath = f'{g.SSOT_FOLDERPATH}/studies/extraction/plant-name-has_pharmacological_activity-pharmacological-activity-name.json'
    input_data = io.json_read(input_filepath)
    actions = []
    for item_i, item in enumerate(input_data[:]):
        print(f'{item_i}/{len(input_data)} - {item}')
        ###
        index = search(actions, 'name', item['pharmacological_activity_name'])
        if index: 
            actions[index]['mentions'] += 1
            index_plant = search(actions[index]['plants'], 'name', item['plant_name'])
            if index_plant: 
                actions[index]['plants'][index_plant]['mentions'] += 1
            else:
                actions[index]['plants'].append({'name': item['plant_name'], 'mentions': 1})
        else:
            actions.append({
                'name': item['pharmacological_activity_name'],
                'plants': [{'name': item['plant_name'], 'mentions': 1}],
                'mentions': 1,
            })
    actions = sorted(actions, key=lambda x: x['mentions'], reverse=True)
    # print(json.dumps(actions[:10], indent=4))
    # quit()
    output_filepath = f'{g.SSOT_FOLDERPATH}/studies/extraction/json/actions-popular.json'
    io.json_write(output_filepath, actions)

def studies__actions_popular_get(regen=False):
    filepath = f'{g.SSOT_FOLDERPATH}/studies/extraction/json/actions-popular.json'
    if regen:
        studies__actions_popular_create()
    else:
        if not os.path.exists(filepath):
            studies__actions_popular_create()
    items = io.json_read(filepath)
    return items

def sqlite3__wcvp_get(taxon_name):
    DB_PATH = f'{g.SSOT_FOLDERPATH}/datasets/powo/wcvp/wcvp.db'
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        SELECT *
        FROM wcvp
        WHERE LOWER(taxon_name) = LOWER(?)
    """, (taxon_name,))
    row = cur.fetchone()
    conn.close()
    return row

def sqlite__plants_get():
    db_filepath = f'{g.VAULT_FOLDERPATH}/terrawhisper/data/masterize/master.db'
    conn = sqlite3.connect(db_filepath)
    cur = conn.cursor()
    cur.execute("""
        SELECT *
        FROM plants
    """)
    row = cur.fetchall()
    conn.close()
    return row

def sqlite__plants_chemicals_get(plant_canonical_name):
    db_filepath = f'{g.VAULT_FOLDERPATH}/terrawhisper/data/observe/observations.db'
    conn = sqlite3.connect(db_filepath)
    cur = conn.cursor()
    cur.execute("""
        SELECT *
        FROM plants_chemicals
        WHERE LOWER(plant_canonical_name) = LOWER(?)
    """, (plant_canonical_name,))
    row = cur.fetchall()
    conn.close()
    return row

def sqlite__plants_activities_get(plant_canonical_name):
    db_filepath = f'{g.VAULT_FOLDERPATH}/terrawhisper/data/observe/observations.db'
    conn = sqlite3.connect(db_filepath)
    cur = conn.cursor()
    cur.execute("""
        SELECT *
        FROM plants_activities
        WHERE LOWER(plant_canonical_name) = LOWER(?)
    """, (plant_canonical_name,))
    row = cur.fetchall()
    conn.close()
    return row

def sqlite__plants_diseases_get(plant_canonical_name):
    db_filepath = f'{g.VAULT_FOLDERPATH}/terrawhisper/data/observe/observations.db'
    conn = sqlite3.connect(db_filepath)
    cur = conn.cursor()
    cur.execute("""
        SELECT *
        FROM plants_diseases
        WHERE LOWER(plant_canonical_name) = LOWER(?)
    """, (plant_canonical_name,))
    row = cur.fetchall()
    conn.close()
    return row

