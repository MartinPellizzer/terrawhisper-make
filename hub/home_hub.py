from lib import g
from lib import io
from lib import llm
from lib import data
from lib import polish
from lib import components
from lib import sections

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

def paragraph__gen(json_article_filepath, key, title, brief, regen=False, dispel=False):
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
                I want you to write the subordinate text for the following section: "{title}". 
                The subordinate text is the first 5 sentences that must be written immediately after the headline. 
                The subordinate text must answer in the most direct, clear, detailed way possible without fluff.
                In sentence 1, you must always reply to the implicit question asked in the section.
                In the following sentences, you give more details.
                Don't give me bold or italicized text. 
                Reply only with the subordinate text.
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
    paragraph_formatted = paragraph_format_1N1(paragraph)
    # paragraph_formatted = paragraph
    html = f'''
        <section style="padding-bottom: 9.6rem;">
            <div class="container-md">
            <h2>{title}</h2>
            {paragraph_formatted}
            </div>
        </section>
    '''
    return html

def sentence__gen(json_article_filepath, key, title, brief, regen=False, dispel=False):
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
        <section style="padding-bottom: 9.6rem;">
            <div class="container-md">
            <h2>{title}</h2>
            <p>
            {paragraph_formatted}
            </p>
            </div>
        </section>
    '''
    return html

def gen():
    url_slug = f'herbal-medicine'
    meta_title = f'Learn Herbal Medicine'
    meta_description = ''
    canonical_html = f'''<link rel="canonical" href="https://terrawhisper.com">'''
    json_article_filepath = f'''{g.DATABASE_FOLDERPATH}/json/{url_slug}.json'''
    json_article = io.json_read(json_article_filepath, create=True)

    regen_function = False
    dispel_function = False

    html_placeholders = ''

    if 0:
        html_placeholders += sentence__gen(
            json_article_filepath, 
            key=f'''
    definition
            ''',
            title=f'''
    What Is Learning Herbal Medicine? Scope, Structure, and Outcomes
            ''', 
            brief=f'''
    Definition of herbal medicine as a field of study
    What distinguishes learning from practicing herbal medicine
    Domains included in herbal education (botany, pharmacology, therapeutics)
    Types of knowledge: theoretical vs practical skills
    Levels of knowledge depth (basic awareness to clinical understanding)
    Expected competencies after learning herbal medicine
            ''', 
            regen=regen_function, dispel=dispel_function
        )

        html_placeholders += paragraph__gen(
            json_article_filepath, 
            key=f'''
    paths_paragraph
            ''',
            title=f'''
    Herbal Medicine Learning Paths
            ''', 
            brief=f'''
    Beginner learning path (basic concepts and simple remedies)
    Intermediate learning path (plant knowledge and formulations)
    Advanced learning path (clinical thinking and case application)
    Self-care vs professional practice learning tracks
    Linear vs modular learning approaches
    Common progression milestones in herbal education
            ''', 
            regen=regen_function, dispel=dispel_function
        )

                # The 3 main learning paths to start mastering herbal medicine are: <strong>The Apothecary Path<strong>, </strong>The Botanist Path</strong>, and <strong>The Chemist Path</strong>.
    html_placeholders += f'''
        <section style="padding-bottom: 9.6rem;">
            <div class="container-xl">
                <h2>Herbal Medicine Learning Paths</h2>
                <p style="margin-bottom: 1.6rem;">
                    The 3 main learning paths to start mastering herbal medicine are:
                </p>
                <ul style="margin-bottom: 1.6rem;">
                    <li><strong>The Apothecary Path</strong></li>
                    <li><strong>The Botanist Path</strong></li>
                    <li><strong>The Chemist Path</strong></li>
                </ul>
                <p style="margin-bottom: 4.8rem;">
                    Choose the one that best fits you below, based on your learning preferences.
                </p>
                <div class="grid-3" style="gap: 3.2rem;">
                    <div>
                        <img src="/images/home/apothecary-path.jpg" width=512 style="margin-bottom: 1.6rem;">
                        <h3>The Apothecary Path</h3>
                        <p style="margin-bottom: 2.4rem;"><em>(The Maker & Practical Herbalist)</em></p>
                        <p style="margin-bottom: 3.2rem;">Difficulty level: <br> ⭐ Beginner to Intermediate</p>
                        <h4 style="margin-bottom: 0.8rem;">Who this path is for</h4>
                        <p>This path is for people who learn best by doing and experimenting. It's for people who want to make remedies immediately and understand herbs through hands-on practice rather than theory.</p>
                        <div style="margin-top: 3.2rem;">
                            <a class="button-default" style="text-transform: uppercase; letter-spacing: 0.5px;" 
                                href="#">Coming Soon
                            </a>
                        </div>
                    </div>
                    <div>
                        <img src="/images/home/botanist-path.jpg" width=512 style="margin-bottom: 1.6rem;">
                        <h3>The Botanist Path</h3>
                        <p style="margin-bottom: 2.4rem;"><em>(The Plant & Field Herbalist)</em></p>
                        <p style="margin-bottom: 3.2rem;">Difficulty level: <br> ⭐⭐ Intermediate</p>
                        <h4 style="margin-bottom: 0.8rem;">Who this path is for</h4>
                        <p>This path is for people fascinated by plants themselves. It's for people who learn through observation, identification, and ecological understanding.</p>
                        <div style="margin-top: 3.2rem;">
                            <a class="button-default" style="text-transform: uppercase; letter-spacing: 0.5px;" 
                                href="#">Coming Soon
                            </a>
                        </div>
                    </div>
                    <div>
                        <img src="/images/home/chemist-path.jpg" width=512 style="margin-bottom: 1.6rem;">
                        <h3>The Chemist Path</h3>
                        <p style="margin-bottom: 2.4rem;"><em>(The Scientific & Analytical Herbalist)</em></p>
                        <p style="margin-bottom: 3.2rem;">Difficulty level: <br> ⭐⭐⭐ Advanced</p>
                        <h4 style="margin-bottom: 0.8rem;">Who this path is for</h4>
                        <p>This path is for people who prefer theory, systems, and scientific understanding before practice. It's for people who want to understand the theory before the practice.</p>
                        <div style="margin-top: 3.2rem;">
                            <a class="button-default" style="text-transform: uppercase; letter-spacing: 0.5px;" 
                                href="#">Coming Soon
                            </a>
                        </div>
                    </div>
                </div>
            </div>
        </section>
    '''

    html_placeholders += sentence__gen(
        json_article_filepath, 
        key=f'''
