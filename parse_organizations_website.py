import os
import ast
import time
import json
import shutil

from bs4 import BeautifulSoup

from lib import g
from lib import io
from lib import llm

import parse_utils
import parse_organizations_data

import re
import unicodedata

HUB_FOLDERPATH = f'{g.DATA_FOLDERPATH}/organizations'

model_filepath = '/home/ubuntu/vault-tmp/llm/gemma-4-12b-it-Q4_K_S.gguf'
model_filepath = '/home/ubuntu/vault-tmp/llm/gemma-4-12B-it-qat-UD-Q4_K_XL.gguf'

_NON_ALNUM = re.compile(r"[^\w\s-]", re.UNICODE)
_SEPARATORS = re.compile(r"[-\s]+")

def to_slug(name: str) -> str:
    """Convert an organization name into a stable, URL-safe slug."""
    name = unicodedata.normalize("NFKD", name)
    name = "".join(c for c in name if not unicodedata.combining(c))
    name = name.replace("&", " and ")
    name = _NON_ALNUM.sub("", name)
    return _SEPARATORS.sub("-", name).strip("-").lower()

def llm_gen(query, description, website_text, input_len_max=0):
    if input_len_max != 0:
        website_text = website_text[:input_len_max]
    prompt = f'''
        Extract the {query} from the following text found in the business website.
        By {query} i mean {description}.
        Reply only with the {query}.
        If you can't find the requested info, reply with "NONE".
        WEBSITE TEXT:
        {website_text}
    '''.strip()
    print(f'LEN CHARS: {len(prompt)}')
    print(f'LEN WORDS: {len(prompt.split())}')
    reply = llm.reply(prompt, model_filepath, max_tokens=512)
    if '</think>' in reply:
        reply = reply.split('</think>')[1].strip()
    if 'none' in reply.lower(): reply = None
    print()
    return reply

def llm_bool_gen(query, description, website_text):
    prompt = f'''
        Tell me if this company {query} from the following text found in the business website.
        By {query} i mean {description}.
        Reply only with the "TRUE" or "FALSE".
        If you can't find the requested info, reply with "NONE".
        WEBSITE TEXT:
        {website_text}
    '''.strip()
    reply = llm.reply(prompt, model_filepath, max_tokens=512)
    if '</think>' in reply:
        reply = reply.split('</think>')[1].strip()
    reply = reply.lower()
    if 'none' in reply.lower(): reply = None
    return reply

