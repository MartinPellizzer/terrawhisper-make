import os
import time
import json
import shutil
import sqlite3

from lib import g
from lib import io

HUB_FOLDERPATH = f'{g.DATA_FOLDERPATH}/organizations'

output_folderpath = f'{HUB_FOLDERPATH}/observe'
db_filepath = f'{output_folderpath}/observations.db'

import parse_organizations_data

def observations_table_organizations_create_backup(regen=False):
    table_name = 'organizations'
    # quit()
    fields_data = parse_organizations_data.data
    table_fields = ''
    for field_item in fields_data:
        field_name = field_item['field_name']
        table_fields += f'''{field_name} TEXT,\n'''
    print(table_fields)
    quit()
    ###
    conn = sqlite3.connect(db_filepath)
    cur = conn.cursor()
    if regen: cur.execute(f"DROP TABLE IF EXISTS {table_name}")
    cur.execute(f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            id INTEGER PRIMARY KEY,
            business_gmap_label TEXT,
            business_gmap_name TEXT,
            business_gmap_website TEXT,
            business_is_category_herbs TEXT,
            business_name_official TEXT,
            business_name_legal TEXT,
            business_name_trade TEXT,
            business_slogan TEXT,
            business_description TEXT,
            business_description_short TEXT,
            business_founded_year TEXT,
            business_founding_story TEXT,
            business_founder_names TEXT,
            business_ownership_type TEXT,
            business_company_type TEXT,
            business_status TEXT,
            business_mission TEXT,
            business_vision TEXT,
            business_core_values TEXT,
            business_type_primary TEXT,
            business_type_secondary TEXT,
            business_industry TEXT, business_niche TEXT,
            business_model TEXT,
            business_website TEXT,
            business_email TEXT,
            business_email_customer_service TEXT,
            business_email_wholesale TEXT,
            business_email_media TEXT,
            business_phone TEXT,
            business_whatsapp TEXT,
            business_fax TEXT,
            business_contact_form TEXT,
            business_headquarters TEXT,
            business_address TEXT,
            business_city TEXT,
            business_state TEXT,
            business_region TEXT,
            business_country TEXT,
            business_postal_code TEXT,
            business_latitude TEXT,
            business_longitude TEXT,
            business_additional_locations TEXT,
            business_farm_locations TEXT,
            business_nursery_locations TEXT,
            business_factory_locations TEXT,
            business_laboratory_locations TEXT,
            business_warehouse_locations TEXT,
            business_retail_locations TEXT,
            business_opening_hours TEXT,
            business_seasonal_hours TEXT,
            business_appointment_required TEXT,
            business_walk_in_available TEXT,
            business_visitor_access TEXT,
            business_medicinal_plants TEXT,
            business_primary_medicinal_plants TEXT,
            business_specialty_plants TEXT,
            business_native_plants TEXT,
            business_rare_plants TEXT,
            business_medicinal_plant_categories TEXT,
            business_botanical_collection_size TEXT,
            business_grows TEXT,
            business_cultivates TEXT,
            business_propagates TEXT,
            business_researches TEXT,
            business_sells TEXT,
            business_distributes TEXT,
            business_exports TEXT,
            business_imports TEXT,
            business_wild_harvests TEXT,
            business_conserves TEXT,
            business_teaches TEXT,
            business_uses_in_products TEXT,
            business_products TEXT,
            business_product_categories TEXT,
            business_flagship_products TEXT,
            business_product_forms TEXT,
            business_herbal_teas TEXT,
            business_tinctures TEXT,
            business_extracts TEXT,
            business_essential_oils TEXT,
            business_capsules TEXT,
            business_powders TEXT,
            business_dried_herbs TEXT,
            business_fresh_herbs TEXT,
            business_seeds TEXT,
            business_seedlings TEXT,
            business_roots TEXT,
            business_bark TEXT,
            business_flowers TEXT,
            business_fruits TEXT,
            business_resins TEXT,
            business_cosmetics TEXT,
            business_soaps TEXT,
            business_creams TEXT,
            business_salves TEXT,
            business_syrups TEXT,
            business_botanical_name TEXT,
            business_common_name TEXT,
            business_plant_part TEXT,
            business_extraction_method TEXT,
            business_preparation_method TEXT,
            business_ingredients TEXT,
            business_packaging TEXT,
            business_package_sizes TEXT,
            business_concentration TEXT,
            business_organic_product TEXT,
            business_private_label TEXT,
            business_wholesale TEXT,
            business_retail TEXT,
            business_herbal_consultation TEXT,
            business_herbal_clinic TEXT,
            business_medicinal_plant_consulting TEXT,
            business_plant_identification TEXT,
            business_botanical_identification TEXT,
            business_cultivation_consulting TEXT,
            business_contract_growing TEXT,
            business_contract_manufacturing TEXT,
            business_private_label_manufacturing TEXT,
            business_extraction_services TEXT,
            business_drying_services TEXT,
            business_milling TEXT,
            business_grinding TEXT,
            business_packaging_service TEXT,
            business_export_services TEXT,
            business_laboratory_testing TEXT,
            business_formulation TEXT,
            business_research_services TEXT,
            business_education TEXT,
            business_workshops TEXT,
            business_courses TEXT,
            business_farm_tours TEXT,
            business_botanical_tours TEXT,
            business_cultivation_methods TEXT,
            business_organic_cultivation TEXT,
            business_regenerative TEXT,
            business_biodynamic TEXT,
            business_permaculture TEXT,
            business_agroforestry TEXT,
            business_greenhouse TEXT,
            business_indoor TEXT,
            business_outdoor TEXT,
            business_wild_harvesting TEXT,
            business_sustainable_wild_harvesting TEXT,
            business_propagation_methods TEXT,
            business_irrigation TEXT,
            business_fertilization TEXT,
            business_soil_management TEXT,
            business_pest_management TEXT,
            business_harvest_methods TEXT,
            business_harvest_season TEXT,
            business_manufacturing TEXT,
            business_processing TEXT,
            business_extraction TEXT,
            business_distillation TEXT,
            business_fermentation TEXT,
            business_drying TEXT,
            business_manufacturing_milling TEXT,
            business_manufacturing_grinding TEXT,
            business_blending TEXT,
            business_manufacturing_formulation TEXT,
            business_encapsulation TEXT,
            business_manufacturing_packaging TEXT,
            business_quality_testing TEXT,
            business_batch_testing TEXT,
            business_traceability TEXT,
            business_facilities_farms TEXT,
            business_facilities_nurseries TEXT,
            business_facilities_laboratories TEXT,
            business_facilities_factories TEXT,
            business_facilities_warehouses TEXT,
            business_facilities_botanical_gardens TEXT,
            business_facilities_greenhouses TEXT,
            business_facilities_visitor_centers TEXT,
            business_facilities_research_centers TEXT,
            business_facilities_education_centers TEXT,
            business_facilities_clinics TEXT,
            business_facilities_retail_stores TEXT,
            business_certifications_certifications TEXT,
            business_certifications_certification_name TEXT,
            business_certifications_certification_number TEXT,
            business_certifications_issuing_organization TEXT,
            business_certifications_issue_date TEXT,
            business_certifications_expiry_date TEXT,
            business_certifications_certification_scope TEXT,
            business_quality_quality_control TEXT,
            business_quality_laboratory_testing TEXT,
            business_quality_batch_testing TEXT,
            business_quality_third_party_testing TEXT,
            business_quality_traceability TEXT,
            business_quality_quality_management_system TEXT,
            business_sustainability_sustainability_policy TEXT,
            business_sustainability_conservation TEXT,
            business_sustainability_biodiversity TEXT,
            business_sustainability_regenerative_agriculture TEXT,
            business_sustainability_ethical_sourcing TEXT,
            business_sustainability_fair_trade TEXT,
            business_sustainability_community_projects TEXT,
            business_sustainability_indigenous_partnerships TEXT,
            business_sustainability_local_sourcing TEXT,
            business_sustainability_recyclable_packaging TEXT,
            business_sustainability_carbon_reduction TEXT,
            business_sustainability_water_conservation TEXT,
            business_research_research_programs TEXT,
            business_research_research_projects TEXT,
            business_research_publications TEXT,
            business_research_patents TEXT,
            business_research_university_partnerships TEXT,
            business_research_clinical_trials TEXT,
            business_research_ethnobotanical_research TEXT,
            business_research_pharmacognosy TEXT,
            business_research_phytochemistry TEXT,
            business_research_plant_breeding TEXT,
            business_education_courses TEXT,
            business_education_webinars TEXT,
            business_education_lectures TEXT,
            business_traditional_medicine_systems_ayurveda TEXT,
            business_traditional_medicine_systems_traditional_chinese_medicine TEXT,
            business_traditional_medicine_systems_western_herbalism TEXT,
            business_traditional_medicine_systems_unani TEXT,
            business_traditional_medicine_systems_kampo TEXT,
            business_traditional_medicine_systems_tibetan_medicine TEXT,
            business_traditional_medicine_systems_indigenous_medicine TEXT,
            business_traditional_medicine_systems_african_traditional_medicine TEXT,
            business_expertise_expertise_topics TEXT,
            business_expertise_medicinal_plant_cultivation TEXT,
            business_expertise_herbal_formulation TEXT,
            business_expertise_ethnobotany TEXT,
            business_expertise_pharmacognosy TEXT,
            business_expertise_herbal_medicine TEXT,
            business_expertise_conservation TEXT,
            business_people_founders TEXT,
            business_people_owners TEXT,
            business_people_ceo TEXT,
            business_people_president TEXT,
            business_people_director TEXT,
            business_people_botanists TEXT,
            business_people_herbalists TEXT,
            business_people_educators TEXT,
            business_people_farm_managers TEXT,
            business_markets_customer_types TEXT,
            business_markets_industries_served TEXT,
            business_markets_export_markets TEXT,
            business_markets_countries_served TEXT,
            business_markets_regions_served TEXT,
            business_markets_international_shipping TEXT,
            business_markets_wholesale_available TEXT,
            business_markets_retail_available TEXT,
            business_markets_private_label_available TEXT,
            business_online_presence_facebook TEXT,
            business_online_presence_instagram TEXT,
            business_online_presence_linkedin TEXT,
            business_online_presence_youtube TEXT,
            business_online_presence_x TEXT,
            business_online_presence_pinterest TEXT,
            business_online_presence_tiktok TEXT,
            business_awards_awards TEXT,
            business_policies_privacy_policy TEXT,
            business_policies_shipping_policy TEXT,
            business_policies_sustainability_policy TEXT,
            business_policies_accessibility_policy TEXT,
            business_languages_languages TEXT,
            business_languages_multilingual_support TEXT,
            business_commerce_accepted_payment_methods TEXT,
            business_commerce_currencies TEXT,
            business_commerce_online_store TEXT,
            business_commerce_ecommerce TEXT,
            business_shipping_shipping_countries TEXT,
            business_shipping_shipping_methods TEXT,
            business_shipping_international_shipping TEXT,
            business_shipping_local_delivery TEXT,
            source_name TEXT,
            source_acronym TEXT,
            business_name_normalize TEXT,
            business_name_display TEXT,
            business_slug TEXT,
            business_name_canonical TEXT
        );
    """)
    conn.execute("PRAGMA journal_mode = WAL;")
    conn.execute("PRAGMA synchronous = OFF;")
    conn.execute("PRAGMA temp_store = MEMORY;")
    conn.commit()
    conn.close()

def observations_table_organizations_create(regen=False):
    table_name = 'organizations'
    # quit()
    fields_data = parse_organizations_data.data
    table_fields = ''
    for field_item in fields_data:
        field_name = field_item['field_name']
        table_fields += f'''{field_name} TEXT,\n'''
    ###
    conn = sqlite3.connect(db_filepath)
    cur = conn.cursor()
    if regen: cur.execute(f"DROP TABLE IF EXISTS {table_name}")
    cur.execute(f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            id INTEGER PRIMARY KEY,
            {table_fields}
            source_name TEXT,
            source_acronym TEXT,
            business_name_normalize TEXT,
            business_name_display TEXT,
            business_slug TEXT,
            business_name_canonical TEXT
        );
    """)
    conn.execute("PRAGMA journal_mode = WAL;")
    conn.execute("PRAGMA synchronous = OFF;")
    conn.execute("PRAGMA temp_store = MEMORY;")
    conn.commit()
    conn.close()

def run():
    print('OBSERVE >> init')

    # try: shutil.rmtree(output_folderpath)
    # except: pass
    os.makedirs(output_folderpath, exist_ok=True)

    # fields_get()
    observations_table_organizations_create(regen=True)

