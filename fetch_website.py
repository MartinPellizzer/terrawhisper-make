import os
import ast
import time
import json
import shutil

from lib import g
from lib import io
from lib import llm

import parse_utils

import re
import unicodedata

import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from urllib.robotparser import RobotFileParser

import re
import unicodedata

_NON_ALNUM = re.compile(r"[^\w\s-]", re.UNICODE)
_SEPARATORS = re.compile(r"[-\s]+")

def to_slug(name: str) -> str:
    """Convert an organization name into a stable, URL-safe slug."""
    name = unicodedata.normalize("NFKD", name)
    name = "".join(c for c in name if not unicodedata.combining(c))
    name = name.replace("&", " and ")
    name = _NON_ALNUM.sub("", name)
    return _SEPARATORS.sub("-", name).strip("-").lower()

def scrape_homepage(url):
    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    parsed = urlparse(url)
    user_agent = "SimpleHomepageScraper/1.0"

    # Check robots.txt
    robots_url = f"{parsed.scheme}://{parsed.netloc}/robots.txt"
    rp = RobotFileParser()

    try:
        r = requests.get(
            robots_url,
            headers={"User-Agent": user_agent},
            timeout=(5, 10),  # 5s connect, 10s read
        )
        if r.status_code == 200:
            rp.parse(r.text.splitlines())
    except requests.RequestException:
        # If robots.txt cannot be read, skip scraping
        return None

    if not rp.can_fetch(user_agent, url):
        # Scraping is not allowed, so skip
        return None

    # Download entire HTML
    try:
        response = requests.get(
            url,
            headers={"User-Agent": user_agent},
            timeout=(5, 10),  # 5s connect, 10s read
        )
        response.raise_for_status()
        return response.text

    except requests.RequestException:
        return None

def fetch_websites():
    input_folderpath = f'{g.DATA_FOLDERPATH}/organizations/fetch/gmap/america/places'.replace(' ', '_')
    output_folderpath = f'{g.DATA_FOLDERPATH}/organizations/fetch/websites/america/places'.replace(' ', '_')
    input_filenames = sorted(os.listdir(input_folderpath))
    start_i = 700
    end_i = 1000
    for input_filename_i, input_filename in enumerate(input_filenames[start_i:end_i]):
        input_filename_base = input_filename.split('.')[0].strip()
        input_filepath = f'{input_folderpath}/{input_filename}'
        place_folderpath = f'{output_folderpath}/{input_filename_base}'
        io.folders_recursive_gen(place_folderpath)
        with open(input_filepath, encoding="utf-8") as f: rows = f.read().strip().split('\n')
        for row in rows:
            print(f'{input_filename_i+start_i}/{len(input_filenames[:end_i])}')
            values = row.split('~')
            print(values)
            if values != [] and values != ['']:
                label = values[0]
                address = values[1]
                website = values[2]
                phone = values[3]
                name = values[4]
                info = values[5]
                slug = to_slug(label)
                print(f'label: {label}')
                print(f'address: {address}')
                print(f'website: {website}')
                print(f'phone: {phone}')
                print(f'name: {name}')
                print(f'info: {info}')
                print(f'slug: {slug}')
                print(f'***************************************')
                print()
                print(info)

                lst = ast.literal_eval(info)
                if 'Erborista' in lst:
                    # print('found')
                    slug = to_slug(label)
                    # print(slug)

                if website.strip() != '':
                    html = scrape_homepage(website)
                    if html is not None:
                        # print(html)
                        output_filepath = f'{place_folderpath}/{slug}.html'
                        io.file_write(output_filepath, html)
                        print(output_filepath)
                        print("Scraping ok.")
                        # quit()
                    else:
                        print("Scraping skipped or failed.")
                time.sleep(2)

def run():
    print(f'ORGANIZATION >> FETCH >> website')

    start = time.perf_counter()
    fetch_websites()
    print(f'fetch websites() - execution time: ', time.perf_counter() - start)

