import os
import json
import random

from lib import g
from lib import io
from lib import llm
from lib import data
from lib import polish

herbs_num = 40000

def medicine_poison_inert_get(tmp_filepath):
    tmp_data = io.json_read(tmp_filepath)
    try: tmp_medicine_poison_inert = tmp_data['medicine_poison_inert'] 
    except: return None
    score_medicine = 0
    score_inert = 0
    score_poison = 0
    for item in tmp_medicine_poison_inert:
        if item['answer'] == 'medicine':
            score_medicine = item['total_score']
        if item['answer'] == 'inert':
            score_inert = item['total_score']
        if item['answer'] == 'poison':
            score_poison = item['total_score']
    if score_medicine > score_inert and score_medicine > score_poison:
        _obj = {
            'answer': 'medicine',
            'total_score': score_medicine,
        }
        return _obj
    elif score_inert > score_medicine and score_inert > score_poison:
        _obj = {
            'answer': 'inert',
            'total_score': score_inert,
        }
        return _obj
    else:
        _obj = {
            'answer': 'poison',
            'total_score': score_poison,
        }
        return _obj

def answer_score_extract(json_data):
    _objs = []
    for item in json_data:
        try: answer = item['answer']
        except: continue
        try: score = item['score']
        except: continue
        _objs.append({
            "answer": answer, 
            "score": score,
        })
    return _objs

def total_score_calc(outputs):
    outputs_final = []
    for output in outputs:
        outputs_final.append({
            'answer': output['answer'],
            'mentions': int(output['mentions']),
            'confidence_score': int(output['confidence_score']),
            'total_score': int(output['mentions']) * int(output['confidence_score']),
        })
    outputs_final = sorted(outputs_final, key=lambda x: x['total_score'], reverse=True)
    print('***********************')
    print('***********************')
    print('***********************')
    for output in outputs_final:
        print(output)
    print('***********************')
    print('***********************')
    print('***********************')
    return outputs_final

def herb_medicine_or_poison_gen(entity_herb_filepath, regen=False, clear=False):
    entity_herb = io.json_read(entity_herb_filepath)
    herb_name_scientific = entity_herb['herb_name_scientific']
    key = 'medicine_or_poison'
    if key not in entity_herb: entity_herb[key] = ''
    if regen: entity_herb[key] = ''
    if clear: 
        entity_herb[key] = ''
        io.json_write(entity_herb_filepath, entity_herb)
        return
    if entity_herb[key] == '':
        outputs = []
        for i in range(10):
            print(f'{i} - {herb_name_scientific}')
            prompt = f'''
                Tell me if the following herb is considered medicinal, poisonous, or inert: {herb_name_scientific}.
                Also, tell give a confidence score from 1 to 10, indicating how sure you are about your answer.
                Reply in the following JSON format: 
                [
                    {{"answer": <write "medicine", "poison", or "inert" here>, "score": 8}} 
                ]
                Only reply with the JSON, don't add additional info.
                Don't include notes, reply ONLY with the JSON.
                /no_think
            '''
            reply = llm.reply(prompt)
            if '</think>' in reply:
                reply = reply.split('</think>')[1].strip()
            json_data = {}
            try: json_data = json.loads(reply)
            except: pass 
            if json_data != {}:
                _objs = answer_score_extract(json_data)
                for _obj in _objs:
                    answer = _obj['answer']
                    score = _obj['score']
                    found = False
                    for output in outputs:
                        if answer in output['answer']: 
                            output['mentions'] += 1
                            output['confidence_score'] += int(score)
                            found = True
                            break
                    if not found:
                        outputs.append({
                            'answer': answer, 
                            'mentions': 1, 
                            'confidence_score': int(score), 
                        })
        outputs = total_score_calc(outputs)
        entity_herb[key] = outputs
        print(entity_herb_filepath)
        io.json_write(entity_herb_filepath, entity_herb)

