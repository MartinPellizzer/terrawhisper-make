### TODO: augment -> create paragraph with the more frequent info, not the first one (ex. the more frequent activities, not the first ones founded)

data = {
    'items': [
        {
            'process': False,
            'regen': False,
            'table_name': 'plants_names_common',
            'section_heading': 'Common names',
            'fields': [
                {'field_name': 'plant_name_scientific',},
                {'field_name': 'relationship_name',},
                {'field_name': 'plant_name_common',},
                {'field_name': 'plant_name_transliteration',},
                {'field_name': 'plant_name_language',},
                {'field_name': 'plant_name_preferred',},
                {'field_name': 'plant_name_country',},
                {'field_name': 'plant_name_area',},
                {'field_name': 'plant_name_type',},
            ],
            'sources': [
                {
                    'source_name': 'col',
                },
            ],
        },
        {
            'process': True,
            'regen': True,
            'table_name': 'plants_synonyms',
            'section_heading': 'Synonyms',
            'fields': [
                {'field_name': 'plant_name_scientific',},
                {'field_name': 'relationship_name',},
                {'field_name': 'plant_synonym',},
            ],
            'sources': [
                {
                    'source_name': 'wcvp',
                },
            ],
        },
        {
            'process': False,
            'regen': False,
            'table_name': 'plants_activities',
            'section_heading': 'Biological Activities',
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
            'section_heading': 'Compounds',
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
            'section_heading': 'Conditions',
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
            'section_heading': 'Preparations',
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
            'section_heading': 'Parts used',
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

