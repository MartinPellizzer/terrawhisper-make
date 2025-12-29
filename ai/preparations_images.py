import os

from lib import g
from lib import io
from lib import data
from lib import zimage

ailments_rows = io.csv_to_dict(f'{g.database_folderpath}/csv/ailments.csv')
preparations_rows = io.csv_to_dict(f'{g.database_folderpath}/csv/preparations.csv')

def image_ai(obj, clear=False):
    json_article_filepath = f'''{g.database_folderpath}/json/{obj['url']}.json'''
    json_article = io.json_read(json_article_filepath)
    preparation_slug = json_article['preparation_slug']
    preparation_name_singular = json_article['preparation_name_singular']
    preparation_name_plural = json_article['preparation_name_plural']
    preparations_rows = json_article['preparations']
    for preparation_i, preparation in enumerate(preparations_rows[:10]):
        herb_name_scientific = preparation['herb_name_scientific']
        herb_slug = herb_name_scientific.lower().strip().replace(' ', '-').replace('.', '')
        output_folderpath = f'''{g.WEBSITE_FOLDERPATH}/images/preparations/{preparation_slug}'''
        out_filepath = f'''{output_folderpath}/{herb_slug}-{preparation_slug}.jpg'''
        if clear:
            try: os.remove(out_filepath)
            except: pass
            continue
        try: os.makedirs(output_folderpath)
        except: pass
        if not os.path.exists(out_filepath):
        # if True:
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
            elif preparation_name_plural == 'decoctions':
                prompt = f'''
                    a pot of herbal decoction on a wooden table surrounded by dry herbs,
                    rustic, vintage, boho,
                '''
            elif preparation_name_plural == 'essential oils':
                prompt = f'''
                    an amber glass bottle with black cap of {herb_name_scientific} essential oil on a wooden table surrounded by dry herbs,
                    rustic, vintage, boho,
                '''
            elif preparation_name_plural == 'creams':
                prompt = f'''
                    a glass jar of {herb_name_scientific} cream on a wooden table surrounded by dry herbs,
                    rustic, vintage, boho,
                '''
            elif preparation_name_plural == 'juices':
                prompt = f'''
                    a glass bottle of {herb_name_scientific} juice on a wooden table surrounded by dry herbs,
                    rustic, vintage, boho,
                '''
            elif preparation_name_plural == 'syrups':
                prompt = f'''
                    a glass bottle of {herb_name_scientific} syrup on a wooden table surrounded by dry herbs,
                    rustic, vintage, boho,
                '''
            elif preparation_name_plural == 'linctuses':
                prompt = f'''
                    herbal linctuses on a wooden table surrounded by dry herbs,
                    rustic, vintage, boho,
                '''
            elif preparation_name_plural == 'mucillages':
                prompt = f'''
                    herbal mucillages on a wooden table surrounded by dry herbs,
                    rustic, vintage, boho,
                '''
            elif preparation_name_plural == 'capsules':
                prompt = f'''
                    a pile of {herb_name_scientific} herbal capsules on a wooden table surrounded by dry herbs,
                    rustic, vintage, boho,
                '''
            elif preparation_name_plural == 'lozenges':
                prompt = f'''
                    herbal lozenges on a wooden table surrounded by dry herbs,
                    rustic, vintage, boho,
                '''
            elif preparation_name_plural == 'baths':
                prompt = f'''
                    a bathtub full of water and dry {herb_name_scientific} herbs,
                    rustic, vintage, boho,
                '''
            elif preparation_name_plural == 'lotions':
                prompt = f'''
                    herbal lotions on a wooden table surrounded by dry herbs,
                    rustic, vintage, boho,
                '''
            zimage.image_create(
                output_filepath=f'{out_filepath}', 
                prompt=prompt, width=768, height=768, seed=-1,
            )

########################################
# generate images for:
# >> terrawhisper/ailments/[ailment]/[preparation].html
########################################
def ailments_preparations_gen(ailments_rows, preparations_rows):
    for ailment_i, ailment in enumerate(ailments_rows):
        ailment_slug = ailment['ailment_slug']
        ailment_name = ailment['ailment_name']
        organ_slug = ailment['organ_slug']
        system_slug = ailment['system_slug']
        print(f'AILMENT: {ailment_i}/{len(ailments_rows)} - {ailment_name}')
        for preparation_i, preparation in enumerate(preparations_rows):
            preparation_slug = preparation['preparation_slug']
            preparation_name_singular = preparation['preparation_name_singular']
            preparation_name_plural = preparation['preparation_name_plural']
            # if preparation_slug != 'teas': continue
            # if preparation_slug != 'tinctures': continue
            # if preparation_slug != 'decoctions': continue
            # if preparation_slug != 'essential-oils': continue

            # if preparation_slug != 'creams': continue
            # if preparation_slug != 'syrups': continue
            # if preparation_slug != 'juices': continue
            # if preparation_slug != 'linctuses': continue

            # if preparation_slug != 'mucillages': continue
            # if preparation_slug != 'capsules': continue
            # if preparation_slug != 'lozenges': continue
            # if preparation_slug != 'baths': continue

            if preparation_slug != 'lotions': continue
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

