from lib import g
from lib import io
from lib import llm
from lib import data
from lib import polish
from lib import components
from lib import sections

model_filepath = '/home/ubuntu/vault-tmp/llm/Qwen3.5-9B-Q8_0.gguf'

def paragraph_format_1N1(text):
    sentences = text.strip().split('. ')
    print(sentences)
    print(len(sentences))
    paragraphs = []
    paragraphs.append(sentences[:1])
    paragraphs.append(sentences[1:-1])
    paragraphs.append(sentences[-1:])
    print(paragraphs)
    print(len(paragraphs))
    paragraphs_html = ''
    for paragraph in paragraphs:
        chunk = '. '.join(paragraph)
        paragraphs_html += f'<p style="margin-bottom: 1.6rem;">{chunk}.</p>'
        paragraphs_html = paragraphs_html.replace('..', '.')
    print(paragraphs_html)
    return paragraphs_html

def paragraph__gen(json_article_filepath, core_entity='learning paths', key='', title='', heading='', brief='', start_text='', regen=False, dispel=False):
    ### llm
    json_article = io.json_read(json_article_filepath, create=True)
    if key not in json_article: json_article[key] = ''
    if regen: json_article[key] = ''
    if dispel: 
        json_article[key] = ''
        io.json_write(json_article_filepath, json_article)
    if not dispel:
        if json_article[key] == '':
            import textwrap
            prompt = textwrap.dedent(f'''
                I have a website about the following central source context: "learning herbal medicine".
                I'm writing an article about the following core entity: "{core_entity}".
                I want you to write the subordinate text for the following title: "{title}". 
                The subordinate text is a detailed paragraph that must be written immediately after the headline. 
                It must follow the BRIEF and it must cover in detail the topics (attributes) mentioned in the ATTRIBUTES.
                It must be the most direct, clear, detailed content possible without fluff.
                It must be at least 5 sentences long.
                Write at least one sentence for each point in the brief.
                Don't give me bold or italicized text. 
                Reply only with the subordinate text.
                Don't write conclusive statements, like those that starts with "ultimately", "in conclusion", "finally", etc.
                {brief}
                {start_text}
            ''').strip()
                # /no_think
                # The subordinate text is the first 5 sentences that must be written immediately after the headline. 
                # Start with the following words: {herb_name_common} 
            print(prompt)
            # reply = llm.reply(prompt)
            reply = llm.reply(prompt, model_filepath)
            if '</think>' in reply:
                reply = reply.split('</think>')[1].strip()
            reply = polish.vanilla(reply)
            json_article[key] = reply
            io.json_write(json_article_filepath, json_article)
            print(json_article_filepath)
    ### html
    paragraph = json_article[key]
    paragraph_formatted = paragraph_format_1N1(paragraph)
    # paragraph_formatted = paragraph
    html = f'''
        <{heading}>{title}</{heading}>
        {paragraph_formatted}
    '''
    return html

def section__gen(json_article_filepath, entity, key='', title='', heading='', brief='', start_text='', regen=False, dispel=False):
    ### llm
    json_article = io.json_read(json_article_filepath, create=True)
    if key not in json_article: json_article[key] = ''
    if regen: json_article[key] = ''
    if dispel: 
        json_article[key] = ''
        io.json_write(json_article_filepath, json_article)
    if not dispel:
        if json_article[key] == '':
            import textwrap
            prompt = textwrap.dedent(f'''
                {brief}
            ''').strip()
            print(prompt)
            reply = llm.reply(prompt, model_filepath)
            if '</think>' in reply:
                reply = reply.split('</think>')[1].strip()
            reply = polish.vanilla(reply)
            json_article[key] = reply
            io.json_write(json_article_filepath, json_article)
            print(json_article_filepath)
    ### html
    paragraph = json_article[key]
    paragraph_formatted = paragraph_format_1N1(paragraph)
    # paragraph_formatted = paragraph
    html = f'''
        <{heading}>{title}</{heading}>
        {paragraph_formatted}
    '''
    return html

def sentence__gen(json_article_filepath, key, title, heading, brief, regen=False, dispel=False):
    ### llm
    json_article = io.json_read(json_article_filepath, create=True)
    if key not in json_article: json_article[key] = ''
    if regen: json_article[key] = ''
    if dispel: 
        json_article[key] = ''
        io.json_write(json_article_filepath, json_article)
    if not dispel:
        if json_article[key] == '':
            import textwrap
            prompt = textwrap.dedent(f'''
                I'm writing an article about the core entity "herbal medicine", which is for a website where the source context is "herbal medicine". 
                I want you to write the subordinate text for a section with the following title: "{title}". 
                The subordinate text is the first 1 sentence that must be written immediately after the headline. 
                The subordinate text must answer in the most direct, clear, detailed way possible without fluff.
                In this you must always reply to the implicit question asked in the section.
                In the following sentences, you give more details.
                Don't give me bold or italicized text. 
                Reply only with the subordinate text.
                Reply with only one sentence.
                BRIEF:
                {brief}
                /no_think
            ''').strip()
                # Start with the following words: {herb_name_common} 
            print(prompt)
            reply = llm.reply(prompt)
            if '</think>' in reply:
                reply = reply.split('</think>')[1].strip()
            reply = polish.vanilla(reply)
            json_article[key] = reply
            io.json_write(json_article_filepath, json_article)
            print(json_article_filepath)
    ### html
    paragraph = json_article[key]
    # paragraph_formatted = paragraph_format_1N1(paragraph)
    paragraph_formatted = paragraph
    html = f'''
        <{heading}>{title}</{heading}>
        <p>
        {paragraph_formatted}
        </p>
    '''
    return html

