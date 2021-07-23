#モジュールのインポート
from time import sleep
import datetime
import sys
import pandas as pd
import openpyxl

import gspread
import json
from google.oauth2.service_account import Credentials
from gspread_dataframe import get_as_dataframe, set_with_dataframe
#
import gspread_asyncio
#

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

#スプレッドシート設定
secret_credentials_json_oath =  './suumo2021-7-22-5e6f221249f8.json' 
scopes = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]
credentials = Credentials.from_service_account_file(
    secret_credentials_json_oath,
    scopes=scopes
)
gc = gspread.authorize(credentials)
# https://docs.google.com/spreadsheets/d/1pOJobvUDVLulU_N3NLpBC2u89adkICXsAzwxP-AaNww/edit#gid=0
workbook = gc.open_by_key('1pOJobvUDVLulU_N3NLpBC2u89adkICXsAzwxP-AaNww')
worksheet = gc.open("suumo").get_worksheet(1)

#
async def simple_gspread_asyncio(agcm):
    agc = await agcm.authorize()
    workbook = await agc.open_by_url("https://docs.google.com/spreadsheets/d/1pOJobvUDVLulU_N3NLpBC2u89adkICXsAzwxP-AaNww/")
    worksheet = await workbook.get_worksheet(0) 
#

# main処理
url = "https://suumo.jp/jj/chintai/ichiran/FR301FC001/?ar=030&bs=040&ra=013&cb=0.0&ct=9999999&et=9999999&cn=9999999&mb=0&mt=9999999&shkr1=03&shkr2=03&shkr3=03&shkr4=03&fw2=&ek=012520110&rn=0125&srch_navi=1%27&page={}"

for i in range(1,2):
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
            #CSV出力
            #df.to_csv("data1.csv", mode="w", index=False, encoding='cp932') 
            #excel出力
            #df.to_excel('data1.xlsx', sheet_name='suumo', index=False)
            #スプレッドシート出力      
            update_sheet = workbook.worksheet("シート1")
            set_with_dataframe(update_sheet, df,resize=True, include_index=False)