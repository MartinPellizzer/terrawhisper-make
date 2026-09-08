import os
import re
import csv
import ast
import json
import shutil
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

shutil.copy2('styles.css', f'{g.website_folderpath}/styles.css')

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

def section_reviews_gen(input_data, identity_gmap_item):
    output_html = ''
    reviews_data = input_data['reviews']
    ### HTML REVIEWS
    html_reviews = f''''''
    for lst in reviews_data:
        for item in lst['items']:
            if item['source_name'] == 'Google Maps':
                # print(json.dumps(item, indent=4))
                review_author_name = item['fields']['business_review_author_name']
                review_text = item['fields']['business_review_text_eng']
                review_stars = item['fields']['business_review_stars']
                if review_stars == '5':
                    review_stars = '★★★★★'
                elif review_stars == '4':
                    review_stars = '★★★★☆'
                elif review_stars == '3':
                    review_stars = '★★★☆☆'
                elif review_stars == '2':
                    review_stars = '★★☆☆☆'
                elif review_stars == '1':
                    review_stars = '★☆☆☆☆'
                html_review = f'''
                    <div class="stars-small">
                        <span>{review_stars}</span>
                    </div>
                    <p class="review-text">
                        {review_text}
                    </p>
                    <div class="review-name">
                        <span>{review_author_name}</span>
                    </div>
                    <div class="review-divider"></div>
                '''
                html_reviews += html_review
    ### HTML OUTPUT
    rating = identity_gmap_item['fields']['business_rating']
    reviews_num = identity_gmap_item['fields']['business_reviews_num']
    if rating != None and reviews_num != None: 
        rating = rating.replace(',', '.')
        reviews_num = reviews_num.replace('(', '').replace(')', '')
        if float(rating) < 1.5:
            review_stars = '★☆☆☆☆'
        elif float(rating) < 2.5:
            review_stars = '★★☆☆☆'
        elif float(rating) < 3.5:
            review_stars = '★★★☆☆'
        elif float(rating) < 4.5:
            review_stars = '★★★★☆'
        elif float(rating) <= 5:
            review_stars = f'''★★★★★'''
        output_html += f'''
            <section class="organization-listing">
                <h2>
                    Customer Reviews
                </h2>
                <div class="rating">
                    <div class="stars-big">
                        <span>{review_stars}</span>
                    </div>
                    <span class="rating-text">
                        {rating} out of 5 · {reviews_num} reviews
                    </span>
                </div>
                <div>
                    {html_reviews}
                </div>
            </section>
        '''
    return output_html

def section_products_gen(input_data):
    html = ''
    text = None
    ### GET DATA
    for lst in input_data['identity']:
        for item in lst['items']:
            if item['source_name'] == 'Website':
                business_products_herbs = item['fields']['business_products_herbs']
                business_products = item['fields']['business_products']
                business_products_categories = item['fields']['business_products_categories']
                business_products_flagship = item['fields']['business_products_flagship']
                business_products_forms = item['fields']['business_products_forms']
    ### GEN HTML
    if business_products_herbs != None: html += f'''<p>business_products_herbs: {business_products_herbs}</p>'''
    if business_products != None: html += f'''<p>business_products: {business_products}</p>'''
    if business_products_categories != None: html += f'''<p>business_products_categories: {business_products_categories}</p>'''
    if business_products_flagship != None: html += f'''<p>business_products_flagship: {business_products_flagship}</p>'''
    if business_products_forms != None: html += f'''<p>business_products_forms: {business_products_forms}</p>'''
    html = f'''
        <section>
            <h2>Products</h2>
            <p style="margin-bottom: 1.6rem;">{input_data['identity'][0]['llm_products']}</p>
        </section>
    '''
            # {html}
    return html

