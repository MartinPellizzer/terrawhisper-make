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

kg_folderpath = f'{g.SSOT_FOLDERPATH}/kg'
wikidata_folderpath = f'{g.SSOT_FOLDERPATH}/wikidata'
powo_folderpath = f'{g.SSOT_FOLDERPATH}/powo'
# taxdmp_folderpath = f'{wikidata_folderpath}/taxdmp'
# taxdmp_nodes_filepath = f'{taxdmp_folderpath}/nodes.dmp'
# taxdmp_names_filepath = f'{taxdmp_folderpath}/names.dmp'
sqlite_database_filepath = f'{kg_folderpath}/taxonomy.db'
lotus_filepath = f'{g.SSOT_FOLDERPATH}/lotus/lotusUniqueNaturalProduct.bson'
herb20_filepath = f'{g.SSOT_FOLDERPATH}/herb20/HERB_herb_info_v2.txt'
pubchem_folderpath = f'{g.SSOT_FOLDERPATH}/pubchem'
lotus_folderpath = f'{g.SSOT_FOLDERPATH}/lotus'

def neo4j_clear_db():
    driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "Newoliark1"))
    def delete_data(tx):
        tx.run("MATCH (n) DETACH DELETE n")
    def drop_constraints(tx):
        result = tx.run("SHOW CONSTRAINTS")
        for record in result:
            name = record["name"]
            tx.run(f"DROP CONSTRAINT {name}")
    def drop_indexes(tx):
        result = tx.run("SHOW INDEXES")
        for record in result:
            name = record["name"]
            tx.run(f"DROP INDEX {name}")
    with driver.session() as session:
        session.execute_write(delete_data)
    with driver.session() as session:
        session.execute_write(drop_constraints)
    with driver.session() as session:
        session.execute_write(drop_indexes)
    driver.close()

# neo4j_clear_db()
# quit()

################################################################################
# KG
################################################################################

def kg__entities__plants():
    wikidata_powo_folderpath = f'{g.SSOT_FOLDERPATH}/wikidata-powo/0000-ids'
    wikidata_powo_filenames = os.listdir(wikidata_powo_folderpath)
    wikidata_powo_data = []
    for wikidata_powo_i, wikidata_powo_filename in enumerate(wikidata_powo_filenames):
        print(f'{wikidata_powo_i}/{len(wikidata_powo_filenames)}')
        wikidata_powo_filepath = f'{wikidata_powo_folderpath}/{wikidata_powo_filename}'
        _data = io.json_read(wikidata_powo_filepath)
        wikidata_powo_data.append(_data)
    for item in wikidata_powo_data:
        print(json.dumps(item, indent=4))
    print(len(wikidata_powo_data))
    tw_plants_data = []
    for item_i, item in enumerate(wikidata_powo_data):
        tw_plant_id = 'TERRA:PLANT:' + str(item_i)
        tw_plant_name = item['powo_plant_name']
        tw_plant_item = {
            'tw_id': tw_plant_id,
            'name': tw_plant_name,
        }
        tw_plants_data.append(tw_plant_item)
    io.json_write(f'{g.SSOT_FOLDERPATH}/kg/entities/plants.json', tw_plants_data)
    preview_data = io.json_read(f'{g.SSOT_FOLDERPATH}/kg/entities/plants.json')
    for preview_item in preview_data:
        print(preview_item)

# kg__entities__plants()
# quit()

def kg__entities__compounds():
    input_folderpath = f'{g.SSOT_FOLDERPATH}/wikidata-powo-lotus/0000-ids'
    input_filenames = os.listdir(input_folderpath)
    input_data = []
    for input_i, input_filename in enumerate(input_filenames):
        print(f'{input_i}/{len(input_filenames)}')
        input_filepath = f'{input_folderpath}/{input_filename}'
        _data = io.json_read(input_filepath)
        input_data.append(_data)
    # extract + deduplicate compounds
    seen = set()
    compounds_items = []
    for item in input_data:
        for compound_item in item['lotus_plant_components']:
            if compound_item['component_lotus_id'] in seen: continue
            compounds_items.append(compound_item)
            seen.add(compound_item['component_lotus_id'])
    # for item in compounds_items:
        # print(json.dumps(item, indent=4))
    tw_compounds_data = []
    for item_i, item in enumerate(compounds_items):
        tw_compound_id = 'TERRA:COMPOUND:' + str(item_i)
        compound_name = item['component_taxonomy_classyfire_parent']
        compound_inchikey = item['component_inchikey']
        tw_compound_item = {
            'tw_id': tw_compound_id,
            'inchikey': compound_inchikey,
            'name': compound_name,
        }
        tw_compounds_data.append(tw_compound_item)
    io.json_write(f'{g.SSOT_FOLDERPATH}/kg/entities/compounds.json', tw_compounds_data)
    preview_data = io.json_read(f'{g.SSOT_FOLDERPATH}/kg/entities/compounds.json')
    for preview_item in preview_data:
        print(preview_item)

# kg__entities__compounds()
# quit()

def kg__relationships__plants_compounds():
    entities_plants_data = io.json_read(f'{g.SSOT_FOLDERPATH}/kg/entities/plants.json')
    entities_compounds_data = io.json_read(f'{g.SSOT_FOLDERPATH}/kg/entities/compounds.json')
    input_folderpath = f'{g.SSOT_FOLDERPATH}/wikidata-powo-lotus/0000-ids'
    input_filenames = os.listdir(input_folderpath)
    triples_plant_compound = []
    for input_i, input_filename in enumerate(input_filenames[:]):
        print(f'{input_i}/{len(input_filenames)}')
        input_filepath = f'{input_folderpath}/{input_filename}'
        input_data = io.json_read(input_filepath)
        # print(json.dumps(input_data, indent=4))
        plant_name = input_data['powo_plant_name']
        tw_plant_id = ''
        for entity_plant_item in entities_plants_data:
            tw_name = entity_plant_item['name']
            if plant_name == tw_name:
                tw_plant_id = entity_plant_item['tw_id']
                break
        for i, compound_item in enumerate(input_data['lotus_plant_components']):
            compound_inchikey = compound_item['component_inchikey']
            tw_compound_id = ''
            for entity_compound_item in entities_compounds_data:
                # print(entity_compound_item['inchikey'])
                if compound_inchikey == entity_compound_item['inchikey']:
                    tw_compound_id = entity_compound_item['tw_id']
                    # print(tw_plant_id, tw_compound_id)
                    triples_plant_compound.append([tw_plant_id, 'has_compound', tw_compound_id])
                    break
    output_content = ''
    for triple in triples_plant_compound:
        triple_tsv = '\t'.join(triple)
        output_content += triple_tsv + '\n'
    output_content = output_content.strip()
    io.file_write(f'{g.SSOT_FOLDERPATH}/kg/relationships/plants-compounds.tsv', output_content)
    quit()

