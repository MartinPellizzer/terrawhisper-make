import os
import json

from lib import g
from lib import io
from lib import llm
from lib import data

# herbs_wcvp = data.herbs_wcvp_get()
# print(herbs_wcvp[0])
# quit()

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

def herb_wcvp_find(herb):
    for herb_wcvp in herbs_wcvp:
        if herb_wcvp['taxon_name'].lower().strip() == herb['herb_name_scientific'].lower().strip():
            return herb_wcvp
    return None

def ssot_taxonomy_families_gen(herb):
    taxonomy_folderpath = f'{g.SSOT_FOLDERPATH}/taxonomy'
    try: os.mkdir(herbs_folderpath)
    except: pass
    ###
    taxonomy_filepath = f'''{taxonomy_folderpath}/families.json'''
    taxonomy_data = io.json_read(taxonomy_filepath, create=True, l=True)
    herb_name_scientific = herb['taxon_name']
    family = herb['family']
    genus = herb['genus']
    species = herb['species']
    ### init familiy
    found = False
    for taxonomy in taxonomy_data:
        if taxonomy['family'].lower().strip() == family.lower().strip():
            found = True
            break
    if not found:
        outputs = []
        for i in range(10):
            print(f'''{i} - {family}''')
            import textwrap
            prompt = textwrap.dedent(f'''
                Write the Linnaean system of classification for the plant: {herb_name_scientific}.
                The Linnaean system is classified by: Kingdom, Division, Class, Subclass, Order, Family, Genus, Species.
                I will give you the Species, Genus, Family of this plant and you to figure out the rest.
                If you are not sure about a name in the classification, reply with "N/A".
                Also, give a score from 1 to 10 for each answer, indicating how confident you are about that specific answer.
                Use as few words as possible.
                Reply with the following JSON format:
                [
                    {{"Kingdom": "write the kingdom name here", "Kingdom_Score": "write kingdom confidence score here"}},
                    {{"Division": "write the division name here", "Division_Score": "write division confidence score here"}},
                    {{"Class": "write the class name here", "Class_Score": "write class confidence score here"}},
                    {{"Subclass": "write the subclass name here", "Subclass_Score": "write subclass confidence score here"}},
                    {{"Order": "write the order name here", "Order_Score": "write order confidence score here"}},
                    {{"Family": "{family}"}},
                    {{"Genus": "{genus}"}},
                    {{"Species": "{species}"}}
                ]
                Reply only with the JSON.
            ''').strip()
            prompt += f'/no_think'
            reply = llm.reply(prompt)
            if '</think>' in reply:
                reply = reply.split('</think>')[1].strip()
            json_data = {}
            try: json_data = json.loads(reply)
            except: pass 
            if json_data != {}:
                _objs = []
                for item in json_data:
                    try: answer = item['Order']
                    except: continue
                    try: answer = item['Subclass']
                    except: continue
                    try: score = str(item['Score'])
                    except: continue
                    _objs.append({
                        "answer": answer.lower(), 
                        "score": score.lower(),
                    })
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
        taxonomy_data.append(
            {
                'family': family,
                'order': outputs,
            }
        )
        io.json_write(taxonomy_filepath, taxonomy_data)

def ssot_taxonomy_orders_gen(herb):
    taxonomy_folderpath = f'{g.SSOT_FOLDERPATH}/taxonomy'
    try: os.mkdir(herbs_folderpath)
    except: pass
    ###
    taxonomy_filepath = f'''{taxonomy_folderpath}/orders.json'''
    taxonomy_data = io.json_read(taxonomy_filepath, create=True, l=True)
    herb_name_scientific = herb['taxon_name']
    ###
    family = herb['family']
    genus = herb['genus']
    species = herb['species']
    ###
    order = [
        e['order'][0]['answer'] 
        for e in io.json_read(f'''{g.SSOT_FOLDERPATH}/taxonomy/families.json''') 
        if e['family'].lower().strip() == family.lower().strip()
    ][0].strip()
    ### init order
    found = False
    for taxonomy in taxonomy_data:
        if taxonomy['order'].lower().strip() == order.lower().strip():
            found = True
            break
    if not found:
        outputs = []
        for i in range(10):
            print(f'''{i} - {order}''')
            import textwrap
            prompt = textwrap.dedent(f'''
                Write the Linnaean system of classification for the plant: {herb_name_scientific}.
                The Linnaean system is classified by: Kingdom, Division, Class, Subclass, Order, Family, Genus, Species.
                I will give you the Species, Genus, Family, Order of this plant and you to figure out the rest.
                If you are not sure about a name in the classification, reply with "N/A".
                Also, give a score from 1 to 10 for the Subclass, indicating how confident you are about that specific answer.
                Use as few words as possible.
                Reply with the following JSON format:
                [
                    {{"Kingdom": "write the kingdom name here"}},
                    {{"Division": "write the division name here"}},
                    {{"Class": "write the class name here"}},
                    {{"Subclass": "write the subclass name here", "Score": "write confidence score here"}},
                    {{"Order": "{order}"}},
                    {{"Family": "{family}"}},
                    {{"Genus": "{genus}"}},
                    {{"Species": "{species}"}}
                ]
                Reply only with the JSON.
            ''').strip()
            prompt += f'/no_think'
            reply = llm.reply(prompt)
            if '</think>' in reply:
                reply = reply.split('</think>')[1].strip()
            json_data = {}
            try: json_data = json.loads(reply)
            except: pass 
            if json_data != {}:
                _objs = []
                for item in json_data:
                    try: answer = item['Subclass']
                    except: continue
                    try: score = str(item['Score'])
                    except: continue
                    if score.lower().strip() == 'n/a': score = str(0)
                    _objs.append({
                        "answer": answer.lower(), 
                        "score": score.lower(),
                    })
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
        taxonomy_data.append(
            {
                'order': order.lower().strip(),
                'subclass': outputs,
            }
        )
        io.json_write(taxonomy_filepath, taxonomy_data)

