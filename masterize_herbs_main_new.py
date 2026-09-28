import os
import re
import json
import time
import shutil
import sqlite3
import unicodedata

from lib import g
from lib import io
from lib import llm

import resolve_utils

HUB_FOLDERPATH = f'''{g.DATA_FOLDERPATH}/herbs'''

def plants_extract_raw():
    input_folderpath = f'{HUB_FOLDERPATH}/fetch/pubmed/medicinal_plant/abstracts'
    output_folderpath = f'{HUB_FOLDERPATH}/parse/pubmed/plants_names/raw'
    io.folders_recursive_gen(output_folderpath)
    # try: shutil.rmtree(output_folderpath)
    # except: pass
    os.makedirs(output_folderpath, exist_ok=True)
    ###
    relationships_found = []
    input_filenames = os.listdir(input_folderpath)
    i = 0
    for input_filename in input_filenames[i:]:
        i += 1
        print(f'{i}/{len(input_filenames)}')
        output_filepath = f'{output_folderpath}/{input_filename}'
        if os.path.exists(output_filepath): continue
        input_filepath = f'{input_folderpath}/{input_filename}'
        input_data = io.json_read(input_filepath)
        try: article_data = input_data['PubmedArticle'][0]['MedlineCitation']['Article']
        except: pass
        try: input_title = article_data['ArticleTitle']
        except: input_title = ''
        try: input_abstract = ' '.join(article_data['Abstract']['AbstractText'])
        except: continue
        # print(json.dumps(input_title, indent=4))
        # print(input_title)
        # print(input_abstract)
        # quit()
        content_to_extract = f'{input_title} {input_abstract}'
        prompt = f'''
            From the SCIENTIFIC STUDY below, extract all the plants names mentioned.
            RULES:
            Write one plant name per new line.
            Plants names include scientific names, common names, abbreviations, and any other type variation.
            Always write the names of the plants names exactly how you find them in the text.
            Only reply with the content requested.
            If you can't find what requested, reply with "NONE".
            SCIENTIFIC STUDY:            
            {content_to_extract}
        '''.strip()
        prompt = prompt.replace('<text>', content_to_extract)
        reply = llm.reply(prompt, model_filepath, max_tokens=512)
        if '</think>' in reply:
            reply = reply.split('</think>')[1].strip()
        print('################################################################################')
        print(reply)
        print('########################################')
        # print(prompt)
        print('################################################################################')
        if 'NONE'.strip() not in reply.strip():
            relationships_found.append(reply)
            output_data = {
                'title': input_title,
                'abstract': input_abstract,
                'reply': reply,
            }
            io.json_write(
                output_filepath,
                output_data,
            )
        # if i > 10:
            # quit()
    print(len(relationships_found))
    # quit()

def plants_string_match():
    input_folderpath = f'{HUB_FOLDERPATH}/parse/pubmed/plants_names/raw'
    output_folderpath = f'{HUB_FOLDERPATH}/parse/pubmed/plants_names/string_match'
    try: shutil.rmtree(output_folderpath)
    except: pass
    io.folders_recursive_gen(output_folderpath)
    ###
    input_filenames = os.listdir(input_folderpath)
    for i, input_filename in enumerate(input_filenames[:]):
        print(f'{i}/{len(input_filenames)}')
        input_filepath = f'{input_folderpath}/{input_filename}'
        output_filepath = f'{output_folderpath}/{input_filename}'
        ###
        input_data = io.json_read(input_filepath)
        lines = [line.strip() for line in input_data['reply'].split('\n') if line.strip() != '']
        lines_match = []
        for line in lines:
            if line in input_data['title'] or line in input_data['abstract']:
                lines_match.append(line)
        # print(json.dumps(input_data, indent=4))
        # print(lines_match)
        # quit()
        output_data = input_data
        output_data['strings_match'] = lines_match
        io.json_write(output_filepath, output_data)
        # print(json.dumps(output_data, indent=4))
        # quit()
    print(json.dumps(output_data, indent=4))
    # quit()