def section_services_gen(input_data):
    html = ''
    text = None
    ### GET DATA
    for lst in input_data['identity']:
        for item in lst['items']:
            if item['source_name'] == 'Website':
                business_herbal_consultation = item['fields']['business_herbal_consultation']
                business_herbal_clinic = item['fields']['business_herbal_clinic']
                business_medicinal_plant_consulting = item['fields']['business_medicinal_plant_consulting']
                business_plant_identification = item['fields']['business_plant_identification']
                business_botanical_identification = item['fields']['business_botanical_identification']
                business_cultivation_consulting = item['fields']['business_cultivation_consulting']
                business_contract_growing = item['fields']['business_contract_growing']
                business_contract_manufacturing = item['fields']['business_contract_manufacturing']
                business_private_label_manufacturing = item['fields']['business_private_label_manufacturing']
                business_extraction_services = item['fields']['business_extraction_services']
                business_drying_services = item['fields']['business_drying_services']
                business_milling = item['fields']['business_milling']
                business_grinding = item['fields']['business_grinding']
                business_packaging_service = item['fields']['business_packaging_service']
                business_export_services = item['fields']['business_export_services']
                business_laboratory_testing = item['fields']['business_laboratory_testing']
                business_formulation = item['fields']['business_formulation']
                business_research_services = item['fields']['business_research_services']
                business_education = item['fields']['business_education']
                business_workshops = item['fields']['business_workshops']
                business_courses = item['fields']['business_courses']
                business_farm_tours = item['fields']['business_farm_tours']
                business_botanical_tours = item['fields']['business_botanical_tours']
    ### GEN HTML
    if business_herbal_consultation != None: html += f'''<p>:business_herbal_consultation {business_herbal_consultation}</p>'''
    if business_herbal_clinic != None: html += f'''<p>business_herbal_clinic: {business_herbal_clinic}</p>'''
    if business_medicinal_plant_consulting != None: html += f'''<p>business_medicinal_plant_consulting: {business_medicinal_plant_consulting}</p>'''
    if business_plant_identification != None: html += f'''<p>business_plant_identification: {business_plant_identification}</p>'''
    if business_botanical_identification != None: html += f'''<p>business_botanical_identification: {business_botanical_identification}</p>'''
    if business_cultivation_consulting != None: html += f'''<p>business_cultivation_consulting: {business_cultivation_consulting}</p>'''
    if business_contract_growing != None: html += f'''<p>business_contract_growing: {business_contract_growing}</p>'''
    if business_contract_manufacturing != None: html += f'''<p>business_contract_manufacturing: {business_contract_manufacturing}</p>'''
    if business_private_label_manufacturing != None: html += f'''<p>business_private_label_manufacturing: {business_private_label_manufacturing}</p>'''
    if business_extraction_services != None: html += f'''<p>business_extraction_services: {business_extraction_services}</p>'''
    if business_drying_services != None: html += f'''<p>business_drying_services: {business_drying_services}</p>'''
    if business_milling != None: html += f'''<p>business_milling: {business_milling}</p>'''
    if business_grinding != None: html += f'''<p>business_grinding: {business_grinding}</p>'''
    if business_packaging_service != None: html += f'''<p>business_packaging_service: {business_packaging_service}</p>'''
    if business_export_services != None: html += f'''<p>business_export_services: {business_export_services}</p>'''
    if business_laboratory_testing != None: html += f'''<p>business_laboratory_testing: {business_laboratory_testing}</p>'''
    if business_formulation != None: html += f'''<p>business_formulation: {business_formulation}</p>'''
    if business_research_services != None: html += f'''<p>business_research_services: {business_research_services}</p>'''
    if business_education != None: html += f'''<p>business_education: {business_education}</p>'''
    if business_workshops != None: html += f'''<p>business_workshops: {business_workshops}</p>'''
    if business_courses != None: html += f'''<p>business_courses: {business_courses}</p>'''
    if business_farm_tours != None: html += f'''<p>business_farm_tours: {business_farm_tours}</p>'''
    if business_botanical_tours != None: html += f'''<p>: {business_botanical_tours}</p>'''
    html = f'''
        <section>
            <h2>Services</h2>
            <p style="margin-bottom: 1.6rem;">{input_data['identity'][0]['llm_services']}</p>
        </section>
    '''
            # {html}
    return html

