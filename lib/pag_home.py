from lib import g
from lib import io
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
    
    meta_title = f'''TerraWhisper'''
    meta_description = f''''''
    html = f'''
        <!DOCTYPE html>
        <html lang="en">
        {components.html_head(meta_title, meta_description)}
        <body>
            {sections.header()}
            {hero_html}
            {sections.footer()}
        </body>
        </html>
    '''
    html_filepath = f'''{g.website_folderpath}/index.html'''
    with open(html_filepath, 'w') as f: f.write(html)

