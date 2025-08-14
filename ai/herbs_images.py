import os
import shutil

from lib import g
from lib import io
from lib import data
from lib import media
from lib import polish

def gen():
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

gen()
