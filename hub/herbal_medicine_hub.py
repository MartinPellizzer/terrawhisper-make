import os
import random
import json

from lib import g
from lib import io
from lib import llm
from lib import data
from lib import polish
from lib import components
from lib import sections

def subordinate__gen(json_article_filepath, key, entity, attribute, context='herbal medicine', regen=False, dispel=False):
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
                I'm writing an article about the core entity "{entity}", which is for a website where the source context is "{context}". 
                I want you to write the subordinate text for the following section: 
                "{attribute}"
                The subordinate text is the first sentence that must be written immediately after the headline. 
                The subordinate text must answer in the most direct, clear, detailed way possible without fluff.
                Don't give me bold or italicized text. 
                Reply only with the subordinate text.
                /no_think
            ''').strip()
            reply = llm.reply(prompt)
            if '</think>' in reply:
                reply = reply.split('</think>')[1].strip()
            reply = polish.vanilla(reply)
            json_article[key] = reply
            io.json_write(json_article_filepath, json_article)
            print(json_article_filepath)
    ### html
    html = f'''
        {json_article[key]}
    '''
    return html

def herbal_medicine__gen():
    url_slug = f'herbal-medicine'
    meta_title = f'Herbal Medicine'
    meta_description = ''
    canonical_html = f'''<link rel="canonical" href="https://terrawhisper.com/{url_slug}.html">'''

    ########################################
    # json
    ########################################
    json_article_filepath = f'''{g.DATABASE_FOLDERPATH}/json/{url_slug}.json'''
    json_article = io.json_read(json_article_filepath, create=True)
    json_article['url'] = url_slug
    io.json_write(json_article_filepath, json_article)

    definition_subordinate_html = subordinate__gen(json_article_filepath, 
        key='definition', 
        entity='herbal medicine', attribute='definition', context='herbal medicine', 
        regen=False, dispel=False
    )
    principles_subordinate_html = subordinate__gen(json_article_filepath, 
        key='principles', 
        entity='herbal medicine', attribute='principles', context='herbal medicine', 
        regen=False, dispel=False
    )
    history_subordinate_html = subordinate__gen(json_article_filepath, 
        key='history', 
        entity='herbal medicine', attribute='history', context='herbal medicine', 
        regen=False, dispel=False
    )
    traditions_subordinate_html = subordinate__gen(json_article_filepath, 
        key='traditions', 
        entity='herbal medicine', attribute='traditions', context='herbal medicine', 
        regen=False, dispel=False
    )
    herbs_subordinate_html = subordinate__gen(json_article_filepath, 
        key='herbs', 
        entity='herbal medicine', attribute='medicinal plants', context='herbal medicine', 
        regen=False, dispel=False
    )
    phytochemicals_subordinate_html = subordinate__gen(json_article_filepath, 
        key='phytochemicals', 
        entity='herbal medicine', attribute='phytochemicals', context='herbal medicine', 
        regen=False, dispel=False
    )
    pharmacology_subordinate_html = subordinate__gen(json_article_filepath, 
        key='pharmacology', 
        entity='herbal medicine', attribute='pharmacology', context='herbal medicine', 
        regen=False, dispel=False
    )
    applications_subordinate_html = subordinate__gen(json_article_filepath, 
        key='applications', 
        entity='herbal medicine', attribute='applications', context='herbal medicine', 
        regen=False, dispel=False
    )
    preparations_subordinate_html = subordinate__gen(json_article_filepath, 
        key='preparations', 
        entity='herbal medicine', attribute='preparations', context='herbal medicine', 
        regen=False, dispel=False
    )
    administration_subordinate_html = subordinate__gen(json_article_filepath, 
        key='administration', 
        entity='herbal medicine', attribute='administration', context='herbal medicine', 
        regen=False, dispel=False
    )
    dosage_subordinate_html = subordinate__gen(json_article_filepath, 
        key='dosage', 
        entity='herbal medicine', attribute='dosage', context='herbal medicine', 
        regen=False, dispel=False
    )
    safety_subordinate_html = subordinate__gen(json_article_filepath, 
        key='safety', 
        entity='herbal medicine', attribute='safety', context='herbal medicine', 
        regen=False, dispel=False
    )
    quality_subordinate_html = subordinate__gen(json_article_filepath, 
        key='quality', 
        entity='herbal medicine', attribute='quality', context='herbal medicine', 
        regen=False, dispel=False
    )
    cultivation_subordinate_html = subordinate__gen(json_article_filepath, 
        key='cultivation', 
        entity='herbal medicine', attribute='cultivation', context='herbal medicine', 
        regen=False, dispel=False
    )
    processing_subordinate_html = subordinate__gen(json_article_filepath, 
        key='processing', 
        entity='herbal medicine', attribute='processing', context='herbal medicine', 
        regen=False, dispel=False
    )
    research_subordinate_html = subordinate__gen(json_article_filepath, 
        key='research', 
        entity='herbal medicine', attribute='research', context='herbal medicine', 
        regen=False, dispel=False
    )
    regulation_subordinate_html = subordinate__gen(json_article_filepath, 
        key='regulation', 
        entity='herbal medicine', attribute='regulation', context='herbal medicine', 
        regen=False, dispel=False
    )
    sustainability_subordinate_html = subordinate__gen(json_article_filepath, 
        key='sustainability', 
        entity='herbal medicine', attribute='sustainability', context='herbal medicine', 
        regen=False, dispel=False
    )
    education_subordinate_html = subordinate__gen(json_article_filepath, 
        key='education', 
        entity='herbal medicine', attribute='education', context='herbal medicine', 
        regen=False, dispel=False
    )

    ########################################
    # html
    ########################################
    intro_html = f'''
        <h1>
            Herbal Medicine
        </h1>
        <p>
            Herbal medicine is a form of healthcare that uses plant-derived substances such as leaves, roots, flowers, and seeds to prevent, treat, or manage health conditions. It is practiced in medical traditions such as Traditional Chinese Medicine, Ayurveda, and Western herbalism, where medicinal plants are prepared as teas, tinctures, extracts, and topical remedies to influence physiological processes through bioactive compounds.
        </p>
    '''
    definition_html = f'''
        <section class="article-section">
            <h2>Definition</h2>
            <p>{definition_subordinate_html}</p>
        </section>
    '''
    principles_html = f'''
        <section class="article-section">
            <h2>Principles</h2>
            <p>{principles_subordinate_html}</p>
        </section>
    '''
    history_html = f'''
        <section class="article-section">
            <h2>Histrory</h2>
            <p>{history_subordinate_html}</p>
        </section>
    '''
    traditions_html = f'''
        <section class="article-section">
            <h2>Traditions</h2>
            <p>{traditions_subordinate_html}</p>
        </section>
    '''
    herbs_html = f'''
        <section class="article-section">
            <h2>Medicinal Plants</h2>
            <p>{herbs_subordinate_html}</p>
            <p><a href="/herbs.html">Medicinal Plants</a></p>
        </section>
    '''
    phytochemicals_html = f'''
        <section class="article-section">
            <h2>Phytochemicals</h2>
            <p>{phytochemicals_subordinate_html}</p>
            <p><a href="/phytochemicals.html">Phytochemicals</a></p>
        </section>
    '''
    pharmacology_html = f'''
        <section class="article-section">
            <h2>Pharmacology</h2>
            <p>{pharmacology_subordinate_html}</p>
        </section>
    '''
    applications_html = f'''
        <section class="article-section">
            <h2>Applications</h2>
            <p>{applications_subordinate_html}</p>
        </section>
    '''
    preparations_html = f'''
        <section class="article-section">
            <h2>Preparations</h2>
            <p>{preparations_subordinate_html}</p>
        </section>
    '''
    administration_html = f'''
        <section class="article-section">
            <h2>Administration</h2>
            <p>{administration_subordinate_html}</p>
        </section>
    '''
    dosage_html = f'''
        <section class="article-section">
            <h2>Dosage</h2>
            <p>{dosage_subordinate_html}</p>
        </section>
    '''
    safety_html = f'''
        <section class="article-section">
            <h2>Safety</h2>
            <p>{safety_subordinate_html}</p>
        </section>
    '''
    quality_html = f'''
        <section class="article-section">
            <h2>Quality</h2>
            <p>{quality_subordinate_html}</p>
        </section>
    '''
    cultivation_html = f'''
        <section class="article-section">
            <h2>Cultivation</h2>
            <p>{cultivation_subordinate_html}</p>
        </section>
    '''
    processing_html = f'''
        <section class="article-section">
            <h2>Processing</h2>
            <p>{processing_subordinate_html}</p>
        </section>
    '''
    research_html = f'''
        <section class="article-section">
            <h2>Research</h2>
            <p>{research_subordinate_html}</p>
        </section>
    '''
    regulation_html = f'''
        <section class="article-section">
            <h2>Regulation</h2>
            <p>{regulation_subordinate_html}</p>
        </section>
    '''
    sustainability_html = f'''
        <section class="article-section">
            <h2>Sustainability</h2>
            <p>{sustainability_subordinate_html}</p>
        </section>
    '''
    education_html = f'''
        <section class="article-section">
            <h2>Education</h2>
            <p>{education_subordinate_html}</p>
        </section>
    '''

    article_html = f'''
        {intro_html}
        {definition_html}
        {principles_html}
        {history_html}
        {traditions_html}
        {herbs_html}
        {phytochemicals_html}
        {pharmacology_html}
        {applications_html}
        {preparations_html}
        {administration_html}
        {dosage_html}
        {safety_html}
        {quality_html}
        {cultivation_html}
        {processing_html}
        {research_html}
        {regulation_html}
        {sustainability_html}
        {education_html}
    '''

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
                    {article_html}
                </article>
            </main>
            {sections.footer()}
        </body>
        </html>
    ''').strip()
    html_filepath = f'''{g.website_folderpath}/{url_slug}.html'''
    with open(html_filepath, 'w') as f: f.write(html)

