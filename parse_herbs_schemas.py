'''
GENERAL SCHEMA FIELDS
[
    entity_1,
    relationship,
    entity_2,
    source_name,
    source_acronym,
    reference_id,
    reference_name,
]
'''

def schema_plants_activities_gen(
    plant_name_raw,
    relationship,
    activity_name_raw,
    source_name,
    source_acronym,
    reference_id,
    reference_name,
):
    item = {
        'plant_name_raw': plant_name_raw,
        'relationship': relationship,
        'activity_name_raw': activity_name_raw,
        'source_name': source_name,
        'source_acronym': source_acronym,
        'reference_id': reference_id,
        'reference_name': reference_name,
    }
    return item

def schema_plants_chemicals_gen(
    plant_name_raw,
    relationship,
    chemical_name_raw,
    source_name,
    source_acronym,
    reference_id,
    reference_name,
):
    item = {
        'plant_name_raw': plant_name_raw,
        'relationship': relationship,
        'chemical_name_raw': chemical_name_raw,
        'source_name': source_name,
        'source_acronym': source_acronym,
        'reference_id': reference_id,
        'reference_name': reference_name,
    }
    return item

