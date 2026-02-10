from lib import g
from lib import components
from lib import sections

def sidebar_hub_gen(): 
    html = f'''
        <div>
        <nav class="nav-global">
            <h2 style="margin-top: 0rem;">Main Hub</h2>
            <ul>
                <li><a href="/herbs.html">Medicinal Herbs</a>
                    <ul>
                        <li><a href="herbs/botany.html">Botany</a></li>
                        <li><a href="/preparations.html">Preparations</a></li>
                        <li><a href="/ailments.html">Ailments</a></li>
                    </ul>
                </li>
            </ul>
        </nav>
        </div>
    '''
    return html

def sidebar_page_gen(items): 
    if not items: return ''
    ###
    items_html = f''
    for item in items:
        href = item['href']
        anchor = item['anchor']
        item_html = f'<li><a href="#{href}">{anchor}</a></li>\n'
        items_html += item_html
    html = f'''
        <aside>
            <nav class="nav-page">
                <h2 style="margin-top: 0rem;">Table of Contents</h2>
                <ul>
                    {items_html}
                </ul>
            <nav>
        </aside>
    '''
    return html

def herbs_hub_gen():

    sections_html_list = []

    sections_html_list.append(f'''
        <h1>Medicinal Herbs: Comprehensive Guide</h1>
        <section>
            <p>
                Medicinal herbs are plants that have been used for centuries to support human health, promote well-being, and complement traditional and modern healing practices. 
                They encompass a diverse range of species, each with unique properties, historical uses, and roles in natural medicine systems around the world. 
                From ancient traditions like Ayurveda and Traditional Chinese Medicine to contemporary herbal research, medicinal herbs continue to be a cornerstone of holistic health knowledge.
            </p>
            <p>
                This guide introduces the essential concepts of medicinal herbs, their classification, botanical attributes, and the scientific frameworks used to study their effects. 
                By exploring the fundamental principles behind these plants, you can develop a deeper understanding of their role in natural health, laying the foundation for further learning about specific herbs, their applications, and evidence-based practices.
            </p>
        </section>
    ''')

    sections_html_list.append(f'''
        <section>
            <h2>What Are Medicinal Herbs?</h2>
            <p>
                Medicinal herbs are plants used for their therapeutic properties to support, prevent, or restore human health. 
                These plants contain bioactive compounds and have documented use in traditional and modern medical systems across different cultures and historical periods.
            </p>
            <p>
                As a botanical entity, a medicinal herb is defined not by culinary use, but by its measurable physiological effects, historical medical application, and recognized role in health-related practices.
            </p>
            <h3>How Are Medicinal Herbs Classified Botanically?</h3>
            <p>
                Medicinal herbs are classified based on botanical families, plant structures, and the specific parts used for therapeutic purposes. 
                Commonly used parts include leaves, roots, flowers, seeds, bark, and stems, each associated with distinct chemical constituents.
            </p>
            <p>
                This botanical classification helps organize herbs within natural medicine systems and allows researchers and practitioners to associate specific plant parts with functional health effects.
            </p>
            <h3>What Attributes Define a Medicinal Herb?</h3>
            <p>
                Each medicinal herb is defined by a set of core attributes that distinguish it from other plants. 
                These attributes include its scientific (Latin) name, common names, geographic origin, growth conditions, and morphological characteristics.
            </p>
            <p>
                Additional defining attributes such as seasonal availability, cultivation environment, and traditional therapeutic applications help establish the herb as a distinct medicinal entity within botanical and healthcare contexts.
            </p>
        </section>
    ''')

    sections_html_list.append(f'''
        <section>
            <h2>How do medicinal herbs work in the human body?</h2>
            <p>
                Medicinal herbs work through bioactive chemical compounds that interact with human biological systems at molecular and cellular levels. 
                These compounds influence enzymes, receptors, and physiological pathways, producing therapeutic effects such as antioxidant, anti-inflammatory, or immune-modulating activity.
            </p>
            <h3>What are the active compounds in medicinal herbs?</h3>
            <p>
                The primary active compounds in medicinal herbs include alkaloids, flavonoids, terpenes, glycosides, and phenolic acids. 
                These bioactive substances are responsible for measurable biological effects, such as reducing oxidative stress, modulating inflammation, supporting immune responses, or influencing nervous system signaling.
            </p>
            <p>
                Each compound class has distinct chemical properties that determine how it is absorbed, metabolized, and utilized by the body. 
                The concentration and combination of these compounds vary by plant species, plant part, and preparation method.
            </p>
            <h3>What is the mechanism of action of medicinal herbs?</h3>
            <p>
                The mechanism of action of medicinal herbs describes how their active compounds interact with biological targets. 
                Common mechanisms include enzyme inhibition or activation, receptor binding, antioxidant activity, modulation of gene expression, and effects on cellular signaling pathways.
            </p>
            <p>
                These mechanisms explain how herbal compounds produce consistent physiological outcomes and help researchers classify herbs based on functional effects rather than traditional usage alone.
            </p>
        </section>
    ''')

    sections_html_list.append(f'''
        <section>
            <h2>What Are Medicinal Herbs Used For?</h2>
            <p>
                Medicinal herbs are used to support human health by influencing physiological systems such as digestion, immunity, sleep regulation, inflammation response, skin function, cardiovascular health, hormonal balance, and cognitive performance. Their uses are based on traditional medicine systems and supported by modern observational research.
            </p>
            <p>
                These applications describe the functional roles of medicinal plants rather than specific preparation methods or dosage guidelines. Understanding herbal uses helps classify plants according to the health outcomes they are commonly associated with.
            </p>
            <h3>Common Health Functions Supported by Medicinal Herbs</h3>
            <p>
                Medicinal herbs are commonly associated with digestive support, immune system modulation, sleep quality improvement, pain and inflammation management, skin health maintenance, cardiovascular support, hormonal regulation, and cognitive and nervous system support.
            </p>
            <p>
                Each of these health functions represents a therapeutic category in which herbs are traditionally grouped based on observed effects, active compounds, and historical usage patterns.
            </p>
            <h3>Medicinal Herbs by Ailments and Conditions</h3>
            <p>
                Medicinal herbs are often categorized according to the ailments and conditions they are used to support. This condition-based classification helps users identify herbs relevant to specific health concerns, such as digestive discomfort, immune challenges, sleep disturbances, or inflammatory conditions.
            </p>
            <p>
                Detailed information about individual herbs and their associations with specific <a href="/ailments.html">ailments and conditions</a> is provided on dedicated pages to allow focused and contextual exploration.
            </p>
            <h3>Why Different Herbs Are Used for Different Conditions</h3>
            <p>
                Different herbs are used for different conditions because each plant contains distinct bioactive compounds that influence specific biological processes. As a result, certain herbs are historically associated with digestive support, while others are linked to calming, anti-inflammatory, or restorative effects.
            </p>
        </section>
    ''')

    sections_html_list.append(f'''
        <section>
            <h2>How Are Medicinal Herbs Commonly Used?</h2>
            <p>
                Medicinal herbs are commonly used through specific preparation and administration methods that determine how their bioactive compounds are delivered to the body. These methods include traditional liquid extractions and modern standardized formats, each influencing absorption, convenience, and practical use.
            </p>
            <h3>Traditional Herbal Preparation Methods</h3>
            <p>
                Traditional medicinal systems prepare herbs using techniques designed to extract water- or alcohol-soluble compounds. Common traditional preparations include herbal teas, infusions, decoctions, and tinctures, which differ based on temperature, extraction time, and plant part used.
            </p>
            <h3>Modern Forms of Herbal Use</h3>
            <p>
                Modern herbal preparations focus on convenience, consistency, and shelf stability. These commonly include capsules, powders, topical ointments, and essential oils, allowing herbs to be consumed or applied in standardized and portable forms.
            </p>
            <h3>General Principles of Herbal Administration</h3>
            <p>
                Herbal administration depends on factors such as preparation type, intended use, and individual characteristics. General principles emphasize appropriate form selection, responsible use, and reliance on accurate informational sources rather than fixed, universal dosing rules.
            </p>
            <p>
                For detailed explanations of preparation types and administration methods, visit the 
                <a href="/preparations.html">Preparations hub</a>, which organizes guidance by herb and usage format.
            </p>
        </section>
    ''')

    sections_html_list.append(f'''
        <section>
            <h2>What safety considerations are important when using medicinal herbs?</h2>
            <p>
                Safety considerations for medicinal herbs include potential side effects, toxicity risks, drug interactions, and population-specific precautions. 
                Understanding these factors helps ensure herbs are used responsibly, reduces adverse health outcomes, and supports informed evaluation of their therapeutic use.
            </p>
            <h3>What side effects and toxicity risks can medicinal herbs cause?</h3>
            <p>
                Medicinal herbs may cause side effects ranging from mild digestive upset to severe toxic reactions, depending on the plant species, dosage, preparation method, and individual sensitivity. 
                Some herbs contain bioactive compounds that can become harmful when misidentified, improperly prepared, or consumed in excessive amounts.
            </p>
            <h3>How do medicinal herbs interact with medications?</h3>
            <p>
                Medicinal herbs can interact with prescription or over-the-counter drugs by enhancing, reducing, or altering their pharmacological effects. 
                These interactions may affect drug metabolism, absorption, or efficacy, increasing the risk of side effects or reducing therapeutic effectiveness.
            </p>
            <h3>Which populations require extra precautions when using medicinal herbs?</h3>
            <p>
                Pregnant individuals, children, older adults, and people with chronic conditions often require additional precautions when using medicinal herbs. 
                Physiological differences and existing health factors can increase sensitivity to herbal compounds, making professional guidance especially important.
            </p>
        </section>
    ''')

    sections_html_list.append(f'''
        <section>
            <!-- Section: Scientific Evidence and Research -->
            <h2>What does scientific research say about medicinal herbs?</h2>
            <p>
                Scientific research on medicinal herbs evaluates their efficacy, safety, and mechanisms of action using clinical trials, observational studies, and laboratory research, helping determine which herbal medicines are supported by evidence and how traditional uses align with modern medical findings.
            </p>
            <p>
                Research on medicinal herbs focuses on the herb as the primary entity, with key attributes including therapeutic effects, active compounds, dosage, safety profile, and clinical relevance. Evidence strength varies depending on study design, population size, and standardization of herbal preparations.
            </p>
            <h3>What types of clinical studies are conducted on medicinal herbs?</h3>
            <p>
                Clinical studies on medicinal herbs include randomized controlled trials, cohort studies, case reports, and meta-analyses that assess effectiveness, adverse effects, interactions, and biological mechanisms in human and laboratory settings.
            </p>
            <p>
                Randomized controlled trials measure specific outcomes such as symptom reduction or biomarker changes, while observational studies examine real-world usage patterns. Meta-analyses aggregate multiple studies to evaluate overall evidence quality and consistency.
            </p>
            <h3>How does traditional herbal evidence differ from modern scientific evidence?</h3>
            <p>
                Traditional herbal evidence is based on historical use and empirical observation, whereas modern scientific evidence relies on controlled experimentation, standardized dosing, and reproducible results to confirm efficacy and safety.
            </p>
            <p>
                Systems such as Ayurveda, Traditional Chinese Medicine, and European herbalism document long-term use patterns, while modern research tests these applications through pharmacological analysis, clinical trials, and safety assessments to validate or refine traditional claims.
            </p>
        </section>
    ''')

    items = [
        {'href': 'intro', 'anchor': 'Introduction'},
        {'href': 'definition', 'anchor': 'Definition'},
        {'href': 'mechanisms', 'anchor': 'Mechanisms'},
        {'href': 'uses', 'anchor': 'Uses'},
        {'href': 'preparations', 'anchor': 'Preparations'},
        {'href': 'safety', 'anchor': 'Safety'},
        {'href': 'research', 'anchor': 'Research'},
    ]

    sections_html_list_new = []
    for i, html in enumerate(sections_html_list):
        html_new = html.replace('<section>', f'''<section id="{items[i]['href']}">''')
        sections_html_list_new.append(html_new)


    content_html = f''.join(sections_html_list_new)

    url_slug = f'herbs'
    meta_title = 'Herbs – Complete Guide to Medicinal, Culinary & Healing Herbs'
    meta_description = 'Explore over 100,000 herbs, their benefits, uses, preparations, and related herbalism topics. Find herbs for stress, digestion, immunity, and more.'
    canonical_html = f'''<link rel="canonical" href="https://terrawhisper.com/herbs.html">'''

    head_html = components.html_head(meta_title, meta_description, css='/styles-herb.css', canonical=canonical_html)
    toc_html = f'''
<!-- Table of Contents -->
<nav aria-label="Table of Contents" id="table-of-contents">
  <h2>Contents</h2>
  <ul>
    <li><a href="#intro">Introduction</a></li>
    <li><a href="#what-are-herbs">What Are Medicinal Herbs?</a>
      <ul>
        <li><a href="#botanical-classification">Botanical Classification</a></li>
        <li><a href="#core-attributes">Core Attributes of Medicinal Herbs</a></li>
      </ul>
    </li>
    <li><a href="#mechanisms">Mechanisms and Active Compounds</a>
      <ul>
        <li><a href="#active-compounds">Active Compounds</a></li>
        <li><a href="#mechanism-of-action">Mechanism of Action</a></li>
      </ul>
    </li>
    <li><a href="#therapeutic-applications">Uses of Medicinal Herbs</a>
      <ul>
        <li><a href="#common-ailments">Common Ailments Treated</a></li>
        <li><a href="#targeted-herbs">Targeted Herbs per Condition</a></li>
      </ul>
    </li>
    <li><a href="#preparations">How to Use Medicinal Herbs</a>
      <ul>
        <li><a href="#traditional-preparations">Traditional Preparations</a></li>
        <li><a href="#modern-preparations">Modern Preparations</a></li>
        <li><a href="#dosage-tips">Dosage and Administration Tips</a></li>
      </ul>
    </li>
    <li><a href="#safety">Safety Considerations</a>
      <ul>
        <li><a href="#side-effects">Side Effects and Toxicity</a></li>
        <li><a href="#drug-interactions">Drug Interactions</a></li>
        <li><a href="#special-populations">Special Populations</a></li>
      </ul>
    </li>
    <li><a href="#evidence">Scientific Research on Medicinal Herbs</a>
      <ul>
        <li><a href="#clinical-studies">Clinical Studies</a></li>
        <li><a href="#traditional-vs-modern">Traditional vs Modern Evidence</a></li>
      </ul>
    </li>
    <li><a href="#further-exploration">Further Exploration</a>
      <ul>
        <li><a href="#comparisons">Herb Comparisons and Alternatives</a></li>
        <li><a href="#formulas">Herbal Combinations and Formulas</a></li>
        <li><a href="#additional-resources">Additional Resources</a></li>
      </ul>
    </li>
    <li><a href="#summary">Summary</a></li>
  </ul>
</nav>
    '''

    attribute_cluster_html = f'''
        Medicinal Herbs</h1>

        Entity Definition & Identity
        Origin & Source Attributes
        Classification Attributes
        Active Components & Chemical Attributes
        Mechanism of Action
        Preparation & Form Attributes
        Dosage & Administration Attributes
        Therapeutic Uses & Indications
        Safety & Risk Attributes
        Quality, Purity & Evaluation Attributes
        Evidence & Validation Attributes
        Legal & Regulatory Attributes
        Cultural & Historical Attributes
        Comparison & Relationship Attributes
        Limitations & Misconceptions
        Future & Research Attributes
    '''

    '''
        Definition (concept, meaning, differentiation, scope)
        Botany (taxonomy, plant parts, species, cultivation types)
        Phytochemistry (active compounds, chemical classes, bioavailability)
        Therapeutics (health uses, conditions, systems, outcomes)
        Traditions (TCM, Ayurveda, Western, indigenous systems, energetics)
        Preparation (forms, methods, administration routes)
        Safety (dosage, toxicity, interactions, contraindications)
        Evidence (research, studies, mechanisms, validation)
        Regulation (legal status, standards, compliance, quality control)
        Cultivation (growing, harvesting, storage, sustainability)
        Selection (comparisons, choice criteria, formats, quality)
        History (cultural, historical, social context)
        Commerce (market, supply chains, sourcing, economics)
    '''

    '''
        What are medicinal herbs? (Definition)
        How are medicinal herbs classified botanically? (Botany)
        What compounds do medicinal herbs contain? (Phytochemistry)
        What are medicinal herbs used for? (Therapeutics)
        Which traditions use medicinal herbs? (Traditions)
        How are medicinal herbs prepared? (Preparation)
        Are medicinal herbs safe to use? (Safety)
        What evidence supports medicinal herbs? (Evidence)
        How are medicinal herbs regulated? (Regulation)
        How are medicinal herbs grown and harvested? (Cultivation)
        How do you choose medicinal herbs? (Selection)
        How have medicinal herbs been used historically? (History)
        How are medicinal herbs produced and sold? (Commerce)
    '''

    article_html = f'''
<h1>Medicinal Herbs</h1>

<section>
  <h2>What are medicinal herbs?</h2>
  <p>Medicinal herbs are plants used to support human health through bioactive compounds that produce therapeutic effects. They are applied in traditional medicine and modern herbalism to prevent disease, manage symptoms, and support physiological functions.</p>
</section>

<section>
  <h2>How are medicinal herbs classified botanically?</h2>
  <p>Medicinal herbs are classified botanically by plant family, genus, species, and the plant parts used, including leaves, roots, flowers, seeds, and bark. Botanical classification also distinguishes annual, biennial, and perennial medicinal herbs.</p>
</section>

<section>
  <h2>What compounds do medicinal herbs contain?</h2>
  <p>Medicinal herbs contain bioactive compounds such as alkaloids, flavonoids, terpenes, glycosides, saponins, tannins, and essential oils. These phytochemicals determine the biological activity, potency, and therapeutic properties of medicinal herbs.</p>
</section>

<section>
  <h2>What are medicinal herbs used for?</h2>
  <p>Medicinal herbs are used to support health conditions related to inflammation, digestion, immunity, stress, sleep, pain, and metabolic balance. Their therapeutic uses depend on active compounds, preparation method, dosage, and traditional or clinical application.</p>
</section>

<section>
  <h2>Which traditions use medicinal herbs?</h2>
  <p>Medicinal herbs are used in traditions such as Ayurveda, Traditional Chinese Medicine, Western herbalism, Indigenous medicine, and Unani medicine. Each system applies medicinal herbs according to unique diagnostic models, energetics, and therapeutic principles.</p>
</section>

<section>
  <h2>How are medicinal herbs prepared?</h2>
  <p>Medicinal herbs are prepared as infusions, decoctions, tinctures, extracts, powders, capsules, salves, and syrups. Preparation methods influence compound concentration, bioavailability, absorption, and the overall effectiveness of medicinal herbs.</p>
</section>

<section>
  <h2>Are medicinal herbs safe to use?</h2>
  <p>Medicinal herbs can be safe when used with proper dosage, preparation, and medical context. Safety depends on toxicity, side effects, herb-drug interactions, pregnancy status, chronic conditions, and guidance from qualified healthcare professionals.</p>
</section>

<section>
  <h2>What evidence supports medicinal herbs?</h2>
  <p>Evidence supporting medicinal herbs includes clinical trials, in vitro studies, in vivo research, and identified mechanisms of action. The reliability of evidence varies by herb, formulation, dosage, study design, and consistency of research findings.</p>
</section>

<section>
  <h2>How are medicinal herbs regulated?</h2>
  <p>Medicinal herbs are regulated differently across regions and are commonly classified as dietary supplements or herbal medicines. Oversight may involve authorities such as the FDA, EMA, and WHO, with varying requirements for quality, safety, and labeling.</p>
</section>

<section>
  <h2>How are medicinal herbs grown and harvested?</h2>
  <p>Medicinal herbs are grown through cultivation or wildcrafting and harvested at specific growth stages to maximize potency. Drying, storage, sustainability practices, and post-harvest handling directly affect herbal quality and shelf life.</p>
</section>

<section>
  <h2>How do you choose medicinal herbs?</h2>
  <p>Medicinal herbs are chosen based on quality, authenticity, preparation form, standardized extracts, certifications, and intended health goals. Careful selection improves safety, consistency, and the likelihood of achieving desired therapeutic outcomes.</p>
</section>

<section>
  <h2>How have medicinal herbs been used historically?</h2>
  <p>Medicinal herbs have been used throughout history in ancient civilizations, folk medicine, and early medical systems. Historical use informed the development of herbal pharmacology, therapeutic traditions, and modern approaches to herbal medicine.</p>
</section>

<section>
  <h2>How are medicinal herbs produced and sold?</h2>
  <p>Medicinal herbs are produced through cultivation, harvesting, processing, and quality control before being sold in local and global markets. Production and distribution involve supply chains, ethical sourcing, regulatory compliance, and quality standards.</p>
</section>
    '''

    article_html_old = f'''
        <h1>Medicinal Herbs</h1>
        <p>Medicinal herbs are plants used for healing, prevention, and overall health. They have active compounds, diverse uses, and specific preparation methods. Understanding their classification, safety, evidence, and cultural context ensures effective and responsible use for health and wellness.</p>

        <section>
            <h2>What are medicinal herbs?</h2>
            <p>Medicinal herbs are plants used to prevent, alleviate, or treat health conditions. They contain bioactive compounds that influence the body’s functions. Traditionally and scientifically, they serve therapeutic purposes without being classified as pharmaceutical drugs.</p>
        </section>

        <section>
            <h2>Where do medicinal herbs come from?</h2>
            <p>Medicinal herbs come from specific plants, including leaves, roots, flowers, seeds, and bark. They grow naturally in the wild or are cultivated on farms. Geographic region, climate, and soil conditions directly affect their potency and characteristics.</p>
        </section>

        <section>
            <h2>How are medicinal herbs classified?</h2>
            <p>Medicinal herbs are classified by botanical family, genus, and species, by therapeutic function, and by traditional systems like Ayurveda or Traditional Chinese Medicine. They can also be grouped by body system, effects, or chemical composition for practical use.</p>
        </section>

        <section>
            <h2>What are their active components?</h2>
            <p>Medicinal herbs contain bioactive compounds such as alkaloids, flavonoids, terpenes, glycosides, polyphenols, and essential oils. These components produce therapeutic effects by interacting with the body’s systems, influencing metabolism, inflammation, immunity, and cellular functions.</p>
        </section>

        <section>
            <h2>How do medicinal herbs work?</h2>
            <p>Medicinal herbs work by interacting with the body’s biological systems to produce therapeutic effects. Their active compounds influence processes such as inflammation, immunity, digestion, and nervous system function, supporting health naturally and modulating physiological responses.</p>
        </section>

        <section>
            <h2>How are they prepared?</h2>
            <p>Medicinal herbs are prepared by drying, crushing, or extracting plant parts. Common methods include teas, decoctions, tinctures, powders, capsules, and topical applications. Preparation depends on the herb, intended use, and desired potency.</p>
        </section>

        <section>
            <h2>How are they dosed?</h2>
            <p>Medicinal herbs are dosed according to age, weight, and health condition. Standardized amounts vary by preparation type, such as teas, tinctures, or capsules. Frequency and duration depend on therapeutic goals and individual response to ensure safe, effective use.</p>
        </section>

        <section>
            <h2>What are their uses?</h2>
            <p>Medicinal herbs are used to prevent and treat health conditions, support bodily functions, and promote overall wellness. They can address specific symptoms, strengthen immunity, and complement conventional treatments, offering both therapeutic and preventive benefits for various ailments.</p>
        </section>

        <section>
            <h2>Are they safe?</h2>
            <p>Medicinal herbs can be safe when used correctly, but some may cause side effects, allergic reactions, or interact with medications. Safety depends on dosage, preparation, individual health, and proper guidance from qualified herbal practitioners.</p>
        </section>

        <section>
            <h2>How is quality evaluated?</h2>
            <p>Quality is evaluated by assessing freshness, purity, and active compound concentration. Standards include third-party testing, contamination checks, and proper storage. Adulteration, pesticides, or heavy metals are identified to ensure the herb’s effectiveness and safety for use.</p>
        </section>

        <section>
            <h2>What evidence supports them?</h2>
            <p>Medicinal herbs are supported by both traditional knowledge and modern scientific research. Clinical studies, pharmacological analyses, and systematic reviews provide evidence for their therapeutic effects. Evidence strength varies, with some herbs extensively studied and others primarily supported by historical use.</p>
        </section>

        <section>
            <h2>What are the regulations?</h2>
            <p>Regulations for medicinal herbs vary by country, controlling their sale, labeling, and health claims. Some herbs are classified as supplements, others as medicines. Compliance with national agencies, such as the FDA or EMA, ensures safety, quality, and legal distribution.</p>
        </section>

        <section>
            <h2>What is their history?</h2>
            <p>Medicinal herbs have been used for thousands of years across cultures, including Ayurveda, Traditional Chinese Medicine, and Indigenous practices. Early civilizations documented herbal remedies for health, prevention, and healing, forming the foundation of modern herbal medicine systems worldwide.</p>
        </section>

        <section>
            <h2>How do they compare to other remedies?</h2>
            <p>Medicinal herbs differ from pharmaceuticals, supplements, and functional foods in that they are natural, whole-plant remedies with multiple active compounds. Unlike isolated drugs, their effects are often synergistic and holistic, targeting multiple body systems simultaneously.</p>
        </section>

        <section>
            <h2>What are common limitations?</h2>
            <p>Medicinal herbs cannot replace all conventional treatments and are not effective for every condition. Their potency varies, interactions with drugs are possible, and evidence may be limited. Incorrect use, dosage errors, or poor-quality herbs can reduce effectiveness or cause harm.</p>
        </section>

        <section>
            <h2>What is the future of medicinal herbs?</h2>
            <p>The future of medicinal herbs lies in evidence-based integration with modern medicine, personalized herbal therapies, and sustainable cultivation. Advances in biotechnology and research will enhance safety, efficacy, and accessibility, bridging traditional knowledge with scientific validation.</p>
        </section>
    '''

    import textwrap
    sidebar_hub_html = sidebar_hub_gen()
    sidebar_page_html = sidebar_page_gen(items) 
    html = textwrap.dedent(f''' 
        <!DOCTYPE html>
        <html lang="en">
        {head_html}
        <body>
            {sections.header_default()}
            <div class="hub">
                {sidebar_hub_html}
                <main>
                    <article>
                        {article_html}
                    </article>
                </main>
                {sidebar_page_html}
            </div>
            {sections.footer()}
        </body>
        </html>
    ''').strip()
    html_filepath = f'''{g.website_folderpath}/{url_slug}.html'''
    with open(html_filepath, 'w') as f: f.write(html)

