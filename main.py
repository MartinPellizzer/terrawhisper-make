import shutil

from lib import g

shutil.copy2('style.css', f'{g.website_folderpath}/style.css')
shutil.copy2('styles-herb.css', f'{g.website_folderpath}/styles-herb.css')
shutil.copy2('styles-tmp.css', f'{g.website_folderpath}/styles-tmp.css')
shutil.copy2('styles.css', f'{g.website_folderpath}/styles.css')
shutil.copy2('styles-herb-monograph.css', f'{g.website_folderpath}/styles-herb-monograph.css')

# HERBS..........................[HRB]
# PREPARATIONS...................[PRP]
# AILMENTS.......................[ALM]
# EQUIPMENT......................[EQP]
# APOTHECARY.....................[APT]
# WELLNESS.......................[WLL]
# NUTRITION......................[NTR]
# SPIRITUALITY...................[SPR]
# ART............................[ART]
# SHOP...........................[SHP]
# HOME...........................[HOM]

########################################
# IMAGES.........................[IMG]
########################################
if 0:
    from lib import zimage
    from lib import data
    from lib import polish
    output_folderpath = f'{g.VAULT_TMP_FOLDERPATH}/terrawhisper/zimage'
    herbs = data.herbs_popular_get('teas', 100)
    for herb_i, herb in enumerate(herbs):
        herb_name_scientific = herb['herb_name_scientific']
        herb_slug = polish.sluggify(herb_name_scientific)
        prompt = f'a cup of {herb_name_scientific} tea'
        zimage.image_create(f'{output_folderpath}/{herb_i}-{herb_slug}.jpg', prompt)
    quit()

########################################
# ART............................[ART]
########################################
if 0:
    if 1:
        from hub import art_hub
        art_hub.main()
        quit()

########################################
# PREPARATIONS...................[PRP]
########################################
if 0:
    if 1:
        from hub import hub_preparations
        hub_preparations.gen()
    if 1:
        from lib import art_preparations_best
        art_preparations_best.gen()
    if 0:
        from lib import art_preparations
        art_preparations.gen()
    if 0:
        from lib import cat_preparations
        cat_preparations.gen()
    quit()

########################################
# AILMENTS.......................[ALM]
########################################
if 0:
    if 0:
        from hub import hub_ailments
        hub_ailments.gen()
        quit()
    if 1:
        from lib import art_ailments_preparations
        art_ailments_preparations.gen()
    if 0:
        from lib import art_ailments
        art_ailments.gen()
        quit()
    if 0:
        from lib import cat_ailments
        cat_ailments.gen()

if 0:
    if 1:
        from ai import preparations_images
        preparations_images.gen()
        quit()

########################################
# EQUIPMENT......................[EQP]
########################################
if 0:
    if 0:
        from hub import hub_equipment
        hub_equipment.main()

########################################
# HUBS...........................[HUB]
########################################
if 0:
    from hub import hub_herbs
    hub_herbs.gen()

if 0:
    from hub import hub_apothecary
    from hub import hub_wellness
    from hub import hub_nutrition
    from hub import hub_spirituality
    from hub import hub_art
    hub_apothecary.gen()
    hub_wellness.gen()
    hub_nutrition.gen()
    hub_spirituality.gen()
    hub_art.gen()

########################################
# CSV............................[CSV]
########################################
if 0:
    from hub import hub_csv
    hub_csv.gen()
    quit()

########################################
# SHOP...........................[SHP]
########################################
if 0:
    if 1:
        from hub import hub_shop
        hub_shop.gen()

    # from hub import hub_shop
    # hub_shop.gen()

    if 0:
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
    if 0:
        from lib import pag_shop_tincture_dosage_safety_cheatsheet
        pag_shop_tincture_dosage_safety_cheatsheet.gen()
    if 0:
        from lib import pag_shop_tincture_dosage_safety_cheatsheet_download
        pag_shop_tincture_dosage_safety_cheatsheet_download.gen()
    if 0:
        from lib import pag_shop_labels
        pag_shop_labels.gen()
    if 0:
        from lib import pag_shop
        pag_shop.gen()

########################################
# HERBS..........................[HRB]
########################################
### RUN ONLY WHEN NEW WCVP FILE
if 0:
    from data import herbs_data
    herbs_data.main()
    quit()

if 0:
    from ai import herbs_ai
    herbs_ai.main()
    # quit()

if 0:
    if 1:
        from ai import herbs_images
        herbs_images.gen()
        quit()

if 1:
    if 1:
        # topic hub
        from hub import herbs_hub
        herbs_hub.main()
    if 0:
        # herb index
        from hub import herbs_index
        herbs_index.main()
    if 0:
        from hub import herb_hub
        herb_hub.main()
    if 0:
        import legacy
        legacy.gen()
    if 0:
        from ai import herbs_wcvp
        herbs_wcvp.gen()
    if 0:
        from ai import herbs_existing
        herbs_existing.gen()
    if 0:
        from lib import art_herbs_benefits
        art_herbs_benefits.gen()
    if 0:
        from lib import art_herbs
        art_herbs.gen()

########################################
# TAXONOMY.........................[TXN]
########################################
if 0:
    if 1:
        from ai import taxonomy_ai
        taxonomy_ai.main()

########################################
# HOME...........................[HOM]
########################################
if 0:
    if 0:
        ### OLD
        from lib import pag_home
        pag_home.gen()
    if 1:
        from hub import home_hub
        home_hub.gen()