# kg__relationships__plants_compounds()
# quit()

def kg__relationships__plants_compounds__preview():
    lines = io.csv_read(f'{g.SSOT_FOLDERPATH}/kg/relationships/plants-compounds.tsv', delimiter='\t')
    for line in lines[:10]:
        print(line)
    print(len(lines))

def kg__relationships__plants_compounds__add():
    neo4j_clear_db()
    driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "Newoliark1"))
    lines = io.csv_read(f'{g.SSOT_FOLDERPATH}/kg/relationships/plants-compounds.tsv', delimiter='\t')
    with driver.session() as session:
        session.run("CREATE CONSTRAINT plant_id IF NOT EXISTS FOR (n:PLANT) REQUIRE n.id IS NODE KEY;")
        session.run("CREATE CONSTRAINT compound_id IF NOT EXISTS FOR (n:COMPOUND) REQUIRE n.id IS NODE KEY;")
    with driver.session() as session:
        def query_exe(tx, batch):
            tx.run("""
                UNWIND $rows AS row
                MERGE (a:PLANT {id: row.plant_id})
                MERGE (b:COMPOUND {id: row.compound_id})
                MERGE (a)-[:HAS_COMPOUND]->(b)
            """, rows=batch)
        batch = []
        for line_i, line in enumerate(lines):
            batch.append({"plant_id": line[0], "compound_id": line[2]})
            if len(batch) == 1000:
                session.execute_write(query_exe, batch)
                batch = []
            print(line_i)
        if batch:
            session.execute_write(query_exe, batch)
    driver.close()

# kg__relationships__plants_compounds__add()
# quit()

def kg__relationships__plants_compounds__preview():
    entities_plants_data = io.json_read(f'{g.SSOT_FOLDERPATH}/kg/entities/plants.json')
    entities_compounds_data = io.json_read(f'{g.SSOT_FOLDERPATH}/kg/entities/compounds.json')
    driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "Newoliark1"))
    with driver.session() as session:
        # query_multihop = """
            # MATCH p=(a:plant)-[:HAS_COMPOUND*]->(b)
            # RETURN p
        # """
        result = session.run("""
            MATCH p=(a:PLANT)-[:HAS_COMPOUND]->(b:COMPOUND)
            RETURN p
        """)
        subjects = []
        objects = []
        for record_i, record in enumerate(result):
            print(record_i)
            p = record["p"]
            for node in p.nodes:
                node = dict(node)
                node_id = node['id']
                if 'PLANT' in node_id:
                    for entity_plant_data in entities_plants_data:
                        tw_id = entity_plant_data['tw_id']
                        name = entity_plant_data['name']
                        if node_id == tw_id:
                            subjects.append(name)
                            break
                elif 'COMPOUND' in node_id:
                    for entity_compound_data in entities_compounds_data:
                        tw_id = entity_compound_data['tw_id']
                        name = entity_compound_data['name']
                        if node_id == tw_id:
                            objects.append(name)
                            break
        for i in range(len(subjects)):
            print(subjects[i], 'HAS_COMPOUND', objects[i])
    driver.close()

def kg__bridge__compounds():
    input_data_folderpath = f'{g.SSOT_FOLDERPATH}/wikidata-powo-lotus-pubchem-oregano/0003-mesh-names'
    input_data_filenames = [item for item in os.listdir(input_data_folderpath)]
    input_data = []
    for i, input_data_filename in enumerate(input_data_filenames):
        print(f'{i}/{len(input_data_filenames)}')
        input_data_filepath = f'{input_data_folderpath}/{input_data_filename}'
        _data = io.json_read(input_data_filepath)
        input_data.append(_data)
    ###
    kg_compounds_data = io.json_read(f'{g.SSOT_FOLDERPATH}/kg/entities/compounds.json')
    bridges = []
    for kg_compound_item in kg_compounds_data[:]:
        for input_item in input_data:
            found = False
            for lotus_plant_component in input_item['lotus_plant_components']:
                if lotus_plant_component['component_inchikey'] == kg_compound_item['inchikey']:
                    try: oregano_id = lotus_plant_component['oregano_id']
                    except: oregano_id = ''
                    bridge = [kg_compound_item['tw_id'], kg_compound_item['inchikey'], lotus_plant_component['component_lotus_id'], oregano_id]
                    # print(kg_compound_item['inchikey'], '->', oregano_id)
                    print(bridge)
                    bridges.append(bridge)
                    found = True
                    break
            if found:
                break
    output_content = ''
    for bridge in bridges:
        bridge_tsv = '\t'.join(bridge)
        output_content += bridge_tsv + '\n'
    output_content = output_content.strip()
    io.file_write(f'{g.SSOT_FOLDERPATH}/kg/bridges/compounds.tsv', output_content)

# kg__bridge__compounds()
# quit()

def kg__bridge__compounds__preview():
    input_filepath = f'{g.SSOT_FOLDERPATH}/kg/bridges/compounds.tsv'
    input_lines = io.file_read(input_filepath).split('\n')
    for line in input_lines[:100]:
        line_pieces = line.split('\t')
        print(line_pieces)
    print(len(input_lines))

# kg__bridge__compounds__preview()
# quit()

def kg__bridge__compounds__filter():
    input_filepath = f'{g.SSOT_FOLDERPATH}/kg/bridges/compounds.tsv'
    input_lines = io.file_read(input_filepath).split('\n')
    output_lines = []
    for line in input_lines[:]:
        line_pieces = line.split('\t')
        failed = False
        for piece in line_pieces:
            if piece.strip() == '':
                failed = True
                break
        if not failed:
            output_lines.append(line)
    output_content = ''
    for line in output_lines:
        line_tsv = line
        output_content += line_tsv + '\n'
    output_content = output_content.strip()
    io.file_write(f'{g.SSOT_FOLDERPATH}/kg/bridges/compounds-filter.tsv', output_content)
    ### preview
    input_filepath = f'{g.SSOT_FOLDERPATH}/kg/bridges/compounds-filter.tsv'
    input_lines = io.file_read(input_filepath).split('\n')
    for line in input_lines[:100]:
        line_pieces = line.split('\t')
        print(line_pieces)
    print(len(input_lines))

# kg__bridge__compounds__filter()
# quit()

