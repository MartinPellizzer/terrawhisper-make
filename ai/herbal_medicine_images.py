import os

from lib import g
from lib import io
from lib import zimage

def herbal_medicine__plants__gen(regen=False):
    output_folderpath = f'''{g.WEBSITE_FOLDERPATH}/images/herbal-medicine'''
    io.folders_recursive_gen(output_folderpath)
    output_filepath = f'''{output_folderpath}/medicinal-herbs.jpg'''
    if regen:
        os.remove(output_filepath)
    if not os.path.exists(output_filepath):
        prompt = f'''
            dry chamomile, turmeric, ginger, and echinacea herb on a wooden table surrounded by other medicinal herbs,
            rustic, vintage, boho,
        '''.replace('  ', ' ')
        zimage.image_create(
            output_filepath=f'{output_filepath}', 
            prompt=prompt, width=768, height=768, seed=-1,
        )

def main():
    herbal_medicine__plants__gen(regen=False)
