import requests
import json
import os
import time

from lib import g
from lib import io

import masterize_utils
import reference_utils

def run():
    '''
    import requests

    query = """
    SELECT ?item ?itemLabel WHERE {
      ?item wdt:P225 "Achillea millefolium".
      SERVICE wikibase:label {
        bd:serviceParam wikibase:language "en".
      }
    }
    """

    response = requests.get(
        "https://query.wikidata.org/sparql",
        params={"query": query, "format": "json"},
        headers={"User-Agent": "Python"}
    )

    data = response.json()

    for row in data["results"]["bindings"]:
        print("QID:", row["item"]["value"])
        print("Label:", row["itemLabel"]["value"])
    '''

    '''
    import requests

    query = """
    SELECT ?item ?ipni WHERE {
      ?item p:P961 ?statement .
      ?statement ps:P961 ?ipni .
      FILTER(?ipni = "2294-2")
    }
    """

    r = requests.get(
        "https://query.wikidata.org/sparql",
        params={"query": query, "format": "json"},
        headers={"User-Agent": "Python"}
    )

    print(r.json())

    '''


    '''
    import requests

    query = """
    SELECT ?item WHERE {
      ?item wdt:P5037 "urn:lsid:ipni.org:names:2294-2".
    }
    """

    r = requests.get(
        "https://query.wikidata.org/sparql",
        params={"query": query, "format": "json"},
        headers={"User-Agent": "Python"}
    )

    print(r.json())
    '''


    def download_entity(qid):

        API = "https://www.wikidata.org/w/api.php"

        r = requests.get(
            API,
            params={
                "action": "wbgetentities",
                "ids": qid,
                "format": "json"
            },
            headers={
                "User-Agent": "MedicinalPlantsBot/1.0"
            }
        )

        r.raise_for_status()

        return r.json()

    source_name = 'wikidata'
    output_foldername = f'fetch'
    ipni_output_folderpath = f'{g.DATA_FOLDERPATH}/{output_foldername}/{source_name}/qids_ipni'
    powo_output_folderpath = f'{g.DATA_FOLDERPATH}/{output_foldername}/{source_name}/qids_powo'
    taxon_output_folderpath = f'{g.DATA_FOLDERPATH}/{output_foldername}/{source_name}/qids_taxon'
    # try: shutil.rmtree(ipni_output_folderpath)
    # except: pass
    io.folders_recursive_gen(ipni_output_folderpath)
    io.folders_recursive_gen(powo_output_folderpath)
    io.folders_recursive_gen(taxon_output_folderpath)

    '''
    plants_rows = masterize_utils.masterize_plants_get_all()
    ipni_ids = []
    for plant_row in plants_rows:
        plant_name_normalized = plant_row[2]
        wcvp_plant_name_row = reference_utils.wcvp_plant_name_get_row(plant_name_normalized)
        ipni_id = wcvp_plant_name_row[5]
        ipni_ids.append(ipni_id)

    ipni_ids_filenames_base = [x.split('.')[0] for x in os.listdir(ipni_output_folderpath)]
    ipni_ids_new = []
    ipni_ids_old = []
    for ipni_id in ipni_ids:
        if ipni_id not in ipni_ids_filenames_base:
            ipni_ids_new.append(ipni_id)
        if ipni_id in ipni_ids_filenames_base:
            ipni_ids_old.append(ipni_id)
        
    print(len(ipni_ids_new))
    print(len(ipni_ids_old))
    print(len(ipni_ids_old) + len(ipni_ids_new))
    print(len(ipni_ids))

    # quit()

    tries = 0
    for i in range(0, len(ipni_ids_new), 50):
        print(f'{i}/{len(ipni_ids_new)}')
        batch = ipni_ids[i:i+20]
        values = "\n".join(f'"{x}"' for x in batch)
        query = f"""
            SELECT ?ipni ?item WHERE {{
                VALUES ?ipni {{
                    {values}
                }}
                ?item wdt:P961 ?ipni .
            }}
        """
        r = requests.get(
            "https://query.wikidata.org/sparql",
            params={
                "query": query,
                "format": "json"
            },
            headers={
                "User-Agent": "MedicinalPlantsBot/1.0"
            }
        )
        r.raise_for_status()
        data = r.json()
        qids = {
            x["ipni"]["value"]:
            x["item"]["value"].split("/")[-1]
            for x in data["results"]["bindings"]
        }
        for key, value in qids.items():
            # print(key, value)
            io.json_write(f'{ipni_output_folderpath}/{key}.json', {'ipni_id': key, 'qid': value})
        
        time.sleep(10)

        tries += 1
        if tries >= 30:
            time.sleep(60)
            tries = 0
        # print(json.dumps(qids_data, indent=4))
        # quit()
    quit()
    '''

    '''
    ### POWO IDS
    plants_rows = masterize_utils.masterize_plants_get_all()
    powo_ids = []
    for plant_row in plants_rows:
        plant_name_normalized = plant_row[2]
        wcvp_plant_name_row = reference_utils.wcvp_plant_name_get_row(plant_name_normalized)
        powo_id = wcvp_plant_name_row[6]
        powo_ids.append(powo_id)

    powo_ids_filenames_base = [x.split('.')[0] for x in os.listdir(powo_output_folderpath)]
    powo_ids_new = []
    powo_ids_old = []
    for powo_id in powo_ids:
        if powo_id not in powo_ids_filenames_base:
            powo_ids_new.append(powo_id)
        if powo_id in powo_ids_filenames_base:
            powo_ids_old.append(powo_id)

    print(len(powo_ids_new))
    print(len(powo_ids_old))
    print(len(powo_ids_old) + len(powo_ids_new))
    print(len(powo_ids))

    tries = 0
    for i in range(0, len(powo_ids_new), 50):
        print(f'{i}/{len(powo_ids_new)}')
        batch = powo_ids[i:i+50]
        values = "\n".join(
            f'"urn:lsid:ipni.org:names:{powo_id}"'
            for powo_id in batch
        )
        query = f"""
            SELECT ?powo ?item WHERE {{
                VALUES ?powo {{
                    {values}
                }}
                ?item wdt:P5037 ?powo .
            }}
        """

        r = requests.get(
            "https://query.wikidata.org/sparql",
            params={
                "query": query,
                "format": "json"
            },
            headers={
                "User-Agent": "MedicinalPlantsBot/1.0"
            }
        )

        r.raise_for_status()

        data = r.json()

        qids = {
            x["powo"]["value"].replace("urn:lsid:ipni.org:names:", ""):
            x["item"]["value"].split("/")[-1]
            for x in data["results"]["bindings"]
        }

        for key, value in qids.items():
            # print(key, value)
            io.json_write(f'{powo_output_folderpath}/{key}.json', {'powo_id': key, 'qid': value})
        
        time.sleep(10)

        tries += 1
        if tries >= 30:
            time.sleep(60)
            tries = 0

        # quit()

    '''

    '''
    ### WCVP TAXON IDS
    plants_rows = masterize_utils.masterize_plants_get_all()
    taxon_names = []
    for plant_row in plants_rows:
        plant_name_normalized = plant_row[2]
        wcvp_plant_name_row = reference_utils.wcvp_plant_name_get_row(plant_name_normalized)
        taxon_name = wcvp_plant_name_row[3]
        taxon_names.append(taxon_name)

    taxon_names_filenames_base = [x.split('.')[0] for x in os.listdir(taxon_output_folderpath)]
    taxon_names_new = []
    taxon_names_old = []
    for taxon_name in taxon_names:
        if taxon_name not in taxon_names_filenames_base:
            taxon_names_new.append(taxon_name)
        if taxon_name in taxon_names_filenames_base:
            taxon_names_old.append(taxon_name)

    print(len(taxon_names_new))
    print(len(taxon_names_old))
    print(len(taxon_names_old) + len(taxon_names_new))
    print(len(taxon_names))

    tries = 0
    for i in range(0, len(taxon_names_new), 50):
        print(f'{i}/{len(taxon_names_new)}')
        batch = taxon_names_new[i:i+50]
        ###
        values = "\n".join(
            f'"{name}"'
            for name in batch
        )
        query = f"""
            SELECT ?taxon_name ?item WHERE {{
                VALUES ?taxon_name {{
                    {values}
                }}
                ?item wdt:P225 ?taxon_name .
            }}
        """
        r = requests.get(
            "https://query.wikidata.org/sparql",
            params={
                "query": query,
                "format": "json"
            },
            headers={
                "User-Agent": "MedicinalPlantsBot/1.0"
            }
        )
        r.raise_for_status()
        data = r.json()
        qids = {
            x["taxon_name"]["value"]:
            x["item"]["value"].split("/")[-1]
            for x in data["results"]["bindings"]
        }
        ###
        for key, value in qids.items():
            # print(key, value)
            io.json_write(f'{taxon_output_folderpath}/{key}.json', {'taxon_name': key, 'qid': value})
        time.sleep(10)
        tries += 1
        if tries >= 30:
            time.sleep(60)
            tries = 0
    quit()
    '''

    ### QIDS JSONS
    qids_output_folderpath = f'{g.DATA_FOLDERPATH}/{output_foldername}/{source_name}/qids'
    io.folders_recursive_gen(qids_output_folderpath)

    qids = set()

    ipni_filenames = sorted(os.listdir(ipni_output_folderpath))
    for i, ipni_filename in enumerate(ipni_filenames):
        print(f'{i}/{len(ipni_filenames)}')
        ipni_filepath = f'{ipni_output_folderpath}/{ipni_filename}'
        data = io.json_read(ipni_filepath)
        qid = data['qid']
        qids.add(qid)

    powo_filenames = sorted(os.listdir(powo_output_folderpath))
    for i, powo_filename in enumerate(powo_filenames):
        print(f'{i}/{len(powo_filenames)}')
        powo_filepath = f'{powo_output_folderpath}/{powo_filename}'
        data = io.json_read(powo_filepath)
        qid = data['qid']
        qids.add(qid)

    taxon_filenames = sorted(os.listdir(taxon_output_folderpath))
    for i, taxon_filename in enumerate(taxon_filenames):
        print(f'{i}/{len(taxon_filenames)}')
        taxon_filepath = f'{taxon_output_folderpath}/{taxon_filename}'
        try: data = io.json_read(taxon_filepath)
        except: continue
        qid = data['qid']
        qids.add(qid)

    qids = sorted(list(qids))

    qids_filenames_base = [x.split('.')[0] for x in os.listdir(qids_output_folderpath)]
    qids_new = []
    qids_old = []
    for qid in qids:
        if qid not in qids_filenames_base:
            qids_new.append(qid)
        if qid in qids_filenames_base:
            qids_old.append(qid)

    print(len(qids_new))
    print(len(qids_old))
    print(len(qids_old) + len(qids_new))
    print(len(qids))

    tries = 0
    BATCH = 50
    for i in range(0, len(qids_new), BATCH):
        print(f'{i}/{len(qids_new)}')
        batch = qids_new[i:i+BATCH]
        r = requests.get(
            "https://www.wikidata.org/w/api.php",
            params={
                "action": "wbgetentities",
                "ids": "|".join(batch),
                "format": "json"
            },
            headers={
                "User-Agent": "MedicinalPlantsBot/1.0"
            }
        )
        r.raise_for_status()
        entities = r.json()["entities"]
        for qid, entity in entities.items():
            io.json_write(f'{qids_output_folderpath}/{qid}.json', entity)

        time.sleep(10)
        tries += 1
        if tries >= 30:
            time.sleep(60)
            tries = 0
