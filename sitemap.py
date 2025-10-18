import os

import g
import util
import util_data
import data_csv

from lib import g
from lib import io
from lib import data


'''
status_rows, status_cols = data_csv.status()
herbs_rows, herbs_cols = data_csv.herbs()

conditions_rows = util.csv_get_rows(g.CSV_CONDITIONS_FILEPATH)
conditions_cols = util.csv_get_cols(conditions_rows)
conditions_rows = conditions_rows[1:]
# print(conditions_rows)

systems_rows = util.csv_get_rows(g.CSV_SYSTEMS_NEW_FILEPATH)
systems_cols = util.csv_get_cols(systems_rows)
systems_rows = systems_rows[1:]
'''

def csv_get_system_by_problem(problem_id):
    system_row = []

    problems_systems_rows_filtered = util.csv_get_rows_filtered(
        g.CSV_PROBLEMS_SYSTEMS_FILEPATH, problems_systems_cols['problem_id'], problem_id,
    )

    if problems_systems_rows_filtered != []:
        problem_system_row = problems_systems_rows_filtered[0]
        system_id = problem_system_row[problems_systems_cols['system_id']]

        systems_rows_filtered = util.csv_get_rows_filtered(
            g.CSV_SYSTEMS_FILEPATH, systems_cols['system_id'], system_id,
        )

        if systems_rows_filtered != []:
            system_row = systems_rows_filtered[0]

    return system_row






def sitemap_remedies_systems():
    urls = ''
    for system_row in systems_rows:
        system_id = system_row[systems_cols['system_id']]
        system_slug = system_row[systems_cols['system_slug']]
        system_name = system_row[systems_cols['system_name']]

        if system_id == '': continue
        if system_slug == '': continue
        if system_name == '': continue

        json_filepath = f'database/json/{g.CATEGORY_REMEDIES}/{system_slug}.json'
        
        if os.path.exists(json_filepath):
            data = util.json_read(json_filepath)
            lastmod = data['lastmod']
            
            html_filepath = f'https://terrawhisper.com/remedies/{system_slug}.html'
            urls += f'''
<url>
  <loc>{html_filepath}</loc>
  <lastmod>{lastmod}</lastmod>
</url>
'''.strip() + '\n'

    return urls



def sitemap_remedies_systems_problems():
    urls = ''
    for problem_row in problems_rows[:g.ART_NUM]:
        problem_id = problem_row[problems_cols['problem_id']]
        problem_slug = problem_row[problems_cols['problem_slug']]
        problem_name = problem_row[problems_cols['problem_names']].split(',')[0].strip()

        if problem_id == '': continue
        if problem_slug == '': continue
        if problem_name == '': continue

        print(f'> {problem_name}')

        system_row = csv_get_system_by_problem(problem_id)
        system_id = system_row[systems_cols['system_id']]
        system_slug = system_row[systems_cols['system_slug']]
        system_name = system_row[systems_cols['system_name']]

        if system_id == '': continue
        if system_slug == '': continue
        if system_name == '': continue

        print(f'  > {system_name}')
        
        json_filepath = f'database/json/{g.CATEGORY_REMEDIES}/{system_slug}/{problem_slug}.json'
        if os.path.exists(json_filepath):
            data = util.json_read(json_filepath)
            lastmod = data['lastmod']
            
            html_filepath = f'https://terrawhisper.com/remedies/{system_slug}/{problem_slug}.html'
            urls += f'''
<url>
  <loc>{html_filepath}</loc>
  <lastmod>{lastmod}</lastmod>
</url>
'''.strip() + '\n'

        json_filepath = f'database/json/{g.CATEGORY_REMEDIES}/{system_slug}/{problem_slug}/teas.json'
        if os.path.exists(json_filepath):
            data = util.json_read(json_filepath)
            lastmod = data['lastmod']
            
            html_filepath = f'https://terrawhisper.com/remedies/{system_slug}/{problem_slug}/teas.html'
            urls += f'''
<url>
  <loc>{html_filepath}</loc>
  <lastmod>{lastmod}</lastmod>
</url>
'''.strip() + '\n'

        json_filepath = f'database/json/{g.CATEGORY_REMEDIES}/{system_slug}/{problem_slug}/tinctures.json'
        if os.path.exists(json_filepath):
            data = util.json_read(json_filepath)
            lastmod = data['lastmod']
            
            html_filepath = f'https://terrawhisper.com/remedies/{system_slug}/{problem_slug}/tinctures.html'
            urls += f'''
<url>
  <loc>{html_filepath}</loc>
  <lastmod>{lastmod}</lastmod>
</url>
'''.strip() + '\n'

    return urls



