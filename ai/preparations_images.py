import os

from lib import g
from lib import io
from lib import zimage

def image_ai(obj, clear=False):
    json_article_filepath = f'''{g.database_folderpath}/json/{obj['url']}.json'''
    json_article = io.json_read(json_article_filepath)
    preparation_slug = json_article['preparation_slug']
    preparation_name_singular = json_article['preparation_name_singular']
    preparation_name_plural = json_article['preparation_name_plural']
    preparation_list = json_article['preparations']
    for preparation_i, preparation in enumerate(preparation_list[:10]):
        herb_name_scientific = preparation['herb_name_scientific']
        herb_slug = herb_name_scientific.lower().strip().replace(' ', '-').replace('.', '')
        out_filepath = f'''{g.WEBSITE_FOLDERPATH}/images/preparations/{preparation_slug}/{herb_slug}-{preparation_slug}.jpg'''
        if clear:
            try: os.remove(out_filepath)
            except: pass
            continue
        # if not os.path.exists(out_filepath):
        if True:
            if 0:
                prompt = f'''
                    herbal {preparation_name_plural} made with dry {herb_name_scientific},
                    on a wooden table,
                    rustic, vintage, boho,
                    warm tones,
                    high resolution,
                '''.replace('  ', ' ')
            if preparation_name_plural == 'teas':
                prompt = f'''
                    a ceramic cup of {herb_name_scientific} tea on a wooden table surrounded by dry herbs,
                    rustic, vintage, boho,
                '''
            elif preparation_name_plural == 'tinctures':
                prompt = f'''
                    a dark amber glass dropper bottle of {herb_name_scientific} tincture on a wooden table surrounded by dry herbs,
                    rustic, vintage, boho,
        '''
            zimage.image_create(
                output_filepath=f'{out_filepath}', 
                prompt=prompt, width=768, height=768, seed=-1,
            )

def gen():
    ailment_list = io.csv_to_dict(f'{g.database_folderpath}/csv/ailments.csv')
    preparation_list = io.csv_to_dict(f'{g.database_folderpath}/csv/preparations.csv')
    for ailment_i, ailment in enumerate(ailment_list):
        ailment_slug = ailment['ailment_slug']
        ailment_name = ailment['ailment_name']
        organ_slug = ailment['organ_slug']
        system_slug = ailment['system_slug']
        print(f'AILMENT: {ailment_i}/{len(ailment_list)} - {ailment_name}')
        for preparation_i, preparation in enumerate(preparation_list):
            preparation_slug = preparation['preparation_slug']
            preparation_name_singular = preparation['preparation_name_singular']
            preparation_name_plural = preparation['preparation_name_plural']
            if preparation_slug != 'tinctures': continue
            print(f'PREPARATION: {preparation_slug}')
            try: os.mkdir(f'''{g.website_folderpath}/ailments''')
            except: pass
            try: os.mkdir(f'''{g.website_folderpath}/ailments/{ailment_slug}''')
            except: pass
            url = f'ailments/{ailment_slug}/{preparation_slug}'
            obj = {
                'url': url,
                'ailment_slug': ailment_slug,
                'ailment_name': ailment_name,
                'organ_slug': organ_slug,
                'system_slug': system_slug,
                'preparation_slug': preparation_slug,
                'preparation_name_singular': preparation_name_singular,
                'preparation_name_plural': preparation_name_plural,
            }
            image_ai(obj, clear=False)
            print(f'########################################')
            print(f'DONE')
            print(f'########################################')
            quit()

