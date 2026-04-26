import os
import json
import time
import random
import shutil
import sqlite3
import requests

from neo4j import GraphDatabase

from lib import g
from lib import io
from lib import llm
from lib import data

kg_folderpath = f'/{g.SSOT_FOLDERPATH}/kg'
wikidata_folderpath = f'{g.SSOT_FOLDERPATH}/wikidata'
# taxdmp_folderpath = f'{wikidata_folderpath}/taxdmp'
# taxdmp_nodes_filepath = f'{taxdmp_folderpath}/nodes.dmp'
# taxdmp_names_filepath = f'{taxdmp_folderpath}/names.dmp'
sqlite_database_filepath = f'{kg_folderpath}/taxonomy.db'
lotus_filepath = f'{g.SSOT_FOLDERPATH}/lotus/lotusUniqueNaturalProduct.bson'
lotus_output_filepath = f'{g.SSOT_FOLDERPATH}/lotus/output.json'
herb20_filepath = f'{g.SSOT_FOLDERPATH}/herb20/HERB_herb_info_v2.txt'
pubchem_folderpath = f'{g.SSOT_FOLDERPATH}/pubchem'

def chunks(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i+n]

########################################
# DUMPS
########################################
def pubchem_properties_batches_to_single_by_inchikey():
    batches_folderpath = f'{g.SSOT_FOLDERPATH}/pubchem/oregano-batches'
    batches_filepaths = sorted([f'{batches_folderpath}/{filename}' for filename in os.listdir(batches_folderpath)])
    print(batches_filepaths)
    for batch_i, batch_filepath in enumerate(batches_filepaths):
        print(f'{batch_i}/{len(batches_filepaths)}')
        batch_data = io.json_read(batch_filepath)
        items_export = batch_data['PropertyTable']['Properties']
        for item_export in items_export:
            item_export_filepath = f'''{g.SSOT_FOLDERPATH}/pubchem/compounds-inchikey/{item_export['InChIKey']}.json'''
            io.json_write(item_export_filepath, item_export)
            # print(item_export_filepath)
        # print(batch_data)
        # quit()

def lotus_bson_to_json():
    export_items = []
    docs_num = 0
    parent_count = 0
    class_count = 0
    superclass_count = 0
    kingdom_count = 0
    npclassifier_pathway_count = 0
    npclassifier_superclass_count = 0
    npclassifier_class_count = 0
    inchikey_count = 0
    for doc_i, doc in enumerate(first_n_bson(lotus_filepath, 1000000)):
        # print(doc["inchikey"])
        print(json.dumps(doc, indent=4, default=str))
        quit()
        docs_num += 1
        component_lotus_id = doc['lotus_id']
        try: component_wikidata_id = doc['wikidata_id']
        except: component_wikidata_id = None
        print(doc_i)
        found = True
        try: component_taxonomy_classyfire_parent = doc['chemicalTaxonomyClassyfireDirectParent']
        except: 
            component_taxonomy_classyfire_parent = None
            parent_count += 1
            found = False
        try: component_taxonomy_classyfire_class = doc['chemicalTaxonomyClassyfireClass']
        except: 
            component_taxonomy_classyfire_class = None
            class_count += 1
            found = False
        try: component_taxonomy_classyfire_superclass = doc['chemicalTaxonomyClassyfireSuperclass']
        except: 
            component_taxonomy_classyfire_superclass = None
            superclass_count += 1
            found = False
        try: component_taxonomy_classyfire_kingdom = doc['chemicalTaxonomyClassyfireKingdom']
        except: 
            component_taxonomy_classyfire_kingdom = None
            kingdom_count += 1
            found = False
        try: component_taxonomy_npclassifier_pathway = doc['chemicalTaxonomyNPclassifierPathway']
        except: 
            component_taxonomy_npclassifier_pathway = None
            npclassifier_pathway_count += 1
            found = False
        try: component_taxonomy_npclassifier_superclass = doc['chemicalTaxonomyNPclassifierSuperclass']
        except: 
            component_taxonomy_npclassifier_superclass = None
            npclassifier_superclass_count += 1
            found = False
        try: component_taxonomy_npclassifier_class = doc['chemicalTaxonomyNPclassifierClass']
        except: 
            component_taxonomy_npclassifier_class = None
            npclassifier_class_count += 1
            found = False
        try: component_inchikey = doc['inchikey']
        except: 
            component_inchikey = None
            inchikey_count += 1
            found = False
        # if not found:
            # print(json.dumps(doc, indent=4, default=str))
            # quit()
        # print(component_lotus_id, component_taxonomy_classyfire_class)
        plant_names = []
        for ref_id in doc.get("taxonomyReferenceObjects", {}):
            for source in doc["taxonomyReferenceObjects"][ref_id]:
                for org in doc["taxonomyReferenceObjects"][ref_id][source]:
                    plant_name = org.get("organism_value")
                    if plant_name and plant_name not in plant_names:
                        plant_names.append(plant_name)
        export_item = {
            'component_lotus_id': component_lotus_id,
            'component_inchikey': component_inchikey,
            'component_wikidata_id': component_wikidata_id,
            'component_taxonomy_npclassifier_pathway': component_taxonomy_npclassifier_pathway,
            'component_taxonomy_npclassifier_superclass': component_taxonomy_npclassifier_superclass,
            'component_taxonomy_npclassifier_class': component_taxonomy_npclassifier_class,
            'component_taxonomy_classyfire_kingdom': component_taxonomy_classyfire_kingdom,
            'component_taxonomy_classyfire_superclass': component_taxonomy_classyfire_superclass,
            'component_taxonomy_classyfire_class': component_taxonomy_classyfire_class,
            'component_taxonomy_classyfire_parent': component_taxonomy_classyfire_parent,
            'plant_names': plant_names,
        }
        # classyfire_partent -> npclassifier_superclass -> npclassifier_pathway
        # ex. Plant X contains cucurbitacin glycosides, a class of triterpenoid compounds (terpenoids).
        export_items.append(export_item)
        continue
        break
    for export_item in export_items:
        print(json.dumps(export_item, indent=4, default=str))
        break
    print(docs_num)
    print(parent_count)
    print(class_count)
    print(superclass_count)
    print(kingdom_count)
    print(npclassifier_pathway_count)
    print(npclassifier_superclass_count)
    print(npclassifier_class_count)
    print('INCHIKEY FAILED COUNTER:', inchikey_count)
    io.json_write(lotus_output_filepath, export_items)
    quit()

# pubchem_properties_batches_to_single_by_inchikey()
# lotus_bson_to_json()
# quit()