topics
        ''',
        title=f'''
Topics Covered in Herbal Medicine Education
        ''', 
        brief=f'''
Plant identification and classification topics
Herbal remedy preparation topics
Human health and condition-based learning topics
Safety and risk awareness topics
Systems of herbal medicine included in curricula
Practical skills vs theoretical knowledge areas
        ''', 
        regen=regen_function, dispel=dispel_function
    )

    html_placeholders += sentence__gen(
        json_article_filepath, 
        key=f'''
foundations
        ''',
        title=f'''
Foundations of Herbal Medicine Knowledge
        ''', 
        brief=f'''
Basic botanical concepts for herbalists
Introduction to plant properties and actions
Fundamental concepts of how herbs influence the body
Terminology used in herbal medicine
Understanding plant energetics (where applicable)
Core principles behind herbal effectiveness
        ''', 
        regen=regen_function, dispel=dispel_function
    )

    html_placeholders += sentence__gen(
        json_article_filepath, 
        key=f'''
            remedies
        ''',
        title=f'''
            Herbal Remedies: Types and Use Cases
        ''', 
        brief=f'''
Definition of herbal remedies
Categories of remedies (internal vs external)
Acute vs chronic use cases
Preventive vs therapeutic applications
Single-herb vs multi-herb formulations
Common forms of remedies used in practice
        ''', 
        regen=regen_function, dispel=dispel_function
    )

    html_placeholders += sentence__gen(
        json_article_filepath, 
        key=f'''
            plants
        ''',
        title=f'''
            Medicinal Plants and Materia Medica Knowledge
        ''', 
        brief=f'''
What is materia medica in herbal medicine
Structure of plant profiles (properties, uses, preparation)
How medicinal plants are categorized
Regional variation in plant usage
Importance of plant identification accuracy
Building a personal materia medica knowledge base
        ''', 
        regen=regen_function, dispel=dispel_function
    )

    html_placeholders += sentence__gen(
        json_article_filepath, 
        key=f'''
            safety
        ''',
        title=f'''
            Herbal Medicine Safety: Principles and Risk Awareness
        ''', 
        brief=f'''
