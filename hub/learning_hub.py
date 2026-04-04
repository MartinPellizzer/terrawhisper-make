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
                It must cover in detail all the topics (attributes) mentioned in the BRIEF.
                It must be the most direct, clear, detailed content possible without fluff.
                It must be at least 5 sentences long.
                Write at least one sentence for each point in the brief.
                Don't give me bold or italicized text. 
                Reply only with the subordinate text.
                BRIEF:
                {brief}
                {start_text}
                /no_think
            ''').strip()
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
            'regen': True,
            'start_text': 'This path is for ',
        },
        {
            'id': 'profile',
            'heading': 'h3',
            'text': 'Recognizing the Maker and Practical Herbalist Profile',
            'brief': 'Describe the psychological and practical traits of learners who learn best by experimenting with tangible preparations rather than memorizing plant classifications.',
            'html_after': '',
        },
        {
            'id': 'methodology',
            'heading': 'h2',
            'text': 'The Recipe-First Learning Methodology',
            'brief': 'Explain the distinct pedagogical approach where specific herbal preparations are taught before deep botanical theory to ensure immediate utility and high learner motivation.',
            'html_after': '',
        },
        {
            'id': 'progression',
            'heading': 'h3',
            'text': 'Standardized Progression of Herbal Preparations',
            'brief': 'Outline the specific learning order for this path, starting with herbal teas and infusions and advancing systematically to tinctures, glycerites, salves, and complex formulations.',
            'html_after': '',
        },
        {
            'id': 'core',
            'heading': 'h2',
            'text': 'Developing Core Formulation and Extraction Skills',
            'brief': 'Detail the practical competencies gained through this path, focusing on the ability to create effective remedies using specific extraction techniques and dosage calculations.',
            'html_after': '',
        },
        {
            'id': 'tools',
            'heading': 'h3',
            'text': 'Building a Functional Home Apothecary',
            'brief': 'Provide guidance on selecting and organizing physical tools and storage systems required to maintain the workflow of a practical herbalist who makes remedies daily.',
            'html_after': '',
        },
        {
            'id': 'limitation',
            'heading': 'h2',
            'text': 'Mitigating the Weakness of Fragmented Knowledge',
            'brief': 'Address the potential limitation where practical focus might lead to superficial understanding, and recommend strategies to deepen botanical knowledge without losing practical momentum.',
            'html_after': '',
        },
        {
            'id': 'compare',
            'heading': 'h2',
            'text': 'How The Apothecary Path Compares to Other Learning Methods',
            'brief': 'Differentiate this practical entity from academic or clinical herbal paths by highlighting the speed of results and the focus on formulation over theoretical diagnosis.',
            'html_after': '',
        },
        {
            'id': 'integrate',
            'heading': 'h3',
            'text': 'Integrating Practical Skills with Deeper Botanical Study',
            'brief': 'Explain how this path serves as a foundation that can eventually integrate with "The Botanist Path" or "The Clinical Path" to create a comprehensive herbalist skill set.',
            'html_after': '',
        },
        {
            'id': 'cta',
            'heading': 'h2',
            'text': 'Starting Your Journey: Immediate Application and Next Steps',
            'brief': 'Conclude with a call to action that encourages the user to identify herbs they currently have and create their first simple remedy to begin the cycle of practical learning.',
            'html_after': '',
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

def gen():
    learning_herbal_medicine__learning_paths__gen()
    learning_herbal_medicine__learning_paths__apothecary__gen()
    
