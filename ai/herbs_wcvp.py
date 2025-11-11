import os
import json
import shutil

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

def json_gen_medicine_poison_inert(wcvp_item, regen=False, clear=False):
    herb_name_scientific = wcvp_item['taxon_name']
    herb_slug = polish.sluggify(herb_name_scientific)
    ###
    json_filepath = f'{g.PLANTS_TMP_FOLDERPATH}/{herb_slug}.json'
    json_data = io.json_read(json_filepath)
    key = 'medicine_poison_inert'
    if key not in json_data: json_data[key] = ''
    if regen: json_data[key] = ''
    if clear: 
        json_data[key] = ''
        io.json_write(json_filepath, json_data)
        return
    if json_data[key] == '':
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
            reply_data = {}
            try: reply_data = json.loads(reply)
            except: pass 
            if reply_data != {}:
                _objs = answer_score_extract(reply_data)
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
        json_data[key] = outputs
        io.json_write(json_filepath, json_data)

def json_gen(wcvp_item):
    herb_name_scientific = wcvp_item['taxon_name']
    herb_slug = polish.sluggify(herb_name_scientific)
    print(f'{herb_slug} [JSON]')
    json_filepath = f'{g.PLANTS_TMP_FOLDERPATH}/{herb_slug}.json'
    json_data = io.json_read(json_filepath, create=True)
    json_data['herb_slug'] = herb_slug
    json_data['herb_name_scientific'] = herb_name_scientific
    json_data['herb_family'] = wcvp_item['family']
    json_data['herb_title'] = herb_name_scientific.capitalize()
    io.json_write(json_filepath, json_data)
    ###
    json_gen_medicine_poison_inert(wcvp_item, regen=False, clear=False)
    # json_gen_intro(herb_slug, regen=False, clear=False)

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
    if 0:
        wcvp_data = io.csv_to_dict(f'{g.WCVP_FOLDERPATH}/wcvp_names.csv', '|')
        for wcvp_item_i, wcvp_item in enumerate(wcvp_data):
            print(f'>>> {wcvp_item_i}/{len(wcvp_data)} - {wcvp_item}')
            print(f'{wcvp_item}')
            json_gen(wcvp_item)
            # quit()
    else:
        num_medicine = 0
        num_inert = 0
        num_poison = 0
        num_total = 0
        tmp_filenames = os.listdir(f'{g.PLANTS_TMP_FOLDERPATH}')
        for tmp_filename_i, tmp_filename in enumerate(tmp_filenames[:]):
            tmp_filepath = f'{g.PLANTS_TMP_FOLDERPATH}/{tmp_filename}'
            print(f'{tmp_filename_i} - {tmp_filepath}')
            medicine_poison_inert = medicine_poison_inert_get(tmp_filepath)
            if medicine_poison_inert == None: continue
            if medicine_poison_inert['answer'] == 'medicine':
                num_medicine += 1
                num_total += 1
                dst_filepath = f'{g.JSON_HERBS_FOLDERPATH}/{tmp_filename}'
                if not os.path.exists(dst_filepath):
                    shutil.copy2(tmp_filepath, dst_filepath)
            if medicine_poison_inert['answer'] == 'inert':
                num_inert += 1
                num_total += 1
            if medicine_poison_inert['answer'] == 'poison':
                num_poison += 1
                num_total += 1
        print(f'MEDICINE: {num_medicine}')
        print(f'INERT: {num_inert}')
        print(f'POISON: {num_poison}')
        print(f'TOTAL: {num_total}')


