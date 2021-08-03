"""
#webdriver自動更新
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
options = webdriver.ChromeOptions()
options.add_argument('--headless')
# webdriver格納パスを指定する場合
custom_path = "./chromedriver/"
# webdriver.exeのパス
driver_path = ChromeDriverManager(path=custom_path).install()
driver = webdriver.Chrome(driver_path, options=options)
"""

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
 
from time import sleep
import datetime
import sys
import pandas as pd
import openpyxl

import gspread
import json
from oauth2client.service_account import ServiceAccountCredentials
from gspread_dataframe import get_as_dataframe, set_with_dataframe

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
names=[]

#Googleスプレッドシートの初期化
SCOPES = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
#CRED = ServiceAccountCredentials.from_json_keyfile_name('sheet_key_prod.json', SCOPES)  #PROD
CRED = ServiceAccountCredentials.from_json_keyfile_name('ullet2021-7-27-948b864dc90d.json', SCOPES)  #DEV
gc = gspread.authorize(CRED)

# https://docs.google.com/spreadsheets/d/1_Ghg0HTIvNf_HExc6KWMrwe7-pZoqyg7LfkAuDkJQXo/edit#gid=0
workbook = gc.open_by_key('1_Ghg0HTIvNf_HExc6KWMrwe7-pZoqyg7LfkAuDkJQXo')
worksheet = gc.open("ullet").get_worksheet(1)



# main処理
url = "http://www.ullet.com/search.html#page/{}"

for i in range(1,3):
    target_url= url.format(i) 
    print(target_url)
    sleep(1)
    driver = webdriver.Chrome('chromedriver',options=options)
    driver.get(target_url)

#会社名を取得してくる
    table = driver.find_elements_by_tag_name("table")[1] 
    class_names=table.find_elements_by_class_name("company_name")
    for name in class_names:     
        print(name.text)
     
        df = df.append(
                    {'会社名': name.text}, ignore_index=True) 




#CSV出力
df.to_csv("data1.csv", mode="w", index=False, encoding='cp932') 
#excel出力
df.to_excel('data1.xlsx', sheet_name='ullet', index=False)

#スプレッドシート出力
#print(df)      
update_sheet = workbook.worksheet("シート1")
set_with_dataframe(update_sheet, df,resize=True, include_index=False)