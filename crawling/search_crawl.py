import urllib.request
from urllib.request import (urlopen, urlparse, urlretrieve)

from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

import numpy as np
import pandas as pd

import os
import time
import shutil
import unicodedata

driver_path = "/home/chkim/SeniorProject/chromedriver"

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('headless')
chrome_options.add_argument("--window-size=1920,1080")
chrome_options.add_argument("disable-gpu")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

def scroll_down():
    SCROLL_PAUSE_SEC = 2

    last_height = driver.execute_script("return document.body.scrollHeight")
    
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(SCROLL_PAUSE_SEC)
        new_height = driver.execute_script("return document.body.scrollHeight")

        if new_height == last_height:
            try:
                driver.find_element(By.CLASS_NAME, "mye4qd").click()
            except:
                break
        last_height = new_height

def create_dir_if_not_exist(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

#item_list = ['코카콜라 캔', 'coca cola can', '닥터페퍼 캔', 'dr pepper can', '파워에이드 캔', 'powerade can', '포카리스웨트 캔', 'pocari sweat can', '펩시 캔', 'pepsi can', '칠성 사이다 캔', 'chilsung cider can', '게토레이 캔', 'gatorade can', '데미소다 애플', 'demisoda apple can']
item_list = ['환타 오렌지 캔', 'fanta orange', '웰치스 포도 캔', 'welchs grape', '이프로 복숭아 캔', '2% peach']

if os.path.exists("./new_classes/"):
    try:
        shutil.rmtree("./new_classes/")
        print("Directory \"new_classes\" remove complete")
        print()
    except:
        pass

for i in range(len(item_list)):
    image_name = item_list[i]

    #driver.get("http://www.google.co.kr/imghp?hl=ko")
    driver.get("http://www.google.com/imghp?hl=en")
    browser = driver.find_element(By.NAME, 'q')
    browser.send_keys(item_list[i])
    browser.send_keys(Keys.RETURN)
    
    scroll_down()
    
    image = driver.find_elements(By.CLASS_NAME, "rg_i.Q4LuWd")

    if i % 2 == 0:
        ko_term_url = []
        for j in image:
            if j.get_attribute("src") != None:
                ko_term_url.append(j.get_attribute("src"))
            else:
                ko_term_url.append(j.get_attribute("data-src"))
    else:
        en_term_url = []
        '''
        for j in image:
            if j.get_attribute("src") != None:
                en_term_url.append(j.get_attribute("src"))
            else:
                en_term_url.append(j.get_attribute("data-src"))
        '''

    w1 = 45
    if i % 2 == 0:
        ko_term_url = pd.DataFrame(ko_term_url)[0].unique()
        
        no_of_wide_chars = sum(1 for c in image_name if unicodedata.east_asian_width(c) in 'WF')
        w1 = w1 - no_of_wide_chars
        print(f"{image_name:<{w1}}| number of images : {len(ko_term_url)}")
        
        continue
    else:
        #en_term_url = pd.DataFrame(en_term_url)[0].unique()
        
        print(f"{image_name:<{w1}}| number of images : {len(en_term_url)}")

    #image_url = np.concatenate([ko_term_url, en_term_url])
    image_url = ko_term_url

    save_path = f"./new_classes/{item_list[i]}/"
    create_dir_if_not_exist(save_path)

    for t, url in enumerate(image_url, 0):
        urlretrieve(url, save_path + image_name + "_" + str(t) + ".jpg")
    
    w2 = 15
    no_of_wide_chars = sum(1 for c in item_list[i-1] if unicodedata.east_asian_width(c) in 'WF')
    w2 = w2 - no_of_wide_chars
    print(f"{item_list[i-1]:<{w2}} and {item_list[i]:<25}| save complete")
    print()

print("Done")
driver.close()
