import os
import json
import random

from lib import g
from lib import io
from lib import llm
from lib import data
from lib import polish

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

def herb_medicine_or_poison_ai(entity_herb_filepath, regen=False, clear=False):
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

def herb_therapeutic_actions_ai(entity_herb_filepath, regen=False, clear=False):
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
        with open(f'{g.database_folderpath}/categories/herbs/therapeutic-actions.txt') as f: 
            therapeutic_actions_prompt = f.read().lower()
        therapeutic_actions_list = [line.strip() for line in therapeutic_actions_prompt.split('\n') if line.strip() != '']
        prompt_json_list = []
        for i, item in enumerate(therapeutic_actions_list):
            prompt_json_list.append(f'''{{"answer": "write name of therapeutic action {i+1} here", "score": "write score {i+1} here"}}''')
        prompt_json_list = ',\n'.join(prompt_json_list)
        prompt = f'''
            For each of the following therapeutic actions, write a confidence score from 1 to 10 indicating how much the plant {herb_name_scientific} has each therapeutic action.
            {therapeutic_actions_prompt}
            Reply using the following JSON format:
            [
                {prompt_json_list}
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
                if answer not in therapeutic_actions_list: 
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

def json_gen(entity_herb_filepath):
    herb_benefits_ai(entity_herb_filepath, regen=False, clear=False)
    herb_therapeutic_actions_ai(entity_herb_filepath, regen=True, clear=False)

def gen():
    entities_herbs_folderpath = f'{g.database_folderpath}/entities/herbs'
    try: os.mkdir(entities_herbs_folderpath)
    except: pass
    ###
    # herb_list = io.csv_to_dict(f'{g.database_folderpath}/csv/herbs.csv')
    herb_list = data.herbs_get()
    herb_medicinal_list = []
    for herb_i, herb in enumerate(herb_list):
        print('####################################')
        print(f'{herb_i}/{len(herb_list)} - {herb}')
        herb_name_scientific = herb['herb_name_scientific']
        if 'herb_name_common' in herb: herb_name_common = herb['herb_name_common']
        else: herb_name_common = ''
        herb_slug = polish.sluggify(herb_name_scientific)
        entity_herb_filepath = f'{entities_herbs_folderpath}/{herb_slug}.json'
        print(entity_herb_filepath)
        entity_herb = io.json_read(entity_herb_filepath, create=True)
        entity_herb['herb_slug'] = herb_slug
        entity_herb['herb_name_scientific'] = herb_name_scientific
        entity_herb['herb_name_common'] = herb_name_common
        io.json_write(entity_herb_filepath, entity_herb)
        herb_medicine_or_poison_ai(entity_herb_filepath, regen=False, clear=False)
        herb_medicinal_list.append(herb)
        ###
        json_gen(entity_herb_filepath)
        # quit()
        print('####################################')
        print()
        print()
        print()
    print(len(herb_medicinal_list))
    # quit()

