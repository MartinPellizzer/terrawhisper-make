'''
Because of "reasons", parsing POWO means converting html in json
'''

import os
import csv
import time
import shutil

from lib import g
from lib import io

from bs4 import BeautifulSoup

def powo_to_jsons():
    source_foldername = 'powo'
    input_foldername = 'fetch'
    output_foldername = 'parse'
    input_folderpath = f'{g.DATA_FOLDERPATH}/{input_foldername}/{source_foldername}/html'
    output_folderpath = f'{g.DATA_FOLDERPATH}/{output_foldername}/{source_foldername}/json'
    try: shutil.rmtree(output_folderpath)
    except: pass
    io.folders_recursive_gen(output_folderpath)
    ###
    input_filenames = sorted(os.listdir(input_folderpath))
    for i, powo_html_filename in enumerate(input_filenames[:]):
        print(f'{i}/{len(input_filenames)}')
        powo_html_filepath = f'{input_folderpath}/{powo_html_filename}'
        powo_html = io.file_read(powo_html_filepath)
        html = powo_html
        soup = BeautifulSoup(html, "html.parser")
        content = soup.find("table").text
        try: 
            row = soup.find("tr", id="/name")
            name_value = row.find("td", class_="treeValueCell").get_text(strip=True).strip("\"'")
            print('name', name_value)
            if len(name_value) > 50: continue
        except: 
            name_value = None
            print(powo_html_filepath)
            print(html)
        try: 
            row = soup.find("tr", id="/kingdom")
            kingdom_value = row.find("td", class_="treeValueCell").get_text(strip=True).strip("\"'")
            print('kingdom', kingdom_value)
            if len(kingdom_value) > 20: continue
        except: 
            kingdom_value = None
            print(powo_html_filepath)
            print(html)
        try: 
            row = soup.find("tr", id="/phylum")
            phylum_value = row.find("td", class_="treeValueCell").get_text(strip=True).strip("\"'")
            print('phylum', phylum_value)
            if len(kingdom_value) > 20: continue
        except: 
            phylum_value = None
            print(powo_html_filepath)
            print(html)
        try: 
            row = soup.find("tr", id="/clazz")
            class_value = row.find("td", class_="treeValueCell").get_text(strip=True).strip("\"'")
            print('class', class_value)
            if len(kingdom_value) > 20: continue
        except: 
            class_value = None
            print(powo_html_filepath)
            print(html)
        try: 
            row = soup.find("tr", id="/subclass")
            subclass_value = row.find("td", class_="treeValueCell").get_text(strip=True).strip("\"'")
            print('subclass', subclass_value)
            if len(kingdom_value) > 20: continue
        except: 
            subclass_value = None
            print(powo_html_filepath)
            print(html)
        try: 
            row = soup.find("tr", id="/order")
            order_value = row.find("td", class_="treeValueCell").get_text(strip=True).strip("\"'")
            print('order', order_value)
            if len(kingdom_value) > 20: continue
        except: 
            order_value = None
            print(powo_html_filepath)
            print(html)
        try: 
            row = soup.find("tr", id="/family")
            family_value = row.find("td", class_="treeValueCell").get_text(strip=True).strip("\"'")
            print('family', family_value)
            if len(kingdom_value) > 20: continue
        except: 
            family_value = None
            print(powo_html_filepath)
            print(html)
        try: 
            row = soup.find("tr", id="/genus")
            genus_value = row.find("td", class_="treeValueCell").get_text(strip=True).strip("\"'")
            print('genus', genus_value)
            if len(kingdom_value) > 20: continue
        except: 
            genus_value = None
            print(powo_html_filepath)
            print(html)
        ###
        powo_json_filepath = f'{output_folderpath}/{powo_html_filename}'.replace('.html', '.json')
        powo_json_data = io.json_read(powo_json_filepath, create=True)
        powo_json_data['name'] = name_value
        powo_json_data['kingdom'] = kingdom_value
        powo_json_data['phylum'] = phylum_value
        powo_json_data['class'] = class_value
        powo_json_data['subclass'] = subclass_value
        powo_json_data['order'] = order_value
        powo_json_data['family'] = family_value
        powo_json_data['genus'] = genus_value
        io.json_write(powo_json_filepath, powo_json_data)
        # print(name_value)
        # print(len(text))
        # quit()

def run():
    print('PARSE >> powo')

    start = time.perf_counter()
    powo_to_jsons() ### WARNING: takes many many minutes
    print(f'powo to_jsons() - execution time: ', time.perf_counter() - start)

