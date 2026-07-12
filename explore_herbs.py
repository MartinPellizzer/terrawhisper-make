from lib import g
from lib import io
from lib import data
from lib import polish

from lib import sections
from lib import components

def herbs_index():
    html_article = ''
    html_article += f'''
        <h1 style="margin-top: 9.6rem;">
            Medicinal Herbs
        </h1>
    '''
    ###
    plants_rows = data.sqlite__plants_get()
    items_counter = 0
    num = 48
    cards = ''
    for plant_row in plants_rows[:num]:
        plant_name = plant_row[1]
        plant_slug = polish.sluggify(plant_name)
        plant_img_src = f'/images/herbs/{plant_slug}.jpg'
        plant_filepath = f'{g.WEBSITE_FOLDERPATH}/images/herbs/{plant_slug}.jpg'
        html_image = f'''
            <img src="{plant_img_src}" alt="{plant_name}" style="margin-bottom: 1.6rem;">
        '''
        cards += f'''
            <article>
                <a href="/herbs/{plant_slug}.html" style="text-decoration: none;">
                    {html_image}
                    <h3>{plant_name}</h3>
                </a>
            </article>
        '''
        items_counter += 1
        if items_counter >= num: break

    li_a_style = f'''text-decoration: none; color: #111; font-size: 1.4rem; display: inline-block;'''
    html_categories = f'''
        <div 
            style=" 
                background-color: #fff; 
                padding: 2.4rem;
box-shadow: rgba(0, 0, 0, 0.1) 0px 1px 2px 0px;
            "
        >
            <h2 style="font-size: 1.8rem; letter-spacing: 0.5px; margin-bottom: 3.2rem; padding-bottom: 0.8rem;
                border-bottom: 3px solid #111;
                display: inline-block;
            ">
                Categories
            </h2>
            <h3 style="font-size: 1.4rem; letter-spacing: 0.5px; margin-bottom: 1.4rem;">
                Explore Herbs
            </h3>
            <ul style="list-style: none; display: flex; flex-direction: column; gap: 0.4rem;">
                <li>
                    <a style="text-decoration: none; color: #111; font-size: 1.4rem;" href="/herbs.html">All Herbs</a>
                </li>
                <li>
                    <a style="text-decoration: none; color: #111; font-size: 1.4rem;" href="/herbs.html">Popular Herbs</a>
                </li>
                <li>
                    <a style="text-decoration: none; color: #111; font-size: 1.4rem;" href="/herbs.html">Recently Added</a>
                </li>
            </ul>
            <hr style="border: 0; border-bottom: 1px solid #d8d8d8; margin-top: 2.4rem; margin-bottom: 2.4rem;">

            <h3 style="font-size: 1.4rem; letter-spacing: 0.5px; margin-bottom: 1.4rem;">
                Alphabet
            </h3>
            <ul style="list-style: none; display: grid; grid-template-columns: repeat(5, 1fr);">
                <li>
                    <a style="{li_a_style}" href="/herbs/a.html">A</a>
                </li>
                <li>
                    <a style="{li_a_style}" href="/herbs/b.html">B</a>
                </li>
                <li>
                    <a style="{li_a_style}" href="/herbs/c.html">C</a>
                </li>
                <li>
                    <a style="{li_a_style}" href="/herbs/c.html">D</a>
                </li>
                <li>
                    <a style="{li_a_style}" href="/herbs/c.html">E</a>
                </li>
                <li>
                    <a style="{li_a_style}" href="/herbs/c.html">F</a>
                </li>
                <li>
                    <a style="{li_a_style}" href="/herbs/c.html">G</a>
                </li>
                <li>
                    <a style="{li_a_style}" href="/herbs/c.html">H</a>
                </li>
                <li>
                    <a style="{li_a_style}" href="/herbs/c.html">I</a>
                </li>
                <li>
                    <a style="{li_a_style}" href="/herbs/c.html">J</a>
                </li>
                <li>
                    <a style="{li_a_style}" href="/herbs/c.html">K</a>
                </li>
                <li>
                    <a style="{li_a_style}" href="/herbs/c.html">L</a>
                </li>
                <li>
                    <a style="{li_a_style}" href="/herbs/c.html">M</a>
                </li>
                <li>
                    <a style="{li_a_style}" href="/herbs/c.html">N</a>
                </li>
                <li>
                    <a style="{li_a_style}" href="/herbs/c.html">O</a>
                </li>
                <li>
                    <a style="{li_a_style}" href="/herbs/c.html">P</a>
                </li>
                <li>
                    <a style="{li_a_style}" href="/herbs/c.html">Q</a>
                </li>
                <li>
                    <a style="{li_a_style}" href="/herbs/c.html">R</a>
                </li>
                <li>
                    <a style="{li_a_style}" href="/herbs/c.html">S</a>
                </li>
                <li>
                    <a style="{li_a_style}" href="/herbs/c.html">T</a>
                </li>
                <li>
                    <a style="{li_a_style}" href="/herbs/c.html">U</a>
                </li>
                <li>
                    <a style="{li_a_style}" href="/herbs/c.html">V</a>
                </li>
                <li>
                    <a style="{li_a_style}" href="/herbs/c.html">W</a>
                </li>
                <li>
                    <a style="{li_a_style}" href="/herbs/c.html">X</a>
                </li>
                <li>
                    <a style="{li_a_style}" href="/herbs/c.html">Y</a>
                </li>
                <li>
                    <a style="{li_a_style}" href="/herbs/c.html">Z</a>
                </li>
            </ul>
            <hr style="border: 0; border-bottom: 1px solid #d8d8d8; margin-top: 2.4rem; margin-bottom: 2.4rem;">

            <h3 style="font-size: 1.4rem; letter-spacing: 0.5px; margin-bottom: 1.4rem;">
                Biological Activity
            </h3>
            <ul style="list-style: none; display: flex; flex-direction: column; gap: 0.4rem;">
                <li>
                    <a style="{li_a_style}" href="/herbs.html">Anti-inflammatory</a>
                </li>
                <li>
                    <a style="{li_a_style}" href="/herbs.html">Antioxidant</a>
                </li>
                <li>
                    <a style="{li_a_style}" href="/herbs.html">Antimicrobial</a>
                </li>
                <li>
                    <a style="{li_a_style}" href="/herbs.html">Antiviral</a>
                </li>
                <li>
                    <a style="{li_a_style}" href="/herbs.html">Antifungal</a>
                </li>
                <li>
                    <a style="{li_a_style}" href="/herbs.html">Adaptogenic</a>
                </li>
                <li>
                    <a style="{li_a_style}" href="/herbs.html">Neuroprotective</a>
                </li>
                <li>
                    <a style="{li_a_style}" href="/herbs.html">Cardioprotective</a>
                </li>
                <li>
                    <a style="{li_a_style}" href="/herbs.html">Hepatoprotective</a>
                </li>
            </ul>
            <a style="{li_a_style} margin-top: 1.6rem;" href="/herbs.html">View all →</a>
            <hr style="border: 0; border-bottom: 1px solid #d8d8d8; margin-top: 2.4rem; margin-bottom: 2.4rem;">

            <h3 style="font-size: 1.4rem; letter-spacing: 0.5px; margin-bottom: 1.4rem;">
                Bioactive Compounds
            </h3>
            <ul style="list-style: none; display: flex; flex-direction: column; gap: 0.4rem;">
                <li>
                    <a style="{li_a_style}" href="/herbs.html">Alkaoids</a>
                </li>
                <li>
                    <a style="{li_a_style}" href="/herbs.html">Flavonoids</a>
                </li>
                <li>
                    <a style="{li_a_style}" href="/herbs.html">Terpenes</a>
                </li>
                <li>
                    <a style="{li_a_style}" href="/herbs.html">Polyphenols</a>
                </li>
                <li>
                    <a style="{li_a_style}" href="/herbs.html">Saponins</a>
                </li>
                <li>
                    <a style="{li_a_style}" href="/herbs.html">Essential Oils</a>
                </li>
                <li>
                    <a style="{li_a_style}" href="/herbs.html">Tannins</a>
                </li>
            </ul>
            <a style="{li_a_style} margin-top: 1.6rem;" href="/herbs.html">View all →</a>
            <hr style="border: 0; border-bottom: 1px solid #d8d8d8; margin-top: 2.4rem; margin-bottom: 2.4rem;">

            <h3 style="font-size: 1.4rem; letter-spacing: 0.5px; margin-bottom: 1.4rem;">
                Body Systems
            </h3>
            <ul style="list-style: none; display: flex; flex-direction: column; gap: 0.4rem;">
                <li>
                    <a style="{li_a_style}" href="/herbs.html">Digestive</a>
                </li>
                <li>
                    <a style="{li_a_style}" href="/herbs.html">Immune</a>
                </li>
                <li>
                    <a style="{li_a_style}" href="/herbs.html">Nervous</a>
                </li>
                <li>
                    <a style="{li_a_style}" href="/herbs.html">Respiratory</a>
                </li>
                <li>
                    <a style="{li_a_style}" href="/herbs.html">Cardiovascular</a>
                </li>
                <li>
                    <a style="{li_a_style}" href="/herbs.html">Skin</a>
                </li>
                <li>
                    <a style="{li_a_style}" href="/herbs.html">Urinary</a>
                </li>
                <li>
                    <a style="{li_a_style}" href="/herbs.html">Musculoskeletal</a>
                </li>
            </ul>
            <a style="{li_a_style} margin-top: 1.6rem;" href="/herbs.html">View all →</a>
            <hr style="border: 0; border-bottom: 1px solid #d8d8d8; margin-top: 2.4rem; margin-bottom: 2.4rem;">

            <h3 style="font-size: 1.4rem; letter-spacing: 0.5px; margin-bottom: 1.4rem;">
                Plant Parts
            </h3>
            <ul style="list-style: none; display: flex; flex-direction: column; gap: 0.4rem;">
                <li>
                    <a style="{li_a_style}" href="/herbs.html">Root</a>
                </li>
                <li>
                    <a style="{li_a_style}" href="/herbs.html">Leaf</a>
                </li>
                <li>
                    <a style="{li_a_style}" href="/herbs.html">Flower</a>
                </li>
                <li>
                    <a style="{li_a_style}" href="/herbs.html">Seed</a>
                </li>
                <li>
                    <a style="{li_a_style}" href="/herbs.html">Fruit</a>
                </li>
                <li>
                    <a style="{li_a_style}" href="/herbs.html">Bark</a>
                </li>
                <li>
                    <a style="{li_a_style}" href="/herbs.html">Rhizome</a>
                </li>
                <li>
                    <a style="{li_a_style}" href="/herbs.html">Whole Plant</a>
                </li>
            </ul>
            <a style="{li_a_style} margin-top: 1.6rem;" href="/herbs.html">View all →</a>
            <hr style="border: 0; border-bottom: 1px solid #d8d8d8; margin-top: 2.4rem; margin-bottom: 2.4rem;">

            <h3 style="font-size: 1.4rem; letter-spacing: 0.5px; margin-bottom: 1.4rem;">
                Botanical Families
            </h3>
            <ul style="list-style: none; display: flex; flex-direction: column; gap: 0.4rem;">
                <li>
                    <a style="{li_a_style}" href="/herbs.html">Lamiaceae</a>
                </li>
                <li>
                    <a style="{li_a_style}" href="/herbs.html">Asteraceae</a>
                </li>
                <li>
                    <a style="{li_a_style}" href="/herbs.html">Fabaceae</a>
                </li>
                <li>
                    <a style="{li_a_style}" href="/herbs.html">Apiaceae</a>
                </li>
                <li>
                    <a style="{li_a_style}" href="/herbs.html">Rosaceae</a>
                </li>
                <li>
                    <a style="{li_a_style}" href="/herbs.html">Rutaceae</a>
                </li>
            </ul>
            <a style="{li_a_style} margin-top: 1.6rem;" href="/herbs.html">View all →</a>
            <hr style="border: 0; border-bottom: 1px solid #d8d8d8; margin-top: 2.4rem; margin-bottom: 2.4rem;">

            <h3 style="font-size: 1.4rem; letter-spacing: 0.5px; margin-bottom: 1.4rem;">
                Geographic Origin
            </h3>
            <ul style="list-style: none; display: flex; flex-direction: column; gap: 0.4rem;">
                <li>
                    <a style="{li_a_style}" href="/herbs.html">Europe</a>
                </li>
                <li>
                    <a style="{li_a_style}" href="/herbs.html">Asia</a>
                </li>
                <li>
                    <a style="{li_a_style}" href="/herbs.html">Africa</a>
                </li>
                <li>
                    <a style="{li_a_style}" href="/herbs.html">North America</a>
                </li>
                <li>
                    <a style="{li_a_style}" href="/herbs.html">South America</a>
                </li>
                <li>
                    <a style="{li_a_style}" href="/herbs.html">Oceania</a>
                </li>
            </ul>
            <a style="{li_a_style} margin-top: 1.6rem;" href="/herbs.html">View all →</a>
            <hr style="border: 0; border-bottom: 1px solid #d8d8d8; margin-top: 2.4rem; margin-bottom: 2.4rem;">

            <h3 style="font-size: 1.4rem; letter-spacing: 0.5px; margin-bottom: 1.4rem;">
                Traditional Medicine
            </h3>
            <ul style="list-style: none; display: flex; flex-direction: column; gap: 0.4rem;">
                <li>
                    <a style="{li_a_style}" href="/herbs.html">Ayurveda</a>
                </li>
                <li>
                    <a style="{li_a_style}" href="/herbs.html">Traditional Chinese Medicine</a>
                </li>
                <li>
                    <a style="{li_a_style}" href="/herbs.html">Western Herbalism</a>
                </li>
                <li>
                    <a style="{li_a_style}" href="/herbs.html">Unani</a>
                </li>
                <li>
                    <a style="{li_a_style}" href="/herbs.html">Native America</a>
                </li>
                <li>
                    <a style="{li_a_style}" href="/herbs.html">African Traditional Medicine</a>
                </li>
            </ul>
            <a style="{li_a_style} margin-top: 1.6rem;" href="/herbs.html">View all →</a>
            <hr style="border: 0; border-bottom: 1px solid #d8d8d8; margin-top: 2.4rem; margin-bottom: 2.4rem;">

        </div>
    '''

    html_article += f'''
        <section style="margin-bottom: 9.6rem;">
            <div class="m-flex" style="gap: 3.2rem;">
                <div style="flex: 1;">
                    {html_categories}
                </div>
                <div style="flex: 3;">
                    <h2>
                        Discover all herbs
                    </h2>
                    <div class="grid-4" style="gap: 1.6rem; row-gap: 3.2rem;">
                        {cards}
                    </div>
                </div>
            </div>
        </section>
    '''

    ###
    url_slug = 'herbs'
    meta_title = f'Medicinal Herbs'
    meta_description = ''
    canonical_html = f'''<link rel="canonical" href="https://terrawhisper.com/{url_slug}.html">'''
    head_html = components.html_head(
        meta_title, meta_description, css='/styles.css', canonical=canonical_html
    )
    html = f''' 
        <!DOCTYPE html>
        <html lang="en">
        {head_html}
        <body style="background-color: #f4f4f4;">
            {sections.header_default()}
            {sections.breadcrumbs_new(url_slug)}
            <main class="container-xl">
                {html_article}
            </main>
            {sections.footer()}
        </body>
        </html>
    '''.strip()
    html_filepath = f'''{g.website_folderpath}/{url_slug}.html'''
    with open(html_filepath, 'w') as f: f.write(html)
    print(html_filepath)

def run():
    print(f'EXPLORE >> herbs')
    herbs_index()