def herbs_ailment_hub_gen():
    url_slug = f'ailments'
    meta_title = ''
    meta_description = ''
    canonical_html = f'''<link rel="canonical" href="https://terrawhisper.com/{url_slug}.html">'''
    head_html = components.html_head(meta_title, meta_description, css='/styles-herb.css', canonical=canonical_html)
    main_html = f'''
<main>
<article>
<!-- Introduction to Common Ailments -->
<h1>Common Ailments and Medicinal Herb Support</h1>
<p>
Common ailments are frequently occurring health conditions that can affect daily comfort, energy, and overall quality of life. 
These conditions include digestive discomfort, mild pain, sleep disturbances, stress, immune challenges, and minor skin issues. 
For a <a href="/ailments/all.html">complete list of common ailments</a> with detailed descriptions, see our dedicated page.
</p>
<p>
Medicinal herbs have been used for centuries to support the body's natural processes in addressing these ailments. 
Through bioactive compounds such as flavonoids, terpenes, and alkaloids, herbs can interact with physiological systems to promote balance, reduce discomfort, and enhance resilience. 
This guide categorizes common ailments by body system and functional effect, providing an overview of herbal support and laying the foundation for exploring specific herbs and their applications in the sections below.
</p>

<!-- Section 1: Digestive Ailments -->
<h2>Digestive Ailments</h2>
<p>
Digestive ailments encompass a range of common conditions affecting the gastrointestinal system, including bloating, indigestion, nausea, and general discomfort. 
These issues can impact nutrient absorption, energy levels, and overall well-being. 
Medicinal herbs have traditionally been used to support digestion, soothe the stomach, and maintain healthy gut function.
</p>
<h3>Gastric and Stomach Issues</h3>
<p>
Herbs such as ginger, peppermint, fennel, and chamomile have long been applied to relieve nausea, reduce stomach cramps, and calm digestive discomfort. 
These plants contain natural compounds that support the stomach lining, regulate motility, and provide gentle relief from irritation. 
For detailed profiles on each herb, including their traditional and modern applications, see the dedicated herb pages linked throughout this section.
</p>
<h3>Digestive Enzyme and Gut Support</h3>
<p>
Certain herbs promote digestive enzyme activity, improve nutrient absorption, and support a balanced gut microbiome. 
Examples include papaya, dandelion root, licorice, and slippery elm. 
Incorporating these herbs into your routine may help optimize digestion, reduce bloating, and support overall gastrointestinal health. 
Individual herb pages provide in-depth information on recommended use and supporting research.
</p>

<!-- Section 2: Immune-Related Ailments -->
<h2>Immune System Challenges</h2>
<p>
Immune system challenges refer to conditions where the body's natural defenses are weakened, imbalanced, or overtaxed, increasing susceptibility to infections, seasonal illnesses, and general malaise. 
Supporting immune function is essential for maintaining overall health and resilience, and medicinal herbs have historically been used to help modulate immune responses.
</p>
<h3>Immune-Boosting Herbs</h3>
<p>
Certain herbs, including astragalus, turmeric, reishi mushroom, and elderberry, have been traditionally recognized for their ability to strengthen the immune system. 
These plants contain bioactive compounds that enhance the body's general defenses, support white blood cell function, and promote resilience against common health challenges. 
Dedicated herb pages provide in-depth information on how each of these herbs can be used to support immunity.
</p>
<h3>Antiviral and Antimicrobial Support</h3>
<p>
Some medicinal herbs exhibit specific antiviral and antimicrobial properties that can help the body respond to pathogens. 
Examples include echinacea, garlic, thyme, and elderberry, which have been studied for their effects against bacterial and viral infections. 
These herbs offer targeted support for immune challenges while complementing overall immune system function. 
Detailed profiles and evidence for each herb are available on their respective pages.
</p>

<!-- Section 3: Sleep and Stress-Related Ailments -->
<h2>Sleep and Stress Disorders</h2>
<p>
Sleep and stress disorders encompass conditions that disrupt restful sleep, relaxation, and overall mental balance. 
Insomnia, difficulty falling asleep, frequent waking, anxiety, and chronic stress can affect energy, mood, and general well-being. 
Medicinal herbs have long been used to promote calm, support sleep quality, and help the body adapt to stress.
</p>
<h3>Sleep Support</h3>
<p>
Certain herbs, such as valerian, chamomile, lemon balm, and passionflower, are traditionally recognized for their ability to improve sleep quality and reduce insomnia. 
These plants contain natural compounds that help relax the nervous system, regulate sleep cycles, and promote a sense of calm. 
For detailed guidance on each herb and its applications, see the dedicated herb pages linked throughout this section.
</p>
<h3>Stress and Anxiety Relief</h3>
<p>
Adaptogenic and calming herbs, including ashwagandha, rhodiola, holy basil, and ginseng, help the body respond to physical and mental stressors. 
These herbs support hormonal balance, modulate cortisol levels, and enhance resilience to anxiety and tension. 
Individual herb profiles provide more information on traditional use, supporting evidence, and practical applications.
</p>

<!-- Section 4: Pain and Inflammatory Conditions -->
<h2>Pain and Inflammation</h2>
<p>
Pain and inflammatory conditions include mild to moderate discomfort, swelling, and irritation in muscles, joints, or tissues. 
These issues can arise from everyday activities, minor injuries, or chronic low-grade inflammation, affecting mobility, comfort, and overall wellness. 
Medicinal herbs have been traditionally applied to reduce inflammation and relieve pain through natural bioactive compounds.
</p>
<h3>Anti-inflammatory Herbs</h3>
<p>
Several herbs, such as turmeric, ginger, willow bark, and boswellia, are known for their anti-inflammatory properties. 
These plants contain compounds that help modulate inflammatory pathways, reduce swelling, and support recovery from minor injuries or chronic inflammation. 
Individual herb pages provide detailed information on their traditional use, efficacy, and recommended applications.
</p>
<h3>Pain-Relieving Herbs</h3>
<p>
Pain-relieving herbs, including clove, capsicum, peppermint, and arnica, offer natural analgesic effects for mild discomfort. 
They may help reduce localized pain, soothe muscle tension, and provide gentle relief without synthetic medications. 
Dedicated herb profiles offer further insights into their mechanisms, uses, and practical applications.
</p>

<!-- Section 5: Skin-Related Ailments -->
<h2>Skin Conditions</h2>
<p>
Skin conditions encompass common dermatological issues such as dryness, irritation, minor wounds, rashes, and inflammation. 
These conditions can affect comfort, appearance, and overall skin health, making supportive care important. 
Medicinal herbs have been traditionally used both topically and systemically to maintain healthy skin and aid in healing.
</p>
<h3>Topical Application Herbs</h3>
<p>
Certain herbs, including aloe vera, calendula, comfrey, and tea tree, are applied externally to soothe irritation, promote wound healing, and reduce inflammation. 
Their natural compounds support skin repair, calm redness, and provide antimicrobial benefits. 
Detailed profiles of these herbs explain their traditional uses, preparation methods, and applications for various skin concerns.
</p>
<h3>Systemic Skin Support</h3>
<p>
Other herbs, such as burdock root, chamomile, and gotu kola, are taken internally to support overall skin health. 
These plants can help balance inflammatory responses, promote detoxification, and nourish the skin from within. 
Individual herb pages provide guidance on usage, efficacy, and supporting evidence for systemic skin support.
</p>

<!-- Section 6: Cardiovascular Conditions -->
<h2>Heart and Circulatory Ailments</h2>
<p>
Heart and circulatory ailments include conditions that affect cardiac function, blood flow, and overall vascular health. 
These issues can manifest as high or low blood pressure, poor circulation, or imbalances in cholesterol levels, potentially impacting energy, endurance, and long-term cardiovascular wellness. 
Medicinal herbs have traditionally been used to support healthy heart function, maintain vascular tone, and promote balanced circulation.
</p>
<h3>Blood Pressure and Circulation</h3>
<p>
Certain herbs, such as hawthorn, garlic, and ginkgo, are known to support healthy circulation and maintain optimal blood pressure. 
These plants can enhance vascular flexibility, improve blood flow, and promote oxygen delivery throughout the body. 
Individual herb pages provide detailed guidance on traditional applications, observed effects, and evidence supporting cardiovascular support.
</p>
<h3>Cholesterol and Heart Function</h3>
<p>
Other herbs, including red yeast rice, green tea, and flaxseed, help support healthy cholesterol levels and overall heart function. 
They contain bioactive compounds that contribute to lipid balance, reduce oxidative stress, and promote long-term cardiovascular health. 
Dedicated herb profiles offer in-depth information on their uses, mechanisms, and practical applications.
</p>


<!-- Section 7: Hormonal and Endocrine Disorders -->
<h2>Hormonal Balance Issues</h2>
<p>
Hormonal balance issues encompass conditions related to the endocrine system, including menstrual irregularities, reproductive health concerns, menopausal symptoms, low testosterone, and general hormonal dysregulation. 
These imbalances can affect energy, mood, metabolism, and overall well-being. 
Medicinal herbs have traditionally been used to support endocrine function, regulate hormones, and promote systemic balance.
</p>
<h3>Female Hormonal Support</h3>
<p>
Herbs such as vitex (chasteberry), black cohosh, maca, and dong quai have long been applied to support female reproductive and hormonal health. 
They can assist with menstrual cycle regulation, alleviate menopausal symptoms, and support fertility. 
Individual herb pages provide detailed insights on traditional use, modern applications, and supporting evidence.
</p>
<h3>Male Hormonal Support</h3>
<p>
For male hormonal health, herbs like tribulus, ginseng, and saw palmetto are traditionally used to support testosterone levels, fertility, and overall endocrine function. 
These plants help maintain hormonal balance, support reproductive health, and enhance vitality. 
Dedicated herb profiles explain their mechanisms, traditional uses, and practical guidance.
</p>

<!-- Section 8: Cognitive and Neurological Concerns -->
<h2>Cognitive and Brain Health</h2>
<p>
Cognitive and neurological concerns include conditions affecting memory, focus, mental clarity, mood, and overall brain function. 
These issues can impact learning, productivity, emotional balance, and daily performance. 
Medicinal herbs have been traditionally used to support cognitive function, protect neural pathways, and promote mental resilience.
</p>
<h3>Memory and Concentration Support</h3>
<p>
Herbs such as ginkgo, bacopa, rosemary, and gotu kola are known for their ability to enhance memory, attention, and overall cognitive performance. 
These plants contain bioactive compounds that improve cerebral circulation, support neurotransmitter function, and facilitate mental clarity. 
Dedicated herb pages provide detailed information on traditional use, modern research, and practical applications for cognitive support.
</p>
<h3>Neuroprotective and Mood-Supporting Herbs</h3>
<p>
Other herbs, including rhodiola, ashwagandha, sage, and lemon balm, offer neuroprotective effects and help maintain emotional balance. 
They support the nervous system, reduce stress-related cognitive decline, and promote resilience against mood disturbances. 
Individual herb profiles provide further insights on mechanisms, applications, and evidence-based benefits.
</p>
</article>
</main>
    '''

    sidebar_hub_html = sidebar_hub_gen()
    sidebar_page_html = '<div></div>'
    import textwrap
    html = textwrap.dedent(f''' 
        <!DOCTYPE html>
        <html lang="en">
        {head_html}
        <body>
            {sections.header_default()}
            <div class="hub">
                {sidebar_hub_html}
                {main_html}
                {sidebar_page_html}
            </div>
            {sections.footer()}
        </body>
        </html>
    ''').strip()
    html_filepath = f'''{g.website_folderpath}/{url_slug}.html'''
    with open(html_filepath, 'w') as f: f.write(html)

