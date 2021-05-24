### 検索ツールサンプル
### これをベースに課題の内容を追記してください

# 検索ソース
source=["ねずこ","たんじろう","きょうじゅろう","ぎゆう","げんや","かなお","ぜんいつ"]

### 検索ツール
def search():
    word =input("鬼滅の登場人物の名前を入力してください >>> ")
  
    if word in source:
        print("{}が見つかりした".format(word))
        return
    print("{}が見つかりません".format(word))
    source.append(word)
    print(source)
        
if __name__ == "__main__":
    search()

# dataを読み込み
with open("./data.csv") as f:
    l_strip = [s.strip() for s in f.readlines()]
    source.append(l_strip)
    print(l_strip)

# data1csvに書き込み
import csv
with open("utf8.data1.csv", mode="w", encoding='utf8') as f:
    writer = csv.writer(f)
    writer.writerow(source)