def plants_resolve_local_llm():
    input_folderpath = f'{HUB_FOLDERPATH}/parse/pubmed/plants_names/string_match'
    output_folderpath = f'{HUB_FOLDERPATH}/parse/pubmed/plants_names/resolve_local'
    # try: shutil.rmtree(output_folderpath)
    # except: pass
    io.folders_recursive_gen(output_folderpath)
    ###
    input_filenames = os.listdir(input_folderpath)
    for i, input_filename in enumerate(input_filenames[:]):
        print(f'{i}/{len(input_filenames)}')
        input_filepath = f'{input_folderpath}/{input_filename}'
        output_filepath = f'{output_folderpath}/{input_filename}'
        if os.path.exists(output_filepath): continue
        ###
        input_data = io.json_read(input_filepath)
        output_data = input_data
        output_data['resolve_local'] = []
        for string_match in input_data['strings_match']:
            prompt = f'''
                Give me the full latin name of the following plant name: {string_match}.
                By full latin name I mean the scientific name that is usually in binomial nomenclature, no abbreviation or author attribution.
                On the opposite, keep variations, subspecies, etc if included in the provided plant name.
                If the plant name is already in it's canonical form, keep it.
                Reply only with the asked content, meaning the full latin name.
                For context, this plant name comes from the following scientific study abstract:
                {input_data['title']} {input_data['abstract']}
            '''.strip()
            reply = llm.reply(prompt, model_filepath, max_tokens=512)
            if '</think>' in reply:
                reply = reply.split('</think>')[1].strip()
            print()
            print('################################################################################')
            print(string_match, '->', reply)
            print('################################################################################')
            print()
            output_data['resolve_local'].append({
                'string_match': string_match,
                'resolved_local': reply,
            })
        io.json_write(output_filepath, output_data)
        # print(json.dumps(output_data, indent=4))
        # quit()

def parse_plants_json():
    input_folderpath = f'{HUB_FOLDERPATH}/parse/pubmed/plants_names/resolve_local'
    output_folderpath = f'{HUB_FOLDERPATH}/parse/pubmed/plants_names/json'
    try: shutil.rmtree(output_folderpath)
    except: pass
    io.folders_recursive_gen(output_folderpath)
    input_filenames = os.listdir(input_folderpath)
    ###
    for i, input_filename in enumerate(input_filenames[:]):
        print(f'{i}/{len(input_filenames)}')
        input_filepath = f'{input_folderpath}/{input_filename}'
        input_data = io.json_read(input_filepath)
        # print(json.dumps(input_data, indent=4))
        # quit()
        output_filepath = f'{output_folderpath}/{input_filename}'
        output_items = []
        for item in input_data['resolve_local']:
            resolve_local_text = item['resolved_local']
            # print(item)
            # quit()
            output_item = {
                'plant_name_scientific_resolve_local': resolve_local_text,
            }
            output_items.append(output_item)
        io.json_write(output_filepath, output_items)

def raw_to_json(foldername, entity_1, entity_2):
    input_folderpath = f'{HUB_FOLDERPATH}/parse/pubmed/{foldername}/raw'
    output_folderpath = f'{HUB_FOLDERPATH}/parse/pubmed/{foldername}/json'
    try: shutil.rmtree(output_folderpath)
    except: pass
    io.folders_recursive_gen(output_folderpath)
    ###
    input_filenames = os.listdir(input_folderpath)
    for i, input_filename in enumerate(input_filenames[:]):
        print(f'{i}/{len(input_filenames)}')
        input_filepath = f'{input_folderpath}/{input_filename}'
        output_filepath = f'{output_folderpath}/{input_filename}'
        ###
        input_data = io.json_read(input_filepath)
        # print(json.dumps(input_data, indent=4))
        relationships_text = input_data['reply']
        relationships_lines = []
        for line in relationships_text.split('\n'):
            line = line.strip()
            if line == '': continue
            if line.startswith('['): line = line[1:]
            if line.endswith(','): line = line[:-1]
            if line.endswith(']'): line = line[:-1]
            chunks = [chunk.strip() for chunk in line.split(', ')]
            relationships_lines.append(chunks)
        # print(len(relationships_lines))
        # study_folderpath = f'{g.VAULT_FOLDERPATH}/terrawhisper/studies/pubmed/medicinal-plant/json'
        study_folderpath = f'{HUB_FOLDERPATH}/fetch/pubmed/medicinal_plant/abstracts'
        study_filepath = f'{study_folderpath}/{input_filename}'
        study_data = io.json_read(study_filepath)
        try: article_data = study_data['PubmedArticle'][0]['MedlineCitation']['Article']
        except: pass
        try: journal_title = article_data['Journal']['Title']
        except: pass
        # print(json.dumps(article_data, indent=4))
        # print(json.dumps(journal_title, indent=4))
        ###
        output_items = []
        for line in relationships_lines:
            # print(line)
            try: entity_1_val, relationship, entity_2_val = line
            except: continue
            output_item = {
                entity_1: entity_1_val,
                f'relationship': relationship,
                entity_2: entity_2_val,
                'source_name': 'pubmed',
                'source_acronym': 'PM',
                f'source_id': input_filename.split('.')[0],
                f'journal_title': journal_title,
            }
            output_items.append(output_item)
        io.json_write(output_filepath, output_items)

