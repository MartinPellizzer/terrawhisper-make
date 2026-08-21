import os
import re
import csv
import ast
import json
import sqlite3
import unicodedata

from lorem_text import lorem

from lib import g
from lib import io
from lib import sections
from lib import components

import masterize_organizations_utils

HUB_FOLDERPATH = f'{g.DATA_FOLDERPATH}/organizations'

_NON_ALNUM = re.compile(r"[^\w\s-]", re.UNICODE)
_SEPARATORS = re.compile(r"[-\s]+")

def to_slug(name: str) -> str:
    """Convert an organization name into a stable, URL-safe slug."""
    name = unicodedata.normalize("NFKD", name)
    name = "".join(c for c in name if not unicodedata.combining(c))
    name = name.replace("&", " and ")
    name = _NON_ALNUM.sub("", name)
    return _SEPARATORS.sub("-", name).strip("-").lower()


def make_slug(canonical_name: str) -> str:
    """
    Convert canonical name into a URL-safe slug.
    Example:
        'BREDUN LP' -> 'bredun-lp'
    """
    if not canonical_name:
        return ""

    # Normalize Unicode
    slug = unicodedata.normalize("NFKD", canonical_name)

    # Remove accents / non-ASCII characters
    slug = slug.encode("ascii", "ignore").decode("ascii")

    # Lowercase
    slug = slug.lower()

    # Replace any sequence of non-alphanumeric characters with "-"
    slug = re.sub(r"[^a-z0-9]+", "-", slug)

    # Remove leading/trailing hyphens
    return slug.strip("-")


def normalize_entity(raw_name: str) -> dict:
    """
    Return the raw name, canonical name, and URL slug.
    """
    canonical_name = normalize_name(raw_name)

    return {
        "raw_name": raw_name,
        "canonical_name": canonical_name,
        "slug": make_slug(canonical_name),
    }

import re


STRONG_HERB_TERMS = {
    "ashwagandha",
    "aloe",
    "arnica",
    "artemisia",
    "calendula",
    "chamomile",
    "echinacea",
    "elderberry",
    "ginkgo",
    "ginseng",
    "gotu kola",
    "hawthorn",
    "hibiscus",
    "holy basil",
    "horsetail",
    "lavender",
    "lemon balm",
    "licorice",
    "marshmallow",
    "milk thistle",
    "moringa",
    "mugwort",
    "nettle",
    "peppermint",
    "rosemary",
    "sage",
    "st john's wort",
    "turmeric",
    "valerian",
    "yarrow",
}

BOTANICAL_TERMS = {
    "herb",
    "herbs",
    "botanical",
    "botanicals",
    "medicinal plant",
    "medicinal plants",
    "dried plant",
    "dried leaves",
    "dried flowers",
    "dried roots",
}

HERBAL_CROPS = {
    "basil",
    "mint",
    "peppermint",
    "spearmint",
    "oregano",
    "thyme",
    "sage",
    "rosemary",
    "marjoram",
    "dill",
    "parsley",
    "cilantro",
    "coriander",
    "tarragon",
    "lemongrass",
}


def herb_relevance(record):
    """
    Classify a USDA operation based only on USDA data.
    """

    # Combine certified product fields
    product_text = " ".join([
        record.get("CR_CertifiedProducts", ""),
        record.get("CR_CertifiedProducts_Add", ""),
        record.get("LS_CertifiedProducts", ""),
        record.get("LS_CertifiedProducts_Add", ""),
        record.get("WC_CertifiedProducts", ""),
        record.get("WC_CertifiedProducts_Add", ""),
        record.get("Han_CertifiedProducts", ""),
        record.get("Han_CertifiedProducts_Add", ""),
    ]).lower()

    # Normalize whitespace
    product_text = re.sub(r"\s+", " ", product_text)

    score = 0
    matches = []

    # Strong herb matches
    for term in STRONG_HERB_TERMS:
        if term in product_text:
            score += 10
            matches.append(term)

    # Botanical matches
    for term in BOTANICAL_TERMS:
        if term in product_text:
            score += 5
            matches.append(term)

    # Herbal crop matches
    for term in HERBAL_CROPS:
        if term in product_text:
            score += 5
            matches.append(term)

    # Classification
    if score >= 10:
        classification = "strong"

    elif score >= 5:
        classification = "possible"

    else:
        classification = "none"

    return {
        "herb_score": score,
        "herb_classification": classification,
        "herb_matches": sorted(set(matches)),
    }