def section_contacts_gen(input_data, identity_gmap_item):
    iframe_html = identity_gmap_item['fields']['business_map']
    iframe_html = re.sub(r'\s(?:width|height)="[^"]*"', '', iframe_html)
    address_html = ''
    address_text = identity_gmap_item['fields']['business_address']
    if address_text != '':
        address_html = f'''
            <div>
                <h3>Address</h3>
                <p>{address_text}</p>
            </div>
        '''
    output_html = f'''
        <section class="contacts">
            <h2>
                Contacts
            </h2>
            {iframe_html}
            {address_html}
            <div>
                <h3>Get in touch</h3>
                <div style="display: flex; items-align: center; gap: 1.2rem; margin-bottom: 2.4rem;">
                    <svg style="width: 2.0rem;" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-phone-icon lucide-phone"><path d="M13.832 16.568a1 1 0 0 0 1.213-.303l.355-.465A2 2 0 0 1 17 15h3a2 2 0 0 1 2 2v3a2 2 0 0 1-2 2A18 18 0 0 1 2 4a2 2 0 0 1 2-2h3a2 2 0 0 1 2 2v3a2 2 0 0 1-.8 1.6l-.468.351a1 1 0 0 0-.292 1.233 14 14 0 0 0 6.392 6.384"/></svg>
                    <span>{identity_gmap_item['fields']['business_phone']}</span>
                </div>
                <div style="display: flex; items-align: center; gap: 1.2rem; margin-bottom: 2.4rem;">
                    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-globe-icon lucide-globe"><circle cx="12" cy="12" r="10"/><path d="M12 2a14.5 14.5 0 0 0 0 20 14.5 14.5 0 0 0 0-20"/><path d="M2 12h20"/></svg>
                    <span>{identity_gmap_item['fields']['business_website']}</span>
                </div>
            </div>
        </section>
    '''
    return output_html

