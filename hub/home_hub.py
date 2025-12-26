from lib import g
from lib import io
from lib import data
from lib import polish
from lib import components
from lib import sections

def gen():
    html_main = ''
    # html_main = f'<h1>Discover the Healing Power of Herbal Medicine<br><span>Backed by Tradition & Science</span></h1>'
    # html_main = f'<h1>Herbalism for Beginners: Herbal Remedies and Natural Healing</h1>'
    # html_main = f'<h1>Herbalism and Herbal Remedies for Natural Healing</h1>'
    html_atf_h1 = f'<h1 style="color: {g.COLOR_CARBON_POWDER }">Herbalism and Herbal Remedies for Natural Healing</h1>'
    html_atf_tagline = f'<p style="color: {g.COLOR_CARBON_POWDER }"><em>Make herbal remedies to heal naturally.</em></p>'
    html_atf_desc = f'''
        <p style="color: {g.COLOR_CARBON_POWDER }">
            <strong>Herbalism</strong> is the practice of using <strong>medicinal herbs</strong> to support health and well-being through simple preparations such as teas, tinctures, salves, and infused oils. This site offers <strong>beginner-friendly, educational guidance</strong> on medicinal herbs, herbal remedies, and their traditional use for common concerns, with an emphasis on <strong>safe and responsible use</strong>.
        </p>
    '''
    html_hero = f'''
        <section class="home-hero" style="padding-top: 9.6rem; padding-bottom: 9.6rem;">
            <div class="container-xl">
                <div style="display: flex; gap: 4.8rem;">
                    <div style="flex: 3;">
                        {html_atf_h1}
                        {html_atf_tagline}
                        {html_atf_desc}
                        <div style="display: flex; gap: 1.6rem;">
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

    html_section_1 = f'''
        <section style="padding-bottom: 9.6rem;">
            <div class="container-xl">
                <h2>What Is Herbalism?</h2>
                <p>
                    Herbalism is the traditional and modern practice of working with <strong>medicinal plants</strong> to create remedies, teas, tinctures, and salves that support everyday health. 
                    It combines plant knowledge, hands-on preparation skills, and an understanding of how herbs have been used historically for digestion, sleep, stress, skin, and immunity.
                </p>
                <div style="display: flex; gap: 4.8rem; margin-top: 4.8rem;">
                    <div style="flex: 1;">
                        <h3>Medicinal Herbs</h3>
                        <p style="margin-bottom: 1.6rem;">Learn about the most common medicinal herbs and their traditional uses for everyday health.</p>
                        <p style="margin-bottom: 1.6rem;"><a href="/herbs.html">Explore Medicinal Herbs</a></p>
                        <img src="/images/home/herbs-medicinal-educational.jpg" alt="Herbs with medicinal properties for educational use in herbalism">
                    </div>
                    <div style="flex: 1;">
                        <h3>Herbal Preparations</h3>
                        <p style="margin-bottom: 1.6rem;">Step-by-step guidance on creating teas, tinctures, salves, and other remedies at home.</p>
                        <p style="margin-bottom: 1.6rem;"><a href="/preparations.html">Learn Herbal Preparation Methods</a></p>
                        <img src="/images/home/herbs-preparations-hands-on.jpg" alt="Herbs with preparation methods for making teas, tinctures, and salves at home">
                    </div>
                    <div style="flex: 1;">
                        <h3>Ailments and Remedies</h3>
                        <p style="margin-bottom: 1.6rem;">Understand how herbal remedies support digestion, sleep, stress management, skin health, and immunity.</p>
                        <p style="margin-bottom: 1.6rem;"><a href="/ailments.html">See Herbal Remedies for Common Ailments</a></p>
                        <img src="/images/home/herbal-remedies-for-ailments.jpg" alt="Herbal remedies in jars and teas for common ailments like digestion, sleep, stress, and immunity">
                    </div>
                </div>
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
        {components.html_head(meta_title, meta_description)}
        <body class="home">
            {sections.header()}
            {html_hero}
            {html_section_1}
            {intro_html}
            {section_2_html}
            {section_3_html}
            {sections.footer()}
        </body>
        </html>
    '''
    html_filepath = f'''{g.website_folderpath}/index.html'''
    with open(html_filepath, 'w') as f: f.write(html)

