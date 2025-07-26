import shutil

from lib import g

shutil.copy2('style.css', f'{g.website_folderpath}/style.css')

# ailments
if 1:
    if 1:
        from lib import art_ailments_preparations
        art_ailments_preparations.gen()

