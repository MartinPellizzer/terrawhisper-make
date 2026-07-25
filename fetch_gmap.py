import os
from time import sleep

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

from lib import g
from lib import io

def get_old_businesses(output_file):
	if not os.path.isfile(output_file): 
		with open(output_file, 'w', encoding="utf-8") as f:
			return []
	else:
		with open(output_file, 'r', encoding="utf-8") as f:
			return [line.split('\\')[0] for line in f.readlines()]

def sanitize(text):
    chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890,.+-()\'&@ '
    try: encoded_string = text.encode('ascii', 'ignore')
    except: return ''
    decoded_string = encoded_string.decode()
    text = ''
    for c in decoded_string:
        if c in chars:
            text += c
    return text

def get_card_element(e):
	try: return e.find_elements(By.XPATH, '//div[@role="main"]')[1]
	except: return None


def scrape_name(e):
	try: return e.find_element(By.XPATH, './/h1').text
	except: return ''
	

def scrape_category(e):
	try: 
        element = e.find_element(By.XPATH, './/h1').text
        return element
	except: return ''
	

def scrape_address(e):
	try: return e.find_element(By.XPATH, './/button[@data-item-id="address"]').text
	except: return ''


def scrape_district(e):
	try: return e.find_element(By.XPATH, './/button[@data-item-id="address"]').text.split(' ')[-1]
	except: return ''


def scrape_website(e):
	try: return e.find_element(By.XPATH, './/a[@data-item-id="authority"]').get_attribute("href")
	except: return ''


def scrape_phone(e):
	try: return e.find_element(By.XPATH, './/button[contains(@data-item-id, "phone")]').text
	except: return ''


def find_new_business(old_businesses):
	global driver
	try: feed = driver.find_element(By.XPATH, '//div[@role="feed"]')
	except: return None, None
	items = feed.find_elements(By.XPATH, './/a/..')
	for item in items:
		a = item.find_element(By.XPATH, './/a')
		a_href = a.get_attribute('href')
		if 'support.' in a_href: continue
		if 'google.' not in a_href: continue
		if '/maps/' not in a_href: continue
		label = a.get_attribute('aria-label')
		label = sanitize(label)
		label = label.replace('Link visitato', '')
		if label not in old_businesses:
			return item, label
	return None, None

def click_on_listing(business):
	for _ in range(3):
		try: 
			business.click()
			return True
		except: 
			print('error click')
			continue
	return False

def scroll_down_up_down():
	global driver
	try: feed = driver.find_element(By.XPATH, '//div[@role="feed"]')
	except: return
	feed.send_keys(Keys.PAGE_DOWN)
	sleep(2)
	feed.send_keys(Keys.PAGE_UP)
	sleep(2)
	feed.send_keys(Keys.PAGE_DOWN)
	sleep(2)
 
def add_business_to_csv(output_file, label, address, website, phone, name, info):
	string_to_write = ''
	string_to_write += f'{label}\\'
	string_to_write += f'{address}\\'
	string_to_write += f'{website}\\'
	string_to_write += f'{phone}\\'
	string_to_write += f'{name}\\'
	string_to_write += f'{info}\n'
	with open(output_file, 'a', encoding="utf-8") as f:
		f.write(string_to_write)

def scrape_new_business(search_text, continent, country, i):
    output_file = f'{g.DATA_FOLDERPATH}/organizations/fetch/gmap/{continent}/{country}/{search_industry}__{continent}__{country}.csv'.replace(' ', '_')

    old_businesses = get_old_businesses(output_file)
    business, label = find_new_business(old_businesses)

    if not business:
        scroll_down_up_down()
        return 'no_new_business_found'

    # google maps is bugged: scroll a bit the screen and try clicking again if needed
    if not click_on_listing(business):
        scroll_down_up_down()
        return 'failed_to_click_listing'

    sleep(5)

    card_element = get_card_element(business)

    name = scrape_name(card_element)
    address = scrape_address(card_element)
    website = scrape_website(card_element)
    phone = scrape_phone(card_element)

    name = sanitize(name)
    address = sanitize(address)
    phone = sanitize(phone)

    print(label)
    print(name)
    print(address)
    print(website)
    print(phone)

    element = card_element.find_element(By.XPATH, './/h1')
    next_sibling = element.find_element(
        By.XPATH,
        "../following-sibling::*[1]"
    )
    info = next_sibling.text.split('\n')

    if name != label:
        # add_business_to_csv(output_file, label, address, website, phone, name)
        return 'name_not_equal_label'
    else:
        add_business_to_csv(output_file, label, address, website, phone, name, info)

def fetch_organizations():
    geckodriver_path = 'geckodriver'
    driver_service = webdriver.FirefoxService(executable_path=geckodriver_path)
    driver = webdriver.Firefox(service=driver_service)
    driver.maximize_window()
    driver.get('https://www.google.com')
    sleep(2)
    driver.find_element(By.XPATH, '//div[text()="Rifiuta tutto"]').click()
    sleep(2)

continents = [
    'america',
    'europe',
]
scrapes_num = 15

for continent in continents[:]:
    rows = io.csv_read(f'{g.DATA_FOLDERPATH}/organizations/fetch/gmap/{continent}.csv')
    print('*********************************')
    print(continent)
    print(f'{i}/{len(rows)}')
    print('*********************************')

    for row in rows[:]:
        country = row[1].strip().lower()
        output_folder = f'{g.DATA_FOLDERPATH}/organizations/fetch/gmap/{continent}/{country}'.replace(' ', '_')
        io.folders_recursive_gen(output_folder)
        print('*********************************')
        print(continent, '>>', country)
        print(f'{i}/{len(rows)}')
        print('*********************************')

        search_industry = f'medicinal herb supplier'
        search_text = f'{search_industry}, {country}'
        driver.get(f'https://www.google.com/maps/search/{search_text}')
        sleep(10)

        for num in range(scrapes_num):
            err = scrape_new_business(search_text, continent, country, num)
            print(err, '\n')

def run():
    print('ORGANIZATIONS >> FETCH >> gmap')

    start = time.perf_counter()
    fetch_organizations()
    print(f'download html_form_master() - execution time: ', time.perf_counter() - start)

'''
old_businesses = []
business, label = find_new_business(old_businesses)

card_element = business.find_elements(By.XPATH, '//div[@role="main"]')[1]
element = card_element.find_element(By.XPATH, './/h1')
next_sibling = element.find_element(
    By.XPATH,
    "../following-sibling::*[1]"
)
info = next_sibling.text.split('\n')
button = next_sibling.find_element(By.XPATH, ".//button")

print(element)
return element
'''
