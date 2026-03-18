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
    pharmacological_effects_subordinate_html = subordinate__gen(json_article_filepath, 
        key='pharmacological_effects', 
        attribute='pharmacological effects', entity='herbal medicine', context='herbal medicine', 
        regen=False, dispel=False
    )
    uses_subordinate_html = subordinate__gen(json_article_filepath, 
        key='uses', 
        entity='herbal medicine', attribute='uses', context='herbal medicine', 
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
    pharmacological_effects_html = f'''
        <section class="article-section">
            <h2>Pharmacological Effects</h2>
            <p>{pharmacological_effects_subordinate_html}</p>
            <p><a href="/actions.html">Pharmacological Actions</a></p>
        </section>
    '''
    uses_html = f'''
        <section class="article-section">
            <h2>Uses</h2>
            <p>{uses_subordinate_html}</p>
            <p><a href="/uses.html">Uses</a></p>
        </section>
    '''
    preparations_html = f'''
        <section class="article-section">
            <h2>Preparations</h2>
            <p>{preparations_subordinate_html}</p>
            <p><a href="/preparations.html">Preparations</a></p>
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
        {pharmacological_effects_html}
        {uses_html}
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
    meta_title = f'Herbal Medicine Phytochemicals'
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
            Classification of Phytochemicals in Herbal Medicine
        </h1>
        <p>
            Phytochemical classification is the systematic grouping of plant-derived chemical compounds based on their molecular structure, biosynthetic origin, and biological activity. In herbal medicine, <a href="/phytochemicals.html">phytochemicals</a> are commonly classified into major groups such as alkaloids, flavonoids, terpenoids, phenolic compounds, glycosides, tannins, and saponins, each of which contributes distinct pharmacological properties to medicinal plants.
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

    herbs_names_filtered = []
    herbs = io.json_read(f'''{g.SSOT_FOLDERPATH}/herbs/herbs-medicinal-validated.json''')
    for herb in herbs:
        herb_name_scientific = herb['taxon_name']
        herb_slug = polish.sluggify(herb_name_scientific)
        herb_data = io.json_read(f'''{g.SSOT_FOLDERPATH}/herbs/herbs-primary/{herb_slug}.json''')
        herb_name_common = herb_data['herb_names_common'][0]['answer']
        for compound in herb_data['herb_active_compounds']:
            name = compound['answer']
            total_score = compound['total_score']
            if name.lower().strip() == phytochemical.lower().strip():
                if total_score >= 600:
                    found = False
                    for herb_name_filtered in herbs_names_filtered:
                        if herb_name_filtered['herb_name_common'].lower().strip() == herb_name_common.lower().strip():
                            found = True
                            break
                    if not found:
                        herbs_names_filtered.append(
                            {
                                'herb_name_common': herb_name_common,
                                'herb_name_scientific': herb_name_scientific,
                                'herb_slug': herb_slug,
                            }
                        )
    random.shuffle(herbs_names_filtered)
    # iprint(herbds_names_filtered)
    
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
    ###
    plant_sources_list_html = ''.join([
        f'''<li><a href="/herbs/{item['herb_slug']}.html">{item['herb_name_common']} ({item['herb_name_scientific']})</a></li>''' 
        for item in herbs_names_filtered[:15]
    ])
    plant_sources_html = f'''
        <section class="article-section">
            <h2>Plant Sources</h2>
            <p>{plant_sources_subordinate_html}</p>
            <p>The following list shows a sample of medicinal plants that are rich in {phytochemical.lower()}.</p>
            <ul>{plant_sources_list_html}</ul>
        </section>
    '''
    ###
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

def actions__gen():
    url_slug = f'actions'
    meta_title = f'Herbal Medicine Pharmacological Actions'
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
        attribute='definition', entity='pharmacological actions', context='herbal medicine', 
        regen=False, dispel=False
    )
    classification_of_actions_subordinate_html = subordinate__gen(json_article_filepath, 
        key='classification_of_actions', 
        attribute='classification of actions', entity='pharmacological actions', context='herbal medicine', 
        regen=False, dispel=False
    )
    mechanisms_of_action_subordinate_html = subordinate__gen(json_article_filepath, 
        key='mechanisms_of_action', 
        attribute='mechanisms of action', entity='pharmacological actions', context='herbal medicine', 
        regen=False, dispel=False
    )
    phytochemical_basis_subordinate_html = subordinate__gen(json_article_filepath, 
        key='phytochemical_basis', 
        attribute='phytochemical basis', entity='pharmacological actions', context='herbal medicine', 
        regen=False, dispel=False
    )
    physiological_targets_subordinate_html = subordinate__gen(json_article_filepath, 
        key='physiological_targets', 
        attribute='physiological targets', entity='pharmacological actions', context='herbal medicine', 
        regen=False, dispel=False
    )
    pharmacological_effects_subordinate_html = subordinate__gen(json_article_filepath, 
        key='pharmacological_effects', 
        attribute='pharmacological effects', entity='pharmacological actions', context='herbal medicine', 
        regen=False, dispel=False
    )
    therapeutic_outcomes_subordinate_html = subordinate__gen(json_article_filepath, 
        key='therapeutic_outcomes', 
        attribute='pharmacological effects', entity='pharmacological actions', context='herbal medicine', 
        regen=False, dispel=False
    )
    synergistic_interactions_subordinate_html = subordinate__gen(json_article_filepath, 
        key='synergistic_interactions', 
        attribute='synergistic interactions', entity='pharmacological actions', context='herbal medicine', 
        regen=False, dispel=False
    )
    dose_response_relationships_subordinate_html = subordinate__gen(json_article_filepath, 
        key='dose_response_relationships', 
        attribute='dose-response relationships', entity='pharmacological actions', context='herbal medicine', 
        regen=False, dispel=False
    )
    variability_factors_subordinate_html = subordinate__gen(json_article_filepath, 
        key='variability_factors', 
        attribute='variability factors', entity='pharmacological actions', context='herbal medicine', 
        regen=False, dispel=False
    )
    safety_and_adverse_effects_subordinate_html = subordinate__gen(json_article_filepath, 
        key='safety_and_adverse_effects', 
        attribute='safety and adverse effects', entity='pharmacological actions', context='herbal medicine', 
        regen=False, dispel=False
    )
    scientific_evidence_subordinate_html = subordinate__gen(json_article_filepath, 
        key='scientific_evidence', 
        attribute='scientific evidence', entity='pharmacological actions', context='herbal medicine', 
        regen=False, dispel=False
    )
    clinical_applications_subordinate_html = subordinate__gen(json_article_filepath, 
        key='clinical_applications', 
        attribute='clinical applications', entity='pharmacological actions', context='herbal medicine', 
        regen=False, dispel=False
    )

    ########################################
    # html
    ########################################
    intro_html = f'''
        <h1>
            Pharmacological Actions of Herbal Medicine
        </h1>
        <p>
            In <a href="/herbal-medicine.html">herbal medicine</a>, pharmacological actions refer to the physiological effects that medicinal plants produce in the body through bioactive compounds such as alkaloids, flavonoids, and terpenes. These actions influence biological systems including the immune, nervous, digestive, and cardiovascular systems, producing effects such as anti-inflammatory, antimicrobial, antioxidant, and sedative activity that contribute to the therapeutic benefits of herbal treatments.
        </p>
    '''
    definition_html = f'''
        <section class="article-section">
            <h2>Definition</h2>
            <p>{definition_subordinate_html}</p>
        </section>
    '''
    classification_of_actions_html = f'''
        <section class="article-section">
            <h2>Classification of Actions</h2>
            <p>{classification_of_actions_subordinate_html}</p>
            <p><a href="/actions/classification.html">Classification</a></p>
        </section>
    '''
    mechanisms_of_action_html = f'''
        <section class="article-section">
            <h2>Mechanisms of Action</h2>
            <p>{mechanisms_of_action_subordinate_html}</p>
        </section>
    '''
    phytochemical_basis_html = f'''
        <section class="article-section">
            <h2>Phytochemical Basis</h2>
            <p>{phytochemical_basis_subordinate_html}</p>
        </section>
    '''
    physiological_targets_html = f'''
        <section class="article-section">
            <h2>Physiological Targets</h2>
            <p>{physiological_targets_subordinate_html}</p>
        </section>
    '''
    pharmacological_effects_html = f'''
        <section class="article-section">
            <h2>Pharmacological Effects</h2>
            <p>{pharmacological_effects_subordinate_html}</p>
        </section>
    '''
    therapeutic_outcomes_html = f'''
        <section class="article-section">
            <h2>Therapeutic Outcomes</h2>
            <p>{therapeutic_outcomes_subordinate_html}</p>
        </section>
    '''
    synergistic_interactions_html = f'''
        <section class="article-section">
            <h2>Synergistic Interactions</h2>
            <p>{synergistic_interactions_subordinate_html}</p>
        </section>
    '''
    dose_response_relationships_html = f'''
        <section class="article-section">
            <h2>Dose-Response Relationships</h2>
            <p>{dose_response_relationships_subordinate_html}</p>
        </section>
    '''
    variability_factors_html = f'''
        <section class="article-section">
            <h2>Variability Factors</h2>
            <p>{variability_factors_subordinate_html}</p>
        </section>
    '''
    safety_and_adverse_effects_html = f'''
        <section class="article-section">
            <h2>Safety and Adverse Effects</h2>
            <p>{safety_and_adverse_effects_subordinate_html}</p>
        </section>
    '''
    scientific_evidence_html = f'''
        <section class="article-section">
            <h2>Scientific Evidence</h2>
            <p>{scientific_evidence_subordinate_html}</p>
        </section>
    '''
    clinical_applications_html = f'''
        <section class="article-section">
            <h2>Clinical Applications</h2>
            <p>{clinical_applications_subordinate_html}</p>
        </section>
    '''

    article_html = f'''
        {intro_html}
        {definition_html}
        {classification_of_actions_html}
        {mechanisms_of_action_html}
        {phytochemical_basis_html}
        {physiological_targets_html}
        {pharmacological_effects_html}
        {therapeutic_outcomes_html}
        {synergistic_interactions_html}
        {dose_response_relationships_html}
        {variability_factors_html}
        {safety_and_adverse_effects_html}
        {scientific_evidence_html}
        {clinical_applications_html}
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

def actions__classification__gen():
    url_slug = f'actions/classification'
    meta_title = f'Pharmacological Actions Classification'
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
    items = data.actions_get()
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
        items_data = []
        for item in items:
            found = False
            for _item in items_data:
                if _item == item:
                    found = True
                    break
            if not found:
                _obj = {
                    'entity': item,
                    'heading': item,
                    'subordinate': '',
                    'slug': item.lower().strip().replace(' ', '-'),
                }
                items_data.append(_obj)
        json_article[key] = items_data
        io.json_write(json_article_filepath, json_article)
    ###
    for json_item in json_article[key]:
        entity = 'Pharmacological action classification'
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
    definition_subordinate_html = subordinate__gen(json_article_filepath, 
        key='definition', 
        attribute='definition', entity='classification of pharmacological actions', context='herbal medicine', 
        regen=False, dispel=False
    )
    purpose_of_classification_subordinate_html = subordinate__gen(json_article_filepath, 
        key='purpose_of_classification', 
        attribute='purpose of classification', entity='classification of pharmacological actions', context='herbal medicine', 
        regen=False, dispel=False
    )
    major_categories_subordinate_html = subordinate__gen(json_article_filepath, 
        key='major_categories', 
        attribute='major categories', entity='classification of pharmacological actions', context='herbal medicine', 
        regen=False, dispel=False
    )
    functional_classification_subordinate_html = subordinate__gen(json_article_filepath, 
        key='functional_classification', 
        attribute='Classification by Therapeutic Function', entity='classification of pharmacological actions', context='herbal medicine', 
        regen=False, dispel=False
    )
    physiological_system_classification_subordinate_html = subordinate__gen(json_article_filepath, 
        key='physiological_system_classification', 
        attribute='Classification by Physiological Target System', entity='classification of pharmacological actions', context='herbal medicine', 
        regen=False, dispel=False
    )
    mechanism_based_classification_subordinate_html = subordinate__gen(json_article_filepath, 
        key='mechanism_based_classification', 
        attribute='Classification by Mechanism of Action', entity='classification of pharmacological actions', context='herbal medicine', 
        regen=False, dispel=False
    )
    biological_activity_classification_subordinate_html = subordinate__gen(json_article_filepath, 
        key='biological_activity_classification', 
        attribute='Classification by Biological Activity', entity='classification of pharmacological actions', context='herbal medicine', 
        regen=False, dispel=False
    )
    primary_vs_secondary_actions_subordinate_html = subordinate__gen(json_article_filepath, 
        key='primary_vs_secondary_actions', 
        attribute='Primary and Secondary Herbal Actions', entity='classification of pharmacological actions', context='herbal medicine', 
        regen=False, dispel=False
    )
    local_vs_systemic_actions_subordinate_html = subordinate__gen(json_article_filepath, 
        key='local_vs_systemic_actions', 
        attribute='Local vs Systemic Herbal Actions', entity='classification of pharmacological actions', context='herbal medicine', 
        regen=False, dispel=False
    )
    direct_vs_indirect_actions_subordinate_html = subordinate__gen(json_article_filepath, 
        key='direct_vs_indirect_actions', 
        attribute='Direct vs Indirect Herbal Actions', entity='classification of pharmacological actions', context='herbal medicine', 
        regen=False, dispel=False
    )
    temporal_classification_subordinate_html = subordinate__gen(json_article_filepath, 
        key='temporal_classification', 
        attribute='Acute vs Long-Term Herbal Actions', entity='classification of pharmacological actions', context='herbal medicine', 
        regen=False, dispel=False
    )
    multi_target_action_classification_subordinate_html = subordinate__gen(json_article_filepath, 
        key='multi_target_action_classification', 
        attribute='Single vs Multi-Target Herbal Actions', entity='classification of pharmacological actions', context='herbal medicine', 
        regen=False, dispel=False
    )
    synergistic_action_classification_subordinate_html = subordinate__gen(json_article_filepath, 
        key='synergistic_action_classification', 
        attribute='Synergistic and Polyherbal Action Categories', entity='classification of pharmacological actions', context='herbal medicine', 
        regen=False, dispel=False
    )
    clinical_application_classification_subordinate_html = subordinate__gen(json_article_filepath, 
        key='clinical_application_classification', 
        attribute='Comparison with Pharmaceutical Action Classification', entity='classification of pharmacological actions', context='herbal medicine', 
        regen=False, dispel=False
    )
    scientific_research_classification_subordinate_html = subordinate__gen(json_article_filepath, 
        key='scientific_research_classification', 
        attribute='Scientific and Pharmacological Research Approaches', entity='classification of pharmacological actions', context='herbal medicine', 
        regen=False, dispel=False
    )

    ########################################
    # html
    ########################################
    intro_html = f'''
        <h1>
            Classification of Pharmacological Actions in Herbal Medicine
        </h1>
        <p>
            In herbal medicine, classification of <a href="/actions.html">pharmacological actions</a> refers to the systematic organization of the physiological effects produced by medicinal plants. Herbal actions are categorized based on therapeutic function, biological mechanisms, target body systems, and clinical outcomes, allowing practitioners and researchers to understand how herbal compounds influence human physiology.
        </p>
    '''
    definition_html = f'''
        <section class="article-section">
            <h2>Definition of Herbal Action Classification</h2>
            <p>{definition_subordinate_html}</p>
        </section>
    '''
    purpose_of_classification_html = f'''
        <section class="article-section">
            <h2>Purpose of Classifying Herbal Actions</h2>
            <p>{purpose_of_classification_subordinate_html}</p>
        </section>
    '''
    ###
    list_html = ''
    for item in json_article['list'][:10]:
        list_html += f'''
            <li>{item['heading']}</li>
        '''
    subsections_html = ''
    for item in json_article['list'][:10]:
        subsections_html += f'''
            <h3>{item['heading']}</h3>
            <p>{item['subordinate']}</p>
            <p><a href="/actions/{item['slug']}.html">{item['heading']}</a></p>
        '''
    major_categories_html = f'''
        <section class="article-section">
            <h2>Major Categories of Herbal Pharmacological Actions</h2>
            <p>{major_categories_subordinate_html}</p>
            <p>The list below shows a sample of the major categories of herbal pharmacological actions.</p>
            <ul>
                {list_html}
            </ul>
            {subsections_html}
        </section>
    '''
    functional_classification_html = f'''
        <section class="article-section">
            <h2>Classification by Therapeutic Function</h2>
            <p>{functional_classification_subordinate_html}</p>
        </section>
    '''
    physiological_system_classification_html = f'''
        <section class="article-section">
            <h2>Classification by Physiological Target System</h2>
            <p>{physiological_system_classification_subordinate_html}</p>
        </section>
    '''
    mechanism_based_classification_html = f'''
        <section class="article-section">
            <h2>Classification by Mechanism of Action</h2>
            <p>{mechanism_based_classification_subordinate_html}</p>
        </section>
    '''
    biological_activity_classification_html = f'''
        <section class="article-section">
            <h2>Classification by Biological Activity</h2>
            <p>{biological_activity_classification_subordinate_html}</p>
        </section>
    '''
    primary_vs_secondary_actions_html = f'''
        <section class="article-section">
            <h2>Primary and Secondary Herbal Actions</h2>
            <p>{primary_vs_secondary_actions_subordinate_html}</p>
        </section>
    '''
    local_vs_systemic_actions_html = f'''
        <section class="article-section">
            <h2>Local vs Systemic Herbal Actions</h2>
            <p>{local_vs_systemic_actions_subordinate_html}</p>
        </section>
    '''
    direct_vs_indirect_actions_html = f'''
        <section class="article-section">
            <h2>Direct vs Indirect Herbal Actions</h2>
            <p>{direct_vs_indirect_actions_subordinate_html}</p>
        </section>
    '''
    temporal_classification_html = f'''
        <section class="article-section">
            <h2>Acute vs Long-Term Herbal Actions</h2>
            <p>{temporal_classification_subordinate_html}</p>
        </section>
    '''
    multi_target_action_classification_html = f'''
        <section class="article-section">
            <h2>Single vs Multi-Target Herbal Actions</h2>
            <p>{multi_target_action_classification_subordinate_html}</p>
        </section>
    '''
    synergistic_action_classification_html = f'''
        <section class="article-section">
            <h2>Synergistic and Polyherbal Action Categories</h2>
            <p>{synergistic_action_classification_subordinate_html}</p>
        </section>
    '''
    clinical_application_classification_html = f'''
        <section class="article-section">
            <h2>Comparison with Pharmaceutical Action Classification</h2>
            <p>{clinical_application_classification_subordinate_html}</p>
        </section>
    '''
    scientific_research_classification_html = f'''
        <section class="article-section">
            <h2>Scientific and Pharmacological Research Approaches</h2>
            <p>{scientific_research_classification_subordinate_html}</p>
        </section>
    '''

    article_html = f'''
        {intro_html}
        {definition_html}
        {purpose_of_classification_html}
        {major_categories_html}
        {functional_classification_html}
        {physiological_system_classification_html}
        {mechanism_based_classification_html}
        {biological_activity_classification_html}
        {primary_vs_secondary_actions_html}
        {local_vs_systemic_actions_html}
        {direct_vs_indirect_actions_html}
        {temporal_classification_html}
        {multi_target_action_classification_html}
        {synergistic_action_classification_html}
        {clinical_application_classification_html}
        {scientific_research_classification_html}
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

def actions_action__gen(action):
    action = action.lower().strip()
    action_slug = action.replace(' ', '-')
    url_slug = f'actions/{action_slug}'
    meta_title = f'Pharmacological Actions {action.title()}'
    meta_description = ''
    canonical_html = f'''<link rel="canonical" href="https://terrawhisper.com/{url_slug}.html">'''

    herbs_names_filtered = []
    herbs = io.json_read(f'''{g.SSOT_FOLDERPATH}/herbs/herbs-medicinal-validated.json''')
    for herb in herbs:
        herb_name_scientific = herb['taxon_name']
        herb_slug = polish.sluggify(herb_name_scientific)
        herb_data = io.json_read(f'''{g.SSOT_FOLDERPATH}/herbs/herbs-primary/{herb_slug}.json''')
        herb_name_common = herb_data['herb_names_common'][0]['answer']
        ###
        for item in herb_data['herb_actions']:
            name = item['answer']
            total_score = item['total_score']
            if name.lower().strip() == action.lower().strip():
                if total_score >= 600:
                    found = False
                    for herb_name_filtered in herbs_names_filtered:
                        if herb_name_filtered['herb_name_common'].lower().strip() == herb_name_common.lower().strip():
                            found = True
                            break
                    if not found:
                        herbs_names_filtered.append(
                            {
                                'herb_name_common': herb_name_common,
                                'herb_name_scientific': herb_name_scientific,
                                'herb_slug': herb_slug,
                            }
                        )
    random.shuffle(herbs_names_filtered)

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
        attribute='introduction', entity=f'{action} action', context='herbal medicine', 
        regen=False, dispel=False
    )
    definition_subordinate_html = subordinate__gen(json_article_filepath, 
        key='definition', 
        attribute='definition', entity=f'{action} action', context='herbal medicine', 
        regen=False, dispel=False
    )
    biological_mechanisms_subordinate_html = subordinate__gen(json_article_filepath, 
        key='biological_mechanisms', 
        attribute='Biological Mechanisms of the Action', entity=f'{action} action', context='herbal medicine', 
        regen=False, dispel=False
    )
    phytochemical_basis_subordinate_html = subordinate__gen(json_article_filepath, 
        key='phytochemical_basis', 
        attribute='Phytochemical Compounds Responsible', entity=f'{action} action', context='herbal medicine', 
        regen=False, dispel=False
    )
    physiological_targets_subordinate_html = subordinate__gen(json_article_filepath, 
        key='physiological_targets', 
        attribute='Physiological Systems Affected', entity=f'{action} action', context='herbal medicine', 
        regen=False, dispel=False
    )
    therapeutic_effects_subordinate_html = subordinate__gen(json_article_filepath, 
        key='therapeutic_effects', 
        attribute='Therapeutic Effects and Health Benefits', entity=f'{action} action', context='herbal medicine', 
        regen=False, dispel=False
    )
    diseases_and_conditions_subordinate_html = subordinate__gen(json_article_filepath, 
        key='diseases_and_conditions', 
        attribute='Conditions Treated by the Action', entity=f'{action} action', context='herbal medicine', 
        regen=False, dispel=False
    )
    herbal_sources_subordinate_html = subordinate__gen(json_article_filepath, 
        key='herbal_sources', 
        attribute='Medicinal Herbs With This Action', entity=f'{action} action', context='herbal medicine', 
        regen=False, dispel=False
    )
    preparation_methods_subordinate_html = subordinate__gen(json_article_filepath, 
        key='preparation_methods', 
        attribute='Preparation Methods for Herbs With This Action', entity=f'{action} action', context='herbal medicine', 
        regen=False, dispel=False
    )
    dosage_subordinate_html = subordinate__gen(json_article_filepath, 
        key='dosage', 
        attribute='Dosage and Administration Considerations', entity=f'{action} action', context='herbal medicine', 
        regen=False, dispel=False
    )
    synergistic_actions_subordinate_html = subordinate__gen(json_article_filepath, 
        key='synergistic_actions', 
        attribute='Synergistic Herbal Combinations', entity=f'{action} action', context='herbal medicine', 
        regen=False, dispel=False
    )
    safety_and_side_effects_subordinate_html = subordinate__gen(json_article_filepath, 
        key='safety_and_side_effects', 
        attribute='Safety and Possible Side Effects', entity=f'{action} action', context='herbal medicine', 
        regen=False, dispel=False
    )
    contraindications_subordinate_html = subordinate__gen(json_article_filepath, 
        key='contraindications', 
        attribute='Contraindications and Drug Interactions', entity=f'{action} action', context='herbal medicine', 
        regen=False, dispel=False
    )
    scientific_evidence_subordinate_html = subordinate__gen(json_article_filepath, 
        key='scientific_evidence', 
        attribute='Scientific Research and Evidence', entity=f'{action} action', context='herbal medicine', 
        regen=False, dispel=False
    )
    clinical_applications_subordinate_html = subordinate__gen(json_article_filepath, 
        key='clinical_applications', 
        attribute='Clinical Applications in Herbal Medicine', entity=f'{action} action', context='herbal medicine', 
        regen=False, dispel=False
    )
    related_herbal_actions_subordinate_html = subordinate__gen(json_article_filepath, 
        key='related_herbal_actions', 
        attribute='Related Herbal Actions', entity=f'{action} action', context='herbal medicine', 
        regen=False, dispel=False
    )

    ########################################
    # html
    ########################################
    ###
    intro_html = f'''
        <h1>
            {action.title()} Action in Herbal Medicine
        </h1>
        <p>
            {intro_subordinate_html}
        </p>
        <p>
            Here you can find a complete <a href="/actions/classification.html">classification of pharmacological actions.</a>
        </p>
    '''
    definition_html = f'''
        <section class="article-section">
            <h2>Definition of the Action</h2>
            <p>{definition_subordinate_html}</p>
        </section>
    '''
    biological_mechanisms_html = f'''
        <section class="article-section">
            <h2>Biological Mechanisms of the Action</h2>
            <p>{biological_mechanisms_subordinate_html}</p>
        </section>
    '''
    phytochemical_basis_html = f'''
        <section class="article-section">
            <h2>Phytochemical Compounds Responsible</h2>
            <p>{phytochemical_basis_subordinate_html}</p>
        </section>
    '''
    physiological_targets_html = f'''
        <section class="article-section">
            <h2>Physiological Systems Affected</h2>
            <p>{physiological_targets_subordinate_html}</p>
        </section>
    '''
    therapeutic_effects_html = f'''
        <section class="article-section">
            <h2>Therapeutic Effects and Health Benefits</h2>
            <p>{therapeutic_effects_subordinate_html}</p>
        </section>
    '''
    diseases_and_conditions_html = f'''
        <section class="article-section">
            <h2>Conditions Treated by the Action</h2>
            <p>{diseases_and_conditions_subordinate_html}</p>
        </section>
    '''
    ###
    list_html = ''.join([
        f'''<li>
            <a href="/herbs/{item['herb_slug']}.html">{item['herb_name_common']} ({item['herb_name_scientific']})</a>
            </li>''' 
        for item in herbs_names_filtered[:15]
    ])
    herbal_sources_html = f'''
        <section class="article-section">
            <h2>Medicinal Herbs With This Action</h2>
            <p>{herbal_sources_subordinate_html}</p>
            <p>The following list shows a sample of medicinal plants that have {action.lower()} action.</p>
            <ul>{list_html}</ul>
        </section>
    '''
    ###
    preparation_methods_html = f'''
        <section class="article-section">
            <h2>Preparation Methods for Herbs With This Action</h2>
            <p>{preparation_methods_subordinate_html}</p>
        </section>
    '''
    dosage_html = f'''
        <section class="article-section">
            <h2>Dosage and Administration Considerations</h2>
            <p>{dosage_subordinate_html}</p>
        </section>
    '''
    synergistic_actions_html = f'''
        <section class="article-section">
            <h2>Synergistic Herbal Combinations</h2>
            <p>{synergistic_actions_subordinate_html}</p>
        </section>
    '''
    safety_and_side_effects_html = f'''
        <section class="article-section">
            <h2>Safety and Possible Side Effects</h2>
            <p>{safety_and_side_effects_subordinate_html}</p>
        </section>
    '''
    contraindications_html = f'''
        <section class="article-section">
            <h2>Contraindications and Drug Interactions</h2>
            <p>{contraindications_subordinate_html}</p>
        </section>
    '''
    scientific_evidence_html = f'''
        <section class="article-section">
            <h2>Scientific Research and Evidence</h2>
            <p>{scientific_evidence_subordinate_html}</p>
        </section>
    '''
    clinical_applications_html = f'''
        <section class="article-section">
            <h2>Clinical Applications in Herbal Medicine</h2>
            <p>{clinical_applications_subordinate_html}</p>
        </section>
    '''
    related_herbal_actions_html = f'''
        <section class="article-section">
            <h2>Related Herbal Actions</h2>
            <p>{related_herbal_actions_subordinate_html}</p>
        </section>
    '''

    article_html = f'''
        {intro_html}
        {definition_html}
        {biological_mechanisms_html}
        {phytochemical_basis_html}
        {physiological_targets_html}
        {therapeutic_effects_html}
        {diseases_and_conditions_html}
        {herbal_sources_html}
        {preparation_methods_html}
        {dosage_html}
        {synergistic_actions_html}
        {safety_and_side_effects_html}
        {contraindications_html}
        {scientific_evidence_html}
        {clinical_applications_html}
        {related_herbal_actions_html}
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

def preparations__gen():
    url_slug = f'preparations'
    meta_title = f'Herbal Medicine Preparations'
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
        attribute='definition', entity='preparation methods', context='herbal medicine', 
        regen=False, dispel=False
    )
    purpose_subordinate_html = subordinate__gen(json_article_filepath, 
        key='purpose', 
        attribute='purpose of herbal preparations in herbal medicine', entity='preparation methods', context='herbal medicine', 
        regen=False, dispel=False
    )
    principles_subordinate_html = subordinate__gen(json_article_filepath, 
        key='principles', 
        attribute='principles of herbal preparation', entity='preparation methods', context='herbal medicine', 
        regen=False, dispel=False
    )
    types_subordinate_html = subordinate__gen(json_article_filepath, 
        key='types', 
        attribute='types of herbal preparations', entity='preparation methods', context='herbal medicine', 
        regen=False, dispel=False
    )
    preparation_methods_subordinate_html = subordinate__gen(json_article_filepath, 
        key='preparation_methods', 
        attribute='preparation methods', entity='preparation methods', context='herbal medicine', 
        regen=False, dispel=False
    )
    plant_materials_subordinate_html = subordinate__gen(json_article_filepath, 
        key='plant_materials', 
        attribute='Plant Materials Used in Preparations', entity='preparation methods', context='herbal medicine', 
        regen=False, dispel=False
    )
    solvents_and_extraction_media_subordinate_html = subordinate__gen(json_article_filepath, 
        key='solvents_and_extraction_media', 
        attribute='Solvents and Extraction Media', entity='preparation methods', context='herbal medicine', 
        regen=False, dispel=False
    )
    chemical_extraction_and_phytochemistry_subordinate_html = subordinate__gen(json_article_filepath, 
        key='chemical_extraction_and_phytochemistry', 
        attribute='Chemical Extraction and Phytochemistry', entity='preparation methods', context='herbal medicine', 
        regen=False, dispel=False
    )
    dosage_forms_and_administration_subordinate_html = subordinate__gen(json_article_filepath, 
        key='dosage_forms_and_administration', 
        attribute='Dosage Forms and Administration', entity='preparation methods', context='herbal medicine', 
        regen=False, dispel=False
    )
    potency_and_concentration_subordinate_html = subordinate__gen(json_article_filepath, 
        key='potency_and_concentration', 
        attribute='Potency and Concentration', entity='preparation methods', context='herbal medicine', 
        regen=False, dispel=False
    )
    quality_and_standardization_subordinate_html = subordinate__gen(json_article_filepath, 
        key='quality_and_standardization', 
        attribute='Quality and Standardization', entity='preparation methods', context='herbal medicine', 
        regen=False, dispel=False
    )
    safety_and_stability_subordinate_html = subordinate__gen(json_article_filepath, 
        key='safety_and_stability', 
        attribute='Safety and Stability', entity='preparation methods', context='herbal medicine', 
        regen=False, dispel=False
    )
    storage_and_shelf_life_subordinate_html = subordinate__gen(json_article_filepath, 
        key='storage_and_shelf_life', 
        attribute='Storage and Shelf Life', entity='preparation methods', context='herbal medicine', 
        regen=False, dispel=False
    )
    manufacturing_and_production_subordinate_html = subordinate__gen(json_article_filepath, 
        key='manufacturing_and_production', 
        attribute='Manufacturing and Production', entity='preparation methods', context='herbal medicine', 
        regen=False, dispel=False
    )
    traditional_preparation_systems_subordinate_html = subordinate__gen(json_article_filepath, 
        key='traditional_preparation_systems', 
        attribute='Traditional Preparation Systems', entity='preparation methods', context='herbal medicine', 
        regen=False, dispel=False
    )
    modern_herbal_extraction_techniques_subordinate_html = subordinate__gen(json_article_filepath, 
        key='modern_herbal_extraction_techniques', 
        attribute='Modern Herbal Extraction Techniques', entity='preparation methods', context='herbal medicine', 
        regen=False, dispel=False
    )
    scientific_research_subordinate_html = subordinate__gen(json_article_filepath, 
        key='scientific_research', 
        attribute='Scientific Research on Herbal Preparations', entity='preparation methods', context='herbal medicine', 
        regen=False, dispel=False
    )
    regulatory_and_legal_aspects_subordinate_html = subordinate__gen(json_article_filepath, 
        key='regulatory_and_legal_aspects', 
        attribute='Regulatory and Legal Aspects', entity='preparation methods', context='herbal medicine', 
        regen=False, dispel=False
    )

    ########################################
    # html
    ########################################
    intro_html = f'''
        <h1>
            Herbal Preparations: Methods, Forms, and Uses in Herbal Medicine
        </h1>
        <p>
            Herbal preparations are medicinal products made by processing plant materials such as leaves, roots, flowers, and seeds to extract their therapeutic compounds. In <a href="/herbal-medicine.html">herbal medicine</a>, preparations are created using methods like infusion, decoction, tincture extraction, and oil infusion to deliver plant-based remedies in forms such as teas, powders, capsules, and topical treatments.
        </p>
    '''
    definition_html = f'''
        <section class="article-section">
            <h2>Definition of Herbal Preparations</h2>
            <p>{definition_subordinate_html}</p>
        </section>
    '''
    purpose_html = f'''
        <section class="article-section">
            <h2>Purpose of Herbal Preparations in Herbal Medicine</h2>
            <p>{purpose_subordinate_html}</p>
        </section>
    '''
    principles_html = f'''
        <section class="article-section">
            <h2>Principles of Herbal Preparation</h2>
            <p>{principles_subordinate_html}</p>
        </section>
    '''
    types_html = f'''
        <section class="article-section">
            <h2>Types of Herbal Preparations</h2>
            <p>{types_subordinate_html}</p>
            <p><a href="/preparations/forms.html">Preparation Forms</a></p>
        </section>
    '''
    preparation_methods_html = f'''
        <section class="article-section">
            <h2>Preparation Methods</h2>
            <p>{preparation_methods_subordinate_html}</p>
        </section>
    '''
    plant_materials_html = f'''
        <section class="article-section">
            <h2>Plant Materials Used in Preparations</h2>
            <p>{plant_materials_subordinate_html}</p>
        </section>
    '''
    solvents_and_extraction_media_html = f'''
        <section class="article-section">
            <h2>Solvents and Extraction Media</h2>
            <p>{solvents_and_extraction_media_subordinate_html}</p>
        </section>
    '''
    chemical_extraction_and_phytochemistry_html = f'''
        <section class="article-section">
            <h2>Chemical Extraction and Phytochemistry</h2>
            <p>{chemical_extraction_and_phytochemistry_subordinate_html}</p>
        </section>
    '''
    dosage_forms_and_administration_html = f'''
        <section class="article-section">
            <h2>Dosage Forms and Administration</h2>
            <p>{dosage_forms_and_administration_subordinate_html}</p>
        </section>
    '''
    potency_and_concentration_html = f'''
        <section class="article-section">
            <h2>Potency and Concentration</h2>
            <p>{potency_and_concentration_subordinate_html}</p>
        </section>
    '''
    quality_and_standardization_html = f'''
        <section class="article-section">
            <h2>Quality and Standardization</h2>
            <p>{quality_and_standardization_subordinate_html}</p>
        </section>
    '''
    safety_and_stability_html = f'''
        <section class="article-section">
            <h2>Safety and Stability</h2>
            <p>{safety_and_stability_subordinate_html}</p>
        </section>
    '''
    storage_and_shelf_life_html = f'''
        <section class="article-section">
            <h2>Storage and Shelf Life</h2>
            <p>{storage_and_shelf_life_subordinate_html}</p>
        </section>
    '''
    manufacturing_and_production_html = f'''
        <section class="article-section">
            <h2>Manufacturing and Production</h2>
            <p>{manufacturing_and_production_subordinate_html}</p>
        </section>
    '''
    traditional_preparation_systems_html = f'''
        <section class="article-section">
            <h2>Traditional Preparation Systems</h2>
            <p>{traditional_preparation_systems_subordinate_html}</p>
        </section>
    '''
    modern_herbal_extraction_techniques_html = f'''
        <section class="article-section">
            <h2>Modern Herbal Extraction Techniques</h2>
            <p>{modern_herbal_extraction_techniques_subordinate_html}</p>
        </section>
    '''
    scientific_research_html = f'''
        <section class="article-section">
            <h2>Scientific Research on Herbal Preparations</h2>
            <p>{scientific_research_subordinate_html}</p>
        </section>
    '''
    regulatory_and_legal_aspects_html = f'''
        <section class="article-section">
            <h2>Regulatory and Legal Aspects</h2>
            <p>{regulatory_and_legal_aspects_subordinate_html}</p>
        </section>
    '''

    article_html = f'''
        {intro_html}
        {definition_html}
        {purpose_html}
        {principles_html}
        {types_html}
        {preparation_methods_html}
        {plant_materials_html}
        {dosage_forms_and_administration_html}
        {solvents_and_extraction_media_html}
        {chemical_extraction_and_phytochemistry_html}
        {dosage_forms_and_administration_html}
        {potency_and_concentration_html}
        {quality_and_standardization_html}
        {safety_and_stability_html}
        {manufacturing_and_production_html}
        {traditional_preparation_systems_html}
        {modern_herbal_extraction_techniques_html}
        {scientific_research_html}
        {regulatory_and_legal_aspects_html}
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

def preparations__forms__gen():
    url_slug = f'preparations/forms'
    meta_title = f'Herbal Preparation Forms: Types, Uses, and Dosage Forms in Herbal Medicine'
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
    definition_subordinate_html = subordinate__gen(json_article_filepath, 
        key='definition', 
        attribute='definition', entity='preparation forms', context='herbal medicine', 
        regen=False, dispel=False
    )
    purpose_subordinate_html = subordinate__gen(json_article_filepath, 
        key='purpose', 
        attribute='Purpose of Herbal Dosage Forms', entity='preparation forms', context='herbal medicine', 
        regen=False, dispel=False
    )
    classification_subordinate_html = subordinate__gen(json_article_filepath, 
        key='classification', 
        attribute='Classification of Herbal Preparation Forms', entity='preparation forms', context='herbal medicine', 
        regen=False, dispel=False
    )
    liquid_subordinate_html = subordinate__gen(json_article_filepath, 
        key='liquid', 
        attribute='Liquid Herbal Forms', entity='preparation forms', context='herbal medicine', 
        regen=False, dispel=False
    )
    solid_subordinate_html = subordinate__gen(json_article_filepath, 
        key='solid', 
        attribute='Solid Herbal Forms', entity='preparation forms', context='herbal medicine', 
        regen=False, dispel=False
    )
    semi_solid_subordinate_html = subordinate__gen(json_article_filepath, 
        key='semi_solid', 
        attribute='Semi-Solid Herbal Forms', entity='preparation forms', context='herbal medicine', 
        regen=False, dispel=False
    )
    oil_based_subordinate_html = subordinate__gen(json_article_filepath, 
        key='oil_based', 
        attribute='Oil-Based Herbal Forms', entity='preparation forms', context='herbal medicine', 
        regen=False, dispel=False
    )
    topical_subordinate_html = subordinate__gen(json_article_filepath, 
        key='topical', 
        attribute='Topical Herbal Forms', entity='preparation forms', context='herbal medicine', 
        regen=False, dispel=False
    )
    inhalation_subordinate_html = subordinate__gen(json_article_filepath, 
        key='inhalation', 
        attribute='Inhalation and Aromatic Forms', entity='preparation forms', context='herbal medicine', 
        regen=False, dispel=False
    )
    internal_vs_external_subordinate_html = subordinate__gen(json_article_filepath, 
        key='internal_vs_external', 
        attribute='Internal vs External Herbal Forms', entity='preparation forms', context='herbal medicine', 
        regen=False, dispel=False
    )
    selection_subordinate_html = subordinate__gen(json_article_filepath, 
        key='selection', 
        attribute='Selection of the Appropriate Form', entity='preparation forms', context='herbal medicine', 
        regen=False, dispel=False
    )
    stability_subordinate_html = subordinate__gen(json_article_filepath, 
        key='stability', 
        attribute='Stability and Shelf Life', entity='preparation forms', context='herbal medicine', 
        regen=False, dispel=False
    )
    dosage_subordinate_html = subordinate__gen(json_article_filepath, 
        key='dosage', 
        attribute='Dosage and Administration', entity='preparation forms', context='herbal medicine', 
        regen=False, dispel=False
    )
    quality_subordinate_html = subordinate__gen(json_article_filepath, 
        key='quality', 
        attribute='Quality and Standardization', entity='preparation forms', context='herbal medicine', 
        regen=False, dispel=False
    )
    safety_subordinate_html = subordinate__gen(json_article_filepath, 
        key='safety', 
        attribute='Safety Considerations', entity='preparation forms', context='herbal medicine', 
        regen=False, dispel=False
    )
    traditional_subordinate_html = subordinate__gen(json_article_filepath, 
        key='traditional', 
        attribute='Traditional Herbal Form Systems', entity='preparation forms', context='herbal medicine', 
        regen=False, dispel=False
    )
    modern_subordinate_html = subordinate__gen(json_article_filepath, 
        key='modern', 
        attribute='Modern Pharmaceutical Herbal Forms', entity='preparation forms', context='herbal medicine', 
        regen=False, dispel=False
    )

    ########################################
    # html
    ########################################
    intro_html = f'''
        <h1>
            Herbal Preparation Forms: Types, Uses, and Dosage Forms in Herbal Medicine
        </h1>
        <p>
            Herbal preparation forms refer to the physical formats in which herbal remedies are delivered, such as teas, tinctures, capsules, powders, oils, creams, and salves. In herbal medicine, these <a href="/preparations.html">preparations</a> determine how medicinal plant compounds are administered, absorbed, and preserved, influencing dosage accuracy, stability, and therapeutic effectiveness.
        </p>
    '''
    definition_html = f'''
        <section class="article-section">
            <h2>Definition of Herbal Preparation Forms</h2>
            <p>{definition_subordinate_html}</p>
        </section>
    '''
    purpose_html = f'''
        <section class="article-section">
            <h2>Purpose of Herbal Dosage Forms</h2>
            <p>{purpose_subordinate_html}</p>
        </section>
    '''
    classification_html = f'''
        <section class="article-section">
            <h2>Classification of Herbal Preparation Forms</h2>
            <p>{classification_subordinate_html}</p>
        </section>
    '''
    liquid_html = f'''
        <section class="article-section">
            <h2>Liquid Herbal Forms</h2>
            <p>{liquid_subordinate_html}</p>
            <ul>
                <li><a href="/preparations/tinctures.html">Tinctures</a></li>
                <li><a href="/preparations/teas.html">Teas</a></li>
                <li><a href="/preparations/syrups.html">Syrups</a></li>
            </ul>
        </section>
    '''
    solid_html = f'''
        <section class="article-section">
            <h2>Solid Herbal Forms</h2>
            <p>{solid_subordinate_html}</p>
            <ul>
                <li><a href="/preparations/capsules.html">Capsules</a></li>
                <li><a href="/preparations/powders.html">Powders</a></li>
            </ul>
        </section>
    '''
    semi_solid_html = f'''
        <section class="article-section">
            <h2>Semi-Solid Herbal Forms</h2>
            <p>{semi_solid_subordinate_html}</p>
            <ul>
                <li><a href="/preparations/salves.html">Salves</a></li>
                <li><a href="/preparations/poultices.html">Poultices</a></li>
            </ul>
        </section>
    '''
    oil_based_html = f'''
        <section class="article-section">
            <h2>Oil-Based Herbal Forms</h2>
            <p>{oil_based_subordinate_html}</p>
            <ul>
                <li><a href="/preparations/oils.html">Oils</a></li>
            </ul>
        </section>
    '''
    topical_html = f'''
        <section class="article-section">
            <h2>Topical Herbal Forms</h2>
            <p>{topical_subordinate_html}</p>
        </section>
    '''
    inhalation_html = f'''
        <section class="article-section">
            <h2>Inhalation and Aromatic Forms</h2>
            <p>{inhalation_subordinate_html}</p>
        </section>
    '''
    internal_vs_external_html = f'''
        <section class="article-section">
            <h2>Internal vs External Herbal Forms</h2>
            <p>{internal_vs_external_subordinate_html}</p>
        </section>
    '''
    selection_html = f'''
        <section class="article-section">
            <h2>Selection of the Appropriate Form</h2>
            <p>{selection_subordinate_html}</p>
        </section>
    '''
    stability_html = f'''
        <section class="article-section">
            <h2>Stability and Shelf Life</h2>
            <p>{stability_subordinate_html}</p>
        </section>
    '''
    dosage_html = f'''
        <section class="article-section">
            <h2>Dosage and Administration</h2>
            <p>{dosage_subordinate_html}</p>
        </section>
    '''
    quality_html = f'''
        <section class="article-section">
            <h2>Quality and Standardization</h2>
            <p>{quality_subordinate_html}</p>
        </section>
    '''
    safety_html = f'''
        <section class="article-section">
            <h2>Safety Considerations</h2>
            <p>{safety_subordinate_html}</p>
        </section>
    '''
    traditional_html = f'''
        <section class="article-section">
            <h2>Traditional Herbal Form Systems</h2>
            <p>{traditional_subordinate_html}</p>
        </section>
    '''
    modern_html = f'''
        <section class="article-section">
            <h2>Modern Pharmaceutical Herbal Forms</h2>
            <p>{modern_subordinate_html}</p>
        </section>
    '''

    article_html = f'''
        {intro_html}
        {definition_html}
        {purpose_html}
        {classification_html}
        {liquid_html}
        {solid_html}
        {semi_solid_html}
        {oil_based_html}
        {topical_html}
        {inhalation_html}
        {internal_vs_external_html}
        {selection_html}
        {stability_html}
        {dosage_html}
        {quality_html}
        {safety_html}
        {traditional_html}
        {modern_html}
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