def ssot_taxonomy_subclasses_gen(herb):
    taxonomy_folderpath = f'{g.SSOT_FOLDERPATH}/taxonomy'
    try: os.mkdir(herbs_folderpath)
    except: pass
    ###
    taxonomy_filepath = f'''{taxonomy_folderpath}/subclasses.json'''
    taxonomy_data = io.json_read(taxonomy_filepath, create=True, l=True)
    herb_name_scientific = herb['taxon_name']
    ###
    family = herb['family']
    genus = herb['genus']
    species = herb['species']
    ###
    order = [
        e['order'][0]['answer'] 
        for e in io.json_read(f'''{g.SSOT_FOLDERPATH}/taxonomy/families.json''') 
        if e['family'].lower().strip() == family.lower().strip()
    ][0].strip()
    subclass = [
        e['subclass'][0]['answer'] 
        for e in io.json_read(f'''{g.SSOT_FOLDERPATH}/taxonomy/orders.json''') 
        if e['order'].lower().strip() == order.lower().strip()
    ][0].strip()
    ### init order
    found = False
    for taxonomy in taxonomy_data:
        if taxonomy['subclass'].lower().strip() == subclass.lower().strip():
            found = True
            break
    if not found:
        outputs = []
        for i in range(10):
            print(f'''{i} - {subclass}''')
            import textwrap
            prompt = textwrap.dedent(f'''
                Write the Linnaean system of classification for the plant: {herb_name_scientific}.
                The Linnaean system is classified by: Kingdom, Division, Class, Subclass, Order, Family, Genus, Species.
                I will give you the Species, Genus, Family, Order, Subclass of this plant and you to figure out the rest.
                If you are not sure about a name in the classification, reply with "N/A".
                Also, give a score from 1 to 10 for the Class, indicating how confident you are about that specific answer.
                Use as few words as possible.
                Reply with the following JSON format:
                [
                    {{"Kingdom": "write the kingdom name here"}},
                    {{"Division": "write the division name here"}},
                    {{"Class": "write the class name here", "Score": "write confidence score here"}},
                    {{"Subclass": "{subclass}"}},
                    {{"Order": "{order}"}},
                    {{"Family": "{family}"}},
                    {{"Genus": "{genus}"}},
                    {{"Species": "{species}"}}
                ]
                Reply only with the JSON.
            ''').strip()
            prompt += f'/no_think'
            reply = llm.reply(prompt)
            if '</think>' in reply:
                reply = reply.split('</think>')[1].strip()
            json_data = {}
            try: json_data = json.loads(reply)
            except: pass 
            if json_data != {}:
                _objs = []
                for item in json_data:
                    try: answer = item['Class']
                    except: continue
                    try: score = str(item['Score'])
                    except: continue
                    if score.lower().strip() == 'n/a': score = str(0)
                    _objs.append({
                        "answer": answer.lower(), 
                        "score": score.lower(),
                    })
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
        taxonomy_data.append(
            {
                'subclass': subclass.lower().strip(),
                'class': outputs,
            }
        )
        io.json_write(taxonomy_filepath, taxonomy_data)

