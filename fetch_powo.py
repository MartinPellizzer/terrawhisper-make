# TODO: clean up code, download with browser
# TODO: download powo plants from master plant db

import os
import time
import random
import sqlite3

from selenium import webdriver
# from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException

from lib import g
from lib import io

import reference_utils
import masterize_utils

datasets_folderpath = f'{g.SSOT_FOLDERPATH}/datasets'

HUB_FOLDERPATH = f'''{g.DATA_FOLDERPATH}/herbs'''

def download_html_form_master():
    geckodriver_path = 'geckodriver'
    driver_service = webdriver.FirefoxService(executable_path=geckodriver_path)
    driver = webdriver.Firefox(service=driver_service)
    output_folderpath = f'{HUB_FOLDERPATH}/fetch/powo/html'
    io.folders_recursive_gen(output_folderpath)

    master_items = masterize_utils.masterize_plants_get_all()
    for i, master_item in enumerate(master_items):
        print(f'{i}/{len(master_items)}')
        ###
        conn = sqlite3.connect(f"{HUB_FOLDERPATH}/reference/wcvp/wcvp.db")
        conn.row_factory = sqlite3.Row
        cursor = conn.execute(f'''
            SELECT *
            FROM wcvp_plants_names
            WHERE taxon_name_normalized = ?
        ''', (master_item['plant_name_scientific_reference_normalize'],))
        wcvp_rows = cursor.fetchall()
        wcvp_items = [dict(row) for row in wcvp_rows]
        conn.close()
        if wcvp_items == []: continue
        wcvp_item = wcvp_items[0]
        ###
        from tabulate import tabulate
        print(tabulate(wcvp_rows, 
            headers=[
                "PLANT_NAME_ID", 
                "ACCEPTED_PLANT_NAME_ID", 
                "TAXON_STATUS", 
                "TAXON_NAME", 
                "TAXON_NAME_NORMALIZED",
                "POWO_ID",
                "IPNI_ID",
            ], 
            tablefmt="plain")
        )
        ###
        powo_id = wcvp_item['powo_id']
        # print(powo_id)
        # quit()
        # powo_id = plant_row[3]
        powo_html_filepath = f'{output_folderpath}/{powo_id}.html'
        if not os.path.exists(powo_html_filepath):
            url = f"https://powo.science.kew.org/api/2/taxon/urn:lsid:ipni.org:names:{powo_id}"
            driver.get(url)
            try:
                WebDriverWait(driver, 10).until(
                    lambda d: d.execute_script("return document.readyState") == "complete"
                )
                print("Page loaded successfully.")
            except TimeoutException:
                print("Timed out waiting for page to load.")
                driver.save_screenshot(f'{HUB_FOLDERPATH}/fetch/powo/timeouts_logs/{powo_id}.png')
                quit()
            html = driver.page_source
            time.sleep(random.randint(13, 21))
            io.file_write(powo_html_filepath, html)
    driver.quit()

def download_html():
    geckodriver_path = 'geckodriver'
    driver_service = webdriver.FirefoxService(executable_path=geckodriver_path)
    driver = webdriver.Firefox(service=driver_service)

    ###
    herb20_filepath = f'{datasets_folderpath}/herb20/herbs_validated.json'
    herb20_data = io.json_read(herb20_filepath)
    print(herb20_data[0])
    quit()
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

def run():
    print('FETCH >> powo')

    start = time.perf_counter()
    # download_html()
    download_html_form_master()
    print(f'download html_form_master() - execution time: ', time.perf_counter() - start)
