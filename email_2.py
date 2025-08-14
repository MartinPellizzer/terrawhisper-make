import json
import random

from lib import io
from lib import llm

def story_gen(topic):
    prompt = f'''
        today i want to write an email about the following topic: {topic}.
        i want to start the email with a story, so give me 10 ideas of story plots i can write to start this email.
        the story ideas must be about me, be relatable, and be a real story, not a fiction story.
        reply in the following JSON format: 
        [
            {{"answer": "write story plot idea 1 here"}}, 
            {{"answer": "write story plot idea 2 here"}}, 
            {{"answer": "write story plot idea 3 here"}} 
        ]
        only reply with the JSON, don't add additional info.
        /no_think
    '''
    reply = llm.reply(prompt).strip()
    if '</think>' in reply:
        reply = reply.split('</think>')[1].strip()
    json_data = {}
    try: json_data = json.loads(reply)
    except: pass 
    story = ''
    if json_data != {}:
        lst = []
        for item in json_data:
            try: answer = item['answer']
            except: continue
            lst.append(answer)
        story = random.choice(lst)
    return story

def working_solution_gen(topic):
    prompt = f'''
        today i want to write an email about the following topic: {topic}.
        i want you to give me the 10 best solutions to use for this topic, why they works, and how to use them.
        reply in the following JSON format: 
        [
            {{"answer": "write the solution 1 here", "why": "write why solution 1 works here", "how": "write how to use solution 1 here"}}, 
            {{"answer": "write the solution 2 here", "why": "write why solution 2 works here", "how": "write how to use solution 2 here"}}, 
            {{"answer": "write the solution 3 here", "why": "write why solution 3 works here", "how": "write how to use solution 3 here"}}, 
            {{"answer": "write the solution 4 here", "why": "write why solution 4 works here", "how": "write how to use solution 4 here"}}, 
            {{"answer": "write the solution 5 here", "why": "write why solution 5 works here", "how": "write how to use solution 5 here"}}, 
            {{"answer": "write the solution 6 here", "why": "write why solution 6 works here", "how": "write how to use solution 6 here"}}, 
            {{"answer": "write the solution 7 here", "why": "write why solution 7 works here", "how": "write how to use solution 7 here"}}, 
            {{"answer": "write the solution 8 here", "why": "write why solution 8 works here", "how": "write how to use solution 8 here"}}, 
            {{"answer": "write the solution 9 here", "why": "write why solution 9 works here", "how": "write how to use solution 9 here"}}, 
            {{"answer": "write the solution 10 here", "why": "write why solution 10 works here", "how": "write how to use solution 10 here"}} 
        ]
        only reply with the JSON, don't add additional info.
        /no_think
    '''
    print(prompt)
    reply = llm.reply(prompt).strip()
    if '</think>' in reply:
        reply = reply.split('</think>')[1].strip()
    json_data = {}
    try: json_data = json.loads(reply)
    except: pass 
    if json_data != {}:
        lst = []
        for item in json_data:
            try: answer = item['answer']
            except: continue
            try: why = item['why']
            except: continue
            try: how = item['how']
            except: continue
            lst.append(f'{answer} {why} {how}')
    working_solution = random.choice(lst)
    return working_solution

topic = 'herbal tinctures: your 5-minute equipment checklist - minimal tools you need'
story = story_gen(topic)
working_solution = working_solution_gen(topic)
print('========================================')
print(story)
print(working_solution)
print('========================================')
prompt = f'''
    Write a short email for my newsletter with the following STRUCTURE and GUIDELINES:
    <STRUCTURE>
    Introduction: 
    {story}
    Working solution:
    {working_solution}
    Conclusion:
    Encourage them to make this herbal remedy, in case they need it.
    Start the email with the words "Dear Apothecary, " and end it with the words "Stay Grounded, Leen".
    Add a P.S. section.
    </STRUCTURE>
'''
print('========================================')