def parse_website_backup():
    start = 0
    end = 10
    ###
    output_folderpath = f'{g.DATA_FOLDERPATH}/organizations/parse/website/json'
    # try: shutil.rmtree(output_folderpath)
    # except: pass
    io.folders_recursive_gen(output_folderpath)
    ###
    input_foldername = f'{HUB_FOLDERPATH}/fetch/gmap/america/places'.replace(' ', '_')
    input_filenames = sorted(os.listdir(input_foldername))
    i = 0
    for input_filename in input_filenames[start:end]:
        print(f'{start+i}/{end}')
        i += 1
        input_filename_base = input_filename.split('.')[0].strip()
        input_filepath = f'{input_foldername}/{input_filename}'
        with open(input_filepath, encoding="utf-8") as f: rows = f.read().strip().split('\n')
        for row in rows:
            values = row.split('~')
            if values != [] and values != ['']:
                label = values[0]
                name = values[1]
                website = values[2]
                slug = to_slug(label)
                print(f'label: {label}')
                print(f'name: {name}')
                print(f'website: {website}')
                print(f'slug: {slug}')
                print(f'***************************************')
                print()

                llm_business_is_category_herbs  = ''
                print(f'website: {website}')
                print(f'slug: {slug}')
                print(f'***************************************')
                print()

                website_filepath = f'{HUB_FOLDERPATH}/fetch/websites/america/places/{input_filename_base}/{slug}.html'
                output_filepath = f'{output_folderpath}/{slug}.json'
                try: html = io.file_read(website_filepath)
                except: html = ''
                if html != '':
                    soup = BeautifulSoup(html, "html.parser")
                    website_text = soup.get_text(separator="\n", strip=True)
                    if website_text.strip() != '':

                        fields_data = parse_organizations_data.data
                        output_items = []
                        output_item = {}
                        for field_item in fields_data:
                            reply = ''
                            if field_item['field_type'] == 'bool':
                                reply = llm_bool_gen(
                                    query=field_item['field_query'],
                                    description=field_item['field_description'],
                                    website_text=website_text
                                )
                            elif field_item['field_type'] == 'text':
                                reply = llm_gen(
                                    query=field_item['field_query'],
                                    description=field_item['field_description'],
                                    website_text=website_text
                                )

                            key = field_item['field_name']
                            val = reply
                            output_item[key] = val

                        output_items.append(output_item)
                        io.json_write(output_filepath, output_items)
                        ###
                        item = output_items[0]
                        print(output_filepath)
                        none_count = 0
                        empty_count = 0
                        value_count = 0
                        for key, val in item.items():
                            if val == None: none_count += 1
                            elif val == '': empty_count += 1
                            else: value_count += 1
                        total_count = none_count + empty_count + value_count
                        print(f'NONE: {none_count}/{total_count} - {none_count/total_count*100}')
                        print(f'EMPTY: {empty_count}/{total_count} - {empty_count/total_count*100}')
                        print(f'VALUE: {value_count}/{total_count} - {value_count/total_count*100}')
                        ###
                        # quit()

                continue
                llm_business_is_category_herbs  = ''
                ###
                llm_business_name_official = ''
                llm_business_name_legal = ''
                llm_business_name_trade = ''
                llm_business_slogan = ''
                llm_business_description = ''
                llm_business_description_short = ''
                llm_business_founded_year = ''
                llm_business_founding_story = ''
                llm_business_founder_names = ''
                llm_business_ownership_type = ''
                llm_business_company_type = ''
                llm_business_status = ''
                llm_business_mission = ''
                llm_business_vision = ''
                llm_business_core_values = ''
                # 2. Business Classification
                llm_business_type_primary = ''
                llm_business_type_secondary = ''
                llm_business_industry = ''
                llm_business_niche = ''
                llm_business_model = ''
                # 3. Contact Information
                llm_business_website = ''
                llm_business_email = ''
                llm_business_phone = ''
                llm_business_fax = ''
                llm_business_whatsapp = ''
                llm_business_contact_form = ''
                llm_business_customer_service_email = ''
                llm_business_wholesale_email = ''
                llm_business_media_email = ''
                # 4. Locations
                llm_business_headquarters = ''
                llm_business_address = ''
                llm_business_city = ''
                llm_business_state = ''
                llm_business_region = ''
                llm_business_country = ''
                llm_business_postal_code = ''
                llm_business_latitude = ''
                llm_business_longitude = ''
                llm_business_additional_locations = ''
                llm_business_farm_locations = ''
                llm_business_nursery_locations = ''
                llm_business_factory_locations = ''
                llm_business_laboratory_locations = ''
                llm_business_warehouse_locations = ''
                llm_business_retail_locations = ''
                # 5. Opening Information
                llm_business_opening_hours = ''
                llm_business_seasonal_hours = ''
                llm_business_appointment_required = ''
                llm_business_walk_in_available = ''
                llm_business_visitor_access = ''
                llm_business_medicinal_plants = ''
                llm_business_primary_medicinal_plants = ''
                llm_business_specialty_plants = ''
                llm_business_native_plants = ''
                llm_business_rare_plants = ''
                llm_business_medicinal_plant_categories = ''
                llm_business_botanical_collection_size = ''

                llm_business_grows = ''
                llm_business_cultivates = ''
                llm_business_propagates = ''
                llm_business_researches = ''
                llm_business_sells = ''
                llm_business_distributes = ''
                llm_business_exports = ''
                llm_business_imports = ''
                llm_business_wild_harvests = ''
                llm_business_conserves = ''
                llm_business_teaches = ''
                llm_business_uses_in_products = ''

                llm_business_products = ''
                llm_business_product_categories = ''
                llm_business_flagship_products = ''
                llm_business_product_forms = ''
                llm_business_herbal_teas = ''
                llm_business_tinctures = ''
                llm_business_extracts = ''
                llm_business_essential_oils = ''
                llm_business_capsules = ''
                llm_business_powders = ''
                llm_business_dried_herbs = ''
                llm_business_fresh_herbs = ''
                llm_business_seeds = ''
                llm_business_seedlings = ''
                llm_business_roots = ''
                llm_business_bark = ''
                llm_business_flowers = ''
                llm_business_fruits = ''
                llm_business_resins = ''
                llm_business_cosmetics = ''
                llm_business_soaps = ''
                llm_business_creams = ''
                llm_business_salves = ''
                llm_business_syrups = ''

                llm_business_herbal_consultation = ''
                llm_business_herbal_clinic = ''
                llm_business_medicinal_plant_consulting = ''
                llm_business_plant_identification = ''
                llm_business_botanical_identification = ''
                llm_business_cultivation_consulting = ''
                llm_business_contract_growing = ''
                llm_business_contract_manufacturing = ''
                llm_business_private_label_manufacturing = ''
                llm_business_extraction_services = ''
                llm_business_drying_services = ''
                llm_business_milling = ''
                llm_business_grinding = ''
                llm_business_packaging = ''
                llm_business_export_services = ''
                llm_business_laboratory_testing = ''
                llm_business_formulation = ''
                llm_business_research_services = ''
                llm_business_education = ''
                llm_business_workshops = ''
                llm_business_courses = ''
                llm_business_farm_tours = ''
                llm_business_botanical_tours = ''

                llm_business_botanical_name = ''
                llm_business_common_name = ''
                llm_business_plant_part = ''
                llm_business_extraction_method = ''
                llm_business_preparation_method = ''
                llm_business_ingredients = ''
                llm_business_packaging_service = ''
                llm_business_package_sizes = ''
                llm_business_concentration = ''
                llm_business_organic_product = ''
                llm_business_private_label = ''
                llm_business_wholesale = ''
                llm_business_retail = ''

                llm_business_cultivation_methods = ''
                llm_business_organic_cultivation = ''
                llm_business_regenerative = ''
                llm_business_biodynamic = ''
                llm_business_permaculture = ''
                llm_business_agroforestry = ''
                llm_business_greenhouse = ''
                llm_business_indoor = ''
                llm_business_outdoor = ''
                llm_business_wild_harvesting = ''
                llm_business_sustainable_wild_harvesting = ''
                llm_business_propagation_methods = ''
                llm_business_irrigation = ''
                llm_business_fertilization = ''
                llm_business_soil_management = ''
                llm_business_pest_management = ''
                llm_business_harvest_methods = ''
                llm_business_harvest_season = ''

                llm_business_manufacturing = ''
                llm_business_processing = ''
                llm_business_extraction = ''
                llm_business_distillation = ''
                llm_business_fermentation = ''
                llm_business_drying = ''
                llm_business_manufacturing_milling = ''
                llm_business_manufacturing_grinding = ''
                llm_business_blending = ''
                llm_business_manufacturing_formulation = ''
                llm_business_encapsulation = ''
                llm_business_manufacturing_packaging = ''
                llm_business_quality_testing = ''
                llm_business_batch_testing = ''
                llm_business_traceability = ''

                llm_business_facilities_farms = ''
                llm_business_facilities_nurseries = ''
                llm_business_facilities_laboratories = ''
                llm_business_facilities_factories = ''
                llm_business_facilities_warehouses = ''
                llm_business_facilities_botanical_gardens = ''
                llm_business_facilities_greenhouses = ''
                llm_business_facilities_visitor_centers = ''
                llm_business_facilities_research_centers = ''
                llm_business_facilities_education_centers = ''
                llm_business_facilities_clinics = ''
                llm_business_facilities_retail_stores = ''

                llm_business_certifications_certifications = ''
                llm_business_certifications_certification_name = ''
                llm_business_certifications_certification_number = ''
                llm_business_certifications_issuing_organization = ''
                llm_business_certifications_issue_date = ''
                llm_business_certifications_expiry_date = ''
                llm_business_certifications_certification_scope = ''

                llm_business_quality_quality_control = ''
                llm_business_quality_laboratory_testing = ''
                llm_business_quality_batch_testing = ''
                llm_business_quality_third_party_testing = ''
                llm_business_quality_traceability = ''
                llm_business_quality_quality_management_system = ''

                llm_business_sustainability_sustainability_policy = ''
                llm_business_sustainability_conservation = ''
                llm_business_sustainability_biodiversity = ''
                llm_business_sustainability_regenerative_agriculture = ''
                llm_business_sustainability_ethical_sourcing = ''
                llm_business_sustainability_fair_trade = ''
                llm_business_sustainability_community_projects = ''
                llm_business_sustainability_indigenous_partnerships = ''
                llm_business_sustainability_local_sourcing = ''
                llm_business_sustainability_recyclable_packaging = ''
                llm_business_sustainability_carbon_reduction = ''
                llm_business_sustainability_water_conservation = ''

                llm_business_research_research_programs = ''
                llm_business_research_research_projects = ''
                llm_business_research_publications = ''
                llm_business_research_patents = ''
                llm_business_research_university_partnerships = ''
                llm_business_research_clinical_trials = ''
                llm_business_research_ethnobotanical_research = ''
                llm_business_research_pharmacognosy = ''
                llm_business_research_phytochemistry = ''
                llm_business_research_plant_breeding = ''

                llm_business_education_courses = ''
                llm_business_education_workshops = ''
                llm_business_education_webinars = ''
                llm_business_education_apprenticeships = ''
                llm_business_education_lectures = ''
                llm_business_education_botanical_walks = ''
                llm_business_education_farm_tours = ''
                llm_business_education_certifications_offered = ''

                llm_business_traditional_medicine_systems_ayurveda = ''
                llm_business_traditional_medicine_systems_traditional_chinese_medicine = ''
                llm_business_traditional_medicine_systems_western_herbalism = ''
                llm_business_traditional_medicine_systems_unani = ''
                llm_business_traditional_medicine_systems_kampo = ''
                llm_business_traditional_medicine_systems_tibetan_medicine = ''
                llm_business_traditional_medicine_systems_indigenous_medicine = ''
                llm_business_traditional_medicine_systems_african_traditional_medicine = ''

                llm_business_expertise_expertise_topics = ''
                llm_business_expertise_medicinal_plant_cultivation = ''
                llm_business_expertise_herbal_formulation = ''
                llm_business_expertise_ethnobotany = ''
                llm_business_expertise_pharmacognosy = ''
                llm_business_expertise_botanical_identification = ''
                llm_business_expertise_herbal_medicine = ''
                llm_business_expertise_conservation = ''
                llm_business_expertise_plant_propagation = ''

                llm_business_people_founders = ''
                llm_business_people_owners = ''
                llm_business_people_ceo = ''
                llm_business_people_president = ''
                llm_business_people_director = ''
                llm_business_people_botanists = ''
                llm_business_people_herbalists = ''
                llm_business_people_researchers = ''
                llm_business_people_agronomists = ''
                llm_business_people_pharmacists = ''
                llm_business_people_educators = ''
                llm_business_people_laboratory_directors = ''
                llm_business_people_farm_managers = ''

                llm_business_markets_customer_types = ''
                llm_business_markets_industries_served = ''
                llm_business_markets_export_markets = ''
                llm_business_markets_import_markets = ''
                llm_business_markets_countries_served = ''
                llm_business_markets_regions_served = ''
                llm_business_markets_international_shipping = ''
                llm_business_markets_wholesale_available = ''
                llm_business_markets_retail_available = ''
                llm_business_markets_private_label_available = ''

                llm_business_online_presence_facebook = ''
                llm_business_online_presence_instagram = ''
                llm_business_online_presence_linkedin = ''
                llm_business_online_presence_youtube = ''
                llm_business_online_presence_x = ''
                llm_business_online_presence_pinterest = ''
                llm_business_online_presence_tiktok = ''
                llm_business_online_presence_github = ''
                llm_business_online_presence_wikipedia = ''

                llm_business_awards_awards = ''
                llm_business_awards_award_name = ''
                llm_business_awards_award_year = ''
                llm_business_awards_awarding_organization = ''

                llm_business_memberships_professional_associations = ''
                llm_business_memberships_industry_memberships = ''
                llm_business_memberships_botanical_societies = ''
                llm_business_memberships_herbal_associations = ''

                llm_business_policies_privacy_policy = ''
                llm_business_policies_shipping_policy = ''
                llm_business_policies_returns_policy = ''
                llm_business_policies_refund_policy = ''
                llm_business_policies_sustainability_policy = ''
                llm_business_policies_accessibility_policy = ''

                llm_business_languages_languages = ''
                llm_business_languages_multilingual_support = ''

                llm_business_commerce_accepted_payment_methods = ''
                llm_business_commerce_currencies = ''
                llm_business_commerce_online_store = ''
                llm_business_commerce_ecommerce = ''

                llm_business_shipping_shipping_countries = ''
                llm_business_shipping_shipping_methods = ''
                llm_business_shipping_international_shipping = ''
                llm_business_shipping_local_delivery = ''

                ###
                website_filepath = f'{g.DATA_FOLDERPATH}/organizations/fetch/websites/america/places/{input_filename_base}/{slug}.html'
                output_filepath = f'{output_folderpath}/{slug}.json'
                try: html = io.file_read(website_filepath)
                except: html = ''
                if html != '':
                    soup = BeautifulSoup(html, "html.parser")
                    website_text = soup.get_text(separator="\n", strip=True)
                    if website_text.strip() != '':
                        llm_business_is_category_herbs = llm_bool_gen(
                            query='is mainly about medicinal plants', 
                            description='that this business is a seller, grower, user, or anything else related to herbs predominantly as their products and core business', 
                            website_text=website_text
                            )

                        ###
                        llm_business_name_official = llm_gen(
                            query='official business name', 
                            description='Official business name exactly as shown on the website', 
                            website_text=website_text
                            )
                        llm_business_name_legal = llm_gen(
                            query='legal business name', 
                            description='Registered legal business name if published', 
                            website_text=website_text
                            )
                        llm_business_name_trade = llm_gen(
                            query='trading business name', 
                            description='Public trading or DBA name', 
                            website_text=website_text
                            )
                        llm_business_slogan = llm_gen(
                            query='business slogan', 
                            description='Official company slogan or tagline', 
                            website_text=website_text
                            )
                        llm_business_description = llm_gen(
                            query='business description', 
                            description='Main factual description of the company', 
                            website_text=website_text
                            )
                        llm_business_description_short = llm_gen(
                            query='short business description', 
                            description='Short summary (1–2 sentences)', 
                            website_text=website_text
                            )
                        llm_business_founded_year = llm_gen(
                            query='business year founded', 
                            description='Year the business was founded', 
                            website_text=website_text
                            )
                        llm_business_founding_story = llm_gen(
                            query='business founding story', 
                            description='History or origin story', 
                            website_text=website_text
                            )
                        llm_business_founder_names = llm_gen(
                            query='business founder names', 
                            description='Founder(s)', 
                            website_text=website_text
                            )
                        llm_business_ownership_type = llm_gen(
                            query='business ownership type', 
                            description='Private, public, cooperative, nonprofit, family-owned, etc.', 
                            website_text=website_text
                            )
                        llm_business_company_type = llm_gen(
                            query='business company type', 
                            description='LLC, Ltd, Inc., GmbH, Cooperative, etc.', 
                            website_text=website_text
                            )
                        llm_business_status = llm_gen(
                            query='business status', 
                            description='Active, acquired, merged, closed, etc.', 
                            website_text=website_text
                            )
                        llm_business_mission = llm_gen(
                            query='business mission', 
                            description='Mission statement', 
                            website_text=website_text
                            )
                        llm_business_vision = llm_gen(
                            query='business vision', 
                            description='Vision statement', 
                            website_text=website_text
                            )
                        llm_business_core_values = llm_gen(
                            query='business core values', 
                            description='''Company's stated values''', 
                            website_text=website_text
                            )

                        # 2. Business Classification
                        llm_business_type_primary = llm_gen(
                            query='primary business type', 
                            description='''Main business role''', 
                            website_text=website_text
                            )
                        llm_business_type_secondary = llm_gen(
                            query='secondary business type', 
                            description='''Additional business roles''', 
                            website_text=website_text
                            )
                        llm_business_industry = llm_gen(
                            query='business industry', 
                            description='''Industry classification''', 
                            website_text=website_text
                            )
                        llm_business_niche = llm_gen(
                            query='business niche', 
                            description='''Specific medicinal plant niche''', 
                            website_text=website_text
                            )
                        llm_business_model = llm_gen(
                            query='business model', 
                            description='''B2B, B2C, Marketplace, Manufacturer, etc.''', 
                            website_text=website_text
                            )
                        # 3. Contact Information
                        llm_business_website = llm_gen(
                            query='website',
                            description='''The official website URL of the business. Extract the primary canonical domain used by the organization (e.g., https://www.example.com).''',
                            website_text=website_text
                        )
                        llm_business_email = llm_gen(
                            query='email',
                            description='''The primary general-purpose email address for contacting the business (e.g., info@example.com). Exclude personal employee emails unless they are the primary contact.''',
                            website_text=website_text
                        )
                        llm_business_customer_service_email = llm_gen(
                            query='customer service email',
                            description='''The dedicated email address for customer support or customer service inquiries (e.g., support@example.com).''',
                            website_text=website_text
                        )
                        llm_business_wholesale_email = llm_gen(
                            query='wholesale email',
                            description='''The dedicated email address for wholesale, bulk orders, distributors, or B2B sales inquiries (e.g., wholesale@example.com).''',
                            website_text=website_text
                        )
                        llm_business_media_email = llm_gen(
                            query='media email',
                            description='''The dedicated email address for press, media, public relations, or journalist inquiries (e.g., media@example.com or press@example.com).''',
                            website_text=website_text
                        )
                        llm_business_phone = llm_gen(
                            query='phone',
                            description='''The primary business telephone number for customer inquiries. Preserve the international dialing code when available.''',
                            website_text=website_text
                        )
                        llm_business_whatsapp = llm_gen(
                            query='whatsapp',
                            description='''The official WhatsApp contact number or WhatsApp Business link provided for customer communication.''',
                            website_text=website_text
                        )
                        llm_business_fax = llm_gen(
                            query='fax',
                            description='''The official fax number published by the business, if available.''',
                            website_text=website_text
                        )
                        llm_business_contact_form = llm_gen(
                            query='contact form',
                            description='''The URL of the official online contact form where visitors can submit inquiries.''',
                            website_text=website_text
                        )
                        # 4. Locations
                        llm_business_headquarters = llm_gen(
                            query='business headquarters', 
                            description='''The primary headquarters location of the business, including the city and country where the company is officially based.''', 
                            website_text=website_text
                        )
                        llm_business_address = llm_gen(
                            query='business address', 
                            description='''The complete street address of the business's primary location, including building number, street name, and other published address details.''', 
                            website_text=website_text
                        )
                        llm_business_city = llm_gen(
                            query='business city', 
                            description='''The city or municipality where the business or facility is located.''', 
                            website_text=website_text
                        )
                        llm_business_state = llm_gen(
                            query='business state', 
                            description='''The state, province, prefecture, or equivalent first-level administrative division where the business is located.''', 
                            website_text=website_text
                        )
                        llm_business_region = llm_gen(
                            query='business region', 
                            description='''The broader geographic or administrative region (e.g., Tuscany, Bavaria, Queensland) where the business operates.''', 
                            website_text=website_text
                        )
                        llm_business_country = llm_gen(
                            query='business country', 
                            description='''The country where the business's primary location is situated. Store using a standardized country name or ISO country code.''', 
                            website_text=website_text
                        )
                        llm_business_postal_code = llm_gen(
                            query='business postal code', 
                            description='''The postal or ZIP code associated with the business's address.''', 
                            website_text=website_text
                        )
                        llm_business_latitude = llm_gen(
                            query='business latitude', 
                            description='''The latitude coordinate of the published business location, if explicitly available on the website.''', 
                            website_text=website_text
                        )
                        llm_business_longitude = llm_gen(
                            query='business longitude', 
                            description='''The longitude coordinate of the published business location, if explicitly available on the website.''', 
                            website_text=website_text
                        )
                        llm_business_additional_locations = llm_gen(
                            query='business additional locations', 
                            description='''Other business locations, offices, branches, or facilities operated by the company besides its headquarters. Include names and addresses when available.''', 
                            website_text=website_text
                        )
                        llm_business_farm_locations = llm_gen(
                            query='business farm locations', 
                            description='''Locations of farms where the business cultivates, grows, or harvests medicinal plants. Include addresses or geographic areas if provided.''', 
                            website_text=website_text
                        )
                        llm_business_nursery_locations = llm_gen(
                            query='business nursery locations', 
                            description='''Locations of plant nurseries where medicinal plants, seedlings, or seeds are propagated or sold.''', 
                            website_text=website_text
                        )
                        llm_business_factory_locations = llm_gen(
                            query='business factory locations', 
                            description='''Locations of manufacturing or production facilities where medicinal plant products are processed, formulated, packaged, or manufactured.''', 
                            website_text=website_text
                        )
                        llm_business_laboratory_locations = llm_gen(
                            query='business laboratory locations', 
                            description='''Locations of laboratories used for research, quality control, testing, extraction, or scientific analysis.''', 
                            website_text=website_text
                        )
                        llm_business_warehouse_locations = llm_gen(
                            query='business warehouse locations', 
                            description='''Locations of warehouses, storage facilities, fulfillment centers, or distribution centers used by the business.''', 
                            website_text=website_text
                        )
                        llm_business_retail_locations = llm_gen(
                            query='business retail locations', 
                            description='''Physical retail stores, herbal shops, apothecaries, garden centers, or showrooms operated by the business where customers can make purchases.''', 
                            website_text=website_text
                        )
                        # 5. Opening Information
                        llm_business_opening_hours = llm_gen(
                            query='opening_hours',
                            description='''The regular hours during which the business is open to visitors or customers.''',
                            website_text=website_text
                        )
                        llm_business_seasonal_hours = llm_gen(
                            query='seasonal_hours',
                            description='''Any changes to the business opening hours that apply during specific seasons, holidays, or periods of the year.''',
                            website_text=website_text
                        )
                        llm_business_appointment_required = llm_gen(
                            query='appointment_required',
                            description='''Whether visitors or customers are required to make an appointment in advance.''',
                            website_text=website_text
                        )
                        llm_business_walk_in_available = llm_gen(
                            query='walk_in_available',
                            description='''Whether visitors or customers can visit without an appointment or prior booking.''',
                            website_text=website_text
                        )
                        llm_business_visitor_access = llm_gen(
                            query='visitor_access',
                            description='''Information about whether and how visitors can access the business or its premises, including any restrictions or requirements.''',
                            website_text=website_text
                        )
                        # 6. Medicinal Plant Specialization
                        llm_business_medicinal_plants = llm_gen(
                            query='medicinal_plants', 
                            description='''Comprehensive list of medicinal plants, herbs, trees, shrubs, or other botanicals mentioned on the website''', 
                            website_text=website_text
                        )
                        llm_business_primary_medicinal_plants = llm_gen(
                            query='primary_medicinal_plants', 
                            description='''Main medicinal plants that are prominently featured, emphasized, or central to the organization's work or offerings''', 
                            website_text=website_text
                        )
                        llm_business_specialty_plants = llm_gen(
                            query='specialty_plants', 
                            description='''Specialty, flagship, signature, or particularly notable plant species associated with the organization''', 
                            website_text=website_text
                        )
                        llm_business_native_plants = llm_gen(
                            query='native_plants', 
                            description='''Medicinal plant species identified as native to the region, country, or geographic area discussed''', 
                            website_text=website_text
                        )
                        llm_business_rare_plants = llm_gen(
                            query='rare_plants', 
                            description='''Rare, threatened, endangered, vulnerable, or otherwise conservation-significant medicinal plant species mentioned''', 
                            website_text=website_text
                        )
                        llm_business_medicinal_plant_categories = llm_gen(
                            query='medicinal_plant_categories', 
                            description='''Categories or groupings of medicinal plants mentioned, such as adaptogens, aromatic herbs, medicinal trees, roots, flowers, or traditional herbal plants''', 
                            website_text=website_text
                        )
                        llm_business_botanical_collection_size = llm_gen(
                            query='botanical_collection_size', 
                            description='''Number of medicinal or botanical plant species in the organization's collection, garden, archive, nursery, or other stated botanical holdings, if specified''', 
                            website_text=website_text
                        )
                        # 7. Plant Relationships
                        llm_business_grows = llm_gen(
                            query='grows',
                            description='''Whether the business grows or cultivates plants, crops, or other botanical species itself.''',
                            website_text=website_text
                        )
                        llm_business_cultivates = llm_gen(
                            query='cultivates',
                            description='''Whether the business actively cultivates plants or botanical species through managed growing practices.''',
                            website_text=website_text
                        )
                        llm_business_propagates = llm_gen(
                            query='propagates',
                            description='''Whether the business propagates plants, such as through seeds, cuttings, division, tissue culture, or other propagation methods.''',
                            website_text=website_text
                        )
                        llm_business_researches = llm_gen(
                            query='researches',
                            description='''Whether the business conducts or supports research involving plants, botanical species, cultivation, or related applications.''',
                            website_text=website_text
                        )
                        llm_business_sells = llm_gen(
                            query='sells',
                            description='''Whether the business sells plants, botanical materials, or plant-derived products directly to customers.''',
                            website_text=website_text
                        )
                        llm_business_distributes = llm_gen(
                            query='distributes',
                            description='''Whether the business distributes plants, botanical materials, or plant-derived products to retailers, businesses, or other organizations.''',
                            website_text=website_text
                        )
                        llm_business_exports = llm_gen(
                            query='exports',
                            description='''Whether the business exports plants, botanical materials, or plant-derived products to other countries.''',
                            website_text=website_text
                        )
                        llm_business_imports = llm_gen(
                            query='imports',
                            description='''Whether the business imports plants, botanical materials, or plant-derived products from other countries.''',
                            website_text=website_text
                        )
                        llm_business_wild_harvests = llm_gen(
                            query='wild_harvests',
                            description='''Whether the business collects plants or botanical materials from wild or naturally occurring populations.''',
                            website_text=website_text
                        )
                        llm_business_conserves = llm_gen(
                            query='conserves',
                            description='''Whether the business engages in plant conservation, preservation, habitat protection, or safeguarding of botanical biodiversity.''',
                            website_text=website_text
                        )
                        llm_business_teaches = llm_gen(
                            query='teaches',
                            description='''Whether the business provides education, training, workshops, courses, or other instruction related to plants, cultivation, or botanical practices.''',
                            website_text=website_text
                        )
                        llm_business_uses_in_products = llm_gen(
                            query='uses_in_products',
                            description='''Whether the business uses plants, botanical materials, or plant-derived ingredients in products it manufactures or offers.''',
                            website_text=website_text
                        )
                        # 8. Products
                        llm_business_products = llm_gen(
                            query='products',
                            description='''Comprehensive information about all herbal and natural health products offered, including formulations, uses, and availability.''',
                            website_text=website_text
                        )
                        llm_business_product_categories = llm_gen(
                            query='product_categories',
                            description='''Overview of the different product categories available, including how products are organized by type or purpose.''',
                            website_text=website_text
                        )
                        llm_business_flagship_products = llm_gen(
                            query='flagship_products',
                            description='''Information about featured, best-selling, or signature products that represent the business's core offerings.''',
                            website_text=website_text
                        )
                        llm_business_product_forms = llm_gen(
                            query='product_forms',
                            description='''Details about the various forms in which products are available, such as teas, tinctures, capsules, powders, oils, and creams.''',
                            website_text=website_text
                        )
                        llm_business_herbal_teas = llm_gen(
                            query='herbal_teas',
                            description='''Information about herbal tea products, including ingredients, intended benefits, preparation methods, and available blends.''',
                            website_text=website_text
                        )
                        llm_business_tinctures = llm_gen(
                            query='tinctures',
                            description='''Details about herbal tinctures, including botanical ingredients, extraction methods, usage recommendations, and intended benefits.''',
                            website_text=website_text
                        )
                        llm_business_extracts = llm_gen(
                            query='extracts',
                            description='''Information about concentrated herbal extracts, including plant sources, extraction processes, applications, and available products.''',
                            website_text=website_text
                        )
                        llm_business_essential_oils = llm_gen(
                            query='essential_oils',
                            description='''Details about essential oils, including botanical origin, aromatic properties, recommended uses, and safety considerations.''',
                            website_text=website_text
                        )
                        llm_business_capsules = llm_gen(
                            query='capsules',
                            description='''Information about herbal capsules, including ingredients, dosage recommendations, intended uses, and available formulations.''',
                            website_text=website_text
                        )
                        llm_business_powders = llm_gen(
                            query='powders',
                            description='''Details about herbal powders, including plant sources, preparation methods, culinary or medicinal uses, and serving recommendations.''',
                            website_text=website_text
                        )
                        llm_business_dried_herbs = llm_gen(
                            query='dried_herbs',
                            description='''Information about dried herbs available for culinary, wellness, or medicinal purposes, including sourcing and preparation.''',
                            website_text=website_text
                        )
                        llm_business_fresh_herbs = llm_gen(
                            query='fresh_herbs',
                            description='''Details about fresh herbs offered, including varieties, seasonal availability, cultivation practices, and recommended uses.''',
                            website_text=website_text
                        )
                        llm_business_seeds = llm_gen(
                            query='seeds',
                            description='''Information about herb and plant seeds available for cultivation, including species, planting guidance, and growing conditions.''',
                            website_text=website_text
                        )
                        llm_business_seedlings = llm_gen(
                            query='seedlings',
                            description='''Details about live herb seedlings available for planting, including varieties, care instructions, and seasonal availability.''',
                            website_text=website_text
                        )
                        llm_business_roots = llm_gen(
                            query='roots',
                            description='''Information about medicinal or culinary roots offered, including botanical sources, preparation methods, and traditional uses.''',
                            website_text=website_text
                        )
                        llm_business_bark = llm_gen(
                            query='bark',
                            description='''Details about herbal bark products, including plant species, preparation methods, and traditional wellness applications.''',
                            website_text=website_text
                        )
                        llm_business_flowers = llm_gen(
                            query='flowers',
                            description='''Information about edible or medicinal flowers available, including botanical varieties, uses, and preparation methods.''',
                            website_text=website_text
                        )
                        llm_business_fruits = llm_gen(
                            query='fruits',
                            description='''Details about herbal or medicinal fruits offered, including varieties, health applications, and available product forms.''',
                            website_text=website_text
                        )
                        llm_business_resins = llm_gen(
                            query='resins',
                            description='''Information about natural plant resins, including botanical sources, traditional uses, and available preparations.''',
                            website_text=website_text
                        )
                        llm_business_cosmetics = llm_gen(
                            query='cosmetics',
                            description='''Details about natural cosmetic products, including ingredients, skincare benefits, and available formulations.''',
                            website_text=website_text
                        )
                        llm_business_soaps = llm_gen(
                            query='soaps',
                            description='''Information about natural or herbal soaps, including ingredients, skin benefits, fragrances, and available varieties.''',
                            website_text=website_text
                        )
                        llm_business_creams = llm_gen(
                            query='creams',
                            description='''Details about herbal creams, including active ingredients, intended uses, application instructions, and product variations.''',
                            website_text=website_text
                        )
                        llm_business_salves = llm_gen(
                            query='salves',
                            description='''Information about herbal salves, including botanical ingredients, intended topical applications, and usage recommendations.''',
                            website_text=website_text
                        )
                        llm_business_syrups = llm_gen(
                            query='syrups',
                            description='''Details about herbal syrups, including ingredients, intended wellness benefits, dosage guidance, and available formulations.''',
                            website_text=website_text
                        )
                        # 9. Product Attributes
                        llm_business_botanical_name = llm_gen(
                            query='botanical_name',
                            description='''The scientific botanical name of the plant, herb, or botanical ingredient, typically using its genus and species.''',
                            website_text=website_text
                        )
                        llm_business_common_name = llm_gen(
                            query='common_name',
                            description='''The commonly used name of the plant, herb, or botanical ingredient, including common or vernacular names.''',
                            website_text=website_text
                        )
                        llm_business_plant_part = llm_gen(
                            query='plant_part',
                            description='''The specific part of the plant used in the product, such as root, leaf, flower, seed, bark, fruit, or whole plant.''',
                            website_text=website_text
                        )
                        llm_business_extraction_method = llm_gen(
                            query='extraction_method',
                            description='''The method used to extract the active or desired botanical compounds, such as water extraction, alcohol extraction, CO₂ extraction, steam distillation, or maceration.''',
                            website_text=website_text
                        )
                        llm_business_preparation_method = llm_gen(
                            query='preparation_method',
                            description='''The form or process used to prepare the botanical product for use, such as dried, powdered, cut, tinctured, infused, encapsulated, or blended.''',
                            website_text=website_text
                        )
                        llm_business_ingredients = llm_gen(
                            query='ingredients',
                            description='''The ingredients contained in the product, including the primary botanical ingredients and any additional ingredients, carriers, excipients, or additives.''',
                            website_text=website_text
                        )
                        llm_business_packaging = llm_gen(
                            query='packaging',
                            description='''The type or format of packaging used for the product, such as bottle, jar, pouch, bag, box, tube, or bulk container.''',
                            website_text=website_text
                        )
                        llm_business_package_sizes = llm_gen(
                            query='package_sizes',
                            description='''The available package quantities or sizes, such as weight, volume, count, or other unit of measure.''',
                            website_text=website_text
                        )
                        llm_business_concentration = llm_gen(
                            query='concentration',
                            description='''The strength or concentration of the botanical preparation, extract, active ingredient, or standardized compound, when specified.''',
                            website_text=website_text
                        )
                        llm_business_organic_product = llm_gen(
                            query='organic_product',
                            description='''Indicates whether the product is identified, marketed, or certified as organic.''',
                            website_text=website_text
                        )
                        llm_business_private_label = llm_gen(
                            query='private_label',
                            description='''Indicates whether the product is available as a private-label product that can be branded and sold under another company's name.''',
                            website_text=website_text
                        )
                        llm_business_wholesale = llm_gen(
                            query='wholesale',
                            description='''Indicates whether the product is available for wholesale purchase, including bulk or business-to-business purchasing.''',
                            website_text=website_text
                        )
                        llm_business_retail = llm_gen(
                            query='retail',
                            description='''Indicates whether the product is available for direct retail purchase by individual consumers.''',
                            website_text=website_text
                        )
                        # 10. Services
                        llm_business_herbal_consultation = llm_gen(
                            query='herbal consultation',
                            description='''Professional consultation services focused on the traditional, therapeutic, or practical use of herbs and medicinal plants.''',
                            website_text=website_text
                        )
                        llm_business_herbal_clinic = llm_gen(
                            query='herbal clinic',
                            description='''A clinic or practice providing consultations and services related to herbal medicine and plant-based wellness.''',
                            website_text=website_text
                        )
                        llm_business_medicinal_plant_consulting = llm_gen(
                            query='medicinal plant consulting',
                            description='''Expert advice on the selection, use, cultivation, sourcing, processing, or commercialization of medicinal plants.''',
                            website_text=website_text
                        )
                        llm_business_plant_identification = llm_gen(
                            query='plant identification',
                            description='''Services for identifying plant species, varieties, or specimens based on their physical or botanical characteristics.''',
                            website_text=website_text
                        )
                        llm_business_botanical_identification = llm_gen(
                            query='botanical identification',
                            description='''Specialized identification and classification of plants using botanical taxonomy and scientific methods.''',
                            website_text=website_text
                        )
                        llm_business_cultivation_consulting = llm_gen(
                            query='cultivation consulting',
                            description='''Consulting services covering the cultivation, propagation, growing conditions, harvesting, and management of plants.''',
                            website_text=website_text
                        )
                        llm_business_contract_growing = llm_gen(
                            query='contract growing',
                            description='''Growing plants or agricultural crops on behalf of another business under an agreed contract or production arrangement.''',
                            website_text=website_text
                        )
                        llm_business_contract_manufacturing = llm_gen(
                            query='contract manufacturing',
                            description='''Manufacturing botanical, herbal, or plant-based products on behalf of another company or brand.''',
                            website_text=website_text
                        )
                        llm_business_private_label_manufacturing = llm_gen(
                            query='private label manufacturing',
                            description='''Production of herbal, botanical, or plant-based products that are sold under a customer's own brand or private label.''',
                            website_text=website_text
                        )
                        llm_business_extraction_services = llm_gen(
                            query='extraction services',
                            description='''Services for extracting active compounds, oils, or other useful constituents from plants or botanical materials.''',
                            website_text=website_text
                        )
                        llm_business_drying_services = llm_gen(
                            query='drying services',
                            description='''Commercial drying of harvested plants, herbs, roots, leaves, flowers, or other botanical materials to preserve and prepare them for further use.''',
                            website_text=website_text
                        )
                        llm_business_milling = llm_gen(
                            query='milling',
                            description='''Mechanical processing of plant or botanical materials into smaller particles or a desired particle size.''',
                            website_text=website_text
                        )
                        llm_business_grinding = llm_gen(
                            query='grinding',
                            description='''Processing herbs, plants, seeds, roots, or other botanical materials into a coarse or fine ground form.''',
                            website_text=website_text
                        )
                        llm_business_packaging_service = llm_gen(
                            query='packaging_service',
                            description='''Packaging services for herbal, botanical, agricultural, or plant-based products in suitable containers or formats.''',
                            website_text=website_text
                        )
                        llm_business_export_services = llm_gen(
                            query='export services',
                            description='''Services supporting the preparation, documentation, logistics, and international shipment of botanical or plant-based products.''',
                            website_text=website_text
                        )
                        llm_business_laboratory_testing = llm_gen(
                            query='laboratory testing',
                            description='''Laboratory analysis and testing of botanical or herbal materials and products for quality, identity, purity, safety, or composition.''',
                            website_text=website_text
                        )
                        llm_business_formulation = llm_gen(
                            query='formulation',
                            description='''Development or preparation of recipes and product formulations using herbs, botanicals, extracts, or other plant-based ingredients.''',
                            website_text=website_text
                        )
                        llm_business_research_services = llm_gen(
                            query='research services',
                            description='''Research and development services involving medicinal plants, botanicals, herbal products, cultivation, extraction, or related scientific topics.''',
                            website_text=website_text
                        )
                        llm_business_education = llm_gen(
                            query='education',
                            description='''Educational services providing knowledge or training related to herbs, medicinal plants, botany, cultivation, processing, or herbal practices.''',
                            website_text=website_text
                        )
                        llm_business_workshops = llm_gen(
                            query='workshops',
                            description='''Practical, focused educational sessions or hands-on activities covering herbal, botanical, cultivation, processing, or related topics.''',
                            website_text=website_text
                        )
                        llm_business_courses = llm_gen(
                            query='courses',
                            description='''Structured educational programs providing systematic instruction in herbal medicine, botany, plant cultivation, or related subjects.''',
                            website_text=website_text
                        )
                        llm_business_farm_tours = llm_gen(
                            query='farm tours',
                            description='''Guided visits to farms or agricultural operations where participants can learn about plant cultivation, harvesting, and production.''',
                            website_text=website_text
                        )
                        llm_business_botanical_tours = llm_gen(
                            query='botanical tours',
                            description='''Guided tours focused on identifying, studying, and learning about botanical species and plant collections in natural or cultivated settings.''',
                            website_text=website_text
                        )
                        # 11. Cultivation
                        llm_business_cultivation_methods = llm_gen(
                            query='cultivation_methods',
                            description='''The overall cultivation approach or farming system used to grow the ingredient, including conventional and specialized agricultural practices.''',
                            website_text=website_text
                        )
                        llm_business_organic_cultivation = llm_gen(
                            query='organic_cultivation',
                            description='''Whether the ingredient is cultivated according to certified or non-certified organic farming practices that avoid synthetic pesticides and fertilizers.''',
                            website_text=website_text
                        )
                        llm_business_regenerative = llm_gen(
                            query='regenerative',
                            description='''Whether regenerative agricultural practices are used to improve soil health, biodiversity, carbon sequestration, and ecosystem resilience.''',
                            website_text=website_text
                        )
                        llm_business_biodynamic = llm_gen(
                            query='biodynamic',
                            description='''Whether the ingredient is produced using biodynamic farming principles, including holistic farm management and biodynamic preparations.''',
                            website_text=website_text
                        )
                        llm_business_permaculture = llm_gen(
                            query='permaculture',
                            description='''Whether permaculture design principles are applied to create sustainable, self-supporting agricultural ecosystems.''',
                            website_text=website_text
                        )
                        llm_business_agroforestry = llm_gen(
                            query='agroforestry',
                            description='''Whether the ingredient is cultivated within an agroforestry system that integrates trees with crops or livestock.''',
                            website_text=website_text
                        )
                        llm_business_greenhouse = llm_gen(
                            query='greenhouse',
                            description='''Whether the ingredient is grown in greenhouse or protected cultivation environments.''',
                            website_text=website_text
                        )
                        llm_business_indoor = llm_gen(
                            query='indoor',
                            description='''Whether the ingredient is cultivated entirely indoors using controlled environmental conditions.''',
                            website_text=website_text
                        )
                        llm_business_outdoor = llm_gen(
                            query='outdoor',
                            description='''Whether the ingredient is grown outdoors under natural environmental conditions.''',
                            website_text=website_text
                        )
                        llm_business_wild_harvesting = llm_gen(
                            query='wild_harvesting',
                            description='''Whether the ingredient is collected from naturally occurring wild populations rather than cultivated sources.''',
                            website_text=website_text
                        )
                        llm_business_sustainable_wild_harvesting = llm_gen(
                            query='sustainable_wild_harvesting',
                            description='''Whether wild harvesting practices are managed to maintain long-term ecosystem health and species populations.''',
                            website_text=website_text
                        )
                        llm_business_propagation_methods = llm_gen(
                            query='propagation_methods',
                            description='''The methods used to propagate or establish the crop, such as seeds, cuttings, grafting, division, or tissue culture.''',
                            website_text=website_text
                        )
                        llm_business_irrigation = llm_gen(
                            query='irrigation',
                            description='''The irrigation methods and water management practices used during cultivation.''',
                            website_text=website_text
                        )
                        llm_business_fertilization = llm_gen(
                            query='fertilization',
                            description='''The fertilizers, nutrient sources, and fertilization practices applied during cultivation.''',
                            website_text=website_text
                        )
                        llm_business_soil_management = llm_gen(
                            query='soil_management',
                            description='''The soil preparation, conservation, and management practices used to maintain soil quality and fertility.''',
                            website_text=website_text
                        )
                        llm_business_pest_management = llm_gen(
                            query='pest_management',
                            description='''The strategies used to prevent, monitor, and control pests and diseases, including integrated pest management approaches.''',
                            website_text=website_text
                        )
                        llm_business_harvest_methods = llm_gen(
                            query='harvest_methods',
                            description='''The techniques and procedures used to harvest the ingredient, including manual or mechanical methods.''',
                            website_text=website_text
                        )
                        llm_business_harvest_season = llm_gen(
                            query='harvest_season',
                            description='''The typical season or time of year during which the ingredient is harvested.''',
                            website_text=website_text
                        )
                        # 12. Manufacturing
                        llm_business_manufacturing = llm_gen(
                            query='manufacturing',
                            description='''The production of goods or products from raw materials through defined manufacturing processes.''',
                            website_text=website_text
                        )
                        llm_business_processing = llm_gen(
                            query='processing',
                            description='''The treatment, conversion, or preparation of raw materials or intermediate materials to produce a desired product or ingredient.''',
                            website_text=website_text
                        )
                        llm_business_extraction = llm_gen(
                            query='extraction',
                            description='''The process of separating and recovering specific compounds, ingredients, or substances from a raw material using physical, chemical, or mechanical methods.''',
                            website_text=website_text
                        )
                        llm_business_distillation = llm_gen(
                            query='distillation',
                            description='''A separation and purification process that uses differences in boiling points to isolate or concentrate specific components of a mixture.''',
                            website_text=website_text
                        )
                        llm_business_fermentation = llm_gen(
                            query='fermentation',
                            description='''A controlled biological process in which microorganisms convert organic substances into desired products, compounds, or intermediates.''',
                            website_text=website_text
                        )
                        llm_business_drying = llm_gen(
                            query='drying',
                            description='''The controlled removal of moisture from raw materials, ingredients, or products to improve stability, preservation, handling, or shelf life.''',
                            website_text=website_text
                        )
                        llm_business_manufacturing_milling = llm_gen(
                            query='manufacturing_milling',
                            description='''The mechanical reduction of raw materials or ingredients into smaller particles or a specified particle size.''',
                            website_text=website_text
                        )
                        llm_business_manufacturing_grinding = llm_gen(
                            query='manufacturing_grinding',
                            description='''The mechanical breakdown of materials into finer particles using friction, impact, compression, or other mechanical forces.''',
                            website_text=website_text
                        )
                        llm_business_blending = llm_gen(
                            query='blending',
                            description='''The controlled mixing of two or more ingredients, materials, or components to achieve a uniform composition or desired properties.''',
                            website_text=website_text
                        )
                        llm_business_manufacturing_formulation = llm_gen(
                            query='manufacturing_formulation',
                            description='''The development and combination of ingredients or components in defined proportions to create a product with specified characteristics or performance.''',
                            website_text=website_text
                        )
                        llm_business_encapsulation = llm_gen(
                            query='encapsulation',
                            description='''The process of enclosing an active ingredient, compound, or material within a capsule or protective coating for delivery, stability, or controlled release.''',
                            website_text=website_text
                        )
                        llm_business_manufacturing_packaging = llm_gen(
                            query='manufacturing_packaging',
                            description='''The process of enclosing, protecting, labeling, and preparing products for storage, transportation, distribution, or sale.''',
                            website_text=website_text
                        )
                        llm_business_quality_testing = llm_gen(
                            query='quality_testing',
                            description='''Testing performed to verify that raw materials, intermediates, or finished products meet defined quality specifications, standards, and requirements.''',
                            website_text=website_text
                        )
                        llm_business_batch_testing = llm_gen(
                            query='batch_testing',
                            description='''Testing performed on a specific production batch to confirm that it meets established specifications for identity, quality, safety, purity, potency, or other required characteristics.''',
                            website_text=website_text
                        )
                        llm_business_traceability = llm_gen(
                            query='traceability',
                            description='''The ability to track the history, origin, processing, movement, and status of materials or products throughout the supply chain and production process.''',
                            website_text=website_text
                        )
                        # 13. Facilities
                        llm_business_facilities_farms = llm_gen(
                            query='farms',
                            description='''Agricultural facilities where plants, crops, or other botanical products are cultivated and managed.''',
                            website_text=website_text
                        )
                        llm_business_facilities_nurseries = llm_gen(
                            query='nurseries',
                            description='''Facilities that propagate, grow, and maintain plants, seedlings, saplings, and other young botanical specimens before sale, transplantation, or further cultivation.''',
                            website_text=website_text
                        )
                        llm_business_facilities_laboratories = llm_gen(
                            query='laboratories',
                            description='''Specialized facilities used for scientific analysis, experimentation, testing, and research involving plants, biological materials, soils, or related products.''',
                            website_text=website_text
                        )
                        llm_business_facilities_factories = llm_gen(
                            query='factories',
                            description='''Industrial facilities where agricultural, botanical, or plant-derived materials are processed, manufactured, packaged, or transformed into finished products.''',
                            website_text=website_text
                        )
                        llm_business_facilities_warehouses = llm_gen(
                            query='warehouses',
                            description='''Storage facilities used to hold plants, agricultural products, botanical materials, equipment, supplies, or finished goods.''',
                            website_text=website_text
                        )
                        llm_business_facilities_botanical_gardens = llm_gen(
                            query='botanical_gardens',
                            description='''Public or private gardens dedicated to the cultivation, conservation, research, documentation, and display of diverse plant species and collections.''',
                            website_text=website_text
                        )
                        llm_business_facilities_greenhouses = llm_gen(
                            query='greenhouses',
                            description='''Controlled-environment structures designed for growing and maintaining plants by regulating conditions such as temperature, humidity, light, and ventilation.''',
                            website_text=website_text
                        )
                        llm_business_facilities_visitor_centers = llm_gen(
                            query='visitor_centers',
                            description='''Facilities that provide visitors with information, exhibits, services, tours, and educational resources related to a site, organization, garden, farm, or research facility.''',
                            website_text=website_text
                        )
                        llm_business_facilities_research_centers = llm_gen(
                            query='research_centers',
                            description='''Facilities dedicated to scientific investigation, experimentation, innovation, and research in areas such as agriculture, botany, horticulture, ecology, or plant science.''',
                            website_text=website_text
                        )
                        llm_business_facilities_education_centers = llm_gen(
                            query='education_centers',
                            description='''Facilities that provide educational programs, workshops, training, demonstrations, and learning resources related to agriculture, plants, horticulture, science, or environmental topics.''',
                            website_text=website_text
                        )
                        llm_business_facilities_clinics = llm_gen(
                            query='clinics',
                            description='''Facilities that provide diagnostic, treatment, consultation, or health-related services, including specialized services for plants, animals, or people where applicable.''',
                            website_text=website_text
                        )
                        llm_business_facilities_retail_stores = llm_gen(
                            query='retail_stores',
                            description='''Commercial facilities where plants, agricultural products, gardening supplies, botanical goods, equipment, or related products are displayed and sold to customers.''',
                            website_text=website_text
                        )
                        # 14. Certifications
                        llm_business_certifications_certifications = llm_gen(
                            query='certifications', 
                            description='''Stores certification records associated with the business, including certification details, issuing organization, dates, and scope.''', 
                            website_text=website_text
                        )
                        llm_business_certifications_certification_name = llm_gen(
                            query='certification_name', 
                            description='''The name or title of the certification obtained by the business or individual.''', 
                            website_text=website_text
                        )
                        llm_business_certifications_certification_number = llm_gen(
                            query='certification_number', 
                            description='''The unique identification number, reference number, or certificate number assigned to the certification.''', 
                            website_text=website_text
                        )
                        llm_business_certifications_issuing_organization = llm_gen(
                            query='issuing_organization', 
                            description='''The organization, authority, or institution that issued the certification.''', 
                            website_text=website_text
                        )
                        llm_business_certifications_issue_date = llm_gen(
                            query='issue_date', 
                            description='''The date on which the certification was issued or became effective.''', 
                            website_text=website_text
                        )
                        llm_business_certifications_expiry_date = llm_gen(
                            query='expiry_date', 
                            description='''The date on which the certification expires or is no longer valid, if applicable.''', 
                            website_text=website_text
                        )
                        llm_business_certifications_certification_scope = llm_gen(
                            query='certification_scope', 
                            description='''Describes the activities, services, products, locations, standards, or areas covered by the certification.''', 
                            website_text=website_text
                        )
                        # 15. Quality
                        llm_business_quality_quality_control = llm_gen(
                            query='quality_control', 
                            description='''Information about the company's procedures and measures for maintaining and monitoring product quality throughout production.''', 
                            website_text=website_text
                        )
                        llm_business_quality_laboratory_testing = llm_gen(
                            query='laboratory_testing', 
                            description='''Information about laboratory tests performed on products, materials, ingredients, or samples to verify quality, safety, purity, or compliance.''', 
                            website_text=website_text
                        )
                        llm_business_quality_batch_testing = llm_gen(
                            query='batch_testing', 
                            description='''Information about testing conducted on individual production batches to verify consistency, quality, safety, or compliance with specifications.''', 
                            website_text=website_text
                        )
                        llm_business_quality_third_party_testing = llm_gen(
                            query='third_party_testing', 
                            description='''Information about independent testing performed by external laboratories or organizations to verify product quality, safety, purity, or compliance.''', 
                            website_text=website_text
                        )
                        llm_business_quality_traceability = llm_gen(
                            query='traceability', 
                            description='''Information about systems and procedures used to track products, ingredients, raw materials, or batches throughout the supply chain and production process.''', 
                            website_text=website_text
                        )
                        llm_business_quality_quality_management_system = llm_gen(
                            query='quality_management_system', 
                            description='''Information about the formal systems, standards, procedures, and processes used to consistently manage, monitor, and improve product quality.''', 
                            website_text=website_text
                        )
                        # 16. Sustainability
                        llm_business_sustainability_sustainability_policy = llm_gen(
                            query='sustainability_policy', 
                            description='''Describes the business's overall sustainability policy, commitments, goals, and practices for reducing environmental and social impacts.''', 
                            website_text=website_text
                        )
                        llm_business_sustainability_conservation = llm_gen(
                            query='conservation', 
                            description='''Describes initiatives and practices focused on conserving natural resources, ecosystems, habitats, and wildlife.''', 
                            website_text=website_text
                        )
                        llm_business_sustainability_biodiversity = llm_gen(
                            query='biodiversity', 
                            description='''Describes efforts to protect, restore, and enhance biodiversity, including the preservation of species, habitats, and ecosystems.''', 
                            website_text=website_text
                        )
                        llm_business_sustainability_regenerative_agriculture = llm_gen(
                            query='regenerative_agriculture', 
                            description='''Describes agricultural practices that restore soil health, improve ecosystem resilience, enhance biodiversity, and reduce environmental impact.''', 
                            website_text=website_text
                        )
                        llm_business_sustainability_ethical_sourcing = llm_gen(
                            query='ethical_sourcing', 
                            description='''Describes how the business sources products and materials responsibly, considering environmental standards, labor conditions, human rights, and supply-chain transparency.''', 
                            website_text=website_text
                        )
                        llm_business_sustainability_fair_trade = llm_gen(
                            query='fair_trade', 
                            description='''Describes the business's use or support of fair-trade products and practices that promote fair prices, decent working conditions, and equitable treatment of producers.''', 
                            website_text=website_text
                        )
                        llm_business_sustainability_community_projects = llm_gen(
                            query='community_projects', 
                            description='''Describes sustainability or social-impact projects that support local communities, including education, infrastructure, livelihoods, conservation, or community development.''', 
                            website_text=website_text
                        )
                        llm_business_sustainability_indigenous_partnerships = llm_gen(
                            query='indigenous_partnerships', 
                            description='''Describes partnerships and initiatives involving Indigenous communities, including respect for Indigenous rights, knowledge, culture, land, and economic participation.''', 
                            website_text=website_text
                        )
                        llm_business_sustainability_local_sourcing = llm_gen(
                            query='local_sourcing', 
                            description='''Describes the extent to which products, ingredients, materials, or services are sourced from local or regional suppliers to support local economies and reduce transportation impacts.''', 
                            website_text=website_text
                        )
                        llm_business_sustainability_recyclable_packaging = llm_gen(
                            query='recyclable_packaging', 
                            description='''Describes the use of packaging that can be recycled, along with initiatives to reduce packaging waste and improve packaging recyclability.''', 
                            website_text=website_text
                        )
                        llm_business_sustainability_carbon_reduction = llm_gen(
                            query='carbon_reduction', 
                            description='''Describes initiatives to measure, reduce, offset, or otherwise manage greenhouse-gas emissions and the business's carbon footprint.''', 
                            website_text=website_text
                        )
                        llm_business_sustainability_water_conservation = llm_gen(
                            query='water_conservation', 
                            description='''Describes practices and initiatives designed to reduce water consumption, improve water efficiency, protect water resources, and minimize water-related environmental impacts.''', 
                            website_text=website_text
                        )
                        # 17. Research
                        llm_business_research_research_programs = llm_gen(
                            query='research_programs', 
                            description='''Organized research programs focused on investigating medicinal plants, natural products, traditional medicine, therapeutic applications, and related scientific topics.''', 
                            website_text=website_text
                        )
                        llm_business_research_research_projects = llm_gen(
                            query='research_projects', 
                            description='''Individual research projects involving the study, development, validation, or application of plants, natural compounds, botanical medicines, and related scientific subjects.''', 
                            website_text=website_text
                        )
                        llm_business_research_publications = llm_gen(
                            query='publications', 
                            description='''Scientific publications, research papers, reviews, books, reports, and other scholarly works documenting research findings and knowledge.''', 
                            website_text=website_text
                        )
                        llm_business_research_patents = llm_gen(
                            query='patents', 
                            description='''Patents and patent applications covering novel discoveries, formulations, extraction methods, compounds, technologies, or other innovations related to botanical and natural-product research.''', 
                            website_text=website_text
                        )
                        llm_business_research_university_partnerships = llm_gen(
                            query='university_partnerships', 
                            description='''Collaborations and formal partnerships with universities or academic institutions supporting research, education, knowledge exchange, and scientific development.''', 
                            website_text=website_text
                        )
                        llm_business_research_clinical_trials = llm_gen(
                            query='clinical_trials', 
                            description='''Clinical studies evaluating the safety, efficacy, pharmacological effects, or therapeutic potential of medicinal plants, botanical preparations, or natural compounds in humans.''', 
                            website_text=website_text
                        )
                        llm_business_research_ethnobotanical_research = llm_gen(
                            query='ethnobotanical_research', 
                            description='''Research examining traditional knowledge and cultural uses of plants, including their medicinal, nutritional, agricultural, and other practical applications.''', 
                            website_text=website_text
                        )
                        llm_business_research_pharmacognosy = llm_gen(
                            query='pharmacognosy', 
                            description='''Research focused on medicinal substances obtained from natural sources, particularly the identification, characterization, evaluation, and quality control of medicinal plants and natural products.''', 
                            website_text=website_text
                        )
                        llm_business_research_phytochemistry = llm_gen(
                            query='phytochemistry', 
                            description='''Research investigating the chemical constituents of plants, including the isolation, identification, characterization, and analysis of bioactive phytochemicals.''', 
                            website_text=website_text
                        )
                        llm_business_research_plant_breeding = llm_gen(
                            query='plant_breeding', 
                            description='''Research involving the selective development and improvement of plant varieties for desirable traits such as yield, quality, resilience, medicinal properties, or enhanced concentrations of bioactive compounds.''', 
                            website_text=website_text
                        )
                        # 18. Education
                        llm_business_education_courses = llm_gen(
                            query='courses', 
                            description='''Educational programs designed to provide structured learning and practical knowledge on specific topics or skills.''', 
                            website_text=website_text
                        )
                        llm_business_education_workshops = llm_gen(
                            query='workshops', 
                            description='''Interactive, hands-on learning sessions focused on developing practical skills, techniques, or knowledge.''', 
                            website_text=website_text
                        )
                        llm_business_education_webinars = llm_gen(
                            query='webinars', 
                            description='''Online educational sessions delivered remotely, typically featuring presentations, demonstrations, or discussions on specific topics.''', 
                            website_text=website_text
                        )
                        llm_business_education_apprenticeships = llm_gen(
                            query='apprenticeships', 
                            description='''Structured work-based learning opportunities that combine practical experience with guided instruction and skill development.''', 
                            website_text=website_text
                        )
                        llm_business_education_lectures = llm_gen(
                            query='lectures', 
                            description='''Educational presentations delivered by an instructor or expert to explain concepts, share knowledge, or explore a specific subject.''', 
                            website_text=website_text
                        )
                        llm_business_education_botanical_walks = llm_gen(
                            query='botanical_walks', 
                            description='''Guided outdoor educational walks focused on identifying, understanding, and learning about plants and their natural environments.''', 
                            website_text=website_text
                        )
                        llm_business_education_farm_tours = llm_gen(
                            query='farm_tours', 
                            description='''Guided visits to farms that provide educational insight into agricultural practices, farming operations, crops, livestock, or food production.''', 
                            website_text=website_text
                        )
                        llm_business_education_certifications_offered = llm_gen(
                            query='certifications_offered', 
                            description='''Professional or educational certifications available to participants who complete specified training, courses, assessments, or requirements.''', 
                            website_text=website_text
                        )
                        # 19. Traditional Medicine Systems
                        llm_business_traditional_medicine_systems_ayurveda = llm_gen(
                            query='ayurveda', 
                            description='''A traditional system of medicine originating in India that emphasizes balance among the body, mind, and environment through diet, lifestyle practices, herbal preparations, and other therapeutic approaches.''', 
                            website_text=website_text
                        )
                        llm_business_traditional_medicine_systems_traditional_chinese_medicine = llm_gen(
                            query='traditional_chinese_medicine', 
                            description='''A traditional medical system originating in China that uses approaches such as acupuncture, herbal medicine, dietary therapy, massage, and movement practices to promote balance and support health.''', 
                            website_text=website_text
                        )
                        llm_business_traditional_medicine_systems_western_herbalism = llm_gen(
                            query='western_herbalism', 
                            description='''A tradition of herbal medicine rooted primarily in European and Western practices that uses medicinal plants and plant preparations to support health and address various health concerns.''', 
                            website_text=website_text
                        )
                        llm_business_traditional_medicine_systems_unani = llm_gen(
                            query='unani', 
                            description='''A traditional system of medicine developed from Greco-Arabic medical traditions and practiced extensively in South Asia and other regions, emphasizing bodily balance, diet, lifestyle, and natural remedies.''', 
                            website_text=website_text
                        )
                        llm_business_traditional_medicine_systems_kampo = llm_gen(
                            query='kampo', 
                            description='''A Japanese traditional medicine system derived from classical Chinese medical traditions that primarily uses standardized combinations of medicinal herbs formulated according to traditional diagnostic principles.''', 
                            website_text=website_text
                        )
                        llm_business_traditional_medicine_systems_tibetan_medicine = llm_gen(
                            query='tibetan_medicine', 
                            description='''A traditional medical system originating in Tibet that integrates herbal and mineral remedies, dietary and behavioral practices, and concepts of bodily balance influenced by Tibetan Buddhist and broader Asian medical traditions.''', 
                            website_text=website_text
                        )
                        llm_business_traditional_medicine_systems_indigenous_medicine = llm_gen(
                            query='indigenous_medicine', 
                            description='''Traditional health practices developed and maintained by Indigenous peoples, incorporating locally available plants, foods, cultural knowledge, spiritual practices, and community-based approaches to health and healing.''', 
                            website_text=website_text
                        )
                        llm_business_traditional_medicine_systems_african_traditional_medicine = llm_gen(
                            query='african_traditional_medicine', 
                            description='''Diverse traditional healing systems practiced across African communities that commonly incorporate medicinal plants, animal or mineral substances, cultural knowledge, spiritual practices, and community-based healing traditions.''', 
                            website_text=website_text
                        )
                        # 20. Expertise
                        llm_business_expertise_expertise_topics = llm_gen(
                            query='expertise_topics', 
                            description='''Areas of specialized knowledge, experience, or professional focus related to herbalism, medicinal plants, botany, and natural medicine.''', 
                            website_text=website_text
                        )
                        llm_business_expertise_medicinal_plant_cultivation = llm_gen(
                            query='medicinal_plant_cultivation', 
                            description='''Knowledge and practical experience in growing, managing, harvesting, and maintaining plants used for medicinal purposes.''', 
                            website_text=website_text
                        )
                        llm_business_expertise_herbal_formulation = llm_gen(
                            query='herbal_formulation', 
                            description='''Expertise in developing, combining, preparing, and optimizing herbal preparations using medicinal plants and botanical ingredients.''', 
                            website_text=website_text
                        )
                        llm_business_expertise_ethnobotany = llm_gen(
                            query='ethnobotany', 
                            description='''Study and knowledge of the relationships between people, cultures, and plants, including traditional uses of plants for food, medicine, rituals, and other purposes.''', 
                            website_text=website_text
                        )
                        llm_business_expertise_pharmacognosy = llm_gen(
                            query='pharmacognosy', 
                            description='''Scientific expertise in the study of medicinal substances derived from natural sources, particularly plants, including their identification, constituents, properties, and therapeutic uses.''', 
                            website_text=website_text
                        )
                        llm_business_expertise_botanical_identification = llm_gen(
                            query='botanical_identification', 
                            description='''Ability to accurately identify and classify plants using botanical characteristics, taxonomy, morphology, and other identification methods.''', 
                            website_text=website_text
                        )
                        llm_business_expertise_herbal_medicine = llm_gen(
                            query='herbal_medicine', 
                            description='''Knowledge and experience in the traditional and contemporary use of medicinal herbs and plant-based remedies to support health and well-being.''', 
                            website_text=website_text
                        )
                        llm_business_expertise_conservation = llm_gen(
                            query='conservation', 
                            description='''Expertise in protecting, preserving, and sustainably managing medicinal plants, botanical resources, habitats, and plant biodiversity.''', 
                            website_text=website_text
                        )
                        llm_business_expertise_plant_propagation = llm_gen(
                            query='plant_propagation', 
                            description='''Knowledge and practical experience in reproducing plants through methods such as seeds, cuttings, division, layering, grafting, and tissue culture.''', 
                            website_text=website_text
                        )
                        # 21. People
                        llm_business_people_founders = llm_gen(
                            query='founders',
                            description='''The founders of the company, organization, farm, institution, or brand, including individuals who established or co-founded it.''',
                            website_text=website_text
                        )
                        llm_business_people_owners = llm_gen(
                            query='owners',
                            description='''The current or past owners of the company, farm, laboratory, organization, or brand, including individuals or ownership groups.''',
                            website_text=website_text
                        )
                        llm_business_people_ceo = llm_gen(
                            query='ceo',
                            description='''The Chief Executive Officer (CEO) or equivalent top executive responsible for leading the organization's overall strategy and operations.''',
                            website_text=website_text
                        )
                        llm_business_people_president = llm_gen(
                            query='president',
                            description='''The president of the company, organization, institution, or association, including current or former presidents.''',
                            website_text=website_text
                        )
                        llm_business_people_director = llm_gen(
                            query='director',
                            description='''Directors or executive directors responsible for overseeing departments, programs, research, operations, or the organization as a whole.''',
                            website_text=website_text
                        )
                        llm_business_people_botanists = llm_gen(
                            query='botanists',
                            description='''Botanists associated with the organization, including plant scientists, taxonomists, or experts involved in botanical research and plant identification.''',
                            website_text=website_text
                        )
                        llm_business_people_herbalists = llm_gen(
                            query='herbalists',
                            description='''Herbalists associated with the organization, including practitioners, formulators, educators, or experts in medicinal plants and herbal medicine.''',
                            website_text=website_text
                        )
                        llm_business_people_researchers = llm_gen(
                            query='researchers',
                            description='''Researchers affiliated with the organization, including scientists, scholars, investigators, and research staff contributing to scientific or technical work.''',
                            website_text=website_text
                        )
                        llm_business_people_agronomists = llm_gen(
                            query='agronomists',
                            description='''Agronomists associated with the organization, including experts in crop science, soil management, sustainable agriculture, and farming practices.''',
                            website_text=website_text
                        )
                        llm_business_people_pharmacists = llm_gen(
                            query='pharmacists',
                            description='''Pharmacists associated with the organization, including licensed pharmacists, pharmaceutical scientists, formulators, and medication experts.''',
                            website_text=website_text
                        )
                        llm_business_people_educators = llm_gen(
                            query='educators',
                            description='''Educators affiliated with the organization, including instructors, trainers, professors, lecturers, and educational program leaders.''',
                            website_text=website_text
                        )
                        llm_business_people_laboratory_directors = llm_gen(
                            query='laboratory_directors',
                            description='''Laboratory directors responsible for overseeing laboratory operations, scientific research, quality assurance, testing, and compliance.''',
                            website_text=website_text
                        )
                        llm_business_people_farm_managers = llm_gen(
                            query='farm_managers',
                            description='''Farm managers responsible for supervising agricultural operations, crop production, livestock management, and day-to-day farm activities.''',
                            website_text=website_text
                        )
                        # 22. Markets
                        llm_business_markets_customer_types = llm_gen(
                            query='customer_types', 
                            description='''Types of customers the business serves, such as consumers, businesses, distributors, retailers, wholesalers, government organizations, or other customer segments.''', 
                            website_text=website_text
                        )
                        llm_business_markets_industries_served = llm_gen(
                            query='industries_served', 
                            description='''Industries, sectors, or business verticals that the company provides products or services to.''', 
                            website_text=website_text
                        )
                        llm_business_markets_export_markets = llm_gen(
                            query='export_markets', 
                            description='''Countries or international markets where the company exports or sells its products outside its primary domestic market.''', 
                            website_text=website_text
                        )
                        llm_business_markets_import_markets = llm_gen(
                            query='import_markets', 
                            description='''Countries or international markets from which the company imports products, materials, components, or other goods.''', 
                            website_text=website_text
                        )
                        llm_business_markets_countries_served = llm_gen(
                            query='countries_served', 
                            description='''Individual countries where the company sells, operates, distributes products, or otherwise provides its products or services.''', 
                            website_text=website_text
                        )
                        llm_business_markets_regions_served = llm_gen(
                            query='regions_served', 
                            description='''Geographic regions, territories, states, provinces, or broader areas where the company operates or serves customers.''', 
                            website_text=website_text
                        )
                        llm_business_markets_international_shipping = llm_gen(
                            query='international_shipping', 
                            description='''Whether the company offers shipping or delivery to customers in countries outside its domestic market, including any stated international shipping capabilities.''', 
                            website_text=website_text
                        )
                        llm_business_markets_wholesale_available = llm_gen(
                            query='wholesale_available', 
                            description='''Whether the company offers products or services through wholesale purchasing arrangements, including bulk sales to retailers, distributors, or other businesses.''', 
                            website_text=website_text
                        )
                        llm_business_markets_retail_available = llm_gen(
                            query='retail_available', 
                            description='''Whether the company sells products or services directly to individual consumers through retail channels, such as physical stores or online stores.''', 
                            website_text=website_text
                        )
                        llm_business_markets_private_label_available = llm_gen(
                            query='private_label_available', 
                            description='''Whether the company offers private-label or white-label products that can be sold under another company's or customer's brand.''', 
                            website_text=website_text
                        )

                        # 23. Online Presence
                        llm_business_online_presence_facebook = llm_gen(
                            query='facebook', 
                            description='''The business's official Facebook profile or page, used for sharing updates, content, announcements, and engaging with its audience.''', 
                            website_text=website_text
                        )
                        llm_business_online_presence_instagram = llm_gen(
                            query='instagram', 
                            description='''The business's official Instagram profile, used for visual content, updates, promotions, and audience engagement.''', 
                            website_text=website_text
                        )
                        llm_business_online_presence_linkedin = llm_gen(
                            query='linkedin', 
                            description='''The business's official LinkedIn profile or company page, used for professional information, company updates, hiring, and industry engagement.''', 
                            website_text=website_text
                        )
                        llm_business_online_presence_youtube = llm_gen(
                            query='youtube', 
                            description='''The business's official YouTube channel, used for publishing and sharing video content, tutorials, presentations, or other media.''', 
                            website_text=website_text
                        )
                        llm_business_online_presence_x = llm_gen(
                            query='x', 
                            description='''The business's official X (formerly Twitter) profile, used for short-form updates, announcements, news, and audience engagement.''', 
                            website_text=website_text
                        )
                        llm_business_online_presence_pinterest = llm_gen(
                            query='pinterest', 
                            description='''The business's official Pinterest profile, used for sharing visual content, inspiration, products, and links through pins and boards.''', 
                            website_text=website_text
                        )
                        llm_business_online_presence_tiktok = llm_gen(
                            query='tiktok', 
                            description='''The business's official TikTok profile, used for publishing short-form video content, promotions, and audience engagement.''', 
                            website_text=website_text
                        )
                        llm_business_online_presence_github = llm_gen(
                            query='github', 
                            description='''The business's official GitHub organization or profile, used for hosting and sharing source code, software projects, documentation, and developer resources.''', 
                            website_text=website_text
                        )
                        llm_business_online_presence_wikipedia = llm_gen(
                            query='wikipedia', 
                            description='''The business's Wikipedia article or relevant Wikipedia page, providing publicly documented, encyclopedic information about the business.''', 
                            website_text=website_text
                        )

                        # 24. Awards
                        llm_business_awards_awards = llm_gen(
                            query='awards', 
                            description='''Stores information about awards and recognitions associated with the business, organization, or entity.''', 
                            website_text=website_text
                        )
                        llm_business_awards_award_name = llm_gen(
                            query='award_name', 
                            description='''The name or title of the award received by the business, organization, or entity.''', 
                            website_text=website_text
                        )
                        llm_business_awards_award_year = llm_gen(
                            query='award_year', 
                            description='''The year in which the award was received or awarded.''', 
                            website_text=website_text
                        )
                        llm_business_awards_awarding_organization = llm_gen(
                            query='awarding_organization', 
                            description='''The name of the organization, institution, association, or body that presented the award.''', 
                            website_text=website_text
                        )

                        # 25. Memberships
                        llm_business_memberships_professional_associations = llm_gen(
                            query='professional_associations', 
                            description='''Professional associations that the business, organization, or individual belongs to, including relevant membership names and affiliations.''', 
                            website_text=website_text
                        )
                        llm_business_memberships_industry_memberships = llm_gen(
                            query='industry_memberships', 
                            description='''Memberships in industry-specific organizations, trade groups, chambers, or professional networks relevant to the business or its field.''', 
                            website_text=website_text
                        )
                        llm_business_memberships_botanical_societies = llm_gen(
                            query='botanical_societies', 
                            description='''Memberships or affiliations with botanical societies and organizations focused on botany, plant science, horticulture, or related fields.''', 
                            website_text=website_text
                        )
                        llm_business_memberships_herbal_associations = llm_gen(
                            query='herbal_associations', 
                            description='''Memberships or affiliations with herbal associations and organizations focused on herbalism, medicinal plants, phytotherapy, or related practices.''', 
                            website_text=website_text
                        )

                        # 26. Policies
                        llm_business_policies_privacy_policy = llm_gen(
                            query='privacy_policy', 
                            description='''A description of how the business collects, uses, stores, shares, and protects customers’ personal information, including any applicable privacy rights and choices.''', 
                            website_text=website_text
                        )
                        llm_business_policies_shipping_policy = llm_gen(
                            query='shipping_policy', 
                            description='''A description of the business’s shipping methods, delivery times, shipping costs, service areas, order processing times, and any shipping restrictions or conditions.''', 
                            website_text=website_text
                        )
                        llm_business_policies_returns_policy = llm_gen(
                            query='returns_policy', 
                            description='''A description of the business’s rules and procedures for returning products, including eligibility requirements, return timeframes, conditions, exclusions, and the return process.''', 
                            website_text=website_text
                        )
                        llm_business_policies_refund_policy = llm_gen(
                            query='refund_policy', 
                            description='''A description of when and how customers can receive refunds, including eligible circumstances, refund methods, processing times, deductions, and any applicable exclusions.''', 
                            website_text=website_text
                        )
                        llm_business_policies_sustainability_policy = llm_gen(
                            query='sustainability_policy', 
                            description='''A description of the business’s environmental and sustainability practices, commitments, initiatives, and policies relating to products, packaging, operations, sourcing, and waste.''', 
                            website_text=website_text
                        )
                        llm_business_policies_accessibility_policy = llm_gen(
                            query='accessibility_policy', 
                            description='''A description of the business’s commitment to accessibility, including accessible products, services, website features, accommodations, and how customers can request accessibility assistance.''', 
                            website_text=website_text
                        )

                        # 27. Languages
                        llm_business_languages_languages = llm_gen(
                            query='languages', 
                            description='''Identifies the languages supported by the business, website, or service, including the primary language and any additional languages available to customers.''', 
                            website_text=website_text
                        )
                        llm_business_languages_multilingual_support = llm_gen(
                            query='multilingual_support', 
                            description='''Indicates whether the business provides multilingual support, such as customer service, website content, staff assistance, or other services in multiple languages.''', 
                            website_text=website_text
                        )

                        # 28. Payment & Commerce
                        llm_business_commerce_accepted_payment_methods = llm_gen(
                            query='accepted_payment_methods', 
                            description='''The payment methods accepted by the business for purchases, such as credit cards, debit cards, PayPal, bank transfers, digital wallets, cash on delivery, or other supported payment options.''', 
                            website_text=website_text
                        )
                        llm_business_commerce_currencies = llm_gen(
                            query='currencies', 
                            description='''The currencies supported by the business for pricing, payments, and transactions, including the applicable currency codes or names.''', 
                            website_text=website_text
                        )
                        llm_business_commerce_online_store = llm_gen(
                            query='online_store', 
                            description='''Indicates whether the business operates an online store where customers can browse and purchase products or services through the website.''', 
                            website_text=website_text
                        )
                        llm_business_commerce_ecommerce = llm_gen(
                            query='ecommerce', 
                            description='''Information about the business’s ecommerce capabilities, including whether it sells products or services online and provides functionality for online purchasing and transactions.''', 
                            website_text=website_text
                        )

                        # 29. Shipping
                        llm_business_shipping_shipping_countries = llm_gen(
                            query='shipping_countries', 
                            description='''The countries where the business offers shipping or delivery for its products or services.''', 
                            website_text=website_text
                        )
                        llm_business_shipping_shipping_methods = llm_gen(
                            query='shipping_methods', 
                            description='''The available methods or options for shipping orders, such as standard, express, or expedited shipping.''', 
                            website_text=website_text
                        )
                        llm_business_shipping_international_shipping = llm_gen(
                            query='international_shipping', 
                            description='''Information about shipping orders internationally, including supported destinations, requirements, and any applicable conditions.''', 
                            website_text=website_text
                        )
                        llm_business_shipping_local_delivery = llm_gen(
                            query='local_delivery', 
                            description='''Information about delivery options available within the business's local service area, including coverage and delivery conditions.''', 
                            website_text=website_text
                        )

                        ###
                        output_items = []
                        output_item = parse_utils.organizations__business_create(
                            business_gmap_label = label,
                            business_gmap_name = name,
                            business_gmap_website = website,
                            ###
                            business_is_category_herbs = llm_business_is_category_herbs,
                            ###
                            business_name_official = llm_business_name_official,
                            business_name_legal = llm_business_name_legal,
                            business_name_trade = llm_business_name_trade,
                            business_slogan = llm_business_slogan,
                            business_description = llm_business_description,
                            business_description_short = llm_business_description_short,
                            business_founded_year = llm_business_founded_year,
                            business_founding_story = llm_business_founding_story,
                            business_founder_names = llm_business_founder_names,
                            business_ownership_type = llm_business_ownership_type,
                            business_company_type = llm_business_company_type,
                            business_status = llm_business_status,
                            business_mission = llm_business_mission,
                            business_vision = llm_business_vision,
                            business_core_values = llm_business_core_values,
                            ###
                            business_type_primary = llm_business_type_primary,
                            business_type_secondary = llm_business_type_secondary,
                            business_industry = llm_business_industry,
                            business_niche = llm_business_niche,
                            business_model = llm_business_model,
                            ###
                            business_website = llm_business_website,
                            business_email = llm_business_email,
                            business_email_customer_service = llm_business_customer_service_email,
                            business_email_wholesale = llm_business_wholesale_email,
                            business_email_media = llm_business_media_email,
                            business_phone = llm_business_phone,
                            business_whatsapp = llm_business_whatsapp,
                            business_fax = llm_business_fax,
                            business_contact_form = llm_business_contact_form,
                            ###
                            business_headquarters = llm_business_headquarters,
                            business_address = llm_business_address,
                            business_city = llm_business_city,
                            business_state = llm_business_state,
                            business_region = llm_business_region,
                            business_country = llm_business_country,
                            business_postal_code = llm_business_postal_code,
                            business_latitude = llm_business_latitude,
                            business_longitude = llm_business_longitude,
                            business_additional_locations = llm_business_additional_locations,
                            business_farm_locations = llm_business_farm_locations,
                            business_nursery_locations = llm_business_nursery_locations,
                            business_factory_locations = llm_business_factory_locations,
                            business_laboratory_locations = llm_business_laboratory_locations,
                            business_warehouse_locations = llm_business_warehouse_locations,
                            business_retail_locations = llm_business_retail_locations,
                            ###
                            business_opening_hours = llm_business_opening_hours,
                            business_seasonal_hours = llm_business_seasonal_hours,
                            business_appointment_required = llm_business_appointment_required,
                            business_walk_in_available = llm_business_walk_in_available,
                            business_visitor_access = llm_business_visitor_access,
                            ###
                            business_medicinal_plants = llm_business_medicinal_plants,
                            business_primary_medicinal_plants = llm_business_primary_medicinal_plants,
                            business_specialty_plants = llm_business_specialty_plants,
                            business_native_plants = llm_business_native_plants,
                            business_rare_plants = llm_business_rare_plants,
                            business_medicinal_plant_categories = llm_business_medicinal_plant_categories,
                            business_botanical_collection_size = llm_business_botanical_collection_size,
                            ###
                            business_grows = llm_business_grows,
                            business_cultivates = llm_business_cultivates,
                            business_propagates = llm_business_propagates,
                            business_researches = llm_business_researches,
                            business_sells = llm_business_sells,
                            business_distributes = llm_business_distributes,
                            business_exports = llm_business_exports,
                            business_imports = llm_business_imports,
                            business_wild_harvests = llm_business_wild_harvests,
                            business_conserves = llm_business_conserves,
                            business_teaches = llm_business_teaches,
                            business_uses_in_products = llm_business_uses_in_products,
                            ###
                            business_products = llm_business_products,
                            business_product_categories = llm_business_product_categories,
                            business_flagship_products = llm_business_flagship_products,
                            business_product_forms = llm_business_product_forms,
                            business_herbal_teas = llm_business_herbal_teas,
                            business_tinctures = llm_business_tinctures,
                            business_extracts = llm_business_extracts,
                            business_essential_oils = llm_business_essential_oils,
                            business_capsules = llm_business_capsules,
                            business_powders = llm_business_powders,
                            business_dried_herbs = llm_business_dried_herbs,
                            business_fresh_herbs = llm_business_fresh_herbs,
                            business_seeds = llm_business_seeds,
                            business_seedlings = llm_business_seedlings,
                            business_roots = llm_business_roots,
                            business_bark = llm_business_bark,
                            business_flowers = llm_business_flowers,
                            business_fruits = llm_business_fruits,
                            business_resins = llm_business_resins,
                            business_cosmetics = llm_business_cosmetics,
                            business_soaps = llm_business_soaps,
                            business_creams = llm_business_creams,
                            business_salves = llm_business_salves,
                            business_syrups = llm_business_syrups,
                            ###
                            business_botanical_name = llm_business_botanical_name,
                            business_common_name = llm_business_common_name,
                            business_plant_part = llm_business_plant_part,
                            business_extraction_method = llm_business_extraction_method,
                            business_preparation_method = llm_business_preparation_method,
                            business_ingredients = llm_business_ingredients,
                            business_packaging = llm_business_packaging,
                            business_package_sizes = llm_business_package_sizes,
                            business_concentration = llm_business_concentration,
                            business_organic_product = llm_business_organic_product,
                            business_private_label = llm_business_private_label,
                            business_wholesale = llm_business_wholesale,
                            business_retail = llm_business_retail,
                            ###
                            business_herbal_consultation = llm_business_herbal_consultation,
                            business_herbal_clinic = llm_business_herbal_clinic,
                            business_medicinal_plant_consulting = llm_business_medicinal_plant_consulting,
                            business_plant_identification = llm_business_plant_identification,
                            business_botanical_identification = llm_business_botanical_identification,
                            business_cultivation_consulting = llm_business_cultivation_consulting,
                            business_contract_growing = llm_business_contract_growing,
                            business_contract_manufacturing = llm_business_contract_manufacturing,
                            business_private_label_manufacturing = llm_business_private_label_manufacturing,
                            business_extraction_services = llm_business_extraction_services,
                            business_drying_services = llm_business_drying_services,
                            business_milling = llm_business_milling,
                            business_grinding = llm_business_grinding,
                            business_packaging_service = llm_business_packaging_service,
                            business_export_services = llm_business_export_services,
                            business_laboratory_testing = llm_business_laboratory_testing,
                            business_formulation = llm_business_formulation,
                            business_research_services = llm_business_research_services,
                            business_education = llm_business_education,
                            business_workshops = llm_business_workshops,
                            business_courses = llm_business_courses,
                            business_farm_tours = llm_business_farm_tours,
                            business_botanical_tours = llm_business_botanical_tours,
                            ###
                            business_cultivation_methods = llm_business_cultivation_methods,
                            business_organic_cultivation = llm_business_organic_cultivation,
                            business_regenerative = llm_business_regenerative,
                            business_biodynamic = llm_business_biodynamic,
                            business_permaculture = llm_business_permaculture,
                            business_agroforestry = llm_business_agroforestry,
                            business_greenhouse = llm_business_greenhouse,
                            business_indoor = llm_business_indoor,
                            business_outdoor = llm_business_outdoor,
                            business_wild_harvesting = llm_business_wild_harvesting,
                            business_sustainable_wild_harvesting = llm_business_sustainable_wild_harvesting,
                            business_propagation_methods = llm_business_propagation_methods,
                            business_irrigation = llm_business_irrigation,
                            business_fertilization = llm_business_fertilization,
                            business_soil_management = llm_business_soil_management,
                            business_pest_management = llm_business_pest_management,
                            business_harvest_methods = llm_business_harvest_methods,
                            business_harvest_season = llm_business_harvest_season,
                            ###
                            business_manufacturing = llm_business_manufacturing,
                            business_processing = llm_business_processing,
                            business_extraction = llm_business_extraction,
                            business_distillation = llm_business_distillation,
                            business_fermentation = llm_business_fermentation,
                            business_drying = llm_business_drying,
                            business_manufacturing_milling = llm_business_manufacturing_milling,
                            business_manufacturing_grinding = llm_business_manufacturing_grinding,
                            business_blending = llm_business_blending,
                            business_manufacturing_formulation = llm_business_manufacturing_formulation,
                            business_encapsulation = llm_business_encapsulation,
                            business_manufacturing_packaging = llm_business_manufacturing_packaging,
                            business_quality_testing = llm_business_quality_testing,
                            business_batch_testing = llm_business_batch_testing,
                            business_traceability = llm_business_traceability,
                            ###
                            business_facilities_farms = llm_business_facilities_farms,
                            business_facilities_nurseries = llm_business_facilities_nurseries,
                            business_facilities_laboratories = llm_business_facilities_laboratories,
                            business_facilities_factories = llm_business_facilities_factories,
                            business_facilities_warehouses = llm_business_facilities_warehouses,
                            business_facilities_botanical_gardens = llm_business_facilities_botanical_gardens,
                            business_facilities_greenhouses = llm_business_facilities_greenhouses,
                            business_facilities_visitor_centers = llm_business_facilities_visitor_centers,
                            business_facilities_research_centers = llm_business_facilities_research_centers,
                            business_facilities_education_centers = llm_business_facilities_education_centers,
                            business_facilities_clinics = llm_business_facilities_clinics,
                            business_facilities_retail_stores = llm_business_facilities_retail_stores,
                            ###
                            business_certifications_certifications = llm_business_certifications_certifications,
                            business_certifications_certification_name = llm_business_certifications_certification_name,
                            business_certifications_certification_number = llm_business_certifications_certification_number,
                            business_certifications_issuing_organization = llm_business_certifications_issuing_organization,
                            business_certifications_issue_date = llm_business_certifications_issue_date,
                            business_certifications_expiry_date = llm_business_certifications_expiry_date,
                            business_certifications_certification_scope = llm_business_certifications_certification_scope,
                            ###
                            business_quality_quality_control = llm_business_quality_quality_control,
                            business_quality_laboratory_testing = llm_business_quality_laboratory_testing,
                            business_quality_batch_testing = llm_business_quality_batch_testing,
                            business_quality_third_party_testing = llm_business_quality_third_party_testing,
                            business_quality_traceability = llm_business_quality_traceability,
                            business_quality_quality_management_system = llm_business_quality_quality_management_system,
                            ###
                            business_sustainability_sustainability_policy = llm_business_sustainability_sustainability_policy,
                            business_sustainability_conservation = llm_business_sustainability_conservation,
                            business_sustainability_biodiversity = llm_business_sustainability_biodiversity,
                            business_sustainability_regenerative_agriculture = llm_business_sustainability_regenerative_agriculture,
                            business_sustainability_ethical_sourcing = llm_business_sustainability_ethical_sourcing,
                            business_sustainability_fair_trade = llm_business_sustainability_fair_trade,
                            business_sustainability_community_projects = llm_business_sustainability_community_projects,
                            business_sustainability_indigenous_partnerships = llm_business_sustainability_indigenous_partnerships,
                            business_sustainability_local_sourcing = llm_business_sustainability_local_sourcing,
                            business_sustainability_recyclable_packaging = llm_business_sustainability_recyclable_packaging,
                            business_sustainability_carbon_reduction = llm_business_sustainability_carbon_reduction,
                            business_sustainability_water_conservation = llm_business_sustainability_water_conservation,
                            ###
                            business_research_research_programs = llm_business_research_research_programs,
                            business_research_research_projects = llm_business_research_research_projects,
                            business_research_publications = llm_business_research_publications,
                            business_research_patents = llm_business_research_patents,
                            business_research_university_partnerships = llm_business_research_university_partnerships,
                            business_research_clinical_trials = llm_business_research_clinical_trials,
                            business_research_ethnobotanical_research = llm_business_research_ethnobotanical_research,
                            business_research_pharmacognosy = llm_business_research_pharmacognosy,
                            business_research_phytochemistry = llm_business_research_phytochemistry,
                            business_research_plant_breeding = llm_business_research_plant_breeding,
                            ###
                            business_education_courses = llm_business_education_courses,
                            # business_education_workshops = llm_business_education_workshops,
                            business_education_webinars = llm_business_education_webinars,
                            # business_education_apprenticeships = llm_business_education_apprenticeships,
                            business_education_lectures = llm_business_education_lectures,
                            # business_education_botanical_walks = llm_business_education_botanical_walks,
                            # business_education_farm_tours = llm_business_education_farm_tours,
                            # business_education_certifications_offered = llm_business_education_certifications_offered,
                            ###
                            business_traditional_medicine_systems_ayurveda = llm_business_traditional_medicine_systems_ayurveda,
                            business_traditional_medicine_systems_traditional_chinese_medicine = llm_business_traditional_medicine_systems_traditional_chinese_medicine,
                            business_traditional_medicine_systems_western_herbalism = llm_business_traditional_medicine_systems_western_herbalism,
                            business_traditional_medicine_systems_unani = llm_business_traditional_medicine_systems_unani,
                            business_traditional_medicine_systems_kampo = llm_business_traditional_medicine_systems_kampo,
                            business_traditional_medicine_systems_tibetan_medicine = llm_business_traditional_medicine_systems_tibetan_medicine,
                            business_traditional_medicine_systems_indigenous_medicine = llm_business_traditional_medicine_systems_indigenous_medicine,
                            business_traditional_medicine_systems_african_traditional_medicine = llm_business_traditional_medicine_systems_african_traditional_medicine,
                            ###
                            business_expertise_expertise_topics = llm_business_expertise_expertise_topics,
                            business_expertise_medicinal_plant_cultivation = llm_business_expertise_medicinal_plant_cultivation,
                            business_expertise_herbal_formulation = llm_business_expertise_herbal_formulation,
                            business_expertise_ethnobotany = llm_business_expertise_ethnobotany,
                            business_expertise_pharmacognosy = llm_business_expertise_pharmacognosy,
                            # business_expertise_botanical_identification = llm_business_expertise_botanical_identification,
                            business_expertise_herbal_medicine = llm_business_expertise_herbal_medicine,
                            business_expertise_conservation = llm_business_expertise_conservation,
                            # business_expertise_plant_propagation = llm_business_expertise_plant_propagation,

                            business_people_founders = llm_business_people_founders,
                            business_people_owners = llm_business_people_owners,
                            business_people_ceo = llm_business_people_ceo,
                            business_people_president = llm_business_people_president,
                            business_people_director = llm_business_people_director,
                            business_people_botanists = llm_business_people_botanists,
                            business_people_herbalists = llm_business_people_herbalists,
                            # business_people_researchers = llm_business_people_researchers,
                            # business_people_agronomists = llm_business_people_agronomists,
                            # business_people_pharmacists = llm_business_people_pharmacists,
                            business_people_educators = llm_business_people_educators,
                            # business_people_laboratory_directors = llm_business_people_laboratory_directors,
                            business_people_farm_managers = llm_business_people_farm_managers,

                            business_markets_customer_types = llm_business_markets_customer_types,
                            business_markets_industries_served = llm_business_markets_industries_served,
                            business_markets_export_markets = llm_business_markets_export_markets,
                            # business_markets_import_markets = llm_business_markets_import_markets,
                            business_markets_countries_served = llm_business_markets_countries_served,
                            business_markets_regions_served = llm_business_markets_regions_served,
                            business_markets_international_shipping = llm_business_markets_international_shipping,
                            business_markets_wholesale_available = llm_business_markets_wholesale_available,
                            business_markets_retail_available = llm_business_markets_retail_available,
                            business_markets_private_label_available = llm_business_markets_private_label_available,

                            business_online_presence_facebook = llm_business_online_presence_facebook,
                            business_online_presence_instagram = llm_business_online_presence_instagram,
                            business_online_presence_linkedin = llm_business_online_presence_linkedin,
                            business_online_presence_youtube = llm_business_online_presence_youtube,
                            business_online_presence_x = llm_business_online_presence_x,
                            business_online_presence_pinterest = llm_business_online_presence_pinterest,
                            business_online_presence_tiktok = llm_business_online_presence_tiktok,
                            # business_online_presence_github = llm_business_online_presence_github,
                            # business_online_presence_wikipedia = llm_business_online_presence_wikipedia,

                            business_awards_awards = llm_business_awards_awards,
                            # business_awards_award_name = llm_business_awards_award_name,
                            # business_awards_award_year = llm_business_awards_award_year,
                            # business_awards_awarding_organization = llm_business_awards_awarding_organization,

                            # business_memberships_professional_associations = llm_business_memberships_professional_associations,
                            # business_memberships_industry_memberships = llm_business_memberships_industry_memberships,
                            # business_memberships_botanical_societies = llm_business_memberships_botanical_societies,
                            # business_memberships_herbal_associations = llm_business_memberships_herbal_associations,

                            business_policies_privacy_policy = llm_business_policies_privacy_policy,
                            business_policies_shipping_policy = llm_business_policies_shipping_policy,
                            # business_policies_returns_policy = llm_business_policies_returns_policy,
                            # business_policies_refund_policy = llm_business_policies_refund_policy,
                            business_policies_sustainability_policy = llm_business_policies_sustainability_policy,
                            business_policies_accessibility_policy = llm_business_policies_accessibility_policy,

                            business_languages_languages = llm_business_languages_languages,
                            business_languages_multilingual_support = llm_business_languages_multilingual_support,

                            business_commerce_accepted_payment_methods = llm_business_commerce_accepted_payment_methods,
                            business_commerce_currencies = llm_business_commerce_currencies,
                            business_commerce_online_store = llm_business_commerce_online_store,
                            business_commerce_ecommerce = llm_business_commerce_ecommerce,

                            business_shipping_shipping_countries = llm_business_shipping_shipping_countries,
                            business_shipping_shipping_methods = llm_business_shipping_shipping_methods,
                            business_shipping_international_shipping = llm_business_shipping_international_shipping,
                            business_shipping_local_delivery = llm_business_shipping_local_delivery,

                            source_name = 'Website',
                            source_acronym = 'WEBSITE',
                        )
                        output_items.append(output_item)
                        io.json_write(output_filepath, output_items)
                        ###
                        item = output_items[0]
                        print(output_filepath)
                        none_count = 0
                        empty_count = 0
                        value_count = 0
                        for key, val in item.items():
                            if val == None: none_count += 1
                            elif val == '': empty_count += 1
                            else: value_count += 1
                        total_count = none_count + empty_count + value_count
                        print(f'NONE: {none_count}/{total_count} - {none_count/total_count*100}')
                        print(f'EMPTY: {empty_count}/{total_count} - {empty_count/total_count*100}')
                        print(f'VALUE: {value_count}/{total_count} - {value_count/total_count*100}')
                        # quit()

