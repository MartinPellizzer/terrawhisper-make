def synonym_create(
    plant_name_raw, 
    plant_synonym_raw, 
    source_name,
):
    item = {
        'plant_name_raw': plant_name_raw,
        'plant_synonym_raw': plant_synonym_raw,
        'source_name': source_name,
    }
    return item

def activity_create(
    plant_name_raw,
    activity_name_raw,
    source_name,
    source_acronym,
    reference_name,
):
    item = {
        'plant_name_raw': plant_name_raw,
        'activity_name_raw': activity_name_raw,
        'source_name': source_name,
        'source_acronym': source_acronym,
        'reference_name': reference_name,
    }
    return item

def chemical_create(
    plant_name_raw, 
    chemical_name_raw, 
    plant_part_name_raw, 
    source_name,
    source_acronym,
    reference_name,
):
    if plant_part_name_raw == None: plant_part_name_raw = ''
    if plant_part_name_raw.lower() == 'null': plant_part_name_raw = ''
    item = {
        'plant_name_raw': plant_name_raw,
        'chemical_name_raw': chemical_name_raw,
        'plant_part_name_raw': plant_part_name_raw,
        'source_name': source_name,
        'source_acronym': source_acronym,
        'reference_name': reference_name,
    }
    return item


def common_name_create(
    plant_name_scientific_raw,
    plant_name_scientific_norm,
    plant_name_common_raw,
    plant_name_common_transliteration,
    plant_name_common_language,
    plant_name_common_preferred,
    plant_name_common_country,
    plant_name_common_area,
    plant_name_common_type,
    source_name,
    source_acronym,
):
    item = {
        'plant_name_scientific_raw': plant_name_scientific_raw,
        'plant_name_scientific_norm': plant_name_scientific_norm,
        'plant_name_common_raw': plant_name_common_raw,
        'plant_name_common_transliteration': plant_name_common_transliteration,
        'plant_name_common_language': plant_name_common_language,
        'plant_name_common_preferred': plant_name_common_preferred,
        'plant_name_common_country': plant_name_common_country,
        'plant_name_common_area': plant_name_common_area,
        'plant_name_common_type': plant_name_common_type,
        'source_name': source_name,
        'source_acronym': source_acronym,
    }
    return item

