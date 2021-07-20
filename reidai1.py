#モジュールのインポート
from bs4 import BeautifulSoup
from time import sleep
import requests
import datetime
import sys
import pandas as pd
sys.path.insert(0,'/usr/lib/chromium-browser/chromedriver')
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException

options = Options()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--user-agent=Mozilla/5.0 (X11; Linux x86_64; rv:61.0) Gecko/20100101 Firefox/61.0')

df = pd.DataFrame()
name=[]
rent=[]
deposit=[]
gratuity=[]

url = "https://suumo.jp/jj/chintai/ichiran/FR301FC001/?ar=030&bs=040&ra=013&cb=0.0&ct=9999999&et=9999999&cn=9999999&mb=0&mt=9999999&shkr1=03&shkr2=03&shkr3=03&shkr4=03&fw2=&ek=012520110&rn=0125&srch_navi=1%27&page={}"

for i in range(1,4):
    target_url= url.format(i) 
    #print(target_url)
    sleep(1)
    driver = webdriver.Chrome('chromedriver',options=options)
    driver.get(target_url)

#不動産情報を取得してくる

    for casset in driver.find_elements(By.CLASS_NAME, 'cassetteitem'):
    #物件名を出力する
        #print(casset.find_element(By.CLASS_NAME, 'cassetteitem_content-title').text)
        name=(casset.find_element(By.CLASS_NAME, 'cassetteitem_content-title').text)

    #家賃を出力する
        rents = casset.find_elements(By.CLASS_NAME, 'cassetteitem_price--rent')

    #敷金を出力する
        deposits = casset.find_elements(By.CLASS_NAME, 'cassetteitem_price--deposit')

    #礼金を出力する
        gratuitys = casset.find_elements(By.CLASS_NAME, 'cassetteitem_price--gratuity')

        for rent, deposit, gratuity in zip(rents, deposits, gratuitys):
            #print(f'{rent.text}, {deposit.text}, {gratuity.text}') 

            df = df.append(
                    {'物件名': name, '家賃': rent.text, '敷金': deposit.text,
                     '礼金': gratuity.text}, ignore_index=True) 
       
            print(df)

            df.to_csv("utf8.data1.csv", mode="w", index=False) 