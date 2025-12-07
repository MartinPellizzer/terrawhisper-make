import os
import random

from PIL import Image, ImageFont, ImageDraw, ImageColor, ImageOps

from lib import g
from lib import data
from lib import media
from lib import polish
from lib import zimage

output_folderpath = f'{g.VAULT_TMP_FOLDERPATH}/terrawhisper/zimage'

if 1:
    for filename in os.listdir(output_folderpath):
        os.remove(f'{output_folderpath}/{filename}')

# herbs = data.herbs_popular_get('teas', 100)

rows_num = 4
cols_num = 4
imgs_num = rows_num * cols_num

herbs = data.herbs_popular_get('teas', 100)[:rows_num]
seeds = [random.randint(0, 99999) for _ in range(imgs_num)]

# seed = 42

img_i = 0
for row_i in range(rows_num):
    herb = herbs[row_i]
    for col_i in range(cols_num):
        # print(seeds[herb_i])
        str_i = ''
        if img_i < 10: str_i = f'000{img_i}'
        elif img_i < 100: str_i = f'00{img_i}'
        elif img_i < 1000: str_i = f'0{img_i}'
        else: str_i = f'{img_i}'
        herb_name_scientific = herb['herb_name_scientific']
        herb_slug = polish.sluggify(herb_name_scientific)
        prompt_tea = f'''
            a ceramic cup of {herb_name_scientific} tea on a wooden table surrounded by dry herbs,
            rustic, vintage, boho
        '''
        prompt_tincture = f'''
            a dark amber glass dropper bottle of {herb_name_scientific} tincture on a wooden table surrounded by dry herbs,
            rustic, vintage, boho,
        '''
        zimage.image_create(f'{output_folderpath}/{str_i}-{herb_slug}.jpg', prompt_tincture, seed=seeds[img_i])
        img_i += 1

img_w = rows_num * 400
img_h = cols_num * 400
img = Image.new(mode="RGB", size=(img_w, img_h), color='#ffffff')
draw = ImageDraw.Draw(img)
images_filepaths = sorted([f'{output_folderpath}/{filename}' for filename in os.listdir(output_folderpath) if filename[0].isdigit()])
img_i = 0
for row_i in range(rows_num):
    for col_i in range(cols_num):
        img_0000 = Image.open(images_filepaths[img_i])
        img_0000 = media.resize(img_0000, 400, 400)
        img.paste(img_0000, (400 * col_i, 400 * row_i))
        img_i += 1
img.save(f'{output_folderpath}/grid.jpg', format='JPEG', subsampling=0, quality=100)