########################################
# MERGES
########################################
def lotus_pubchem__inchikey_cid__merge():
    # add to lotus objects "pubchem_cids" by searching it with inchikey on bulk download file
    pubchem_cid_inchikey_filepath = f'{pubchem_folderpath}/CID-InChI-Key'
    # print(os.listdir(pubchem_folderpath))
    '''
    def build_mapping(file_path, target_inchikeys):
        mapping = {}
        with open(file_path, "r") as f:
            for i, line in enumerate(f):
                parts = line.strip().split("\t")
                if len(parts) < 2:
                    continue  # skip malformed lines
                cid = parts[0]
                inchikey = parts[1]
                if inchikey in target_inchikeys:
                    mapping.setdefault(inchikey, []).append(cid)
                if i % 1_000_000 == 0:
                    print(f"Processed {i} lines...")
        return mapping
    '''
    '''
    def write_matches(input_path, target_keys, output_dir):
        os.makedirs(output_dir, exist_ok=True)
        for i, line in enumerate(open(input_path, "r")):
            parts = line.strip().split("\t")
            if len(parts) < 2:
                continue
            cid, inchi, inchikey = parts[0], parts[1], parts[2]
            print(parts)
            print(cid)
            print(inchi)
            print(inchikey)
            print()
            if i > 10: quit()
            continue
            if inchikey in target_keys:
                filepath = os.path.join(output_dir, f"{inchikey}.json")
                # append CID safely
                if os.path.exists(filepath):
                    with open(filepath, "r") as f:
                        data = json.load(f)
                else:
                    data = {
                        "inchikey": inchikey,
                        "cids": []
                    }
                data["cids"].append(cid)
                with open(filepath, "w") as f:
                    json.dump(data, f)
            if i % 1_000_000 == 0:
                print(f"{i} lines processed")
    '''
    lotus_items = io.json_read(lotus_output_filepath)
    lotus_components_inchikey = [item['component_inchikey'] for item in lotus_items]
    print(lotus_components_inchikey[0])
    print(len(lotus_components_inchikey))
    lotus_components_inchikey = set(
        item['component_inchikey'] for item in lotus_items
    )
    '''
    mapping = build_mapping(
        pubchem_cid_inchikey_filepath,   # unzipped file
        lotus_components_inchikey,
    )
    '''
    '''
    write_matches(
        input_path=pubchem_cid_inchikey_filepath, 
        target_keys=lotus_components_inchikey, 
        output_dir=f'{pubchem_folderpath}/lotus-pubchem-inchikey-cid-extract',
    )
    '''
    def sqlite_table_pubchem_inchikey_cid_create():
        conn = sqlite3.connect(f'{pubchem_folderpath}/pubchem_inchikey_cid_mapping.db')
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS pubchem_inchikey_cid_mapping (
                inchikey TEXT,
                inchi TEXT,
                cid TEXT
            )
        """)
        cur.execute("PRAGMA synchronous = OFF")
        cur.execute("PRAGMA journal_mode = MEMORY")
        cur.execute("PRAGMA temp_store = MEMORY")
        cur.execute("PRAGMA cache_size = 1000000")
        with open(pubchem_cid_inchikey_filepath, "r") as f:
            for i, line in enumerate(f):
                parts = line.strip().split("\t")
                if len(parts) < 2:
                    continue
                cid, inchi, inchikey = parts[0], parts[1], parts[2]
                cur.execute("INSERT INTO pubchem_inchikey_cid_mapping VALUES (?, ?, ?)", (inchikey, inchi, cid))
                if i % 100000 == 0:
                    conn.commit()
                    print(f"{i} lines inserted")
        cur.execute("CREATE INDEX IF NOT EXISTS idx_inchikey ON pubchem_inchikey_cid_mapping(inchikey)")
        conn.commit()
        conn.close()
    sqlite_table_pubchem_inchikey_cid_create()
    pass
    quit()

def get_cids(db_path, inchikey):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute(
        "SELECT cid FROM pubchem_inchikey_cid_mapping WHERE inchikey = ?",
        (inchikey,)
    )
    results = [row[0] for row in cur.fetchall()]
    conn.close()
    return results

# test
lotus_items = io.json_read(lotus_output_filepath)
lotus_items_output = []
print('here')
for i, lotus_item in enumerate(lotus_items[:]):
    print(f'{i}/{len(lotus_items)}')
    inchikey = lotus_item['component_inchikey']
    cids = get_cids(f'{pubchem_folderpath}/pubchem_inchikey_cid_mapping.db', inchikey)
    _item = lotus_item
    _item['pubchem_cids'] = cids
    lotus_items_output.append(_item)
    # break
lotus_folderpath = f'{g.SSOT_FOLDERPATH}/lotus'
io.json_write(f'{lotus_folderpath}/0001-cid.json', lotus_items_output) 

# lotus_pubchem__inchikey_cid__merge()
# lotus_items = io.json_read(lotus_output_filepath)
# print(lotus_items[0])
quit()

def pubchem_batches_by_inchikey():
    chunk_size = 10
    lotus_items = io.json_read(lotus_output_filepath)
    print(lotus_items[0])
    quit()
    lotus_components_inchikeys = sorted([item['component_inchikey'] for item in lotus_items])
    # print(lotus_components_inchikeys[0])
    # quit()
    for batch_i, batch in enumerate(chunks(lotus_components_inchikeys, chunk_size)):
        print(f'{batch_i}/{len(lotus_components_inchikeys)//chunk_size}')
        # url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/{','.join(batch)}/record/JSON"
        # url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/{','.join(batch)}/property/InChIKey,CanonicalSMILES,IUPACName/JSON"
        FIELDS = "InChIKey,CanonicalSMILES,IUPACName,Title"
        # url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/{','.join(batch)}/property/{FIELDS}/JSON"
        url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/inchikey/{','.join(batch)}/property/{FIELDS}/JSON"
        batch_i_str = ''
        if batch_i < 10: batch_i_str = f'0000{batch_i}'
        elif batch_i < 100: batch_i_str = f'000{batch_i}'
        elif batch_i < 1000: batch_i_str = f'00{batch_i}'
        elif batch_i < 10000: batch_i_str = f'0{batch_i}'
        elif batch_i < 100000: batch_i_str = f'{batch_i}'
        output_filepath = f"{g.SSOT_FOLDERPATH}/pubchem/lotus-compounds-inchikey-batches/batch_{batch_i_str}.json"
        if os.path.exists(output_filepath): continue
        ###
        r = requests.get(url)
        if r.status_code == 200:
            data = r.json()
            with open(output_filepath, 'w') as f:
                json.dump(data, f)
        else:
            print("Error:", r.status_code)
            print(url)
            break
        time.sleep(random.randint(2, 3))
        # print('#########################################################')
        # print(data['PropertyTable']['Properties'][0])
        # print('#########################################################')
        # break

# pubchem_batches_by_inchikey()
# quit()

def herb20_todo():
    export_data = []
    items = io.csv_to_dict(herb20_filepath, delimiter='\t')
    for item in items:
        # print(item)
        latin_name = item['Herb_latin_name']
        used_part = item['UsePart']
        function = item['Function']
        indication = item['Indication']
        print(latin_name)
        print(used_part)
        print(indication)
        print()
        pass
    print(items[0])
    '''
    Herb_id	
    Herb_pinyin_name	
    Herb_cn_name	
    Herb_alias_name	
    Herb_en_name	
    Herb_latin_name	
    Properties	
    Meridians	
    UsePart	
    Function	
    Indication	
    Toxicity	
    Clinical_manifestations	
    Therapeutic_en_class	
    Therapeutic_cn_class	
    SymMap_id	
    TCMID_id	
    TCMSP_id	
    TCM_ID_id
    * 1. Herb_id: A unique identifier for each herb within the HERD database.
    4. Herb_pinyin_name: The pronunciation of the herb's Chinese name using Pinyin.
    2. Herb_cn_name: The official Chinese name of the herb.
    3. Herb_alias_name: Various alternative names for the herb in Chinese.
    * 5. Herb_en_name: The common English name of the herb.
    * 6. Herb_latin_name: The scientific Latin name that classifies the species of the herb.
    7. Properties: A description of the inherent characteristics or 'properties' of the herb, often referring to its nature in Traditional Chinese Medicine (TCM), such as being warm, cold, sweet, pungent, etc.
    8. Meridians: The specific pathways or 'meridians' in the body through which the herb is believed to act, according to TCM theory.
    * 9. UsePart: The specific part of the herb that is used for medicinal purposes, such as the root, leaf, seed, or bulb.
    * 10. Function: A description of the medicinal functions or 'effects' the herb is traditionally believed to have.
    * 11. Indication: The conditions or symptoms for which the herb is traditionally used to treat.
    * 12. Toxicity: Information regarding the potential toxicity or side effects of the herb.
    * 13. Clinical_manifestations: The observed clinical effects or indications that the herb may address or alleviate.
    * 14. Therapeutic_en_class: The therapeutic category of the herb in English, which may include terms like 'blood activation and stasis removal' or 'medicinal for detoxification'.
    15. Therapeutic_cn_class: The therapeutic category of the herb in Chinese, providing a cultural and linguistic context for its use.
    18. SymMap_id: A cross-reference identifier for the herb within the SymMap database.
    16. TCMID_id: A cross-reference identifier linking the herb to the TCMID database.
    17. TCM_ID_id: A cross-reference identifier for the herb within the TCM-ID database.
    19. TCMSP_id: A cross-reference identifier for the herb within the TCMSP database.
    '''
    quit()

def first_n_bson(path, n=5):
    from bson import BSON
    with open(path, "rb") as f:
        for _ in range(n):
            size_bytes = f.read(4)
            if not size_bytes:
                break
            size = int.from_bytes(size_bytes, "little")
            f.seek(-4, 1)
            raw = f.read(size)
            yield BSON(raw).decode()

# parse lotus file (.bson) -> extract fields you need -> save to json

def lotus_json_preview(formatted=False):
    items = io.json_read(lotus_output_filepath)
    if not formatted:
        print(items[0])
    else:
        print(json.dumps(items[0], indent=4))
    quit()
# lotus_json_preview(formatted=True)

def lotus_pubchem_match():
    lotus_items = io.json_read(lotus_output_filepath)
    for lotus_item_i, lotus_item in enumerate(lotus_items):
        print(f'{lotus_item_i}/{len(lotus_items)}')
        # lotus_item = lotus_items[0]
        lotus_item_inchikey = lotus_item['component_inchikey']
        pubchem_inchikey_filepath = f'''{g.SSOT_FOLDERPATH}/pubchem/compounds-inchikey/{lotus_item_inchikey}.json'''
        try: pubchem_data = io.json_read(pubchem_inchikey_filepath)
        except: continue
        pubchem_cid = pubchem_data['CID']
        print(lotus_item)
        print(lotus_item_inchikey)
        print(pubchem_inchikey_filepath)
        print(pubchem_data)
        ###
        print(pubchem_cid)
        oregano_compounds_text = io.file_read(
            f'{g.SSOT_FOLDERPATH}/oregano/oregano-master/Integration/Integration V3/GESTION_ID/COMPOUND.tsv'
        )
        oregano_compounds_lines = oregano_compounds_text.split('\n')
        ###
        headings = oregano_compounds_lines[0].split('\t')
        headings[0] = 'ID_OREGANO'
        cids = []
        for line_i, line in enumerate(oregano_compounds_lines[:]):
            if line_i == 0: continue
            if line.strip() == '': continue
            values = line.split('\t')
            item = {}
            for i in range(len(headings)):
                item[headings[i]] = values[i].strip()
            # print(json.dumps(item, indent=4))
            # quit()
            pubchem_compound_id = item['PUBCHEM COMPOUND']
            if pubchem_compound_id.strip() == '': continue
            if ',' in pubchem_compound_id: continue
            if ';' in pubchem_compound_id: continue
            # print(pubchem_compound_id, pubchem_cid)
            if str(pubchem_compound_id).strip() == str(pubchem_cid).strip():
                print(item)
                # print('ID:', item['ID_OREGANO'], '  WIKIDATA:', item['WIKIPEDIA'], '  CID:', pubchem_compound_id)
        if lotus_item_i > 5: quit()
    quit()

lotus_pubchem_match()
quit()

def powo_plants_jsons():
    plants_folderpath = f'{wikidata_folderpath}/entity_has-use_medicinal-plant'
    plants_filepaths = sorted([f'{plants_folderpath}/{filename}' for filename in os.listdir(plants_folderpath)])
    failed = []
    for plant_filepath_i, plant_filepath in enumerate(plants_filepaths):
        plant_filename_raw = plant_filepath.split('/')[-1].split('.')[0]
        plant_data = io.json_read(plant_filepath)
        try: claim = plant_data['entities'][plant_filename_raw]['claims']['P5037'][0]
        except: claim = None
        if claim:
            value = claim['mainsnak']['datavalue']['value']
            print(json.dumps(value, indent=4))
            value_url_id = value.split(':')[-1]
            print(value_url_id)
            output_filepath = f'{kg_folderpath}/powo/plants-jsons/{value_url_id}.json'
            if not os.path.exists(output_filepath):
                url = f"https://powo.science.kew.org/api/2/taxon/{value}"
                headers = {
                    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36"
                }
                try:
                    response = requests.get(url, headers=headers)
                    response.raise_for_status()
                    data = response.json()
                    io.json_write(output_filepath, data)
                    print(data)
                except:
                    failed.append(plant_filepath)
                time.sleep(random.randint(2, 3))

    for f in failed:
        print(f)
    print(len(failed))
    quit()

def powo_plants_taxonomies_get():
    plants_folderpath = f'{wikidata_folderpath}/entity_has-use_medicinal-plant'
    plants_filepaths = sorted([f'{plants_folderpath}/{filename}' for filename in os.listdir(plants_folderpath)])
    plants_taxonomies = []
    for plant_filepath_i, plant_filepath in enumerate(plants_filepaths):
        print(f'{plant_filepath_i}/{len(plants_filepaths)}')
        plant_filename_raw = plant_filepath.split('/')[-1].split('.')[0]
        plant_data = io.json_read(plant_filepath)
        try: claim = plant_data['entities'][plant_filename_raw]['claims']['P5037'][0]
        except: claim = None
        try: taxon_name = plant_data['entities'][plant_filename_raw]['claims']['P225'][0]['mainsnak']['datavalue']['value']
        except: taxon_name = None
        if claim:
            value = claim['mainsnak']['datavalue']['value']
            print(json.dumps(value, indent=4))
            value_url_id = value.split(':')[-1]
            print(value_url_id)
            plant_filepath = f'{kg_folderpath}/powo/plants-jsons/{value_url_id}.json'
            if os.path.exists(plant_filepath):
                plant_data = io.json_read(plant_filepath)
                kingdom = plant_data['kingdom']
                phylum = plant_data['phylum']
                clazz = plant_data['clazz']
                subclass = plant_data['subclass']
                order = plant_data['order']
                family = plant_data['family']
                genus = plant_data['genus']
                # try: species = plant_data['species']
                # except: species = None
                species = taxon_name
                item = {
                    'species': species,
                    'genus': genus,
                    'family': family,
                    'order': order,
                    'subclass': subclass,
                    'clazz': clazz,
                    'phylum': phylum,
                    'kingdom': kingdom,
                }
                plants_taxonomies.append(item)
    return plants_taxonomies

def powo_lotus_match():
    lotus_items = io.json_read(lotus_output_filepath)
    powo_plants_taxonomies = powo_plants_taxonomies_get()
    matches = []
    for lotus_item_i, lotus_item in enumerate(lotus_items):
        print(f'{lotus_item_i}/{len(lotus_items)}')
        # print(lotus_item)
        lotus_plant_name = lotus_item['plant_names'][0]
        for powo_item in powo_plants_taxonomies:
            powo_plant_species = powo_item['species']
            if lotus_plant_name == powo_plant_species:
                print('found')
                print(lotus_item)
                print(powo_item)
                match = {
                    'powo_plant_species': powo_plant_species,
                    'lotus_components': lotus_item,
                }
                matches.append(match)
                # break
        # break
    io.json_write(f'{kg_folderpath}/powo-lotus/matches-all.json', matches)
    quit()


# lotus_items = io.json_read(lotus_output_filepath)
# print(lotus_items[0])

def oregano_cids_extract():
    oregano_compounds_text = io.file_read(f'{g.SSOT_FOLDERPATH}/oregano/oregano-master/Integration/Integration V3/GESTION_ID/COMPOUND.tsv')
    oregano_compounds_lines = oregano_compounds_text.split('\n')
    ###
    # oregano_compounds_data = io.csv_to_dict(f'{g.SSOT_FOLDERPATH}/oregano/oregano-master/Integration/Integration V3/GESTION_ID/COMPOUND.tsv', delimiter='\t')
    headings = oregano_compounds_lines[0].split('\t')
    headings[0] = 'ID_OREGANO'
    cids = []
    for line_i, line in enumerate(oregano_compounds_lines[:]):
        if line_i == 0: continue
        if line.strip() == '': continue
        values = line.split('\t')
        item = {}
        for i in range(len(headings)):
            item[headings[i]] = values[i].strip()
        # print(json.dumps(item, indent=4))
        # quit()
        pubchem_compound_id = item['PUBCHEM COMPOUND']
        if pubchem_compound_id.strip() == '': continue
        if ',' in pubchem_compound_id: continue
        if ';' in pubchem_compound_id: continue
        print(item['ID_OREGANO'], item['WIKIPEDIA'], pubchem_compound_id)
        cids.append(pubchem_compound_id.strip())
    print(cids[:10])
    print(len(cids))
    print(len(list(set(cids))))
    cids = sorted(list(set(cids)))

# cids = oregano_cids_extract()

def oregano_compound_to_pubmed_match():
    oregano_compounds_text = io.file_read(
        f'{g.SSOT_FOLDERPATH}/oregano/oregano-master/Integration/Integration V3/GESTION_ID/COMPOUND.tsv'
    )
    oregano_compounds_lines = oregano_compounds_text.split('\n')
    ###
    headings = oregano_compounds_lines[0].split('\t')
    headings[0] = 'ID_OREGANO'
    cids = []
    for line_i, line in enumerate(oregano_compounds_lines[:]):
        if line_i == 0: continue
        if line.strip() == '': continue
        values = line.split('\t')
        item = {}
        for i in range(len(headings)):
            item[headings[i]] = values[i].strip()
        # print(json.dumps(item, indent=4))
        # quit()
        pubchem_compound_id = item['PUBCHEM COMPOUND']
        if pubchem_compound_id.strip() == '': continue
        if ',' in pubchem_compound_id: continue
        if ';' in pubchem_compound_id: continue
        # pubchem_cid_filepath = f'''{g.SSOT_FOLDERPATH}/pubchem/oregano-compounds/{pubchem_compound_id}.json'''
        # pubchem_data = io.json_read(pubchem_cid_filepath)
        # try: pubchem_title = pubchem_data['Title']
        # except: pubchem_title = ''
        # print('ID:', item['ID_OREGANO'], '  WIKIDATA:', item['WIKIPEDIA'], '  CID:', pubchem_compound_id, '  TITLE:', pubchem_title)
        print('ID:', item['ID_OREGANO'], '  WIKIDATA:', item['WIKIPEDIA'], '  CID:', pubchem_compound_id)

# oregano_compound_to_pubmed_match()

quit()

def pubmed_properties_from_cids(cids):
    chunk_size = 100
    for batch_i, batch in enumerate(chunks(cids, chunk_size)):
        print(f'{batch_i}/{len(cids)//chunk_size}')
        # url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/{','.join(batch)}/record/JSON"
        # url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/{','.join(batch)}/property/InChIKey,CanonicalSMILES,IUPACName/JSON"
        FIELDS = "InChIKey,CanonicalSMILES,IUPACName,Title"
        url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/{','.join(batch)}/property/{FIELDS}/JSON"
        batch_i_str = ''
        if batch_i < 10: batch_i_str = f'000{batch_i}'
        elif batch_i < 100: batch_i_str = f'00{batch_i}'
        elif batch_i < 1000: batch_i_str = f'0{batch_i}'
        elif batch_i < 10000: batch_i_str = f'{batch_i}'
        output_filepath = f"{g.SSOT_FOLDERPATH}/pubchem/oregano-batches/batch_{batch_i_str}.json"
        if os.path.exists(output_filepath): continue
        ###
        r = requests.get(url)
        if r.status_code == 200:
            data = r.json()
            with open(output_filepath, 'w') as f:
                json.dump(data, f)
        else:
            print("Error:", r.status_code)
            print(url)
            break
        time.sleep(random.randint(3, 5))
        # print('#########################################################')
        # print(data['PropertyTable']['Properties'][0])
        # print('#########################################################')
        # break

# pubmed_properties_from_cids(cids)

def pubmed_properties_batches_to_single():
    batches_folderpath = f'{g.SSOT_FOLDERPATH}/pubchem/oregano-batches'
    batches_filepaths = sorted([f'{batches_folderpath}/{filename}' for filename in os.listdir(batches_folderpath)])
    print(batches_filepaths)
    for batch_i, batch_filepath in enumerate(batches_filepaths):
        print(f'{batch_i}/{len(batches_filepaths)}')
        batch_data = io.json_read(batch_filepath)
        items_export = batch_data['PropertyTable']['Properties']
        for item_export in items_export:
            item_export_filepath = f'''{g.SSOT_FOLDERPATH}/pubchem/oregano-compounds/{item_export['CID']}.json'''
            io.json_write(item_export_filepath, item_export)
            # print(item_export_filepath)
        # print(batch_data)
        # quit()
quit()

# oregano_items = io.csv_to_dict(f'{g.SSOT_FOLDERPATH}/oregano/oregano-master/Data_OREGANO/Graphs/OREGANO_V3.tsv', delimiter='\t')
oregano_text = io.file_read(f'{g.SSOT_FOLDERPATH}/oregano/oregano-master/Data_OREGANO/Graphs/OREGANO_V3_WIW.tsv')
oregano_lines = oregano_text.split('\n')
triples_failed = []
s_types = []
for oregano_line in oregano_lines:
    try: chunk_1, chunk_2, chunk_3 = oregano_line.split('\t')
    except:
        triples_failed.append(oregano_line)
        continue
    s_type = chunk_1.split(':')[0]
    if s_type not in s_types:
        s_types.append(s_type)
    print(chunk_2)
    # print(chunk_1, '->', chunk_2, '->', chunk_3)
    # quit()

print('#########################################3')
for s_type in s_types:
    print(s_type)
quit()

'''
plants_folderpath = f'{kg_folderpath}/powo/plants-jsons'
plants_filepaths = sorted([f'{plants_folderpath}/{filename}' for filename in os.listdir(plants_folderpath)])
data = []
for plant_filepath in plants_filepaths:
    plant_data = io.json_read(plant_filepath)
    print(json.dumps(plant_data, indent=4))
    kingdom = plant_data['kingdom']
    phylum = plant_data['phylum']
    clazz = plant_data['clazz']
    subclass = plant_data['subclass']
    order = plant_data['order']
    family = plant_data['family']
    genus = plant_data['genus']
    # try: species = plant_data['species']
    # except: species = None
    print(json.dumps(plant_data, indent=4))
    quit()
    item = {
        'species': species,
        'genus': genus,
        'family': family,
        'order': order,
        'subclass': subclass,
        'clazz': clazz,
        'phylum': phylum,
        'kingdom': kingdom,
    }
    data.append(item)
'''

uri = "bolt://localhost:7687"
username = "neo4j"
password = "Newoliark1"

driver = GraphDatabase.driver(uri, auth=(username, password))

def neo4j_clear():
    with driver.session() as session:
        tx = session.begin_transaction()
        tx.run("MATCH (n) DETACH DELETE n")
        tx.commit()

with driver.session() as session:
    # 1. Delete all data
    session.run("MATCH (n) DETACH DELETE n")

    # 2. Drop constraints
    constraints = session.run("SHOW CONSTRAINTS").data()
    for c in constraints:
        session.run(f"DROP CONSTRAINT {c['name']}")

    # 3. Drop indexes
    indexes = session.run("SHOW INDEXES").data()
    for i in indexes:
        session.run(f"DROP INDEX {i['name']}")

# neo4j_clear()
# quit()

def insert_taxonomy(tx, batch):
    query = """
    UNWIND $rows AS row

    // Require at least species
    WITH row WHERE row.species IS NOT NULL

    MERGE (sp:Species {name: row.species})

    // Genus
    FOREACH (_ IN CASE WHEN row.genus IS NOT NULL THEN [1] ELSE [] END |
        MERGE (g:Genus {name: row.genus})
        MERGE (sp)-[:PARENT_OF]->(g)
    )

    // Family (connect to genus if exists)
    FOREACH (_ IN CASE WHEN row.family IS NOT NULL THEN [1] ELSE [] END |
        MERGE (f:Family {name: row.family})

        FOREACH (_ IN CASE WHEN row.genus IS NOT NULL THEN [1] ELSE [] END |
            MERGE (g:Genus {name: row.genus})
            MERGE (g)-[:PARENT_OF]->(f)
        )
    )

    // Order
    FOREACH (_ IN CASE WHEN row.order IS NOT NULL THEN [1] ELSE [] END |
        MERGE (o:Order {name: row.order})

        FOREACH (_ IN CASE WHEN row.family IS NOT NULL THEN [1] ELSE [] END |
            MERGE (f:Family {name: row.family})
            MERGE (f)-[:PARENT_OF]->(o)
        )
    )

    // Subclass
    FOREACH (_ IN CASE WHEN row.subclass IS NOT NULL THEN [1] ELSE [] END |
        MERGE (c:Subclass {name: row.subclass})

        FOREACH (_ IN CASE WHEN row.order IS NOT NULL THEN [1] ELSE [] END |
            MERGE (o:Order {name: row.order})
            MERGE (o)-[:PARENT_OF]->(c)
        )
    )

    // Clazz
    FOREACH (_ IN CASE WHEN row.clazz IS NOT NULL THEN [1] ELSE [] END |
        MERGE (c:Clazz {name: row.clazz})

        FOREACH (_ IN CASE WHEN row.subclass IS NOT NULL THEN [1] ELSE [] END |
            MERGE (o:Subclass {name: row.subclass})
            MERGE (o)-[:PARENT_OF]->(c)
        )
    )

    // Phylum
    FOREACH (_ IN CASE WHEN row.phylum IS NOT NULL THEN [1] ELSE [] END |
        MERGE (p:Phylum {name: row.phylum})

        FOREACH (_ IN CASE WHEN row.clazz IS NOT NULL THEN [1] ELSE [] END |
            MERGE (c:Clazz {name: row.clazz})
            MERGE (c)-[:PARENT_OF]->(p)
        )
    )

    // Kingdom
    FOREACH (_ IN CASE WHEN row.kingdom IS NOT NULL THEN [1] ELSE [] END |
        MERGE (k:Kingdom {name: row.kingdom})

        FOREACH (_ IN CASE WHEN row.phylum IS NOT NULL THEN [1] ELSE [] END |
            MERGE (p:Phylum {name: row.phylum})
            MERGE (p)-[:PARENT_OF]->(k)
        )
    )
    """
    query = """