def herb_benefits_ai(entity_herb_filepath, regen=False, clear=False):
    entity_herb = io.json_read(entity_herb_filepath)
    herb_name_scientific = entity_herb['herb_name_scientific']
    key = 'herb_benefits'
    if key not in entity_herb: entity_herb[key] = ''
    if regen: entity_herb[key] = ''
    if clear: 
        entity_herb[key] = ''
        io.json_write(entity_herb_filepath, entity_herb)
        return
    if entity_herb[key] == '' or entity_herb[key] == []:
        outputs = []
        prompt = f'''
            Write a list of the 10 best health benefits of the plant {herb_name_scientific}.
            Each benefit must be less than 4 words.
            Each benefit must start with an action verb.
            Also write a confidence score from 1 to 10, indicating how sure you are about your answer.
            Reply using the following JSON format:
            [
                {{"answer": "write benefit 1 here", "score": "write score 1 here"}},
                {{"answer": "write benefit 2 here", "score": "write score 2 here"}},
                {{"answer": "write benefit 3 here", "score": "write score 3 here"}},
                {{"answer": "write benefit 4 here", "score": "write score 4 here"}},
                {{"answer": "write benefit 5 here", "score": "write score 5 here"}},
                {{"answer": "write benefit 6 here", "score": "write score 6 here"}},
                {{"answer": "write benefit 7 here", "score": "write score 7 here"}},
                {{"answer": "write benefit 8 here", "score": "write score 8 here"}},
                {{"answer": "write benefit 9 here", "score": "write score 9 here"}},
                {{"answer": "write benefit 10 here", "score": "write score 10 here"}}
            ]
            Reply only with the JSON.
        '''
        prompt += f'/no_think'
        reply = llm.reply(prompt)
        if '</think>' in reply:
            reply = reply.split('</think>')[1].strip()
        json_data = {}
        try: json_data = json.loads(reply)
        except: pass 
        if json_data != {}:
            _objs = answer_score_extract(json_data)
            for _obj in _objs:
                answer = _obj['answer']
                score = _obj['score']
                found = False
                for output in outputs:
                    if answer in output['answer']: 
                        output['mentions'] += 1
                        output['confidence_score'] += int(score)
                        found = True
                        break
                if not found:
                    outputs.append({
                        'answer': answer, 
                        'mentions': 1, 
                        'confidence_score': int(score), 
                    })
        outputs = total_score_calc(outputs)
        entity_herb[key] = outputs
        print(entity_herb_filepath)
        io.json_write(entity_herb_filepath, entity_herb)