def herbs_preparations_hub_gen():
    url_slug = f'preparations'
    meta_title = ''
    meta_description = ''
    canonical_html = f'''<link rel="canonical" href="https://terrawhisper.com/{url_slug}.html">'''
    head_html = components.html_head(meta_title, meta_description, css='/styles-herb.css', canonical=canonical_html)
    import textwrap
    main_html = f'''
        <main>
            <article>
<h1>Herbal Preparations: Methods and Guidelines</h1>
<p>
Herbal preparations are the structured methods used to process, extract, and deliver the therapeutic components of <a href="/herbs.html">medicinal herbs</a>. 
These methods determine how active compounds are released, absorbed, and utilized by the body, which in turn affects the overall efficacy of the herb. 
Understanding these principles provides the foundation for safe, effective, and targeted use in both traditional and modern contexts.
For a comprehensive overview of every herbal preparation, see the <a href="/preparations/all.html">complete herbal preparations index</a>.
</p>
<p>
The choice of preparation method impacts potency, bioavailability, and intended effects. 
Traditional methods, such as teas, decoctions, and tinctures, have been refined over centuries, while modern approaches, including capsules, standardized extracts, and essential oils, emphasize consistency and convenience. 
Both approaches contribute to the effective use of medicinal herbs and illustrate the evolution of herbal practice.
</p>

<!-- Section 2: Traditional Methods -->
<h2>Traditional Methods</h2>
<p>
Traditional methods of herbal preparations have been refined over centuries to optimize the extraction and delivery of active compounds from medicinal herbs. 
These approaches emphasize the relationship between plant parts, preparation technique, and intended therapeutic effect, forming the foundation of classical herbal practice.
</p>
<h3>Teas and Infusions</h3>
<p>
Teas and infusions involve steeping leaves, flowers, or seeds in hot water to extract water-soluble compounds. 
They are widely used for gentle, daily support of digestion, relaxation, and general wellness. 
This method allows for easy consumption and preserves delicate plant constituents.
</p>
<h3>Decoctions</h3>
<p>
Decoctions are created by boiling tougher plant materials, such as roots, barks, and seeds, in water to release concentrated bioactive compounds. 
This method is traditionally employed for herbs requiring stronger extraction to achieve therapeutic potency.
</p>
<h3>Tinctures</h3>
<p>
Tinctures are alcohol-based extracts that preserve and concentrate the active compounds of herbs. 
They provide a longer shelf life compared with water-based preparations and allow for precise dosing, making them suitable for targeted therapeutic use.
</p>
<h3>Salves, Ointments, and Poultices</h3>
<p>
Topical preparations, including salves, ointments, and poultices, apply herbal extracts directly to the skin. 
These methods are used for localized conditions such as inflammation, muscle soreness, or skin irritations, delivering concentrated compounds directly where they are needed.
</p>

<!-- Section 3: Contemporary Methods -->
<h2>Contemporary Methods</h2>
<p>
Modern herbal preparations have been developed to improve convenience, standardization, and consistent delivery of active compounds from medicinal herbs. 
These formats are designed to provide reproducible potency, precise dosing, and user-friendly administration while complementing traditional methods.
</p>
<h3>Capsules and Tablets</h3>
<p>
Capsules and tablets are standardized oral forms that allow for precise dosing and convenient daily use. 
They are ideal for users seeking consistent potency without the preparation time required for teas or decoctions.
</p>
<h3>Powders and Granules</h3>
<p>
Powders and granules consist of dried and ground plant material, which can be mixed into liquids, food, or smoothies. 
This format preserves the integrity of the herb and offers flexible ways to incorporate medicinal herbs into daily routines.
</p>
<h3>Essential Oils</h3>
<p>
Essential oils are highly concentrated volatile compounds extracted from plant material. 
They are commonly used in aromatherapy, topical applications, and sometimes in oral use under professional guidance, delivering targeted therapeutic benefits.
</p>
<h3>Extracts and Standardized Concentrates</h3>
<p>
Extracts and standardized concentrates provide controlled formulations with measured active compounds. 
These preparations are particularly useful in clinical or research contexts where consistent, reproducible potency is essential for efficacy and safety.
</p>

<!-- Section 4: Best Practices for Herbal Preparations -->
<h2>Best Practices for Herbal Preparations</h2>
<p>
Effective herbal preparations rely not only on the method but also on consistent practices that preserve potency, quality, and safety. 
Applying these general principles ensures that medicinal herbs deliver their intended therapeutic benefits across all preparation types, whether traditional or modern.
</p>
<h3>Dosage Considerations</h3>
<p>
Understanding appropriate dosage is crucial for maximizing the efficacy of herbal preparations. 
While specific dosing varies by herb and condition, high-level guidance emphasizes moderation, gradual introduction, and attention to individual response. 
These principles help users achieve therapeutic outcomes safely and consistently.
</p>
<h3>Storage and Shelf Life</h3>
<p>
Proper storage is essential to maintain the potency and stability of herbal preparations. 
Factors such as temperature, light, humidity, and container type affect how long preparations retain their active compounds. 
Following best practices in storage ensures that herbs remain effective and safe for use over time.
</p>
<h3>Preparation Tools and Techniques</h3>
<p>
Using the right tools and techniques optimizes extraction and quality of herbal preparations. 
Common considerations include clean and appropriate utensils, precise measurement, and correct handling to preserve active compounds. 
Adhering to proper methods contributes to consistent, high-quality results across all preparation types.
</p>

<h2>Choosing the Right Herbal Preparation</h2>
<p>
Selecting the appropriate herbal preparation depends on the intended therapeutic outcome and the characteristics of the medicinal herb. 
Different methods deliver active compounds in varying concentrations, absorption rates, and durations of effect, making the choice of preparation a critical factor in achieving desired benefits.
</p>
<h3>Matching Methods to Desired Effects</h3>
<p>
Certain preparations are better suited for specific applications. 
For example, teas and infusions are gentle and ideal for digestive support, while decoctions provide concentrated effects for systemic conditions. 
Topical salves and ointments deliver compounds directly to affected areas, and tinctures or standardized extracts allow for precise dosing. 
Understanding these relationships ensures that herbal preparations are used effectively and appropriately.
</p>
<h3>Integration with Other Therapies</h3>
<p>
Herbal preparations can be combined with multi-herb formulas or complementary treatments to enhance therapeutic outcomes. 
Selecting methods that harmonize with other interventions, whether traditional remedies or modern approaches, supports holistic wellness. 
This integration emphasizes the strategic role of preparation choice within the broader context of <a href="/herbs.html">medicinal herbs</a>.
</p>
            </article>
        </main>
    '''

    sidebar_hub_html = sidebar_hub_gen()
    sidebar_page_html = '<div></div>'
    import textwrap
    html = textwrap.dedent(f''' 
        <!DOCTYPE html>
        <html lang="en">
        {head_html}
        <body>
            {sections.header_default()}
            <div class="hub">
                {sidebar_hub_html}
                {main_html}
                {sidebar_page_html}
            </div>
            {sections.footer()}
        </body>
        </html>
    ''').strip()
    html_filepath = f'''{g.website_folderpath}/{url_slug}.html'''
    with open(html_filepath, 'w') as f: f.write(html)

