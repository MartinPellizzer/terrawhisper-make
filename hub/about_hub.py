from lib import g
from lib import components
from lib import sections

def gen():
    html_article = f'''
    <section class="container-xl" style="margin-top: 9.6rem; margin-bottom: 9.6rem;">
        <div class="m-flex" style="gap: 6.4rem;">
            <div style="flex: 1;">
                <p>Dear Apothecary,</p>
                <p>Welcome to Terra Whisper.</p>
                <p>I write to you from a quiet place among the Alpine Mountains, where wind moves through stone corridors and old pine forests hold more memory than any library I have ever known. My name is Klaus Randell, and I am an apothecary by trade and by calling. For many years I have studied plants not only as medicine, but as language-living systems that speak through chemistry, tradition, and time.</p>
                <p>Terra Whisper was created as an attempt to gather that language into one place.</p>
                <p>This website exists as a living materia medica of more than 10,000 medicinal plants. It is not meant to replace traditional knowledge, nor to simplify it. Instead, it is an ever-growing archive designed to collect, compare, and preserve the widest possible range of herbal information available to us today. My goal is simple in intention, though vast in scope: to aggregate as much knowledge about herbs as can responsibly be gathered, across cultures, disciplines, and eras.</p>
                <p>To achieve this, Terra Whisper draws from sources across the open web. This includes ethnobotanical records, historical apothecary texts, and modern scientific literature such as PubMed, as well as global botanical institutions like Plants of the World Online. Each source is treated as a fragment of a larger mosaic rather than a final authority.</p>
                <p>Because of this diversity of input, every piece of information you find here is accompanied by a reliability score. This score reflects how consistent, well-supported, and cross-verified we consider the source material to be. It is important to understand that this score does not claim to define absolute truth. Instead, it indicates confidence based on evidence quality, consensus, and traceability. Herbal knowledge is often contextual, and certainty is rarely absolute.</p>
                <p>In time, I will publish a full editorial guideline explaining exactly how these scores are determined, including the criteria, weighting, and limitations involved. Transparency is essential to the integrity of this work, and I do not wish for Terra Whisper to become a black box of curated belief.</p>
                <p>This project is not finished, nor will it ever be. It is a growing field rather than a completed structure.</p>
                <p>If you are reading this, consider yourself part of its early soil.</p>
                <p>With respect from the mountains,<br>Klaus Randell</p>
            </div>
            <div style="flex: 1;">
                <img src="/images/about-us/klaus-randell.jpg">
            </div>
        </div>
    </section>
    '''

    meta_title = f'''About Us | Terra Whisper'''
    meta_description = f''''''
    html = f'''
        <!DOCTYPE html>
        <html lang="en">
        {components.html_head(meta_title, meta_description, css='/style.css')}
        <body class="article">
            {sections.header_default()}
            {html_article}
            {sections.footer()}
        </body>
        </html>
    '''
    html_filepath = f'''{g.website_folderpath}/about-us.html'''
    with open(html_filepath, 'w') as f: f.write(html)