def parse_website():
    start = 0
    end = 10
    ###
    output_folderpath = f'{g.DATA_FOLDERPATH}/organizations/parse/website/json'
    # try: shutil.rmtree(output_folderpath)
    # except: pass
    io.folders_recursive_gen(output_folderpath)
    ###
    input_foldername = f'{HUB_FOLDERPATH}/fetch/gmap/america/places'.replace(' ', '_')
    input_filenames = sorted(os.listdir(input_foldername))
    i = 0
    for input_filename in input_filenames[start:end]:
        print(f'{start+i}/{end}')
        i += 1
        input_filename_base = input_filename.split('.')[0].strip()
        input_filepath = f'{input_foldername}/{input_filename}'
        with open(input_filepath, encoding="utf-8") as f: rows = f.read().strip().split('\n')
        for row in rows:
            values = row.split('~')
            if values != [] and values != ['']:
                gmap_label = values[0]
                website = values[2]
                gmap_name = values[4]
                slug = to_slug(gmap_label)
                print(f'label: {gmap_label}')
                print(f'website: {website}')
                print(f'name: {gmap_name}')
                print(f'slug: {slug}')
                print(f'***************************************')
                print()

                website_filepath = f'{HUB_FOLDERPATH}/fetch/websites/america/places/{input_filename_base}/{slug}.html'
                output_filepath = f'{output_folderpath}/{slug}.json'
                try: html = io.file_read(website_filepath)
                except: html = ''
                if html != '':
                    soup = BeautifulSoup(html, "html.parser")
                    website_text = soup.get_text(separator="\n", strip=True)
                    if website_text.strip() != '':

                        fields_data = parse_organizations_data.data
                        output_items = []
                        output_item = {}
                        for field_item in fields_data:
                            reply = ''
                            if field_item['field_name'] == 'business_gmap_name_raw':
                                reply = gmap_name
                            elif field_item['field_type'] == 'bool':
                                reply = llm_bool_gen(
                                    query=field_item['field_query'],
                                    description=field_item['field_description'],
                                    website_text=website_text
                                )
                            elif field_item['field_type'] == 'text':
                                reply = llm_gen(
                                    query=field_item['field_query'],
                                    description=field_item['field_description'],
                                    website_text=website_text
                                )

                            key = field_item['field_name']
                            val = reply
                            output_item[key] = val

                        output_items.append(output_item)
                        io.json_write(output_filepath, output_items)
                        ###
                        item = output_items[0]
                        print(output_filepath)
                        none_count = 0
                        empty_count = 0
                        value_count = 0
                        for key, val in item.items():
                            if val == None: none_count += 1
                            elif val == '': empty_count += 1
                            else: value_count += 1
                        total_count = none_count + empty_count + value_count
                        print(f'NONE: {none_count}/{total_count} - {none_count/total_count*100}')
                        print(f'EMPTY: {empty_count}/{total_count} - {empty_count/total_count*100}')
                        print(f'VALUE: {value_count}/{total_count} - {value_count/total_count*100}')
                        ###
                        # quit()

                continue
                ###
                llm_business_name_official = ''
                llm_business_name_legal = ''
                llm_business_name_trade = ''
                llm_business_description = ''
                llm_business_description_short = ''
                llm_business_founded_year = ''
                llm_business_founding_story = ''
                llm_business_founder_names = ''
                llm_business_ownership_type = ''
                llm_business_company_type = ''
                llm_business_status = ''
                llm_business_mission = ''
                llm_business_vision = ''
                llm_business_core_values = ''
                # 2. Business Classification
                llm_business_type_primary = ''
                llm_business_type_secondary = ''
                llm_business_industry = ''
                llm_business_niche = ''
                llm_business_model = ''
                # 3. Contact Information
                llm_business_website = ''
                llm_business_email = ''
                llm_business_fax = ''
                llm_business_whatsapp = ''
                llm_business_contact_form = ''
                llm_business_customer_service_email = ''
                llm_business_wholesale_email = ''
                llm_business_media_email = ''
                # 4. Locations
                llm_business_headquarters = ''
                llm_business_address = ''
                llm_business_city = ''
                llm_business_state = ''
                llm_business_region = ''
                llm_business_country = ''
                llm_business_postal_code = ''
                llm_business_latitude = ''
                llm_business_longitude = ''
                llm_business_additional_locations = ''
                llm_business_farm_locations = ''
                llm_business_nursery_locations = ''
                llm_business_factory_locations = ''
                llm_business_laboratory_locations = ''
                llm_business_warehouse_locations = ''
                llm_business_retail_locations = ''
                # 5. Opening Information
                llm_business_opening_hours = ''
                llm_business_seasonal_hours = ''
                llm_business_appointment_required = ''
                llm_business_walk_in_available = ''
                llm_business_visitor_access = ''
                llm_business_medicinal_plants = ''
                llm_business_primary_medicinal_plants = ''
                llm_business_specialty_plants = ''
                llm_business_native_plants = ''
                llm_business_rare_plants = ''
                llm_business_medicinal_plant_categories = ''
                llm_business_botanical_collection_size = ''

                llm_business_grows = ''
                llm_business_cultivates = ''
                llm_business_propagates = ''
                llm_business_researches = ''
                llm_business_sells = ''
                llm_business_distributes = ''
                llm_business_exports = ''
                llm_business_imports = ''
                llm_business_wild_harvests = ''
                llm_business_conserves = ''
                llm_business_teaches = ''
                llm_business_uses_in_products = ''

                llm_business_products = ''
                llm_business_product_categories = ''
                llm_business_flagship_products = ''
                llm_business_product_forms = ''
                llm_business_herbal_teas = ''
                llm_business_tinctures = ''
                llm_business_extracts = ''
                llm_business_essential_oils = ''
                llm_business_capsules = ''
                llm_business_powders = ''
                llm_business_dried_herbs = ''
                llm_business_fresh_herbs = ''
                llm_business_seeds = ''
                llm_business_seedlings = ''
                llm_business_roots = ''
                llm_business_bark = ''
                llm_business_flowers = ''
                llm_business_fruits = ''
                llm_business_resins = ''
                llm_business_cosmetics = ''
                llm_business_soaps = ''
                llm_business_creams = ''
                llm_business_salves = ''
                llm_business_syrups = ''

                llm_business_herbal_consultation = ''
                llm_business_herbal_clinic = ''
                llm_business_medicinal_plant_consulting = ''
                llm_business_plant_identification = ''
                llm_business_botanical_identification = ''
                llm_business_cultivation_consulting = ''
                llm_business_contract_growing = ''
                llm_business_contract_manufacturing = ''
                llm_business_private_label_manufacturing = ''
                llm_business_extraction_services = ''
                llm_business_drying_services = ''
                llm_business_milling = ''
                llm_business_grinding = ''
                llm_business_packaging = ''
                llm_business_export_services = ''
                llm_business_laboratory_testing = ''
                llm_business_formulation = ''
                llm_business_research_services = ''
                llm_business_education = ''
                llm_business_workshops = ''
                llm_business_courses = ''
                llm_business_farm_tours = ''
                llm_business_botanical_tours = ''

                llm_business_botanical_name = ''
                llm_business_common_name = ''
                llm_business_plant_part = ''
                llm_business_extraction_method = ''
                llm_business_preparation_method = ''
                llm_business_ingredients = ''
                llm_business_packaging_service = ''
                llm_business_package_sizes = ''
                llm_business_concentration = ''
                llm_business_organic_product = ''
                llm_business_private_label = ''
                llm_business_wholesale = ''
                llm_business_retail = ''

                llm_business_cultivation_methods = ''
                llm_business_organic_cultivation = ''
                llm_business_regenerative = ''
                llm_business_biodynamic = ''
                llm_business_permaculture = ''
                llm_business_agroforestry = ''
                llm_business_greenhouse = ''
                llm_business_indoor = ''
                llm_business_outdoor = ''
                llm_business_wild_harvesting = ''
                llm_business_sustainable_wild_harvesting = ''
                llm_business_propagation_methods = ''
                llm_business_irrigation = ''
                llm_business_fertilization = ''
                llm_business_soil_management = ''
                llm_business_pest_management = ''
                llm_business_harvest_methods = ''
                llm_business_harvest_season = ''

                llm_business_manufacturing = ''
                llm_business_processing = ''
                llm_business_extraction = ''
                llm_business_distillation = ''
                llm_business_fermentation = ''
                llm_business_drying = ''
                llm_business_manufacturing_milling = ''
                llm_business_manufacturing_grinding = ''
                llm_business_blending = ''
                llm_business_manufacturing_formulation = ''
                llm_business_encapsulation = ''
                llm_business_manufacturing_packaging = ''
                llm_business_quality_testing = ''
                llm_business_batch_testing = ''
                llm_business_traceability = ''

                llm_business_facilities_farms = ''
                llm_business_facilities_nurseries = ''
                llm_business_facilities_laboratories = ''
                llm_business_facilities_factories = ''
                llm_business_facilities_warehouses = ''
                llm_business_facilities_botanical_gardens = ''
                llm_business_facilities_greenhouses = ''
                llm_business_facilities_visitor_centers = ''
                llm_business_facilities_research_centers = ''
                llm_business_facilities_education_centers = ''
                llm_business_facilities_clinics = ''
                llm_business_facilities_retail_stores = ''

                llm_business_certifications_certifications = ''
                llm_business_certifications_certification_name = ''
                llm_business_certifications_certification_number = ''
                llm_business_certifications_issuing_organization = ''
                llm_business_certifications_issue_date = ''
                llm_business_certifications_expiry_date = ''
                llm_business_certifications_certification_scope = ''

                llm_business_quality_quality_control = ''
                llm_business_quality_laboratory_testing = ''
                llm_business_quality_batch_testing = ''
                llm_business_quality_third_party_testing = ''
                llm_business_quality_traceability = ''
                llm_business_quality_quality_management_system = ''

                llm_business_sustainability_sustainability_policy = ''
                llm_business_sustainability_conservation = ''
                llm_business_sustainability_biodiversity = ''
                llm_business_sustainability_regenerative_agriculture = ''
                llm_business_sustainability_ethical_sourcing = ''
                llm_business_sustainability_fair_trade = ''
                llm_business_sustainability_community_projects = ''
                llm_business_sustainability_indigenous_partnerships = ''
                llm_business_sustainability_local_sourcing = ''
                llm_business_sustainability_recyclable_packaging = ''
                llm_business_sustainability_carbon_reduction = ''
                llm_business_sustainability_water_conservation = ''

                llm_business_research_research_programs = ''
                llm_business_research_research_projects = ''
                llm_business_research_publications = ''
                llm_business_research_patents = ''
                llm_business_research_university_partnerships = ''
                llm_business_research_clinical_trials = ''
                llm_business_research_ethnobotanical_research = ''
                llm_business_research_pharmacognosy = ''
                llm_business_research_phytochemistry = ''
                llm_business_research_plant_breeding = ''

                llm_business_education_courses = ''
                llm_business_education_workshops = ''
                llm_business_education_webinars = ''
                llm_business_education_apprenticeships = ''
                llm_business_education_lectures = ''
                llm_business_education_botanical_walks = ''
                llm_business_education_farm_tours = ''
                llm_business_education_certifications_offered = ''

                llm_business_traditional_medicine_systems_ayurveda = ''
                llm_business_traditional_medicine_systems_traditional_chinese_medicine = ''
                llm_business_traditional_medicine_systems_western_herbalism = ''
                llm_business_traditional_medicine_systems_unani = ''
                llm_business_traditional_medicine_systems_kampo = ''
                llm_business_traditional_medicine_systems_tibetan_medicine = ''
                llm_business_traditional_medicine_systems_indigenous_medicine = ''
                llm_business_traditional_medicine_systems_african_traditional_medicine = ''

                llm_business_expertise_expertise_topics = ''
                llm_business_expertise_medicinal_plant_cultivation = ''
                llm_business_expertise_herbal_formulation = ''
                llm_business_expertise_ethnobotany = ''
                llm_business_expertise_pharmacognosy = ''
                llm_business_expertise_botanical_identification = ''
                llm_business_expertise_herbal_medicine = ''
                llm_business_expertise_conservation = ''
                llm_business_expertise_plant_propagation = ''

                llm_business_people_founders = ''
                llm_business_people_owners = ''
                llm_business_people_ceo = ''
                llm_business_people_president = ''
                llm_business_people_director = ''
                llm_business_people_botanists = ''
                llm_business_people_herbalists = ''
                llm_business_people_researchers = ''
                llm_business_people_agronomists = ''
                llm_business_people_pharmacists = ''
                llm_business_people_educators = ''
                llm_business_people_laboratory_directors = ''
                llm_business_people_farm_managers = ''

                llm_business_markets_customer_types = ''
                llm_business_markets_industries_served = ''
                llm_business_markets_export_markets = ''
                llm_business_markets_import_markets = ''
                llm_business_markets_countries_served = ''
                llm_business_markets_regions_served = ''
                llm_business_markets_international_shipping = ''
                llm_business_markets_wholesale_available = ''
                llm_business_markets_retail_available = ''
                llm_business_markets_private_label_available = ''

                llm_business_online_presence_facebook = ''
                llm_business_online_presence_instagram = ''
                llm_business_online_presence_linkedin = ''
                llm_business_online_presence_youtube = ''
                llm_business_online_presence_x = ''
                llm_business_online_presence_pinterest = ''
                llm_business_online_presence_tiktok = ''
                llm_business_online_presence_github = ''
                llm_business_online_presence_wikipedia = ''

                llm_business_awards_awards = ''
                llm_business_awards_award_name = ''
                llm_business_awards_award_year = ''
                llm_business_awards_awarding_organization = ''

                llm_business_memberships_professional_associations = ''
                llm_business_memberships_industry_memberships = ''
                llm_business_memberships_botanical_societies = ''
                llm_business_memberships_herbal_associations = ''

                llm_business_policies_privacy_policy = ''
                llm_business_policies_shipping_policy = ''
                llm_business_policies_returns_policy = ''
                llm_business_policies_refund_policy = ''
                llm_business_policies_sustainability_policy = ''
                llm_business_policies_accessibility_policy = ''

                llm_business_languages_languages = ''
                llm_business_languages_multilingual_support = ''

                llm_business_commerce_accepted_payment_methods = ''
                llm_business_commerce_currencies = ''
                llm_business_commerce_online_store = ''
                llm_business_commerce_ecommerce = ''

                llm_business_shipping_shipping_countries = ''
                llm_business_shipping_shipping_methods = ''
                llm_business_shipping_international_shipping = ''
                llm_business_shipping_local_delivery = ''

                ###
                website_filepath = f'{g.DATA_FOLDERPATH}/organizations/fetch/websites/america/places/{input_filename_base}/{slug}.html'
                output_filepath = f'{output_folderpath}/{slug}.json'
                try: html = io.file_read(website_filepath)
                except: html = ''
                if html != '':
                    soup = BeautifulSoup(html, "html.parser")
                    website_text = soup.get_text(separator="\n", strip=True)
                    if website_text.strip() != '':

                        ###
                        llm_business_name_official = llm_gen(
                            query='official business name', 
                            description='Official business name exactly as shown on the website', 
                            website_text=website_text
                            )
                        llm_business_name_legal = llm_gen(
                            query='legal business name', 
                            description='Registered legal business name if published', 
                            website_text=website_text
                            )
                        llm_business_name_trade = llm_gen(
                            query='trading business name', 
                            description='Public trading or DBA name', 
                            website_text=website_text
                            )
                        llm_business_description = llm_gen(
                            query='business description', 
                            description='Main factual description of the company', 
                            website_text=website_text
                            )
                        llm_business_description_short = llm_gen(
                            query='short business description', 
                            description='Short summary (1–2 sentences)', 
                            website_text=website_text
                            )
                        llm_business_founded_year = llm_gen(
                            query='business year founded', 
                            description='Year the business was founded', 
                            website_text=website_text
                            )
                        llm_business_founding_story = llm_gen(
                            query='business founding story', 
                            description='History or origin story', 
                            website_text=website_text
                            )
                        llm_business_founder_names = llm_gen(
                            query='business founder names', 
                            description='Founder(s)', 
                            website_text=website_text
                            )
                        llm_business_ownership_type = llm_gen(
                            query='business ownership type', 
                            description='Private, public, cooperative, nonprofit, family-owned, etc.', 
                            website_text=website_text
                            )
                        llm_business_company_type = llm_gen(
                            query='business company type', 
                            description='LLC, Ltd, Inc., GmbH, Cooperative, etc.', 
                            website_text=website_text
                            )
                        llm_business_status = llm_gen(
                            query='business status', 
                            description='Active, acquired, merged, closed, etc.', 
                            website_text=website_text
                            )
                        llm_business_mission = llm_gen(
                            query='business mission', 
                            description='Mission statement', 
                            website_text=website_text
                            )
                        llm_business_vision = llm_gen(
                            query='business vision', 
                            description='Vision statement', 
                            website_text=website_text
                            )
                        llm_business_core_values = llm_gen(
                            query='business core values', 
                            description='''Company's stated values''', 
                            website_text=website_text
                            )

                        # 2. Business Classification
                        llm_business_type_primary = llm_gen(
                            query='primary business type', 
                            description='''Main business role''', 
                            website_text=website_text
                            )
                        llm_business_type_secondary = llm_gen(
                            query='secondary business type', 
                            description='''Additional business roles''', 
                            website_text=website_text
                            )
                        llm_business_industry = llm_gen(
                            query='business industry', 
                            description='''Industry classification''', 
                            website_text=website_text
                            )
                        llm_business_niche = llm_gen(
                            query='business niche', 
                            description='''Specific medicinal plant niche''', 
                            website_text=website_text
                            )
                        llm_business_model = llm_gen(
                            query='business model', 
                            description='''B2B, B2C, Marketplace, Manufacturer, etc.''', 
                            website_text=website_text
                            )
                        # 3. Contact Information
                        llm_business_website = llm_gen(
                            query='website',
                            description='''The official website URL of the business. Extract the primary canonical domain used by the organization (e.g., https://www.example.com).''',
                            website_text=website_text
                        )
                        llm_business_email = llm_gen(
                            query='email',
                            description='''The primary general-purpose email address for contacting the business (e.g., info@example.com). Exclude personal employee emails unless they are the primary contact.''',
                            website_text=website_text
                        )
                        llm_business_customer_service_email = llm_gen(
                            query='customer service email',
                            description='''The dedicated email address for customer support or customer service inquiries (e.g., support@example.com).''',
                            website_text=website_text
                        )
                        llm_business_wholesale_email = llm_gen(
                            query='wholesale email',
                            description='''The dedicated email address for wholesale, bulk orders, distributors, or B2B sales inquiries (e.g., wholesale@example.com).''',
                            website_text=website_text
                        )
                        llm_business_media_email = llm_gen(
                            query='media email',
                            description='''The dedicated email address for press, media, public relations, or journalist inquiries (e.g., media@example.com or press@example.com).''',
                            website_text=website_text
                        )
                        llm_business_whatsapp = llm_gen(
                            query='whatsapp',
                            description='''The official WhatsApp contact number or WhatsApp Business link provided for customer communication.''',
                            website_text=website_text
                        )
                        llm_business_fax = llm_gen(
                            query='fax',
                            description='''The official fax number published by the business, if available.''',
                            website_text=website_text
                        )
                        llm_business_contact_form = llm_gen(
                            query='contact form',
                            description='''The URL of the official online contact form where visitors can submit inquiries.''',
                            website_text=website_text
                        )
                        # 4. Locations
                        llm_business_headquarters = llm_gen(
                            query='business headquarters', 
                            description='''The primary headquarters location of the business, including the city and country where the company is officially based.''', 
                            website_text=website_text
                        )
                        llm_business_address = llm_gen(
                            query='business address', 
                            description='''The complete street address of the business's primary location, including building number, street name, and other published address details.''', 
                            website_text=website_text
                        )
                        llm_business_city = llm_gen(
                            query='business city', 
                            description='''The city or municipality where the business or facility is located.''', 
                            website_text=website_text
                        )
                        llm_business_state = llm_gen(
                            query='business state', 
                            description='''The state, province, prefecture, or equivalent first-level administrative division where the business is located.''', 
                            website_text=website_text
                        )
                        llm_business_region = llm_gen(
                            query='business region', 
                            description='''The broader geographic or administrative region (e.g., Tuscany, Bavaria, Queensland) where the business operates.''', 
                            website_text=website_text
                        )
                        llm_business_country = llm_gen(
                            query='business country', 
                            description='''The country where the business's primary location is situated. Store using a standardized country name or ISO country code.''', 
                            website_text=website_text
                        )
                        llm_business_postal_code = llm_gen(
                            query='business postal code', 
                            description='''The postal or ZIP code associated with the business's address.''', 
                            website_text=website_text
                        )
                        llm_business_latitude = llm_gen(
                            query='business latitude', 
                            description='''The latitude coordinate of the published business location, if explicitly available on the website.''', 
                            website_text=website_text
                        )
                        llm_business_longitude = llm_gen(
                            query='business longitude', 
                            description='''The longitude coordinate of the published business location, if explicitly available on the website.''', 
                            website_text=website_text
                        )
                        llm_business_additional_locations = llm_gen(
                            query='business additional locations', 
                            description='''Other business locations, offices, branches, or facilities operated by the company besides its headquarters. Include names and addresses when available.''', 
                            website_text=website_text
                        )
                        llm_business_farm_locations = llm_gen(
                            query='business farm locations', 
                            description='''Locations of farms where the business cultivates, grows, or harvests medicinal plants. Include addresses or geographic areas if provided.''', 
                            website_text=website_text
                        )
                        llm_business_nursery_locations = llm_gen(
                            query='business nursery locations', 
                            description='''Locations of plant nurseries where medicinal plants, seedlings, or seeds are propagated or sold.''', 
                            website_text=website_text
                        )
                        llm_business_factory_locations = llm_gen(
                            query='business factory locations', 
                            description='''Locations of manufacturing or production facilities where medicinal plant products are processed, formulated, packaged, or manufactured.''', 
                            website_text=website_text
                        )
                        llm_business_laboratory_locations = llm_gen(
                            query='business laboratory locations', 
                            description='''Locations of laboratories used for research, quality control, testing, extraction, or scientific analysis.''', 
                            website_text=website_text
                        )
                        llm_business_warehouse_locations = llm_gen(
                            query='business warehouse locations', 
                            description='''Locations of warehouses, storage facilities, fulfillment centers, or distribution centers used by the business.''', 
                            website_text=website_text
                        )
                        llm_business_retail_locations = llm_gen(
                            query='business retail locations', 
                            description='''Physical retail stores, herbal shops, apothecaries, garden centers, or showrooms operated by the business where customers can make purchases.''', 
                            website_text=website_text
                        )
                        # 5. Opening Information
                        llm_business_opening_hours = llm_gen(
                            query='opening_hours',
                            description='''The regular hours during which the business is open to visitors or customers.''',
                            website_text=website_text
                        )
                        llm_business_seasonal_hours = llm_gen(
                            query='seasonal_hours',
                            description='''Any changes to the business opening hours that apply during specific seasons, holidays, or periods of the year.''',
                            website_text=website_text
                        )
                        llm_business_appointment_required = llm_gen(
                            query='appointment_required',
                            description='''Whether visitors or customers are required to make an appointment in advance.''',
                            website_text=website_text
                        )
                        llm_business_walk_in_available = llm_gen(
                            query='walk_in_available',
                            description='''Whether visitors or customers can visit without an appointment or prior booking.''',
                            website_text=website_text
                        )
                        llm_business_visitor_access = llm_gen(
                            query='visitor_access',
                            description='''Information about whether and how visitors can access the business or its premises, including any restrictions or requirements.''',
                            website_text=website_text
                        )
                        # 6. Medicinal Plant Specialization
                        llm_business_medicinal_plants = llm_gen(
                            query='medicinal_plants', 
                            description='''Comprehensive list of medicinal plants, herbs, trees, shrubs, or other botanicals mentioned on the website''', 
                            website_text=website_text
                        )
                        llm_business_primary_medicinal_plants = llm_gen(
                            query='primary_medicinal_plants', 
                            description='''Main medicinal plants that are prominently featured, emphasized, or central to the organization's work or offerings''', 
                            website_text=website_text
                        )
                        llm_business_specialty_plants = llm_gen(
                            query='specialty_plants', 
                            description='''Specialty, flagship, signature, or particularly notable plant species associated with the organization''', 
                            website_text=website_text
                        )
                        llm_business_native_plants = llm_gen(
                            query='native_plants', 
                            description='''Medicinal plant species identified as native to the region, country, or geographic area discussed''', 
                            website_text=website_text
                        )
                        llm_business_rare_plants = llm_gen(
                            query='rare_plants', 
                            description='''Rare, threatened, endangered, vulnerable, or otherwise conservation-significant medicinal plant species mentioned''', 
                            website_text=website_text
                        )
                        llm_business_medicinal_plant_categories = llm_gen(
                            query='medicinal_plant_categories', 
                            description='''Categories or groupings of medicinal plants mentioned, such as adaptogens, aromatic herbs, medicinal trees, roots, flowers, or traditional herbal plants''', 
                            website_text=website_text
                        )
                        llm_business_botanical_collection_size = llm_gen(
                            query='botanical_collection_size', 
                            description='''Number of medicinal or botanical plant species in the organization's collection, garden, archive, nursery, or other stated botanical holdings, if specified''', 
                            website_text=website_text
                        )
                        # 7. Plant Relationships
                        llm_business_grows = llm_gen(
                            query='grows',
                            description='''Whether the business grows or cultivates plants, crops, or other botanical species itself.''',
                            website_text=website_text
                        )
                        llm_business_cultivates = llm_gen(
                            query='cultivates',
                            description='''Whether the business actively cultivates plants or botanical species through managed growing practices.''',
                            website_text=website_text
                        )
                        llm_business_propagates = llm_gen(
                            query='propagates',
                            description='''Whether the business propagates plants, such as through seeds, cuttings, division, tissue culture, or other propagation methods.''',
                            website_text=website_text
                        )
                        llm_business_researches = llm_gen(
                            query='researches',
                            description='''Whether the business conducts or supports research involving plants, botanical species, cultivation, or related applications.''',
                            website_text=website_text
                        )
                        llm_business_sells = llm_gen(
                            query='sells',
                            description='''Whether the business sells plants, botanical materials, or plant-derived products directly to customers.''',
                            website_text=website_text
                        )
                        llm_business_distributes = llm_gen(
                            query='distributes',
                            description='''Whether the business distributes plants, botanical materials, or plant-derived products to retailers, businesses, or other organizations.''',
                            website_text=website_text
                        )
                        llm_business_exports = llm_gen(
                            query='exports',
                            description='''Whether the business exports plants, botanical materials, or plant-derived products to other countries.''',
                            website_text=website_text
                        )
                        llm_business_imports = llm_gen(
                            query='imports',
                            description='''Whether the business imports plants, botanical materials, or plant-derived products from other countries.''',
                            website_text=website_text
                        )
                        llm_business_wild_harvests = llm_gen(
                            query='wild_harvests',
                            description='''Whether the business collects plants or botanical materials from wild or naturally occurring populations.''',
                            website_text=website_text
                        )
                        llm_business_conserves = llm_gen(
                            query='conserves',
                            description='''Whether the business engages in plant conservation, preservation, habitat protection, or safeguarding of botanical biodiversity.''',
                            website_text=website_text
                        )
                        llm_business_teaches = llm_gen(
                            query='teaches',
                            description='''Whether the business provides education, training, workshops, courses, or other instruction related to plants, cultivation, or botanical practices.''',
                            website_text=website_text
                        )
                        llm_business_uses_in_products = llm_gen(
                            query='uses_in_products',
                            description='''Whether the business uses plants, botanical materials, or plant-derived ingredients in products it manufactures or offers.''',
                            website_text=website_text
                        )
                        # 8. Products
                        llm_business_products = llm_gen(
                            query='products',
                            description='''Comprehensive information about all herbal and natural health products offered, including formulations, uses, and availability.''',
                            website_text=website_text
                        )
                        llm_business_product_categories = llm_gen(
                            query='product_categories',
                            description='''Overview of the different product categories available, including how products are organized by type or purpose.''',
                            website_text=website_text
                        )
                        llm_business_flagship_products = llm_gen(
                            query='flagship_products',
                            description='''Information about featured, best-selling, or signature products that represent the business's core offerings.''',
                            website_text=website_text
                        )
                        llm_business_product_forms = llm_gen(
                            query='product_forms',
                            description='''Details about the various forms in which products are available, such as teas, tinctures, capsules, powders, oils, and creams.''',
                            website_text=website_text
                        )
                        llm_business_herbal_teas = llm_gen(
                            query='herbal_teas',
                            description='''Information about herbal tea products, including ingredients, intended benefits, preparation methods, and available blends.''',
                            website_text=website_text
                        )
                        llm_business_tinctures = llm_gen(
                            query='tinctures',
                            description='''Details about herbal tinctures, including botanical ingredients, extraction methods, usage recommendations, and intended benefits.''',
                            website_text=website_text
                        )
                        llm_business_extracts = llm_gen(
                            query='extracts',
                            description='''Information about concentrated herbal extracts, including plant sources, extraction processes, applications, and available products.''',
                            website_text=website_text
                        )
                        llm_business_essential_oils = llm_gen(
                            query='essential_oils',
                            description='''Details about essential oils, including botanical origin, aromatic properties, recommended uses, and safety considerations.''',
                            website_text=website_text
                        )
                        llm_business_capsules = llm_gen(
                            query='capsules',
                            description='''Information about herbal capsules, including ingredients, dosage recommendations, intended uses, and available formulations.''',
                            website_text=website_text
                        )
                        llm_business_powders = llm_gen(
                            query='powders',
                            description='''Details about herbal powders, including plant sources, preparation methods, culinary or medicinal uses, and serving recommendations.''',
                            website_text=website_text
                        )
                        llm_business_dried_herbs = llm_gen(
                            query='dried_herbs',
                            description='''Information about dried herbs available for culinary, wellness, or medicinal purposes, including sourcing and preparation.''',
                            website_text=website_text
                        )
                        llm_business_fresh_herbs = llm_gen(
                            query='fresh_herbs',
                            description='''Details about fresh herbs offered, including varieties, seasonal availability, cultivation practices, and recommended uses.''',
                            website_text=website_text
                        )
                        llm_business_seeds = llm_gen(
                            query='seeds',
                            description='''Information about herb and plant seeds available for cultivation, including species, planting guidance, and growing conditions.''',
                            website_text=website_text
                        )
                        llm_business_seedlings = llm_gen(
                            query='seedlings',
                            description='''Details about live herb seedlings available for planting, including varieties, care instructions, and seasonal availability.''',
                            website_text=website_text
                        )
                        llm_business_roots = llm_gen(
                            query='roots',
                            description='''Information about medicinal or culinary roots offered, including botanical sources, preparation methods, and traditional uses.''',
                            website_text=website_text
                        )
                        llm_business_bark = llm_gen(
                            query='bark',
                            description='''Details about herbal bark products, including plant species, preparation methods, and traditional wellness applications.''',
                            website_text=website_text
                        )
                        llm_business_flowers = llm_gen(
                            query='flowers',
                            description='''Information about edible or medicinal flowers available, including botanical varieties, uses, and preparation methods.''',
                            website_text=website_text
                        )
                        llm_business_fruits = llm_gen(
                            query='fruits',
                            description='''Details about herbal or medicinal fruits offered, including varieties, health applications, and available product forms.''',
                            website_text=website_text
                        )
                        llm_business_resins = llm_gen(
                            query='resins',
                            description='''Information about natural plant resins, including botanical sources, traditional uses, and available preparations.''',
                            website_text=website_text
                        )
                        llm_business_cosmetics = llm_gen(
                            query='cosmetics',
                            description='''Details about natural cosmetic products, including ingredients, skincare benefits, and available formulations.''',
                            website_text=website_text
                        )
                        llm_business_soaps = llm_gen(
                            query='soaps',
                            description='''Information about natural or herbal soaps, including ingredients, skin benefits, fragrances, and available varieties.''',
                            website_text=website_text
                        )
                        llm_business_creams = llm_gen(
                            query='creams',
                            description='''Details about herbal creams, including active ingredients, intended uses, application instructions, and product variations.''',
                            website_text=website_text
                        )
                        llm_business_salves = llm_gen(
                            query='salves',
                            description='''Information about herbal salves, including botanical ingredients, intended topical applications, and usage recommendations.''',
                            website_text=website_text
                        )
                        llm_business_syrups = llm_gen(
                            query='syrups',
                            description='''Details about herbal syrups, including ingredients, intended wellness benefits, dosage guidance, and available formulations.''',
                            website_text=website_text
                        )
                        # 9. Product Attributes
                        llm_business_botanical_name = llm_gen(
                            query='botanical_name',
                            description='''The scientific botanical name of the plant, herb, or botanical ingredient, typically using its genus and species.''',
                            website_text=website_text
                        )
                        llm_business_common_name = llm_gen(
                            query='common_name',
                            description='''The commonly used name of the plant, herb, or botanical ingredient, including common or vernacular names.''',
                            website_text=website_text
                        )
                        llm_business_plant_part = llm_gen(
                            query='plant_part',
                            description='''The specific part of the plant used in the product, such as root, leaf, flower, seed, bark, fruit, or whole plant.''',
                            website_text=website_text
                        )
                        llm_business_extraction_method = llm_gen(
                            query='extraction_method',
                            description='''The method used to extract the active or desired botanical compounds, such as water extraction, alcohol extraction, CO₂ extraction, steam distillation, or maceration.''',
                            website_text=website_text
                        )
                        llm_business_preparation_method = llm_gen(
                            query='preparation_method',
                            description='''The form or process used to prepare the botanical product for use, such as dried, powdered, cut, tinctured, infused, encapsulated, or blended.''',
                            website_text=website_text
                        )
                        llm_business_ingredients = llm_gen(
                            query='ingredients',
                            description='''The ingredients contained in the product, including the primary botanical ingredients and any additional ingredients, carriers, excipients, or additives.''',
                            website_text=website_text
                        )
                        llm_business_packaging = llm_gen(
                            query='packaging',
                            description='''The type or format of packaging used for the product, such as bottle, jar, pouch, bag, box, tube, or bulk container.''',
                            website_text=website_text
                        )
                        llm_business_package_sizes = llm_gen(
                            query='package_sizes',
                            description='''The available package quantities or sizes, such as weight, volume, count, or other unit of measure.''',
                            website_text=website_text
                        )
                        llm_business_concentration = llm_gen(
                            query='concentration',
                            description='''The strength or concentration of the botanical preparation, extract, active ingredient, or standardized compound, when specified.''',
                            website_text=website_text
                        )
                        llm_business_organic_product = llm_gen(
                            query='organic_product',
                            description='''Indicates whether the product is identified, marketed, or certified as organic.''',
                            website_text=website_text
                        )
                        llm_business_private_label = llm_gen(
                            query='private_label',
                            description='''Indicates whether the product is available as a private-label product that can be branded and sold under another company's name.''',
                            website_text=website_text
                        )
                        llm_business_wholesale = llm_gen(
                            query='wholesale',
                            description='''Indicates whether the product is available for wholesale purchase, including bulk or business-to-business purchasing.''',
                            website_text=website_text
                        )
                        llm_business_retail = llm_gen(
                            query='retail',
                            description='''Indicates whether the product is available for direct retail purchase by individual consumers.''',
                            website_text=website_text
                        )
                        # 10. Services
                        llm_business_herbal_consultation = llm_gen(
                            query='herbal consultation',
                            description='''Professional consultation services focused on the traditional, therapeutic, or practical use of herbs and medicinal plants.''',
                            website_text=website_text
                        )
                        llm_business_herbal_clinic = llm_gen(
                            query='herbal clinic',
                            description='''A clinic or practice providing consultations and services related to herbal medicine and plant-based wellness.''',
                            website_text=website_text
                        )
                        llm_business_medicinal_plant_consulting = llm_gen(
                            query='medicinal plant consulting',
                            description='''Expert advice on the selection, use, cultivation, sourcing, processing, or commercialization of medicinal plants.''',
                            website_text=website_text
                        )
                        llm_business_plant_identification = llm_gen(
                            query='plant identification',
                            description='''Services for identifying plant species, varieties, or specimens based on their physical or botanical characteristics.''',
                            website_text=website_text
                        )
                        llm_business_botanical_identification = llm_gen(
                            query='botanical identification',
                            description='''Specialized identification and classification of plants using botanical taxonomy and scientific methods.''',
                            website_text=website_text
                        )
                        llm_business_cultivation_consulting = llm_gen(
                            query='cultivation consulting',
                            description='''Consulting services covering the cultivation, propagation, growing conditions, harvesting, and management of plants.''',
                            website_text=website_text
                        )
                        llm_business_contract_growing = llm_gen(
                            query='contract growing',
                            description='''Growing plants or agricultural crops on behalf of another business under an agreed contract or production arrangement.''',
                            website_text=website_text
                        )
                        llm_business_contract_manufacturing = llm_gen(
                            query='contract manufacturing',
                            description='''Manufacturing botanical, herbal, or plant-based products on behalf of another company or brand.''',
                            website_text=website_text
                        )
                        llm_business_private_label_manufacturing = llm_gen(
                            query='private label manufacturing',
                            description='''Production of herbal, botanical, or plant-based products that are sold under a customer's own brand or private label.''',
                            website_text=website_text
                        )
                        llm_business_extraction_services = llm_gen(
                            query='extraction services',
                            description='''Services for extracting active compounds, oils, or other useful constituents from plants or botanical materials.''',
                            website_text=website_text
                        )
                        llm_business_drying_services = llm_gen(
                            query='drying services',
                            description='''Commercial drying of harvested plants, herbs, roots, leaves, flowers, or other botanical materials to preserve and prepare them for further use.''',
                            website_text=website_text
                        )
                        llm_business_milling = llm_gen(
                            query='milling',
                            description='''Mechanical processing of plant or botanical materials into smaller particles or a desired particle size.''',
                            website_text=website_text
                        )
                        llm_business_grinding = llm_gen(
                            query='grinding',
                            description='''Processing herbs, plants, seeds, roots, or other botanical materials into a coarse or fine ground form.''',
                            website_text=website_text
                        )
                        llm_business_packaging_service = llm_gen(
                            query='packaging_service',
                            description='''Packaging services for herbal, botanical, agricultural, or plant-based products in suitable containers or formats.''',
                            website_text=website_text
                        )
                        llm_business_export_services = llm_gen(
                            query='export services',
                            description='''Services supporting the preparation, documentation, logistics, and international shipment of botanical or plant-based products.''',
                            website_text=website_text
                        )
                        llm_business_laboratory_testing = llm_gen(
                            query='laboratory testing',
                            description='''Laboratory analysis and testing of botanical or herbal materials and products for quality, identity, purity, safety, or composition.''',
                            website_text=website_text
                        )
                        llm_business_formulation = llm_gen(
                            query='formulation',
                            description='''Development or preparation of recipes and product formulations using herbs, botanicals, extracts, or other plant-based ingredients.''',
                            website_text=website_text
                        )
                        llm_business_research_services = llm_gen(
                            query='research services',
                            description='''Research and development services involving medicinal plants, botanicals, herbal products, cultivation, extraction, or related scientific topics.''',
                            website_text=website_text
                        )
                        llm_business_education = llm_gen(
                            query='education',
                            description='''Educational services providing knowledge or training related to herbs, medicinal plants, botany, cultivation, processing, or herbal practices.''',
                            website_text=website_text
                        )
                        llm_business_workshops = llm_gen(
                            query='workshops',
                            description='''Practical, focused educational sessions or hands-on activities covering herbal, botanical, cultivation, processing, or related topics.''',
                            website_text=website_text
                        )
                        llm_business_courses = llm_gen(
                            query='courses',
                            description='''Structured educational programs providing systematic instruction in herbal medicine, botany, plant cultivation, or related subjects.''',
                            website_text=website_text
                        )
                        llm_business_farm_tours = llm_gen(
                            query='farm tours',
                            description='''Guided visits to farms or agricultural operations where participants can learn about plant cultivation, harvesting, and production.''',
                            website_text=website_text
                        )
                        llm_business_botanical_tours = llm_gen(
                            query='botanical tours',
                            description='''Guided tours focused on identifying, studying, and learning about botanical species and plant collections in natural or cultivated settings.''',
                            website_text=website_text
                        )
                        # 11. Cultivation
                        llm_business_cultivation_methods = llm_gen(
                            query='cultivation_methods',
                            description='''The overall cultivation approach or farming system used to grow the ingredient, including conventional and specialized agricultural practices.''',
                            website_text=website_text
                        )
                        llm_business_organic_cultivation = llm_gen(
                            query='organic_cultivation',
                            description='''Whether the ingredient is cultivated according to certified or non-certified organic farming practices that avoid synthetic pesticides and fertilizers.''',
                            website_text=website_text
                        )
                        llm_business_regenerative = llm_gen(
                            query='regenerative',
                            description='''Whether regenerative agricultural practices are used to improve soil health, biodiversity, carbon sequestration, and ecosystem resilience.''',
                            website_text=website_text
                        )
                        llm_business_biodynamic = llm_gen(
                            query='biodynamic',
                            description='''Whether the ingredient is produced using biodynamic farming principles, including holistic farm management and biodynamic preparations.''',
                            website_text=website_text
                        )
                        llm_business_permaculture = llm_gen(
                            query='permaculture',
                            description='''Whether permaculture design principles are applied to create sustainable, self-supporting agricultural ecosystems.''',
                            website_text=website_text
                        )
                        llm_business_agroforestry = llm_gen(
                            query='agroforestry',
                            description='''Whether the ingredient is cultivated within an agroforestry system that integrates trees with crops or livestock.''',
                            website_text=website_text
                        )
                        llm_business_greenhouse = llm_gen(
                            query='greenhouse',
                            description='''Whether the ingredient is grown in greenhouse or protected cultivation environments.''',
                            website_text=website_text
                        )
                        llm_business_indoor = llm_gen(
                            query='indoor',
                            description='''Whether the ingredient is cultivated entirely indoors using controlled environmental conditions.''',
                            website_text=website_text
                        )
                        llm_business_outdoor = llm_gen(
                            query='outdoor',
                            description='''Whether the ingredient is grown outdoors under natural environmental conditions.''',
                            website_text=website_text
                        )
                        llm_business_wild_harvesting = llm_gen(
                            query='wild_harvesting',
                            description='''Whether the ingredient is collected from naturally occurring wild populations rather than cultivated sources.''',
                            website_text=website_text
                        )
                        llm_business_sustainable_wild_harvesting = llm_gen(
                            query='sustainable_wild_harvesting',
                            description='''Whether wild harvesting practices are managed to maintain long-term ecosystem health and species populations.''',
                            website_text=website_text
                        )
                        llm_business_propagation_methods = llm_gen(
                            query='propagation_methods',
                            description='''The methods used to propagate or establish the crop, such as seeds, cuttings, grafting, division, or tissue culture.''',
                            website_text=website_text
                        )
                        llm_business_irrigation = llm_gen(
                            query='irrigation',
                            description='''The irrigation methods and water management practices used during cultivation.''',
                            website_text=website_text
                        )
                        llm_business_fertilization = llm_gen(
                            query='fertilization',
                            description='''The fertilizers, nutrient sources, and fertilization practices applied during cultivation.''',
                            website_text=website_text
                        )
                        llm_business_soil_management = llm_gen(
                            query='soil_management',
                            description='''The soil preparation, conservation, and management practices used to maintain soil quality and fertility.''',
                            website_text=website_text
                        )
                        llm_business_pest_management = llm_gen(
                            query='pest_management',
                            description='''The strategies used to prevent, monitor, and control pests and diseases, including integrated pest management approaches.''',
                            website_text=website_text
                        )
                        llm_business_harvest_methods = llm_gen(
                            query='harvest_methods',
                            description='''The techniques and procedures used to harvest the ingredient, including manual or mechanical methods.''',
                            website_text=website_text
                        )
                        llm_business_harvest_season = llm_gen(
                            query='harvest_season',
                            description='''The typical season or time of year during which the ingredient is harvested.''',
                            website_text=website_text
                        )
                        # 12. Manufacturing
                        llm_business_manufacturing = llm_gen(
                            query='manufacturing',
                            description='''The production of goods or products from raw materials through defined manufacturing processes.''',
                            website_text=website_text
                        )
                        llm_business_processing = llm_gen(
                            query='processing',
                            description='''The treatment, conversion, or preparation of raw materials or intermediate materials to produce a desired product or ingredient.''',
                            website_text=website_text
                        )
                        llm_business_extraction = llm_gen(
                            query='extraction',
                            description='''The process of separating and recovering specific compounds, ingredients, or substances from a raw material using physical, chemical, or mechanical methods.''',
                            website_text=website_text
                        )
                        llm_business_distillation = llm_gen(
                            query='distillation',
                            description='''A separation and purification process that uses differences in boiling points to isolate or concentrate specific components of a mixture.''',
                            website_text=website_text
                        )
                        llm_business_fermentation = llm_gen(
                            query='fermentation',
                            description='''A controlled biological process in which microorganisms convert organic substances into desired products, compounds, or intermediates.''',
                            website_text=website_text
                        )
                        llm_business_drying = llm_gen(
                            query='drying',
                            description='''The controlled removal of moisture from raw materials, ingredients, or products to improve stability, preservation, handling, or shelf life.''',
                            website_text=website_text
                        )
                        llm_business_manufacturing_milling = llm_gen(
                            query='manufacturing_milling',
                            description='''The mechanical reduction of raw materials or ingredients into smaller particles or a specified particle size.''',
                            website_text=website_text
                        )
                        llm_business_manufacturing_grinding = llm_gen(
                            query='manufacturing_grinding',
                            description='''The mechanical breakdown of materials into finer particles using friction, impact, compression, or other mechanical forces.''',
                            website_text=website_text
                        )
                        llm_business_blending = llm_gen(
                            query='blending',
                            description='''The controlled mixing of two or more ingredients, materials, or components to achieve a uniform composition or desired properties.''',
                            website_text=website_text
                        )
                        llm_business_manufacturing_formulation = llm_gen(
                            query='manufacturing_formulation',
                            description='''The development and combination of ingredients or components in defined proportions to create a product with specified characteristics or performance.''',
                            website_text=website_text
                        )
                        llm_business_encapsulation = llm_gen(
                            query='encapsulation',
                            description='''The process of enclosing an active ingredient, compound, or material within a capsule or protective coating for delivery, stability, or controlled release.''',
                            website_text=website_text
                        )
                        llm_business_manufacturing_packaging = llm_gen(
                            query='manufacturing_packaging',
                            description='''The process of enclosing, protecting, labeling, and preparing products for storage, transportation, distribution, or sale.''',
                            website_text=website_text
                        )
                        llm_business_quality_testing = llm_gen(
                            query='quality_testing',
                            description='''Testing performed to verify that raw materials, intermediates, or finished products meet defined quality specifications, standards, and requirements.''',
                            website_text=website_text
                        )
                        llm_business_batch_testing = llm_gen(
                            query='batch_testing',
                            description='''Testing performed on a specific production batch to confirm that it meets established specifications for identity, quality, safety, purity, potency, or other required characteristics.''',
                            website_text=website_text
                        )
                        llm_business_traceability = llm_gen(
                            query='traceability',
                            description='''The ability to track the history, origin, processing, movement, and status of materials or products throughout the supply chain and production process.''',
                            website_text=website_text
                        )
                        # 13. Facilities
                        llm_business_facilities_farms = llm_gen(
                            query='farms',
                            description='''Agricultural facilities where plants, crops, or other botanical products are cultivated and managed.''',
                            website_text=website_text
                        )
                        llm_business_facilities_nurseries = llm_gen(
                            query='nurseries',
                            description='''Facilities that propagate, grow, and maintain plants, seedlings, saplings, and other young botanical specimens before sale, transplantation, or further cultivation.''',
                            website_text=website_text
                        )
                        llm_business_facilities_laboratories = llm_gen(
                            query='laboratories',
                            description='''Specialized facilities used for scientific analysis, experimentation, testing, and research involving plants, biological materials, soils, or related products.''',
                            website_text=website_text
                        )
                        llm_business_facilities_factories = llm_gen(
                            query='factories',
                            description='''Industrial facilities where agricultural, botanical, or plant-derived materials are processed, manufactured, packaged, or transformed into finished products.''',
                            website_text=website_text
                        )
                        llm_business_facilities_warehouses = llm_gen(
                            query='warehouses',
                            description='''Storage facilities used to hold plants, agricultural products, botanical materials, equipment, supplies, or finished goods.''',
                            website_text=website_text
                        )
                        llm_business_facilities_botanical_gardens = llm_gen(
                            query='botanical_gardens',
                            description='''Public or private gardens dedicated to the cultivation, conservation, research, documentation, and display of diverse plant species and collections.''',
                            website_text=website_text
                        )
                        llm_business_facilities_greenhouses = llm_gen(
                            query='greenhouses',
                            description='''Controlled-environment structures designed for growing and maintaining plants by regulating conditions such as temperature, humidity, light, and ventilation.''',
                            website_text=website_text
                        )
                        llm_business_facilities_visitor_centers = llm_gen(
                            query='visitor_centers',
                            description='''Facilities that provide visitors with information, exhibits, services, tours, and educational resources related to a site, organization, garden, farm, or research facility.''',
                            website_text=website_text
                        )
                        llm_business_facilities_research_centers = llm_gen(
                            query='research_centers',
                            description='''Facilities dedicated to scientific investigation, experimentation, innovation, and research in areas such as agriculture, botany, horticulture, ecology, or plant science.''',
                            website_text=website_text
                        )
                        llm_business_facilities_education_centers = llm_gen(
                            query='education_centers',
                            description='''Facilities that provide educational programs, workshops, training, demonstrations, and learning resources related to agriculture, plants, horticulture, science, or environmental topics.''',
                            website_text=website_text
                        )
                        llm_business_facilities_clinics = llm_gen(
                            query='clinics',
                            description='''Facilities that provide diagnostic, treatment, consultation, or health-related services, including specialized services for plants, animals, or people where applicable.''',
                            website_text=website_text
                        )
                        llm_business_facilities_retail_stores = llm_gen(
                            query='retail_stores',
                            description='''Commercial facilities where plants, agricultural products, gardening supplies, botanical goods, equipment, or related products are displayed and sold to customers.''',
                            website_text=website_text
                        )
                        # 14. Certifications
                        llm_business_certifications_certifications = llm_gen(
                            query='certifications', 
                            description='''Stores certification records associated with the business, including certification details, issuing organization, dates, and scope.''', 
                            website_text=website_text
                        )
                        llm_business_certifications_certification_name = llm_gen(
                            query='certification_name', 
                            description='''The name or title of the certification obtained by the business or individual.''', 
                            website_text=website_text
                        )
                        llm_business_certifications_certification_number = llm_gen(
                            query='certification_number', 
                            description='''The unique identification number, reference number, or certificate number assigned to the certification.''', 
                            website_text=website_text
                        )
                        llm_business_certifications_issuing_organization = llm_gen(
                            query='issuing_organization', 
                            description='''The organization, authority, or institution that issued the certification.''', 
                            website_text=website_text
                        )
                        llm_business_certifications_issue_date = llm_gen(
                            query='issue_date', 
                            description='''The date on which the certification was issued or became effective.''', 
                            website_text=website_text
                        )
                        llm_business_certifications_expiry_date = llm_gen(
                            query='expiry_date', 
                            description='''The date on which the certification expires or is no longer valid, if applicable.''', 
                            website_text=website_text
                        )
                        llm_business_certifications_certification_scope = llm_gen(
                            query='certification_scope', 
                            description='''Describes the activities, services, products, locations, standards, or areas covered by the certification.''', 
                            website_text=website_text
                        )
                        # 15. Quality
                        llm_business_quality_quality_control = llm_gen(
                            query='quality_control', 
                            description='''Information about the company's procedures and measures for maintaining and monitoring product quality throughout production.''', 
                            website_text=website_text
                        )
                        llm_business_quality_laboratory_testing = llm_gen(
                            query='laboratory_testing', 
                            description='''Information about laboratory tests performed on products, materials, ingredients, or samples to verify quality, safety, purity, or compliance.''', 
                            website_text=website_text
                        )
                        llm_business_quality_batch_testing = llm_gen(
                            query='batch_testing', 
                            description='''Information about testing conducted on individual production batches to verify consistency, quality, safety, or compliance with specifications.''', 
                            website_text=website_text
                        )
                        llm_business_quality_third_party_testing = llm_gen(
                            query='third_party_testing', 
                            description='''Information about independent testing performed by external laboratories or organizations to verify product quality, safety, purity, or compliance.''', 
                            website_text=website_text
                        )
                        llm_business_quality_traceability = llm_gen(
                            query='traceability', 
                            description='''Information about systems and procedures used to track products, ingredients, raw materials, or batches throughout the supply chain and production process.''', 
                            website_text=website_text
                        )
                        llm_business_quality_quality_management_system = llm_gen(
                            query='quality_management_system', 
                            description='''Information about the formal systems, standards, procedures, and processes used to consistently manage, monitor, and improve product quality.''', 
                            website_text=website_text
                        )
                        # 16. Sustainability
                        llm_business_sustainability_sustainability_policy = llm_gen(
                            query='sustainability_policy', 
                            description='''Describes the business's overall sustainability policy, commitments, goals, and practices for reducing environmental and social impacts.''', 
                            website_text=website_text
                        )
                        llm_business_sustainability_conservation = llm_gen(
                            query='conservation', 
                            description='''Describes initiatives and practices focused on conserving natural resources, ecosystems, habitats, and wildlife.''', 
                            website_text=website_text
                        )
                        llm_business_sustainability_biodiversity = llm_gen(
                            query='biodiversity', 
                            description='''Describes efforts to protect, restore, and enhance biodiversity, including the preservation of species, habitats, and ecosystems.''', 
                            website_text=website_text
                        )
                        llm_business_sustainability_regenerative_agriculture = llm_gen(
                            query='regenerative_agriculture', 
                            description='''Describes agricultural practices that restore soil health, improve ecosystem resilience, enhance biodiversity, and reduce environmental impact.''', 
                            website_text=website_text
                        )
                        llm_business_sustainability_ethical_sourcing = llm_gen(
                            query='ethical_sourcing', 
                            description='''Describes how the business sources products and materials responsibly, considering environmental standards, labor conditions, human rights, and supply-chain transparency.''', 
                            website_text=website_text
                        )
                        llm_business_sustainability_fair_trade = llm_gen(
                            query='fair_trade', 
                            description='''Describes the business's use or support of fair-trade products and practices that promote fair prices, decent working conditions, and equitable treatment of producers.''', 
                            website_text=website_text
                        )
                        llm_business_sustainability_community_projects = llm_gen(
                            query='community_projects', 
                            description='''Describes sustainability or social-impact projects that support local communities, including education, infrastructure, livelihoods, conservation, or community development.''', 
                            website_text=website_text
                        )
                        llm_business_sustainability_indigenous_partnerships = llm_gen(
                            query='indigenous_partnerships', 
                            description='''Describes partnerships and initiatives involving Indigenous communities, including respect for Indigenous rights, knowledge, culture, land, and economic participation.''', 
                            website_text=website_text
                        )
                        llm_business_sustainability_local_sourcing = llm_gen(
                            query='local_sourcing', 
                            description='''Describes the extent to which products, ingredients, materials, or services are sourced from local or regional suppliers to support local economies and reduce transportation impacts.''', 
                            website_text=website_text
                        )
                        llm_business_sustainability_recyclable_packaging = llm_gen(
                            query='recyclable_packaging', 
                            description='''Describes the use of packaging that can be recycled, along with initiatives to reduce packaging waste and improve packaging recyclability.''', 
                            website_text=website_text
                        )
                        llm_business_sustainability_carbon_reduction = llm_gen(
                            query='carbon_reduction', 
                            description='''Describes initiatives to measure, reduce, offset, or otherwise manage greenhouse-gas emissions and the business's carbon footprint.''', 
                            website_text=website_text
                        )
                        llm_business_sustainability_water_conservation = llm_gen(
                            query='water_conservation', 
                            description='''Describes practices and initiatives designed to reduce water consumption, improve water efficiency, protect water resources, and minimize water-related environmental impacts.''', 
                            website_text=website_text
                        )
                        # 17. Research
                        llm_business_research_research_programs = llm_gen(
                            query='research_programs', 
                            description='''Organized research programs focused on investigating medicinal plants, natural products, traditional medicine, therapeutic applications, and related scientific topics.''', 
                            website_text=website_text
                        )
                        llm_business_research_research_projects = llm_gen(
                            query='research_projects', 
                            description='''Individual research projects involving the study, development, validation, or application of plants, natural compounds, botanical medicines, and related scientific subjects.''', 
                            website_text=website_text
                        )
                        llm_business_research_publications = llm_gen(
                            query='publications', 
                            description='''Scientific publications, research papers, reviews, books, reports, and other scholarly works documenting research findings and knowledge.''', 
                            website_text=website_text
                        )
                        llm_business_research_patents = llm_gen(
                            query='patents', 
                            description='''Patents and patent applications covering novel discoveries, formulations, extraction methods, compounds, technologies, or other innovations related to botanical and natural-product research.''', 
                            website_text=website_text
                        )
                        llm_business_research_university_partnerships = llm_gen(
                            query='university_partnerships', 
                            description='''Collaborations and formal partnerships with universities or academic institutions supporting research, education, knowledge exchange, and scientific development.''', 
                            website_text=website_text
                        )
                        llm_business_research_clinical_trials = llm_gen(
                            query='clinical_trials', 
                            description='''Clinical studies evaluating the safety, efficacy, pharmacological effects, or therapeutic potential of medicinal plants, botanical preparations, or natural compounds in humans.''', 
                            website_text=website_text
                        )
                        llm_business_research_ethnobotanical_research = llm_gen(
                            query='ethnobotanical_research', 
                            description='''Research examining traditional knowledge and cultural uses of plants, including their medicinal, nutritional, agricultural, and other practical applications.''', 
                            website_text=website_text
                        )
                        llm_business_research_pharmacognosy = llm_gen(
                            query='pharmacognosy', 
                            description='''Research focused on medicinal substances obtained from natural sources, particularly the identification, characterization, evaluation, and quality control of medicinal plants and natural products.''', 
                            website_text=website_text
                        )
                        llm_business_research_phytochemistry = llm_gen(
                            query='phytochemistry', 
                            description='''Research investigating the chemical constituents of plants, including the isolation, identification, characterization, and analysis of bioactive phytochemicals.''', 
                            website_text=website_text
                        )
                        llm_business_research_plant_breeding = llm_gen(
                            query='plant_breeding', 
                            description='''Research involving the selective development and improvement of plant varieties for desirable traits such as yield, quality, resilience, medicinal properties, or enhanced concentrations of bioactive compounds.''', 
                            website_text=website_text
                        )
                        # 18. Education
                        llm_business_education_courses = llm_gen(
                            query='courses', 
                            description='''Educational programs designed to provide structured learning and practical knowledge on specific topics or skills.''', 
                            website_text=website_text
                        )
                        llm_business_education_workshops = llm_gen(
                            query='workshops', 
                            description='''Interactive, hands-on learning sessions focused on developing practical skills, techniques, or knowledge.''', 
                            website_text=website_text
                        )
                        llm_business_education_webinars = llm_gen(
                            query='webinars', 
                            description='''Online educational sessions delivered remotely, typically featuring presentations, demonstrations, or discussions on specific topics.''', 
                            website_text=website_text
                        )
                        llm_business_education_apprenticeships = llm_gen(
                            query='apprenticeships', 
                            description='''Structured work-based learning opportunities that combine practical experience with guided instruction and skill development.''', 
                            website_text=website_text
                        )
                        llm_business_education_lectures = llm_gen(
                            query='lectures', 
                            description='''Educational presentations delivered by an instructor or expert to explain concepts, share knowledge, or explore a specific subject.''', 
                            website_text=website_text
                        )
                        llm_business_education_botanical_walks = llm_gen(
                            query='botanical_walks', 
                            description='''Guided outdoor educational walks focused on identifying, understanding, and learning about plants and their natural environments.''', 
                            website_text=website_text
                        )
                        llm_business_education_farm_tours = llm_gen(
                            query='farm_tours', 
                            description='''Guided visits to farms that provide educational insight into agricultural practices, farming operations, crops, livestock, or food production.''', 
                            website_text=website_text
                        )
                        llm_business_education_certifications_offered = llm_gen(
                            query='certifications_offered', 
                            description='''Professional or educational certifications available to participants who complete specified training, courses, assessments, or requirements.''', 
                            website_text=website_text
                        )
                        # 19. Traditional Medicine Systems
                        llm_business_traditional_medicine_systems_ayurveda = llm_gen(
                            query='ayurveda', 
                            description='''A traditional system of medicine originating in India that emphasizes balance among the body, mind, and environment through diet, lifestyle practices, herbal preparations, and other therapeutic approaches.''', 
                            website_text=website_text
                        )
                        llm_business_traditional_medicine_systems_traditional_chinese_medicine = llm_gen(
                            query='traditional_chinese_medicine', 
                            description='''A traditional medical system originating in China that uses approaches such as acupuncture, herbal medicine, dietary therapy, massage, and movement practices to promote balance and support health.''', 
                            website_text=website_text
                        )
                        llm_business_traditional_medicine_systems_western_herbalism = llm_gen(
                            query='western_herbalism', 
                            description='''A tradition of herbal medicine rooted primarily in European and Western practices that uses medicinal plants and plant preparations to support health and address various health concerns.''', 
                            website_text=website_text
                        )
                        llm_business_traditional_medicine_systems_unani = llm_gen(
                            query='unani', 
                            description='''A traditional system of medicine developed from Greco-Arabic medical traditions and practiced extensively in South Asia and other regions, emphasizing bodily balance, diet, lifestyle, and natural remedies.''', 
                            website_text=website_text
                        )
                        llm_business_traditional_medicine_systems_kampo = llm_gen(
                            query='kampo', 
                            description='''A Japanese traditional medicine system derived from classical Chinese medical traditions that primarily uses standardized combinations of medicinal herbs formulated according to traditional diagnostic principles.''', 
                            website_text=website_text
                        )
                        llm_business_traditional_medicine_systems_tibetan_medicine = llm_gen(
                            query='tibetan_medicine', 
                            description='''A traditional medical system originating in Tibet that integrates herbal and mineral remedies, dietary and behavioral practices, and concepts of bodily balance influenced by Tibetan Buddhist and broader Asian medical traditions.''', 
                            website_text=website_text
                        )
                        llm_business_traditional_medicine_systems_indigenous_medicine = llm_gen(
                            query='indigenous_medicine', 
                            description='''Traditional health practices developed and maintained by Indigenous peoples, incorporating locally available plants, foods, cultural knowledge, spiritual practices, and community-based approaches to health and healing.''', 
                            website_text=website_text
                        )
                        llm_business_traditional_medicine_systems_african_traditional_medicine = llm_gen(
                            query='african_traditional_medicine', 
                            description='''Diverse traditional healing systems practiced across African communities that commonly incorporate medicinal plants, animal or mineral substances, cultural knowledge, spiritual practices, and community-based healing traditions.''', 
                            website_text=website_text
                        )
                        # 20. Expertise
                        llm_business_expertise_expertise_topics = llm_gen(
                            query='expertise_topics', 
                            description='''Areas of specialized knowledge, experience, or professional focus related to herbalism, medicinal plants, botany, and natural medicine.''', 
                            website_text=website_text
                        )
                        llm_business_expertise_medicinal_plant_cultivation = llm_gen(
                            query='medicinal_plant_cultivation', 
                            description='''Knowledge and practical experience in growing, managing, harvesting, and maintaining plants used for medicinal purposes.''', 
                            website_text=website_text
                        )
                        llm_business_expertise_herbal_formulation = llm_gen(
                            query='herbal_formulation', 
                            description='''Expertise in developing, combining, preparing, and optimizing herbal preparations using medicinal plants and botanical ingredients.''', 
                            website_text=website_text
                        )
                        llm_business_expertise_ethnobotany = llm_gen(
                            query='ethnobotany', 
                            description='''Study and knowledge of the relationships between people, cultures, and plants, including traditional uses of plants for food, medicine, rituals, and other purposes.''', 
                            website_text=website_text
                        )
                        llm_business_expertise_pharmacognosy = llm_gen(
                            query='pharmacognosy', 
                            description='''Scientific expertise in the study of medicinal substances derived from natural sources, particularly plants, including their identification, constituents, properties, and therapeutic uses.''', 
                            website_text=website_text
                        )
                        llm_business_expertise_botanical_identification = llm_gen(
                            query='botanical_identification', 
                            description='''Ability to accurately identify and classify plants using botanical characteristics, taxonomy, morphology, and other identification methods.''', 
                            website_text=website_text
                        )
                        llm_business_expertise_herbal_medicine = llm_gen(
                            query='herbal_medicine', 
                            description='''Knowledge and experience in the traditional and contemporary use of medicinal herbs and plant-based remedies to support health and well-being.''', 
                            website_text=website_text
                        )
                        llm_business_expertise_conservation = llm_gen(
                            query='conservation', 
                            description='''Expertise in protecting, preserving, and sustainably managing medicinal plants, botanical resources, habitats, and plant biodiversity.''', 
                            website_text=website_text
                        )
                        llm_business_expertise_plant_propagation = llm_gen(
                            query='plant_propagation', 
                            description='''Knowledge and practical experience in reproducing plants through methods such as seeds, cuttings, division, layering, grafting, and tissue culture.''', 
                            website_text=website_text
                        )
                        # 21. People
                        llm_business_people_founders = llm_gen(
                            query='founders',
                            description='''The founders of the company, organization, farm, institution, or brand, including individuals who established or co-founded it.''',
                            website_text=website_text
                        )
                        llm_business_people_owners = llm_gen(
                            query='owners',
                            description='''The current or past owners of the company, farm, laboratory, organization, or brand, including individuals or ownership groups.''',
                            website_text=website_text
                        )
                        llm_business_people_ceo = llm_gen(
                            query='ceo',
                            description='''The Chief Executive Officer (CEO) or equivalent top executive responsible for leading the organization's overall strategy and operations.''',
                            website_text=website_text
                        )
                        llm_business_people_president = llm_gen(
                            query='president',
                            description='''The president of the company, organization, institution, or association, including current or former presidents.''',
                            website_text=website_text
                        )
                        llm_business_people_director = llm_gen(
                            query='director',
                            description='''Directors or executive directors responsible for overseeing departments, programs, research, operations, or the organization as a whole.''',
                            website_text=website_text
                        )
                        llm_business_people_botanists = llm_gen(
                            query='botanists',
                            description='''Botanists associated with the organization, including plant scientists, taxonomists, or experts involved in botanical research and plant identification.''',
                            website_text=website_text
                        )
                        llm_business_people_herbalists = llm_gen(
                            query='herbalists',
                            description='''Herbalists associated with the organization, including practitioners, formulators, educators, or experts in medicinal plants and herbal medicine.''',
                            website_text=website_text
                        )
                        llm_business_people_researchers = llm_gen(
                            query='researchers',
                            description='''Researchers affiliated with the organization, including scientists, scholars, investigators, and research staff contributing to scientific or technical work.''',
                            website_text=website_text
                        )
                        llm_business_people_agronomists = llm_gen(
                            query='agronomists',
                            description='''Agronomists associated with the organization, including experts in crop science, soil management, sustainable agriculture, and farming practices.''',
                            website_text=website_text
                        )
                        llm_business_people_pharmacists = llm_gen(
                            query='pharmacists',
                            description='''Pharmacists associated with the organization, including licensed pharmacists, pharmaceutical scientists, formulators, and medication experts.''',
                            website_text=website_text
                        )
                        llm_business_people_educators = llm_gen(
                            query='educators',
                            description='''Educators affiliated with the organization, including instructors, trainers, professors, lecturers, and educational program leaders.''',
                            website_text=website_text
                        )
                        llm_business_people_laboratory_directors = llm_gen(
                            query='laboratory_directors',
                            description='''Laboratory directors responsible for overseeing laboratory operations, scientific research, quality assurance, testing, and compliance.''',
                            website_text=website_text
                        )
                        llm_business_people_farm_managers = llm_gen(
                            query='farm_managers',
                            description='''Farm managers responsible for supervising agricultural operations, crop production, livestock management, and day-to-day farm activities.''',
                            website_text=website_text
                        )
                        # 22. Markets
                        llm_business_markets_customer_types = llm_gen(
                            query='customer_types', 
                            description='''Types of customers the business serves, such as consumers, businesses, distributors, retailers, wholesalers, government organizations, or other customer segments.''', 
                            website_text=website_text
                        )
                        llm_business_markets_industries_served = llm_gen(
                            query='industries_served', 
                            description='''Industries, sectors, or business verticals that the company provides products or services to.''', 
                            website_text=website_text
                        )
                        llm_business_markets_export_markets = llm_gen(
                            query='export_markets', 
                            description='''Countries or international markets where the company exports or sells its products outside its primary domestic market.''', 
                            website_text=website_text
                        )
                        llm_business_markets_import_markets = llm_gen(
                            query='import_markets', 
                            description='''Countries or international markets from which the company imports products, materials, components, or other goods.''', 
                            website_text=website_text
                        )
                        llm_business_markets_countries_served = llm_gen(
                            query='countries_served', 
                            description='''Individual countries where the company sells, operates, distributes products, or otherwise provides its products or services.''', 
                            website_text=website_text
                        )
                        llm_business_markets_regions_served = llm_gen(
                            query='regions_served', 
                            description='''Geographic regions, territories, states, provinces, or broader areas where the company operates or serves customers.''', 
                            website_text=website_text
                        )
                        llm_business_markets_international_shipping = llm_gen(
                            query='international_shipping', 
                            description='''Whether the company offers shipping or delivery to customers in countries outside its domestic market, including any stated international shipping capabilities.''', 
                            website_text=website_text
                        )
                        llm_business_markets_wholesale_available = llm_gen(
                            query='wholesale_available', 
                            description='''Whether the company offers products or services through wholesale purchasing arrangements, including bulk sales to retailers, distributors, or other businesses.''', 
                            website_text=website_text
                        )
                        llm_business_markets_retail_available = llm_gen(
                            query='retail_available', 
                            description='''Whether the company sells products or services directly to individual consumers through retail channels, such as physical stores or online stores.''', 
                            website_text=website_text
                        )
                        llm_business_markets_private_label_available = llm_gen(
                            query='private_label_available', 
                            description='''Whether the company offers private-label or white-label products that can be sold under another company's or customer's brand.''', 
                            website_text=website_text
                        )

                        # 23. Online Presence
                        llm_business_online_presence_facebook = llm_gen(
                            query='facebook', 
                            description='''The business's official Facebook profile or page, used for sharing updates, content, announcements, and engaging with its audience.''', 
                            website_text=website_text
                        )
                        llm_business_online_presence_instagram = llm_gen(
                            query='instagram', 
                            description='''The business's official Instagram profile, used for visual content, updates, promotions, and audience engagement.''', 
                            website_text=website_text
                        )
                        llm_business_online_presence_linkedin = llm_gen(
                            query='linkedin', 
                            description='''The business's official LinkedIn profile or company page, used for professional information, company updates, hiring, and industry engagement.''', 
                            website_text=website_text
                        )
                        llm_business_online_presence_youtube = llm_gen(
                            query='youtube', 
                            description='''The business's official YouTube channel, used for publishing and sharing video content, tutorials, presentations, or other media.''', 
                            website_text=website_text
                        )
                        llm_business_online_presence_x = llm_gen(
                            query='x', 
                            description='''The business's official X (formerly Twitter) profile, used for short-form updates, announcements, news, and audience engagement.''', 
                            website_text=website_text
                        )
                        llm_business_online_presence_pinterest = llm_gen(
                            query='pinterest', 
                            description='''The business's official Pinterest profile, used for sharing visual content, inspiration, products, and links through pins and boards.''', 
                            website_text=website_text
                        )
                        llm_business_online_presence_tiktok = llm_gen(
                            query='tiktok', 
                            description='''The business's official TikTok profile, used for publishing short-form video content, promotions, and audience engagement.''', 
                            website_text=website_text
                        )
                        llm_business_online_presence_github = llm_gen(
                            query='github', 
                            description='''The business's official GitHub organization or profile, used for hosting and sharing source code, software projects, documentation, and developer resources.''', 
                            website_text=website_text
                        )
                        llm_business_online_presence_wikipedia = llm_gen(
                            query='wikipedia', 
                            description='''The business's Wikipedia article or relevant Wikipedia page, providing publicly documented, encyclopedic information about the business.''', 
                            website_text=website_text
                        )

                        # 24. Awards
                        llm_business_awards_awards = llm_gen(
                            query='awards', 
                            description='''Stores information about awards and recognitions associated with the business, organization, or entity.''', 
                            website_text=website_text
                        )
                        llm_business_awards_award_name = llm_gen(
                            query='award_name', 
                            description='''The name or title of the award received by the business, organization, or entity.''', 
                            website_text=website_text
                        )
                        llm_business_awards_award_year = llm_gen(
                            query='award_year', 
                            description='''The year in which the award was received or awarded.''', 
                            website_text=website_text
                        )
                        llm_business_awards_awarding_organization = llm_gen(
                            query='awarding_organization', 
                            description='''The name of the organization, institution, association, or body that presented the award.''', 
                            website_text=website_text
                        )

                        # 25. Memberships
                        llm_business_memberships_professional_associations = llm_gen(
                            query='professional_associations', 
                            description='''Professional associations that the business, organization, or individual belongs to, including relevant membership names and affiliations.''', 
                            website_text=website_text
                        )
                        llm_business_memberships_industry_memberships = llm_gen(
                            query='industry_memberships', 
                            description='''Memberships in industry-specific organizations, trade groups, chambers, or professional networks relevant to the business or its field.''', 
                            website_text=website_text
                        )
                        llm_business_memberships_botanical_societies = llm_gen(
                            query='botanical_societies', 
                            description='''Memberships or affiliations with botanical societies and organizations focused on botany, plant science, horticulture, or related fields.''', 
                            website_text=website_text
                        )
                        llm_business_memberships_herbal_associations = llm_gen(
                            query='herbal_associations', 
                            description='''Memberships or affiliations with herbal associations and organizations focused on herbalism, medicinal plants, phytotherapy, or related practices.''', 
                            website_text=website_text
                        )

                        # 26. Policies
                        llm_business_policies_privacy_policy = llm_gen(
                            query='privacy_policy', 
                            description='''A description of how the business collects, uses, stores, shares, and protects customers’ personal information, including any applicable privacy rights and choices.''', 
                            website_text=website_text
                        )
                        llm_business_policies_shipping_policy = llm_gen(
                            query='shipping_policy', 
                            description='''A description of the business’s shipping methods, delivery times, shipping costs, service areas, order processing times, and any shipping restrictions or conditions.''', 
                            website_text=website_text
                        )
                        llm_business_policies_returns_policy = llm_gen(
                            query='returns_policy', 
                            description='''A description of the business’s rules and procedures for returning products, including eligibility requirements, return timeframes, conditions, exclusions, and the return process.''', 
                            website_text=website_text
                        )
                        llm_business_policies_refund_policy = llm_gen(
                            query='refund_policy', 
                            description='''A description of when and how customers can receive refunds, including eligible circumstances, refund methods, processing times, deductions, and any applicable exclusions.''', 
                            website_text=website_text
                        )
                        llm_business_policies_sustainability_policy = llm_gen(
                            query='sustainability_policy', 
                            description='''A description of the business’s environmental and sustainability practices, commitments, initiatives, and policies relating to products, packaging, operations, sourcing, and waste.''', 
                            website_text=website_text
                        )
                        llm_business_policies_accessibility_policy = llm_gen(
                            query='accessibility_policy', 
                            description='''A description of the business’s commitment to accessibility, including accessible products, services, website features, accommodations, and how customers can request accessibility assistance.''', 
                            website_text=website_text
                        )

                        # 27. Languages
                        llm_business_languages_languages = llm_gen(
                            query='languages', 
                            description='''Identifies the languages supported by the business, website, or service, including the primary language and any additional languages available to customers.''', 
                            website_text=website_text
                        )
                        llm_business_languages_multilingual_support = llm_gen(
                            query='multilingual_support', 
                            description='''Indicates whether the business provides multilingual support, such as customer service, website content, staff assistance, or other services in multiple languages.''', 
                            website_text=website_text
                        )

                        # 28. Payment & Commerce
                        llm_business_commerce_accepted_payment_methods = llm_gen(
                            query='accepted_payment_methods', 
                            description='''The payment methods accepted by the business for purchases, such as credit cards, debit cards, PayPal, bank transfers, digital wallets, cash on delivery, or other supported payment options.''', 
                            website_text=website_text
                        )
                        llm_business_commerce_currencies = llm_gen(
                            query='currencies', 
                            description='''The currencies supported by the business for pricing, payments, and transactions, including the applicable currency codes or names.''', 
                            website_text=website_text
                        )
                        llm_business_commerce_online_store = llm_gen(
                            query='online_store', 
                            description='''Indicates whether the business operates an online store where customers can browse and purchase products or services through the website.''', 
                            website_text=website_text
                        )
                        llm_business_commerce_ecommerce = llm_gen(
                            query='ecommerce', 
                            description='''Information about the business’s ecommerce capabilities, including whether it sells products or services online and provides functionality for online purchasing and transactions.''', 
                            website_text=website_text
                        )

                        # 29. Shipping
                        llm_business_shipping_shipping_countries = llm_gen(
                            query='shipping_countries', 
                            description='''The countries where the business offers shipping or delivery for its products or services.''', 
                            website_text=website_text
                        )
                        llm_business_shipping_shipping_methods = llm_gen(
                            query='shipping_methods', 
                            description='''The available methods or options for shipping orders, such as standard, express, or expedited shipping.''', 
                            website_text=website_text
                        )
                        llm_business_shipping_international_shipping = llm_gen(
                            query='international_shipping', 
                            description='''Information about shipping orders internationally, including supported destinations, requirements, and any applicable conditions.''', 
                            website_text=website_text
                        )
                        llm_business_shipping_local_delivery = llm_gen(
                            query='local_delivery', 
                            description='''Information about delivery options available within the business's local service area, including coverage and delivery conditions.''', 
                            website_text=website_text
                        )

                        ###
                        output_items = []
                        output_item = parse_utils.organizations__business_create(
                            business_gmap_label = label,
                            business_gmap_name = name,
                            business_gmap_website = website,
                            ###
                            business_name_official = llm_business_name_official,
                            business_name_legal = llm_business_name_legal,
                            business_name_trade = llm_business_name_trade,
                            business_description = llm_business_description,
                            business_description_short = llm_business_description_short,
                            business_founded_year = llm_business_founded_year,
                            business_founding_story = llm_business_founding_story,
                            business_founder_names = llm_business_founder_names,
                            business_ownership_type = llm_business_ownership_type,
                            business_company_type = llm_business_company_type,
                            business_status = llm_business_status,
                            business_mission = llm_business_mission,
                            business_vision = llm_business_vision,
                            business_core_values = llm_business_core_values,
                            ###
                            business_type_primary = llm_business_type_primary,
                            business_type_secondary = llm_business_type_secondary,
                            business_industry = llm_business_industry,
                            business_niche = llm_business_niche,
                            business_model = llm_business_model,
                            ###
                            business_website = llm_business_website,
                            business_email = llm_business_email,
                            business_email_customer_service = llm_business_customer_service_email,
                            business_email_wholesale = llm_business_wholesale_email,
                            business_email_media = llm_business_media_email,
                            business_whatsapp = llm_business_whatsapp,
                            business_fax = llm_business_fax,
                            business_contact_form = llm_business_contact_form,
                            ###
                            business_headquarters = llm_business_headquarters,
                            business_address = llm_business_address,
                            business_city = llm_business_city,
                            business_state = llm_business_state,
                            business_region = llm_business_region,
                            business_country = llm_business_country,
                            business_postal_code = llm_business_postal_code,
                            business_latitude = llm_business_latitude,
                            business_longitude = llm_business_longitude,
                            business_additional_locations = llm_business_additional_locations,
                            business_farm_locations = llm_business_farm_locations,
                            business_nursery_locations = llm_business_nursery_locations,
                            business_factory_locations = llm_business_factory_locations,
                            business_laboratory_locations = llm_business_laboratory_locations,
                            business_warehouse_locations = llm_business_warehouse_locations,
                            business_retail_locations = llm_business_retail_locations,
                            ###
                            business_opening_hours = llm_business_opening_hours,
                            business_seasonal_hours = llm_business_seasonal_hours,
                            business_appointment_required = llm_business_appointment_required,
                            business_walk_in_available = llm_business_walk_in_available,
                            business_visitor_access = llm_business_visitor_access,
                            ###
                            business_medicinal_plants = llm_business_medicinal_plants,
                            business_primary_medicinal_plants = llm_business_primary_medicinal_plants,
                            business_specialty_plants = llm_business_specialty_plants,
                            business_native_plants = llm_business_native_plants,
                            business_rare_plants = llm_business_rare_plants,
                            business_medicinal_plant_categories = llm_business_medicinal_plant_categories,
                            business_botanical_collection_size = llm_business_botanical_collection_size,
                            ###
                            business_grows = llm_business_grows,
                            business_cultivates = llm_business_cultivates,
                            business_propagates = llm_business_propagates,
                            business_researches = llm_business_researches,
                            business_sells = llm_business_sells,
                            business_distributes = llm_business_distributes,
                            business_exports = llm_business_exports,
                            business_imports = llm_business_imports,
                            business_wild_harvests = llm_business_wild_harvests,
                            business_conserves = llm_business_conserves,
                            business_teaches = llm_business_teaches,
                            business_uses_in_products = llm_business_uses_in_products,
                            ###
                            business_products = llm_business_products,
                            business_product_categories = llm_business_product_categories,
                            business_flagship_products = llm_business_flagship_products,
                            business_product_forms = llm_business_product_forms,
                            business_herbal_teas = llm_business_herbal_teas,
                            business_tinctures = llm_business_tinctures,
                            business_extracts = llm_business_extracts,
                            business_essential_oils = llm_business_essential_oils,
                            business_capsules = llm_business_capsules,
                            business_powders = llm_business_powders,
                            business_dried_herbs = llm_business_dried_herbs,
                            business_fresh_herbs = llm_business_fresh_herbs,
                            business_seeds = llm_business_seeds,
                            business_seedlings = llm_business_seedlings,
                            business_roots = llm_business_roots,
                            business_bark = llm_business_bark,
                            business_flowers = llm_business_flowers,
                            business_fruits = llm_business_fruits,
                            business_resins = llm_business_resins,
                            business_cosmetics = llm_business_cosmetics,
                            business_soaps = llm_business_soaps,
                            business_creams = llm_business_creams,
                            business_salves = llm_business_salves,
                            business_syrups = llm_business_syrups,
                            ###
                            business_botanical_name = llm_business_botanical_name,
                            business_common_name = llm_business_common_name,
                            business_plant_part = llm_business_plant_part,
                            business_extraction_method = llm_business_extraction_method,
                            business_preparation_method = llm_business_preparation_method,
                            business_ingredients = llm_business_ingredients,
                            business_packaging = llm_business_packaging,
                            business_package_sizes = llm_business_package_sizes,
                            business_concentration = llm_business_concentration,
                            business_organic_product = llm_business_organic_product,
                            business_private_label = llm_business_private_label,
                            business_wholesale = llm_business_wholesale,
                            business_retail = llm_business_retail,
                            ###
                            business_herbal_consultation = llm_business_herbal_consultation,
                            business_herbal_clinic = llm_business_herbal_clinic,
                            business_medicinal_plant_consulting = llm_business_medicinal_plant_consulting,
                            business_plant_identification = llm_business_plant_identification,
                            business_botanical_identification = llm_business_botanical_identification,
                            business_cultivation_consulting = llm_business_cultivation_consulting,
                            business_contract_growing = llm_business_contract_growing,
                            business_contract_manufacturing = llm_business_contract_manufacturing,
                            business_private_label_manufacturing = llm_business_private_label_manufacturing,
                            business_extraction_services = llm_business_extraction_services,
                            business_drying_services = llm_business_drying_services,
                            business_milling = llm_business_milling,
                            business_grinding = llm_business_grinding,
                            business_packaging_service = llm_business_packaging_service,
                            business_export_services = llm_business_export_services,
                            business_laboratory_testing = llm_business_laboratory_testing,
                            business_formulation = llm_business_formulation,
                            business_research_services = llm_business_research_services,
                            business_education = llm_business_education,
                            business_workshops = llm_business_workshops,
                            business_courses = llm_business_courses,
                            business_farm_tours = llm_business_farm_tours,
                            business_botanical_tours = llm_business_botanical_tours,
                            ###
                            business_cultivation_methods = llm_business_cultivation_methods,
                            business_organic_cultivation = llm_business_organic_cultivation,
                            business_regenerative = llm_business_regenerative,
                            business_biodynamic = llm_business_biodynamic,
                            business_permaculture = llm_business_permaculture,
                            business_agroforestry = llm_business_agroforestry,
                            business_greenhouse = llm_business_greenhouse,
                            business_indoor = llm_business_indoor,
                            business_outdoor = llm_business_outdoor,
                            business_wild_harvesting = llm_business_wild_harvesting,
                            business_sustainable_wild_harvesting = llm_business_sustainable_wild_harvesting,
                            business_propagation_methods = llm_business_propagation_methods,
                            business_irrigation = llm_business_irrigation,
                            business_fertilization = llm_business_fertilization,
                            business_soil_management = llm_business_soil_management,
                            business_pest_management = llm_business_pest_management,
                            business_harvest_methods = llm_business_harvest_methods,
                            business_harvest_season = llm_business_harvest_season,
                            ###
                            business_manufacturing = llm_business_manufacturing,
                            business_processing = llm_business_processing,
                            business_extraction = llm_business_extraction,
                            business_distillation = llm_business_distillation,
                            business_fermentation = llm_business_fermentation,
                            business_drying = llm_business_drying,
                            business_manufacturing_milling = llm_business_manufacturing_milling,
                            business_manufacturing_grinding = llm_business_manufacturing_grinding,
                            business_blending = llm_business_blending,
                            business_manufacturing_formulation = llm_business_manufacturing_formulation,
                            business_encapsulation = llm_business_encapsulation,
                            business_manufacturing_packaging = llm_business_manufacturing_packaging,
                            business_quality_testing = llm_business_quality_testing,
                            business_batch_testing = llm_business_batch_testing,
                            business_traceability = llm_business_traceability,
                            ###
                            business_facilities_farms = llm_business_facilities_farms,
                            business_facilities_nurseries = llm_business_facilities_nurseries,
                            business_facilities_laboratories = llm_business_facilities_laboratories,
                            business_facilities_factories = llm_business_facilities_factories,
                            business_facilities_warehouses = llm_business_facilities_warehouses,
                            business_facilities_botanical_gardens = llm_business_facilities_botanical_gardens,
                            business_facilities_greenhouses = llm_business_facilities_greenhouses,
                            business_facilities_visitor_centers = llm_business_facilities_visitor_centers,
                            business_facilities_research_centers = llm_business_facilities_research_centers,
                            business_facilities_education_centers = llm_business_facilities_education_centers,
                            business_facilities_clinics = llm_business_facilities_clinics,
                            business_facilities_retail_stores = llm_business_facilities_retail_stores,
                            ###
                            business_certifications_certifications = llm_business_certifications_certifications,
                            business_certifications_certification_name = llm_business_certifications_certification_name,
                            business_certifications_certification_number = llm_business_certifications_certification_number,
                            business_certifications_issuing_organization = llm_business_certifications_issuing_organization,
                            business_certifications_issue_date = llm_business_certifications_issue_date,
                            business_certifications_expiry_date = llm_business_certifications_expiry_date,
                            business_certifications_certification_scope = llm_business_certifications_certification_scope,
                            ###
                            business_quality_quality_control = llm_business_quality_quality_control,
                            business_quality_laboratory_testing = llm_business_quality_laboratory_testing,
                            business_quality_batch_testing = llm_business_quality_batch_testing,
                            business_quality_third_party_testing = llm_business_quality_third_party_testing,
                            business_quality_traceability = llm_business_quality_traceability,
                            business_quality_quality_management_system = llm_business_quality_quality_management_system,
                            ###
                            business_sustainability_sustainability_policy = llm_business_sustainability_sustainability_policy,
                            business_sustainability_conservation = llm_business_sustainability_conservation,
                            business_sustainability_biodiversity = llm_business_sustainability_biodiversity,
                            business_sustainability_regenerative_agriculture = llm_business_sustainability_regenerative_agriculture,
                            business_sustainability_ethical_sourcing = llm_business_sustainability_ethical_sourcing,
                            business_sustainability_fair_trade = llm_business_sustainability_fair_trade,
                            business_sustainability_community_projects = llm_business_sustainability_community_projects,
                            business_sustainability_indigenous_partnerships = llm_business_sustainability_indigenous_partnerships,
                            business_sustainability_local_sourcing = llm_business_sustainability_local_sourcing,
                            business_sustainability_recyclable_packaging = llm_business_sustainability_recyclable_packaging,
                            business_sustainability_carbon_reduction = llm_business_sustainability_carbon_reduction,
                            business_sustainability_water_conservation = llm_business_sustainability_water_conservation,
                            ###
                            business_research_research_programs = llm_business_research_research_programs,
                            business_research_research_projects = llm_business_research_research_projects,
                            business_research_publications = llm_business_research_publications,
                            business_research_patents = llm_business_research_patents,
                            business_research_university_partnerships = llm_business_research_university_partnerships,
                            business_research_clinical_trials = llm_business_research_clinical_trials,
                            business_research_ethnobotanical_research = llm_business_research_ethnobotanical_research,
                            business_research_pharmacognosy = llm_business_research_pharmacognosy,
                            business_research_phytochemistry = llm_business_research_phytochemistry,
                            business_research_plant_breeding = llm_business_research_plant_breeding,
                            ###
                            business_education_courses = llm_business_education_courses,
                            # business_education_workshops = llm_business_education_workshops,
                            business_education_webinars = llm_business_education_webinars,
                            # business_education_apprenticeships = llm_business_education_apprenticeships,
                            business_education_lectures = llm_business_education_lectures,
                            # business_education_botanical_walks = llm_business_education_botanical_walks,
                            # business_education_farm_tours = llm_business_education_farm_tours,
                            # business_education_certifications_offered = llm_business_education_certifications_offered,
                            ###
                            business_traditional_medicine_systems_ayurveda = llm_business_traditional_medicine_systems_ayurveda,
                            business_traditional_medicine_systems_traditional_chinese_medicine = llm_business_traditional_medicine_systems_traditional_chinese_medicine,
                            business_traditional_medicine_systems_western_herbalism = llm_business_traditional_medicine_systems_western_herbalism,
                            business_traditional_medicine_systems_unani = llm_business_traditional_medicine_systems_unani,
                            business_traditional_medicine_systems_kampo = llm_business_traditional_medicine_systems_kampo,
                            business_traditional_medicine_systems_tibetan_medicine = llm_business_traditional_medicine_systems_tibetan_medicine,
                            business_traditional_medicine_systems_indigenous_medicine = llm_business_traditional_medicine_systems_indigenous_medicine,
                            business_traditional_medicine_systems_african_traditional_medicine = llm_business_traditional_medicine_systems_african_traditional_medicine,
                            ###
                            business_expertise_expertise_topics = llm_business_expertise_expertise_topics,
                            business_expertise_medicinal_plant_cultivation = llm_business_expertise_medicinal_plant_cultivation,
                            business_expertise_herbal_formulation = llm_business_expertise_herbal_formulation,
                            business_expertise_ethnobotany = llm_business_expertise_ethnobotany,
                            business_expertise_pharmacognosy = llm_business_expertise_pharmacognosy,
                            # business_expertise_botanical_identification = llm_business_expertise_botanical_identification,
                            business_expertise_herbal_medicine = llm_business_expertise_herbal_medicine,
                            business_expertise_conservation = llm_business_expertise_conservation,
                            # business_expertise_plant_propagation = llm_business_expertise_plant_propagation,

                            business_people_founders = llm_business_people_founders,
                            business_people_owners = llm_business_people_owners,
                            business_people_ceo = llm_business_people_ceo,
                            business_people_president = llm_business_people_president,
                            business_people_director = llm_business_people_director,
                            business_people_botanists = llm_business_people_botanists,
                            business_people_herbalists = llm_business_people_herbalists,
                            # business_people_researchers = llm_business_people_researchers,
                            # business_people_agronomists = llm_business_people_agronomists,
                            # business_people_pharmacists = llm_business_people_pharmacists,
                            business_people_educators = llm_business_people_educators,
                            # business_people_laboratory_directors = llm_business_people_laboratory_directors,
                            business_people_farm_managers = llm_business_people_farm_managers,

                            business_markets_customer_types = llm_business_markets_customer_types,
                            business_markets_industries_served = llm_business_markets_industries_served,
                            business_markets_export_markets = llm_business_markets_export_markets,
                            # business_markets_import_markets = llm_business_markets_import_markets,
                            business_markets_countries_served = llm_business_markets_countries_served,
                            business_markets_regions_served = llm_business_markets_regions_served,
                            business_markets_international_shipping = llm_business_markets_international_shipping,
                            business_markets_wholesale_available = llm_business_markets_wholesale_available,
                            business_markets_retail_available = llm_business_markets_retail_available,
                            business_markets_private_label_available = llm_business_markets_private_label_available,

                            business_online_presence_facebook = llm_business_online_presence_facebook,
                            business_online_presence_instagram = llm_business_online_presence_instagram,
                            business_online_presence_linkedin = llm_business_online_presence_linkedin,
                            business_online_presence_youtube = llm_business_online_presence_youtube,
                            business_online_presence_x = llm_business_online_presence_x,
                            business_online_presence_pinterest = llm_business_online_presence_pinterest,
                            business_online_presence_tiktok = llm_business_online_presence_tiktok,
                            # business_online_presence_github = llm_business_online_presence_github,
                            # business_online_presence_wikipedia = llm_business_online_presence_wikipedia,

                            business_awards_awards = llm_business_awards_awards,
                            # business_awards_award_name = llm_business_awards_award_name,
                            # business_awards_award_year = llm_business_awards_award_year,
                            # business_awards_awarding_organization = llm_business_awards_awarding_organization,

                            # business_memberships_professional_associations = llm_business_memberships_professional_associations,
                            # business_memberships_industry_memberships = llm_business_memberships_industry_memberships,
                            # business_memberships_botanical_societies = llm_business_memberships_botanical_societies,
                            # business_memberships_herbal_associations = llm_business_memberships_herbal_associations,

                            business_policies_privacy_policy = llm_business_policies_privacy_policy,
                            business_policies_shipping_policy = llm_business_policies_shipping_policy,
                            # business_policies_returns_policy = llm_business_policies_returns_policy,
                            # business_policies_refund_policy = llm_business_policies_refund_policy,
                            business_policies_sustainability_policy = llm_business_policies_sustainability_policy,
                            business_policies_accessibility_policy = llm_business_policies_accessibility_policy,

                            business_languages_languages = llm_business_languages_languages,
                            business_languages_multilingual_support = llm_business_languages_multilingual_support,

                            business_commerce_accepted_payment_methods = llm_business_commerce_accepted_payment_methods,
                            business_commerce_currencies = llm_business_commerce_currencies,
                            business_commerce_online_store = llm_business_commerce_online_store,
                            business_commerce_ecommerce = llm_business_commerce_ecommerce,

                            business_shipping_shipping_countries = llm_business_shipping_shipping_countries,
                            business_shipping_shipping_methods = llm_business_shipping_shipping_methods,
                            business_shipping_international_shipping = llm_business_shipping_international_shipping,
                            business_shipping_local_delivery = llm_business_shipping_local_delivery,

                            source_name = 'Website',
                            source_acronym = 'WEBSITE',
                        )
                        output_items.append(output_item)
                        io.json_write(output_filepath, output_items)
                        ###
                        item = output_items[0]
                        print(output_filepath)
                        none_count = 0
                        empty_count = 0
                        value_count = 0
                        for key, val in item.items():
                            if val == None: none_count += 1
                            elif val == '': empty_count += 1
                            else: value_count += 1
                        total_count = none_count + empty_count + value_count
                        print(f'NONE: {none_count}/{total_count} - {none_count/total_count*100}')
                        print(f'EMPTY: {empty_count}/{total_count} - {empty_count/total_count*100}')
                        print(f'VALUE: {value_count}/{total_count} - {value_count/total_count*100}')
                        # quit()

