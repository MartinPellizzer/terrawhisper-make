import os
import json
import random

from lib import g
from lib import io
from lib import llm
from lib import data
from lib import polish

herbs_wcvp = None

herbs_num = 140000

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
    key = 'herb_family'
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

def herb_parts_gen(entity_herb_filepath, regen=False, clear=False):
    entity_herb = io.json_read(entity_herb_filepath)
    herb_name_scientific = entity_herb['herb_name_scientific']
    key = 'herb_parts'
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
                Tell me the medicinal plant parts used of the following plant with scientific name: {herb_name_scientific}.
                In specific, write a confidence score from 1 to 10, indicating how sure you are about your answer.
                The possible plant parts used are the following:
                    Leaves
                    Stems
                    Shoots
                    Roots
                    Rhizomes
                    Tubers
                    Bulbs
                    Corms
                    Flowers
                    Seeds
                    Fruits
                    Cones
                    Bark
                    Wood
                    Resin
                    Oleoresin
                    Gum
                    Balsam
                    Latex
                    Sap
                    Pollen
                    Spores
                Reply using the following JSON format:
                [
                    {{"answer": "write plant part name 1 here", "score": "write score 1 here"}},
                    {{"answer": "write plant part name 2 here", "score": "write score 2 here"}},
                    {{"answer": "write plant part name 3 here", "score": "write score 3 here"}}
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

def herb_traditional_systems_gen(herb_filepath, regen=False, clear=False):
    entity_herb = io.json_read(herb_filepath)
    herb_name_scientific = entity_herb['herb_name_scientific']
    key = 'herb_traditional_systems'
    if key not in entity_herb: entity_herb[key] = ''
    if regen: entity_herb[key] = ''
    if clear: 
        entity_herb[key] = ''
        io.json_write(herb_filepath, entity_herb)
        return
    if entity_herb[key] == '' or entity_herb[key] == []:
        main_list_text = f'''
                European Herbal Medicine
                Ayurvedic Medicine
                Traditional Chinese Medicine
                Unani Medicine
                Native American Herbal Medicine
                African Traditional Medicine
                Japanese Kampo Medicine
                Tibetan Medicine
                Mediterranean Herbal Traditions
                Korean Traditional Medicine
            '''.strip()
        outputs = []
        for i in range(10):
            print(f'{i} - {herb_name_scientific}')
            import textwrap
            main_list_prompt = [e.strip() for e in main_list_text.split('\n') if e.strip() != '']
            random.shuffle(main_list_prompt)
            main_list_prompt = '\n'.join(main_list_prompt)
            prompt = textwrap.dedent(f''' 
                Tell me the traditional systems that used the following plant with scientific name: {herb_name_scientific}.
                In specific, write a confidence score from 1 to 10, indicating how sure you are about your answer.
                The possible traditional systems are the following:
                {main_list_prompt}
                Reply using the following JSON format:
                [
                    {{"answer": "write traditional system name 1 here", "score": "write score 1 here"}},
                    {{"answer": "write traditional system name 2 here", "score": "write score 2 here"}},
                    {{"answer": "write traditional system name 3 here", "score": "write score 3 here"}},
                    {{"answer": "write traditional system name 4 here", "score": "write score 4 here"}},
                    {{"answer": "write traditional system name 5 here", "score": "write score 5 here"}},
                    {{"answer": "write traditional system name 6 here", "score": "write score 6 here"}},
                    {{"answer": "write traditional system name 7 here", "score": "write score 7 here"}},
                    {{"answer": "write traditional system name 8 here", "score": "write score 8 here"}},
                    {{"answer": "write traditional system name 9 here", "score": "write score 9 here"}},
                    {{"answer": "write traditional system name 10 here", "score": "write score 10 here"}}
                ]
                Reply only with the JSON.
            ''').strip()
            prompt += f'\n/no_think'
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
        print(herb_filepath)
        io.json_write(herb_filepath, entity_herb)
        # print(entity_herb)
        # quit()

def herb_historical_preparations_gen(herb_filepath, regen=False, clear=False):
    entity_herb = io.json_read(herb_filepath)
    herb_name_scientific = entity_herb['herb_name_scientific']
    key = 'herb_historical_preparations'
    if key not in entity_herb: entity_herb[key] = ''
    if regen: entity_herb[key] = ''
    if clear: 
        entity_herb[key] = ''
        io.json_write(herb_filepath, entity_herb)
        return
    if entity_herb[key] == '' or entity_herb[key] == []:
        main_list_text = f'''
                Infusion
                Decoction
                Tincture
                Poultice
                Oil infusion
                Ointment
                Syrup
                Powder
                Herbal bath
                Culinary use
            '''.strip()
        outputs = []
        for i in range(10):
            print(f'{i} - {herb_name_scientific}')
            import textwrap
            main_list_prompt = [e.strip() for e in main_list_text.split('\n') if e.strip() != '']
            random.shuffle(main_list_prompt)
            main_list_prompt = '\n'.join(main_list_prompt)
            prompt = textwrap.dedent(f''' 
                Tell me the most used historical preparation methods of the following plant with scientific name: {herb_name_scientific}.
                In specific, write a confidence score from 1 to 10, indicating how sure you are about your answer.
                The possible historical preparation methods are the following:
                {main_list_prompt}
                Reply using the following JSON format:
                [
                    {{"answer": "write historical preparation method name 1 here", "score": "write score 1 here"}},
                    {{"answer": "write historical preparation method name 2 here", "score": "write score 2 here"}},
                    {{"answer": "write historical preparation method name 3 here", "score": "write score 3 here"}},
                    {{"answer": "write historical preparation method name 4 here", "score": "write score 4 here"}},
                    {{"answer": "write historical preparation method name 5 here", "score": "write score 5 here"}},
                    {{"answer": "write historical preparation method name 6 here", "score": "write score 6 here"}},
                    {{"answer": "write historical preparation method name 7 here", "score": "write score 7 here"}},
                    {{"answer": "write historical preparation method name 8 here", "score": "write score 8 here"}},
                    {{"answer": "write historical preparation method name 9 here", "score": "write score 9 here"}},
                    {{"answer": "write historical preparation method name 10 here", "score": "write score 10 here"}}
                ]
                Reply only with the JSON.
            ''').strip()
            prompt += f'\n/no_think'
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
        print(herb_filepath)
        io.json_write(herb_filepath, entity_herb)
        # print(entity_herb)
        # quit()

def herb_medicinal_actions_gen(herb_filepath, regen=False, clear=False):
    entity_herb = io.json_read(herb_filepath)
    herb_name_scientific = entity_herb['herb_name_scientific']
    key = 'herb_medicinal_actions'
    if key not in entity_herb: entity_herb[key] = ''
    if regen: entity_herb[key] = ''
    if clear: 
        entity_herb[key] = ''
        io.json_write(herb_filepath, entity_herb)
        return
    if entity_herb[key] == '' or entity_herb[key] == []:
        main_list_text = f'''
            Carminative
            Sedative
            Anti-inflammatory
            Antispasmodic
            Astringent
            Diuretic
            Stimulant
            Expectorant
            Tonic
            Bitter
        '''.strip()
        outputs = []
        for i in range(10):
            print(f'{i} - {herb_name_scientific}')
            import textwrap
            main_list_prompt = [e.strip() for e in main_list_text.split('\n') if e.strip() != '']
            random.shuffle(main_list_prompt)
            main_list_prompt = '\n'.join(main_list_prompt)
            prompt = textwrap.dedent(f''' 
                Tell me the medicinal actions of the following plant with scientific name: {herb_name_scientific}.
                In specific, write a confidence score from 1 to 10, indicating how sure you are about your answer.
                The possible medicinal actions are the following:
                {main_list_prompt}
                Reply using the following JSON format:
                [
                    {{"answer": "write medicinal action name 1 here", "score": "write score 1 here"}},
                    {{"answer": "write medicinal action name 2 here", "score": "write score 2 here"}},
                    {{"answer": "write medicinal action name 3 here", "score": "write score 3 here"}},
                    {{"answer": "write medicinal action name 4 here", "score": "write score 4 here"}},
                    {{"answer": "write medicinal action name 5 here", "score": "write score 5 here"}},
                    {{"answer": "write medicinal action name 6 here", "score": "write score 6 here"}},
                    {{"answer": "write medicinal action name 7 here", "score": "write score 7 here"}},
                    {{"answer": "write medicinal action name 8 here", "score": "write score 8 here"}},
                    {{"answer": "write medicinal action name 9 here", "score": "write score 9 here"}},
                    {{"answer": "write medicinal action name 10 here", "score": "write score 10 here"}}
                ]
                Reply only with the JSON.
            ''').strip()
            prompt += f'\n/no_think'
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
        print(herb_filepath)
        io.json_write(herb_filepath, entity_herb)
        # print(entity_herb)
        # quit()

def herb_active_compounds_gen(herb_filepath, regen=False, clear=False):
    entity_herb = io.json_read(herb_filepath)
    herb_name_scientific = entity_herb['herb_name_scientific']
    key = 'herb_active_compounds'
    if key not in entity_herb: entity_herb[key] = ''
    if regen: entity_herb[key] = ''
    if clear: 
        entity_herb[key] = ''
        io.json_write(herb_filepath, entity_herb)
        return
    if entity_herb[key] == '' or entity_herb[key] == []:
        main_list_text = f'''
            Flavonoid
            Phenolic acid
            Tannin
            Terpenoid
            Alkaloid
            Saponin
            Essential oil
            Coumarin
            Anthocyanin
            Glycoside
        '''.strip()
        outputs = []
        for i in range(10):
            print(f'{i} - {herb_name_scientific}')
            import textwrap
            main_list_prompt = [e.strip() for e in main_list_text.split('\n') if e.strip() != '']
            random.shuffle(main_list_prompt)
            main_list_prompt = '\n'.join(main_list_prompt)
            prompt = textwrap.dedent(f''' 
                Tell me the medicinal actions of the following plant with scientific name: {herb_name_scientific}.
                In specific, write a confidence score from 1 to 10, indicating how sure you are about your answer.
                The possible medicinal actions are the following:
                {main_list_prompt}
                Reply using the following JSON format:
                [
                    {{"answer": "write medicinal action name 1 here", "score": "write score 1 here"}},
                    {{"answer": "write medicinal action name 2 here", "score": "write score 2 here"}},
                    {{"answer": "write medicinal action name 3 here", "score": "write score 3 here"}},
                    {{"answer": "write medicinal action name 4 here", "score": "write score 4 here"}},
                    {{"answer": "write medicinal action name 5 here", "score": "write score 5 here"}},
                    {{"answer": "write medicinal action name 6 here", "score": "write score 6 here"}},
                    {{"answer": "write medicinal action name 7 here", "score": "write score 7 here"}},
                    {{"answer": "write medicinal action name 8 here", "score": "write score 8 here"}},
                    {{"answer": "write medicinal action name 9 here", "score": "write score 9 here"}},
                    {{"answer": "write medicinal action name 10 here", "score": "write score 10 here"}}
                ]
                Reply only with the JSON.
            ''').strip()
            prompt += f'\n/no_think'
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
        print(herb_filepath)
        io.json_write(herb_filepath, entity_herb)
        # print(entity_herb)
        # quit()

def herb_drugs_interaction_gen(herb_filepath, regen=False, clear=False):
    entity_herb = io.json_read(herb_filepath)
    herb_name_scientific = entity_herb['herb_name_scientific']
    key = 'herb_drugs_interaction'
    if key not in entity_herb: entity_herb[key] = ''
    if regen: entity_herb[key] = ''
    if clear: 
        entity_herb[key] = ''
        io.json_write(herb_filepath, entity_herb)
        return
    if entity_herb[key] == '' or entity_herb[key] == []:
        outputs = []
        for i in range(10):
            print(f'{i} - {herb_name_scientific}')
            import textwrap
            prompt = textwrap.dedent(f''' 
                Tell me if the following plant with scientific name {herb_name_scientific} has known drug interactions.
                In specific, write a confidence score from 1 to 10, indicating how sure you are about your answer.
                The answers names are the following and I want the score for each:
                Yes
                No
                Unknown
                Reply using the following JSON format:
                [
                    {{"answer": "write answer name 1 here", "score": "write score 1 here"}},
                    {{"answer": "write answer name 2 here", "score": "write score 2 here"}},
                    {{"answer": "write answer name 3 here", "score": "write score 3 here"}}
                ]
                Reply only with the JSON.
                Reply only with one word.
            ''').strip()
            prompt += f'\n/no_think'
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
        print(herb_filepath)
        io.json_write(herb_filepath, entity_herb)
        # print(entity_herb)
        # quit()

def herb_allergies_gen(herb_filepath, regen=False, clear=False):
    entity_herb = io.json_read(herb_filepath)
    herb_name_scientific = entity_herb['herb_name_scientific']
    key = 'herb_allergies'
    if key not in entity_herb: entity_herb[key] = ''
    if regen: entity_herb[key] = ''
    if clear: 
        entity_herb[key] = ''
        io.json_write(herb_filepath, entity_herb)
        return
    if entity_herb[key] == '' or entity_herb[key] == []:
        outputs = []
        for i in range(10):
            print(f'{i} - {herb_name_scientific}')
            import textwrap
            prompt = textwrap.dedent(f''' 
                Tell me if the following plant with scientific name {herb_name_scientific} has known allergies.
                In specific, write a confidence score from 1 to 10, indicating how sure you are about your answer.
                The answers names are the following and I want the score for each:
                Yes
                No
                Unknown
                Reply using the following JSON format:
                [
                    {{"answer": "write answer name 1 here", "score": "write score 1 here"}},
                    {{"answer": "write answer name 2 here", "score": "write score 2 here"}},
                    {{"answer": "write answer name 3 here", "score": "write score 3 here"}}
                ]
                Reply only with the JSON.
                Reply only with one word.
            ''').strip()
            prompt += f'\n/no_think'
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
        print(herb_filepath)
        io.json_write(herb_filepath, entity_herb)
        # print(entity_herb)
        # quit()

def herb_toxicity_gen(herb_filepath, regen=False, clear=False):
    entity_herb = io.json_read(herb_filepath)
    herb_name_scientific = entity_herb['herb_name_scientific']
    key = 'herb_toxicity'
    if key not in entity_herb: entity_herb[key] = ''
    if regen: entity_herb[key] = ''
    if clear: 
        entity_herb[key] = ''
        io.json_write(herb_filepath, entity_herb)
        return
    if entity_herb[key] == '' or entity_herb[key] == []:
        outputs = []
        for i in range(10):
            print(f'{i} - {herb_name_scientific}')
            import textwrap
            prompt = textwrap.dedent(f''' 
                Tell me if the following plant with scientific name {herb_name_scientific} has known toxicity.
                In specific, write a confidence score from 1 to 10, indicating how sure you are about your answer.
                The answers names are the following and I want the score for each:
                Yes
                No
                Unknown
                Reply using the following JSON format:
                [
                    {{"answer": "write answer name 1 here", "score": "write score 1 here"}},
                    {{"answer": "write answer name 2 here", "score": "write score 2 here"}},
                    {{"answer": "write answer name 3 here", "score": "write score 3 here"}}
                ]
                Reply only with the JSON.
                Reply only with one word.
            ''').strip()
            prompt += f'\n/no_think'
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
        print(herb_filepath)
        io.json_write(herb_filepath, entity_herb)
        # print(entity_herb)
        # quit()

def herb_contraindications_gen(herb_filepath, regen=False, clear=False):
    entity_herb = io.json_read(herb_filepath)
    herb_name_scientific = entity_herb['herb_name_scientific']
    key = 'herb_contraindications'
    if key not in entity_herb: entity_herb[key] = ''
    if regen: entity_herb[key] = ''
    if clear: 
        entity_herb[key] = ''
        io.json_write(herb_filepath, entity_herb)
        return
    if entity_herb[key] == '' or entity_herb[key] == []:
        outputs = []
        for i in range(10):
            print(f'{i} - {herb_name_scientific}')
            import textwrap
            prompt = textwrap.dedent(f''' 
                Tell me if the following plant with scientific name {herb_name_scientific} has known contraindications.
                In specific, write a confidence score from 1 to 10, indicating how sure you are about your answer.
                The answers names are the following and I want the score for each:
                Yes
                No
                Unknown
                Reply using the following JSON format:
                [
                    {{"answer": "write answer name 1 here", "score": "write score 1 here"}},
                    {{"answer": "write answer name 2 here", "score": "write score 2 here"}},
                    {{"answer": "write answer name 3 here", "score": "write score 3 here"}}
                ]
                Reply only with the JSON.
                Reply only with one word.
            ''').strip()
            prompt += f'\n/no_think'
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
        print(herb_filepath)
        io.json_write(herb_filepath, entity_herb)
        # print(entity_herb)
        # quit()


def herb_pregnancy_and_breastfeeding_gen(herb_filepath, regen=False, clear=False):
    entity_herb = io.json_read(herb_filepath)
    herb_name_scientific = entity_herb['herb_name_scientific']
    key = 'herb_pregnancy_and_breastfeeding'
    if key not in entity_herb: entity_herb[key] = ''
    if regen: entity_herb[key] = ''
    if clear: 
        entity_herb[key] = ''
        io.json_write(herb_filepath, entity_herb)
        return
    if entity_herb[key] == '' or entity_herb[key] == []:
        outputs = []
        for i in range(10):
            print(f'{i} - {herb_name_scientific}')
            import textwrap
            prompt = textwrap.dedent(f''' 
                Tell me if the following plant with scientific name {herb_name_scientific} has known pregnancy and breastfeeding safety issues.
                In specific, write a confidence score from 1 to 10, indicating how sure you are about your answer.
                The answers names are the following and I want the score for each:
                Yes
                No
                Unknown
                Reply using the following JSON format:
                [
                    {{"answer": "write answer name 1 here", "score": "write score 1 here"}},
                    {{"answer": "write answer name 2 here", "score": "write score 2 here"}},
                    {{"answer": "write answer name 3 here", "score": "write score 3 here"}}
                ]
                Reply only with the JSON.
                Reply only with one word.
            ''').strip()
            prompt += f'\n/no_think'
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
        print(herb_filepath)
        io.json_write(herb_filepath, entity_herb)
        # print(entity_herb)
        # quit()

def herb_generally_safe_gen(herb_filepath, regen=False, clear=False):
    entity_herb = io.json_read(herb_filepath)
    herb_name_scientific = entity_herb['herb_name_scientific']
    key = 'herb_generally_safe'
    if key not in entity_herb: entity_herb[key] = ''
    if regen: entity_herb[key] = ''
    if clear: 
        entity_herb[key] = ''
        io.json_write(herb_filepath, entity_herb)
        return
    if entity_herb[key] == '' or entity_herb[key] == []:
        outputs = []
        for i in range(10):
            print(f'{i} - {herb_name_scientific}')
            import textwrap
            prompt = textwrap.dedent(f''' 
                Tell me if the following plant with scientific name {herb_name_scientific} is considered generally safe for medicinal use and preparations.
                In specific, write a confidence score from 1 to 10, indicating how sure you are about your answer.
                The answers names are the following and I want the score for each:
                Yes
                No
                Unknown
                Reply using the following JSON format:
                [
                    {{"answer": "write answer name 1 here", "score": "write score 1 here"}},
                    {{"answer": "write answer name 2 here", "score": "write score 2 here"}},
                    {{"answer": "write answer name 3 here", "score": "write score 3 here"}}
                ]
                Reply only with the JSON.
                Reply only with one word.
            ''').strip()
            prompt += f'\n/no_think'
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
        print(herb_filepath)
        io.json_write(herb_filepath, entity_herb)
        # print(entity_herb)
        # quit()

def herb_preparations_gen(herb_filepath, regen=False, clear=False):
    entity_herb = io.json_read(herb_filepath)
    herb_name_scientific = entity_herb['herb_name_scientific']
    key = 'herb_preparations'
    if key not in entity_herb: entity_herb[key] = ''
    if regen: entity_herb[key] = ''
    if clear: 
        entity_herb[key] = ''
        io.json_write(herb_filepath, entity_herb)
        return
    if entity_herb[key] == '' or entity_herb[key] == []:
        main_list_text = f'''
            Infusion
            Decoction
            Tincture
            Poultice
            Powder
            Capsule
            Essential Oil
            Extract
            Oil Infusion
            Culinary Use
            '''.strip()
        outputs = []
        for i in range(10):
            print(f'{i} - {herb_name_scientific}')
            import textwrap
            main_list_prompt = [e.strip() for e in main_list_text.split('\n') if e.strip() != '']
            random.shuffle(main_list_prompt)
            main_list_prompt = '\n'.join(main_list_prompt)
            prompt = textwrap.dedent(f''' 
                Tell me the most used preparation methods of the following plant with scientific name: {herb_name_scientific}.
                In specific, write a confidence score from 1 to 10, indicating how sure you are about your answer.
                The possible historical preparation methods are the following:
                {main_list_prompt}
                Reply using the following JSON format:
                [
                    {{"answer": "write historical preparation method name 1 here", "score": "write score 1 here"}},
                    {{"answer": "write historical preparation method name 2 here", "score": "write score 2 here"}},
                    {{"answer": "write historical preparation method name 3 here", "score": "write score 3 here"}},
                    {{"answer": "write historical preparation method name 4 here", "score": "write score 4 here"}},
                    {{"answer": "write historical preparation method name 5 here", "score": "write score 5 here"}},
                    {{"answer": "write historical preparation method name 6 here", "score": "write score 6 here"}},
                    {{"answer": "write historical preparation method name 7 here", "score": "write score 7 here"}},
                    {{"answer": "write historical preparation method name 8 here", "score": "write score 8 here"}},
                    {{"answer": "write historical preparation method name 9 here", "score": "write score 9 here"}},
                    {{"answer": "write historical preparation method name 10 here", "score": "write score 10 here"}}
                ]
                Reply only with the JSON.
            ''').strip()
            prompt += f'\n/no_think'
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
        print(herb_filepath)
        io.json_write(herb_filepath, entity_herb)
        # print(entity_herb)
        # quit()

def herb_growing_soil_gen(herb_filepath, regen=False, clear=False):
    entity_herb = io.json_read(herb_filepath)
    herb_name_scientific = entity_herb['herb_name_scientific']
    key = 'herb_growing_soil'
    if key not in entity_herb: entity_herb[key] = ''
    if regen: entity_herb[key] = ''
    if clear: 
        entity_herb[key] = ''
        io.json_write(herb_filepath, entity_herb)
        return
    if entity_herb[key] == '' or entity_herb[key] == []:
        main_list_text = f'''
            Sandy soil
            Silty soil
            Clay soil
            Loamy soil
            Sandy loam
            Silty loam
            Clay loam
            Rocky soil
            Gravelly soil
            Chalky soil
            Humus-rich soil
            Peaty soil
            Compact soil
            Light soil
            Heavy soil
        '''.strip()
        outputs = []
        for i in range(10):
            print(f'{i} - {herb_name_scientific}')
            import textwrap
            main_list_prompt = [e.strip() for e in main_list_text.split('\n') if e.strip() != '']
            random.shuffle(main_list_prompt)
            main_list_prompt = '\n'.join(main_list_prompt)
            prompt = textwrap.dedent(f''' 
                Tell me the best type of soil to grow the following plant with scientific name: {herb_name_scientific}.
                In specific, write a confidence score from 1 to 10, indicating how sure you are about your answer.
                The possible types of soil for you to pick from are the following:
                {main_list_prompt}
                Reply using the following JSON format:
                [
                    {{"answer": "write the type of soil name here", "score": "write score here"}}
                ]
                Reply only with the JSON.
            ''').strip()
            prompt += f'\n/no_think'
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
        print(herb_filepath)
        io.json_write(herb_filepath, entity_herb)
        # print(entity_herb)
        # quit()

def herb_growing_soil_drainage_gen(herb_filepath, regen=False, clear=False):
    entity_herb = io.json_read(herb_filepath)
    herb_name_scientific = entity_herb['herb_name_scientific']
    key = 'herb_growing_soil_drainage'
    if key not in entity_herb: entity_herb[key] = ''
    if regen: entity_herb[key] = ''
    if clear: 
        entity_herb[key] = ''
        io.json_write(herb_filepath, entity_herb)
        return
    if entity_herb[key] == '' or entity_herb[key] == []:
        main_list_text = f'''
            Well-drained conditions
            Moderately well-drained conditions
            Moderate drainage
            Poor drainage
            Freely draining soil
            Moist but well-drained soil
            Slow-draining soil
            Rapidly draining soil
        '''.strip()
        outputs = []
        for i in range(10):
            print(f'{i} - {herb_name_scientific}')
            import textwrap
            main_list_prompt = [e.strip() for e in main_list_text.split('\n') if e.strip() != '']
            random.shuffle(main_list_prompt)
            main_list_prompt = '\n'.join(main_list_prompt)
            prompt = textwrap.dedent(f''' 
                Tell me the best type of soil drainage to grow the following plant with scientific name: {herb_name_scientific}.
                In specific, write a confidence score from 1 to 10, indicating how sure you are about your answer.
                The possible types of soil drainage for you to pick from are the following:
                {main_list_prompt}
                Reply using the following JSON format:
                [
                    {{"answer": "write the type of soil drainage name here", "score": "write score here"}}
                ]
                Reply only with the JSON.
            ''').strip()
            prompt += f'\n/no_think'
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
        print(herb_filepath)
        io.json_write(herb_filepath, entity_herb)
        # print(entity_herb)
        # quit()

def herb_growing_soil_fertility_gen(herb_filepath, regen=False, clear=False):
    entity_herb = io.json_read(herb_filepath)
    herb_name_scientific = entity_herb['herb_name_scientific']
    key = 'herb_growing_soil_fertility'
    if key not in entity_herb: entity_herb[key] = ''
    if regen: entity_herb[key] = ''
    if clear: 
        entity_herb[key] = ''
        io.json_write(herb_filepath, entity_herb)
        return
    if entity_herb[key] == '' or entity_herb[key] == []:
        main_list_text = f'''
            Low fertility soils
            Moderate fertility soils
            Nutrient-rich soils
            Organically rich soils
            Average nutrient levels
            Poor nutrient soils
            High organic matter soils
        '''.strip()
        outputs = []
        for i in range(10):
            print(f'{i} - {herb_name_scientific}')
            import textwrap
            main_list_prompt = [e.strip() for e in main_list_text.split('\n') if e.strip() != '']
            random.shuffle(main_list_prompt)
            main_list_prompt = '\n'.join(main_list_prompt)
            prompt = textwrap.dedent(f''' 
                Tell me the best type of soil fertility to grow the following plant with scientific name: {herb_name_scientific}.
                In specific, write a confidence score from 1 to 10, indicating how sure you are about your answer.
                The possible types of soil fertility for you to pick from are the following:
                {main_list_prompt}
                Reply using the following JSON format:
                [
                    {{"answer": "write the type of soil fertility name here", "score": "write score here"}}
                ]
                Reply only with the JSON.
            ''').strip()
            prompt += f'\n/no_think'
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
        print(herb_filepath)
        io.json_write(herb_filepath, entity_herb)
        # print(entity_herb)
        # quit()

def herb_growing_soil_ph_gen(herb_filepath, regen=False, clear=False):
    entity_herb = io.json_read(herb_filepath)
    herb_name_scientific = entity_herb['herb_name_scientific']
    key = 'herb_growing_soil_ph'
    if key not in entity_herb: entity_herb[key] = ''
    if regen: entity_herb[key] = ''
    if clear: 
        entity_herb[key] = ''
        io.json_write(herb_filepath, entity_herb)
        return
    if entity_herb[key] == '' or entity_herb[key] == []:
        main_list_text = f'''
            Acidic soils
            Slightly acidic soils
            Neutral soils
            Slightly alkaline soils
            Alkaline soils
            Acidic to neutral soils
            Neutral to slightly alkaline soils
        '''.strip()
        outputs = []
        for i in range(10):
            print(f'{i} - {herb_name_scientific}')
            import textwrap
            main_list_prompt = [e.strip() for e in main_list_text.split('\n') if e.strip() != '']
            random.shuffle(main_list_prompt)
            main_list_prompt = '\n'.join(main_list_prompt)
            prompt = textwrap.dedent(f''' 
                Tell me the best type of soil ph to grow the following plant with scientific name: {herb_name_scientific}.
                In specific, write a confidence score from 1 to 10, indicating how sure you are about your answer.
                The possible types of soil ph for you to pick from are the following:
                {main_list_prompt}
                Reply using the following JSON format:
                [
                    {{"answer": "write the type of soil ph name here", "score": "write score here"}}
                ]
                Reply only with the JSON.
            ''').strip()
            prompt += f'\n/no_think'
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
        print(herb_filepath)
        io.json_write(herb_filepath, entity_herb)
        # print(entity_herb)
        # quit()

def herb_growing_sunlight_type_gen(herb_filepath, regen=False, clear=False):
    entity_herb = io.json_read(herb_filepath)
    herb_name_scientific = entity_herb['herb_name_scientific']
    key = 'herb_growing_sunlight_type'
    if key not in entity_herb: entity_herb[key] = ''
    if regen: entity_herb[key] = ''
    if clear: 
        entity_herb[key] = ''
        io.json_write(herb_filepath, entity_herb)
        return
    if entity_herb[key] == '' or entity_herb[key] == []:
        main_list_text = f'''
            Full sun
            Partial sun
            Partial shade
            Full shade
            Dappled shade
            Open sunlight
            Filtered sunlight
        '''.strip()
        outputs = []
        for i in range(10):
            print(f'{i} - {herb_name_scientific}')
            import textwrap
            main_list_prompt = [e.strip() for e in main_list_text.split('\n') if e.strip() != '']
            random.shuffle(main_list_prompt)
            main_list_prompt = '\n'.join(main_list_prompt)
            prompt = textwrap.dedent(f''' 
                Tell me the best sunlight type to grow the following plant with scientific name: {herb_name_scientific}.
                In specific, write a confidence score from 1 to 10, indicating how sure you are about your answer.
                The possible sunlight types for you to pick from are the following:
                {main_list_prompt}
                Reply using the following JSON format:
                [
                    {{"answer": "write the sunlight type name here", "score": "write score here"}}
                ]
                Reply only with the JSON.
            ''').strip()
            prompt += f'\n/no_think'
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
        print(herb_filepath)
        io.json_write(herb_filepath, entity_herb)
        # print(entity_herb)
        # quit()

def herb_growing_sunlight_tolerance_gen(herb_filepath, regen=False, clear=False):
    entity_herb = io.json_read(herb_filepath)
    herb_name_scientific = entity_herb['herb_name_scientific']
    key = 'herb_growing_sunlight_tolerance'
    if key not in entity_herb: entity_herb[key] = ''
    if regen: entity_herb[key] = ''
    if clear: 
        entity_herb[key] = ''
        io.json_write(herb_filepath, entity_herb)
        return
    if entity_herb[key] == '' or entity_herb[key] == []:
        main_list_text = f'''
            A wide range of light conditions
            Both sun and partial shade
            Partial shade to full shade
            Full sun to partial shade
            Low-light conditions
            Variable light exposure
        '''.strip()
        outputs = []
        for i in range(10):
            print(f'{i} - {herb_name_scientific}')
            import textwrap
            main_list_prompt = [e.strip() for e in main_list_text.split('\n') if e.strip() != '']
            random.shuffle(main_list_prompt)
            main_list_prompt = '\n'.join(main_list_prompt)
            prompt = textwrap.dedent(f''' 
                Tell me the sunlight tolerance to grow the following plant with scientific name: {herb_name_scientific}.
                In specific, write a confidence score from 1 to 10, indicating how sure you are about your answer.
                The possible sunlight tolerances for you to pick from are the following:
                {main_list_prompt}
                Reply using the following JSON format:
                [
                    {{"answer": "write the sunlight tolerance name here", "score": "write score here"}}
                ]
                Reply only with the JSON.
            ''').strip()
            prompt += f'\n/no_think'
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
        print(herb_filepath)
        io.json_write(herb_filepath, entity_herb)
        # print(entity_herb)
        # quit()

def herb_growing_watering_type_gen(herb_filepath, regen=False, clear=False):
    entity_herb = io.json_read(herb_filepath)
    herb_name_scientific = entity_herb['herb_name_scientific']
    key = 'herb_growing_watering_type'
    if key not in entity_herb: entity_herb[key] = ''
    if regen: entity_herb[key] = ''
    if clear: 
        entity_herb[key] = ''
        io.json_write(herb_filepath, entity_herb)
        return
    if entity_herb[key] == '' or entity_herb[key] == []:
        main_list_text = f'''
            Dry soils
            Moderately moist soils
            Moist soils
            Consistently moist soils
            Seasonally moist soils
            Well-balanced moisture levels
        '''.strip()
        outputs = []
        for i in range(10):
            print(f'{i} - {herb_name_scientific}')
            import textwrap
            main_list_prompt = [e.strip() for e in main_list_text.split('\n') if e.strip() != '']
            random.shuffle(main_list_prompt)
            main_list_prompt = '\n'.join(main_list_prompt)
            prompt = textwrap.dedent(f''' 
                Tell me the best watering type to grow the following plant with scientific name: {herb_name_scientific}.
                In specific, write a confidence score from 1 to 10, indicating how sure you are about your answer.
                The possible watering types for you to pick from are the following:
                {main_list_prompt}
                Reply using the following JSON format:
                [
                    {{"answer": "write the watering type name here", "score": "write score here"}}
                ]
                Reply only with the JSON.
            ''').strip()
            prompt += f'\n/no_think'
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
        print(herb_filepath)
        io.json_write(herb_filepath, entity_herb)
        # print(entity_herb)
        # quit()

def herb_growing_watering_tolerance_gen(herb_filepath, regen=False, clear=False):
    entity_herb = io.json_read(herb_filepath)
    herb_name_scientific = entity_herb['herb_name_scientific']
    key = 'herb_growing_watering_tolerance'
    if key not in entity_herb: entity_herb[key] = ''
    if regen: entity_herb[key] = ''
    if clear: 
        entity_herb[key] = ''
        io.json_write(herb_filepath, entity_herb)
        return
    if entity_herb[key] == '' or entity_herb[key] == []:
        main_list_text = f'''
            Periodic dry conditions
            Occasional drought
            Short periods of dryness
            Variable moisture levels
            Moderate moisture fluctuations
            Both dry and moist conditions
        '''.strip()
        outputs = []
        for i in range(10):
            print(f'{i} - {herb_name_scientific}')
            import textwrap
            main_list_prompt = [e.strip() for e in main_list_text.split('\n') if e.strip() != '']
            random.shuffle(main_list_prompt)
            main_list_prompt = '\n'.join(main_list_prompt)
            prompt = textwrap.dedent(f''' 
                Tell me the watering tolerance to grow the following plant with scientific name: {herb_name_scientific}.
                In specific, write a confidence score from 1 to 10, indicating how sure you are about your answer.
                The possible watering tolerances for you to pick from are the following:
                {main_list_prompt}
                Reply using the following JSON format:
                [
                    {{"answer": "write the watering tolerance name here", "score": "write score here"}}
                ]
                Reply only with the JSON.
            ''').strip()
            prompt += f'\n/no_think'
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
        print(herb_filepath)
        io.json_write(herb_filepath, entity_herb)
        # print(entity_herb)
        # quit()

def herb_family_wcvp(herb_filepath, regen=False, clear=False):
    global herbs_wcvp
    herb = io.json_read(herb_filepath)
    herb_name_scientific = herb['herb_name_scientific']
    herb_slug = herb['herb_slug']
    key = 'herb_family'
    if key not in herb: herb[key] = ''
    if regen: herb[key] = ''
    if clear: 
        herb[key] = ''
        io.json_write(herb_filepath, herb)
        return
    if herb[key] == '':
        if not herbs_wcvp:
            herbs_wcvp = [
                io.json_read(f'{g.PLANT_MEDICINE_FOLDERPATH}/{filename}')
                for filename in os.listdir(f'{g.PLANT_MEDICINE_FOLDERPATH}')
            ][:herbs_num]
        herb_family = ''
        for herb_wcvp_i, herb_wcvp in enumerate(herbs_wcvp):
            # print(herb_wcvp)
            # print('####################################')
            # print(f'{herb_wcvp_i}/{len(herbs_wcvp)} - {herb_wcvp}')
            # print('####################################')
            herb_wcvp_slug = herb_wcvp['herb_slug']
            if herb_slug == herb_wcvp_slug:
                herb_family = herb_wcvp['herb_family']
                break
        herb[key] = herb_family
        io.json_write(herb_filepath, herb)

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

def herb_traditional_medicinal_uses_gen(entity_herb_filepath, regen=False, clear=False):
    entity_herb = io.json_read(entity_herb_filepath)
    herb_name_scientific = entity_herb['herb_name_scientific']
    key = 'herb_traditional_uses'
    if key not in entity_herb: entity_herb[key] = ''
    if regen: entity_herb[key] = ''
    if clear: 
        entity_herb[key] = ''
        io.json_write(entity_herb_filepath, entity_herb)
        return
    if entity_herb[key] == '' or entity_herb[key] == []:
        outputs = []
        for i in range(1):
            print(f'{i} - {herb_name_scientific}')
            prompt = f'''
                Tell me primary traditional uses of the following medicinal herb with scientific name: {herb_name_scientific}.
                In specific, write a confidence score from 1 to 10, indicating how sure you are about your answer.
                Reply using the following JSON format:
                [
                    {{"answer": "write the traditional use 1 here", "score": "write score 1 here"}},
                    {{"answer": "write the traditional use 2 here", "score": "write score 2 here"}},
                    {{"answer": "write the traditional use 3 here", "score": "write score 3 here"}}
                ]
                Reply only with the JSON.
                Reply in as few words as possible.
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
                    outputs.append({
                        'answer': _obj['answer'], 
                        'mentions': 1, 
                        'confidence_score': int(_obj['score']), 
                    })
        outputs = total_score_calc(outputs)
        entity_herb[key] = outputs
        io.json_write(entity_herb_filepath, entity_herb)
        print(entity_herb_filepath)

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
    herb_slug = polish.sluggify(herb_name_scientific)
    ###
    herb_filepath = f'''{herbs_folderpath}/{herb_slug}.json'''
    herb_data = io.json_read(herb_filepath, create=True)
    herb_data['herb_slug'] = herb_slug
    herb_data['herb_name_scientific'] = herb_name_scientific
    io.json_write(herb_filepath, herb_data)
    ###
    herb_names_common_gen(herb_filepath, regen=False, clear=False)
    herb_origin_continents_gen(herb_filepath, regen=False, clear=False)
    herb_medicine_or_poison_gen(herb_filepath, regen=False, clear=False)
    ###
    herb_traditional_medicinal_uses_gen(herb_filepath, regen=False, clear=False)
    herb_family_ai(herb_filepath, regen=False, clear=False)
    herb_parts_gen(herb_filepath, regen=False, clear=False)
    herb_traditional_systems_gen(herb_filepath, regen=False, clear=False)
    herb_historical_preparations_gen(herb_filepath, regen=False, clear=False)
    ###
    herb_medicinal_actions_gen(herb_filepath, regen=False, clear=False)
    ###
    herb_active_compounds_gen(herb_filepath, regen=False, clear=False)
    ### safety
    herb_drugs_interaction_gen(herb_filepath, regen=False, clear=False)
    herb_allergies_gen(herb_filepath, regen=False, clear=False)
    herb_toxicity_gen(herb_filepath, regen=False, clear=False)
    herb_contraindications_gen(herb_filepath, regen=False, clear=False)
    herb_pregnancy_and_breastfeeding_gen(herb_filepath, regen=False, clear=False)
    herb_generally_safe_gen(herb_filepath, regen=False, clear=False)
    ### preparations
    herb_preparations_gen(herb_filepath, regen=False, clear=False)
    ### growing...
    herb_growing_soil_gen(herb_filepath, regen=False, clear=False)
    herb_growing_soil_drainage_gen(herb_filepath, regen=False, clear=False)
    herb_growing_soil_fertility_gen(herb_filepath, regen=False, clear=False)
    herb_growing_soil_ph_gen(herb_filepath, regen=False, clear=False)
    herb_growing_sunlight_type_gen(herb_filepath, regen=False, clear=False)
    herb_growing_sunlight_tolerance_gen(herb_filepath, regen=False, clear=False)
    herb_growing_watering_type_gen(herb_filepath, regen=False, clear=False)
    herb_growing_watering_tolerance_gen(herb_filepath, regen=False, clear=False)
    # herb_family_wcvp(herb_filepath, regen=False, clear=False)
    # herb_native_regions_ai(entity_herb_filepath, regen=False, clear=False)
    # herb_benefits_ai(entity_herb_filepath, regen=False, clear=False)
    # herb_therapeutic_actions_ai(entity_herb_filepath, regen=False, clear=False)


def herbs_primary_gen():
    herbs = data.herbs_primary_get()
    for herb_i, herb in enumerate(herbs):
        print('####################################')
        print(f'{herb_i}/{len(herbs)} - {herb}')
        print('####################################')
        herbs_primary_json(herb)
        print()
        print()
        print()

def herbs_popular_gen():
    herbs = data.herbs_popular_get('teas', 100)
    for herb_i, herb in enumerate(herbs):
        print('####################################')
        print(f'{herb_i}/{len(herbs)} - {herb}')
        print('####################################')
        herbs_primary_json(herb)
        print()
        print()
        print()

def herbs_primary_report():
    herbs = data.herbs_primary_get()
    herb_drugs_interaction_total_yes = 0
    herb_drugs_interaction_total_no = 0
    herb_drugs_interaction_total_unknown = 0
    herb_drugs_interaction_leading_yes = 0
    herb_drugs_interaction_leading_no = 0
    herb_drugs_interaction_leading_unknown = 0
    for herb_i, herb in enumerate(herbs):
        print('####################################')
        print(f'{herb_i}/{len(herbs)} - {herb}')
        print('####################################')
        herbs_folderpath = f'{g.SSOT_FOLDERPATH}/herbs/herbs-primary'
        ###
        herb_name_scientific = herb['herb_name_scientific']
        herb_slug = polish.sluggify(herb_name_scientific)
        ###
        herb_filepath = f'''{herbs_folderpath}/{herb_slug}.json'''
        herb_data = io.json_read(herb_filepath, create=True)
        ###
        herb_drugs_interaction = herb_data['herb_drugs_interaction']
        total_score_yes = 0
        total_score_no = 0
        total_score_unknown = 0
        for item in herb_drugs_interaction:
            print(item)
            if item['answer'] == 'yes':
                herb_drugs_interaction_total_yes += 1
                total_score_yes = item['total_score'] 
            if item['answer'] == 'no':
                herb_drugs_interaction_total_no += 1
                total_score_no = item['total_score'] 
            if item['answer'] == 'unknown':
                herb_drugs_interaction_total_unknown += 1
                total_score_unknown = item['total_score'] 
        if total_score_yes > total_score_no and total_score_yes > total_score_unknown: 
            herb_drugs_interaction_leading_yes += 1
        elif total_score_no > total_score_yes and total_score_no > total_score_unknown: 
            herb_drugs_interaction_leading_no += 1
        elif total_score_unknown > total_score_yes and total_score_unknown > total_score_no: 
            herb_drugs_interaction_leading_unknown += 1
        else:
            herb_drugs_interaction_leading_unknown += 1
    print('herb_drugs_interaction_total_yes:', herb_drugs_interaction_total_yes)
    print('herb_drugs_interaction_total_no:', herb_drugs_interaction_total_no)
    print('herb_drugs_interaction_total_unknown:', herb_drugs_interaction_total_unknown)
    print('herb_drugs_interaction_leading_yes:', herb_drugs_interaction_leading_yes)
    print('herb_drugs_interaction_leading_no:', herb_drugs_interaction_leading_no)
    print('herb_drugs_interaction_leading_unknown :', herb_drugs_interaction_leading_unknown)
    quit()

    print()
    print()
    print()

def main():
    herbs_primary_gen()
    herbs_popular_gen()

    # herbs_primary_report()

    # herbs_wcvp_medicinal_gen()