def classify_usda_operation(record):
    types = []
    if record.get("opSC_CR") == "Certified":
        types.append("CROP_PRODUCER")
    if record.get("opSC_WC") == "Certified":
        types.append("WILD_CROP_OPERATOR")
    if record.get("opSC_LS") == "Certified":
        types.append("LIVESTOCK_PRODUCER")
    if record.get("opSC_HANDLING") == "Certified":
        types.append("HANDLER")
    if record.get("opEx_broker"):
        types.append("BROKER")
    if record.get("opEx_distributor"):
        types.append("DISTRIBUTOR")
    if record.get("opEx_marketerTrader"):
        types.append("MARKETER_TRADER")
    if record.get("opEx_retailer"):
        types.append("RETAILER")
    if record.get("opEx_privateLabeler"):
        types.append("PRIVATE_LABELER")
    if record.get("opEx_copacker"):
        types.append("CO_PACKER")
    if record.get("opEx_storage"):
        types.append("STORAGE")
    return types

def classify_product_domain(record):
    text = " ".join([
        record.get("CR_CertifiedProducts", ""),
        record.get("LS_CertifiedProducts", ""),
        record.get("WC_CertifiedProducts", ""),
        record.get("Han_CertifiedProducts", ""),
    ]).lower()
    # Broad plant signals
    plant_terms = [
        "crop",
        "grain",
        "wheat",
        "barley",
        "rice",
        "corn",
        "maize",
        "lentil",
        "pea",
        "bean",
        "seed",
        "fruit",
        "vegetable",
        "flower",
        "leaf",
        "root",
        "plant",
        "herb",
        "spice",
        "tree",
        "vine",
    ]
    plant_terms = [
        'ashwagandha',
    ]
    if any(term in text for term in plant_terms):
        return "PLANT"
    return "UNKNOWN"