def learning_herbal_medicine__learning_paths__gen():
    url_slug = f'learning-paths'
    meta_title = f'Herbal Medicine Learning Paths'
    meta_description = 'Explore the Apothecary, Botanist, and Chemist learning paths in herbal medicine. Discover which methodology aligns with your learning style, goals, and experience level to build a sustainable practice.'
    canonical_html = f'''<link rel="canonical" href="https://terrawhisper.com/{url_slug}.html">'''

    ########################################
    # json
    ########################################
    json_article_filepath = f'''{g.DATABASE_FOLDERPATH}/json/{url_slug}.json'''
    json_article = io.json_read(json_article_filepath, create=True)
    json_article['url'] = url_slug
    io.json_write(json_article_filepath, json_article)

    regen_function = False
    dispel_function = False

    html_article = ''
    html_article += sentence__gen(
            json_article_filepath, 
            key=f'''
intro
            ''', title=f'''
Choosing Your Herbalism Curriculum: The Three Learning Paths Explained
            ''', 
            heading=f'''
h1
            '''.strip(),
            brief=f'''
            ''', 
            regen=regen_function, dispel=dispel_function
    )
    ######################################## 
    html_article += sentence__gen(
            json_article_filepath, 
            key=f'''
definition
            ''',
            title=f'''
What Are Learning Paths in Herbal Medicine?
            ''', 
            heading=f'''
h2
            '''.strip(),
            brief=f'''
            ''', 
            regen=regen_function, dispel=dispel_function
    )
    ###
    html_article += sentence__gen(
            json_article_filepath, 
            key=f'''
definition_0000
            ''',
            title=f'''
Why Herbal Medicine Can Be Learned in Different Ways
            ''', 
            heading=f'''
h3
            '''.strip(),
            brief=f'''
            ''', 
            regen=regen_function, dispel=dispel_function
    )
    ###
    html_article += sentence__gen(
            json_article_filepath, 
            key=f'''
definition_0001
            ''',
            title=f'''
The Three Core Approaches to Studying Herbalism
            ''', 
            heading=f'''
h3
            '''.strip(),
            brief=f'''
            ''', 
            regen=regen_function, dispel=dispel_function
    )
    ######################################## 
    html_article += sentence__gen(
            json_article_filepath, 
            key=f'''
overview
            ''',
            title=f'''
The 3 Core Learning Paths in Herbal Medicine
            ''', 
            heading=f'''
h2
            '''.strip(),
            brief=f'''
            ''', 
            regen=regen_function, dispel=dispel_function
    )
    ### 
    html_article += sentence__gen(
            json_article_filepath, 
            key=f'''
overview_0000
            ''',
            title=f'''
Overview of the Three Herbal Learning Paths
            ''', 
            heading=f'''
h3
            '''.strip(),
            brief=f'''
            ''', 
            regen=regen_function, dispel=dispel_function
    )

    ######################################## 
    if 0:
        html_article += paragraph__gen(
                json_article_filepath, 
                key=f'''
    apothecary
                ''',
                title=f'''
    The Apothecary Path: Learning Herbal Medicine Through Making Remedies
                ''', 
                heading=f'''
    h2
                '''.strip(),
                brief=f'''
    Definition of the Apothecary learning approach
    Why hands-on practice is the starting point
    The importance of preparation methods in herbal traditions
    How making remedies teaches herbal properties
    Practical outcomes of this learning style
                ''', 
                regen=regen_function, dispel=dispel_function
        )
    html_article += f'''
    <h2>The Apothecary Path: Learning Herbal Medicine Through Making Remedies</h2>
    <img src="/images/home/apothecary-path.jpg" width=512 style="margin-bottom: 1.6rem;">
    <p>The Apothecary Path refers to a method of learning herbal medicine by actively creating remedies, which bridges theory and practice.</p>
    <p>This approach begins with hands-on practice because preparing herbs and formulations develops essential skills and deepens understanding. Preparation methods are central to herbal traditions, as they influence the potency and effectiveness of remedies. Making remedies allows learners to observe how different herbs interact and how their properties are revealed through use.</p>
    <p>This learning style leads to tangible outcomes, such as personalized treatments and a deeper connection to the medicinal properties of plants.</p>
    <p>The following list shows the most common types of herbal preparations used in the apothecary learning path.</p>
    <ul>
        <li>Herbal teas and infusions</li>
        <li>Tinctures and glycerites</li>
        <li>Herbal oils</li>
        <li>Salves and balms</li>
        <li>Syrups and oxymels</li>
    </ul>
    '''
    ###
    if 0:
        html_article += paragraph__gen(
                json_article_filepath, 
                key=f'''
    apothecary_who
                ''',
                title=f'''
    Who the Apothecary Path Is For
                ''', 
                heading=f'''
    h3
                '''.strip(),
                brief=f'''
    Characteristics of hands-on learners
    Typical student profiles:
    DIY herbalists
    homesteaders
    home remedy makers
    Motivation factors behind this learning style
    Learning preferences: experimentation and crafting
    Real-world goals of these learners
                ''', 
                regen=regen_function, dispel=dispel_function
        )
    html_article += f'''
<h3>Who the Apothecary Path Is For</h3>
<p>
This path is ideal for hands-on learners who thrive through experimentation and crafting.
</p>
<p>
This path suits DIY herbalists, homesteaders, and home remedy makers who seek practical skills in creating and using herbal medicine. These learners are motivated by the desire to grow, prepare, and apply their own remedies. They prefer learning by doing, rather than through passive instruction.
</p>
<p>
Their real-world goals include self-sufficiency, wellness, and a deeper connection to natural healing practices.
</p>
<p>The following list describes the types of learners who are typically drawn to the apothecary approach.</p>
<ul>
    <li>DIY herbal learners</li>
    <li>Homesteaders</li>
    <li>Natural health enthusiasts</li>
    <li>People building a home apothecary</li>
</ul>
    '''
    if 0:
        html_article += paragraph__gen(
                json_article_filepath, 
                key=f'''
    apothecary_0000
                ''',
                title=f'''
    How Apothecary Learners Study Herbal Medicine
                ''', 
                heading=f'''
    h3
                '''.strip(),
                brief=f'''
    Learning through preparation techniques
    Observation of herb effects through use
    Trial-and-error formulation
    Building a home apothecary
    Developing intuition about herbs through practice
                ''', 
                regen=regen_function, dispel=dispel_function
        )
        html_article += f'''
    <ol>
    <li>Learn a preparation method.</li>
    <li>Choose suitable herbs.</li>
    <li>Create a remedy.</li>
    <li>Observe results.</li>
    <li>Refine the formulation.</li>
    </ol>
        '''
    html_article += f'''
<h3>
How Apothecary Learners Study Herbal Medicine 
</h3>
<p>
Apothecary learners study herbal medicine by mastering the preparation techniques required to create effective remedies.
</p>
<p>
They observe the effects of herbs in real-world applications to understand their properties and interactions. Through trial and error, they refine formulations to achieve desired therapeutic outcomes. Establishing a personal home apothecary allows them to experiment and refine their skills systematically.
</p>
<p>
Practicing regularly helps them develop an intuitive understanding of herbs and their uses.
</p>
<p>The following steps outline how students typically learn herbal medicine through practical remedy making.</p>
<ol>
    <li>Learn a preparation method</li>
    <li>Choose suitable herbs</li>
    <li>Create a remedy</li>
    <li>Observe results</li>
    <li>Refine the formulation</li>
</ol>
</p>
    '''
    if 0:
        html_article += paragraph__gen(
                json_article_filepath, 
                key=f'''
    apothecary_0001
                ''',
                title=f'''
    Typical Learning Progression for the Apothecary Path
                ''', 
                heading=f'''
    h3
                '''.strip(),
                brief=f'''
    Herbal teas and infusions
    Tinctures and glycerites
    Oils, salves, and balms
    Syrups and oxymels
    Creating simple herbal formulas
                ''', 
                regen=regen_function, dispel=dispel_function
        )
        html_article += f'''
    <ol>
    <li>Herbal teas and infusions</li>
    <li>Tinctures and glycerites</li>
    <li>Herbal oils and salves</li>
    <li>Syrups and oxymels</li>
    <li>Simple herbal formulas</li>
    </ol>
        '''
    html_article += f'''
<h3>
Typical Learning Progression for the Apothecary Path 
</h3>
<p>
The Apothecary Path typically begins with foundational knowledge of herbal teas and infusions, which introduce students to basic herb preparation and extraction methods.
</p>
<p>
Next, learners move on to tinctures and glycerites, mastering alcohol and glycerin-based formulations for concentrated herbal extracts. Following this, students explore oils, salves, and balms, learning essential techniques for creating topical applications. Syrups and oxymels come next, focusing on sweetened herbal preparations for internal use.
</p>
<p>
Finally, students create simple herbal formulas by combining various preparations to address specific health needs.
</p>
<p>The following sequence shows the common order in which apothecary learners develop remedy-making skills.</p>
<ol>
    <li>Herbal teas and infusions</li>
    <li>Tinctures and glycerites</li>
    <li>Herbal oils and salves</li>
    <li>Syrups and oxymels</li>
    <li>Simple herbal formulas</li>
</ol>
    '''
    if 0:
        html_article += paragraph__gen(
                json_article_filepath, 
                key=f'''
    apothecary_0002
                ''',
                title=f'''
    Common Questions Asked by Apothecary Learners
                ''', 
                heading=f'''
    h3
                '''.strip(),
                brief=f'''
    What remedies can I make with common herbs?
    Which preparation method works best for each herb?
    How long should remedies steep or extract?
    How can I combine herbs into formulas?
    How should remedies be stored and used?
                ''', 
                regen=regen_function, dispel=dispel_function
        )
        html_article += f'''
    <dl>
    <dt>What remedies can I make with common herbs?</dt>
    <dd>Beginners usually start with teas, tinctures, and simple salves.</dd>
    <dt>Which preparation works best for each herb?</dt>
    <dd>Different herbs extract better in water, alcohol, or oil.</dd>
    <dt>How should herbal remedies be stored?</dt>
    <dd>Most preparations are stored in dark glass containers away from heat and light.</dd>
    </dl>
        '''
    html_article += f'''
<h3>
Common Questions Asked by Apothecary Learners 
</h3>
<dl>
<dt style="font-weight: 700; margin-bottom: 0.8rem;">What remedies can I make with common herbs?</dt>
<dd style="margin-bottom: 1.6rem;">Common kitchen and garden herbs can be turned into simple remedies such as herbal teas, tinctures, infused oils, syrups, and salves depending on the plant and the desired effect.</dd>
<dt style="font-weight: 700; margin-bottom: 0.8rem;">Which preparation method works best for each herb?</dt>
<dd style="margin-bottom: 1.6rem;">The best preparation method depends on the plant’s chemical properties, with delicate leaves often suited for teas while tougher roots, barks, and resins typically extract better in alcohol tinctures or long infusions.</dd>
<dt style="font-weight: 700; margin-bottom: 0.8rem;">How long should remedies steep or extract?</dt>
<dd style="margin-bottom: 1.6rem;">Herbal teas usually steep for 5–15 minutes, while stronger infusions may steep for several hours and tinctures typically extract for 2–6 weeks.</dd>
<dt style="font-weight: 700; margin-bottom: 0.8rem;">How can I combine herbs into formulas?</dt>
<dd style="margin-bottom: 1.6rem;">Herbal formulas are created by combining complementary herbs that support the same health goal while balancing primary active herbs with supportive or harmonizing plants.</dd>
<dt style="font-weight: 700; margin-bottom: 0.8rem;">How should remedies be stored and used?</dt>
<dd>Most herbal remedies should be stored in airtight containers away from heat, light, and moisture and used according to recommended dosage guidelines.</dd>
</dl>
'''

    html_article += paragraph__gen(
            json_article_filepath, 
            key=f'''
apothecary_0003
            ''',
            title=f'''
Strengths of the Apothecary Learning Approach
            ''', 
            heading=f'''
h3
            '''.strip(),
            brief=f'''
Rapid practical skill development
Immediate application of knowledge
Strong formulation abilities
High learner motivation
Tangible results from early study
            ''', 
            regen=regen_function, dispel=dispel_function
    )
    html_article += f'''
<ul>
<li>Rapid practical results</li>
<li>Strong formulation skills</li>
<li>Hands-on learning</li>
<li>High learner motivation</li>
</ul>
    '''
    html_article += paragraph__gen(
            json_article_filepath, 
            key=f'''
apothecary_0004
            ''',
            title=f'''
Challenges of the Apothecary Path
            ''', 
            heading=f'''
h3
            '''.strip(),
            brief=f'''
Limited plant identification knowledge
Risk of fragmented herbal understanding
Difficulty understanding herb mechanisms
Overreliance on recipes
Need for complementary botanical or scientific study
            ''', 
            regen=regen_function, dispel=dispel_function
    )
    html_article += f'''
<ul>
<li>Limited botanical knowledge</li>
<li>Fragmented understanding of herbs</li>
<li>Less focus on plant identification</li>
<li>Possible reliance on recipes</li>
</ul>
    '''
    html_article += paragraph__gen(
            json_article_filepath, 
            key=f'''
apothecary_0004
            ''',
            title=f'''
Difficulty Level and Skills Developed
            ''', 
            heading=f'''
h3
            '''.strip(),
            brief=f'''
Accessibility for beginners
Manual skills developed
Basic herbal knowledge gained
Practical remedy-making confidence
Typical progression toward deeper herbal study
            ''', 
            regen=regen_function, dispel=dispel_function
    )
    html_article += f'''
<table>
<tr>
<th>Difficulty</th>
<th>Main Skills Developed</th>
</tr>
<tr>
<td>Beginner → Intermediate</td>
<td>Remedy preparation, herbal formulation, home apothecary building</td>
</tr>
</table>
    '''

    ######################################## 
    html_article += sentence__gen(
            json_article_filepath, 
            key=f'''
botanist
            ''',
            title=f'''
The Botanist Path: Learning Herbal Medicine Through Plants and Nature
            ''', 
            heading=f'''
h2
            '''.strip(),
            brief=f'''
            ''', 
            regen=regen_function, dispel=dispel_function
    )

    ######################################## 
    html_article += sentence__gen(
            json_article_filepath, 
            key=f'''
chemist
            ''',
            title=f'''
The Chemist Path: Learning Herbal Medicine Through Science and Mechanisms
            ''', 
            heading=f'''
h2
            '''.strip(),
            brief=f'''
            ''', 
            regen=regen_function, dispel=dispel_function
    )

    ######################################## 
    html_article += sentence__gen(
            json_article_filepath, 
            key=f'''
compare
            ''',
            title=f'''
Comparing the Three Herbal Medicine Learning Paths
            ''', 
            heading=f'''
h2
            '''.strip(),
            brief=f'''
            ''', 
            regen=regen_function, dispel=dispel_function
    )

    ######################################## 
    html_article += sentence__gen(
            json_article_filepath, 
            key=f'''
choose
            ''',
            title=f'''
How to Choose the Right Herbal Medicine Learning Path
            ''', 
            heading=f'''
h2
            '''.strip(),
            brief=f'''
            ''', 
            regen=regen_function, dispel=dispel_function
    )

    ######################################## 
    html_article += sentence__gen(
            json_article_filepath, 
            key=f'''
integrate
            ''',
            title=f'''
Why Most Herbalists Eventually Combine All Three Learning Paths
            ''', 
            heading=f'''
h2
            '''.strip(),
            brief=f'''
            ''', 
            regen=regen_function, dispel=dispel_function
    )

    ######################################## 
    html_article += sentence__gen(
            json_article_filepath, 
            key=f'''
start
            ''',
            title=f'''
Where to Start Your Herbal Medicine Learning Journey
            ''', 
            heading=f'''
h2
            '''.strip(),
            brief=f'''
            ''', 
            regen=regen_function, dispel=dispel_function
    )

    html_article = sections.toc(html_article)

    ###
    head_html = components.html_head(
        meta_title, meta_description, css='/styles-herb-monograph.css', canonical=canonical_html
    )
    import textwrap
    html = textwrap.dedent(f''' 
        <!DOCTYPE html>
        <html lang="en">
        {head_html}
        <body>
            {sections.header_default()}
            {sections.breadcrumbs_new(url_slug)}
            <main>
                <article class="container-md article">
                    {html_article}
                </article>
            </main>
            {sections.footer()}
        </body>
        </html>
    ''').strip()
    html_filepath = f'''{g.website_folderpath}/{url_slug}.html'''
    with open(html_filepath, 'w') as f: f.write(html)

