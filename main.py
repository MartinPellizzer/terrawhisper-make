import shutil

from lib import g

shutil.copy2('style.css', f'{g.website_folderpath}/style.css')

# HERBS..........................[HRB]
# PREPARATIONS...................[PRP]
# AILMENTS.......................[ALM]
# WELLNESS.......................[WLL]
# SHOP...........................[SHP]
# HOME...........................[HOM]

########################################
# HERBS..........................[HRB]
########################################
if 0:
    if 1:
        from ai import herbs
        herbs.gen()
    if 0:
        from ai import herbs_images
        herbs_images.gen()
    if 0:
        from lib import art_herbs_benefits
        art_herbs_benefits.gen()
    if 0:
        from lib import art_herbs
        art_herbs.gen()
    if 0:
        from lib import cat_herbs
        cat_herbs.gen()

########################################
# PREPARATIONS...................[PRP]
########################################
if 0:
    if 0:
        from lib import art_preparations_best
        art_preparations_best.gen()
    if 0:
        from lib import art_preparations
        art_preparations.gen()
    if 0:
        from lib import cat_preparations
        cat_preparations.gen()

########################################
# AILMENTS.......................[ALM]
########################################
if 0:
    if 1:
        from lib import art_ailments_preparations
        art_ailments_preparations.gen()
    if 1:
        from lib import art_ailments
        art_ailments.gen()
    if 1:
        from lib import cat_ailments
        cat_ailments.gen()

########################################
# WELLNESS.......................[WLL]
########################################
if 1:
    if 1:
        from lib import art_wellness
        art_wellness.gen()

########################################
# SHOP...........................[SHP]
########################################
if 0:
    if 1:
        from lib import pag_shop_labels_download
        pag_shop_labels_download.gen()
    if 0:
        from lib import pag_shop_tincture_dosage_and_safety_download
        pag_shop_tincture_dosage_and_safety_download.gen()
    if 0:
        from lib import pag_shop_herb_drying_checklist
        pag_shop_herb_drying_checklist.gen()
    if 0:
        from lib import pag_shop_herb_drying_checklist_download
        pag_shop_herb_drying_checklist_download.gen()
    if 1:
        from lib import pag_shop_tincture_dosage_safety_cheatsheet
        pag_shop_tincture_dosage_safety_cheatsheet.gen()
    if 1:
        from lib import pag_shop_tincture_dosage_safety_cheatsheet_download
        pag_shop_tincture_dosage_safety_cheatsheet_download.gen()
    if 0:
        from lib import pag_shop_labels
        pag_shop_labels.gen()
    if 1:
        from lib import pag_shop
        pag_shop.gen()

########################################
# HOME...........................[HOM]
########################################
if 0:
    if 1:
        from lib import pag_home
        pag_home.gen()

