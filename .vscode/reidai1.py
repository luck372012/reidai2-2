#モジュールのインポート
from time import sleep
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

base_url = 'https://suumo.jp/jj/chintai/ichiran/FR301FC001/?ar=030&bs=040&ra=013&cb=0.0&ct=9999999&et=9999999&cn=9999999&mb=0&mt=9999999&shkr1=03&shkr2=03&shkr3=03&shkr4=03&fw2=&ek=012520110&rn=0125&srch_navi=1'

driver = webdriver.Chrome('chromedriver',options=options)
driver.get(base_url)


#不動産情報を取得してくる

for casset in driver.find_elements(By.CLASS_NAME, 'cassetteitem'):
 # 物件名を出力する
    print(casset.find_element(By.CLASS_NAME, 'cassetteitem_content-title').text)
   
tables=[]
trs =[] 
df = pd.DataFrame()
  #家賃を出力する
tables = driver.find_elements_by_css_selector("div.cassetteitem-item > table")
for table in tables:
    trs = table.find_elements_by_css_selector("tr")  

    rent = trs[0].find_elements_by_css_selector("tr > td:nth-child(4) > ul > li:nth-child(1) > span > span")
    print(rent.text)

  #敷金を出力する
#tables = driver.find_elements_by_css_selector("div.cassetteitem-item > table")
#for table in tables:
   # deposits = table.find_elements_by_css_selector("tr >td:nth-child(5) > ul > li:nth-child(1) > span")
    #for deposit in deposits:
        #print(deposit.text)

    

    #deposit = trs[0].find_element_by_css_selector("tr > td:nth-child(5) > ul > li:nth-child(1) > span").text
    #print(deposit.text)

  #礼金を出力する
#tables = driver.find_elements_by_css_selector("div.cassetteitem-item > table")
#for gratuity in gratuity:
    #gratuitys = table.find_elements_by_css_selector("tr > td:nth-child(5) > ul > li:nth-child(2) > span")
   # for gratuity in gratuitys:
      #  print(gratuity.text)



    #gratuity = trs[0].find_element_by_css_selector("tr > td:nth-child(5) > ul > li:nth-child(2) > span").text
    #print(gratuity.text)

    df = pd.DataFrame()
    df = df.append(
          {"物件名":(casset.find_element(By.CLASS_NAME, 'cassetteitem_content-title').text), 
           "家賃": rent,
             #"敷金": deposit
             },
             #"礼金": gratuity）, 
              ignore_index=True)
    
print(df)