def render_listing(master_item):
    business_name_canonical = master_item['business_name_canonical']
    business_name_display = master_item['business_name_display']
    business_slug = master_item['business_slug']
    url_slug = f'organizations/{business_slug}'

    input_data = io.json_read(f'{HUB_FOLDERPATH}/compile/{business_name_canonical}.json')

    # if len(input_data['identity'][0]) < 2: return
    # print(json.dumps(input_data, indent=4))
    # quit()

    html_article = ''

    if 1:
        html_article += f'<h1>{business_name_display}</h1>'

        # print(json.dumps(input_data, indent=4))
        # quit()

        identity_data = input_data['identity']
        location_data = input_data['location']
        contact_data = input_data['contact']

        
        identity_gmap_item = None
        for identity_list in identity_data:
            # print(json.dumps(identity_list, indent=4))
            for identity_item in identity_list:
                # print(json.dumps(identity_item, indent=4))
                if identity_item['source_name'] == 'Google Maps':
                    identity_gmap_item = identity_item

        location_gmap_item = None
        for lst in location_data:
            # print(json.dumps(identity_list, indent=4))
            for item in lst:
                # print(json.dumps(location_item, indent=4))
                if item['source_name'] == 'Google Maps':
                    location_gmap_item = item

        contact_gmap_item = None
        for lst in contact_data:
            for item in lst:
                if item['source_name'] == 'Google Maps':
                    contact_gmap_item = item

        # print(json.dumps(identity_data, indent=4))
        # quit()
        # print(json.dumps(gmap_item, indent=4))
        # quit()
        html_article += f'''<h2>Identity</h2>'''
        html_article += f'''<p>{identity_gmap_item['llm']}</p>'''

        html_article += f'''<p>address: {location_gmap_item['fields']['business_address']}</p>'''
        html_article += f'''<p>phone: {contact_gmap_item['fields']['business_phone']}</p>'''
        html_article += f'''<p>website: {identity_gmap_item['fields']['business_website']}</p>'''
        html_article += f'''
            <p>
                rating: {identity_gmap_item['fields']['business_rating']} ({identity_gmap_item['fields']['business_reviews_num']})
            </p>
        '''
        html_article += f'''
<iframe src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3348.0964118728743!2d-96.84058512365978!3d32.94846387520341!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x864e9fecd95cce51%3A0xce8e79e6fdad6e5c!2sCHIOMA%20Co.%20Wellness%20%26%20Beauty%20Apothecary!5e0!3m2!1sen!2sit!4v1787318301722!5m2!1sen!2sit" width="600" height="450" style="border:0;" allowfullscreen="" loading="lazy" referrerpolicy="strict-origin-when-cross-origin"></iframe>
        '''

        """
        location_data = input_data['location']
        html_article += f'''<h2>Location</h2>'''
        html_article += f'''<p>{location_data[0]['llm']}</p>'''
        """
    else:
        for input_key, input_val in input_data.items():
            # print(input_key, input_val)
            if input_key == 'business_name_canonical': continue
            html_article += f'''<h2>{input_key}</h2>'''
            html_article += f'''<p>{input_val[0]['llm']}</p>'''
            for field_key, field_val in input_val[0].items():
                if field_key == 'llm': continue
                html_article += f'''<p>{field_key}: {field_val}</p>'''
                # print(html_article)
        # quit()
        
    """
    quit()

    ###
    identity_data = input_data['identity'][0]


    html_article += f'''<p>{identity_data['llm']}</p>'''

    ## Business Overview
    fields = {
        'business_is_category_herbs': identity_data['business_is_category_herbs'],
        'official business name': identity_data['official business name'],
        'business slogan': identity_data['business slogan'],
        'short business description': identity_data['short business description'],
        'business description': identity_data['business description'],
        'primary business type': identity_data['primary business type'],
        'secondary business type': identity_data['secondary business type'],
        'business industry': identity_data['business industry'],
        'business niche': identity_data['business niche'],
        'business model': identity_data['business model'],
        'business status': identity_data['business status'],
    }
    html_article += f'<h2>Business Overview</h2>'
    for key, val in fields.items():
        if val != None:
            html_article += f'<p>{key}: {val}</p>'
        else:
            html_article += f'<p style="color: red;">{key}: {val}</p>'
    """

    '''
    ## Business Identity
    fields = {
        'legal business name': row['business_name_legal'],
        'trading business name': row['business_name_trade'],
        'business company type': row['business_company_type'],
        'business ownership type': row['business_ownership_type'],
        'business year founded': row['business_founded_year'],
        'business founding story': row['business_founding_story'],
        'business founder names': row['business_founder_names'],
        'business mission': row['business_mission'],
        'business vision': row['business_vision'],
        'business core values': row['business_core_values'],
    }
    html_article += f'<h2>Business Identity and History</h2>'
    for key, val in fields.items():
        if val != None:
            html_article += f'<p>{key}: {val}</p>'
        else:
            html_article += f'<p style="color: red;">{key}: {val}</p>'

    # 3. Location & Geographic Presence
    fields = {
        'business headquarters': row['business_headquarters'],
        'business address': row['business_address'],
        'business city': row['business_city'],
        'business state': row['business_state'],
        'business region': row['business_region'],
        'business country': row['business_country'],
        'business postal code': row['business_postal_code'],
        'business latitude': row['business_latitude'],
        'business longitude': row['business_longitude'],
        'business additional locations': row['business_additional_locations'],
        'business farm locations': row['business_farm_locations'],
        'business nursery locations': row['business_nursery_locations'],
        'business factory locations': row['business_factory_locations'],
        'business laboratory locations': row['business_laboratory_locations'],
        'business warehouse locations': row['business_warehouse_locations'],
        'business retail locations': row['business_retail_locations'],
    }
    html_article += f'<h2>Location and Geographic Presence</h2>'
    for key, val in fields.items():
        if val != None:
            html_article += f'<p>{key}: {val}</p>'
        else:
            html_article += f'<p style="color: red;">{key}: {val}</p>'

    # 4. Visitor Information
    fields = {
        'opening_hours': row['business_opening_hours'],
        'seasonal_hours': row['business_seasonal_hours'],
        'appointment_required': row['business_appointment_required'],
        'walk_in_available': row['business_walk_in_available'],
        'visitor_access': row['business_visitor_access'],
    }
    html_article += f'<h2>Visitor Information</h2>'
    for key, val in fields.items():
        if val != None:
            html_article += f'<p>{key}: {val}</p>'
        else:
            html_article += f'<p style="color: red;">{key}: {val}</p>'

    # 5. Medicinal Plant Focus
    fields = {
        'medicinal_plants ': row['business_medicinal_plants'],
        'primary_medicinal_plants': row['business_primary_medicinal_plants'],
        'specialty_plants': row['business_specialty_plants'],
        'native_plants': row['business_native_plants'],
        'rare_plants': row['business_rare_plants'],
        'medicinal_plant_categories': row['business_medicinal_plant_categories'],
        'botanical_collection_size': row['business_botanical_collection_size'],
    }
    html_article += f'<h2>Medicinal Plant Focus</h2>'
    for key, val in fields.items():
        if val != None:
            html_article += f'<p>{key}: {val}</p>'
        else:
            html_article += f'<p style="color: red;">{key}: {val}</p>'

    # 6. Botanical Activities
    fields = {
        'grows': row['business_grows'],
        'cultivates': row['business_cultivates'],
        'propagates': row['business_propagates'],
        'researches': row['business_researches'],
        'sells': row['business_sells'],
        'distributes': row['business_distributes'],
        'exports': row['business_exports'],
        'imports': row['business_imports'],
        'wild_harvests': row['business_wild_harvests'],
        'conserves': row['business_conserves'],
        'teaches': row['business_teaches'],
        'uses_in_products': row['business_uses_in_products'],
    }
    html_article += f'<h2>Botanical Activities</h2>'
    for key, val in fields.items():
        if val != None:
            html_article += f'<p>{key}: {val}</p>'
        else:
            html_article += f'<p style="color: red;">{key}: {val}</p>'

    # 7. Products
    fields = {
        'products': row['business_products'],
        'product_categories': row['business_product_categories'],
        'flagship_products': row['business_flagship_products'],
        'product_forms': row['business_product_forms'],
    }
    html_article += f'<h2>Products</h2>'
    for key, val in fields.items():
        if val != None:
            html_article += f'<p>{key}: {val}</p>'
        else:
            html_article += f'<p style="color: red;">{key}: {val}</p>'

    # 8. Product Types
    fields = {
        'herbal_teas': row['business_herbal_teas'],
        'tinctures': row['business_tinctures'],
        'extracts': row['business_extracts'],
        'essential_oils': row['business_essential_oils'],
        'capsules': row['business_capsules'],
        'powders': row['business_powders'],
        'dried_herbs': row['business_dried_herbs'],
        'fresh_herbs': row['business_fresh_herbs'],
        'seeds': row['business_seeds'],
        'seedlings': row['business_seedlings'],
        'roots': row['business_roots'],
        'bark': row['business_bark'],
        'flowers': row['business_flowers'],
        'fruits': row['business_fruits'],
        'resins': row['business_resins'],
        'cosmetics': row['business_cosmetics'],
        'soaps': row['business_soaps'],
        'creams': row['business_creams'],
        'salves': row['business_salves'],
        'syrups': row['business_syrups'],
    }
    html_article += f'<h2>Product Types</h2>'
    for key, val in fields.items():
        if val != None:
            html_article += f'<p>{key}: {val}</p>'
        else:
            html_article += f'<p style="color: red;">{key}: {val}</p>'

    # 9. Product Specifications
    fields = {
        'botanical_name': row['business_botanical_name'],
        'common_name': row['business_common_name'],
        'plant_part': row['business_plant_part'],
        'extraction_method': row['business_extraction_method'],
        'preparation_method': row['business_preparation_method'],
        'ingredients': row['business_ingredients'],
        'packaging': row['business_packaging'],
        'package_sizes': row['business_package_sizes'],
        'concentration': row['business_concentration'],
        'organic_product': row['business_organic_product'],
        'private_label': row['business_private_label'],
        'wholesale': row['business_wholesale'],
        'retail': row['business_retail'],
    }
    html_article += f'<h2>Product Specifications</h2>'
    for key, val in fields.items():
        if val != None:
            html_article += f'<p>{key}: {val}</p>'
        else:
            html_article += f'<p style="color: red;">{key}: {val}</p>'

    # 10. Services
    fields = {
        'herbal consultation': row['business_herbal_consultation'],
        'herbal clinic': row['business_herbal_clinic'],
        'medicinal plant consulting': row['business_medicinal_plant_consulting'],
        'plant identification': row['business_plant_identification'],
        'botanical identification': row['business_botanical_identification'],
        'cultivation consulting': row['business_cultivation_consulting'],
        'contract growing': row['business_contract_growing'],
        'contract manufacturing': row['business_contract_manufacturing'],
        'private label manufacturing': row['business_private_label_manufacturing'],
        'extraction services': row['business_extraction_services'],
        'drying services': row['business_drying_services'],
        'milling': row['business_milling'],
        'grinding': row['business_grinding'],
        'packaging_service': row['business_packaging_service'],
        'export services': row['business_export_services'],
        'laboratory testing': row['business_laboratory_testing'],
        'formulation': row['business_formulation'],
        'research services': row['business_research_services'],
        'education': row['business_education'],
        'workshops': row['business_workshops'],
        'courses': row['business_courses'],
        'farm tours': row['business_farm_tours'],
        'botanical tours': row['business_botanical_tours'],
    }
    html_article += f'<h2>Services</h2>'
    for key, val in fields.items():
        if val != None:
            html_article += f'<p>{key}: {val}</p>'
        else:
            html_article += f'<p style="color: red;">{key}: {val}</p>'

    # 11. Cultivation & Agricultural Practices
    fields = {
        'cultivation_methods': row['business_cultivation_methods'],
        'organic_cultivation': row['business_organic_cultivation'],
        'regenerative': row['business_regenerative'],
        'biodynamic': row['business_biodynamic'],
        'permaculture': row['business_permaculture'],
        'agroforestry': row['business_agroforestry'],
        'greenhouse': row['business_greenhouse'],
        'indoor': row['business_indoor'],
        'outdoor': row['business_outdoor'],
        'wild_harvesting': row['business_wild_harvesting'],
        'sustainable_wild_harvesting': row['business_sustainable_wild_harvesting'],
        'propagation_methods': row['business_propagation_methods'],
        'irrigation': row['business_irrigation'],
        'fertilization': row['business_fertilization'],
        'soil_management': row['business_soil_management'],
        'pest_management': row['business_pest_management'],
        'harvest_methods': row['business_harvest_methods'],
        'harvest_season': row['business_harvest_season'],
    }
    html_article += f'<h2>Cultivation and Agricultural Practices</h2>'
    for key, val in fields.items():
        if val != None:
            html_article += f'<p>{key}: {val}</p>'
        else:
            html_article += f'<p style="color: red;">{key}: {val}</p>'

    # 12. Processing & Manufacturing
    fields = {
        'manufacturing': row['business_manufacturing'],
        'processing': row['business_processing'],
        'extraction': row['business_extraction'],
        'distillation': row['business_distillation'],
        'fermentation': row['business_fermentation'],
        'drying': row['business_drying'],
        'manufacturing_milling': row['business_manufacturing_milling'],
        'manufacturing_grinding': row['business_manufacturing_grinding'],
        'blending': row['business_blending'],
        'manufacturing_formulation': row['business_manufacturing_formulation'],
        'encapsulation': row['business_encapsulation'],
        'manufacturing_packaging': row['business_manufacturing_packaging'],
        'quality_testing': row['business_quality_testing'],
        'batch_testing': row['business_batch_testing'],
        'traceability': row['business_traceability'],
    }
    html_article += f'<h2>Processing and Manufacturing</h2>'
    for key, val in fields.items():
        if val != None:
            html_article += f'<p>{key}: {val}</p>'
        else:
            html_article += f'<p style="color: red;">{key}: {val}</p>'

    # 13. Facilities & Infrastructure
    fields = {
        'farms': row['business_facilities_farms'],
        'nurseries': row['business_facilities_nurseries'],
        'laboratories': row['business_facilities_laboratories'],
        'factories': row['business_facilities_factories'],
        'warehouses': row['business_facilities_warehouses'],
        'botanical_gardens': row['business_facilities_botanical_gardens'],
        'greenhouses': row['business_facilities_greenhouses'],
        'visitor_centers': row['business_facilities_visitor_centers'],
        'research_centers': row['business_facilities_research_centers'],
        'education_centers': row['business_facilities_education_centers'],
        'clinics': row['business_facilities_clinics'],
        'retail_stores': row['business_facilities_retail_stores'],
    }
    html_article += f'<h2>Facilities and Infrastructure</h2>'
    for key, val in fields.items():
        if val != None:
            html_article += f'<p>{key}: {val}</p>'
        else:
            html_article += f'<p style="color: red;">{key}: {val}</p>'

    # 14. Quality, Testing & Certifications
    fields = {
        'quality_control': row['business_quality_quality_control'],
        'laboratory_testing': row['business_quality_laboratory_testing'],
        'batch_testing': row['business_quality_batch_testing'],
        'third_party_testing': row['business_quality_third_party_testing'],
        'traceability': row['business_quality_traceability'],
        'quality_management_system': row['business_quality_quality_management_system'],
        'certifications': row['business_certifications_certifications'],
        'certification_name': row['business_certifications_certification_name'],
        'certification_number': row['business_certifications_certification_number'],
        'issuing_organization': row['business_certifications_issuing_organization'],
        'issue_date': row['business_certifications_issue_date'],
        'expiry_date': row['business_certifications_expiry_date'],
        'certification_scope': row['business_certifications_certification_scope'],
    }
    html_article += f'<h2>Quality, Testing and Certifications</h2>'
    for key, val in fields.items():
        if val != None:
            html_article += f'<p>{key}: {val}</p>'
        else:
            html_article += f'<p style="color: red;">{key}: {val}</p>'

    # 15. Sustainability & Conservation
    fields = {
        'sustainability_policy': row['business_sustainability_sustainability_policy'],
        'conservation': row['business_sustainability_conservation'],
        'biodiversity': row['business_sustainability_biodiversity'],
        'regenerative_agriculture': row['business_sustainability_regenerative_agriculture'],
        'ethical_sourcing': row['business_sustainability_ethical_sourcing'],
        'fair_trade': row['business_sustainability_fair_trade'],
        'community_projects': row['business_sustainability_community_projects'],
        'indigenous_partnerships': row['business_sustainability_indigenous_partnerships'],
        'local_sourcing': row['business_sustainability_local_sourcing'],
        'recyclable_packaging': row['business_sustainability_recyclable_packaging'],
        'carbon_reduction': row['business_sustainability_carbon_reduction'],
        'water_conservation': row['business_sustainability_water_conservation'],
    }
    html_article += f'<h2>Sustainability and Conservation</h2>'
    for key, val in fields.items():
        if val != None:
            html_article += f'<p>{key}: {val}</p>'
        else:
            html_article += f'<p style="color: red;">{key}: {val}</p>'

    # 16. Research & Scientific Work
    fields = {
        'research_programs': row['business_research_research_programs'],
        'research_projects': row['business_research_research_projects'],
        'publications': row['business_research_publications'],
        'patents': row['business_research_patents'],
        'university_partnerships': row['business_research_university_partnerships'],
        'clinical_trials': row['business_research_clinical_trials'],
        'ethnobotanical_research': row['business_research_ethnobotanical_research'],
        'pharmacognosy': row['business_research_pharmacognosy'],
        'phytochemistry': row['business_research_phytochemistry'],
        'plant_breeding': row['business_research_plant_breeding'],
    }
    html_article += f'<h2>Research and Scientific Work</h2>'
    for key, val in fields.items():
        if val != None:
            html_article += f'<p>{key}: {val}</p>'
        else:
            html_article += f'<p style="color: red;">{key}: {val}</p>'

    # 17. Education & Training
    fields = {
        'courses': row['business_education_courses'],
        'workshops': row['business_education_workshops'],
        'webinars': row['business_education_webinars'],
        'apprenticeships': row['business_education_apprenticeships'],
        'lectures': row['business_education_lectures'],
        'botanical_walks': row['business_education_botanical_walks'],
        'farm_tours': row['business_education_farm_tours'],
        'certifications_offered': row['business_education_certifications_offered'],
    }
    html_article += f'<h2>Education and Training</h2>'
    for key, val in fields.items():
        if val != None:
            html_article += f'<p>{key}: {val}</p>'
        else:
            html_article += f'<p style="color: red;">{key}: {val}</p>'

    # 18. Traditional Medicine & Therapeutic Systems
    fields = {
        'ayurveda': row['business_traditional_medicine_systems_ayurveda'],
        'traditional_chinese_medicine': row['business_traditional_medicine_systems_traditional_chinese_medicine'],
        'western_herbalism': row['business_traditional_medicine_systems_western_herbalism'],
        'unani': row['business_traditional_medicine_systems_unani'],
        'kampo': row['business_traditional_medicine_systems_kampo'],
        'tibetan_medicine': row['business_traditional_medicine_systems_tibetan_medicine'],
        'indigenous_medicine': row['business_traditional_medicine_systems_indigenous_medicine'],
        'african_traditional_medicine': row['business_traditional_medicine_systems_african_traditional_medicine'],
    }
    html_article += f'<h2>Traditional Medicine and Therapeutic Systems</h2>'
    for key, val in fields.items():
        if val != None:
            html_article += f'<p>{key}: {val}</p>'
        else:
            html_article += f'<p style="color: red;">{key}: {val}</p>'

    # 19. Expertise
    fields = {
        'expertise_topics': row['business_expertise_expertise_topics'],
        'medicinal_plant_cultivation': row['business_expertise_medicinal_plant_cultivation'],
        'herbal_formulation': row['business_expertise_herbal_formulation'],
        'ethnobotany': row['business_expertise_ethnobotany'],
        'pharmacognosy': row['business_expertise_pharmacognosy'],
        'botanical_identification': row['business_expertise_botanical_identification'],
        'herbal_medicine': row['business_expertise_herbal_medicine'],
        'conservation': row['business_expertise_conservation'],
        'plant_propagation': row['business_expertise_plant_propagation'],
    }
    html_article += f'<h2>Expertise</h2>'
    for key, val in fields.items():
        if val != None:
            html_article += f'<p>{key}: {val}</p>'
        else:
            html_article += f'<p style="color: red;">{key}: {val}</p>'

    # 20. People & Leadership
    fields = {
        'founders': row['business_people_founders'],
        'owners': row['business_people_owners'],
        'ceo': row['business_people_ceo'],
        'president': row['business_people_president'],
        'director': row['business_people_director'],
        'botanists': row['business_people_botanists'],
        'herbalists': row['business_people_herbalists'],
        'researchers': row['business_people_researchers'],
        'agronomists': row['business_people_agronomists'],
        'pharmacists': row['business_people_pharmacists'],
        'educators': row['business_people_educators'],
        'laboratory_directors': row['business_people_laboratory_directors'],
        'farm_managers': row['business_people_farm_managers'],
    }
    html_article += f'<h2>People and Leadership</h2>'
    for key, val in fields.items():
        if val != None:
            html_article += f'<p>{key}: {val}</p>'
        else:
            html_article += f'<p style="color: red;">{key}: {val}</p>'

    # 21. Markets & Customers
    fields = {
        'customer_types': row['business_markets_customer_types'],
        'industries_served': row['business_markets_industries_served'],
        'countries_served': row['business_markets_countries_served'],
        'regions_served': row['business_markets_regions_served'],
        'export_markets': row['business_markets_export_markets'],
        'import_markets': row['business_markets_import_markets'],
    }
    html_article += f'<h2>Markets and Customers</h2>'
    for key, val in fields.items():
        if val != None:
            html_article += f'<p>{key}: {val}</p>'
        else:
            html_article += f'<p style="color: red;">{key}: {val}</p>'

    # 22. Wholesale & Commercial Availability
    fields = {
        'international_shipping': row['business_markets_international_shipping'],
        'wholesale_available': row['business_markets_wholesale_available'],
        'retail_available': row['business_markets_retail_available'],
        'private_label_available': row['business_markets_private_label_available'],
    }
    html_article += f'<h2>Wholesale and Commercial Availability</h2>'
    for key, val in fields.items():
        if val != None:
            html_article += f'<p>{key}: {val}</p>'
        else:
            html_article += f'<p style="color: red;">{key}: {val}</p>'

    # 23. E-commerce & Payments
    fields = {
        'online_store': row['business_commerce_online_store'],
        'ecommerce': row['business_commerce_ecommerce'],
        'accepted_payment_methods': row['business_commerce_accepted_payment_methods'],
        'currencies': row['business_commerce_currencies'],
    }
    html_article += f'<h2>E-commerce and Payments</h2>'
    for key, val in fields.items():
        if val != None:
            html_article += f'<p>{key}: {val}</p>'
        else:
            html_article += f'<p style="color: red;">{key}: {val}</p>'

    # 24. Shipping & Delivery
    fields = {
        'shipping_countries': row['business_shipping_shipping_countries'],
        'shipping_methods': row['business_shipping_shipping_methods'],
        'international_shipping': row['business_shipping_international_shipping'],
        'local_delivery': row['business_shipping_local_delivery'],
    }
    html_article += f'<h2>Shipping and Delivery</h2>'
    for key, val in fields.items():
        if val != None:
            html_article += f'<p>{key}: {val}</p>'
        else:
            html_article += f'<p style="color: red;">{key}: {val}</p>'

    # 25. Awards & Recognition
    fields = {
        'awards': row['business_awards_awards'],
        'award_name': row['business_awards_award_name'],
        'award_year': row['business_awards_award_year'],
        'awarding_organization': row['business_awards_awarding_organization'],
    }
    html_article += f'<h2>Awards and Recognition</h2>'
    for key, val in fields.items():
        if val != None:
            html_article += f'<p>{key}: {val}</p>'
        else:
            html_article += f'<p style="color: red;">{key}: {val}</p>'

    # 26. Professional & Industry Affiliations
    fields = {
        'professional_associations': row['business_memberships_professional_associations'],
        'industry_memberships': row['business_memberships_industry_memberships'],
        'botanical_societies': row['business_memberships_botanical_societies'],
        'herbal_associations': row['business_memberships_herbal_associations'],
    }
    html_article += f'<h2>Professional and Industry Affiliations</h2>'
    for key, val in fields.items():
        if val != None:
            html_article += f'<p>{key}: {val}</p>'
        else:
            html_article += f'<p style="color: red;">{key}: {val}</p>'

    # 27. Social & Online Presence
    fields = {
        'facebook': row['business_online_presence_facebook'],
        'instagram': row['business_online_presence_instagram'],
        'linkedin': row['business_online_presence_linkedin'],
        'youtube': row['business_online_presence_youtube'],
        'x': row['business_online_presence_x'],
        'pinterest': row['business_online_presence_pinterest'],
        'tiktok': row['business_online_presence_tiktok'],
        'github': row['business_online_presence_github'],
        'wikipedia': row['business_online_presence_wikipedia'],
    }
    html_article += f'<h2>Social and Online Presence</h2>'
    for key, val in fields.items():
        if val != None:
            html_article += f'<p>{key}: {val}</p>'
        else:
            html_article += f'<p style="color: red;">{key}: {val}</p>'

    # 28. Policies
    fields = {
        'privacy_policy': row['business_policies_privacy_policy'],
        'shipping_policy': row['business_policies_shipping_policy'],
        'returns_policy': row['business_policies_returns_policy'],
        'refund_policy': row['business_policies_refund_policy'],
        'sustainability_policy': row['business_policies_sustainability_policy'],
        'accessibility_policy': row['business_policies_accessibility_policy'],
    }
    html_article += f'<h2>Policies</h2>'
    for key, val in fields.items():
        if val != None:
            html_article += f'<p>{key}: {val}</p>'
        else:
            html_article += f'<p style="color: red;">{key}: {val}</p>'

    # 29. Language & Customer Support
    fields = {
        'languages': row['business_languages_languages'],
        'multilingual_support': row['business_languages_multilingual_support'],
        'customer service email': row['business_email_customer_service'],
        'wholesale email': row['business_email_wholesale'],
        'media email': row['business_email_media'],
    }
    html_article += f'<h2>Language and Customer Support</h2>'
    for key, val in fields.items():
        if val != None:
            html_article += f'<p>{key}: {val}</p>'
        else:
            html_article += f'<p style="color: red;">{key}: {val}</p>'

    # 30. Contact
    fields = {
        'website': row['business_website'],
        'email': row['business_email'],
        'phone': row['business_phone'],
        'whatsapp': row['business_whatsapp'],
        'fax': row['business_fax'],
        'contact form': row['business_contact_form'],
    }
    html_article += f'<h2>Contact</h2>'
    for key, val in fields.items():
        if val != None:
            html_article += f'<p>{key}: {val}</p>'
        else:
            html_article += f'<p style="color: red;">{key}: {val}</p>'

    '''


    '''
    html_article += f'<h2>ALL</h2>'
    for key, val in items.items():
        # pass
        # if val != None:
            html_article += f'<p>{key}: {val}</p>'
    '''



    meta_title = f'{business_name_canonical}'
    meta_description = f''
    canonical_html = f'''<link rel="canonical" href="https://terrawhisper.com/{url_slug}.html">'''
    head_html = components.html_head(
        meta_title, meta_description, css='/styles.css', canonical=canonical_html
    )

    html = f''' 
        <!DOCTYPE html>
        <html lang="en">
        {head_html}
        <body>
            {sections.header_dark()}
            <main class="container-md listing" style="margin-top: 4.8rem;">
                {html_article}
            </main>
            {sections.footer()}
        </body>
        </html>
    '''.strip()
    html_filepath = f'{g.website_folderpath}/{url_slug}.html'
    with open(html_filepath, 'w') as f: f.write(html)
    print(html_filepath)


