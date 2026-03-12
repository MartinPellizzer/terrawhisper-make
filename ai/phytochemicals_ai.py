import json

from lib import g
from lib import io
from lib import llm


def phytochemicals_gen():
    json_folderpath = f'{g.SSOT_FOLDERPATH}/phytochemicals'
    json_filepath = f'''{json_folderpath}/phytochemicals.json'''
    json_data = io.json_read(json_filepath, create=True)
    regen = False
    dispel = False
    ###
    key = 'list'
    if key not in json_data: json_data[key] = ''
    if regen: json_data[key] = ''
    if dispel: 
        json_data[key] = ''
        io.json_write(json_filepath, json_data)
        return
    if json_data[key] == '' or json_data[key] == []:
        outputs = []
        for i in range(100):

            import textwrap
            prompt = textwrap.dedent(f''' 
                Give me a list of the 10 most popular phytochemicals in medicinal plants, in the context of herbal medicine.
                Also, write a confidence score from 1 to 10, indicating how sure you are about your answer.
                Reply using the following JSON format:
                [
                    {{"answer": "write phytochemical name 1 here", "score": "write score 1 here"}},
                    {{"answer": "write phytochemical name 2 here", "score": "write score 2 here"}},
                    {{"answer": "write phytochemical name 3 here", "score": "write score 3 here"}},
                    {{"answer": "write phytochemical name 4 here", "score": "write score 4 here"}},
                    {{"answer": "write phytochemical name 5 here", "score": "write score 5 here"}},
                    {{"answer": "write phytochemical name 6 here", "score": "write score 6 here"}},
                    {{"answer": "write phytochemical name 7 here", "score": "write score 6 here"}},
                    {{"answer": "write phytochemical name 8 here", "score": "write score 8 here"}},
                    {{"answer": "write phytochemical name 9 here", "score": "write score 9 here"}},
                    {{"answer": "write phytochemical name 10 here", "score": "write score 10 here"}}
                ]
                Reply only with the JSON.
            ''').strip()

            prompt += f'\n/no_think'
            print(prompt)
            reply = llm.reply(prompt)
            if '</think>' in reply:
                reply = reply.split('</think>')[1].strip()
            _json_data = {}
            try: _json_data = json.loads(reply)
            except: pass 
            if _json_data != {}:
                _objs = []
                for item in _json_data:
                    try: answer = item['answer']
                    except: continue
                    try: score = item['score']
                    except: continue
                    _objs.append({
                        "answer": answer, 
                        "score": score,
                    })
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
        json_data[key] = outputs
        io.json_write(json_filepath, json_data)

def main():
    phytochemicals_gen()