def kg__relationsips__compound_disease__extract():
    oregano_relationships_filepath = f'{g.SSOT_FOLDERPATH}/oregano/oregano-master/Data_OREGANO/Graphs/OREGANO_V3.tsv'
    oregano_relationships_lines = io.file_read(oregano_relationships_filepath).split('\n')
    bridges_compounds_filepath = f'{g.SSOT_FOLDERPATH}/kg/bridges/compounds-filter.tsv'
    bridges_compounds_lines = io.file_read(bridges_compounds_filepath).split('\n')
    oregano_relationships_lines_filtered = []
    for i, oregano_relationship_line in enumerate(oregano_relationships_lines[:]):
        print(i)
        oregano_relationship_pieces = oregano_relationship_line.split('\t')
        if len(oregano_relationship_pieces) == 3:
            oregano_relationship_node_1 = oregano_relationship_pieces[0]
            oregano_relationship_type = oregano_relationship_pieces[1]
            oregano_relationship_node_2 = oregano_relationship_pieces[2]
            if oregano_relationship_type == 'is_substance_that_treats':
                oregano_relationships_lines_filtered.append(oregano_relationship_line)
    print(len(oregano_relationships_lines_filtered))
    output_content = '\n'.join(oregano_relationships_lines_filtered)
    io.file_write(f'{g.SSOT_FOLDERPATH}/oregano/relationships-is_substance_that_treats.tsv', output_content)

def kg__relationsips__compound_disease__extract__preview():
    lines = io.file_read(f'{g.SSOT_FOLDERPATH}/oregano/relationships-is_substance_that_treats.tsv').split('\n')
    print(len(lines))

# kg__relationsips__compound_disease__extract()
kg__relationsips__compound_disease__extract__preview()
quit()

########################################
# DATASETS DOWNLOAD
########################################
quit()

########################################
# DATASETS DOWNLOAD
########################################
def chunks(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i+n]

def wikidata_medicinal_plants_download():
    ### wikidata/0000
    data = io.json_read(f'{wikidata_folderpath}/entity_has-use_medicinal-plant.json')
    for item in data:
        item_url = item['item']
        item_id = item_url.split('/')[-1]
        print(item_id)
        output_filepath = f'{wikidata_folderpath}/0000-medicinal-plants/{item_id}.json'
        if not os.path.exists(output_filepath):
            url = f"https://www.wikidata.org/wiki/Special:EntityData/{item_id}.json"
            headers = {
                "User-Agent": "MyWikidataApp/1.0 (your_email@example.com) requests"
            }
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            data = response.json()
            io.json_write(output_filepath, data)
            time.sleep(random.randint(2, 3))
            # break
    quit()

def wikidata_medicinal_plants_properties_download():
    ### wikidata/0001
    entity_folderpath = f'{wikidata_folderpath}/0000-medicinal-plants'
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
            output_filepath = f'{wikidata_folderpath}/0001-properties/{p_id}.json'
            if not os.path.exists(output_filepath):
                url = f"https://www.wikidata.org/wiki/Special:EntityData/{p_id}.json"
                headers = {
                    "User-Agent": "MyWikidataApp/1.0 (your_email@example.com) requests"
                }
                response = requests.get(url, headers=headers)
                response.raise_for_status()
                data = response.json()
                io.json_write(output_filepath, data)
                time.sleep(random.randint(2, 3))
                # quit()
    quit()

def wikidata_medicinal_plants_properties_distribution():
    ### wikidata/0002
    p_distributions = []
    entity_foldername = 'entity_has-use_medicinal-plant'
    entity_folderpath = f'{wikidata_folderpath}/{entity_foldername}'
    entities_filepaths = [f'{entity_folderpath}/{filename}' for filename in os.listdir(entity_folderpath)]
    ###
    relationship_folderpath = f'{wikidata_folderpath}/0001-properties'
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
    io.json_write(f'{wikidata_folderpath}/0002-distribution/relationships-distribution.json', p_distributions)
    quit()

def wikidata_medicinal_plants_find_in_wcvp():
    entity_folderpath = f'{wikidata_folderpath}/0000-medicinal-plants'
    entities_filepaths = [f'{entity_folderpath}/{filename}' for filename in os.listdir(entity_folderpath)]
    ###
    from_folderpath = entity_folderpath
    to_folderpath = f'{wikidata_folderpath}/0003-found-in-wcvp'
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

################################################################################
# POWO -> taxonomy
################################################################################
def powo_plants_download_jsons():
    plants_folderpath = f'{wikidata_folderpath}/0000-medicinal-plants'
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
            output_filepath = f'{kg_folderpath}/powo/0000-plants/{value_url_id}.json'
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

################################################################################
# WIKIDATA/POWO
################################################################################
def wikidata_plants__powo_plants__match_jsons():
    plants_folderpath = f'{wikidata_folderpath}/0000-medicinal-plants'
    plants_filepaths = sorted([f'{plants_folderpath}/{filename}' for filename in os.listdir(plants_folderpath)])
    failed = []
    powo_plants = []
    for plant_filepath_i, plant_filepath in enumerate(plants_filepaths):
        print(f'{plant_filepath_i}/{len(plants_filepaths)}')
        plant_filename_raw = plant_filepath.split('/')[-1].split('.')[0]
        plant_data = io.json_read(plant_filepath)
        try: claim = plant_data['entities'][plant_filename_raw]['claims']['P5037'][0]
        except: claim = None
        if claim:
            value = claim['mainsnak']['datavalue']['value']
            print(json.dumps(value, indent=4))
            value_url_id = value.split(':')[-1]
            print(value_url_id)
            powo_filepath = f'{powo_folderpath}/0000-plants/{value_url_id}.json'
            if os.path.exists(powo_filepath):
                powo_plant_data = io.json_read(powo_filepath)
                powo_plant_kingdom = powo_plant_data['kingdom']
                powo_plant_phylum = powo_plant_data['phylum']
                powo_plant_class = powo_plant_data['clazz']
                powo_plant_subclass = powo_plant_data['subclass']
                powo_plant_order = powo_plant_data['order']
                powo_plant_family = powo_plant_data['family']
                powo_plant_genus = powo_plant_data['genus']
                try: powo_plant_species = powo_plant_data['species']
                except: powo_plant_species = ''
                powo_plant_name = powo_plant_data['name']
                powo_plant_rank = powo_plant_data['rank']
                # print(json.dumps(powo_plant_data, indent=4))
                # print(plant_filename_raw)
                # quit()
                _powo_plant = {
                    'wikidata_id': plant_filename_raw,
                    'powo_id': value_url_id,
                    'powo_plant_kingdom': powo_plant_kingdom,
                    'powo_plant_phylum': powo_plant_phylum,
                    'powo_plant_class': powo_plant_class,
                    'powo_plant_subclass': powo_plant_subclass,
                    'powo_plant_order': powo_plant_order,
                    'powo_plant_family': powo_plant_family,
                    'powo_plant_genus': powo_plant_genus,
                    'powo_plant_species': powo_plant_species,
                    'powo_plant_name': powo_plant_name,
                    'powo_plant_rank': powo_plant_rank,
                }
                powo_plants.append(_powo_plant)
                output_filepath = f'{g.SSOT_FOLDERPATH}/wikidata-powo/0000-ids/{plant_filename_raw}.json'
                io.json_write(output_filepath, _powo_plant)
            else:
                failed.append(powo_filepath)
    print(len(failed))
    ranks = set([item['powo_plant_rank'] for item in powo_plants])
    genus_count = 0
    species_count = 0
    form_count = 0
    subspecies_count = 0
    variety_count = 0
    for powo_plant in powo_plants:
        rank = powo_plant['powo_plant_rank']
        if rank.lower() == 'genus': genus_count += 1
        elif rank.lower() == 'species': species_count += 1
        elif rank.lower() == 'form': form_count += 1
        elif rank.lower() == 'subspecies': subspecies_count += 1
        elif rank.lower() == 'variety': variety_count += 1
    print(genus_count)
    print(species_count)
    print(form_count)
    print(subspecies_count)
    print(variety_count)
        
    # print(ranks)
    quit()