new_actions_candidates = []
def herb_therapeutic_actions_ai(entity_herb_filepath, regen=False, clear=False):
    global new_actions_candidates
    entity_herb = io.json_read(entity_herb_filepath)
    herb_name_scientific = entity_herb['herb_name_scientific']
    key = 'herb_therapeutic_actions'
    if key not in entity_herb: entity_herb[key] = ''
    if regen: entity_herb[key] = ''
    if clear: 
        entity_herb[key] = ''
        io.json_write(entity_herb_filepath, entity_herb)
        return
    if entity_herb[key] == '' or entity_herb[key] == []:
        outputs = []
        list_random_num = random.randint(7, 13)
        with open(f'{g.database_folderpath}/categories/herbs/therapeutic-actions.txt') as f: 
            therapeutic_actions_prompt = f.read().lower()
        therapeutic_actions_list = [line.strip() for line in therapeutic_actions_prompt.split('\n') if line.strip() != '']
        therapeutic_actions_list_clipped = therapeutic_actions_list[:list_random_num]
        prompt_json_list = []
        for i, _ in enumerate(therapeutic_actions_list_clipped):
            prompt_json_list.append(f'''{{"answer": "write name of therapeutic action {i+1} here", "score": "write score {i+1} here"}}''')
        prompt_json_list = ',\n'.join(prompt_json_list)
        random.shuffle(therapeutic_actions_list_clipped)
        prompt_json_list_examples = ', '.join(therapeutic_actions_list_clipped[:3])
        prompt = f'''
            For each of the following therapeutic actions, write a confidence score from 1 to 10 indicating how much the plant {herb_name_scientific} has each therapeutic action.
            {therapeutic_actions_prompt}
            Reply using the following JSON format:
            [
                {prompt_json_list}
            ]
            Reply only with the JSON.
        '''
        prompt = f'''
            Write a list of about {list_random_num} therapeutic actions of the plant {herb_name_scientific}.
            For reference, by therapeutic actions I mean things like: {prompt_json_list_examples}.
            Reply using the following JSON format:
            [
                {prompt_json_list}
            ]
            Reply only with the JSON.
        '''
        prompt += f'/no_think'
        print(prompt)
        reply = llm.reply(prompt)
        if '</think>' in reply:
            reply = reply.split('</think>')[1].strip()
        json_data = {}
        try: json_data = json.loads(reply)
        except: pass 
        if json_data != {}:
            _objs = answer_score_extract(json_data)
            for _obj in _objs:
                answer = _obj['answer'].lower().strip()
                score = int(float(_obj['score']))
                if answer not in therapeutic_actions_list: 
                    if answer not in new_actions_candidates:
                        new_actions_candidates.append(answer)
                    print(therapeutic_actions_list)
                    print(f'''
                        ##########################################################
                        NOT FOUND: {answer}
                        ##########################################################
                    ''')
                    continue
                found = False
                for output in outputs:
                    if answer in output['answer']: 
                        output['mentions'] += 1
                        output['confidence_score'] += int(score)
                        found = True
                        break
                if not found:
                    outputs.append({
                        'answer': answer, 
                        'mentions': 1, 
                        'confidence_score': int(score), 
                    })
        outputs = total_score_calc(outputs)
        entity_herb[key] = outputs
        print(entity_herb_filepath)
        io.json_write(entity_herb_filepath, entity_herb)
        # quit()
        for x in new_actions_candidates:
            print(x)

def herb_names_common_gen(entity_herb_filepath, regen=False, clear=False):
    entity_herb = io.json_read(entity_herb_filepath)
    herb_name_scientific = entity_herb['herb_name_scientific']
    key = 'herb_names_common'
    if key not in entity_herb: entity_herb[key] = ''
    if regen: entity_herb[key] = ''
    if clear: 
        entity_herb[key] = ''
        io.json_write(entity_herb_filepath, entity_herb)
        return
    if entity_herb[key] == '' or entity_herb[key] == []:
        outputs = []
        for i in range(10):
            print(f'{i} - {herb_name_scientific}')
            prompt = f'''
                Write a list of the most well known and popular common names for the following plant with scientific name: {herb_name_scientific}.
                Also write a confidence score from 1 to 10, indicating how sure you are about your answer.
                Reply using the following JSON format:
                [
                    {{"answer": "write common name 1 here", "score": "write score 1 here"}},
                    {{"answer": "write common name 2 here", "score": "write score 2 here"}},
                    {{"answer": "write common name 3 here", "score": "write score 3 here"}}
                ]
                Reply only with the JSON.
            '''
            prompt += f'/no_think'
            reply = llm.reply(prompt)
            if '</think>' in reply:
                reply = reply.split('</think>')[1].strip()
            json_data = {}
            try: json_data = json.loads(reply)
            except: pass 
            if json_data != {}:
                _objs = answer_score_extract(json_data)
                for _obj in _objs:
                    answer = _obj['answer']
                    score = _obj['score']
                    found = False
                    for output in outputs:
                        if answer in output['answer']: 
                            output['mentions'] += 1
                            output['confidence_score'] += int(score)
                            found = True
                            break
                    if not found:
                        outputs.append({
                            'answer': answer, 
                            'mentions': 1, 
                            'confidence_score': int(score), 
                        })
        outputs = total_score_calc(outputs)
        entity_herb[key] = outputs
        print(entity_herb_filepath)
        io.json_write(entity_herb_filepath, entity_herb)