def preparations__methods__gen():
    url_slug = f'preparations/methods'
    meta_title = f'Herbal Preparation Methods: Techniques for Making Herbal Remedies'
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
    definition_subordinate_html = subordinate__gen(json_article_filepath, 
        key='definition', 
        attribute='definition', entity='classification of pharmacological actions', context='herbal medicine', 
        regen=False, dispel=False
    )

    ########################################
    # html
    ########################################
    intro_html = f'''
        <h1>
            Herbal Preparation Methods: Techniques for Making Herbal Remedies
        </h1>
        <p>
            Herbal preparation methods are techniques used to process medicinal plants in order to extract and preserve their therapeutic compounds. In herbal medicine, methods such as infusion, decoction, tincture extraction, oil infusion, and distillation transform raw plant materials into remedies like teas, extracts, powders, and essential oils.
        </p>
    '''
    definition_html = f'''
        <section class="article-section">
            <h2>Definition of Herbal Action Classification</h2>
            <p>{definition_subordinate_html}</p>
        </section>
    '''

    article_html = f'''
        {intro_html}
        {definition_html}
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

def preparations_preparation__gen(preparation):
    preparation = preparation.lower().strip()
    preparation_slug = preparation.replace(' ', '-')
    url_slug = f'preparations/{preparation_slug}'
    meta_title = f'{preparation.title()} in Herbal Medicine: Uses, Preparation, and Safety'
    meta_description = ''
    canonical_html = f'''<link rel="canonical" href="https://terrawhisper.com/{url_slug}.html">'''

    herbs_names_filtered = []
    herbs = io.json_read(f'''{g.SSOT_FOLDERPATH}/herbs/herbs-medicinal-validated.json''')
    for herb in herbs:
        herb_name_scientific = herb['taxon_name']
        herb_slug = polish.sluggify(herb_name_scientific)
        herb_data = io.json_read(f'''{g.SSOT_FOLDERPATH}/herbs/herbs-primary/{herb_slug}.json''')
        herb_name_common = herb_data['herb_names_common'][0]['answer']
        ###
        for item in herb_data['herb_preparations']:
            name = item['answer']
            total_score = item['total_score']
            if name.lower().strip() == preparation.lower().strip():
                if total_score >= 600:
                    found = False
                    for herb_name_filtered in herbs_names_filtered:
                        if herb_name_filtered['herb_name_common'].lower().strip() == herb_name_common.lower().strip():
                            found = True
                            break
                    if not found:
                        herbs_names_filtered.append(
                            {
                                'herb_name_common': herb_name_common,
                                'herb_name_scientific': herb_name_scientific,
                                'herb_slug': herb_slug,
                            }
                        )
    random.shuffle(herbs_names_filtered)

    regen_function = False
    dispel_function = False
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
        attribute='introduction', entity=f'{preparation}', context='herbal medicine', 
        regen=regen_function, dispel=dispel_function
    )
    definition_subordinate_html = subordinate__gen(json_article_filepath, 
        key='definition', 
        attribute='definition', entity=f'{preparation}', context='herbal medicine', 
        regen=regen_function, dispel=dispel_function
    )
    purpose_subordinate_html = subordinate__gen(json_article_filepath, 
        key='purpose', 
        attribute='Purpose and Role in Herbal Medicine', entity=f'{preparation}', context='herbal medicine', 
        regen=regen_function, dispel=dispel_function
    )
    characteristics_subordinate_html = subordinate__gen(json_article_filepath, 
        key='characteristics', 
        attribute='Characteristics of the Preparation Form', entity=f'{preparation}', context='herbal medicine', 
        regen=regen_function, dispel=dispel_function
    )
    preparation_subordinate_html = subordinate__gen(json_article_filepath, 
        key='preparation', 
        attribute='Preparation Method', entity=f'{preparation}', context='herbal medicine', 
        regen=regen_function, dispel=dispel_function
    )
    ingredients_subordinate_html = subordinate__gen(json_article_filepath, 
        key='ingredients', 
        attribute='Ingredients and Plant Materials Used', entity=f'{preparation}', context='herbal medicine', 
        regen=regen_function, dispel=dispel_function
    )
    solvents_subordinate_html = subordinate__gen(json_article_filepath, 
        key='solvents', 
        attribute='Solvents or Base Materials', entity=f'{preparation}', context='herbal medicine', 
        regen=regen_function, dispel=dispel_function
    )
    chemical_subordinate_html = subordinate__gen(json_article_filepath, 
        key='chemical', 
        attribute='Chemical Extraction and Active Compounds', entity=f'{preparation}', context='herbal medicine', 
        regen=regen_function, dispel=dispel_function
    )
    dosage_subordinate_html = subordinate__gen(json_article_filepath, 
        key='dosage', 
        attribute='Dosage and Administration', entity=f'{preparation}', context='herbal medicine', 
        regen=regen_function, dispel=dispel_function
    )
    therapeutic_subordinate_html = subordinate__gen(json_article_filepath, 
        key='therapeutic', 
        attribute='Therapeutic Uses', entity=f'{preparation}', context='herbal medicine', 
        regen=regen_function, dispel=dispel_function
    )
    advantages_subordinate_html = subordinate__gen(json_article_filepath, 
        key='advantages', 
        attribute='Advantages and Limitations', entity=f'{preparation}', context='herbal medicine', 
        regen=regen_function, dispel=dispel_function
    )
    quality_subordinate_html = subordinate__gen(json_article_filepath, 
        key='quality', 
        attribute='Quality and Standardization', entity=f'{preparation}', context='herbal medicine', 
        regen=regen_function, dispel=dispel_function
    )
    safety_subordinate_html = subordinate__gen(json_article_filepath, 
        key='safety', 
        attribute='Safety and Side Effects', entity=f'{preparation}', context='herbal medicine', 
        regen=regen_function, dispel=dispel_function
    )
    storage_subordinate_html = subordinate__gen(json_article_filepath, 
        key='storage', 
        attribute='Storage and Shelf Life', entity=f'{preparation}', context='herbal medicine', 
        regen=regen_function, dispel=dispel_function
    )
    traditional_subordinate_html = subordinate__gen(json_article_filepath, 
        key='traditional', 
        attribute='Traditional Uses in Herbal Medicine Systems', entity=f'{preparation}', context='herbal medicine', 
        regen=regen_function, dispel=dispel_function
    )
    modern_subordinate_html = subordinate__gen(json_article_filepath, 
        key='modern', 
        attribute='Modern Applications and Research', entity=f'{preparation}', context='herbal medicine', 
        regen=regen_function, dispel=dispel_function
    )

    ########################################
    # html
    ########################################
    ###
    intro_html = f'''
        <h1>
            {preparation.title()} in Herbal Medicine: Uses, Preparation, and Safety
        </h1>
        <p>
            {intro_subordinate_html}
        </p>
        <p>
            Here you can find a more about <a href="/preparations/forms.html">preparation forms</a> in herbal medicine.
        </p>
    '''
    definition_html = f'''
        <section class="article-section">
            <h2>Definition of {preparation.title()}</h2>
            <p>{definition_subordinate_html}</p>
        </section>
    '''
    purpose_html = f'''
        <section class="article-section">
            <h2>Purpose and Role in Herbal Medicine</h2>
            <p>{purpose_subordinate_html}</p>
        </section>
    '''
    characteristics_html = f'''
        <section class="article-section">
            <h2>Characteristics of the Preparation Form</h2>
            <p>{characteristics_subordinate_html}</p>
        </section>
    '''
    preparation_html = f'''
        <section class="article-section">
            <h2>Preparation Method</h2>
            <p>{preparation_subordinate_html}</p>
        </section>
    '''
    ###
    list_html = ''.join([
        f'''<li>
            <a href="/herbs/{item['herb_slug']}.html">{item['herb_name_common']} ({item['herb_name_scientific']})</a>
            </li>''' 
        for item in herbs_names_filtered[:15]
    ])
    ingredients_html = f'''
        <section class="article-section">
            <h2>Ingredients and Plant Materials Used</h2>
            <p>{ingredients_subordinate_html}</p>
            <p>The following list shows a sample of medicinal plants that are used to make {preparation.lower()}.</p>
            <ul>{list_html}</ul>
        </section>
    '''
    ###
    solvents_html = f'''
        <section class="article-section">
            <h2>Solvents or Base Materials</h2>
            <p>{solvents_subordinate_html}</p>
        </section>
    '''
    chemical_html = f'''
        <section class="article-section">
            <h2>Chemical Extraction and Active Compounds</h2>
            <p>{chemical_subordinate_html}</p>
        </section>
    '''
    dosage_html = f'''
        <section class="article-section">
            <h2>Dosage and Administration</h2>
            <p>{dosage_subordinate_html}</p>
        </section>
    '''
    therapeutic_html = f'''
        <section class="article-section">
            <h2>Therapeutic Uses</h2>
            <p>{therapeutic_subordinate_html}</p>
        </section>
    '''
    advantages_html = f'''
        <section class="article-section">
            <h2>Advantages and Limitations</h2>
            <p>{advantages_subordinate_html}</p>
        </section>
    '''
    quality_html = f'''
        <section class="article-section">
            <h2>Quality and Standardization</h2>
            <p>{quality_subordinate_html}</p>
        </section>
    '''
    safety_html = f'''
        <section class="article-section">
            <h2>Safety and Side Effects</h2>
            <p>{safety_subordinate_html}</p>
        </section>
    '''
    storage_html = f'''
        <section class="article-section">
            <h2>Storage and Shelf Life</h2>
            <p>{storage_subordinate_html}</p>
        </section>
    '''
    traditional_html = f'''
        <section class="article-section">
            <h2>Traditional Uses in Herbal Medicine Systems</h2>
            <p>{traditional_subordinate_html}</p>
        </section>
    '''
    modern_html = f'''
        <section class="article-section">
            <h2>Modern Applications and Research</h2>
            <p>{modern_subordinate_html}</p>
        </section>
    '''

    article_html = f'''
        {intro_html}
        {definition_html}
        {purpose_html}
        {characteristics_html}
        {preparation_html}
        {ingredients_html}
        {solvents_html}
        {chemical_html}
        {dosage_html}
        {therapeutic_html}
        {advantages_html}
        {quality_html}
        {safety_html}
        {storage_html}
        {traditional_html}
        {modern_html}
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

