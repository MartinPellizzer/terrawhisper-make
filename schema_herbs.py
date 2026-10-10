### TODO: augment -> create paragraph with the more frequent info, not the first one (ex. the more frequent activities, not the first ones founded)

data = {
    'items': [
        {
            'process': False,
            'regen': False,
            'table_name': 'plants_activities',
            'fields': [
                {
                    'field_name': 'plant_name_scientific',
                },
                {
                    'field_name': 'relationship_name',
                },
                {
                    'field_name': 'activity_name',
                },
            ],
            'sources': [
                {
                    'source_name': 'pubmed',
                },
            ],
        },
        {
            'process': False,
            'regen': False,
            'table_name': 'plants_compounds',
            'fields': [
                {
                    'field_name': 'plant_name_scientific',
                },
                {
                    'field_name': 'relationship_name',
                },
                {
                    'field_name': 'compound_name',
                },
            ],
            'sources': [
                {
                    'source_name': 'pubmed',
                },
            ],
        },
        {
            'process': False,
            'regen': False,
            'table_name': 'plants_conditions',
            'fields': [
                {
                    'field_name': 'plant_name_scientific',
                },
                {
                    'field_name': 'relationship_name',
                },
                {
                    'field_name': 'condition_name',
                },
            ],
            'sources': [
                {
                    'source_name': 'pubmed',
                },
            ],
        },
        {
            'process': False,
            'regen': False,
            'table_name': 'plants_preparations',
            'fields': [
                {
                    'field_name': 'plant_name_scientific',
                },
                {
                    'field_name': 'relationship_name',
                },
                {
                    'field_name': 'preparation_name',
                },
            ],
            'sources': [
                {
                    'source_name': 'pubmed',
                },
            ],
        },
        {
            'process': False,
            'regen': False,
            'table_name': 'plants_plants_parts',
            'fields': [
                {
                    'field_name': 'plant_name_scientific',
                },
                {
                    'field_name': 'relationship_name',
                },
                {
                    'field_name': 'plant_part_name',
                },
            ],
            'sources': [
                {
                    'source_name': 'pubmed',
                },
            ],
        },
    ],
}