def herb_family_ai(entity_herb_filepath, regen=False, clear=False):
    entity_herb = io.json_read(entity_herb_filepath)
    herb_name_scientific = entity_herb['herb_name_scientific']
    key = 'family'
    if key not in entity_herb: entity_herb[key] = ''
    if regen: entity_herb[key] = ''
    if clear: 
        entity_herb[key] = ''
        io.json_write(entity_herb_filepath, entity_herb)
        return
    if entity_herb[key] == '':
        outputs = []
        for i in range(10):
            print(f'{i} - {herb_name_scientific}')
            prompt = f'''
                Write the family name of the following plant based on linnaean taxonomy system: {herb_name_scientific}.
                Also, tell give a confidence score from 1 to 10, indicating how sure you are about your answer.
                Reply in the following JSON format: 
                [
                    {{"answer": "write family name here", "score": "write confidence score here 1-10"}} 
                ]
                Only reply with the JSON, don't add additional info.
                Don't include notes, reply ONLY with the JSON.
                /no_think
            '''
            reply = llm.reply(prompt)
            if '</think>' in reply:
                reply = reply.split('</think>')[1].strip()
            json_data = {}
            try: json_data = json.loads(reply)
            except: pass 
            if json_data != {}:
                _objs = answer_score_extract(json_data)
                for _obj in _objs:
                    answer = _obj['answer']
                    score = int(_obj['score'])
                    found = False
                    for output in outputs:
                        if answer in output['answer']: 
                            output['mentions'] += 1
                            output['confidence_score'] += int(score)
                            found = True
                            break
                    if not found:
                        outputs.append({
                            'answer': answer, 
                            'mentions': 1, 
                            'confidence_score': int(score), 
                        })
        outputs = total_score_calc(outputs)
        entity_herb[key] = outputs
        print(entity_herb_filepath)
        io.json_write(entity_herb_filepath, entity_herb)

def herb_native_regions_ai(entity_herb_filepath, regen=False, clear=False):
    entity_herb = io.json_read(entity_herb_filepath)
    herb_name_scientific = entity_herb['herb_name_scientific']
    key = 'native_regions'
    if key not in entity_herb: entity_herb[key] = ''
    if regen: entity_herb[key] = ''
    if clear: 
        entity_herb[key] = ''
        io.json_write(entity_herb_filepath, entity_herb)
        return
    if entity_herb[key] == '':
        outputs = []
        for i in range(1):
            rand_num = random.randint(7, 13)
            prompt_json_list = []
            for i in range(rand_num):
                prompt_json_list.append(
                    f'''{{"answer": f"write native region name {i} here", "score": "write confidence score here 1-10"}}'''
                )
            prompt_json_list = ',\n'.join(prompt_json_list)
            print(f'{i} - {herb_name_scientific}')
            prompt = f'''
                Write a list of {rand_num} the native regions of the following plant: {herb_name_scientific}.
                Also, tell give a confidence score from 1 to 10, indicating how sure you are about your answer.
                Reply in the following JSON format: 
                [
                    {prompt_json_list}
                ]
                Only reply with the JSON, don't add additional info.
                Don't include notes, reply ONLY with the JSON.
                /no_think
            '''
            reply = llm.reply(prompt)
            if '</think>' in reply:
                reply = reply.split('</think>')[1].strip()
            json_data = {}
            try: json_data = json.loads(reply)
            except: pass 
            if json_data != {}:
                _objs = answer_score_extract(json_data)
                for _obj in _objs:
                    answer = _obj['answer']
                    score = int(_obj['score'])
                    found = False
                    for output in outputs:
                        if answer in output['answer']: 
                            output['mentions'] += 1
                            output['confidence_score'] += int(score)
                            found = True
                            break
                    if not found:
                        outputs.append({
                            'answer': answer, 
                            'mentions': 1, 
                            'confidence_score': int(score), 
                        })
        outputs = total_score_calc(outputs)
        entity_herb[key] = outputs
        print(entity_herb_filepath)
        io.json_write(entity_herb_filepath, entity_herb)