UNWIND $rows AS row

WITH row WHERE row.species IS NOT NULL

// Species = your plant name
MERGE (sp:Taxon {scientificName: row.species})
SET sp.taxonRank = "species"

// Genus
FOREACH (_ IN CASE WHEN row.genus IS NOT NULL THEN [1] ELSE [] END |
    MERGE (g:Taxon {scientificName: row.genus})
    SET g.taxonRank = "genus"
    MERGE (sp)-[:PARENT_TAXON]->(g)
)

// Family
FOREACH (_ IN CASE WHEN row.family IS NOT NULL THEN [1] ELSE [] END |
    MERGE (f:Taxon {scientificName: row.family})
    SET f.taxonRank = "family"

    FOREACH (_ IN CASE WHEN row.genus IS NOT NULL THEN [1] ELSE [] END |
        MERGE (g:Taxon {scientificName: row.genus})
        MERGE (g)-[:PARENT_TAXON]->(f)
    )
)

// Order
FOREACH (_ IN CASE WHEN row.order IS NOT NULL THEN [1] ELSE [] END |
    MERGE (o:Taxon {scientificName: row.order})
    SET o.taxonRank = "order"

    FOREACH (_ IN CASE WHEN row.family IS NOT NULL THEN [1] ELSE [] END |
        MERGE (f:Taxon {scientificName: row.family})
        MERGE (f)-[:PARENT_TAXON]->(o)
    )
)

