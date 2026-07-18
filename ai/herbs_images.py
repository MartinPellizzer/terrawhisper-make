import os
import shutil

from lib import g
from lib import io
from lib import data
from lib import media
from lib import polish
from lib import zimage

# herbs_primary = data.herbs_primary_get()
# herbs_popular = data.herbs_popular_get('teas', 100)

import masterize_utils

def gen_old():
    herbs = data.herbs_medicinal_get()
    for herb_i, herb in enumerate(herbs):
        herb_name_scientific = herb['herb_name_scientific']
        herb_slug = polish.sluggify(herb_name_scientific)
        ###
        out_filepath = f'''{g.database_folderpath}/images/herbs/{herb_slug}.jpg'''
        if not os.path.exists(out_filepath):
            prompt = f'''
                dry {herb_name_scientific} herb,
                on a wooden table,
                rustic, vintage, boho,
                warm tones,
                high resolution,
            '''.replace('  ', ' ')
            image = media.image_gen(prompt, 1024, 1024)
            image = media.resize(image, 768, 768)
            # image.show()
            image.save(out_filepath)
        # quit()
    in_folderpath = f'''{g.database_folderpath}/images/herbs'''
    web_folderpath = f'''{g.website_folderpath}/images/herbs'''
    for in_filename in os.listdir(in_folderpath):
        in_filepath = f'''{in_folderpath}/{in_filename}'''
        web_filepath = f'''{web_folderpath}/{in_filename}'''
        print(in_filepath)
        print(web_filepath)
        print()
        shutil.copy2(in_filepath, web_filepath)

def herbs_gen(dispel=False):
    herbs = []
    if 1:
        for herb in herbs_primary: 
            herbs.append({'herb_name_scientific': herb['herb_name_scientific']})
    if 1:
        for herb in herbs_popular: 
            herbs.append({'herb_name_scientific': herb['herb_name_scientific']})
    for herb_i, herb in enumerate(herbs):
        herb_name_scientific = herb['herb_name_scientific']
        herb_slug = polish.sluggify(herb_name_scientific)
        ###
        output_folderpath = f'''{g.WEBSITE_FOLDERPATH}/images/herbs/primary'''
        output_filepath = f'''{output_folderpath}/{herb_slug}.jpg'''
        try: os.makedirs(output_folderpath)
        except: pass
        if dispel:
            try: os.remove(out_filepath)
            except: pass
            continue
        ###
        if not os.path.exists(output_filepath):
            prompt = f'''
                dry {herb_name_scientific} herb on a wooden table surrounded by other medicinal herbs,
                rustic, vintage, boho,
            '''.replace('  ', ' ')
            zimage.image_create(
                output_filepath=f'{output_filepath}', 
                prompt=prompt, width=768, height=768, seed=-1,
            )
        quit()

def herbs_gen_new(dispel=False):
    # rows = data.sqlite3__wikidata_powo_get_all()
    plants_rows = masterize_utils.masterize_plants_get_all()
    # print(rows[0])
    # print(plants_rows[0])
    # quit()
    # herbs = [row[-2] for row in rows if row[-1] == 'SPECIES']
    herbs = [row[1] for row in plants_rows]
    for herb_i, herb in enumerate(herbs):
        print(f'{herb_i}/{len(herbs)} - {herb}')
        herb_name_scientific = herb
        herb_slug = polish.sluggify(herb_name_scientific)
        ###
        # output_folderpath = f'''{g.WEBSITE_FOLDERPATH}/images/herbs/primary'''
        output_folderpath = f'''{g.WEBSITE_FOLDERPATH}/images/herbs'''
        output_filepath = f'''{output_folderpath}/{herb_slug}.jpg'''
        try: os.makedirs(output_folderpath)
        except: pass
        if dispel:
            try: os.remove(out_filepath)
            except: pass
            continue
        ###
        if not os.path.exists(output_filepath):
            prompt = f'''
                dry {herb_name_scientific} herb on a wooden table surrounded by other medicinal herbs,
                rustic, vintage, boho,
            '''.replace('  ', ' ')
            zimage.image_create(
                output_filepath=f'{output_filepath}', 
                prompt=prompt, width=768, height=768, seed=-1,
            )

def gen():
    herbs_gen_new(dispel=False)

