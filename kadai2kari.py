import os
from selenium.webdriver import Chrome, ChromeOptions
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

    # ページ終了まで繰り返し取得
    exp_name_list = []
    exp_neshu_list = []
    exp_kinmuchi_list = []


    # 検索結果の一番上の会社名を取得
    name_list = driver.find_elements_by_class_name("cassetteRecruit__name")



    # 1ページ分繰り返し
    print(len(name_list))
    for name in name_list:
        exp_name_list.append(name.text)
        print(name.text)
        
    # xpathを定義してfind関数で要素をリストで取得(年収)
    xpath ="//tr[3]/td" 
    elems = driver.find_elements_by_xpath(xpath)
    # 取得した要素を1つずつ表示
    for elem in elems:
        exp_neshu_list.append(elem.text)
        print(elem.text)
    
    # xpathを定義してfind関数で要素をリストで取得(勤務地)
    xpath ="//tr[5]/td" 
    elems = driver.find_elements_by_xpath(xpath)
    # 取得した要素を1つずつ表示
    for elem in elems:
        exp_kinmuchi_list.append(elem.text)
        print(elem.text)

    # 次のページクリック   
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    driver.find_element_by_class_name("pager__next").find_element_by_tag_name("a").click()
    
    
    # 検索結果の一番上の会社名を取得
    name_list = driver.find_elements_by_class_name("cassetteRecruit__name")
  
    # 1ページ分繰り返し
    print(len(name_list))
    for name in name_list:
        exp_name_list.append(name.text)
        print(name.text)
    
    # xpathを定義してfind関数で要素をリストで取得(年収)
    xpath ="//tr[3]/td" 
    elems = driver.find_elements_by_css_selector("body > div.wrapper > div:nth-child(5)")
    # 取得した要素を1つずつ表示
    for elem in elems:
        exp_neshu_list.append(elem.text)
        print(elem.text)
    

    # xpathを定義してfind関数で要素をリストで取得(勤務地)
    xpath ="//tr[5]/td" 
    elems = driver.find_elements_by_xpath(xpath)
    # 取得した要素を1つずつ表示
    for elem in elems:
        exp_kinmuchi_list.append(elem.text)
        print(elem.text)

    # CSVファイルに出力
    d = {'会社名': exp_name_list, '勤務先': exp_neshu_list, '年収': exp_kinmuchi_list}
    df = pd.DataFrame(d.values(), index=d.keys()).T
    print(df)
    df.to_csv("utf8.data1.csv","a") 

# 直接起動された場合はmain()を起動(モジュールとして呼び出された場合は起動しないようにするため)
if __name__ == "__main__":
    main()
    
    