// Class
FOREACH (_ IN CASE WHEN row.clazz IS NOT NULL THEN [1] ELSE [] END |
    MERGE (c:Taxon {scientificName: row.clazz})
    SET c.taxonRank = "class"

    FOREACH (_ IN CASE WHEN row.order IS NOT NULL THEN [1] ELSE [] END |
        MERGE (o:Taxon {scientificName: row.order})
        MERGE (o)-[:PARENT_TAXON]->(c)
    )
)

// Phylum
FOREACH (_ IN CASE WHEN row.phylum IS NOT NULL THEN [1] ELSE [] END |
    MERGE (p:Taxon {scientificName: row.phylum})
    SET p.taxonRank = "phylum"

    FOREACH (_ IN CASE WHEN row.clazz IS NOT NULL THEN [1] ELSE [] END |
        MERGE (c:Taxon {scientificName: row.clazz})
        MERGE (c)-[:PARENT_TAXON]->(p)
    )
)

// Kingdom
FOREACH (_ IN CASE WHEN row.kingdom IS NOT NULL THEN [1] ELSE [] END |
    MERGE (k:Taxon {scientificName: row.kingdom})
    SET k.taxonRank = "kingdom"

    FOREACH (_ IN CASE WHEN row.phylum IS NOT NULL THEN [1] ELSE [] END |
        MERGE (p:Taxon {scientificName: row.phylum})
        MERGE (p)-[:PARENT_TAXON]->(k)
    )
)
    """
    tx.run(query, rows=batch)

batch_size = 1000

with driver.session() as session:
    for i in range(0, len(plants_taxonomies), batch_size):
        session.execute_write(insert_taxonomy, plants_taxonomies[i:i+batch_size])

driver.close()

quit()


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



def db_read_family(plant_taxon_name):
    with driver.session() as session:
        tx = session.begin_transaction()
        query = """
            MATCH (p:Plant {name: $plant})-[:HAS_FAMILY]->(f:Family)
            RETURN f.name
        """
        result = tx.run(query, plant=plant_taxon_name)
        record = result.single()
        family = record['f.name'] if record else none
        tx.commit()
        print(family)
        # return record["family"] if record else None

        import textwrap
        prompt = textwrap.dedent(f'''
            Write one sentence with the following data and relationships:
            {plant_taxon_name} -> has family -> {family}
        ''').strip()
        print(prompt)
        reply = llm.reply(prompt, model_filepath, temperature=0)
        if '</think>' in reply:
            reply = reply.split('</think>')[1].strip()
        print('########################################')
        print(reply)
        print('########################################')

    
def db_insert__plant_family():
    triples = []
    jsons_foldername = 'wikidata-wcvp-jsons'
    jsons_folderpath = f'{wikidata_folderpath}/{jsons_foldername}'
    jsons_filepaths = [f'{jsons_folderpath}/{filename}' for filename in os.listdir(jsons_folderpath)]
    for json_filepath in jsons_filepaths:
        json_data = io.json_read(json_filepath)
        _item = {
            'taxon_name': json_data['taxon_name'],
            'family': json_data['family'],
        }
        triples.append(_item)
    ###
    batch_size = 1000
    with driver.session() as session:
        for i in range(0, len(triples), batch_size):
            batch = triples[i:i+batch_size]
            query = """
            UNWIND $rows AS row
            MERGE (p:Plant {name: row.taxon_name})
            MERGE (f:Family {name: row.family})
            MERGE (p)-[:HAS_FAMILY]->(f)
            """
            tx = session.begin_transaction()
            tx.run(query, rows=batch)
            tx.commit()

def insert_families_orders():
    data = io.json_read(f'{wikidata_folderpath}/families-orders.json')
    ###
    batch_size = 1000
    with driver.session() as session:
        for i in range(0, len(data), batch_size):
            batch = data[i:i+batch_size]
            query = """
                UNWIND $rows AS row
                MERGE (f:Family {name: row.family})
                MERGE (o:Order  {name: row.order})
                MERGE (f)-[:HAS_ORDER]->(o)
            """
            tx = session.begin_transaction()
            tx.run(query, rows=batch)
            tx.commit()

'''
insert_families_orders()

driver.close()

quit() 
# db_clear()
db_insert__plant_family()
'''

'''
def read_dmp(path, num_fields=None):
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            # remove trailing row terminator
            line = line.strip()

            # remove final '|'
            if line.endswith("|"):
                line = line[:-1]

            # split on the real delimiter
            parts = [x.strip() for x in line.split("\t|\t")]

            # optional sanity check
            if num_fields and len(parts) != num_fields:
                continue  # or raise error

            yield parts
'''

def read_dmp(path, num_fields=None):
    rows = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            # remove whitespace/newline
            line = line.strip()
            # remove trailing '|'
            if line.endswith("|"):
                line = line[:-1]
            # split on the custom delimiter
            parts = [x.strip() for x in line.split("\t|\t")]
            # optional validation
            if num_fields and len(parts) != num_fields:
                continue  # or raise ValueError
            rows.append(parts)
    return rows

'''
nodes_families = []
nodes = []
for row_i, row in enumerate(rows):
    # print(f'{row_i}/{len(list(rows))}')
    tax_id = row[0]
    parent_tax_id = row[1]
    rank = row[2]
    division_id = row[4]
    if rank == 'family':
        _item = {
            'tax_id': row[0],
            'parent_tax_id': row[1],
            'rank': row[2],
            'division_id': row[4],
        }
        nodes_families.append(_item)
        nodes.append(row)


print(f'NODES: {len(list(nodes_families))}')
print(nodes[0])
'''

'''
'''

def sqlite_table_nodes_create():
    conn = sqlite3.connect(sqlite_database_filepath)
    cur = conn.cursor()
    cur.execute("""
        SELECT name FROM sqlite_master 
        WHERE type='table' AND name='nodes';
    """)
    exists = cur.fetchone() is not None
    if not exists:
        cur.execute('''
            CREATE TABLE IF NOT EXISTS nodes (
                tax_id INTEGER PRIMARY KEY,
                parent_tax_id INTEGER,
                rank TEXT
            )
        ''')
        rows = read_dmp(taxdmp_nodes_filepath)
        data = [(int(r[0]), int(r[1]), r[2]) for r in rows]
        cur.executemany(
            "INSERT INTO nodes (tax_id, parent_tax_id, rank) VALUES (?, ?, ?)",
            data
        )
        conn.commit()

def sqlite_table_names_create():
    conn = sqlite3.connect(sqlite_database_filepath)
    cur = conn.cursor()
    cur.execute("""
        SELECT name FROM sqlite_master 
        WHERE type='table' AND name='names';
    """)
    exists = cur.fetchone() is not None
    if not exists:
        cur.execute('''
            CREATE TABLE IF NOT EXISTS names (
                tax_id INTEGER,
                name_txt TEXT,
                unique_name TEXT,
                name_class TEXT
            )
        ''')
        rows = read_dmp(taxdmp_names_filepath)
        data = [(int(r[0]), r[1], r[2], r[3]) for r in rows]
        cur.executemany(
            "INSERT INTO names (tax_id, name_txt, unique_name, name_class) VALUES (?, ?, ?, ?)",
            data
        )
        conn.commit()

def sqlite_table_index_create():
    conn = sqlite3.connect(sqlite_database_filepath)
    cur = conn.cursor()
    cur.execute("CREATE INDEX IF NOT EXISTS idx_names_name ON names(name_txt)")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_names_tax ON names(tax_id)")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_nodes_tax ON nodes(tax_id)")
    conn.commit()

def sqlite_table_nodes_rows_count():
    conn = sqlite3.connect(sqlite_database_filepath)
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM nodes")
    print("NODES ROWS:", cur.fetchone()[0])

def sqlite_table_names_rows_count():
    conn = sqlite3.connect(sqlite_database_filepath)
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM names")
    print("NAMES ROWS:", cur.fetchone()[0])

def sqlite_table_nodes_rows_sample():
    conn = sqlite3.connect(sqlite_database_filepath)
    cur = conn.cursor()
    cur.execute("SELECT * FROM nodes LIMIT 10")
    for row in cur.fetchall():
        print(row)

def sqlite_table_names_rows_sample():
    conn = sqlite3.connect(sqlite_database_filepath)
    cur = conn.cursor()
    cur.execute("SELECT * FROM nodes LIMIT 10")
    for row in cur.fetchall():
        print(row)

sqlite_table_nodes_create()
sqlite_table_names_create()
sqlite_table_index_create()
###
sqlite_table_nodes_rows_count()
sqlite_table_names_rows_count()
sqlite_table_nodes_rows_sample()
sqlite_table_names_rows_sample()

# get [families] from 'wikidata-wcvp-jsons'
def families_get():
    triples = []
    families = []
    jsons_foldername = 'wikidata-wcvp-jsons'
    jsons_folderpath = f'{wikidata_folderpath}/{jsons_foldername}'
    jsons_filepaths = [f'{jsons_folderpath}/{filename}' for filename in os.listdir(jsons_folderpath)]
    for json_filepath in jsons_filepaths:
        json_data = io.json_read(json_filepath)
        _item = {
            'taxon_name': json_data['taxon_name'],
            'family': json_data['family'],
        }
        triples.append(_item)
        if json_data['family'] not in families:
            families.append(json_data['family'])
    return families

def get_lineage(cur, family_name):
    lineage = []

    # resolve name → tax_id
    cur.execute("""
        SELECT tax_id
        FROM names
        WHERE name_txt = ?
        AND name_class = 'scientific name'
        LIMIT 1
    """, (family_name,))

    result = cur.fetchone()
    if not result:
        return []

    tax_id = result[0]

    visited = set()   # 🔴 IMPORTANT: cycle protection

    while tax_id is not None:

        # stop infinite loops
        if tax_id in visited:
            print("Cycle detected at:", tax_id)
            break
        visited.add(tax_id)

        cur.execute("""
            SELECT n.tax_id, n.parent_tax_id, n.rank, nm.name_txt
            FROM nodes n
            JOIN names nm ON n.tax_id = nm.tax_id
            WHERE n.tax_id = ?
            AND nm.name_class = 'scientific name'
        """, (tax_id,))

        row = cur.fetchone()
        if not row:
            break

        lineage.append(row)

        parent_tax_id = row[1]

        # 🔴 safety stop conditions
        if parent_tax_id is None or parent_tax_id == tax_id:
            break

        tax_id = parent_tax_id

    return lineage

def compress_to_7_ranks(lineage):
    """
    lineage: list of tuples (tax_id, parent_tax_id, rank, name)
    returns: dict with 7-level taxonomy
    """

    # target structure
    taxonomy = {
        "kingdom": None,
        "phylum": None,
        "class": None,
        "order": None,
        "family": None,
        "genus": None,
        "species": None
    }

    # NCBI uses "phylum" or "division" for plants
    rank_map = {
        "superkingdom": "kingdom",
        "kingdom": "kingdom",
        "phylum": "phylum",
        "division": "phylum",

        "class": "class",
        "order": "order",
        "family": "family",
        "genus": "genus",
        "species": "species"
    }

    for tax_id, parent_id, rank, name in lineage:
        if rank in rank_map:
            canonical_rank = rank_map[rank]

            # keep first match (most specific in upward traversal)
            if taxonomy[canonical_rank] is None:
                taxonomy[canonical_rank] = name

    return taxonomy

def sqlite_query_families_orders():
    families = families_get()
    parents = []
    conn = sqlite3.connect(sqlite_database_filepath)
    cur = conn.cursor()
    parents_ranks = []
    for family_i, family in enumerate(families):
        print(f'{family_i}/{len(families)}')
        lineage = get_lineage(cur, family)
        lineage = compress_to_7_ranks(lineage)
        print(lineage)
        # quit()
        continue
        query = """
