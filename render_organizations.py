import csv
import json

from lib import io
import re
import unicodedata

def normalize_name(raw_name: str) -> str:
    """
    Convert a raw USDA operation name into a clean canonical name.
    Example:
        '"BREDUN" LP' -> 'BREDUN LP'
    """
    if not raw_name:
        return ""

    # Normalize Unicode characters
    name = unicodedata.normalize("NFKC", raw_name)

    # Remove surrounding quotation marks
    name = name.replace('"', '').replace("'", "")

    # Collapse multiple whitespace characters
    name = re.sub(r"\s+", " ", name)

    return name.strip()


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

def render_listing():
    url_slug = f'organizations/'

def gen():
    print(f'ORGANIZATIONS >> RENDER >> ALL')

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
            render_listing()