def normalize_plant_name(name):
    # Common botanical author abbreviations (extend over time)
    AUTHOR_PATTERNS = [
        r"\bL\.\b",
        r"\bLinn\.\b",
        r"\bDC\.\b",
        r"\bHook\.?\s*f?\.?\b",
        r"\bBenth\.\b",
        r"\bWilld\.\b",
        r"\bMill\.\b",
        r"\bLam\.\b",
        r"\bRoxb\.\b",
    ]
    AUTHOR_REGEX = re.compile("|".join(AUTHOR_PATTERNS), re.IGNORECASE)
    if not name:
        return ""
    # Unicode normalization
    name = unicodedata.normalize("NFKC", name)
    # lowercase
    name = name.lower()
    # normalize hybrid sign
    name = name.replace("×", " x ")
    # remove botanical author citations
    name = AUTHOR_REGEX.sub("", name)
    # remove punctuation except letters, numbers and spaces
    name = re.sub(r"[.,;:()\[\]{}]", " ", name)
    # collapse whitespace
    name = re.sub(r"\s+", " ", name).strip()
    return name

def normalize_plants_names():
    input_folderpath = f'{HUB_FOLDERPATH}/parse/pubmed/plants_names/json'
    output_folderpath = f'{HUB_FOLDERPATH}/normalize/pubmed/plants_names/json'
    try: shutil.rmtree(output_folderpath)
    except: pass
    io.folders_recursive_gen(output_folderpath)
    input_filenames = os.listdir(input_folderpath)
    ###
    for i, input_filename in enumerate(input_filenames[:]):
        print(f'{i}/{len(input_filenames)}')
        input_filepath = f'{input_folderpath}/{input_filename}'
        input_data = io.json_read(input_filepath)
        # print(json.dumps(input_data, indent=4))
        # quit()
        ###
        output_filepath = f'{output_folderpath}/{input_filename}'
        if os.path.exists(output_filepath): continue
        ###
        for input_item in input_data:
            input_item['plant_name_scientific_normalize'] = normalize_plant_name(input_item['plant_name_scientific_resolve_local'])
            # print(json.dumps(normalized_item, indent=4))
            # quit()
        io.json_write(output_filepath, input_data)
    print(json.dumps(input_data[0], indent=4))
    # quit()

def resolve_plants_names():
    input_folderpath = f'{HUB_FOLDERPATH}/normalize/pubmed/plants_names/json'
    output_folderpath = f'{HUB_FOLDERPATH}/resolve/pubmed/plants_names/json'
    try: shutil.rmtree(output_folderpath)
    except: pass
    io.folders_recursive_gen(output_folderpath)
    ###
    wcvp_folderpath = f'{HUB_FOLDERPATH}/reference/wcvp/wcvp.db'
    wcvp_conn = sqlite3.connect(wcvp_folderpath)
    wcvp_conn.row_factory = sqlite3.Row
    ###
    input_filenames = os.listdir(input_folderpath)
    for i, input_filename in enumerate(input_filenames[:]):
        print(f'HERBS_RESOLVE {i}/{len(input_filenames)}')
        input_filepath = f'{input_folderpath}/{input_filename}'
        input_data = io.json_read(input_filepath)
        # print(json.dumps(input_data, indent=4))
        # quit()
        ###
        output_filepath = f'{output_folderpath}/{input_filename}'
        if os.path.exists(output_filepath): continue
        ###
        resolved_data = []
        for input_item in input_data:
            ### RESOLVE PLANT NAME (WCVP)
            wcvp_row = resolve_utils.resolve_plant_accepted(wcvp_conn, input_item['plant_name_scientific_normalize'])
            if wcvp_row:
                wcvp_item = dict(wcvp_row)
                # print(wcvp_item)
                input_item['plant_name_scientific_reference'] = wcvp_row['taxon_name']
                input_item['plant_name_scientific_reference_normalize'] = wcvp_row['taxon_name_normalized']
                resolved_data.append(input_item)
                # print(json.dumps(resolved_data, indent=4))
                # quit()
        if resolved_data != []:
            io.json_write(output_filepath, resolved_data)
    wcvp_conn.close()
    print(json.dumps(resolved_data[0], indent=4))
    # quit()

