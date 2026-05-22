import os
import time
import random
import csv
from datetime import datetime
import re
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from PIL import Image, ImageFont, ImageDraw, ImageColor, ImageOps

from lib import g
from lib import io

profile_path = "/home/ubuntu/snap/firefox/common/.mozilla/firefox/m5hj6mvr-copy.default"
options = Options()
options.binary_location = "/snap/firefox/current/usr/lib/firefox/firefox"
options.add_argument("-profile")
options.add_argument(profile_path)
driver = webdriver.Firefox(options=options)
driver.get("https://google.com")



    # SEARCH RESULTS
    elements = driver.find_elements(By.XPATH, '//*[@role="listitem"]')
    rows = []
    asins_done = []
    for element in elements:
        try: link = element.find_element(By.XPATH, './/a').get_attribute('href')
        except: continue
        link_no_ref = link.split('/ref=')[0]
        if 'sspa' in link_no_ref: continue
        if '/dp/' not in link_no_ref: continue
        asin = link_no_ref.split('/')[-1]
        print(asin)
        if asin in asins_done: continue
        else: asins_done.append(asin)
        print(link_no_ref)
        row = [link_no_ref]
        rows.append(row)
    print("################################################")
    print(len(rows))
    print("################################################")


'''

import os
import time
import random
import csv
from datetime import datetime
import re
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
from PIL import Image, ImageFont, ImageDraw, ImageColor, ImageOps

from lib import g
from lib import io
#import data_csv
#import util
#import util_data

vault = '/home/ubuntu/vault'
vault_tmp = '/home/ubuntu/vault-tmp'

# options = Options()
# options.binary_location = r'C:\Program Files\Mozilla Firefox\firefox.exe'
# driver = webdriver.Firefox(executable_path=r'C:\drivers\geckodriver.exe', options=options)

geckodriver_path = 'geckodriver'
driver_service = webdriver.FirefoxService(executable_path=geckodriver_path)

driver = webdriver.Firefox(service=driver_service)
driver.get('https://www.google.com')
driver.maximize_window()
'''