Why safety is critical in herbal medicine
Types of risks associated with herbs
Understanding contraindications
Recognizing safe vs unsafe usage contexts
Importance of correct plant identification for safety
Role of professional guidance in risk reduction
        ''', 
        regen=regen_function, dispel=dispel_function
    )

    html_placeholders += sentence__gen(
        json_article_filepath, 
        key=f'''
preparation
        ''',
        title=f'''
Herbal Preparation Skills and Techniques
        ''', 
        brief=f'''
Purpose of preparing herbal remedies
Skill sets required for preparation
Differences between preparation techniques
Selecting the right preparation for plant type
Tools and materials used in herbal preparation
Beginner vs advanced preparation complexity
        ''', 
        regen=regen_function, dispel=dispel_function
    )

    html_placeholders += sentence__gen(
        json_article_filepath, 
        key=f'''
ways
        ''',
        title=f'''
Ways to Learn Herbal Medicine: Methods and Formats
        ''', 
        brief=f'''
Self-study through books and online resources
Structured courses and certifications
Apprenticeship and mentorship models
Workshops and hands-on training
Online vs in-person learning formats
Choosing the right learning method based on goals
        ''', 
        regen=regen_function, dispel=dispel_function
    )

    html_placeholders += sentence__gen(
        json_article_filepath, 
        key=f'''
systems
        ''',
        title=f'''
Herbal Medicine Systems: Comparative Learning Approaches
        ''', 
        brief=f'''
Overview of major herbal medicine systems
Differences in diagnostic frameworks
Differences in treatment philosophy
Variations in herb selection and formulation
Cultural context of each system
Benefits of studying multiple systems
        ''', 
        regen=regen_function, dispel=dispel_function
    )

    html_placeholders += sentence__gen(
        json_article_filepath, 
        key=f'''
benefits
        ''',
        title=f'''
Benefits of Learning Herbal Medicine
        ''', 
        brief=f'''
Personal health empowerment
Preventive health knowledge
Self-sufficiency in natural remedies
Understanding of plant-based healing
Connection to traditional knowledge systems
Practical everyday applications
        ''', 
        regen=regen_function, dispel=dispel_function
    )

    html_placeholders += sentence__gen(
        json_article_filepath, 
        key=f'''
guides
        ''',
        title=f'''
Core Guides to Start Learning Herbal Medicine
        ''', 
        brief=f'''
Beginner-friendly herbal medicine guides
Step-by-step remedy-making tutorials
Introductory plant identification resources
Safety-focused beginner content
Structured learning sequences
Most essential starting topics for new learners
        ''', 
        regen=regen_function, dispel=dispel_function
    )

    html_placeholders += sentence__gen(
        json_article_filepath, 
        key=f'''
herbal_medicine
        ''',
        title=f'''
Herbal Medicine Knowledge Structure (Topical Map Overview)
        ''', 
        brief=f'''
How herbal medicine knowledge is organized
Relationship between plants, preparations, and applications
Hierarchy of topics (foundations → applications → specialization)
Core vs supplementary knowledge areas
How topics connect within a learning journey
Navigation paths for exploring the subject
        ''', 
        regen=regen_function, dispel=dispel_function
    )

    html_placeholders += sentence__gen(
        json_article_filepath, 
        key=f'''
trust
        ''',
        title=f'''
Trust, Accuracy, and Knowledge Reliability in Herbal Medicine
        ''', 
        brief=f'''
Importance of accurate herbal information
Sources of reliable herbal knowledge
Differences between traditional knowledge and modern evidence
Role of research and validation
Risks of misinformation in herbal medicine
Importance of continuous learning and verification
        ''', 
        regen=regen_function, dispel=dispel_function
    )

    html_placeholders += sentence__gen(
        json_article_filepath, 
        key=f'''
start
        ''',
        title=f'''
Start Learning Herbal Medicine: Next Steps and Direction
        ''', 
        brief=f'''