SELECT
    family.name_txt AS family,
    n.rank AS family_rank,
    n.tax_id,
    n.parent_tax_id,
    parent.name_txt AS parent_name,
    parent_node.rank AS parent_rank
FROM names family
JOIN nodes n ON family.tax_id = n.tax_id
JOIN nodes parent_node ON n.parent_tax_id = parent_node.tax_id
JOIN names parent ON parent_node.tax_id = parent.tax_id
WHERE family.name_txt = ?
AND family.name_class = 'scientific name'
AND parent.name_class = 'scientific name'
AND parent_node.rank = 'order';
        """
        query = """
SELECT
    n0.tax_id AS family_id,
    f.name_txt AS family_name,

    n1.tax_id AS parent1_id,
    p1.name_txt AS parent1_name,
    n1.rank AS parent1_rank,

    n2.tax_id AS parent2_id,
    p2.name_txt AS parent2_name,
    n2.rank AS parent2_rank,

    n3.tax_id AS parent3_id,
    p3.name_txt AS parent3_name,
    n3.rank AS parent3_rank,

    n4.tax_id AS parent4_id,
    p4.name_txt AS parent4_name,
    n4.rank AS parent4_rank

FROM nodes n0
JOIN names f ON f.tax_id = n0.tax_id

LEFT JOIN nodes n1 ON n0.parent_tax_id = n1.tax_id
LEFT JOIN names p1 ON p1.tax_id = n1.tax_id

