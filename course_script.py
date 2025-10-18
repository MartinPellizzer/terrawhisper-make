from lib import io
from lib import llm

course_topic = f'how to make your first medicinal herbal tinctures at home in one afternoon'

################################################################################
# demo
################################################################################

'''
ingredients
    - herb
    - alcohol
    - knife
    - glass jars
    - cheesecloth

lessons
    1. Prepare a cup of fresh or dried herbs (Gather herbs fresh or dry, clean, and chop them)
    2. Prepare a cup of high-proof alcohol (Choose high-proof alcohol, like vodka)
    3. Combine herbs and alcohol in a jar (fill jar halfway with chopped herbs, pour alcohol to cover herbs completely)
    4. Seal jar and label it ()
    5. Let the mixture steep for 2 weeks (in a dark and cool place, shaking daily)
    6. Strain mixture through cheesecloth (into another jar)
    7. Store tincture in dark glass bottles

lessons
    - Gather herbs, clean, and chop them
    - Choose high-proof alcohol, like vodka
    - Fill jar halfway with chopped herbs
    - Pour alcohol to cover herbs completely
    - Seal jar and store in dark place
    - Let sit for 4-6 weeks, shaking weekly
    - Strain mixture through cheesecloth
    - Store tincture in dark glass bottles
    - Label with date and herb name
'''

# lessons
'''
1. Prepare a cup of herbs
2. Prepare a cup of high-proof alcohol
3. Combine herbs and alcohol in a jar
4. Seal jar and label it
5. Let the mixture steep for 2 weeks
6. Strain mixture through cheesecloth
7. Store tincture in dark glass bottles
'''
lessons = [
    '1. Prepare a cup of herbs',
    '2. Prepare a cup of high-proof alcohol',
    '3. Combine herbs and alcohol in a jar',
    '4. Seal jar and label it',
    '5. Let the mixture steep for 2 weeks',
    '6. Strain mixture through cheesecloth',
    '7. Store tincture in dark glass bottles',
]

if 0:
    prompt = f'''
        i'm making a course about how to make your first medicinal herbal tincture.
        for reference here's a list of all the lessons:
        1. Prepare a cup of herbs
        2. Prepare a cup of high-proof alcohol
        3. Combine herbs and alcohol in a jar
        4. Seal jar and label it
        5. Let the mixture steep for 2 weeks
        6. Strain mixture through cheesecloth
        7. Store tincture in dark glass bottles
        
        give me a list of the critical components associate with lesson "{lessons[1]}".
        reply only with the components. 
    '''
    prompt += f'/no_think'
    print(prompt)
    reply = llm.reply(prompt).strip()
    if '</think>' in reply:
        reply = reply.split('</think>')[1].strip()

# components
if 0:
    prompt = f'''
        i'm making a course about how to make your first medicinal herbal tincture.
        for reference here's a list of all the lessons:
        1. Prepare a cup of herbs
        2. Prepare a cup of high-proof alcohol
        3. Combine herbs and alcohol in a jar
        4. Seal jar and label it
        5. Let the mixture steep for 2 weeks (in a dark and cool place, shaking daily)
        6. Strain mixture through cheesecloth (into another jar)
        7. Store tincture in dark glass bottles
        
        give me a full, complete, and exhaustive step-by-step procedure on how to execute lesson "{lessons[6]}".
        write each step of the procedure in less than 10 words.
        write each step with a number and in a separated line.
        reply only with the procedure. 
    '''
    prompt += f'/no_think'
    print(prompt)
    reply = llm.reply(prompt).strip()
    if '</think>' in reply:
        reply = reply.split('</think>')[1].strip()
    with open('tmp-reply.txt', 'w') as f:
        f.write(reply)

# scripts
if 1:
    project_folderpath = '/home/ubuntu/vault/terrawhisper/database/shop/courses/make-your-first-tincture'
    src_folderpath = f'{project_folderpath}/src'
    with open('tmp-outline.txt') as f: lessons_outlines = f.read().split('---')
    for lesson_i, lesson_outline in enumerate(lessons_outlines):
        lines = ''
        for line in lesson_outline.split('\n'):
            if line.strip() == '': continue
            if line[0].isdigit():
                lines += f'Lesson {line}\n'
            elif line.startswith('    '):
                lines += f'               Step {line.strip()}\n'
        prompt = f'''
            i'm making a course about the following topic: {course_topic}.
            write the content for the following LESSON, using the following GUIDELINES and STRUCTURE.

            LESSON:
            {lines}

            STRUCTURE:
            1. hook and why this matters
                - start by explaining why this lesson is important.
                - then tell in one line what you will cover in this lesson.
                - example: "if your CV doesn't stand out, recruiters won't even open it. today, I'll show you how to fox that in 10 minutes."
            2. core teaching
                - start with "let me break it down into 3 steps:"
                - then break it into 3 steps, name the steps as the ones provided above.
                - use examples, case studies, or stories to make it engaging.
            3. summary/highlights
                - write a list of highlights from the lesson.
            4. action step
                - give them 1 simple task at the end.
                - example: "take 5 minutes to update your CV headline using the formula i just showed you."
            5. tease the next lesson
                - example: "how that your CV is optimized, next, we'll cover how to get recruitres to actually notice you. see you in the next lesson!"
        '''
        prompt += f'/no_think'
        print(prompt)
        reply = llm.reply(prompt).strip()
        if '</think>' in reply:
            reply = reply.split('</think>')[1].strip()
        i_str = ''
        if lesson_i < 10: i_str = f'0{lesson_i}'
        else: i_str = f'{lesson_i}'
        with open(f'{src_folderpath}/{lesson_i}.txt', 'w') as f:
            f.write(reply)