################################################################################
# LOTUS -> plants constituents
################################################################################
def lotus_bson_preview():
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
    for doc_i, doc in enumerate(first_n_bson(lotus_filepath, 1000000)):
        print(json.dumps(doc, indent=4, default=str))
        quit()

# lotus_bson_preview()
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
    wikidata_count = 0
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
    for doc_i, doc in enumerate(first_n_bson(lotus_filepath, 1000000)):
        # print(doc["inchikey"])
        # print(json.dumps(doc, indent=4, default=str))
        # quit()
        docs_num += 1
        print(doc_i)
        component_lotus_id = doc['lotus_id']
        try: component_wikidata_id = doc['wikidata_id']
        except: 
            component_wikidata_id = None
            wikidata_count += 1
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
    print('WIKIDATA FAILED COUNTER:', wikidata_count)
    lotus_output_filepath = f'{g.SSOT_FOLDERPATH}/lotus/0000-bson-to-json/data.json'
    io.json_write(lotus_output_filepath, export_items)
    quit()

def lotus_group_components_by_plant():
    output_data = []
    input_filepath = f'{lotus_folderpath}/0000-bson-to-json/data.json'
    input_data = io.json_read(input_filepath)
    for input_i, input_item in enumerate(input_data[:]):
        print(f'{input_i}/{len(input_data)}')
        plant_names = input_item['plant_names']
        component_lotus_id = input_item['component_lotus_id']
        component_inchikey = input_item['component_inchikey']
        component_wikidata_id = input_item['component_wikidata_id']
        component_taxonomy_npclassifier_pathway = input_item['component_taxonomy_npclassifier_pathway']
        component_taxonomy_npclassifier_superclass = input_item['component_taxonomy_npclassifier_superclass']
        component_taxonomy_npclassifier_class = input_item['component_taxonomy_npclassifier_class']
        component_taxonomy_classyfire_kingdom = input_item['component_taxonomy_classyfire_kingdom']
        component_taxonomy_classyfire_superclass = input_item['component_taxonomy_classyfire_superclass']
        component_taxonomy_classyfire_class = input_item['component_taxonomy_classyfire_class']
        component_taxonomy_classyfire_parent = input_item['component_taxonomy_classyfire_parent']
        # print(json.dumps(input_item, indent=4))
        # quit()
        for plant_name in plant_names:
            plant_name = plant_name.strip().lower()
            found = False
            for output_item in output_data:
                if plant_name == output_item['plant_name']:
                    new_component = {
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
                    }
                    output_item['components'].append(new_component)
                    found = True
                    break
            if not found:
                new_item = {
                    'plant_name': plant_name,
                    'components': [
                        {
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
                        },
                    ]
                }
                output_data.append(new_item)
        # print(plant_names)
    print(len(output_data))
    # print(json.dumps(output_data, indent=4))
    io.json_write(f'{lotus_folderpath}/0001-plants-constituents-group/data.json', output_data)
    # for output_item in output_data:
        # if len(output_item['components']) > 1:
            # print(json.dumps(output_item, indent=4))

################################################################################
# WIKIDATA/POWO + LOTUS
################################################################################
def wikidata_powo_plants__lotus_plants__match_jsons():
    wikidata_powo_folderpath = f'{g.SSOT_FOLDERPATH}/wikidata-powo/0000-ids'
    wikidata_powo_filenames = os.listdir(wikidata_powo_folderpath)
    wikidata_powo_data = []
    for wikidata_powo_i, wikidata_powo_filename in enumerate(wikidata_powo_filenames):
        print(f'{wikidata_powo_i}/{len(wikidata_powo_filenames)}')
        wikidata_powo_filepath = f'{wikidata_powo_folderpath}/{wikidata_powo_filename}'
        _data = io.json_read(wikidata_powo_filepath)
        wikidata_powo_data.append(_data)
    lotus_filepath = f'{lotus_folderpath}/0001-plants-constituents-group/data.json'
    lotus_data = io.json_read(lotus_filepath)
    for lotus_item_i, lotus_item in enumerate(lotus_data):
        print(f'{lotus_item_i}/{len(lotus_data)}')
        # print(json.dumps(lotus_item, indent=4))
        # print(len(lotus_item['components']))
        lotus_plant_name = lotus_item['plant_name']
        found = False
        for wikidata_powo_item in wikidata_powo_data:
            wikidata_id = wikidata_powo_item['wikidata_id']
            powo_plant_name = wikidata_powo_item['powo_plant_name']
            if lotus_plant_name.lower().strip() == powo_plant_name.lower().strip():
                lotus_plant_name = lotus_item['plant_name']
                lotus_plant_components = lotus_item['components']
                output_data = {
                    **wikidata_powo_item, 
                    'lotus_plant_name': lotus_plant_name,
                    'lotus_plant_components': lotus_plant_components,
                }
                # print(json.dumps(output_data, indent=4))
                output_filepath = f'{g.SSOT_FOLDERPATH}/wikidata-powo-lotus/0000-ids/{wikidata_id}.json'
                io.json_write(output_filepath, output_data)
                # quit()
            pass
        # quit()
    # for x in wikidata_powo_data:
        # print(x)

################################################################################
# PUBCHEM
################################################################################
def pubchem_sqlite_table_inchikey_cid_create():
    pubchem_cid_inchikey_filepath = f'{pubchem_folderpath}/CID-InChI-Key'
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

