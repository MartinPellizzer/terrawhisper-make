import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options

from lib import g
from lib import io


with open('/home/ubuntu/vault/terrawhisper/accounts/buffer-username.txt') as f: username = f.read().strip()
with open('/home/ubuntu/vault/terrawhisper/accounts/buffer-password.txt') as f: password = f.read().strip()


geckodriver_path = 'geckodriver'
driver_service = webdriver.FirefoxService(executable_path=geckodriver_path)

driver = webdriver.Firefox(service=driver_service)
driver.get('https://www.google.com')
driver.maximize_window()
driver.get("https://login.buffer.com/login")
time.sleep(10)
e = driver.find_element(By.XPATH, '//input[@type="email"]')
e.send_keys(username) 
time.sleep(5)
e = driver.find_element(By.XPATH, '//input[@type="password"]')
e.send_keys(password) 
time.sleep(5)
e = driver.find_element(By.XPATH, '//button[@id="login-form-submit"]')
e.click()
time.sleep(5)

i = 0
running = True
while running:
    twitter_posts_filepath = f'{g.twitter_folderpath}/posts.json'
    twitter_posts_json = io.json_read(twitter_posts_filepath)
    posts = [post for post in twitter_posts_json['posts'] if post['posted'] == 0]
    if posts == []: 
        running = False
        break 
    ###
    post = posts[0]
    post_content = post['content']
    driver.get("https://publish.buffer.com/all-channels")
    time.sleep(10)
    driver.find_element(By.XPATH, '//button[contains(text(), "New")]').click()
    time.sleep(10)
    driver.find_element(By.XPATH, '//label[contains(text(), "Post")]').click()
    time.sleep(10)
    e = driver.find_element(By.XPATH, '//div[@aria-label="composer textbox"]')
    time.sleep(5)
    e.click()
    for c in post_content:
        e.send_keys(c)
    time.sleep(10)
    driver.find_element(By.XPATH, '//div[contains(text(), "Add to Queue")]').click()
    time.sleep(10)
    post['posted'] = 1
    io.json_write(twitter_posts_filepath, twitter_posts_json)
    time.sleep(10)

    i += 1
    if i >= 3: running = False
