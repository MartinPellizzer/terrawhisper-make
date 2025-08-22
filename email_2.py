import json
import random

from lib import io
from lib import llm

topic = 'tincture dosage and safety checklist'

def story_gen(topic):
    prompt = f'''
        today i want to write an email about the following topic: {topic}.
        i want to start the email with a story, so give me 10 ideas of story plots i can write to start this email.
        the story ideas must be about me, be relatable, and be a real story (not a fiction story).
        also, it must be a story about a long time ago past.
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

story = story_gen(topic)
# working_solution = working_solution_gen(topic)
working_solution = 'checklist'
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

    <GUIDELINES>
    Write using a blend of the following 2 styles:
    Style 1:
        Write this in my personal voice. Make it raw, honest, and unfiltered. Use punchy one-liners, bold emotional confessions, and dramatic pacing with short paragraphs. Don’t polish the language too much—I want it real. It should feel like I’m talking directly to a friend over a drink, not giving a TED Talk.
        Use casual slang where it fits. Curse if it serves the point. Use ellipses, parentheses, and capitalization for rhythm and emphasis. Balance vulnerability with wit. Show that I’m not afraid to admit mistakes, but I’m also not afraid to laugh at them.
        Think: Gary Vee meets Brene Brown with a little Dave Chappelle spice.
        Never swear.
        Never use acronym.
    Style 2:
        Write in a warm, grounded, poetic tone that feels like ancient wisdom remembered. 
        Use short, gentle sentences that speak directly to the reader (“you”), often beginning with a truth and ending with a soft reframe or reminder. 
        Prioritize simplicity, slowness, and intuition over trends or complexity. 
        Use earthy, sensory language (e.g. bloated, nourished, rooted, ritual, tea, thrive, remember). 
        Healing is nonlinear, and herbs are gentle guides—not quick fixes. 
        Let each post feel like a quiet truth shared over tea.
    </GUIDELINES>
'''
prompt += '/no_think'
print(prompt)
print('========================================')

reply = llm.reply(prompt).strip()
if '</think>' in reply:
    reply = reply.split('</think>')[1].strip()