How to begin learning herbal medicine step-by-step
Choosing a first area of focus
Building a simple learning routine
Selecting beginner-friendly herbs
Avoiding common beginner mistakes
Transitioning from learning to practice
        ''', 
        regen=regen_function, dispel=dispel_function
    )

    html_main = ''
    # html_main = f'<h1>Discover the Healing Power of Herbal Medicine<br><span>Backed by Tradition & Science</span></h1>'
    # html_main = f'<h1>Herbalism for Beginners: Herbal Remedies and Natural Healing</h1>'
    # html_main = f'<h1>Herbalism and Herbal Remedies for Natural Healing</h1>'
    html_atf_h1 = f'<h1 style="color: {g.COLOR_CARBON_POWDER }">Herbal Medicine for Natural Healing</h1>'
    html_atf_tagline = f'<p style="color: {g.COLOR_CARBON_POWDER }"><em>Make herbal remedies to heal naturally.</em></p>'
    html_atf_desc = f'''
        <p style="color: {g.COLOR_CARBON_POWDER}">
            <strong>Herbalism</strong> is the practice of using <strong>medicinal herbs</strong> to support health and well-being through simple preparations such as teas, tinctures, salves, and infused oils. This site offers <strong>beginner-friendly, educational guidance</strong> on medicinal herbs, herbal remedies, and their traditional use for common concerns, with an emphasis on <strong>safe and responsible use</strong>.
        </p>
    '''

    html_hero_old = f'''
        <section class="home-hero" style="padding-top: 9.6rem; padding-bottom: 9.6rem;">
            <div class="container-xl">
                <div class="m-flex" style="gap: 4.8rem;">
                    <div style="flex: 3;">
                        {html_atf_h1}
                        {html_atf_tagline}
                        {html_atf_desc}
                        <div class="m-flex" style="gap: 1.6rem;">
                            <div style="margin-top: 1.6rem;">
                                <a class="button-default" href="/herbs.html">Start Learning Herbalism</a>
                            </div>
                            <div style="margin-top: 1.6rem;">
                                <a class="button-default-ghost" href="/shop/course-preparation-tincture.html">Download Your Free Herbal Guide</a>
                            </div>
                        </div>
                    </div>
                    <div style="flex: 2;">
                        <img src="/images/home/herbalism-herbal-remedies-beginner-apothecary.jpg" alt="Beginner-friendly herbalism setup with medicinal herbs, tinctures, and a mortar and pestle">
                    </div>
                </div>
            </div>
        </section>
    '''

    html_hero = f'''
        <section style="width: 100%;">
          <div style="display: grid; grid-template-columns: minmax(2rem, 1fr) minmax(0, 640px) minmax(0, 640px) minmax(2rem, 1fr); align-items: center;
          ">
            <div style="grid-column: 2;">
              <h1 style="margin-bottom: 1.6rem;">
                Herbal Medicine for Natural Healing
              </h1>

              <p>
                <strong>Herbalism</strong> is the practice of using 
                <strong>medicinal herbs</strong> to support health and well-being 
                through simple preparations such as teas, tinctures, salves, and 
                infused oils.
              </p>

              <div style="margin-top: 2.4rem;">
                <a href="/herbal-medicine.html"
                   style="text-transform: uppercase; letter-spacing: 0.5px;">
                  Learn Herbal Medicine
                </a>
              </div>
            </div>

            <!-- IMAGE -->
            <div style="grid-column: 3 / 5; height: 80vh;">
              <img 
                src="/images/home/sage.jpg" 
                alt="Herbal setup"
                style="width: 100%; height: 100%; object-fit: cover;"
              >
            </div>

          </div>
        </section>
    '''
        # <section style="background-color: {g.COLOR_WHITE_WHISPER}">
    text_padding_right_rem = 9.6
    text_padding_right_px = text_padding_right_rem * 10
    text_w = 1280 // 2 + text_padding_right_px
    html_hero = f'''
        <section>
            <div style="display: flex; align-items: center;">
                <div style="flex: 1;">
                    <div style="max-width: {text_w}px; margin-left: auto; padding-right: {text_padding_right_rem}rem;">
                        <h1 style="color: {g.COLOR_CARBON_POWDER}; margin-bottom: 1.6rem;">
                            Herbal Medicine for Natural Healing
                        </h1>
                        <p style="color: {g.COLOR_CARBON_POWDER};">
                            <strong>Herbalism</strong> is the practice of using <strong>medicinal herbs</strong> to support health and well-being through simple preparations such as teas, tinctures, salves, and infused oils. This site offers <strong>beginner-friendly, educational guidance</strong> on medicinal herbs, herbal remedies, and their traditional use for common concerns, with an emphasis on <strong>safe and responsible use</strong>.
                        </p>
                        <div style="margin-top: 2.4rem;">
                            <a class="button-default" style="text-transform: uppercase; letter-spacing: 0.5px;" href="/herbal-medicine.html">Learn Herbal Medicine</a>
                        </div>
                    </div>
                </div>
                <div style="flex: 1;">
                    <img src="/images/home/sage.jpg" alt="Beginner-friendly herbalism setup with medicinal herbs, tinctures, and a mortar and pestle" style="height: 80vh; object-fit: cover;">
                </div>
            </div>
        </section>
    '''

    padding_x = 4.8
    text_padding_right_rem = padding_x
    text_padding_left_rem = padding_x
    text_padding_right_px = text_padding_right_rem * 10
    text_w = 1280 // 2 + text_padding_right_px
    text_w = 768
    html_hero = f'''
        <section style="margin-bottom: 9.6rem;">
            <div class="m-flex" style="align-items: center;">
                <div style="flex: 1; padding-top: 9.6rem; padding-bottom: 9.6rem;">
                    <div style="max-width: {text_w}px; margin-left: auto; margin-right: auto; padding-right: {text_padding_right_rem}rem; padding-left: {text_padding_left_rem}rem;">
                        <h1 style="color: {g.COLOR_CARBON_POWDER}; margin-bottom: 1.6rem;">
                            Learn Herbal Medicine: How to Study Medicinal Plants, Remedies, and Safe Practice
                        </h1>
                        <p>