def uses__gen():
    url_slug = f'uses'
    meta_title = f'Uses of Herbal Medicine: Conditions, Applications, and Therapeutic Roles'
    meta_description = ''
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

    definition_subordinate_html = subordinate__gen(json_article_filepath, 
        key='definition', 
        attribute='Definition of Herbal Medicine Uses', entity='uses', context='herbal medicine', 
        regen=regen_function, dispel=dispel_function
    )
    principles_subordinate_html = subordinate__gen(json_article_filepath, 
        key='principles', 
        attribute='Principles Behind Herbal Therapeutic Uses', entity='uses', context='herbal medicine', 
        regen=regen_function, dispel=dispel_function
    )
    types_subordinate_html = subordinate__gen(json_article_filepath, 
        key='types', 
        attribute='Types of Herbal Medicine Uses', entity='uses', context='herbal medicine', 
        regen=regen_function, dispel=dispel_function
    )
    preventive_subordinate_html = subordinate__gen(json_article_filepath, 
        key='preventive', 
        attribute='Preventive Uses of Herbal Medicine', entity='uses', context='herbal medicine', 
        regen=regen_function, dispel=dispel_function
    )
    acute_subordinate_html = subordinate__gen(json_article_filepath, 
        key='acute', 
        attribute='Therapeutic Uses for Acute Conditions', entity='uses', context='herbal medicine', 
        regen=regen_function, dispel=dispel_function
    )
    chronic_subordinate_html = subordinate__gen(json_article_filepath, 
        key='chronic', 
        attribute='Therapeutic Uses for Chronic Conditions', entity='uses', context='herbal medicine', 
        regen=regen_function, dispel=dispel_function
    )
    body_subordinate_html = subordinate__gen(json_article_filepath, 
        key='body', 
        attribute='Body System–Based Uses', entity='uses', context='herbal medicine', 
        regen=regen_function, dispel=dispel_function
    )
    symptom_subordinate_html = subordinate__gen(json_article_filepath, 
        key='symptom', 
        attribute='Symptom-Based Uses', entity='uses', context='herbal medicine', 
        regen=regen_function, dispel=dispel_function
    )
    functional_subordinate_html = subordinate__gen(json_article_filepath, 
        key='functional', 
        attribute='Functional Health Uses', entity='uses', context='herbal medicine', 
        regen=regen_function, dispel=dispel_function
    )
    traditional_subordinate_html = subordinate__gen(json_article_filepath, 
        key='traditional', 
        attribute='Traditional Medical Uses', entity='uses', context='herbal medicine', 
        regen=regen_function, dispel=dispel_function
    )
    modern_subordinate_html = subordinate__gen(json_article_filepath, 
        key='modern', 
        attribute='Modern Clinical Uses', entity='uses', context='herbal medicine', 
        regen=regen_function, dispel=dispel_function
    )
    formulas_subordinate_html = subordinate__gen(json_article_filepath, 
        key='formulas', 
        attribute='Herbal Formulas and Combination Uses', entity='uses', context='herbal medicine', 
        regen=regen_function, dispel=dispel_function
    )
    individual_subordinate_html = subordinate__gen(json_article_filepath, 
        key='individual', 
        attribute='Individual Herb vs Formula-Based Uses', entity='uses', context='herbal medicine', 
        regen=regen_function, dispel=dispel_function
    )
    safety_subordinate_html = subordinate__gen(json_article_filepath, 
        key='safety', 
        attribute='Safety Considerations in Herbal Uses', entity='uses', context='herbal medicine', 
        regen=regen_function, dispel=dispel_function
    )
    evidence_subordinate_html = subordinate__gen(json_article_filepath, 
        key='evidence', 
        attribute='Evidence-Based Uses of Herbal Medicine', entity='uses', context='herbal medicine', 
        regen=regen_function, dispel=dispel_function
    )
    limitations_subordinate_html = subordinate__gen(json_article_filepath, 
        key='limitations', 
        attribute='Limitations of Herbal Therapeutic Uses', entity='uses', context='herbal medicine', 
        regen=regen_function, dispel=dispel_function
    )

    ########################################
    # html
    ########################################
    intro_html = f'''
        <h1>
            Uses of Herbal Medicine: Conditions, Applications, and Therapeutic Roles
        </h1>
        <p>
            The uses of <a href="/herbal-medicine.html">herbal medicine</a> refer to the therapeutic, preventive, and supportive ways in which medicinal plants are applied to maintain health or address medical conditions. Herbal remedies are used across traditional and modern healthcare systems to treat symptoms, support physiological functions, and prevent disease through plant-derived preparations such as teas, tinctures, extracts, and topical treatments.
        </p>
    '''
    definition_html = f'''
        <section class="article-section">
            <h2>Definition of Herbal Medicine Uses</h2>
            <p>{definition_subordinate_html}</p>
        </section>
    '''
    principles_html = f'''
        <section class="article-section">
            <h2>Principles Behind Herbal Therapeutic Uses</h2>
            <p>{principles_subordinate_html}</p>
        </section>
    '''
    types_html = f'''
        <section class="article-section">
            <h2>Types of Herbal Medicine Uses</h2>
            <p>{types_subordinate_html}</p>
        </section>
    '''
    preventive_html = f'''
        <section class="article-section">
            <h2>Preventive Uses of Herbal Medicine</h2>
            <p>{preventive_subordinate_html}</p>
        </section>
    '''
    acute_html = f'''
        <section class="article-section">
            <h2>Therapeutic Uses for Acute Conditions</h2>
            <p>{acute_subordinate_html}</p>
        </section>
    '''
    chronic_html = f'''
        <section class="article-section">
            <h2>Therapeutic Uses for Chronic Conditions</h2>
            <p>{chronic_subordinate_html}</p>
        </section>
    '''
    body_html = f'''
        <section class="article-section">
            <h2>Body System–Based Uses</h2>
            <p>{body_subordinate_html}</p>
        </section>
    '''
    symptom_html = f'''
        <section class="article-section">
            <h2>Symptom-Based Uses</h2>
            <p>{symptom_subordinate_html}</p>
            <p><a href="/uses/symptoms.html">Symptom-Based Uses</a></p>
        </section>
    '''
    functional_html = f'''
        <section class="article-section">
            <h2>Functional Health Uses</h2>
            <p>{functional_subordinate_html}</p>
        </section>
    '''
    traditional_html = f'''
        <section class="article-section">
            <h2>Traditional Medical Uses</h2>
            <p>{traditional_subordinate_html}</p>
        </section>
    '''
    modern_html = f'''
        <section class="article-section">
            <h2>Modern Clinical Uses</h2>
            <p>{modern_subordinate_html}</p>
        </section>
    '''
    formulas_html = f'''
        <section class="article-section">
            <h2>Herbal Formulas and Combination Uses</h2>
            <p>{formulas_subordinate_html}</p>
        </section>
    '''
    individual_html = f'''
        <section class="article-section">
            <h2>Individual Herb vs Formula-Based Uses</h2>
            <p>{individual_subordinate_html}</p>
        </section>
    '''
    safety_html = f'''
        <section class="article-section">
            <h2>Safety Considerations in Herbal Uses</h2>
            <p>{safety_subordinate_html}</p>
        </section>
    '''
    evidence_html = f'''
        <section class="article-section">
            <h2>Evidence-Based Uses of Herbal Medicine</h2>
            <p>{evidence_subordinate_html}</p>
        </section>
    '''
    limitations_html = f'''
        <section class="article-section">
            <h2>Limitations of Herbal Therapeutic Uses</h2>
            <p>{limitations_subordinate_html}</p>
        </section>
    '''

    article_html = f'''
        {intro_html}
        {definition_html}
        {principles_html}
        {types_html}
        {preventive_html}
        {acute_html}
        {chronic_html}
        {body_html}
        {symptom_html}
        {functional_html}
        {traditional_html}
        {modern_html}
        {formulas_html}
        {individual_html}
        {safety_html}
        {evidence_html}
        {limitations_html}
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

def uses__symptoms__gen():
    url_slug = f'uses/symptoms'
    meta_title = f'Symptom-Based Uses of Herbal Medicine: Relief, Support, and Natural Remedies'
    meta_description = ''
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

    definition_subordinate_html = subordinate__gen(json_article_filepath, 
        key='definition', 
        attribute='Definition of Symptom-Based Herbal Uses', entity='symptom-based uses', context='herbal medicine', 
        regen=regen_function, dispel=dispel_function
    )
    difference_subordinate_html = subordinate__gen(json_article_filepath, 
        key='difference', 
        attribute='Difference Between Symptom-Based and Condition-Based Treatment', entity='symptom-based uses', context='herbal medicine', 
        regen=regen_function, dispel=dispel_function
    )
    principles_subordinate_html = subordinate__gen(json_article_filepath, 
        key='principles', 
        attribute='Principles of Symptom Relief in Herbal Medicine', entity='symptom-based uses', context='herbal medicine', 
        regen=regen_function, dispel=dispel_function
    )
    categories_subordinate_html = subordinate__gen(json_article_filepath, 
        key='categories', 
        attribute='Categories of Symptoms Treated with Herbs', entity='symptom-based uses', context='herbal medicine', 
        regen=regen_function, dispel=dispel_function
    )
    pain_subordinate_html = subordinate__gen(json_article_filepath, 
        key='pain', 
        attribute='Pain-Related Symptoms', entity='symptom-based uses', context='herbal medicine', 
        regen=regen_function, dispel=dispel_function
    )
    inflammatory_subordinate_html = subordinate__gen(json_article_filepath, 
        key='inflammatory', 
        attribute='Inflammatory Symptoms', entity='symptom-based uses', context='herbal medicine', 
        regen=regen_function, dispel=dispel_function
    )
    digestive_subordinate_html = subordinate__gen(json_article_filepath, 
        key='digestive', 
        attribute='Digestive Symptoms', entity='symptom-based uses', context='herbal medicine', 
        regen=regen_function, dispel=dispel_function
    )
    respiratory_subordinate_html = subordinate__gen(json_article_filepath, 
        key='respiratory', 
        attribute='Respiratory Symptoms', entity='symptom-based uses', context='herbal medicine', 
        regen=regen_function, dispel=dispel_function
    )
    nervous_subordinate_html = subordinate__gen(json_article_filepath, 
        key='nervous', 
        attribute='Nervous System and Mental Symptoms', entity='symptom-based uses', context='herbal medicine', 
        regen=regen_function, dispel=dispel_function
    )
    skin_subordinate_html = subordinate__gen(json_article_filepath, 
        key='skin', 
        attribute='Skin-Related Symptoms', entity='symptom-based uses', context='herbal medicine', 
        regen=regen_function, dispel=dispel_function
    )
    energy_subordinate_html = subordinate__gen(json_article_filepath, 
        key='energy', 
        attribute='Energy and Fatigue Symptoms', entity='symptom-based uses', context='herbal medicine', 
        regen=regen_function, dispel=dispel_function
    )
    immune_subordinate_html = subordinate__gen(json_article_filepath, 
        key='immune', 
        attribute='Immune-Related Symptoms', entity='symptom-based uses', context='herbal medicine', 
        regen=regen_function, dispel=dispel_function
    )
    hormonal_subordinate_html = subordinate__gen(json_article_filepath, 
        key='hormonal', 
        attribute='Hormonal and Metabolic Symptoms', entity='symptom-based uses', context='herbal medicine', 
        regen=regen_function, dispel=dispel_function
    )
    acute_subordinate_html = subordinate__gen(json_article_filepath, 
        key='acute', 
        attribute='Acute vs Chronic Symptom Management', entity='symptom-based uses', context='herbal medicine', 
        regen=regen_function, dispel=dispel_function
    )
    formulations_subordinate_html = subordinate__gen(json_article_filepath, 
        key='formulations', 
        attribute='Herbal Formulations for Symptom Relief', entity='symptom-based uses', context='herbal medicine', 
        regen=regen_function, dispel=dispel_function
    )
    safety_subordinate_html = subordinate__gen(json_article_filepath, 
        key='safety', 
        attribute='Safety and Limitations of Symptom-Based Use', entity='symptom-based uses', context='herbal medicine', 
        regen=regen_function, dispel=dispel_function
    )
    evidence_subordinate_html = subordinate__gen(json_article_filepath, 
        key='evidence', 
        attribute='Evidence for Symptom Relief with Herbs', entity='symptom-based uses', context='herbal medicine', 
        regen=regen_function, dispel=dispel_function
    )

    ########################################
    # html
    ########################################
    intro_html = f'''
        <h1>
            Symptom-Based Uses of Herbal Medicine: Relief, Support, and Natural Remedies
        </h1>
        <p>
            Symptom-based <a href="/uses.html">uses</a> of herbal medicine refer to the application of medicinal plants to relieve or manage specific symptoms such as pain, inflammation, digestive discomfort, stress, or fatigue, rather than directly targeting an underlying disease. These uses focus on improving comfort, supporting physiological function, and providing short-term or long-term relief through plant-based preparations.
        </p>
    '''
    definition_html = f'''
        <section class="article-section">
            <h2>Definition of Symptom-Based Herbal Uses</h2>
            <p>{definition_subordinate_html}</p>
        </section>
    '''
    difference_html = f'''
        <section class="article-section">
            <h2>Difference Between Symptom-Based and Condition-Based Treatment</h2>
            <p>{difference_subordinate_html}</p>
        </section>
    '''
    principles_html = f'''
        <section class="article-section">
            <h2>Principles of Symptom Relief in Herbal Medicine</h2>
            <p>{principles_subordinate_html}</p>
        </section>
    '''
    ###
    list_html = ''
    list_data = data.symptoms_get(10)
    for item in list_data:
        item_slug = item.lower().strip().replace(' ', '-')
        list_html += f'''
            <li>
                <a href="/uses/{item_slug}.html">{item}</a>
            </li>
        ''' 
    categories_html = f'''
        <section class="article-section">
            <h2>Categories of Symptoms Treated with Herbs</h2>
            <p>{categories_subordinate_html}</p>
            <p>The following list shows a sample of common symptoms treated with herbal medicine.</p>
            <ul>{list_html}</ul>
        </section>
    '''
    ###
    pain_html = f'''
        <section class="article-section">
            <h2>Pain-Related Symptoms</h2>
            <p>{pain_subordinate_html}</p>
        </section>
    '''
    inflammatory_html = f'''
        <section class="article-section">
            <h2>Inflammatory Symptoms</h2>
            <p>{inflammatory_subordinate_html}</p>
        </section>
    '''
    digestive_html = f'''
        <section class="article-section">
            <h2>Digestive Symptoms</h2>
            <p>{digestive_subordinate_html}</p>
        </section>
    '''
    respiratory_html = f'''
        <section class="article-section">
            <h2>Respiratory Symptoms</h2>
            <p>{respiratory_subordinate_html}</p>
        </section>
    '''
    nervous_html = f'''
        <section class="article-section">
            <h2>Nervous System and Mental Symptoms</h2>
            <p>{nervous_subordinate_html}</p>
        </section>
    '''
    skin_html = f'''
        <section class="article-section">
            <h2>Skin-Related Symptoms</h2>
            <p>{skin_subordinate_html}</p>
        </section>
    '''
    energy_html = f'''
        <section class="article-section">
            <h2>Energy and Fatigue Symptoms</h2>
            <p>{energy_subordinate_html}</p>
        </section>
    '''
    immune_html = f'''
        <section class="article-section">
            <h2>Immune-Related Symptoms</h2>
            <p>{immune_subordinate_html}</p>
        </section>
    '''
    hormonal_html = f'''
        <section class="article-section">
            <h2>Hormonal and Metabolic Symptoms</h2>
            <p>{hormonal_subordinate_html}</p>
        </section>
    '''
    acute_html = f'''
        <section class="article-section">
            <h2>Acute vs Chronic Symptom Management</h2>
            <p>{acute_subordinate_html}</p>
        </section>
    '''
    formulations_html = f'''
        <section class="article-section">
            <h2>Herbal Formulations for Symptom Relief</h2>
            <p>{formulations_subordinate_html}</p>
        </section>
    '''
    safety_html = f'''
        <section class="article-section">
            <h2>Safety and Limitations of Symptom-Based Use</h2>
            <p>{safety_subordinate_html}</p>
        </section>
    '''
    evidence_html = f'''
        <section class="article-section">
            <h2>Evidence for Symptom Relief with Herbs</h2>
            <p>{evidence_subordinate_html}</p>
        </section>
    '''

    article_html = f'''
        {intro_html}
        {definition_html}
        {difference_html}
        {principles_html}
        {categories_html}
        {pain_html}
        {inflammatory_html}
        {digestive_html}
        {respiratory_html}
        {nervous_html}
        {skin_html}
        {energy_html}
        {immune_html}
        {hormonal_html}
        {acute_html}
        {formulations_html}
        {safety_html}
        {evidence_html}
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