################################################################################
# WIKIDATA/POWO/LOTUS + PUBCHEM
################################################################################
def wikidta_powo_lotus_inchikey__pubchem_cids__merge():
    input_folderpath = f'{g.SSOT_FOLDERPATH}/wikidata-powo-lotus/0000-ids'
    input_filenames = os.listdir(input_folderpath)
    for input_filename_i, input_filename in enumerate(input_filenames[:]):
        print(f'{input_filename_i}/{len(input_filenames)}')
        input_filepath = f'{input_folderpath}/{input_filename}'
        input_data = io.json_read(input_filepath)
        lotus_plant_components = input_data['lotus_plant_components']
        output_filepath = f'{g.SSOT_FOLDERPATH}/wikidata-powo-lotus-pubchem/0000-ids/{input_filename}'
        for i, lotus_plant_component in enumerate(lotus_plant_components):
            lotus_plant_component_inchikey = lotus_plant_component['component_inchikey']
            # print(lotus_plant_component_inchikey)
            # print(json.dumps(input_data, indent=4))
            conn = sqlite3.connect(f'{pubchem_folderpath}/pubchem_inchikey_cid_mapping.db')
            cur = conn.cursor()
            cur.execute(
                "SELECT cid FROM pubchem_inchikey_cid_mapping WHERE inchikey = ?",
                (lotus_plant_component_inchikey,)
            )
            results = [row[0] for row in cur.fetchall()]
            conn.close()
            lotus_plant_component['pubchem_cids'] = results
            # print(json.dumps(lotus_plant_component, indent=4))
            # break
        io.json_write(output_filepath, input_data)
        # quit()
    return results

################################################################################
# OREGANO
################################################################################
def oregano_clear_db():
    driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "Newoliark1"))
    def delete_data(tx):
        tx.run("MATCH (n) DETACH DELETE n")
    def drop_constraints(tx):
        result = tx.run("SHOW CONSTRAINTS")
        for record in result:
            name = record["name"]
            tx.run(f"DROP CONSTRAINT {name}")
    def drop_indexes(tx):
        result = tx.run("SHOW INDEXES")
        for record in result:
            name = record["name"]
            tx.run(f"DROP INDEX {name}")
    with driver.session() as session:
        session.execute_write(delete_data)
    with driver.session() as session:
        session.execute_write(drop_constraints)
    with driver.session() as session:
        session.execute_write(drop_indexes)
    driver.close()

def oregano__kg_create__batch_grouped():
    from collections import defaultdict
    driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "Newoliark1"))
    oregano_relationships_filepath = f'{g.SSOT_FOLDERPATH}/oregano/oregano-master/Data_OREGANO/Graphs/OREGANO_V3.tsv'
    def batch_insert_grouped(tx, grouped_batch):
        for rel_type, rows in grouped_batch.items():
            query = f"""
            UNWIND $rows AS row
            WITH row,
                 split(row.s, ":")[0] AS s_type,
                 split(row.s, ":")[1] AS s_id,
                 split(row.o, ":")[0] AS o_type,
                 split(row.o, ":")[1] AS o_id
            MERGE (s:Entity {{id: row.s}})
            SET s.type = s_type
            MERGE (o:Entity {{id: row.o}})
            SET o.type = o_type
            MERGE (s)-[:{rel_type}]->(o)
            """
            tx.run(query, rows=rows)
    batch = defaultdict(list)
    batch_size = 5000
    with open(oregano_relationships_filepath) as f:
        with driver.session() as session:
            session.run("CREATE INDEX entity_id IF NOT EXISTS FOR (n:Entity) ON (n.id)")
            for line in f:
                s, p, o = line.strip().split("\t")
                if p == "rdf/type":
                    continue
                batch[p].append({"s": s, "o": o})
                if sum(len(v) for v in batch.values()) >= batch_size:
                    session.execute_write(batch_insert_grouped, batch)
                    batch.clear()
                    print(batch_size)
            if batch:
                session.execute_write(batch_insert_grouped, batch)
    driver.close()

################################################################################
# WIKIDATA/POWO/LOTUS/PUBCHEM + OREGANO
################################################################################
def wikidata_powo_lotus_pubchem_cids__oregano_ids__merge():
    oregano_data = []
    oregano_compounds_text = io.file_read(
        f'{g.SSOT_FOLDERPATH}/oregano/oregano-master/Integration/Integration V3/GESTION_ID/COMPOUND.tsv'
    )
    oregano_compounds_lines = oregano_compounds_text.split('\n')
    ###
    headings = oregano_compounds_lines[0].split('\t')
    headings[0] = 'ID_OREGANO'
    cids = []
    for line_i, line in enumerate(oregano_compounds_lines[:]):
        print(line_i)
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
        # print('ID:', item['ID_OREGANO'], '  WIKIDATA:', item['WIKIPEDIA'], '  CID:', pubchem_compound_id)
        item = {
            'oregano_id': item['ID_OREGANO'],
            'pubchem_cid': pubchem_compound_id,
        }
        oregano_data.append(item)
    input_folderpath = f'{g.SSOT_FOLDERPATH}/wikidata-powo-lotus-pubchem/0000-ids'
    input_filenames = os.listdir(input_folderpath)
    # input_data = []
    for i, input_filename in enumerate(input_filenames[:]):
        print(i)
        # print(json.dumps(input_item, indent=4))
        input_filepath = f'{input_folderpath}/{input_filename}'
        input_item = io.json_read(input_filepath)
        input_components = input_item['lotus_plant_components']
        for input_component_i, input_component in enumerate(input_components):
            # print(f'{input_component_i}/{len(input_components)}')
            pubchem_cids = input_component['pubchem_cids']
            for pubchem_cid in pubchem_cids:
                pubchem_cid_found = False
                for oregano_item in oregano_data:
                    oregano_id = oregano_item['oregano_id']
                    if oregano_item['pubchem_cid'] == pubchem_cid:
                        # print(oregano_id, pubchem_cid)
                        input_component['oregano_id'] = oregano_id
                        pubchem_cid_found = True
                        break
                        # quit()
                if pubchem_cid_found:
                    # print(input_component)
                    break
                    # quit()
            # print(pubchem_ids)
        output_filepath = f'{g.SSOT_FOLDERPATH}/wikidata-powo-lotus-pubchem-oregano/0000-ids/{input_filename}'
        io.json_write(output_filepath, input_item)
        # quit()