def sitemap_main():
    urls = ''
    urls += f'''
<url>
  <loc>https://terrawhisper.com/</loc>
  <lastmod>2024-03-17</lastmod>
</url>
'''.strip() + '\n'
    urls += f'''
<url>
  <loc>https://terrawhisper.com/remedies.html</loc>
  <lastmod>2024-03-17</lastmod>
</url>
'''.strip() + '\n'
    urls += f'''
<url>
  <loc>https://terrawhisper.com/herbs.html</loc>
  <lastmod>2024-03-17</lastmod>
</url>
'''.strip() + '\n'

    return urls


def sitemap_herbs():
    urls = ''
    for herb_row in herbs_rows:
        herb_id = herb_row[herbs_cols['herb_id']].strip()
        herb_slug = herb_row[herbs_cols['herb_slug']].strip()
        herb_name_scientific = herb_row[herbs_cols['herb_name_scientific']].strip()
        if herb_id == '': continue
        if herb_slug == '': continue
        if herb_name_scientific == '': continue
        data = util.json_read(f'database/json/herbs/{herb_slug}.json')
        lastmod = data['lastmod']
        filepath_out = f'website/herbs/{herb_slug}.html'
        filepath_web = f'https://terrawhisper.com/herbs/{herb_slug}.html'
        if os.path.exists(filepath_out):
            urls += f'''
<url>
  <loc>{filepath_web}</loc>
  <lastmod>{lastmod}</lastmod>
</url>
            '''.strip() + '\n'
        data = util.json_read(f'database/json/herbs/{herb_slug}/medicine.json')
        lastmod = data['lastmod']
        filepath_out = f'website/herbs/{herb_slug}/medicine.html'
        filepath_web = f'https://terrawhisper.com/herbs/{herb_slug}/medicine.html'
        if os.path.exists(filepath_out):
            urls += f'''
<url>
  <loc>{filepath_web}</loc>
  <lastmod>{lastmod}</lastmod>
</url>
            '''.strip() + '\n'
        data = util.json_read(f'database/json/herbs/{herb_slug}/medicine/benefits.json')
        lastmod = data['lastmod']
        filepath_out = f'website/herbs/{herb_slug}/medicine/benefits.html'
        filepath_web = f'https://terrawhisper.com/herbs/{herb_slug}/medicine/benefits.html'
        if os.path.exists(filepath_out):
            urls += f'''
<url>
  <loc>{filepath_web}</loc>
  <lastmod>{lastmod}</lastmod>
</url>
            '''.strip() + '\n'
        data = util.json_read(f'database/json/herbs/{herb_slug}/medicine/constituents.json')
        lastmod = data['lastmod']
        filepath_out = f'website/herbs/{herb_slug}/medicine/constituents.html'
        filepath_web = f'https://terrawhisper.com/herbs/{herb_slug}/medicine/constituents.html'
        if os.path.exists(filepath_out):
            urls += f'''
<url>
  <loc>{filepath_web}</loc>
  <lastmod>{lastmod}</lastmod>
</url>
            '''.strip() + '\n'
        data = util.json_read(f'database/json/herbs/{herb_slug}/medicine/preparations.json')
        lastmod = data['lastmod']
        filepath_out = f'website/herbs/{herb_slug}/medicine/preparations.html'
        filepath_web = f'https://terrawhisper.com/herbs/{herb_slug}/medicine/preparations.html'
        if os.path.exists(filepath_out):
            urls += f'''
<url>
  <loc>{filepath_web}</loc>
  <lastmod>{lastmod}</lastmod>
</url>
            '''.strip() + '\n'
        data = util.json_read(f'database/json/herbs/{herb_slug}/medicine/side-effects.json')
        lastmod = data['lastmod']
        filepath_out = f'website/herbs/{herb_slug}/medicine/side-effects.html'
        filepath_web = f'https://terrawhisper.com/herbs/{herb_slug}/medicine/side-effects.html'
        if os.path.exists(filepath_out):
            urls += f'''
<url>
  <loc>{filepath_web}</loc>
  <lastmod>{lastmod}</lastmod>
</url>
            '''.strip() + '\n'
        try: 
            data = util.json_read(f'database/json/herbs/{herb_slug}/medicine/precautions.json')
            lastmod = data['lastmod']
            filepath_out = f'website/herbs/{herb_slug}/medicine/precautions.html'
            filepath_web = f'https://terrawhisper.com/herbs/{herb_slug}/medicine/precautions.html'
            if os.path.exists(filepath_out):
                urls += f'''
<url>
  <loc>{filepath_web}</loc>
  <lastmod>{lastmod}</lastmod>
</url>
                '''.strip() + '\n'
        except: pass
    return urls