def uses__symptom__gen(symptom):
    symptom = symptom.lower().strip()
    symptom_slug = symptom.replace(' ', '-')
    url_slug = f'uses/{symptom_slug}'
    meta_title = f'Herbal Medicine for {symptom.title()}: Uses, Remedies, and Safety'
    meta_description = ''
    canonical_html = f'''<link rel="canonical" href="https://terrawhisper.com/{url_slug}.html">'''

    herbs_names_filtered = []
    herbs = io.json_read(f'''{g.SSOT_FOLDERPATH}/herbs/herbs-medicinal-validated.json''')
    for herb in herbs:
        herb_name_scientific = herb['taxon_name']
        herb_slug = polish.sluggify(herb_name_scientific)
        herb_data = io.json_read(f'''{g.SSOT_FOLDERPATH}/herbs/herbs-primary/{herb_slug}.json''')
        herb_name_common = herb_data['herb_names_common'][0]['answer']
        ###
        for item in herb_data['herb_symptoms']:
            name = item['answer']
            total_score = item['total_score']
            if name.lower().strip() == symptom.lower().strip():
                if total_score >= 600:
                    found = False
                    for herb_name_filtered in herbs_names_filtered:
                        if herb_name_filtered['herb_name_common'].lower().strip() == herb_name_common.lower().strip():
                            found = True
                            break
                    if not found:
                        herbs_names_filtered.append(
                            {
                                'herb_name_common': herb_name_common,
                                'herb_name_scientific': herb_name_scientific,
                                'herb_slug': herb_slug,
                            }
                        )
    random.shuffle(herbs_names_filtered)

    regen_function = False
    dispel_function = False
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
        attribute='introduction', entity=f'{symptom}', context='herbal medicine', 
        regen=regen_function, dispel=dispel_function
    )
    definition_subordinate_html = subordinate__gen(json_article_filepath, 
        key='definition', 
        attribute='definition', entity=f'{symptom}', context='herbal medicine', 
        regen=regen_function, dispel=dispel_function
    )
    types_subordinate_html = subordinate__gen(json_article_filepath, 
        key='types', 
        attribute='Types of {symptom.title()}', entity=f'{symptom}', context='herbal medicine', 
        regen=regen_function, dispel=dispel_function
    )
    causes_subordinate_html = subordinate__gen(json_article_filepath, 
        key='causes', 
        attribute='Causes of {symptom.title()}', entity=f'{symptom}', context='herbal medicine', 
        regen=regen_function, dispel=dispel_function
    )
    how_subordinate_html = subordinate__gen(json_article_filepath, 
        key='how', 
        attribute='How Herbal Medicine Helps with {symptom.title()}', entity=f'{symptom}', context='herbal medicine', 
        regen=regen_function, dispel=dispel_function
    )
    best_subordinate_html = subordinate__gen(json_article_filepath, 
        key='best', 
        attribute='Best Herbs for {symptom.title()}', entity=f'{symptom}', context='herbal medicine', 
        regen=regen_function, dispel=dispel_function
    )
    actions_subordinate_html = subordinate__gen(json_article_filepath, 
        key='actions', 
        attribute='Herbal Actions Relevant to {symptom.title()}', entity=f'{symptom}', context='herbal medicine', 
        regen=regen_function, dispel=dispel_function
    )
    preparation_subordinate_html = subordinate__gen(json_article_filepath, 
        key='preparation', 
        attribute='Preparation Methods for {symptom.title()} Relief', entity=f'{symptom}', context='herbal medicine', 
        regen=regen_function, dispel=dispel_function
    )
    dosage_subordinate_html = subordinate__gen(json_article_filepath, 
        key='dosage', 
        attribute='Dosage and Administration', entity=f'{symptom}', context='herbal medicine', 
        regen=regen_function, dispel=dispel_function
    )
    combining_subordinate_html = subordinate__gen(json_article_filepath, 
        key='combining', 
        attribute='Combining Herbs for {symptom.title()}', entity=f'{symptom}', context='herbal medicine', 
        regen=regen_function, dispel=dispel_function
    )
    lifestyle_subordinate_html = subordinate__gen(json_article_filepath, 
        key='lifestyle', 
        attribute='Lifestyle and Supportive Measures', entity=f'{symptom}', context='herbal medicine', 
        regen=regen_function, dispel=dispel_function
    )
    when_subordinate_html = subordinate__gen(json_article_filepath, 
        key='when', 
        attribute='When to Use Herbal Medicine for {symptom.title()}', entity=f'{symptom}', context='herbal medicine', 
        regen=regen_function, dispel=dispel_function
    )
    safety_subordinate_html = subordinate__gen(json_article_filepath, 
        key='safety', 
        attribute='Safety and Risks', entity=f'{symptom}', context='herbal medicine', 
        regen=regen_function, dispel=dispel_function
    )
    attention_subordinate_html = subordinate__gen(json_article_filepath, 
        key='attention', 
        attribute='When to Seek Medical Attention', entity=f'{symptom}', context='herbal medicine', 
        regen=regen_function, dispel=dispel_function
    )
    evidence_subordinate_html = subordinate__gen(json_article_filepath, 
        key='evidence', 
        attribute='Scientific Evidence for Herbal Use', entity=f'{symptom}', context='herbal medicine', 
        regen=regen_function, dispel=dispel_function
    )

    ########################################
    # html
    ########################################
    ###
    intro_html = f'''
        <h1>
            Herbal Medicine for {symptom.title()}: Uses, Remedies, and Safety
        </h1>
        <p>
            {intro_subordinate_html}
        </p>
        <p>
            Here you can find a more about <a href="/uses/symptoms.html">symptoms to treat</a> with herbal medicine.
        </p>
    '''
    definition_html = f'''
        <section class="article-section">
            <h2>Definition of {symptom.title()}</h2>
            <p>{definition_subordinate_html}</p>
        </section>
    '''
    types_html = f'''
        <section class="article-section">
            <h2>Types of {symptom.title()}</h2>
            <p>{types_subordinate_html}</p>
        </section>
    '''
    causes_html = f'''
        <section class="article-section">
            <h2>Causes of {symptom.title()}</h2>
            <p>{causes_subordinate_html}</p>
        </section>
    '''
    how_html = f'''
        <section class="article-section">
            <h2>How Herbal Medicine Helps with {symptom.title()}</h2>
            <p>{how_subordinate_html}</p>
        </section>
    '''
    ###
    list_html = ''.join([
        f'''<li>
            <a href="/herbs/{item['herb_slug']}.html">{item['herb_name_common']} ({item['herb_name_scientific']})</a>
            </li>''' 
        for item in herbs_names_filtered[:15]
    ])
    best_html = f'''
        <section class="article-section">
            <h2>Best Herbs for {symptom.title()}</h2>
            <p>{best_subordinate_html}</p>
            <p>The following list shows a sample of medicinal plants that are used to treat {symptom.lower()}.</p>
            <ul>{list_html}</ul>
        </section>
    '''
    ###
    actions_html = f'''
        <section class="article-section">
            <h2>Herbal Actions Relevant to {symptom.title()}</h2>
            <p>{actions_subordinate_html}</p>
        </section>
    '''
    preparation_html = f'''
        <section class="article-section">
            <h2>Preparation Methods for {symptom.title()} Relief</h2>
            <p>{preparation_subordinate_html}</p>
        </section>
    '''
    dosage_html = f'''
        <section class="article-section">
            <h2>Dosage and Administration</h2>
            <p>{dosage_subordinate_html}</p>
        </section>
    '''
    combining_html = f'''
        <section class="article-section">
            <h2>Combining Herbs for {symptom.title()}</h2>
            <p>{combining_subordinate_html}</p>
        </section>
    '''
    lifestyle_html = f'''
        <section class="article-section">
            <h2>Lifestyle and Supportive Measures</h2>
            <p>{lifestyle_subordinate_html}</p>
        </section>
    '''
    when_html = f'''
        <section class="article-section">
            <h2>When to Use Herbal Medicine for {symptom.title()}</h2>
            <p>{when_subordinate_html}</p>
        </section>
    '''
    safety_html = f'''
        <section class="article-section">
            <h2>Safety and Risks</h2>
            <p>{safety_subordinate_html}</p>
        </section>
    '''
    attention_html = f'''
        <section class="article-section">
            <h2>When to Seek Medical Attention</h2>
            <p>{attention_subordinate_html}</p>
        </section>
    '''
    evidence_html = f'''
        <section class="article-section">
            <h2>Scientific Evidence for Herbal Use</h2>
            <p>{evidence_subordinate_html}</p>
        </section>
    '''

    article_html = f'''
        {intro_html}
        {definition_html}
        {types_html}
        {causes_html}
        {how_html}
        {best_html}
        {actions_html}
        {preparation_html}
        {dosage_html}
        {combining_html}
        {lifestyle_html}
        {when_html}
        {safety_html}
        {attention_html}
        {evidence_html}
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
    ###
    herbs__gen()
    ###
    phytochemicals__gen()
    phytochemicals__classification__gen()
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
    actions__gen()
    actions__classification__gen()
    for action in data.actions_get(10):
        actions_action__gen(action)
        # break
    ###
    preparations__gen()
    preparations__forms__gen()
    for item in data.preparations_get(10):
        preparations_preparation__gen(item)
        # break
    # preparations__methods__gen()
    ###
    uses__gen()
    uses__symptoms__gen()
    for item in data.symptoms_get(10):
        uses__symptom__gen(item)
        # break