################################################################################
# WIKIDATA/POWO/LOTUS/PUBCHEM/OREGANO + INTERNALE MAPPING
################################################################################
def wikidata_powo_lotus_pubchem_oregano__compounds_ids__diseases_ids_merge():
    driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "Newoliark1"))
    input_folderpath = f'{g.SSOT_FOLDERPATH}/wikidata-powo-lotus-pubchem-oregano/0000-ids'
    input_filenames = sorted(os.listdir(input_folderpath))
    for i, input_filename in enumerate(input_filenames[:]):
        print(f'{i}/{len(input_filenames)}')
        input_filepath = f'{input_folderpath}/{input_filename}'
        input_item = io.json_read(input_filepath)
        # print(json.dumps(input_item, indent=4))
        for lotus_plant_component in input_item['lotus_plant_components']:
            if 'oregano_id' in lotus_plant_component:
                oregano_component_id = lotus_plant_component['oregano_id']
                # print(oregano_component_id)
                # quit()
                query = """
                    MATCH p=(s:Entity {id: $compound_id})
                            -[:is_substance_that_treats]->
                            (o) 
                    RETURN o.id as id
                """
                with driver.session() as session:
                    result = session.run(query, compound_id=oregano_component_id)
                    diseases = [record['id'] for record in result]
                    # print(diseases)
                    if diseases != []:
                        # quit()
                        pass
                    lotus_plant_component['oregano_diseases_ids'] = diseases
        output_folderpath = f'{g.SSOT_FOLDERPATH}/wikidata-powo-lotus-pubchem-oregano/0001-diseases'
        output_filepath = f'{output_folderpath}/{input_filename}'
        # print(json.dumps(input_item, indent=4))
        io.json_write(output_filepath, input_item)
        # break
    driver.close()
    ###
    input_folderpath = f'{g.SSOT_FOLDERPATH}/wikidata-powo-lotus-pubchem-oregano/0001-diseases'
    input_filenames = sorted(os.listdir(input_folderpath))
    for i, input_filename in enumerate(input_filenames[:]):
        print(f'{i}/{len(input_filenames)}')
        input_filepath = f'{input_folderpath}/{input_filename}'
        input_item = io.json_read(input_filepath)
        for lotus_plant_component in input_item['lotus_plant_components']:
            if 'oregano_diseases_ids' in lotus_plant_component:
                oregano_diseases_ids = lotus_plant_component['oregano_diseases_ids']
                print(oregano_diseases_ids)
        # quit()

def oregano_disease_ids__mesh_disease_ids():
    oregano_data = []
    oregano_file_content = io.file_read(
        f'{g.SSOT_FOLDERPATH}/oregano/oregano-master/Integration/Integration V3/GESTION_ID/DISEASES.tsv'
    )
    oregano_compounds_lines = oregano_file_content.split('\n')
    ###
    headings = oregano_compounds_lines[0].split('\t')
    headings[0] = 'ID'
    oregano_diseases_items = []
    for line_i, line in enumerate(oregano_compounds_lines[:]):
        print(line_i)
        if line_i == 0: continue
        if line.strip() == '': continue
        values = line.split('\t')
        item = {}
        for i in range(len(headings)):
            item[headings[i]] = values[i].strip()
        oregano_diseases_items.append(item)
    ###
    input_folderpath = f'{g.SSOT_FOLDERPATH}/wikidata-powo-lotus-pubchem-oregano/0001-diseases'
    input_filenames = sorted(os.listdir(input_folderpath))
    for i, input_filename in enumerate(input_filenames[:]):
        print(f'{i}/{len(input_filenames)}')
        input_filepath = f'{input_folderpath}/{input_filename}'
        input_item = io.json_read(input_filepath)
        for lotus_plant_component in input_item['lotus_plant_components']:
            lotus_plant_component['mesh_diseases_ids'] = []
            if 'oregano_diseases_ids' in lotus_plant_component:
                oregano_diseases_ids = lotus_plant_component['oregano_diseases_ids']
                if oregano_diseases_ids != []:
                    for oregano_disease_id in oregano_diseases_ids:
                        print(oregano_disease_id)
                        # match oregano/mesh disease ids
                        for oregano_disease_item in oregano_diseases_items:
                            if oregano_disease_item['ID'] == oregano_disease_id:
                                if 'MESH' in oregano_disease_item and oregano_disease_item['MESH'] != '': 
                                    mesh_id = oregano_disease_item['MESH']
                                    lotus_plant_component['mesh_diseases_ids'].append(mesh_id)
                                    print(oregano_disease_id, mesh_id)
                                    # quit()
                                    break
                        # quit()
        # print(json.dumps(input_item, indent=4))
        output_filepath = f'{g.SSOT_FOLDERPATH}/wikidata-powo-lotus-pubchem-oregano/0002-mesh-ids/{input_filename}'
        io.json_write(output_filepath, input_item)
        # break
        # quit()

# oregano_disease_ids__mesh_disease_ids()
# quit()

def mesh_disease_ids__mesh_disease_names():
    input_folderpath = f'{g.SSOT_FOLDERPATH}/wikidata-powo-lotus-pubchem-oregano/0002-mesh-ids'
    input_filenames = sorted(os.listdir(input_folderpath))
    for i, input_filename in enumerate(input_filenames[:]):
        print(f'{i}/{len(input_filenames)}')
        input_filepath = f'{input_folderpath}/{input_filename}'
        input_item = io.json_read(input_filepath)
        for lotus_plant_component in input_item['lotus_plant_components']:
            lotus_plant_component['mesh_diseases'] = []
            mesh_diseases_ids = lotus_plant_component['mesh_diseases_ids']
            print(mesh_diseases_ids)
            if mesh_diseases_ids != []:
                for mesh_disease_id in mesh_diseases_ids:
                    mesh_filepath = f'{g.SSOT_FOLDERPATH}/mesh/0000-ids-jsons/{mesh_disease_id}.json'
                    try: mesh_data = io.json_read(mesh_filepath)
                    except: mesh_data = {}
                    if mesh_data != {}:
                        label = mesh_data['label']
                        if label['@language'] == 'en':
                            value = label['@value']
                        else:
                            value = ''
                        if value != '':
                            lotus_plant_component['mesh_diseases'].append({
                                'mesh_disease_id': mesh_disease_id,
                                'mesh_disease_name': value,
                            })
                            print(json.dumps(mesh_data, indent=4))
                            print(mesh_data['label'])
                            # break
                            # quit()
        # print(json.dumps(input_item, indent=4))
        # quit()
        output_filepath = f'{g.SSOT_FOLDERPATH}/wikidata-powo-lotus-pubchem-oregano/0003-mesh-names/{input_filename}'
        io.json_write(output_filepath, input_item)
        # quit()

# mesh_disease_ids__mesh_disease_names()
# quit()