def gen_old():
    print(f'ORGANIZATIONS >> RENDER >> ALL')

    input_foldername = f'{g.DATA_FOLDERPATH}/organizations/fetch/gmap/america/places'.replace(' ', '_')
    input_filenames = sorted(os.listdir(input_foldername))
    for input_filename in input_filenames[:10]:
        input_filepath = f'{input_foldername}/{input_filename}'
        with open(input_filepath, encoding="utf-8") as f: rows = f.read().strip().split('\n')
        for row in rows:
            values = row.split('~')
            print(values)
            if values != [] and values != ['']:
                label = values[0]
                address = values[1]
                website = values[2]
                phone = values[3]
                name = values[4]
                info = values[5]
                slug = to_slug(label)
                print(f'label: {label}')
                print(f'address: {address}')
                print(f'website: {website}')
                print(f'phone: {phone}')
                print(f'name: {name}')
                print(f'info: {info}')
                print(f'slug: {slug}')
                print(f'***************************************')
                print()
                print(info)

                lst = ast.literal_eval(info)
                if 'Erborista' in lst:
                    # print('found')
                    slug = to_slug(label)
                    # print(slug)
                    render_listing(name, slug)
                    quit()

    quit()
    filepath = "/home/ubuntu/vault/terrawhisper/data/organizations/fetch/usda_organic/INTEGRITY_Export_20260701.csv"
    items = io.csv_to_dict(filepath, delimiter=',')
    # print(json.dumps(items[0], indent=4))
    # print(json.dumps(items[1], indent=4))
    # print(json.dumps(items[2], indent=4))
    for record in items[2:]:
        # print(json.dumps(item, indent=4))
        types = classify_usda_operation(record)
        domain = classify_product_domain(record)
        # print(domain, types)
        # print(record.get("CR_CertifiedProducts", ""))
        # print(record.get("LS_CertifiedProducts", ""))
        # print(record.get("WC_CertifiedProducts", ""))
        # print(record.get("Han_CertifiedProducts", ""))
        if domain == "PLANT":
            print()
            print(domain, types)
            print(record.get("CR_CertifiedProducts", ""))
            print(record.get("LS_CertifiedProducts", ""))
            print(record.get("WC_CertifiedProducts", ""))
            print(record.get("Han_CertifiedProducts", ""))
            quit()
        continue
        ###
        op_name = item['op_name']
        print(op_name)
        result = normalize_entity(op_name)
        herb_business = herb_relevance(item)
        if herb_business['herb_matches'] != []:
            print(herb_relevance(item))
            print(result)
    quit()

    with open(filepath, encoding="utf-8", newline="") as f:
        for row in csv.reader(f):
            print(row, flush=True)
            quit()
            render_listing(name, slug)

def run():
    print(f'ORGANIZATIONS >> RENDER >> ALL')

    master_items = masterize_organizations_utils.masterize_organizations_get_all()
    for master_item in master_items[:]:
        # print(json.dumps(master_item, indent=4))
        render_listing(master_item)

