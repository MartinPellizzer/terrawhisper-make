import shutil

from lib import g

shutil.copy2('style.css', f'{g.website_folderpath}/style.css')

# HERBS..........................[HRB]
# AILMENTS.......................[ALM]
# SHOP...........................[SHP]
# HOME...........................[HOM]

########################################
# HERBS..........................[HRB]
########################################
if 1:
    if 0:
        from ai import herbs
        herbs.gen()
    if 1:
        from ai import herbs_images
        herbs_images.gen()
    if 0:
        from lib import art_herbs_benefits
        art_herbs_benefits.gen()
    if 0:
        from lib import art_herbs
        art_herbs.gen()
    if 1:
        from lib import cat_herbs
        cat_herbs.gen()

########################################
# AILMENTS.......................[ALM]
########################################
if 0:
    if 0:
        from lib import art_ailments_preparations
        art_ailments_preparations.gen()
    if 0:
        from lib import art_ailments
        art_ailments.gen()
    if 1:
        from lib import cat_ailments
        cat_ailments.gen()

########################################
# SHOP...........................[SHP]
########################################
if 0:
    if 1:
        from lib import pag_shop_labels_download
        pag_shop_labels_download.gen()

########################################
# HOME...........................[HOM]
########################################
if 0:
    if 1:
        from lib import pag_home
        pag_home.gen()

