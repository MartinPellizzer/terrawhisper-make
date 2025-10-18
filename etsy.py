import os
import random

from PIL import Image, ImageFont, ImageDraw, ImageColor, ImageOps

from lib import g
from lib import media

def shop_labels_etsy():
    herb_list = os.listdir(f'{g.assets_folderpath}/shop/labels/public/100/vintage/oval/1x2/png')
    c_light_2 = g.color_linen
    c_dark_2 = g.color_carbon_powder
    images_filepaths = []
    width = 1216
    height = 832
    ### images
    pin_w = 2000
    pin_h = 2000
    row_num = 10
    col_num = 10
    scale = 0.30
    gap = 30
    img_i = 0
    mx = -200
    my = -200
    pin_image = Image.new(mode="RGBA", size=(pin_w, pin_h), color=g.color_linen)
    herb_list_shuffle = herb_list[:]
    random.shuffle(herb_list_shuffle)
    x_cur = mx
    for col_i in range(col_num):
        y_cur = my
        for row_i in range(row_num):
            img_i = img_i % len(herb_list_shuffle)
            herb_filename_correct = herb_list[img_i]
            print(herb_filename_correct)
            rnd = random.randint(0, 3)
            if rnd == 0:
                image_filepath = f'{g.assets_folderpath}/shop/labels/public/100/vintage/round/3x3/png/{herb_filename_correct}'
                label_w = int(3 * 300 * scale)
                label_h = int(3 * 300 * scale)
            elif rnd == 1:
                image_filepath = f'{g.assets_folderpath}/shop/labels/public/100/vintage/oval/3x5/png/{herb_filename_correct}'
                label_w = int(3 * 300 * scale)
                label_h = int(5 * 300 * scale)
            elif rnd == 2:
                image_filepath = f'{g.assets_folderpath}/shop/labels/public/100/vintage/square/3x3/png/{herb_filename_correct}'
                label_w = int(3 * 300 * scale)
                label_h = int(3 * 300 * scale)
            else:
                image_filepath = f'{g.assets_folderpath}/shop/labels/public/100/vintage/rectangle/3x5/png/{herb_filename_correct}'
                label_w = int(3 * 300 * scale)
                label_h = int(5 * 300 * scale)
            image = Image.open(image_filepath)
            image = media.resize(image, label_w, label_h)
            # pin_image.paste(image, (label_w*col_i+gap*col_i+mx, label_h*row_i+gap*row_i+my), image)
            pin_image.paste(image, (x_cur, y_cur), image)
            y_cur += label_h + gap
            img_i += 1
        x_cur += label_w + gap
    pin_image = pin_image.convert('RGB')
    ### save pin
    img = pin_image.convert('RGB')
    img_filepath = f'/home/ubuntu/Downloads/labels-etsy.jpg'
    img.save(img_filepath, format='JPEG', subsampling=0, quality=100)

shop_labels_etsy()
