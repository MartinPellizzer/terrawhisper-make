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


    print(html_article)
    ###
    html_article = sections.toc(html_article)
    print('###########################################################3')
    print(html_article)

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

def preparations__infusions__gen():
    url_slug = f'preparations/infusions'
    meta_title = f'Herbal Infusions: Definition, Benefits, and How to Make This Preparation'
    meta_description = ''
    canonical_html = f'''<link rel="canonical" href="https://terrawhisper.com/{url_slug}.html">'''
    core_entity = 'infusions'

    ########################################
    # json
    ########################################
    json_article_filepath = f'''{g.DATABASE_FOLDERPATH}/json/{url_slug}.json'''
    json_article = io.json_read(json_article_filepath, create=True)
    json_article['url'] = url_slug
    io.json_write(json_article_filepath, json_article)

    regen_function = False
    dispel_function = False

    _sections = [
        {
            'id': 'intro',
            'heading': 'h1',
            'text': f'''
Herbal Infusions: Definition, Benefits, and How to Make This Preparation
''',
            'brief': f'''
''',
            'html_after': '[toc]',
        },
        {
            'id': 'what',
            'heading': 'h2',
            'text': f'''
            What Is an Herbal Infusion?
''',
            'brief': f'''
**Brief**
Define the entity precisely and explain how infusions function as a **water-based extraction method used primarily for leaves, flowers, and other soft plant materials**.
**Attributes**
* herbal infusion definition
* infusion extraction mechanism
* plant material types
* infusion temperature
* infusion steeping process
            ''',
            'html_after': '',
            'start_text': '',
        },
        {
            'id': 'what__0000',
            'heading': 'h3',
            'text': f'''
            What Makes an Infusion Different From Herbal Tea?
''',
            'brief': f'''
**Brief**
Clarify that herbal tea is a **casual term**, while infusion is the **technical herbal preparation method** used in herbal medicine.
**Attributes**
* terminology differences
* herbalism vs common language
* medicinal infusion vs beverage tea
            ''',
            'html_after': '',
            'start_text': '',
        },
        {
            'id': 'why',
            'heading': 'h2',
            'text': f'''
Why Herbal Infusions Are Used in Herbal Medicine
            ''',
            'brief': f'''
**Brief**
Explain why herbalists use infusions instead of other preparations and how they efficiently extract **water-soluble compounds**.
**Attributes**
* water-soluble phytochemicals
* gentle extraction method
* suitable plant parts
* digestion and absorption
* medicinal delivery
            ''',
            'html_after': '',
            'start_text': '',
        },
        {
            'id': 'why__0000',
            'heading': 'h3',
            'text': f'''
Medicinal Compounds Extracted in Infusions
            ''',
            'brief': f'''
**Brief**
Explain which compounds dissolve into water during infusion and why they are therapeutically valuable.
**Attributes**
* flavonoids
* polyphenols
* tannins
* mucilage
* volatile oils (partially)
* minerals
            ''',
            'html_after': '',
            'start_text': '',
        },
        {
            'id': 'plant_parts',
            'heading': 'h2',
            'text': f'''
Plant Parts Best Suited for Herbal Infusions
            ''',
            'brief': f'''
**Brief**
Explain why infusions work best for delicate plant materials rather than hard plant tissues.
**Attributes**
* leaves
* flowers
* soft stems
* aerial parts
* fresh vs dried herbs
            ''',
            'html_after': '',
            'start_text': '',
        },
        {
            'id': 'herbs',
            'heading': 'h3',
            'text': f'''
Herbs Commonly Prepared as Infusions
            ''',
            'brief': f'''
**Brief**
Provide examples of herbs traditionally prepared as infusions and link to herb-specific pages.
**Attributes**
* chamomile
* peppermint
* nettle
* lemon balm
* raspberry leaf
* linden flower
            ''',
            'html_after': '',
            'start_text': '',
        },

        {
            'id': 'how',
            'heading': 'h2',
            'text': f'''
How to Make an Herbal Infusion (Step-by-Step)
            ''',
            'brief': f'''
**Brief**
Explain that an herbal infusion is a **simple process of steeping herbs in hot water to extract medicinal compounds**, and that the method works best for **leaves, flowers, and other delicate plant parts**.
**Attributes to cover**
* hot water extraction
* steeping process
* herb to water ratio
* steeping time
* straining
            ''',
            'html_after': '',
            'start_text': '',
        },
        {
            'id': 'how__0000',
            'heading': 'h3',
            'text': f'''
The Master Recipe for a Basic Herbal Infusion
            ''',
            'brief': f'''
**Brief**
Introduce a **universal ratio and method** beginners can apply to most infusion herbs.
### Standard Ratio
* **1 teaspoon dried herb per cup (240 ml) of water**
  or
* **1 tablespoon fresh herb per cup of water**
For larger batches:
* **1 tablespoon dried herb per 2 cups water**
Explain that this ratio creates a **balanced infusion that is flavorful but not overly strong**.
            ''',
            'html_after': '',
            'start_text': '',
        },
        {
            'id': 'how__0001',
            'heading': 'h3',
            'text': f'''
Equipment You Need
            ''',
            'brief': f'''
**Brief**
Explain the minimal tools required so beginners can start immediately.
**Equipment**
* kettle or pot for boiling water
* mug, jar, or teapot
* lid or small plate to cover
* strainer or tea filter
* measuring spoon
Explain that **covering the infusion is important to retain aromatic oils**.
            ''',
            'html_after': '',
            'start_text': '',
        },
        {
            'id': 'how__0002',
            'heading': 'h3',
            'text': f'''
Step 1: Choose the Right Herb
            ''',
            'brief': f'''
**Brief**
Explain that infusions are best for **soft plant parts**.
**Good herbs for beginners**
* chamomile
* peppermint
* lemon balm
* nettle
* linden flower
Explain that **roots, bark, and seeds usually require decoctions instead**.
            ''',
            'html_after': f'''
<p>Here's a list of common herbs used for this preparation.</p>
<ul>
    <li>Chamomile</li>
    <li>Peppermint</li>
    <li>Lemon Balm</li>
    <li>Nettle</li>
    <li>Liden</li>
</ul>
            ''',
            'image_src': f'''
/images/preparations/infusions/preparation-choose-herb.jpg
            ''',
            'image_alt': f'''
Herbs chosen to prepare infusions
            ''',
            'start_text': '',
        },
        {
            'id': 'how__0003',
            'heading': 'h3',
            'text': f'''
Step 2: Measure the Herbs
            ''',
            'brief': f'''
**Brief**
Explain how to measure herbs correctly using the master ratio.
Example:
* **1 teaspoon dried chamomile**
* **1 tablespoon fresh peppermint**
Add herbs directly into the mug or teapot.
**Attributes**
* herb potency
* fresh vs dried herb quantity
* scaling recipe
            ''',
            'html_after': '',
            'start_text': '',
            'image_src': f'''
/images/preparations/infusions/preparation-measure-herb.jpg
            ''',
            'image_alt': f'''
Herbs measured to prepare infusions
            ''',
        },
        {
            'id': 'how__0004',
            'heading': 'h3',
            'text': f'''
Step 3: Heat Fresh Water
            ''',
            'brief': f'''
**Brief**
Explain that water should be hot but not boiling, then poured immediately over the herbs.
**Details to include**
* ideal temperature: near boiling (70-90°C / 160-190°F)
* explain that to reach this temperature you can boil water and then wait about 5 minutes to make it cool slightly, it should reach about 80 degree celsius this way, this technique is useful if you don't have a termometer
* fresh water improves flavor
* avoid reheated water
            ''',
            'html_before': f'''''',
            'html_after': '',
            'start_text': '',
            'image_src': f'''
/images/preparations/infusions/preparation-boil-water.jpg
            ''',
            'image_alt': f'''
Boil water to prepare infusions
            ''',
            'regen': True,
        },
        {
            'id': 'how__0005',
            'heading': 'h3',
            'text': f'''
Step 4: Pour Water Over the Herbs
            ''',
            'brief': f'''
**Brief**
Explain that hot water **begins the extraction process instantly**.
Instructions
1. Place herbs in mug or teapot
2. Pour hot water over herbs
3. Ensure herbs are fully submerged
Explain that **water activates the release of plant compounds**.
            ''',
            'html_after': '',
            'start_text': '',
            'image_src': f'''
/images/preparations/infusions/preparation-pour-water.jpg
            ''',
            'image_alt': f'''
Pour water to prepare infusions
            ''',
        },
        {
            'id': 'how__0006',
            'heading': 'h3',
            'text': f'''
Step 5: Cover and Steep
            ''',
            'brief': f'''
**Brief**
Explain that steeping allows the plant compounds to dissolve into the water.
Standard steeping time:
**5–15 minutes**
Explain why covering matters:
* traps volatile oils
* improves medicinal potency
            ''',
            'html_after': '',
            'start_text': '',
            'image_src': f'''
/images/preparations/infusions/preparation-cover-and-steep.jpg
            ''',
            'image_alt': f'''
Cover and steep to prepare infusions
            ''',
        },
        {
            'id': 'how__0007',
            'heading': 'h3',
            'text': f'''
Step 6: Strain the Herbs
            ''',
            'brief': f'''
**Brief**
Explain how to remove plant material once steeping is complete.
Methods:
* fine mesh strainer
* tea filter
* cheesecloth
Explain that the remaining liquid is the **finished infusion**.
            ''',
            'html_after': '',
            'start_text': '',
            'image_src': f'''
/images/preparations/infusions/preparation-strain-herb.jpg
            ''',
            'image_alt': f'''
Strain the herb to prepare infusions
            ''',
        },
        {
            'id': 'how__0008',
            'heading': 'h3',
            'text': f'''
Step 7: Taste and Adjust
            ''',
            'brief': f'''
**Brief**
Teach beginners how to adjust strength.
Ways to adjust:
If too strong
* add hot water
If too weak
* steep longer next time
* increase herb quantity
Optional additions
* honey
* lemon
            ''',
            'html_after': '',
            'start_text': '',
            'image_src': f'''
/images/preparations/infusions/preparation-taste-adjust.jpg
            ''',
            'image_alt': f'''
Taste and adjust the prepared infusions
            ''',
        },
        {
            'id': 'how__0009',
            'heading': 'h3',
            'text': f'''
Signs Your Infusion Is Done Correctly
            ''',
            'brief': f'''
**Brief**
Explain sensory indicators beginners can use to judge success.
Good infusion signs:
* noticeable herbal aroma
* visible color change in water
* balanced flavor
Examples
Chamomile → golden
Peppermint → greenish
            ''',
            'html_after': '',
            'start_text': '',
        },
        {
            'id': 'how__0010',
            'heading': 'h3',
            'text': f'''
Common Beginner Mistakes
            ''',
            'brief': f'''
**Brief**
Prevent common problems so beginners succeed.
Mistakes to explain:
Using too much herb
Steeping too long (bitterness)
Not covering the cup
Using stale herbs
Using water that isn't hot enough
            ''',
            'html_after': '',
            'start_text': '',
        },
        {
            'id': 'how__0011',
            'heading': 'h3',
            'text': f'''
Example Beginner Infusion (Chamomile)
            ''',
            'brief': f'''
**Brief**
Provide a simple real-world example.
Recipe
1 tsp dried chamomile
1 cup boiling water
steep 10 minutes
Flavor: mild, floral, relaxing.
            ''',
            'html_after': '',
            'start_text': '',
        },
        {
            'id': 'ratios',
            'heading': 'h2',
            'text': f'''
Herb-to-Water Ratios for Infusions
            ''',
            'brief': f'''
**Brief**
Explain standard dosage ratios and how they change depending on herb potency or preparation goals.
**Attributes**
* dried herb ratio
* fresh herb ratio
* strong infusions
* weak infusions
* therapeutic dosage
            ''',
            'html_after': '',
            'start_text': '',
        },
        {
            'id': 'ratios_0000',
            'heading': 'h3',
            'text': f'''
Strong Infusions vs Standard Infusions
            ''',
            'brief': f'''
**Brief**
Explain when herbalists use **long-steep mineral infusions** compared to regular infusions.
**Attributes**
* overnight infusions
* mineral extraction
* nettle infusion example
* nourishing infusions
            ''',
            'html_after': '',
            'start_text': '',
        },
        {
            'id': 'how_long',
            'heading': 'h2',
            'text': f'''
How Long Should Herbal Infusions Steep?
            ''',
            'brief': f'''
**Brief**
Explain the importance of steeping time and how it affects extraction.
**Attributes**
* typical steep time
* stronger extraction
* bitterness risks
* herb-specific variation
            ''',
            'html_after': '',
            'start_text': '',
        },
        {
            'id': 'how_long_0000',
            'heading': 'h3',
            'text': f'''
Why Covering the Infusion Matters
            ''',
            'brief': f'''
**Brief**
Explain how covering prevents volatile oils from escaping.
**Attributes**
* volatile oils
* aroma compounds
* medicinal potency
            ''',
            'html_after': '',
            'start_text': '',
        },
        {
            'id': 'comparison',
            'heading': 'h2',
            'text': f'''
Infusions vs Decoctions: Key Differences
            ''',
            'brief': f'''
**Brief**
Explain the difference between the two herbal preparation methods.
**Attributes**
* preparation method
* plant material type
* heat intensity
* extraction strength
            ''',
            'html_after': '',
            'start_text': '',
        },
        {
            'id': 'comparison_0000',
            'heading': 'h3',
            'text': f'''
When to Use a Decoction Instead
            ''',
            'brief': f'''
**Brief**
Explain when roots, bark, and seeds require boiling rather than steeping.
**Attributes**
* roots
* bark
* seeds
* tough plant tissues
            ''',
            'html_after': '',
            'start_text': '',
        },
        {
            'id': 'fresh_vs_dried',
            'heading': 'h2',
            'text': f'''
Fresh vs Dried Herbs for Infusions
            ''',
            'brief': f'''
**Brief**
Explain the differences in potency, flavor, and preparation.
**Attributes**
* potency differences
* water content
* flavor profile
* dosage adjustments
            ''',
            'html_after': '',
            'start_text': '',
        },
        {
            'id': 'benefits',
            'heading': 'h2',
            'text': f'''
Benefits of Drinking Herbal Infusions
            ''',
            'brief': f'''
**Brief**
Explain the general health benefits and how infusions deliver herbal medicine in a gentle way.
**Attributes**
* hydration
* nutrient intake
* gentle herbal therapy
* digestive support
* relaxation
            ''',
            'html_after': '',
            'start_text': '',
        },
        {
            'id': 'safety',
            'heading': 'h2',
            'text': f'''
Safety Considerations for Herbal Infusions
            ''',
            'brief': f'''
**Brief**
Explain that herbs are biologically active and must be used responsibly.
**Attributes**
* herb safety
* dosage awareness
* allergies
* pregnancy considerations
* herb-drug interactions
            ''',
            'html_after': '',
            'start_text': '',
        },
        {
            'id': 'store',
            'heading': 'h2',
            'text': f'''
How to Store Herbal Infusions
            ''',
            'brief': f'''
**Brief**
Explain proper storage and shelf life.
**Attributes**
* refrigeration
* shelf life
* bacterial growth
* reheating
            ''',
            'html_after': '',
            'start_text': '',
        },
    ]

    html_article = ''

    for section in _sections:
        if 'regen' in section: _regen = section['regen']
        else: _regen = regen_function
        if 'start_text' in section: _start_text = f'''Start the reply with the following words: {section['start_text']}'''
        else: _start_text = ''
        if 'html_manual' not in section or section['html_manual'] == '':
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
        else:
            html_article += f'''<{section['heading']}>{section['text']}</{section['heading']}>'''
            html_article += section['html_manual']
        if 'image_src' in section and section['image_src'] != '':
            html_article += f'''<img src="{section['image_src'].strip()}">'''
        if section['html_after'] != '':
            html_article += section['html_after']


    print(html_article)
    ###
    html_article = sections.toc(html_article)
    print('###########################################################3')
    print(html_article)

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
    preparations__infusions__gen()
    