def sitemap_status():
    urls = ''
    for status_row in status_rows:
        status_exe = status_row[status_cols['status_exe']]
        status_id = status_row[status_cols['status_id']]
        status_slug = status_row[status_cols['status_slug']]
        status_name = status_row[status_cols['status_names']].split(',')[0].strip()
        if status_exe == '': continue
        if status_id == '': continue
        if status_slug == '': continue
        if status_name == '': continue
        system_row = util_data.get_system_by_status(status_id)
        system_id = system_row[systems_cols['system_id']]
        system_slug = system_row[systems_cols['system_slug']]
        system_name = system_row[systems_cols['system_name']]
        if system_id == '': continue
        if system_slug == '': continue
        if system_name == '': continue
        filepath_slug = f'remedies/{system_slug}/{status_slug}'
        filepath_out = f'website/{filepath_slug}.html'
        filepath_web = f'https://terrawhisper.com/{filepath_slug}.html'
        data = util.json_read(f'database/json/{filepath_slug}.json')
        lastmod = data['lastmod']
        if os.path.exists(filepath_out):
            urls += f'''
<url>
  <loc>{filepath_web}</loc>
  <lastmod>{lastmod}</lastmod>
</url>
            '''.strip() + '\n'
    return urls
        

    
def test_sitemap():
    sitemap_content = util.file_read('sitemap.xml')
    lines = sitemap_content.split('\n')
    for line in lines:
        if '<loc>' in line:
            line = line.replace('<loc>', '').replace('</loc>', '').strip()
            line = line.replace('https://terrawhisper.com', 'website')
            if not os.path.exists:
                print(f'missing: {line}')

def sitemap_all():
    sitemap = ''
    sitemap += '<?xml version="1.0" encoding="UTF-8"?>\n'
    sitemap += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    sitemap += sitemap_main()
    sitemap += sitemap_status()
    # sitemap += sitemap_remedies_systems_problems()
    # sitemap += sitemap_plants()
    sitemap += sitemap_herbs()
    sitemap += '</urlset>\n'
    util.file_write('sitemap.xml', sitemap.strip())

def sitemap_cat_preparations():
    sitemap = ''
    category_slug = 'preparations'
    url_relative = f'{category_slug}'
    json_article_filepath = f'database/json/{url_relative}.json'
    json_article = io.json_read(json_article_filepath)
    filepath_web = f'https://terrawhisper.com/{category_slug}.html'
    lastmod = json_article['lastmod']
    sitemap += f'''
<url>
<loc>{filepath_web}</loc>
</url>
    '''.strip() + '\n'
    return sitemap

def sitemap_art_preparations():
    sitemap = ''
    category_slug = 'preparations'
    preparations_list = io.csv_to_dict(f'database/entities/preparations.csv')
    for preparation_i, preparation in enumerate(preparations_list):
        preparation_slug = preparation['entity_slug']
        url_relative = f'{category_slug}/{preparation_slug}'
        json_article_filepath = f'database/json/{url_relative}.json'
        json_article = io.json_read(json_article_filepath)
        filepath_web = f'https://terrawhisper.com/{category_slug}/{preparation_slug}.html'
        lastmod = json_article['lastmod']
        sitemap += f'''
<url>
<loc>{filepath_web}</loc>
</url>
    '''.strip() + '\n'
    return sitemap

def sitemap_art_preparations_best():
    sitemap = ''
    category_slug = 'preparations'
    preparations_list = io.csv_to_dict(f'database/entities/preparations.csv')
    for preparation_i, preparation in enumerate(preparations_list):
        preparation_slug = preparation['entity_slug']
        url_relative = f'{category_slug}/{preparation_slug}/best'
        json_article_filepath = f'database/json/{url_relative}.json'
        json_article = io.json_read(json_article_filepath)
        filepath_web = f'https://terrawhisper.com/{url_relative}.html'
        lastmod = json_article['lastmod']
        sitemap += f'''
<url>
<loc>{filepath_web}</loc>
</url>
    '''.strip() + '\n'
    return sitemap

