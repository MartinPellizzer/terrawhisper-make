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

def schema_plants_conditions_gen(
    plant_name_raw,
    relationship,
    condition_name_raw,
    source_name,
    source_acronym,
    reference_id,
    reference_name,
):
    item = {
        'plant_name_raw': plant_name_raw,
        'relationship': relationship,
        'condition_name_raw': condition_name_raw,
        'source_name': source_name,
        'source_acronym': source_acronym,
        'reference_id': reference_id,
        'reference_name': reference_name,
    }
    return item

def schema_plants_parts_gen(
    plant_name_raw,
    relationship,
    plant_part_name_raw,
    source_name,
    source_acronym,
    reference_id,
    reference_name,
):
    item = {
        'plant_name_raw': plant_name_raw,
        'relationship': relationship,
        'plant_part_name_raw': plant_part_name_raw,
        'source_name': source_name,
        'source_acronym': source_acronym,
        'reference_id': reference_id,
        'reference_name': reference_name,
    }
    return item

def schema_preparations_gen(
    plant_name_raw,
    relationship,
    preparation_name_raw,
    source_name,
    source_acronym,
    reference_id,
    reference_name,
):
    item = {
        'plant_name_raw': plant_name_raw,
        'relationship': relationship,
        'preparation_name_raw': preparation_name_raw,
        'source_name': source_name,
        'source_acronym': source_acronym,
        'reference_id': reference_id,
        'reference_name': reference_name,
    }
    return item