def ssot_taxonomy_classes_gen(herb):
    taxonomy_folderpath = f'{g.SSOT_FOLDERPATH}/taxonomy'
    try: os.mkdir(herbs_folderpath)
    except: pass
    ###
    taxonomy_filepath = f'''{taxonomy_folderpath}/classes.json'''
    taxonomy_data = io.json_read(taxonomy_filepath, create=True, l=True)
    herb_name_scientific = herb['taxon_name']
    ###
    family = herb['family']
    genus = herb['genus']
    species = herb['species']
    ###
    order = [
        e['order'][0]['answer'] 
        for e in io.json_read(f'''{g.SSOT_FOLDERPATH}/taxonomy/families.json''') 
        if e['family'].lower().strip() == family.lower().strip()
    ][0].strip()
    subclass = [
        e['subclass'][0]['answer'] 
        for e in io.json_read(f'''{g.SSOT_FOLDERPATH}/taxonomy/orders.json''') 
        if e['order'].lower().strip() == order.lower().strip()
    ][0].strip()
    _class = [
        e['class'][0]['answer'] 
        for e in io.json_read(f'''{g.SSOT_FOLDERPATH}/taxonomy/subclasses.json''') 
        if e['subclass'].lower().strip() == subclass.lower().strip()
    ][0].strip()
    ### init order
    found = False
    for taxonomy in taxonomy_data:
        if taxonomy['class'].lower().strip() == _class.lower().strip():
            found = True
            break
    if not found:
        outputs = []
        for i in range(10):
            print(f'''{i} - {_class}''')
            import textwrap
            prompt = textwrap.dedent(f'''
                Write the Linnaean system of classification for the plant: {herb_name_scientific}.
                The Linnaean system is classified by: Kingdom, Division, Class, Subclass, Order, Family, Genus, Species.
                I will give you the Species, Genus, Family, Order, Subclass, Class of this plant and you to figure out the rest.
                If you are not sure about a name in the classification, reply with "N/A".
                Also, give a score from 1 to 10 for the Division, indicating how confident you are about that specific answer.
                Use as few words as possible.
                Reply with the following JSON format:
                [
                    {{"Kingdom": "write the kingdom name here"}},
                    {{"Division": "write the division name here", "Score": "write confidence score here"}},
                    {{"Class": "{_class}"}},
                    {{"Subclass": "{subclass}"}},
                    {{"Order": "{order}"}},
                    {{"Family": "{family}"}},
                    {{"Genus": "{genus}"}},
                    {{"Species": "{species}"}}
                ]
                Reply only with the JSON.
            ''').strip()
            prompt += f'/no_think'
            reply = llm.reply(prompt)
            if '</think>' in reply:
                reply = reply.split('</think>')[1].strip()
            json_data = {}
            try: json_data = json.loads(reply)
            except: pass 
            if json_data != {}:
                _objs = []
                for item in json_data:
                    try: answer = item['Division']
                    except: continue
                    try: score = str(item['Score'])
                    except: continue
                    if score.lower().strip() == 'n/a': score = str(0)
                    _objs.append({
                        "answer": answer.lower(), 
                        "score": score.lower(),
                    })
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
        taxonomy_data.append(
            {
                'class': _class.lower().strip(),
                'division': outputs,
            }
        )
        io.json_write(taxonomy_filepath, taxonomy_data)


def taxonomy_gen():
    ### run data/herbs_data.py before this when adding new herbs
    herbs_folderpath = f'{g.SSOT_FOLDERPATH}/herbs'
    herbs_filepath = f'''{herbs_folderpath}/herbs-medicinal-validated.json'''
    herbs = io.json_read(herbs_filepath)
    for herb_i, herb in enumerate(herbs):
        print('####################################')
        print(f'{herb_i}/{len(herbs)} - {herb}')
        print('####################################')
        # TODO: fix families
        # ssot_taxonomy_families_gen(herb)
        # ssot_taxonomy_orders_gen(herb)
        # ssot_taxonomy_subclasses_gen(herb)
        ssot_taxonomy_classes_gen(herb)
        continue
        ### get generated order from family
        taxonomy_folderpath = f'{g.SSOT_FOLDERPATH}/taxonomy'
        taxonomy_filepath = f'''{taxonomy_folderpath}/taxonomy.json'''
        taxonomy_data = io.json_read(taxonomy_filepath)
        order = [
            item['order'][0]['answer']
            for item in taxonomy_data 
            if item['family'].lower().strip() == family.lower().strip()
        ][0]
        ### get generated class from order
        taxonomy_folderpath = f'{g.SSOT_FOLDERPATH}/taxonomy'
        taxonomy_filepath = f'''{taxonomy_folderpath}/order.json'''
        taxonomy_data = io.json_read(taxonomy_filepath)
        _class = [
            item['class'][0]['answer']
            for item in taxonomy_data 
            if item['order'].lower().strip() == order.lower().strip()
        ][0]
        ssot_taxonomy_class_gen(family, order, _class)
        ###
        # print(family)
        # family
        # order
        # class
        # division
        # kingdom
        # quit()
    print()
    print()
    print()
    quit()

def main():
    taxonomy_gen()