def wikidata_powo_lotu_pubchem_oregano__preview_diseases_names():
    input_folderpath = f'{g.SSOT_FOLDERPATH}/wikidata-powo-lotus-pubchem-oregano/0003-mesh-names'
    input_filenames = sorted(os.listdir(input_folderpath))
    for i, input_filename in enumerate(input_filenames[:]):
        print(f'{i}/{len(input_filenames)}')
        input_filepath = f'{input_folderpath}/{input_filename}'
        input_item = io.json_read(input_filepath)
        for lotus_plant_component in input_item['lotus_plant_components']:
            mesh_diseases = lotus_plant_component['mesh_diseases']
            if mesh_diseases != []:
                print(mesh_diseases)
                quit()

quit()

# wikidata_powo_lotus_pubchem_oregano__compounds_ids__diseases_ids_merge()
# quit()

'''
def oregano_compound_id_to_targets_ids():
    oregano_text = io.file_read(f'{g.SSOT_FOLDERPATH}/oregano/oregano-master/Data_OREGANO/Graphs/OREGANO_V3_WIW.tsv')
    oregano_lines = oregano_text.split('\n')
    triples_failed = []
    s_types = []
    triples = []
    for oregano_line_i, oregano_line in enumerate(oregano_lines):
        print(f'{oregano_line_i}/{len(oregano_lines)}')
        try: chunk_1, chunk_2, chunk_3 = oregano_line.split('\t')
        except:
            triples_failed.append(oregano_line)
            continue
        s_type = chunk_1.split(':')[0]
        if s_type not in s_types:
            s_types.append(s_type)
        # print(chunk_2)
        # print(chunk_1, '->', chunk_2, '->', chunk_3)
        if chunk_1 == 'NATURAL_COMPOUND:22707':
            triple = [chunk_1, chunk_2, chunk_3]
            if triple not in triples:
                triples.append(triple)
            print(triples)
            # quit()
    for triple in triples:
        print(triple)
    print(len(triples))
    quit()
'''

'''
def oregano_natural_compound_relationships_triples_get():
    oregano_text = io.file_read(f'{g.SSOT_FOLDERPATH}/oregano/oregano-master/Data_OREGANO/Graphs/OREGANO_V3.tsv')
    oregano_lines = oregano_text.split('\n')
    triples_failed = []
    s_types = []
    triples = []
    for oregano_line_i, oregano_line in enumerate(oregano_lines):
        print(f'{oregano_line_i}/{len(oregano_lines)}')
        try: chunk_1, chunk_2, chunk_3 = oregano_line.split('\t')
        except:
            triples_failed.append(oregano_line)
            continue
        s_type = chunk_1.split(':')[0]
        if s_type not in s_types:
            s_types.append(s_type)
        # if chunk_1 == 'NATURAL_COMPOUND:22707':
        if chunk_1 == 'GENE:16036':
            triple = [chunk_1, chunk_2, chunk_3]
            if triple not in triples:
                triples.append(triple)
            print(triples)
            # quit()
    for triple in triples:
        print(triple)
    print(len(triples))
    quit()
'''

def oregano__diseases_get():
    oregano_target_lines = io.file_read(
        f'{g.SSOT_FOLDERPATH}/oregano/oregano-master/Integration/Integration V3/GESTION_ID/DISEASES.tsv'
    ).split('\n')
    ###
    headings = oregano_target_lines[0].split('\t')
    field_mesh_failed_count = 0
    output_items = []
    for heading in headings:
        # print(heading)
        headings[0] = 'ID'
        cids = []
        for line_i, line in enumerate(oregano_target_lines[:]):
            print(f'{line_i}/{len(oregano_target_lines)}')
            if line_i == 0: continue
            if line.strip() == '': continue
            values = line.split('\t')
            item = {}
            for i in range(len(headings)):
                item[headings[i]] = values[i].strip()
            # print(json.dumps(item, indent=4))
            # quit()
            if 'MESH' not in item or item['MESH'].strip() == '':
                field_mesh_failed_count = 0
            else:
                output_items.append(item)
            # if line_i > 5:
                # quit()
    # print(field_mesh_failed_count)
    return output_items

def oregano__neo4j__diseases_by_compound():
    driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "Newoliark1"))
    query = """
        MATCH (c:Entity {type: "COMPOUND", id: $compound_id})
        MATCH (c)-[*1..6]-(d:Entity {type: "DISEASE"})
        RETURN DISTINCT d.id AS disease_id
    """
    query = """
        MATCH (c:Entity {type: "NATURAL_COMPOUND", id: $compound_id})
        MATCH (c)-[*1..6]-(d:Entity {type: "DISEASE"})
        RETURN DISTINCT d.id AS disease_id
    """
    query = """
        MATCH p=(s:Entity {type: "NATURAL_COMPOUND", id: $compound_id})
                -[:is_substance_that_treats]->
                (o) 
        RETURN o.id as id
    """
    with driver.session() as session:
        result = session.run(query, compound_id="NATURAL_COMPOUND:1095")
        diseases = [record['id'] for record in result]
    print(diseases)
    driver.close()

# oregano__neo4j__diseases_by_compound()
# quit()

def mesh__jsons_get():
    '''
    mesh_filepath = f'{g.SSOT_FOLDERPATH}/mesh/mesh.nt'
    mesh_content = io.file_read(mesh_filepath)
    mesh_lines = mesh_content.split('\n')
    for line in mesh_lines[:100]:
        print(line)
    from rdflib import Graph, URIRef, RDFS
    graph = Graph()
    graph.parse(mesh_filepath, format="nt")
    def get_mesh_name(mesh_id):
        uri = URIRef(f"http://id.nlm.nih.gov/mesh/{mesh_id}")
        for _, _, label in g.triples((uri, RDFS.label, None)):
            return str(label)
        return None
    print(get_mesh_name("D054868"))
    '''
    oregano_diseases = oregano__diseases_get()
    mesh_ids = []
    for oregano_disease in oregano_diseases:
        mesh_id = oregano_disease['MESH']
        # if mesh_id not in mesh_ids:
        mesh_id_chunks = mesh_id.split(';')
        # mesh_id_chunk = mesh_id.split(';')[0]
        # mesh_ids.append(mesh_id_chunk)
        for mesh_id_chunk in mesh_id_chunks:
            mesh_ids.append(mesh_id_chunk)
    print(len(mesh_ids))
    mesh_ids = sorted(list(set(mesh_ids)))
    print(len(mesh_ids))
    # quit()
    # for i, mesh_id in enumerate(mesh_ids):
        # print(mesh_id)
        # if i > 10000:
            # quit()
    # quit()
    '''
    mesh_ids = [item['MESH'] for item in oregano_diseases]
    mesh_ids = sorted(list(set(mesh_ids)))
    print(mesh_ids[:100])
    quit()
    '''

    session = requests.Session()
    for mesh_id_i, mesh_id in enumerate(mesh_ids[7000:]):
        print(f'{mesh_id_i}/{len(mesh_ids)}')
        output_filepath = f'{g.SSOT_FOLDERPATH}/mesh/0000-ids-jsons/{mesh_id}.json'
        try: 
            print(mesh_id)
            if 'OMIM' in mesh_id: continue
            output_data = io.json_read(output_filepath)
            if output_data == {}: os.remove(output_filepath)
        except:
            pass
        if not os.path.exists(output_filepath):
            url = f"https://id.nlm.nih.gov/mesh/{mesh_id}.json"
            print(url)
            data = {}
            for attempt in range(5):
                try:
                    r = requests.get(url, timeout=10)
                    if r.status_code == 200:
                        data =  r.json()
                        break
                except requests.exceptions.RequestException:
                    print('failed')
                    pass
                time.sleep(2 * (attempt + 1))  # exponential backoff
            if data != {}:
                io.json_write(output_filepath, data)
            if mesh_id_i % 100 == 0 and mesh_id_i != 0:
                time.sleep(60)
        # if mesh_id_i > 5:
            # quit()
    quit()