def sitemap_art_preparations_herbs():
    sitemap = ''
    category_slug = 'preparations'
    preparation_list = io.csv_to_dict(f'database/entities/preparations.csv')
    for preparation_i, preparation in enumerate(preparation_list):
        print(f'{preparation_i}/{len(preparation_list)} - {preparation}')
        preparation_slug = preparation['entity_slug']
        preparation_name_singular = preparation['entity_name_singular']
        preparation_name_plural = preparation['entity_name_plural']
        ###
        if not os.path.exists(f'{g.WEBSITE_FOLDERPATH}/{category_slug}/{preparation_slug}'): 
            os.mkdir(f'{g.WEBSITE_FOLDERPATH}/{category_slug}/{preparation_slug}')
        ###
        herb_list = data.preparations_popular_100_get(preparation_slug)
        for herb in herb_list:
            herb_slug = herb['herb_slug']
            herb_name_scientific = herb['herb_name_scientific']
            url_relative = f'{category_slug}/{preparation_slug}/{herb_slug}'
            json_article_filepath = f'database/json/{url_relative}.json'
            json_article = io.json_read(json_article_filepath)
            filepath_web = f'https://terrawhisper.com/{url_relative}.html'
            lastmod = json_article['lastmod']
            sitemap += f'''
<url>
<loc>{filepath_web}</loc>
</url>
    '''.strip() + '\n'
    return sitemap

def sitemap_preparations_gen():
    sitemap = ''
    sitemap += '<?xml version="1.0" encoding="UTF-8"?>\n'
    sitemap += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    sitemap += sitemap_cat_preparations()
    sitemap += sitemap_art_preparations()
    sitemap += sitemap_art_preparations_best()
    sitemap += sitemap_art_preparations_herbs()
    sitemap += '</urlset>\n'
    util.file_write('sitemap-preparations.xml', sitemap.strip())
    util.file_write(f'{g.WEBSITE_FOLDERPATH}/sitemap-preparations.xml', sitemap.strip())

def sitemap_cat_ailments():
    sitemap = ''
    category_slug = 'ailments'
    url_relative = f'{category_slug}'
    filepath_web = f'https://terrawhisper.com/{category_slug}.html'
    sitemap += f'''
<url>
<loc>{filepath_web}</loc>
</url>
    '''.strip() + '\n'
    return sitemap

def sitemap_art_ailments():
    sitemap = ''
    category_slug = 'ailments'
    ailment_list = io.csv_to_dict('systems-organs-ailments.csv')
    for ailment_i, ailment in enumerate(ailment_list):
        ailment_slug = ailment['ailment_slug']
        url_relative = f'{category_slug}/{ailment_slug}'
        filepath_web = f'https://terrawhisper.com/{category_slug}/{ailment_slug}.html'
        sitemap += f'''
<url>
<loc>{filepath_web}</loc>
</url>
    '''.strip() + '\n'
    return sitemap

def sitemap_art_ailments_preparations():
    sitemap = ''
    category_slug = 'ailments'
    ailment_list_foldername = f'{g.WEBSITE_FOLDERPATH}/{category_slug}'
    for ailment_foldername in os.listdir(f'{ailment_list_foldername}'):
        ailment_folderpath = f'{ailment_list_foldername}/{ailment_foldername}'
        if os.path.isdir(ailment_folderpath):
            preparation_list_filename = os.listdir(f'{ailment_folderpath}')
            for preparation_filename in preparation_list_filename:
                ailment_preparation_filepath = f'{ailment_folderpath}/{preparation_filename}'
                filepath_web = f'https://terrawhisper.com/{category_slug}/{ailment_foldername}/{preparation_filename}'
                sitemap += f'''
        <url>
        <loc>{filepath_web}</loc>
        </url>
            '''.strip() + '\n'
    return sitemap

def sitemap_ailments_gen():
    sitemap = ''
    sitemap += '<?xml version="1.0" encoding="UTF-8"?>\n'
    sitemap += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    sitemap += sitemap_cat_ailments()
    sitemap += sitemap_art_ailments()
    sitemap += sitemap_art_ailments_preparations()
    sitemap += '</urlset>\n'
    util.file_write('sitemap-ailments.xml', sitemap.strip())
    util.file_write(f'{g.WEBSITE_FOLDERPATH}/sitemap-ailments.xml', sitemap.strip())

# sitemap_all()
# sitemap_preparations_gen()
sitemap_ailments_gen()