def analyse_website():
    output_folderpath = f'{g.DATA_FOLDERPATH}/organizations/parse/website/json'
    # try: shutil.rmtree(output_folderpath)
    # except: pass
    io.folders_recursive_gen(output_folderpath)
    ###
    input_foldername = f'{g.DATA_FOLDERPATH}/organizations/fetch/gmap/america/places'.replace(' ', '_')
    input_filenames = sorted(os.listdir(input_foldername))
    for input_filename in input_filenames[:10]:
        input_filename_base = input_filename.split('.')[0].strip()
        input_filepath = f'{input_foldername}/{input_filename}'
        with open(input_filepath, encoding="utf-8") as f: rows = f.read().strip().split('\n')
        for row in rows:
            values = row.split('~')
            if values != [] and values != ['']:
                label = values[0]
                website = values[2]
                slug = to_slug(label)
                print(f'label: {label}')
                print(f'website: {website}')
                print(f'slug: {slug}')
                print(f'***************************************')
                print()
                ###
                output_filepath = f'{output_folderpath}/{slug}.json'
                data = io.json_read(output_filepath)
                item = data[0]
                none_count = 0
                empty_count = 0
                value_count = 0
                for key, val in item.items():
                    if val == None: none_count += 1
                    elif val == '': empty_count += 1
                    else: value_count += 1
                total_count = none_count + empty_count + value_count
                print(f'NONE: {none_count}/{total_count} - {none_count/total_count*100}')
                print(f'EMPTY: {empty_count}/{total_count} - {empty_count/total_count*100}')
                print(f'VALUE: {value_count}/{total_count} - {value_count/total_count*100}')
                quit()

