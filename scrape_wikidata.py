import requests

url = "https://www.wikidata.org/wiki/Special:EntityData/Q37153.json"
url = "https://www.wikidata.org/w/api.php?action=wbgetentities&ids=Q37153|P31|Q5&props=labels&languages=en&format=json"

headers = {
    "User-Agent": "MyWikidataApp/1.0 (your_email@example.com) requests"
}

response = requests.get(url, headers=headers)
response.raise_for_status()

data = response.json()
print(data["entities"]["Q37153"]["labels"]["en"]["value"])
print(data["entities"])

quit()

def triples_resolution_sparql():
    import sys
    from SPARQLWrapper import SPARQLWrapper, JSON

    endpoint_url = "https://query.wikidata.org/sparql"

    query = """
    SELECT ?plant ?plantLabel ?use ?useLabel WHERE {
      ?plant wdt:P31/wdt:P279* wd:Q207123 .
      OPTIONAL { ?plant wdt:P366 ?use . }

      SERVICE wikibase:label {
        bd:serviceParam wikibase:language "en".
      }
    }
    LIMIT 200
    """


    def get_results(endpoint_url, query):
        user_agent = "WDQS-example Python/%s.%s" % (sys.version_info[0], sys.version_info[1])
        # TODO adjust user agent; see https://w.wiki/CX6
        sparql = SPARQLWrapper(endpoint_url, agent=user_agent)
        sparql.setQuery(query)
        sparql.setReturnFormat(JSON)
        return sparql.query().convert()


    for i in range(2):
        results = get_results(endpoint_url, query)

        for result in results["results"]["bindings"]:
            print(result)

        print(len(results["results"]["bindings"]))



def triples_extraction():
    import json
    from lib import io

    label_map = [
        {'id': 'Q37153', 'value': 'Aguacate',},
        {'id': 'P366', 'value': 'has use',},
    ]

    wikidata_folderpath = f'/home/ubuntu/vault/terrawhisper/database/ssot/wikidata'
    wikidata_filepath = f'{wikidata_folderpath}/label-map.json'

    label_map = io.json_read(wikidata_filepath, create=True)

    s_id = 'Q37153'
    with open(f"{wikidata_folderpath}/{subject_id}.json", "r", encoding="utf-8") as f:
        json_data = json.load(f)

    claims = data['entities'][subject_id]['claims']

    quit()

    subject_id = 'Q37153'
    predicate_id = 'P366'
    with open(f"{subject_id}.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    # print(json.dumps(data['entities'][subject]['claims']['P366'], indent=4))

    claims = data['entities'][subject_id]['claims']

    for claim in claims:
        subject_value = [item['value'] for item in label_map if item['id'] == subject_id][0]
        # _predicate = claim
        # _object = claim['mainsnak']['datavalue']['value']['id']

        # triple = f'{_subject} -> {_predicate} -> {_object}'
        # print(triple)
        predicate_id = claim
        predicate_data = claims[predicate_id]
        if predicate_id == 'P366':
            for predicate_item in predicate_data:
                # print(predicate_item)
                o_value = predicate_item['mainsnak']['datavalue']['value']
                print(o_value)
                # predicate_values = [item['value'] for item in label_map if item['id'] == predicate_id]
                # print(predicate_values)
            quit()
        predicate_values = [item['value'] for item in label_map if item['id'] == predicate_id]
        if predicate_values != []:
            predicate_value = predicate_values[0]
        else:
            predicate_value = predicate_id
        
        # print(claims[claim])
        print(subject_value, '->', predicate_value, '->', claims[claim][0]['mainsnak']['datavalue']['value'])

    # TODO
    # https://www.wikidata.org/w/api.php?action=wbgetentities&ids=Q37153|P31|Q5&props=labels&languages=en&format=json

triples_extraction()

quit()

import requests

def fetch_entities(qids):
    ids = "|".join(qids)
    url = "https://www.wikidata.org/w/api.php"
    
    params = {
        "action": "wbgetentities",
        "ids": ids,
        "format": "json",
        "languages": "en"
    }
    
    return requests.get(url, params=params).json()["entities"]

fetch_entities(['Q37153'])

quit()

# pip install sparqlwrapper
# https://rdflib.github.io/sparqlwrapper/

import sys
from SPARQLWrapper import SPARQLWrapper, JSON

endpoint_url = "https://query.wikidata.org/sparql"

query = """
SELECT ?item ?itemLabel
WHERE
{
  ?item wdt:P366 wd:Q188840. # Must be a cat
  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],mul,en". }
}
LIMIT 500 OFFSET 0
"""


def get_results(endpoint_url, query):
    user_agent = "WDQS-example Python/%s.%s" % (sys.version_info[0], sys.version_info[1])
    # TODO adjust user agent; see https://w.wiki/CX6
    sparql = SPARQLWrapper(endpoint_url, agent=user_agent)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    return sparql.query().convert()


for i in range(2):
    results = get_results(endpoint_url, query)

    for result in results["results"]["bindings"]:
        print(result)

    print(len(results["results"]["bindings"]))
