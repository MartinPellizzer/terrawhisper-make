from lib import g
from lib import io
from lib import data
from lib import polish
from lib import components
from lib import sections

def gen():
    html_main = f''
    opacity = 0.7
    hero_html = f'''
        <section class="home-hero" style="background-image: linear-gradient(to bottom, rgba(0, 0, 0, {opacity}), rgba(0, 0, 0, {opacity})), url(/images/home/medicinal-herbs.jpg); background-size: cover; background-position: center; padding-top: 9.6rem; padding-bottom: 9.6rem;">
            <div class="container-xl">
                <div style="display: flex">
                    <div style="flex: 2;">
                        <h1>Discover the Healing Power of Herbal Medicine<br><span>Backed by Tradition & Science</span></h1>
                        <p>Explore trusted, evidence-based guides on herbs, remedies, and natural practices. From ancient wisdom to modern research, we help you use plants safely and effectively for holistic wellness.</p>
                        <div style="display: flex; gap: 1.6rem;">
                            <div style="margin-top: 3.2rem;">
                                <a class="button-accent" href="/ailments.html">Explore Remedies</a>
                            </div>
                            <div style="margin-top: 3.2rem;">
                                <a class="button-ghost" href="/herbs.html">Learn About Herbs</a>
                            </div>
                        </div>
                    </div>
                    <div style="flex: 1;">
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

    herbs_popular = data.preparation_herbs_popular_100('teas')[:15]
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

    meta_title = f'''TerraWhisper'''
    meta_description = f''''''
    html = f'''
        <!DOCTYPE html>
        <html lang="en">
        {components.html_head(meta_title, meta_description)}
        <body class="home">
            {sections.header()}
            {hero_html}
            {intro_html}
            {section_2_html}
            {section_3_html}
            {sections.footer()}
        </body>
        </html>
    '''
    html_filepath = f'''{g.website_folderpath}/index.html'''
    with open(html_filepath, 'w') as f: f.write(html)

