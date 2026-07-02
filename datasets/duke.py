import os
import time
import json
import random
import shutil

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options

from lib import g
from lib import io
from lib import data
from lib import polish

page_num = 96

def download_urls():
    geckodriver_path = 'geckodriver'
    driver_service = webdriver.FirefoxService(executable_path=geckodriver_path)
    driver = webdriver.Firefox(service=driver_service)
    # driver.maximize_window()
    for i in range(page_num):
        herbs_urls_data = []
        if i == 0:
            driver.get(f'https://phytochem.nal.usda.gov/?type=plant&keyword=')
        else:
            driver.get(f'https://phytochem.nal.usda.gov/?type=plant&keyword=&page={i}')
        time.sleep(random.randint(13, 21))
        uls = driver.find_elements(By.XPATH, '//ul[@class="usa-collection"]')
        for ul in uls:
            lis = ul.find_elements(By.XPATH, './/li')
            for li in lis:
                a = li.find_element(By.XPATH, './/a')
                href = a.get_attribute('href')
                text = a.text
                print(text, href)
                herbs_urls_data.append({'herb_name_latin': text, 'herb_url': href})
        herbs_urls_filepath = f'{g.SSOT_FOLDERPATH}/datasets/duke/urls/{i}.json'
        io.json_write(herbs_urls_filepath, herbs_urls_data)
    driver.quit()

def create_urls_json():
    herbs_urls_data_full = []
    for i in range(page_num):
        herbs_urls_filepath = f'{g.SSOT_FOLDERPATH}/datasets/duke/urls/{i}.json'
        herbs_urls_data = io.json_read(herbs_urls_filepath)
        for herb_url_item in herbs_urls_data:
            herbs_urls_data_full.append(herb_url_item)
    for herb_url_item in herbs_urls_data_full:
        print(json.dumps(herb_url_item, indent=4))
    herbs_urls_filepath = f'{g.SSOT_FOLDERPATH}/datasets/duke/herbs_urls.json'
    io.json_write(herbs_urls_filepath, herbs_urls_data_full)

def validate_plants_wcvp():
    ### VALIDATE PLANTS WCVP
    duke__data_merged_filepath = f'{g.SSOT_FOLDERPATH}/datasets/duke/herbs_urls_validated.json'
    duke__data_merged = io.json_read(duke__data_merged_filepath, create=True, l=True)
    duke__data_merged = []
    ###
    herbs_urls_filepath = f'{g.SSOT_FOLDERPATH}/datasets/duke/herbs_urls.json'
    herbs_urls_data = io.json_read(herbs_urls_filepath)
    for i, herb_url_item in enumerate(herbs_urls_data):
        print(f'{i}/{len(herbs_urls_data)} - {herb_url_item}')
        print(json.dumps(herb_url_item, indent=4))
        ###
        wcvp_row = data.sqlite3__wcvp_get(herb_url_item['herb_name_latin'])
        data_merged = herb_url_item
        if wcvp_row != None:
            data_merged['wcvp'] = json.loads(wcvp_row[2])
        else:
            data_merged['wcvp'] = None
        duke__data_merged.append(data_merged)
        ###
        io.json_write(duke__data_merged_filepath, duke__data_merged)
        # quit()