Learning herbal medicine means acquiring structured knowledge and practical skills to identify medicinal plants, prepare remedies, understand safety, and apply plant-based treatments for self-care or professional use, whether as a beginner, self-learner, or practitioner moving from informal exploration to systematic, real-world application.
                        </p>
                        <div style="margin-top: 3.2rem;">
                            <a class="button-default" style="text-transform: uppercase; letter-spacing: 0.5px;" href="/herbal-medicine.html">Learn Herbal Medicine</a>
                        </div>
                    </div>
                </div>
                <div style="flex: 1;">
                    <img src="/images/home/sage.jpg" alt="Beginner-friendly herbalism setup with medicinal herbs, tinctures, and a mortar and pestle" style="height: 80vh; object-fit: cover;">
                </div>
            </div>
        </section>
    '''

    html_what = f'''
        <section style="padding-bottom: 9.6rem;">
            <div class="container-md">
                <h2>
What Is Learning Herbal Medicine? Scope, Structure, and Outcomes
                </h2>
                <p>
Learning herbal medicine is the structured study of plant-based remedies, encompassing theoretical knowledge of botany, pharmacology, and therapeutics, combined with practical skills in preparation and application, designed to progress from basic awareness to advanced clinical understanding, equipping learners with the ability to safely identify, use, and evaluate medicinal plants and their formulations.
                </p>
            </div>
        </section>
    '''

    html_paths = f'''
        <section style="padding-bottom: 9.6rem;">
            <div class="container-md">
                <h2>
Herbal Medicine Learning Paths: Beginner to Advanced Progression
                </h2>
                <p>
Herbal medicine learning paths progress from beginner to advanced by starting with foundational concepts and simple remedies, moving through intermediate study of plant knowledge and formulation techniques, and culminating in advanced clinical thinking and case-based application, with distinct tracks for self-care or professional practice and options for linear or modular progression to achieve common milestones in herbal education.
                </p>
            </div>
        </section>
    '''

    html_topics = f'''
        <section style="padding-bottom: 9.6rem;">
            <div class="container-md">
                <h2>
Topics Covered in Herbal Medicine Education
                </h2>
                <p>
Topics covered in herbal medicine education include the identification and classification of medicinal plants, preparation of herbal remedies, understanding human health conditions and appropriate herbal applications, awareness of safety and risks, study of various herbal medicine systems, and the development of both practical skills and theoretical knowledge.
                </p>
            </div>
        </section>
    '''

    html_foundations = f'''
        <section style="padding-bottom: 9.6rem;">
            <div class="container-md">
                <h2>