LEFT JOIN nodes n2 ON n1.parent_tax_id = n2.tax_id
LEFT JOIN names p2 ON p2.tax_id = n2.tax_id

LEFT JOIN nodes n3 ON n2.parent_tax_id = n3.tax_id
LEFT JOIN names p3 ON p3.tax_id = n3.tax_id

LEFT JOIN nodes n4 ON n3.parent_tax_id = n4.tax_id
LEFT JOIN names p4 ON p4.tax_id = n4.tax_id

WHERE f.name_txt = ?
AND f.name_class = 'scientific name';
        """
        query = """
SELECT
    child.name_txt AS family,
    parent.name_txt AS parent_name,
    parent_node.rank AS parent_rank,
    parent_node.tax_id AS parent_tax_id
FROM names child
JOIN nodes child_node ON child.tax_id = child_node.tax_id
JOIN nodes parent_node ON child_node.parent_tax_id = parent_node.tax_id
JOIN names parent ON parent_node.tax_id = parent.tax_id
WHERE child.name_txt = ?
AND child.name_class = 'scientific name'
AND parent.name_class = 'scientific name';
        """
        query = """
SELECT
    f.name_txt  AS level0_family,
    p1.name_txt AS level1_parent,
    p1n.rank    AS level1_rank,

    p2.name_txt AS level2_parent,
    p2n.rank    AS level2_rank,

    p3.name_txt AS level3_parent,
    p3n.rank    AS level3_rank,

    p4.name_txt AS level4_parent,
    p4n.rank    AS level4_rank,

    p5.name_txt AS level5_parent,
    p5n.rank    AS level5_rank

FROM names f
JOIN nodes n0 ON f.tax_id = n0.tax_id

-- level 1
JOIN nodes p1n ON n0.parent_tax_id = p1n.tax_id
JOIN names p1 ON p1n.tax_id = p1.tax_id

-- level 2
LEFT JOIN nodes p2n ON p1n.parent_tax_id = p2n.tax_id
LEFT JOIN names p2 ON p2n.tax_id = p2.tax_id

-- level 3
LEFT JOIN nodes p3n ON p2n.parent_tax_id = p3n.tax_id
LEFT JOIN names p3 ON p3n.tax_id = p3.tax_id

-- level 4
LEFT JOIN nodes p4n ON p3n.parent_tax_id = p4n.tax_id
LEFT JOIN names p4 ON p4n.tax_id = p4.tax_id

-- level 5
LEFT JOIN nodes p5n ON p4n.parent_tax_id = p5n.tax_id
LEFT JOIN names p5 ON p5n.tax_id = p5.tax_id