def masterize_plants_init(regen=False):
    table_name = 'plants'
    output_folderpath = f'{HUB_FOLDERPATH}/masterize'
    db_filepath = f'{output_folderpath}/master.db'
    ###
    os.makedirs(output_folderpath, exist_ok=True)
    conn = sqlite3.connect(db_filepath)
    cur = conn.cursor()
    if regen:
        cur.execute(f"DROP TABLE IF EXISTS {table_name}")
    cur.execute(f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            id INTEGER PRIMARY KEY,
            plant_name_scientific_reference TEXT NOT NULL UNIQUE,
            plant_name_scientific_reference_normalize TEXT NOT NULL UNIQUE
        );
    """)
    conn.execute("PRAGMA journal_mode = WAL;")
    conn.execute("PRAGMA synchronous = OFF;")
    conn.execute("PRAGMA temp_store = MEMORY;")
    ###
    cur.execute(f"CREATE INDEX IF NOT EXISTS idx_{table_name}_name_scientific_reference ON {table_name}(plant_name_scientific_reference)")
    cur.execute(f"CREATE INDEX IF NOT EXISTS idx_{table_name}_name_scientific_reference_normalize ON {table_name}(plant_name_scientific_reference_normalize)")
    conn.commit()
    conn.close()

def masterize_plants_add():
    table_name = 'plants'
    input_folderpath = f'{HUB_FOLDERPATH}/resolve/pubmed/plants_names/json'
    output_folderpath = f'{HUB_FOLDERPATH}/masterize'
    db_filepath = f'{output_folderpath}/master.db'
    ###
    input_filenames = os.listdir(input_folderpath)
    all_data = []
    for i, input_filename in enumerate(input_filenames[:]):
        print(f'PLANTS - {i}/{len(input_filenames)}')
        input_filepath = f'{input_folderpath}/{input_filename}'
        input_data = io.json_read(input_filepath)
        for input_item in input_data:
            all_data.append(input_item)
            # print(json.dumps(input_item, indent=4))
            # quit()
    # print(json.dumps(all_data[0], indent=4))
    # quit()
    ###
    conn = sqlite3.connect(db_filepath)
    cur = conn.cursor()
    cur.executemany(
        f"""
            INSERT OR IGNORE INTO {table_name} (
                plant_name_scientific_reference, 
                plant_name_scientific_reference_normalize
            )
            VALUES (?, ?)
        """,
        [
            (
                item.get("plant_name_scientific_reference"),
                item.get("plant_name_scientific_reference_normalize"),
            )
            for item in all_data
        ]
    )
    conn.commit()
    rows = conn.execute(f"SELECT * FROM {table_name}")
    for row in list(rows)[:10]:
        print(row)
        i += 1
    rows = conn.execute(f"SELECT * FROM {table_name}")
    print(len(list(rows)))
    conn.close()


def run():
    if 0:
        start = time.perf_counter()
        # plants_extract_raw() ### WARNING: takes many many hours (nightly running)
        # plants_string_match()
        # plants_resolve_local_llm() ### WARNING: takes many many hours (nightly running)
        parse_plants_json()
        print(f'parse plants() - execution time: ', time.perf_counter() - start)
 
    if 0:
        start = time.perf_counter()
        normalize_plants_names()
        print(f'normalize plants names() - execution time: ', time.perf_counter() - start)

    if 0:
        start = time.perf_counter()
        resolve_plants_names()
        print(f'resolve plants names() - execution time: ', time.perf_counter() - start)

    if 0:
        start = time.perf_counter()
        masterize_plants_init(regen=True)
        masterize_plants_add()
        print(f'masterize plants names() - execution time: ', time.perf_counter() - start)