def section_identity_gen(input_data):
    # print(json.dumps(input_data['identity'], indent=4))
    # quit()
    ### INTRO TEXT
    html = ''
    text = None
    ### GET DATA
    for lst in input_data['identity']:
        for item in lst['items']:
            if item['source_name'] == 'Website':
                business_name_official = item['fields']['business_name_official']
                business_name_legal = item['fields']['business_name_legal']
                business_name_trade = item['fields']['business_name_trade']
                business_company_type = item['fields']['business_company_type']
                business_ownership_type = item['fields']['business_ownership_type']
                business_slogan = item['fields']['business_slogan']
                business_description = item['fields']['business_description']
                business_type_primary = item['fields']['business_type_primary']
                business_type_secondary = item['fields']['business_type_secondary']
                business_industry = item['fields']['business_industry']
                business_niche = item['fields']['business_niche']
                business_model = item['fields']['business_model']
                business_status = item['fields']['business_status']
                business_founding_year = item['fields']['business_founding_year']
                business_founding_story = item['fields']['business_founding_story']
                business_founder_names = item['fields']['business_founder_names']
                business_mission = item['fields']['business_mission']
                business_vision = item['fields']['business_vision']
                business_core_values = item['fields']['business_core_values']
    ### GEN HTML
    html_intro = ''
    html_quick_facts = f''
    html_identity = f''

    if business_description != None:
            # <p style="padding-bottom: 1.6rem; margin-bottom: 1.6rem; border-bottom: 1px solid #e5e5e5;">
        html_intro += f'''
            <p style="margin-bottom: 1.6rem;">
                {business_description}
            </p>
        '''

    border_spacing = '3.2rem;'
    html_quick_facts += f'<dl class="quick-facts" style="padding-bottom: {border_spacing}; margin-bottom: {border_spacing}; border-bottom: 1px solid #e5e5e5;">'
    if business_name_official != None:
        html_quick_facts += f'''<div><dt>Official Name</dt> <dd>{business_name_official}</dd></div>'''
    if business_company_type != None:
        html_quick_facts += f'''<div><dt>Company type:</dt> <dd>{business_company_type}</dd></div>'''
    if business_ownership_type != None:
        html_quick_facts += f'''<div><dt>Ownership type:</dt> <dd>{business_ownership_type}</dd></div>'''
    if business_type_primary != None:
        html_quick_facts += f'''<div><dt>Primary business type</dt> <dd>{business_type_primary}</dd></div>'''
    if business_type_secondary != None:
        html_quick_facts += f'''<div><dt>Secondary business type</dt> <dd>{business_type_secondary}</dd></div>'''
    if business_industry != None:
        html_quick_facts += f'''<div><dt>Business industry</dt> <dd>{business_industry}</dd></div>'''
    if business_niche != None:
        html_quick_facts += f'''<div><dt>Business niche</dt> <dd>{business_niche}</dd></div>'''
    if business_model != None:
        html_quick_facts += f'''<div><dt>Business model</dt> <dd>{business_model}</dd></div>'''
    if business_status != None:
        html_quick_facts += f'''<div><dt>Business status</dt> <dd>{business_status}</dd></div>'''
    html_quick_facts += f'</dl>'

    # html_identity += f'<dl class="quick-facts" style="display: flex; flex-direction: column; gap: 1.6rem; padding-bottom: {border_spacing}; margin-bottom: {border_spacing}; border-bottom: 1px solid #e5e5e5;">'
    html_identity += f'<dl class="quick-facts" style="display: flex; flex-direction: column; gap: 1.6rem; margin-bottom: 4.8rem;">'
    if business_core_values != None:
        html_identity += f'''<div><dt>Core values</dt> <dd>{business_core_values}</dd></div>'''
    if business_mission != None:
        html_identity += f'''<div><dt>Mission</dt> <dd>{business_mission}</dd></div>'''
    if business_vision != None:
        html_identity += f'''<div><dt>Vision</dt> <dd>{business_vision}</dd></div>'''
    if business_founding_year != None:
        html_identity += f'''<div><dt>Founding year</dt> <dd>{business_founding_year}</dd></div>'''
    if business_founding_story != None:
        html_identity += f'''<div><dt>Founding story</dt> <dd>{business_founding_story}</dd></div>'''
    if business_founder_names != None:
        html_identity += f'''<div><dt>Founder names</dt> <dd>{business_founder_names}</dd></div>'''
    html_identity += f'</dl>'
    """
    if business_name_legal != None:
        html += f'''<p>name_legal: {business_name_legal}</p>'''
    if business_name_trade != None:
        html += f'''<p>name_trade: {business_name_trade}</p>'''
    if business_slogan != None:
        html += f'''<p>Slogan: {business_slogan}</p>'''

    """
    # print(json.dumps(item, indent=4))
    # quit()
    if html_intro != '':
        html += f'''
            {html_intro}
        '''
    if html_quick_facts != '':
        html += f'''
            {html_quick_facts}
        '''
        '''
            <h2>
                Quick Facts
            </h2>
        '''
    if html_identity != '':
        html += f'''
            <h2>
                About this business
            </h2>
            {html_identity}
        '''

    return html

