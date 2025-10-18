import os
import json

from lib import g
from lib import io
from lib import llm

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
            'average_score': int(output['confidence_score']) // int(output['mentions']),
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
    key = 'medicine'
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
                Give me a score from 1 to 10, indicating how much the following plant is considered medicinal: {herb_name_scientific}.
                Reply in the following JSON format: 
                [
                    {{"answer": "{herb_name_scientific}", "score": "insert score here"}} 
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

def json_gen(json_herb_filepath):
    herb_medicine_or_poison_ai(json_herb_filepath, regen=False, clear=False)

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

def gen():
    tmp_filenames = os.listdir(f'{g.PLANTS_TMP_FOLDERPATH}')
    for tmp_filename_i, tmp_filename in enumerate(tmp_filenames[:]):
        tmp_filepath = f'{g.PLANTS_TMP_FOLDERPATH}/{tmp_filename}'
        print(f'{tmp_filename_i} - {tmp_filepath}')
        medicine_poison_inert = medicine_poison_inert_get(tmp_filepath)
        if medicine_poison_inert == None: continue
        if medicine_poison_inert['answer'] == 'medicine':
            json_herb_filepath = f'{g.JSON_HERBS_FOLDERPATH}/{tmp_filename}'
            if os.path.isfile(json_herb_filepath):
                print(json_herb_filepath)
                json_gen(json_herb_filepath)
                # quit()

