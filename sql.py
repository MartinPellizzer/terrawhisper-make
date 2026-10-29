import json
import sqlite3

from lib import g

HUB_FOLDERPATH = f'''{g.DATA_FOLDERPATH}/herbs'''
output_folderpath = f'{HUB_FOLDERPATH}/database'
db_filepath = f'{output_folderpath}/terra.db'

sql_query_plants_activities_table_create = f'''
    CREATE TABLE IF NOT EXISTS plants_activities (
        plant_activity_id INTEGER PRIMARY KEY,
        plant_id TEXT,
        activity_id TEXT,
        study_id TEXT
    );
'''

########################################
# ENTITIES
########################################

def sql_plants():
    conn = sqlite3.connect(db_filepath)
    cur = conn.cursor()
    conn.row_factory = sqlite3.Row
    cursor = conn.execute(f'''
        SELECT * 
        FROM plants
    ''')
    rows = cursor.fetchall()
    items = [dict(row) for row in rows]
    return items

def sql_plant_id_by_name_normalize(name):
    conn = sqlite3.connect(db_filepath)
    cur = conn.cursor()
    conn.row_factory = sqlite3.Row
    cursor = conn.execute(f'''
        SELECT * 
        FROM plants
        WHERE plant_name_scientific_reference_normalize == ?
    ''', (name,))
    rows = cursor.fetchall()
    items = [dict(row) for row in rows]
    if items != []: item = items[0]
    else: item = None
    return item

def sql_activity_id_by_name_normalize(name):
    conn = sqlite3.connect(db_filepath)
    cur = conn.cursor()
    conn.row_factory = sqlite3.Row
    cursor = conn.execute(f'''
        SELECT * 
        FROM activities
        WHERE activity_name_reference_normalize == ?
    ''', (name,))
    rows = cursor.fetchall()
    items = [dict(row) for row in rows]
    if items != []: item = items[0]
    else: item = None
    return item

def sql_plant_name_common_id_by_name_normalize(name):
    conn = sqlite3.connect(db_filepath)
    cur = conn.cursor()
    conn.row_factory = sqlite3.Row
    cursor = conn.execute(f'''
        SELECT * 
        FROM plants_names_common
        WHERE plant_name_common_reference_normalize == ?
    ''', (name,))
    rows = cursor.fetchall()
    items = [dict(row) for row in rows]
    if items != []: item = items[0]
    else: item = None
    return item

def sql_study_id_by_pmid(pmid):
    conn = sqlite3.connect(db_filepath)
    cur = conn.cursor()
    conn.row_factory = sqlite3.Row
    cursor = conn.execute(f'''
        SELECT * 
        FROM studies
        WHERE study_pmid == ?
    ''', (pmid,))
    rows = cursor.fetchall()
    items = [dict(row) for row in rows]
    if items != []: item = items[0]
    else: item = None
    return item

########################################
# ASSERTIONS
########################################

def sql_plant_activities_by_name(name):
    conn = sqlite3.connect(db_filepath)
    cur = conn.cursor()
    conn.row_factory = sqlite3.Row
    query = '''
        SELECT
            p.*,
            a.*
        FROM plants AS p
        JOIN plants_activities AS pa
            ON p.plant_id = pa.plant_id
        JOIN activities AS a
            ON pa.activity_id = a.activity_id
        WHERE p.plant_name_scientific_reference_normalize = ?;
    '''
    query = '''
        SELECT
            plants.*,
            activities.*,
            studies.*
        FROM plants
        JOIN plants_activities
            ON plants.plant_id = plants_activities.plant_id
        JOIN activities
            ON plants_activities.activity_id = activities.activity_id
        JOIN studies
            ON plants_activities.study_id = studies.study_id
        WHERE plants.plant_name_scientific_reference_normalize = ?;
    '''
    query = '''
        SELECT
            activities.*,
            COUNT(*) AS count,
            json_group_array(
                json_object(
                    'study_pmid', studies.study_pmid,
                    'study_title', studies.study_title
                )
            ) AS studies
        FROM plants
        JOIN plants_activities
            ON plants.plant_id = plants_activities.plant_id
        JOIN activities
            ON plants_activities.activity_id = activities.activity_id
        JOIN studies
            ON plants_activities.study_id = studies.study_id
        WHERE plants.plant_name_scientific_reference_normalize = ?
        GROUP BY activities.activity_name_reference
        ORDER BY count DESC;
    '''
    """
    query = '''
        SELECT
            a.*,
            COUNT(*) AS occurrence_count
        FROM plants AS p
        JOIN plants_activities AS pa
            ON p.plant_id = pa.plant_id
        JOIN activities AS a
            ON pa.activity_id = a.activity_id
        WHERE p.plant_name_scientific_reference_normalize = ?
        GROUP BY a.activity_id
        ORDER BY occurrence_count DESC;
    '''
    """
    cursor = conn.execute(query, (name,))
    rows = cursor.fetchall()
    items = [dict(row) for row in rows]
    items = [
        {
            **dict(row),
            "studies": json.loads(row["studies"])
        }
        for row in rows
    ]
    conn.close()
    return items