WHERE f.name_txt = ?
AND f.name_class = 'scientific name';
        """
        cur.execute(query, (family,))
        res = cur.fetchall()
        if res:
            res = res[0]
            print(res)
            parents_ranks.append([res[2], res[1]])
            # parents.append({'family': res[0], 'order': res[3]})
        # quit()
    # for parent_rank in parents_ranks:
        # print(parent_rank)
    # io.json_write(f'{kg_folderpath}/taxonomy/families-orders.json', parents)
    # print(len(triples))
    # print(len(parents))

def sqlite_query_orders_classes():
    families_orders_data = io.json_read(f'{kg_folderpath}/taxonomy/families-orders.json')
    orders = [item['order'] for item in families_orders_data]
    ###
    parents = []
    conn = sqlite3.connect(sqlite_database_filepath)
    cur = conn.cursor()
    for order in orders:
        query = f"""
        SELECT
            child.name_txt AS child,
            n.tax_id,
            n.parent_tax_id,
            parent.name_txt AS parent_name
        FROM names child
        JOIN nodes n ON child.tax_id = n.tax_id
        JOIN names parent ON n.parent_tax_id = parent.tax_id
        WHERE child.name_txt = '{order}'
        AND child.name_class = 'scientific name'
        AND parent.name_class = 'scientific name'
        """
        cur.execute(query)
        res = cur.fetchall()
        if res:
            res = res[0]
            print(res)
            # parents.append({'family': res[0], 'order': res[3]})
    # io.json_write(f'{kg_folderpath}/taxonomy/families-orders.json', parents)
    # print(len(triples))
    # print(len(parents))

def sqlite_query_test():
    parents = []
    conn = sqlite3.connect(sqlite_database_filepath)
    cur = conn.cursor()
    query = f"""
    SELECT
        child.name_txt AS child,
        n.tax_id,
        n.parent_tax_id,
        n.rank,
        parent.name_txt AS parent_name
    FROM names child
    JOIN nodes n ON child.tax_id = n.tax_id
    JOIN names parent ON n.parent_tax_id = parent.tax_id
    WHERE child.name_txt = 'campanulids'
    AND child.name_class = 'scientific name'
    AND parent.name_class = 'scientific name'
    """
    cur.execute(query)
    res = cur.fetchall()
    if res:
        res = res[0]
        print(res)

sqlite_query_families_orders()
# sqlite_query_orders_classes()
# sqlite_query_test()

quit()


'''
cur.execute("""
SELECT n.tax_id, n.parent_tax_id, n.rank
FROM names nm
JOIN nodes n ON nm.tax_id = n.tax_id
WHERE nm.name_txt = 'Rosaceae'
LIMIT 10
""")
'''

'''
'''

# print(cur.fetchall())

# quit()

        # if 'Rosaceae' in name_txt:

'''
rows = read_dmp(taxdmp_names_filepath)
names_families = []
for node in nodes_families:
    node_id = node['tax_id']
    for row in rows:
        row_id = row[0]
        row_txt = row[1]
        print('FAMILY:', node_id, row_id, row_txt)
        if row_id == node_id:
            _item = {
                'tax_id': row_id,
                'name_txt': row_txt,
            }
            names_families.append(_item)
            found = True
            break

for item in names_families:
    print(item)

io.json_write(f'{wikidata_folderpath}/names_families.json', names_families)

quit()

# get 'ROSACEAE' id
result = None
rows = read_dmp(taxdmp_names_filepath)
for row in rows:
    name_txt = row[1]
    if 'Rosaceae' in name_txt:
        result = row

print(result)

quit()

names_rows = read_dmp(taxdmp_names_filepath)
names = []
i = 0
for node in nodes:
    node_id = node['tax_id']
    node_parent_id = node['parent_tax_id']
    node_name = None
    node_parent_name = None
    # found = False
    for row in names_rows:
        name_id = row[0]
        name_txt = row[1]
        print('FAMILY:', name_id, node_id, name_txt)
        ###
        if name_id == node_id:
            node_name = name_txt
        if name_id == node_parent_id:
            node_parent_name = name_txt
        if node_name != None and node_parent_name != None:
            _item = {
                'node_id': node_id,
                'node_name': node_name,
                'node_parent_name': node_parent_name,
            }
            names.append(_item)
            found = True
            break
    break
    # if found:
    i += 1
    # if i >= 5: break


for item in names:
    print(item)

quit()

divisions_rows = read_dmp(f'{taxdmp_folderpath}/division.dmp')
divisions = []
i = 0
for family in families:
    division_id = family['division_id']
    found = False
    for row in divisions_rows:
        tax_id = row[0]
        print(division_id, tax_id)
        if tax_id == division_id:
            _item = {
                'division_id': tax_id,
                'division_cde': row[1],
                'division_name': row[2],
                'comments': row[3],
            }
            divisions.append(_item)
            found = True
            break
    if found:
        break
    i += 1
    if i >= 5: break

'''
if 0:
    for item in names:
        print(f'''TAXON_ID:     {item['taxon_id']}''')
        print(f'''NAME_TXT:     {item['name_txt']}''')
        print(f'''UNIQUE_NAME:  {item['unique_name']}''')
        print(f'''NAME_CLASS:   {item['name_class']}''')
        print()

    for item in divisions:
        print(f'''DIVISION_ID:      {item['division_id']}''')
        print(f'''DIVISION_CDE:     {item['division_cde']}''')
        print(f'''DIVISION_NAME:    {item['division_name']}''')
        print(f'''COMMENTS:         {item['comments']}''')
        print()

'''
quit()


quit()
'''

model_filepath = '/home/ubuntu/vault-tmp/llm/gemma-4-26B-A4B-it-UD-Q4_K_XL.gguf'


# driver.close()

# quit()

def create_node(tx):
    tx.run("CREATE (n:Test {name: $name})", name="Python Node")

'''
with driver.session() as session:
    session.execute_write(create_node)
'''

def get_nodes(tx):
    query = "MATCH (n:Test) RETURN n.name AS name"
    result = tx.run(query)
    return [record["name"] for record in result]

'''
with driver.session() as session:
    names = session.execute_read(get_nodes)
    print(names)

'''
# driver.close()
# quit()

def wikidata_taxon_names_get():
    import os
    from lib import io
    taxon_names = []
    ###
    entity_foldername = 'entity_has-use_medicinal-plant'
    entity_folderpath = f'{wikidata_folderpath}/{entity_foldername}'
    entities_filepaths = [f'{entity_folderpath}/{filename}' for filename in os.listdir(entity_folderpath)]
    ###
    relationship_foldername = 'property_medicinal-plant'
    relationship_folderpath = f'{wikidata_folderpath}/{relationship_foldername}'
    ###
    P_ID = 'P225'
    for entity_i, entity_filepath in enumerate(entities_filepaths):
        s_id = entity_filepath.split('/')[-1].split('.')[0]
        s_data = io.json_read(entity_filepath)
        claims = s_data['entities'][s_id]['claims']
        for claim in claims:
            p_id = claim.strip()
            if p_id == P_ID:
                o_taxon_name_value = claims[P_ID][0]['mainsnak']['datavalue']['value']
                # print(o_taxon_name_value)
                taxon_names.append({'id': s_id, 'taxon_name': o_taxon_name_value})
        # quit()
    return taxon_names

# wikidata_taxon_names = wikidata_taxon_names_get()

# herbs_wcvp = data.herbs_wcvp_get()
# for herb in herbs_wcvp[:100]:
    # print(herb['family'])
    # print(herb)


def wikidata_found_in_wcvp_gen():
    entity_foldername = 'entity_has-use_medicinal-plant'
    entity_folderpath = f'{wikidata_folderpath}/{entity_foldername}'
    entities_filepaths = [f'{entity_folderpath}/{filename}' for filename in os.listdir(entity_folderpath)]
    ###
    relationship_foldername = 'property_medicinal-plant'
    relationship_folderpath = f'{wikidata_folderpath}/{relationship_foldername}'
    ###
    from_folderpath = f'{wikidata_folderpath}/entity_has-use_medicinal-plant'
    to_folderpath = f'{wikidata_folderpath}/wikidata-found-in-wcvp'
    ###
    P_ID = 'P225'
    for entity_i, entity_filepath in enumerate(entities_filepaths[:99999]):
        s_id = entity_filepath.split('/')[-1].split('.')[0]
        s_data = io.json_read(entity_filepath)
        claims = s_data['entities'][s_id]['claims']
        for claim in claims:
            p_id = claim.strip()
            if p_id == P_ID:
                o_taxon_name_value = claims[P_ID][0]['mainsnak']['datavalue']['value']
                from_filepath = f'{from_folderpath}/{s_id}.json'
                to_filepath = f'{to_folderpath}/{s_id}.json' 
                if os.path.exists(to_filepath):
                    continue
                found = False
                for herb_wcvp in herbs_wcvp:
                    if o_taxon_name_value.lower().strip() == herb_wcvp['taxon_name'].lower().strip():
                        shutil.copy2(from_filepath, to_filepath)
                        print(s_id, '->', o_taxon_name_value, '->', herb_wcvp['family'])
                        found = True
                        break
                if not found:
                    print('N/A')

def wikidata_wcvp_family_gen():
    wikidata_found_in_wcvp_foldername = 'wikidata-found-in-wcvp'
    wikidata_found_in_wcvp_folderpath = f'{wikidata_folderpath}/{wikidata_found_in_wcvp_foldername}'
    wikidata_found_in_wcvp_filepaths = [
        f'{wikidata_found_in_wcvp_folderpath}/{filename}' for filename in os.listdir(wikidata_found_in_wcvp_folderpath)
    ]
    ###
    output_folderpath = f'{wikidata_folderpath}/wikidata-wcvp-jsons'
    ###
    P_ID = 'P225'
    for wikidata_found_in_wcvp_filepath in wikidata_found_in_wcvp_filepaths[:10]:
        s_id = wikidata_found_in_wcvp_filepath.split('/')[-1].split('.')[0]
        s_data = io.json_read(wikidata_found_in_wcvp_filepath)
        claims = s_data['entities'][s_id]['claims']
        for claim in claims:
            p_id = claim.strip()
            if p_id == P_ID:
                o_taxon_name_value = claims[P_ID][0]['mainsnak']['datavalue']['value']
                output_filepath = f'{output_folderpath}/{s_id}.json'
                if os.path.exists(output_filepath):
                    continue
                for herb_wcvp in herbs_wcvp:
                    if o_taxon_name_value.lower().strip() == herb_wcvp['taxon_name'].lower().strip():
                        print(s_id, '->', o_taxon_name_value, '->', herb_wcvp['family'])
                        _item = {
                            'id': s_id,
                            'taxon_name': herb_wcvp['taxon_name'],
                            'family': herb_wcvp['family'],
                        }
                        io.json_write(output_filepath, _item)
                        break

# wikidata_wcvp_family_gen()

# quit()

def scrape_powo():
    # gbif.org
    import time

    from selenium import webdriver
    from selenium.webdriver.common.keys import Keys
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.firefox.options import Options

    geckodriver_path = 'geckodriver'
    driver_service = webdriver.FirefoxService(executable_path=geckodriver_path)

    driver = webdriver.Firefox(service=driver_service)
    driver.get('https://www.google.com')
    driver.maximize_window()

    # driver.get('https://www.gbif.org/')
    time.sleep(10)

    taxon_name = 'achillea millefolium'
    powo_taxon_id = 'urn:lsid:ipni.org:names:541365-1'
    driver.get(f'https://powo.science.kew.org/taxon/{powo_taxon_id}')

    e = driver.find_element(By.XPATH, '//ul[@id="siteSearchInputHome"]')


'''
e = driver.find_element(By.XPATH, '//input[@id="siteSearchInputHome"]')
for c in 'test':
    try: e.send_keys(c)
    except: break
e.send_keys(Keys.ENTER)
'''

# quit()

def plants_taxon():
    import os
    import time
    import random

    from lib import io

    entity_foldername = 'entity_has-use_medicinal-plant'
    entity_folderpath = f'{wikidata_folderpath}/{entity_foldername}'
    entities_filepaths = [f'{entity_folderpath}/{filename}' for filename in os.listdir(entity_folderpath)]
    ###
    relationship_foldername = 'property_medicinal-plant'
    relationship_folderpath = f'{wikidata_folderpath}/{relationship_foldername}'
    ###
    for entity_i, entity_filepath in enumerate(entities_filepaths):
        s_id = entity_filepath.split('/')[-1].split('.')[0]
        s_data = io.json_read(entity_filepath)
        try: s_label = s_data['entities'][s_id]['labels']['en']['value']
        except: s_label = 'S_LABEL N/A'
        claims = s_data['entities'][s_id]['claims']
        print(entity_filepath)
        print(f'{entity_i}/{len(entities_filepaths)}')
        for claim in claims:
            p_id = claim.strip()
            p_filepath = f'{relationship_folderpath}/{p_id}.json'
            p_data = io.json_read(p_filepath)
            p_label = p_data['entities'][p_id]['labels']['en']['value']
            ###
            try: o_type = claims[p_id][0]['mainsnak']['datavalue']['type']
            except: continue
            if o_type == 'string':
                o_value = claims[p_id][0]['mainsnak']['datavalue']['value']
            elif o_type == 'monolingualtext':
                o_value = claims[p_id][0]['mainsnak']['datavalue']['value']
                o_value = o_value['text']
            else:
                o_value = claims[p_id][0]['mainsnak']['datavalue']['value']
                try: o_id = o_value['id']
                except: 
                    o_id = None
                    o_value = 'ID N/A'

                if o_id:
                    o_filepath = f'{wikidata_folderpath}/Q/{o_id}.json'
                    o_data = io.json_read(o_filepath)
                    try: o_value = o_data['entities'][o_id]['labels']['en']['value']
                    except: o_value = 'N/A'
            ###
            print(s_label, '->', p_label, '->', o_value)
            # quit()
        quit()
    quit()

# plants_taxon()

def entities_relationships_distribution():
    import os
    import time
    import random

    from lib import io

    p_distributions = []

    entity_foldername = 'entity_has-use_medicinal-plant'
    entity_folderpath = f'{wikidata_folderpath}/{entity_foldername}'
    entities_filepaths = [f'{entity_folderpath}/{filename}' for filename in os.listdir(entity_folderpath)]
    ###
    relationship_foldername = 'property_medicinal-plant'
    relationship_folderpath = f'{wikidata_folderpath}/{relationship_foldername}'
    ###
    i = 0
    for entity_i, entity_filepath in enumerate(entities_filepaths):
        s_id = entity_filepath.split('/')[-1].split('.')[0]
        s_data = io.json_read(entity_filepath)
        try: s_label = s_data['entities'][s_id]['labels']['en']['value']
        except: s_label = 'S_LABEL N/A'
        claims = s_data['entities'][s_id]['claims']
        print(entity_filepath)
        print(f'{entity_i}/{len(entities_filepaths)}')
        for claim in claims:
            p_id = claim.strip()
            p_filepath = f'{relationship_folderpath}/{p_id}.json'
            p_data = io.json_read(p_filepath)
            p_label = p_data['entities'][p_id]['labels']['en']['value']
            print(p_id)
            found = False
            for p_distribution in p_distributions:
                if p_id == p_distribution['id']:
                    p_distribution['count'] += 1
                    found = True
                    break
            if not found:
                _item = {
                    'id': p_id,
                    'label': p_label,
                    'count': 1,
                }
                p_distributions.append(_item)
        i += 1
        if i >= 99999: break
    p_distributions = sorted(p_distributions, key=lambda x: x['count'], reverse=True)
    for p_distribution in p_distributions:
        print(p_distribution)
    io.json_write(f'{wikidata_folderpath}/relationships-distribution.json', p_distributions)
    quit()

# entities_relationships_distribution()

def entities_jsons_get():
    import os
    import time
    import random

    import requests

    from lib import io

    data = io.json_read(f'{wikidata_folderpath}/entity_has-use_medicinal-plant.json')
    for item in data:
        item_url = item['item']
        item_id = item_url.split('/')[-1]
        print(item_id)
    
        output_filepath = f'{wikidata_folderpath}/entity_has-use_medicinal-plant/{item_id}.json'
        if not os.path.exists(output_filepath):
            # url = "https://www.wikidata.org/wiki/Special:EntityData/Q37153.json"
            # url = "https://www.wikidata.org/w/api.php?action=wbgetentities&ids=Q37153|P31|Q5&props=labels&languages=en&format=json"
            url = f"https://www.wikidata.org/wiki/Special:EntityData/{item_id}.json"

            headers = {
                "User-Agent": "MyWikidataApp/1.0 (your_email@example.com) requests"
            }

            response = requests.get(url, headers=headers)
            response.raise_for_status()

            data = response.json()
            # print(data["entities"]["Q37153"]["labels"]["en"]["value"])
            # print(data["entities"])
            io.json_write(output_filepath, data)

            time.sleep(random.randint(2, 3))
            # break

    quit()

def relationships_jsons_get():
    import os
    import time
    import random

    import requests

    from lib import io

    print(wikidata_folderpath)
    entity_foldername = 'entity_has-use_medicinal-plant'
    entity_folderpath = f'{wikidata_folderpath}/{entity_foldername}'
    entities_filenames = os.listdir(entity_folderpath)
    for entity_filename in entities_filenames:
        entity_id = entity_filename.split('.')[0]
        entity_filepath = f'{entity_folderpath}/{entity_filename}'
        print(entity_filepath)
        ###
        data = io.json_read(entity_filepath)
        claims = data['entities'][entity_id]['claims']
        for claim in claims:
            p_id = claim.strip()

            output_filepath = f'{wikidata_folderpath}/property_medicinal-plant/{p_id}.json'
            if not os.path.exists(output_filepath):
                url = f"https://www.wikidata.org/wiki/Special:EntityData/{p_id}.json"

                headers = {
                    "User-Agent": "MyWikidataApp/1.0 (your_email@example.com) requests"
                }

                response = requests.get(url, headers=headers)
                response.raise_for_status()

                data = response.json()
                # print(data["entities"]["Q37153"]["labels"]["en"]["value"])
                # print(data["entities"])
                io.json_write(output_filepath, data)

                time.sleep(random.randint(2, 3))
                # quit()

    quit()

def entity_json_download(q_id):
    import os
    import time
    import random

    import requests

    from lib import io

    output_filepath = f'{wikidata_folderpath}/Q/{q_id}.json'
    if not os.path.exists(output_filepath):
        url = f"https://www.wikidata.org/wiki/Special:EntityData/{q_id}.json"

        headers = {
            "User-Agent": "MyWikidataApp/1.0 (your_email@example.com) requests"
        }

        response = requests.get(url, headers=headers)
        response.raise_for_status()

        data = response.json()
        io.json_write(output_filepath, data)
        time.sleep(random.randint(2, 3))

def triples_gen():
    import os
    import time
    import random

    from lib import io

    entity_foldername = 'entity_has-use_medicinal-plant'
    entity_folderpath = f'{wikidata_folderpath}/{entity_foldername}'
    entities_filepaths = [f'{entity_folderpath}/{filename}' for filename in os.listdir(entity_folderpath)]
    ###
    relationship_foldername = 'property_medicinal-plant'
    relationship_folderpath = f'{wikidata_folderpath}/{relationship_foldername}'
    ###
    for entity_i, entity_filepath in enumerate(entities_filepaths):
        s_id = entity_filepath.split('/')[-1].split('.')[0]
        s_data = io.json_read(entity_filepath)
        try: s_label = s_data['entities'][s_id]['labels']['en']['value']
        except: s_label = 'S_LABEL N/A'
        claims = s_data['entities'][s_id]['claims']
        print(entity_filepath)
        print(f'{entity_i}/{len(entities_filepaths)}')
        for claim in claims:
            p_id = claim.strip()
            p_filepath = f'{relationship_folderpath}/{p_id}.json'
            p_data = io.json_read(p_filepath)
            p_label = p_data['entities'][p_id]['labels']['en']['value']
            ###
            try: o_type = claims[p_id][0]['mainsnak']['datavalue']['type']
            except: continue
            if o_type == 'string':
                o_value = claims[p_id][0]['mainsnak']['datavalue']['value']
            elif o_type == 'monolingualtext':
                o_value = claims[p_id][0]['mainsnak']['datavalue']['value']
                o_value = o_value['text']
            else:
                o_value = claims[p_id][0]['mainsnak']['datavalue']['value']
                try: o_id = o_value['id']
                except: 
                    o_id = None
                    o_value = 'ID N/A'

                if o_id:
                    entity_json_download(o_id)

                    o_filepath = f'{wikidata_folderpath}/Q/{o_id}.json'
                    o_data = io.json_read(o_filepath)
                    try: o_value = o_data['entities'][o_id]['labels']['en']['value']
                    except: o_value = 'N/A'
                    # quit()
                    # print(p_id)
                    # print(o_value)
            ###
            print(s_label, '->', p_label, '->', o_value)
            # quit()
        # quit()
    quit()

# entities_jsons_get()
# relationships_jsons_get()

# triples_gen()

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
    with open(f"{wikidata_folderpath}/{s_id}.json", "r", encoding="utf-8") as f:
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

# triples_extraction()

# quit()

'''
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
'''


def get_results(endpoint_url, query):
    user_agent = "WDQS-example Python/%s.%s" % (sys.version_info[0], sys.version_info[1])
    # TODO adjust user agent; see https://w.wiki/CX6
    sparql = SPARQLWrapper(endpoint_url, agent=user_agent)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    return sparql.query().convert()


'''
for i in range(2):
    results = get_results(endpoint_url, query)

    for result in results["results"]["bindings"]:
        print(result)

    print(len(results["results"]["bindings"]))
'''


def main():
    sqlite_table_nodes_create(nodes)
    quit()

main()