def learning_herbal_medicine__learning_paths__apothecary__gen():
    url_slug = f'learning-paths/apothecary'
    meta_title = f'The Apothecary Path: A Practical Methodology for Mastering Herbalism'
    meta_description = ''
    canonical_html = f'''<link rel="canonical" href="https://terrawhisper.com/{url_slug}.html">'''
    core_entity = 'the apothecary path'

    ########################################
    # json
    ########################################
    json_article_filepath = f'''{g.DATABASE_FOLDERPATH}/json/{url_slug}.json'''
    json_article = io.json_read(json_article_filepath, create=True)
    json_article['url'] = url_slug
    io.json_write(json_article_filepath, json_article)

    regen_function = False
    dispel_function = False

    '''
    <li><a href="" style="text-transform: capitalize;">infusions</a></li>
    <li><a href="" style="text-transform: capitalize;">decoctions</a></li>
    <li><a href="" style="text-transform: capitalize;">herbal powders</a></li>
    <li><a href="" style="text-transform: capitalize;">fresh vs dried herbs</a></li>
    <li><a href="" style="text-transform: capitalize;">preparation ratios</a></li>
    <li><a href="" style="text-transform: capitalize;">dosing basics</a></li>
    '''
    _sections = [
        {
            'id': 'intro',
            'heading': 'h1',
            'text': 'The Apothecary Path: A Hands-On Method for Learning Herbal Medicine',
            'brief': 'Define the core entity "The Apothecary Path" as the primary learning route for individuals who prioritize immediate preparation and formulation over theoretical botany.',
            'html_after': '[toc]',
        },
        {
            'id': 'what',
            'heading': 'h2',
            'text': 'What Is the Apothecary Path?',
            'brief': f'''
* definition of the apothecary learning approach
* relationship between herbalism and remedy making
* difference between **study-first vs practice-first learning**
* origin of the apothecary tradition
* role of experimentation in herbal learning
* what “practical herbalism” means
* the core philosophy of learning through preparation
            ''',
            'html_after': '',
        },
        {
            'id': 'who',
            'heading': 'h2',
            'text': 'Who the Apothecary Path Is For',
            'brief': f'''
* DIY learners
* homesteaders
* natural health enthusiasts
* people building a home apothecary
* beginner herbalists
* hands-on learners
* self-taught herbal medicine practitioners
            ''',
            'html_after': f'''
<p>The following list shows the people who are most interested in this learning path.</p>
<ul>
<li>DIY learners</li>
<li>homesteaders</li>
<li>natural health enthusiasts</li>
<li>people building a home apothecary</li>
<li>beginner herbalists</li>
<li>hands-on learners</li>
<li>self-taught herbal medicine practitioners</li>
</ul>
''',
            'regen': regen_function,
            'start_text': 'This path is for ',
        },
        {
            'id': 'how',
            'heading': 'h2',
            'text': 'How the Apothecary Path Works',
            'brief': f'''
* learning by making remedies
* incremental knowledge building
* feedback through experimentation
* practical herbal skill development
* intuitive formulation skills
* experiential plant understanding
            ''',
            'regen': regen_function,
            'html_after': '',
        },
        {
            'id': 'skills',
            'heading': 'h2',
            'text': 'The Core Skills of the Apothecary Herbalist',
            'brief': f'''
* ingredient selection
* herbal preparation techniques
* extraction methods
* dosage awareness
* storage and preservation
* formulation
* plant identification basics
            ''',
            'regen': regen_function,
            'html_after': f'''
<p>The following list shows the core skills of the apothecary herbalist.</p>
<ul>
<li>herbal preparation techniques</li>
<li>formulation</li>
<li>ingredient selection</li>
<li>plant identification basics</li>
<li>extraction methods</li>
<li>dosage awareness</li>
<li>storage and preservation</li>
</ul>
''',
            'start_text': 'The apothecary herbalist learns core skills ',
        },
        {
            'id': 'stages',
            'heading': 'h2',
            'text': 'The Learning Stages of the Apothecary Path',
            'brief': f'''
Stage 1: Foundations of Herbal Remedy Making
Stage 2: Learning Through Simple Herbal Preparations
Stage 3: Liquid Herbal Extracts
Stage 4: Oil-Based Herbal Preparations
Stage 5: Topical Herbal Remedies
Stage 6: Syrups and Sweet Preparations
Stage 7: Building Simple Herbal Formulas
Stage 8: Understanding the Herbs Behind the Remedies
Stage 9: Building a Personal Home Apothecary
Stage 10: Advanced Apothecary Skills
Stage 11: Mastery Through Practice and Observation
            ''',
            'regen': regen_function,
            'html_after': f'''
''',
            'start_text': 'In the first stage of this learning path',
        },
        {
            'id': 'stage_1',
            'heading': 'h3',
            'text': 'Stage 1: Foundations of Herbal Remedy Making',
            'brief': f'''
* basic herbal medicine concepts
* herbs vs pharmaceuticals
* herbal safety basics
* herbal actions
* basic terminology
* preparation categories
* simple herbal uses
            ''',
            'regen': regen_function,
            'html_after': f'''
<p>The resources to complete this step are coming soon.</p>
''',
            'start_text': '',
        },
        {
            'id': 'stage_2',
            'heading': 'h3',
            'text': 'Stage 2: Learning Through Simple Herbal Preparations',
            'brief': f'''
* herbal teas
* infusions
* decoctions
* herbal powders
* fresh vs dried herbs
* preparation ratios
* dosing basics
            ''',
            'regen': regen_function,
            'html_after': f'''
<p>Use the following resources to complete Stage 2.</p>
<ol>
<li><a href="/preparations/infusions.html" style="text-transform: capitalize;">Herbal Infusions: What They Are and How to Make Them</a></li>
</ol>
<p>More resources to master this step are coming soon.</p>
''',
            'start_text': '',
        },
        {
            'id': 'stage_3',
            'heading': 'h3',
            'text': 'Stage 3: Liquid Herbal Extracts',
            'brief': f'''
* tinctures
* glycerites
* alcohol extraction
* menstruum ratios
* shelf life
* extraction strengths
* alcohol vs glycerin extraction
            ''',
            'regen': regen_function,
            'html_after': f'''
<p>The resources to complete this step are coming soon.</p>
            ''',
            'start_text': '',
        },
        {
            'id': 'stage_4',
            'heading': 'h3',
            'text': 'Stage 4: Oil-Based Herbal Preparations',
            'brief': f'''
* infused oils
* oil infusion methods
* solar infusion
* heat infusion
* oil shelf life
* carrier oils
* lipid extraction
            ''',
            'regen': regen_function,
            'html_after': f'''
<p>The resources to complete this step are coming soon.</p>
            ''',
            'start_text': '',
        },
        {
            'id': 'stage_5',
            'heading': 'h3',
            'text': 'Stage 5: Topical Herbal Remedies',
            'brief': f'''
* salves
* balms
* herbal creams
* herbal ointments
* beeswax ratios
* skin applications
* topical herbal safety
            ''',
            'regen': regen_function,
            'html_after': f'''
<p>The resources to complete this step are coming soon.</p>
            ''',
            'start_text': '',
        },
        {
            'id': 'stage_6',
            'heading': 'h3',
            'text': 'Stage 6: Syrups and Sweet Preparations',
            'brief': f'''
* herbal syrups
* honey extractions
* oxymels
* electuaries
* cough remedies
* immune tonics
* flavor balancing
            ''',
            'regen': regen_function,
            'html_after': f'''
<p>The resources to complete this step are coming soon.</p>
            ''',
            'start_text': '',
        },
        {
            'id': 'stage_7',
            'heading': 'h3',
            'text': 'Stage 7: Building Simple Herbal Formulas',
            'brief': f'''
* single herb vs formula
* synergy between herbs
* herbal ratios
* combining actions
* flavor balance
* formulation intuition
            ''',
            'regen': regen_function,
            'html_after': f'''
<p>The resources to complete this step are coming soon.</p>
            ''',
            'start_text': '',
        },
        {
            'id': 'stage_8',
            'heading': 'h3',
            'text': 'Stage 8: Understanding the Herbs Behind the Remedies',
            'brief': f'''
* plant constituents
* herbal energetics
* herbal actions
* plant families
* plant parts used
* ecological harvesting
* materia medica basics
            ''',
            'regen': regen_function,
            'html_after': f'''
<p>The resources to complete this step are coming soon.</p>
            ''',
            'start_text': '',
        },
        {
            'id': 'stage_9',
            'heading': 'h3',
            'text': 'Stage 9: Building a Personal Home Apothecary',
            'brief': f'''
* apothecary organization
* jar storage
* labeling systems
* remedy shelf life
* inventory management
* core herbal toolkit
            ''',
            'regen': regen_function,
            'html_after': f'''
<p>The resources to complete this step are coming soon.</p>
            ''',
            'start_text': '',
        },
        {
            'id': 'stage_10',
            'heading': 'h3',
            'text': 'Stage 10: Advanced Apothecary Skills',
            'brief': f'''
* formulation refinement
* complex formulas
* seasonal remedies
* personalized remedies
* clinical reasoning
* herb compatibility
            ''',
            'regen': regen_function,
            'html_after': f'''
<p>The resources to complete this step are coming soon.</p>
            ''',
            'start_text': '',
        },
        {
            'id': 'stage_11',
            'heading': 'h3',
            'text': 'Stage 11: Mastery Through Practice and Observation',
            'brief': f'''
* herbal journaling
* experimentation
* observing results
* refining formulas
* herbal intuition
* long-term learning
            ''',
            'regen': regen_function,
            'html_after': f'''
<p>The resources to complete this step are coming soon.</p>
            ''',
            'start_text': '',
        },

        {
            'id': 'results',
            'heading': 'h2',
            'text': 'What You Can Make on the Apothecary Path',
            'brief': f'''
* sleep teas
* digestive tinctures
* herbal salves
* immune syrups
* herbal bitters
* herbal oils
* everyday remedies
            ''',
            'regen': regen_function,
            'html_after': f'''
            ''',
            'start_text': '',
        },
        {
            'id': 'pros',
            'heading': 'h2',
            'text': 'Strengths of the Apothecary Learning Method',
            'brief': f'''
* fast practical results
* high motivation
* intuitive formulation
* strong remedy familiarity
* experiential learning
            ''',
            'regen': regen_function,
            'html_after': f'''
            ''',
            'start_text': '',
        },
        {
            'id': 'cons',
            'heading': 'h2',
            'text': 'Weaknesses and Limitations of the Apothecary Path',
            'brief': f'''
* fragmented theoretical knowledge
* lack of botanical depth
* risk of incomplete plant understanding
* limited diagnostic framework
            ''',
            'regen': regen_function,
            'html_after': f'''
            ''',
            'start_text': '',
        },
        {
            'id': 'pitfalls',
            'heading': 'h2',
            'text': 'How to Avoid the Common Pitfalls of the Apothecary Path',
            'brief': f'''
* studying herbs alongside remedies
* building a materia medica
* learning plant identification
* documenting formulas
* expanding plant knowledge
            ''',
            'regen': regen_function,
            'html_after': f'''
            ''',
            'start_text': '',
        },
        {
            'id': 'tools',
            'heading': 'h2',
            'text': 'Essential Tools for the Herbal Apothecary',
            'brief': f'''
* glass jars
* tincture bottles
* droppers
* scales
* measuring tools
* strainers
* herb grinders
            ''',
            'regen': regen_function,
            'html_after': f'''
            ''',
            'start_text': '',
        },
        {
            'id': 'cta',
            'heading': 'h2',
            'text': 'How to Start the Apothecary Path Today',
            'brief': f'''
* beginner remedies
* first herbs to buy
* starter apothecary kit
* beginner formulas
* first learning projects
            ''',
            'regen': regen_function,
            'html_after': f'''
            ''',
            'start_text': '',
        },
        {
            'id': 'faq',
            'heading': 'h2',
            'text': 'Frequently Asked Questions About the Apothecary Path',
            'brief': f'''
What Is the First Remedy a Beginner Should Make?
How Many Herbs Should a Beginner Start With?
Do You Need a Garden to Follow the Apothecary Path?
Is the Apothecary Path Safe for Beginners?
            ''',
            'regen': regen_function,
            'html_after': f'''
            ''',
            'start_text': '',
        },
        {
            'id': 'related',
            'heading': 'h2',
            'text': 'Related Herbal Learning Paths',
            'brief': f'''
* the botanical path
* the clinical herbalist path
* the traditional herbalist path
* the intuitive herbalist path
* comparison of herbal learning methods
            ''',
            'regen': regen_function,
            'html_after': f'''
            ''',
            'start_text': '',
        },
        {
            'id': 'recap',
            'heading': 'h2',
            'text': 'The Complete Curriculum of the Apothecary Herbalist',
            'brief': f'''
* beginner skills
* intermediate skills
* advanced skills
* mastery milestones
* lifelong herbal practice
            ''',
            'regen': regen_function,
            'html_after': f'''
            ''',
            'start_text': '',
        },

    ]


    html_article = ''

    for section in _sections:
        if 'regen' in section: _regen = section['regen']
        else: _regen = regen_function
        if 'start_text' in section: _start_text = f'''Start the reply with the following words: {section['start_text']}'''
        else: _start_text = ''
        html_article += paragraph__gen(
                json_article_filepath, 
                core_entity=core_entity,
                key=section['id'],
                title=section['text'],
                heading=section['heading'],
                brief=section['brief'],
                start_text=_start_text,
                regen=_regen, dispel=dispel_function,
        )
        if section['html_after'] != '':
            html_article += section['html_after']


    # print(html_article)
    ###
    html_article = sections.toc(html_article)
    # print('###########################################################3')
    # print(html_article)

    ###
    head_html = components.html_head(
        meta_title, meta_description, css='/styles-herb-monograph.css', canonical=canonical_html
    )
    import textwrap
    html = textwrap.dedent(f''' 
        <!DOCTYPE html>
        <html lang="en">
        {head_html}
        <body>
            {sections.header_default()}
            {sections.breadcrumbs_new(url_slug)}
            <main>
                <article class="container-md article">
                    {html_article}
                </article>
            </main>
            {sections.footer()}
        </body>
        </html>
    ''').strip()
    html_filepath = f'''{g.website_folderpath}/{url_slug}.html'''
    io.folder_create_from_filepath(html_filepath)
    with open(html_filepath, 'w') as f: f.write(html)