def herbs_botany_gen():
    url_slug = 'herbs/botany'

    article_html = f'''
<h1>The Complete Botany of Medicinal Herbs</h1>
<p>
Understanding the botany of medicinal herbs is essential for identifying, cultivating, and using plants safely and effectively. This guide covers taxonomy, plant structures such as roots, stems, leaves, flowers, fruits, and seeds, growth cycles, habitats, phenology, and conservation practices. By linking morphology, biochemistry, and lifecycle knowledge, you can fully grasp how medicinal plants produce bioactive compounds and adapt to different environments, supporting both traditional and modern herbal medicine.
</p>

<section>
  <h2>What is plant taxonomy?</h2>
  <p>Plant taxonomy organizes plants into kingdom, division, class, order, family, genus, and species. It distinguishes hybrids, annuals, perennials, woody, and herbaceous types, providing a standardized system to identify, classify, and study medicinal plants across traditional and scientific contexts.</p>
</section>

<section>
  <h2>What are plant structures?</h2>
  <p>Plant structures include roots, stems, leaves, flowers, fruits, seeds, bark, bulbs, resins, and latex. Each part has distinct traits, functions, and medicinal relevance, helping identify species and determine which plant parts contain bioactive compounds for therapeutic use.</p>
</section>

<section>
  <h2>How do plants grow?</h2>
  <p>Plants grow through germination, vegetative growth, flowering, reproduction, and dormancy. Lifespan varies from annuals, biennials, to perennials, while propagation occurs via seeds, cuttings, grafting, or layering, affecting medicinal potency and cultivation strategies.</p>
</section>

<section>
  <h2>Where do medicinal plants grow?</h2>
  <p>Medicinal plants grow in habitats defined by climate, soil type, sunlight, water, and altitude. Native and exotic species occupy specific ecosystems, often with companion plants, and adapt to environmental stresses to survive and produce bioactive compounds.</p>
</section>

<section>
  <h2>What compounds do plants produce?</h2>
  <p>Plants produce bioactive compounds including secondary metabolites such as alkaloids, flavonoids, terpenes, essential oils, and toxins. These compounds vary by plant part and growth stage, contribute to defense mechanisms, and determine the plant’s medicinal properties.</p>
</section>

<section>
  <h2>How are medicinal plants cultivated?</h2>
  <p>Medicinal plants are cultivated using soil preparation, fertilization, irrigation, pruning, harvesting, and post-harvest handling. Organic or conventional methods influence growth, bioactive compound concentration, quality, and medicinal efficacy while supporting sustainable cultivation practices.</p>
</section>

<section>
  <h2>When do plants change seasonally?</h2>
  <p>Plants change seasonally through leaf emergence, flowering, fruiting, and dormancy cycles. Seasonal variation affects bioactive compound levels, medicinal potency, harvest timing, and ecological interactions in both wild and cultivated environments.</p>
</section>

<section>
  <h2>How are plants identified?</h2>
  <p>Plants are identified by leaf shape, arrangement, flower structure, stem texture, root type, seed morphology, latex, and surface hairs. Accurate identification ensures correct species selection for medicinal use and prevents confusion with toxic or non-medicinal lookalikes.</p>
</section>

<section>
  <h2>How did plants evolve?</h2>
  <p>Plants evolved through adaptations evident in phylogeny, genetic diversity, and structural traits. Evolution shaped reproduction, secondary metabolite production, and species relationships, while molecular markers provide modern tools for classification and understanding medicinal plant lineage.</p>
</section>

<section>
  <h2>How are medicinal plants protected?</h2>
  <p>Medicinal plants are protected by conserving endangered species, addressing habitat loss, maintaining ex situ collections like seed banks, enforcing in situ protection, practicing sustainable harvesting, and preserving biodiversity to ensure ecological balance and long-term medicinal resources.</p>
</section>
    '''

    meta_title = 'Botany of Medicinal Herbs: Plant Structures, Growth & Identification'
    meta_description = 'Explore the botany of medicinal herbs, including plant structures, taxonomy, growth cycles, habitats, and identification. Learn how roots, leaves, flowers, and seeds contribute to medicinal properties and sustainable cultivation practices.'
    canonical_html = f'''<link rel="canonical" href="https://terrawhisper.com/herbs/botany.html">'''
    head_html = components.html_head(meta_title, meta_description, css='/styles-herb.css', canonical=canonical_html)
    import textwrap
    sidebar_hub_html = sidebar_hub_gen()
    sidebar_page_html = sidebar_page_gen([]) 
    html = textwrap.dedent(f''' 
        <!DOCTYPE html>
        <html lang="en">
        {head_html}
        <body>
            {sections.header_default()}
            <div class="hub">
                {sidebar_hub_html}
                <main>
                    <article>
                        {article_html}
                    </article>
                </main>
                {sidebar_page_html}
            </div>
            {sections.footer()}
        </body>
        </html>
    ''').strip()
    html_filepath = f'''{g.website_folderpath}/{url_slug}.html'''
    with open(html_filepath, 'w') as f: f.write(html)


def main():
    herbs_hub_gen()
    herbs_botany_gen()
    herbs_ailment_hub_gen()
    herbs_preparations_hub_gen()

main()