def section_location_gen(input_data):
    html = ''
    text = None
    ### GET DATA
    for lst in input_data['identity']:
        for item in lst['items']:
            if item['source_name'] == 'Website':
                business_headquarters = item['fields']['business_headquarters']
                business_city = item['fields']['business_city']
                business_state = item['fields']['business_state']
                business_region = item['fields']['business_region']
                business_country = item['fields']['business_country']
                business_postal_code = item['fields']['business_postal_code']
                business_latitude = item['fields']['business_latitude']
                business_longitude = item['fields']['business_longitude']
                business_additional_locations = item['fields']['business_additional_locations']
                business_farm_locations = item['fields']['business_farm_locations']
                business_nursery_locations = item['fields']['business_nursery_locations']
                business_factory_locations = item['fields']['business_factory_locations']
                business_laboratory_locations = item['fields']['business_laboratory_locations']
                business_warehouse_locations = item['fields']['business_warehouse_locations']
                business_retail_locations = item['fields']['business_retail_locations']
            if item['source_name'] == 'Google Maps':
                business_address = item['fields']['business_address']
    ### GEN HTML
    html += f'<dl class="quick-facts" style="margin-bottom: 4.8rem;">'
    if business_address != None: html += f'''<div style="margin-bottom: 1.6rem;">
<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-map-pin-house"><path d="M15 22a1 1 0 0 1-1-1v-4a1 1 0 0 1 .445-.832l3-2a1 1 0 0 1 1.11 0l3 2A1 1 0 0 1 22 17v4a1 1 0 0 1-1 1z"/><path d="M18 10a8 8 0 0 0-16 0c0 4.993 5.539 10.193 7.399 11.799a1 1 0 0 0 .601.2"/><path d="M18 22v-3"/><circle cx="10" cy="10" r="3"/></svg>
        <dt>Full address</dt> <dd>{business_address}</dd>
        </div>
    '''
    if business_headquarters != None:
        html += f'''<div><dt>Headquarters</dt> <dd>{business_headquarters}</dd></div>'''
    if business_city != None: 
        html += f'''<div><dt>City</dt> <dd>{business_city}</dd></div>'''
    if business_state != None: 
        html += f'''<div><dt>State</dt> <dd>{business_state}</dd></div>'''
    # if business_region != None: 
        # html += f'''<div><dt>Region</dt> <dd>{business_region}</dd></div>'''
    if business_country != None: 
        html += f'''<div><dt>Country</dt> <dd>{business_country}</dd></div>'''
    if business_postal_code != None: 
        html += f'''<div><dt>Postal code</dt> <dd>{business_postal_code}</dd></div>'''
    if business_latitude != None: 
        html += f'''<div><dt>Latitude</dt> <dd>{business_latitude}</dd></div>'''
    if business_longitude != None: 
        html += f'''<div><dt>Longitude</dt> <dd>{business_longitude}</dd></div>'''
    if business_additional_locations != None: 
        html += f'''<div><dt>Additional locations</dt> <dd>{business_additional_locations}</dd></div>'''
    if business_farm_locations != None: 
        html += f'''<div><dt>Farm locations</dt> <dd>{business_farm_locations}</dd></div>'''
    if business_nursery_locations != None: 
        html += f'''<div><dt>Nursery locations</dt> <dd>{business_nursery_locations}</dd></div>'''
    if business_factory_locations != None: 
        html += f'''<div><dt>Factory locations</dt> <dd>{business_factory_locations}</dd></div>'''
    if business_laboratory_locations != None: 
        html += f'''<div><dt>Laboratory locations</dt> <dd>{business_laboratory_locations}</dd></div>'''
    if business_warehouse_locations != None: 
        html += f'''<div><dt>Warehouse locations</dt> <dd>{business_warehouse_locations}</dd></div>'''
    if business_retail_locations != None: 
        html += f'''<div><dt>Retail locations</dt> <dd>{business_retail_locations}</dd></div>'''
    html += f'</dl>'
    print(json.dumps(input_data, indent=4))
    html = f'''
        <section>
            <h2>Location</h2>
            <p style="margin-bottom: 1.6rem;">{input_data['identity'][0]['llm_location']}</p>
            {html}
        </section>
    '''
    return html

def section_visitor_gen(input_data):
    html = ''
    text = None
    ### GET DATA
    for lst in input_data['identity']:
        for item in lst['items']:
            if item['source_name'] == 'Website':
                business_opening_hours = item['fields']['business_opening_hours']
                business_seasonal_hours = item['fields']['business_seasonal_hours']
                business_appointment_required = item['fields']['business_appointment_required']
                business_walk_in_available = item['fields']['business_walk_in_available']
                business_visitor_access = item['fields']['business_visitor_access']
    ### GEN HTML
    if business_opening_hours != None: html += f'''<p>opening_hours: {business_opening_hours}</p>'''
    if business_seasonal_hours != None: html += f'''<p>business_seasonal_hours: {business_seasonal_hours}</p>'''
    if business_appointment_required != None: html += f'''<p>business_appointment_required: {business_appointment_required}</p>'''
    if business_walk_in_available != None: html += f'''<p>business_walk_in_available: {business_walk_in_available}</p>'''
    if business_visitor_access != None: html += f'''<p>business_visitor_access: {business_visitor_access}</p>'''
    html = f'''
        <section>
            <h2>Visitor</h2>
            {html}
        </section>
    '''
    return html

