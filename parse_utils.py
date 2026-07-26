def chemical_create(
    plant_name_raw, 
    chemical_name_raw, 
    plant_part_name_raw, 
    source_id, 
    source_name
):
    item = {
        'plant_name_raw': plant_name_raw,
        'chemical_name_raw': chemical_name_raw,
        'plant_part_name_raw': plant_part_name_raw,
        'source_id': source_id,
        'source_name': source_name,
    }
    return item
