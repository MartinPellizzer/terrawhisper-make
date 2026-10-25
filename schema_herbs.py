### TODO: augment -> create paragraph with the more frequent info, not the first one (ex. the more frequent activities, not the first ones founded)

morphology_data = {
    'items': [
        {
            'process': False,
            'regen': False,
            'table_name': 'plants_growth_forms',
            'section_heading': 'Morphologies',
            'fields': [
                {'field_name': 'plant_name_scientific',},
                {'field_name': 'relationship_name',},
                {'field_name': 'growth_form_name',},
                {'field_name': 'category', 'derive': 1, 'augment': 0},
            ],
            'sources': [
                {
                    'source_name': 'gift',
                },
            ],
        },

        {
            'process': False,
            'regen': False,
            'table_name': 'plants_climbers',
            'section_heading': 'Morphologies',
            'fields': [
                {'field_name': 'plant_name_scientific',},
                {'field_name': 'relationship_name',},
                {'field_name': 'climber_name',},
                {'field_name': 'category', 'derive': 1, 'augment': 0},
            ],
            'sources': [
                {
                    'source_name': 'gift',
                },
            ],
        },

        {
            'process': False,
            'regen': False,
            'table_name': 'plants_heights',
            'section_heading': 'Morphologies',
            'fields': [
                {'field_name': 'plant_name_scientific',},
                {'field_name': 'relationship_name',},
                {'field_name': 'height_name',},
                {'field_name': 'category', 'derive': 1, 'augment': 0},
            ],
            'sources': [
                {
                    'source_name': 'gift',
                },
            ],
        },
    ]
}

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
            'process': False,
            'regen': False,
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
            'table_name': 'plants_taxonomies',
            'section_heading': 'Taxonomical Classification',
            'fields': [
                {'field_name': 'plant_name_scientific',},
                {'field_name': 'relationship_name',},
                {'field_name': 'taxonomy_name',},
                {'field_name': 'taxonomy_level',},
            ],
            'sources': [
                {
                    'source_name': 'powo',
                },
            ],
        },

        {
            'process': False,
            'regen': False,
            'table_name': 'plants_distributions',
            'section_heading': 'Distribution',
            'fields': [
                {'field_name': 'plant_name_scientific',},
                {'field_name': 'relationship_name',},
                {'field_name': 'locality_continent_name',},
                {'field_name': 'locality_continent_code',},
                {'field_name': 'locality_region_name', 'augment': 1,},
                {'field_name': 'locality_region_code',},
                {'field_name': 'locality_area_name', 'augment': 1,},
                {'field_name': 'locality_area_code',},
                {'field_name': 'locality_introduced',},
                {'field_name': 'locality_extinct',},
                {'field_name': 'locality_doubtful',},
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
                {'field_name': 'plant_name_scientific',},
                {'field_name': 'relationship_name',},
                {'field_name': 'activity_name',},
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
                {'field_name': 'plant_name_scientific',},
                {'field_name': 'relationship_name',},
                {'field_name': 'plant_part_name',},
            ],
            'sources': [
                {
                    'source_name': 'pubmed',
                },
            ],
        },
    ],
}

for morphology_item in morphology_data['items']:
    data['items'].append(morphology_item)

"""
{
    'process': True,
    'regen': True,
    'table_name': 'plants_traits',
    'section_heading': 'Traits',
    'fields': [
        {'field_name': 'plant_name_scientific',},
        {'field_name': 'relationship_name',},
        {'field_name': 'trait_1_name', 'augment': 0},
        {'field_name': 'trait_2_name', 'derive': 1, 'augment': 0},
        {'field_name': 'trait_units', 'derive': 1, 'augment': 0},
        {'field_name': 'trait_type', 'derive': 1,},
        {'field_name': 'trait_value', 'derive': 1, 'augment': 0},
        {'field_name': 'trait_category', 'derive': 1,},
        {'field_name': 'plant_author', 'derive': 1,},
        {'field_name': 'plant_genus', 'derive': 1,},
        {'field_name': 'trait_agreement', 'derive': 1,},
        {'field_name': 'trait_coeff_var', 'derive': 1,},
        {'field_name': 'trait_n', 'derive': 0,},
        {'field_name': 'trait_refs', 'derive': 0,},
    ],
    'sources': [
        {
            'source_name': 'gift',
        },
    ],
},
"""

"""
        {
            'process': True,
            'regen': True,
            'table_name': 'plants_traits',
            'section_heading': 'Traits',
            'fields': [
                {'field_name': 'plant_name_scientific',},
                {'field_name': 'relationship_name',},
                {'field_name': 'trait_name', 'augment': 0},
                {'field_name': 'category', 'derive': 1, 'augment': 0},
            ],
            'sources': [
                {
                    'source_name': 'gift',
                },
            ],
        },
"""
