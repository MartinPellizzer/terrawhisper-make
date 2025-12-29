
jsons_filenames = os.listdir(f'{g.pinterest_tmp_image_folderpath}/pins')
article_filename = ''
i = 0
for _json_filename in jsons_filenames:
    json_n = int(_json_filename.split('.')[0])
    if json_n == i:
        found = True
        article_filename = _json_filename
        break

article_filepath = f'{g.pinterest_tmp_image_folderpath}/pins/{article_filename}'
print(f'{i}/{len(jsons_filenames)} >> {article_filepath}')

data = io.json_read(article_filepath)
title = data['title'].title()
url = data["url"]
img_filepath = data['img_filepath']
description = data['description']
board_name = data['board_name']
# LOG
print('ARTICLE_FILEPATH: ' + article_filepath)
print('TITLE: ' + title)
print('URL: ' + url)
print('IMG_FILEPATH: ' + img_filepath)
print('DESCRIPTION: ' + description)
try:
    driver.get("https://www.pinterest.com/pin-creation-tool/")
except:
    pass
    # failed_pins_num += 1
    # return
time.sleep(10)
try:
    e = driver.find_element(By.XPATH, '//input[@id="storyboard-upload-input"]')
except:
    pass
    # failed_pins_num += 1
    # return
img_filepath_formatted = img_filepath
e.send_keys(f'{img_filepath_formatted}') 
time.sleep(10)
e = driver.find_element(By.XPATH, '//input[@id="storyboard-selector-title"]')
for c in title:
    try: e.send_keys(c)
    except: break
time.sleep(5) 
e = driver.find_element(By.XPATH, "//div[@class='notranslate public-DraftEditor-content']")
for c in description:
    try: e.send_keys(c)
    except: break
time.sleep(5)

success = False
for _ in range(5):
    e = driver.find_element(By.XPATH, '//input[@id="WebsiteField"]')
    e.send_keys(Keys.CONTROL + "a")
    e.send_keys(Keys.BACKSPACE)
    for c in url:
        try: e.send_keys(c)
        except: break
    time.sleep(1) 
    written_text = e.get_attribute('value')
    if url == written_text:
        print('success')
        success = True
        break
    else:
        print('fail')
if not success:
    return

e = driver.find_element(By.XPATH, '//input[@id="WebsiteField"]')
