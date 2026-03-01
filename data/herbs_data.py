import os
import json

from lib import g
from lib import io
from lib import llm
from lib import data

herbs_wcvp = data.herbs_wcvp_get()
herbs_primary_medicinal = data.herbs_primary_medicinal_get()
herbs_popular = data.herbs_popular_get('teas', 100)

def herb_wcvp_find(herb):
    for herb_wcvp in herbs_wcvp:
        if herb_wcvp['taxon_name'].lower().strip() == herb['herb_name_scientific'].lower().strip():
            return herb_wcvp
    return None

def herbs_medicinal_validated_gen():
    herbs = []
    if 1:
        for herb in herbs_primary_medicinal: 
            herbs.append({'herb_name_scientific': herb['herb_name_scientific']})
    if 1:
        for herb in herbs_popular: 
            herbs.append({'herb_name_scientific': herb['herb_name_scientific']})
    herbs_medicinal_validated = []
    for herb_i, herb in enumerate(herbs):
        print('####################################')
        print(f'{herb_i}/{len(herbs)} - {herb}')
        print('####################################')
        found = False
        for _herb in herbs_medicinal_validated:
            if _herb['taxon_name'].lower().strip() == herb['herb_name_scientific'].lower().strip():
                found = True
                break
        if not found:
            herb_wcvp = herb_wcvp_find(herb)
            if herb_wcvp:
                print(herb_wcvp)
                herbs_medicinal_validated.append(herb_wcvp)
    herbs_medicinal_validated_folderpath = f'{g.SSOT_FOLDERPATH}/herbs'
    herbs_medicinal_validated_filepath = f'''{herbs_medicinal_validated_folderpath}/herbs-medicinal-validated.json'''
    io.json_write(herbs_medicinal_validated_filepath, herbs_medicinal_validated)

def main():
    # herbs_medicinal_validated_gen()
    pass