def sql_plant_activities_by_plant_name_and_group(name):
    """
    Get all activities of a plant. 
    Group and sort them by frequency. 
    Include list of studies for each activity.
    """
    conn = sqlite3.connect(db_filepath)
    cur = conn.cursor()
    conn.row_factory = sqlite3.Row
    query = """
        SELECT
            plants.*,
            activities.*,
            COUNT(*) AS count,
            json_group_array(
                json_object(
                    'study_pmid', studies.study_pmid,
                    'study_title', studies.study_title
                )
            ) AS studies
        FROM plants
        JOIN plants_activities
            ON plants.plant_id = plants_activities.plant_id
        JOIN activities
            ON plants_activities.activity_id = activities.activity_id
        JOIN studies
            ON plants_activities.study_id = studies.study_id
        WHERE plants.plant_name_scientific_reference = ?
        GROUP BY activities.activity_id
        ORDER BY count DESC;
    """
    cursor = conn.execute(query, (name,))
    rows = cursor.fetchall()
    items = [dict(row) for row in rows]
    items = [
        {
            **dict(row),
            "studies": json.loads(row["studies"])
        }
        for row in rows
    ]
    conn.close()
    return items

def sql__plants__plants_names_common__by_plant_name__and_group_____backup(name):
    """
    """
    conn = sqlite3.connect(db_filepath)
    cur = conn.cursor()
    conn.row_factory = sqlite3.Row
    query = """
        SELECT
            plants.*,
            plants_names_common.*,
            COUNT(*) AS count,
            json_group_array(
                json_object(
                    'study_pmid', studies.study_pmid,
                    'study_title', studies.study_title
                )
            ) AS studies
        FROM plants
        JOIN plants__plants_names_common
            ON plants.plant_id = plants__plants_names_common.plant_id
        JOIN plants_names_common
            ON plants__plants_names_common.plant_name_common_id = plants_names_common.plant_name_common_id
        JOIN studies
            ON plants__plants_names_common.study_id = studies.study_id
        WHERE plants.plant_name_scientific_reference = ?
        GROUP BY plants_names_common.plant_name_common_id
        ORDER BY count DESC;
    """
    cursor = conn.execute(query, (name,))
    rows = cursor.fetchall()
    items = [dict(row) for row in rows]
    items = [
        {
            **dict(row),
            "studies": json.loads(row["studies"])
        }
        for row in rows
    ]
    conn.close()
    return items

def sql__plants__plants_names_common__by_plant_name__and_group(name):
    """
    """
    conn = sqlite3.connect(db_filepath)
    cur = conn.cursor()
    conn.row_factory = sqlite3.Row
    query = """
        SELECT
            plants.*,
            plants_names_common.*
        FROM plants
        JOIN plants__plants_names_common
            ON plants.plant_id = plants__plants_names_common.plant_id
        JOIN plants_names_common
            ON plants__plants_names_common.plant_name_common_id = plants_names_common.plant_name_common_id
        WHERE plants.plant_name_scientific_reference = ?
    """
    cursor = conn.execute(query, (name,))
    rows = cursor.fetchall()
    items = [dict(row) for row in rows]
    '''
    items = [
        {
            **dict(row),
            "studies": json.loads(row["studies"])
        }
        for row in rows
    ]
    '''
    conn.close()
    return items

