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

file = open("C:\\Users\\OP745\\Desktop\\data.csv", 'r')
f_list = file.readlines()
file.close()
# リストから1行ずつ読み込む
for f_line in f_list:
    source.append(f_line)
    print(f_line) 

# data1csvに書き込み
import csv
f = open('utf8.data1.csv', 'w', encoding='utf8')
writer = csv.writer(f)
writer.writerow(source)
f.close()