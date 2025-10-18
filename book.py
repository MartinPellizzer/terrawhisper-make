import time
import json
import random

from lib import g
from lib import io
from lib import llm

def outline_init():
    outline_filepath = f'{g.SHOP_FOLDERPATH}/books/tincture-mastery/outline.txt'
    with open(outline_filepath) as f: content = f.read().strip()
    lines = [line for line in content.split('\n') if line.strip() != '']
    lines_formatted = []
    for line in lines:
        if line.startswith('            '):
            line = line.strip()
            if line[0].isdigit():
                line = ' '.join(line.split(' ')[1:])
            line = f'[H4] {line.strip()}'
            print(f'            {line.strip()}')
        elif line.startswith('        '):
            line = line.strip()
            if line[0].isdigit():
                line = ' '.join(line.split(' ')[1:])
            line = f'[H3] {line.strip()}'
            print(f'        {line.strip()}')
        elif line.startswith('    '):
            line = line.strip()
            if line[0].isdigit():
                line = ' '.join(line.split(' ')[1:])
            line = f'[H2] {line.strip()}'
            print(f'    {line.strip()}')
        else:
            line = line.strip()
            if line[0].isdigit():
                line = ' '.join(line.split(' ')[1:])
            line = f'[H1] {line.strip()}'
            print(f'{line.strip()}')
        lines_formatted.append(line)
    print()
    print()
    print()

    for line in lines_formatted:
        print(line)

    print()
    print()
    print()

    outline_dict = {}
    outline_dict['chapter_list'] = []
    chapter_cur = None
    section_cur = None
    subsection_cur = None
    for line in lines_formatted:
        line_type = line.split(' ')[0]
        line_content = ' '.join(line.split(' ')[1:])
        if line_type == '[H1]':
            outline_dict['chapter_list'].append({
                'name': line_content,
                'section_list': [],
            })
            chapter_cur = outline_dict['chapter_list'][-1]
        elif line_type == '[H2]':
            chapter_cur['section_list'].append({
                'name': line_content,
                'subsection_list': [],
            })
            section_cur = chapter_cur['section_list'][-1]
        elif line_type == '[H3]':
            section_cur['subsection_list'].append({
                'name': line_content,
                'qa_list': [],
            })
            subsection_cur = section_cur['subsection_list'][-1]
        elif line_type == '[H4]':
            subsection_cur['qa_list'].append({
                'question': line_content,
                'answer_short': '',
                'answer_medium': '',
                'answer_long': '',
            })

    print()
    print()
    print()

    print(json.dumps(
        outline_dict,
        indent=4,
    ))
    json_filepath = f'{g.SHOP_FOLDERPATH}/books/tincture-mastery/data.json'
    io.json_write(json_filepath, outline_dict)

def answer_gen():
    json_filepath = f'{g.SHOP_FOLDERPATH}/books/tincture-mastery.json'
    json_data = io.json_read(json_filepath)
    chapter_list = json_data['chapter_list']
    for chapter in chapter_list:
        print(f'''CHAPTER: {chapter['name']}''')
        section_list = chapter['section_list']
        for section in section_list:
            print(f'''SECTION: {section['name']}''')
            subsection_list = section['subsection_list']
            for subsection in subsection_list:
                print(f'''SUBSECTION: {subsection['name']}''')
                qa_list = subsection['qa_list']
                for qa in qa_list:
                    print(f'''QUESTION: {qa['question']}''')
                    question = qa['question']
                    ### gen answer short
                    if qa['answer_short'] == '':
                        prompt = f'Answer the following question in one line: {question}'
                        prompt += f'/no_think'
                        reply = llm.reply(prompt, model_filepath='')
                        if '</think>' in reply:
                            reply = reply.split('</think>')[1].strip()
                        qa['answer_short'] = reply
                        io.json_write(json_filepath, json_data)
                    ### gen answer medium
                    if qa['answer_medium'] == '':
                        prompt = f'Answer the following question in one paragraph: {question}'
                        prompt += f'/no_think'
                        reply = llm.reply(prompt, model_filepath='')
                        if '</think>' in reply:
                            reply = reply.split('</think>')[1].strip()
                        qa['answer_medium'] = reply
                        io.json_write(json_filepath, json_data)
                    ### gen answer long
                    if qa['answer_long'] == '':
                        prompt = f'Answer the following question in one page: {question}'
                        prompt += f'/no_think'
                        reply = llm.reply(prompt, model_filepath='')
                        if '</think>' in reply:
                            reply = reply.split('</think>')[1].strip()
                        qa['answer_long'] = reply
                        io.json_write(json_filepath, json_data)
                    if 0:
                        ### gen answer long book
                        if 'answer_long_book' not in qa: qa['answer_long_book'] = ''
                        if qa['answer_long_book'] == '':
                            prompt = f'Answer the following question in one page of a book: {question}. Format it like tipical content you find in books.'
                            prompt += f'/no_think'
                            reply = llm.reply(prompt, model_filepath='')
                            if '</think>' in reply:
                                reply = reply.split('</think>')[1].strip()
                            qa['answer_long_book'] = reply
                            io.json_write(json_filepath, json_data)