def download_csvs():
    geckodriver_path = 'geckodriver'
    driver_service = webdriver.FirefoxService(executable_path=geckodriver_path)
    driver = webdriver.Firefox(service=driver_service)
    ###
    duke__data_merged_filepath = f'{g.SSOT_FOLDERPATH}/datasets/duke/herbs_urls_validated.json'
    duke__data_merged = io.json_read(duke__data_merged_filepath)
    validated_num = 0
    for i, duke__item in enumerate(duke__data_merged):
        print(f'{i}/{len(duke__data_merged)} - {duke__item}')
        # print(json.dumps(duke__item, indent=4))
        if duke__item['wcvp'] == None: continue
        validated_num += 1
        ###
        herb_name_latin = duke__item['herb_name_latin']
        herb_name_latin_slug = polish.sluggify(herb_name_latin)
        herb_url = duke__item['herb_url']
        output_folderpath = f'{g.SSOT_FOLDERPATH}/datasets/duke/csv/{herb_name_latin_slug}'
        os.makedirs(output_folderpath, exist_ok=True)
        ###
        output_chemicals_filepath = f'{output_folderpath}/chemicals.csv'
        output_activities_filepath = f'{output_folderpath}/activities.csv'
        if os.path.exists(output_chemicals_filepath) and os.path.exists(output_activities_filepath): continue
        driver.get(herb_url)
        time.sleep(random.randint(2, 3))
        if not os.path.exists(output_chemicals_filepath):
            elements_csv = driver.find_elements(By.XPATH, '//a/span[text()="CSV"]')
            for e in elements_csv:
                if e.text.strip() == 'CSV':
                    e.click()
                    time.sleep(random.randint(2, 3))
                    break
            input_filepath = f'/home/ubuntu/Downloads/Plant Chemicals.csv'
            try: 
                shutil.copy2(input_filepath, output_chemicals_filepath)
                time.sleep(random.randint(2, 3))
                os.remove(input_filepath)
            except:
                io.file_write(f'{output_folderpath}/chemicals.csv', '')
                time.sleep(random.randint(2, 3))
        ###
        if not os.path.exists(output_activities_filepath):
            try: element_csv = driver.find_element(By.XPATH, '//a[text()="Activities"]')
            except:
                time.sleep(random.randint(300, 600))
                continue
            element_csv.click()
            time.sleep(random.randint(2, 3))
            elements_csv = driver.find_elements(By.XPATH, '//a/span[text()="CSV"]')
            for e in elements_csv:
                if e.text.strip() == 'CSV':
                    e.click()
                    time.sleep(random.randint(2, 3))
                    break
            input_filepath = f'/home/ubuntu/Downloads/Plant Activities.csv'
            try: 
                shutil.copy2(input_filepath, output_activities_filepath)
                time.sleep(random.randint(2, 3))
                os.remove(input_filepath)
            except:
                io.file_write(f'{output_folderpath}/activities.csv', '')
                time.sleep(random.randint(2, 3))
        ###
        # break
    print(validated_num)

def herbs_validated_0000():
    duke__input_data_filepath = f'{g.SSOT_FOLDERPATH}/datasets/duke/herbs_urls_validated.json'
    duke__input_data = io.json_read(duke__input_data_filepath)
    for i, duke__input_item in enumerate(duke__input_data):
        print(f'{i}/{len(duke__input_data)} - {duke__input_item}')
        if duke__input_item['wcvp'] == None: continue
        ###
        herb_name_latin = duke__input_item['herb_name_latin']
        herb_name_latin_slug = polish.sluggify(herb_name_latin)
        herb_url = duke__input_item['herb_url']
        ###
        duke__output_data = duke__input_item
        duke__chemicals_csv_filepath = f'{g.SSOT_FOLDERPATH}/datasets/duke/csv/{herb_name_latin_slug}/chemicals.csv'
        duke__activities_csv_filepath = f'{g.SSOT_FOLDERPATH}/datasets/duke/csv/{herb_name_latin_slug}/activities.csv'
        try: 
            duke__chemicals_data = io.csv_to_dict(duke__chemicals_csv_filepath, delimiter=',')
            duke__output_data['chemicals'] = duke__chemicals_data
        except: pass
        try: 
            duke__activities_data = io.csv_to_dict(duke__activities_csv_filepath, delimiter=',')
            duke__output_data['activities'] = duke__activities_data
        except: pass
        ###
        duke__output_data_filepath = f'{g.SSOT_FOLDERPATH}/datasets/duke/json/{herb_name_latin_slug}.json'
        io.json_write(duke__output_data_filepath, duke__output_data)
        # print(json.dumps(duke__output_data, indent=5))
        # quit()

    

def download():
    # download_urls()
    # create_urls_json()
    # validate_plants_wcvp()
    # download_csvs()

    herbs_validated_0000()