def herb_origin_continents_gen(entity_herb_filepath, regen=False, clear=False):
    entity_herb = io.json_read(entity_herb_filepath)
    herb_name_scientific = entity_herb['herb_name_scientific']
    key = 'herb_origin_continents'
    if key not in entity_herb: entity_herb[key] = ''
    if regen: entity_herb[key] = ''
    if clear: 
        entity_herb[key] = ''
        io.json_write(entity_herb_filepath, entity_herb)
        return
    if entity_herb[key] == '' or entity_herb[key] == []:
        outputs = []
        for i in range(10):
            print(f'{i} - {herb_name_scientific}')
            prompt = f'''
                Tell me the continents of origin of the the following plant with scientific name: {herb_name_scientific}.
                In specific, write a confidence score from 1 to 10, indicating how sure you are about your answer.
                The possible continents are 7: Africa, Antarctica, Asia, Europe, North America, South America, Australia.
                Reply using the following JSON format:
                [
                    {{"answer": "write origin continent name 1 here", "score": "write score 1 here"}},
                    {{"answer": "write origin continent name 2 here", "score": "write score 2 here"}},
                    {{"answer": "write origin continent name 3 here", "score": "write score 3 here"}}
                ]
                Reply only with the JSON.
            '''
            prompt += f'/no_think'
            reply = llm.reply(prompt)
            if '</think>' in reply:
                reply = reply.split('</think>')[1].strip()
            json_data = {}
            try: json_data = json.loads(reply)
            except: pass 
            if json_data != {}:
                _objs = answer_score_extract(json_data)
                for _obj in _objs:
                    answer = _obj['answer'].strip().lower()
                    score = int(_obj['score'])
                    found = False
                    for output in outputs:
                        if answer in output['answer']: 
                            output['mentions'] += 1
                            output['confidence_score'] += int(score)
                            found = True
                            break
                    if not found:
                        outputs.append({
                            'answer': answer, 
                            'mentions': 1, 
                            'confidence_score': int(score), 
                        })
        outputs = total_score_calc(outputs)
        entity_herb[key] = outputs
        print(entity_herb_filepath)
        io.json_write(entity_herb_filepath, entity_herb)
        # print(entity_herb)
        # quit()

def json_gen(herb):
    entities_herbs_folderpath = f'{g.DATABASE_FOLDERPATH}/entities/herbs'
    try: os.mkdir(entities_herbs_folderpath)
    except: pass
    ###
    herb_name_scientific = herb['herb_name_scientific']
    try: herb_slug = herb['herb_slug']
    except: herb_slug = polish.sluggify(herb_name_scientific)
    ###
    entity_herb_filepath = f'''{entities_herbs_folderpath}/{herb_slug}.json'''
    entity_herb = io.json_read(entity_herb_filepath, create=True)
    entity_herb['herb_slug'] = herb_slug
    entity_herb['herb_name_scientific'] = herb_name_scientific
    try: entity_herb['herb_family'] = herb['herb_family']
    except: pass
    io.json_write(entity_herb_filepath, entity_herb)
    ###
    herb_name_common_gen(entity_herb_filepath, regen=False, clear=False)
    # herb_medicine_or_poison_gen(entity_herb_filepath, regen=False, clear=False)
    # herb_family_ai(entity_herb_filepath, regen=False, clear=False)
    # herb_native_regions_ai(entity_herb_filepath, regen=False, clear=False)
    # herb_benefits_ai(entity_herb_filepath, regen=False, clear=False)
    # herb_therapeutic_actions_ai(entity_herb_filepath, regen=False, clear=False)

    # herb_origin_continents_gen(entity_herb_filepath, regen=False, clear=False)