def analyse_jsons():
    input_folderpath = f'{HUB_FOLDERPATH}/parse/website/json'
    input_filenames = sorted(os.listdir(input_folderpath))
    i = 0
    fields = []
    for input_filename in input_filenames[:]:
        i += 1
        input_filepath = f'{input_folderpath}/{input_filename}'
        data = io.json_read(input_filepath)[0]
        for key, val in data.items():
            found = False        
            for field in fields:
                if field['name'] == key:
                    none_count = 0
                    empty_count = 0
                    value_count = 0
                    if val == None: none_count += 1
                    elif val == '': empty_count += 1
                    else: value_count += 1
                    field['analytics']['none'] += none_count
                    field['analytics']['empty'] += empty_count
                    field['analytics']['value'] += value_count
                    ###
                    found = True        
                    break
            if not found:
                none_count = 0
                empty_count = 0
                value_count = 0
                if val == None: none_count += 1
                elif val == '': empty_count += 1
                else: value_count += 1
                item_new = {
                    'name': key,
                    'analytics': {
                        'none': none_count,
                        'empty': empty_count,
                        'value': value_count,
                    },
                }
                fields.append(item_new)

    # print(json.dumps(fields, indent=4))

    fields = sorted(fields, key=lambda x: x["analytics"]["value"], reverse=True)

    print(json.dumps(fields, indent=4))
    quit()

def run():
    print(f'ORGANIZATION >> PARSE >> main')

    # parse_website_backup()

    start = time.perf_counter()
    parse_website()
    print(f'''
################################################################################
parse website() - execution time: 
---
SECONDS: {(time.perf_counter() - start)}
MINUTES: {(time.perf_counter() - start)/60}
HOURS:   {(time.perf_counter() - start)/60/60}
################################################################################
    ''')

    # analyse_website()
    # analyse_jsons()

