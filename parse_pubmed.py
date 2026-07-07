import os
import time
import shutil

from lib import g
from lib import io
from lib import llm


model_filepath = '/home/ubuntu/vault-tmp/llm/gemma-4-12b-it-Q4_K_S.gguf'
model_filepath = '/home/ubuntu/vault-tmp/llm/gemma-4-26B-A4B-it-UD-Q4_K_XL.gguf'

### TODO: extract plant names exactly as they are. 
###       do coreference in a separate step by reusing the source text context

def observations_extract_raw():
    input_folderpath = f'{g.VAULT_FOLDERPATH}/terrawhisper/data/fetch/pubmed/medicinal_plant/abstracts'
    output_folderpath = f'{g.VAULT_FOLDERPATH}/terrawhisper/data/parse/pubmed/chemicals/raw'
    # try: shutil.rmtree(output_folderpath)
    # except: pass
    # os.makedirs(output_folderpath, exist_ok=True)
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
            From the scientific study ABSTRACT below, extract all the relationships (observations) between plant name, plant part, and chemical.
            Write each observation using this format: [plant name, plant part part, chemical name]
            RULES:
            Always write the names of the plants in latin binomial scientific name, no common names or abbreviated names.
            Always write the names of the chemicals of the herbs exactly how you find them in the text.
            If the plant part name is NOT mentioned in the relationship, fill it with null.
            Only reply with the relationships requested.
            If you can't find any of these relationships, reply with "NONE".
            ABSTRACT:
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

def observations_activities_extract_raw():
    input_folderpath = f'{g.VAULT_FOLDERPATH}/terrawhisper/data/fetch/pubmed/medicinal_plant/abstracts'
    output_folderpath = f'{g.VAULT_FOLDERPATH}/terrawhisper/data/parse/pubmed/activities/raw'
    io.folders_recursive_gen(output_folderpath)
    # try: shutil.rmtree(output_folderpath)
    # except: pass
    # os.makedirs(output_folderpath, exist_ok=True)
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
            From the scientific study ABSTRACT below, extract all the relationships (observations) between plant name and biological activity.
            Write each observation using this format: [plant name, biological activity]
            RULES:
            Always write the names of the plants in latin binomial scientific name, no common names or abbreviated names.
            Always write the names of the biological activities of the herbs exactly how you find them in the text. By biological activities I mean things like Adaptogen, Adrenalytic, Anti-inflammatory, etc.
            Only reply with the relationships requested.
            If you can't find any of these relationships, reply with "NONE".
            ABSTRACT:
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

def observations_activities_raw_to_json():
    input_folderpath = f'{g.VAULT_FOLDERPATH}/terrawhisper/data/parse/pubmed/activities/raw'
    output_folderpath = f'{g.VAULT_FOLDERPATH}/terrawhisper/data/parse/pubmed/activities/json'
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
        study_folderpath = f'{g.VAULT_FOLDERPATH}/terrawhisper/studies/pubmed/medicinal-plant/json'
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
            try: plant_name, activity_name = line
            except: continue
            output_item = {
                f'plant_name': plant_name,
                f'activity_name': activity_name,
                f'source_id': input_filename.split('.')[0],
                f'journal_title': journal_title,
            }
            output_items.append(output_item)
        io.json_write(output_filepath, output_items)

def observations_diseases_raw_to_json():
    entity_type = 'diseases'
    source_name = 'pubmed'
    input_foldername = f'parse'
    output_foldername = f'parse'
    input_folderpath = f'{g.VAULT_FOLDERPATH}/terrawhisper/data/{input_foldername}/{source_name}/{entity_type}/raw'
    output_folderpath = f'{g.VAULT_FOLDERPATH}/terrawhisper/data/{output_foldername}/{source_name}/{entity_type}/json'
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
        study_folderpath = f'{g.VAULT_FOLDERPATH}/terrawhisper/studies/pubmed/medicinal-plant/json'
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
            try: plant_name, disease_name = line
            except: continue
            output_item = {
                f'plant_name': plant_name,
                f'disease_name': disease_name,
                f'source_id': input_filename.split('.')[0],
                f'journal_title': journal_title,
            }
            output_items.append(output_item)
        io.json_write(output_filepath, output_items)

def observations_diseases_extract_raw():
    output_foldername = 'diseases'
    input_folderpath = f'{g.VAULT_FOLDERPATH}/terrawhisper/data/fetch/pubmed/medicinal_plant/abstracts'
    output_folderpath = f'{g.VAULT_FOLDERPATH}/terrawhisper/data/parse/pubmed/{output_foldername}/raw'
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
            From the scientific study ABSTRACT below, extract all the relationships (observations) between plant name and treated disease name.
            Write each observation using this format: [plant name, disease name]
            RULES:
            Always write the names of the plants in latin binomial scientific name, no common names or abbreviated names.
            Always write the names of the diseases exactly how you find them in the text. By disease health diseases I mean I want to extract all health conditions, disorders, symptoms, syndromes, ailments, and health issues that the plant is claimed to treat, relieve, prevent, manage, or improve.
            Only reply with the relationships requested.
            If you can't find any of these relationships, reply with "NONE".
            ABSTRACT:
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

def observations_raw_to_json():
    input_folderpath = f'{g.VAULT_FOLDERPATH}/terrawhisper/data/parse/pubmed/chemicals/raw'
    output_folderpath = f'{g.VAULT_FOLDERPATH}/terrawhisper/data/parse/pubmed/chemicals/json'
    try: shutil.rmtree(output_folderpath)
    except: pass
    os.makedirs(output_folderpath, exist_ok=True)
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
        study_folderpath = f'{g.VAULT_FOLDERPATH}/terrawhisper/studies/pubmed/medicinal-plant/json'
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
            try: plant_name, plant_part_name, chemical_name = line
            except: continue
            output_item = {
                f'plant_name': plant_name,
                f'plant_part_name': plant_part_name,
                f'chemical_name': chemical_name,
                f'source_id': input_filename.split('.')[0],
                f'journal_title': journal_title,
            }
            output_items.append(output_item)
        io.json_write(output_filepath, output_items)
    '''
    for output_item in output_items:
        print(output_item)
    print(len(output_items))
    io.json_write(output_filepath, output_items)
    '''

def run():
    print('parse >> pubmed')

    start = time.perf_counter()
    # observations_extract_raw() ### WARNING: takes many many hours (nightly running)
    # observations_raw_to_json()
    print(f'observations() - execution time: ', time.perf_counter() - start)

    start = time.perf_counter()
    # observations_activities_extract_raw() ### WARNING: takes many many hours (nightly running)
    # observations_activities_raw_to_json()
    print(f'observations_activities() - execution time: ', time.perf_counter() - start)

    start = time.perf_counter()
    # observations_diseases_raw_to_json()
    print(f'observations_diseases() - execution time: ', time.perf_counter() - start)

    start = time.perf_counter()
    # observations_diseases_extract_raw() ### WARNING: takes many many hours (nightly running)
    print(f'observations_diseases() - execution time: ', time.perf_counter() - start)