# mesh__jsons_get()
# oregano__diseases_get()

# start = time.perf_counter()
# oregano__kg_create__batch_grouped()
# end = time.perf_counter()
# print(f"Execution time: {end - start:.6f} seconds")

# oregano_natural_compound_relationships_triples_get()
quit()

# oregano_text = io.file_read(f'{g.SSOT_FOLDERPATH}/oregano/oregano-master/Data_OREGANO/Graphs/OREGANO_V3_WIW.tsv')
oregano_text = io.file_read(f'{g.SSOT_FOLDERPATH}/oregano/oregano-master/Data_OREGANO/Graphs/OREGANO_V3.tsv')
oregano_lines = oregano_text.split('\n')
triples = []
relationships = []
entities = []
for oregano_line_i, oregano_line in enumerate(oregano_lines[:50]):
    # print(f'{oregano_line_i}/{len(oregano_lines)}')
    try: chunk_1, chunk_2, chunk_3 = oregano_line.split('\t')
    except: continue
    # if chunk_1.split(':')[0].lower().strip() == 'natural_compound':
        # if chunk_2 not in relationships:
    relationships.append(chunk_2)
    triple = [chunk_1, chunk_2, chunk_3]
    print(oregano_line)
    triples.append(triple)
    # quit()

print(len(triples))
quit()
'''
['NATURAL_COMPOUND:16168', 'rdf/type', 'COMPOUND']
['NATURAL_COMPOUND:16168', 'has_target', 'PROTEIN:358']
['NATURAL_COMPOUND:99', 'has_code', 'G02AC01']
['NATURAL_COMPOUND:1515', 'interacts_with', 'COMPOUND:1']
['NATURAL_COMPOUND:982', 'is_affecting', 'GENE:746']
['NATURAL_COMPOUND:1015', 'is_substance_that_treats', 'DISEASE:2631']
['NATURAL_COMPOUND:569', 'has_indication', 'INDICATION:1']
['NATURAL_COMPOUND:569', 'has_side_effect', 'SIDE_EFFECT:1']
'''

'''
natural compound, type, compound
natural compound, has target, protein
natural compound, is affecting, gene
natural compound, has indication, indication
natural compound, has side effect, side effect

compound, downregulates, gene
compound, upregulatges, gene
compound, is substance that treats, disease
compound, has code, *code
compound, interacts with, compound

protein, involved in, bioprocess
protein, gene product of, gene

reaction, part of, bioprocess
reaction, reaction of, pathway

gene, causes condition, disease
gene, acts within, pathway

disease, has phenotype, phenotype

pathway, participates in, pathway
'''

# for triple in triples:
    # print(triple)
quit()

# oregano_compound_id_to_targets_ids()

oregano_target_lines = io.file_read(
    f'{g.SSOT_FOLDERPATH}/oregano/oregano-master/Integration/Integration V3/GESTION_ID/TARGET.tsv'
).split('\n')
###
headings = oregano_target_lines[0].split('\t')
for heading in headings:
    # print(heading)
    headings[0] = 'TARGET_ID'
    cids = []
    for line_i, line in enumerate(oregano_target_lines[:]):
        print(line_i)
        if line_i == 0: continue
        if line.strip() == '': continue
        values = line.split('\t')
        item = {}
        for i in range(len(headings)):
            item[headings[i]] = values[i].strip()
        if item['TARGET_ID'] == 'PROTEIN:1519':
            print(json.dumps(item, indent=4))
            # TODO: resolve protein name with UNIPROTKB id
            quit()

# TODO: investigate oregano dataset (relationships chain)
quit()

# oregano_items = io.csv_to_dict(f'{g.SSOT_FOLDERPATH}/oregano/oregano-master/Data_OREGANO/Graphs/OREGANO_V3.tsv', delimiter='\t')

print('#########################################3')
for s_type in s_types:
    print(s_type)

quit()
quit()

################################################################################
# KNOWLEDGE GRAPH
################################################################################
def kg_jsons__create():
    input_folderpath = f'{g.SSOT_FOLDERPATH}/wikidata-powo/0000-ids'
    for i, input_filename in enumerate(sorted(os.listdir(input_folderpath))):
        i_str = ''
        if i < 10: i_str = f'00000{i}'
        elif i < 100: i_str = f'0000{i}'
        elif i < 1000: i_str = f'000{i}'
        elif i < 10000: i_str = f'00{i}'
        elif i < 100000: i_str = f'0{i}'
        elif i < 1000000: i_str = f'{i}'
        output_filepath = f'{g.SSOT_FOLDERPATH}/kg/jsons/{i_str}.json'
        if not os.path.exists(output_filepath):
            input_filepath = f'{input_folderpath}/{input_filename}'
            input_data = io.json_read(input_filepath)
            output_data = {'terra_id': i_str, **input_data}
            io.json_write(output_filepath, output_data)
        # quit()

# kg_jsons__create()
quit()

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

quit()

def pubchem_properties_from_cids(cids):
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

def pubchem_properties_batches_to_single():
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

# herbs_wcvp = data.herbs_wcvp_get()
# for herb in herbs_wcvp[:100]:
    # print(herb['family'])
    # print(herb)


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

def plants_taxon():
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

# entities_relationships_distribution()


def triples_gen():
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