def preparations__preparation__gen(data):
    entity = data['entity']
    entity_singular = data['entity_singular']
    preparation_steps = data['preparation_steps']
    if 'preparation_info' in data: 
        preparation_info = f'''
            Additional context: {data['preparation_info']}
        '''
    else:
        preparation_info = ''
    
    entity_slug = polish.sluggify(entity)
    url_slug = f'preparations/{entity_slug}'
    meta_title = f'{entity} in Herbal Medicine'
    meta_description = ''
    canonical_html = f'''<link rel="canonical" href="https://terrawhisper.com/{url_slug}.html">'''

    ########################################
    # json
    ########################################
    json_article_filepath = f'''{g.DATABASE_FOLDERPATH}/json/{url_slug}.json'''
    json_article = io.json_read(json_article_filepath, create=True)
    json_article['url'] = url_slug
    io.json_write(json_article_filepath, json_article)

    if 0:
        curated_info = ''
        if preparation_steps == '':
            import textwrap
            prompt = textwrap.dedent(f'''
    I have a website about the following central source context: "learning herbal medicine".
    Write the procedure in 5 steps to make the following herbal preparation: "{entity}".
    Give only one action per step.
    Use the following information if applicable:
    - Optimal water temperature: 80 degree celsius
            ''').strip()
            print(prompt)
            reply = llm.reply(prompt, model_filepath)
            if '</think>' in reply:
                reply = reply.split('</think>')[1].strip()

    '''
    H1
    [Preparation Name]: Definition, Preparation Method, and Uses in Herbal Medicine
    H2
    What Is an Herbal [Preparation Name]?
    H2
    How the [Preparation Name] Extraction Process Works
    H2
    How to Prepare an Herbal [Preparation Name] (Step-by-Step)
    H3
    Ingredients and Equipment Needed
    H3
    Step-by-Step Preparation Process
    H3
    Recommended Ratios, Time, and Temperature
    H2
    Best Herbs and Plant Parts for [Preparation Name] Preparations
    H2
    [Preparation Name] vs Other Herbal Preparations
    H2
    When to Use [Preparation Name] in Herbal Practice
    H2
    Safety Considerations and Best Practices
    H2
    The Role of [Preparation Name] in Traditional Herbal Medicine
    '''
    regen_function = False
    dispel_function = False

    prompt_article_title = f'''
Write the section for an article titled: "{entity}: Definition, Method, and Uses in Herbal Medicine
    '''
    prompt_article_writing_rules = f'''
Writing rules:
- Write 4–6 concise sentences.
- Use clear factual statements and avoid filler language.
- Maintain an educational tone suitable for beginner herbalists.
Do not include headings or formatting, only the paragraph text.
    '''

    _sections_new = [
        {
            'id': 'intro',
            'hierarchy': 'h1',
            'heading': f'''
                {entity}: Definition, Method, and Uses in Herbal Medicine
            ''',
            'brief': f'''
                {prompt_article_title}
                {entity}: Definition, Method, and Uses in Herbal Medicine
                Brief
                The introduction must immediately satisfy definition + purpose + procedural framing in the first 2–3 sentences.
                Explain what the preparation is, how it extracts medicinal compounds, and when it is typically used.
                Include:
                the extraction principle (water, alcohol, oil, heat, etc.)
                plant parts commonly used
                the main advantage of the preparation
                Example structure:
                Sentence 1 → definition
                Sentence 2 → extraction mechanism
                Sentence 3 → typical herbs or plant parts used
                Sentence 4 → when this preparation is preferred
                This paragraph establishes entity identity and topical salience, which strongly influences retrieval probability.
                {prompt_article_writing_rules}
            ''',
            'html_after': '[toc]',
            'regen': regen_function,
        },
        {
            'id': 'mechanism',
            'hierarchy': 'h2',
            'heading': f'''
                What Is an Herbal {entity_singular}?
            ''',
            'brief': f'''
                {prompt_article_title}
                Intent covered: definition
                Brief
                Provide a clear conceptual definition of the preparation method as used in herbal medicine.
                Explain:
                the basic idea of the preparation
                what type of solvent or medium is used
                the types of plant materials typically processed
                the goal of the preparation (extracting phytochemicals)
                Clarify how this preparation fits within the broader category of herbal preparations.
                Avoid describing exact steps here. Focus purely on what the preparation is and why it exists.
                {preparation_info}
                {prompt_article_writing_rules}
            ''',
            'regen': regen_function,
        },
        {
            'id': 'procedure',
            'hierarchy': 'h2',
            'heading': f'''
                How the {entity_singular} Extraction Process Works
                How to Prepare an Herbal {entity} (Step-by-Step)
            ''',
            'brief': f'''
                {prompt_article_title}
                Intent covered: mechanism / scientific understanding
                Brief
                Explain how the extraction process works at a functional level.
                Cover:
                the solvent used (water, alcohol, oil)
                how temperature, time, or solvent polarity affect extraction
                which types of plant compounds are usually extracted
                Explain why this preparation works better for certain plant parts.
                Examples:
                leaves
                flowers
                roots
                bark
                seeds
                This section builds conceptual understanding so readers know why the preparation method exists, not just how to perform it.
                {preparation_info}
                {prompt_article_writing_rules}
            ''',
            'regen': regen_function,
        },

        {
            'id': 'procedure',
            'hierarchy': 'h2',
            'heading': f'''
                How to Prepare an Herbal {entity_singular} (Step-by-Step)
            ''',
            'brief': f'''
                {prompt_article_title}
                Intent covered: dominant procedural intent
                Content weight: largest section in the article
                Brief (What to write here)
                Begin this section with a short introductory passage (2–4 sentences) that explains the overall preparation process before detailing the individual steps. This introduction should summarize how the preparation works, what variables influence it, and what the reader will learn in the following subsections.
                Specifically, this introductory text should:
                • Explain that the preparation involves extracting plant compounds using a specific solvent and process (heat, alcohol, oil, soaking, etc.).
                • Mention the key variables that determine the final preparation, such as herb quantity, solvent ratio, temperature, and extraction time.
                • Clarify that the following subsections will guide the reader through ingredients, equipment, preparation steps, and optimal conditions.
                The goal is to create a procedural overview so both users and search engines understand that this section contains the complete method for preparing the herbal extract.
                Avoid listing detailed steps here; instead, provide a concise procedural summary that prepares the reader for the structured instructions in the H3 subsections.
                {preparation_info}
                {prompt_article_writing_rules}
            ''',
            'regen': regen_function,
        },
        {
            'id': 'procedure__ingredients',
            'hierarchy': 'h3',
            'heading': f'''
                Ingredients and Equipment Needed
            ''',
            'brief': f'''
                {prompt_article_title}
                Brief
                Ingredients and Equipment Needed
                List and explain the essential components required to perform the preparation.
                Cover:
                plant material (fresh or dried herbs)
                extraction medium (water, alcohol, oil)
                preparation tools (jar, pot, strainer, etc.)
                Explain why each item is necessary and mention practical alternatives where appropriate.
                {preparation_info}
                {prompt_article_writing_rules}
            ''',
            'regen': regen_function,
        },
        {
            'id': 'procedure__herbs',
            'hierarchy': 'h3',
            'heading': f'''
                How to Prepare the Herbs Before Extraction
            ''',
            'brief': f'''
                {prompt_article_title}
                Explain how herbs should be prepared before extraction.
                Brief
                How to Prepare the Herbs Before Extraction
                chopping or crushing herbs
                fresh vs dried plant material
                particle size and extraction efficiency
                removing impurities
                Explain why preparation affects extraction quality.
                {preparation_info}
                {prompt_article_writing_rules}
            ''',
            'regen': regen_function,
        },
        {
            'id': 'procedure__ratio',
            'hierarchy': 'h3',
            'heading': f'''
                Recommended Herb-to-Solvent Ratio
            ''',
            'brief': f'''
                {prompt_article_title}
                Brief
                Recommended Herb-to-Solvent Ratio
                Explain the ideal proportion between herbs and the extracting liquid.
                Describe:
                common ratios used in herbal preparation
                how ratios change for fresh vs dried herbs
                how stronger or weaker preparations can be created
                Give clear examples.
                {preparation_info}
                {prompt_article_writing_rules}
            ''',
            'regen': regen_function,
        },
        {
            'id': 'procedure__steps',
            'hierarchy': 'h3',
            'heading': f'''
                Step-by-Step Preparation Process
            ''',
            'brief': f'''
                {prompt_article_title}
                Brief
                Step-by-Step Preparation Process
                Provide the complete chronological process.
                Each step should include:
                the action
                the reason for the step
                a practical tip
                Typical sequence:
                measure herbs
                add solvent
                apply heat or extraction method
                allow extraction time
                strain or filter
                collect the preparation
                Ensure the process is easy for beginners to replicate.
                {preparation_info}
                {prompt_article_writing_rules}
            ''',
            'regen': regen_function,
        },
        {
            'id': 'procedure__time_temp',
            'hierarchy': 'h3',
            'heading': f'''
                Optimal Extraction Time and Temperature
            ''',
            'brief': f'''
                {prompt_article_title}
                Brief
                Optimal Extraction Time and Temperature
                Explain how time and temperature affect the extraction process.
                Describe:
                typical duration ranges
                how heat affects compound release
                what happens if extraction is too short or too long
                Clarify differences depending on plant material type.
                {preparation_info}
                {prompt_article_writing_rules}
            ''',
            'regen': regen_function,
        },
        {
            'id': 'procedure__strength',
            'hierarchy': 'h3',
            'heading': f'''
                How to Adjust the Strength of the Preparation
            ''',
            'brief': f'''
                {prompt_article_title}
                Brief
                How to Adjust the Strength of the Preparation
                Explain how users can control the potency of the preparation.
                Discuss:
                increasing or reducing herb quantity
                adjusting extraction time
                adjusting solvent volume
                strong vs mild preparations
                {preparation_info}
                {prompt_article_writing_rules}
            ''',
            'regen': regen_function,
        },
        {
            'id': 'procedure__strain_store',
            'hierarchy': 'h3',
            'heading': f'''
                How to Strain and Store the Preparation
            ''',
            'brief': f'''
                {prompt_article_title}
                Brief
                How to Strain and Store the Preparation
                Explain what to do after the extraction is complete.
                Cover:
                filtering methods
                storage containers
                refrigeration or preservation
                typical shelf life
                Focus on maintaining potency and safety.
                {preparation_info}
                {prompt_article_writing_rules}
            ''',
            'regen': regen_function,
        },
        {
            'id': 'procedure__mistakes',
            'hierarchy': 'h3',
            'heading': f'''
            Common Mistakes to Avoid When Preparing {entity}
            ''',
            'brief': f'''
                {prompt_article_title}
                Brief
                Common Mistakes to Avoid When Preparing {entity}
                Explain frequent preparation errors and how to avoid them.
                Examples:
                overheating delicate herbs
                incorrect ratios
                over-extraction
                improper storage
                {preparation_info}
                {prompt_article_writing_rules}
            ''',
            'regen': regen_function,
        },
        {
            'id': 'usage',
            'hierarchy': 'h2',
            'heading': f'''
                Which Herbs and Plant Parts Work Best for {entity}
            ''',
            'brief': f'''
                {prompt_article_title}
                Which Herbs and Plant Parts Work Best for {entity}
                Intent covered: usage / application
                Brief
                Explain when this preparation method is appropriate.
                Describe:
                which plant parts it works best for
                examples of specific herbs
                why these herbs respond well to this preparation method
                Example structure:
                leaves and flowers
                roots and bark
                aromatic herbs
                mucilaginous herbs
                Focus on selection criteria, not preparation steps.
                {preparation_info}
                {prompt_article_writing_rules}
            ''',
            'regen': regen_function,
        },
        {
            'id': 'comparison',
            'hierarchy': 'h2',
            'heading': f'''
                {entity} vs Other Herbal Preparations
            ''',
            'brief': f'''
                {prompt_article_title}
                {entity} vs Other Herbal Preparations
                Intent covered: comparison
                Brief
                Explain how this preparation differs from other extraction methods.
                Compare with other pereparation types like the following when it makes sense:
                infusion
                decoction
                tincture
                maceration
                Focus on differences in:
                solvent
                extraction strength
                preparation time
                plant parts suitability
                A simple comparison table improves clarity and supports comparison queries.
                {preparation_info}
                {prompt_article_writing_rules}
            ''',
            'regen': regen_function,
        },
        {
            'id': 'when',
            'hierarchy': 'h2',
            'heading': f'''
                When to Use {entity} in Herbal Practice
            ''',
            'brief': f'''
                {prompt_article_title}
                When to Use {entity} in Herbal Practice
                Intent covered: practical decision-making
                Brief
                Explain situations where this preparation method is preferred.
                Discuss:
                medicinal goals
                herbal traditions
                convenience and shelf life
                strength of extraction
                This section answers questions like:
                when should you use a decoction instead of an infusion
                Focus on decision logic, not preparation instructions.
                {preparation_info}
                {prompt_article_writing_rules}
            ''',
            'regen': regen_function,
        },
        {
            'id': 'safety',
            'hierarchy': 'h2',
            'heading': f'''
                Safety Considerations and Best Practices
            ''',
            'brief': f'''
                {prompt_article_title}
                Safety Considerations and Best Practices
                Intent covered: safety intent
                Brief
                Provide responsible guidance for safe preparation and use.
                Cover:
                proper herb identification
                contamination risks
                storage recommendations
                dosage awareness
                Clarify that some herbs require professional guidance.
                Avoid repeating preparation steps; focus strictly on risk prevention.
                {preparation_info}
                {prompt_article_writing_rules}
            ''',
            'regen': regen_function,
        },
        {
            'id': 'historical',
            'hierarchy': 'h2',
            'heading': f'''
                The Role of {entity} in Traditional Herbal Medicine
            ''',
            'brief': f'''
                {prompt_article_title}
                The Role of {entity} in Traditional Herbal Medicine
                Intent covered: contextual / historical
                Brief
                Explain how this preparation method has been used historically in herbal traditions.
                Discuss:
                traditional herbal systems (European, Chinese, Ayurvedic, etc.)
                common historical uses
                why this preparation method became widely used
                This section adds topical depth and cultural context without overlapping with practical sections.
                {preparation_info}
                {prompt_article_writing_rules}
            ''',
            'regen': regen_function,
        },

    ]

    html_article = ''
    for section in _sections_new:
        if 'regen' in section: _regen = section['regen']
        else: _regen = regen_function
        html_article += section__gen(
                json_article_filepath, 
                entity=entity,
                key=section['id'],
                title=section['heading'],
                heading=section['hierarchy'],
                brief=section['brief'],
                regen=_regen, dispel=dispel_function,
        )

    # print(html_article)
    ###
    html_article = sections.toc(html_article)
    # print('###########################################################3')
    # print(html_article)

    ###
    head_html = components.html_head(
        meta_title, meta_description, css='/styles-herb-monograph.css', canonical=canonical_html
    )
    import textwrap
    html = textwrap.dedent(f''' 
        <!DOCTYPE html>
        <html lang="en">
        {head_html}
        <body>
            {sections.header_default()}
            {sections.breadcrumbs_new(url_slug)}
            <main>
                <article class="container-md article">
                    {html_article}
                </article>
            </main>
            {sections.footer()}
        </body>
        </html>
    ''').strip()
    html_filepath = f'''{g.website_folderpath}/{url_slug}.html'''
    io.folder_create_from_filepath(html_filepath)
    with open(html_filepath, 'w') as f: f.write(html)