Foundations of Herbal Medicine Knowledge
                </h2>
                <p>
Foundations of herbal medicine knowledge encompass understanding basic botanical concepts, plant properties and actions, and the principles by which herbs influence human physiology, including terminology, plant energetics where applicable, and the core mechanisms behind herbal effectiveness.
                </p>
            </div>
        </section>
    '''


    html_section_1 = f'''
        <section style="padding-bottom: 9.6rem;">
            <div class="container-xl">
                <h2>What Is Herbalism?</h2>
                <p style="max-width: 720px;">
                    Herbalism is the traditional and modern practice of working with <strong>medicinal plants</strong> to create remedies, teas, tinctures, and salves that support everyday health. 
                    It combines plant knowledge, hands-on preparation skills, and an understanding of how herbs have been used historically for digestion, sleep, stress, skin, and immunity.
                </p>
                <div class="m-flex" style="gap: 4.8rem; margin-top: 4.8rem;">
                    <div style="flex: 1;">
                        <img style="margin-bottom: 1.6rem;" src="/images/home/herbs-medicinal-educational.jpg" alt="Herbs with medicinal properties for educational use in herbalism">
                        <h3>Medicinal Herbs</h3>
                        <p style="margin-bottom: 1.6rem;">Learn about the most common medicinal herbs and their traditional uses for everyday health.</p>
                        <p style="margin-bottom: 1.6rem;"><a href="/herbs.html">Explore Medicinal Herbs</a></p>
                    </div>
                    <div style="flex: 1;">
                        <img style="margin-bottom: 1.6rem;" src="/images/home/herbs-preparations-hands-on.jpg" alt="Herbs with preparation methods for making teas, tinctures, and salves at home">
                        <h3>Herbal Preparations</h3>
                        <p style="margin-bottom: 1.6rem;">Step-by-step guidance on creating teas, tinctures, salves, and other remedies at home.</p>
                        <p style="margin-bottom: 1.6rem;"><a href="/preparations.html">Learn Herbal Preparation Methods</a></p>
                    </div>
                    <div style="flex: 1;">
                        <img style="margin-bottom: 1.6rem;" src="/images/home/herbal-remedies-for-ailments.jpg" alt="Herbal remedies in jars and teas for common ailments like digestion, sleep, stress, and immunity">
                        <h3>Ailments and Remedies</h3>
                        <p style="margin-bottom: 1.6rem;">Understand how herbal remedies support digestion, sleep, stress management, skin health, and immunity.</p>
                        <p style="margin-bottom: 1.6rem;"><a href="/ailments.html">See Herbal Remedies for Common Ailments</a></p>
                    </div>
                </div>
            </div>
        </section>
    '''

    html_section_2 = f'''
        <section style="padding-bottom: 9.6rem;">
            <div class="container-xl">
                <h2>Medicinal Herbs and Their Uses</h2>
                <div class="m-flex" style="justify-content: space-between;">
                    <p style="max-width: 720px;">
                        <strong>Medicinal herbs</strong> are plants that contain natural compounds traditionally used to support health and well-being. 
                        Their properties depend on the plant species, the part used, and the way the herb is prepared.
                    </p>
                    <div>
                        <a class="button-default" href="/herbs.html">View All Herbs</a>
                    </div>
                </div>
                <div class="m-flex" style="gap: 4.8rem; margin-top: 4.8rem;">
                    <div style="flex: 1;">
                        <h3>What Makes a Plant Medicinal?</h3>
                        <p>
                        A plant is considered medicinal when it contains bioactive compounds that have been traditionally used to support the body. 
                        These compounds may include essential oils, flavonoids, bitters, or alkaloids.
                        </p>
                    </div>
                    <div style="flex: 1;">
                        <h3>Plant Parts Used in Herbalism</h3>
                        <p style="margin-bottom: 1.6rem;">
                            Different parts of a medicinal plant are used in herbalism depending on where the active compounds are concentrated.
                        </p>
                        <ul>
                          <li><strong>Leaves and flowers</strong>: often used for teas and infusions</li>
                          <li><strong>Roots and rhizomes</strong>: commonly prepared as decoctions or tinctures</li>
                          <li><strong>Seeds and fruits</strong>: used for oils, powders, or teas</li>
                          <li><strong>Bark and resins</strong>: valued for concentrated herbal preparations</li>
                        </ul>
                    </div>
                    <div style="flex: 1;">
                        <h3>General Categories of Herbal Use</h3>
                        <p style="margin-bottom: 1.6rem;">
                        Medicinal herbs are commonly grouped by the type of support they have traditionally been used to provide.
                        </p>
                        <ul>
                          <li>Digestive support</li>
                          <li>Immune support</li>
                          <li>Relaxation and sleep support</li>
                          <li>Skin care and topical use</li>
                          <li>Respiratory support</li>
                        </ul>
                    </div>
                <div>
            </div>
        </section>
    '''

    html_section_3 = f'''
        <section style="padding-bottom: 9.6rem;">
            <div class="container-xl">
                <h2 style="max-width: 720px;">Herbal Remedies and Preparation Methods</h2>
                <div class="m-flex" style="justify-content: space-between;">
                    <p style="max-width: 720px;">
                        <strong>Herbal remedies</strong> are made by preparing medicinal herbs in specific ways to make their beneficial compounds available for use. 
                        Common preparation methods include teas, tinctures, salves, oils, and syrups, each suited to different herbs and purposes.
                    </p>
                    <div>
                        <a class="button-default" href="/herbs.html">Learn All Preparations</a>
                    </div>
                </div>
                <div class="m-flex" style="gap: 4.8rem; margin-top: 4.8rem;">
                    <div style="flex: 1;">