def section_plants_gen(input_data):
    html = ''
    html_plants = ''
    ### HTML REVIEWS
    html_plants += f'''<ul style="list-style: none; display: flex; flex-wrap: wrap; gap: 1.6rem;">'''
    for lst in input_data['herbs']:
        for item in lst['items']:
            if item['source_name'] == 'Website':
                # print(json.dumps(item, indent=4))
                # quit()
                business_herb_name_raw = f'''
                    <li style="border: 1px solid #e5e5e5; padding: 0.4rem 1.2rem;">
                        {item['fields']['business_herb_name_raw']}
                    </li>
                '''
                html_plants += business_herb_name_raw
    html_plants += f'''</ul>'''
    html = f'''
        <section style="margin-bottom: 4.8rem;">
            <h2>Medicinal Plants</h2>
            {html_plants}
        </section>
    '''
    return html

    html = ''
    text = None
    ### GET DATA
    for lst in input_data['identity']:
        for item in lst['items']:
            if item['source_name'] == 'Website':
                business_medicinal_plants = item['fields']['business_medicinal_plants']
                business_primary_medicinal_plants = item['fields']['business_primary_medicinal_plants']
                business_specialty_plants = item['fields']['business_specialty_plants']
                business_native_plants = item['fields']['business_native_plants']
                business_rare_plants = item['fields']['business_rare_plants']
                business_medicinal_plant_categories = item['fields']['business_medicinal_plant_categories']
                business_botanical_collection_size = item['fields']['business_botanical_collection_size']
    ### GEN HTML
    if business_medicinal_plants != None: html += f'''<p>business_medicinal_plants: {business_medicinal_plants}</p>'''
    if business_primary_medicinal_plants != None: html += f'''<p>business_primary_medicinal_plants: {business_primary_medicinal_plants}</p>'''
    if business_specialty_plants != None: html += f'''<p>business_specialty_plants: {business_specialty_plants}</p>'''
    if business_native_plants != None: html += f'''<p>business_native_plants: {business_native_plants}</p>'''
    if business_rare_plants != None: html += f'''<p>business_rare_plants: {business_rare_plants}</p>'''
    if business_medicinal_plant_categories != None: html += f'''<p>business_medicinal_plant_categories: {business_medicinal_plant_categories}</p>'''
    if business_botanical_collection_size != None: html += f'''<p>business_botanical_collection_size: {business_botanical_collection_size}</p>'''
    html = f'''
        <section>
            <h2>Medicinal Plants</h2>
            {html}
        </section>
    '''
    return html

def section_activities_gen(input_data):
    html = ''
    text = None
    ### GET DATA
    for lst in input_data['identity']:
        for item in lst['items']:
            if item['source_name'] == 'Website':
                business_grows = item['fields']['business_grows']
                business_cultivates = item['fields']['business_cultivates']
                business_propagates = item['fields']['business_propagates']
                business_researches = item['fields']['business_researches']
                business_sells = item['fields']['business_sells']
                business_distributes = item['fields']['business_distributes']
                business_exports = item['fields']['business_exports']
                business_imports = item['fields']['business_imports']
                business_wild_harvests = item['fields']['business_wild_harvests']
                business_conserves = item['fields']['business_conserves']
                business_teaches = item['fields']['business_teaches']
                business_uses_in_products = item['fields']['business_uses_in_products']
    ### GEN HTML
    if business_grows != None: html += f'''<p>business_grows: {business_grows}</p>'''
    if business_cultivates != None: html += f'''<p>business_cultivates: {business_cultivates}</p>'''
    if business_propagates != None: html += f'''<p>business_propagates: {business_propagates}</p>'''
    if business_researches != None: html += f'''<p>business_researches: {business_researches}</p>'''
    if business_sells != None: html += f'''<p>business_sells: {business_sells}</p>'''
    if business_distributes != None: html += f'''<p>business_distributes: {business_distributes}</p>'''
    if business_exports != None: html += f'''<p>business_exports: {business_exports}</p>'''
    if business_imports != None: html += f'''<p>business_imports: {business_imports}</p>'''
    if business_wild_harvests != None: html += f'''<p>business_wild_harvests: {business_wild_harvests}</p>'''
    if business_conserves != None: html += f'''<p>business_conserves: {business_conserves}</p>'''
    if business_teaches != None: html += f'''<p>business_teaches: {business_teaches}</p>'''
    if business_uses_in_products != None: html += f'''<p>business_uses_in_products: {business_uses_in_products}</p>'''
    html = f'''
        <section style="margin-bottom: 4.8rem;">
            <h2>Botanical Activities</h2>
            <p style="margin-bottom: 1.6rem;">{input_data['identity'][0]['llm_activities']}</p>
        </section>
    '''
    return html
            # {html}