def herbs_wcvp_medicinal_json(herb):
    herbs_folderpath = f'{g.SSOT_FOLDERPATH}/herbs/herbs-wcvp/medicinal'
    try: os.mkdir(herbs_folderpath)
    except: pass
    ###
    herb_name_scientific = herb['herb_name_scientific']
    try: herb_slug = herb['herb_slug']
    except: herb_slug = polish.sluggify(herb_name_scientific)
    try: herb_family = herb['herb_family']
    except: herb_family = ''
    ###
    herb_filepath = f'''{herbs_folderpath}/{herb_slug}.json'''
    herb_data = io.json_read(herb_filepath, create=True)
    herb_data['herb_slug'] = herb_slug
    herb_data['herb_name_scientific'] = herb_name_scientific
    try: herb_data['herb_family'] = herb_family
    except: pass
    io.json_write(herb_filepath, herb_data)
    ###
    herb_names_common_gen(herb_filepath, regen=False, clear=False)
    herb_origin_continents_gen(herb_filepath, regen=False, clear=False)

def herbs_wcvp_medicinal_gen():
    herbs = [
        io.json_read(f'{g.PLANT_MEDICINE_FOLDERPATH}/{filename}')
        for filename in os.listdir(f'{g.PLANT_MEDICINE_FOLDERPATH}')
    ][:herbs_num]
    for herb_i, herb in enumerate(herbs):
        print('####################################')
        print(f'{herb_i}/{len(herbs)} - {herb}')
        print('####################################')
        herbs_wcvp_medicinal_json(herb)
        # break
    print(len(herbs))

def herbs_primary_json(herb):
    herbs_folderpath = f'{g.SSOT_FOLDERPATH}/herbs/herbs-primary'
    try: os.mkdir(herbs_folderpath)
    except: pass
    ###
    herb_name_scientific = herb['herb_name_scientific']
    try: herb_slug = herb['herb_slug']
    except: herb_slug = polish.sluggify(herb_name_scientific)
    try: herb_family = herb['herb_family']
    except: herb_family = ''
    ###
    herb_filepath = f'''{herbs_folderpath}/{herb_slug}.json'''
    herb_data = io.json_read(herb_filepath, create=True)
    herb_data['herb_slug'] = herb_slug
    herb_data['herb_name_scientific'] = herb_name_scientific
    herb_data['herb_family'] = herb_family
    io.json_write(herb_filepath, herb_data)
    ###
    herb_names_common_gen(herb_filepath, regen=False, clear=False)
    herb_origin_continents_gen(herb_filepath, regen=False, clear=False)
    herb_medicine_or_poison_gen(herb_filepath, regen=False, clear=False)
    # herb_family_ai(entity_herb_filepath, regen=False, clear=False)
    # herb_native_regions_ai(entity_herb_filepath, regen=False, clear=False)
    # herb_benefits_ai(entity_herb_filepath, regen=False, clear=False)
    # herb_therapeutic_actions_ai(entity_herb_filepath, regen=False, clear=False)


def herbs_primary_gen():
    herbs = data.herbs_primary_get()
    for herb_i, herb in enumerate(herbs):
        print('####################################')
        print(f'{herb_i}/{len(herbs)} - {herb}')
        herbs_primary_json(herb)
        print('####################################')
        print()
        print()
        print()

def main():
    herbs_primary_gen()
    herbs_wcvp_medicinal_gen()
    if 0:
        herbs = data.herbs_popular_get('teas', 100)
        for herb_i, herb in enumerate(herbs):
            print('####################################')
            print(f'{herb_i}/{len(herbs)} - {herb}')
            json_gen(herb)
            print('####################################')
            print()
            print()
            print()
