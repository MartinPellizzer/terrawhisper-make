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

def sqlite_table_master_plants_get():
    db_filepath = f'{g.DATA_FOLDERPATH}/masterize/master.db'
    conn = sqlite3.connect(db_filepath)
    cur = conn.cursor()
    cur.execute("""
        SELECT *
        FROM plants
    """)
    row = cur.fetchall()
    conn.close()
    return row

def download_html_form_master():
    geckodriver_path = 'geckodriver'
    driver_service = webdriver.FirefoxService(executable_path=geckodriver_path)
    driver = webdriver.Firefox(service=driver_service)

    plants_rows = masterize_utils.masterize_plants_get_all()
    for i, plant_row in enumerate(plants_rows):
        print(f'{i}/{len(plants_rows)}')
        plant_name_normalized = plant_row[2]
        wcvp_row = reference_utils.wcvp_plant_name_get_row(plant_name_normalized)
        powo_id = wcvp_row[5]
        print(plant_row)
        print(wcvp_row)
        print(powo_id)
        # quit()
        # powo_id = plant_row[3]
        powo_html_filepath = f'{g.DATA_FOLDERPATH}/fetch/powo/html/{powo_id}.html'
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
                driver.save_screenshot(f'{g.DATA_FOLDERPATH}/fetch/powo/timeouts_logs/{powo_id}.png')
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
