import os
import time
import random

from selenium import webdriver
# from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException

from lib import g
from lib import io

datasets_folderpath = f'{g.SSOT_FOLDERPATH}/datasets'

def download_html():
    '''
    geckodriver_path = "geckodriver"
    profile_path = "/home/ubuntu/selenium-firefox-profile"
    options = Options()
    options.profile = profile_path
    service = Service(executable_path=geckodriver_path)
    driver = webdriver.Firefox(
        service=service,
        options=options
    )
    '''

    geckodriver_path = 'geckodriver'
    driver_service = webdriver.FirefoxService(executable_path=geckodriver_path)
    driver = webdriver.Firefox(service=driver_service)

    ###
    herb20_filepath = f'{datasets_folderpath}/herb20/herbs_validated.json'
    herb20_data = io.json_read(herb20_filepath)
    powo_jsons_failed = []
    for herb20_i, herb20_item in enumerate(herb20_data[:]):
        print(f'{herb20_i}/{len(herb20_data)} - {herb20_item}')
        if herb20_item['wcvp'] == None: continue
        ###
        herb20_powo_id = herb20_item['wcvp']['powo_id']
        powo_html_filepath = f'{datasets_folderpath}/powo/html/{herb20_powo_id}.html'
        if not os.path.exists(powo_html_filepath):
            url = f"https://powo.science.kew.org/api/2/taxon/urn:lsid:ipni.org:names:{herb20_powo_id}"
            driver.get(url)
            try:
                WebDriverWait(driver, 10).until(
                    lambda d: d.execute_script("return document.readyState") == "complete"
                )
                print("Page loaded successfully.")
            except TimeoutException:
                print("Timed out waiting for page to load.")
                driver.save_screenshot("timeout.png")
                quit()
            html = driver.page_source
            time.sleep(random.randint(13, 21))
            io.file_write(powo_html_filepath, html)
    driver.quit()

# download_html()

if 0:
    from bs4 import BeautifulSoup
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")
    title = soup.find("table").text
    print(title)

def html_to_json():
    from bs4 import BeautifulSoup
    powo_json_folderpath = f'{datasets_folderpath}/powo/json'
    powo_html_folderpath = f'{datasets_folderpath}/powo/html'
    powo_html_filenames = sorted(os.listdir(powo_html_folderpath))
    for i, powo_html_filename in enumerate(powo_html_filenames):
        print(f'{i}/{len(powo_html_filenames)}')
        powo_html_filepath = f'{powo_html_folderpath}/{powo_html_filename}'
        powo_html = io.file_read(powo_html_filepath)
        html = powo_html
        soup = BeautifulSoup(html, "html.parser")
        content = soup.find("table").text
        try: 
            row = soup.find("tr", id="/kingdom")
            kingdom_value = row.find("td", class_="treeValueCell").get_text(strip=True).strip("\"'")
            print('kingdom', kingdom_value)
        except: 
            kingdom_value = None
            print(powo_html_filepath)
            print(html)
        try: 
            row = soup.find("tr", id="/phylum")
            phylum_value = row.find("td", class_="treeValueCell").get_text(strip=True).strip("\"'")
            print('phylum', phylum_value)
        except: 
            phylum_value = None
            print(powo_html_filepath)
            print(html)
        try: 
            row = soup.find("tr", id="/clazz")
            class_value = row.find("td", class_="treeValueCell").get_text(strip=True).strip("\"'")
            print('class', class_value)
        except: 
            class_value = None
            print(powo_html_filepath)
            print(html)
        try: 
            row = soup.find("tr", id="/subclass")
            subclass_value = row.find("td", class_="treeValueCell").get_text(strip=True).strip("\"'")
            print('subclass', subclass_value)
        except: 
            subclass_value = None
            print(powo_html_filepath)
            print(html)
        try: 
            row = soup.find("tr", id="/order")
            order_value = row.find("td", class_="treeValueCell").get_text(strip=True).strip("\"'")
            print('order', order_value)
        except: 
            order_value = None
            print(powo_html_filepath)
            print(html)
        try: 
            row = soup.find("tr", id="/family")
            family_value = row.find("td", class_="treeValueCell").get_text(strip=True).strip("\"'")
            print('family', family_value)
        except: 
            family_value = None
            print(powo_html_filepath)
            print(html)
        try: 
            row = soup.find("tr", id="/genus")
            genus_value = row.find("td", class_="treeValueCell").get_text(strip=True).strip("\"'")
            print('genus', genus_value)
        except: 
            genus_value = None
            print(powo_html_filepath)
            print(html)
        ###
        powo_json_filepath = f'{powo_json_folderpath}/{powo_html_filename}'.replace('.html', '.json')
        powo_json_data = io.json_read(powo_json_filepath, create=True)
        powo_json_data['kingdom'] = kingdom_value
        powo_json_data['phylum'] = phylum_value
        powo_json_data['class'] = class_value
        powo_json_data['subclass'] = subclass_value
        powo_json_data['order'] = order_value
        powo_json_data['family'] = family_value
        powo_json_data['genus'] = genus_value
        io.json_write(powo_json_filepath, powo_json_data)
        # print(repr(text))
        # print(len(text))
        # quit()


quit()
powo_html_folderpath = f'{datasets_folderpath}/powo/html'
powo_html_filenames = sorted(os.listdir(powo_html_folderpath))
print(len(powo_html_filenames))

herb20_filepath = f'{datasets_folderpath}/herb20/herbs_validated.json'
herb20_data = io.json_read(herb20_filepath)
print(len(herb20_data))
herb20_data_validated = []
for item in herb20_data:
    if item['wcvp'] == None: continue
    if 'plant_name_id' in item['wcvp']: continue
    print(item['wcvp'])
    herb20_data_validated.append(item)
        
print(len(herb20_data_validated))

