import random

from lib import g

def html_head(meta_title, meta_description, form_head='', css='/style.css', canonical=''):
    with open(g.GOOGLE_ADSENSE_SCRIPT) as f: google_adsense_script = f.read()
    with open(g.GOOGLE_ANALYTICS_SCRIPT) as f: google_analytics_script = f.read()
    html = f'''
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <link rel="stylesheet" href="{css}">
            <title>{meta_title}</title>
            <meta name="description" content="{meta_description}">
            {canonical}
            {google_adsense_script}
            {google_analytics_script}
            {form_head}
        </head>
    '''
    return html

def html_lead_magnet_random():
    with open(f'{g.DATABASE_FOLDERPATH}/assets/scripts/newsletter/form-course-preparation-tincture.txt') as f: 
        form_body_0000 = f.read()
    with open(f'{g.DATABASE_FOLDERPATH}/assets/scripts/newsletter/form-checklist-10-herbs-90-percent-ailments.txt') as f: 
        form_body_0001 = f.read()
    lead_magnets = [
        {
            'suptitle': 'FREE COURSE',
            'title': 'How to make medicinal herbl tinctures for common ailments at home and in a weekend (using the Healing Drop System).',
            'img_src': '/images/shop/banner-course-preparation-tincture.jpg',
            'img_alt': 'tincture preparation course banner',
            'form_body': form_body_0000,
        },
        {
            'suptitle': 'FREE CHECKLIST',
            'title': 'The Only 10 Herbs You Need to Heal 90% of Common Ailments.',
            'img_src': '/images/shop/checklist-10-herbs-90-percent-ailments-banner.jpg',
            'img_alt': '10 herbs that heals 90% of common ailments',
            'form_body': form_body_0001,
        },
    ]
    lead_magnet = random.choice(lead_magnets)
    html = f'''
        <div class="free-gift">
            <p class="free-gift-heading">{lead_magnet['suptitle']}</p>
            <p style="text-align: center; margin-bottom: 1.6rem;">{lead_magnet['title']}</p>
            <img src="{lead_magnet['img_src']}" alt="{lead_magnet['img_alt']}">
            {lead_magnet['form_body']}
        </div>
    '''
    return html