########################################
# generate images for:
# >> terrawhisper/preparations.html
########################################
def preparations_gen(preparations_rows):
    for preparation_i, preparation in enumerate(preparations_rows):
        preparation_slug = preparation['preparation_slug']
        preparation_name_singular = preparation['preparation_name_singular']
        preparation_name_plural = preparation['preparation_name_plural']
        print(f'PREPARATION: {preparation_slug}')
        output_folderpath = f'''{g.WEBSITE_FOLDERPATH}/images/preparations/'''
        out_filepath = f'''{output_folderpath}/herbal-{preparation_slug}.jpg'''
        try: os.makedirs(output_folderpath)
        except: pass
        if not os.path.exists(out_filepath):
        # if True:
            if preparation_name_plural == 'teas':
                prompt = f'''
                    a ceramic cup of herbal tea on a wooden table surrounded by dry herbs,
                    rustic, vintage, boho,
                '''
            elif preparation_name_plural == 'tinctures':
                prompt = f'''
                    a dark amber glass dropper bottle of herbal tincture on a wooden table surrounded by dry herbs,
                    rustic, vintage, boho,
                '''
            elif preparation_name_plural == 'decoctions':
                prompt = f'''
                    a pot of herbal decoction on a wooden table surrounded by dry herbs,
                    rustic, vintage, boho,
                '''
            elif preparation_name_plural == 'essential oils':
                prompt = f'''
                    an amber glass bottle with black cap of herbal essential oil on a wooden table surrounded by dry herbs,
                    rustic, vintage, boho,
                '''
            elif preparation_name_plural == 'creams':
                prompt = f'''
                    a glass jar of herbal cream on a wooden table surrounded by dry herbs,
                    rustic, vintage, boho,
                '''
            elif preparation_name_plural == 'juices':
                prompt = f'''
                    a glass bottle of herbal juice on a wooden table surrounded by dry herbs,
                    rustic, vintage, boho,
                '''
            elif preparation_name_plural == 'syrups':
                prompt = f'''
                    a glass bottle of herbal syrup on a wooden table surrounded by dry herbs,
                    rustic, vintage, boho,
                '''
            elif preparation_name_plural == 'linctuses':
                prompt = f'''
                    herbal linctuses on a wooden table surrounded by dry herbs,
                    rustic, vintage, boho,
                '''
            elif preparation_name_plural == 'mucillages':
                prompt = f'''
                    herbal mucillages on a wooden table surrounded by dry herbs,
                    rustic, vintage, boho,
                '''
            elif preparation_name_plural == 'capsules':
                prompt = f'''
                    herbal capsules on a wooden table surrounded by dry herbs,
                    rustic, vintage, boho,
                '''
            elif preparation_name_plural == 'lozenges':
                prompt = f'''
                    herbal lozenges on a wooden table surrounded by dry herbs,
                    rustic, vintage, boho,
                '''
            elif preparation_name_plural == 'baths':
                prompt = f'''
                    a bathtub full of water and herbs,
                    rustic, vintage, boho,
                '''
            elif preparation_name_plural == 'lotions':
                prompt = f'''
                    herbal lotions on a wooden table surrounded by dry herbs,
                    rustic, vintage, boho,
                '''
            else:
                prompt = f'''
                    cat
                '''
            zimage.image_create(
                output_filepath=f'{out_filepath}', 
                prompt=prompt, width=768, height=768, seed=-1,
            )

def ailments_gen():
    clusters = data.systems_ailments_get()
    systems_slugs = [cluster['system_slug'] for cluster in clusters]
    for system_slug in systems_slugs:
        output_filepath = f'''{g.WEBSITE_FOLDERPATH}/images/systems/{system_slug}.jpg'''
        if os.path.exists(output_filepath): continue
        system_text = system_slug
        if system_text == 'integumentary': system_text = 'skin'
        elif system_text == 'musculoskeletal': system_text = 'muscular'
        prompt = f'''
a glass jar with dry herbs inside and a white label with black text "{system_text}" in script font, on a wooden table surrounded by medicinal herbs, rustic, vintage, boho
        '''
        print(prompt)
        zimage.image_create(
            output_filepath=f'{output_filepath}', 
            prompt=prompt, width=768, height=768, seed=-1,
        )

    organs_slugs = data.organs_get()
    for organ_slug in organs_slugs:
        output_filepath = f'''{g.WEBSITE_FOLDERPATH}/images/organs/{organ_slug}.jpg'''
        if os.path.exists(output_filepath): continue
        organ_text = organ_slug
        if organ_text == 'stomach': organ_text = 'belly'
        elif organ_text == 'adrenal glands': organ_text = 'adrenal'
        prompt = f'''
a glass jar with dry herbs inside and a white label with black text "{organ_text}" in script font, on a wooden table surrounded by medicinal herbs, rustic, vintage, boho
        '''
        zimage.image_create(
            output_filepath=f'{output_filepath}', 
            prompt=prompt, width=768, height=768, seed=-1,
        )

    ailments = io.csv_to_dict(f'{g.DATABASE_FOLDERPATH}/csv/ailments.csv')
    for ailment in ailments:
        ailment_slug = ailment['ailment_slug']
        ailment_name = ailment['ailment_name']
        output_filepath = f'''{g.WEBSITE_FOLDERPATH}/images/ailments/{ailment_slug}.jpg'''
        if os.path.exists(output_filepath): continue
        ailment_text = ailment_name
        prompt = f'''
a glass jar with dry herbs inside and a white label with black text "{ailment_text}" in script font, on a wooden table surrounded by medicinal herbs, rustic, vintage, boho
        '''
        zimage.image_create(
            output_filepath=f'{output_filepath}', 
            prompt=prompt, width=768, height=768, seed=-1,
        )

def gen():
    ailments_gen()
    # ailments_preparations_gen(ailments_rows, preparations_rows)
    # preparations_gen(preparations_rows)