def render_listing(master_item):
    business_name_canonical = master_item['business_name_canonical']
    business_name_display = master_item['business_name_display']
    business_slug = master_item['business_slug']
    url_slug = f'organizations/{business_slug}'

    input_data = io.json_read(f'{HUB_FOLDERPATH}/compile/{business_name_canonical}.json')

    '''
    for products in input_data['products']:
        for item in products['items']:
            print(item['fields']['business_products_herbs'])
            if item['fields']['business_products_herbs']:
                print(json.dumps(input_data, indent=4))
                print('here')
                quit()
    return
    '''
    # if business_name_canonical != 'blue boy herbs': return
    # print(json.dumps(input_data, indent=4))
    # quit()
    identity_data = input_data['identity']
    
    identity_gmap_item = None
    for identity_list in identity_data:
        for identity_item in identity_list['items']:
            if identity_item['source_name'] == 'Google Maps':
                identity_gmap_item = identity_item

    if identity_gmap_item['fields']['business_type_primary'] == None: return
    if 'erboristeria' not in identity_gmap_item['fields']['business_type_primary'].lower(): return
    if 'stati uniti' not in identity_gmap_item['fields']['business_address'].lower(): return

    identity_gmap_item['fields']['business_type_primary'] = 'Herbal shop'
    identity_gmap_item['fields']['business_address'] = identity_gmap_item['fields']['business_address'].replace('Stati Uniti', 'United States')
    # quit()

    ### SKIP MISSING IDENTITY WEBSITE
    found = False
    for lst in input_data['identity']:
        for item in lst['items']:
            if item['source_name'] == 'Website':
                found = True
    if not found:
        return

    # print(json.dumps(identity_data, indent=4))
    # quit()
    # print(json.dumps(gmap_item, indent=4))
    # quit()

    ################################################################################
    # INTRO
    ################################################################################
    html_article = ''

    hero_html = f'''
        {sections.breadcrumbs_explorer(url_slug)}
        <div style="display: flex; justify-content: space-between;">
            <div>
                <h1>{business_name_display}</h1>
                <span class="badge" style="display: inline-block;">{identity_gmap_item['fields']['business_type_primary']}</span>
            </div>
            <div style="display: flex; flex-direction: column; align-items: center; margin-top: 0.8rem;">
                <span style="display: inline-block;" class="hero-score">4.8 / 5</span>
                <span style="display: inline-block;" class="hero-reviews-num">4 Ratings</span>
            </div>
        </div>
    '''

    html_article += f''


    ################################################################################
    # IDENTITY
    ################################################################################
    html_article += section_identity_gen(input_data)

    ################################################################################
    # LOCATION
    ################################################################################
    html_article += section_location_gen(input_data)

    ################################################################################
    # VISITOR
    ################################################################################
    ### TODO: gen llm
    # html_article += section_visitor_gen(input_data)

    ################################################################################
    # PLANTS
    ################################################################################
    html_article += section_plants_gen(input_data)

    ################################################################################
    # ACTIVITIES
    ################################################################################
    ### TODO: gen llm
    html_article += section_activities_gen(input_data)

    ################################################################################
    # PRODUCTS
    ################################################################################
    ### TODO: gen llm
    html_article += section_products_gen(input_data)

    ################################################################################
    # SERVICES
    ################################################################################
    ### TODO: gen llm
    html_article += section_services_gen(input_data)

    ################################################################################
    # REVIEWS
    ################################################################################
    html_article += section_reviews_gen(input_data, identity_gmap_item)

    ################################################################################
    # CONTACTS (SIDEBAR)
    ################################################################################
    contacts_html = section_contacts_gen(input_data, identity_gmap_item)


    main_html = f'''
    '''

    '''

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
            <div class="container-xl organization-listing">
                <main>
                    {hero_html}
                    <div class="layout">
                        <div>
                            {html_article}
                        </div>
                        <aside>
                            {contacts_html}      
                        </aside>
                    </div>
                </main>
            </div>
            {sections.footer()}
        </body>
        </html>
    '''.strip()
    html_filepath = f'{g.website_folderpath}/{url_slug}.html'
    with open(html_filepath, 'w') as f: f.write(html)
    print(html_filepath)
    # quit()

