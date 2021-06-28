import os
from selenium.webdriver import Chrome, ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager
def setup_class(cls):
    cls.driver = webdriver.Chrome(ChromeDriverManager().install())
import time
import pandas as pd

# Chromeを起動する関数


def set_driver(driver_path, headless_flg):
    # Chromeドライバーの読み込み
    options = ChromeOptions()

    # ヘッドレスモード（画面非表示モード）をの設定
    if headless_flg == True:
        options.add_argument('--headless')

    # 起動オプションの設定
    options.add_argument(
        '--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36')
    # options.add_argument('log-level=3')
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--ignore-ssl-errors')
    options.add_argument('--incognito')          # シークレットモードの設定を付与

    # ChromeのWebDriverオブジェクトを作成する。
    return Chrome(executable_path=os.getcwd() + "/" + driver_path, options=options)

# main処理

def main():   
    # 検索
    search_keyword =input("キーワードを入力してください >>> ")

    # driverを起動
    if os.name == 'nt': #Windows
        driver = set_driver("chromedriver.exe", False)
    elif os.name == 'posix': #Mac
        driver = set_driver("chromedriver", False)
    # Webサイトを開く
    driver.get("https://tenshoku.mynavi.jp/")
    time.sleep(5)
 
    try:
        # ポップアップを閉じる
        driver.execute_script('document.querySelector(".karte-close").click()')
        time.sleep(5)
        # ポップアップを閉じる
        driver.execute_script('document.querySelector(".karte-close").click()')
    except:
        pass
    
    # 検索窓に入力
    driver.find_element_by_class_name(
        "topSearch__text").send_keys(search_keyword)
    # 検索ボタンクリック
    driver.find_element_by_class_name("topSearch__button").click()

    #ページ終了まで繰り返し取得
    exp_name_list = []
   
    # 検索結果の一番上の会社名を取得
    name_list = driver.find_elements_by_css_selector(".cassetteRecruit .cassetteRecruit__name")


    # 1ページ分繰り返し
    print(len(name_list))
    for name in name_list:
        exp_name_list.append(name.text)
        print(name.text)

    #１ページ目会社情報取得
    exp_work_list=[] 
    exp_sarary_list=[]
    tables=[]
    trs =[] 

    tables = driver.find_elements_by_css_selector(".cassetteRecruit .tableCondition")
    print(len(tables))

    for table in tables:
        trs = table.find_elements_by_css_selector("tr")
        work = trs[2].find_element_by_css_selector("td")
        sarary = trs[3].find_element_by_css_selector("td")
        exp_work_list.append(work.text) 
        exp_sarary_list.append(sarary.text) 


    # 次のページクリック   
    #driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    # driver.find_element_by_class_name("pager__next").find_element_by_tag_name("a").click()
    while True:
        try:
            next_page_link = driver.find_element_by_css_selector(".iconFont--arrowLeft").get_attribute("href")
            driver.get(next_page_link)

            tables = driver.find_elements_by_css_selector(".cassetteRecruit .tableCondition")
            print(len(tables))

            for table in tables:
                trs = table.find_elements_by_css_selector("tr")
                work = trs[2].find_element_by_css_selector("td")
                sarary = trs[3].find_element_by_css_selector("td")
                exp_work_list.append(work.text) 
                exp_sarary_list.append(sarary.text) 


        except:
            break
    # Comment:2ページ目以降は、上記処理をwhileループにて繰り返すことで実現する
    # #２ページ目会社情報取得
    # name_list = driver.find_elements_by_class_name("cassetteRecruit__name")


    # # 1ページ分繰り返し
    # print(len(name_list))
    # for name in name_list:
    #     exp_name_list.append(name.text)
    #     print(name.text)



    # tables = driver.find_elements_by_css_selector("div.cassetteRecruit__main")
    # for table in tables:
    #     for tr in trs:
    #         trs = table.find_elements_by_css_selector("tr")
  
    # work_list = trs[2].find_elements_by_css_selector("td")
    # sarary_list = trs[4].find_elements_by_css_selector("td")

    # # 取得した要素を1つずつ表示
    # print(len(work_list))
    # for work in work_list:   
    #     exp_work_list.append(work.text) 
    #     print(work.text)
    
    # print(len(sarary_list))
    # for sarary in sarary_list:   
    #     exp_sarary_list.append(sarary.text) 
    #     print(sarary.text)       



    # CSVファイルに出力
    df = pd.DataFrame({'会社名': exp_name_list, 
                       '勤務先': exp_work_list, 
                       '年収': exp_sarary_list})
    print(df)
    df.to_csv("utf8.data1.csv", mode="w", index=False) 
    driver.quit()
   

# 直接起動された場合はmain()を起動(モジュールとして呼び出された場合は起動しないようにするため)
if __name__ == "__main__":
    main()
    
    