def gen():
    learning_herbal_medicine__learning_paths__gen()
    learning_herbal_medicine__learning_paths__apothecary__gen()
    preparations__preparation__gen(
        {
            'entity': 'Infusions',
            'entity_singular': 'Infusion',
            'preparation_info': 'uses hot water',
            'preparation_steps': '',
        }
    )
    preparations__preparation__gen(
        {
            'entity': 'Decoctions',
            'entity_singular': 'Decoction',
            'preparation_steps': '',
        }
    )
    preparations__preparation__gen(
        {
            'entity': 'Tinctures',
            'entity_singular': 'Tincture',
            'preparation_steps': '',
        }
    )
    preparations__preparation__gen(
        {
            'entity': 'Macerations',
            'entity_singular': 'Maceration',
            'preparation_steps': '',
        }
    )
    preparations__preparation__gen(
        {
            'entity': 'Syrups',
            'entity_singular': 'Syrup',
            'preparation_steps': '',
        }
    )
    preparations__preparation__gen(
        {
            'entity': 'Oils',
            'entity_singular': 'Oil',
            'preparation_steps': '',
        }
    )
    preparations__preparation__gen(
        {
            'entity': 'Salves',
            'entity_singular': 'Salve',
            'preparation_steps': '',
        }
    )
    preparations__preparation__gen(
        {
            'entity': 'Poultices',
            'entity_singular': 'Poultice',
            'preparation_steps': '',
        }
    )
    preparations__preparation__gen(
        {
            'entity': 'Compresses',
            'entity_singular': 'Compress',
            'preparation_steps': '',
        }
    )