quit()


# procedure (full demo)
if 1:
    prompt = f'''
        write a full, complete, exhaustive step-by-step actionable procedure on how to make your first, quick, easy, inexpensive medicinal herbal tincture.
        write each step in less than 10 words.
        reply only with the procedure.
    '''
    prompt += f'/no_think'
    print(prompt)
    reply = llm.reply(prompt).strip()
    if '</think>' in reply:
        reply = reply.split('</think>')[1].strip()

# procedure (steps)
if 0:
    json_article_filepath = f'''course-tincture-making-system.json'''
    json_article = io.json_read(json_article_filepath, create=True)
    key = 'lessons'
    prompt = f'''
        write a step-by-step actionable procedure on how to make your first, quick, easy, inexpensive medicinal herbal tincture.
        write each step in less than 10 words.
        reply only with the procedure.
    '''
    prompt += f'/no_think'
    print(prompt)
    reply = llm.reply(prompt).strip()
    if '</think>' in reply:
        reply = reply.split('</think>')[1].strip()
    lines = [{'title': line.strip()} for line in reply.strip().split('\n')]
    json_article[key] = lines
    io.json_write(json_article_filepath, json_article)

if 0:
    json_article_filepath = f'''course-tincture-making-system.json'''
    json_article = io.json_read(json_article_filepath, create=True)
    for obj_i, obj in enumerate(json_article['sections']):
        obj['outline'] = ''
    io.json_write(json_article_filepath, json_article)

quit()

json_article_filepath = f'''course-tincture-making-system.json'''
json_article = io.json_read(json_article_filepath, create=True)
prompt_lessons_titles = '\n'.join([f'''{obj_i+1}. {obj['title']}''' for obj_i, obj in enumerate(json_article['sections'])])
for obj_i, obj in enumerate(json_article['sections']):
    # lesson outline
    prompt = f'''
        i'm making a course about how to make your first medicinal herbal tincture.
        here's a list of the lessons:
        {prompt_lessons_titles}
        also i have a content template that goes like this:
        ### why it's important.
        briefly describe why it's important.
        ---
        ### what's involved. 
        briefly describe the critical components associated with the step. at least 3 components.
        ---
        ### component 1: insert component title heading
        step 1
        step 2
        step 3
        etc.
        ---
        ### component 2: insert component title heading
        component 2
        step 1
        step 2
        step 3
        etc.
        ---
        ### component 3: insert component title heading
        component 3
        step 1
        step 2
        step 3
        etc.
        ---
        ### what can happen.
        good outcome.
        better outcome.
        best outcome.
        can you apply that template to lesson "{obj_i+1}. {obj['title']}" when it comes to "how to make your first medicinal herbal tincture"?
        keep the "---" and the "###" from the template.
    '''
    prompt += f'/no_think'
    print(prompt)
    reply = llm.reply(prompt).strip()
    if '</think>' in reply:
        reply = reply.split('</think>')[1].strip()
    reply_chunks = reply.split('---')
    obj['outline'] = {}
    if len(reply_chunks) == 6:
        obj['outline']['why'] = reply_chunks[0].strip()
        obj['outline']['what'] = reply_chunks[1].strip()
        component_heading = ''
        component_content = ''
        for line in reply_chunks[2].strip().split('\n'):
            line = line.strip()
            if line == '': continue
            if line.startswith('#'): component_heading = line.split(':')[1]
            else: component_content += line
        obj['outline']['component_1'] = {}
        obj['outline']['component_1']['heading'] = component_heading
        obj['outline']['component_1']['content'] = component_content
        ###
        component_heading = ''
        component_content = ''
        for line in reply_chunks[3].strip().split('\n'):
            line = line.strip()
            if line == '': continue
            if line.startswith('#'): component_heading = line.split(':')[1]
            else: component_content += line
        obj['outline']['component_2'] = {}
        obj['outline']['component_2']['heading'] = component_heading
        obj['outline']['component_2']['content'] = component_content
        ###
        component_heading = ''
        component_content = ''
        for line in reply_chunks[4].strip().split('\n'):
            line = line.strip()
            if line == '': continue
            if line.startswith('#'): component_heading = line.split(':')[1]
            else: component_content += line
        obj['outline']['component_3'] = {}
        obj['outline']['component_3']['heading'] = component_heading
        obj['outline']['component_3']['content'] = component_content

        obj['outline']['result'] = reply_chunks[5].strip()
    io.json_write(json_article_filepath, json_article)
    # quit()
quit()


################################################################################
# 1. experts
################################################################################
prompt = f'''
    identify the top 6 experts on how to make your first medicinal herbal tincture, and give me their top 9 strategies.
    provide it to me in a list.
    reply only with the list.
'''
prompt += f'/no_think'
print(prompt)
reply = llm.reply(prompt).strip()
if '</think>' in reply:
    reply = reply.split('</think>')[1].strip()
reply = reply.strip().lower().replace(' ', '-')

################################################################################
# 2. experts cluster
################################################################################
prompt = f'''
    here are the top 9 strategies of the top 6 experts on how to make your first medicinal herbal tincture:
    {reply}
    do you see any duplicate answer repeated from one expert to the next? give me 9.
'''
prompt += f'/no_think'
print(prompt)
reply = llm.reply(prompt).strip()
if '</think>' in reply:
    reply = reply.split('</think>')[1].strip()
reply = reply.strip().lower().replace(' ', '-')