<h3>Types of Herbal Preparation Methods</h3>
<p>
Herbal remedies are prepared using different methods depending on the plant material, the desired strength, and how the remedy will be used.
</p>

<ul>
  <li><strong>Teas and infusions</strong>: gentle preparations made with hot water</li>
  <li><strong>Decoctions</strong>: simmered preparations for roots and bark</li>
  <li><strong>Tinctures</strong>: concentrated extracts made with alcohol or glycerin</li>
  <li><strong>Salves and balms</strong>: topical remedies made with infused oils and wax</li>
  <li><strong>Infused oils</strong>: herbs steeped in oil for external use</li>
</ul>
                    </div>
                    <div style="flex: 1;">
<h3>What Is a Home Apothecary?</h3>
<p>
A <strong>home apothecary</strong> is a personal collection of herbs, remedies, and tools used to prepare and store herbal preparations at home. 
It typically includes dried herbs, jars, measuring tools, and basic supplies for making simple remedies.
</p>
                    </div>
                    <div style="flex: 1;">
<h3>Herbal Preparation for Beginners</h3>
<p>
Beginners often start with simple herbal preparations such as teas, infused oils, and basic salves. 
These methods require minimal equipment and allow new herbalists to learn safely while building confidence.
</p>
                    </div>
                <div>
            </div>
        </section>
    '''



    intro_html = f'''
        <section style="padding-top: 9.6rem; padding-bottom: 9.6rem;">
            <div class="container-xl">
                <h2 style="text-align: center; margin-bottom: 4.8rem;">Understand the World of Herbal Medicine</h2>
                <div class="grid-3" style="gap: 4.8rem;">
                    <div>
                        <h3 style="margin-bottom: 1.6rem;">What Is Herbal Medicine?</h3>
                        <p>
                          Herbal medicine is the practice of using plants and plant extracts to support health and wellness. Rooted in centuries of tradition, it combines natural remedies with modern scientific insights. From calming teas to potent tinctures, herbs offer a wide range of therapeutic benefits. 
                        </p>
                    </div>
                    <div>
                        <h3 style="margin-bottom: 1.6rem;">History & Tradition</h3>
                        <p>
                          Herbs have shaped healing practices across cultures, from traditional Chinese medicine and Ayurveda to Indigenous ethnobotany worldwide. Exploring these historical and cultural contexts deepens our understanding of herbal medicine's enduring role in wellness. 
                        </p>
                    </div>
                    <div>
                        <h3 style="margin-bottom: 1.6rem;">Modern Applications</h3>
                        <p>
                          Today, herbal medicine intersects with modern science through research on bioactive compounds, clinical studies, and evidence-based therapies. Herbs are studied for their roles in immunity, stress management, digestion, and overall vitality. 
                        </p>
                    </div>
                </div>
            </div>
        </section>
    '''

    color_carbon_powder = '#101211'
    section_2_html = f'''
        <section style="padding-top: 9.6rem; padding-bottom: 9.6rem; background-color: {color_carbon_powder};">
            <div class="container-xl" style="color: #ffffff;">
                <h2 style="text-align: center; margin-bottom: 4.8rem;">Explore Core Areas of Herbal Medicine</h2>
                <div class="grid-3" style="gap: 4.8rem;">
                    <div>
                        <h3 style="margin-bottom: 1.6rem;">Medicinal Herbs</h3>
                        <p>Discover our complete index of medicinal plants, from common kitchen herbs like ginger and turmeric to clinically studied botanicals such as ashwagandha and echinacea. Each profile explores traditional uses, active compounds, scientific research, and safe applications. Begin your journey by exploring the Medicinal Herbs Hub.</p>
                        <div style="margin-top: 1.6rem;">
                            <a class="button-invert" href="/herbs.html">Medicinal Herbs Hub</a>
                        </div>
                    </div>
                    <div>
                        <h3 style="margin-bottom: 1.6rem;">Ailments</h3>
                        <p>Learn how herbal medicine supports specific health goals. From calming the nervous system and promoting better sleep, to supporting digestive health, immunity, and skin balance, our condition-based guides connect symptoms to well-studied herbal remedies. Visit the Ailments Hub to explore natural options tailored to your needs.</p>
                        <div style="margin-top: 1.6rem;">
                            <a class="button-invert" href="/ailments.html">Ailments Hub</a>
                        </div>
                    </div>
                    <div>
                        <h3 style="margin-bottom: 1.6rem;">Preparations</a></h3>
                        <p>The way herbs are prepared affects their potency and benefits. Explore tutorials on making herbal teas, tinctures, salves, capsules, and more. Whether you're a beginner or an experienced herbalist, our Preparations Hub will guide you through safe, effective, and traditional techniques and methods.</p>
                        <div style="margin-top: 1.6rem;">
                            <a class="button-invert" href="/preparations.html">Preparations Hub</a>
                        </div>
                    </div>
                </div>
            </div>
        </section>
    '''

    herbs_popular = data.herbs_popular_get('teas', 15)
    cards = ''
    for herb in herbs_popular:
        herb_name_scientific = herb['herb_name_scientific']
        if herb_name_scientific == 'mentha piperita':
            herb_name_scientific = 'mentha x piperita'
        herb_slug = polish.sluggify(herb_name_scientific)
        img_src = f'/images/herbs/{herb_slug}.jpg'
        img_alt = f'{herb_name_scientific}'
        card = f'''
            <div>
                <h3 style="margin-bottom: 1.6rem;">{herb_name_scientific.capitalize()}</h3>
                <img src="{img_src}" alt="{img_alt}">
                <div style="margin-top: 1.6rem;">
                    <a class="button-default-ghost" href="/herbs/{herb_slug}.html">{herb_name_scientific.capitalize()}</a>
                </div>
            </div>
        '''
        cards += card
    section_3_html = f'''
        <section style="padding-top: 9.6rem; padding-bottom: 9.6rem;">
            <div class="container-xl">
                <h2 style="text-align: center; margin-bottom: 4.8rem;">Explore The Most Used Medicinal Herbs</h2>
                <div class="grid-3" style="gap: 4.8rem;">
                    {cards}
                </div>
            </div>
        </section>
    '''

    meta_title = f'''Herbalism & Herbal Remedies for Natural Healing | Terra Whisper'''
    meta_description = f'''Learn herbalism from the ground up. Discover medicinal herbs, herbal remedies, apothecary methods, and beginner-friendly natural healing guides.'''
    
    html = f'''
        <!DOCTYPE html>
        <html lang="en">
        {components.html_head(meta_title, meta_description, css='/style.css')}
        <body class="home">
            {sections.header_default()}
            {html_hero}
            {html_placeholders}
            {sections.footer()}
        </body>
        </html>
    '''
            # {html_section_1}
            # {html_section_2}
            # {html_section_3}
    html_filepath = f'''{g.website_folderpath}/index.html'''
    with open(html_filepath, 'w') as f: f.write(html)

