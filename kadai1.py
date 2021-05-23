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