def herbs__gen():
    url_slug = f'herbs'
    meta_title = f'Medicinal Plants'
    meta_description = ''
    canonical_html = f'''<link rel="canonical" href="https://terrawhisper.com/{url_slug}.html">'''

    ########################################
    # json
    ########################################
    json_article_filepath = f'''{g.DATABASE_FOLDERPATH}/json/{url_slug}.json'''
    json_article = io.json_read(json_article_filepath, create=True)
    json_article['url'] = url_slug
    io.json_write(json_article_filepath, json_article)

    definition_subordinate_html = subordinate__gen(json_article_filepath, 
        key='definition', 
        entity='medicinal plants', attribute='definition', context='herbal medicine', 
        regen=False, dispel=False
    )
    classification_subordinate_html = subordinate__gen(json_article_filepath, 
        key='classification', 
        entity='medicinal plants', attribute='classification', context='herbal medicine', 
        regen=False, dispel=False
    )
    parts_subordinate_html = subordinate__gen(json_article_filepath, 
        key='parts', 
        entity='medicinal plants', attribute='parts', context='herbal medicine', 
        regen=False, dispel=False
    )
    compounds_subordinate_html = subordinate__gen(json_article_filepath, 
        key='compounds', 
        entity='medicinal plants', attribute='compounds', context='herbal medicine', 
        regen=False, dispel=False
    )
    actions_subordinate_html = subordinate__gen(json_article_filepath, 
        key='actions', 
        entity='medicinal plants', attribute='actions', context='herbal medicine', 
        regen=False, dispel=False
    )
    uses_subordinate_html = subordinate__gen(json_article_filepath, 
        key='uses', 
        entity='medicinal plants', attribute='uses', context='herbal medicine', 
        regen=False, dispel=False
    )
    preparations_subordinate_html = subordinate__gen(json_article_filepath, 
        key='preparations', 
        entity='medicinal plants', attribute='preparations', context='herbal medicine', 
        regen=False, dispel=False
    )
    dosage_subordinate_html = subordinate__gen(json_article_filepath, 
        key='dosage', 
        entity='medicinal plants', attribute='dosage', context='herbal medicine', 
        regen=False, dispel=False
    )
    safety_subordinate_html = subordinate__gen(json_article_filepath, 
        key='safety', 
        entity='medicinal plants', attribute='safety', context='herbal medicine', 
        regen=False, dispel=False
    )
    identification_subordinate_html = subordinate__gen(json_article_filepath, 
        key='identification', 
        entity='medicinal plants', attribute='identification', context='herbal medicine', 
        regen=False, dispel=False
    )
    cultivation_subordinate_html = subordinate__gen(json_article_filepath, 
        key='cultivation', 
        entity='medicinal plants', attribute='cultivation', context='herbal medicine', 
        regen=False, dispel=False
    )
    harvesting_subordinate_html = subordinate__gen(json_article_filepath, 
        key='harvesting', 
        entity='medicinal plants', attribute='harvesting', context='herbal medicine', 
        regen=False, dispel=False
    )
    processing_subordinate_html = subordinate__gen(json_article_filepath, 
        key='processing', 
        entity='medicinal plants', attribute='processing', context='herbal medicine', 
        regen=False, dispel=False
    )
    storage_subordinate_html = subordinate__gen(json_article_filepath, 
        key='storage', 
        entity='medicinal plants', attribute='storage', context='herbal medicine', 
        regen=False, dispel=False
    )
    research_subordinate_html = subordinate__gen(json_article_filepath, 
        key='research', 
        entity='medicinal plants', attribute='research', context='herbal medicine', 
        regen=False, dispel=False
    )
    regulation_subordinate_html = subordinate__gen(json_article_filepath, 
        key='regulation', 
        entity='medicinal plants', attribute='regulation', context='herbal medicine', 
        regen=False, dispel=False
    )
    sustainability_subordinate_html = subordinate__gen(json_article_filepath, 
        key='sustainability', 
        entity='medicinal plants', attribute='sustainability', context='herbal medicine', 
        regen=False, dispel=False
    )

    ########################################
    # html
    ########################################
    intro_html = f'''
        <h1>
            Medicinal Plants
        </h1>
        <p>
            A medicinal plant is a plant species used for therapeutic purposes because it contains biologically active compounds that influence human health. These plants are the primary raw materials of <a href="/herbal-medicine.html">herbal medicine</a> and are used to prepare remedies such as teas, tinctures, extracts, and topical formulations. Medicinal plants have been used for thousands of years across medical systems such as Ayurveda, Traditional Chinese Medicine, and Western herbalism.
        </p>
    '''
    definition_html = f'''
        <section class="article-section">
            <h2>Definition</h2>
            <p>{definition_subordinate_html}</p>
        </section>
    '''
    classification_html = f'''
        <section class="article-section">
            <h2>Classification</h2>
            <p>{classification_subordinate_html}</p>
        </section>
    '''
    parts_html = f'''
        <section class="article-section">
            <h2>Parts</h2>
            <p>{parts_subordinate_html}</p>
        </section>
    '''
    compounds_html = f'''
        <section class="article-section">
            <h2>Compounds</h2>
            <p>{compounds_subordinate_html}</p>
            <p><a href="/phytochemicals.html">Phytochemicals</a></p>
        </section>
    '''
    actions_html = f'''
        <section class="article-section">
            <h2>Actions</h2>
            <p>{actions_subordinate_html}</p>
        </section>
    '''
    uses_html = f'''
        <section class="article-section">
            <h2>Uses</h2>
            <p>{uses_subordinate_html}</p>
        </section>
    '''
    preparations_html = f'''
        <section class="article-section">
            <h2>Preparations</h2>
            <p>{preparations_subordinate_html}</p>
        </section>
    '''
    dosage_html = f'''
        <section class="article-section">
            <h2>Dosage</h2>
            <p>{dosage_subordinate_html}</p>
        </section>
    '''
    safety_html = f'''
        <section class="article-section">
            <h2>Safety</h2>
            <p>{safety_subordinate_html}</p>
        </section>
    '''
    identification_html = f'''
        <section class="article-section">
            <h2>Identification</h2>
            <p>{identification_subordinate_html}</p>
        </section>
    '''
    cultivation_html = f'''
        <section class="article-section">
            <h2>Cultivation</h2>
            <p>{cultivation_subordinate_html}</p>
        </section>
    '''
    harvesting_html = f'''
        <section class="article-section">
            <h2>Harvesting</h2>
            <p>{harvesting_subordinate_html}</p>
        </section>
    '''
    processing_html = f'''
        <section class="article-section">
            <h2>Processing</h2>
            <p>{processing_subordinate_html}</p>
        </section>
    '''
    storage_html = f'''
        <section class="article-section">
            <h2>Storage</h2>
            <p>{storage_subordinate_html}</p>
        </section>
    '''
    research_html = f'''
        <section class="article-section">
            <h2>Research</h2>
            <p>{research_subordinate_html}</p>
        </section>
    '''
    regulation_html = f'''
        <section class="article-section">
            <h2>Regulation</h2>
            <p>{regulation_subordinate_html}</p>
        </section>
    '''
    sustainability_html = f'''
        <section class="article-section">
            <h2>Sustainability</h2>
            <p>{sustainability_subordinate_html}</p>
        </section>
    '''

    article_html = f'''
        {intro_html}
        {definition_html}
        {classification_html}
        {parts_html}
        {compounds_html}
        {actions_html}
        {uses_html}
        {preparations_html}
        {dosage_html}
        {safety_html}
        {identification_html}
        {cultivation_html}
        {harvesting_html}
        {processing_html}
        {storage_html}
        {research_html}
        {regulation_html}
        {sustainability_html}
    '''
    '''

    '''

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
                    {article_html}
                </article>
            </main>
            {sections.footer()}
        </body>
        </html>
    ''').strip()
    html_filepath = f'''{g.website_folderpath}/{url_slug}.html'''
    with open(html_filepath, 'w') as f: f.write(html)

def phytochemicals__gen():
    url_slug = f'phytochemicals'
    meta_title = f'Phytochemicals'
    meta_description = ''
    canonical_html = f'''<link rel="canonical" href="https://terrawhisper.com/{url_slug}.html">'''

    ########################################
    # json
    ########################################
    json_article_filepath = f'''{g.DATABASE_FOLDERPATH}/json/{url_slug}.json'''
    json_article = io.json_read(json_article_filepath, create=True)
    json_article['url'] = url_slug
    io.json_write(json_article_filepath, json_article)

    definition_subordinate_html = subordinate__gen(json_article_filepath, 
        key='definition', 
        entity='phytochemicals', attribute='definition', context='herbal medicine', 
        regen=False, dispel=False
    )
    function_subordinate_html = subordinate__gen(json_article_filepath, 
        key='function', 
        entity='phytochemicals', attribute='function', context='herbal medicine', 
        regen=False, dispel=False
    )
    classification_subordinate_html = subordinate__gen(json_article_filepath, 
        key='classification', 
        entity='phytochemicals', attribute='classification', context='herbal medicine', 
        regen=False, dispel=False
    )
    biosynthesis_subordinate_html = subordinate__gen(json_article_filepath, 
        key='biosynthesis', 
        entity='phytochemicals', attribute='biosynthesis', context='herbal medicine', 
        regen=False, dispel=False
    )
    pharmacology_subordinate_html = subordinate__gen(json_article_filepath, 
        key='pharmacology', 
        entity='phytochemicals', attribute='pharmacological effects', context='herbal medicine', 
        regen=False, dispel=False
    )
    therapy_subordinate_html = subordinate__gen(json_article_filepath, 
        key='therapy', 
        entity='phytochemicals', attribute='therapeutic roles', context='herbal medicine', 
        regen=False, dispel=False
    )
    source_subordinate_html = subordinate__gen(json_article_filepath, 
        key='source', 
        entity='phytochemicals', attribute='plant sources', context='herbal medicine', 
        regen=False, dispel=False
    )
    extraction_subordinate_html = subordinate__gen(json_article_filepath, 
        key='extraction', 
        entity='phytochemicals', attribute='extraction methods', context='herbal medicine', 
        regen=False, dispel=False
    )
    stability_subordinate_html = subordinate__gen(json_article_filepath, 
        key='stability', 
        entity='phytochemicals', attribute='factors affecting phytochemical content', context='herbal medicine', 
        regen=False, dispel=False
    )
    bioavailability_subordinate_html = subordinate__gen(json_article_filepath, 
        key='bioavailability', 
        entity='phytochemicals', attribute='bioavailability', context='herbal medicine', 
        regen=False, dispel=False
    )
    safety_subordinate_html = subordinate__gen(json_article_filepath, 
        key='safety', 
        entity='phytochemicals', attribute='safety', context='herbal medicine', 
        regen=False, dispel=False
    )
    research_subordinate_html = subordinate__gen(json_article_filepath, 
        key='research', 
        entity='phytochemicals', attribute='research', context='herbal medicine', 
        regen=False, dispel=False
    )
    industry_subordinate_html = subordinate__gen(json_article_filepath, 
        key='industry', 
        entity='phytochemicals', attribute='industrial applications', context='herbal medicine', 
        regen=False, dispel=False
    )
    ecology_subordinate_html = subordinate__gen(json_article_filepath, 
        key='ecology', 
        entity='phytochemicals', attribute='ecology', context='herbal medicine', 
        regen=False, dispel=False
    )

    ########################################
    # html
    ########################################
    intro_html = f'''
        <h1>
            Phytochemicals: Plant Compounds in Herbal Medicine
        </h1>
        <p>
            Phytochemicals are naturally occurring chemical compounds produced by plants, particularly as secondary metabolites involved in defense, signaling, and environmental adaptation. In <a href="/herbal-medicine.html">herbal medicine</a>, phytochemicals such as alkaloids, flavonoids, terpenoids, and phenolic compounds are responsible for many therapeutic effects because they interact with biological systems to produce antioxidant, anti-inflammatory, antimicrobial, and other pharmacological activities.
        </p>
    '''
    definition_html = f'''
        <section class="article-section">
            <h2>Definition</h2>
            <p>{definition_subordinate_html}</p>
        </section>
    '''
    function_html = f'''
        <section class="article-section">
            <h2>Function</h2>
            <p>{function_subordinate_html}</p>
        </section>
    '''
    classification_html = f'''
        <section class="article-section">
            <h2>Classification</h2>
            <p>{classification_subordinate_html}</p>
            <p><a href="/phytochemicals/classification.html">Classification</a></p>
        </section>
    '''
    biosynthesis_html = f'''
        <section class="article-section">
            <h2>Biosynthesis</h2>
            <p>{biosynthesis_subordinate_html}</p>
        </section>
    '''
    pharmacology_html = f'''
        <section class="article-section">
            <h2>Pharmacology</h2>
            <p>{pharmacology_subordinate_html}</p>
        </section>
    '''
    therapy_html = f'''
        <section class="article-section">
            <h2>Therapy</h2>
            <p>{therapy_subordinate_html}</p>
        </section>
    '''
    source_html = f'''
        <section class="article-section">
            <h2>Source</h2>
            <p>{source_subordinate_html}</p>
        </section>
    '''
    extraction_html = f'''
        <section class="article-section">
            <h2>Extraction</h2>
            <p>{extraction_subordinate_html}</p>
        </section>
    '''
    stability_html = f'''
        <section class="article-section">
            <h2>Stability</h2>
            <p>{stability_subordinate_html}</p>
        </section>
    '''
    bioavailability_html = f'''
        <section class="article-section">
            <h2>Bioavailability</h2>
            <p>{bioavailability_subordinate_html}</p>
        </section>
    '''
    safety_html = f'''
        <section class="article-section">
            <h2>Safety</h2>
            <p>{safety_subordinate_html}</p>
        </section>
    '''
    research_html = f'''
        <section class="article-section">
            <h2>Research</h2>
            <p>{research_subordinate_html}</p>
        </section>
    '''
    industry_html = f'''
        <section class="article-section">
            <h2>Industry</h2>
            <p>{industry_subordinate_html}</p>
        </section>
    '''
    ecology_html = f'''
        <section class="article-section">
            <h2>Ecology</h2>
            <p>{ecology_subordinate_html}</p>
        </section>
    '''

    article_html = f'''
        {intro_html}
        {definition_html}
        {function_html}
        {classification_html}
        {biosynthesis_html}
        {pharmacology_html}
        {therapy_html}
        {source_html}
        {extraction_html}
        {stability_html}
        {bioavailability_html}
        {safety_html}
        {research_html}
        {industry_html}
        {ecology_html}
    '''
    '''

    '''

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
                    {article_html}
                </article>
            </main>
            {sections.footer()}
        </body>
        </html>
    ''').strip()
    html_filepath = f'''{g.website_folderpath}/{url_slug}.html'''
    with open(html_filepath, 'w') as f: f.write(html)