def text_format(text):
    text_formatted = text
    text_formatted = text_formatted.replace('’', "'")
    text_formatted = text_formatted.replace('–', "-")
    text_formatted = text_formatted.replace('—', "-")
    import string
    printable = set(string.printable)
    # printable = filter(lambda x: x in printable, text_formatted)
    printable = ''.join(filter(lambda x: x in printable, text_formatted))
    return printable

px_in = 20
px_out = 20

def h1(pdf, text):
    pdf.add_page()
    pdf.set_font('Helvetica', size=36, style='B')
    pdf.x = px_out
    pdf.multi_cell(210 - px_in - px_out, 12, text=f'{text}')
    pdf.ln()

def h2(pdf, text):
    pdf.add_page()
    pdf.set_font('Helvetica', size=24, style='B')
    pdf.x = px_out
    pdf.multi_cell(210 - px_in - px_out, 10, text=f'{text}')
    pdf.ln()

def h3(pdf, text):
    # pdf.add_page()
    pdf.set_font('Helvetica', size=16, style='B')
    pdf.x = px_out
    pdf.multi_cell(210 - px_in - px_out, 8, text=f'{text}')
    pdf.ln()

def h4(pdf, text):
    pdf.set_font('Helvetica', size=12, style='B')
    pdf.x = px_out
    pdf.multi_cell(210 - px_in - px_out, 6, text=f'{text}')
    pdf.ln()

def pdf_gen(qa_len):
    from fpdf import FPDF
    pdf = FPDF()
    json_filepath = f'{g.SHOP_FOLDERPATH}/books/tincture-mastery.json'
    json_data = io.json_read(json_filepath)
    chapter_list = json_data['chapter_list']
    for chapter_i, chapter in enumerate(chapter_list):
        print(f'''CHAPTER: {chapter['name']}''')
        chapter_name = chapter['name']
        chapter_name = text_format(chapter_name)
        text = f'{chapter_i+1}. {chapter_name}'
        h1(pdf, text)
        ### section
        section_list = chapter['section_list']
        for section_i, section in enumerate(section_list):
            print(f'''SECTION: {section['name']}''')
            section_name = section['name']
            section_name = text_format(section_name)
            text = f'{chapter_i+1}.{section_i+1} {section_name}'
            h2(pdf, text)
            ### subsection
            subsection_list = section['subsection_list']
            for subsection_i, subsection in enumerate(subsection_list):
                print(f'''SUBSECTION: {subsection['name']}''')
                subsection_name = subsection['name']
                subsection_name = text_format(subsection_name)
                text = f'{chapter_i+1}.{section_i+1}.{subsection_i+1} {subsection_name}'
                h3(pdf, text)
                ### qa
                qa_list = subsection['qa_list']
                for qa_i, qa in enumerate(qa_list):
                    print(f'''QUESTION: {qa}''')
                    question = qa['question']
                    question = text_format(question)
                    text = f'{chapter_i+1}.{section_i+1}.{subsection_i+1}.{qa_i+1} {question}'
                    h4(pdf, text)
                    if qa_len == 'short':
                        answer = qa['answer_short']
                        answer = text_format(answer)
                    elif qa_len == 'medium':
                        answer = qa['answer_medium']
                        answer = text_format(answer)
                    elif qa_len == 'long':
                        answer = qa['answer_long']
                        answer = text_format(answer)
                    elif qa_len == 'long-book':
                        answer = qa['answer_long_book']
                        answer = text_format(answer)
                    pdf.set_font('Helvetica', size=11)
                    pdf.x = px_out
                    pdf.multi_cell(210 - px_in - px_out, 6, text=f'{answer}')
                    pdf.ln()
    pdf.output(f'{g.SHOP_FOLDERPATH}/books/tincture-mastery-{qa_len}.pdf')

