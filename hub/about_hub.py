from lib import g
from lib import components
from lib import sections

def gen():
    meta_title = f'''About Terra Whisper'''
    meta_description = f'''Learn about Terra Whisper, a growing directory dedicated to documenting medicinal herbs from around the world.'''
    html = f'''
        <!DOCTYPE html>
        <html lang="en">
        {components.html_head(meta_title, meta_description, css='/style.css')}
        <body class="article">
            {sections.header_default()}

            <body style="
            margin:0;
            font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;
            background:#fff;
            color:#222;
            line-height:1.7;
            ">

            <main style="
            max-width:900px;
            margin:auto;
            padding:60px 20px;
            ">

            <h1 style="
            font-size:42px;
            margin-bottom:20px;
            ">
            About Terra Whisper
            </h1>

            <p>

            Terra Whisper is an independent project dedicated to documenting
            medicinal herbs from around the world. Our goal is to create a
            comprehensive, well-organized reference covering medicinal plants,
            their botanical classification, traditional uses, preparation methods,
            safety information and scientific research.

            </p>

            <h2>Our Mission</h2>

            <p>

            We believe reliable information about medicinal plants should be easy
            to explore and understand. Terra Whisper aims to become a trusted
            knowledge base that organizes information into clear, structured herb
            profiles rather than scattered articles.

            </p>

            <h2>What You'll Find</h2>

            <ul>

            <li>Medicinal herb profiles</li>

            <li>Botanical taxonomy</li>

            <li>Common and scientific names</li>

            <li>Traditional uses across different cultures</li>

            <li>Preparation methods</li>

            <li>Safety information</li>

            <li>Scientific references when available</li>

            </ul>

            <h2>Our Approach</h2>

            <p>

            Each herb is documented using a consistent structure to make information
            easy to navigate and compare. As the directory grows, new herbs and
            additional references are continually added to expand the collection.

            </p>

            <h2>Editorial Principles</h2>

            <ul>

            <li>Accuracy over popularity.</li>

            <li>Clear distinction between traditional use and scientific evidence.</li>

            <li>Continuous review and improvement.</li>

            <li>Organized, structured information.</li>

            </ul>

            <h2>Disclaimer</h2>

            <p>

            The information published on Terra Whisper is provided for educational
            and informational purposes only. It is not intended to diagnose,
            treat, cure or prevent any disease and should not replace professional
            medical advice. Always consult a qualified healthcare professional
            before using medicinal herbs, especially if you are pregnant, nursing,
            taking medication or managing a medical condition.

            </p>

            </main>


            </body>
            </html>
            {sections.footer()}
        </body>
        </html>
    '''
    html_filepath = f'''{g.website_folderpath}/about-us.html'''
    with open(html_filepath, 'w') as f: f.write(html)

