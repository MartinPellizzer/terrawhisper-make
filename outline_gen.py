from lib import llm

prompt = f'''
    I want to make the number one website about medicinal herbs.
    One of its main topic hub is the "Herbs" one, located at domain.com/herbs.html
    I want to be number on in the world for this topic and dominate it.
    To do that i want to use the koray semantic topical authority (STA) methodology and guideline.
    To start give me the outline of the html structure using STA.
    Include only the headings in the outline: H1, H2, H3, etc.
    Reply only with the html code.
    /no_think
'''
html = llm.reply(prompt)
if '</think>' in html:
    html = html.split('</think>')[1].strip()

new_html = html
for i in range(100):
    prompt = f'''
        I want to make the number one website about medicinal herbs.
        One of its main topic hub is the "Herbs" one, located at domain.com/herbs.html
        I want to be number on in the world for this topic and dominate it.
        To do that i want to use the koray semantic topical authority (STA) methodology and guideline.
        I have the following outline in html, and i want you to give it a score and give me advice based on STA to improve it, by adding, subtracting, rearanging, or merging sections together:
        Don't give me html code, only descriptive advices.
        {new_html}
        /no_think
    '''
    advice = llm.reply(prompt)
    if '</think>' in advice:
        advice = advice.split('</think>')[1].strip()

    prompt = f'''
        I want to make the number one website about medicinal herbs.
        One of its main topic hub is the "Herbs" one, located at domain.com/herbs.html
        I want to be number on in the world for this topic and dominate it.
        To do that i want to use the koray semantic topical authority (STA) methodology and guideline.
        I have the following outline in html, and the following advice, and i want you to reply with a fixed version of the outline following the advice.
        The most important thing is that i want to avoid reundancy and duplicate content at all costs, so use the advice to redesign the structure of the outline in a way to avoid writing repetitive content.
        {new_html}
        {advice}
        Reply only with the html code.
        Include only the headings in the outline: H1, H2, H3, etc.
        /no_think
    '''
    new_html = llm.reply(prompt)
    if '</think>' in new_html:
        new_html = new_html.split('</think>')[1].strip()