def answer_merge_gen(qa_len):
    json_filepath = f'{g.SHOP_FOLDERPATH}/books/tincture-mastery.json'
    json_data = io.json_read(json_filepath)
    chapter_list = json_data['chapter_list']
    for chapter in chapter_list:
        print(f'''CHAPTER: {chapter['name']}''')
        section_list = chapter['section_list']
        for section in section_list:
            print(f'''SECTION: {section['name']}''')
            subsection_list = section['subsection_list']
            for subsection in subsection_list:
                print(f'''SUBSECTION: {subsection['name']}''')
                if qa_len == 'short':
                    if 'merged_answers_short' not in subsection: 
                        qa_list = subsection['qa_list']
                        qa_list_flat = ''
                        for qa_i, qa in enumerate(qa_list):
                            print(f'''QUESTION: {qa}''')
                            question = qa['question']
                            question = text_format(question)
                            answer = qa['answer_short']
                            answer = text_format(answer)
                            qa_list_flat += f'{answer} '
                        ### qa
                        prompt = f'Write one page of a book using the following content: {qa_list_flat}'
                        prompt += f'/no_think'
                        reply = llm.reply(prompt, model_filepath='')
                        if '</think>' in reply:
                            reply = reply.split('</think>')[1].strip()
                        reply = text_format(reply)
                        subsection['merged_answers_short'] = reply
                        io.json_write(json_filepath, json_data)
                elif qa_len == 'medium':
                    if 'merged_answers_medium' not in subsection: 
                        qa_list = subsection['qa_list']
                        qa_list_flat = ''
                        for qa_i, qa in enumerate(qa_list):
                            print(f'''QUESTION: {qa}''')
                            question = qa['question']
                            question = text_format(question)
                            answer = qa['answer_medium']
                            answer = text_format(answer)
                            qa_list_flat += f'{answer} '
                        ### qa
                        prompt = f'Write one page of a book using the following content: {qa_list_flat}'
                        prompt += f'/no_think'
                        reply = llm.reply(prompt, model_filepath='')
                        if '</think>' in reply:
                            reply = reply.split('</think>')[1].strip()
                        reply = text_format(reply)
                        subsection['merged_answers_medium'] = reply
                        io.json_write(json_filepath, json_data)
            # return

def pdf_merge_answers_gen(qa_len):
    from fpdf import FPDF
    pdf = FPDF()
    json_filepath = f'{g.SHOP_FOLDERPATH}/books/tincture-mastery.json'
    json_data = io.json_read(json_filepath)
    chapter_list = json_data['chapter_list']
    for chapter_i, chapter in enumerate(chapter_list):
        print(f'''CHAPTER: {chapter['name']}''')
        chapter_name = chapter['name']
        chapter_name = text_format(chapter_name)
        text = f'{chapter_i+1}. {chapter_name}'
        h1(pdf, text)
        ### section
        section_list = chapter['section_list']
        for section_i, section in enumerate(section_list):
            print(f'''SECTION: {section['name']}''')
            section_name = section['name']
            section_name = text_format(section_name)
            text = f'{chapter_i+1}.{section_i+1} {section_name}'
            h2(pdf, text)
            ### subsection
            subsection_list = section['subsection_list']
            for subsection_i, subsection in enumerate(subsection_list):
                print(f'''SUBSECTION: {subsection['name']}''')
                subsection_name = subsection['name']
                subsection_name = text_format(subsection_name)
                text = f'{chapter_i+1}.{section_i+1}.{subsection_i+1} {subsection_name}'
                h3(pdf, text)
                if qa_len == 'short':
                    text = subsection['merged_answers_short']
                elif qa_len == 'medium':
                    text = subsection['merged_answers_medium']
                pdf.set_font('Helvetica', size=11)
                pdf.x = px_out
                pdf.multi_cell(210 - px_in - px_out, 6, text=f'{text}')
                pdf.ln()
    pdf.output(f'{g.SHOP_FOLDERPATH}/books/tincture-mastery-merged-answers-{qa_len}.pdf')

def txt_merge_answers_gen():
    from fpdf import FPDF
    pdf = FPDF()
    json_filepath = f'{g.SHOP_FOLDERPATH}/books/tincture-mastery.json'
    json_data = io.json_read(json_filepath)
    chapter_list = json_data['chapter_list']
    for chapter_i, chapter in enumerate(chapter_list):
        print(f'''CHAPTER: {chapter['name']}''')
        chapter_name = chapter['name']
        chapter_name = text_format(chapter_name)
        text = f'{chapter_i+1}. {chapter_name}'
        h1(pdf, text)
        ### section
        section_list = chapter['section_list']
        for section_i, section in enumerate(section_list):
            print(f'''SECTION: {section['name']}''')
            section_name = section['name']
            section_name = text_format(section_name)
            text = f'{chapter_i+1}.{section_i+1} {section_name}'
            h2(pdf, text)
            ### subsection
            subsection_list = section['subsection_list']
            for subsection_i, subsection in enumerate(subsection_list):
                print(f'''SUBSECTION: {subsection['name']}''')
                subsection_name = subsection['name']
                subsection_name = text_format(subsection_name)
                text = f'{chapter_i+1}.{section_i+1}.{subsection_i+1} {subsection_name}'
                h3(pdf, text)
                try: text = subsection['merged_answers_short']
                except: continue
                pdf.set_font('Helvetica', size=11)
                pdf.x = px_out
                pdf.multi_cell(210 - px_in - px_out, 6, text=f'{text}')
                pdf.ln()
    pdf.output(f'{g.SHOP_FOLDERPATH}/books/tincture-mastery-merged-answers-short.pdf')