def explore_category():
    links = f''
    links += f'<ul>'
    master_items = masterize_organizations_utils.masterize_organizations_get_all()
    for master_item in master_items[:]:
        business_name_canonical = master_item['business_name_canonical']
        business_name_display = master_item['business_name_display']
        business_slug = master_item['business_slug']
        url_slug = f'organizations/{business_slug}'
        ###
        input_data = io.json_read(f'{HUB_FOLDERPATH}/compile/{business_name_canonical}.json')
        identity_data = input_data['identity']
        identity_gmap_item = None
        for identity_list in identity_data:
            for identity_item in identity_list['items']:
                if identity_item['source_name'] == 'Google Maps':
                    identity_gmap_item = identity_item
        # if identity_gmap_item['fields']['business_type_primary'] != "Erboristeria": continue
        if identity_gmap_item['fields']['business_type_primary'] == None: continue
        if 'erboristeria' not in identity_gmap_item['fields']['business_type_primary'].lower(): continue
        if 'stati uniti' not in identity_gmap_item['fields']['business_address'].lower(): continue
        ###
        links += f'''<li><a href="/{url_slug}.html">{business_name_display}</a></li>'''
    links += f'</ul>'

    meta_title = f'Organizations'
    meta_description = f''
    canonical_html = f'''<link rel="canonical" href="https://terrawhisper.com/organizations.html">'''
    head_html = components.html_head(
        meta_title, meta_description, css='/styles.css', canonical=canonical_html
    )

    html = f''' 
        <!DOCTYPE html>
        <html lang="en">
        {head_html}
        <body>
            {sections.header_dark()}
            <div class="container-xl organization-listing">
                <main>
                    <div>
                        {links}
                    </div>
                </main>
            </div>
            {sections.footer()}
        </body>
        </html>
    '''.strip()
    html_filepath = f'{g.website_folderpath}/organizations.html'
    with open(html_filepath, 'w') as f: f.write(html)
    print(html_filepath)

def analyze_missing_identity_website(master_items):
    not_found = 0
    for master_item in master_items[:]:
        business_name_canonical = master_item['business_name_canonical']
        input_data = io.json_read(f'{HUB_FOLDERPATH}/compile/{business_name_canonical}.json')
        found = False
        for lst in input_data['identity']:
            for item in lst['items']:
                if item['source_name'] == 'Website':
                    found = True
        if not found:
            not_found += 1
    return not_found

def run():
    print(f'ORGANIZATIONS >> RENDER >> ALL')

    output_folderpath = f'{g.website_folderpath}/organizations'
    try: shutil.rmtree(output_folderpath)
    except: pass
    io.folders_recursive_gen(output_folderpath)
    # print(output_folderpath)
    # quit()

    explore_category()

    master_items = masterize_organizations_utils.masterize_organizations_get_all()
    for master_item in master_items[:]:
        pass
        # print(json.dumps(master_item, indent=4))
        render_listing(master_item)

    print('MISSING IDENTITY WEBSITE:', analyze_missing_identity_website(master_items))

