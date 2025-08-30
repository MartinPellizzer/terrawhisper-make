import os

from lib import g
from lib import io

project_name = f'terrawhisper'

def keywords_get(category='', seed=''):
    keywords_all = []
    folderpath_00 = f'{g.vault_folderpath}/{project_name}/database/keywords/pinterest-pinclicks/{category}'
    for foldername_00 in os.listdir(folderpath_00):
        folderpath_01 = f'{folderpath_00}/{foldername_00}'
        for filename_01 in os.listdir(folderpath_01):
            filepath = f'{folderpath_01}/{filename_01}'
            if seed == '':
                keywords_rows = io.csv_to_dict(filepath, ',')
                for k in keywords_rows:
                    try: int(k['Search Volume'])
                    except: continue
                    keywords_all.append(k)
            else:
                if seed in filename_01:
                    keywords_rows = io.csv_to_dict(filepath, ',')
                    for k in keywords_rows:
                        try: int(k['Search Volume'])
                        except: continue
                        keywords_all.append(k)
    keywords_rows = keywords_all
    keywords_rows = sorted(keywords_rows, key=lambda x: int(x['Search Volume']), reverse=True)
    for keyword_row in keywords_rows[:200]:
        print(keyword_row['Search Volume'], keyword_row['Label'])
    print(len(keywords_rows))
    return keywords_rows

keywords = keywords_get(category='00-herbal-medicine', seed='')
quit()

keywords_density = []
for i, k in enumerate(keywords[:20000]): 
    found = False
    keyword_list = k['Label'].split()
    for word in keyword_list:
        word.strip().lower()
        for keyword_density in keywords_density:
            if word == keyword_density['Label']:
                keyword_density['mentions'] += 1
                found = True
                break
        if not found:
            keywords_density.append(
                {
                    'Label': word,
                    'mentions': 1,
                }
            )
keywords_density = sorted(keywords_density, key=lambda x: int(x['mentions']), reverse=True)
for k in keywords_density[:200]:
    print(k)