def answer_random_get():
    json_filepath = f'{g.SHOP_FOLDERPATH}/books/tincture-mastery.json'
    json_data = io.json_read(json_filepath)
    chapter_list = json_data['chapter_list']
    chapter = random.choice(chapter_list)
    section_list = chapter['section_list']
    section = random.choice(section_list)
    subsection_list = section['subsection_list']
    subsection = random.choice(subsection_list)
    qa_list = subsection['qa_list']
    qa = random.choice(qa_list)
    answer = qa['answer_long']
    answer = text_format(answer)
    print('################################################################################')
    print(answer)
    print('################################################################################')

def course_ideas_gen():
    json_filepath = f'{g.SHOP_FOLDERPATH}/books/tincture-mastery.json'
    json_data = io.json_read(json_filepath)
    chapter_list = json_data['chapter_list']
    outline_filepath = f'{g.SHOP_FOLDERPATH}/books/tincture-mastery-outline.txt'
    with open(outline_filepath) as f: content = f.read().strip()
    lines = [line for line in content.split('\n') if line.strip() != '']
    random.shuffle(lines)
    lines = '\n'.join(lines[:100])
    prompt = f'''
        Given the list of topics below, I want you to suggest me a list of 15 ideas of valuable teaching materials.
        This material must be in form of mini-courses, checklist, cheat sheet, template, or other easy consumable meterial.
        These courses must be about 2 hour long, easy and fast to consume.
        They must provide quick actionable advice for instant results and gratification.
        They must appeal to a mass market and be beginner friendly.
        These should be so valuable that people would gladly pay a premium price to get them. 
        Give me just the list of ideas and explain in one sentence each what is that idea and why it is a valuable idea.
        Start each idea title with the words "how to". Include between brackets the type of material (course, checklist, etc.)
        Give me only 15 ideas.
        Here are the topics:
        {lines}
    '''
    print(prompt)
    prompt += f'/no_think'
    reply = llm.reply(prompt, model_filepath='')
    if '</think>' in reply:
        reply = reply.split('</think>')[1].strip()

def course_outline_gen(topic):
        # I'm making a mini-course in audio format about the following topic: {topic}
    prompt = f'''
        I'm interested in this:
        {topic}
        Expand on it. Explaing to me how to create a full mini-course of it and all the supporting material that I can offer to people as a "sampler" for free to then have their trust in buying the course.
    '''
    print(prompt)
    prompt += f'/no_think'
    reply = llm.reply(prompt, model_filepath='')
    if '</think>' in reply:
        reply = reply.split('</think>')[1].strip()

def jason_course_outline_gen(topic):
    prompt = f'''
        Identify the top 6 experts on "{topic}", and give me their top 9 strategies. Provide it to me in a list.
    '''
    print(prompt)
    prompt += f'/no_think'
    reply = llm.reply(prompt, model_filepath='')
    if '</think>' in reply:
        reply = reply.split('</think>')[1].strip()
    ###
    prompt = f'''
        Here's a list of experts and their strategies on "{topic}":
        {reply}
        Do you see any duplicate answers repeated from one expert to the next? Give me 9.
    '''
    print(prompt)
    prompt += f'/no_think'
    reply = llm.reply(prompt, model_filepath='')
    if '</think>' in reply:
        reply = reply.split('</think>')[1].strip()
    ###
    prompt = f'''
        Here's a list of overlaps strategies from experts on "{topic}":
        {reply}
        Merge these overlaps into one "universal starter method" distilled from all these experts, so you get a single, non-redundant recipe/checklist.
    '''
    print(prompt)
    prompt += f'/no_think'
    reply = llm.reply(prompt, model_filepath='')
    if '</think>' in reply:
        reply = reply.split('</think>')[1].strip()


'''
how to make your first medicinal herbal tincture
how to choose the right herb for your wellness goals
how to store tinctures for optimal shelf life

'''
# course_ideas_gen()
topic = 'how to make your first medicinal herbal tincture'
# course_outline_gen(topic)

# jason_course_outline_gen(topic)

course_slug = f'tincture-mastery'
if 1:
    start_time = time.time()
    outline_init()
    # answer_gen()
    # pdf_gen('short')
    # pdf_gen('medium')
    # pdf_gen('long')
    # pdf_gen('long-book')
    # answer_merge_gen('short')
    # answer_merge_gen('medium')
    # pdf_merge_answers_gen('medium')
    # answer_random_get()
    delta_time = time.time() - start_time
    print(f'EXECUTION SECONDS: {delta_time}')
    print(f'EXECUTION MINUTES: {delta_time//60}')


        
quit()