def phytochemicals__classification__gen():
    url_slug = f'phytochemicals/classification'
    meta_title = f'Phytochemicals Classification'
    meta_description = ''
    canonical_html = f'''<link rel="canonical" href="https://terrawhisper.com/{url_slug}.html">'''
    
    phytochemicals = data.phytochemicals_get()

    ########################################
    # json
    ########################################
    json_article_filepath = f'''{g.DATABASE_FOLDERPATH}/json/{url_slug}.json'''
    json_article = io.json_read(json_article_filepath, create=True)
    json_article['url'] = url_slug
    io.json_write(json_article_filepath, json_article)

    definition_subordinate_html = subordinate__gen(json_article_filepath, 
        key='definition', 
        attribute='definition', entity='phytochemicals', context='herbal medicine', 
        regen=False, dispel=False
    )

    ###
    json_article = io.json_read(json_article_filepath)
    regen = False
    dispel = False
    key = 'list'
    if key not in json_article: json_article[key] = ''
    if regen: json_article[key] = ''
    if dispel: 
        json_article[key] = ''
        io.json_write(json_article_filepath, json_article)
        return
    if json_article[key] == '' or json_article[key] == []:
        phytochemicals_data = []
        for phytochemical in phytochemicals:
            found = False
            for _phytochemical in phytochemicals_data:
                if _phytochemical == phytochemical:
                    found = True
                    break
            if not found:
                _obj = {
                    'entity': phytochemical,
                    'heading': phytochemical,
                    'subordinate': '',
                }
                phytochemicals_data.append(_obj)
        json_article[key] = phytochemicals_data
        io.json_write(json_article_filepath, json_article)
    ###
    for json_item in json_article[key]:
        entity = 'phytochemical classification'
        context = 'herbal medicine'
        attribute = json_item['entity']
        key = 'subordinate'
        if json_item[key] == '':
            if key not in json_item: json_item[key] = ''
            if regen: json_item[key] = ''
            if dispel: 
                json_item[key] = ''
                io.json_write(json_article_filepath, json_item)
            if not dispel:
                if json_item[key] == '':
                    import textwrap
                    prompt = textwrap.dedent(f'''
                        I'm writing an article about the core entity "{entity}", which is for a website where the source context is "{context}". 
                        I want you to write the subordinate text for the following section: 
                        "{attribute}"
                        The subordinate text is the first sentence that must be written immediately after the headline. 
                        The subordinate text must answer in the most direct, clear, detailed way possible without fluff.
                        Don't give me bold or italicized text. 
                        Reply only with the subordinate text.
                        /no_think
                    ''').strip()
                    reply = llm.reply(prompt)
                    if '</think>' in reply:
                        reply = reply.split('</think>')[1].strip()
                    reply = polish.vanilla(reply)
                    json_item[key] = reply
                    io.json_write(json_article_filepath, json_article)
                    print(json_article_filepath)

    ###
    phytochemicals_html = ''
    for phytochemical in json_article['list']:
        phytochemicals_html += f'''
            <h2>
                {phytochemical['heading'].title()}
            </h2>
            <p>
                {phytochemical['subordinate']}
            </p>
        '''

    definition_subordinate_html = subordinate__gen(json_article_filepath, 
        key='definition', 
        attribute='definition', entity='phytochemicals', context='herbal medicine', 
        regen=False, dispel=False
    )
    principles_subordinate_html = subordinate__gen(json_article_filepath, 
        key='principles', 
        attribute='principles', entity='phytochemicals classification', context='herbal medicine', 
        regen=False, dispel=False
    )
    ###
    major_classes_subordinate_html = subordinate__gen(json_article_filepath, 
        key='major_classes', 
        attribute='major classes', entity='phytochemicals classification', context='herbal medicine', 
        regen=False, dispel=False
    )
    alkaloids_subordinate_html = subordinate__gen(json_article_filepath, 
        key='alkaloids', 
        attribute='alkaloids', entity='phytochemicals classification', context='herbal medicine', 
        regen=False, dispel=False
    )
    flavonoids_subordinate_html = subordinate__gen(json_article_filepath, 
        key='flavonoids', 
        attribute='flavonoids', entity='phytochemicals classification', context='herbal medicine', 
        regen=False, dispel=False
    )
    terpenoids_subordinate_html = subordinate__gen(json_article_filepath, 
        key='terpenoids', 
        attribute='terpenoids', entity='phytochemicals classification', context='herbal medicine', 
        regen=False, dispel=False
    )
    phenolic_compounds_subordinate_html = subordinate__gen(json_article_filepath, 
        key='phenolic_compounds', 
        attribute='phenolic compounds', entity='phytochemicals classification', context='herbal medicine', 
        regen=False, dispel=False
    )
    glycosides_subordinate_html = subordinate__gen(json_article_filepath, 
        key='glycosides', 
        attribute='glycosides', entity='phytochemicals classification', context='herbal medicine', 
        regen=False, dispel=False
    )
    tannins_subordinate_html = subordinate__gen(json_article_filepath, 
        key='tannins', 
        attribute='tannins', entity='phytochemicals classification', context='herbal medicine', 
        regen=False, dispel=False
    )
    saponins_subordinate_html = subordinate__gen(json_article_filepath, 
        key='saponins', 
        attribute='saponins', entity='phytochemicals classification', context='herbal medicine', 
        regen=False, dispel=False
    )
    essential_oils_subordinate_html = subordinate__gen(json_article_filepath, 
        key='essential_oils', 
        attribute='essential oils', entity='phytochemicals classification', context='herbal medicine', 
        regen=False, dispel=False
    )
    ###
    structural_classification_subordinate_html = subordinate__gen(json_article_filepath, 
        key='structural_classification', 
        attribute='structural classification', entity='phytochemicals classification', context='herbal medicine', 
        regen=False, dispel=False
    )
    biosynthetic_classification_subordinate_html = subordinate__gen(json_article_filepath, 
        key='biosynthetic_classification', 
        attribute='biosynthetic classification', entity='phytochemicals classification', context='herbal medicine', 
        regen=False, dispel=False
    )
    functional_classification_subordinate_html = subordinate__gen(json_article_filepath, 
        key='functional_classification', 
        attribute='functional classification', entity='phytochemicals classification', context='herbal medicine', 
        regen=False, dispel=False
    )
    plant_distribution_subordinate_html = subordinate__gen(json_article_filepath, 
        key='plant_distribution', 
        attribute='plant distribution', entity='phytochemicals classification', context='herbal medicine', 
        regen=False, dispel=False
    )
    analytical_methods_subordinate_html = subordinate__gen(json_article_filepath, 
        key='analytical_methods', 
        attribute='analytical methods', entity='phytochemicals classification', context='herbal medicine', 
        regen=False, dispel=False
    )
    role_subordinate_html = subordinate__gen(json_article_filepath, 
        key='role', 
        attribute='role', entity='phytochemicals classification', context='herbal medicine', 
        regen=False, dispel=False
    )
    developments_subordinate_html = subordinate__gen(json_article_filepath, 
        key='developments', 
        attribute='developments', entity='phytochemicals classification', context='herbal medicine', 
        regen=False, dispel=False
    )

    ########################################
    # html
    ########################################
    intro_html = f'''
        <h1>
            Phytochemicals: Plant Compounds in Herbal Medicine
        </h1>
        <p>
            Phytochemicals are naturally occurring chemical compounds produced by plants, particularly as secondary metabolites involved in defense, signaling, and environmental adaptation. In <a href="/herbal-medicine.html">herbal medicine</a>, phytochemicals such as alkaloids, flavonoids, terpenoids, and phenolic compounds are responsible for many therapeutic effects because they interact with biological systems to produce antioxidant, anti-inflammatory, antimicrobial, and other pharmacological activities.
        </p>
    '''
    definition_html = f'''
        <section class="article-section">
            <h2>Definition</h2>
            <p>{definition_subordinate_html}</p>
        </section>
    '''
    principles_html = f'''
        <section class="article-section">
            <h2>Principles</h2>
            <p>{principles_subordinate_html}</p>
        </section>
    '''
    ###
    major_classes_html = f'''
        <section class="article-section">
            <h2>Major Classes</h2>
            <p>{major_classes_subordinate_html}</p>
            <p>The list below shows some of the most important major phytochemical classes in herbal medicine.</p>
            <ul>
                <li>Alkaloids</li>
                <li>Flavonoids</li>
                <li>Terpenoids</li>
                <li>Phenolic Compounds</li>
                <li>Glycosides</li>
                <li>Tannins</li>
                <li>Saponins</li>
                <li>Essential Oils</li>
            </ul>
        </section>
    '''
    alkaloids_html = f'''
        <h3>Alkaloids</h3>
        <p>{alkaloids_subordinate_html.replace('Alkaloids', '<a href="/phytochemicals/alkaloids.html">Alkaloids</a>')}</p>
    '''
    flavonoids_html = f'''
        <h3>Flavonoids</h3>
        <p>{flavonoids_subordinate_html.replace('Flavonoids', '<a href="/phytochemicals/flavonoids.html">Flavonoids</a>')}</p>
    '''
    terpenoids_html = f'''
        <h3>Terpenoids</h3>
        <p>{terpenoids_subordinate_html.replace('Terpenoids', '<a href="/phytochemicals/terpenoids.html">Terpenoids</a>')}</p>
    '''
    phenolic_compounds_html = f'''
        <h3>Phenolic Compounds</h3>
        <p>{phenolic_compounds_subordinate_html.replace('Phenolic compounds', '<a href="/phytochemicals/phenolic-compounds.html">Phenolic compounds</a>')}</p>
    '''
    glycosides_html = f'''
        <h3>Glycosides</h3>
        <p>{glycosides_subordinate_html.replace('Glycosides', '<a href="/phytochemicals/glycosides.html">Glycosides</a>')}</p>
    '''
    tannins_html = f'''
        <h3>Tannins</h3>
        <p>{tannins_subordinate_html.replace('Tannins', '<a href="/phytochemicals/tannins.html">Tannins</a>')}</p>
    '''
    saponins_html = f'''
        <h3>Saponins</h3>
        <p>{saponins_subordinate_html.replace('Saponins', '<a href="/phytochemicals/saponins.html">Saponins</a>')}</p>
    '''
    essential_oils_html = f'''
        <h3>Essential Oils</h3>
        <p>{essential_oils_subordinate_html.replace('Essential oils', '<a href="/phytochemicals/essential-oils.html">Essential oils</a>')}</p>
    '''
    ###
    structural_classification_html = f'''
        <section class="article-section">
            <h2>Structural Classification</h2>
            <p>{structural_classification_subordinate_html}</p>
        </section>
    '''
    biosynthetic_classification_html = f'''
        <section class="article-section">
            <h2>Biosynthetic Classification</h2>
            <p>{biosynthetic_classification_subordinate_html}</p>
        </section>
    '''
    functional_classification_html = f'''
        <section class="article-section">
            <h2>Functional Classification</h2>
            <p>{functional_classification_subordinate_html}</p>
        </section>
    '''
    plant_distribution_html = f'''
        <section class="article-section">
            <h2>Plant Distribution</h2>
            <p>{plant_distribution_subordinate_html}</p>
        </section>
    '''
    analytical_methods_html = f'''
        <section class="article-section">
            <h2>Analytical Methods</h2>
            <p>{analytical_methods_subordinate_html}</p>
        </section>
    '''
    role_html = f'''
        <section class="article-section">
            <h2>Role</h2>
            <p>{role_subordinate_html}</p>
        </section>
    '''
    developments_html = f'''
        <section class="article-section">
            <h2>Developments</h2>
            <p>{developments_subordinate_html}</p>
        </section>
    '''

    article_html = f'''
        {intro_html}
        {definition_html}
        {principles_html}
        {major_classes_html}
            {alkaloids_html}
            {flavonoids_html}
            {terpenoids_html}
            {phenolic_compounds_html}
            {glycosides_html}
            {tannins_html}
            {saponins_html}
            {essential_oils_html}
        {structural_classification_html}
        {biosynthetic_classification_html}
        {functional_classification_html}
        {plant_distribution_html}
        {analytical_methods_html}
        {role_html}
        {developments_html}
    '''
    '''
Phytochemical Classification
│
├─ Major Phytochemical Classes
│   ├─ Alkaloids
│   ├─ Flavonoids
│   ├─ Terpenoids
│   ├─ Phenolic Compounds
│   ├─ Glycosides
│   ├─ Tannins
│   ├─ Saponins
│   └─ Essential Oils
├─ Structural Classification
├─ Biosynthetic Classification
├─ Functional Classification
├─ Plant Distribution
├─ Analytical Methods
├─ Role in Herbal Medicine
└─ Modern Developments

    '''

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
                    {article_html}
                </article>
            </main>
            {sections.footer()}
        </body>
        </html>
    ''').strip()
    html_filepath = f'''{g.website_folderpath}/{url_slug}.html'''
    io.folder_create_from_filepath(html_filepath)
    with open(html_filepath, 'w') as f: f.write(html)

def phytochemicals__phytochemical__gen(phytochemical):
    phytochemical_slug = phytochemical.replace(' ', '-')
    url_slug = f'phytochemicals/{phytochemical_slug}'
    meta_title = f'Phytochemicals {phytochemical.title()}'
    meta_description = ''
    canonical_html = f'''<link rel="canonical" href="https://terrawhisper.com/{url_slug}.html">'''
    
    ########################################
    # json
    ########################################
    json_article_filepath = f'''{g.DATABASE_FOLDERPATH}/json/{url_slug}.json'''
    json_article = io.json_read(json_article_filepath, create=True)
    json_article['url'] = url_slug
    io.json_write(json_article_filepath, json_article)

    ###
    intro_subordinate_html = subordinate__gen(json_article_filepath, 
        key='intro', 
        attribute='introduction', entity=f'phytochemicals {phytochemical}', context='herbal medicine', 
        regen=False, dispel=False
    )
    definition_subordinate_html = subordinate__gen(json_article_filepath, 
        key='definition', 
        attribute='definition', entity=f'phytochemicals {phytochemical}', context='herbal medicine', 
        regen=False, dispel=False
    )
    chemical_structure_subordinate_html = subordinate__gen(json_article_filepath, 
        key='chemical_structure', 
        attribute='chemical structure', entity=f'phytochemicals {phytochemical}', context='herbal medicine', 
        regen=False, dispel=False
    )
    biosynthesis_subordinate_html = subordinate__gen(json_article_filepath, 
        key='biosynthesis', 
        attribute='biosynthesis', entity=f'phytochemicals {phytochemical}', context='herbal medicine', 
        regen=False, dispel=False
    )
    subclasses_subordinate_html = subordinate__gen(json_article_filepath, 
        key='subclasses', 
        attribute=f'subclasses of {phytochemical}', entity=f'phytochemicals {phytochemical}', context='herbal medicine', 
        regen=False, dispel=False
    )
    plant_sources_subordinate_html = subordinate__gen(json_article_filepath, 
        key='plant_sources', 
        attribute='plant sources', entity=f'phytochemicals {phytochemical}', context='herbal medicine', 
        regen=False, dispel=False
    )
    plant_part_distribution_subordinate_html = subordinate__gen(json_article_filepath, 
        key='plant_part_distribution', 
        attribute='plant part distribution', entity=f'phytochemicals {phytochemical}', context='herbal medicine', 
        regen=False, dispel=False
    )
    biological_role_in_plants_subordinate_html = subordinate__gen(json_article_filepath, 
        key='biological_role_in_plants', 
        attribute='biological role in plants', entity=f'phytochemicals {phytochemical}', context='herbal medicine', 
        regen=False, dispel=False
    )
    pharmacological_effects_subordinate_html = subordinate__gen(json_article_filepath, 
        key='pharmacological_effects', 
        attribute='pharmacological effects', entity=f'phytochemicals {phytochemical}', context='herbal medicine', 
        regen=False, dispel=False
    )
    mechanisms_of_action_subordinate_html = subordinate__gen(json_article_filepath, 
        key='mechanisms_of_action', 
        attribute='mechanisms of action', entity=f'phytochemicals {phytochemical}', context='herbal medicine', 
        regen=False, dispel=False
    )
    therapeutic_applications_subordinate_html = subordinate__gen(json_article_filepath, 
        key='therapeutic_applications', 
        attribute='therapeutic applications', entity=f'phytochemicals {phytochemical}', context='herbal medicine', 
        regen=False, dispel=False
    )
    extraction_methods_subordinate_html = subordinate__gen(json_article_filepath, 
        key='extraction_methods', 
        attribute='extraction methods', entity=f'phytochemicals {phytochemical}', context='herbal medicine', 
        regen=False, dispel=False
    )
    stability_factors_subordinate_html = subordinate__gen(json_article_filepath, 
        key='stability_factors', 
        attribute='stability factors', entity=f'phytochemicals {phytochemical}', context='herbal medicine', 
        regen=False, dispel=False
    )
    bioavailability_subordinate_html = subordinate__gen(json_article_filepath, 
        key='bioavailability', 
        attribute='bioavailability', entity=f'phytochemicals {phytochemical}', context='herbal medicine', 
        regen=False, dispel=False
    )
    safety_and_toxicity_subordinate_html = subordinate__gen(json_article_filepath, 
        key='safety_and_toxicity', 
        attribute='safety and toxicity', entity=f'phytochemicals {phytochemical}', context='herbal medicine', 
        regen=False, dispel=False
    )
    drug_interactions_subordinate_html = subordinate__gen(json_article_filepath, 
        key='drug_interactions', 
        attribute='drug interactions', entity=f'phytochemicals {phytochemical}', context='herbal medicine', 
        regen=False, dispel=False
    )
    scientific_research_subordinate_html = subordinate__gen(json_article_filepath, 
        key='scientific_research', 
        attribute='scientific_research', entity=f'phytochemicals {phytochemical}', context='herbal medicine', 
        regen=False, dispel=False
    )
    industrial_applications_subordinate_html = subordinate__gen(json_article_filepath, 
        key='industrial_applications', 
        attribute='industrial applications', entity=f'phytochemicals {phytochemical}', context='herbal medicine', 
        regen=False, dispel=False
    )

    ########################################
    # html
    ########################################
    ###
    intro_html = f'''
        <h1>
            {phytochemical.title()} in Herbal Medicine
        </h1>
        <p>
            {intro_subordinate_html}
        </p>
        <p>
            Here you can find a complete <a href="/phytochemicals/classification.html">classification of phytochemicals.</a>
        </p>
    '''
    definition_html = f'''
        <section class="article-section">
            <h2>Definition</h2>
            <p>{definition_subordinate_html}</p>
        </section>
    '''
    chemical_structure_html = f'''
        <section class="article-section">
            <h2>Chemical Structure</h2>
            <p>{chemical_structure_subordinate_html}</p>
        </section>
    '''
    biosynthesis_html = f'''
        <section class="article-section">
            <h2>Biosynthesis</h2>
            <p>{biosynthesis_subordinate_html}</p>
        </section>
    '''
    subclasses_html = f'''
        <section class="article-section">
            <h2>Subclasses</h2>
            <p>{subclasses_subordinate_html}</p>
        </section>
    '''
    plant_sources_html = f'''
        <section class="article-section">
            <h2>Plant Sources</h2>
            <p>{plant_sources_subordinate_html}</p>
        </section>
    '''
    plant_part_distribution_html = f'''
        <section class="article-section">
            <h2>Plant Part Distribution</h2>
            <p>{plant_part_distribution_subordinate_html}</p>
        </section>
    '''
    biological_role_in_plants_html = f'''
        <section class="article-section">
            <h2>Biological Role in Plants</h2>
            <p>{biological_role_in_plants_subordinate_html}</p>
        </section>
    '''
    pharmacological_effects_html = f'''
        <section class="article-section">
            <h2>Pharmacological Effects</h2>
            <p>{pharmacological_effects_subordinate_html}</p>
        </section>
    '''
    mechanisms_of_action_html = f'''
        <section class="article-section">
            <h2>Mechanisms of Action</h2>
            <p>{mechanisms_of_action_subordinate_html}</p>
        </section>
    '''
    therapeutic_applications_html = f'''
        <section class="article-section">
            <h2>Therapeutic Applications</h2>
            <p>{therapeutic_applications_subordinate_html}</p>
        </section>
    '''
    extraction_methods_html = f'''
        <section class="article-section">
            <h2>Extraction Methods</h2>
            <p>{extraction_methods_subordinate_html}</p>
        </section>
    '''
    stability_factors_html = f'''
        <section class="article-section">
            <h2>Stability Factors</h2>
            <p>{stability_factors_subordinate_html}</p>
        </section>
    '''
    bioavailability_html = f'''
        <section class="article-section">
            <h2>Bioavailability</h2>
            <p>{bioavailability_subordinate_html}</p>
        </section>
    '''
    safety_and_toxicity_html = f'''
        <section class="article-section">
            <h2>Safety and Toxicity</h2>
            <p>{safety_and_toxicity_subordinate_html}</p>
        </section>
    '''
    drug_interactions_html = f'''
        <section class="article-section">
            <h2>Drug Interactions</h2>
            <p>{drug_interactions_subordinate_html}</p>
        </section>
    '''
    scientific_research_html = f'''
        <section class="article-section">
            <h2>Scientific Research</h2>
            <p>{scientific_research_subordinate_html}</p>
        </section>
    '''
    industrial_applications_html = f'''
        <section class="article-section">
            <h2>Industrial Applications</h2>
            <p>{industrial_applications_subordinate_html}</p>
        </section>
    '''

    article_html = f'''
        {intro_html}
        {definition_html}
        {chemical_structure_html}
        {biosynthesis_html}
        {subclasses_html}
        {plant_sources_html}
        {plant_part_distribution_html}
        {biological_role_in_plants_html}
        {pharmacological_effects_html}
        {mechanisms_of_action_html}
        {therapeutic_applications_html}
        {extraction_methods_html}
        {stability_factors_html}
        {bioavailability_html}
        {safety_and_toxicity_html}
        {drug_interactions_html}
        {scientific_research_html}
        {industrial_applications_html}
    '''
    '''
    '''

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
                    {article_html}
                </article>
            </main>
            {sections.footer()}
        </body>
        </html>
    ''').strip()
    html_filepath = f'''{g.website_folderpath}/{url_slug}.html'''
    io.folder_create_from_filepath(html_filepath)
    with open(html_filepath, 'w') as f: f.write(html)

def main():
    herbal_medicine__gen()
    phytochemicals__gen()
    phytochemicals__classification__gen()
    ###
    phytochemicals = [
        'alkaloids', 
        'flavonoids', 
        'terpenoids',
        'phenolic compounds',
        'glycosides',
        'tannins',
        'saponins',
        'essential oils',
    ]
    for phytochemical in phytochemicals:
        phytochemicals__phytochemical__gen(phytochemical)
    ###
    herbs__gen()

